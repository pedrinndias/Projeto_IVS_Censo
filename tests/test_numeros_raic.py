"""Os números digitados à mão nos geradores da RAIC batem com os dados?

Só leitura: os geradores (`gerar_apresentacao_oral_raic.py`, `gerar_relatorio_raic.py`) estão congelados
(o relatório e a apresentação já foram enviados) e não são tocados. Cada número é calculado dos CSVs,
formatado em pt-BR e procurado no texto do gerador.

Não cobertos (sem fonte de dados simples): 79,99 × 80,0 (IEP nacional), 14,9% (água), 52,1 milhões
(moradores do recorte), medianas de renda 2.313,87 e 6.092,84, médias 3,64 e 3,14, 99,98, e os
coeficientes da Tabela 1 e da Figura 1 (que vêm de `pecas.json`).
"""
import re
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
EDA = RAIZ / 'banco_de_dados' / 'eda'
ORAL, RELATORIO = 'gerar_apresentacao_oral_raic.py', 'gerar_relatorio_raic.py'
TEXTOS = {g: (RAIZ / 'scripts' / g).read_text(encoding='utf-8') for g in (ORAL, RELATORIO)}


def br(v, d=0) -> str:
    return f'{v:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def _csv(caminho, **kw) -> pd.DataFrame:
    return pd.read_csv(caminho, encoding='utf-8-sig', **kw)


def _casos() -> list:
    eleg = _csv(EDA / 'elegibilidade_setores.csv', sep=';').set_index('Dados_sig')['n_setores']
    rural = _csv(EDA / 'exclusao_rural_conferencia.csv', sep=';')
    n_urb, n_rur = int(rural['n_ok_urbano'].sum()), int(rural['n_ok_rural'].sum())
    renda = _csv(EDA / 'renda_outliers_rastreados.csv', sep=';').sort_values('renda_media_setor', ascending=False)
    rep = _csv(RAIZ / 'banco_de_dados' / 'nacional' / 'representatividade_elsi_no_brasil.csv', sep=';').set_index('metrica')
    t04 = _csv(RAIZ / 'analises_exploratorias' / '00_referencia' / 'tabelas' / 'T04_descritivas_regiao.csv')
    se = int(t04[(t04['regiao'] == 'Sudeste') & (t04['indicador'] == 'pct_agua_inad')]['n'].iloc[0])
    cobertura = _csv(RAIZ / 'relatorio_parcial_raic' / 'dados' / 'tabela1_descritivas.csv', dtype=str)
    n_analf = int(cobertura.set_index('indicador').loc['pct_analfab', 'n'].replace('.', ''))
    ambos = (ORAL, RELATORIO)
    return [
        ('setores nos 70 municípios', br(eleg.sum()), ambos),
        ('sem moradores', br(eleg['ZERADO']), ambos),
        ('com sigilo', br(eleg['SIGILOSO']), ambos),
        ('depois de tirar sem moradores e sigilo', br(eleg['OK']), ambos),
        ('rurais excluídos', br(n_rur), ambos),
        ('% rural excluído', br(100 * n_rur / (n_rur + n_urb), 2), ambos),
        ('setores urbanos do recorte', br(n_urb), ambos),
        ('renda do setor extremo', br(renda['renda_media_setor'].iloc[0], 2), ambos),
        ('maior renda restante', br(renda['renda_media_setor'].iloc[1], 2), (ORAL,)),
        ('razão do extremo para a mediana do município', br(renda['razao_mediana_mun'].iloc[0], 1), (ORAL,)),
        ('população do Brasil', br(rep.at['população (v0001)', 'Brasil']), ambos),
        ('setores do Brasil', br(rep.at['setores (todos)', 'Brasil']), ambos),
        ('população dos 70 municípios (milhões)', br(rep.at['população (v0001)', 'ELSI_70'] / 1e6, 1), (RELATORIO,)),
        ('% da população do país', br(rep.at['população (v0001)', 'pct_ELSI_sobre_Brasil'], 1), (RELATORIO,)),
        ('% dos setores urbanos elegíveis do país', br(rep.at['setores urbanos elegíveis', 'pct_ELSI_sobre_Brasil'], 1), (RELATORIO,)),
        ('setores do Sudeste', br(se), (RELATORIO,)),
        ('% do Sudeste no recorte', br(100 * se / n_urb, 1), (RELATORIO,)),
        ('cobertura do analfabetismo', br(100 * n_analf / n_urb, 2), (RELATORIO,)),
        ('% sem dado de analfabetismo', br(100 - 100 * n_analf / n_urb, 1), (RELATORIO,)),
    ]


try:
    CASOS = [(d, n, g) for d, n, gs in _casos() for g in gs]
except FileNotFoundError:     # sem os dados da entrega, os casos ficam vazios e o teste é pulado
    CASOS = []


@pytest.mark.parametrize('descricao, numero, gerador', CASOS, ids=[f'{g[7:14]}-{d}' for d, _, g in CASOS])
def test_numero_digitado_bate_com_os_dados(descricao, numero, gerador):
    assert re.search(r'(?<![\d.,])' + re.escape(numero) + r'(?!\d)', TEXTOS[gerador]), \
        f'{descricao}: os dados dão {numero}, que não está em {gerador}'
