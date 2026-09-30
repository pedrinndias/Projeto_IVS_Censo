"""Testes de scripts/juntar_decks.py — sobretudo de consertar_estrutura.

Monta, em tmp_path, um pacote .pptx sintético mínimo (só as partes que a função lê:
presentation.xml + .rels, dois masters + .rels, três layouts + .rels e
[Content_Types].xml) com os três defeitos reais do deck da fatorial: o master 2
listado duas vezes em <p:sldMasterIdLst>, o ID colidindo com o do próprio layout, e
o slideLayout3 órfão (.rels aponta pro master 1, que não o lista de volta).
"""
import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
import juntar_decks as jd  # noqa: E402

NSP = "http://schemas.openxmlformats.org/presentationml/2006/main"
NSR = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
RELTYPE = jd.RELTYPE

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/ppt/presentation.xml" ContentType='
    '"application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
    '</Types>'
)

PRESENTATION = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<p:presentation xmlns:p="{NSP}" xmlns:r="{NSR}">'
    '<p:sldMasterIdLst>'
    '<p:sldMasterId id="2147483648" r:id="rId1"/>'
    '<p:sldMasterId id="2147483649" r:id="rId101"/>'
    '<p:sldMasterId id="2147483649" r:id="rId106"/>'
    '</p:sldMasterIdLst><p:sldIdLst/></p:presentation>'
)

PRESENTATION_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    f'<Relationship Id="rId1" Type="{RELTYPE}/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
    f'<Relationship Id="rId101" Type="{RELTYPE}/slideMaster" Target="slideMasters/slideMaster2.xml"/>'
    f'<Relationship Id="rId106" Type="{RELTYPE}/slideMaster" Target="slideMasters/slideMaster2.xml"/>'
    '</Relationships>'
)

LAYOUT_XML = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:p="{NSP}"/>'

MASTER1 = "ppt/slideMasters/slideMaster1.xml"
MASTER2 = "ppt/slideMasters/slideMaster2.xml"
LAYOUT1 = "ppt/slideLayouts/slideLayout1.xml"
LAYOUT2 = "ppt/slideLayouts/slideLayout2.xml"
LAYOUT3 = "ppt/slideLayouts/slideLayout3.xml"


def _master_xml(layout_rid):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<p:sldMaster xmlns:p="{NSP}" xmlns:r="{NSR}">'
        f'<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="{layout_rid}"/></p:sldLayoutIdLst>'
        '</p:sldMaster>'
    )


def _rels(entradas):
    linhas = "".join(f'<Relationship Id="{i}" Type="{t}" Target="{tg}"/>' for i, t, tg in entradas)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'{linhas}</Relationships>'
    )


def _pacote_defeituoso():
    """Dict (ordenado) caminho -> texto, com os três defeitos."""
    return {
        "[Content_Types].xml": CONTENT_TYPES,
        "ppt/presentation.xml": PRESENTATION,
        "ppt/_rels/presentation.xml.rels": PRESENTATION_RELS,
        MASTER1: _master_xml("rId1"),
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": _rels(
            [("rId1", f"{RELTYPE}/slideLayout", "../slideLayouts/slideLayout1.xml")]
        ),
        MASTER2: _master_xml("rId1"),
        "ppt/slideMasters/_rels/slideMaster2.xml.rels": _rels(
            [("rId1", f"{RELTYPE}/slideLayout", "../slideLayouts/slideLayout2.xml")]
        ),
        LAYOUT1: LAYOUT_XML,
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": _rels(
            [("rId1", f"{RELTYPE}/slideMaster", "../slideMasters/slideMaster1.xml")]
        ),
        LAYOUT2: LAYOUT_XML,
        "ppt/slideLayouts/_rels/slideLayout2.xml.rels": _rels(
            [("rId1", f"{RELTYPE}/slideMaster", "../slideMasters/slideMaster2.xml")]
        ),
        # órfão: aponta pro master 1, que não o lista em sldLayoutIdLst
        LAYOUT3: LAYOUT_XML,
        "ppt/slideLayouts/_rels/slideLayout3.xml.rels": _rels(
            [("rId1", f"{RELTYPE}/slideMaster", "../slideMasters/slideMaster1.xml")]
        ),
    }


def _gravar_pacote(caminho, arquivos):
    with zipfile.ZipFile(caminho, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, texto in arquivos.items():
            z.writestr(nome, texto)


def _ids_e_layouts_por_master(caminho):
    """Lê o pacote e devolve (lista de todos os ids usados, lista dos masters
    citados em sldMasterIdLst, dict master -> conjunto de layouts que ele lista)."""
    with zipfile.ZipFile(caminho) as z:
        pres = z.read("ppt/presentation.xml").decode("utf-8")
        rels_pres = jd.parse_rels(z.read("ppt/_rels/presentation.xml.rels").decode("utf-8"))
        todos_ids, alvos_master, layouts_por_master = [], [], {}
        for tag in re.findall(r"<p:sldMasterId[^>]*/>", pres):
            todos_ids.append(int(re.search(r'id="(\d+)"', tag).group(1)))
            rid = re.search(r'r:id="([^"]+)"', tag).group(1)
            alvo = jd.resolver_target("ppt/presentation.xml", rels_pres[rid][1])
            alvos_master.append(alvo)

            xml_master = z.read(alvo).decode("utf-8")
            rels_master = jd.parse_rels(z.read(jd.rels_de(z, alvo)).decode("utf-8"))
            layouts = set()
            for tag_l in re.findall(r"<p:sldLayoutId[^>]*/>", xml_master):
                todos_ids.append(int(re.search(r'id="(\d+)"', tag_l).group(1)))
                rid_l = re.search(r'r:id="([^"]+)"', tag_l).group(1)
                layouts.add(jd.resolver_target(alvo, rels_master[rid_l][1]))
            layouts_por_master[alvo] = layouts
        return todos_ids, alvos_master, layouts_por_master


def test_consertar_estrutura_desduplica_ids_unicos_e_liga_orfao(tmp_path):
    entrada = tmp_path / "defeituoso.pptx"
    saida = tmp_path / "consertado.pptx"
    _gravar_pacote(entrada, _pacote_defeituoso())

    jd.consertar_estrutura(entrada, saida)

    todos_ids, alvos_master, layouts_por_master = _ids_e_layouts_por_master(saida)

    # nenhum master listado duas vezes
    assert len(alvos_master) == len(set(alvos_master)) == 2

    # IDs únicos e >= 2147483648 (master e layout dividem o mesmo espaço de IDs)
    assert len(todos_ids) == len(set(todos_ids))
    assert all(i >= 2147483648 for i in todos_ids)

    # cada layout está listado no master que o .rels dele aponta (o órfão inclusive)
    assert layouts_por_master[MASTER1] == {LAYOUT1, LAYOUT3}
    assert layouts_por_master[MASTER2] == {LAYOUT2}


def test_consertar_estrutura_e_idempotente(tmp_path):
    entrada = tmp_path / "defeituoso.pptx"
    saida1 = tmp_path / "consertado1.pptx"
    saida2 = tmp_path / "consertado2.pptx"
    _gravar_pacote(entrada, _pacote_defeituoso())

    jd.consertar_estrutura(entrada, saida1)
    jd.consertar_estrutura(saida1, saida2)  # rodar de novo sobre o já consertado

    partes = [
        "ppt/presentation.xml",
        "ppt/_rels/presentation.xml.rels",
        MASTER1,
        MASTER2,
        "ppt/slideMasters/_rels/slideMaster1.xml.rels",
        "ppt/slideMasters/_rels/slideMaster2.xml.rels",
    ]
    with zipfile.ZipFile(saida1) as z1, zipfile.ZipFile(saida2) as z2:
        for parte in partes:
            assert z1.read(parte) == z2.read(parte), parte


def test_consertar_estrutura_aceita_entrada_igual_a_saida(tmp_path):
    caminho = tmp_path / "no_lugar.pptx"
    _gravar_pacote(caminho, _pacote_defeituoso())

    jd.consertar_estrutura(caminho, caminho)

    _, alvos_master, layouts_por_master = _ids_e_layouts_por_master(caminho)
    assert len(alvos_master) == 2
    assert layouts_por_master[MASTER1] == {LAYOUT1, LAYOUT3}
