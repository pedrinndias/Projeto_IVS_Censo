# Estado — ontologia dos dados (nov/2026)

Prompt: [`prompt_ontologia_dados_2026-11.md`](prompt_ontologia_dados_2026-11.md). Branch `feat/ontologia-dados`. Nada commitado.

**Ponto atual:** sessão de 23/11 fechada. Lotes 1 e 2 certificados (27/128). Por decisão do Pedro, os lotes 3+ ficam para outra
sessão. Commit e bloco do CLAUDE.md aguardam o OK dele.

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
- **Fase 5 (passo 1):** `gabarito.py` regerado: o recálculo confere com o banco, e o `gabarito.json` saiu inalterado.
  `checar.py` → `27/128`; `resumo.md` regerado.

## O que falhou ou desviou
- `graphify query` não apontou o código (devolveu READMEs e relatórios); as linhas vieram de `grep` em `src/` e `scripts/`.
- `fonte` só aceita `dicionario | usuario | amostra`, então o `arquivo:linha` foi para `referencia`, não para `fonte`.
- Nenhum item NÃO BATE.

## Não executado (registrado)
- Fase 5, passo 2 (reavaliar as 13 perguntas com `/anthropic-skills:skill-creator`): sem OK do Pedro.
- Fase 6 (camada do IVS final): não executada, porque o IVS não está congelado.

## O que falta
1. **Lotes 3+ (~101 colunas, a maioria `fonte: dicionario`), noutra sessão:** apresentar em lotes de até 15, por tabela. Começar
   pelas 93 colunas de `setores_censitarios` ainda `certificado: false`, depois as 6 de `dicionario_variaveis` e as 2 de
   `metadados`. Pedido de cada lote: descrição × `dicionario_variaveis` (consulta) e perfil no recorte. Gravar `true` só com
   "aprovo".
2. Fase 5, passo 2 (opcional, com OK) e Fase 6 (só com o IVS congelado e o arquivo final nomeado pelo Pedro).
3. Fase 7, pendente de OK: commit (mensagem abaixo), bloco "Dados" no `CLAUDE.md` do projeto, O03 (a branch não está na `main`;
   a `main` está 2 commits à frente do `origin`: `8e1e1ca`, `482c37d`).

Mensagem de commit proposta (só com o nome do Pedro, sem trailer):
`feat(ontologia): armadilhas D03/D04, referências arquivo:linha e lotes 1-2 certificados`

Os scripts `certificar.py`, `aplicar_proposta.py` e `validar.py` estavam no scratchpad da sessão de 23/11 e podem ter sido
apagados. `certificar.py` só troca `certificado: false` por `true` na linha do nó pedido.
