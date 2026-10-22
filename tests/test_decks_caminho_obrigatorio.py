"""Os scripts do relatório descritivo não adivinham o deck de trabalho: o caminho vem como argumento."""
import importlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))


@pytest.mark.parametrize('nome', ['comparar_edicoes_relatorio', 'anexar_versoes_ao_relatorio'])
def test_sem_argumento_pede_o_caminho(nome, monkeypatch):
    monkeypatch.setattr(sys, 'argv', [nome])
    with pytest.raises(SystemExit, match='uso'):
        importlib.import_module(nome).main()


@pytest.mark.skipif(not shutil.which('node'), reason='node ausente')
def test_gerador_js_sem_saida_recusa():
    r = subprocess.run(['node', str(RAIZ / 'scripts' / 'gerar_relatorio_descritivo.js')],
                       capture_output=True, text=True, cwd=RAIZ)
    assert r.returncode == 1 and 'uso' in r.stderr
