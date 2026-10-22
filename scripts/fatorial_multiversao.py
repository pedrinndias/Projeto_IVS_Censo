"""Fatorial multiversão a partir do relatório parcial corrigido (out/2026), camadas 1 a 3.

Prompt: `docs/prompts/prompt_fatorial_multiversao_2026-10.md` · estado:
`docs/prompts/estado_fatorial_multiversao_2026-10.md`.

    ./.venv/bin/python scripts/fatorial_multiversao.py --camada 1|2|3

Camada 1: as 4.017 combinações das 12 variáveis do Quadro 2, uma fatorial cada (eixo principal,
2 fatores), em duas réguas (postos no conjunto e postos dentro do município). Camada 2: os 9
métodos de rotação e peso do NB05 × 3 normalizações × sigilo do analfabetismo sobre 13 conjuntos.
Camada 3: os finalistas, estabilidade por município, replicação entre metades e o IVS proposto.
Reaproveita o motor do NB05 (`ivs_especificacoes.py`) e a base de `eda_versoes.py`.
"""
from __future__ import annotations

import argparse
import itertools
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'src', RAIZ / 'scripts'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import eda_versoes as ev  # noqa: E402
import fatorial_ampliada as fa  # noqa: E402
import ivs_especificacoes as ie  # noqa: E402
from ivs_censo.fatorial import (fatoracao_eixo_principal, horn, kmo,  # noqa: E402
                                alinhar_cargas, postos, rodar_cenario, rotacao_promax)

SAIDA = RAIZ / 'banco_de_dados' / 'eda' / 'fatorial_multiversao'
SEMENTE = 42
VARS = {'AGU': 'pct_agua_inad', 'ESG': 'pct_esgoto_inad', 'LIX': 'pct_lixo_inad',
        'MOR': 'razao_moradores', 'ANA': 'pct_analfab', 'REN': 'renda_inv',
        'PPI': 'pct_raca_pretpardind', 'CAN': 'pct_sem_agua_canalizada', 'BAN': 'pct_sem_banheiro',
        'MNC': 'pct_moradia_nao_convencional', 'IDO': 'pct_idoso_60mais', 'CRI': 'pct_pop_0a14'}
COD = {v: k for k, v in VARS.items()}
NUCLEO = ['AGU', 'ESG', 'LIX', 'MOR', 'ANA', 'REN', 'PPI']
COMPLEMENTARES = ['CAN', 'BAN', 'MNC', 'IDO', 'CRI']
REGUAS = ('global', 'municipal')
CRIT = ie.CRIT
EQUIV = {'spearman': 0.95, 'troca': 0.10}
EXTRACAO = 'eixo_principal'   # a mesma da camada 1; com ACP o lixo vira um fator sozinho (NB04, achado 8)
PISO_MUN = ie.PISO_MUN    # setores por município para entrar nas medianas "dentro do município"
REF = {'conjunto': 'nucleo', 'rotacao': 'promax', 'metodo': '60_40', 'normalizacao': 'municipal',
       'sigilo': 'ausente'}


def carregar() -> pd.DataFrame:
    """Recorte do relatório (104.108 urbanos OK) pela mesma base das análises de outubro."""
    cfg = {'base': 'entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db', 'indicadores': 'todos',
           'recorte': {'urbano': True, 'dados_sig': 'OK', 'piso_pop': None, 'municipios': None},
           'indice': {'renda': 'sem_extremo'}}
    return ev.montar_base(cfg).df


def matriz(d: pd.DataFrame, cols: list[str], regua: str) -> np.ndarray:
    """Spearman no conjunto (postos globais) ou dentro do município (postos percentis por município)."""
    if regua == 'global':
        return np.corrcoef(postos(d[cols].to_numpy()), rowvar=False)
    return np.corrcoef(d.groupby('NM_MUN')[cols].rank(pct=True).to_numpy(), rowvar=False)


def diagnostico(R: np.ndarray, cols: list[str], horn_p: np.ndarray) -> tuple[dict, np.ndarray, np.ndarray]:
    """Estrutura de uma combinação: adequação, número de fatores e eixo principal com promax
    (e as comunalidades e os MSA, que a camada 1 grava por variável)."""
    k_, msa = kmo(R)
    val = np.sort(np.linalg.eigvalsh(R))[::-1]
    L, h2, info = fatoracao_eixo_principal(R, 2)
    P, _, phi = rotacao_promax(L)
    carga = np.abs(P).max(axis=1)
    d = {'kmo': k_, 'msa_min': msa.min(), 'msa_min_var': COD[cols[int(msa.argmin())]],
         'kaiser': int((val > 1).sum()), 'horn': int((val > horn_p).sum()),
         'h2_min': h2.min(), 'h2_min_var': COD[cols[int(h2.argmin())]],
         'carga_min': carga.min(), 'phi': abs(phi[0, 1]), 'heywood': info['heywood']}
    d['elegivel'] = bool(k_ >= CRIT['kmo'] and msa.min() >= CRIT['msa'] and h2.min() >= CRIT['h2']
                         and carga.min() >= CRIT['carga'])
    return d, h2, msa


# ─────────────────────────────────────────────────────────────────────────────
# Camada 1
# ─────────────────────────────────────────────────────────────────────────────
def subconjuntos() -> list[tuple[str, ...]]:
    return [c for k in range(3, 13) for c in itertools.combinations(VARS, k)]


def efeito_variavel(sub: pd.DataFrame) -> pd.DataFrame:
    """Pares de combinações que diferem só numa variável: o que muda quando ela entra."""
    regs = []
    for regua, g in sub.groupby('regua'):
        chave = g.set_index('codigos')
        for v in VARS:
            com = g[g[v] == 1]
            pares = [(c, '+'.join(x for x in c.split('+') if x != v)) for c in com['codigos']]
            pares = [(c, s) for c, s in pares if s in chave.index]
            a, b = chave.loc[[c for c, _ in pares]], chave.loc[[s for _, s in pares]]
            regs.append({'regua': regua, 'codigo': v, 'variavel': VARS[v], 'pares': len(pares),
                         'delta_kmo_mediana': float(np.median(a['kmo'].to_numpy() - b['kmo'].to_numpy())),
                         'delta_n_mediana': float(np.median(a['n'].to_numpy() - b['n'].to_numpy())),
                         'elegivel_sem': float(b['elegivel'].mean()), 'elegivel_com': float(a['elegivel'].mean()),
                         'derruba_elegibilidade': float((b['elegivel'].to_numpy() & ~a['elegivel'].to_numpy()).mean()),
                         'h2_mediana': float(com[f'h2_{v}'].median()),
                         'msa_mediana': float(com[f'msa_{v}'].median())})
    return pd.DataFrame(regs)


def fatorial_completa(d: pd.DataFrame, codigos: list[str], regua: str) -> dict:
    """Uma fatorial "para mostrar": matriz, anti-imagem, autovalores, cargas em todas as rotações."""
    cols = [VARS[c] for c in codigos]
    s = d.dropna(subset=cols)
    R = matriz(s, cols, regua)
    r = rodar_cenario(postos(s[cols].to_numpy()) if regua == 'global'
                      else s.groupby('NM_MUN')[cols].rank(pct=True).to_numpy(),
                      metodo='pearson', com_horn=True, extracao='eixo_principal')
    Rinv = np.linalg.inv(R)
    dg = np.sqrt(np.diag(Rinv))
    anti = -Rinv / np.outer(dg, dg)
    np.fill_diagonal(anti, r['msa'])
    return {'n': len(s), 'R': R, 'anti': anti, 'r': r, 'codigos': codigos}


def gravar_fatorial(f: dict, nome: str) -> None:
    c, r = f['codigos'], f['r']
    pd.DataFrame(f['R'], index=c, columns=c).to_csv(SAIDA / f'{nome}_correlacao.csv', float_format='%.6g')
    pd.DataFrame(f['anti'], index=c, columns=c).to_csv(SAIDA / f'{nome}_antiimagem.csv', float_format='%.6g')
    pd.DataFrame({'componente': range(1, len(c) + 1), 'autovalor': r['autovalores'], 'horn': r['horn']}
                 ).to_csv(SAIDA / f'{nome}_autovalores.csv', index=False, float_format='%.6g')
    cargas = pd.DataFrame({'codigo': c, 'msa': r['msa'], 'h2': r['comunalidade'],
                           'h2_obliqua': r['comunalidade_obliqua']})
    for nm, M in (('sem_rotacao', r['sem_rotacao']), ('varimax', r['varimax']),
                  ('promax_padrao', r['promax_padrao']), ('promax_estrutura', r['promax_estrutura'])):
        for j in range(2):
            cargas[f'{nm}_F{j + 1}'] = M[:, j]
    cargas.to_csv(SAIDA / f'{nome}_cargas.csv', index=False, float_format='%.6g')
    pd.DataFrame([{'n': f['n'], 'kmo': r['kmo'], 'bartlett_qui2': r['bartlett_qui2'],
                   'bartlett_gl': r['bartlett_gl'], 'det_R': r['det_R'], 'kaiser': r['kaiser'],
                   'horn': r['horn_retidos'], 'var_explicada_2': r['var_explicada_k'],
                   'phi': r['phi'][0, 1]}]).to_csv(SAIDA / f'{nome}_adequacao.csv', index=False,
                                                   float_format='%.6g')


def camada1(df: pd.DataFrame) -> None:
    t0 = time.time()
    horn_p = {p: horn(20000, p, semente=SEMENTE) for p in range(3, 13)}   # n ≥ 20 mil em todas: Horn só depende de p
    regs = []
    for i, comb in enumerate(subconjuntos()):
        cols = [VARS[c] for c in comb]
        s = df.dropna(subset=cols)
        for regua in REGUAS:
            R = matriz(s, cols, regua)
            dg, h2, msa = diagnostico(R, cols, horn_p[len(cols)])
            linha = {'codigos': '+'.join(comb), 'p': len(comb), 'regua': regua, 'n': len(s),
                     'pct_recorte': len(s) / len(df), **{c: int(c in comb) for c in VARS},
                     'demografia_dupla': int('IDO' in comb and 'CRI' in comb), **dg}
            linha.update({f'h2_{c}': h for c, h in zip(comb, h2)})
            linha.update({f'msa_{c}': m for c, m in zip(comb, msa)})
            regs.append(linha)
        if i % 500 == 0:
            print(f'  {i}/4017  {time.time() - t0:.0f} s', flush=True)
    sub = pd.DataFrame(regs)
    sub.to_csv(SAIDA / 'camada1_subconjuntos.csv', index=False, float_format='%.6g')
    efeito_variavel(sub).to_csv(SAIDA / 'camada1_efeito_variavel.csv', index=False, float_format='%.6g')
    for regua in REGUAS:
        gravar_fatorial(fatorial_completa(df, list(VARS), regua), f'camada1_12_{regua}')
        gravar_fatorial(fatorial_completa(df, NUCLEO, regua), f'camada1_nucleo_{regua}')
    print(f'camada 1: {len(sub)} linhas em {time.time() - t0:.0f} s')


# ─────────────────────────────────────────────────────────────────────────────
# Camada 2
# ─────────────────────────────────────────────────────────────────────────────
NORMALIZACOES = ('municipal', 'global', 'postos_municipal')
SIGILOS = ('ausente', 'piso', 'zero')


def conjuntos() -> dict[str, list[str]]:
    """Os 13: o núcleo, o núcleo menos cada uma das 7 e o núcleo mais cada complementar."""
    c = {'nucleo': NUCLEO}
    c.update({f'nucleo-{v}': [x for x in NUCLEO if x != v] for v in NUCLEO})
    c.update({f'nucleo+{v}': NUCLEO + [v] for v in COMPLEMENTARES})
    return c


def com_sigilo(df: pd.DataFrame, sigilo: str) -> pd.DataFrame:
    """Analfabetismo suprimido: ausente, piso (um analfabeto no setor: 1/(V00900+1), o 3,14% da EDA
    §14.1) ou zero."""
    if sigilo == 'ausente':
        return df
    d = df.copy()
    falta = d['pct_analfab'].isna()
    d.loc[falta, 'pct_analfab'] = 1 / (d.loc[falta, 'V00900'] + 1) if sigilo == 'piso' else 0.0
    return d


def ancora(cols: list[str]) -> list[str]:
    """`ie.reparticoes` acha a dimensão socioeconômica pela coluna 'renda_inv'; sem a renda, a
    âncora passa ao analfabetismo e, sem ele, à cor/raça (só o rótulo muda, não os dados)."""
    if 'renda_inv' in cols:
        return cols
    alvo = next(c for c in ('pct_analfab', 'pct_raca_pretpardind') if c in cols)
    return ['renda_inv' if c == alvo else c for c in cols]


def elegivel(r: dict, rot: str) -> dict:
    M, h2 = ie.cargas_rotacao(r, rot)
    carga = np.abs(M).max(axis=1)
    e = {'kmo': r['kmo'], 'msa_min': r['msa'].min(), 'h2_min': h2.min(), 'carga_min': carga.min()}
    e['elegivel'] = bool(e['kmo'] >= CRIT['kmo'] and e['msa_min'] >= CRIT['msa']
                         and e['h2_min'] >= CRIT['h2'] and e['carga_min'] >= CRIT['carga'])
    return e


def sinais(M: np.ndarray) -> np.ndarray:
    """+1/−1 por variável: o sinal da carga na própria dimensão. Variável com carga negativa (ex.:
    idosos) entra invertida, senão o peso — que vem do quadrado da carga — a somaria ao contrário."""
    dim = np.abs(M).argmax(axis=1)
    return np.sign(M[np.arange(len(M)), dim])


def indice_norm(d: pd.DataFrame, cols: list[str], w: np.ndarray, sinal: np.ndarray, norm: str) -> np.ndarray:
    """Índice 0–1: soma ponderada dos componentes normalizados (o `ie.indice` do NB05, mais postos)."""
    x = d[cols] * sinal
    x = pd.concat([x, d[['NM_MUN']]], axis=1)
    if norm in ('municipal', 'global'):
        return ie.indice(x, cols, w, norm)
    sem_variacao = ~x.groupby('NM_MUN')[cols].transform(lambda s: s.max() > s.min()).any(axis=1)
    v = (x.groupby('NM_MUN')[cols].rank(pct=True) * w).sum(axis=1)
    return v.where(~sem_variacao).to_numpy()


def faixas_ivs(v, mun) -> dict:
    return {'faixa_ivs_bh': ie.faixas(v, mun, 'ivs_bh'), 'faixa_quartis': ie.faixas(v, mun, 'quartis')}


def rodar_base(df: pd.DataFrame, nome: str, codigos: list[str], sigilo: str):
    """As 9 × 3 especificações de um conjunto com uma política de sigilo."""
    cols = [VARS[c] for c in codigos]
    d = com_sigilo(df, sigilo).dropna(subset=cols).reset_index(drop=True)
    rodadas = {'spearman': rodar_cenario(d[cols].to_numpy(), com_horn=False, extracao=EXTRACAO),
               'mun': rodar_cenario(d.groupby('NM_MUN')[cols].rank(pct=True).to_numpy(),
                                    metodo='pearson', com_horn=False, extracao=EXTRACAO)}
    fcu = d['is_fcu'].to_numpy(dtype=float)
    ok = ~np.isnan(fcu)
    okr = ok & d['renda_inv'].notna().to_numpy()      # sem a renda no conjunto, ela pode faltar
    auc_renda = fa.auc_postos(d['renda_inv'].to_numpy()[okr], fcu[okr])
    for norm in NORMALIZACOES:
        r = rodadas['mun' if norm == 'postos_municipal' else 'spearman']
        for (rot, met), (M, rep) in ie.reparticoes(r, ancora(cols)).items():
            w = fa.pesos_indice(M, rep)
            s = sinais(M)
            v = indice_norm(d, cols, w, s, norm)
            ok2 = ok & ~np.isnan(v)
            esp = {'conjunto': nome, 'codigos': '+'.join(codigos), 'p': len(codigos), 'sigilo': sigilo,
                   'rotacao': rot, 'metodo': met, 'normalizacao': norm, 'n': len(d),
                   'pct_recorte': len(d) / len(df), 'peso_F1': ie.peso_f1(M, rep, ancora(cols)),
                   **elegivel(r, rot), 'phi': r['phi'][0, 1],
                   'auc_fcu': fa.auc_postos(v[ok2], fcu[ok2]), 'auc_renda_sozinha': auc_renda,
                   'auc_fcu_mun': ie.auc_municipal(v[ok2], fcu[ok2], d['NM_MUN'].to_numpy()[ok2])[0],
                   **{f'peso_{COD[c]}': x * sg for c, x, sg in zip(cols, w, s)}}
            yield esp, pd.Series(v, index=d['CD_SETOR'])


def eixo_de(esp: dict) -> str | None:
    """Em qual eixo esta especificação difere da referência (None: é a referência; '': mais de um)."""
    dif = [k for k in ('conjunto', 'sigilo', 'normalizacao') if esp[k] != REF[k]]
    if (esp['rotacao'], esp['metodo']) != (REF['rotacao'], REF['metodo']):
        dif.append('rotacao_peso')
    return None if not dif else (dif[0] if len(dif) == 1 else '')


def camada2(df: pd.DataFrame) -> None:
    t0 = time.time()
    regs, vetores = [], {}
    for nome, codigos in conjuntos().items():
        for sigilo in (SIGILOS if 'ANA' in codigos else ('ausente',)):
            for esp, v in rodar_base(df, nome, codigos, sigilo):
                e = eixo_de(esp)
                esp['eixo'] = 'referencia' if e is None else e
                regs.append(esp)
                if e != '':
                    vetores[len(regs) - 1] = v
        print(f'  {nome}: {time.time() - t0:.0f} s', flush=True)
    esp = pd.DataFrame(regs)
    esp['id'] = [f'E{i + 1:04d}' for i in range(len(esp))]
    # comparações com a referência, na amostra comum, para as especificações de um eixo só
    mun = df.set_index('CD_SETOR')['NM_MUN']
    iref = int(esp.index[esp['eixo'] == 'referencia'][0])
    ref = vetores[iref].reindex(df['CD_SETOR']).to_numpy()
    comps = []
    for i, v in vetores.items():
        c = ie.comparar(ref, v.reindex(df['CD_SETOR']).to_numpy(), mun.reindex(df['CD_SETOR']).to_numpy())
        c['equivalente'] = bool(c['spearman_mun'] >= EQUIV['spearman'] and c['troca_faixa'] < EQUIV['troca'])
        comps.append({'id': esp.at[i, 'id'], **c})
    esp = esp.merge(pd.DataFrame(comps), on='id', how='left')
    cols = ['id', 'eixo'] + [c for c in esp.columns if c not in ('id', 'eixo')]
    esp[cols].to_csv(SAIDA / 'camada2_especificacoes.csv', index=False, float_format='%.6g')
    resumo = []
    for eixo, g in esp[esp['eixo'].isin(['conjunto', 'sigilo', 'normalizacao', 'rotacao_peso'])].groupby('eixo'):
        pior = g.loc[g['troca_faixa'].idxmax()]
        resumo.append({'eixo': eixo, 'alternativas': len(g), 'equivalentes': int(g['equivalente'].sum()),
                       'veredito': 'equivalentes' if g['equivalente'].all() else 'decisao_necessaria',
                       'maior_troca_faixa': pior['troca_faixa'], 'spearman_mun_min': g['spearman_mun'].min(),
                       'alternativa_mais_distante': pior['id']})
    pd.DataFrame(resumo).to_csv(SAIDA / 'camada2_efeito_eixo.csv', index=False, float_format='%.6g')
    print(f'camada 2: {len(esp)} especificações em {time.time() - t0:.0f} s')


# ─────────────────────────────────────────────────────────────────────────────
# Camada 3
# ─────────────────────────────────────────────────────────────────────────────
def congruencia_tucker(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Coeficiente de Tucker por fator: Σab / √(Σa²·Σb²). ≥ 0,95 = fator replicado; 0,85–0,94 = parecido."""
    return (A * B).sum(axis=0) / np.sqrt((A ** 2).sum(axis=0) * (B ** 2).sum(axis=0))


def matriz_entrada(d: pd.DataFrame, cols: list[str], norm: str) -> tuple[np.ndarray, str]:
    if norm == 'postos_municipal':
        return d.groupby('NM_MUN')[cols].rank(pct=True).to_numpy(), 'pearson'
    return d[cols].to_numpy(), 'spearman'


def pesos_de(X: np.ndarray, metodo: str, cols: list[str], rot: str, met: str):
    r = rodar_cenario(X, metodo=metodo, com_horn=False, extracao=EXTRACAO)
    M, rep = ie.reparticoes(r, ancora(cols))[(rot, met)]
    return r, M, rep


def tucker_metades(d: pd.DataFrame, cols: list[str], f, metade: dict) -> np.ndarray:
    """Tucker de cada fator entre as duas metades de municípios, nas cargas da rotação do finalista
    (sem rotação: só o primeiro fator), alinhadas."""
    cargas = []
    for h in (0, 1):
        Xh, metodo = matriz_entrada(d[d['NM_MUN'].map(metade) == h], cols, f['normalizacao'])
        cargas.append(pesos_de(Xh, metodo, cols, f['rotacao'], f['metodo'])[1])
    return congruencia_tucker(cargas[0], alinhar_cargas(cargas[1], cargas[0]))


def camada3(df: pd.DataFrame) -> None:
    t0 = time.time()
    esp = pd.read_csv(SAIDA / 'camada2_especificacoes.csv')
    eixos = pd.read_csv(SAIDA / 'camada2_efeito_eixo.csv')
    ids = [esp.loc[esp['eixo'] == 'referencia', 'id'].iloc[0]]
    ids += eixos.loc[eixos['veredito'] == 'decisao_necessaria', 'alternativa_mais_distante'].tolist()
    fin = esp[esp['id'].isin(ids)].set_index('id').loc[ids].reset_index()
    fin['papel'] = ['proposta'] + [f'alternativa_{e}' for e in
                                   eixos.set_index('alternativa_mais_distante').loc[ids[1:], 'eixo']]
    setores = df[['CD_SETOR', 'NM_MUN', 'regiao', 'is_fcu', 'v0001', 'pop_60mais',
                  'pct_idoso_60mais', 'renda_media_sem_extremo']].copy()
    estab, repl, perfis, linhas = [], [], [], []
    rng = np.random.default_rng(SEMENTE)
    muns = df.groupby('NM_MUN')['regiao'].first()
    metade = {m: 0 for m in muns.index}
    for _, g in muns.groupby(muns):                      # metades estratificadas por região
        ordem = rng.permutation(g.index.to_numpy())
        metade.update({m: i % 2 for i, m in enumerate(ordem)})
    for _, f in fin.iterrows():
        codigos = f['codigos'].split('+')
        cols = [VARS[c] for c in codigos]
        d = com_sigilo(df, f['sigilo']).dropna(subset=cols).reset_index(drop=True)
        X, metodo = matriz_entrada(d, cols, f['normalizacao'])
        r, M, rep = pesos_de(X, metodo, cols, f['rotacao'], f['metodo'])
        w, s = fa.pesos_indice(M, rep), sinais(M)
        v = indice_norm(d, cols, w, s, f['normalizacao'])
        fx = faixas_ivs(v, d['NM_MUN'].to_numpy())
        col = 'ivs' if f['papel'] == 'proposta' else f"ivs_{f['id']}"
        t = pd.DataFrame({'CD_SETOR': d['CD_SETOR'], col: v,
                          **({'faixa_ivs_bh': fx['faixa_ivs_bh'], 'faixa_quartis': fx['faixa_quartis']}
                             if f['papel'] == 'proposta' else {f"faixa_{f['id']}": fx['faixa_ivs_bh']})})
        setores = setores.merge(t, on='CD_SETOR', how='left', validate='one_to_one')
        # estabilidade: um município de fora por vez (reportada, não ordenada)
        for m in sorted(d['NM_MUN'].unique()):
            dm = d[d['NM_MUN'] != m]
            Xm, _ = matriz_entrada(dm, cols, f['normalizacao'])
            _, Mm, repm = pesos_de(Xm, metodo, cols, f['rotacao'], f['metodo'])
            estab.append({'id': f['id'], 'fora': m, 'peso_F1': ie.peso_f1(Mm, repm, ancora(cols)),
                          **{f'peso_{COD[c]}': x for c, x in zip(cols, fa.pesos_indice(Mm, repm))}})
        # replicação entre metades de municípios, nas cargas da rotação do finalista
        tk = tucker_metades(d, cols, f, metade)
        tk2 = tk[1] if len(tk) > 1 else np.nan
        repl.append({'id': f['id'], 'tucker_F1': tk[0], 'tucker_F2': tk2,
                     'municipios_metade_A': sum(1 for x in metade.values() if x == 0)})
        # perfil dos setores perdidos
        perdidos = ~df['CD_SETOR'].isin(d['CD_SETOR'])
        for grupo, sel in (('perdidos', perdidos), ('mantidos', ~perdidos)):
            g = df[sel]
            perfis.append({'id': f['id'], 'grupo': grupo, 'setores': int(sel.sum()),
                           'pct_recorte': float(sel.mean()),
                           'renda_mediana': g['renda_media_sem_extremo'].median(),
                           'pct_fcu': g['is_fcu'].mean(), 'pct_sudeste': (g['regiao'] == 'Sudeste').mean()})
        e = pd.DataFrame([x for x in estab if x['id'] == f['id']])
        linhas.append({**f.to_dict(), 'n_ivs': int((~np.isnan(v)).sum()),
                       'peso_F1_min': e['peso_F1'].min(), 'peso_F1_max': e['peso_F1'].max(),
                       'amp_peso_F1': e['peso_F1'].max() - e['peso_F1'].min(),
                       'fora_no_min': e.loc[e['peso_F1'].idxmin(), 'fora'],
                       'fora_no_max': e.loc[e['peso_F1'].idxmax(), 'fora'],
                       'tucker_F1': tk[0], 'tucker_F2': tk2})
        print(f"  {f['id']} ({f['papel']}): {time.time() - t0:.0f} s", flush=True)
    pd.DataFrame(linhas).to_csv(SAIDA / 'camada3_finalistas.csv', index=False, float_format='%.6g')
    pd.DataFrame(estab).to_csv(SAIDA / 'camada3_estabilidade.csv', index=False, float_format='%.6g')
    pd.DataFrame(repl).to_csv(SAIDA / 'camada3_replicacao.csv', index=False, float_format='%.6g')
    pd.DataFrame(perfis).to_csv(SAIDA / 'camada3_perfil_perdidos.csv', index=False, float_format='%.6g')
    setores.to_csv(SAIDA / 'ivs_proposto_por_setor.csv', index=False, float_format='%.6g')
    print(f'camada 3: {len(fin)} finalistas em {time.time() - t0:.0f} s')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--camada', type=int, required=True, choices=(1, 2, 3))
    a = ap.parse_args()
    SAIDA.mkdir(parents=True, exist_ok=True)
    df = carregar()
    print(f'recorte: {len(df)} setores')
    {1: camada1, 2: camada2, 3: camada3}[a.camada](df)


if __name__ == '__main__':
    main()
