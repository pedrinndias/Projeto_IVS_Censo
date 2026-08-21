"""Código compartilhado do projeto IVS — Censo 2022.

Este pacote reúne o que antes vivia duplicado dentro dos notebooks: quais variáveis
vêm de qual arquivo do Censo, como cada indicador é calculado e como ler os CSVs do
IBGE. A pipeline de notebooks (`notebooks/Fase3_EDA_ELSI/`) continua sendo a
referência para o recorte ELSI; este pacote existe para que os mesmos cálculos possam
ser aplicados a outros recortes — em particular ao **Brasil inteiro** — sem copiar
código.

Uso típico (a partir de um script em `scripts/`):

    import sys
    sys.path.insert(0, str(ROOT / 'src'))
    from ivs_censo import ARQUIVOS_CENSO, calcular_indicadores, tabela_variaveis
"""
from .fontes import (
    ARQUIVOS_CENSO,
    MAPA_VARIAVEL_ARQUIVO,
    colunas_do_arquivo,
    encontrar_raiz,
)
from .indicadores import (
    INDICADORES_IVS,
    INDICADORES_COMPLEMENTARES,
    TODOS_INDICADORES,
    INDICADORES_POR_NOME,
    calcular_indicadores,
    classificar_dados_sig,
    safe_div,
)
from .dicionario import carregar_dicionario_oficial, tabela_variaveis

__all__ = [
    'ARQUIVOS_CENSO',
    'MAPA_VARIAVEL_ARQUIVO',
    'colunas_do_arquivo',
    'encontrar_raiz',
    'INDICADORES_IVS',
    'INDICADORES_COMPLEMENTARES',
    'TODOS_INDICADORES',
    'INDICADORES_POR_NOME',
    'calcular_indicadores',
    'classificar_dados_sig',
    'safe_div',
    'carregar_dicionario_oficial',
    'tabela_variaveis',
]
