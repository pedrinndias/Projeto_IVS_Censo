# 01_Extracao_Filtragem_ELSI

> Notebook Jupyter convertido para markdown. Origem: `notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb`

# Fase 3 — Notebook 01: Extração e Filtragem ELSI-Brasil

**Objetivo:** ler os 8 arquivos do Censo Demográfico 2022, filtrar apenas os setores
censitários pertencentes aos **70 municípios da amostra do ELSI-Brasil** e exportar
uma base bruta unificada, pronta para a análise exploratória do Notebook 02.

**Por que existe:** os notebooks anteriores (Fase 1 e Fase 2) processavam o Brasil
inteiro (~468 mil setores de 5.297 municípios). O objetivo científico do projeto é
uma análise **intraurbana** restrita aos 70 municípios do ELSI-Brasil — este notebook
aplica esse filtro pela primeira vez na pipeline.

**Entradas:**
- `dados/Agregados_por_setores_*.csv` — 8 CSVs do Censo 2022 (IBGE)
- `dados/municipios_elsi_brasil.csv` — lista oficial dos 70 municípios ELSI

**Saída:**
- `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` — base bruta filtrada, com sigilo
  preservado (marcação `X` do IBGE mantida).

**Etapas:**
1. Carregar a lista dos 70 municípios ELSI.
2. Ler o arquivo básico do Censo e identificar os setores ELSI (cruzamento por UF +
   nome normalizado).
3. Validar que todos os 70 municípios foram encontrados.
4. Ler os outros 7 arquivos do Censo filtrando por `CD_SETOR` ∈ lista ELSI.
5. Fazer o merge unificado.
6. Classificar morfologia urbana predominante por setor.
7. Auditoria de integridade.
8. Exportar a base bruta filtrada.

---

**Revisão de 09/08/2026 — colunas acrescentadas** (atende às demandas da orientadora
sobre setores rurais, vilas/favelas e índice de envelhecimento):

| Origem | Colunas novas | Para quê |
|---|---|---|
| arquivo básico | `CD_SIT`, `CD_TIPO`, `CD_FCU`, `NM_FCU` | identificar setores de **Favela e Comunidade Urbana** (`CD_TIPO = 1`) e detalhar a situação urbano/rural |
| arquivo demografia | `V01034`–`V01039` (faixas de 15 a 59 anos) | permitir a **Razão de Dependência de Idosos** (60+ / 15–59) do Quadro 1 de Galvão et al. (Hygeia, 2025) |

A base passou de 58 para 68 colunas. O recorte (109.032 setores dos 70 municípios) e
todas as regras metodológicas anteriores permanecem inalterados.

## 1. Imports, caminhos e funções utilitárias

### Célula de código: `setup`

```python
# ── Imports: bibliotecas usadas no notebook ───────────────────────────────────
import os                  # utilidades do sistema (montar caminhos, os.sep = '\' no Windows, criar pastas)
import unicodedata         # normalização de acentos de texto (usado em normalize_name)
import pandas as pd        # manipulação de tabelas (DataFrames) — biblioteca central do projeto
import numpy as np         # operações numéricas vetorizadas (arrays); aqui usado pontualmente
from pathlib import Path   # caminhos como objetos (mais robusto e portátil que concatenar strings)

def _find_project_root():
    """Detecta a raiz do projeto (independente de onde o Jupyter inicia o kernel)."""
    cwd = Path.cwd().resolve()                       # diretório de trabalho atual, em caminho absoluto
    for d in [cwd, *cwd.parents]:                    # percorre a pasta atual e todas as pastas-pai (subindo a árvore)
        # considera "raiz" a 1ª pasta que tenha requirements.txt E a pasta dados/ E a pasta docs/
        if (d / 'requirements.txt').is_file() and (d / 'dados').is_dir() and (d / 'docs').is_dir():
            return d                                 # achou a raiz: devolve esse diretório
    raise RuntimeError(f'Raiz do projeto não encontrada a partir de: {cwd}')  # se nada casar, erro claro

ROOT = _find_project_root()                          # guarda a raiz do projeto
CAMINHO_DADOS = str(ROOT / 'dados') + os.sep         # caminho da pasta de dados brutos + barra final
CAMINHO_BD    = str(ROOT / 'banco_de_dados') + os.sep # caminho da pasta de saídas + barra final
os.makedirs(CAMINHO_BD, exist_ok=True)               # cria a pasta de saída se ainda não existir (sem erro se já existe)
print(f'Raiz do projeto: {ROOT}')                    # log: raiz detectada
print(f'  dados:           {CAMINHO_DADOS}')          # log: caminho de entrada
print(f'  banco_de_dados:  {CAMINHO_BD}')             # log: caminho de saída


def normalize_name(s):
    """Lowercase, sem acentos, espaços colapsados. Para cruzar nomes de municípios."""
    if pd.isna(s):                                   # se o valor for nulo (NaN)...
        return ''                                    # ...devolve texto vazio (evita erro nas etapas seguintes)
    s = str(s).strip().lower()                       # vira texto, remove espaços das pontas e converte p/ minúsculas
    s = unicodedata.normalize('NFD', s)              # decompõe acentos: 'ã' -> 'a' + marca de til separada
    s = ''.join(c for c in s if not unicodedata.combining(c))  # descarta as marcas de acento; sobra a letra base
    return ' '.join(s.split())                       # colapsa espaços repetidos em um só (ex.: 'são  paulo' -> 'sao paulo')


def ler_csv_padronizado(caminho, usecols, rename_cols=None,
                       encoding_list=('utf-8', 'latin1'),
                       sep=';', dtype=str):
    """Lê um CSV tentando utf-8 e, se falhar, latin1 — que decodifica qualquer byte
    (fallback garantido para os CSVs do IBGE). Renomeia colunas-chave se necessário."""
    for enc in encoding_list:                        # tenta cada encoding na ordem (utf-8, depois latin1)
        try:
            df = pd.read_csv(caminho, sep=sep, dtype=dtype, usecols=usecols,  # lê só as colunas pedidas, tudo como texto
                             encoding=enc, low_memory=False)                  # low_memory=False evita aviso de tipo misto
            if rename_cols:                          # se foi pedido renomear alguma coluna...
                df = df.rename(columns=rename_cols)  # ...renomeia (ex.: 'CD_setor' -> 'CD_SETOR' para padronizar a chave)
            print(f'  {os.path.basename(caminho)} — encoding: {enc} — {len(df):,} linhas')  # log: nome, encoding, nº linhas
            return df                                # deu certo: devolve o DataFrame lido
        except UnicodeDecodeError:                   # se este encoding não conseguiu decodificar...
            continue                                 # ...passa para o próximo da lista
    raise UnicodeDecodeError(f'Não foi possível ler {caminho}.')  # nenhum encoding funcionou: erro

print('Setup concluído.')                            # log final desta célula
```

## 2. Carregar a lista dos 70 municípios ELSI-Brasil

Fonte: <https://elsi.cpqrr.fiocruz.br/amostra/>. A lista foi consolidada em
`dados/municipios_elsi_brasil.csv` com as colunas: `regiao`, `uf_codigo` (código IBGE
de 2 dígitos), `uf_sigla`, `nm_municipio`.

### Célula de código: `elsi-load`

```python
# Lê a lista oficial dos 70 municípios ELSI (CSV separado por ';', tudo como texto p/ preservar zeros à esquerda)
df_elsi = pd.read_csv(CAMINHO_DADOS + 'municipios_elsi_brasil.csv', sep=';', dtype=str)
df_elsi['nm_municipio_norm'] = df_elsi['nm_municipio'].map(normalize_name)  # cria coluna com o nome normalizado (sem acento/minúsculo)
# chave composta = código da UF (2 dígitos, com zero à esquerda) + '|' + nome normalizado; identifica o município de forma única
df_elsi['chave_municipio'] = df_elsi['uf_codigo'].str.zfill(2) + '|' + df_elsi['nm_municipio_norm']

assert len(df_elsi) == 70, f'Esperado 70 municípios ELSI, encontrado {len(df_elsi)}'  # trava de segurança: têm que ser exatamente 70
assert df_elsi['chave_municipio'].is_unique, 'Chave (UF + nome) tem duplicatas — verificar lista.'  # nenhuma chave pode repetir

print(f'{len(df_elsi)} municípios ELSI-Brasil carregados.')      # log: quantos municípios entraram
print('\nDistribuição por região:')                              # cabeçalho do próximo log
print(df_elsi['regiao'].value_counts().to_string())             # conta quantos municípios há por região
print('\nDistribuição por UF:')                                  # cabeçalho do próximo log
print(df_elsi.groupby(['regiao', 'uf_sigla']).size().to_string())  # conta municípios por (região, UF)
```

## 3. Identificar os setores ELSI no arquivo básico

O arquivo básico (`Agregados_por_setores_basico_BR_*.csv`) contém um registro por setor
censitário do país (~468 mil) e tem as colunas `CD_SETOR` (chave) e `NM_MUN`. A partir
do `CD_SETOR` derivamos o **código IBGE da UF** (primeiros 2 dígitos) e do **município**
(primeiros 7 dígitos). O cruzamento com a lista ELSI é feito pela chave composta
`(uf_codigo, nm_municipio_normalizado)` — necessário porque há municípios homônimos em
UFs diferentes (ex.: Tabatinga em AM e SP).

### Colunas de classificação territorial (acrescentadas em 09/08/2026)

Além de `SITUACAO` (Urbana/Rural), o arquivo básico traz três colunas que a pipeline
não lia e que são necessárias para as demandas de **exclusão de setores rurais** e de
**contagem de setores de vilas e favelas**:

| Coluna | O que é |
|---|---|
| `CD_SIT` | Código da situação do setor — detalha o par Urbana/Rural |
| `CD_TIPO` | Tipo de setor (especial ou não) — **`1` = Favela e Comunidade Urbana (FCU)** |
| `CD_FCU` / `NM_FCU` | Código e nome da Favela ou Comunidade Urbana à qual o setor pertence |

Correspondência de `CD_SIT` com `SITUACAO`, verificada nos 468.099 setores do Brasil:

| `CD_SIT` | `SITUACAO` | Setores (Brasil) |
|---|---|---:|
| 1, 2, 3 | Urbana | 354.965 |
| 5, 6, 7, 8 | Rural | 112.031 |
| 9 | *(vazia)* | 1.101 |

Os setores com `CD_SIT = 9` têm **`v0001 = 0` sem exceção** (as 1.101 ocorrências no
Brasil): são massas d'água / setores sem população, e é por isso que ficam sem
`SITUACAO`. No recorte ELSI são 78 setores.

`CD_TIPO = 1` equivale exatamente a ter `NM_FCU` preenchido (33.272 setores no Brasil),
o que confirma o código como o marcador de favela/comunidade urbana do Censo 2022.

### Célula de código: `basico-load`

```python
# Colunas que vamos ler do arquivo básico: chave do setor, nome do município, bairro,
# situação urbano/rural, classificação territorial e população total.
# CD_SIT/CD_TIPO/CD_FCU/NM_FCU acrescentadas em 09/08/2026: CD_SIT detalha a situação
# (e explica os setores sem SITUACAO), CD_TIPO=1 marca Favela e Comunidade Urbana.
col_basico = ['CD_SETOR', 'NM_MUN', 'NM_BAIRRO', 'SITUACAO',
              'CD_SIT', 'CD_TIPO', 'CD_FCU', 'NM_FCU',   # classificação territorial (rural/urbano e FCU)
              'v0001']

print('Lendo o arquivo básico do Censo 2022 (~468 mil setores)...')  # log: início da leitura (arquivo grande)
df_basico = ler_csv_padronizado(                                     # usa a função utilitária (tenta utf-8/latin1)
    CAMINHO_DADOS + 'Agregados_por_setores_basico_BR_20250417.csv',  # caminho do arquivo básico
    usecols=col_basico,                                             # lê apenas as colunas acima (economiza memória)
)

# Derivar UF e código de município a partir do CD_SETOR (15 dígitos: UF[2] + MUN[5] + ...)
df_basico['CD_UF'] = df_basico['CD_SETOR'].str[:2]    # código da UF = 2 primeiros dígitos do código do setor
df_basico['CD_MUN'] = df_basico['CD_SETOR'].str[:7]   # código do município = 7 primeiros dígitos (UF + município)
df_basico['NM_MUN_NORM'] = df_basico['NM_MUN'].map(normalize_name)  # nome do município normalizado (p/ cruzar com a lista ELSI)
df_basico['chave_municipio'] = df_basico['CD_UF'] + '|' + df_basico['NM_MUN_NORM']  # mesma chave composta da lista ELSI

print(f'\nTotal de setores no Censo 2022: {len(df_basico):,}')                  # log: nº total de setores do Brasil
print(f'Total de municípios no Censo 2022: {df_basico["CD_MUN"].nunique():,}')  # log: nº de municípios distintos (códigos únicos)

# Conferência das novas colunas no universo nacional (serve de referência para o recorte ELSI)
print('\nCD_SIT × SITUACAO (Brasil):')                                          # log: cruzamento situação detalhada × Urbana/Rural
print(pd.crosstab(df_basico['CD_SIT'], df_basico['SITUACAO'].fillna('(vazia)')).to_string())
print('\nCD_TIPO (Brasil) — 1 = Favela e Comunidade Urbana:')                   # log: distribuição dos tipos de setor
print(df_basico['CD_TIPO'].value_counts(dropna=False).sort_index().to_string())
```

### Célula de código: `elsi-filter`

```python
# Filtrar setores cujo município está na lista ELSI
chaves_elsi = set(df_elsi['chave_municipio'])  # converte as 70 chaves p/ set (busca O(1), bem mais rápida que lista)
df_basico_elsi = df_basico[df_basico['chave_municipio'].isin(chaves_elsi)].copy()  # mantém só os setores cuja chave está no set; .copy() evita SettingWithCopyWarning depois

setores_elsi = set(df_basico_elsi['CD_SETOR'])           # conjunto de códigos de setor ELSI (usado p/ filtrar os outros 7 arquivos)
muns_encontrados = df_basico_elsi['chave_municipio'].unique()  # quais municípios da lista realmente apareceram nos dados

print(f'Setores filtrados: {len(df_basico_elsi):,}')                               # log: nº de setores que sobraram
print(f'Municípios ELSI encontrados: {len(muns_encontrados)} de 70')               # log: quantos dos 70 foram localizados
print(f'Municípios distintos na base filtrada: {df_basico_elsi["CD_MUN"].nunique()}')  # log: confere por código de município
```

### Validação — todos os 70 municípios ELSI foram localizados?

Se algum município não foi encontrado, a célula abaixo lista os faltantes (geralmente
indicam grafia divergente entre a lista ELSI e o IBGE — corrigir em
`dados/municipios_elsi_brasil.csv`).

### Célula de código: `validate`

```python
# municípios da lista ELSI cuja chave NÃO apareceu nos setores encontrados (~ = "não está em")
faltantes = df_elsi[~df_elsi['chave_municipio'].isin(set(muns_encontrados))]

if len(faltantes) == 0:                                  # se a lista de faltantes está vazia...
    print('✅ Todos os 70 municípios ELSI foram localizados no Censo 2022.')  # ...tudo certo
else:
    print(f'⚠️  {len(faltantes)} municípios ELSI NÃO foram encontrados:')     # senão, avisa quantos faltaram
    print(faltantes[['regiao', 'uf_sigla', 'nm_municipio']].to_string(index=False))  # lista os faltantes p/ inspeção
    print('\nProváveis causas: grafia divergente, acento, hífen, ou nome alternativo.')  # dica de diagnóstico
    print('Verifique a coluna NM_MUN do arquivo básico do Censo para a UF em questão.')  # onde investigar

# Resumo de setores por município
resumo_mun = (df_basico_elsi.groupby(['CD_UF', 'NM_MUN'])  # agrupa por UF e nome do município
              .size().rename('n_setores').reset_index()    # conta linhas (setores) por grupo e nomeia a coluna 'n_setores'
              .sort_values(['CD_UF', 'NM_MUN']))            # ordena por UF e nome
print(f'\nResumo (primeiros 10 municípios por contagem de setores):')  # cabeçalho do log
print(resumo_mun.nlargest(10, 'n_setores').to_string(index=False))     # mostra os 10 municípios com mais setores
```

## 4. Ler os demais 7 arquivos do Censo, filtrando por `CD_SETOR`

Como já temos o conjunto de `CD_SETOR` da ELSI, lemos cada um dos outros 7 arquivos e
filtramos imediatamente para reduzir o uso de memória. Cada arquivo é grande
(domicílio2 tem 747 MB, alfabetização 701 MB), por isso a filtragem é feita em
**chunks** de 100 mil linhas.

### Célula de código: `demais-defs`

```python
# Mapeamento de colunas alvo por arquivo (mesmas variáveis usadas na Fase 2)
# ARQUIVOS é um dicionário: cada chave ('dom1', 'dom2'...) descreve um arquivo do Censo,
# quais colunas ler (usecols) e como renomear a coluna-chave do setor (rename).
ARQUIVOS = {
    'dom1': {  # Características do Domicílio - Parte 1 (denominadores domiciliares e morfologia)
        'arquivo': 'Agregados_por_setores_caracteristicas_domicilio1_BR.csv',
        'usecols': ['CD_setor', 'V00001', 'V00002', 'V00005', 'V00006',  # V00001/2 = domicílios; V00005/6 = moradores
                    'V00047', 'V00048', 'V00049', 'V00050', 'V00051', 'V00052',  # tipos de domicílio (morfologia urbana)
                    # V00053-V00058: tipos de domicilio improvisado (DPIO) - habitacao precaria
                    'V00053', 'V00054', 'V00055', 'V00056', 'V00057', 'V00058'],
        'rename': {'CD_setor': 'CD_SETOR'},  # neste arquivo a chave vem como 'CD_setor'; padronizamos p/ 'CD_SETOR'
    },
    'dom2': {  # Características do Domicílio - Parte 2 (saneamento: água, esgoto, lixo, banheiro)
        'arquivo': 'Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv',
        'usecols': ['setor', 'V00112', 'V00113', 'V00114', 'V00115', 'V00116', 'V00117', 'V00118',  # água inadequada
                    'V00312', 'V00313', 'V00314', 'V00315', 'V00316',  # esgoto inadequado
                    'V00398', 'V00399', 'V00400', 'V00401', 'V00402',  # lixo inadequado (V00398 = caçamba; incluída por fidelidade ao IVS-BH 2012)
                    'V00236', 'V00238',  # banheiro de uso comum / sem banheiro nem sanitário (descritivas)
                    # V00495: sem banheiro de uso exclusivo com chuveiro e vaso sanitario
                    'V00495'],
        'rename': {'setor': 'CD_SETOR'},  # aqui a chave vem como 'setor'; padronizamos p/ 'CD_SETOR'
    },
    'alfab': {  # Alfabetização (15+): V00900 = sabe ler/escrever, V00901 = não sabe (analfabetos)
        'arquivo': 'Agregados_por_setores_alfabetizacao_BR.csv',
        'usecols': ['CD_setor', 'V00900', 'V00901'],
        'rename': {'CD_setor': 'CD_SETOR'},
    },
    'raca': {  # Cor ou Raça: V01318 = preta, V01320 = parda, V01321 = indígena
        'arquivo': 'Agregados_por_setores_cor_ou_raca_BR.csv',
        'usecols': ['CD_SETOR', 'V01318', 'V01320', 'V01321'],
        'rename': None,  # aqui a chave já é 'CD_SETOR' — não precisa renomear
    },
    'renda': {  # Renda do responsável: V06004 = rendimento nominal médio mensal (R$)
        'arquivo': 'Agregados_por_setores_renda_responsavel_BR.csv',
        'usecols': ['CD_SETOR', 'V06004'],
        'rename': None,
    },
    'demog': {  # Demografia (faixas etárias) — pirâmide etária completa do setor
        'arquivo': 'Agregados_por_setores_demografia_BR.csv',
        # Bloco etário total (ambos os sexos), conforme dicionário oficial do IBGE:
        #   V01031=0-4  V01032=5-9  V01033=10-14  -> população com MENOS DE 15 ANOS
        #   V01034=15-19  V01035=20-24  V01036=25-29  V01037=30-39  V01038=40-49
        #   V01039=50-59                              -> população de 15 A 59 ANOS
        #   V01040=60-69  V01041=70+                  -> população de 60 ANOS OU MAIS
        # As faixas 15-59 (V01034-V01039) foram acrescentadas em 09/08/2026 para permitir
        # a Razão de Dependência de Idosos (RDI = 60+ / 15-59), conforme Galvão et al.
        # (Hygeia, v.21, 2025, Quadro 1).
        'usecols': ['CD_setor', 'V01031', 'V01032', 'V01033',
                    'V01034', 'V01035', 'V01036', 'V01037', 'V01038', 'V01039',
                    'V01040', 'V01041'],
        'rename': {'CD_setor': 'CD_SETOR'},
    },
    'parent': {  # Parentesco
        'arquivo': 'Agregados_por_setores_parentesco_BR.csv',
        # V01062/V01063: pessoa responsavel por sexo (masculino/feminino)
        'usecols': ['CD_SETOR', 'V01042', 'V01062', 'V01063'],  # V01042 = nº de responsáveis (pessoas) — NÃO usado como denominador
        'rename': None,
    },
}


def ler_filtrado(arquivo, usecols, rename, setores_alvo,
                 encoding_list=('utf-8', 'latin1'), chunksize=100_000):
    """Lê um CSV em chunks, filtrando linhas cujo CD_SETOR está em setores_alvo."""
    caminho = CAMINHO_DADOS + arquivo                       # monta o caminho completo do arquivo
    chave_origem = (rename and next(iter(rename))) or 'CD_SETOR'  # nome da coluna-chave no arquivo de origem (antes de renomear)
    for enc in encoding_list:                               # tenta cada encoding (utf-8, depois latin1)
        try:
            pedacos = []                                    # lista que acumula os pedaços filtrados de cada chunk
            reader = pd.read_csv(caminho, sep=';', dtype=str, usecols=usecols,  # lê em "modo streaming": devolve um iterador de chunks
                                 encoding=enc, chunksize=chunksize, low_memory=False)  # cada chunk tem até 100 mil linhas
            for chunk in reader:                            # processa um pedaço de cada vez (segura a memória)
                if rename:                                  # se precisa renomear a chave...
                    chunk = chunk.rename(columns=rename)    # ...renomeia neste pedaço
                chunk = chunk[chunk['CD_SETOR'].isin(setores_alvo)]  # mantém só as linhas dos setores ELSI
                if len(chunk):                              # se sobrou alguma linha neste pedaço...
                    pedacos.append(chunk)                   # ...guarda o pedaço filtrado
            # junta todos os pedaços num único DataFrame; se nada sobrou, cria um vazio com as colunas certas
            df = pd.concat(pedacos, ignore_index=True) if pedacos else pd.DataFrame(columns=[chave_origem] + list(usecols))
            print(f'  {arquivo} — encoding: {enc} — {len(df):,} setores filtrados')  # log: arquivo, encoding, nº de setores
            return df                                       # deu certo: devolve o resultado filtrado
        except UnicodeDecodeError:                          # encoding falhou...
            continue                                        # ...tenta o próximo
    raise UnicodeDecodeError(f'Não foi possível ler {caminho}.')  # nenhum encoding funcionou: erro

print('Funções definidas.')                                 # log: célula só define coisas (não processa dados ainda)
```

### Célula de código: `demais-load`

```python
print('Lendo e filtrando os 7 arquivos complementares (chunks de 100 mil linhas)...\n')  # log inicial

dfs = {}                                          # dicionário que vai guardar um DataFrame por arquivo (chave -> df filtrado)
for chave, cfg in ARQUIVOS.items():               # percorre cada arquivo descrito em ARQUIVOS
    dfs[chave] = ler_filtrado(cfg['arquivo'], cfg['usecols'], cfg['rename'], setores_elsi)  # lê e filtra pelos setores ELSI

print('\nLeitura concluída.')                      # log final: todos os 7 arquivos foram lidos
```

## 5. Merge unificado pelo `CD_SETOR`

Junção `LEFT JOIN` mantendo todos os setores ELSI do arquivo básico. Se algum setor
estiver ausente nos arquivos complementares, fica com `NaN` nas colunas correspondentes
(será inspecionado na auditoria).

### Célula de código: `merge`

```python
# Ponto de partida do merge: a base básica filtrada, sem as colunas auxiliares que já cumpriram seu papel
df = df_basico_elsi.drop(columns=['NM_MUN_NORM', 'chave_municipio']).copy()  # remove colunas de cruzamento; .copy() = DataFrame independente
for chave in ['dom1', 'dom2', 'alfab', 'raca', 'renda', 'demog', 'parent']:  # junta os 7 arquivos, na ordem
    df = df.merge(dfs[chave], on='CD_SETOR', how='left')   # LEFT JOIN pelo CD_SETOR: mantém todos os setores ELSI; faltantes viram NaN
    print(f'  + {chave}: shape após merge = {df.shape}')   # log: (nº de linhas, nº de colunas) após cada junção

print(f'\nBase unificada: {len(df):,} setores × {len(df.columns)} colunas')  # log final: tamanho da base unificada
```

## 6. Classificador de Morfologia Urbana

Define o **tipo de moradia predominante** por setor a partir das contagens dos arquivos
do IBGE: casa (V00047), casa de vila/condomínio (V00048), apartamento (V00049),
cortiço (V00050), maloca indígena (V00051), estrutura degradada (V00052). Útil para
análises da EDA (perfis morfológicos vs. vulnerabilidade).

### Célula de código: `morf`

```python
# Dicionário: código IBGE do tipo de domicílio -> rótulo legível da morfologia urbana
DIC_MORFOLOGIA = {
    'V00047': 'Casa',
    'V00048': 'Casa de Vila/Condomínio',
    'V00049': 'Apartamento',
    'V00050': 'Cortiço/Casa de Cômodos',
    'V00051': 'Maloca Indígena',
    'V00052': 'Estrutura Degradada/Inacabada',
}

cols_morf = list(DIC_MORFOLOGIA)  # lista das colunas de morfologia (as chaves do dicionário: ['V00047', ..., 'V00052'])
# converte essas colunas (texto) p/ número; 'X' e valores inválidos viram NaN; depois NaN -> 0 (p/ poder comparar contagens)
morf_num = df[cols_morf].apply(pd.to_numeric, errors='coerce').fillna(0)
# idxmax(axis=1) acha, em cada linha (setor), a coluna com maior contagem; .map traduz o código p/ o rótulo legível
df['Moradia_Predominante'] = morf_num.idxmax(axis=1).map(DIC_MORFOLOGIA)
# caso especial: setores em que TODOS os tipos somam 0 (sem informação de moradia) recebem rótulo próprio
df.loc[morf_num.sum(axis=1) == 0, 'Moradia_Predominante'] = 'Indefinido/Sem Moradia'

print(df['Moradia_Predominante'].value_counts(dropna=False).to_string())  # log: quantos setores em cada categoria de moradia
```

## 7. Auditoria de integridade

Verifica: (a) nenhum setor foi duplicado ou perdido no merge; (b) a chave primária está
íntegra; (c) o marcador de sigilo `X` do IBGE foi preservado (necessário para o
tratamento de elegibilidade nas etapas seguintes); (d) variáveis-chave das 8 fontes
estão presentes.

### Célula de código: `audit`

```python
erros = 0                                              # contador de erros graves; se ficar > 0, a base é reprovada
print('=== AUDITORIA DE INTEGRIDADE ===\n')            # cabeçalho do relatório de auditoria

if len(df) == len(df_basico_elsi):                     # checagem 1: o merge não pode ter criado nem perdido linhas
    print(f'[OK] Linhas mantidas: {len(df):,}')        # nº de linhas igual ao esperado -> OK
else:
    print(f'[ERRO] Linhas mudaram: esperado {len(df_basico_elsi):,}, obtido {len(df):,}')  # divergiu -> erro
    erros += 1                                          # incrementa o contador de erros

if df['CD_SETOR'].is_unique and df['CD_SETOR'].notna().all():  # checagem 2: chave primária única e sem nulos
    print('[OK] CD_SETOR íntegra (única, sem nulos).')
else:
    print('[ERRO] CD_SETOR tem duplicatas ou valores nulos.')
    erros += 1

cols_essenciais = ['v0001', 'V00001', 'V00112', 'V00312', 'V00398',   # checagem 3: colunas-chave de cada uma das 8 fontes
                   'V00900', 'V00901', 'V01318', 'V06004', 'V01031',
                   'V01034', 'V01040', 'V01042',                      # faixas 15-59 e 60+ (indicadores de envelhecimento)
                   'CD_SIT', 'CD_TIPO', 'NM_FCU',                     # classificação territorial (rural/urbano e favelas)
                   'Moradia_Predominante']
faltando = [c for c in cols_essenciais if c not in df.columns]  # lista as colunas essenciais que não existem na base
if not faltando:                                       # se a lista está vazia (nada faltando)...
    print(f'[OK] Variáveis essenciais presentes ({len(cols_essenciais)} colunas).')
else:
    print(f'[ERRO] Colunas faltando: {faltando}')
    erros += 1

setores_com_sigilo = df.eq('X').any(axis=1).sum()      # checagem 4: conta setores que têm 'X' (sigilo IBGE) em qualquer coluna
if setores_com_sigilo > 0:                             # esperamos que exista sigilo (a base mantém o 'X' de propósito)
    print(f'[OK] Sigilo do IBGE preservado: {setores_com_sigilo:,} setores contêm "X".')
else:
    print('[ALERTA] Nenhum sigilo "X" detectado — verificar se a leitura está correta.')  # ausência total = suspeito

n_muns = df['CD_MUN'].nunique()                        # checagem 5: nº de municípios distintos na base final
if n_muns == 70:                                       # tem que ser exatamente 70
    print(f'[OK] 70 municípios ELSI presentes.')
else:
    print(f'[ALERTA] {n_muns} municípios distintos na base (esperado 70).')

# checagem 6: coerência das faixas etárias — a soma das 11 faixas tem que reproduzir v0001
faixas_etarias = ['V01031', 'V01032', 'V01033', 'V01034', 'V01035', 'V01036',   # 0-4 até 50-59...
                  'V01037', 'V01038', 'V01039', 'V01040', 'V01041']              # ...mais 60-69 e 70+
_soma_faixas = df[faixas_etarias].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=11)  # soma só quando as 11 existem
_pop = pd.to_numeric(df['v0001'], errors='coerce')     # população total do setor (NaN se sigilosa)
_comparavel = _soma_faixas.notna() & _pop.notna()      # setores em que dá para comparar (sem sigilo dos dois lados)
_divergentes = int((_soma_faixas[_comparavel] != _pop[_comparavel]).sum())  # quantos não batem
if _divergentes == 0:                                  # bateu em todos os setores comparáveis
    print(f'[OK] Faixas etárias somam v0001 nos {int(_comparavel.sum()):,} setores comparáveis.')
else:
    print(f'[ALERTA] {_divergentes:,} setores em que a soma das faixas etárias difere de v0001 (verificar sigilo).')

# checagem 7: CD_TIPO=1 tem que coincidir com NM_FCU preenchido (marcador de favela)
_tipo1 = df['CD_TIPO'].eq('1')                         # setores marcados como Favela e Comunidade Urbana
_com_nome = df['NM_FCU'].notna()                       # setores com nome de FCU preenchido
print(f'[INFO] Setores CD_TIPO=1 (FCU): {int(_tipo1.sum()):,} | com NM_FCU preenchido: {int(_com_nome.sum()):,} '
      f'| divergências: {int((_tipo1 ^ _com_nome).sum()):,}')

# veredito final: verde se erros == 0; vermelho (e instrução de interromper) caso contrário
print('\n' + ('🟢 BASE APROVADA.' if erros == 0 else f'🔴 {erros} ERROS — INTERROMPER.'))

# Panorama territorial do recorte ELSI (insumo direto das demandas de rural e de favelas)
print('\n--- Panorama territorial (70 municípios ELSI) ---')
print(pd.crosstab(df['CD_SIT'], df['SITUACAO'].fillna('(vazia)')).to_string())   # situação detalhada × Urbana/Rural
print('\nCD_TIPO:')
print(df['CD_TIPO'].value_counts(dropna=False).sort_index().to_string())         # tipos de setor no recorte
```

## 8. Exportar a base bruta filtrada

Saída final: `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv`. Mantém o sigilo `X`
intacto — o tratamento de sigilo e o cálculo dos indicadores ficam para etapas
posteriores (após a EDA do Notebook 02).

### Célula de código: `export`

```python
saida = CAMINHO_BD + 'Base_ELSI_Bruta_Censo2022.csv'   # caminho do arquivo de saída
# salva a base: index=False (não grava o índice), sep=';' (padrão IBGE/Excel-BR), utf-8-sig (com BOM, abre certo no Excel)
df.to_csv(saida, index=False, sep=';', encoding='utf-8-sig')

tamanho_mb = os.path.getsize(saida) / (1024 * 1024)    # tamanho do arquivo em MB (bytes / 1024 / 1024)
print(f'✅ Base exportada para: {saida}')                                        # log: onde salvou
print(f'   {len(df):,} setores × {len(df.columns)} colunas — {tamanho_mb:.1f} MB')  # log: dimensões e tamanho

print('\nPróximo passo: abrir o Notebook 02 (Análises Descritivas).')  # orientação de fluxo
```
