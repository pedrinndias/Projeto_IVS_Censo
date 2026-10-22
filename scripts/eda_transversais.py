#!/usr/bin/env python
"""As análises que atravessam as versões (E1 a E6).

    ./.venv/bin/python scripts/eda_transversais.py analises_exploratorias/<E…>

Lê `<pasta>/config.json` (`analise`: E1…E6) e grava `tabelas/`, `figuras/` e `catalogo.csv`
no mesmo formato das versões, para que `gerar_deck_versao.js` e `verificar_versao.py`
sirvam sem mudança. Usa o que as versões já gravaram (`setores_indice.csv`, T26) e as
funções do motor (`scripts/eda_versoes.py`): a base, o índice, o k-médias e a silhueta.

| Análise | Bloco | Tabelas | Figuras |
|---|---|---|---|
| E1 incerteza | 14 | T40–T42 | F40–F41 |
| E2 estabilidade | 15 | T43–T45 | F42–F43 |
| E3 desigualdade intramunicipal | 16 | T46–T47 | F44 |
| E4 população em risco | 17 | T48–T49 | F45 |
| E5 IVS e envelhecimento | 18 | T50–T52 | F46–F47 |
| E6 tipologias | 19 | T53–T57 | F48–F49 |
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eda_versoes as ev  # noqa: E402
from eda_versoes import (ARGILA, CINZA, PETROLEO, br, estilo, ie, intbr, pctbr, plt,  # noqa: E402
                         rho)

PASTAS = ev.RAIZ / 'analises_exploratorias'
REF = PASTAS / '00_referencia'
N_BOOT, SEMENTE = 1000, 42
MIN_SETORES = ie.MIN_GRUPO   # destaques por município só entre os que têm ao menos 30 setores


# ── As versões já geradas ──────────────────────────────────────────────────────
def versoes() -> pd.DataFrame:
    """Uma linha por versão com índice por setor: pasta, elegibilidade, normalização."""
    linhas = []
    for s in sorted(PASTAS.glob('**/setores_indice.csv')):
        pasta = s.parent
        nome = str(pasta.relative_to(PASTAS))
        if nome.startswith(('E', '00_sintese')):
            continue
        cfg = json.loads((pasta / 'config.json').read_text(encoding='utf-8'))
        t26 = pasta / 'tabelas' / 'T26_auc_e_elegibilidade.csv'
        eleg = None
        if t26.exists():
            t = pd.read_csv(t26)
            eleg = int(t.loc[t['medida'] == 'elegível pelos critérios do NB05', 'valor'].iloc[0])
        ic = cfg.get('indice') or {}
        linhas.append({'versao': nome, 'arquivo': s, 'elegivel': eleg,
                       'normalizacao': ic.get('normalizacao', 'municipal'), 'agregacao': ic.get('agregacao', 'soma'),
                       'estrato': nome.startswith(('A4_', 'A5_', 'A3_'))})
    return pd.DataFrame(linhas)


def ler_setores(arq) -> pd.DataFrame:
    """O `setores_indice.csv` de uma versão. A base nacional (A6) grava o município como
    "Nome/UF"; tira-se o sufixo para casar com os nomes da referência."""
    s = pd.read_csv(arq, dtype={'CD_SETOR': str})
    s['NM_MUN'] = s['NM_MUN'].str.replace(r'/[A-Z]{2}$', '', regex=True)
    return s


def referencia() -> pd.DataFrame:
    return ler_setores(REF / 'setores_indice.csv')


def gini(v):
    return ev.gini(np.asarray(v, dtype=float))


# ── E1. Incerteza ─────────────────────────────────────────────────────────────
def e1(S):
    ref = referencia()
    vs = versoes()
    vs = vs[(vs['elegivel'] == 1)]
    usadas, alto, conta = [], pd.Series(0.0, index=ref['CD_SETOR']), pd.Series(0.0, index=ref['CD_SETOR'])
    for _, v in vs.iterrows():
        s = ler_setores(v['arquivo']).set_index('CD_SETOR')
        if v['versao'] != '00_referencia':
            m = s.reindex(ref['CD_SETOR'])
            if len(s) == len(ref) and np.allclose(m['ivs'], ref['ivs'].to_numpy(), equal_nan=True):
                continue                                   # índice idêntico ao da referência (ex.: C5)
        s = s[s.index.isin(conta.index)]
        conta.loc[s.index] += 1
        alto.loc[s.index] += (s['faixa_ivs_bh'] >= 2).astype(float)
        usadas.append({'versao': v['versao'], 'setores_comuns': len(s), 'pct_alto': 100 * (s['faixa_ivs_bh'] >= 2).mean()})
    t40 = pd.DataFrame(usadas)
    S.tabela('T40', 'versoes_usadas', 14, 'e1_versoes', t40,
             {'pct_alto_min': pctbr(t40['pct_alto'].min()), 'pct_alto_max': pctbr(t40['pct_alto'].max())})
    frac = (alto / conta).where(conta > 0)
    cat = pd.cut(frac, [-0.001, 0, 0.999, 1], labels=['nunca em risco elevado', 'às vezes', 'sempre em risco elevado'])
    t41 = cat.value_counts().reindex(['nunca em risco elevado', 'às vezes', 'sempre em risco elevado']).rename_axis('situacao').reset_index(name='setores')
    t41['pct'] = 100 * t41['setores'] / t41['setores'].sum()
    g = t41.set_index('situacao')['pct']
    c41 = {'pct_nunca': pctbr(g['nunca em risco elevado']), 'pct_as_vezes': pctbr(g['às vezes']), 'pct_sempre': pctbr(g['sempre em risco elevado'])}
    S.tabela('T41', 'situacao_dos_setores', 14, 'e1_situacao', t41, c41)
    d = pd.DataFrame({'NM_MUN': ref.set_index('CD_SETOR')['NM_MUN'], 'cat': cat})
    t42 = (pd.crosstab(d['NM_MUN'], d['cat'], normalize='index') * 100).reset_index()
    t42.columns = ['NM_MUN', 'pct_nunca', 'pct_as_vezes', 'pct_sempre']
    t42['setores'] = t42['NM_MUN'].map(d['NM_MUN'].value_counts())
    t42 = t42.sort_values('pct_as_vezes', ascending=False)
    u = t42[t42['setores'] >= MIN_SETORES]
    c42 = {'mun_max': u['NM_MUN'].iloc[0], 'pct_max': pctbr(u['pct_as_vezes'].iloc[0]),
           'mun_min': u['NM_MUN'].iloc[-1], 'pct_min': pctbr(u['pct_as_vezes'].iloc[-1])}
    S.tabela('T42', 'incerteza_por_municipio', 14, 'e1_municipios', t42, c42)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(frac.dropna(), bins=np.linspace(0, 1, 21), color=PETROLEO)
    estilo(ax, 'Fração das versões elegíveis em que o setor fica em risco elevado ou muito elevado', 'Setores')
    S.figura('F40', 'fracao_em_risco', 14, 'e1_hist', fig, 'T41', c41)
    t42 = u
    u = t42.head(25)
    fig, ax = plt.subplots(figsize=(8, 0.3 * len(u) + 1.2))
    ax.barh(u['NM_MUN'], u['pct_as_vezes'], color=ARGILA)
    ax.invert_yaxis()
    ax.tick_params(axis='y', labelsize=7)
    estilo(ax, '% dos setores do município que ora estão, ora não estão em risco elevado')
    S.figura('F41', 'incerteza_por_municipio', 14, 'e1_mun_fig', fig, 'T42', c42)


# ── E2. Estabilidade ──────────────────────────────────────────────────────────
def pesos_de(d, col):
    r = ev.rodar_cenario(d[col].to_numpy(), com_horn=False)
    M, rep = ie.reparticoes(r, col)[('promax', '60_40')]
    return ev.fa.pesos_indice(M, rep), r['kmo']


def sortear_municipios(pos: dict, rng) -> np.ndarray:
    """Posições dos setores de uma reamostragem por município (com reposição): a unidade é o
    município, que entra com todos os seus setores; reamostrar setores subestima a incerteza."""
    nomes = list(pos)
    return np.concatenate([pos[nomes[i]] for i in rng.integers(0, len(nomes), len(nomes))])


def e2(S, cfg_ref):
    b = ev.montar_base(cfg_ref)
    ix = ev.calcular_indice(b.df, cfg_ref)
    d, col, s = ix.d, ix.col, ix.setores
    rot = [ev.ROT[c] for c in col]
    linhas = []
    for mun in sorted(d['NM_MUN'].unique()):
        w, kmo = pesos_de(d[d['NM_MUN'] != mun], col)
        v = ie.indice(d, col, w, 'municipal')
        f = ie.faixas(v, d['NM_MUN'], 'ivs_bh')
        linhas.append({'municipio_excluido': mun, 'kmo': kmo, 'spearman_com_referencia': rho(pd.Series(v), s['ivs']),
                       'pct_mudam_faixa': 100 * (f != s['faixa_ivs_bh'].to_numpy()).mean(),
                       **{f'peso_{c}': 100 * x for c, x in zip(col, w)}})
    t43 = pd.DataFrame(linhas).sort_values('spearman_com_referencia')
    c43 = {'mun_min': t43['municipio_excluido'].iloc[0], 'rho_min': br(t43['spearman_com_referencia'].iloc[0]),
           'pct_max': pctbr(t43['pct_mudam_faixa'].max())}
    S.tabela('T43', 'um_municipio_de_fora', 15, 'e2_loo', t43, c43)
    rng = np.random.default_rng(SEMENTE)
    pos = d.groupby('NM_MUN').indices
    boot = []
    for _ in range(N_BOOT):
        w, kmo = pesos_de(d.iloc[sortear_municipios(pos, rng)], col)
        v = ie.indice(d, col, w, 'municipal')
        boot.append({'kmo': kmo, 'spearman': rho(pd.Series(v), s['ivs']),
                     'auc_municipal': ie.auc_municipal(v, d['is_fcu'], d['NM_MUN'])[0], **dict(zip(col, 100 * w))})
    bt = pd.DataFrame(boot)
    t44 = pd.DataFrame({'componente': col, 'rotulo': rot, 'peso_referencia': 100 * ix.w,
                        'p2_5': [bt[c].quantile(.025) for c in col], 'mediana': [bt[c].median() for c in col],
                        'p97_5': [bt[c].quantile(.975) for c in col]})
    t44['amplitude'] = t44['p97_5'] - t44['p2_5']
    a = t44.loc[t44['amplitude'].idxmax()]
    c44 = {'comp': a['rotulo'], 'p2_5': br(a['p2_5'], 1), 'p97_5': br(a['p97_5'], 1)}
    S.tabela('T44', 'pesos_reamostragem', 15, 'e2_pesos', t44, c44)
    ref_med = {'kmo': ix.r['kmo'], 'spearman': 1.0, 'auc_municipal': ix.auc_mun[0]}
    t45 = pd.DataFrame([{'medida': m, 'referencia': ref_med[m], 'p2_5': bt[m].quantile(.025), 'mediana': bt[m].median(),
                         'p97_5': bt[m].quantile(.975)} for m in ['kmo', 'spearman', 'auc_municipal']])
    t45['reamostragens'] = N_BOOT
    S.tabela('T45', 'medidas_reamostragem', 15, 'e2_medidas', t45,
             {'rho_p2_5': br(t45.loc[1, 'p2_5']), 'auc_p2_5': br(t45.loc[2, 'p2_5']), 'auc_p97_5': br(t45.loc[2, 'p97_5']),
              'n_boot': intbr(N_BOOT)})
    fig, ax = plt.subplots(figsize=(8, 0.2 * len(t43) + 1.2))
    ax.barh(t43['municipio_excluido'], t43['pct_mudam_faixa'], color=ARGILA)
    ax.invert_yaxis()
    ax.tick_params(axis='y', labelsize=6)
    estilo(ax, '% dos setores que mudam de faixa quando o município sai da estimação dos pesos')
    S.figura('F42', 'um_municipio_de_fora', 15, 'e2_loo_fig', fig, 'T43', c43)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.boxplot([bt[c] for c in col], showfliers=False, medianprops={'color': ARGILA})
    ax.plot(range(1, len(col) + 1), 100 * ix.w, 'o', color=PETROLEO, label='Peso na referência')
    ax.set_xticks(range(1, len(col) + 1), rot, rotation=30, ha='right')
    ax.legend(frameon=False, fontsize=8)
    estilo(ax, '', 'Peso no índice (%)')
    S.figura('F43', 'pesos_reamostragem', 15, 'e2_pesos_fig', fig, 'T44', c44)


# ── E3. Desigualdade intramunicipal entre versões ─────────────────────────────
def e3(S):
    ref = referencia()
    vs = versoes()
    vs = vs[(vs['normalizacao'] == 'municipal') & (vs['agregacao'] == 'soma') & ~vs['estrato']]
    linhas = []
    for _, v in vs.iterrows():
        s = ler_setores(v['arquivo'])
        s = s[s['CD_SETOR'].isin(set(ref['CD_SETOR']))]
        for mun, x in s.groupby('NM_MUN'):
            linhas.append({'versao': v['versao'], 'NM_MUN': mun, 'setores': len(x), 'gini': gini(x['ivs'].dropna())})
    t = pd.DataFrame(linhas)
    t['posto'] = t.groupby('versao')['gini'].rank(ascending=False)
    t46 = t.groupby('versao').agg(municipios=('NM_MUN', 'size'), gini_mediano=('gini', 'median'),
                                  gini_min=('gini', 'min'), gini_max=('gini', 'max')).reset_index()
    t46['spearman_postos_com_ref'] = [rho(t[t['versao'] == v].set_index('NM_MUN')['gini'],
                                          t[t['versao'] == '00_referencia'].set_index('NM_MUN')['gini'].reindex(
                                              t[t['versao'] == v]['NM_MUN'])) for v in t46['versao']]
    u = t46.sort_values('spearman_postos_com_ref')
    c46 = {'versao_min': u['versao'].iloc[0], 'rho_min': br(u['spearman_postos_com_ref'].iloc[0])}
    S.tabela('T46', 'gini_por_versao', 16, 'e3_versoes', t46, c46)
    g = t.groupby('NM_MUN').agg(gini_min=('gini', 'min'), gini_max=('gini', 'max'), posto_min=('posto', 'min'), posto_max=('posto', 'max'))
    g['gini_referencia'] = t[t['versao'] == '00_referencia'].set_index('NM_MUN')['gini']
    g['amplitude_posto'] = g['posto_max'] - g['posto_min']
    g['setores'] = ref['NM_MUN'].value_counts()
    t47 = g.reset_index().sort_values('gini_referencia', ascending=False)
    u = t47[t47['setores'] >= MIN_SETORES]
    a = u.loc[u['amplitude_posto'].idxmax()]
    c47 = {'mun': a['NM_MUN'], 'posto_min': intbr(a['posto_min']), 'posto_max': intbr(a['posto_max'])}
    S.tabela('T47', 'gini_por_municipio', 16, 'e3_municipios', t47, c47)
    t47 = t47.dropna(subset=['gini_referencia'])          # município de um setor só: sem Gini
    fig, ax = plt.subplots(figsize=(8, 0.2 * len(t47) + 1.2))
    y = np.arange(len(t47))
    ax.hlines(y, t47['gini_min'], t47['gini_max'], color=CINZA, lw=2)
    ax.plot(t47['gini_referencia'], y, 'o', ms=3, color=ARGILA, label='Referência')
    ax.set_yticks(y, t47['NM_MUN'], fontsize=6)
    ax.invert_yaxis()
    ax.legend(frameon=False, fontsize=7)
    estilo(ax, 'Gini do índice no município: menor e maior entre as versões (linha) e referência (ponto)')
    S.figura('F44', 'gini_entre_versoes', 16, 'e3_fig', fig, 'T47', c47)


# ── E4. População em risco entre versões ──────────────────────────────────────
def e4(S):
    ref = referencia()
    vs = versoes()
    vs = vs[~vs['estrato']]
    linhas = []
    for _, v in vs.iterrows():
        s = ler_setores(v['arquivo'])
        s = s[s['CD_SETOR'].isin(set(ref['CD_SETOR']))]
        alto = s['faixa_ivs_bh'] >= 2
        linhas.append({'versao': v['versao'], 'elegivel': v['elegivel'], 'setores': len(s), 'pessoas': s['v0001'].sum(),
                       'pessoas_alto': s.loc[alto, 'v0001'].sum(), 'pct_pessoas_alto': 100 * s.loc[alto, 'v0001'].sum() / s['v0001'].sum(),
                       'pessoas_60_alto': s.loc[alto, 'pop_60mais'].sum(),
                       'pct_60_alto': 100 * s.loc[alto, 'pop_60mais'].sum() / s['pop_60mais'].sum()})
    t48 = pd.DataFrame(linhas).sort_values('pct_pessoas_alto')
    r = t48[t48['versao'] == '00_referencia'].iloc[0]
    c48 = {'pct_ref': pctbr(r['pct_pessoas_alto']), 'p60_ref': intbr(r['pessoas_60_alto']),
           'pct_min': pctbr(t48['pct_pessoas_alto'].min()), 'versao_min': t48['versao'].iloc[0],
           'pct_max': pctbr(t48['pct_pessoas_alto'].max()), 'versao_max': t48['versao'].iloc[-1]}
    S.tabela('T48', 'pessoas_em_risco_por_versao', 17, 'e4_versoes', t48, c48)
    linhas = []
    for _, v in vs[vs['elegivel'] == 1].iterrows():
        s = ler_setores(v['arquivo'])
        s = s[s['CD_SETOR'].isin(set(ref['CD_SETOR']))]
        s['alto'] = (s['faixa_ivs_bh'] >= 2) * s['v0001']
        p = s.groupby('NM_MUN').agg(alto=('alto', 'sum'), pessoas=('v0001', 'sum'))
        for mun, x in p.iterrows():
            linhas.append({'versao': v['versao'], 'NM_MUN': mun, 'pct': 100 * x['alto'] / x['pessoas']})
    t = pd.DataFrame(linhas)
    t49 = t.groupby('NM_MUN')['pct'].agg(pct_min='min', pct_max='max').reset_index()
    t49['pct_referencia'] = t49['NM_MUN'].map(t[t['versao'] == '00_referencia'].set_index('NM_MUN')['pct'])
    t49['amplitude'] = t49['pct_max'] - t49['pct_min']
    t49['setores'] = t49['NM_MUN'].map(ref['NM_MUN'].value_counts())
    t49 = t49.sort_values('amplitude', ascending=False)
    u = t49[t49['setores'] >= MIN_SETORES]
    S.tabela('T49', 'pessoas_em_risco_por_municipio', 17, 'e4_municipios', t49,
             {'mun': u['NM_MUN'].iloc[0], 'pct_min': pctbr(u['pct_min'].iloc[0]), 'pct_max': pctbr(u['pct_max'].iloc[0])})
    fig, ax = plt.subplots(figsize=(8, 0.28 * len(t48) + 1.2))
    ax.barh(t48['versao'], t48['pct_pessoas_alto'], color=[ARGILA if v == '00_referencia' else PETROLEO for v in t48['versao']])
    ax.tick_params(axis='y', labelsize=7)
    estilo(ax, '% dos moradores em setores de risco elevado ou muito elevado (regra do IVS-BH)')
    S.figura('F45', 'pessoas_em_risco_por_versao', 17, 'e4_fig', fig, 'T48', c48)


# ── E5. IVS e envelhecimento ──────────────────────────────────────────────────
def e5(S, cfg_ref):
    b = ev.montar_base(cfg_ref)
    env = ev.ENVELHECIMENTO
    s = referencia().merge(b.df[['CD_SETOR'] + env], on='CD_SETOR', how='left')
    linhas = [{'escopo': 'Total', **{f'rho_{e}': rho(s['ivs'], s[e]) for e in env}}]
    linhas += [{'escopo': r, **{f'rho_{e}': rho(x['ivs'], x[e]) for e in env}} for r, x in s.groupby('regiao')]
    t50 = pd.DataFrame(linhas)
    c50 = {'rho_60': br(t50['rho_pct_idoso_60mais'].iloc[0]), 'rho_iep': br(t50['rho_iep_setor'].iloc[0])}
    S.tabela('T50', 'ivs_x_envelhecimento', 18, 'e5_correl', t50, c50)
    s['faixa'] = s['faixa_ivs_bh'].map(ev.rotulo_faixa)
    t51 = s[s['faixa_ivs_bh'] >= 0].groupby('faixa_ivs_bh').agg(
        setores=('ivs', 'size'), mediana_pct_60mais=('pct_idoso_60mais', 'median'), mediana_iep=('iep_setor', 'median'),
        mediana_rdi=('rdi_setor', 'median'), pessoas_60mais=('pop_60mais', 'sum')).reset_index()
    t51.insert(1, 'faixa', t51['faixa_ivs_bh'].map(ev.rotulo_faixa))
    c51 = {'med_baixo': br(t51['mediana_pct_60mais'].iloc[0]), 'med_muito': br(t51['mediana_pct_60mais'].iloc[-1])}
    S.tabela('T51', 'envelhecimento_por_faixa', 18, 'e5_faixas', t51, c51)
    t52 = pd.DataFrame([{'NM_MUN': m, 'setores': len(x), 'rho_ivs_60mais': rho(x['ivs'], x['pct_idoso_60mais'])}
                        for m, x in s.groupby('NM_MUN')]).sort_values('rho_ivs_60mais')
    u = t52[t52['setores'] >= MIN_SETORES].dropna()
    S.tabela('T52', 'ivs_x_60mais_por_municipio', 18, 'e5_municipios', t52,
             {'mun_min': u['NM_MUN'].iloc[0], 'rho_min': br(u['rho_ivs_60mais'].iloc[0]),
              'mun_max': u['NM_MUN'].iloc[-1], 'rho_max': br(u['rho_ivs_60mais'].iloc[-1])})
    m = s[['ivs', 'pct_idoso_60mais']].dropna()
    fig, ax = plt.subplots(figsize=(7, 5))
    hb = ax.hexbin(m['ivs'], m['pct_idoso_60mais'], gridsize=50, cmap=ev.SEQUENCIAL, mincnt=1)
    plt.colorbar(hb, ax=ax, label='setores')
    estilo(ax, 'IVS da referência (0 a 1, no município)', 'Proporção de pessoas de 60+')
    S.figura('F46', 'ivs_x_60mais', 18, 'e5_hex', fig, 'T50', c50)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.boxplot([s.loc[s['faixa_ivs_bh'] == f, 'pct_idoso_60mais'].dropna() for f in range(4)], showfliers=False,
               medianprops={'color': ARGILA})
    ax.set_xticks(range(1, 5), ie.ROT_FAIXA)
    estilo(ax, 'Faixa do IVS (regra do IVS-BH)', 'Proporção de pessoas de 60+')
    S.figura('F47', '60mais_por_faixa', 18, 'e5_box', fig, 'T51', c51)


# ── E6. Tipologias ────────────────────────────────────────────────────────────
def e6(S, cfg_ref):
    b = ev.montar_base(cfg_ref)
    ix = ev.calcular_indice(b.df, cfg_ref)
    d, col, s = ix.d, ix.col, ix.setores
    g = d['NM_MUN']
    Z = ((d[col] - d[col].groupby(g).transform('min')) / (d[col].groupby(g).transform('max') - d[col].groupby(g).transform('min'))).fillna(0)
    sil, rots = [], {}
    for k in range(3, 7):
        rot = ev.kmedias(Z.to_numpy(), k)[0]
        rots[k] = ev.ordenar_grupos(rot, s['ivs'].to_numpy())
        sil.append({'k': k, 'silhueta_setores': ev.silhueta(Z.to_numpy(), rot)})
    t53 = pd.DataFrame(sil)
    kb = int(t53.loc[t53['silhueta_setores'].idxmax(), 'k'])
    S.tabela('T53', 'silhueta_setores', 19, 'e6_sil_setores', t53, {'k': intbr(kb), 'sil': br(t53['silhueta_setores'].max())})
    perfis = []
    for k in sorted({kb, 4}):
        for grupo, x in Z.groupby(rots[k]):
            perfis.append({'k': k, 'grupo': int(grupo) + 1, 'setores': len(x), 'pct_setores': 100 * len(x) / len(Z),
                           'ivs_medio': s['ivs'][x.index].mean(), 'pct_fcu': 100 * s['is_fcu'][x.index].mean(),
                           **{c: x[c].mean() for c in col}})
    t54 = pd.DataFrame(perfis)
    u = t54[t54['k'] == 4]
    a = u.loc[u['pct_fcu'].idxmax()]
    c54 = {'grupo': intbr(a['grupo']), 'pct_fcu': pctbr(a['pct_fcu']), 'pct_setores': pctbr(a['pct_setores'])}
    S.tabela('T54', 'perfis_grupos_setores', 19, 'e6_perfis_setores', t54, c54)
    med = b.df.groupby('NM_MUN')[[c if c != 'renda_inv' else 'renda_media' for c in col]].median()
    Zm = ((med - med.mean()) / med.std()).fillna(0)
    silm, rotm = [], {}
    for k in range(3, 7):
        rot = ev.kmedias(Zm.to_numpy(), k)[0]
        rotm[k] = rot
        silm.append({'k': k, 'silhueta_municipios': ev.silhueta(Zm.to_numpy(), rot, amostra=len(Zm))})
    t55 = pd.DataFrame(silm)
    km = int(t55.loc[t55['silhueta_municipios'].idxmax(), 'k'])
    S.tabela('T55', 'silhueta_municipios', 19, 'e6_sil_mun', t55, {'k': intbr(km), 'sil': br(t55['silhueta_municipios'].max())})
    regiao = b.df.groupby('NM_MUN')['regiao'].first()
    t56 = pd.DataFrame({'NM_MUN': med.index, 'regiao': regiao.reindex(med.index).to_numpy(),
                        f'grupo_k{km}': rotm[km] + 1, 'grupo_k4': rotm[4] + 1}).sort_values([f'grupo_k{km}', 'NM_MUN'])
    S.tabela('T56', 'grupos_de_municipios', 19, 'e6_municipios', t56, {'k': intbr(km)})
    pm = med.assign(grupo=rotm[km] + 1).groupby('grupo').median()
    pm.insert(0, 'municipios', pd.Series(rotm[km] + 1).value_counts().sort_index().to_numpy())
    t57 = pm.reset_index()
    S.tabela('T57', 'perfis_grupos_municipios', 19, 'e6_perfis_mun', t57,
             {'k': intbr(km), 'n_max': intbr(t57['municipios'].max())})
    u = t54[t54['k'] == 4]
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ev.mapa_calor(ax, u[col].to_numpy(), [ev.ROT[c] for c in col], [f'grupo {int(x)}' for x in u['grupo']], ev.SEQUENCIAL, 0, 1, fs=8)
    ax.set_title('Média dos componentes normalizados (0 a 1) em cada grupo de setores, k = 4', fontsize=9)
    S.figura('F48', 'perfis_grupos_setores', 19, 'e6_fig_setores', fig, 'T54', c54)
    fig, ax = plt.subplots(figsize=(8, 4))
    cont = pd.crosstab(t56[f'grupo_k{km}'], t56['regiao'])
    esq = np.zeros(len(cont))
    for r in [r for r in ev.REGIOES.values() if r in cont.columns]:
        ax.barh([f'grupo {i}' for i in cont.index], cont[r], left=esq, color=ev.CORES_REGIAO[r], label=r)
        esq += cont[r].to_numpy()
    ax.legend(frameon=False, fontsize=7)
    estilo(ax, f'Municípios em cada grupo (k = {km}), por região')
    S.figura('F49', 'grupos_de_municipios', 19, 'e6_fig_mun', fig, 'T56', {'k': intbr(km)})


def main():
    t0 = time.time()
    pasta = Path(sys.argv[1]).resolve()
    cfg = json.loads((pasta / 'config.json').read_text(encoding='utf-8'))
    cfg_ref = ev.ler_config(REF)
    S = ev.Saida(pasta, json.loads(ev.MODELOS.read_text(encoding='utf-8')))
    a = cfg['analise']
    {'E1': lambda: e1(S), 'E2': lambda: e2(S, cfg_ref), 'E3': lambda: e3(S), 'E4': lambda: e4(S),
     'E5': lambda: e5(S, cfg_ref), 'E6': lambda: e6(S, cfg_ref)}[a]()
    S.fechar()
    print(f"{cfg['versao']}: {len(S.linhas)} itens · {time.time() - t0:.0f} s")
    for r in S.linhas:
        print(f"  {r['id']}: {r['o_que_mostra'][:150]}")


if __name__ == '__main__':
    main()
