# Levantamento das análises exploratórias possíveis

Outubro de 2026. Depois da grade do NB05, o projeto passou a poder produzir o IVS em
**muitas versões**: com ou sem certos dados, com indicadores diferentes e com índices novos
ao lado do IVS. Este documento lista o que é possível explorar, com o que já existe no
repositório e o que faltaria. **Não escolhe nada**: a última seção reúne as decisões que
são da orientadora.

Legenda de viabilidade:
- 🟢 os dados e o código já estão no repositório;
- 🟡 os dados estão no repositório, mas falta código;
- 🔴 precisa de dado novo (baixar ou pedir acesso).

---

## 1. O ponto de partida

| O que já existe | Onde |
|---|---|
| 7 indicadores do IVS e cerca de 20 complementares, por setor, nos 70 municípios | `src/ivs_censo/indicadores.py`, `banco_de_dados/entrega_orientadora/` |
| Os mesmos indicadores para os ~468 mil setores do Brasil | `banco_de_dados/nacional/` (`scripts/proporcoes_brasil.py`) |
| Três tratamentos da renda (original, sem extremo, mediana municipal) | `src/ivs_censo/renda.py`, `banco_de_dados/eda/renda_*` |
| Grade de 324 especificações do IVS, com elegibilidade, estabilidade e AUC contra FCU | `banco_de_dados/eda/ivs_especificacoes/` |
| Classificação Favela e Comunidade Urbana (FCU) por setor | base ELSI (`CD_FCU`) |
| Indicadores de envelhecimento (IEP, RDI, proporção de 70+ entre os 60+) | `indicadores.py`, Galvão et al. (2025) |
| Malha geográfica dos setores | **não existe** — só o dicionário dela |

A grade atual cruza sete dimensões: renda (3) × lixo (2) × banheiro (3) × rotação e pesos (9)
× normalização (2), e cada uma das 324 versões é classificada por duas regras de faixa.

---

## 2. Os quatro eixos em que uma versão pode variar

### A. Que setores entram (a base)

| Alternativa | O que muda | Viab. |
|---|---|---|
| Só urbanos (atual) × urbanos e rurais | Os rurais têm saneamento muito pior e podem dominar o fator de saneamento | 🟡 |
| Só `Dados_sig = OK` (atual) × incluir sigilosos com imputação | Recupera setores pequenos, mas inventa dado | 🟡 |
| Piso de população por setor (ex.: ≥ 50 moradores) | Tira setores com proporções instáveis | 🟡 |
| Com × sem o extremo de renda de BH | Já medido para a renda; não para o índice inteiro | 🟢 |
| 70 municípios ELSI × Brasil inteiro × uma região | A estrutura fatorial é a mesma fora do ELSI? | 🟡 (indicadores prontos; fatorial não rodada) |
| Por porte do município ou por região | A estrutura muda entre capitais e municípios pequenos? | 🟡 |

### B. Que indicadores entram

| Alternativa | Situação |
|---|---|
| Renda: 3 tratamentos | 🟢 na grade |
| Lixo: com × sem | 🟢 na grade |
| Banheiro: fora × V00495 × graduado | 🟢 na grade |
| Água: inadequada (atual) × sem água canalizada × só no terreno | 🟡 indicadores calculados, fora da grade |
| Esgoto: definição com 312 × 249 setores divergentes | 🟡 diagnóstico feito (`diagnostico_esgoto_312_vs_249.csv`) |
| Moradia: razão moradores × domicílio improvisado × habitação precária | 🟡 calculados, fora da grade |
| Raça/cor (pretos, pardos e indígenas): dentro × fora do índice | 🟡 |
| Responsável mulher, crianças de 0 a 4 anos | 🟡 calculados, nunca testados no índice |
| Envelhecimento (IEP, RDI, 60+): como terceira dimensão | 🟡 calculados; ver índice D2 |

### C. Como o índice é construído

| Etapa | Alternativas possíveis | Na grade? |
|---|---|---|
| Extração | eixo principal (atual) × máxima verossimilhança × componentes principais | não |
| Nº de fatores | 1 × 2 (atual) × o que a análise paralela de Horn indicar | parcial |
| Rotação | nenhuma × Varimax × promax | sim |
| Pesos | carga², comunalidades, 50/50, 60/40 × **pesos iguais** × média de postos | parcial |
| Normalização | min-max municipal × min-max global × **escore z** × **percentis** | parcial |
| Agregação | soma ponderada (atual) × **média geométrica** (o manual da OCDE trata disso) | não |
| Faixas | regra do IVS-BH × quartis × **quintis** × **quebras naturais (Jenks)** × agrupamento (k-means) | parcial |

### D. Índices novos, ao lado do IVS

| Índice | Ideia | Viab. |
|---|---|---|
| D1. Subíndices | Socioeconômico e saneamento separados, para ver qual dimensão puxa a vulnerabilidade | 🟡 |
| D2. IVS-Idoso | IVS com uma dimensão demográfica (IEP, RDI, 60+), coerente com o ELSI | 🟡 (precisa decisão conceitual) |
| D3. Índice de moradia | Habitação precária, improvisado, tipo de moradia e razão de moradores | 🟡 |
| D4. Réplica aproximada do IBP | O Índice Brasileiro de Privação (Allik et al., 2020) refeito com o Censo 2022, para comparar | 🟡 (conferir se as três variáveis existem nos agregados de 2022) |
| D5. Índice "orientado por conhecimento" × "orientado por dados" | Pesos de especialistas × pesos da fatorial, como em Gioia et al. (2020) | 🟢 os dois polos já existem (60/40 e SS) |
| D6. Pesos iguais / média de postos | Índice mais simples, sem fatorial; serve de linha de base | 🟢 (já entra no item 6 do NB05) |

---

## 3. As análises exploratórias, uma a uma

Cada análise pode rodar sobre **qualquer versão** dos eixos A–D.

| # | Análise | Pergunta que responde | Viab. |
|---|---|---|---|
| E1 | Descritivas por versão (distribuição, assimetria, extremos) | Como cada versão espalha os setores? | 🟢 |
| E2 | Correlação entre versões (Spearman entre os índices) | As versões ordenam os setores do mesmo jeito? | 🟢 parcial no NB05 |
| E3 | Concordância de faixas entre versões (kappa, % que muda de faixa) | Quantos setores mudam de risco conforme a escolha? | 🟢 parcial |
| E4 | Validade contra FCU (AUC global e municipal) | A versão separa favela de não favela? | 🟢 |
| E5 | O que o índice acrescenta à renda | Vale a pena um índice ou basta a renda? | 🟢 feito no NB05 |
| E6 | Análise de incerteza (sorteio de versões, estilo Monte Carlo) | Para cada setor, em quantas versões ele cai em risco elevado? | 🟡 |
| E7 | Estabilidade (um município de fora; bootstrap de setores) | Os pesos dependem de poucos municípios? | 🟢 só o primeiro |
| E8 | Desigualdade dentro do município (P90/P10, Gini/Theil do IVS) | Quais cidades são mais desiguais por dentro? | 🟡 |
| E9 | População em risco (pessoas, e pessoas de 60+, por faixa) | Quantos idosos vivem em setores de risco elevado? | 🟡 (dados prontos) |
| E10 | IVS × envelhecimento (IEP, RDI) | Os setores mais velhos são os mais ou os menos vulneráveis? | 🟡 |
| E11 | Tipologias (agrupamento de setores ou de municípios) | Há perfis de vulnerabilidade, além de um eixo só? | 🟡 |
| E12 | ELSI × Brasil (representatividade do recorte) | Os 70 municípios se parecem com o Brasil urbano? | 🟢 (`comparativo_brasil_vs_elsi.csv`) |
| E13 | Autocorrelação espacial (Moran global e LISA) e mapas | A vulnerabilidade forma manchas? Onde? | 🔴 precisa da malha de setores do IBGE |
| E14 | Comparação com o IVS-BH 2012 em Belo Horizonte | O índice mudou de lugar entre 2010 e 2022? | 🔴 precisa compatibilizar setores 2010 × 2022 |
| E15 | Validade com desfechos de saúde | O índice prevê algo de saúde? | 🔴 dados por município (DataSUS) ou do ELSI individual, com autorização |

---

## 4. O cuidado com o número de versões

A grade atual já tem 324 especificações. Cada eixo novo multiplica esse número: só a água (3)
e a normalização por escore z e percentis (+2) levariam a grade a cerca de 1.900 versões (162 × 4 × 3).
Isso traz três riscos:

1. **Escolher a versão pelo resultado.** Com muitas versões, alguma sempre parece melhor
   por acaso. O NB05 evitou isso fixando os critérios antes de rodar (ver o README de
   `banco_de_dados/eda/ivs_especificacoes/`); qualquer ampliação precisa do mesmo cuidado.
2. **Amostras diferentes.** Versões com indicadores diferentes perdem setores diferentes.
   A comparação justa é na amostra comum, como o NB05 já faz.
3. **Custo de leitura.** Ninguém lê 1.900 linhas. As análises E2, E3 e E6 resumem a grade
   inteira em poucas figuras e são as que escalam.

Duas formas de controlar, para a orientadora escolher:

- **Um eixo por vez**: partir da referência proposta e variar só um eixo, mantendo os
  outros fixos. Barato e fácil de explicar.
- **Grade completa com resumo**: rodar tudo e reportar só E2, E3 e E6. Mais completo, mais
  caro, e exige critérios fixados antes.

---

## 5. Decisões que são da orientadora

1. Quais eixos (A–D) entram nesta rodada, e quais ficam para depois.
2. Se o IVS-Idoso (D2) faz sentido como produto à parte ou como dimensão do IVS.
3. Se o recorte continua só nos 70 municípios ou se o Brasil entra como comparação.
4. Se vale baixar a malha de setores do IBGE para a análise espacial e os mapas (E13),
   que já estão no cronograma como pendentes.
5. Um eixo por vez ou grade completa com resumo (seção 4).
6. Quais critérios fixar **antes** de rodar as versões novas.
