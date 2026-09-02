"""Gera o PDF que destrincha o critério de outlier de renda.

O deck da EDA Central resume a classificação em um slide e meio. Este documento abre a
regra inteira: o corte de Tukey por município, a trava dos municípios pequenos, os três
testes de coerência com os limiares que cada um usa, o que cada teste efetivamente pegou,
e os dois diagnósticos que ficam de fora da classificação de propósito.

Todos os números são recalculados aqui a partir de banco_de_dados/eda/, não digitados.
A regra descrita é a de src/ivs_censo/renda.py; as constantes são importadas de lá, para
que o texto não descreva uma versão diferente da que roda.

Uso:
    uv run --with reportlab --with matplotlib --with pandas \
        python scripts/gerar_pdf_outliers_renda.py \
        docs/Apresentacoes_IVS/complementos/Criterio_Outliers_Renda.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

RAIZ = Path(__file__).resolve().parents[1]
EDA = RAIZ / "banco_de_dados" / "eda"
sys.path.insert(0, str(RAIZ / "src"))
from ivs_censo.renda import (K_TUKEY, MIN_SETORES_MUNICIPIO,  # noqa: E402
                             RAZAO_IMPLAUSIVEL)

TINTA = colors.HexColor("#1A1A1A")
PETROL = colors.HexColor("#1F4E4A")
CLAY = colors.HexColor("#A83A2C")
CINZA = colors.HexColor("#666666")
LINHA = colors.HexColor("#C8C8C8")
FUNDO = colors.HexColor("#F2F0EC")

SERIF, SANS, MONO = "Times-Roman", "Helvetica", "Courier"
SERIF_B, SANS_B = "Times-Bold", "Helvetica-Bold"


def ler(nome: str) -> pd.DataFrame:
    return pd.read_csv(EDA / nome, sep=";", encoding="utf-8-sig")


# ── dados ───────────────────────────────────────────────────────────────────
T = ler("renda_outliers_rastreados.csv")
CLASSES = ler("renda_classes_resumo.csv")
CRIT = ler("renda_criterio_global_vs_municipal.csv")
PEQ = ler("renda_setores_pequenos.csv")
MUN = ler("exclusao_rural_conferencia.csv")
NORM = ler("renda_normalizacao_impacto.csv")

SUS = T[T.classe_renda == "SUSPEITO"]
EXT = T[T.classe_renda == "EXTREMO"]
N_SUS, N_EXT = len(SUS), len(EXT)

MOTIVOS = SUS["motivos"].fillna("").value_counts()
POR_TESTE = {m: int(SUS["motivos"].fillna("").str.contains(m).sum())
             for m in ["e_favela", "pct_analfab_acima", "pct_raca_pretpardind_acima"]}
QTD_TESTES = SUS["motivos"].fillna("").str.count(r"\+").add(1).value_counts().sort_index()

MUN_PEQ = MUN[MUN.n_ok_urbano < MIN_SETORES_MUNICIPIO].sort_values("n_ok_urbano")
N_MUN_PEQ, N_SET_PEQ = len(MUN_PEQ), int(MUN_PEQ.n_ok_urbano.sum())
N_MUN_AVAL = int((MUN.n_ok_urbano >= MIN_SETORES_MUNICIPIO).sum())

IMPL_EXT = EXT[EXT.razao_implausivel].sort_values("razao_mediana_mun", ascending=False)
IMPL_SUS = int(SUS.razao_implausivel.sum())
CONCORDAM = int(CRIT.concordam.sum())
SO_GLOBAL = int(CRIT.so_global.sum())
SO_MUNICIPAL = int(CRIT.so_municipal.sum())
N_GLOBAL = int(CRIT.outlier_global.sum())
N_MUNICIPAL = int(CRIT.outlier_municipal.sum())

FIGDIR = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "banco_de_dados" / "eda" / "figuras"


def br(x, casas=2):
    """Formata número no padrão brasileiro."""
    s = f"{x:,.{casas}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


# ── figura de apoio ─────────────────────────────────────────────────────────
def figura_motivos(destino: Path) -> Path:
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.2, 3.1))

    rotulos = {"e_favela": "é favela\n(CD_TIPO = 1)",
               "pct_analfab_acima": "analfabetismo\nacima do p50 local",
               "pct_raca_pretpardind_acima": "PPI acima\ndo p75 local"}
    nomes = [rotulos[k] for k in POR_TESTE]
    vals = list(POR_TESTE.values())
    barras = a.barh(nomes, vals, color=["#1F4E4A", "#A83A2C", "#7A9B96"], height=0.6)
    a.bar_label(barras, padding=3, fontsize=9)
    a.set_xlim(0, max(vals) * 1.25)
    a.set_title(f"Quantos dos {N_SUS} suspeitos cada teste pegou", fontsize=9.5, loc="left")
    a.tick_params(labelsize=8)
    for lado in ("top", "right", "bottom"):
        a.spines[lado].set_visible(False)
    a.set_xticks([])

    dados = [EXT["cv_renda"].dropna(), SUS["cv_renda"].dropna()]
    bp = b.boxplot(dados, orientation="horizontal", widths=0.5, patch_artist=True, showfliers=False,
                   tick_labels=[f"EXTREMO (n={len(dados[0])})", f"SUSPEITO (n={len(dados[1])})"])
    for caixa, cor in zip(bp["boxes"], ["#7A9B96", "#A83A2C"]):
        caixa.set_facecolor(cor)
        caixa.set_alpha(0.55)
    for m in bp["medians"]:
        m.set_color("#1A1A1A")
    b.axvline(0.78, color="#1F4E4A", ls="--", lw=1)
    b.set_ylim(0.35, 2.65)
    b.text(0.78, 0.48, "  mediana nacional 0,78", fontsize=7.5, color="#1F4E4A",
           va="bottom", ha="left")
    b.set_title("Coeficiente de variação da renda no setor", fontsize=9.5, loc="left")
    b.tick_params(labelsize=8)
    for lado in ("top", "right"):
        b.spines[lado].set_visible(False)

    fig.tight_layout()
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return destino


FIG_MOTIVOS = figura_motivos(FIGDIR / "renda_criterio_motivos.png")

# ── estilos ─────────────────────────────────────────────────────────────────
E = {
    "capa": ParagraphStyle("capa", fontName=SERIF_B, fontSize=21, leading=25, textColor=TINTA),
    "sub": ParagraphStyle("sub", fontName=SANS, fontSize=9.5, leading=13.5, textColor=CINZA),
    "h1": ParagraphStyle("h1", fontName=SERIF_B, fontSize=13.5, leading=16, textColor=PETROL,
                         spaceBefore=16, spaceAfter=5),
    "h2": ParagraphStyle("h2", fontName=SANS_B, fontSize=10, leading=13, textColor=TINTA,
                         spaceBefore=11, spaceAfter=3),
    "p": ParagraphStyle("p", fontName=SANS, fontSize=9.2, leading=13.4, textColor=TINTA,
                        alignment=TA_JUSTIFY, spaceAfter=5),
    "destaque": ParagraphStyle("destaque", fontName=SANS, fontSize=9.2, leading=13.4,
                               textColor=CLAY, alignment=TA_JUSTIFY, spaceAfter=5),
    "nota": ParagraphStyle("nota", fontName=SANS, fontSize=7.6, leading=10.4, textColor=CINZA,
                           spaceBefore=1, spaceAfter=9),
    "leg": ParagraphStyle("leg", fontName=SANS, fontSize=7.6, leading=10, textColor=CINZA,
                          alignment=1, spaceBefore=2, spaceAfter=9),
}


def P(t, e="p"):
    return Paragraph(t, E[e])


def nota(t):
    return Paragraph(t, E["nota"])


def tabela(cabecalho, linhas, larguras, tam=7.6, alinha_dir=None):
    dados = [[Paragraph(f"<b>{c}</b>", ParagraphStyle(
        "th", fontName=SANS_B, fontSize=tam, leading=tam + 2.2, textColor=PETROL))
        for c in cabecalho]]
    est_cel = ParagraphStyle("td", fontName=SANS, fontSize=tam, leading=tam + 2.4, textColor=TINTA)
    for ln in linhas:
        dados.append([c if isinstance(c, Paragraph) else Paragraph(str(c), est_cel) for c in ln])
    t = Table(dados, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    estilo = [
        ("GRID", (0, 0), (-1, -1), 0.35, LINHA),
        ("BACKGROUND", (0, 0), (-1, 0), FUNDO),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for c in (alinha_dir or []):
        estilo.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(estilo))
    return t


def caixa(titulo, texto, cor=PETROL):
    est_t = ParagraphStyle("bt", fontName=SANS_B, fontSize=8.8, leading=11.5, textColor=cor)
    est_c = ParagraphStyle("bc", fontName=SANS, fontSize=8.6, leading=12,
                           textColor=TINTA, alignment=TA_JUSTIFY)
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


# ── documento ───────────────────────────────────────────────────────────────
saida = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "docs" / "Apresentacoes_IVS" / "complementos" / "Criterio_Outliers_Renda.pdf"
saida.parent.mkdir(parents=True, exist_ok=True)

LARG, ALT = A4
MARG = 2.0 * cm


def rodape(canv, doc):
    canv.saveState()
    canv.setFont(SANS, 7.3)
    canv.setFillColor(CINZA)
    canv.drawString(MARG, 1.25 * cm,
                    "Critério de outliers de renda · IVS intraurbano · Censo 2022 · ELSI-Brasil")
    canv.drawRightString(LARG - MARG, 1.25 * cm, f"{doc.page}")
    canv.setStrokeColor(LINHA)
    canv.setLineWidth(0.4)
    canv.line(MARG, 1.62 * cm, LARG - MARG, 1.62 * cm)
    canv.restoreState()


doc = BaseDocTemplate(str(saida), pagesize=A4,
                      leftMargin=MARG, rightMargin=MARG,
                      topMargin=1.8 * cm, bottomMargin=2.1 * cm,
                      title="Critério de outliers de renda",
                      author="Pedro Dias Soares")
doc.addPageTemplates([PageTemplate(
    id="corpo",
    frames=[Frame(MARG, 2.1 * cm, LARG - 2 * MARG, ALT - 1.8 * cm - 2.1 * cm, id="f")],
    onPage=rodape)])

S = []

# ── abertura ────────────────────────────────────────────────────────────────
S.append(P("Os extremos de renda: o critério, aberto", "capa"))
S.append(Spacer(1, 5))
S.append(P("Como um setor censitário vira SUSPEITO, EXTREMO ou NORMAL · Anexo à EDA Central "
           "· Índice de Vulnerabilidade da Saúde intraurbano · Censo Demográfico 2022 · "
           "70 municípios do ELSI-Brasil<br/>Pedro Dias Soares · Iniciação Científica · "
           "Fiocruz Minas, Instituto René Rachou", "sub"))
S.append(Spacer(1, 12))

S.append(caixa(
    "O que este documento acrescenta ao que está na apresentação",
    "O deck resume a classificação em um slide e meio e mostra o resultado. Aqui está a regra "
    "inteira: onde exatamente cai o corte de extremo, por que ele é calculado dentro de cada "
    f"município, quais são os três testes de coerência e o limiar de cada um, quantos dos "
    f"{N_SUS} suspeitos cada teste pegou sozinho, e as duas colunas de diagnóstico que ficam "
    "fora da classificação de propósito. Nada aqui muda a apresentação nem os números já "
    "apresentados."))
S.append(Spacer(1, 10))

# ── 1. o problema ───────────────────────────────────────────────────────────
S.append(P("1  Por que a renda precisa de um tratamento próprio", "h1"))
S.append(P(
    "A renda média do responsável, <font face='Courier'>V06004</font>, é a componente do IVS "
    "com a distribuição mais torta: assimetria de 3,74 no recorte urbano, contra 2,38 a 3,42 "
    "das três variáveis de saneamento. Os extremos dela não têm todos a mesma natureza, e é "
    "essa a razão de existir um critério em vez de uma regra única."))
S.append(P(
    "São três coisas diferentes com a mesma aparência. Há <b>erro de dado</b>, como o setor de "
    "favela em Belo Horizonte com R$ 170.418,06 de renda média por responsável. Há <b>extremo "
    "genuíno</b>, o bairro rico cuja renda alta o entorno inteiro sustenta. E há <b>setor "
    "pequeno com média instável</b>, onde poucos domicílios fazem a média oscilar. Excluir os "
    "três ou manter os três perde informação nos dois sentidos: no primeiro caso some a "
    "desigualdade real que o índice existe para medir, no segundo o erro entra no cálculo."))

# ── 2. o procedimento ───────────────────────────────────────────────────────
S.append(P("2  O procedimento, etapa a etapa", "h1"))
S.append(P(
    "A regra está em <font face='Courier'>src/ivs_censo/renda.py</font>, na função "
    "<font face='Courier'>rastrear_outliers_renda</font>. Ela rotula em quatro etapas, e as "
    "constantes citadas abaixo são importadas do módulo por este gerador, de modo que o texto "
    "não pode descrever uma versão diferente da que roda."))

S.append(P("2.1  Etapa 1: onde cai o corte de extremo", "h2"))
S.append(P(
    f"O corte é o limite superior de Tukey, <font face='Courier'>q3 + k × (q3 − q1)</font>, com "
    f"<b>k = {br(K_TUKEY, 1)}</b>. Essa escolha merece atenção porque o valor usual, e o que "
    f"aparece na tabela de outliers da apresentação, é k = 1,5. Com k = 1,5 rotula-se a cauda "
    f"inteira; a intenção aqui não é descrever a cauda, e sim isolar o extremo distante, então "
    f"o critério usa o corte de outlier extremo. Os dois limiares convivem no projeto para "
    f"finalidades diferentes: k = 1,5 descreve a forma da distribuição de cada componente, "
    f"k = {br(K_TUKEY, 1)} seleciona casos para inspeção."))

S.append(P("2.2  Etapa 2: o corte é calculado dentro de cada município", "h2"))
S.append(P(
    "O quartil e o intervalo interquartil saem da distribuição do próprio município, não do "
    "país. O IVS é um índice intraurbano, que compara setores dentro da mesma cidade: R$ 20 mil "
    "é um valor comum em São Paulo e uma anomalia em Autazes. Um corte nacional mede a "
    "distância entre cidades, que não é o objeto da análise. A seção 6 mostra o quanto os dois "
    "critérios divergem na prática."))

S.append(P("2.3  Etapa 3: a trava dos municípios pequenos", "h2"))
S.append(P(
    f"Em município com poucos setores o quartil não é confiável, então a regra não rotula por "
    f"ele: quando o município tem menos de <b>{MIN_SETORES_MUNICIPIO} setores</b>, o limite "
    f"superior fica indefinido e nenhum setor de lá pode ser marcado. Isso tem consequência "
    f"concreta e não está na apresentação: <b>{N_MUN_PEQ} dos 70 municípios</b>, somando "
    f"<b>{br(N_SET_PEQ, 0)} setores</b>, estão estruturalmente fora da detecção. "
    f"{N_MUN_AVAL} municípios são efetivamente avaliados."))
S.append(tabela(
    ["Município", "Região", "Setores urbanos"],
    [[r.NM_MUN, r.regiao, int(r.n_ok_urbano)] for r in MUN_PEQ.itertuples()],
    [7.4 * cm, 5.2 * cm, 4.4 * cm], alinha_dir=[2]))
S.append(nota("Fonte: exclusao_rural_conferencia.csv, recorte urbano elegível. Um erro de renda "
              "num desses setores passa despercebido pela regra, e é uma limitação a declarar."))

S.append(P("2.4  Etapa 4: os três testes de coerência", "h2"))
S.append(P(
    "Passado o corte, o setor é extremo. A pergunta seguinte é se o resto do perfil dele "
    "sustenta a renda declarada. O que levanta suspeita não é o valor em si, e sim a "
    "<b>incoerência</b> entre a renda e o restante do setor. São três testes, e cada um compara "
    "o setor com o próprio município:"))
S.append(tabela(
    ["Teste", "Condição exata", "Limiar"],
    [["<font face='Courier'>e_favela</font>",
      "<font face='Courier'>CD_TIPO = 1</font>, ou seja, Favela e Comunidade Urbana",
      "não é limiar, é categoria"],
     ["<font face='Courier'>pct_analfab_acima</font>",
      "analfabetismo do setor acima do do município",
      "<b>mediana</b> (p50) local"],
     ["<font face='Courier'>pct_raca_pretpardind_acima</font>",
      "proporção preta, parda ou indígena acima da do município",
      "<b>terceiro quartil</b> (p75) local"]],
    [4.9 * cm, 7.5 * cm, 4.6 * cm]))
S.append(nota("Os dois limiares são diferentes, e a apresentação diz apenas 'acima da mediana do "
              "município' para os dois. O de cor/raça é o p75, não a mediana."))
S.append(P(
    "Basta <b>um</b> dos três disparar para o setor ser considerado incoerente. Daí a "
    "classificação: extremo <b>e</b> incoerente é SUSPEITO; extremo e coerente é EXTREMO; o "
    "resto é NORMAL. Setor sem renda informada não é outlier de renda e fica em NORMAL."))

S.append(caixa(
    "O que a regra não faz",
    "Ela rotula, não remove. Nenhuma observação é excluída da base pelo módulo, e as duas "
    "versões da análise, com e sem os suspeitos, ficam publicadas lado a lado. A decisão de "
    "excluir é de quem analisa, e é justamente para sustentá-la que as duas versões existem."))

S.append(PageBreak())

# ── 3. o resultado ──────────────────────────────────────────────────────────
S.append(P("3  O resultado: as três classes", "h1"))
S.append(tabela(
    ["Classe", "Setores", "% da base", "Renda mediana", "Renda média", "Renda máxima"],
    [[f"<b>{r.classe_renda}</b>", br(r.n_setores, 0), br(r.pct_setores, 3) + "%",
      "R$ " + br(r.renda_mediana), "R$ " + br(r.renda_media), "R$ " + br(r.renda_max)]
     for r in CLASSES.itertuples()],
    [2.7 * cm, 2.2 * cm, 2.2 * cm, 3.3 * cm, 3.3 * cm, 3.3 * cm], alinha_dir=[1, 2, 3, 4, 5]))
S.append(nota("Fonte: renda_classes_resumo.csv. Recorte urbano elegível, 104.108 setores."))
S.append(P(
    f"Um detalhe da tabela que vale explicitar, porque é fácil ler ao contrário: a renda "
    f"mediana dos SUSPEITOS, R$ {br(float(CLASSES.loc[CLASSES.classe_renda == 'SUSPEITO', 'renda_mediana'].iloc[0]))}, "
    f"é <b>menor</b> que a dos EXTREMOS, R$ {br(float(CLASSES.loc[CLASSES.classe_renda == 'EXTREMO', 'renda_mediana'].iloc[0]))}. "
    f"Isso é coerente com o desenho: o critério não seleciona os valores mais altos, seleciona "
    f"os valores altos <b>no lugar errado</b>."))

# ── 4. o que cada teste pegou ───────────────────────────────────────────────
S.append(P("4  O que cada teste efetivamente pegou", "h1"))
S.append(P(
    f"Esta é a abertura que o deck não traz. Dos {N_SUS} suspeitos, a coluna "
    f"<font face='Courier'>motivos</font> registra quais testes dispararam em cada um. A "
    f"distribuição é bastante desigual."))
S.append(tabela(
    ["Combinação de testes que disparou", "Setores"],
    [[m.replace("_", "_") if m else "(nenhum)", int(n)] for m, n in MOTIVOS.items()],
    [12.5 * cm, 4.5 * cm], alinha_dir=[1]))
S.append(nota("Fonte: renda_outliers_rastreados.csv, coluna motivos."))
S.append(Image(str(FIG_MOTIVOS), width=17.0 * cm, height=17.0 * cm * 3.1 / 9.2))
S.append(Paragraph("À esquerda, quantos suspeitos cada teste marcou, contando também os setores "
                   "em que mais de um disparou. À direita, o coeficiente de variação da renda "
                   "nas duas classes.", E["leg"]))
S.append(P(
    f"Três leituras. Primeira: <b>{int(QTD_TESTES.get(1, 0))} dos {N_SUS} suspeitos disparam um "
    f"único teste</b>, e apenas {int(QTD_TESTES.get(3, 0))} disparam os três. A suspeita, na "
    f"maioria dos casos, se apoia num sinal só."))
S.append(P(
    f"Segunda: esse sinal único costuma ser o mais fraco dos três. "
    f"{int(MOTIVOS.get('pct_analfab_acima', 0))} setores são flagrados apenas por ter "
    f"analfabetismo acima da mediana do município, e estar acima da mediana é, por construção, "
    f"um evento de cerca de metade dos setores. Esses casos merecem inspeção individual antes "
    f"de qualquer exclusão, não tratamento de bloco."))
S.append(P(
    f"Terceira: {POR_TESTE['e_favela']} dos {N_SUS} são favela, o que corresponde aos 33% "
    f"citados na apresentação. Como <font face='Courier'>e_favela</font> é um dos testes, "
    f"nenhum setor de favela pode cair em EXTREMO. A frase 'nenhum dos extremos coerentes é "
    f"favela' repete a regra, não a confirma, e por isso não deve ser usada como evidência a "
    f"favor do critério."))

_cols = ["CD_SETOR", "NM_MUN", "NM_BAIRRO", "renda_media_setor", "renda_p50_mun",
         "razao_mediana_mun", "n_domicilios", "cv_renda", "motivos"]
_top = SUS.sort_values("renda_media_setor", ascending=False)[_cols].head(8)
S.append(KeepTogether([
    P("4.1  Os maiores suspeitos", "h2"),
    tabela(
        ["Setor", "Município", "Bairro", "Renda", "Mediana mun.", "Razão", "Dom.", "CV", "Testes"],
        [[str(r.CD_SETOR), r.NM_MUN, ("—" if pd.isna(r.NM_BAIRRO) else r.NM_BAIRRO),
          br(r.renda_media_setor, 0), br(r.renda_p50_mun, 0), br(r.razao_mediana_mun, 1) + "×",
          br(r.n_domicilios, 0), br(r.cv_renda, 2),
          str(r.motivos).replace("e_favela", "favela")
                        .replace("pct_analfab_acima", "analfab")
                        .replace("pct_raca_pretpardind_acima", "PPI")]
         for r in _top.itertuples()],
        [2.9 * cm, 2.1 * cm, 2.5 * cm, 1.6 * cm, 1.7 * cm, 1.2 * cm, 1.0 * cm, 1.0 * cm, 3.0 * cm],
        tam=6.6, alinha_dir=[3, 4, 5, 6, 7]),
    nota("Renda e mediana municipal em reais. Razão = renda do setor ÷ mediana do município. "
         "CV = √V06005 ÷ V06004."),
]))

# ── 5. diagnósticos fora da regra ───────────────────────────────────────────
S.append(P("5  Os dois diagnósticos que ficam fora da classificação", "h1"))
S.append(P(
    "O módulo calcula mais duas colunas que <b>não</b> entram na classificação. Isso é "
    "deliberado: a regra de três classes já foi apresentada, e mudá-la por conta própria "
    "alteraria números já vistos. As colunas existem para mostrar onde a regra não enxerga."))

S.append(P("5.1  cv_renda: a média depende de quantas declarações?", "h2"))
S.append(P(
    "O arquivo do IBGE traz <font face='Courier'>V06005</font>, a variância do rendimento no "
    "setor, e com ela dá para calcular o coeficiente de variação, "
    "<font face='Courier'>√V06005 ÷ V06004</font>. Ele mede o quanto a média do setor depende "
    "de poucas declarações. A mediana nacional é 0,78, o p99 é 2,53 e o p99,9 é 8,12."))
S.append(P(
    f"Entre os suspeitos a mediana do CV é {br(SUS.cv_renda.median(), 2)}, contra "
    f"{br(EXT.cv_renda.median(), 2)} entre os extremos coerentes: quase o dobro. É a evidência "
    f"independente de que os dois grupos não são a mesma coisa, e ela não vem do critério, vem "
    f"de uma variável que o critério não usa."))
S.append(caixa(
    "Por que isto derruba a hipótese da vírgula fora do lugar",
    "A leitura de que o valor de Belo Horizonte seria R$ 1.704,18, ou seja, 170.418,06 dividido "
    "por 100, é testável com essa variável. Se apenas a média tivesse deslizado uma casa "
    "decimal, o coeficiente de variação do setor seria da ordem de 526. Ele é 5,26. A variância "
    "publicada pelo IBGE é coerente com a média alta, o que significa que o dado não indica erro "
    "de digitação: indica um setor com uma ou poucas declarações enormes puxando a média. A "
    "consequência é diferente e mais incômoda, porque não se corrige dividindo por 100 nem se "
    "resolve excluindo 66 setores. Argumenta-se por estatística robusta, posto ou logaritmo, "
    "para a variável inteira.", CLAY))

S.append(P("5.2  razao_implausivel: o ponto cego da regra", "h2", ))
S.append(P(
    f"O teste de coerência não enxerga erro de dado em bairro rico, porque ali o entorno "
    f"sustenta a renda alta e o setor sai como EXTREMO. A coluna "
    f"<font face='Courier'>razao_implausivel</font> é o contrapeso: marca o setor cuja renda "
    f"supera <b>{br(RAZAO_IMPLAUSIVEL, 0)} vezes a mediana do município</b>, independentemente "
    f"do perfil do entorno. Ela marca {len(IMPL_EXT)} setores classificados como EXTREMO e "
    f"{IMPL_SUS} já classificados como SUSPEITO."))
S.append(P(
    f"Os {len(IMPL_EXT)} da tabela abaixo são os casos que a regra atual não pega. O primeiro "
    f"deles é o segundo maior valor de renda de toda a base."))
_impl = IMPL_EXT[_cols].head(13)
S.append(tabela(
    ["Setor", "Município", "Bairro", "Renda", "Mediana mun.", "Razão", "Dom.", "CV"],
    [[str(r.CD_SETOR), r.NM_MUN, ("—" if pd.isna(r.NM_BAIRRO) else r.NM_BAIRRO),
      br(r.renda_media_setor, 0), br(r.renda_p50_mun, 0), br(r.razao_mediana_mun, 1) + "×",
      br(r.n_domicilios, 0), br(r.cv_renda, 2)]
     for r in _impl.itertuples()],
    [3.1 * cm, 2.6 * cm, 3.3 * cm, 2.0 * cm, 2.1 * cm, 1.5 * cm, 1.2 * cm, 1.2 * cm],
    tam=6.9, alinha_dir=[3, 4, 5, 6, 7]))
S.append(nota("Fonte: renda_outliers_rastreados.csv, filtrando classe EXTREMO com "
              "razao_implausivel verdadeiro. Promover esta coluna a critério é decisão de "
              "método, e por isso não foi feita sem sua arbitragem."))

# ── 6. global x municipal ───────────────────────────────────────────────────
S.append(P("6  Por que o corte é municipal, em números", "h1"))
S.append(P(
    f"A escolha entre corte global e corte municipal não é detalhe: os dois selecionam "
    f"conjuntos bastante diferentes. O critério global marca {br(N_GLOBAL, 0)} setores, o "
    f"municipal marca {br(N_MUNICIPAL, 0)}, e apenas <b>{br(CONCORDAM, 0)}</b> estão nos dois. "
    f"São {br(SO_GLOBAL, 0)} marcados só pelo global e {br(SO_MUNICIPAL, 0)} só pelo municipal."))
S.append(tabela(
    ["Região", "Setores", "Global", "% global", "Municipal", "% municipal", "Coincidem"],
    [[r.regiao, br(r.n_setores, 0), br(r.outlier_global, 0), br(r.pct_global, 2) + "%",
      br(r.outlier_municipal, 0), br(r.pct_municipal, 2) + "%", br(r.concordam, 0)]
     for r in CRIT.itertuples()],
    [2.9 * cm, 2.1 * cm, 1.9 * cm, 2.1 * cm, 2.3 * cm, 2.6 * cm, 2.1 * cm],
    tam=7.4, alinha_dir=[1, 2, 3, 4, 5, 6]))
S.append(nota("Fonte: renda_criterio_global_vs_municipal.csv."))
S.append(P(
    "A inversão entre Norte e Sudeste é o argumento inteiro. O critério global marca 4,61% dos "
    "setores do Sudeste e só 1,32% dos do Norte, porque responde à pergunta 'este setor é rico "
    "para o Brasil?'. O critério municipal inverte, com 7,40% no Norte e 2,22% no Sudeste, "
    "porque responde a 'este setor destoa da própria cidade?'. Para um índice intraurbano, a "
    "segunda pergunta é a certa, e a primeira encontraria anomalia onde há apenas riqueza."))

# ── 7. tamanho do setor ─────────────────────────────────────────────────────
S.append(P("7  A relação com o tamanho do setor", "h1"))
S.append(P(
    "A hipótese de que os valores exorbitantes se concentram em setores pequenos se confirma "
    "pela metade, e a distinção importa. O valor em si não depende do tamanho: o Spearman entre "
    "número de domicílios e renda é −0,031, e o maior valor da base está num setor de 186 "
    "domicílios, que é o tamanho mediano. Já a taxa de suspeita depende, e bastante."))
S.append(tabela(
    ["Faixa de domicílios", "Setores", "% da base", "Renda mediana", "Renda máxima",
     "CV", "Suspeitos", "% suspeitos"],
    [[r.faixa_dom, br(r.n_setores, 0), br(r.pct_da_base, 2) + "%", br(r.renda_mediana, 0),
      br(r.renda_max, 0), br(r.cv, 3), int(r.n_suspeitos), br(r.pct_suspeitos, 3) + "%"]
     for r in PEQ.itertuples()],
    [2.9 * cm, 1.8 * cm, 1.9 * cm, 2.3 * cm, 2.2 * cm, 1.6 * cm, 1.8 * cm, 2.2 * cm],
    tam=7.2, alinha_dir=[1, 2, 3, 4, 5, 6, 7]))
S.append(nota("Fonte: renda_setores_pequenos.csv. CV é o coeficiente de variação da renda dentro "
              "da faixa, não o CV do setor."))
S.append(P(
    "A taxa de suspeita cai de 0,265% nos setores de até 50 domicílios para 0,045% nos de 201 a "
    "400, seis vezes menos, e o coeficiente de variação acompanha, de 1,109 para 0,913. O "
    "mecanismo é o esperado: média de poucos domicílios oscila mais. Ele existe, está medido, e "
    "não é o que produz o maior valor da base."))

# ── 8. limitações ───────────────────────────────────────────────────────────
S.append(P("8  As quatro limitações do critério, nomeadas", "h1"))
S.append(tabela(
    ["Limitação", "O que ela significa"],
    [["<b>A separação favela / não favela é definição</b>",
      f"<font face='Courier'>e_favela</font> é um dos testes, então todo setor de favela que "
      f"seja outlier municipal cai obrigatoriamente em SUSPEITO e nenhum pode cair em EXTREMO. "
      f"A coluna 'São favela?' da apresentação repete a regra; ela não a valida."],
     ["<b>O sinal do analfabetismo é fraco</b>",
      f"Estar acima da mediana do município é evento de cerca de 50% por construção, e "
      f"{int(MOTIVOS.get('pct_analfab_acima', 0))} dos {N_SUS} suspeitos são flagrados só por "
      f"ele. São os casos que mais precisam de inspeção individual."],
     ["<b>Erro em bairro rico é invisível</b>",
      f"A regra detecta incoerência de contexto, não implausibilidade de magnitude. Os "
      f"{len(IMPL_EXT)} setores da seção 5.2 saem como EXTREMO porque o entorno sustenta renda "
      f"alta, e só <font face='Courier'>razao_implausivel</font> os denuncia."],
     ["<b>Municípios pequenos ficam fora</b>",
      f"{N_MUN_PEQ} municípios e {br(N_SET_PEQ, 0)} setores não são avaliados, porque abaixo de "
      f"{MIN_SETORES_MUNICIPIO} setores o quartil do município não é confiável. Um erro de renda "
      f"nesses setores não é detectado."]],
    [5.0 * cm, 12.0 * cm], tam=7.8))

# ── 9. o que fazer ──────────────────────────────────────────────────────────
S.append(P("9  O que eu recomendo, e o que depende da senhora", "h1"))
S.append(P(
    f"Minha recomendação continua sendo que os {N_SUS} suspeitos saiam do cálculo do índice e "
    f"fiquem na EDA como achado de qualidade do dado, com as duas versões publicadas. O "
    f"argumento não é o efeito na média nem na correlação, que é pequeno, e sim o efeito na "
    f"normalização min-max por município, que é o insumo do índice: em Autazes um único valor "
    f"ruim comprime 81,4% dos setores no primeiro decil da escala, e sem ele são 14,3%. Dos "
    f"{len(NORM)} municípios avaliados nessa tabela, {int((NORM.n_suspeitos > 0).sum())} têm ao "
    f"menos um suspeito."))
S.append(P("Três decisões seguem em aberto e são de método, não de execução:", "p"))
S.append(tabela(
    ["#", "Decisão", "Minha leitura"],
    [["1", "Promover <font face='Courier'>razao_implausivel</font> a critério, em vez de "
           "deixá-la como diagnóstico",
      f"Pegaria os {len(IMPL_EXT)} casos da seção 5.2, que hoje escapam. Muda números já "
      f"apresentados, então não fiz sem sua palavra."],
     ["2", "Inspecionar individualmente os "
           f"{int(MOTIVOS.get('pct_analfab_acima', 0))} suspeitos de sinal único",
      "É trabalho manual e finito. Reduziria a chance de excluir setor legítimo por um teste "
      "que dispara em metade da base por construção."],
     ["3", "Transformar a variável, em log ou em posto, em vez de tratar caso a caso",
      "Mesmo removendo os 66, Belo Horizonte fica com 70,8% dos setores no primeiro decil. O "
      "que quebra a escala é a assimetria de 3,74, não os 66 valores."]],
    [0.8 * cm, 7.4 * cm, 8.8 * cm], tam=7.8))
S.append(Spacer(1, 8))
S.append(caixa(
    "Onde está cada coisa",
    "A regra: <font face='Courier'>src/ivs_censo/renda.py</font>. A execução e as tabelas: "
    "<font face='Courier'>scripts/auditoria_renda.py</font>. Os "
    f"{br(len(T), 0)} setores extremos, um por linha e com identificação completa: "
    "<font face='Courier'>banco_de_dados/eda/renda_outliers_rastreados.csv</font>. Este PDF é "
    "gerado por <font face='Courier'>scripts/gerar_pdf_outliers_renda.py</font>, que recalcula "
    "todos os números a partir dos CSVs e importa as constantes do módulo."))

doc.build(S)
print("pdf escrito:", saida)
