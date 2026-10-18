# Plano: parte semântica do graphify em vida_os e Projeto_IVS_Censo22 (out/2026)

> Arquivo de estado. A sessão que executar lê **só este arquivo**, faz a próxima etapa
> pendente, marca a tabela e para. Regras de custo herdadas de
> `prompt_graphify_update_2026-09.md` (sem `--mode deep`, ondas de 2, Sonnet).

## Estado

| Etapa | Situação | Custo LLM |
|---|---|---|
| 0 — AST (`graphify update .`) nos dois repositórios | **Concluída 18/10** — vida_os 429→1148 nós; IVS 2025→2963 nós | zero |
| 1 — Cortar o corpus (`.graphifyignore`) | **Concluída 18/10** — IVS: 59 docs + 1 PDF | zero |
| 2 — Onda 1: vida_os (1 chunk) + IVS chunk 1 | **Concluída 18/10** — vida_os 76 nós/125 arestas (fechado: 1194 nós, 3075 arestas); IVS c1 102/196 | ~99k + ~101k tokens (5h: 48%→54%) |
| 3 — Onda 2: IVS chunks 2 e 3 | **Concluída 18/10** — c2 161/354, c3 118/208 | ~155k + ~129k tokens |
| 4 — Merge, cluster, relatório, queries de conferência | **Concluída 18/10** — IVS 3174 nós, 4932 arestas, 255 comunidades; queries acham os nós novos | zero (rótulos reaproveitados, sem LLM) |
| 5 — Commit + push de `graphify-out/` nos dois | **Concluída 18/10** | zero |

Custo real da parte semântica: ~485 mil tokens Sonnet em 4 subagentes (a estimativa era ~120 mil:
cada subagente gasta ~100 mil só com o prompt da extração e o próprio contexto). Na próxima vez,
estimar ~100 mil por subagente e preferir chunks maiores (até 25 arquivos) a mais chunks.
| (opcional) `graphify label --missing-only` | não planejada | LLM, decidir depois |

## O que falta extrair (medido em 18/10, nada no cache semântico)

| Repositório | Arquivos | Tamanho | Observação |
|---|---|---|---|
| vida_os | 5 docs | ~9,8 mil palavras | README (5,5 mil), AUDITORIA-SEGURANCA-OPUS, PLANO-MELHORIAS, index.html, privacidade.html |
| IVS | 58 docs + 5 PDFs | ~38 mil palavras + PDFs | 36 READMEs de `analises_exploratorias` (~70 palavras cada); o grosso está em `docs/prompts`, `relatorio_*`, `versoes_fatorial` |

**O risco está nos PDFs:** `Relatorio_Descritivo_IVS_2026-10_v3.pdf` (140 pág.) e `_v4_APOIO.pdf`
(295 pág.) não têm texto extraível. O subagente leria página por página como imagem, o que
custa mais que todo o resto somado. São exportações dos .pptx (já ignorados), e
`CONSTRUCAO.md`/`INTERPRETACAO.md`/`CORRECOES.md` descrevem o mesmo conteúdo.

## Etapa 1 — cortar o corpus (grátis)

Acrescentar ao `.graphifyignore` do IVS:

```
# PDFs exportados dos decks do relatório descritivo (os .md descrevem o mesmo)
relatorio_descritivo/*.pdf
# Versões intermediárias do relatório parcial: fica só o final
relatorio_parcial_raic/*_v1*.pdf
```

Resultado esperado: IVS cai para 58 docs + 1 PDF de 9 páginas. Conferir antes de seguir
(rodar na raiz de cada repositório, com o Python de `~/.local/share/uv/tools/graphifyy/bin/python`):

```python
from pathlib import Path; from graphify.detect import detect_incremental
r = detect_incremental(Path("."), "graphify-out/manifest.json")
print({k: len(v) for k, v in r["new_files"].items() if k != "code"})
```

## Etapas 2 e 3 — extração semântica em 2 ondas

Procedimento da skill (`references/update.md` → SKILL.md Parte B), com estes limites:

- Chunks agrupados por pasta: **vida_os** = 1 chunk (5 arquivos); **IVS chunk 1** =
  `analises_exploratorias/` (37 arquivos pequenos); **chunk 2** = `docs/` + `scripts/README.md`;
  **chunk 3** = `relatorio_*` + `versoes_fatorial/` + `banco_de_dados/` + PDF do RAIC.
- `subagent_type="general-purpose"`, `model="sonnet"`, prompt do `extraction-spec.md` literal.
- Cada subagente **grava o chunk em disco e responde uma linha** ("chunk N: X nós, Y arestas").
  Nada de JSON na resposta: o resultado não pode voltar para o contexto principal.
- Estimativa: ~15–25 mil tokens de leitura por subagente, ~120 mil no total.

## Controle de uso (antes de cada onda)

1. Chamar `get_usage`. **Parar** se o limite de 5h estiver ≥ 80% ou o semanal ≥ 85%:
   anotar aqui o que ficou pronto e esperar o reset.
2. Chunk que já existe em `graphify-out/.graphify_chunk_NN.json` não é refeito.
3. Na sessão principal: nunca ler `graph.json` nem um chunk inteiro; saída de script com
   `head -60`; consultas ao grafo com `--budget 1500`.
4. Rodar numa **sessão nova**, que lê só este arquivo, e não na sessão longa que fez a
   varredura (cada turno dela recarrega ~170 mil tokens de contexto).

## Etapa 4 — conferir

Nós e arestas antes/depois e três consultas (`--budget 1500`):
"o que é a V00237 e onde ela entra no índice", "qual a proposta de referência do NB05",
"onde está a regra das faixas do IVS". No vida_os: `graphify query "como funciona a skill da Alexa"`.

## Etapa 5 — versionar

`graphify-out/` é versionado nos dois repositórios. Commit
`chore(graphify): atualização AST + semântica de outubro` e push. Commit só com o seu nome.
