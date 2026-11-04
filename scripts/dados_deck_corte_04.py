"""Números e figuras do deck do corte de carga < 0,4 por rotação (demanda da orientadora, nov/2026).

Segue a estrutura do deck final da multiversão (`Analise_Fatorial_e_IVS_2026-10.pptx`). As partes que
não dependem do corte (ponto de partida, exploratória dos 12, matrizes, quantos fatores e os apêndices de
correlação e cargas) são os mesmos slides daquele deck, lidos de `dados/FIN.json`: mesma base, mesmos 12
indicadores. O resto sai de `scripts/fatorial_corte_04.py` (`banco_de_dados/eda/fatorial_corte_04/`): o
corte, as versões, as duas propostas lado a lado (sem idosos e crianças; A com promax · 60/40, B com
Varimax · 60/40), os pesos, o IVS das duas, idosos e crianças, a sensibilidade e as decisões. Grava
`apresentacoes_multiversao/dados/C04.json` e as figuras `figuras/C04_*.png`, no formato de
`scripts/gerar_decks_multiversao.js`. Os números saem dos CSVs; as frases de interpretação são escritas à
mão e precisam ser conferidas com eles a cada nova rodada.

    ./.venv/bin/python scripts/dados_deck_corte_04.py
    node scripts/gerar_decks_multiversao.js C04
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'src', RAIZ / 'scripts'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import dados_apresentacoes_multiversao as dm  # noqa: E402
import fatorial_ampliada as fa  # noqa: E402
import fatorial_corte_04 as fc  # noqa: E402
import fatorial_multiversao as fm  # noqa: E402
import ivs_especificacoes as ie  # noqa: E402
from ivs_censo.fatorial import rodar_cenario  # noqa: E402

from dados_apresentacoes_multiversao import (CLAY, CINZA, FAIXAS, NOME, OCRE, PETROL, PORTES, REGIOES,  # noqa: E402
                                             SURF, TINTA, WHIS, barras, br, desc, estilo, explica, fmt, intbr,
                                             mapa_calor, pct, salvar)

ENT = 'banco_de_dados/eda/fatorial_corte_04/'
F_PASSOS, F_CARGAS, F_VERSOES, F_FINAIS = (f'{ENT}{n}.csv' for n in
                                           ('corte_passos', 'cargas_finais', 'versoes', 'finais_comparados'))
F_FINALISTAS, F_ESTAB, F_REPL, F_PERF, F_CORTE, F_IVS = (
    f'{ENT}{n}' for n in ('finalistas.csv', 'estabilidade.csv', 'replicacao.csv', 'perfil_perdidos.csv',
                          'corte_estabilidade.csv', 'ivs_final_por_setor.csv'))
F_SC, F_SR, F_SE = (f'{ENT}sensibilidade_{n}.csv' for n in ('corte', 'reamostragem', 'reentrada'))
F_ADEQ = 'banco_de_dados/eda/fatorial_multiversao/camada1_12_global_adequacao.csv'
ROTA = {'sem_rotacao': 'sem rotação', 'varimax': 'Varimax', 'promax': 'promax'}
METODO = {'unico': 'fator único', 'ss': 'soma dos quadrados', 'ss_padrao': 'soma dos quadrados (padrão)',
          'ss_estrutura': 'soma dos quadrados (estrutura)', 'comunalidades': 'comunalidades',
          '50_50': '50/50', '60_40': '60/40'}
FAM = {'12': 'os 12', '12_sem_idade': 'sem idosos e crianças', 'anterior_7': 'proposta anterior (os 7)'}
PAPEL = {'a': 'proposta A (promax)', 'b': 'proposta B (Varimax)', 'os_12': 'os 12 (regra literal)',
         'sem_rotacao': 'sem rotação', 'anterior_7': 'proposta anterior (os 7)'}
AB = ('a', 'b')
COR_AB = {'a': PETROL, 'b': OCRE}
PISO_MUN = 100       # municípios com ao menos 100 setores nas tabelas por município
# os slides do deck da multiversão que valem tal como estão (mesma base, mesmos 12 indicadores)
DO_FIN = {'partida': ['FIN-04', 'FIN-05'], 'exploratoria': ['FIN-07', 'FIN-08', 'FIN-09', 'FIN-10', 'FIN-11', 'FIN-12'],
          'matrizes': ['FIN-13'] + [f'FIN-{i}' for i in range(14, 21)], 'fatores': ['FIN-21', 'FIN-22', 'FIN-23'],
          'apendice': ['FIN-77', 'FIN-78', 'FIN-79']}


class Deck(dm.Deck):
    def gravar(self) -> None:
        dm.DADOS.mkdir(parents=True, exist_ok=True)
        (dm.DADOS / f'{self.cod}.json').write_text(json.dumps(
            {'deck': self.cod, 'titulo': self.titulo, 'arquivo': 'Corte_Carga_04_Duas_Propostas_2026-11_v2.pptx',
             'ordem': self.ordem, 'slides': self.slides}, ensure_ascii=False, indent=1), encoding='utf-8')

    def do_fin(self, ids: list[str]) -> None:
        """Copia slides do deck da multiversão; as divisórias renumeram na sequência deste deck."""
        fin = json.loads((dm.DADOS / 'FIN.json').read_text(encoding='utf-8'))['slides']
        for i in ids:
            x = dict(fin[i])
            if 'numero' in x:
                self.secao(x['titulo'], x['sub'])
            else:
                self.add(x.pop('titulo'), x.pop('fontes'), **x)


def nome_versao(r) -> str:
    return f"{ROTA[r['rotacao']]} · {METODO[r['metodo']]}"


def junta(itens: list[str]) -> str:
    itens = list(itens)
    return ' e '.join([', '.join(itens[:-1]), itens[-1]]) if len(itens) > 1 else (itens[0] if itens else 'nenhum')


def nomes(codigos) -> list[str]:
    return [NOME[c].split(' (')[0].lower() for c in fc.FAMILIAS['12'] if c in codigos]


def sem_acento(s: str) -> str:
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()


def troca_mun(v: pd.DataFrame, a: str, b: str) -> pd.DataFrame:
    """% de setores que mudam de faixa entre dois IVS em cada município, com as faixas refeitas nos setores
    que os dois têm (como `ie.comparar`, mas por município)."""
    t = v[v[a].notna() & v[b].notna()]
    m = t['NM_MUN'].to_numpy()
    muda = ie.faixas(t[a].to_numpy(), m, 'ivs_bh') != ie.faixas(t[b].to_numpy(), m, 'ivs_bh')
    return pd.DataFrame({'mun': m, 'muda': muda}).groupby('mun')['muda'].agg(['size', 'mean'])


# ───────────────────────────────────────────────────────────── figuras
def fig_trajetoria(p: pd.DataFrame) -> str:
    """Carga máxima de cada indicador no 1º passo e no último, por rotação (família dos 12)."""
    p = p[p['familia'] == '12']
    fig, axs = plt.subplots(1, 3, figsize=(10, 7.2), sharey=True)
    ordem = list(fc.FAMILIAS['12'])[::-1]
    for ax, rot in zip(axs, fc.ROTACOES):
        g = p[p['rotacao'] == rot]
        ini = g[g['passo'] == 1].set_index('codigo')['carga_max']
        fim = g[g['passo'] == g['passo'].max()].set_index('codigo')['carga_max']
        sai = g[g['retirado']].set_index('codigo')
        for y, c in enumerate(ordem):
            ax.plot(ini[c], y, 'o', mfc='white', mec=CINZA, ms=6)
            if c in fim.index:
                ax.plot([ini[c], fim[c]], [y, y], color=CINZA, lw=0.8)
                ax.plot(fim[c], y, 'o', color=PETROL, ms=6)
            else:
                ax.plot(sai.at[c, 'carga_max'], y, 'X', color=CLAY, ms=8)
                ax.text(0.5, y + 0.3, f"sai no passo {int(sai.at[c, 'passo'])}", ha='left', fontsize=9, color=CLAY)
        ax.axvline(fc.CORTE, color=CLAY, ls='--', lw=1)
        ax.set_xlim(0, 1.05)
        ax.set_title(ROTA[rot], fontsize=12, loc='left')
        estilo(ax, 'carga máxima (valor absoluto)')
        ax.tick_params(labelsize=10)
    axs[0].set_yticks(range(len(ordem)), [NOME[c] for c in ordem])
    fig.tight_layout()
    return salvar(fig, 'C04_trajetoria.png')


def fig_troca(v: pd.DataFrame) -> str:
    """Troca de faixa de cada versão contra a promax · 60/40 da família."""
    fig, axs = plt.subplots(2, 1, figsize=(8.5, 7.6), sharex=True)
    for ax, fam in zip(axs, ('12_sem_idade', '12')):
        g = v[(v['familia'] == fam) & ~((v['rotacao'] == fc.FINAL[0]) & (v['metodo'] == fc.FINAL[1]))]
        g = g.sort_values('troca_faixa_vs_final')
        cor = [CLAY if x >= 0.10 else PETROL for x in g['troca_faixa_vs_final']]
        ax.barh([nome_versao(r) for _, r in g.iterrows()], 100 * g['troca_faixa_vs_final'], color=cor)
        ax.axvline(10, color=CINZA, ls='--', lw=0.8)
        ax.set_title(FAM[fam] + (' (contra a proposta A)' if fam == '12_sem_idade' else ' (contra os 12 · promax · 60/40)'),
                     fontsize=12, loc='left')
        estilo(ax, '% dos setores que mudam de faixa' if fam == '12' else '')
        ax.tick_params(labelsize=10)
    fig.tight_layout()
    return salvar(fig, 'C04_troca_faixa.png')


def fig_pesos(v: pd.DataFrame) -> str:
    """Peso de cada indicador nas três versões promax · 60/40 (negativo: entra invertido)."""
    ids = [f'{f}·{fc.FINAL[0]}·{fc.FINAL[1]}' for f in ('12', '12_sem_idade', 'anterior_7')]
    rot = {'12': 'os 12', '12_sem_idade': 'proposta A (sem idosos e crianças)', 'anterior_7': 'proposta anterior (os 7)'}
    t = v.set_index('id').loc[ids]
    cods = [c for c in fc.FAMILIAS['12'] if f'peso_{c}' in t and t[f'peso_{c}'].notna().any()][::-1]
    fig, ax = plt.subplots(figsize=(8.5, 6.4))
    y = np.arange(len(cods))
    for k, (i, cor) in enumerate(zip(ids, (CINZA, PETROL, OCRE))):
        ax.barh(y + (k - 1) * 0.27, [100 * t.at[i, f'peso_{c}'] if pd.notna(t.at[i, f'peso_{c}']) else 0
                                      for c in cods], 0.27, color=cor, label=rot[i.split('·')[0]])
    ax.axvline(0, color='#1A1A1A', lw=0.6)
    ax.set_yticks(y, [NOME[c] for c in cods])
    ax.tick_params(labelsize=10)
    ax.legend(fontsize=10, frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
    estilo(ax, 'peso no índice (%)')
    return salvar(fig, 'C04_pesos.png')


def fig_mapas(M: dict, nm: dict) -> str:
    """As cargas das duas propostas em mapa de calor, lado a lado."""
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.8), facecolor=SURF)
    for ax, x, tit in zip(axs, AB, ('A · promax (matriz padrão)', 'B · Varimax')):
        P = M[x]
        ax.imshow(P, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
        ax.set_yticks(range(len(nm[x])), nm[x], fontsize=9)
        ax.set_xticks([0, 1], ['F1', 'F2'])
        ax.set_title(tit, fontsize=11, loc='left')
        for i in range(P.shape[0]):
            for j in range(2):
                ax.text(j, i, br(P[i, j], 2), ha='center', va='center', fontsize=9,
                        color='white' if abs(P[i, j]) > .55 else TINTA)
    fig.tight_layout()
    return salvar(fig, 'C04_cargas_mapa.png')


def fig_planos(M: dict, nm: dict) -> str:
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.8), facecolor=SURF, sharex=True, sharey=True)
    for ax, x, tit in zip(axs, AB, ('A · promax (matriz padrão)', 'B · Varimax')):
        P = M[x]
        ax.axhline(0, color=CINZA, lw=.6)
        ax.axvline(0, color=CINZA, lw=.6)
        ax.scatter(P[:, 0], P[:, 1], color=COR_AB[x])
        for i, n_ in enumerate(nm[x]):
            perto = any(abs(P[i, 1] - P[j, 1]) < 0.08 and abs(P[i, 0] - P[j, 0]) < 0.25 for j in range(i))
            ax.annotate(n_, (P[i, 0], P[i, 1]), fontsize=8, xytext=(4, -11 if perto else 4), textcoords='offset points')
        ax.set_xlim(-0.3, 1.7)    # espaço para os rótulos à direita dos pontos
        ax.set_title(tit, fontsize=11, loc='left')
        estilo(ax, 'carga em F1 (socioeconômica)', 'carga em F2 (saneamento)' if x == 'a' else '')
    fig.tight_layout()
    return salvar(fig, 'C04_plano_fatorial.png')


def fig_barras_ab(rotulos, va, vb, nome: str, xl: str) -> str:
    fig, ax = plt.subplots(figsize=(7.4, 4.6), facecolor=SURF)
    y = np.arange(len(rotulos))
    ax.barh(y - 0.2, va, 0.4, color=COR_AB['a'], label=PAPEL['a'])
    ax.barh(y + 0.2, vb, 0.4, color=COR_AB['b'], label=PAPEL['b'])
    ax.set_yticks(y, rotulos, fontsize=9)
    ax.invert_yaxis()
    ax.legend(fontsize=9, frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=2)
    estilo(ax, xl)
    fig.tight_layout()
    return salvar(fig, nome)


def fig_colunas_ab(rotulos, va, vb, nome: str, yl: str) -> str:
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    x = np.arange(len(rotulos))
    ax.bar(x - 0.2, va, 0.4, color=COR_AB['a'], label=PAPEL['a'])
    ax.bar(x + 0.2, vb, 0.4, color=COR_AB['b'], label=PAPEL['b'])
    ax.set_xticks(x, rotulos)
    ax.legend(fontsize=9, frameon=False)
    estilo(ax, 'faixa do IVS', yl)
    return salvar(fig, nome)


# ───────────────────────────────────────────────────────────── slides
def main() -> None:
    p = pd.read_csv(RAIZ / F_PASSOS)
    c = pd.read_csv(RAIZ / F_CARGAS)
    v = pd.read_csv(RAIZ / F_VERSOES)
    f = pd.read_csv(RAIZ / F_FINAIS)
    fin_ = pd.read_csv(RAIZ / F_FINALISTAS)
    est = pd.read_csv(RAIZ / F_ESTAB)
    rep = pd.read_csv(RAIZ / F_REPL).set_index('id')
    perf = pd.read_csv(RAIZ / F_PERF)
    corte = pd.read_csv(RAIZ / F_CORTE)
    ivs = pd.read_csv(RAIZ / F_IVS, dtype={'CD_SETOR': str})
    adeq = pd.read_csv(RAIZ / F_ADEQ).iloc[0]
    sc, sr, se = pd.read_csv(RAIZ / F_SC), pd.read_csv(RAIZ / F_SR).set_index('rotacao'), pd.read_csv(RAIZ / F_SE)
    df = fm.carregar()
    df['porte'] = pd.cut(df['pop_municipio'], [0, 100_000, 500_000, np.inf], labels=PORTES, right=True)
    prop = fin_.set_index('papel')
    cods = {x: prop.at[x, 'codigos'].split('+') for x in AB}
    D = Deck('C04', 'O corte de carga fatorial < 0,4 e as duas propostas de IVS')
    fin = {fam: v[v['id'] == f'{fam}·{fc.FINAL[0]}·{fc.FINAL[1]}'].iloc[0] for fam in ('12', '12_sem_idade', 'anterior_7')}
    ultimo = p.groupby(['familia', 'rotacao'])['passo'].transform('max') == p['passo']
    saem = {k: set(g['codigo']) for k, g in p[p['retirado']].groupby(['familia', 'rotacao'])}
    sempre = set.intersection(*saem.values())
    depende = {x: [ROTA[r] for (fm_, r), ss in saem.items() if fm_ == '12' and x not in ss]
               for x in set.union(*saem.values()) - sempre}
    frase_depende = '; '.join(f'{NOME[x].split(" (")[0].lower()} fica só com {junta(rr)}' for x, rr in depende.items())
    n_ab = {x: int(prop.at[x, 'n']) for x in AB}
    perda = n_ab['b'] - n_ab['a']
    ido12 = p[ultimo & (p['familia'] == '12') & (p['rotacao'] == 'promax')].set_index('codigo')['carga_max']

    D.add('O corte de carga fatorial < 0,4 e as duas propostas de IVS', ['docs/prompts/ (demanda de nov/2026)'], capa=True,
          kicker='ÍNDICE DE VULNERABILIDADE À SAÚDE · CENSO 2022 · 70 MUNICÍPIOS DO ELSI-BRASIL',
          sub='Os 12 indicadores na mesma análise fatorial; os de carga menor que 0,4 saem. O corte em cada rotação, '
              'as versões comparadas e duas propostas de IVS lado a lado — para a orientadora escolher.',
          rodape='Pedro Dias Soares · Fiocruz Minas — IRR · nov/2026')
    sumario = D.add('Como esta apresentação está organizada', ['scripts/fatorial_corte_04.py'],
                    cab=['Seção', 'Título', 'Slide'], colW=[0.8, 4.6, 0.9], linhas=[])

    # ── 1. ponto de partida
    D.secao('Ponto de partida', 'A demanda da orientadora, a base e os 12 indicadores.')
    D.add('A demanda e como ela foi atendida', ['scripts/fatorial_corte_04.py'], blocos=[
        ['A demanda.', '"Acionar todos os indicadores que já selecionamos na carga fatorial. Os indicadores com '
                       'carga fatorial menor que 0,4, retirar."'],
        ['Os indicadores.', f'Os {len(fc.FAMILIAS["12"])} do relatório parcial entram juntos na mesma fatorial.'],
        ['A fatorial.', 'Extração por eixo principal, 2 fatores, correlação de Spearman entre os setores dos 70 '
                        'municípios; analfabetismo sob sigilo fica ausente.'],
        ['O corte.', f'Sai um indicador por vez, o de menor carga, e a fatorial é refeita sem ele, até todos ficarem '
                     f'com carga de pelo menos {br(fc.CORTE, 1)}. Retirar um indicador muda a carga dos outros: por '
                     'isso o corte não é feito de uma vez.'],
        ['As versões.', 'O corte é repetido em cada rotação (sem rotação, Varimax, promax), porque a carga depende '
                        'dela. Depois, cada rotação calcula o índice com os seus métodos de peso.'],
        ['Duas famílias.', 'Os 12 completos, como a regra pede, e os 12 sem idosos e crianças. Idosos e crianças '
                           'passam no corte; tirá-los é decisão do projeto, não da regra: o projeto os lê como estrutura '
                           'etária, não como vulnerabilidade.'],
        ['Duas propostas.', 'Ambas sem idosos e crianças e com pesos 60/40 (o IVS de 2012): A com promax, em que o sem '
                            'banheiro passa no corte, e B com Varimax, em que ele sai. A escolha é da orientadora.']])
    resumo = D.add('A decisão em uma página', [F_FINALISTAS, F_CORTE, F_SR, F_PASSOS],
                   cab=['Medida', 'Proposta A (promax)', 'Proposta B (Varimax)'], colW=[2.9, 2.1, 2.1], linhas=[])
    termos = D.add('Os termos desta apresentação', ['scripts/fatorial_corte_04.py'], blocos=[
        ['Carga.', 'O quanto um indicador acompanha um fator. Na Varimax é a correlação; na promax, o efeito próprio do '
                   'fator, que pode passar de 1.'],
        ['Comunalidade (h²).', 'A parte da variação do indicador que os fatores explicam.'],
        ['Regra literal.', 'Os 12 indicadores só com a regra do 0,4, sem tirar idosos e crianças.'],
        ['Núcleo ou proposta anterior.', 'Os 7 indicadores do Quadro 1, com lixo e sem corte. Não são os 7 da proposta B, '
                                         'que tem sem água canalizada no lugar do lixo.'],
        ['Finalistas.', 'As propostas A e B e as três alternativas comparadas a elas: a regra literal, sem rotação e a '
                        'proposta anterior.'],
        ['Troca de faixa.', 'A % de setores que mudam de faixa entre dois índices. Até 10% é tratado como equivalente.'],
        ['Normalização de Kaiser.', 'Ajuste que dá o mesmo peso a todos os indicadores na rotação. SPSS e R usam; '
                                    'aqui ela não foi usada, e o slide "O corte muda com as escolhas de método" mostra o efeito.']])
    D.do_fin(DO_FIN['partida'])
    D.do_fin(DO_FIN['exploratoria'])
    D.do_fin(DO_FIN['matrizes'])
    D.do_fin(DO_FIN['fatores'])

    # ── o corte
    D.secao('O corte', 'Quem sai em cada rotação, em que ordem e com que carga.')
    g1 = p[(p['familia'] == '12') & (p['passo'] == 1)].pivot(index='codigo', columns='rotacao', values='carga_max')
    linhas = [[NOME[k]] + [br(g1.at[k, r], 2) + (' ✗' if g1.at[k, r] < fc.CORTE else '') for r in fc.ROTACOES]
              for k in fc.FAMILIAS['12']]
    abaixo = [NOME[k].lower() for k in fc.FAMILIAS['12'] if (g1.loc[k] < fc.CORTE).any()]
    D.add('Os 12 indicadores antes do corte', [F_PASSOS], cab=['Indicador'] + [ROTA[r] for r in fc.ROTACOES],
          colW=[2.9, 1.4, 1.4, 1.4], linhas=linhas, explica=explica(
              'A carga máxima de cada indicador na fatorial com os 12 juntos, no primeiro passo, em cada rotação.',
              'Mostra quem começa abaixo do corte. ✗ marca carga menor que 0,4 (com duas casas, 0,40 pode ser 0,3995 '
              'ou 0,4004).',
              'Sem rotação conta só o 1º fator, porque é o único que entra no índice; na Varimax, a carga é a '
              'correlação do indicador com o fator; na promax, a matriz padrão (o efeito próprio do fator, como um '
              'coeficiente de regressão).',
              f'Começam abaixo de 0,4 em ao menos uma rotação: {", ".join(abaixo)}.'))
    D.add('O corte passo a passo', [F_PASSOS], figura=fig_trajetoria(p),
          legenda='Carga máxima no primeiro passo (círculo vazio) e no último (cheio); ✗: quando o indicador saiu. Os 12.',
          explica=explica(
              'A trajetória do corte nos 12, em cada rotação.',
              'Mostra que a carga muda quando outro indicador sai: o corte precisa ser refeito a cada passo.',
              'Linha tracejada: o corte de 0,4. Um ✗ à esquerda dela é um indicador retirado; o rótulo diz em que passo.',
              f'Saem nas três rotações: {junta(nomes(sempre))}. Depende da rotação: {frase_depende or "nenhum"}.'))
    rem = p[p['retirado']]
    linhas = []
    for fam in ('12', '12_sem_idade'):
        for rot in fc.ROTACOES:
            r = rem[(rem['familia'] == fam) & (rem['rotacao'] == rot)].sort_values('passo')
            vv = v[(v['familia'] == fam) & (v['rotacao'] == rot)].iloc[0]
            linhas.append([FAM[fam], ROTA[rot], ' → '.join(f"{NOME[x].split(' (')[0]} ({br(y, 2)})"
                                                         for x, y in zip(r['codigo'], r['carga_max'])),
                           str(int(vv['p'])), intbr(vv['n'])])
    D.add('O que sai em cada rotação', [F_PASSOS, F_VERSOES], cab=['Família', 'Rotação', 'Saem, na ordem (carga ao sair)',
                                                               'Ficam', 'Setores'],
          colW=[1.6, 1.1, 3.2, 0.75, 0.9], linhas=linhas, explica=explica(
              'A lista dos retirados em cada rotação e nas duas famílias, com a carga que cada um tinha ao sair.',
              'É a resposta direta à demanda: quem a regra do 0,4 tira.',
              '"Setores": os que têm todos os indicadores que ficaram, a base daquela versão. Na família sem idosos e '
              'crianças, eles saíram antes, por decisão do projeto.',
              f'Saem em todas as {len(saem)}: {junta(nomes(sempre))}. Depende da rotação: {frase_depende or "nenhum"}.'))
    ban = p[ultimo & (p['codigo'] == 'BAN')].set_index(['familia', 'rotacao'])
    ban_sai = rem[rem['codigo'] == 'BAN'].set_index(['familia', 'rotacao'])
    linhas = []
    for fam in ('12', '12_sem_idade'):
        for rot in fc.ROTACOES:
            x = ban.loc[(fam, rot)] if (fam, rot) in ban.index else ban_sai.loc[(fam, rot)]
            vv = v[(v['familia'] == fam) & (v['rotacao'] == rot)].iloc[0]
            linhas.append([FAM[fam], ROTA[rot], br(x['carga_max'], 3), br(x['h2'], 3),
                           'fica' if (fam, rot) in ban.index else 'sai', intbr(vv['n'])])
    D.add('O sem banheiro: o caso que depende da rotação', [F_PASSOS, F_VERSOES],
          cab=['Família', 'Rotação', 'Carga', 'Comunalidade', 'Corte', 'Setores'], colW=[1.8, 1.1, 0.9, 1.2, 0.8, 1.0],
          linhas=linhas, explica=explica(
              'A carga e a comunalidade do sem banheiro no passo em que ele saiu ou no último.',
              'É o único indicador cujo destino muda com a rotação — e é o que separa as propostas A e B.',
              'Comunalidade: quanto da variação do indicador os fatores explicam (sem rotação, só o F1). O projeto '
              'tinha fixado 0,30 como mínimo, além da carga de 0,40.',
              f'Nas duas rotações ele fica perto do corte: passa por pouco na promax e sai por pouco na Varimax. A '
              f'comunalidade fica abaixo de 0,30. Mantê-lo custa '
              f'{intbr(perda)} setores à proposta A, que não têm o dado do banheiro.'))
    linhas = []
    for x in AB:
        g = corte[corte['proposta'] == x]
        base = set(prop.at[x, 'codigos'].split('+'))
        difs = g[~g['igual_a_proposta']].groupby('mantidos')['fora'].apply(list)
        linhas.append([PAPEL[x], f"{int(g['igual_a_proposta'].sum())} de {len(g)}", 'mesma lista', '—'])
        for k, m in difs.items():
            ks = set(k.split('+'))
            mud = '; '.join(t for t in ('sai ' + junta(nomes(base - ks)) if base - ks else '',
                                        'entra ' + junta(nomes(ks - base)) if ks - base else '') if t)
            linhas.append([PAPEL[x], str(len(m)), mud, ', '.join(m[:6]) + ('…' if len(m) > 6 else '')])
    D.add('O corte se mantém sem cada município?', [F_CORTE],
          cab=['Proposta', 'Rodadas', 'O que muda na lista', 'Municípios retirados'], colW=[1.9, 0.9, 2.6, 1.8],
          linhas=linhas, explica=explica(
              f'O corte de cada proposta refeito {corte["fora"].nunique()} vezes, cada vez sem um dos municípios.',
              'Testa se a lista que sobra é dos dados ou de uma cidade: a regra do 0,4 é aplicada de novo em cada rodada.',
              'A primeira linha de cada proposta conta as rodadas que dão a mesma lista; as outras, as que mudam.',
              'Mesma lista em ' + ' e '.join(f"{int(corte.loc[corte['proposta'] == x, 'igual_a_proposta'].sum())} de "
                                              f"{int((corte['proposta'] == x).sum())} rodadas na {x.upper()}" for x in AB)
              + f"; as listas só mudam sem {junta(sorted(corte.loc[~corte['igual_a_proposta'], 'fora'].unique()))}, e nem todo "
                'indicador que sai nessas rodadas estava perto de 0,40.'))

    # ── as versões
    D.secao('As versões', 'Rotações e métodos de peso sobre a lista que sobrou, comparados à promax · 60/40 da família.')
    D.add('Como as versões foram comparadas', [F_VERSOES], blocos=[
        ['As versões.', 'Sem rotação há um método de peso (o fator único leva tudo). Com Varimax, três: soma dos '
                        'quadrados das cargas, 50/50 e 60/40. Com promax, cinco: soma dos quadrados da matriz padrão, '
                        'da estrutura, comunalidades, 50/50 e 60/40.'],
        ['A referência.', 'Cada versão contra a promax · 60/40 da sua família — na família sem idosos e crianças, '
                          'a proposta A. A proposta B é a linha "Varimax · 60/40" dessa família.'],
        ['A comparação.', 'Só nos setores que as duas versões têm: as faixas das duas são refeitas nesses setores. '
                          'O índice de cada versão continua o da sua amostra (a régua mín-máx não é refeita).'],
        ['Spearman.', 'Concordância da ordem dos setores dentro de cada município (mediana entre municípios); 1 é '
                      'a mesma ordem.'],
        ['Troca de faixa.', 'A % de setores que mudam de faixa (baixo, médio, elevado, muito elevado) pela regra do '
                            'IVS-BH. Até 10% é tratado como equivalente.']])
    cab = ['Versão', 'Ind.', 'Setores', 'KMO', 'h² mín.', 'Peso socioec.', 'Spearman', 'Troca']
    for fam in ('12_sem_idade', '12'):
        g = v[v['familia'] == fam]
        linhas = [[nome_versao(r) + (' (A)' if fam == '12_sem_idade' and (r['rotacao'], r['metodo']) == fc.FINAL else
                                     ' (B)' if fam == '12_sem_idade' and (r['rotacao'], r['metodo']) == ('varimax', '60_40')
                                     else ''),
                   str(int(r['p'])), intbr(r['n']), br(r['kmo'], 3), br(r['h2_min'], 2),
                   pct(r['peso_F1'] / 100), br(r['spearman_mun_vs_final'], 3), pct(r['troca_faixa_vs_final'])]
                  for _, r in g.iterrows()]
        alt = g[~((g['rotacao'] == fc.FINAL[0]) & (g['metodo'] == fc.FINAL[1]))]
        pior = alt.loc[alt['troca_faixa_vs_final'].idxmax()]
        refn = 'a proposta A' if fam == '12_sem_idade' else 'os 12 · promax · 60/40'
        D.add(f'As versões: {FAM[fam]}', [F_VERSOES], cab=cab, colW=[2.5, 0.45, 0.85, 0.65, 0.7, 0.95, 1.0, 0.75],
              linhas=linhas, explica=explica(
                  f'As {len(g)} versões da família "{FAM[fam]}" e a distância de cada uma a {refn}.',
                  'Mostra quanto a rotação e o método de peso mudam o índice depois do corte.',
                  'h² mín.: a menor comunalidade da versão. Peso socioec.: a fração do índice que vem do fator da renda. '
                  'Versões de rotações diferentes podem ter listas e setores diferentes.',
                  f'Spearman de {br(alt["spearman_mun_vs_final"].min(), 3)} a {br(alt["spearman_mun_vs_final"].max(), 3)}. '
                  f'A mais distante é {nome_versao(pior)}, com {pct(pior["troca_faixa_vs_final"])} dos setores '
                  'mudando de faixa.'))
    acima = v[(v['familia'] != 'anterior_7') & (v['troca_faixa_vs_final'] >= 0.10)]
    D.add('Troca de faixa de cada versão', [F_VERSOES], figura=fig_troca(v),
          legenda='% dos setores que mudam de faixa em relação à promax · 60/40 da família; vermelho: 10% ou mais.',
          explica=explica(
              'A troca de faixa de todas as versões, nas duas famílias, ordenada.',
              'Separa as escolhas que mudam o índice das que não mudam.',
              'Barra vermelha: a versão muda a faixa de 10% ou mais dos setores e não é equivalente.',
              f'{len(acima)} versões chegam a 10%: '
              f'{junta([f"{nome_versao(r)} ({FAM[r.familia]}, {pct(r.troca_faixa_vs_final)})" for _, r in acima.iterrows()])}. '
              'As demais ficam abaixo.'))
    g = v[v['familia'] != 'anterior_7'].drop_duplicates(['familia', 'rotacao'])
    linhas = [[FAM[r['familia']], ROTA[r['rotacao']], br(r['kmo'], 3), br(r['msa_min'], 2), br(r['h2_min'], 2),
               br(r['carga_min'], 2), 'sim' if r['elegivel'] else 'não', br(r['auc_fcu_mun'], 3)]
              for _, r in g.iterrows()]
    eleg = g[g['elegivel']]
    D.add('Os critérios que o projeto tinha fixado', [F_VERSOES],
          cab=['Família', 'Rotação', 'KMO', 'MSA mín.', 'h² mín.', 'Carga mín.', 'Elegível', 'AUC mun.'],
          colW=[1.9, 1.2, 0.7, 0.85, 0.8, 0.95, 0.9, 0.9], linhas=linhas, explica=explica(
              'Os critérios fixados antes da multiversão (KMO ≥ 0,70; MSA ≥ 0,50; comunalidade ≥ 0,30; carga ≥ 0,40), '
              'por família e rotação.',
              'A regra da orientadora cobre só a carga; aqui se vê se as versões passam também nos outros critérios.',
              'Uma linha por rotação: os critérios dependem da fatorial, não do método de peso. Sem rotação, a '
              'comunalidade é a carga ao quadrado no F1, então o corte de 0,40 deixa passar comunalidade de só 0,16. '
              'AUC mun.: separação entre setores de favela e os demais, dentro do município, só como descrição.',
              'Elegíveis em todos os critérios: ' + (', '.join(f'{FAM[r["familia"]]} com {ROTA[r["rotacao"]]}'
                                                             for _, r in eleg.iterrows()) or 'nenhuma') +
              f'. Nenhuma das duas propostas é elegível: {int((g.query("not elegivel")["h2_min"] < 0.30).sum())} '
              'versões ficam de fora pela comunalidade abaixo de 0,30.'))

    # ── as duas propostas
    D.secao('As duas propostas', 'Ambas sem idosos e crianças, pesos 60/40, régua municipal. A: promax, mantém o sem '
                                 'banheiro. B: Varimax, a regra tira o sem banheiro.')
    r_ = {x: rodar_cenario(df.dropna(subset=[fm.VARS[k] for k in cods[x]])[[fm.VARS[k] for k in cods[x]]].to_numpy(),
                           com_horn=True, extracao=fm.EXTRACAO) for x in AB}
    M = {'a': r_['a']['promax_padrao'], 'b': r_['b']['varimax']}
    h2 = {'a': r_['a']['comunalidade_obliqua'], 'b': r_['b']['comunalidade']}
    nm = {x: [NOME[k] for k in cods[x]] for x in AB}
    pior = {x: (cods[x][int(np.argmin(h2[x]))], float(np.min(h2[x]))) for x in AB}
    cmin = {x: (cods[x][int(np.argmin(np.abs(M[x]).max(axis=1)))], float(np.abs(M[x]).max(axis=1).min())) for x in AB}
    D.add('As duas propostas', [F_FINALISTAS], blocos=[
        ['Comum às duas.', f'Partem dos 12; {junta(nomes(sempre))} saem pela regra do 0,4; '
                           f'{NOME["IDO"]} e {NOME["CRI"]} ficam fora por decisão do projeto (passam no corte, com '
                           f'cargas {br(ido12["IDO"], 2)} e {br(ido12["CRI"], 2)} nos 12). Eixo principal, 2 fatores, '
                           'pesos 60/40, régua mín-máx dentro do município.'],
        ['Proposta A — promax.', f"{len(cods['a'])} indicadores, com o sem banheiro (carga {br(cmin['a'][1], 3) if cmin['a'][0] == 'BAN' else br(ban.loc[('12_sem_idade', 'promax'), 'carga_max'], 3)}). "
                                 f"{intbr(n_ab['a'])} setores ({pct(prop.at['a', 'pct_recorte'])} do recorte)."],
        ['Proposta B — Varimax.', f"{len(cods['b'])} indicadores; a regra tira o sem banheiro (carga "
                                  f"{br(ban_sai.loc[('12_sem_idade', 'varimax'), 'carga_max'], 3)}). {intbr(n_ab['b'])} setores "
                                  f"({pct(prop.at['b', 'pct_recorte'])} do recorte)."],
        ['O que nenhuma resolve.', f"Nenhuma passa na comunalidade de 0,30 fixada pelo projeto: na A, a menor é a do "
                                   f"{NOME[pior['a'][0]].lower()} ({br(pior['a'][1], 3)}); na B, a da "
                                   f"{NOME[pior['b'][0]].lower()} ({br(pior['b'][1], 3)}). A única versão que passa em "
                                   "todos os critérios é a dos 12 com Varimax, que inclui idosos e crianças."],
        ['A diferença.', f"A proposta A troca {intbr(perda)} setores de cobertura pela presença do sem banheiro; os setores sem o "
                         f"dado do banheiro são os mais pobres (slide \"Quem cada proposta deixa sem IVS\")."]])
    sit = {}
    for x, rot in (('a', 'promax'), ('b', 'varimax')):
        for k in fc.FAMILIAS['12']:
            if k in ('IDO', 'CRI'):
                sit[(x, k)] = 'fora por decisão'
            elif k in cods[x]:
                sit[(x, k)] = 'fica'
            else:
                sit[(x, k)] = f"sai pela regra ({br(rem[(rem['familia'] == '12_sem_idade') & (rem['rotacao'] == rot) & (rem['codigo'] == k)]['carga_max'].iloc[0], 2)})"
    D.add('O que a regra tirou e o que foi decisão', [F_PASSOS],
          cab=['Indicador', 'Proposta A (promax)', 'Proposta B (Varimax)'], colW=[2.9, 2.0, 2.0],
          linhas=[[NOME[k], sit[('a', k)], sit[('b', k)]] for k in fc.FAMILIAS['12']], explica=explica(
              'Os 12 indicadores em três grupos: os que ficam, os que a regra do 0,4 tirou (com a carga ao sair) e os '
              'que ficaram fora por decisão do projeto.',
              'Separa o que é da regra da orientadora do que é escolha nossa.',
              'Idosos e crianças passam no corte; saem porque descrevem a estrutura etária e dominariam o fator '
              'socioeconômico (seção "Idosos e crianças").',
              f'A regra tira {junta(nomes(sempre))} nas duas; o sem banheiro só na B.'))
    todos = [k for k in fc.FAMILIAS['12_sem_idade'] if k in cods['a'] or k in cods['b']]
    def cel(x, k, j):  # noqa: E306
        return br(M[x][cods[x].index(k), j], 3) if k in cods[x] else '—'
    def hh(x, k):  # noqa: E306
        return br(h2[x][cods[x].index(k)], 3) if k in cods[x] else '—'
    D.add('As cargas das duas propostas', [F_FINALISTAS],
          cab=['Indicador', 'A F1', 'A F2', 'A h²', 'B F1', 'B F2', 'B h²'], colW=[2.6, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
          linhas=[[NOME[k], cel('a', k, 0), cel('a', k, 1), hh('a', k), cel('b', k, 0), cel('b', k, 1), hh('b', k)]
                  for k in todos], explica=explica(
              'As cargas e a comunalidade (h²) de cada indicador: na A, a matriz padrão da promax; na B, a Varimax.',
              'As cargas definem a que dimensão cada indicador pertence e como o peso se reparte dentro dela.',
              'F1 é a dimensão em que a renda carrega mais (socioeconômica); F2, a outra (saneamento). Na Varimax a '
              'carga é a correlação com o fator; na padrão da promax, o efeito próprio do fator, que pode passar de 1. '
              'Carga perto de 1 ou acima pede cautela.',
              f"Na A, a renda tem carga {br(M['a'][cods['a'].index('REN'), 0], 3)} no F1; na B, "
              f"{br(M['b'][cods['b'].index('REN'), 0], 3)}."))
    D.add('Proposta A: matriz de estrutura e correlação entre fatores', [F_FINALISTAS],
          cab=['Indicador', 'Estrutura F1', 'Estrutura F2', 'MSA'], colW=[2.9, 1.3, 1.3, 1.0],
          linhas=[[nm['a'][i], br(r_['a']['promax_estrutura'][i, 0], 3), br(r_['a']['promax_estrutura'][i, 1], 3),
                   br(r_['a']['msa'][i], 3)] for i in range(len(cods['a']))], explica=explica(
              'Na promax os fatores podem se correlacionar; a estrutura é a correlação simples entre indicador e fator.',
              'Completa a matriz padrão: um indicador pode ter estrutura alta num fator só por causa da correlação '
              'entre os fatores (Φ).',
              'Φ (fi) perto de 1 seria um fator só; perto de 0, dois fatores independentes. Na Varimax (B), Φ é 0 '
              'por construção.',
              f"Φ = {br(r_['a']['phi'][0, 1], 3)}. A renda tem estrutura {br(r_['a']['promax_estrutura'][cods['a'].index('REN'), 0], 3)} "
              'no F1, abaixo de 1.'))
    D.add('As cargas em mapa de calor', [F_FINALISTAS], figura=fig_mapas(M, nm),
          legenda='Cargas da proposta A (matriz padrão da promax) e da proposta B (Varimax).', explica=explica(
              oque='As duas matrizes de cargas em cores.', serve='Mostra de relance a que fator cada indicador pertence.',
              ler='Vermelho forte numa coluna: o indicador pertence àquele fator. Células claras nas duas colunas: o '
                  'indicador não pertence bem a nenhum.'))
    D.add('O plano fatorial', [F_FINALISTAS], figura=fig_planos(M, nm),
          legenda='Cargas da proposta A (padrão da promax) e da proposta B (Varimax).', explica=explica(
              oque='Cada ponto é um indicador, posicionado pelas cargas nos dois fatores.',
              serve='Mostra os grupos que a fatorial encontrou: indicadores próximos medem a mesma coisa.',
              ler='À direita e perto do eixo horizontal: dimensão socioeconômica. No alto e perto do eixo vertical: '
                  'saneamento. Perto da origem: o indicador quase não se explica pelos fatores.'))
    linhas = [['Indicadores', str(len(cods['a'])), str(len(cods['b']))],
              ['Setores (% do recorte)', f"{intbr(n_ab['a'])} ({pct(prop.at['a', 'pct_recorte'])})",
               f"{intbr(n_ab['b'])} ({pct(prop.at['b', 'pct_recorte'])})"],
              ['KMO', br(r_['a']['kmo'], 3), br(r_['b']['kmo'], 3)],
              ['MSA mínimo', br(r_['a']['msa'].min(), 3), br(r_['b']['msa'].min(), 3)],
              ['Comunalidade mínima', f"{br(pior['a'][1], 3)} ({NOME[pior['a'][0]].split(' (')[0].lower()})",
               f"{br(pior['b'][1], 3)} ({NOME[pior['b'][0]].split(' (')[0].lower()})"],
              ['Carga mínima', f"{br(cmin['a'][1], 3)} ({NOME[cmin['a'][0]].split(' (')[0].lower()})",
               f"{br(cmin['b'][1], 3)} ({NOME[cmin['b'][0]].split(' (')[0].lower()})"],
              ['Elegível (4 critérios)', 'sim' if prop.at['a', 'elegivel'] else 'não', 'sim' if prop.at['b', 'elegivel'] else 'não'],
              ['Variância comum dos 2 fatores', dm.ev.pctbr(r_['a']['var_explicada_k']), dm.ev.pctbr(r_['b']['var_explicada_k'])],
              ['Fatores retidos (Horn · Kaiser)', f"{r_['a']['horn_retidos']} · {r_['a']['kaiser']}",
               f"{r_['b']['horn_retidos']} · {r_['b']['kaiser']}"],
              ['Φ entre os fatores', br(r_['a']['phi'][0, 1], 3), '0 (ortogonal)'],
              ['Tucker F1 · F2 (metades)', f"{br(rep.at['a', 'tucker_F1'], 3)} · {br(rep.at['a', 'tucker_F2'], 3)}",
               f"{br(rep.at['b', 'tucker_F1'], 3)} · {br(rep.at['b', 'tucker_F2'], 3)}"]]
    D.add('As duas propostas em números', [F_FINALISTAS, F_REPL], cab=['Medida', 'Proposta A (promax)', 'Proposta B (Varimax)'],
          colW=[2.8, 2.1, 2.1], linhas=linhas, explica=explica(
              'A adequação, a base e a replicação de cada proposta.',
              'Resume, numa tabela, o que muda entre A e B.',
              'Horn e Kaiser contam os fatores pedidos pelos dados de cada lista; o índice usa 2. Tucker: as cargas de '
              'duas metades sorteadas de municípios comparadas (0,95 ou mais: replicado).',
              f"A B cobre {intbr(perda)} setores a mais; as duas replicam (Tucker acima de 0,95 nos dois fatores)."
              if min(rep.at[x, k] for x in AB for k in ('tucker_F1', 'tucker_F2')) >= 0.95 else
              f"A B cobre {intbr(perda)} setores a mais."))

    # ── os pesos
    D.secao('Os pesos', 'Por dimensão e por indicador, a estabilidade por município e a replicação entre metades.')
    base_p = v[v['familia'] == '12_sem_idade']
    dos_dados = base_p[~base_p['metodo'].isin(['unico', '50_50', '60_40'])]
    D.add('O peso da dimensão socioeconômica em cada método', [F_VERSOES],
          cab=['Rotação', 'Método de peso', 'Peso socioeconômico'], colW=[2.0, 2.8, 2.0],
          linhas=[[ROTA[x.rotacao], METODO[x.metodo] + (' (A)' if (x.rotacao, x.metodo) == fc.FINAL else
                                                         ' (B)' if (x.rotacao, x.metodo) == ('varimax', '60_40') else ''),
                   pct(x.peso_F1 / 100)] for x in base_p.itertuples()], explica=explica(
              oque='Quanto do índice vem da dimensão socioeconômica em cada forma de calcular os pesos (família sem '
                   'idosos e crianças).',
              serve='O IVS de 2012 usa 60% socioeconômica e 40% saneamento. Aqui se vê quanto os dados dariam.',
              ler='"Soma dos quadrados" e "comunalidades" saem dos dados; 50/50 e 60/40 são fixos. Sem rotação há um '
                  'fator só. A composição das dimensões não é a de 2012: o lixo saiu e entraram sem água canalizada '
                  'e, na A, sem banheiro.',
              mostra='As duas propostas usam 60/40. Pelos dados, a dimensão socioeconômica levaria de '
                     f"{pct(dos_dados['peso_F1'].min() / 100)} a {pct(dos_dados['peso_F1'].max() / 100)}."))
    pesos = {x: pd.Series({k: prop.at[x, f'peso_{k}'] for k in cods[x]}) for x in AB}
    e = {x: est[est['id'] == x] for x in AB}
    def faixa_peso(x, k):  # noqa: E306
        if k not in cods[x]:
            return '—', '—'
        return pct(abs(pesos[x][k])), f"{pct(e[x][f'peso_{k}'].abs().min())} a {pct(e[x][f'peso_{k}'].abs().max())}"
    D.add('O peso de cada indicador nas duas propostas', [F_FINALISTAS, F_ESTAB],
          cab=['Indicador', 'A peso', 'A sem 1 mun.', 'B peso', 'B sem 1 mun.'], colW=[2.6, 0.9, 1.5, 0.9, 1.5],
          linhas=[[NOME[k], *faixa_peso('a', k), *faixa_peso('b', k)] for k in todos], explica=explica(
              oque='A fração do índice que vem de cada indicador, e o menor e o maior valor ao tirar um município.',
              serve='É o que define o índice: IVS = soma de cada indicador padronizado vezes o seu peso.',
              ler='Dentro de cada dimensão, o peso se reparte pelo quadrado das cargas: quem carrega mais pesa mais. '
                  'Variação pequena em pontos pode ser grande em proporção para indicadores de peso baixo.',
              mostra=f"O maior peso é o de {NOME[pesos['a'].abs().idxmax()]} nas duas: "
                     f"{pct(pesos['a'].abs().max())} na A e {pct(pesos['b'].abs().max())} na B."))
    D.add('O peso de cada indicador: o gráfico', [F_FINALISTAS],
          figura=fig_barras_ab([NOME[k] for k in todos], [100 * abs(pesos['a'].get(k, 0)) for k in todos],
                               [100 * abs(pesos['b'].get(k, 0)) for k in todos], 'C04_pesos_ab.png', 'peso no índice (%)'),
          legenda='Pesos nas duas propostas.', explica=explica(
              oque='Os mesmos pesos em barras, A e B lado a lado.', serve='Mostra quem domina cada índice.',
              ler='Barras longas: indicadores que mais determinam a posição de um setor no IVS.'))
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4), facecolor=SURF, sharey=True)
    for ax, x in zip(axs, AB):
        ax.boxplot([100 * e[x][f'peso_{k}'].abs() for k in cods[x]], tick_labels=nm[x], whis=WHIS,
                   medianprops={'color': CLAY})
        ax.tick_params(axis='x', labelrotation=40, labelsize=8)
        ax.set_title(PAPEL[x], fontsize=11, loc='left')
        estilo(ax, '', 'peso (%) sem 1 município' if x == 'a' else '')
    fig.tight_layout()
    D.add('A estabilidade: um município de fora por vez', [F_ESTAB], figura=salvar(fig, 'C04_estabilidade.png'),
          legenda=f"Peso de cada indicador nas {len(e['a'])} rodadas, cada uma sem um município.", explica=explica(
              oque=f"Os pesos recalculados {len(e['a'])} vezes, cada vez sem um dos municípios (a lista fica fixa).",
              serve='É a medida de incerteza adotada: os municípios são a unidade de replicação do ELSI.',
              ler='Caixa estreita: peso estável. Pontos isolados: um município que, sozinho, muda o peso. O peso '
                  'socioeconômico fica em 60% por construção.',
              mostra=dm.amplitude_texto(e['a'], cods['a']).replace('dentro das dimensões, o peso', 'Na A, o peso') + '; '
                     + dm.amplitude_texto(e['b'], cods['b']).replace('dentro das dimensões, o peso', 'na B, o') + '.'))
    D.add('A replicação entre metades dos municípios', [F_REPL],
          cab=['Finalista', 'Tucker F1', 'Tucker F2'], colW=[3.4, 1.4, 1.4],
          linhas=[[PAPEL[x.papel], br(rep.at[x.papel, 'tucker_F1'], 3), br(rep.at[x.papel, 'tucker_F2'], 3)]
                  for x in fin_.itertuples()], explica=explica(
              oque='Os municípios foram divididos em duas metades sorteadas dentro de cada região (as mesmas da '
                   'multiversão); a fatorial rodou em cada metade e as cargas foram comparadas pelo coeficiente de '
                   'Tucker, uma correlação entre as duas colunas de cargas.',
              serve='Testa se a estrutura é dos dados ou de um grupo de municípios.',
              ler='Tucker de 0,95 ou mais: fator replicado; de 0,85 a 0,94: parecido; abaixo: diferente. Sem rotação há '
                  'um fator só.',
              mostra=f"A: {br(rep.at['a', 'tucker_F1'], 3)} e {br(rep.at['a', 'tucker_F2'], 3)}; B: "
                     f"{br(rep.at['b', 'tucker_F1'], 3)} e {br(rep.at['b', 'tucker_F2'], 3)}."))

    # ── o IVS das duas propostas
    D.secao('O IVS das duas propostas', 'Faixas, quem mora em cada uma e quem fica sem IVS.')
    vv = ivs.merge(df[['CD_SETOR', 'porte']], on='CD_SETOR')
    q = {x: desc(vv[f'ivs_{x}']) for x in AB}
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), facecolor=SURF, sharex=True)
    for ax, x in zip(axs, AB):
        ax.hist(vv[f'ivs_{x}'].dropna(), bins=60, color=COR_AB[x])
        ax.set_title(PAPEL[x], fontsize=11, loc='left')
        estilo(ax, 'IVS (0 a 1, régua do município)', 'setores' if x == 'a' else '')
    fig.tight_layout()
    D.add('A distribuição do IVS', [F_IVS], figura=salvar(fig, 'C04_ivs_hist.png'),
          legenda='IVS por setor nas duas propostas.', explica=explica(
              oque='O histograma do IVS de cada proposta: cada setor recebe um valor de 0 a 1.',
              serve='0 = o setor menos vulnerável da sua cidade em todos os indicadores; 1 = o mais.',
              ler='Como a régua é de cada município, o valor diz onde o setor fica dentro da própria cidade.',
              mostra=f"A: {intbr(q['a']['n'])} setores (mediana {br(q['a']['mediana'], 3)}); B: {intbr(q['b']['n'])} "
                     f"(mediana {br(q['b']['mediana'], 3)})."))
    t = {}
    for x in AB:
        ok = vv[vv[f'faixa_{x}'] >= 0].astype({f'faixa_{x}': int})
        g = ok.groupby(f'faixa_{x}')
        t[x] = pd.DataFrame({'setores': g.size(), 'pop': g['v0001'].sum(), 'p60': g['pop_60mais'].sum(),
                             'idoso': g['pct_idoso_60mais'].mean(), 'fcu': g['is_fcu'].mean()})
    ler_fx = ('Regra do IVS-BH 2012, dentro de cada município: médio = média ± 0,5 desvio-padrão; elevado até +1,5; '
              'acima, muito elevado; abaixo de −0,5, baixo.')
    D.add('As quatro faixas: setores e moradores', [F_IVS],
          cab=['Faixa', 'A setores', 'A moradores', 'A %', 'B setores', 'B moradores', 'B %'],
          colW=[1.3, 0.95, 1.2, 0.7, 0.95, 1.2, 0.7],
          linhas=[[FAIXAS[i]] + [y for x in AB for y in (intbr(t[x].at[i, 'setores']), intbr(t[x].at[i, 'pop']),
                                                           pct(t[x].at[i, 'pop'] / t[x]['pop'].sum()))]
                  for i in t['a'].index], explica=explica(
              oque='Quantos setores e quantos moradores ficam em cada faixa, nas duas propostas.',
              serve='As faixas são o produto que vai para os mapas e para a gestão: onde priorizar.', ler=ler_fx,
              mostra=f"Moradores em setores de faixa elevada ou muito elevada: {intbr(t['a']['pop'].iloc[-2:].sum())} na A "
                     f"e {intbr(t['b']['pop'].iloc[-2:].sum())} na B."))
    D.add('As quatro faixas: o gráfico', [F_IVS],
          figura=fig_colunas_ab(FAIXAS, t['a']['pop'] / 1e6, t['b']['pop'] / 1e6, 'C04_faixas.png', 'moradores (milhões)'),
          legenda='Moradores por faixa nas duas propostas.', explica=explica(
              oque='Os moradores de cada faixa, em milhões.', serve='Dá a dimensão da população em cada nível.',
              ler=ler_fx + ' A B cobre mais setores, por isso tem mais moradores em todas as faixas.'))
    cab_ab = ie.comparar(vv['ivs_a'].to_numpy(), vv['ivs_b'].to_numpy(), vv['NM_MUN'].to_numpy())
    comuns = vv[vv['ivs_a'].notna() & vv['ivs_b'].notna()]
    sem_refazer = (comuns['faixa_a'] != comuns['faixa_b']).mean()
    linhas = [[f'{PAPEL[x]}: IVS-BH igual aos quartis', pct((vv.loc[vv[f'faixa_{x}'] >= 0, f'faixa_{x}'] == vv.loc[vv[f'faixa_{x}'] >= 0, f'quartis_{x}']).mean())]
              for x in AB] + [['A × B (setores comuns)', f"troca {pct(cab_ab['troca_faixa'])}; Spearman {br(cab_ab['spearman_mun'], 3)}"]]
    D.add('As faixas: duas regras e duas propostas', [F_IVS], cab=['Comparação', 'Resultado'], colW=[3.0, 3.6],
          linhas=linhas, explica=explica(
              oque='A concordância entre a regra do IVS-BH e os quartis (25% dos setores de cada município em cada faixa) '
                   'em cada proposta, e a troca de faixa entre A e B nos setores que as duas têm.',
              serve='Mostra o quanto a regra de faixa e a escolha entre A e B mudam a classificação.',
              ler='A regra do IVS-BH põe mais setores no "médio" que em outra faixa; os quartis forçam 25% em cada faixa — a discordância vem '
                  'em parte da construção das regras.',
              mostra=f"Entre A e B, {pct(cab_ab['troca_faixa'])} dos setores comuns mudam de faixa. Sem refazer as faixas nesses "
                     f"setores, são {pct(sem_refazer)}: a diferença vem dos setores a mais da B, que mudam a média do município."))
    fr_ido = '; '.join(f"{PAPEL[x]}: {intbr(t[x].p60.iloc[-2:].sum())} ({pct(t[x].p60.iloc[-2:].sum() / t[x].p60.sum())})"
                       for x in AB)
    D.add('Os idosos em cada faixa: a tabela', [F_IVS],
          cab=['Faixa', 'A pessoas 60+', 'A % idosos', 'B pessoas 60+', 'B % idosos'], colW=[1.4, 1.4, 1.2, 1.4, 1.2],
          linhas=[[FAIXAS[i]] + [y for x in AB for y in (intbr(t[x].at[i, 'p60']), pct(t[x].at[i, 'p60'] / t[x].p60.sum()))]
                  for i in t['a'].index], explica=explica(
              oque='Quantas pessoas de 60 anos ou mais moram em cada faixa, nas duas propostas.',
              serve='É a pergunta do ELSI-Brasil: onde moram os idosos em relação à vulnerabilidade do território. Com os '
                    'idosos fora do índice, a pergunta não é circular.',
              ler='"% idosos": distribuição dos idosos com IVS entre as faixas.',
              mostra='Idosos em setores de faixa elevada ou muito elevada — ' + fr_ido + '.'))
    D.add('Os idosos em cada faixa: o gráfico', [F_IVS],
          figura=fig_colunas_ab(FAIXAS, 100 * t['a']['idoso'], 100 * t['b']['idoso'], 'C04_idosos_faixa.png',
                                '% de idosos no setor (média)'),
          legenda='Proporção média de idosos nos setores de cada faixa.', explica=explica(
              oque='A proporção média de pessoas de 60 anos ou mais nos setores de cada faixa.',
              serve='Mostra se os setores mais vulneráveis são mais jovens ou mais envelhecidos.',
              ler='Barras que caem para a direita: os setores mais vulneráveis têm menos idosos proporcionalmente.'))
    D.add('As favelas em cada faixa', [F_IVS], cab=['Faixa', 'A setores', 'A % favela', 'B setores', 'B % favela'],
          colW=[1.5, 1.3, 1.3, 1.3, 1.3],
          linhas=[[FAIXAS[i]] + [y for x in AB for y in (intbr(t[x].at[i, 'setores']), pct(t[x].at[i, 'fcu']))]
                  for i in t['a'].index], explica=explica(
              oque='A proporção de setores de favela e comunidade urbana em cada faixa.',
              serve='Checagem de bom senso: favela deveria se concentrar nas faixas mais altas.',
              ler='Descrição, não validação: o critério de favela do IBGE já incorpora moradia.',
              mostra=f"Na faixa muito elevada: {pct(t['a'].fcu.iloc[-1])} de favela na A e {pct(t['b'].fcu.iloc[-1])} na B."))
    for por, rot_p, ordem in (('regiao', 'Por região', REGIOES), ('porte', 'Por porte do município', PORTES)):
        fig, axs = plt.subplots(2, 1, figsize=(7.6, 5.4), facecolor=SURF, sharex=True)
        mtx = {}
        for ax, x in zip(axs, AB):
            ok = vv[vv[f'faixa_{x}'] >= 0].astype({f'faixa_{x}': int})
            ct = pd.crosstab(ok[por], ok[f'faixa_{x}'], normalize='index').reindex(ordem)
            mtx[x] = ct[3]
            esq = np.zeros(len(ct))
            for j, cor_ in enumerate([CINZA, PETROL, OCRE, CLAY]):
                ax.barh(ordem, 100 * ct[j], left=esq, color=cor_, label=FAIXAS[j])
                esq += 100 * ct[j].to_numpy()
            ax.invert_yaxis()
            ax.set_title(PAPEL[x], fontsize=10, loc='left')
            estilo(ax, '% dos setores' if x == 'b' else '')
        axs[0].legend(fontsize=7, frameon=False, ncol=4, loc='lower right', bbox_to_anchor=(1.0, 1.02))
        fig.tight_layout()
        D.add(f'{rot_p}: a distribuição das faixas', [F_IVS], figura=salvar(fig, f'C04_faixas_{por}.png'),
              legenda=f'Distribuição das faixas {rot_p.lower()}, nas duas propostas.', explica=explica(
                  oque='A parte dos setores em cada faixa, para cada grupo.',
                  serve='Mostra se algum grupo concentra setores nas faixas altas.',
                  ler='Com a régua do município, a faixa diz onde o setor fica dentro da própria cidade: comparar grupos '
                      'descreve a forma das distribuições internas, não o nível de vulnerabilidade de cada um.',
                  mostra='% em faixa muito elevada (A / B): ' + '; '.join(f'{i} {pct(mtx["a"][i])} / {pct(mtx["b"][i])}'
                                                                         for i in ordem) + '.'))
    m = {}
    for x in AB:
        ok = vv[vv[f'faixa_{x}'] >= 0]
        m[x] = ok[ok[f'faixa_{x}'] >= 2].groupby('NM_MUN')['v0001'].sum()
    top = m['a'].sort_values(ascending=False).head(15)
    D.add('Os municípios com mais moradores em faixa elevada ou muito elevada', [F_IVS],
          cab=['Município', 'A moradores', 'B moradores'], colW=[2.8, 1.8, 1.8],
          linhas=[[i, intbr(y), intbr(m['b'].get(i, 0))] for i, y in top.items()], explica=explica(
              oque='Os 15 municípios com mais moradores em setores de faixa elevada ou muito elevada na proposta A, com '
                   'o mesmo número na B.',
              serve='Mostra onde está, em números absolutos, a população que o índice aponta como mais vulnerável.',
              ler='São contagens, não médias: a média de um índice padronizado por município não se compara entre '
                  'cidades. A diferença entre A e B vem sobretudo dos setores sem o dado do banheiro.'))
    so_a = vv[vv['ivs_b'].notna() & vv['ivs_a'].isna()]
    ambas = vv[vv['ivs_b'].isna() & vv['ivs_a'].isna()]
    com = vv[vv['ivs_a'].notna()]
    grupos = [('Sem IVS nas duas', ambas), ('Sem IVS só na A (falta o banheiro)', so_a), ('Com IVS nas duas', com)]
    nort = lambda g: pct(g['regiao'].isin(['Norte', 'Nordeste']).mean())  # noqa: E731
    D.add('Quem cada proposta deixa sem IVS', [F_IVS, F_PERF],
          cab=['Grupo', 'Setores', 'Moradores', 'Renda mediana', '% favela', '% N e NE'],
          colW=[2.6, 0.95, 1.2, 1.25, 0.85, 1.0],
          linhas=[[n_, intbr(len(g)), intbr(g['v0001'].sum()), fmt('REN', g['renda_media_sem_extremo'].median()),
                   pct(g['is_fcu'].mean()), nort(g)] for n_, g in grupos], explica=explica(
              oque='Os setores do recorte divididos pelo que acontece com eles: sem IVS nas duas propostas (falta o '
                   'analfabetismo, sob sigilo), sem IVS só na A (falta o dado do banheiro) e com IVS nas duas.',
              serve='Perder setores é decisão: se os perdidos são diferentes dos mantidos, o índice fica enviesado.',
              ler='Compare cada grupo com o dos setores com IVS. A média dos perdidos da A junta os dois primeiros grupos, '
                  'que são opostos, e esconde isso.',
              mostra=f"Os {intbr(len(so_a))} setores que só a A perde têm renda mediana de "
                     f"{fmt('REN', so_a['renda_media_sem_extremo'].median())} e {pct(so_a['is_fcu'].mean())} de favela: "
                     'são mais pobres que os que ficam. Os que as duas perdem são mais ricos.'))
    g = vv.groupby('NM_MUN')
    cob = pd.DataFrame({'n': g.size(), 'a': g['ivs_a'].apply(lambda s: s.notna().mean()),
                        'b': g['ivs_b'].apply(lambda s: s.notna().mean())})
    cob = cob[cob['n'] >= PISO_MUN].sort_values('a').head(12)
    D.add('A cobertura do IVS por município', [F_IVS], cab=['Município', 'Setores', 'Cobertura A', 'Cobertura B'],
          colW=[2.8, 1.2, 1.4, 1.4],
          linhas=[[i, intbr(x.n), pct(x.a), pct(x.b)] for i, x in cob.iterrows()], explica=explica(
              oque=f'A % de setores de cada município que recebem IVS, nos 12 municípios (com {PISO_MUN} setores ou mais) '
                   'de menor cobertura na A.',
              serve='Mostra onde a falta do dado do banheiro mais pesa.',
              ler='Cobertura baixa: muitos setores do município ficam fora dos mapas e das faixas.',
              mostra=f"Menor cobertura na A: {cob.index[0]} ({pct(cob['a'].iloc[0])}, contra {pct(cob['b'].iloc[0])} na B)."))
    tm = troca_mun(vv, 'ivs_a', 'ivs_b')
    tm = tm[tm['size'] >= PISO_MUN].sort_values('mean', ascending=False)
    D.add('A troca de faixa entre A e B por município', [F_IVS], cab=['Município', 'Setores comuns', 'Troca A × B'],
          colW=[2.8, 1.6, 1.6], linhas=[[i, intbr(x['size']), pct(x['mean'])] for i, x in tm.head(12).iterrows()],
          explica=explica(
              oque=f'A % de setores que mudam de faixa entre A e B em cada município (com {PISO_MUN} setores comuns ou '
                   'mais), com as faixas refeitas nos setores comuns; os 12 maiores.',
              serve='Mostra se a escolha entre A e B pesa mais em algumas cidades.',
              ler='Até 10% é tratado como equivalente.',
              mostra=f"Mediana entre os municípios: {pct(tm['mean'].median())}; "
                     f"{int((tm['mean'] >= 0.10).sum())} de {len(tm)} chegam a 10% sem arredondar."))
    D.add('As finalistas lado a lado', [F_FINALISTAS],
          cab=['Finalista', 'Ind.', 'Método', 'Setores', 'Troca vs A', 'Troca vs B'], colW=[2.3, 0.5, 1.7, 1.0, 1.0, 1.0],
          linhas=[[PAPEL[x.papel], str(len(x.codigos.split('+'))), f'{ROTA[x.rotacao]} · {METODO[x.metodo]}', intbr(x.n),
                   '—' if x.papel == 'a' else pct(x.troca_faixa_vs_a), '—' if x.papel == 'b' else pct(x.troca_faixa_vs_b)]
                  for x in fin_.itertuples()],
          explica=explica(
              oque='As duas propostas e as alternativas: a regra literal (com idosos e crianças), sem rotação e a '
                   'proposta anterior.',
              serve='São as especificações para decidir, com o custo de cada uma.',
              ler='"Troca": % de setores que mudam de faixa, nos setores comuns. Até 10%: equivalente.'))

    # ── idosos e crianças
    D.secao('Idosos e crianças', 'Passam no corte, mas mudam o que o índice mede.')
    pi = 100 * (abs(fin['12']['peso_IDO']) + fin['12']['peso_CRI'])
    D.add('O peso de cada indicador com e sem idosos e crianças', [F_VERSOES], figura=fig_pesos(v),
          legenda='Peso no índice de cada indicador, promax · 60/40; barra à esquerda do zero: entra invertido.',
          explica=explica(
              'O peso de cada indicador nos 12 (regra literal), na proposta A e na proposta anterior.',
              'Mostra o que pesa no índice quando idosos e crianças ficam.',
              'O peso é a fração do índice que vem do indicador. Peso negativo: o indicador entra invertido.',
              f'Nos 12, idosos e crianças somam {br(pi, 1)}% do índice (em módulo) e a renda fica com '
              f'{br(100 * fin["12"]["peso_REN"], 1)}%. Os idosos entram invertidos: menos idosos conta como mais '
              'vulnerabilidade.'))
    g = c[(c['familia'] == '12') & (c['rotacao'] == 'promax')]
    linhas = [[NOME[x['codigo']], br(x['F1'], 3), br(x['F2'], 3), br(x['estrutura_F1'], 3), br(x['estrutura_F2'], 3),
               br(x['h2'], 3)] for _, x in g.iterrows()]
    cri, ren = g.set_index('codigo').loc['CRI'], g.set_index('codigo').loc['REN']
    cri1 = p[(p['familia'] == '12') & (p['rotacao'] == 'promax') & (p['passo'] == 1) & (p['codigo'] == 'CRI')]['carga_max'].iloc[0]
    D.add('As cargas dos 12 com promax (regra literal)', [F_CARGAS],
          cab=['Indicador', 'Padrão F1', 'Padrão F2', 'Estrutura F1', 'Estrutura F2', 'Comunalidade'],
          colW=[2.4, 0.9, 0.9, 1.05, 1.05, 1.3], linhas=linhas, explica=explica(
              'As cargas dos indicadores que ficam nos 12 com promax: a matriz padrão (que define o corte e os pesos) '
              'e a de estrutura.',
              'Mostra quem forma cada fator quando idosos e crianças entram.',
              'F1 é o fator da renda (socioeconômico); F2, o do saneamento. Carga perto de 1 ou acima pede cautela '
              '(pode indicar solução imprópria) — vale para as crianças aqui e para a renda na proposta A. Estas são as '
              f'cargas depois do corte; no 1º passo, as crianças têm {br(cri1, 3)}.',
              f'Crianças têm a maior carga do F1 ({br(cri["F1"], 3)}), acima da renda ({br(ren["F1"], 3)}): com os 12, '
              'o F1 passa a misturar a estrutura etária com a renda.'))
    rotulo = {'12': 'Os 12', '12_sem_idade': 'Proposta A (sem idosos e crianças)', 'anterior_7': 'Proposta anterior (os 7)'}
    linhas = [[rotulo[x['a']], rotulo[x['b']], intbr(x['n_comum']), br(x['spearman_mun'], 3), pct(x['troca_faixa'])]
              for _, x in f.iterrows()]
    par = f.set_index(['a', 'b'])
    t_ant = par.at[('12_sem_idade', 'anterior_7'), 'troca_faixa']
    D.add('Com e sem idosos e crianças, e a proposta anterior', [F_FINAIS], cab=['Versão', 'Contra', 'Setores', 'Spearman', 'Troca'],
          colW=[2.6, 2.4, 0.9, 0.9, 0.8], linhas=linhas, explica=explica(
              'Os 12, a proposta A e a proposta anterior, duas a duas, nos setores comuns (todas promax · 60/40).',
              'Mede o efeito de idosos e crianças e o efeito do corte sobre o IVS que já existia.',
              'Mesmas medidas das versões: Spearman dentro do município e troca de faixa; até 10% é equivalente.',
              f'Tirar idosos e crianças muda a faixa de {pct(par.at[("12", "12_sem_idade"), "troca_faixa"])} dos '
              f'setores. A proposta A fica a {pct(t_ant)} de troca da proposta anterior: '
              + ('equivalente.' if t_ant < 0.10 else 'mais perto dela que os 12, mas acima do limite de equivalência.')))
    tm12 = troca_mun(vv, 'ivs_a', 'ivs_os_12')
    tm12 = tm12[tm12['size'] >= PISO_MUN].sort_values('mean', ascending=False)
    D.add('A troca de faixa por município: com e sem idosos e crianças', [F_IVS],
          cab=['Município', 'Setores comuns', 'Troca A × os 12'], colW=[2.8, 1.6, 1.6],
          linhas=[[i, intbr(x['size']), pct(x['mean'])] for i, x in tm12.head(12).iterrows()], explica=explica(
              oque=f'A % de setores que mudam de faixa entre a proposta A e os 12 em cada município (com {PISO_MUN} '
                   'setores comuns ou mais); os 12 maiores.',
              serve='Mostra que a decisão sobre idosos e crianças pesa por cidade, não só em média.',
              ler='Até 10% é tratado como equivalente.',
              mostra=f"Mediana entre os municípios: {pct(tm12['mean'].median())}; {int((tm12['mean'] >= 0.30).sum())} de "
                     f"{len(tm12)} passam de 30%."))

    # ── sensibilidade
    D.secao('Sensibilidade', 'Quanto o corte e o IVS mudam com cada alternativa.')
    s_sem, s_12 = (sc[sc['familia'] == x].set_index('variante') for x in ('12_sem_idade', '12'))
    def ban_em(r):  # noqa: E306
        return f"{'fica' if r['ban_fica'] else 'sai'} ({br(r['ban_carga'], 3)})" + (' †' if r['alerta'] else '')
    mostrar = ['varimax', 'varimax_kaiser', 'promax', 'promax_k3_nenhuma', 'promax_k2_nenhuma', 'promax_k4_spss',
               'promax_k2_spss', 'promax_estrutura', 'varimax_municipal', 'promax_municipal', 'varimax_3f', 'promax_3f']
    ficam_sem = int(s_sem['ban_fica'].sum())
    sem_ban = sc[sc['familia'] == 'sem_idade_sem_banheiro'].iloc[0]
    tira = [x for x in fc.FAMILIAS['12_sem_idade'] if x not in sem_ban['mantidos'].split('+') and x not in ('BAN', 'LIX', 'MNC')]
    lm_fora = sc[sc['familia'] != 'sem_idade_sem_banheiro']['mantidos'].map(lambda s: not {'LIX', 'MNC'} & set(s.split('+')))
    D.add('O corte muda com as escolhas de método', [F_SC],
          cab=['Variante', 'Sem banheiro (sem idosos)', 'Ficam', 'Sem banheiro (os 12)', 'Ficam'],
          colW=[2.7, 1.6, 0.6, 1.6, 0.6],
          linhas=[[s_sem.at[k, 'rotulo'], ban_em(s_sem.loc[k]), str(s_sem.at[k, 'p']), ban_em(s_12.loc[k]), str(s_12.at[k, 'p'])]
                  for k in mostrar], explica=explica(
              'O corte refeito mudando uma escolha por vez: normalização de Kaiser, kappa da promax, matriz de estrutura, '
              'postos dentro do município e 3 fatores.',
              'Mostra se a saída do sem banheiro é dos dados ou do método. É o indicador que separa A e B.',
              'Entre parênteses, a última carga do sem banheiro. † marca alerta de solução imprópria (Heywood) ou falta de '
              f'convergência em algum passo. "Ficam": indicadores que sobram. Nas {len(s_sem)} variantes rodadas, a tabela '
              'mostra as principais.',
              f'Sem idosos e crianças, ele fica em {ficam_sem} de {len(s_sem)} variantes. Lixo e moradia não convencional saem '
              f"em {int(lm_fora.sum())} de {len(lm_fora)}. O esgoto também é frágil: sai em {int((~s_sem['mantidos'].str.contains('ESG')).sum())} "
              f'de {len(s_sem)}. Tirar o sem banheiro da promax não basta: {junta(nomes(tira)) if tira else "nada mais"} '
              'também saem.'))
    igual = {x: int(corte.loc[corte['proposta'] == x, 'igual_a_proposta'].sum()) for x in AB}
    D.add('O sem banheiro quando os municípios mudam', [F_SR, F_CORTE],
          cab=['Rotação', 'Réplicas', 'Corte mantém o sem banheiro', 'Carga mediana', 'Faixa de 95%'],
          colW=[1.3, 0.9, 2.1, 1.2, 1.4],
          linhas=[[ROTA[k], intbr(x['replicas']), pct(x['ban_fica']), br(x['carga_mediana'], 3),
                   f"{br(x['carga_p025'], 3)} a {br(x['carga_p975'], 3)}"] for k, x in sr.iterrows()], explica=explica(
              'Os 70 municípios sorteados com reposição, e o corte refeito em cada sorteio.',
              'Mede o quanto o destino do sem banheiro depende de quais municípios entram. Não é erro amostral: o Censo não '
              'é amostra.',
              f'Tirar uma cidade por vez repete a lista em {igual["a"]} (A) e {igual["b"]} (B) de {corte["fora"].nunique()} '
              'rodadas: nenhuma cidade sozinha decide. O sorteio muda os 70 de uma vez, e a carga oscila mais. Os dois '
              'resultados são compatíveis.',
              'A faixa de 95% da carga cobre o 0,40 nas duas rotações: a regra não separa A e B com folga.'))
    D.add('Os retirados voltam à lista?', [F_SE], cab=['Proposta', 'Indicador que volta', 'Carga', 'Passa no 0,4?'],
          colW=[2.0, 2.8, 1.0, 1.2],
          linhas=[[PAPEL[x['proposta']], NOME[x['codigo']], br(x['carga'], 3), 'sim' if x['passa'] else 'não']
                  for _, x in se.iterrows()], explica=explica(
              'Cada indicador retirado volta sozinho à lista final da proposta, e a fatorial é refeita.',
              'A amostra cresce quando o sem banheiro sai, e o corte retira um por vez: confere se a ordem deixou de fora '
              'alguém que passaria.',
              'Carga do indicador que voltou, na mesma rotação da proposta.',
              f"{int(se['passa'].sum())} de {len(se)} voltas passam no 0,4."))
    cruz = []
    for x in AB:
        ordenada = np.sort(np.abs(M[x]), axis=1)
        cruz += [[PAPEL[x], NOME[k], br(ordenada[i, 1], 3), br(ordenada[i, 0], 3)] for i, k in enumerate(cods[x])
                 if ordenada[i, 0] >= 0.30]
    D.add('As cargas cruzadas das propostas', [F_FINALISTAS], cab=['Proposta', 'Indicador', 'Maior carga', 'Outra carga'],
          colW=[2.0, 2.8, 1.1, 1.1], linhas=cruz or [['—', 'nenhuma', '—', '—']], explica=explica(
              'Os indicadores com carga de pelo menos 0,30 nos dois fatores.',
              'O índice põe cada indicador só no fator de maior carga. Carga alta nos dois enfraquece essa escolha.',
              'Quanto mais perto as duas cargas, mais frágil é dizer a que dimensão o indicador pertence.',
              f'{len(cruz)} casos. A regra do 0,4 olha só a maior carga e não testa a outra.'))
    cols_ivs = [f'ivs_{x}' for x in fin_['papel']]
    Rf = ivs[cols_ivs].corr(method='spearman')
    piso_r = np.floor(20 * Rf.to_numpy().min()) / 20
    D.add('Concordância entre as finalistas', [F_IVS],
          figura=mapa_calor(Rf, 'C04_concordancia.png', piso_r, 1, 'Greens', rot={x: PAPEL[x[4:]] for x in cols_ivs}),
          legenda='Spearman entre os IVS das finalistas, nos setores que cada par tem.', explica=explica(
              oque='A correlação de Spearman entre os IVS de cada par de finalistas, no conjunto dos setores.',
              serve='Mostra o quanto as alternativas ordenam os setores do mesmo jeito.',
              ler=f'1 = mesma ordem dos setores; quanto mais claro, mais as duas versões discordam. A escala começa em {br(piso_r, 2)}.'))
    comum = vv[vv['ivs_a'].notna()]
    fcu_c = comum['is_fcu'].to_numpy(dtype=float)
    renda_c = -comum['renda_media_sem_extremo'].to_numpy()
    okc = ~np.isnan(fcu_c) & ~np.isnan(renda_c)
    linhas = [[PAPEL[x.papel], br(x.auc_fcu, 3), br(x.auc_renda_sozinha, 3),
               br(fa.auc_postos(comum[f'ivs_{x.papel}'].to_numpy()[okc], fcu_c[okc]), 3)] for x in fin_.itertuples()]
    linhas.append(['renda sozinha', '—', '—', br(fa.auc_postos(renda_c[okc], fcu_c[okc]), 3)])
    D.add('A AUC contra favela, como descrição', [F_FINALISTAS, F_IVS],
          cab=['Finalista', 'AUC (amostra própria)', 'Renda (amostra própria)', 'AUC nos setores da A'],
          colW=[2.4, 1.5, 1.6, 1.6], linhas=linhas, explica=explica(
              oque='A AUC mede o quanto o índice separa os setores de favela dos demais: 0,5 = acaso; 1 = separação perfeita.',
              serve='Era usada como validação nas versões anteriores. Fica aqui como descrição.',
              ler='As duas primeiras colunas usam a amostra de cada finalista e não se comparam entre linhas (a própria '
                  'renda muda de amostra para amostra). A última usa os mesmos setores (os da A) para todas.',
              mostra='Nos mesmos setores, a renda sozinha separa favela tão bem ou melhor que qualquer índice: a AUC '
                     'acompanha o conteúdo socioeconômico e não serve para julgar os pesos.'))
    pp = perf[perf['grupo'] == 'perdidos']
    falta = {k: int(df[fm.VARS[k]].isna().sum()) for k in ('ANA', 'BAN')}
    D.add('Quantos setores cada finalista perde', [F_PERF],
          cab=['Finalista', 'Perdidos', '% recorte', 'Renda mediana', '% favela'], colW=[2.4, 1.1, 1.0, 1.6, 1.0],
          linhas=[[PAPEL[x.id], intbr(x.setores), pct(x.pct_recorte), fmt('REN', x.renda_mediana), pct(x.pct_fcu)]
                  for x in pp.itertuples()],
          explica=explica(
              oque='Os setores do recorte que ficam sem IVS em cada finalista, por dado ausente num componente.',
              serve='Perder setores é decisão.',
              ler=f"No recorte, faltam o analfabetismo em {intbr(falta['ANA'])} setores e o sem banheiro em "
                  f"{intbr(falta['BAN'])}. Nas finalistas com o sem banheiro, os perdidos misturam os dois grupos.",
              mostra='A mediana dos perdidos da A parece "mais rica", mas junta dois grupos opostos (slide "Quem cada '
                     'proposta deixa sem IVS").'))

    # ── decisões
    D.secao('As decisões', 'O que a regra resolve e o que continua com a orientação.')
    alt = v[(v['familia'] == '12_sem_idade') & ~((v['rotacao'] == fc.FINAL[0]) & (v['metodo'] == fc.FINAL[1]))]
    troca_alt = alt.set_index(['rotacao', 'metodo'])['troca_faixa_vs_final']
    ban_b = p[(p['familia'] == '12_sem_idade') & (p['rotacao'] == 'varimax') & (p['codigo'] == 'BAN')].sort_values('passo')['carga_max']
    D.add('O que levar à orientação', [F_PASSOS, F_VERSOES, F_FINAIS, F_CORTE, F_IVS],
          cab=['#', 'Ponto', 'O que os dados mostram', 'Pergunta'], colW=[0.35, 1.6, 3.6, 1.75], linhas=[
              ['1', junta(nomes(sempre)).capitalize(), f'saem nas {len(saem)} combinações de rotação e família',
               '— (a regra resolve, com 2 fatores)'],
              ['2', 'Proposta A ou B', f'A (promax) mantém o sem banheiro, com peso de {pct(prop.at["a", "peso_BAN"])} e comunalidade {br(ban.loc[("12_sem_idade", "promax"), "h2"], 2)}; '
                                       f'na Varimax ele começa em {br(ban_b.iloc[0], 3)} e sai em {br(ban_b.iloc[-1], 3)}. A '
                                       f'custa {intbr(perda)} setores, {pct(so_a["is_fcu"].mean())} deles favela e mais '
                                       f'pobres. B (Varimax) cobre {pct(prop.at["b", "pct_recorte"])} do recorte. A × B: '
                                       f'{pct(cab_ab["troca_faixa"])} de troca', 'qual rotação?'],
              ['3', 'Idosos e crianças', f'passam no corte, mas levam {br(pi, 1)}% do índice e invertem os idosos; '
                                         f'{pct(par.at[("12", "12_sem_idade"), "troca_faixa"])} de troca (mediana por '
                                         f'município {pct(tm12["mean"].median())})', 'ficam fora, como contexto?'],
              ['4', 'Critérios do projeto', f'nenhuma proposta passa na comunalidade de 0,30 (A: {br(pior["a"][1], 2)}; '
                                            f'B: {br(pior["b"][1], 2)}); só os 12 com Varimax passam em tudo',
               'a comunalidade vira critério?'],
              ['5', 'Método de peso', 'contra a A, os métodos da promax que saem dos dados ficam a no máximo '
                                      f'{pct(troca_alt["promax"].drop("50_50").max())} de troca; o 50/50 vai a '
                                      f'{pct(troca_alt["promax", "50_50"])} na promax e {pct(troca_alt["varimax", "50_50"])} na Varimax, '
                                      f'e sem rotação a {pct(troca_alt["sem_rotacao"].max())}',
               'manter 60/40?']],
          explica=explica(
              'Os cinco pontos que saem desta análise, com a pergunta que cada um deixa.',
              'É o que precisa de decisão da orientadora.',
              'A regra do 0,4 resolve o ponto 1, dada a escolha de 2 fatores; os outros são escolhas.',
              'A decisão principal é entre A e B: rotação contra cobertura dos setores mais pobres, com o sem banheiro '
              'perto do corte nas duas.'))
    D.add('Limitações', [F_ADEQ, F_VERSOES], blocos=[
        ['Estudo ecológico.', 'As relações são entre setores, não entre pessoas.'],
        ['Número de fatores.', f'O corte usa 2 fatores em todos os passos, como o IVS de 2012. Com os 12 juntos, Kaiser '
                               f'retém {int(adeq["kaiser"])} e Horn {int(adeq["horn"])}; Kaiser e Horn não são refeitos a '
                               'cada retirada. O corte com 3 fatores está em "O corte muda com as escolhas de método".'],
        ['Critérios que não cabem juntos.', 'Com um fator, comunalidade é carga ao quadrado: a carga de 0,40 da regra '
                                            'corresponde a comunalidade 0,16, abaixo do mínimo de 0,30.'],
        ['Sigilo.', 'O analfabetismo sob sigilo fica ausente, e o ausente cai nos setores de renda mais alta; o sem '
                    'banheiro ausente cai nos mais pobres.'],
        ['Carga acima de 1.', f"Na proposta A a renda tem carga padrão de {br(M['a'][cods['a'].index('REN'), 0], 3)}: "
                              'possível na promax, mas pede cautela ao ler o peso da renda.'],
        ['Sem normalização de Kaiser.', 'Varimax e promax foram calculadas sem ela, ao contrário do padrão de SPSS e R. '
                                        'O efeito está no slide "O corte muda com as escolhas de método".'],
        ['Faixas relativas.', 'As faixas são calculadas dentro de cada município: dizem a posição do setor na própria '
                              'cidade, não comparam o nível de vulnerabilidade entre cidades.'],
        ['Amostras.', 'Cada versão roda nos setores com todos os seus indicadores; as comparações refazem as faixas nos '
                      'setores comuns, mas não a régua mín-máx.'],
        ['Autocorrelação espacial.', 'Setores vizinhos não são independentes; o I de Moran fica para o geoprocessamento.'],
        ['Validação.', 'Não há desfecho de saúde no projeto; a AUC contra favela é só descrição.']])
    D.add('Próximos passos', ['scripts/fatorial_corte_04.py'], blocos=[
        ['1.', 'Levar os cinco pontos à orientadora, começando pela escolha entre A e B.'],
        ['2.', 'Recalcular o IVS com as escolhas dela (o motor roda qualquer família, rotação e peso).'],
        ['3.', 'Se a orientadora pedir: um caminho híbrido para os setores sem o dado do banheiro, que exige outra régua.'],
        ['4.', 'Mapas temáticos no QGIS 3.x e I de Moran; redação do artigo e do relatório final.']])

    # ── apêndices
    D.do_fin(DO_FIN['apendice'])
    rows = []
    for mun_, g in sorted(vv.groupby('NM_MUN'), key=lambda kv: sem_acento(kv[0])):
        cel_ = []
        for x in AB:
            ok = g[g[f'faixa_{x}'] >= 0]
            cel_ += [intbr(len(ok)), pct((ok[f'faixa_{x}'] >= 2).mean()) if len(ok) else '—']
        rows.append([mun_ + (' *' if len(g[g['faixa_a'] >= 0]) < 30 else ''), *cel_])
    for k, parte in enumerate((rows[:35], rows[35:])):
        D.add(f'Apêndice: os 70 municípios ({k + 1} de 2) · * menos de 30 setores na A', [F_IVS],
              cab=['Município', 'A setores', 'A % elev.', 'B setores', 'B % elev.'], linhas=parte, duas=True)
    secoes = [(D.slides[i]['numero'], D.slides[i]['titulo'], D.ordem.index(i) + 1) for i in D.ordem if 'numero' in D.slides[i]]
    n_de = {D.slides[i]['titulo']: D.ordem.index(i) + 1 for i in D.ordem}
    D.slides[sumario].update(linhas=[[a_, b_, str(c_)] for a_, b_, c_ in secoes], explica=explica(
        'As seções, na ordem em que aparecem.', 'Para ir direto ao que interessa.',
        f"A decisão resumida está no slide {n_de['A decisão em uma página']}, os termos no {n_de['Os termos desta apresentação']} "
        f"e as perguntas à orientadora no {n_de['O que levar à orientação']}."))
    D.slides[resumo].update(linhas=[
        ['Indicadores', str(len(cods['a'])), str(len(cods['b']))],
        ['Setores com IVS', f"{intbr(n_ab['a'])} ({pct(prop.at['a', 'pct_recorte'])})", f"{intbr(n_ab['b'])} ({pct(prop.at['b', 'pct_recorte'])})"],
        ['Sem banheiro no corte', f"fica ({br(ban.loc[('12_sem_idade', 'promax'), 'carga_max'], 3)})",
         f"sai ({br(ban_b.iloc[0], 3)} no 1º passo, {br(ban_b.iloc[-1], 3)} ao sair)"],
        ['Peso do sem banheiro', pct(prop.at['a', 'peso_BAN']), '—'],
        ['Corte mantém o sem banheiro ao sortear municípios', pct(sr.at['promax', 'ban_fica']), pct(sr.at['varimax', 'ban_fica'])],
        ['Comunalidade mínima (mínimo do projeto: 0,30)', br(pior['a'][1], 3), br(pior['b'][1], 3)],
        ['Tucker F1 · F2', f"{br(rep.at['a', 'tucker_F1'], 3)} · {br(rep.at['a', 'tucker_F2'], 3)}",
         f"{br(rep.at['b', 'tucker_F1'], 3)} · {br(rep.at['b', 'tucker_F2'], 3)}"],
        ['Fatores correlacionados (Φ)', br(r_['a']['phi'][0, 1], 3) + ': a promax admite', br(r_['b']['phi'][0, 1], 3) + ': a Varimax ignora'],
    ], explica=explica(
        'As duas propostas e o que cada uma custa. Ambas tiram idosos e crianças por decisão do projeto, não pela regra.',
        'É a decisão que esta apresentação leva à orientadora.',
        'A leva o sem banheiro e perde setores; B cobre mais setores e usa uma rotação que trata os fatores como '
        'independentes, embora estejam correlacionados.',
        f'A × B: {pct(cab_ab["troca_faixa"])} de troca de faixa nos setores comuns. A regra do 0,4 não decide sozinha, porque o sem '
        f'banheiro fica perto do corte; A deixa sem IVS {intbr(perda)} setores mais pobres. Pergunta: que regra de corte vale?'))
    D.gravar()
    print(f'{len(D.ordem)} slides → {dm.DADOS.relative_to(RAIZ)}/C04.json')


if __name__ == '__main__':
    main()
