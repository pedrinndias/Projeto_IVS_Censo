<!-- converted from guia_analises.docx -->


GUIA COMPLETO DE
ANÁLISE EXPLORATÓRIA
E ANÁLISE ESTATÍSTICA

Para preparação de pesquisas e artigos científicos
Baseado nos Módulos 2 e 3 do Curso de Análise de Dados
FIOCRUZ — Campus Virtual
Módulo 2: Estatística Descritiva e Comunicação de Resultados
Módulo 3: Modelos Estatísticos

PARTE I  ANÁLISE EXPLORATÓRIA E DESCRITIVA
A análise exploratória de dados é uma etapa fundamental e imprescindível antes de qualquer modelagem mais avançada. Ela permite entender a estrutura dos dados, detectar padrões, identificar outliers e escolher os modelos mais adequados para cada situação de pesquisa.

# 1. Variáveis Aleatórias

Em estatística, o termo variável aleatória representa uma característica de interesse em um determinado estudo. Ao medir, por exemplo, o consumo de cigarro em um estudo sobre morbidade, outras variáveis como época do ano, faixa etária e doença também são consideradas variáveis aleatórias. Uma variável aleatória é uma medição de determinado tópico da qual se obtêm valores não antecipados.
## 1.1 Variáveis Qualitativas
Descrevem atributos ou categorias — características que não possuem valor numérico intrínseco — e se dividem em:
- Nominal: quando descrevem atributos não ordenáveis, como tipo de doença (câncer, HIV, hepatite) ou época do ano (verão, outono, inverno).
- Ordinal: quando descrevem qualidades que possuem ordem natural, como faixa etária ("<18 anos", "18 a 25 anos", ">25 anos") ou tempo de consumo ("<1 ano", "1 a 3 anos").

## 1.2 Variáveis Quantitativas
Descrevem características mensuráveis numericamente e se dividem em:
- Discreta: assume valores inteiros, como idade (18, 19, 20 anos) ou número de filhos.
- Contínua: assume valores fracionados, como altura (1,80 m) e peso (67,8 kg).



# 2. Levantamento Estatístico e Amostragem

O trabalho estatístico abrange coleta de dados, cálculo de medidas e análise, sendo denominado de 'levantamento' estatístico. Ele pode ser classificado quanto à abrangência e à origem dos dados.
## 2.1 Quanto à Abrangência
- Total (Censo): todos os elementos/indivíduos de estudo entram na pesquisa. Exemplo: pesquisa com todos os alunos de uma escola.
- Parcial (Amostra): apenas uma parte representativa dos elementos é incluída no estudo. Exemplo: Pesquisa Nacional por Amostras de Domicílios (PNAD).

## 2.2 Quanto à Origem dos Dados
- Primários: coletados diretamente do ambiente de estudo pelo próprio pesquisador. Exemplo: pesquisas de campo, entrevistas, experimentos.
- Secundários: coletados por outros indivíduos/instituições, muitas vezes com periodicidade regular (a cada 2, 3 ou 5 anos). Exemplo: censo escolar, dados do DATASUS.

## 2.3 Tipos de Amostragem
A amostragem é amplamente usada em levantamentos estatísticos devido à redução de custos e tempo, e à possibilidade de realizar pesquisas destrutivas ou de alto risco. As amostras podem ser conduzidas de diferentes formas:
- Amostragem Aleatória Simples (AAS): considerada o padrão ouro em estatística. Todos os elementos devem estar enumerados e a seleção é feita por sorteio usando software de geração de números aleatórios. Requer conhecimento prévio de todos os indivíduos da população.
- Amostragem Estratificada: a população é dividida em subgrupos (estratos) e amostras são retiradas de cada estrato. Garante representatividade de subgrupos minoritários.
- Amostragem por Conglomerados: a população é dividida em grupos (conglomerados) e alguns grupos são sorteados para compor a amostra. Útil quando a lista completa de indivíduos não está disponível.
- Amostragem Sistemática: os elementos são selecionados em intervalos regulares (ex.: a cada 10 indivíduos da lista). Requer que a lista esteja disponível.


# 3. Medidas de Locação (Tendência Central)

As medidas de locação resumem o máximo possível os dados para extrair informações sobre uma amostra. Elas medem o 'centro' ou 'meio' da distribuição dos dados e são essenciais para a análise estatística.
## 3.1 Média Aritmética
A média aritmética é dada pela soma de todas as observações dividida pelo número delas:
x̄ = (Σᵢ₌₁ⁿ xᵢ) / n
A média aritmética é uma medida de locação muito natural e amplamente utilizada. Sua principal limitação é a sensibilidade para valores extremos/aberrantes (outliers): todas as observações recebem o mesmo peso (1/n). Na presença desses valores, pode não ser a medida mais apropriada.

## 3.2 Mediana
A mediana é o número que divide uma amostra ordenada em dois grupos de igual quantidade de observações. É a alternativa mais robusta à média quando há outliers, pois é insensível a valores extremos:
- Se n for ímpar: mediana = elemento do meio = observação de posição (n+1)/2
- Se n for par: mediana = média das duas observações centrais (posições n/2 e n/2 + 1)
A mediana equivale ao 50º percentil, ao 5º decil ou ao 2º quartil (Q₂).

## 3.3 Média Aritmética Ponderada
É uma modificação da média aritmética onde cada elemento tem pesos distintos (wᵢ). É útil quando certos atributos valem mais do que outros — por exemplo, na avaliação da qualidade de serviços de saúde:
w̄ = (Σᵢ₌₁ⁿ wᵢ · xᵢ) / (Σᵢ₌₁ⁿ wᵢ)

## 3.4 Quantis
Os quantis expressam medidas mais gerais de distribuição dos dados, não restringindo-se apenas ao centro. O q-ésimo quantil é o valor até o qual temos q% dos pontos da amostra ordenada. Os tipos mais utilizados são:

Para cálculo dos percentis, usam-se duas regras: se (n×p)/100 não for inteiro, o p-ésimo percentil é a (k+1)-ésima maior observação (em que k é o maior inteiro menor que (n×p)/100); se (n×p)/100 for inteiro, o percentil é a média entre as observações de posição (n×p)/100 e (n×p)/100 + 1.
# 4. Medidas de Dispersão

As medidas de dispersão quantificam a variabilidade dos dados ao redor de um centro. Duas amostras podem ter a mesma média, mas distribuições completamente diferentes — e as medidas de dispersão capturam essa diferença.
## 4.1 Amplitude
É a medida de variabilidade mais simples, definida pela distância entre o maior e o menor valor da amostra:
Amplitude = Máximo − Mínimo
Exemplo: para pesos de recém-nascidos com min=2069g e max=4146g, Amplitude = 4146 − 2069 = 2077g. Principal limitação: é altamente sensível a outliers.

## 4.2 Variância
A estatística mais utilizada para medir o espalhamento dos dados em torno de um centro. A variância amostral é a média dos desvios ao quadrado, dividida por (n-1):
s² = Σᵢ₌₁ⁿ (xᵢ − x̄)² / (n − 1)
Observação importante: a unidade da variância é o quadrado da unidade dos dados (ex.: se os dados são em mg/dL, a variância é em (mg/dL)²). Por isso, foi desenvolvida a estatística de desvio-padrão.

## 4.3 Desvio-Padrão
Resulta da raiz quadrada da variância, estando na mesma unidade dos dados originais. Pode ser interpretado como 'o quanto, em média, os dados se desviam da média':
s = √s² = √[Σᵢ₌₁ⁿ (xᵢ − x̄)² / (n − 1)]
Quanto maior o desvio-padrão, maior a dispersão dos dados em torno da média. É a medida de dispersão mais amplamente reportada em artigos científicos.

## 4.4 Coeficiente de Variação (CV)
Relaciona o desvio-padrão com a média, permitindo comparar a variabilidade relativa entre amostras com escalas ou unidades diferentes. O CV não tem unidade de medida:
CV = s / x̄  (ou em percentual: CV% = (s / x̄) × 100%)
Exemplo de interpretação: CV = 9,22% significa que o desvio-padrão corresponde a 9,22% da média, indicando variabilidade moderada. Quanto menor o CV, mais homogênea é a amostra.

## 4.5 Intervalo Interquartil (IQ)
É uma medida robusta de dispersão, menos sensível a outliers do que a amplitude, pois utiliza apenas o 1º e o 3º quartil (ignorando os extremos):
IQ = Q₃ − Q₁
Em que Q₁ é o valor até o qual temos 25% dos dados e Q₃ o valor até o qual temos 75%. O IQ representa a amplitude dos 50% centrais dos dados e é frequentemente reportado junto à mediana nas tabelas descritivas de artigos.

# 5. Métodos Gráficos — Visualização de Dados

Os gráficos são representações dos dados de forma a tornar sua compreensão mais acessível. Diferentemente das estatísticas numéricas, os gráficos geralmente utilizam todos os dados para gerar uma ilustração. A visualização adequada é indispensável antes e após a análise estatística.

## 5.1 Gráfico de Barras
Gráfico mais utilizado para apresentar dados categóricos. As barras podem ser verticais ou horizontais, e apresentam a frequência de cada grupo, preferencialmente em frequência relativa (percentual).
- Uso: variáveis qualitativas (nominal ou ordinal) ou quantitativas discretas com poucos valores.
- Boas práticas: use cores diferentes apenas quando há intenção de destacar algum agrupamento. Barras de uma mesma categoria devem ter a mesma cor.
- Evitar: iniciar o eixo Y em valor diferente de zero, pois distorce a percepção das diferenças entre grupos.

## 5.2 Gráfico de Linha
Ideal para monitoramento no tempo de determinada variável — séries temporais. Auxilia na avaliação de tendências ou mudanças ao longo do tempo.
- Uso: variáveis medidas em múltiplos pontos no tempo (semanas epidemiológicas, meses, anos).
- Atenção: comparações de apenas 2, 3 ou 4 pontos de tempo podem ser mais bem ilustradas em gráficos de barras.

## 5.3 Box Plot (Diagrama de Caixa)
Muito utilizado para ilustrar a distribuição dos dados, usando as estatísticas de localização importantes (mediana e quartis) para descrever a assimetria da distribuição.

Leitura da assimetria: se Q₃ é mais distante da mediana do que Q₁, a distribuição é positivamente assimétrica (cauda à direita). Se Q₁ é mais distante, a distribuição é negativamente assimétrica (cauda à esquerda).
O box plot pode ser estratificado por uma segunda variável categórica (ex.: estadiamento da doença), permitindo comparar as estatísticas de localização entre grupos.

## 5.4 Gráfico de Dispersão (Scatter Plot)
Utilizado quando se deseja avaliar e representar a relação entre duas variáveis numéricas. Cada eixo representa uma variável de um mesmo grupo de indivíduos, e cada ponto representa um indivíduo.
- Uso: investigar relações lineares ou não lineares entre duas variáveis quantitativas.
- Frequentemente inclui uma reta (ou curva) de regressão para evidenciar a tendência.
- Fundamental: sempre visualizar o gráfico de dispersão ANTES de calcular o coeficiente de correlação, para verificar se a relação é de fato linear.

## 5.5 Histograma
Gráfico utilizado para representar a distribuição de frequências de uma variável quantitativa contínua. As barras são adjacentes (sem espaço entre elas), e cada barra representa um intervalo de valores.
- Uso: visualizar a forma da distribuição (simétrica, assimétrica, bimodal), verificar presença de outliers.
- Importante para verificar o pressuposto de normalidade antes de testes paramétricos.

## 5.6 Princípios de Boas Práticas na Visualização
Uma boa visualização deve ser intuitiva, fácil de entender e transmitir uma única mensagem clara por gráfico:
- Clareza e simplicidade: tente sempre limitar a apenas uma mensagem por gráfico. Evite gráficos complexos com diferentes informações na mesma visualização.
- Uso adequado de cores: use cores para distinguir itens ou representar valores em uma escala. Não use cores diferentes apenas por estética, quando as barras representam a mesma unidade.
- Acessibilidade: considere o daltonismo ao escolher paletas de cores. Evite combinações vermelho-verde.
- Eixos honestos: sempre inicie o eixo Y em zero para gráficos de barras. Eixos truncados distorcem a comparação visual.
- Rótulos e títulos: todo gráfico deve ter título claro, rótulos nos eixos com unidades de medida, e fonte dos dados quando necessário.


PARTE II  INFERÊNCIA ESTATÍSTICA
A inferência estatística é um conjunto de técnicas que tem como objetivo estudar a população a partir de informações obtidas por uma amostra. O objetivo é generalizar o resultado obtido na amostra para a população de interesse.
# 6. Conceitos Fundamentais de Inferência


Um estimador é dito não viciado se seu valor esperado coincide com o parâmetro de interesse. É consistente se à medida que o tamanho da amostra aumenta, a variância tende a zero. O Teorema Central do Limite garante que a distribuição amostral da média se aproxima da Normal para amostras suficientemente grandes, independentemente da distribuição original dos dados.
# 7. Intervalo de Confiança

O intervalo de confiança (IC) é um intervalo de valores calculado a partir dos dados amostrais que fornece uma faixa dentro da qual se espera que o parâmetro populacional verdadeiro esteja, com um determinado nível de confiança (γ). Proporciona uma estimativa mais informativa do que a estimativa pontual.

## 7.1 IC para Média Populacional (σ² conhecida — distribuição Normal)
[x̄ − z_{γ/2} · σ/√n ; x̄ + z_{γ/2} · σ/√n]
Em que z_{γ/2} é o quantil da distribuição Normal padrão. Para γ = 0,95, z_{γ/2} = 1,96. No R: qnorm().
## 7.2 IC para Média Populacional (σ² desconhecida — distribuição t de Student)
Na prática, raramente conhecemos o desvio-padrão populacional. Nesse caso, ele é estimado pelo desvio-padrão amostral s e o IC é dado por:
[x̄ − t_{γ/2, n−1} · s/√n ; x̄ + t_{γ/2, n−1} · s/√n]
Em que t_{γ/2, n−1} é o valor crítico da distribuição t de Student com n-1 graus de liberdade. A distribuição t é simétrica e se aproxima da Normal quando n cresce. No R: qt().
## 7.3 IC para Proporção Populacional
A proporção é bastante utilizada em epidemiologia, podendo ser interpretada como prevalência ou incidência de uma doença. Para amostras grandes, utiliza-se a aproximação Normal:
[p̂ − z_{γ/2} · √(p̂(1−p̂)/n) ; p̂ + z_{γ/2} · √(p̂(1−p̂)/n)]
Em que p̂ é a proporção amostral. Para γ = 0,99, z_{γ/2} = 2,58.
# 8. Fundamentos do Teste de Hipóteses

Os testes de hipóteses representam uma regra de decisão que permite rejeitar ou não uma hipótese questionada, com base em valores obtidos em uma amostra. O objetivo é fornecer ferramentas que permitam validar ou refutar uma hipótese a partir dos resultados de uma amostra.
## 8.1 Formulação das Hipóteses
- Hipótese Nula (H₀): afirmação inicial ou padrão em que não há efeito ou diferença. É geralmente a hipótese que o teste busca rejeitar. Exemplo: não há diferença na média dos grupos A e B (μ₁ = μ₂).
- Hipótese Alternativa (H₁ ou Hₐ): afirmação que contradiz a hipótese nula, sugerindo que há um efeito ou diferença. Exemplo: há diferença na média dos grupos A e B (μ₁ ≠ μ₂).

## 8.2 Tipos de Erros e Poder do Teste

## 8.3 Elementos do Teste de Hipótese
- Nível de Significância (α): limiar predefinido para decidir se o resultado é estatisticamente significativo. Valores mais usados: 1%, 5% ou 10%.
- Estatística de Teste: valor calculado a partir dos dados da amostra que permite decidir se devemos rejeitar a hipótese nula.
- Região Crítica (Valor Crítico): intervalo ou ponto além do qual rejeitamos H₀. Depende do tipo de teste (bilateral ou unilateral) e do nível de significância.
- p-valor: probabilidade de obtermos uma estatística de teste tão extrema quanto a observada, ou mais, sob a suposição de que H₀ é verdadeira. Se p-valor < α, rejeita-se H₀.

## 8.4 Tipos de Teste Quanto à Direção
- Teste bilateral (duas caudas): H₁: μ ≠ μ₀ — região crítica está nas duas regiões extremas.
- Teste unilateral à direita: H₁: μ > μ₀ — região crítica está na cauda direita.
- Teste unilateral à esquerda: H₁: μ < μ₀ — região crítica está na cauda esquerda.

## 8.5 Etapas para Realização de um Teste de Hipótese
- Enunciar as hipóteses H₀ e H₁.
- Determinar um nível de significância (α) aceitável.
- Determinar a região crítica (valor crítico).
- Calcular o valor da Estatística de Teste.
- Rejeitar ou não H₀ com base na estatística de teste vs. região crítica, ou comparar o p-valor com o nível de significância.


# 9. Testes de Hipótese para Média

## 9.1 Teste t de Student para Uma Amostra
Usado quando se quer testar se a média de uma única amostra é igual a um valor conhecido ou específico. A distribuição da amostra deve ser normal e o desvio-padrão populacional é desconhecido.
Hipóteses: H₀: μ = μ₀  |  H₁: μ ≠ μ₀ (bilateral) ou H₁: μ > μ₀ (unilateral à direita)
t = (x̄ − μ₀) / (s / √n)   com n−1 graus de liberdade
Em que s é o desvio-padrão amostral, n é o tamanho da amostra e μ₀ é o valor hipotético para μ. No R: t.test().

## 9.2 Teste t de Student para Duas Amostras Independentes
Usado para comparar as médias de duas amostras independentes e determinar se há diferença significativa entre elas. Assume independência entre os grupos.
Hipóteses: H₀: μ₁ = μ₂  |  H₁: μ₁ ≠ μ₂
A estatística de teste considera a diferença das médias amostrais dos dois grupos com desvio-padrão amostral diferente para as duas situações: variâncias populacionais iguais ou diferentes. No R: t.test(x, y).
## 9.3 Teste t de Student para Duas Amostras Pareadas
Utilizado quando se quer comparar duas médias de amostras dependentes — as mesmas amostras são testadas duas vezes (ex.: antes e depois de um tratamento). A estatística de teste considera a média e o desvio-padrão da diferença entre as medidas dos grupos 1 e 2.
Hipóteses: H₀: μ₁ = μ₂  |  H₁: μ₁ ≠ μ₂ (ou μ₁ < μ₂)
No R: t.test(antes, depois, paired = TRUE).
## 9.4 ANOVA — Análise de Variância (3 ou mais grupos)
A Análise de Variância (ANOVA) é uma técnica estatística usada para comparar as médias de três ou mais grupos, determinando se há diferenças estatisticamente significativas entre elas.
Hipóteses: H₀: todas as médias dos grupos são iguais  |  H₁: pelo menos um grupo tem média diferente dos outros.
A ANOVA compara a variabilidade entre os grupos com a variabilidade dentro deles. Se a ANOVA indicar diferenças significativas, aplica-se um teste post-hoc (ex.: Teste de Tukey) para identificar quais pares de grupos diferem entre si. No R: aov() + TukeyHSD().

# 10. Testes de Hipótese para Proporção

O teste de hipótese para proporção é uma técnica estatística utilizada para tomar decisões sobre a proporção de uma característica em uma população com base em dados amostrais. É particularmente útil quando se quer comparar a prevalência ou a frequência de um evento ou característica entre grupos.
## 10.1 Teste para Uma Proporção
Usado quando se quer testar se a proporção de uma amostra é significativamente diferente de uma proporção hipotética conhecida (proporção/prevalência populacional conhecida).
Hipóteses: H₀: p = p₀  |  H₁: p ≠ p₀
z = (p̂ − p₀) / √[p₀(1 − p₀) / n]
Em que p̂ é a proporção amostral, n é o tamanho da amostra e p₀ é o valor hipotético para p. No R: prop.test().
## 10.2 Teste para Duas Proporções
Utilizado para comparar as proporções de dois grupos independentes e determinar se há diferença estatisticamente significativa entre elas.
Hipóteses: H₀: p₁ = p₂  |  H₁: p₁ ≠ p₂
A estatística de teste considera a diferença das proporções amostrais dos grupos 1 e 2. Particularmente útil em estudos de prevalência ou incidência. No R: prop.test(c(x1, x2), c(n1, n2)).
PARTE III  MODELOS ESTATÍSTICOS
Um modelo estatístico é um conjunto de observações (espaço amostral) e um conjunto de distribuições probabilísticas referente a esse espaço amostral. Modelos estatísticos buscam descrever e quantificar a relação, dependência ou associação entre variáveis.
# 11. Análise de Correlação

A correlação mede a força e a direção da associação linear entre duas variáveis numéricas. Para analisar essa associação, seleciona-se uma amostra aleatória e as duas variáveis são observadas simultaneamente em cada indivíduo.
## 11.1 Coeficiente de Correlação de Pearson (r)
É a medida mais comum de correlação linear e mede a intensidade de associação linear existente entre duas variáveis numéricas:
r = Σ(xᵢ−x̄)(yᵢ−ȳ) / √[Σ(xᵢ−x̄)² × Σ(yᵢ−ȳ)²]

O coeficiente de Pearson só deve ser calculado quando a correlação é linear (verifique pelo gráfico de dispersão). Quando os pontos formam uma nuvem cujo eixo principal é uma curva, o valor de r não mede corretamente a associação.
Para avaliar a significância estatística do coeficiente de correlação: H₀: ρ = 0 (não há correlação linear) | H₁: ρ ≠ 0 (há correlação linear). Estatística de teste: t = r / √[(1−r²)/(n−2)], com n-2 graus de liberdade. No R: cor.test().
## 11.2 Coeficiente de Correlação de Spearman (rₛ)
O coeficiente de Pearson é paramétrico e assume distribuição normal para as duas variáveis. Caso essa suposição não seja válida, deve-se preferir o coeficiente de correlação de Spearman, que é baseado nos postos (rankings) das observações e, portanto, não paramétrico.

# 12. Modelos de Regressão Linear

Os modelos de regressão são ferramentas estatísticas usadas para descrever a relação entre uma variável dependente (ou resposta) e uma ou mais variáveis independentes (ou preditoras). Permitem não só prever valores, mas também examinar a força e a natureza dessas relações.
## 12.1 Regressão Linear Simples
Descreve a relação entre uma variável dependente e uma variável independente a partir de equações de linhas retas. O modelo assume que a relação entre X e Y é linear:
Y = β₀ + β₁X + ε
- β₀: intercepto — valor de Y quando X = 0.
- β₁: coeficiente angular — mudança média em Y para cada unidade de mudança em X.
- ε: termo de erro — captura a variação em Y não explicada por X.

Os coeficientes β₀ e β₁ são estimados pelo método dos mínimos quadrados, que encontra a reta que minimiza a soma dos quadrados dos resíduos (diferenças entre valores observados e estimados). No R: lm(). Teste de Wald para significância dos coeficientes: H₀: β₁ = 0.
## 12.2 Regressão Linear Múltipla
Extensão da regressão linear simples que permite modelar a relação entre uma variável dependente Y e várias variáveis independentes X₁, X₂, …, Xₖ:
Y = β₀ + β₁X₁ + β₂X₂ + ... + βₖXₖ + ε
A interpretação dos coeficientes βⱼ é feita de forma ajustada: representa a mudança média em Y para cada unidade de mudança em Xⱼ, mantendo todas as demais variáveis constantes. Permite controlar fatores de confusão. No R: lm(Y ~ X1 + X2 + ...).
## 12.3 Qualidade do Ajuste — Coeficiente de Determinação R²
A qualidade de ajuste no modelo de regressão linear é avaliada pelo coeficiente de determinação R², que é a proporção da variabilidade total observada de Y explicada pela regressão. Quanto maior o R², melhor a qualidade de ajuste. Existem várias técnicas para verificar os pressupostos e fazer diagnóstico dos modelos.
## 12.4 Pressupostos da Regressão Linear

# 13. Regressão Logística

O modelo de regressão logística avalia a relação entre uma variável dependente binária (ou dicotômica) e uma ou mais variáveis independentes. É útil quando o objetivo é modelar a probabilidade de o desfecho ocorrer ou, ainda, estimar a razão de chances (Odds Ratio — OR), uma medida de associação bastante utilizada em epidemiologia.
A regressão logística modela o logit da probabilidade como uma função linear das variáveis independentes:
log(p / (1−p)) = β₀ + β₁X₁ + β₂X₂ + ... + βₖXₖ
- Logit: logaritmo da razão de chances (odds).
- β₀: intercepto — indica o logit da probabilidade de Y=1 quando todas as variáveis independentes são zero.
- βⱼ: mudança no logit da probabilidade de Y=1 para cada unidade de aumento na variável Xⱼ.
- exp(βⱼ): razão de chances (OR) associada a Xⱼ — interpretação direta em epidemiologia.

Exemplos de variáveis binárias de interesse na saúde: doente (sim/não), inatividade física (sim/não), óbito (sim/não). No R: glm(Y ~ X1 + X2, family='binomial').

# 14. Regressão de Poisson

O modelo de regressão de Poisson é utilizado para modelar a contagem de eventos que ocorrem em um intervalo de tempo ou espaço. É apropriado para dados em que a variável dependente é uma contagem (número de ocorrências de um evento em um dado período ou localização geográfica).
Exemplos de variáveis de contagem na saúde: número de internações por doença respiratória por semana epidemiológica, casos de dengue por bairro, óbitos anuais por câncer de mama por estado.
log(λ) = β₀ + β₁X₁ + β₂X₂ + ... + βₖXₖ
Em que λ é a média esperada de Y. Para modelar taxas (em vez de contagens brutas), introduz-se um offset (log da população ou do valor esperado). Exponenciando os coeficientes, obtemos o Risco Relativo (RR). No R: glm(Y ~ X1 + X2, family='poisson').
Atenção: a regressão de Poisson assume que a média é igual à variância (λ). Se a variância observada for maior que a média (superdispersão), a regressão Binomial Negativa pode ser mais apropriada. Se houver número excessivo de zeros, pode-se usar modelos Poisson inflacionado de zeros (ZIP) ou Binomial Negativa inflacionada de zeros (ZINB).
# 15. Modelos Lineares Generalizados (GLM) e Aditivos Generalizados (GAM)

A regressão logística, a regressão de Poisson e a regressão linear fazem parte de uma classe de modelos denominada Modelos Lineares Generalizados (GLM — Generalized Linear Models). Os GLMs são uma extensão dos modelos de regressão linear ao permitir que a variável dependente assuma outras distribuições de probabilidade, como a Binomial e Poisson.
## 15.1 Modelos Lineares Generalizados (GLM)
O GLM tem flexibilidade para modelar diferentes tipos de variáveis dependentes (contínuas, categóricas, contagens) por meio de funções de ligação (link functions). As distribuições de família mais comuns são: Normal (identidade), Binomial (logito), Poisson (log) e Gama (log ou inversa).
## 15.2 Modelos Aditivos Generalizados (GAM)
Os GAMs são uma extensão dos GLMs que permitem modelar de maneira mais flexível as relações entre variáveis explicativas e a variável dependente. Enquanto os GLMs assumem que a relação entre as variáveis explicativas e a variável resposta é linear (ou linear após aplicação de uma função de ligação), os GAMs permitem que essas relações sejam não lineares, utilizando funções suaves (splines).
g(μ) = β₀ + f₁(X₁) + f₂(X₂) + ... + fₖ(Xₖ)
Em que g(μ) é a função de ligação e f₁, f₂, …, fₖ são funções suaves que descrevem a relação não linear entre as variáveis explicativas e a variável dependente. A variável dependente Y pode ser contínua (Normal), dicotômica (Binomial/logística) ou uma contagem (Poisson).

# 16. Modelos Multiníveis (Hierárquicos)

Os modelos multiníveis, também conhecidos como modelos hierárquicos, são uma classe de modelos estatísticos usados para lidar com dados que têm uma estrutura hierárquica ou agrupada. Permitem a análise simultânea de efeitos de nível de grupo e individual em desfechos individuais.
São especialmente úteis quando os dados possuem dependências entre observações dentro de grupos, como alunos em escolas, pacientes em hospitais ou indivíduos em regiões geográficas.
- Equação de nível individual: Yᵢⱼ = b₀ⱼ + b₁ⱼIᵢⱼ + εᵢⱼ  (Yᵢⱼ = desfecho do i-ésimo indivíduo do grupo j)
- Os coeficientes b₀ⱼ (intercepto) e b₁ⱼ (inclinação) variam entre grupos e são modelados em equações de nível de grupo que contêm a parte fixa (γ) e a parte aleatória (U).

Perguntas clássicas respondidas por modelos multinível: Quanto da variação na variável de desfecho é atribuída a diferentes níveis de grupo vs. individuais? Como variáveis de grupo modificam a relação entre variáveis individuais e o desfecho?
No R: lme4::lmer() para desfechos contínuos; lme4::glmer() para desfechos binários ou de contagem.
# 17. Modelos de Séries Temporais

A modelagem de séries temporais é voltada para dados coletados em intervalos de tempo regulares (dias, semanas, meses, anos), com o objetivo de identificar padrões, tendências e sazonalidades ao longo do tempo. É muito útil para monitorar epidemias, taxa de internações, uso de medicamentos ou número de atendimentos em serviços de saúde.
## 17.1 Componentes de uma Série Temporal
- Tendência: mudança contínua (aumento ou diminuição) da série analisada em longo prazo. Pode ser linear ou não linear.
- Sazonalidade: flutuações periódicas e regulares que se repetem em intervalos fixos (mensais, trimestrais, anuais).
- Ciclos: flutuações de longo prazo que não possuem período fixo.
- Ruído (componente irregular): variações aleatórias que não seguem nenhum padrão identificável.

Um conceito importante na modelagem de séries temporais é o de estacionaridade. Uma série é dita estacionária se propriedades estatísticas (como média e variância) permanecem constantes ao longo do tempo. Séries com tendência precisam ser 'tratadas' (diferenciadas) para se tornarem estacionárias.
## 17.2 Modelos Clássicos
### Modelo de Médias Móveis — MA(q)
Modelo linear em que o valor atual de uma série temporal é definido como uma combinação linear dos erros passados (ruído aleatório) mais um termo de média. Denotado por MA(q):
Zₜ = μ + aₜ − θ₁aₜ₋₁ − ... − θqaₜ₋q

### Modelo Autorregressivo — AR(p)
O valor atual da série temporal é explicado como uma combinação linear dos valores passados da própria série. Denotado por AR(p):
Zₜ = φ₁Zₜ₋₁ + ... + φₚZₜ₋ₚ + aₜ

### Modelo ARMA(p,q)
Combinação dos modelos AR(p) e MA(q) — captura tanto a dependência com valores passados quanto com erros passados.
### Modelo ARIMA(p,d,q)
Extensão do ARMA para séries com tendência. O componente de integração (I) torna a série estacionária ao diferenciar os valores (subtrair os valores anteriores) d vezes.
Zₜ = φ₁Zₜ₋₁ + ... + φₚZₜ₋ₚ + aₜ − θ₁aₜ₋₁ − ... − θqaₜ₋q  [após d diferenciações]

### Modelo SARIMA(p,d,q)(P,D,Q)m
Extensão do ARIMA incluindo componentes sazonais. Denotado por SARIMA(p,d,q)(P,D,Q)m, em que P, D e Q são as ordens autorregressiva, de diferenciação e de médias móveis sazonais, respectivamente, e m é o período da sazonalidade (ex.: 12 para dados mensais). No R: forecast::auto.arima(); astsa::sarima().
# 18. Modelos de Sobrevivência

São métodos estatísticos utilizados para analisar o tempo até a ocorrência de um evento de interesse, como morte, recorrência de uma doença, tempo de hospitalização ou qualquer outro desfecho clínico. Ajudam a estimar não apenas a probabilidade de um evento ocorrer, mas também quando ele provavelmente acontecerá.
## 18.1 Componentes Principais
- Evento de interesse: morte, alta hospitalar, recidiva de uma doença, etc.
- Tempo até o evento: variável principal, representando o tempo em dias, meses ou anos até que o evento ocorra.
- Censura: muitos pacientes podem não apresentar o desfecho de interesse até o fim do estudo — são chamados 'censurados'. Esses dados são mantidos na análise até quando se tem informação dos indivíduos. Exemplo: pacientes que não faleceram até o fim do estudo são censurados.

## 18.2 Curva de Kaplan-Meier
Método simples para estimar a probabilidade de sobrevivência ao longo do tempo. Gera uma curva de sobrevivência que mostra a proporção de pacientes que ainda não experimentaram o evento em diferentes pontos do tempo.
Ŝ(t) = ∏_{j: tⱼ ≤ t} (rⱼ − dⱼ) / rⱼ
- tⱼ: conjunto de tempos até o desfecho registrado.
- dⱼ: número de desfechos observados no tempo tⱼ.
- rⱼ: número de indivíduos em risco no tempo tⱼ.

O método assume que a censura é independente do tempo de sobrevivência. Para comparar curvas de sobrevivência entre grupos, aplica-se o Teste Log-Rank. No R: survival::survfit(); survminer::ggsurvplot().
## 18.3 Modelo de Regressão de Cox (Riscos Proporcionais)
Usado para identificar fatores de risco que afetam o tempo de sobrevivência, considerando variáveis preditoras (ex.: idade, sexo, comorbidades). Mede o impacto de cada variável na taxa de risco (hazard rate):
h(t) = h₀(t) · exp(β₁X₁ + β₂X₂ + ... + βₖXₖ)
- Xᵢ: variáveis de risco (idade, sexo, nível educacional, etc.)
- βᵢ: coeficientes estimados para Xᵢ — exp(βᵢ) é interpretado como Hazard Ratio (HR)
- h₀(t): função de risco de linha de base (quando todos os Xs são zero)

O modelo de Cox é semiparamétrico: não faz suposição sobre a forma de h₀(t), mas assume proporcionalidade dos riscos entre grupos ao longo do tempo. No R: survival::coxph().

PARTE IV  GUIA DE SELEÇÃO DE ANÁLISES
# 19. Como Escolher a Análise Adequada

A escolha do método de análise depende da natureza da variável dependente (desfecho), do tipo das variáveis independentes, do delineamento do estudo e das perguntas de pesquisa. O quadro a seguir resume as principais combinações:


# 20. Checklist para Preparação de Pesquisa Científica

Antes de realizar qualquer análise, siga este checklist para garantir que as análises escolhidas sejam adequadas e os resultados, válidos:
## 20.1 Etapa Pré-Análise
- Defina claramente a pergunta de pesquisa e os objetivos (primário e secundários).
- Identifique e classifique as variáveis: variável dependente (desfecho) e variáveis independentes (preditoras/exposições).
- Verifique o tipo de cada variável: qualitativa (nominal/ordinal) ou quantitativa (discreta/contínua).
- Avalie o delineamento do estudo (transversal, coorte, caso-controle, experimental/ensaio clínico).
- Verifique a origem e qualidade dos dados (primários vs. secundários; dados ausentes; outliers).

## 20.2 Análise Exploratória (SEMPRE realizar antes dos modelos)
- Calcule estatísticas descritivas para todas as variáveis: média e DP (quantitativas simétricas) ou mediana e IQ (assimétricas).
- Construa tabelas de frequência para variáveis qualitativas.
- Visualize os dados: histogramas, box plots e gráficos de dispersão.
- Identifique e avalie outliers.
- Avalie dados faltantes (missing data) e decida a estratégia de tratamento.
- Verifique pressupostos de normalidade (histograma, Q-Q plot, Shapiro-Wilk) para guiar a escolha de testes.

## 20.3 Análise Estatística Inferencial
- Escolha o teste ou modelo adequado com base no tipo de desfecho, variáveis e delineamento (use o Guia da Seção 19).
- Formule as hipóteses H₀ e H₁ claramente.
- Defina o nível de significância (α = 5% na maioria dos casos).
- Verifique os pressupostos do teste/modelo escolhido antes de aplicá-lo.
- Execute a análise e interprete os resultados: estatística de teste, p-valor, IC95%, tamanho de efeito.
- Apresente sempre os IC95% e não apenas o p-valor isolado.
- Para múltiplos testes, considere correção para comparações múltiplas (Bonferroni, FDR).

## 20.4 Comunicação dos Resultados
- Apresente estatísticas descritivas em tabelas estruturadas (Tabela 1 de características basais).
- Escolha visualizações adequadas ao tipo de dado e à mensagem que deseja transmitir.
- Evite gráficos que distorçam a percepção (eixos truncados, cores inadequadas, excesso de informação).
- Relate o tamanho amostral, o método de amostragem e o nível de significância adotado na seção de métodos.
- Interprete os resultados no contexto biológico/clínico/epidemiológico — não apenas estatisticamente.


| 💡 ATENÇÃO: Uma variável quantitativa contínua pode ser restruturada como discreta ou mesmo como qualitativa ordinal, dependendo do interesse do analista. Por exemplo, peso (quantitativo contínuo) pode virar faixas de peso (<60 kg, 60–80 kg, >80 kg) — qualitativa ordinal. O rigor na classificação é imprescindível para a escolha correta dos modelos. |
| --- |
| Tipo de Variável | Exemplos |
| --- | --- |
| Qualitativa Nominal | Tipo de doença, cor dos olhos, estado civil |
| Qualitativa Ordinal | Estágio da doença (I, II, III), grau de escolaridade |
| Quantitativa Discreta | Número de internações, contagem de células |
| Quantitativa Contínua | Peso, altura, pressão arterial, IMC |
| 📌 Para que a generalização do resultado obtido na amostra seja válida para a população, a amostra precisa ser representativa, ou seja, deve representar bem a população de interesse. |
| --- |
| PROPRIEDADE: Se yᵢ = xᵢ + c (com c constante), então ȳ = x̄ + c. A soma dos desvios em relação à média é sempre zero: Σ(xᵢ − x̄) = 0. |
| --- |
| Tipo | Divisão | Notação e Exemplo |
| --- | --- | --- |
| Percentil | Grupos de 1% | P₃ = 3% dos dados abaixo; P₅₀ = mediana |
| Decil | Grupos de 10% | D₃ = 30% dos dados abaixo; D₅ = mediana |
| Quartil | Grupos de 25% | Q₁ = 25%; Q₂ = 50% (mediana); Q₃ = 75% |
| Medida de Dispersão | Quando Usar |
| --- | --- |
| Amplitude | Rápida visualização da variação; sensível a outliers |
| Variância (s²) | Base de cálculo; unidade ao quadrado |
| Desvio-Padrão (s) | Dados sem muitos outliers; distribuição simétrica |
| Coeficiente de Variação (CV%) | Comparar variabilidade entre grupos com escalas diferentes |
| Intervalo Interquartil (IQ) | Dados assimétricos ou com outliers; acompanha a mediana |
| ⚠️ O QUARTETO DE ANSCOMBE: Quatro conjuntos de dados completamente diferentes (linear, não linear, com outlier, constante) possuem exatamente as mesmas estatísticas descritivas (média, desvio-padrão, correlação de Pearson = 0,82). Isso demonstra que NUNCA se deve confiar apenas em números — a visualização é obrigatória!

O DATASAURUS: Doze conjuntos de dados aparentemente distintos — incluindo um que forma a imagem de um dinossauro — possuem médias, desvios-padrão e correlações praticamente idênticas. Visualize sempre os dados antes de analisá-los. |
| --- |
| Elemento do Box Plot | Significado | Interpretação |
| --- | --- | --- |
| Linha central da caixa | Mediana (Q₂) | Centro dos dados |
| Limite inferior da caixa | 1º Quartil (Q₁) | 25% dos dados abaixo |
| Limite superior da caixa | 3º Quartil (Q₃) | 75% dos dados abaixo |
| Comprimento da caixa | Intervalo Interquartil (IQ) | Dispersão dos 50% centrais |
| Limite inferior da haste | Q₁ − 1,5 × IQ | Limite para não-outliers |
| Limite superior da haste | Q₃ + 1,5 × IQ | Limite para não-outliers |
| Pontos fora das hastes | Outliers (discrepantes) | Valores extremos |
| TABELAS vs. GRÁFICOS: Transmitir resultados por tabelas permite mostrar os dados de forma acurada e incluir muita informação, contudo tabelas não são consumidas rapidamente. A principal finalidade da visualização de dados é transformar os resultados de forma que seja de fácil consumo, compreensível e útil ao leitor. Use gráficos para comunicar padrões e tendências, e tabelas para reportar valores precisos. |
| --- |
| Conceito | Definição | Exemplo |
| --- | --- | --- |
| Parâmetro (μ, σ, p) | Quantidade desconhecida da população, representada por letras gregas | Média real de IMC de todos os adultos do Rio de Janeiro |
| Estimador | Combinação de elementos da amostra para representar o parâmetro | Média amostral x̄ (estimador de μ) |
| Estimativa | Valor numérico obtido pelo estimador em uma certa amostra | x̄ = 25,7 Kg/m² calculado na amostra |
| Erro Padrão | Desvio-padrão das estimativas entre diferentes amostras; mede a incerteza da estimativa | Erro padrão da média = s / √n |
| INTERPRETAÇÃO CORRETA: Um IC de 95% significa que se obtivermos várias amostras de mesmo tamanho, esperamos que a proporção de intervalos que contêm o valor de μ seja igual a 0,95 (95%). Não significa que existe 95% de chance de o parâmetro estar naquele intervalo específico. |
| --- |
| Tipo de Erro | Definição |
| --- | --- |
| Erro Tipo I (α) | Rejeitar H₀ quando ela é verdadeira (falso positivo). Probabilidade = nível de significância α. |
| Erro Tipo II (β) | Não rejeitar H₀ quando ela é falsa (falso negativo). Probabilidade = β. |
| Poder do Teste (1−β) | Probabilidade de rejeitar H₀ quando a hipótese alternativa é verdadeira. Um teste de maior poder é mais desejável. |
| ⚠️ Pressupostos gerais: normalidade dos dados e independência das observações são pressupostos necessários para os testes paramétricos apresentados a seguir. Verifique sempre se os dados atendem a essas suposições antes de realizar os testes. |
| --- |
| EXEMPLO PRÁTICO: Verificar se a média de IMC de estudantes de pós-graduação está acima do peso (IMC > 25 Kg/m²). Com n=50, x̄=26,4, s=4: t = (26,4 − 25) / (4/√50) = 2,47. Como t > t_crítico = 1,68 (α=5%, unicaudal), rejeita-se H₀. Conclusão: os estudantes estão, em média, acima do peso. |
| --- |
| Teste para Média | Quando Usar |
| --- | --- |
| Teste t — 1 amostra | Comparar média amostral com valor de referência conhecido |
| Teste t — 2 amostras independentes | Comparar médias de dois grupos distintos (ex.: sexo masculino vs. feminino) |
| Teste t — 2 amostras pareadas | Comparar medidas do mesmo indivíduo em dois momentos (antes/depois) |
| ANOVA | Comparar médias de três ou mais grupos simultaneamente |
| Valor de r | Tipo de Correlação | Interpretação |
| --- | --- | --- |
| r = +1 | Linear perfeita positiva | Todos os pontos estão em linha reta ascendente |
| 0 < r < 1 | Linear positiva | À medida que X aumenta, Y tende a aumentar |
| r = 0 | Nenhuma correlação linear | Não há relação linear aparente |
| -1 < r < 0 | Linear negativa | À medida que X aumenta, Y tende a diminuir |
| r = -1 | Linear perfeita negativa | Todos os pontos estão em linha reta descendente |
| ⚠️ CORRELAÇÃO ≠ CAUSALIDADE: Um valor elevado de r não indica necessariamente que uma variável causa mudança na outra. Podem existir outras variáveis não observadas que influenciam ambas (variáveis de confusão). Jamais interprete uma correlação como relação causal sem delineamento experimental adequado. |
| --- |
| Pressuposto | Descrição e Como Verificar |
| --- | --- |
| Linearidade | A relação entre Y e X deve ser linear. Verificar: gráfico de dispersão Y vs X; gráfico de resíduos vs. valores ajustados. |
| Independência | Os erros devem ser independentes entre si. Verificar: delineamento do estudo; teste de Durbin-Watson para séries temporais. |
| Homocedasticidade | A variância dos erros deve ser constante ao longo de todos os valores de X. Verificar: gráfico de resíduos vs. valores ajustados; teste de Breusch-Pagan. |
| Normalidade dos Resíduos | Os resíduos do modelo devem ser normalmente distribuídos. Verificar: Q-Q plot dos resíduos; teste de Shapiro-Wilk. |
| INTERPRETAÇÃO DO OR: Após exponenciar βⱼ, temos a Razão de Chances (OR). OR = 1,93 para inatividade física significa que a chance de a pessoa inaativa fisicamente ter o desfecho de interesse é 1,93 vezes a chance de pessoas ativas. O IC95% do OR permite verificar a significância estatística: se não contiver o valor 1, o OR é significativo a 5%. |
| --- |
| Tipo de Modelo | Variável Dependente / Uso |
| --- | --- |
| Regressão Linear (LM) | Contínua — associação/predição de desfecho numérico |
| Regressão Logística (GLM Binomial) | Binária (sim/não) — OR; prevalência; risco |
| Regressão de Poisson (GLM Poisson) | Contagem de eventos — RR; taxas de incidência |
| Binomial Negativa | Contagem com superdispersão — alternativa ao Poisson |
| GAM | Qualquer tipo — quando a relação é não linear |
| Análise de Sobrevivência | Uso Principal |
| --- | --- |
| Kaplan-Meier | Estimar e descrever graficamente a curva de sobrevivência; comparar grupos com teste Log-Rank |
| Regressão de Cox | Identificar fatores de risco; calcular Hazard Ratios ajustados; controlar confundidores |
| Desfecho (Y) | Variável Independente (X) | Objetivo | Análise Indicada |
| --- | --- | --- | --- |
| Quantitativo contínuo | Nenhuma | Descrever distribuição | Média ± DP; Mediana (IQ); Histograma; Box plot |
| Quantitativo contínuo | Categórica (2 grupos indep.) | Comparar médias | Teste t independente; Mann-Whitney |
| Quantitativo contínuo | Categórica (2 grupos pareados) | Comparar médias (antes/depois) | Teste t pareado; Wilcoxon |
| Quantitativo contínuo | Categórica (≥3 grupos) | Comparar médias | ANOVA + Tukey; Kruskal-Wallis |
| Quantitativo contínuo | Quantitativa | Associação linear | Correlação de Pearson ou Spearman |
| Quantitativo contínuo | Quantitativa(s) | Predição / ajuste | Regressão linear simples ou múltipla |
| Binário (0/1) | Quantitativa(s) / Categórica(s) | OR; probabilidade | Regressão logística (GLM Binomial) |
| Contagem | Quantitativa(s) / Categórica(s) | RR; taxa de incidência | Regressão de Poisson ou Binomial Negativa |
| Tempo até evento | Quantitativa(s) / Categórica(s) | Sobrevivência; HR | Kaplan-Meier; Cox; AFT |
| Qualquer tipo | Hierarquicamente estruturadas | Efeitos fixos e aleatórios | Modelos multinível (lmer/glmer) |
| Qualquer tipo | Quantitativa — relação não linear | Relação não linear | GAM (Modelos Aditivos Generalizados) |
| Série temporal | Tempo | Tendência / previsão | ARIMA; SARIMA; Decomposição STL |
| 💡 LEMBRE-SE: O uso de múltiplas abordagens para responder a uma pergunta na área da saúde deve sempre ser incentivado, pois torna mais robusta a evidência fornecida. Os modelos estatísticos, matemáticos e computacionais fornecem informações distintas e complementares para a compreensão de um fenômeno.

Nunca confie apenas nos números — visualize sempre os dados antes, durante e após a análise estatística (lição do Quarteto de Anscombe e do Datasaurus). |
| --- |