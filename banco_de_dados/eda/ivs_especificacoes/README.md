# Motor de especificações do IVS (NB05, Fase C) — procedência

Itens 1 a 6 do pedido da orientadora (set/2026): renda, rotação, pesos na oblíqua, lixo,
banheiro e o que o índice acrescenta à renda, tratados como **uma grade só**, rodada da
mesma forma. Todo arquivo desta pasta sai de:

    python scripts/ivs_especificacoes.py     # alguns minutos; lê o .db da entrega em modo só leitura

A matemática é a de `src/ivs_censo/fatorial.py` (`rodar_cenario`, `reparticao`,
`comunalidades_obliquas`) e a do motor da Fase 2 (`scripts/fatorial_ampliada.py`:
`carregar`, `montar`, `pesos_indice`, `indice_01`, `auc_postos`), reaproveitadas sem
reescrever. Nenhum número deste README é medição: os números estão nos CSVs.
Especificação da grade e critérios: `docs/prompts/prompt_nb05_ivs_final_2026-09.md`,
seções 2.1 e 2.2.

## A grade

| Dimensão | Alternativas |
|---|---|
| Renda (invertida) | original · sem extremo · mediana municipal |
| Lixo | com · sem |
| Banheiro | fora · V00495 (`pct_sem_banheiro`) · graduado |
| Rotação | sem rotação (um fator só: o teste de "um fator ou dois") · Varimax · promax (κ = 4) |
| Pesos entre as dimensões | Varimax: SS, 50/50, 60/40 · promax: SS da padrão, SS da estrutura, comunalidades, 50/50, 60/40 · sem rotação: nenhum |
| Normalização do índice | min-max dentro do município (referência) · min-max global (sensibilidade) |
| Faixas | regra do IVS-BH 2012 · quartis (ambas dentro do município) |

Renda × lixo × banheiro = 18 bases; em cada uma, 9 esquemas de peso = 162 índices; com as
duas normalizações, 324 especificações (uma linha cada em `especificacoes.csv`), cada uma
classificada pelas duas regras de faixa.

## Método

- **Recorte e amostra.** `urbano == 1` e `Dados_sig == 'OK'`; Spearman; exclusão por lista
  **por base** (`n`, `perdidos_vs_recorte`). **Amostra comum**: casos completos em todas as
  variáveis de todas as especificações (`n_comum`). As métricas que comparam
  especificações saem nas duas amostras (sufixos `_propria` e `_comum`); com `n`
  diferentes, a amostra própria mistura efeito da especificação com efeito da amostra.
- **Banheiro graduado** = (1·V00236 + 2·V00237 + 3·V00238) / (3·V00001): as três partes de
  V00495, mutuamente exclusivas (partição conferida na Fase B,
  `../fatorial_ampliada/banheiro_particao.csv`); faltante se alguma parte faltar.
- **F1** é a dimensão socioeconômica: aquela em que a renda invertida tem a maior carga
  absoluta. `peso_f1` é o peso dela, em %.
- **Pesos.** SS = soma dos quadrados das cargas, normalizada (`reparticao`, o do NB04).
  "Comunalidades" (a "variância única" da seção 2.1) = a comunalidade oblíqua de cada
  variável, diag(PΦPᵀ), contada uma vez, na dimensão da sua maior carga padrão, somada por
  dimensão e normalizada — **leitura operacional**, registrada como pergunta. 60/40 = 0,6
  para F1 (socioeconômica) e 0,4 para a outra (saneamento), como no IVS-BH 2012.
- **Índice**, como o do NB04: `pesos_indice(M, rep)` manda cada variável para a dimensão
  de maior carga e reparte o peso da dimensão pelo quadrado da carga (M = Varimax, a matriz
  padrão em todos os métodos da promax, ou a carga única); `indice_01` normaliza por min-max
  e soma com esses pesos — global, ou com mín e máx de cada município. Variável constante
  num município (`pares_mun_var_constantes`) não contribui para o índice ali.
- **Faixas**, dentro de cada município. Regra do IVS-BH 2012 (PDF em `docs/referencias/`,
  p. 7): médio = média ± 0,5 DP; baixo, abaixo; elevado, até média + 1,5 DP; muito
  elevado, acima. Quartis: um quarto dos setores do município em cada faixa. Município com
  um único setor na amostra não tem DP: o setor fica sem faixa pela regra do IVS-BH
  (`faixas_indefinidas`). Os números dos pesos do Quadro 3 (p. 7) não estão na camada de
  texto do PDF; o 60/40 segue a seção 2.1 do prompt.
- **Elegibilidade** (seção 2.2, fixada antes de rodar): KMO ≥ 0,70; MSA ≥ 0,50 em toda
  variável; comunalidade ≥ 0,30 em toda variável; toda variável com carga ≥ 0,40 em algum
  fator (na promax, a matriz padrão). Falhou um critério, a especificação fica inelegível —
  nada é corrigido tirando variável. As colunas `*_ok`, `comunalidade_min_variavel` e
  `carga_max_min_variavel` dizem qual critério e qual variável.
- **Estabilidade**: um município de fora por vez, só nas fatorações elegíveis, uma vez por
  fatoração (não por normalização nem faixa). `amp_peso_f1` = amplitude do peso de F1
  (critério a); `amp_peso_var_max` = a maior amplitude do peso de uma variável no índice.
  Nos pesos fixos (50/50, 60/40), `amp_peso_f1` é zero por construção.
- **Validade contra FCU**: AUC por Mann–Whitney (`auc_postos`), global e mediana dentro dos
  municípios com ao menos 30 setores de FCU e 30 fora (`n_mun_*` diz quantos entram).
- **Referência proposta** (seção 2.2): entre as elegíveis com normalização municipal,
  melhor posição média, com peso igual, em (a) `amp_peso_f1`, (b) mediana municipal da AUC
  na amostra comum e (c) número de variáveis; empate, a mais próxima do IVS-BH 2012 (renda
  original, com lixo, sem banheiro, 60/40) e, se ainda empatar, a maior AUC municipal.
  **É proposta, não decisão.** `referencia.csv` traz também três leituras de sensibilidade:
  (b) na amostra própria; (a) pela amplitude dos pesos das variáveis; normalização global.
  Correlação de postos e mudança de faixa são medidas contra a proposta da leitura principal.
- **O que o índice acrescenta à renda** (item 6, `acrescimo_renda.csv`, só elegíveis): AUC
  do índice × renda invertida sozinha × média de postos com pesos iguais — global, mediana
  municipal e **dentro dos decis de renda de cada município** (AUC de cada estrato, somada
  pelos pares FCU × fora, peso n1·n0); regressão logística FCU ~ renda e FCU ~ renda +
  índice, por IRLS em numpy, com preditores padronizados: deviance, queda de deviance, z do
  índice e AUC dos dois modelos. `conclusao` resume os números, sem adjetivo.
- **Limite.** FCU é critério do IBGE que já usa condições de moradia: há circularidade
  parcial com as variáveis de saneamento, e a AUC contra FCU não é validação independente.
- **Sem bootstrap.** A estabilidade por município não é intervalo de confiança.

## Trava (C.5)

IVS-6 (sem lixo), renda original, Varimax, pesos SS, normalização global = o índice do
NB04. O script confere o peso de F1, a AUC do índice e a AUC da renda invertida sozinha
(constante `TRAVA`) **antes** de gravar qualquer arquivo; `tests/test_ivs_especificacoes.py`
repete a conferência.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `especificacoes.csv` | uma linha por especificação: base, rotação, pesos, normalização; `n` e perdidos; KMO, MSA, Bartlett, Kaiser, Horn; critérios de elegibilidade; peso de F1 e estabilidade; AUC nas duas amostras; comparação com a proposta; postos e posição na leitura principal |
| `pesos.csv` | por base × rotação × método: peso de F1 e F2 e, por variável, peso no índice (%) e dimensão (1 = F1) |
| `avaliacao.csv` | as métricas de avaliação em formato longo, uma linha por especificação e amostra |
| `acrescimo_renda.csv` | item 6, para as elegíveis (`referencia` marca a proposta) |
| `estabilidade.csv` | um município de fora por vez: resumo por fatoração elegível e método de peso |
| `referencia.csv` | a proposta de cada leitura, os postos e o porquê |
| `ivs_referencia_por_setor.csv` | **fora do git** (regra `*_por_setor.csv` do `.gitignore`; regenerável pelo script): índice e faixas da proposta por setor, e o mesmo índice com normalização global |
| `figuras/auc_por_especificacao.png` | AUC global e mediana municipal por especificação, com a linha da renda sozinha |
| `figuras/peso_f1_por_especificacao.png` | peso de F1 por fatoração elegível, com a faixa de um município de fora por vez |
| `figuras/concordancia_faixas.png` | faixas da proposta × principais alternativas, na amostra comum |
