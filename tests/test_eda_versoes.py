"""O motor das análises por versão reproduz, no 00_referencia, os números já publicados:
as descritivas da 2ª rodada (`eda/atualizada/`) e o n, o índice, as faixas e a AUC
municipal da referência proposta do NB05 (`eda/ivs_especificacoes/`), até a 4ª casa."""
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
import eda_versoes as ev  # noqa: E402

REF = RAIZ / 'analises_exploratorias' / '00_referencia'
EDA = RAIZ / 'banco_de_dados' / 'eda'


def test_faixas_alternativas_aguenta_ivs_ausente():
    """Município sem régua (IVS ausente) fica com a classe 'indefinida' em todas as regras por posto."""
    rng = np.random.default_rng(5)
    n = 60
    d = pd.DataFrame({'NM_MUN': np.repeat(['M1', 'M2', 'M3'], n // 3), 'x': rng.normal(size=n), 'y': rng.normal(size=n)})
    s = d[['NM_MUN']].copy()
    s['ivs'] = np.where(d['NM_MUN'] == 'M3', np.nan, rng.random(n))
    for regra in ('ivs_bh', 'quartis'):
        s[f'faixa_{regra}'] = ev.ie.faixas(s['ivs'], s['NM_MUN'], regra)
    tabelas = {}
    S = SimpleNamespace(tabela=lambda i, nome, bloco, chave, t, c: tabelas.update({i: t}), figura=lambda *a: None)
    ev.faixas_alternativas(SimpleNamespace(setores=s, d=d, col=['x', 'y']), S)
    t = tabelas['T36']
    indef = t[(t['classe'] == 'indefinida') & t['regra'].isin(['quintis', 'quebras naturais (4 classes)'])]
    assert indef['setores'].tolist() == [n // 3, n // 3]


@pytest.fixture(scope='module')
def base():
    cfg = ev.ler_config(REF)
    return cfg, ev.montar_base(cfg)


@pytest.fixture(scope='module')
def indice(base):
    cfg, b = base
    return ev.calcular_indice(b.df, cfg)


def test_recorte_e_indicadores(base):
    _, b = base
    assert len(b.df) == 104_108
    assert b.df['NM_MUN'].nunique() == 70
    assert len(b.inds) == 31


def test_descritivas_da_segunda_rodada(base):
    _, b = base
    pub = pd.read_csv(EDA / 'atualizada' / 'descritivas_globais.csv', sep=';', encoding='utf-8-sig', index_col=0)
    # a 2ª rodada publica a renda sem o extremo de BH com o rótulo `renda_media`
    # (eda/atualizada/README.md); os valores saem arredondados na 4ª casa
    nome = {'renda_media': 'renda_media_sem_extremo'}
    comuns = list(pub.index)
    assert len(comuns) == 7
    novo = ev.tab_desc(b.df, [nome.get(c, c) for c in comuns])
    for col in ['n', 'media', 'dp', 'min', 'p25', 'mediana', 'p75', 'max', 'assim', 'curt']:
        np.testing.assert_allclose(novo[col].to_numpy(float), pub.loc[comuns, col].to_numpy(float),
                                   atol=5.1e-5, rtol=0, err_msg=col)


def test_indice_da_referencia(indice):
    pub = pd.read_csv(EDA / 'ivs_especificacoes' / 'ivs_referencia_por_setor.csv', dtype={'CD_SETOR': str})
    s = indice.setores
    assert len(s) == len(pub) == 73_878
    m = s.merge(pub, on='CD_SETOR', how='inner', validate='one_to_one')
    assert len(m) == len(pub)
    assert np.abs(m['ivs'] - m['ivs_referencia']).max() < 1e-4
    assert (m['faixa_ivs_bh_x'].map(ev.rotulo_faixa) == m['faixa_ivs_bh_y']).mean() > 0.9999


def test_auc_e_elegibilidade_da_referencia(indice):
    ref = pd.read_csv(EDA / 'ivs_especificacoes' / 'referencia.csv')
    ref = ref[ref['leitura'] == 'principal'].iloc[0]
    assert ref['id'] == 'original·lixo_sem·banheiro_graduado·promax·60_40·municipal'
    assert round(indice.auc_mun[0], 4) == round(float(ref['valor_b']), 4)
    assert indice.eleg['elegivel']
    assert round(100 * indice.rep.max(), 4) == 60.0


def test_formatacao_ptbr():
    assert ev.br(73878, 0) == '73.878'
    assert ev.br(0.81864, 4) == '0,8186'
    assert ev.pctbr(15.94) == '15,9%'
    assert ev.br(np.nan) == '—'


def test_gini_e_theil():
    assert ev.gini(np.ones(10)) == pytest.approx(0)
    assert ev.theil(np.ones(10)) == pytest.approx(0)
    x = np.r_[np.zeros(9), 1.0]
    assert ev.gini(x) == pytest.approx(0.9)
    assert ev.theil(x) == pytest.approx(np.log(10))


def test_media_geometrica_trata_componente_constante_como_zero():
    """Componente constante no município entra como 0 (sem carência), como na soma."""
    d = pd.DataFrame({'NM_MUN': ['A'] * 3, 'x': [0.0, 0.5, 1.0], 'y': [0.3, 0.3, 0.3]})
    w = np.array([0.5, 0.5])
    v = ev.indice_versao(d, ['x', 'y'], w, 'municipal', 'geometrica')
    esperado = np.exp(0.5 * np.log(np.array([0.0, 0.5, 1.0]) + ev.DESLOCAMENTO) + 0.5 * np.log(ev.DESLOCAMENTO))
    np.testing.assert_allclose(v, esperado)
    soma = ev.indice_versao(d, ['x', 'y'], w, 'municipal', 'soma')
    np.testing.assert_allclose(soma, [0.0, 0.25, 0.5])


def test_ler_setores_tira_a_uf_do_nome_do_municipio(tmp_path):
    import eda_transversais as et
    arq = tmp_path / 's.csv'
    pd.DataFrame({'CD_SETOR': ['1', '2'], 'NM_MUN': ['Belo Horizonte/MG', 'Contagem']}).to_csv(arq, index=False)
    assert et.ler_setores(arq)['NM_MUN'].tolist() == ['Belo Horizonte', 'Contagem']
