"""Corte de carga fatorial < 0,4 (demanda da orientadora, nov/2026), em cada rotação.

"Acionar todos os indicadores na carga fatorial; os com carga menor que 0,4, retirar." Parte dos
12 indicadores do relatório parcial e aplica o corte **dentro de cada rotação** (sem rotação,
Varimax, promax): eixo principal, 2 fatores, Spearman no conjunto, analfabetismo sigiloso ausente.
O corte é iterativo: sai um indicador por vez, o de menor carga máxima, e a fatorial é refeita,
até todos ficarem com carga ≥ 0,4 (ou sobrarem 3). Sem rotação há um fator só no índice, então o
corte olha só o F1 (`ie.cargas_rotacao`); na promax, a matriz padrão.

Duas famílias: os 12, e os 12 sem idosos e crianças (estrutura etária, que domina o F1). Em cada
rotação, os métodos de peso do NB05; a versão final de cada família é promax · 60/40 · régua
municipal, e toda versão é comparada a ela na amostra comum. A proposta anterior (os 7 do
Quadro 1, sem corte) entra como referência.

Depois, as duas propostas do deck (sem idosos e crianças: A com promax · 60/40, que mantém o sem
banheiro; B com Varimax · 60/40, em que a regra o retira) e as finalistas passam pelo que a camada 3 da
multiversão fazia: IVS e faixas por setor, pesos com um município de fora, replicação entre metades de
municípios e o perfil dos setores perdidos; nas propostas, o corte é refeito sem cada município.

    ./.venv/bin/python scripts/fatorial_corte_04.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'src', RAIZ / 'scripts'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import fatorial_ampliada as fa  # noqa: E402
import fatorial_multiversao as fm  # noqa: E402
import ivs_especificacoes as ie  # noqa: E402
from ivs_censo.fatorial import rodar_cenario  # noqa: E402

SAIDA = RAIZ / 'banco_de_dados' / 'eda' / 'fatorial_corte_04'
CORTE = 0.40
MINIMO = 3
ROTACOES = ('sem_rotacao', 'varimax', 'promax')
FAMILIAS = {'12': list(fm.VARS), '12_sem_idade': [c for c in fm.VARS if c not in ('IDO', 'CRI')]}
FINAL = ('promax', '60_40')
# as duas propostas do deck (sem idosos e crianças) e as alternativas comparadas a elas: (papel, família, rotação, peso)
FINALISTAS = [('a', '12_sem_idade', 'promax', '60_40'), ('b', '12_sem_idade', 'varimax', '60_40'),
              ('os_12', '12', 'promax', '60_40'), ('sem_rotacao', '12_sem_idade', 'sem_rotacao', 'unico'),
              ('anterior_7', 'anterior_7', 'promax', '60_40')]
PROPOSTAS = ('a', 'b')


def ajustar(d: pd.DataFrame, codigos: list[str]) -> tuple[dict, pd.DataFrame]:
    cols = [fm.VARS[c] for c in codigos]
    s = d.dropna(subset=cols).reset_index(drop=True)
    return rodar_cenario(s[cols].to_numpy(), com_horn=False, extracao=fm.EXTRACAO), s


def cortar(d: pd.DataFrame, codigos: list[str], rot: str) -> tuple[list[str], dict, pd.DataFrame, list[dict]]:
    """Corte iterativo de uma rotação: devolve os que ficam, a fatorial final, a amostra e os passos."""
    atuais, passos = list(codigos), []
    for passo in range(1, len(codigos) + 1):
        r, s = ajustar(d, atuais)
        M, h2 = ie.cargas_rotacao(r, rot)
        carga = np.abs(M).max(axis=1)
        i = int(carga.argmin())
        sai = carga[i] < CORTE and len(atuais) > MINIMO
        passos += [{'rotacao': rot, 'passo': passo, 'codigo': c, 'carga_max': x, 'h2': h, 'n': len(s),
                    'retirado': sai and j == i} for j, (c, x, h) in enumerate(zip(atuais, carga, h2))]
        if not sai:
            return atuais, r, s, passos
        atuais.pop(i)
    raise RuntimeError('corte sem fim')  # inalcançável: o laço para em MINIMO


def versoes(nome: str, codigos: list[str], r: dict, s: pd.DataFrame, rot: str, retirados: list[str]):
    """Os métodos de peso da rotação sobre a lista que sobrou do corte."""
    cols = [fm.VARS[c] for c in codigos]
    fcu = s['is_fcu'].to_numpy(dtype=float)
    for (rot_, met), (M, rep) in ie.reparticoes(r, fm.ancora(cols)).items():
        if rot_ != rot:
            continue
        w, sg = fa.pesos_indice(M, rep), fm.sinais(M)
        v = fm.indice_norm(s, cols, w, sg, 'municipal')
        ok = ~np.isnan(fcu) & ~np.isnan(v)
        esp = {'familia': nome, 'rotacao': rot, 'metodo': met, 'p': len(codigos),
               'mantidos': '+'.join(codigos), 'retirados': '+'.join(retirados), 'n': len(s),
               'peso_F1': ie.peso_f1(M, rep, fm.ancora(cols)), **fm.elegivel(r, rot), 'phi': r['phi'][0, 1],
               'auc_fcu': fa.auc_postos(v[ok], fcu[ok]),
               'auc_fcu_mun': ie.auc_municipal(v[ok], fcu[ok], s['NM_MUN'].to_numpy()[ok])[0],
               **{f'peso_{fm.COD[c]}': x * g for c, x, g in zip(cols, w, sg)}}
        yield esp, pd.Series(v, index=s['CD_SETOR'])


def cargas_tabela(nome: str, codigos: list[str], r: dict, rot: str) -> list[dict]:
    M, h2 = ie.cargas_rotacao(r, rot)
    regs = []
    for j, c in enumerate(codigos):
        reg = {'familia': nome, 'rotacao': rot, 'codigo': c, 'indicador': ie.ROT[fm.VARS[c]], 'h2': h2[j],
               **{f'F{k + 1}': M[j, k] for k in range(M.shape[1])}}
        if rot == 'promax':
            reg.update({f'estrutura_F{k + 1}': r['promax_estrutura'][j, k] for k in range(2)})
        regs.append(reg)
    return regs


def metades(df: pd.DataFrame) -> dict:
    """Municípios em duas metades sorteadas dentro de cada região: as mesmas da camada 3 da multiversão."""
    rng = np.random.default_rng(fm.SEMENTE)
    muns = df.groupby('NM_MUN')['regiao'].first()
    metade = {}
    for _, g in muns.groupby(muns):
        metade.update({m: i % 2 for i, m in enumerate(rng.permutation(g.index.to_numpy()))})
    return metade


def finalistas(df: pd.DataFrame, listas: dict, esp: pd.DataFrame) -> None:
    """As propostas e as alternativas, como a camada 3 da multiversão: IVS e faixas por setor, pesos com um
    município de fora, replicação entre metades, perfil dos setores perdidos e, nas propostas, se o corte se
    mantém quando cada município sai."""
    setores = df[['CD_SETOR', 'NM_MUN', 'regiao', 'is_fcu', 'v0001', 'pop_60mais', 'pct_idoso_60mais',
                  'renda_media_sem_extremo']].copy()
    metade, mun = metades(df), df['NM_MUN'].to_numpy()
    estab, repl, perfis, linhas, vet = [], [], [], [], {}
    for papel, fam, rot, met in FINALISTAS:
        codigos = listas[(fam, rot)]
        cols = [fm.VARS[c] for c in codigos]
        d = df.dropna(subset=cols).reset_index(drop=True)
        X, metodo = fm.matriz_entrada(d, cols, 'municipal')
        _, M, rep = fm.pesos_de(X, metodo, cols, rot, met)
        v = fm.indice_norm(d, cols, fa.pesos_indice(M, rep), fm.sinais(M), 'municipal')
        fx = fm.faixas_ivs(v, d['NM_MUN'].to_numpy())
        t = pd.DataFrame({'CD_SETOR': d['CD_SETOR'], f'ivs_{papel}': v, f'faixa_{papel}': fx['faixa_ivs_bh'],
                          f'quartis_{papel}': fx['faixa_quartis']})
        setores = setores.merge(t, on='CD_SETOR', how='left', validate='one_to_one')
        vet[papel] = setores[f'ivs_{papel}'].to_numpy()
        for m in sorted(d['NM_MUN'].unique()):
            dm = d[d['NM_MUN'] != m]
            _, Mm, repm = fm.pesos_de(fm.matriz_entrada(dm, cols, 'municipal')[0], metodo, cols, rot, met)
            estab.append({'id': papel, 'fora': m, 'peso_F1': ie.peso_f1(Mm, repm, fm.ancora(cols)),
                          **{f'peso_{fm.COD[c]}': x for c, x in zip(cols, fa.pesos_indice(Mm, repm))}})
        tk = fm.tucker_metades(d, cols, {'normalizacao': 'municipal', 'rotacao': rot, 'metodo': met}, metade)
        tk2 = tk[1] if len(tk) > 1 else np.nan
        repl.append({'id': papel, 'tucker_F1': tk[0], 'tucker_F2': tk2})
        perdidos = ~df['CD_SETOR'].isin(d['CD_SETOR'])
        for grupo, sel in (('perdidos', perdidos), ('mantidos', ~perdidos)):
            g = df[sel]
            perfis.append({'id': papel, 'grupo': grupo, 'setores': int(sel.sum()), 'pct_recorte': float(sel.mean()),
                           'renda_mediana': g['renda_media_sem_extremo'].median(), 'pct_fcu': g['is_fcu'].mean()})
        e = pd.DataFrame([x for x in estab if x['id'] == papel])
        fcu, ren = d['is_fcu'].to_numpy(dtype=float), d['renda_inv'].to_numpy()
        ok = ~np.isnan(fcu) & ~np.isnan(ren)
        linhas.append({**esp.set_index('id').loc[f'{fam}·{rot}·{met}'].to_dict(), 'id': papel, 'papel': papel,
                       'codigos': '+'.join(codigos), 'pct_recorte': len(d) / len(df), 'n_ivs': int((~np.isnan(v)).sum()),
                       'auc_renda_sozinha': fa.auc_postos(ren[ok], fcu[ok]),
                       'peso_F1_min': e['peso_F1'].min(), 'peso_F1_max': e['peso_F1'].max(),
                       'amp_peso_F1': e['peso_F1'].max() - e['peso_F1'].min(), 'tucker_F1': tk[0], 'tucker_F2': tk2})
        print(f'  finalista {papel}', flush=True)
    for x in linhas:   # cada finalista contra as duas propostas, nos setores comuns
        for prop in PROPOSTAS:
            x.update({f'{k}_vs_{prop}': y for k, y in ie.comparar(vet[prop], vet[x['papel']], mun).items()})
    # o corte de cada proposta se mantém quando cada município sai?
    corte = []
    for papel, fam, rot, _ in FINALISTAS[:len(PROPOSTAS)]:
        for m in sorted(df['NM_MUN'].unique()):
            ficam = cortar(df[df['NM_MUN'] != m], FAMILIAS[fam], rot)[0]
            corte.append({'proposta': papel, 'fora': m, 'mantidos': '+'.join(ficam),
                          'igual_a_proposta': ficam == listas[(fam, rot)]})
    pd.DataFrame(linhas).to_csv(SAIDA / 'finalistas.csv', index=False, float_format='%.6g')
    pd.DataFrame(estab).to_csv(SAIDA / 'estabilidade.csv', index=False, float_format='%.6g')
    pd.DataFrame(repl).to_csv(SAIDA / 'replicacao.csv', index=False, float_format='%.6g')
    pd.DataFrame(perfis).to_csv(SAIDA / 'perfil_perdidos.csv', index=False, float_format='%.6g')
    pd.DataFrame(corte).to_csv(SAIDA / 'corte_estabilidade.csv', index=False)
    setores.to_csv(SAIDA / 'ivs_final_por_setor.csv', index=False, float_format='%.6g')
    c = pd.DataFrame(corte).groupby('proposta')['igual_a_proposta']
    print(f'{len(FINALISTAS)} finalistas; corte igual à proposta (rodadas sem um município): '
          + ', '.join(f'{p} {int(g.sum())} de {len(g)}' for p, g in c))


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    df = fm.carregar()
    print(f'recorte: {len(df)} setores')
    passos, cargas, regs, vetores, listas = [], [], [], {}, {}
    for nome, codigos in FAMILIAS.items():
        for rot in ROTACOES:
            ficam, r, s, p = cortar(df, codigos, rot)
            listas[(nome, rot)] = ficam
            retirados = [c for c in codigos if c not in ficam]
            passos += [{'familia': nome, **x} for x in p]
            cargas += cargas_tabela(nome, ficam, r, rot)
            for esp, v in versoes(nome, ficam, r, s, rot, retirados):
                regs.append(esp)
                vetores[(nome, rot, esp['metodo'])] = v
            print(f'  {nome} · {rot}: saem {retirados or "nenhum"}', flush=True)
    # a proposta anterior: os 7 do Quadro 1, promax 60/40, sem corte
    r, s = ajustar(df, fm.NUCLEO)
    for esp, v in versoes('anterior_7', fm.NUCLEO, r, s, 'promax', []):
        if esp['metodo'] == FINAL[1]:
            regs.append(esp)
            vetores[('anterior_7', 'promax', esp['metodo'])] = v

    setores, mun = df['CD_SETOR'], df.set_index('CD_SETOR')['NM_MUN'].reindex(df['CD_SETOR']).to_numpy()
    alinhado = {k: v.reindex(setores).to_numpy() for k, v in vetores.items()}
    esp = pd.DataFrame(regs)
    esp['id'] = [f'{f}·{r_}·{m}' for f, r_, m in zip(esp['familia'], esp['rotacao'], esp['metodo'])]
    comps = []
    for (f, r_, m), v in alinhado.items():
        ref = alinhado[('12' if f == 'anterior_7' else f, *FINAL)]   # a anterior é comparada à final dos 12
        comps.append({'id': f'{f}·{r_}·{m}', **{f'{k}_vs_final': x for k, x in ie.comparar(ref, v, mun).items()}})
    esp = esp.merge(pd.DataFrame(comps), on='id', how='left')
    finais = {'12': alinhado[('12', *FINAL)], '12_sem_idade': alinhado[('12_sem_idade', *FINAL)],
              'anterior_7': alinhado[('anterior_7', *FINAL)]}
    pares = [{'a': a, 'b': b, **ie.comparar(finais[a], finais[b], mun)}
             for a, b in (('12', '12_sem_idade'), ('12', 'anterior_7'), ('12_sem_idade', 'anterior_7'))]

    pd.DataFrame(passos).to_csv(SAIDA / 'corte_passos.csv', index=False, float_format='%.6g')
    pd.DataFrame(cargas).to_csv(SAIDA / 'cargas_finais.csv', index=False, float_format='%.6g')
    esp[['id'] + [c for c in esp.columns if c != 'id']].to_csv(SAIDA / 'versoes.csv', index=False,
                                                              float_format='%.6g')
    pd.DataFrame(pares).to_csv(SAIDA / 'finais_comparados.csv', index=False, float_format='%.6g')
    print(f'{len(esp)} versões em {SAIDA.relative_to(RAIZ)}')
    listas[('anterior_7', 'promax')] = fm.NUCLEO
    finalistas(df, listas, esp)


if __name__ == '__main__':
    main()
