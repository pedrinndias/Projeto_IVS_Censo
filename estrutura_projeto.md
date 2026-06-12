# 🏗️ Arquitetura e Estrutura do Projeto IVS — Censo 2022

> Última atualização: 22/05/2026 (revisão metodológica: denominador V00001 + taxa de analfabetismo)

---

## Visão Geral

Este projeto constrói um **Índice de Vulnerabilidade à Saúde (IVS)** intraurbano a partir dos dados agregados por setor censitário do **Censo Demográfico 2022** (IBGE), restrito aos **70 municípios da amostra do ELSI-Brasil**, como parte de uma **Iniciação Científica** na **Fiocruz Minas — IRR**.

**Tecnologias:** Python 3.10+ · Pandas · NumPy · Matplotlib · Jupyter Notebooks · QGIS (futuro)
**Dependências:** ver [`requirements.txt`](requirements.txt) (`pandas`, `numpy`, `matplotlib`, `openpyxl`, `xlsxwriter`)

> **Documento mestre:** [`GUIA_DO_PROJETO.md`](GUIA_DO_PROJETO.md) — objetivos, metodologia, estado e plano (canônico).
> **Diagnóstico técnico:** [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md).

---

## Árvore de Diretórios (estado atual)

```
Projeto_IVS_Censo22/
│
├── 📄 README.md                       Apresentação geral do projeto
├── 📄 GUIA_DO_PROJETO.md              Documento mestre de retomada (canônico)
├── 📄 estrutura_projeto.md            Este documento
├── 📄 requirements.txt                Dependências Python
├── 📄 LICENSE                         Licença MIT
│
├── 📂 dados/                          DADOS BRUTOS DO IBGE (~2.4 GB, não versionados)
│   ├── Agregados_por_setores_*.csv    8 CSVs oficiais do Censo 2022 (baixar do IBGE)
│   └── municipios_elsi_brasil.csv     Lista oficial dos 70 municípios ELSI (versionada)
│
├── 📂 notebooks/Fase3_EDA_ELSI/       PIPELINE ATIVA
│   ├── 01_Extracao_Filtragem_ELSI.ipynb     Extrai os 8 CSVs, filtra os 70 municípios
│   ├── 02_Analises_Descritivas.ipynb        EDA completa (descritivas, correlações, missing)
│   └── README.md
│
├── 📂 banco_de_dados/                 OUTPUTS DA PIPELINE ATIVA (Fase 3)
│   ├── Base_ELSI_Bruta_Censo2022.csv  Saída do Notebook 01 (filtrada por ELSI, ~17 MB)
│   ├── 📂 eda/                        Saídas do Notebook 02 (descritivas + figuras)
│   │   ├── descritivas_globais.csv
│   │   ├── descritivas_por_municipio.csv
│   │   ├── descritivas_por_regiao.csv
│   │   ├── outliers.csv
│   │   ├── missing_por_municipio.csv
│   │   ├── correlacao_pearson.csv  ·  correlacao_spearman.csv
│   │   ├── elegibilidade_setores.csv
│   │   ├── diagnostico_proporcoes_fora_intervalo.csv   (auditoria C1)
│   │   ├── diagnostico_esgoto_312_vs_249.csv           (auditoria C2)
│   │   ├── extremos_razao_moradores.csv                (auditoria R4)
│   │   ├── auditoria_analfabetismo_municipio.csv
│   │   └── 📂 figuras/               histogramas, boxplots, correlação, missing (PNG)
│   └── 📂 entrega_orientadora/        Bases entregues à orientadora (CSV + SQLite .db)
│       ├── Base_ELSI_70Municipios_Censo2022.{csv,db}
│       ├── Base_BeloHorizonte_Censo2022.{csv,db}
│       └── README.md                 ← fonte da verdade da metodologia atual
│
├── 📂 docs/                           DOCUMENTAÇÃO-FONTE E RELATÓRIOS
│   ├── Cálculo IVS2012.docx           Metodologia operacional do IVS-BH
│   ├── guia_analises.docx             Framework FIOCRUZ de EDA
│   ├── indice_vulnerabilidade2012 (2).pdf   IVS-BH 2012 oficial
│   ├── Estudo Longitudinal da Saúde dos Idosos Brasileiros.docx
│   ├── Plano de trabalho.pdf  ·  Plano_Artigo_Cientifico_IC_Preenchido.docx
│   ├── Relatorio_EDA_Fase3_IVS_ELSI.{md,docx}     Relatório técnico-interpretativo da EDA
│   ├── Relatorio_Integridade_Projeto.md           Diagnóstico técnico
│   └── 📂 Apresentacoes_IVS/          Apresentações (PPTX) + Dicionário de Variáveis (XLSX)
│
├── 📂 Backup/                         LEGADOS — Fases 1 e 2, scripts antigos
│   ├── Fase1_IVS_Basico/              5 notebooks (sem filtro ELSI)
│   ├── Fase2_IVS_Multidimensional/    4 notebooks (sem filtro ELSI, com V01042)
│   ├── ETL/  ·  formatar/  ·  banco_de_dados/
│   └── DIAGNOSTICO_COMPLETO_PROJETO.md
│
└── 📂 tests/                          Testes sanity-check da pipeline
    └── test_pipeline_fase3.py
```

---

## Fontes de Dados

Os 8 arquivos CSV brutos do IBGE em `dados/` são os dados-fonte imutáveis (não versionados — baixar do IBGE):

| # | Arquivo | Dimensão do IVS | Variáveis-chave | Tamanho |
|---|---|---|---|---|
| 1 | `Agregados_por_setores_basico_BR_20250417.csv` | Identificação + população | `CD_SETOR`, `NM_MUN`, `v0001` | 130 MB |
| 2 | `Agregados_por_setores_caracteristicas_domicilio1_BR.csv` | Denominador habitacional | `V00001`, `V00002`, `V00005`, `V00006` | 177 MB |
| 3 | `Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv` | Saneamento | Água (V00112–V00118), Esgoto (V00312–V00316), Lixo (V00398–V00402) | 747 MB |
| 4 | `Agregados_por_setores_alfabetizacao_BR.csv` | Educação | `V00900` (15+ alfabetizados), `V00901` (15+ analfabetos) | 701 MB |
| 5 | `Agregados_por_setores_cor_ou_raca_BR.csv` | Vulnerabilidade social | `V01318` (preta), `V01320` (parda), `V01321` (indígena) | 192 MB |
| 6 | `Agregados_por_setores_renda_responsavel_BR.csv` | Renda | `V06004` (rendimento médio mensal) | 26 MB |
| 7 | `Agregados_por_setores_demografia_BR.csv` | Sobrecarga infantil (uso futuro) | `V01031`–`V01033` | 85 MB |
| 8 | `Agregados_por_setores_parentesco_BR.csv` | Auditoria de coletivos | `V01042` (pessoas responsáveis — **não** é denominador) | 346 MB |

---

## Pipeline de Análise — Fase 3 (ativa)

A pipeline ativa aplica o recorte dos **70 municípios ELSI** e produz a EDA. As Fases 1 e 2 (Brasil inteiro) estão arquivadas em `Backup/` como histórico.

```
dados/*.csv (8 arquivos) + dados/municipios_elsi_brasil.csv
  │
  ▼  01_Extracao_Filtragem_ELSI.ipynb
  │   Cruza por (UF + nome normalizado) → filtra 70 municípios
  │   Merge unificado + classificador de Morfologia Urbana
  │   Auditoria automática de integridade (sigilo 'X' preservado)
  │   Saída → banco_de_dados/Base_ELSI_Bruta_Censo2022.csv (109.032 setores)
  │
  ▼  02_Analises_Descritivas.ipynb
  │   Sigilo 'X' → NaN  →  Elegibilidade (Dados_sig)  →  7 proporções brutas
  │   Descritivas (global / município / região), histogramas, boxplots,
  │   outliers (IQR + P95), missing, correlações (Pearson + Spearman)
  │   Saída → banco_de_dados/eda/*.csv + figuras/*.png (106.281 setores OK)
  │
  ▼  (a criar) Notebook 03+ → normalização por município, análise fatorial,
                              IVS final, categorização em 4 faixas, mapas (QGIS)
```

---

## As 7 Variáveis-Componente do IVS

**Revisão de 22/05/2026** — denominador domiciliar **V00001** (Domicílios Particulares Permanentes Ocupados), padrão do IVS-BH 2012. O `V01042` foi **descartado** como denominador (é contagem de pessoas, não de domicílios).

| Dimensão | Indicador | Fórmula (Censo 2022) |
|---|---|---|
| **Saneamento** | Água inadequada | (V00112 + … + V00118) / **V00001** |
| | Esgoto inadequado | (V00312 + … + V00316) / **V00001** *(faixa em validação)* |
| | Lixo inadequado | (V00398 + … + V00402) / **V00001** |
| **Socioeconômica** | Razão de moradores | (V00005 + V00006) / **(V00001 + V00002)** *(reproduz o V0005 do IBGE)* |
| | Analfabetismo (15+) | V00901 / **(V00900 + V00901)** |
| | Renda média (invertida no índice) | V06004 (uso direto) |
| | Raça/cor (pretos + pardos + indígenas) | (V01318 + V01320 + V01321) / v0001 |

### Classificação de elegibilidade (`Dados_sig`)

| Classe | Critério |
|---|---|
| **OK** | participa das análises |
| **SIGILOSO** | `v0001` ou `V00001` sigilosos (NaN) |
| **COLETIVO** | `V00001 = 0` com `v0001 > 0` (população 100% em domicílios coletivos) |
| **ZERADO** | `v0001 = 0` (setor sem população) |

### Limitações Documentadas

| O que o IVS 2012 pedia | Limitação no Censo 2022 | Solução adotada |
|---|---|---|
| % chefes com <4 anos de estudo | Anos de instrução não disponíveis nos agregados | Taxa de analfabetismo `V00901 / (V00900 + V00901)` |
| % famílias ≤2 salários mínimos | Faixas salariais não disponíveis | Rendimento médio (V06004) com normalização invertida |
| Coef. óbitos cardiovasculares | IBGE registrou só se houve óbito, sem causa | Buscar DATASUS (Sistema SIM) futuramente |

---

## Convenções de Engenharia

- **Detecção da raiz do projeto** (`_find_project_root`) — torna os notebooks portáveis (executáveis a partir de qualquer cwd).
- **Fallback de encoding** (`utf-8 → latin1 → cp1252`) — robusto contra a inconsistência dos CSVs do IBGE.
- **Leitura em chunks** dos 2 CSVs maiores (701 MB e 747 MB) — protege a RAM.
- **Chave composta (UF + nome normalizado)** no filtro ELSI — necessária por causa de municípios homônimos em UFs diferentes.
- **Sigilo preservado** na base bruta (`X` mantido); o tratamento é feito a jusante no Notebook 02.

---

## Problemas Conhecidos e Pendências

Detalhamento em [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md).

| # | Problema | Status |
|---|---|---|
| 1 | Variáveis de esgoto — V00312–V00316 vs V00249–V00253 (diagnóstico empírico no Notebook 02) | 🟡 Decisão final pendente |
| 2 | Normalização de renda por município (no Notebook 03 a criar) | 🟡 Próxima fase |
| 3 | Relatórios em `docs/` (EDA e Integridade) com números da era V01042 — regerar a partir dos CSVs atuais | 🟡 Documentação |
| 4 | ~8 GB de dados duplicados/obsoletos em `Backup/` | 🟢 Limpeza opcional |
| 5 | Análise fatorial + cálculo do IVS final + categorização | 🔴 Pendente |

---

> Para contribuições ou dúvidas, consulte o [`GUIA_DO_PROJETO.md`](GUIA_DO_PROJETO.md) ou entre em contato com o pesquisador responsável.
