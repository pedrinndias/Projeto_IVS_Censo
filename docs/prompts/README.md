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
| [`prompt_analises_exploratorias_versoes_2026-10.md`](prompt_analises_exploratorias_versoes_2026-10.md) | Uma análise exploratória completa por versão do IVS e da base (31 versões em seis ondas), cada uma com tabelas, figuras, catálogo e um deck extenso, e a síntese entre elas | 14 sessões curtas em Sonnet, uma por lote, com teto de 10 a 40 chamadas; **não executado** |
| [`prompt_relatorio_descritivo_2026-10.md`](prompt_relatorio_descritivo_2026-10.md) | O relatório descritivo do andamento para a orientadora: as demandas de setembro e como foram cobertas, um indicador por slide, a descritiva da fatorial e os pedidos dela sobre a fatorial, com processo de correção registrado (`relatorio_descritivo/`) | executado em 07/10/2026 (lotes 0 a 5, deck v2, 87 slides); correções pelo protocolo da seção 5 |
| [`prompt_apoio_reuniao_v4_2026-10.md`](prompt_apoio_reuniao_v4_2026-10.md) | A v4 do relatório descritivo, só para o Pedro na reunião remota: depois de cada slide da v3, um slide de apoio com o que é o conteúdo, as perguntas prováveis da orientadora com resposta e de onde vem, e os números para saber de cor; mais perguntas gerais e glossário | executado em 09/10/2026 sem parar: v4_APOIO com 295 slides e 445 perguntas, verificador verde (C-09) |
| [`prompt_simplificacao_correcoes_2026-10.md`](prompt_simplificacao_correcoes_2026-10.md) | A simplificação geral do código (sem mudar estrutura nem saída, com prova de equivalência) e a correção dos 8 erros da revisão `/ponytail` de 22/10, regerando as saídas e listando os números que mudaram nos entregáveis | uma sessão em Sonnet, cinco fases sem parar, ~155 chamadas; ramo `simplificacao-codigo`; **não executado** |
| [`prompt_versoes_fatorial_108_2026-10.md`](prompt_versoes_fatorial_108_2026-10.md) | A análise fatorial em 108 versões (renda × lixo × água canalizada × banheiro × moradia), com deck principal, caderno de 108 fichas e planilha (`versoes_fatorial/`) | executado em 08/10/2026 (lotes 0 a 5 sem parar); 24 de 108 elegíveis; correções pela seção 5 |

> Prompt executado é registro, não receita a repetir. O do NB04 descreve a etapa como
> pendente porque é anterior à execução — o que saiu dela está em
> [`../relatorios/Relatorio_Analise_Fatorial_NB04.md`](../relatorios/Relatorio_Analise_Fatorial_NB04.md).
