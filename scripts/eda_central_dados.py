"""Extrai da EDA todos os números que a apresentação usa, num só JSON.

Por que este script existe
--------------------------
A primeira versão do deck tinha os números digitados no gerador. Três saíram errados —
copiados do deck de junho, que era de outro recorte — e outros três misturavam o recorte
urbano (104.108 setores) com o recorte com rurais (106.281) na mesma frase, sem dizer.

Aqui cada número é lido do CSV que o produziu, e **carrega o recorte junto**. O gerador
não digita valor nenhum: ele formata o que este arquivo entrega.

Uso:
    ./.venv/bin/python scripts/eda_central_dados.py banco_de_dados/eda/dados_deck.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ivs_censo import encontrar_raiz                                   # noqa: E402

RAIZ = encontrar_raiz(Path(__file__).resolve().parent)
EDA = RAIZ / 'banco_de_dados' / 'eda'
NAC = RAIZ / 'banco_de_dados' / 'nacional'

# Os dois recortes coexistem na pasta e NÃO são comparáveis linha a linha.
URBANO = 'setores urbanos elegíveis (104.108)'
RURAIS = 'elegíveis incluindo rurais (106.281)'
ORDEM_REGIAO = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']


def ler(pasta: Path, nome: str, **kw) -> pd.DataFrame:
    return pd.read_csv(pasta / f'{nome}.csv', sep=';', encoding='utf-8-sig', **kw)


def n2(v, casas=2):
    """Número no formato brasileiro: milhar com ponto, decimal com vírgula."""
    if pd.isna(v):
        return '—'
    s = f'{float(v):,.{casas}f}'
    return s.replace(',', '\x00').replace('.', ',').replace('\x00', '.')


def pct(v, casas=2):
    return n2(v, casas) + '%'


def inteiro(v):
    return f'{int(round(float(v))):,}'.replace(',', '.')


def bloco(titulo, recorte, fonte, colunas, linhas, nota=None):
    """Uma tabela pronta para o slide, com a procedência colada nela."""
    return {'titulo': titulo, 'recorte': recorte, 'fonte': fonte,
            'colunas': colunas, 'linhas': linhas, 'nota': nota}


def por_regiao(df, col_valor, casas=3, escala=1.0, coluna_regiao='regiao'):
    """Extrai valores por região na ordem canônica."""
    m = {r: None for r in ORDEM_REGIAO}
    for _, ln in df.iterrows():
        if ln[coluna_regiao] in m:
            m[ln[coluna_regiao]] = n2(float(ln[col_valor]) * escala, casas)
    return [m[r] for r in ORDEM_REGIAO]


d: dict = {'recortes': {'urbano': URBANO, 'com_rurais': RURAIS}, 'blocos': {}}
B = d['blocos']

# ── elegibilidade e recorte ─────────────────────────────────────────────────
el = ler(EDA, 'elegibilidade_setores', index_col=0)
d['eleg'] = {k: inteiro(el.loc[k, 'n_setores']) for k in el.index}
sit = ler(EDA, 'situacao_urbano_rural_total', index_col=0).iloc[0]
d['urbano_rural'] = {
    'n_setores': inteiro(sit['n_setores']), 'set_urbana': inteiro(sit['set_urbana']),
    'set_rural': inteiro(sit['set_rural']), 'dom_urbana': inteiro(sit['dom_urbana']),
    'dom_rural': inteiro(sit['dom_rural']),
    'pct_set_urbana': n2(sit['pct_set_urbana']), 'pct_set_rural': n2(sit['pct_set_rural']),
}
exc = ler(EDA, 'exclusao_rural_conferencia')
d['exclusao'] = {
    'n_ok_total': inteiro(exc['n_ok_total'].sum()), 'n_ok_urbano': inteiro(exc['n_ok_urbano'].sum()),
    'municipios': str(len(exc)),
    'perdem_10pct': str(int(((1 - exc['n_ok_urbano'] / exc['n_ok_total']) > 0.10).sum())),
    'menos_de_10_setores': str(int((exc['n_ok_urbano'] < 10).sum())),
}

# ── descritivas das 7 componentes ───────────────────────────────────────────
de = ler(EDA, 'descritivas_globais', index_col=0)
IVS7 = ['pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad', 'razao_moradores',
        'pct_analfab', 'renda_media', 'pct_raca_pretpardind']
ROT7 = {'pct_agua_inad': 'Água inadequada', 'pct_esgoto_inad': 'Esgoto inadequado',
        'pct_lixo_inad': 'Lixo inadequado', 'razao_moradores': 'Razão de moradores',
        'pct_analfab': 'Analfabetismo 15+', 'renda_media': 'Renda média (R$)',
        'pct_raca_pretpardind': 'Preta, parda ou indígena'}
B['descritivas'] = bloco(
    'As sete componentes em números', URBANO, 'descritivas_globais.csv',
    ['Componente', 'n', 'Média', 'Mediana', 'p75', 'Máx', 'Assim.'],
    [[ROT7[v], inteiro(de.loc[v, 'n']),
      n2(de.loc[v, 'media'], 2 if v == 'renda_media' else 3),
      n2(de.loc[v, 'mediana'], 2 if v == 'renda_media' else 3),
      n2(de.loc[v, 'p75'], 2 if v == 'renda_media' else 3),
      n2(de.loc[v, 'max'], 2 if v == 'renda_media' else 3),
      n2(de.loc[v, 'assim'], 2)] for v in IVS7])

# descritivas por região — média de cada componente
dr = ler(EDA, 'descritivas_por_regiao')
linhas = []
for v in IVS7:
    sub = dr[dr['variavel'] == v]
    linhas.append([ROT7[v]] + por_regiao(sub, 'media', 2 if v == 'renda_media' else 3))
B['por_regiao'] = bloco(
    'As sete componentes por região', URBANO, 'descritivas_por_regiao.csv',
    ['Componente'] + ORDEM_REGIAO, linhas,
    'Média entre setores. O gradiente Norte–Sul aparece em seis das sete.')

# ── outliers ────────────────────────────────────────────────────────────────
ou = ler(EDA, 'outliers', index_col=0)
B['outliers'] = bloco(
    'Outliers pela regra do IQR', URBANO, 'outliers.csv',
    ['Componente', 'q1', 'q3', 'Limite sup.', 'Outliers', '% da base', 'IQR serve?'],
    [[ROT7[v], n2(ou.loc[v, 'q1'], 3), n2(ou.loc[v, 'q3'], 3), n2(ou.loc[v, 'lim_sup'], 3),
      inteiro(ou.loc[v, 'n_outliers']), pct(ou.loc[v, 'pct_outliers']),
      'não' if bool(ou.loc[v, 'iqr_nao_informativo']) else 'sim'] for v in IVS7],
    'Onde a mediana e o q1 são zero, o IQR marca como atípico todo setor com qualquer inadequação.')

# ── faltantes ───────────────────────────────────────────────────────────────
mi = ler(EDA, 'missing_por_municipio', index_col=0)
col_analf = [c for c in mi.columns if 'analfab' in c]
d['missing'] = {
    'municipios': str(len(mi)),
    'pior_mun': str(mi[col_analf[0]].idxmax()) if col_analf else '—',
    'pior_pct': n2(mi[col_analf[0]].max()) if col_analf else '—',
}
au = ler(EDA, 'auditoria_analfabetismo_v00900_bins')
B['sigilo_porte'] = bloco(
    'O sigilo do analfabetismo depende do porte do setor', RURAIS,
    'auditoria_analfabetismo_v00900_bins.csv',
    ['Pessoas alfabetizadas no setor', 'Setores', 'Com V00901 sigilosa', '% sigilo'],
    [[ln['v900_bin'], inteiro(ln['n_setores']), inteiro(ln['n_v901_sigilo']), n2(ln['pct_sigilo'])]
     for _, ln in au.iterrows()],
    'De 44,09% nos setores menores a 3,33% nos maiores — a supressão não é aleatória.')

# ── blocos descritivos, todos do recorte urbano ─────────────────────────────
def desc_regiao(nome_arq, variavel, rotulo, escala=100, casas=2):
    df = ler(EDA, nome_arq)
    if 'variavel' in df.columns:
        df = df[df['variavel'] == variavel]
    return [rotulo] + por_regiao(df, 'media', casas, escala)

hp_g = ler(EDA, 'habitacao_precaria_global', index_col=0)
ib_g = ler(EDA, 'inadequacao_banheiro_global', index_col=0)
rf_g = ler(EDA, 'resp_feminino_global', index_col=0)
td_g = ler(EDA, 'tipo_domicilio_global', index_col=0)
d['descritivos'] = {
    # nomear a coluna: o global traz pct_dom_improv E pct_hab_precaria, e .iloc[0] pegava
    # a primeira — que é a de improvisados, com rótulo de precária
    'hab_precaria': pct(float(hp_g.loc['mean', 'pct_hab_precaria']) * 100),
    'dom_improv': pct(float(hp_g.loc['mean', 'pct_dom_improv']) * 100),
    'sem_banheiro': pct(float(ib_g.loc['mean', 'pct_sem_banheiro']) * 100),
    'sem_banheiro_nem_sanit': pct(float(ib_g.loc['mean', 'pct_sem_banheiro_nem_sanitario']) * 100),
    'resp_feminino': pct(float(rf_g.loc['mean', rf_g.columns[0]]) * 100),   # tabela de coluna única
    'apartamento': pct(float(td_g.loc['mean', 'pct_apartamento']) * 100),
    'convencional': pct(float(td_g.loc['mean', 'pct_moradia_convencional']) * 100),
}
B['descritivos_regiao'] = bloco(
    'Os blocos descritivos, por região', URBANO,
    'habitacao_precaria · inadequacao_banheiro · resp_feminino · tipo_domicilio (por_regiao)',
    ['Indicador'] + ORDEM_REGIAO,
    [desc_regiao('habitacao_precaria_por_regiao', 'pct_hab_precaria', 'Habitação precária (%)'),
     desc_regiao('habitacao_precaria_por_regiao', 'pct_dom_improv', 'Domicílios improvisados (%)'),
     desc_regiao('inadequacao_banheiro_por_regiao', 'pct_sem_banheiro', 'Sem banheiro exclusivo (%)'),
     desc_regiao('inadequacao_banheiro_por_regiao', 'pct_sem_banheiro_nem_sanitario', 'Sem banheiro nem sanitário (%)'),
     desc_regiao('resp_feminino_por_regiao', None, 'Chefia feminina (%)'),
     desc_regiao('tipo_domicilio_por_regiao', 'pct_apartamento', 'Apartamento (%)'),
     desc_regiao('tipo_domicilio_por_regiao', 'pct_moradia_convencional', 'Moradia convencional (%)')],
    'Média entre setores, todas no mesmo recorte — o que a versão anterior deste deck não garantia.')

# ── envelhecimento ──────────────────────────────────────────────────────────
env_t = ler(EDA, 'indicadores_envelhecimento_total').iloc[0]
env_r = ler(EDA, 'indicadores_envelhecimento_por_regiao')
d['envelhecimento'] = {'IEP': n2(env_t['IEP'], 1), 'RDI': n2(env_t['RDI'], 1),
                       'pct_60mais': n2(env_t['pct_60mais']), 'pct_0a14': n2(env_t['pct_pop_0a14'])}
B['envelhecimento'] = bloco(
    'Envelhecimento populacional por região', URBANO, 'indicadores_envelhecimento_por_regiao.csv',
    ['Indicador'] + ORDEM_REGIAO,
    [['População (milhões)'] + por_regiao(env_r, 'pop_total', 1, 1e-6),
     ['Menores de 15 anos (%)'] + por_regiao(env_r, 'pct_pop_0a14', 2),
     ['60 anos ou mais (%)'] + por_regiao(env_r, 'pct_60mais', 2),
     ['Índice de envelhecimento (IEP)'] + por_regiao(env_r, 'IEP', 1),
     ['Razão de dependência (RDI)'] + por_regiao(env_r, 'RDI', 1)],
    'IEP = 60+ ÷ menores de 15 × 100, conforme Galvão et al. (Hygeia, 2025).')

# ── favelas ─────────────────────────────────────────────────────────────────
fc = ler(EDA, 'favelas_fcu_total').iloc[0]
d['fcu'] = {k: (inteiro(fc[k]) if 'pct' not in k else n2(fc[k])) for k in
            ['n_setores_fcu', 'pct_setores_fcu', 'n_fcu_distintas', 'pop_fcu', 'pct_pop_fcu',
             'dom_fcu', 'pct_dom_fcu']}
cmp_fcu = ler(EDA, 'favelas_fcu_comparativo_indicadores')
c_ind = [c for c in cmp_fcu.columns if c.lower() in ('indicador', 'variavel')][0]
cols = list(cmp_fcu.columns)
B['favela_resto'] = bloco(
    'Favela e restante da cidade, indicador a indicador', URBANO,
    'favelas_fcu_comparativo_indicadores.csv',
    [c.replace('_', ' ') for c in cols],
    [[str(ln[c]) if not isinstance(ln[c], float) else n2(ln[c], 3) for c in cols]
     for _, ln in cmp_fcu.iterrows()],
    'Quantas vezes o valor médio no setor de favela supera o de fora.')

# ── cobertura e faixas (recorte COM RURAIS — declarado) ─────────────────────
cb = ler(EDA, 'cobertura_total').iloc[0]
d['cobertura'] = {'n': inteiro(cb['n_setores_OK']),
                  'agua': n2(cb['pct_agua_adeq_100']), 'esgoto': n2(cb['pct_esgoto_adeq_100']),
                  'lixo': n2(cb['pct_lixo_adeq_100']), 'tres': n2(cb['pct_saneamento_3_100']),
                  'coleta': n2(cb['pct_coleta_lixo_100']), 'dados7': n2(cb['pct_dados_7vars_100'])}
cbr = ler(EDA, 'cobertura_por_regiao')
B['cobertura_regiao'] = bloco(
    'Cobertura integral de saneamento por região', RURAIS, 'cobertura_por_regiao.csv',
    ['Serviço 100% adequado'] + ORDEM_REGIAO,
    [['Água (%)'] + por_regiao(cbr, 'pct_agua_adeq_100', 1),
     ['Esgoto (%)'] + por_regiao(cbr, 'pct_esgoto_adeq_100', 1),
     ['Lixo (%)'] + por_regiao(cbr, 'pct_lixo_adeq_100', 1),
     ['Os três juntos (%)'] + por_regiao(cbr, 'pct_saneamento_3_100', 1)],
    'Setores em que NENHUM domicílio está na condição inadequada.')

sa = ler(EDA, 'saneamento_categorias_por_regiao')
linhas = []
for var in sa['variavel'].unique():
    sub = sa[sa['variavel'] == var]
    linhas.append([var, 'setores em 0%'] + por_regiao(sub, 'pct_0', 1))
    linhas.append(['', 'setores em 50% ou mais'] + por_regiao(sub, 'pct_50mais', 1))
B['saneamento_faixas'] = bloco(
    'Gravidade do saneamento em faixas', RURAIS, 'saneamento_categorias_por_regiao.csv',
    ['Serviço', 'Faixa'] + ORDEM_REGIAO, linhas)

mo = ler(EDA, 'morfologia_v00048_v00058_por_regiao')
B['morfologia'] = bloco(
    'Tipo de espécie do domicílio', RURAIS, 'morfologia_v00048_v00058_por_regiao.csv',
    ['Código', 'Tipo', 'Total (%)'] + ORDEM_REGIAO,
    [[ln['codigo'], ln['tipo'], n2(ln['pct_total'], 3)] +
     [n2(ln[f'pct_{r}'], 3) for r in ORDEM_REGIAO] for _, ln in mo.iterrows()],
    'Percentual sobre domicílios (V00001 + V00002), não sobre setores.')

# ── água canalizada ─────────────────────────────────────────────────────────
ag = ler(EDA, 'agua_canalizada_por_regiao')
B['agua'] = bloco(
    'Canalização da água por região', URBANO, 'agua_canalizada_por_regiao.csv',
    ['Região', 'Dentro de casa', 'Só no terreno', 'Não chega', 'Sem canalização', 'Suprimido'],
    [[ln['regiao'], n2(ln['pct_dentro_casa']), n2(ln['pct_so_terreno']), n2(ln['pct_nao_encanada']),
      n2(ln['pct_sem_canalizacao']), n2(ln['pct_suprimido'])] for _, ln in ag.iterrows()],
    'Razão agregada sobre domicílios. "Suprimido" é a parcela que o sigilo tira de V00200 e V00201.')

# ── nacional ────────────────────────────────────────────────────────────────
if (NAC / 'comparativo_brasil_vs_elsi.csv').exists():
    cp = ler(NAC, 'comparativo_brasil_vs_elsi')
    c_ind = cp.columns[0]
    br = [c for c in cp.columns if 'BR_urbano' in c and 'razao_agregada' in c]
    el_ = [c for c in cp.columns if 'ELSI70_urbano' in c and 'razao_agregada' in c]
    if br and el_:
        B['brasil_elsi'] = bloco(
            'A amostra ELSI comparada com o Brasil urbano', 'Brasil urbano × ELSI-70 urbano',
            'nacional/comparativo_brasil_vs_elsi.csv',
            ['Indicador', 'Brasil urbano', 'ELSI-70', 'Razão'],
            [[ROT7[v], n2(cp.loc[cp[c_ind] == v, br[0]].iloc[0], 3),
              n2(cp.loc[cp[c_ind] == v, el_[0]].iloc[0], 3),
              n2(float(cp.loc[cp[c_ind] == v, el_[0]].iloc[0])
                 / float(cp.loc[cp[c_ind] == v, br[0]].iloc[0]), 2)]
             for v in IVS7 if v in set(cp[c_ind])],
            'Razão agregada: soma dos numeradores ÷ soma dos denominadores em cada recorte.')
    rp = ler(NAC, 'representatividade_elsi_no_brasil').set_index('metrica')
    d['nacional'] = {i: {'Brasil': inteiro(rp.loc[i, 'Brasil']), 'ELSI': inteiro(rp.loc[i, 'ELSI_70'])}
                     for i in rp.index}

Path(sys.argv[1] if len(sys.argv) > 1 else EDA / 'dados_deck.json').write_text(
    json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'{len(B)} blocos de tabela + {len(d) - 2} conjuntos de indicadores')
for k, v in B.items():
    print(f'  {k:22} {len(v["linhas"]):>3} linhas · {v["recorte"]}')
