"""Gera o quadro de indicadores pedido pela orientadora, a partir do código.

Demanda 2 (set/2026): um quadro que explique cada indicador calculado pela pipeline — o
que mede, como é calculado e de onde vêm os dados — sem nada digitado à parte. Tudo sai
de `TODOS_INDICADORES` (`indicadores.py`), do mapa de arquivos-fonte (`fontes.py`) e do
dicionário oficial do IBGE (via `tabela_variaveis`, em `dicionario.py`).

Isso também fecha a parte do achado IND-3 sobre os 26 indicadores: eles passam a ter
este quadro próprio, com fórmula e descrição de cada código V.

Saídas (em `banco_de_dados/entrega_orientadora/`):
  - `Quadro_Indicadores.csv` / `.xlsx`
  - `Quadro_Indicadores.md` — versão para colar em documento

Uso:
    python scripts/gerar_quadro_indicadores.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))  # torna o pacote importável sem instalar

from ivs_censo import ARQUIVOS_CENSO, encontrar_raiz, tabela_variaveis   # noqa: E402
from ivs_censo.indicadores import TODOS_INDICADORES                      # noqa: E402


def _descrever_codigos(codigos: list[str], oficial: pd.DataFrame) -> str:
    """'V00112 — descrição do IBGE | V00113 — ...', na ordem do indicador."""
    partes = []
    for cod in codigos:
        desc = oficial.loc[cod, 'descricao_oficial'] if cod in oficial.index else '(sem descrição)'
        partes.append(f'{cod} — {desc}')
    return ' | '.join(partes)


def montar_quadro(raiz: Path) -> pd.DataFrame:
    """Um indicador por linha, com numerador/denominador descritos e o arquivo de origem."""
    oficial = tabela_variaveis(raiz / 'dados').set_index('variavel')
    arquivo_de = {var: fonte.arquivo for fonte in ARQUIVOS_CENSO.values() for var in fonte.variaveis}

    linhas = []
    for ind in TODOS_INDICADORES:
        codigos = [*ind.numerador, *ind.denominador]
        arquivos = sorted({arquivo_de[c] for c in codigos if c in arquivo_de})

        observacao = []
        if ind.complemento:
            observacao.append('valor = complemento (1 − numerador/denominador)')
        if len(ind.numerador) > 1:
            observacao.append('numerador soma várias variáveis: sigilo parcial em uma delas '
                              'entra como zero (min_count=1)')
        if ind.min_count_den > 1:
            observacao.append(f'denominador exige as {ind.min_count_den} parcelas presentes '
                              '(sem tolerância a sigilo parcial)')
        if not ind.limitar_0_1:
            observacao.append('sem corte em [0, 1] — não é proporção')
        if ind.escala != 1:
            observacao.append(f'escala ×{ind.escala:g}')

        linhas.append({
            'indicador': ind.nome,
            'dimensao': ind.dimensao,
            'entra_no_ivs7': 'Sim' if ind.no_ivs else 'Não',
            'o_que_mede': ind.descricao,
            'numerador': _descrever_codigos(ind.numerador, oficial),
            'denominador': _descrever_codigos(ind.denominador, oficial) or '(sem denominador)',
            'complemento': 'Sim' if ind.complemento else 'Não',
            'arquivo_fonte': ' | '.join(arquivos) or '(indefinido)',
            'observacao': '; '.join(observacao) or '(sem observação)',
        })
    return pd.DataFrame(linhas)


def _para_markdown(df: pd.DataFrame) -> str:
    """Markdown sem depender de `tabulate` (o projeto só usa numpy/pandas)."""
    cols = list(df.columns)
    linhas = ['| ' + ' | '.join(cols) + ' |', '|' + '|'.join(['---'] * len(cols)) + '|']
    for _, linha in df.iterrows():
        celulas = [str(linha[c]).replace('|', '\\|').replace('\n', ' ') for c in cols]
        linhas.append('| ' + ' | '.join(celulas) + ' |')
    return '\n'.join(linhas) + '\n'


def main() -> None:
    raiz = encontrar_raiz(Path(__file__).resolve().parent)
    destino = raiz / 'banco_de_dados' / 'entrega_orientadora'
    destino.mkdir(parents=True, exist_ok=True)

    quadro = montar_quadro(raiz)
    print(f'Quadro de indicadores: {len(quadro)} linhas '
          f'({int((quadro["entra_no_ivs7"] == "Sim").sum())} do IVS-7, '
          f'{int((quadro["entra_no_ivs7"] == "Não").sum())} complementares)')
    assert len(quadro) == len(TODOS_INDICADORES), 'quadro tem que ter uma linha por indicador'

    csv_saida = destino / 'Quadro_Indicadores.csv'
    quadro.to_csv(csv_saida, sep=';', index=False, encoding='utf-8-sig')

    xlsx_saida = destino / 'Quadro_Indicadores.xlsx'
    with pd.ExcelWriter(xlsx_saida, engine='xlsxwriter') as xls:
        quadro.to_excel(xls, sheet_name='Quadro de indicadores', index=False)
        for aba in xls.book.worksheets():
            aba.set_column(0, 0, 26)
            aba.set_column(1, 2, 14)
            aba.set_column(3, 3, 50)
            aba.set_column(4, 5, 60)
            aba.set_column(6, 8, 32)

    md_saida = destino / 'Quadro_Indicadores.md'
    md_saida.write_text(_para_markdown(quadro), encoding='utf-8')

    print(f'Exportado: {csv_saida}')
    print(f'Exportado: {xlsx_saida}')
    print(f'Exportado: {md_saida}')


if __name__ == '__main__':
    main()
