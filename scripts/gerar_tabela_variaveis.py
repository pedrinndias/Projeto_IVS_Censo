"""Gera a tabela de variáveis do projeto com descrição oficial do IBGE e arquivo-fonte.

Demanda da orientadora (jul/2026): *"ajustar tabela para mostrar o que significa cada
variável e a fonte da planilha do censo"*.

Saídas (em `banco_de_dados/entrega_orientadora/`):
  - `Dicionario_Variaveis_Projeto.csv`
  - `Dicionario_Variaveis_Projeto.xlsx`  (uma aba por arquivo do Censo + aba consolidada)

Uso:
    python scripts/gerar_tabela_variaveis.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))  # torna o pacote importável sem instalar

from ivs_censo import ARQUIVOS_CENSO, encontrar_raiz, tabela_variaveis  # noqa: E402
from ivs_censo.indicadores import TODOS_INDICADORES                      # noqa: E402


def main() -> None:
    raiz = encontrar_raiz(Path(__file__).resolve().parent)
    destino = raiz / 'banco_de_dados' / 'entrega_orientadora'
    destino.mkdir(parents=True, exist_ok=True)

    tabela = tabela_variaveis(raiz / 'dados')
    print(f'Tabela de variáveis: {len(tabela)} linhas, {tabela["arquivo_fonte"].nunique()} arquivos do Censo')
    print(tabela.groupby(['bloco_do_projeto', 'arquivo_fonte']).size().rename('n_variaveis').to_string())

    sem_descricao = tabela[tabela['descricao_oficial'] == '(sem descrição)']
    if len(sem_descricao):
        print(f'\n[ALERTA] {len(sem_descricao)} variáveis sem descrição: {sem_descricao["variavel"].tolist()}')
    else:
        print('\n[OK] Todas as variáveis têm descrição.')
    print(f'[INFO] Descrições vindas do dicionário oficial do IBGE: '
          f'{int((tabela["origem_da_descricao"] == "Dicionário oficial IBGE").sum())} de {len(tabela)}')

    # Tabela auxiliar: como cada indicador é calculado (numerador / denominador)
    formulas = pd.DataFrame([{
        'indicador': ind.nome,
        'dimensao': ind.dimensao,
        'componente_do_ivs': 'sim' if ind.no_ivs else 'não (descritivo)',
        'numerador': ' + '.join(ind.numerador),
        'denominador': ' + '.join(ind.denominador) or '(sem denominador)',
        'escala': '×100' if ind.escala == 100 else 'proporção (0 a 1)' if ind.limitar_0_1 else 'valor absoluto',
        'descricao': ind.descricao,
    } for ind in TODOS_INDICADORES])

    csv_saida = destino / 'Dicionario_Variaveis_Projeto.csv'
    tabela.to_csv(csv_saida, sep=';', index=False, encoding='utf-8-sig')

    xlsx_saida = destino / 'Dicionario_Variaveis_Projeto.xlsx'
    with pd.ExcelWriter(xlsx_saida, engine='xlsxwriter') as xls:
        tabela.to_excel(xls, sheet_name='Todas as variáveis', index=False)
        formulas.to_excel(xls, sheet_name='Fórmulas dos indicadores', index=False)
        for chave, fonte in ARQUIVOS_CENSO.items():                       # uma aba por arquivo do Censo
            recorte = tabela[tabela['arquivo_fonte'] == fonte.arquivo]
            if len(recorte):
                recorte.to_excel(xls, sheet_name=fonte.rotulo[:31], index=False)
        for aba in xls.book.worksheets():                                 # largura de coluna legível
            aba.set_column(0, 0, 14)
            aba.set_column(1, 1, 80)
            aba.set_column(2, 7, 28)

    print(f'\nExportado: {csv_saida}')
    print(f'Exportado: {xlsx_saida}')


if __name__ == '__main__':
    main()
