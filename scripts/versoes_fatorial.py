"""As 108 versões da análise fatorial: renda × lixo × água canalizada × banheiro × moradia.

Lista e leituras: `versoes_fatorial/VERSOES.md` e `versoes_fatorial/INTERPRETACAO.md`. Cada
versão é uma fatorial com o método da referência proposta do NB05 (promax, pesos 60/40,
normalização municipal, 2 fatores), na amostra própria; as comparações entre versões usam a
amostra comum às 108. Reaproveita o motor do NB05 (`ivs_especificacoes.py`) e o da fatorial
ampliada (`fatorial_ampliada.py`) por importação, sem editar nenhum dos dois.

    ./.venv/bin/python scripts/versoes_fatorial.py [--sem-estabilidade] [--so V023,V010]

Grava em banco_de_dados/eda/versoes_fatorial/: versoes.csv, cargas.csv, pares_por_eixo.csv,
pares_detalhe.csv, estabilidade.csv. A trava (as 18 versões que o NB05 já rodou têm de bater
com especificacoes.csv) roda junto; se não bater, nada é gravado.
"""
from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'src'))
sys.path.insert(0, str(RAIZ / 'scripts'))
import fatorial_ampliada as fa  # noqa: E402
import ivs_especificacoes as ie  # noqa: E402
from ivs_censo.fatorial import rodar_cenario  # noqa: E402

SAIDA = RAIZ / 'banco_de_dados' / 'eda' / 'versoes_fatorial'
ESPEC = RAIZ / 'banco_de_dados' / 'eda' / 'ivs_especificacoes' / 'especificacoes.csv'

# Os cinco eixos, na ordem dos IDs (V001 = primeira combinação). Código → (rótulo, coluna).
EIXOS = {
    'renda': {'original': 'original', 'sem_extremo': 'sem extremo', 'mediana_mun': 'com mediana'},
    'lixo': {'com': 'com', 'sem': 'sem'},
    'agua': {'nenhuma': '—', 'nao_chega': '+ não chega', 'sem_canalizacao': '+ sem canalização'},
    'banheiro': {'fora': '—', 'v00495': '+ sem banheiro (V00495)', 'graduado': '+ banheiro graduado'},
    'moradia': {'nao': '—', 'sim': '+ não convencional'},
}
COL_AGUA = {'nenhuma': None, 'nao_chega': 'pct_agua_nao_encanada', 'sem_canalizacao': 'pct_sem_agua_canalizada'}
COL_BANHEIRO = ie.BANHEIROS
COL_MORADIA = {'nao': None, 'sim': 'pct_moradia_nao_convencional'}
ROT = {**ie.ROT, 'pct_moradia_nao_convencional': fa.ROT.get('pct_moradia_nao_convencional', 'Moradia não convencional')}
REFERENCIA = 'V023'
FAIXA = ['baixo', 'medio', 'elevado', 'muito_elevado']


def versoes() -> list[dict]:
    """As 108 combinações, com ID e colunas (IVS-7 sem/com lixo, depois água, banheiro, moradia)."""
    out = []
    for k, (r, l, a, b, m) in enumerate(itertools.product(*(list(v) for v in EIXOS.values())), 1):
        colunas = list(fa.IVS7_INV) if l == 'com' else fa._sem_lixo(fa.IVS7_INV)
        colunas += [c for c in (COL_AGUA[a], COL_BANHEIRO[b], COL_MORADIA[m]) if c]
        out.append({'id': f'V{k:03d}', 'renda': r, 'lixo': l, 'agua': a, 'banheiro': b, 'moradia': m,
                    'colunas': colunas})
    return out


def id_nb05(v: dict) -> str | None:
    """O id da linha equivalente em especificacoes.csv (só sem água canalizada e sem moradia)."""
    if v['agua'] != 'nenhuma' or v['moradia'] != 'nao':
        return None
    return ie.ident({'renda': v['renda'], 'lixo': v['lixo'], 'banheiro': v['banheiro']},
                    'promax', '60_40', 'municipal')


def falhou(e: dict) -> str:
    nomes = {'kmo_ok': 'KMO < 0,70', 'msa_ok': 'MSA < 0,50', 'comunalidade_ok': 'comunalidade < 0,30',
             'cargas_ok': 'carga < 0,40'}
    return '; '.join(t for k, t in nomes.items() if not e[k])


def rodar(v: dict, df: pd.DataFrame, comum: np.ndarray, N: int, estab: bool):
    colunas = v['colunas']
    d, _ = fa.montar(df, colunas, v['renda'])
    r = rodar_cenario(d[colunas].to_numpy())
    pos, mun = d.index.to_numpy(), d['NM_MUN'].to_numpy()
    fcu = d['is_fcu'].to_numpy(dtype=float)
    ok, c = ~np.isnan(fcu), comum[pos]
    e = ie.elegibilidade(r, 'promax', colunas)
    M, rep = ie.reparticoes(r, colunas)[('promax', '60_40')]
    w = fa.pesos_indice(M, rep)
    val = ie.indice(d, colunas, w, 'municipal')
    fb = ie.faixas(val, mun, 'ivs_bh')
    am, nm = ie.auc_municipal(val, fcu, mun)
    amc, nmc = ie.auc_municipal(val[c], fcu[c], mun[c])
    linha = {k: v[k] for k in ('id', 'renda', 'lixo', 'agua', 'banheiro', 'moradia')}
    linha.update({
        'p': len(colunas), 'variaveis': ', '.join(ROT[x] for x in colunas), 'colunas': ' '.join(colunas),
        'n': len(d), 'perdidos_vs_recorte': N - len(d), 'n_comum': int(c.sum()), 'n_fcu': int(fcu[ok].sum()),
        'kmo': r['kmo'], 'bartlett_qui2': r['bartlett_qui2'], 'bartlett_gl': r['bartlett_gl'],
        'msa_min': float(r['msa'].min()), 'msa_min_variavel': ROT[colunas[int(r['msa'].argmin())]],
        'fatores_kaiser': r['kaiser'], 'fatores_horn': r['horn_retidos'],
        'var_explicada_2f': 100 * float(r['autovalores'][:2].sum() / len(colunas)),
        'phi': float(r['phi'][0, 1]), **e, 'criterio_que_falhou': falhou(e),
        'peso_f1': ie.peso_f1(M, rep, colunas),
        'auc_global_propria': fa.auc_postos(val[ok], fcu[ok]),
        'auc_global_comum': fa.auc_postos(val[ok & c], fcu[ok & c]),
        'auc_mun_propria': am, 'n_mun_propria': nm, 'auc_mun_comum': amc, 'n_mun_comum': nmc,
        **{f'pct_{f}': 100 * float((fb == k).mean()) for k, f in enumerate(FAIXA)},
        'pct_indefinida': 100 * float((fb < 0).mean()), 'id_nb05': id_nb05(v) or '',
    })
    fr = ie.fator_renda(M, colunas)
    estr = r['promax_estrutura']
    cargas = [{'id': v['id'], 'variavel': x, 'rotulo': ROT[x], 'ordem': i,
               'f1': M[i, fr], 'f2': M[i, 1 - fr], 'estrutura_f1': estr[i, fr], 'estrutura_f2': estr[i, 1 - fr],
               'comunalidade': r['comunalidade_obliqua'][i], 'msa': r['msa'][i], 'peso_indice': 100 * w[i],
               'dimensao': 'F1 (socioeconômica)' if abs(M[i, fr]) >= abs(M[i, 1 - fr]) else 'F2 (saneamento)'}
              for i, x in enumerate(colunas)]
    est = None
    if estab:
        cheio = {('promax', '60_40'): linha['peso_f1']}
        e_ = ie.estabilidade(d, colunas, {'promax'})
        e_ = e_[e_['metodo'] == '60_40']
        est = ie.resumir_estabilidade(e_, {'id': v['id']}, colunas, cheio)[0]
        linha['amp_peso_var_max'] = est['amp_peso_var_max']
    cheio_v = np.full(N, np.nan)
    cheio_v[pos] = val
    fx = np.full(N, -1, dtype=np.int8)
    fx[pos] = fb
    return linha, cargas, est, cheio_v, fx


def spearman(a, b) -> float:
    return float(pd.Series(a).rank().corr(pd.Series(b).rank()))


def pares(V: pd.DataFrame, IDX: dict, FX: dict, comum: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Para cada eixo e cada troca de nível, os pares de versões que só diferem nele."""
    chave = V.set_index(list(EIXOS))['id']
    det = []
    for eixo, niveis in EIXOS.items():
        outros = [e for e in EIXOS if e != eixo]
        for a, b in itertools.combinations(list(niveis), 2):
            for resto in itertools.product(*(list(EIXOS[o]) for o in outros)):
                ka = dict(zip(outros, resto), **{eixo: a})
                kb = dict(zip(outros, resto), **{eixo: b})
                ia = chave[tuple(ka[e] for e in EIXOS)]
                ib = chave[tuple(kb[e] for e in EIXOS)]
                ra, rb = V.set_index('id').loc[ia], V.set_index('id').loc[ib]
                m = comum & ~np.isnan(IDX[ia]) & ~np.isnan(IDX[ib])
                det.append({'eixo': eixo, 'de': a, 'para': b, 'id_de': ia, 'id_para': ib,
                            'd_kmo': rb['kmo'] - ra['kmo'], 'd_var_2f': rb['var_explicada_2f'] - ra['var_explicada_2f'],
                            'd_auc_mun_comum': rb['auc_mun_comum'] - ra['auc_mun_comum'],
                            'd_auc_global_comum': rb['auc_global_comum'] - ra['auc_global_comum'],
                            'd_kaiser': rb['fatores_kaiser'] - ra['fatores_kaiser'],
                            'd_horn': rb['fatores_horn'] - ra['fatores_horn'],
                            'elegivel_de': bool(ra['elegivel']), 'elegivel_para': bool(rb['elegivel']),
                            'spearman': spearman(IDX[ia][m], IDX[ib][m]),
                            'pct_muda_faixa': 100 * float((FX[ia][m] != FX[ib][m]).mean())})
    det = pd.DataFrame(det)
    res = []
    for (eixo, a, b), g in det.groupby(['eixo', 'de', 'para'], sort=False):
        lin = {'eixo': eixo, 'de': a, 'para': b, 'pares': len(g),
               'passam_a_elegivel': int((~g['elegivel_de'] & g['elegivel_para']).sum()),
               'deixam_de_ser_elegivel': int((g['elegivel_de'] & ~g['elegivel_para']).sum()),
               'elegiveis_de': int(g['elegivel_de'].sum()), 'elegiveis_para': int(g['elegivel_para'].sum())}
        for col in ('d_kmo', 'd_var_2f', 'd_auc_mun_comum', 'd_auc_global_comum', 'd_kaiser', 'd_horn',
                    'spearman', 'pct_muda_faixa'):
            lin.update({f'{col}_mediana': g[col].median(), f'{col}_min': g[col].min(), f'{col}_max': g[col].max()})
        res.append(lin)
    return pd.DataFrame(res), det


def conferir_trava(V: pd.DataFrame) -> list[str]:
    """As versões equivalentes às do NB05 têm de bater com especificacoes.csv."""
    esp = pd.read_csv(ESPEC).set_index('id')
    erros = []
    for _, v in V[V['id_nb05'] != ''].iterrows():
        e = esp.loc[v['id_nb05']]
        for col in ('n', 'kmo', 'msa_min', 'fatores_kaiser', 'fatores_horn', 'peso_f1', 'auc_global_propria',
                    'auc_mun_propria'):
            if not np.isclose(float(v[col]), float(e[col]), rtol=1e-6, atol=1e-9):
                erros.append(f"{v['id']} {col}: {v[col]} ≠ {e[col]}")
        if bool(v['elegivel']) != bool(e['elegivel']):
            erros.append(f"{v['id']} elegivel")
    ref = V.set_index('id').loc[REFERENCIA]
    if int(ref['n']) != 73878 or not bool(ref['elegivel']):
        erros.append(f'{REFERENCIA}: n {ref["n"]}, elegível {ref["elegivel"]}')
    return erros


def main() -> None:
    estab = '--sem-estabilidade' not in sys.argv
    so = sys.argv[sys.argv.index('--so') + 1].split(',') if '--so' in sys.argv else None
    t0 = time.time()
    df = ie.carregar_base()
    N = len(df)
    lista = versoes()
    todas = sorted({c for v in lista for c in v['colunas'] if c != 'renda_inv'} | set(fa.RENDAS.values()))
    comum = df[todas].notna().all(axis=1).to_numpy()
    print(f'base {N} setores; amostra comum {int(comum.sum())} ({time.time() - t0:.0f} s)', flush=True)
    L, C, E, IDX, FX = [], [], [], {}, {}
    for v in lista:
        if so and v['id'] not in so:
            continue
        t = time.time()
        linha, cargas, est, iv, fx = rodar(v, df, comum, N, estab)
        L.append(linha)
        C += cargas
        if est:
            E.append(est)
        IDX[v['id']], FX[v['id']] = iv, fx
        print(f"{v['id']}: p={linha['p']} n={linha['n']} kmo={linha['kmo']:.4f} "
              f"elegível={linha['elegivel']} ({time.time() - t:.1f} s)", flush=True)
    V = pd.DataFrame(L)
    ref = V.set_index('id')
    if REFERENCIA in IDX:
        m0 = comum & ~np.isnan(IDX[REFERENCIA])
        V['spearman_v023_comum'] = [spearman(IDX[REFERENCIA][m0 & ~np.isnan(IDX[i])], IDX[i][m0 & ~np.isnan(IDX[i])])
                                    for i in V['id']]
        V['muda_faixa_v023_comum'] = [100 * float((FX[REFERENCIA][m0 & ~np.isnan(IDX[i])]
                                                  != FX[i][m0 & ~np.isnan(IDX[i])]).mean()) for i in V['id']]
    erros = conferir_trava(V) if REFERENCIA in ref.index else []
    if erros:
        sys.exit('TRAVA NÃO BATE — nada gravado:\n  ' + '\n  '.join(erros[:20]))
    if so:
        print('rodada parcial (--so): nada gravado')
        return
    SAIDA.mkdir(parents=True, exist_ok=True)
    V.to_csv(SAIDA / 'versoes.csv', index=False)
    pd.DataFrame(C).to_csv(SAIDA / 'cargas.csv', index=False)
    if E:
        pd.DataFrame(E).to_csv(SAIDA / 'estabilidade.csv', index=False)
    res, det = pares(V, IDX, FX, comum)
    res.to_csv(SAIDA / 'pares_por_eixo.csv', index=False)
    det.to_csv(SAIDA / 'pares_detalhe.csv', index=False)
    print(f"108 versões, {int(V['elegivel'].sum())} elegíveis; trava das "
          f"{int((V['id_nb05'] != '').sum())} do NB05 OK ({time.time() - t0:.0f} s)")


if __name__ == '__main__':
    main()
