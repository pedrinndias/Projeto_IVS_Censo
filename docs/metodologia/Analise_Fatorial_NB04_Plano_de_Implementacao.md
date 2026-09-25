# Plano de implementação do Notebook 04

## Análise fatorial, estrutura latente e definição dos pesos do IVS

**Projeto:** Índice de Vulnerabilidade à Saúde (IVS) intraurbano — Censo Demográfico 2022 / ELSI-Brasil
**Instituição:** Fiocruz Minas — Instituto René Rachou (IRR) · Iniciação Científica
**Pesquisador:** Pedro Dias Soares
**Data:** 16 de setembro de 2026
**Base metodológica:** MATOS & RODRIGUES, *Análise fatorial* (Enap, 2019) · FIGUEIREDO & SILVA (2010)

> **Documentos irmãos:** [`Analise_Fatorial_Enap2019_Guia_de_Leitura.md`](Analise_Fatorial_Enap2019_Guia_de_Leitura.md) (o estudo do livro) e [`Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md`](Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md) (a análise já rodada).
>
> **Versão em PDF:** [`Implementacao_Fatorial_NB04_Brainstorm_e_Prompt.pdf`](Implementacao_Fatorial_NB04_Brainstorm_e_Prompt.pdf).

---

## 0. O ponto de partida

O Notebook 04 **não é uma análise fatorial nova**. É a consolidação da que existe, acrescida das extensões que a leitura do livro da Enap tornou necessárias, e da decisão sobre os pesos. Tratá-lo como implementação do zero é a forma mais rápida de perder duas semanas e chegar aos mesmos números.

### Inventário de reuso

| Ativo | O que já resolve |
|---|---|
| `scripts/diagnostico_fatorial.py` | 219 linhas em numpy puro, sem dependência nova: KMO e MSA por matriz anti-imagem, Bartlett com cauda por Wilson–Hilferty, autovalores, análise paralela de Horn, ACP e rotação Varimax. Roda seis cenários e grava CSVs. **É a base, não um rascunho a descartar.** |
| `banco_de_dados/eda/fatorial/` | 19 CSVs com os seis cenários calculados, incluindo `resumo_adequabilidade.csv`. Referência de conferência para qualquer reimplementação. |
| `banco_de_dados/entrega_orientadora/*.db` | SQLite **versionado**, tabela `setores_censitarios`, 109.032 linhas × 105 colunas, as 7 variáveis já calculadas. O NB04 roda sem os 2,4 GB de dados brutos do Censo. |
| `src/ivs_censo/indicadores.py` | Definição canônica dos indicadores (`INDICADORES_IVS` × `INDICADORES_COMPLEMENTARES`). O NB04 importa daqui — nunca redefine fórmulas. |
| `docs/Analise_Fatorial_Figueiredo2010_...md` | Interpretação dos seis cenários, diagnóstico do lixo, convergência 65/35 × 60/40, e o checklist de 15 passos. Os itens 13, 14 e 15 são o escopo do NB04. |

### Os números que já estão na mesa

| Cenário | n | KMO | MSA mín | \|r\|≥0,30 | Fatores (Kaiser) | Var. acum. | Comun. mín |
|---|---:|---:|---:|---:|---:|---:|---:|
| 7 vars, Spearman | 87.545 | 0,783 | 0,700 | 57,1% | 2 | 62,1% | 0,253 |
| 7 vars, Pearson | 87.545 | 0,732 | 0,542 | 33,3% | 3 | 53,6% | 0,327 |
| **6 vars, sem lixo** | 87.545 | **0,787** | 0,715 | **80,0%** | **1** | **70,0%** | 0,380 |
| 6 vars, sem analfab. | 104.093 | 0,707 | 0,603 | 53,3% | 2 | 63,8% | 0,328 |
| 7 vars, min-max municipal | 87.241 | 0,720 | 0,624 | 42,9% | 3 | 56,5% | 0,091 |

Bartlett em todos: p ≈ 0 (χ² = 235.084, gl 21, no cenário principal). Pesos empíricos sem lixo: **65% socioeconômica / 35% saneamento**, contra ~60/40 da literatura (IVS-BH 2012).

---

## 1. Inventário de ideias

Veredito: **ENTRA** no NB04, **DEPOIS** (NB05 ou geoprocessamento), ou **FORA** do escopo. Custo em horas de trabalho efetivo, pressupondo o reuso do `diagnostico_fatorial.py`.

### Família A — Extensões do método

Decorrem das cinco revisões apontadas pelo estudo do livro. São o núcleo do NB04.

| # | Ideia | O que responde | Custo | Veredito | Observação |
|---|---|---|---:|---|---|
| **A1** | Rotação oblíqua (`promax`) | Os dois fatores são correlacionados? Quanto? A repartição 65/35 sobrevive? | 3–4 h | **ENTRA** | Prioridade máxima. `promax` é Varimax seguido de transformação oblíqua por mínimos quadrados — reaproveita o código existente. Produz a matriz de correlação entre fatores, que hoje não existe. Livro p. 38. |
| **A2** | Fatoração do eixo principal | ACP e AF divergem, como a regra de Stevens sugere? | 2–3 h | **ENTRA** | É ACP iterada com comunalidades na diagonal. Se as cargas baterem com a ACP, uma frase encerra a questão no artigo. Livro p. 27. |
| **A3** | Escores pelo método da regressão | O índice 0–1 ordena os setores como o escore refinado ordenaria? | 2 h | **ENTRA** | `B = R⁻¹A` — três linhas de numpy. O produto é a correlação de Spearman entre os rankings: acima de ~0,95 valida o índice 0–1. Livro p. 24–25. |
| **A4** | SMC e diagnóstico de multicolinearidade | Renda × cor/raça a −0,811 compromete a separação dos pesos? | 1 h | **ENTRA** | SMC é `1 − 1/diag(R⁻¹)`. Barato e responde a objeção previsível de parecerista. Livro p. 42. |
| **A5** | Bootstrap das cargas | Os pesos são estáveis, ou dependem da amostra? | 3 h | **ENTRA** | **Não está em nenhuma das duas referências** — acréscimo do projeto, e precisa ser declarado como tal. É a resposta direta à crítica de instabilidade que o livro faz aos métodos não refinados (p. 23). Com 87 mil setores, 1.000 reamostragens rodam em minutos. Maior ganho de credibilidade por hora investida. |

### Família B — Decisões de composição

O NB04 deve produzir a **evidência**, não necessariamente a decisão — três delas são da orientadora.

| # | Ideia | O que responde | Custo | Veredito | Observação |
|---|---|---|---:|---|---|
| **B1** | Ordem NB03 ↔ NB04 | Fatorar antes ou depois da normalização municipal? | 0 h | **ENTRA** | Já medido: normalizar antes derruba o KMO de 0,783 para 0,720 e muda os pesos de 65/35 para 56/44. A recomendação (fatorar sobre brutos) só precisa virar decisão registrada no GUIA §6.2. |
| **B2** | Um fator ou dois | Manter as duas dimensões do IVS-BH ou aceitar a solução unifatorial? | 1 h | **ENTRA** | Kaiser e Horn apontam **um** fator sem o lixo. Calcular o índice nas duas versões e comparar as classificações em 4 faixas dá à orientadora o custo concreto da escolha. **A métrica é quantos setores mudam de faixa**, não variância explicada. |
| **B3** | Transformar variáveis antes de fatorar | Log, posto ou winsorização resolvem a assimetria melhor que Spearman? | 4 h | DEPOIS | Usar Spearman *é* uma padronização por posto embutida; fazer as duas coisas é redundante. Tratar no NB03. Relatório da EDA §13. |
| **B4** | Política do sigilo no analfabetismo | Os 16.563 setores perdidos enviesam a solução? | 2 h | **ENTRA** | Parcialmente medido: a *estrutura* não muda. Falta comparar as cargas nos dois conjuntos e reportar o índice com e sem imputação. O livro não oferece nada sobre faltantes — lacuna a declarar. |

### Família C — Validação

| # | Ideia | O que responde | Custo | Veredito | Observação |
|---|---|---|---:|---|---|
| **C1** | Validação externa contra setores de favela | O IVS separa os 19.452 setores de FCU dos demais? | 2 h | **ENTRA** | **A validação mais forte disponível ao projeto.** `CD_TIPO = 1` é marcador independente, oficial, com 100% de concordância já verificada. Curva ROC e diferença de medianas valem mais que qualquer estatística interna à fatorial — testa se o índice mede algo *real*, não se é internamente coerente. |
| **C2** | Sensibilidade dos pesos | A classificação muda se os pesos forem 60/40 em vez de 65/35? | 2 h | **ENTRA** | Tabela de contingência entre as classificações. Se a concordância for alta, a decisão nº 1 do GUIA deixa de ser crítica — e isso é resultado publicável. |
| **C3** | Estabilidade por subamostra | A estrutura se mantém entre municípios e regiões? | 3 h | DEPOIS | 14 dos 70 municípios perdem mais da metade dos setores no recorte urbano — instabilidade encontrada pode ser de amostra, não de estrutura. Melhor depois do piso mínimo definido. |
| **C4** | I de Moran dos escores | Qual o tamanho da dependência espacial que a fatorial ignora? | — | DEPOIS | Depende da malha de setores (geoprocessamento). Registrar como limitação declarada no NB04. |

### Família D — Engenharia

| # | Questão | Opções | Veredito | Observação |
|---|---|---|---|---|
| **D1** | Dependências | numpy puro × `factor_analyzer` + `scipy` | **numpy** | O `requirements.txt` tem cinco pacotes e o script existente foi escrito para não crescer essa lista. Promax, eixo principal, escores por regressão, SMC e bootstrap são álgebra linear que o numpy já faz. |
| **D2** | Onde mora o código | Notebook × módulo em `src/` × script | **módulo + notebook** | A matemática vai para `src/ivs_censo/fatorial.py`, com testes em `tests/`; o notebook chama, interpreta e produz figuras. É a correção já feita no NB02 em 20/08/2026. |
| **D3** | Figuras | Scree plot, mapa de cargas, diagrama de fatores | **ENTRA** | Matplotlib puro, paleta do projeto, dpi 150, em `banco_de_dados/eda/fatorial/figuras/`. O scree plot com a linha de Horn sobreposta é a figura do artigo. |

---

## 2. Arquitetura recomendada

Onze itens entram: A1–A5, B1, B2, B4, C1, C2 e D3, sobre a estrutura de D1 e D2. Estimativa: **20 a 26 horas** de trabalho efetivo. A ordem importa — cada bloco consome o anterior.

| § | Bloco | O que faz | Saída |
|---:|---|---|---|
| 1 | **Carga e recorte** | Lê o `.db` da entrega, aplica `urbano = 1 AND Dados_sig = 'OK'`, importa indicadores de `src/ivs_censo`, inverte a renda. Confere 104.108 setores e 87.545 completos. | Conferência impressa |
| 2 | **Adequabilidade** | Matriz de correlação, KMO, MSA, Bartlett + **SMC** (A4). **Trava:** tem de reproduzir `resumo_adequabilidade.csv` exatamente. | `nb04_adequabilidade.csv` |
| 3 | **Número de fatores** | Autovalores, Kaiser, Horn, variância acumulada + **scree plot** (D3). Registra que Kaiser retém 1 fator sem o lixo e que o 2º se sustenta na teoria. | `scree_horn.png` |
| 4 | **Extração comparada** | ACP e **eixo principal** (A2), lado a lado, com a maior diferença absoluta entre cargas. | `nb04_extracao_comparada.csv` |
| 5 | **Rotação comparada** | Varimax e **promax** (A1). Publica a **matriz de correlação entre fatores** e recalcula a repartição dos pesos na solução oblíqua. Verifica cargas > 1 e, se houver, a variância residual. | `nb04_cargas_{varimax,promax}.csv` |
| 6 | **Estabilidade** | **Bootstrap** de 1.000 reamostragens (A5): IC 95% para cada carga e para a repartição entre dimensões. | `nb04_bootstrap_cargas.csv` |
| 7 | **Pesos e escores** | Fixa os pesos. Calcula as **duas versões**: índice 0–1 por média ponderada e **escore por regressão** (A3). Reporta Spearman entre os rankings. | `nb04_pesos.csv` · escores |
| 8 | **Cenários de decisão** | Índice sob: 1 × 2 fatores (B2); pesos empíricos × 60/40 (C2); com e sem sigilo (B4). Tabelas de contingência entre as classificações em 4 faixas. | `nb04_cenarios.csv` |
| 9 | **Validação externa** | **Separação dos setores de FCU** (C1): distribuição, diferença de medianas, curva ROC. | `nb04_validacao_fcu.{csv,png}` |
| 10 | **Síntese e decisões** | Tabela final de pesos; o que fica decidido; o que vai para a orientadora; limitações declaradas. | Seção do relatório |

### O que não fazer

- **Não recalcular os indicadores.** Vêm de `src/ivs_censo/indicadores.py`; redefini-los no notebook recria a dívida que o NB02 levou meses para pagar.
- **Não decidir o que é da orientadora.** Destino do lixo, número de fatores e política do sigilo são decisões dela. O notebook produz a evidência e o custo de cada opção.
- **Não adicionar dependências** sem necessidade demonstrada.
- **Não calcular o IVS final.** Isso é o Notebook 05, depois da normalização municipal do NB03. Aqui o produto são os **pesos** e a estrutura.

---

## 3. Resultados esperados

Previsões deste documento, não medições. Servem para calibrar a leitura — se der diferente, é informação.

| Bloco | Esperado | Se der diferente |
|---|---|---|
| Extração comparada (§4) | Cargas próximas, com diferenças maiores nas variáveis de comunalidade baixa (água, razão de moradores) | Divergência > 0,10 em variável de comunalidade alta indica erro de implementação, não achado |
| Rotação (§5) | Correlação entre fatores entre 0,30 e 0,55, positiva. Pesos deslocando de 65/35 na direção de 60/40 | **Correlação > 0,70** sugere que a solução de dois fatores não se sustenta e reabre B2 com força |
| Bootstrap (§6) | Intervalos estreitos; peso de cada dimensão variando menos de 3 pontos percentuais | Intervalos largos seriam achado importante e mudariam a conversa sobre pesos |
| Escores (§7) | Spearman > 0,97 entre o índice 0–1 e o escore refinado | **Abaixo de 0,90** obrigaria a adotar o escore refinado como oficial, com custo de interpretabilidade |
| Validação FCU (§9) | Separação nítida; AUC > 0,75 | **Abaixo de 0,65** seria problema sério de validade, a enfrentar antes de qualquer mapa |

**Critério de sucesso.** O NB04 cumpriu seu papel quando for possível responder, com um número e a referência que o sustenta: **quais são os pesos do IVS e por quê**; **quão sensível é a classificação a essa escolha**; e **o índice separa os territórios que sabidamente são vulneráveis**. Tudo o mais é instrumentação.

---

## 4. A objeção de fundo — reflexivo × formativo

> **Procedência.** Esta seção vem de um parecer isolado, produzido numa rodada de *pressure-test* (`/council`) **interrompida com 1 de 5 conselheiros concluídos**. Não é consenso, não foi revisada por pares, não foi confrontada com a literatura. Está registrada porque a objeção é séria — **não porque esteja decidida**.

A análise fatorial pressupõe modelo **reflexivo**: o construto latente *causa* os indicadores. O IVS pode ser **formativo**: esgoto inadequado não é causado pela vulnerabilidade, é parte constituinte dela.

Se for formativo: remover uma variável muda a definição do construto; as cargas não são pesos legítimos; a correlação de −0,811 entre renda e cor/raça deixa de ser redundância a declarar e vira duas dimensões substantivas a manter; e o lixo com fator próprio deixa de ser anomalia a excluir — excluí-lo seria deixar a matriz de correlação decidir a política pública.

A consequência seria reenquadrar o NB04: fatorial como **diagnóstico de redundância**, não motor de ponderação, com os pesos 60/40 vindos da teoria e defendidos como escolha normativa explícita.

**Encaminhamento:** levar à orientadora como questão aberta, buscar Diamantopoulos & Winklhofer (2001) e o capítulo de ponderação de Nardo et al. (2008). **Não decidir com base num único parecer não revisado.** O NB04 pode e deve rodar enquanto isso — os diagnósticos (adequabilidade, estrutura, redundância, validação externa) são úteis sob qualquer das duas leituras. O que fica condicionado é apenas o uso das cargas **como pesos**.

---

## 5. Prioridade

Se só der para fazer três coisas:

1. **C1 — validação externa contra os setores de FCU.** É a única que testa se o índice mede algo real. Vale mais que toda a discussão de rotação.
2. **A1 — rotação oblíqua.** É a única revisão que muda um número já reportado (os pesos 65/35) e a única cuja ausência é atacável por um parecerista com a referência do próprio projeto na mão.
3. **B2 reformulado — quantos setores mudam de faixa** entre 1 e 2 fatores. Se classificarem igual, o debate Kaiser × Horn × IVS-BH é irrelevante, e isso se diz à banca.

---

*Documentos citados: `GUIA_DO_PROJETO.md` (§3, §6.2, §6.3, §8) · `docs/metodologia/Analise_Fatorial_Enap2019_Guia_de_Leitura.md` · `docs/metodologia/Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md` · `docs/relatorios/Relatorio_EDA_Fase3_IVS_ELSI.md` (§13, §15) · `scripts/diagnostico_fatorial.py` · `src/ivs_censo/indicadores.py`.*
