## 🚀 Como usar

**Dentro do Claude Code** (depois de reiniciar) — construir o grafo do projeto atual:
```
/graphify .
``` 
Isso gera três arquivos em `graphify-out/`:
- `graph.html` → abre no navegador, clicável, com filtro e busca
- `GRAPH_REPORT.md` → os destaques: conceitos-chave, conexões surpreendentes, perguntas sugeridas
- `graph.json` → o grafo completo, que você consulta sem reler os arquivos

**Consultar (em vez de fazer grep/reler arquivos):**
```
/graphify query "o que conecta a autenticação ao banco de dados?"
/graphify path "UserService" "DatabasePool"     # menor caminho entre dois símbolos
/graphify explain "RateLimiter"                  # o que um conceito toca
```
Cada aresta vem marcada `EXTRACTED` (estava explícito no código) ou `INFERRED` (o graphify deduziu).

**Flags úteis:**
```
/graphify . --update          # re-extrai só os arquivos que mudaram
/graphify . --cluster-only    # recalcula comunidades sem re-extrair
/graphify . --no-viz          # só relatório + JSON, sem HTML
/graphify . --mode deep       # extração de relações mais agressiva
/graphify add https://arxiv.org/abs/1706.03762   # adiciona um paper ao grafo
```

> **No terminal PowerShell** (fora do chat), use `graphify .` **sem a barra** — a `/` inicial é separador de caminho no PowerShell. Dentro do chat do Claude Code, use `/graphify`.

## 📦 Extras opcionais (instale só se precisar)

O que instalei cobre **código**. Para outros tipos de arquivo:
```powershell
uv tool install "graphifyy[pdf]"        # PDFs
uv tool install "graphifyy[office]"     # .docx / .xlsx
uv tool install "graphifyy[video]"      # transcrição de vídeo/áudio (local)
uv tool install "graphifyy[all]"        # tudo de uma vez
```
Dentro do Claude Code, a leitura semântica de docs/PDFs/imagens usa **o próprio modelo da sua sessão** — não precisa de chave de API. Só o modo *headless* (`graphify extract` no terminal puro) exigiria uma chave.

## 🔧 Opcionais que valem a pena depois

```powershell
graphify claude install    # (rodar dentro de um projeto) faz o Claude consultar o grafo automaticamente
graphify hook install      # reconstrói o grafo a cada git commit (só AST, custo zero)
```

E, para o cache do Claude Code não invalidar a cada build, adicione ao `.claudeignore` do projeto:
```
graph.json
graphify-out/
```