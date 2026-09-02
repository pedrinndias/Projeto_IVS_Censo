# Projeto IVS — Índice de Vulnerabilidade à Saúde (Censo 2022)

## Objetivo

Construir um **Índice de Vulnerabilidade à Saúde (IVS)** intraurbano a partir dos dados agregados por setor censitário do **Censo Demográfico 2022 (IBGE)**, para os **70 municípios da amostra do ELSI-Brasil** (Estudo Longitudinal da Saúde dos Idosos Brasileiros).

O projeto faz parte de uma **Iniciação Científica** vinculada à **Fiocruz Minas — IRR**, na área de Saúde Coletiva, Saúde Urbana e Epidemiologia Espacial.

> **Documento mestre:** [`GUIA_DO_PROJETO.md`](GUIA_DO_PROJETO.md) — versão atualizada e canônica de objetivos, metodologia, estado e plano.
> **Manual de uso:** [`docs/MANUAL_DO_PROJETO.md`](docs/MANUAL_DO_PROJETO.md) — onde achar cada arquivo, de onde vem cada número e como apresentar o projeto.
> **Diagnóstico técnico mais recente:** [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md).

## Status Atual

A pipeline ativa é a **Fase 3 (`notebooks/Fase3_EDA_ELSI/`)**, que aplica o filtro pelos 70 municípios do ELSI-Brasil e produz a EDA (análise exploratória). O recorte de análise são os **104.108 setores urbanos elegíveis** (de 109.032 na base). As Fases 1 e 2 estão arquivadas em [`Backup/`](Backup/) como histórico.

| Etapa | Status |
|---|---|
| Obtenção dos dados brutos do Censo 2022 | ✅ Concluída |
| Mapeamento e dicionários de variáveis | ✅ Concluída |
| Lista oficial dos 70 municípios ELSI-Brasil ([`dados/municipios_elsi_brasil.csv`](dados/municipios_elsi_brasil.csv)) | ✅ Concluída |
| Fase 3 — Notebook 01 (extração + filtro ELSI) | ✅ Concluída |
| Fase 3 — Notebook 02 (análises descritivas / EDA) | ✅ Concluída |
| Validação das variáveis de esgoto | ✅ Concluída — **V00312–V00316** confirmado no dicionário oficial do IBGE (V00249–V00253 é tipologia de habitação) |
| Demandas da orientadora (jul/2026) — 7 itens | ✅ Concluídas (ver abaixo) |
| Linha de base nacional (~468 mil setores) | ✅ [`scripts/proporcoes_brasil.py`](scripts/proporcoes_brasil.py) |
| Normalização de renda por município | 🔴 Pendente (a fazer no Notebook 03) |
| Análise fatorial / ACP — definição dos pesos | 🔴 Pendente (Notebook 04) |
| Cálculo do IVS final + categorização em 4 faixas | 🔴 Pendente (Notebook 05) |
| Mapas temáticos (QGIS 3.x) | 🔴 Pendente |
| Redação do artigo científico | 🟡 Plano preenchido em `docs/Plano_Artigo_Cientifico_IC_Preenchido.docx` |

### Demandas da orientadora — revisão de 09/08/2026

| # | Demanda | Onde foi atendida |
|---|---|---|
| 1 | Ajustar o índice de envelhecimento | NB02 §7e — **IEP = 60+ / menores de 15** (era 0–4), mais RDI e % 60+, conforme Galvão et al. (*Hygeia*, 2025) |
| 2 | Tabela com o significado de cada variável e a fonte da planilha | [`scripts/gerar_tabela_variaveis.py`](scripts/gerar_tabela_variaveis.py) → `Dicionario_Variaveis_Projeto.{csv,xlsx}` e a tabela `dicionario_variaveis` dos `.db` |
| 3 | Excluir setores rurais, conferindo a porcentagem | NB02 §3b — filtro urbano + `exclusao_rural_conferencia.csv` |
| 4 | Agrupar as moradias "normais" no tipo de domicílio | NB02 §7f — `pct_moradia_convencional` (casa + vila/condomínio + apartamento) |
| 5 | Criar um indicador de apartamento | NB02 §7f — `pct_apartamento` = V00049 / V00001 |
| 6 | Quantos setores do ELSI são de vilas e favelas | NB02 §7g — **19.452 no recorte de análise (18,7%)**, 19.507 na base completa (17,9%), via `CD_TIPO = 1` |
| 7 | Proporções para o Brasil todo e depois para os 70 municípios | [`scripts/proporcoes_brasil.py`](scripts/proporcoes_brasil.py) → `banco_de_dados/nacional/` |

## Metodologia

O IVS é um indicador composto que sintetiza **7 variáveis** em **2 dimensões**, calculado ao nível do setor censitário.

A operacionalização adotada na pipeline ativa (Fase 3) segue o padrão do **IVS-BH 2012**, ancorada no denominador domiciliar **V00001 (Domicílios Particulares Permanentes Ocupados)** — o equivalente no Censo 2022 do `V002` (Dom_part_p) do Censo 2010 usado pelo IVS-BH. Decisão consolidada na revisão metodológica de **22/05/2026** (orientadora): o `V01042` do arquivo de parentesco é uma **contagem de pessoas responsáveis**, não de domicílios, e por isso foi descartado como denominador. O `V01042` segue sendo extraído apenas para auditoria de setores 100% coletivos.

| Dimensão | Indicador | Censo 2022 (numerador) | Denominador |
|---|---|---|---|
| **Saneamento** | Água inadequada | V00112 a V00118 (7 vars.) | **V00001** |
| | Esgoto inadequado | V00312 a V00316 (5 vars.) *(confirmado no dicionário oficial)* | **V00001** |
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

## Decisões Metodológicas

Toda escolha que muda um número está registrada com justificativa, verificação empírica e
status. A tabela abaixo é o resumo; o detalhamento está nos documentos indicados ao final.

**Os três princípios que orientam as decisões:** (1) onde o `Cálculo IVS2012.docx` define,
o projeto reproduz — o objetivo é *replicar* o IVS-BH no Censo 2022, não redesenhá-lo;
(2) quando o Censo 2022 não permite reproduzir, a substituição é **declarada** em vez de
improvisada; (3) nenhuma decisão entra sem uma verificação que a sustente.

### Consolidadas

| Decisão | Justificativa | Verificação | Status |
|---|---|---|---|
| **Denominador `V00001`** (Dom. Particulares Permanentes Ocupados) | Equivalente exato do `V002` do Censo 2010 usado pelo IVS-BH. O `V01042` foi descartado: conta *pessoas* responsáveis, não domicílios | Nenhuma proporção ultrapassa 1,0 em 104.108 setores; com o denominador anterior, várias estouravam | ✅ |
| **Analfabetismo = `V00901 / (V00900+V00901)`** | O denominador de uma taxa é a população de referência inteira — quem sabe **mais** quem não sabe ler | A fórmula anterior (`/V00900`) gerava setores com valor acima de 1 | ✅ |
| **Razão de moradores com DPPO + DPIO** nos dois lados | Reproduz a definição oficial do `V0005` do IBGE | Confere com o valor publicado | ✅ |
| **Ordem da regra `Dados_sig`**: população zero antes de sigilo | Setores vazios (massas d'água) eram contados como "dado suprimido pelo IBGE" | Sigilo real caiu de 2.751 para 1.015; **nenhum setor `OK` mudou de classe** | ✅ |
| **Recorte urbano aplicado na análise, não na extração** | Auditabilidade, reversibilidade e fidelidade do dado bruto. A base preserva os 109.032 setores | `CD_SIT` 1–3 = Urbana e 5–8 = Rural nos 468.099 setores do país, sem exceção | ✅ |
| **Sigilo vira ausente, nunca zero** | O sigilo do analfabetismo **não é aleatório**: incide onde há poucos analfabetos. Imputar zero subestimaria as áreas menos vulneráveis | Afeta 15,9% dos setores, concentrados nas capitais | ✅ na EDA; ⚠️ política do cálculo final a definir |
| **IEP = 60+ / menores de 15** (Galvão et al., 2025) | A versão anterior usava 0–4, o que inflava o índice ~3× e o tornava incomparável. O corte de 65 é impossível: o IBGE agrega "60 a 69" | Soma das 11 faixas reproduz `v0001` em 99.957 setores; IEP nacional deu **79,99** contra 80,0 do IBGE | ✅ |
| **Favela identificada por `CD_TIPO = 1`** | É o campo oficial de classificação do setor; `NM_FCU` é atributo descritivo | Os dois critérios coincidem nos 468.099 setores do país: 33.272 setores | ✅ |
| **Caçamba (`V00398`) conta como lixo inadequado** | Fidelidade à metodologia-fonte: só a coleta porta a porta (`V00397`) é adequada | — | ⚠️ **em revisão** (ver abaixo) |
| **Indicadores descritivos ficam fora do índice** | Um componente precisa de direção inequívoca. `pct_apartamento` não tem: verticalização aparece em área rica e em conjunto popular | Separação estrutural no código: `INDICADORES_IVS` (7) × `INDICADORES_COMPLEMENTARES` (16) | ✅ |
| **Fórmulas em módulo compartilhado** | Copiar o código para rodar o Brasil criaria duas versões que divergem na primeira correção — e aí a comparação Brasil × ELSI deixa de ser legítima | População nacional confere: **203.080.756**, o número oficial do Censo. O NB02 passou a importar o módulo em 20/08/2026 e reproduz as 38 tabelas | ✅ no NB02 — pendente no NB01, que ainda tem lista de variáveis própria |

### Em aberto — dependem de definição com a orientação

| # | Decisão | O que trava |
|---|---|---|
| 1 | **Critério dos pesos**: empíricos (análise fatorial) ou guiados pela literatura (60% socioeconômica / 40% saneamento)? Renda, cor/raça e analfabetismo se correlacionam a −0,81 e −0,76 — pesos iguais dariam três votos à posição social sem que fosse escolha deliberada | Notebooks 04 e 05 |
| 2 | **Indicador de lixo**: entra como está, ou a caçamba é separada? É a variável menos correlacionada com todas as demais e a única em que o recorte ELSI está pior que o Brasil urbano — pode estar medindo porte urbano | Composição do índice |
| 3 | **Política de sigilo no analfabetismo** para o cálculo final | Notebook 03 |
| 4 | **Piso mínimo de setores** por município: 14 dos 70 perdem mais da metade dos setores no recorte urbano | Tabelas municipais e mapas |

### Onde está cada nível de detalhe

| Documento | O que traz |
|---|---|
| [`GUIA_DO_PROJETO.md`](GUIA_DO_PROJETO.md) §6 | **A versão canônica**: decisão, justificativa, alternativa descartada, verificação e status |
| [`docs/Relatorio_EDA_Fase3_IVS_ELSI.md`](docs/Relatorio_EDA_Fase3_IVS_ELSI.md) §12 | A argumentação estendida e o passo a passo de execução de cada demanda |
| [`docs/MANUAL_DO_PROJETO.md`](docs/MANUAL_DO_PROJETO.md) Parte C | Arquivos e células tocados, comandos, como conferir e como desfazer |

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
├── src/ivs_censo/                     Código compartilhado (procedência das variáveis,
│   │                                  fórmulas dos indicadores, regra de elegibilidade)
│   ├── fontes.py                      Os 8 arquivos do Censo e o que se lê de cada um
│   ├── indicadores.py                 Definição e cálculo dos 26 indicadores
│   └── dicionario.py                  Tabela de variáveis (descrição IBGE + arquivo-fonte)
│
├── scripts/                           Executáveis versionados
│   ├── gerar_tabela_variaveis.py      Dicionário de variáveis (CSV + XLSX)
│   ├── gerar_entrega_orientadora.py   Pacote de entrega (CSV + SQLite)
│   ├── gerar_tabelas_auditoria.py     Tabelas de auditoria/apresentação de banco_de_dados/eda/
│   └── proporcoes_brasil.py           Indicadores para o Brasil inteiro + comparativo
│
├── banco_de_dados/                    Outputs da pipeline ativa (Fase 3)
│   ├── Base_ELSI_Bruta_Censo2022.csv  Saída do Notebook 01 (filtrada por ELSI)
│   ├── nacional/                      Saídas do cálculo Brasil inteiro
│   ├── entrega_orientadora/           Pacote de entrega + dicionário de variáveis
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
│   ├── MANUAL_DO_PROJETO.md                Manual: onde achar tudo e como apresentar
│   ├── Relatorio_EDA_Fase3_IVS_ELSI.{md,docx}
│   ├── Apresentacoes_IVS/                  Apresentação atual + roteiro; historico/ e dicionarios/ (ver README.md da pasta)
│   └── Relatorio_Integridade_Projeto.md    Diagnóstico técnico mais recente
│
├── Backup/                            Legados — Fases 1 e 2, scripts antigos
│   ├── Fase1_IVS_Basico/              5 notebooks (sem filtro ELSI)
│   ├── Fase2_IVS_Multidimensional/    4 notebooks (sem filtro ELSI, com V01042)
│   ├── ETL/, formatar/, banco_de_dados/
│   └── DIAGNOSTICO_COMPLETO_PROJETO.md
│
└── tests/                             65 testes (artefatos da pipeline + fórmulas dos indicadores)
```

## Problemas Conhecidos

Lista resumida — detalhamento técnico em [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md).

| # | Problema | Gravidade |
|---|---|---|
| 1 | ~~**Variáveis de esgoto**~~ — o dicionário oficial do IBGE (versionado em `dados/`) confirma **V00312–V00316** como esgoto inadequado; V00249–V00253 é tipologia de habitação. O diagnóstico empírico (célula `step4b` do Notebook 02, `diagnostico_esgoto_312_vs_249.csv`) corrobora. | ✅ Resolvido |
| 2 | **Normalização de renda global** — usa min/max global; será trocada para por município no Notebook 03 (a criar). | 🟡 Pendente (próxima fase) |
| 3 | ~~**Ausência do filtro ELSI**~~ | ✅ Resolvido (Fase 3) |
| 4 | ~~**Denominadores divergentes**~~ — consolidado **V00001** (Dom. Particulares Permanentes Ocupados) na revisão de 22/05/2026; `V01042` descartado (é contagem de pessoas, não de domicílios). | ✅ Resolvido |
| 5 | **Dados duplicados em `Backup/`** — ~8 GB de arquivos obsoletos. Limpeza opcional. | 🟢 Organizacional |
| 6 | ~~**Massas d'água contadas como sigilo**~~ — 1.736 setores sem população apareciam como `SIGILOSO`; a ordem das condições foi invertida. Nenhum setor `OK` mudou. | ✅ Resolvido |
| 7 | **Municípios pequenos após o filtro urbano** — 29 dos 70 perdem mais de 10% dos setores e 14 perdem mais da metade. Afeta a estabilidade das descritivas municipais. | 🟡 Metodológico |
| 8 | ~~**Fórmulas duplicadas no Notebook 02**~~ — **resolvido em 20/08/2026**: o NB02 importa `src/ivs_censo`. Resta o **Notebook 01**, que mantém um dicionário `ARQUIVOS` próprio: acrescentar variável exige mexer nele e em `fontes.py`. | 🟡 Manutenção (só no NB01) |

## Dados Utilizados

| Arquivo do Censo 2022 | Dimensão do IVS | Tamanho |
|---|---|---|
| `Agregados_por_setores_basico_BR_20250417.csv` | Identificação, situação, tipo de setor (favela) e população | 137 MB |
| `Agregados_por_setores_caracteristicas_domicilio1_BR.csv` | Denominadores e tipos de domicílio (V00001–V00006, V00047–V00058) | 186 MB |
| `Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv` | Saneamento (água, esgoto, lixo, banheiro) | 784 MB |
| `Agregados_por_setores_alfabetizacao_BR.csv` | Educação (V00900, V00901) | 735 MB |
| `Agregados_por_setores_cor_ou_raca_BR.csv` | Raça/cor (V01318, V01320, V01321) | 201 MB |
| `Agregados_por_setores_renda_responsavel_BR.csv` | Renda (V06004) | 27 MB |
| `Agregados_por_setores_demografia_BR.csv` | Pirâmide etária completa (V01031–V01041) — indicadores de envelhecimento | 89 MB |
| `Agregados_por_setores_parentesco_BR.csv` | Responsáveis por sexo (V01042, V01062, V01063) | 362 MB |

Fonte: [IBGE — Censo Demográfico 2022 — Agregados por Setores Censitários](https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html).

## Como Executar

### Pré-requisitos
- Python 3.10+
- Os 8 CSVs do Censo 2022 em `dados/` (não versionados — baixar do IBGE)

### Instalação
Ambiente virtual dedicado, na raiz do projeto (o `.venv/` fica fora do git):

```bash
python3 -m venv .venv && ./.venv/bin/python -m pip install -r requirements.txt
```

Tudo abaixo — testes, notebooks, scripts — roda com o Python desse ambiente
(`./.venv/bin/python`), sem precisar de `activate`. Confira que ficou de pé com:

```bash
./.venv/bin/python -m pytest tests/ -q
```

### Execução da Pipeline Ativa
Os notebooks da Fase 3 devem ser executados na ordem numérica:

```
notebooks/Fase3_EDA_ELSI/  →  01 → 02
```

Pelo Jupyter, ou sem abrir interface (mesmo resultado, útil para conferir que a
pipeline ainda roda de ponta a ponta):

```bash
./.venv/bin/jupyter execute notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb
```

- **Notebook 01:** extrai e filtra → produz `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` (109.032 setores × 68 colunas, ~24 MB).
- **Notebook 02:** EDA completa → produz as tabelas-resumo (CSVs) e 4 figuras em `banco_de_dados/eda/` — a procedência arquivo a arquivo está em [`banco_de_dados/eda/README.md`](banco_de_dados/eda/README.md).

> A execução completa consome bastante RAM e tempo (~2.4 GB de CSVs brutos). Os notebooks leem apenas as colunas necessárias e processam os arquivos maiores em chunks.

### Testes Sanity
```bash
./.venv/bin/python -m pytest tests/ -v
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
