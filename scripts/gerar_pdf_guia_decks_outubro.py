"""Gera o guia de apoio das duas apresentações de outubro — a cronologia do projeto e as
demandas de setembro —, explicado do zero.

Para que serve
--------------
Os dois decks foram escritos para quem acompanhou o projeto. Este guia faz o caminho inverso:
supõe que o leitor não sabe o que é um setor censitário, uma análise fatorial ou um commit, e
explica, slide por slide, o que está ali, o que cada termo quer dizer, como ler os números e o
que responder se perguntarem.

Como o guia está montado
------------------------
- Parte A (o mínimo para entender tudo) e Parte D (glossário): scripts/guia_outubro_base.py.
- Parte B, a cronologia slide a slide: scripts/guia_outubro_cronologia.py.
- Parte C, as demandas de setembro slide a slide: scripts/guia_outubro_demandas.py.

Cada verbete abre com a miniatura do próprio slide: os dois .pptx são convertidos em PDF pelo
LibreOffice e cada página é colada, em vetor, no espaço que o verbete reservou (pypdf). Sem o
LibreOffice, o espaço fica com um quadro e o número do slide.

Antes de montar, o script confere se o título de cada verbete aparece no slide de mesmo
número: se um deck for regerado e os slides mudarem de lugar, o guia para em vez de explicar
o slide errado.

Os números que vêm de CSV ou do git são calculados aqui, dos mesmos arquivos que os decks
leem, e chegam aos textos como N.<nome>. Os que só existem em documento (decisões do GUIA,
demandas de julho, contagens das auditorias) aparecem como estão no documento citado.

Uso:
    uv run --with reportlab --with pandas --with pypdf python scripts/gerar_pdf_guia_decks_outubro.py \\
        [docs/Apresentacoes_IVS/complementos/Guia_Apoio_Cronologia_e_Demandas.pdf]
"""
from __future__ import annotations

import glob
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from datetime import date
from pathlib import Path

import pandas as pd
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
import guia_outubro_base as TXT_BASE          # noqa: E402
import guia_outubro_cronologia as TXT_CRONO   # noqa: E402
import guia_outubro_demandas as TXT_DEM       # noqa: E402

COMP = RAIZ / "docs" / "Apresentacoes_IVS" / "complementos"
DECKS = {"cronologia": COMP / "Cronologia_Projeto_IVS_2026-10.pptx",
         "demandas": COMP / "Demandas_Setembro_IVS_2026-10.pptx"}
DECK_ATUAL = RAIZ / "docs" / "Apresentacoes_IVS" / "Analise_Fatorial_NB04_2026-09.pptx"
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else COMP / "Guia_Apoio_Cronologia_e_Demandas.pdf"
FA = RAIZ / "banco_de_dados" / "eda" / "fatorial_ampliada"
IE = RAIZ / "banco_de_dados" / "eda" / "ivs_especificacoes"
ENTREGA = RAIZ / "banco_de_dados" / "entrega_orientadora"

# Paleta: a mesma de gerar_pdf_guia_fatorial.py, para os guias parecerem do mesmo projeto.
TINTA = colors.HexColor("#1A1A1A")
PETROL = colors.HexColor("#1F4E4A")
CLAY = colors.HexColor("#A83A2C")
CINZA = colors.HexColor("#666666")
LINHA = colors.HexColor("#C8C8C8")
FUNDO = colors.HexColor("#F2F0EC")


# ── fontes ───────────────────────────────────────────────────────────────────
def registrar_fontes():
    """STIX (a Times que vem no matplotlib, com grego e símbolos: Φ, Δ, ≥, ×) no texto, e
    DejaVu Sans nos rótulos. As fontes padrão do PDF não têm esses símbolos."""
    pastas = glob.glob(str(RAIZ / ".venv" / "lib" / "python*" / "site-packages" / "matplotlib"
                           / "mpl-data" / "fonts" / "ttf"))
    pastas += glob.glob(str(RAIZ / ".venv" / "Lib" / "site-packages" / "matplotlib" / "mpl-data"
                            / "fonts" / "ttf"))
    try:
        import matplotlib
        pastas.append(str(Path(matplotlib.get_data_path()) / "fonts" / "ttf"))
    except ImportError:
        pass
    for pasta in map(Path, pastas):
        if (pasta / "STIXGeneral.ttf").exists():
            arquivos = {"Serif": "STIXGeneral.ttf", "Serif-B": "STIXGeneralBol.ttf",
                        "Serif-I": "STIXGeneralItalic.ttf", "Serif-BI": "STIXGeneralBolIta.ttf",
                        "Sans": "DejaVuSans.ttf", "Sans-B": "DejaVuSans-Bold.ttf",
                        "Sans-I": "DejaVuSans-Oblique.ttf", "Sans-BI": "DejaVuSans-BoldOblique.ttf",
                        "Mono": "DejaVuSansMono.ttf"}
            for nome, arq in arquivos.items():
                pdfmetrics.registerFont(TTFont(nome, str(pasta / arq)))
            break
    else:
        raise SystemExit("Fontes STIX/DejaVu não encontradas: crie o ambiente (.venv) do projeto, "
                         "que traz o matplotlib.")
    pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I",
                                  boldItalic="Serif-BI")
    pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I",
                                  boldItalic="Sans-BI")


# ── formatação brasileira ────────────────────────────────────────────────────
def br(x, casas=2):
    return f"{float(x):.{casas}f}".replace(".", ",")


def mil(x):
    return f"{int(round(float(x))):,}".replace(",", ".")


def reais(x):
    return "R$ " + f"{float(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def dm(iso):
    return f"{iso[8:10]}/{iso[5:7]}"


def dma(iso):
    return f"{dm(iso)}/{iso[:4]}"


class Numeros(dict):
    """Dicionário com acesso por atributo: os textos escrevem {N.kmo}, não {N['kmo']}."""
    def __getattr__(self, nome):
        try:
            return self[nome]
        except KeyError:
            raise AttributeError(f"número '{nome}' não calculado em numeros()") from None


# ── os números, lidos dos arquivos ───────────────────────────────────────────
def git(*args):
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True,
                          check=True).stdout


def numeros() -> Numeros:
    N = Numeros()
    hoje = date.today()
    N["hoje"] = hoje.strftime("%d/%m/%Y")

    # git: datas, contagens, tipos
    log = git("log", "--reverse", "--date=short", "--format=%ad").split()
    cont = Counter(log)
    N["commits"], N["primeiro"], N["ultimo"] = str(len(log)), dma(log[0]), dma(log[-1])
    N["top5"] = " · ".join(f"{dm(d)} ({n})" for d, n in cont.most_common(5))
    N["c_25set"] = str(cont.get("2026-09-25", 0))
    entre = lambda a, b: str(sum(a <= d <= b for d in log))  # noqa: E731
    for k, (a, b) in {"marabr": ("2026-03-01", "2026-04-30"), "mai": ("2026-05-01", "2026-05-31"),
                      "jun": ("2026-06-01", "2026-06-30"), "jul": ("2026-07-01", "2026-07-31"),
                      "ago": ("2026-08-01", "2026-08-31"), "set1": ("2026-09-01", "2026-09-17"),
                      "set2": ("2026-09-18", "2026-09-30"), "out": ("2026-10-01", "2026-10-31")}.items():
        N[f"c_{k}"] = entre(a, b)
    tipos = Counter()
    for msg in git("log", "--format=%s").splitlines():
        m = re.match(r"^([A-Za-z]+)(\([^)]*\))?!?:", msg)
        t = m.group(1).lower() if m else ("merge" if msg.lower().startswith("merge") else "sem prefixo")
        tipos[{"teste": "test", "dados": "data"}.get(t, t)] += 1
    for t in ["docs", "feat", "fix", "chore", "data", "test", "refactor"]:
        N[f"t_{t}"] = str(tipos[t])
    N["t_sem"] = str(tipos["sem prefixo"])

    # linha de base do NB04 (a coluna origem pode ter ';' — só as duas primeiras importam)
    B = {}
    for linha in (FA / "linha_de_base_nb04.csv").read_text(encoding="utf-8-sig").strip().splitlines()[1:]:
        partes = linha.split(";")
        B[partes[0]] = float(partes[1])
    N["kmo"], N["msa_min"] = br(B["kmo"], 4), br(B["msa_minimo"], 4)
    N["bartlett"] = mil(B["bartlett_qui2"])
    N["p_soc"], N["p_san"] = br(B["pesos_ivs6_varimax_socioeconomica"]), br(B["pesos_ivs6_varimax_saneamento"])
    N["p_soc1"], N["p_san1"] = br(B["pesos_ivs6_varimax_socioeconomica"], 1), br(B["pesos_ivs6_varimax_saneamento"], 1)
    N["phi"], N["auc_ind"] = br(B["phi_promax"], 4), br(B["auc_indice"], 4)
    N["auc_renda"], N["auc_postos"] = br(B["auc_renda_invertida_sozinha"], 4), br(B["auc_media_postos_pesos_iguais"], 4)
    N["p_sem_sp"] = br(B["pesos_sem_sao_paulo"])

    # cenários da fatorial ampliada
    C = pd.read_csv(FA / "cenarios.csv", sep=";", encoding="utf-8-sig").set_index("cenario")
    for c in C.index:
        k = c.lower()
        N[f"{k}_n"], N[f"{k}_p"] = mil(C.at[c, "n"]), str(int(C.at[c, "p"]))
        N[f"{k}_kmo"], N[f"{k}_msa"] = br(C.at[c, "kmo"], 3), br(C.at[c, "msa_min"], 3)
        N[f"{k}_k"], N[f"{k}_h"] = str(int(C.at[c, "fatores_kaiser"])), str(int(C.at[c, "fatores_horn"]))
        N[f"{k}_var2"] = br(C.at[c, "var_explicada_2f"], 1)
        perd = C.at[c, "perdidos_vs_S0"]
        N[f"{k}_perd"] = mil(perd) if pd.notna(perd) else "0"
    V = pd.read_csv(FA / "validacao_fcu.csv", sep=";", encoding="utf-8-sig")
    M_IND, M_REN, M_POS = "indice_01 (pesos Varimax)", "renda invertida sozinha", "media simples de postos"
    piv = V.pivot_table(index="cenario", columns="medida", values="auc")
    for c in piv.index:
        k = c.lower()
        N[f"auc_{k}"], N[f"aucr_{k}"], N[f"aucp_{k}"] = (br(piv.at[c, M_IND], 4), br(piv.at[c, M_REN], 4),
                                                         br(piv.at[c, M_POS], 4))
    vence = piv[M_REN] > piv[M_IND]
    N["renda_vence"], N["n_cen"] = str(int(vence.sum())), str(len(piv))
    N["renda_perde_em"] = " e ".join(piv.index[~vence].str.replace("_", " "))
    s1 = V[(V.cenario == "S1") & (V.medida == M_IND)].iloc[0]
    N["fcu_s1"], N["nfcu_s1"] = mil(s1.n_fcu), mil(s1.n - s1.n_fcu)
    R3 = ["S0", "S0_renda_sem_extremo", "S0_renda_mediana_mun"]
    N["dif_kmo"] = br(max(C.loc[R3, "kmo"]) - min(C.loc[R3, "kmo"]), 5)
    N["dif_auc"] = br(max(piv.loc[R3, M_IND]) - min(piv.loc[R3, M_IND]), 4)
    P = pd.read_csv(FA / "pesos.csv", sep=";", encoding="utf-8-sig")
    for c in ["S0", "S1", "S6", "S7"]:
        for r in ["sem_rotacao", "varimax", "promax_padrao", "promax_estrutura"]:
            x = P[(P.cenario == c) & (P.rotacao == r)].iloc[0]
            N[f"pw_{c.lower()}_{r}"] = f"{br(x.peso_f1, 1)} / {br(x.peso_f2, 1)}"
        N[f"phi_{c.lower()}"] = br(P[(P.cenario == c) & (P.rotacao == "promax_padrao")].phi.iloc[0], 3)
    semrot = P[(P.rotacao == "sem_rotacao") & P.cenario.isin(["S0", "S1", "S6", "S7"])].peso_f1
    N["semrot_min"], N["semrot_max"] = br(semrot.min(), 1), br(semrot.max(), 1)
    K = pd.read_csv(FA / "cargas.csv", sep=";", encoding="utf-8-sig")
    nc = K[(K.cenario == "S5") & (K.variavel == "pct_moradia_nao_convencional")].iloc[0]
    N["nc_h2"], N["nc_zeros"], N["nc_msa"] = br(nc.comunalidade, 3), br(nc.pct_zeros, 1), br(nc.msa, 3)
    N["nc_carga"] = br(max(abs(nc.varimax_f1), abs(nc.varimax_f2)), 3)
    lx = K[(K.cenario == "S0") & (K.variavel == "pct_lixo_inad")].iloc[0]
    N["lixo_s0_f2"], N["lixo_s0_h2"] = br(lx.varimax_f2, 3), br(lx.comunalidade, 3)
    S = pd.read_csv(FA / "sensibilidade_municipios.csv", sep=";", encoding="utf-8-sig")
    for c in ["S0", "S1", "S6"]:
        x = S[S.cenario == c]
        i = x.delta_varimax.abs().idxmax()
        N[f"sens_{c.lower()}"], N[f"sens_{c.lower()}_mun"] = br(abs(x.at[i, "delta_varimax"])), x.at[i, "municipio_fora"]
        N[f"lixo_muda_{c.lower()}"] = str(int(x.lixo_muda.astype(str).str.lower().eq("true").sum()))
    N["sens_max"] = br(max(S.delta_varimax.abs().max(), S.delta_promax_padrao.abs().max()))
    N["rodadas"] = str(int((S.cenario == "S0").sum()))

    # renda: o setor extremo e as alternativas de imputação
    arq_bh = ENTREGA / "Base_BeloHorizonte_Censo2022.csv"
    sep_bh = ";" if ";" in arq_bh.open(encoding="utf-8-sig").readline() else ","
    bh = pd.read_csv(arq_bh, sep=sep_bh, encoding="utf-8-sig", usecols=["CD_SETOR", "renda_media"],
                     dtype={"CD_SETOR": str})
    N["renda_extremo"] = reais(bh.loc[bh.CD_SETOR == "310620005650366", "renda_media"].iloc[0])
    I = pd.read_csv(RAIZ / "banco_de_dados" / "eda" / "atualizada" / "renda_imputacao_alternativas.csv",
                    sep=";", encoding="utf-8-sig").set_index("alternativa")
    N["med_bh"] = reais(I.at["mediana de BH sem o setor", "valor_imputado"])
    N["med_bh_com"] = reais(I.at["mediana de BH com o setor", "valor_imputado"])
    N["med_70"] = reais(I.at["mediana dos 70 municípios sem o setor", "valor_imputado"])
    N["bh_media"], N["bh_dp"] = reais(I.at["mediana de BH sem o setor", "bh_media"]), reais(I.at["mediana de BH sem o setor", "bh_dp"])
    N["bh_max"] = reais(I.at["mediana de BH sem o setor", "bh_max"])

    # entrega, quadro e banheiro
    Q = pd.read_csv(ENTREGA / "Quadro_Indicadores.csv", sep=None, engine="python", encoding="utf-8-sig")
    N["n_ind"], N["n_ind_ivs7"] = str(len(Q)), str(int((Q.entra_no_ivs7 == "Sim").sum()))
    N["quadro"] = [[f"`{r.indicador}`", r.dimensao, r.entra_no_ivs7, r.o_que_mede] for r in Q.itertuples()]
    for dim, k in [("Saneamento", "san"), ("Socioeconômica", "soc"), ("Morfologia", "morf"), ("Demografia", "dem")]:
        N[f"q_{k}"] = str(int((Q.dimensao == dim).sum()))
    cab = (ENTREGA / "Base_ELSI_70Municipios_Censo2022.csv").open(encoding="utf-8-sig").readline()
    N["n_cols"] = str(len(cab.split(";" if ";" in cab else ",")))
    BP = pd.read_csv(FA / "banheiro_particao.csv", sep=";", encoding="utf-8-sig",
                     usecols=["V00238", "V00495", "bate_com_v00495"])
    bate = BP.bate_com_v00495.astype(str).str.lower()
    pres = bate.isin(["true", "false"])
    N["setores_base"], N["part_pres"] = mil(len(BP)), mil(pres.sum())
    N["part_bate"], N["part_aus"] = mil((bate == "true").sum()), mil(len(BP) - pres.sum())
    amb = BP.dropna(subset=["V00238", "V00495"])
    N["juncao_n"], N["juncao_vale"] = mil(len(amb)), mil((amb.V00238 <= amb.V00495).sum())

    # a grade do NB05
    E = pd.read_csv(IE / "especificacoes.csv")
    el = E[E.elegivel]
    REF = pd.read_csv(IE / "referencia.csv").set_index("leitura")
    ref = REF.loc["principal"]
    N["n_esp"], N["n_eleg"] = str(len(E)), str(len(el))
    N["n_bases"], N["n_esq"] = str(E.groupby(["renda", "lixo", "banheiro"]).ngroups), str(E.groupby(["rotacao", "metodo"]).ngroups)
    N["n_eleg_mun"] = str(int((el.normalizacao == "municipal").sum()))
    N["n_mun_total"] = str(int((E.normalizacao == "municipal").sum()))
    conta = lambda m: f"{int((E.elegivel & m).sum())} de {int(m.sum())}"  # noqa: E731
    N["eleg_semrot"], N["eleg_vari"], N["eleg_prom"] = (conta(E.rotacao == "sem_rotacao"),
                                                       conta(E.rotacao == "varimax"), conta(E.rotacao == "promax"))
    N["eleg_lixo_com"], N["eleg_lixo_sem"] = conta(E.lixo == "com"), conta(E.lixo == "sem")
    N["eleg_b_fora"], N["eleg_b_v495"], N["eleg_b_grad"] = (conta(E.banheiro == "fora"),
                                                           conta(E.banheiro == "v00495"), conta(E.banheiro == "graduado"))
    N["eleg_esquema"] = conta((E.rotacao == "promax") & (E.metodo == "ss_padrao"))
    N["eleg_base"] = conta((E.renda == "original") & (E.lixo == "sem") & (E.banheiro == "fora"))

    def comun(lixo, banheiro):
        r = E[(E.renda == "original") & (E.lixo == lixo) & (E.banheiro == banheiro)
              & (E.rotacao == "varimax") & (E.metodo == "ss")].iloc[0]
        return br(r.comunalidade_min, 3), str(r.comunalidade_min_variavel).lower()
    (N["h2_agua"], _), (N["h2_grad"], _) = comun("com", "fora"), comun("com", "graduado")
    (N["h2_v495"], N["h2_v495_var"]), (N["h2_sem"], N["h2_sem_var"]) = comun("com", "v00495"), comun("sem", "fora")
    for r in ["original", "sem_extremo", "mediana_mun"]:
        N[f"auc_r_{r}"] = br(el[el.renda == r].auc_mun_comum.mean(), 4)
    PS = pd.read_csv(IE / "pesos.csv")
    pr = PS[(PS.renda == ref.renda) & (PS.lixo == ref.lixo) & (PS.banheiro == ref.banheiro)]
    pega = lambda rot, met: br(pr[(pr.rotacao == rot) & (pr.metodo == met)].peso_f1.iloc[0], 1)  # noqa: E731
    N["ref_vari_ss"], N["ref_pad"] = pega("varimax", "ss"), pega("promax", "ss_padrao")
    N["ref_est"], N["ref_com"] = pega("promax", "ss_estrutura"), pega("promax", "comunalidades")
    A = pd.read_csv(IE / "acrescimo_renda.csv")
    Ar = A[A.referencia].iloc[0]
    N["acr_n"] = str(len(A))
    N["acr_rg"] = str(int((A.auc_renda_global > A.auc_indice_global).sum()))
    N["acr_rm"] = str(int((A.auc_renda_mun > A.auc_indice_mun).sum()))
    N["acr_ie"] = str(int((A.auc_indice_estratos > A.auc_renda_estratos).sum()))
    N["z_min"], N["z_max"] = br(A.z_indice.min(), 1), br(A.z_indice.max(), 1)
    N["ganho_max"] = br((A.auc_modelo_renda_indice - A.auc_modelo_renda).max(), 4)
    for col, k in [("auc_indice_global", "ig"), ("auc_renda_global", "rg"), ("auc_indice_mun", "im"),
                   ("auc_renda_mun", "rm"), ("auc_indice_estratos", "ie"), ("auc_renda_estratos", "re"),
                   ("auc_modelo_renda", "mod"), ("auc_modelo_renda_indice", "mod2")]:
        N[f"ref_{k}"] = br(Ar[col], 4)
    N["ref_dev"], N["ref_z"] = br(Ar.queda_deviance, 1), br(Ar.z_indice, 1)
    N["ref_n"] = mil(E[E.id == ref.id].n.iloc[0])
    N["ref_amp"] = br(E[E.id == ref.id].amp_peso_f1.iloc[0], 1)
    N["ref_eleg"] = str(int(ref.elegiveis))
    for leitura, k in [("principal", "pri"), ("amostra_propria", "pro"),
                       ("estabilidade_pesos_variaveis", "est"), ("normalizacao_global", "glo")]:
        N[f"posto_{k}"] = br(REF.at[leitura, "posto_medio"], 1)
    av = pd.read_csv(IE / "avaliacao.csv")
    g = av[(av.id == ref.id.replace("municipal", "global")) & (av.amostra == "comum")].iloc[0]
    N["muda_bh"], N["muda_q"], N["spearman_g"] = br(g.muda_faixa_ivs_bh, 1), br(g.muda_faixa_quartis, 1), br(g.spearman_ref, 3)
    for rid, k in [(ref.id.replace("municipal", "global"), "glo"),
                   ("original·lixo_com·banheiro_fora·varimax·ss·municipal", "nb04"),
                   ("original·lixo_sem·banheiro_fora·varimax·ss·municipal", "semlixo"),
                   (REF.at["estabilidade_pesos_variaveis", "id"], "est")]:
        r = av[(av.id == rid) & (av.amostra == "comum")].iloc[0]
        N[f"conc_{k}"] = br(100 - r.muda_faixa_ivs_bh, 1)
    X = pd.read_csv(IE / "ivs_referencia_por_setor.csv", usecols=["faixa_ivs_bh", "faixa_quartis"])
    FX = ["baixo", "medio", "elevado", "muito_elevado"]
    for col, k in [("faixa_ivs_bh", "bh"), ("faixa_quartis", "q")]:
        vc = X[col].value_counts()
        for f in FX:
            N[f"fx_{k}_{f}"] = mil(vc.get(f, 0))
            N[f"fx_{k}_{f}_pct"] = br(100 * vc.get(f, 0) / len(X), 1)
        N[f"fx_{k}_indef"] = mil(len(X) - sum(vc.get(f, 0) for f in FX))
    N["fx_total"] = mil(len(X))

    # grafo, decks e testes
    G = json.loads((RAIZ / "graphify-out" / "graph.json").read_text(encoding="utf-8"))
    N["g_nos"], N["g_arestas"] = mil(len(G["nodes"])), mil(len(G.get("links", G.get("edges", []))))
    N["g_com"] = str(len({n.get("community") for n in G["nodes"] if n.get("community") is not None}))
    contar = lambda p: sum(bool(re.match(r"ppt/slides/slide\d+\.xml$", n)) for n in zipfile.ZipFile(p).namelist())  # noqa: E731
    N["slides_atual"] = str(contar(DECK_ATUAL))
    N["slides_crono"], N["slides_dem"] = str(contar(DECKS["cronologia"])), str(contar(DECKS["demandas"]))
    N["n_historico"] = str(len(list((RAIZ / "docs" / "Apresentacoes_IVS" / "historico").glob("*.pptx"))))
    try:
        saida = subprocess.run([str(RAIZ / ".venv" / "bin" / "python"), "-m", "pytest", "--collect-only", "-q"],
                               cwd=RAIZ, capture_output=True, text=True, timeout=300).stdout
        N["testes"] = re.search(r"(\d+) tests? collected", saida).group(1)
    except (OSError, AttributeError, subprocess.TimeoutExpired):
        N["testes"] = str(sum(len(re.findall(r"^\s*def test_", f.read_text(encoding="utf-8"), re.M))
                              for f in (RAIZ / "tests").glob("*.py")))
    return N


# ── os slides: textos (para conferir) e PDFs (para as miniaturas) ────────────
def textos_dos_slides(pptx: Path) -> list[str]:
    z = zipfile.ZipFile(pptx)
    nomes = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                   key=lambda s: int(re.findall(r"\d+", s)[0]))
    return [html.unescape(" ".join(re.findall(r"<a:t>([^<]*)</a:t>", z.read(n).decode("utf-8"))))
            for n in nomes]


def decks_em_pdf(pasta: Path) -> dict:
    """Converte os dois decks em PDF com o LibreOffice; devolve {} se ele não estiver instalado."""
    soffice = (shutil.which("soffice") or shutil.which("libreoffice")
               or next((p for p in ["/Applications/LibreOffice.app/Contents/MacOS/soffice"] if Path(p).exists()), None))
    if not soffice:
        print("aviso: LibreOffice não encontrado — o guia sai sem as miniaturas dos slides")
        return {}
    perfil = (pasta / "perfil_lo").resolve()
    leitores = {}
    for nome, pptx in DECKS.items():
        subprocess.run([soffice, f"-env:UserInstallation={perfil.as_uri()}", "--headless",
                        "--convert-to", "pdf", "--outdir", str(pasta), str(pptx)],
                       check=True, capture_output=True, timeout=600)
        leitores[nome] = PdfReader(str(pasta / (pptx.stem + ".pdf")))
    return leitores


# ── estilos e peças de página ────────────────────────────────────────────────
def estilos():
    base = dict(fontName="Serif", fontSize=10.5, leading=14.6, textColor=TINTA)
    E = {
        "corpo": ParagraphStyle("corpo", alignment=TA_JUSTIFY, spaceAfter=6, **base),
        "lista": ParagraphStyle("lista", alignment=TA_LEFT, leftIndent=14, bulletIndent=3,
                                spaceAfter=3, **base),
        "rotulo": ParagraphStyle("rotulo", fontName="Sans-B", fontSize=7.6, leading=10,
                                 textColor=CLAY, spaceBefore=9, spaceAfter=3),
        "sobre": ParagraphStyle("sobre", fontName="Sans-B", fontSize=7.6, leading=10,
                                textColor=CLAY, spaceAfter=1),
        "verbete": ParagraphStyle("verbete", fontName="Serif-B", fontSize=15.5, leading=19,
                                  textColor=TINTA, spaceAfter=6),
        "secao": ParagraphStyle("secao", fontName="Serif-B", fontSize=15, leading=19,
                                textColor=PETROL, spaceBefore=16, spaceAfter=7),
        "subsecao": ParagraphStyle("subsecao", fontName="Serif-B", fontSize=11.5, leading=15,
                                   textColor=TINTA, spaceBefore=9, spaceAfter=4),
        "parte": ParagraphStyle("parte", fontName="Serif-B", fontSize=30, leading=36,
                                textColor=PETROL, spaceAfter=10),
        "parte_sub": ParagraphStyle("parte_sub", fontName="Serif-I", fontSize=13, leading=18,
                                    textColor=CINZA, spaceAfter=18),
        "frase": ParagraphStyle("frase", fontName="Serif-I", fontSize=11.5, leading=15.5,
                                textColor=PETROL),
        "caixa": ParagraphStyle("caixa", fontName="Serif", fontSize=10, leading=13.8,
                                textColor=TINTA, alignment=TA_JUSTIFY, spaceAfter=4),
        "pergunta": ParagraphStyle("pergunta", fontName="Serif-B", fontSize=10, leading=13.8,
                                   textColor=TINTA, spaceAfter=1),
        "celula": ParagraphStyle("celula", fontName="Serif", fontSize=9.2, leading=11.8, textColor=TINTA),
        "celula_cab": ParagraphStyle("celula_cab", fontName="Serif-B", fontSize=9.2, leading=11.8,
                                     textColor=TINTA),
        "termo": ParagraphStyle("termo", fontName="Serif", fontSize=10.2, leading=14,
                                textColor=TINTA, alignment=TA_JUSTIFY, spaceAfter=5,
                                leftIndent=12, firstLineIndent=-12),
        "capa_t": ParagraphStyle("capa_t", fontName="Serif-B", fontSize=32, leading=38,
                                 textColor=TINTA, spaceAfter=14),
        "capa_s": ParagraphStyle("capa_s", fontName="Serif", fontSize=14, leading=20,
                                 textColor=CINZA, spaceAfter=10),
        "capa_k": ParagraphStyle("capa_k", fontName="Sans-B", fontSize=8.5, leading=12,
                                 textColor=CLAY, spaceAfter=10),
        "sumario0": ParagraphStyle("sumario0", fontName="Serif-B", fontSize=11.5, leading=16,
                                   textColor=PETROL, spaceBefore=8),
        "sumario1": ParagraphStyle("sumario1", fontName="Serif", fontSize=9.6, leading=12.6,
                                   textColor=TINTA, leftIndent=16),
    }
    return E


EST = None


def marcar(texto: str) -> str:
    """`código` vira monoespaçada; o resto é o mini-HTML do reportlab (<b>, <i>). Caminho longo
    não vaza da margem: o reportlab quebra palavra maior que a linha (splitLongWords)."""
    return re.sub(r"`([^`]+)`", lambda m: f'<font name="Mono" size="8.6">{m.group(1)}</font>', texto)


def paragrafos(texto: str, estilo="corpo") -> list:
    """Parágrafos separados por linha em branco. Linha que começa com '• ' abre um item de
    lista; as linhas seguintes, sem marcador, continuam o mesmo item."""
    saida = []
    for bloco in texto.strip().split("\n\n"):
        linhas = [l.strip() for l in bloco.strip().split("\n")]
        if any(l.startswith("• ") for l in linhas):
            intro, itens = [], []
            for l in linhas:
                if l.startswith("• "):
                    itens.append(l[2:])
                elif itens:
                    itens[-1] += " " + l
                else:
                    intro.append(l)
            if intro:
                saida.append(Paragraph(marcar(" ".join(intro)), EST[estilo]))
            saida += [Paragraph(marcar(i), EST["lista"], bulletText="•") for i in itens]
        else:
            saida.append(Paragraph(marcar(" ".join(linhas)), EST[estilo]))
    return saida


def caixa(conteudo: list, cor=PETROL, fundo=FUNDO, barra=2.2):
    t = Table([[conteudo]], colWidths=[None])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fundo),
                           ("LINEBEFORE", (0, 0), (0, -1), barra, cor),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def tabela(cab, linhas, larguras_cm):
    # Na célula, o código fica um ponto menor que no texto corrido: coluna estreita.
    cel = lambda c: marcar(str(c)).replace('size="8.6"', 'size="7.8"')  # noqa: E731
    dados = [[Paragraph(cel(c), EST["celula_cab"]) for c in cab]]
    dados += [[Paragraph(cel(c), EST["celula"]) for c in ln] for ln in linhas]
    t = Table(dados, colWidths=[w * cm for w in larguras_cm], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 1.0, TINTA),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, TINTA),
                           ("LINEBELOW", (0, -1), (-1, -1), 1.0, TINTA),
                           ("LINEBELOW", (0, 1), (-1, -2), 0.3, LINHA),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


POSICOES: dict = {}
TEM_MINIATURAS = False


class Miniatura(Flowable):
    """Reserva o espaço do slide e anota onde ficou; a página do slide entra depois, pelo pypdf."""

    def __init__(self, deck: str, n: int, largura: float):
        super().__init__()
        self.deck, self.n = deck, n
        self.width, self.height = largura, largura * 540 / 960
        self.hAlign = "CENTER"

    def wrap(self, *_):
        return self.width, self.height

    def draw(self):
        c = self.canv
        x, y = c.absolutePosition(0, 0)
        POSICOES[(self.deck, self.n)] = (c.getPageNumber() - 1, x, y, self.width)
        c.saveState()
        c.setStrokeColor(LINHA)
        c.setLineWidth(0.6)
        c.rect(0, 0, self.width, self.height)
        if not TEM_MINIATURAS:
            c.setFont("Sans", 9)
            c.setFillColor(CINZA)
            c.drawCentredString(self.width / 2, self.height / 2, f"[slide {self.n}]")
        c.restoreState()


def marca_sumario(flowable, texto: str, nivel: int, parte: str | None = None):
    flowable._sumario = (texto, nivel)
    if parte:
        flowable._parte = parte
    return flowable


class Guia(BaseDocTemplate):
    def __init__(self, arquivo, **kw):
        super().__init__(arquivo, pagesize=A4, leftMargin=2.3 * cm, rightMargin=2.3 * cm,
                         topMargin=2.3 * cm, bottomMargin=2.0 * cm, **kw)
        quadro = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="q",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="capa", frames=[quadro]),
                               PageTemplate(id="corpo", frames=[quadro], onPageEnd=self.moldura)])
        self.parte_atual = ""

    def beforeDocument(self):
        self._n_marcas = 0
        self.parte_atual = ""

    def afterFlowable(self, f):
        if getattr(f, "_parte", None):
            self.parte_atual = f._parte
        if getattr(f, "_sumario", None):
            texto, nivel = f._sumario
            self._n_marcas += 1
            chave = f"m{self._n_marcas}"
            self.canv.bookmarkPage(chave)
            self.canv.addOutlineEntry(texto, chave, level=nivel, closed=nivel == 0)
            self.notify("TOCEntry", (nivel, texto, self.page, chave))

    def moldura(self, c, doc):
        c.saveState()
        larg, alt = A4
        c.setFont("Sans", 7.6)
        c.setFillColor(CINZA)
        c.drawString(doc.leftMargin, alt - 1.45 * cm, "Guia de apoio · Cronologia do projeto e Demandas de setembro")
        c.drawRightString(larg - doc.rightMargin, alt - 1.45 * cm, self.parte_atual)
        c.setStrokeColor(LINHA)
        c.setLineWidth(0.5)
        c.line(doc.leftMargin, alt - 1.6 * cm, larg - doc.rightMargin, alt - 1.6 * cm)
        c.setFont("Serif", 9)
        c.drawCentredString(larg / 2, 1.15 * cm, str(c.getPageNumber()))
        c.restoreState()


# ── montagem ─────────────────────────────────────────────────────────────────
def render_blocos(blocos: list, parte: str, nivel: int = 1) -> list:
    """Blocos de texto corrido: ('secao', t) · ('subsecao', t) · ('p', texto) ·
    ('caixa', titulo, texto) · ('exemplo', titulo, texto) · ('tabela', cab, linhas, larguras)."""
    s = []
    for b in blocos:
        tipo = b[0]
        if tipo == "secao":
            s.append(CondPageBreak(5 * cm))
            s.append(marca_sumario(Paragraph(b[1], EST["secao"]), b[1], nivel, parte))
        elif tipo == "subsecao":
            s.append(Paragraph(b[1], EST["subsecao"]))
        elif tipo == "p":
            s += paragrafos(b[1])
        elif tipo in ("caixa", "exemplo"):
            cor = PETROL if tipo == "caixa" else CLAY
            dentro = [Paragraph(b[1].upper(), EST["sobre"] if tipo == "exemplo" else
                                ParagraphStyle("c", parent=EST["sobre"], textColor=PETROL))]
            dentro += paragrafos(b[2], "caixa")
            s += [Spacer(1, 3), caixa(dentro, cor), Spacer(1, 8)]
        elif tipo == "tabela":
            s += [Spacer(1, 3), tabela(b[1], b[2], b[3]), Spacer(1, 9)]
        else:
            raise ValueError(f"bloco desconhecido: {tipo}")
    return s


def abrir_parte(letra: str, titulo: str, sub: str, abertura: str, rotulo: str) -> list:
    t = marca_sumario(Paragraph(f"Parte {letra} — {titulo}", EST["parte"]), f"Parte {letra} — {titulo}", 0, rotulo)
    return [PageBreak(), Spacer(1, 3.2 * cm), t, Paragraph(sub, EST["parte_sub"])] + paragrafos(abertura)


SECOES_VERBETE = [("mostra", "O que aparece no slide"), ("zero", "O que isso quer dizer, do zero"),
                  ("numeros", "Como ler os números"), ("apresentar", "Como apresentar")]


def verbete(deck: str, rotulo_deck: str, v: dict) -> list:
    titulo = v.get("titulo_guia") or v["titulo"]
    cab = Paragraph(f"{rotulo_deck.upper()} · SLIDE {v['n']}", EST["sobre"])
    tit = marca_sumario(Paragraph(titulo, EST["verbete"]), f"{v['n']}. {titulo}", 1)
    topo = [cab, tit, Miniatura(deck, v["n"], 13.6 * cm), Spacer(1, 9),
            caixa([Paragraph(marcar(v["frase"]), EST["frase"])], PETROL), Spacer(1, 2)]
    s = [CondPageBreak(14.5 * cm), KeepTogether(topo)]
    for chave, rotulo in SECOES_VERBETE:
        if v.get(chave):
            s.append(Paragraph(rotulo.upper(), EST["rotulo"]))
            s += paragrafos(v[chave])
        if chave == "zero" and v.get("tabela"):
            cab, linhas, larguras = v["tabela"]
            s += [Spacer(1, 3), tabela(cab, linhas, larguras), Spacer(1, 6)]
    if v.get("perguntas"):
        dentro = [Paragraph("SE PERGUNTAREM", EST["sobre"])]
        for q, r in v["perguntas"]:
            dentro.append(Paragraph(marcar(q), EST["pergunta"]))
            dentro += paragrafos(r, "caixa")
        s += [Spacer(1, 6), caixa(dentro, CLAY)]
    s.append(Spacer(1, 14))
    return s


def conferir(verbetes: list, textos: list[str], nome: str):
    erros = []
    if [v["n"] for v in verbetes] != list(range(1, len(textos) + 1)):
        erros.append(f"{nome}: os verbetes não cobrem os slides 1–{len(textos)} em ordem")
    for v in verbetes:
        if 1 <= v["n"] <= len(textos) and v["titulo"] not in textos[v["n"] - 1]:
            erros.append(f"{nome}, slide {v['n']}: título '{v['titulo']}' não está no slide")
    if erros:
        raise SystemExit("O guia não corresponde aos decks:\n  " + "\n  ".join(erros))


def main():
    global EST, TEM_MINIATURAS
    registrar_fontes()
    EST = estilos()
    N = numeros()
    vc, vd = TXT_CRONO.verbetes(N), TXT_DEM.verbetes(N)
    conferir(vc, textos_dos_slides(DECKS["cronologia"]), "cronologia")
    conferir(vd, textos_dos_slides(DECKS["demandas"]), "demandas")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pdfs = decks_em_pdf(tmp)
        TEM_MINIATURAS = bool(pdfs)

        hist = [Spacer(1, 4.5 * cm), Paragraph("PROJETO IVS · CENSO 2022 · FIOCRUZ MINAS — INSTITUTO RENÉ RACHOU", EST["capa_k"]),
                Paragraph("Guia das apresentações de outubro, explicado do zero", EST["capa_t"]),
                Paragraph(f"A cronologia do projeto ({N.slides_crono} slides) e as demandas de setembro "
                          f"({N.slides_dem} slides): o que cada slide mostra, o que cada termo quer dizer, "
                          "como ler os números e o que responder se perguntarem.", EST["capa_s"]),
                Spacer(1, 1.2 * cm),
                Paragraph(f"Pedro Dias Soares · Iniciação Científica · gerado em {N.hoje}", EST["capa_s"]),
                NextPageTemplate("corpo"), PageBreak()]
        historia = hist
        historia += render_blocos(TXT_BASE.como_usar(N), "Como usar", nivel=0)
        sumario = TableOfContents(dotsMinLevel=1)
        sumario.levelStyles = [EST["sumario0"], EST["sumario1"]]
        historia += [PageBreak(), Paragraph("Sumário", EST["secao"]), sumario]
        historia += abrir_parte("A", "O mínimo para entender tudo", "Leia uma vez, antes dos slides",
                                TXT_BASE.abertura_a(N), "Parte A · O mínimo para entender tudo")
        historia += render_blocos(TXT_BASE.parte_a(N), "Parte A · O mínimo para entender tudo")
        historia += abrir_parte("B", "A cronologia, slide a slide", f"Cronologia_Projeto_IVS_2026-10.pptx · {N.slides_crono} slides",
                                TXT_CRONO.abertura(N), "Parte B · A cronologia")
        for v in vc:
            historia += verbete("cronologia", "Cronologia", v)
        historia += abrir_parte("C", "As demandas de setembro, slide a slide", f"Demandas_Setembro_IVS_2026-10.pptx · {N.slides_dem} slides",
                                TXT_DEM.abertura(N), "Parte C · As demandas de setembro")
        for v in vd:
            historia += verbete("demandas", "Demandas de setembro", v)
        historia += abrir_parte("D", "Glossário", "Os termos dos dois decks, em ordem alfabética",
                                TXT_BASE.abertura_d(N), "Parte D · Glossário")
        for termo, definicao in TXT_BASE.glossario(N):
            historia.append(Paragraph(f"<b>{marcar(termo)}</b> — {marcar(definicao)}", EST["termo"]))
        historia += render_blocos(TXT_BASE.fecho(N), "Parte D · Glossário")

        provisorio = tmp / "guia_sem_miniaturas.pdf"
        doc = Guia(str(provisorio), title="Guia das apresentações de outubro", author="Pedro Dias Soares",
                   subject="Cronologia do projeto IVS e demandas de setembro, explicadas do zero")
        doc.multiBuild(historia)

        escritor = PdfWriter(clone_from=str(provisorio))
        if pdfs:
            for (deck, n), (pagina, x, y, largura) in POSICOES.items():
                slide = pdfs[deck].pages[n - 1]
                escala = largura / float(slide.mediabox.width)
                escritor.pages[pagina].merge_transformed_page(
                    slide, Transformation().scale(escala, escala).translate(x, y))
        SAIDA.parent.mkdir(parents=True, exist_ok=True)
        with open(SAIDA, "wb") as f:
            escritor.write(f)
    print(f"guia escrito: {SAIDA} ({len(PdfReader(str(SAIDA)).pages)} páginas, "
          f"{len(POSICOES)} miniaturas)")


if __name__ == "__main__":
    main()
