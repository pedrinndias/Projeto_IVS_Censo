#!/usr/bin/env python
"""A síntese das análises exploratórias por versão (lote 6).

    ./.venv/bin/python scripts/sintese_versoes.py

Lê o que cada versão gravou e produz, sem recalcular nenhum índice:

* `analises_exploratorias/00_sintese/` — tabelas, figuras e `catalogo.csv` da comparação
  entre todas as versões (bloco 20), no formato das versões, para o mesmo gerador de deck;
* `analises_exploratorias/Catalogo_Mestre.xlsx` — todas as tabelas e figuras de todas as
  versões, com as colunas de escolha (Vai para o artigo? · Seção · Comentários);
* `analises_exploratorias/README.md` — o índice: uma linha por versão, com status, n e deck.

A comparação é descritiva: nenhuma versão é "a melhor".
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eda_versoes as ev  # noqa: E402
from eda_versoes import ARGILA, CINZA, PETROLEO, br, estilo, intbr, pctbr, plt  # noqa: E402

PASTAS = ev.RAIZ / 'analises_exploratorias'
SINTESE = PASTAS / '00_sintese'
EIXOS = {'00': 'Referência', 'A': 'A — que setores entram', 'B': 'B — que indicadores entram',
         'C': 'C — como o índice é construído', 'D': 'D — índices novos ao lado do IVS',
         'E': 'E — análises que atravessam as versões'}


def tab(pasta, prefixo):
    f = next((pasta / 'tabelas').glob(f'{prefixo}_*.csv'), None)
    return pd.read_csv(f) if f else None


def valor(t, medida):
    return float(t.loc[t['medida'] == medida, 'valor'].iloc[0]) if t is not None and (t['medida'] == medida).any() else np.nan


def pastas_de_versao():
    return sorted(p.parent for p in PASTAS.glob('**/catalogo.csv') if '00_sintese' not in str(p))


def linha_da_versao(pasta):
    nome = str(pasta.relative_to(PASTAS))
    cfg = json.loads((pasta / 'config.json').read_text(encoding='utf-8'))
    t01, t19, t24, t26 = tab(pasta, 'T01'), tab(pasta, 'T19'), tab(pasta, 'T24'), tab(pasta, 'T26')
    t31, t33 = tab(pasta, 'T31'), tab(pasta, 'T33')
    n_ind = t24['n'].iloc[0] if t24 is not None else (valor(t19, 'setores (n)') if t19 is not None else np.nan)
    return {'versao': nome, 'eixo': EIXOS['00' if nome.startswith('00') else nome[0]], 'titulo': cfg.get('titulo', ''),
            'setores_recorte': (t01.iloc[-2]['setores'] if t01 is not None and len(t01) > 1 else np.nan),
            'setores_indice': n_ind, 'kmo': valor(t19, 'KMO'),
            'auc_global': valor(t26, 'AUC global contra FCU'), 'auc_municipal': valor(t26, 'AUC municipal (mediana)'),
            'elegivel': valor(t26, 'elegível pelos critérios do NB05'),
            'spearman_com_referencia': t31['spearman'].iloc[0] if t31 is not None else np.nan,
            'pct_mudam_faixa': t33['pct_mudam'].iloc[0] if t33 is not None else np.nan,
            'deck': next((str(p.relative_to(PASTAS)) for p in pasta.glob('*.pptx')), '')}


def sintese(S, linhas):
    t = linhas[~linhas['versao'].str.startswith('E')].drop(columns='deck')
    u = t[t['versao'] != '00_referencia'].dropna(subset=['spearman_com_referencia'])
    a = u.loc[u['spearman_com_referencia'].idxmin()]
    c60 = {'n_eleg': intbr((t['elegivel'] == 1).sum()), 'versao_min': a['versao'], 'rho_min': br(a['spearman_com_referencia'])}
    # o número de versões elegíveis tem de ser célula: vai na tabela por eixo (T61)
    S.tabela('T60', 'todas_as_versoes', 20, 'sint_tabela', t, {k: v for k, v in c60.items() if k != 'n_eleg'})
    e = t.groupby('eixo').agg(versoes=('versao', 'size'), elegiveis=('elegivel', lambda s: int((s == 1).sum())),
                              auc_municipal_min=('auc_municipal', 'min'), auc_municipal_max=('auc_municipal', 'max'),
                              pct_mudam_max=('pct_mudam_faixa', 'max')).reset_index()
    tot = pd.DataFrame([{'eixo': 'Todas', 'versoes': int(e['versoes'].sum()), 'elegiveis': int(e['elegiveis'].sum()),
                         'auc_municipal_min': t['auc_municipal'].min(), 'auc_municipal_max': t['auc_municipal'].max(),
                         'pct_mudam_max': t['pct_mudam_faixa'].max()}])
    e = pd.concat([e, tot], ignore_index=True)
    c61 = {'n_versoes': intbr(tot['versoes'].iloc[0]), 'n_eleg': intbr(tot['elegiveis'].iloc[0]),
           'auc_min': br(tot['auc_municipal_min'].iloc[0]), 'auc_max': br(tot['auc_municipal_max'].iloc[0])}
    S.tabela('T61', 'versoes_por_eixo', 20, 'sint_eixos', e, c61)
    v = t.dropna(subset=['spearman_com_referencia', 'auc_municipal'])
    fig, ax = plt.subplots(figsize=(9, 6))
    for ok, cor, rot in ((1, PETROLEO, 'elegível'), (0, ARGILA, 'não elegível')):
        x = v[v['elegivel'] == ok]
        ax.scatter(x['spearman_com_referencia'], x['auc_municipal'], color=cor, s=28, label=rot)
        for _, r in x.iterrows():
            ax.annotate(r['versao'].split('/')[-1][:18], (r['spearman_com_referencia'], r['auc_municipal']),
                        fontsize=6, color=CINZA, xytext=(3, 2), textcoords='offset points')
    ax.axhline(v.loc[v['versao'] == '00_referencia', 'auc_municipal'].iloc[0], color=CINZA, lw=0.6, ls=':')
    ax.legend(frameon=False, fontsize=8)
    estilo(ax, 'Correlação de postos com o índice da referência', 'AUC municipal contra FCU (mediana)')
    S.figura('F60', 'proximidade_x_auc', 20, 'sint_disp', fig, 'T60', {k: v for k, v in c60.items() if k != 'n_eleg'})
    w = t.dropna(subset=['pct_mudam_faixa']).sort_values('pct_mudam_faixa')
    w = w[w['versao'] != '00_referencia']
    fig, ax = plt.subplots(figsize=(8, 0.22 * len(w) + 1.2))
    ax.barh(w['versao'], w['pct_mudam_faixa'], color=[PETROLEO if x == 1 else ARGILA for x in w['elegivel']])
    ax.tick_params(axis='y', labelsize=6)
    estilo(ax, '% dos setores que mudam de faixa em relação à referência (petróleo: elegível; argila: não elegível)')
    m = w.iloc[-1]
    S.figura('F61', 'mudam_de_faixa', 20, 'sint_barras', fig, 'T60',
             {'versao_max': m['versao'], 'pct_max': pctbr(m['pct_mudam_faixa'])})


def catalogo_mestre(linhas):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Catálogo mestre'
    cab = ['Versão', 'Eixo', 'ID', 'Tipo', 'Bloco', 'Título no deck', 'O que mostra', 'Arquivo', 'Deck', 'Slide',
           'Vai para o artigo?', 'Seção', 'Comentários']
    ws.append(cab)
    for p in pastas_de_versao():
        nome = str(p.relative_to(PASTAS))
        eixo = EIXOS['00' if nome.startswith('00') else nome[0]] if not nome.startswith('00_sintese') else 'Síntese'
        deck = next((str(x.relative_to(PASTAS)) for x in p.glob('*.pptx')), '')
        for _, r in pd.read_csv(p / 'catalogo.csv', dtype=str, keep_default_na=False).iterrows():
            ws.append([nome, eixo, r['id'], r['tipo'], int(r['bloco']), r['titulo'], r['o_que_mostra'],
                       f"{nome}/{r['arquivo']}", deck, int(r['slide']) if r['slide'].isdigit() else '', '', '', ''])
    for c in ws[1]:
        c.font = Font(bold=True)
    larguras = [28, 30, 6, 8, 6, 60, 70, 48, 40, 6, 16, 16, 40]
    for i, w in enumerate(larguras):
        ws.column_dimensions[chr(65 + i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row[5:7]:
            c.alignment = Alignment(wrap_text=True, vertical='top')
    dv = DataValidation(type='list', formula1='"Sim,Não,Talvez"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f'K2:K{ws.max_row}')
    ws.freeze_panes = 'C2'
    ws.auto_filter.ref = ws.dimensions
    ws2 = wb.create_sheet('Versões')
    ws2.append(list(linhas.columns))
    for _, r in linhas.iterrows():
        ws2.append([None if isinstance(x, float) and np.isnan(x) else x for x in r.tolist()])
    for c in ws2[1]:
        c.font = Font(bold=True)
    wb.save(PASTAS / 'Catalogo_Mestre.xlsx')
    return ws.max_row - 1


def readme(linhas):
    m = ['# Análises exploratórias por versão', '',
         'Uma análise exploratória completa para cada versão possível do IVS e da base, cada uma com',
         'tabelas, figuras e um deck que explica cada item. Nenhuma versão é "a melhor": a referência',
         'continua sendo a proposta do NB05 até a orientadora decidir. Prompt:',
         '`docs/prompts/prompt_analises_exploratorias_versoes_2026-10.md`.', '',
         '- **Escolher o que vai para o artigo:** `Catalogo_Mestre.xlsx` (colunas Vai para o artigo? · Seção · Comentários).',
         '- **Comparação entre todas as versões:** `00_sintese/`.',
         '- **Parâmetros que ninguém fixou:** `PERGUNTAS.md`. **Versões que dependem de dado que não temos:** `X_bloqueadas.md`.',
         '- **Onde a execução parou e como regenerar:** `ESTADO.md` e o README de cada versão.', '',
         '| Versão | Eixo | Status | Setores no índice | Deck |', '|---|---|---|---:|---|']
    for _, r in linhas.iterrows():
        st = '—' if np.isnan(r['elegivel']) else ('elegível' if r['elegivel'] == 1 else '**não elegível**')
        n = '—' if np.isnan(r['setores_indice']) else intbr(r['setores_indice'])
        m.append(f"| `{r['versao']}` | {r['eixo'].split(' — ')[0]} | {st} | {n} | [{Path(r['deck']).name}]({r['deck']}) |")
    (PASTAS / 'README.md').write_text('\n'.join(m) + '\n', encoding='utf-8')


def main():
    linhas = pd.DataFrame([linha_da_versao(p) for p in pastas_de_versao() if not str(p).endswith('00_sintese')])
    SINTESE.mkdir(exist_ok=True)
    S = ev.Saida(SINTESE, json.loads(ev.MODELOS.read_text(encoding='utf-8')))
    sintese(S, linhas)
    S.fechar()
    readme(linhas)
    print(f'00_sintese: {len(S.linhas)} itens · {len(linhas)} versões no README')
    for r in S.linhas:
        print(f"  {r['id']}: {r['o_que_mostra'][:160]}")


if __name__ == '__main__':
    if '--catalogo' in sys.argv:
        linhas = pd.DataFrame([linha_da_versao(p) for p in pastas_de_versao() if not str(p).endswith('00_sintese')])
        print(f'Catalogo_Mestre.xlsx: {catalogo_mestre(linhas)} itens')
    else:
        main()
