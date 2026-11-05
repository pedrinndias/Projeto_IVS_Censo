# Projeto IVS — Índice de Vulnerabilidade à Saúde (Censo 2022)

## Objetivo

Construir um **Índice de Vulnerabilidade à Saúde (IVS)** intraurbano a partir dos dados agregados por setor censitário do **Censo Demográfico 2022 (IBGE)**, para os **70 municípios da amostra do ELSI-Brasil** (Estudo Longitudinal da Saúde dos Idosos Brasileiros).

O projeto faz parte de uma **Iniciação Científica** vinculada à **Fiocruz Minas — IRR**, na área de Saúde Coletiva, Saúde Urbana e Epidemiologia Espacial.

> **Documento mestre:** [`GUIA_DO_PROJETO.md`](GUIA_DO_PROJETO.md) — canônico para objetivos, metodologia e decisões consolidadas. Foi revisado até set/2026 (NB05); o que veio depois está neste README e nos arquivos de estado.
> **Manual de uso:** [`docs/MANUAL_DO_PROJETO.md`](docs/MANUAL_DO_PROJETO.md) — onde achar cada arquivo, de onde vem cada número e como apresentar o projeto (revisado até set/2026).
> **Revisão técnica mais recente:** [`docs/relatorios/Simplificacao_e_Correcoes_2026-10.md`](docs/relatorios/Simplificacao_e_Correcoes_2026-10.md) — os 8 erros corrigidos em 22/10/2026 e o que ficou por regerar.
> **Decisão em curso:** [`apresentacoes_multiversao/Corte_Carga_04_Duas_Propostas_2026-11_v2.pptx`](apresentacoes_multiversao/Corte_Carga_04_Duas_Propostas_2026-11_v2.pptx) — as duas propostas de IVS para a orientadora escolher (decisão resumida no slide 5, perguntas no 81).
> **Análise fatorial (Notebook 04):** [`docs/metodologia/Analise_Fatorial_LEIAME.md`](docs/metodologia/Analise_Fatorial_LEIAME.md) — índice do estudo do livro da Enap, do plano de implementação e do prompt de execução.

## Status Atual

*Atualizado em 05/11/2026.*

A pipeline ativa é a **Fase 3 (`notebooks/Fase3_EDA_ELSI/`)**: aplica o filtro pelos 70 municípios do ELSI-Brasil e produz a EDA (análise exploratória), a análise fatorial e os testes de especificação do IVS. O recorte de análise são os **104.108 setores urbanos elegíveis** (de 109.032 na base). As Fases 1 e 2 estão arquivadas em [`Backup/`](Backup/) como histórico.

**O IVS final ainda não está escolhido.** Há índices calculados, mas todos são propostas: a composição, a rotação e os pesos dependem da orientadora. As mais recentes são as propostas A e B do corte de carga < 0,4 — ver [Propostas de IVS](#propostas-de-ivs).

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
| Normalização de renda por município | ✅ Feita no cálculo do índice (`ie.indice`, em [`scripts/ivs_especificacoes.py`](scripts/ivs_especificacoes.py), usada no NB05); não há Notebook 03 |
| Fase 3 — Notebook 04 (análise fatorial) | ✅ Concluída em 17/09/2026 — [`04_Analise_Fatorial.ipynb`](notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb), [relatório](docs/relatorios/Relatorio_Analise_Fatorial_NB04.md) |
| Fase 3 — Notebook 04b (fatorial ampliada) | ✅ Concluída em 25/09/2026 — [`04b_Analise_Fatorial_Ampliada.ipynb`](notebooks/Fase3_EDA_ELSI/04b_Analise_Fatorial_Ampliada.ipynb): cenários com novas variáveis, sem lixo e sensibilidade por município |
| Fase 3 — Notebook 05 (testes de especificação do IVS) | ✅ Concluída em 27/09/2026 — [`05_Calculo_IVS_Final.ipynb`](notebooks/Fase3_EDA_ELSI/05_Calculo_IVS_Final.ipynb), [relatório](docs/relatorios/Relatorio_IVS_Final_NB05.md): 324 especificações, 192 elegíveis, referência proposta e 4 faixas |
| Análises exploratórias por versão | ✅ Concluídas em 06/10/2026 — 39 decks em [`analises_exploratorias/`](analises_exploratorias/README.md); o que vai para o artigo se escolhe no `Catalogo_Mestre.xlsx` |
| 108 versões da análise fatorial | ✅ Concluídas em 08/10/2026 — [`versoes_fatorial/`](versoes_fatorial/ESTADO.md); os decks têm números antigos (problema 9) |
| Relatório descritivo do andamento | ✅ Concluído em 09/10/2026 — [`relatorio_descritivo/`](relatorio_descritivo/ESTADO.md): v3 (140 slides) e apoio v4 (295 slides); números antigos em alguns slides (problema 9) |
| Fatorial multiversão | ✅ Concluída em 22/10/2026 — 8.034 fatoriais, 999 especificações e 13 decks em [`apresentacoes_multiversao/`](apresentacoes_multiversao/) ([estado](docs/prompts/estado_fatorial_multiversao_2026-10.md)) |
| Revisão, simplificação do código e correção de 8 erros | ✅ Concluída em 22/10/2026 — [relatório](docs/relatorios/Simplificacao_e_Correcoes_2026-10.md) |
| Corte de carga < 0,4 (demanda de nov/2026) | ✅ Rodado em 04/11/2026 — deck v2 com 88 slides e duas propostas lado a lado |
| Escolha do IVS final | 🟡 Aguarda a orientadora: proposta A ou B e as perguntas em [Em aberto](#em-aberto--dependem-de-definição-com-a-orientação) |
| RAIC 2026 (apresentação oral) | 🟡 Relatório parcial entregue; deck de 15 slides (`_ENVIO_v4`) e roteiro v4.1 em [`relatorio_parcial_raic/`](relatorio_parcial_raic/); evento de 09 a 13/11/2026 |
| Mapas temáticos (QGIS 3.x) | 🔴 Pendente |
| Redação do artigo científico | 🟡 Plano preenchido em `docs/referencias/Plano_Artigo_Cientifico_IC_Preenchido.docx` |

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

### Demanda da orientadora — nov/2026

> "Acionar todos os indicadores que já selecionamos na carga fatorial. Os indicadores com carga fatorial menor que 0,4, retirar."

Atendida em [`scripts/fatorial_corte_04.py`](scripts/fatorial_corte_04.py) (o corte) e [`scripts/fatorial_corte_04_sensibilidade.py`](scripts/fatorial_corte_04_sensibilidade.py) (o quanto ele depende do método). Saídas em `banco_de_dados/eda/fatorial_corte_04/`; resultado em [Propostas de IVS](#propostas-de-ivs).

## Metodologia

O desenho de partida do IVS (Quadro 1) é um indicador composto que sintetiza **7 variáveis** em **2 dimensões**, calculado ao nível do setor censitário. A composição final ainda está em decisão: a análise fatorial parte hoje de 12 indicadores (ver [Propostas de IVS](#propostas-de-ivs)).

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

### Propostas de IVS

Cada etapa da análise produziu uma proposta. Nenhuma é o IVS final. Todas usam régua min-max municipal.

| Proposta | Data | Indicadores | Rotação · pesos | Setores com IVS |
|---|---|---|---|---:|
| Referência do NB05 | 27/09/2026 | Quadro 1 sem lixo, com banheiro graduado | promax · 60/40 | 73.877 |
| IVS proposto da multiversão (E0009) | 22/10/2026 | Os 7 do Quadro 1 | promax · 60/40 | 87.544 |
| **Proposta A** do corte | 04/11/2026 | 8: água, esgoto, moradores, analfabetismo, renda, cor/raça, sem água canalizada, sem banheiro | promax · 60/40 | 75.926 (72,9% do recorte) |
| **Proposta B** do corte | 04/11/2026 | 7: os mesmos, sem o sem banheiro | Varimax · 60/40 | 87.511 (84,1% do recorte) |

Os 7 da proposta B não são os 7 do Quadro 1: sem água canalizada entra no lugar do lixo.

**O que o corte mostrou:**

- **Lixo e moradia não convencional** saem nas três rotações. **Sem banheiro** sai sem rotação e na Varimax, e fica na promax, por pouco: é o que separa A de B.
- **Idosos e crianças** passam no corte. Saem das duas propostas por decisão do projeto, não pela regra: são lidos como estrutura etária, não como vulnerabilidade.
- **A e B dão quase o mesmo índice:** Spearman de 0,996 dentro do município e 4,4% dos setores trocando de faixa, na amostra comum. A diferença prática é a cobertura: A perde 11.585 setores que não têm o dado do banheiro.
- **A permanência do sem banheiro é frágil:** ao reamostrar os municípios (1.000 réplicas), ele fica em 57,5% das vezes na promax e 31,0% na Varimax.
- **Nenhuma das duas passa em todos os critérios pré-registrados:** a comunalidade mínima é 0,18 em A e 0,24 em B, abaixo de 0,30. KMO, MSA e carga mínima passam.

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
| **Indicadores descritivos ficam fora do índice** | Um componente precisa de direção inequívoca. `pct_apartamento` não tem: verticalização aparece em área rica e em conjunto popular | Separação estrutural no código: `INDICADORES_IVS` (7) × `INDICADORES_COMPLEMENTARES` (21) | ✅ |
| **Fórmulas em módulo compartilhado** | Copiar o código para rodar o Brasil criaria duas versões que divergem na primeira correção — e aí a comparação Brasil × ELSI deixa de ser legítima | População nacional confere: **203.080.756**, o número oficial do Censo. O NB02 passou a importar o módulo em 20/08/2026 e reproduz as 38 tabelas | ✅ no NB02 e no NB01 (desde 21/08/2026, d71f55f) |

### Em aberto — dependem de definição com a orientação

A demanda de nov/2026 respondeu em parte quais indicadores entram (os 12, com o corte de 0,4). As demais respostas às perguntas P1 a P5 não estão registradas no repositório; até lá, vale o padrão da tabela. A "troca de faixa" é a maior encontrada na multiversão entre as alternativas de cada eixo.

| # | Decisão | Padrão enquanto não há resposta | O que se sabe |
|---|---|---|---|
| 1 | **Proposta A ou B**, ou seja, o sem banheiro entra? | — | Ver [Propostas de IVS](#propostas-de-ivs) |
| 2 | **Modelo do índice** (P1): reflexivo, formativo ou híbrido? | Híbrido | A fatorial define os pesos dentro de cada dimensão; a divisão entre elas é escolha do projeto |
| 3 | **Sigilo do analfabetismo** (P3) | Ausente; imputações como sensibilidade | Eixo equivalente: até 2,7% de troca de faixa |
| 4 | **Régua** (P4): min-max municipal, min-max global ou postos no município? | Min-max municipal | Exige decisão: até 31,8% de troca de faixa |
| 5 | **Rotação e pesos** (P5): empíricos ou guiados pela literatura (60% socioeconômica / 40% saneamento)? Renda, cor/raça e analfabetismo se correlacionam a −0,81 e −0,76 (par a par; na matriz *listwise* da fatorial cai a 0,784 — ver `docs/relatorios/Relatorio_Analise_Fatorial_NB04.md`): pesos iguais dariam três votos à posição social sem que fosse escolha deliberada | Promax com 60/40 | Exige decisão: até 18,5% de troca de faixa |
| 6 | **Indicador de lixo**: a caçamba é separada? É a variável menos correlacionada com as demais e a única em que o recorte ELSI está pior que o Brasil urbano — pode estar medindo porte urbano | Sai pelo corte de 0,4 | A pergunta só volta se o lixo voltar ao índice |
| 7 | **Piso mínimo de setores** por município: 14 dos 70 perdem mais da metade dos setores no recorte urbano | Sem piso | Afeta tabelas municipais e mapas |

Os parâmetros exploratórios que ninguém fixou (piso de população do setor, faixas de porte, número de grupos e outros) estão em [`analises_exploratorias/PERGUNTAS.md`](analises_exploratorias/PERGUNTAS.md).

### Onde está cada nível de detalhe

| Documento | O que traz |
|---|---|
| [`GUIA_DO_PROJETO.md`](GUIA_DO_PROJETO.md) §6 | **A versão canônica**: decisão, justificativa, alternativa descartada, verificação e status |
| [`docs/relatorios/Relatorio_EDA_Fase3_IVS_ELSI.md`](docs/relatorios/Relatorio_EDA_Fase3_IVS_ELSI.md) §12 | A argumentação estendida e o passo a passo de execução de cada demanda |
| [`docs/MANUAL_DO_PROJETO.md`](docs/MANUAL_DO_PROJETO.md) Parte C | Arquivos e células tocados, comandos, como conferir e como desfazer |
| [`docs/prompts/estado_fatorial_multiversao_2026-10.md`](docs/prompts/estado_fatorial_multiversao_2026-10.md) | O pré-registro, as perguntas P1 a P5 e os critérios de elegibilidade e equivalência |

## Estrutura de Pastas

```
Projeto_IVS_Censo22/
│
├── README.md                          Este arquivo (apresentação geral)
├── GUIA_DO_PROJETO.md                 Documento mestre de retomada (revisado até set/2026)
├── estrutura_projeto.md               Mapa detalhado das pastas (revisado até set/2026)
├── requirements.txt                   Dependências Python
├── package.json                       Dependência dos decks (pptxgenjs)
├── LICENSE                            Licença MIT
│
├── dados/                             Dados brutos do IBGE (imutáveis)
│   ├── Agregados_por_setores_*.csv    8 CSVs oficiais do Censo 2022 (~2,4 GB, fora do git)
│   ├── municipios_elsi_brasil.csv     Lista oficial dos 70 municípios ELSI
│   ├── FavelaseComunidadesUrbanas2022Setores_20250417.xlsx
│   ├── dicionario_de_dados_*.xlsx     Dicionários oficiais do IBGE
│   ├── banco_de_dados/                Bases legadas (~5,6 GB, fora do git)
│   ├── output/                        Outputs de scripts auxiliares
│   └── processed/                     Exports em Excel (legado)
│
├── src/ivs_censo/                     Código compartilhado
│   ├── fontes.py                      Os 8 arquivos do Censo, o que se lê de cada um e a leitura dos CSVs
│   ├── indicadores.py                 Definição e cálculo dos 28 indicadores
│   ├── dicionario.py                  Tabela de variáveis (descrição IBGE + arquivo-fonte)
│   ├── fatorial.py                    KMO, Bartlett, Horn, extração, rotações e cenários
│   └── renda.py                       Rastreamento e classificação dos extremos de renda
│
├── notebooks/Fase3_EDA_ELSI/          Pipeline ativa
│   ├── 01_Extracao_Filtragem_ELSI.ipynb
│   ├── 02_Analises_Descritivas.ipynb
│   ├── 04_Analise_Fatorial.ipynb
│   ├── 04b_Analise_Fatorial_Ampliada.ipynb
│   ├── 05_Calculo_IVS_Final.ipynb
│   └── README.md
│
├── scripts/                           Executáveis versionados (61 .py, 14 .js; ver scripts/README.md)
│   ├── proporcoes_brasil.py           Indicadores para o Brasil inteiro + comparativo
│   ├── gerar_entrega_orientadora.py   Pacote de entrega (CSV + SQLite)
│   ├── ivs_especificacoes.py          Motor do NB05: índice, faixas e as 324 especificações
│   ├── fatorial_ampliada.py           Motor do NB04b
│   ├── eda_versoes.py                 Motor das análises exploratórias por versão
│   ├── versoes_fatorial.py            Motor das 108 versões
│   ├── fatorial_multiversao.py        Motor da multiversão (camadas 1 a 3)
│   ├── fatorial_corte_04.py           Corte de carga < 0,4 e as propostas A e B
│   ├── gerar_decks_multiversao.js     Decks da multiversão e do corte
│   └── verificar_*.py                 Verificadores das entregas
│
├── banco_de_dados/                    Saídas da pipeline ativa
│   ├── Base_ELSI_Bruta_Censo2022.csv  Saída do Notebook 01 (filtrada por ELSI)
│   ├── nacional/                      Saídas do cálculo Brasil inteiro
│   ├── entrega_orientadora/           Pacote de entrega + dicionário de variáveis
│   └── eda/                           Tabelas e figuras (procedência em eda/README.md)
│       ├── fatorial/                  NB04
│       ├── fatorial_ampliada/         NB04b
│       ├── ivs_especificacoes/        NB05
│       ├── versoes_fatorial/          As 108 versões
│       ├── fatorial_multiversao/      Camadas 1 a 3
│       └── fatorial_corte_04/         Corte de carga < 0,4 e sensibilidade
│
├── analises_exploratorias/            39 decks por versão do IVS e da base (A1–A6, B1–B8, C1–C6,
│                                      D1–D5, E1–E6), síntese e Catalogo_Mestre.xlsx
├── versoes_fatorial/                  Decks e planilha das 108 versões
├── apresentacoes_multiversao/         Deck final, 12 decks de indicador (fichas/) e decks do corte
├── relatorio_descritivo/              Relatório do andamento (v3) e apoio (v4)
├── relatorio_parcial_raic/            Relatório parcial, deck oral e roteiro da RAIC 2026
│
├── docs/                              Documentação
│   ├── MANUAL_DO_PROJETO.md           Manual: onde achar tudo e como apresentar
│   ├── relatorios/                    Relatórios técnicos, auditorias e revisões
│   ├── metodologia/                   Guias de leitura e plano da análise fatorial
│   ├── referencias/                   Cálculo IVS2012, Plano de trabalho, plano do artigo
│   ├── prompts/                       Prompts de execução e arquivos de estado de cada frente
│   └── Apresentacoes_IVS/             Apresentações anteriores à multiversão (ver README.md da pasta)
│
├── graphify-out/                      Grafo de conhecimento do repositório
│
├── Backup/                            Legados — Fases 1 e 2, scripts antigos
│   ├── Fase1_IVS_Basico/              5 notebooks (sem filtro ELSI)
│   ├── Fase2_IVS_Multidimensional/    4 notebooks (sem filtro ELSI, com V01042)
│   ├── ETL/, formatar/, banco_de_dados/, worktrees_resgatadas/
│   └── DIAGNOSTICO_COMPLETO_PROJETO.md
│
└── tests/                             170 testes (artefatos, fórmulas, fatorial, motores do IVS, números da RAIC)
```

## Problemas Conhecidos

Lista resumida — detalhamento técnico em [`docs/relatorios/Relatorio_Integridade_Projeto.md`](docs/relatorios/Relatorio_Integridade_Projeto.md) e, para out/2026, em [`docs/relatorios/Simplificacao_e_Correcoes_2026-10.md`](docs/relatorios/Simplificacao_e_Correcoes_2026-10.md).

| # | Problema | Gravidade |
|---|---|---|
| 1 | ~~**Variáveis de esgoto**~~ — o dicionário oficial do IBGE (versionado em `dados/`) confirma **V00312–V00316** como esgoto inadequado; V00249–V00253 é tipologia de habitação. O diagnóstico empírico (célula `step4b` do Notebook 02, `diagnostico_esgoto_312_vs_249.csv`) corrobora. | ✅ Resolvido |
| 2 | ~~**Normalização de renda global**~~ — o índice de referência usa min/max dentro de cada município (`ie.indice`, `normalizacao='municipal'`); a global ficou como sensibilidade. | ✅ Resolvido |
| 3 | ~~**Ausência do filtro ELSI**~~ | ✅ Resolvido (Fase 3) |
| 4 | ~~**Denominadores divergentes**~~ — consolidado **V00001** (Dom. Particulares Permanentes Ocupados) na revisão de 22/05/2026; `V01042` descartado (é contagem de pessoas, não de domicílios). | ✅ Resolvido |
| 5 | **Dados legados ocupando disco** — `dados/banco_de_dados/` (~5,6 GB, fora do git; nenhum script ou notebook ativo aponta para lá) e `Backup/` (~306 MB). Limpeza opcional. | 🟢 Organizacional |
| 6 | ~~**Massas d'água contadas como sigilo**~~ — 1.736 setores sem população apareciam como `SIGILOSO`; a ordem das condições foi invertida. Nenhum setor `OK` mudou. | ✅ Resolvido |
| 7 | **Municípios pequenos após o filtro urbano** — 29 dos 70 perdem mais de 10% dos setores e 14 perdem mais da metade. Afeta a estabilidade das descritivas municipais. | 🟡 Metodológico |
| 8 | ~~**Fórmulas duplicadas nos notebooks**~~ — o NB02 importa `src/ivs_censo` desde 20/08/2026, e o dicionário `ARQUIVOS` do NB01 agora é derivado de `fontes.py`. | ✅ Resolvido |
| 9 | **Decks com números antigos** — o relatório descritivo (v3 e v4_APOIO: FA12, FA13, FP13, DS16) e os decks das 108 versões (VP08–VP13 e 97 fichas) têm trava de edição à mão e não foram regerados depois de 22/10/2026; os dados e a planilha foram. Os valores novos estão na seção 3 de `Simplificacao_e_Correcoes_2026-10.md`. Falta decidir entre regerar e corrigir à mão. | 🟡 Entregáveis |
| 10 | **Cópias com sufixo ` 2`** — centenas de arquivos não versionados (`F31_x 2.png`, `test_y 2.py`) aparecem nas regerações; causa provável é a sincronização do iCloud, não verificada. Quatro delas estão em `tests/`, e por isso o `pytest` conta 209 testes em vez de 170. Antes de apagar, compare com o original. | 🟢 Organizacional |
| 11 | **`requirements.txt` e `.venv` divergem** — o `pypdf` é usado por quatro scripts e está no `.venv`, mas não é declarado; numa instalação nova, é preciso instalá-lo à parte. O `reportlab` é o inverso: está declarado e falta no `.venv`, então os cinco `gerar_pdf_*.py` que o usam não rodam até reinstalar. Detalhes em [`scripts/README.md`](scripts/README.md). | 🟢 Manutenção |

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
- Para gerar os decks: Node.js (`npm install` instala o `pptxgenjs`); para os PDFs dos relatórios, LibreOffice

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
Os notebooks da Fase 3 devem ser executados na ordem numérica (não há Notebook 03):

```
notebooks/Fase3_EDA_ELSI/  →  01 → 02 → 04 → 04b → 05
```

Pelo Jupyter, ou sem abrir interface (mesmo resultado, útil para conferir que a
pipeline ainda roda de ponta a ponta). Sem `--inplace`, o `.ipynb` não é regravado:

```bash
./.venv/bin/python .venv/bin/jupyter-execute notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb --timeout=-1
```

- **Notebook 01:** extrai e filtra → produz `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` (109.032 setores × 74 colunas, ~27 MB).
- **Notebook 02:** EDA completa → produz as tabelas-resumo (CSVs) e 4 figuras em `banco_de_dados/eda/` — a procedência arquivo a arquivo está em [`banco_de_dados/eda/README.md`](banco_de_dados/eda/README.md).
- **Notebook 04:** análise fatorial → `banco_de_dados/eda/fatorial/`.
- **Notebook 04b:** fatorial ampliada, chamando `scripts/fatorial_ampliada.py` → `banco_de_dados/eda/fatorial_ampliada/`.
- **Notebook 05:** testes de especificação, chamando `scripts/ivs_especificacoes.py` → `banco_de_dados/eda/ivs_especificacoes/`. É gerado por `scripts/gerar_notebook_ivs_final.py`, que compara com o `HEAD`: só passa depois de commitar as saídas regeradas.

> A execução completa consome bastante RAM e tempo (~2.4 GB de CSVs brutos). Os notebooks leem apenas as colunas necessárias e processam os arquivos maiores em chunks.

### Análises fora dos notebooks
O corte de carga < 0,4 e o deck das duas propostas:

```bash
./.venv/bin/python scripts/fatorial_corte_04.py
```

```bash
./.venv/bin/python scripts/fatorial_corte_04_sensibilidade.py
```

```bash
./.venv/bin/python scripts/dados_deck_corte_04.py
```

```bash
node scripts/gerar_decks_multiversao.js C04
```

Os demais motores e geradores estão em [`scripts/README.md`](scripts/README.md); cada versão exploratória traz o comando no próprio README. Rode no máximo 3 ou 4 versões de `eda_versoes.py` ao mesmo tempo, porque todas juntas travam uma máquina de 16 GB. Depois de regerar em massa, rode o `pytest`: há testes que leem as saídas.

### Testes Sanity
```bash
./.venv/bin/python -m pytest tests/ -v --ignore-glob='* 2.py'
```

São 170 testes. O `--ignore-glob` deixa de fora as cópias ` 2` (problema 10).

## Referências Metodológicas

- SMS-BH. *Índice de Vulnerabilidade da Saúde 2012*. Belo Horizonte: Secretaria Municipal de Saúde, 2013.
- Passarelli-Araujo H. *Mapeando as disparidades socioeconômicas de saúde urbana: um estudo comparativo entre seis capitais brasileiras*. Rev. bras. Est. Pop., v.40, 1-25, 2023.
- Caiaffa WT et al. *Saúde urbana, cidades e a interseção de sistemas*. Rio de Janeiro: Fiocruz, 2021.
- Buss PM, Pellegrini Filho A. *A saúde e seus determinantes sociais*. Physis, v.17, n.1, p.77-93, 2007.
- Matos DAS, Rodrigues EC. *Análise fatorial*. Brasília: Enap, 2019.
- Figueiredo Filho DB, Silva Júnior JA. *Visão além do alcance: uma introdução à análise fatorial*. Opinião Pública, v.16, n.1, 2010.

## Créditos

**Pesquisador:** Pedro Dias Soares
**Instituição:** Fiocruz Minas — IRR
**Área:** Saúde Coletiva — Saúde Urbana e Epidemiologia Espacial
**Período:** Março/2026 – Fevereiro/2027
**Licença:** MIT (ver [LICENSE](LICENSE))
