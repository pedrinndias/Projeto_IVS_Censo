# Estado — fatorial multiversão e apresentações (out/2026)

Prompt: `docs/prompts/prompt_fatorial_multiversao_2026-10.md`

## Situação: **fases 0 a 7 concluídas** (22/10/2026) — próximas sessões são de correção, depois das respostas da orientadora

**22/10/2026 — o Pedro pediu execução automática de todas as fases, sem parar** ("Execute todas
as fases de forma automática sem parar"). Isso inclui pular a aprovação do piloto (Fase 5): os
12 decks saem no mesmo layout de uma vez.

## Pré-registro (gravado em 22/10/2026; não muda depois da Fase 1)

### Perguntas e padrões

| # | Pergunta à orientadora | Padrão enquanto não houver resposta |
|---|---|---|
| P1 | Reflexivo, formativo ou híbrido? | Híbrido |
| P2 | Quais das 12 entram? | Os 7 do Quadro 1 |
| P3 | Sigilo do analfabetismo? | Ausente; imputações (limite inferior e zero) como sensibilidade |
| P4 | Régua: min-max municipal, min-max global ou postos no município? | Min-max municipal |
| P5 | Rotação e método de peso? | Promax com 60/40 |

IVS proposto = combinação dos cinco padrões, sempre marcado como proposta.

### Critérios

- Elegibilidade: KMO ≥ 0,70; MSA mínimo ≥ 0,50; comunalidade mínima ≥ 0,30; carga máxima mínima ≥ 0,40.
- Equivalência: Spearman dentro do município ≥ 0,95 **e** troca de faixa < 10%.
- Perda de base: > 5% dos 104.108 setores → marcada, com perfil dos perdidos.
- Semente 42.

### Variáveis

AGU `pct_agua_inad` · ESG `pct_esgoto_inad` · LIX `pct_lixo_inad` · MOR `razao_moradores` ·
ANA `pct_analfab` · REN `renda_inv` (sem o extremo, invertida) · PPI `pct_raca_pretpardind` ·
CAN `pct_sem_agua_canalizada` · BAN `pct_sem_banheiro` · MNC `pct_moradia_nao_convencional` ·
IDO `pct_idoso_60mais` · CRI `pct_pop_0a14`. Só a renda é invertida.


## Resultados (22/10/2026)

- **Fase 1:** 4.017 combinações × 2 réguas = 8.034 fatoriais (~22 min). Trava: KMO do núcleo no conjunto
  0,7825 = NB04. Elegíveis: 3,3% no conjunto, 0,6% dentro dos municípios. Lixo, moradia
  não convencional e sem banheiro têm comunalidade mediana < 0,30 nas duas réguas; dentro dos municípios
  também água (0,13), esgoto (0,30) e sem água canalizada (0,33) ficam no limite.
- **Fase 2:** 999 especificações; 6 elegíveis (todas sem lixo, analfabetismo imputado com zero,
  Varimax). Veredito dos eixos contra o IVS proposto: conjunto — decisão necessária (até
  36,1% de troca de faixa); normalização — decisão necessária
  (31,8%, postos no município); rotação e peso — decisão necessária
  (18,5%, sem rotação); sigilo — equivalentes
  (2,7%).
- **Fase 3:** 4 finalistas (E0009, E0171, E0027, E0001). IVS proposto (E0009) em 87.544 setores; o proposto
  **não passa** nos critérios pré-registrados (comunalidade mínima 0,052, do lixo). Tucker entre metades:
  0,967 (F1) e 0,924 (F2).
- **Fases 4 a 7 (2ª rodada, 22/10/2026 — pedido do Pedro: "para cada slide explique o que está acontecendo, o
  que é aquilo, para que serve, explique o gráfico; quero a análise exploratória de cada indicador antes da
  fatorial"):** cada slide de conteúdo tem um visual (gráfico ou tabela) e a coluna "O que é / Para que serve /
  Como ler / O que mostra". Decks de indicador com 37–38 slides (parte A exploratória: definição, cálculo,
  adequações, cobertura e sigilo, descritivas, histograma, boxplot, acumulada, percentis, região, porte, 70
  municípios, desigualdade interna, favela, gradiente de renda, Brasil × 70, extremos; parte B na fatorial).
  Deck final com 81 slides, com uma seção exploratória dos 12. 215 figuras. Verificador exige "O que é" e
  "Como ler" em todo slide de conteúdo; verde nas 7 fases; folhas de contato vistas (REN, FIN).

## Decisões tomadas na execução (registrar para o Pedro)

| Ponto | O que foi feito | Por quê |
|---|---|---|
| Extração nas camadas 2 e 3 | Eixo principal, como na camada 1 | Com componentes principais o lixo vira um fator sozinho e leva 40% do peso no "60/40" (NB04, achado 8) |
| Variável com carga negativa no índice | Entra invertida (sinal da carga na própria dimensão) | Senão o peso, que vem do quadrado da carga, a somaria ao contrário (ex.: idosos) |
| Âncora da dimensão socioeconômica sem a renda | Analfabetismo; sem ele, cor/raça | `ie.reparticoes` acha F1 pela renda |
| Faixas na comparação entre versões | Refeitas na amostra comum | Sem isso o eixo sigilo dava 11,4% de troca, que era efeito de amostra (2,7% de método) — achado do /ponytail-review |
| Alternativa de cada eixo nos finalistas | A de maior troca de faixa | Mostra o custo máximo da escolha |
| Piloto (Fase 5) | Sem parada para aprovação | Pedido do Pedro: execução sem parar |
| Verificador da Fase 4 | Estrutural (sem nan, figuras e fontes existem, IDs nos slides) | Não confere cada número contra o CSV: os números saem do código que lê o CSV, mas a conferência célula a célula não foi feita |

## Respostas da orientadora

| Pergunta | Resposta | Data |
|---|---|---|
| P1 … P5 | aguardando | — |

## Decisões do Pedro

| Ponto | Resposta | Data |
|---|---|---|
| 12 arquivos + 1 final; idosos e crianças com deck; piloto na renda | padrão proposto, sem resposta | 22/10/2026 |
| Executar todas as fases sem parar | **pedido** | 22/10/2026 |

## Fase 0 — correção do índice municipal

`scripts/ivs_especificacoes.py`: `indice` deixa ausente o município sem variação em nenhum
componente (antes: 0,0000); `faixas` por quartis exige ≥ 4 setores no município (antes: um setor
só virava "muito elevado"). Dois testes novos; suíte 119 verde. **Nada foi regerado**: na
referência do NB05 muda 1 setor (São Raimundo do Doca Bezerra); `eda_versoes.indice_versao`
(normalizações z e postos) não foi tocado e continua dando 0 a município sem variação.

## Mensagem à orientadora (para o Pedro enviar)

> Professora, para seguir com a análise fatorial a partir do relatório parcial corrigido,
> preciso da sua posição em cinco pontos. Enquanto não tiver resposta, sigo com o padrão entre
> parênteses e mostro o custo de cada alternativa.
>
> 1. O IVS deve ser lido como um construto único medido pelos indicadores, como um índice
>    formado pela soma de facetas, ou como um híbrido (a fatorial define os pesos dentro de cada
>    dimensão e a divisão entre saneamento e socioeconômica é escolha nossa)? (híbrido)
> 2. Quais dos 12 indicadores do relatório entram no índice? (os 7 do Quadro 1)
> 3. Como tratar o analfabetismo suprimido por sigilo em 16% dos setores? (deixar ausente e
>    mostrar o efeito de imputar o mínimo possível)
> 4. A padronização é dentro de cada município, com a régua do conjunto, ou por postos dentro
>    do município? (dentro de cada município)
> 5. Qual rotação e qual divisão de pesos: sem rotação, Varimax ou promax; pesos da fatorial,
>    50/50 ou 60/40 do IVS de 2012? (promax com 60/40)

## Achados do /ponytail-review por fase

| Fase | Corrigido | Registrado (só estilo) |
|---|---|---|
| 0–3 | 1) troca de faixa medida na amostra comum; 2) AUC da renda vazia sem a renda; 3) teste de `comparar`; 4) constante sem uso | — |
| 4–7, 2ª rodada (/ponytail-review) | frase "maior proporção sem dado no Norte (0,0%)" quando não falta dado em água, lixo, moradores e moradia — corrigida; conferido que nenhuma coluna de explicação estoura nem fica abaixo da fonte 9 | — |
| 4–7, 1ª rodada (folhas de contato; sem /ponytail-review formal) | `~` sobre coluna lida do CSV dava "-17 de 12"; R$ sem caber na coluna; texto do P1 tornado factual; rótulos amontoados no histograma; "100,0%" para 99,99% | — |

## Histórico

| Fase | Data | Resultado | Chamadas |
|---|---|---|---:|
| 0 | 22/10/2026 | Estado, correção do índice com 2 testes, mensagem à orientadora | 6 |
| 1–3 | 22/10/2026 | Motor `fatorial_multiversao.py`, 6 testes; camadas rodadas e verificadas | — |
| 4–7 | 22/10/2026 | `dados_apresentacoes_multiversao.py`, `gerar_decks_multiversao.js`, `verificar_multiversao.py`; 13 decks; suíte 125 verde | — |
| 4–7, 2ª rodada | 22/10/2026 | Decks reescritos com explicação por slide e EDA completa: 12 × 37–38 slides + final de 81 | — |
