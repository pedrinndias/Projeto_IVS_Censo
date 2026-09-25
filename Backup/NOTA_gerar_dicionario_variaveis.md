# Nota — `gerar_dicionario_variaveis.py` resgatado (HIG-08)

**Origem:** `.claude/worktrees/flamboyant-davinci-bb1785/scripts/gerar_dicionario_variaveis.py`
(mtime 30/05/2026), uma worktree órfã — `.git` do diretório aponta para um caminho de outra
máquina/SO (`D:/Iniciação Cientifica/Projeto_IVS_Censo22/...`), não é mais um repositório git
válido. `git log --all` não encontra este caminho em nenhum commit: o script nunca foi
versionado no repositório principal.

**O que ele faz:** monta, com `openpyxl`, o `Dicionario_Variaveis_IVS_Censo2022.xlsx` em 7 abas
(Inicio, Componentes_IVS, Variaveis_Brutas_Censo, Variaveis_Derivadas, Guia_por_Arquivo,
De_Para_2010_2022, Decisoes_Metodologicas) — as mesmas abas do arquivo hoje em
`docs/Apresentacoes_IVS/dicionarios/Dicionario_Variaveis_IVS_Censo2022.xlsx`.

**Estado ao ser resgatado (só copiado para cá, nada executado nem integrado):**
- Caminho de saída no script é `docs/Dicionario_Variaveis_IVS_Censo2022.xlsx` (raiz de `docs/`),
  desatualizado frente à localização atual do arquivo
  (`docs/Apresentacoes_IVS/dicionarios/`) — a reorganização de `docs/` é posterior a este script.
- O hash do `.xlsx` gerado por esta cópia do script (visto numa das worktrees órfãs) **não bate**
  com o hash do arquivo hoje versionado — não foi conferido se a diferença é só metadado do
  `openpyxl` (data de criação embutida) ou conteúdo; não decidido aqui.
- Não adicionado a `scripts/README.md` nem chamado por nenhum outro script: decisão de wiring
  (caminho de saída, conferência de conteúdo, teste) fica para quem tratar o achado HIG-08 de
  fato, fora do escopo do Lote D (que só pedia resgatar antes de qualquer limpeza de worktrees,
  HIG-07 — as worktrees órfãs em `.claude/worktrees` não foram apagadas).
