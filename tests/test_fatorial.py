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

from ivs_censo.fatorial import (IVS7, ROTULOS, _sinal_positivo, acp, alinhar_cargas,  # noqa: E402
                                bartlett, bootstrap_cargas, chi2_sf,
                                comunalidades_obliquas, escores_regressao,
                                fatoracao_eixo_principal, horn, kmo, matriz_correlacao,
                                postos, reparticao, rodar_cenario,
                                rotacao_promax, smc, varimax)

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
    qui, gl, pval = bartlett(R, len(X))

    # os três números que o Notebook 04 usa como trava do bloco de adequabilidade
    assert round(kmo_global, 4) == 0.7826
    assert round(float(msa.min()), 4) == 0.6995
    assert round(qui, 4) == 235084.3838
    # FAT-07: só o qui-quadrado estava travado; gl e p-valor também mudam se a fórmula mudar.
    assert gl == 21                             # p(p-1)/2 com p=7, não p(p+1)/2
    assert pval < 1e-10                          # com 87 mil casos, rejeita H0 por construção

    ref = pd.read_csv(CARGAS_REF, sep=';', index_col=0, encoding='utf-8-sig')
    calculado = pd.DataFrame(np.column_stack([cargas, rot, comun, msa]),
                             index=[ROTULOS.get(c, c) for c in colunas],
                             columns=list(ref.columns)).round(3)
    assert list(calculado.index) == list(ref.index)
    # HIG-05: numpy>=1.26 pode devolver o sinal cru de `eigh` trocado (documentado em
    # `acp`); normaliza pela mesma convenção do resto do projeto (soma da coluna > 0 →
    # sinal +1, como em `rodar_cenario`/`_sinal_positivo`) em vez de exigir uma versão
    # mínima de numpy testada.
    calc_arr = calculado.to_numpy() * _sinal_positivo(calculado.to_numpy())
    ref_arr = ref.to_numpy() * _sinal_positivo(ref.to_numpy())
    np.testing.assert_allclose(calc_arr, ref_arr, atol=1e-6)


def test_varimax_atinge_o_otimo_da_rotacao_2d():
    """O critério de parada (razão entre somas de valores singulares) pode parar cedo.

    Conferência independente: numa matriz real (IVS-6), o ângulo que o Varimax escolhe
    tem de bater com o ótimo achado por busca em grade + seção áurea no próprio ângulo
    de rotação — sem usar o algoritmo de Kaiser. Referência medida: critério do Varimax
    0,19070539 contra ótimo 0,19070564.
    """
    con = sqlite3.connect(BANCO)
    try:
        df = pd.read_sql(
            f"select {', '.join(['urbano', 'Dados_sig'] + IVS7)} from setores_censitarios", con)
    finally:
        con.close()
    df = df[(df['urbano'].astype(str) == '1') & (df['Dados_sig'] == 'OK')].copy()
    df['renda_inv'] = -df['renda_media']
    colunas6 = [c if c != 'renda_media' else 'renda_inv' for c in IVS7 if c != 'pct_lixo_inad']
    X = df[colunas6].dropna()

    R = X.corr(method='spearman').to_numpy()
    _, cargas = acp(R, 2)
    L = varimax(cargas)

    def crit(mat):
        return np.sum(np.var(mat ** 2, axis=0))

    def crit_theta(theta):
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        return crit(cargas @ rot)

    grade = np.linspace(0, np.pi / 2, 20_001)
    i = int(np.argmax([crit_theta(t) for t in grade]))
    a, b = grade[max(i - 1, 0)], grade[min(i + 1, len(grade) - 1)]

    razao = (np.sqrt(5) - 1) / 2                                      # seção áurea, maximização
    c, d = b - razao * (b - a), a + razao * (b - a)
    while abs(b - a) > 1e-12:
        if crit_theta(c) > crit_theta(d):
            b = d
        else:
            a = c
        c, d = b - razao * (b - a), a + razao * (b - a)
    crit_otimo = crit_theta((a + b) / 2)

    assert abs(crit(L) - crit_otimo) < 1e-9, (
        f'varimax não achou o ótimo: {crit(L):.8f} vs {crit_otimo:.8f}')


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


@pytest.mark.skipif(not BANCO.exists(), reason='banco da entrega ausente')
def test_promax_ivs6_bate_com_referencia_do_nb04():
    """FAT-07: trava Φ e a repartição do promax sobre o IVS-6 real (linha de base do NB04).

    Mesma consulta de `test_varimax_atinge_o_otimo_da_rotacao_2d` (IVS7 menos
    `pct_lixo_inad`). Φ[0,1] não depende da ordem dos fatores que `acp`/`varimax`
    devolvem; a repartição (65,82/34,18 no padrão e 59,64/40,36 na estrutura) também
    não, por usar `max`. Mata "promax com kappa=2", "alvo sem o sinal" e "estrutura =
    padrão" — mutações que passariam pelos testes de propriedade acima, que não têm
    referência numérica externa.
    """
    con = sqlite3.connect(BANCO)
    try:
        df = pd.read_sql(
            f"select {', '.join(['urbano', 'Dados_sig'] + IVS7)} from setores_censitarios", con)
    finally:
        con.close()
    df = df[(df['urbano'].astype(str) == '1') & (df['Dados_sig'] == 'OK')].copy()
    df['renda_inv'] = -df['renda_media']
    colunas6 = [c if c != 'renda_media' else 'renda_inv' for c in IVS7 if c != 'pct_lixo_inad']
    X = df[colunas6].dropna()

    R = X.corr(method='spearman').to_numpy()
    _, cargas = acp(R, 2)
    padrao, estrutura, phi = rotacao_promax(cargas)

    assert round(abs(phi[0, 1]), 4) == 0.5215
    assert round(max(reparticao(padrao)), 4) == 0.6582
    assert round(max(reparticao(estrutura)), 4) == 0.5964


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


def test_escores_com_phi_em_solucao_obliqua_tem_variancia_um_e_correlacao_igual_a_phi():
    """FAT-04: sem `phi`, a matriz padrão é usada como se fosse a de estrutura e erra.

    Com `phi` (B = R⁻¹·padrão·Φ), a covariância teórica dos escores B'RB fecha
    exatamente em Φ — diagonal 1 (padronizados), fora da diagonal igual à correlação
    entre fatores que o promax estimou.
    """
    R, _, _ = _matriz_fatorial()
    _, cargas = acp(R, 2)
    padrao, _, phi = rotacao_promax(cargas)

    B = escores_regressao(R, padrao, phi)
    cov_escores = B.T @ R @ B
    np.testing.assert_allclose(cov_escores, phi, atol=1e-8)
    np.testing.assert_allclose(np.diag(cov_escores), 1.0, atol=1e-8)


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


def test_eixo_principal_com_heywood_reescala_as_cargas_para_bater_com_h():
    """FAT-06: com Heywood, as cargas cruas tinham soma dos quadrados > h (já cortado).

    A matriz do achado (R muito colinear, k=1) força comunalidade estimada >= 1. Depois
    da correção, a soma dos quadrados de `cargas` bate com `h`, e `info['heywood']`
    continua `True` — reporta o caso, não esconde.
    """
    R = np.array([[1, .8, .7], [.8, 1, .5], [.7, .5, 1]])
    cargas, h, info = fatoracao_eixo_principal(R, 1)

    assert info['heywood'] is True
    np.testing.assert_allclose((cargas ** 2).sum(axis=1), h, atol=1e-10)


def test_acp_superestima_a_comunalidade_que_o_eixo_principal_acerta():
    """A advertência de Stevens (1992), em forma verificável.

    Sobre uma matriz gerada por um modelo fatorial exato, a comunalidade verdadeira é
    conhecida. O eixo principal a recupera; a ACP a **superestima**, variável por variável,
    porque põe 1 na diagonal e conta também a variância específica. A comparação é por
    variável, e não pela soma: comparar somas passaria mesmo se o eixo principal virasse
    uma ACP multiplicada por uma constante, que é justamente a regressão que este teste
    tem de pegar.
    """
    R, _, comun = _matriz_fatorial()
    _, cargas_acp = acp(R, 2)
    cargas_paf, h_paf, _ = fatoracao_eixo_principal(R, 2)
    comun_acp = (cargas_acp ** 2).sum(axis=1)

    np.testing.assert_allclose(h_paf, comun, atol=1e-4)
    assert (comun_acp > comun + 0.05).all(), (
        f'a ACP deveria superestimar todas as comunalidades; folga mínima '
        f'{(comun_acp - comun).min():.4f}')
    # e a superestimação é maior onde a variável compartilha menos com as demais
    ordem_smc = np.argsort(smc(R))
    excesso = comun_acp - comun
    assert excesso[ordem_smc[0]] > excesso[ordem_smc[-1]]


def test_postos_recusa_valor_ausente():
    """NaN não tem posto, e ordená-lo como o maior valor daria uma correlação plausível.

    É o pior defeito possível neste módulo: nada falha, e o número sai errado. A guarda
    existe porque `postos` é público e o resto do projeto tolera faltante.
    """
    X = np.array([[1.0, 2.0], [np.nan, 3.0], [3.0, 4.0]])
    with pytest.raises(ValueError, match='ausentes'):
        postos(X)
    with pytest.raises(ValueError, match='ausentes'):
        matriz_correlacao(X, 'spearman')


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


def test_rodar_cenario_orienta_sinais_e_fecha_as_contas():
    # Duas dimensões latentes, três variáveis cada; uma coluna entra com o sinal trocado
    # para que o autovetor possa sair em qualquer sentido.
    rng = np.random.default_rng(7)
    f = rng.standard_normal((3000, 2))
    X = np.column_stack([f[:, 0] + 0.6 * rng.standard_normal(3000) for _ in range(3)]
                        + [f[:, 1] + 0.6 * rng.standard_normal(3000) for _ in range(3)])
    r = rodar_cenario(-X, k=2)
    for chave in ('sem_rotacao', 'varimax', 'promax_padrao'):
        assert (r[chave].sum(axis=0) > 0).all(), chave
    np.testing.assert_allclose(r['promax_estrutura'], r['promax_padrao'] @ r['phi'], atol=1e-12)
    np.testing.assert_allclose(np.diag(r['phi']), 1.0, atol=1e-12)
    for rep in r['pesos'].values():
        assert rep.sum() == pytest.approx(1.0)
    R = matriz_correlacao(-X)
    assert r['kmo'] == pytest.approx(kmo(R)[0])
    assert r['kaiser'] == int((np.linalg.eigvalsh(R) > 1).sum()) == 2
    assert r['horn_retidos'] == 2
    # Varimax e sem rotação têm a mesma comunalidade: a rotação ortogonal não a muda.
    np.testing.assert_allclose((r['varimax'] ** 2).sum(axis=1), r['comunalidade'], atol=1e-10)
    np.testing.assert_allclose(r['pesos']['varimax'], reparticao(r['varimax']))
    assert rodar_cenario(X, com_horn=False)['horn_retidos'] is None


# ─────────────────────────────────────────────────────────────────────────────
# FAT-07: Horn com semente fixa, alinhamento e percentis do bootstrap
# ─────────────────────────────────────────────────────────────────────────────
def test_horn_com_semente_fixa_bate_com_array_travado():
    """`horn(100, 5, sims=10, semente=99)` trava byte a byte — array gravado à parte.

    Mata "semente trocada" (mudaria o array inteiro) e "Horn devolvendo zeros" (um
    array de zeros nunca bateria com este, que é estritamente decrescente e positivo).
    """
    esperado = np.array([1.29379674, 1.1380489, 0.98994011, 0.8613523, 0.71686195])
    np.testing.assert_allclose(horn(100, 5, sims=10, semente=99), esperado, atol=1e-8)


def test_alinhar_cargas_desfaz_sinal_e_ordem():
    """`alinhar_cargas` tem de devolver a referência mesmo com colunas trocadas e sinal invertido.

    É o que o bootstrap depende para não confundir instabilidade real com o LAPACK
    tendo devolvido os fatores em outra ordem. Mata "sem inverter sinal".
    """
    _, referencia, _ = _matriz_fatorial()
    embaralhada = referencia[:, ::-1].copy()   # troca a ordem das duas colunas
    embaralhada[:, 0] = -embaralhada[:, 0]     # e inverte o sinal de uma delas

    alinhada = alinhar_cargas(embaralhada, referencia)
    np.testing.assert_allclose(alinhada, referencia, atol=1e-10)


def test_bootstrap_cargas_percentis_sao_2_5_97_5():
    """Os percentis do IC do bootstrap são 2,5/97,5, não 5/95 — e batem com o cálculo à parte.

    `cargas_ic` e `np.percentile(cargas_reamostragens, [2.5, 97.5], ...)` usam a mesma
    matriz de reamostragens devolvida: têm de bater exatamente, não só por tolerância.
    """
    rng = np.random.default_rng(3)
    F = rng.standard_normal((500, 2))
    carga_verdadeira = np.array([[0.8, 0.1], [0.7, 0.2], [0.1, 0.8], [0.2, 0.7], [0.6, 0.3]])
    X = F @ carga_verdadeira.T + 0.5 * rng.standard_normal((500, 5))

    resultado = bootstrap_cargas(X, 2, n_rep=20, seed=1, metodo='pearson')
    lo_esperado = np.percentile(resultado['cargas_reamostragens'], 2.5, axis=0)
    hi_esperado = np.percentile(resultado['cargas_reamostragens'], 97.5, axis=0)
    np.testing.assert_allclose(resultado['cargas_ic'][0], lo_esperado)
    np.testing.assert_allclose(resultado['cargas_ic'][1], hi_esperado)


# ─────────────────────────────────────────────────────────────────────────────
# L3: renda x cor/raça — par a par diverge do listwise (D4)
# ─────────────────────────────────────────────────────────────────────────────
@pytest.mark.skipif(not BANCO.exists(), reason='banco da entrega ausente')
def test_renda_x_cor_raca_par_a_par_diverge_do_listwise():
    """D4/L3: a correlação renda x cor/raça muda de conclusão conforme a procedência.

    Par a par (só as duas variáveis sem faltante) dá 0,8106 sobre 104.094 setores;
    dentro do recorte listwise das 7 variáveis do IVS7 (87.545 casos, o que a
    fatorial de fato decompõe) dá 0,7845 — abaixo do limiar de multicolinearidade
    0,80 usado no projeto. Sem este teste, nada trava que a escolha de procedência
    muda a conclusão.
    """
    con = sqlite3.connect(BANCO)
    try:
        df = pd.read_sql(
            f"select {', '.join(['urbano', 'Dados_sig'] + IVS7)} from setores_censitarios", con)
    finally:
        con.close()
    df = df[(pd.to_numeric(df['urbano'], errors='coerce') == 1)
           & (df['Dados_sig'] == 'OK')].copy()
    df['renda_inv'] = -df['renda_media']

    par = df[['renda_inv', 'pct_raca_pretpardind']].dropna()
    r_par = par.corr(method='spearman').loc['renda_inv', 'pct_raca_pretpardind']

    colunas7 = [c if c != 'renda_media' else 'renda_inv' for c in IVS7]
    listwise = df[colunas7].dropna()
    r_listwise = listwise.corr(method='spearman').loc['renda_inv', 'pct_raca_pretpardind']

    assert len(par) == 104_094
    assert len(listwise) == 87_545
    assert round(r_par, 4) == 0.8106
    assert round(r_listwise, 4) == 0.7845
    assert abs(r_par - r_listwise) > 0.02, 'procedência não muda a conclusão de multicolinearidade'


# ─────────────────────────────────────────────────────────────────────────────
# FAT-12: chi2_sf na cauda
# ─────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize('gl, x, esperado', [
    (21, 105, 3.73e-13),   # conferido com scipy.stats.chi2.sf fora do repo
    (15, 75, 5.66e-10),
    (1, 30, 4.3e-8),
])
def test_chi2_sf_bate_com_valor_tabelado_na_cauda(gl, x, esperado):
    """FAT-12: Wilson–Hilferty errava por ordens de grandeza nesta região da cauda.

    Com os graus de liberdade pequenos do projeto (Bartlett usa gl = p(p-1)/2), a
    aproximação normal antiga não bate — a gama incompleta regularizada bate.
    """
    assert chi2_sf(x, gl) == pytest.approx(esperado, rel=1e-2)
