"""Extrai de banco_de_dados/eda/ os números do critério de outliers de renda.

Alimenta o deck do critério (scripts/gerar_deck_criterio_renda.js), para que nenhum número
seja digitado no gerador.

O PDF (scripts/gerar_pdf_outliers_renda.py) ainda faz a própria derivação, porque também
precisa dos DataFrames crus para desenhar a figura. As duas leem os mesmos CSVs e importam
as mesmas constantes, e os totais foram conferidos entre si; ainda assim, unificar as duas
é dívida em aberto — derivação em dois lugares é a causa raiz que este projeto já pagou
para corrigir uma vez.

As constantes da regra são importadas de src/ivs_censo/renda.py, para que o texto dos
artefatos não descreva uma versão diferente da que roda.

Uso:
    ./.venv/bin/python scripts/dados_criterio_renda.py banco_de_dados/eda/dados_criterio_renda.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
EDA = RAIZ / "banco_de_dados" / "eda"
sys.path.insert(0, str(RAIZ / "src"))
from ivs_censo.renda import (K_TUKEY, MIN_SETORES_MUNICIPIO,  # noqa: E402
                             RAZAO_IMPLAUSIVEL)


def br(x, casas=2):
    """Número no padrão brasileiro: milhar com ponto, decimal com vírgula."""
    if pd.isna(x):
        return "—"
    s = f"{x:,.{casas}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def ler(nome: str) -> pd.DataFrame:
    return pd.read_csv(EDA / nome, sep=";", encoding="utf-8-sig")


def calcular() -> dict:
    T = ler("renda_outliers_rastreados.csv")
    classes = ler("renda_classes_resumo.csv")
    crit = ler("renda_criterio_global_vs_municipal.csv")
    peq = ler("renda_setores_pequenos.csv")
    mun = ler("exclusao_rural_conferencia.csv")
    norm = ler("renda_normalizacao_impacto.csv")

    sus = T[T.classe_renda == "SUSPEITO"]
    ext = T[T.classe_renda == "EXTREMO"]
    motivos = sus["motivos"].fillna("").value_counts()
    por_teste = {m: int(sus["motivos"].fillna("").str.contains(m).sum())
                 for m in ("e_favela", "pct_analfab_acima", "pct_raca_pretpardind_acima")}
    qtd = sus["motivos"].fillna("").str.count(r"\+").add(1).value_counts().sort_index()
    mun_peq = mun[mun.n_ok_urbano < MIN_SETORES_MUNICIPIO].sort_values("n_ok_urbano")
    impl_ext = ext[ext.razao_implausivel].sort_values("razao_mediana_mun", ascending=False)

    def linha_setor(r, com_motivos=True):
        base = [str(r.CD_SETOR), r.NM_MUN,
                "—" if pd.isna(r.NM_BAIRRO) else str(r.NM_BAIRRO),
                br(r.renda_media_setor, 0), br(r.renda_p50_mun, 0),
                br(r.razao_mediana_mun, 1) + "×", br(r.n_domicilios, 0), br(r.cv_renda, 2)]
        if com_motivos:
            base.append(str(r.motivos).replace("e_favela", "favela")
                        .replace("pct_analfab_acima", "analfab")
                        .replace("pct_raca_pretpardind_acima", "PPI"))
        return base

    d = {
        "constantes": {
            "k_tukey": br(K_TUKEY, 1),
            "min_setores": str(MIN_SETORES_MUNICIPIO),
            "razao_implausivel": br(RAZAO_IMPLAUSIVEL, 0),
        },
        "totais": {
            "n_suspeitos": str(len(sus)),
            "n_extremos": br(len(ext), 0),
            "n_rastreados": br(len(T), 0),
            "n_mun_peq": str(len(mun_peq)),
            "n_set_peq": br(int(mun_peq.n_ok_urbano.sum()), 0),
            "n_mun_aval": str(int((mun.n_ok_urbano >= MIN_SETORES_MUNICIPIO).sum())),
            "n_impl_ext": str(len(impl_ext)),
            "n_impl_sus": str(int(sus.razao_implausivel.sum())),
            "um_teste": str(int(qtd.get(1, 0))),
            "tres_testes": str(int(qtd.get(3, 0))),
            "so_analfab": str(int(motivos.get("pct_analfab_acima", 0))),
            "n_favela": str(por_teste["e_favela"]),
            "cv_med_sus": br(sus.cv_renda.median(), 2),
            "cv_med_ext": br(ext.cv_renda.median(), 2),
            "n_global": br(int(crit.outlier_global.sum()), 0),
            "n_municipal": br(int(crit.outlier_municipal.sum()), 0),
            "concordam": br(int(crit.concordam.sum()), 0),
            "so_global": br(int(crit.so_global.sum()), 0),
            "so_municipal": br(int(crit.so_municipal.sum()), 0),
            "norm_avaliados": str(len(norm)),
            "norm_com_suspeito": str(int((norm.n_suspeitos > 0).sum())),
        },
        "por_teste": {k: str(v) for k, v in por_teste.items()},
        "tabelas": {},
    }

    d["tabelas"]["classes"] = {
        "colunas": ["Classe", "Setores", "% da base", "Renda mediana", "Renda média", "Renda máxima"],
        "linhas": [[r.classe_renda, br(r.n_setores, 0), br(r.pct_setores, 3) + "%",
                    br(r.renda_mediana), br(r.renda_media), br(r.renda_max)]
                   for r in classes.itertuples()],
        "fonte": "renda_classes_resumo.csv. Recorte urbano elegível, 104.108 setores.",
    }
    d["tabelas"]["municipios_pequenos"] = {
        "colunas": ["Município", "Região", "Setores"],
        "linhas": [[r.NM_MUN, r.regiao, str(int(r.n_ok_urbano))] for r in mun_peq.itertuples()],
        "fonte": "exclusao_rural_conferencia.csv, recorte urbano elegível.",
    }
    d["tabelas"]["motivos"] = {
        "colunas": ["Combinação de testes que disparou", "Setores"],
        "linhas": [[m if m else "(nenhum)", str(int(n))] for m, n in motivos.items()],
        "fonte": "renda_outliers_rastreados.csv, coluna motivos.",
    }
    d["tabelas"]["maiores_suspeitos"] = {
        "colunas": ["Setor", "Município", "Bairro", "Renda", "Mediana mun.", "Razão", "Dom.", "CV", "Testes"],
        "linhas": [linha_setor(r) for r in
                   sus.sort_values("renda_media_setor", ascending=False).head(8).itertuples()],
        "fonte": "renda_outliers_rastreados.csv. Razão = renda do setor ÷ mediana do município.",
    }
    d["tabelas"]["implausiveis"] = {
        "colunas": ["Setor", "Município", "Bairro", "Renda", "Mediana mun.", "Razão", "Dom.", "CV"],
        "linhas": [linha_setor(r, com_motivos=False) for r in impl_ext.head(10).itertuples()],
        "fonte": "renda_outliers_rastreados.csv, classe EXTREMO com razao_implausivel verdadeiro.",
    }
    d["tabelas"]["criterios"] = {
        "colunas": ["Região", "Setores", "Global", "% global", "Municipal", "% municipal", "Coincidem"],
        "linhas": [[r.regiao, br(r.n_setores, 0), br(r.outlier_global, 0), br(r.pct_global, 2) + "%",
                    br(r.outlier_municipal, 0), br(r.pct_municipal, 2) + "%", br(r.concordam, 0)]
                   for r in crit.itertuples()],
        "fonte": "renda_criterio_global_vs_municipal.csv.",
    }
    d["tabelas"]["tamanho"] = {
        "colunas": ["Faixa de domicílios", "Setores", "% da base", "Renda mediana",
                    "Renda máxima", "CV", "Suspeitos", "% suspeitos"],
        "linhas": [[r.faixa_dom, br(r.n_setores, 0), br(r.pct_da_base, 2) + "%",
                    br(r.renda_mediana, 0), br(r.renda_max, 0), br(r.cv, 3),
                    str(int(r.n_suspeitos)), br(r.pct_suspeitos, 3) + "%"]
                   for r in peq.itertuples()],
        "fonte": "renda_setores_pequenos.csv. CV é o da renda dentro da faixa, não o do setor.",
    }
    return d


def main() -> None:
    destino = Path(sys.argv[1]) if len(sys.argv) > 1 else EDA / "dados_criterio_renda.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(calcular(), ensure_ascii=False, indent=1), encoding="utf-8")
    print("dados escritos:", destino)


if __name__ == "__main__":
    main()
