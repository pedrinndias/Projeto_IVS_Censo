# Projeto IVS — Índice de Vulnerabilidade à Saúde (Censo 2022)

## Objetivo

Construir um **Índice de Vulnerabilidade à Saúde (IVS)** intraurbano a partir dos dados agregados por setor censitário do **Censo Demográfico 2022 (IBGE)**, para os **70 municípios da amostra do ELSI-Brasil** (Estudo Longitudinal da Saúde dos Idosos Brasileiros).

O projeto faz parte de uma **Iniciação Científica** vinculada à **Fiocruz Minas — IRR**, na área de Saúde Coletiva, Saúde Urbana e Epidemiologia Espacial.

## Status Atual

> ⚠️ **Projeto em reestruturação** — veja [`DIAGNOSTICO_COMPLETO_PROJETO.md`](DIAGNOSTICO_COMPLETO_PROJETO.md) para detalhes.

| Etapa | Status |
|---|---|
| Obtenção dos dados brutos do Censo 2022 | ✅ Concluída |
| Mapeamento e dicionários de variáveis | ✅ Concluída |
| Pipeline ETL (extração, unificação, cálculo) | ⚠️ Requer correções |
| Filtro dos 70 municípios ELSI-Brasil | 🔴 Pendente |
| Normalização de renda por município | 🔴 Pendente |
| Validação de variáveis de esgoto | 🔴 Pendente |
| Mapas temáticos (QGIS) | 🔴 Pendente |
| Redação do artigo científico | 🔴 Pendente |

## Metodologia

O IVS é um indicador composto que sintetiza **7 variáveis** em **2 dimensões**, calculado ao nível do setor censitário:

| Dimensão | Indicadores | Variáveis do Censo 2022 |
|---|---|---|
| **Saneamento** | Água inadequada | V00112 a V00118 |
| | Esgoto inadequado | *(em validação)* |
| | Lixo inadequado | V00398 a V00402 |
| **Socioeconômica** | Analfabetismo (15+ anos) | V00901 / V00900 |
| | Densidade habitacional | *(em validação)* |
| | Renda (min-max invertido) | V06004 |
| | Raça/cor (proxy de vulnerabilidade social) | V01318 + V01320 + V01321 |

A metodologia é baseada no **IVS de Belo Horizonte (SMS-BH, 2012/2013)** e complementada pelo **Índice de Saúde Urbana (ISU)** de Passarelli-Araujo (2023).

## Estrutura de Pastas

```
Projeto_IVS_Censo22/
│
├── dados/                                  # Dados brutos do IBGE (8 CSVs agregados por setor)
│   ├── Agregados_por_setores_*.csv         #   ~2.4 GB — dados-fonte imutáveis
│   ├── banco_de_dados/                     #   Outputs da Fase 1 (legado)
│   │   ├── SQL/                            #     Bancos SQLite (~4.3 GB)
│   │   └── *.csv, *.xlsx                   #     Bases intermediárias/finais
│   ├── output/                             #   Resultados de scripts auxiliares
│   └── processed/                          #   Dados formatados em Excel
│
├── banco_de_dados/                         # Outputs da Fase 2 (pipeline ativa)
│   ├── Base_Bruta_Multidimensional_Censo2022.csv
│   ├── Base_Analitica_Multidimensional_Calculada.csv
│   ├── Base_Auditoria_Todos_Setores.csv
│   ├── Base_IVS_Multidimensional_Formatada.xlsx
│   └── Relatorio_Metodologico_Fase2_Atualizado.xlsx
│
├── notebooks/                              # Jupyter Notebooks (pipeline de análise)
│   ├── Fase1_IVS_Basico/                   #   Fase 1 — versão inicial (5 notebooks)
│   │   ├── 01_Unificacao_Base_Censo.ipynb
│   │   ├── 02_Extracao_Variaveis_Alvo.ipynb
│   │   ├── 03_Auditoria_Dados.ipynb
│   │   ├── 04_Calculo_Final_IVS.ipynb
│   │   └── 05_Formatacao_e_Dicionarios.ipynb
│   ├── Fase2_IVS_Multidimensional/         #   Fase 2 — versão atual (4 notebooks)
│   │   ├── 01_Extracao_Base_Bruta_Completa.ipynb
│   │   ├── 02_Tratamento_e_Calculo_Multidimensional.ipynb
│   │   ├── 03_Formatacao_e_Dicionarios_Fase2.ipynb
│   │   └── 04_Relatorio_Metodologico_e_Auditoria_Final.ipynb
│   └── banco_de_dados/                     #   CSV intermediário (duplicata)
│
├── docs/                                   # Dicionários de dados e relatórios
│   ├── dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx
│   ├── dicionario_de_dados_renda_responsavel.xlsx
│   ├── Dicionario_de_dados_malha_agregados.ods
│   ├── Relatorio_Metodologico_IVS_2022_Corrigido.xlsx
│   └── Relatorio_Modular_Variaveis.xlsx
│
├── formatar/                               # Scripts auxiliares de formatação
│   ├── busca3.py                           #   Relatório de equivalência de variáveis
│   └── formatar3.py                        #   Relatório modular cruzando dicionários
│
├── src/ETL/                                # Scripts de extração e mapeamento
│   ├── mapeamento_variaveis.py             #   Varredura dos CSVs do Censo
│   └── ficheiros_inuteis/                  #   CSVs descartados (~4.3 GB)
│
├── tests/                                  # (vazia — testes futuros)
│
├── DIAGNOSTICO_COMPLETO_PROJETO.md         # Diagnóstico detalhado do projeto
├── Plano_Artigo_Cientifico_IC_Preenchido.docx  # Plano do artigo científico
├── estrutura_projeto.md                    # Documentação da arquitetura (desatualizada)
├── requirements.txt                        # Dependências Python
└── LICENSE                                 # Licença MIT
```

## Pipelines de Análise

O projeto possui **duas versões** da pipeline, desenvolvidas sequencialmente:

### Fase 1 — IVS Básico *(legado)*
- 5 notebooks em `notebooks/Fase1_IVS_Basico/`
- 6 fontes de dados, denominador baseado em domicílios permanentes (V00001)
- Indicador de renda simples (normalização min-max invertida global)
- Saída: `dados/banco_de_dados/Base_Analitica_IVS_Calculado.csv`

### Fase 2 — IVS Multidimensional *(ativa)*
- 4 notebooks em `notebooks/Fase2_IVS_Multidimensional/`
- 8 fontes de dados (inclui demografia e parentesco)
- Denominador baseado em responsáveis (V01042 — "total de lares reais")
- Classificação de elegibilidade: `OK` / `SIGILOSO` / `COLETIVO` / `ZERADO`
- Proxy de Extrema Pobreza Multidimensional (renda 40% + falta banheiro 20% + improvisados 20% + sobrecarga infantil 20%)
- Saída: `banco_de_dados/Base_Analitica_Multidimensional_Calculada.csv`

## Problemas Conhecidos

1. **Ausência do filtro ELSI-Brasil** — a pipeline processa todos os 5.297 municípios brasileiros (~450k setores) em vez de apenas os 70 municípios ELSI
2. **Normalização de renda global** — deveria ser por município para capturar desigualdades intraurbanas
3. **Variáveis de esgoto inconsistentes** — `busca3.py` usa V00249-V00253, notebooks usam V00312-V00316
4. **Dados duplicados** — ~8 GB de arquivos obsoletos/duplicados espalhados pelo projeto

Veja [`DIAGNOSTICO_COMPLETO_PROJETO.md`](DIAGNOSTICO_COMPLETO_PROJETO.md) para o detalhamento completo e plano de ação.

## Dados Utilizados

| Arquivo do Censo 2022 | Dimensão do IVS | Tamanho |
|---|---|---|
| `Agregados_por_setores_basico_BR_20250417.csv` | Filtros e população base | 130 MB |
| `Agregados_por_setores_caracteristicas_domicilio1_BR.csv` | Denominador habitacional | 177 MB |
| `Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv` | Saneamento básico | 747 MB |
| `Agregados_por_setores_alfabetizacao_BR.csv` | Educação / Escolaridade | 701 MB |
| `Agregados_por_setores_cor_ou_raca_BR.csv` | Vulnerabilidade social | 192 MB |
| `Agregados_por_setores_renda_responsavel_BR.csv` | Renda (base financeira) | 26 MB |
| `Agregados_por_setores_demografia_BR.csv` | Sobrecarga infantil (Fase 2) | 85 MB |
| `Agregados_por_setores_parentesco_BR.csv` | Total de lares reais (Fase 2) | 346 MB |

Fonte: [IBGE — Censo Demográfico 2022 — Agregados por Setores Censitários](https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html)

## Como Executar

### Pré-requisitos
```
Python 3.10+
```

### Instalação
```bash
pip install pandas numpy openpyxl xlsxwriter
```

### Execução
Os notebooks devem ser executados na ordem numérica dentro da pasta da fase desejada:

```
notebooks/Fase2_IVS_Multidimensional/
  01 → 02 → 03 → 04
```

> **Atenção:** A execução completa pode demorar vários minutos e consumir bastante memória RAM devido ao tamanho dos CSVs (~2.4 GB de dados brutos).

## Referências Metodológicas

- SMS-BH. *Índice de Vulnerabilidade da Saúde 2012*. Belo Horizonte: Secretaria Municipal de Saúde, 2013.
- Passarelli-Araujo H. *Mapeando as disparidades socioeconômicas de saúde urbana: um estudo comparativo entre seis capitais brasileiras*. Rev. bras. Est. Pop., v.40, 1-25, 2023.
- Caiaffa WT et al. *Saúde urbana, cidades e a interseção de sistemas*. Rio de Janeiro: Fiocruz, 2021.
- Buss PM, Pellegrini Filho A. *A saúde e seus determinantes sociais*. Physis, v.17, n.1, p.77-93, 2007.

## Créditos

**Pesquisador:** Pedro Dias Soares  
**Instituição:** Fiocruz Minas — IRR  
**Área:** Saúde Coletiva — Saúde Urbana e Epidemiologia Espacial  
**Período:** Março/2026 – Fevereiro/2027  
**Licença:** MIT (ver [LICENSE](LICENSE))