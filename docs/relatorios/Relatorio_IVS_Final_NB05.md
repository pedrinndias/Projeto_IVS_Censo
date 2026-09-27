# Relatório — Notebook 05: Cálculo do IVS final

**Item 9 do pedido** de `docs/prompts/prompt_nb05_ivs_final_2026-09.md`. Método, achados, a
especificação de referência com as alternativas lado a lado, limitações e as perguntas que
continuam da orientadora. Todo número abaixo vem dos CSVs de
`banco_de_dados/eda/ivs_especificacoes/`, gerados por `scripts/ivs_especificacoes.py` (o
motor da Fase C) e conferidos, célula a célula, em
`notebooks/Fase3_EDA_ELSI/05_Calculo_IVS_Final.ipynb`.

## Método

O motor monta 324 especificações: renda (original · sem extremo · mediana municipal) ×
lixo (com · sem) × banheiro (fora · V00495 · graduado) = 18 bases, cada uma com 9 esquemas de
peso (sem rotação; Varimax com SS/50-50/60-40; promax com SS da matriz padrão, SS da
estrutura, comunalidades, 50-50 e 60-40) e 2 normalizações do índice (municipal e global). Uma
especificação é elegível quando KMO ≥ 0,70, MSA mínimo ≥ 0,50, comunalidade mínima ≥ 0,30 e
carga máxima mínima ≥ 0,40 (seção 2.2 do prompt) — critérios fixados antes de rodar. Entre as
elegíveis, a referência proposta é a de melhor posição média em três critérios de peso igual:
(a) estabilidade (amplitude do peso do fator 1 ao deixar um município de fora), (b) validade
discriminante dentro do município (AUC contra FCU) e (c) parcimônia (menos variáveis).

## Achados

1. **192 de 324 especificações são elegíveis** (96 com normalização municipal, 96 com normalização global).
2. **Renda:** entre as elegíveis, a AUC municipal média por versão de renda fica em 0,7964 (original), 0,7968 (sem o extremo de Belo Horizonte) e 0,7968 (mediana municipal) — as três coladas.
3. **Rotação:** sem rotação (um fator) é inelegível em toda a grade (0 de 36); Varimax elege 72 de 108; promax elege 120 de 180.
4. **Pesos na oblíqua (promax):** elegibilidade por método — 50_50: 24/36; 60_40: 24/36; comunalidades: 24/36; ss_estrutura: 24/36; ss_padrao: 24/36. Nos métodos de peso fixo (50-50, 60-40) a amplitude do peso do fator 1 é zero por construção; entre os métodos que dependem dos dados, a amplitude vai de 0,74 a 21,22 pontos percentuais.
5. **Lixo:** com lixo, 48 de 162 especificações são elegíveis; sem lixo, 144 de 162.
6. **Banheiro:** elegibilidade por versão — fora: 48/108; graduado: 48/108; v00495: 96/108. Faixas indefinidas (setor no único município de sua faixa) por versão — fora: 0; graduado: 108; v00495: 0.
7. **O que o índice acrescenta à renda** (item 6 do pedido): nas 192 especificações elegíveis, a AUC do índice fica sempre abaixo da renda invertida sozinha, global e na mediana municipal; dentro dos decis de renda de cada município fica sempre acima; somar o índice à renda na regressão logística sempre reduz a deviance. Na referência: estratos 0,7062 (índice) × 0,5900 (renda); deviance −135,5 (z 17,5), AUC 0,8900 → 0,8909.
8. **IVS final da referência:** definido para 73878 setores; faixas pela regra do IVS-BH 2012 — medio: 31052; baixo: 21270; elevado: 17622; muito_elevado: 3933; por quartis municipais — muito_elevado: 18493; medio: 18472; elevado: 18464; baixo: 18449. IVS médio mais baixo em São Raimundo do Doca Bezerra (0,0000; 1 setores) e mais alto em Rosário (0,5317; 15 setores) — tabela completa dos 70 municípios no notebook, seção 10.
9. **Perda de setores por dado ausente:** a base da especificação de referência fica com 73878 dos 104108 setores do recorte da seção 1 do prompt (30230 a menos, 29,0% — variável ausente nos componentes do banheiro graduado ou da renda, em parte por sigilo do IBGE). Dentro dessa base, o FCU em si está definido em 73878 de 73878 setores (sigilo específico do FCU nesta base: 0).

## A referência proposta e as alternativas (seção 2.2 do prompt)

A leitura **principal** (critério (a) = amplitude do peso do fator 1; critério (b) = AUC
municipal na amostra comum às três versões de banheiro) propõe
`original·lixo_sem·banheiro_graduado·promax·60_40·municipal` — postos 24,5º (estabilidade),
43,0º (AUC municipal) e 48,5º
(parcimônia), posição média 38,67. As três variantes de leitura
abaixo trocam a amostra, o critério (a) ou a normalização — nenhuma delas é a escolhida aqui:

| Leitura | Especificação | Elegíveis | Posto (a) | Posto (b) | Posto (c) | Posto médio |
|---|---|---:|---:|---:|---:|---:|
| principal | `original·lixo_sem·banheiro_graduado·promax·60_40·municipal` | 96 | 24,5 | 43,0 | 48,5 | 38,67 |
| amostra_propria | `original·lixo_sem·banheiro_v00495·promax·60_40·municipal` | 96 | 24,5 | 41,0 | 48,5 | 38,00 |
| estabilidade_pesos_variaveis | `sem_extremo·lixo_sem·banheiro_fora·promax·comunalidades·municipal` | 96 | 10,0 | 61,0 | 12,5 | 27,83 |
| normalizacao_global | `sem_extremo·lixo_sem·banheiro_fora·varimax·60_40·global` | 96 | 24,5 | 75,5 | 12,5 | 37,50 |

Isto é **proposta**, não decisão (seção 0.2 do prompt): a escolha entre a leitura principal e
as três alternativas continua com a orientadora.

## Limitações

- **Circularidade parcial com o FCU.** O achado 7 usa a queda de deviance de FCU (critério do
  IBGE que já incorpora condições de moradia) como medida do que o índice acrescenta à renda;
  parte da separação vem de as mesmas dimensões de saneamento aparecerem nos dois lados.
- **Falácia ecológica.** O IVS é calculado por setor censitário, mas a validação por AUC
  contra FCU e a comparação com o IVS-BH 2012 operam em agregados municipais ou por faixa —
  um padrão médio no setor ou no município não garante o mesmo padrão para cada domicílio.
- **Perda de setores por dado ausente.** Achado 9: 30230 dos
  104108 setores do recorte ficam fora da base da especificação de referência por
  variável ausente — em parte por sigilo do IBGE nos componentes do banheiro ou da renda, não
  só no FCU (que, nesta base, está definido em todos os setores que sobram).

## Perguntas à orientadora

Nenhuma é fechada por este notebook (seção 0.2 do prompt: "não decidir pela orientadora").

- Qual renda usar — original, sem o extremo de Belo Horizonte, ou mediana municipal (achado
  2)? As três ficam coladas em AUC municipal.
- Qual rotação — Varimax ou promax (achado 3)? Sem rotação é inelegível em toda a grade.
- Como dividir os pesos na solução oblíqua — SS da matriz padrão, SS da estrutura,
  comunalidades, 50/50 ou 60/40 da literatura (achado 4)? Os pesos fixos (50/50, 60/40) têm
  amplitude zero por construção e por isso vencem sempre o critério (a) como escrito.
- O lixo entra no índice (achado 5)?
- O banheiro entra, e em qual versão — fora, V00495 ou a graduada da Fase B (achado 6)?
- Normalização do índice — dentro do município (leitura principal) ou global (leitura
  `normalizacao_global` da tabela acima)?
- Qual regra de faixas — IVS-BH 2012 (achado 8) ou quartis municipais?
- Que peso a AUC contra FCU deve ter na escolha, dada a circularidade parcial (limitações)?
