# Prompt de execução — revisão de ponta a ponta do projeto (nov/2026)

**Pedido do Pedro (12/11/2026):** "Quero fazer uma revisão de ponta a ponta [...] códigos usando a skill
/ponytail, análises, apresentações, se eu estou seguindo no rumo certo, quero passar um pente fino no meu
projeto", executada "ininterruptamente, já adicionando as skills".
**Como usar:** sessão nova do Claude Code na raiz do projeto (`Projeto_IVS_Censo22`), modelo
**Claude Fable 5.2**, esforço **alto**, modo de permissão que não pare a cada comando (Auto ou Bypass). Cole:
*"Execute `docs/prompts/prompt_revisao_ponta_a_ponta_2026-11.md`, todas as fases, sem parar. Leia primeiro
`docs/prompts/estado_revisao_ponta_a_ponta_2026-11.md` se ele existir."*
**Saída:** `docs/relatorios/Revisao_Ponta_a_Ponta_2026-11.md` e um resumo de até 20 linhas no chat.
**Custo:** sessão longa, até ~170 chamadas somando os tetos. A Fase 4 usa `/council` (cerca de 11 chamadas
a mais, **custo alto**); apague o passo 4.3 se não quiser.

| Fase | O quê | Skills | Teto de chamadas |
|---|---|---|---:|
| 0 | Linha de base: estado, git, testes, leitura do que já se sabe | — | 12 |
| 1 | Código | `/ponytail-audit` | 45 |
| 2 | Análises e método | `/data:statistical-analysis`, `/data:validate-data` | 40 |
| 3 | Apresentações e relatórios | `/anthropic-skills:pptx`, `/anthropic-skills:pdf`, `/anthropic-skills:docx` | 35 |
| 4 | Rumo: objetivos × entregas × demandas | `/council` (uma pergunta) | 25 |
| 5 | Relatório final | — | 15 |

**Autorização de execução contínua.** O Pedro pediu, por escrito, execução de todas as fases sem parar e
escolheu as skills da tabela. Isto substitui, só para este prompt, duas regras do `CLAUDE.md` global: "pare ao
fim de cada etapa" e "nunca invoque uma skill por conta própria" (as skills da tabela estão autorizadas; as
outras, não). As demais regras dele continuam valendo. Nenhuma fase espera aprovação e nenhuma pergunta vai
ao Pedro no meio: diante de ambiguidade, escolha a leitura mais conservadora, registre a suposição no estado
e siga. Quando um passo falha, registre e passe ao próximo.

---

## 1. Regras que valem para todas as fases

### 1.1 Somente leitura
- **Não edite** código, notebooks, decks, planilhas, dados nem documentação. Não commite, não troque de
  branch, não faça push, não apague nem mova nada.
- **Pode escrever só:** o relatório final, o arquivo de estado e scripts de conferência no diretório de
  rascunho (scratchpad) da sessão, nunca dentro do repositório.
- **Pode rodar:** `pytest`, scripts de leitura (pandas, python-pptx, pypdf) sobre as saídas, `graphify
  query|path|explain`, `git log|show|diff`. **Não rode** a pipeline nem regere saídas (notebooks,
  `fatorial_multiversao.py`, geradores de deck e de relatório): demoram e sobrescrevem arquivos versionados.
  Quando a dúvida só se resolve rodando, registre como SUSPEITA, com o comando que resolveria.
- `relatorio_parcial_raic/Apresentacao_Oral_RAIC_2026_Pedro_ENVIO_v5.pptx` está aberto no PowerPoint (há um
  `~$…` ao lado): só leia.

### 1.2 Onde não ler
`dados/` (8 GB brutos do IBGE), `.venv/`, `node_modules/`, `Backup/` (metodologia abandonada, denominador
V01042), `graphify-out/` (só via `graphify query`), pastas `historico/`, arquivos `* 2.*` (cópias do iCloud) e
`~$*`. Bases grandes (`banco_de_dados/**/Base_*.csv`, `*.db`): só com `usecols`/`nrows` ou SQL agregado, sem
imprimir tabela inteira.

### 1.3 Economia
- **Grafo antes de abrir arquivo:** `graphify query "<pergunta>" --budget 1500`. O grafo é do commit
  `85ced4af` (22/10/2026). Estes arquivos mudaram depois e devem ser lidos direto: `src/ivs_censo/fatorial.py`,
  `scripts/fatorial_corte_04.py`, `scripts/fatorial_corte_04_sensibilidade.py`, `scripts/dados_deck_corte_04.py`,
  `scripts/ajustar_apresentacao_oral_raic.py`, `scripts/gerar_roteiro_word_raic.py`,
  `tests/test_fatorial_corte_04.py`, `README.md`, `scripts/README.md`, `notebooks/Fase3_EDA_ELSI/README.md`.
- Uma verificação = um script; saída truncada (`head -60`). Não releia o que já leu.
- Subagentes são opcionais: no máximo 3 em paralelo, modelo Sonnet, receita fechada e teto de 25 chamadas
  cada, sem verificador do verificador. Bom uso: conferir número a número os slides da Fase 3.
- Fase que estoura o teto: feche com o que tem, registre no estado o que faltou e siga.

### 1.4 Como registrar cada achado
| Campo | Conteúdo |
|---|---|
| id | `C01…` código, `A01…` análise, `P01…` apresentação, `E01…` estrutura, `R01…` rumo |
| severidade | **Crítico**: número errado em entregável ou erro de método que muda o IVS. **Alto**: muda conclusão ou decisão. **Médio**: atrapalha reprodução ou leitura. **Baixo**: acabamento |
| evidência | `arquivo:linha`, ou arquivo + slide/página, ou comando + saída resumida |
| por que importa | uma frase |
| correção | concreta: o que mudar e onde |
| esforço | P (minutos), M (horas), G (dias) |
| status | **CONFIRMADO** (você rodou ou conferiu) ou **SUSPEITA** (indício, com o comando que resolveria) |

### 1.5 Estado retomável
Crie `docs/prompts/estado_revisao_ponta_a_ponta_2026-11.md` na Fase 0 e atualize ao fim de cada fase: fase
concluída, chamadas gastas, achados até aqui (id e uma linha), suposições feitas e o que ficou de fora. Se a
sessão cair, a próxima retoma da fase seguinte sem refazer nada.

---

## 2. O que já se sabe (não gaste chamadas redescobrindo)

### 2.1 Auditoria de estrutura de 12/11/2026
Vai para a seção "Estrutura" do relatório como está, sem reinvestigar:
- O repositório fica dentro do iCloud ("Mesa e Documentos" ligado). Isso gerou 388 cópias `" 2"` (as 386
  idênticas já foram para a Lixeira) e um `.git/index 2`. Restam duas cópias diferentes do original:
  `scripts/gerar_roteiro_word_raic 2.py` (variante de 19/10, nunca commitada) e
  `relatorio_parcial_raic/Roteiro_Apresentacao_Oral_RAIC_2026_Pedro 2.docx`.
- O grafo está 10 commits atrás e `graphify-out/cache/last_query_stamp` é versionado (muda a cada consulta).
- `GUIA_DO_PROJETO.md` e `estrutura_projeto.md` estão parados em 26–27/09, mas o README chama o GUIA de
  documento mestre e canônico.
- `reportlab` está no `requirements.txt` e falta no `.venv`. `scripts/README.md` cita
  `relatorio_descritivo/Relatorio_Descritivo_IVS_2026-10_com_108_versoes.pptx`, que não existe.
- Não há tags marcando entregas. O repositório é público e tem CSV/.db de 40–70 MB repetidos no histórico
  (`.git` com 558 MB).
- Fora do git: `apresentacoes_multiversao/figuras/C04_pesos_final.png` (nenhum script gera) e
  `relatorio_parcial_raic/Apresentacao_Oral_RAIC_2026_Pedro_ENVIO_v4.pdf`.
- O que está bem: 170 testes passando, `git fsck` limpo, commits só com o nome do Pedro.

### 2.2 Revisões anteriores: leia antes da Fase 1
- `docs/relatorios/Simplificacao_e_Correcoes_2026-10.md`: os erros E1–E8 foram corrigidos em 22/10. Leia §3
  (entregáveis afetados e não regerados), §4 (a investigar) e §5 (decisões para o Pedro). Na revisão, só
  confira se E1–E8 continuam corrigidos e cobertos por teste, e o que de §3–§5 segue aberto.
- `docs/relatorios/Auditoria_Integral_2026-09.md` e `docs/relatorios/Revisao_Geral_2026-09.md`: confira por
  amostra se algum achado de setembro voltou.
- `README.md`, seções "Problemas Conhecidos" e "Em aberto — dependem de definição com a orientação"
  (decisões 1–7, perguntas P1–P5), e `analises_exploratorias/PERGUNTAS.md`.
- "Problema 9": os decks das 108 versões e do relatório descritivo têm números antigos.
- **Código nunca revisado:** tudo o que entrou depois da revisão de 22/10, ou seja
  `git diff c1dcfb8..HEAD -- src scripts tests notebooks` (correção do NB05, corte de carga < 0,4,
  sensibilidade do corte, geradores da RAIC v4).

---

## 3. Fases

### Fase 0 — Linha de base (≤ 12 chamadas)
1. Leia o estado, se existir, e retome dele. Senão, crie-o.
2. `git status -sb` e `git log --oneline -15`; registre o HEAD no estado.
3. `.venv/bin/python -m pytest -q -p no:cacheprovider` (esperado: 170 passam).
4. Leia as fontes da seção 2.2 (só as seções indicadas) e o `GUIA_DO_PROJETO.md` §6 (decisões canônicas).
5. Registre no estado a lista de números-chave a conferir nas Fases 2 e 3, cada um com a fonte declarada.
   Ponto de partida, a completar: 104.108 setores no recorte de análise, 70 municípios, 19.452 setores de
   favela (18,7%), 73.877 setores com IVS definido, 12 indicadores na fatorial, 324 especificações (NB05),
   8.034 fatoriais e 999 especificações (multiversão), cargas e pesos das propostas A e B.

### Fase 1 — Código (≤ 45 chamadas) — `/ponytail-audit`
Invoque `/ponytail-audit` no início. É a auditoria do `/ponytail`: mesma régua (o menor código que resolve,
nada especulativo), mas só aponta e não muda nada, como este prompt exige. Ordem:
1. O código nunca revisado (seção 2.2, último item).
2. `src/ivs_censo/`: indicadores, fontes, renda, fatorial, dicionário.
3. O caminho do IVS: `scripts/ivs_especificacoes.py`, `scripts/fatorial_multiversao.py`,
   `scripts/fatorial_corte_04.py`, `scripts/fatorial_corte_04_sensibilidade.py`, `scripts/proporcoes_brasil.py`,
   `scripts/eda_versoes.py`, `scripts/eda_transversais.py`.
4. Notebooks `notebooks/Fase3_EDA_ELSI/` 01, 02, 04, 04b e 05: as células de cálculo, não as de gráfico.
5. `tests/`: o que é crítico e não tem teste (normalização, inversão da renda, corte de 0,4, exclusão
   rural, ausentes e sigilo)?
6. Geradores de deck e relatório (`scripts/gerar_*`, `scripts/dados_*`, `scripts/*.js`), por amostra:
   números digitados à mão (o E6 ficou sem correção porque a RAIC estava congelada), caminhos que não
   existem, duplicação.

Responda obrigatoriamente: (a) o cálculo do IVS bate com a metodologia declarada no README (denominador
V00001, renda invertida, régua min-max municipal)? (b) o corte de 0,4 é aplicado em cada rotação como o
README diz, e o que acontece com indicador que fica sozinho num fator? (c) o que pode ser apagado ou
juntado sem mudar saída?

### Fase 2 — Análises e método (≤ 40 chamadas) — `/data:statistical-analysis` e `/data:validate-data`
Invoque `/data:statistical-analysis` para a estatística e `/data:validate-data` para o QA de método, contas
e viés, como se a análise fosse para a orientadora amanhã.
1. **Fatorial:** adequação (KMO, Bartlett, MSA por variável), extração (máxima verossimilhança via EM),
   número de fatores, rotação, comunalidades, casos de Heywood, estabilidade (replicação entre metades,
   bootstrap por município). Confira se o corte de 0,4 foi aplicado de forma iterativa e igual entre as
   rotações, e se a saída dos indicadores muda a interpretação das dimensões.
2. **IVS:** direção de cada indicador, normalização, pesos, ausentes e sigilo, efeito do recorte urbano e da
   falta de piso de setores (14 dos 70 municípios perdem mais da metade). A unidade de inferência é o
   município, não o setor: confira se as incertezas respeitam isso.
3. **Propostas A e B:** o que de fato as separa (o sem banheiro), quanto troca de faixa entre elas, e se os
   números do deck de decisão batem com `banco_de_dados/eda/fatorial_corte_04/*.csv`.
4. **Multiverso:** as 324 + 108 + 999 especificações respondem às perguntas P1–P5 ou só as descrevem? Há
   resultado robusto que já permitiria decidir alguma delas?
5. Confira os números-chave da Fase 0 contra as saídas em CSV, com script de leitura.

### Fase 3 — Apresentações e relatórios (≤ 35 chamadas) — `/anthropic-skills:pptx`, `/anthropic-skills:pdf`, `/anthropic-skills:docx`
Use as skills só para ler. Prioridade:
1. `apresentacoes_multiversao/Corte_Carga_04_Duas_Propostas_2026-11_v2.pptx`, a decisão em curso (o slide 5
   resume): os números batem com os CSV? a orientadora consegue decidir com ele? o que falta?
2. **RAIC:** `relatorio_parcial_raic/Relatorio_Parcial_RAIC_2026_Pedro_corrigido.pdf`,
   `Apresentacao_Oral_RAIC_2026_Pedro_ENVIO_v5.pptx` (se não existir, `_ENVIO_v4.pptx`),
   `ROTEIRO_APRESENTACAO_ORAL.md` e `NOTAS_PARA_ORIENTADORA.md`. A RAIC vai de 09 a 13/11/2026: número
   errado nos slides vai para a seção "Urgente", no topo do relatório.
3. **Problema 9**, por amostra: 5 dos 51 decks de `analises_exploratorias/`, `versoes_fatorial/` e
   `relatorio_descritivo/`. Quantos números antigos sobram, e algum desses decks ainda está em uso?
4. **Coerência:** o que o README, o relatório parcial e o deck de decisão dizem sobre o mesmo número ou a
   mesma decisão.

Critérios: o número confere com a saída; cada slide tem uma mensagem; o gráfico é legível; os termos são
os mesmos entre documentos; o que a banca ou a orientadora vai perguntar e não está respondido.

### Fase 4 — Rumo (≤ 25 chamadas)
Leia, na pasta-mãe (fora do git): `../Plano de acao/Plano de trabalho.pdf`, `../Plano de acao/Objetivos.docx`
e `../Demandas da minha professora orientadorastembro.pdf`. Leia também
`docs/referencias/Plano_Artigo_Cientifico_IC_Preenchido.docx`.
1. Monte a tabela objetivo ou demanda × entrega × status × evidência.
2. Responda direto: o projeto converge para um IVS final, mapas e artigo, ou abre versões mais rápido do que
   fecha decisões? Qual é o menor caminho até o IVS final, os mapas (QGIS, pendentes) e o artigo?
3. Invoque `/council` **uma vez** (custo alto, cerca de 11 chamadas) com uma única pergunta: a decisão de
   maior impacto que você identificou (por exemplo, o que priorizar até o fim da IC). Leve o veredito ao
   relatório, marcado como opinião.

### Fase 5 — Relatório (≤ 15 chamadas)
Escreva `docs/relatorios/Revisao_Ponta_a_Ponta_2026-11.md` com:
1. **Urgente** (só se houver).
2. **Veredito**, em até 10 linhas: está no rumo? o que está sólido e o que é risco.
3. **Achados** ranqueados por severidade, com os campos da 1.4, separados em Código, Análises,
   Apresentações e Estrutura.
4. **O que está bem feito**, curto e com evidência, para não mexer.
5. **Rumo:** a tabela da Fase 4 e o menor caminho até o fim.
6. **Plano de ação** em dois horizontes (até a próxima reunião com a orientadora; até o fim da IC), cada
   item com o achado de origem e o esforço.
7. **Perguntas para a orientadora**, no máximo 7, cada uma com o que muda conforme a resposta.
8. **O que não foi revisado**, e por quê.

Feche o estado e escreva no chat um resumo de até 20 linhas com o caminho do relatório. Não commite: o
Pedro decide o que entra no git.
