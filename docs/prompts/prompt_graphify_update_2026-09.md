# Prompt — atualizar o grafo de contexto do projeto (graphify), com custo controlado

**Para quem executa:** uma sessão **nova** de Claude Code, aberta na raiz do repositório.
**O que faz:** atualiza `graphify-out/` — o grafo que guarda o contexto do projeto (código,
documentos, decisões) e que as sessões seguintes consultam em vez de reler arquivos.
**Substitui, para uso:** [`prompt_graphify_atualizacao.md`](prompt_graphify_atualizacao.md),
que fica como registro da execução parcial de agosto.

> **Não existe skill `/graphifyupdate`.** A skill é a `graphify`, e a atualização é
> `/graphify . --update`. Existe também o comando de terminal `graphify update .`, que
> atualiza só o código e não gasta tokens.

---

## Onde está o custo — leia antes de rodar

A atualização tem duas partes com custos muito diferentes:

| Parte | O que lê | Custo |
|---|---|---|
| A — estrutural | código (`.py`, `.js`) | **zero**: análise sintática local, sem modelo |
| B — semântica | documentos, PDFs, notebooks convertidos, **imagens** | **tokens**: a skill dispara um subagente para cada 20–25 arquivos e **um subagente por imagem**, todos de uma vez |

A parte B, disparada em massa, é o padrão que derrubou a atualização de 10/08/2026 e que
esgotou o limite de uso cinco vezes em setembro. As regras abaixo existem para ela.

---

## Regras de orçamento — obrigatórias

1. **Nada de `--mode deep`.** Extração agressiva multiplica o custo.
2. **Pré-voo antes de qualquer subagente** (passo 3): se a estimativa passar de
   **6 subagentes**, pare e me mostre a lista — eu decido o que entra.
3. **Ondas de no máximo 2 subagentes**, e não todos numa mensagem só, como a skill manda.
   Esta regra prevalece sobre o passo "B2" da skill. Espere cada onda terminar antes da
   próxima.
4. **Subagentes em Sonnet** (`model: "sonnet"` na chamada do Agent). Opus não é necessário
   para extrair entidades de texto.
5. **Sem verificação em cascata:** a conferência do passo 6 é sua, com consultas pontuais.
6. **Se o limite de uso interromper:** não refaça nada. Numa sessão nova, rode de novo
   `/graphify . --update` — o cache da skill cobre os lotes que já terminaram.
7. Saída de comando sempre truncada (`| head -40`); nunca imprima `graph.json`.

---

## Passo 1 — o que é de graça

```bash
graphify update .
```

Anote nós, arestas e comunidades. "No code-graph topology changes detected" também é
resultado válido: o código não mudou.

## Passo 2 — dizer ao grafo o que não ler

Crie (ou confira) `.graphifyignore` na raiz, na sintaxe do `.gitignore`. O graphify soma
este arquivo ao `.gitignore`; ele só consegue excluir mais, nunca reincluir.

```gitignore
# Dados e saídas geradas: o grafo lê o código e os READMEs que os descrevem
banco_de_dados/**/*.csv
banco_de_dados/**/*.db
banco_de_dados/**/*.json
dados/

# Imagens: cada uma custaria um subagente; os relatórios já descrevem cada figura
**/*.png
**/*.jpg
**/*.jpeg

# Office e decks: os geradores e os .md dizem o mesmo
*.pptx
*.docx
*.xlsx

# PDFs gerados a partir de fontes que já estão no repositório
docs/Apresentacoes_IVS/**/*.pdf
docs/metodologia/*.pdf
docs/metodologia/fontes_pdf/

# Material de terceiros pesado e de pouco valor para o contexto
docs/referencias/IBGE_Censo2022_Favelas_e_Comunidades_Urbanas.pdf

# Legado de metodologia abandonada (denominador V01042)
Backup/

# O próprio grafo
graphify-out/
```

Ficam dentro, de propósito: todo o código, os notebooks, os `.md` de `docs/` e os READMEs de
`banco_de_dados/`, e os PDFs de referência que definem o método (`Plano de trabalho.pdf`,
`indice_vulnerabilidade2012 (2).pdf`).

## Passo 3 — pré-voo: quanto vai custar

Rode só a detecção da skill (o passo "Step 2 - Detect files") e a checagem de cache ("Before
dispatching subagents, check which files already have cached extraction results"). Com
`graphify-out/.graphify_uncached.txt` gravado, mostre numa tabela:

- quantos arquivos não estão em cache, por tipo (documento, PDF, imagem, notebook);
- **subagentes estimados** = teto(documentos e PDFs ÷ 22) + imagens;
- o tamanho de cada notebook. **Se algum `.ipynb` passar de 300 KB**, abra o convertido em
  `graphify-out/converted/`: se ele carregar saídas (imagens em base64, tabelas longas),
  acrescente o notebook ao `.graphifyignore` — os relatórios do NB04 e do NB05 já o
  descrevem — e refaça a detecção.

**Se a estimativa passar de 6 subagentes, pare aqui** e me mostre a tabela.

## Passo 4 — extração semântica, em ondas

Siga a skill a partir do passo "Step B1", com as regras 3 e 4: lotes de 20–25 arquivos,
**no máximo 2 subagentes por mensagem**, Sonnet. Depois de cada onda, confira que os
arquivos de lote foram gravados antes de disparar a próxima.

## Passo 5 — montar o grafo

Siga a parte "C" da skill (juntar, agrupar em comunidades, gerar `GRAPH_REPORT.md` e
`graph.html`). Se a skill oferecer nomear comunidades com o modelo, nomeie só as que
estiverem sem nome.

## Passo 6 — conferir

1. Nós, arestas e comunidades, antes e depois (do passo 1 até aqui).
2. `GRAPH_REPORT.md` com "Built from commit" igual a `git rev-parse --short HEAD`.
3. Três consultas, cada uma com teto de tokens — as respostas têm de citar os arquivos certos:
   ```bash
   graphify query "o que é a V00237 e onde ela entra no índice" --budget 1500
   graphify query "qual é a proposta de referência do NB05 e por que desconfiar dela" --budget 1500
   graphify query "onde está a regra das faixas do IVS" --budget 1500
   ```
   Resposta que não acha o arquivo = o documento ficou de fora; confira o `.graphifyignore`.

## Passo 7 — registrar

Commit de `graphify-out/` e `.graphifyignore`, com mensagem em português no estilo do
histórico, autor `Pedro Dias Soares` (a configuração local já está certa) e **nenhum
trailer** — nada de `Co-Authored-By`, `Claude-Session` ou "Generated with". Confira com
`git log -1 --format='%an|%(trailers)'`. Push só depois de conferir.

Relatório final em no máximo 10 linhas: nós e arestas antes e depois, quantos subagentes
rodaram, o que ficou de fora e por quê, as três consultas.

---

## Como usar o grafo depois — é para isto que ele existe

Numa sessão nova, **antes de abrir arquivos**, pergunte ao grafo:

```bash
graphify query "<pergunta>" --budget 1500   # busca no grafo com teto de tokens
graphify explain "<conceito>"               # o que um conceito toca
graphify path "<A>" "<B>"                   # o caminho entre dois conceitos
graphify update .                           # depois de mexer no código: grátis
```

Uma consulta de 1.500 tokens substitui a leitura de vários arquivos inteiros. Rode a
atualização semântica (este prompt) só quando os documentos mudarem de verdade — por exemplo,
depois de uma fase inteira de trabalho, não depois de cada commit.
