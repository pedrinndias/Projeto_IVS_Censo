# `docs/prompts/` — prompts executáveis

Prompts escritos para colar numa sessão de Claude Code aberta na raiz do projeto. Ficam
versionados pelo mesmo motivo que os scripts: o que produziu um resultado tem de ser
recuperável.

| Arquivo | O que executa | Custo |
|---|---|---|
| [`prompt_nb04_analise_fatorial.md`](prompt_nb04_analise_fatorial.md) | O Notebook 04 inteiro, em quatro fases, com as skills por fase | sessão longa; **já foi executado** em 16–17/09/2026 |
| [`prompt_auditoria_integral.md`](prompt_auditoria_integral.md) | A auditoria do projeto de ponta a ponta, em sete fases | sessão longa; roda a pipeline inteira |
| [`prompt_graphify_atualizacao.md`](prompt_graphify_atualizacao.md) | A atualização do grafo do repositório em `graphify-out/` | o grafo está desatualizado desde 10/08/2026 |

> Prompt executado é registro, não receita a repetir. O do NB04 descreve a etapa como
> pendente porque é anterior à execução — o que saiu dela está em
> [`../relatorios/Relatorio_Analise_Fatorial_NB04.md`](../relatorios/Relatorio_Analise_Fatorial_NB04.md).
