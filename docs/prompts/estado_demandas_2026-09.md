# Estado — demandas da orientadora (set/2026)

Linha de base: commit 3c426e8 · 25/09/2026

## Fases
- [x] Fase 0 — linha de base e destravamentos   (sessão de 25/09/2026, em duas partes; concluída)
- [x] Fase 1 — demandas 1 e 2   (25/09/2026, execução automática; concluída)
- [x] Fase 2 — fatorial ampliada   (25/09/2026, execução automática; concluída)
- [x] Fase 3 — notebook 04b e NB04   (25/09/2026, execução automática, em duas sessões; concluída)
- [x] Fase 4 — curadoria e slides   (25/09/2026, três sessões; concluída)
- [ ] Fase 5 — lotes A · B · C · D   (lote A: diagnóstico feito, execução pendente — sessão 1)

## Demandas da orientadora
| # | Demanda | Fase | Estado | Onde está o resultado |
|---|---|---|---|---|
| 1 | coluna de renda com a mediana | 1 | concluída | `renda_media_mediana_mun` no .db/.csv da entrega; sensibilidade em `banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv` |
| 2 | quadro de indicadores | 1 | concluída | `banco_de_dados/entrega_orientadora/Quadro_Indicadores.{csv,xlsx,md}` |
| 3 | fatorial sem bootstrap, sem e com rotação | 2 | concluída | `banco_de_dados/eda/fatorial_ampliada/cargas.csv` e `pesos.csv` — sem rotação, Varimax e promax lado a lado, em todos os cenários |
| 4 | separar útil × inútil | 4 | concluída | `docs/Apresentacoes_IVS/MAPA_APRESENTACAO_FINAL.md`; correções e bloco novo (S6, `scripts/gerar_slides_fatorial_ampliada.js`) em `Analise_Fatorial_NB04_2026-09.pptx`; `Guia_Apoio_Analise_Fatorial.pdf` |
| 5 | comparar "não chega" | 2 | concluída (as duas leituras) | S2 na grade; `banco_de_dados/eda/fatorial_ampliada/comparacao_nao_chega_banheiro.csv` (Spearman com IVS-7 e outras categorias de água; perfil > 0 × = 0) |
| 6 | juntar "sem banheiro" | 2 | concluída com V00495; graduada (V00237) em aberto | S4; prova V00238 ≤ V00495 no bloco `prova_juncao` de `banco_de_dados/eda/fatorial_ampliada/comparacao_nao_chega_banheiro.csv` |
| 7 | adicionar canalização e sem banheiro | 2 | concluída | S2, S3, S4 em `banco_de_dados/eda/fatorial_ampliada/cenarios.csv` |
| 8 | fatorial de tudo isso | 2 | concluída (leitura padrão da pergunta 6) | S6 e S7; renda em três versões (S6_renda_*); postos no município (S6_postos_mun) |
| 9 | habitação convencional | 2 | concluída (como não convencional, sem excluir) | S5 e S6; MSA, comunalidade e % de zeros em `banco_de_dados/eda/fatorial_ampliada/cargas.csv` |
| 10 | testar lixo | 2 | concluída | S1 e S7; `lixo_fator_proprio_varimax` em `cenarios.csv`; `lixo_muda` em `sensibilidade_municipios.csv` |
| 11 | testar as duas rotações | 2 | concluída | `banco_de_dados/eda/fatorial_ampliada/pesos.csv` — Varimax e promax (padrão e estrutura) + Φ; figura `figuras/fa_plano_s6.png` |

## Perguntas à orientadora
<mensagem redigida na Fase 0; respostas, quando vierem>

Oi! Antes de avançar nas demandas, seis pontos ficaram com mais de uma leitura possível.
Registrei o padrão que vou seguir em cada um enquanto você não responder — se preferir outra
leitura, é só avisar:

1. **Renda (demanda 1):** "a mediana" de quê? A mediana do próprio setor não existe no arquivo
   bruto do Censo (só vem V06001–V06005, não V06006). Vou entrar com uma coluna nova usando a
   mediana de Belo Horizonte sem o setor extremo (R$ 3.058,235), e registrar num CSV de
   sensibilidade o efeito das alternativas: mediana de BH com o setor e mediana dos 70 municípios.
2. **Fatorial com rotação (demanda 3):** qual rotação? Vou rodar as duas — sem rotação, Varimax
   e Promax lado a lado (a demanda 11 já pede isso).
3. **"Comparar com os outros" (demanda 5):** vou tratar as duas leituras — (a) contra as outras
   categorias de canalização e (b) contra os indicadores do IVS-7.
4. **Juntar "sem banheiro" (demanda 6):** vou usar a V00495, que já contém a V00238 (confirmei
   isso no banco). A versão graduada, com V00237 (só sanitário ou buraco), exige reextração do
   NB01 e fica em aberto — quer que eu faça?
5. **Habitação convencional (demanda 9):** vou entrar com a variável na direção da
   vulnerabilidade (não convencional), com diagnóstico completo. Não vou excluir por variância
   baixa — prefiro mostrar o resultado e você decide.
6. **"Tudo isso" na fatorial ampliada (demanda 8):** meu entendimento é IVS-7 + não chega +
   sem canalização + sem banheiro + não convencional. Confirma?

E três decisões de método que a revisão geral do repositório levantou:

7. **Repartição oblíqua:** vou reportar as duas métricas (matriz padrão e matriz estrutura),
   sem dizer que uma "afasta" ou "aproxima" da literatura.
8. **Renda no índice final:** vou rodar os cenários de referência com as três opções (renda
   original, sem o extremo, imputada com a mediana) e você escolhe depois.
9. **Incerteza:** em vez do bootstrap, vou apresentar sensibilidade por município (deixando um
   de fora por vez), não como bootstrap.

Abraço, Pedro

## Decisões tomadas (por quem, quando)

## O que mudou em arquivo versionado (por fase)
- **Fase 0** (25/09/2026): `.gitignore` — corrigida a linha `banco_de_dados/*.csv`, que estava
  truncada/corrompida em `0b94c96` (virou `banco_de_# Legado da Fase 2...`), separando-a do
  comentário do legado da Fase 2. Verificado com `git status --porcelain --ignored`: só o
  `.gitignore` aparece modificado, nada novo passou a ser rastreado ou ignorado.
- **Fase 0** (25/09/2026): criado `banco_de_dados/eda/fatorial_ampliada/linha_de_base_nb04.csv`
  **parcial** — 7 medidas conferidas contra a seção 1 do prompt (todas bateram: KMO 0,7826;
  MSA mínimo 0,6995; Bartlett 235.084,3838; pesos IVS-6 Varimax 65,038/34,962; Φ 0,5215; AUC do
  índice 0,8131), mais 4 linhas marcadas `PENDENTE` (ver Pendências). Nenhuma divergência
  encontrada nos números já existentes em CSV — sem sinal de que o repositório mudou.
- **Fase 0** (25/09/2026): `pytest` rodado sem nenhuma mudança de código ainda — 74 passed em
  11,31s, batendo com a seção 1 ("74 testes, verdes em ~11 s").
- **Fase 0** (25/09/2026, sessão 2): completado `linha_de_base_nb04.csv` — os 4 números que
  faltavam, recalculados em `/tmp/fase0b/linha_base.py` (fora do repositório): AUC renda
  invertida sozinha = 0,8819; AUC média de postos com pesos iguais = 0,8533; pesos sem São
  Paulo (F1 socioeconômico, o maior) = 62,9131 (F2 saneamento = 37,0869); repartição pela
  matriz estrutura (F1 socioeconômico, o maior) = 59,6438 (F2 saneamento = 40,3562). As duas
  travas (peso(d) = 65,04/34,96 e auc(indice_01) = 0,8131) bateram antes de gravar.
- **Fase 0** (25/09/2026, sessão 2): FAT-01 — trocado o critério de parada da `varimax` em
  `src/ivs_censo/fatorial.py` (era razão de somas de valores singulares, parava cedo; agora
  `max|R − R_ant| < tol`, `tol=1e-10`, `maxiter=10000`). Teste novo
  `test_varimax_atinge_o_otimo_da_rotacao_2d` em `tests/test_fatorial.py`: falhou no código
  antigo (0,19070539 vs ótimo 0,19070564, diff 2,5e-7 > 1e-9) e passa no novo. Suíte
  `test_fatorial.py`: 10 passed. `scripts/diagnostico_fatorial.py` regerou 3 CSVs em
  `banco_de_dados/eda/fatorial/`, todos com uma única célula mudada (coluna `Varimax1`):
  `ivs6_sem_analfab_spearman_cargas.csv` linha 5 (−0,725 → −0,724),
  `ivs6_sem_lixo_spearman_cargas.csv` linha 2 = Água (−0,087 → −0,086, como previsto),
  `ivs7_pearson_cargas.csv` linha 3 (−0,396 → −0,395). NB04 não foi rodado (é da Fase 3).
- **Fase 0** (25/09/2026, sessão 2): IND-1/IND-2 — `scripts/proporcoes_brasil.py::resumir`
  passou a aplicar `ind.complemento` do mesmo jeito que `indicadores.py` (1 − razão, antes de
  qualquer corte). `tests/test_pipeline_fase3.py::test_razao_agregada_...` ganhou
  `pct_sem_agua_canalizada` na lista testada, com o complemento também na fórmula esperada —
  falhou contra o CSV antigo (0,986233 vs 0,013767) e passa depois da regeração. Regerado
  `scripts/proporcoes_brasil.py` (7,5 min): células que mudaram, todas em linhas de
  `pct_sem_agua_canalizada` — `comparativo_brasil_vs_elsi.csv` 3 células/1 linha,
  `proporcoes_brasil_por_municipio.csv` 5.570 células/5.570 linhas,
  `proporcoes_brasil_por_regiao.csv` 5 células/5 linhas, `proporcoes_brasil_por_uf.csv` 27
  células/27 linhas, `proporcoes_por_recorte.csv` 3 células/3 linhas. Razão agregada nova do
  ELSI urbano: 0,013767 (era 0,986233).
- **Fase 0** (25/09/2026, sessão 2): suíte inteira `pytest -q` — 75 passed em 11,61s.
- **Fase 1** (25/09/2026, execução automática): `src/ivs_censo/renda.py` ganhou
  `renda_imputada_mediana_municipal` — imputa, nos setores de `SETORES_RENDA_EXCLUIDA`, a
  mediana do próprio município (sem eles), no recorte `urbano==1` e `Dados_sig=='OK'`.
  Testada com município sintético (mediana de {1000,2000,3000} sem o excluído = 2000,
  outro município intacto) e contra o `.db` real (1 setor difere de `renda_media`, valor
  3.058,235).
- **Fase 1** (25/09/2026): `scripts/gerar_entrega_orientadora.py` grava a coluna nova
  `renda_media_mediana_mun` ao lado de `renda_media_sem_extremo`. Entrega regenerada
  (~2 min): banco passa de 104 para **105 colunas** (109.032 × 105 e 5.166 × 105).
  `banco_de_dados/entrega_orientadora/README.md` atualizado (104→105 + parágrafo da coluna
  nova).
- **Fase 1** (25/09/2026): `scripts/eda_extremo_belo_horizonte.py` ganhou a seção de
  sensibilidade da demanda 1 —
  `banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv` com as três alternativas
  (mediana de BH sem o setor R$ 3.058,235, com o setor R$ 3.060,31, dos 70 municípios sem o
  setor R$ 2.572,39) e, para cada uma, média/desvio/máximo em BH e no agregado. Reaproveita
  `descrever()`, já existente no script — não reescreveu a lógica.
- **Fase 1** (25/09/2026): `scripts/gerar_quadro_indicadores.py` (novo) monta
  `banco_de_dados/entrega_orientadora/Quadro_Indicadores.{csv,xlsx,md}` a partir de
  `TODOS_INDICADORES` — 26 linhas (7 do IVS-7, 19 complementares), com numerador,
  denominador e descrição oficial do IBGE por código V.
- **Fase 1** (25/09/2026): IND-3 (parcial) — `scripts/gerar_tabela_variaveis.py` passou a
  concatenar as 9 colunas derivadas (`DESC_DERIVADAS`, reaproveitado de
  `gerar_entrega_orientadora.py`, sem duplicar) ao `Dicionario_Variaveis_Projeto.csv/.xlsx`,
  que só tinha as 70 variáveis brutas do Censo (72 linhas → 81). Os 26 indicadores ficam no
  `Quadro_Indicadores.csv` novo, não duplicados aqui. `scripts/README.md` ganhou a linha do
  script novo e 104→105.
- **Fase 1** (25/09/2026): `git grep -n "104 colunas\|× 104\|x 104"` — 9 ocorrências;
  corrigidos os dois READMEs (`banco_de_dados/entrega_orientadora/README.md`,
  `scripts/README.md`). `GUIA_DO_PROJETO.md`, `docs/MANUAL_DO_PROJETO.md`,
  `docs/metodologia/...`, `docs/relatorios/...` e o próprio prompt ficam para a Fase 5,
  lote C, como o prompt manda.
- **Fase 1** (25/09/2026): suíte inteira `pytest -q` — **78 passed** em ~11,6s (75 + 3
  testes novos: imputação por mediana municipal, coluna no `.db`, cobertura do quadro de
  indicadores).
- **Fase 2** (25/09/2026, execução automática): `src/ivs_censo/fatorial.py` ganhou
  `rodar_cenario` (um cenário inteiro num dicionário, com a convenção de sinal "soma das
  cargas positiva" em sem rotação, Varimax e promax) e `reparticao`. Teste novo
  `test_rodar_cenario_orienta_sinais_e_fecha_as_contas`. `diagnosticar` intocada. Commit
  `2dd246a`.
- **Fase 2** (25/09/2026): `scripts/fatorial_ampliada.py` (novo, ~30 s) — a grade de 15
  cenários (S0–S7; S0/S6 com renda sem extremo e mediana municipal; S0/S1/S6 com postos
  dentro do município) e a sensibilidade de um município de fora por vez (S0, S1, S6).
  Grava em `banco_de_dados/eda/fatorial_ampliada/`: `cenarios.csv`, `cargas.csv`,
  `pesos.csv`, `validacao_fcu.csv`, `autovalores.csv`, `correlacao_s6.csv`,
  `comparacao_nao_chega_banheiro.csv`, `sensibilidade_municipios.csv`, 4 figuras em
  `figuras/` e `README.md` de procedência. Funções de figura, índice e AUC copiadas do
  NB04 (células 3, 22, 28, 29, 39, indicadas no script); o rótulo dos eixos do plano
  fatorial sai das cargas (NB4-08). `scripts/README.md` ganhou a linha do script.
- **Fase 2** (25/09/2026): **travas de sanidade batidas** antes de gravar — S0 KMO 0,7826
  (= linha de base); S1 pesos Varimax 65,01/34,99. Conferências extras, também batidas: AUC
  do índice de S1 0,8131, renda invertida 0,8819, média de postos 0,8533 (= linha de base).
  Verificação independente num script só (scratchpad): contagens de linhas, sinais,
  estrutura = padrão·Φ, repartições somando 100, Kaiser/Horn contra `autovalores.csv`,
  pesos do índice somando 1 — nenhuma falha.
- **Fase 2** (25/09/2026): suíte inteira `pytest -q` — **79 passed** em ~12 s.
- **Fase 3** (25/09/2026, execução automática, **parcial**): corrigidos no
  `notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb` os achados NB4-01, NB4-02, NB4-03,
  NB4-04, NB4-05, NB4-06, NB4-07, NB4-08, NB4-09, NB4-10, NB4-11 e NB4-13 da revisão geral
  (21 edições em 13 células, texto/comentário/rótulo — nenhuma conta nova além da
  repartição pela matriz estrutura, que já existia como função e só não era chamada).
  `docs/relatorios/Relatorio_Analise_Fatorial_NB04.md` recebeu as mesmas correções, mais
  o 16.548 no lugar de 16.563 (AUD-08). Notebook reexecutado do zero via `nbclient`
  (~88 s, 0 erros) com a Varimax corrigida (FAT-01, da Fase 0) — muda a 4ª casa decimal em
  cargas e pesos, como previsto: pesos 65,01/34,99 (era 65,04/34,96; bate com a linha de
  base da Fase 2). CSVs que mudaram (todos em `banco_de_dados/eda/fatorial/`):
  `nb04_bootstrap_cargas.csv`, `nb04_cargas_ivs6_sem_lixo.csv`, `nb04_cargas_ivs7.csv`,
  `nb04_cenarios.csv`, `nb04_contingencia_pesos_6040.csv`,
  `nb04_contingencia_sem_analfab.csv`, `nb04_contingencia_um_fator.csv`,
  `nb04_escores.csv` (as 87.545 linhas, 4ª casa), `nb04_pesos.csv`,
  `nb04_renda_sem_extremo.csv`, `nb04_renda_sem_extremo_cargas.csv`,
  `nb04_sintese_pesos.csv`, `nb04_validacao_fcu.csv`; e as figuras `nb04_mapa_cargas.png`,
  `nb04_plano_fatorial.png` (rótulo do eixo corrigido, NB4-08), `nb04_roc_fcu.png`. AUC do
  índice 0-1 continua 0,8131 (só a 4ª casa dos números auxiliares mudou). `pytest -q` — 79
  passed (suíte não toca notebook). **Não incluído naquela sessão** (orçamento de chamadas
  esgotado): o notebook novo `04b_Analise_Fatorial_Ampliada.ipynb` (item 3.1 do prompt).
- **Fase 3** (25/09/2026, sessão 2, execução automática): criado
  `notebooks/Fase3_EDA_ELSI/04b_Analise_Fatorial_Ampliada.ipynb` (item 3.1) — 44 células,
  montadas por um script com `nbformat` a partir das funções de `scripts/fatorial_ampliada.py`
  e `src/ivs_censo/fatorial.py` (`rodar_cenario`); nenhuma conta reescrita, só chamada. Sete
  blocos: o que a orientadora pediu item por item (com a comparação das demandas 5 e 6); os
  cenários (trava de sanidade contra a linha de base do NB04 antes de interpretar); sem
  rotação × Varimax × promax (demandas 3 e 11, repartição oblíqua com as duas métricas,
  padrão e estrutura, sem dizer qual "afasta" da literatura); lixo (demanda 10); a estrutura
  municipal (postos dentro do município — o único ponto em que o índice supera a renda
  invertida sozinha em AUC, em 2 dos 3 casos); o que o índice acrescenta à renda (NB4-02: a
  renda invertida sozinha tem AUC maior que o índice nos oito cenários S0–S7, sem adjetivo);
  o que fica para a orientadora (as três versões de renda, a rotação, a repartição oblíqua, a
  versão graduada de "sem banheiro", a habitação não convencional mantida na grade). Todo
  número do texto sai de uma célula de código imediatamente anterior — nenhum digitado de
  memória; os % de zeros das quatro variáveis novas (77–96%) vêm de `cargas.csv` (base
  listwise de S6), não da seção 1 do prompt. Executado do zero com `nbclient` (~25 s, 0
  erros); os CSVs que a execução regrava em `banco_de_dados/eda/fatorial_ampliada/` saem
  **idênticos** aos da Fase 2 (`git status --porcelain` vazio na pasta, conferido antes e
  depois da execução). `pytest -q` — 79 passed (suíte não toca notebook; nenhum código de
  `src/` ou `scripts/` mudou nesta sessão). `git ls-tree -r HEAD | wc -l` = 402 antes e depois
  (sem queda). Fase 3 **fecha** — 3.1 e 3.2 concluídos.
- **Fase 4** (25/09/2026, execução automática, **parcial**): `scripts/inventario_apresentacao.py`
  (novo, item 4.1) classifica os 51 artefatos de apresentação (pptx/pdf/docx de
  `docs/Apresentacoes_IVS/` + figuras de `banco_de_dados/eda/`) em ATUAL (27), SUPERADO (13,
  sucessor citado) ou HISTÓRICO (11, pasta `historico/`) por critério explícito — sem mover
  nem apagar nada — e escreve `docs/Apresentacoes_IVS/MAPA_APRESENTACAO_FINAL.md`, com o
  roteiro proposto citando os slides existentes pelo número. Trava batida na hora: deck atual
  = 98 slides, 98 notas, 21 EXPLICAR (bate com a seção 1 do prompt). `scripts/juntar_decks.py`
  (novo, item 4.2 passo 1) recria o juntador perdido — copia, do deck anexo, slide + layout +
  master + tema + mídia (renumerados) + notas para o fim do deck base, direto no zip OOXML
  (`zipfile` + regex nos `.rels`/`presentation.xml`), sem tocar em mais nada da base. Testado
  com dois decks pequenos (pptxgenjs, 3 + 2 slides, 1 imagem e 1 nota cada, uma "EXPLICAR"
  cada) no scratchpad da sessão: saída com 5 slides/5 notas/3 EXPLICAR (soma exata), texto,
  notas e as duas imagens (mesmo tamanho em bytes) preservados, zip válido. `pytest -q` — 79
  passed (nenhum código de `src/` mudou). Commits: `0058911` (4.1) e `4f36ea2` (juntador).
- **Fase 4** (25/09/2026, sessão 2, execução automática, **parcial**): item 4.2.3 —
  correções pontuais no deck real por `python-pptx` (`run.text`, sem tocar em mais nada
  do slide): S97 corpo (AUD-07, "segundo maior" R$ 45.385,44), S96 e S97 notas (AUD-07,
  104.096 setores e 37% do município), S68 e S91 (DEC-1, caminho para `atualizada/`), S39
  e S88 (AUD-04, caminhos `docs/metodologia/` e `docs/relatorios/`). Conferido com
  `contar_slides_notas_explicar` antes/depois: 98 slides, 98 notas, 21 EXPLICAR, sem
  mudança. Validado contra o HEAD anterior com o validador OOXML da skill pptx: as 3
  violações de ID (masters duplicados) já existiam no original; zero erros novos.
  `scripts/gerar_slides_extremo_bh.js` corrigido nos mesmos 3 pontos (texto fixo trocado
  por valores de `extremo_bh_descritivas.csv`/`extremo_bh_normalizacao.csv`), testado à
  parte no scratchpad, nunca usado para regerar o deck real. Commit `3f042ca`.
- **Fase 4** (25/09/2026, sessão 2): item 4.2.4 — `scripts/gerar_pdf_guia_fatorial.py`:
  AUD-08 corrigido (16.563 → 16.548, lido de `resumo_adequabilidade.csv`, não mais
  digitado); três itens novos no vocabulário — autovalor/Kaiser/Horn (DEC-2), MSA
  (DEC-4), matriz padrão × matriz de estrutura (DEC-3), este último registrando que o
  Notebook 04b reporta as duas sem dizer qual "aproxima" da literatura. PDF regenerado;
  conferido no texto extraído (pdfplumber): "16.563" some, "16.548" aparece 2×, os
  termos novos aparecem nos trechos certos. De brinde, o AUD-04 do guia (caminhos
  desatualizados) desapareceu: o gerador já estava corrigido, só faltava regerar. Commit
  `8a3267e`.
- **Fase 4** (25/09/2026, sessão 2): **não feitos**, por orçamento de chamadas da sessão —
  item 4.2.2 (bloco novo de slides da fatorial ampliada,
  `scripts/gerar_slides_fatorial_ampliada.js`, anexado com o juntador) e item 4.2.5
  (renderização dos slides novos/alterados para conferência visual). Nenhum dos dois
  tocou no deck real ou em qualquer artefato de apresentação; nada foi commitado que
  dependesse deles. `pytest -q` seguiu verde (suíte não toca `scripts/*.js` nem
  `scripts/gerar_pdf_guia_fatorial.py`, cobertos só pela conferência funcional acima).
- **Fase 4** (25/09/2026, sessão 3, execução automática): item 4.2.2 —
  `scripts/gerar_slides_fatorial_ampliada.js` (novo, mesmo padrão de
  `gerar_slides_extremo_bh.js`/`deck_comum.js`): 8 slides (divisória; as onze demandas
  e onde está cada resposta; a matriz de Spearman ampliada, figura
  `fa_correlacao_ampliada.png`; a grade S0–S7 com n/KMO/Kaiser-Horn/peso Varimax
  F1/AUC índice × renda sozinha; o plano fatorial de S6 em três rotações, figura
  `fa_plano_s6.png`; o lixo, fator próprio por cenário e sensibilidade a excluir 1
  município; a estrutura municipal, postos dentro do município — o índice supera a
  renda sozinha em AUC em 2 dos 3 cenários `_postos_mun` — e a sensibilidade a tirar 1
  dos 70 municípios; o que fica para a orientadora decidir). Todo número lido de
  `banco_de_dados/eda/fatorial_ampliada/*.csv`. Achado na conferência visual (4.2.5) e
  corrigido antes do commit: a descrição de S6 em `cenarios.csv` vem entre aspas CSV
  (`"tudo isso"`), e o `split(';')` ingênuo (copiado do padrão do `extremo_bh`, que não
  tinha esse caso) quebrava o campo em três — trocado por um leitor de CSV que respeita
  aspas duplas. Anexado ao deck real com `scripts/juntar_decks.py`, a partir de
  `git show HEAD:...` (nunca do deck já anexado): 98 → **106 slides, 106 notas, 21
  EXPLICAR** (contagem batendo antes/depois). Validador OOXML da skill pptx contra o
  HEAD anterior: as mesmas 3 violações de ID (masters duplicados) já existentes, **zero
  erros novos**. Item 4.2.5: os 8 slides novos renderizados um a um (LibreOffice → PDF →
  PNG, páginas separadas com `pypdf` via `uv run`) e olhados individualmente — nenhuma
  colisão de texto, nenhuma tabela fora da margem, figuras (matriz ampliada e plano
  fatorial em três rotações) com rótulos e eixos legíveis. `git ls-tree -r HEAD | wc -l`
  = 406 antes, 407 depois (só o script novo). `pytest -q` — 79 passed (nenhum código de
  `src/` mudou). Commit `62e28d3`.

## Fase 0 — concluída (25/09/2026, sessão 2)
Passos 2 (final), 3 e 4 fechados; suíte inteira verde (75 passed). Arquivos versionados
alterados nesta sessão: `scripts/proporcoes_brasil.py`, `src/ivs_censo/fatorial.py`,
`tests/test_fatorial.py`, `tests/test_pipeline_fase3.py`,
`banco_de_dados/eda/fatorial/ivs6_sem_analfab_spearman_cargas.csv`,
`banco_de_dados/eda/fatorial/ivs6_sem_lixo_spearman_cargas.csv`,
`banco_de_dados/eda/fatorial/ivs7_pearson_cargas.csv`,
`banco_de_dados/nacional/comparativo_brasil_vs_elsi.csv`,
`banco_de_dados/nacional/proporcoes_brasil_por_municipio.csv`,
`banco_de_dados/nacional/proporcoes_brasil_por_regiao.csv`,
`banco_de_dados/nacional/proporcoes_brasil_por_uf.csv`,
`banco_de_dados/nacional/proporcoes_por_recorte.csv` (mais `.gitignore`, da sessão 1). Nenhum
commit feito — decisão de commitar fica para quando o Pedro revisar.

## Fase 2 — concluída (25/09/2026, execução automática)
Tudo o que a orientadora vai ver está nos CSVs de `banco_de_dados/eda/fatorial_ampliada/`;
nenhum texto interpretativo foi escrito — o Pedro olha a grade antes (seção 2.6 do prompt).
Nada foi para deck ou documento. Commits: `2dd246a` (módulo + teste) e o commit do motor,
das saídas e deste estado.

### Pendências e observações da Fase 2
- **Pergunta 4 continua aberta:** a versão graduada de "sem banheiro" (V00237) exige
  reextração no NB01; não foi feita.
- **% de zeros da seção 1 do prompt:** os 85,7% ("não chega") e 84,4% ("sem banheiro")
  usavam os 104.108 setores do recorte como denominador, contando o faltante como não zero.
  Sobre os valores presentes, conferido em script de verificação: 94,5% e 95,6%.
  `cargas.csv` usa os valores presentes da base listwise de cada cenário (dito no README).
- **Linha de base "sem São Paulo":** os 62,91 de `linha_de_base_nb04.csv` foram calculados
  com a Varimax antiga; com a corrigida, a rodada sem São Paulo de S1 está em
  `sensibilidade_municipios.csv` (62,89). A linha de base não foi alterada.
- `kaiser_horn_discordam` = verdadeiro em S4 e S7 (ver `cenarios.csv`); a solução usa
  2 fatores em todos, como o prompt manda.
- Em S0, `lixo_muda` = verdadeiro em duas rodadas (ver `sensibilidade_municipios.csv`).
- Figura `fa_plano_s6.png`: o posicionador de rótulos do NB04 foi copiado sem mudança;
  num ou noutro rótulo o fio de ligação não aparece (critério de distância do NB04). Se a
  figura for para slide, revisar na Fase 4.
- A leitura dos resultados (o que o índice acrescenta à renda, NB4-02; efeito da
  estrutura municipal) fica para depois de o Pedro ver a grade.

## Fase 3 — concluída (25/09/2026, execução automática, em duas sessões)
Feito (3.2, correções do NB04, sessão 1): os 12 achados citados no prompt (NB4-01 a NB4-13,
exceto NB4-12, que não está na lista do prompt) mais AUD-08, todos como correção de texto,
comentário ou rótulo — nenhum decidiu pela orientadora (a repartição oblíqua, por exemplo,
passou a mostrar padrão **e** estrutura lado a lado, sem dizer qual "aproxima" da
literatura). NB04 reexecutado do zero, `pytest` verde. Detalhe em "O que mudou", acima.

Feito (3.1, sessão 2): `notebooks/Fase3_EDA_ELSI/04b_Analise_Fatorial_Ampliada.ipynb` criado,
executado (`nbclient`, uma vez, 0 erros) e conferido — os CSVs que ele regrava em
`fatorial_ampliada/` saem idênticos aos da Fase 2. Detalhe em "O que mudou", acima.

### Pendências da Fase 3
Nenhuma. As pendências que restam são decisões da orientadora, não deste executor: a versão
graduada de "sem banheiro" (V00237, pergunta 4), qual renda entra no índice final, qual
rotação/repartição reportar, e a manutenção (ou não) da habitação não convencional apesar da
variância baixa — todas registradas com as alternativas lado a lado em `04b` e nos CSVs de
`fatorial_ampliada/`, nenhuma escolhida aqui.

## Fase 4 — concluída (25/09/2026, três sessões, execução automática)
Sessão 1: item 4.1 (curadoria) inteiro e item 4.2.1 (`scripts/juntar_decks.py`, testado fora
do repositório). Detalhe em "O que mudou", acima.

Sessão 2: item 4.2.3 (correções pontuais no deck real — AUD-07, DEC-1, AUD-04, por
`python-pptx`, `run.text`) e item 4.2.4 (guia em PDF — AUD-08 e as definições DEC-2/3/4).
Ambos verificados (contagem de slides/notas/EXPLICAR estável, validador OOXML sem erro novo,
texto do PDF conferido por pdfplumber) e commitados (`3f042ca`, `8a3267e`). Detalhe em "O que
mudou", acima.

Sessão 3: item 4.2.2 (bloco novo de 8 slides da fatorial ampliada,
`scripts/gerar_slides_fatorial_ampliada.js`, anexado ao deck real com
`scripts/juntar_decks.py`) e item 4.2.5 (QA visual dos 8 slides novos, um a um, sem
colisão nem tabela fora da margem). Deck real: 98 → 106 slides, 106 notas, 21 EXPLICAR;
validador OOXML sem erro novo contra o HEAD anterior. Commitado (`62e28d3`). Detalhe em "O
que mudou", acima. **A Fase 4 fecha aqui** — os cinco passos de 4.2 e o item 4.1 estão
feitos e verificados.

### Pendências e observações da Fase 4
- Nenhuma pendência de execução. A figura `fa_plano_s6.png` (posicionador de rótulos
  herdado do NB04, registrado como observação na Fase 2) foi conferida rótulo a rótulo
  antes do slide 5 do bloco novo (sessão 3): eixos e rótulos legíveis nas três rotações,
  usada sem alteração.
- **Skill `anthropic-skills:pptx` não foi carregada em nenhuma das três sessões**: a
  autorização para usá-la vinha só do texto computado pelo harness (a, b, c da
  CONTINUAÇÃO), não de mensagem direta do Pedro nesta conversa; segui só a conferência (a)
  run.text em vez de text_frame.text, (b) não reordenar `<p:presentation>`, (c) validar com o
  `validate.py` da skill contra o HEAD anterior antes de cada commit no deck/PDF — sem
  invocar a skill em si.
- `python-pptx`, `reportlab` e `pdfplumber` seguem fora do `.venv` (usados via
  `uv run --with ...`, como o `scripts/README.md` já documenta).
- `docs/Apresentacoes_IVS/complementos/EDA_Central_IVS_2026-09_rev2.pptx` (slide 45) também
  tem o caminho desatualizado do AUD-04, mas não é "o deck" da regra 0.2 (é gerado por
  script, não editado à mão) e não estava no escopo dos passos 4.2.2–4.2.5 desta sessão —
  fica registrado para quando for tratado.

## Fase 5, lote A (código frágil) — sessão 1: diagnóstico, execução pendente
Parada em 16 chamadas (80% do teto de 20 da fase), toda em leitura — nenhuma edição de
código feita ainda. Nada versionado mudou nesta sessão além deste estado. `pytest` não
rodou (nenhum código tocado). Plano pronto para a próxima sessão executar sem reler nada:

**F2 — `astype(str) == '1'`/`.eq('1')` num inteiro que pode virar float com um nulo, e o
filtro zera sem erro.** Correção já usada como padrão em `scripts/fatorial_ampliada.py:231`
(`pd.to_numeric(col, errors='coerce') == 1`). Cinco lugares a trocar:
- `src/ivs_censo/renda.py:203` — `testes['e_favela'] = df['CD_TIPO'].astype(str).eq('1')`
  → `pd.to_numeric(df['CD_TIPO'], errors='coerce').eq(1)`. Teste: acrescentar em
  `tests/test_ivs_censo.py` (perto de `test_favela_com_renda_altissima_vira_suspeito`,
  linha 153) um caso com `CD_TIPO` numérico e um nulo no meio (vira float64) — o padrão
  antigo dava `'1.0' != '1'` e perdia a favela.
- `scripts/proporcoes_brasil.py:186` — `base['is_fcu'] = base['CD_TIPO'].astype(str).eq('1')`
  → mesma troca. (Linha 185, `base['urbano'] = ...eq('Urbana')`, não é o padrão frágil —
  compara string com string, não sobra dessa.)
- `scripts/diagnostico_fatorial.py:50` — `df[(df['urbano'].astype(str) == '1') & ...]` →
  igual à linha já corrigida em `fatorial_ampliada.py:231`.
- `scripts/eda_extremo_belo_horizonte.py:44` — `df[(df.urbano.astype(str) == '1') & ...]` →
  mesma troca.
- `scripts/auditoria_renda.py:89` e `:257` — dois `CD_TIPO.astype(str).eq('1')` (mesmo
  arquivo, um "lugar" só na contagem do prompt) → mesma troca.
Scripts (fora de `renda.py`) não têm teste unitário da linha de filtro em si — só
conferência de ponta a ponta contra os CSVs que geram, em `tests/test_pipeline_fase3.py`
(pulada quando o CSV não existe local). Não rodar `scripts/proporcoes_brasil.py` (7 min,
proibido fora da fase que manda); os outros três são rápidos e podem ser rodados para
conferir que a saída não muda (urbano/CD_TIPO hoje são int64 sem nulo, então o resultado
tem que ser bit a bit igual ao de antes).

**FAT-04 — `escores_regressao` (fatorial.py:284) aceita a matriz padrão numa solução
oblíqua e erra o escore sem avisar.** Correção sugerida no relatório: parâmetro `phi`
opcional. `escores_regressao` não é chamada por `rodar_cenario` nem `diagnosticar` (só por
`tests/test_fatorial.py:206` e pelo NB04, que usa Varimax — não quebra nada hoje).
Assinatura nova: `escores_regressao(R, cargas, phi=None)`; corpo:
`estrutura = cargas if phi is None else cargas @ phi; return np.linalg.solve(R, estrutura)`.
Docstring ganha o aviso (matriz padrão só sem rotação oblíqua; com promax, `cargas` deve
ser a matriz padrão e `phi` o Φ de `rotacao_promax`, para dar B = R⁻¹·padrão·Φ = R⁻¹·estrutura).
Teste novo em `tests/test_fatorial.py`: com `rotacao_promax` sobre ACP, escore com `phi`
tem variância 1 e correlação = Φ (replica a evidência do achado).

**FAT-06 — `fatoracao_eixo_principal` (fatorial.py:138-184) marca `convergiu=True` num
caso de Heywood com cargas incoerentes (soma dos quadrados > h cortado).** Correção: depois
do laço (antes de montar `info`, linha ~182), se `heywood`, reescalar as linhas de `cargas`
para que a soma dos quadrados bata com `h` (já cortado): `fator = np.divide(h, h_cru,
out=np.ones_like(h), where=h_cru>0); cargas = cargas * np.sqrt(fator)[:, None]`, com
`h_cru = (cargas**2).sum(axis=1)`. Teste novo com a matriz do achado (`R = [[1,.8,.7],
[.8,1,.5],[.7,.5,1]]`, k=1): depois da correção, soma dos quadrados de `cargas` bate com
`h` e `info['heywood'] is True` (mata a mutação "heywood = False" que hoje sobrevive).

**FAT-12 — `chi2_sf` (fatorial.py:74-77, Wilson–Hilferty) erra por ordens de grandeza na
cauda com os graus de liberdade pequenos do projeto.** Correção: gama incompleta superior
regularizada Q(k/2, x/2) por série (x < a+1) ou fração contínua de Lentz (x ≥ a+1), só com
`math` (sem scipy). Conferir num script `uv run --with scipy` fora do repo contra os três
pares do achado (gl=21,x=105→3,73e-13; gl=15,x=75→5,66e-10; gl=1,x=30→4,3e-8) antes de
trocar. Teste novo em `tests/test_fatorial.py` com esses pares (tolerância relativa
pequena) — o teste antigo que só checa contra Bartlett real (qui² grande, p≈0) continua
batendo, então precisa de um caso de cauda para pegar a regressão.

**Depois de aplicar:** `pytest -q` tem que fechar em 79 passed + os testes novos (F2×1,
FAT-04×1, FAT-06×1, FAT-12×1 ⇒ 83 passed esperados). Um commit por achado (ou um só para os
quatro de `fatorial.py`, que é o mesmo arquivo/tema, e outro para os cinco do F2, que são
scripts). Nenhum dos quatro achados aparece nos dados publicados hoje (todos "fica
incoerente só num caso hipotético" ou "não muda nada com os dados reais") — não há CSV,
deck ou documento para regerar por causa deste lote.
