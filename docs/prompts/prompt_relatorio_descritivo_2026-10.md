# Prompt — Relatório descritivo do andamento (outubro/2026)

Uma apresentação em PowerPoint, em **formato de relatório descritivo**, para a orientadora
comparar os resultados do Pedro com os dela. Ela tem quatro partes:
1. as demandas de setembro e como cada uma foi coberta;
2. a descritiva de cada indicador, um por slide;
3. a descritiva da análise fatorial, uma medida por slide;
4. o que a orientadora pediu especificamente da fatorial.

A interpretação do pedido está em `relatorio_descritivo/INTERPRETACAO.md`, com os requisitos
R1–R14 e as leituras L1–L7. **Este prompt não a repete; lê-la é obrigatório.**

---

## Como usar

- **Um lote por sessão nova, em Sonnet.** Na primeira mensagem, cole só isto:
  *"Execute o LOTE N de `docs/prompts/prompt_relatorio_descritivo_2026-10.md`. Leia primeiro
  `relatorio_descritivo/ESTADO.md`."*
- **O que cada sessão lê:**
  - o lote 0 lê `ESTADO.md`, `INTERPRETACAO.md` e as seções 0 a 3 deste prompt;
  - os lotes seguintes leem `ESTADO.md`, `CONSTRUCAO.md`, a seção 0 e o bloco do próprio lote;
  - uma correção lê `ESTADO.md`, `CORRECOES.md`, `CONSTRUCAO.md` e a seção 5.
- **Abra a sessão nesta mesma pasta**, não pelo botão de tarefa: o botão cria uma cópia a partir
  do último commit, e `analises_exploratorias/` e `relatorio_descritivo/` ainda não estão
  commitadas.
- **Cada lote termina parado.** O Pedro revisa o que saiu e manda correções (lote C) ou
  libera o lote seguinte. Nenhum lote começa o próximo.

---

## 0. Regras

### 0.1 Orçamento de tokens (obrigatório)

1. Cada lote tem um teto de chamadas de ferramenta (tabela da seção 4). Ao chegar a 80% do
   teto, grave o estado e pare, mesmo no meio.
2. Nada de subagentes, workflows ou skills.
3. Toda saída de comando vai truncada (`| head -60`). Nunca imprima um CSV inteiro.
4. Não abra `.pptx` nem `.png` gerados para conferir. Quem confere é o verificador
   (seção 3). A **única** exceção é uma folha de contato por lote, só dos slides novos (§3.3).
5. Dois erros iguais seguidos: pare e reporte.
6. Não releia nada que o `ESTADO.md` ou o `CONSTRUCAO.md` já registram.
7. O relatório de fim de lote tem no máximo 15 linhas e lista os IDs dos slides criados ou
   alterados.

### 0.2 Regras contra alucinação (valem para todo slide)

1. **Nenhum número digitado à mão.** O gerador JS só lê `relatorio_descritivo/dados/numeros.json`.
   Esse arquivo sai de `scripts/dados_relatorio_descritivo.py`, que só lê os CSVs e o `.db` da
   seção 1.
2. **Todo slide tem um ID estável** no canto superior direito (seção 2) e uma linha "Fonte:"
   com o arquivo e a coluna de onde saem os números.
3. **O texto do slide é factual.** As frases "O que mostra" são modelos preenchidos com os
   números do próprio slide. Exemplo: *"Metade dos setores tem até {mediana}; um em cada
   quatro tem mais de {p75}; {pct_zeros} dos setores têm valor zero."*
   - Não use causa nem adjetivo de juízo ("alto", "preocupante", "expressivo").
   - Não cite outro indicador.
4. **Interpretação só com fonte.** Uma frase interpretativa precisa citar um documento do
   projeto no rodapé. Sem documento, use a caixa "[Pedro: interpretar]".
5. **O que não se sabe fica escrito "A CONFERIR".** Nunca preencha por suposição.
6. **Redação das demandas:** use a do registro, com o selo "redação do registro" (leitura L6).
7. **Na Parte DS, nenhum gráfico ou tabela põe dois indicadores juntos** (requisito R5). Isso
   inclui correlação, dispersão e boxplots lado a lado.
8. **A especificação do NB05 é "referência proposta"**, nunca "final" ou "escolhida". A escolha
   é da orientadora.
9. **Sem marcas de texto gerado.** Evite: "vale destacar", "é importante notar", "em suma",
   "robusto", "abrangente", emoji, travessão como enfeite.
10. **Commit só a pedido do Pedro**, e só com o nome dele: sem `Co-Authored-By`, sem linha de
    ferramenta.

---

## 1. Fatos verificados (não redescobrir)

**Ambiente**
- Use `./.venv/bin/python` (pandas 3, openpyxl, matplotlib; **sem scipy**). Os decks usam
  Node com `pptxgenjs` e `scripts/deck_comum.js` (`criarDeck(meta)`).
- Exemplo completo de uso: `scripts/gerar_deck_versao.js`.
- Formatadores pt-BR prontos em `scripts/eda_versoes.py`: `br`, `intbr` e `pctbr`.

**Demandas e o que contornamos**
- **As 11 demandas:** `docs/prompts/estado_demandas_2026-09.md`, linhas 16–26 (tabela: nº,
  demanda, fase, estado, onde está o resultado). Todas estão "concluída". A demanda 6 foi
  concluída com V00495; a versão graduada (V00237) foi feita depois, no NB05, Fase B.
- **Leituras adotadas e perguntas à orientadora:** mesmo arquivo, linhas 28–61 (6 perguntas e
  3 decisões de método). A seção "Decisões tomadas", linha 63, está **vazia**: não há registro
  de resposta dela. Isso entra como "A CONFERIR com o Pedro".
- **Desdobramentos do NB05:** `docs/prompts/estado_nb05_2026-09.md`, linhas 21–31 (itens 1–9).
- **Fontes dos contornos:** cite sempre arquivo e linha.
  - `estado_demandas_2026-09.md`: Perguntas (28–61), pendências das Fases 2, 3 e 4 (linhas
    288–306, 318–324 e 343–360);
  - `estado_nb05_2026-09.md`: Fases A e B;
  - `docs/relatorios/Apanhado_Analises_Exploratorias_2026-10.md`, §6 (armadilhas).
- **Deck que já cobre as demandas por tema:** `scripts/gerar_deck_demandas_setembro.js`. Os
  números e os textos dele já foram conferidos; **reaproveite os dados, não o layout**.

**Base e descritiva** (tudo já gerado e conferido na versão `00_referencia` das análises
exploratórias; **só leitura**, não regerar)
- **Base:** `banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db`, recorte
  urbano com `Dados_sig = OK`.
  - Funil: `analises_exploratorias/00_referencia/tabelas/T01_funil.csv` (109.032 → 106.347
    urbanos → … → 104.108).
  - Figura do funil: `figuras/F01_funil.png`.
- **Descritivas dos 31 indicadores:** `analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv`.
  - Colunas: `indicador, rotulo, n, media, dp, cv_pct, min, p10, p25, mediana, p75, p90, max,
    iq, assim, curt, pct_zeros`.
  - Proporções vêm em 0–1; `pct_zeros` já vem em %.
  - Perdas por indicador: `T02_perdas_por_indicador.csv` (`n_validos, n_faltantes, pct_faltantes`).
  - Por região: `T04`. Por município: `T05` (70 × 31).
- **Armadilha:** `banco_de_dados/eda/atualizada/descritivas_globais.csv` rotula `renda_media`,
  mas mede a renda sem o extremo. **Não use; use a T03.**
- **Definições** (numerador, denominador, códigos V, o que mede, se entra no IVS-7):
  `banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv` (separador `;`, `utf-8-sig`,
  28 linhas). As três que faltam:
  - `banheiro_graduado` = (1·V00236 + 2·V00237 + 3·V00238) / (3·V00001), em
    `scripts/ivs_especificacoes.py:58-62`;
  - `renda_media_sem_extremo` e `renda_media_mediana_mun`: docstrings em `src/ivs_censo/renda.py`.
- **Histograma por indicador:** monte a base com `ler_config('analises_exploratorias/00_referencia')`
  e `montar_base(cfg)` de `scripts/eda_versoes.py`. Não recalcule indicador nenhum.

**Fatorial**
- **Referência proposta do NB05** (n = 73.878, sete variáveis: os componentes sem o lixo,
  renda invertida, mais `banheiro_graduado`). Tabelas em `analises_exploratorias/00_referencia/tabelas/`:

  | Tabela | Conteúdo |
  |---|---|
  | `T19_adequacao_fatorial` | `medida, valor`, 9 linhas |
  | `T20_variaveis_cargas` | MSA; comunalidade e comunalidade oblíqua; cargas sem rotação, Varimax, promax padrão e promax estrutura, F1 e F2 |
  | `T21_autovalores` | `componente, autovalor, horn, pct_variancia, pct_acumulado` |
  | `T22_phi` | |
  | `T23_pesos` | `variavel, rotulo, dimensao, carga, peso_dimensao, peso` |
  | `T24_indice_descritivas` | |
  | `T25_faixas` | `regra, faixa, setores, pct` |
  | `T26_auc_e_elegibilidade` | |
  | `T27_auc_por_municipio` | |

  Figuras: `F22_sedimentacao_horn`, `F23_mapa_cargas`, `F24_histograma_por_faixa`, `F25_curva_roc`.
- **Linha de base do NB04** (IVS-7, n = 87.545): `banco_de_dados/eda/fatorial/nb04_*.csv`. Os
  números-chave estão em `banco_de_dados/eda/fatorial_ampliada/linha_de_base_nb04.csv`.
- **Demandas da fatorial** (3, 5 a 11): `banco_de_dados/eda/fatorial_ampliada/`. Arquivos:
  `cenarios.csv`, `cargas.csv`, `pesos.csv`, `autovalores.csv`, `comparacao_nao_chega_banheiro.csv`,
  `banheiro_particao.csv`, `correlacao_s6.csv`, `sensibilidade_municipios.csv`,
  `validacao_fcu.csv`. O `README.md` da pasta define os cenários S1–S7.
- **Grade do NB05:** `banco_de_dados/eda/ivs_especificacoes/` (`especificacoes.csv`,
  `avaliacao.csv`, `pesos.csv`, `referencia.csv`, `estabilidade.csv`, `acrescimo_renda.csv`).

---

## 2. A apresentação

### 2.1 Arquivos

**Processo** (requisito R12), em `relatorio_descritivo/`:
- `INTERPRETACAO.md` — o pedido e as leituras (já existe);
- `ESTADO.md` — o lote, a versão do deck e o histórico;
- `CONSTRUCAO.md` — a receita: comandos na ordem, o layout de cada tipo de slide, de onde sai
  cada parte;
- `CORRECOES.md` — o registro das correções;
- `dados/manifesto.csv` — uma linha por slide: `id, parte, titulo, requisito, fontes, figura,
  funcao_geradora, versao_criada, versao_alterada`;
- `dados/numeros.json` — todo número que aparece em slide, por ID.

**Entregas**, também em `relatorio_descritivo/`:
- `Relatorio_Descritivo_IVS_2026-10.pptx`;
- `Relatorio_Descritivo_numeros.xlsx` — números com precisão total, para a orientadora conferir
  célula a célula;
- `figuras/<ID>.png`.

**Scripts**, em `scripts/`:
- `dados_relatorio_descritivo.py` gera o JSON, o manifesto, as figuras e o xlsx;
- `gerar_relatorio_descritivo.js` monta o deck inteiro a partir do JSON e do manifesto, sempre
  do zero (nunca edita o `.pptx`);
- `verificar_relatorio_descritivo.py` é o verificador.

### 2.2 Abertura e fechamento

| ID | Slide |
|---|---|
| A01 | Capa: título, data, versão do deck (v1, v2…), base |
| A02 | Como ler. Os IDs. A linha Fonte. As três bases e qual parte usa cada uma (104.108 na DS; 73.878 na FA; 87.545 e os cenários na FP). O formato dos números |
| A03 | Roteiro: as quatro partes, com a faixa de IDs de cada uma |
| Z01 | Onde está cada número: ID → arquivo e coluna (resumo do manifesto) |
| Z02 | O que está em aberto: as perguntas sem resposta (DM15) e as escolhas de método da orientadora |

### 2.3 Parte DM — As demandas e como foram cobertas (R2, R3)

| ID | Slide |
|---|---|
| DM00 | Divisória |
| DM01 | Quadro-resumo: as 11 demandas (nº, redação do registro, estado, onde está, ID do slide de resultado) |
| DM02–DM12 | Uma demanda por slide, layout fixo (abaixo) |
| DM13 | Desdobramentos do NB05: os 9 itens. Selo: "origem: estado_nb05, não demanda direta da orientadora — A CONFERIR com o Pedro" (leitura L1) |
| DM14 | Tudo o que contornamos: obstáculo · saída adotada · efeito nos números · fonte (arquivo:linha) |
| DM15 | As perguntas enviadas à orientadora e ainda sem resposta registrada, com o padrão seguido em cada uma |

**Layout DM02–DM12** — cinco caixas, sempre na mesma posição:
1. **Pedido** — redação do registro.
2. **Como lemos** — leitura adotada; "uma leitura só" se não havia ambiguidade.
3. **O que foi feito** — até 3 linhas.
4. **O que contornamos** — obstáculo → saída, ou "nenhum contorno".
5. **Resultado** — um número ou uma tabela pequena, com o ID do slide em que o resultado
   aparece por inteiro (DS para as demandas 1 e 2; FP para as demais).

Rodapé: Fonte.

### 2.4 Parte DS — Descritiva dos indicadores, versão atual (R4, R5, R6, R10)

| ID | Slide |
|---|---|
| DS00 | Divisória |
| DS01 | A base: funil (T01, tabela e F01) |
| DS02 | Perdas por indicador (T02, só tabela) |
| DS03–DS33 | Um indicador por slide, 31 slides. Ordem: a da T03, com `renda_media_sem_extremo` e `renda_media_mediana_mun` logo depois de `renda_media` |
| DS34 | Por município e por região: só o aviso de que as tabelas estão no anexo xlsx (abas `Por_municipio` e `Por_regiao`). Sem gráfico |

**Layout DS03–DS33:**
- **Título:** o nome do indicador em português (`rotulo`).
- **Subtítulo:** "o que mede" (Quadro).
- **Etiqueta no topo:** a dimensão.
- **Caixa "Como é calculado":** numerador e denominador, com os códigos V; unidade; "Entra no
  IVS-7?"; "Entra na referência proposta?".
- **Tabela "Distribuição nos 104.108 setores":**
  - n válidos e faltantes (n e %);
  - média, DP, CV;
  - mín, P10, P25, mediana, P75, P90, máx;
  - % de zeros, assimetria.
- **Figura deste indicador só:** histograma com um boxplot horizontal fino em cima.
  - Com `pct_zeros` ≥ 50%: histograma dos valores positivos, e a legenda diz quantos são zero.
  - Arquivo: `figuras/DSxx.png`.
- **"O que mostra":** duas frases-modelo (§0.2, regra 3).
- **Notas do apresentador:** a função que gera o slide, a coluna no `.db` e como conferir.

### 2.5 Partes FA e FP — Fatorial (R7, R8)

**Parte FA** — descritiva da referência proposta (leitura L3). O primeiro slide traz o selo:
"especificação proposta no NB05; a escolha é da orientadora".

| ID | Slide | Fonte |
|---|---|---|
| FA00 | Divisória e a especificação: variáveis, rotação, pesos, normalização | `ESTADO.md` das análises exploratórias, receita |
| FA01 | A amostra: 73.878 setores; de onde sai e o que perde | T02 e T01 |
| FA02 | Matriz de correlação de entrada, 7 × 7, só tabela | **A CONFERIR:** qual correlação o `rodar_cenario` usa; ler a docstring em `src/ivs_censo/fatorial.py` |
| FA03 | Adequação: KMO, Bartlett e as demais linhas | T19 |
| FA04 | MSA e comunalidades por variável | T20 |
| FA05 | Autovalores e análise paralela de Horn | T21 e F22 |
| FA06 | Quantos fatores: Kaiser, Horn, retidos | T21 e T19 |
| FA07 | Cargas sem rotação | T20 |
| FA08 | Cargas Varimax | T20 |
| FA09 | Cargas promax: padrão e estrutura | T20 e F23 |
| FA10 | Correlação entre fatores (Φ) | T22 |
| FA11 | Pesos: da dimensão (60/40) e por variável | T23 |
| FA12 | O índice: descritivas e histograma | T24 e F24 |
| FA13 | As faixas pelas duas regras | T25 |
| FA14 | Validação contra FCU: AUC global e municipal | T26 e F25 |
| FA15 | AUC por município: distribuição das 70 AUCs; a lista vai no anexo | T27 |
| FA16 | Elegibilidade: os critérios e se a referência passa | T26 |

**Parte FP** — o que a orientadora pediu da fatorial. Um slide por pedido, em ordem de
demanda. Layout: **Pedido** (1 linha) · **Resultado** (tabela do CSV) · **O que mostra** (frase
factual) · **Fonte**. Aqui a comparação entre cenários é o próprio pedido, então pode.

| ID | Pedido |
|---|---|
| FP00 | Divisória |
| FP01 | Demanda 1 — renda com a mediana: o efeito das três rendas (`banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv` e grade do NB05) |
| FP02 | Demanda 3 — fatorial sem bootstrap, sem e com rotação |
| FP03 | Demanda 5 — "não chega": as duas leituras |
| FP04 | Demanda 6 — juntar "sem banheiro": V00495 e a prova V00238 ≤ V00495; depois, o graduado |
| FP05 | Demanda 7 — canalização e sem banheiro na fatorial |
| FP06 | Demanda 8 — tudo junto (S6 e S7) |
| FP07 | Demanda 9 — moradia não convencional |
| FP08 | Demanda 10 — o lixo |
| FP09 | Demanda 11 — as duas rotações |
| FP10 | Incerteza: um município de fora por vez, no lugar do bootstrap |
| FP11 | Validação contra FCU, cenário a cenário |
| FP12 | A grade do NB05: 324 especificações e 192 elegíveis, por dimensão |
| FP13 | A renda sozinha contra o índice (`acrescimo_renda.csv`) |

### 2.6 Padrão visual e de números (R1, R9, R10)

- **Formato:** 16:9, `criarDeck`. Paleta: tinta `#1A1A1A`, petrol `#1F4E4A`, clay `#A83A2C`,
  cinza `#666666`. Figuras em matplotlib, dpi 150, mesma paleta.
- **Uma divisória por parte, e só.** Sem slides de transição. Sem "neste slide". O título diz
  o que é; o subtítulo, a definição curta.
- **Números em pt-BR:**

  | Tipo | Formato |
  |---|---|
  | Proporções | em %, 2 casas |
  | Renda | R$, 2 casas |
  | Razão de moradores, IEP, RDI | 2 casas |
  | `banheiro_graduado` | 3 casas |
  | Assimetria | 2 casas |
  | Setores | inteiro com ponto de milhar |
  | Anexo xlsx | precisão total |

- **Anexo `Relatorio_Descritivo_numeros.xlsx`** (pandas com openpyxl), abas:
  - `Indice_slides`: o manifesto mais três colunas vazias para a escolha — "Vai para o artigo?
    (Sim/Talvez/Não)", "Seção do artigo", "Comentários" (requisito R13);
  - `Descritivas` (T03 com as definições do Quadro);
  - `Por_municipio` (T05);
  - `Por_regiao` (T04);
  - `Fatorial` (T19 a T27, em blocos).

---

## 3. Verificação

### 3.1 O verificador

`scripts/verificar_relatorio_descritivo.py` imprime OK ou FALHA por item, em no máximo 30
linhas:
1. **IDs:** todo slide do `.pptx` tem ID e linha "Fonte:"; os IDs são únicos e batem com o
   `manifesto.csv`, na mesma ordem.
2. **Números contra as tabelas:** cada número do `numeros.json` é recomparado com a tabela de
   origem (T03, T02, T19–T27, CSVs da `fatorial_ampliada`), com tolerância de 1e-9.
3. **Caminho independente:** três indicadores sorteados com semente fixa (sempre um de
   saneamento e um de demografia) são recalculados direto do `.db`, com SQL e pandas, sem o
   motor. O n, a média e a mediana têm de bater com a T03.
4. **Figuras:** toda figura citada no manifesto existe.
5. **Parte DS sem comparação:** nenhum slide DS tem mais de um indicador na figura nem as
   palavras "×", "versus", "correlação" ou "comparado".
6. **Vocabulário:** nenhum slide contém as expressões proibidas (§0.2, regra 9).
7. **Pendências:** conta quantos "A CONFERIR" e "[Pedro: interpretar]" restam, e lista os IDs.

### 3.2 Ordem de execução em todo lote

```
./.venv/bin/python scripts/dados_relatorio_descritivo.py
node scripts/gerar_relatorio_descritivo.js
./.venv/bin/python scripts/verificar_relatorio_descritivo.py
```

### 3.3 Folha de contato

Uma por lote, só dos slides novos.

```
soffice --headless --convert-to pdf --outdir <scratch> relatorio_descritivo/Relatorio_Descritivo_IVS_2026-10.pptx
swift scripts/folha_contato.swift <scratch>/Relatorio_Descritivo_IVS_2026-10.pdf <scratch>/folha.png 4 1600 <páginas>
```

Olhe a folha **uma vez**, à procura de texto cortado, sobreposição e figura fora do lugar.
Corrija e não olhe de novo; o verificador basta.

---

## 4. Lotes

| Lote | O quê | Teto | Para quando |
|---|---|---:|---|
| **0 — Piloto** | Cria `CONSTRUCAO.md`, `CORRECOES.md`, os três scripts e oito slides-piloto: A01, A02, DM02 (demanda 1), DS01, DS da chefia feminina, DS do IEP, FA05 e FP08 | 40 | Deck piloto, verificador verde e folha de contato. **Pedro aprova o layout e responde às leituras L1 e L3** |
| **1 — Demandas** | Parte DM inteira (DM00–DM15) e A03 | 30 | Deck v1 com A e DM |
| **2 — Descritiva** | Parte DS inteira (DS00–DS34) e as abas `Descritivas`, `Por_municipio` e `Por_regiao` | 35 | Deck com A, DM e DS |
| **3 — Fatorial descritiva** | Parte FA inteira | 30 | Deck com A, DM, DS e FA |
| **4 — Pedidos da fatorial** | Parte FP inteira e a aba `Fatorial` | 35 | Deck com tudo menos Z |
| **5 — Fechamento** | Z01, Z02, aba `Indice_slides`, verificação completa, uma linha em `docs/prompts/README.md` e outra em `docs/Apresentacoes_IVS/README.md` | 25 | Deck completo; a contagem de pendências do item 7 do verificador vai para o relatório |
| **C — Correção** | Um lote de correções do Pedro (seção 5) | 20 | Correções aplicadas e verificador verde |

**O fim de todo lote:**
1. rodar os três comandos de §3.2;
2. fazer a folha de contato dos slides novos;
3. atualizar o `ESTADO.md` (lote, versão do deck, histórico) e o `CONSTRUCAO.md`;
4. reportar em até 15 linhas;
5. **parar**.

---

## 5. Protocolo de correção (requisito R11)

1. **Leitura:** leia só `ESTADO.md`, `CORRECOES.md` e `CONSTRUCAO.md`.
2. **Registro:** registre cada pedido do Pedro **com as palavras dele** em `CORRECOES.md`, como
   `C-NN`, com os IDs de slide citados.
3. **Leitura do pedido:** escreva a sua leitura em uma linha.
   - Se houver duas leituras possíveis, **pergunte antes de mexer**.
   - Se a correção contradiz o `INTERPRETACAO.md`, atualize-o e diga isso no relatório.
4. **Localização:** ache no `manifesto.csv` a função e a fonte que geram o slide.
5. **Mudança cirúrgica:** mude só isso.
   - Número errado se corrige **na origem** (script ou leitura da tabela), nunca no JS.
   - Se a origem for uma tabela da `00_referencia` ou de `banco_de_dados/eda/`, **não a altere**:
     registre "A CONFERIR na origem" e reporte.
6. **Execução:** rode os três comandos de §3.2. A versão do deck sobe (v2, v3…). Os slides
   alterados ganham `versao_alterada` no manifesto.
7. **Relatório:** C-NN → leitura → slides alterados → verificador.

Formato do registro em `CORRECOES.md`:

```
## C-NN — dd/mm/aaaa — slides DS07, DS08
Pedido (palavras do Pedro): "..."
Leitura: ...
Mudança: arquivo:função — o que mudou
Verificação: verificador OK (itens 1–7) · versão do deck v3
```

---

## O que nunca fazer

- **Gráfico ou tabela que ponha dois indicadores lado a lado na Parte DS.** Isso inclui
  matrizes de correlação, dispersões e boxplots de vários indicadores.
- Reaproveitar nos slides DS as figuras agrupadas por dimensão da `00_referencia` (F02 a F13).
- Chamar a referência do NB05 de "final" ou "escolhida".
- Inventar redação da orientadora, resposta dela, data, leitura ou número.
- Editar o `.pptx` à mão.
- Regerar ou alterar qualquer arquivo de `analises_exploratorias/` ou `banco_de_dados/eda/`.
- Começar o lote seguinte sem o OK do Pedro.
- Commit sem pedido; subagentes; skills.
