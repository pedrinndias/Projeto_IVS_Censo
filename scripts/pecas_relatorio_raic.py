"""Peças visuais do relatório parcial RAIC 2026: Figura 1, Tabela 1 e Quadro 2.

Os 12 indicadores são os da matriz de correlação que o Pedro definiu em 11/10/2026
(`relatorio_parcial_raic/ARQUITETURA.md`, §10): o IVS-7, sem água canalizada, sem banheiro,
moradia não convencional e os dois grupos do índice de envelhecimento do projeto — idosos
(60+) e crianças (menores de 15), o numerador e o denominador do `iep_setor`.

Travas (abortam se falharem):
  1. a matriz S6 de `fatorial_ampliada.py` se reproduz (n = 69.458; renda × PPI = 0,79),
     o que prova que o método daqui é o mesmo da matriz que o Pedro aprovou;
  2. n, média, mediana e máximo da T03 batem com o .db nos 12 indicadores, e as 7 linhas do
     IVS-7 da Tabela 1 batem com a tabela que o Pedro aprovou;
  3. o Quadro 2 tem Saneamento 5, Socioeconômica 4, Morfologia 1 e Demografia 2.

Uso:
    ./.venv/bin/python scripts/pecas_relatorio_raic.py

Saídas em `relatorio_parcial_raic/`: `figuras/fig1_correlacao.png` e, em `dados/`,
`matriz_spearman.csv`, `tabela1_descritivas.csv`, `quadro2_indicadores.csv` e `pecas.json`
(todo número que o texto do relatório cita sai daqui).
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from fatorial_ampliada import TINTA, rampa_divergente  # noqa: E402  (paleta da matriz aprovada)

RAIZ = Path(__file__).resolve().parents[1]
DB = RAIZ / 'banco_de_dados' / 'entrega_orientadora' / 'Base_ELSI_70Municipios_Censo2022.db'
T03 = RAIZ / 'analises_exploratorias' / '00_referencia' / 'tabelas' / 'T03_descritivas_global.csv'
QUADRO = RAIZ / 'banco_de_dados' / 'entrega_orientadora' / 'Quadro_Indicadores.csv'
SAIDA = RAIZ / 'relatorio_parcial_raic'
FIG, DADOS = SAIDA / 'figuras', SAIDA / 'dados'

# (coluna no .db, rótulo na figura, rótulo na tabela e no quadro) — na ordem da matriz do Pedro
INDICADORES = [
    ('pct_agua_inad', 'Água inadequada', 'Água inadequada'),
    ('pct_esgoto_inad', 'Esgoto inadequado', 'Esgoto inadequado'),
    ('pct_lixo_inad', 'Lixo inadequado', 'Lixo inadequado'),
    ('razao_moradores', 'Razão de moradores', 'Razão de moradores'),
    ('pct_analfab', 'Analfabetismo 15+', 'Analfabetismo 15+'),
    ('renda_media_sem_extremo', 'Renda (invertida)', 'Renda média (R$)'),
    ('pct_raca_pretpardind', 'Cor/raça PPI', 'Preta, parda ou indígena'),
    ('pct_sem_agua_canalizada', 'Sem água canalizada', 'Sem água canalizada'),
    ('pct_sem_banheiro', 'Sem banheiro', 'Sem banheiro'),
    ('pct_moradia_nao_convencional', 'Moradia não convencional', 'Moradia não convencional'),
    ('pct_idoso_60mais', 'Idosos (60+)', 'Idosos (60 anos ou mais)'),
    ('pct_pop_0a14', 'Crianças (0–14)', 'Crianças (0 a 14 anos)'),
]
COLUNAS = [c for c, _, _ in INDICADORES]
N_IVS7 = 7
RENDA = 'renda_media_sem_extremo'

# Trava 1: a matriz "IVS-7 e as quatro novas (S6)" de fatorial_ampliada.py, com a renda original
S6 = ['pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad', 'razao_moradores', 'pct_analfab',
      'renda_media', 'pct_raca_pretpardind', 'pct_agua_nao_encanada', 'pct_sem_agua_canalizada',
      'pct_sem_banheiro', 'pct_moradia_nao_convencional']

# Trava 2: a tabela que o Pedro aprovou (imagem de 11/10), linha a linha. Única diferença:
# o máximo do analfabetismo é 37/51 = 0,72549…, que dá 0,725; a imagem trazia 0,726 por
# arredondamento duplo (0,7255 → 0,726).
APROVADA = {
    'pct_agua_inad': ['104.108', '0,070', '0,000', '0,012', '1,000', '3,42'],
    'pct_esgoto_inad': ['104.107', '0,082', '0,000', '0,018', '1,000', '2,98'],
    'pct_lixo_inad': ['104.108', '0,116', '0,000', '0,059', '1,000', '2,38'],
    'razao_moradores': ['104.108', '2,691', '2,713', '2,926', '6,913', '−0,22'],
    'pct_analfab': ['87.556', '0,036', '0,027', '0,050', '0,725', '2,34'],
    'renda_media_sem_extremo': ['104.095', '4.185,81', '2.572,39', '4.835,82', '140.172,64', '3,20'],
    'pct_raca_pretpardind': ['104.106', '0,527', '0,572', '0,704', '1,000', '−0,39'],
}

# Trava 3: contagem do Quadro 2 por dimensão, na ordem em que o quadro é impresso
DIMENSOES = {'Saneamento': 5, 'Socioeconômica': 4, 'Morfologia': 1, 'Demografia': 2}


def trava(ok: bool, msg: str) -> None:
    if not ok:
        sys.exit(f'TRAVA FALHOU: {msg}')


def br(v: float, casas: int) -> str:
    """Número no padrão brasileiro: ponto de milhar, vírgula decimal, sinal de menos tipográfico.

    Arredonda pela NBR 5891 (5 seguido só de zeros vai para o par), depois de tirar o ruído do
    float: o p75 da renda é 4835,825 exato e o float guarda 4835,825000000001.
    """
    d = Decimal(repr(round(float(v), 9))).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_EVEN)
    s = f'{d:,.{casas}f}'.replace(',', '_').replace('.', ',').replace('_', '.')
    return s.replace('-', '−')


def carregar() -> pd.DataFrame:
    cols = sorted(set(COLUNAS) | set(S6))
    con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    df = pd.read_sql(f"SELECT NM_MUN, CD_UF, urbano, Dados_sig, {', '.join(cols)} FROM setores_censitarios", con)
    con.close()
    # mesmo filtro de fatorial_ampliada.carregar(): setor urbano e elegível
    df = df[(pd.to_numeric(df['urbano'], errors='coerce') == 1) & (df['Dados_sig'] == 'OK')]
    df = df[cols].apply(pd.to_numeric, errors='coerce').assign(NM_MUN=df['NM_MUN'], CD_UF=df['CD_UF'].astype(str))
    trava(len(df) == 104_108, f'recorte com {len(df)} setores, esperado 104.108')
    return df


def spearman(df: pd.DataFrame, colunas: list[str], renda: str) -> tuple[int, pd.DataFrame]:
    """Spearman com exclusão por lista e renda invertida (valor maior = renda menor), como no NB04."""
    d = df[colunas].copy()
    d[renda] = -d[renda]
    d = d.dropna()
    return len(d), d.corr(method='spearman')


def robustez(df: pd.DataFrame) -> dict:
    """Duas checagens da Figura 1 pedidas na revisão (council de 11/10/2026).

    - pares: Spearman com todos os setores que têm o par (sem a exclusão por lista, que tira os
      setores com sigilo, os de melhor condição);
    - intra: Spearman dos postos dentro de cada município, isto é, só a variação intraurbana;
      e, nos municípios com 30 setores ou mais, quantos têm idosos × renda negativa.
    """
    d = df[COLUNAS].copy()
    d[RENDA] = -d[RENDA]
    pares = d.corr(method='spearman')  # pandas usa os pares completos
    c = d.dropna().assign(NM_MUN=df['NM_MUN'])
    postos = c.groupby('NM_MUN')[COLUNAS].rank(pct=True)
    intra = postos.corr()  # Pearson dos postos = Spearman intraurbano
    grandes = c.groupby('NM_MUN').filter(lambda g: len(g) >= 30)
    por_mun = grandes.groupby('NM_MUN')[['pct_idoso_60mais', RENDA]].apply(
        lambda g: g.corr(method='spearman').iloc[0, 1])
    sel = [(RENDA, 'pct_raca_pretpardind'), ('pct_analfab', RENDA), ('pct_agua_inad', 'pct_esgoto_inad'),
           ('pct_idoso_60mais', RENDA), ('pct_pop_0a14', RENDA), ('pct_idoso_60mais', 'pct_pop_0a14')]
    return {
        'pares': {f'{a}|{b}': round(float(pares.loc[a, b]), 4) for a, b in sel},
        'intra': {f'{a}|{b}': round(float(intra.loc[a, b]), 4) for a, b in sel},
        'municipios_30mais': int(len(por_mun)),
        'municipios_idoso_renda_negativa': int((por_mun < 0).sum()),
        'mediana_municipal_idoso_renda': round(float(por_mun.median()), 4),
    }


def figura(R: pd.DataFrame) -> Path:
    nomes = [f for _, f, _ in INDICADORES]
    M = R.loc[COLUNAS, COLUNAS].to_numpy()
    p = len(nomes)
    fig, ax = plt.subplots(figsize=(7.6, 6.9), facecolor='white')
    ax.imshow(np.array([[rampa_divergente(M[i, j]) for j in range(p)] for i in range(p)]))
    for i in range(p):
        for j in range(p):
            ax.text(j, i, br(M[i, j], 2), ha='center', va='center', fontsize=9,
                    color='white' if abs(M[i, j]) > 0.55 else TINTA)
    ax.axhline(N_IVS7 - 0.5, color=TINTA, lw=1.6)
    ax.axvline(N_IVS7 - 0.5, color=TINTA, lw=1.6)
    ax.set_xticks(range(p))
    ax.set_xticklabels(nomes, rotation=45, ha='right', fontsize=10)
    ax.set_yticks(range(p))
    ax.set_yticklabels(nomes, fontsize=10)
    # sem título: a legenda da Figura 1 fica no texto do relatório
    FIG.mkdir(parents=True, exist_ok=True)
    caminho = FIG / 'fig1_correlacao.png'
    fig.savefig(caminho, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return caminho


def tabela1(df: pd.DataFrame) -> pd.DataFrame:
    t03 = pd.read_csv(T03).set_index('indicador')
    linhas = []
    for col, _, rotulo in INDICADORES:
        r, s = t03.loc[col], df[col].dropna()
        trava(int(r['n']) == len(s) and np.isclose(r['media'], s.mean())
              and np.isclose(r['mediana'], s.median()) and np.isclose(r['max'], s.max()),
              f'a T03 não bate com o .db em {col}')
        casas = 2 if col == RENDA else 3
        fmt = [br(r['n'], 0), br(r['media'], casas), br(r['mediana'], casas),
               br(r['p75'], casas), br(r['max'], casas), br(r['assim'], 2)]
        if col in APROVADA:
            trava(fmt == APROVADA[col], f'{col}: {fmt} difere da tabela aprovada {APROVADA[col]}')
        linhas.append({'indicador': col, 'Indicador': rotulo, 'n': fmt[0], 'Média': fmt[1],
                       'Mediana': fmt[2], 'p75': fmt[3], 'Máx': fmt[4], 'Assim.': fmt[5],
                       'n_bruto': int(r['n']), 'media_bruta': float(r['media'])})
    return pd.DataFrame(linhas)


def quadro2() -> pd.DataFrame:
    q = pd.read_csv(QUADRO, sep=';', encoding='utf-8-sig').set_index('indicador')
    linhas = []
    for col, _, rotulo in INDICADORES:
        r = q.loc['renda_media' if col == RENDA else col]
        # tira as notas técnicas entre parênteses ("reproduz o V0005…", "complemento de V00199…")
        mede = re.sub(r'\s*\((?:reproduz|complemento)[^)]*\)', '', r['o_que_mede']).strip()
        linhas.append({'Dimensão': r['dimensao'], 'Indicador': rotulo, 'O que mede': mede,
                       'IVS-7': r['entra_no_ivs7'], 'indicador': col})
    quadro = pd.DataFrame(linhas)
    contagem = quadro['Dimensão'].value_counts().to_dict()
    trava(contagem == DIMENSOES, f'Quadro 2 por dimensão = {contagem}, esperado {DIMENSOES}')
    ordem = {d: i for i, d in enumerate(DIMENSOES)}
    return quadro.sort_values('Dimensão', key=lambda s: s.map(ordem), kind='stable')


def main() -> None:
    df = carregar()

    n6, R6 = spearman(df, S6, 'renda_media')
    trava(n6 == 69_458 and round(R6.loc['renda_media', 'pct_raca_pretpardind'], 2) == 0.79
          and round(R6.loc['pct_analfab', 'renda_media'], 2) == 0.76,
          f'a matriz S6 não se reproduz (n = {n6})')

    n, R = spearman(df, COLUNAS, RENDA)
    fig = figura(R)
    tab = tabela1(df)
    quadro = quadro2()

    DADOS.mkdir(parents=True, exist_ok=True)
    rot = {c: f for c, f, _ in INDICADORES}
    R.loc[COLUNAS, COLUNAS].rename(index=rot, columns=rot).round(4).to_csv(
        DADOS / 'matriz_spearman.csv', encoding='utf-8-sig')
    tab.drop(columns=['n_bruto', 'media_bruta']).to_csv(
        DADOS / 'tabela1_descritivas.csv', index=False, encoding='utf-8-sig')
    quadro.to_csv(DADOS / 'quadro2_indicadores.csv', index=False, encoding='utf-8-sig')
    pecas = {
        'gerado_por': 'scripts/pecas_relatorio_raic.py',
        'setores_no_recorte': 104_108,
        'trava_s6': {'n': n6, 'renda_x_ppi': round(float(R6.loc['renda_media', 'pct_raca_pretpardind']), 4)},
        'figura1': {'n_dados_completos': n, 'metodo': 'Spearman, exclusão por lista, renda invertida',
                    'indicadores': COLUNAS,
                    'R': {a: {b: round(float(R.loc[a, b]), 4) for b in COLUNAS} for a in COLUNAS}},
        'robustez_figura1': robustez(df),
        # contexto da média regional da renda: peso de Brasília no Centro-Oeste (código de UF iniciado em 5)
        'centro_oeste': {'setores': int((df['CD_UF'].str[:1] == '5').sum()),
                         'brasilia': int(((df['CD_UF'].str[:1] == '5') & (df['NM_MUN'] == 'Brasília')).sum())},
        'tabela1': tab.drop(columns=['Indicador']).to_dict(orient='records'),
        'quadro2_por_dimensao': DIMENSOES,
    }
    (DADOS / 'pecas.json').write_text(json.dumps(pecas, ensure_ascii=False, indent=1), encoding='utf-8')

    print(f'Travas 1–3 ok. Figura 1: n = {br(n, 0)} setores com dados completos -> {fig.relative_to(RAIZ)}')
    for a, b in [(RENDA, 'pct_raca_pretpardind'), ('pct_analfab', RENDA), ('pct_agua_inad', 'pct_esgoto_inad'),
                 ('pct_idoso_60mais', RENDA), ('pct_pop_0a14', RENDA), ('pct_idoso_60mais', 'pct_pop_0a14')]:
        print(f'  {rot[a]} × {rot[b]}: {br(R.loc[a, b], 2)}')
    print(tab[['Indicador', 'n', 'Média', 'Mediana', 'p75', 'Máx', 'Assim.']].to_string(index=False))
    print(quadro[['Dimensão', 'Indicador', 'IVS-7']].to_string(index=False))
    print(f'Dados em {DADOS.relative_to(RAIZ)}/')


if __name__ == '__main__':
    main()
