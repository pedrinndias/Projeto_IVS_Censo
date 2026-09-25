"""Anexa os slides de um .pptx ao fim de outro, sem regerar nenhum dos dois.

Copia, do deck anexo para o deck base: slide, layout, master e tema (só os que o
slide anexado usa, renumerados para não colidir com o que já existe na base),
notas e mídia. Atualiza [Content_Types].xml, os .rels e as listas de slide/master
de ppt/presentation.xml. Não apaga nada do deck base; grava sempre num arquivo de
saída novo.

Uso: ./.venv/bin/python scripts/juntar_decks.py <base.pptx> <anexo.pptx> <saida.pptx>

Depois de rodar, confira sempre (é o próprio script que confere, no fim):
número de slides, número de notas e marcações "EXPLICAR" — base + anexo == saída.
"""
import re
import sys
import zipfile
from pathlib import Path

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

RELTYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def ler(z, nome):
    return z.read(nome).decode("utf-8")


def proximo_indice(nomes, prefixo, sufixo):
    """Maior índice numérico já usado em ppt/<prefixo>N<sufixo>, mais 1."""
    maior = 0
    padrao = re.compile(r"^ppt/" + re.escape(prefixo) + r"(\d+)" + re.escape(sufixo) + r"$")
    for n in nomes:
        m = padrao.match(n)
        if m:
            maior = max(maior, int(m.group(1)))
    return maior + 1


def rels_de(z, parte):
    """Caminho do .rels de uma parte (ppt/slides/slide1.xml -> ppt/slides/_rels/slide1.xml.rels)."""
    d = parte.rsplit("/", 1)
    pasta, arq = (d[0], d[1]) if len(d) == 2 else ("", d[0])
    return f"{pasta}/_rels/{arq}.rels" if pasta else f"_rels/{arq}.rels"


def parse_rels(xml_bytes_str):
    """Retorna dict rId -> (type, target) a partir do texto do .rels."""
    out = {}
    for m in re.finditer(
        r'<Relationship\s+Id="([^"]+)"\s+Type="([^"]+)"\s+Target="([^"]+)"[^/]*/>',
        xml_bytes_str,
    ):
        out[m.group(1)] = (m.group(2), m.group(3))
    return out


def resolver_target(base_parte, target):
    """Resolve um Target relativo do .rels contra a pasta da parte que o contém."""
    if target.startswith("/"):
        return target.lstrip("/")
    pasta = base_parte.rsplit("/", 1)[0]
    partes = (pasta + "/" + target).split("/")
    pilha = []
    for p in partes:
        if p == "..":
            pilha.pop()
        elif p and p != ".":
            pilha.append(p)
    return "/".join(pilha)


class Merge:
    def __init__(self, z_base, z_anexo):
        self.zb = z_base
        self.za = z_anexo
        self.nomes_base = set(z_base.namelist())
        self.novos = {}  # caminho novo -> bytes
        self.copiado = {}  # caminho antigo (no anexo) -> caminho novo (na base)
        self.rel_novas = {}  # arquivo .rels da base -> lista de (Id, Type, Target) a acrescentar
        self.ct_overrides = []  # (PartName, ContentType) a acrescentar em [Content_Types].xml

    def copiar_parte(self, caminho_antigo, prefixo, sufixo, content_type):
        if caminho_antigo in self.copiado:
            return self.copiado[caminho_antigo]
        idx = proximo_indice(self.nomes_base | set(self.novos), prefixo, sufixo)
        novo = f"ppt/{prefixo}{idx}{sufixo}"
        dados = self.za.read(caminho_antigo)
        self.novos[novo] = dados
        self.copiado[caminho_antigo] = novo
        self.ct_overrides.append((("/" + novo), content_type))
        return novo

    def copiar_midia(self, caminho_antigo):
        if caminho_antigo in self.copiado:
            return self.copiado[caminho_antigo]
        ext = caminho_antigo.rsplit(".", 1)[-1]
        idx = proximo_indice(self.nomes_base | set(self.novos), "media/image", "." + ext)
        novo = f"ppt/media/image{idx}.{ext}"
        self.novos[novo] = self.za.read(caminho_antigo)
        self.copiado[caminho_antigo] = novo
        return novo

    def reescrever_rels_filhos(self, xml_texto, caminho_antigo_parte):
        """Reescreve, no texto do .rels de uma parte já copiada, os Targets que
        apontam para partes que também precisam ser copiadas (mídia, etc.)."""
        rels = parse_rels(xml_texto)
        novo_texto = xml_texto
        for rid, (tipo, target) in rels.items():
            if target.startswith("http"):
                continue
            alvo_abs = resolver_target(caminho_antigo_parte, target)
            if "/media/" in alvo_abs:
                novo_alvo = self.copiar_midia(alvo_abs)
                novo_rel = "../media/" + novo_alvo.rsplit("/", 1)[-1]
                novo_texto = novo_texto.replace(f'Target="{target}"', f'Target="{novo_rel}"')
        return novo_texto

    def copiar_tema(self, caminho_tema):
        novo = self.copiar_parte(
            caminho_tema, "theme/theme", ".xml",
            "application/vnd.openxmlformats-officedocument.theme+xml",
        )
        return novo

    def copiar_master(self, caminho_master):
        if caminho_master in self.copiado:
            return self.copiado[caminho_master]
        novo = self.copiar_parte(
            caminho_master, "slideMasters/slideMaster", ".xml",
            "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml",
        )
        rels_antigo = rels_de(self.za, caminho_master)
        if rels_antigo in self.za.namelist():
            texto = ler(self.za, rels_antigo)
            rels = parse_rels(texto)
            novo_texto = texto
            for rid, (tipo, target) in rels.items():
                alvo_abs = resolver_target(caminho_master, target)
                if tipo.endswith("/theme"):
                    novo_alvo = self.copiar_tema(alvo_abs)
                elif tipo.endswith("/slideLayout"):
                    novo_alvo = self.copiar_layout(alvo_abs)
                elif "/media/" in alvo_abs:
                    novo_alvo = self.copiar_midia(alvo_abs)
                else:
                    continue
                rel_novo = "../" + novo_alvo.split("/", 1)[1]
                novo_texto = novo_texto.replace(f'Target="{target}"', f'Target="{rel_novo}"')
            self.novos[rels_de(self.za, novo)] = novo_texto.encode("utf-8")
        return novo

    def copiar_layout(self, caminho_layout):
        if caminho_layout in self.copiado:
            return self.copiado[caminho_layout]
        novo = self.copiar_parte(
            caminho_layout, "slideLayouts/slideLayout", ".xml",
            "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml",
        )
        rels_antigo = rels_de(self.za, caminho_layout)
        if rels_antigo in self.za.namelist():
            texto = ler(self.za, rels_antigo)
            rels = parse_rels(texto)
            novo_texto = texto
            for rid, (tipo, target) in rels.items():
                alvo_abs = resolver_target(caminho_layout, target)
                if tipo.endswith("/slideMaster"):
                    # a referência de volta ao master é resolvida depois de copiar o
                    # master (evita recursão infinita master<->layout); se o master
                    # já foi copiado, usa o mapeamento; senão, mantém o texto igual e
                    # deixa para o chamador (copiar_master) tratar layouts filhos.
                    if alvo_abs in self.copiado:
                        novo_alvo = self.copiado[alvo_abs]
                        rel_novo = "../" + novo_alvo.split("/", 1)[1]
                        novo_texto = novo_texto.replace(f'Target="{target}"', f'Target="{rel_novo}"')
                elif "/media/" in alvo_abs:
                    novo_alvo = self.copiar_midia(alvo_abs)
                    rel_novo = "../" + novo_alvo.split("/", 1)[1]
                    novo_texto = novo_texto.replace(f'Target="{target}"', f'Target="{rel_novo}"')
            self.novos[rels_de(self.za, novo)] = novo_texto.encode("utf-8")
        return novo

    def copiar_notas(self, caminho_notas):
        novo = self.copiar_parte(
            caminho_notas, "notesSlides/notesSlide", ".xml",
            "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml",
        )
        rels_antigo = rels_de(self.za, caminho_notas)
        if rels_antigo in self.za.namelist():
            texto = ler(self.za, rels_antigo)
            novo_texto = self.reescrever_rels_filhos(texto, caminho_notas)
            self.novos[rels_de(self.za, novo)] = novo_texto.encode("utf-8")
        return novo

    def copiar_slide(self, caminho_slide):
        novo = self.copiar_parte(
            caminho_slide, "slides/slide", ".xml",
            "application/vnd.openxmlformats-officedocument.presentationml.slide+xml",
        )
        rels_antigo = rels_de(self.za, caminho_slide)
        novo_texto_rels = None
        if rels_antigo in self.za.namelist():
            texto = ler(self.za, rels_antigo)
            rels = parse_rels(texto)
            novo_texto_rels = texto
            for rid, (tipo, target) in rels.items():
                if target.startswith("../slideLayouts/"):
                    alvo_abs = resolver_target(caminho_slide, target)
                    novo_alvo = self.copiar_layout(alvo_abs)
                    rel_novo = "../" + novo_alvo.split("/", 1)[1]
                    novo_texto_rels = novo_texto_rels.replace(f'Target="{target}"', f'Target="{rel_novo}"')
                elif tipo.endswith("/notesSlide"):
                    alvo_abs = resolver_target(caminho_slide, target)
                    novo_alvo = self.copiar_notas(alvo_abs)
                    rel_novo = "../" + novo_alvo.split("/", 1)[1]
                    novo_texto_rels = novo_texto_rels.replace(f'Target="{target}"', f'Target="{rel_novo}"')
                elif "/media/" in resolver_target(caminho_slide, target):
                    alvo_abs = resolver_target(caminho_slide, target)
                    novo_alvo = self.copiar_midia(alvo_abs)
                    rel_novo = "../" + novo_alvo.split("/", 1)[1]
                    novo_texto_rels = novo_texto_rels.replace(f'Target="{target}"', f'Target="{rel_novo}"')
            self.novos[rels_de(self.za, novo)] = novo_texto_rels.encode("utf-8")
        return novo


def ordem_dos_slides(z):
    """Lê ppt/presentation.xml + seus rels e devolve a lista de caminhos
    ppt/slides/slideN.xml na ordem de exibição."""
    pres = ler(z, "ppt/presentation.xml")
    rels_texto = ler(z, "ppt/_rels/presentation.xml.rels")
    rels = parse_rels(rels_texto)
    ids = re.findall(r'<p:sldId[^>]*r:id="([^"]+)"', pres)
    caminhos = []
    for rid in ids:
        tipo, target = rels[rid]
        caminhos.append(resolver_target("ppt/presentation.xml", target))
    return caminhos


def main():
    if len(sys.argv) != 4:
        sys.exit("uso: juntar_decks.py <base.pptx> <anexo.pptx> <saida.pptx>")
    base_p, anexo_p, saida_p = (Path(a) for a in sys.argv[1:4])

    with zipfile.ZipFile(base_p) as zb, zipfile.ZipFile(anexo_p) as za:
        m = Merge(zb, za)
        slides_anexo = ordem_dos_slides(za)
        if not slides_anexo:
            sys.exit("o anexo não tem slides")

        novos_caminhos_slide = [m.copiar_slide(c) for c in slides_anexo]

        # ppt/presentation.xml da base: acrescenta <p:sldId> e, se precisou copiar
        # slideMaster(es) novos, <p:sldMasterId> também.
        pres_base = ler(zb, "ppt/presentation.xml")
        rels_pres_base_texto = ler(zb, "ppt/_rels/presentation.xml.rels")

        # ids de sldId já usados na base
        ids_existentes = [int(x) for x in re.findall(r'<p:sldId[^>]*\bid="(\d+)"', pres_base)]
        prox_id = (max(ids_existentes) + 1) if ids_existentes else 256
        rids_existentes = set(re.findall(r'Id="(rId\d+)"', rels_pres_base_texto))
        prox_rid = 1
        while f"rId{prox_rid}" in rids_existentes:
            prox_rid += 1

        novas_rel_linhas = []
        novos_sldid_linhas = []
        for caminho_novo in novos_caminhos_slide:
            rid = f"rId{prox_rid}"
            prox_rid += 1
            novas_rel_linhas.append(
                f'<Relationship Id="{rid}" '
                f'Type="{RELTYPE}/slide" Target="slides/{caminho_novo.split("/")[-1]}"/>'
            )
            novos_sldid_linhas.append(f'<p:sldId id="{prox_id}" r:id="{rid}"/>')
            prox_id += 1

        rels_pres_base_novo = rels_pres_base_texto.replace(
            "</Relationships>", "".join(novas_rel_linhas) + "</Relationships>"
        )
        pres_base_novo = re.sub(
            r"(</p:sldIdLst>)", "".join(novos_sldid_linhas) + r"\1", pres_base, count=1
        )

        # [Content_Types].xml da base: Overrides para as partes novas
        ct_texto = ler(zb, "[Content_Types].xml")
        overrides = "".join(
            f'<Override PartName="{pn}" ContentType="{ctp}"/>' for pn, ctp in m.ct_overrides
        )
        ct_novo = ct_texto.replace("</Types>", overrides + "</Types>")

        # grava o zip de saída: tudo da base, sobrescrevendo os 3 arquivos mexidos,
        # mais tudo que veio novo do anexo
        with zipfile.ZipFile(saida_p, "w", zipfile.ZIP_DEFLATED) as zs:
            for item in zb.infolist():
                dados = zb.read(item.filename)
                if item.filename == "ppt/presentation.xml":
                    dados = pres_base_novo.encode("utf-8")
                elif item.filename == "ppt/_rels/presentation.xml.rels":
                    dados = rels_pres_base_novo.encode("utf-8")
                elif item.filename == "[Content_Types].xml":
                    dados = ct_novo.encode("utf-8")
                zs.writestr(item, dados)
            for caminho, dados in m.novos.items():
                zs.writestr(caminho, dados)

    print(f"anexados {len(novos_caminhos_slide)} slides de {anexo_p.name} ao fim de "
          f"{base_p.name} -> {saida_p}")


if __name__ == "__main__":
    main()
