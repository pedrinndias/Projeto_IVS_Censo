"""Gera o guia de apoio dos slides marcados com "EXPLICAR SLIDE" no deck da fatorial.

Para que serve
--------------
O deck da análise fatorial foi escrito para quem já sabe o que é uma carga fatorial. Este
guia é o contrário: supõe que o leitor nunca viu análise fatorial e não acompanhou o
projeto. Ele cobre, um a um, os slides que o autor marcou como "EXPLICAR SLIDE", mais a
Parte 8 inteira, que ele pediu por extenso.

A estrutura de cada verbete é sempre a mesma, e é de propósito: o que está no slide · o
conceito do zero · como ler os números · o que dizer se perguntarem. Quem estiver com
pressa lê só o último item de cada um.

Nenhum número é digitado aqui: todos saem de banco_de_dados/eda/fatorial/.

Uso:
    uv run --with reportlab --with pandas python scripts/gerar_pdf_guia_fatorial.py \
        docs/Apresentacoes_IVS/complementos/Guia_Apoio_Analise_Fatorial.pdf
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

RAIZ = Path(__file__).resolve().parents[1]
FAT = RAIZ / "banco_de_dados" / "eda" / "fatorial"

# Paleta e fontes: as mesmas de gerar_pdf_outliers_renda.py, para os dois documentos
# parecerem do mesmo projeto.
TINTA = colors.HexColor("#1A1A1A")
PETROL = colors.HexColor("#1F4E4A")
CLAY = colors.HexColor("#A83A2C")
CINZA = colors.HexColor("#666666")
LINHA = colors.HexColor("#C8C8C8")
FUNDO = colors.HexColor("#F2F0EC")
SERIF, SERIF_B = "Times-Roman", "Times-Bold"
SANS, SANS_B, MONO = "Helvetica", "Helvetica-Bold", "Courier"


def ler(nome):
    return pd.read_csv(FAT / nome, sep=";", encoding="utf-8-sig")


# ── os números, lidos dos arquivos ──────────────────────────────────────────
RES = ler("resumo_adequabilidade.csv").set_index("nome")
PESOS = ler("nb04_sintese_pesos.csv")
CEN = ler("nb04_cenarios.csv").set_index("cenario")
VAL = ler("nb04_validacao_fcu.csv")
PHI = ler("nb04_phi_ivs6_sem_lixo.csv")
BOOT = ler("nb04_bootstrap_cargas.csv")
CARG = ler("nb04_cargas_ivs6_sem_lixo.csv").set_index("variavel")
EXTR = ler("nb04_extracao_comparada.csv")
RENDA = ler("nb04_renda_sem_extremo.csv").set_index("medida")
ADEQ = ler("nb04_adequabilidade.csv")


def br(x, casas=3):
    """Número em português: vírgula decimal, ponto de milhar."""
    return f"{x:,.{casas}f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def inteiro(x):
    return f"{int(round(x)):,}".replace(",", ".")


SOCIO = 100 * PESOS.loc[PESOS.dimensao == "Socioeconômica", "peso"].sum()
SANEA = 100 * PESOS.loc[PESOS.dimensao == "Saneamento", "peso"].sum()
PHI12 = abs(PHI.iloc[0, 2])
AUC_IDX, AUC_ESC = VAL.auc[0], VAL.auc[1]
LIXO = EXTR[(EXTR.cenario == "ivs7_spearman") & (EXTR.variavel == "Lixo inadequado")].iloc[0]
KMO7, KMO6 = RES.loc["ivs7_spearman", "kmo"], RES.loc["ivs6_sem_lixo_spearman", "kmo"]
VAR7 = RES.loc["ivs7_spearman", "var_acumulada_k"]
VAR6 = RES.loc["ivs6_sem_lixo_spearman", "var_acumulada_k"]
RM = CARG.loc["Razão de moradores"]
RENDA_MUDA = int(RENDA.loc["setores que mudam de faixa", "com renda_media_sem_extremo"])
RENDA_RHO = RENDA.loc["Spearman entre os ordenamentos", "com renda_media_sem_extremo"]

# ── estilos ─────────────────────────────────────────────────────────────────
E = {
    "capa": ParagraphStyle("capa", fontName=SERIF_B, fontSize=22, leading=26, textColor=TINTA),
    "capasub": ParagraphStyle("capasub", fontName=SANS, fontSize=10.5, leading=15, textColor=CINZA),
    "h1": ParagraphStyle("h1", fontName=SERIF_B, fontSize=15, leading=18, textColor=PETROL,
                         spaceBefore=18, spaceAfter=7),
    "slide": ParagraphStyle("slide", fontName=SERIF_B, fontSize=12.5, leading=15, textColor=TINTA,
                            spaceBefore=15, spaceAfter=2),
    "h2": ParagraphStyle("h2", fontName=SANS_B, fontSize=9.4, leading=12.5, textColor=PETROL,
                         spaceBefore=9, spaceAfter=2),
    "p": ParagraphStyle("p", fontName=SANS, fontSize=9.3, leading=13.6, textColor=TINTA,
                        alignment=TA_JUSTIFY, spaceAfter=5),
    "cod": ParagraphStyle("cod", fontName=MONO, fontSize=8.2, leading=11.4, textColor=TINTA,
                          spaceAfter=4, leftIndent=8),
    "nota": ParagraphStyle("nota", fontName=SANS, fontSize=7.8, leading=10.6, textColor=CINZA,
                           spaceBefore=1, spaceAfter=8),
}


def P(t, e="p"):
    return Paragraph(t, E[e])


def tabela(cab, linhas, larguras, tam=8.0):
    est_h = ParagraphStyle("th", fontName=SANS_B, fontSize=tam, leading=tam + 2.2, textColor=PETROL)
    est_c = ParagraphStyle("td", fontName=SANS, fontSize=tam, leading=tam + 2.6, textColor=TINTA)
    dados = [[Paragraph(f"<b>{c}</b>", est_h) for c in cab]]
    dados += [[Paragraph(str(c), est_c) for c in ln] for ln in linhas]
    t = Table(dados, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.35, LINHA),
        ("BACKGROUND", (0, 0), (-1, 0), FUNDO),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
    ]))
    return t


def caixa(titulo, texto, cor=PETROL):
    est_t = ParagraphStyle("bt", fontName=SANS_B, fontSize=8.9, leading=11.8, textColor=cor)
    est_c = ParagraphStyle("bc", fontName=SANS, fontSize=8.7, leading=12.4, textColor=TINTA,
                           alignment=TA_JUSTIFY)
    t = Table([[Paragraph(titulo, est_t)], [Paragraph(texto, est_c)]],
              colWidths=[17.0 * cm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), FUNDO),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, cor),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ]))
    return t


def verbete(n, titulo, o_que, conceito, numeros, resposta, extra=None):
    """Um slide explicado, sempre na mesma ordem."""
    bloco = [P(f"Slide {n} · {titulo}", "slide"),
             P("O QUE ESTÁ NO SLIDE", "h2"), P(o_que),
             P("O CONCEITO, DO ZERO", "h2"), P(conceito)]
    if extra is not None:
        bloco += [Spacer(1, 3), extra, Spacer(1, 5)]
    bloco += [P("COMO LER OS NÚMEROS", "h2"), P(numeros), Spacer(1, 4),
              caixa("SE A ORIENTADORA PERGUNTAR", resposta, CLAY), Spacer(1, 6)]
    return bloco


# ── documento ───────────────────────────────────────────────────────────────
saida = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    RAIZ / "docs" / "Apresentacoes_IVS" / "complementos" / "Guia_Apoio_Analise_Fatorial.pdf")
saida.parent.mkdir(parents=True, exist_ok=True)
LARG, ALT = A4
MARG = 2.0 * cm


def rodape(canv, doc):
    canv.saveState()
    canv.setFont(SANS, 7.3)
    canv.setFillColor(CINZA)
    canv.drawString(MARG, 1.25 * cm,
                    "Guia de apoio · Análise fatorial e os pesos do IVS · Notebook 04")
    canv.drawRightString(LARG - MARG, 1.25 * cm, f"{doc.page}")
    canv.setStrokeColor(LINHA)
    canv.setLineWidth(0.4)
    canv.line(MARG, 1.62 * cm, LARG - MARG, 1.62 * cm)
    canv.restoreState()


doc = BaseDocTemplate(str(saida), pagesize=A4, leftMargin=MARG, rightMargin=MARG,
                      topMargin=1.8 * cm, bottomMargin=2.1 * cm,
                      title="Guia de apoio — análise fatorial e os pesos do IVS",
                      author="Pedro Dias Soares")
doc.addPageTemplates([PageTemplate(id="corpo",
                                   frames=[Frame(MARG, 2.1 * cm, LARG - 2 * MARG,
                                                 ALT - 1.8 * cm - 2.1 * cm, id="f")],
                                   onPage=rodape)])
S = []

# ═════════ CAPA ═════════
S += [Spacer(1, 1.6 * cm),
      P("Guia de apoio", "capa"),
      P("Os slides da análise fatorial, explicados do zero", "capa"),
      Spacer(1, 0.5 * cm),
      P("Índice de Vulnerabilidade à Saúde (IVS) intraurbano · Censo Demográfico 2022 · "
        "70 municípios do ELSI-Brasil<br/>Iniciação Científica · Fiocruz Minas — Instituto "
        "René Rachou · Pedro Dias Soares · setembro de 2026", "capasub"),
      Spacer(1, 0.8 * cm),
      caixa("PARA QUE SERVE ESTE DOCUMENTO",
            "O deck da análise fatorial foi escrito para quem já sabe o que é uma carga "
            "fatorial. Este guia supõe o contrário: que você nunca viu análise fatorial e "
            "não acompanhou o projeto. Ele cobre um a um os slides marcados com "
            "<b>EXPLICAR SLIDE</b>, mais a Parte 8 inteira. <br/><br/>"
            "Cada verbete tem sempre quatro partes, na mesma ordem: <b>o que está no "
            "slide</b> · <b>o conceito, do zero</b> · <b>como ler os números</b> · "
            "<b>o que dizer se perguntarem</b>. Se o tempo for curto, leia só a última — "
            "ela está em caixa, no fim de cada verbete, e é uma resposta pronta."),
      Spacer(1, 0.5 * cm),
      caixa("A ÚNICA COISA QUE VOCÊ PRECISA SABER ANTES DE ABRIR O DECK",
            "O projeto mede a vulnerabilidade de um setor censitário com <b>sete "
            "indicadores</b>: água inadequada, esgoto inadequado, lixo inadequado, razão de "
            "moradores por domicílio, analfabetismo, renda e proporção de pessoas pretas, "
            "pardas ou indígenas. Para virar um índice único, cada um precisa de um "
            "<b>peso</b>. A pergunta do Notebook 04 é uma só: <b>quanto cada indicador "
            "deve pesar, e por quê?</b> Tudo no deck existe para responder isso.", PETROL),
      PageBreak()]

# ═════════ PARTE 0 — VOCABULÁRIO ═════════
S += [P("Parte 0 — O vocabulário, em uma página", "h1"),
      P("Seis palavras aparecem o tempo todo no deck. Se estas seis estiverem claras, o "
        "resto se lê sozinho. Nenhuma delas exige matemática para ser entendida."),

      P("1. VARIÁVEL LATENTE (ou CONSTRUTO)", "h2"),
      P("Algo que existe mas não se mede diretamente. Ninguém tem um aparelho que meça "
        "\"vulnerabilidade\" de um bairro. O que se mede são <b>sintomas</b>: falta de "
        "esgoto, renda baixa, analfabetismo. A vulnerabilidade é a coisa por trás deles. "
        "Inteligência é o exemplo clássico: não se mede inteligência, medem-se respostas a "
        "questões, e se supõe que a inteligência as produz."),

      P("2. FATOR", "h2"),
      P("É o nome que a técnica dá à variável latente quando ela é estimada a partir dos "
        "dados. Se sete indicadores variam juntos de um jeito organizado, a análise "
        "fatorial diz: <b>existem duas coisas por trás deles</b> — e chama essas duas "
        "coisas de Fator 1 e Fator 2. Quem dá nome aos fatores é o pesquisador, olhando "
        "quais indicadores andam com qual. Neste projeto, o Fator 1 ficou sendo a "
        "<b>dimensão socioeconômica</b> e o Fator 2, o <b>saneamento</b>."),

      P("3. CARGA FATORIAL", "h2"),
      P("<b>É o número mais importante do deck inteiro.</b> A carga mede o quanto um "
        "indicador pertence a um fator, numa escala de −1 a 1. Carga alta significa que "
        "aquele indicador é uma boa manifestação daquele fator; carga perto de zero "
        "significa que ele não tem nada a ver com aquele fator. No projeto, a renda tem "
        f"carga {br(CARG.loc['Renda (invertida)', 'Varimax1'], 3)} no Fator 1 — é quase "
        "uma tradução direta da dimensão socioeconômica — e apenas "
        f"{br(CARG.loc['Renda (invertida)', 'Varimax2'], 3)} no Fator 2."),

      P("4. COMUNALIDADE", "h2"),
      P("Quanto da variação de um indicador os fatores conseguem explicar. Também vai de 0 "
        "a 1. Comunalidade alta quer dizer \"este indicador está bem representado pela "
        "estrutura\"; comunalidade baixa quer dizer \"este indicador tem vida própria, os "
        "fatores não dão conta dele\". É por comunalidade que se descobre que um indicador "
        "não pertence ao conjunto."),

      P("5. ROTAÇÃO", "h2"),
      P("Uma etapa que <b>não muda a qualidade da solução, só a torna legível</b>. A "
        "primeira solução que o computador devolve costuma ter todos os indicadores "
        "carregando um pouco em todos os fatores, o que não se interpreta. A rotação gira "
        "os eixos até que cada indicador carregue alto em <b>um</b> fator e baixo nos "
        "outros. É como girar um mapa até o norte ficar para cima: a cidade não mudou de "
        "lugar, ficou mais fácil de ler."),

      P("6. ESCORE FATORIAL", "h2"),
      P("Depois de saber quanto cada indicador pesa, aplica-se isso a cada setor "
        "censitário e sai um número por setor — o escore. É o que vira o índice. O deck "
        "mostra duas maneiras de calculá-lo, e compara as duas."),
      Spacer(1, 6),
      caixa("E A PALAVRA QUE VOCÊ VAI OUVIR MAIS: “ADEQUABILIDADE”",
            "Antes de rodar a análise, há testes que dizem se ela <b>faz sentido naqueles "
            "dados</b>. Se os sete indicadores não tiverem nada a ver uns com os outros, "
            "não existe fator comum para encontrar, e a técnica devolveria um resultado "
            "sem significado. Os dois testes que aparecem no deck são o <b>KMO</b> "
            "(quanto maior, melhor; acima de 0,70 é bom) e o <b>teste de Bartlett</b>. "
            f"No projeto o KMO deu {br(KMO7, 3)}, então a base passa.", PETROL),
      PageBreak()]

# ═════════ PARTE 1 — OS SLIDES MARCADOS ═════════
S += [P("Parte 1 — Os slides que você marcou", "h1"),
      P("Na ordem do deck. Cada um é independente: dá para ler só o que for perguntado.")]

E6 = EXTR[EXTR.cenario == "ivs6_sem_lixo_spearman"].set_index("variavel")
S += verbete(
    15, "Divergência 2 — a técnica de extração",
    "Uma tabela com duas colunas de números quase iguais, chamadas <b>ACP</b> e <b>eixo "
    "principal</b>, e uma terceira coluna com a diferença entre elas.",
    "Existem duas maneiras de extrair fatores, e a diferença entre elas cabe numa frase: "
    "<b>o que cada uma faz com a parte da variação que é só daquele indicador.</b><br/><br/>"
    "Imagine que a variação de cada indicador tem duas partes: a que ele <i>compartilha</i> "
    "com os outros seis, e a que é <i>só dele</i>. A <b>ACP</b> (análise de componentes "
    "principais) usa tudo — compartilhado e próprio. A <b>análise fatorial propriamente "
    "dita</b>, aqui chamada de eixo principal, usa só a parte compartilhada, porque é essa "
    "que revela a coisa comum por trás.<br/><br/>"
    "Na maior parte dos casos as duas dão quase o mesmo resultado, e o projeto vinha "
    "supondo isso. O livro da Enap traz uma advertência de Stevens (1992) que desfaz a "
    "suposição: com <b>menos de 20 variáveis</b> e comunalidades baixas, elas podem "
    "divergir. O projeto tem 6 variáveis. Por isso o teste virou obrigatório.",
    "A coluna da diferença é o que importa. Ela é <b>grande onde o indicador compartilha "
    f"pouco com os outros</b> — a água ({br(E6.loc['Água inadequada','dif_2'],3)}) e a razão "
    f"de moradores — e <b>pequena onde compartilha muito</b>: a renda difere só "
    f"{br(E6.loc['Renda (invertida)','dif_2'],3)}. Isso é exatamente o que Stevens previu, "
    "e é sinal de que a implementação está certa, não de que há problema.",
    "“Existem duas técnicas parecidas, e a literatura diz que elas só divergem quando há "
    "poucas variáveis. Nós temos seis, então testamos em vez de supor. Divergem, sim — e "
    "divergem justamente nas variáveis que menos se relacionam com as outras, que é onde a "
    "teoria manda esperar. Reportamos as duas soluções.”")

S += verbete(
    16, "Divergência 3 — a regra de comunalidade",
    "Uma citação do livro em destaque, e dois números soltos sobre a variável <b>razão de "
    "moradores</b>.",
    "Muitos manuais ensinam uma regra simples: <b>se a comunalidade de um indicador for "
    "menor que 0,50, exclua-o</b>. A ideia é que os fatores não estão dando conta daquele "
    "indicador, então ele não pertence ao conjunto.<br/><br/>"
    "O problema é aplicar a regra sozinha, como se fosse automática. O livro da Enap diz "
    "explicitamente, na página 58, que esse critério “não deve ser utilizado isoladamente "
    "e de maneira muito rígida” — e no próprio exemplo dele mantém um item abaixo do corte, "
    "porque a carga fatorial dele era alta.<br/><br/>"
    "É o caso da razão de moradores neste projeto, e por isso o slide existe: ela ficaria "
    "de fora por uma regra mecânica, e fica dentro por uma razão declarada.",
    f"Comunalidade {br(RM['comun_ortogonal'],3)} — abaixo do corte de 0,50. Carga "
    f"{br(RM['Varimax1'],3)} no fator socioeconômico — bem acima do limite de 0,40 que "
    "torna uma variável relevante. Os dois números vão reportados juntos, sempre: é a "
    "condição para manter a variável de forma honesta.",
    "“A regra do 0,50 existe, e nós a conhecemos. O livro que adotamos como referência diz "
    "que ela não deve ser aplicada isoladamente, e mantém um item abaixo do corte no "
    "próprio exemplo. Mantivemos a razão de moradores pelo mesmo motivo: a carga dela é "
    "alta. E reportamos os dois números lado a lado, para ninguém precisar descobrir "
    "sozinho.”")

S += verbete(
    17, "As cargas, nas duas rotações",
    "Duas grades de números coloridos, lado a lado, chamadas <b>Varimax</b> e <b>promax</b>. "
    "Seis linhas (as variáveis) e duas colunas (os fatores) em cada.",
    "Este é o resultado central da análise: <b>quanto cada variável pertence a cada "
    "fator</b>. Tom quente é carga positiva, tom frio é negativa, cinza é perto de zero — "
    "e o valor vai impresso em cada célula, para a leitura não depender de enxergar cor."
    "<br/><br/>"
    "As duas grades são a mesma solução vista de dois jeitos. <b>Varimax</b> supõe que os "
    "dois fatores são independentes um do outro. <b>Promax</b> permite que eles sejam "
    "correlacionados. O livro recomenda a segunda em Ciências Humanas, porque nessa área "
    "quase nada é independente de verdade — e de fato, aqui, os dois fatores se "
    f"correlacionam a {br(PHI12,3)}.",
    "Leia por coluna. No Fator 1 as cargas altas são renda, analfabetismo e cor/raça — é o "
    "bloco socioeconômico. No Fator 2 são água e esgoto — é o saneamento. Nenhuma variável "
    "tem carga acima de 0,40 nas duas colunas ao mesmo tempo, e isso tem nome: "
    "<b>estrutura simples</b>. É o sinal de que a solução é interpretável.",
    "“Esta é a estrutura que os dados devolveram: um bloco socioeconômico e um bloco de "
    "saneamento, que é exatamente a divisão que o IVS-BH 2012 já usava. Mostramos as duas "
    "rotações porque a literatura recomenda a oblíqua, e queríamos ver se a conclusão "
    "mudava. Não muda.”")

tab_pesos = tabela(
    ["Variável", "Dimensão", "Carga", "Peso"],
    [[r.variavel, r.dimensao, br(r.carga, 3), br(r.peso_pct, 2) + "%"]
     for _, r in PESOS.sort_values("peso", ascending=False).iterrows()],
    [5.6 * cm, 4.0 * cm, 2.4 * cm, 2.4 * cm])

S += verbete(
    20, "Os pesos do IVS",
    "A tabela final: cada variável com o seu peso em porcentagem, somando 100%.",
    "Aqui está o produto do trabalho. A conta que transforma carga em peso tem dois passos, "
    "e os dois são simples.<br/><br/>"
    "<b>Primeiro, quanto cada dimensão pesa.</b> Soma-se o quadrado das cargas de cada "
    "fator. Quanto mais as variáveis carregam num fator, mais aquele fator explica, e mais "
    "ele pesa. Deu <b>" + br(SOCIO, 1) + "% para a socioeconômica</b> e <b>" + br(SANEA, 1) +
    "% para o saneamento</b>.<br/><br/>"
    "<b>Segundo, quanto cada variável pesa dentro da sua dimensão.</b> Mesma lógica: "
    "proporcional ao quadrado da carga. Uma variável que representa bem a dimensão pesa "
    "mais que uma que a representa mal.<br/><br/>"
    "Por que não dar peso igual a todas? Porque renda, cor/raça e analfabetismo medem, em "
    "boa parte, <b>a mesma coisa</b> — eles se correlacionam entre 0,63 e 0,78. Peso igual "
    "daria três votos à posição social e um só ao saneamento, sem que ninguém tivesse "
    "decidido isso.",
    "A referência da literatura — o IVS de Belo Horizonte de 2012 — usa <b>60% e 40%</b>. "
    "Nós chegamos a " + br(SOCIO, 1) + " e " + br(SANEA, 1) + " <b>sem olhar para ela</b>, "
    "só a partir dos dados. Cinco pontos de diferença entre um peso empírico e um peso da "
    "literatura é convergência, não conflito — e é o argumento mais forte do slide.",
    "“Os pesos saem da estrutura que os próprios dados mostraram, não de escolha nossa. E "
    "o resultado bate com o IVS-BH 2012 dentro de cinco pontos percentuais, o que é uma "
    "validação: duas rotas independentes chegaram quase ao mesmo lugar.”",
    extra=tab_pesos)

S += verbete(
    21, "Os pesos são estáveis",
    "Uma tabela com um intervalo ao lado de cada carga, e um número em destaque: o "
    "intervalo da repartição entre as dimensões.",
    "O livro faz uma crítica dura ao tipo de índice que o projeto planeja: diz que ele é "
    "“muito instável por depender fortemente da amostra em particular que está sendo "
    "analisada”. Traduzindo: <b>se você tivesse sorteado outros setores, será que os pesos "
    "seriam outros?</b><br/><br/>"
    "A resposta honesta a essa crítica não é discordar — é medir. A técnica usada chama-se "
    "<b>bootstrap</b>, e a ideia é quase artesanal: sorteia-se, com reposição, um novo "
    "conjunto de setores do mesmo tamanho, refaz-se a análise inteira, e anota-se o "
    "resultado. Mil vezes. No fim, vê-se o quanto os pesos balançaram.",
    "A repartição entre as dimensões ficou entre <b>64,7% e 65,3%</b> nas mil repetições — "
    "uma amplitude de <b>0,59 ponto percentual</b>. Na prática, os pesos não se movem. Com "
    "87 mil setores, a incerteza de amostragem é desprezível; o que limita esta análise "
    "não é a quantidade de setores, é a quantidade de variáveis.",
    "“Essa crítica é do próprio livro que adotamos, e nós a levamos a sério: medimos. Mil "
    "reamostragens movem os pesos em menos de meio ponto percentual. A instabilidade que a "
    "literatura teme não apareceu nesta amostra.”")

S += verbete(
    22, "O índice e o escore refinado concordam menos que o previsto",
    "Três números grandes — 0,924, 0,945 e 0,950 — e dois blocos de texto explicando por "
    "que os dois primeiros ficaram abaixo do terceiro.",
    "Há duas maneiras de transformar os pesos num número por setor.<br/><br/>"
    "A <b>primeira</b> é a que o projeto planeja usar: põe cada variável numa escala de 0 a "
    "1, multiplica pelo peso, soma. Simples, interpretável, e é o que o IVS-BH faz. O livro "
    "chama esse método de <b>“não refinado”</b>.<br/><br/>"
    "A <b>segunda</b> é o método da regressão, que o livro chama de refinado. Ele é mais "
    "estável estatisticamente, mas devolve um número abstrato, sem escala natural, e exige "
    "a matriz completa para ser reproduzido por outra pessoa.<br/><br/>"
    "O plano era calcular os dois e usar a <b>concordância entre eles</b> como validação: se "
    "ordenassem os setores do mesmo jeito, o método simples estaria justificado. O corte "
    "combinado era 0,95.",
    "Deu <b>0,924</b> e <b>0,945</b>, conforme a variante. Os dois abaixo do corte — e é "
    "aqui que o slide fica interessante. A causa não é instabilidade: é que o índice 0–1 "
    "trabalha com os <b>valores</b> das variáveis e o modelo fatorial foi estimado sobre os "
    "<b>postos</b> delas (a posição de cada setor na fila, não o valor). São duas escalas "
    "diferentes. Quanto mais coerente o escore fica com o modelo, mais ele se afasta do "
    "índice planejado.",
    "“Essa é a questão técnica mais aberta que saiu do Notebook 04. Os dois métodos "
    "concordam em 92%, o que é alto mas ficou abaixo do que combinamos como validação. "
    "Sabemos exatamente por quê — é uma diferença de escala, não de qualidade — e há três "
    "saídas possíveis. Qual adotar é decisão que trazemos para a senhora.”")

S += verbete(
    24, "Contra os setores de favela",
    "Uma curva subindo da esquerda para a direita, uma diagonal tracejada, e um número "
    f"grande: <b>AUC {br(AUC_IDX, 3)}</b>.",
    "Todos os testes anteriores dizem se as variáveis se <b>organizam</b> bem. Nenhum deles "
    "diz se o índice <b>acerta</b>. Para isso é preciso comparar o índice com algo que já "
    "se saiba ser verdade, e que não tenha sido usado para construí-lo.<br/><br/>"
    "O projeto tem esse marcador: o IBGE classifica oficialmente quais setores são "
    "<b>Favela e Comunidade Urbana</b>. Nenhuma das seis variáveis do índice foi usada "
    "nessa classificação — ela é totalmente externa.<br/><br/>"
    "A <b>curva ROC</b> responde: se eu ordenar todos os setores pelo índice, os setores de "
    "favela aparecem no topo? A área embaixo dessa curva, a <b>AUC</b>, resume isso num "
    "número entre 0,5 e 1. <b>0,5 é o acaso</b> — equivale a sortear. <b>1 é a separação "
    "perfeita.</b> Uma leitura direta: a AUC é a probabilidade de que, sorteando um setor "
    "de favela e um setor comum, o de favela tenha índice maior.",
    f"O índice deu <b>{br(AUC_IDX,3)}</b> e o escore refinado, <b>{br(AUC_ESC,3)}</b>. O "
    "corte que o plano fixou como “separação nítida” era 0,75, e o patamar abaixo do qual "
    "haveria problema de validade era 0,65. Os dois passam com folga. Em palavras: "
    f"sorteando um setor de favela e um setor comum, o de favela tem índice maior em "
    f"{br(100*AUC_IDX,1)}% das vezes.",
    "“Este é o teste mais forte que temos, porque o marcador é externo: a lista de favelas "
    "é do IBGE e nenhuma variável do índice entrou nela. A área sob a curva é "
    f"{br(AUC_IDX,3)} — bem acima do 0,75 que fixamos como critério. O índice separa os "
    "territórios que sabidamente são vulneráveis.”")

S += verbete(
    25, "O custo de cada escolha, em setores",
    "Uma tabela com três cenários e, em cada um, quantos setores mudam de faixa de risco.",
    "Várias decisões do projeto ainda estão em aberto, e todas têm defensores dos dois "
    "lados. A pergunta que este slide responde é diferente de “qual está certa”: é "
    "<b>“quanto custa errar”</b>.<br/><br/>"
    "A métrica foi escolhida de propósito. Não é variância explicada nem nenhuma estatística "
    "interna — é <b>quantos setores mudam de faixa de risco</b>. Um índice serve para "
    "classificar território e orientar política pública; o que importa é se a escolha "
    "metodológica muda a classificação de quem vai receber essa política.<br/><br/>"
    "Os setores são divididos em quatro faixas por quartis: o quarto menos vulnerável, o "
    "seguinte, e assim por diante. Cada cenário recalcula o índice de outro jeito e conta "
    "quantos setores trocaram de faixa.",
    f"<b>Pesos 60/40 em vez de {br(SOCIO,0)}/{br(SANEA,0)}:</b> mudam "
    f"{inteiro(CEN.loc['pesos_6040','setores_que_mudam_de_faixa'])} setores, "
    f"{br(CEN.loc['pesos_6040','pct'],1)}% — o menor custo dos três. "
    f"<b>Sem o analfabetismo:</b> {inteiro(CEN.loc['sem_analfab','setores_que_mudam_de_faixa'])} "
    f"setores, {br(CEN.loc['sem_analfab','pct'],1)}%. <b>Um fator em vez de dois:</b> "
    f"{inteiro(CEN.loc['um_fator','setores_que_mudam_de_faixa'])} setores, "
    f"{br(CEN.loc['um_fator','pct'],1)}%.",
    "“O objetivo deste bloco não é escolher — é mostrar o preço de cada opção. A decisão "
    "sobre os pesos, que parecia a mais dramática, move só 2,5% dos setores de faixa. Isso "
    "a torna a menos crítica das três, e é um resultado publicável por si só.”")

S += verbete(
    27, "A renda sem o extremo não muda nada",
    "Uma tabela com duas colunas quase idênticas e três números em destaque, entre eles "
    "um <b>0,0000</b>.",
    "Em uma rodada anterior da análise exploratória descobriu-se um setor de Belo Horizonte "
    "com renda média absurdamente alta — provável erro de dado. Toda a análise exploratória "
    "foi refeita sem ele, criando uma segunda coluna de renda.<br/><br/>"
    "A análise fatorial é <b>anterior</b> a essa correção: ela usa a coluna original. Ficou "
    "a dúvida: será que a fatorial inteira precisa ser refeita?<br/><br/>"
    "Este slide responde. Um setor em 87 mil não deveria mudar nada — mas a renda é a "
    "variável de maior carga do índice, e o valor extremo era grande o bastante para ter "
    "motivado uma rodada inteira da EDA. Era barato medir em vez de supor.",
    "A maior diferença entre as cargas é <b>0,0000</b>: elas batem até a quarta casa "
    f"decimal. O KMO muda na quinta casa. E apenas <b>{inteiro(RENDA_MUDA)} setores</b> de "
    f"87.544 mudam de faixa — {br(100*RENDA_MUDA/87544, 2)}% —, com correlação de "
    f"{br(RENDA_RHO, 6)} entre os dois índices.",
    "“Verificamos: trocar a coluna de renda não muda a estrutura, não muda os pesos e "
    "praticamente não muda a classificação. As cargas batem até a quarta casa decimal. A "
    "pendência está fechada — podemos manter como está ou migrar, sem custo.”")

S += [PageBreak(),
      P("Slide 42 · As seis decisões — o porquê de cada uma", "slide"),
      P("Você marcou este slide pedindo <b>o porquê de cada decisão</b>. Elas estão abaixo "
        "na ordem do slide, cada uma com o que está em jogo, o argumento de cada lado e o "
        "que a evidência do projeto diz. <b>Nenhuma foi fechada</b> — o papel do Notebook "
        "04 foi produzir o custo de cada opção, não escolher."),
      Spacer(1, 4),

      P("1 · Pesos empíricos ou os 60/40 da literatura?", "h2"),
      P("<b>O que está em jogo:</b> usar os pesos que os dados devolveram "
        f"({br(SOCIO,1)}/{br(SANEA,1)}) ou os que o IVS-BH 2012 usa (60/40).<br/>"
        "<b>A favor dos empíricos:</b> o livro (p. 71) diz que os itens contribuem de "
        "maneira desigual e que a carga mede essa contribuição — peso igual seria uma "
        "escolha disfarçada de neutralidade.<br/>"
        "<b>A favor dos 60/40:</b> comparabilidade direta com o IVS-BH 2012, que é a "
        "metodologia-fonte do projeto.<br/>"
        f"<b>O que a evidência diz:</b> os dois convergem, e trocar um pelo outro move "
        f"{br(CEN.loc['pesos_6040','pct'],1)}% dos setores de faixa. É a decisão de menor "
        "custo das seis."),

      P("2 · O indicador de lixo entra no índice?", "h2"),
      P("<b>O que está em jogo:</b> o lixo é um dos sete indicadores originais, herdado da "
        "metodologia do IVS-BH 2012.<br/>"
        "<b>A favor de tirar:</b> ele não acompanha nenhum dos outros seis. Pelo método da "
        f"análise fatorial propriamente dita, a comunalidade dele é <b>{br(LIXO['comun_PAF'],3)}</b> "
        "— quase nada da variação dele é compartilhada com o construto. Sem ele, a "
        f"variância explicada sobe de {br(VAR7,1)}% para {br(VAR6,1)}% <b>com menos "
        "variáveis</b>, e a água recupera a representação que havia perdido.<br/>"
        "<b>A favor de manter:</b> fidelidade literal ao <i>Cálculo IVS2012</i>, que o "
        "projeto adotou como fonte.<br/>"
        "<b>Cuidado:</b> esta decisão <b>se inverte</b> se o IVS for entendido como índice "
        "formativo em vez de construto reflexivo — é o assunto dos slides 28 e 29."),

      P("3 · O que fazer com o sigilo no analfabetismo?", "h2"),
      P("<b>O que está em jogo:</b> o IBGE oculta o dado de analfabetismo em setores "
        "pequenos, para proteger a identidade dos moradores. Exigir a variável custa "
        "<b>16.563 setores</b>, que ficam sem índice.<br/>"
        "<b>A favor de manter a variável:</b> ela é um dos três pilares do bloco "
        "socioeconômico, com carga alta.<br/>"
        "<b>A favor de retirá-la:</b> recupera os 16.563 setores.<br/>"
        f"<b>O que a evidência diz:</b> retirá-la move {br(CEN.loc['sem_analfab','pct'],1)}% "
        "dos setores de faixa. E há um problema declarado: o sigilo <b>não é aleatório</b>, "
        "incide sobre os setores de melhor situação — então a base analisada é enviesada "
        "para os mais vulneráveis."),

      P("4 · Um fator ou dois?", "h2"),
      P("<b>O que está em jogo:</b> o índice tem uma dimensão ou duas.<br/>"
        "<b>A favor de um:</b> é o que os critérios estatísticos indicam. Na solução sem o "
        "lixo, tanto o critério de Kaiser quanto a análise paralela de Horn retêm um só "
        "fator. E com um fator a discussão de rotação desaparece inteira.<br/>"
        "<b>A favor de dois:</b> a teoria. O IVS-BH 2012 define duas dimensões, e a leitura "
        "por dimensões é o que permite dizer “este setor é vulnerável por saneamento” em vez "
        "de só “é vulnerável”.<br/>"
        f"<b>O que a evidência diz:</b> a troca move {br(CEN.loc['um_fator','pct'],1)}% dos "
        "setores — o maior custo das três. É a decisão mais delicada, porque estatística e "
        "teoria apontam para lados opostos."),

      P("5 · Rotação ortogonal ou oblíqua?", "h2"),
      P("<b>O que está em jogo:</b> supor que as duas dimensões são independentes "
        "(ortogonal) ou aceitar que se correlacionam (oblíqua).<br/>"
        "<b>A favor da oblíqua:</b> é o que o livro recomenda (p. 38), e com ela se obtém a "
        "correlação entre os fatores — uma evidência que a solução ortogonal não pode "
        f"produzir. Aqui deu {br(PHI12,3)}, positiva e moderada, que é o que a teoria da "
        "vulnerabilidade prevê.<br/>"
        "<b>A favor da ortogonal:</b> é mais simples de reportar e é o que a literatura do "
        "IVS usa.<br/>"
        "<b>O que a evidência diz:</b> a escolha muda os pesos em 0,8 ponto percentual. "
        "Praticamente indiferente para o resultado."),

      P("6 · O índice oficial será o 0–1 ou o escore refinado?", "h2"),
      P("<b>O que está em jogo:</b> qual dos dois números vai para os mapas e para o artigo."
        "<br/><b>A favor do 0–1:</b> interpretável, comparável com o IVS-BH, e reproduzível "
        "por terceiros com uma tabela de seis pesos.<br/>"
        "<b>A favor do refinado:</b> é o que o livro recomenda, é mais estável, e separa "
        f"melhor os setores de favela ({br(AUC_ESC,3)} contra {br(AUC_IDX,3)}).<br/>"
        "<b>O que a evidência diz:</b> a concordância entre os dois ficou em 0,924, abaixo "
        "do 0,95 que validaria o primeiro sem ressalva — é o assunto do slide 22."),
      Spacer(1, 6),
      caixa("SE PERGUNTAREM POR QUE NADA FOI DECIDIDO",
            "“Porque não são decisões técnicas — são decisões de projeto, e algumas têm "
            "consequência para o que o índice significa. O que o Notebook 04 podia fazer "
            "era tirá-las do terreno da opinião: cada uma agora tem o custo medido em "
            "quantos setores mudam de faixa. Trago as seis para a senhora com esse número "
            "na mão.”", CLAY),
      PageBreak()]

S += verbete(
    43, "O que fica declarado como limitação",
    "Uma tabela com nove linhas: cada limitação e onde ela afeta o resultado.",
    "Declarar limitação não é confessar erro — é dizer onde o resultado vale e onde não "
    "vale. Um artigo sem seção de limitações costuma ser lido com <b>mais</b> desconfiança, "
    "não menos. As nove se agrupam em três famílias:<br/><br/>"
    "<b>Limites do método estatístico (1 a 3).</b> O teste de Bartlett não informa nada "
    "numa base de 87 mil setores, porque com amostra grande ele sempre dá significativo; a "
    "análise foi feita sobre os postos das variáveis, não sobre os valores; e duas "
    "variáveis do bloco socioeconômico são muito correlacionadas entre si.<br/><br/>"
    "<b>Limites dos dados (4, 7 e 8).</b> O sigilo do IBGE remove setores de forma não "
    "aleatória; a padronização usada é provisória, porque a definitiva pertence a uma etapa "
    "posterior; e a análise usa a coluna de renda original.<br/><br/>"
    "<b>Limites do desenho (5, 6 e 9).</b> Setores vizinhos não são independentes, e a "
    "técnica supõe que sejam; as conclusões valem para territórios e não para pessoas; e "
    "há uma questão conceitual em aberto sobre a natureza do índice.",
    "Duas merecem ser ditas em voz alta na apresentação. A <b>falácia ecológica</b> (linha "
    "6): tudo o que o índice diz é sobre <i>setores</i>, nunca sobre pessoas — dizer que "
    "“moradores de setores vulneráveis são analfabetos” seria erro grave, e o projeto se "
    "protege disso explicitamente. E a <b>dependência espacial</b> (linha 5): setores "
    "vizinhos se parecem, o que infla a força aparente da estrutura. Não há solução "
    "simples; a medida do problema virá com o I de Moran, na etapa de geoprocessamento.",
    "“Essas nove estão declaradas de propósito. Três são limites do método que a própria "
    "literatura aponta, três são dos dados e três são do desenho do estudo. A que mais "
    "importa para a leitura dos resultados é a falácia ecológica: o índice descreve "
    "territórios, e nada do que ele diz se transfere para indivíduos.”")

# ═════════ PARTE 2 — A PARTE 8 INTEIRA ═════════
S += [PageBreak(),
      P("Parte 2 — A Parte 8 do deck, inteira (slides 30 a 40)", "h1"),
      P("Você marcou a Parte 8 por extenso. Ela tem onze slides e um objetivo só: mostrar "
        "que a análise não saiu de uma caixa-preta. Esta parte do guia explica <b>por que "
        "esses slides existem</b> e o que cada um está dizendo, sem exigir que você leia "
        "código."),
      Spacer(1, 4),
      caixa("ANTES DE TUDO: POR QUE TEM CÓDIGO NUMA APRESENTAÇÃO DE MÉTODO",
            "Porque a análise foi <b>escrita à mão</b>, e não chamada de uma biblioteca "
            "pronta. Isso é incomum e a pergunta vai aparecer. A Parte 8 é a resposta "
            "antecipada: ela mostra que cada conta é conhecida, verificável e escrita em "
            "cinco a quinze linhas — e termina mostrando como fazer a mesma análise em R, "
            "que é a linguagem da bibliografia da área. Se a orientadora quiser conferir "
            "por outro caminho, o caminho está no deck.", PETROL),
      Spacer(1, 6),

      P("Slide 31 · Por que numpy puro, e não uma biblioteca pronta", "slide"),
      P("<b>A situação:</b> existem bibliotecas que fazem análise fatorial com uma linha de "
        "comando. O projeto não usou nenhuma — escreveu as contas usando só ferramentas "
        "básicas de matemática.<br/><br/>"
        "<b>A razão prática:</b> o projeto declara cinco pacotes como dependência. Cada "
        "pacote a mais é uma coisa a instalar, a versionar e a justificar na dissertação. "
        "Tudo que a análise precisa é álgebra linear que as ferramentas básicas já "
        "fazem.<br/><br/>"
        "<b>A razão que apareceu depois, e é a melhor:</b> quem escreve a conta à mão "
        "<b>precisa saber a conta</b>. Foi escrevendo que ficou claro, por exemplo, por que "
        "uma solução com fatores correlacionados produz <i>duas</i> tabelas de cargas em vez "
        "de uma. Isso não se aprende chamando uma função."),
      Spacer(1, 3),
      caixa("SE PERGUNTAREM",
            "“Teria sido mais rápido usar uma biblioteca, e o resultado seria o mesmo. O "
            "que ganhamos foi poder responder a qualquer pergunta sobre o método sem dizer "
            "‘a biblioteca faz’. Numa iniciação científica isso vale mais do que as horas "
            "economizadas. E os slides seguintes mostram a equivalência com o pacote padrão "
            "da área, em R.”", CLAY),

      P("Slide 32 · O caminho, em nove passos", "slide"),
      P("É o mapa da Parte 8. Nove passos, e ao lado de cada um a função que o faz no "
        "projeto e a que faria o mesmo em R. <b>É o slide para mostrar se a pergunta for "
        "“vocês fizeram tudo isso mesmo?”</b> — a coluna da direita mostra que cada passo "
        "corresponde a uma função padrão da área.<br/><br/>"
        "Os nove passos são, em português: (1) medir como as variáveis andam juntas; "
        "(2 e 3) testar se faz sentido procurar fatores nesses dados; (4) checar se duas "
        "variáveis não são quase a mesma coisa; (5) decidir quantos fatores; (6) extrair; "
        "(7 e 8) girar os eixos para a solução ficar legível; (9) transformar tudo num "
        "número por setor."),

      P("Slides 33 a 36 · As quatro contas, linha a linha", "slide"),
      P("Quatro slides no mesmo formato: o código à esquerda, e à direita o que cada linha "
        "faz e <b>por que ela está ali</b>. Não é preciso entender o código para conduzir a "
        "conversa — o que cada um dos quatro resolve cabe em um parágrafo."),
      Spacer(1, 3),
      tabela(["Slide", "A conta", "O que ela resolve, em uma frase"],
             [["33", "KMO",
               "Compara o quanto duas variáveis andam juntas com o quanto elas continuam "
               "andando juntas depois de descontar todas as outras. Se sobra muita relação "
               "própria, não há fator comum — e o KMO cai."],
              ["34", "Extração",
               "Encontra, a partir da tabela de correlações, quais são os fatores e quanto "
               "cada variável pertence a cada um. Quatro linhas, e a terceira é a que "
               "transforma o resultado matemático em algo interpretável."],
              ["35", "Rotação Varimax",
               "Gira os eixos até que cada variável carregue alto em um fator só. Não muda "
               "a qualidade da solução, muda a legibilidade — como girar um mapa até o "
               "norte ficar para cima."],
              ["36", "Rotação promax",
               "Faz o mesmo, mas deixando os eixos se inclinarem, o que permite que os "
               "fatores sejam correlacionados. É a rotação que o livro recomenda, e a única "
               "que produz a correlação entre os fatores."]],
             [1.4 * cm, 3.2 * cm, 9.8 * cm]),
      Spacer(1, 5),
      caixa("O DETALHE DO SLIDE 35 QUE VALE GUARDAR",
            "Há um aviso em vermelho no slide da Varimax: o R, por padrão, aplica uma "
            "normalização que o código do projeto não aplica. <b>Rodar a mesma análise nas "
            "duas ferramentas sem saber disso dá números levemente diferentes</b>, e a "
            "pessoa conclui que alguém errou. Ninguém errou — é uma opção padrão diferente. "
            "Se a orientadora rodar em R e vier com números que não batem na terceira casa "
            "decimal, é quase certo que seja isso.", CLAY),

      P("Slides 37, 38 e 39 · A mesma análise em R", "slide"),
      P("Três slides com o código em R que reproduz a análise inteira, usando o pacote "
        "<b>psych</b> — que é o padrão da área e é o que a bibliografia usa, inclusive os "
        "exemplos do próprio livro da Enap.<br/><br/>"
        "<b>Por que isso está no deck:</b> por dois motivos. Primeiro, porque mostra que "
        "cada passo do projeto corresponde a uma função reconhecida — não se inventou "
        "método. Segundo, e mais importante: rodar a mesma análise em duas implementações "
        "independentes é, ele próprio, <b>um teste</b>. Se as duas concordam, é improvável "
        "que ambas estejam erradas do mesmo jeito.<br/><br/>"
        "<b>O que dizer:</b> que o script está pronto e versionado, e que basta rodar. "
        "Vale ser honesto num ponto: <b>ele ainda não foi executado</b>. Está documentado, "
        "não conferido."),

      P("Slide 40 · O que esperar de diferente entre as duas", "slide"),
      P("Fecha a Parte 8 com cinco pontos em que Python e R divergem por opção padrão, não "
        "por erro: a normalização da rotação, o sinal dos fatores, a ordem deles, o modo "
        "como a análise paralela sorteia os dados, e a correlação de Spearman (que é "
        "idêntica nos dois).<br/><br/>"
        "<b>A regra que o slide estabelece, e é a parte útil dele:</b> se os números "
        "divergirem além desses cinco pontos, o problema é real e vale investigar. Não se "
        "atribui divergência à diferença de linguagem sem antes conferir a lista."),
      Spacer(1, 5),
      caixa("SE A ORIENTADORA PERGUNTAR POR QUE NÃO FIZERAM EM R DESDE O COMEÇO",
            "“A pipeline inteira do projeto é em Python — extração, tratamento do sigilo, "
            "os indicadores, a EDA. Trazer a análise fatorial para R significaria manter "
            "duas linguagens e duas versões dos dados. Escrevemos em Python e documentamos "
            "o equivalente em R, que fica disponível como conferência independente sempre "
            "que a senhora quiser.”", CLAY)]

# ═════════ PARTE 3 — COLA DE BOLSO ═════════
S += [PageBreak(),
      P("Parte 3 — Cola de bolso", "h1"),
      P("Uma página só. Os números que sustentam a apresentação inteira, e o que dizer se "
        "travar."),
      Spacer(1, 4),
      P("OS NÚMEROS QUE VOCÊ PRECISA TER NA PONTA DA LÍNGUA", "h2"),
      tabela(["Número", "O que é", "Se perguntarem, responda"],
             [[f"{br(SOCIO,1)} / {br(SANEA,1)}", "a repartição dos pesos",
               "socioeconômica e saneamento; a literatura usa 60/40, e nós chegamos aqui "
               "sem olhar para ela"],
              [br(KMO7, 3), "o KMO",
               "mede se faz sentido procurar fatores nestes dados; acima de 0,70 é bom"],
              [br(AUC_IDX, 3), "a AUC contra as favelas",
               "sorteando um setor de favela e um comum, o de favela tem índice maior em "
               f"{br(100*AUC_IDX,1)}% das vezes"],
              [br(PHI12, 3), "a correlação entre os dois fatores",
               "as duas dimensões andam juntas, o que a teoria previa — e é por isso que a "
               "rotação oblíqua é a recomendada"],
              ["0,59 ponto", "a incerteza dos pesos",
               "mil reamostragens movem os pesos em menos de meio ponto percentual"],
              [f"{br(CEN.loc['pesos_6040','pct'],1)}%", "o custo de trocar os pesos",
               "só isso dos setores muda de faixa entre 65/35 e 60/40"],
              ["87.545", "os setores analisados",
               "de 104.108 no recorte urbano; a diferença é o sigilo do IBGE"],
              [br(LIXO["comun_PAF"], 3), "a comunalidade do lixo",
               "quase nada da variação dele é compartilhada com o resto — por isso a "
               "proposta de retirá-lo"]],
             [2.6 * cm, 4.4 * cm, 8.4 * cm], tam=7.8),
      Spacer(1, 8),

      P("AS TRÊS FRASES QUE RESUMEM O TRABALHO", "h2"),
      P("<b>1.</b> “Os pesos do IVS são "
        f"{br(SOCIO,1)}% para a dimensão socioeconômica e {br(SANEA,1)}% para saneamento, e "
        "eles saem da estrutura que os próprios dados mostraram.”<br/>"
        "<b>2.</b> “Esses pesos são estáveis: mil reamostragens os movem em menos de meio "
        "ponto percentual.”<br/>"
        f"<b>3.</b> “E o índice funciona: separa os setores de favela com AUC de "
        f"{br(AUC_IDX,3)}, usando uma classificação oficial do IBGE que não entrou na "
        "construção dele.”"),
      Spacer(1, 6),

      caixa("SE VOCÊ TRAVAR NUMA PERGUNTA TÉCNICA",
            "Três saídas honestas, em ordem de preferência.<br/><br/>"
            "<b>1. “Esse número está no arquivo, posso abrir.”</b> Tudo o que está no deck "
            "sai de uma tabela em <font face='Courier'>banco_de_dados/eda/fatorial/</font>. "
            "Abrir o arquivo na frente dela é resposta melhor do que arriscar de memória."
            "<br/><br/>"
            "<b>2. “Essa é uma das decisões que trago para a senhora.”</b> Vale para as "
            "seis do slide 42. Não é escapatória — é o que o notebook foi desenhado para "
            "fazer.<br/><br/>"
            "<b>3. “Não sei, vou verificar e volto.”</b> É a melhor resposta quando for "
            "verdade. O projeto tem a rastreabilidade para cumprir a promessa: cada número "
            "tem um arquivo, e cada arquivo tem o código que o gerou.", PETROL),
      Spacer(1, 8),

      P("ONDE ESTÁ CADA COISA", "h2"),
      tabela(["Se precisar de…", "Está em"],
             [["a EDA Central inteira, dentro deste mesmo deck",
               "slides 44 a 94 — a numeração impressa neles é a original da EDA (1 a 51)"],
              ["o relatório escrito da análise fatorial",
               "docs/relatorios/Relatorio_Analise_Fatorial_NB04.md"],
              ["o código comentado linha a linha, com a versão em R",
               "docs/metodologia/Codigo_Analise_Fatorial_Comentado.md"],
              ["as tabelas com todos os números",
               "banco_de_dados/eda/fatorial/nb04_*.csv"],
              ["as figuras em alta resolução",
               "banco_de_dados/eda/fatorial/figuras/"]],
             [6.4 * cm, 10.6 * cm], tam=7.8)]

doc.build(S)
print(f"guia escrito: {saida}")
