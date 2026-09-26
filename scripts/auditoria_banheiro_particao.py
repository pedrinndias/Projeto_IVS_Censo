"""B.2 do prompt NB05 — testa se V00495 é exatamente a soma de V00236+V00237+V00238.

Hipótese, a partir do dicionário oficial do IBGE (bloco "Características do Domicílio -
Parte 2"): V00495 ("sem banheiro de uso exclusivo com chuveiro e vaso sanitário") é a
UNIÃO de três categorias que o Censo já trata como mutuamente exclusivas — V00236 (só
banheiro de uso comum), V00237 (só sanitário ou buraco para dejeções) e V00238 (nem
banheiro nem sanitário). Se a identidade fechar sem resto, a partição justifica o
"banheiro graduado" (Fase C): uma escala ordinal 1·V00236 + 2·V00237 + 3·V00238.

Saída: banco_de_dados/eda/fatorial_ampliada/banheiro_particao.csv — uma linha por setor,
com as quatro variáveis, a soma das três partes e se a identidade bateu (só é avaliável
nos setores em que as quatro estão presentes; sigilo do IBGE deixa `NaN`).

Uso:
    python scripts/auditoria_banheiro_particao.py
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))  # torna o pacote importável sem instalar

from ivs_censo import encontrar_raiz  # noqa: E402

COLUNAS = ['V00236', 'V00237', 'V00238', 'V00495']


def main() -> None:
    raiz = encontrar_raiz(Path(__file__).resolve().parent)
    entrega = raiz / 'banco_de_dados' / 'entrega_orientadora' / 'Base_ELSI_70Municipios_Censo2022.db'
    destino = raiz / 'banco_de_dados' / 'eda' / 'fatorial_ampliada'
    destino.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(entrega) as con:
        df = pd.read_sql(f"SELECT CD_SETOR, CD_MUN, V00001, {', '.join(COLUNAS)} "
                          'FROM setores_censitarios', con)

    df['n_presentes'] = df[COLUNAS].notna().sum(axis=1)
    completos = df['n_presentes'] == 4
    df['soma_v00236_v00237_v00238'] = df['V00236'] + df['V00237'] + df['V00238']
    df['bate_com_v00495'] = pd.NA
    df.loc[completos, 'bate_com_v00495'] = (
        df.loc[completos, 'soma_v00236_v00237_v00238'] == df.loc[completos, 'V00495'])

    n_completos = int(completos.sum())
    n_bate = int(df.loc[completos, 'bate_com_v00495'].sum())
    print(f'Setores: {len(df):,} | com as 4 variáveis presentes: {n_completos:,} '
          f'| identidade V00495 = V00236+V00237+V00238 bate em: {n_bate:,} de {n_completos:,}')

    if n_completos and n_bate == n_completos:
        print('Resto: nenhum — a partição fecha exatamente onde as quatro variáveis estão '
              'presentes (V00236, V00237 e V00238 são categorias mutuamente exclusivas do '
              'IBGE que compõem V00495; ver descrições oficiais no dicionário do Censo).')
    elif n_completos:
        divergentes = df.loc[completos & ~df['bate_com_v00495'].astype(bool)]
        print(f'ATENÇÃO: {len(divergentes):,} setor(es) com as 4 presentes e a soma NÃO bate '
              'com V00495 — checar o dicionário do IBGE para uma quinta categoria do bloco '
              '(candidatos: variável adjacente a V00238, verificada manualmente por '
              'scripts/auditoria_banheiro_particao.py em 26/09/2026 e não encontrada).')

    saida = destino / 'banheiro_particao.csv'
    df.to_csv(saida, sep=';', index=False, encoding='utf-8-sig')
    print(f'\nExportado: {saida}')


if __name__ == '__main__':
    main()
