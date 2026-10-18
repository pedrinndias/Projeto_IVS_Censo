"""Verificador das 108 versões da análise fatorial (§3 do prompt das 108 versões).

1. Enumerador: 108 IDs únicos, sem as duas águas, batendo com versoes_fatorial/VERSOES.md.
2. Trava: as versões equivalentes às do NB05 batem com especificacoes.csv; V023 = 73.878, elegível.
3. Caminho independente: duas versões novas sorteadas (semente 42) refeitas com as colunas lidas
   do .db por SQL, sem o laço do motor; n e KMO têm de bater.
4. Decks: IDs na ordem, nenhuma "Fonte:" no slide, "Fontes:" nas notas; toda célula das tabelas
   do numeros.json aparece no slide.
5. Números: KMO, n e cargas de cada ficha recomparados com versoes.csv e cargas.csv.
6. Vocabulário proibido e "melhor"/"escolhida" junto de um código de versão.
7. Pendências (informativo).

Uso:  ./.venv/bin/python scripts/verificar_versoes_fatorial.py
"""
from __future__ import annotations

import json
import random
import re
import sqlite3
import sys
import zipfile
from html import unescape
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
sys.path.insert(0, str(RAIZ / 'src'))
PASTA = RAIZ / 'versoes_fatorial'
RES = RAIZ / 'banco_de_dados' / 'eda' / 'versoes_fatorial'
DB = RAIZ / 'banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db'
PROIBIDAS = ['vale destacar', 'é importante notar', 'em suma', 'robusto', 'abrangente', 'vale ressaltar']
ok_geral = []


def item(n, ok, msg):
    ok_geral.append(ok)
    print(f"{'OK   ' if ok else 'FALHA'} {n}. {msg}")


def texto(no: str) -> str:
    return ' '.join(''.join(unescape(t) for t in re.findall(r'<a:t>([^<]*)</a:t>', p))
                    for p in re.findall(r'<a:p>.*?</a:p>', no, re.S))


def ler(arq: Path, pasta: str) -> list[str]:
    with zipfile.ZipFile(arq) as z:
        nomes = sorted((n for n in z.namelist() if re.fullmatch(rf'ppt/{pasta}/\w+?\d+\.xml', n)),
                       key=lambda n: int(re.findall(r'\d+', n.split('/')[-1])[0]))
        return [texto(z.read(n).decode('utf-8')) for n in nomes]


def main() -> None:
    import versoes_fatorial as vf
    import dados_versoes_fatorial as dv
    from ivs_censo.fatorial import rodar_cenario
    V = pd.read_csv(RES / 'versoes.csv', keep_default_na=False, na_values=[''])
    C = pd.read_csv(RES / 'cargas.csv')
    N = json.loads((PASTA / 'dados' / 'numeros.json').read_text(encoding='utf-8'))

    # 1
    lista = vf.versoes()
    md = (PASTA / 'VERSOES.md').read_text(encoding='utf-8')
    linhas = dict(re.findall(r'^\| (V\d{3}) \| ([^|]+) \|', md, re.M))
    ok = (len(lista) == 108 == len({x['id'] for x in lista}) == len(V)
          and not any({'pct_agua_nao_encanada', 'pct_sem_agua_canalizada'} <= set(x['colunas']) for x in lista)
          and all(linhas[x['id']].strip() == dict(vf.EIXOS['renda'])[x['renda']] for x in lista)
          and list(V['id']) == [x['id'] for x in lista])
    item(1, ok, '108 versões únicas, sem as duas águas, iguais a VERSOES.md e a versoes.csv')

    # 2
    V['elegivel'] = V['elegivel'].astype(str).str.lower().eq('true')
    V['id_nb05'] = V['id_nb05'].fillna('')
    erros = vf.conferir_trava(V)
    item(2, not erros, f"trava: {int((V['id_nb05'] != '').sum())} versões do NB05 conferidas; "
         + ('; '.join(erros[:4]) if erros else 'tudo bate; V023 com 73.878 e elegível'))

    # 3 — caminho independente: SQL + rodar_cenario, sem montar nem o laço do motor
    novas = [x for x in lista if not vf.id_nb05(x)]
    alvo = random.Random(42).sample(novas, 2)
    con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    base = pd.read_sql("SELECT * FROM setores_censitarios WHERE CAST(urbano AS REAL) = 1 AND Dados_sig = 'OK'", con)
    con.close()
    base = base.apply(lambda s: pd.to_numeric(s, errors='coerce') if s.name not in ('CD_SETOR', 'NM_MUN', 'Dados_sig') else s)
    tot = base['V00001'].where(base['V00001'] > 0)
    base['banheiro_graduado'] = (base['V00236'] + 2 * base['V00237'] + 3 * base['V00238']) / (3 * tot)
    renda = {'original': 'renda_media', 'sem_extremo': 'renda_media_sem_extremo', 'mediana_mun': 'renda_media_mediana_mun'}
    msgs, ok3 = [], True
    for x in alvo:
        cols = x['colunas']
        b = base.copy()
        b['renda_inv'] = -b[renda[x['renda']]]
        d = b[cols].dropna()
        r = rodar_cenario(d.to_numpy())
        v = V.set_index('id').loc[x['id']]
        bate = len(d) == int(v['n']) and np.isclose(r['kmo'], v['kmo'], rtol=1e-6)
        ok3 &= bool(bate)
        msgs.append(f"{x['id']} n {len(d)}/{int(v['n'])} KMO {r['kmo']:.6f}/{v['kmo']:.6f}")
    item(3, ok3, 'refeito do .db: ' + '; '.join(msgs))

    # 4
    prob = []
    for deck, arq in (('principal', 'Versoes_Fatorial_Principal.pptx'), ('caderno', 'Caderno_Fichas_108.pptx')):
        sl, nt = ler(PASTA / arq, 'slides'), ler(PASTA / arq, 'notesSlides')
        ordem = N[deck]['ordem']
        if len(sl) != len(ordem):
            prob.append(f'{deck}: {len(sl)} slides, {len(ordem)} no json')
        for k, sid in enumerate(ordem[:len(sl)]):
            t = sl[k]
            if sid not in t or 'Fonte:' in t or k >= len(nt) or 'Fontes:' not in nt[k]:
                prob.append(f'{deck} {sid}: ID/fonte')
            x = N[deck]['slides'][sid]
            for campo in ('linhas', 'versao', 'adequacao', 'cargas', 'valid'):
                for ln in x.get(campo, []):
                    prob += [f'{sid}: "{c}"' for c in ln if str(c) and str(c) not in t and len(str(c)) < 60]
    item(4, not prob, 'decks: IDs, fontes só nas notas, células no slide' + ('' if not prob else ': ' + '; '.join(prob[:5])))

    # 5
    erros = []
    for _, v in V.iterrows():
        f = N['caderno']['slides'][v['id']]
        ad, ve = dict(f['adequacao']), dict(f['versao'])
        if ad['KMO'] != dv.br(v['kmo'], 4) or ve['Setores (amostra própria)'] != dv.intbr(v['n']):
            erros.append(v['id'])
        cc = C[C['id'] == v['id']].sort_values('ordem')
        if len(f['cargas']) != len(cc) or len(cc) != int(v['p']) or any(
                a[1] != dv.br(b, 3) for a, b in zip(f['cargas'], cc['f1'])):
            erros.append(v['id'] + ' cargas')
    item(5, not erros, f"fichas contra versoes.csv e cargas.csv: {erros[:5] or 'tudo bate'}")

    # 6
    voc = []
    for deck, arq in (('principal', 'Versoes_Fatorial_Principal.pptx'), ('caderno', 'Caderno_Fichas_108.pptx')):
        for k, t in enumerate(ler(PASTA / arq, 'slides')):
            lo = t.lower()
            voc += [f'{deck} {k + 1}: {p}' for p in PROIBIDAS if p in lo]
            if re.search(r'(?<!não )\b(melhor|escolhida)\b', lo) and re.search(r'V\d{3}', t):
                voc.append(f'{deck} {k + 1}: melhor/escolhida')
    item(6, not voc, f'vocabulário: {voc[:5] or "nenhum problema"}')

    # 7
    pend = sum(t.count('A CONFERIR') for arq in ('Versoes_Fatorial_Principal.pptx', 'Caderno_Fichas_108.pptx')
               for t in ler(PASTA / arq, 'slides'))
    print(f'INFO  7. "A CONFERIR" nos dois decks: {pend}')
    print('VERIFICAÇÃO ' + ('VERDE' if all(ok_geral) else 'VERMELHA'))
    sys.exit(0 if all(ok_geral) else 1)


if __name__ == '__main__':
    main()
