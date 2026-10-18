"""Lista o que o Pedro mudou à mão nas tabelas de uma cópia do relatório descritivo.

O deck é regerado do zero a cada lote ou correção, e isso apagaria edições feitas no
PowerPoint. Este script compara, slide a slide e célula a célula, as tabelas da cópia
editada com as do deck gerado e grava cada diferença com o ID do slide, para a mudança ser
levada à origem (protocolo de correção, seção 5 do prompt) antes de regerar.

Uso:  ./.venv/bin/python scripts/comparar_edicoes_relatorio.py [deck_editado.pptx]
      (sem argumento, compara o deck principal, que o Pedro edita, com dados/ultimo_gerado.pptx)
Saída: relatorio_descritivo/dados/edicoes_do_pedro.csv (e as primeiras linhas na tela)
"""
from __future__ import annotations

import re
import sys
import zipfile
from html import unescape
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
PASTA = RAIZ / 'relatorio_descritivo'
GERADO = PASTA / 'dados' / 'ultimo_gerado.pptx'          # o último deck gerado, intocado
PRINCIPAL = PASTA / 'Relatorio_Descritivo_IVS_2026-10.pptx'


ID = re.compile(r'^(A|DM|DS|FA|FP|Z)\d{2}$')


def texto(no: str) -> str:
    """Texto de um trecho de XML: os pedaços (runs) de um parágrafo juntos, sem espaço — o
    PowerPoint quebra uma palavra em vários pedaços ao editar —, e os parágrafos separados."""
    return ' '.join(''.join(unescape(t) for t in re.findall(r'<a:t>([^<]*)</a:t>', par))
                    for par in re.findall(r'<a:p>.*?</a:p>', no, re.S)).strip()


def slides(arq: Path) -> dict[str, list]:
    """{ID do slide: tabelas}. O ID é a caixa de texto do canto (DM02, DS20…); slide sem ID
    fica como 'sem ID n'. Assim, apagar ou mover slides não desalinha a comparação."""
    out = {}
    with zipfile.ZipFile(arq) as z:
        nomes = sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)),
                       key=lambda n: int(re.findall(r'\d+', n)[0]))
        for k, n in enumerate(nomes):
            xml = z.read(n).decode('utf-8')
            ids = [t for t in (texto(sp) for sp in re.findall(r'<p:sp>.*?</p:sp>', xml, re.S)) if ID.match(t)]
            tabs = [[[texto(tc) for tc in re.findall(r'<a:tc[ >].*?</a:tc>', tr, re.S)]
                     for tr in re.findall(r'<a:tr[ >].*?</a:tr>', tb, re.S)]
                    for tb in re.findall(r'<a:tbl>.*?</a:tbl>', xml, re.S)]
            out[ids[0] if ids else f'sem ID {k + 1}'] = tabs
    return out


def main() -> None:
    editado = Path(sys.argv[1]) if len(sys.argv) > 1 else PRINCIPAL
    a, b = slides(GERADO), slides(editado)
    sumidos = [k for k in a if k not in b]
    novos = [k for k in b if k not in a]
    print(f'Gerado: {len(a)} slides; editado: {len(b)}. Apagados: {sumidos or "nenhum"}. '
          f'Novos ou sem ID: {novos or "nenhum"}.')
    difs = []
    for sid in (k for k in a if k in b):
        for t, (xa, xb) in enumerate(zip(a[sid], b[sid])):
            for i in range(max(len(xa), len(xb))):
                la = xa[i] if i < len(xa) else []
                lb = xb[i] if i < len(xb) else []
                for j in range(max(len(la), len(lb))):
                    va = la[j] if j < len(la) else '(não existe)'
                    vb = lb[j] if j < len(lb) else '(não existe)'
                    if ' '.join(va.split()) != ' '.join(vb.split()):
                        difs.append(dict(slide=sid, tabela=t + 1, linha=i, coluna=j + 1,
                                         rotulo_da_linha=(la or lb or [''])[0], gerado=va, editado=vb))
        if len(a[sid]) != len(b[sid]):
            difs.append(dict(slide=sid, tabela=0, linha=0, coluna=0, rotulo_da_linha='(nº de tabelas)',
                             gerado=str(len(a[sid])), editado=str(len(b[sid]))))
    for k in sumidos:
        difs.append(dict(slide=k, tabela=0, linha=0, coluna=0, rotulo_da_linha='(slide apagado)',
                         gerado='existe', editado='apagado'))
    df = pd.DataFrame(difs, columns=['slide', 'tabela', 'linha', 'coluna', 'rotulo_da_linha', 'gerado', 'editado'])
    saida = PASTA / 'dados' / 'edicoes_do_pedro.csv'
    df.to_csv(saida, index=False, encoding='utf-8-sig')
    print(f'{len(df)} diferenças em {df["slide"].nunique()} slides → {saida.relative_to(RAIZ)}')
    if len(df):
        print(df.head(25).to_string(index=False, max_colwidth=38))


if __name__ == '__main__':
    main()
