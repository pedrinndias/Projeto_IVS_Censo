# 🏗️ Arquitetura e Estrutura do Projeto IVS — Censo 2022

> Última atualização: 06/05/2026

---

## Visão Geral

Este projeto constrói um **Índice de Vulnerabilidade à Saúde (IVS)** intraurbano a partir dos dados agregados por setor censitário do **Censo Demográfico 2022** (IBGE), como parte de uma **Iniciação Científica** na **Fiocruz Minas — IRR**.

**Tecnologias:** Python 3.12 · Pandas · NumPy · Jupyter Notebooks · SQLite · QGIS (futuro)  
**Dependências:** `pandas`, `numpy`, `openpyxl`, `xlsxwriter`

---

## Árvore de Diretórios

```
Projeto_IVS_Censo22/
│
├── 📄 README.md                            Apresentação geral do projeto
├── 📄 DIAGNOSTICO_COMPLETO_PROJETO.md      Diagnóstico + plano de ação (mai/2026)
├── 📄 estrutura_projeto.md                 Este documento
├── 📄 requirements.txt                     Dependências Python
├── 📄 LICENSE                              Licença MIT
├── 📄 .gitignore                           Regras de exclusão do Git
├── 📄 Plano_Artigo_Cientifico_IC_Preenchido.docx
│                                           Roteiro de construção do artigo científico
│
├── 📂 dados/                               DADOS BRUTOS DO IBGE
│   ├── Agregados_por_setores_*.csv         8 CSVs oficiais do Censo 2022 (~2.4 GB)
│   ├── 📂 banco_de_dados/                  Outputs da Fase 1 (legado)
│   │   ├── Base_Analitica_IVS_Calculado.csv
│   │   ├── Base_Bruta_Unificada_Censo2022.csv
│   │   ├── Base_Censo_Completa_Unificada.csv   (1 GB)
│   │   ├── Base_IVS_Final_Formatada.xlsx
│   │   ├── temp_merge1.csv                     (temporário — deletar)
│   │   └── 📂 SQL/                         Bancos SQLite (~4.3 GB)
│   │       ├── Banco_Censo_Completo.db         (3 GB)
│   │       ├── Banco_IVS.db                    (1.2 GB)
│   │       └── Banco_IVS_Essencial.db          (54 MB)
│   ├── 📂 output/                          Resultados de scripts auxiliares
│   │   ├── informacoes_agregados.csv
│   │   ├── resultados_busca.csv
│   │   └── Comparativo_Variaveis.xlsx
│   └── 📂 processed/                       Exports em Excel (legado)
│       ├── Base_Analitica_IVS_Calculado.xlsx
│       └── Base_IVS_Essencial.xlsx
│
├── 📂 banco_de_dados/                      OUTPUTS DA FASE 2 (pipeline ativa)
│   ├── Base_Bruta_Multidimensional_Censo2022.csv       (67 MB)
│   ├── Base_Analitica_Multidimensional_Calculada.csv   (74 MB)
│   ├── Base_Auditoria_Todos_Setores.csv                (104 MB)
│   ├── Base_IVS_Multidimensional_Formatada.xlsx        (57 MB)
│   └── Relatorio_Metodologico_Fase2_Atualizado.xlsx    (12 KB)
│
├── 📂 notebooks/                           PIPELINE DE ANÁLISE
│   ├── 📂 Fase1_IVS_Basico/               Versão inicial — 5 notebooks (legado)
│   │   ├── 01_Unificacao_Base_Censo.ipynb
│   │   ├── 02_Extracao_Variaveis_Alvo.ipynb
│   │   ├── 03_Auditoria_Dados.ipynb
│   │   ├── 04_Calculo_Final_IVS.ipynb
│   │   └── 05_Formatacao_e_Dicionarios.ipynb
│   ├── 📂 Fase2_IVS_Multidimensional/     Versão atual — 4 notebooks (ativa)
│   │   ├── 01_Extracao_Base_Bruta_Completa.ipynb
│   │   ├── 02_Tratamento_e_Calculo_Multidimensional.ipynb
│   │   ├── 03_Formatacao_e_Dicionarios_Fase2.ipynb
│   │   └── 04_Relatorio_Metodologico_e_Auditoria_Final.ipynb
│   └── 📂 banco_de_dados/                 CSV intermediário (duplicata)
│       └── Base_Bruta_Multidimensional_Censo2022.csv
│
├── 📂 docs/                                DOCUMENTAÇÃO E DICIONÁRIOS
│   ├── dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx
│   ├── dicionario_de_dados_renda_responsavel.xlsx
│   ├── Dicionario_de_dados_malha_agregados.ods
│   ├── Relatorio_Metodologico_IVS_2022_Corrigido.xlsx
│   └── Relatorio_Modular_Variaveis.xlsx
│
├── 📂 formatar/                            SCRIPTS AUXILIARES
│   ├── busca3.py                           Gerador do Relatório Metodológico
│   ├── formatar3.py                        Relatório modular de variáveis
│   └── informacoes_agregados.csv           Output do mapeamento
│
├── 📂 src/ETL/                             SCRIPTS DE EXTRAÇÃO
│   ├── mapeamento_variaveis.py             Varredura dos CSVs do Censo
│   └── 📂 ficheiros_inuteis/              CSVs descartados (~4.3 GB)
│
└── 📂 tests/                               (vazia — testes futuros)
```

---

## Fontes de Dados

Os 8 arquivos CSV brutos do IBGE em `dados/` são os dados-fonte imutáveis do projeto:

| # | Arquivo | Dimensão do IVS | Variáveis-chave | Tamanho |
|---|---|---|---|---|
| 1 | `Agregados_por_setores_basico_BR_20250417.csv` | Identificação + população | `CD_SETOR`, `NM_MUN`, `v0001`, `v0005` | 130 MB |
| 2 | `Agregados_por_setores_caracteristicas_domicilio1_BR.csv` | Denominador habitacional | `V00001` (dom. permanentes), `V00002` (improvisados) | 177 MB |
| 3 | `Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv` | Saneamento básico | Água (V00112–V00118), Esgoto, Lixo (V00398–V00402) | 747 MB |
| 4 | `Agregados_por_setores_alfabetizacao_BR.csv` | Educação | `V00900` (pop. 15+), `V00901` (analfabetos) | 701 MB |
| 5 | `Agregados_por_setores_cor_ou_raca_BR.csv` | Vulnerabilidade social | `V01318` (preta), `V01320` (parda), `V01321` (indígena) | 192 MB |
| 6 | `Agregados_por_setores_renda_responsavel_BR.csv` | Renda | `V06004` (rendimento médio mensal) | 26 MB |
| 7 | `Agregados_por_setores_demografia_BR.csv` | Sobrecarga infantil | `V01031`–`V01033` (pop. 0–14 anos) | 85 MB |
| 8 | `Agregados_por_setores_parentesco_BR.csv` | Total de lares reais | `V01042` (responsáveis) | 346 MB |

> Arquivos 7 e 8 são usados **apenas na Fase 2**.

---

## Pipelines de Análise

### Fase 1 — IVS Básico *(legado, supersedida)*

```
dados/*.csv
  │
  ▼  01_Unificacao_Base_Censo.ipynb
  │   Lê 6 CSVs em chunks → SQLite → JOIN → exporta CSV unificado (1 GB)
  │
  ▼  02_Extracao_Variaveis_Alvo.ipynb
  │   Lê apenas colunas essenciais → merge → exporta para SQLite + Excel
  │
  ▼  03_Auditoria_Dados.ipynb
  │   Verifica integridade (linhas, nulos, duplicatas)
  │
  ▼  04_Calculo_Final_IVS.ipynb
  │   Filtro: pop > 0 e dom > 0
  │   Cálculo dos 7 indicadores (0 a 1)
  │   Denominador de saneamento: V00001
  │   Renda: min-max invertido GLOBAL
  │
  ▼  05_Formatacao_e_Dicionarios.ipynb
      Excel formatado com 4 abas (Base + 2 Dicionários + Prova Real)

  Saída → dados/banco_de_dados/Base_Analitica_IVS_Calculado.csv
```

**Características:**
- 6 fontes de dados
- Denominador de saneamento: `V00001` (domicílios particulares permanentes)
- Densidade habitacional: `v0005` (variável pronta do IBGE)
- Indicador econômico: apenas renda invertida simples
- 7 indicadores finais

---

### Fase 2 — IVS Multidimensional *(ativa)*

```
dados/*.csv (8 arquivos)
  │
  ▼  01_Extracao_Base_Bruta_Completa.ipynb
  │   Lê 8 CSVs → merge → classificador de Morfologia Urbana
  │   Auditoria automática de integridade do JOIN
  │
  ▼  02_Tratamento_e_Calculo_Multidimensional.ipynb
  │   Tratamento de sigilo ('X' → -1)
  │   Classificação: OK / SIGILOSO / COLETIVO / ZERADO
  │   Cálculo dos 6 indicadores base (0 a 1)
  │   Proxy de Extrema Pobreza Multidimensional:
  │     = Renda Invertida (40%) + Falta Banheiro (20%)
  │       + Improvisados (20%) + Sobrecarga Infantil (20%)
  │
  ▼  03_Formatacao_e_Dicionarios_Fase2.ipynb
  │   Excel formatado com 4 abas
  │
  ▼  04_Relatorio_Metodologico_e_Auditoria_Final.ipynb
      Relatório De-Para + Mapa de Arquivos + Limitações
      Auditoria final (volume, chave, limites, morfologia)

  Saída → banco_de_dados/Base_Analitica_Multidimensional_Calculada.csv
```

**Características:**
- 8 fontes de dados (inclui demografia e parentesco)
- Denominador de saneamento: `V01042` (total de responsáveis)
- Densidade habitacional: `(V00005 + V00006) / V01042` (cálculo manual)
- Classificação de elegibilidade com coluna `Dados_sig`
- Coluna `Moradia_Predominante` (morfologia urbana)
- 7 indicadores finais (inclui `ind_pobreza_multidimensional`)

---

## Variáveis do IVS

Conforme o **Relatório Metodológico** (`docs/Relatorio_Metodologico_IVS_2022_Corrigido.xlsx`):

### De-Para: Censo 2010 → Censo 2022

| Componente | IVS 2012 (Censo 2010) | Censo 2022 Equivalente | Denominador |
|---|---|---|---|
| **Água inadequada** | V013, V014, V015 | V00112 a V00118 (7 var.) | V00001 |
| **Esgoto inadequado** | V019 a V028 | ⚠️ V00312–V00316 ou V00249–V00253 (*) | V00001 |
| **Lixo inadequado** | V037 a V042 | V00398 a V00402 (5 var.) | V00001 |
| **Analfabetismo** | V068 a V134 | V00901 / V00900 | V00900 (pop. 15+) |
| **Densidade habitacional** | Pop. / dom. ocupados | v0005 (pronta do IBGE) | — |
| **Renda** | % fam. ≤2 SM | V06004 (renda média invertida) | — |
| **Raça/cor** | Pretos + Pardos + Indígenas | V01318 + V01320 + V01321 | v0001 (pop. total) |

> (*) **Inconsistência interna no Relatório Metodológico:** a aba "De_Para" indica V00312–V00316, enquanto a aba "Mapa_de_Arquivos" indica V00249–V00253. Os notebooks usam V00312–V00316. A ser resolvido com o dicionário do IBGE.

### Limitações Documentadas

| O que o IVS 2012 pedia | Limitação no Censo 2022 | Solução adotada |
|---|---|---|
| % chefes com <4 anos de estudo | Dados de anos de instrução não disponibilizados nos agregados | Taxa de analfabetismo (V00901) como substituto |
| % famílias ≤2 salários mínimos | Contagem por faixas salariais não disponível | Rendimento médio (V06004) com normalização invertida |
| Coef. óbitos cardiovasculares | IBGE registrou apenas se houve óbito, sem causa mortis | Dados futuros do DATASUS (Sistema SIM) |

---

## Outputs Gerados

### Fase 1 (legado) → `dados/banco_de_dados/`

| Arquivo | Conteúdo | Tamanho |
|---|---|---|
| `Base_Censo_Completa_Unificada.csv` | Todas as colunas de 6 CSVs unificadas | 1 GB |
| `Base_Bruta_Unificada_Censo2022.csv` | Base com colunas selecionadas | 35 MB |
| `Base_Analitica_IVS_Calculado.csv` | 7 indicadores calculados (0 a 1) | 50 MB |
| `Base_IVS_Final_Formatada.xlsx` | Excel com 4 abas formatadas | 37 MB |
| `SQL/Banco_Censo_Completo.db` | SQLite com todas as tabelas | 3 GB |
| `SQL/Banco_IVS.db` | SQLite filtrado | 1.2 GB |
| `SQL/Banco_IVS_Essencial.db` | SQLite com base essencial | 54 MB |

### Fase 2 (ativa) → `banco_de_dados/`

| Arquivo | Conteúdo | Tamanho |
|---|---|---|
| `Base_Bruta_Multidimensional_Censo2022.csv` | Todas as variáveis antes do cálculo (texto) | 67 MB |
| `Base_Analitica_Multidimensional_Calculada.csv` | 7 indicadores calculados, só setores OK | 74 MB |
| `Base_Auditoria_Todos_Setores.csv` | Base completa (inclui SIGILOSO/COLETIVO/ZERADO) | 104 MB |
| `Base_IVS_Multidimensional_Formatada.xlsx` | Excel com 4 abas (Base + Dicionários + Prova) | 57 MB |
| `Relatorio_Metodologico_Fase2_Atualizado.xlsx` | De-Para + Mapa de Arquivos + Limitações | 12 KB |

---

## Documentação de Referência

| Arquivo | Localização | Descrição |
|---|---|---|
| `dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx` | `docs/` | Dicionário oficial do IBGE — define todas as variáveis dos CSVs agregados |
| `dicionario_de_dados_renda_responsavel.xlsx` | `docs/` | Dicionário específico do arquivo de renda |
| `Dicionario_de_dados_malha_agregados.ods` | `docs/` | Dicionário da malha territorial (shapefiles) |
| `Relatorio_Metodologico_IVS_2022_Corrigido.xlsx` | `docs/` | De-Para de variáveis (2010→2022), limitações e mapa de arquivos |
| `Relatorio_Modular_Variaveis.xlsx` | `docs/` | Relatório detalhado de cada coluna por arquivo CSV |

---

## Scripts Auxiliares

### `formatar/busca3.py`
Gera o `Relatorio_Metodologico_IVS_2022_Corrigido.xlsx`. Contém o mapeamento de equivalência entre variáveis do Censo 2010 e 2022 em 3 abas: De-Para, Limitações, Mapa de Arquivos.

### `formatar/formatar3.py`
Gera o `Relatorio_Modular_Variaveis.xlsx`. Cruza os dicionários de dados oficiais com a lista de colunas de cada CSV para produzir um relatório modular com uma aba por arquivo.

### `src/ETL/mapeamento_variaveis.py`
Script de varredura que lê os cabeçalhos e conta linhas de cada CSV agregado, gerando `informacoes_agregados.csv`.

---

## Fluxo de Dados (Visão Macro)

```
┌─────────────────────────────────────────────────┐
│              IBGE — Censo 2022                  │
│         8 CSVs agregados por setor              │
│              dados/*.csv (~2.4 GB)              │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│         01_Extracao_Base_Bruta_Completa          │
│  Leitura seletiva + merge + morfologia urbana   │
│  Auditoria automática de integridade            │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│      02_Tratamento_e_Calculo_Multidimensional    │
│  Sigilo (X→-1) → Elegibilidade (Dados_sig)      │
│  Proporções de risco (0 a 1)                    │
│  Proxy de Extrema Pobreza Multidimensional       │
│  Normalização Min-Max para renda e densidade     │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│       03_Formatacao_e_Dicionarios_Fase2          │
│  Excel premium com 4 abas formatadas            │
│  Dicionários de dados e aplicação               │
│  Prova Real Estatística                         │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│   04_Relatorio_Metodologico_e_Auditoria_Final    │
│  De-Para de variáveis (2010→2022)               │
│  Mapa de Arquivos + Limitações + Soluções        │
│  Auditoria: volume, chave, limites, morfologia  │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              OUTPUTS FINAIS                      │
│  banco_de_dados/*.csv + *.xlsx                  │
│                                                  │
│  (futuro) → QGIS para mapas temáticos           │
└─────────────────────────────────────────────────┘
```

---

## Problemas Conhecidos e Pendências

Para o detalhamento completo, consulte [`DIAGNOSTICO_COMPLETO_PROJETO.md`](DIAGNOSTICO_COMPLETO_PROJETO.md).

| # | Problema | Status |
|---|---|---|
| 0 | Ausência do filtro ELSI-Brasil (70 municípios) — analisou Brasil inteiro | 🔴 Bloqueante |
| 1 | Variáveis de esgoto inconsistentes no Relatório Metodológico | 🔴 A resolver |
| 2 | Normalização de renda global (deveria ser por município) | 🔴 A resolver |
| 3 | Denominadores divergentes entre Relatório e Fase 2 | 🔴 A resolver |
| 4 | Duas pipelines paralelas coexistindo | 🟡 Organizar |
| 5 | ~8 GB de dados duplicados/obsoletos | 🟡 Limpar |

---

> Para contribuições ou dúvidas, consulte o `README.md` ou entre em contato com o pesquisador responsável.