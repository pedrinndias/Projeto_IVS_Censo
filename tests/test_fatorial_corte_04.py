"""Testes do corte de carga < 0,4 por rotação (scripts/fatorial_corte_04.py)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
import fatorial_corte_04 as fc  # noqa: E402
import fatorial_corte_04_sensibilidade as fs  # noqa: E402
import fatorial_multiversao as fm  # noqa: E402
from ivs_censo.fatorial import fatoracao_eixo_principal, rotacao_promax  # noqa: E402

CODIGOS = ['AGU', 'ESG', 'CAN', 'REN', 'PPI', 'ANA', 'LIX', 'MNC']


def base(n=3000, semente=3):
    """Dois fatores bem definidos e dois indicadores de ruído puro (LIX e MNC)."""
    rng = np.random.default_rng(semente)
    cargas = np.array([[.1, .8], [.2, .75], [.1, .8], [.8, .1], [.75, .2], [.8, .1], [0, 0], [0, 0]])
    X = rng.normal(size=(n, 2)) @ cargas.T + .5 * rng.normal(size=(n, len(CODIGOS)))
    return pd.DataFrame(X, columns=[fm.VARS[c] for c in CODIGOS])


def test_corte_tira_o_ruido_e_para_no_limiar():
    for rot in fc.ROTACOES[1:]:
        ficam, r, s, passos = fc.cortar(base(), CODIGOS, rot)
        assert set(ficam) == set(CODIGOS) - {'LIX', 'MNC'}
        p = pd.DataFrame(passos)
        assert p['retirado'].sum() == 2 and p.groupby('passo')['retirado'].sum().max() == 1  # um por vez
        ultimo = p[p['passo'] == p['passo'].max()]
        assert (ultimo['carga_max'] >= fc.CORTE).all()


def test_corte_refaz_a_fatorial_a_cada_passo():
    """A carga de quem fica é a da fatorial refeita sem o retirado, não a do primeiro passo."""
    _, _, _, passos = fc.cortar(base(), CODIGOS, 'promax')
    p = pd.DataFrame(passos)
    agu = p[p['codigo'] == 'AGU'].set_index('passo')['carga_max']
    assert len(agu) == 3 and agu.nunique() == 3


def test_corte_nao_desce_abaixo_do_minimo():
    d = pd.DataFrame(np.random.default_rng(0).normal(size=(500, 5)),
                     columns=[fm.VARS[c] for c in CODIGOS[:5]])
    ficam, _, _, _ = fc.cortar(d, CODIGOS[:5], 'varimax')
    assert len(ficam) == fc.MINIMO


def test_corte_guarda_os_alertas_da_fatorial():
    p = pd.DataFrame(fc.cortar(base(), CODIGOS, 'varimax')[3])
    assert not p['heywood'].any() and p['convergiu'].all()


def test_sensibilidade_repete_o_corte_e_a_promax_do_modulo():
    d = base()
    cols = [fm.VARS[c] for c in CODIGOS]
    R = fm.matriz(d, cols, 'global')
    L = fatoracao_eixo_principal(R, 2)[0]
    assert np.allclose(fs.promax_variante(L, 4, 'nenhuma'), rotacao_promax(L)[0])

    def matriz(lista):
        i = [CODIGOS.index(c) for c in lista]
        return R[np.ix_(i, i)]
    for rot in ('varimax', 'promax'):
        assert fs.cortar_R(matriz, CODIGOS, fs.VARIANTES[rot][1])[0] == fc.cortar(d, CODIGOS, rot)[0]
