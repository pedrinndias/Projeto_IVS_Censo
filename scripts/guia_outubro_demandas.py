"""Texto do guia: as demandas de setembro, slide a slide (Parte C).

Não gera nada sozinho: é lido por scripts/gerar_pdf_guia_decks_outubro.py. Um verbete por slide,
na ordem do deck; `titulo` tem de aparecer no slide de mesmo número (o gerador confere). Todos os
números chegam em N, calculados dos mesmos CSVs que o deck lê.
"""


def abertura(N):
    return f"""O deck das demandas de setembro é a prestação de contas das últimas tarefas pedidas pela
orientadora: as onze demandas de setembro e os nove itens que vieram em seguida. Ele vai do pedido à
decisão, em dez partes: o que foi pedido e como foi lido; o ponto de partida (o NB04); as demandas 1 e 2;
a fatorial ampliada (demandas 3 e 5 a 11); a revisão da apresentação (demanda 4); os testes seguintes e o
banheiro graduado; a grade do IVS final ({N.n_esp} especificações); o que o índice acrescenta à renda; a
referência proposta e por que desconfiar dela; e o que fica para a orientadora decidir.

Este é o deck mais técnico dos dois. Se ainda não leu a Parte A, leia antes as seções A.5 (índice
composto), A.6 (análise fatorial), A.7 (validação) e A.9 (especificação e grade)."""


def verbetes(N):
    return [
        dict(n=1, titulo="As demandas de setembro",
             frase="A capa: o deck responde às últimas demandas da orientadora, do pedido aos números, e deixa as escolhas de método com ela.",
             mostra="""A identificação do projeto no alto, o título "As demandas de setembro" e um subtítulo que resume o
deck: o que foi pedido, como cada pedido foi lido, o que foi feito e o que os números dizem — da fatorial
ampliada ao IVS final do Notebook 05. A última frase do subtítulo é a mais importante: as escolhas de
método ficam com a orientadora, com os números ao lado de cada uma.""",
             zero="""Uma <b>demanda</b> é um pedido de análise feito pela orientadora. Em setembro foram onze, e depois vieram
mais nove itens de teste. O deck não toma as decisões de método: mostra o que cada opção muda. O
<b>Notebook 05</b> (NB05) é o notebook que calcula o IVS final.""",
             apresentar="""“Este deck responde às demandas de setembro: o que foi pedido, como eu li cada pedido, o que foi feito
e o que os números mostram. No fim, ficam as escolhas que são suas, cada uma com os números.”"""),

        dict(n=2, titulo="O roteiro",
             frase="As dez partes do deck, na ordem em que cada resposta prepara a seguinte.",
             mostra="""Uma tabela de dez linhas: o número da parte, o nome e o que ela responde.""",
             zero=f"""A ordem segue uma lógica de argumento:

• primeiro, <b>o que foi pedido</b> e como cada pedido ambíguo foi interpretado (parte 1);
• depois, <b>o ponto de partida</b>: o índice que já existia, o do NB04 (parte 2);
• em seguida, as <b>respostas</b>: renda e quadro (parte 3), a fatorial ampliada (parte 4), a revisão da
apresentação (parte 5) e os testes seguintes (parte 6);
• então, a <b>síntese</b>: todas as combinações de escolhas numa grade de {N.n_esp} especificações (parte 7)
e o que o índice acrescenta à renda (parte 8);
• por fim, a <b>proposta</b> e o <b>que falta decidir</b> (partes 9 e 10).""",
             apresentar="""“São dez partes. Começo pelo pedido e pelo ponto de partida, passo pelas respostas a cada demanda,
junto tudo numa grade de especificações e termino nas escolhas que ficam com você.”"""),

        dict(n=3, titulo="O pedido e como foi lido",
             frase="A divisória da parte 1: as onze demandas e os nove pontos que admitiam mais de uma leitura.",
             mostra="""O número 1 em vermelho, o título "O pedido e como foi lido" e o subtítulo: onze demandas de setembro;
nove pontos com mais de uma leitura.""",
             zero="""Pedido de análise raramente é preciso o bastante para virar conta sem interpretação. Esta parte deixa
explícito como cada pedido foi lido — para que a orientadora possa corrigir a leitura antes de discutir
os números.""",
             apresentar="""“A primeira parte é o pedido, e como eu o interpretei.”"""),

        dict(n=4, titulo="As onze demandas",
             frase="As onze demandas de setembro, o estado de cada uma — todas feitas — e onde está o resultado.",
             mostra="""Uma tabela de onze linhas com quatro colunas: o número da demanda, o que foi pedido, o estado e onde
está o resultado (um arquivo ou um cenário).""",
             zero=f"""As onze demandas, em palavras simples:

• <b>1. Coluna de renda com a mediana</b>: trocar a renda do setor extremo de Belo Horizonte pela mediana
(Parte A, A.5) e entregar isso como uma coluna nova.
• <b>2. Quadro de indicadores</b>: uma tabela única com todos os indicadores, como cada um é calculado e de
que arquivo vem ({N.n_ind} indicadores).
• <b>3. Fatorial sem bootstrap, sem e com rotação</b>: refazer a análise fatorial mostrando lado a lado a
solução sem rotação e as com rotação, e sem o bootstrap (A.8).
• <b>4. Separar o útil do inútil</b>: revisar a apresentação principal, tirando o que não serve.
• <b>5. Comparar o "não chega"</b>: comparar a variável de água que não chega encanada ao domicílio com as
outras categorias de água e com os indicadores do índice.
• <b>6. Juntar o "sem banheiro"</b>: reunir as categorias de falta de banheiro numa variável só.
• <b>7. Acrescentar canalização e sem banheiro</b>: pôr essas variáveis novas na análise fatorial.
• <b>8. A fatorial de "tudo isso"</b>: uma análise com todas as variáveis novas juntas.
• <b>9. Habitação convencional</b>: incluir a variável de tipo de moradia.
• <b>10. Testar o lixo</b>: ver o que muda com e sem o lixo.
• <b>11. Testar as duas rotações</b>: Varimax e promax lado a lado (A.6).

Cada demanda virou um ou mais <b>cenários</b> — conjuntos de variáveis — chamados de S0 a S7, explicados no
slide 13.""",
             apresentar="""“As onze demandas estão feitas. A tabela diz onde está cada resultado; a maioria virou um cenário da
análise fatorial ampliada, que eu mostro na parte 4.”""",
             perguntas=[("Por que a demanda 6 diz “a graduada em 26/09”?", "Porque juntar o “sem banheiro” tinha duas leituras: usar a variável que já é a soma (V00495) ou criar uma versão em graus, que exigia extrair uma variável nova do Censo (V00237). A primeira foi feita em 25/09; a segunda, no dia seguinte.")]),

        dict(n=5, titulo="Como li o que tinha mais de uma leitura",
             frase="Nove pontos ambíguos e a leitura adotada em cada um, enquanto a orientadora não responde.",
             mostra="""Uma tabela de nove linhas: o ponto (com o número da demanda) e a leitura adotada.""",
             zero=f"""Cada ponto, explicado:

• <b>Renda (demanda 1)</b>: "a mediana" de quê? A mediana da renda dentro do próprio setor não existe nos
dados publicados. A leitura adotada: uma coluna nova em que o setor extremo recebe a mediana de Belo
Horizonte sem ele ({N.med_bh}); as alternativas ficam registradas.
• <b>Rotação (demanda 3)</b>: qual rotação? As duas, e também a solução sem rotação, lado a lado.
• <b>"Comparar com os outros" (demanda 5)</b>: comparar com o quê? As duas leituras: com as outras
categorias de canalização da água e com os indicadores do índice.
• <b>Juntar "sem banheiro" (demanda 6)</b>: usar a `V00495`, que já contém a `V00238`; a versão em graus
exigia extrair a `V00237`.
• <b>Habitação convencional (demanda 9)</b>: entra virada para o lado da vulnerabilidade — a proporção de
moradias <i>não</i> convencionais —, sem ser excluída por variar pouco.
• <b>"Tudo isso" (demanda 8)</b>: o IVS-7 mais as quatro variáveis novas.
• <b>Repartição oblíqua</b>: na promax há duas matrizes (A.6); as duas são mostradas, sem dizer qual é "a
certa".
• <b>Renda no índice</b>: os cenários rodam com as três versões da renda; a escolha é da orientadora.
• <b>Incerteza</b>: sensibilidade por município em vez de bootstrap (A.8).""",
             apresentar="""“Nove pontos tinham mais de uma leitura. Em cada um, segui a leitura que está na tabela, e ela pode ser
trocada sem refazer o trabalho: basta mudar o parâmetro do cenário e rodar de novo.”""",
             perguntas=[("E se a orientadora tinha outra leitura em mente?", "Então troca-se a leitura. Todas as análises são geradas por programa a partir de parâmetros; mudar uma leitura é mudar um parâmetro e rodar de novo.")]),

        dict(n=6, titulo="Como o trabalho foi feito",
             frase="As dez fases do trabalho em três dias: seis em 25/09, duas em 26/09 e duas em 27/09.",
             mostra="""Uma página de diário com seis entradas: 25/09 (Fase 0; Fases 1 e 2; Fases 3 e 4; Fase 5), 26/09 (Fases A e
B) e 27/09 (Fases C e D).""",
             zero="""O trabalho foi dividido em fases, cada uma com um arquivo de estado que registra o que foi feito:

• <b>Fase 0</b>: a linha de base — os números do NB04 contra os quais tudo é comparado — e as correções que
travavam o resto (a Varimax, a proporção nacional de água).
• <b>Fases 1 e 2</b>: as demandas 1 e 2 e a fatorial ampliada.
• <b>Fases 3 e 4</b>: o Notebook 04b, que roda a fatorial ampliada, e a revisão da apresentação.
• <b>Fase 5</b>: o resto da revisão geral do repositório.
• <b>Fases A e B</b>: as pendências e o banheiro graduado.
• <b>Fases C e D</b>: o motor de especificações e o Notebook 05.

A cronologia (Parte B, slides 21 a 26) conta as mesmas fases com mais detalhe.""",
             apresentar="""“O trabalho foi feito em fases, cada uma registrada: em 25/09, as demandas; em 26 e 27/09, os testes de
cada escolha e o IVS final.”"""),

        dict(n=7, titulo="O ponto de partida: o NB04",
             frase="A divisória da parte 2: o índice que existia antes das demandas e o quanto ele separa as favelas.",
             mostra="""O número 2 em vermelho, o título "O ponto de partida: o NB04" e o subtítulo: o índice que já existia antes
das demandas — e o quanto ele separa as favelas.""",
             zero="""Toda mudança precisa de um ponto de comparação. Aqui ele é o NB04, o notebook da análise fatorial de
17/09, corrigido em 25/09.""",
             apresentar="""“Antes das respostas, o ponto de partida: o índice do NB04.”"""),

        dict(n=8, titulo="O índice do NB04, em seis números",
             frase="Os seis números que resumem o NB04 — e o sexto, em vermelho, é o problema: a renda sozinha separa as favelas melhor que o índice.",
             mostra=f"""À esquerda, seis números grandes em duas colunas, cada um sobre um filete e com uma legenda embaixo:
{N.kmo}, {N.msa_min}, {N.p_soc1} / {N.p_san1}, {N.phi}, {N.auc_ind} e, em vermelho, {N.auc_renda}. À
direita, a curva ROC do índice contra os setores de favela, com a área sombreada e a AUC escrita no canto.""",
             zero="""Os seis números, um por um:

• <b>KMO do IVS-7</b>: o quanto os dados servem para análise fatorial (A.6). Acima de 0,7 é bom.
• <b>MSA mínimo</b>: o KMO da variável que menos conversa com as outras. É o do lixo: ele está no limite.
• <b>Pesos do IVS-6 com Varimax</b>: sem o lixo, a análise acha dois fatores e reparte o peso entre eles —
socioeconômico e saneamento.
• <b>Φ</b>: na rotação promax, a correlação entre os dois fatores. Moderada: as dimensões não são independentes.
• <b>AUC do índice</b>: o quanto o índice separa os setores de favela (A.7).
• <b>AUC da renda sozinha</b>: o mesmo, usando só a renda invertida. Está em vermelho porque é maior.

A <b>curva ROC</b>, à direita, mostra a separação de todos os jeitos possíveis de cortar o índice. O eixo de
baixo é a proporção de setores <i>não</i> favela que o corte marcaria por engano; o eixo da esquerda, a
proporção de favelas que ele acertaria. A diagonal tracejada é o acaso; quanto mais a curva sobe para o
canto de cima, à esquerda, melhor.""",
             numeros=f"""A AUC de {N.auc_ind} quer dizer que, sorteando um setor de favela e um que não é, o índice dá o valor
maior ao de favela em cerca de 81% dos pares. A renda sozinha faz isso em cerca de 88% ({N.auc_renda}). A
curva foi calculada sobre {N.fcu_s1} setores de favela contra {N.nfcu_s1} que não são. Sem São Paulo, o peso
socioeconômico cairia para {N.p_sem_sp}% — o que mostra quanto um município grande pode pesar.""",
             apresentar=f"""“Este é o ponto de partida. Os dados servem para análise fatorial, a análise divide os pesos em
aproximadamente dois terços socioeconômico e um terço saneamento, e o índice separa bem as favelas — mas a
renda sozinha separa melhor. Guardem esse sexto número, porque ele volta.”""",
             perguntas=[("Uma AUC de 0,81 é boa?", "É boa: bem acima do acaso (0,5). O ponto não é que o índice seja ruim, e sim que a renda, sozinha, já é melhor nessa tarefa específica."),
                        ("Por que comparar com a renda?", "Porque a renda é o indicador mais simples e mais conhecido. Se o índice não superar a renda em nada, precisa justificar por que existe. A parte 8 mostra em que ele supera.")]),

        dict(n=9, titulo="Demandas 1 e 2 — a renda e o quadro",
             frase="A divisória da parte 3: a renda com a mediana e o quadro de indicadores.",
             mostra="""O número 3 em vermelho, o título "Demandas 1 e 2 — a renda e o quadro" e o subtítulo: a mediana no lugar
do setor extremo; os indicadores num quadro só.""",
             zero="""As duas primeiras demandas são de dados, não de análise: uma coluna nova de renda e uma tabela que
documenta todos os indicadores.""",
             apresentar="""“A parte 3 responde às duas primeiras demandas.”"""),

        dict(n=10, titulo="Demanda 1: a renda com a mediana",
             frase="O setor de renda extrema recebe a mediana de Belo Horizonte, e as três versões da renda dão praticamente o mesmo resultado na análise fatorial.",
             mostra=f"""Uma frase de abertura sobre o setor `310620005650366` ({N.renda_extremo} de renda média). Depois, duas
tabelas. A primeira tem as três alternativas de valor para pôr no lugar do extremo: a mediana de BH sem o
setor ({N.med_bh}), a mediana de BH com o setor ({N.med_bh_com}) e a mediana dos 70 municípios sem o setor
({N.med_70}) — com a média, o desvio-padrão e o máximo de BH depois da troca. A segunda tem o efeito de
cada versão da renda na análise fatorial: KMO, MSA mínimo e AUC do índice no IVS-7 e no cenário S6. Uma
linha de leitura, em vermelho, fecha o slide.""",
             zero=f"""O problema é o <b>valor extremo</b>: um setor com renda média muito acima de todos os outros. Na
normalização min-max (A.5), ele vira o máximo, e todos os outros setores ficam espremidos perto de zero.

A solução pedida é a <b>imputação pela mediana</b>: trocar o valor extremo pela mediana — o valor do meio
de uma lista ordenada, que não é puxado por extremos. Três medianas foram consideradas:

• a de Belo Horizonte <b>sem</b> o setor ({N.med_bh}) — a escolhida, porque o setor é de BH e a mediana não
deve incluir o próprio valor que se quer corrigir;
• a de Belo Horizonte <b>com</b> o setor ({N.med_bh_com}) — quase igual, porque a mediana é robusta a um
valor extremo;
• a dos 70 municípios ({N.med_70}) — mais baixa, porque mistura cidades de renda menor.

Depois da troca, a média de BH fica em {N.bh_media}, o desvio-padrão em {N.bh_dp} e o máximo em {N.bh_max}.

As três versões da renda no projeto passam a ser: a <b>original</b> (com o setor extremo), a <b>sem o
extremo</b> (o setor fica sem valor) e a <b>mediana municipal</b> (o setor recebe a mediana de BH).""",
             numeros=f"""A segunda tabela é a que importa para a decisão: entre as três versões, o KMO muda no máximo
{N.dif_kmo} e a AUC do índice, {N.dif_auc}. São diferenças na terceira ou quarta casa decimal — na prática,
nenhuma. Por isso a conclusão do slide: a escolha da renda é conceitual (qual tratamento do extremo é mais
defensável), não empírica (os números não decidem).""",
             apresentar="""“O setor extremo de Belo Horizonte recebeu a mediana da cidade sem ele, e as alternativas ficaram
registradas. Na análise fatorial, as três versões da renda dão o mesmo resultado até a terceira casa. Então
a escolha da renda é de princípio: qual tratamento do extremo você prefere defender.”""",
             perguntas=[("Por que o extremo quase não muda a fatorial, se muda tanto a normalização?", "Porque a análise fatorial usa a correlação de Spearman, que trabalha com posições (A.6). O setor extremo é “o primeiro” com qualquer valor. Já a normalização min-max usa o valor em si — e aí ele distorce tudo.")]),

        dict(n=11, titulo="Demanda 2: o quadro de indicadores",
             frase=f"Os {N.n_ind} indicadores do projeto, por dimensão, com os {N.n_ind_ivs7} que entram no IVS-7 marcados com asterisco.",
             mostra=f"""Uma tabela com quatro linhas, uma por dimensão: saneamento ({N.q_san} indicadores), socioeconômica
({N.q_soc}), morfologia ({N.q_morf}) e demografia ({N.q_dem}). Para cada uma, quantos indicadores, quantos
entram no IVS-7 e a lista dos nomes; os do IVS-7 têm um asterisco.""",
             zero="""O quadro completo, na entrega à orientadora, tem para cada indicador: o que mede, o numerador, o
denominador, se usa complemento, o arquivo de origem e uma observação. A tabela abaixo reproduz, do próprio
quadro, o que cada nome quer dizer. Os indicadores fora do IVS-7 são <b>descritivos</b>: caracterizam o
território (idade, tipo de moradia, chefia feminina), mas não entram na soma do índice.""",
             tabela=(["Indicador", "Dimensão", "IVS-7", "O que mede (do quadro)"], N.quadro, [5.3, 2.75, 1.15, 7.2]),
             apresentar=f"""“O quadro documenta os {N.n_ind} indicadores: como cada um é calculado e de onde vem. Sete entram no
índice; os outros descrevem o território.”"""),

        dict(n=12, titulo="Demandas 3 e 5 a 11 — a fatorial ampliada",
             frase="A divisória da parte 4: a análise fatorial repetida em oito cenários, um para cada mudança pedida.",
             mostra="""O número 4 em vermelho, o título "Demandas 3 e 5 a 11 — a fatorial ampliada" e o subtítulo: oito
cenários sem bootstrap, o IVS-7 do NB04 e o que muda a cada variável que entra ou sai.""",
             zero="""A maior parte das demandas pede para mudar o conjunto de variáveis da análise fatorial. Em vez de uma
análise nova para cada pedido, a <b>fatorial ampliada</b> organiza tudo em <b>cenários</b>: cada cenário é
uma análise fatorial completa, com um conjunto de variáveis, e todos são comparados com o S0 (o IVS-7 do
NB04).""",
             apresentar="""“A parte 4 é a fatorial ampliada: oito cenários, um para cada mudança pedida.”"""),

        dict(n=13, titulo="Os cenários: o que entra em cada um",
             frase="Os oito cenários da fatorial ampliada, cada um com o número de variáveis e de setores e os resultados de adequação e de quantos fatores manter.",
             mostra="""Uma tabela de oito linhas (S0 a S7) e nove colunas: o nome, o que entra, a demanda que o cenário
responde, o número de variáveis, o número de setores, o KMO, o MSA mínimo, os fatores pelas regras de
Kaiser e de Horn (K/H) e a variância explicada por dois fatores.""",
             zero=f"""Os cenários:

• <b>S0</b>: o IVS-7, que reproduz o NB04 — o ponto de comparação;
• <b>S1</b>: o IVS-6, sem o lixo (demanda 10);
• <b>S2</b>: o IVS-7 mais a água que não chega encanada (demandas 5 e 7);
• <b>S3</b>: o IVS-7 mais a falta de água canalizada (demanda 7);
• <b>S4</b>: o IVS-7 mais a falta de banheiro, pela `V00495` (demandas 6 e 7);
• <b>S5</b>: o IVS-7 mais a moradia não convencional (demanda 9);
• <b>S6</b>: o IVS-7 mais as quatro novas — "tudo isso" (demanda 8);
• <b>S7</b>: o S6 sem o lixo (demandas 8 e 10).

As colunas de resultado (A.6): o <b>KMO</b> diz se os dados servem para análise fatorial; o <b>MSA
mínimo</b>, qual variável conversa menos com as outras; <b>Fatores K/H</b>, quantos fatores as regras de
Kaiser e de Horn mandam manter; e a <b>variância explicada por dois fatores</b>, quanto da informação das
variáveis cabe em duas dimensões.""",
             numeros=f"""Três leituras:

• Todos os cenários têm KMO acima de 0,7: todos servem para análise fatorial.
• Quando entram variáveis com muito sigilo, a base perde setores: o S6 fica com {N.s6_n} setores, contra
{N.s0_n} do S0.
• Quanto mais variáveis, mais fatores as regras pedem e menos cabe em dois: no S6, as regras pedem
{N.s6_k} fatores e dois explicam {N.s6_var2}% da variância, contra {N.s0_var2}% no S0. O índice usa dois
fatores — as duas dimensões do IVS-BH 2012 —, e esse número mostra o que se perde com isso.""",
             apresentar="""“Cada linha é uma análise fatorial completa. Todos os cenários servem para a técnica; o que muda é
quantos setores sobram e quantas dimensões os dados pedem. Com tudo junto, os dados pedem mais de duas.”""",
             perguntas=[("O que quer dizer “3 / 2” em fatores K/H?", "Que a regra de Kaiser manda manter três fatores e a de Horn, mais exigente, dois. Quando as duas discordam, a de Horn costuma ser a mais confiável.")]),

        dict(n=14, titulo="Demandas 3 e 11: sem rotação, Varimax e promax",
             frase="Como os pesos se repartem entre os dois fatores em cada rotação — e a correlação entre os fatores quando se deixa que eles se correlacionem.",
             mostra=f"""Uma tabela com quatro cenários (S0, S1, S6 e S7) e sete colunas: os pesos do fator 1 e do fator 2 sem
rotação, com Varimax, com promax pela matriz padrão e com promax pela matriz estrutura; o Φ; e a variável
que puxa o fator 2. Embaixo, dois blocos: a leitura e "o que não está dito".""",
             zero=f"""Cada célula como "{N.pw_s0_varimax}" quer dizer: o fator 1 leva {N.pw_s0_varimax.split(' / ')[0]}% do peso e o
fator 2, o resto. O <b>fator 1</b> é sempre puxado pela renda (é o socioeconômico); o <b>fator 2</b> é puxado
pelo lixo no S0, pela água inadequada no S1 e pela água que não chega no S6 e no S7.

As rotações (A.6):

• <b>sem rotação</b>, o primeiro fator pega quase tudo: entre {N.semrot_min}% e {N.semrot_max}% do peso;
• a <b>Varimax</b> gira os eixos mantendo os fatores independentes e reparte melhor o peso;
• a <b>promax</b> deixa os fatores se correlacionarem; o <b>Φ</b> é essa correlação. A <b>matriz padrão</b>
dá o efeito próprio de cada fator; a <b>matriz estrutura</b> soma a parte que os fatores compartilham — por
isso, nela, o fator 2 sempre ganha um pouco mais de peso.""",
             numeros=f"""O S1 (sem o lixo) é o que mais muda: sem rotação, {N.pw_s1_sem_rotacao}; com Varimax, {N.pw_s1_varimax}
(são os pesos do NB04); com promax padrão, {N.pw_s1_promax_padrao}; com promax estrutura, {N.pw_s1_promax_estrutura}.
O Φ do S1 é {N.phi_s1}: as duas dimensões são bem correlacionadas. No S0, com o lixo, o Φ cai para {N.phi_s0} —
porque o lixo, que puxa o fator 2, conversa pouco com o resto.""",
             apresentar="""“A rotação muda bastante a repartição dos pesos: sem rotação, o primeiro fator leva três quartos; com
rotação, cerca de dois terços. E qual matriz usar na promax muda o resultado — essa escolha é sua.”""",
             perguntas=[("Qual rotação é a certa?", "Não há uma certa. A Varimax supõe que as dimensões são independentes; a promax deixa que se correlacionem, o que é mais realista aqui (Φ de 0,52 no S1). Mas a escolha muda os pesos, e por isso está nas perguntas à orientadora.")]),

        dict(n=15, titulo="O plano fatorial do S6",
             frase="Um mapa das onze variáveis do S6 nos dois primeiros fatores, em três versões: sem rotação, Varimax e promax.",
             mostra="""Uma figura grande com três painéis lado a lado. Em cada um, cada ponto é uma variável: a posição na
horizontal é a carga no fator 1 (renda e analfabetismo) e na vertical, a carga no fator 2 (água que não
chega e sem água canalizada). As quatro variáveis novas estão em vermelho; as do IVS-7, em verde escuro.""",
             zero="""Este tipo de gráfico se chama <b>plano fatorial</b>. Lê-se assim: variável perto do eixo horizontal, à
direita, pertence ao fator 1; perto do eixo vertical, em cima, pertence ao fator 2; perto do centro, não
pertence a nenhum.

O que a figura mostra:

• <b>sem rotação</b>, todas as variáveis ficam à direita (o fator 1 pega tudo), e o fator 2 só separa as de
saneamento (em cima) das socioeconômicas (embaixo);
• com <b>Varimax</b>, o quadro fica limpo: renda, analfabetismo, cor/raça e razão de moradores vão para a
direita, embaixo (fator 1); as variáveis de água e banheiro sobem (fator 2);
• com <b>promax</b>, a separação é ainda mais nítida;
• em todas as versões, a <b>moradia não convencional</b> fica perto do centro — não pertence a nenhum fator
(slide 17) —, e o <b>lixo</b> fica fraco nos dois.""",
             apresentar="""“O plano fatorial mostra as duas dimensões com clareza depois da rotação: a socioeconômica de um lado,
a água e o banheiro do outro. A moradia não convencional fica no centro: não pertence a nenhuma.”"""),

        dict(n=16, titulo="Demandas 5, 6 e 7: uma variável nova por vez",
             frase="O que cada variável nova faz com a base de setores, com a adequação e com a separação das favelas — e a prova de que juntar a falta de banheiro é usar a V00495.",
             mostra="""Uma tabela com cinco cenários (S0, S2, S3, S4 e S5) e oito colunas: setores, setores perdidos em relação
ao S0, KMO, fatores K/H, AUC do índice, AUC da renda e se o lixo forma fator próprio. Embaixo, dois blocos:
a junção da demanda 6 e a comparação da demanda 5.""",
             zero=f"""As variáveis novas (o quadro do slide 11 tem as definições):

• <b>água não chega</b> (S2): domicílios em que a água não chega encanada (`V00201`);
• <b>sem água canalizada</b> (S3): domicílios em que a água não chega encanada até dentro de casa;
• <b>sem banheiro</b> (S4): domicílios sem banheiro de uso exclusivo (`V00495`);
• <b>moradia não convencional</b> (S5): cortiço, maloca, estrutura degradada.

"<b>Perdidos vs S0</b>" é quantos setores saem porque a variável nova está sob sigilo neles: {N.s2_perd} no
S2, {N.s3_perd} no S3, {N.s4_perd} no S4 e {N.s5_perd} no S5.

<b>A junção da demanda 6</b>. A `V00238` (nem banheiro nem sanitário) é uma das partes da `V00495`. Para
"juntar", basta usar a `V00495` — somar as duas contaria a `V00238` duas vezes. Prova: a `V00238` nunca passa
da `V00495` em {N.juncao_vale} de {N.juncao_n} setores com as duas presentes.

<b>A comparação da demanda 5</b>. A água que não chega foi comparada nas duas leituras do slide 5: com as
outras categorias de água e com os indicadores do IVS-7 — pela correlação de Spearman e pelo perfil dos
setores com e sem o problema.""",
             numeros=f"""O S4 (com a falta de banheiro) tem a maior AUC do índice entre os cenários com uma variável a mais
({N.auc_s4}), mas também perde mais setores ({N.s4_perd}). A AUC da renda muda de cenário para cenário
porque a base de setores muda. E, em todos os cenários com variável de água ou banheiro, o lixo deixa de
ter fator próprio.""",
             apresentar="""“Cada variável nova faz duas coisas: tira setores da base, por causa do sigilo, e redistribui os
fatores. Juntar a falta de banheiro é usar a variável que já é a soma; as contas confirmam isso setor a
setor.”"""),

        dict(n=17, titulo="Demanda 9: a moradia não convencional",
             frase="A moradia não convencional entrou como pedido, mas quase não conversa com as outras variáveis: 92% dos setores não têm nenhuma.",
             mostra=f"""Três números grandes: a comunalidade da variável no S5 ({N.nc_h2}, em vermelho), a porcentagem de setores
com valor zero ({N.nc_zeros}%) e o MSA da variável ({N.nc_msa}). Embaixo, a leitura.""",
             zero=f"""A demanda 9 pedia a habitação convencional. Ela entrou virada para o lado da vulnerabilidade: a proporção
de moradias <i>não</i> convencionais (cortiço, maloca, estrutura degradada).

O resultado mostra um contraste:

• o <b>MSA</b> de {N.nc_msa} passa no critério (0,50): a variável não atrapalha a análise;
• mas a <b>comunalidade</b> é de {N.nc_h2} — os fatores explicam pouco mais de 1% do que ela varia —, e a maior
carga é {N.nc_carga}. Ela não pertence a nenhum fator.

A razão é simples: em {N.nc_zeros}% dos setores, não há nenhuma moradia não convencional. Uma variável que é
quase sempre zero tem pouca variação para dividir com as outras. A variável ficou no S5 e no S6, como pedido,
e o resultado mostra por que ela não carrega o índice.""",
             apresentar="""“A moradia não convencional entrou, mas os fatores explicam só cerca de 1% dela: em mais de nove de cada
dez setores, ela é zero. Não é um problema da variável — é que ela descreve um fenômeno raro e concentrado.”"""),

        dict(n=18, titulo="Demanda 8: tudo isso junto",
             frase="Com as quatro variáveis novas juntas, os dados pedem quatro dimensões e dois fatores explicam menos da metade da informação.",
             mostra="""À esquerda, uma tabela com o S6, o S7 e três variantes do S6 (renda sem o extremo, renda com a mediana
e postos no município), com o número de variáveis, de setores, o KMO, os fatores K/H e a variância
explicada por dois fatores. À direita, o <i>scree plot</i> do S6. Embaixo, à esquerda, a leitura.""",
             zero=f"""O <b>scree plot</b> (A.6) mostra os autovalores em ordem: a linha com pontos é o que os dados dão; a linha
tracejada vermelha é o que dados aleatórios dariam (a regra de Horn); a linha pontilhada em 1 é a regra de
Kaiser. Ficam os fatores cujo ponto está acima das duas linhas. No S6, são quatro.

As variantes do S6 testam se o resultado depende da renda (não depende: as três rendas dão o mesmo) e da
forma de medir. Os <b>postos no município</b> trocam cada valor pela posição do setor dentro da sua cidade
— o que compara cada setor só com os vizinhos de município.""",
             numeros=f"""Com onze variáveis, o KMO sobe ({N.s6_kmo}), mas as regras pedem {N.s6_k} fatores e dois explicam só
{N.s6_var2}% da variância (contra {N.s0_var2}% no IVS-7). A base cai para {N.s6_n} setores. Com postos no
município, o MSA mínimo cai para {N.s6_postos_mun_msa}, abaixo do critério de 0,50.""",
             apresentar="""“Juntando tudo, os dados pedem quatro dimensões, não duas, e perde-se uma parte grande da base. Se o
índice continuar com duas dimensões, como no IVS de Belo Horizonte, vale lembrar que, com tudo junto, metade
da informação fica de fora.”"""),

        dict(n=19, titulo="Demanda 10: o lixo",
             frase="Com o lixo, ele forma uma dimensão sozinho; sem ele, a análise pede uma dimensão só — o lixo é que sustenta a estrutura em dois fatores no IVS-7.",
             mostra="""Uma tabela com os oito cenários e três colunas: fatores K/H, se o lixo forma fator próprio na Varimax e
em quantos municípios a saída do município muda o lixo de fator.""",
             zero=f"""Desde junho se sabe que o lixo conversa pouco com as outras variáveis. A tabela mostra as consequências:

• no <b>S0</b> (IVS-7) e no <b>S5</b>, o lixo ocupa um fator sozinho;
• no <b>S1</b> (sem lixo), as regras pedem um fator só ({N.s1_k} por Kaiser e {N.s1_h} por Horn): sem o lixo,
a vulnerabilidade vira uma dimensão única;
• quando entram as variáveis de água e de banheiro (S2, S3, S4 e S6), o fator 2 passa a ser o da água, e o
lixo perde o fator próprio;
• na sensibilidade, a saída de um município muda o lixo de fator em {N.lixo_muda_s0} das {N.rodadas} rodadas
do S0.

A última coluna só tem valores para S0, S1 e S6, os cenários em que a sensibilidade por município foi
rodada.""",
             apresentar="""“O lixo é a variável que decide a estrutura: com ele, há duas dimensões, mas uma delas é só o lixo; sem
ele, há uma. Se a orientadora tirar o lixo, vale discutir se o índice continua com duas dimensões.”""",
             perguntas=[("Então o lixo deve sair?", "Os números não decidem sozinhos. A favor de tirar: ele forma um fator à parte e baixa a qualidade da fatorial. Contra: ele está no IVS-BH 2012, e tirá-lo quebra a comparação. É uma das escolhas da orientadora (slide 40).")]),

        dict(n=20, titulo="A incerteza: um município de fora por vez",
             frase="Tirando um município por vez, o peso do fator 1 se move no máximo cerca de três pontos percentuais — e quem mais move são São Paulo e Salvador.",
             mostra="""À esquerda, uma figura com duas faixas, S6 em cima e S1 embaixo: cada ponto é o peso do fator 1 numa
rodada sem um município, e o traço vermelho é o peso com todos. O ponto que se afasta tem o rótulo "sem São
Paulo". À direita, uma tabela com a maior variação, em pontos percentuais, na Varimax e na promax, para S0,
S1 e S6, com o município responsável. Embaixo, a leitura.""",
             zero=f"""É a <b>sensibilidade por município</b> (A.8): a análise é refeita {N.rodadas} vezes — uma com todos os
municípios e uma sem cada um — e mede-se quanto o peso do fator 1 muda. "Maior |Δ|" é a maior mudança, em
valor absoluto (sem sinal), medida em <b>pontos percentuais</b>.

Na figura, quase todos os pontos ficam colados no traço vermelho: tirar quase qualquer município não muda
nada. As exceções são as metrópoles: sem São Paulo, o peso do fator 1 no S1 cai cerca de dois pontos.""",
             numeros=f"""No S0, a maior mudança é {N.sens_s0} p.p., sem {N.sens_s0_mun}; no S1, {N.sens_s1} p.p., sem
{N.sens_s1_mun}; no S6, {N.sens_s6} p.p., sem {N.sens_s6_mun}. O máximo de todas as rodadas, nas duas
rotações, é {N.sens_max} p.p. Em pesos de cerca de 60%, isso é uma variação pequena: o resultado não depende
de um município só.""",
             apresentar="""“Em vez de bootstrap, tirei um município de cada vez. O peso do fator 1 se move no máximo uns três
pontos, e só quando sai uma metrópole. O resultado é estável.”"""),

        dict(n=21, titulo="A validação contra as favelas, cenário a cenário",
             frase=f"A AUC contra as favelas em cada cenário: a renda sozinha vence o índice em {N.renda_vence} de {N.n_cen} cenários.",
             mostra="""Uma tabela com os oito cenários e três AUCs: a do índice, a da média simples dos postos e a da renda
sozinha (em negrito). Embaixo, a leitura.""",
             zero=f"""As três colunas (A.7):

• a <b>AUC do índice</b>: o índice com os pesos da Varimax;
• a <b>AUC da média de postos</b>: ordenar os setores em cada indicador e tirar a média das posições, sem
peso nenhum — um "índice ingênuo";
• a <b>AUC da renda sozinha</b>: só a renda invertida.

Em todos os oito cenários da tabela, a renda vence, e a média sem peso também fica acima do índice. Contando
as variantes (as três rendas e os postos no município), a renda vence em {N.renda_vence} de {N.n_cen}; as
exceções são {N.renda_perde_em}.""",
             apresentar="""“Em todos os cenários, a renda sozinha separa as favelas melhor que o índice. Isso não condena o índice:
mostra que separar favelas não é a tarefa em que ele se destaca. A parte 8 mostra onde ele se destaca.”""",
             perguntas=[("A validação contra favelas não está viciada?", "Em parte, sim: o IBGE usa condições de infraestrutura para identificar favelas, e algumas delas estão no índice. Por isso a AUC é um dos três critérios de escolha, e não o único.")]),

        dict(n=22, titulo="Demanda 4 — a apresentação revista",
             frase="A divisória da parte 5: a revisão da apresentação principal.",
             mostra="""O número 5 em vermelho, o título "Demanda 4 — a apresentação revista" e o subtítulo: o que ficou, o que saiu
e os números que estavam errados.""",
             zero="""A demanda 4 pedia para separar, na apresentação principal, o que serve do que não serve.""",
             apresentar="""“A parte 5 é a revisão da apresentação.”"""),

        dict(n=23, titulo="Separar o útil do inútil",
             frase="O deck principal foi inventariado, corrigido e ampliado — sem ser regerado.",
             mostra="""Quatro blocos: o inventário, os números corrigidos (com o filete vermelho), o bloco novo e o deck hoje.""",
             zero=f"""• <b>O inventário</b>: um programa listou todos os artefatos de apresentação, e um documento
(`MAPA_APRESENTACAO_FINAL.md`) diz o que entra, o que sai e em que ordem.
• <b>Os números corrigidos</b>: três números errados nos slides e um no guia de apoio (16.548 no lugar de
16.563), todos relidos das tabelas. Os códigos (AUD-07, DEC-1, AUD-04, AUD-08) identificam cada achado nas
auditorias.
• <b>O bloco novo</b>: os slides da fatorial ampliada e, depois, os do IVS final são gerados por programa e
anexados ao deck principal por outro programa, o "juntador".
• <b>O deck hoje</b>: tem {N.slides_atual} slides, e a estrutura interna do arquivo foi conferida e consertada em
30/09.

Por que não regerar o deck principal? Porque ele tem marcações e anotações feitas à mão; regerá-lo apagaria
esse trabalho. Os blocos novos entram por fora.""",
             apresentar="""“A apresentação principal foi inventariada e corrigida, e os blocos novos — a fatorial ampliada e o IVS
final — foram anexados sem mexer no que já estava lá.”"""),

        dict(n=24, titulo="Os testes seguintes",
             frase="A divisória da parte 6: os nove itens da etapa de 26/09 e o banheiro graduado.",
             mostra="""O número 6 em vermelho, o título "Os testes seguintes" e o subtítulo: os nove itens da etapa de 26/09 e o
banheiro graduado.""",
             zero="""Depois das demandas, ficaram escolhas em aberto. A etapa seguinte transformou cada uma num teste.""",
             apresentar="""“A parte 6 são os testes que vieram depois das demandas.”"""),

        dict(n=25, titulo="Os nove itens da etapa seguinte",
             frase="Os nove itens de teste e o resultado de cada um: cada escolha em aberto virou uma dimensão da grade do NB05.",
             mostra="""Uma tabela de nove linhas: o item, o que foi pedido e o resultado.""",
             zero=f"""Os itens 1 a 5 são as escolhas em aberto; cada uma virou uma dimensão da grade (parte 7):

• <b>1. Renda</b>: as três versões entram na grade; empatam na AUC.
• <b>2. Rotação</b>: sem rotação, nenhuma especificação passa nos critérios ({N.eleg_semrot}); com Varimax,
{N.eleg_vari}; com promax, {N.eleg_prom}.
• <b>3. Pesos na rotação oblíqua</b>: cinco esquemas — SS da matriz padrão, SS da estrutura, comunalidades,
50/50 e 60/40 (A.6).
• <b>4. Lixo</b>: com lixo, {N.eleg_lixo_com} passam; sem lixo, {N.eleg_lixo_sem}.
• <b>5. Banheiro</b>: fora, pela `V00495` ou graduado (slide 26).

Os outros itens: <b>6</b>, o que o índice acrescenta à renda (parte 8); <b>7</b>, transformar em verificação
três afirmações que estavam escritas sem conta; <b>8</b>, pendências pequenas (o dicionário, um caminho
citado num slide da EDA Central, a reexecução de scripts); <b>9</b>, o Notebook 05, o relatório e os slides.""",
             apresentar="""“Cada escolha em aberto virou um teste. As cinco primeiras viraram dimensões da grade que vem na parte
7; as outras foram verificações e pendências.”"""),

        dict(n=26, titulo="O banheiro graduado",
             frase="A falta de banheiro em três graus, cada um com um peso — e a prova de que as três partes somam o total em todos os setores.",
             mostra=f"""Uma tabela com as quatro variáveis — `V00236`, `V00237`, `V00238` e `V00495` —, o que cada uma conta, o grau e
o peso. Embaixo, em negrito, a fórmula do banheiro graduado. Por fim, dois números: {N.part_bate} de
{N.part_pres} (em vermelho) e {N.part_aus}.""",
             zero="""O Censo conta os domicílios sem banheiro de uso exclusivo (`V00495`) e divide esse total em três partes:

• `V00236` — só banheiro de uso comum (dividido com outras casas): grau leve, peso 1;
• `V00237` — só sanitário ou buraco para dejeções: grau intermediário, peso 2;
• `V00238` — nem banheiro nem sanitário: grau grave, peso 3.

O <b>banheiro graduado</b> soma as três com os pesos e divide pelo máximo possível (3 vezes o total de
domicílios): (1·`V00236` + 2·`V00237` + 3·`V00238`) ÷ (3·`V00001`). Ele vai de 0 (todos com banheiro
exclusivo) a 1 (todos sem banheiro nem sanitário).""",
             numeros=f"""Exemplo: um setor com 100 domicílios, dos quais 4 só têm banheiro comum, 3 só têm sanitário e 1 não tem
nada. O graduado é (4 + 2×3 + 3×1) ÷ 300 = 13 ÷ 300 ≈ 0,043. A versão simples (`V00495`) diria 8 ÷ 100 =
0,08, tratando os 8 casos como iguais.

Os dois números do slide: em {N.part_bate} de {N.part_pres} setores com as quatro variáveis presentes, as três
partes somam exatamente o total — uma partição perfeita. Os {N.part_aus} setores restantes têm alguma das
quatro sob sigilo, e o graduado fica ausente neles.""",
             apresentar="""“O banheiro graduado distingue a gravidade: dividir um banheiro não é o mesmo que não ter nem
sanitário. As contas confirmam que as três partes somam o total em todos os setores em que dá para
conferir.”""",
             perguntas=[("Por que os pesos 1, 2 e 3?", "São a forma mais simples de ordenar a gravidade, sem inventar distâncias. Outros pesos são possíveis; esses ficaram documentados e podem ser trocados.")]),

        dict(n=27, titulo="O IVS final — a grade do Notebook 05",
             frase="A divisória da parte 7: todas as combinações das escolhas em aberto, com regras fixadas antes de rodar.",
             mostra="""O número 7 em vermelho, o título "O IVS final — a grade do Notebook 05" e o subtítulo: todas as combinações
das escolhas em aberto, com regras fixadas antes de rodar.""",
             zero="""Esta é a parte central do deck. Em vez de escolher uma especificação, o NB05 calcula todas e mostra o que
cada escolha muda (A.9).""",
             apresentar="""“A parte 7 é o IVS final: todas as combinações, calculadas.”"""),

        dict(n=28, titulo=f"A grade: {N.n_esp} especificações",
             frase=f"De onde vêm as {N.n_esp} especificações, quantas passam nos critérios ({N.n_eleg}) e como se escolhe a referência.",
             mostra=f"""Cinco números grandes em fila: {N.n_bases} bases, {N.n_esq} esquemas, 2 normalizações, {N.n_esp}
especificações e, em vermelho, {N.n_eleg} elegíveis. Embaixo, dois blocos: o critério de elegibilidade e o
critério de escolha da referência.""",
             zero=f"""A conta da grade:

• <b>{N.n_bases} bases</b>: 3 versões da renda × 2 do lixo (com, sem) × 3 do banheiro (fora, `V00495`,
graduado). Uma base é o conjunto de variáveis que vai para a análise fatorial;
• <b>{N.n_esq} esquemas</b>: sem rotação (um fator só); Varimax com SS, 50/50 e 60/40; promax com SS da padrão,
SS da estrutura, comunalidades, 50/50 e 60/40;
• <b>2 normalizações</b>: no município ou global (A.5);
• {N.n_bases} × {N.n_esq} × 2 = <b>{N.n_esp} especificações</b>.

Uma especificação é <b>elegível</b> se passar nos quatro critérios (KMO, MSA, comunalidade, carga). Entre as
elegíveis, a <b>referência</b> é a de melhor posição média em estabilidade, AUC no município e parcimônia
(A.9). Os critérios foram escritos antes de rodar a grade.""",
             apresentar=f"""“São {N.n_esp} especificações — todas as combinações de renda, lixo, banheiro, rotação, pesos e
normalização. {N.n_eleg} passam nos critérios de qualidade, e entre elas os três critérios de escolha
apontam uma referência.”"""),

        dict(n=29, titulo="Quem passa nos critérios, base a base",
             frase="Em cada uma das 18 bases, quantas das 18 especificações passam — e por que as bases com o lixo caem.",
             mostra="""Uma tabela com seis linhas (renda × lixo) e três colunas de banheiro (fora, `V00495`, graduado). Cada
célula diz quantas das 18 especificações daquela base são elegíveis (9 esquemas × 2 normalizações).
Embaixo, em vermelho, "Por que cai".""",
             zero=f"""O padrão da tabela:

• a <b>renda não muda nada</b>: as três linhas de cada lixo são iguais;
• <b>sem lixo</b>, as três versões de banheiro passam (16 de 18 cada);
• <b>com lixo</b>, só passa a base com a `V00495`.

"16 de 18" e não 18: as 2 que caem em cada base são as do fator único (sem rotação, nas duas
normalizações), que nunca passam.""",
             numeros=f"""O motivo da queda é a <b>comunalidade mínima</b> (A.6), o critério de 0,30:

• com o lixo e sem banheiro — a base do IVS-7 do NB04 —, a comunalidade da água inadequada fica em
{N.h2_agua}: abaixo do mínimo;
• com o lixo e o banheiro graduado, a do banheiro graduado fica em {N.h2_grad}: abaixo por um triz;
• com o lixo e a `V00495`, a mínima sobe para {N.h2_v495} e a base passa;
• sem o lixo, a mínima é {N.h2_sem} (da {N.h2_sem_var}), e todas passam.""",
             apresentar="""“A renda não muda a elegibilidade. O lixo muda: com ele, a água fica com comunalidade baixa e o IVS-7
original não passa nos critérios. Sem o lixo, todas as versões de banheiro passam.”""",
             perguntas=[("O IVS-7 do NB04 não passa? Então o NB04 estava errado?", "Não estava errado: o NB04 usou o IVS-6 (sem lixo) como base principal justamente por causa do lixo. O que a grade mostra é que, com os critérios fixados agora, o IVS-7 completo fica de fora pela comunalidade da água.")]),

        dict(n=30, titulo="Rotação e esquema de peso",
             frase="Em toda a grade, o fator único nunca passa; com dois fatores, todos os esquemas passam no mesmo número.",
             mostra="""À esquerda, uma tabela com os nove esquemas (rotação e peso) e quantos são elegíveis de 36. À direita, com
o filete vermelho, o bloco "Um fator ou dois".""",
             zero=f"""• <b>Sem rotação, fator único</b>: {N.eleg_semrot}. Com um fator só, alguma variável fica sempre com
comunalidade baixa.
• <b>Todos os outros esquemas</b>: {N.eleg_esquema} cada. A elegibilidade depende da base e da rotação, não
de como os pesos são repartidos depois — por isso os cinco esquemas da promax passam no mesmo número.

<b>Um fator ou dois?</b> As regras de Kaiser e de Horn indicam um fator no IVS-6 (slide 19). Mas o fator
único reprova em toda a grade pela comunalidade. Por isso as comparações usam sempre dois fatores — as duas
dimensões do IVS-BH 2012.""",
             apresentar="""“Com um fator só, nada passa; com dois, todos os esquemas passam igualmente. Então o critério de
qualidade não escolhe o esquema de pesos: essa escolha é de método.”"""),

        dict(n=31, titulo="Os pesos na solução oblíqua",
             frase="Na base da referência, quanto pesa o fator 1 em cada esquema — e quanto esse peso oscila quando se tira um município.",
             mostra="""À esquerda, uma tabela com os nove esquemas e os pesos dos fatores F1 e F2 na base da referência (renda
original, sem lixo, banheiro graduado). À direita, uma figura com o peso do fator 1 em cada especificação
elegível cujo peso vem dos dados: o ponto é o peso com todos os municípios; a barra vertical, o intervalo
quando se tira um município de cada vez. Duas linhas pontilhadas marcam 60% (o 60/40 do IVS-BH 2012) e 50%.""",
             zero=f"""Na tabela, <b>F1</b> é o fator socioeconômico e <b>F2</b>, o de saneamento. Os esquemas que dependem dos dados
dão ao F1 entre {N.ref_est}% (promax, SS da estrutura) e {N.ref_vari_ss}% (Varimax, SS); os fixos dão 50% ou
60% por definição; o fator único dá 100%, porque só há um fator.

Na figura, barras curtas são especificações estáveis; barras longas, instáveis. As mais longas são as com o
lixo e a `V00495` na promax por comunalidades, em que o peso do F1 pode ir de cerca de 60% a mais de 80%
conforme o município que sai.""",
             numeros=f"""Na base da referência: Varimax SS, {N.ref_vari_ss}%; promax SS da padrão, {N.ref_pad}%; promax SS da
estrutura, {N.ref_est}%; promax por comunalidades, {N.ref_com}%. Todos ficam acima de 60%: os dados dão à
dimensão socioeconômica um pouco mais de peso do que o 60/40 fixo.""",
             apresentar="""“Os pesos que vêm dos dados dão ao fator socioeconômico entre 62% e 67% nesta base — um pouco mais que o
60/40 de Belo Horizonte. E a figura mostra quais especificações oscilam quando se tira um município.”"""),

        dict(n=32, titulo="A AUC de cada especificação",
             frase="A AUC de cada especificação contra as favelas, em ordem — e a linha tracejada da renda sozinha, que nenhuma alcança.",
             mostra=f"""Uma figura com dois painéis. No da esquerda, a AUC global; no da direita, a mediana da AUC dentro dos
municípios. Em cada painel, as {N.n_mun_total} especificações com normalização no município aparecem em ordem
crescente, com cores por rotação (ponto cheio: elegível; vazado: inelegível). A linha tracejada é a renda
sozinha; a estrela, a referência proposta. Embaixo, a AUC média por versão de renda.""",
             zero="""Este gráfico, com os pontos em ordem crescente, mostra de uma vez a faixa de valores de todas as
especificações. A AUC global compara todos os setores juntos; a mediana dentro dos municípios compara cada
favela só com setores da mesma cidade (A.7).

O que se vê: a linha tracejada da renda sozinha fica acima de todos os pontos, nos dois painéis. A estrela
(a referência) não está entre as melhores na AUC — ela foi escolhida pela posição média nos três critérios,
não só por este.""",
             numeros=f"""A AUC média dentro do município, entre as elegíveis, por versão de renda: original {N.auc_r_original},
sem o extremo {N.auc_r_sem_extremo}, mediana municipal {N.auc_r_mediana_mun}. A diferença é de milésimos: a
renda não decide nada aqui.""",
             apresentar="""“Nenhuma especificação alcança a renda sozinha na separação das favelas, em nenhuma das duas medidas. E
as três versões da renda dão a mesma AUC.”"""),

        dict(n=33, titulo="O que o índice acrescenta à renda",
             frase="A divisória da parte 8: se a renda separa melhor, o que o índice tem a mais?",
             mostra="""O número 8 em vermelho, o título "O que o índice acrescenta à renda" e o subtítulo: a renda sozinha separa
melhor; dentro de cada faixa de renda, o índice acrescenta.""",
             zero="""Esta parte responde à pergunta incômoda que atravessa os dois decks.""",
             apresentar="""“A parte 8 responde à pergunta que vocês devem estar fazendo: se a renda separa melhor, para que o
índice?”"""),

        dict(n=34, titulo="A renda sozinha contra o índice",
             frase=f"A renda vence o índice em todas as {N.acr_n} especificações elegíveis; mas, entre setores de renda parecida, o índice vence em todas.",
             mostra=f"""Quatro números grandes: {N.acr_rg} de {N.acr_n} (a renda vence na AUC global), {N.acr_rm} de {N.acr_n} (a renda
vence dentro do município), {N.acr_ie} de {N.acr_n} em vermelho (o índice vence dentro dos decis de renda) e
z ≥ {N.z_min} (o índice soma à renda na regressão logística). Embaixo, uma tabela com as três AUCs na
referência proposta e um bloco sobre a regressão.""",
             zero="""A chave está nos <b>decis de renda</b> (A.7). Em cada município, os setores são divididos em dez grupos de
renda parecida, e a AUC é calculada só entre setores do mesmo grupo. Ali a renda quase não varia, então ela
não consegue separar — e o que o índice separa é informação que a renda não tem: água, esgoto, banheiro,
analfabetismo, cor/raça, aperto.

A <b>regressão logística</b> (A.7) faz a mesma pergunta de outro jeito: um modelo prevê se o setor é favela
pela renda; acrescenta-se o índice; se o modelo melhora, o índice traz informação nova. A <b>estatística
z</b> mede se a melhora é maior que o acaso.""",
             numeros=f"""Na referência proposta: AUC global do índice {N.ref_ig} contra {N.ref_rg} da renda; dentro do município,
{N.ref_im} contra {N.ref_rm}; dentro dos decis de renda, {N.ref_ie} contra {N.ref_re} — aqui o índice ganha com
folga, e a renda cai para não muito acima do acaso (0,5).

Na regressão: somar o índice à renda reduz a deviance (o erro do modelo) em {N.ref_dev}, com z = {N.ref_z} —
muito acima de 2 —, e leva a AUC do modelo de {N.ref_mod} a {N.ref_mod2}. Em toda a grade, o z fica entre
{N.z_min} e {N.z_max}, e o ganho de AUC, em até {N.ganho_max}. Ou seja: o índice acrescenta informação
real, mas pouca, na tarefa de separar favelas.""",
             apresentar="""“A renda separa melhor no geral, mas o índice vence quando se compara setores de renda parecida. Ele
mede o que a renda não mede — e isso é o que se espera de um índice de vulnerabilidade.”""",
             perguntas=[("Se o ganho na regressão é tão pequeno, o índice vale a pena?", "Para separar favelas, ele acrescenta pouco à renda. Mas o objetivo do índice é medir vulnerabilidade à saúde, não identificar favelas. O que os decis mostram é que ele ordena setores de renda parecida por outras condições — exatamente o que um índice composto deve fazer.")]),

        dict(n=35, titulo="A referência proposta — e por que desconfiar",
             frase="A divisória da parte 9: a especificação que os critérios apontam, e as razões para tratá-la como proposta.",
             mostra="""O número 9 em vermelho, o título "A referência proposta — e por que desconfiar" e o subtítulo: uma proposta,
não uma decisão; quatro leituras dos critérios, quatro resultados.""",
             zero="""Os critérios de escolha admitem mais de uma leitura. Esta parte mostra a referência de cada leitura e os
pontos frágeis da principal.""",
             apresentar="""“A parte 9 é a referência proposta — e por que eu não a trataria como decisão.”"""),

        dict(n=36, titulo="Quatro leituras, quatro propostas",
             frase="Cada leitura dos critérios aponta uma especificação diferente — e a principal fica, em média, só por volta do 39º lugar.",
             mostra="""Uma tabela com quatro linhas — as quatro leituras — e as escolhas de cada proposta: renda, lixo, banheiro,
rotação, pesos e normalização, mais o posto médio. A primeira linha, a principal, está em vermelho.""",
             zero=f"""As quatro leituras:

• <b>Principal</b>: estabilidade medida pelo peso do fator 1; AUC na amostra comum. Aponta renda original,
sem lixo, banheiro graduado, promax, 60/40, normalização no município.
• <b>AUC na amostra própria</b>: a mesma, mas com a AUC calculada na base de cada especificação. Troca o
banheiro graduado pela `V00495`.
• <b>Estabilidade pelos pesos das variáveis</b>: mede a estabilidade pelo quanto oscila o peso de cada
variável, e não só o do fator 1. Aponta renda sem o extremo, sem lixo, sem banheiro, promax por
comunalidades.
• <b>Normalização global</b>: a melhor entre as de normalização global. Aponta renda sem o extremo, sem lixo,
sem banheiro, Varimax, 60/40.

O <b>posto médio</b> é a média das posições da especificação nos três critérios; quanto menor, melhor. A
principal fica com {N.posto_pri}: entre as {N.ref_eleg} elegíveis, ela não é a primeira em nada, mas é a que
fica, em média, mais bem colocada. Nenhuma especificação é a melhor em tudo.""",
             numeros=f"""Postos médios: principal {N.posto_pri}; amostra própria {N.posto_pro}; estabilidade pelas variáveis
{N.posto_est}; normalização global {N.posto_glo}. As quatro concordam em duas coisas: <b>sem lixo</b> e
<b>normalização no município</b> (salvo a leitura que, por construção, só olha a global).""",
             apresentar="""“Conforme a leitura dos critérios, a referência muda. Mas há dois consensos: todas tiram o lixo, e as
que podem escolher normalizam dentro do município.”"""),

        dict(n=37, titulo="Por que desconfiar da principal",
             frase="Cinco motivos, todos com número, para tratar a referência principal como proposta e não como decisão.",
             mostra="""Cinco blocos: o critério (a) degenera (com o filete vermelho); medida de outro jeito, a proposta muda; o
60/40 não foi conferido na fonte; a normalização importa; o corte de 0,30 é rígido?""",
             zero=f"""• <b>O critério de estabilidade degenera</b>. Ele mede quanto o peso do fator 1 muda ao tirar um município.
Nos pesos fixos (50/50, 60/40), o peso não muda nunca — é fixado —, e a amplitude é {N.ref_amp} por construção.
A principal é 60/40: ela ganha esse critério sem ter sido testada nele.
• <b>Medida de outro jeito, a proposta muda</b>. Pela estabilidade dos pesos das variáveis, a proposta passa a
ser outra (slide 36).
• <b>O 60/40 não foi conferido na fonte</b>. Os números do Quadro 3 do documento do IVS-BH 2012 (página 7 do
PDF) não saíram na extração do texto. Falta confirmar, no próprio PDF, que é 0,6 para a dimensão
socioeconômica e 0,4 para o saneamento.
• <b>A normalização importa</b>. Normalizando de forma global em vez de no município, {N.muda_bh}% dos setores
mudam de faixa pela regra do IVS-BH e {N.muda_q}% pelos quartis; a correlação de Spearman entre as duas
versões do índice fica em {N.spearman_g} — alta, mas um em cada dez setores muda de faixa.
• <b>O corte de 0,30 é rígido?</b> O IVS-7 com o banheiro graduado ficou de fora por uma comunalidade de
{N.h2_grad}, um milésimo abaixo do corte. Com um corte de 0,29, a lista de elegíveis mudaria.""",
             apresentar="""“A referência principal ganhou em parte por um critério que não a testou, depende de um 60/40 que ainda
precisa ser conferido no documento original, e um corte de comunalidade aplicado ao pé da letra deixou de
fora uma base por um milésimo. São cinco motivos para tratá-la como ponto de partida da discussão.”"""),

        dict(n=38, titulo="As faixas da referência",
             frase="Como a referência se divide em faixas pelas duas regras, e quanto ela concorda com quatro alternativas.",
             mostra=f"""Em cima, uma figura com quatro quadros (matrizes de concordância). Em cada um, as linhas são as faixas da
referência proposta e as colunas, as faixas de uma alternativa, todas pela regra do IVS-BH 2012; cada célula é
a porcentagem de setores. Embaixo, uma tabela com quantos setores caem em cada faixa pela regra do IVS-BH
2012 e pelos quartis municipais.""",
             zero=f"""Uma <b>matriz de concordância</b> cruza duas classificações. Na diagonal (de cima, à esquerda, para baixo,
à direita) ficam os setores que caem na mesma faixa nas duas; fora dela, os que mudam. O rodapé de cada
quadro diz quanto fica na mesma faixa:

• a mesma especificação com normalização global: {N.conc_glo}%;
• o IVS-7 do NB04 (renda original, com lixo, sem banheiro, Varimax): {N.conc_nb04}% — a maior diferença;
• o IVS-6 com Varimax: {N.conc_semlixo}%;
• a referência pela estabilidade das variáveis: {N.conc_est}%.

As duas regras de faixa (A.5): a do <b>IVS-BH 2012</b> usa a média e o desvio-padrão, dentro de cada
município, e dá faixas de tamanhos diferentes; os <b>quartis</b> dividem cada município em quatro grupos
iguais.""",
             numeros=f"""Pela regra do IVS-BH 2012: baixo {N.fx_bh_baixo}, médio {N.fx_bh_medio}, elevado {N.fx_bh_elevado} e muito elevado
{N.fx_bh_muito_elevado} ({N.fx_bh_muito_elevado_pct}% dos setores). Pelos quartis, cerca de um quarto em cada
faixa ({N.fx_q_baixo}, {N.fx_q_medio}, {N.fx_q_elevado} e {N.fx_q_muito_elevado}). "Indefinida" é o setor
que fica sozinho numa faixa do seu município, onde a regra não se aplica: {N.fx_bh_indef} pela regra do
IVS-BH.

A regra do IVS-BH reserva o "muito elevado" para poucos setores, os que se destacam muito da média; os
quartis põem um quarto de cada município nessa faixa. Para um gestor de saúde, a primeira aponta poucas
prioridades; a segunda, muitas.""",
             apresentar="""“A referência concorda em cerca de 90% dos setores com as alternativas próximas, mas só em dois terços
com o IVS-7 original. E a regra de faixas muda muito o tamanho do grupo de maior risco: poucos setores
pela regra de Belo Horizonte, um quarto pelos quartis.”"""),

        dict(n=39, titulo="O que fica para decidir",
             frase="A divisória da parte 10: as escolhas da orientadora, cada uma com os números.",
             mostra="""O número 10 em vermelho, o título "O que fica para decidir" e o subtítulo: as escolhas são da orientadora;
os números de cada uma estão aqui.""",
             zero="""O fecho do deck é uma agenda de decisões.""",
             apresentar="""“Para fechar, o que fica para você decidir.”"""),

        dict(n=40, titulo="As sete escolhas",
             frase="As sete escolhas de método, as opções de cada uma e o que a grade mostra sobre elas.",
             mostra="""Uma tabela de sete linhas e três colunas: a escolha, as opções e o que os números mostram.""",
             zero=f"""Cada escolha, com o resumo dos números:

• <b>Renda</b> — original, sem o extremo ou mediana municipal: empatam (AUC média de {N.auc_r_original},
{N.auc_r_sem_extremo} e {N.auc_r_mediana_mun}). A escolha é de princípio.
• <b>Rotação</b> — sem rotação, Varimax ou promax: elegíveis {N.eleg_semrot}, {N.eleg_vari} e {N.eleg_prom}.
• <b>Pesos na oblíqua</b> — cinco esquemas: passam em igual número; os fixos empatam a estabilidade por
construção.
• <b>Lixo</b> — com ou sem: elegíveis {N.eleg_lixo_com} com lixo e {N.eleg_lixo_sem} sem.
• <b>Banheiro</b> — fora, `V00495` ou graduado: elegíveis {N.eleg_b_fora}, {N.eleg_b_v495} e {N.eleg_b_grad}.
• <b>Normalização</b> — no município ou global: com a global, {N.muda_bh}% dos setores mudam de faixa.
• <b>Faixas</b> — regra do IVS-BH 2012 ou quartis municipais: as distribuições estão no slide 38.""",
             apresentar="""“Estas são as sete escolhas. Para cada uma, a grade mostra o que muda. Algumas os números praticamente
resolvem — a renda não faz diferença; com lixo, quase nada passa —, outras são de princípio.”"""),

        dict(n=41, titulo="As perguntas de método",
             frase="As sete perguntas que os critérios não respondem sozinhos.",
             mostra="""Uma tabela com duas colunas: a pergunta e o porquê dela.""",
             zero=f"""As perguntas, explicadas:

• <b>O critério de estabilidade fica como está, ou mede os pesos das variáveis?</b> As duas leituras dão
propostas diferentes (slide 36).
• <b>O corte de comunalidade de 0,30 é rígido?</b> O IVS-7 com o banheiro graduado ficou de fora por
{N.h2_grad}.
• <b>A regra da grade basta para o lixo sair, ou a saída pede justificativa própria?</b> O IVS-7 do NB04 é
inelegível pela comunalidade da água ({N.h2_agua}); tirar o lixo é uma decisão com peso no artigo.
• <b>Amostra comum ou própria no critério de AUC?</b> A proposta troca o banheiro graduado pela `V00495`.
• <b>O 60/40 confere com o Quadro 3 do PDF?</b> Os números não saíram na extração do texto.
• <b>Que papel a AUC contra favelas deve ter?</b> A renda sozinha vence, e o critério de favela do IBGE olha,
em parte, o próprio saneamento (A.7).
• <b>Os pesos por comunalidades na promax estão certos?</b> A leitura operacional — a comunalidade de cada
variável, somada na dimensão em que ela tem a maior carga — precisa ser confirmada.""",
             apresentar="""“E estas são as perguntas de método que surgiram ao rodar a grade. Nenhuma tem resposta técnica única;
todas pedem uma decisão.”"""),

        dict(n=42, titulo="Onde está cada resultado",
             frase="Onde encontrar cada resultado do deck, para conferir qualquer número.",
             mostra="""Uma tabela com seis linhas: o resultado e onde ele está. No pé, a data em que o deck foi gerado e o
comando para gerá-lo de novo.""",
             zero="""• A <b>entrega</b> à orientadora, com as três rendas e o banheiro graduado: `banco_de_dados/entrega_orientadora/`.
• A <b>fatorial ampliada</b>: o notebook `04b_Analise_Fatorial_Ampliada.ipynb` e as tabelas em
`banco_de_dados/eda/fatorial_ampliada/`.
• A <b>grade do IVS final</b>: o notebook `05_Calculo_IVS_Final.ipynb` e as tabelas em
`banco_de_dados/eda/ivs_especificacoes/`.
• Os <b>relatórios</b>: o do IVS final e o da análise fatorial, em `docs/relatorios/`.
• O <b>deck principal</b>: na raiz de `docs/Apresentacoes_IVS/`.
• O <b>registro de cada fase</b>: os arquivos de estado das demandas e do NB05.

O comando no pé (`node scripts/gerar_deck_demandas_setembro.js`) gera o deck de novo, lendo as tabelas do
dia: se a orientadora escolher uma especificação e as tabelas mudarem, o deck acompanha.""",
             apresentar="""“Qualquer número deste deck pode ser conferido nestes arquivos, e o deck pode ser gerado de novo a
qualquer momento.”"""),
    ]
