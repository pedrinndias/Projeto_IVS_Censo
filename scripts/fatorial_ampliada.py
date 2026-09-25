"""Fatorial ampliada, sem bootstrap — demandas 3, 5, 6, 7, 8, 9, 10 e 11 da orientadora.

As oito demandas são uma análise só: uma grade de cenários, cada um rodado da mesma forma
e gravado numa tabela só. A receita é a do Notebook 04, para ser comparável: Spearman,
casos completos **por cenário**, extração por componentes principais, renda invertida,
2 fatores em todos os cenários (Kaiser e Horn reportados ao lado), e a solução sem
rotação, em Varimax e em promax (padrão, estrutura e Φ). **Sem bootstrap** (demanda 3):
a incerteza vira sensibilidade por município — um de fora por vez —, que **não** é
bootstrap e não deve ser lida como intervalo de confiança.

Cenários (ver `CENARIOS`): S0 = IVS-7 (reproduz o NB04, trava de sanidade), S1 = sem lixo,
S2–S5 = IVS-7 + uma variável nova, S6 = IVS-7 + as quatro, S7 = S6 sem lixo. Para S0 e
S6, as outras duas versões de renda (sem o extremo, imputada com a mediana municipal —
a original é o próprio S0/S6). Para S0, S1 e S6, a versão com postos **dentro do
município**, que tira da matriz a diferença entre cidades.

Nada aqui escolhe pela orientadora: nenhuma rotação, renda ou variável é "a certa"; o
script só põe as alternativas lado a lado. O IVS final é do NB05.

A matemática vive em `src/ivs_censo/fatorial.py` (`rodar_cenario`, com a Varimax já
corrigida — FAT-01). As funções de índice, AUC e figura são cópias do NB04, com a célula
de origem indicada em cada uma, para que o número daqui e o de lá saiam da mesma conta.

Uso:
    python scripts/fatorial_ampliada.py

Saídas: `banco_de_dados/eda/fatorial_ampliada/` (ver o README.md de lá) e um resumo de no
máximo 40 linhas no stdout. Depende de pandas, numpy e matplotlib (só para as figuras).
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'src'))

from ivs_censo.fatorial import IVS7, ROTULOS, alinhar_cargas, rodar_cenario  # noqa: E402

DB = RAIZ / 'banco_de_dados' / 'entrega_orientadora' / 'Base_ELSI_70Municipios_Censo2022.db'
SAIDA = RAIZ / 'banco_de_dados' / 'eda' / 'fatorial_ampliada'
FIG = SAIDA / 'figuras'
LINHA_BASE = SAIDA / 'linha_de_base_nb04.csv'

# Trava de sanidade (prompt de set/2026, 2.2). S0 tem de reproduzir o KMO do NB04, lido da
# linha de base; S1, os pesos da Varimax corrigida — 65,01, e não os 65,04 da Varimax que
# parava cedo (FAT-01). Na 1ª casa, os dois dão 65,0. Se não bater, o defeito é do motor.
PESO_S1_VARIMAX = 65.01

IVS7_INV = [c if c != 'renda_media' else 'renda_inv' for c in IVS7]
NOVAS = ['pct_agua_nao_encanada', 'pct_sem_agua_canalizada', 'pct_sem_banheiro',
         'pct_moradia_nao_convencional']
ROT = {**ROTULOS,
       'pct_agua_nao_encanada': 'Água não chega',
       'pct_sem_agua_canalizada': 'Sem água canalizada',
       'pct_sem_banheiro': 'Sem banheiro',
       'pct_moradia_nao_convencional': 'Moradia não convencional',
       'pct_agua_so_terreno': 'Água só no terreno',
       'renda_media': 'Renda média'}
RENDAS = {'original': 'renda_media', 'sem_extremo': 'renda_media_sem_extremo',
          'mediana_mun': 'renda_media_mediana_mun'}


def _sem_lixo(cols):
    return [c for c in cols if c != 'pct_lixo_inad']


# nome, variáveis, descrição, demanda
CENARIOS = [
    ('S0', IVS7_INV, 'IVS-7 (referência, reproduz o NB04)', '—'),
    ('S1', _sem_lixo(IVS7_INV), 'IVS-6 (IVS-7 sem lixo)', '10'),
    ('S2', IVS7_INV + ['pct_agua_nao_encanada'], 'IVS-7 + não chega', '5, 7'),
    ('S3', IVS7_INV + ['pct_sem_agua_canalizada'], 'IVS-7 + sem canalização', '7'),
    ('S4', IVS7_INV + ['pct_sem_banheiro'], 'IVS-7 + sem banheiro (V00495)', '6, 7'),
    ('S5', IVS7_INV + ['pct_moradia_nao_convencional'], 'IVS-7 + não convencional', '9'),
    ('S6', IVS7_INV + NOVAS, 'IVS-7 + as quatro ("tudo isso")', '8'),
    ('S7', _sem_lixo(IVS7_INV + NOVAS), 'S6 sem lixo', '8, 10'),
]
VARIANTES_RENDA = ['S0', 'S6']          # + sem_extremo e mediana_mun (a original é o próprio)
VARIANTES_MUNICIPIO = ['S0', 'S1', 'S6']  # postos dentro do município e um de fora por vez


# ── Paleta e figuras: copiadas do NB04 (célula 3) ────────────────────────────
TINTA, PETROL, CLAY, CINZA = '#1A1A1A', '#1F4E4A', '#A83A2C', '#666666'
SURF = '#FCFCFB'
VIRGULA = plt.matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:g}'.replace('.', ','))


def rampa_divergente(v):
    """Interpola cinza-claro -> clay (positivo) ou cinza-claro -> petrol (negativo). NB04, célula 3."""
    neutro = np.array([0.94, 0.94, 0.93])
    alvo = np.array([0.659, 0.227, 0.173]) if v >= 0 else np.array([0.122, 0.306, 0.290])
    t = min(abs(v), 1.0)
    return tuple(neutro + t * (alvo - neutro))


def salvar(fig, nome):
    """Grava a figura no padrão do projeto (dpi 150). NB04, célula 3."""
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / nome, dpi=150, bbox_inches='tight', facecolor=SURF)
    plt.close(fig)
    return nome


def posicionar_rotulos(pontos, textos, lim=1.0):
    """Escolhe, para cada rótulo, a direção que menos colide. NB04, célula 22, sem mudança."""
    alt, larg_car = 0.085, 0.036
    direcoes = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    postos_ = []
    for (px, py), txt in zip(pontos, textos):
        larg = larg_car * len(txt)
        melhor, melhor_custo = None, np.inf
        for raio in (0.11, 0.20):
            for dx, dy in direcoes:
                norma = np.hypot(dx, dy) or 1
                cx = px + raio * dx / norma + (larg / 2) * np.sign(dx)
                cy = py + raio * dy / norma + (alt / 2) * (dy if dy else 0.6)
                custo = 0.0
                custo += 300 * max(0, (cx + larg / 2) - lim) + 300 * max(0, -lim - (cx - larg / 2))
                custo += 300 * max(0, (cy + alt / 2) - lim) + 300 * max(0, -lim - (cy - alt / 2))
                for (qx, qy, ql, qa) in postos_:
                    ox = max(0, min(cx + larg/2, qx + ql/2) - max(cx - larg/2, qx - ql/2))
                    oy = max(0, min(cy + alt/2, qy + qa/2) - max(cy - alt/2, qy - qa/2))
                    custo += 40 * ox * oy
                for (ox_, oy_) in pontos:
                    if abs(ox_ - cx) < larg/2 and abs(oy_ - cy) < alt/2:
                        custo += 3
                if abs(cy) < alt / 2 or abs(cx) < 0.02:
                    custo += 2
                custo += 0.5 * raio
                if custo < melhor_custo:
                    melhor, melhor_custo = (cx, cy, larg, alt, dx, dy), custo
        postos_.append(melhor[:4])
        yield melhor


def rotulo_eixo(cargas, j, nomes):
    """Nome do eixo tirado das cargas, nunca fixo (NB4-08: o NB04 escrevia 'saneamento'
    num painel em que o fator 2 era o lixo). As duas variáveis de maior |carga| no fator."""
    ordem = np.argsort(-np.abs(cargas[:, j]))[:2]
    return f'Fator {j + 1} — ' + ' · '.join(nomes[i] for i in ordem)


def plano_fatorial(ax, cargas, nomes, destaque=(), titulo=''):
    """NB04, célula 22. Mudou: `destaque` aceita várias variáveis, o limite do quadro
    acompanha a maior carga (a padrão da promax pode passar de 1) e o rótulo do eixo sai
    das cargas (`rotulo_eixo`)."""
    lim = max(1.0, float(np.ceil(np.abs(cargas).max() * 10) / 10))
    ax.axhline(0, color=CINZA, lw=0.9, zorder=1)
    ax.axvline(0, color=CINZA, lw=0.9, zorder=1)
    pontos = [(cargas[i, 0], cargas[i, 1]) for i in range(len(nomes))]
    colocados = list(posicionar_rotulos(pontos, nomes, lim=lim))
    for i, nome in enumerate(nomes):
        x, y = pontos[i]
        fora = nome in destaque
        cor = CLAY if fora else PETROL
        cx, cy, larg, alt, dx, dy = colocados[i]
        if np.hypot(cx - x, cy - y) > 0.16:
            ax.plot([x, cx - np.sign(dx) * larg / 2 if dx else cx], [y, cy],
                    color=cor, lw=0.7, alpha=0.5, zorder=2)
        ax.scatter([x], [y], s=95 if fora else 70, color=cor, zorder=4,
                   edgecolor=SURF, linewidth=1.4)
        ax.text(cx, cy, nome, ha='center', va='center', fontsize=9, color=cor,
                fontweight='bold' if fora else 'normal', zorder=5)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.xaxis.set_major_formatter(VIRGULA); ax.yaxis.set_major_formatter(VIRGULA)
    ax.tick_params(colors=CINZA, labelsize=8.5)
    ax.set_xlabel(rotulo_eixo(cargas, 0, nomes), color=CINZA, fontsize=9)
    ax.set_ylabel(rotulo_eixo(cargas, 1, nomes), color=CINZA, fontsize=9)
    ax.set_title(titulo, color=TINTA, fontsize=11, loc='left')
    ax.set_aspect('equal')
    ax.grid(color=CINZA, alpha=0.12, lw=0.7); ax.set_axisbelow(True)
    for lado in ('top', 'right'):
        ax.spines[lado].set_visible(False)
    for lado in ('left', 'bottom'):
        ax.spines[lado].set_color(CINZA)
    ax.set_facecolor(SURF)


# ── Índice e validação: copiados do NB04 (células 28, 29 e 39) ───────────────
def pesos_indice(vmax, rep):
    """`montar_pesos` do NB04 (célula 28): cada variável vai para a dimensão de maior
    carga, e o peso da dimensão se reparte pelo quadrado da carga dentro dela."""
    dimensao = np.abs(vmax).argmax(axis=1)
    peso = np.zeros(vmax.shape[0])
    for j in range(vmax.shape[1]):
        membros = dimensao == j
        if membros.any():
            dentro = vmax[membros, j] ** 2
            peso[membros] = rep[j] * dentro / dentro.sum()
    return peso


def indice_01(d, colunas, peso):
    """O `indice_01` do NB04 (célula 29): min-max global e média ponderada."""
    sub = d[colunas]
    return ((sub - sub.min()) / (sub.max() - sub.min()) * peso).sum(axis=1).to_numpy()


def auc_postos(escore, positivo):
    """AUC por Mann–Whitney, como no NB04 (célula 39)."""
    r = pd.Series(np.asarray(escore, dtype=float)).rank().to_numpy()
    pos = np.asarray(positivo) == 1
    n1, n0 = pos.sum(), (~pos).sum()
    return float((r[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def lixo_fator_proprio(vmax, colunas):
    """O lixo está sozinho na dimensão de maior carga dele? (None se não há lixo.)"""
    if 'pct_lixo_inad' not in colunas:
        return None
    dim = np.abs(vmax).argmax(axis=1)
    return bool((dim == dim[colunas.index('pct_lixo_inad')]).sum() == 1)


# ── Dados ────────────────────────────────────────────────────────────────────
def carregar() -> pd.DataFrame:
    cols = (['CD_SETOR', 'NM_MUN', 'urbano', 'Dados_sig', 'is_fcu'] + IVS7
            + [RENDAS['sem_extremo'], RENDAS['mediana_mun']] + NOVAS
            + ['pct_agua_so_terreno', 'V00238', 'V00495'])
    con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    df = pd.read_sql(f"SELECT {', '.join(cols)} FROM setores_censitarios", con)
    con.close()
    # filtro numérico: `astype(str) == '1'` devolve zero sem erro se a coluna virar float (F2)
    df = df[(pd.to_numeric(df['urbano'], errors='coerce') == 1) & (df['Dados_sig'] == 'OK')].copy()
    for c in ['is_fcu', 'V00238', 'V00495']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    return df


def montar(df, colunas, renda='original', transf='empilhada'):
    """Base de um cenário: exclusão por lista nas variáveis dele, e só nelas."""
    d = df[['CD_SETOR', 'NM_MUN', 'is_fcu']].copy()
    for c in colunas:
        d[c] = -df[RENDAS[renda]] if c == 'renda_inv' else df[c]
    d = d.dropna(subset=colunas)
    zeros = (d[colunas] == 0).mean()
    if transf == 'postos_mun':
        # posto percentil dentro do município: tira da matriz a diferença entre cidades
        d[colunas] = d.groupby('NM_MUN')[colunas].rank(pct=True)
    return d, zeros


# ── A grade ──────────────────────────────────────────────────────────────────
def rodar(df, nome, colunas, descricao, demanda, renda, transf, n_s0):
    d, zeros = montar(df, colunas, renda, transf)
    r = rodar_cenario(d[colunas].to_numpy())
    nomes = [ROT[c] for c in colunas]
    imin = int(np.argmin(r['msa']))
    val = r['autovalores']
    linha = {
        'cenario': nome, 'descricao': descricao, 'demanda': demanda, 'renda': renda,
        'transformacao': transf, 'p': r['p'], 'n': r['n'],
        'perdidos_vs_S0': (n_s0 - r['n']) if n_s0 is not None else 0,
        'kmo': r['kmo'], 'msa_min': float(r['msa'][imin]), 'msa_min_variavel': nomes[imin],
        'bartlett_qui2': r['bartlett_qui2'], 'bartlett_gl': r['bartlett_gl'],
        'det_R': r['det_R'], 'autovalor_1': val[0], 'autovalor_2': val[1], 'autovalor_3': val[2],
        'fatores_kaiser': r['kaiser'], 'fatores_horn': r['horn_retidos'],
        'kaiser_horn_discordam': r['kaiser'] != r['horn_retidos'],
        'var_explicada_2f': r['var_explicada_k'],
        'lixo_fator_proprio_varimax': lixo_fator_proprio(r['varimax'], colunas),
    }
    peso = pesos_indice(r['varimax'], r['pesos']['varimax'])
    cargas = pd.DataFrame({'cenario': nome, 'variavel': colunas, 'rotulo': nomes})
    for chave in ('sem_rotacao', 'varimax', 'promax_padrao', 'promax_estrutura'):
        for j in range(2):
            cargas[f'{chave}_f{j + 1}'] = r[chave][:, j]
    cargas['comunalidade'] = r['comunalidade']
    cargas['comunalidade_obliqua'] = r['comunalidade_obliqua']
    cargas['msa'] = r['msa']
    cargas['pct_zeros'] = 100 * zeros[colunas].to_numpy()
    cargas['peso_indice_varimax'] = peso
    pesos = []
    for rot, rep in r['pesos'].items():
        M = r[rot]
        pesos.append({'cenario': nome, 'rotacao': rot,
                      'peso_f1': 100 * rep[0], 'peso_f2': 100 * rep[1],
                      'f1_maior_carga': nomes[int(np.abs(M[:, 0]).argmax())],
                      'f2_maior_carga': nomes[int(np.abs(M[:, 1]).argmax())],
                      'phi': r['phi'][0, 1] if rot.startswith('promax') else np.nan})
    fcu = d['is_fcu'].to_numpy()
    ok = ~np.isnan(fcu)
    medidas = {'indice_01 (pesos Varimax)': indice_01(d, colunas, peso),
               'renda invertida sozinha': d['renda_inv'].to_numpy(),
               'media simples de postos': d[colunas].rank(pct=True).mean(axis=1).to_numpy()}
    valid = [{'cenario': nome, 'medida': m, 'n': int(ok.sum()), 'n_fcu': int((fcu[ok] == 1).sum()),
              'auc': auc_postos(e[ok], fcu[ok])} for m, e in medidas.items()]
    autoval = pd.DataFrame({'cenario': nome, 'componente': np.arange(1, r['p'] + 1),
                            'autovalor': val, 'horn': r['horn']})
    return {'linha': linha, 'cargas': cargas, 'pesos': pesos, 'valid': valid,
            'autoval': autoval, 'r': r, 'd': d, 'colunas': colunas}


def sensibilidade(nome, s):
    """Um município de fora por vez (70 rodadas). É sensibilidade, não bootstrap."""
    ref, d, colunas = s['r'], s['d'], s['colunas']
    nomes = [ROT[c] for c in colunas]
    p0v, p0p = 100 * ref['pesos']['varimax'][0], 100 * ref['pesos']['promax_padrao'][0]
    lixo0 = lixo_fator_proprio(ref['varimax'], colunas)
    f1 = nomes[int(np.abs(ref['varimax'][:, 0]).argmax())]
    linhas = [{'cenario': nome, 'municipio_fora': '(nenhum)', 'n': ref['n'],
               'fator1_maior_carga': f1, 'peso_f1_varimax': p0v, 'delta_varimax': 0.0,
               'peso_f1_promax_padrao': p0p, 'delta_promax_padrao': 0.0,
               'lixo_fator_proprio': lixo0}]
    for mun in sorted(d['NM_MUN'].unique()):
        r = rodar_cenario(d.loc[d['NM_MUN'] != mun, colunas].to_numpy(), com_horn=False)
        V = alinhar_cargas(r['varimax'], ref['varimax'])
        P = alinhar_cargas(r['promax_padrao'], ref['promax_padrao'])
        pv = 100 * (V[:, 0] ** 2).sum() / (V ** 2).sum()
        pp = 100 * (P[:, 0] ** 2).sum() / (P ** 2).sum()
        linhas.append({'cenario': nome, 'municipio_fora': mun, 'n': r['n'],
                       'fator1_maior_carga': f1, 'peso_f1_varimax': pv, 'delta_varimax': pv - p0v,
                       'peso_f1_promax_padrao': pp, 'delta_promax_padrao': pp - p0p,
                       'lixo_fator_proprio': lixo_fator_proprio(V, colunas)})
    t = pd.DataFrame(linhas)
    rod = t['municipio_fora'] != '(nenhum)'
    for col in ('delta_varimax', 'delta_promax_padrao'):
        t[f'mais_move_{col[6:]}'] = rod & (t[col].abs() == t.loc[rod, col].abs().max())
    t['lixo_muda'] = rod & (t['lixo_fator_proprio'] != lixo0) if lixo0 is not None else False
    return t


def comparacao(df):
    """Demandas 5 e 6: Spearman, perfil (> 0 × = 0) e a prova de que V00495 contém V00238."""
    linhas = []
    outras = IVS7 + ['pct_agua_so_terreno', 'pct_sem_agua_canalizada']
    for ind in ('pct_agua_nao_encanada', 'pct_sem_banheiro'):
        outro = 'pct_sem_banheiro' if ind == 'pct_agua_nao_encanada' else 'pct_agua_nao_encanada'
        for v in outras + [outro]:
            par = df[[ind, v]].dropna()
            linhas.append({'bloco': 'spearman', 'indicador': ROT[ind], 'variavel': ROT[v],
                           'grupo': '', 'valor': par[ind].rank().corr(par[v].rank()),
                           'n': len(par)})
        for v in IVS7:
            for g, m in (('> 0', df[ind] > 0), ('= 0', df[ind] == 0)):
                s = df.loc[m, v].dropna()
                linhas.append({'bloco': 'perfil_mediana', 'indicador': ROT[ind],
                               'variavel': ROT[v], 'grupo': g, 'valor': s.median(), 'n': len(s)})
    ambos = df[['V00238', 'V00495']].dropna()
    linhas.append({'bloco': 'prova_juncao', 'indicador': 'V00238 <= V00495',
                   'variavel': 'setores em que vale', 'grupo': '',
                   'valor': int((ambos['V00238'] <= ambos['V00495']).sum()), 'n': len(ambos)})
    return pd.DataFrame(linhas)


# ── Figuras ──────────────────────────────────────────────────────────────────
def figuras(s6, sens):
    r, colunas = s6['r'], s6['colunas']
    nomes = [ROT[c] for c in colunas]
    p, n7 = len(colunas), len(IVS7_INV)

    fig, ax = plt.subplots(figsize=(9.6, 8.4), facecolor=SURF)
    R = r['R']
    ax.imshow(np.array([[rampa_divergente(R[i, j]) for j in range(p)] for i in range(p)]))
    for i in range(p):
        for j in range(p):
            ax.text(j, i, f'{R[i, j]:.2f}'.replace('.', ','), ha='center', va='center',
                    fontsize=8, color=SURF if abs(R[i, j]) > 0.55 else TINTA)
    ax.axhline(n7 - 0.5, color=TINTA, lw=1.6); ax.axvline(n7 - 0.5, color=TINTA, lw=1.6)
    ax.set_xticks(range(p)); ax.set_xticklabels(nomes, rotation=45, ha='right', fontsize=9)
    ax.set_yticks(range(p)); ax.set_yticklabels(nomes, fontsize=9)
    n_fmt = f"{r['n']:,}".replace(',', '.')
    ax.set_title(f'Spearman — IVS-7 e as quatro novas (S6, n = {n_fmt})',
                 color=TINTA, fontsize=11.5, loc='left')
    feitas = [salvar(fig, 'fa_correlacao_ampliada.png')]

    fig, ax = plt.subplots(figsize=(7.6, 4.6), facecolor=SURF)
    k = np.arange(1, p + 1)
    ax.plot(k, r['autovalores'], 'o-', color=PETROL, label='autovalor observado')
    ax.plot(k, r['horn'], '--', color=CLAY, label='Horn (dados aleatórios)')
    ax.axhline(1, color=CINZA, lw=0.8, ls=':', label='Kaiser (autovalor 1)')
    ax.set_xticks(k); ax.yaxis.set_major_formatter(VIRGULA)
    ax.set_xlabel('componente', color=CINZA); ax.set_ylabel('autovalor', color=CINZA)
    ax.set_title('Scree plot de S6 com a linha de Horn', color=TINTA, fontsize=11.5, loc='left')
    ax.legend(frameon=False, fontsize=9); ax.set_facecolor(SURF)
    for lado in ('top', 'right'):
        ax.spines[lado].set_visible(False)
    feitas.append(salvar(fig, 'fa_scree_s6.png'))

    fig, eixos = plt.subplots(1, 3, figsize=(19.5, 6.9), facecolor=SURF)
    novas = {ROT[c] for c in NOVAS}
    for ax, (chave, tit) in zip(eixos, [('sem_rotacao', 'Sem rotação'), ('varimax', 'Varimax'),
                                         ('promax_padrao', 'Promax (matriz padrão)')]):
        plano_fatorial(ax, r[chave], nomes, destaque=novas, titulo=tit)
    fig.suptitle('Plano fatorial de S6 — as quatro variáveis novas em destaque',
                 color=TINTA, fontsize=12.5, x=0.007, ha='left', y=1.0)
    feitas.append(salvar(fig, 'fa_plano_s6.png'))

    fig, ax = plt.subplots(figsize=(9.2, 3.6), facecolor=SURF)
    rng = np.random.default_rng(42)                 # só o espalhamento vertical dos pontos
    for y, cen in enumerate(['S1', 'S6']):
        t = sens[(sens['cenario'] == cen)]
        rod = t[t['municipio_fora'] != '(nenhum)']
        ref = t.loc[t['municipio_fora'] == '(nenhum)', 'peso_f1_varimax'].iloc[0]
        ax.scatter(rod['peso_f1_varimax'], y + rng.uniform(-0.18, 0.18, len(rod)), s=16,
                   color=PETROL, alpha=0.6, edgecolor='none')
        ax.plot([ref, ref], [y - 0.3, y + 0.3], color=CLAY, lw=2)
        m = rod.loc[rod['mais_move_varimax']].iloc[0]
        ax.annotate(f"sem {m['municipio_fora']}", (m['peso_f1_varimax'], y + 0.22),
                    fontsize=8.5, color=CLAY, ha='center', va='bottom')
    ax.set_yticks([0, 1]); ax.set_yticklabels(['S1', 'S6']); ax.set_ylim(-0.6, 1.7)
    ax.xaxis.set_major_formatter(VIRGULA)
    ax.set_xlabel('peso do fator 1 na Varimax (%) — um município de fora por rodada', color=CINZA)
    ax.set_title('Sensibilidade por município (não é bootstrap) — traço: todos os municípios',
                 color=TINTA, fontsize=11, loc='left')
    ax.set_facecolor(SURF)
    for lado in ('top', 'right'):
        ax.spines[lado].set_visible(False)
    feitas.append(salvar(fig, 'fa_sensibilidade_municipios.png'))
    return feitas


def gravar(tab, nome):
    tab.to_csv(SAIDA / nome, sep=';', index=False, encoding='utf-8-sig', float_format='%.6f')


def main() -> None:
    df = carregar()
    # leitura linha a linha: a coluna `origem` da linha de base tem ';' dentro do texto
    linhas = LINHA_BASE.read_text(encoding='utf-8').splitlines()[1:]
    base = pd.Series({l.split(';')[0]: l.split(';')[1] for l in linhas if l.strip()})
    res = {}
    s0 = res['S0'] = rodar(df, *CENARIOS[0], 'original', 'empilhada', None)
    n_s0 = s0['r']['n']
    s1 = res['S1'] = rodar(df, *CENARIOS[1], 'original', 'empilhada', n_s0)

    # ── trava de sanidade: nada é gravado se S0/S1 não reproduzirem o NB04 ──
    kmo0 = round(s0['r']['kmo'], 4)
    peso1 = 100 * s1['r']['pesos']['varimax']
    ok_kmo = kmo0 == round(float(base['kmo']), 4)
    ok_peso = (round(peso1.max(), 2) == PESO_S1_VARIMAX
               and round(peso1.max(), 1) == round(float(base['pesos_ivs6_varimax_socioeconomica']), 1))
    print(f"trava S0: KMO {kmo0:.4f} (NB04 {float(base['kmo']):.4f}) -> {'ok' if ok_kmo else 'FALHOU'}")
    print(f"trava S1: pesos Varimax {peso1[0]:.2f}/{peso1[1]:.2f} (esperado {PESO_S1_VARIMAX:.2f}) "
          f"-> {'ok' if ok_peso else 'FALHOU'}")
    if not (ok_kmo and ok_peso):
        sys.exit('trava de sanidade falhou: o motor não reproduz o NB04 — nada foi gravado')

    for nome, cols, desc, dem in CENARIOS[2:]:
        res[nome] = rodar(df, nome, cols, desc, dem, 'original', 'empilhada', n_s0)
    for nome, cols, desc, dem in CENARIOS:
        if nome in VARIANTES_RENDA:
            for renda in ('sem_extremo', 'mediana_mun'):
                res[f'{nome}_renda_{renda}'] = rodar(df, f'{nome}_renda_{renda}', cols,
                                                     f'{desc}, renda {renda}', dem, renda,
                                                     'empilhada', n_s0)
        if nome in VARIANTES_MUNICIPIO:
            res[f'{nome}_postos_mun'] = rodar(df, f'{nome}_postos_mun', cols,
                                              f'{desc}, postos dentro do município', dem,
                                              'original', 'postos_mun', n_s0)

    SAIDA.mkdir(parents=True, exist_ok=True)
    cen = pd.DataFrame([s['linha'] for s in res.values()])
    gravar(cen, 'cenarios.csv')
    gravar(pd.concat([s['cargas'] for s in res.values()]), 'cargas.csv')
    pesos = pd.DataFrame([p for s in res.values() for p in s['pesos']])
    gravar(pesos, 'pesos.csv')
    valid = pd.DataFrame([v for s in res.values() for v in s['valid']])
    gravar(valid, 'validacao_fcu.csv')
    gravar(pd.concat([s['autoval'] for s in res.values()]), 'autovalores.csv')
    nomes6 = [ROT[c] for c in res['S6']['colunas']]
    gravar(pd.DataFrame(res['S6']['r']['R'], index=nomes6, columns=nomes6)
           .rename_axis('variavel').reset_index(), 'correlacao_s6.csv')
    comp = comparacao(df)
    gravar(comp, 'comparacao_nao_chega_banheiro.csv')
    sens = pd.concat([sensibilidade(c, res[c]) for c in VARIANTES_MUNICIPIO])
    gravar(sens, 'sensibilidade_municipios.csv')
    feitas = figuras(res['S6'], sens)

    # ── resumo (≤ 40 linhas) ──
    pv = pesos[pesos['rotacao'] == 'varimax'].set_index('cenario')
    pp = pesos[pesos['rotacao'] == 'promax_padrao'].set_index('cenario')
    pe = pesos[pesos['rotacao'] == 'promax_estrutura'].set_index('cenario')
    au = valid.pivot(index='cenario', columns='medida', values='auc')
    print('cenario               n      perd  KMO    MSAmin(var)          K/H  v2f   '
          'Varimax F1  PromaxP F1 PromaxE F1 phi    AUC ind/renda/postos')
    for _, c in cen.iterrows():
        k = c['cenario']
        print(f"{k:<21} {c['n']:>6} {c['perdidos_vs_S0']:>6} {c['kmo']:.4f} "
              f"{c['msa_min']:.3f}({c['msa_min_variavel'][:13]:<13}) {c['fatores_kaiser']}/"
              f"{c['fatores_horn']}  {c['var_explicada_2f']:.1f}  {pv.loc[k, 'peso_f1']:6.2f}"
              f"({pv.loc[k, 'f1_maior_carga'][:4]}) {pp.loc[k, 'peso_f1']:6.2f}     "
              f"{pe.loc[k, 'peso_f1']:6.2f}     {pp.loc[k, 'phi']:.3f}  "
              f"{au.loc[k, 'indice_01 (pesos Varimax)']:.4f}/{au.loc[k, 'renda invertida sozinha']:.4f}"
              f"/{au.loc[k, 'media simples de postos']:.4f}")
    for c in VARIANTES_MUNICIPIO:
        t = sens[(sens['cenario'] == c) & (sens['municipio_fora'] != '(nenhum)')]
        m = t.loc[t['mais_move_varimax']].iloc[0]
        print(f"sens {c}: peso F1 Varimax de {t['peso_f1_varimax'].min():.2f} a "
              f"{t['peso_f1_varimax'].max():.2f}; mais move: {m['municipio_fora']} "
              f"({m['delta_varimax']:+.2f}); lixo muda de fator em {int(t['lixo_muda'].sum())}")
    sp = sens[(sens['cenario'] == 'S1') & (sens['municipio_fora'] == 'São Paulo')]
    a1 = au.loc['S1']
    print(f"conferência NB04 (S1): AUC índice {a1['indice_01 (pesos Varimax)']:.4f} "
          f"(base {float(base['auc_indice']):.4f}), renda {a1['renda invertida sozinha']:.4f} "
          f"(base {float(base['auc_renda_invertida_sozinha']):.4f}), postos "
          f"{a1['media simples de postos']:.4f} (base {float(base['auc_media_postos_pesos_iguais']):.4f}),"
          f" sem SP {sp['peso_f1_varimax'].iloc[0]:.2f} (base {float(base['pesos_sem_sao_paulo']):.2f})")
    pj = comp[comp['bloco'] == 'prova_juncao'].iloc[0]
    print(f"prova da junção: V00238 <= V00495 em {int(pj['valor'])} de {int(pj['n'])} setores")
    print('figuras:', ', '.join(feitas))


if __name__ == '__main__':
    main()
