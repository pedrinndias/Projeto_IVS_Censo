# Prompt de execução — fatorial multiversão e as apresentações dos indicadores e do IVS (out/2026)

**Base acordada com a orientadora:** `relatorio_parcial_raic/Relatorio_Parcial_RAIC_2026_Pedro_corrigido.pdf`
(os 12 indicadores do Quadro 2, a Tabela 1 e a Figura 1). Tudo aqui dá sequência a esse documento.
**Desenho da análise:** saiu de um council de 5 conselheiros e 5 revisões (22/10/2026), resumido na seção 1.
**Desenho das apresentações:** pedido do Pedro (22/10/2026), seção 1.2.
**Como usar:** uma fase por sessão. Diga: *"Execute a FASE N. Leia primeiro
`docs/prompts/estado_fatorial_multiversao_2026-10.md`."*

| Fase | O quê | Você recebe | Teto de chamadas | Modelo |
|---|---|---|---:|---|
| 0 | Pré-registro, mensagem à orientadora, correção do índice municipal | Estado com as 5 perguntas e regras; mensagem pronta; 1 correção com teste | 20 | Opus |
| 1 | Camada 1 — os 4.017 subconjuntos das 12 variáveis | Tabela de 12 linhas (efeito de cada variável) + 1 figura | 30 | Sonnet |
| 2 | Camada 2 — eixos de método sobre 13 conjuntos | Uma tabela por pergunta: "tanto faz" ou "decisão necessária, custo X" | 35 | Sonnet |
| 3 | Camada 3 — finalistas e o IVS proposto | Estabilidade, replicação, faixas, IVS por setor | 25 | Sonnet |
| 4 | Números e figuras das apresentações | `Fatorial_Multiversao_numeros.xlsx` + figuras + `numeros.json` | 35 | Sonnet |
| 5 | **Piloto:** o deck da renda | 1 PowerPoint (~20 slides) para aprovar o layout | 30 | Opus |
| 6 | Os outros 11 decks de indicador | 11 PowerPoints no layout aprovado | 30 | Sonnet |
| 7 | O deck final — análise fatorial e o IVS | 1 PowerPoint (~60–70 slides) | 40 | Opus |

**Pare ao fim de cada fase**, grave o estado e mostre o resultado ao Pedro. Nenhuma fase começa a
seguinte sozinha.

---

## 1. O pedido e a leitura adotada

### 1.1 A análise — nas palavras do Pedro (22/10/2026)

1. "uma nova análise fatorial com diversas versões para serem analisadas e estudadas";
2. "versionamentos já anteriormente solicitados pela professora orientadora: sem rotação,
   com Varimax ou com promax";
3. "versionamento com e sem variáveis dentro das 12 apontadas, ou seja as versões estão
   escalando de forma exponencial".

### 1.2 As apresentações — nas palavras do Pedro (22/10/2026)

> "Após a análise fatorial quero uma apresentação rica, com suas matrizes, análises descritivas
> de cada indicador, quero uma apresentação extensa e descritiva individual de cada indicador e
> uma final reunindo os resultados e apontando o índice do IVS."

**Leituras adotadas** (o Pedro não respondeu às três perguntas de 22/10; valem os padrões
propostos, até ele dizer outra coisa):
- **12 arquivos separados**, um por indicador, mais **1 final**;
- **idosos e crianças têm deck próprio**, como os outros 10, mesmo fora do índice — são o tema
  do ELSI;
- **piloto: a renda**, o indicador com mais análises (critério de outlier, setor extremo, três
  versões).

### 1.3 O que as rodadas anteriores ensinaram (e este prompt evita)

| Erro passado | Onde | Como este prompt evita |
|---|---|---|
| Grades de 324 e de 108 geraram material, não decisão | NB05, `versoes_fatorial/` | Toda análise responde a uma das perguntas P1–P5; o deck final termina nas decisões |
| O critério de estabilidade favorecia os pesos fixos (amplitude zero por construção) | NB05, achado 4 | A estabilidade é incerteza **reportada**, nunca critério de escolha |
| A AUC contra favela foi lida como validação dos pesos (a renda sozinha separa melhor: 0,88 × 0,81) | Revisão geral, NB4-02 | A AUC aparece só como descrição, sempre ao lado da renda sozinha |
| Bootstrap com setores independentes subestimou a incerteza | NB4-01 | Incerteza só por município (deixar um de fora) e por metades de municípios |
| O banheiro graduado tirou 29% da base sem decisão | NB05, achado 9 | Cada versão informa a base perdida **e o perfil** dos setores perdidos |
| A divisão do peso na promax mudava de lado conforme a matriz (65,8 × 59,6) | NB4-03 | Padrão e estrutura são reportadas sempre juntas |
| Município sem variação ganhava IVS 0 e faixa "muito elevado" nos quartis | `ie.indice`, `ie.faixas` | Corrigido na Fase 0, com teste |
| Números digitados à mão em decks | `scripts/README.md` | Todo número sai do `numeros.json`; verificador em cada fase |

### 1.4 A análise em três camadas (decisão do council)

- **Camada 1** enumera **inteiros** os 4.017 subconjuntos das 12 (pedido 3), com **um** método e
  só diagnósticos de estrutura. O resumo é uma tabela de 12 linhas: o que cada variável faz com
  a análise quando entra ou sai.
- **Camada 2** cruza **todos** os eixos de método da orientadora (pedido 2) sobre 13 conjuntos:
  o núcleo e o núcleo com uma variável a mais ou a menos.
- **Camada 3** aprofunda só os finalistas e calcula o **IVS proposto**.

---

## 2. Regras que valem para todas as fases

### 2.1 Código: `/ponytail`

- **Antes de escrever código, invoque `/ponytail`** (nível full). O menor código que resolve,
  reaproveitando o que existe:
  - fatorial: `rodar_cenario`, `fatoracao_eixo_principal`, `rotacao_promax`,
    `comunalidades_obliquas`, `kmo` (`src/ivs_censo/fatorial.py`);
  - pesos, elegibilidade, índice, faixas, AUC, estabilidade: importar de
    `scripts/ivs_especificacoes.py` (`reparticoes`, `elegibilidade`, `indice`, `faixas`,
    `auc_municipal`, `estabilidade`), como `scripts/versoes_fatorial.py` faz;
  - base: `fa.carregar()` de `scripts/fatorial_ampliada.py`; indicadores: `calcular_indicadores`;
  - descritivas, Gini, Theil, porte, Brasil × 70: as funções de `scripts/eda_versoes.py`
    (`descritivas`, `tab_desc`, `gini`, `theil`, `brasil_x_70`); base nacional em
    `banco_de_dados/nacional/Base_Brasil_Censo2022.db` (se faltar: `scripts/base_nacional_versoes.py`, ~2 min);
  - decks: `scripts/deck_comum.js` (`criarDeck`), no padrão de `scripts/gerar_relatorio_descritivo.js`
    (trava de sobrescrita por `gerado.sha256`, ID no canto, fonte nas notas);
  - folha de contato: `soffice --headless --convert-to pdf` + `scripts/folha_contato.swift`.
- **Quatro arquivos novos, não mais:**
  - `scripts/fatorial_multiversao.py` — o motor das Fases 1 a 3 (`--camada 1|2|3`);
  - `scripts/dados_apresentacoes_multiversao.py` — Fase 4 (`numeros.json`, figuras, `.xlsx`);
  - `scripts/gerar_decks_multiversao.js` — Fases 5 a 7 (`<indicador>` ou `final`);
  - `scripts/verificar_multiversao.py` — conferência de todas as fases (`--fase N`);
  - mais `tests/test_fatorial_multiversao.py` (um teste por função nova não trivial).
- **Sem dependência nova.** O `requirements.txt` e o `package.json` já têm o necessário.

### 2.2 Verificação: `/ponytail-review`

Ao fim de **cada fase**, antes de gravar o estado:
1. `./.venv/bin/python -m pytest tests/ -q` verde;
2. `./.venv/bin/python scripts/verificar_multiversao.py --fase N` verde;
3. **invoque `/ponytail-review` sobre o diff da fase** e corrija o que ele apontar como erro;
   o que for só estilo, registre no estado e siga;
4. nas fases de deck (5 a 7), a folha de contato vista página a página.

### 2.3 Regras de conteúdo

- **Nenhum número digitado à mão.** Todo número de slide sai do `numeros.json`, que sai dos CSVs
  das Fases 1 a 3 ou do `.db` da entrega.
- **Não decidir pela orientadora.** Quando houver duas leituras, rode as duas, registre a
  pergunta no estado e siga com o padrão da seção 3.
- **Base comum para comparar.** A fatorial roda na amostra própria de cada versão; as
  comparações entre versões usam a amostra comum.
- **Comparação dentro do município.** Spearman e troca de faixa são calculados dentro de cada
  município (mediana entre os que têm ≥ 30 setores), além do global.
- **Saídas da análise:** `banco_de_dados/eda/fatorial_multiversao/`.
  **Apresentações:** `apresentacoes_multiversao/` (seção 4).

---

## 3. Pré-registro (a Fase 0 grava; ninguém muda depois da Fase 1)

### 3.1 As cinco perguntas — cada análise existe para responder uma delas

| # | Pergunta à orientadora | Respondida por | Padrão enquanto não houver resposta |
|---|---|---|---|
| P1 | O IVS é construto **reflexivo**, índice **formativo** ou **híbrido** (fatorial dentro de cada bloco; divisão entre blocos por decisão)? | Relatório NB04 §5 + Camada 2 | Híbrido |
| P2 | Quais das 12 entram no índice? | Camada 1 + Camada 2 (núcleo ± 1) | Os 7 do Quadro 1 |
| P3 | Como tratar o sigilo do analfabetismo (16% dos setores, nos de renda alta)? | Camada 2, eixo sigilo | Ausente, com as duas imputações como sensibilidade |
| P4 | Que régua: min-max municipal, min-max global ou postos no município (trata zeros e assimetria, como o relatório promete)? | Camada 2, eixo normalização | Min-max municipal, como o relatório diz |
| P5 | Sem rotação, Varimax ou promax, e qual método de peso? | Camada 2, eixos rotação × peso | Promax com 60/40 |

O **IVS proposto** (Fase 3 e deck final) é o da combinação dos cinco padrões. Ele aparece sempre
marcado como **proposta**, com o custo de cada alternativa ao lado.

### 3.2 Critérios fixados antes de rodar

- **Elegibilidade** (os mesmos do NB05): KMO ≥ 0,70; MSA mínimo ≥ 0,50; comunalidade mínima
  ≥ 0,30; carga máxima mínima ≥ 0,40. Registrar quantas versões falham **só** pela
  comunalidade: dentro do município a água cai a 0,29 (medido em 22/10).
- **Regra de equivalência:** duas opções de um eixo são equivalentes se o Spearman do índice,
  dentro do município, for ≥ 0,95 **e** menos de 10% dos setores trocarem de faixa. Todas
  equivalentes → "tanto faz; vale o argumento conceitual". Senão → "decisão necessária", com o
  custo medido.
- **Perda de base:** versão que perde mais de 5% dos 104.108 setores é marcada, e o perfil dos
  setores perdidos (região, renda mediana, % FCU) é descrito.
- **Semente:** 42 em tudo.

### 3.3 As 12 variáveis

| Código no deck | Coluna | Dimensão | No IVS (Quadro 1)? |
|---|---|---|---|
| AGU | `pct_agua_inad` | Saneamento | sim |
| ESG | `pct_esgoto_inad` | Saneamento | sim |
| LIX | `pct_lixo_inad` | Saneamento | sim |
| MOR | `razao_moradores` | Socioeconômica | sim |
| ANA | `pct_analfab` | Socioeconômica | sim |
| REN | `renda_inv` (renda sem o extremo, invertida) | Socioeconômica | sim |
| PPI | `pct_raca_pretpardind` | Socioeconômica | sim |
| CAN | `pct_sem_agua_canalizada` | Saneamento | não |
| BAN | `pct_sem_banheiro` | Saneamento | não |
| MNC | `pct_moradia_nao_convencional` | Morfologia | não |
| IDO | `pct_idoso_60mais` | Demografia | não |
| CRI | `pct_pop_0a14` | Demografia | não |

Todas existem no `.db` da entrega (conferido em 22/10). Só a renda é invertida. Idosos ×
crianças correlacionam −0,79 por construção (mesmo denominador): subconjunto com as duas leva a
marca `demografia_dupla`. Nos decks, a renda aparece em R$ (original), e só a análise fatorial
usa a invertida.

---

## FASE 0 — Pré-registro e correção (teto: 20 chamadas)

1. Criar `docs/prompts/estado_fatorial_multiversao_2026-10.md` com o modelo da seção 6.
2. Copiar a seção 3 para o estado, com a data. Ela não muda depois da Fase 1.
3. **Corrigir o índice municipal** em `scripts/ivs_especificacoes.py` (`/ponytail`: a causa, uma vez,
   no código compartilhado):
   - `indice`: componente constante no município continua contribuindo 0, mas **município sem
     nenhuma variação** fica `NaN` (hoje vira 0,0000);
   - `faixas`, regra de quartis: grupo com menos de 4 setores fica −1 (hoje um setor único vira
     "muito elevado");
   - antes de editar, `grep -rn "ie.indice\|ie.faixas\|indice_versao\|def indice\|def faixas" scripts tests`
     e conferir cada chamador;
   - um teste para cada caso em `tests/test_ivs_especificacoes.py`;
   - **não regerar** NB05, versões nem análises exploratórias; só registrar o que mudaria.
4. Redigir a mensagem única à orientadora com P1–P5 e os padrões, para o Pedro enviar.
5. Seção 2.2 (pytest, `/ponytail-review`). Parar.

## FASE 1 — Camada 1: os 4.017 subconjuntos (teto: 30 chamadas)

**Responde P2.** É a explosão pedida, enumerada inteira.

1. Todos os subconjuntos das 12 com 3 ou mais variáveis (4.017). Para cada um, uma fatorial:
   `rodar_cenario(X, k=2, metodo='spearman', com_horn=True, extracao='eixo_principal')`, em
   **duas réguas**: postos globais e postos dentro do município. Custo medido: 0,15 s por rodada;
   ~20 min no total. Rodar em segundo plano.
2. `camada1_subconjuntos.csv` (uma linha por subconjunto e régua): 12 colunas 0/1, n, % do
   recorte, KMO, MSA mínimo e qual, Kaiser, Horn, comunalidade mínima e qual, Φ da promax,
   elegível, `demografia_dupla`.
3. **O resumo** — `camada1_efeito_variavel.csv`, 12 linhas × 2 réguas: para cada variável,
   comparar os pares de subconjuntos que diferem só nela: variação mediana do KMO, da %
   elegível e do n, e a comunalidade mediana da própria variável.
4. `camada1_cargas_12.csv`: a fatorial das 12 juntas (cargas sem rotação, Varimax, promax padrão
   e estrutura, Φ, comunalidades, MSA) — vai para o slide 16 de cada deck.
5. Registrar no estado, sem escolher nada: variáveis que (a) derrubam a elegibilidade em mais da
   metade dos pares, (b) custam mais de 5% da base, (c) têm comunalidade mediana < 0,30.
6. Seção 2.2. Parar e mostrar a tabela de 12 linhas.

## FASE 2 — Camada 2: os eixos de método (teto: 35 chamadas)

**Responde P3, P4 e P5; confirma P2.**

**Conjuntos (13):** o núcleo (os 7 do Quadro 1); o núcleo menos cada uma das 7; o núcleo mais
cada um dos 5 complementares. Um 14º só se o Pedro pedir depois de ver a Fase 1.

**Eixos, em cada conjunto:**
- rotação × peso, os 9 do NB05 (`ie.reparticoes`): sem rotação; Varimax com SS, 50/50, 60/40;
  promax com SS da padrão, SS da estrutura, comunalidades, 50/50, 60/40;
- normalização (3): min-max municipal, min-max global, postos no município;
- sigilo do analfabetismo, **só nos conjuntos com analfabetismo**: ausente; imputado com o
  limite inferior (um analfabeto no setor, o cálculo que deu 3,14% na seção VI do relatório —
  achar com `grep -rn "3,14\|3.14\|limite inferior" scripts docs/relatorios relatorio_parcial_raic`);
  imputado com zero.

Total ≈ 13 × 9 × 3 = 351 especificações, mais o eixo sigilo.

1. `camada2_especificacoes.csv`: elegibilidade, peso das duas dimensões (padrão e estrutura),
   peso de cada variável, n, AUC descritiva contra FCU e AUC da renda sozinha na mesma base.
2. `camada2_efeito_eixo.csv`: para cada eixo, com os outros na referência (núcleo, promax,
   60/40, municipal, ausente), Spearman dentro do município e % de troca de faixa entre as
   opções; a regra da seção 3.2 escreve "equivalentes" ou "decisão necessária, custo X".
3. Seção 2.2. Parar e mostrar a tabela por pergunta.

## FASE 3 — Camada 3: finalistas e o IVS proposto (teto: 25 chamadas)

Finalistas = o **IVS proposto** (os cinco padrões) + no máximo uma alternativa por eixo marcado
"decisão necessária" (no máximo 6 ao todo). Em cada um:
1. estabilidade deixando um município de fora (`ie.estabilidade`, 70 rodadas): amplitude do peso
   de cada dimensão e de cada variável — **reportar, não ordenar**;
2. replicação: duas metades dos municípios (semente 42, estratificada por região); congruência
   de Tucker entre as cargas das metades (função nova, com teste);
3. faixas pela regra do IVS-BH e por quartis, já com a correção da Fase 0;
4. perfil dos setores perdidos, se a versão perde mais de 5%.

Saídas: `camada3_finalistas.csv`, `camada3_estabilidade.csv`, `camada3_replicacao.csv` e
`ivs_proposto_por_setor.csv` (CD_SETOR, município, região, FCU, população, 60+, IVS, faixa IVS-BH,
faixa quartis, e o IVS de cada finalista). Seção 2.2. Parar.

## FASE 4 — Números e figuras das apresentações (teto: 35 chamadas)

`scripts/dados_apresentacoes_multiversao.py` lê os CSVs das Fases 1 a 3 e o `.db` e grava em
`apresentacoes_multiversao/`:
- `dados/numeros.json` — um bloco por slide, com ID, título, textos, tabela e fonte;
- `figuras/` — PNG de cada figura (paleta e fontes de `relatorio_descritivo/figuras/`);
- `Fatorial_Multiversao_numeros.xlsx` — uma aba por deck, cada tabela com o ID do slide.

**Os textos são frases factuais com o número dentro**, montadas por modelo e preenchidas pelo
script (como no relatório descritivo). Nada de "interessante", "notável", "significativo" sem
teste. O verificador da fase confere que todo número do JSON existe no CSV citado.
Seção 2.2. Parar.

## FASE 5 — Piloto: o deck da renda (teto: 30 chamadas)

1. `node scripts/gerar_decks_multiversao.js REN` → `apresentacoes_multiversao/fichas/REN_Renda.pptx`,
   com a estrutura da seção 4.1.
2. Folha de contato; verificador; seção 2.2.
3. **Parar e esperar o Pedro aprovar o layout.** Ajustes pedidos entram no gerador, não no
   `.pptx`. Só depois da aprovação a Fase 6 começa.

## FASE 6 — Os outros 11 decks (teto: 30 chamadas)

`node scripts/gerar_decks_multiversao.js todos` (os 11 restantes, no layout aprovado).
Folha de contato de cada um, verificador, seção 2.2. Slide que não se aplica ao indicador (ex.:
"valores extremos" na razão de moradores, se não houver) **fica no deck** com a frase "não se
aplica: <motivo>", para a numeração continuar igual em todos. Parar.

## FASE 7 — O deck final (teto: 40 chamadas)

`node scripts/gerar_decks_multiversao.js final` →
`apresentacoes_multiversao/Analise_Fatorial_e_IVS_2026-10.pptx`, com a estrutura da seção 4.2.
Folha de contato, verificador, seção 2.2. Parar.

---

## 4. As apresentações

**Padrão em todos os decks** (o do relatório descritivo aprovado em 07/10):
- 16:9, `deck_comum.js`; uma mensagem por slide; o **título afirma** o achado;
- ID no canto superior direito; **fonte só nas notas do apresentador**;
- tabelas **nativas e editáveis**; tabela de 70 municípios vai inteira no apêndice e, no corpo,
  com os 10 maiores e os 10 menores;
- **trava contra sobrescrita** (`gerado.sha256`, como em `gerar_relatorio_descritivo.js`): se o
  Pedro editar um deck, o gerador recusa sobrescrever sem `--sobrescrever`;
- o IVS sempre marcado como **proposta**.

### 4.1 Os 12 decks de indicador — `apresentacoes_multiversao/fichas/<COD>_<Nome>.pptx`

Mesma estrutura e mesmos IDs em todos (`<COD>-01` a `<COD>-20`), para comparar um com o outro.

| ID | Slide | Conteúdo | Fonte |
|---|---|---|---|
| 01 | Capa | Nome, o que mede, dimensão, se está no IVS | Quadro 2 |
| 02 | Como é calculado | Variáveis do Censo, numerador ÷ denominador, arquivo do IBGE | `indicadores.py`, `fontes.py` |
| 03 | Adequações ao Censo 2022 | Ex.: caçamba, 15+, setor extremo da renda | Relatório corrigido, seção IV |
| 04 | Cobertura e sigilo | Setores com o dado e o **perfil dos que não têm** (região, renda mediana, FCU) | `.db` |
| 05 | Estatísticas descritivas | n, média, mediana, DP, p25, p75, máx, assimetria, % de zeros | `.db` |
| 06 | Distribuição | Histograma, boxplot e densidade | `.db` |
| 07 | Por região | Tabela das 5 regiões + boxplot | `.db` |
| 08 | Por porte | Até 100 mil · 100–500 mil · mais de 500 mil | `.db` |
| 09 | Os 70 municípios (1) | Mediana por município: os 10 maiores e os 10 menores | `.db` |
| 10 | Os 70 municípios (2) | Figura com os 70 ordenados | `.db` |
| 11 | Desigualdade dentro das cidades | Amplitude interquartil e Gini por município | `.db` |
| 12 | Favela × fora da favela | Comparação das descritivas | `.db` |
| 13 | Brasil × 70 municípios | Média, mediana e % de zeros nos dois | Base nacional |
| 14 | Valores extremos | Quantos, onde, e o que se decidiu | `.db`, `renda.py` |
| 15 | Correlação com os outros 11 | Spearman no conjunto e dentro dos municípios, lado a lado | Fase 1 |
| 16 | Na análise fatorial das 12 | Carga (sem rotação, Varimax, promax), comunalidade, MSA, nas duas réguas | `camada1_cargas_12.csv` |
| 17 | Entrar ou sair do índice | O efeito dele nas 4.017 combinações | `camada1_efeito_variavel.csv` |
| 18 | Peso no índice | Nos finalistas, e quanto varia ao tirar um município | Fase 3 |
| 19 | Síntese | 4 a 5 frases factuais e a proposta: entra ou não entra | Fases 1 a 3 |
| 20 | Apêndice | Tabela dos 70 municípios inteira | `.db` |

Idosos e crianças: os slides 17 e 18 dizem "fora do índice por ser demografia; aparece aqui como
descrição" e mostram a relação com o IVS proposto (Spearman e média por faixa).

### 4.2 O deck final — `apresentacoes_multiversao/Analise_Fatorial_e_IVS_2026-10.pptx`

IDs `FIN-01` em diante. Cerca de 60 a 70 slides.

| Parte | Slides | Conteúdo |
|---|---|---|
| 1. Ponto de partida | ~5 | O relatório corrigido; os 12 indicadores; a base (109.032 → 104.108); painel descritivo dos 12 (Tabela 1 atualizada); o que aprendemos com as análises anteriores (tabela da seção 1.3) |
| 2. As matrizes | ~8 | Spearman 12×12 no conjunto e dentro dos municípios (mapa de calor + tabela); a diferença entre as duas; matriz anti-imagem com MSA; KMO e Bartlett; determinante |
| 3. Quantos fatores | ~4 | Autovalores, scree plot, Horn e Kaiser, nas duas réguas |
| 4. A explosão de versões | ~8 | Como as 4.017 foram rodadas; o efeito de cada variável (tabela de 12 linhas + figura); a distribuição do KMO e da elegibilidade; as 13 versões da Camada 2 |
| 5. Os métodos | ~8 | Um slide por eixo (rotação × peso, normalização, sigilo): "tanto faz" ou "decisão necessária, custo X" |
| 6. A solução proposta | ~8 | Matriz de cargas sem rotação, Varimax, promax padrão e promax estrutura; Φ; comunalidades; plano fatorial; variância explicada |
| 7. Os pesos | ~6 | Por dimensão e por variável; empírico × 60/40; estabilidade por município; replicação entre metades |
| 8. **O IVS proposto** | ~12 | Distribuição; as 4 faixas pela regra do IVS-BH e por quartis; setores e **população** por faixa; **idosos por faixa**; favelas por faixa; por região; por porte; os 70 municípios (corpo: 10 + 10; apêndice: todos); os finalistas lado a lado |
| 9. Sensibilidade | ~4 | Quantos setores mudam de faixa com cada alternativa; concordância entre os finalistas |
| 10. Fechamento | ~5 | As decisões para a professora (P1–P5, uma linha cada, com a recomendação marcada); limitações; próximos passos (mapas no QGIS, I de Moran) |
| Apêndice | ~6 | Matrizes completas, tabela dos 70 municípios, as 351 especificações resumidas |

---

## 5. O que NÃO fazer

- Não rodar estabilidade nos 4.017 (seriam ~281 mil fatoriais).
- Não ordenar versões por estabilidade nem por AUC.
- Não fazer uma ficha por versão (o erro das 108).
- Não regerar as análises de outubro (`analises_exploratorias/`, `versoes_fatorial/`) nem o NB05.
- Não alterar o relatório parcial nem a apresentação do RAIC.
- Não editar um `.pptx` à mão para corrigir: corrigir o gerador e regerar.

---

## 6. Modelo do arquivo de estado

```markdown
# Estado — fatorial multiversão e apresentações (out/2026)

Prompt: `docs/prompts/prompt_fatorial_multiversao_2026-10.md`

## Situação: fase N concluída — próxima: fase N+1

## Pré-registro (gravado em DD/MM/2026; não muda depois da Fase 1)
(seção 3 do prompt, copiada)

## Respostas da orientadora
| Pergunta | Resposta | Data |
|---|---|---|
| P1 … P5 | aguardando | — |

## Decisões do Pedro
| Ponto | Resposta | Data |
|---|---|---|
| 12 arquivos + 1 final; idosos e crianças com deck; piloto na renda | padrão proposto, sem resposta | 22/10/2026 |

## Achados do /ponytail-review por fase
| Fase | Corrigido | Registrado (só estilo) |
|---|---|---|

## Histórico
| Fase | Data | Resultado | Chamadas |
|---|---|---|---:|
```
