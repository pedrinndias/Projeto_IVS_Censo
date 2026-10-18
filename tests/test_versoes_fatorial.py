"""O enumerador das 108 versões da análise fatorial (scripts/versoes_fatorial.py)."""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
sys.path.insert(0, str(RAIZ / 'src'))

import versoes_fatorial as vf  # noqa: E402


def test_108_versoes_unicas_e_sem_as_duas_aguas():
    v = vf.versoes()
    assert len(v) == 108
    assert len({x['id'] for x in v}) == 108
    assert len({tuple(x['colunas']) + (x['renda'],) for x in v}) == 108
    for x in v:
        assert not {'pct_agua_nao_encanada', 'pct_sem_agua_canalizada'} <= set(x['colunas'])
        assert 6 <= len(x['colunas']) <= 10


def test_ids_batem_com_a_lista_versoes_md():
    md = (RAIZ / 'versoes_fatorial' / 'VERSOES.md').read_text(encoding='utf-8')
    linhas = {m.group(1): m.group(0) for m in re.finditer(r'^\| (V\d{3}) \|.*$', md, re.M)}
    rot = {e: dict(n) for e, n in vf.EIXOS.items()}
    for x in vf.versoes():
        celulas = [c.strip() for c in linhas[x['id']].strip('|').split('|')]
        assert celulas[1:6] == [rot['renda'][x['renda']], rot['lixo'][x['lixo']], rot['agua'][x['agua']],
                                rot['banheiro'][x['banheiro']], rot['moradia'][x['moradia']]]
        assert int(celulas[6]) == len(x['colunas'])


def test_referencia_proposta_e_a_v023():
    v = {x['id']: x for x in vf.versoes()}['V023']
    assert (v['renda'], v['lixo'], v['agua'], v['banheiro'], v['moradia']) == \
        ('original', 'sem', 'nenhuma', 'graduado', 'nao')
    assert vf.id_nb05(v) == 'original·lixo_sem·banheiro_graduado·promax·60_40·municipal'
