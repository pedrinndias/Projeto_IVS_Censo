"""Calcula os indicadores de proporção por setor censitário para o BRASIL INTEIRO
e compara com o recorte dos 70 municípios do ELSI-Brasil.

Demanda da orientadora (jul/2026): *"indicadores de proporção de presença de atributos
em relação à quantidade de domicílio no setor — fazer o Brasil todo e depois para os
70 municípios"*.

O que o script faz:

1. lê os 8 arquivos do Censo 2022 **sem filtro de município** (~468 mil setores),
   em chunks, convertendo cada pedaço para número na hora (segura a memória);
2. aplica as mesmas regras da pipeline ELSI — sigilo `X` → `NaN`, classificação
   `Dados_sig`, recorte urbano — usando o módulo compartilhado `src/ivs_censo`;
3. calcula os indicadores por setor com as fórmulas do Notebook 02;
4. agrega em quatro níveis (Brasil, região, UF, município) e em três recortes
   (Brasil todo, Brasil urbano, ELSI-70 urbano);
5. exporta a tabela comparativa **Brasil × 70 municípios**, que serve de linha de base
   de representatividade da amostra ELSI.

Cada indicador é resumido de duas formas, porque elas respondem a perguntas diferentes:

* **média/mediana entre setores** — trata cada setor como uma observação. É a leitura
  intraurbana, coerente com o objeto do projeto e com as descritivas do Notebook 02;
* **razão agregada** (soma dos numeradores / soma dos denominadores) — trata o recorte
  como um território único. É o número comparável com estatísticas publicadas.

Uso:
    python scripts/proporcoes_brasil.py                  # completo (~10 min, lê 2,4 GB)
    python scripts/proporcoes_brasil.py --salvar-setores # grava também o CSV por setor
    python scripts/proporcoes_brasil.py --limite-chunks 3  # teste rápido (parcial)
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))  # torna o pacote importável sem instalar

from ivs_censo import ARQUIVOS_CENSO, encontrar_raiz                                  # noqa: E402
from ivs_censo.indicadores import (INDICADORES_IVS, TODOS_INDICADORES,                # noqa: E402
                                   calcular_indicadores, classificar_dados_sig)

CHUNK = 200_000                       # linhas por pedaço de leitura
COLS_CATEGORIA = ['SITUACAO', 'CD_SIT', 'CD_TIPO', 'NM_MUN']   # texto repetitivo -> category (economiza RAM)
COLS_TEXTO = ['CD_FCU', 'NM_FCU', 'NM_BAIRRO']                 # texto livre


def _para_numero(bloco: pd.DataFrame) -> pd.DataFrame:
    """Converte um bloco de colunas-texto do IBGE em número: 'X' (sigilo) -> NaN,
    vírgula decimal -> ponto, e o resto para float64.

    **float64 é obrigatório aqui, não é preciosismo.** Com float32 (24 bits de mantissa)
    a soma da população do país erra por arredondamento acumulado: dá 203.080.736 em vez
    dos 203.080.756 do Censo 2022. O erro relativo é ínfimo (1e-7) e não muda nenhuma
    proporção, mas os totais publicados deixam de bater com o IBGE — e é justamente por
    eles que o resultado vai ser conferido. Custo: ~0,3 GB a mais de RAM.
    """
    bloco = bloco.replace({'X': None, 'x': None})
    bloco = bloco.apply(lambda c: c.astype(str).str.replace(',', '.', regex=False))
    return bloco.apply(pd.to_numeric, errors='coerce').astype('float64')


def ler_arquivo_nacional(caminho_dados: Path, chave: str, limite_chunks: int | None = None) -> pd.DataFrame:
    """Lê um dos arquivos do Censo inteiro (sem filtro), já convertido, indexado por CD_SETOR."""
    fonte = ARQUIVOS_CENSO[chave]
    caminho = caminho_dados / fonte.arquivo
    inicio = time.time()

    for encoding in ('utf-8', 'latin1'):                     # os CSVs do IBGE alternam entre os dois
        try:
            pedacos = []
            leitor = pd.read_csv(caminho, sep=';', dtype=str, usecols=fonte.colunas,
                                 encoding=encoding, chunksize=CHUNK, low_memory=False)
            for i, pedaco in enumerate(leitor):
                if limite_chunks is not None and i >= limite_chunks:
                    break
                pedaco = pedaco.rename(columns={fonte.chave: 'CD_SETOR'}).set_index('CD_SETOR')
                numericas = [c for c in pedaco.columns if c not in COLS_CATEGORIA + COLS_TEXTO]
                convertido = _para_numero(pedaco[numericas])                       # V… viram float64
                for c in [c for c in pedaco.columns if c in COLS_CATEGORIA]:       # códigos repetitivos
                    convertido[c] = pedaco[c].astype('category')
                for c in [c for c in pedaco.columns if c in COLS_TEXTO]:           # texto livre
                    convertido[c] = pedaco[c]
                pedacos.append(convertido)
            df = pd.concat(pedacos)
            print(f'  {fonte.rotulo:<22} {len(df):>8,} setores  '
                  f'({encoding}, {time.time() - inicio:.0f}s, {df.memory_usage(deep=True).sum() / 1e6:.0f} MB)')
            return df
        except UnicodeDecodeError:
            continue
    # latin1 decodifica qualquer byte, então este ponto só é alcançável se o arquivo
    # sumir ou vier truncado. RuntimeError, e não UnicodeDecodeError: esta última exige
    # cinco argumentos e levantá-la com um só trocaria o erro real por um TypeError.
    raise RuntimeError(f'Não foi possível ler {caminho}')


def montar_base_nacional(caminho_dados: Path, limite_chunks: int | None = None) -> pd.DataFrame:
    """Lê os 8 arquivos e devolve a base nacional unificada, indexada por CD_SETOR."""
    print('Lendo os 8 arquivos do Censo 2022 para o Brasil inteiro (sem filtro de município)...')
    partes = {chave: ler_arquivo_nacional(caminho_dados, chave, limite_chunks) for chave in ARQUIVOS_CENSO}

    base = partes.pop('basico')                                        # o básico define o universo de setores
    for chave, parte in partes.items():
        base = base.join(parte, how='left')                            # LEFT JOIN: mantém todos os setores
    base['CD_UF'] = base.index.str[:2]                                 # UF = 2 primeiros dígitos do geocódigo
    base['CD_MUN'] = base.index.str[:7]                                # município = 7 primeiros dígitos
    print(f'\nBase nacional: {len(base):,} setores × {len(base.columns)} colunas '
          f'({base.memory_usage(deep=True).sum() / 1e9:.2f} GB em memória)')
    return base


def resumir(df: pd.DataFrame, nomes: list[str]) -> pd.DataFrame:
    """Para cada indicador: descritivas entre setores + razão agregada do recorte."""
    linhas = []
    for ind in TODOS_INDICADORES:
        if ind.nome not in nomes or ind.nome not in df.columns:
            continue
        s = df[ind.nome].dropna()
        if ind.denominador:                                            # razão agregada (soma/soma)
            num_setor = df[ind.numerador].sum(axis=1, min_count=1)
            den_setor = df[ind.denominador].sum(axis=1, min_count=ind.min_count_den)
            # Somar cada lado por conta própria mede numerador e denominador em
            # conjuntos DIFERENTES de setores: onde o numerador é sigiloso, o setor sai
            # do numerador mas o denominador dele continua na conta, e a razão sai baixa
            # demais. Em pct_apartamento isso dava −8,9%; em pct_sem_banheiro, −13,1%.
            # Restringir aos setores em que os dois lados existem é o que torna a razão
            # agregada uma razão de fato.
            par = num_setor.notna() & den_setor.notna()
            num, den = num_setor[par].sum(), den_setor[par].sum()
            agregado = (num / den * ind.escala) if den else np.nan
        else:
            agregado = df[ind.numerador[0]].mean()                     # renda: média simples
        linhas.append({
            'indicador': ind.nome,
            'dimensao': ind.dimensao,
            'componente_ivs': ind.no_ivs,
            'n_setores': int(len(s)),
            'media_entre_setores': s.mean(),
            'dp_entre_setores': s.std(),
            'p25': s.quantile(0.25) if len(s) else np.nan,
            'mediana': s.median() if len(s) else np.nan,
            'p75': s.quantile(0.75) if len(s) else np.nan,
            'razao_agregada': agregado,
        })
    return pd.DataFrame(linhas)


def resumir_por_grupo(df: pd.DataFrame, chaves: list[str], nomes: list[str]) -> pd.DataFrame:
    """Aplica `resumir` dentro de cada grupo (região, UF ou município)."""
    saida = []
    for chave, grupo in df.groupby(chaves, sort=True, observed=True):
        chave = chave if isinstance(chave, tuple) else (chave,)
        parcial = resumir(grupo, nomes)
        for k, v in zip(chaves, chave):
            parcial.insert(0, k, v)
        saida.append(parcial)
    return pd.concat(saida, ignore_index=True) if saida else pd.DataFrame()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--salvar-setores', action='store_true',
                    help='grava também os indicadores por setor (CSV grande, ~200 MB, não versionado)')
    ap.add_argument('--limite-chunks', type=int, default=None,
                    help='lê apenas N chunks de cada arquivo — só para teste rápido; resultado PARCIAL')
    args = ap.parse_args()

    raiz = encontrar_raiz(Path(__file__).resolve().parent)
    destino = raiz / 'banco_de_dados' / 'nacional'
    destino.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    # ── 1. Base nacional ──────────────────────────────────────────────────────
    base = montar_base_nacional(raiz / 'dados', args.limite_chunks)

    # ── 2. Elegibilidade e recorte urbano (mesmas regras do Notebook 02) ──────
    base['Dados_sig'] = classificar_dados_sig(base)
    base['urbano'] = base['SITUACAO'].astype(str).eq('Urbana')
    base['is_fcu'] = base['CD_TIPO'].astype(str).eq('1')
    print('\nElegibilidade (Brasil):')
    print(base['Dados_sig'].value_counts().rename('n_setores').to_frame()
          .assign(pct=lambda d: (d['n_setores'] / len(base) * 100).round(2)).to_string())
    print(f"\nSituação: urbanos {int(base['urbano'].sum()):,} | "
          f"não urbanos {int((~base['urbano']).sum()):,} | FCU {int(base['is_fcu'].sum()):,}")

    # ── 3. Municípios do ELSI (para separar os recortes) ──────────────────────
    elsi = pd.read_csv(raiz / 'dados' / 'municipios_elsi_brasil.csv', sep=';', dtype=str)
    import unicodedata

    def normaliza(s):
        s = unicodedata.normalize('NFD', str(s).strip().lower())
        return ' '.join(''.join(c for c in s if not unicodedata.combining(c)).split())

    chaves_elsi = set(elsi['uf_codigo'].str.zfill(2) + '|' + elsi['nm_municipio'].map(normaliza))
    base['is_elsi'] = (base['CD_UF'] + '|' + base['NM_MUN'].astype(str).map(normaliza)).isin(chaves_elsi)
    print(f"Setores nos 70 municípios do ELSI: {int(base['is_elsi'].sum()):,} "
          f"({base['is_elsi'].mean() * 100:.2f}% do país) | "
          f"municípios casados: {base.loc[base['is_elsi'], 'CD_MUN'].nunique()}")

    # ── 4. Indicadores por setor ──────────────────────────────────────────────
    print('\nCalculando indicadores por setor...')
    indicadores = calcular_indicadores(base)
    base = pd.concat([base, indicadores], axis=1)
    nomes = [c for c in indicadores.columns]
    print(f'  {len(nomes)} indicadores calculados para {len(base):,} setores')

    # regiões a partir do código da UF (1=N, 2=NE, 3=SE, 4=S, 5=CO)
    mapa_regiao = {'1': 'Norte', '2': 'Nordeste', '3': 'Sudeste', '4': 'Sul', '5': 'Centro-Oeste'}
    base['regiao'] = base['CD_UF'].str[0].map(mapa_regiao)

    # ── 5. Recortes ───────────────────────────────────────────────────────────
    ok = base['Dados_sig'] == 'OK'
    recortes = {
        'Brasil (todos os setores elegíveis)': base[ok],
        'Brasil (apenas urbanos)':             base[ok & base['urbano']],
        'ELSI 70 municípios (apenas urbanos)': base[ok & base['urbano'] & base['is_elsi']],
    }
    for nome, recorte in recortes.items():
        print(f'  {nome:<38} {len(recorte):>8,} setores')

    # ── 6. Tabelas ────────────────────────────────────────────────────────────
    print('\nAgregando...')
    total = pd.concat([resumir(r, nomes).assign(recorte=nome) for nome, r in recortes.items()], ignore_index=True)
    total = total[['recorte', *[c for c in total.columns if c != 'recorte']]]

    br_urbano = recortes['Brasil (apenas urbanos)']
    por_regiao = resumir_por_grupo(br_urbano, ['regiao'], nomes)
    por_uf = resumir_por_grupo(br_urbano, ['CD_UF'], nomes)
    por_municipio = resumir_por_grupo(br_urbano, ['CD_UF', 'CD_MUN', 'NM_MUN'], nomes)

    # comparativo Brasil × ELSI (o entregável central desta demanda)
    comp = (total[total['recorte'] != 'Brasil (todos os setores elegíveis)']
            .pivot(index='indicador', columns='recorte',
                   values=['media_entre_setores', 'mediana', 'razao_agregada']))
    comp.columns = [f'{a}__{"BR_urbano" if "Brasil" in b else "ELSI70_urbano"}' for a, b in comp.columns]
    comp['razao_ELSI_sobre_BR'] = (comp['razao_agregada__ELSI70_urbano']
                                   / comp['razao_agregada__BR_urbano']).round(3)
    comp = comp.reset_index()

    # representatividade da amostra ELSI dentro do Brasil
    repres = pd.DataFrame([{
        'metrica': m,
        'Brasil': b,
        'ELSI_70': e,
        'pct_ELSI_sobre_Brasil': round(e / b * 100, 2) if b else np.nan,
    } for m, b, e in [
        ('setores (todos)', len(base), int(base['is_elsi'].sum())),
        ('setores urbanos elegíveis', len(br_urbano), len(recortes['ELSI 70 municípios (apenas urbanos)'])),
        ('municípios', base['CD_MUN'].nunique(), base.loc[base['is_elsi'], 'CD_MUN'].nunique()),
        ('população (v0001)', base['v0001'].sum(), base.loc[base['is_elsi'], 'v0001'].sum()),
        ('domicílios (V00001)', base['V00001'].sum(), base.loc[base['is_elsi'], 'V00001'].sum()),
        ('setores de favela (FCU)', int(base['is_fcu'].sum()), int((base['is_fcu'] & base['is_elsi']).sum())),
    ]])

    # ── 7. Exportação ─────────────────────────────────────────────────────────
    def exporta(df, nome):
        caminho = destino / nome
        df.to_csv(caminho, sep=';', index=False, encoding='utf-8-sig', float_format='%.6f')
        print(f'  {nome:<42} {len(df):>7,} linhas')

    print('\nExportando:')
    exporta(total, 'proporcoes_por_recorte.csv')
    exporta(por_regiao, 'proporcoes_brasil_por_regiao.csv')
    exporta(por_uf, 'proporcoes_brasil_por_uf.csv')
    exporta(por_municipio, 'proporcoes_brasil_por_municipio.csv')
    exporta(comp, 'comparativo_brasil_vs_elsi.csv')
    exporta(repres, 'representatividade_elsi_no_brasil.csv')

    if args.salvar_setores:
        cols = ['CD_UF', 'CD_MUN', 'NM_MUN', 'regiao', 'SITUACAO', 'CD_TIPO',
                'Dados_sig', 'urbano', 'is_fcu', 'is_elsi', 'v0001', 'V00001', *nomes]
        caminho = destino / 'indicadores_brasil_por_setor.csv'
        base[cols].to_csv(caminho, sep=';', encoding='utf-8-sig', float_format='%.6f')
        print(f'  indicadores_brasil_por_setor.csv          {len(base):>7,} linhas '
              f'({caminho.stat().st_size / 1e6:.0f} MB)')

    # ── 8. Resumo no console ──────────────────────────────────────────────────
    print('\n=== Comparativo Brasil urbano × 70 municípios ELSI (razão agregada) ===')
    cols_show = ['indicador', 'razao_agregada__BR_urbano', 'razao_agregada__ELSI70_urbano', 'razao_ELSI_sobre_BR']
    ivs = [i.nome for i in INDICADORES_IVS]
    print(comp[comp['indicador'].isin(ivs)][cols_show].round(4).to_string(index=False))
    print('\n=== Representatividade da amostra ELSI ===')
    print(repres.to_string(index=False))
    print(f'\nConcluído em {(time.time() - t0) / 60:.1f} min. Saídas em {destino}')
    if args.limite_chunks:
        print('*** ATENÇÃO: rodado com --limite-chunks; os resultados são PARCIAIS. ***')


if __name__ == '__main__':
    main()
