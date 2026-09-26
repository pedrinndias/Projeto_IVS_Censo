# Nota — arquivo resgatado da worktree órfã `flamboyant-davinci-bb1785`

**Arquivo:** `docs/Dicionario_Variaveis_IVS_Censo2022.xlsx` (caminho antigo, dentro da worktree)
**Data do arquivo (mtime):** 30/05/2026

## Por que foi copiado para cá

Verificação da Fase A (A.6, `prompt_nb05_ivs_final_2026-09.md`): hash do conteúdo bruto
e do conteúdo normalizado (CRLF → LF) não bate com nenhum dos 883 blobs de
`git rev-list --all --objects` (todo o histórico, todos os refs). Pelo critério do
prompt isso conta como "único de verdade", então a pasta da worktree não foi movida
para a Lixeira e este arquivo foi copiado para cá.

## O que a comparação célula a célula mostrou (openpyxl, mesmo método do item 8.1)

Das 7 abas, só **1 linha** difere do `.xlsx` hoje versionado
(`docs/Apresentacoes_IVS/dicionarios/Dicionario_Variaveis_IVS_Censo2022.xlsx`):

- Aba `Variaveis_Brutas_Censo`, variável V00398 — descrição "queimado" (nesta cópia)
  vs "caçamba de serviço de limpeza" (versão atual).

Isto é exatamente a correção do commit `4922909` (HIG-09). Ou seja: este arquivo é um
retrato do dicionário **anterior** a essa correção, não é conteúdo novo. Mantido aqui
por completude e registro, não por valor de conteúdo aparente — quem revisar pode
decidir se ainda serve para algo.
