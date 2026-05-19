"""Testes sanity-check da pipeline Fase 3.

Executar:
    python -m pytest tests/ -v

Estes testes não rodam a pipeline; eles apenas verificam que os artefatos
finais (Base_ELSI_Bruta_Censo2022.csv + CSVs em banco_de_dados/eda/) estão
presentes e com as características esperadas.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
BD = ROOT / 'banco_de_dados'
EDA = BD / 'eda'

ESPERADOS_INDICADORES = {
    'pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad',
    'razao_moradores', 'pct_analfab', 'renda_media', 'pct_raca_pretpardind',
}


def _read(p: Path) -> pd.DataFrame:
    return pd.read_csv(p, sep=';', encoding='utf-8-sig')


def test_lista_elsi_tem_70_municipios():
    df = pd.read_csv(ROOT / 'dados' / 'municipios_elsi_brasil.csv', sep=';', dtype=str)
    assert len(df) == 70
    assert df['nm_municipio'].notna().all()
    assert df['uf_codigo'].notna().all()


def test_base_bruta_existe_e_tem_109032_setores():
    base = BD / 'Base_ELSI_Bruta_Censo2022.csv'
    if not base.exists():
        pytest.skip(
            f'Base bruta não está versionada (~17 MB) e não foi gerada localmente: {base}. '
            'Rode notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb antes do teste.'
        )
    df = pd.read_csv(base, sep=';', dtype=str)
    assert len(df) == 109_032, f'Esperado 109.032 setores, obtido {len(df)}'
    assert df['CD_MUN'].nunique() == 70


def test_descritivas_globais_tem_7_indicadores():
    df = _read(EDA / 'descritivas_globais.csv')
    df = df.rename(columns={df.columns[0]: 'variavel'})
    assert set(df['variavel']) == ESPERADOS_INDICADORES


def test_descritivas_por_municipio_tem_490_linhas():
    df = _read(EDA / 'descritivas_por_municipio.csv')
    # 70 municípios × 7 indicadores = 490
    assert len(df) == 490
    assert df['NM_MUN'].nunique() == 70


def test_descritivas_por_regiao_tem_35_linhas():
    df = _read(EDA / 'descritivas_por_regiao.csv')
    # 5 regiões × 7 indicadores
    assert len(df) == 35
    assert df['regiao'].nunique() == 5


def test_correlacoes_simetricas():
    for f in ['correlacao_pearson.csv', 'correlacao_spearman.csv']:
        df = pd.read_csv(EDA / f, sep=';', index_col=0)
        assert df.shape == (7, 7)
        # Diagonal igual a 1
        for c in df.columns:
            assert abs(df.loc[c, c] - 1.0) < 1e-9
        # Simetria
        for i in df.columns:
            for j in df.columns:
                assert abs(df.loc[i, j] - df.loc[j, i]) < 1e-9


def test_elegibilidade_setores_soma_109032():
    df = _read(EDA / 'elegibilidade_setores.csv')
    df = df.rename(columns={df.columns[0]: 'Dados_sig'})
    assert df['n_setores'].sum() == 109_032


@pytest.mark.parametrize('arquivo', [
    'descritivas_globais.csv',
    'descritivas_por_municipio.csv',
    'descritivas_por_regiao.csv',
    'outliers.csv',
    'missing_por_municipio.csv',
    'correlacao_pearson.csv',
    'correlacao_spearman.csv',
    'elegibilidade_setores.csv',
])
def test_arquivos_eda_existem(arquivo):
    assert (EDA / arquivo).exists(), f'Faltando: {arquivo}'


def test_figuras_eda_existem():
    fig_dir = EDA / 'figuras'
    for png in ['histogramas.png', 'boxplots_por_regiao.png',
                'matriz_correlacao.png', 'missing_por_municipio.png']:
        assert (fig_dir / png).exists(), f'Faltando figura: {png}'
