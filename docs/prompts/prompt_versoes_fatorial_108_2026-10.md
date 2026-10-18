# Prompt — As 108 versões da análise fatorial, com 108 fichas (outubro/2026)

Rodar a análise fatorial em 108 versões e entregar três peças em formato de relatório descritivo:
- um **deck principal**, com cerca de 16 slides: os eixos, as 108 de uma vez, um eixo por vez e as
  elegíveis;
- um **caderno de fichas**, com uma versão por slide, 108 fichas;
- uma **planilha**, com uma linha por versão e colunas de seleção para o artigo.

Leituras obrigatórias:
- **O pedido e as leituras adotadas:** `versoes_fatorial/INTERPRETACAO.md` (requisitos V1–V8,
  leituras L1–L7).
- **A lista das 108 versões:** `versoes_fatorial/VERSOES.md` (IDs V001–V108).

Este prompt não repete nenhum dos dois.

---

## Como usar

- **Um lote por sessão nova, em Sonnet**, aberta nesta mesma pasta (não pelo botão de tarefa:
  nada disto está commitado). Na primeira mensagem, cole: *"Execute o LOTE N de
  `docs/prompts/prompt_versoes_fatorial_108_2026-10.md`. Leia primeiro `versoes_fatorial/ESTADO.md`."*
- **O que cada sessão lê:**
  - o lote 0 lê `ESTADO.md`, `INTERPRETACAO.md`, o cabeçalho e as linhas V001–V030 de
    `VERSOES.md`, e as seções 0 a 3 deste prompt;
  - os lotes seguintes leem `ESTADO.md`, `CONSTRUCAO.md`, a seção 0 e o bloco do lote;
  - uma correção lê `ESTADO.md`, `CORRECOES.md`, `CONSTRUCAO.md` e a seção 5.
- **Cada lote termina parado**, a menos que o Pedro diga "sem parar". Nesse caso os lotes seguem
  em sequência, com o fim de lote completo (§4) em cada um.

---

## 0. Regras

### 0.1 Orçamento de tokens

1. **Teto por lote** (seção 4). A 80% do teto, grave o estado e pare.
2. **Nada de subagentes, workflows ou skills.**
3. **Saída sempre truncada** (`| head -60`). Nunca imprima um CSV inteiro nem leia `.pptx` ou
   `.png` gerados. A exceção é **uma** folha de contato por lote, só dos slides novos.
4. **Dois erros iguais seguidos:** pare e reporte.
5. **Relatório de fim de lote:** até 15 linhas.

### 0.2 O que não se toca

1. **`relatorio_descritivo/` inteiro e os quatro scripts dele:** `dados_relatorio_descritivo.py`,
   `gerar_relatorio_descritivo.js`, `verificar_relatorio_descritivo.py` e
   `comparar_edicoes_relatorio.py`. O Pedro está editando aquele deck à mão (V4).
2. **Só leitura:** `analises_exploratorias/`, `banco_de_dados/eda/ivs_especificacoes/` e
   `banco_de_dados/eda/fatorial_ampliada/`.
3. **Só importação, nunca edição:** `scripts/ivs_especificacoes.py`, `scripts/fatorial_ampliada.py`,
   `src/ivs_censo/*`.
4. **Commit só a pedido do Pedro**, só com o nome dele, sem trailer.

### 0.3 Regras contra alucinação (as do relatório descritivo, que o Pedro aprovou)

1. **Nenhum número digitado à mão no JS.** Tudo sai de `versoes_fatorial/dados/numeros.json`,
   que sai dos CSVs de resultado.
2. **Todo slide tem ID** no canto superior direito: V001–V108 nas fichas, VP01… no deck
   principal. **A fonte vai só nas notas do apresentador** (C-02 do relatório); nenhuma linha
   "Fonte:" no slide.
3. **Frases "O que mostra" factuais:** modelos preenchidos com os números do próprio slide.
   - Sem causa e sem adjetivo de juízo.
   - Nenhuma versão é chamada de "melhor" ou "escolhida"; a referência proposta (V023) é sempre
     "proposta".
4. **O que não tem fonte fica "A CONFERIR".**
5. **Sem marcas de texto gerado:** "vale destacar", "é importante notar", "em suma", "robusto",
   emoji.
6. **Tabelas nativas do PowerPoint**, editáveis (V6). Nenhuma tabela vira imagem.

---

## 1. Fatos verificados (não redescobrir)

**Motor do NB05 a reaproveitar**
- Importe `scripts/ivs_especificacoes.py` como `ie` e `scripts/fatorial_ampliada.py` como `fa`; os
  dois têm `main()` protegido. O que usar de cada um:

  | Função ou objeto | O que faz |
  |---|---|
  | `ie.carregar_base()` | A base da fatorial ampliada mais V00236/V00237 e a coluna `banheiro_graduado` |
  | `fa.montar(df, colunas, renda)` | Devolve `(d, _)`, já com o recorte e a renda invertida |
  | `rodar_cenario(X, com_horn=True)` | Em `src/ivs_censo/fatorial.py`. Correlação de Spearman, 2 fatores |
  | `ie.reparticoes(r, colunas)[('promax', '60_40')]` | Devolve `(M, rep)` |
  | `fa.pesos_indice(M, rep)` | Os pesos das variáveis no índice |
  | `ie.indice(d, colunas, w, 'municipal')` | O índice |
  | `ie.faixas(v, mun, 'ivs_bh')` | As faixas (0–3; −1 = indefinida) |
  | `ie.elegibilidade(r, 'promax', colunas)` | Os quatro critérios, com o que falhou |
  | `ie.auc_grupos`, `ie.auc_municipal(v, fcu, mun)` | A validação contra FCU |
  | `ie.estabilidade(d, colunas, {'promax'})` | Um município de fora por vez |
  | `ie.fator_renda`, `ie.ROT`, `fa.ROT` | Fator da renda e rótulos |

  O `main()` de `ie` (a partir da linha 368) é o modelo de laço: amostra comum na linha 377,
  registro por base em seguida.
- **Variáveis:**
  - `fa.IVS7_INV` (os 7 do IVS, com `renda_inv`) e `fa._sem_lixo(...)`;
  - `fa.RENDAS` = {original, sem_extremo, mediana_mun} → colunas de renda;
  - `fa.NOVAS` traz `pct_agua_nao_encanada`, `pct_sem_agua_canalizada`, `pct_sem_banheiro` e a
    moradia não convencional, todas já carregadas por `fa.carregar`.
- **Água:** "não chega" = V00201 (`pct_agua_nao_encanada`); "sem canalização" = V00200 + V00201
  (`pct_sem_agua_canalizada`).

**Versões já rodadas, que servem de trava**
- As 18 versões sem água canalizada e sem moradia existem em
  `banco_de_dados/eda/ivs_especificacoes/especificacoes.csv`. A linha equivalente é a de id
  `<renda>·lixo_<com|sem>·banheiro_<fora|v00495|graduado>·promax·60_40·municipal`.
- **A referência proposta é a V023:** renda original, sem lixo, banheiro graduado, n = 73.878,
  KMO 0,7807, elegível.

**Tempo**
- Não há medida do tempo de uma versão com Horn, nem da estabilidade (70 rodadas por versão).
  O lote 0 mede antes de rodar tudo.

**Estilo**
- Os decks usam `scripts/deck_comum.js` (`criarDeck`).
- O estilo aprovado está em `scripts/gerar_relatorio_descritivo.js`. **Leia, não importe nem
  edite:** o arquivo executa ao ser carregado. Copie para o gerador novo os layouts de que
  precisar (`tabelaLarga`, `tabelaTexto`, `divisoria`, `paragrafo`, `marca`).
- Paleta das figuras: as constantes `TINTA`, `PETROLEO`, `ARGILA` e `CINZA` de `scripts/eda_versoes.py`.
- Formatadores pt-BR: `br`, `intbr` e `pctbr`, também de `scripts/eda_versoes.py`.

---

## 2. O que produzir

### 2.1 Arquivos

**Cálculo** (`banco_de_dados/eda/versoes_fatorial/`), feito por `scripts/versoes_fatorial.py`:
- `versoes.csv` — uma linha por versão:
  - `id`, os 5 eixos, `p`, `variaveis`;
  - `n`, `n_comum`;
  - `kmo`, `bartlett_qui2`, `bartlett_gl`, `msa_min`, `msa_min_variavel`;
  - `fatores_kaiser`, `fatores_horn`, `var_explicada_2f`, `phi`;
  - os 4 critérios e `elegivel`, com `criterio_que_falhou`;
  - `peso_f1`, `auc_global_propria`, `auc_global_comum`, `auc_mun_comum`, `n_mun`;
  - % por faixa do IVS-BH;
  - `spearman_v023_comum` e `muda_faixa_v023_comum` (comparação com a referência proposta);
- `cargas.csv` — versão × variável: promax padrão F1/F2, estrutura F1/F2, comunalidade
  oblíqua, MSA, peso no índice;
- `pares_por_eixo.csv` — para cada eixo e cada troca de nível (ex.: lixo com → sem), os pares de
  versões que só diferem nele, com a mediana, o mínimo e o máximo de:
  - Δ KMO, Δ variância, Δ AUC municipal comum, Δ fatores (Kaiser/Horn);
  - quantos passam a ser elegíveis ou deixam de ser;
  - Spearman entre os índices e % que muda de faixa (amostra comum);
- `estabilidade.csv` — se couber no orçamento de tempo (lote 1);
- `README.md` — a procedência, no padrão das outras pastas de `eda/`.

**Processo e entregas** (`versoes_fatorial/`):
- os registros: `ESTADO.md`, `CONSTRUCAO.md`, `CORRECOES.md`, `dados/numeros.json`,
  `dados/manifesto.csv`, `figuras/`;
- as peças: `Versoes_Fatorial_Principal.pptx`, `Caderno_Fichas_108.pptx` e
  `Versoes_Fatorial_numeros.xlsx`.

**Scripts novos:**

| Script | O que faz |
|---|---|
| `scripts/versoes_fatorial.py` | Enumera as versões, roda e grava os resultados |
| `scripts/dados_versoes_fatorial.py` | Gera `numeros.json`, manifesto, figuras e xlsx |
| `scripts/gerar_versoes_fatorial.js` | Gera os dois decks, sempre do zero |
| `scripts/verificar_versoes_fatorial.py` | A conferência (§3) |
| `scripts/comparar_edicoes_versoes.py` | Leva à origem as edições do Pedro, como o do relatório: casa slides pelo ID e junta os pedaços de texto sem espaço |
| `tests/test_versoes_fatorial.py` | Os testes do enumerador e da trava |

**Trava contra sobrescrita**, a mesma do gerador do relatório: grave o sha256 do deck gerado
e recuse sobrescrever se o arquivo foi editado à mão, salvo com `--sobrescrever`. Guarde
sempre uma cópia intocada em `dados/ultimo_gerado_<deck>.pptx`.

### 2.2 O enumerador

- **Ordem dos IDs:** `itertools.product` na ordem renda (original, sem extremo, mediana) → lixo
  (com, sem) → água (nenhuma, não chega, sem canalização) → banheiro (fora, V00495, graduado) →
  moradia (não, sim). V001 é a primeira combinação.
- **O teste:** 108 IDs únicos; nenhuma versão com as duas águas; V001, V002, V019, V023 e V024
  iguais às linhas de `VERSOES.md`.
- **Colunas na ordem do `fa`:** IVS-7 (sem o lixo, se for o caso), depois água, banheiro e moradia.

### 2.3 Caderno de fichas (V2)

| ID | Slide |
|---|---|
| VF00 | Capa |
| VF01 | Como ler uma ficha. Os 5 eixos e o código; o que é amostra própria e comum; os 4 critérios |
| V001–V108 | Uma ficha por versão, na ordem dos IDs |

**Layout da ficha.** Fixo nas 108; só tabelas, nenhuma figura.
- **Título:** "V047 — renda sem extremo · sem lixo · + não chega · banheiro fora · com moradia".
  Subtítulo: "p variáveis · n setores (amostra própria)".
- **Selo no topo**, no acento: **"Passa nos critérios do NB05"** ou **"Não passa: <critério que
  falhou>"**. Na V023, mais o selo **"referência proposta"**.
- **Esquerda — "A versão":** os 5 eixos, variáveis (p), setores na amostra própria e na comum.
- **Centro — "Adequação":**
  - KMO, Bartlett (χ² e gl), MSA mínimo (e de qual variável);
  - fatores por Kaiser e por Horn, retidos (2), variância dos 2 fatores, Φ.
- **Direita — "Cargas e pesos":** uma linha por variável, com F1 e F2 (promax padrão), comunalidade
  e peso no índice (%).
- **Faixa de baixo — "Validação e faixas":** AUC global (própria e comum), AUC municipal (comum,
  com o nº de municípios), % dos setores em cada faixa do IVS-BH, Spearman com a V023 e % que
  muda de faixa.
- **"O que mostra":** duas frases-modelo. Exemplos:
  - *"Kaiser e Horn indicam {k} e {h} fatores; a solução usa 2."*
  - *"A maior carga em F1 é de {var}; em F2, de {var}."*
- **Notas do apresentador:** fontes (`versoes.csv`, `cargas.csv`, linha do id) e a função geradora.

### 2.4 Deck principal (V3)

| ID | Slide | Fonte |
|---|---|---|
| VP01 | Capa | |
| VP02 | Como ler | Códigos, as duas amostras, o método fixo (L1), o selo de proposta |
| VP03 | Os 5 eixos e o código | Tabela de `VERSOES.md` |
| VP04 | A amostra | Setores por versão (mín–máx e quais perdem mais) e a amostra comum, com quantos saem e por quê |
| VP05 | As 108 de uma vez: elegibilidade | Figura em grade de 6 linhas (renda × lixo) por 18 colunas (água × banheiro × moradia). Cada célula com o ID, pintada por passa / não passa. Tabela-resumo ao lado |
| VP06 | As 108 de uma vez: KMO | A mesma grade, com o KMO na célula; escala de uma cor só |
| VP07 | As 108 de uma vez: AUC municipal (comum) | A mesma grade |
| VP08 | Um eixo por vez: renda | Mostra, com números, que as três rendas quase não diferem |
| VP09 | Um eixo por vez: lixo | `pares_por_eixo.csv` |
| VP10 | Um eixo por vez: água canalizada | `pares_por_eixo.csv` |
| VP11 | Um eixo por vez: banheiro | `pares_por_eixo.csv` |
| VP12 | Um eixo por vez: moradia | `pares_por_eixo.csv` |
| VP13 | As elegíveis | Tabela: ID, eixos, n, KMO, AUC municipal comum, Spearman com a V023 |
| VP14 | A ordem das elegíveis pelas leituras do NB05 | Só se o lote 1 calculou a estabilidade; senão "A CONFERIR — estabilidade não calculada" |
| VP15 | O que está em aberto | As leituras L1–L7 e o que depende da orientadora |

Figuras em matplotlib, dpi 150, na paleta do projeto. A grade tem eixos rotulados com as
palavras, não com códigos.

### 2.5 Planilha `Versoes_Fatorial_numeros.xlsx`

- **`Versoes`:** `versoes.csv` mais as três colunas vazias: "Vai para o artigo? (Sim/Talvez/Não)",
  "Seção do artigo", "Comentários". Com filtro automático nos 5 eixos.
- **`Cargas`:** `cargas.csv`.
- **`Pares_por_eixo`.**
- **`Indice_slides`:** o manifesto.

---

## 3. Verificação

`scripts/verificar_versoes_fatorial.py` imprime OK ou FALHA por item, em até 30 linhas:
1. **Enumerador:** 108 IDs únicos, sem as duas águas juntas, e as linhas conferidas de
   `VERSOES.md` batendo.
2. **Trava:** as 18 versões equivalentes batem com `especificacoes.csv` (promax · 60_40 ·
   municipal) em n, KMO, MSA mínimo, fatores Kaiser e Horn, `peso_f1` e `elegivel`, com
   tolerância de 1e-6. A V023 dá n = 73.878 e é elegível.
3. **Caminho independente:** duas versões novas sorteadas (semente 42) são refeitas sem o laço do
   motor. As colunas vêm direto do `.db`, por SQL, com o recorte; o resto é `rodar_cenario`. O n e
   o KMO têm de bater.
4. **Fichas:** 108 fichas, na ordem; cada uma com o seu ID, sem "Fonte:" no slide e com "Fontes:"
   nas notas. Toda célula de tabela do `numeros.json` aparece no slide.
5. **Números:** os do `numeros.json` são recomparados com `versoes.csv`, `cargas.csv` e
   `pares_por_eixo.csv`.
6. **Vocabulário proibido** e as palavras "melhor" ou "escolhida" junto de um ID de versão.
7. **Pendências:** contagem de "A CONFERIR" por slide (informativo).

**Folha de contato:** uma por lote, só dos slides novos. Converta com
`soffice --headless --convert-to pdf` no scratchpad e monte com
`swift scripts/folha_contato.swift <pdf> <png> <colunas> <largura> <p1,p2,...>`. As páginas vão
separadas por vírgula, não por faixa. Olhe uma vez, corrija e não olhe de novo.

---

## 4. Lotes

| Lote | O quê | Teto | Para quando |
|---|---|---:|---|
| **0 — Motor e trava** | Pasta e registros (`ESTADO`, `CONSTRUCAO`, `CORRECOES`); `versoes_fatorial.py` com o enumerador e os testes. Roda a V023 e uma versão nova, **medindo o tempo** de cada uma. Depois a trava das 18; depois as 108 sem estabilidade | 40 | `versoes.csv` e `cargas.csv` com 108 linhas de versão; trava verde; tempo por versão no `ESTADO.md` |
| **1 — Estabilidade e pares** | `pares_por_eixo.csv` e o README de procedência. **Estabilidade:** se 108 × 70 rodadas couberem em 20 minutos pelo tempo medido, rode em todas; senão, só nas elegíveis, e diga isso no `ESTADO.md` | 30 | Resultados completos; itens 1–3 do verificador verdes |
| **2 — Fichas piloto** | `dados_versoes_fatorial.py`, `gerar_versoes_fatorial.js` e o verificador. Caderno piloto com VF00, VF01, V001, V023 (referência proposta), V024 e V010 (10 variáveis: com lixo, não chega, V00495 e moradia) | 35 | **O Pedro aprova o layout da ficha** |
| **3 — Caderno completo** | As 108 fichas | 30 | Itens 4–5 verdes; folha de contato de uma amostra de 12 fichas |
| **4 — Deck principal** | VP01–VP15 e as figuras de grade | 35 | Deck pronto, verificador verde |
| **5 — Planilha e fechamento** | xlsx; `comparar_edicoes_versoes.py`; uma linha em `docs/prompts/README.md`, outra em `scripts/README.md` e o README da pasta de resultados | 25 | Tudo verde; relatório final |
| **C — Correção** | Um lote de correções (seção 5) | 20 | Corrigido e verde |

**O fim de todo lote:**
1. rodar o que o lote gerou e o verificador;
2. fazer a folha de contato, se houve slide novo;
3. atualizar `ESTADO.md` e `CONSTRUCAO.md`;
4. reportar em até 15 linhas;
5. parar, salvo se o Pedro disse "sem parar".

---

## 5. Protocolo de correção

1. **Leitura:** leia só `ESTADO.md`, `CORRECOES.md` e `CONSTRUCAO.md`.
2. **Edições à mão:** se o Pedro editou um deck, rode `comparar_edicoes_versoes.py` **antes** de
   regerar qualquer coisa.
3. **Registro:** cada pedido vai para `CORRECOES.md`, como C-NN, **com as palavras do Pedro**, os
   IDs citados e a sua leitura em uma linha. Se houver duas leituras, pergunte antes de mexer.
4. **Mudança na origem:** corrija no script ou na leitura da tabela, nunca no `.pptx`. Regere,
   rode o verificador e suba a versão do deck.
5. **Relatório:** C-NN → slides alterados → verificador.

---

## O que nunca fazer

- Tocar em `relatorio_descritivo/` ou nos scripts dele, nem regerar aquele deck.
- Editar `ivs_especificacoes.py`, `fatorial_ampliada.py` ou `src/ivs_censo/` (só importar).
- Chamar uma versão de "melhor", "final" ou "escolhida".
- Pôr fonte, caminho de arquivo ou nome de função em texto visível do slide.
- Ler `.pptx` ou `.png` gerados fora da folha de contato.
- Começar o lote seguinte sem o OK do Pedro, a menos que ele tenha dito "sem parar".
- Commit sem pedido; subagentes; skills.
