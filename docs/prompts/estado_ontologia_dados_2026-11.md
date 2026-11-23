# Estado — ontologia dos dados (nov/2026)

Prompt: [`prompt_ontologia_dados_2026-11.md`](prompt_ontologia_dados_2026-11.md). Branch `feat/ontologia-dados`. Commits: `9f8210e` (lotes 1-2) e o do `CLAUDE.md`.

**Ponto atual:** ontologia 100% certificada (**128/128**). Lotes 3 a 10 aprovados em bloco pelo Pedro em 23/11 ("Siga todos os
lotes de forma automática…"), com 40 correções documentadas em `ontologia/avaliacao/certificacao_2026-11.md`. As mudanças dos
lotes 3 a 10 ainda não foram commitadas.

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

## Não executado (registrado)
- Fase 5, passo 2 (reavaliar as 13 perguntas com `/anthropic-skills:skill-creator`): sem OK do Pedro.
- Fase 6 (camada do IVS final): não executada, porque o IVS não está congelado.

## O que falta
1. Commit das mudanças dos lotes 3 a 10 (com OK do Pedro).
2. Revisão do Pedro, quando quiser, das 40 correções aprovadas em bloco (lista em `certificacao_2026-11.md`).
3. Fase 5, passo 2 (reavaliação com modelos, opcional, com OK) e Fase 6 (só com o IVS congelado).
4. O03, pendente de OK: juntar `feat/ontologia-dados` à `main` e enviar ao `origin` (a `main` está 2 commits à frente:
   `8e1e1ca`, `482c37d`).
5. Fora da ontologia: corrigir o formato de `metadados` (D04) em `scripts/gerar_entrega_orientadora.py`.

Os scripts (`certificar.py`, `validar.py`, `evid_lotes3.py`, `lotes3a10.py`) e o log `log_lotes3a10.json` ficaram no scratchpad
da sessão de 23/11 e podem ter sido apagados. O que importa deles está em `certificacao_2026-11.md`.
