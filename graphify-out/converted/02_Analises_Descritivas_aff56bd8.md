# 02_Analises_Descritivas

> Notebook Jupyter convertido para markdown. Origem: `notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb`

# Fase 3 — Notebook 02: Análise Exploratória (EDA)

**Entrada:** `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` (produzido pelo Notebook 01).

**Objetivo:** caracterizar a base filtrada dos 70 municípios ELSI antes de qualquer
cálculo de IVS — descrever distribuições, detectar outliers, avaliar dados faltantes
e estudar a estrutura de correlação entre as 7 variáveis-componente do IVS. Esta EDA
alimenta a **Tabela 1** do artigo científico.

**Referência metodológica:**
- `docs/Cálculo IVS2012.docx` — regras operacionais do IVS-BH (denominador,
  `Dados_sig`, tratamento de sigilo).
- `docs/guia_analises.docx` — framework FIOCRUZ de EDA: medidas de tendência
  central (média / mediana / quantis), dispersão (DP / IQR / CV), gráficos
  (histograma, boxplot, matriz de correlação) e análise de missing.
- `dados/dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx` (IBGE) —
  definições oficiais das variáveis do Censo 2022.
- **Galvão, S. M. et al.** Envelhecimento populacional em Mato Grosso e sua relação com
  indicadores demográficos e econômicos. *Hygeia*, v. 21, e2106, 2025 — definições dos
  indicadores de envelhecimento (seção 7e).

**Decisões metodológicas adotadas nesta etapa (revisão de 2026-05-22):**

| Decisão | Antes | Agora | Justificativa |
|---|---|---|---|
| **Denominador domiciliar** | V01042 (responsáveis) | **V00001** (Dom. Particulares Permanentes Ocupados) | V01042 é uma contagem de PESSOAS no arquivo Parentesco. O padrão IVS-BH 2012 usa o equivalente do V002 (Dom_part_p) do Censo 2010 — que no 2022 corresponde a V00001. Confirmado pelo de-para da orientadora em `Relatorio_Metodologico_IVS_2022_Corrigido.xlsx`. |
| **Taxa de analfabetismo** | V00901 / V00900 | **V00901 / (V00900 + V00901)** | V00900 = 15+ que SABEM ler/escrever; V00901 = 15+ que NÃO sabem. O denominador correto da taxa é o total de pessoas com 15+ anos, soma das duas. |
| **Razão de moradores** | (V00005+V00006) / V01042 | **(V00005+V00006) / (V00001+V00002)** | Reproduz a definição oficial do V0005 do IBGE (média de moradores em Dom. Particulares Ocupados = pessoas / DPPO+DPIO). |

**Revisão de 2026-08-09 — demandas da orientadora:**

| Seção | Mudança | Demanda atendida |
|---|---|---|
| 3 | `Dados_sig`: `ZERADO` passa a ser avaliado antes de `SIGILOSO` (os 78 setores de massa d'água deixam de ser contados como sigilo) | consistência |
| **3b (nova)** | **Exclusão dos setores rurais** com tabela de conferência por município e região | *"excluir setores rurais, conferir com a porcentagem"* |
| 7e | **Índice de envelhecimento corrigido**: denominador passa de 0–4 para **menores de 15 anos**; acrescentados RDI e % 60+ | *"ajustar índice de envelhecimento (ler artigo)"* |
| **7f (nova)** | Agrupamento de **moradias convencionais** e **indicador de apartamento** | *"agrupar moradias normais"* + *"criar um indicador de apartamento"* |
| **7g (nova)** | Contagem de **setores de vilas e favelas (FCU)** e comparação de indicadores | *"quantos setores são de vilas e favelas"* |

> **Atenção ao recorte:** a partir da seção 3b, `df_ok` contém **apenas setores urbanos**.
> Todas as descritivas, correlações e figuras das seções 4 em diante referem-se a esse
> conjunto. O objeto `df_ok_com_rural` preserva o conjunto elegível anterior ao filtro.

**Roteiro:**
1. Imports e carregamento.
2. Tipagem e tratamento de sigilo (`X` → `NaN`).
3. Classificação `Dados_sig` e filtro dos setores `OK`.
   - 3b. Recorte urbano — exclusão dos setores rurais.
4. Cálculo das 7 proporções brutas (sem normalização).
5. Descritivas globais.
6. Descritivas por município.
7. Descritivas por região.
   - 7b. Habitação precária · 7c. Inadequação de banheiro · 7d. Responsável do sexo feminino
   - 7e. Indicadores de envelhecimento · 7f. Tipo de domicílio · 7g. Vilas e favelas (FCU)
8. Distribuições — histogramas.
9. Distribuições — boxplots por região.
10. Análise de outliers (regra IQR).
11. Análise de dados faltantes.
12. Matriz de correlação (Pearson e Spearman).
13. Exportação dos artefatos.

## 1. Imports e carregamento da base filtrada

### Célula de código: `step1`

```python
# ── Imports ───────────────────────────────────────────────────────────────────
import os                          # caminhos e criação de pastas
import numpy as np                 # operações numéricas (NaN, arrays, divisão segura)
import pandas as pd                # DataFrames (núcleo da análise)
import matplotlib.pyplot as plt    # gráficos (histogramas, boxplots, mapas de calor)
from pathlib import Path           # caminhos como objetos

pd.set_option('display.max_columns', 50)   # ao imprimir, mostra até 50 colunas (em vez de truncar)
pd.set_option('display.width', 200)        # largura da saída no console (evita quebrar tabelas)


def _find_project_root():
    """Detecta a raiz do projeto (independente de onde o Jupyter inicia o kernel)."""
    cwd = Path.cwd().resolve()              # diretório atual, absoluto
    for d in [cwd, *cwd.parents]:           # sobe a árvore de diretórios
        if (d / 'requirements.txt').is_file() and (d / 'dados').is_dir() and (d / 'docs').is_dir():  # marca da raiz
            return d
    raise RuntimeError(f'Raiz do projeto não encontrada a partir de: {cwd}')

ROOT = _find_project_root()                                    # raiz do projeto
CAMINHO_BD  = str(ROOT / 'banco_de_dados') + os.sep            # pasta com a base bruta (entrada deste notebook)
CAMINHO_EDA = str(ROOT / 'banco_de_dados' / 'eda') + os.sep    # pasta de saída dos CSVs da EDA
CAMINHO_FIG = str(ROOT / 'banco_de_dados' / 'eda' / 'figuras') + os.sep  # pasta de saída das figuras (.png)
os.makedirs(CAMINHO_EDA, exist_ok=True)    # cria a pasta de CSVs se não existir
os.makedirs(CAMINHO_FIG, exist_ok=True)    # cria a pasta de figuras se não existir
print(f'Raiz do projeto: {ROOT}')          # log

# carrega a base bruta do Notebook 01; dtype=str = tudo como texto (preserva 'X' do sigilo e zeros à esquerda)
df = pd.read_csv(CAMINHO_BD + 'Base_ELSI_Bruta_Censo2022.csv', sep=';', dtype=str)
print(f'Base carregada: {len(df):,} setores × {len(df.columns)} colunas')  # log: dimensões
print(f'Municípios distintos: {df["CD_MUN"].nunique()}')                    # log: deve ser 70
print(f'UFs distintas: {df["CD_UF"].nunique()}')                            # log: nº de UFs representadas
```

## 2. Tipagem e tratamento de sigilo

O IBGE marca células sigilosas com `X`. Para a EDA, convertemos `X` em `NaN` (as
estatísticas descritivas pulam essas observações). A classificação `Dados_sig` da
próxima célula decide quais setores ficam fora da análise.

### Célula de código: `step2`

```python
# Colunas que são TEXTO (identificação) e não devem virar número.
# CD_SIT/CD_TIPO/CD_FCU/NM_FCU são códigos de classificação territorial (não contagens):
# entram aqui para não serem convertidos em número na conversão abaixo.
COLS_TEXTO = ['CD_SETOR', 'CD_UF', 'CD_MUN', 'NM_MUN', 'NM_BAIRRO',
              'SITUACAO', 'CD_SIT', 'CD_TIPO', 'CD_FCU', 'NM_FCU',
              'Moradia_Predominante']
cols_num = [c for c in df.columns if c not in COLS_TEXTO]  # todas as demais colunas = numéricas (variáveis V…)

# Marca sigilo ('X') como NaN.
df[cols_num] = df[cols_num].replace({'X': None, 'x': None})  # troca o marcador de sigilo do IBGE por nulo (None -> NaN)

# Algumas colunas (notadamente V06004 — rendimento médio) usam vírgula como
# separador decimal ('2453,03' em vez de '2453.03'). Trocamos antes de
# converter para numérico, senão pd.to_numeric devolve NaN para a maioria.
df[cols_num] = df[cols_num].apply(
    lambda c: c.astype(str).str.replace(',', '.', regex=False)  # em cada coluna: troca ',' por '.' (decimal padrão Python)
)
df[cols_num] = df[cols_num].apply(pd.to_numeric, errors='coerce')  # converte p/ número; o que não der vira NaN (errors='coerce')

print('Tipos após conversão:')                                                  # log
print(df[cols_num[:5]].dtypes.to_string())                                       # mostra o tipo das 5 primeiras colunas numéricas
print(f"\nTotal de células nulas (incluindo sigilo): {df[cols_num].isna().sum().sum():,}")  # total de NaN na base
print(f"V06004 (renda média) — válidos: {df['V06004'].notna().sum():,}/{len(df):,}")        # confere o conserto da vírgula decimal
print(f"Colunas de classificação territorial preservadas como texto: "                      # confere que os códigos não viraram número
      f"{[c for c in ['CD_SIT', 'CD_TIPO', 'CD_FCU', 'NM_FCU'] if c in df.columns]}")
```

## 3. Classificação `Dados_sig` e filtro de setores elegíveis

Regras inspiradas no `Cálculo IVS2012.docx` (seção *Tratamento dos dados*), agora
ancoradas no denominador padrão **V00001** (Dom. Particulares Permanentes Ocupados):

- **SIGILOSO** — alguma das variáveis-base (`v0001`, `V00001`) está sigilosa (`NaN`).
- **COLETIVO** — setor sem domicílios particulares permanentes (`V00001 == 0` mas
  população `v0001 > 0`): toda a população reside em coletivos (asilos, presídios,
  alojamentos). Esses setores não admitem cálculo das proporções domiciliares.
- **ZERADO** — `v0001 == 0` (setor sem população).
- **OK** — caso contrário; participa das análises.

### Célula de código: `step3`

```python
# Regra Dados_sig — revisada em 2026-05-22; ordem das condições corrigida em 2026-08-09.
# Ancorada em V00001 (Domicílios Particulares Permanentes Ocupados), que é o
# denominador padrão do IVS-BH 2012 (equivalente ao V002 do Domicilio01 do Censo
# 2010, conforme dicionário oficial IBGE).
#
# Definições:
#  • ZERADO   — v0001 == 0 (setor sem população residente).
#  • SIGILOSO — v0001 ou V00001 estão como sigilo (NaN).
#  • COLETIVO — V00001 == 0 com v0001 > 0 (toda a população em domicílios coletivos:
#               asilos, presídios, alojamentos). Cálculo de proporções domiciliares
#               é indefinido nesses setores.
#  • OK       — caso contrário; participa das análises.
#
# CORREÇÃO DE 09/08/2026 — ZERADO passou a ser avaliado ANTES de SIGILOSO.
# Motivo: os 78 setores do recorte ELSI com CD_SIT = 9 (massas d'água) têm
# v0001 = 0 e V00001 vazio. Como o sigilo era testado primeiro, eles eram rotulados
# SIGILOSO — isto é, contados como "dado suprimido pelo IBGE" quando na verdade são
# setores sem população. Nenhum setor OK muda de classe com esta correção; ela só
# deixa de inflar a contagem de sigilo.

cond_sig    = df[['v0001', 'V00001']].isna().any(axis=1)        # True se v0001 OU V00001 for NaN (sigiloso)
cond_zerado = df['v0001'].fillna(-1) == 0                       # True se população == 0 (fillna(-1) evita que NaN conte como 0)
cond_col    = (df['V00001'].fillna(-1) == 0) & ~cond_zerado     # True se não há domicílios (V00001==0) MAS há população (não zerado)

df['Dados_sig'] = np.select(                                    # np.select: aplica a 1ª condição verdadeira, na ordem
    [cond_zerado, cond_sig, cond_col],                          # ordem importa: população zero primeiro, depois sigilo, depois coletivo
    ['ZERADO', 'SIGILOSO', 'COLETIVO'],                         # rótulo correspondente a cada condição
    default='OK',                                              # se nenhuma bateu, o setor é elegível ('OK')
)

resumo = df['Dados_sig'].value_counts().rename('n_setores').to_frame()  # conta setores por classe e vira DataFrame
resumo['pct'] = (resumo['n_setores'] / len(df) * 100).round(2)          # adiciona a coluna de percentual
print('Elegibilidade dos setores (70 municípios ELSI):')                # log
print(resumo.to_string())                                               # mostra a tabela de elegibilidade

# Conferência da correção: os setores ZERADO devem coincidir com CD_SIT = 9 (massas d'água)
if 'CD_SIT' in df.columns:                                              # a coluna só existe nas bases geradas a partir de 09/08/2026
    print('\nDados_sig × CD_SIT (confere o reenquadramento das massas d\'água):')
    print(pd.crosstab(df['Dados_sig'], df['CD_SIT']).to_string())

df_ok = df[df['Dados_sig'] == 'OK'].copy()                     # df_ok = apenas os setores elegíveis; .copy() = cópia independente
print(f'\nSetores OK para análise: {len(df_ok):,}')            # log: quantos sobraram
print(f'Municípios representados: {df_ok["CD_MUN"].nunique()}')  # log: quantos municípios ainda têm pelo menos 1 setor OK
```

## 3b. Recorte urbano — exclusão dos setores rurais

**Demanda da orientadora (jul/2026):** *"excluir setores rurais, conferir com a
porcentagem"*.

O IVS é, por definição, um índice **intraurbano** — compara setores *dentro* de cada
cidade. Setores rurais entram na base porque o recorte é municipal (o município inteiro
dos 70 do ELSI), mas não pertencem ao objeto de análise: são áreas de baixa densidade,
com padrões de saneamento e morfologia que não se comparam aos urbanos e que puxariam
artificialmente a cauda alta de vulnerabilidade.

**Onde o filtro é aplicado:** aqui, no notebook de análise — **não** na extração. A base
bruta (`Base_ELSI_Bruta_Censo2022.csv`) continua com os 109.032 setores, o que mantém a
exclusão auditável e reversível: a tabela de conferência abaixo mostra exatamente quanto
saiu, por município e por região.

**Critério:** `SITUACAO == 'Urbana'`, equivalente a `CD_SIT ∈ {1, 2, 3}`.

| `CD_SIT` | Situação | Entra na análise? |
|---|---|---|
| 1, 2, 3 | Urbana | ✅ sim |
| 5, 6, 7, 8 | Rural (povoado, núcleo, lugarejo, área rural) | ❌ não |
| 9 | Massa d'água — `v0001 = 0` | ❌ não (já excluído como `ZERADO`) |

A partir desta célula, **`df_ok` contém apenas setores urbanos elegíveis**. O conjunto
anterior fica preservado em `df_ok_com_rural` para as comparações desta seção.

### Célula de código: `filtro-urbano`

```python
# ── Mapa UF -> região (usado nesta seção e reaproveitado nas seguintes) ───────
df_elsi_ref = pd.read_csv(str(ROOT / 'dados' / 'municipios_elsi_brasil.csv'), sep=';', dtype=str)  # lista oficial dos 70 municípios
mapa_regiao = dict(zip(df_elsi_ref['uf_codigo'].str.zfill(2), df_elsi_ref['regiao']))              # {'31': 'Sudeste', ...}
df['regiao'] = df['CD_UF'].map(mapa_regiao)                                                        # região em TODA a base
df_ok['regiao'] = df_ok['CD_UF'].map(mapa_regiao)                                                  # região no conjunto elegível
ORDEM_REGIAO = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']                             # ordem fixa p/ tabelas e gráficos


def _tabela_situacao(g):
    """Composição urbano/rural de um grupo de setores, em setores E em domicílios (V00001)."""
    urb = g['SITUACAO'].eq('Urbana')                       # máscara dos setores urbanos
    rur = g['SITUACAO'].eq('Rural')                        # máscara dos setores rurais
    sem = g['SITUACAO'].isna()                             # setores sem SITUACAO (CD_SIT = 9, massas d'água)
    n = len(g)                                             # total de setores do grupo
    return pd.Series({
        'n_setores':    n,                                 # total de setores
        'set_urbana':   int(urb.sum()),                    # nº de setores urbanos
        'dom_urbana':   g.loc[urb, 'V00001'].sum(),        # domicílios (V00001) nos setores urbanos
        'set_rural':    int(rur.sum()),                    # nº de setores rurais
        'dom_rural':    g.loc[rur, 'V00001'].sum(),        # domicílios nos setores rurais
        'set_sem':      int(sem.sum()),                    # nº de setores sem SITUACAO
        'dom_sem':      g.loc[sem, 'V00001'].sum(),        # domicílios neles (esperado: 0)
        'pct_set_urbana': round(urb.sum() / n * 100, 2) if n else np.nan,   # % de setores urbanos
        'pct_set_rural':  round(rur.sum() / n * 100, 2) if n else np.nan,   # % de setores rurais
    })


# ---- Composição urbano/rural sobre TODA a base (109.032 setores) ----
sit_total = _tabela_situacao(df).to_frame('TOTAL_70_municipios').T                       # linha única com o total
sit_reg = (df.groupby('regiao').apply(_tabela_situacao, include_groups=False)            # uma linha por região
           .reindex(ORDEM_REGIAO).reset_index())
sit_mun = (df.groupby(['CD_UF', 'CD_MUN', 'NM_MUN', 'regiao']).apply(_tabela_situacao, include_groups=False)  # uma linha por município
           .reset_index().sort_values(['CD_UF', 'NM_MUN']))

print('Composição urbano/rural — 70 municípios ELSI (todos os 109.032 setores):')        # log
print(sit_total.to_string())
print('\nPor região:')
print(sit_reg.to_string(index=False))

# ---- Conferência do que o filtro remove do conjunto ELEGÍVEL (Dados_sig == OK) ----
df_ok_com_rural = df_ok.copy()                                     # guarda o conjunto elegível ANTES do recorte urbano
mask_urbano = df_ok['SITUACAO'].eq('Urbana')                       # máscara: só setores urbanos

conf_mun = (df_ok_com_rural.assign(_urb=mask_urbano.astype(int))   # tabela de conferência por município
            .groupby(['CD_UF', 'CD_MUN', 'NM_MUN', 'regiao'])
            .agg(n_ok_total=('_urb', 'size'), n_ok_urbano=('_urb', 'sum'))
            .reset_index())
conf_mun['n_ok_rural'] = conf_mun['n_ok_total'] - conf_mun['n_ok_urbano']                          # quantos saem
conf_mun['pct_excluido'] = (conf_mun['n_ok_rural'] / conf_mun['n_ok_total'] * 100).round(2)        # % excluído do município
conf_mun = conf_mun.sort_values('pct_excluido', ascending=False).reset_index(drop=True)            # os mais afetados primeiro

n_antes, n_depois = len(df_ok), int(mask_urbano.sum())             # tamanho antes e depois do recorte
print(f'\n--- Recorte urbano aplicado ao conjunto elegível ---')   # log
print(f'  Setores OK antes do filtro:  {n_antes:,}')
print(f'  Setores OK urbanos (mantidos): {n_depois:,} ({n_depois / n_antes * 100:.2f}%)')
print(f'  Setores OK rurais (excluídos): {n_antes - n_depois:,} ({(n_antes - n_depois) / n_antes * 100:.2f}%)')
print(f'  Municípios que perdem mais de 10% dos setores: {int((conf_mun["pct_excluido"] > 10).sum())}')
print('\n10 municípios mais afetados pela exclusão:')
print(conf_mun.head(10).to_string(index=False))

# ---- APLICA o filtro: daqui para frente, df_ok é urbano ----
df_ok = df_ok[mask_urbano].copy()                                  # substitui df_ok pelo subconjunto urbano
print(f'\nConjunto de análise final: {len(df_ok):,} setores urbanos elegíveis '
      f'em {df_ok["CD_MUN"].nunique()} municípios.')

# ---- Exporta as tabelas de conferência ----
sit_total.to_csv(CAMINHO_EDA + 'situacao_urbano_rural_total.csv', sep=';', encoding='utf-8-sig')                    # total
sit_reg.to_csv(CAMINHO_EDA + 'situacao_urbano_rural_por_regiao.csv', sep=';', index=False, encoding='utf-8-sig')    # por região
sit_mun.to_csv(CAMINHO_EDA + 'situacao_urbano_rural_por_municipio.csv', sep=';', index=False, encoding='utf-8-sig')  # por município
conf_mun.to_csv(CAMINHO_EDA + 'exclusao_rural_conferencia.csv', sep=';', index=False, encoding='utf-8-sig')          # o que o filtro removeu
print('\nArtefatos exportados: situacao_urbano_rural_{total,por_regiao,por_municipio}.csv, exclusao_rural_conferencia.csv')
```

## 4. Cálculo das 7 proporções brutas (sem normalização)

Para a EDA usamos as **proporções brutas** dos componentes do IVS — a normalização
min-max só faz sentido depois, na construção do índice. Denominadores alinhados ao
padrão IVS-BH 2012 / de-para oficial da orientadora:

| Variável | Numerador | Denominador |
|---|---|---|
| `pct_agua_inad` | V00112 + V00113 + V00114 + V00115 + V00116 + V00117 + V00118 | **V00001** |
| `pct_esgoto_inad` | V00312 + V00313 + V00314 + V00315 + V00316 | **V00001** |
| `pct_lixo_inad` | V00398 + V00399 + V00400 + V00401 + V00402 | **V00001** |
| `razao_moradores` | V00005 + V00006 | **V00001 + V00002** *(reproduz V0005 do IBGE)* |
| `pct_analfab` | V00901 | **V00900 + V00901** *(total de pessoas com 15+ anos)* |
| `renda_media` | V06004 (direto, sem denominador) | — |
| `pct_raca_pretpardind` | V01318 + V01320 + V01321 | **v0001** (pop. total) |

**Tratamento de sigilo (decisão para EDA):** se *todas* as variáveis-numerador de
um indicador estão sigilosas (`NaN`), o indicador vira `NaN` também — não zero.
Isto preserva a transparência sobre dados faltantes nas tabelas descritivas e nos
mapas de missing. Implementado via `sum(axis=1, min_count=1)`.

Para `pct_analfab`, V00901 está sigilosa em ~16% dos setores ELSI. A decisão é
**manter NaN** nesses setores (não imputar zero), expondo claramente a perda de N
no relatório descritivo. Em contraste com a Fase 2 (que convertia sigilo residual
para zero, apropriado para o cálculo final do índice).

### Célula de código: `step4`

```python
def safe_div(num, den):
    # Divide com segurança: evita o RuntimeWarning de divisão por zero/NaN
    # calculando o quociente apenas onde den > 0 (resultado idêntico ao anterior).
    num = np.asarray(num, dtype=float)         # converte o numerador p/ array de float
    den = np.asarray(den, dtype=float)         # converte o denominador p/ array de float
    out = np.full(num.shape, np.nan)           # cria um array do mesmo tamanho preenchido com NaN (resultado padrão)
    np.divide(num, den, out=out, where=den > 0)  # divide só nas posições onde den > 0; o resto permanece NaN
    return out                                 # devolve o array de proporções

agua_cols   = ['V00112', 'V00113', 'V00114', 'V00115', 'V00116', 'V00117', 'V00118']  # formas de água inadequada
esgoto_cols = ['V00312', 'V00313', 'V00314', 'V00315', 'V00316']                        # formas de esgoto inadequado
# NB: V00398 ("Lixo depositado em cacamba de servico de limpeza") e INCLUIDO de
# proposito. O IVS-BH 2012 (docs/Calculo IVS2012.docx, Tabela 3 = V037 no Censo 2010)
# conta a cacamba como lixo INADEQUADO; so a coleta porta-a-porta (V00397) e adequada.
# NAO remover V00398 sem decisao metodologica explicita (verificado em 18/06/2026).
lixo_cols   = ['V00398', 'V00399', 'V00400', 'V00401', 'V00402']  # formas de destino inadequado do lixo
raca_cols   = ['V01318', 'V01320', 'V01321']                      # cor/raça: preta + parda + indígena (PPI)

# Denominador padrão IVS-BH 2012: V00001 (Dom. Particulares Permanentes Ocupados).
# min_count=1 → se TODAS as parcelas estiverem sigilosas (NaN), a soma vira NaN
# (em vez do default 0). Isto preserva o sigilo nas proporções.
df_ok['pct_agua_inad']   = safe_div(df_ok[agua_cols].sum(axis=1, min_count=1),   df_ok['V00001'])  # % domicílios c/ água inadequada
df_ok['pct_esgoto_inad'] = safe_div(df_ok[esgoto_cols].sum(axis=1, min_count=1), df_ok['V00001'])  # % domicílios c/ esgoto inadequado
df_ok['pct_lixo_inad']   = safe_div(df_ok[lixo_cols].sum(axis=1, min_count=1),   df_ok['V00001'])  # % domicílios c/ lixo inadequado

# Razão de moradores = (moradores em DPP Ocupados + moradores em DPI Ocupados)
# dividido por (DPP Ocupados + DPI Ocupados). Reproduz V0005 do IBGE.
df_ok['razao_moradores'] = safe_div(
    df_ok[['V00005', 'V00006']].sum(axis=1, min_count=1),       # numerador: total de moradores (permanentes + improvisados)
    df_ok[['V00001', 'V00002']].sum(axis=1, min_count=1),       # denominador: total de domicílios ocupados (permanentes + improvisados)
)

# Taxa de analfabetismo = V00901 / (V00900 + V00901). Sigilo em V00901 mantém NaN
# (não imputamos zero).
denom_alfab = df_ok[['V00900', 'V00901']].sum(axis=1, min_count=2)  # min_count=2 → ambas precisam estar presentes
df_ok['pct_analfab'] = safe_div(df_ok['V00901'], denom_alfab)       # analfabetos / total de pessoas 15+

df_ok['renda_media']          = df_ok['V06004']                                                    # renda: usa V06004 direto (já é uma média em R$)
df_ok['pct_raca_pretpardind'] = safe_div(df_ok[raca_cols].sum(axis=1, min_count=1), df_ok['v0001'])  # % PPI sobre a população total

INDICADORES = ['pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad',   # lista dos 7 indicadores-componente do IVS
               'razao_moradores', 'pct_analfab', 'renda_media',
               'pct_raca_pretpardind']

# ---- C1 — Diagnóstico de proporções fora de [0, 1] ANTES do clipping ----
print('Diagnóstico de proporções fora de [0, 1] (antes do clipping):')
diag = []                                                # acumula uma linha de diagnóstico por indicador de proporção
for c in [x for x in INDICADORES if x.startswith('pct_')]:  # percorre só os indicadores que são proporção (pct_*)
    n_acima  = int((df_ok[c] > 1).sum())                 # quantos setores têm proporção > 1 (impossível: indica erro de dado)
    n_abaixo = int((df_ok[c] < 0).sum())                 # quantos têm proporção < 0 (impossível)
    n_validos = int(df_ok[c].notna().sum())              # quantos têm valor calculável (não-NaN)
    maximo = df_ok[c].max()                              # valor máximo observado (antes de cortar)
    diag.append({'variavel': c, 'n_validos': n_validos, 'n_>1': n_acima,  # guarda os números num dicionário
                 'n_<0': n_abaixo, 'max_bruto': round(maximo, 4)})
diag_df = pd.DataFrame(diag)                             # vira tabela
print(diag_df.to_string(index=False))                   # imprime o diagnóstico

diag_df.to_csv(CAMINHO_EDA + 'diagnostico_proporcoes_fora_intervalo.csv',  # exporta o diagnóstico p/ auditoria
               sep=';', index=False, encoding='utf-8-sig')

# Clipping mantido (necessário para que a EDA produza distribuições válidas em
# [0,1]), com diagnóstico transparente acima.
for c in [x for x in INDICADORES if x.startswith('pct_')]:  # para cada proporção...
    df_ok[c] = df_ok[c].clip(lower=0, upper=1)              # ...força o valor a ficar entre 0 e 1 (corta eventuais extrapolações)

# ---- R4 — inspeção de razao_moradores em extremos ----
extremos_razao = pd.concat([                             # junta os 5 menores e os 5 maiores valores de razao_moradores
    df_ok.nsmallest(5, 'razao_moradores')[['CD_SETOR','NM_MUN','NM_BAIRRO',   # 5 menores + colunas p/ auditar o cálculo
                                           'V00001','V00002','V00005','V00006','razao_moradores']],
    df_ok.nlargest(5,  'razao_moradores')[['CD_SETOR','NM_MUN','NM_BAIRRO',   # 5 maiores
                                           'V00001','V00002','V00005','V00006','razao_moradores']],
])
print('\n5 menores e 5 maiores razao_moradores (auditoria — possíveis denominadores incorretos):')
print(extremos_razao.to_string(index=False))            # imprime os extremos p/ inspeção visual
extremos_razao.to_csv(CAMINHO_EDA + 'extremos_razao_moradores.csv',  # exporta os extremos
                       sep=';', index=False, encoding='utf-8-sig')

# ---- Auditoria adicional do analfabetismo (cobertura) ----
n_total = len(df_ok)                                                       # total de setores OK
n_v900_ok = int(df_ok['V00900'].notna().sum())                            # quantos têm V00900 (alfabetizados) preenchido
n_v901_ok = int(df_ok['V00901'].notna().sum())                            # quantos têm V00901 (analfabetos) preenchido
n_ambos   = int((df_ok['V00900'].notna() & df_ok['V00901'].notna()).sum())  # quantos têm AS DUAS preenchidas
n_pct_validos = int(df_ok['pct_analfab'].notna().sum())                   # quantos têm a taxa calculável
print(f'\nCobertura analfabetismo (sigilo do IBGE):')                      # log
print(f'  V00900 não-nulo: {n_v900_ok:,} / {n_total:,}  ({n_v900_ok/n_total*100:.2f}%)')
print(f'  V00901 não-nulo: {n_v901_ok:,} / {n_total:,}  ({n_v901_ok/n_total*100:.2f}%)')
print(f'  AMBAS não-nulas: {n_ambos:,} / {n_total:,}  ({n_ambos/n_total*100:.2f}%)')
print(f'  pct_analfab calculável: {n_pct_validos:,} / {n_total:,}  ({n_pct_validos/n_total*100:.2f}%)')

print('\nProporções calculadas. Resumo rápido:')          # log
print(df_ok[INDICADORES].describe().round(4).to_string())  # estatísticas-resumo rápidas dos 7 indicadores
```

## 4b. (Diagnóstico) Confirmação das variáveis de esgoto

O Relatório Metodológico legado tinha uma inconsistência: a aba *De_Para* indicava
**V00312–V00316** e a aba *Mapa_de_Arquivos* indicava **V00249–V00253**. Com o
dicionário oficial do IBGE em mãos
(`dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx`) a questão
está resolvida:

- **V00312–V00316** = "Destinação do esgoto do banheiro ou sanitário..." — é o
  bloco correto para o componente *Esgoto inadequado*.
- **V00249–V00253** = "Tipo de espécie é casa de vila ou em condomínio, banheiros..." —
  bloco de tipologia de habitação, **não tem relação direta com esgoto**.

A célula abaixo mantém a comparação empírica para registro: confirma que a faixa
V00249–V00253 não estoura V00001 mas representa um conceito diferente, e que
V00312–V00316 produz proporções coerentes em [0, 1] sobre V00001 (denominador
adotado).

### Célula de código: `step4b`

```python
# Comparação empírica das duas faixas (mantida para registro).
# A faixa V00249–V00253 vem do arquivo domicilio2; precisa ser relida porque o
# Notebook 01 não a extrai (não é necessária para os cálculos do IVS).

CAMINHO_DADOS = str(ROOT / 'dados') + os.sep              # caminho da pasta de dados brutos (p/ reler o arquivo de domicílio2)
setores_elsi = set(df['CD_SETOR'].astype(str))           # conjunto de setores ELSI (p/ filtrar a releitura)

cols_alt = ['setor', 'V00249', 'V00250', 'V00251', 'V00252', 'V00253']  # bloco alternativo (a investigar)
pedacos = []                                             # acumula os chunks filtrados
for enc in ('utf-8', 'latin1'):                          # tenta cada encoding
    try:
        reader = pd.read_csv(                            # leitura em chunks (arquivo grande)
            CAMINHO_DADOS + 'Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv',
            sep=';', dtype=str, usecols=cols_alt,
            encoding=enc, chunksize=100_000, low_memory=False,
        )
        for chunk in reader:                             # processa pedaço a pedaço
            chunk = chunk.rename(columns={'setor': 'CD_SETOR'})   # padroniza a chave do setor
            chunk = chunk[chunk['CD_SETOR'].isin(setores_elsi)]   # mantém só setores ELSI
            if len(chunk):
                pedacos.append(chunk)
        break                                            # leitura OK: sai do loop de encodings
    except UnicodeDecodeError:
        continue                                         # encoding falhou: tenta o próximo
df_esg_alt = pd.concat(pedacos, ignore_index=True)       # junta todos os pedaços
df_esg_alt[['V00249','V00250','V00251','V00252','V00253']] = (   # converte o bloco alternativo p/ número
    df_esg_alt[['V00249','V00250','V00251','V00252','V00253']]
        .replace({'X': None, 'x': None})                 # sigilo -> NaN
        .apply(pd.to_numeric, errors='coerce')           # texto -> número
)
df_esg_alt['soma_249_253'] = df_esg_alt[['V00249','V00250','V00251','V00252','V00253']].sum(axis=1, min_count=1)  # soma por setor

# Aliar à base OK — denominador de referência agora é V00001
df_cmp = df_ok[['CD_SETOR', 'V00001'] + esgoto_cols].copy()       # recorta a base OK c/ o bloco oficial de esgoto
df_cmp['soma_312_316'] = df_cmp[esgoto_cols].sum(axis=1, min_count=1)  # soma do bloco oficial (V00312–V00316)
df_cmp = df_cmp.merge(df_esg_alt[['CD_SETOR', 'soma_249_253']], on='CD_SETOR', how='left')  # traz a soma do bloco alternativo

print('Comparação das duas faixas de esgoto (setores OK):')      # log
print(pd.DataFrame({                                             # compara as distribuições (describe) das duas somas e do denominador
    'soma_249_253 (somatório por setor)': df_cmp['soma_249_253'].describe(),
    'soma_312_316 (somatório por setor)': df_cmp['soma_312_316'].describe(),
    'V00001 (denominador adotado)':       df_cmp['V00001'].describe(),
}).round(2).to_string())

# Qual faixa "estoura" o denominador V00001?
n_estoura_312 = int((df_cmp['soma_312_316'] > df_cmp['V00001']).sum())  # nº de setores em que o bloco oficial passa do denominador
n_estoura_249 = int((df_cmp['soma_249_253'] > df_cmp['V00001']).sum())  # idem p/ o bloco alternativo (sinal de incompatibilidade)
print(f'\nSetores em que a soma > V00001:')
print(f'  V00312–V00316: {n_estoura_312:,}  ({n_estoura_312/len(df_cmp)*100:.2f}%)')
print(f'  V00249–V00253: {n_estoura_249:,}  ({n_estoura_249/len(df_cmp)*100:.2f}%)')

# Diferença setor a setor
df_cmp['diff'] = df_cmp['soma_249_253'] - df_cmp['soma_312_316']  # diferença entre as duas somas por setor
n_249_maior = int((df_cmp['diff'] > 0).sum())                    # em quantos setores o alternativo é maior
n_312_maior = int((df_cmp['diff'] < 0).sum())                    # em quantos o oficial é maior
n_iguais    = int((df_cmp['diff'] == 0).sum())                   # em quantos são iguais
print(f'\nRelação setor a setor (V00249-253 vs V00312-316):')
print(f'  V00249-253 > V00312-316: {n_249_maior:,}')
print(f'  V00312-316 > V00249-253: {n_312_maior:,}')
print(f'  iguais:                   {n_iguais:,}')

df_cmp[['CD_SETOR', 'V00001', 'soma_312_316', 'soma_249_253', 'diff']].to_csv(  # exporta o diagnóstico de esgoto
    CAMINHO_EDA + 'diagnostico_esgoto_312_vs_249.csv',
    sep=';', index=False, encoding='utf-8-sig',
)
print('\nArquivo salvo: banco_de_dados/eda/diagnostico_esgoto_312_vs_249.csv')   # log
print('Decisão metodológica: V00312–V00316 é o bloco correto (conforme dicionário oficial IBGE).')  # conclusão
```

## 5. Descritivas globais das 7 variáveis

Tabela síntese seguindo o guia FIOCRUZ (Seções 3 e 4): n, média, DP, CV, mínimo,
quartis, máximo, IQR, assimetria e curtose. Para o artigo, o par **(mediana, IQR)**
é mais robusto que **(média, DP)** quando há assimetria/outliers — calculamos os
dois para escolher na hora da redação.

### Célula de código: `step5`

```python
def descritiva(s):                              # calcula um conjunto de estatísticas-resumo para uma série (coluna)
    s = s.dropna()                              # remove NaN (estatísticas devem ignorar dados faltantes)
    if len(s) == 0:                             # se a série ficou vazia (tudo NaN)...
        return pd.Series({k: np.nan for k in    # ...devolve todas as estatísticas como NaN (evita erro)
            ['n','media','dp','cv_pct','min','p25','mediana','p75','max','iq','assim','curt']})
    mean = s.mean()                             # média (guardada à parte p/ reaproveitar no CV)
    return pd.Series({
        'n': int(len(s)),                       # nº de observações válidas
        'media':   mean,                        # média aritmética
        'dp':      s.std(),                     # desvio-padrão (dispersão)
        'cv_pct':  (s.std() / mean * 100) if mean != 0 else np.nan,  # coeficiente de variação (%) = DP/média; NaN se média=0
        'min':     s.min(),                     # valor mínimo
        'p25':     s.quantile(0.25),            # 1º quartil (percentil 25)
        'mediana': s.median(),                  # mediana (percentil 50)
        'p75':     s.quantile(0.75),            # 3º quartil (percentil 75)
        'max':     s.max(),                     # valor máximo
        'iq':      s.quantile(0.75) - s.quantile(0.25),  # intervalo interquartil (IQR = P75 - P25)
        'assim':   s.skew(),                    # assimetria (>0 = cauda à direita)
        'curt':    s.kurtosis(),                # curtose (achatamento; >0 = caudas pesadas)
    })

desc_global = pd.DataFrame({c: descritiva(df_ok[c]) for c in INDICADORES}).T  # aplica a cada indicador e transpõe (1 linha por variável)
desc_global = desc_global.round(4)                                            # arredonda p/ 4 casas
print('Descritivas globais (setores OK dos 70 municípios ELSI):\n')           # log
print(desc_global.to_string())                                                # imprime a tabela de descritivas globais
```

## 6. Descritivas por município

Tabela longa com, para cada município e variável: `n`, média, DP, mediana, P25, P75.
Útil para a **Tabela 1 do artigo** e para identificar municípios com perfis
discrepantes.

### Célula de código: `step6`

```python
def desc_grupo(grupo, col):                     # descritivas de uma coluna dentro de um grupo (ex.: um município)
    s = grupo[col].dropna()                     # série da coluna no grupo, sem NaN
    if len(s) == 0:                             # grupo sem dados válidos...
        return pd.Series({k: np.nan for k in ['n','media','dp','p25','mediana','p75']})  # ...tudo NaN
    return pd.Series({
        'n':       int(len(s)),                 # nº de setores válidos no grupo
        'media':   s.mean(),                    # média
        'dp':      s.std(),                     # desvio-padrão
        'p25':     s.quantile(0.25),            # 1º quartil
        'mediana': s.median(),                  # mediana
        'p75':     s.quantile(0.75),            # 3º quartil
    })

linhas = []                                     # acumula uma linha por (município, variável)
for (cd_uf, cd_mun, nm_mun), g in df_ok.groupby(['CD_UF', 'CD_MUN', 'NM_MUN'], sort=True):  # agrupa por município
    for col in INDICADORES:                     # para cada um dos 7 indicadores...
        d = desc_grupo(g, col)                  # calcula as descritivas naquele município
        d['CD_UF'] = cd_uf                      # anexa identificação: UF
        d['CD_MUN'] = cd_mun                    # código do município
        d['NM_MUN'] = nm_mun                    # nome do município
        d['variavel'] = col                     # qual indicador é esta linha
        linhas.append(d)                        # guarda a linha
desc_mun = pd.DataFrame(linhas)[['CD_UF','CD_MUN','NM_MUN','variavel','n','media','dp','p25','mediana','p75']]  # monta a tabela na ordem desejada
desc_mun = desc_mun.sort_values(['CD_UF','NM_MUN','variavel']).reset_index(drop=True)  # ordena e reindexa
print(f'Linhas geradas: {len(desc_mun)} (70 municípios × {len(INDICADORES)} variáveis)')  # log: deve dar 490
print('\nPrimeiras 14 linhas (2 municípios × 7 variáveis):')                               # log
print(desc_mun.head(14).round(4).to_string(index=False))                                   # amostra das primeiras linhas
```

## 7. Descritivas por região geográfica

Agrega o resultado por região (Norte / Nordeste / Sudeste / Sul / Centro-Oeste)
usando a lista oficial ELSI como dicionário UF → região.

### Célula de código: `step7`

```python
# relê a lista ELSI p/ montar o dicionário UF -> região (a base df_ok só tem o código da UF)
df_elsi = pd.read_csv(str(ROOT / 'dados' / 'municipios_elsi_brasil.csv'), sep=';', dtype=str)
mapa_regiao = dict(zip(df_elsi['uf_codigo'].str.zfill(2), df_elsi['regiao']))  # dicionário {'31':'Sudeste', ...}
df_ok['regiao'] = df_ok['CD_UF'].map(mapa_regiao)                              # cria a coluna 'regiao' a partir do código da UF

linhas = []                                     # acumula uma linha por (região, variável)
for regiao, g in df_ok.groupby('regiao', sort=True):  # agrupa por região
    for col in INDICADORES:                     # para cada indicador...
        d = desc_grupo(g, col)                  # descritivas naquela região
        d['regiao'] = regiao                    # anexa a região
        d['variavel'] = col                     # anexa o nome do indicador
        linhas.append(d)
desc_reg = pd.DataFrame(linhas)[['regiao','variavel','n','media','dp','p25','mediana','p75']]  # monta a tabela
desc_reg = desc_reg.sort_values(['regiao','variavel']).reset_index(drop=True)                   # ordena
print(desc_reg.round(4).to_string(index=False))                                                 # imprime descritivas por região
```

## 7b. Variáveis complementares de habitação precária

Duas variáveis derivadas de domicílios, **descritivas** — NÃO entram nos 7 componentes do
IVS-BH 2012 nem nas correlações / análise fatorial. Promovê-las a componente do índice é
decisão metodológica da orientadora.

| Variável | Numerador | Denominador |
|---|---|---|
| `pct_dom_improv` | V00002 (Domicílios Particulares Improvisados Ocupados) | V00001 + V00002 |
| `pct_hab_precaria` | V00050 (cortiço) + V00052 (estrutura permanente degradada) + V00053–V00058 (improvisados) | V00001 + V00002 |

Códigos confirmados no dicionário oficial do IBGE
(`docs/Apresentacoes_IVS/Dicionario_IBGE_Oficial_Variaveis_do_Projeto.xlsx`). São variáveis
muito esparsas (quase tudo zero) — reportar com mediana/P95 e contagem de setores > 0.

### Célula de código: `hab-precaria`

```python
# Variáveis complementares de habitação precária (descritivas, FORA do IVS-7).
den_dom = df_ok[['V00001', 'V00002']].sum(axis=1, min_count=1)  # denominador domiciliar: permanentes + improvisados
df_ok['pct_dom_improv'] = safe_div(df_ok['V00002'], den_dom)    # % de domicílios improvisados sobre o total de domicílios

# Habitação precária = cortiço (V00050) + estrutura permanente degradada (V00052)
# + todos os domicílios improvisados (V00053-V00058).
precaria_cols = ['V00050', 'V00052', 'V00053', 'V00054', 'V00055', 'V00056', 'V00057', 'V00058']  # tipos precários
df_ok['pct_hab_precaria'] = safe_div(df_ok[precaria_cols].sum(axis=1, min_count=1), den_dom)        # % habitação precária

COMPLEMENTARES = ['pct_dom_improv', 'pct_hab_precaria']  # lista das 2 variáveis complementares desta seção

print('Descritivas globais — habitação precária (setores OK):')                                       # log
print(df_ok[COMPLEMENTARES].describe(percentiles=[.5, .9, .95, .99]).round(5).to_string())            # describe c/ percentis altos (esparsas)
for c in COMPLEMENTARES:                                                                               # para cada variável...
    print(f'  {c}: setores com valor > 0 = {(df_ok[c] > 0).sum():,} ({(df_ok[c] > 0).mean()*100:.2f}%)')  # quantos setores têm valor > 0

# Por região (reaproveita desc_grupo e a coluna regiao da seção 7)
linhas = []
for regiao, g in df_ok.groupby('regiao', sort=True):    # agrupa por região
    for col in COMPLEMENTARES:                          # e por variável complementar
        d = desc_grupo(g, col); d['regiao'] = regiao; d['variavel'] = col; linhas.append(d)  # descritivas + identificação
hab_reg = (pd.DataFrame(linhas)[['regiao', 'variavel', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
           .sort_values(['regiao', 'variavel']).reset_index(drop=True))  # tabela por região
print('\nPor região:')
print(hab_reg.round(5).to_string(index=False))

# Por município
linhas = []
for (cd_uf, cd_mun, nm_mun), g in df_ok.groupby(['CD_UF', 'CD_MUN', 'NM_MUN'], sort=True):  # agrupa por município
    for col in COMPLEMENTARES:
        d = desc_grupo(g, col)
        d['CD_UF'] = cd_uf; d['CD_MUN'] = cd_mun; d['NM_MUN'] = nm_mun; d['variavel'] = col  # anexa identificação
        linhas.append(d)
hab_mun = (pd.DataFrame(linhas)[['CD_UF', 'CD_MUN', 'NM_MUN', 'variavel', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
           .sort_values(['CD_UF', 'NM_MUN', 'variavel']).reset_index(drop=True))  # tabela por município

# Exporta artefatos
df_ok[COMPLEMENTARES].describe(percentiles=[.5, .9, .95, .99]).round(6).to_csv(   # describe global -> CSV
    CAMINHO_EDA + 'habitacao_precaria_global.csv', sep=';', encoding='utf-8-sig')
hab_reg.to_csv(CAMINHO_EDA + 'habitacao_precaria_por_regiao.csv', sep=';', index=False, encoding='utf-8-sig')      # por região -> CSV
hab_mun.to_csv(CAMINHO_EDA + 'habitacao_precaria_por_municipio.csv', sep=';', index=False, encoding='utf-8-sig')  # por município -> CSV
print('\nArtefatos exportados: habitacao_precaria_{global,por_regiao,por_municipio}.csv')  # log
```

## 7c. Inadequação de banheiro

Duas variáveis descritivas de inadequação sanitária domiciliar — NÃO entram nos 7
componentes do IVS-BH 2012 (promovê-las a componente é decisão da orientadora):

| Variável | Numerador | Denominador |
|---|---|---|
| `pct_sem_banheiro` | V00495 (sem banheiro de uso exclusivo com chuveiro e vaso sanitário) | V00001 |
| `pct_sem_banheiro_nem_sanitario` | V00238 (não tinham banheiro nem sanitário) | V00001 |

V00495 = inadequação ampla (sem banheiro privativo completo — pode ter só comum ou só
sanitário); V00238 = privação extrema (nenhuma instalação). Denominador V00001 (DPPO),
como nas demais variáveis de saneamento. Códigos confirmados no dicionário oficial do IBGE.

### Célula de código: `banheiro-inad`

```python
# Inadequação de banheiro (descritivas, FORA do IVS-7). Denominador V00001 (DPPO).
df_ok['pct_sem_banheiro'] = np.clip(safe_div(df_ok['V00495'], df_ok['V00001']), 0, 1)  # % sem banheiro privativo completo (V00495/V00001), cortado em [0,1]
df_ok['pct_sem_banheiro_nem_sanitario'] = np.clip(safe_div(df_ok['V00238'], df_ok['V00001']), 0, 1)  # % sem banheiro nem sanitário (privação extrema)

BANHEIRO = ['pct_sem_banheiro', 'pct_sem_banheiro_nem_sanitario']  # as 2 variáveis desta seção
print('Descritivas globais - inadequacao de banheiro (setores OK):')                       # log
print(df_ok[BANHEIRO].describe(percentiles=[.5, .9, .95, .99]).round(5).to_string())       # describe c/ percentis altos
for c in BANHEIRO:
    print(f'  {c}: setores com valor > 0 = {(df_ok[c] > 0).sum():,} ({(df_ok[c] > 0).mean()*100:.2f}%)')  # nº de setores > 0

# Por região
linhas = []
for regiao, g in df_ok.groupby('regiao', sort=True):    # agrupa por região
    for col in BANHEIRO:
        d = desc_grupo(g, col); d['regiao'] = regiao; d['variavel'] = col; linhas.append(d)  # descritivas + identificação
ban_reg = (pd.DataFrame(linhas)[['regiao', 'variavel', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
           .sort_values(['regiao', 'variavel']).reset_index(drop=True))  # tabela por região (origem dos % do slide)
print('\nPor regiao:')
print(ban_reg.round(5).to_string(index=False))

# Por município
linhas = []
for (cd_uf, cd_mun, nm_mun), g in df_ok.groupby(['CD_UF', 'CD_MUN', 'NM_MUN'], sort=True):  # agrupa por município
    for col in BANHEIRO:
        d = desc_grupo(g, col)
        d['CD_UF'] = cd_uf; d['CD_MUN'] = cd_mun; d['NM_MUN'] = nm_mun; d['variavel'] = col
        linhas.append(d)
ban_mun = (pd.DataFrame(linhas)[['CD_UF', 'CD_MUN', 'NM_MUN', 'variavel', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
           .sort_values(['CD_UF', 'NM_MUN', 'variavel']).reset_index(drop=True))  # tabela por município

df_ok[BANHEIRO].describe(percentiles=[.5, .9, .95, .99]).round(6).to_csv(   # describe global -> CSV
    CAMINHO_EDA + 'inadequacao_banheiro_global.csv', sep=';', encoding='utf-8-sig')
ban_reg.to_csv(CAMINHO_EDA + 'inadequacao_banheiro_por_regiao.csv', sep=';', index=False, encoding='utf-8-sig')      # por região -> CSV
ban_mun.to_csv(CAMINHO_EDA + 'inadequacao_banheiro_por_municipio.csv', sep=';', index=False, encoding='utf-8-sig')  # por município -> CSV
print('\nArtefatos exportados: inadequacao_banheiro_{global,por_regiao,por_municipio}.csv')  # log
```

## 7d. Pessoa responsável do sexo feminino

Variável descritiva sociodemográfica (domicílios chefiados por mulher) — NÃO entra nos 7
componentes do IVS-BH 2012; é um marcador de contexto frequentemente associado à
vulnerabilidade em saúde.

| Variável | Numerador | Denominador |
|---|---|---|
| `pct_resp_feminino` | V01063 (pessoa responsável pelo domicílio, sexo feminino) | V01062 + V01063 (total de responsáveis por sexo) |

Códigos confirmados no dicionário oficial do IBGE (arquivo Parentesco). V01062+V01063 ≈
V01042 (total de responsáveis) em 99,7% dos setores.

### Célula de código: `resp-fem`

```python
# Pessoa responsavel do sexo feminino (descritiva sociodemografica, FORA do IVS-7).
resp_tot = df_ok[['V01062', 'V01063']].sum(axis=1, min_count=1)  # total de responsáveis por sexo (masculino V01062 + feminino V01063)
df_ok['pct_resp_feminino'] = np.clip(safe_div(df_ok['V01063'], resp_tot), 0, 1)  # % de responsáveis mulheres, cortado em [0,1]

print('Descritivas globais - responsavel do sexo feminino (setores OK):')                  # log
print(df_ok['pct_resp_feminino'].describe(percentiles=[.5, .9, .95, .99]).round(5).to_string())  # describe
print(f"  Total resp. feminino (V01063):     {int(df_ok['V01063'].sum()):,}")               # nº absoluto de responsáveis mulheres
print(f"  Total resp. por sexo (V01062+V01063): {int(resp_tot.sum()):,}")                   # nº absoluto de responsáveis (ambos sexos)
print(f"  Setores com maioria feminina (>50%): {(df_ok['pct_resp_feminino'] > 0.5).sum():,} ({(df_ok['pct_resp_feminino'] > 0.5).mean()*100:.1f}%)")  # setores chefiados majoritariamente por mulheres

# Por regiao
linhas = []
for regiao, g in df_ok.groupby('regiao', sort=True):    # agrupa por região
    d = desc_grupo(g, 'pct_resp_feminino'); d['regiao'] = regiao; linhas.append(d)  # descritivas + região
resp_reg = (pd.DataFrame(linhas)[['regiao', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
            .sort_values('regiao').reset_index(drop=True))  # tabela por região
print('\nPor regiao:')
print(resp_reg.round(5).to_string(index=False))

# Por municipio
linhas = []
for (cd_uf, cd_mun, nm_mun), g in df_ok.groupby(['CD_UF', 'CD_MUN', 'NM_MUN'], sort=True):  # agrupa por município
    d = desc_grupo(g, 'pct_resp_feminino')
    d['CD_UF'] = cd_uf; d['CD_MUN'] = cd_mun; d['NM_MUN'] = nm_mun; linhas.append(d)  # anexa identificação
resp_mun = (pd.DataFrame(linhas)[['CD_UF', 'CD_MUN', 'NM_MUN', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
            .sort_values(['CD_UF', 'NM_MUN']).reset_index(drop=True))  # tabela por município

df_ok['pct_resp_feminino'].describe(percentiles=[.5, .9, .95, .99]).round(6).to_csv(   # describe global -> CSV
    CAMINHO_EDA + 'resp_feminino_global.csv', sep=';', encoding='utf-8-sig')
resp_reg.to_csv(CAMINHO_EDA + 'resp_feminino_por_regiao.csv', sep=';', index=False, encoding='utf-8-sig')      # por região -> CSV
resp_mun.to_csv(CAMINHO_EDA + 'resp_feminino_por_municipio.csv', sep=';', index=False, encoding='utf-8-sig')  # por município -> CSV
print('\nArtefatos exportados: resp_feminino_{global,por_regiao,por_municipio}.csv')  # log
```

## 7e. Indicadores de envelhecimento populacional

**Demanda da orientadora (jul/2026):** *"ajustar índice de envelhecimento (ler artigo)"*.

As definições seguem o **Quadro 1 de Galvão et al.** (*Envelhecimento populacional em
Mato Grosso e sua relação com indicadores demográficos e econômicos*, Hygeia, v. 21,
e2106, 2025), que por sua vez adota os indicadores das Nações Unidas para estudos
populacionais. São descritivas demográficas — **não** entram nos 7 componentes do IVS.

| Indicador | Fórmula (× 100) | Variáveis do Censo 2022 | Situação |
|---|---|---|---|
| **IEP** — Índice de Envelhecimento Populacional | 60+ / **menores de 15 anos** | (V01040+V01041) / (V01031+V01032+V01033) | ✅ implementado |
| **RDI** — Razão de Dependência de Idosos | 60+ / **15 a 59 anos** | (V01040+V01041) / (V01034+…+V01039) | ✅ implementado |
| **% 60 anos ou mais** | 60+ / população total | (V01040+V01041) / v0001 | ✅ implementado |
| **LI** — Longevidade | **75+** / 60+ | — | ❌ **inviável** (ver abaixo) |

### Correção do denominador (o ajuste pedido)

A versão anterior desta seção calculava o índice de envelhecimento como
**idosos 60+ / crianças de 0 a 4 anos** (V01031). Está errado: o denominador do IEP é a
população com **menos de 15 anos** — 0–4 **mais** 5–9 **mais** 10–14
(V01031 + V01032 + V01033). Com o denominador antigo o índice ficava ~3× maior do que o
publicado pelo IBGE, e não era comparável com nenhuma referência da literatura.

Referências de validação (IBGE/Censo 2022, citadas em Galvão et al., 2025): IEP do
**Brasil = 80,0** (era 44,8 em 2010); **Norte 41,4**, **Sul 95,4**, **Sudeste 98,0**.

### Por que a Longevidade (LI) não é calculável

O LI exige a população de **75 anos ou mais**. Nos agregados por setor censitário a
faixa etária mais fina no topo da pirâmide é **V01041 = "70 anos ou mais"** — não há
corte em 75. Também não há corte em 65, motivo pelo qual todos os indicadores usam 60+.

Como substituto parcial, calculamos a **proporção de 70+ entre os 60+**
(V01041 / (V01040 + V01041)), que mede o mesmo fenômeno — o envelhecimento *dentro* do
grupo idoso — mas **não é o LI** e não deve ser comparada com valores de LI publicados.

### Agregado × por setor

Cada indicador é calculado de duas formas, e as duas são exportadas:

- **agregado** (razão das somas do grupo) — é o número comparável com o publicado para
  municípios, regiões e Brasil; é o que deve ir para as tabelas do artigo;
- **por setor** (razão dentro de cada setor, depois descritivas) — mostra a *variação
  intraurbana*, que é o objeto do projeto. Setores sem crianças (denominador 0) ficam
  `NaN`, não zero.

### Célula de código: `idade-estrutura`

```python
# Indicadores de envelhecimento populacional (descritivas, FORA do IVS-7).
# Definições: Galvão et al., Hygeia v.21, e2106, 2025, Quadro 1 (indicadores da ONU).

FAIXA_0A14   = ['V01031', 'V01032', 'V01033']                                    # 0-4, 5-9, 10-14  -> menores de 15 anos
FAIXA_15A59  = ['V01034', 'V01035', 'V01036', 'V01037', 'V01038', 'V01039']      # 15-19 ... 50-59  -> população em idade ativa
FAIXA_60MAIS = ['V01040', 'V01041']                                              # 60-69 e 70+      -> idosos

# Contagens absolutas por setor (min_count=1: se TODAS as parcelas forem sigilosas, fica NaN)
df_ok['n_crianca_0a4']  = df_ok['V01031']                                        # mantida da versão anterior (comparabilidade)
df_ok['n_pop_0a14']     = df_ok[FAIXA_0A14].sum(axis=1, min_count=1)             # denominador CORRETO do IEP
df_ok['n_pop_15a59']    = df_ok[FAIXA_15A59].sum(axis=1, min_count=1)            # denominador do RDI
df_ok['n_idoso_60mais'] = df_ok[FAIXA_60MAIS].sum(axis=1, min_count=1)           # numerador dos três indicadores
df_ok['n_idoso_70mais'] = df_ok['V01041']                                        # topo da pirâmide (não existe corte em 75)

# Proporções sobre a população total do setor (v0001)
df_ok['pct_crianca_0a4']  = np.clip(safe_div(df_ok['n_crianca_0a4'], df_ok['v0001']), 0, 1)   # % de crianças de 0 a 4
df_ok['pct_pop_0a14']     = np.clip(safe_div(df_ok['n_pop_0a14'], df_ok['v0001']), 0, 1)      # % de menores de 15
df_ok['pct_idoso_60mais'] = np.clip(safe_div(df_ok['n_idoso_60mais'], df_ok['v0001']), 0, 1)  # % de 60 anos ou mais

# Índices POR SETOR (mostram a variação intraurbana). Denominador 0 -> NaN (safe_div), nunca zero.
df_ok['iep_setor'] = safe_div(df_ok['n_idoso_60mais'], df_ok['n_pop_0a14']) * 100    # IEP = 60+ / menores de 15
df_ok['rdi_setor'] = safe_div(df_ok['n_idoso_60mais'], df_ok['n_pop_15a59']) * 100   # RDI = 60+ / 15 a 59
# Proxy de longevidade: NÃO é o LI (que exigiria 75+, inexistente nos agregados por setor).
df_ok['prop_70mais_entre_60mais'] = safe_div(df_ok['n_idoso_70mais'], df_ok['n_idoso_60mais']) * 100

IDADE = ['pct_crianca_0a4', 'pct_pop_0a14', 'pct_idoso_60mais']                  # proporções etárias
ENVELHECIMENTO = ['iep_setor', 'rdi_setor', 'prop_70mais_entre_60mais']          # índices por setor


def _indicadores_agregados(g):
    """Indicadores de envelhecimento AGREGADOS (razão das somas) — o número comparável
    com o publicado pelo IBGE para municípios/regiões/Brasil."""
    cri04 = g['n_crianca_0a4'].sum()                     # total de crianças de 0 a 4 no grupo
    p014  = g['n_pop_0a14'].sum()                        # total de menores de 15
    p1559 = g['n_pop_15a59'].sum()                       # total de 15 a 59
    i60   = g['n_idoso_60mais'].sum()                    # total de 60+
    i70   = g['n_idoso_70mais'].sum()                    # total de 70+
    pop   = g['v0001'].sum()                             # população total
    return pd.Series({
        'n_setores':      len(g),                                                        # nº de setores no grupo
        'pop_total':      int(pop),                                                      # população residente
        'n_crianca_0a4':  int(cri04),                                                    # contagem 0-4
        'n_pop_0a14':     int(p014),                                                     # contagem 0-14
        'n_pop_15a59':    int(p1559),                                                    # contagem 15-59
        'n_idoso_60mais': int(i60),                                                      # contagem 60+
        'n_idoso_70mais': int(i70),                                                      # contagem 70+
        'pct_pop_0a14':   round(p014 / pop * 100, 2) if pop else np.nan,                 # % de menores de 15
        'pct_60mais':     round(i60 / pop * 100, 2) if pop else np.nan,                  # % de 60 anos ou mais
        'IEP':            round(i60 / p014 * 100, 1) if p014 else np.nan,                # Índice de Envelhecimento
        'RDI':            round(i60 / p1559 * 100, 1) if p1559 else np.nan,              # Razão de Dependência de Idosos
        'prop_70mais_entre_60mais': round(i70 / i60 * 100, 1) if i60 else np.nan,        # proxy de longevidade (NÃO é o LI)
    })


# ---- Global (todos os setores urbanos elegíveis dos 70 municípios) ----
env_global = _indicadores_agregados(df_ok)
print('Indicadores de envelhecimento AGREGADOS — 70 municípios ELSI (setores urbanos elegíveis):')
print(env_global.to_string())
print('\nReferências do Censo 2022 para conferência (Galvão et al., 2025, citando IBGE):')
print('  IEP Brasil = 80,0  |  Norte = 41,4  |  Sul = 95,4  |  Sudeste = 98,0')
print('  (a comparação não é exata: aqui o recorte é urbano e restrito aos 70 municípios do ELSI)')

print('\nDescritivas POR SETOR (variação intraurbana):')
print(df_ok[IDADE + ENVELHECIMENTO].describe(percentiles=[.1, .5, .9, .95, .99]).round(3).to_string())
for c in ENVELHECIMENTO:                                                                  # quantos setores não têm o índice
    print(f'  {c}: calculável em {df_ok[c].notna().sum():,} de {len(df_ok):,} setores '
          f'({df_ok[c].isna().sum():,} com denominador zero ou sigiloso)')

# ---- Agregados por região e por município ----
env_reg = (df_ok.groupby('regiao').apply(_indicadores_agregados, include_groups=False)     # uma linha por região
           .reindex(ORDEM_REGIAO).reset_index())
env_mun = (df_ok.groupby(['CD_UF', 'CD_MUN', 'NM_MUN', 'regiao'])                          # uma linha por município
           .apply(_indicadores_agregados, include_groups=False).reset_index()
           .sort_values('IEP', ascending=False))
print('\nAgregados por região:')
print(env_reg[['regiao', 'pop_total', 'pct_pop_0a14', 'pct_60mais', 'IEP', 'RDI']].to_string(index=False))
print('\n10 municípios mais envelhecidos (maior IEP):')
print(env_mun.head(10)[['NM_MUN', 'regiao', 'pop_total', 'pct_60mais', 'IEP', 'RDI']].to_string(index=False))
print('\n5 municípios menos envelhecidos (menor IEP):')
print(env_mun.tail(5)[['NM_MUN', 'regiao', 'pop_total', 'pct_60mais', 'IEP', 'RDI']].to_string(index=False))


# ---- Descritivas por setor, agrupadas por região e por município ----
def _desc_long(chaves, colunas):                 # helper: tabela longa de descritivas agrupando por 'chaves'
    linhas = []
    for chave, g in df_ok.groupby(chaves, sort=True):        # agrupa pelas chaves recebidas (1 ou várias colunas)
        chave = chave if isinstance(chave, tuple) else (chave,)  # garante tupla (1 chave vem como escalar)
        for col in colunas:                      # para cada variável pedida...
            d = desc_grupo(g, col)               # descritivas no grupo
            for k, v in zip(chaves, chave):      # anexa cada coluna-chave com seu valor
                d[k] = v
            d['variavel'] = col                  # qual variável é esta linha
            linhas.append(d)
    return pd.DataFrame(linhas)                  # devolve a tabela longa


COLS_DESC = IDADE + ENVELHECIMENTO                                                          # o que descrever por setor
idade_reg = (_desc_long(['regiao'], COLS_DESC)[['regiao', 'variavel', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
             .sort_values(['regiao', 'variavel']).reset_index(drop=True))                   # por região
idade_mun = (_desc_long(['CD_UF', 'CD_MUN', 'NM_MUN'], COLS_DESC)
             [['CD_UF', 'CD_MUN', 'NM_MUN', 'variavel', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
             .sort_values(['CD_UF', 'NM_MUN', 'variavel']).reset_index(drop=True))          # por município

# ---- Exporta artefatos ----
df_ok[COLS_DESC].describe(percentiles=[.1, .5, .9, .95, .99]).round(6).to_csv(              # describe global (por setor)
    CAMINHO_EDA + 'estrutura_etaria_global.csv', sep=';', encoding='utf-8-sig')
idade_reg.to_csv(CAMINHO_EDA + 'estrutura_etaria_por_regiao.csv', sep=';', index=False, encoding='utf-8-sig')
idade_mun.to_csv(CAMINHO_EDA + 'estrutura_etaria_por_municipio.csv', sep=';', index=False, encoding='utf-8-sig')
env_global.to_frame('TOTAL_70_municipios').T.to_csv(                                        # agregados: total
    CAMINHO_EDA + 'indicadores_envelhecimento_total.csv', sep=';', encoding='utf-8-sig')
env_reg.to_csv(CAMINHO_EDA + 'indicadores_envelhecimento_por_regiao.csv', sep=';', index=False, encoding='utf-8-sig')
env_mun.to_csv(CAMINHO_EDA + 'estrutura_etaria_contagem_por_municipio.csv', sep=';', index=False, encoding='utf-8-sig')
print('\nArtefatos exportados: estrutura_etaria_{global,por_regiao,por_municipio,contagem_por_municipio}.csv '
      'e indicadores_envelhecimento_{total,por_regiao}.csv')
```

## 7f. Tipo de domicílio — moradias convencionais e indicador de apartamento

**Demandas da orientadora (jul/2026):** *"agrupar variáveis como moradias normais no
tipo do domicílio"* e *"criar um indicador de apartamento"*.

O Censo 2022 desdobra o **tipo de espécie** do domicílio em 12 variáveis: seis para os
Domicílios Particulares Permanentes Ocupados (DPPO, V00047–V00052) e seis para os
Domicílios Particulares Improvisados Ocupados (DPIO, V00053–V00058). O agrupamento
adotado:

| Grupo | Variáveis | Descrição oficial IBGE |
|---|---|---|
| **Convencional** ("moradia normal") | V00047 | casa |
| | V00048 | casa de vila ou em condomínio |
| | V00049 | apartamento |
| **Não convencional** (permanente) | V00050 | habitação em casa de cômodos ou cortiço |
| | V00051 | habitação indígena sem paredes ou maloca |
| | V00052 | estrutura residencial permanente degradada ou inacabada |
| **Improvisado** (DPIO) | V00053–V00058 | tenda/barraca, dentro de estabelecimento, abrigo natural, estrutura em logradouro público, estrutura não residencial degradada, veículo |

### Denominador

`V00001` (DPPO) para os grupos convencional e não convencional — os dois são
subconjuntos exatos dos DPPO. Isto foi **verificado empiricamente** na base ELSI:
a soma V00047+…+V00052 nunca ultrapassa V00001 em nenhum dos 106 mil setores
elegíveis; quando fica abaixo, a diferença é de no máximo 6 domicílios e decorre de
**sigilo** em alguma das parcelas (o IBGE suprime contagens muito pequenas).

Para os improvisados o denominador é `V00001 + V00002` (todos os domicílios
particulares ocupados), já usado na seção 7b de habitação precária.

### Indicadores criados

| Variável | Fórmula |
|---|---|
| `pct_moradia_convencional` | (V00047 + V00048 + V00049) / V00001 |
| `pct_moradia_nao_convencional` | (V00050 + V00051 + V00052) / V00001 |
| `pct_apartamento` | **V00049 / V00001** |
| `pct_casa` | V00047 / V00001 |
| `pct_casa_vila_condominio` | V00048 / V00001 |

A coluna categórica `Moradia_Predominante` (gerada no Notebook 01) ganha uma versão
agrupada, `Moradia_Predominante_Agrupada`, com as mesmas três classes acima.

> **Nota:** `pct_apartamento` é um indicador *descritivo* de morfologia urbana, não um
> componente do IVS. Ele não tem direção de vulnerabilidade definida — verticalização
> aparece tanto em áreas centrais de alta renda quanto em conjuntos habitacionais
> populares — e por isso serve para caracterizar o território, não para pontuá-lo.

### Célula de código: `tipo-domicilio`

```python
# Tipo de domicílio: moradias convencionais, não convencionais e apartamento.
# Descritivas de morfologia urbana — FORA do IVS-7. Denominador V00001 (DPPO).

CONVENCIONAL     = ['V00047', 'V00048', 'V00049']   # casa + casa de vila/condomínio + apartamento
NAO_CONVENCIONAL = ['V00050', 'V00051', 'V00052']   # cortiço/casa de cômodos + maloca indígena + estrutura degradada
IMPROVISADO      = ['V00053', 'V00054', 'V00055', 'V00056', 'V00057', 'V00058']  # DPIO (tenda, veículo, logradouro etc.)

# Conferência do denominador: a soma dos 6 tipos de DPPO tem que caber dentro de V00001
_soma_dppo = df_ok[CONVENCIONAL + NAO_CONVENCIONAL].sum(axis=1, min_count=1)   # soma dos tipos de domicílio permanente
_dif = (_soma_dppo - df_ok['V00001']).dropna()                                  # diferença em relação ao denominador
print('Conferência do denominador (soma dos tipos de DPPO vs. V00001):')        # log
print(f'  setores comparáveis: {len(_dif):,} | soma == V00001 em {int((_dif == 0).sum()):,} '
      f'| soma > V00001 em {int((_dif > 0).sum()):,} (deve ser 0) | déficit máximo: {int(-_dif.min())} domicílios')
print('  O déficit residual vem do sigilo do IBGE em parcelas pequenas, não de erro de denominador.')

# Proporções (denominador V00001), cortadas em [0, 1]
df_ok['pct_moradia_convencional']     = np.clip(safe_div(df_ok[CONVENCIONAL].sum(axis=1, min_count=1), df_ok['V00001']), 0, 1)
df_ok['pct_moradia_nao_convencional'] = np.clip(safe_div(df_ok[NAO_CONVENCIONAL].sum(axis=1, min_count=1), df_ok['V00001']), 0, 1)
df_ok['pct_apartamento']              = np.clip(safe_div(df_ok['V00049'], df_ok['V00001']), 0, 1)   # <- indicador de apartamento
df_ok['pct_casa']                     = np.clip(safe_div(df_ok['V00047'], df_ok['V00001']), 0, 1)
df_ok['pct_casa_vila_condominio']     = np.clip(safe_div(df_ok['V00048'], df_ok['V00001']), 0, 1)

TIPO_DOM = ['pct_moradia_convencional', 'pct_moradia_nao_convencional',
            'pct_apartamento', 'pct_casa', 'pct_casa_vila_condominio']

# Versão agrupada da classificação categórica criada no Notebook 01
MAPA_AGRUPADO = {                                                   # de-para: rótulo detalhado -> grupo
    'Casa': 'Convencional',
    'Casa de Vila/Condomínio': 'Convencional',
    'Apartamento': 'Convencional',
    'Cortiço/Casa de Cômodos': 'Não convencional',
    'Maloca Indígena': 'Não convencional',
    'Estrutura Degradada/Inacabada': 'Não convencional',
    'Indefinido/Sem Moradia': 'Indefinido',
}
df_ok['Moradia_Predominante_Agrupada'] = df_ok['Moradia_Predominante'].map(MAPA_AGRUPADO).fillna('Indefinido')

print('\nDescritivas globais — tipo de domicílio (setores urbanos elegíveis):')
print(df_ok[TIPO_DOM].describe(percentiles=[.1, .5, .9, .95, .99]).round(4).to_string())
print('\nDistribuição da moradia predominante (detalhada × agrupada):')
print(pd.crosstab(df_ok['Moradia_Predominante'], df_ok['Moradia_Predominante_Agrupada']).to_string())

# Totais absolutos de domicílios por tipo (agregado dos 70 municípios)
tot_dppo = df_ok['V00001'].sum()                                                  # total de DPPO no recorte
linhas_tot = []
for grupo, cols in [('Convencional', CONVENCIONAL), ('Não convencional', NAO_CONVENCIONAL), ('Improvisado (DPIO)', IMPROVISADO)]:
    s = df_ok[cols].sum().sum()                                                   # soma de domicílios do grupo
    linhas_tot.append({'grupo': grupo, 'n_domicilios': int(s), 'pct_sobre_V00001': round(s / tot_dppo * 100, 3)})
tipo_total = pd.DataFrame(linhas_tot)
print(f'\nTotais de domicílios por grupo (denominador V00001 = {int(tot_dppo):,}):')
print(tipo_total.to_string(index=False))

# Por região e por município (reaproveita o helper _desc_long da seção anterior)
tipo_reg = (_desc_long(['regiao'], TIPO_DOM)[['regiao', 'variavel', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
            .sort_values(['regiao', 'variavel']).reset_index(drop=True))
tipo_mun = (_desc_long(['CD_UF', 'CD_MUN', 'NM_MUN'], TIPO_DOM)
            [['CD_UF', 'CD_MUN', 'NM_MUN', 'variavel', 'n', 'media', 'dp', 'p25', 'mediana', 'p75']]
            .sort_values(['CD_UF', 'NM_MUN', 'variavel']).reset_index(drop=True))
print('\nMédia por região:')
print(tipo_reg.pivot(index='regiao', columns='variavel', values='media').reindex(ORDEM_REGIAO).round(4).to_string())

# Ranking de verticalização (municípios com maior proporção média de apartamento)
apto_mun = (tipo_mun[tipo_mun['variavel'] == 'pct_apartamento']
            .sort_values('media', ascending=False)[['NM_MUN', 'n', 'media', 'mediana', 'p75']])
print('\n10 municípios com maior proporção média de apartamentos:')
print(apto_mun.head(10).round(4).to_string(index=False))

# Exporta artefatos
df_ok[TIPO_DOM].describe(percentiles=[.1, .5, .9, .95, .99]).round(6).to_csv(
    CAMINHO_EDA + 'tipo_domicilio_global.csv', sep=';', encoding='utf-8-sig')
tipo_total.to_csv(CAMINHO_EDA + 'tipo_domicilio_totais_por_grupo.csv', sep=';', index=False, encoding='utf-8-sig')
tipo_reg.to_csv(CAMINHO_EDA + 'tipo_domicilio_por_regiao.csv', sep=';', index=False, encoding='utf-8-sig')
tipo_mun.to_csv(CAMINHO_EDA + 'tipo_domicilio_por_municipio.csv', sep=';', index=False, encoding='utf-8-sig')
(df_ok.groupby(['regiao', 'Moradia_Predominante_Agrupada']).size().rename('n_setores').reset_index()
 .to_csv(CAMINHO_EDA + 'moradia_predominante_agrupada_por_regiao.csv', sep=';', index=False, encoding='utf-8-sig'))
print('\nArtefatos exportados: tipo_domicilio_{global,totais_por_grupo,por_regiao,por_municipio}.csv '
      'e moradia_predominante_agrupada_por_regiao.csv')
```

## 7g. Setores de vilas e favelas (FCU) no recorte ELSI

**Demanda da orientadora (jul/2026):** *"dentro do ELSI, quantos setores são de vilas e
favelas"*.

No Censo 2022 o IBGE substituiu a antiga categoria "aglomerado subnormal" pelas
**Favelas e Comunidades Urbanas (FCU)**. A marcação vem do arquivo básico, em três
colunas que a pipeline passou a ler em 09/08/2026:

| Coluna | Conteúdo |
|---|---|
| `CD_TIPO` | tipo do setor — **`1` = Favela e Comunidade Urbana** |
| `CD_FCU` | código da FCU a que o setor pertence |
| `NM_FCU` | nome da FCU (ex.: "Vitória", "Triângulo Novo") |

**Validação da marcação:** no Brasil inteiro, `CD_TIPO = 1` coincide exatamente com
`NM_FCU` preenchido — 33.272 setores nos dois critérios. No recorte ELSI aparecem 25
setores com nome de FCU mas `CD_TIPO ≠ 1`; a célula abaixo os isola e os quantifica.
O critério adotado é o **`CD_TIPO = 1`**, que é o campo de classificação oficial.

Além da contagem pedida, a célula compara os sete indicadores do IVS entre setores de
FCU e não-FCU — é a primeira evidência empírica, dentro deste projeto, de que o índice
capta a desigualdade intraurbana que se propõe a medir.

### Célula de código: `favelas-fcu`

```python
# Setores de Favelas e Comunidades Urbanas (FCU) no recorte ELSI.
# Critério oficial: CD_TIPO == '1' (arquivo básico do Censo 2022).

df['is_fcu']    = df['CD_TIPO'].eq('1')      # marcação em TODA a base (109.032 setores)
df_ok['is_fcu'] = df_ok['CD_TIPO'].eq('1')   # marcação no conjunto de análise (urbanos elegíveis)

# ---- Divergências entre CD_TIPO=1 e NM_FCU preenchido ----
_div = df[df['CD_TIPO'].eq('1') != df['NM_FCU'].notna()]                       # setores em que os dois critérios discordam
print(f'Divergências CD_TIPO=1 × NM_FCU preenchido: {len(_div):,} setores')     # log
if len(_div):
    print(_div.groupby(['CD_TIPO', 'SITUACAO'], dropna=False).size().rename('n_setores').to_string())
    print('  Exemplos:')
    print(_div[['CD_SETOR', 'NM_MUN', 'CD_TIPO', 'NM_FCU', 'Dados_sig']].head(5).to_string(index=False))
    print('  -> adotado CD_TIPO=1 como critério (campo oficial de classificação do setor).')

# ---- Contagem geral ----
n_fcu_base = int(df['is_fcu'].sum())                                            # FCU em toda a base
n_fcu_ok   = int(df_ok['is_fcu'].sum())                                         # FCU no conjunto de análise
print(f'\n=== Setores de Favela e Comunidade Urbana (FCU) nos 70 municípios ELSI ===')
print(f'  Na base completa:            {n_fcu_base:,} de {len(df):,} setores ({n_fcu_base / len(df) * 100:.2f}%)')
print(f'  No conjunto de análise:      {n_fcu_ok:,} de {len(df_ok):,} setores urbanos elegíveis '
      f'({n_fcu_ok / len(df_ok) * 100:.2f}%)')
print(f'  FCUs distintas (CD_FCU):     {df.loc[df["is_fcu"], "CD_FCU"].nunique():,}')
print(f'  População nos setores FCU:   {int(df.loc[df["is_fcu"], "v0001"].sum()):,}')
print(f'  Domicílios (V00001) em FCU:  {int(df.loc[df["is_fcu"], "V00001"].sum()):,}')
print(f'  Municípios com pelo menos 1 setor FCU: {df.loc[df["is_fcu"], "CD_MUN"].nunique()} de 70')


def _resumo_fcu(g):
    """Contagem de setores FCU e o peso populacional/domiciliar deles no grupo."""
    fcu = g['is_fcu']                                                            # máscara dos setores FCU
    n = len(g)                                                                   # total de setores do grupo
    pop, pop_fcu = g['v0001'].sum(), g.loc[fcu, 'v0001'].sum()                   # população total e em FCU
    dom, dom_fcu = g['V00001'].sum(), g.loc[fcu, 'V00001'].sum()                 # domicílios total e em FCU
    return pd.Series({
        'n_setores':     n,                                                      # setores no grupo
        'n_setores_fcu': int(fcu.sum()),                                         # setores de FCU
        'pct_setores_fcu': round(fcu.sum() / n * 100, 2) if n else np.nan,       # % de setores em FCU
        'n_fcu_distintas': g.loc[fcu, 'CD_FCU'].nunique(),                       # quantas FCUs diferentes
        'pop_fcu':       int(pop_fcu),                                           # população em FCU
        'pct_pop_fcu':   round(pop_fcu / pop * 100, 2) if pop else np.nan,       # % da população em FCU
        'dom_fcu':       int(dom_fcu),                                           # domicílios em FCU
        'pct_dom_fcu':   round(dom_fcu / dom * 100, 2) if dom else np.nan,       # % dos domicílios em FCU
    })


fcu_total = _resumo_fcu(df).to_frame('TOTAL_70_municipios').T                                  # linha total
fcu_reg = (df.groupby('regiao').apply(_resumo_fcu, include_groups=False)                       # por região
           .reindex(ORDEM_REGIAO).reset_index())
fcu_mun = (df.groupby(['CD_UF', 'CD_MUN', 'NM_MUN', 'regiao']).apply(_resumo_fcu, include_groups=False)  # por município
           .reset_index().sort_values('n_setores_fcu', ascending=False))

print('\nPor região:')
print(fcu_reg.to_string(index=False))
print('\n15 municípios com mais setores de FCU:')
print(fcu_mun.head(15)[['NM_MUN', 'regiao', 'n_setores', 'n_setores_fcu', 'pct_setores_fcu', 'pct_pop_fcu']].to_string(index=False))
print(f'\nMunicípios sem nenhum setor de FCU: {int((fcu_mun["n_setores_fcu"] == 0).sum())}')
print(fcu_mun[fcu_mun['n_setores_fcu'] == 0]['NM_MUN'].tolist())

# ---- Comparação dos indicadores do IVS: FCU × não-FCU ----
COMPARAR = INDICADORES + ['pct_moradia_convencional', 'pct_apartamento',        # 7 do IVS + morfologia + envelhecimento
                          'pct_pop_0a14', 'pct_idoso_60mais', 'iep_setor']
linhas = []
for col in COMPARAR:
    a = df_ok.loc[df_ok['is_fcu'], col].dropna()                                 # valores nos setores de FCU
    b = df_ok.loc[~df_ok['is_fcu'], col].dropna()                                # valores fora de FCU
    linhas.append({
        'variavel': col,
        'n_fcu': len(a), 'media_fcu': a.mean(), 'mediana_fcu': a.median(),       # descritivas em FCU
        'n_nao_fcu': len(b), 'media_nao_fcu': b.mean(), 'mediana_nao_fcu': b.median(),  # descritivas fora
        'razao_medias': (a.mean() / b.mean()) if b.mean() not in (0, np.nan) else np.nan,  # quantas vezes maior
    })
comp_fcu = pd.DataFrame(linhas).round(4)
print('\n--- Indicadores em setores de FCU × demais setores urbanos elegíveis ---')
print(comp_fcu.to_string(index=False))

# ---- Exporta artefatos ----
fcu_total.to_csv(CAMINHO_EDA + 'favelas_fcu_total.csv', sep=';', encoding='utf-8-sig')
fcu_reg.to_csv(CAMINHO_EDA + 'favelas_fcu_por_regiao.csv', sep=';', index=False, encoding='utf-8-sig')
fcu_mun.to_csv(CAMINHO_EDA + 'favelas_fcu_por_municipio.csv', sep=';', index=False, encoding='utf-8-sig')
comp_fcu.to_csv(CAMINHO_EDA + 'favelas_fcu_comparativo_indicadores.csv', sep=';', index=False, encoding='utf-8-sig')
print('\nArtefatos exportados: favelas_fcu_{total,por_regiao,por_municipio,comparativo_indicadores}.csv')
```

## 8. Distribuições — histogramas

Histograma de cada uma das 7 variáveis (guia FIOCRUZ, Seção 5.5). Permite ver a
forma da distribuição: simétrica, assimétrica, bimodal, com massa em zero, etc.

### Célula de código: `step8`

```python
fig, axes = plt.subplots(3, 3, figsize=(15, 10))   # cria uma grade 3×3 de subgráficos (9 espaços; usamos 7)
axes = axes.flatten()                              # transforma a matriz 3×3 de eixos numa lista linear (mais fácil indexar)
for i, col in enumerate(INDICADORES):              # para cada indicador (com seu índice i)...
    ax = axes[i]                                   # pega o subgráfico correspondente
    df_ok[col].dropna().hist(bins=50, ax=ax, color='#4C72B0', edgecolor='white')  # histograma da variável (50 faixas), sem NaN
    ax.set_title(col, fontsize=10)                 # título do subgráfico = nome da variável
    ax.set_xlabel(''); ax.set_ylabel('frequência') # rótulos dos eixos
    ax.grid(False)                                 # remove a grade de fundo
for j in range(len(INDICADORES), len(axes)):       # nos espaços que sobraram (8º e 9º)...
    axes[j].axis('off')                            # ...desliga o eixo (subgráfico em branco)
fig.suptitle('Histogramas — 7 variáveis-componente do IVS (setores urbanos elegíveis, 70 municípios ELSI)', fontsize=12)  # título geral
fig.tight_layout()                                 # ajusta espaçamentos p/ nada se sobrepor
fig.savefig(CAMINHO_FIG + 'histogramas.png', dpi=150, bbox_inches='tight')  # salva a figura em PNG (150 dpi)
plt.show()                                         # exibe a figura no notebook
```

## 9. Distribuições — boxplots por região

Boxplots estratificados por região (guia FIOCRUZ, Seção 5.3) para comparar centro,
dispersão e outliers entre regiões.

### Célula de código: `step9`

```python
ordem_regiao = ['Norte','Nordeste','Sudeste','Sul','Centro-Oeste']  # ordem fixa das regiões no eixo x
fig, axes = plt.subplots(3, 3, figsize=(15, 11))   # grade 3×3 de subgráficos
axes = axes.flatten()                              # lista linear de eixos
for i, col in enumerate(INDICADORES):              # para cada indicador...
    ax = axes[i]                                   # subgráfico correspondente
    dados = [df_ok[df_ok['regiao'] == r][col].dropna() for r in ordem_regiao]  # lista de séries: valores do indicador por região (sem NaN)
    ax.boxplot(dados, tick_labels=ordem_regiao, showfliers=True,   # desenha 5 boxplots (um por região); mostra outliers
               medianprops={'color': 'red'})       # mediana em vermelho
    ax.set_title(col, fontsize=10)                 # título = nome da variável
    ax.tick_params(axis='x', rotation=30)          # inclina os rótulos do eixo x em 30° (cabem melhor)
    ax.grid(False)                                 # sem grade de fundo
for j in range(len(INDICADORES), len(axes)):       # espaços extras (8º, 9º)...
    axes[j].axis('off')                            # ...desligados
fig.suptitle('Boxplots por região — variáveis-componente do IVS (setores urbanos elegíveis)', fontsize=12)  # título geral
fig.tight_layout()                                 # ajusta espaçamentos
fig.savefig(CAMINHO_FIG + 'boxplots_por_regiao.png', dpi=150, bbox_inches='tight')  # salva PNG
plt.show()                                         # exibe
```

## 10. Análise de outliers (regra do IQR)

Conta o número de setores fora do intervalo `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]` para cada
variável (guia FIOCRUZ, Seção 5.3). Outliers não devem ser removidos automaticamente
nesta fase — apenas inventariados.

### Célula de código: `step10`

```python
def conta_outliers(s):                          # conta outliers de uma série pela regra de Tukey (1.5×IQR) + alternativa P95
    s = s.dropna()                              # ignora NaN
    q1, q3 = s.quantile(0.25), s.quantile(0.75)  # 1º e 3º quartis
    iq = q3 - q1                                # intervalo interquartil (IQR)
    lim_inf, lim_sup = q1 - 1.5*iq, q3 + 1.5*iq  # limites de Tukey: abaixo/acima = outlier
    fora = ((s < lim_inf) | (s > lim_sup)).sum()  # nº de valores fora dos limites
    p95 = s.quantile(0.95)                      # percentil 95 (alternativa robusta p/ distribuições zero-infladas)
    n_p95 = int((s > p95).sum())               # nº de valores acima do P95
    # Flag: regra IQR é não-informativa quando P25 == mediana (distribuição
    # zero-inflada ou super-concentrada). Nestes casos, recomenda-se reportar
    # apenas o P95.
    iqr_inadequado = (q1 == s.median())        # True quando Q1 == mediana (muita massa em um único valor, ex.: zero)
    return pd.Series({
        'n_validos':   int(len(s)),            # nº de observações válidas
        'q1': q1, 'q3': q3, 'iq': iq,          # quartis e IQR
        'lim_inf': lim_inf, 'lim_sup': lim_sup,  # limites de Tukey
        'n_outliers':  int(fora),              # nº de outliers pela regra IQR
        'pct_outliers': round(fora / len(s) * 100, 2) if len(s) else np.nan,  # % de outliers
        'p95': p95,                            # valor do P95
        'n_acima_p95':  n_p95,                 # nº acima do P95
        'pct_acima_p95': round(n_p95 / len(s) * 100, 2) if len(s) else np.nan,  # % acima do P95
        'iqr_nao_informativo': iqr_inadequado, # flag de IQR não-informativo (ver acima)
    })

outliers = pd.DataFrame({c: conta_outliers(df_ok[c]) for c in INDICADORES}).T  # aplica a cada indicador e transpõe (1 linha por variável)
print('Outliers por variável — regra IQR (1.5 × IQR) + alternativa P95:\n')    # log
print(outliers.round(4).to_string())                                           # imprime a tabela de outliers
print('\nNota: `iqr_nao_informativo=True` indica distribuição zero-inflada;')  # nota interpretativa
print('use n_acima_p95 / pct_acima_p95 em vez da regra IQR no relatório.')      # recomendação prática
```

## 11. Análise de dados faltantes

Mapa de calor da % de células faltantes em cada variável-componente, por município.
Indispensável para detectar municípios com cobertura ruim (guia FIOCRUZ, checklist
20.2).

### Célula de código: `step11`

```python
miss_mun = (df_ok.groupby('NM_MUN')[INDICADORES]   # agrupa por município e seleciona os 7 indicadores
            .apply(lambda g: g.isna().mean() * 100)  # em cada município: % de NaN por variável (média de booleanos × 100)
            .round(2))                              # arredonda p/ 2 casas
print('Top 10 municípios com mais dados faltantes (média entre variáveis):')  # log
miss_mun['_media'] = miss_mun.mean(axis=1)          # coluna auxiliar: % média de missing entre as 7 variáveis
print(miss_mun.sort_values('_media', ascending=False).head(10).to_string())  # 10 municípios com mais missing

fig, ax = plt.subplots(figsize=(8, max(8, len(miss_mun) * 0.15)))  # figura com altura proporcional ao nº de municípios
m = miss_mun.drop(columns='_media').values         # matriz de % de missing (sem a coluna auxiliar)
im = ax.imshow(m, aspect='auto', cmap='Reds', vmin=0, vmax=max(1, m.max()))  # mapa de calor: quanto mais vermelho, mais missing
ax.set_yticks(range(len(miss_mun)))                # uma marca no eixo y por município
ax.set_yticklabels(miss_mun.index, fontsize=6)     # rótulos = nomes dos municípios
ax.set_xticks(range(len(INDICADORES)))             # uma marca no eixo x por variável
ax.set_xticklabels(INDICADORES, rotation=45, ha='right', fontsize=8)  # rótulos das variáveis, inclinados
fig.colorbar(im, ax=ax, label='% faltante')        # barra de cores (legenda do mapa de calor)
ax.set_title('Dados faltantes (%) por município × variável')  # título
fig.tight_layout()                                 # ajusta espaçamentos
fig.savefig(CAMINHO_FIG + 'missing_por_municipio.png', dpi=150, bbox_inches='tight')  # salva PNG
plt.show()                                         # exibe
```

## 12. Matriz de correlação

Correlação de Pearson (linear) e Spearman (postos / não paramétrica) entre as 7
variáveis (guia FIOCRUZ, Seção 11). Subsidia a futura análise fatorial — variáveis
muito correlacionadas tendem a se agrupar no mesmo fator.

### Célula de código: `step12`

```python
corr_p = df_ok[INDICADORES].corr(method='pearson').round(3)   # matriz de correlação de Pearson (associação linear) 7×7
corr_s = df_ok[INDICADORES].corr(method='spearman').round(3)  # matriz de Spearman (postos; robusta a assimetria/não-linearidade)

print('Pearson:\n', corr_p.to_string(), '\n')   # imprime a matriz de Pearson
print('Spearman:\n', corr_s.to_string())        # imprime a matriz de Spearman

fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 6))  # 2 subgráficos lado a lado (Pearson | Spearman)
for ax, mat, titulo in [(a1, corr_p, 'Pearson'), (a2, corr_s, 'Spearman')]:  # itera sobre os 2 mapas
    im = ax.imshow(mat.values, cmap='RdBu_r', vmin=-1, vmax=1)  # mapa de calor da matriz; escala fixa -1..1 (vermelho=+, azul=-)
    ax.set_xticks(range(len(INDICADORES))); ax.set_yticks(range(len(INDICADORES)))  # marcas dos eixos (uma por variável)
    ax.set_xticklabels(INDICADORES, rotation=45, ha='right', fontsize=8)  # rótulos das colunas (inclinados)
    ax.set_yticklabels(INDICADORES, fontsize=8)  # rótulos das linhas
    ax.set_title(f'Correlação — {titulo}')       # título do subgráfico
    for i in range(len(INDICADORES)):            # percorre as linhas da matriz...
        for j in range(len(INDICADORES)):        # ...e as colunas, p/ escrever o número em cada célula
            ax.text(j, i, f'{mat.values[i,j]:.2f}', ha='center', va='center',  # valor da correlação no centro da célula
                    color='black' if abs(mat.values[i,j]) < 0.6 else 'white', fontsize=7)  # texto preto se fraco, branco se forte (contraste)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)  # barra de cores ao lado de cada mapa
fig.tight_layout()                               # ajusta espaçamentos
fig.savefig(CAMINHO_FIG + 'matriz_correlacao.png', dpi=150, bbox_inches='tight')  # salva PNG
plt.show()                                       # exibe
```

## 13. Exportação dos artefatos

Salva os CSVs com as tabelas descritivas em `banco_de_dados/eda/`. As figuras
já foram salvas em `banco_de_dados/eda/figuras/` ao longo das células anteriores.

### Célula de código: `step13`

```python
# Exporta as tabelas principais da EDA para CSV (sep=';', utf-8-sig p/ abrir no Excel-BR)
desc_global.to_csv(CAMINHO_EDA + 'descritivas_globais.csv',       sep=';', encoding='utf-8-sig')                # descritivas globais (índice = variável)
desc_mun.to_csv(   CAMINHO_EDA + 'descritivas_por_municipio.csv', sep=';', encoding='utf-8-sig', index=False)  # por município (sem índice)
desc_reg.to_csv(   CAMINHO_EDA + 'descritivas_por_regiao.csv',    sep=';', encoding='utf-8-sig', index=False)  # por região (sem índice)
outliers.to_csv(   CAMINHO_EDA + 'outliers.csv',                  sep=';', encoding='utf-8-sig')                # tabela de outliers
miss_mun.drop(columns='_media').to_csv(CAMINHO_EDA + 'missing_por_municipio.csv',   # % de missing por município (sem a coluna auxiliar)
                                        sep=';', encoding='utf-8-sig')
corr_p.to_csv(CAMINHO_EDA + 'correlacao_pearson.csv',  sep=';', encoding='utf-8-sig')   # matriz de Pearson
corr_s.to_csv(CAMINHO_EDA + 'correlacao_spearman.csv', sep=';', encoding='utf-8-sig')   # matriz de Spearman
resumo.to_csv(CAMINHO_EDA + 'elegibilidade_setores.csv', sep=';', encoding='utf-8-sig') # tabela de elegibilidade (Dados_sig)

print('Artefatos exportados em', CAMINHO_EDA)   # log: onde foram salvos os CSVs
print('Figuras em', CAMINHO_FIG)                # log: onde foram salvas as figuras
```
