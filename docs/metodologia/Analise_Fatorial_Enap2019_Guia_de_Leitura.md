# O livro da Enap lido a partir do Projeto IVS

## MATOS & RODRIGUES, *Análise fatorial* (Enap, 2019) — estudo completo e o que ele muda no projeto

**Projeto:** Índice de Vulnerabilidade à Saúde (IVS) intraurbano — Censo Demográfico 2022 / ELSI-Brasil
**Instituição:** Fiocruz Minas — Instituto René Rachou (IRR) · Iniciação Científica
**Pesquisador:** Pedro Dias Soares
**Data:** 16 de setembro de 2026
**Obra:** MATOS, Daniel Abud Seabra; RODRIGUES, Erica Castilho. *Análise fatorial*. Brasília: Enap, 2019. 74 p. Coleção Metodologias de Pesquisa. ISBN 978-85-256-0118-6.

> **Documento irmão:** [`Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md`](Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md), de 24/08/2026, que analisa Figueiredo & Silva (2010) e roda os testes nos dados. Este documento **não repete aquele**: cobre o que o livro da Enap acrescenta, e os pontos em que os dois divergem.
>
> **Versão em PDF:** [`Guia_Leitura_Analise_Fatorial_Enap2019.pdf`](Guia_Leitura_Analise_Fatorial_Enap2019.pdf) — mesma substância, diagramada para leitura impressa.

---

## Sumário executivo

1. **O livro da Enap não é uma segunda opinião sobre Figueiredo & Silva (2010) — ele discorda dele em três pontos que mudam decisões já tomadas no projeto.** A rotação deve ser oblíqua e não Varimax; a técnica deve ser análise fatorial e não componentes principais; e a regra de comunalidade de 0,50 não deve ser aplicada como corte rígido.

2. **Nos três casos, o livro dá razão ao que os dados do projeto já indicavam.** O achado mais forte do documento sobre Figueiredo — que aplicar o corte de comunalidade mecanicamente teria excluído a água, a variável errada — deixa de ser crítica própria e passa a ser convergência com a bibliografia (p. 58).

3. **O livro sustenta duas ressalvas que o projeto já fazia por conta própria.** Que o Bartlett tende a rejeitar H₀ em amostras grandes (p. 43), e que "AFC" não deve nomear uma ACP com número de fatores fixado *a priori*.

4. **Dois limites novos, que nenhuma das duas referências cobre:** dados faltantes (o projeto perde 15,9% dos setores por sigilo não aleatório) e dependência espacial (setores vizinhos não são independentes, e a AF pressupõe que sejam).

5. **E um limite conceitual que é o mais sério de todos:** o livro ensina a **mensurar um construto** (modelo reflexivo); o projeto precisa **compor um índice** (modelo formativo). Ver a seção 5.

---

## 1. Como ler o livro

O livro tem 74 páginas e é curto o bastante para ser lido inteiro. Este documento não é um resumo — é um companheiro de margem, para ser lido junto.

A diferença importa porque o projeto não chega neste livro do zero. A análise fatorial já está **rodada**: `scripts/diagnostico_fatorial.py` produziu KMO, Bartlett, autovalores, análise paralela de Horn, comunalidades e cargas rotacionadas para seis cenários, em `banco_de_dados/eda/fatorial/`.

### Roteiro em três sessões

| Sessão | Páginas | Tempo | O que extrair |
|---|---|---|---|
| 1ª | 7–26 | ~50 min | O vocabulário: variável latente, fator, carga fatorial, escore fatorial, comunalidade. Meta: entender por que uma carga pode ser uma correlação *ou* um coeficiente de regressão — isso decide qual matriz se reporta. |
| 2ª | 26–46 | ~60 min | O núcleo de decisão: AF × ACP, número de fatores, extração, **rotação**, e as Tabelas 7 e 8 (p. 44 e 46). É aqui que o livro contradiz o que o projeto fez. Ler com o `resumo_adequabilidade.csv` ao lado. |
| 3ª | 46–71 | ~55 min | Os dois exemplos. O Exemplo 2 (p. 67–71) é o **molde exato** do caso do IVS: índice socioeconômico latente a partir de itens do IBGE, com escores usados depois em outro modelo. |

Se o tempo for curto, ler nesta ordem: **37–39** (rotação), **67–71** (Exemplo 2), **26–28** (AF × ACP), **22–26** (escores). São dezesseis páginas e cobrem quatro das cinco revisões da seção 4.

> As páginas citadas neste documento são as **do livro** (numeração impressa). No arquivo PDF, somar 1: a página 9 do livro é a página 10 do PDF.

---

## 2. O que o livro acrescenta ao que já foi feito

| Tema | Páginas | O que o projeto fez | O que o livro acrescenta |
|---|---|---|---|
| **Rotação oblíqua** | 34–39 | Varimax (ortogonal), seguindo Figueiredo | Diz que Varimax em Ciências Humanas "não parece ter nenhum sentido" sem evidência forte de que os fatores são independentes. Os do IVS não são. |
| **AF × ACP** | 26–28 | ACP sobre a matriz de correlação | Com menos de 20 variáveis e comunalidades baixas, as duas técnicas *divergem* (Stevens, 1992). O projeto tem 6–7 variáveis e uma comunalidade de 0,380. |
| **Escores fatoriais** | 22–26, 69–71 | Ainda não calculados; o plano é média ponderada das variáveis padronizadas | Classifica a média ponderada pelas cargas como método **"não refinado"** e instável, e ensina o método da regressão como alternativa. |
| **Matriz padrão × estrutura** | 21–22 | Não se aplicava (solução ortogonal) | Com rotação oblíqua surgem duas matrizes de cargas com leituras diferentes. Define qual reportar: a **padrão**. |
| **Regra da comunalidade** | 26, 58 | Descobriu empiricamente que o corte de 0,50 excluiria a variável errada | Dá respaldo bibliográfico: o critério "não deve ser utilizado isoladamente e de maneira muito rígida". |

---

## 3. Companheiro de leitura, seção por seção

### A. Introdução e o que é análise fatorial — p. 7–11

Variáveis latentes e construtos; fator como combinação linear das variáveis originais; técnicas de *dependência* (regressão) × *interdependência* (AF); uso exploratório × confirmatório.

**Pergunta a carregar:** *o IVS é uma AFE ou uma AFC? E se a resposta honesta for "nenhuma das duas exatamente", como isso se escreve?*

**No projeto.** Na página 9 o livro lista **"vulnerabilidade social"** entre os exemplos de variável latente, ao lado de inteligência e nível socioeconômico. É o construto do projeto nomeado pela referência — vale citar.

Quanto à postura, o projeto está no mesmo lugar ambíguo do artigo de Figueiredo: duas dimensões (saneamento e socioeconômica) vêm *a priori* do IVS-BH 2012, mas a estimação é exploratória. O livro é mais rigoroso que o artigo — reserva "AFC" para modelagem de equações estruturais e a deixa fora do escopo. Isso confirma a correção já registrada na §5.4 do documento irmão: escrever **"análise fatorial exploratória com número de fatores orientado pela teoria"**, nunca "AFC".

### B. Níveis de mensuração e tipos de correlação — p. 11–15

Escalas nominal, ordinal, intervalar e de razão; e a correlação que cada combinação pede: Pearson, bisserial, policórica, polisserial, tetracórica.

**Pergunta a carregar:** *o livro oferece cinco correlações e nenhuma é a que eu uso. O que isso significa?*

**No projeto.** Primeira lacuna real do livro. As cinco correlações resolvem combinações de variáveis **categóricas**. As sete variáveis do IVS são contínuas — proporções, uma razão e uma renda em reais — o que pelo catálogo levaria a Pearson. Mas o projeto usa **Spearman**, por um motivo que o livro não contempla: assimetria de 3,42 na água, 3,74 na renda e curtose de 49,5 na renda. Spearman não está entre as cinco porque o livro trata de escalas Likert, não de proporções infladas de zeros.

O efeito dessa escolha já está medido:

| Critério | Pearson | Spearman | Leitura |
|---|---:|---:|---|
| KMO global | 0,732 | **0,783** | Sobe dentro da faixa "bom" (Tabela 6, p. 43) |
| MSA mínimo | 0,542 | **0,700** | Sai da zona "medíocre" |
| Coeficientes \|r\| ≥ 0,30 | 33,3% | **57,1%** | Com Pearson a base **reprova** no critério da "maioria acima de 0,30" (p. 42) |
| Fatores por Kaiser | 3 | **2** | Solução mais parcimoniosa |
| Variância acumulada | 53,6% | **62,1%** | Só Spearman cruza o patamar de 60% de Hair |

Com Pearson, a base seria reprovada em dois critérios de adequabilidade da Etapa 1. A escolha por Spearman não é cosmética — é o que torna a análise defensável, e precisa ser justificada com a não-normalidade documentada na §9 do relatório da EDA.

### C. Fatores, formas de representação e cargas fatoriais — p. 15–22

A matriz-R, a representação gráfica dos fatores como eixos, a equação linear, a definição de carga fatorial. Termina distinguindo matriz de estrutura de matriz padrão.

**Pergunta a carregar:** *se eu adotar rotação oblíqua, qual das duas matrizes de cargas vira o peso do índice?*

**No projeto.** O exemplo didático da Tabela 1 (p. 15) tem sete itens, e o **item 7 se correlaciona fracamente com todos os outros** — o livro anuncia ali que ele provavelmente terá de sair. O `pct_lixo_inad` é essa figura: correlações de 0,10 a 0,24 com todas as demais. A diferença, que enriquece a discussão, é que o lixo **não** ficou com comunalidade baixa: ficou com 0,859, porque formou um fator só dele. O livro não tem esse caso; o projeto tem.

O ponto denso está nas páginas 21–22: quando os fatores são correlacionados, a carga deixa de ser correlação e passa a ser **coeficiente de regressão**, e surgem duas matrizes — *estrutura* (correlações) e *padrão* (coeficientes de regressão). O livro registra que a maioria interpreta a **padrão**. Hoje isso não afeta o projeto, porque a solução Varimax é ortogonal e as duas coincidem. Se a seção H convencer a migrar para oblíqua, os pesos passam a sair da matriz padrão — e isso precisa ser dito explicitamente.

> **Armadilha (p. 22).** Uma carga oblíqua **pode passar de 1**, por ser coeficiente de regressão. Se isso ocorrer, checar a variância residual: se for negativa, a solução é inadmissível e sugere fatores demais. Vale guardar o teste — a matriz do IVS é mal condicionada por renda × cor/raça a −0,811.

### D. Escores fatoriais e o método da regressão — p. 22–26

Escore fatorial como média ponderada das variáveis pelas cargas; métodos "não refinados" × "refinados"; o método da regressão, em que os pesos saem de `B = R⁻¹A`.

**Pergunta a carregar:** *o IVS que eu planejo é, na classificação deste livro, um método não refinado. Isso é um problema?*

**No projeto.** Estas quatro páginas contêm a crítica mais direta ao plano atual. O GUIA (§3, item 4) prevê o IVS como "média ponderada das variáveis padronizadas", com pesos vindos da fatorial. Na taxonomia da página 23, isso é um **método não refinado**, com três defeitos: depende da escala das variáveis, depende da rotação escolhida, e "é muito instável por depender fortemente da amostra em particular que está sendo analisada".

Mas há uma tensão real, que não se resolve só aceitando o conselho:

| Critério | Escore refinado (regressão) | Média ponderada 0–1 |
|---|---|---|
| Estabilidade estatística | Alta — é o que o livro recomenda | Baixa — instável entre amostras |
| Escala resultante | Padronizada, aprox. −3 a +3 | **0 a 1, diretamente interpretável** |
| Categorização em 4 faixas | Possível, mas por quantis de um escore abstrato | **Natural e comunicável ao gestor** |
| Comparabilidade com o IVS-BH 2012 | Perdida — o IVS-BH é média ponderada | **Preservada** |
| Reprodutibilidade por terceiros | Exige `R⁻¹` e os dados completos | **Sete pesos numa tabela bastam** |

**A saída não é escolher: é calcular os dois e usar a concordância como validação.** Se o escore refinado e o índice 0–1 ordenarem os setores igual — Spearman acima de ~0,95 —, a instabilidade que o livro teme não se materializou, e o índice 0–1 se reporta com a evidência no apêndice. Se divergirem, descobriu-se algo importante antes de publicar.

Anotar também a p. 24: os escores servem como **substitutos das variáveis originais** em análises posteriores, inclusive para resolver multicolinearidade em regressões. É munição para quando o IVS for cruzado com desfechos do ELSI.

### E. Comunalidade, análise fatorial e componentes principais — p. 26–28

Variância comum, específica e de erro; comunalidade e o mínimo de 0,50; AF × ACP — a ACP usa toda a variância, a AF apenas a compartilhada.

**Pergunta a carregar:** *rodei ACP. O livro diz que, no meu tamanho de problema, a AF daria outro resultado. Daria?*

**No projeto.** As três páginas mais consequentes, por uma razão aritmética. O livro traz a regra de convergência de Hair (as duas dão o mesmo com >30 variáveis ou comunalidades >0,60) e a advertência de Stevens (1992): **com menos de 20 variáveis e comunalidades abaixo de 0,4, os resultados podem divergir**.

| Condição para AF ≈ ACP | Limiar | Caso do IVS (sem lixo) | Situação |
|---|---:|---:|---|
| Número de variáveis | > 30 | 6 | **falha** |
| Comunalidade da maioria | > 0,60 | 4 de 6 acima | limítrofe |
| Comunalidade mínima | > 0,40 | 0,380 (razão de moradores) | **falha** |

Duas das três falham. Não se pode mais afirmar que "ACP e AF dariam a mesma coisa" — virou hipótese a testar. E o teste é barato. Se divergirem, a escolha se decide pela citação de Tabachnick & Fidell na p. 27: análise fatorial para uma solução teórica não contaminada por erro, componentes principais para um resumo empírico. O IVS quer estimar um construto teórico — isso aponta para AF.

> Guardar a definição de comunalidade como "proporção de variância explicada pelos fatores **retidos**". É a base lógica do achado sobre a água: 0,253 com sete variáveis, 0,822 sem o lixo. **A comunalidade é propriedade da solução, não da variável.**

### F. Autovalores, diagrama de declividade e variância acumulada — p. 28–32

Kaiser (autovalor > 1), *scree test* de Cattell, patamar de 60% — com a instrução de usá-los em conjunto e a advertência de que costumam discordar.

**Pergunta a carregar:** *meu segundo autovalor é 1,049 e o terceiro é 0,958. Kaiser está decidindo com folga de 0,09 — ele tem autoridade para isso com 7 variáveis?*

**No projeto.** Não tem, e o livro diz isso. Na p. 29 registra que Kaiser funciona melhor entre **20 e 50 variáveis** (Tabachnick & Fidell) e é mais preciso com comunalidades pós-extração acima de 0,7 (Stevens). O projeto tem 6–7 variáveis e comunalidades a partir de 0,380. **Kaiser é o mais fraco dos três critérios aqui** — o que é desconfortável, porque é ele que sustenta o segundo fator.

E há um detalhe já medido: na solução recomendada, sem o lixo, **Kaiser retém apenas um fator** (2º autovalor = 0,9585) e Horn concorda. A retenção do segundo se apoia na razão teórica. A p. 32 dá o respaldo: a decisão final pode ser teórica, e a pergunta certa é "teoricamente faz mais sentido essas variáveis estarem agrupadas em quantos fatores?". É a citação que legitima a escolha, e precisa aparecer no artigo.

Notar ainda que a **análise paralela de Horn**, que o script do projeto já implementa e que é mais robusta que Kaiser, **não está neste livro** — está em nota de rodapé em Figueiredo. O projeto usa um critério melhor que o da sua referência principal; vale dizer isso.

### G. Extração de fatores — p. 32–34

Cinco métodos: componentes principais, fatores principais, máxima verossimilhança, MQO e MQG.

**No projeto.** Leitura rápida com uma consequência prática. O livro observa que, com um número razoável de observações e variáveis, os métodos de extração **não devem divergir muito** — e que essa convergência é, ela própria, uma forma de validar as estimativas. Com 87 mil setores, rodar dois métodos e mostrar que as cargas batem é sensibilidade barata e convincente.

A restrição é de engenharia: o `requirements.txt` tem pandas, numpy e matplotlib, e o `diagnostico_fatorial.py` implementou tudo à mão em numpy para não crescer essa lista. A **fatoração do eixo principal** é implementável em numpy em poucas linhas — é ACP iterada com comunalidades estimadas na diagonal. Máxima verossimilhança já pede otimização numérica.

### H. Rotação de fatores e a escolha do método — p. 34–39

> **A passagem mais importante do livro para este projeto — p. 38:**
> "usar rotação ortogonal com dados de Ciências Humanas e Sociais não parece ter nenhum sentido. Nessas áreas, as variáveis quase sempre são correlacionadas. Assim, existem autores que defendem que esse tipo de rotação fatorial nunca deveria ser utilizado em Ciências Humanas e Sociais. Portanto, para usar rotação ortogonal, o pesquisador precisaria ter evidências teóricas ou empíricas muito fortes de que os fatores não são correlacionados."

**No projeto.** O `diagnostico_fatorial.py` usa Varimax, herdado de Figueiredo, que o usa "por ser a mais comum". O livro trata essa escolha como o caminho que exige prova — e a prova que pede é de que os fatores **não** se correlacionam. No IVS, independência entre a dimensão socioeconômica e a de saneamento é implausível: esgoto inadequado com analfabetismo a 0,429 e com renda a −0,454, em Spearman.

A consequência vai além do rigor formal. A rotação oblíqua produz uma **matriz de correlação entre os fatores**, que a ortogonal não pode produzir. Essa matriz é evidência que o projeto hoje não tem:

- **Valida a estrutura.** No Exemplo 1 (p. 66), a interpretação das correlações entre fatores — negativas entre concepções opostas, positiva entre afins — é usada como confirmação de que a solução faz sentido teórico.
- **Afeta os pesos.** A repartição 65/35 foi calculada por soma dos quadrados das cargas *ortogonais*. Com fatores correlacionados, parte da variância é compartilhada, e a repartição muda. O número que hoje converge com os 60/40 do IVS-BH **precisa ser recalculado** antes de virar peso oficial.
- **Justifica a escolha *a posteriori*.** A p. 67 registra que "as correlações encontradas entre os fatores evidenciam que a escolha por uma rotação oblíqua foi acertada". É o padrão da área e será esperado.

Quanto ao método: o livro nomeia `oblimin` como a oblíqua geralmente mais indicada e `promax` como a alternativa rápida para bases muito grandes. Com 87 mil casos, `promax` é a escolha pragmática — e é implementável em numpy sem grande esforço, por ser Varimax seguido de transformação oblíqua por mínimos quadrados.

### I. Planejamento e etapas da AFE — p. 39–46

Duas etapas: adequação da base (amostra, mensuração, matriz de correlações, Bartlett, KMO) e a análise (número de fatores, extração, rotação, interpretação). Fecha com as Tabelas 7 e 8.

**No projeto.** Conferência da Tabela 7 (p. 44) contra o `resumo_adequabilidade.csv`:

| Critério do livro | Patamar | Resultado (7 comp., Spearman) | Situação |
|---|---|---|---|
| Tamanho da amostra | > 100 e ≥ 5 obs./variável | 87.545 · 12.506:1 | Atendido com folga |
| Nível de mensuração | Definir o tipo de correlação | Contínuas · Spearman | Atendido, com justificativa fora do catálogo do livro |
| Matriz de correlação | Maioria dos coeficientes > 0,30 | 57,1% — e 80,0% sem o lixo | Atendido |
| Teste de Bartlett | p < 0,05 | χ² = 235.084 · gl 21 · p ≈ 0 | Atendido, **mas vazio** |
| KMO | ≥ 0,50; ideal a partir de 0,70 | 0,783 · MSA mín. 0,700 | Atendido |

> **O livro dá razão à ressalva sobre o Bartlett.** A §5.1 do documento irmão critica Figueiredo por apresentar o BTS sem ressalva sobre sensibilidade ao *n*. Na p. 43 a Enap faz exatamente essa ressalva: o teste "depende muito do tamanho amostral e tende a rejeitar a hipótese nula para amostras grandes", e por isso "a significância desse teste não é uma garantia de que todas as variáveis vão se agrupar em fatores".
>
> **Como reportar:** em vez de "o Bartlett é vazio nesta escala", escrever *"conforme advertem Matos & Rodrigues (2019, p. 43), o teste tende a rejeitar H₀ em amostras grandes; a conclusão de adequabilidade se apoia no KMO e nos MSA individuais"*.

Segundo ganho, na p. 42: o livro fixa em **0,80** o limiar a partir do qual correlações altas indicam multicolinearidade, em que "fica inviável separar o peso delas em cada um dos fatores". A correlação de Spearman entre renda e cor/raça é **−0,811**. Está acima do limiar, por pouco. Não invalida nada, mas um parecerista atento levantará — melhor que apareça declarado. A mesma página sugere a **SMC por variável** como diagnóstico complementar; é uma linha de numpy.

### J. Exemplo 1 — os nove passos — p. 46–67

Percurso completo em R sobre um questionário de 12 itens e 756 respondentes.

**No projeto.** Ler pelo **item 12**, o personagem central: suspeito na matriz de correlações (passo 3), confirmado na rotação com carga 0,182 (passo 8), comunalidade 0,036, excluído, e o modelo sobe de 53,6% para 58,1%. É a mesma sequência percorrida com o lixo — inclusive na ordem: suspeita na matriz, confirmação na solução rotacionada, exclusão, ganho de variância (62,1% → 70,0%).

Duas passagens a marcar:

- **P. 58.** "O critério da comunalidade maior do que 0,5 não deve ser utilizado isoladamente e de maneira muito rígida" — e o livro mantém no modelo um item abaixo do corte porque ele tem carga alta. **É a frase que resolve o caso da `razao_moradores`** (comunalidade 0,380, carga 0,532): há respaldo para mantê-la, desde que os dois números sejam reportados.
- **P. 59.** O procedimento de exclusão: identificar problemáticas por indeterminação fatorial *e* comunalidade baixa, excluir **poucas por vez**, reajustar, repetir. É o protocolo formal do que o projeto fez informalmente com o lixo — citá-lo faz a exclusão aparecer como procedimento, não conveniência.

Uma diferença de escala que convém não esconder: o exemplo tem 756 casos e 12 itens (razão 63:1); o projeto tem 87.545 e 6 variáveis (14.590:1). **Nenhum critério de amostra do livro é exigente para este caso** — o que significa que eles não informam nada sobre a qualidade da solução. O que limita a análise não é o *n*, é o número pequeno de variáveis, e o livro não trata desse problema.

### K. Exemplo 2 — o índice de nível socioeconômico — p. 67–71

Indicador de NSE a partir de 13 itens da Prova Brasil (2.497.431 alunos), um único fator, escores usados como variável explicativa em modelo multinível.

**A parte mais diretamente aproveitável do livro inteiro.** O desenho é o do projeto: construto socioeconômico latente, itens do IBGE, amostra enorme, escores reaproveitados a jusante.

| Aspecto | Exemplo 2 (NSE) | Projeto IVS |
|---|---|---|
| Unidade | Aluno | **Setor censitário** — a carga descreve covariação entre territórios, não entre pessoas |
| Variáveis | 13 itens categóricos | 6 ou 7 proporções contínuas |
| Correlação | Policórica | Spearman |
| Nº de fatores | **1** — e a rotação então não é necessária | 2, o segundo sustentado pela teoria |
| Variância explicada | 66% | **70,0%** (sem o lixo) |
| Escores | Método da regressão | A definir — ver seção D |
| Uso a jusante | Preditor em modelo multinível | Índice 0–1, 4 faixas, mapas, cruzamento com o ELSI |

Duas frases para transcrever:

- **P. 69:** "a rotação não precisa ser executada quando encontramos apenas 1 fator". Relevante porque na solução sem lixo Kaiser aponta um único fator — se a orientadora preferir a solução unifatorial, toda a discussão de rotação desaparece e o índice fica mais simples de defender, ao custo de abandonar a estrutura de duas dimensões do IVS-BH. É alternativa legítima e merece ir à mesa.
- **P. 71:** os fatores mantêm a representatividade das variáveis originais, de modo que "os itens contribuem de maneira desigual para o fator: quanto maior a carga fatorial, maior a contribuição do item", e "isso não acontece em outras técnicas mais simples de elaboração de índices", que pressupõem contribuição igual. **É a formulação canônica do argumento da decisão nº 1 do GUIA** — a de que pesos iguais dariam "três votos" à posição social sem escolha deliberada.

---

## 4. As cinco revisões que a leitura obriga

| # | Ponto | Situação atual | O que fazer |
|---|---|---|---|
| 1 | **Rotação** | Varimax, herdado de Figueiredo | Rodar `promax`/`oblimin`, reportar a matriz de correlação entre fatores, **recalcular a repartição 65/35** na solução oblíqua antes de fixá-la |
| 2 | **Extração** | ACP; equivalência com AF pressuposta | Duas das três condições de Stevens falham. Rodar fatoração do eixo principal e comparar cargas |
| 3 | **Escores** | Plano: média ponderada 0–1 | É "não refinado" (p. 23). Calcular também o escore pelo método da regressão e reportar a correlação entre os rankings |
| 4 | **Multicolinearidade** | Renda × cor/raça a −0,811, tratada como argumento a favor de pesos empíricos | Está acima do limiar de 0,80 (p. 42). Declarar nas limitações e acrescentar SMC por variável |
| 5 | **Comunalidade da `razao_moradores`** | 0,380 — decisão pendente | A p. 58 autoriza manter variável abaixo de 0,50 quando a carga é alta (0,532). Manter, citando a passagem, reportando os dois números |

---

## 5. Onde o livro não alcança o projeto

O documento sobre Figueiredo registrou três descompassos daquele artigo. Dois deles o livro da Enap resolve (a ressalva do Bartlett e o rigor na nomenclatura da AFC). Restam quatro, e três são novos.

### 5.1 Modelo reflexivo × formativo — o limite mais sério

> **Registro de procedência.** Esta seção nasce de um parecer isolado, produzido numa rodada de *pressure-test* (`/council`) que foi **interrompida com 1 de 5 conselheiros concluídos**. Não é consenso de conselho, não foi revisada por pares e não foi confrontada com a literatura. Está aqui porque a objeção é séria e precisa ser enfrentada — **não porque esteja decidida**. Tratar como hipótese a investigar.

A análise fatorial — e o livro inteiro — pressupõe um modelo **reflexivo**: um construto latente *causa* os indicadores. Inteligência causa o desempenho nos itens do teste; o NSE causa a posse dos bens do Exemplo 2.

O IVS pode não funcionar assim. Vulnerabilidade não *causa* esgoto inadequado — esgoto inadequado *é parte constituinte* da vulnerabilidade. Isso caracterizaria um índice **formativo**. E num índice formativo:

- remover uma variável **muda a definição do construto**, em vez de apenas melhorar a medida;
- as cargas não são pesos legítimos — são correlações com o eixo de variância dominante;
- renda × cor/raça a −0,811 deixaria de ser "multicolinearidade a declarar" e passaria a ser duas dimensões substantivas a manter deliberadamente;
- o lixo com fator próprio deixaria de ser anomalia a excluir e passaria a ser evidência de que coleta de lixo é uma dimensão politicamente distinta — e excluí-la seria deixar a matriz de correlação decidir a política pública.

Se essa leitura se sustentar, a consequência é reenquadrar o Notebook 04: a fatorial vira **diagnóstico de redundância**, não motor de ponderação, e os pesos 60/40 vêm da teoria, defendidos como escolha normativa explícita.

**O que fazer com isso:** levar à orientadora como questão aberta e buscar a literatura (Diamantopoulos & Winklhofer, 2001, sobre indicadores formativos; Nardo et al., 2008, cap. sobre ponderação). Não é decisão a tomar sozinho, e não é decisão a tomar com base num único parecer não revisado.

### 5.2 O livro mede um construto; o projeto precisa compor um índice

Mesmo limite do artigo de 2010, e relacionado ao anterior. O livro termina nos escores usados como variável em outro modelo. O projeto precisa de um índice 0–1, com pesos explícitos, em quatro faixas, mapeável. Normalização, forma de agregação (aritmética ou geométrica), tratamento de faltantes na composição e análise de sensibilidade dos pesos ficam fora. Referência: Nardo et al. (2008), somado ao que o IVS-BH 2012 e o ISU de Passarelli-Araujo (2023) já resolveram.

### 5.3 Dados faltantes não aparecem no livro

O livro **não discute dados faltantes em nenhuma das 74 páginas** — seus exemplos são questionários com resposta completa. O projeto perde **16.563 setores (15,9%)** na exclusão por lista, quase todos pelo sigilo do analfabetismo, e o GUIA (§6.2.6) documenta que esse sigilo **não é aleatório**: incide nos setores de melhor situação. A amostra de 87.545 é enviesada para os setores mais vulneráveis. O cenário sem analfabetismo, já rodado, mostra que a estrutura não muda — bom argumento —, mas o tratamento adequado exige literatura que o projeto ainda não tem.

### 5.4 Dependência espacial

A AF pressupõe unidades independentes. Setores censitários vizinhos não são: vulnerabilidade se agrupa no espaço, e o projeto já prevê calcular o I de Moran. Autocorrelação espacial infla a covariação observada e, com ela, autovalores e cargas. Nada no livro toca nisso. Não é preciso resolver nesta etapa; é preciso **declarar**, e o I de Moran dos escores dará a medida do problema.

### 5.5 Falácia ecológica

Já registrada no projeto, e vale repetir porque o Exemplo 2 induz ao erro: lá as unidades são alunos e o NSE é atributo de pessoas. Aqui as unidades são territórios. Toda carga fatorial do IVS descreve covariação **entre setores** e nada afirma sobre indivíduos.

---

## 6. Perguntas para a orientação

| # | Pergunta | Origem | Recomendação |
|---|---|---|---|
| 1 | A solução oficial será ortogonal ou oblíqua? | p. 37–39 | **Oblíqua** (`promax`), pela recomendação do livro e pela evidência de validação que produz |
| 2 | ACP ou análise fatorial propriamente dita? | p. 26–28 | Rodar as duas; reportar AF como principal se divergirem |
| 3 | Um fator ou dois? | p. 28–32 | Dois, por razão teórica declarada — registrando que Kaiser e Horn apontam um na solução sem lixo |
| 4 | O índice será escore fatorial ou média ponderada 0–1? | p. 22–26 | **Média ponderada 0–1** como oficial, com o escore refinado no apêndice como validação |
| 5 | A `razao_moradores` fica com comunalidade 0,380? | p. 58 | **Sim**, citando a passagem que relativiza o corte |
| 6 | A fatorial roda antes ou depois da normalização municipal? | fora do livro | **Antes**, sobre os brutos — já medido na §4.4 do documento irmão |
| 7 | O IVS é um construto reflexivo ou um índice formativo? | fora do livro | **Em aberto.** Ver §5.1 — precisa de literatura e de decisão da orientação |

---

## Referências

MATOS, D. A. S.; RODRIGUES, E. C. **Análise fatorial**. Brasília: Enap, 2019. 74 p. (Coleção Metodologias de Pesquisa).

FIGUEIREDO FILHO, D. B.; SILVA JÚNIOR, J. A. Visão além do alcance: uma introdução à análise fatorial. **Opinião Pública**, Campinas, v. 16, n. 1, p. 160–185, jun. 2010.

HAIR, J. F. et al. **Análise multivariada de dados**. 5. ed. Porto Alegre: Bookman, 2005.

TABACHNICK, B. G.; FIDELL, L. S. **Using Multivariate Statistics**. Needham Heights: Allyn & Bacon, 2007.

STEVENS, J. P. **Applied Multivariate Statistics for the Social Sciences**. 2. ed. Hillsdale: Erlbaum, 1992.

FIELD, A.; MILES, J.; FIELD, Z. **Discovering Statistics Using R**. London: Sage, 2012.

DISTEFANO, C.; ZHU, M.; MINDRILA, D. Understanding and using factor scores. **Practical Assessment, Research & Evaluation**, v. 14, n. 20, p. 1–11, 2009.

NARDO, M. et al. **Handbook on Constructing Composite Indicators**. Paris: OECD/JRC, 2008.

DIAMANTOPOULOS, A.; WINKLHOFER, H. M. Index construction with formative indicators. **Journal of Marketing Research**, v. 38, n. 2, p. 269–277, 2001. *(a conferir — indicada na §5.1, ainda não lida)*

SECRETARIA MUNICIPAL DE SAÚDE DE BELO HORIZONTE. **Índice de Vulnerabilidade à Saúde 2012**. Belo Horizonte: SMS-BH, 2013.

---

*Documentos do projeto citados: `GUIA_DO_PROJETO.md` (§3, §4, §6.2.6, §6.3, §8) · `docs/metodologia/Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md` (§3.2, §4.4, §5.1, §5.4) · `docs/relatorios/Relatorio_EDA_Fase3_IVS_ELSI.md` (§9, §13, §15) · `scripts/diagnostico_fatorial.py` · `banco_de_dados/eda/fatorial/resumo_adequabilidade.csv`.*

*Todos os números do projeto citados vêm de `banco_de_dados/eda/fatorial/` e `banco_de_dados/eda/correlacao_spearman.csv`, gerados por scripts versionados. Nenhum foi recalculado para este documento.*
