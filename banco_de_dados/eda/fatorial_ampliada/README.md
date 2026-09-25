# Fatorial ampliada, sem bootstrap — procedência

Demandas 3, 5, 6, 7, 8, 9, 10 e 11 da orientadora (set/2026), tratadas como **uma análise
só**: uma grade de cenários rodados da mesma forma. Todo arquivo desta pasta, exceto
`linha_de_base_nb04.csv`, sai de:

    python scripts/fatorial_ampliada.py      # ~30 s; lê o .db da entrega em modo só leitura

A matemática é a de `src/ivs_censo/fatorial.py` (`rodar_cenario`, com a Varimax corrigida
em FAT-01). Índice, AUC e figuras copiam as funções do Notebook 04 (célula de origem
indicada no script). Nenhum número deste README é medição: os números estão nos CSVs.

## Método (igual ao NB04, para ser comparável)

- Recorte: `urbano == 1` (filtro numérico) e `Dados_sig == 'OK'`.
- Spearman; exclusão por lista (casos completos) **por cenário** — o `n` muda de um
  cenário para outro, e `perdidos_vs_S0` diz quanto.
- Extração por componentes principais (ACP); renda entra invertida (`renda_inv`).
- Kaiser (autovalor > 1) e Horn (50 simulações, até 20 mil linhas, semente 42) reportados
  lado a lado; a solução apresentada usa **2 fatores em todos os cenários**, para as
  rotações serem comparáveis. `kaiser_horn_discordam` marca quando os dois critérios
  divergem.
- Três soluções: sem rotação, Varimax e promax (κ = 4), esta com matriz padrão, matriz
  estrutura e Φ.
- **Convenção de sinal:** em todas as soluções, cada fator tem soma das cargas positiva
  (FAT-10, NB4-20). Na promax o sinal vale para padrão e estrutura, e Φ recebe sᵢ·sⱼ.
- **Sem bootstrap.** A incerteza aparece como sensibilidade por município (um de fora por
  vez), que **não** é intervalo de confiança.

## Cenários

| Cenário | Variáveis | Demanda |
|---|---|---|
| S0 | IVS-7 (referência; trava de sanidade contra o NB04) | — |
| S1 | IVS-6 (IVS-7 sem lixo; trava dos pesos com a Varimax corrigida) | 10 |
| S2 | IVS-7 + água não chega (`pct_agua_nao_encanada`) | 5, 7 |
| S3 | IVS-7 + sem água canalizada (`pct_sem_agua_canalizada`) | 7 |
| S4 | IVS-7 + sem banheiro (`pct_sem_banheiro`, V00495 — já contém a V00238) | 6, 7 |
| S5 | IVS-7 + moradia não convencional (`pct_moradia_nao_convencional`) | 9 |
| S6 | IVS-7 + as quatro ("tudo isso") | 8 |
| S7 | S6 sem lixo | 8, 10 |
| S0/S6 `_renda_sem_extremo`, `_renda_mediana_mun` | a mesma grade com as outras duas versões de renda (a original é o próprio S0/S6) | 1 (decisão aberta) |
| S0/S1/S6 `_postos_mun` | cada variável em posto percentil **dentro do município**, depois a mesma receita | estrutura municipal |

Nada aqui escolhe rotação, renda ou variável: as alternativas ficam lado a lado para a
orientadora decidir. O IVS final é do NB05.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `cenarios.csv` | uma linha por cenário: n, perdidos vs S0, KMO, MSA mínimo (e a variável), Bartlett (estatística e gl), determinante de R, autovalores 1–3, fatores por Kaiser e por Horn, variância explicada por 2 fatores, se o lixo fica sozinho num fator na Varimax |
| `cargas.csv` | formato longo (cenário × variável): cargas sem rotação, Varimax, promax padrão e estrutura; comunalidade (ortogonal e oblíqua), MSA, % de zeros **na base listwise do cenário**, peso da variável no índice |
| `pesos.csv` | repartição dos 2 fatores em cada solução (promax pela matriz padrão **e** pela estrutura), a variável de maior carga em cada fator, e Φ |
| `validacao_fcu.csv` | AUC contra `is_fcu` do índice de cada cenário (construído como o `indice_01` do NB04: pesos da Varimax, min-max global), ao lado das duas linhas de base — renda invertida sozinha e média simples de postos — na mesma base (NB4-02) |
| `autovalores.csv` | todos os autovalores de cada cenário e o patamar de Horn |
| `correlacao_s6.csv` | a matriz de Spearman de S6, a da figura 1 |
| `comparacao_nao_chega_banheiro.csv` | demandas 5 e 6: Spearman par a par (n de cada par) de "não chega" e de "sem banheiro" com o IVS-7 e com as outras categorias de água; perfil — mediana de cada variável do IVS-7 nos setores com o indicador > 0 e = 0; prova da junção (V00238 ≤ V00495) |
| `sensibilidade_municipios.csv` | S0, S1 e S6 com um município de fora por vez: peso do fator 1 (Varimax e promax padrão, alinhados à solução completa), variação, se o lixo continua sozinho num fator, e qual município mais move cada número |
| `linha_de_base_nb04.csv` | números do NB04 anteriores a esta análise (Fase 0); lidos pela trava de sanidade |
| `figuras/fa_correlacao_ampliada.png` | matriz de Spearman de S6, com uma linha separando as quatro novas |
| `figuras/fa_scree_s6.png` | scree plot de S6 com a linha de Horn e a de Kaiser |
| `figuras/fa_plano_s6.png` | plano fatorial de S6 em três painéis (sem rotação, Varimax, promax padrão); o rótulo de cada eixo sai das cargas (NB4-08) |
| `figuras/fa_sensibilidade_municipios.png` | peso do fator 1 na Varimax nas 70 rodadas de S1 e S6 |

## Trava de sanidade

O script para **sem gravar nada** se S0 não reproduzir o KMO do NB04 (lido de
`linha_de_base_nb04.csv`) ou se S1 não der os pesos da Varimax corrigida (valor esperado
fixado no script, com a explicação de FAT-01).

## Observação sobre o % de zeros

`pct_zeros` é calculado sobre os valores presentes na base listwise do cenário. Um % de
zeros calculado sobre todos os setores do recorte (contando o faltante como não zero)
sai menor; os dois não são comparáveis.
