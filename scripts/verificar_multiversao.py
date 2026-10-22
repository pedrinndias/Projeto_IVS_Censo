"""Conferência da fatorial multiversão e das 13 apresentações (todas as fases).

    ./.venv/bin/python scripts/verificar_multiversao.py --fase N      # N = 1 a 7

Cada fase confere o que ela grava; sai com código 1 se algo falhar. Fases 5 a 7 leem o XML do .pptx
com zipfile (sem python-pptx): número de slides igual ao do JSON, o ID de cada slide no texto dele,
nenhum "nan"/"inf" no texto, e toda fonte citada existindo no disco.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
import fatorial_multiversao as fm  # noqa: E402

MV = fm.SAIDA
PASTA = RAIZ / 'apresentacoes_multiversao'
falhas: list[str] = []


def checa(ok: bool, msg: str) -> None:
    print(('  ok   ' if ok else '  FALHA ') + msg)
    if not ok:
        falhas.append(msg)


def fase1() -> None:
    s = pd.read_csv(MV / 'camada1_subconjuntos.csv')
    checa(len(s) == 2 * 4017 and s['codigos'].nunique() == 4017, f'4.017 combinações × 2 réguas ({len(s)} linhas)')
    checa(s['kmo'].between(0, 1).all(), 'KMO entre 0 e 1')
    e = pd.read_csv(MV / 'camada1_efeito_variavel.csv')
    checa(len(e) == 24 and (e['pares'] > 0).all(), 'efeito de cada variável: 12 × 2 réguas, todas com pares')
    nuc = s[(s['codigos'] == '+'.join(fm.NUCLEO)) & (s['regua'] == 'global')].iloc[0]
    checa(abs(nuc['kmo'] - 0.7826) < 0.001, f"trava: KMO do núcleo no conjunto = NB04 (0,7826): {nuc['kmo']:.4f}")
    for a in ('12', 'nucleo'):
        for r in fm.REGUAS:
            checa((MV / f'camada1_{a}_{r}_cargas.csv').exists(), f'camada1_{a}_{r}_*.csv')


def fase2() -> None:
    e = pd.read_csv(MV / 'camada2_especificacoes.csv')
    esperado = (13 + 2 * 12) * 9 * 3       # 13 conjuntos; os 12 com analfabetismo têm mais 2 políticas de sigilo
    checa(len(e) == esperado, f'{esperado} especificações ({len(e)})')
    checa((e['eixo'] == 'referencia').sum() == 1, 'uma referência')
    ref = e[e['eixo'] == 'referencia'].iloc[0]
    checa(ref['spearman_mun'] > 0.999 and ref['troca_faixa'] == 0, 'a referência comparada consigo dá 1 e 0')
    checa(set(pd.read_csv(MV / 'camada2_efeito_eixo.csv')['eixo']) == {'conjunto', 'sigilo', 'normalizacao', 'rotacao_peso'},
          'veredito dos 4 eixos')


def fase3() -> None:
    f = pd.read_csv(MV / 'camada3_finalistas.csv')
    checa(1 <= len(f) <= 6 and (f['papel'] == 'proposta').sum() == 1, f'{len(f)} finalistas, uma proposta')
    est = pd.read_csv(MV / 'camada3_estabilidade.csv')
    checa((est.groupby('id').size() == 70).all(), '70 rodadas de estabilidade por finalista')
    v = pd.read_csv(MV / 'ivs_proposto_por_setor.csv')
    checa(len(v) == 104108 and v['ivs'].dropna().between(0, 1).all(), 'IVS por setor: 104.108 linhas, entre 0 e 1')
    checa(set(v['faixa_ivs_bh'].dropna().unique()) <= {-1, 0, 1, 2, 3}, 'faixas válidas')
    r = pd.read_csv(MV / 'camada3_replicacao.csv').set_index('id')
    checa(r.loc[f.loc[f['rotacao'] == 'sem_rotacao', 'id'], 'tucker_F2'].isna().all(),
          'sem rotação há um fator só: o Tucker do F2 é ausente')


def fase4() -> None:
    for js in sorted((PASTA / 'dados').glob('*.json')):
        n = json.loads(js.read_text(encoding='utf-8'))
        txt = json.dumps(n['slides'], ensure_ascii=False)
        checa(not re.search(r'\b(nan|NaN|inf)\b', txt), f'{js.name}: sem nan/inf')
        figs = [x['figura'] for x in n['slides'].values() if x.get('figura')]
        checa(all((PASTA / f).exists() for f in figs), f'{js.name}: {len(figs)} figuras existem')
        conteudo = {k: x for k, x in n['slides'].items()
                    if not any(x.get(c) for c in ('capa', 'numero', 'blocos', 'duas', 'matriz'))}
        sem_exp = [k for k, x in conteudo.items()
                   if not {'O que é.', 'Como ler.'} <= {e for e, _ in x.get('explica', [])}]
        checa(not sem_exp, f'{js.name}: os {len(conteudo)} slides de conteúdo têm "O que é" e "Como ler" {sem_exp[:3]}')
        checa(all(x.get('legenda') for x in conteudo.values() if x.get('figura')), f'{js.name}: toda figura tem legenda')
        fontes = {re.split(r'[,;]', f)[0].strip() for x in n['slides'].values() for f in x.get('fontes', [])}
        fontes = {f for f in fontes if '/' in f}
        checa(all((RAIZ / f).exists() for f in fontes), f'{js.name}: {len(fontes)} fontes citadas existem')
    fin = (PASTA / 'dados' / 'FIN.json').read_text(encoding='utf-8')
    checa('troca duas coisas juntas' in fin and 'junto com a régua' in fin,
          'FIN: o "Como ler" e as limitações avisam que a normalização por postos também troca a matriz')
    checa(len(list((PASTA / 'dados').glob('*.json'))) == 13, '13 decks com dados')
    checa((PASTA / 'Fatorial_Multiversao_numeros.xlsx').exists(), 'planilha de números')


def deck(cod: str) -> None:
    n = json.loads((PASTA / 'dados' / f'{cod}.json').read_text(encoding='utf-8'))
    p = PASTA / n['arquivo']
    if not p.exists():
        checa(False, f'{n["arquivo"]} existe')
        return
    z = zipfile.ZipFile(p)
    slides = sorted((x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', x)),
                    key=lambda x: int(re.findall(r'\d+', x)[0]))
    checa(len(slides) == len(n['ordem']), f'{p.name}: {len(slides)} slides = {len(n["ordem"])} do JSON')
    sem_id, com_nan = [], []
    for sid, x in zip(n['ordem'], slides):
        t = ''.join(re.findall(r'<a:t>([^<]*)</a:t>', z.read(x).decode('utf-8')))
        if sid not in t:
            sem_id.append(sid)
        if re.search(r'\b(nan|NaN|inf)\b', t):
            com_nan.append(sid)
    checa(not sem_id, f'{p.name}: o ID de cada slide está nele {sem_id[:3]}')
    checa(not com_nan, f'{p.name}: sem nan/inf no texto {com_nan[:3]}')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--fase', type=int, required=True)
    f = ap.parse_args().fase
    print(f'Fase {f}')
    if f == 1:
        fase1()
    elif f == 2:
        fase2()
    elif f == 3:
        fase3()
    elif f == 4:
        fase4()
    elif f == 5:
        deck('REN')
    elif f == 6:
        for c in fm.VARS:
            deck(c)
    elif f == 7:
        deck('FIN')
    print('VERDE' if not falhas else f'{len(falhas)} FALHA(S)')
    sys.exit(1 if falhas else 0)


if __name__ == '__main__':
    main()
