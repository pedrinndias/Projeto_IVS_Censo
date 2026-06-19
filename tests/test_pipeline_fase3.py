"""Testes sanity-check da pipeline Fase 3.

Executar:
    python -m pytest tests/ -v

Estes testes não rodam a pipeline; eles apenas verificam que os artefatos
finais (Base_ELSI_Bruta_Censo2022.csv + CSVs em banco_de_dados/eda/) estão
presentes e com as características esperadas.
"""
from __future__ import annotations          # permite anotações de tipo "adiadas" (ex.: -> pd.DataFrame sem aspas) em Python antigo
from pathlib import Path                     # caminhos como objetos
import pandas as pd                          # leitura dos CSVs a verificar
import pytest                                # framework de testes (asserts, skip, parametrize)

ROOT = Path(__file__).resolve().parents[1]   # raiz do projeto = 1 nível acima da pasta tests/ (parents[1])
BD = ROOT / 'banco_de_dados'                 # pasta de saídas da pipeline
EDA = BD / 'eda'                             # subpasta com os CSVs da EDA

# Conjunto esperado dos 7 indicadores-componente do IVS (usado em vários testes)
ESPERADOS_INDICADORES = {
    'pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad',
    'razao_moradores', 'pct_analfab', 'renda_media', 'pct_raca_pretpardind',
}


def _read(p: Path) -> pd.DataFrame:          # helper: lê um CSV no padrão do projeto
    return pd.read_csv(p, sep=';', encoding='utf-8-sig')  # separador ';' e encoding utf-8-sig (com BOM)


def test_lista_elsi_tem_70_municipios():     # TESTE: a lista oficial tem exatamente 70 municípios e sem nulos nas chaves
    df = pd.read_csv(ROOT / 'dados' / 'municipios_elsi_brasil.csv', sep=';', dtype=str)
    assert len(df) == 70                      # tem que ter 70 linhas
    assert df['nm_municipio'].notna().all()   # nenhum nome de município nulo
    assert df['uf_codigo'].notna().all()      # nenhum código de UF nulo


def test_base_bruta_existe_e_tem_109032_setores():  # TESTE: a base bruta tem 109.032 setores e 70 municípios
    base = BD / 'Base_ELSI_Bruta_Censo2022.csv'
    if not base.exists():                     # a base não é versionada (~17 MB); se não foi gerada localmente...
        pytest.skip(                          # ...pula o teste (não falha) com uma mensagem explicativa
            f'Base bruta não está versionada (~17 MB) e não foi gerada localmente: {base}. '
            'Rode notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb antes do teste.'
        )
    df = pd.read_csv(base, sep=';', dtype=str)
    assert len(df) == 109_032, f'Esperado 109.032 setores, obtido {len(df)}'  # contagem exata de setores
    assert df['CD_MUN'].nunique() == 70       # exatamente 70 municípios distintos


def test_descritivas_globais_tem_7_indicadores():  # TESTE: o CSV global lista exatamente os 7 indicadores esperados
    df = _read(EDA / 'descritivas_globais.csv')
    df = df.rename(columns={df.columns[0]: 'variavel'})  # a 1ª coluna (índice exportado) vira 'variavel'
    assert set(df['variavel']) == ESPERADOS_INDICADORES  # o conjunto de variáveis bate com o esperado


def test_descritivas_por_municipio_tem_490_linhas():  # TESTE: 70 municípios × 7 indicadores = 490 linhas
    df = _read(EDA / 'descritivas_por_municipio.csv')
    # 70 municípios × 7 indicadores = 490
    assert len(df) == 490                     # contagem total de linhas
    assert df['NM_MUN'].nunique() == 70       # 70 municípios distintos


def test_descritivas_por_regiao_tem_35_linhas():  # TESTE: 5 regiões × 7 indicadores = 35 linhas
    df = _read(EDA / 'descritivas_por_regiao.csv')
    # 5 regiões × 7 indicadores
    assert len(df) == 35                       # contagem total de linhas
    assert df['regiao'].nunique() == 5         # 5 regiões distintas


def test_correlacoes_simetricas():            # TESTE: as matrizes de correlação são 7×7, simétricas e com diagonal = 1
    for f in ['correlacao_pearson.csv', 'correlacao_spearman.csv']:  # testa as duas matrizes
        df = pd.read_csv(EDA / f, sep=';', index_col=0)  # 1ª coluna é o índice (nomes das variáveis)
        assert df.shape == (7, 7)             # tem que ser 7×7
        # Diagonal igual a 1
        for c in df.columns:                  # para cada variável...
            assert abs(df.loc[c, c] - 1.0) < 1e-9  # correlação consigo mesma = 1 (tolerância p/ float)
        # Simetria
        for i in df.columns:                  # corr(i, j) deve ser igual a corr(j, i)
            for j in df.columns:
                assert abs(df.loc[i, j] - df.loc[j, i]) < 1e-9  # simetria (tolerância p/ float)


def test_elegibilidade_setores_soma_109032():  # TESTE: a soma das classes Dados_sig devolve os 109.032 setores
    df = _read(EDA / 'elegibilidade_setores.csv')
    df = df.rename(columns={df.columns[0]: 'Dados_sig'})  # 1ª coluna (índice exportado) vira 'Dados_sig'
    assert df['n_setores'].sum() == 109_032   # soma de todas as classes = total de setores


@pytest.mark.parametrize('arquivo', [         # TESTE parametrizado: roda uma vez por arquivo da lista abaixo
    'descritivas_globais.csv',
    'descritivas_por_municipio.csv',
    'descritivas_por_regiao.csv',
    'outliers.csv',
    'missing_por_municipio.csv',
    'correlacao_pearson.csv',
    'correlacao_spearman.csv',
    'elegibilidade_setores.csv',
])
def test_arquivos_eda_existem(arquivo):       # verifica que cada CSV esperado da EDA existe
    assert (EDA / arquivo).exists(), f'Faltando: {arquivo}'


def test_figuras_eda_existem():               # TESTE: as 4 figuras esperadas da EDA existem
    fig_dir = EDA / 'figuras'
    for png in ['histogramas.png', 'boxplots_por_regiao.png',
                'matriz_correlacao.png', 'missing_por_municipio.png']:
        assert (fig_dir / png).exists(), f'Faltando figura: {png}'
