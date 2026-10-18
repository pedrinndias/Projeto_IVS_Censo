"""Catálogo de tudo o que a análise exploratória já produziu — tabelas, figuras, decks,
notebooks e relatórios — com a situação de cada item e em que tabelas aparece cada
indicador. Não calcula nada novo: só lê os arquivos que existem e os READMEs que os
descrevem.

    ./.venv/bin/python scripts/gerar_catalogo_analises.py

Saída: docs/relatorios/Catalogo_Analises_Exploratorias.xlsx
"""
import csv
import fnmatch
import re
import subprocess
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
EDA = RAIZ / "banco_de_dados" / "eda"
SAIDA = RAIZ / "docs" / "relatorios" / "Catalogo_Analises_Exploratorias.xlsx"
QUADRO = RAIZ / "banco_de_dados" / "entrega_orientadora" / "Quadro_Indicadores.csv"

# pasta -> (situação, rodada)
PASTAS = {
    EDA: ("ver coluna Situação", "EDA Fase 3 (NB02) e auditorias"),
    EDA / "atualizada": ("Vigente", "EDA 2ª rodada — renda sem o extremo (02/09)"),
    EDA / "fatorial": ("ver coluna Situação", "Análise fatorial — diagnóstico (24/08) e NB04 (17/09)"),
    EDA / "fatorial_ampliada": ("Vigente", "Fatorial ampliada — demandas de setembro (25/09)"),
    EDA / "ivs_especificacoes": ("Vigente", "NB05 — 324 especificações do IVS (27/09)"),
    RAIZ / "banco_de_dados" / "nacional": ("Vigente", "Brasil inteiro — comparação com os 70 municípios"),
}

TEMAS = [  # (tema, padrões no nome do arquivo) — o primeiro que casar vence
    ("Índice e análise fatorial", ["nb04_", "autovalores", "cargas", "pesos", "cenarios", "especificacoes",
                                   "referencia", "estabilidade", "acrescimo_renda", "avaliacao", "linha_de_base",
                                   "resumo_adequabilidade", "_correlacao", "phi_", "bootstrap", "particao",
                                   "sensibilidade_municipios", "comparacao_nao_chega", "correlacao_s6", "ivs_"]),
    ("Favelas e comunidades urbanas (FCU)", ["fcu", "favela"]),
    ("Renda", ["renda", "extremo"]),
    ("Saneamento", ["agua", "esgoto", "lixo", "banheiro", "saneamento", "cobertura"]),
    ("Moradia e domicílio", ["habitacao", "tipo_domicilio", "moradia", "morfologia", "razao_moradores"]),
    ("Envelhecimento e estrutura etária", ["etaria", "envelhecimento"]),
    ("Chefia feminina", ["resp_feminino"]),
    ("Analfabetismo e sigilo", ["analfabetismo"]),
    ("Urbano e rural", ["urbano_rural", "exclusao_rural"]),
    ("Brasil × ELSI", ["brasil", "representatividade", "recorte"]),
    ("Qualidade dos dados", ["missing", "outliers", "elegibilidade", "diagnostico", "fora_intervalo"]),
    ("Panorama dos indicadores", ["descritivas", "correlacao_pearson", "correlacao_spearman", "comparacao_antes"]),
    ("Dados dos decks", ["dados_"]),
]


# arquivos que nenhum README descreve numa tabela
DESCRICOES_EXTRA = {
    "diagnostico_esgoto_312_vs_249.csv": "Diagnóstico do esgoto (NB02, seção 4b): as duas definições de esgoto inadequado comparadas",
    "estrutura_etaria_contagem_por_setor.csv": "Contagens por faixa etária, uma linha por setor (NB02, seção 7e)",
    "resp_feminino_contagem_por_setor.csv": "Responsáveis por sexo (V01062/V01063), uma linha por setor",
    "dados_criterio_renda.json": "Números do deck do critério de outliers de renda (scripts/dados_criterio_renda.py)",
    "dados_deck.json": "Números do deck da EDA Central, 1ª rodada (scripts/eda_central_dados.py)",
    "dados_deck_atualizado.json": "Números do deck da EDA Central, 2ª rodada (scripts/eda_central_dados.py --atualizada)",
    "resumo_adequabilidade.csv": "Uma linha por cenário do diagnóstico fatorial — a referência de conferência dos demais",
    "banheiro_particao.csv": "Conferência de que V00236, V00237 e V00238 particionam o V00495 (base do banheiro graduado)",
    "ivs_referencia_por_setor.csv": "IVS da especificação de referência proposta, uma linha por setor",
}


def git_datas(caminho):
    rel = str(caminho.relative_to(RAIZ))
    out = subprocess.run(["git", "log", "--format=%ad", "--date=short", "--", rel],
                         cwd=RAIZ, capture_output=True, text=True).stdout.split()
    return (out[-1], out[0]) if out else ("", "")


def tema_de(nome):
    n = nome.lower()
    for tema, pads in TEMAS:
        if any(p in n for p in pads):
            return tema
    return "Outros"


def expandir(token):
    """`a_{x,y}.csv` -> [a_x.csv, a_y.csv]."""
    m = re.search(r"\{([^}]*)\}", token)
    if not m:
        return [token]
    return [x for alt in m.group(1).split(",") for x in expandir(token[:m.start()] + alt + token[m.end():])]


def notas_readme(pasta):
    """Lê as tabelas do README da pasta: arquivo (ou padrão) -> (seção, descrição)."""
    leia = pasta / "README.md"
    notas = {}
    if not leia.exists():
        return notas
    secao = ""
    for linha in leia.read_text(encoding="utf-8").splitlines():
        if linha.startswith("#"):
            secao = linha.lstrip("# ").strip()
            continue
        if not linha.startswith("|") or set(linha) <= set("|-: "):
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        tokens = [t for c in celulas for t in re.findall(r"`([^`]+)`", c)
                  if re.search(r"\.(csv|png|svg|json)$|\*|\{", t)]
        prefixos = [t for t in re.findall(r"`([a-z0-9_]{6,})`", celulas[0])]
        if not tokens and prefixos:
            desc = " · ".join(re.sub(r"[`*]", "", c) for c in celulas[1:])
            for t in prefixos:
                notas.setdefault("prefixo:" + t, (secao, desc))
            continue
        if not tokens:
            continue
        com_arquivo = [c for c in celulas if any(f"`{t}`" in c for t in tokens)]
        desc = " · ".join(re.sub(r"[`*]", "", c) for c in celulas if c not in com_arquivo)
        for t in tokens:
            for p in expandir(t.split("/")[-1]):
                notas.setdefault(p, (secao, desc.strip(" ·")))
    return notas


def nota_para(nome, notas):
    if nome in notas:
        return notas[nome]
    for padrao, v in notas.items():
        if "*" in padrao and fnmatch.fnmatch(nome, padrao):
            return v
    prefixos = [k[8:] for k in notas if k.startswith("prefixo:") and nome.startswith(k[8:] + "_")]
    if prefixos:
        return notas["prefixo:" + max(prefixos, key=len)]
    return ("", DESCRICOES_EXTRA.get(nome, ""))


def forma_csv(caminho):
    with open(caminho, encoding="utf-8-sig", errors="replace") as f:
        cab = f.readline()
        sep = ";" if cab.count(";") > cab.count(",") else ","
        cols = next(csv.reader([cab], delimiter=sep))
        linhas = sum(1 for _ in f)
    return sep, cols, linhas


def situacao(pasta, nome, secao):
    if pasta == EDA:
        if (EDA / "atualizada" / nome).exists():
            return "Superado pela 2ª rodada (renda com o extremo)"
        if "gerar_tabelas_auditoria" in secao or "Gerados por [`scripts/gerar_tabelas" in secao:
            return "Vigente — recorte com rurais (106.281 setores)"
        if nome.startswith("dados_deck"):
            return "Insumo de deck"
        return "Vigente"
    if pasta == EDA / "fatorial":
        return "Vigente — NB04" if nome.startswith("nb04_") else "Histórico — diagnóstico de 24/08"
    return PASTAS[pasta][0]


# ------------------------------------------------------------------ tabelas e figuras
indicadores = pd.read_csv(QUADRO, sep=";", encoding="utf-8-sig")
nomes_ind = list(indicadores["indicador"]) + ["renda_media_sem_extremo", "renda_media_mediana_mun", "renda_inv"]
tabelas, figuras = [], []
onde_aparece = {n: [] for n in nomes_ind}
for pasta, (_, rodada) in PASTAS.items():
    notas = notas_readme(pasta)
    for arq in sorted(pasta.glob("*.csv")) + sorted(pasta.glob("*.json")):
        secao, desc = nota_para(arq.name, notas)
        desc = desc or DESCRICOES_EXTRA.get(arq.name, "")
        ini, fim = git_datas(arq)
        linha = dict(pasta=str(pasta.relative_to(RAIZ)), arquivo=arq.name, tema=tema_de(arq.name),
                     rodada=rodada, situacao=situacao(pasta, arq.name, secao), secao_readme=secao,
                     descricao_readme=desc, primeiro_commit_neste_caminho=ini, ultimo_commit=fim, linhas="", colunas="")
        if arq.suffix == ".csv":
            sep, cols, n = forma_csv(arq)
            linha.update(linhas=n, colunas=len(cols))
            if n <= 5000:   # rótulos de linha só nas tabelas-resumo; as por setor só pelo cabeçalho
                primeira = pd.read_csv(arq, sep=sep, usecols=[0], encoding="utf-8-sig").iloc[:, 0].astype(str)
                rotulos = set(cols) | set(primeira)
            else:
                rotulos = set(cols)
            texto = " ".join(rotulos)
            for ind in nomes_ind:
                if re.search(rf"(?<![a-z_]){re.escape(ind)}(?![a-z0-9_])", texto):
                    onde_aparece[ind].append(f"{linha['pasta'].split('/')[-1]}/{arq.name}")
        tabelas.append(linha)
    for fig in sorted(list(pasta.glob("figuras/*.png")) + list(pasta.glob("figuras/*.svg"))):
        secao, desc = nota_para(fig.name, notas)
        ini, fim = git_datas(fig)
        figuras.append(dict(pasta=str(fig.parent.relative_to(RAIZ)), arquivo=fig.name, tema=tema_de(fig.name),
                            rodada=rodada, situacao=situacao(pasta, fig.name, secao),
                            descricao_readme=desc, primeiro_commit_neste_caminho=ini, ultimo_commit=fim))

# ------------------------------------------------------------------ decks, notebooks, relatórios
decks = []
for d in sorted((RAIZ / "docs" / "Apresentacoes_IVS").rglob("*.pptx")):
    sub = d.parent.name
    sit = {"Apresentacoes_IVS": "Apresentação atual", "complementos": "Complemento vigente",
           "historico": "Histórico — já apresentado"}.get(sub, sub)
    with zipfile.ZipFile(d) as z:
        n = sum(1 for x in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", x))
    ini, fim = git_datas(d)
    decks.append(dict(pasta=str(d.parent.relative_to(RAIZ)), arquivo=d.name, situacao=sit, slides=n,
                      primeiro_commit_neste_caminho=ini, ultimo_commit=fim))

docs = []
for p in sorted((RAIZ / "notebooks").rglob("*.ipynb")) + sorted((RAIZ / "docs" / "relatorios").glob("*.md")) \
        + sorted((RAIZ / "Backup").rglob("*.ipynb")):
    if ".ipynb_checkpoints" in str(p) or p.name == "README.md":
        continue
    ini, fim = git_datas(p)
    fase = "Backup — Fases 1 e 2 (Brasil inteiro)" if "Backup" in p.parts else \
           ("Notebook vigente" if p.suffix == ".ipynb" else "Relatório")
    docs.append(dict(pasta=str(p.parent.relative_to(RAIZ)), arquivo=p.name, situacao=fase, primeiro_commit_neste_caminho=ini, ultimo_commit=fim))

# ------------------------------------------------------------------ indicadores
ind = indicadores[["indicador", "dimensao", "entra_no_ivs7", "o_que_mede"]].copy()
extra = pd.DataFrame([
    ("renda_media_sem_extremo", "Socioeconômica", "Variante", "Renda média do responsável sem o setor extremo de BH"),
    ("renda_media_mediana_mun", "Socioeconômica", "Variante", "Renda média do responsável com o extremo trocado pela mediana do município"),
    ("renda_inv", "Socioeconômica", "Variante", "Renda invertida, como entra na fatorial"),
], columns=ind.columns)
ind = pd.concat([ind, extra], ignore_index=True)
ind["n_tabelas"] = ind["indicador"].map(lambda n: len(onde_aparece.get(n, [])))
ind["tabelas_onde_aparece"] = ind["indicador"].map(lambda n: " | ".join(onde_aparece.get(n, [])))

# ------------------------------------------------------------------ gravação
ESCOLHA = ["Vai para o artigo? (Sim/Talvez/Não)", "Seção do artigo", "Comentários"]
abas = {"Indicadores": ind, "Tabelas": pd.DataFrame(tabelas), "Figuras": pd.DataFrame(figuras),
        "Decks": pd.DataFrame(decks), "Notebooks_e_relatorios": pd.DataFrame(docs)}
for nome in ("Indicadores", "Tabelas", "Figuras"):
    for c in ESCOLHA:
        abas[nome][c] = ""
resumo = pd.DataFrame([
    ("Indicadores catalogados", len(ind)), ("Tabelas (CSV/JSON)", len(tabelas)), ("Figuras", len(figuras)),
    ("Decks", len(decks)), ("Notebooks e relatórios", len(docs)),
    ("Tabelas vigentes", sum(t["situacao"].startswith("Vigente") for t in tabelas)),
    ("Tabelas superadas ou históricas", sum(not t["situacao"].startswith(("Vigente", "Insumo")) for t in tabelas)),
], columns=["item", "quantidade"])
with pd.ExcelWriter(SAIDA, engine="openpyxl") as xw:
    resumo.to_excel(xw, sheet_name="Resumo", index=False)
    for nome, df in abas.items():
        df.to_excel(xw, sheet_name=nome, index=False)
    for ws in xw.book.worksheets:
        ws.freeze_panes = "B2"
        ws.auto_filter.ref = ws.dimensions
        for col in ws.columns:
            larg = max(len(str(c.value or "")) for c in col[:200])
            ws.column_dimensions[col[0].column_letter].width = min(max(10, larg + 2), 60)
print(resumo.to_string(index=False))
print("\nTabelas por tema:")
print(pd.DataFrame(tabelas).groupby("tema").size().sort_values(ascending=False).to_string())
print("\nSituação:")
print(pd.DataFrame(tabelas).groupby("situacao").size().to_string())
print("\nIndicadores sem nenhuma tabela:", list(ind.loc[ind.n_tabelas == 0, "indicador"]))
