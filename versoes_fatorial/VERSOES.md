# Versões da análise fatorial — renda × lixo × água × banheiro × moradia

Pedido do Pedro (07–08/10/2026): "Análise fatorial dos 3 tipos de rendas com versões com lixo e
sem lixo" e, além dessas 6, "mais versões adicionando os indicadores trabalhados de canalização
de água e com/sem banheiro, moradia convencional". **Lista, não execução.** Nada foi rodado. Em 08/10 o Pedro escolheu as 108 fichas; o prompt de
execução é `docs/prompts/prompt_versoes_fatorial_108_2026-10.md` e as leituras ficam em `INTERPRETACAO.md`.

## Os eixos

| Eixo | Opções | Variável |
|---|---|---|
| Renda | original · sem extremo · com mediana | `renda_media`, `renda_media_sem_extremo`, `renda_media_mediana_mun` (entram invertidas) |
| Lixo | com · sem | `pct_lixo_inad` |
| Água canalizada (somada à água inadequada do IVS) | nenhuma · não chega · sem canalização | `pct_agua_nao_encanada`, `pct_sem_agua_canalizada` |
| Banheiro | fora · sem banheiro · graduado | `pct_sem_banheiro` (V00495), `banheiro_graduado` |
| Moradia | sem · com não convencional | `pct_moradia_nao_convencional` |

Fixas em todas: água inadequada, esgoto, razão de moradores, analfabetismo e cor/raça.
"Não chega" e "sem canalização" não entram juntas, porque uma contém a outra: "sem canalização" = V00200 + V00201, e "não chega" = V00201.

**Total: 3 × 2 × 3 × 3 × 2 = 108 versões**, de 6 a 10 variáveis.
- 18 já existem na grade do NB05, com os 18 métodos de rotação, pesos e normalização.
- 8 existem na fatorial ampliada, mas com a receita do NB04 (Varimax), não com a da referência.
- As outras são novas.

## Antes de rodar: o que decidir

1. **Método fixo** (recomendado: o da referência proposta — promax, 60/40, municipal), ou os 18
   métodos da grade (1.944 rodadas).
2. **Amostra:** cada versão perde setores diferentes (o banheiro graduado e a "não chega" são os que mais
   perdem). Comparar só na amostra comum a todas, como o NB05 faz, ou cada uma na própria.
3. **Renda:** as três só diferem num setor (BH). Na grade do NB05 dão resultados iguais até a
   3ª casa. Rodar as três triplica a lista sem mudar o resultado.

## As 108 versões

| ID | Renda | Lixo | Água canalizada | Banheiro | Moradia | Variáveis | Já existe em |
|---|---|---|---|---|---|---|---|
| V001 | original | com | — | — | — | 7 | grade do NB05 (18 métodos); fatorial ampliada S0 (receita do NB04, Varimax) |
| V002 | original | com | — | — | + não convencional | 8 | fatorial ampliada S5 (receita do NB04, Varimax) |
| V003 | original | com | — | + sem banheiro (V00495) | — | 8 | grade do NB05 (18 métodos); fatorial ampliada S4 (receita do NB04, Varimax) |
| V004 | original | com | — | + sem banheiro (V00495) | + não convencional | 9 | **nova** |
| V005 | original | com | — | + banheiro graduado | — | 8 | grade do NB05 (18 métodos) |
| V006 | original | com | — | + banheiro graduado | + não convencional | 9 | **nova** |
| V007 | original | com | + não chega | — | — | 8 | fatorial ampliada S2 (receita do NB04, Varimax) |
| V008 | original | com | + não chega | — | + não convencional | 9 | **nova** |
| V009 | original | com | + não chega | + sem banheiro (V00495) | — | 9 | **nova** |
| V010 | original | com | + não chega | + sem banheiro (V00495) | + não convencional | 10 | **nova** |
| V011 | original | com | + não chega | + banheiro graduado | — | 9 | **nova** |
| V012 | original | com | + não chega | + banheiro graduado | + não convencional | 10 | **nova** |
| V013 | original | com | + sem canalização | — | — | 8 | fatorial ampliada S3 (receita do NB04, Varimax) |
| V014 | original | com | + sem canalização | — | + não convencional | 9 | **nova** |
| V015 | original | com | + sem canalização | + sem banheiro (V00495) | — | 9 | **nova** |
| V016 | original | com | + sem canalização | + sem banheiro (V00495) | + não convencional | 10 | **nova** |
| V017 | original | com | + sem canalização | + banheiro graduado | — | 9 | **nova** |
| V018 | original | com | + sem canalização | + banheiro graduado | + não convencional | 10 | **nova** |
| V019 | original | sem | — | — | — | 6 | grade do NB05 (18 métodos); fatorial ampliada S1 (receita do NB04, Varimax) |
| V020 | original | sem | — | — | + não convencional | 7 | **nova** |
| V021 | original | sem | — | + sem banheiro (V00495) | — | 7 | grade do NB05 (18 métodos) |
| V022 | original | sem | — | + sem banheiro (V00495) | + não convencional | 8 | **nova** |
| V023 | original | sem | — | + banheiro graduado | — | 7 | grade do NB05 (18 métodos) |
| V024 | original | sem | — | + banheiro graduado | + não convencional | 8 | **nova** |
| V025 | original | sem | + não chega | — | — | 7 | **nova** |
| V026 | original | sem | + não chega | — | + não convencional | 8 | **nova** |
| V027 | original | sem | + não chega | + sem banheiro (V00495) | — | 8 | **nova** |
| V028 | original | sem | + não chega | + sem banheiro (V00495) | + não convencional | 9 | **nova** |
| V029 | original | sem | + não chega | + banheiro graduado | — | 8 | **nova** |
| V030 | original | sem | + não chega | + banheiro graduado | + não convencional | 9 | **nova** |
| V031 | original | sem | + sem canalização | — | — | 7 | **nova** |
| V032 | original | sem | + sem canalização | — | + não convencional | 8 | **nova** |
| V033 | original | sem | + sem canalização | + sem banheiro (V00495) | — | 8 | **nova** |
| V034 | original | sem | + sem canalização | + sem banheiro (V00495) | + não convencional | 9 | **nova** |
| V035 | original | sem | + sem canalização | + banheiro graduado | — | 8 | **nova** |
| V036 | original | sem | + sem canalização | + banheiro graduado | + não convencional | 9 | **nova** |
| V037 | sem extremo | com | — | — | — | 7 | grade do NB05 (18 métodos); fatorial ampliada S0_renda_sem_extremo (receita do NB04, Varimax) |
| V038 | sem extremo | com | — | — | + não convencional | 8 | **nova** |
| V039 | sem extremo | com | — | + sem banheiro (V00495) | — | 8 | grade do NB05 (18 métodos) |
| V040 | sem extremo | com | — | + sem banheiro (V00495) | + não convencional | 9 | **nova** |
| V041 | sem extremo | com | — | + banheiro graduado | — | 8 | grade do NB05 (18 métodos) |
| V042 | sem extremo | com | — | + banheiro graduado | + não convencional | 9 | **nova** |
| V043 | sem extremo | com | + não chega | — | — | 8 | **nova** |
| V044 | sem extremo | com | + não chega | — | + não convencional | 9 | **nova** |
| V045 | sem extremo | com | + não chega | + sem banheiro (V00495) | — | 9 | **nova** |
| V046 | sem extremo | com | + não chega | + sem banheiro (V00495) | + não convencional | 10 | **nova** |
| V047 | sem extremo | com | + não chega | + banheiro graduado | — | 9 | **nova** |
| V048 | sem extremo | com | + não chega | + banheiro graduado | + não convencional | 10 | **nova** |
| V049 | sem extremo | com | + sem canalização | — | — | 8 | **nova** |
| V050 | sem extremo | com | + sem canalização | — | + não convencional | 9 | **nova** |
| V051 | sem extremo | com | + sem canalização | + sem banheiro (V00495) | — | 9 | **nova** |
| V052 | sem extremo | com | + sem canalização | + sem banheiro (V00495) | + não convencional | 10 | **nova** |
| V053 | sem extremo | com | + sem canalização | + banheiro graduado | — | 9 | **nova** |
| V054 | sem extremo | com | + sem canalização | + banheiro graduado | + não convencional | 10 | **nova** |
| V055 | sem extremo | sem | — | — | — | 6 | grade do NB05 (18 métodos) |
| V056 | sem extremo | sem | — | — | + não convencional | 7 | **nova** |
| V057 | sem extremo | sem | — | + sem banheiro (V00495) | — | 7 | grade do NB05 (18 métodos) |
| V058 | sem extremo | sem | — | + sem banheiro (V00495) | + não convencional | 8 | **nova** |
| V059 | sem extremo | sem | — | + banheiro graduado | — | 7 | grade do NB05 (18 métodos) |
| V060 | sem extremo | sem | — | + banheiro graduado | + não convencional | 8 | **nova** |
| V061 | sem extremo | sem | + não chega | — | — | 7 | **nova** |
| V062 | sem extremo | sem | + não chega | — | + não convencional | 8 | **nova** |
| V063 | sem extremo | sem | + não chega | + sem banheiro (V00495) | — | 8 | **nova** |
| V064 | sem extremo | sem | + não chega | + sem banheiro (V00495) | + não convencional | 9 | **nova** |
| V065 | sem extremo | sem | + não chega | + banheiro graduado | — | 8 | **nova** |
| V066 | sem extremo | sem | + não chega | + banheiro graduado | + não convencional | 9 | **nova** |
| V067 | sem extremo | sem | + sem canalização | — | — | 7 | **nova** |
| V068 | sem extremo | sem | + sem canalização | — | + não convencional | 8 | **nova** |
| V069 | sem extremo | sem | + sem canalização | + sem banheiro (V00495) | — | 8 | **nova** |
| V070 | sem extremo | sem | + sem canalização | + sem banheiro (V00495) | + não convencional | 9 | **nova** |
| V071 | sem extremo | sem | + sem canalização | + banheiro graduado | — | 8 | **nova** |
| V072 | sem extremo | sem | + sem canalização | + banheiro graduado | + não convencional | 9 | **nova** |
| V073 | com mediana | com | — | — | — | 7 | grade do NB05 (18 métodos); fatorial ampliada S0_renda_mediana_mun (receita do NB04, Varimax) |
| V074 | com mediana | com | — | — | + não convencional | 8 | **nova** |
| V075 | com mediana | com | — | + sem banheiro (V00495) | — | 8 | grade do NB05 (18 métodos) |
| V076 | com mediana | com | — | + sem banheiro (V00495) | + não convencional | 9 | **nova** |
| V077 | com mediana | com | — | + banheiro graduado | — | 8 | grade do NB05 (18 métodos) |
| V078 | com mediana | com | — | + banheiro graduado | + não convencional | 9 | **nova** |
| V079 | com mediana | com | + não chega | — | — | 8 | **nova** |
| V080 | com mediana | com | + não chega | — | + não convencional | 9 | **nova** |
| V081 | com mediana | com | + não chega | + sem banheiro (V00495) | — | 9 | **nova** |
| V082 | com mediana | com | + não chega | + sem banheiro (V00495) | + não convencional | 10 | **nova** |
| V083 | com mediana | com | + não chega | + banheiro graduado | — | 9 | **nova** |
| V084 | com mediana | com | + não chega | + banheiro graduado | + não convencional | 10 | **nova** |
| V085 | com mediana | com | + sem canalização | — | — | 8 | **nova** |
| V086 | com mediana | com | + sem canalização | — | + não convencional | 9 | **nova** |
| V087 | com mediana | com | + sem canalização | + sem banheiro (V00495) | — | 9 | **nova** |
| V088 | com mediana | com | + sem canalização | + sem banheiro (V00495) | + não convencional | 10 | **nova** |
| V089 | com mediana | com | + sem canalização | + banheiro graduado | — | 9 | **nova** |
| V090 | com mediana | com | + sem canalização | + banheiro graduado | + não convencional | 10 | **nova** |
| V091 | com mediana | sem | — | — | — | 6 | grade do NB05 (18 métodos) |
| V092 | com mediana | sem | — | — | + não convencional | 7 | **nova** |
| V093 | com mediana | sem | — | + sem banheiro (V00495) | — | 7 | grade do NB05 (18 métodos) |
| V094 | com mediana | sem | — | + sem banheiro (V00495) | + não convencional | 8 | **nova** |
| V095 | com mediana | sem | — | + banheiro graduado | — | 7 | grade do NB05 (18 métodos) |
| V096 | com mediana | sem | — | + banheiro graduado | + não convencional | 8 | **nova** |
| V097 | com mediana | sem | + não chega | — | — | 7 | **nova** |
| V098 | com mediana | sem | + não chega | — | + não convencional | 8 | **nova** |
| V099 | com mediana | sem | + não chega | + sem banheiro (V00495) | — | 8 | **nova** |
| V100 | com mediana | sem | + não chega | + sem banheiro (V00495) | + não convencional | 9 | **nova** |
| V101 | com mediana | sem | + não chega | + banheiro graduado | — | 8 | **nova** |
| V102 | com mediana | sem | + não chega | + banheiro graduado | + não convencional | 9 | **nova** |
| V103 | com mediana | sem | + sem canalização | — | — | 7 | **nova** |
| V104 | com mediana | sem | + sem canalização | — | + não convencional | 8 | **nova** |
| V105 | com mediana | sem | + sem canalização | + sem banheiro (V00495) | — | 8 | **nova** |
| V106 | com mediana | sem | + sem canalização | + sem banheiro (V00495) | + não convencional | 9 | **nova** |
| V107 | com mediana | sem | + sem canalização | + banheiro graduado | — | 8 | **nova** |
| V108 | com mediana | sem | + sem canalização | + banheiro graduado | + não convencional | 9 | **nova** |
