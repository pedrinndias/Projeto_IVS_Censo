"""Roteiro em Word da apresentação oral da RAIC 2026, para uso próprio no ensaio e no dia.

Lê as falas, "Se der branco", "Passo para", as perguntas, as reservas e a lista de números de
`relatorio_parcial_raic/ROTEIRO_APRESENTACAO_ORAL.md` (a mesma fonte das notas do pptx). Uma página por
slide (o 1 junto com o 2 e o 14 junto com o 15), fala em 14 pt, Calibri, e a cor da 34ª RAIC só no
cabeçalho de cada slide e na faixa do topo da primeira página (tirada do modelo da Coordic).

Marcação das falas no roteiro: **âncora** (negrito) e *(pausa)*.

Uso:  ./.venv/bin/python scripts/gerar_roteiro_word_raic.py
Saída: relatorio_parcial_raic/Roteiro_Apresentacao_Oral_RAIC_2026_Pedro.docx
"""
from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
PASTA = RAIZ / 'relatorio_parcial_raic'
ROTEIRO = PASTA / 'ROTEIRO_APRESENTACAO_ORAL.md'
MODELO = PASTA / 'modelos' / 'APRESENTACAO_ORAL_Coordic.pptx'
SAIDA = PASTA / 'Roteiro_Apresentacao_Oral_RAIC_2026_Pedro.docx'

TEAL, CINZA, CINZA_CLARO = '3B848E', '6B7780', 'C9CED2'
PALAVRAS_POR_MIN = 130          # ritmo calmo; cada (pausa) soma 2 s e cada slide 2 s de transição
TITULO_CURTO = {1: 'Abertura', 15: 'Obrigado'}
JUNTO_DO_ANTERIOR = {2, 15}     # sem quebra de página antes


# ---------------------------------------------------------------- leitura do roteiro

def ler_roteiro() -> tuple[list[dict], list[dict], list[dict], list[str]]:
    md = ROTEIRO.read_text(encoding='utf-8')
    corpo, resto = md.split('## Reserva para a arguição', 1)
    slides = []
    for bloco in re.split(r'(?m)^### ', corpo.split('## Os slides', 1)[1])[1:]:
        cab, texto = bloco.split('\n', 1)
        m = re.match(r'(\d+)\. (?:[A-ZÇÕÃÉ]+ · )?(.*?) — \d+ s', cab)
        campos = {}
        for rot, val in re.findall(r'(?ms)^- \*\*(Fala|Se der branco|Passo para)[^*]*:\*\* (.*?)(?=^- \*\*|\Z)', texto):
            val = re.sub(r'\s+', ' ', val.split('\n---', 1)[0]).strip().strip('"')
            campos[rot] = val
        n = int(m[1])
        fala = campos.get('Fala', '')
        palavras = len(re.sub(r'\*\([^)]*\)\*', '', fala).replace('*', '').split())
        seg = palavras / PALAVRAS_POR_MIN * 60 + 2 * fala.count('*(pausa)*') + 2
        slides.append({'n': n, 'titulo': TITULO_CURTO.get(n, m[2]), 'fala': fala, 'seg': max(5, round(seg / 5) * 5),
                       'branco': campos.get('Se der branco'), 'passo': campos.get('Passo para')})
    tabela, resto = resto.split('## Perguntas prováveis', 1)
    reservas = [{'id': c[0], 'slide': c[1].replace('**', ''), 'pergunta': c[2].strip('"')}
                for c in re.findall(r'\| (R\d) \| (.*?) \| (.*?) \|', tabela)]
    perguntas_md, resto = resto.split('\n---', 1)
    perguntas = []
    for q, a in re.findall(r'(?ms)^\d+\. \*\*"(.*?)"\*\* (.*?)(?=^\d+\. |\Z)', perguntas_md):
        a = re.sub(r'\s+', ' ', a).strip()
        r = re.findall(r'\((R\d)\)', a)
        perguntas.append({'p': q, 'r': re.sub(r'\s*\(R\d\)', '', a), 'reserva': ', '.join(r)})
    cola_md = resto.split('## Números que não posso errar', 1)[1].split('\n---', 1)[0]
    cola = [re.sub(r'\s+', ' ', x).strip() for x in re.split(r'(?m)^- ', cola_md) if x.strip()]
    return slides, reservas, perguntas, cola


def faixa_raic() -> io.BytesIO:
    """A faixa do topo do layout 'Conteúdo' do modelo da Coordic (logo da 34ª RAIC)."""
    with zipfile.ZipFile(MODELO) as z:
        im = Image.open(io.BytesIO(z.read('ppt/media/image2.png')))
    buf = io.BytesIO()
    im.crop((0, 0, im.width, int(im.height * 0.115))).save(buf, format='PNG')
    buf.seek(0)
    return buf


# ---------------------------------------------------------------- utilidades do docx

def run(p, texto: str, tam: float = 14, bold=False, cor: str = '000000', italic=False):
    r = p.add_run(texto)
    r.bold, r.italic = bold, italic
    r.font.size = Pt(tam)
    r.font.color.rgb = RGBColor.from_string(cor)
    return r


def par(doc, antes=0, depois=6, entre=None, alinhar=None):
    p = doc.add_paragraph()
    f = p.paragraph_format
    f.space_before, f.space_after = Pt(antes), Pt(depois)
    if entre:
        f.line_spacing = entre
    if alinhar is not None:
        p.alignment = alinhar
    return p


def filete(p, cor: str = TEAL, tam: int = 8) -> None:
    ppr = p._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    for k, v in (('w:val', 'single'), ('w:sz', str(tam)), ('w:space', '2'), ('w:color', cor)):
        b.set(qn(k), v)
    bdr.append(b)
    ppr.append(bdr)


def fala(p, texto: str, tam: float = 14) -> None:
    for peca in re.split(r'(\*\([^)]*\)\*|\*\*.*?\*\*)', texto):
        if not peca:
            continue
        if peca.startswith('*('):
            run(p, f'({peca[2:-2]})', tam - 2, italic=True, cor=CINZA)
        elif peca.startswith('**'):
            run(p, peca[2:-2], tam, bold=True)
        else:
            run(p, peca, tam)


def quebra(doc) -> None:
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def numero_pagina(p) -> None:
    for tipo, texto in (('begin', None), (None, 'PAGE'), ('end', None)):
        r = p.add_run()
        r.font.size, r.font.color.rgb = Pt(10), RGBColor.from_string(CINZA)
        e = OxmlElement('w:fldChar' if tipo else 'w:instrText')
        if tipo:
            e.set(qn('w:fldCharType'), tipo)
        else:
            e.set(qn('xml:space'), 'preserve')
            e.text = texto
        r._r.append(e)


def mm_ss(s: int) -> str:
    return f'{s // 60}:{s % 60:02d}'


# ---------------------------------------------------------------- páginas

def preparar(doc) -> None:
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin = s.right_margin = Cm(2.2)
    s.top_margin, s.bottom_margin = Cm(1.8), Cm(1.6)
    estilo = doc.styles['Normal']
    estilo.font.name = 'Calibri'
    estilo.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
    estilo.font.size = Pt(12)
    rodape = s.footer.paragraphs[0]
    rodape.alignment = WD_ALIGN_PARAGRAPH.CENTER
    numero_pagina(rodape)


def pagina_tempos(doc, slides) -> None:
    doc.add_picture(faixa_raic(), width=Cm(16.6))
    p = par(doc, antes=10, depois=2)
    run(p, 'Fala na RAIC', 20, True, TEAL)
    p = par(doc, depois=12)
    run(p, '9 a 13 de novembro, Fiocruz Minas. Até 10 min de fala e uns 10 de perguntas.', 12, cor=CINZA)

    t = doc.add_table(rows=1, cols=7)
    t.style = 'Table Grid'
    for c, h in zip(t.rows[0].cells, ['Slide', '', 'Alvo', 'Acumulado', 'Ensaio 1', 'Ensaio 2', 'Ensaio 3']):
        run(c.paragraphs[0], h, 11, True, TEAL)
    acumulado = 0
    for s in slides:
        acumulado += s['seg']
        cs = t.add_row().cells
        for c, v in zip(cs, [str(s['n']), s['titulo'], f"{s['seg']} s", mm_ss(acumulado), '', '', '']):
            run(c.paragraphs[0], v, 11)
    for i, w in enumerate([1.2, 6.6, 1.5, 2.6, 1.6, 1.6, 1.6]):
        t.columns[i].width = Cm(w)
        for c in t.columns[i].cells:
            c.width = Cm(w)

    p = par(doc, antes=14, depois=4)
    run(p, 'Passou de 10 min: ', 12, True)
    run(p, 'corto, não acelero. Ordem de corte: o slide 11 (esgoto) sai e vira uma frase no 10; '
           'depois, a Tabela 1 (slide 8).', 12)
    p = par(doc, depois=4)
    run(p, 'De cor: ', 12, True)
    run(p, 'a abertura (slides 1 e 2) e as duas últimas frases do 14.', 12)


def pagina_slide(doc, s) -> None:
    if s['n'] not in JUNTO_DO_ANTERIOR:
        quebra(doc)
    p = par(doc, antes=18 if s['n'] in JUNTO_DO_ANTERIOR else 0, depois=10)
    run(p, f"{s['n']}  ", 16, True, TEAL)
    run(p, s['titulo'], 14, True, TEAL)
    filete(p)
    fala(par(doc, depois=10, entre=1.4), s['fala'])
    for rot in ('branco', 'passo'):
        if s[rot]:
            p = par(doc, depois=2)
            run(p, 'Se der branco: ' if rot == 'branco' else 'Passo para: ', 11, True, CINZA)
            run(p, s[rot], 11, cor=CINZA)
    p = par(doc, antes=10, depois=0)
    run(p, f"Alvo {s['seg']} s", 11, cor=CINZA)
    run(p, '      Tempo:  ______   ______   ______', 11, cor=CINZA_CLARO)


def pagina_perguntas(doc, perguntas) -> None:
    quebra(doc)
    p = par(doc, depois=10)
    run(p, 'Perguntas que podem fazer', 16, True, TEAL)
    filete(p)
    for i, q in enumerate(perguntas, 1):
        p = par(doc, depois=1)
        run(p, f'{i}. {q["p"]}', 12.5, True)
        p = par(doc, depois=8, entre=1.15)
        run(p, q['r'], 12)
        if q['reserva']:
            run(p, f'  → {q["reserva"]}', 12, True, TEAL)


def pagina_reservas(doc, reservas, cola) -> None:
    quebra(doc)
    if reservas:  # o deck de 30/10 não tem slides de reserva
        p = par(doc, depois=8)
        run(p, 'Reservas, depois do Obrigado', 16, True, TEAL)
        filete(p)
        for r in reservas:
            p = par(doc, depois=3)
            run(p, f'{r["id"]}  ', 12, True, TEAL)
            run(p, f'{r["slide"]}. ', 12)
            run(p, r['pergunta'], 12, italic=True, cor=CINZA)
    p = par(doc, antes=16 if reservas else 0, depois=8)
    run(p, 'Números que não posso errar', 16, True, TEAL)
    filete(p)
    for linha in cola:
        p = par(doc, depois=3)
        rot, _, resto = linha.partition(':')
        run(p, rot + ':', 12, True)
        run(p, resto, 12)


def main() -> None:
    slides, reservas, perguntas, cola = ler_roteiro()
    doc = Document()
    preparar(doc)
    pagina_tempos(doc, slides)
    for s in slides:
        pagina_slide(doc, s)
    pagina_perguntas(doc, perguntas)
    pagina_reservas(doc, reservas, cola)
    doc.save(str(SAIDA))
    total = sum(s['seg'] for s in slides)
    print(f'{SAIDA.relative_to(RAIZ)}: {len(slides)} slides, {mm_ss(total)} de fala estimada, '
          f'{len(perguntas)} perguntas, {len(reservas)} reservas')


if __name__ == '__main__':
    main()
