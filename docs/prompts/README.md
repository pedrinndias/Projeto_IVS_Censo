# `docs/prompts/` — prompts executáveis

Prompts escritos para colar numa sessão de Claude Code aberta na raiz do projeto. Ficam
versionados pelo mesmo motivo que os scripts: o que produziu um resultado tem de ser
recuperável.

| Arquivo | O que executa | Custo |
|---|---|---|
| [`prompt_nb04_analise_fatorial.md`](prompt_nb04_analise_fatorial.md) | O Notebook 04 inteiro, em quatro fases, com as skills por fase | sessão longa; **já foi executado** em 16–17/09/2026 |
| [`prompt_auditoria_integral.md`](prompt_auditoria_integral.md) | A auditoria do projeto de ponta a ponta, em sete fases | sessão longa; roda a pipeline inteira |
| [`prompt_graphify_atualizacao.md`](prompt_graphify_atualizacao.md) | A atualização do grafo do repositório em `graphify-out/` | a parte de **código** foi atualizada em 25/09/2026 com `graphify update .`, sem custo de modelo; a leitura semântica dos **documentos** continua a de agosto |
| [`prompt_demandas_orientadora_2026-09.md`](prompt_demandas_orientadora_2026-09.md) | As 11 demandas da orientadora de setembro e as correções da revisão geral, em seis fases com teto de chamadas | uma sessão por fase; **não executado** |
| [`prompt_nb05_ivs_final_2026-09.md`](prompt_nb05_ivs_final_2026-09.md) | Os testes de especificação (renda, rotação, pesos na oblíqua, lixo, banheiro graduado, o que o índice acrescenta à renda) e o NB05, em quatro fases | um agente por fase; Fases A-C concluídas em 26-27/09/2026, Fase D em andamento (notebook e relatório prontos, slides pendentes) — [`../relatorios/Relatorio_IVS_Final_NB05.md`](../relatorios/Relatorio_IVS_Final_NB05.md) |
| [`prompt_graphify_update_2026-09.md`](prompt_graphify_update_2026-09.md) | A atualização do grafo de contexto (`graphify-out/`) com pré-voo de custo, `.graphifyignore` e extração em ondas | sessão nova; para antes de passar de 6 subagentes |
| [`prompt_economia_tokens.md`](prompt_economia_tokens.md) | Regras de uso de tokens e de escolha de modelo, a partir do que foi medido em setembro, com uma versão curta para o `CLAUDE.md` | colar no início da sessão |

> Prompt executado é registro, não receita a repetir. O do NB04 descreve a etapa como
> pendente porque é anterior à execução — o que saiu dela está em
> [`../relatorios/Relatorio_Analise_Fatorial_NB04.md`](../relatorios/Relatorio_Analise_Fatorial_NB04.md).
