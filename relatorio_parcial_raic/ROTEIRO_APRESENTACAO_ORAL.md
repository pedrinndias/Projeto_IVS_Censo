# Roteiro — apresentação oral RAIC 2026 (v3)

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
**Regras:** até 10 min de fala e ~10 min de arguição, com 2 doutores. Envio até 02/11/2026 (é
Finados, então mirar sexta, 30/10). No assunto do e-mail: "Pedro Dias Soares – Oral". Enviar o
arquivo **`_ENVIO.pptx`**, que vai sem as notas.
**Orçamento:** 11 slides de fala, com 999 palavras. Os tempos abaixo são calculados a 130
palavras/min, com as pausas, e somam **8 min 15 s**. Em ritmo lento (110 palavras/min) dá cerca de
9 min, dentro dos 10. Mais 7 slides de reserva.

---

## O fio da apresentação

> **A média da cidade esconde o que acontece dentro dela. Hoje mostro a etapa que vem antes
> do índice: o que o Censo 2022 me obrigou a decidir. Os dados me mostraram três coisas, e
> cada uma muda o cálculo.**

O lado humano vem de dois lugares. O primeiro é uma imagem que a plateia completa sozinha:
"duas ruas da mesma cidade". O segundo é o que você aprendeu de verdade: *cada decisão muda o
resultado*. Ninguém é inventado, e nenhum número é inventado.

## Regras de construção dos slides

- **Etiqueta de seção** acima do título: METODOLOGIA (4 e 5), RESULTADOS (6 a 9) e CONCLUSÕES
  (10). Assim o avaliador encontra cada item do edital.
- **O título afirma**, sem ser causal. Uma mensagem por slide.
- **Cada termo técnico é explicado em uma frase**, dentro da fala: assimetria, sigilo,
  correlação, padronizar, análise fatorial.
- **Números para o ouvido:** na fala, "203 milhões", "pouco mais de 104 mil"; o número exato
  fica na tela.
- **Nenhum mapa.** Ainda não há mapas do índice.
- **Decorar só a abertura (slides 1 e 2) e o fecho (fim do 10).** No meio, falar a partir dos
  títulos.

---

## Os slides

### 1. Capa — 15 s · layout Capa
- **Tela:** os campos do template. Título: *Índice de vulnerabilidade à saúde das cidades
  brasileiras: dados do censo demográfico de 2022* · Aluno: Pedro Dias Soares · Orientadora:
  Amanda Cristina de Souza Andrade · Coorientador(a): não se aplica · Grupo de pesquisa:
  **[A CONFIRMAR, porque NESPE é o núcleo]** · Ingresso: 06/03/2026 · Programa: FAPEMIG ·
  Belo Horizonte, 2026.
- **Fala (decorar):** "Boa tarde. Eu sou o Pedro, bolsista FAPEMIG aqui no René Rachou desde
  março, orientado pela professora Amanda Andrade. Vou falar de um índice de vulnerabilidade à
  saúde feito com o Censo de 2022."

### 2. A média da cidade esconde o que acontece dentro dela — 55 s
- **Tela:** à esquerda, o quadrado "média" (1 cidade, 1 número) → a grade de setores, rotulada
  "esquema ilustrativo — não são dados". À direita, quatro definições curtas. **Setor
  censitário:** a menor área com dados do Censo, como um quarteirão ou poucos. **Vulnerabilidade
  à saúde:** condições do lugar (saneamento, renda, escolaridade) que deixam os moradores mais
  expostos a adoecer. **Para quê:** achar, dentro da cidade, as áreas com condições mais
  desfavoráveis (IVS de Belo Horizonte, 2012). **Lacuna:** não havia esse índice com o Censo
  2022 para os municípios estudados.
- **Fala (decorar):** "Pensem em duas ruas da mesma cidade: numa tem esgoto, na outra não. A
  média da cidade junta as duas num número só e esconde essa diferença. *(pausa)* É disso que
  trata a vulnerabilidade à saúde. São as condições do lugar onde a gente mora, como saneamento,
  renda e escolaridade, que deixam as pessoas mais expostas a adoecer. Para enxergar isso, o
  IBGE divide a cidade em setores censitários. Pensem num quarteirão, ou em poucos quarteirões.
  Em 2012, Belo Horizonte usou esses setores para criar um índice e achar as áreas com
  condições piores. Com o Censo de 2022, esse índice ainda não existia para as cidades que eu
  estudo."

### 3. O projeto quer medir a vulnerabilidade onde ela acontece — 40 s
- **Tela:** objetivo geral do projeto da orientadora, **[texto literal da Amanda — A
  CONFIRMAR]** · Meus objetivos: (1) construir o IVS intraurbano, **em andamento**;
  (2) analisar a distribuição espacial, **a iniciar** · Faixa no pé: "Hoje: a etapa que vem
  antes do índice — o que o Censo 2022 me obrigou a decidir".
- **Fala:** "O projeto da professora Amanda tem como objetivo *(objetivo geral — A
  CONFIRMAR)*. Dentro dele, eu tenho dois objetivos. O primeiro é construir esse índice, e está
  em andamento. O segundo é ver como ele se distribui no espaço, em mapas, e vem depois. Então
  hoje eu não vou mostrar o índice pronto. Vou mostrar a etapa que vem antes dele: o que o
  Censo de 2022 me obrigou a decidir, e como cada decisão muda o resultado."

### 4. METODOLOGIA · Reconstruí o IVS de 2012 com o Censo 2022 nos 70 municípios do ELSI-Brasil — 55 s
- **Tela:** duas colunas com as 7 variáveis (Saneamento · Socioeconômica). Embaixo: "As
  variáveis do IVS 2012 que existem no Censo 2022, com adaptações (reserva R1)." À direita, o
  funil: 109.032 → 106.281 → **104.108 setores urbanos · 52,1 milhões de moradores**, e uma linha
  final: "A exclusão rural é desigual: passa de 10% em 29 dos 70 municípios (R6)."
- **Fala:** "Usei as variáveis do índice de Belo Horizonte que existem no Censo de 2022, com
  algumas adaptações. São duas dimensões. No saneamento, água, esgoto e lixo inadequados. Na
  parte socioeconômica, quantas pessoas moram por domicílio, analfabetismo, renda e a proporção
  de pessoas pretas, pardas e indígenas. As cidades são as 70 do ELSI-Brasil, o estudo de
  envelhecimento feito aqui no René Rachou. Comecei com 109 mil setores. Tirei os que não têm
  moradores, os que o IBGE escondeu por sigilo e os rurais, porque o índice é urbano. Ficaram
  pouco mais de 104 mil setores, onde moram 52 milhões de pessoas. No total, os rurais são só
  2% dos setores, mas em 29 municípios passam de 10%. Isso entra nas limitações."

### 5. METODOLOGIA · Antes de confiar nos dados, conferi o processamento com os números oficiais — 55 s
- **Tela:** **203.080.756** (o código reproduz a população oficial do Brasil, 468.099 setores) ·
  **79,99 × 80,0** (índice de envelhecimento: meu cálculo × IBGE). Uma caixa: "Uma decisão: um
  setor de favela em BH com renda média de R$ 170.418,06 por mês — 55,7 vezes a mediana do
  município. Incoerente com o perfil do setor: retirado da análise descritiva." Rodapé: as outras
  adequações (R1).
- **Fala:** "Antes de olhar qualquer resultado, eu precisava saber se o meu código lia o Censo
  direito. Rodei as mesmas rotinas no Brasil inteiro e comparei com o que o IBGE publica. A
  população bateu até a última pessoa: 203 milhões. O índice de envelhecimento deu 79,99, e o
  do IBGE é 80. No caminho apareceram decisões. Uma delas foi um setor de favela em Belo
  Horizonte com renda média de 170 mil reais por mês, quase 56 vezes a mediana da cidade. Não
  combina com o próprio setor, então tirei esse setor da análise descritiva. *(pausa)* Aí caiu
  a ficha: cada decisão muda o resultado. Por isso cada uma precisa ser justificada e
  registrada."

### 6. RESULTADOS · Em 74% dos setores, nenhum domicílio foi registrado com água inadequada — 55 s
- **Visual:** barras com o % de setores sem nenhum domicílio registrado com o problema: água 74%
  · esgoto 73% · lixo 63%. À direita: "A renda também: média 63% acima da mediana" e "O que isso
  muda: na régua de 0 a 1 do índice, quase todos os setores ficariam espremidos num canto". Nota
  pequena: "parte dos zeros vem de parcelas suprimidas pelo IBGE".
- **Fala:** "Agora, o que os dados me mostraram. Primeiro: em 74% dos setores, nenhum
  domicílio foi registrado com água inadequada. No esgoto são 73%, e no lixo, 63%. Parte desses
  zeros vem do sigilo do IBGE. Para a cidade é uma boa notícia, mas para o método é um problema.
  Quando quase tudo é zero e poucos setores concentram o problema, a distribuição fica torta. A
  renda faz o mesmo: a média fica 63% acima da mediana, porque poucos setores muito ricos puxam
  a média para cima. O índice vai pôr todas as variáveis na mesma régua, de zero a um. Com
  tantos zeros, quase todos os setores ficariam espremidos num canto dessa régua. Isso precisa
  ser tratado antes do cálculo."

### 7. RESULTADOS · O dado que falta também diz alguma coisa — 55 s
- **Visual:** barras de renda mediana do responsável, R$ 2.313,87 onde o analfabetismo existe
  e **R$ 6.092,84** onde ele está sob sigilo. À direita, em destaque: "**16%** dos setores sem o
  dado de analfabetismo". Caixa: "Média observada 3,64%; a real fica entre 3,14% e 3,64%. O
  efeito é pequeno, mas o sigilo não é aleatório."
- **Fala:** "Segundo achado. Quando um setor tem pouquíssima gente numa categoria, o IBGE
  esconde o número, para ninguém ser identificado. É o sigilo. No analfabetismo, o dado sumiu em
  16% dos setores. E que setores são esses? *(pausa)* Onde o dado existe, a renda mediana é de
  uns 2.300 reais. Onde ele sumiu, passa de 6 mil. O IBGE esconde justamente onde há poucos
  analfabetos, que são os setores mais ricos. Sem esses setores, a média que eu observo é 3,6%,
  e a real fica entre 3,1 e 3,6. O efeito é pequeno, mas mostra que esse dado não sumiu por
  acaso. Ele precisa de um tratamento próprio."

### 8. RESULTADOS · Renda, cor/raça e analfabetismo andam juntos; o lixo anda sozinho — 50 s
- **Visual:** os três círculos ligados (0,79 / 0,76 / 0,63) e o lixo afastado (−0,05 a 0,21).
  Régua: "correlação: 0 = nenhuma relação; 1 = mesma ordem". Caixa: "Hipótese a testar: seguindo
  o IVS 2012, o projeto conta a caçamba como destino inadequado (o Censo só registra o destino).
  A caçamba pode refletir o jeito de coletar da cidade, não a vulnerabilidade."
- **Fala:** "Terceiro achado. Medi como as variáveis andam juntas, com uma correlação que vai de
  zero, quando não há relação, a um, quando duas variáveis ordenam os setores do mesmo jeito.
  Renda, cor/raça e analfabetismo ficam entre 0,63 e 0,79. É alto. As três parecem medir a mesma
  coisa: a posição social do setor. Já o lixo quase não se relaciona com nada. Tenho uma
  hipótese, que ainda vou testar. Seguindo o índice de 2012, eu conto a caçamba como destino
  inadequado do lixo. Só que a caçamba pode ter mais a ver com o jeito de coletar de cada cidade
  do que com vulnerabilidade."

### 9. RESULTADOS · Dentro das cidades, renda mais alta anda junto com mais idosos — 40 s
- **Visual:** número grande **50 de 53** (municípios em que a proporção de idosos é maior nos
  setores de renda mais alta; mediana municipal da correlação −0,46). Ao lado: "No conjunto dos
  setores: idosos × renda invertida −0,52 · crianças × renda invertida +0,62". Rodapé:
  "Associação entre áreas, não entre pessoas. Municípios com pelo menos 30 setores com dados
  completos." O "16×" do Norte × Sul foi para a reserva R4.
- **Fala:** "E aqui aparece o tema do nosso núcleo, o envelhecimento. Nos setores de renda mais
  alta há, proporcionalmente, mais idosos. Nos de renda mais baixa, mais crianças. E isso não é
  só diferença entre cidades. Dos 53 municípios em que deu para calcular dentro da cidade, em 50
  a relação vai nessa direção. *(pausa)* Um cuidado importante: é uma associação entre áreas,
  não entre pessoas. Não dá para tirar daí conclusão sobre um idoso em particular."

### 10. CONCLUSÕES · Conclusões e próximos passos — 70 s
- **Tela:** à esquerda, **Conclusões**: (1) montar o IVS com o Censo 2022 exige decisões
  explícitas sobre zeros, sigilo e valores extremos; (2) o sigilo se concentra nos setores mais
  ricos e precisa de tratamento próprio; (3) o lixo se comporta à parte e será testado na análise
  fatorial. À direita, **Próximos passos**: análise fatorial **[frase A CONFIRMAR com a
  Amanda]** → pesos → faixas de vulnerabilidade → mapas no QGIS → artigo. Embaixo, a frase do
  trabalho e a limitação (estudo ecológico).
- **Fala:** "Para fechar. Eu queria um índice que enxergasse dentro da cidade, e antes de
  calcular os dados me mostraram três coisas que mudam o cálculo. Os zeros pedem um tratamento
  antes de pôr tudo na mesma régua, e essa régua vai ser a de cada município, como em Belo
  Horizonte. O sigilo pede um tratamento próprio para os dados que faltam. E o lixo vai ser
  testado na análise fatorial, uma técnica que mostra quais variáveis medem a mesma coisa e
  ajuda a definir o peso de cada uma. *(frase sobre a análise fatorial — A CONFIRMAR)* Depois
  vêm as faixas de vulnerabilidade e os mapas. Uma limitação acompanha tudo: é um estudo
  ecológico, com dados de áreas, não de pessoas. *(pausa)* **(decorar)** O que eu levo até aqui
  é isto: com dados, cada decisão muda o resultado. Por isso, cada uma está justificada e
  registrada."

### 11. Obrigado(a)! — 5 s · layout Final
- **Fala:** "Obrigado. Fico à disposição para as perguntas."

---

## Reserva para a arguição (depois do "Obrigado", fora dos 10 min)

| # | Slide | Pergunta que ele responde |
|---|---|---|
| R1 | As adequações ao Censo 2022, com os códigos das variáveis | "Como as variáveis de 2012 foram reconstruídas?" |
| R2 | Matriz de Spearman completa (12 indicadores, n = 75.629) | "E as correlações dos complementares?" |
| R3 | Tabela 1 completa | "Quais são as descritivas?" |
| R4 | Médias por região (o 16× da água, Norte × Sul, está aqui) | "E as diferenças regionais? Dá para generalizar?" |
| R5 | O setor de R$ 170.418,06 | "Por que tirar só esse setor?" |
| R6 | Critério dos 53 municípios e a exclusão rural desigual | "Por que 53, se são 70?" |
| R7 | Análise fatorial — **só se a Amanda autorizar** | "E a análise fatorial?" |

## Perguntas prováveis da banca, com respostas curtas

1. **"E o índice? Cadê o resultado?"** Esta é a etapa que vem antes do índice. Os três achados
   mudam o cálculo, e calcular sem tratá-los daria um índice distorcido. O índice e os mapas
   são os próximos passos.
2. **"Isso não é falácia ecológica?"** É um estudo ecológico, e as relações são entre áreas.
   Eu não concluo nada sobre indivíduos; isso está nas limitações.
3. **"Como você sabe que o índice mede vulnerabilidade à saúde, sem dado de saúde?"** Ele
   mede condições do lugar que influenciam a saúde, como o de 2012. O de 2012 tinha um
   coeficiente de óbitos cardiovasculares, mas o Censo 2022 registra só se houve óbito, sem a
   causa.
4. **"É comparável com o IVS de 2012?"** São as mesmas dimensões, com adaptações
   documentadas: o analfabetismo é a partir de 15 anos (em 2012 era a partir de 5), e a renda
   média do responsável substitui as faixas de salário mínimo, que o Censo 2022 não traz por
   setor (R1).
5. **"Por que 53 e não 70?"** Para calcular a correlação dentro de cada município, adotei o
   mínimo de 30 setores com todos os dados. Alguns municípios pequenos ficam com poucos setores
   depois do recorte urbano (R6).
6. **"Por que tirar o setor de R$ 170 mil?"** A renda média dele é 55,7 vezes a mediana do
   município, num setor de favela com 7% de analfabetismo. Só esse saiu, e os demais extremos
   ficaram (R5).
7. **"A validação com o Brasil prova que os indicadores estão certos?"** Não prova cada
   indicador. Prova que o código lê e soma o Censo como o IBGE.
8. **"Por que padronizar dentro de cada município?"** O índice é intraurbano: a régua é a
   própria cidade, como no IVS de Belo Horizonte, calculado para um só município.
9. **"Cor/raça como variável de vulnerabilidade?"** Ela entra como marcador de desigualdade
   social estrutural, como no IVS de 2012.
10. **"E a análise fatorial?"** Responder com a frase combinada com a Amanda. Se houver
    autorização, mostrar R7.

---

## Antes do envio

- [ ] **Hoje:** mandar à Amanda uma mensagem única pedindo até 23/10: (a) o grupo de pesquisa;
  (b) o texto do objetivo geral do projeto; (c) a frase sobre a análise fatorial, com ou sem
  números, mesmo que só na reserva; (d) se "Coorientador(a): não se aplica" serve. Sem resposta,
  usar o provisório: NESPE, o objetivo do relatório, "análise fatorial em andamento, sem
  resultados apresentados" e tirar a R7.
- [ ] Trocar os 4 A CONFIRMAR no gerador e rodar de novo. Conferir que não sobrou marca-texto
  amarelo no `_ENVIO.pptx`.
- [ ] Confirmar com a Coordic se os slides de reserva depois do "Obrigado" podem ir no arquivo.
- [ ] Ensaiar duas vezes com cronômetro, uma delas gravada, com um ouvinte de fora da área. O
  alvo é de 7 a 9 min. Se ficar abaixo de 7, desacelere e faça as pausas; não acrescente
  conteúdo.
- [ ] Ensaiar a arguição: alguém faz as perguntas 1, 2, 5 e 7 sem aviso.
