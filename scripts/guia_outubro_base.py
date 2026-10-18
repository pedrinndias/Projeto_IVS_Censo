"""Texto do guia das apresentações de outubro: como usar, a Parte A (o mínimo para entender
tudo), o glossário e o fecho.

Não gera nada sozinho: é lido por scripts/gerar_pdf_guia_decks_outubro.py, que passa os
números em N (calculados dos CSVs e do git). Marcação: <b>, <i>; `código` sai em monoespaçada;
linha em branco separa parágrafos; linhas que começam com "• " viram lista.
"""


def como_usar(N):
    return [
        ("secao", "Como usar este guia"),
        ("p", f"""Este guia explica, um por um, os {int(N.slides_crono) + int(N.slides_dem)} slides das duas
apresentações de outubro: a <b>cronologia do projeto</b> ({N.slides_crono} slides) e as <b>demandas de
setembro</b> ({N.slides_dem} slides). Ele foi escrito para quem não sabe nada do assunto — nem o que é um
setor censitário, nem o que é uma análise fatorial, nem o que é um commit. Nada é dado como sabido: cada
termo é explicado na primeira vez em que aparece, e o glossário, no fim, repete todos em ordem alfabética.

O guia tem quatro partes. A <b>Parte A</b> é o mínimo para entender tudo: o projeto, os dados, o que é
um índice, o que é uma análise fatorial, como se valida um índice e como o trabalho fica registrado no
computador. Leia uma vez, com calma, antes dos slides. A <b>Parte B</b> explica a cronologia, slide a
slide. A <b>Parte C</b> explica as demandas de setembro, slide a slide. A <b>Parte D</b> é o glossário:
consulte quando uma palavra travar a leitura."""),
        ("subsecao", "Como cada slide é explicado"),
        ("p", """Todo verbete das Partes B e C tem a mesma estrutura, de propósito, para você saber onde procurar:

• <b>A miniatura do slide</b>, no alto — é o próprio slide, para você saber de qual se trata.
• <b>Em uma frase</b>: a ideia do slide, se você só tiver tempo para uma coisa.
• <b>O que aparece no slide</b>: cada elemento, na ordem em que o olho lê.
• <b>O que isso quer dizer, do zero</b>: os conceitos por trás, sem pressupor nada.
• <b>Como ler os números</b>: o que cada número significa e se ele é bom, ruim ou neutro (só quando há números).
• <b>Como apresentar</b>: uma fala possível, em linguagem de reunião.
• <b>Se perguntarem</b>: as perguntas mais prováveis, com resposta."""),
        ("subsecao", "Se o tempo for curto"),
        ("p", """Leia a Parte A inteira — ela é a base de tudo. Depois, de cada slide, leia só "Em uma frase" e
"Como apresentar". Na véspera de apresentar, releia os "Se perguntarem" dos slides com números."""),
        ("caixa", "De onde vêm os números deste guia", f"""Nenhum número que vem de planilha foi copiado à mão: o
programa que gera este guia lê os mesmos arquivos de dados e o mesmo histórico do git que geram os slides,
e escreve os números nos textos na hora. Se um dado mudar, basta gerar o guia de novo, e ele muda junto
com os slides. Os números que só existem em documento — decisões de método registradas no GUIA do projeto,
contagens das auditorias, as demandas de julho — aparecem como estão no documento citado. Este guia foi
gerado em {N.hoje}."""),
    ]


def abertura_a(N):
    return """Esta parte junta, em ordem, tudo o que é preciso saber para que os slides façam sentido. Ela
começa pelo problema que o projeto quer resolver, passa pelos dados e pelas contas, e termina no modo como
o trabalho fica registrado. Não há fórmula que não venha acompanhada de um exemplo."""


def parte_a(N):
    return [
        ("secao", "A.1 O projeto, em palavras simples"),
        ("p", """Imagine que a secretaria de saúde de uma cidade precisa decidir para onde mandar mais equipes,
mais agentes comunitários, mais vacinação. Ela quer saber em quais pedaços da cidade as pessoas estão mais
expostas a adoecer por causa das condições em que vivem: casa sem esgoto, água que não chega pela torneira,
lixo que não é recolhido, muita gente dividindo poucos cômodos, adultos que não sabem ler, renda baixa.
Nenhuma dessas coisas, sozinha, diz tudo. E ninguém mede "vulnerabilidade" diretamente — não existe um
termômetro para isso.

O que se faz, então, é juntar vários desses sinais num número só, um <b>índice</b>. É isso que o projeto
constrói: o <b>Índice de Vulnerabilidade à Saúde</b>, o <b>IVS</b>. Ele é <b>intraurbano</b>, ou seja,
compara pedaços de uma mesma cidade entre si (um bairro com outro, um quarteirão com outro), e não uma
cidade com outra.

A ideia não é nova. Em 2012, a Secretaria Municipal de Saúde de Belo Horizonte publicou o seu IVS,
calculado com os dados do Censo de 2010 — no projeto, ele é chamado de <b>IVS-BH 2012</b> e é a
referência de método. O projeto refaz esse índice com os dados do <b>Censo de 2022</b> e o estende para
<b>70 municípios</b> de todas as regiões do país: os municípios do estudo ELSI-Brasil (explicado em A.3)."""),
        ("tabela", ["Item", "Detalhe"], [
            ["Quem", "Pedro Dias Soares, bolsista de Iniciação Científica (IC)"],
            ["Onde", "Fiocruz Minas — Instituto René Rachou (IRR), em Belo Horizonte"],
            ["Quando", "março de 2026 a fevereiro de 2027"],
            ["O que entrega", "um Relatório Final de IC e um artigo científico submetido a uma revista"],
        ], [3.2, 13.0]),
        ("p", """<b>Iniciação Científica</b> é o programa em que um estudante de graduação trabalha num projeto de
pesquisa sob a orientação de um pesquisador — a <b>orientadora</b>, que aparece muito nos slides, porque é
ela quem pede as análises (as <b>demandas</b>) e quem toma as decisões de método."""),

        ("secao", "A.2 De onde vêm os dados: o Censo e o setor censitário"),
        ("p", """O <b>Censo Demográfico</b> é a contagem de toda a população do país, feita pelo <b>IBGE</b>
(Instituto Brasileiro de Geografia e Estatística). Recenseadores visitam cada domicílio e fazem perguntas:
quantas pessoas moram ali, de onde vem a água, para onde vai o esgoto, quem sabe ler, quanto ganha a pessoa
responsável. A edição usada aqui é a de 2022.

Para proteger as pessoas, o IBGE não publica as respostas de cada casa. Ele publica <b>contagens por área
pequena</b>. A menor dessas áreas é o <b>setor censitário</b>: um pedaço de território desenhado para que
um único recenseador consiga percorrê-lo. Na cidade, um setor costuma ser um conjunto de poucos quarteirões.
O Brasil inteiro tem 468.099 setores. Os 70 municípios do projeto têm, juntos, {setores} setores.

Cada setor tem um código de 15 dígitos. Nos slides aparece o setor `310620005650366`: os sete primeiros
dígitos (`3106200`) são o código do município — Belo Horizonte —, e o resto identifica o setor dentro dele.

O setor é a <b>unidade de análise</b> do projeto: o IVS é calculado para cada setor, não para cada
pessoa e não para cada cidade.""".format(setores=N.setores_base)),
        ("subsecao", "As variáveis: códigos que são contagens"),
        ("p", """Cada informação do Censo vem numa coluna com um código, como `V00001` ou `V00901`. Quase todas são
<b>contagens</b> — "quantos domicílios deste setor têm tal coisa" ou "quantas pessoas deste setor são
assim". As que mais aparecem nos slides:

• `V00001` — <b>domicílios particulares permanentes ocupados</b>. Domicílio <i>particular</i> é o de uma
família (não é hotel, asilo ou presídio, que são <i>coletivos</i>); <i>permanente</i> é o construído para
morar (não é uma barraca, que seria <i>improvisado</i>); <i>ocupado</i> é o que tinha morador na data do
Censo. É o total de casas "normais" com gente dentro — o denominador mais usado no projeto.
• `V00900` e `V00901` — pessoas de 15 anos ou mais que <i>sabem</i> e que <i>não sabem</i> ler e escrever.
• `V06004` — rendimento médio mensal da pessoa responsável pelo domicílio, no setor.
• `V00236`, `V00237`, `V00238` e `V00495` — as partes da falta de banheiro, explicadas na Parte C.
• `V00199` — domicílios com água canalizada (que chega por cano até dentro de casa)."""),
        ("subsecao", "O sigilo"),
        ("p", """Quando uma contagem é muito pequena — por exemplo, um setor em que só duas pessoas não sabem ler —,
publicar o número poderia permitir identificar essas pessoas. Nesses casos o IBGE troca o número por um
"X": é o <b>sigilo</b>. No projeto, o X vira <b>dado ausente</b>, nunca zero. Por quê? Porque zero seria
uma mentira (há gente ali, só não se sabe quantos), e porque o sigilo não cai ao acaso: ele cai justamente
onde a contagem é pequena. No analfabetismo, por exemplo, o sigilo aparece nos setores com poucos
analfabetos — os de melhor situação. Trocar o X por zero empurraria esses setores para uma situação ainda
melhor do que a real; trocar por qualquer outro número seria inventar dado.

A consequência prática aparece em vários slides: toda vez que uma variável com muito sigilo entra na
análise, setores "caem" da base, porque ficam com algum dado ausente."""),
        ("subsecao", "Os oito arquivos"),
        ("p", """O IBGE publica os dados por setor em vários arquivos, um por tema. O projeto usa oito: o básico
(identificação e população), dois de características do domicílio (o primeiro com os totais de domicílios,
o segundo com água, esgoto, lixo e banheiro), alfabetização, cor ou raça, renda do responsável, demografia
(idade) e parentesco. O de parentesco era usado no começo, por causa da variável `V01042`, e foi
abandonado em maio — a história está na Parte B."""),

        ("secao", "A.3 Por que 70 municípios: o ELSI-Brasil"),
        ("p", """O <b>ELSI-Brasil</b> é o Estudo Longitudinal da Saúde dos Idosos Brasileiros, coordenado pela
Fiocruz. Ele acompanha uma amostra de pessoas de 50 anos ou mais que moram em <b>70 municípios</b>
espalhados pelas cinco regiões do país. <i>Longitudinal</i> quer dizer que as mesmas pessoas são
entrevistadas de novo de tempos em tempos, para ver como a saúde delas muda.

O projeto calcula o IVS para todos os setores desses 70 municípios. Com isso, a vulnerabilidade do lugar
onde cada participante mora pode, por exemplo, ser relacionada à saúde dele. É por isso que os slides falam
em "recorte ELSI", "base ELSI" e "70 municípios"."""),
        ("subsecao", "O recorte urbano"),
        ("p", """O IVS é intraurbano, então só os setores <b>urbanos</b> entram na análise. Cada setor tem, no
Censo, a sua <b>situação</b> (`SITUACAO`): urbana ou rural. O filtro é aplicado na hora da análise, e não
na hora de extrair os dados — a base completa continua guardada, para que dê para conferir e desfazer.
Dos setores dos 70 municípios, 104.108 são urbanos."""),

        ("secao", "A.4 Indicador: numerador, denominador e porcentagem"),
        ("p", """Um <b>indicador</b> é uma conta que transforma contagens em algo comparável. Pense em dois setores:
o setor A tem 30 domicílios sem esgoto, o setor B tem 300. O B está pior? Depende do tamanho. Se o B tiver
3.000 domicílios, são 10%; se o A tiver 60, são 50%. Por isso se divide pelo total:

• o <b>numerador</b> é o que se quer medir (domicílios sem esgoto);
• o <b>denominador</b> é o total de referência (todos os domicílios do setor);
• o resultado é uma <b>proporção</b>, um número entre 0 e 1 — que, vezes 100, é a porcentagem.

Nos nomes das colunas do projeto, `pct_` quer dizer proporção (de "percentual"): `pct_esgoto_inad` é a
proporção de domicílios com esgoto inadequado; `pct_analfab`, a de analfabetos entre as pessoas de 15 anos
ou mais."""),
        ("exemplo", "Por que o denominador importa", """Em maio, o projeto trocou o denominador de `V01042` (que conta
<i>pessoas responsáveis</i>, no arquivo de parentesco) por `V00001` (que conta <i>domicílios</i>). Parece
detalhe, mas não é: o IVS-BH 2012 dividia por domicílios, e só com o mesmo denominador os dois índices
ficam comparáveis. Trocar o denominador muda todos os indicadores de uma vez."""),
        ("subsecao", "Taxa e razão"),
        ("p", """Uma <b>taxa</b> tem no denominador a população inteira de referência: analfabetos ÷ (todas as pessoas
de 15 anos ou mais). Ela nunca passa de 1 (100%). Uma <b>razão</b> divide uma coisa por outra que não a
contém: analfabetos ÷ alfabetizados. Ela pode passar de 1 — num setor com 60 analfabetos e 40 alfabetizados,
dá 1,5. A primeira versão do projeto calculava o analfabetismo como razão, e isso foi corrigido em maio.

A <b>razão de moradores</b> (`razao_moradores`) é uma razão de propósito: moradores ÷ domicílios, a média
de pessoas por casa — um sinal de aperto."""),
        ("subsecao", "O complemento"),
        ("p", """Às vezes é mais fácil contar quem <i>tem</i> do que quem <i>não tem</i>. O Censo conta bem os
domicílios <i>com</i> água canalizada (`V00199`), uma contagem grande que quase nunca cai em sigilo. A
proporção <i>sem</i> água canalizada sai então pelo <b>complemento</b>: 1 − (com água ÷ total). Se 92% têm,
8% não têm."""),

        ("secao", "A.5 O índice composto: como sete números viram um"),
        ("p", """Um <b>índice composto</b> junta vários indicadores numa nota só, como uma média de boletim que
junta as notas de várias matérias. Montá-lo tem quatro passos."""),
        ("subsecao", "1. Escolher os componentes"),
        ("p", """O IVS-BH 2012 usa sete indicadores, e por isso o projeto chama essa base de <b>IVS-7</b>. Eles se
dividem em duas <b>dimensões</b> (dois grandes temas):"""),
        ("tabela", ["Dimensão", "Indicador", "O que mede"], [
            ["Saneamento", "água inadequada (`pct_agua_inad`)", "domicílios sem abastecimento de água adequado"],
            ["Saneamento", "esgoto inadequado (`pct_esgoto_inad`)", "domicílios sem rede de esgoto ou fossa adequada"],
            ["Saneamento", "lixo inadequado (`pct_lixo_inad`)", "domicílios sem coleta de lixo porta a porta"],
            ["Socioeconômica", "razão de moradores (`razao_moradores`)", "pessoas por domicílio: o aperto"],
            ["Socioeconômica", "analfabetismo (`pct_analfab`)", "pessoas de 15+ que não sabem ler e escrever"],
            ["Socioeconômica", "renda (`renda_media`)", "rendimento médio do responsável — entra invertida"],
            ["Socioeconômica", "cor ou raça (`pct_raca_pretpardind`)", "pessoas pretas, pardas e indígenas"],
        ], [3.0, 5.6, 7.6]),
        ("p", """Quando o lixo sai, a base vira <b>IVS-6</b>. Nos slides aparecem outras bases, com variáveis a mais
(água que não chega, falta de banheiro, moradia não convencional) — a Parte C explica cada uma."""),
        ("subsecao", "2. Pôr tudo na mesma régua: a normalização"),
        ("p", """Os indicadores estão em escalas diferentes: proporções vão de 0 a 1, a renda vai de algumas centenas
a dezenas de milhares de reais, a razão de moradores fica em torno de 3. Para somar, é preciso pôr todos na
mesma régua. A <b>normalização min-max</b> faz isso: em cada indicador, o pior setor vira 1, o melhor vira 0,
e os outros ficam no meio, na proporção certa. A conta é (valor − mínimo) ÷ (máximo − mínimo)."""),
        ("exemplo", "Exemplo de normalização", """Três setores com esgoto inadequado de 10%, 30% e 60%. O mínimo é 10%,
o máximo é 60%, e a distância entre eles é 50 pontos. O primeiro fica em (10 − 10) ÷ 50 = 0; o segundo em
(30 − 10) ÷ 50 = 0,4; o terceiro em (60 − 10) ÷ 50 = 1."""),
        ("p", """Dois detalhes importam nos slides. Primeiro, a <b>renda entra invertida</b>: renda alta é boa, ao
contrário dos outros indicadores, em que mais é pior; invertendo, todos passam a dizer "mais = mais
vulnerável". Segundo, a normalização pode ser feita <b>no município</b> (mínimo e máximo de cada cidade) ou
de forma <b>global</b> (mínimo e máximo de todos os setores juntos). No município, o índice diz quem está
pior <i>dentro da sua cidade</i>; no global, compara todo mundo com todo mundo.

E um alerta: um valor extremo estraga a régua. Se um setor tem renda de R$ 170 mil e o segundo mais rico tem
R$ 45 mil, o de R$ 170 mil vira o máximo e todos os outros ficam espremidos perto de zero. É a história do
"setor extremo" de Belo Horizonte, nos dois decks."""),
        ("subsecao", "3. Dar pesos e somar"),
        ("p", """O índice é a soma dos indicadores normalizados, cada um multiplicado por um <b>peso</b>. Os pesos
dizem quanto cada parte conta. Podem vir de uma regra fixa — por exemplo, 60% para a dimensão
socioeconômica e 40% para o saneamento (o "60/40") ou metade para cada uma (o "50/50") — ou podem vir dos
próprios dados, por uma análise fatorial (A.6). Escolher os pesos é uma das decisões que ficam com a
orientadora."""),
        ("subsecao", "4. Cortar em faixas"),
        ("p", """O índice final vai de 0 a 1. Para usar na prática, ele é cortado em <b>faixas de risco</b>: baixo,
médio, elevado e muito elevado. Há duas regras em teste:

• a <b>regra do IVS-BH 2012</b>, que usa a média e o desvio-padrão. O <b>desvio-padrão</b> mede o quanto os
valores costumam se afastar da média. Quem fica muito acima da média cai em "muito elevado", e assim por
diante. Com essa regra, as faixas têm tamanhos diferentes;
• os <b>quartis municipais</b>: dentro de cada município, os setores são ordenados e divididos em quatro
grupos do mesmo tamanho. Cada faixa fica com um quarto dos setores."""),

        ("secao", "A.6 Análise fatorial, sem fórmula"),
        ("p", """A análise fatorial é a técnica que o projeto usa para descobrir <b>como os indicadores se agrupam</b>
e, daí, <b>quanto cada grupo deve pesar</b>. É o assunto mais técnico dos dois decks. Aqui vai a ideia,
passo a passo."""),
        ("subsecao", "Variáveis que andam juntas"),
        ("p", """Pense nas notas de um aluno em matemática, física e química. Elas costumam subir e descer juntas,
porque refletem uma mesma coisa que ninguém mede diretamente — algo como "facilidade com exatas". Na
análise fatorial, essa coisa escondida se chama <b>fator</b>.

Com os setores acontece o mesmo. Onde a renda é baixa, o analfabetismo tende a ser alto e a casa tende a
ser mais cheia: esses indicadores andam juntos e formam um fator <b>socioeconômico</b>. Onde falta esgoto,
costuma faltar água: formam um fator de <b>saneamento</b>. A análise fatorial encontra esses fatores nos
dados, sem que ninguém diga de antemão quais são."""),
        ("subsecao", "Correlação, e por que Spearman"),
        ("p", """O quanto duas variáveis andam juntas se mede pela <b>correlação</b>, um número de −1 a 1. Perto de 1:
sobem juntas; perto de −1: uma sobe quando a outra desce; perto de 0: não têm relação. O projeto usa a
<b>correlação de Spearman</b>, que em vez dos valores usa as <b>posições</b> (os <b>postos</b>: primeiro,
segundo, terceiro…). Assim, um setor com renda absurda conta como "o primeiro", e não como um valor gigante
que distorce tudo."""),
        ("subsecao", "Os dados servem para isso? KMO, MSA e Bartlett"),
        ("p", """Antes de procurar fatores, testa-se se os dados se prestam a isso:

• o <b>KMO</b> (de Kaiser-Meyer-Olkin) vai de 0 a 1 e diz se as correlações são <i>compartilhadas</i> por
várias variáveis, e não só por pares isolados. Abaixo de 0,5 é inaceitável; de 0,7 para cima, bom; de 0,8
para cima, muito bom;
• o <b>MSA</b> é o KMO de cada variável, separado: mostra qual variável conversa pouco com as outras;
• o <b>teste de Bartlett</b> verifica se existe alguma correlação. Se as variáveis fossem independentes,
não haveria fator para achar. Com dezenas de milhares de setores, ele sempre dá "sim"."""),
        ("subsecao", "Quantos fatores: autovalor, Kaiser e Horn"),
        ("p", """Cada fator encontrado resume uma parte da informação de todas as variáveis. O <b>autovalor</b> mede
quanto: um autovalor de 3 quer dizer que aquele fator vale por três variáveis. Para decidir quantos fatores
manter, há duas regras:

• a <b>regra de Kaiser</b>: fica o fator com autovalor maior que 1 (que vale por mais de uma variável);
• a <b>regra de Horn</b> (ou análise paralela): gera dados aleatórios do mesmo tamanho, calcula os
autovalores que o puro acaso produziria, e só mantém o fator que supera o acaso. É mais exigente.

Nos slides, "Fatores K/H" mostra o que cada regra indica: "2 / 2" é dois por Kaiser e dois por Horn. O
gráfico desses autovalores, em ordem decrescente, se chama <b>scree plot</b> (gráfico de cotovelo)."""),
        ("subsecao", "Cargas e comunalidade"),
        ("p", """A <b>carga fatorial</b> diz o quanto uma variável "pertence" a um fator: vai de −1 a 1, e perto de 1
quer dizer muito. A <b>comunalidade</b> diz quanto de uma variável os fatores conseguem explicar, juntos: vai
de 0 a 1. Uma variável com comunalidade de 0,25 tem só um quarto do seu comportamento explicado pelos
fatores; o resto é dela, não conversa com as outras. No projeto, uma especificação só é aceita se toda
variável tiver comunalidade de pelo menos 0,30 e carga máxima de pelo menos 0,40."""),
        ("subsecao", "Rotação: Varimax e promax"),
        ("p", """Depois de achar os fatores, os eixos podem ser "girados" para que cada variável fique perto de um
fator só — o que torna o resultado mais fácil de interpretar. Isso é a <b>rotação</b>.

• <b>Sem rotação</b>, o primeiro fator costuma pegar quase tudo: é o fator "geral".
• A <b>Varimax</b> gira mantendo os fatores independentes entre si, como eixos em ângulo reto: a correlação
entre eles é zero.
• A <b>promax</b> deixa os fatores se correlacionarem, como eixos que não formam ângulo reto (rotação
<b>oblíqua</b>). A correlação entre os fatores se chama <b>Φ</b> (a letra grega "fi"). Com rotação oblíqua
surgem duas tabelas de cargas: a <b>matriz padrão</b>, com o efeito próprio de cada fator, e a <b>matriz
estrutura</b>, com a correlação simples entre variável e fator — que inclui a parte que os dois fatores
compartilham."""),
        ("subsecao", "Dos fatores aos pesos"),
        ("p", """Cada fator tem uma "força": a <b>soma dos quadrados das cargas</b>, abreviada <b>SS</b> (do inglês
<i>sum of squares</i>). Dividindo a força de cada fator pela soma das forças, saem os pesos em porcentagem.
Por exemplo, 65% para o fator socioeconômico e 35% para o de saneamento. Na promax, a força pode ser
calculada com a matriz padrão ou com a estrutura, e dá números diferentes. Outras regras repartem pelas
<b>comunalidades</b>, ou fixam o peso (50/50, 60/40)."""),
        ("caixa", "Três termos que aparecem de passagem", """<b>Eixo principal</b> e <b>componentes principais</b> são
dois jeitos de extrair os fatores; não é preciso conhecer a diferença para ler os slides. Um <b>caso de
Heywood</b> é quando a conta dá uma comunalidade acima de 1, o que é impossível e indica problema. Os
<b>escores</b> são as notas de cada setor em cada fator."""),

        ("secao", "A.7 O índice funciona? A validação contra as favelas"),
        ("p", """Como saber se o índice mede o que promete? Uma forma é compará-lo com algo que não foi usado para
construí-lo. O projeto usa a classificação de <b>Favelas e Comunidades Urbanas</b>, a <b>FCU</b>: o IBGE
marca cada setor que é favela ou comunidade urbana (no campo `CD_TIPO`, valor 1). Se o índice mede
vulnerabilidade, os setores de favela deveriam, em geral, ter índice mais alto."""),
        ("subsecao", "A AUC, explicada com um sorteio"),
        ("p", """Sorteie um setor de favela e um setor que não é favela, e veja qual dos dois tem o índice maior.
Repita isso milhares de vezes. A <b>AUC</b> é a proporção de vezes em que o setor de favela ganhou.

• AUC de 0,5: o índice acerta tanto quanto uma moeda — não separa nada;
• AUC de 1,0: o setor de favela ganha sempre;
• AUC de 0,8: o setor de favela tem índice maior em 80% dos pares.

O nome vem do gráfico de onde ela sai, a <b>curva ROC</b>: AUC é a "área sob a curva" (<i>area under the
curve</i>). Uma curva que sobe rápido para o canto de cima, à esquerda, tem área grande; a diagonal é o
acaso."""),
        ("subsecao", "A comparação que importa: a renda sozinha"),
        ("p", """Nos slides, a AUC do índice é sempre posta ao lado da AUC da <b>renda invertida sozinha</b>. Se a
renda, sozinha, separa as favelas melhor do que o índice, o índice não está ajudando a <i>separar
favelas</i>. Isso não quer dizer que o índice não serve: um índice de vulnerabilidade mede mais do que a
condição de favela. Mas é um sinal importante, e os decks mostram que é o que acontece.

Há também uma ressalva de <b>circularidade</b>: para marcar um setor como favela, o IBGE olha em parte as
mesmas condições de infraestrutura (água, esgoto) que entram no índice. Um índice com saneamento leva uma
vantagem "de graça" nessa comparação."""),
        ("subsecao", "Comparar só o comparável: dentro do município e dentro da faixa de renda"),
        ("p", """A AUC <b>global</b> compara setores de todos os municípios juntos. A AUC <b>dentro do município</b>
compara cada favela só com setores da mesma cidade, e depois resume (pela mediana). A AUC <b>dentro dos
decis de renda</b> vai além: em cada município, os setores são divididos em dez grupos de renda parecida
(os <b>decis</b>), e só se comparam setores do mesmo grupo. Ali a renda já não ajuda, porque é quase igual
— e o que sobra mostra se o índice traz informação <i>além</i> da renda."""),
        ("subsecao", "Regressão logística, deviance e z"),
        ("p", """A <b>regressão logística</b> é um modelo que estima a chance de um setor ser favela a partir de outras
variáveis. Ajusta-se primeiro um modelo só com a renda, depois um com a renda e o índice. Se acrescentar o
índice melhora o modelo, o índice traz informação nova. A <b>deviance</b> mede o quanto o modelo erra
(menor é melhor), e a <b>estatística z</b> mede se a contribuição do índice é maior do que o acaso
explicaria. Como regra prática, z acima de 2 já é considerado significativo."""),

        ("secao", "A.8 Quanto o resultado depende de detalhes: a sensibilidade"),
        ("p", """Todo resultado estatístico tem alguma incerteza. Uma técnica comum para medi-la é o <b>bootstrap</b>:
refazer a análise centenas de vezes, cada vez com uma amostra sorteada dos próprios dados, e ver quanto o
resultado oscila. Ele faz sentido quando os dados são uma amostra. Aqui não são: o projeto tem todos os
setores urbanos dos 70 municípios.

A pergunta útil é outra: <b>quanto o resultado depende de um município?</b> Para responder, a análise é
refeita tirando um município de cada vez: uma rodada com todos e mais 70, uma sem cada município, num total
de {rodadas} rodadas. Se tirar São Paulo muda muito os pesos, o resultado depende demais de São Paulo. Isso
é a <b>sensibilidade por município</b>.

As diferenças entre porcentagens se medem em <b>pontos percentuais</b> (p.p.): de 65% para 63% são 2 p.p.
(e não "2%")."""
         .format(rodadas=N.rodadas)),

        ("secao", "A.9 Especificação, grade, elegível e referência"),
        ("p", f"""Para construir o IVS final, há várias escolhas em aberto: qual versão da renda usar, se o lixo
entra, se a falta de banheiro entra (e em qual versão), qual rotação, como dividir os pesos, como
normalizar. Cada combinação dessas escolhas é uma <b>especificação</b>. Testar todas as combinações é
montar uma <b>grade</b>: são {N.n_esp} especificações.

Uma especificação é <b>elegível</b> quando passa em critérios mínimos de qualidade (KMO, MSA, comunalidade
e carga), fixados <i>antes</i> de rodar a grade — para que ninguém escolha a especificação olhando o
resultado. Das {N.n_esp}, {N.n_eleg} são elegíveis.

Entre as elegíveis, a <b>referência proposta</b> é a de melhor <b>posição média</b> em três critérios com o
mesmo peso: <b>estabilidade</b> (quanto o peso muda ao tirar um município), <b>validação</b> (a AUC dentro
do município) e <b>parcimônia</b> (menos variáveis é melhor). É uma <i>proposta</i>, não uma decisão:
escolher a especificação final é papel da orientadora."""),

        ("secao", "A.10 O código, o git e os commits"),
        ("p", """O projeto inteiro mora numa pasta no computador, o <b>repositório</b>, com os dados, os programas,
os documentos e as apresentações. O <b>git</b> é o programa que guarda a história dessa pasta.

Cada vez que um trabalho fica pronto, ele é registrado num <b>commit</b>: uma "foto" das mudanças, com
data, autor e uma mensagem que diz o que mudou. Cada commit tem um identificador curto, o <b>hash</b> (por
exemplo, `2d0c909`), que permite voltar exatamente àquela versão. A cronologia se apoia nessas fotos: é
por isso que ela tem datas tão precisas.

As mensagens dos commits começam com um prefixo que diz o tipo de mudança:

• `feat` — uma funcionalidade nova (uma análise, um script, uma coluna);
• `fix` — uma correção;
• `docs` — documentação (relatórios, guias, READMEs);
• `chore` — manutenção (configurações, organização);
• `data` ou `dados` — dados regerados;
• `test` ou `teste` — testes automáticos;
• `refactor` — reorganização do código sem mudar o resultado.

Um <b>branch</b> é uma linha de trabalho dentro do repositório; a principal se chama `main`."""),
        ("subsecao", "Notebooks, scripts, módulos e testes"),
        ("p", """• Um <b>notebook</b> (Jupyter) é um documento que mistura texto, código e resultados — tabelas e
gráficos — na ordem em que a análise acontece. Os do projeto são numerados: NB01 (extração dos dados e
filtro dos 70 municípios), NB02 (análise descritiva), NB04 (análise fatorial), NB04b (fatorial ampliada) e
NB05 (o IVS final).
• Um <b>script</b> é um programa que roda sozinho e grava um resultado (uma tabela, um gráfico, um deck).
Ficam na pasta `scripts/`.
• Um <b>módulo</b> é código compartilhado, usado por vários notebooks e scripts. O do projeto é
`src/ivs_censo`, onde vivem as fórmulas de todos os indicadores — assim, a fórmula é a mesma em todo lugar.
• Um <b>CSV</b> é uma tabela salva como texto, com os valores separados por vírgula ou ponto e vírgula. A
maioria dos números dos slides sai de arquivos CSV.
• Um <b>teste</b> é um pequeno programa que confere se o código dá o resultado esperado. O projeto tem
{testes} testes.
• <b>EDA</b> (do inglês <i>exploratory data analysis</i>) é a análise exploratória: descrever os dados,
medir, comparar e procurar problemas antes de construir qualquer modelo.""".replace("{testes}", N.testes)),
        ("subsecao", "Decks gerados por script"),
        ("p", """Nos slides aparece muito a expressão "gerado por script". Quer dizer que ninguém digitou os números
no slide: um programa lê as tabelas e monta a apresentação. Se uma tabela muda, roda-se o programa de novo e
o slide muda junto — sem chance de o slide ficar com um número velho. Os dois decks de outubro foram feitos
assim, e este guia também.

As <b>anotações do apresentador</b> são o texto escondido embaixo de cada slide. No PowerPoint, aparecem em
<i>Exibir › Anotações</i> e, durante a apresentação, só na tela de quem apresenta. Os dois decks trazem ali
detalhes que não couberam no slide."""),

        ("secao", "A.11 As duas apresentações, lado a lado"),
        ("tabela", ["", "Cronologia do projeto", "Demandas de setembro"], [
            ["Pergunta que responde", "O que aconteceu, quando e por quê?", "O que foi pedido, o que foi feito e o que os números dizem?"],
            ["Para quem", "Quem precisa entender a trajetória inteira", "A reunião de decisão com a orientadora"],
            ["Organização", "Por data: sete capítulos e três leituras transversais", "Por demanda: dez partes, da pergunta à decisão"],
            ["De onde vêm os dados", "Histórico do git, GUIA do projeto e CSVs", "CSVs da fatorial ampliada e da grade do NB05"],
            ["Tamanho", f"{N.slides_crono} slides", f"{N.slides_dem} slides"],
        ], [3.6, 6.3, 6.3]),
        ("p", """As duas seguem a mesma identidade visual dos outros decks do projeto: fundo branco, letra serifada,
uma régua fina sob o título e o vermelho reservado ao que merece destaque. Todo slide com dado tem, no pé,
uma linha "Fonte:" dizendo de qual arquivo saiu o que está ali. As divisórias de parte trazem um número
grande em vermelho; o número pequeno no canto inferior direito é o número do slide."""),
    ]


def abertura_d(N):
    return """Os termos que aparecem nos dois decks e neste guia, em ordem alfabética. Cada definição foi
escrita para ser entendida sozinha; quando um termo depende de outro, o outro também está aqui."""


def glossario(N):
    termos = [
        ("50/50 e 60/40", "Pesos fixos para as duas dimensões do índice: metade para cada uma, ou 60% para a socioeconômica e 40% para o saneamento (a proporção atribuída ao IVS-BH 2012, ainda a confirmar no PDF original)."),
        ("Agregados por setor", "Os dados do Censo publicados como contagens por setor censitário, e não por pessoa."),
        ("Amostra comum", "O conjunto de setores presente em todas as versões comparadas, para que a comparação não dependa de qual versão perdeu mais setores por dado ausente. Seu contrário é a amostra própria de cada versão."),
        ("Análise fatorial", "Técnica que encontra, nos dados, grupos de variáveis que andam juntas (os fatores) e diz quanto cada variável pertence a cada grupo."),
        ("Anotações do apresentador", "O texto escondido embaixo de cada slide, visível só para quem apresenta."),
        ("AUC", "Área sob a curva ROC. Probabilidade de um setor de favela, sorteado, ter índice maior que um setor que não é favela, também sorteado. 0,5 é o acaso; 1 é a separação perfeita."),
        ("Autovalor", "Quanto da informação das variáveis um fator resume. Autovalor 3: o fator vale por três variáveis."),
        ("Backup/", "A pasta do repositório com o legado: as versões antigas da pipeline (Fases 1 e 2), guardadas como histórico."),
        ("Bartlett (teste de)", "Teste que verifica se as variáveis têm alguma correlação entre si. Sem correlação, não há fator para achar."),
        ("Base", "Na grade do NB05, uma combinação de renda, lixo e banheiro — o conjunto de variáveis que vai para a análise fatorial. São 18 bases."),
        ("Bootstrap", "Refazer uma análise muitas vezes com amostras sorteadas dos próprios dados, para medir a incerteza. Não foi usado aqui: o projeto trabalha com todos os setores, não com uma amostra."),
        ("Branch", "Uma linha de trabalho dentro do repositório git. A principal se chama main."),
        ("Caçamba", "Contêiner comunitário de lixo (variável `V00398`). Pelo método do IVS-BH 2012, conta como destino inadequado: só a coleta porta a porta é adequada."),
        ("Carga fatorial", "O quanto uma variável pertence a um fator, de −1 a 1."),
        ("Cenário (S0 a S7)", "Na fatorial ampliada, cada conjunto de variáveis testado: S0 é o IVS-7 do NB04, S1 é sem o lixo, S2 a S5 acrescentam uma variável cada, S6 junta as quatro e S7 é o S6 sem o lixo."),
        ("Censo Demográfico", "A contagem de toda a população, feita pelo IBGE. A edição usada é a de 2022."),
        ("Commit", "Registro de uma mudança no git, com data, autor e mensagem. É a unidade da cronologia."),
        ("Complemento", "1 menos uma proporção: se 92% têm água canalizada, o complemento, 8%, é a proporção sem."),
        ("Comunalidade", "Quanto de uma variável os fatores explicam juntos, de 0 a 1. Abaixo de 0,30, a variável conversa pouco com as outras e a especificação deixa de ser elegível."),
        ("Correlação", "Medida, de −1 a 1, de quanto duas variáveis andam juntas."),
        ("CSV", "Tabela salva como texto, com os valores separados por vírgula ou ponto e vírgula."),
        ("Decil", "Cada um dos dez grupos de mesmo tamanho em que se divide uma lista ordenada. \"Decis de renda\": os setores do município divididos em dez faixas de renda."),
        ("Deck", "Uma apresentação de slides."),
        ("Denominador", "O total pelo qual se divide para fazer uma proporção. Nos indicadores de domicílio do projeto, é `V00001`."),
        ("Desvio-padrão (DP)", "O quanto os valores costumam se afastar da média."),
        ("Deviance", "Medida do erro de um modelo estatístico; quanto menor, melhor o ajuste."),
        ("Dimensão", "Um grande tema do índice: saneamento ou socioeconômica."),
        ("EDA", "Análise exploratória de dados: descrever, medir e procurar problemas antes de modelar. A EDA Central teve duas rodadas, em agosto e setembro."),
        ("Elegível", "Especificação que passa nos quatro critérios mínimos: KMO ≥ 0,70, MSA ≥ 0,50, comunalidade ≥ 0,30 e carga máxima ≥ 0,40."),
        ("ELSI-Brasil", "Estudo Longitudinal da Saúde dos Idosos Brasileiros, coordenado pela Fiocruz, com participantes em 70 municípios."),
        ("Escore", "A nota de cada setor em cada fator."),
        ("Especificação", "Uma combinação completa de escolhas para calcular o IVS: renda, lixo, banheiro, rotação, esquema de peso e normalização."),
        ("Faixa de risco", "Categoria do índice: baixo, médio, elevado ou muito elevado."),
        ("Fator", "Uma dimensão escondida que explica por que várias variáveis andam juntas."),
        ("FCU", "Favelas e Comunidades Urbanas: a classificação do IBGE para os setores que são favela ou comunidade urbana (campo `CD_TIPO` = 1)."),
        ("Φ (fi)", "A correlação entre os fatores numa rotação oblíqua (promax). Na Varimax é zero por construção."),
        ("Git", "Programa que guarda o histórico de mudanças de uma pasta de projeto."),
        ("Grade", "O conjunto de todas as especificações testadas — no NB05, " + N.n_esp + "."),
        ("Grafo do projeto", "Um mapa do repositório em que cada conceito, arquivo ou função é um nó e cada relação é uma ligação; serve para achar onde cada coisa está."),
        ("Hash", "O identificador curto de um commit, como `2d0c909`."),
        ("Heywood (caso de)", "Comunalidade acima de 1, que é impossível: sinal de problema na estimação."),
        ("Horn (regra de)", "Mantém só os fatores cujo autovalor supera o que dados aleatórios do mesmo tamanho dariam. Também chamada de análise paralela."),
        ("IBGE", "Instituto Brasileiro de Geografia e Estatística, que faz o Censo."),
        ("Imputação", "Preencher um valor que falta, ou que foi retirado, com uma estimativa — como a mediana."),
        ("Índice composto", "Um número que junta vários indicadores, cada um com um peso."),
        ("Indicador", "Uma conta que transforma contagens em algo comparável, em geral uma proporção."),
        ("IVS", "Índice de Vulnerabilidade à Saúde."),
        ("IVS-7 e IVS-6", "O IVS com os sete indicadores do IVS-BH 2012, e o mesmo sem o lixo."),
        ("IVS-BH 2012", "O índice da Secretaria Municipal de Saúde de Belo Horizonte, feito com o Censo de 2010: a referência de método do projeto."),
        ("Kaiser (regra de)", "Mantém os fatores com autovalor maior que 1."),
        ("KMO", "Medida, de 0 a 1, de quanto os dados se prestam à análise fatorial. De 0,7 para cima é bom."),
        ("Mediana", "O valor do meio de uma lista ordenada: metade fica abaixo, metade acima. Ao contrário da média, não é puxada por um extremo."),
        ("Min-max", "Normalização que põe o pior valor em 1 e o melhor em 0."),
        ("Módulo", "Código compartilhado por vários programas. O do projeto é `src/ivs_censo`."),
        ("MSA", "O KMO de cada variável, separado."),
        ("NB01 a NB05", "Os notebooks da pipeline: extração e filtro (01), análise descritiva (02), análise fatorial (04), fatorial ampliada (04b) e IVS final (05)."),
        ("Normalização", "Pôr indicadores de escalas diferentes na mesma régua. No município: mínimo e máximo de cada cidade; global: de todos os setores juntos."),
        ("Notebook", "Documento que mistura texto, código e resultados, na ordem da análise."),
        ("Numerador", "A parte de cima de uma proporção: o que se quer medir."),
        ("Outlier (valor extremo)", "Um valor muito distante dos demais, como o setor de Belo Horizonte com renda média de " + N.renda_extremo + "."),
        ("p.p. (pontos percentuais)", "A diferença entre duas porcentagens: de 65% para 63% são 2 p.p."),
        ("Parcimônia", "Preferir o modelo mais simples, com menos variáveis, quando os outros não são claramente melhores."),
        ("Partição", "Divisão de um total em partes que não se sobrepõem e somam o total. A falta de banheiro (`V00495`) se divide exatamente em `V00236`, `V00237` e `V00238`."),
        ("Peso", "Quanto cada indicador ou dimensão conta na soma do índice."),
        ("Posto", "A posição de um valor numa lista ordenada (primeiro, segundo…). Postos no município: a posição do setor dentro da sua cidade."),
        ("Posto médio", "A média das posições de uma especificação nos três critérios de escolha; o menor é o melhor."),
        ("Promax", "Rotação oblíqua: deixa os fatores se correlacionarem. Tem duas matrizes, a padrão e a estrutura."),
        ("Proporção", "Numerador dividido pelo denominador, de 0 a 1."),
        ("Recorte urbano", "Só os setores urbanos (`SITUACAO` = urbana): 104.108 nos 70 municípios."),
        ("Referência proposta", "A especificação elegível de melhor posição média nos três critérios. É uma proposta: a escolha final é da orientadora."),
        ("Regressão logística", "Modelo que estima a chance de algo acontecer (aqui: o setor ser favela) a partir de outras variáveis."),
        ("Renda invertida", "A renda virada do avesso, para que, como nos outros indicadores, mais seja pior."),
        ("Repositório", "A pasta do projeto, com todo o seu histórico no git."),
        ("ROC (curva)", "Gráfico que mostra o quanto um índice separa dois grupos; a área sob ela é a AUC."),
        ("Rotação", "Girar os eixos dos fatores para que cada variável fique perto de um só."),
        ("Script", "Programa que roda sozinho e grava um resultado."),
        ("Scree plot", "Gráfico dos autovalores em ordem decrescente, usado para decidir quantos fatores manter."),
        ("Sensibilidade por município", "Refazer a análise tirando um município por vez, para ver quanto o resultado depende de cada um."),
        ("Setor censitário", "A menor área com dados publicados pelo Censo, em geral poucos quarteirões na cidade."),
        ("Sigilo", "O \"X\" que o IBGE põe no lugar de contagens pequenas. No projeto vira dado ausente, nunca zero."),
        ("Spearman (correlação de)", "Correlação feita com as posições (postos) em vez dos valores, menos sensível a extremos."),
        ("SS", "Soma dos quadrados das cargas de um fator: a sua força, usada para calcular os pesos."),
        ("Taxa e razão", "Na taxa, o denominador contém o numerador (analfabetos ÷ todos de 15+), e ela nunca passa de 1. Na razão, não contém (analfabetos ÷ alfabetizados), e ela pode passar de 1."),
        ("Teste automático", "Programa que confere se o código dá o resultado esperado. O projeto tem " + N.testes + "."),
        ("V00001", "Domicílios particulares permanentes ocupados: o denominador dos indicadores de domicílio."),
        ("Varimax", "Rotação ortogonal: mantém os fatores independentes, com correlação zero entre eles."),
        ("Worktree", "Uma cópia de trabalho paralela do repositório. As que ficaram esquecidas foram para a Lixeira em setembro."),
        ("z (estatística)", "Mede se um efeito é maior do que o acaso explicaria; acima de 2 já é considerado significativo."),
    ]
    return sorted(termos, key=lambda t: t[0].lower().replace("φ", "f").replace("(", ""))


def fecho(N):
    return [
        ("secao", "Como este guia foi feito"),
        ("p", f"""Este guia foi gerado em {N.hoje} pelo programa `scripts/gerar_pdf_guia_decks_outubro.py`. Os
textos estão em `scripts/guia_outubro_base.py`, `scripts/guia_outubro_cronologia.py` e
`scripts/guia_outubro_demandas.py`. Os números vêm dos mesmos arquivos que alimentam os slides:

• o histórico do git, para as datas e as contagens de commits;
• `banco_de_dados/eda/fatorial_ampliada/`, para a linha de base do NB04, os cenários S0–S7, os pesos, a
validação, a sensibilidade e a partição do banheiro;
• `banco_de_dados/eda/ivs_especificacoes/`, para a grade do NB05, a referência proposta, o índice contra
a renda e as faixas;
• `banco_de_dados/entrega_orientadora/`, para o quadro de indicadores, a renda do setor extremo e o número
de colunas da entrega;
• o próprio arquivo de cada deck, para as miniaturas e o número de slides.

Antes de montar o guia, o programa confere se o título de cada verbete aparece no slide de mesmo número.
Se um deck for regerado e os slides mudarem de lugar, ele para e diz qual verbete não confere — em vez de
explicar o slide errado. Para gerar de novo:"""),
        ("p", "`uv run --with reportlab --with pandas --with pypdf python scripts/gerar_pdf_guia_decks_outubro.py`"),
    ]
