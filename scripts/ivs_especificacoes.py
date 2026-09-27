"""Motor de especificações do IVS (NB05, Fase C: itens 1 a 6 do pedido de set/2026).

A grade (docs/prompts/prompt_nb05_ivs_final_2026-09.md, seção 2.1): renda (original · sem
extremo · mediana municipal) × lixo (com · sem) × banheiro (fora · V00495 · graduado) = 18
bases. Em cada base, três soluções — sem rotação (um fator: o teste de "um fator ou dois"),
Varimax e promax — e os métodos de peso (Varimax: SS, 50/50, 60/40; promax: SS da padrão,
SS da estrutura, comunalidades, 50/50, 60/40) = 162 índices; cada um com normalização
municipal (referência) e global (sensibilidade) = 324 especificações, classificadas em
faixas pela regra do IVS-BH 2012 e por quartis municipais.

    python scripts/ivs_especificacoes.py     # grava em banco_de_dados/eda/ivs_especificacoes/

Reaproveita o motor da Fase 2 (`carregar`, `montar`, `pesos_indice`, `indice_01`,
`auc_postos` de `scripts/fatorial_ampliada.py`) e `rodar_cenario` do módulo. Sem bootstrap:
a incerteza aparece como estabilidade (um município de fora por vez). A trava da seção C.5
roda primeiro; se não bater, nada é gravado.
"""
from __future__ import annotations

import sqlite3
import sys
import textwrap
import time
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'src'))
sys.path.insert(0, str(RAIZ / 'scripts'))
import fatorial_ampliada as fa  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from ivs_censo.fatorial import comunalidades_obliquas, reparticao, rodar_cenario  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

SAIDA = RAIZ / 'banco_de_dados' / 'eda' / 'ivs_especificacoes'
FIG = SAIDA / 'figuras'
BANHEIROS = {'fora': None, 'v00495': 'pct_sem_banheiro', 'graduado': 'banheiro_graduado'}
ROT = {**fa.ROT, 'banheiro_graduado': 'Banheiro graduado'}
FAIXAS = ['baixo', 'medio', 'elevado', 'muito_elevado']
ROT_FAIXA = ['baixo', 'médio', 'elevado', 'muito elevado']
FIXOS = ('unico', '50_50', '60_40')    # métodos em que o peso de F1 não depende dos dados
MIN_GRUPO = 30    # setores de FCU e fora dela, por município, para entrar na AUC municipal
TRAVA = {'peso_f1': 65.01, 'auc_indice': 0.8131, 'auc_renda': 0.8819}
IVS_BH = {'renda': 'original', 'lixo': 'com', 'banheiro': 'fora', 'metodo': '60_40'}
# leituras dos critérios da seção 2.2: nome, normalização, critério (a), critério (b)
LEITURAS = [('principal', 'municipal', 'amp_peso_f1', 'auc_mun_comum'),
            ('amostra_propria', 'municipal', 'amp_peso_f1', 'auc_mun_propria'),
            ('estabilidade_pesos_variaveis', 'municipal', 'amp_peso_var_max', 'auc_mun_comum'),
            ('normalizacao_global', 'global', 'amp_peso_f1', 'auc_mun_comum')]
ORDEM = ['renda', 'lixo', 'banheiro', 'rotacao', 'metodo', 'normalizacao']


def banheiro_graduado(df: pd.DataFrame) -> pd.Series:
    """(1·V00236 + 2·V00237 + 3·V00238) / (3·V00001): as três partes de V00495 (partição da
    Fase B), graduadas; faltante se alguma parte ou o total faltar."""
    total = df['V00001'].where(df['V00001'] > 0)
    return (df['V00236'] + 2 * df['V00237'] + 3 * df['V00238']) / (3 * total)


def carregar_base() -> pd.DataFrame:
    """A base da Fase 2 (`carregar`) mais as partes do banheiro graduado."""
    df = fa.carregar()
    con = sqlite3.connect(f'file:{fa.DB}?mode=ro', uri=True)
    extra = pd.read_sql('SELECT CD_SETOR, V00001, V00236, V00237 FROM setores_censitarios', con)
    con.close()
    df = df.merge(extra, on='CD_SETOR', how='left', validate='one_to_one').reset_index(drop=True)
    for c in ['V00001', 'V00236', 'V00237']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['banheiro_graduado'] = banheiro_graduado(df)
    return df


def bases():
    """As 18 bases (renda × lixo × banheiro), com as variáveis na ordem da Fase 2."""
    for renda in fa.RENDAS:
        for lixo in ('com', 'sem'):
            for banheiro, extra in BANHEIROS.items():
                colunas = list(fa.IVS7_INV) if lixo == 'com' else fa._sem_lixo(fa.IVS7_INV)
                yield ({'renda': renda, 'lixo': lixo, 'banheiro': banheiro},
                       colunas + ([extra] if extra else []))


def ident(chave: dict, rotacao: str, metodo: str, normalizacao: str) -> str:
    return '·'.join([chave['renda'], f"lixo_{chave['lixo']}", f"banheiro_{chave['banheiro']}",
                     rotacao, metodo, normalizacao])


def fator_renda(M: np.ndarray, colunas: list[str]) -> int:
    """F1 é a dimensão socioeconômica: a de maior carga absoluta da renda invertida."""
    return int(np.abs(M[colunas.index('renda_inv')]).argmax())


def peso_f1(M: np.ndarray, rep: np.ndarray, colunas: list[str]) -> float:
    return 100 * float(rep[fator_renda(M, colunas)])


def reparticoes(r: dict, colunas: list[str]) -> dict:
    """Por (rotação, método): as cargas que repartem o peso dentro das dimensões e a
    repartição entre elas. Na promax, a distribuição dentro usa sempre a matriz padrão."""
    out = {('sem_rotacao', 'unico'): (r['sem_rotacao'][:, :1], np.array([1.0]))}
    for rot, M in (('varimax', r['varimax']), ('promax', r['promax_padrao'])):
        literatura = np.full(2, 0.4)
        literatura[fator_renda(M, colunas)] = 0.6   # IVS-BH 2012: socioeconômica 0,6; saneamento 0,4
        if rot == 'varimax':
            out[(rot, 'ss')] = (M, reparticao(M))
        else:
            out[(rot, 'ss_padrao')] = (M, reparticao(M))
            out[(rot, 'ss_estrutura')] = (M, reparticao(r['promax_estrutura']))
            # comunalidade de cada variável contada uma vez, na dimensão de maior carga padrão
            h2 = comunalidades_obliquas(M, r['phi'])
            dim = np.abs(M).argmax(axis=1)
            out[(rot, 'comunalidades')] = (M, np.array([h2[dim == j].sum() for j in range(2)]) / h2.sum())
        out[(rot, '50_50')] = (M, np.array([0.5, 0.5]))
        out[(rot, '60_40')] = (M, literatura)
    return out


def elegibilidade(r: dict, rotacao: str, colunas: list[str]) -> dict:
    """Critérios da seção 2.2, fixados antes de rodar (a promax lê a matriz padrão)."""
    if rotacao == 'sem_rotacao':
        M = r['sem_rotacao'][:, :1]
        h2 = M[:, 0] ** 2
    elif rotacao == 'varimax':
        M, h2 = r['varimax'], r['comunalidade']
    else:
        M, h2 = r['promax_padrao'], r['comunalidade_obliqua']
    carga = np.abs(M).max(axis=1)
    e = {'kmo_ok': bool(r['kmo'] >= 0.70), 'msa_ok': bool(r['msa'].min() >= 0.50),
         'comunalidade_ok': bool(h2.min() >= 0.30), 'cargas_ok': bool(carga.min() >= 0.40),
         'comunalidade_min': float(h2.min()), 'comunalidade_min_variavel': ROT[colunas[int(h2.argmin())]],
         'carga_max_min': float(carga.min()), 'carga_max_min_variavel': ROT[colunas[int(carga.argmin())]]}
    e['elegivel'] = e['kmo_ok'] and e['msa_ok'] and e['comunalidade_ok'] and e['cargas_ok']
    return e


def indice(d: pd.DataFrame, colunas: list[str], peso: np.ndarray, normalizacao: str) -> np.ndarray:
    """O `indice_01` do NB04: global (sensibilidade) ou com mín e máx de cada município."""
    if normalizacao == 'global':
        return fa.indice_01(d, colunas, peso)
    out = pd.Series(np.nan, index=d.index)
    for _, g in d.groupby('NM_MUN'):
        out.loc[g.index] = fa.indice_01(g, colunas, peso)
    return out.to_numpy()


def faixas(valor, municipio, regra: str) -> np.ndarray:
    """Quatro faixas dentro de cada município (0 baixo … 3 muito elevado); −1 se indefinida."""
    s = pd.Series(np.asarray(valor, dtype=float))
    g = s.groupby(np.asarray(municipio))
    if regra == 'ivs_bh':
        # IVS-BH 2012, p. 7: médio = média ± 0,5 DP; elevado até média + 1,5 DP; acima, muito elevado
        z = ((s - g.transform('mean')) / g.transform('std')).to_numpy()
        f = np.select([z < -0.5, z <= 0.5, z <= 1.5], [0, 1, 2], 3)
    else:
        z = g.rank(pct=True).to_numpy()
        f = np.clip(np.ceil(4 * z) - 1, 0, 3)
    return np.where(np.isnan(z), -1, f).astype(np.int8)


def auc_grupos(escore, positivo, grupo) -> pd.DataFrame:
    """A AUC de `auc_postos` (Mann–Whitney) dentro de cada grupo, com n1 e n0."""
    t = pd.DataFrame({'e': np.asarray(escore, dtype=float), 'y': np.asarray(positivo, dtype=float),
                      'g': np.asarray(grupo)}).dropna(subset=['e', 'y'])
    t['r'] = t.groupby('g')['e'].rank()
    n1 = t.groupby('g')['y'].sum()
    n0 = t.groupby('g')['y'].count() - n1
    s1 = (t['r'] * (t['y'] == 1)).groupby(t['g']).sum()
    return pd.DataFrame({'auc': (s1 - n1 * (n1 + 1) / 2) / (n1 * n0), 'n1': n1, 'n0': n0})


def auc_municipal(escore, positivo, municipio) -> tuple[float, int]:
    """Mediana da AUC entre os municípios com ao menos MIN_GRUPO setores de FCU e fora."""
    t = auc_grupos(escore, positivo, municipio)
    t = t[(t['n1'] >= MIN_GRUPO) & (t['n0'] >= MIN_GRUPO)]
    return float(t['auc'].median()), len(t)


def auc_estratos(escore, positivo, municipio, renda_inv) -> tuple[float, int]:
    """AUC dentro dos decis de renda de cada município, somada pelos pares FCU × fora
    (peso n1·n0): o escore ainda separa FCU entre setores de renda parecida?"""
    mun = np.asarray(municipio)
    q = pd.Series(np.asarray(renda_inv, dtype=float)).groupby(mun).rank(pct=True)
    decil = np.ceil(10 * q).clip(1, 10).astype(int)
    grupo = pd.factorize(pd.Series(mun).astype(str) + '|' + decil.astype(str))[0]
    t = auc_grupos(escore, positivo, grupo)
    t = t[(t['n1'] > 0) & (t['n0'] > 0)]
    w = t['n1'] * t['n0']
    return float((t['auc'] * w).sum() / w.sum()), len(t)


def logistica(X, y, iter_max: int = 100, tol: float = 1e-10):
    """Regressão logística por IRLS (numpy): coeficientes, erros-padrão, deviance e preditor."""
    X = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(X.shape[1])
    for _ in range(iter_max):
        p = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))
        w = np.clip(p * (1 - p), 1e-12, None)
        passo = np.linalg.solve((X.T * w) @ X, X.T @ (y - p))
        b = b + passo
        if np.abs(passo).max() < tol:
            break
    eta = X @ b
    p = np.clip(1 / (1 + np.exp(-np.clip(eta, -30, 30))), 1e-15, 1 - 1e-15)
    dev = float(-2 * (y * np.log(p) + (1 - y) * np.log(1 - p)).sum())
    ep = np.sqrt(np.diag(np.linalg.inv((X.T * (p * (1 - p))) @ X)))
    return b, ep, dev, eta


def spearman(a, b) -> float:
    return float(np.corrcoef(pd.Series(a).rank(), pd.Series(b).rank())[0, 1])


def estabilidade(d: pd.DataFrame, colunas: list[str], alvo: set) -> pd.DataFrame:
    """Um município de fora por vez, sem bootstrap: peso de F1 e pesos das variáveis no
    índice, só para as rotações elegíveis da base."""
    regs = []
    for mun in sorted(d['NM_MUN'].unique()):
        r = rodar_cenario(d.loc[d['NM_MUN'] != mun, colunas].to_numpy(), com_horn=False)
        for (rot, met), (M, rep) in reparticoes(r, colunas).items():
            if rot in alvo:
                regs.append({'rotacao': rot, 'metodo': met, 'fora': mun,
                             'peso_f1': peso_f1(M, rep, colunas),
                             **dict(zip(colunas, fa.pesos_indice(M, rep)))})
    return pd.DataFrame(regs)


def resumir_estabilidade(e: pd.DataFrame, chave: dict, colunas: list[str], cheio: dict) -> list[dict]:
    """Critério (a) da seção 2.2 — amplitude do peso de F1 — e, à parte, a maior amplitude
    do peso de uma variável no índice."""
    out = []
    for (rot, met), g in e.groupby(['rotacao', 'metodo'], sort=False):
        amp = g[colunas].max() - g[colunas].min()
        out.append({**chave, 'rotacao': rot, 'metodo': met, 'rodadas': len(g),
                    'peso_f1_cheio': cheio[(rot, met)], 'peso_f1_min': g['peso_f1'].min(),
                    'peso_f1_max': g['peso_f1'].max(),
                    'amp_peso_f1': g['peso_f1'].max() - g['peso_f1'].min(),
                    'fora_no_min': g.loc[g['peso_f1'].idxmin(), 'fora'],
                    'fora_no_max': g.loc[g['peso_f1'].idxmax(), 'fora'],
                    'amp_peso_var_max': 100 * float(amp.max()), 'variavel_amp_max': ROT[amp.idxmax()]})
    return out


def ordenar(esp: pd.DataFrame, norm: str, col_a: str, col_b: str) -> pd.DataFrame:
    """Seção 2.2: posição média, com peso igual, em (a) estabilidade, (b) AUC municipal e
    (c) parcimônia, entre as elegíveis; empate, a mais próxima do IVS-BH 2012 (se ainda
    empatar, a de maior AUC municipal)."""
    e = esp[esp['elegivel'] & (esp['normalizacao'] == norm)].copy()
    e['posto_a'] = e[col_a].rank(method='average')
    e['posto_b'] = (-e[col_b]).rank(method='average')
    e['posto_c'] = e['p'].rank(method='average')
    e['posto_medio'] = e[['posto_a', 'posto_b', 'posto_c']].mean(axis=1)
    e['dist_ivs_bh'] = sum((e[k] != v).astype(int) for k, v in IVS_BH.items())
    return e.sort_values(['posto_medio', 'dist_ivs_bh', col_b], ascending=[True, True, False])


def trava(df: pd.DataFrame) -> dict:
    """C.5: IVS-6 (sem lixo), renda original, Varimax, pesos SS, normalização global — o
    `indice_01` do NB04 refeito com as mesmas funções."""
    colunas = fa._sem_lixo(fa.IVS7_INV)
    d, _ = fa.montar(df, colunas, 'original')
    r = rodar_cenario(d[colunas].to_numpy(), com_horn=False)
    M, rep = reparticoes(r, colunas)[('varimax', 'ss')]
    fcu = d['is_fcu'].to_numpy(dtype=float)
    ok = ~np.isnan(fcu)
    v = indice(d, colunas, fa.pesos_indice(M, rep), 'global')
    return {'peso_f1': round(peso_f1(M, rep, colunas), 2),
            'auc_indice': round(fa.auc_postos(v[ok], fcu[ok]), 4),
            'auc_renda': round(fa.auc_postos(d['renda_inv'].to_numpy()[ok], fcu[ok]), 4)}


def salvar(fig, nome: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIG / nome, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def gravar(tab: pd.DataFrame, nome: str) -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    tab.to_csv(SAIDA / nome, index=False, float_format='%.10g')


def fig_auc(esp: pd.DataFrame, renda_comum: dict, ref_id: str | None) -> None:
    e0 = esp[esp['normalizacao'] == 'municipal']
    cores = {'sem_rotacao': fa.CINZA, 'varimax': fa.PETROL, 'promax': fa.CLAY}
    fig, eixos = plt.subplots(1, 2, figsize=(12, 4.8), facecolor=fa.SURF)
    for ax, (col, chave, titulo) in zip(eixos, (('auc_global_comum', 'global', 'AUC global contra FCU'),
                                                ('auc_mun_comum', 'mun', 'Mediana da AUC dentro dos municípios'))):
        e = e0.sort_values(col).reset_index(drop=True)
        for rot, cor in cores.items():
            s = e[e['rotacao'] == rot]
            el = s['elegivel'].to_numpy(dtype=bool)
            if el.any():
                ax.scatter(s.index[el], s[col].to_numpy()[el], s=14, color=cor, label=f'{rot}, elegível')
            if (~el).any():
                ax.scatter(s.index[~el], s[col].to_numpy()[~el], s=14, facecolors='none', edgecolors=cor,
                           label=f'{rot}, inelegível')
        ax.axhline(renda_comum[chave], color=fa.TINTA, ls='--', lw=1, label='renda invertida sozinha')
        if ref_id is not None:
            i = int(e.index[e['id'] == ref_id][0])
            ax.scatter([i], [e.loc[i, col]], marker='*', s=180, color=fa.TINTA, zorder=5,
                       label='referência proposta')
        ax.set_title(f'{titulo}\n(normalização municipal, amostra comum)', fontsize=9)
        ax.set_xlabel('especificações, em ordem crescente', fontsize=8)
        ax.set_ylabel('AUC', fontsize=8)
        ax.yaxis.set_major_formatter(fa.VIRGULA)
        ax.set_facecolor(fa.SURF)
    eixos[0].legend(fontsize=7, frameon=False, loc='lower right')
    salvar(fig, 'auc_por_especificacao.png')


def fig_peso(estab: pd.DataFrame) -> None:
    e = estab[~estab['metodo'].isin(FIXOS)].reset_index(drop=True)
    if e.empty:
        return
    x = np.arange(len(e))
    cor = [fa.PETROL if r == 'varimax' else fa.CLAY for r in e['rotacao']]
    fig, ax = plt.subplots(figsize=(max(8, 0.22 * len(e) + 2), 5.8), facecolor=fa.SURF)
    ax.vlines(x, e['peso_f1_min'], e['peso_f1_max'], colors=cor, lw=2)
    ax.scatter(x, e['peso_f1_cheio'], color=cor, s=16, zorder=3)
    for y, txt in ((50, '50/50'), (60, '60/40 (IVS-BH 2012)')):
        ax.axhline(y, color=fa.CINZA, ls=':', lw=1)
        ax.text(x[-1] + 0.4, y, txt, fontsize=7, color=fa.CINZA, ha='right', va='bottom')
    rotulos = (e['renda'] + ' · lixo ' + e['lixo'] + ' · banheiro ' + e['banheiro'] + ' · '
               + e['rotacao'] + ' ' + e['metodo'])
    ax.set_xticks(x)
    ax.set_xticklabels(rotulos, rotation=90, fontsize=6)
    ax.set_ylabel('peso de F1 (dimensão da renda), %', fontsize=8)
    ax.set_title('Peso de F1 nas fatorações elegíveis: amostra inteira (ponto) e um município '
                 'de fora por vez (barra)', fontsize=9)
    ax.yaxis.set_major_formatter(fa.VIRGULA)
    ax.set_facecolor(fa.SURF)
    salvar(fig, 'peso_f1_por_especificacao.png')


def fig_concordancia(pares: list) -> None:
    if not pares:
        return
    cmap = LinearSegmentedColormap.from_list('projeto', [fa.SURF, fa.PETROL])
    fig, eixos = plt.subplots(1, len(pares), figsize=(3.7 * len(pares), 4.4), facecolor=fa.SURF,
                              squeeze=False)
    for ax, (titulo, a, b) in zip(eixos[0], pares):
        ok = (a >= 0) & (b >= 0)
        tab = np.zeros((4, 4))
        np.add.at(tab, (a[ok].astype(int), b[ok].astype(int)), 1)
        tab = 100 * tab / tab.sum()
        ax.imshow(tab, cmap=cmap, vmin=0)
        for i in range(4):
            for j in range(4):
                ax.text(j, i, f'{tab[i, j]:.1f}'.replace('.', ','), ha='center', va='center', fontsize=7,
                        color='white' if tab[i, j] > tab.max() / 2 else fa.TINTA)
        ax.set_xticks(range(4))
        ax.set_yticks(range(4))
        ax.set_xticklabels(ROT_FAIXA, rotation=45, ha='right', fontsize=7)
        ax.set_yticklabels(ROT_FAIXA, fontsize=7)
        ax.set_title(titulo, fontsize=7)
        ax.set_xlabel(f'alternativa · na mesma faixa: {np.trace(tab):.1f}%'.replace('.', ','), fontsize=7)
    eixos[0][0].set_ylabel('referência proposta', fontsize=8)
    fig.suptitle('Faixas pela regra do IVS-BH 2012, % dos setores da amostra comum', fontsize=9)
    salvar(fig, 'concordancia_faixas.png')


def main() -> None:
    t0 = time.time()
    df = carregar_base()
    medido = trava(df)
    print('trava C.5:', medido, flush=True)
    if medido != TRAVA:
        sys.exit(f'TRAVA NÃO BATE — esperado {TRAVA}, medido {medido}. Nenhum CSV gravado.')
    N = len(df)
    # amostra comum: casos completos nas variáveis de todas as especificações
    todas = ([c for c in fa.IVS7 if c != 'renda_media'] + list(fa.RENDAS.values())
             + [c for c in BANHEIROS.values() if c])
    comum = df[todas].notna().all(axis=1).to_numpy()
    linhas, pesos, estab, acresc, IDX, FX = [], [], [], [], [], []
    for chave, colunas in bases():
        d, _ = fa.montar(df, colunas, chave['renda'])
        r = rodar_cenario(d[colunas].to_numpy())
        pos, mun = d.index.to_numpy(), d['NM_MUN'].to_numpy()
        fcu = d['is_fcu'].to_numpy(dtype=float)
        ok, c = ~np.isnan(fcu), comum[pos]
        info = {'p': len(colunas), 'variaveis': ', '.join(ROT[x] for x in colunas),
                'n': len(d), 'perdidos_vs_recorte': N - len(d), 'n_comum': int(c.sum()),
                'n_fcu': int(fcu[ok].sum()), 'kmo': r['kmo'], 'msa_min': float(r['msa'].min()),
                'msa_min_variavel': ROT[colunas[int(r['msa'].argmin())]],
                'bartlett_qui2': r['bartlett_qui2'], 'bartlett_gl': r['bartlett_gl'],
                'fatores_kaiser': r['kaiser'], 'fatores_horn': r['horn_retidos'],
                'pares_mun_var_constantes': int((d.groupby('NM_MUN')[colunas].nunique() <= 1).to_numpy().sum())}
        eleg = {rot: elegibilidade(r, rot, colunas) for rot in ('sem_rotacao', 'varimax', 'promax')}
        reps = reparticoes(r, colunas)
        cheio = {k: peso_f1(M, rep, colunas) for k, (M, rep) in reps.items()}
        alvo = {rot for rot, e in eleg.items() if e['elegivel']}
        amp = {}
        if alvo:    # uma vez por fatoração elegível, não por normalização ou faixa
            for x in resumir_estabilidade(estabilidade(d, colunas, alvo), chave, colunas, cheio):
                estab.append(x)
                amp[(x['rotacao'], x['metodo'])] = x
        # o que o índice acrescenta à renda: as duas comparações da base
        renda = d['renda_inv'].to_numpy()
        postos = d[colunas].rank(pct=True).mean(axis=1).to_numpy()
        comp = {nome: (fa.auc_postos(s[ok], fcu[ok]), auc_municipal(s, fcu, mun)[0],
                       auc_estratos(s, fcu, mun, renda)[0])
                for nome, s in (('renda', renda), ('postos', postos))}
        z_renda = (renda - renda.mean()) / renda.std()
        _, _, dev1, eta1 = logistica(z_renda[ok, None], fcu[ok])
        auc_mod1 = fa.auc_postos(eta1, fcu[ok])
        for (rot, met), (M, rep) in reps.items():
            w = fa.pesos_indice(M, rep)
            dim = np.where(np.abs(M).argmax(axis=1) == fator_renda(M, colunas), 1, 2)
            base_id = {**chave, 'rotacao': rot, 'metodo': met}
            pesos.append({**base_id, 'elegivel': eleg[rot]['elegivel'], 'peso_f1': cheio[(rot, met)],
                          'peso_f2': 100 - cheio[(rot, met)] if M.shape[1] == 2 else np.nan,
                          **{f'peso_{x}': 100 * v for x, v in zip(colunas, w)},
                          **{f'dimensao_{x}': k for x, k in zip(colunas, dim)}})
            for norm in ('municipal', 'global'):
                v = indice(d, colunas, w, norm)
                fb, fq = faixas(v, mun, 'ivs_bh'), faixas(v, mun, 'quartis')
                cheio_v = np.full(N, np.nan, dtype=np.float32)
                cheio_v[pos] = v
                fx = np.full((2, N), -1, dtype=np.int8)
                fx[0, pos], fx[1, pos] = fb, fq
                IDX.append(cheio_v)
                FX.append(fx)
                am, nm = auc_municipal(v, fcu, mun)
                amc, nmc = auc_municipal(v[c], fcu[c], mun[c])
                linha = {'id': ident(chave, rot, met, norm), **base_id, 'normalizacao': norm, **info,
                         **eleg[rot], 'peso_f1': cheio[(rot, met)],
                         'amp_peso_f1': amp.get((rot, met), {}).get('amp_peso_f1', np.nan),
                         'amp_peso_var_max': amp.get((rot, met), {}).get('amp_peso_var_max', np.nan),
                         'auc_global_propria': fa.auc_postos(v[ok], fcu[ok]),
                         'auc_global_comum': fa.auc_postos(v[ok & c], fcu[ok & c]),
                         'auc_mun_propria': am, 'n_mun_propria': nm, 'auc_mun_comum': amc,
                         'n_mun_comum': nmc, 'faixas_indefinidas': int((fb < 0).sum() + (fq < 0).sum())}
                linhas.append(linha)
                if eleg[rot]['elegivel']:
                    ae, ne = auc_estratos(v, fcu, mun, renda)
                    z = (v - v.mean()) / v.std()
                    b, ep, dev2, eta2 = logistica(np.column_stack([z_renda, z])[ok], fcu[ok])
                    acresc.append({'id': linha['id'], **base_id, 'normalizacao': norm, 'n': int(ok.sum()),
                                   'auc_indice_global': linha['auc_global_propria'],
                                   'auc_renda_global': comp['renda'][0], 'auc_postos_global': comp['postos'][0],
                                   'auc_indice_mun': am, 'auc_renda_mun': comp['renda'][1],
                                   'auc_postos_mun': comp['postos'][1], 'n_mun': nm,
                                   'auc_indice_estratos': ae, 'auc_renda_estratos': comp['renda'][2],
                                   'auc_postos_estratos': comp['postos'][2], 'n_estratos': ne,
                                   'deviance_renda': dev1, 'deviance_renda_indice': dev2,
                                   'queda_deviance': dev1 - dev2, 'auc_modelo_renda': auc_mod1,
                                   'auc_modelo_renda_indice': fa.auc_postos(eta2, fcu[ok]),
                                   'coef_indice': b[2], 'z_indice': b[2] / ep[2]})
        print(f"{ident(chave, '', '', '')[:-3]}: n={len(d)}, elegíveis={sorted(alvo)} "
              f"({time.time() - t0:.0f} s)", flush=True)

    esp = pd.DataFrame(linhas)
    esp['elegivel'] = esp['elegivel'].astype(bool)
    ordens, refs = {}, []
    for nome, norm, a, b in LEITURAS:
        o = ordens[nome] = ordenar(esp, norm, a, b)
        if o.empty:
            continue
        top = o.iloc[0]
        fixo = '; amplitude zero por construção (peso de F1 fixo)' if top['metodo'] in FIXOS else ''
        refs.append({'leitura': nome, 'criterio_a': a, 'criterio_b': b, 'elegiveis': len(o), 'id': top['id'],
                     **{k: top[k] for k in ORDEM}, 'p': top['p'], 'valor_a': top[a], 'valor_b': top[b],
                     'posto_a': top['posto_a'], 'posto_b': top['posto_b'], 'posto_c': top['posto_c'],
                     'posto_medio': top['posto_medio'], 'dist_ivs_bh': top['dist_ivs_bh'],
                     'empatadas_no_topo': int((o['posto_medio'] == top['posto_medio']).sum()),
                     'segunda': o.iloc[1]['id'] if len(o) > 1 else '',
                     'posto_medio_segunda': o.iloc[1]['posto_medio'] if len(o) > 1 else np.nan,
                     'porque': (f"melhor posição média entre {len(o)} elegíveis (normalização {norm}): "
                                f"estabilidade {top['posto_a']:g}º, AUC municipal {top['posto_b']:g}º, "
                                f"parcimônia {top['posto_c']:g}º{fixo}")})
    principal = ordens['principal']
    ref_id = principal.iloc[0]['id'] if not principal.empty else None
    esp = esp.merge(principal[['id', 'posto_a', 'posto_b', 'posto_c', 'posto_medio', 'dist_ivs_bh']],
                    on='id', how='left')
    esp['posicao'] = esp['id'].map({i: k + 1 for k, i in enumerate(principal['id'])})
    esp['referencia'] = esp['id'] == ref_id
    ids = esp['id'].to_numpy()
    if ref_id is not None:
        k_ref = int(np.flatnonzero(ids == ref_id)[0])
        rv, rf = IDX[k_ref], FX[k_ref]
        comp_ref = []
        for k in range(len(IDX)):
            linha = {}
            for amostra, m in (('propria', ~np.isnan(IDX[k]) & ~np.isnan(rv)), ('comum', comum)):
                linha[f'spearman_ref_{amostra}'] = spearman(IDX[k][m], rv[m])
                linha[f'muda_faixa_ivs_bh_{amostra}'] = 100 * float(np.mean(FX[k][0, m] != rf[0, m]))
                linha[f'muda_faixa_quartis_{amostra}'] = 100 * float(np.mean(FX[k][1, m] != rf[1, m]))
            comp_ref.append(linha)
        esp = pd.concat([esp, pd.DataFrame(comp_ref)], axis=1)

    av = []
    for amostra in ('propria', 'comum'):
        t = esp[['id'] + ORDEM + ['elegivel', 'referencia']].copy()
        t['amostra'] = amostra
        t['n'] = esp['n'] if amostra == 'propria' else esp['n_comum']
        for m in ('auc_global', 'auc_mun', 'n_mun', 'spearman_ref', 'muda_faixa_ivs_bh', 'muda_faixa_quartis'):
            t[m] = esp[f'{m}_{amostra}'] if f'{m}_{amostra}' in esp else np.nan
        av.append(t)
    acr = pd.DataFrame(acresc)
    acr['referencia'] = acr['id'] == ref_id
    acr['conclusao'] = [
        (f"estratos de renda: índice {x.auc_indice_estratos:.4f} × renda {x.auc_renda_estratos:.4f}; "
         f"somar o índice à renda na logística: deviance −{x.queda_deviance:.1f} (z {x.z_indice:.1f}), "
         f"AUC {x.auc_modelo_renda:.4f} → {x.auc_modelo_renda_indice:.4f}") for x in acr.itertuples()]

    gravar(esp, 'especificacoes.csv')
    gravar(pd.DataFrame(pesos), 'pesos.csv')
    gravar(pd.concat(av, ignore_index=True), 'avaliacao.csv')
    gravar(acr, 'acrescimo_renda.csv')
    gravar(pd.DataFrame(estab), 'estabilidade.csv')
    gravar(pd.DataFrame(refs), 'referencia.csv')

    fcu_all = df['is_fcu'].to_numpy(dtype=float)
    mun_all = df['NM_MUN'].to_numpy()
    rc = -df['renda_media'].to_numpy()
    okc = comum & ~np.isnan(fcu_all)
    renda_comum = {'global': fa.auc_postos(rc[okc], fcu_all[okc]),
                   'mun': auc_municipal(rc[comum], fcu_all[comum], mun_all[comum])[0]}
    fig_auc(esp, renda_comum, ref_id)
    fig_peso(pd.DataFrame(estab))
    if ref_id is not None:
        m = ~np.isnan(IDX[k_ref])
        k_glob = int(np.flatnonzero(ids == ref_id.replace('·municipal', '·global'))[0])
        setor = df.loc[m, ['CD_SETOR', 'NM_MUN', 'is_fcu']].copy()
        setor['amostra_comum'] = comum[m]
        setor['ivs_referencia'] = IDX[k_ref][m]
        setor['faixa_ivs_bh'] = pd.Categorical.from_codes(FX[k_ref][0, m], FAIXAS)
        setor['faixa_quartis'] = pd.Categorical.from_codes(FX[k_ref][1, m], FAIXAS)
        setor['ivs_normalizacao_global'] = IDX[k_glob][m]
        gravar(setor, 'ivs_referencia_por_setor.csv')
        # alternativas: a mesma com normalização global, os índices do NB04 (IVS-7 e IVS-6,
        # Varimax SS) com normalização municipal e a proposta da leitura pelos pesos das variáveis
        o = ordens['estabilidade_pesos_variaveis']
        cand = [ids[k_glob]] + [ident({'renda': 'original', 'lixo': lx, 'banheiro': 'fora'}, 'varimax', 'ss',
                                      'municipal') for lx in ('com', 'sem')]
        cand.append(o.iloc[0]['id'] if not o.empty else None)
        alternativas = list(dict.fromkeys(a for a in cand if a and a != ref_id))[:4]
        fig_concordancia([('\n'.join(textwrap.wrap(a.replace('·', ' · '), 36)), rf[0, comum],
                           FX[int(np.flatnonzero(ids == a)[0])][0, comum]) for a in alternativas])

    print(f'{len(esp)} especificações; elegíveis: {int(esp["elegivel"].sum())} '
          f'({esp[esp["elegivel"]].groupby("rotacao").size().to_dict()}); amostra comum {int(comum.sum())} '
          f'de {N}', flush=True)
    for x in refs:
        print(f"  [{x['leitura']}] {x['id']} — {x['porque']}")
    if ref_id is not None:
        print('  acréscimo (referência):', acr.loc[acr['referencia'], 'conclusao'].iloc[0])
    print(f'pronto em {time.time() - t0:.0f} s')


if __name__ == '__main__':
    main()
