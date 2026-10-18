# Notas do apresentador da v2 (fontes de cada slide), guardadas antes de sair do deck

## 1 · A01

[A01] Relatório descritivo do andamento
Requisitos: R1, R14
Fontes: —
1

## 2 · DM00

[DM00] As demandas e como foram cobertas
Requisitos: R2, R3
Fontes: docs/prompts/estado_demandas_2026-09.md:16-26
2

## 3 · DM01

[DM01] As 11 demandas
Requisitos: R2
Fontes: docs/prompts/estado_demandas_2026-09.md:16-26
3

## 4 · DM02

[DM02] Demanda 1 — a renda com a mediana
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:16; docs/prompts/estado_demandas_2026-09.md:35-38; docs/prompts/estado_demandas_2026-09.md:105-120; src/ivs_censo/renda.py:91-97
Fontes: docs/prompts/estado_demandas_2026-09.md:16, 35-38, 105-120; banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv
4

## 5 · DM03

[DM03] Demanda 2 — quadro de indicadores
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:17; docs/prompts/estado_demandas_2026-09.md:122-125; docs/prompts/estado_nb05_2026-09.md:1; docs/prompts/estado_nb05_2026-09.md:234-245
Fontes: docs/prompts/estado_demandas_2026-09.md:17; docs/prompts/estado_demandas_2026-09.md:122-125; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv
5

## 6 · DM04

[DM04] Demanda 3 — fatorial sem bootstrap, sem e com rotação
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:18; docs/prompts/estado_demandas_2026-09.md:28-61; docs/prompts/estado_demandas_2026-09.md:140-148
Fontes: docs/prompts/estado_demandas_2026-09.md:18; docs/prompts/estado_demandas_2026-09.md:39-40, 140-148; banco_de_dados/eda/fatorial_ampliada/pesos.csv (S0)
6

## 7 · DM06

[DM06] Demanda 5 — comparar "não chega"
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:20; docs/prompts/estado_demandas_2026-09.md:28-61; docs/prompts/estado_demandas_2026-09.md:288-293
Fontes: docs/prompts/estado_demandas_2026-09.md:20; docs/prompts/estado_demandas_2026-09.md:41-42, 290-293; banco_de_dados/eda/fatorial_ampliada/comparacao_nao_chega_banheiro.csv (bloco spearman)
7

## 8 · DM07

[DM07] Demanda 6 — juntar "sem banheiro"
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:21; docs/prompts/estado_demandas_2026-09.md:28-61; docs/prompts/estado_nb05_2026-09.md:1; docs/prompts/estado_nb05_2026-09.md:195-245
Fontes: docs/prompts/estado_demandas_2026-09.md:21; docs/prompts/estado_demandas_2026-09.md:43-45; docs/prompts/estado_nb05_2026-09.md:195-245; comparacao_nao_chega_banheiro.csv (prova_juncao); banco_de_dados/eda/fatorial_ampliada/banheiro_particao.csv
8

## 9 · DM08

[DM08] Demanda 7 — adicionar canalização e sem banheiro
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:22; docs/prompts/estado_demandas_2026-09.md:140-148
Fontes: docs/prompts/estado_demandas_2026-09.md:22; banco_de_dados/eda/fatorial_ampliada/cenarios.csv (n, perdidos_vs_S0, kmo)
9

## 10 · DM09

[DM09] Demanda 8 — fatorial de tudo isso
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:23; docs/prompts/estado_demandas_2026-09.md:28-61
Fontes: docs/prompts/estado_demandas_2026-09.md:23; banco_de_dados/eda/fatorial_ampliada/cenarios.csv (n, kmo, var_explicada_2f)
10

## 11 · DM10

[DM10] Demanda 9 — habitação convencional
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:24; docs/prompts/estado_demandas_2026-09.md:28-61; docs/prompts/estado_demandas_2026-09.md:318-324
Fontes: docs/prompts/estado_demandas_2026-09.md:24; docs/prompts/estado_demandas_2026-09.md:46-48, 318-324; banco_de_dados/eda/fatorial_ampliada/cargas.csv (moradia não convencional)
11

## 12 · DM11

[DM11] Demanda 10 — testar lixo
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:25; docs/prompts/estado_demandas_2026-09.md:288-306
Fontes: docs/prompts/estado_demandas_2026-09.md:25; banco_de_dados/eda/fatorial_ampliada/cenarios.csv; docs/prompts/estado_demandas_2026-09.md:301
12

## 13 · DM12

[DM12] Demanda 11 — testar as duas rotações
Requisitos: R2, R3
Textos tirados de: docs/prompts/estado_demandas_2026-09.md:26; docs/prompts/estado_demandas_2026-09.md:28-61; docs/prompts/estado_demandas_2026-09.md:288-306; docs/prompts/estado_demandas_2026-09.md:343-347
Fontes: docs/prompts/estado_demandas_2026-09.md:26; docs/prompts/estado_demandas_2026-09.md:53-55, 302-304, 344-347; banco_de_dados/eda/fatorial_ampliada/pesos.csv (S1)
13

## 14 · DM14

[DM14] Tudo o que contornamos
Requisitos: R3
Fontes: caixas "O que contornamos" de DM02–DM12
14

## 15 · DS00

[DS00] Descritiva dos indicadores
Requisitos: R4, R5
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv
15

## 16 · DS01

[DS01] A base
Requisitos: R6, R10
Fontes: analises_exploratorias/00_referencia/tabelas/T01_funil.csv; F01_funil.png
16

## 17 · DS02

[DS02] Setores com valor, indicador a indicador
Requisitos: R4, R10
Fontes: analises_exploratorias/00_referencia/tabelas/T02_perdas_por_indicador.csv
17

## 18 · DS03

[DS03] Água inadequada
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_agua_inad (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_agua_inad.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 87
18

## 19 · DS03-2

[DS03-2] Água inadequada: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
19

## 20 · DS04

[DS04] Esgoto inadequado
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_esgoto_inad (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_esgoto_inad.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 90
20

## 21 · DS04-2

[DS04-2] Esgoto inadequado: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
21

## 22 · DS05

[DS05] Lixo inadequado
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_lixo_inad (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_lixo_inad.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 93
22

## 23 · DS05-2

[DS05-2] Lixo inadequado: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
23

## 24 · DS06

[DS06] Sem água canalizada
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_sem_agua_canalizada (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_sem_agua_canalizada.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 153
24

## 25 · DS06-2

[DS06-2] Sem água canalizada: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
25

## 26 · DS07

[DS07] Água não chega
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_agua_nao_encanada (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_agua_nao_encanada.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 157
26

## 27 · DS07-2

[DS07-2] Água não chega: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
27

## 28 · DS08

[DS08] Água só no terreno
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_agua_so_terreno (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_agua_so_terreno.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 160
28

## 29 · DS08-2

[DS08-2] Água só no terreno: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
29

## 30 · DS09

[DS09] Sem banheiro
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_sem_banheiro (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_sem_banheiro.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 164
30

## 31 · DS09-2

[DS09-2] Sem banheiro: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
31

## 32 · DS10

[DS10] Sem banheiro nem sanitário
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_sem_banheiro_nem_sanitario (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_sem_banheiro_nem_sanitario.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 167
32

## 33 · DS10-2

[DS10-2] Sem banheiro nem sanitário: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
33

## 34 · DS11

[DS11] Só sanitário
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_so_sanitario (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_so_sanitario.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 170
34

## 35 · DS11-2

[DS11-2] Só sanitário: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
35

## 36 · DS12

[DS12] Banheiro de uso comum
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_banheiro_comum (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_banheiro_comum.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 173
36

## 37 · DS12-2

[DS12-2] Banheiro de uso comum: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
37

## 38 · DS13

[DS13] Banheiro graduado
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: banheiro_graduado (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha banheiro_graduado.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; scripts/ivs_especificacoes.py:58-62; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: scripts/ivs_especificacoes.py, função banheiro_graduado (linha 58)
38

## 39 · DS13-2

[DS13-2] Banheiro graduado: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
39

## 40 · DS14

[DS14] Razão de moradores
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: razao_moradores (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha razao_moradores.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 96
40

## 41 · DS14-2

[DS14-2] Razão de moradores: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
41

## 42 · DS15

[DS15] Analfabetismo 15+
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_analfab (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_analfab.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 99
42

## 43 · DS15-2

[DS15-2] Analfabetismo 15+: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
43

## 44 · DS16

[DS16] Renda média
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: renda_media (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha renda_media.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 102
44

## 45 · DS16-2

[DS16-2] Renda média: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
45

## 46 · DS17

[DS17] Renda sem o extremo
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: renda_media_sem_extremo (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha renda_media_sem_extremo.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; src/ivs_censo/renda.py:113-127; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/renda.py, função renda_sem_extremos (linha 113)
46

## 47 · DS17-2

[DS17-2] Renda sem o extremo: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
47

## 48 · DS18

[DS18] Renda (mediana mun.)
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: renda_media_mediana_mun (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha renda_media_mediana_mun.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; src/ivs_censo/renda.py:130-144; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/renda.py, função renda_imputada_mediana_municipal (linha 130)
48

## 49 · DS18-2

[DS18-2] Renda (mediana mun.): por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
49

## 50 · DS19

[DS19] Cor/raça PPI
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_raca_pretpardind (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_raca_pretpardind.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 105
50

## 51 · DS19-2

[DS19-2] Cor/raça PPI: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
51

## 52 · DS20

[DS20] Responsável mulher
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_resp_feminino (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_resp_feminino.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 176
52

## 53 · DS20-2

[DS20-2] Responsável mulher: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
53

## 54 · DS21

[DS21] Domicílio improvisado
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_dom_improv (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_dom_improv.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 122
54

## 55 · DS21-2

[DS21-2] Domicílio improvisado: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
55

## 56 · DS22

[DS22] Habitação precária
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_hab_precaria (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_hab_precaria.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 124
56

## 57 · DS22-2

[DS22-2] Habitação precária: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
57

## 58 · DS23

[DS23] Moradia convencional
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_moradia_convencional (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_moradia_convencional.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 127
58

## 59 · DS23-2

[DS23-2] Moradia convencional: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
59

## 60 · DS24

[DS24] Moradia não convencional
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_moradia_nao_convencional (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_moradia_nao_convencional.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 130
60

## 61 · DS24-2

[DS24-2] Moradia não convencional: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
61

## 62 · DS25

[DS25] Apartamento
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_apartamento (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_apartamento.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 133
62

## 63 · DS25-2

[DS25-2] Apartamento: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
63

## 64 · DS26

[DS26] Casa
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_casa (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_casa.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 135
64

## 65 · DS26-2

[DS26-2] Casa: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
65

## 66 · DS27

[DS27] Casa de vila/condomínio
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_casa_vila_condominio (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_casa_vila_condominio.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 137
66

## 67 · DS27-2

[DS27-2] Casa de vila/condomínio: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); metade ou mais em zero: % > 0 e média. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
67

## 68 · DS28

[DS28] Crianças 0–4
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_crianca_0a4 (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_crianca_0a4.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 178
68

## 69 · DS28-2

[DS28-2] Crianças 0–4: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
69

## 70 · DS29

[DS29] População 0–14
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_pop_0a14 (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_pop_0a14.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 180
70

## 71 · DS29-2

[DS29-2] População 0–14: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
71

## 72 · DS30

[DS30] Pessoas 60+
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: pct_idoso_60mais (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha pct_idoso_60mais.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 182
72

## 73 · DS30-2

[DS30-2] Pessoas 60+: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
73

## 74 · DS31

[DS31] Índice de envelhecimento
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: iep_setor (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha iep_setor.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 185
74

## 75 · DS31-2

[DS31-2] Índice de envelhecimento: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
75

## 76 · DS32

[DS32] Dependência idosa
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: rdi_setor (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha rdi_setor.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 188
76

## 77 · DS32-2

[DS32-2] Dependência idosa: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
77

## 78 · DS33

[DS33] 70+ entre 60+
Requisitos: R4, R5, R6, R10
Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: prop_70mais_entre_60mais (tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). Conferir: T03 e T02 da 00_referencia, linha prop_70mais_entre_60mais.
Fontes: analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv; T02_perdas_por_indicador.csv; banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv; Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores
Calculado em: src/ivs_censo/indicadores.py, linha 191
78

## 79 · DS33-2

[DS33-2] 70+ entre 60+: por região, município e FCU
Requisitos: R4, C-04
Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); mediana. Números de T04, T05, T15 e, para FCU com zeros, da base da 00_referencia.
Fontes: analises_exploratorias/00_referencia/tabelas/T04_descritivas_regiao.csv; analises_exploratorias/00_referencia/tabelas/T05_descritivas_municipio.csv; analises_exploratorias/00_referencia/tabelas/T15_fcu_por_indicador.csv
79

## 80 · DC00

[DC00] Correlações entre os indicadores
Requisitos: C-04
Fontes: analises_exploratorias/00_referencia/tabelas/T12_correlacao_spearman.csv
80

## 81 · DC01

[DC01] Os componentes do IVS-7
Requisitos: C-04
Fontes: analises_exploratorias/00_referencia/tabelas/T12_correlacao_spearman.csv
81

## 82 · DC02

[DC02] Os componentes do IVS-7: mapa
Requisitos: C-04
Fontes: analises_exploratorias/00_referencia/tabelas/T12_correlacao_spearman.csv
82

## 83 · DC03

[DC03] Saneamento
Requisitos: C-04
Fontes: analises_exploratorias/00_referencia/tabelas/T12_correlacao_spearman.csv
83

## 84 · DC04

[DC04] Socioeconômica
Requisitos: C-04
Fontes: analises_exploratorias/00_referencia/tabelas/T12_correlacao_spearman.csv
84

## 85 · DC05

[DC05] Morfologia
Requisitos: C-04
Fontes: analises_exploratorias/00_referencia/tabelas/T12_correlacao_spearman.csv
85

## 86 · DC06

[DC06] Demografia
Requisitos: C-04
Fontes: analises_exploratorias/00_referencia/tabelas/T12_correlacao_spearman.csv
86

## 87 · DC07

[DC07] Os 31 indicadores
Requisitos: C-04
Fontes: analises_exploratorias/00_referencia/tabelas/T12_correlacao_spearman.csv
87

## 88 · FA00

[FA00] Descritiva da análise fatorial
Requisitos: R7
Fontes: banco_de_dados/eda/ivs_especificacoes/referencia.csv (leitura principal)
88

## 89 · FA01

[FA01] A amostra da fatorial
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T01_funil.csv; analises_exploratorias/00_referencia/tabelas/T02_perdas_por_indicador.csv; analises_exploratorias/00_referencia/tabelas/T20_variaveis_cargas.csv (variáveis)
89

## 90 · FA02

[FA02] A matriz de correlação de entrada
Requisitos: R7
Recalculada por fa02() com matriz_correlacao(X, "spearman") de src/ivs_censo/fatorial.py:394, na base de montar_base(00_referencia) com os sete componentes completos.
Fontes: src/ivs_censo/fatorial.py:394-400 (matriz_correlacao) e 579-594 (rodar_cenario); base: Base_ELSI_70Municipios_Censo2022.db, recorte da 00_referencia
90

## 91 · FA03

[FA03] Adequação dos dados à fatorial
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T19_adequacao_fatorial.csv
91

## 92 · FA04

[FA04] MSA e comunalidade por variável
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T20_variaveis_cargas.csv (msa, comunalidade, comunalidade_obliqua)
92

## 93 · FA05

[FA05] Autovalores e análise paralela de Horn
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T21_autovalores.csv; F22_sedimentacao_horn.png
93

## 94 · FA06

[FA06] Quantos fatores
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T19_adequacao_fatorial.csv; analises_exploratorias/00_referencia/tabelas/T23_pesos.csv (dimensões)
94

## 95 · FA07

[FA07] Cargas sem rotação
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T20_variaveis_cargas.csv (sem_rotacao_f1, sem_rotacao_f2)
95

## 96 · FA08

[FA08] Cargas Varimax
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T20_variaveis_cargas.csv (varimax_f1, varimax_f2)
96

## 97 · FA09

[FA09] Cargas promax: matriz padrão e matriz estrutura
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T20_variaveis_cargas.csv (promax_*); F23_mapa_cargas.png
97

## 98 · FA10

[FA10] Correlação entre os fatores (Φ)
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T22_phi.csv
98

## 99 · FA11

[FA11] Os pesos do índice
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T23_pesos.csv
99

## 100 · FA12

[FA12] O índice da referência proposta
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T24_indice_descritivas.csv (Total); F24_histograma_por_faixa.png
100

## 101 · FA13

[FA13] As faixas, pelas duas regras
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T25_faixas.csv
101

## 102 · FA14

[FA14] Validação contra as favelas (FCU)
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T26_auc_e_elegibilidade.csv; F25_curva_roc.png
102

## 103 · FA15

[FA15] AUC por município
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T27_auc_por_municipio.csv; analises_exploratorias/00_referencia/tabelas/T26_auc_e_elegibilidade.csv
103

## 104 · FA16

[FA16] Elegibilidade pelos critérios do NB05
Requisitos: R7
Fontes: analises_exploratorias/00_referencia/tabelas/T26_auc_e_elegibilidade.csv
104

## 105 · FP00

[FP00] O que a orientadora pediu da fatorial
Requisitos: R8
Fontes: docs/prompts/estado_demandas_2026-09.md:16-26
105

## 106 · FC01

[FC01] Cenário S0: IVS-7 (referência, reproduz o NB04)
Requisitos: C-04
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; scripts/fatorial_ampliada.py (CENARIOS, carregar, montar)
106

## 107 · FC02

[FC02] Cenário S1: IVS-6 (IVS-7 sem lixo)
Requisitos: C-04
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; scripts/fatorial_ampliada.py (CENARIOS, carregar, montar)
107

## 108 · FC03

[FC03] Cenário S2: IVS-7 + não chega
Requisitos: C-04
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; scripts/fatorial_ampliada.py (CENARIOS, carregar, montar)
108

## 109 · FC04

[FC04] Cenário S3: IVS-7 + sem canalização
Requisitos: C-04
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; scripts/fatorial_ampliada.py (CENARIOS, carregar, montar)
109

## 110 · FC05

[FC05] Cenário S4: IVS-7 + sem banheiro (V00495)
Requisitos: C-04
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; scripts/fatorial_ampliada.py (CENARIOS, carregar, montar)
110

## 111 · FC06

[FC06] Cenário S5: IVS-7 + não convencional
Requisitos: C-04
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; scripts/fatorial_ampliada.py (CENARIOS, carregar, montar)
111

## 112 · FC07

[FC07] Cenário S6: IVS-7 + as quatro ("tudo isso")
Requisitos: C-04
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; scripts/fatorial_ampliada.py (CENARIOS, carregar, montar)
112

## 113 · FC08

[FC08] Cenário S7: S6 sem lixo
Requisitos: C-04
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; scripts/fatorial_ampliada.py (CENARIOS, carregar, montar)
113

## 114 · FC09

[FC09] As variantes dos cenários
Requisitos: C-04
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv
114

## 115 · FP01

[FP01] Demanda 1 — o efeito das três rendas na fatorial
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; banco_de_dados/eda/fatorial_ampliada/pesos.csv (varimax)
115

## 116 · FP02

[FP02] Demanda 3 — sem bootstrap, sem e com rotação
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/cargas.csv (S0)
116

## 117 · FP03

[FP03] Demanda 5 — o perfil dos setores com e sem "água não chega"
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/comparacao_nao_chega_banheiro.csv (bloco perfil_mediana)
117

## 118 · FP04

[FP04] Demanda 6 — o "sem banheiro" na fatorial
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; banco_de_dados/eda/ivs_especificacoes/especificacoes.csv (banheiro, elegivel)
118

## 119 · FP05

[FP05] Demanda 7 — canalização e sem banheiro, uma por vez
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv
119

## 120 · FP06

[FP06] Demanda 8 — tudo isso junto
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv; docs/prompts/estado_demandas_2026-09.md:298-299
120

## 121 · FP07

[FP07] Demanda 9 — a moradia não convencional
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv
121

## 122 · FP08

[FP08] Demanda 10 — testar o lixo
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/cenarios.csv (colunas n, kmo, fatores_kaiser, fatores_horn, var_explicada_2f, lixo_fator_proprio_varimax); docs/prompts/estado_demandas_2026-09.md:25
122

## 123 · FP09

[FP09] Demanda 11 — as duas rotações
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/pesos.csv (S0, S1, S6)
123

## 124 · FP11

[FP11] Validação contra FCU, cenário a cenário
Requisitos: R8
Fontes: banco_de_dados/eda/fatorial_ampliada/validacao_fcu.csv
124

## 125 · FP13

[FP13] A renda sozinha contra o índice
Requisitos: R8
Fontes: banco_de_dados/eda/ivs_especificacoes/acrescimo_renda.csv
125

## 126 · VP00

[VP00] As 108 versões da análise fatorial
Fontes: banco_de_dados/eda/versoes_fatorial/versoes.csv
126

## 127 · VP02

[VP02] Como ler
Fontes: versoes_fatorial/INTERPRETACAO.md
127

## 128 · VP03

[VP03] Os cinco eixos
Fontes: versoes_fatorial/VERSOES.md
128

## 129 · VP04

[VP04] A amostra
Fontes: banco_de_dados/eda/versoes_fatorial/versoes.csv (n, n_comum)
129

## 130 · VP05

[VP05] As 108 de uma vez: quem passa nos critérios
Fontes: banco_de_dados/eda/versoes_fatorial/versoes.csv (elegivel, criterio_que_falhou)
130

## 131 · VP06

[VP06] As 108 de uma vez: KMO
Fontes: banco_de_dados/eda/versoes_fatorial/versoes.csv (kmo)
131

## 132 · VP07

[VP07] As 108 de uma vez: AUC no município
Fontes: banco_de_dados/eda/versoes_fatorial/versoes.csv (auc_mun_comum)
132

## 133 · VP08

[VP08] Um eixo por vez: renda
Fontes: banco_de_dados/eda/versoes_fatorial/pares_por_eixo.csv; banco_de_dados/eda/versoes_fatorial/pares_detalhe.csv
133

## 134 · VP09

[VP09] Um eixo por vez: lixo
Fontes: banco_de_dados/eda/versoes_fatorial/pares_por_eixo.csv; banco_de_dados/eda/versoes_fatorial/pares_detalhe.csv
134

## 135 · VP10

[VP10] Um eixo por vez: água canalizada
Fontes: banco_de_dados/eda/versoes_fatorial/pares_por_eixo.csv; banco_de_dados/eda/versoes_fatorial/pares_detalhe.csv
135

## 136 · VP11

[VP11] Um eixo por vez: banheiro
Fontes: banco_de_dados/eda/versoes_fatorial/pares_por_eixo.csv; banco_de_dados/eda/versoes_fatorial/pares_detalhe.csv
136

## 137 · VP12

[VP12] Um eixo por vez: moradia
Fontes: banco_de_dados/eda/versoes_fatorial/pares_por_eixo.csv; banco_de_dados/eda/versoes_fatorial/pares_detalhe.csv
137

## 138 · VP13

[VP13] As versões que passam nos critérios
Fontes: banco_de_dados/eda/versoes_fatorial/versoes.csv (elegivel)
138

## 139 · VP13-2

[VP13-2] As versões que passam nos critérios (2)
Fontes: banco_de_dados/eda/versoes_fatorial/versoes.csv (elegivel)
139

## 140 · VP14

[VP14] A ordem das elegíveis pelos critérios do NB05
Fontes: banco_de_dados/eda/versoes_fatorial/versoes.csv; banco_de_dados/eda/versoes_fatorial/estabilidade.csv; scripts/ivs_especificacoes.py:ordenar
140
