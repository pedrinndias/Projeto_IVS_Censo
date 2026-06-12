# Projeto IVS — Índice de Vulnerabilidade à Saúde (Censo 2022)

## Objetivo

Construir um **Índice de Vulnerabilidade à Saúde (IVS)** intraurbano a partir dos dados agregados por setor censitário do **Censo Demográfico 2022 (IBGE)**, para os **70 municípios da amostra do ELSI-Brasil** (Estudo Longitudinal da Saúde dos Idosos Brasileiros).

O projeto faz parte de uma **Iniciação Científica** vinculada à **Fiocruz Minas — IRR**, na área de Saúde Coletiva, Saúde Urbana e Epidemiologia Espacial.

> **Documento mestre:** [`GUIA_DO_PROJETO.md`](GUIA_DO_PROJETO.md) — versão atualizada e canônica de objetivos, metodologia, estado e plano.
> **Diagnóstico técnico mais recente:** [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md).

## Status Atual

A pipeline ativa é a **Fase 3 (`notebooks/Fase3_EDA_ELSI/`)**, que aplica o filtro pelos 70 municípios do ELSI-Brasil e produz a EDA (análise exploratória) sobre 106.281 setores OK. As Fases 1 e 2 estão arquivadas em [`Backup/`](Backup/) como histórico.

| Etapa | Status |
|---|---|
| Obtenção dos dados brutos do Censo 2022 | ✅ Concluída |
| Mapeamento e dicionários de variáveis | ✅ Concluída |
| Lista oficial dos 70 municípios ELSI-Brasil ([`dados/municipios_elsi_brasil.csv`](dados/municipios_elsi_brasil.csv)) | ✅ Concluída |
| Fase 3 — Notebook 01 (extração + filtro ELSI) | ✅ Concluída |
| Fase 3 — Notebook 02 (análises descritivas / EDA) | ✅ Concluída |
| Validação das variáveis de esgoto (V00249–V00253 vs V00312–V00316) | 🟡 Diagnóstico empírico no Notebook 02 (célula `step4b`); decisão final pendente |
| Normalização de renda por município | 🔴 Pendente (a fazer no Notebook 03) |
| Análise fatorial / ACP — definição dos pesos | 🔴 Pendente (Notebook 04) |
| Cálculo do IVS final + categorização em 4 faixas | 🔴 Pendente (Notebook 05) |
| Mapas temáticos (QGIS 3.x) | 🔴 Pendente |
| Redação do artigo científico | 🟡 Plano preenchido em `docs/Plano_Artigo_Cientifico_IC_Preenchido.docx` |

## Metodologia

O IVS é um indicador composto que sintetiza **7 variáveis** em **2 dimensões**, calculado ao nível do setor censitário.

A operacionalização adotada na pipeline ativa (Fase 3) segue o padrão do **IVS-BH 2012**, ancorada no denominador domiciliar **V00001 (Domicílios Particulares Permanentes Ocupados)** — o equivalente no Censo 2022 do `V002` (Dom_part_p) do Censo 2010 usado pelo IVS-BH. Decisão consolidada na revisão metodológica de **22/05/2026** (orientadora): o `V01042` do arquivo de parentesco é uma **contagem de pessoas responsáveis**, não de domicílios, e por isso foi descartado como denominador. O `V01042` segue sendo extraído apenas para auditoria de setores 100% coletivos.

| Dimensão | Indicador | Censo 2022 (numerador) | Denominador |
|---|---|---|---|
| **Saneamento** | Água inadequada | V00112 a V00118 (7 vars.) | **V00001** |
| | Esgoto inadequado | V00312 a V00316 *(faixa em validação — ver §Problemas Conhecidos)* | **V00001** |
| | Lixo inadequado | V00398 a V00402 (5 vars.) | **V00001** |
| **Socioeconômica** | Analfabetismo (15+) | V00901 | **V00900 + V00901** (total de pessoas 15+) |
| | Densidade habitacional | V00005 + V00006 | **V00001 + V00002** *(reproduz o V0005 do IBGE)* |
| | Renda (invertida no índice) | V06004 (rendimento médio mensal) | — |
| | Raça/cor (pretos + pardos + indígenas) | V01318 + V01320 + V01321 | v0001 (pop. total) |

A metodologia é baseada no **IVS de Belo Horizonte (SMS-BH, 2012/2013)** e complementada pelo **Índice de Saúde Urbana (ISU)** de Passarelli-Araujo (2023).

### Limitações Documentadas

| Item exigido no IVS 2012 | Limitação no Censo 2022 | Solução adotada |
|---|---|---|
| % chefes com <4 anos de estudo | Anos de instrução não disponíveis nos agregados | Taxa de analfabetismo (V00901 / (V00900 + V00901)) |
| % famílias ≤2 salários mínimos | Contagem por faixa salarial não disponível | Rendimento médio (V06004) com normalização invertida |
| Coef. óbitos por doenças cardiovasculares | IBGE registrou apenas se houve óbito, sem causa | Buscar DATASUS (Sistema SIM) futuramente |

## Estrutura de Pastas

```
Projeto_IVS_Censo22/
│
├── README.md                          Este arquivo (apresentação geral)
├── GUIA_DO_PROJETO.md                 Documento mestre de retomada (canônico)
├── requirements.txt                   Dependências Python
├── LICENSE                            Licença MIT
│
├── dados/                             Dados brutos do IBGE (~2.4 GB, imutáveis)
│   ├── Agregados_por_setores_*.csv    8 CSVs oficiais do Censo 2022
│   ├── municipios_elsi_brasil.csv     Lista oficial dos 70 municípios ELSI
│   ├── output/                        Outputs de scripts auxiliares
│   └── processed/                     Exports em Excel (legado)
│
├── banco_de_dados/                    Outputs da pipeline ativa (Fase 3)
│   ├── Base_ELSI_Bruta_Censo2022.csv  Saída do Notebook 01 (filtrada por ELSI)
│   └── eda/                           Saídas do Notebook 02 (EDA)
│       ├── descritivas_globais.csv
│       ├── descritivas_por_municipio.csv
│       ├── descritivas_por_regiao.csv
│       ├── outliers.csv
│       ├── missing_por_municipio.csv
│       ├── correlacao_pearson.csv
│       ├── correlacao_spearman.csv
│       ├── elegibilidade_setores.csv
│       ├── diagnostico_proporcoes_fora_intervalo.csv    (auditoria C1)
│       ├── diagnostico_esgoto_312_vs_249.csv            (auditoria C2)
│       ├── extremos_razao_moradores.csv                 (auditoria R4)
│       └── figuras/                                     histogramas, boxplots, correlação, missing
│
├── notebooks/Fase3_EDA_ELSI/          Pipeline ativa
│   ├── 01_Extracao_Filtragem_ELSI.ipynb
│   ├── 02_Analises_Descritivas.ipynb
│   └── README.md
│
├── docs/                              Documentação-fonte
│   ├── Cálculo IVS2012.docx
│   ├── guia_analises.docx
│   ├── indice_vulnerabilidade2012 (2).pdf
│   ├── Plano_Artigo_Cientifico_IC_Preenchido.docx
│   ├── Plano de trabalho.pdf
│   ├── Relatorio_EDA_Fase3_IVS_ELSI.{md,docx}
│   ├── Apresentacao_EDA_Fase3_IVS_ELSI.pptx
│   └── Relatorio_Integridade_Projeto.md    Diagnóstico técnico mais recente
│
├── Backup/                            Legados — Fases 1 e 2, scripts antigos
│   ├── Fase1_IVS_Basico/              5 notebooks (sem filtro ELSI)
│   ├── Fase2_IVS_Multidimensional/    4 notebooks (sem filtro ELSI, com V01042)
│   ├── ETL/, formatar/, banco_de_dados/
│   └── DIAGNOSTICO_COMPLETO_PROJETO.md
│
└── tests/                             Testes unitários (sanity-checks da pipeline)
```

## Problemas Conhecidos

Lista resumida — detalhamento técnico em [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md).

| # | Problema | Gravidade |
|---|---|---|
| 1 | **Variáveis de esgoto** — V00312–V00316 vs V00249–V00253. O Notebook 02 inclui um diagnóstico empírico (célula `step4b`) e exporta `diagnostico_esgoto_312_vs_249.csv` para subsidiar a decisão final. | 🟡 Pendente |
| 2 | **Normalização de renda global** — usa min/max global; será trocada para por município no Notebook 03 (a criar). | 🟡 Pendente (próxima fase) |
| 3 | ~~**Ausência do filtro ELSI**~~ | ✅ Resolvido (Fase 3) |
| 4 | ~~**Denominadores divergentes**~~ — consolidado **V00001** (Dom. Particulares Permanentes Ocupados) na revisão de 22/05/2026; `V01042` descartado (é contagem de pessoas, não de domicílios). | ✅ Resolvido |
| 5 | **Dados duplicados em `Backup/`** — ~8 GB de arquivos obsoletos. Limpeza opcional. | 🟢 Organizacional |

## Dados Utilizados

| Arquivo do Censo 2022 | Dimensão do IVS | Tamanho |
|---|---|---|
| `Agregados_por_setores_basico_BR_20250417.csv` | Filtros e população base (v0001, v0005) | 130 MB |
| `Agregados_por_setores_caracteristicas_domicilio1_BR.csv` | Denominador habitacional (V00001, V00002, V00005, V00006) | 177 MB |
| `Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv` | Saneamento (água, esgoto, lixo) | 747 MB |
| `Agregados_por_setores_alfabetizacao_BR.csv` | Educação (V00900, V00901) | 701 MB |
| `Agregados_por_setores_cor_ou_raca_BR.csv` | Raça/cor (V01318, V01320, V01321) | 192 MB |
| `Agregados_por_setores_renda_responsavel_BR.csv` | Renda (V06004) | 26 MB |
| `Agregados_por_setores_demografia_BR.csv` | Sobrecarga infantil (futuro) | 85 MB |
| `Agregados_por_setores_parentesco_BR.csv` | Total de Responsáveis (V01042) | 346 MB |

Fonte: [IBGE — Censo Demográfico 2022 — Agregados por Setores Censitários](https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html).

## Como Executar

### Pré-requisitos
- Python 3.10+
- Os 8 CSVs do Censo 2022 em `dados/` (não versionados — baixar do IBGE)

### Instalação
```bash
pip install -r requirements.txt
```

### Execução da Pipeline Ativa
Os notebooks da Fase 3 devem ser executados na ordem numérica:

```
notebooks/Fase3_EDA_ELSI/  →  01 → 02
```

- **Notebook 01:** extrai e filtra → produz `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` (109.032 setores × 47 colunas, ~17 MB).
- **Notebook 02:** EDA completa → produz 11 CSVs e 4 figuras em `banco_de_dados/eda/`.

> A execução completa consome bastante RAM e tempo (~2.4 GB de CSVs brutos). Os notebooks leem apenas as colunas necessárias e processam os arquivos maiores em chunks.

### Testes Sanity
```bash
python -m pytest tests/ -v
```

## Referências Metodológicas

- SMS-BH. *Índice de Vulnerabilidade da Saúde 2012*. Belo Horizonte: Secretaria Municipal de Saúde, 2013.
- Passarelli-Araujo H. *Mapeando as disparidades socioeconômicas de saúde urbana: um estudo comparativo entre seis capitais brasileiras*. Rev. bras. Est. Pop., v.40, 1-25, 2023.
- Caiaffa WT et al. *Saúde urbana, cidades e a interseção de sistemas*. Rio de Janeiro: Fiocruz, 2021.
- Buss PM, Pellegrini Filho A. *A saúde e seus determinantes sociais*. Physis, v.17, n.1, p.77-93, 2007.
- Matos DAS, Rodrigues EC. *Análise fatorial*. Brasília: Enap, 2019.

## Créditos

**Pesquisador:** Pedro Dias Soares
**Instituição:** Fiocruz Minas — IRR
**Área:** Saúde Coletiva — Saúde Urbana e Epidemiologia Espacial
**Período:** Março/2026 – Fevereiro/2027
**Licença:** MIT (ver [LICENSE](LICENSE))
