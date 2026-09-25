# Estado — demandas da orientadora (set/2026)

Linha de base: commit 3c426e8 · 25/09/2026

## Fases
- [x] Fase 0 — linha de base e destravamentos   (sessão de 25/09/2026, em duas partes; concluída)
- [x] Fase 1 — demandas 1 e 2   (25/09/2026, execução automática; concluída)
- [x] Fase 2 — fatorial ampliada   (25/09/2026, execução automática; concluída)
- [ ] Fase 3 — notebook 04b e NB04
- [ ] Fase 4 — curadoria e slides
- [ ] Fase 5 — lotes A · B · C · D

## Demandas da orientadora
| # | Demanda | Fase | Estado | Onde está o resultado |
|---|---|---|---|---|
| 1 | coluna de renda com a mediana | 1 | concluída | `renda_media_mediana_mun` no .db/.csv da entrega; sensibilidade em `banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv` |
| 2 | quadro de indicadores | 1 | concluída | `banco_de_dados/entrega_orientadora/Quadro_Indicadores.{csv,xlsx,md}` |
| 3 | fatorial sem bootstrap, sem e com rotação | 2 | concluída | `banco_de_dados/eda/fatorial_ampliada/cargas.csv` e `pesos.csv` — sem rotação, Varimax e promax lado a lado, em todos os cenários |
| 4 | separar útil × inútil | 4 | | |
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
