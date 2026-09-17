"""Gera o plano de emergência para a apresentação: o livro condensado + o roteiro + o Q&A.

Para que serve
--------------
É o documento para quem não vai conseguir terminar de ler o livro antes da reunião. Ele
faz três coisas que o Guia de Apoio não faz:

  1. condensa o livro da Enap no que sustenta a apresentação, com a página de cada
     passagem citável — para poder dizer "está na página tal" sem blefe;
  2. dá o roteiro da fala, bloco a bloco, com o que dizer e o que apontar;
  3. antecipa as perguntas prováveis com a resposta pronta e o número que a sustenta.

O Guia de Apoio (Guia_Apoio_Analise_Fatorial.pdf) explica os slides marcados. Este aqui
prepara a apresentação inteira. Os dois se complementam e não se repetem.

Nenhum número é digitado: todos saem de banco_de_dados/eda/fatorial/.

Uso:
    uv run --with reportlab --with pandas python scripts/gerar_pdf_plano_emergencia.py \
        docs/Apresentacoes_IVS/complementos/Plano_Emergencia_Apresentacao.pdf
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
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

RAIZ = Path(__file__).resolve().parents[1]
FAT = RAIZ / "banco_de_dados" / "eda" / "fatorial"

TINTA = colors.HexColor("#1A1A1A")
PETROL = colors.HexColor("#1F4E4A")
CLAY = colors.HexColor("#A83A2C")
CINZA = colors.HexColor("#666666")
LINHA = colors.HexColor("#C8C8C8")
FUNDO = colors.HexColor("#F2F0EC")
SERIF, SERIF_B = "Times-Roman", "Times-Bold"
SANS, SANS_B, MONO = "Helvetica", "Helvetica-Bold", "Courier"

ler = lambda n: pd.read_csv(FAT / n, sep=";", encoding="utf-8-sig")
RES = ler("resumo_adequabilidade.csv").set_index("nome")
PESOS = ler("nb04_sintese_pesos.csv")
CEN = ler("nb04_cenarios.csv").set_index("cenario")
VAL = ler("nb04_validacao_fcu.csv")
PHI = ler("nb04_phi_ivs6_sem_lixo.csv")
CARG = ler("nb04_cargas_ivs6_sem_lixo.csv").set_index("variavel")
EXTR = ler("nb04_extracao_comparada.csv")
AUTOV = ler("nb04_autovalores.csv")
RENDA = ler("nb04_renda_sem_extremo.csv").set_index("medida")


def br(x, c=3):
    return f"{x:,.{c}f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def inteiro(x):
    return f"{int(round(x)):,}".replace(",", ".")


SOCIO = 100 * PESOS.loc[PESOS.dimensao == "Socioeconômica", "peso"].sum()
SANEA = 100 * PESOS.loc[PESOS.dimensao == "Saneamento", "peso"].sum()
PHI12 = abs(PHI.iloc[0, 2])
AUC_IDX, AUC_ESC = VAL.auc[0], VAL.auc[1]
KMO7, KMO6 = RES.loc["ivs7_spearman", "kmo"], RES.loc["ivs6_sem_lixo_spearman", "kmo"]
VAR7 = RES.loc["ivs7_spearman", "var_acumulada_k"]
VAR6 = RES.loc["ivs6_sem_lixo_spearman", "var_acumulada_k"]
BART = RES.loc["ivs7_spearman", "bartlett_qui2"]
LIXO = EXTR[(EXTR.cenario == "ivs7_spearman") & (EXTR.variavel == "Lixo inadequado")].iloc[0]
A6 = AUTOV[AUTOV.cenario == "ivs6_sem_lixo_spearman"].reset_index(drop=True)
A7 = AUTOV[AUTOV.cenario == "ivs7_spearman"].reset_index(drop=True)
RM = CARG.loc["Razão de moradores"]
RENDA_MUDA = int(RENDA.loc["setores que mudam de faixa", "com renda_media_sem_extremo"])

E = {
    "capa": ParagraphStyle("capa", fontName=SERIF_B, fontSize=22, leading=26, textColor=TINTA),
    "capasub": ParagraphStyle("capasub", fontName=SANS, fontSize=10.5, leading=15, textColor=CINZA),
    "h1": ParagraphStyle("h1", fontName=SERIF_B, fontSize=15, leading=18, textColor=PETROL,
                         spaceBefore=17, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName=SANS_B, fontSize=9.6, leading=12.6, textColor=PETROL,
                         spaceBefore=10, spaceAfter=2),
    "h3": ParagraphStyle("h3", fontName=SERIF_B, fontSize=11.5, leading=14, textColor=TINTA,
                         spaceBefore=12, spaceAfter=2),
    "p": ParagraphStyle("p", fontName=SANS, fontSize=9.3, leading=13.6, textColor=TINTA,
                        alignment=TA_JUSTIFY, spaceAfter=5),
    "cit": ParagraphStyle("cit", fontName=SERIF, fontSize=9.8, leading=13.6, textColor=TINTA,
                          leftIndent=14, rightIndent=8, spaceBefore=3, spaceAfter=3),
    "fala": ParagraphStyle("fala", fontName=SANS, fontSize=9.1, leading=13.2, textColor=CLAY,
                           leftIndent=10, alignment=TA_JUSTIFY, spaceAfter=5),
}
P = lambda t, e="p": Paragraph(t, E[e])


def tabela(cab, linhas, larg, tam=8.0):
    eh = ParagraphStyle("th", fontName=SANS_B, fontSize=tam, leading=tam + 2.2, textColor=PETROL)
    ec = ParagraphStyle("td", fontName=SANS, fontSize=tam, leading=tam + 2.6, textColor=TINTA)
    d = [[Paragraph(f"<b>{c}</b>", eh) for c in cab]]
    d += [[Paragraph(str(c), ec) for c in ln] for ln in linhas]
    t = Table(d, colWidths=larg, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.35, LINHA), ("BACKGROUND", (0, 0), (-1, 0), FUNDO),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5)]))
    return t


def caixa(titulo, texto, cor=PETROL):
    et = ParagraphStyle("bt", fontName=SANS_B, fontSize=8.9, leading=11.8, textColor=cor)
    ec = ParagraphStyle("bc", fontName=SANS, fontSize=8.7, leading=12.4, textColor=TINTA,
                        alignment=TA_JUSTIFY)
    t = Table([[Paragraph(titulo, et)], [Paragraph(texto, ec)]], colWidths=[17.0 * cm],
              hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), FUNDO), ("LINEBEFORE", (0, 0), (0, -1), 2.2, cor),
        ("TOPPADDING", (0, 0), (-1, 0), 6), ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2)]))
    return t

saida = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    RAIZ / "docs" / "Apresentacoes_IVS" / "complementos" / "Plano_Emergencia_Apresentacao.pdf")
saida.parent.mkdir(parents=True, exist_ok=True)
LARG, ALT = A4
MARG = 2.0 * cm


def rodape(canv, doc):
    canv.saveState()
    canv.setFont(SANS, 7.3); canv.setFillColor(CINZA)
    canv.drawString(MARG, 1.25 * cm, "Plano de emergência · apresentação da análise fatorial")
    canv.drawRightString(LARG - MARG, 1.25 * cm, f"{doc.page}")
    canv.setStrokeColor(LINHA); canv.setLineWidth(0.4)
    canv.line(MARG, 1.62 * cm, LARG - MARG, 1.62 * cm)
    canv.restoreState()


doc = BaseDocTemplate(str(saida), pagesize=A4, leftMargin=MARG, rightMargin=MARG,
                      topMargin=1.8 * cm, bottomMargin=2.1 * cm,
                      title="Plano de emergência — apresentação da análise fatorial",
                      author="Pedro Dias Soares")
doc.addPageTemplates([PageTemplate(id="c", frames=[Frame(MARG, 2.1 * cm, LARG - 2 * MARG,
                                   ALT - 1.8 * cm - 2.1 * cm, id="f")], onPage=rodape)])
S = []

# ═════════ CAPA ═════════
S += [Spacer(1, 1.4 * cm),
      P("Plano de emergência", "capa"),
      P("O livro em oito páginas, o roteiro da fala e as perguntas prováveis", "capa"),
      Spacer(1, 0.45 * cm),
      P("Análise fatorial e os pesos do IVS · Notebook 04<br/>Iniciação Científica · Fiocruz "
        "Minas — Instituto René Rachou · Pedro Dias Soares · setembro de 2026", "capasub"),
      Spacer(1, 0.7 * cm),
      caixa("LEIA ISTO PRIMEIRO",
            "Este documento parte de um pressuposto: <b>não vai dar tempo de terminar o "
            "livro.</b> Ele não tenta resumir as 74 páginas — tenta entregar o que sustenta "
            "<i>esta</i> apresentação, com a página de cada passagem, para você poder dizer "
            "“está na página tal” sem blefar.<br/><br/>"
            "São cinco partes. A <b>1</b> é o livro condensado. A <b>2</b> é o eixo do "
            "deck: os três pontos em que o livro contraria a referência anterior do "
            "projeto. A <b>3</b> é o roteiro da fala. A <b>4</b> são as perguntas prováveis "
            "com resposta pronta. A <b>5</b> é o que cortar se o tempo apertar.<br/><br/>"
            "<b>Se você só tiver uma hora:</b> leia a Parte 2 e a Parte 4. Elas são o que "
            "separa apresentar de ser arguido.", CLAY),
      Spacer(1, 0.4 * cm),
      caixa("E O OUTRO DOCUMENTO",
            "O <i>Guia de Apoio</i> explica, um a um, os slides que você marcou com "
            "“EXPLICAR SLIDE”, e tem o vocabulário do zero na Parte 0. Este aqui prepara a "
            "apresentação inteira. Não se repetem: se a dúvida é <b>“o que este slide quer "
            "dizer”</b>, vá no Guia de Apoio; se é <b>“o que eu falo e o que me perguntam”</b>, "
            "é aqui.", PETROL),
      PageBreak()]

# ═════════ PARTE 1 — O LIVRO ═════════
S += [P("Parte 1 — O livro da Enap, condensado", "h1"),
      P("MATOS, D. A. S.; RODRIGUES, E. C. <b>Análise fatorial</b>. Brasília: Enap, 2019. "
        "74 p. Coleção Metodologias de Pesquisa. É a referência metodológica principal do "
        "projeto, e é curto — 74 páginas, das quais 25 são os dois exemplos aplicados."),

      P("O que o livro é, e o que ele não é", "h2"),
      P("É uma <b>introdução à análise fatorial exploratória</b>, escrita para servidores "
        "públicos e pesquisadores em formação, com exemplos rodados em R. Não é um tratado: "
        "ele próprio diz, na p. 28, que a comparação entre análise fatorial e componentes "
        "principais “é uma questão polêmica na literatura” e que aprofundá-la “foge ao "
        "escopo deste livro”.<br/><br/>"
        "Isso importa para a sua defesa: <b>o livro é a referência do projeto, não a "
        "autoridade final</b>. Onde ele não alcança — e são cinco pontos, listados no fim "
        "desta parte — o projeto teve de buscar outra coisa, e isso é mérito, não falha."),

      P("A espinha dorsal: o livro organiza tudo em dois estágios", "h3"),
      P("Se você memorizar só uma coisa do livro, memorize esta divisão. Ela é a estrutura "
        "das Tabelas 7 (p. 44) e 8 (p. 46), e é a estrutura da sua apresentação."),
      Spacer(1, 3),
      tabela(["Etapa 1 — a base aguenta? (p. 39–44)", "O patamar que o livro fixa"],
             [["Tamanho da amostra", "mais de 100 casos, e pelo menos 5 observações por "
                                     "variável (o ideal seria 10)"],
              ["Nível de mensuração", "definir o tipo de correlação conforme a natureza das "
                                      "variáveis"],
              ["Matriz de correlação", "a maioria dos coeficientes acima de 0,3"],
              ["Teste de Bartlett", "deve ser estatisticamente significante, p &lt; 0,05"],
              ["Teste KMO", "quanto mais perto de 1, melhor; 0,5 é o mínimo aceitável, "
                            "o ideal é a partir de 0,7"]],
             [6.0 * cm, 11.0 * cm], tam=8.0),
      Spacer(1, 6),
      tabela(["Etapa 2 — a análise em si (p. 44–46)", "O que o livro diz"],
             [["Número de fatores", "três critérios — autovalor maior que 1 (Kaiser), o "
                                    "diagrama de inclinação, e 60% de variância acumulada. "
                                    "<b>“Os critérios devem ser usados em conjunto.”</b>"],
              ["Método de extração", "componentes principais, fatores principais, máxima "
                                     "verossimilhança, mínimos quadrados"],
              ["Rotação", "ortogonal (varimax, quartimax…) ou oblíqua (oblimin, promax…)"],
              ["Interpretação", "examinar como as variáveis se agrupam, nomear os fatores e "
                                "justificar teoricamente"]],
             [6.0 * cm, 11.0 * cm], tam=8.0),
      Spacer(1, 7),
      caixa("A FRASE DO LIVRO QUE MAIS PROTEGE O SEU TRABALHO (p. 45)",
            "“Mesmo que você esteja fazendo uma análise fatorial exploratória, <b>não espere "
            "que ela faça milagres. Você deve sempre se valer de teoria e/ou de pesquisas "
            "anteriores.</b> Portanto, mesmo sendo uma técnica exploratória, algum tipo de "
            "hipótese sobre o agrupamento das variáveis sempre deve existir.”<br/><br/>"
            "<b>Por que isso te protege:</b> a decisão mais frágil do projeto é reter dois "
            "fatores quando os critérios estatísticos indicam um. Esta frase, do próprio "
            "livro, diz que decidir por teoria não é desvio — é o procedimento correto.",
            CLAY)]

S += [PageBreak(),
      P("As oito passagens que você pode citar de cabeça", "h3"),
      P("Com a página. São as que o deck usa e as que respondem a perguntas prováveis. "
        "Decorar as páginas vale mais do que decorar as frases: quem sabe a página passa a "
        "impressão de ter lido o livro inteiro."),
      Spacer(1, 3),
      tabela(["Pág.", "O que o livro diz", "Onde isso aparece na sua apresentação"],
             [["18 e 71", "“Os itens contribuem de maneira desigual para o fator: quanto "
                          "maior a carga fatorial, maior a contribuição do item.” E isso "
                          "“não acontece em outras técnicas mais simples de elaboração de "
                          "índices”, que supõem contribuição igual.",
               "<b>É o argumento central a favor dos pesos empíricos.</b> Aparece duas "
               "vezes no livro — na p. 18 e no fecho do Exemplo 2, na p. 71."],
              ["22", "Numa solução oblíqua a carga é coeficiente de regressão e pode passar "
                     "de 1; se passar, confere-se a variância residual — negativa, a "
                     "solução é inadmissível.",
               "O cheque que o slide da rotação promax faz. No projeto a maior carga deu "
                f"{br(CARG[['Padrao1','Padrao2']].abs().to_numpy().max(),3)} e a menor "
                f"variância residual, {br(CARG.var_residual.min(),3)} — positiva."],
              ["26–28", "Regra de Stevens (1992): com <b>menos de 20 variáveis</b> e "
                        "comunalidades baixas, componentes principais e análise fatorial "
                        "podem divergir.",
               "Slide 15. Justifica ter rodado as duas técnicas em vez de supor equivalência."],
              ["29", "O critério de Kaiser funciona melhor <b>entre 20 e 50 variáveis</b>.",
               "Slide 9. É por isso que Kaiser é o critério mais fraco aqui: são 6 ou 7 "
               "variáveis."],
              ["32", "A decisão sobre o número de fatores pode ser teórica; a pergunta certa "
                     "é “teoricamente faz mais sentido essas variáveis estarem agrupadas em "
                     "quantos fatores?”.",
               "Slide 9. <b>É a passagem que legitima reter dois fatores.</b>"],
              ["38", "“Usar rotação ortogonal com dados de Ciências Humanas e Sociais não "
                     "parece ter nenhum sentido. […] para usar rotação ortogonal, o "
                     "pesquisador precisaria ter evidências teóricas ou empíricas muito "
                     "fortes de que os fatores não são correlacionados.”",
               "Slide 14. <b>É a citação mais forte do deck.</b> Inverte o ônus da prova: "
               "ortogonal é que precisa ser justificada."],
              ["42–43", "Correlação acima de <b>0,8</b> indica multicolinearidade. E o teste "
                        "de Bartlett “depende muito do tamanho amostral e tende a rejeitar a "
                        "hipótese nula para amostras grandes”.",
               "Slides 4 e 7. Sustenta a ressalva do Bartlett e a discussão da correlação "
               "renda × cor/raça."],
              ["58", "“O critério da comunalidade maior do que 0,5 não deve ser utilizado "
                     "isoladamente e de maneira muito rígida.”",
               "Slide 16. Autoriza manter a razão de moradores, que tem comunalidade "
                f"{br(RM['comun_ortogonal'],3)} e carga {br(RM['Varimax1'],3)}."]],
             [1.4 * cm, 7.6 * cm, 8.0 * cm], tam=7.7),

      P("O Exemplo 2 do livro (p. 67–71) é o molde do seu caso", "h3"),
      P("Se a orientadora perguntar “em que isso se parece com o que já se faz na "
        "literatura”, este é o exemplo a citar. O livro constrói um <b>indicador de nível "
        "socioeconômico</b> a partir de 13 itens do questionário da Prova Brasil — "
        "televisão, geladeira, carro, computador, escolaridade dos pais —, com 2.497.431 "
        "alunos. Um fator só, 66% da variância explicada, escores calculados pelo método da "
        "regressão e usados depois como variável explicativa num modelo multinível."),
      Spacer(1, 3),
      tabela(["", "Exemplo 2 do livro", "O projeto IVS"],
             [["O que se quer medir", "nível socioeconômico do aluno",
               "vulnerabilidade do setor censitário"],
              ["Unidade", "aluno (pessoa)", "<b>setor censitário (território)</b>"],
              ["Variáveis", "13 itens categóricos", "6 ou 7 proporções contínuas"],
              ["Correlação", "policórica", "Spearman"],
              ["Nº de fatores", "1 — e o livro nota que então a rotação é dispensável",
               "2, o segundo sustentado pela teoria"],
              ["Variância explicada", "66%", f"{br(VAR6,1)}% sem o lixo"],
              ["Uso depois", "preditor num modelo multinível",
               "índice 0–1, quatro faixas, mapas"]],
             [3.6 * cm, 6.4 * cm, 7.0 * cm], tam=7.8),
      Spacer(1, 5),
      caixa("A DIFERENÇA QUE VOCÊ PRECISA DIZER ANTES QUE PERGUNTEM",
            "No Exemplo 2 as unidades são <b>pessoas</b>. No seu projeto são "
            "<b>territórios</b>. Tudo o que o índice diz vale para setores censitários e "
            "nada se transfere para indivíduos — chama-se <b>falácia ecológica</b> e está "
            "declarada nas limitações. Dizer isso você mesmo, antes de ser perguntado, é o "
            "que mostra domínio.", CLAY),

      P("Os cinco pontos em que o livro não alcança o projeto", "h3"),
      P("Esta lista é a sua proteção contra a pergunta “e por que vocês fizeram diferente "
        "do livro?”. Em nenhum destes o livro dá resposta — e o projeto teve de buscar "
        "fora."),
      Spacer(1, 3),
      tabela(["O que falta no livro", "O que o projeto fez"],
             [["<b>A correlação que o projeto usa não está no catálogo dele.</b> O livro "
               "lista Pearson, bisserial, policórica, polisserial e tetracórica — todas "
               "para variáveis categóricas. Spearman não está lá.",
               "Usou Spearman e justificou pela não-normalidade: assimetria de 3,42 na água "
               "e 3,74 na renda. O deck mostra que com Pearson a base <b>reprovaria</b> em "
               "dois critérios da Etapa 1."],
              ["<b>Dados faltantes não aparecem em nenhuma das 74 páginas.</b> Os exemplos "
               "do livro são questionários com resposta completa.",
               "Declarou o problema: 16.563 setores perdidos pelo sigilo do IBGE, e o sigilo "
               "não é aleatório — incide nos setores de melhor situação."],
              ["<b>Dependência espacial.</b> O livro pressupõe unidades independentes, "
               "porque foi escrito para respondentes de questionário.",
               "Declarou como limitação. Setores vizinhos se parecem, o que infla a "
               "estrutura aparente. O I de Moran medirá isso na etapa de geoprocessamento."],
              ["<b>Análise paralela de Horn.</b> Critério moderno para decidir o número de "
               "fatores; não está no livro.",
               "O projeto usa. <b>Está usando um critério melhor que o da própria "
               "referência</b> — vale dizer isso."],
              ["<b>Compor um índice.</b> O livro termina nos escores fatoriais usados como "
               "variável em outro modelo. Não trata de índice 0–1, pesos explícitos, faixas "
               "de risco nem mapas.",
               "É a etapa seguinte, e a referência para ela é outra: o manual da OCDE/JRC "
               "sobre indicadores compostos (Nardo et al., 2008)."]],
             [7.6 * cm, 9.4 * cm], tam=7.8)]

# ═════════ PARTE 2 — O EIXO ═════════
S += [PageBreak(),
      P("Parte 2 — O eixo da apresentação: onde a Enap contraria Figueiredo", "h1"),
      P("O projeto vinha seguindo um artigo de 2010 (Figueiredo Filho &amp; Silva Júnior, "
        "<i>Visão além do alcance</i>). O livro da Enap é posterior, mais rigoroso, e o "
        "contraria em <b>três pontos</b>. Nos três, o livro dá razão ao que os dados do "
        "projeto já indicavam — e é isso que faz a apresentação ter uma história para "
        "contar em vez de ser uma lista de resultados.<br/><br/>"
        "<b>Se você entender só esta página, consegue conduzir a reunião.</b>"),

      P("Divergência 1 — a rotação (slide 14)", "h3"),
      P("<b>Figueiredo usa Varimax</b>, que supõe fatores independentes, e justifica com "
        "“por ser a mais comum”. <b>O livro (p. 38) diz que isso não faz sentido em "
        "Ciências Humanas</b>, onde quase nada é independente, e inverte o ônus da prova: "
        "quem usa ortogonal é que precisa provar a independência.<br/>"
        f"<b>O que os dados disseram:</b> os dois fatores se correlacionam a {br(PHI12,3)}. "
        "Não são independentes. A rotação oblíqua, além disso, produz um objeto que a "
        "ortogonal não pode produzir — a própria correlação entre os fatores —, e o valor "
        "encontrado é positivo e moderado, que é exatamente o que a teoria da "
        "vulnerabilidade prevê: território pobre tem pior saneamento."),
      P("Custo de trocar de rotação: <b>0,8 ponto percentual</b> nos pesos. Praticamente "
        "indiferente para o resultado — o que é uma boa notícia, e vale dizer."),

      P("Divergência 2 — a técnica de extração (slide 15)", "h3"),
      P("<b>Figueiredo trata componentes principais e análise fatorial como "
        "intercambiáveis. O livro (p. 26–28) traz a regra de Stevens (1992):</b> abaixo de "
        "20 variáveis e com comunalidades baixas, elas podem divergir.<br/>"
        f"<b>O que os dados disseram:</b> divergem — e divergem onde a teoria mandava "
        f"esperar. A água, que compartilha pouco com as outras, difere "
        f"{br(EXTR[(EXTR.cenario=='ivs6_sem_lixo_spearman')&(EXTR.variavel=='Água inadequada')].iloc[0]['dif_2'],3)} "
        "entre as duas técnicas; a renda, que compartilha muito, difere "
        f"{br(EXTR[(EXTR.cenario=='ivs6_sem_lixo_spearman')&(EXTR.variavel=='Renda (invertida)')].iloc[0]['dif_2'],3)}."),

      P("Divergência 3 — a regra de comunalidade (slide 16)", "h3"),
      P("<b>Figueiredo trata o corte de 0,50 como teste final de inclusão</b> — abaixo "
        "disso, exclua e rode de novo. <b>O livro (p. 58) diz que o critério “não deve ser "
        "utilizado isoladamente e de maneira muito rígida”</b>, e no próprio exemplo mantém "
        "um item abaixo do corte porque a carga era alta.<br/>"
        f"<b>O que os dados disseram:</b> a razão de moradores tem comunalidade "
        f"{br(RM['comun_ortogonal'],3)} e carga {br(RM['Varimax1'],3)}. Fica no índice, com "
        "os dois números reportados juntos."),
      Spacer(1, 5),
      caixa("O ACHADO QUE É SÓ SEU, E QUE VALE CONTAR",
            "A regra mecânica de comunalidade do artigo de 2010, aplicada sem olhar a "
            "estrutura, teria excluído <b>a água</b> — que é um dos dois pilares do "
            "saneamento. A comunalidade dela era 0,253 na solução de sete variáveis. Mas "
            "ela estava baixa porque o <b>lixo</b> havia monopolizado o segundo fator. "
            "Retirado o lixo, a água sobe para 0,822 e vira a variável de maior carga do "
            "saneamento.<br/><br/>"
            "<b>A lição, e ela é uma crítica ao artigo:</b> a comunalidade não é propriedade "
            "da variável, é propriedade da <i>solução</i>. A ordem correta é diagnosticar a "
            "estrutura, remover o que é externo ao construto, e só então avaliar "
            "comunalidades. Seguir a regra ao pé da letra teria excluído a vítima em vez do "
            "problema.", CLAY),
      Spacer(1, 6),
      P("E o que o livro faz pelo caso do lixo", "h2"),
      P("O exemplo didático do livro (Tabela 1, p. 15) tem sete itens, e o <b>item 7</b> se "
        "correlaciona fracamente com todos os outros — o livro anuncia ali mesmo que ele "
        "provavelmente terá de sair, e no Exemplo 1 ele de fato sai, com a variância "
        "explicada subindo de 53,6% para 58,1%.<br/><br/>"
        f"<b>O seu lixo é o item 7 do livro.</b> Retirado, a variância sobe de "
        f"{br(VAR7,1)}% para {br(VAR6,1)}% <b>com menos variáveis</b> — o mesmo movimento. "
        "A diferença, que enriquece a discussão: no livro o item problemático tem "
        "comunalidade baixa; o seu lixo tem comunalidade <i>alta</i> na ACP (0,859), porque "
        f"formou um fator só dele — e pelo eixo principal cai para {br(LIXO['comun_PAF'],3)}.")]

# ═════════ PARTE 3 — O ROTEIRO ═════════
S += [PageBreak(),
      P("Parte 3 — O roteiro da fala", "h1"),
      P("Dez blocos. A coluna da direita é o que dizer — não para ler, mas para ter na "
        "cabeça a frase que abre cada bloco. Os tempos somam <b>46 minutos</b> sem a Parte "
        "8; com ela, 51."),
      Spacer(1, 4),
      tabela(["Bloco", "Slides", "min", "A frase que abre, e o que apontar"],
             [["<b>1 · Abertura</b>", "1–2", "2",
               "“O Notebook 04 responde uma pergunta só: <b>quanto cada indicador deve "
               "pesar no índice, e por quê.</b> Quatro decisões estavam travadas por falta "
               "dessa resposta.” Aponte a tabela das quatro decisões."],
              ["<b>2 · A base aguenta?</b>", "3–7", "5",
               "“Antes de procurar fatores, é preciso testar se faz sentido procurá-los "
                f"nestes dados.” Vá direto ao KMO de {br(KMO7,3)}. No slide 5, o ponto "
                "forte: <b>com Pearson a base reprovaria</b> — a escolha por Spearman é o "
                "que torna a análise defensável. No 7, adiante o problema da "
                "multicolinearidade antes que perguntem."],
              ["<b>3 · Quantos fatores</b>", "8–10", "4",
               "“Aqui os critérios discordam, e o livro manda usá-los em conjunto "
               "justamente por isso.” Seja honesto: sem o lixo, Kaiser e Horn retêm "
               "<b>um</b>. A retenção do segundo é decisão teórica, e a p. 32 do livro "
               "legitima. Aponte o segundo ponto do scree, abaixo da linha do acaso."],
              ["<b>4 · O caso do lixo</b>", "11–12", "3",
               "“Um dos sete indicadores não pertence ao conjunto, e agora isso está "
                f"medido.” O número que fecha: comunalidade {br(LIXO['comun_PAF'],3)} pelo "
                "eixo principal. Conte o paralelo com o item 7 do livro."],
              ["<b>5 · As três divergências</b>", "13–18", "7",
               "“O projeto seguia um artigo de 2010. O livro que adotamos o contraria em "
               "três pontos, e nos três os dados já apontavam para o mesmo lado.” "
               "<b>É o coração da apresentação.</b> Termine no slide 18, o plano dos "
               "fatores — é a imagem que fixa o argumento do lixo."],
              ["<b>6 · Os pesos</b>", "19–22", "6",
                f"“Os pesos são {br(SOCIO,1)} e {br(SANEA,1)}, e saem da estrutura que os "
                "próprios dados mostraram.” Depois a convergência com o IVS-BH (60/40) "
                "como validação. No 21, a estabilidade. No 22, seja franco: a concordância "
                "entre os dois métodos de escore ficou abaixo do combinado, e sabemos por "
                "quê."],
              ["<b>7 · O índice funciona?</b>", "23–25", "5",
               "“Nenhum teste anterior diz se o índice <i>acerta</i>. Para isso é preciso "
                f"um marcador externo.” AUC {br(AUC_IDX,3)} contra os setores de favela do "
                "IBGE. No 25, o custo de cada escolha em setores — é o slide que mais "
                "impressiona, porque traduz metodologia em política pública."],
              ["<b>8 · As duas em aberto</b>", "26–29", "4",
               "“Duas perguntas sobraram. Uma respondemos rodando; a outra não se responde "
               "com dados.” A renda, em 30 segundos. E então a questão reflexivo × "
               "formativo, que é a mais séria — <b>a decisão sobre o lixo se inverte</b> "
               "conforme a resposta."],
              ["<b>9 · O código</b>", "30–40", "5",
               "<b>Este bloco é cortável.</b> Se o tempo apertar, diga só: “a análise foi "
               "escrita à mão em vez de chamada de uma biblioteca, e os slides 30 a 40 "
               "mostram cada conta e o equivalente em R, caso a senhora queira conferir por "
               "outro caminho”. E siga."],
              ["<b>10 · O que vai para a senhora</b>", "41–43", "5",
               "“Seis decisões, e nenhuma delas é nossa para fechar. O que o notebook fez "
               "foi medir o custo de cada opção.” Termine nas limitações — fechar por elas "
               "passa mais segurança do que fechar por resultados."]],
             [3.4 * cm, 1.5 * cm, 1.0 * cm, 11.1 * cm], tam=7.7),
      Spacer(1, 7),
      caixa("COMO ABRIR E COMO FECHAR",
            "<b>A abertura</b> tem de deixar claro o que este notebook <i>não</i> faz, ou a "
            "expectativa fica errada a reunião inteira: “o produto aqui são os pesos e a "
            "estrutura — o IVS final é o Notebook 05, depois da normalização por "
            "município”.<br/><br/>"
            "<b>O fecho</b>, se a apresentação correu bem, é uma frase só: “as três "
            "perguntas que o notebook precisava responder têm resposta com número: quais "
            "são os pesos e por quê; quanto a classificação é sensível a essa escolha; e se "
            "o índice separa os territórios que sabidamente são vulneráveis”.<br/><br/>"
            "<b>Atenção:</b> o slide que fechava a apresentação foi retirado. Hoje ela "
            "termina nas limitações e emenda direto na EDA Central, que está anexada a "
            "partir do slide 44. Ou você diz a frase de fecho de viva voz, ou avisa que o "
            "que vem a seguir é material de consulta.", CLAY)]

# ═════════ PARTE 4 — AS PERGUNTAS ═════════
S += [PageBreak(),
      P("Parte 4 — As perguntas prováveis, com a resposta", "h1"),
      P("Quinze. As cinco primeiras são quase certas. Cada resposta cabe em vinte segundos "
        "e tem um número atrás dela."),

      P("As que quase certamente virão", "h2"),
      tabela(["A pergunta", "A resposta"],
             [["<b>Por que 65/35 e não 60/40, que é o do IVS-BH?</b>",
                f"“Os {br(SOCIO,1)}/{br(SANEA,1)} saem da estrutura que os dados mostraram, "
                "sem olhar para a literatura. Chegar a cinco pontos do IVS-BH por caminho "
                "independente é validação. E medimos o custo de trocar: "
                f"{br(CEN.loc['pesos_6040','pct'],1)}% dos setores mudam de faixa. Se a "
                "senhora preferir 60/40 pela comparabilidade, sabemos exatamente o que "
                "isso custa.”"],
              ["<b>Vocês vão mesmo tirar o lixo do índice?</b>",
               "“É decisão da senhora, e trago a evidência. Pela análise fatorial "
                f"propriamente dita, a comunalidade dele é {br(LIXO['comun_PAF'],3)} — quase "
                "nada da variação dele é compartilhada com o resto. Sem ele a variância "
                f"explicada sobe de {br(VAR7,1)}% para {br(VAR6,1)}% com <i>menos</i> "
                "variáveis. Mas há uma ressalva conceitual no slide 28 que pode inverter "
                "essa conclusão, e prefiro apresentá-la.”"],
              ["<b>Por que Spearman e não Pearson?</b>",
                "“Pela não-normalidade: assimetria de 3,42 na água e 3,74 na renda, curtose "
                "de 49,5. E o custo da escolha está medido — com Pearson o KMO cai para "
                f"{br(RES.loc['ivs7_pearson','kmo'],3)}, o MSA mínimo para "
                f"{br(RES.loc['ivs7_pearson','msa_min'],3)}, e a base <b>reprovaria</b> em "
                "dois critérios da Etapa 1 do livro.”"],
              ["<b>Dois fatores mesmo? Os critérios não indicam um?</b>",
               "“Indicam um, e isso está no slide com todas as letras. A retenção do "
               "segundo é decisão teórica, e o livro autoriza na página 32: a pergunta "
               "certa é ‘teoricamente faz mais sentido essas variáveis estarem agrupadas em "
                f"quantos fatores?’. O custo de ir para um fator é "
                f"{br(CEN.loc['um_fator','pct'],1)}% dos setores mudando de faixa.”"],
              ["<b>Como vocês sabem que o índice está certo?</b>",
                f"“Pela validação externa: AUC de {br(AUC_IDX,3)} contra os "
                "setores de favela do IBGE, que é uma classificação oficial em que nenhuma "
                "variável do índice entrou. Sorteando um setor de favela e um comum, o de "
                f"favela tem índice maior em {br(100*AUC_IDX,1)}% das vezes.”"]],
             [5.0 * cm, 12.0 * cm], tam=7.8),

      P("As técnicas", "h2"),
      tabela(["A pergunta", "A resposta"],
             [["<b>O Bartlett deu significativo, então está tudo bem?</b>",
                "“Não, e é preciso dizer isso. Com 87 mil casos o teste rejeita por "
                "construção — o próprio livro adverte na página 43. A conclusão de "
                "adequabilidade se apoia no KMO e nos MSA individuais, que não crescem com "
                "o tamanho da amostra.”"],
              ["<b>Renda e cor/raça não estão correlacionadas demais?</b>",
               "“Estão altas, e é bom que a senhora tenha perguntado porque há uma sutileza. "
                "O número que circula nos nossos documentos é −0,81, calculado par a par "
                "sobre os 104 mil setores. Na matriz que a análise fatorial efetivamente "
                "decompõe, que é por exclusão de casos, o valor é <b>0,784</b> — abaixo do "
                "limiar de 0,80 do livro. Continua alto, e está nas limitações.”"],
              ["<b>Por que não usaram uma biblioteca pronta?</b>",
               "“Para não crescer a lista de dependências, e porque escrever a conta obriga "
               "a entendê-la. Documentamos o equivalente em R com o pacote psych, que é o "
               "padrão da área, justamente para permitir conferência independente.”"],
              ["<b>Vocês rodaram em R para conferir?</b>",
               "“Ainda não. O script está escrito e versionado, mas não foi executado. É a "
               "conferência mais forte que temos disponível e ainda está pendente.” "
               "<b>Não invente que rodou.</b>"],
              ["<b>Quantos setores entraram, afinal?</b>",
               "“104.108 no recorte urbano elegível, e <b>87.545</b> na análise fatorial — "
               "a diferença são 16.563 setores em que o IBGE sigila o analfabetismo. E esse "
               "sigilo não é aleatório: incide sobre os setores de melhor situação, então a "
               "amostra é enviesada para os mais vulneráveis. Está declarado.”"]],
             [5.0 * cm, 12.0 * cm], tam=7.8),

      P("As difíceis", "h2"),
      tabela(["A pergunta", "A resposta"],
             [["<b>Isso quer dizer que quem mora nesses setores é analfabeto e pobre?</b>",
               "“Não, e é uma distinção que o projeto faz questão de manter. Tudo o que o "
               "índice diz é sobre <b>territórios</b>. Passar disso para indivíduos é "
               "falácia ecológica, e está nas limitações com a referência.” "
               "<b>É a pergunta mais importante da lista.</b>"],
              ["<b>Esse índice é um construto ou uma soma de coisas diferentes?</b>",
               "“É a questão conceitual que trago em aberto, nos slides 28 e 29. Se for "
               "construto reflexivo, a análise fatorial é o instrumento certo. Se for índice "
               "formativo, parte dos nossos diagnósticos não se aplica e a decisão sobre o "
               "lixo se inverte. O que os dados sugerem é um híbrido, e falta literatura — "
               "Bollen e Lennox, de 1991, é o núcleo da discussão e não está lido.”"],
              ["<b>Os pesos não vão mudar se vocês mudarem a amostra?</b>",
               "“Medimos. Mil reamostragens com reposição movem a repartição entre as "
               "dimensões em <b>0,59 ponto percentual</b>. Com 87 mil setores a incerteza "
               "amostral é desprezível — o que limita esta análise é o número pequeno de "
               "variáveis, não o de casos.”"],
              ["<b>E a normalização por município, que é o objetivo intraurbano?</b>",
               "“É o Notebook 03, e a ordem entre os dois foi medida. Normalizar antes de "
               "fatorar derruba o KMO de 0,783 para 0,720 e muda os pesos de 65/35 para "
               "56/44. Fatoramos sobre os indicadores brutos de propósito: a covariação "
               "completa é o que identifica o construto.”"],
              ["<b>Por que a renda aparece invertida?</b>",
               "“Para que todas as sete variáveis apontem no mesmo sentido — valor maior, "
               "mais vulnerável. A inversão não muda correlações, autovalores, KMO nem "
               "comunalidades; muda só o sinal das cargas, e com ele a leitura.”"]],
             [5.0 * cm, 12.0 * cm], tam=7.8),
      Spacer(1, 6),
      caixa("A REGRA DE OURO",
            "<b>Nunca invente um número.</b> Todo valor do deck sai de uma tabela em "
            "<font face='Courier'>banco_de_dados/eda/fatorial/</font>, e abrir o arquivo na "
            "frente dela é resposta melhor do que arriscar de memória. E “não sei, vou "
            "verificar e volto” é resposta aceitável numa iniciação científica — inventar "
            "não é.", CLAY)]

# ═════════ PARTE 5 — SE O TEMPO APERTAR ═════════
S += [PageBreak(),
      P("Parte 5 — Se o tempo apertar", "h1"),
      P("Duas listas. A primeira é o que não pode cair de jeito nenhum. A segunda é o que "
        "cortar, em ordem — corte de cima para baixo até caber."),

      P("Os onze slides que não podem cair", "h2"),
      tabela(["Slide", "Por que é indispensável"],
             [["2", "monta o problema; sem ele ninguém entende por que a reunião existe"],
              ["4", "a base é adequada — é a licença para tudo o que vem depois"],
              ["9", "o número de fatores, com a honestidade de dizer que os critérios "
                    "discordam"],
              ["12", "o caso do lixo; é o achado mais concreto do trabalho"],
              ["14", "a rotação; é a citação mais forte e o eixo da história"],
              ["17", "as cargas — é a estrutura, o resultado central"],
              ["18", "o plano dos fatores; é a imagem que fixa o argumento do lixo"],
              ["20", "os pesos. Se só um slide sobrevivesse, seria este"],
              ["24", "a validação contra as favelas; é a prova de que funciona"],
              ["25", "o custo de cada escolha; traduz método em política pública"],
              ["42", "as seis decisões; é o que a reunião precisa produzir"]],
             [1.6 * cm, 15.4 * cm], tam=7.9),

      P("O que cortar, nesta ordem", "h2"),
      tabela(["Corte", "Slides", "O que dizer ao pular"],
             [["1º", "30–40 (a Parte 8 inteira)",
               "“A análise foi escrita à mão e não chamada de uma biblioteca; os slides 30 "
               "a 40 mostram cada conta e o equivalente em R, se a senhora quiser conferir "
               "por outro caminho.”"],
              ["2º", "27 (a renda sem o extremo)",
                f"“Verificamos a pendência da renda: não muda nada — {inteiro(RENDA_MUDA)} "
                "setores de 87 mil mudam de faixa.”"],
              ["3º", "21 (o bootstrap)",
               "“Os pesos são estáveis: mil reamostragens os movem em menos de meio ponto "
               "percentual.”"],
              ["4º", "15 e 16 (divergências 2 e 3)",
               "“Há mais dois pontos em que o livro contraria a referência anterior, e nos "
               "dois os dados nos deram razão. Estão no material.”"],
              ["5º", "6 (a matriz de correlação)",
               "“A estrutura já aparece na matriz de correlação, antes de fatorar.” "
               "<b>Só corte este se for necessário</b> — é um slide que convence."]],
             [1.2 * cm, 4.4 * cm, 11.4 * cm], tam=7.9),
      Spacer(1, 7),

      caixa("SE A REUNIÃO TIVER 15 MINUTOS",
            "Quatro slides e três frases.<br/><br/>"
            "<b>Slide 2</b> — “Quatro decisões estavam travadas por falta de saber quanto "
            "cada indicador deve pesar.”<br/>"
            f"<b>Slide 20</b> — “Os pesos são {br(SOCIO,1)} e {br(SANEA,1)}, saem dos dados, "
            "e batem com o IVS-BH dentro de cinco pontos.”<br/>"
            f"<b>Slide 24</b> — “E funciona: separa os setores de favela com AUC de "
            f"{br(AUC_IDX,3)}, contra uma lista oficial do IBGE.”<br/>"
            "<b>Slide 42</b> — “São seis decisões, e trago todas com o custo medido.”", CLAY),
      Spacer(1, 8),

      P("A véspera", "h2"),
      P("<b>Na noite anterior</b>, leia a Parte 2 deste documento (as três divergências) e "
        "a Parte 4 (as perguntas). São as duas que fazem diferença entre apresentar e ser "
        "arguido. A Parte 1 é consulta, não leitura corrida.<br/><br/>"
        "<b>Na hora</b>, tenha aberto: este documento, o Guia de Apoio, e a pasta "
        "<font face='Courier'>banco_de_dados/eda/fatorial/</font>. Se um número for "
        "questionado, abrir o arquivo na frente dela encerra a questão.<br/><br/>"
        "<b>Três coisas que você deve dizer sem ser perguntado</b>, porque dizê-las "
        "primeiro é o que demonstra domínio: que o Bartlett não informa nada nesta escala; "
        "que o índice descreve territórios e não pessoas; e que o script em R está escrito "
        "mas ainda não foi rodado."),
      Spacer(1, 6),
      caixa("O QUE ESTE TRABALHO TEM DE MELHOR, E QUE VOCÊ PODE DIZER SEM EXAGERO",
            "Três coisas.<br/><br/>"
            "<b>Uma convergência que ninguém forçou.</b> Os pesos saíram dos dados e caíram "
            "a cinco pontos do IVS-BH 2012, que foi construído por outro caminho, em outra "
            "década.<br/><br/>"
            "<b>Uma validação com marcador externo.</b> A lista de favelas do IBGE não "
            "entrou na construção do índice, e o índice a recupera com AUC de "
            f"{br(AUC_IDX,3)}. Poucos índices compostos têm um teste desses disponível."
            "<br/><br/>"
            "<b>Uma crítica própria à referência.</b> A regra mecânica de comunalidade "
            "teria excluído a água em vez do lixo. Perceber isso — e mostrar por quê — é "
            "contribuição, não repetição de manual.", PETROL)]

doc.build(S)
print(f"plano escrito: {saida}")
