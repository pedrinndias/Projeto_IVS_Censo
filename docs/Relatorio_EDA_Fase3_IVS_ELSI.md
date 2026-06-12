# Relatório de Análise Exploratória de Dados (EDA)

## IVS intraurbano — Censo Demográfico 2022 / ELSI-Brasil

> **Documento:** Relatório técnico-interpretativo da análise exploratória da
> Fase 3 da pipeline.
> **Pipeline:** [`notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb`](../notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb)
> **Insumos analisados:** CSVs e figuras em [`banco_de_dados/eda/`](../banco_de_dados/eda/)
> **Data:** 12 de junho de 2026 (regerado sobre a metodologia consolidada em 22/05/2026: denominador **V00001** + taxa de analfabetismo `V00901/(V00900+V00901)`)
> **Pesquisador:** Pedro Dias Soares — IC Fiocruz Minas / IRR

---

## Sumário Executivo

A análise exploratória foi conduzida sobre uma base de **109.032 setores
censitários** dos **70 municípios da amostra do ELSI-Brasil**, extraídos do
Censo Demográfico 2022. Após aplicar as regras de elegibilidade definidas pelo
IVS-BH 2012 (Secretaria Municipal de Saúde de Belo Horizonte), **106.281 setores
(97,5%)** foram considerados aptos para a análise. As **sete variáveis-componente**
do IVS foram calculadas em proporções brutas, com denominador domiciliar **V00001
(Domicílios Particulares Permanentes Ocupados)** — o equivalente no Censo 2022 do
denominador padrão do IVS-BH 2012.

Os principais achados podem ser sintetizados em quatro grandes blocos:

1. **Distribuições marcadamente assimétricas para saneamento.** As medianas de
   inadequação de água, esgoto e lixo são iguais a zero — mais da metade dos
   setores ELSI tem acesso adequado em todas as três dimensões — mas a cauda à
   direita revela bolsões de **vulnerabilidade extrema concentrados no Norte e
   em municípios pequenos do Nordeste e MG/PR rurais**. Em Portel/PA, Placas/PA
   e Autazes/AM, **mais de 95% dos setores** apresentam alguma forma de
   saneamento inadequado.

2. **Gradiente Norte→Sul replica o padrão histórico de desigualdade.** A região
   Norte apresenta as piores condições em água (35,6% setores inadequados em
   média), esgoto (27,1%) e densidade habitacional (mediana de 3,20 pessoas por
   domicílio). Em contraste, Sul e Sudeste exibem proporções médias de inadequação
   em torno de 5% ou menos para água e esgoto (medianas iguais a zero). A renda média segue o mesmo eixo, com
   municípios do Nordeste e Norte abaixo de R$ 1.800 (mediana) versus São
   Caetano do Sul/SP em R$ 5.292.

3. **Correlação forte e estruturada entre as variáveis socioeconômicas.** A
   correlação de Spearman entre renda média e proporção de pessoas pretas,
   pardas e indígenas é de **−0,81** — o maior valor absoluto observado entre
   todos os pares. Renda e analfabetismo têm correlação de **−0,75**, e raça/cor
   com analfabetismo de **+0,62**. As variáveis de saneamento se correlacionam
   menos entre si (0,14 a 0,45), mas todas se associam ao bloco socioeconômico.
   Esse padrão sustenta a hipótese de dois fatores latentes — saneamento e
   socioeconômico — recomendada pelo IVS-BH 2012.

4. **Dados faltantes concentrados em grandes cidades.** Cerca de 16% dos
   setores têm sigilo para analfabetismo (V00900/V00901), majoritariamente em
   São Caetano do Sul, Porto Alegre, Curitiba, Belo Horizonte, Rio de Janeiro e
   São Paulo — refletindo a regra do IBGE de suprimir microdados em setores com
   poucos residentes de 15 anos ou mais. As demais variáveis têm cobertura ≥ 99%.

A EDA confirma a viabilidade da construção do IVS sobre essa base e fornece
evidência empírica das hipóteses centro-periferia que o estudo se propõe a
quantificar. Recomenda-se prosseguir com a análise fatorial baseada em
**correlação de Spearman** (dada a forte assimetria das variáveis de saneamento)
e considerar **normalização da renda por município**, não global.

---

## 1. Introdução

Este relatório documenta a análise exploratória dos dados que servirão de base
para a construção do **Índice de Vulnerabilidade à Saúde (IVS) intraurbano**
para os 70 municípios participantes do ELSI-Brasil (Estudo Longitudinal da
Saúde dos Idosos Brasileiros), com dados do Censo Demográfico 2022.

A EDA cumpre quatro funções, conforme o checklist FIOCRUZ (Módulo 2 do Curso
de Análise de Dados): (i) caracterizar a estrutura e a qualidade dos dados,
(ii) detectar padrões e outliers, (iii) escolher métricas descritivas adequadas
à distribuição de cada variável e (iv) verificar pressupostos antes da
modelagem subsequente — neste caso, a análise fatorial.

Todas as **sete variáveis-componente** do IVS-BH 2012 foram operacionalizadas
para o Censo 2022 da seguinte forma:

| Dimensão | Variável | Numerador (Censo 2022) | Denominador |
|---|---|---|---|
| Saneamento | % domicílios com **água inadequada** | V00112 a V00118 | V00001 |
| Saneamento | % domicílios com **esgoto inadequado** | V00312 a V00316 | V00001 |
| Saneamento | % domicílios com **lixo inadequado** | V00398 a V00402 | V00001 |
| Socioeconômica | **Razão de moradores por domicílio** | V00005 + V00006 | V00001 + V00002 |
| Socioeconômica | **% pessoas analfabetas** (15+) | V00901 | V00900 + V00901 |
| Socioeconômica | **Rendimento médio mensal** (R$) | V06004 (direto) | — |
| Socioeconômica | **% pretos, pardos e indígenas** | V01318 + V01320 + V01321 | v0001 |

O denominador domiciliar **V00001 (Domicílios Particulares Permanentes Ocupados)** foi
adotado para os indicadores de saneamento por ser o equivalente no Censo 2022 do `V002`
(Dom_part_p) do Censo 2010, denominador padrão do IVS-BH 2012. Esta foi a decisão
consolidada na **revisão metodológica de 22/05/2026** (orientadora): o `V01042` do arquivo
de parentesco é uma contagem de *pessoas* responsáveis, não de domicílios, e foi descartado
como denominador. Validação empírica: com V00001 **nenhuma** proporção de saneamento
ultrapassa 1,0 (ver `diagnostico_proporcoes_fora_intervalo.csv`). A razão de moradores usa
`(V00001 + V00002)` para reproduzir o V0005 do IBGE, e a taxa de analfabetismo usa o total
de pessoas com 15+ anos (`V00900 + V00901`) no denominador.

---

## 2. Universo Amostral

O **Notebook 01** (Extração e Filtragem ELSI) localizou os 70 municípios
oficiais do ELSI-Brasil no arquivo básico do Censo 2022 por chave composta
(código IBGE da UF + nome normalizado do município). Todos os 70 foram
identificados, com a seguinte distribuição:

| Região | Municípios | UFs envolvidas | Setores totais |
|---|---:|---|---:|
| Sudeste | 26 | MG, ES, RJ, SP | 64.281 |
| Nordeste | 22 | MA, PI, CE, RN, PB, PE, AL, SE, BA | 20.628 |
| Sul | 9 | PR, SC, RS | 7.561 |
| Centro-Oeste | 7 | MS, MT, GO, DF | 10.171 |
| Norte | 6 | AM, PA | 6.391 |
| **Total** | **70** | **22** | **109.032** |

A dominância do Sudeste reflete o desenho amostral do ELSI-Brasil, que
contempla 26 municípios nessa região, incluindo as áreas metropolitanas de São
Paulo, Rio de Janeiro e Belo Horizonte.

---

## 3. Tratamento e Elegibilidade

### 3.1 Sigilo do IBGE

O IBGE suprime células com marcador `X` em setores onde a contagem é
suficientemente baixa para comprometer o anonimato (geralmente setores com
menos de 5 domicílios particulares permanentes para indicadores domiciliares,
e poucos indivíduos para indicadores pessoais). No Notebook 02, o marcador
`X` foi convertido em `NaN` antes da conversão para tipos numéricos.

### 3.2 Separador decimal

A variável `V06004` (rendimento médio mensal) é entregue pelo IBGE no padrão
brasileiro, com vírgula como separador decimal (ex.: `'2453,03'`). O Notebook
02 substitui a vírgula por ponto antes da conversão numérica — uma correção
crítica que recuperou 106.262 valores válidos (originalmente parseados como
NaN em ~98% dos setores por um bug de parsing).

### 3.3 Classificação `Dados_sig`

Conforme as regras do IVS-BH 2012, cada setor recebeu uma classificação:

| Classe | Critério | n | % |
|---|---|---:|---:|
| **OK** | Setor elegível para análise | 106.281 | **97,48%** |
| **SIGILOSO** | Variável-base (`v0001` ou `V00001`) sigilosa | 2.751 | 2,52% |
| COLETIVO | `V00001 = 0` com população > 0 (asilos, presídios) | 0 | 0,00% |
| ZERADO | População residente nula | 0 | 0,00% |
| **Total** | | **109.032** | 100,00% |

**Interpretação.** A taxa de elegibilidade de **97,5%** é excelente e compara
favoravelmente com o IVS-BH original (que excluiu 2,7% dos setores em 2012,
n = 106 de 3.937). Não há setores 100% coletivos nem zerados — o desenho
amostral do ELSI-Brasil concentra-se em áreas urbanas habitadas. As análises a
seguir consideram somente os **106.281 setores OK**.

---

## 4. Análise por Variável

Esta seção descreve a distribuição de cada uma das sete variáveis-componente
do IVS para o conjunto de 70 municípios ELSI. Para cada variável reportam-se
medidas de tendência central (média, mediana), dispersão (DP, CV, IQR),
forma da distribuição (assimetria, curtose) e cobertura efetiva de dados.

### 4.1 Saneamento

#### Água inadequada (`pct_agua_inad`)

| Estatística | Valor |
|---|---:|
| n | 106.281 |
| Média | 0,083 (8,3%) |
| Mediana | 0,000 |
| P75 | 0,017 (1,7%) |
| Máximo | 1,000 (100%) |
| Desvio-padrão | 0,221 |
| Coeficiente de Variação | 267,8% |
| Assimetria | +3,07 |
| Curtose | +8,46 |

**Distribuição extremamente assimétrica à direita.** A maioria absoluta dos
setores ELSI tem acesso adequado à água (mediana = 0). Mas a cauda longa
indica a existência de setores onde 100% dos domicílios têm acesso inadequado
ou ausente, elevando a média para 8,3% e produzindo um CV de 268% — um nível
de dispersão muito alto que reflete a coexistência de dois regimes
estatísticos distintos: a "norma urbana" próxima de zero e os "bolsões"
próximos de um.

**Para o artigo:** reportar **mediana e IQR**, não média e DP (a média é
fortemente influenciada pelos bolsões).

#### Esgoto inadequado (`pct_esgoto_inad`)

| Estatística | Valor |
|---|---:|
| n | 106.280 |
| Média | 0,092 (9,2%) |
| Mediana | 0,000 |
| P75 | 0,023 (2,3%) |
| Máximo | 1,000 |
| Assimetria | +2,76 |
| Curtose | +6,52 |

Padrão similar ao da água, com **35 dos 70 municípios (50%)** tendo mais da
metade dos setores com algum esgotamento inadequado.

#### Lixo inadequado (`pct_lixo_inad`)

| Estatística | Valor |
|---|---:|
| n | 106.281 |
| Média | 0,126 (12,6%) |
| Mediana | 0,000 |
| P75 | 0,071 (7,1%) |
| Máximo | 1,000 |
| Assimetria | +2,23 |

A inadequação no destino do lixo tem **média mais alta (12,6%)** que água e
esgoto, indicando que a coleta inadequada é um problema mais disseminado
mesmo em municípios bem-atendidos quanto a água e esgoto.

### 4.2 Razão de moradores por domicílio (`razao_moradores`)

| Estatística | Valor |
|---|---:|
| n | 106.281 |
| Média | 2,70 |
| Mediana | 2,72 |
| Desvio-padrão | 0,40 |
| Assimetria | +0,09 |
| Mínimo | 1,00 |
| Máximo | 8,79 |

Variável de comportamento **mais simétrico** — média e mediana praticamente
coincidem. Com o denominador `(V00001 + V00002)`, o mínimo é **1,00** (ao menos um
morador por domicílio ocupado), eliminando os valores < 1 que apareciam com o
denominador anterior (V01042). A densidade média brasileira de moradores por domicílio é
historicamente próxima de 3,0; o valor observado (2,70) está dentro do
esperado e a baixa variabilidade (CV = 14,8%) sugere que esta variável
contribuirá com **menos discriminação** ao IVS do que as variáveis de
saneamento — mas é homogeneamente informativa.

### 4.3 Analfabetismo (`pct_analfab`)

| Estatística | Valor |
|---|---:|
| n | 89.527 (cobertura: 84,2%) |
| Média | 0,039 (3,9%) |
| Mediana | 0,028 (2,8%) |
| P25 / P75 | 0,013 / 0,052 (1,3% / 5,2%) |
| Máximo | 0,842 (84,2%) |
| Assimetria | +2,98 |
| Curtose | +17,7 |

A cobertura efetiva de 84% (15,8% sigilo) reflete a supressão do IBGE em
setores com poucos indivíduos de 15 anos ou mais. Com o denominador correto
`V00901 / (V00900 + V00901)`, a taxa fica naturalmente limitada a [0, 1]
(máximo observado 84,2%, contra os valores espúrios > 1 que a fórmula anterior
`V00901 / V00900` produzia). A mediana de 2,8% é compatível com a taxa nacional
de analfabetismo — esperada inferior em territórios urbanos. A alta curtose
(+17,7) indica a existência de setores com **taxa de analfabetismo extremamente
elevada**, concentrados em pequenos municípios do Nordeste rural (Arara/PB
mediana de **31,1%**, Jaqueira/PE 24,9%, Água Preta/PE 24,2%).

### 4.4 Rendimento médio (`renda_media`)

| Estatística | Valor (R$) |
|---|---:|
| n | 106.262 |
| Média | 4.141,33 |
| Mediana | 2.545,98 |
| P25 | 1.735,33 |
| P75 | 4.755,20 |
| Mínimo | 318,88 |
| Máximo | 170.418,06 |
| Assimetria | +3,76 |
| Curtose | +49,9 |

A renda apresenta a **distribuição mais assimétrica** entre todas as
variáveis, com média (R$ 4.141) muito superior à mediana (R$ 2.546) — sinal
clássico de concentração de renda. A cauda direita estende-se a valores
extremos (R$ 170 mil), refletindo setores residenciais de altíssima renda nas
áreas nobres das capitais.

**Para o artigo, é mandatório usar mediana e IQR** para reportar renda. O
intervalo interquartil de R$ 3.020 já é, por si só, ilustrativo da
heterogeneidade dentro das ELSI.

### 4.5 Raça/Cor — pretos, pardos e indígenas (`pct_raca_pretpardind`)

| Estatística | Valor |
|---|---:|
| n | 106.279 |
| Média | 0,530 (53,0%) |
| Mediana | 0,576 (57,6%) |
| Desvio-padrão | 0,229 |
| Assimetria | −0,39 |
| Curtose | −0,81 |

Esta é a **única variável com assimetria negativa** e a única bem distribuída
no intervalo [0,1]: a curtose negativa indica uma distribuição mais plana que
a Normal. A mediana de **57,6%** revela que, no conjunto ELSI, a maioria dos
setores tem mais de metade da população classificada como preta, parda ou
indígena. Discriminação regional é elevada — ver Seção 5.

---

## 5. Análise Regional

A Tabela abaixo apresenta as medianas das sete variáveis estratificadas pelas
cinco regiões geográficas do Brasil. Valores em negrito indicam o **pior**
desempenho regional para cada indicador.

| Região | Água inad. | Esgoto inad. | Lixo inad. | Razão mor. | Analfab. | Renda média (R$) | PPI |
|---|---:|---:|---:|---:|---:|---:|---:|
| Norte | **0,199** | **0,082** | 0,000 | **3,20** | 0,030 | 1.774 | **0,774** |
| Nordeste | 0,011 | 0,000 | 0,000 | 2,79 | **0,053** | **1.693** | 0,737 |
| Centro-Oeste | 0,000 | 0,000 | 0,000 | 2,81 | 0,028 | 3.083 | 0,607 |
| Sudeste | 0,000 | 0,000 | 0,000 | 2,66 | 0,024 | 2.714 | 0,514 |
| Sul | 0,000 | 0,000 | 0,000 | 2,60 | 0,017 | **3.686** | 0,222 |

> *PPI = pretos, pardos e indígenas. Valores em negrito: pior do indicador.*

### Interpretação substantiva

- **Norte e Nordeste concentram a precariedade.** A Região Norte lidera tanto
  na inadequação de água (mediana de 20% dos setores) quanto na densidade
  habitacional (3,2 pessoas por domicílio). O Nordeste tem a pior renda
  (mediana R$ 1.693) e o pior analfabetismo (5,3%).

- **Sul é a região mais bem-atendida e mais homogeneamente branca.** A renda
  mediana é a maior (R$ 3.686), a inadequação de saneamento é praticamente
  nula nas medianas, o analfabetismo é o menor (1,7%) e a proporção de
  pretos/pardos/indígenas é dramaticamente inferior (22,2%, contra 77,4% no
  Norte). Esse contraste de **55 pontos percentuais** entre Norte e Sul para
  raça/cor é o maior gradiente regional observado entre todas as variáveis.

- **Centro-Oeste apresenta perfil dual.** A renda mediana (R$ 3.083) é puxada
  fortemente para cima por Brasília/DF e Campo Grande/MS. A composição
  raça/cor (60,7%) está intermediária. As variáveis de saneamento ficam
  próximas do Sudeste, sugerindo boa cobertura urbana mesmo em municípios
  menos populosos como Vicentinópolis/GO.

- **Sudeste tem o maior contraste interno.** Embora os indicadores agregados
  da região sejam bons, ela contém tanto municípios excelentes (São Caetano
  do Sul, com renda mediana de R$ 5.292) quanto periferias problemáticas. A
  análise por município (Seção 6) revela essa heterogeneidade.

---

## 6. Heterogeneidade Municipal

Esta seção lista os municípios extremos em cada variável-componente do IVS,
extraídos da tabela [`descritivas_por_municipio.csv`](../banco_de_dados/eda/descritivas_por_municipio.csv).

### 6.1 Top-5 municípios com PIORES medianas em saneamento

| Posição | Água | Esgoto | Lixo |
|---|---|---|---|
| 1 | Portel/PA (99,0%) | Placas/PA (98,7%) | Portel/PA (99,4%) |
| 2 | Placas/PA (97,1%) | Portel/PA (98,4%) | Autazes/AM (96,7%) |
| 3 | Autazes/AM (96,4%) | Santa Maria do Oeste/PR (98,3%) | Salto/SP (96,4%) |
| 4 | Coroaci/MG (95,7%) | Urandi/BA (98,2%) | Placas/PA (94,2%) |
| 5 | Santa Maria do Oeste/PR (93,8%) | Japoatã/SE (98,2%) | São R. do Doca Bezerra/MA (91,4%) |

Os municípios do **Pará** (Portel, Placas) e **Amazonas** (Autazes) aparecem
sistematicamente entre os piores em todos os três quesitos. **Coroaci/MG,
Santa Maria do Oeste/PR, Urandi/BA e Japoatã/SE** são pequenos
municípios rurais cuja inadequação tende a ser próxima de 100% em quase todos
os setores — atenção para o n pequeno (29 a 47 setores).

A presença de **Salto/SP** no top-5 de lixo inadequado é surpreendente para
um município paulista — pode indicar problema de classificação categórica nas
variáveis V00398-V00402 que merece checagem (e.g., se "caçamba de serviço de
limpeza" foi indevidamente contabilizada como inadequada, conforme observação
no documento `Cálculo IVS2012.docx`).

### 6.2 Renda mediana — extremos

| Posição | Mais baixa (R$) | Mais alta (R$) |
|---|---|---|
| 1 | Portel/PA — **1.022** | São Caetano do Sul/SP — **5.292** |
| 2 | Rosário/MA — 1.039 | Curitiba/PR — 4.115 |
| 3 | Água Preta/PE — 1.055 | Porto Alegre/RS — 3.951 |
| 4 | Jaqueira/PE — 1.073 | Brasília/DF — 3.388 |
| 5 | São R. do Doca Bezerra/MA — 1.083 | Campinas/SP — 3.375 |

A razão entre o município mais rico (São Caetano do Sul) e o mais pobre
(Portel) é de **5,18 vezes** — magnitude condizente com a desigualdade
estrutural histórica do Brasil. Esses extremos serão fundamentais quando se
discutir a **normalização da renda**: uma normalização min-max global (como
empregada pela Fase 2 da pipeline) comprime essa amplitude para [0,1], mas
trata Portel e São Caetano como pertencendo ao mesmo "mercado de renda" —
algo claramente inadequado para uma análise intraurbana. A normalização
**por município** é fortemente recomendada para o IVS final.

### 6.3 Outros padrões municipais

- **Maior razão de moradores por domicílio:** Portel/PA (4,6) e Autazes/AM
  (3,7) — coerente com a precariedade habitacional dessas localidades.
- **Maior taxa de analfabetismo:** Arara/PB (31,1%), Jaqueira/PE (24,9%),
  Água Preta/PE (24,2%) — municípios pequenos do Nordeste interior.
- **Maior proporção de pretos/pardos/indígenas:** Autazes/AM (92,9%),
  Salvador/BA (88,9%), Rosário/MA (88,1%), Portel/PA (87,8%), Itajuípe/BA
  (84,5%).

---

## 7. Análise de Outliers (regra IQR)

A regra clássica do diagrama de caixa (Tukey, 1977) classifica como outlier
qualquer valor fora do intervalo `[Q1 − 1,5·IQR, Q3 + 1,5·IQR]`. Os resultados
estão em [`outliers.csv`](../banco_de_dados/eda/outliers.csv):

| Variável | n_outliers | % outliers | Interpretação |
|---|---:|---:|---|
| pct_agua_inad | 21.476 | **20,2%** | Artefato da concentração em zero |
| pct_esgoto_inad | 21.158 | **19,9%** | Artefato da concentração em zero |
| pct_lixo_inad | 19.557 | **18,4%** | Artefato da concentração em zero |
| renda_media | 10.850 | 10,2% | Outliers reais — cauda direita |
| pct_analfab | 4.696 | 5,2% | Setores de alta vulnerabilidade educacional |
| razao_moradores | 3.829 | 3,6% | Setores com superlotação extrema |
| pct_raca_pretpardind | 0 | 0,0% | Distribuição bem-comportada |

**Interpretação importante.** Os altos percentuais de "outliers" em água,
esgoto e lixo (~20%) **não são erros nem aberrações estatísticas**, mas
consequência matemática direta da regra IQR aplicada a uma distribuição
extremamente concentrada em zero: como Q1 = 0 e Q3 é muito próximo de zero
(0,017 para água), qualquer valor moderado fica acima de
`Q3 + 1,5·IQR ≈ 0,04`. Isso significa que **a regra IQR não é apropriada
para identificar valores aberrantes nessas variáveis** — ela apenas redescobre
o fato já conhecido de que as inadequações de saneamento têm distribuição
bimodal.

Recomendação: **não excluir nenhum setor com base em outliers de saneamento.**
Os bolsões de inadequação extrema são o objeto principal do estudo, não
ruído a remover.

Para renda, os outliers superiores correspondem a setores de altíssima renda
em áreas nobres das capitais e devem ser preservados; influenciarão a
normalização e justificam o uso de mediana e IQR para descrição.

---

## 8. Análise de Dados Faltantes

### 8.1 Cobertura por variável (global)

| Variável | n válidos | % cobertura |
|---|---:|---:|
| pct_agua_inad | 106.281 | 100,00% |
| pct_lixo_inad | 106.281 | 100,00% |
| razao_moradores | 106.281 | 100,00% |
| pct_esgoto_inad | 106.280 | 100,00% |
| pct_raca_pretpardind | 106.279 | 100,00% |
| renda_media | 106.262 | 99,98% |
| **pct_analfab** | **89.527** | **84,24%** |

### 8.2 Concentração de missing em grandes cidades (analfabetismo)

Os setores com sigilo em V00900/V00901 concentram-se em municípios densamente
povoados — onde a regra do IBGE de suprimir setores com poucos indivíduos
acaba afetando muitas microáreas. Os 10 municípios com maior taxa de missing
para analfabetismo:

| Município | UF | % missing analfab. |
|---|---|---:|
| São Caetano do Sul | SP | 29,7% |
| Porto Alegre | RS | 27,5% |
| Curitiba | PR | 23,1% |
| São Pedro da Aldeia | RJ | 22,7% |
| Belo Horizonte | MG | 22,5% |
| Canoas | RS | 20,9% |
| Rio de Janeiro | RJ | 20,0% |
| Campinas | SP | 19,9% |
| São Paulo | SP | 19,7% |
| Araçatuba | SP | 18,5% |

Inversamente, **11 municípios pequenos têm zero missing em todas as
variáveis**: Arara/PB, Coroaci/MG, Ibatiba/ES, Itajuípe/BA, Jaqueira/PE,
Portel/PA, Salinas/MG, Santa Maria do Oeste/PR, São Raimundo do Doca
Bezerra/MA, Urandi/BA e Água Preta/PE.

**Implicação metodológica.** O sigilo do IBGE introduz um **viés sistemático**
nas análises agregadas: setores pequenos (que tendem a ser de classes médias
em vias urbanas tradicionais) são preferencialmente suprimidos. Discutir essa
limitação na seção de Discussão do artigo, conforme já indicado no
[`Plano_Artigo_Cientifico_IC_Preenchido.docx`](Plano_Artigo_Cientifico_IC_Preenchido.docx).

---

## 9. Estrutura de Correlações

A matriz de correlação fornece a evidência empírica mais direta da estrutura
latente que a análise fatorial buscará explicitar. São apresentados dois
coeficientes — Pearson (paramétrico, mede associação linear) e Spearman
(não-paramétrico, baseado em postos, robusto à assimetria). **Dada a forte
assimetria das variáveis de saneamento e renda, Spearman é mais informativo.**

### 9.1 Matriz de Spearman

|  | água | esgoto | lixo | razão | analfab | renda | PPI |
|---|---:|---:|---:|---:|---:|---:|---:|
| pct_agua_inad | 1,00 | 0,45 | 0,14 | 0,27 | 0,27 | −0,28 | 0,36 |
| pct_esgoto_inad | 0,45 | 1,00 | 0,23 | 0,35 | **0,45** | **−0,46** | 0,44 |
| pct_lixo_inad | 0,14 | 0,23 | 1,00 | −0,04 | 0,19 | −0,18 | 0,21 |
| razao_moradores | 0,27 | 0,35 | −0,04 | 1,00 | 0,41 | −0,44 | 0,46 |
| pct_analfab | 0,27 | 0,45 | 0,19 | 0,41 | 1,00 | **−0,75** | **0,62** |
| renda_media | −0,28 | −0,46 | −0,18 | −0,44 | −0,75 | 1,00 | **−0,81** |
| pct_raca_pretpardind | 0,36 | 0,44 | 0,21 | 0,46 | 0,62 | **−0,81** | 1,00 |

> *Valores em negrito: |ρ| ≥ 0,45.*

### 9.2 Leitura substantiva

**Eixo socioeconômico (dimensão dominante).** As três correlações mais fortes
são todas no triângulo renda × analfabetismo × raça/cor (PPI):

- **renda × PPI = −0,81**
- **renda × analfab = −0,75**
- **analfab × PPI = +0,62**

Esse resultado é metodologicamente importante: ele sustenta a hipótese de
**raça/cor como proxy de vulnerabilidade socioeconômica estrutural**,
mencionada no Plano do Artigo (Tabela 5, onde a variável aparece com um
asterisco). A correlação de −0,81 entre PPI e renda média é o sinal empírico
mais forte da desigualdade racial-econômica nos territórios do ELSI-Brasil e
sustenta a inclusão da variável raça/cor no IVS apesar de ser uma variável
categórica subjacente.

**Densidade habitacional como mediadora.** A razão de moradores correlaciona
positivamente com PPI (0,46) e com analfabetismo (0,41), e negativamente com
renda (−0,44). Embora não seja a variável mais discriminante, contribui de
forma coerente para o vetor socioeconômico.

**Eixo saneamento (dimensão secundária).** Água, esgoto e lixo formam um
bloco coerente, mas com correlações entre si mais modestas (0,14 a 0,45). A
correlação **esgoto × analfabetismo = +0,45** sugere que esgoto inadequado
pode estar relacionado a contextos socioeconômicos vulneráveis — uma
correlação cruzada entre dimensões.

**Lixo é o componente mais autônomo.** Suas correlações com as demais
variáveis raramente excedem 0,20. Isso significa que o indicador de lixo
trará informação **distinta** dos demais — possivelmente capturando uma
dimensão de cobertura municipal de serviços de limpeza pública que não se
reduz à pobreza individual.

### 9.3 Implicações para a análise fatorial

A estrutura de correlações é coerente com **dois fatores latentes**:

1. **Fator 1 (socioeconômico):** renda média (invertida), analfabetismo,
   raça/cor (PPI), razão de moradores. Esperam-se cargas fatoriais altas para
   estas quatro variáveis.
2. **Fator 2 (saneamento):** água inadequada, esgoto inadequado, lixo
   inadequado. Cargas fatoriais menores, mas coerentes.

O **peso relativo** do Fator 1 será provavelmente superior ao do Fator 2 —
consistente com a divisão histórica do IVS-BH (~60% socioeconômico / ~40%
saneamento). A confirmação dependerá da análise fatorial (PCA ou Análise
Fatorial Exploratória) no Notebook 03.

> **Recomendação técnica:** usar a matriz de correlação de **Spearman** como
> entrada da análise fatorial, dado o desvio acentuado de normalidade das
> variáveis de saneamento e renda (assimetrias 2,2 a 4,7).

---

## 10. Implicações para a Construção do IVS

Esta EDA sustenta cinco recomendações práticas para a construção do índice
nas etapas seguintes:

1. **Reportar mediana e IQR** (não média e DP) nas tabelas descritivas do
   artigo para todas as variáveis assimétricas (água, esgoto, lixo, renda,
   analfabetismo).

2. **Normalizar renda por município**, e não globalmente. A razão de 5,18×
   entre os extremos (Portel × São Caetano do Sul) confirma que a renda
   precisa ser interpretada relativamente ao mercado local de cada cidade,
   sob pena de comprimir indevidamente a variação intraurbana.

3. **Usar correlação de Spearman** como entrada da análise fatorial, em
   função da forte assimetria não-linear das variáveis.

4. **Preservar os outliers de saneamento** — não são erros, são justamente os
   bolsões de vulnerabilidade que o estudo se propõe a identificar. A regra
   IQR é inadequada como critério de exclusão para essas variáveis.

5. **Considerar imputação ou exclusão pareada para o sigilo de
   analfabetismo.** Excluir os ~16% de setores com sigilo poderia introduzir
   viés contra grandes cidades. Imputar a mediana municipal é uma opção
   metodologicamente defensável.

---

## 11. Limitações da Análise Exploratória

| Limitação | Origem | Mitigação proposta |
|---|---|---|
| 16% de sigilo em analfabetismo | Regra IBGE de supressão | Reportar transparentemente; considerar imputação por mediana municipal |
| Variáveis de saneamento bimodais | Realidade da cobertura nacional | Análises com mediana/IQR; análises fatoriais robustas |
| Município de Salto/SP atípico em lixo | Possível classificação categórica de "caçamba de serviço" | Validar com o dicionário do IBGE |
| Correlação 0,14 entre água e lixo | Heterogeneidade real entre serviços | Tratar como bloco saneamento mesmo assim |
| Falácia ecológica | Inerente ao delineamento ecológico | Reportar explicitamente na seção de Discussão do artigo |

---

## 12. Próximos Passos

1. **Notebook 03 — Análise Fatorial.** Aplicar PCA / Análise Fatorial
   Exploratória sobre a matriz de correlação de Spearman para extrair os
   pesos das variáveis e gerar o **IVS contínuo (0–1)**.
2. **Categorização em 4 faixas.** Definir os pontos de corte
   (Baixo / Médio / Elevado / Muito Elevado) com base em quartis ou desvios
   da média, conforme metodologia IVS-BH.
3. **Geoprocessamento.** Construir os mapas temáticos do IVS por setor
   censitário no QGIS 3.x. Atenção aos 10 municípios pequenos (n < 50 setores)
   onde o mapa será menos rico visualmente.
4. **Revisão metodológica com a orientadora.** Submeter as recomendações
   desta EDA (normalização por município, uso de Spearman, tratamento de
   sigilo) antes da execução do Notebook 03.
5. **Iniciar a redação dos Resultados** do artigo a partir das tabelas e
   figuras desta EDA — especialmente a **Tabela 1** (descritivas por
   município) e a **Figura 1** (matriz de correlação).

---

## Anexos — Localização dos artefatos

| Arquivo | Caminho | Conteúdo |
|---|---|---|
| Base bruta filtrada | [`banco_de_dados/Base_ELSI_Bruta_Censo2022.csv`](../banco_de_dados/Base_ELSI_Bruta_Censo2022.csv) | 109k setores × 47 colunas (Notebook 01) |
| Descritivas globais | [`banco_de_dados/eda/descritivas_globais.csv`](../banco_de_dados/eda/descritivas_globais.csv) | 7 variáveis × 12 estatísticas |
| Descritivas por município | [`banco_de_dados/eda/descritivas_por_municipio.csv`](../banco_de_dados/eda/descritivas_por_municipio.csv) | 70 mun × 7 var |
| Descritivas por região | [`banco_de_dados/eda/descritivas_por_regiao.csv`](../banco_de_dados/eda/descritivas_por_regiao.csv) | 5 reg × 7 var |
| Outliers | [`banco_de_dados/eda/outliers.csv`](../banco_de_dados/eda/outliers.csv) | Regra IQR |
| Missing por município | [`banco_de_dados/eda/missing_por_municipio.csv`](../banco_de_dados/eda/missing_por_municipio.csv) | % faltante por mun × var |
| Correlações | [`banco_de_dados/eda/correlacao_pearson.csv`](../banco_de_dados/eda/correlacao_pearson.csv) · [`spearman.csv`](../banco_de_dados/eda/correlacao_spearman.csv) | Matriz 7×7 |
| Elegibilidade | [`banco_de_dados/eda/elegibilidade_setores.csv`](../banco_de_dados/eda/elegibilidade_setores.csv) | Distribuição `Dados_sig` |
| Figuras | [`banco_de_dados/eda/figuras/`](../banco_de_dados/eda/figuras/) | Histogramas, boxplots, missing, correlação |

---

## Referências metodológicas

- SMS-BH. *Cálculo IVS 2012* — documento operacional do Índice de
  Vulnerabilidade da Saúde de Belo Horizonte (em [`docs/Cálculo IVS2012.docx`](Cálculo%20IVS2012.docx)).
- FIOCRUZ — Campus Virtual. *Curso de Análise de Dados, Módulo 2: Estatística
  Descritiva e Comunicação de Resultados* (em [`docs/guia_analises.docx`](guia_analises.docx)).
- Passarelli-Araujo, H. (2023). *Mapeando as disparidades socioeconômicas de
  saúde urbana: um estudo comparativo entre seis capitais brasileiras*. Revista
  Brasileira de Estudos de População, v. 40.
- Tukey, J.W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
