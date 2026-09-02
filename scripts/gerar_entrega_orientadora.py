"""Regenera o pacote de entrega (CSV + SQLite) a partir da base atual da pipeline.

Até 09/08/2026 os arquivos de `banco_de_dados/entrega_orientadora/` tinham sido gerados
por um script ad-hoc que nunca foi versionado — não eram reproduzíveis. Este script
ocupa esse lugar e, de quebra, entrega a demanda da tabela de variáveis: o
`dicionario_variaveis` de cada `.db` agora traz **descrição oficial do IBGE, tema e
arquivo-fonte** de cada coluna.

Saídas (em `banco_de_dados/entrega_orientadora/`):
  - `Base_ELSI_70Municipios_Censo2022.csv` / `.db`
  - `Base_BeloHorizonte_Censo2022.csv` / `.db`

Cada `.db` tem três tabelas: `setores_censitarios`, `dicionario_variaveis`, `metadados`.

Uso:
    python scripts/gerar_entrega_orientadora.py
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))  # torna o pacote importável sem instalar

from ivs_censo import ARQUIVOS_CENSO, encontrar_raiz, tabela_variaveis          # noqa: E402
from ivs_censo.indicadores import (TODOS_INDICADORES, calcular_indicadores,     # noqa: E402
                                   classificar_dados_sig)

COLS_TEXTO = ['CD_SETOR', 'CD_UF', 'CD_MUN', 'NM_MUN', 'NM_BAIRRO', 'SITUACAO',
              'CD_SIT', 'CD_TIPO', 'CD_FCU', 'NM_FCU', 'Moradia_Predominante']

MAPA_MORADIA_AGRUPADA = {
    'Casa': 'Convencional', 'Casa de Vila/Condomínio': 'Convencional', 'Apartamento': 'Convencional',
    'Cortiço/Casa de Cômodos': 'Não convencional', 'Maloca Indígena': 'Não convencional',
    'Estrutura Degradada/Inacabada': 'Não convencional', 'Indefinido/Sem Moradia': 'Indefinido',
}

# Descrição das colunas criadas pela pipeline (as do IBGE vêm do dicionário oficial)
DESC_DERIVADAS = {
    'CD_UF': 'Código IBGE da Unidade da Federação (2 primeiros dígitos do CD_SETOR)',
    'CD_MUN': 'Código IBGE do município (7 primeiros dígitos do CD_SETOR)',
    'Dados_sig':'Elegibilidade do setor: OK / SIGILOSO / ZERADO / COLETIVO (regra do Cálculo IVS2012.docx)',
    'Moradia_Predominante': 'Tipo de moradia com maior contagem no setor (classificação derivada)',
    'Moradia_Predominante_Agrupada': 'Moradia predominante agrupada em Convencional / Não convencional / Indefinido',
    'urbano': '1 se SITUACAO = Urbana (recorte de análise do IVS); 0 caso contrário',
    'is_fcu': '1 se o setor é de Favela e Comunidade Urbana (CD_TIPO = 1)',
}


def preparar_base(raiz: Path) -> pd.DataFrame:
    """Lê a base bruta do Notebook 01 e aplica tipagem, elegibilidade e indicadores."""
    caminho = raiz / 'banco_de_dados' / 'Base_ELSI_Bruta_Censo2022.csv'
    if not caminho.exists():
        raise SystemExit(f'Base bruta não encontrada: {caminho}\n'
                         'Rode antes o notebook 01_Extracao_Filtragem_ELSI.ipynb.')
    df = pd.read_csv(caminho, sep=';', dtype=str)
    print(f'Base bruta: {len(df):,} setores × {len(df.columns)} colunas')

    cols_num = [c for c in df.columns if c not in COLS_TEXTO]
    df[cols_num] = (df[cols_num].replace({'X': None, 'x': None})
                    .apply(lambda c: c.astype(str).str.replace(',', '.', regex=False))
                    .apply(pd.to_numeric, errors='coerce'))

    df['Dados_sig'] = classificar_dados_sig(df)
    df['urbano'] = df['SITUACAO'].eq('Urbana').astype(int)
    df['is_fcu'] = df['CD_TIPO'].eq('1').astype(int)
    df['Moradia_Predominante_Agrupada'] = df['Moradia_Predominante'].map(MAPA_MORADIA_AGRUPADA).fillna('Indefinido')

    # Indicadores só para os setores elegíveis — nos demais ficam vazios (NULL no .db)
    ok = df['Dados_sig'] == 'OK'
    indicadores = calcular_indicadores(df[ok])
    for col in indicadores.columns:
        df[col] = pd.NA
        df.loc[ok, col] = indicadores[col]


    print(f'  elegibilidade: ' + ' | '.join(f'{k}={v:,}' for k, v in df['Dados_sig'].value_counts().items()))
    recorte = (df['Dados_sig'] == 'OK') & (df['urbano'] == 1)
    print(f'  urbanos na base: {int(df["urbano"].sum()):,} | '
          f'recorte de análise (OK e urbano): {int(recorte.sum()):,}')
    print(f'  setores de FCU na base: {int(df["is_fcu"].sum()):,} | '
          f'no recorte: {int((recorte & (df["is_fcu"] == 1)).sum()):,}')
    print(f'  indicadores calculados: {len(indicadores.columns)}')
    return df


def montar_dicionario(raiz: Path, colunas: list[str]) -> pd.DataFrame:
    """Dicionário das colunas da entrega: IBGE + derivadas da pipeline + indicadores."""
    oficial = tabela_variaveis(raiz / 'dados').set_index('variavel')
    formulas = {ind.nome: ind for ind in TODOS_INDICADORES}

    linhas = []
    for col in colunas:
        if col in oficial.index:                                   # variável original do Censo
            linha = oficial.loc[col]
            linhas.append({'coluna': col, 'descricao': linha['descricao_oficial'],
                           'tema': linha['tema_ibge'], 'origem': 'Censo 2022 (IBGE)',
                           'arquivo_fonte': linha['arquivo_fonte'], 'formula': ''})
        elif col in formulas:                                      # indicador calculado
            ind = formulas[col]
            den = ' + '.join(ind.denominador) or '(sem denominador)'
            linhas.append({'coluna': col, 'descricao': ind.descricao, 'tema': ind.dimensao,
                           'origem': 'Calculado pela pipeline', 'arquivo_fonte': '(derivado)',
                           'formula': f'({" + ".join(ind.numerador)}) / ({den})'
                                      + (' × 100' if ind.escala == 100 else '')})
        else:                                                      # coluna derivada de classificação
            linhas.append({'coluna': col, 'descricao': DESC_DERIVADAS.get(col, '(sem descrição)'),
                           'tema': 'Identificação', 'origem': 'Derivado pela pipeline',
                           'arquivo_fonte': '(derivado)', 'formula': ''})
    return pd.DataFrame(linhas)


def gravar(df: pd.DataFrame, dicionario: pd.DataFrame, destino: Path, nome: str, rotulo: str) -> None:
    """Grava o par CSV + SQLite de um recorte."""
    csv_path, db_path = destino / f'{nome}.csv', destino / f'{nome}.db'
    df.to_csv(csv_path, sep=';', index=False, encoding='utf-8-sig')

    metadados = pd.DataFrame([
        ('recorte', rotulo),
        ('fonte', 'IBGE — Censo Demográfico 2022, Agregados por Setores Censitários'),
        ('gerado_em', date.today().isoformat()),
        ('gerado_por', 'scripts/gerar_entrega_orientadora.py'),
        ('n_setores', f'{len(df):,}'),
        ('n_municipios', f"{df['CD_MUN'].nunique()}"),
        ('n_setores_ok', f"{int((df['Dados_sig'] == 'OK').sum()):,}"),
        # Duas contagens diferentes, e a distinção importa: `n_setores_urbanos` conta
        # SITUACAO='Urbana' na base inteira (inclui zerados e sigilosos); o recorte de
        # análise é a INTERSEÇÃO com Dados_sig='OK'. Publicar só a primeira fazia a
        # documentação anunciar 106.347 como recorte — número maior que os 106.281
        # elegíveis, impossível por construção, e diferente dos 104.108 que a própria
        # consulta SQL recomendada devolve.
        ('n_setores_urbanos', f"{int(df['urbano'].sum()):,}"),
        ('n_setores_recorte_analise',
         f"{int(((df['Dados_sig'] == 'OK') & (df['urbano'] == 1)).sum()):,}"),
        ('n_setores_favela_fcu', f"{int(df['is_fcu'].sum()):,}"),
        ('n_setores_favela_fcu_no_recorte',
         f"{int(((df['Dados_sig'] == 'OK') & (df['urbano'] == 1) & (df['is_fcu'] == 1)).sum()):,}"),
        ('denominador_domiciliar', 'V00001 — Domicílios Particulares Permanentes Ocupados'),
        ('recorte_de_analise', 'Setores urbanos (SITUACAO = Urbana) com Dados_sig = OK'),
        ('arquivos_do_censo', ' | '.join(f.arquivo for f in ARQUIVOS_CENSO.values())),
    ], columns=['chave', 'valor'])

    if db_path.exists():
        db_path.unlink()                                            # recria do zero (evita schema antigo)
    with sqlite3.connect(db_path) as con:
        df.to_sql('setores_censitarios', con, index=False)
        dicionario.to_sql('dicionario_variaveis', con, index=False)
        metadados.to_sql('metadados', con, index=False)
        con.execute('CREATE INDEX idx_mun ON setores_censitarios (CD_MUN)')
        con.execute('CREATE INDEX idx_sig ON setores_censitarios (Dados_sig)')

    print(f'  {nome}: {len(df):,} setores × {len(df.columns)} colunas — '
          f'CSV {csv_path.stat().st_size / 1e6:.1f} MB | DB {db_path.stat().st_size / 1e6:.1f} MB')


def main() -> None:
    raiz = encontrar_raiz(Path(__file__).resolve().parent)
    destino = raiz / 'banco_de_dados' / 'entrega_orientadora'
    destino.mkdir(parents=True, exist_ok=True)

    df = preparar_base(raiz)
    dicionario = montar_dicionario(raiz, list(df.columns))
    faltando = dicionario[dicionario['descricao'] == '(sem descrição)']['coluna'].tolist()
    print(f'\nDicionário: {len(dicionario)} colunas descritas'
          + (f' — SEM DESCRIÇÃO: {faltando}' if faltando else ' — todas com descrição'))

    print('\nGravando entregáveis:')
    gravar(df, dicionario, destino, 'Base_ELSI_70Municipios_Censo2022', '70 municípios da amostra ELSI-Brasil')
    bh = df[df['CD_MUN'] == '3106200'].copy()                       # Belo Horizonte
    gravar(bh, dicionario, destino, 'Base_BeloHorizonte_Censo2022', 'Belo Horizonte (MG)')
    print(f'\nSaídas em {destino}')


if __name__ == '__main__':
    main()
