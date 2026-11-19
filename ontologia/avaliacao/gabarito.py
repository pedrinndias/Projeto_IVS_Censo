"""Gabarito das perguntas de avaliação da ontologia, calculado pelo código do projeto.

Recalcula os indicadores com `calcular_indicadores` e a elegibilidade com
`classificar_dados_sig` a partir das variáveis brutas, confere contra as colunas
gravadas no banco e grava `gabarito.json` ao lado deste arquivo.

Uso (da raiz do projeto): PYTHONPATH=src .venv/bin/python ontologia/avaliacao/gabarito.py
"""
from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path

import pandas as pd

from ivs_censo.indicadores import calcular_indicadores, classificar_dados_sig
from ivs_censo.renda import SETORES_RENDA_EXCLUIDA

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

RAIZ = Path(__file__).resolve().parents[2]
DB = RAIZ / "banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db"
SAIDA = Path(__file__).with_name("gabarito.json")
CONFERIR = ["pct_agua_inad", "pct_esgoto_inad", "pct_analfab", "pct_idoso_60mais"]


def carregar() -> pd.DataFrame:
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        return pd.read_sql("SELECT * FROM setores_censitarios", con)
    finally:
        con.close()


def conferir(df: pd.DataFrame, recalc: pd.DataFrame, sig: pd.Series) -> None:
    """Falha se o recálculo não bate com o que está gravado no banco."""
    for col in CONFERIR:
        dif = (recalc[col] - df[col]).abs().max()
        if not dif < 1e-9:
            raise ValueError(f"{col}: recálculo difere do banco (máx {dif})")
    divergentes = int((sig != df["Dados_sig"]).sum())
    if divergentes:
        raise ValueError(f"Dados_sig: {divergentes} setores divergem do banco")
    log.info("Recálculo confere com o banco: %s e Dados_sig.", ", ".join(CONFERIR))


def main() -> None:
    df = carregar()
    recalc = calcular_indicadores(df)
    sig = classificar_dados_sig(df)
    conferir(df, recalc, sig)

    rec = (df["SITUACAO"] == "Urbana") & (sig == "OK")
    # Convenção das análises (RAIC, fatorial): renda sem os setores de SETORES_RENDA_EXCLUIDA.
    renda_projeto = recalc["renda_media"].where(~df["CD_SETOR"].isin(SETORES_RENDA_EXCLUIDA))
    fcu = df["CD_TIPO"] == "1"
    r = recalc[rec]
    por_mun = df[rec].groupby("NM_MUN").size().sort_values(ascending=False)
    bh = rec & (df["NM_MUN"] == "Belo Horizonte")
    sp = rec & (df["NM_MUN"] == "São Paulo")

    gabarito = {
        "Q01": int(len(df)),
        "Q02": int(rec.sum()),
        "Q03": int(fcu.sum()),
        "Q04": int((rec & fcu).sum()),
        "Q05": round(float(r["pct_agua_inad"].mean()), 4),
        "Q06": {"favela": round(float(recalc.loc[rec & fcu, "pct_esgoto_inad"].mean()), 4),
                "demais": round(float(recalc.loc[rec & ~fcu, "pct_esgoto_inad"].mean()), 4)},
        "Q07": {"municipio": str(por_mun.index[0]), "setores": int(por_mun.iloc[0])},
        "Q08": round(float(recalc.loc[bh, "pct_analfab"].mean()), 4),
        # Q09 tem duas leituras: a convenção do projeto (sem o extremo) é a oficial;
        # a renda original fica registrada porque a linha de base foi corrigida antes desta descoberta.
        "Q09": {"padrao_projeto": int((renda_projeto[rec] > 5000).sum()),
                "renda_original": int((r["renda_media"] > 5000).sum())},
        "Q10": round(float(recalc.loc[sp, "pct_idoso_60mais"].mean()), 4),
        "Q11": int(df["v0001"].sum()),
        "Q12": "sem_resposta",
        "Q13": "sem_resposta",
    }
    SAIDA.write_text(json.dumps(gabarito, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Gabarito gravado em %s", SAIDA)
    log.info(json.dumps(gabarito, ensure_ascii=False))


if __name__ == "__main__":
    main()
