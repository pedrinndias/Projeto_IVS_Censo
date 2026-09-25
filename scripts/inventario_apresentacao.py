"""Inventário dos artefatos de apresentação (Fase 4, item 4.1).

Lista cada .pptx de docs/Apresentacoes_IVS/ (raiz, complementos/, historico/), os
PDFs e .docx de complementos/, os relatórios de docs/relatorios/ e as figuras de
banco_de_dados/eda/. Classifica cada um em ATUAL, SUPERADO ou HISTÓRICO por
critério explícito (não por gosto) e escreve o mapa em Markdown, incluindo um
roteiro proposto para a apresentação final. Não move nem apaga nada.

Uso: uv run --with python-pptx --with pandas python scripts/inventario_apresentacao.py <saida.md>
"""
import sys
from pathlib import Path

import pandas as pd
from pptx import Presentation

RAIZ = Path(__file__).resolve().parent.parent
APRES = RAIZ / "docs" / "Apresentacoes_IVS"
COMPLEMENTOS = APRES / "complementos"
HISTORICO = APRES / "historico"
RELATORIOS = RAIZ / "docs" / "relatorios"
EDA = RAIZ / "banco_de_dados" / "eda"
DECK_ATUAL = APRES / "Analise_Fatorial_NB04_2026-09.pptx"

# Geradores conhecidos (scripts/README.md) — mapeamento verificável, não achismo.
GERADORES = {
    "Analise_Fatorial_NB04_2026-09.pptx": (
        "gerar_deck_fatorial.js (base) + gerar_slides_extremo_bh.js "
        "(slides 95-98, anexados) + edição manual depois — não é 100% reproduzível"
    ),
    "EDA_Central_IVS_2026-09_rev2.pptx": "gerar_deck_eda_central.js",
    "Criterio_Outliers_Renda.pptx": "gerar_deck_criterio_renda.js",
    "Criterio_Outliers_Renda.pdf": "gerar_pdf_outliers_renda.py",
    "Guia_Apoio_Analise_Fatorial.pdf": "gerar_pdf_guia_fatorial.py",
    "Plano_Emergencia_Apresentacao.pdf": "gerar_pdf_plano_emergencia.py",
    "Resumo_EDA_Central_2026-08.docx": "gerar_resumo_eda_central.py",
    "Resumo_EDA_Central_2026-08.pdf": "gerar_resumo_eda_central.py (exportado a mão para PDF)",
    "Roteiro_EDA_Central_2a_rodada.docx": "atualizar_roteiro_2a_rodada.py (migra da 1a rodada)",
}


def extrair_texto_pptx(caminho: Path) -> str:
    prs = Presentation(str(caminho))
    partes = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                partes.append(shape.text_frame.text)
        if slide.has_notes_slide:
            partes.append(slide.notes_slide.notes_text_frame.text)
    return "\n".join(partes)


def contar_slides_notas_explicar(caminho: Path):
    prs = Presentation(str(caminho))
    n_slides = len(prs.slides)
    n_notas = sum(1 for s in prs.slides if s.has_notes_slide)
    texto_total = extrair_texto_pptx(caminho)
    n_explicar = texto_total.count("EXPLICAR")
    return n_slides, n_notas, n_explicar


def listar(diretorio: Path, exts):
    if not diretorio.exists():
        return []
    return [
        p
        for p in sorted(diretorio.rglob("*"))
        if p.is_file() and p.suffix.lower() in exts and not p.name.startswith(".")
    ]


def linha(caminho: Path, texto_deck_atual: str):
    rel = caminho.relative_to(RAIZ)
    stat = caminho.stat()
    data = pd.Timestamp(stat.st_mtime, unit="s").strftime("%Y-%m-%d")
    tamanho_kb = round(stat.st_size / 1024, 1)
    gerador = GERADORES.get(caminho.name, "não identificado")
    citado = caminho.name in texto_deck_atual if texto_deck_atual else False
    return {
        "arquivo": str(rel),
        "data": data,
        "tamanho_kb": tamanho_kb,
        "gerador": gerador,
        "citado_no_deck_atual": citado,
    }


def classificar(item: dict, homonimos_superados: set) -> tuple:
    caminho = RAIZ / item["arquivo"]
    nome = caminho.name
    if HISTORICO in caminho.parents:
        return "HISTÓRICO", "pasta historico/ — metodologia abandonada, fica como registro"
    if caminho == DECK_ATUAL:
        return "ATUAL", "deck vigente (98 slides); editado à mão depois de gerado"
    if nome == "EDA_Central_IVS_2026-09_rev2.pptx":
        return (
            "SUPERADO",
            "conteúdo incorporado ao deck atual, slides 44-94 (ver seção 1 do prompt)",
        )
    if nome == "Roteiro_EDA_Central_1a_rodada.docx" or nome == "Roteiro_EDA_Central_1a_rodada.pdf":
        return "SUPERADO", "sucessor: Roteiro_EDA_Central_2a_rodada.docx"
    if nome in homonimos_superados:
        return "SUPERADO", "existe versão homônima mais nova em banco_de_dados/eda/atualizada/"
    if item["gerador"] != "não identificado":
        return "ATUAL", f"reproduzível por scripts/{item['gerador'].split(' ')[0]}"
    return "ATUAL (sem gerador versionado identificado)", "requer checagem do Pedro"


def main():
    if len(sys.argv) != 2:
        sys.exit("uso: inventario_apresentacao.py <saida.md>")
    saida = Path(sys.argv[1])

    texto_deck_atual = extrair_texto_pptx(DECK_ATUAL) if DECK_ATUAL.exists() else ""
    n_slides_atual, n_notas_atual, n_explicar_atual = contar_slides_notas_explicar(DECK_ATUAL)

    pptxs = listar(APRES, {".pptx"})
    pdfs = listar(COMPLEMENTOS, {".pdf"})
    docxs = listar(COMPLEMENTOS, {".docx"})
    relatorios = listar(RELATORIOS, {".md", ".docx"})
    figuras = listar(EDA, {".png"})

    # figuras homônimas: mesmo nome de arquivo presente em banco_de_dados/eda/atualizada/
    atualizada_nomes = {p.name for p in (EDA / "atualizada" / "figuras").glob("*.png")}
    homonimos_superados = set()
    for p in (EDA / "figuras").glob("*.png") if (EDA / "figuras").exists() else []:
        if p.name in atualizada_nomes:
            homonimos_superados.add(p.name)

    itens = []
    for caminho in pptxs + pdfs + docxs + relatorios + figuras:
        item = linha(caminho, texto_deck_atual)
        estado, obs = classificar(item, homonimos_superados)
        item["estado"] = estado
        item["observacao"] = obs
        itens.append(item)

    df = pd.DataFrame(itens)

    def tabela(sub: pd.DataFrame) -> str:
        if sub.empty:
            return "_nenhum item._\n"
        cols = ["arquivo", "data", "tamanho_kb", "gerador", "citado_no_deck_atual", "observacao"]
        linhas = ["| arquivo | data | KB | gerador | citado no deck atual | observação |",
                  "|---|---|---|---|---|---|"]
        for _, r in sub[cols].iterrows():
            linhas.append(
                f"| {r['arquivo']} | {r['data']} | {r['tamanho_kb']} | {r['gerador']} | "
                f"{'sim' if r['citado_no_deck_atual'] else 'não'} | {r['observacao']} |"
            )
        return "\n".join(linhas) + "\n"

    atuais = df[df["estado"].str.startswith("ATUAL")].sort_values("arquivo")
    superados = df[df["estado"] == "SUPERADO"].sort_values("arquivo")
    historicos = df[df["estado"] == "HISTÓRICO"].sort_values("arquivo")

    n_figuras_ampliada = len(list((EDA / "fatorial_ampliada" / "figuras").glob("*.png")))

    md = []
    md.append("# Mapa da apresentação final\n")
    md.append(
        "Gerado por `scripts/inventario_apresentacao.py` (Fase 4, item 4.1). Não move nem "
        "apaga nada — é uma proposta; quem decide é o Pedro.\n"
    )
    md.append(
        f"Deck atual conferido na hora: `{DECK_ATUAL.relative_to(RAIZ)}` — "
        f"{n_slides_atual} slides, {n_notas_atual} com notas, "
        f"{n_explicar_atual} marcações \"EXPLICAR\".\n"
    )
    md.append("## Critério de classificação\n")
    md.append(
        "- **ATUAL:** reflete a metodologia vigente (denominador V00001, recorte urbano de "
        "104.108, indicadores do módulo) e é reproduzível por script versionado (ou é o "
        "próprio deck vigente).\n"
        "- **SUPERADO:** tem sucessor identificado que o substitui — dito na coluna "
        "observação.\n"
        "- **HISTÓRICO:** está na pasta `historico/`, de metodologia abandonada — fica como "
        "registro.\n"
    )
    md.append("## ATUAL\n")
    md.append(tabela(atuais))
    md.append("\n## SUPERADO\n")
    md.append(tabela(superados))
    md.append("\n## HISTÓRICO\n")
    md.append(tabela(historicos))

    md.append("\n## Roteiro proposto para a apresentação final\n")
    md.append(
        "Sequência de slides do deck de 98 (numeração impressa mantida) mais o bloco novo da "
        "fatorial ampliada, anexado ao fim pelo juntador (nunca regerando o deck):\n\n"
        "1. **Slides 1-43 — análise fatorial (NB04).** Metodologia vigente, corrigida na "
        "Fase 3 (NB4-01 a NB4-13, AUD-08 pendente para o guia).\n"
        "2. **Slides 44-94 — EDA Central.** Incorporada ao deck atual; `EDA_Central_IVS_"
        "2026-09_rev2.pptx` fica como registro (SUPERADO nesta tabela), não entra de novo.\n"
        "3. **Slides 95-98 — o extremo de Belo Horizonte.** Números corrigidos em 4.2.3 "
        "(AUD-07): segundo maior R$ 45.385,44; agregado de 104.096 setores; fração 37%.\n"
        f"4. **Slides {n_slides_atual + 1}-{n_slides_atual + 8} (novos, item 4.2.2) — a "
        "fatorial ampliada.** Divisória; o que a orientadora pediu; a matriz ampliada; a "
        "tabela de cenários; o plano fatorial em três rotações (revisar rótulos e eixos de "
        "`fa_plano_s6.png` antes — pendência da Fase 2); lixo; a estrutura municipal; o que "
        f"fica para ela decidir. {n_figuras_ampliada} figuras disponíveis em "
        "`banco_de_dados/eda/fatorial_ampliada/figuras/`.\n"
    )
    md.append(
        "\nNão entram no roteiro (por ora): `Criterio_Outliers_Renda.*` e "
        "`Plano_Emergencia_Apresentacao.pdf` (materiais de apoio, não slides do deck "
        "principal); tudo em `historico/`.\n"
    )

    saida.write_text("".join(md), encoding="utf-8")
    print("linhas:", len(df), "| ATUAL:", len(atuais), "| SUPERADO:", len(superados),
          "| HISTORICO:", len(historicos))
    print("deck atual:", n_slides_atual, "slides,", n_notas_atual, "notas,",
          n_explicar_atual, "EXPLICAR")


if __name__ == "__main__":
    main()
