"""Regenera as tabelas de auditoria e de apresentação de `banco_de_dados/eda/`.

Estas 9 tabelas foram commitadas em 2026 a partir de código ad-hoc que nunca entrou no
git — eram os "CSVs órfãos" do README da pasta. Este script recupera a procedência delas:
o código aqui reproduz os arquivos commitados **valor a valor**, conferido célula a
célula em 20/08/2026. Oito saem byte a byte iguais (fora a quebra de linha CRLF -> LF);
em `auditoria_analfabetismo_municipio.csv` mudou só a ordem de 11 linhas empatadas —
ver o comentário sobre o desempate em `tabelas_analfabetismo`.

Recorte
-------
Todas as tabelas usam `Dados_sig == 'OK'` — **106.281 setores, com os rurais**. É o
recorte que valia quando elas foram geradas, e é o que sustenta os números já
apresentados à orientadora. O Notebook 02, da seção 3b em diante, usa o recorte urbano
(104.108 setores); por isso estes arquivos **não** são comparáveis linha a linha com as
tabelas da pipeline. Para migrar de recorte, filtrar `SITUACAO == 'Urbana'` em `df_ok`
logo após a classificação — os números todos mudam, e as apresentações antigas deixam de
bater.

Uso:
    ./.venv/bin/python scripts/gerar_tabelas_auditoria.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))  # torna o pacote importável sem instalar

from ivs_censo import (INDICADORES_IVS, calcular_indicadores,          # noqa: E402
                       classificar_dados_sig, encontrar_raiz)

# Colunas de identificação — não viram número (mesma lista do Notebook 02).
COLS_TEXTO = ['CD_SETOR', 'CD_UF', 'CD_MUN', 'NM_MUN', 'NM_BAIRRO',
              'SITUACAO', 'CD_SIT', 'CD_TIPO', 'CD_FCU', 'NM_FCU',
              'Moradia_Predominante']

INDICADORES = [ind.nome for ind in INDICADORES_IVS]     # os 7 componentes do IVS
ORDEM_REGIAO = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']  # ordem das colunas na morfologia

# Lixo: o bloco inadequado completo é V00398–V00402. V00398 é a caçamba de serviço de
# limpeza — lixo que É recolhido, só que indiretamente. Tirando a caçamba do numerador
# sobra "lixo sem coleta nenhuma", que é o que a coluna coleta_lixo_100 mede.
LIXO_SEM_COLETA = ['V00399', 'V00400', 'V00401', 'V00402']

# Tipo de espécie do domicílio (arquivo Domicílio 1). V00047 (casa) fica de fora das
# linhas por ser o caso-base: a tabela existe para mostrar o que NÃO é casa.
MORFOLOGIA = {
    'V00048': 'Casa de vila/condomínio',
    'V00049': 'Apartamento',
    'V00050': 'Cortiço/casa de cômodos',
    'V00051': 'Maloca indígena',
    'V00052': 'Estrutura permanente degradada',
    'V00053': 'Tenda/barraca',
    'V00054': 'Dentro de estabelecimento',
    'V00055': 'Abrigo natural/outras',
    'V00056': 'Estrutura em logradouro público',
    'V00057': 'Estrutura não-residencial degradada',
    'V00058': 'Veículo',
}

# Faixas de V00900 (pessoas de 15+ que sabem ler) usadas na auditoria do sigilo:
# setores pequenos são os que mais sofrem supressão, e é isso que a tabela mostra.
BINS_V00900 = [0, 10, 50, 100, 200, 500, 1000, float('inf')]
ROTULOS_V00900 = ['1-10', '11-50', '51-100', '101-200', '201-500', '501-1000', '1000+']

SANEAMENTO = {                       # rótulo da apresentação -> indicador calculado
    'Água inadequada': 'pct_agua_inad',
    'Esgoto inadequado': 'pct_esgoto_inad',
    'Lixo inadequado': 'pct_lixo_inad',
}


def carregar_setores_ok(raiz: Path) -> pd.DataFrame:
    """Lê a base bruta do Notebook 01 e devolve só os setores elegíveis, já numéricos.

    Repete o pré-processamento das seções 2 e 3 do Notebook 02: sigilo `X` -> `NaN`,
    vírgula decimal -> ponto, classificação `Dados_sig` e mapa UF -> região.
    """
    base = raiz / 'banco_de_dados' / 'Base_ELSI_Bruta_Censo2022.csv'
    if not base.exists():
        raise SystemExit(f'Base não encontrada: {base}\nRode antes o Notebook 01 da Fase 3.')

    df = pd.read_csv(base, sep=';', dtype=str)                      # tudo como texto (preserva 'X' e zeros à esquerda)
    cols_num = [c for c in df.columns if c not in COLS_TEXTO]       # as demais são variáveis V…
    df[cols_num] = df[cols_num].replace({'X': None, 'x': None})     # sigilo do IBGE -> nulo
    df[cols_num] = df[cols_num].apply(lambda c: c.astype(str).str.replace(',', '.', regex=False))  # decimal
    df[cols_num] = df[cols_num].apply(pd.to_numeric, errors='coerce')                              # -> número

    df['Dados_sig'] = classificar_dados_sig(df)                     # mesma regra do Notebook 02
    ref = pd.read_csv(raiz / 'dados' / 'municipios_elsi_brasil.csv', sep=';', dtype=str)
    df['regiao'] = df['CD_UF'].map(dict(zip(ref['uf_codigo'].str.zfill(2), ref['regiao'])))

    ok = df[df['Dados_sig'] == 'OK'].copy()                         # recorte destas tabelas (com rurais)
    ok[INDICADORES] = calcular_indicadores(ok, INDICADORES_IVS)     # fórmulas de src/ivs_censo
    print(f'Setores OK (com rurais): {len(ok):,} de {len(df):,}')
    return ok


def _cobertura(g: pd.DataFrame) -> pd.Series:
    """Quantos setores do grupo têm cobertura *integral* de cada serviço.

    "Integral" = o indicador de inadequação é exatamente 0, isto é, nenhum domicílio do
    setor está na condição inadequada. É a leitura otimista pedida para o slide de
    cobertura; a leitura por média de setor está nas descritivas do Notebook 02.
    """
    n = len(g)
    agua = int((g['pct_agua_inad'] == 0).sum())
    esgoto = int((g['pct_esgoto_inad'] == 0).sum())
    lixo = int((g['pct_lixo_inad'] == 0).sum())
    san3 = int(((g['pct_agua_inad'] == 0) & (g['pct_esgoto_inad'] == 0) & (g['pct_lixo_inad'] == 0)).sum())
    dados7 = int(g[INDICADORES].notna().all(axis=1).sum())          # setores sem nenhum dos 7 indicadores nulo
    coleta = int((g[LIXO_SEM_COLETA].sum(axis=1, min_count=1) == 0).sum())
    # dtype=object para as contagens saírem inteiras no CSV (senão o pandas promove tudo
    # a float por causa das colunas de percentual, e a tabela vira 106281.0)
    return pd.Series({
        'n_setores_OK': n,
        'agua_adeq_100': agua,     'pct_agua_adeq_100': round(agua / n * 100, 1),
        'esgoto_adeq_100': esgoto, 'pct_esgoto_adeq_100': round(esgoto / n * 100, 1),
        'lixo_adeq_100': lixo,     'pct_lixo_adeq_100': round(lixo / n * 100, 1),
        'saneamento_3_100': san3,  'pct_saneamento_3_100': round(san3 / n * 100, 1),
        'dados_7vars_100': dados7, 'pct_dados_7vars_100': round(dados7 / n * 100, 1),
        'coleta_lixo_100': coleta, 'pct_coleta_lixo_100': round(coleta / n * 100, 1),
    }, dtype=object)


def tabelas_cobertura(ok: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """cobertura_{total,por_regiao,por_municipio}.csv"""
    total = _cobertura(ok).to_frame('TOTAL_70_municipios').T                      # linha única, nomeada
    por_regiao = (ok.groupby('regiao').apply(_cobertura, include_groups=False)
                  .reindex(ORDEM_REGIAO).reset_index())                           # ordem fixa das regiões
    por_municipio = (ok.groupby(['CD_UF', 'CD_MUN', 'NM_MUN', 'regiao'])
                     .apply(_cobertura, include_groups=False).reset_index())
    return {'cobertura_total': total,
            'cobertura_por_regiao': por_regiao,
            'cobertura_por_municipio': por_municipio}


def tabela_saneamento_categorias(ok: pd.DataFrame) -> pd.DataFrame:
    """saneamento_categorias_por_regiao.csv — distribui os setores em 3 faixas de gravidade.

    Faixas: 0% (nenhum domicílio inadequado), 1–49% e 50%+. O denominador é o número de
    setores **com o indicador calculável** — setores sigilosos naquele indicador ficam
    fora da conta, e não empurram artificialmente a faixa de 0%.
    """
    linhas = []
    for rotulo, col in SANEAMENTO.items():
        for regiao in ORDEM_REGIAO:
            s = ok.loc[ok['regiao'] == regiao, col].dropna()
            n = len(s)
            linhas.append({
                'variavel': rotulo, 'regiao': regiao, 'n_setores': n,
                'pct_0':      round((s == 0).sum() / n * 100, 1),
                'pct_1_49':   round(((s > 0) & (s < 0.5)).sum() / n * 100, 1),
                'pct_50mais': round((s >= 0.5).sum() / n * 100, 1),
            })
    return pd.DataFrame(linhas)


def tabela_morfologia(ok: pd.DataFrame) -> pd.DataFrame:
    """morfologia_v00048_v00058_por_regiao.csv — tipo de espécie do domicílio, em domicílios.

    Diferente das outras tabelas da EDA, esta conta **domicílios**, não setores: o
    denominador é V00001 + V00002 (particulares permanentes ocupados + improvisados
    ocupados), que é o universo em que o IBGE classifica o tipo de espécie.
    """
    codigos = list(MORFOLOGIA)
    tabela = pd.DataFrame({'codigo': codigos, 'tipo': [MORFOLOGIA[c] for c in codigos]})

    den_total = ok[['V00001', 'V00002']].sum().sum()                       # domicílios dos 70 municípios
    tabela['total'] = [int(ok[c].sum()) for c in codigos]
    tabela['pct_total'] = (tabela['total'] / den_total * 100).round(3)

    for regiao in ORDEM_REGIAO:
        g = ok[ok['regiao'] == regiao]
        den = g[['V00001', 'V00002']].sum().sum()                          # denominador da própria região
        tabela[f'n_{regiao}'] = [int(g[c].sum()) for c in codigos]
        tabela[f'pct_{regiao}'] = (tabela[f'n_{regiao}'] / den * 100).round(3)
    return tabela


def tabelas_analfabetismo(ok: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """auditoria_analfabetismo_{municipio,v00900_bins}.csv — quanto o sigilo em V00901 pesa.

    V00901 (15+ que não sabem ler) é a variável mais suprimida da base: o IBGE sigila
    contagens pequenas, e analfabetos são poucos justamente nos setores ricos. As duas
    tabelas medem esse viés — por município e por porte do setor.
    """
    linhas = []
    for nm_mun, g in ok.groupby('NM_MUN'):
        pct = g['pct_analfab'].dropna() * 100                               # em pontos percentuais
        linhas.append({
            'NM_MUN': nm_mun,
            'n_setores': len(g),
            'n_sigilo': int(g['V00901'].isna().sum()),                      # setores com V00901 suprimida
            'pct_sigilo_v901': round(g['V00901'].isna().mean() * 100, 2),
            'n_v901_zero': int((g['V00901'] == 0).sum()),                   # setores com zero analfabetos declarados
            'n_validos': len(pct),
            'media_pct': round(pct.mean(), 2),
            'mediana_pct': round(pct.median(), 2),
            'max_pct': round(pct.max(), 2),
        })
    # desempate por nome: sem ele a ordem dos 11 municípios com sigilo 0% fica à mercê do
    # quicksort (instável) e a tabela muda de ordem a cada execução, sem mudar um número
    por_municipio = (pd.DataFrame(linhas)
                     .sort_values(['pct_sigilo_v901', 'NM_MUN'], ascending=[False, True], kind='stable')
                     .reset_index(drop=True))

    faixa = pd.cut(ok['V00900'], bins=BINS_V00900, labels=ROTULOS_V00900, right=True)  # porte do setor
    g = ok.groupby(faixa, observed=False)['V00901']
    bins = pd.DataFrame({
        'n_setores': g.size(),
        'n_v901_sigilo': g.apply(lambda s: int(s.isna().sum())),
        'n_v901_zero': g.apply(lambda s: int((s == 0).sum())),
        'media_v901': g.mean(),                                             # média entre os setores não sigilosos
    })
    bins['pct_sigilo'] = (bins['n_v901_sigilo'] / bins['n_setores'] * 100).round(2)
    bins = bins.reset_index().rename(columns={'V00900': 'v900_bin'})
    return {'auditoria_analfabetismo_municipio': por_municipio,
            'auditoria_analfabetismo_v00900_bins': bins}


def tabelas_resp_feminino(ok: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """resp_feminino_contagem_{por_regiao,por_municipio}.csv — em pessoas, não em setores.

    O Notebook 02 (seção 7d) resume `pct_resp_feminino` por setor. Estas tabelas somam os
    responsáveis (V01062 homens, V01063 mulheres) do território inteiro — é o número que
    vai no slide, e não é a média das proporções por setor.
    """
    def _contar(chaves: list[str]) -> pd.DataFrame:
        g = ok.groupby(chaves)
        # as somas são contagens de pessoas: viram inteiro (a soma vem float por causa do
        # sigilo em NaN, e sem o cast a tabela sai com '668426.0')
        t = pd.DataFrame({
            'n_setores': g.size(),
            'resp_feminino': g['V01063'].sum().astype('int64'),
            'resp_masculino': g['V01062'].sum().astype('int64'),
        })
        t['resp_total_sexo'] = t['resp_feminino'] + t['resp_masculino']
        t['pct_resp_feminino'] = (t['resp_feminino'] / t['resp_total_sexo'] * 100).round(2)
        return t.reset_index()

    por_regiao = _contar(['regiao']).set_index('regiao').reindex(ORDEM_REGIAO).reset_index()
    return {'resp_feminino_contagem_por_regiao': por_regiao,
            'resp_feminino_contagem_por_municipio': _contar(['CD_UF', 'CD_MUN', 'NM_MUN', 'regiao'])}


def main() -> None:
    raiz = encontrar_raiz(Path(__file__).resolve().parent)
    destino = raiz / 'banco_de_dados' / 'eda'
    ok = carregar_setores_ok(raiz)

    tabelas: dict[str, pd.DataFrame] = {}
    tabelas.update(tabelas_cobertura(ok))
    tabelas['saneamento_categorias_por_regiao'] = tabela_saneamento_categorias(ok)
    tabelas['morfologia_v00048_v00058_por_regiao'] = tabela_morfologia(ok)
    tabelas.update(tabelas_analfabetismo(ok))
    tabelas.update(tabelas_resp_feminino(ok))

    for nome, tabela in tabelas.items():
        # cobertura_total tem o nome do recorte no índice; as demais são tabelas planas
        indice = nome == 'cobertura_total'
        tabela.to_csv(destino / f'{nome}.csv', sep=';', index=indice, encoding='utf-8-sig')
        print(f'  {nome}.csv  ({len(tabela)} linhas)')
    print(f'\n{len(tabelas)} tabelas gravadas em {destino}')


if __name__ == '__main__':
    main()
