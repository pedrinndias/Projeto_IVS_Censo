# Estado — demandas da orientadora (set/2026)

Linha de base: commit 3c426e8 · 25/09/2026

## Fases
- [x] Fase 0 — linha de base e destravamentos   (sessão de 25/09/2026, em duas partes; concluída)
- [ ] Fase 1 — demandas 1 e 2
- [ ] Fase 2 — fatorial ampliada
- [ ] Fase 3 — notebook 04b e NB04
- [ ] Fase 4 — curadoria e slides
- [ ] Fase 5 — lotes A · B · C · D

## Demandas da orientadora
| # | Demanda | Fase | Estado | Onde está o resultado |
|---|---|---|---|---|
| 1 | coluna de renda com a mediana | 1 | | |
| 2 | quadro de indicadores | 1 | | |
| 3 | fatorial sem bootstrap, sem e com rotação | 2 | | |
| 4 | separar útil × inútil | 4 | | |
| 5 | comparar "não chega" | 2 | | |
| 6 | juntar "sem banheiro" | 2 | | |
| 7 | adicionar canalização e sem banheiro | 2 | | |
| 8 | fatorial de tudo isso | 2 | | |
| 9 | habitação convencional | 2 | | |
| 10 | testar lixo | 2 | | |
| 11 | testar as duas rotações | 2 | | |

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
