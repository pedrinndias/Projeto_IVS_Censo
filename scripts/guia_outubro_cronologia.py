"""Texto do guia: a cronologia do projeto, slide a slide (Parte B).

Não gera nada sozinho: é lido por scripts/gerar_pdf_guia_decks_outubro.py. Um verbete por slide,
na ordem do deck; `titulo` tem de aparecer no slide de mesmo número (o gerador confere). Números
de CSV e do git chegam em N; os que só existem em documento estão escritos como no documento.
"""


def abertura(N):
    return f"""A cronologia conta o projeto como um filme: do primeiro commit, em {N.primeiro}, até hoje. Ela
abre com oito slides de contexto (o projeto, os dados, a linha do tempo, o ritmo do trabalho, as
apresentações antigas), segue com sete capítulos em ordem de data, e fecha com três leituras
transversais — as decisões de método, os achados e a organização — e com o estado atual do projeto.

Os capítulos são feitos de páginas de <b>diário</b>: cada linha tem uma data em vermelho, à esquerda, o
fato em negrito e um detalhe em cinza. Quando um capítulo tem mais fatos do que cabem num slide, ele
continua no seguinte, com "(continuação)" no título."""


def verbetes(N):
    return [
        dict(n=1, titulo="Cronologia do projeto",
             frase="A capa: diz o que é o deck — o processo inteiro do projeto, em ordem — e quanto histórico há por trás dele.",
             mostra=f"""No alto, em letras pequenas e espaçadas, a identificação: Projeto IVS, Censo 2022, Fiocruz
Minas — Instituto René Rachou. Abaixo, o título grande, "Cronologia do projeto", e um subtítulo que
resume o conteúdo: o que mudou, quando, por quê, o que se descobriu e como o repositório foi organizado,
de março a outubro de 2026. No pé da página, o autor e o tamanho do histórico: {N.commits} commits, de
{N.primeiro} a {N.ultimo}.""",
             zero="""Um <b>commit</b> é um registro de mudança no projeto, com data e descrição (Parte A, seção
A.10). A capa dá o número de commits porque ele mede o quanto de trabalho registrado sustenta a
cronologia: cada data dos slides seguintes vem de um desses registros, ou de um documento do projeto
quando o trabalho foi feito antes de ser registrado.""",
             apresentar="""“Esta apresentação conta o projeto em ordem de data: o que foi feito, por que foi feito e o que
mudou no caminho. Ela não é uma apresentação de resultados — é o mapa de como chegamos até aqui. Cada
data vem do histórico do projeto, então dá para conferir qualquer uma delas.”""",
             perguntas=[("Por que o histórico começa em março?", "Porque é quando o repositório foi criado. O período da bolsa também começa em março de 2026, com o Programa de Inserção do IRR.")]),

        dict(n=2, titulo="Como ler este deck",
             frase="As regras do jogo: de onde vem cada data, de onde vem cada número e como o deck está organizado.",
             mostra="""Quatro blocos de texto, em duas colunas. <b>As datas</b>: são as do commit, salvo quando um documento
registra outra. <b>Os números</b>: saem dos CSVs gravados pelos scripts, lidos na hora em que o deck é
gerado. <b>As anotações</b>: cada página de diário tem, nas anotações do apresentador, a fonte de cada
item e os commits do dia. <b>A ordem</b>: sete capítulos por data, três leituras transversais e o estado
atual. O último bloco tem um filete vermelho em cima, para marcar que é o mapa do resto.""",
             zero="""Há duas datas possíveis para um fato: a do dia em que o trabalho foi feito e a do dia em que ele foi
registrado no git. Quase sempre são a mesma. A exceção mais importante são as demandas de julho: o
GUIA do projeto registra que foram implementadas em 09/08, mas só entraram no git em 20 e 21/08. Nesses
casos o slide usa a data do documento e diz qual é o documento.

"Os números saem dos CSVs" quer dizer que nenhum valor foi digitado no slide: um programa lê as tabelas
produzidas pelas análises e escreve os números. Um <b>CSV</b> é uma tabela salva como texto. Se a tabela
mudar, basta gerar o deck de novo.

As <b>anotações do apresentador</b> são o texto escondido embaixo de cada slide; no PowerPoint, aparecem
em Exibir › Anotações.""",
             apresentar="""“Antes de começar, duas regras. As datas são as do histórico do projeto; quando um trabalho foi feito
antes de ser registrado, eu uso a data do documento e digo qual é. E nenhum número foi digitado: todos
saem das tabelas das análises. Se precisarem conferir qualquer item, as anotações deste deck trazem a
fonte e o registro de cada um.”""",
             perguntas=[("O que é um “capítulo” e o que é uma “leitura transversal”?", "Os capítulos contam o tempo: março a maio, junho, julho e agosto, e assim por diante. As leituras transversais cortam o tempo por tema: todas as decisões de método juntas, todos os achados juntos, toda a organização junta.")]),

        dict(n=3, titulo="O projeto em uma página",
             frase="Quem, onde, quando, o quê e para quê: a identidade do projeto, o objetivo, a pergunta, a hipótese e o desenho do estudo.",
             mostra="""À esquerda, uma tabela de oito linhas: título, tipo (Iniciação Científica), instituição (Fiocruz
Minas — Instituto René Rachou), período (março de 2026 a fevereiro de 2027), unidade (setor censitário),
recorte (setores urbanos dos 70 municípios do ELSI-Brasil), referência (IVS-BH 2012) e produto (relatório
final e artigo). À direita, quatro blocos: objetivo, pergunta, hipótese e desenho — este último com o
filete vermelho.""",
             zero="""• <b>IVS intraurbano</b>: um índice que compara pedaços de uma mesma cidade (Parte A, A.1).
• <b>Setor censitário</b>: a menor área com dados do Censo, em geral poucos quarteirões (A.2).
• <b>ELSI-Brasil</b>: o estudo de saúde dos idosos cujos 70 municípios definem o recorte (A.3).
• <b>IVS-BH 2012</b>: o índice de Belo Horizonte, feito com o Censo de 2010, que serve de modelo de método.
• <b>Hipótese</b>: a resposta que se espera encontrar. Aqui, que setores da periferia tenham IVS mais alto
que os do centro — o "padrão centro-periferia" descrito em estudos de cidades brasileiras. A <b>hipótese
nula</b> é a ausência de padrão: se os dados não mostrarem diferença, fica-se com ela.
• <b>Estudo ecológico</b>: um estudo em que a unidade é um grupo (aqui, o setor), e não a pessoa. Ele
permite dizer que um <i>setor</i> é vulnerável, mas não que cada pessoa dele é. Tirar conclusões
individuais de dados de grupo é um erro conhecido, a <i>falácia ecológica</i>.
• <b>Quatro faixas de risco</b>: baixo, médio, elevado e muito elevado (A.5).""",
             apresentar="""“O projeto constrói um índice de vulnerabilidade à saúde para cada setor censitário urbano dos 70
municípios do ELSI-Brasil, com o Censo de 2022, seguindo o método do IVS de Belo Horizonte de 2012. A
pergunta é como essa vulnerabilidade se distribui dentro das cidades; a expectativa é encontrar o padrão
centro-periferia. É um estudo ecológico: falamos de lugares, não de pessoas.”""",
             perguntas=[("Por que só setores urbanos?", "Porque o índice é intraurbano — compara pedaços de cidade — e porque as variáveis de saneamento têm outro significado no campo (lá, poço e fossa podem ser a solução adequada)."),
                        ("O índice vai dizer quem está doente?", "Não. Ele mede as condições do lugar que expõem as pessoas a adoecer. Para falar de pessoas, é preciso cruzar com dados individuais, como os do ELSI-Brasil.")]),

        dict(n=4, titulo="Os dados: oito arquivos do Censo 2022",
             frase="De onde vêm os dados: oito arquivos do IBGE, um por tema, todos com contagens por setor censitário.",
             mostra="""Uma tabela de oito linhas, uma por arquivo. A primeira coluna tem o nome do arquivo (abreviado com
"…" no começo, porque os nomes completos são longos), a segunda o tema e a terceira as variáveis mais
importantes daquele arquivo. A última linha, a do arquivo de parentesco, traz a observação "o denominador
abandonado em maio".""",
             zero="""O IBGE publica os dados do Censo por setor em arquivos separados por tema, como capítulos de um livro:

• <b>básico</b>: o código do setor (`CD_SETOR`), o nome do município (`NM_MUN`) e a população;
• <b>características do domicílio 1</b>: os totais de domicílios e de moradores (`V00001`, `V00002`,
`V00005`, `V00006`) — os denominadores;
• <b>características do domicílio 2</b>: água, esgoto, lixo e banheiro — o saneamento;
• <b>alfabetização</b>: quem sabe (`V00900`) e quem não sabe (`V00901`) ler e escrever, entre as pessoas de
15 anos ou mais;
• <b>cor ou raça</b>: as contagens de pessoas por cor ou raça (`V01318`, `V01320`, `V01321`) — no índice,
pretos, pardos e indígenas;
• <b>renda do responsável</b>: `V06004`, o rendimento médio mensal da pessoa responsável pelo domicílio;
• <b>demografia</b>: as idades, usadas nos indicadores de envelhecimento;
• <b>parentesco</b>: a relação de cada morador com o responsável. Dele vinha `V01042`, o número de
responsáveis, que foi o primeiro denominador do projeto e foi trocado em maio (slide 11).

Todos os arquivos usam o mesmo código de setor, e é por ele que são juntados numa tabela só.""",
             apresentar="""“Tudo vem de oito arquivos do Censo de 2022, publicados pelo IBGE por setor censitário. Eles são
juntados pelo código do setor. A linha de baixo lembra uma mudança importante de maio: o denominador
deixou de vir do arquivo de parentesco.”""",
             perguntas=[("Os dados são das pessoas ou dos setores?", "Dos setores. O IBGE não publica respostas individuais: publica contagens por setor, e o índice é calculado para cada setor.")]),

        dict(n=5, titulo="Quantos setores ficam a cada etapa",
             frase=f"Da base inteira dos 70 municípios ao IVS final, quantos setores sobram a cada filtro — de {N.setores_base} a {N.ref_n}.",
             mostra=f"""Quatro barras horizontais, uma por etapa, com o número de setores e a porcentagem em relação à
base. Debaixo de cada rótulo, em cinza, o arquivo de onde o número saiu. As três primeiras barras são
pretas; a última, a do IVS final, é vermelha. No pé, uma frase lembra que o Brasil inteiro tem 468.099
setores e que a perda até o IVS final é dado ausente.

As etapas: a base com todos os setores dos 70 municípios ({N.setores_base}, 100%); o recorte urbano
(104.108); o IVS-7 com as sete variáveis presentes ({N.s0_n}); e a especificação de referência do IVS final
({N.ref_n}).""",
             zero="""Cada etapa é um filtro, como peneiras cada vez mais finas:

• <b>base ELSI</b>: todos os setores dos 70 municípios, urbanos e rurais;
• <b>recorte urbano</b>: só os setores que o IBGE classifica como urbanos (A.3);
• <b>IVS-7</b>: só os setores em que os sete indicadores do índice existem ao mesmo tempo. Basta um deles
estar sob sigilo para o setor sair;
• <b>IVS final</b>: só os setores com todas as variáveis da especificação de referência do NB05 — que inclui
as partes do banheiro graduado, com mais sigilo.

A perda não é um defeito do método: é a consequência de tratar o sigilo como dado ausente, e não como zero
(A.2).""",
             numeros=f"""A porcentagem ao lado de cada número é em relação à base: o IVS-7 fica com cerca de quatro em cada
cinco setores; a referência do IVS final, com cerca de dois em cada três ({N.ref_n} setores). Os 468.099
setores do país aparecem só em texto, porque são a base de comparação "Brasil × ELSI" e não passam pelos
filtros.""",
             apresentar=f"""“A base tem {N.setores_base} setores. Ficam os urbanos, depois só os que têm todos os indicadores, e a
especificação de referência do IVS final cobre {N.ref_n}. O que se perde no caminho é dado sob sigilo do
IBGE, que nós tratamos como ausente — nunca como zero.”""",
             perguntas=[("Perder um terço dos setores não enviesa o índice?", "Pode enviesar, e por isso o número está à vista. O sigilo cai mais onde as contagens são pequenas. Os decks comparam as versões numa amostra comum de setores justamente para que a comparação não dependa de quem perdeu mais.")]),

        dict(n=6, titulo="A linha do tempo em uma página",
             frase="O projeto inteiro numa folha: uma coluna por mês, com os marcos principais e o número de commits de cada período.",
             mostra=f"""Oito colunas, da esquerda para a direita: março e abril, maio, junho, julho, agosto, setembro (dias
1 a 17), setembro (dias 18 a 30) e outubro. No alto de cada coluna, o nome do período e, embaixo, o número
de commits: {N.c_marabr}, {N.c_mai}, {N.c_jun}, {N.c_jul}, {N.c_ago}, {N.c_set1}, {N.c_set2} e {N.c_out}.
Debaixo de uma régua preta vêm os marcos, cada um com o dia em vermelho. Setembro foi partido em dois
porque concentra quase metade do histórico.""",
             zero="""É o resumo visual dos sete capítulos que vêm depois. Alguns marcos para guardar:

• <b>maio</b>: o projeto se reorganiza (Fase 2), ganha o documento mestre (o GUIA) e começa a Fase 3, a
atual, com o filtro dos 70 municípios. No dia 22, troca o denominador;
• <b>junho</b>: a análise descritiva cresce, com indicadores novos e a decisão sobre a caçamba de lixo;
• <b>julho e agosto</b>: as sete demandas de julho, o módulo de fórmulas compartilhado e a primeira
análise fatorial;
• <b>setembro</b>: a auditoria de agosto, a renda sem o valor extremo, a análise fatorial completa (NB04),
a revisão geral e as demandas de setembro, e o IVS final (NB05);
• <b>outubro</b>: o grafo do projeto e estas apresentações.

Abril não tem commit: é o mês do Programa de Inserção do IRR e do curso introdutório, atividades do
cronograma do bolsista que não passam pelo repositório.""",
             apresentar="""“Esta é a linha do tempo em uma página. Maio é a reorganização; junho, a análise descritiva; julho e
agosto, as primeiras demandas da orientadora e o código compartilhado; setembro, a análise fatorial e o
IVS final. Os números embaixo de cada mês mostram onde o trabalho se concentrou.”""",
             perguntas=[("Por que julho tem só um commit?", "Porque as demandas de julho foram trabalhadas em julho e começo de agosto e registradas no git só em 20 e 21/08. O commit de julho é o do primeiro grafo do projeto.")]),

        dict(n=7, titulo="O ritmo do trabalho",
             frase=f"Dois gráficos de barras: quantos commits por mês e de que tipo — e os cinco dias mais intensos.",
             mostra=f"""À esquerda, um gráfico de colunas com os commits de cada mês, de março a outubro, com o número em
cima de cada coluna. À direita, um gráfico de barras deitadas com os commits por tipo de mudança, do mais
frequente para o menos frequente: documentação ({N.t_docs}), funcionalidade nova ({N.t_feat}), correção
({N.t_fix}), manutenção ({N.t_chore}), sem prefixo ({N.t_sem}), dados regerados ({N.t_data}) e os demais.
Embaixo, uma linha com os cinco dias de mais commits: {N.top5}.""",
             zero="""O <b>tipo</b> de cada commit vem do prefixo da mensagem (A.10): `docs` é documentação, `feat` é coisa
nova, `fix` é correção, `chore` é manutenção, `data` é dado regerado, `test` é teste, `refactor` é
reorganização. Os primeiros commits, de março, ainda não usavam prefixo — por isso a barra "sem prefixo".

Ler um gráfico de colunas é simples: a altura da coluna é a quantidade. A coluna de setembro é de longe a
mais alta. O gráfico da direita mostra que a maior parte do trabalho registrado é documentação: relatórios,
guias, registros de decisão. Isso é coerente com um projeto em que cada decisão de método precisa ficar
escrita e justificada.""",
             numeros=f"""O dia mais intenso, 25/09, tem {N.c_25set} commits: é o dia em que a revisão geral do repositório e as
demandas de setembro foram executadas, em seis fases (capítulo 5). Os outros picos — 18/06, 17/09, 15/05
e 02/09 — são os dias de entrega de cada etapa: a análise descritiva ampliada, a análise fatorial, o
começo da Fase 3 e a auditoria de agosto.""",
             apresentar="""“O ritmo não foi uniforme: o trabalho vem em ondas, e cada pico é uma entrega. Setembro concentra
quase metade dos registros. E a maior parte dos registros é documentação, porque cada decisão de método
fica escrita, com a justificativa, antes de virar número.”""",
             perguntas=[("Muito commit num dia não é sinal de pressa?", "Não necessariamente: cada commit é uma mudança pequena e com um tema só, para que dê para voltar atrás em cada uma separadamente. Muitos commits num dia é sinal de trabalho bem fatiado.")]),

        dict(n=8, titulo="As apresentações que ficaram pelo caminho",
             frase=f"As {N.n_historico} apresentações antigas, guardadas como estavam no dia em que foram mostradas — e qual é a atual.",
             mostra=f"""Uma tabela com três colunas: a data, o nome da apresentação e o número de slides. São os decks da
pasta `historico/`, de 15/05 a 21/08. Embaixo, um parágrafo diz qual é a apresentação atual: o deck da
análise fatorial, na raiz da pasta, com {N.slides_atual} slides — com a EDA Central, a fatorial ampliada e
o IVS final anexados — e que os dois decks novos ficam em `complementos/`.""",
             zero="""Cada deck antigo é uma fotografia do projeto num momento. O de 15/05 ainda usa o denominador antigo
(`V01042`); o de 22/05 apresenta a troca; os de 28 e 30/05 mostram as correções e comparam a análise antiga
com a nova; os de junho trazem a análise descritiva refeita; os de 09/08 são a retomada e o andamento das
demandas de julho; o de 21/08 é a primeira rodada da EDA Central.

Eles não são apagados nem regerados porque são o registro do que foi efetivamente apresentado. A regra da
pasta é ter <b>um arquivo só na raiz</b> — a apresentação atual —, para que ninguém abra uma versão velha
por engano. Os de apoio vão para `complementos/`; os que saíram de circulação, para `historico/`.""",
             apresentar="""“Estas são as apresentações que já foram feitas, guardadas como estavam. Não uso nenhuma delas como
fonte de número: os números de hoje são os do deck atual e destes dois novos.”""",
             perguntas=[("Por que não atualizar os decks antigos?", "Porque eles registram o que foi mostrado em cada data. Atualizá-los apagaria a história — e um número antigo num deck antigo não engana ninguém, desde que fique claro que é histórico.")]),

        dict(n=9, titulo="Março a maio — a base",
             frase="A divisória do capítulo 1: os três primeiros meses, do repositório vazio à primeira análise com o filtro dos 70 municípios.",
             mostra="""Um slide de divisória: o número 1, grande e em vermelho, o título "Março a maio — a base" e, embaixo
de uma régua, o subtítulo: do repositório vazio à primeira EDA com o filtro ELSI e à troca do denominador.""",
             zero="""As divisórias marcam o começo de cada capítulo e não têm dados. Este capítulo cobre o período em que o
projeto ganhou forma: as primeiras versões da análise (as Fases 1 e 2, hoje no `Backup/`), o documento
mestre, a Fase 3 — a que vale hoje — e a primeira grande correção de método, a do denominador.""",
             apresentar="""“O primeiro capítulo vai de março a maio: é quando o projeto ganha a forma atual.”"""),

        dict(n=10, titulo="Março a maio",
             frase="As primeiras versões da análise, o programa de inserção na Fiocruz e a reorganização de maio, com o documento mestre.",
             mostra="""Uma página de diário com seis entradas: 12/03 (repositório criado com a primeira versão da pipeline),
16/03 (auditoria em SQLite), 25/03 (variáveis multidimensionais), "mar–abr" (Programa de Inserção do IRR e
Curso Introdutório), 06/05 (Fase 2) e 14/05 (o GUIA do projeto vira o documento mestre).""",
             zero="""• <b>12/03 — o começo</b>. O repositório nasce com três notebooks: um de <i>auditoria de integridade</i>
(conferir se os dados chegaram completos e coerentes — se as somas batem, se não há setor duplicado), um de
cálculo do índice e um de formatação final. Essa é a <b>Fase 1</b>. Uma <b>pipeline</b> é a sequência de
etapas que leva o dado bruto ao resultado.
• <b>16/03 — SQLite</b>. SQLite é um banco de dados guardado num arquivo só. A auditoria conferia, entre
outras coisas, se a tabela tinha o número esperado de colunas; o número esperado estava errado e foi
corrigido.
• <b>25/03 — variáveis multidimensionais</b>. O começo do trabalho com as variáveis de várias dimensões
(saneamento, renda, educação…).
• <b>março e abril — inserção no IRR</b>. O programa de entrada do bolsista no instituto e o curso
introdutório. Não passa pelo repositório, mas é parte do cronograma.
• <b>06/05 — Fase 2</b>. O projeto organiza o fluxo da análise em extração, processamento e metodologia,
reescreve o README (o texto de apresentação do repositório) e documenta inconsistências internas: variáveis
de esgoto e denominadores que não batiam entre si.
• <b>14/05 — o GUIA</b>. Nasce o `GUIA_DO_PROJETO.md`, o documento mestre onde cada decisão de método passa
a ser registrada com a justificativa, a verificação e o status. Boa parte das datas e decisões citadas
nestes decks vêm dele.""",
             apresentar="""“O repositório começa em março com uma primeira versão da análise. Em maio, o projeto se reorganiza e
ganha um documento mestre, o GUIA, onde toda decisão de método passa a ser registrada com justificativa.
É esse registro que permite reconstruir tudo o que vem depois.”""",
             perguntas=[("O que aconteceu com as Fases 1 e 2?", "Foram substituídas pela Fase 3, a partir de 15/05, e guardadas na pasta Backup/ como histórico. A principal diferença é que a Fase 3 aplica o recorte dos 70 municípios desde o início.")]),

        dict(n=11, titulo="Março a maio (continuação)",
             frase="Maio decisivo: a Fase 3 começa, a primeira análise descritiva sai, o denominador é corrigido e as bases vão para a orientadora.",
             mostra="""A continuação do diário, com seis entradas: 15/05 (a Fase 3 e a primeira EDA), 19/05 (correções de
integridade depois da auditoria), 22/05 (a troca do denominador e a correção do analfabetismo), 25/05
(as bases entregues à orientadora), 28/05 (o deck das correções) e 30/05 (o comparativo entre a análise
antiga e a nova).""",
             zero="""• <b>15/05 — a Fase 3</b>. É o dia mais intenso de maio. O Notebook 01 (NB01) extrai os dados e filtra os
setores dos 70 municípios do ELSI-Brasil; o Notebook 02 (NB02) faz a primeira <b>EDA</b> — a análise
exploratória: médias, distribuições, correlações, comparações entre regiões —, seguindo o guia de análises
da Fiocruz e a metodologia oficial. Dois cuidados técnicos aparecem: a renda vinha com vírgula decimal (o
padrão brasileiro), que o computador lia errado se não fosse avisado; e o sigilo foi preservado nas
proporções (A.2). Saem um relatório técnico e o primeiro deck — ainda com o denominador antigo. As versões
anteriores vão para o `Backup/`.
• <b>19/05 — integridade</b>. Uma auditoria aponta problemas e eles são corrigidos; o relatório de
integridade registra o quê.
• <b>22/05 — o denominador</b>. A decisão mais importante do capítulo. O denominador dos indicadores de
domicílio passa de `V01042` (número de <i>responsáveis</i>, do arquivo de parentesco) para `V00001`
(número de <i>domicílios</i> particulares permanentes ocupados). O motivo: `V00001` é o equivalente, no
Censo de 2022, do `V002` que o IVS-BH 2012 usou em 2010 — e só com a mesma unidade os dois índices são
comparáveis. No mesmo dia, o analfabetismo deixa de ser uma <i>razão</i> (analfabetos ÷ alfabetizados, que
passava de 1 em alguns setores) e vira <i>taxa</i> (analfabetos ÷ todas as pessoas de 15 anos ou mais) —
veja A.4.
• <b>25/05 — a entrega</b>. As bases dos 70 municípios e de Belo Horizonte vão para a orientadora, na
pasta `entrega_orientadora/`.
• <b>28 e 30/05 — as correções apresentadas</b>. Um deck com as correções e dois que comparam a análise
antiga com a nova e mostram a análise completa corrigida.""",
             apresentar="""“Em 15 de maio começa a Fase 3, a atual: o filtro dos 70 municípios e a primeira análise descritiva.
Uma semana depois vem a correção mais importante do começo do projeto: o denominador passa a ser o número
de domicílios, como no IVS de Belo Horizonte, e o analfabetismo passa a ser uma taxa de verdade. No fim
do mês, as bases vão para a orientadora.”""",
             perguntas=[("Qual era o problema com V01042?", "Ele conta responsáveis (pessoas), e não domicílios. O IVS-BH 2012 dividia por domicílios; para que os dois índices sejam comparáveis, o denominador tem de ser a mesma coisa."),
                        ("Como a taxa de analfabetismo podia passar de 1?", "Porque a fórmula antiga dividia analfabetos por alfabetizados. Num setor com mais analfabetos do que alfabetizados, essa razão passa de 1. A taxa divide pelo total de pessoas de 15 anos ou mais, e nunca passa de 1.")]),

        dict(n=12, titulo="Junho — a EDA cresce",
             frase="A divisória do capítulo 2: junho, quando a análise descritiva é refeita com o denominador novo e ganha indicadores.",
             mostra="""O número 2 em vermelho, o título "Junho — a EDA cresce" e o subtítulo: o denominador novo em tudo, os
indicadores descritivos e a caçamba que saiu e voltou.""",
             zero="""Junho é o mês de consolidar a análise descritiva (a EDA). Três assuntos: propagar o denominador novo
para todos os resultados, criar indicadores que descrevem o território sem entrar no índice, e decidir o
que fazer com a caçamba de lixo.""",
             apresentar="""“O segundo capítulo é junho: a análise descritiva cresce e uma decisão de método é tomada duas vezes
no mesmo dia.”"""),

        dict(n=13, titulo="Junho",
             frase="Tudo é refeito com o denominador novo, o dicionário oficial do IBGE entra no projeto e a caçamba de lixo gera uma decisão de fidelidade ao método.",
             mostra="""Três entradas: 12/06 (tudo sincronizado com o denominador `V00001`), 18/06 (o dicionário oficial do
IBGE) e 18/06 (a caçamba sai do lixo inadequado e volta no mesmo dia).""",
             zero="""• <b>12/06 — sincronizar</b>. Depois da troca do denominador, todos os produtos precisam ser refeitos: o
relatório da EDA (em Markdown e em Word), o relatório de integridade, o deck. Duas correções técnicas
entram junto: uma <i>divisão segura</i> (quando o denominador é zero, o resultado fica ausente, sem aviso de
erro), e o alinhamento dos números de <i>assimetria</i> e <i>curtose</i> — medidas de formato de uma
distribuição: a assimetria diz se os valores se acumulam de um lado; a curtose, se há muitos valores
extremos — e de duas correlações, para que o texto, a tabela e o gráfico mostrassem o mesmo número.
• <b>18/06 — o dicionário</b>. O dicionário é a lista que diz o que cada código de variável significa. O
oficial do IBGE passa a ser a fonte das descrições.
• <b>18/06 — a caçamba</b>. Caçamba é o contêiner comunitário onde os moradores deixam o lixo (`V00398`).
Ela é destino adequado ou inadequado? No mesmo dia, a caçamba foi tirada do numerador do lixo inadequado e
depois devolvida. Ficou como <b>inadequada</b>, por fidelidade ao método do IVS-BH 2012 (o documento
"Cálculo IVS2012"), em que só a coleta porta a porta (`V00397`) é adequada. Mas a ressalva ficou escrita:
a EDA mostrou que o lixo é a variável que menos se correlaciona com as outras.""",
             apresentar="""“Em junho, tudo foi refeito com o denominador novo. E houve uma decisão típica do projeto: a caçamba
de lixo foi mantida como destino inadequado porque é assim no método de Belo Horizonte — mesmo com
indícios de que isso torna o lixo uma variável à parte. A decisão é de fidelidade; o indício ficou
registrado e voltou em setembro.”""",
             perguntas=[("Por que manter a caçamba se os dados sugeriam outra coisa?", "Porque o primeiro princípio do projeto é a fidelidade à metodologia de origem, o IVS-BH 2012. Mudar o método por conta própria quebraria a comparação. O indício foi registrado, e o lixo voltou a ser testado em setembro (demanda 10)."),
                        ("O que é o “numerador do lixo inadequado”?", "A contagem de domicílios cujo lixo não tem destino adequado. Dividida pelo total de domicílios, dá a proporção de lixo inadequado do setor.")]),

        dict(n=14, titulo="Junho (continuação)",
             frase="Indicadores que descrevem o território sem entrar no índice, tabelas de cobertura, e a pipeline comentada linha a linha.",
             mostra="""Quatro entradas: 18/06 (indicadores descritivos novos), 18/06 (cobertura, urbano/rural e morfologia),
18/06 (o deck extenso da EDA com as seis demandas adicionais) e 19/06 (a pipeline comentada linha a linha;
as versões fixadas).""",
             zero="""• <b>Indicadores descritivos</b>. Habitação precária (domicílios improvisados e degradados), falta de
banheiro, domicílios chefiados por mulher (`V01063`), estrutura etária (crianças até 4 anos, idosos de 60
anos ou mais). Eles caracterizam o território, mas <b>não entram no índice</b>: um componente de índice
precisa ter direção clara ("mais é pior"), e nem todos têm.
• <b>Cobertura</b>. Tabelas dos setores em que o serviço chega a 100% dos domicílios (saneamento, coleta de
lixo): mostram onde a variável quase não varia.
• <b>Urbano/rural</b>. Uma tabela com a situação de cada setor, nos três níveis (setor, município, região),
que preparou o recorte urbano de agosto.
• <b>Morfologia</b>. As variáveis `V00048` a `V00058` descrevem o tipo de domicílio — casa, apartamento,
casa de vila ou condomínio, habitação precária… — e foram tabuladas por região.
• <b>O deck de 18/06</b>. Uma apresentação extensa da EDA, que respondia também a seis pedidos adicionais da
orientadora; hoje está no `historico/`.
• <b>19/06 — reprodutibilidade</b>. Os notebooks foram comentados linha a linha e limpos de resultados
antigos; as versões das bibliotecas foram fixadas (para que o mesmo código dê o mesmo resultado em outro
computador); e foi documentado de onde vem cada tabela da EDA.""",
             apresentar="""“Junho também trouxe indicadores que descrevem o território — habitação precária, chefia feminina,
idade — sem entrar no índice, porque nem todos têm uma direção clara de vulnerabilidade. E o mês fecha com
a pipeline comentada e as versões fixadas: qualquer pessoa consegue refazer a análise.”""",
             perguntas=[("Por que um indicador sem direção não entra no índice?", "Porque o índice soma coisas em que “mais é pior”. O apartamento é o exemplo: há prédios de alto padrão e conjuntos habitacionais populares. Mais apartamentos não quer dizer mais vulnerabilidade.")]),

        dict(n=15, titulo="Julho e agosto — retomada e módulo",
             frase="A divisória do capítulo 3: as demandas de julho e o momento em que as fórmulas saem dos notebooks para um módulo compartilhado.",
             mostra="""O número 3 em vermelho, o título "Julho e agosto — retomada e módulo" e o subtítulo: o primeiro grafo,
as sete demandas de julho e o código que sai dos notebooks.""",
             zero="""Depois de uma pausa nos registros em julho, o projeto é retomado com as sete demandas da orientadora e
com uma mudança de organização importante: as fórmulas dos indicadores passam a morar num lugar só.""",
             apresentar="""“O terceiro capítulo cobre julho e agosto: as demandas de julho e a reorganização do código.”"""),

        dict(n=16, titulo="Julho e agosto",
             frase="O primeiro grafo do projeto, as sete demandas de julho e o resultado de cada uma.",
             mostra="""Quatro entradas: 08/07 (o primeiro grafo de conhecimento do projeto), "julho" (as sete demandas da
orientadora), 09/08 (as sete demandas implementadas, com os números de cada uma) e 10/08 (atualização
parcial do grafo).""",
             zero="""• <b>08/07 — o grafo</b>. Um <b>grafo de conhecimento</b> é um mapa do projeto: cada conceito, arquivo ou
função vira um ponto (um <i>nó</i>), e cada relação entre eles vira uma ligação (uma <i>aresta</i>). Serve
para achar rapidamente onde cada coisa está. A primeira versão leu 28 arquivos.
• <b>As sete demandas de julho</b>: (1) ajustar o índice de envelhecimento; (2) fazer a tabela de variáveis
com a fonte de cada uma; (3) excluir os setores rurais; (4) agrupar as moradias convencionais; (5) criar
um indicador de apartamento; (6) contar os setores de vilas e favelas; (7) calcular as proporções para o
Brasil inteiro, para comparar.
• <b>09/08 — os resultados</b>:
• o <b>índice de envelhecimento</b> (IEP) passa a ser pessoas de 60 anos ou mais ÷ menores de 15 anos, a
definição usada na literatura (antes dividia por crianças de 0 a 4 anos, o que dava um número três vezes
maior e incomparável); no recorte, ele vale 92,7 — 92,7 idosos para cada 100 jovens;
• a tabela de variáveis tem 72 variáveis, de 8 arquivos;
• o recorte urbano deixa 104.108 setores; 2,04% saem por serem rurais;
• 99,19% das moradias do recorte são convencionais;
• o apartamento (31,5% em média) fica <b>fora</b> do índice, por não ter direção (slide 14);
• os setores de favela e comunidade urbana passam a ser identificados pelo campo oficial `CD_TIPO = 1`:
são 19.452 no recorte, 18,7% dos setores urbanos;
• a população do Brasil calculada pelo projeto confere com a oficial: 203.080.756 pessoas.
• <b>10/08</b>. O grafo é atualizado em parte: o código e quatro figuras; dezesseis documentos ficaram para
depois.""",
             numeros="""Quase todos os números deste slide vêm do GUIA do projeto (§6.4), porque as demandas de julho foram
feitas antes de entrar no git. O de que a população do Brasil "confere" é uma verificação: somar a
população de todos os setores do país dá o total oficial do Censo, sinal de que nenhum setor se perdeu na
leitura.""",
             apresentar="""“Em julho vieram sete demandas da orientadora, e em 9 de agosto as sete estavam prontas: o índice de
envelhecimento pela definição da literatura, o recorte urbano, as favelas pelo campo oficial do IBGE, as
proporções do Brasil inteiro. A população do país calculada por nós confere com a oficial.”""",
             perguntas=[("Por que 19.452 favelas é um número importante?", "Porque essas favelas são, depois, o padrão externo usado para validar o índice (Parte A, A.7). Quase um em cada cinco setores urbanos do recorte é favela ou comunidade urbana.")]),

        dict(n=17, titulo="Julho e agosto (continuação)",
             frase="As fórmulas vão para um módulo compartilhado, a água canalizada passa a ser medida pelo complemento e começa a análise fatorial.",
             mostra="""Quatro entradas: 20/08 (o módulo compartilhado `src/ivs_censo`), 21/08 (ambiente reprodutível; a água
canalizada pelo complemento de `V00199`), 21/08 (auditoria de renda, tabelas órfãs recuperadas, testes de
43 para 59) e 24/08 (o primeiro diagnóstico fatorial).""",
             zero="""• <b>20/08 — o módulo</b>. Até então, a fórmula de cada indicador estava escrita dentro do notebook. Para
calcular o Brasil inteiro, seria preciso copiá-la — e duas cópias divergem na primeira correção feita numa
só. A solução foi um <b>módulo</b>, `src/ivs_censo`, onde cada fórmula está escrita uma vez e é usada por
todos: o NB02, o cálculo do Brasil e a entrega à orientadora.
• <b>21/08 — a água</b>. O Censo divide os domicílios em três grupos: com água canalizada até dentro de
casa (`V00199`), canalizada só até o terreno (`V00200`) e sem canalização (`V00201`). Os três somam o total
— e isso foi conferido: fecham 100,00% nos 81.270 setores com os três presentes. O problema: `V00200` e
`V00201` são contagens pequenas e o IBGE as põe sob sigilo com frequência; somá-las deixaria 21,9% dos
setores sem valor. A saída foi medir pelo <b>complemento</b>: sem água canalizada = 1 − `V00199` ÷ total
(A.4).
• <b>21/08 — auditoria e testes</b>. Uma auditoria da renda; a recuperação de tabelas "órfãs" (CSVs que
existiam sem que se soubesse qual programa os tinha gerado — passaram a ter um gerador conhecido); e os
<b>testes automáticos</b> sobem de 43 para 59. Saem também a primeira rodada da EDA Central, com roteiro de
fala, e o registro das decisões de agosto.
• <b>24/08 — a análise fatorial começa</b>. O script `diagnostico_fatorial.py` mede se as bases candidatas
servem para análise fatorial (KMO, MSA, Bartlett — A.6). É a "geração 1" das saídas de fatorial.""",
             apresentar="""“Em agosto, o código ganha uma regra que vale até hoje: cada fórmula existe uma vez só, num módulo
compartilhado. A água canalizada passa a ser medida pelo complemento, para não perder um quinto dos setores
por sigilo. E no dia 24 começa a análise fatorial.”""",
             perguntas=[("Por que medir pelo complemento não muda o resultado?", "Porque as três variáveis somam exatamente o total. Medir “quem não tem” diretamente ou como “total menos quem tem” dá o mesmo número; a diferença é que o segundo jeito quase nunca esbarra no sigilo.")]),

        dict(n=18, titulo="Setembro, primeira quinzena",
             frase="A divisória do capítulo 4: a auditoria de agosto, a renda sem o valor extremo e a análise fatorial completa.",
             mostra="""O número 4 em vermelho, o título "Setembro, primeira quinzena" e o subtítulo: a auditoria de agosto, a
renda sem o extremo e a análise fatorial do NB04.""",
             zero="""Os primeiros dezessete dias de setembro preparam e entregam a análise fatorial (o NB04), que define
como os indicadores se agrupam e quanto cada grupo pesa.""",
             apresentar="""“O quarto capítulo é a primeira quinzena de setembro: a análise fatorial.”"""),

        dict(n=19, titulo="Setembro, 1 a 17",
             frase="A auditoria de agosto, o setor de renda extrema de Belo Horizonte e a preparação da análise fatorial.",
             mostra="""Cinco entradas: 02/09 (a auditoria de agosto), 02/09 (a renda sem o extremo), 02/09 (a raiz da pasta
de apresentações com um arquivo só), 13/09 (o livro da Enap e o plano do NB04) e 16/09 (o plano de execução
do NB04 registrado).""",
             zero=f"""• <b>A auditoria de agosto</b>. Uma revisão do trabalho de agosto que gerou correções: as proporções do
Brasil passam a medir numerador e denominador nos mesmos setores (antes, um setor com o numerador sob
sigilo podia entrar no denominador e baixar a proporção); a renda é conferida contra outras variáveis do
arquivo de renda (`V06001` a `V06005`), e fica documentado o viés do <i>sigilo parcial</i> — quando parte
da informação de renda de um setor está escondida; a base completa de favelas é separada do recorte usado
na análise.
• <b>A renda sem o extremo</b>. Um setor de Belo Horizonte, o `310620005650366`, tinha renda média de
{N.renda_extremo} por responsável — muito acima de todos os outros. Na normalização min-max (A.5), ele vira
o máximo e espreme todos os outros setores perto de zero. A entrega ganha a coluna `renda_media_sem_extremo`
(a renda com esse setor retirado), e a segunda rodada da EDA é feita sem ele, com um deck, o critério de
renda por extenso e o roteiro.
• <b>Um arquivo só na raiz</b>. A pasta de apresentações passa a ter só a apresentação atual na raiz; o
resto vai para `complementos/` e `historico/` (slide 8).
• <b>13 e 16/09 — o estudo</b>. Antes de programar a análise fatorial, o estudo: um guia de leitura do
manual de análise fatorial da Enap (a Escola Nacional de Administração Pública) e o plano de execução do
NB04.""",
             apresentar=f"""“No começo de setembro, a auditoria de agosto corrige as proporções do Brasil e a separação das
favelas. E aparece o setor de renda extrema de Belo Horizonte: {N.renda_extremo} de renda média. Sozinho,
ele distorce a escala da renda inteira; por isso a entrega ganha uma coluna sem ele. Depois, duas semanas
de estudo antes de programar a análise fatorial.”""",
             perguntas=[("O setor extremo é um erro do IBGE?", "Não dá para afirmar. Pode ser um setor pequeno, com poucos domicílios de renda altíssima. O ponto não é se ele é verdadeiro: é que, verdadeiro ou não, ele estraga a régua da normalização. Por isso o projeto mantém as versões da renda com e sem ele.")]),

        dict(n=20, titulo="Setembro, 1 a 17 (continuação)",
             frase="O NB04 entrega a análise fatorial completa — e um resultado incômodo: a renda sozinha separa as favelas melhor que o índice.",
             mostra=f"""Quatro entradas, todas de 17/09, o segundo dia mais intenso do histórico: o NB04 com os números
principais, o relatório e o deck com as correções da primeira revisão, a auditoria integral (22 achados) e a
reorganização da pasta `docs/`.""",
             zero=f"""• <b>O NB04</b>. O notebook da análise fatorial (A.6). Um módulo novo faz rotação oblíqua (promax),
extração pelo eixo principal e escores. Os números da entrada, um por um:
• <b>KMO {N.kmo}</b>: os dados servem bem para análise fatorial (acima de 0,7 é bom);
• <b>pesos do IVS-6 com Varimax: {N.p_soc}% socioeconômica e {N.p_san}% saneamento</b>: sem o lixo, a
análise encontra dois fatores, e o socioeconômico é quase duas vezes mais forte;
• <b>Φ da promax {N.phi}</b>: quando se deixa os fatores se correlacionarem, a correlação entre eles é
moderada — as duas dimensões não são independentes;
• <b>AUC contra FCU: índice {N.auc_ind} × renda sozinha {N.auc_renda}</b>: o índice separa bem as favelas,
mas a renda, sozinha, separa melhor (A.7).
• <b>Relatório e deck</b>. Com as correções de uma primeira revisão, a renda sem o extremo, a discussão
<i>reflexivo × formativo</i> e o código traduzido para R. Num modelo <b>reflexivo</b>, os indicadores são
consequências de uma vulnerabilidade escondida, e a análise fatorial é a ferramenta natural; num
<b>formativo</b>, os indicadores <i>compõem</i> a vulnerabilidade, e os pesos viriam da teoria. O projeto
documentou as duas leituras. <b>R</b> é outra linguagem de estatística, usada por muitos pesquisadores.
Saem também dois documentos de apoio para apresentar (um guia dos slides e um plano de estudo) e a EDA
Central é anexada ao deck.
• <b>A auditoria integral</b>. Uma revisão de ponta a ponta do projeto, com 22 achados (problemas e pontos
frágeis).
• <b>A casa arrumada</b>. A pasta `docs/` passa a ter subpastas por tipo de uso; as bases antigas vão para
o arquivo; 61 tabelas ganham registro de procedência; os 18 programas executáveis ganham um índice; o NB04 é
comentado linha a linha.""",
             numeros=f"""O mais importante é o par de AUCs: {N.auc_ind} contra {N.auc_renda}. Em palavras: sorteando um setor
de favela e um que não é, o índice acerta qual é o de favela em cerca de 81% das vezes; a renda sozinha, em
cerca de 88%. Esse resultado volta várias vezes nas demandas de setembro.""",
             apresentar=f"""“Em 17 de setembro sai a análise fatorial completa. Os dados servem bem, com KMO de {N.kmo}. Sem o lixo,
a análise divide os pesos em {N.p_soc1}% socioeconômico e {N.p_san1}% saneamento. E um resultado incômodo: a
renda sozinha separa as favelas melhor que o índice. No mesmo dia, uma auditoria integral levanta 22 pontos
para corrigir.”""",
             perguntas=[("Se a renda sozinha separa melhor, para que o índice?", "Porque separar favelas não é o objetivo do índice — é só um teste de validade. O índice mede condições que a renda não mede. As demandas de setembro (Parte C, parte 8) mostram que, entre setores de renda parecida, o índice separa melhor que a renda."),
                        ("O que é o IVS-6?", "O IVS-7 sem o lixo. Foi a base principal do NB04, porque o lixo, sozinho, formava um fator à parte.")]),

        dict(n=21, titulo="25 de setembro — a revisão e as demandas",
             frase=f"A divisória do capítulo 5: um único dia com {N.c_25set} commits — a revisão geral do repositório e as demandas de setembro.",
             mostra="""O número 5 em vermelho, o título "25 de setembro — a revisão e as demandas" e o subtítulo: um dia, 44
commits, a revisão geral e as seis fases das demandas de setembro.""",
             zero="""Este capítulo é um dia só. Nele, o repositório inteiro foi revisado e as onze demandas de setembro da
orientadora foram executadas, organizadas em seis fases (0 a 5).""",
             apresentar="""“O quinto capítulo é um dia: 25 de setembro, o mais intenso do histórico.”"""),

        dict(n=22, titulo="25 de setembro",
             frase="A revisão geral encontra 83 problemas, as demandas de setembro ganham um plano em seis fases e a Fase 0 corrige o que travava o resto.",
             mostra="""Três entradas: a revisão geral do repositório inteiro, o plano de execução das demandas de setembro em
seis fases e a Fase 0 (linha de base e destravamentos).""",
             zero="""• <b>A revisão geral</b>. Uma leitura crítica de todo o repositório: código, dados, notebooks, documentos,
apresentações. Encontrou 83 achados — 92 brutos, dos quais 9 eram o mesmo defeito visto por dois caminhos e
foram juntados. Dezessete tinham sido introduzidos <i>depois</i> da auditoria de 17/09 — trabalho novo
também traz erro novo.
• <b>O plano em seis fases</b>. Da Fase 0 (a linha de base) à Fase 5 (o resto da revisão), com um arquivo de
estado que registra o que cada fase fez.
• <b>A Fase 0</b>. O que travava o resto:
• a <b>Varimax</b> (A.6) é um processo de tentativas que gira os eixos aos poucos até parar de melhorar. Ela
parava cedo demais, antes de chegar ao resultado final. A correção a faz parar só quando a rotação deixa de
mudar (uma diferença menor que 10<super>−10</super>, um número minúsculo);
• a proporção de domicílios sem água canalizada no <b>Brasil</b> saía invertida — 0,986 em vez de 0,0138 —
porque o cálculo agregado esquecia o complemento (A.4). Ou seja: dizia que 98,6% dos domicílios do país
não tinham água canalizada, quando o certo é 1,38%;
• uma regra que impedia arquivos de dados grandes de irem para o git tinha se perdido e foi restaurada;
• a <b>linha de base</b> do NB04 foi gravada: os números contra os quais todo cenário novo seria comparado.""",
             apresentar="""“No dia 25, o repositório inteiro foi revisado: 83 achados. Antes de atacar as demandas, a Fase 0
corrigiu o que travava o resto — a Varimax, que parava antes da hora, e a proporção nacional de água
canalizada, que saía pelo avesso — e gravou a linha de base para comparar tudo depois.”""",
             perguntas=[("A Varimax errada mudou os resultados do NB04?", "Mudou pouco, mas mudou; por isso o NB04 foi regerado com a versão corrigida na Fase 3 do mesmo dia. O número que importa é o de depois da correção."),
                        ("Como um erro de 0,986 passou despercebido?", "Era um número agregado do Brasil, usado só para comparação, e não entrava no índice. Foi a revisão sistemática que o achou — é para isso que ela existe.")]),

        dict(n=23, titulo="25 de setembro (continuação)",
             frase="As fases 1 a 5: a renda com a mediana, o quadro de indicadores, a fatorial ampliada, o NB04 corrigido, os slides e o resto da revisão.",
             mostra="""Três entradas: Fases 1 e 2 (renda, quadro e fatorial ampliada), Fases 3 e 4 (o NB04 corrigido, o NB04b e
os slides) e Fase 5 (o resto da revisão, em quatro lotes).""",
             zero=f"""• <b>Fases 1 e 2</b>. A <b>demanda 1</b> pedia uma coluna de renda com a mediana. A <b>mediana</b> é o valor
do meio de uma lista ordenada; ao contrário da média, não é puxada por um valor extremo. A renda do setor
extremo foi trocada pela mediana de Belo Horizonte sem ele ({N.med_bh}) — isso é uma <b>imputação</b>:
preencher um valor com uma estimativa. A <b>demanda 2</b> pedia o quadro de indicadores: saiu com {N.n_ind}
indicadores. E a <b>fatorial ampliada</b>: uma grade de cenários (S0 a S7, explicados na Parte C) que repete
a análise fatorial com variáveis a mais ou a menos, sem bootstrap (A.8).
• <b>Fases 3 e 4</b>. O NB04 é regerado com a Varimax corrigida; um notebook novo, o NB04b, roda a fatorial
ampliada em sete blocos. A apresentação é revista: um inventário do que existe, um roteiro, um programa que
junta decks (o "juntador") e a correção de três números errados nos slides e de um no guia de apoio (16.548
no lugar de 16.563). Os códigos como AUD-07 e DEC-1 são os identificadores de cada achado nas auditorias.
• <b>Fase 5</b>. O resto da revisão, em quatro lotes: <b>A</b>, código frágil — por exemplo, um teste que
comparava um número como texto (o texto "1" não é igual ao texto "1.0", mesmo que os números sejam iguais),
trocado por comparação numérica em cinco lugares; <b>B</b>, testes automáticos novos; <b>C</b>,
documentação; <b>D</b>, organização do repositório.""",
             apresentar="""“O resto do dia foi executar as demandas. A renda ganha uma versão com a mediana, sai o quadro de
indicadores, e a análise fatorial é repetida numa grade de cenários. O NB04 é corrigido, a apresentação é
revista e os pontos que sobravam da revisão são resolvidos em quatro lotes.”""",
             perguntas=[("O que é a “fatorial ampliada”?", "A mesma análise fatorial do NB04, repetida com conjuntos diferentes de variáveis — acrescentando as que a orientadora pediu ou tirando o lixo —, para ver o que muda. Cada conjunto é um cenário.")]),

        dict(n=24, titulo="26 e 27 de setembro — os testes e o IVS final",
             frase="A divisória do capítulo 6: dois dias para testar cada escolha em aberto, extrair uma variável nova do Censo e calcular o IVS final.",
             mostra="""O número 6 em vermelho, o título "26 e 27 de setembro — os testes e o IVS final" e o subtítulo: os nove
itens da etapa seguinte, as variantes de cada escolha, o banheiro graduado e o Notebook 05.""",
             zero="""Depois das demandas, ficaram escolhas de método sem resposta: qual renda, qual rotação, como pesar,
se o lixo entra, se o banheiro entra. Em vez de escolher, o projeto testou todas as combinações — e
deixou a escolha para a orientadora.""",
             apresentar="""“O sexto capítulo são dois dias: 26 e 27 de setembro, os testes de cada escolha e o IVS final.”"""),

        dict(n=25, titulo="26 e 27 de setembro",
             frase="O plano dos nove itens, as pendências resolvidas e a extração da variável V00237 para o banheiro graduado.",
             mostra="""Três entradas de 26/09: o plano dos testes de especificação e do NB05, a Fase A (o que estava inferido
vira verificação; as pendências pequenas) e a Fase B (a `V00237` e o banheiro graduado).""",
             zero=f"""• <b>O plano</b>. Nove itens: as três versões da renda, as rotações, os pesos na rotação oblíqua, o lixo, o
banheiro graduado, o motor que testa as especificações, a verificação do que estava inferido, as pendências
pequenas e o Notebook 05.
• <b>Fase A — de inferência a verificação</b>. Três afirmações dos documentos tinham sido escritas sem uma
conta que as comprovasse. Viraram verificação: (1) a correlação entre renda e cor/raça é −0,81 quando se
usa cada par de variáveis com os dados que tiver (<i>par a par</i>), mas 0,784 quando se usa só os setores
com todas as variáveis (<i>listwise</i>) — e a análise fatorial usa a segunda; dois documentos ganharam a
nota; (2) dois números da matriz de correlação do NB02 foram recalculados por um programa independente e
bateram; (3) o gerador do dicionário de variáveis teve o caminho de saída corrigido. As pendências pequenas:
o caminho citado no slide 45 da EDA Central e a reexecução de scripts.
• <b>Fase B — o banheiro graduado</b>. O Censo divide a falta de banheiro exclusivo (`V00495`) em três
partes: só banheiro de uso comum (`V00236`), só sanitário ou buraco (`V00237`) e nem banheiro nem
sanitário (`V00238`). A `V00237` não estava na base e foi extraída. Conferido setor a setor: as três partes
somam exatamente o total em {N.part_bate} de {N.part_pres} setores com as quatro presentes — uma
<b>partição</b> perfeita. Daí sai o <b>banheiro graduado</b>, que dá peso 1, 2 e 3 a cada grau de falta (a
fórmula está na Parte C). A entrega à orientadora é regerada, com {N.n_cols} colunas.""",
             apresentar="""“No dia 26, três afirmações que estavam escritas sem conta viram verificação, e a falta de banheiro
ganha uma versão em graus: banheiro de uso comum, só sanitário, nada. Para isso, uma variável nova foi
extraída do Censo, e a soma das partes bate em todos os setores.”""",
             perguntas=[("Por que “graduado”?", "Porque não trata toda falta de banheiro igual: ter só um banheiro de uso comum é menos grave do que não ter nem sanitário. Cada grau recebe um peso diferente.")]),

        dict(n=26, titulo="26 e 27 de setembro (continuação)",
             frase=f"O motor de especificações testa {N.n_esp} combinações, o NB05 calcula o IVS final e o repositório perde 597 MB de cópias esquecidas.",
             mostra="""Três entradas de 27/09: a Fase C (o motor de especificações), a Fase D (o Notebook 05, o relatório e os
slides) e as worktrees órfãs que vão para a Lixeira.""",
             zero=f"""• <b>Fase C — o motor</b>. Um programa que monta todas as combinações das escolhas em aberto: 3 rendas × 2
opções de lixo × 3 de banheiro = {N.n_bases} bases; cada uma com {N.n_esq} esquemas de rotação e peso e 2
normalizações = {N.n_esp} especificações (A.9). {N.n_eleg} passam nos critérios de qualidade, fixados
antes de rodar. Entre elas, o motor aponta uma referência proposta — e três leituras alternativas dos
critérios.
• <b>Fase D — o NB05</b>. O Notebook 05 é escrito e executado por um programa (com as bibliotecas `nbformat`
e `nbclient`), o que garante que ele rode do começo ao fim sem intervenção. Sai o relatório do IVS final,
com todos os números lidos das tabelas, e os slides do IVS final são anexados ao deck principal, que fica
com {N.slides_atual} slides.
• <b>As worktrees órfãs</b>. Uma <b>worktree</b> é uma cópia de trabalho paralela do repositório. Cinco
delas tinham ficado esquecidas no disco, ocupando 597 MB. Depois de resgatados os dois arquivos que só
existiam nelas, foram movidas para a Lixeira — movidas, e não apagadas, para que desse para voltar atrás.""",
             apresentar=f"""“No dia 27, um programa testa todas as combinações de escolhas: {N.n_esp} especificações, das quais
{N.n_eleg} passam nos critérios de qualidade. O Notebook 05 calcula o IVS final e propõe uma referência —
uma proposta, porque as escolhas são da orientadora.”""",
             perguntas=[("Por que testar todas as combinações em vez de escolher a melhor?", "Porque cada escolha tem argumentos dos dois lados, e escolher olhando o resultado viciaria a análise. A grade mostra o que cada escolha muda; a decisão fica com quem tem a autoridade de método.")]),

        dict(n=27, titulo="De 30/09 até hoje",
             frase="A divisória do capítulo 7: os dias mais recentes — a estrutura do deck, o grafo do projeto e estas apresentações.",
             mostra="""O número 7 em vermelho, o título "De 30/09 até hoje" e o subtítulo: a estrutura do deck, o grafo do
projeto e estas duas apresentações.""",
             zero="""O último capítulo é de manutenção e de memória: consertar a estrutura do deck principal, atualizar o mapa
do projeto e produzir estas duas apresentações.""",
             apresentar="""“O último capítulo vai de 30 de setembro até hoje.”"""),

        dict(n=28, titulo="De 30/09 até hoje",
             frase="O deck principal tem a estrutura interna consertada, o grafo passa a ler os documentos e o branch principal muda de nome.",
             mostra="""Cinco entradas: 30/09 (a estrutura do deck consertada), 30/09 (o grafo do código e o que o grafo não
lê), 01/10 (o grafo lê os documentos), 01/10 (o branch principal passa a se chamar main) e a data de hoje
(estas duas apresentações).""",
             zero=f"""• <b>A estrutura do deck</b>. Um arquivo `.pptx` é, por dentro, um pacote de arquivos de texto (XML). Um
deles, o <i>master</i>, é o molde de todos os slides; os <i>layouts</i> são variações dele. Ao juntar decks,
o master tinha sido registrado duas vezes, dois elementos usavam o mesmo identificador e alguns layouts
ficaram sem dono — o tipo de defeito que faz o PowerPoint pedir para "reparar" o arquivo. O programa que
junta decks ganhou uma etapa que conserta isso, e três testes automáticos.
• <b>O grafo</b>. O mapa do projeto (slide 16) é atualizado. Primeiro o código; depois, a lista do que ele não
deve ler (dados, figuras, arquivos do Office, PDFs gerados, o legado); por fim, os documentos. O grafo fica
com {N.g_nos} nós, {N.g_arestas} arestas e {N.g_com} comunidades. Uma <b>comunidade</b> é um grupo de nós
muito ligados entre si — um assunto do projeto.
• <b>main</b>. O <b>branch</b> principal (A.10) passa a se chamar `main`, o nome padrão atual.
• <b>Estas apresentações</b>. A cronologia e a das demandas de setembro, geradas por programa a partir do git
e das tabelas.""",
             apresentar="""“Nos últimos dias, consertei a estrutura interna do deck principal, para que o PowerPoint não precise
repará-lo, e atualizei o mapa do projeto, que agora lê também os documentos. E estas duas apresentações
foram geradas a partir do histórico e das tabelas.”"""),

        dict(n=29, titulo="As decisões de método, em ordem",
             frase="A divisória do capítulo 8, a primeira leitura transversal: todas as decisões de método juntas.",
             mostra="""O número 8 em vermelho, o título "As decisões de método, em ordem" e o subtítulo: o que foi decidido,
quando, e o que ficou para a orientadora.""",
             zero="""A partir daqui, o deck deixa de seguir o calendário e passa a cortar o projeto por tema. Esta leitura
junta as decisões de método: as já consolidadas e as que esperam a orientadora.""",
             apresentar="""“Agora três leituras por tema. A primeira: as decisões de método.”"""),

        dict(n=30, titulo="As decisões consolidadas do GUIA",
             frase="As doze decisões de método já tomadas e registradas no GUIA do projeto, cada uma com a data em que foi tomada.",
             mostra="""Uma tabela com três colunas: o número da seção do GUIA (de 6.2.1 a 6.2.12), a decisão e a data. Onde o
GUIA não registra a data e nenhum commit a isola, aparece um travessão.""",
             zero="""As doze decisões, em palavras simples:

• <b>6.2.1 — denominador</b>: os indicadores de domicílio dividem por `V00001` (domicílios), como o IVS-BH
2012, e não por `V01042` (responsáveis).
• <b>6.2.2 — analfabetismo</b>: taxa, e não razão (A.4).
• <b>6.2.3 — razão de moradores</b>: moradores ÷ domicílios, contando também os improvisados, exatamente como
o IBGE calcula o número publicado — o que permite conferir.
• <b>6.2.4 — a ordem do rótulo de sigilo</b>: cada setor recebe um rótulo de qualidade do dado (`Dados_sig`).
Testa-se primeiro se o setor tem população zero, depois se há sigilo, depois se é coletivo. Na ordem
antiga, setores vazios (muitos são lagos e represas) eram contados como sigilosos.
• <b>6.2.5 — recorte urbano</b>: aplicado na análise, não na extração (A.3).
• <b>6.2.6 — sigilo</b>: o X vira ausente, nunca zero; o analfabetismo sob sigilo não é preenchido (A.2).
• <b>6.2.7 — envelhecimento</b>: idosos ÷ menores de 15, a definição da literatura (Galvão e colegas, 2025).
• <b>6.2.8 — favelas</b>: identificadas pelo campo oficial `CD_TIPO = 1`.
• <b>6.2.9 — água canalizada</b>: pelo complemento de `V00199` (slide 17).
• <b>6.2.10 — caçamba</b>: destino inadequado, como no IVS-BH 2012 (slide 13).
• <b>6.2.11 — indicadores descritivos</b>: ficam fora do índice, por não terem direção clara (slide 14).
• <b>6.2.12 — fórmulas</b>: num módulo compartilhado (slide 17).""",
             apresentar="""“Estas são as doze decisões de método já consolidadas, todas registradas no GUIA com a justificativa e
a alternativa descartada. Quase todas seguem o mesmo princípio: ficar o mais perto possível do método do
IVS de Belo Horizonte, para que os índices sejam comparáveis.”""",
             perguntas=[("Alguma dessas decisões pode mudar?", "Pode, se a orientadora pedir — e o GUIA registra a alternativa descartada de cada uma, justamente para que voltar atrás seja fácil. A da caçamba é a mais discutível, por causa do comportamento do lixo.")]),

        dict(n=31, titulo="As regras de setembro, e o que não é decisão minha",
             frase="As regras fixadas antes de rodar a grade do IVS final — e a lista do que fica com a orientadora.",
             mostra="""Quatro blocos. À esquerda: <b>elegibilidade</b> (os quatro critérios mínimos), <b>escolha</b> (os três
critérios para apontar a referência) e <b>incerteza</b> (sensibilidade por município, não bootstrap). À
direita, com o filete vermelho: <b>fica com a orientadora</b> — as sete escolhas que o projeto não faz
sozinho.""",
             zero="""• <b>Elegibilidade</b>: KMO de pelo menos 0,70, MSA de pelo menos 0,50, comunalidade de pelo menos 0,30 e
carga máxima de pelo menos 0,40 (A.6). Basta falhar em um para a especificação sair.
• <b>Escolha</b>: entre as elegíveis, a de melhor posição média em três critérios com o mesmo peso:
estabilidade, AUC dentro do município e parcimônia (A.9).
• <b>Incerteza</b>: medida tirando um município de cada vez (A.8).
• <b>O que fica com a orientadora</b>: qual renda (original, sem o extremo ou com a mediana municipal);
qual rotação; como dividir os pesos na rotação oblíqua; se o lixo entra; se o banheiro entra, e em qual
versão; a normalização (no município ou global); e a regra das faixas (a do IVS-BH 2012 ou quartis).

O ponto central é a ordem: as regras foram escritas <i>antes</i> de rodar a grade. Se fossem escritas
depois, sempre se poderia ajustá-las até a especificação preferida ganhar.""",
             apresentar="""“As regras foram fixadas antes de rodar, para que o resultado não escolhesse a regra. E há sete
escolhas que eu não faço: o NB05 mostra o que cada uma muda, com números, e a decisão é da orientadora.”""",
             perguntas=[("Por que o próprio pesquisador não escolhe?", "Porque são escolhas de método com consequências para a comparação com o IVS-BH 2012 e para o artigo, e cabem a quem orienta. O papel da análise é mostrar, com números, o que cada opção muda.")]),

        dict(n=32, titulo="Os achados, em ordem",
             frase="A divisória do capítulo 9, a segunda leitura transversal: o que se descobriu sobre os dados e sobre o próprio código.",
             mostra="""O número 9 em vermelho, o título "Os achados, em ordem" e o subtítulo: o que se descobriu sobre os dados e
sobre o próprio código, na ordem em que apareceu.""",
             zero="""Um <b>achado</b> é um fato descoberto pela análise: um problema nos dados, um erro no código, um resultado
que muda a interpretação. Esta leitura junta os treze principais.""",
             apresentar="""“A segunda leitura: os achados, na ordem em que apareceram.”"""),

        dict(n=33, titulo="Os achados",
             frase="Os cinco primeiros achados: o analfabetismo acima de 1, o lixo isolado, as favelas, a água que fecha a conta e o setor de renda extrema.",
             mostra="""Cinco entradas: 22/05, 18/06, 09/08, 21/08 e 02/09.""",
             zero=f"""• <b>22/05 — o analfabetismo acima de 1</b>. Uma "taxa" que passava de 100% era sinal de fórmula errada: era
uma razão (slide 11).
• <b>18/06 — o lixo isolado</b>. O lixo é a variável que menos se correlaciona com as outras, e a única em
que os 70 municípios estão <i>pior</i> que o Brasil urbano. Esse achado acompanha a decisão da caçamba e
volta na análise fatorial: o lixo tende a formar um fator sozinho.
• <b>09/08 — as favelas</b>. Quase um em cada cinco setores urbanos do recorte é favela ou comunidade urbana
(19.452, 18,7%). E os dois jeitos de identificá-las — o campo `CD_TIPO = 1` e o nome da comunidade
preenchido — coincidem nos 468.099 setores do país.
• <b>21/08 — a água fecha a conta</b>. As três categorias de abastecimento somam exatamente o total de
domicílios em 100,00% dos 81.270 setores com as três presentes: dá para medir pelo complemento sem perder
nada.
• <b>02/09 — o setor extremo</b>. Um único setor de Belo Horizonte, com renda média de {N.renda_extremo},
muda a escala da renda de todos os setores na normalização. Daí a coluna sem ele e, em setembro, a versão com
a mediana.""",
             apresentar="""“Os primeiros achados são sobre os dados: uma fórmula de analfabetismo errada, o lixo que não conversa
com as outras variáveis, o tamanho das favelas no recorte, a água que fecha a conta e um setor de renda
extrema que distorce a escala.”"""),

        dict(n=34, titulo="Os achados (continuação)",
             frase="O índice contra a renda, dois erros de código corrigidos, o lixo que pede um fator só e a partição exata do banheiro.",
             mostra="""Cinco entradas: 17/09, três de 25/09 e 26/09.""",
             zero=f"""• <b>17/09 — o índice contra a renda</b>. O índice do NB04 separa as favelas com AUC {N.auc_ind}; a renda
sozinha, com {N.auc_renda}. E mais: a <b>média simples dos postos</b> — ordenar os setores em cada indicador e
tirar a média das posições, sem peso nenhum — chega a {N.auc_postos}, também acima do índice. Ou seja: na
tarefa de separar favelas, os pesos da fatorial não ajudam.
• <b>25/09 — a Varimax</b>. Parava antes de convergir (slide 22); corrigida, o NB04 foi regerado.
• <b>25/09 — a água do Brasil</b>. A proporção nacional sem água canalizada saía 0,986 em vez de 0,0138,
porque o cálculo agregado esquecia o complemento.
• <b>25/09 — sem o lixo, um fator só</b>. No IVS-6 (o IVS-7 sem o lixo), as duas regras de quantos fatores
manter (A.6) indicam um fator só: a vulnerabilidade vira uma dimensão única. Com o lixo, ele ocupa um fator
sozinho. É uma pista de que a estrutura em duas dimensões depende do lixo.
• <b>26/09 — a partição exata</b>. A falta de banheiro (`V00495`) é exatamente a soma das suas três partes
em {N.part_bate} de {N.part_pres} setores (slide 25).""",
             apresentar=f"""“Em setembro, os achados ficam mais incômodos: a renda sozinha, e até uma média simples sem peso,
separam as favelas melhor que o índice; e, sem o lixo, a análise fatorial enxerga uma dimensão só. Também
apareceram dois erros de código, ambos corrigidos.”""",
             perguntas=[("Se a média sem peso é melhor, a fatorial é inútil?", "Não para o que ela faz — descobrir como os indicadores se agrupam. Mas o achado mostra que a validação contra favelas, sozinha, não justifica os pesos. Por isso a escolha da especificação usa três critérios, e não só a AUC.")]),

        dict(n=35, titulo="Os achados (continuação)",
             frase="Os três achados do IVS final: o IVS-7 não passa nos critérios, a renda vence em todas as especificações e o critério de estabilidade engana nos pesos fixos.",
             mostra="""Três entradas, todas de 27/09.""",
             zero=f"""• <b>O IVS-7 não passa</b>. A base do NB04, com os sete indicadores, falha num critério: a comunalidade da
água fica em {N.h2_agua}, abaixo do mínimo de 0,30 (A.6). A água conversa pouco com o resto quando o lixo
está junto. Sem o lixo, ou acrescentando a falta de banheiro (`V00495`), a análise passa.
• <b>A renda vence em todas</b>. Nas {N.acr_n} especificações elegíveis, a renda sozinha separa as favelas
melhor que o índice — tanto comparando todos os setores juntos ({N.acr_rg} de {N.acr_n}) quanto dentro de
cada município ({N.acr_rm} de {N.acr_n}). Mas, dentro de cada faixa de renda (os decis, A.7), o índice
separa melhor em {N.acr_ie} de {N.acr_n}: ele traz informação que a renda não tem.
• <b>A estabilidade engana</b>. O critério de estabilidade mede quanto o peso do primeiro fator muda ao tirar
um município. Com pesos fixos (50/50 ou 60/40), o peso não muda nunca — não porque seja estável, mas porque
foi fixado. Essas especificações ganham o critério "de graça", e é isso que decide a referência proposta.""",
             apresentar="""“Os achados do IVS final são três: a base original não passa nos critérios de qualidade; a renda vence
o índice em todas as especificações, mas o índice vence dentro de cada faixa de renda; e o critério de
estabilidade favorece os pesos fixos sem mérito. Os três vão para a mesa da orientadora.”""",
             perguntas=[("Isso invalida a referência proposta?", "Não invalida, mas pede cautela: a referência ganhou em parte por um critério que não a testou. O deck das demandas mostra a alternativa que surge quando a estabilidade é medida de outro jeito.")]),

        dict(n=36, titulo="A organização, em ordem",
             frase="A divisória do capítulo 10, a terceira leitura transversal: como o repositório chegou à forma de hoje.",
             mostra="""O número 10 em vermelho, o título "A organização, em ordem" e o subtítulo: como o repositório chegou à
forma de hoje — pastas, módulo, testes, documentação e apresentações.""",
             zero="""A organização é o que permite a outra pessoa — ou ao próprio autor, meses depois — achar cada coisa e
refazer cada número. Esta leitura conta como ela foi construída.""",
             apresentar="""“A terceira leitura: a organização do projeto.”"""),

        dict(n=37, titulo="A organização",
             frase="Do documento mestre ao ambiente que roda do zero: como o projeto ficou reproduzível.",
             mostra="""Seis entradas: 14/05, 15/05, 19/06, 20/08, 21/08 e 02/09.""",
             zero="""• <b>14/05 — um documento mestre</b>: o GUIA concentra identidade, método, decisões e plano.
• <b>15/05 — o legado no Backup/</b>: as versões antigas saem do caminho, sem serem apagadas.
• <b>19/06 — versões fixadas</b>: as bibliotecas ficam com versão definida, e cada tabela da EDA tem a
procedência registrada.
• <b>20/08 — o código sai dos notebooks</b>: as fórmulas vão para o módulo `src/ivs_censo`; os programas que
rodam sozinhos, para `scripts/`.
• <b>21/08 — o ambiente roda do zero</b>: qualquer computador com as instruções consegue recriar o ambiente
e rodar os notebooks; 59 testes automáticos.
• <b>02/09 — uma apresentação na raiz</b>: a atual fica à vista; o apoio vai para `complementos/`; o que
saiu de circulação, para `historico/`.

<b>Reproduzível</b> quer dizer que outra pessoa, com os mesmos dados e o mesmo código, chega aos mesmos
números. É o padrão de qualidade da pesquisa atual.""",
             apresentar="""“A organização foi construída aos poucos, sempre com o mesmo objetivo: que qualquer pessoa consiga
achar cada coisa e refazer cada número.”"""),

        dict(n=38, titulo="A organização (continuação)",
             frase="A documentação por tipo de uso, o repositório limpo, os decks montados por programa e o mapa do projeto.",
             mostra="""Quatro entradas: 17/09, 25/09, 27/09 e 01/10.""",
             zero="""• <b>17/09 — documentação por tipo de uso</b>: `docs/` ganha subpastas — `metodologia/` (guias e notas de
método), `relatorios/` (os relatórios), `prompts/` (planos de execução e arquivos de estado de cada fase),
`referencias/` (material de terceiros) e `Apresentacoes_IVS/`. O índice dos executáveis fica em
`scripts/README.md`, e 61 tabelas ganham procedência.
• <b>25/09 — o repositório limpo</b>: arquivos de configuração que deviam estar no git passam a estar, e a
árvore de pastas documentada é regerada direto da lista de arquivos do git.
• <b>27/09 — decks por programa</b>: o deck principal não é mais regerado; recebe blocos novos, gerados por
programa, pelo "juntador".
• <b>01/10 — o mapa</b>: o grafo do projeto passa a cobrir código e documentos, para achar onde cada coisa
está.""",
             apresentar="""“Em setembro, a documentação foi separada por tipo de uso, e as apresentações passaram a ser montadas
por programa — o que é a garantia de que nenhum número fica desatualizado num slide.”"""),

        dict(n=39, titulo="O repositório hoje",
             frase="Uma tabela com cada pasta do projeto, o que ela guarda e quantos arquivos tem.",
             mostra=f"""Uma tabela com três colunas: a pasta, o que ela guarda e quantos arquivos ela tem no git, contados na
hora em que o deck foi gerado. A linha dos testes informa {N.testes} testes coletados.""",
             zero=f"""Um roteiro das pastas, de cima para baixo:

• `notebooks/Fase3_EDA_ELSI/` — os notebooks da análise: NB01, NB02, NB04, NB04b e NB05;
• `src/ivs_censo/` — o módulo com as fórmulas e as funções compartilhadas;
• `scripts/` — os programas que rodam sozinhos (entrega, auditorias, fatorial, NB05, decks e este guia);
• `tests/` — os testes automáticos, que conferem se o código dá o resultado esperado. "{N.testes}
coletados" é quantos testes o programa de testes (o `pytest`) encontrou;
• `banco_de_dados/` — as saídas: a entrega à orientadora, as tabelas da EDA, da fatorial e do NB05;
• `docs/metodologia/`, `docs/relatorios/`, `docs/prompts/`, `docs/referencias/` — a documentação, por tipo;
• `docs/Apresentacoes_IVS/` — as apresentações;
• `Backup/` — o legado;
• `graphify-out/` — o grafo do projeto.

A pasta `dados/`, com os arquivos brutos do IBGE (vários gigabytes), não vai para o git: é baixada de novo
quando necessário.""",
             numeros="""O número de arquivos não mede importância: `banco_de_dados/` e `graphify-out/` têm muitos arquivos
porque guardam saídas geradas automaticamente; `src/ivs_censo/` tem poucos, mas é o coração do cálculo.""",
             apresentar="""“É assim que o repositório está hoje: cada pasta com um papel, e um mapa completo no MANUAL do
projeto.”"""),

        dict(n=40, titulo="Onde o projeto está",
             frase="A divisória do capítulo 11: o cronograma contra o que foi feito, e o que vem depois.",
             mostra="""O número 11 em vermelho, o título "Onde o projeto está" e o subtítulo: o cronograma contra o que foi
feito, e o que vem depois.""",
             zero="""O fecho do deck volta ao calendário, mas olhando para a frente.""",
             apresentar="""“Para fechar, onde o projeto está e o que vem.”"""),

        dict(n=41, titulo="O cronograma contra o realizado",
             frase="Cada etapa do cronograma da bolsa, o período previsto e a situação de hoje.",
             mostra="""Uma tabela com nove linhas e três colunas: a etapa, o período previsto no cronograma e onde ela está.""",
             zero=f"""Linha a linha:

• <b>Consistência do banco de dados</b> (prevista de março a julho): feita, com auditorias em maio, agosto e
setembro e a revisão geral.
• <b>Análise descritiva</b> (março a setembro): feita — o NB02 e a EDA Central, em duas rodadas.
• <b>Demandas de julho</b>: feitas em 09/08.
• <b>Demandas de setembro e os nove itens seguintes</b>: feitos de 25 a 27/09; faltam as respostas da
orientadora.
• <b>Cálculo do IVS</b> (agosto e setembro): a análise fatorial e o NB05 estão prontos, com {N.n_eleg}
especificações elegíveis e uma referência proposta; as escolhas são da orientadora.
• <b>Faixas de risco</b> (setembro): calculadas para a referência pelas duas regras; falta escolher a regra.
• <b>Mapas temáticos</b> (setembro): pendentes. Os mapas mostram o IVS de cada setor no mapa da cidade, num
programa de geoprocessamento (o QGIS).
• <b>Artigo científico</b> (outubro a dezembro): o plano está preenchido; a redação, pendente.
• <b>Relatório Final de IC</b> (dezembro a fevereiro): a começar.""",
             apresentar="""“O cronograma está em dia até o cálculo do índice, que só depende das escolhas da orientadora. Os mapas
estão atrasados em relação ao previsto, porque dependem do índice fechado. O artigo e o relatório final
vêm depois.”""",
             perguntas=[("Por que os mapas ainda não foram feitos?", "Porque mapear antes de fechar a especificação seria fazer o trabalho duas vezes: os mapas dependem do índice e das faixas finais.")]),

        dict(n=42, titulo="O que vem depois",
             frase="Os próximos cinco passos, na ordem em que um destrava o seguinte.",
             mostra="""Cinco blocos numerados, um embaixo do outro; o primeiro tem o filete vermelho.""",
             zero="""• <b>1. As escolhas da orientadora</b>: renda, rotação, pesos, lixo, banheiro, normalização e faixas — com
os números do NB05 ao lado de cada pergunta. Tudo depende disto.
• <b>2. O IVS final fechado</b>: rodar a especificação escolhida, gravar o índice e as faixas de cada setor e
conferir contra a referência proposta.
• <b>3. Os mapas temáticos</b>: o IVS e as faixas no mapa, município a município.
• <b>4. O artigo</b>: escrito na ordem do plano — tabelas, método, resultados, discussão, introdução e
resumo —, seguindo o STROBE, uma lista de verificação internacional para relatar estudos observacionais.
• <b>5. O relatório final</b>: de dezembro a fevereiro, com a submissão do artigo em fevereiro de 2027.""",
             apresentar="""“O próximo passo não é meu: são as escolhas da orientadora. Com elas, o índice fecha, os mapas saem e o
artigo começa.”"""),

        dict(n=43, titulo="De onde saiu esta cronologia",
             frase="As fontes de cada parte do deck e o comando para gerá-lo de novo.",
             mostra=f"""Uma tabela com duas colunas: a fonte e o que ela deu ao deck — o git ({N.commits} commits, de
{N.primeiro} a {N.ultimo}), o GUIA do projeto, as tabelas da fatorial ampliada e da grade do NB05, os
arquivos de estado das fases, os relatórios e o grafo. Embaixo, a data em que o deck foi gerado e o comando
para gerá-lo de novo.""",
             zero="""Este slide existe para a <b>rastreabilidade</b>: qualquer número ou data do deck pode ser seguido até a
sua origem. O comando no pé (`node scripts/gerar_deck_cronologia.js`) roda o programa que monta o deck;
`node` é o programa que executa código escrito em JavaScript.""",
             apresentar="""“Tudo o que vocês viram sai destas fontes, e o deck pode ser gerado de novo a qualquer momento, com os
dados do dia.”"""),
    ]
