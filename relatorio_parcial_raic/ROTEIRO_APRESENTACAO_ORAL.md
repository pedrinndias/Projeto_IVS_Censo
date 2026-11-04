# Roteiro — apresentação oral RAIC 2026 (v4.1)

**Versão 4.1, 04/11/2026.** Para treinar. O deck `_ENVIO_v4.pptx` não mudou: tudo aqui muda só a fala e a
arguição. Depois de um novo council e de uma nova conferência dos dados (cerca de 125 valores, nenhum
errado), as falas passam a contar as três coisas (sigilo, zeros, lixo), explicam os termos que faltavam,
tratam o 3,14% como cenário e o −0,79 como parte construção, e deixam de dizer que o lixo "será testado".
A arguição ganhou respostas sobre o setor de R$ 170 mil, sigilo e tamanho do setor, setores completos e a
fatorial depois do envio. Entraram o plano de treino e um terceiro corte de emergência.

**Versão 4, 30/10/2026.** Segue o deck `_ENVIO_v4.pptx`, montado sobre a versão que editei à mão:
15 slides, todos na fala (sigilo antes dos zeros, a Tabela 1 e a matriz na sequência, três grafos de
correlação), sem slides de reserva. Falas novas nos slides 6 a 14; a caçamba saiu da fala e virou
pergunta da arguição. Revisada à noite depois do pente fino do council: a Tabela 1 ganhou fala, as
remissões a reservas que não existem saíram e as conclusões passaram a trazer o 50 de 53.

**Versão 3.2, 26/10/2026.** Falas reescritas em primeira pessoa e em tom oral, cada slide com
"Se der branco" e "Passo para", perguntas novas e a lista de números. O Word passou a ser um
roteiro de uso próprio (sem página para a orientadora, sem miniaturas).

**Versão 3.1, 19/10/2026.** Falas revisadas num terceiro council, para o roteiro em Word do
ensaio com a orientadora (`Roteiro_Apresentacao_Oral_RAIC_2026_Pedro.docx`). Nas falas, **negrito**
marca as âncoras e ==trecho== marca o que ainda depende da professora.

**Versão 3, 19/10/2026.** Revisão feita depois de duas checagens:
- os números foram recalculados a partir dos dados brutos do IBGE;
- um segundo council (5 conselheiros, 5 revisões e 1 presidente) avaliou o deck pronto.

A v3 corrige 5 frases imprecisas, põe "Metodologia", "Resultados" e "Conclusões" visíveis,
aplica as mudanças do council e reescreve as falas para soarem faladas, não lidas. A v2 está
no git (commit `0e00a0a`) e a v1 em `historico/`.

**Base:** `Relatorio_Parcial_RAIC_2026_Pedro_corrigido.pdf`. Todo número da fala está no
relatório ou nos dados que o geraram.
**Template:** `APRESENTAÇÃO ORAL.pptx` da Coordic, em 16:9 e Calibri, com os layouts Capa,
Conteúdo e Final.
**Regras:** até 10 min de fala e ~10 min de arguição, com 2 doutores. O prazo de envio foi 02/11/2026.
Levar o mesmo arquivo que foi enviado; se não foi o **`_ENVIO_v4.pptx`**, conferir este roteiro com ele.
**Orçamento:** 15 slides de fala. Os tempos abaixo são calculados a 130 palavras/min, com as
pausas, e somam **9 min 25 s**. É estimativa: só o cronômetro em voz alta confirma. Se o ensaio passar de
9 min 30 s, corte nesta ordem: o slide 11 (esgoto) vira uma frase no 10; a Tabela 1 (slide 8) passa
direto; o slide 12 vira uma frase no 13.

---

## O fio da apresentação

> **A média da cidade esconde o que acontece dentro dela. Hoje mostro a etapa que vem antes
> do índice: o que o Censo 2022 me obrigou a decidir. Os dados me mostraram três coisas, e
> cada uma muda o cálculo.**

O lado humano vem de dois lugares. O primeiro é uma imagem que a plateia completa sozinha:
"duas ruas da mesma cidade". O segundo é o que você aprendeu de verdade: *cada decisão muda o
resultado*. Ninguém é inventado, e nenhum número é inventado.

## Regras de construção dos slides

- **Etiqueta de seção** acima do título: METODOLOGIA (4 e 5), RESULTADOS (6 a 13) e CONCLUSÕES
  (14). Assim o avaliador encontra cada item do edital.
- **O título afirma**, sem ser causal. Uma mensagem por slide.
- **Cada termo técnico é explicado em uma frase**, dentro da fala: assimetria, sigilo,
  correlação, padronizar, análise fatorial.
- **Números para o ouvido:** na fala, "203 milhões", "pouco mais de 104 mil"; o número exato
  fica na tela.
- **Nenhum mapa.** Ainda não há mapas do índice.
- **Decorar só a abertura (slides 1 e 2) e o fecho (fim do 14).** No meio, falar a partir dos
  títulos.

---

## Os slides

### 1. Capa — 20 s · layout Capa
- **Tela:** os campos do template. Título: *Índice de vulnerabilidade à saúde das cidades
  brasileiras: dados do censo demográfico de 2022* · Aluno: Pedro Dias Soares · Orientadora:
  Amanda Cristina de Souza Andrade · Coorientador(a): não se aplica · Grupo de pesquisa: NESPE ·
  Ingresso: 06/03/2026 · Programa: FAPEMIG · Belo Horizonte, 2026.
- **Fala:** "Boa tarde. Eu sou o **Pedro**, bolsista **FAPEMIG** aqui no René Rachou desde março,
  com orientação da professora Amanda Andrade. Vou apresentar um índice de **vulnerabilidade à
  saúde** construído com o **Censo de 2022**."
- **Se der branco:** "Sou o Pedro, e o trabalho é um índice com o Censo 2022."
- **Passo para:** as duas ruas.

### 2. A média da cidade esconde o que acontece dentro dela — 55 s
- **Tela:** à esquerda, o quadrado "média" (1 cidade, 1 número) → a grade de setores, rotulada
  "esquema ilustrativo — não são dados". À direita, quatro definições curtas. **Setor
  censitário:** a menor área com dados do Censo, como um quarteirão ou poucos. **Vulnerabilidade
  à saúde:** condições do lugar (saneamento, renda, escolaridade) que deixam os moradores mais
  expostos a adoecer. **Para quê:** achar, dentro da cidade, as áreas com condições mais
  desfavoráveis (IVS de Belo Horizonte, 2012). **Lacuna:** não havia esse índice com o Censo
  2022 para os municípios estudados.
- **Fala:** "Pensem em **duas ruas** da mesma cidade, uma com esgoto e outra sem. A média da cidade
  junta as duas num número só, e essa diferença some. *(pausa)* A vulnerabilidade à saúde trata
  disso, das **condições do lugar** onde as pessoas moram, como saneamento, renda e escolaridade,
  que deixam quem mora ali mais exposto a adoecer. Para enxergar essas diferenças, o IBGE divide a
  cidade em **setores censitários**, que são um quarteirão ou poucos quarteirões. Em **2012, Belo
  Horizonte** usou esses setores para construir um índice e localizar as áreas com condições piores.
  Com o Censo de 2022, esse índice ainda não existia para as cidades que eu estudo."
- **Se der branco:** "A média esconde, o setor mostra."
- **Passo para:** o projeto e os meus objetivos.

### 3. O projeto quer medir a vulnerabilidade onde ela acontece — 35 s
- **Tela:** objetivo geral do projeto da orientadora (o texto do relatório parcial) ·
  Objetivos específicos: (1) construir o IVS intraurbano, **em andamento**;
  (2) analisar a distribuição espacial, **a iniciar** · Faixa no pé: "Hoje: a etapa que vem
  antes do índice — o que o Censo 2022 me obrigou a decidir".
- **Fala:** "O projeto da professora Amanda quer entender a **desigualdade dentro das cidades**,
  construindo esse índice para cidades brasileiras. Dentro dele, eu tenho **dois objetivos**. O
  primeiro é construir o índice, e isso está em andamento. O segundo, que vem depois, é ver como ele
  se distribui no espaço, em mapas. Então hoje eu não trago o índice pronto. Trago a **etapa
  anterior**, o que o Censo de 2022 me obrigou a decidir antes de calcular."
- **Se der branco:** "Hoje é a etapa antes do índice."
- **Passo para:** as variáveis e os setores.

### 4. METODOLOGIA · Reconstruí o IVS de 2012 com o Censo 2022 nos 70 municípios do ELSI-Brasil — 60 s
- **Tela:** duas colunas com as 7 variáveis (Saneamento · Socioeconômica). Embaixo: "As
  variáveis do IVS 2012 que existem no Censo 2022, com adaptações." À direita, o
  funil: 109.032 → 106.281 → **104.108 setores urbanos · 52,1 milhões de moradores**, e uma linha
  final: "A exclusão rural é desigual: passa de 10% em 29 dos 70 municípios."
- **Fala:** "Usei as variáveis do índice de Belo Horizonte que existem no Censo de 2022, com algumas
  adaptações. Elas se dividem em **duas dimensões**. No saneamento, entram os domicílios com água,
  esgoto e lixo inadequados. Na parte socioeconômica, entram o número de moradores por domicílio, o
  analfabetismo, a renda e a proporção de pessoas pretas, pardas e indígenas. As cidades são as **70
  do ELSI-Brasil**, o estudo de envelhecimento feito aqui no René Rachou. Dos **109 mil** setores,
  tirei os que não têm moradores, os omitidos inteiros por sigilo e os rurais, porque o índice é urbano.
  Ficaram pouco mais de **104 mil**, onde moram 52 milhões de pessoas. No total os rurais são só 2%,
  mas em **29 municípios** eles passam de 10%, e isso entra nas limitações."
- **Se der branco:** "Duas dimensões, 70 cidades, 104 mil setores."
- **Passo para:** a conferência do código.

### 5. METODOLOGIA · Antes de confiar nos dados, conferi o processamento com os números oficiais — 55 s
- **Tela:** **203.080.756** (o código reproduz a população oficial do Brasil, 468.099 setores) ·
  **79,99 × 80,0** (índice de envelhecimento: meu cálculo × IBGE). Uma caixa: "Uma decisão: um
  setor de favela em BH com renda média de R$ 170.418,06 por mês — 55,7 vezes a mediana do
  município. Incoerente com o perfil do setor: retirado da análise descritiva." Rodapé: as outras
  adequações.
- **Fala:** "Antes de olhar qualquer resultado, eu precisava saber se o meu código **lia o Censo
  corretamente**. Então rodei as mesmas rotinas para o Brasil inteiro e comparei com o que o IBGE
  publica. A população bateu exatamente, **203 milhões**. O índice de envelhecimento, que compara
  idosos e crianças, deu **79,99**, e o do IBGE é 80. *(pausa)*
  No caminho também tive que tomar decisões. Um setor de favela em Belo Horizonte aparecia com renda
  média de **170 mil reais** por mês, quase 56 vezes a mediana dos setores da cidade. Esse valor não
  é coerente com o perfil do próprio setor, então tirei esse setor da análise descritiva e
  **registrei o motivo**."
- **Se der branco:** "O código bate com o IBGE, e um setor saiu, com motivo."
- **Passo para:** o dado que falta.

### 6. RESULTADOS · O dado que falta diz alguma coisa — 45 s
- **Visual:** barras de renda mediana do responsável, R$ 2.313,87 onde o analfabetismo existe
  e **R$ 6.092,84** onde ele está sob sigilo. À direita, em destaque: "**16%** dos setores sem o
  dado de analfabetismo". Caixa: "Média observada 3,64%; a real fica entre 3,14% e 3,64%. O
  efeito é pequeno, mas o sigilo não é aleatório."
- **Fala:** "Agora, o que os dados mostraram. São **três coisas**. A primeira é o **sigilo**: quando há muito pouca gente numa categoria, o IBGE omite o número para proteger as pessoas. No analfabetismo, o dado falta em **16%** dos setores. *(pausa)* Onde ele existe, a renda mediana é de uns **2.300 reais**. Onde falta, passa de **6 mil**. O sigilo cai mais nos setores de renda alta. A média observada é de **3,6%**; com um analfabeto em cada setor sem o dado, seria **3,1%**. O efeito é pequeno, mas o dado não falta ao acaso."
- **Se der branco:** "O sigilo cai mais nos setores ricos."
- **Passo para:** os zeros do saneamento.

### 7. RESULTADOS · Só 26% dos setores têm algum domicílio registrado com água inadequada — 45 s
- **Visual:** barras com o % de setores com ao menos um domicílio registrado com o problema, em
  coral: água 26% · esgoto 27% · lixo 37%; em cinza, o resto, "74% · 73% · 63% sem nenhum". À
  direita: "A renda também: média 63% acima da mediana", com mediana R$ 2.572,39 e média
  R$ 4.185,81, e "O que isso muda: na régua de 0 a 1 do índice, quase todos os setores ficariam
  espremidos num canto". Nota pequena: "parte dos zeros vem do sigilo: quando o IBGE suprime só
  algumas parcelas, elas entram como zero".
- **Fala:** "A segunda coisa são os **zeros**. Só **26%** dos setores têm algum domicílio registrado com água inadequada. No esgoto são 27%, e no lixo, 37%. Para a cidade é bom, mas no cálculo quase todos os setores ficam no zero e a distribuição fica **muito assimétrica**. A renda tem o mesmo desequilíbrio. A média, de uns **4.200 reais**, fica **63% acima da mediana**, de uns 2.600, puxada por poucos setores muito ricos. Como o índice coloca tudo na mesma **régua, de zero a um**, quase todos os setores ficariam espremidos num canto dela."
- **Se der branco:** "Poucos setores com o problema, régua espremida."
- **Passo para:** a Tabela 1.

### 8. RESULTADOS · Estatísticas descritivas dos 12 indicadores (Tabela 1) — 30 s
- **Tela:** a Tabela 1 (n, média, mediana, p75, máximo e assimetria dos 12 indicadores); em
  negrito, os 5 complementares, fora do IVS 2012.
- **Fala:** "Esta é a **Tabela 1**: os sete do índice e, em negrito, cinco complementares que eu também analiso. Só duas colunas. A **mediana** é zero nos três de saneamento. A **assimetria**, muitos valores baixos e poucos muito altos, é alta no saneamento e na renda. E o n do analfabetismo, 87 mil setores, é o sigilo."
- **Se der branco:** "Mediana zero, assimetria alta, o n é o sigilo."
- **Passo para:** como as variáveis andam juntas.

### 9. RESULTADOS · Matriz de correlação de Spearman entre os 12 indicadores — 40 s
- **Visual:** a matriz da Figura 1 (n = 75.629), com quadrados nos pares que aparecem nos grafos
  dos slides 10 a 12.
- **Fala:** "Depois, olhei como as variáveis andam juntas, com a **correlação de Spearman**. Perto de um, os dois indicadores ordenam os setores do mesmo jeito. Perto de zero, não têm relação. Negativa, vão em sentidos opostos. Os quadrados são os pares que vêm a seguir. Antes, a **terceira coisa**: olhem a linha do **lixo**. *(pausa)* Com os outros seis do índice, ela fica entre **menos 0,05 e 0,21**. O lixo quase não conversa com o resto."
- **Se der branco:** "Perto de um, mesma ordem; e o lixo quase não se liga."
- **Passo para:** o triângulo.

### 10. RESULTADOS · Renda, cor/raça e analfabetismo andam juntos — 25 s
- **Visual:** os três círculos ligados (0,79 / 0,76 / 0,63). Caixa "Como ler": "As três medem a
  posição social do setor."
- **Fala:** "Renda, cor/raça e analfabetismo ficam entre **0,63 e 0,79**, o que é alto. A renda
  entra **invertida**, para que valor alto signifique mais vulnerabilidade, como nas outras. Então,
  onde a renda é menor, há mais pessoas pretas, pardas e indígenas e mais analfabetismo. As três
  parecem captar a mesma coisa, a **posição social** do setor."
- **Se der branco:** "Três juntas: a posição social."
- **Passo para:** o esgoto.

### 11. RESULTADOS · O esgoto inadequado acompanha esse bloco, mas com força moderada — 25 s
- **Visual:** o mesmo triângulo com o esgoto no centro, ligado às três por 0,42 / 0,42 / 0,40.
- **Fala:** "O **esgoto** inadequado também acompanha esse bloco, mas com força moderada, em torno de **0,4** com cada uma das três. Junto com o que vimos no lixo, isso mostra que o saneamento **não se comporta como um bloco só**. É isso que a **análise fatorial**, a técnica que mostra quais indicadores andam em grupo, testa."
- **Se der branco:** "O esgoto vem junto, mais fraco."
- **Passo para:** idosos e crianças.

### 12. RESULTADOS · Mais idosos onde a renda é maior; mais crianças onde ela é menor — 30 s
- **Visual:** grafo de seis círculos (cor/raça, moradores por domicílio, idosos, renda,
  crianças, analfabetismo), 15 pares; coral tracejado = relação inversa. Idosos × crianças −0,79.
- **Fala:** "Aqui entra o tema do nosso núcleo, o **envelhecimento**. As linhas tracejadas em coral são relações **inversas**. Onde há mais **crianças**, há mais moradores por domicílio, renda menor e mais analfabetismo. Os **idosos** vão no sentido oposto. A relação entre idosos e crianças é de **menos 0,79**, em parte por construção, porque as duas são parcelas da mesma população."
- **Se der branco:** "Crianças com o bloco social, idosos ao contrário."
- **Passo para:** dentro de cada cidade.

### 13. RESULTADOS · Dentro das cidades, renda mais alta anda junto com mais idosos — 30 s
- **Visual:** número grande **50 de 53** (municípios em que a proporção de idosos é maior nos
  setores de renda mais alta; mediana municipal da correlação −0,46). Ao lado: "No conjunto dos
  setores: idosos × renda invertida −0,52 (coral) · crianças × renda invertida +0,62 (teal)".
  Rodapé: "Associação entre áreas, não entre pessoas. Municípios com pelo menos 30 setores com
  dados completos."
- **Fala:** "E isso não é só efeito de juntar cidades diferentes. **Dentro** de cada cidade, os
  setores de renda mais alta têm proporcionalmente mais idosos. Em **50 das 53** cidades em que deu
  para fazer a conta, a relação vai na mesma direção. *(pausa)* Essa associação é **entre áreas, e
  não entre pessoas**, então não permite concluir nada sobre um idoso em particular."
- **Se der branco:** "50 de 53, áreas e não pessoas."
- **Passo para:** as conclusões.

### 14. CONCLUSÕES · Conclusões e próximos passos — 65 s
- **Tela:** à esquerda, **Conclusões**: (1) montar o IVS com o Censo 2022 exige decisões
  explícitas sobre zeros, sigilo e valores extremos; o lixo, que quase não se liga aos outros
  indicadores, será testado na análise fatorial; (2) o sigilo do analfabetismo se concentra nos
  setores mais ricos e precisa de tratamento próprio; (3) em 50 de 53 municípios, os setores de
  renda mais alta têm mais idosos (associação entre áreas). À direita, **Próximos
  passos**: análise fatorial → pesos → faixas de vulnerabilidade → mapas no QGIS → artigo.
  Embaixo, a frase do trabalho e a limitação (estudo ecológico).
- **Fala:** "Resumindo, antes de calcular o índice, os dados me mostraram três coisas que mudam o cálculo. O **sigilo** do analfabetismo precisa de um tratamento próprio. Os **zeros** e os valores extremos precisam de um ajuste antes de as variáveis irem para a mesma régua, que vai ser a de cada município. E o **lixo** entra na **análise fatorial**, que ajuda a definir os pesos. Ela já está em andamento, em discussão com a minha orientadora. Para o nosso núcleo: em **50 de 53** cidades, os idosos estão mais nos setores de renda mais alta. Tudo isso é um **estudo ecológico**, de áreas, e não de pessoas. *(pausa)* O que eu levo desta etapa é que, com dados, **cada decisão muda o resultado**. Por isso cada uma das minhas está justificada e registrada."
- **Se der branco:** "Sigilo, zeros, lixo, fatorial em andamento, 50 de 53, estudo ecológico."
- **Passo para:** o agradecimento.

### 15. Obrigado! — 5 s · layout Final
- **Fala:** "Obrigado. Fico à disposição para as perguntas."

---

## Reserva para a arguição (depois do "Obrigado", fora dos 10 min)

Nenhum slide de reserva: a Tabela 1 e a matriz estão na fala (slides 8 e 9), e as antigas R1, R4, R5
e R6 não estão no deck. As perguntas abaixo se respondem de boca.

## Perguntas prováveis da banca, com respostas curtas

1. **"Cadê o índice?"** Hoje eu trouxe a etapa anterior ao índice. Os zeros, o sigilo e o lixo mudam
   o cálculo, calcular sem tratá-los daria um índice distorcido, e o índice e os mapas são os
   próximos passos. O que reconstruí até aqui foram as dimensões e as variáveis.
2. **"Isso não é falácia ecológica?"** É um estudo ecológico, e as relações são entre áreas. Não
   concluo nada sobre indivíduos, e isso está nas limitações.
3. **"Como mede vulnerabilidade à saúde sem dado de saúde?"** Ele mede condições do lugar que
   influenciam a saúde, como o de 2012. O de 2012 usava óbitos cardiovasculares, mas o Censo 2022
   registra só se houve óbito, sem a causa.
4. **"É comparável com o IVS de 2012?"** São as mesmas dimensões, com adaptações documentadas. O
   analfabetismo agora é a partir de 15 anos (antes era a partir de 5), e a renda média do
   responsável substitui as faixas de salário mínimo, que o Censo 2022 não traz por setor.
5. **"Por que 53 e não 70?"** Para calcular a correlação dentro de cada município, exigi pelo menos
   30 setores com todos os dados. Os municípios pequenos ficam com poucos setores depois do recorte
   urbano e do sigilo.
6. **"Por que tirar o setor de R$ 170 mil, e não os outros?"** Era o maior valor da base, 55,7 vezes
   a mediana do município, num setor de favela com 7% de analfabetismo. Foi uma decisão de julgamento,
   não uma regra automática, e por isso está registrada. A auditoria marcou 65 setores suspeitos, como
   um em Belém, com 43,5 vezes a mediana. Eles ficaram, porque não tenho prova de que o dado está errado.
7. **"A validação com o Brasil prova que os indicadores estão certos?"** Não prova cada indicador.
   Prova que o código lê e soma o Censo como o IBGE.
8. **"E a análise fatorial?"** Curta: está em andamento e em discussão com a minha orientadora, por
   isso não trouxe resultado no slide. Se insistirem, e só com o OK da Amanda: depois do envio, com
   corte de carga menor que 0,4, o lixo e a moradia não convencional saíram em todas as rotações. O que
   isso muda no índice ainda é decisão da orientadora.
9. **"Por que padronizar dentro de cada município?"** O índice é intraurbano, então a régua é a
   própria cidade, como no IVS de Belo Horizonte, que foi calculado para um só município. O custo é
   que ele mostra a posição do setor na cidade e não compara o nível entre cidades.
10. **"Cor/raça como variável de vulnerabilidade?"** Entra como marcador de desigualdade social
   estrutural, como no IVS de 2012.
11. **"E as diferenças entre regiões?"** A água inadequada é 16 vezes maior nos municípios do Norte
   que nos do Sul, mas o Norte tem só 6 municípios, então isso descreve a amostra, não a região.
12. **"Por que o lixo fica à parte?"** Ele quase não se liga aos outros indicadores, e é isso que a
   análise fatorial examina (pergunta 8). Tenho uma hipótese. Seguindo o IVS de 2012, conto a
   caçamba, o contêiner coletivo, como destino inadequado, e o Censo só registra o destino. A
   caçamba pode refletir o modo de coleta da cidade, não a vulnerabilidade.
13. **"O sigilo vira ausente ou zero?"** Depende de quanto foi escondido. Se o IBGE suprimiu todo o
   numerador, o indicador fica ausente. Se suprimiu só algumas parcelas, elas entram como zero, e
   isso subestima um pouco os valores. O sem banheiro também tem sigilo: são 91.912 setores com o dado.
14. **"O sigilo depende da renda ou do tamanho do setor?"** Dos dois. Ele cai de 29% nos setores menores
   para 4% nos maiores. Mas, em setores de tamanho parecido, de 421 a 478 moradores, vai de 1% nos mais
   pobres a 47% nos mais ricos. A renda pesa mesmo controlando o tamanho.
15. **"O 3,14% é um limite?"** Não, é um cenário: supõe um analfabeto em cada setor sem o dado. Serve para
   mostrar que o efeito sobre a média é pequeno.
16. **"O −0,79 entre idosos e crianças não é só matemática?"** Em parte, sim. As duas são parcelas da mesma
   população, então não leio esse número como achado. O achado é a relação de cada uma com a renda.
17. **"As correlações usam só 73% dos setores?"** Sim, os 75.629 com os 12 indicadores completos. Faltam
   dois grupos opostos: sem analfabetismo, de renda mais alta, e sem banheiro, mais pobres. É uma
   limitação. Com os pares completos, a faixa do lixo quase não muda.
18. **"Por que o −0,46 é negativo, se a renda alta anda com mais idosos?"** Porque a renda entra invertida:
   valor alto quer dizer renda baixa. O sinal negativo diz que mais idosos andam com renda mais alta.

---

## Números que não posso errar

- Saneamento: água 26%, esgoto 27%, lixo 37% dos setores com algum domicílio registrado com o
  problema (74%, 73% e 63% sem nenhum).
- Renda: mediana R$ 2.572,39, média R$ 4.185,81 (63% acima).
- Sigilo no analfabetismo: 16% dos setores; renda mediana R$ 2.313,87 com o dado e R$ 6.092,84 sem;
  média observada 3,64%; 3,14% no cenário de um analfabeto por setor; sigilo de 29% a 4% do menor ao
  maior tamanho de setor.
- Correlações: renda, cor/raça e analfabetismo de 0,63 a 0,79; esgoto com as três, 0,40 a 0,42;
  lixo com os outros 6 do IVS, de −0,05 a 0,21; idosos × crianças −0,79 (em parte por construção).
- Idosos e renda: 50 de 53 municípios.
- Validação: 203.080.756 pessoas; índice de envelhecimento 79,99 contra 80.
- Recorte: 109.032 → 104.108 setores, 52,1 milhões de moradores; 29 municípios com mais de 10% de rurais.
- Setor retirado: R$ 170.418,06, 55,7 vezes a mediana do município; 65 setores suspeitos ficaram.

---

## Plano de treino

- Hoje, 04/11: mandar à Amanda a frase da pergunta 8 e pedir o OK; sem resposta, usar só a versão curta.
  Confirmar qual arquivo foi enviado.
- 05/11: decorar a abertura (slides 1 e 2) e o fim do 14; depois uma fala inteira, em voz alta, com
  cronômetro.
- 06/11: arguição: alguém faz sem aviso as perguntas 1, 6, 8, 14, 15, 16 e 17.
- 07/11: simulação completa gravada, com um ouvinte de fora da área. Alvo de 8 a 9,5 min.
- 08/11: revisão leve: frases-chave, "Se der branco", os três cortes e os números. Nada novo.

---

## Antes do evento

- [ ] Confirmar com a orientadora o "Programa de vínculo: FAPEMIG" e o "Coorientador(a): não se
  aplica" da capa, e até onde falar da fatorial (pergunta 8).
- [ ] Confirmar que o arquivo enviado à Coordic foi o `_ENVIO_v4.pptx`.
- [ ] Levar o arquivo em pen drive e neste roteiro impresso.
- [ ] Se ficar abaixo de 8 min no ensaio, desacelerar e fazer as pausas; não acrescentar conteúdo.
