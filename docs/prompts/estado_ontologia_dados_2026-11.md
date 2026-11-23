# Estado — ontologia dos dados (nov/2026)

Prompt: [`prompt_ontologia_dados_2026-11.md`](prompt_ontologia_dados_2026-11.md). Branch `feat/ontologia-dados`. Commits: `9f8210e` (lotes 1-2) e o do `CLAUDE.md`.

**Ponto atual:** ontologia 100% certificada (**128/128**) e reavaliada (13/13 com Sonnet e Haiku). Banco da entrega regerado em
23/11 com o D04 corrigido e auditado: os dados são idênticos aos de 22/10, e o código está estável (170/170 testes). Prompt e
auditoria de 22/11 versionados. Tudo na `main` e no `origin`. Fase 6 não executada: o IVS não está congelado.

## O que funcionou (com evidência)
- **Fase 0:** branch certa; `checar.py` → `certificado: 0/128 itens`, sem PROBLEMA.
- **Fase 1:** perfil regerado no scratchpad (`--dicionario dicionario_variaveis`). O bloco `tabelas` é idêntico ao de
  `ontologia/perfil.json` (3 tabelas; 108/108 colunas cobertas pelo dicionário). A fonte não mudou.
- **Fase 2:** origem de cada métrica e do recorte com `arquivo:linha`, e fatos D03/D04/Dados_sig conferidos no banco. Tudo em
  `ontologia/avaliacao/proposta_alteracoes_2026-11.md`.
- **Fase 3:** `gabarito.py` regerado: saiu idêntico, e o recálculo confere com o banco. As 8 métricas e o recorte saíram com SQL
  montado do YAML: todos BATEM com o recálculo (dif. ≤ 1e-17), com Q02/Q05 e com a tabela aprovada em 11/10
  (`scripts/pecas_relatorio_raic.py:73-81`, n e média de cada indicador). As 3 tabelas também batem com as granularidades.
  Tabela em `ontologia/avaliacao/certificacao_2026-11.md`.
- Parada 1: o Pedro aprovou em 23/11. Proposta aplicada em `ontologia/ontologia.yaml` (+32 −7); `checar.py` sem PROBLEMA (0/128);
  `resumo.md` regerado (77 linhas).
- **Lote 1:** aprovado pelo Pedro em 23/11. `certificado: true` nas 8 métricas, em `recortes.analise` e nas 3 tabelas;
  `checar.py` → `12/128 itens`; `resumo.md` regerado. Script de certificação: `certificar.py` no scratchpad, que troca só a
  linha `certificado` do nó pedido.
- **Lote 2:** aprovado pelo Pedro em 23/11, com uma correção: a armadilha de `V00001` foi reescrita (NULL nos 1.015 SIGILOSO
  e nos 1.736 ZERADO; nunca no recorte) e a coluna ficou com `fonte: usuario`. `certificado: true` nas 15 colunas;
  `checar.py` → `27/128 itens`; `resumo.md` regerado.
- **Lotes 3 a 10 (101 itens):** evidência por item: descrição × `dicionario_variaveis` (92/93; `urbano` corrigido antes) ×
  dicionário oficial do IBGE (62/62 `V*` idênticas); perfil no recorte; 22 fórmulas recalculadas (diferença 0). Principais
  correções: armadilha das 22 `pct_*` (no recorte, todo NULL vem do numerador inteiro sigiloso, até 15.897 setores); armadilha
  das 3 métricas de saneamento; `prop_70mais_entre_60mais` (0 a 100, não proporção); escala e NULL de `iep_setor`/`rdi_setor`;
  `NM_BAIRRO` (39,8% NULL); `NM_FCU`; valores de `Moradia_Predominante` e da agrupada; unidade de `V00005`/`V00006`
  (pessoas); `tema`, `origem`, `arquivo_fonte` e `formula` em `dicionario_variaveis`. Itens corrigidos → `fonte: usuario`.
  Depois: `checar.py` 128/128; gabarito inalterado; as métricas continuam BATENDO; `resumo.md` com 103 linhas.
- **Fase 5 (passo 1):** `gabarito.py` regerado: o recálculo confere com o banco, e o `gabarito.json` saiu inalterado.
  `checar.py` → `27/128`; `resumo.md` regerado.

## O que falhou ou desviou
- `graphify query` não apontou o código (devolveu READMEs e relatórios); as linhas vieram de `grep` em `src/` e `scripts/`.
- `fonte` só aceita `dicionario | usuario | amostra`, então o `arquivo:linha` foi para `referencia`, não para `fonte`.
- Nenhum item NÃO BATE.

- **Reavaliação (Fase 5, passo 2), com OK do Pedro em 23/11:** dois agentes novos, Sonnet e Haiku, com o protocolo de
  `resultados.md` (usei o Agent direto em vez do `skill-creator`, por ser o mesmo protocolo e mais barato). Sonnet 13/13,
  73.822 tokens, 3 chamadas; Haiku 13/13, 86.392 tokens, 7 chamadas. Detalhe em `ontologia/avaliacao/resultados.md`.
- **D04:** `scripts/gerar_entrega_orientadora.py` grava os números de `metadados` sem separador de milhar e renomeia a chave
  para `cd_setor_excluido_de_renda_media_sem_extremo` (commit `c32b7c9`). Testado gravando num diretório temporário: CAST dá
  109032. Os 6 testes da entrega passam; o ruff tem os mesmos 5 avisos de antes. O banco entregue (22/10) **não** foi regerado,
  e a armadilha de `metadados.valor` diz isso.
- **Revisão das 40 correções:** os 8 números escritos à mão nas correções foram reconferidos no banco e batem.
- **O03:** `main` avançada por fast-forward até a `feat/ontologia-dados`, sem troca de branch, e enviada ao `origin`.

- **Regeração do banco (23/11):** cópia dos `.db` antigos guardada; CSVs byte a byte iguais; `setores_censitarios` e
  `dicionario_variaveis` idênticos nos dois bancos; `metadados` só com as mudanças esperadas. `pytest`: um teste lia a chave
  antiga e foi atualizado, depois 170/170. As falhas dos verificadores de decks são anteriores (C09 e item 4, sem leitura do
  banco). Perfil regerado; armadilha de `metadados.valor` reescrita, com o D04 como histórico. Relatório:
  `ontologia/avaliacao/auditoria_regeracao_2026-11-23.md`.
- **Documentos:** `docs/prompts/prompt_ontologia_dados_2026-11.md` e `docs/relatorios/Auditoria_Projeto_e_Dados_2026-11-22.md`
  versionados (os links da ontologia deixam de estar quebrados).

## Não executado (registrado)
- Fase 6 (camada do IVS final): não executada, porque o IVS não está congelado.

## O que falta
1. **IVS final (Fase 6):** só depois de o IVS ser congelado e de o Pedro dizer qual arquivo é o final. A revisão de ponta a
   ponta recomenda congelar como proposta com prazo de veto da orientadora; a decisão é dela.
2. **Avisar a orientadora** de que o `.db` foi regerado: os dados são os mesmos, e só a tabela `metadados` mudou de formato.
3. Revisão do Pedro, quando quiser, das 40 correções aprovadas em bloco (lista em `certificacao_2026-11.md`).
4. Pendências anteriores, fora da ontologia: `verificar_relatorio_descritivo.py` com `IndexError` (C09) e o item 4 de
   `verificar_versoes_fatorial.py` (células dos decks VP09–VP11).
5. Sugestão para a skill (fora do projeto): o `resumo.py` marcar certificação também nas colunas.
