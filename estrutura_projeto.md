---
# Documentação da Arquitetura e Estrutura do Projeto

## Visão Geral
Este projeto tem como objetivo unificar, processar e analisar dados do Censo 2022, utilizando Python, Jupyter Notebooks e SQLite para manipulação eficiente de grandes volumes de dados. A estrutura foi desenhada para garantir organização, reprodutibilidade e facilidade de manutenção.

## Estrutura de Pastas e Arquivos

```
├── arquivos_git.txt
├── estrutura_projeto.md
├── LICENSE
├── objetos_git.txt
├── README.md
├── requirements.txt
├── dados/
│   ├── Agregados_por_setores_*.csv
│   └── banco_de_dados/
│       ├── Base_Analitica_IVS_Calculado.csv
│       ├── Base_Bruta_Unificada_Censo2022.csv
│       ├── Base_Censo_Completa_Unificada.csv
│       └── SQL/
├── output/
│   ├── informacoes_agregados.csv
│   └── resultados_busca.csv
├── processed/
├── docs/
├── formatar/
│   ├── busca3.py
│   ├── formatar3.py
│   └── informacoes_agregados.csv
├── notebooks/
│   ├── 01_Unificacao_Base_Censo.ipynb
│   ├── 02_Extracao_Variaveis_Alvo.ipynb
│   ├── 03_Auditoria_Dados.ipynb
│   ├── 04_Calculo_Final_IVS.ipynb
│   └── 05_Formatacao_e_Dicionarios.ipynb
└── src/
    └── ETL/
        ├── mapeamento_variaveis.py
        └── ficheiros_inuteis/
            └── (arquivos CSV não utilizados)
```

## Descrição dos Principais Arquivos e Pastas

- **arquivos_git.txt / objetos_git.txt**: Listas de arquivos e objetos versionados pelo Git.
- **estrutura_projeto.md**: Este documento, detalhando a arquitetura do projeto.
- **requirements.txt**: Dependências Python necessárias para execução.
- **dados/**: Contém todos os arquivos brutos do Censo e subpastas para bancos de dados e SQL.
  - **banco_de_dados/**: Armazena bases intermediárias e finais em CSV e o banco SQLite.
- **output/**: Resultados de buscas e informações agregadas geradas pelo processamento.
- **formatar/**: Scripts e arquivos auxiliares para formatação e busca de dados.
- **notebooks/**: Jupyter Notebooks que documentam e executam cada etapa do pipeline de dados.
- **src/ETL/**: Scripts de ETL (Extract, Transform, Load) e mapeamento de variáveis.
- **processed/**: Pasta reservada para dados já processados (pode ser utilizada em etapas futuras).

## Lógica de Processamento e Fluxo de Dados

1. **Leitura dos Dados Brutos**
   - Os arquivos CSV do Censo são armazenados em `dados/`.
   - O notebook `01_Unificacao_Base_Censo.ipynb` lê esses arquivos em blocos (chunks) para evitar sobrecarga de memória.
   - As colunas de chave (ex: `CD_SETOR`) são padronizadas durante a leitura.

2. **Armazenamento no Banco de Dados**
   - Os dados lidos são salvos em tabelas SQLite dentro de `dados/banco_de_dados/Banco_Censo_Completo.db`.
   - Cada arquivo CSV gera uma tabela correspondente no banco.

3. **Unificação das Tabelas**
   - Um JOIN SQL une todas as tabelas em uma única tabela `base_censo_unificada`.
   - Essa tabela é exportada para `Base_Censo_Completa_Unificada.csv`.

4. **Processamento e Análises**
   - Notebooks subsequentes (`02_Extracao_Variaveis_Alvo.ipynb`, etc.) extraem variáveis, realizam auditorias e calculam indicadores.
   - Scripts em `formatar/` e `src/ETL/` auxiliam na transformação e padronização dos dados.

5. **Geração de Resultados**
   - Resultados finais e intermediários são salvos em `output/` e `dados/banco_de_dados/`.

## Descrição dos Notebooks e Scripts

### Notebooks
- **01_Unificacao_Base_Censo.ipynb**: Unifica e padroniza os dados brutos, salva no SQLite e exporta a base unificada.
- **02_Extracao_Variaveis_Alvo.ipynb**: Extrai variáveis de interesse para análises posteriores.
- **03_Auditoria_Dados.ipynb**: Realiza auditoria e validação dos dados unificados.
- **04_Calculo_Final_IVS.ipynb**: Calcula o Índice de Vulnerabilidade Social (IVS) e outros indicadores.
- **05_Formatacao_e_Dicionarios.ipynb**: Formata os dados finais e gera dicionários de variáveis.

### Scripts Python
- **formatar/busca3.py**: Realiza buscas específicas em arquivos de dados e gera relatórios metodológicos de equivalência de variáveis entre censos.
- **formatar/formatar3.py**: Formata e padroniza arquivos agregados, gera relatórios modulares e dicionários de variáveis.
- **src/ETL/mapeamento_variaveis.py**: Mapeia e documenta variáveis utilizadas no projeto, faz varredura dos arquivos CSV e resume colunas e linhas.

## Resumo do Fluxo de Dados

1. **Entrada**: CSVs brutos em `dados/`
2. **Processamento**: Notebooks e scripts Python
3. **Banco de Dados**: SQLite em `dados/banco_de_dados/`
4. **Saída**: CSVs finais em `output/` e `dados/banco_de_dados/`

## Observações
- O projeto prioriza o uso de chunks para leitura e escrita, evitando problemas de memória.
- Toda a lógica de padronização e unificação está documentada nos notebooks, facilitando a reprodutibilidade.
- Scripts auxiliares podem ser executados separadamente para tarefas específicas de formatação ou busca.

---

Para dúvidas ou contribuições, consulte o README.md ou entre em contato com os responsáveis pelo projeto.

- **Agregados_por_setores_pessoas_indigenas_BR.csv**
  - Informações sobre pessoas indígenas por setor censitário.

- **Agregados_por_setores_pessoas_quilombolas_BR.csv**
  - Informações sobre pessoas quilombolas por setor censitário.

- **Agregados_por_setores_renda_responsavel_BR.csv**
  - Dados sobre a renda do responsável pelo domicílio.

---

Cada arquivo na pasta `ETL` representa um aspecto específico dos dados do censo, permitindo análises segmentadas e detalhadas por setor censitário. A organização facilita a identificação e o uso dos dados conforme a necessidade de cada etapa do projeto.

## Dicionários de Dados

Os dicionários de dados são arquivos essenciais para compreensão das variáveis presentes nos arquivos agregados. Eles detalham nomes, definições, tipos e descrições das variáveis utilizadas nos arquivos .csv do projeto.

Arquivos presentes:

- **dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx** (src/ETL)
- **dicionario_de_dados_renda_responsavel.xlsx** (src/ETL)
- **Dicionario_de_dados_malha_agregados.ods** (src/ETL)
- **dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx** (data)

Esses arquivos fornecem tabelas explicativas sobre cada variável dos arquivos agregados, facilitando a análise e interpretação dos dados.



## Observações sobre os arquivos .csv e binários

Os arquivos .csv agregados na pasta ETL são grandes e podem conter milhares de linhas, cada um representando setores censitários e suas respectivas variáveis. Para entender o significado de cada coluna, consulte os dicionários de dados.

Os arquivos .csv de resultados e comparativos são gerados a partir de análises, buscas ou cruzamentos de variáveis, e servem para documentar e facilitar a interpretação dos dados processados.

Os arquivos binários (.xlsx, .ods) não podem ser lidos diretamente por sistemas de texto, mas são fundamentais para consulta das definições e estrutura dos dados.