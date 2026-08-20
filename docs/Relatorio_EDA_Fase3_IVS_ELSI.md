# Relatório de Análise Exploratória de Dados (EDA)

## IVS intraurbano — Censo Demográfico 2022 / ELSI-Brasil

> **Documento:** relatório técnico-interpretativo da análise exploratória da Fase 3.
> **Pipeline:** [`notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb`](../notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb)
> **Insumos:** CSVs e figuras em [`banco_de_dados/eda/`](../banco_de_dados/eda/)
> **Data:** 9 de agosto de 2026 (reescrito sobre o recorte urbano)
> **Pesquisador:** Pedro Dias Soares — IC Fiocruz Minas / IRR

**O que mudou nesta versão.** A anterior, de 12/06/2026, descrevia 106.281 setores
elegíveis com os rurais incluídos. Esta descreve o **recorte urbano de 104.108 setores**,
incorpora a correção da regra de elegibilidade e acrescenta os blocos descritivos criados
para atender às demandas de julho: envelhecimento populacional, tipo de domicílio e
setores de favela. Todos os números aqui foram lidos dos CSVs da execução de 09/08/2026.

**A seção 12 é nova e tem propósito distinto do resto.** Enquanto as demais seções
apresentam *resultados*, ela documenta o *caminho*: para cada demanda de julho, o que foi
pedido, por que decidi como decidi — incluindo as alternativas descartadas —, o passo a
passo da execução e o que verifiquei antes de aceitar cada número. Serve para que qualquer
decisão possa ser auditada ou revertida sem depender da minha memória, e alimenta
diretamente a seção de métodos do artigo.

---

## Sumário Executivo

A base analisada reúne **104.108 setores censitários urbanos** dos 70 municípios da
amostra do ELSI-Brasil, com 52,1 milhões de residentes. Sobre eles calculei as sete
variáveis-componente do IVS e mais dezesseis indicadores descritivos.

**Cinco conclusões que orientam a próxima etapa:**

1. **As três variáveis de saneamento têm mediana zero.** Em mais da metade dos setores
   urbanos, água, esgoto e lixo estão integralmente adequados. As distribuições são
   infladas de zeros, com coeficientes de variação entre 218% e 284%. Isso invalida a
   regra do IQR para detectar outliers nessas variáveis e condiciona a escolha do método
   de normalização.

2. **A renda é fortemente assimétrica** (média R$ 4.187, mediana R$ 2.572, máximo
   R$ 170.418; assimetria 3,74 e curtose 49,5). A normalização min-max global comprime
   quase todos os setores num canto da escala e precisa ser substituída por normalização
   por município.

3. **O analfabetismo tem 15,9% de dados faltantes, de forma não aleatória.** O sigilo do
   IBGE incide justamente onde a contagem absoluta de analfabetos é pequena, ou seja, nos
   setores de menor vulnerabilidade educacional. Imputar zero enviesaria o índice.

4. **Renda, cor/raça e analfabetismo são fortemente colineares** (Spearman de −0,81 e
   −0,76 com a renda). A análise fatorial provavelmente extrairá um fator socioeconômico
   dominante carregado por essas três variáveis.

5. **O lixo inadequado se comporta de forma independente das demais** (correlações de
   0,10 a 0,20, e −0,06 com a razão de moradores) e é a única variável em que o recorte
   ELSI está pior que o Brasil urbano. Há indício de que ele esteja capturando porte
   urbano em vez de vulnerabilidade.

**Validação externa da pipeline.** Aplicando as mesmas fórmulas aos 468.099 setores do
país, o índice de envelhecimento agregado resultou em **79,99** contra os **80,0**
publicados pelo IBGE, e a população somou **203.080.756**, o número oficial do Censo 2022.

---

## 1. Introdução

Esta EDA antecede a construção do índice. Seu objetivo não é medir vulnerabilidade, e sim
responder a três perguntas que determinam como o índice poderá ser construído:

- **Qual a forma das distribuições?** Define se a padronização min-max é adequada e se as
  variáveis precisam de transformação.
- **Onde faltam dados, e o padrão de ausência é aleatório?** Define a política de
  tratamento do sigilo no cálculo final.
- **As sete variáveis medem construtos distintos?** Define se a ponderação pode ser
  empírica (análise fatorial) e quantos fatores esperar.

O referencial de organização é o framework de EDA da FIOCRUZ (`docs/guia_analises.docx`):
medidas de tendência central e dispersão, gráficos de distribuição, análise de outliers,
análise de dados faltantes e estrutura de correlação.

---

## 2. Universo Amostral

| Região | Municípios | Setores na base | Rurais | % rural | Setores urbanos elegíveis |
|---|---:|---:|---:|---:|---:|
| Sudeste | 26 | 64.291 | 859 | 1,34% | 61.989 |
| Nordeste | 22 | 20.548 | 577 | 2,81% | 19.497 |
| Centro-Oeste | 7 | 10.186 | 544 | 5,34% | 9.490 |
| Sul | 9 | 7.486 | 167 | 2,23% | 7.217 |
| Norte | 6 | 6.521 | 460 | 7,05% | 5.915 |
| **Total** | **70** | **109.032** | **2.607** | **2,39%** | **104.108** |

O **Sudeste concentra 59% dos setores** da amostra. São Paulo sozinho responde por 27.301
setores e o Rio de Janeiro por 13.782. Qualquer média simples entre setores é, na prática,
dominada pelas grandes capitais do Sudeste — o que precisa ser considerado ao interpretar
os agregados do recorte.

---

## 3. Tratamento e Elegibilidade

### 3.1 Sigilo do IBGE

O IBGE substitui contagens muito pequenas pela letra `X`. A base bruta preserva o marcador;
a conversão para `NaN` ocorre no início do notebook de análise. Nas somas de numerador uso
`min_count=1`: o indicador só resulta ausente quando **todas** as parcelas estão sigilosas,
nunca zero silencioso.

### 3.2 Separador decimal

O rendimento médio (`V06004`) vem com vírgula decimal (`2453,03`). Sem a substituição por
ponto antes da conversão numérica, a coluna inteira se tornaria nula. O tratamento está na
célula `step2`.

### 3.3 Classificação `Dados_sig`

| Classe | Critério | Setores | % |
|---|---|---:|---:|
| ZERADO | `v0001 = 0` — setor sem população residente | 1.736 | 1,59% |
| SIGILOSO | `v0001` ou `V00001` suprimidos pelo IBGE | 1.015 | 0,93% |
| COLETIVO | `V00001 = 0` com população > 0 | 0 | — |
| **OK** | participa da análise | **106.281** | **97,48%** |

**Correção aplicada em 09/08/2026.** A condição de sigilo estava sendo avaliada antes da
condição de população zero. Com isso, 1.736 setores sem população — entre eles os 78 de
massa d'água (`CD_SIT = 9`) — eram rotulados `SIGILOSO`, isto é, contados como dado
suprimido pelo IBGE. Invertida a ordem, o sigilo real caiu de 2.751 para 1.015 setores.
Nenhum setor `OK` mudou de classe: a correção não altera o conjunto analisado, apenas
deixa de superestimar a supressão nos relatórios.

### 3.4 Recorte urbano

O IVS é um índice intraurbano. Setores rurais entram na base porque o recorte é municipal,
mas não pertencem ao objeto de análise. O filtro (`SITUACAO = 'Urbana'`, equivalente a
`CD_SIT ∈ {1, 2, 3}`) é aplicado no notebook de análise, e não na extração — a base bruta
preserva os 109.032 setores, o que torna a exclusão auditável e reversível.

| | Setores |
|---|---:|
| Base bruta dos 70 municípios | 109.032 |
| Elegíveis (`Dados_sig = OK`) | 106.281 |
| **Urbanos elegíveis — recorte de análise** | **104.108** |
| Excluídos pelo filtro rural | 2.173 (2,04%) |

**A exclusão é desigual entre municípios.** Nove municípios não perdem nenhum setor, mas
**29 dos 70 perdem mais de 10%** e **14 perdem mais da metade**. Os casos extremos são
São Raimundo do Doca Bezerra (19 setores elegíveis, 3 urbanos), Orizânia (21 → 5) e
São Paulo das Missões (18 → 6). Descritivas municipais nesses casos são instáveis, e a
adoção de um piso mínimo de setores para análises por município precisa ser decidida.
Conferência completa em `exclusao_rural_conferencia.csv`.

---

## 4. Análise por Variável

Descritivas globais dos sete componentes, sobre os 104.108 setores urbanos elegíveis:

| Indicador | n | Média | DP | Mediana | P75 | Máximo | CV % | Assimetria |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pct_agua_inad` | 104.108 | 0,0696 | 0,1974 | 0,0000 | 0,0118 | 1,0000 | 284 | 3,42 |
| `pct_esgoto_inad` | 104.107 | 0,0820 | 0,2143 | 0,0000 | 0,0182 | 1,0000 | 261 | 2,98 |
| `pct_lixo_inad` | 104.108 | 0,1158 | 0,2524 | 0,0000 | 0,0594 | 1,0000 | 218 | 2,38 |
| `razao_moradores` | 104.108 | 2,6909 | 0,3899 | 2,7126 | 2,9261 | 6,9135 | 14 | −0,22 |
| `pct_analfab` | 87.556 | 0,0364 | 0,0352 | 0,0271 | 0,0499 | 0,7255 | 97 | 2,34 |
| `renda_media` | 104.096 | 4.187,41 | 4.150,66 | 2.572,39 | 4.835,89 | 170.418,06 | 99 | 3,74 |
| `pct_raca_pretpardind` | 104.106 | 0,5267 | 0,2283 | 0,5719 | 0,7044 | 1,0000 | 43 | −0,39 |

Figura: `figuras/histogramas.png`.

### 4.1 Saneamento

**Água inadequada** (soma de `V00112`–`V00118` ÷ `V00001`). Média de 6,96% dos domicílios,
mediana zero, P75 de 1,18%. Um quarto dos setores tem alguma inadequação; a concentração
está no Norte, cuja média regional (0,323) é dezesseis vezes a do Sul (0,020). As piores
medianas municipais são Portel (0,919), Placas (0,832) e Ananindeua (0,825).

**Esgoto inadequado** (`V00312`–`V00316` ÷ `V00001`). Média de 8,20%, mediana zero. Piores
medianas municipais: Portel (0,980), Vicentinópolis (0,979), São Raimundo do Doca Bezerra
(0,971). A faixa de variáveis foi confirmada no dicionário oficial do IBGE — `V00309` a
`V00311` (rede geral e fossa séptica) são adequadas e ficam fora do numerador. O
diagnóstico empírico que compara esta faixa com a alternativa `V00249`–`V00253` está na
célula `step4b` e em `diagnostico_esgoto_312_vs_249.csv`.

**Lixo inadequado** (`V00398`–`V00402` ÷ `V00001`). Média de 11,58%, a maior das três, e
com o menor coeficiente de variação. É a única variável de saneamento cujo perfil regional
é praticamente plano: varia apenas de 0,091 (Centro-Oeste) a 0,154 (Nordeste). A pior
mediana municipal é Salto (0,964), seguida de Groaíras (0,720) e Salvador (0,340).

> **Sobre a caçamba.** A `V00398` (lixo depositado em caçamba de serviço de limpeza) conta
> como destino **inadequado**, seguindo o `Cálculo IVS2012.docx`, em que apenas a coleta
> porta a porta (`V00397`) é adequada. A decisão é herdada da metodologia-fonte, mas tem
> consequência empírica discutida na seção 11.

### 4.2 Razão de moradores por domicílio

`(V00005 + V00006) ÷ (V00001 + V00002)`, fórmula que reproduz o `V0005` publicado pelo
IBGE. É a variável mais bem comportada do conjunto: CV de 14%, distribuição aproximadamente
simétrica (assimetria −0,22), mínimo exatamente 1,00 e máximo 6,91. Média regional de 3,19
no Norte contra 2,53 no Sul. Maiores medianas municipais: Portel (4,23), Autazes (3,64) e
Coroaci (3,38). Os extremos foram auditados em `extremos_razao_moradores.csv`.

### 4.3 Analfabetismo de 15 anos ou mais

`V00901 ÷ (V00900 + V00901)`. Média de 3,64% e mediana de 2,71%, com máximo de 72,55%.
É a variável com maior perda de casos: **87.556 setores calculáveis de 104.108 (84,1%)**.
O padrão regional foge do gradiente Norte-Sul das demais: o pico é o Nordeste (0,062) e não
o Norte (0,033). Maiores medianas municipais: Arara (0,231), Água Preta (0,213) e Jaqueira
(0,191). O tratamento do sigilo está detalhado na seção 8.

### 4.4 Rendimento médio do responsável

`V06004`, usado diretamente. Média de R$ 4.187,41 e mediana de R$ 2.572,39 — a diferença
entre as duas já indica a assimetria. O máximo, R$ 170.418,06 num único setor, é
plausível: trata-se de rendimento médio dos responsáveis, e há setores de altíssima renda.
Extremos municipais: São Caetano do Sul (mediana R$ 5.292), Curitiba (R$ 4.115) e Porto
Alegre (R$ 3.987) no topo; Jaqueira (R$ 1.062), Água Preta (R$ 1.240) e Rosário (R$ 1.272)
na base — uma razão de cinco vezes entre os extremos.

### 4.5 Cor ou raça preta, parda e indígena

`(V01318 + V01320 + V01321) ÷ v0001`. Média de 52,67% e mediana de 57,19%, com a
distribuição mais espalhada do conjunto (é a única com assimetria negativa e nenhum outlier
pela regra do IQR). Extremos municipais: Salvador (0,889), Autazes (0,846) e Rosário
(0,838) no topo; Taió (0,160), Charqueadas (0,167) e São Caetano do Sul (0,172) na base.

---

## 5. Análise Regional

Médias entre setores, por região:

| Região | Água | Esgoto | Lixo | Moradores | Analfab. | Renda (R$) | PPI |
|---|---:|---:|---:|---:|---:|---:|---:|
| Norte | 0,323 | 0,238 | 0,098 | 3,194 | 0,033 | 2.881 | 0,748 |
| Nordeste | 0,118 | 0,162 | 0,154 | 2,771 | 0,062 | 3.008 | 0,713 |
| Centro-Oeste | 0,055 | 0,075 | 0,091 | 2,762 | 0,031 | 4.945 | 0,565 |
| Sudeste | 0,038 | 0,049 | 0,111 | 2,626 | 0,030 | 4.491 | 0,474 |
| Sul | 0,020 | 0,029 | 0,102 | 2,529 | 0,021 | 4.842 | 0,246 |

Figura: `figuras/boxplots_por_regiao.png`.

**Interpretação.** O gradiente Norte-Sul é consistente em cinco das sete variáveis: água
(16×), esgoto (8×), razão de moradores, renda e proporção PPI (3×). Duas variáveis fogem
do padrão, e as duas exceções são informativas:

- **O analfabetismo tem pico no Nordeste**, não no Norte. Reflete a história educacional
  das duas regiões e mostra que vulnerabilidade educacional e sanitária não são a mesma
  dimensão territorial.
- **O lixo é plano entre regiões.** Como a coleta porta a porta é quase universal nas
  áreas urbanas de todas as regiões, o que sobra no indicador é sobretudo a caçamba, que
  não segue o gradiente de desenvolvimento.

O Centro-Oeste apresentar a maior renda média (R$ 4.945) reflete o peso de Brasília na
composição regional da amostra, com 5.418 setores em sete municípios.

---

## 6. Heterogeneidade Municipal

As descritivas por município estão em `descritivas_por_municipio.csv` (70 municípios × 7
variáveis = 490 linhas). Três padrões se destacam:

**Os mesmos municípios lideram várias dimensões.** Portel aparece como pior mediana em água
e esgoto e maior razão de moradores; Arara e Água Preta lideram analfabetismo e estão entre
as menores rendas. Há um pequeno conjunto de municípios de alta vulnerabilidade em várias
dimensões ao mesmo tempo, o que é um bom sinal para a construção de um índice composto.

**A amplitude intermunicipal é grande.** A renda mediana varia cinco vezes entre o maior e
o menor município; a mediana de esgoto inadequado varia de praticamente zero a 0,98.

**Os municípios pequenos são instáveis após o recorte urbano.** Os casos com menos de dez
setores urbanos (São Raimundo do Doca Bezerra, Orizânia, São Paulo das Missões) produzem
medianas que oscilam muito com poucos setores. Nas tabelas por município, esses valores
devem ser lidos com reserva.

---

## 7. Análise de Outliers

| Indicador | P25 | P75 | Limite superior | Outliers pelo IQR | P95 | IQR informativo? |
|---|---:|---:|---:|---:|---:|:--|
| `pct_agua_inad` | 0,000 | 0,012 | 0,030 | 21.532 (20,7%) | 0,558 | **não** |
| `pct_esgoto_inad` | 0,000 | 0,018 | 0,045 | 20.901 (20,1%) | 0,693 | **não** |
| `pct_lixo_inad` | 0,000 | 0,059 | 0,149 | 19.124 (18,4%) | 0,846 | **não** |
| `razao_moradores` | 2,479 | 2,926 | 3,597 | 3.632 (3,5%) | 3,286 | sim |
| `pct_analfab` | 0,013 | 0,050 | 0,106 | 4.114 (4,7%) | 0,103 | sim |
| `renda_media` | 1.752 | 4.836 | 9.461 | 10.469 (10,1%) | 12.896 | sim |
| `pct_raca_pretpardind` | 0,353 | 0,704 | 1,232 | 0 (0,0%) | 0,846 | sim |

**A regra do IQR não é aplicável às três variáveis de saneamento.** Quando o primeiro
quartil e a mediana são ambos zero, o intervalo interquartil fica minúsculo e qualquer
valor positivo acima de um limiar de 3 a 15 pontos percentuais é classificado como outlier.
Os 18% a 21% de setores flagrados não são erros de medição nem casos extremos: são os
setores que simplesmente têm alguma inadequação, num universo em que a maioria não tem
nenhuma.

Por isso a tabela `outliers.csv` traz também as colunas `p95`, `n_acima_p95`,
`pct_acima_p95` e a sinalização `iqr_nao_informativo`. **Para essas três variáveis, o
percentil 95 é o critério apropriado de cauda alta.**

Nos demais indicadores o IQR funciona. Os 10,1% de outliers da renda são reais: refletem a
cauda de setores de alta renda, não erro de dado. A proporção PPI não tem nenhum outlier,
consequência de ser limitada em [0, 1] e ter distribuição espalhada.

---

## 8. Análise de Dados Faltantes

| Variável | Setores com valor | Cobertura |
|---|---:|---:|
| `pct_agua_inad` | 104.108 | 100,00% |
| `pct_lixo_inad` | 104.108 | 100,00% |
| `razao_moradores` | 104.108 | 100,00% |
| `pct_esgoto_inad` | 104.107 | 100,00% |
| `pct_raca_pretpardind` | 104.106 | 100,00% |
| `renda_media` | 104.096 | 99,99% |
| **`pct_analfab`** | **87.556** | **84,10%** |

Figura: `figuras/missing_por_municipio.png`.

**O problema está concentrado numa variável.** Seis das sete têm cobertura praticamente
total. O analfabetismo perde 15,9% dos setores porque o IBGE suprime a contagem de
analfabetos (`V00901`) quando ela é pequena.

Municípios mais afetados: Belo Horizonte (22,5%), Araçatuba (18,8%), Brasília (16,3%),
Ananindeua (9,7%), Belém (6,8%).

**O sigilo não é aleatório — é informativo.** Ele incide onde o número absoluto de
analfabetos é pequeno, isto é, nos setores urbanos de melhor situação educacional. Isso
significa que:

- **imputar zero enviesaria o índice**, subestimando o analfabetismo exatamente nas áreas
  de menor vulnerabilidade e comprimindo artificialmente a variabilidade do indicador;
- **descartar os setores** reduziria o conjunto analítico em 16% e o faria de forma
  seletiva, eliminando preferencialmente os setores de melhor situação.

Na EDA mantive os valores ausentes. Para o cálculo do índice a política precisa ser
definida explicitamente; a alternativa mais defensável é imputação por mediana municipal
com indicador de imputação, mas isso ainda não está decidido.

---

## 9. Estrutura de Correlações

Matriz de Spearman; a de Pearson está em `correlacao_pearson.csv`. Uso Spearman como
referência porque as distribuições estão longe da normalidade.

Figura: `figuras/matriz_correlacao.png`.

| | Água | Esgoto | Lixo | Moradores | Analfab. | Renda | PPI |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Água** | 1,00 | 0,42 | 0,10 | 0,26 | 0,23 | −0,26 | 0,35 |
| **Esgoto** | 0,42 | 1,00 | 0,20 | 0,35 | 0,43 | −0,45 | 0,43 |
| **Lixo** | 0,10 | 0,20 | 1,00 | −0,06 | 0,16 | −0,16 | 0,19 |
| **Moradores** | 0,26 | 0,35 | −0,06 | 1,00 | 0,41 | −0,44 | 0,46 |
| **Analfabetismo** | 0,23 | 0,43 | 0,16 | 0,41 | 1,00 | −0,76 | 0,63 |
| **Renda** | −0,26 | −0,45 | −0,16 | −0,44 | −0,76 | 1,00 | −0,81 |
| **PPI** | 0,35 | 0,43 | 0,19 | 0,46 | 0,63 | −0,81 | 1,00 |

### 9.1 Leitura

**Um bloco socioeconômico muito coeso.** Renda, cor/raça e analfabetismo formam um
triângulo de correlações fortes: −0,81, −0,76 e 0,63. As três medem, em boa parte, o mesmo
construto latente de posição social do território.

**Um bloco de saneamento moderado.** Água e esgoto se correlacionam a 0,42, e ambos se
ligam ao bloco socioeconômico com magnitudes entre 0,23 e 0,45. É uma dimensão distinta,
mas não ortogonal.

**O lixo isolado.** Correlaciona-se de 0,10 a 0,20 com todas as demais e −0,06 com a razão
de moradores. Não pertence claramente a nenhum dos dois blocos.

**A razão de moradores é intermediária**, com correlações de 0,26 a 0,46 com quase tudo —
comporta-se como variável de ligação entre as duas dimensões.

### 9.2 Implicações para a análise fatorial

- Esperar **dois fatores**, e não os dois blocos teóricos simetricamente: um fator
  socioeconômico forte (renda, PPI, analfabetismo, com a razão de moradores carregando
  parcialmente) e um fator de saneamento mais fraco (água e esgoto).
- **O lixo provavelmente ficará com comunalidade baixa** em ambos os fatores. Será
  preciso decidir se permanece no índice, se entra com peso reduzido ou se é reportado
  como indicador descritivo à parte.
- A colinearidade do bloco socioeconômico é o argumento técnico a favor de pesos
  empíricos: uma ponderação igual entre as sete variáveis daria à posição social três
  votos e ao saneamento dois e meio, sem que essa fosse uma escolha deliberada.

---

## 10. Blocos Descritivos Complementares

Estes indicadores não integram o IVS. Caracterizam o território e alimentam as tabelas
descritivas do artigo.

### 10.1 Habitação precária e banheiro

| Indicador | n | Média | P95 | P99 | Máximo |
|---|---:|---:|---:|---:|---:|
| `pct_dom_improv` | 98.969 | 0,00073 | 0,000 | 0,000 | 0,973 |
| `pct_hab_precaria` | 104.108 | 0,00654 | 0,026 | 0,165 | 1,000 |
| `pct_sem_banheiro` | 91.912 | 0,00235 | 0,000 | 0,055 | 1,000 |
| `pct_sem_banheiro_nem_sanitario` | 101.139 | 0,00016 | 0,000 | 0,000 | 0,667 |

São fenômenos raros no recorte urbano: as medianas e mesmo os percentis 90 são zero em
todos os quatro. A privação sanitária extrema praticamente desapareceu das cidades da
amostra, o que justifica mantê-los fora do índice — não discriminariam setores.

### 10.2 Pessoa responsável do sexo feminino

`V01063 ÷ (V01062 + V01063)`. Média de 52,81% e mediana de 53,39% (n = 103.961). Por
região: Nordeste 55,4%, Norte 54,2%, Sudeste 52,5%, Sul 51,3%, Centro-Oeste 49,8%. Na
maioria dos setores urbanos da amostra, portanto, as mulheres já são maioria entre as
pessoas responsáveis pelo domicílio.

### 10.3 Indicadores de envelhecimento

Definições do Quadro 1 de Galvão et al. (*Hygeia*, v.21, e2106, 2025), que adota os
indicadores das Nações Unidas.

| Indicador | Fórmula (× 100) | Valor no recorte |
|---|---|---:|
| IEP — Índice de Envelhecimento | 60+ ÷ menores de 15 anos | **92,7** |
| RDI — Razão de dependência de idosos | 60+ ÷ 15 a 59 anos | **25,5** |
| Percentual de 60 anos ou mais | 60+ ÷ população total | **16,65%** |
| Percentual de menores de 15 anos | — | 17,96% |

Por região: Sul 111,9 · Sudeste 105,5 · Nordeste 81,7 · Centro-Oeste 73,0 · Norte 56,3.
No Sul e no Sudeste da amostra já há mais idosos do que crianças.

**Correção do denominador.** A versão anterior calculava o índice como idosos ÷ crianças de
0 a 4 anos (`V01031`). O denominador correto é a população com menos de 15 anos
(`V01031 + V01032 + V01033`). Com o denominador antigo o índice ficava cerca de três vezes
maior e não era comparável com nenhuma referência publicada.

**A Longevidade (75+ ÷ 60+) não é calculável** nos agregados por setor: a faixa mais fina
no topo da pirâmide é `V01041` = "70 anos ou mais". Calculo a proporção de 70+ entre os
60+ (44,6% no recorte) como substituto parcial, explicitamente rotulado como tal.

### 10.4 Tipo de domicílio

| Grupo | Domicílios | % sobre `V00001` |
|---|---:|---:|
| Convencional (casa, vila/condomínio, apartamento) | 19.128.392 | 99,187% |
| Não convencional (cortiço, maloca, estrutura degradada) | 110.168 | 0,571% |
| Improvisado (DPIO) | 11.525 | 0,060% |

`pct_apartamento` = `V00049 ÷ V00001`: média de 31,5% entre setores, com gradiente Sul
39,0% · Sudeste 34,8% · Centro-Oeste 29,0% · Nordeste 23,8% · Norte 16,4%. Municípios mais
verticalizados: São Caetano do Sul (53,4%), Porto Alegre (52,4%), Rio de Janeiro (42,1%).

**Verificação do denominador.** A soma dos seis tipos de domicílio permanente nunca
ultrapassa `V00001` em nenhum dos 104 mil setores; quando fica abaixo, o déficit é de no
máximo seis domicílios e decorre de sigilo em parcelas pequenas. Isso confirma `V00001`
como denominador correto para o bloco.

### 10.5 Setores de favela e comunidade urbana

O Censo 2022 substituiu a categoria "aglomerado subnormal" pelas Favelas e Comunidades
Urbanas, marcadas em `CD_TIPO = 1`.

| | Valor |
|---|---:|
| Setores de FCU no recorte | **19.507 (17,9%)** |
| Favelas distintas (`CD_FCU`) | 5.903 |
| População residente em FCU | 10.071.575 |
| Domicílios em FCU | 3.443.687 |
| Municípios com pelo menos uma FCU | 42 de 70 |

Distribuição regional (percentual dos setores de cada região): Norte 50,6% · Nordeste
27,7% · Sudeste 14,6% · Sul 8,5% · Centro-Oeste 4,6%. É a maior heterogeneidade regional
de qualquer variável do projeto. Em Ananindeua 58,9% dos setores são de favela, em Belém
55,9% e em Manaus 51,7%.

**Comparação entre setores de FCU e demais setores urbanos elegíveis:**

| Indicador | Em FCU | Fora de FCU | Razão |
|---|---:|---:|---:|
| Esgoto inadequado | 0,214 | 0,052 | **4,14×** |
| Lixo inadequado | 0,248 | 0,085 | 2,90× |
| Analfabetismo | 0,062 | 0,029 | 2,14× |
| Água inadequada | 0,108 | 0,061 | 1,77× |
| Cor/raça PPI | 0,735 | 0,479 | 1,53× |
| Menores de 15 anos | 0,222 | 0,161 | 1,38× |
| Razão de moradores | 2,927 | 2,637 | 1,11× |
| Renda média | R$ 1.610 | R$ 4.780 | 0,34× |
| Apartamento | 0,033 | 0,377 | 0,09× |
| Índice de envelhecimento | 55,2 | 153,0 | 0,36× |

**Este é o resultado mais relevante da EDA para a validação do índice.** Os setores de FCU
são identificados por classificação independente, feita pelo próprio IBGE, e todos os
componentes do IVS se movem na direção esperada com magnitudes grandes. Quando o índice
estiver calculado, comparar sua distribuição entre FCU e não-FCU será o teste de validade
de critério mais direto disponível, sem depender de fonte externa.

---

## 11. Comparação com o Brasil

O script `scripts/proporcoes_brasil.py` aplica as mesmas fórmulas aos 468.099 setores do
país. Não é recorte de análise: serve de linha de base de representatividade.

| Métrica | Brasil | ELSI 70 | % |
|---|---:|---:|---:|
| Setores censitários | 468.099 | 109.032 | 23,3% |
| Setores urbanos elegíveis | 347.400 | 104.108 | 30,0% |
| Municípios | 5.572 | 70 | 1,3% |
| População | 203.080.756 | 52.732.704 | 26,0% |
| Domicílios | 72.438.953 | 19.458.006 | 26,9% |
| Setores de favela | 33.272 | 19.507 | **58,6%** |

| Indicador (razão agregada) | Brasil urbano | ELSI 70 | Razão |
|---|---:|---:|---:|
| Esgoto inadequado | 0,155 | 0,080 | 0,52× |
| Analfabetismo | 0,058 | 0,036 | 0,62× |
| Água inadequada | 0,083 | 0,069 | 0,83× |
| Razão de moradores | 2,762 | 2,695 | 0,98× |
| Cor/raça PPI | 0,544 | 0,551 | 1,01× |
| Renda média | R$ 3.209 | R$ 4.187 | 1,31× |
| **Lixo inadequado** | **0,094** | **0,114** | **1,21×** |

A amostra é mais rica, mais alfabetizada e mais bem servida de esgoto que o Brasil urbano —
o esperado numa amostra de capitais e cidades médias. **Ela deve ser descrita no artigo
como representativa do Brasil urbano de grande porte, não do Brasil.**

**A exceção é o lixo**, única variável em que o recorte está pior que o país. A hipótese
mais provável é a caçamba (`V00398`), que conta como destino inadequado e é muito mais
comum em cidade grande do que em município pequeno. Se confirmada, significa que o
indicador de lixo captura parcialmente **porte urbano** em vez de vulnerabilidade — o que
é coerente com ele ser também o menos correlacionado com todas as demais variáveis.
Recomendo decompor `V00398` das demais formas antes de fechar a ponderação do índice.

---

## 12. Memória das decisões: como cada demanda foi atendida

Esta seção registra o caminho, não só o resultado. Para cada demanda de julho documento
**o que foi pedido**, **por que decidi como decidi** (incluindo as alternativas que
descartei), **o passo a passo da execução** e **o que verifiquei antes de aceitar o
número**. O objetivo é que qualquer decisão possa ser auditada — ou revertida — sem
depender da minha memória.

### 12.1 Os três princípios que segui

Antes das demandas propriamente ditas, vale explicitar as regras que usei para decidir
quando havia mais de um caminho possível:

**1. A metodologia-fonte manda.** Quando o `Cálculo IVS2012.docx` define alguma coisa —
quais formas de saneamento são inadequadas, qual o denominador, como classificar setores
inelegíveis — eu reproduzo, mesmo quando o resultado é contraintuitivo. O projeto se
propõe a *replicar* o IVS-BH no Censo 2022, não a redesenhá-lo. O caso mais visível é a
caçamba de lixo (§12.9).

**2. Quando o Censo 2022 não permite reproduzir, documento a substituição.** Três
componentes do IVS-BH original não existem nos agregados por setor. Nesses casos escolho o
substituto mais próximo e **declaro a limitação**, em vez de improvisar um cálculo que
pareça equivalente. O mesmo vale para o índice de Longevidade, que simplesmente não é
calculável (§12.2).

**3. Toda escolha que muda um número precisa de verificação empírica.** Nenhuma decisão
metodológica entrou sem um teste que a sustente: o denominador foi validado por nenhuma
proporção ultrapassar 1,0; as faixas etárias, pela soma reproduzir a população; o cálculo
nacional, por reproduzir números publicados pelo IBGE. Onde não consegui verificar,
digo isso explicitamente.

---

### 12.2 Demanda 1 — Ajustar o índice de envelhecimento

**O que foi pedido.** *"Ajustar índice de envelhecimento (ler artigo)"*, com o artigo de
Galvão et al. (*Hygeia*, v.21, e2106, 2025) anexado.

**O diagnóstico.** A versão anterior da seção etária calculava o índice como
**idosos de 60+ divididos por crianças de 0 a 4 anos** (`V01031`). Isso não corresponde a
nenhuma definição publicada. O Quadro 1 do artigo define o Índice de Envelhecimento
Populacional como **60 anos ou mais sobre a população com menos de 15 anos** — que são
três faixas somadas, e não uma.

**Por que a correção importa e não é cosmética.** Com o denominador antigo, o índice ficava
cerca de três vezes maior que o publicado, e **incomparável com qualquer referência**: não
dava para confrontar com o IEP do Brasil, nem com o de outros estudos, nem com os valores
regionais do próprio artigo. Um índice que não pode ser comparado com nada não sustenta
argumento nenhum no artigo.

**Alternativas que descartei:**

- *Manter 0–4 e renomear o indicador* para algo como "razão idosos/primeira infância".
  Descartado: perderia a comparabilidade, que é justamente o que dá valor ao indicador.
- *Usar o corte de 65 anos*, mais comum na literatura internacional. **Impossível:** o IBGE
  agrega a faixa como "60 a 69 anos" (`V01040`), sem separar 65. Por isso todos os
  indicadores do projeto usam 60+.

**Como fiz, passo a passo:**

1. Li o artigo e extraí o Quadro 1, com as quatro definições: IEP, RDI, LI e percentual de
   60 anos ou mais.
2. Conferi no dicionário oficial do IBGE quais faixas etárias existem nos agregados por
   setor. Descobri que o bloco vai de `V01031` (0–4) até `V01041` (70 ou mais).
3. Descobri que **as faixas de 15 a 59 anos (`V01034`–`V01039`) não estavam sendo lidas**
   pela pipeline — o Notebook 01 só extraía 0–4, 5–9, 10–14, 60–69 e 70+. Sem elas, a
   Razão de Dependência de Idosos seria impossível.
4. Editei o `usecols` do bloco `demog` no Notebook 01 e reprocessei a base inteira. A base
   passou de 58 para 68 colunas.
5. Reescrevi a célula `idade-estrutura` do Notebook 02 com as três definições viáveis.
6. Calculei cada indicador de **duas formas** (ver abaixo o porquê).
7. Rodei o cálculo nacional para validar contra o número publicado.

**Por que calculo agregado e por setor.** São coisas diferentes e as duas são necessárias:

- O **agregado** (razão das somas do grupo) é o número comparável com o que o IBGE publica
  para municípios, regiões e Brasil. É o que vai para as tabelas do artigo.
- O **por setor** (razão dentro de cada setor, depois descritivas) é o que mostra a
  variação *intraurbana*, que é o objeto do projeto. Setores sem crianças ficam ausentes,
  não zero — dividir por zero não é zero.

**O que verifiquei:**

- A soma das 11 faixas etárias reproduz exatamente `v0001` em todos os **99.957 setores
  comparáveis** (aqueles sem sigilo dos dois lados). Isso valida que as faixas foram lidas
  corretamente e que nenhuma ficou faltando.
- O IEP agregado do Brasil deu **79,99** contra os **80,0** publicados pelo IBGE.
- Por região, o padrão se mantém: Norte 42,9 (publicado 41,4), Sudeste 97,1 (98,0), Sul
  91,5 (95,4). As diferenças são coerentes com o meu recorte ser urbano e o publicado
  incluir rurais.

**O que ficou impossível.** O índice de **Longevidade (75+ ÷ 60+) não é calculável** nos
agregados por setor: a faixa mais fina no topo da pirâmide é "70 anos ou mais". Calculei a
proporção de 70+ entre os 60+ (44,6% no recorte) como substituto parcial, **rotulado
explicitamente como não sendo o LI** — não pode ser comparado com valores de LI publicados.

---

### 12.3 Demanda 2 — Tabela de variáveis com o significado e a fonte

**O que foi pedido.** *"Ajustar tabela para mostrar o que significa cada variável e a fonte
da planilha do censo"*.

**Por que a escolha da fonte das descrições.** Optei por usar **os dicionários oficiais do
IBGE** como fonte das descrições, e não redigir descrições próprias. Motivo: descrição
escrita por mim é interpretação, e interpretação em tabela de metodologia vira fonte de
divergência com o revisor. Onde o IBGE descreve, uso a palavra dele.

**O problema que isso criou, e como resolvi.** Dez colunas do projeto **não constam de
nenhum dicionário oficial**: são as de identificação e classificação territorial
(`CD_SETOR`, `SITUACAO`, `CD_SIT`, `CD_TIPO`, `CD_FCU`, `NM_FCU`, além das derivadas
`CD_UF` e `CD_MUN`). Para essas escrevi a descrição, mas acrescentei uma coluna
**`origem_da_descricao`** que separa o que é texto do IBGE do que é texto do projeto.
Quem ler a tabela sabe exatamente de onde veio cada linha.

**Como fiz:**

1. Criei `src/ivs_censo/fontes.py` como **fonte única de verdade** sobre procedência: para
   cada um dos 8 arquivos do Censo, qual o nome da chave do setor naquele arquivo (o IBGE
   alterna entre `CD_SETOR`, `CD_setor` e `setor`) e quais variáveis o projeto lê dele.
2. Criei `src/ivs_censo/dicionario.py`, que lê as três abas relevantes dos dois dicionários
   oficiais e cruza com o mapa de procedência.
3. Acrescentei a coluna `usada_nos_indicadores`, derivada automaticamente das definições
   dos indicadores — assim ela nunca fica dessincronizada das fórmulas.
4. `scripts/gerar_tabela_variaveis.py` gera CSV e XLSX (este com uma aba por arquivo do
   Censo), e a mesma tabela é embutida na tabela `dicionario_variaveis` dos bancos SQLite
   da entrega.

**Resultado e verificação.** São **67 variáveis** de **8 arquivos**; 57 descrições vêm do
dicionário oficial e 10 da documentação do projeto. Um teste automatizado confere que toda
variável usada em algum indicador aparece na tabela.

---

### 12.4 Demanda 3 — Excluir setores rurais

**O que foi pedido.** *"Excluir setores rurais, conferir com a porcentagem"*.

**Por que excluir.** O IVS é um índice **intraurbano**: ele compara setores dentro de uma
mesma cidade. Setores rurais entram na base porque o recorte da amostra é municipal — o
município inteiro dos 70 do ELSI —, mas não pertencem ao objeto. Eles têm padrões de
saneamento estruturalmente diferentes (fossa e poço são a norma, não a exceção) e, se
mantidos, puxariam artificialmente a cauda alta de vulnerabilidade, fazendo o índice medir
em parte a diferença campo-cidade em vez da desigualdade dentro da cidade.

**A decisão mais importante: onde aplicar o filtro.** Apliquei no **notebook de análise, e
não na extração**. A base bruta continua com os 109.032 setores. As razões:

- **Auditabilidade.** Com a base completa preservada, dá para mostrar exatamente quanto e
  quem saiu — que é justamente a "conferência com a porcentagem" pedida.
- **Reversibilidade.** Se a decisão mudar, ou se alguém quiser uma análise comparando
  urbano e rural, basta não aplicar o filtro. Não é preciso reprocessar 2,4 GB.
- **Rastreabilidade do dado bruto.** A base bruta continua sendo um retrato fiel do que o
  IBGE publica para aqueles municípios, sem recorte analítico embutido.

**Como fiz:**

1. Verifiquei a equivalência entre `SITUACAO` e `CD_SIT` nos 468.099 setores do país, para
   ter certeza de que o critério era estável: `CD_SIT` 1, 2 e 3 correspondem a Urbana
   (354.965 setores) e 5 a 8 a Rural (112.031), sem nenhuma exceção.
2. Investiguei os setores com `SITUACAO` vazia: são `CD_SIT = 9` e **todos os 1.101 do
   país têm população zero**. São massas d'água. No recorte ELSI são 78, e já saem pela
   regra de elegibilidade, antes do filtro urbano.
3. Criei a seção 3b do Notebook 02, que monta as tabelas de composição por município e
   região, aplica o filtro e exporta a conferência.
4. Exportei quatro tabelas, incluindo `exclusao_rural_conferencia.csv`, que mostra por
   município quantos setores entraram e quantos saíram.

**O que a conferência revelou — e que eu não esperava.** A exclusão remove só 2,04% dos
setores no agregado, mas é **muito desigual**: nove municípios não perdem nada, **29 dos
70 perdem mais de 10%** e **14 perdem mais da metade**. São Raimundo do Doca Bezerra fica
com 3 setores urbanos, de 19 elegíveis. Isso tem consequência direta: médias e medianas
municipais desses casos são instáveis, e é preciso decidir um piso mínimo de setores para
incluir um município nas análises municipais. Sem a tabela de conferência, esse efeito
teria passado despercebido.

---

### 12.5 Demanda 4 — Agrupar as moradias convencionais

**O que foi pedido.** *"Agrupar variáveis como moradias normais no tipo do domicílio"*.

**Como decidi o agrupamento.** O Censo 2022 desdobra o tipo de espécie do domicílio em 12
variáveis: seis para os Domicílios Particulares Permanentes Ocupados (`V00047`–`V00052`) e
seis para os Improvisados (`V00053`–`V00058`). Agrupei em três blocos:

- **Convencional:** casa, casa de vila ou em condomínio, apartamento (`V00047`–`V00049`).
- **Não convencional:** cortiço ou casa de cômodos, maloca indígena, estrutura residencial
  permanente degradada ou inacabada (`V00050`–`V00052`).
- **Improvisado:** os seis tipos de DPIO (`V00053`–`V00058`).

O critério do corte é a **adequação da edificação como moradia**, que é o que interessa a
um índice de vulnerabilidade — e não a tipologia arquitetônica. Casa e apartamento são
formas convencionais de morar; cortiço e estrutura degradada não são.

**Por que o denominador é `V00001` — e como verifiquei.** Os seis tipos de DPPO são,
por definição, um desdobramento do total de DPPO. Mas definição no papel não basta: testei
nos 104.108 setores. A soma dos seis tipos **nunca ultrapassa `V00001` em nenhum setor**;
quando fica abaixo, o déficit é de **no máximo 6 domicílios** e decorre de sigilo em
parcelas pequenas. Se a soma tivesse estourado o denominador em algum setor, isso indicaria
erro de interpretação das variáveis — não estourou.

**Resultado.** Convencional 99,187% dos domicílios, não convencional 0,571%, improvisado
0,060%. Criei também uma versão agrupada da classificação categórica de moradia
predominante, com as mesmas três classes.

---

### 12.6 Demanda 5 — Criar um indicador de apartamento

**O que foi pedido.** *"Criar um indicador de apartamento"*.

**A fórmula e por quê.** `pct_apartamento = V00049 ÷ V00001`. O denominador é o mesmo do
bloco de tipo de domicílio, pela razão verificada em §12.5.

**A decisão de não incluí-lo no IVS.** Este é um indicador **descritivo de morfologia
urbana**, e o mantive fora dos sete componentes do índice deliberadamente. O motivo é que
**ele não tem direção de vulnerabilidade definida**: verticalização aparece tanto em área
central de alta renda quanto em conjunto habitacional popular. Um componente de índice
composto precisa ter direção inequívoca — "mais é pior" ou "mais é melhor" —, e este não
tem. Ele serve para *caracterizar* o território, não para *pontuá-lo*.

**Resultado.** Média de 31,5% entre setores, com gradiente claro: Sul 39,0%, Sudeste 34,8%,
Centro-Oeste 29,0%, Nordeste 23,8%, Norte 16,4%. Municípios mais verticalizados: São
Caetano do Sul (53,4%), Porto Alegre (52,4%), Rio de Janeiro (42,1%).

---

### 12.7 Demanda 6 — Quantos setores são de vilas e favelas

**O que foi pedido.** *"Dentro do ELSI, quantos setores são de vilas e favelas"*.

**O obstáculo inicial.** A pergunta parecia simples, mas a informação **não estava na
base**: o Notebook 01 lia apenas cinco colunas do arquivo básico e nenhuma delas
identificava favelas. Foi preciso voltar à extração.

**Por que `CD_TIPO = 1` e não o nome da favela.** O Censo 2022 substituiu a categoria
"aglomerado subnormal" pelas **Favelas e Comunidades Urbanas**, e traz três colunas
relacionadas: `CD_TIPO` (classificação do tipo de setor), `CD_FCU` e `NM_FCU` (código e
nome da FCU). Havia dois critérios possíveis: usar `CD_TIPO = 1` ou usar "tem `NM_FCU`
preenchido".

Testei os dois nos **468.099 setores do país** e eles coincidem exatamente: 33.272 setores
pelos dois critérios. Adotei `CD_TIPO = 1` por ser o **campo oficial de classificação**
do setor, enquanto o nome é um atributo descritivo. No recorte ELSI aparecem **25 setores**
com nome de FCU preenchido mas `CD_TIPO ≠ 1`; a célula os isola e quantifica, e eles seguem
o critério oficial (ficam de fora).

**Como fiz:**

1. Inspecionei o cabeçalho do arquivo básico e descobri que `CD_SIT`, `CD_TIPO`, `CD_FCU` e
   `NM_FCU` estavam lá desde sempre, apenas não eram lidas.
2. Acrescentei as quatro ao `usecols` do Notebook 01 (junto com as faixas etárias da
   demanda 1, para reprocessar uma vez só).
3. Marquei as quatro como colunas de **texto** no Notebook 02 — são códigos de
   classificação, não contagens; se fossem convertidas para número, `CD_TIPO = 0` viraria
   zero numérico e perderia o sentido de categoria.
4. Reprocessei a base e criei a seção 7g do Notebook 02.
5. Além da contagem pedida, acrescentei a comparação de todos os indicadores entre setores
   de FCU e os demais.

**Por que fui além da contagem.** A pergunta pedia um número, mas os setores de FCU são
identificados por uma **classificação independente, feita pelo próprio IBGE**. Isso os
torna um padrão-ouro disponível de graça: se o índice funciona, ele tem que ser mais alto
em favela. Comparar os componentes entre os dois grupos é, portanto, uma **validação de
critério** — e é o teste mais direto que teremos quando o IVS estiver calculado.

**Resultado.** 19.507 setores de FCU no recorte (17,9%), em 5.903 favelas distintas, com
10,07 milhões de residentes, presentes em 42 dos 70 municípios. Todos os componentes se
movem na direção esperada: esgoto inadequado 4,14× maior, lixo 2,90×, analfabetismo 2,14×,
e renda a um terço.

---

### 12.8 Demanda 7 — Proporções para o Brasil todo

**O que foi pedido.** *"Indicadores de proporção de presença de atributos em relação à
quantidade de domicílio no setor, fazer o Brasil todo e depois para os 70 municípios"*.

**A decisão estruturante: não duplicar as fórmulas.** O caminho rápido seria copiar o
código do Notebook 02 e tirar o filtro de municípios. Rejeitei: duas cópias da mesma
fórmula divergem na primeira correção que alguém fizer em uma só delas, e aí os números do
Brasil e do ELSI deixam de ser comparáveis — que é justamente o ponto da demanda.

Em vez disso extraí as definições para **`src/ivs_censo/indicadores.py`**, onde cada
indicador é declarado como um objeto com numerador, denominador, escala e regras de
tratamento. O notebook e o script nacional aplicam **a mesma definição**. É a única forma
de garantir que a comparação seja legítima.

**Como fiz:**

1. Criei o módulo `src/ivs_censo/` com três partes: procedência das variáveis (`fontes.py`),
   definição dos indicadores (`indicadores.py`) e dicionário (`dicionario.py`).
2. Escrevi `scripts/proporcoes_brasil.py`, que lê os 8 arquivos em blocos, monta a base
   nacional e calcula os 23 indicadores.
3. Apliquei as mesmas regras de elegibilidade e o mesmo recorte urbano, para os números
   serem comparáveis linha a linha.
4. Exportei três recortes — Brasil todos os setores, Brasil urbano, ELSI urbano — mais as
   tabelas por região, UF e município, o comparativo e a representatividade.

**Um erro que este processo revelou.** Na primeira execução usei `float32` para economizar
memória. A população do Brasil somou **203.080.736**, e o número oficial do Censo é
**203.080.756** — 20 pessoas de diferença. O erro relativo é de 1 em 10 milhões, irrelevante
para qualquer proporção, mas os totais são exatamente por onde alguém confere o trabalho.
Refiz em `float64` e acrescentei um teste automatizado que trava a soma no valor oficial,
para o erro não voltar.

**O que a comparação mostrou.** A amostra ELSI cobre 26% da população do país com 1,3% dos
municípios, e concentra **58,6% de todos os setores de favela do Brasil**. Ela é mais rica,
mais alfabetizada e mais bem servida de esgoto que o Brasil urbano — deve ser descrita no
artigo como representativa do **Brasil urbano de grande porte**, não do Brasil. A exceção é
o lixo inadequado, discutida na §11.

---

### 12.9 Decisões que não vieram de demanda

Três escolhas metodológicas relevantes foram feitas fora do escopo das demandas, e ficam
registradas aqui pelo mesmo motivo.

**O denominador `V00001`.** É a decisão mais consequente do projeto inteiro, porque entra
em cinco dos sete componentes. Uma versão anterior usava `V01042`, do arquivo de
Parentesco. O problema: `V01042` conta **pessoas responsáveis**, não domicílios — usá-lo
como denominador domiciliar mistura duas unidades. O `V00001` (Domicílios Particulares
Permanentes Ocupados) é o equivalente exato, no Censo 2022, do `V002` que o IVS-BH usou no
Censo 2010. A verificação empírica que fechou a questão: com `V00001`, **nenhuma proporção
ultrapassa 1,0** em nenhum dos 104 mil setores; com o denominador anterior, várias
estouravam — sinal inequívoco de que o denominador estava errado.

**A ordem das condições da regra `Dados_sig`.** A regra testava sigilo antes de população
zero. Como consequência, setores sem nenhuma população mas com `V00001` vazio eram
rotulados `SIGILOSO` — isto é, contados como *dado suprimido pelo IBGE* quando na verdade
são setores vazios, muitos deles massas d'água. Inverti a ordem. O efeito: o sigilo real
caiu de 2.751 para 1.015 setores e apareceram 1.736 `ZERADO`. **Nenhum setor elegível mudou
de classe** — o conjunto analisado é idêntico. O que muda é parar de superestimar a
supressão do IBGE em todo relatório que cite esse número.

**A caçamba de lixo (`V00398`).** Conta como destino **inadequado**, o que surpreende
qualquer um que leia a tabela pela primeira vez. É o que o `Cálculo IVS2012.docx` determina:
apenas a coleta porta a porta (`V00397`) é adequada. Mantive por fidelidade à
metodologia-fonte (princípio 1 da §12.1) e deixei a anotação no código para não ser
"corrigido" por engano no futuro. **Mas registro a ressalva:** as análises desta EDA
levantaram indício empírico de que essa escolha distorce o indicador — o lixo é a variável
menos correlacionada com todas as outras (§9) e a única em que a amostra está pior que o
Brasil urbano (§11). A hipótese é que a caçamba seja muito mais comum em cidade grande, e
que o indicador esteja capturando porte urbano. É uma decisão a rever com a orientação
antes de fechar a ponderação.

---

### 12.10 Resumo das verificações

Toda decisão acima passou por pelo menos uma verificação empírica. As principais:

| O que foi verificado | Como | Resultado |
|---|---|---|
| Denominador domiciliar | Nenhuma proporção pode passar de 1,0 | 0 setores acima de 1,0 em 104.108 |
| Faixas etárias lidas corretamente | Soma das 11 faixas contra `v0001` | Idêntico em 99.957 setores comparáveis |
| Fórmula do envelhecimento | IEP nacional contra o publicado pelo IBGE | 79,99 contra 80,0 |
| Cadeia inteira de agregação | População nacional contra o Censo | 203.080.756, exato |
| Denominador do tipo de domicílio | Soma dos tipos não pode passar de `V00001` | 0 estouros; déficit máximo de 6 por sigilo |
| Critério de identificação de favela | `CD_TIPO = 1` contra `NM_FCU` preenchido, no país | Coincidem: 33.272 setores |
| Equivalência `SITUACAO` × `CD_SIT` | Tabulação cruzada nos 468.099 setores | Sem exceções |
| Reprodutibilidade dos artefatos | Suíte de testes automatizados | 43 testes |
| Números dos relatórios e da apresentação | Script de auditoria contra os CSVs de origem | 286 valores conferidos, 0 divergências |

---

## 13. Implicações para a Construção do IVS

1. **Normalização por município, não global.** É a mudança mais urgente. A assimetria da
   renda e a natureza intraurbana do objetivo tornam a escala global inadequada.

2. **Tratar as distribuições infladas de zeros.** Para água, esgoto e lixo, a padronização
   min-max é dominada pela cauda. Avaliar transformação, winsorização no P95 ou
   padronização por posto.

3. **Definir a política de sigilo no analfabetismo** antes do cálculo, com imputação
   explícita e indicador de imputação, ou justificar formalmente a exclusão dos setores.

4. **Decidir o destino do indicador de lixo** à luz das seções 9 e 11.

5. **Pesos empíricos, mas com leitura crítica.** A colinearidade do bloco socioeconômico
   favorece a análise fatorial; ainda assim é preciso confrontar o resultado com a
   proporção de referência do IVS-BH (60% socioeconômica, 40% saneamento).

6. **Piso mínimo de setores por município** nas análises municipais, dado o efeito do
   recorte urbano em municípios pequenos.

---

## 14. Limitações da Análise Exploratória

- **Falácia ecológica.** Todas as medidas são agregadas por setor; nada aqui autoriza
  inferência sobre indivíduos (Lima-Costa & Barreto, 2003).
- **Exclusão de institucionalizados.** A regra `Dados_sig` remove setores 100% coletivos
  (asilos, presídios). No recorte ELSI nenhum setor caiu nessa classe, mas a população
  institucionalizada permanece sub-representada dentro dos setores mistos.
- **O recorte urbano reduz municípios pequenos** de forma desigual, como detalhado em 3.4.
- **O sigilo do analfabetismo é seletivo** e afeta 15,9% dos setores.
- **Três componentes do IVS-BH original não são reprodutíveis** com os agregados do Censo
  2022 (anos de estudo, faixas de renda, óbitos cardiovasculares).
- **A EDA é descritiva.** Nenhuma inferência ou teste de hipótese foi conduzido; as
  correlações são exploratórias.

---

## 15. Próximos Passos

| Etapa | Entrega | Depende de |
|---|---|---|
| Notebook 03 | Normalização min-max por município, com renda invertida | nada |
| Notebook 04 | Análise fatorial: KMO, Bartlett, número de fatores, cargas e pesos | NB03 |
| Notebook 05 | IVS final, categorização em 4 faixas e validação contra os setores de FCU | NB04 e decisão sobre pesos |
| Geoprocessamento | Mapas coropléticos e autocorrelação espacial (Moran) | NB05 e malha de setores 2022 |

---

## Anexos — Localização dos artefatos

**Tabelas** (`banco_de_dados/eda/`)

| Arquivo | Conteúdo |
|---|---|
| `descritivas_globais.csv` | Seção 4 |
| `descritivas_por_municipio.csv` · `descritivas_por_regiao.csv` | Seções 5 e 6 |
| `elegibilidade_setores.csv` | Seção 3.3 |
| `situacao_urbano_rural_{total,por_regiao,por_municipio}.csv` · `exclusao_rural_conferencia.csv` | Seção 3.4 |
| `outliers.csv` | Seção 7 |
| `missing_por_municipio.csv` | Seção 8 |
| `correlacao_pearson.csv` · `correlacao_spearman.csv` | Seção 9 |
| `habitacao_precaria_*.csv` · `inadequacao_banheiro_*.csv` · `resp_feminino_*.csv` | Seções 10.1 e 10.2 |
| `indicadores_envelhecimento_*.csv` · `estrutura_etaria_*.csv` | Seção 10.3 |
| `tipo_domicilio_*.csv` · `moradia_predominante_agrupada_por_regiao.csv` | Seção 10.4 |
| `favelas_fcu_*.csv` | Seção 10.5 |
| `diagnostico_proporcoes_fora_intervalo.csv` · `diagnostico_esgoto_312_vs_249.csv` · `extremos_razao_moradores.csv` | Auditorias |

**Figuras** (`banco_de_dados/eda/figuras/`): `histogramas.png`, `boxplots_por_regiao.png`,
`matriz_correlacao.png`, `missing_por_municipio.png`.

**Nacional** (`banco_de_dados/nacional/`): `proporcoes_por_recorte.csv`,
`proporcoes_brasil_por_{regiao,uf,municipio}.csv`, `comparativo_brasil_vs_elsi.csv`,
`representatividade_elsi_no_brasil.csv` — seção 11.

---

## Referências metodológicas

- **SMS-BH.** *Índice de Vulnerabilidade da Saúde 2012.* Belo Horizonte, 2013.
- **Galvão, S. M. et al.** Envelhecimento populacional em Mato Grosso e sua relação com
  indicadores demográficos e econômicos. *Hygeia*, v. 21, e2106, 2025.
- **Lima-Costa, M. F.; Barreto, S. M.** Tipos de estudos epidemiológicos: conceitos básicos
  e aplicações na área do envelhecimento. *Epidemiol. Serv. Saúde*, v. 12, n. 4, 2003.
- **Passarelli-Araujo, H.** Mapeando as disparidades socioeconômicas de saúde urbana.
  *Rev. Bras. Est. Pop.*, v. 40, 2023.
- **Matos, D. A. S.; Rodrigues, E. C.** *Análise fatorial.* Brasília: Enap, 2019.
- **IBGE.** *Censo Demográfico 2022 — Agregados por Setores Censitários.* Rio de Janeiro, 2022.
