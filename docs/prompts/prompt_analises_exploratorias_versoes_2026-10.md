# Prompt de execução — as análises exploratórias por versão, com um deck extenso cada

Outubro de 2026. Produz, numa pasta só, **uma análise exploratória completa para cada
versão possível do IVS e da base**, cada uma com tabelas, figuras e uma apresentação
PowerPoint extensa que explica cada gráfico e cada tabela. O objetivo não é escolher
nada: é pôr na mesa, de forma organizada, tudo o que os dados e os índices trabalhados
desde março conseguem mostrar, para que Pedro e a orientadora escolham o que vai para o
artigo.

Base deste prompt:
- [`../relatorios/Apanhado_Analises_Exploratorias_2026-10.md`](../relatorios/Apanhado_Analises_Exploratorias_2026-10.md)
  e o catálogo que o acompanha: o que já existe e o que vale;
- [`../metodologia/Levantamento_Analises_Exploratorias_2026-10.md`](../metodologia/Levantamento_Analises_Exploratorias_2026-10.md):
  os eixos em que uma versão pode variar (A a D) e as análises (E1 a E15).

## Como usar

Abrir uma **sessão nova** (`/clear`) na raiz do projeto, com o modelo **Sonnet** e esforço
médio, e pedir **um lote por vez** (seção 4). Cada lote é uma sessão.

- **Lotes 0a e 0b:** ler este prompt das seções 0 a 3 (uma vez) e mais nada além do
  código que vão reaproveitar.
- **Do lote 1a em diante:** ler só `analises_exploratorias/ESTADO.md`, a seção 0.1, a
  linha do lote na seção 4 e as linhas das versões dele nas seções 2.2 e 2.3 (com
  `grep -n` e `sed -n`). Nunca o prompt inteiro de novo, nem o apanhado, nem os relatórios.

---

## 0. Regras

### 0.1 Orçamento de tokens — a regra que vem antes de todas

O custo de uma sessão cresce com o **número de chamadas de ferramenta**, porque cada uma
relê o contexto inteiro (medido em setembro, `prompt_economia_tokens.md`). Por isso:

1. **Teto de chamadas por lote**, na seção 4. **Ao chegar a 80% do teto**: terminar a
   versão em curso, gravar `ESTADO.md` e parar — mesmo que o lote não tenha acabado. Nunca
   parar no meio de uma versão.
2. **Uma versão = três comandos**, e só três:
   - `python scripts/eda_versoes.py analises_exploratorias/<versao>` — gera tudo e imprime
     um resumo de no máximo 30 linhas;
   - `node scripts/gerar_deck_versao.js analises_exploratorias/<versao>`;
   - `python scripts/verificar_versao.py analises_exploratorias/<versao>` — todas as
     conferências da seção 3 num script só, saída de no máximo 20 linhas.
   Se um deles falhar, uma correção e uma nova tentativa. **Falhou duas vezes do mesmo
   jeito: gravar o estado e parar**, sem insistir.
3. **Nada de ler o que o motor gerou.** Não abrir CSV, PNG nem PPTX para "dar uma olhada";
   o resumo e o verificador dizem o que precisa ser dito. Quando for inevitável ler um CSV,
   com pandas, filtro e `head`.
4. **Imagens: uma folha de contato no lote 0b** (o deck piloto, em escala reduzida), e
   nenhuma depois — salvo se o verificador apontar texto saindo da caixa numa página
   específica, e aí só essa página.
5. **Os textos dos slides não são escritos à mão em cada versão.** "Como ler" e as notas
   longas vêm de `analises_exploratorias/_modelos/textos_blocos.json`, escrito uma vez no
   lote 0a; "O que mostra" é preenchido pelo gerador a partir do CSV. Cada versão só
   escreve um `textos.json` curto (a pergunta da versão, o que muda, as limitações):
   **no máximo 40 linhas**.
6. **Não reler.** O que o lote vai reaproveitar (assinaturas de função, nomes de coluna)
   fica anotado em `ESTADO.md` pelo lote que descobriu.
7. `grep` com escopo (fora de `graphify-out/`, `.venv/`, `node_modules/`, `banco_de_dados/`);
   grafo antes de abrir arquivo (`graphify query "<pergunta>" --budget 1500`); saídas com
   `| head -60`.
8. **Sem subagentes e sem workflows.** Nenhum.
9. **Relatório de fim de lote: no máximo 15 linhas**, e então parar. O lote seguinte só
   começa quando Pedro mandar, em sessão nova.
10. **Se o limite de uso bater:** na sessão seguinte, `git status` e `ESTADO.md` primeiro;
    retomar da última versão completa, sem refazer as anteriores.

### 0.2 Projeto
- **Reaproveitar, não reescrever.** Indicadores vêm de `src/ivs_censo/indicadores.py`;
  renda, de `src/ivs_censo/renda.py`; fatorial, de `src/ivs_censo/fatorial.py`; índice,
  pesos, faixas e AUC, das funções de `scripts/ivs_especificacoes.py` e
  `scripts/fatorial_ampliada.py`. Se uma função precisar mudar, a mudança vai no módulo,
  com teste.
- **Número que aparece em deck sai de CSV gerado**, nunca digitado no gerador. Os
  geradores só formatam.
- **Ler a base em modo só leitura**: `banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db`
  (e a de Belo Horizonte, quando a versão pedir). Nada sobrescreve as pastas existentes de
  `banco_de_dados/eda/`.
- Testes com `pytest`; os 103 testes atuais continuam passando.
- Decks com `scripts/deck_comum.js` (identidade visual do projeto) e `pptxgenjs`.
- Figuras em matplotlib, dpi 150, paleta do projeto: tinta `#1A1A1A`, petróleo `#1F4E4A`,
  argila `#A83A2C`, cinza `#666666`.
- Commits só com o nome de Pedro Dias Soares, sem `Co-Authored-By` nem qualquer outra
  marca; ramo de trabalho sem o prefixo `claude/`. Commit só quando Pedro pedir.
- Nos arquivos produzidos (decks, READMEs, comentários de código), linguagem do projeto:
  sem menção a assistente, sessão ou ferramenta de geração.

### 0.3 O que o executor não decide
- **Nenhuma versão é "a melhor".** Toda comparação entre versões é descritiva. A
  referência continua sendo a proposta do NB05 até a orientadora decidir.
- Quando uma versão precisar de um parâmetro que ninguém fixou (piso de população,
  composição do IVS-Idoso, método de imputação), rodar com o valor-padrão desta seção 2.3,
  rotulá-lo no deck como **"parâmetro exploratório — não é decisão"** e registrar a
  pergunta em `analises_exploratorias/PERGUNTAS.md`.
- Nada é retirado de uma versão para "fazer funcionar" (ex.: tirar variável para passar
  no KMO). Versão que falha um critério fica registrada como falha.

---

## 1. Fatos verificados — não redescobrir

| Fato | Fonte |
|---|---|
| Recorte da EDA: 104.108 setores urbanos com `Dados_sig = OK`, 70 municípios | `entrega_orientadora/README.md` |
| Base com rurais (`Dados_sig = OK`): 106.281 setores | idem |
| Fatorial do NB04: 87.545 setores com os 7 componentes completos | `Relatorio_Analise_Fatorial_NB04.md` |
| Referência proposta do NB05: `original·lixo_sem·banheiro_graduado·promax·60_40·municipal`, 73.878 setores | `eda/ivs_especificacoes/referencia.csv` |
| Grade do NB05: 324 especificações, 192 elegíveis (96 municipais, 96 globais) | `eda/ivs_especificacoes/especificacoes.csv` |
| Critérios de elegibilidade: KMO ≥ 0,70; MSA ≥ 0,50; comunalidade ≥ 0,30; carga ≥ 0,40 | `eda/ivs_especificacoes/README.md` |
| AUC do NB04 contra FCU: 0,813 | relatório NB04 |
| `eda/atualizada/` substitui 15 tabelas de `eda/` com o mesmo nome e o rótulo `renda_media` | `eda/atualizada/README.md` |
| 31 indicadores e variantes; `pct_so_sanitario` e `pct_banheiro_comum` nunca tabulados | `docs/relatorios/Catalogo_Analises_Exploratorias.xlsx` |
| Renda sigilosa e analfabetismo com faltantes não aleatórios (15,9%) | relatório da EDA |
| Saneamento com mediana zero: IQR não serve para outlier nessas variáveis | relatório da EDA |
| Não existe malha geográfica dos setores no computador | verificado em 05/10/2026 |
| Arquivos do Censo em `dados/`: básico, domicílio 1 e 2, renda, demografia, parentesco, alfabetização, cor ou raça. **Faltam** domicílio parte 3 e óbitos | verificado em 06/10/2026 |

---

## 2. A arquitetura

### 2.1 A pasta

```
analises_exploratorias/
├── README.md              ← índice: uma linha por versão, com status, n e link do deck
├── ESTADO.md              ← onde a execução parou (lido no início de cada sessão)
├── PERGUNTAS.md           ← parâmetros exploratórios e perguntas para a orientadora
├── Catalogo_Mestre.xlsx   ← todas as tabelas e figuras de todas as versões, com as
│                            colunas de escolha (Vai para o artigo? · Seção · Comentários)
├── 00_referencia/
├── 00_sintese/            ← a comparação entre todas as versões (feita por último)
├── A1_com_rurais/
├── ...
└── X_bloqueadas.md        ← as versões que dependem de dado que não temos
```

Cada subpasta de versão tem sempre a mesma forma:

```
<versao>/
├── README.md        ← o que muda em relação à referência, recorte, n, como regenerar
├── config.json      ← a definição da versão (lida pelo motor; nada fica no código)
├── tabelas/         ← T01_*.csv, T02_*.csv … (numeradas na ordem do deck)
├── figuras/         ← F01_*.png, F02_*.png …
├── catalogo.csv     ← uma linha por tabela e figura: id, título, bloco, o que mostra,
│                      arquivo, slide do deck
└── <versao>.pptx    ← o deck extenso
```

Arquivos por setor com mais de 50 MB não são versionados (acrescentar ao `.gitignore`).

### 2.2 As versões

Cada versão é a **referência com uma coisa mudada**: um eixo por vez. Assim cada deck
responde a uma pergunta só ("o que muda se…"), e a síntese compara todas contra a mesma
base.

| Pasta | O que muda | Blocos (seção 2.4) |
|---|---|---|
| **00_referencia** | Nada: o recorte da EDA (104.108), todos os 31 indicadores e o IVS da referência proposta | todos |
| **A — que setores entram** | | |
| A1_com_rurais | Inclui os setores rurais (106.281) | 1–8, 10, 13 |
| A2_piso_populacional | Só setores com pelo menos o piso de moradores | 1–8, 10, 13 |
| A3_belo_horizonte | Só Belo Horizonte (base própria da entrega) — conversa com o IVS-BH 2012 | todos |
| A4_por_regiao | Os blocos rodados separadamente em cada uma das cinco regiões | 1–8, 10, 13 |
| A5_por_porte | Os blocos por faixa de porte do município | 1–8, 10, 13 |
| A6_brasil | Os indicadores nos ~468 mil setores do Brasil, lado a lado com os 70 municípios | 1–7, 9, 13 |
| **B — que indicadores entram** | | |
| B1_renda | As três rendas (original, sem o extremo, mediana municipal) | 2–7, 9–10, 13 |
| B2_agua | Água inadequada × sem canalização × não encanada × só no terreno | 2–7, 9–10, 13 |
| B3_banheiro | Fora × V00495 × graduado × as quatro partições | 2–7, 9–10, 13 |
| B4_esgoto | As duas definições de esgoto (312 × 249) | 2–7, 9–10, 13 |
| B5_lixo | Com × sem lixo | 9–10, 13 |
| B6_moradia | Razão de moradores × improvisado × habitação precária × tipos de moradia | 2–7, 9–10, 13 |
| B7_raca | O índice com e sem cor ou raça | 9–10, 13 |
| B8_complementares | Chefia feminina, crianças de 0 a 4 e de 0 a 14 anos, como candidatas ao índice | 2–7, 9–10, 13 |
| **C — como o índice é construído** | | |
| C1_rotacao_e_pesos | Sem rotação × Varimax × promax; os 9 esquemas de peso | 9–13 |
| C2_extracao | Componentes principais × eixo principal × máxima verossimilhança | 9–10, 13 |
| C3_normalizacao | Min-max municipal × min-max global × escore z × percentis | 10–13 |
| C4_agregacao | Soma ponderada × média geométrica | 10–13 |
| C5_faixas | Regra do IVS-BH × quartis × quintis × quebras naturais × agrupamento | 10–12 |
| C6_pesos_iguais | Pesos iguais e média de postos, sem fatorial | 10–13 |
| **D — índices novos ao lado do IVS** | | |
| D1_subindices | Socioeconômico e saneamento separados | 10–13 |
| D2_ivs_idoso | O IVS com uma dimensão de envelhecimento (IEP, RDI, 60+) | 8–13 |
| D3_indice_moradia | Um índice só de moradia | 9–13 |
| D4_ibp_aproximado | Réplica aproximada do Índice Brasileiro de Privação com o Censo 2022 | 10–13 |
| D5_especialista_x_dados | Pesos do IVS-BH (60/40) × pesos da fatorial, como em Gioia et al. (2020) | 10–13 |
| **E — análises que atravessam as versões** | | |
| E1_incerteza | Para cada setor, em quantas das versões elegíveis ele cai em risco elevado | próprio |
| E2_estabilidade | Um município de fora por vez e reamostragem de setores | próprio |
| E3_desigualdade_intramunicipal | P90/P10, Gini e Theil do IVS dentro de cada município | próprio |
| E4_populacao_em_risco | Pessoas e pessoas de 60+ em cada faixa, por município | próprio |
| E5_ivs_e_envelhecimento | IVS × IEP, RDI e 60+ | próprio |
| E6_tipologias | Agrupamento de setores e de municípios por perfil de vulnerabilidade | próprio |

**Bloqueadas** (vão só para `X_bloqueadas.md`, com o que falta para cada uma): análise
espacial e mapas (falta a malha de setores do IBGE); comparação com o IVS-BH de 2010
(falta compatibilizar os setores de 2010 e 2022); validação com óbitos (falta o arquivo
de óbitos do Censo, 93 variáveis por setor); sigilosos imputados (falta decidir o método).

### 2.3 Parâmetros exploratórios (valores-padrão, nenhum é decisão)

| Parâmetro | Valor-padrão | Onde aparece |
|---|---|---|
| Piso de população (A2) | 50 moradores; registrar também 100 numa tabela de sensibilidade | A2 |
| Faixas de porte (A5) | três faixas: até 100 mil, de 100 a 500 mil e mais de 500 mil habitantes | A5 |
| Composição do IVS-Idoso (D2) | terceira dimensão com IEP, RDI e % 60+, pesos pela fatorial | D2 |
| Variáveis do IBP aproximado (D4) | as que o relatório técnico de Allik et al. (2020) usa, quando existirem nos agregados de 2022; as ausentes, listadas | D4 |
| Número de grupos (C5, E6) | o que o critério da silhueta indicar entre 3 e 6, com 4 sempre reportado | C5, E6 |
| Reamostragens (E2) | 1.000, semente 42 | E2 |

### 2.4 A bateria de blocos (a "máxima" análise exploratória)

Cada versão roda os blocos marcados na tabela 2.2, sempre na mesma ordem e com os mesmos
números de tabela e figura, para que os decks sejam comparáveis entre si.

| Bloco | Conteúdo | Tabelas e figuras mínimas |
|---|---|---|
| 1. Recorte | Quantos setores entram, quantos saem e por quê; perdas por variável | funil de setores; perdas por indicador |
| 2. Descritivas | Para cada indicador da versão: n, média, DP, mediana, P10, P25, P75, P90, mín., máx., assimetria, curtose, % de zeros, CV — global, por região e por município | tabela global; tabela por região; tabela por município |
| 3. Distribuições | Histogramas, boxplots por região, gráficos de densidade | um painel por dimensão |
| 4. Faltantes e sigilo | Faltantes por indicador e por município; o padrão não aleatório do sigilo | mapa de calor de faltantes |
| 5. Extremos | Critério adequado a cada indicador (IQR onde serve; o critério da renda; zeros onde há inflação de zeros) | lista de extremos; contagem por município |
| 6. Correlações | Spearman e Pearson, mapa de calor, pares acima de 0,80, dendrograma das variáveis | duas matrizes; figura |
| 7. Favelas (FCU) | FCU × não FCU em cada indicador: medianas, diferença, AUC de cada indicador sozinho | tabela; figura de barras pareadas |
| 8. Envelhecimento | Pirâmide, 60+, IEP, RDI e 70+ entre os 60+, e o cruzamento com os demais indicadores | pirâmide; tabela; dispersão |
| 9. Adequação fatorial | KMO, MSA por variável, Bartlett, autovalores, Kaiser × Horn, cargas, comunalidades, Φ | tabelas; gráfico de sedimentação com a linha de Horn; mapa de cargas |
| 10. O índice da versão | Pesos, distribuição do índice, faixas pelas duas regras, AUC contra FCU (global e mediana municipal), elegibilidade pelos critérios do NB05 | tabelas; curva ROC; histograma por faixa |
| 11. Quem está em risco | Setores, pessoas e pessoas de 60+ por faixa, por município | tabela; barras empilhadas |
| 12. Desigualdade interna | P90/P10, Gini e Theil do índice dentro de cada município | tabela; gráfico ordenado |
| 13. Comparação com a referência | Spearman com a referência, setores que mudam de faixa (matriz de contingência), municípios mais afetados | tabela; matriz; figura |

### 2.5 O motor

- `scripts/eda_versoes.py <pasta>`: lê o `config.json` da versão, monta a base, roda os
  blocos marcados e grava `tabelas/`, `figuras/` e `catalogo.csv`. **Um motor só para
  todas as versões**; o que muda é o `config.json`.
- `scripts/gerar_deck_versao.js <pasta>`: lê `catalogo.csv`, as tabelas e um
  `textos.json` da versão e monta o deck. **Um gerador só para todos os decks.**
- `scripts/verificar_versao.py <pasta>`: as conferências da seção 3, num comando só.
- `analises_exploratorias/_modelos/textos_blocos.json`: para cada bloco e cada tipo de
  tabela ou figura, o título-modelo, o "Como ler" e a nota longa do apresentador, com
  campos que o gerador preenche (`{indicador}`, `{n}`, `{mediana}`…). Escrito uma vez, no
  lote 0a, e reaproveitado por todas as versões.
- `scripts/gerar_catalogo_analises.py` passa a incluir `analises_exploratorias/*/catalogo.csv`
  e gera o `Catalogo_Mestre.xlsx`.
- Testes em `tests/test_eda_versoes.py`: o `00_referencia` reproduz os números já
  publicados (descritivas da 2ª rodada, AUC e n da referência do NB05) até a 4ª casa.

### 2.6 O deck de cada versão

Extenso e autoexplicativo: quem não estava na reunião precisa entender sozinho.

1. Capa: nome da versão, a pergunta que ela responde, data, n de setores.
2. "O que muda nesta versão": comparação lado a lado com a referência.
3. Recorte e n (bloco 1).
4. Sumário dos blocos.
5. Para cada bloco: um slide de abertura e, **para cada tabela e cada figura**, um slide
   com:
   - título que afirma o achado (não "Tabela 3", e sim o que ela mostra);
   - a figura ou tabela;
   - **"Como ler"**: uma a duas linhas sobre o que está em cada eixo ou coluna;
   - **"O que mostra"**: os números que importam, puxados do CSV;
   - o ID (T07, F12) no rodapé, o mesmo do catálogo;
   - nas **notas do apresentador**, a explicação longa, com os termos técnicos
     explicados do zero.
6. Síntese da versão: o que ela mostra de diferente da referência.
7. **Candidatos ao artigo**: a lista de tabelas e figuras desta versão, com os IDs, para
   marcar no catálogo.
8. Limitações e parâmetros exploratórios usados.
9. Apêndice: dicionário dos indicadores da versão (o que mede, numerador, denominador).

Tabela grande demais para um slide vai paginada (vários slides), nunca com fonte
ilegível. Tamanho esperado: de 40 a 90 slides por versão.

---

## 3. Verificação (em todo lote, pelo `verificar_versao.py`)

1. `pytest` passa.
2. Cada deck é convertido para PDF (`soffice --headless --convert-to pdf`) e conferido
   página a página numa folha de contato: nenhum texto saindo da caixa, nenhuma figura
   cortada.
3. Script de conferência: todo número citado em "O que mostra" existe no CSV do mesmo ID.
4. Varredura dos decks e READMEs por palavras proibidas (seção 0.2).
5. `catalogo.csv` tem uma linha para cada arquivo de `tabelas/` e `figuras/`, e cada
   linha aponta um slide que existe.

---

## 4. Os lotes

Cada linha é **uma sessão**. O teto conta todas as chamadas de ferramenta da sessão.

| Lote | O que faz | Teto de chamadas | Para ao fim e mostra |
|---|---|---:|---|
| **0a — Motor** | `eda_versoes.py` (blocos 1–13), `verificar_versao.py`, `textos_blocos.json`, `tests/test_eda_versoes.py`, `ESTADO.md` | 40 | testes passando e o resumo do motor |
| **0b — Piloto** | `gerar_deck_versao.js` e o `00_referencia` completo; uma folha de contato | 35 | o deck piloto: **Pedro aprova formato e tamanho antes de qualquer outra versão** |
| 1a | A1, A2, A3 | 30 | os decks e o que cada recorte muda |
| 1b | A4, A5, A6 | 30 | idem |
| 2a | B1, B2, B3, B4 | 30 | idem |
| 2b | B5, B6, B7, B8 | 30 | idem |
| 3a | C1, C2, C3 | 30 | idem |
| 3b | C4, C5, C6 | 30 | idem |
| 4a — Parâmetros | Mostrar a Pedro os parâmetros de D2 e D4 (seção 2.3), sem rodar nada | 10 | **esperar o OK** |
| 4b | D1, D2, D3 | 30 | os decks |
| 4c | D4, D5 | 25 | os decks |
| 5a | E1, E2, E3 | 30 | os decks |
| 5b | E4, E5, E6 | 30 | os decks |
| **6 — Síntese** | `00_sintese`, `Catalogo_Mestre.xlsx`, `README.md` da pasta, `X_bloqueadas.md` | 35 | a pasta inteira pronta para a escolha |

São 14 sessões. A conta para um lote de três versões: 3 versões × 3 comandos = 9
chamadas, mais as de escrever os três `textos.json` e os `config.json`, mais o estado —
cabe em 30 com folga para uma correção por versão.

## O que nunca fazer

- Escolher uma versão, um índice ou uma tabela para o artigo.
- Reescrever indicador, fatorial ou critério que já existe no código.
- Digitar número no gerador de deck.
- Sobrescrever qualquer arquivo de `banco_de_dados/eda/` ou de `docs/Apresentacoes_IVS/`.
- Encadear dois lotes na mesma sessão, ou começar um lote sem Pedro mandar.
- Passar do teto de chamadas do lote.
- Baixar dado novo (malha, óbitos) sem pedido explícito.
