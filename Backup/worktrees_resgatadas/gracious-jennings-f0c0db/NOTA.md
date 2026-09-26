# Nota — arquivo resgatado da worktree órfã `gracious-jennings-f0c0db`

**Arquivo:** `banco_de_dados/eda/diagnostico_esgoto_312_vs_249.csv`
**Data do arquivo (mtime):** 22/05/2026

## Por que foi copiado para cá

Verificação da Fase A (A.6, `prompt_nb05_ivs_final_2026-09.md`): hash do conteúdo bruto
e do conteúdo normalizado (CRLF → LF) não bate com nenhum dos 883 blobs de
`git rev-list --all --objects` (todo o histórico, todos os refs). Pelo critério do
prompt isso conta como "único de verdade", então a pasta da worktree não foi movida
para a Lixeira e este arquivo foi copiado para cá.

## Contexto

O padrão `banco_de_dados/**/diagnostico_esgoto_*.csv` está no `.gitignore` (linha 20)
— arquivos assim nunca entram no git, então não achar o hash em nenhum commit já era
esperado, não é por si só sinal de conteúdo perdido.

O repositório principal tem hoje um arquivo com o mesmo nome
(`banco_de_dados/eda/diagnostico_esgoto_312_vs_249.csv`, também fora do git, 106.282
linhas nesta cópia da worktree), e o conteúdo **difere** do desta worktree (`diff`
simples; não comparado célula a célula). Não dá para saber, só por isso, qual dos dois
é o mais atual ou o correto — registrado aqui para quem decidir.
