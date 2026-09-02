# Análise fatorial e o IVS do Censo 2022

## O artigo de Figueiredo Filho & Silva Júnior (2010) lido a partir do projeto — e testado nos dados dele

**Projeto:** Índice de Vulnerabilidade à Saúde (IVS) intraurbano — Censo Demográfico 2022 / ELSI-Brasil
**Instituição:** Fiocruz Minas — Instituto René Rachou (IRR) · Iniciação Científica
**Pesquisador:** Pedro Dias Soares
**Data:** 24 de agosto de 2026

**Artigo analisado:** FIGUEIREDO FILHO, Dalson Britto; SILVA JÚNIOR, José Alexandre da. *Visão além do alcance: uma introdução à análise fatorial.* Opinião Pública, Campinas, v. 16, n. 1, p. 160–185, jun. 2010.

---

## Sumário executivo

Este documento faz três coisas: sintetiza o artigo, mostra ponto a ponto onde ele encosta no projeto e — em vez de parar na correspondência conceitual — **roda os testes que o artigo prescreve sobre os dados reais do projeto**, nos 104.108 setores censitários do recorte de análise. Os testes estão em `scripts/diagnostico_fatorial.py` e as tabelas em `banco_de_dados/eda/fatorial/`.

O que saiu disso:

1. **O artigo é o manual da única etapa central que ainda falta.** O `GUIA_DO_PROJETO.md` (§8) lista "Análise fatorial / pesos / cálculo do IVS final" como pendente, e o relatório da EDA (§15) prevê um Notebook 04 com "KMO, Bartlett, número de fatores, cargas e pesos" — que é literalmente a sequência das Tabelas 1 a 3 do artigo.

2. **A base é adequada à análise fatorial, pelos critérios do próprio artigo.** Com os 7 componentes do IVS e correlação de Spearman: KMO = 0,783 (faixa "mediano" de Friel, bem acima do piso de 0,50 de Hair), BTS = 235.084 com 21 g.l. e p < 0,001, 57,1% dos coeficientes com |r| ≥ 0,30, e razão de 12.506 casos por variável — contra o mínimo de 5 para 1 recomendado.

3. **O indicador de lixo não pertence ao índice, e agora isso está medido.** Ele não aparece com comunalidade baixa: ele **forma um fator só dele** (carga 0,919 no segundo componente rotacionado, comunalidade 0,859, correlações de 0,10 a 0,20 com todo o resto). É o retrato exato da variável que o artigo manda considerar excluir por ser "estatisticamente independente das demais". Isso converte a ressalva empírica da §6.2.10 do Guia em evidência.

4. **A regra mecânica de comunalidade do artigo teria excluído a variável errada.** Na solução com as 7 variáveis, quem fica abaixo de 0,50 é a **água** (0,253) — e o artigo diz para excluir e re-rodar. Mas a comunalidade da água é baixa *porque o lixo sequestrou o segundo fator*: retirado o lixo, a água sobe para 0,822. Seguir a regra sem olhar a estrutura teria custado ao índice um componente central de saneamento.

5. **Os pesos empíricos convergem com os da literatura.** Sem o lixo, os dois fatores rotacionados distribuem 65% do peso para a dimensão socioeconômica e 35% para saneamento — perto da referência do IVS-BH 2012 (60/40) que o projeto já adota. A decisão em aberto nº 1 da §6.3 do Guia deixa de ser um dilema e vira uma convergência a ser reportada.

6. **A ordem entre normalizar e fatorar não é indiferente — e isso é uma decisão nova.** A padronização min-max **por município** prevista para o Notebook 03 é uma transformação afim com escala diferente por grupo: ela muda a matriz de correlação e, com ela, todo o resultado. Nos mesmos setores, o KMO cai de 0,783 para 0,720, o critério de Kaiser passa a apontar 3 fatores em vez de 2, e a repartição dos pesos entre as duas dimensões vai de 65/35 para 56/44. Rodar a fatorial antes ou depois do NB03 dá índices diferentes.

7. **Há três pontos em que o artigo não alcança o problema deste projeto**, e é preciso dizê-los na dissertação metodológica: o Bartlett é vazio com dezenas de milhares de casos, a ACP sobre matriz de Spearman é uma ACP de postos e precisa ser declarada como tal, e o artigo trata de mensurar um construto — não de compor um índice ponderado, que é o passo seguinte e pede outra literatura.

---

## 1. O artigo em síntese

### 1.1 O problema que ele ataca

O artigo parte de um problema de mensuração: como medir o que não se observa diretamente. Os autores enunciam duas saídas. A primeira é eleger um **proxy** — e o exemplo que eles dão, logo na introdução, é justamente medir **vulnerabilidade social** por uma linha de pobreza. Simples, e arriscado: nem sempre existe proxy adequado. A segunda é identificar variáveis que "caminham juntas" e reduzi-las a poucas dimensões latentes por **análise fatorial**. Mais informativa, e mais exigente tecnicamente.

O projeto está inteiramente do lado da segunda saída: sete variáveis do Censo que se supõe manifestarem um construto único — vulnerabilidade à saúde do território.

### 1.2 Duas distinções que o artigo faz e que importam aqui

**Exploratória (AFE) × confirmatória (AFC).** A AFE explora o padrão de correlação sem hipótese prévia sobre a estrutura; a AFC testa em que medida certas variáveis representam dimensões definidas *a priori* pela teoria. O artigo se declara confirmatório: fixa duas dimensões vindas de Dahl (1971) e verifica se os indicadores se organizam nelas.

**ACP × AF propriamente dita.** Ambas produzem combinações lineares que maximizam variância captada, mas a ACP usa **toda** a variância e a AF apenas a **compartilhada**. A citação que o artigo traz de Tabachnick e Fidell resume a escolha: análise fatorial para uma solução teórica não contaminada por erro; componentes principais para um resumo empírico do conjunto de dados. Hair et al. são citados para relativizar: com mais de 30 variáveis, ou comunalidades acima de 0,60 na maioria delas, as duas chegam praticamente ao mesmo lugar. O artigo usa ACP, por ser o método mais difundido.

### 1.3 Os três estágios do planejamento

**Estágio 1 — adequabilidade da base.**

| Critério | Patamar recomendado no artigo |
|---|---|
| Nível de mensuração | Variáveis contínuas ou discretas; categóricas só como *dummies* |
| Tamanho da amostra | Mínimo 50, desejável 100 ou mais |
| Razão casos/variáveis | Igual ou superior a 5 para 1 |
| Padrão de correlação | A maior parte dos coeficientes acima de 0,30 |
| KMO | Piso de 0,50 (Hair et al.); 0,60 em Pallant. Escala de Friel: 0,90–1 excelente · 0,80–0,89 bom · 0,70–0,79 mediano · 0,60–0,69 medíocre · 0,50–0,59 ruim · abaixo de 0,50 inadequado |
| Bartlett Test of Sphericity (BTS) | Estatisticamente significante (p < 0,05) |

**Estágio 2 — extração e número de fatores.** Escolher a técnica de extração e decidir quantos fatores reter, num *trade-off* declarado entre parcimônia e variância explicada. Os critérios oferecidos: regra de Kaiser (autovalor > 1, que funciona melhor entre 20 e 50 variáveis), *scree test* de Cattell, variância acumulada com patamar de 60% em Hair et al., e — em perspectiva confirmatória — a **razão teórica**, que o artigo trata como critério legítimo ao lado dos estatísticos. Em nota de rodapé o artigo ainda registra a análise paralela de Horn (1965): reter apenas os autovalores maiores que os gerados por dados aleatórios de mesmo tamanho.

**Estágio 3 — rotação.** Ortogonal (Varimax, Quartimax, Equamax), que supõe fatores independentes e é mais fácil de reportar; ou oblíqua (Oblimin, Promax), que permite fatores correlacionados e é mais difícil de interpretar. O artigo usa Varimax, por ser a mais comum.

### 1.4 As estatísticas de leitura dos resultados

Depois de estimar, o artigo percorre — e é aqui que ele vira um checklist utilizável:

- **Comunalidade**: proporção da variância de cada variável explicada pelos fatores retidos. Mínimo usual de 0,50; abaixo disso, "a variável deve ser excluída e a análise fatorial deve ser realizada novamente". O artigo trata a comunalidade como o **teste final de inclusão** de uma variável.
- **Cargas fatoriais**: limite de 0,40 para considerar que a variável contribui para o fator.
- **Estrutura simples**: a mesma variável não deve carregar acima de 0,40 em dois fatores. No exemplo, duas variáveis violam isso, são excluídas, e o modelo é re-estimado — passando de 75,79% para 82,30% de variância acumulada com uma solução mais parcimoniosa.
- **Escores fatoriais**: os fatores extraídos, padronizados (média zero, distância em desvios-padrão), viram os eixos de um plano em que os casos são classificados por quadrante.

### 1.5 O exemplo e a conclusão

O exemplo aplica ACP com Varimax a 10 indicadores de democracia, 127 países em 1985, e recupera as duas dimensões da poliarquia de Dahl (1971): contestação e inclusividade. A conclusão é uma tese sobre erro de medida: variáveis mal medidas comprometem a validade das inferências.

---

## 2. Por que este artigo importa para este projeto

### 2.1 Ele é o manual da etapa que falta

O estado do projeto, pelo `GUIA_DO_PROJETO.md`:

| Etapa | Status registrado |
|---|---|
| Notebook 01 — extração e filtro ELSI | ✅ concluída |
| Notebook 02 — EDA completa | ✅ concluída |
| Linha de base nacional | ✅ concluída |
| Normalização de renda por município | 🔴 pendente |
| **Análise fatorial / pesos / IVS final** | 🔴 **pendente** |
| Categorização em 4 faixas | 🔴 pendente |
| Mapas temáticos (QGIS) | 🔴 pendente |

O plano do relatório da EDA (§15) descreve o Notebook 04 como "Análise fatorial: KMO, Bartlett, número de fatores, cargas e pesos". É a Tabela 1 do artigo, item por item. O artigo não é uma referência tangencial: é o roteiro da etapa seguinte.

### 2.2 A correspondência é estrutural, não analógica

O paralelo entre o desenho do artigo e o do projeto é mais forte do que a semelhança de método:

| | Artigo (Figueiredo & Silva, 2010) | Projeto IVS — Censo 2022 |
|---|---|---|
| Construto latente | Democracia | Vulnerabilidade à saúde do território |
| Teoria que define as dimensões | Dahl (1971), *Poliarquia* | IVS-BH 2012 (SMS-BH, 2013) |
| Dimensões esperadas | Contestação e inclusividade | Saneamento e socioeconômica |
| Variáveis observadas | 10 indicadores de democracia | 7 componentes do Censo 2022 |
| Unidade de análise | País-ano (127 casos, 1985) | Setor censitário (104.108 urbanos elegíveis) |
| Postura | Confirmatória: nº de fatores fixado a priori | Confirmatória: duas dimensões vindas do IVS-BH |
| Uso do resultado | Escores como eixos de classificação | Pesos para compor o índice e classificar em 4 faixas |

Nos dois casos há uma teoria que **precede** os dados e diz quantas dimensões esperar. É a diferença entre "vamos ver o que aparece" e "vamos testar se aparece o que a teoria previu" — e ela muda a leitura dos critérios de retenção, como se verá na §4.4.

### 2.3 Ele responde a uma decisão explicitamente em aberto

A §6.3 do Guia registra quatro decisões travadas. A primeira:

> **Critério dos pesos**: empíricos (análise fatorial) ou guiados pela literatura (60% socioeconômica / 40% saneamento, padrão IVS-BH)?

E o argumento já anotado a favor dos pesos empíricos: renda, cor/raça e analfabetismo se correlacionam a −0,81 e −0,76, de modo que pesos iguais dariam "três votos" à posição social sem que isso fosse escolha deliberada. Esse é exatamente o raciocínio do artigo — variáveis que "caminham juntas" medem em boa parte a mesma coisa, e tratá-las como informação independente é erro de medida.

O artigo, porém, **não decide** entre peso empírico e peso teórico: ele mostra como extrair a estrutura. A decisão sobre pesos é do projeto, e a §5 deste documento mostra que, com os números na mesa, ela ficou bem mais fácil.

---

## 3. Aplicação: os critérios do artigo rodados nos dados do projeto

### 3.1 Como foi feito

- **Script:** `scripts/diagnostico_fatorial.py` (só pandas e numpy — nenhuma dependência nova).
- **Base:** `banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.csv`.
- **Recorte:** `urbano = 1` e `Dados_sig = OK` — o mesmo recorte de análise do Notebook 02.
- **Variáveis:** os 7 componentes do IVS, com a **renda invertida** (−renda) para que todas apontem no mesmo sentido: valor maior = mais vulnerável. A inversão não altera |r|, autovalores, KMO nem comunalidades; altera apenas o sinal das cargas, e com isso a leitura.
- **Correlação:** Spearman como referência, seguindo a decisão já tomada na §9 do relatório da EDA ("uso Spearman como referência porque as distribuições estão longe da normalidade"); Pearson calculado em paralelo para comparação.
- **Extração:** componentes principais sobre a matriz de correlação, com rotação Varimax implementada no próprio script.
- **Cenários:** as 7 variáveis; sem o lixo; sem o analfabetismo (para medir o efeito do descarte por sigilo); e os dois primeiros repetidos sobre os dados padronizados min-max por município.
- **Casos:** exclusão por lista (*listwise*) — 87.545 setores completos nas 7 variáveis, contra 104.108 do recorte. A perda é quase toda do sigilo do analfabetismo, e a §6 trata do viés que ela introduz.

Todas as tabelas geradas estão em `banco_de_dados/eda/fatorial/`.

### 3.2 Estágio 1 — a base é adequada

| Critério do artigo | Patamar | Resultado (7 componentes, Spearman) | Veredito |
|---|---|---|---|
| Nível de mensuração | Contínuas ou discretas | Todas contínuas (proporções, razão, renda em R$) | ✅ |
| Tamanho da amostra | ≥ 100 | 87.545 setores | ✅ |
| Razão casos/variáveis | ≥ 5:1 | 12.506:1 | ✅ |
| Correlações acima de 0,30 | "a maior parte" | 57,1% dos coeficientes | ✅ no limite |
| KMO | ≥ 0,50 (Hair) / ≥ 0,60 (Pallant) | **0,783** — "mediano" na escala de Friel | ✅ |
| MSA individual | ≥ 0,50 | mínimo de 0,700 (lixo) | ✅ |
| BTS | p < 0,05 | χ² = 235.084 · 21 g.l. · p < 0,001 | ✅ (ver ressalva na §6.1) |

Com **Pearson** em vez de Spearman a base passa por menos: KMO cai para 0,732, apenas 33,3% dos coeficientes chegam a 0,30, o MSA mínimo cai para 0,542 e o critério de Kaiser passa a indicar três fatores. A distância entre os dois resultados é a medida do quanto as distribuições fogem da normalidade — assimetria de 3,42 na água e de 3,74 na renda, curtose de 49,5 na renda. A escolha por Spearman, já registrada no relatório da EDA, se confirma; e o custo dessa escolha está discutido na §6.2.

### 3.3 Estágio 2 — quantos fatores

Autovalores das 7 variáveis (Spearman), com a análise paralela de Horn:

| Componente | Autovalor | % variância | % acumulado | Autovalor aleatório (Horn) |
|---|---:|---:|---:|---:|
| 1 | 3,300 | 47,1 | 47,1 | 1,026 |
| 2 | 1,049 | 15,0 | **62,1** | 1,016 |
| 3 | 0,958 | 13,7 | 75,8 | 1,008 |
| 4 | 0,620 | 8,9 | 84,7 | 1,001 |
| 5 | 0,554 | 7,9 | 92,6 | 0,993 |
| 6 | 0,348 | 5,0 | 97,5 | 0,985 |
| 7 | 0,172 | 2,5 | 100,0 | 0,973 |

Os três critérios convergem para **dois fatores**: Kaiser (dois autovalores acima de 1), Horn (os mesmos dois superam o aleatório) e variância acumulada (62,1%, acima do patamar de 60% de Hair et al.). Vale notar quanto isso é apertado: o segundo autovalor é 1,049 e o terceiro, 0,958. A regra de Kaiser está decidindo com folga de 0,09 — e o próprio artigo adverte que ela funciona melhor entre 20 e 50 variáveis, não com 7. É mais uma razão para o critério teórico pesar na decisão.

### 3.4 Estágio 3 — as cargas rotacionadas

Solução Varimax com dois fatores, 7 variáveis. **Sinais ajustados para que carga positiva signifique maior vulnerabilidade** (o sinal do autovetor é arbitrário):

| Variável | Fator 1 | Fator 2 | Comunalidade | MSA |
|---|---:|---:|---:|---:|
| Renda (invertida) | **0,858** | 0,153 | 0,759 | 0,724 |
| Cor/raça PPI | **0,835** | 0,169 | 0,725 | 0,782 |
| Analfabetismo 15+ | **0,822** | 0,071 | 0,681 | 0,819 |
| Razão de moradores | **0,678** | −0,373 | 0,599 | 0,857 |
| Esgoto inadequado | **0,634** | 0,261 | 0,470 | 0,834 |
| Água inadequada | **0,482** | 0,144 | **0,253** | 0,753 |
| Lixo inadequado | 0,118 | **0,919** | 0,859 | 0,700 |

Variância explicada após a rotação: 46,0% no Fator 1 e 16,1% no Fator 2.

O resultado é inequívoco e não é o que a teoria previa. O **Fator 1 não é "socioeconômico"** — é um fator geral de vulnerabilidade, que puxa junto renda, cor/raça, analfabetismo, densidade, esgoto e até a água. O **Fator 2 não é "saneamento"** — é o **lixo sozinho**. A segunda dimensão que o critério de Kaiser encontrou não é uma dimensão do construto: é uma variável que não pertence ao construto.

### 3.5 O que acontece quando o lixo sai

| Variável | Fator 1 | Fator 2 | Comunalidade | MSA |
|---|---:|---:|---:|---:|
| Renda (invertida) | **0,915** | 0,137 | 0,856 | 0,715 |
| Analfabetismo 15+ | **0,868** | 0,127 | 0,770 | 0,815 |
| Cor/raça PPI | **0,833** | 0,245 | 0,754 | 0,780 |
| Razão de moradores | **0,532** | 0,312 | **0,380** | 0,913 |
| Água inadequada | 0,087 | **0,903** | 0,822 | 0,745 |
| Esgoto inadequado | 0,392 | **0,679** | 0,615 | 0,850 |

Adequabilidade: KMO = 0,787 · BTS χ² = 225.320 (15 g.l., p < 0,001) · **80,0% dos coeficientes com |r| ≥ 0,30** · variância acumulada 70,0% com dois fatores.

Aqui a estrutura teórica aparece limpa: **Fator 1 socioeconômico** (renda, analfabetismo, cor/raça, densidade) e **Fator 2 de saneamento** (água e esgoto). Nenhuma variável viola a estrutura simples do artigo — nenhuma carrega acima de 0,40 nos dois fatores. E a variância acumulada sobe de 62,1% para 70,0% com **menos** variáveis: é o mesmo movimento que o artigo descreve no seu próprio exemplo, quando exclui duas variáveis e vai de 75,79% para 82,30%.

Uma ressalva honesta: nessa solução o **critério de Kaiser retém apenas um fator** — o segundo autovalor é 0,9585, logo abaixo de 1, e Horn concorda. A retenção do segundo fator passa a se apoiar na razão teórica, que o artigo admite explicitamente como critério na postura confirmatória (e ele mesmo faz isso: fixa dois fatores a priori e afrouxa o critério de variância acumulada). Isto tem de ser reportado como escolha, não escondido atrás de um número.

---

## 4. O que os resultados decidem

### 4.1 Decisão 2 do Guia — o indicador de lixo

A §6.2.10 do Guia mantém a caçamba de lixo (`V00398`) como destino inadequado por fidelidade ao `Cálculo IVS2012.docx`, registrando a ressalva de que o lixo é "a variável menos correlacionada com todas as demais" e a hipótese de que esteja capturando porte urbano.

A análise fatorial converte a ressalva em medida. O lixo não é apenas fraco: ele é **ortogonal ao construto**. Fica com 0,118 de carga no fator geral de vulnerabilidade e 0,919 num fator que é só dele. Nos termos do artigo: "como a análise fatorial depende do padrão de correlação entre as variáveis observadas, espera-se que variáveis estatisticamente independentes não contribuam para a construção de um fator comum".

Mantê-lo no índice com peso empírico significa dar peso a uma dimensão que não é vulnerabilidade. **Recomendação:** retirar o lixo do índice e reportá-lo como indicador descritivo, com a §6.2.10 reescrita para registrar que a fidelidade à metodologia-fonte foi mantida na *definição* do indicador, e que a exclusão do *índice* é resultado empírico documentado — não redesenho arbitrário.

### 4.2 A regra de comunalidade do artigo teria excluído a variável errada

Este é o achado metodologicamente mais interessante do exercício, e vale para a discussão do artigo na dissertação.

Na solução com 7 variáveis, a **água** aparece com comunalidade 0,253 — muito abaixo do piso de 0,50. A regra do artigo é direta: excluir e re-rodar. Se ela fosse aplicada mecanicamente, o índice perderia um dos dois componentes centrais do bloco de saneamento.

Mas a comunalidade da água é baixa por uma razão estrutural: com dois fatores retidos e o lixo monopolizando o segundo, **não sobra fator para a água carregar**. Retirado o lixo, a água salta de 0,253 para **0,822** e passa a ser a variável de maior carga do fator de saneamento.

A lição, e é uma crítica ao artigo: a comunalidade **não é uma propriedade da variável**, é uma propriedade da variável *dada a solução*. Aplicar o corte de 0,50 variável a variável, sem antes verificar se a solução está distorcida por outra variável, leva a excluir a vítima em vez do problema. A ordem correta é: diagnosticar a estrutura → remover o que é externo ao construto → só então avaliar comunalidades.

Feito isso, resta um caso legítimo: a **razão de moradores** cai para 0,380 na solução de 6 variáveis. Ela é a variável-ponte descrita na §9.1 do relatório da EDA e a única sobrevivente do bloco de densidade habitacional. Fica como decisão aberta — manter por razão teórica e reportar a comunalidade baixa, ou excluir e reduzir o índice a 5 componentes.

### 4.3 Decisão 1 do Guia — os pesos

Repartição do peso entre os dois fatores rotacionados, por soma dos quadrados das cargas:

| Solução | Dimensão socioeconômica | Dimensão saneamento |
|---|---:|---:|
| 6 componentes, sem lixo, indicadores brutos | **65,0%** | **35,0%** |
| 7 componentes, brutos (Fator 2 = lixo) | 74,0% | 26,0% |
| 6 componentes, sem lixo, min-max por município | 55,7% | 44,3% |
| **Referência IVS-BH 2012 (literatura)** | **~60%** | **~40%** |

A solução recomendada — 6 componentes, sem lixo — devolve **65/35** contra os **60/40** da literatura. Cinco pontos percentuais de diferença. Isso desarma a decisão nº 1 do Guia: não há escolha dramática entre peso empírico e peso teórico, porque os dois convergem. O caminho mais defensável é **usar os pesos empíricos e reportar a convergência com o IVS-BH como validação externa da estrutura** — é o argumento mais forte que o projeto pode fazer, e ele só existe porque os dois números foram calculados separadamente.

### 4.4 Uma decisão nova: a ordem entre o Notebook 03 e o Notebook 04

O plano prevê NB03 (normalização min-max por município) → NB04 (fatorial). A padronização min-max por município é uma transformação afim com **escala diferente para cada grupo** — logo, ela muda a matriz de correlação global. Não é uma questão de opinião; é medível:

| | Indicadores brutos | Min-max por município |
|---|---:|---:|
| KMO (7 componentes) | 0,783 | 0,720 |
| Coeficientes com \|r\| ≥ 0,30 | 57,1% | 42,9% |
| Fatores por Kaiser | 2 | 3 |
| Variância acumulada (2 fatores) | 62,1% | 56,5% |
| Comunalidade mínima | 0,253 | 0,091 |
| Peso socioeconômico / saneamento (sem lixo) | 65 / 35 | 56 / 44 |

Nos mesmos 87 mil setores, normalizar antes de fatorar piora todos os indicadores de adequabilidade e muda os pesos em nove pontos percentuais. A razão é conceitual: a normalização municipal **remove deliberadamente a variação entre municípios**, que é parte substancial da covariação que sustenta o fator geral. Isso é coerente com o objetivo intraurbano do projeto — mas significa que a fatorial passa a estimar a estrutura da vulnerabilidade *dentro* dos municípios, não a estrutura geral.

As duas opções são defensáveis; o que não é defensável é escolher sem saber que se está escolhendo. **Recomendação:** estimar a estrutura fatorial sobre os indicadores brutos (a covariação completa é o que identifica o construto), aplicar a normalização municipal na composição do índice, e registrar o teste acima como decisão na §6.2 do Guia.

### 4.5 Decisão 3 do Guia — o sigilo do analfabetismo

A exclusão por lista custa 16.563 setores (15,9% do recorte), e a §6.2.6 do Guia já documenta que esse sigilo **não é aleatório**: incide nos setores de melhor situação. A amostra de 87.545 casos é, portanto, enviesada para os setores mais vulneráveis.

O cenário sem o analfabetismo mede o tamanho do problema: com 104.093 setores e 6 variáveis, KMO = 0,707, dois fatores, 63,8% de variância acumulada, e o lixo de novo isolado (carga 0,935, comunalidade 0,880). **A estrutura não muda.** O viés de seleção afeta as magnitudes, não as conclusões — o que é um argumento útil para a seção de limitações do artigo científico.

---

## 5. Onde o artigo não alcança este projeto

O artigo é de 2010, foi escrito para ciência política e para amostras de dezenas ou centenas de casos. Três descompassos precisam ser declarados.

### 5.1 O Bartlett é vazio nesta escala

O BTS testa se a matriz de correlação é a identidade. Com 87.545 casos, qualquer correlação diferente de zero por uma fração desprezível produz significância. O χ² = 235.084 com 21 graus de liberdade não é evidência de estrutura forte: é evidência de amostra grande. O artigo apresenta o BTS como um dos dois testes de adequabilidade sem qualquer ressalva sobre sensibilidade ao *n* — porque na amostra dele, de 127 casos, o teste de fato informa.

**Como reportar:** citar o BTS por convenção, mas apoiar a conclusão de adequabilidade no **KMO e nos MSA individuais**, que não crescem com o *n*.

### 5.2 ACP sobre matriz de Spearman é ACP de postos

Toda a análise aqui usa Spearman, seguindo o relatório da EDA e a evidência de não-normalidade. É defensável, e a comparação com Pearson na §3.2 mostra o que se ganha. Mas é preciso ser exato sobre o que se está fazendo: decompor uma matriz de Spearman equivale a rodar a ACP sobre os **postos** das variáveis, não sobre elas. As cargas se referem a posições relativas, não a magnitudes; e os escores fatoriais dela derivados herdam essa natureza ordinal. O artigo trabalha só com Pearson e não discute a alternativa.

**Como reportar:** declarar a ACP como sendo sobre a matriz de Spearman, justificar pela assimetria documentada (3,42 na água, 3,74 na renda, curtose 49,5) e apresentar a solução de Pearson como análise de sensibilidade — as tabelas já estão geradas.

### 5.3 O artigo mede um construto; o projeto precisa compor um índice

Este é o limite mais importante. O artigo termina nos escores fatoriais usados como **eixos de classificação** — o gráfico de quadrantes de contestação × inclusividade. O projeto precisa de outra coisa: um **índice composto**, numa escala 0–1, com pesos explícitos, categorizado em quatro faixas de risco e mapeável.

A análise fatorial entrega o insumo — a estrutura e a repartição do peso entre dimensões — mas não cobre as decisões que vêm depois: normalização (min-max, z-score, posto), forma de agregação (média aritmética ponderada, geométrica), tratamento de dados faltantes na composição e análise de sensibilidade dos pesos. Para isso a referência natural é o manual da OCDE/JRC de indicadores compostos (Nardo et al., 2008), somado ao que o próprio IVS-BH 2012 e o ISU de Passarelli-Araujo (2023) já resolveram nesse terreno.

### 5.4 Duas imprecisões do artigo que convém não reproduzir

**"Análise fatorial confirmatória" ali não é AFC.** O artigo chama de AFC o procedimento de fixar o número de fatores *a priori* e rodar ACP com Varimax. AFC no sentido técnico é um modelo de equações estruturais, com estrutura de cargas especificada e índices de ajuste (χ²/gl, CFI, RMSEA) — o próprio artigo remete a SEM numa nota de rodapé, sem estabelecer a distinção. Ao citar, o projeto deve dizer "ACP com número de fatores definido pela teoria", não "AFC".

**Unidade de análise.** As unidades aqui são setores censitários, não pessoas. Toda carga fatorial descreve a covariação **entre territórios**, e nada afirma sobre indivíduos. É a falácia ecológica que o Guia já se comprometeu a discutir com Lima-Costa & Barreto (2003), e ela se aplica integralmente à leitura das cargas.

---

## 6. Checklist operacional para o Notebook 04

Derivado do artigo, com o estado atual de cada item.

| # | Passo | Critério | Situação |
|---|---|---|---|
| 1 | Definir o recorte e a exclusão de casos | *listwise*, com o viés do sigilo declarado | ✅ testado (§4.5) |
| 2 | Escolher e justificar a matriz de correlação | Spearman, com Pearson como sensibilidade | ✅ decidido e medido |
| 3 | Verificar razão casos/variáveis | ≥ 5:1 | ✅ 12.506:1 |
| 4 | Proporção de \|r\| ≥ 0,30 | "a maior parte" | ✅ 57,1% / 80,0% sem lixo |
| 5 | KMO e MSA por variável | ≥ 0,50 | ✅ 0,783 e mínimo 0,700 |
| 6 | BTS | p < 0,05 | ✅ com a ressalva da §5.1 |
| 7 | Autovalores, Kaiser, scree, Horn | convergência entre critérios | ✅ 2 fatores |
| 8 | Variância acumulada | ≥ 60% | ✅ 62,1% / 70,0% sem lixo |
| 9 | Diagnosticar variável externa ao construto | fator próprio, correlações baixas | ✅ lixo identificado |
| 10 | Re-estimar sem ela e reavaliar comunalidades | ≥ 0,50 | ⚠️ pendente decidir a razão de moradores (0,380) |
| 11 | Rotação Varimax e estrutura simples | nenhuma carga > 0,40 em dois fatores | ✅ atendida sem o lixo |
| 12 | Definir os pesos e confrontar com a literatura | comparar com 60/40 do IVS-BH | ✅ 65/35 — convergem |
| 13 | Decidir a ordem NB03 → NB04 | registrar como decisão na §6.2 | 🔴 pendente (§4.4) |
| 14 | Gerar escores e compor o índice | fora do escopo do artigo | 🔴 pendente — ver §5.3 |
| 15 | Categorizar em 4 faixas e validar contra os setores de FCU | validação externa | 🔴 pendente (NB05) |

O item 15 merece uma nota: o projeto tem uma oportunidade de validação que o artigo não tinha. Os 19.452 setores de Favela e Comunidade Urbana identificados por `CD_TIPO = 1` são um marcador **externo** de vulnerabilidade, validado setor a setor contra a lista oficial do IBGE com 100% de concordância (§6.2.8 do Guia). Um IVS bem construído deve separar esses setores dos demais — e isso é um teste de validade de critério, mais forte do que qualquer estatística interna à fatorial.

---

## 7. Reprodutibilidade

Tudo que este documento afirma sobre os dados vem de um script versionado, pela mesma exigência que o projeto se impôs ao resolver o problema dos "CSVs órfãos" (item 12 da §9 do Guia).

```
scripts/diagnostico_fatorial.py           gera todas as tabelas abaixo
banco_de_dados/eda/fatorial/
  resumo_adequabilidade.csv               um cenário por linha: n, KMO, BTS, fatores, variância
  ivs7_spearman_{correlacao,autovalores,cargas}.csv
  ivs7_pearson_{correlacao,autovalores,cargas}.csv
  ivs6_sem_lixo_spearman_{...}.csv
  ivs6_sem_analfab_spearman_{...}.csv
  ivs7_minmax_municipal_spearman_{...}.csv
  ivs6_sem_lixo_minmax_municipal_spearman_{...}.csv
```

Rodar com: `python scripts/diagnostico_fatorial.py`

O script é **diagnóstico**, não o cálculo do IVS: ele opera sobre os indicadores brutos, antes da padronização do Notebook 03 e da definição de pesos do Notebook 04. O que ele produz alimenta essas duas etapas.

---

## Referências

FIGUEIREDO FILHO, D. B.; SILVA JÚNIOR, J. A. Visão além do alcance: uma introdução à análise fatorial. **Opinião Pública**, Campinas, v. 16, n. 1, p. 160–185, jun. 2010.

DAHL, R. **Poliarquia**: participação e oposição. São Paulo: Edusp, 1971.

HAIR, J. F. et al. **Multivariate Data Analysis**. 6. ed. Upper Saddle River: Pearson Prentice Hall, 2006.

TABACHNICK, B. G.; FIDELL, L. S. **Using Multivariate Statistics**. 5. ed. Boston: Allyn & Bacon, 2007.

HORN, J. L. A rationale and test for the number of factors in factor analysis. **Psychometrika**, v. 30, p. 179–185, 1965.

NARDO, M. et al. **Handbook on Constructing Composite Indicators**: methodology and user guide. Paris: OECD/JRC, 2008.

SECRETARIA MUNICIPAL DE SAÚDE DE BELO HORIZONTE. **Índice de Vulnerabilidade à Saúde 2012**. Belo Horizonte: SMS-BH, 2013.

PASSARELLI-ARAUJO, H. Índice de Saúde Urbana aplicado a capitais brasileiras, 2023. *(referência citada na §3 do `GUIA_DO_PROJETO.md`; conferir os dados bibliográficos completos antes de citar no artigo.)*

LIMA-COSTA, M. F.; BARRETO, S. M. Tipos de estudos epidemiológicos: conceitos básicos e aplicações na área do envelhecimento. **Epidemiologia e Serviços de Saúde**, v. 12, n. 4, p. 189–201, 2003.

IBGE. **Censo Demográfico 2022**: Favelas e Comunidades Urbanas — resultados do universo. Rio de Janeiro: IBGE, 2024.

---

*Documentos do projeto citados: `GUIA_DO_PROJETO.md` (§6.2.6, §6.2.8, §6.2.10, §6.3, §8) · `docs/Relatorio_EDA_Fase3_IVS_ELSI.md` (§9, §13, §15) · `src/ivs_censo/indicadores.py`.*
