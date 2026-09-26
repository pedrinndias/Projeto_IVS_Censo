# Prompt de execução — testes de especificação e o NB05 (IVS final)

**Para quem executa:** uma sessão de Claude Code aberta na raiz do repositório.
**Escrito em:** 26/09/2026, depois das Fases 0–5 de
[`prompt_demandas_orientadora_2026-09.md`](prompt_demandas_orientadora_2026-09.md).
**Estado de partida:** `master` em `6800484`, 90 testes verdes, 410 arquivos versionados.

---

## Como usar

**Uma fase por agente, em contexto limpo.** Este documento é único; a execução não. Cada
fase é executada por um agente novo que lê só: a seção 0 (regras), a seção 1 (fatos), a
seção 2 (decisões) e o bloco da sua fase. O estado vai para
`docs/prompts/estado_nb05_2026-09.md`, criado na Fase A.

| Fase | O quê | Itens do pedido | Teto | Modelo |
|---|---|---|---:|---|
| **A** | pendências pequenas, inferências, worktrees | 7, 8.1, 8.2, 8.3, worktrees | 35 | Sonnet |
| **B** | extrair `V00237` e construir o banheiro graduado | 5 | 30 | Sonnet |
| **C** | o motor de especificações do IVS e todos os testes | 1, 2, 3, 4, 5, 6 | 45 | Opus |
| **D** | o notebook NB05, o relatório e os slides | 9 | 40 | Sonnet |

**Ordem obrigatória:** A → B → C → D. A depende de nada; B muda a base; C usa a base de B;
D mostra o que C calculou. Uma trava que falha para a execução naquela fase.

**Lição das execuções anteriores, obrigatória:** os agentes estouraram o teto em três de
dez fases porque começaram lendo demais. Aqui cada fase traz a receita — **não explore o
repositório além do que o bloco manda ler.**

---

## 0. Regras

### 0.1 Orçamento
1. Teto de chamadas da fase; ao chegar a 85%, pare, grave o estado, commite o que estiver
   verificado e devolva "não concluída".
2. Uma verificação = um script. Saída sempre truncada (`| head -60`). Nunca imprimir arquivo
   inteiro; `.ipynb` por JSON; CSV por pandas.
3. Não reexecutar `scripts/proporcoes_brasil.py`. O NB01 só roda na Fase B.
4. Sem subagentes, workflows ou skills dentro de uma fase.

### 0.2 Projeto
- Código do projeto só com numpy e pandas. Conferência externa (scipy, statsmodels) só em
  `uv run --with ...` fora do repositório.
- **Não decidir pela orientadora.** Onde houver escolha, calcular todas as alternativas e
  deixar a escolha registrada como pergunta. O NB05 **propõe** uma especificação de
  referência por critérios escritos **antes** de ver os resultados (seção 2.2) — e diz que
  é proposta.
- Todo número de documento ou slide sai de CSV gerado por script.
- O deck `docs/Apresentacoes_IVS/Analise_Fatorial_NB04_2026-09.pptx` (106 slides, 21
  marcações "EXPLICAR") nunca é regerado: só recebe bloco anexado com
  `scripts/juntar_decks.py` e é validado depois (seção 1).
- Commits: um por tema, mensagem em português no estilo do histórico, autor
  `Pedro Dias Soares` (configuração local do repositório já está certa). **Nenhum trailer**
  — nada de `Co-Authored-By`, `Claude-Session`, "Generated with". Depois de cada commit:
  `git log -1 --format='%an|%(trailers)'`. Antes e depois de cada commit:
  `git ls-tree -r HEAD | wc -l` ≥ 410 (houve um incidente de índice numa sessão anterior).
  Use `git add` só com caminhos explícitos, um tema por vez. **Sem push** — o agente
  principal faz o push depois de conferir tudo.
- Comentários de código em português, curtos, no estilo do arquivo; sem menção a IA.
- Não apagar arquivo versionado. Fora do git, só a Fase A mexe — e move para a Lixeira.
- Toda mudança de código com teste; `pytest` verde no fim de cada fase.

---

## 1. Fatos verificados — não redescobrir

**Base.** `banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db`, tabela
`setores_censitarios`, 109.032 × 105. Abrir em modo só leitura. Recorte:
`pd.to_numeric(urbano) == 1` e `Dados_sig == 'OK'` → 104.108 setores. FCU em `is_fcu`.

**Rendas disponíveis.** `renda_media` (original, com o setor 310620005650366 a
R$ 170.418,06), `renda_media_sem_extremo` (o setor vira NaN),
`renda_media_mediana_mun` (o setor recebe a mediana de BH, R$ 3.058,24). A fatorial usa a
renda **invertida** (`-renda`).

**Camada fatorial** (`src/ivs_censo/fatorial.py`, corrigida em 25/09): `kmo`, `bartlett`,
`smc`, `acp`, `horn`, `varimax` (converge por `max|ΔR| < 1e-10`), `rotacao_promax`,
`comunalidades_obliquas`, `escores_regressao(R, cargas, phi=None)` (com `phi`, usa a matriz
estrutura, o certo em solução oblíqua), `matriz_correlacao`, `postos`, `alinhar_cargas`,
`rodar_cenario` (devolve um cenário inteiro num dicionário), `diagnosticar`.

**Motor da grade** (`scripts/fatorial_ampliada.py`, Fase 2): funções `carregar`, `montar`
(listwise nas variáveis do cenário; `renda=` escolhe a versão da renda), `rodar`,
`sensibilidade`, `comparacao`, `figuras`, `gravar`; saídas em
`banco_de_dados/eda/fatorial_ampliada/`. **O motor do NB05 reaproveita estas funções.**

**Como o índice do NB04 é construído** — e o NB05 constrói igual: `pesos_indice(vmax, rep)`
manda cada variável para a dimensão em que tem a maior carga absoluta e reparte o peso da
dimensão (`rep`, a repartição entre fatores) pelo quadrado da carga dentro dela;
`indice_01(d, colunas, peso)` normaliza cada variável por min-max **global** e soma com esses
pesos; `auc_postos` calcula a AUC por Mann–Whitney. As três funções estão no motor da Fase 2.

**Resultados que servem de trava:** IVS-7 (S0) KMO 0,7826; IVS-6 sem lixo (S1) pesos
Varimax 65,01/34,99; AUC do índice S1 0,8131; AUC da renda invertida sozinha 0,8819; AUC da
média de postos com pesos iguais 0,8533. Repartição oblíqua de S1: 65,82/34,18 pela matriz
padrão, 59,64/40,36 pela estrutura; Φ 0,5215.

**Banheiro.** `pct_sem_banheiro` = V00495/V00001 ("sem banheiro de uso exclusivo com
chuveiro e vaso"); `pct_sem_banheiro_nem_sanitario` = V00238/V00001. V00238 ≤ V00495 em
90.858 de 90.858 setores. **V00237** ("apenas sanitário ou buraco para dejeções") está na
coluna 149 de `dados/Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv`
(747 MB) e **não foi extraída**; V00236 ("apenas banheiro de uso comum") está no banco. A
lista de colunas extraídas vive em `src/ivs_censo/fontes.py` (linha ~66, bloco banheiro).

**Método de referência (IVS-BH 2012, `docs/referencias/`).** Conversão de escala min-max
(`(x − mín) / (máx − mín)`) e renda invertida como `1 − renda/máximo`. A regra das faixas
(baixo, médio, elevado, muito elevado) e os pesos da literatura (60/40) estão em
`docs/referencias/indice_vulnerabilidade2012 (2).pdf` — extrair com pypdf e citar a página.

**Deck e validação.** Validador OOXML da skill pptx:
`/Users/pedro/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/3766a732-e014-46b5-9805-e4f03319bcc4/a61a5a39-d6ca-41c8-b16f-0a03b0893fac/skills/pptx/scripts/office/validate.py`,
rodado com `uv run --with lxml --with defusedxml --with python-pptx python <validate.py>
<deck_novo> --original <deck_do_HEAD>`. Erro novo em relação ao original = não commitar.
Editar texto de slide só por `run.text`; nunca reordenar filhos de `<p:presentation>`.

---

## 2. Decisões e critérios

### 2.1 As dimensões de especificação que o NB05 testa

| Dimensão | Alternativas | Item do pedido |
|---|---|---|
| Renda | original · sem extremo · mediana municipal | 1 |
| Rotação | sem rotação · Varimax · promax | 2 |
| Pesos na oblíqua | SS da matriz padrão · SS da estrutura · variância única (comunalidades de P) · 50/50 · 60/40 da literatura | 3 |
| Lixo | com · sem | 4 |
| Banheiro | fora · V00495 · graduado (Fase B) | 5 |
| Normalização do índice | min-max **dentro do município** (intraurbano, referência) · min-max global (sensibilidade) | — |
| Faixas | regra do IVS-BH 2012 (extraída do PDF) · quartis dentro do município (sensibilidade) | — |

Pesos na Varimax: SS das cargas rotacionadas, 50/50 e 60/40. Sem rotação: um fator só
(sem pesos entre dimensões) — é o teste de "um fator ou dois".

### 2.2 Critérios da especificação de referência — fixados ANTES de rodar

Uma especificação é **elegível** se: KMO ≥ 0,70; MSA de toda variável ≥ 0,50; comunalidade
de toda variável ≥ 0,30 (se alguma falhar, a especificação é registrada como inelegível —
não se corrige tirando a variável); os dois fatores interpretáveis (cada variável com carga ≥ 0,40
em algum fator).

Entre as elegíveis, a **referência proposta** é a de melhor posição média em três
critérios, com peso igual: (a) estabilidade — menor amplitude do peso do fator 1 ao deixar
um município de fora; (b) validade discriminante **dentro do município** — mediana, entre
os 70, da AUC contra FCU; (c) parcimônia — menos variáveis. Empate: a mais próxima do
IVS-BH 2012. Isto é **proposta**, não decisão: o NB05 mostra a referência e as
alternativas lado a lado, e a escolha final fica registrada como pergunta à orientadora.

### 2.3 Perguntas que continuam dela
Qual renda; qual rotação; como dividir os pesos; se o lixo entra; se o banheiro entra e em
qual versão; normalização municipal ou global; regra das faixas. O NB05 responde a cada uma
com números, e não fecha nenhuma.

---

## FASE A — Pendências pequenas, inferências e worktrees
**Teto 35. Itens 7, 8.1, 8.2, 8.3 e a limpeza das worktrees.**

**A.1 — Estado.** Crie `docs/prompts/estado_nb05_2026-09.md` com as fases A–D, a tabela
dos itens 1–9 do pedido e uma seção "Perguntas à orientadora".

**A.2 — Item 7: as três inferências dos agentes, transformadas em verificação.** Leia em
`docs/prompts/estado_demandas_2026-09.md` só as linhas que citam cada uma (grep). Para
cada uma, escreva no estado: **o que o agente inferiu, por que inferiu** (a causa — ex.:
fonte que não nomeava os documentos, orçamento esgotado, número reaproveitado sem script)
e **o resultado da verificação determinística** que substitui a inferência:
1. *D4 (−0,81 × 0,784):* `git grep -n -e '−0,81' -e '-0,81' -e '−0,8106'` em todo o
   repositório; toda ocorrência analítica tem de ter a nota do valor listwise (0,784) no
   mesmo parágrafo. Liste as que não têm e corrija-as (é texto; um commit).
2. *NBS-4 (0,033 e 82,8% no NB02):* recalcule num script a matriz de correlação do NB02
   par a par × listwise sobre o recorte urbano, com as mesmas variáveis da célula, e
   confirme ou corrija os dois números no markdown do NB02 (sem reexecutar o notebook).
3. *HIG-08 (gerador do dicionário):* ver A.3.

**A.3 — Item 8.1:** em `Backup/gerar_dicionario_variaveis.py`, troque o caminho de saída
antigo pelo atual (`docs/Apresentacoes_IVS/dicionarios/Dicionario_Variaveis_IVS_Censo2022.xlsx`),
mantendo-o como script de backup (não entra em `scripts/`). Rode-o gravando em `/tmp` e
compare célula a célula com o `.xlsx` versionado (openpyxl): liste as diferenças. Se forem
só as duas já esperadas (V00398 "caçamba") e metadado, registre; se houver outras,
registre sem corrigir. Atualize `Backup/NOTA_gerar_dicionario_variaveis.md`.

**A.4 — Item 8.2:** o slide 45 de
`docs/Apresentacoes_IVS/complementos/EDA_Central_IVS_2026-09_rev2.pptx` cita um caminho
anterior à reorganização de `docs/`. Esse deck **é gerado** por
`scripts/gerar_deck_eda_central.js`: corrija o caminho no gerador (grep pelo caminho
antigo) e regere o deck avulso para o mesmo arquivo. Confira: mesmo número de slides e
texto idêntico ao anterior exceto o caminho (script de comparação slide a slide com
python-pptx via `uv run`). Valide com o validador da seção 1. **Se a regeração mudar
qualquer outra coisa além do caminho**, não use o deck regerado: corrija só o texto do
slide 45 no deck existente por `run.text` e registre a divergência gerador × deck no estado.

**A.5 — Item 8.3:** reexecute `scripts/eda_extremo_belo_horizonte.py` e
`scripts/auditoria_renda.py` — nos dois modos, o padrão e `--sem-extremo` (que grava em
`eda/atualizada/`); confira no código os argumentos antes de rodar — e confirme com `git status` que **nenhum arquivo gerado
mudou** (a troca do filtro `astype(str)` não deveria alterar nada). Se algo mudar, pare e
reporte a diferença célula a célula — não commite a mudança.

**A.6 — Worktrees órfãs** (`.claude/worktrees/`, 5 pastas, 597 MB, fora do git). Uma
verificação em 26/09 achou em cada uma de 31 a 35 arquivos cujo conteúdo, byte a byte, não
existe em nenhum objeto do git — quase certamente as mesmas versões com fim de linha do
Windows (CRLF), mas isso não foi provado. Script: para cada arquivo de cada worktree,
normalize CRLF → LF e procure o hash no git (`git hash-object` do conteúdo normalizado +
`git cat-file -e`), inclusive em todo o histórico (`git rev-list --all --objects`). Resultado
por arquivo: idêntico ao git, idêntico após normalizar, ou **único de verdade**.
- Se **nenhum** arquivo for único de verdade: mova as cinco pastas para a Lixeira do macOS
  (`osascript -e 'tell application "Finder" to delete POSIX file "<caminho absoluto>"'`),
  nunca `rm`, e rode `git worktree prune`. Registre o espaço liberado.
- Se houver arquivo único de verdade: copie-o para `Backup/worktrees_resgatadas/<pasta>/`
  com uma nota, e **não** mova a pasta; registre no estado.

**A.7 —** `pytest` verde; commits por tema; estado atualizado no último commit.

---

## FASE B — O banheiro graduado (item 5)
**Teto 30.**

**B.1 — Extrair a V00237. Faça B.3 ANTES de regenerar**, para regenerar uma vez só:
acrescente `'V00237'` ao bloco de banheiro de `src/ivs_censo/fontes.py` (o NB01 deriva dele a
lista de colunas) e os dois indicadores de B.3 em `indicadores.py`. Então reexecute o NB01
com nbclient **numa cópia em /tmp, sem gravar saídas no `.ipynb` versionado** (o NB01 é
versionado sem saídas; lê 8 GB, ~30 s; grava a base bruta, que é ignorada pelo git), e depois
`scripts/gerar_entrega_orientadora.py` (~2 min). Travas: 109.032 linhas; todas as colunas
antigas idênticas às do `.db` do HEAD (compare por hash de cada coluna); as novas são só
`V00237` e as que os indicadores novos gerarem. **O número de colunas final é o que o gerador
produzir** — a base bruta passa de 68 colunas para 69, o banco de 105 para o que der;
atualize as citações com o número real.

**B.2 — A partição.** Num script, teste se
`V00495 = V00236 + V00237 + V00238 (+ resto)` em cada setor com as quatro presentes, e
descreva o resto (se existir, o que ele é segundo o dicionário do IBGE). Grave em
`banco_de_dados/eda/fatorial_ampliada/banheiro_particao.csv`.

**B.3 — Os indicadores.** Em `src/ivs_censo/indicadores.py`, dois indicadores novos,
simples, no padrão dos existentes: `pct_so_sanitario` = V00237/V00001 e
`pct_banheiro_comum` = V00236/V00001, com comentário de uma linha cada. O **banheiro
graduado** é definido no motor da Fase C, não no módulo:
`graduado = (1·V00236 + 2·V00237 + 3·V00238) / (3·V00001)` — escala ordinal de
gravidade (uso comum < só sanitário < nada). Teste: com dados sintéticos, 0 ≤ graduado ≤ 1
e graduado = 0 onde V00495 = 0.

**B.4 —** regere o quadro de indicadores e o dicionário da entrega (os geradores da Fase 1),
atualize as contagens onde forem citadas (`git grep -n -e "105 colunas" -e "68 colunas" -e
"26 indicadores"`) com os números reais, `pytest` verde, commits por tema.

---

## FASE C — O motor de especificações (itens 1, 2, 3, 4, 5 e 6)
**Teto 45. Modelo Opus.**

**C.1 — Leia só:** as assinaturas de `scripts/fatorial_ampliada.py` (grep `^def`), o
`README.md` de `banco_de_dados/eda/fatorial_ampliada/` e a regra das faixas e os pesos do
IVS-BH 2012 no PDF de `docs/referencias/` (pypdf, grep por "elevado", "faixa", "peso",
"0,4", "0,6"; cite a página). Se o PDF não trouxer a regra das faixas, use média ± 0,5 DP e
quartis como as duas alternativas e registre que a regra original não foi encontrada.

**C.2 — O motor:** `scripts/ivs_especificacoes.py`, importando do módulo e do motor da
Fase 2. Para cada especificação da seção 2.1 (combinações válidas; registre o total):
1. monta as variáveis (renda invertida na versão da especificação; lixo; banheiro), casos
   completos (listwise) — **registre n e os setores perdidos**;
2. adequação (KMO, MSA, Bartlett, comunalidades), Kaiser e Horn;
3. extração ACP, 2 fatores (1 no caso "sem rotação" como teste unifatorial), rotação,
   convenção de sinal (soma das cargas positiva);
4. pesos das dimensões pelo método da especificação (seção 2.1);
5. **o índice**, construído como o do NB04: pesos por `pesos_indice(vmax, rep)` (a
   repartição `rep` vem do método de pesos da especificação) e soma ponderada das variáveis
   normalizadas. Normalização global = `indice_01` do motor da Fase 2 (sensibilidade);
   normalização **dentro do município** = o mesmo, com mín e máx de cada município
   (referência, porque o IVS é intraurbano). Reaproveite as funções; não reescreva;
6. faixas pela regra do IVS-BH e por quartis municipais;
7. avaliação: AUC contra FCU **global** e **mediana da AUC dentro dos municípios** (só
   municípios com ao menos 30 setores de FCU e 30 fora; registre quantos); estabilidade
   (70 rodadas deixando um município de fora — **só para as elegíveis**, para caber no
   tempo); correlação de postos com a referência; % de setores que mudam de faixa em relação
   à referência. **As métricas de comparação entre especificações (AUC, correlação de postos,
   mudança de faixa) são calculadas também sobre a amostra comum a todas as especificações**
   — com n diferentes, a comparação na amostra própria mistura efeito da especificação com
   efeito da amostra. Registre as duas.

**C.3 — Item 6: o que o índice acrescenta à renda.** Para as elegíveis e para a
referência: (a) AUC do índice × AUC da renda invertida sozinha × média de postos com pesos
iguais, global e dentro do município; (b) **AUC dentro de estratos de renda** (decis de
renda dentro do município): se o índice ainda separa FCU entre setores de renda parecida,
ele acrescenta algo; (c) regressão logística FCU ~ renda e FCU ~ renda + índice, por IRLS
em numpy, com a diferença de deviance e de AUC. Registre, sem adjetivo, a conclusão que os
números sustentam. Declare o limite: FCU é critério do IBGE que já usa condições de
moradia — há circularidade parcial com as variáveis de saneamento.

**C.4 — Saídas** em `banco_de_dados/eda/ivs_especificacoes/`: `especificacoes.csv` (uma
linha por especificação, com elegibilidade e todas as métricas), `pesos.csv`,
`avaliacao.csv`, `acrescimo_renda.csv`, `estabilidade.csv`, `referencia.csv` (a proposta
e o porquê, pelos critérios da seção 2.2) e `ivs_referencia_por_setor.csv` — este **fora
do git** se passar de 5 MB (siga a regra `*_por_setor.csv` do `.gitignore`), com o gerador
versionado. README de procedência. Figuras (matplotlib, dpi 150, paleta do projeto):
AUC por especificação com a linha da renda sozinha; peso F1 por especificação; mapa de
concordância de faixas entre a referência e as principais alternativas.

**C.5 — Travas:** a especificação "IVS-6 (sem lixo), renda original, Varimax, pesos SS,
normalização global" tem de dar pesos **65,01/34,99** e AUC do índice **0,8131** — é o
`indice_01` do NB04, reconstruído com as mesmas funções; a renda invertida sozinha, na mesma
amostra, **0,8819**. Se não bater, pare antes de gravar qualquer CSV. Testes do motor em
`tests/test_ivs_especificacoes.py` (índice entre 0 e 1; faixas com as 4 classes; pesos
somando 1; reprodução da trava).

---

## FASE D — O NB05 (item 9)
**Teto 40.**

**D.1 — O notebook** `notebooks/Fase3_EDA_ELSI/05_Calculo_IVS_Final.ipynb`, escrito por um
único script com nbformat, **chamando o motor da Fase C** (não copia conta). Blocos:
(1) o que a orientadora pediu e onde está cada resposta; (2) as especificações testadas e
quantas são elegíveis; (3) renda; (4) rotação; (5) pesos na oblíqua; (6) lixo;
(7) banheiro; (8) o que o índice acrescenta à renda; (9) a referência proposta, pelos
critérios da seção 2.2, e as alternativas lado a lado; (10) o IVS final da referência:
distribuição, faixas, tabela por município, mapa de faixas em BH se houver geometria (se
não houver, tabela); (11) as perguntas que continuam dela. Comentários linha a linha no
estilo do NB04. Cada interpretação cita o número da célula anterior.
Execute uma vez com nbclient (timeout de 1.800 s por célula) e **salve com as saídas**, como
o NB04 e o 04b; confira que os CSVs regravados ficam idênticos aos da Fase C.

**D.2 — Relatório** `docs/relatorios/Relatorio_IVS_Final_NB05.md`: achados numerados,
método, a referência e as alternativas, limitações (circularidade do FCU, falácia
ecológica, perda de setores por sigilo), as perguntas à orientadora.

**D.3 — Slides:** gerador `scripts/gerar_slides_ivs_final.js` no padrão de
`scripts/gerar_slides_fatorial_ampliada.js` (uns 8 slides, todo número de CSV), anexado ao
deck com `scripts/juntar_decks.py` a partir da versão do HEAD, validado (seção 1),
conferido: slides = 106 + N, notas = 106 + N, 21 "EXPLICAR" intactas; renderize só os
slides novos e olhe cada um.

**D.4 — Documentação:** uma linha em `docs/relatorios/README.md`, em `docs/prompts/README.md`,
no README de `notebooks/Fase3_EDA_ELSI/` e no GUIA (status do NB05). `pytest` verde.
Commits por tema. Estado final com a tabela dos itens 1–9 preenchida.

---

## O que nunca fazer
- Escolher pela orientadora qualquer item da seção 2.3.
- Somar V00238 com V00495 ou usar o banheiro graduado sem a partição da Fase B.
- Regerar o deck de 106 slides.
- Rodar bootstrap.
- Apagar arquivo com `rm` fora do git, ou apagar arquivo versionado.
- Digitar número em documento, slide ou comentário.
- Commitar com trailer, ou dar push.
