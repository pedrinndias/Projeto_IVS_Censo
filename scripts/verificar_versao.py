#!/usr/bin/env python
"""Conferências de uma versão das análises exploratórias, num comando só.

    ./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/<versao> [--sem-pytest]

1. `pytest` passa;
2. o deck (se já existe) vira PDF pelo LibreOffice com uma página por slide; nenhuma
   caixa de texto estoura (estimativa de linhas × altura) e nenhuma figura sai do slide;
3. todo número dos campos de cada item do catálogo existe no CSV do mesmo ID (ou no
   CSV-fonte, no caso das figuras);
4. nenhuma palavra proibida nos decks, READMEs e textos da versão;
5. o `catalogo.csv` cobre todo arquivo de `tabelas/` e `figuras/`, e todo slide apontado
   existe e traz o ID do item.

Saída de no máximo 20 linhas; código de saída 1 se alguma conferência falhar.
"""
import json
import math
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
MODELOS = RAIZ / 'analises_exploratorias' / '_modelos' / 'textos_blocos.json'
NUMERO = re.compile(r'^-?(\d{1,3}(\.\d{3})+|\d+)(,\d+)?%?$')
PROIBIDAS = re.compile(r'\b(claude|anthropic|chatgpt|openai|copilot|llm|prompt|assistente|'
                       r'intelig[êe]ncia artificial|sess[ãa]o|gerad[oa] automaticamente)\b', re.I)
EMU = 914400


def numero(txt):
    t = txt.rstrip('%')
    d = len(t.split(',')[1]) if ',' in t else 0
    return float(t.replace('.', '').replace(',', '.')), d


def celulas(csv: Path) -> np.ndarray:
    df = pd.read_csv(csv)
    v = pd.concat([pd.to_numeric(df[c], errors='coerce') for c in df.columns]).dropna()
    return v.to_numpy(float)


def conferir_numeros(pasta: Path, cat: pd.DataFrame) -> list:
    erros = []
    for _, r in cat.iterrows():
        csv = next((pasta / 'tabelas').glob(f"{r['fonte']}_*.csv"), None)
        if csv is None:
            erros.append(f"{r['id']}: CSV-fonte {r['fonte']} não encontrado")
            continue
        vals = celulas(csv)
        for k, txt in json.loads(r['campos']).items():
            if not isinstance(txt, str) or not NUMERO.match(txt):
                continue
            x, d = numero(txt)
            tol = 0.5 * 10 ** -d + 1e-9
            if not (np.any(np.abs(vals - x) <= tol) or np.any(np.abs(100 * vals - x) <= tol)):
                erros.append(f"{r['id']}: {k} = {txt} não está em {csv.name}")
    return erros


def textos_pptx(pptx: Path):
    """Texto de cada slide (com as notas) e o XML de cada slide, na ordem."""
    with zipfile.ZipFile(pptx) as z:
        nomes = sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)),
                       key=lambda n: int(re.findall(r'\d+', n)[-1]))
        xmls = [z.read(n).decode('utf-8') for n in nomes]
        notas = {int(re.findall(r'\d+', n)[-1]): z.read(n).decode('utf-8') for n in z.namelist()
                 if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n)}
        pres = z.read('ppt/presentation.xml').decode('utf-8')
    tam = re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', pres)
    texto = [' '.join(re.findall(r'<a:t>([^<]*)</a:t>', x)) for x in xmls]
    nota = [' '.join(re.findall(r'<a:t>([^<]*)</a:t>', notas.get(i + 1, ''))) for i in range(len(xmls))]
    return texto, nota, xmls, (int(tam.group(1)), int(tam.group(2)))


def estouros(xmls, tam) -> list:
    """Estimativa grosseira: linhas necessárias × altura da fonte contra a altura da caixa."""
    ruins = set()
    for i, x in enumerate(xmls, 1):
        for sp in re.findall(r'<p:sp>.*?</p:sp>', x, re.S):
            ext = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', sp)
            if not ext or '<a:t>' not in sp:
                continue
            _, _, cx, cy = map(int, ext.groups())
            larg = cx / EMU - 0.2
            alt = 0.0
            for p in re.findall(r'<a:p>.*?</a:p>', sp, re.S):
                t = ''.join(re.findall(r'<a:t>([^<]*)</a:t>', p))
                sz = re.search(r'sz="(\d+)"', p)
                pt = int(sz.group(1)) / 100 if sz else 18
                linhas = max(1, math.ceil(len(t) * 0.5 * pt / 72 / max(larg, 0.1)))
                alt += linhas * pt * 1.2 / 72
            if alt > 1.15 * (cy / EMU - 0.1) + 0.05:
                ruins.add(i)
        for pic in re.findall(r'<p:pic>.*?</p:pic>', x, re.S):
            ext = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', pic)
            if ext:
                ox, oy, cx, cy = map(int, ext.groups())
                if ox < 0 or oy < 0 or ox + cx > tam[0] * 1.001 or oy + cy > tam[1] * 1.001:
                    ruins.add(i)
    return sorted(ruins)


def paginas_pdf(pptx: Path) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, str(pptx)],
                       capture_output=True, timeout=600)
        pdf = Path(tmp) / (pptx.stem + '.pdf')
        return len(re.findall(rb'/Type\s*/Page[^s]', pdf.read_bytes())) if pdf.exists() else -1


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 1:
        sys.exit('uso: verificar_versao.py analises_exploratorias/<versao> [--sem-pytest]')
    pasta = Path(args[0]).resolve()
    saida, falhou = [f'Verificação de {pasta.name}'], False

    def linha(ok, msg, detalhes=()):
        nonlocal falhou
        falhou |= not ok
        saida.append(f"[{'ok' if ok else 'FALHA'}] {msg}")
        saida.extend(f'    {d}' for d in list(detalhes)[:3])

    # 1. pytest
    if '--sem-pytest' in sys.argv:
        saida.append('[--] pytest pulado (--sem-pytest)')
    else:
        r = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider'], cwd=RAIZ,
                           capture_output=True, text=True)
        fim = (r.stdout.strip().splitlines() or ['sem saída'])[-1]
        linha(r.returncode == 0, f'pytest: {fim}')

    cat = pd.read_csv(pasta / 'catalogo.csv', dtype={'slide': str}, keep_default_na=False)

    # 5. catálogo × arquivos
    arquivos = {str(p.relative_to(pasta)) for sub in ('tabelas', 'figuras') for p in (pasta / sub).glob('*.*')}
    no_cat = set(cat['arquivo'])
    linha(arquivos == no_cat and cat['id'].is_unique,
          f'catálogo: {len(cat)} itens, {len(arquivos)} arquivos',
          [f'sem linha: {a}' for a in sorted(arquivos - no_cat)] + [f'sem arquivo: {a}' for a in sorted(no_cat - arquivos)])

    # 3. números dos campos
    erros = conferir_numeros(pasta, cat)
    linha(not erros, f'números dos campos: {len(erros)} sem correspondência no CSV', erros)

    # 2 e 4. deck
    decks = sorted(pasta.glob('*.pptx'))
    textos_livres = [p for p in [pasta / 'README.md', pasta / 'textos.json', pasta / 'catalogo.csv', MODELOS] if p.exists()]
    achados = [f'{p.name}: {m.group(0)}' for p in textos_livres for m in PROIBIDAS.finditer(p.read_text(encoding='utf-8'))]
    if not decks:
        saida.append('[--] deck ainda não gerado: conferências de PDF, caixas e slides puladas')
    for deck in decks:
        texto, nota, xmls, tam = textos_pptx(deck)
        n = len(texto)
        pags = paginas_pdf(deck)
        linha(pags == n, f'{deck.name}: {n} slides, PDF com {pags} páginas')
        ruins = estouros(xmls, tam)
        linha(not ruins, f'caixas de texto ou figuras fora do lugar: {len(ruins)} slides',
              [f'slides {", ".join(map(str, ruins[:15]))}'] if ruins else [])
        sem = [f"{r['id']} → slide {r['slide']}" for _, r in cat.iterrows()
               if not r['slide'] or not r['slide'].isdigit() or not 1 <= int(r['slide']) <= n
               or r['id'] not in texto[int(r['slide']) - 1]]
        linha(not sem, f'slides do catálogo: {len(sem)} itens sem slide válido com o ID', sem)
        achados += [f'{deck.name} slide {i + 1}: {m.group(0)}' for i, t in enumerate(texto)
                    for m in PROIBIDAS.finditer(t + ' ' + nota[i])]
    linha(not achados, f'palavras proibidas: {len(achados)}', achados)

    print('\n'.join(saida[:20]))
    return 1 if falhou else 0


if __name__ == '__main__':
    sys.exit(main())
