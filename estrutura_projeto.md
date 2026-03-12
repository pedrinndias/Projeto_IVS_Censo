# Estrutura do Projeto IVS Censo

Este projeto está organizado para facilitar o processamento, análise e armazenamento de dados do Censo IVS. Abaixo está uma descrição detalhada da estrutura das pastas e arquivos, com foco especial na pasta `ETL`.

## Estrutura Geral

- **LICENSE**: Arquivo de licença do projeto.
- **README.md**: Documentação inicial e instruções de uso.
- **requirements.txt**: Lista de dependências Python necessárias para execução.
- **Base de dados/**: Contém os dados brutos do censo.
    - **IVS Censo 2022/**: Dados do censo de 2022.
        - **Setores Censitários/**: Dados organizados por setores censitários.
- **data/**: Pasta destinada ao armazenamento de dados intermediários ou processados.
- **output/**: Resultados finais e arquivos gerados.
    - **resultados_busca.csv**: Resultado de buscas ou análises.
- **src/**: Código fonte do projeto.
    - **ETL/**: Arquivos de transformação, limpeza e agregação de dados.

---

## Pasta `src/ETL/`

A pasta `ETL` (Extract, Transform, Load) contém arquivos CSV agregados por setores censitários, cada um representando diferentes aspectos dos dados do censo. Abaixo, segue a lista dos arquivos presentes e uma breve descrição de cada um:

### Arquivos e Descrições

- **Agregados_por_setores_alfabetizacao_BR.csv**
  - Contém dados agregados sobre alfabetização por setor censitário no Brasil.
  - Inclui informações sobre o nível de alfabetização da população.

- **Agregados_por_setores_basico_BR_20250417.csv**
  - Dados básicos agregados por setor censitário.
  - Engloba informações demográficas essenciais, como população total, idade, sexo, etc.

- **Agregados_por_setores_caracteristicas_domicilio1_BR.csv**
  - Características dos domicílios (primeira parte), como tipo de construção, material predominante, etc.

- **Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv**
  - Características dos domicílios (segunda parte), incluindo acesso a serviços básicos (água, energia, saneamento).

- **Agregados_por_setores_caracteristicas_domicilio3_BR_20250417.csv**
  - Características dos domicílios (terceira parte), abordando aspectos complementares como posse de bens e equipamentos.

- **Agregados_por_setores_cor_ou_raca_BR.csv**
  - Dados agregados sobre cor ou raça da população por setor censitário.

- **Agregados_por_setores_demografia_BR.csv**
  - Informações demográficas detalhadas, como distribuição etária, sexo, e outros indicadores populacionais.

- **Agregados_por_setores_domicilios_indigenas_BR.csv**
  - Dados sobre domicílios indígenas por setor censitário.

- **Agregados_por_setores_domicilios_quilombolas_BR.csv**
  - Dados sobre domicílios quilombolas por setor censitário.

- **Agregados_por_setores_obitos_BR.csv**
  - Informações sobre óbitos registrados por setor censitário.

- **Agregados_por_setores_parentesco_BR.csv**
  - Dados sobre relações de parentesco entre moradores dos domicílios.

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