"""Testes do módulo compartilhado `src/ivs_censo`.

Diferente de `test_pipeline_fase3.py` (que confere artefatos já gerados), estes testes
exercitam as fórmulas diretamente, com dados sintéticos — servem de rede de proteção
para o cálculo nacional (`scripts/proporcoes_brasil.py`), que não tem um artefato
pequeno para conferir.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from ivs_censo import (ARQUIVOS_CENSO, MAPA_VARIAVEL_ARQUIVO, calcular_indicadores,  # noqa: E402
                       classificar_dados_sig, safe_div, tabela_variaveis)
from ivs_censo.indicadores import INDICADORES_IVS, TODOS_INDICADORES                  # noqa: E402


def test_safe_div_nao_estoura_com_zero():
    """Denominador zero ou negativo devolve NaN — nunca inf, nunca zero silencioso."""
    r = safe_div([10, 10, 10], [2, 0, -1])
    assert r[0] == 5
    assert np.isnan(r[1]) and np.isnan(r[2])


def test_classificar_dados_sig_prioriza_populacao_zero():
    """Setor sem população com V00001 vazio é ZERADO (massa d'água), não SIGILOSO."""
    df = pd.DataFrame({
        'v0001':  [1000.0, 0.0,   np.nan, 500.0, 0.0],
        'V00001': [300.0,  np.nan, 100.0, 0.0,   0.0],
    })
    sig = classificar_dados_sig(df)
    assert list(sig) == ['OK', 'ZERADO', 'SIGILOSO', 'COLETIVO', 'ZERADO']


def _linha_sintetica(**kwargs):
    """Um setor com valores redondos, para conferir as fórmulas na mão."""
    base = {c: 0.0 for c in {v for ind in TODOS_INDICADORES for v in (*ind.numerador, *ind.denominador)}}
    base.update(kwargs)
    return pd.DataFrame([base])


def test_proporcoes_de_saneamento_usam_v00001():
    df = _linha_sintetica(V00001=100.0, V00112=5.0, V00113=5.0, V00312=20.0, V00398=10.0)
    r = calcular_indicadores(df, INDICADORES_IVS).iloc[0]
    assert r['pct_agua_inad'] == pytest.approx(0.10)     # (5+5)/100
    assert r['pct_esgoto_inad'] == pytest.approx(0.20)   # 20/100
    assert r['pct_lixo_inad'] == pytest.approx(0.10)     # 10/100


def test_analfabetismo_usa_total_de_15_mais():
    """A taxa é V00901 / (V00900 + V00901) — não V00901 / V00900."""
    df = _linha_sintetica(V00900=90.0, V00901=10.0)
    r = calcular_indicadores(df, INDICADORES_IVS).iloc[0]
    assert r['pct_analfab'] == pytest.approx(0.10)       # 10/(90+10), não 10/90


def test_analfabetismo_exige_as_duas_parcelas():
    """Se V00901 está sigilosa (NaN), a taxa fica NaN — não vira zero."""
    df = _linha_sintetica(V00900=90.0)
    df['V00901'] = np.nan
    r = calcular_indicadores(df, INDICADORES_IVS).iloc[0]
    assert pd.isna(r['pct_analfab'])


def test_razao_de_moradores_reproduz_v0005():
    df = _linha_sintetica(V00001=100.0, V00002=10.0, V00005=300.0, V00006=30.0)
    r = calcular_indicadores(df, INDICADORES_IVS).iloc[0]
    assert r['razao_moradores'] == pytest.approx(330 / 110)


def test_indice_de_envelhecimento_e_razao_de_dependencia():
    """IEP = 60+ / menores de 15 × 100; RDI = 60+ / 15-59 × 100 (Galvão et al., 2025)."""
    df = _linha_sintetica(V01031=10.0, V01032=10.0, V01033=10.0,      # 30 menores de 15
                          V01034=100.0, V01039=100.0,                  # 200 de 15 a 59
                          V01040=40.0, V01041=20.0, v0001=290.0)       # 60 idosos (20 com 70+)
    r = calcular_indicadores(df).iloc[0]
    assert r['iep_setor'] == pytest.approx(200.0)                      # 60/30 × 100
    assert r['rdi_setor'] == pytest.approx(30.0)                       # 60/200 × 100
    assert r['prop_70mais_entre_60mais'] == pytest.approx(100 / 3)     # 20/60 × 100
    assert r['pct_pop_0a14'] == pytest.approx(30 / 290)


def test_indicadores_de_tipo_de_domicilio():
    df = _linha_sintetica(V00001=200.0, V00047=100.0, V00048=20.0, V00049=60.0, V00050=20.0)
    r = calcular_indicadores(df).iloc[0]
    assert r['pct_apartamento'] == pytest.approx(0.30)                 # 60/200
    assert r['pct_moradia_convencional'] == pytest.approx(0.90)        # (100+20+60)/200
    assert r['pct_moradia_nao_convencional'] == pytest.approx(0.10)    # 20/200


def test_toda_variavel_de_indicador_tem_arquivo_fonte():
    """Nenhum indicador pode depender de variável sem procedência declarada."""
    for ind in TODOS_INDICADORES:
        for var in (*ind.numerador, *ind.denominador):
            assert var in MAPA_VARIAVEL_ARQUIVO, f'{ind.nome} usa {var}, que não está em nenhum arquivo declarado'


def test_tabela_de_variaveis_esta_completa():
    """Demanda 2: toda variável precisa de descrição e de arquivo-fonte."""
    tabela = tabela_variaveis(ROOT / 'dados')
    assert len(tabela) > 60
    assert (tabela['descricao_oficial'] != '(sem descrição)').all(), \
        tabela.loc[tabela['descricao_oficial'] == '(sem descrição)', 'variavel'].tolist()
    assert tabela['arquivo_fonte'].notna().all()
    assert tabela['arquivo_fonte'].nunique() == len(ARQUIVOS_CENSO)    # os 8 arquivos do Censo
