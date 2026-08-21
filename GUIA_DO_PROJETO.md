# Guia do Projeto IVS — Censo 2022

> **Documento mestre de retomada.** Reúne, num só lugar, o *porquê* científico, o *como*
> metodológico e o *estado atual* do código. Serve como ponto de partida para retomar o
> trabalho e como base de alinhamento entre o pesquisador e o assistente (Claude).
>
> **Atualizado em:** 10/08/2026 — acrescentada a **seção 6**, que consolida as decisões
> metodológicas com justificativa, verificação e status, e registra as quatro decisões que
> seguem em aberto. Antes disso, 09/08/2026: demandas da orientadora (recorte urbano,
> envelhecimento, tipo de domicílio, favelas, tabela de variáveis e linha de base nacional).
> **Documentos relacionados no repositório:** [`docs/MANUAL_DO_PROJETO.md`](docs/MANUAL_DO_PROJETO.md) ·
> [`README.md`](README.md) ·
> [`estrutura_projeto.md`](estrutura_projeto.md) ·
> [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md) ·
> [`Backup/DIAGNOSTICO_COMPLETO_PROJETO.md`](Backup/DIAGNOSTICO_COMPLETO_PROJETO.md) *(histórico)*

---

## 1. Identidade do Projeto

| Item | Detalhe |
|---|---|
| **Título** | Índice de Vulnerabilidade à Saúde (IVS) intraurbano — Censo Demográfico 2022 |
| **Tipo** | Iniciação Científica (bolsista) |
| **Instituição** | Fiocruz Minas — Instituto René Rachou (IRR) |
| **Área** | Saúde Coletiva — Saúde Urbana e Epidemiologia Espacial |
| **Pesquisador** | Pedro Dias Soares |
| **Período** | Março/2026 – Fevereiro/2027 |
| **Produto final** | Relatório Final de IC + artigo científico submetido a periódico |

---

## 2. Objetivo Científico

### Objetivo geral
Avaliar as desigualdades intraurbanas em saúde por meio da construção de um **Índice de
Vulnerabilidade à Saúde (IVS)** para um conjunto de cidades brasileiras, usando dados do
Censo Demográfico 2022.

### Objetivos específicos
1. Construir um IVS intraurbano, ao nível do **setor censitário**, para os **70 municípios
   da amostra do ELSI-Brasil** (Estudo Longitudinal da Saúde dos Idosos Brasileiros).
2. Analisar a **distribuição espacial** do IVS (mapas temáticos).
3. Descrever a distribuição das variáveis socioeconômicas e de saneamento por setor.
4. Comparar o perfil de vulnerabilidade entre municípios de diferentes regiões e portes.

### Pergunta de pesquisa (PICOS)
Qual a distribuição espacial da vulnerabilidade à saúde nos setores censitários dos
municípios do ELSI-Brasil, construída a partir das variáveis do Censo 2022, e quais padrões
intraurbanos de desigualdade emergem dessa distribuição?

| | |
|---|---|
| **P** — População | Setores censitários **urbanos** dos 70 municípios do ELSI-Brasil (Censo 2022) — 104.108 setores elegíveis |
| **I** — Exposição | Variáveis de saneamento e socioeconômicas em nível de setor |
| **C** — Comparação | Distribuição do IVS entre setores e entre municípios/regiões |
| **O** — Desfecho | IVS contínuo (0–1) e categorizado em 4 faixas de risco |
| **S** — Estudo | Ecológico, com dados agregados por setor censitário |

### Hipóteses
- **H0:** não há padrão espacial sistemático do IVS dentro dos municípios.
- **H1:** setores periféricos apresentam IVS mais alto que áreas centrais (padrão
  centro-periferia descrito na literatura).

---

## 3. Fundamentação Metodológica

O projeto é um **estudo ecológico**. A unidade de análise é o **setor censitário** — a menor
unidade territorial do IBGE — o que permite enxergar desigualdades *dentro* de cada cidade
(análise intraurbana).

**Referências metodológicas centrais:**
- **IVS-BH 2012** (SMS-BH, 2013) — referência principal. Indicador composto que sintetiza
  variáveis de saneamento e socioeconômicas por setor censitário em Belo Horizonte.
- **ISU de Passarelli-Araujo (2023)** — Índice de Saúde Urbana aplicado a 6 capitais
  brasileiras; evidência empírica do padrão centro-periferia.
- **Caiaffa et al. (2021)** e **Buss & Pellegrini Filho (2007)** — determinantes sociais
  e territoriais da saúde.
- **Matos & Rodrigues (2019)** — referência sobre análise fatorial.

**A lacuna:** não existe um IVS padronizado e atualizado com dados do **Censo 2022** para o
conjunto de municípios do ELSI-Brasil. Os estudos anteriores usaram o Censo 2010.

### Etapas estatísticas planejadas
1. Análise descritiva (frequências, média, mediana, desvio-padrão) por município.
2. Padronização **min-max** de cada variável para escala 0–1.
3. **Análise fatorial / ACP** para identificar a estrutura latente e definir os pesos.
4. Cálculo do IVS como média ponderada das variáveis padronizadas (referência IVS-BH:
   dimensão socioeconômica ~60%, saneamento ~40%).
5. Categorização dos setores em 4 faixas (Baixo / Médio / Elevado / Muito Elevado).
6. Geoprocessamento e mapas temáticos no **QGIS**.

### Ética
Usa apenas dados secundários, públicos e anônimos do IBGE. Conforme a Resolução CNS
510/2016 (art. 1°, II e III), **não requer submissão ao CEP**. Segue a LGPD (Lei 13.709/2018).

---

## 4. As Variáveis do IVS

O IVS sintetiza **7 variáveis** em **2 dimensões**. A direção é sempre "↑ valor = ↑
vulnerabilidade" (a renda é invertida).

| Dimensão | Variável | Direção |
|---|---|---|
| **Saneamento** | % domicílios com abastecimento de água inadequado ou ausente | ↑ |
| | % domicílios com esgotamento sanitário inadequado ou ausente | ↑ |
| | % domicílios com destino do lixo inadequado ou ausente | ↑ |
| **Socioeconômica** | Razão de moradores por domicílio (densidade habitacional) | ↑ |
| | % de pessoas analfabetas | ↑ |
| | Rendimento nominal mensal médio das pessoas responsáveis | ↓ (invertido) |
| | % de pessoas de raça/cor preta, parda e indígena | ↑ |

### De-Para: Censo 2010 → Censo 2022

| Componente | IVS 2012 (Censo 2010) | Censo 2022 | Denominador (Relatório) |
|---|---|---|---|
| Água inadequada | V013–V015 | V00112 a V00118 (7 var.) | V00001 |
| Esgoto inadequado | V019–V028 | **V00312–V00316** ✅ (confirmado no dicionário oficial) | V00001 |
| Lixo inadequado | V037–V042 | V00398 a V00402 (5 var.) | V00001 |
| Analfabetismo (15+) | V068–V134 | V00901 / (V00900 + V00901) | V00900 + V00901 (pop. 15+) |
| Densidade habitacional | Pop. / dom. ocupados | (V00005 + V00006) / (V00001 + V00002) *(reproduz o V0005 do IBGE)* | V00001 + V00002 |
| Renda | % fam. ≤ 2 SM | V06004 (rendimento médio, invertido) | — |
| Raça/cor | Pretos + Pardos + Indígenas | V01318 + V01320 + V01321 | v0001 (pop. total) |

### Limitações do Censo 2022 documentadas
| O IVS 2012 pedia | Limitação no Censo 2022 | Solução adotada |
|---|---|---|
| % chefes com < 4 anos de estudo | Anos de instrução não disponíveis nos agregados | Taxa de analfabetismo (V00901) |
| % famílias ≤ 2 salários mínimos | Faixas salariais não disponíveis | Rendimento médio (V06004) invertido |
| Coef. óbitos cardiovasculares | IBGE registrou só se houve óbito, sem causa | Buscar DATASUS (SIM) futuramente |

### Variáveis descritivas complementares (fora dos 7 componentes)

Não entram no índice, mas caracterizam o território e alimentam as tabelas do artigo.
Todas calculadas no Notebook 02 e disponíveis no pacote de entrega.

| Bloco | Variáveis |
|---|---|
| Habitação precária | `pct_dom_improv`, `pct_hab_precaria` |
| Banheiro | `pct_sem_banheiro`, `pct_sem_banheiro_nem_sanitario` |
| Chefia domiciliar | `pct_resp_feminino` |
| **Tipo de domicílio** | `pct_moradia_convencional` (casa + vila/condomínio + apartamento), `pct_moradia_nao_convencional`, **`pct_apartamento`**, `pct_casa`, `pct_casa_vila_condominio` |
| **Envelhecimento** | `pct_pop_0a14`, `pct_idoso_60mais`, **`iep_setor`**, `rdi_setor`, `prop_70mais_entre_60mais` |

### Indicadores de envelhecimento — definições

Fonte: **Galvão, S. M. et al.** *Envelhecimento populacional em Mato Grosso e sua relação
com indicadores demográficos e econômicos.* Hygeia, v. 21, e2106, 2025 — Quadro 1
(indicadores adotados pelas Nações Unidas em estudos populacionais).

| Indicador | Fórmula (× 100) | Censo 2022 | Situação |
|---|---|---|---|
| **IEP** — Índice de Envelhecimento | 60+ / **menores de 15** | (V01040+V01041) / (V01031+V01032+V01033) | ✅ |
| **RDI** — Razão de Dependência de Idosos | 60+ / 15 a 59 | (V01040+V01041) / (V01034…V01039) | ✅ |
| **% 60 anos ou mais** | 60+ / população total | (V01040+V01041) / v0001 | ✅ |
| **LI** — Longevidade | 75+ / 60+ | — | ❌ **inviável**: a faixa mais fina no topo é "70 anos ou mais" (V01041) |

> **Correção de 09/08/2026:** o protótipo anterior usava 60+ / **0–4 anos**, o que
> inflava o índice em ~3×. O denominador correto é a população com menos de 15 anos.
> Valores de referência do Censo 2022 para conferência: IEP Brasil = 80,0; Norte = 41,4;
> Sul = 95,4; Sudeste = 98,0.

### Recorte urbano

O IVS é intraurbano; os setores **rurais são excluídos da análise**. O filtro
(`SITUACAO = Urbana`, equivalente a `CD_SIT ∈ {1,2,3}`) é aplicado no **Notebook 02**,
não na extração — a base bruta preserva os 109.032 setores e a tabela
`exclusao_rural_conferencia.csv` registra exatamente o que saiu, por município.

| | Setores |
|---|---:|
| Base bruta (70 municípios) | 109.032 |
| Elegíveis (`Dados_sig = OK`) | 106.281 |
| **Elegíveis urbanos — recorte de análise** | **104.108** (97,96%) |
| Excluídos pelo filtro rural | 2.173 (2,04%) |

⚠️ A exclusão é desigual entre municípios: 29 dos 70 perdem mais de 10% dos setores, e
alguns municípios pequenos perdem mais de 75% (São Raimundo do Doca Bezerra fica com 3
setores). Isso precisa ser considerado nas análises por município e declarado nas
limitações do artigo.

### Setores de vilas e favelas (FCU)

O Censo 2022 substituiu "aglomerado subnormal" por **Favela e Comunidade Urbana**,
marcada em `CD_TIPO = 1` (com `CD_FCU`/`NM_FCU` identificando a comunidade). No recorte
ELSI são **19.507 setores (17,9%)**, distribuídos em 5.903 FCUs distintas de 42 dos 70
municípios, abrigando 10,07 milhões de pessoas.

---

## 5. O Código — Pipeline Ativa e Legados

A **pipeline ativa** vive em `notebooks/Fase3_EDA_ELSI/` e finalmente aplica o
recorte dos 70 municípios ELSI. As versões anteriores foram movidas para `Backup/`.

### Fase 3 — EDA com filtro ELSI *(ativa)*
`notebooks/Fase3_EDA_ELSI/` — 2 notebooks (01→02).

| Notebook | O que faz |
|---|---|
| `01_Extracao_Filtragem_ELSI` | Lê os 8 CSVs do Censo, cruza por (UF + nome normalizado) com `dados/municipios_elsi_brasil.csv`, filtra apenas os setores dos 70 municípios, faz o merge unificado, classifica morfologia urbana e roda auditoria de integridade. Saída: `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv`. |
| `02_Analises_Descritivas` | EDA completa seguindo o framework FIOCRUZ: tipagem com sigilo → `Dados_sig` → **recorte urbano** → 7 proporções brutas com denominador **V00001** → descritivas globais/municípios/regiões → blocos complementares (habitação precária, banheiro, chefia feminina, **envelhecimento**, **tipo de domicílio**, **favelas**) → histogramas → boxplots por região → outliers (IQR) → mapa de missing → matriz de correlação (Pearson + Spearman). Saídas: CSVs e PNGs em `banco_de_dados/eda/`. |

### Código compartilhado e scripts *(criados em 09/08/2026)*

A pipeline de notebooks continua sendo a referência do recorte ELSI. O que precisava
rodar **fora** dela — o Brasil inteiro, o pacote de entrega — passou a usar um módulo
comum, para as fórmulas não existirem em duas versões.

| Onde | O que é |
|---|---|
| `src/ivs_censo/fontes.py` | Os 8 arquivos do Censo, a chave do setor em cada um e quais variáveis o projeto lê. É a fonte da coluna "arquivo-fonte" da tabela de variáveis. |
| `src/ivs_censo/indicadores.py` | Definição declarativa dos 23 indicadores (numerador, denominador, escala) + `calcular_indicadores` e `classificar_dados_sig`. |
| `src/ivs_censo/dicionario.py` | Lê os dicionários oficiais do IBGE e monta a tabela de variáveis. |
| `scripts/gerar_tabela_variaveis.py` | Gera `Dicionario_Variaveis_Projeto.{csv,xlsx}`. |
| `scripts/gerar_entrega_orientadora.py` | Regenera o pacote de entrega (CSV + SQLite, 95 colunas, 3 tabelas). Antes disso os `.db` vinham de um script ad-hoc não versionado. |
| `scripts/proporcoes_brasil.py` | Calcula os indicadores para os ~468 mil setores do Brasil e compara com os 70 municípios ELSI. |
| `scripts/gerar_tabelas_auditoria.py` | Regenera as 9 tabelas de auditoria/apresentação de `banco_de_dados/eda/` (cobertura de saneamento, morfologia, sigilo em V00901, responsáveis por sexo). Antes vinham de código ad-hoc não versionado — eram os "CSVs órfãos". Usam o recorte com rurais (106.281 setores). |

Cobertura de testes: `tests/test_pipeline_fase3.py` (artefatos) e `tests/test_ivs_censo.py`
(fórmulas, com dados sintéticos).

As **decisões metodológicas** que regem esta pipeline — denominador, regra de
elegibilidade, recorte urbano, tratamento do sigilo — estão consolidadas na
**seção 6**, com justificativa, verificação e status.

### Legados em `Backup/`
- `Backup/Fase1_IVS_Basico/` — 5 notebooks; pipeline inicial (sem filtro ELSI), denominador V00001.
- `Backup/Fase2_IVS_Multidimensional/` — 4 notebooks; segunda iteração (sem filtro ELSI), introduziu V01042 e a Proxy de Extrema Pobreza Multidimensional.
- `Backup/ETL/`, `Backup/formatar/`, `Backup/banco_de_dados/` — scripts auxiliares e bases intermediárias antigas.
- `Backup/DIAGNOSTICO_COMPLETO_PROJETO.md` — diagnóstico histórico.

> ⚠️ **O que ainda falta para o IVS final:** análise fatorial (pesos), composição
> ponderada das duas dimensões e categorização em 4 faixas de risco. O notebook 02
> entrega as descritivas necessárias para alimentar essa próxima etapa.

---

## 6. As Decisões Metodológicas — justificativa, verificação e status

Esta seção é o **registro canônico das decisões**. Cada uma traz: o que foi decidido, a
justificativa, a alternativa descartada, a verificação empírica que a sustenta e o status.
Se algum documento do repositório divergir daqui, **vale esta seção**.

O detalhamento operacional de cada decisão — qual célula, qual comando, como desfazer —
está na Parte C de [`docs/MANUAL_DO_PROJETO.md`](docs/MANUAL_DO_PROJETO.md). A argumentação
estendida, com o passo a passo de execução, está na §12 de
[`docs/Relatorio_EDA_Fase3_IVS_ELSI.md`](docs/Relatorio_EDA_Fase3_IVS_ELSI.md).

### 6.1 Os três princípios que orientam as decisões

**1. A metodologia-fonte manda.** Onde o `Cálculo IVS2012.docx` define — quais formas de
saneamento são inadequadas, qual o denominador, como classificar setores inelegíveis — o
projeto reproduz, mesmo quando o resultado é contraintuitivo. O objetivo é *replicar* o
IVS-BH no Censo 2022, não redesenhá-lo. Caso mais visível: a caçamba de lixo (§6.2.10).

**2. Quando o Censo 2022 não permite reproduzir, a substituição é declarada.** Três
componentes do IVS-BH não existem nos agregados por setor. Nesses casos adota-se o
substituto mais próximo e **declara-se a limitação**, em vez de improvisar um cálculo de
aparência equivalente. O mesmo vale para o que é simplesmente impossível, como o índice de
Longevidade (§6.2.7).

**3. Toda escolha que muda um número é verificada empiricamente.** Nenhuma decisão entrou
sem um teste que a sustente. Onde não foi possível verificar, isso está dito.

### 6.2 Decisões consolidadas

#### 6.2.1 Denominador domiciliar: `V00001`

**Decisão.** O denominador domiciliar é `V00001` (Domicílios Particulares Permanentes
Ocupados), usado em cinco dos sete componentes.

**Justificativa.** É o equivalente exato, no Censo 2022, do `V002` que o IVS-BH 2012 usou
no Censo 2010. Manter a mesma unidade de referência é o que torna os dois índices
comparáveis.

**Alternativa descartada.** `V01042`, do arquivo Parentesco, usado numa versão anterior.
Ele conta **pessoas responsáveis**, não domicílios — usá-lo como denominador domiciliar
mistura duas unidades de análise. A leitura do `Cálculo IVS2012.docx` que sugeria
"considerar o número de responsáveis como total de domicílios" vale apenas para detectar
setores 100% coletivos.

**Verificação.** Com `V00001`, **nenhuma proporção ultrapassa 1,0** em nenhum dos 104.108
setores. Com o denominador anterior, várias estouravam — sinal inequívoco de erro.

**Status:** ✅ consolidada em 22/05/2026, revalidada em 09/08/2026.

#### 6.2.2 Taxa de analfabetismo: denominador é o total de 15+

**Decisão.** `pct_analfab = V00901 / (V00900 + V00901)`.

**Justificativa.** `V00900` conta quem **sabe** ler e escrever e `V00901` quem **não sabe**,
ambos com 15 anos ou mais. O denominador de uma taxa de analfabetismo é a população de
referência inteira, que é a soma das duas.

**Alternativa descartada.** `V00901 / V00900`, usada antes — matematicamente é uma razão
entre analfabetos e alfabetizados, não uma taxa, e gerava setores com valor acima de 1.

**Status:** ✅ consolidada.

#### 6.2.3 Razão de moradores

**Decisão.** `(V00005 + V00006) / (V00001 + V00002)` — inclui domicílios permanentes e
improvisados nos dois lados.

**Justificativa.** Reproduz exatamente a definição do `V0005` publicado pelo IBGE (média de
moradores em Domicílios Particulares Ocupados), o que permite conferir o cálculo contra o
número oficial.

**Status:** ✅ consolidada e validada.

#### 6.2.4 Ordem das condições da regra `Dados_sig`

**Decisão.** As condições são avaliadas nesta ordem: **`ZERADO` → `SIGILOSO` → `COLETIVO`
→ `OK`**. População zero é testada **antes** de sigilo.

**Justificativa.** Com a ordem anterior, setores sem nenhuma população mas com `V00001`
vazio eram rotulados `SIGILOSO`, isto é, contados como *dado suprimido pelo IBGE* quando na
verdade são setores vazios — muitos deles massas d'água (`CD_SIT = 9`). O erro não afeta o
cálculo, mas superestima a supressão em todo relatório que cite esse número.

**Verificação.** O sigilo real caiu de 2.751 para 1.015 setores, e apareceram 1.736
`ZERADO`. **Nenhum setor `OK` mudou de classe** — o conjunto analisado é idêntico.

**Status:** ✅ corrigida em 09/08/2026.

#### 6.2.5 Recorte urbano aplicado na análise, não na extração

**Decisão.** O filtro `SITUACAO = Urbana` é aplicado no Notebook 02. A base bruta preserva
os 109.032 setores.

**Justificativa.** Três razões: **auditabilidade** (a conferência município a município só
é possível com a base completa), **reversibilidade** (desfazer é uma linha, sem reprocessar
2,4 GB) e **fidelidade do dado bruto** (a base continua sendo o retrato do que o IBGE
publica, sem recorte analítico embutido).

**Por que excluir os rurais.** O IVS é intraurbano. Setores rurais têm padrões de
saneamento estruturalmente distintos — fossa e poço são a norma, não a exceção — e, se
mantidos, fariam o índice medir em parte a diferença campo-cidade em vez da desigualdade
dentro da cidade.

**Verificação.** `CD_SIT` 1–3 corresponde a Urbana e 5–8 a Rural em todos os 468.099
setores do país, sem exceção. Os setores com `CD_SIT = 9` têm população zero nas 1.101
ocorrências nacionais.

**Consequência registrada.** A exclusão é desigual: 29 dos 70 municípios perdem mais de
10% dos setores e 14 perdem mais da metade. Precisa constar nas limitações e exige decidir
um piso mínimo de setores para análises municipais (§6.3).

**Status:** ✅ consolidada em 09/08/2026.

#### 6.2.6 Tratamento do sigilo

**Decisão.** O `X` do IBGE vira ausente, nunca zero. Nas somas de numerador, o indicador só
resulta ausente quando **todas** as parcelas estão sigilosas (`min_count=1`). Em
`pct_analfab`, o sigilo é mantido como ausente e **não imputado**.

**Justificativa.** O sigilo do analfabetismo **não é aleatório**: incide onde a contagem
absoluta de analfabetos é pequena, ou seja, nos setores de melhor situação educacional.
Imputar zero subestimaria o analfabetismo justamente nas áreas menos vulneráveis e
comprimiria artificialmente a variabilidade do indicador. Descartar os setores também não
serve: removeria 16% do conjunto de forma seletiva.

**Quantificação do viés (ago/2026).** Os setores sem o dado têm renda mediana de
R$ 6.092,84 contra R$ 2.313,89 dos que têm, e 30,8% de população preta, parda ou indígena
contra 60,6%. O sigilo cai monotonicamente com o porte do setor: 44,1% onde há de 1 a 10
pessoas alfabetizadas, 3,3% acima de mil. Como o IBGE reporta os zeros (9.268 setores
declaram `V00901 = 0`), o valor suprimido é ≥ 1 — e isso limita a média verdadeira da
amostra ao intervalo **3,14% a 3,64%**, faixa estreita o bastante para não mudar nenhuma
conclusão. Detalhamento em `docs/Relatorio_EDA_Fase3_IVS_ELSI.md`, seção 14.1.

**Decisão de agosto de 2026 (orientadora).** A limitação é **aceita e declarada**, sem
imputação. A alternativa antes cogitada — imputar pela mediana municipal com indicador de
imputação — fica descartada para a EDA: ela transferiria aos setores ricos o perfil dos
pobres, na direção oposta ao viés real.

**Status:** ✅ consolidada. A política para o **cálculo final do índice** — excluir os
16.552 setores, calcular o IVS com as seis componentes restantes, ou reportá-los à parte —
segue pendente no Notebook 05.

#### 6.2.7 Indicadores de envelhecimento

**Decisão.** IEP = 60+ ÷ **menores de 15 anos**; RDI = 60+ ÷ 15–59; percentual de 60+ sobre
a população total. Fonte: Quadro 1 de Galvão et al. (2025), que adota os indicadores das
Nações Unidas.

**Justificativa.** A versão anterior usava 60+ ÷ crianças de 0 a 4 anos, o que não
corresponde a nenhuma definição publicada: o índice ficava cerca de três vezes maior e
**incomparável com qualquer referência** — não dava para confrontar com o IEP do Brasil nem
com os valores regionais do próprio artigo.

**Alternativa descartada.** O corte de 65 anos, mais comum na literatura internacional, é
**impossível**: o IBGE agrega a faixa como "60 a 69" (`V01040`). Por isso todos os
indicadores do projeto usam 60+.

**O que é inviável.** O índice de **Longevidade (75+ ÷ 60+) não é calculável** nos
agregados por setor — a faixa mais fina no topo é `V01041` = "70 anos ou mais". A proporção
de 70+ entre os 60+ é calculada como substituto parcial, explicitamente rotulada como **não
sendo o LI**.

**Verificação.** A soma das 11 faixas etárias reproduz `v0001` em todos os 99.957 setores
comparáveis. O IEP nacional resultou em **79,99** contra os **80,0** publicados pelo IBGE.

**Status:** ✅ corrigida em 09/08/2026.

#### 6.2.8 Critério de identificação de favelas

**Decisão.** Setor de Favela e Comunidade Urbana é aquele com **`CD_TIPO = 1`**.

**Justificativa.** É o campo oficial de classificação do tipo de setor; `NM_FCU` é atributo
descritivo.

**Verificação.** Os dois critérios possíveis — `CD_TIPO = 1` e "tem `NM_FCU` preenchido" —
coincidem exatamente nos 468.099 setores do país: 33.272 setores pelos dois. No recorte
ELSI há 25 setores com nome de FCU mas `CD_TIPO ≠ 1`, isolados e quantificados na análise;
eles seguem o critério oficial.

**✅ Validada setor a setor contra a lista oficial (21/08/2026).** O IBGE publica
`FavelaseComunidadesUrbanas2022Setores_20250417.xlsx` (33.272 setores, 12.348 FCU, 656
municípios — bate com a publicação). Cruzando com a nossa base: dos 109.032 setores do
recorte ELSI, **19.507 estão na lista oficial e são exatamente os 19.507 com `CD_TIPO = 1`**
— zero falso positivo, zero omissão, **100,00% de concordância**. Os 25 setores com `NM_FCU`
preenchido e `CD_TIPO ≠ 1` não estão na lista oficial: são setores minúsculos (845 pessoas
somadas) que apenas fazem divisa com uma FCU. `NM_FCU` é atributo descritivo; `CD_TIPO` é a
classificação. Planilha em `dados/`.

**Fonte oficial localizada em 21/08/2026.** IBGE. *Censo Demográfico 2022: Favelas e
Comunidades Urbanas — Resultados do universo.* Rio de Janeiro: IBGE, 2024, 171 p. A
definição e os quatro critérios de identificação estão transcritos em
`docs/Relatorio_EDA_Fase3_IVS_ELSI.md`, seção 14.2.

**⚠️ Limitação estrutural revelada pela fonte (nota 7, p. 75).** Além das 12.348 FCU
classificadas, o IBGE identificou **2.298 FCU com 21 a 50 domicílios que não receberam
setor censitário próprio** — e para as quais não há informação específica divulgada. Isso
significa que `CD_TIPO = 1` **não encontra as favelas pequenas**: seus moradores estão
contabilizados dentro de setores comuns. A comparação "favela × resto da cidade" do NB02
(§7g) é portanto conservadora nos dois sentidos — subestima a população em favela e
contamina o grupo de comparação com ela.

**Unidade de análise.** O IBGE conta **áreas**; nós contamos **setores**. Uma FCU é formada
por 2 setores na mediana do recorte ELSI (média 3,3; máximo 128), e 47% delas têm um setor
só. Os dois números nunca vão coincidir e não devem ser apresentados lado a lado sem essa
nota.

**Representatividade da amostra ELSI, conferida contra o oficial:**

| | Brasil (IBGE 2024) | ELSI-70 (nossa base) | Cobertura |
|---|---|---|---|
| FCU distintas | 12.348 | 5.899 | 47,8% |
| Municípios com FCU | 656 | 42 | 6,4% |
| População em FCU | 16.390.815 | 10.069.994 | **61,4%** |
| Domicílios em FCU | 6.556.998 | 3.443.687 | 52,5% |

Os 70 municípios do ELSI concentram **61,4% de toda a população favelada do país** sendo
apenas 6,4% dos municípios com FCU. É um argumento de representatividade forte para o
artigo — e vale registrar que ele decorre do desenho do ELSI, que privilegia grandes
centros urbanos.

**Status:** ✅ consolidada em 09/08/2026; fonte oficial e limitação incorporadas em
21/08/2026.

#### 6.2.9 Água canalizada: medir pelo complemento de `V00199`

**Decisão (21/08/2026).** `pct_sem_agua_canalizada = 1 − V00199/V00001`, e **não**
`(V00200 + V00201)/V00001`.

**Justificativa.** As três variáveis formam partição de `V00001` — conferido: fecham em
**100,00%** dos 81.270 setores em que as três estão presentes, com diferença máxima de
1,1 × 10⁻¹⁶. Mas `V00200` e `V00201` são contagens pequenas, que o IBGE sigila: exigindo as
duas, **21,9%** dos setores ficam sem valor. `V00199` é contagem grande e quase nunca é
sigilada — pelo complemento, o mesmo número sai com **0,04%** de ausentes.

**Este é um eixo distinto do que já está no IVS.** `pct_agua_inad` (V00112–V00118) mede a
*fonte* da água; a trinca mede a *entrega*. Um domicílio ligado à rede geral pode receber
água só no terreno. Spearman entre os dois: 0,459.

**⚠️ Ressalva.** A identidade só é *verificável* onde as três estão presentes. Nos setores
com sigilo em V00200/V00201, aplicá-la é extrapolação — justificada porque a partição é
definida pelo IBGE, mas suposição, não medição.

**Vale também para os agregados.** Somar `V00200 + V00201` por região subestima o total pelo
mesmo motivo: a contagem suprimida some do numerador e `V00001` continua inteiro no
denominador. As três categorias somam 99,7% a 99,9%, não 100%. A tabela regional usa o
complemento e publica a diferença na coluna `pct_suprimido`.

**Status:** ✅ consolidada; testada em `test_particao_da_agua_canalizada_fecha`.

#### 6.2.10 A caçamba de lixo (`V00398`) conta como destino inadequado

**Decisão.** Mantida como inadequada, conforme o `Cálculo IVS2012.docx`, em que apenas a
coleta porta a porta (`V00397`) é adequada.

**Justificativa.** Princípio 1 (§6.1): fidelidade à metodologia-fonte.

**⚠️ Ressalva empírica registrada.** As análises desta EDA levantaram indício de que a
escolha distorce o indicador: o lixo é a variável **menos correlacionada com todas as
demais** (0,10 a 0,20) e a **única em que o recorte ELSI está pior que o Brasil urbano**
(1,21×). A hipótese é que a caçamba seja muito mais comum em cidade grande e que o
indicador esteja capturando **porte urbano** em vez de vulnerabilidade.

**Status:** ⚠️ mantida por fidelidade, mas **em revisão** — ver §6.3.

#### 6.2.11 Indicadores descritivos ficam fora do índice

**Decisão.** Os dezesseis indicadores complementares (habitação precária, banheiro, chefia
feminina, envelhecimento, tipo de domicílio) **não integram o IVS**.

**Justificativa.** Um componente de índice composto precisa de direção inequívoca de
vulnerabilidade. `pct_apartamento` é o exemplo claro: verticalização aparece tanto em área
central de alta renda quanto em conjunto habitacional popular — não há "mais é pior". Esses
indicadores servem para **caracterizar** o território, não para pontuá-lo.

**Como isso é garantido no código.** A separação é estrutural: em
`src/ivs_censo/indicadores.py` existem duas listas, `INDICADORES_IVS` (7) e
`INDICADORES_COMPLEMENTARES` (16). Um indicador não entra no índice por descuido.

**Status:** ✅ consolidada.

#### 6.2.12 Fórmulas em módulo compartilhado

**Decisão.** As definições dos indicadores vivem em `src/ivs_censo/indicadores.py`, em
forma declarativa, e são usadas pelo cálculo nacional e pelos scripts de entrega.

**Justificativa.** Copiar o código do notebook para rodar o Brasil inteiro criaria duas
versões da mesma fórmula, que divergem na primeira correção feita em uma só delas — e aí a
comparação Brasil × ELSI deixa de ser legítima, que é justamente o objetivo dela.

**Resolvido em 20/08/2026.** O Notebook 02 passou a importar o módulo: as fórmulas
saíram das células e a EDA e o cálculo nacional leem a mesma definição. Conferido rodando o
notebook inteiro — as 38 tabelas se reproduzem, com desvio máximo de 1,5 × 10⁻¹⁵ (soma
*pairwise* do numpy, não mudança de metodologia).

**⚠️ Dívida remanescente.** O Notebook **01** ainda não usa o módulo: ele carrega um
dicionário `ARQUIVOS` próprio, escrito à mão. Acrescentar variável ao projeto exige mexer
em dois lugares — o notebook e `fontes.py` — ou eles divergem.

**Status:** 🟢 implementada no NB02; pendente no NB01.

### 6.3 Decisões em aberto

Quatro pontos dependem de definição com a orientação e travam etapas seguintes:

| # | Decisão | O que ela trava | Elementos para decidir |
|---|---|---|---|
| 1 | **Critério dos pesos**: empíricos (análise fatorial) ou guiados pela literatura (60% socioeconômica / 40% saneamento, padrão IVS-BH)? | Notebooks 04 e 05 | Renda, cor/raça e analfabetismo se correlacionam a −0,81 e −0,76: pesos iguais dariam três votos à posição social sem que isso fosse escolha deliberada |
| 2 | **Indicador de lixo**: entra como está, ou `V00398` (caçamba) é separada das demais formas? | Composição do índice | §6.2.10 — o indicador pode estar medindo porte urbano |
| 3 | **Política de sigilo no analfabetismo** para o cálculo final | Notebook 03 | §6.2.6 — o sigilo é informativo, não aleatório |
| 4 | **Piso mínimo de setores** por município nas análises municipais | Tabelas municipais e mapas | §6.2.5 — 14 municípios perdem mais da metade dos setores |

### 6.4 As demandas de julho de 2026 — resumo

Sete demandas, todas implementadas em 09/08/2026. A justificativa de cada escolha está nas
subseções acima; o processo de execução, na §12 do relatório da EDA.

| # | Demanda | Decisão principal | Resultado |
|---|---|---|---|
| 1 | Ajustar o índice de envelhecimento | Denominador passa a ser menores de 15 (§6.2.7) | IEP 92,7 no recorte |
| 2 | Tabela de variáveis com a fonte | Descrições do dicionário oficial, com coluna de procedência | 67 variáveis, 8 arquivos |
| 3 | Excluir setores rurais | Filtro na análise, não na extração (§6.2.5) | 104.108 setores; 2,04% excluídos |
| 4 | Agrupar moradias convencionais | Critério de adequação da edificação | 99,19% convencionais |
| 5 | Indicador de apartamento | Fora do índice, por falta de direção (§6.2.11) | média de 31,5% |
| 6 | Contagem de vilas e favelas | Critério `CD_TIPO = 1` (§6.2.8) | 19.507 setores (17,9%) |
| 7 | Proporções para o Brasil todo | Módulo compartilhado (§6.2.12) | população confere: 203.080.756 |

Pendente: a **redação das limitações** com Lima-Costa & Barreto (2003) — falácia ecológica,
viés de sobrevivência e exclusão de institucionalizados.

### 6.5 Onde cada nível de detalhe está documentado

| Documento | O que traz | Quando consultar |
|---|---|---|
| **Esta seção** | A decisão canônica, a justificativa e o status | "O que foi decidido, afinal?" |
| [`docs/Relatorio_EDA_Fase3_IVS_ELSI.md`](docs/Relatorio_EDA_Fase3_IVS_ELSI.md), §12 | A argumentação estendida, alternativas descartadas e passo a passo da execução | "Por que, e como foi feito?" |
| [`docs/MANUAL_DO_PROJETO.md`](docs/MANUAL_DO_PROJETO.md), Parte C | Arquivos e células tocados, comandos, como conferir e como desfazer | "Onde está e como rodo de novo?" |

---

## 7. Estrutura de Pastas

```
Projeto_IVS_Censo22/
│
├── README.md                          Apresentação geral
├── GUIA_DO_PROJETO.md                 Este documento (mestre de retomada)
├── estrutura_projeto.md               Arquitetura técnica
├── requirements.txt                   Dependências Python
├── LICENSE                            Licença MIT
│
├── dados/                             DADOS BRUTOS DO IBGE (~2.4 GB, imutáveis)
│   ├── Agregados_por_setores_*.csv     8 CSVs oficiais do Censo 2022
│   ├── municipios_elsi_brasil.csv     Lista oficial dos 70 municípios ELSI
│   ├── output/                        Outputs de scripts auxiliares
│   └── processed/                     Exports em Excel (legado)
│
├── banco_de_dados/                    OUTPUTS DA PIPELINE ATIVA (Fase 3)
│   ├── Base_ELSI_Bruta_Censo2022.csv  Saída do Notebook 01 (filtrada por ELSI)
│   └── eda/                           Saídas do Notebook 02 (descritivas + figuras)
│       ├── descritivas_globais.csv
│       ├── descritivas_por_municipio.csv
│       ├── descritivas_por_regiao.csv
│       ├── outliers.csv
│       ├── missing_por_municipio.csv
│       ├── correlacao_pearson.csv
│       ├── correlacao_spearman.csv
│       └── figuras/                   PNGs (histogramas, boxplots, correlação)
│
├── notebooks/Fase3_EDA_ELSI/          PIPELINE ATIVA
│   ├── 01_Extracao_Filtragem_ELSI.ipynb
│   ├── 02_Analises_Descritivas.ipynb
│   └── README.md
│
├── docs/                              DOCUMENTAÇÃO-FONTE
│   ├── Cálculo IVS2012.docx           Metodologia operacional do IVS-BH
│   ├── guia_analises.docx             Framework FIOCRUZ de EDA
│   ├── indice_vulnerabilidade2012 (2).pdf  IVS-BH 2012 oficial
│   ├── Estudo Longitudinal da Saúde dos Idosos Brasileiros.docx
│   ├── Plano de trabalho.pdf
│   └── Plano_Artigo_Cientifico_IC_Preenchido.docx
│
├── Backup/                            LEGADOS (Fases 1 e 2, scripts antigos)
│   ├── Fase1_IVS_Basico/              5 notebooks da pipeline inicial
│   ├── Fase2_IVS_Multidimensional/    4 notebooks da segunda iteração
│   ├── ETL/                           mapeamento_variaveis.py
│   ├── formatar/                      busca3.py, formatar3.py
│   ├── banco_de_dados/                CSVs intermediários antigos
│   └── DIAGNOSTICO_COMPLETO_PROJETO.md
│
├── src/ivs_censo/                     Código compartilhado (fontes, indicadores, dicionário)
├── scripts/                           gerar_tabela_variaveis · gerar_entrega_orientadora · proporcoes_brasil · gerar_tabelas_auditoria
└── tests/                             test_pipeline_fase3.py + test_ivs_censo.py (43 testes)
```

### Os 8 arquivos-fonte do Censo 2022

| Arquivo | Dimensão | Variáveis-chave |
|---|---|---|
| `..._basico_BR_20250417.csv` | Identificação + população | `CD_SETOR`, `NM_MUN`, `v0001`, `v0005` |
| `..._caracteristicas_domicilio1_BR.csv` | Denominador habitacional | `V00001`, `V00002`, `V00005`, `V00006` |
| `..._caracteristicas_domicilio2_BR_20250417.csv` | Saneamento | Água, esgoto, lixo, banheiro |
| `..._alfabetizacao_BR.csv` | Educação | `V00900` (alfabetizados 15+ — *sabe ler/escrever*), `V00901` (analfabetos 15+). Total 15+ = V00900 + V00901 |
| `..._cor_ou_raca_BR.csv` | Vulnerabilidade social | `V01318`, `V01320`, `V01321` |
| `..._renda_responsavel_BR.csv` | Renda | `V06004` (rendimento médio mensal) |
| `..._demografia_BR.csv` | Sobrecarga infantil (Fase 2) | `V01031`–`V01033` (pop. 0–14) |
| `..._parentesco_BR.csv` | Total de lares reais (Fase 2) | `V01042` (responsáveis) |

---

## 8. Estado Atual

| Etapa | Status |
|---|---|
| Obtenção dos dados brutos do Censo 2022 | ✅ Concluída |
| Mapeamento e dicionários de variáveis | ✅ Concluída |
| Pipeline ETL Fase 2 (sem filtro ELSI) | ⚠️ Legada — substituída pela Fase 3 |
| Lista oficial dos 70 municípios ELSI-Brasil | ✅ [`dados/municipios_elsi_brasil.csv`](dados/municipios_elsi_brasil.csv) |
| Fase 3 — Notebook 01 (extração + filtro ELSI) | ✅ [`notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb`](notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb) |
| Fase 3 — Notebook 02 (análises descritivas) | ✅ [`notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb`](notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb) — implementado |
| Demandas da orientadora (jul/2026) — 7 itens | ✅ Concluídas em 09/08/2026 (envelhecimento, tabela de variáveis, recorte urbano, moradia convencional, apartamento, favelas, Brasil todo) |
| Linha de base nacional (~468 mil setores) | ✅ `scripts/proporcoes_brasil.py` → `banco_de_dados/nacional/` |
| Normalização de renda por município | 🔴 Pendente |
| Validação das variáveis de esgoto | ✅ Concluída — V00312–V00316 confirmado no dicionário oficial do IBGE |
| Análise fatorial / pesos / cálculo do IVS final | 🔴 Pendente |
| Categorização em 4 faixas de risco | 🔴 Pendente |
| Mapas temáticos (QGIS) | 🔴 Pendente |
| Redação do artigo científico | 🟡 Plano preenchido, redação pendente |

A pipeline ativa agora é a **Fase 3** em `notebooks/Fase3_EDA_ELSI/`, que finalmente
aplica o recorte dos 70 municípios. As Fases 1 e 2 ficam preservadas como histórico.

---

## 9. Problemas Conhecidos

Detalhamento completo em [`Backup/DIAGNOSTICO_COMPLETO_PROJETO.md`](Backup/DIAGNOSTICO_COMPLETO_PROJETO.md) *(histórico)* e em [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md).

| # | Problema | Gravidade |
|---|---|---|
| **0** | ~~**Ausência do filtro ELSI-Brasil**~~ — **resolvido na Fase 3**: `notebooks/Fase3_EDA_ELSI/01` filtra os 70 municípios ELSI (109.032 setores) antes de qualquer cálculo. | ✅ Resolvido |
| **1** | ~~**Variáveis de esgoto inconsistentes**~~ — **resolvido**: o dicionário oficial do IBGE (`dados/dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx` e o recorte em `docs/Apresentacoes_IVS/dicionarios/Dicionario_IBGE_Oficial_Variaveis_do_Projeto.xlsx`) confirma que **V00312–V00316** é o bloco de esgoto inadequado (fossa rudimentar, vala, rio/lago/mar, outra forma, inexistente). V00309–V00311 são adequadas (rede geral, fossa séptica). Os notebooks já usam V00312–V00316; o diagnóstico empírico está na célula `step4b` do Notebook 02. | ✅ Resolvido |
| **2** | **Normalização de renda global** — usa min/max de todos os setores do Brasil; deveria ser por município para capturar desigualdade intraurbana. | 🔴 Crítico |
| **3** | ~~Denominadores divergentes~~ — **resolvido em 22/05/2026**: consolidado **V00001** (Dom. Particulares Permanentes Ocupados) como denominador domiciliar, padrão do IVS-BH 2012. O **V01042 foi descartado** (é contagem de pessoas, não de domicílios). Decisão empiricamente validada: com V00001 nenhuma proporção de saneamento estoura 1,0. | ✅ Resolvido |
| **4** | ~~Duas pipelines paralelas~~ — **resolvido**: a Fase 3 é a oficial; as Fases 1 e 2 foram arquivadas em `Backup/` como histórico. | ✅ Resolvido |
| **5** | **~8 GB de dados duplicados/obsoletos** espalhados pelo projeto. | 🟡 Organizacional |
| **6** | ~~README/docs parcialmente desatualizados~~ — **resolvido**: `docs/Relatorio_EDA_Fase3_IVS_ELSI.md` foi regerado em 12/06/2026 sobre a metodologia V00001 e está consistente com os CSVs atuais; `Relatorio_Integridade_Projeto.md` revisado na mesma data. | ✅ Resolvido |
| **7** | ~~requirements.txt incorreto~~ — **resolvido**: lista `pandas`, `numpy`, `matplotlib`, `openpyxl`, `xlsxwriter`; sem módulos built-in. Em 20/08/2026 ganhou `ipykernel`/`nbclient`: a pipeline **são** os notebooks, e sem kernel não havia como executá-los. | ✅ Resolvido |
| **8** | **Código duplicado nos notebooks** — função `ler_csv_padronizado` definida duas vezes na Fase 2; auditoria duplicada na Fase 1. | 🟢 Menor |
| **9** | ~~Entregáveis sem código-fonte~~ — os `.db`/`.csv` de `entrega_orientadora/` vinham de script ad-hoc não versionado. **Resolvido em 09/08/2026**: `scripts/gerar_entrega_orientadora.py`. | ✅ Resolvido |
| **10** | ~~Massas d'água contadas como sigilo~~ — 1.736 setores sem população apareciam como `SIGILOSO` porque a condição de sigilo era testada antes da de população zero. **Resolvido**: ordem invertida em `classificar_dados_sig`; nenhum setor `OK` mudou. | ✅ Resolvido |
| **11** | **Municípios pequenos ficam com poucos setores após o filtro urbano** — 29 dos 70 perdem >10% dos setores; alguns ficam com menos de 10. Afeta a estabilidade das descritivas por município e precisa constar nas limitações. | 🟡 Metodológico |
| **12** | ~~CSVs órfãos em `banco_de_dados/eda/`~~ — 9 tabelas commitadas sem código que as reproduzisse. **Resolvido em 20/08/2026**: `scripts/gerar_tabelas_auditoria.py` as regenera valor a valor. Fica registrado que elas são do recorte **com rurais** (106.281 setores), diferente do recorte urbano do NB02. | ✅ Resolvido |

---

## 10. Plano de Retomada — Próximos Passos

Ordem sugerida de ataque ao reentrar no projeto:

### Prioridade 0 — Desbloquear (filtro ELSI-Brasil) ✅ Concluída na Fase 3
- [x] Obter a lista oficial dos **70 municípios do ELSI-Brasil**
      (fonte: <https://elsi.cpqrr.fiocruz.br/amostra/>).
- [x] Criar `dados/municipios_elsi_brasil.csv`.
- [x] Adicionar o filtro no notebook de extração (Fase 3, Notebook 01).
- [x] Reprocessar a pipeline apenas com os setores dos 70 municípios.

### Prioridade 1 — Validação metodológica (em paralelo)
- [x] Resolver a inconsistência das variáveis de esgoto consultando o dicionário do IBGE — **V00312–V00316 confirmado** (dicionário oficial versionado).
- [x] Decidir e **documentar** o denominador de saneamento — **V00001** consolidado em 22/05/2026.
- [ ] Mudar a normalização de renda para **por município** (Notebook 03).
- [x] Validar a razão de moradores `(V00005+V00006)/(V00001+V00002)` — reproduz o V0005 do IBGE.

### Prioridade 1b — Demandas da orientadora (jul/2026) ✅ Concluídas em 09/08/2026
- [x] **Índice de envelhecimento** com denominador correto (menores de 15), mais RDI e % 60+.
- [x] **Tabela de variáveis** com descrição oficial do IBGE e arquivo-fonte do Censo.
- [x] **Exclusão dos setores rurais**, com conferência por município e região.
- [x] **Agrupamento das moradias convencionais** no tipo de domicílio.
- [x] **Indicador de apartamento** (`pct_apartamento`).
- [x] **Contagem de setores de vilas e favelas** (FCU) no recorte ELSI.
- [x] **Proporções para o Brasil todo** e comparativo com os 70 municípios.
- [ ] Redigir as limitações do artigo com Lima-Costa & Barreto (2003): falácia ecológica,
      viés de sobrevivência e exclusão de institucionalizados (que na base corresponde a
      `Dados_sig = COLETIVO`). **Parcial:** a limitação do sigilo do analfabetismo foi
      escrita e quantificada em 21/08/2026 (seção 14.1 do relatório da EDA); faltam as
      outras três.

### Prioridade 2 — Completar o cálculo do IVS
- [ ] Implementar a **análise fatorial / ACP** para definir os pesos.
- [ ] Calcular o **IVS final** (média ponderada das variáveis padronizadas).
- [ ] Categorizar os setores em 4 faixas (Baixo / Médio / Elevado / Muito Elevado).

### Prioridade 3 — Limpeza e organização
- [ ] Remover `src/ETL/ficheiros_inuteis/` e demais duplicados (~8 GB).
- [ ] Decidir o destino da Fase 1 (arquivar ou remover).
- [x] Corrigir `requirements.txt`, `.gitignore` e a documentação — em 20/08/2026 o `.venv/`
      passou a ser ignorado, o `requirements.txt` ganhou o kernel dos notebooks e o
      `README`/`GUIA` passaram a documentar a criação do ambiente.

### Prioridade 4 — Geoprocessamento e artigo
- [ ] Mapas temáticos no QGIS (atualizar referência: usar QGIS 3.x, não 2.10.1).
- [ ] Definir o **periódico-alvo** (impacta toda a formatação do artigo).
- [ ] Avançar a redação seguindo o `Plano_Artigo_Cientifico_IC_Preenchido.docx`.

---

## 11. Cronograma do Bolsista

| Atividade | Período |
|---|---|
| Programa de Inserção do IRR + Curso Introdutório | Mar–Abr/2026 |
| Revisão bibliográfica (SciELO, PubMed) | Mar–Dez/2026 |
| Reuniões periódicas com a orientadora | Mar/2026–Fev/2027 |
| Análise da consistência do banco de dados | Mar–Jul/2026 |
| Análise dos dados (estatística + mapas) | Mar–Set/2026 |
| Cálculo do IVS (fatorial, padronização, ponderação) | Ago–Set/2026 |
| Mapas temáticos (QGIS) | Set/2026 |
| Trabalhos para congressos (RAIC, Saúde Coletiva) | Conforme chamadas |
| Redação do artigo (tabelas→resultados→discussão→introdução→resumo) | Out–Dez/2026 |
| Redação do Relatório Final de IC | Dez/2026–Fev/2027 |
| Submissão do artigo | Fev/2027 |

---

## 12. O Plano do Artigo — Estado das Fases

O `Plano_Artigo_Cientifico_IC_Preenchido.docx` segue a sequência de redação
**tabelas → método → resultados → discussão → introdução → resumo** (Pereira & Galvão;
checklist STROBE).

| Fase | Conteúdo | Completude |
|---|---|---|
| Brainstorm | Contextualização e lacuna | ~80% |
| Fase 0 | Objetivos e hipóteses | ~80% |
| Fase 1 | Tabelas e figuras planejadas | 100% |
| Fase 2 | Método | ~95% |
| Fase 3 | Resultados | ~40% (depende da análise) |
| Fase 4 | Discussão | ~60% |
| Fase 5 | Introdução | ~60% (verificar referências) |
| Fase 6 | Resumo | ~60% |
| Fase 7 | Checklist final | 100% |

**Pendências do plano a resolver:**
- Definir o **periódico-alvo** e suas normas (limite de palavras, referências, citação).
- Preencher: Pesquisador(a) Principal, objetivo refinado (versão final).
- Resolver as notas internas "Conferir isso ainda!" (Introdução) e "Verificar
  possibilidade!" (Tabela 6 da Discussão).
- Verificar a referência "Agero (2020)" — citada mas ausente da lista de referências-chave.
- Adicionar **nota de rodapé** explicando raça/cor como *proxy* de vulnerabilidade social
  estrutural (a Tabela 5 tem um asterisco sem explicação).
- Expandir a lista de referências (hoje 8) — incluir publicação de referência do
  ELSI-Brasil, metodologia do Censo 2022 e revisões internacionais recentes.
- Decidir o critério dos **pesos do IVS**: empíricos puros (análise fatorial) ou guiados
  pela literatura (~60% socioeconômica / ~40% saneamento, conforme IVS-BH 2012).

---

## 13. Como Executar

**Pré-requisitos:** Python 3.10+ e os 8 CSVs do Censo 2022 em `dados/`.

```bash
python3 -m venv .venv && ./.venv/bin/python -m pip install -r requirements.txt
```

Todo comando do projeto usa o Python desse ambiente (`./.venv/bin/python`); o `.venv/`
não é versionado. Os notebooks também rodam sem interface, o que serve de conferência
de que a pipeline continua de pé:

```bash
./.venv/bin/jupyter execute notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb
```

Executar os notebooks da **pipeline ativa (Fase 3)** na ordem numérica:

```
notebooks/Fase3_EDA_ELSI/  →  01 → 02
```

> O Notebook 01 extrai e filtra os 70 municípios ELSI (gera `Base_ELSI_Bruta_Censo2022.csv`);
> o Notebook 02 roda a EDA. As Fases 1 e 2 em `Backup/` são legado e não fazem parte da
> pipeline atual.

> A execução completa consome bastante RAM e tempo (~2.4 GB de CSVs brutos). Os notebooks
> leem apenas as colunas necessárias para proteger a memória.

---

## 14. Referências

- **IBGE.** *Censo Demográfico 2022: Favelas e Comunidades Urbanas — Resultados do
  universo.* Rio de Janeiro: IBGE, 2024. 171 p. — definição e critérios de FCU (§6.2.8).
- **SMS-BH.** *Índice de Vulnerabilidade da Saúde 2012.* Belo Horizonte: Secretaria
  Municipal de Saúde, 2013.
- **Passarelli-Araujo, H.** Mapeando as disparidades socioeconômicas de saúde urbana: um
  estudo comparativo entre seis capitais brasileiras. *Rev. Bras. Est. Pop.*, v. 40, 2023.
- **Caiaffa, W. T. et al.** *Saúde urbana, cidades e a interseção de sistemas.* Rio de
  Janeiro: Fiocruz, 2021.
- **Buss, P. M.; Pellegrini Filho, A.** A saúde e seus determinantes sociais. *Physis*,
  v. 17, n. 1, p. 77–93, 2007.
- **Gioia, T. B.; Pereira, A. C. F.; Raminelli, J. A.** Avaliação de métodos para
  construção de um índice de vulnerabilidade de saúde para Londrina-PR. *Hygeia*, v. 16,
  2020.
- **Matos, D. A. S.; Rodrigues, E. C.** *Análise fatorial.* Brasília: Enap, 2019.
- **Allik, M. et al.** *Developing a small-area deprivation measure for Brazil.* Glasgow:
  University of Glasgow, 2020.
- **Kalache, A.; Gatti, A. A.** Envelhecimento ativo: um paradigma para o século XXI.
  *Rev. Bras. Geriatr. Gerontol.*, v. 23, n. 1, 2020.
- **IBGE.** *Censo Demográfico 2022 — Agregados por Setores Censitários.* Rio de Janeiro:
  IBGE, 2022.
- **Galvão, S. M.; Galvão, N. D.; Alves, M. R.; Rocha, S. C.; Rocon, P. C.; Andrade,
  A. C. S.** Envelhecimento populacional em Mato Grosso e sua relação com indicadores
  demográficos e econômicos. *Hygeia*, v. 21, e2106, 2025. — Definições do IEP, RDI,
  LI e % 60+ (Quadro 1); referência de estudo ecológico com análise espacial (Moran).
- **Lima-Costa, M. F.; Barreto, S. M.** Tipos de estudos epidemiológicos: conceitos
  básicos e aplicações na área do envelhecimento. *Epidemiologia e Serviços de Saúde*,
  v. 12, n. 4, p. 189–201, 2003. — Tipologia de estudos e fontes de viés
  (respondente próximo, exclusão de institucionalizados, viés de sobrevivência).
