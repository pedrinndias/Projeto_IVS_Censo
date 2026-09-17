"""Testes do módulo `src/ivs_censo/fatorial.py`.

Duas famílias, com propósitos diferentes:

* **Conferência contra o que já foi calculado.** `test_acp_varimax_reproduz_csv` roda a
  extração sobre o banco da entrega e compara com
  `banco_de_dados/eda/fatorial/ivs7_spearman_cargas.csv`, gerado em 24/08/2026 a partir do
  CSV equivalente. É a trava que impede uma reimplementação silenciosamente diferente — e,
  de quebra, verifica que o `.db` e o `.csv` da entrega dizem a mesma coisa.
* **Propriedades algébricas das funções novas**, que não têm referência anterior para
  conferir: promax, eixo principal e escores por regressão são testados pelo que a
  matemática obriga a valer.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from ivs_censo.fatorial import (IVS7, ROTULOS, acp, bartlett,                    # noqa: E402
                                comunalidades_obliquas, escores_regressao,
                                fatoracao_eixo_principal, kmo, matriz_correlacao,
                                postos, rotacao_promax, smc, varimax)

BANCO = ROOT / 'banco_de_dados' / 'entrega_orientadora' / 'Base_ELSI_70Municipios_Censo2022.db'
CARGAS_REF = ROOT / 'banco_de_dados' / 'eda' / 'fatorial' / 'ivs7_spearman_cargas.csv'


def _matriz_fatorial(p: int = 6, k: int = 2, semente: int = 7):
    """Uma matriz de correlação gerada por um modelo fatorial exato de `k` fatores.

    R = AAᵀ + diag(unicidades), com as unicidades positivas por construção. Serve para
    testar recuperação: quem estimar bem tem de devolver as comunalidades de origem.
    """
    rng = np.random.default_rng(semente)
    A = np.zeros((p, k))
    for i in range(p):
        A[i, i % k] = rng.uniform(0.65, 0.85)        # carga alta no fator do bloco
        A[i, (i + 1) % k] = rng.uniform(-0.2, 0.2)   # carga cruzada pequena
    comun = (A ** 2).sum(axis=1)
    R = A @ A.T + np.diag(1 - comun)
    return R, A, comun


# ─────────────────────────────────────────────────────────────────────────────
# (a) conferência contra os CSVs de referência
# ─────────────────────────────────────────────────────────────────────────────
@pytest.mark.skipif(not BANCO.exists() or not CARGAS_REF.exists(),
                    reason='banco da entrega ou CSV de referência ausente')
def test_acp_varimax_reproduz_csv():
    """A extração sobre o `.db` reproduz `ivs7_spearman_cargas.csv` com tolerância 1e-6.

    O CSV de referência guarda três casas decimais; a comparação, portanto, é entre o
    valor calculado arredondado a três casas e o que está gravado. Diferença aqui
    significa erro de migração, não achado — pare antes de seguir.
    """
    con = sqlite3.connect(BANCO)
    try:
        df = pd.read_sql(
            f"select {', '.join(['urbano', 'Dados_sig'] + IVS7)} from setores_censitarios", con)
    finally:
        con.close()
    df = df[(df['urbano'].astype(str) == '1') & (df['Dados_sig'] == 'OK')].copy()
    df['renda_inv'] = -df['renda_media']
    colunas = [c if c != 'renda_media' else 'renda_inv' for c in IVS7]
    X = df[colunas].dropna()

    assert len(df) == 104_108, 'recorte urbano + Dados_sig OK mudou'
    assert len(X) == 87_545, 'casos completos nas 7 variáveis mudaram'

    R = X.corr(method='spearman').to_numpy()
    val, cargas = acp(R, 2)
    rot = varimax(cargas)
    comun = (cargas ** 2).sum(axis=1)
    kmo_global, msa = kmo(R)
    qui, gl, _ = bartlett(R, len(X))

    # os três números que o Notebook 04 usa como trava do bloco de adequabilidade
    assert round(kmo_global, 4) == 0.7826
    assert round(float(msa.min()), 4) == 0.6995
    assert round(qui, 4) == 235084.3838

    ref = pd.read_csv(CARGAS_REF, sep=';', index_col=0, encoding='utf-8-sig')
    calculado = pd.DataFrame(np.column_stack([cargas, rot, comun, msa]),
                             index=[ROTULOS.get(c, c) for c in colunas],
                             columns=list(ref.columns)).round(3)
    assert list(calculado.index) == list(ref.index)
    np.testing.assert_allclose(calculado.to_numpy(), ref.to_numpy(), atol=1e-6)


# ─────────────────────────────────────────────────────────────────────────────
# (b) promax
# ─────────────────────────────────────────────────────────────────────────────
def test_promax_em_fatores_ortogonais_devolve_correlacao_quase_zero():
    """Com fatores independentes por construção, a rotação oblíqua não deve inclinar nada.

    A matriz é bloco-diagonal: três variáveis correlacionadas entre si, três outras
    correlacionadas entre si, e nada entre os blocos. Se o promax inventasse correlação
    aqui, todo Φ estimado sobre os dados reais seria suspeito.
    """
    bloco = np.full((3, 3), 0.6)
    np.fill_diagonal(bloco, 1.0)
    R = np.block([[bloco, np.zeros((3, 3))], [np.zeros((3, 3)), bloco]])

    _, cargas = acp(R, 2)
    padrao, estrutura, phi = rotacao_promax(cargas)

    assert abs(phi[0, 1]) < 1e-6, f'Φ fora da diagonal deu {phi[0, 1]:.6f}'
    np.testing.assert_allclose(np.diag(phi), 1.0, atol=1e-12)
    np.testing.assert_allclose(estrutura, padrao @ phi, atol=1e-12)


def test_promax_preserva_comunalidade_e_expoe_phi():
    """Numa matriz com fatores de fato correlacionados, Φ sai do zero e a comunalidade fica.

    A comunalidade de uma solução oblíqua é diag(padrão·Φ·padrãoᵀ), não a soma dos
    quadrados das cargas — a diferença é a variância que os fatores compartilham. Este
    teste guarda a etapa de escala do promax, que é onde é fácil errar: sem ela, Φ deixa
    de ter diagonal unitária e a comunalidade vaza.
    """
    R, _, _ = _matriz_fatorial()
    _, cargas = acp(R, 2)
    comun_ortogonal = (varimax(cargas) ** 2).sum(axis=1)

    padrao, _, phi = rotacao_promax(cargas)
    np.testing.assert_allclose(np.diag(phi), 1.0, atol=1e-10)
    np.testing.assert_allclose(comunalidades_obliquas(padrao, phi), comun_ortogonal, atol=1e-8)


# ─────────────────────────────────────────────────────────────────────────────
# (c) escores por regressão
# ─────────────────────────────────────────────────────────────────────────────
def test_escores_por_regressao_tem_variancia_um():
    """Com cargas de ACP, os escores B = R⁻¹A saem padronizados — variância exatamente 1.

    Vale para a solução sem rotação e para a rotacionada por Varimax, porque uma rotação
    ortogonal não muda o subespaço. É a checagem mais barata de que R⁻¹A está sendo
    calculado na ordem certa.
    """
    rng = np.random.default_rng(3)
    F = rng.standard_normal((4000, 2))
    carga_verdadeira = np.array([[0.8, 0.1], [0.7, 0.2], [0.1, 0.8], [0.2, 0.7], [0.6, 0.3]])
    X = F @ carga_verdadeira.T + 0.5 * rng.standard_normal((4000, 5))

    R = matriz_correlacao(X, 'pearson')
    Z = (X - X.mean(axis=0)) / X.std(axis=0)
    _, cargas = acp(R, 2)

    for nome, A in (('sem rotação', cargas), ('varimax', varimax(cargas))):
        escores = Z @ escores_regressao(R, A)
        np.testing.assert_allclose(escores.var(axis=0), 1.0, atol=1e-8,
                                   err_msg=f'variância != 1 com cargas {nome}')


# ─────────────────────────────────────────────────────────────────────────────
# extensões restantes: eixo principal, SMC, postos
# ─────────────────────────────────────────────────────────────────────────────
def test_eixo_principal_recupera_as_comunalidades_do_modelo():
    """Sobre uma matriz gerada por um modelo fatorial exato, a iteração volta à origem."""
    R, _, comun = _matriz_fatorial()
    cargas, h, info = fatoracao_eixo_principal(R, 2)

    assert info['convergiu'], f"não convergiu em {info['iteracoes']} iterações"
    assert not info['heywood']
    np.testing.assert_allclose(h, comun, atol=1e-4)
    np.testing.assert_allclose((cargas ** 2).sum(axis=1), comun, atol=1e-4)


def test_eixo_principal_difere_da_acp_quando_a_comunalidade_e_baixa():
    """A advertência de Stevens (1992) tem de aparecer: com comunalidade baixa, divergem.

    A ACP põe 1 na diagonal e a AF põe a comunalidade; quanto mais longe de 1 estiver a
    comunalidade, maior a diferença. Se este teste passasse a falhar, seria sinal de que o
    eixo principal virou ACP disfarçada — e o bloco 4 do Notebook 04 perderia o sentido.
    """
    R, _, comun = _matriz_fatorial()
    _, cargas_acp = acp(R, 2)
    cargas_paf, _, _ = fatoracao_eixo_principal(R, 2)
    assert comun.min() < 0.8
    assert (cargas_acp ** 2).sum() > (cargas_paf ** 2).sum()


def test_smc_bate_com_o_r_quadrado_da_regressao():
    """SMC = 1 − 1/diag(R⁻¹) tem de dar o mesmo que regredir cada variável nas demais."""
    R, _, _ = _matriz_fatorial()
    p = R.shape[0]
    esperado = np.empty(p)
    for j in range(p):
        outras = [i for i in range(p) if i != j]
        beta = np.linalg.solve(R[np.ix_(outras, outras)], R[outras, j])
        esperado[j] = R[j, outras] @ beta
    np.testing.assert_allclose(smc(R), esperado, atol=1e-10)


def test_postos_com_empates_batem_com_o_pandas():
    """O Spearman do bootstrap passa por `postos`; empates são muitos nas proporções."""
    x = np.array([0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 2.0, 2.0])
    y = np.array([3.0, 1.0, 1.0, 1.0, 9.0, 9.0, 0.0, 5.0])
    X = np.column_stack([x, y])
    esperado = pd.DataFrame(X).rank(method='average').to_numpy()
    np.testing.assert_allclose(postos(X), esperado)
    np.testing.assert_allclose(matriz_correlacao(X, 'spearman'),
                               pd.DataFrame(X).corr(method='spearman').to_numpy(), atol=1e-12)
