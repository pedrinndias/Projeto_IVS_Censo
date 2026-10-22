"""Testes das análises transversais (scripts/eda_transversais.py)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
import eda_transversais as et  # noqa: E402


def test_bootstrap_sorteia_municipios_inteiros():
    """A unidade da reamostragem é o município: ele entra com todos os setores, repetido ou não."""
    d = pd.DataFrame({'NM_MUN': ['A'] * 3 + ['B'] * 5 + ['C'] * 7})
    pos = d.groupby('NM_MUN').indices
    rng = np.random.default_rng(0)
    for _ in range(50):
        n = d.iloc[et.sortear_municipios(pos, rng)]['NM_MUN'].value_counts()
        assert all(n.get(m, 0) % len(p) == 0 for m, p in pos.items())
        assert sum(n.get(m, 0) // len(p) for m, p in pos.items()) == len(pos)
