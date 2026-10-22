"""Testes do motor da fatorial multiversão (scripts/fatorial_multiversao.py)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
import fatorial_multiversao as fm  # noqa: E402


def test_contagens_das_camadas():
    assert len(fm.subconjuntos()) == 4017
    c = fm.conjuntos()
    assert len(c) == 13 and c['nucleo'] == fm.NUCLEO and len(c['nucleo+IDO']) == 8


def test_tucker():
    A = np.array([[.8, .1], [.7, .2], [.1, .9]])
    assert np.allclose(fm.congruencia_tucker(A, A), 1)
    assert np.allclose(fm.congruencia_tucker(A, -A), -1)


def test_replicacao_usa_a_rotacao_do_finalista():
    """Sem rotação há um fator só: o Tucker mede esse fator (o F2 fica ausente), não o promax de dois."""
    rng = np.random.default_rng(1)
    n = 2000
    cargas = np.array([[.8, .1], [.7, .2], [.1, .8], [.2, .7], [.75, .1], [.1, .75], [.7, .3]])
    cols = [fm.VARS[c] for c in fm.NUCLEO]
    d = pd.DataFrame(rng.normal(size=(n, 2)) @ cargas.T + .5 * rng.normal(size=(n, 7)), columns=cols)
    d['NM_MUN'] = np.tile(['A', 'B', 'C', 'D'], n // 4)
    metade = {'A': 0, 'B': 1, 'C': 0, 'D': 1}
    f = {'normalizacao': 'municipal', 'rotacao': 'promax', 'metodo': '60_40'}
    assert len(fm.tucker_metades(d, cols, f, metade)) == 2
    assert len(fm.tucker_metades(d, cols, {**f, 'rotacao': 'sem_rotacao', 'metodo': 'unico'}, metade)) == 1
    assert len(fm.tucker_metades(d, cols, {**f, 'rotacao': 'varimax', 'metodo': 'ss'}, metade)) == 2


def test_sinais_invertem_carga_negativa():
    M = np.array([[.8, .1], [-.7, .2], [.1, -.9]])
    assert list(fm.sinais(M)) == [1, -1, -1]


def test_sigilo_piso_e_zero():
    d = pd.DataFrame({'pct_analfab': [0.1, np.nan], 'V00900': [50, 99]})
    assert fm.com_sigilo(d, 'piso')['pct_analfab'].tolist() == [0.1, 0.01]
    assert fm.com_sigilo(d, 'zero')['pct_analfab'].tolist() == [0.1, 0.0]
    assert np.isnan(fm.com_sigilo(d, 'ausente')['pct_analfab'][1])


def test_postos_municipal_sem_variacao_fica_ausente():
    d = pd.DataFrame({'a': [1., 2., 3., 5.], 'b': [3., 1., 2., 5.], 'NM_MUN': ['M', 'M', 'M', 'U']})
    v = fm.indice_norm(d, ['a', 'b'], np.array([.5, .5]), np.array([1, 1]), 'postos_municipal')
    assert np.isnan(v[3]) and np.all((v[:3] > 0) & (v[:3] <= 1))


