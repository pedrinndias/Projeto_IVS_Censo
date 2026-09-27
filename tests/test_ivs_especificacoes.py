"""Testes do motor de especificações do IVS (scripts/ivs_especificacoes.py)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
import ivs_especificacoes as ie  # noqa: E402


def _dados(n=400, semente=1):
    """Seis variáveis de dois fatores latentes, em dois municípios."""
    rng = np.random.default_rng(semente)
    f = rng.normal(size=(n, 2))
    cargas = np.array([[.8, .1], [.7, .2], [.1, .8], [.2, .7], [.75, .1], [.1, .75]])
    colunas = ['a', 'b', 'c', 'renda_inv', 'e', 'g']
    d = pd.DataFrame(f @ cargas.T + 0.5 * rng.normal(size=(n, 6)), columns=colunas)
    d['NM_MUN'] = np.where(np.arange(n) % 2 == 0, 'M1', 'M2')
    return d, colunas


def test_pesos_somam_1():
    d, colunas = _dados()
    r = ie.rodar_cenario(d[colunas].to_numpy(), com_horn=False)
    reps = ie.reparticoes(r, colunas)
    assert len(reps) == 9          # 1 sem rotação + 3 Varimax + 5 promax
    for M, rep in reps.values():
        assert rep.sum() == pytest.approx(1)
        assert ie.fa.pesos_indice(M, rep).sum() == pytest.approx(1)
    # 60/40: o 0,6 vai para a dimensão da renda
    M, rep = reps[('varimax', '60_40')]
    assert ie.peso_f1(M, rep, colunas) == pytest.approx(60)


def test_indice_entre_0_e_1():
    d, colunas = _dados()
    peso = np.full(len(colunas), 1 / len(colunas))
    for norm in ('global', 'municipal'):
        v = ie.indice(d, colunas, peso, norm)
        assert not np.isnan(v).any()
        assert v.min() >= 0 and v.max() <= 1 + 1e-12


def test_indice_municipal_usa_min_max_de_cada_municipio():
    d, colunas = _dados()
    d.loc[d['NM_MUN'] == 'M2', colunas] += 10          # desloca um município inteiro
    peso = np.full(len(colunas), 1 / len(colunas))
    v = ie.indice(d, colunas, peso, 'municipal')
    for _, g in d.groupby('NM_MUN'):
        assert v[g.index].min() >= 0 and v[g.index].max() <= 1 + 1e-12
        assert v[g.index].max() > 0.5


def test_faixas_quatro_classes():
    rng = np.random.default_rng(2)
    v = rng.lognormal(size=2000)
    mun = np.repeat(['M1', 'M2'], 1000)
    for regra in ('ivs_bh', 'quartis'):
        assert set(ie.faixas(v, mun, regra)) == {0, 1, 2, 3}


def test_auc_grupos_bate_com_auc_postos():
    rng = np.random.default_rng(3)
    e = rng.normal(size=600)
    y = (rng.random(600) < 0.3).astype(float)
    g = np.repeat([0, 1, 2], 200)
    t = ie.auc_grupos(e, y, g)
    for k in range(3):
        assert t.loc[k, 'auc'] == pytest.approx(ie.fa.auc_postos(e[g == k], y[g == k]))


def test_logistica_recupera_coeficientes():
    rng = np.random.default_rng(4)
    x = rng.normal(size=(20000, 1))
    y = (rng.random(20000) < 1 / (1 + np.exp(-(-1 + 2 * x[:, 0])))).astype(float)
    b, ep, dev, _ = ie.logistica(x, y)
    assert b == pytest.approx([-1, 2], abs=0.1)
    assert (ep > 0).all() and dev > 0


def test_banheiro_graduado():
    df = pd.DataFrame({'V00001': [10, 10, 10, 0], 'V00236': [0, 10, 0, 0],
                       'V00237': [0, 0, 5, 0], 'V00238': [0, 0, 5, 0]})
    g = ie.banheiro_graduado(df)
    assert g.iloc[:3].tolist() == pytest.approx([0, 1 / 3, 25 / 30])
    assert np.isnan(g.iloc[3])


@pytest.mark.skipif(not ie.fa.DB.exists(), reason='base da entrega ausente')
def test_trava_nb04():
    """IVS-6 sem lixo, renda original, Varimax SS, normalização global = o índice do NB04."""
    assert ie.trava(ie.carregar_base()) == ie.TRAVA
