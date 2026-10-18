#!/usr/bin/env python
"""Base nacional por setor, no formato da base da entrega, para a versão A6_brasil.

    ./.venv/bin/python scripts/base_nacional_versoes.py      # ~10 min, lê os 2,4 GB de dados/

Lê os arquivos do Censo do Brasil inteiro com `proporcoes_brasil.montar_base_nacional` e
aplica as mesmas regras de `gerar_entrega_orientadora.preparar_base` (Dados_sig, urbano,
FCU, indicadores só nos setores OK, as duas variantes de renda). Diferença de propósito:
`NM_MUN` ganha a sigla da UF ("Bom Jesus/PI"), porque o nome sozinho se repete no país e o
índice é normalizado por município. Grava `banco_de_dados/nacional/Base_Brasil_Censo2022.db`
(não versionado).
"""
import sqlite3
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'src'))
sys.path.insert(0, str(RAIZ / 'scripts'))

from ivs_censo.indicadores import calcular_indicadores, classificar_dados_sig  # noqa: E402
from ivs_censo.renda import renda_imputada_mediana_municipal, renda_sem_extremos  # noqa: E402
import proporcoes_brasil as pb  # noqa: E402

SIGLAS = {'11': 'RO', '12': 'AC', '13': 'AM', '14': 'RR', '15': 'PA', '16': 'AP', '17': 'TO', '21': 'MA',
          '22': 'PI', '23': 'CE', '24': 'RN', '25': 'PB', '26': 'PE', '27': 'AL', '28': 'SE', '29': 'BA',
          '31': 'MG', '32': 'ES', '33': 'RJ', '35': 'SP', '41': 'PR', '42': 'SC', '43': 'RS', '50': 'MS',
          '51': 'MT', '52': 'GO', '53': 'DF'}
DESTINO = RAIZ / 'banco_de_dados' / 'nacional' / 'Base_Brasil_Censo2022.db'


def main() -> None:
    df = pb.montar_base_nacional(RAIZ / 'dados').reset_index()
    for c in df.columns:
        if isinstance(df[c].dtype, pd.CategoricalDtype):
            df[c] = df[c].astype(str)
    df['UF'] = df['CD_UF'].map(SIGLAS)
    df['NM_MUN'] = df['NM_MUN'] + '/' + df['UF']
    df['CD_UF'] = pd.to_numeric(df['CD_UF'])
    df['Dados_sig'] = classificar_dados_sig(df)
    df['urbano'] = df['SITUACAO'].eq('Urbana').astype(int)
    df['is_fcu'] = df['CD_TIPO'].eq('1').astype(int)
    ok = df['Dados_sig'] == 'OK'
    ind = calcular_indicadores(df[ok])
    df = pd.concat([df, ind.reindex(df.index)], axis=1)
    df['renda_media_sem_extremo'] = renda_sem_extremos(df, 'renda_media')
    df['renda_media_mediana_mun'] = renda_imputada_mediana_municipal(df, 'renda_media')
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.unlink(missing_ok=True)
    with sqlite3.connect(DESTINO) as con:
        df.to_sql('setores_censitarios', con, index=False, chunksize=50_000)
    rec = ok & (df['urbano'] == 1)
    print(f'{DESTINO.relative_to(RAIZ)}: {len(df):,} setores; urbanos OK {int(rec.sum()):,}; '
          f'FCU no recorte {int((rec & (df["is_fcu"] == 1)).sum()):,}; {len(ind.columns)} indicadores')


if __name__ == '__main__':
    main()
