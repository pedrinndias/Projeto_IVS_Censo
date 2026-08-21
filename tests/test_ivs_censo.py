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
from ivs_censo.indicadores import (INDICADORES_IVS, INDICADORES_POR_NOME,             # noqa: E402
                                   TODOS_INDICADORES)


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


# ─────────────────────────────────────────────────────────────────────────────
# Rastreamento dos extremos de renda (src/ivs_censo/renda.py)
# ─────────────────────────────────────────────────────────────────────────────
from ivs_censo.renda import (EXTREMO, NORMAL, SUSPEITO,                        # noqa: E402
                             limites_tukey, rastrear_outliers_renda)


def _cidade_sintetica(nome, rendas, favela=None, analfab=None, raca=None):
    """Um município com N setores, para conferir a regra na mão."""
    n = len(rendas)
    return pd.DataFrame({
        'CD_MUN': [nome] * n,
        'V06004': rendas,
        'CD_TIPO': favela if favela is not None else ['0'] * n,
        'pct_analfab': analfab if analfab is not None else [0.05] * n,
        'pct_raca_pretpardind': raca if raca is not None else [0.5] * n,
    })


def test_tukey_k3_e_mais_folgado_que_o_boxplot():
    """k=3 marca só o extremo; k=1.5 marcaria a cauda inteira."""
    s = pd.Series(list(range(100)))
    _, sup15 = limites_tukey(s, k=1.5)
    _, sup30 = limites_tukey(s, k=3.0)
    assert sup30 > sup15


def test_extremo_coerente_nao_vira_suspeito():
    """Renda alta num setor sem nenhum sinal contrário é EXTREMO, não erro de dado."""
    df = _cidade_sintetica('X', [1000.0] * 40 + [90000.0],
                           analfab=[0.20] * 40 + [0.01],      # o extremo é o MENOS analfabeto
                           raca=[0.80] * 40 + [0.10])         # e o de menor proporção PPI
    r = rastrear_outliers_renda(df)
    assert r['classe_renda'].iloc[-1] == EXTREMO
    assert not r['incoerente'].iloc[-1]


def test_favela_com_renda_altissima_vira_suspeito():
    """O caso de Belo Horizonte: extremo de renda num setor de favela é incoerente."""
    df = _cidade_sintetica('X', [1000.0] * 40 + [90000.0],
                           favela=['0'] * 40 + ['1'])
    r = rastrear_outliers_renda(df)
    assert r['classe_renda'].iloc[-1] == SUSPEITO
    assert 'e_favela' in r['motivos'].iloc[-1]


def test_criterio_e_por_municipio_e_nao_global():
    """O mesmo valor é normal na cidade rica e extremo na cidade pobre — o IVS é intraurbano."""
    rica = _cidade_sintetica('RICA', [8000.0 + i * 100 for i in range(40)] + [12000.0])
    pobre = _cidade_sintetica('POBRE', [1000.0 + i * 10 for i in range(40)] + [12000.0])
    r = rastrear_outliers_renda(pd.concat([rica, pobre], ignore_index=True))
    assert r['classe_renda'].iloc[40] == NORMAL      # 12 mil na cidade rica: dentro da faixa
    assert r['classe_renda'].iloc[-1] != NORMAL      # o mesmo 12 mil na cidade pobre: extremo


def test_municipio_pequeno_nao_e_rotulado():
    """Com menos de 20 setores o quartil do município não sustenta o corte."""
    df = _cidade_sintetica('MINI', [1000.0] * 5 + [90000.0])
    r = rastrear_outliers_renda(df)
    assert (r['classe_renda'] == NORMAL).all()
    assert r['renda_lim_sup_mun'].isna().all()


def test_setor_sem_renda_nao_e_outlier_de_renda():
    """Sigilo em V06004 não pode virar classificação."""
    df = _cidade_sintetica('X', [1000.0] * 40 + [np.nan])
    r = rastrear_outliers_renda(df)
    assert r['classe_renda'].iloc[-1] == NORMAL


def test_analfabetismo_exige_o_denominador_inteiro():
    """O caso inverso do teste acima: V00900 sigiloso e V00901 presente.

    Descoberto por teste de mutação em 21/08/2026. O teste anterior
    (`test_analfabetismo_exige_as_duas_parcelas`) passa mesmo com `min_count_den=1`,
    porque ali o NUMERADOR já é NaN. Só este caso protege o parâmetro: sem V00900 o
    denominador ficaria valendo V00901 sozinho, e a taxa sairia 100% de analfabetismo
    justamente nos setores em que o IBGE suprimiu a contagem de alfabetizados.
    """
    df = _linha_sintetica(V00901=10.0)
    df['V00900'] = np.nan
    r = calcular_indicadores(df, INDICADORES_IVS).iloc[0]
    assert pd.isna(r['pct_analfab']), 'sem V00900 a taxa não é calculável — não pode virar 1,0'


# ─────────────────────────────────────────────────────────────────────────────
# Canalização da água (V00199-V00201), acrescentada em 21/08/2026
# ─────────────────────────────────────────────────────────────────────────────
def test_complemento_inverte_a_proporcao():
    """`complemento=True` devolve 1 - num/den. É o que permite medir 'a água não chega
    dentro do domicílio' pela variável que o IBGE quase nunca sigila."""
    df = _linha_sintetica(V00001=100.0, V00199=85.0, V00200=10.0, V00201=5.0)
    r = calcular_indicadores(df, [INDICADORES_POR_NOME['pct_sem_agua_canalizada']]).iloc[0]
    assert r['pct_sem_agua_canalizada'] == pytest.approx(0.15)      # 1 - 85/100


def test_complemento_equivale_a_somar_as_duas_parcelas():
    """A trinca é partição de V00001, então o complemento de V00199 tem que dar
    exatamente (V00200+V00201)/V00001 — é essa identidade que justifica a troca."""
    df = _linha_sintetica(V00001=200.0, V00199=150.0, V00200=30.0, V00201=20.0)
    nomes = ['pct_sem_agua_canalizada', 'pct_agua_so_terreno', 'pct_agua_nao_encanada']
    r = calcular_indicadores(df, [INDICADORES_POR_NOME[n] for n in nomes]).iloc[0]
    assert r['pct_sem_agua_canalizada'] == pytest.approx(
        r['pct_agua_so_terreno'] + r['pct_agua_nao_encanada'])


def test_complemento_e_aplicado_antes_do_corte():
    """Se o clip [0,1] viesse antes, o complemento devolveria o valor invertido errado.
    Setor com V00199 > V00001 (inconsistência de dado) tem que cair em 0, não em 1."""
    df = _linha_sintetica(V00001=100.0, V00199=120.0)
    r = calcular_indicadores(df, [INDICADORES_POR_NOME['pct_sem_agua_canalizada']]).iloc[0]
    assert r['pct_sem_agua_canalizada'] == 0.0     # 1 - 1,2 = -0,2 -> cortado em 0


def test_canalizacao_tem_procedencia_declarada():
    """As três variáveis novas precisam estar no mapa de arquivos-fonte, senão a tabela
    de variáveis da orientadora sai com procedência em branco."""
    for var in ('V00199', 'V00200', 'V00201'):
        assert MAPA_VARIAVEL_ARQUIVO.get(var) == 'dom2'
