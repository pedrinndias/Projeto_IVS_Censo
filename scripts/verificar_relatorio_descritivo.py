"""Verificador do relatório descritivo (`relatorio_descritivo/`). Itens da §3.1 do prompt.

1. ID em todo slide e "Fontes:" nas notas (C-02: nenhuma linha Fonte no slide), na ordem do manifesto.
2. Números: cada célula de tabela do numeros.json está no slide; as descritivas DS batem
   com T03/T02; todo número dos textos de demanda aparece nas linhas do registro citadas.
3. Caminho independente: indicadores recalculados direto do .db (SQL + pandas, sem o motor),
   comparados com a T03 (n, média, mediana).
4. Figuras citadas existem.
5. Parte DS sem comparação entre indicadores.
6. Vocabulário proibido.
7. Pendências: "A CONFERIR" e "[Pedro: interpretar]".
8. (C-01) Arquivo de origem: aba Indicadores da planilha de gerenciamento × Quadro, e a linha
   "Calculado em" aponta para uma linha que cita o indicador.

Uso:  ./.venv/bin/python scripts/verificar_relatorio_descritivo.py [deck.pptx]
      (sem argumento, dados/ultimo_gerado.pptx: o deck principal é editado à mão pelo Pedro)
"""
from __future__ import annotations

import json
import random
import re
import sqlite3
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
PASTA = RAIZ / 'relatorio_descritivo'
TAB = RAIZ / 'analises_exploratorias' / '00_referencia' / 'tabelas'
DB = RAIZ / 'banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db'
DECK = Path(sys.argv[1]) if len(sys.argv) > 1 else PASTA / 'dados' / 'ultimo_gerado.pptx'
PROIBIDAS = ['vale destacar', 'é importante notar', 'em suma', 'robusto', 'abrangente',
             'vale ressaltar', 'cabe destacar']
resultado = []


def item(n, ok, msg):
    resultado.append(ok)
    print(f"{'OK   ' if ok else 'FALHA'} {n}. {msg}")


def textos_pptx(arq: Path) -> list[str]:
    with zipfile.ZipFile(arq) as z:
        nomes = sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)),
                       key=lambda n: int(re.findall(r'\d+', n)[0]))
        return [' '.join(re.findall(r'<a:t>([^<]*)</a:t>', z.read(n).decode('utf-8')))
                .replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
                for n in nomes]


def notas_pptx(arq: Path) -> list[str]:
    with zipfile.ZipFile(arq) as z:
        nomes = sorted((n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n)),
                       key=lambda n: int(re.findall(r'\d+', n)[0]))
        return [' '.join(re.findall(r'<a:t>([^<]*)</a:t>', z.read(n).decode('utf-8'))) for n in nomes]


def numeros_de(txt: str) -> set[str]:
    return set(re.findall(r'\d[\d.,]*\d|\d', txt))


def linhas_de(ref: str) -> str:
    arq, faixa = ref.rsplit(':', 1)
    a, b = (faixa.split('-') + [faixa])[:2]
    ls = (RAIZ / arq).read_text(encoding='utf-8').splitlines()
    return '\n'.join(ls[int(a) - 1:int(b)])


def main() -> None:
    import dados_relatorio_descritivo as dr
    N = json.loads((PASTA / 'dados/numeros.json').read_text(encoding='utf-8'))
    man = pd.read_csv(PASTA / 'dados/manifesto.csv', encoding='utf-8-sig')
    sl = textos_pptx(DECK)

    # 1
    notas = notas_pptx(DECK)
    falhas = [f'slide {k + 1}' for k, (t, i) in enumerate(zip(sl, man['id']))
              if i not in t or 'Fonte:' in t or k >= len(notas) or 'Fontes:' not in notas[k]]
    ok = len(sl) == len(man) and list(man['id']) == N['ordem'] and not falhas and man['id'].is_unique
    item(1, ok, f'{len(sl)} slides, {len(man)} no manifesto; sem ID, com Fonte no slide ou sem fonte nas notas: {falhas or "nenhum"}')

    # 2
    prob = []
    for k, sid in enumerate(N['ordem']):
        x, t = N['slides'][sid], sl[k]
        for ln in x.get('linhas', []) + x.get('definicao', []):
            prob += [f'{sid}: "{c}"' for c in ln if str(c) and str(c) not in t and str(c) != '—'
                     and len(str(c)) < 60]
        if sid.startswith('DS') and 'indicador' in x:
            ind = x['indicador']
            r = dr.T03.loc[ind]
            for rot, col in [('Média', 'media'), ('Mediana', 'mediana'), ('P90', 'p90'), ('Máximo', 'max')]:
                v = dict(x['linhas'])[rot]
                if v != dr.fmt(ind, r[col]):
                    prob.append(f'{sid} {rot}: {v} ≠ T03 {dr.fmt(ind, r[col])}')
        if 'fonte_texto' in x:
            fonte = '\n'.join(linhas_de(f) for f in x['fonte_texto'])
            nf = numeros_de(fonte)
            for _, txt in x['caixas']:
                prob += [f'{sid}: número "{n}" fora do registro' for n in numeros_de(txt) if n not in nf]
    item(2, not prob, 'números do JSON no slide, contra T03/T02 e contra o registro'
         + ('' if not prob else ': ' + '; '.join(prob[:6])))

    # 3 — caminho independente: Quadro (códigos V) + SQL, sem o motor
    q = pd.read_csv(RAIZ / 'banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv',
                    sep=';', encoding='utf-8-sig').set_index('indicador')
    codigos = lambda s: re.findall(r'V\d{5}', s)
    simples = q[(q['complemento'] == 'Não') & q['numerador'].str.match(r'^V\d{5}')]
    rnd = random.Random(42)
    alvos = ['pct_resp_feminino', 'iep_setor']
    alvos.append(rnd.choice(sorted(i for i in simples.index if simples.loc[i, 'dimensao'] == 'Saneamento')))
    con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    cols = {c.lower(): c for c in pd.read_sql('SELECT * FROM setores_censitarios LIMIT 1', con).columns}
    msgs, ok3 = [], True
    for ind in alvos:
        num, den = codigos(q.loc[ind, 'numerador']), codigos(q.loc[ind, 'denominador'])
        sel = ', '.join(f'"{cols[c.lower()]}"' for c in sorted(set(num + den)))
        df = pd.read_sql(f"SELECT {sel} FROM setores_censitarios WHERE CAST(urbano AS REAL) = 1 "
                         f"AND Dados_sig = 'OK'", con).apply(pd.to_numeric, errors='coerce')
        df.columns = [c.upper() for c in df.columns]
        a = df[num].sum(axis=1, min_count=1)
        b = df[den].sum(axis=1, min_count=1)
        v = (a / b.where(b > 0)) * (100 if '×100' in str(q.loc[ind, 'observacao']) else 1)
        v = v.dropna()
        r = dr.T03.loc[ind]
        bate = (len(v) == r['n'] and np.isclose(v.mean(), r['media'], rtol=1e-9)
                and np.isclose(v.median(), r['mediana'], rtol=1e-9))
        ok3 &= bool(bate)
        msgs.append(f"{ind} n {len(v)}/{int(r['n'])}" + ('' if bate else f" média {v.mean():.6g}/{r['media']:.6g}"))
    con.close()
    item(3, ok3, 'recalculado do .db: ' + '; '.join(msgs))

    # 4
    falt = [f for f in man['figura'].dropna() if f and not (PASTA / f).exists()]
    item(4, not falt, f'figuras faltando: {falt or "nenhuma"}')

    # 5
    ruins = [sid for k, sid in enumerate(N['ordem']) if sid.startswith('DS') and sid != 'DS01'
             and re.search(r'×(?!\s?\d)|\bversus\b|correlaç|comparad', sl[k], re.I)]
    item(5, not ruins, f'slides DS com comparação: {ruins or "nenhum"}')

    # 6
    voc = [f'{N["ordem"][k]}: {p}' for k, t in enumerate(sl) for p in PROIBIDAS if p in t.lower()]
    item(6, not voc, f'vocabulário proibido: {voc or "nenhum"}')

    # 8 — C-01
    ger, dif, lin = dr.GER, [], []
    for ind in q.index:
        a = sorted(x.strip() for x in str(ger.loc[ind, 'Arquivo do Censo de origem']).split('|'))
        b = sorted(x.strip() for x in str(q.loc[ind, 'arquivo_fonte']).split('|'))
        if a != b:
            dif.append(ind)
    for ind, onde in ger['Calculado em'].items():
        m = re.match(r'(\S+), .*?linha (\d+)', str(onde))
        if not m:
            lin.append(ind)
            continue
        txt = '\n'.join((RAIZ / m.group(1)).read_text(encoding='utf-8').splitlines()[int(m.group(2)) - 1:int(m.group(2)) + 2])
        chave = {'renda_media_sem_extremo': 'renda_sem_extremos', 'renda_media_mediana_mun':
                 'renda_imputada_mediana_municipal'}.get(ind, ind)
        if chave not in txt:
            lin.append(f'{ind} ({onde})')
    item(8, not dif and not lin, f'origem: {len(q) - len(dif)}/{len(q)} iguais ao Quadro '
         f'{dif or ""}; "Calculado em" sem o indicador na linha: {lin or "nenhum"}')

    # 7 (informativo)
    pend = {N['ordem'][k]: t.count('A CONFERIR') + t.count('[Pedro: interpretar]')
            for k, t in enumerate(sl)}
    pend = {k: v for k, v in pend.items() if v}
    print(f'INFO  7. pendências: {sum(pend.values())} em {pend or "nenhum slide"}')
    print('VERIFICAÇÃO ' + ('VERDE' if all(resultado) else 'VERMELHA'))
    sys.exit(0 if all(resultado) else 1)


if __name__ == '__main__':
    main()
