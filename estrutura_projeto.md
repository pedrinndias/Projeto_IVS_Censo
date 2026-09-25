# 🏗️ Arquitetura e Estrutura do Projeto IVS — Censo 2022

> Última atualização: 25/09/2026 (Fase 5, lote C, HIG-11: árvore regerada por script a partir de `git ls-files`, desatualizada desde antes da reorganização de `docs/` e da chegada do NB04)

---

## Visão Geral

Este projeto constrói um **Índice de Vulnerabilidade à Saúde (IVS)** intraurbano a partir dos dados agregados por setor censitário do **Censo Demográfico 2022** (IBGE), restrito aos **70 municípios da amostra do ELSI-Brasil**, como parte de uma **Iniciação Científica** na **Fiocruz Minas — IRR**.

**Tecnologias:** Python 3.10+ · Pandas · NumPy · Matplotlib · Jupyter Notebooks · QGIS (futuro)
**Dependências:** ver [`requirements.txt`](requirements.txt) (`pandas`, `numpy`, `matplotlib`, `openpyxl`, `xlsxwriter`)

> **Documento mestre:** [`GUIA_DO_PROJETO.md`](GUIA_DO_PROJETO.md) — objetivos, metodologia, estado e plano (canônico).
> **Diagnóstico técnico:** [`docs/relatorios/Relatorio_Integridade_Projeto.md`](docs/relatorios/Relatorio_Integridade_Projeto.md).

---

## Árvore de Diretórios (estado atual)

> Gerada por script a partir de `git ls-files` (só o que está versionado; `dados/` bruto do
> IBGE, `.venv/`, `.claude/` e `node_modules/` ficam de fora por não serem versionados ou por
> serem internos de ferramenta). Profundidade limitada a 3 níveis, com contagem de arquivos
> por pasta em vez de listar cada um — para o conteúdo linha a linha de uma pasta, `git
> ls-files <pasta>`. Total: 410 arquivos versionados em 25/09/2026.

```
Projeto_IVS_Censo22/
├── .gitignore · GUIA_DO_PROJETO.md · LICENSE · README.md · estrutura_projeto.md ·
│   graphify.md · package.json · package-lock.json · requirements.txt
├── .vscode/  (1 arquivo)
├── Backup/  (17 arquivos)                    LEGADO — Fases 1 e 2, pré-filtro ELSI
│   ├── ETL/  (1 arquivo)
│   ├── Fase1_IVS_Basico/  (5 arquivos)
│   ├── Fase2_IVS_Multidimensional/  (4 arquivos)
│   ├── banco_de_dados/  (1 arquivo)
│   │   └── fase2_bases/  (1 arquivo)
│   └── formatar/  (3 arquivos)
├── banco_de_dados/  (170 arquivos)           OUTPUTS DA PIPELINE
│   ├── eda/  (153 arquivos)
│   │   ├── atualizada/  (27 arquivos)
│   │   ├── fatorial/  (43 arquivos)
│   │   ├── fatorial_ampliada/  (14 arquivos)
│   │   └── figuras/  (7 arquivos)
│   ├── entrega_orientadora/  (10 arquivos)
│   └── nacional/  (7 arquivos)
├── dados/  (4 arquivos)                      só `municipios_elsi_brasil.csv` e afins; os
│                                              8 CSVs brutos do IBGE não são versionados
├── docs/  (61 arquivos)                      DOCUMENTAÇÃO
│   ├── Apresentacoes_IVS/  (26 arquivos)
│   │   ├── complementos/  (10 arquivos)
│   │   ├── dicionarios/  (2 arquivos)
│   │   └── historico/  (11 arquivos)
│   ├── metodologia/  (13 arquivos)
│   │   └── fontes_pdf/  (4 arquivos)
│   ├── prompts/  (6 arquivos)
│   ├── referencias/  (8 arquivos)
│   └── relatorios/  (7 arquivos)
├── graphify-out/  (108 arquivos)             grafo de conhecimento — gerado por skill, não
│   ├── cache/  (86 arquivos)                 mantido à mão (HIG-13)
│   │   ├── ast/  (58 arquivos)
│   │   └── semantic/  (27 arquivos)
│   └── converted/  (12 arquivos)
├── notebooks/  (5 arquivos)
│   └── Fase3_EDA_ELSI/  (5 arquivos)         01, 02, 04, 04b + README — PIPELINE ATIVA
├── scripts/  (26 arquivos)                   EXECUTÁVEIS VERSIONADOS
├── src/  (6 arquivos)
│   └── ivs_censo/  (6 arquivos)              CÓDIGO COMPARTILHADO (importável por scripts)
└── tests/  (3 arquivos)                      testes sanity-check e de fórmulas
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
  │   Sigilo 'X' → NaN  →  Elegibilidade (Dados_sig)  →  RECORTE URBANO
  │   7 proporções brutas + blocos complementares (habitação, banheiro, chefia
  │   feminina, envelhecimento, tipo de domicílio, favelas)
  │   Descritivas (global / município / região), histogramas, boxplots,
  │   outliers (IQR + P95), missing, correlações (Pearson + Spearman)
  │   Saída → banco_de_dados/eda/*.csv + figuras/*.png (104.108 setores urbanos OK)
  │
  ▼  04_Analise_Fatorial.ipynb / 04b_Analise_Fatorial_Ampliada.ipynb → análise fatorial
     (concluída — ver GUIA_DO_PROJETO.md); IVS final, categorização e mapas (QGIS) seguem
     como próxima etapa
```

### Linha lateral — cálculo nacional (não é recorte de análise)

```
dados/*.csv (8 arquivos, sem filtro de município)
  │
  ▼  scripts/proporcoes_brasil.py   (usa src/ivs_censo — mesmas fórmulas do NB02)
  │   468.099 setores → elegibilidade → recorte urbano → 26 indicadores
  │   Agrega por Brasil / região / UF / município e compara com os 70 ELSI
  │   Saída → banco_de_dados/nacional/*.csv        (~10 min de execução)
```

Serve de **linha de base de representatividade**: mostra o quanto a amostra ELSI difere
do país (é mais urbana, mais rica e concentra 58,6% dos setores de favela do Brasil).

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
| **ZERADO** | `v0001 = 0` (setor sem população) — avaliado **primeiro** |
| **SIGILOSO** | `v0001` ou `V00001` sigilosos (NaN) |
| **COLETIVO** | `V00001 = 0` com `v0001 > 0` (população 100% em domicílios coletivos) |
| **OK** | participa das análises |

> A ordem importa e foi corrigida em 09/08/2026: `ZERADO` passou a ser testado antes de
> `SIGILOSO`. Sem isso, 1.736 setores sem população (entre eles as 78 massas d'água,
> `CD_SIT = 9`) apareciam como dado suprimido pelo IBGE. Nenhum setor `OK` mudou.

**Recorte de análise:** além de `Dados_sig = OK`, exige-se `SITUACAO = Urbana`.
109.032 setores na base → 106.281 elegíveis → **104.108 urbanos elegíveis**.

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

Detalhamento em [`docs/relatorios/Relatorio_Integridade_Projeto.md`](docs/relatorios/Relatorio_Integridade_Projeto.md).

| # | Problema | Status |
|---|---|---|
| 1 | ~~Variáveis de esgoto~~ — **V00312–V00316** confirmado no dicionário oficial do IBGE (versionado em `dados/`); V00249–V00253 é tipologia de habitação | ✅ Resolvido |
| 2 | Normalização de renda por município (no Notebook 03 a criar) | 🟡 Próxima fase |
| 3 | ~~Relatórios em `docs/` com números da era V01042~~ — regerados em 12/06/2026 sobre a metodologia V00001 | ✅ Resolvido |
| 4 | ~8 GB de dados duplicados/obsoletos em `Backup/` | 🟢 Limpeza opcional |
| 5 | Análise fatorial — **concluída** (NB04/04b); cálculo do IVS final + categorização | 🔴 Pendente |

---

> Para contribuições ou dúvidas, consulte o [`GUIA_DO_PROJETO.md`](GUIA_DO_PROJETO.md) ou entre em contato com o pesquisador responsável.
