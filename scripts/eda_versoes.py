#!/usr/bin/env python
"""Motor das análises exploratórias por versão (blocos 1 a 13).

    ./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/<versao>

Lê `<versao>/config.json`, monta a base, roda os blocos marcados e grava `tabelas/`,
`figuras/`, `catalogo.csv` e `setores_indice.csv`. Um motor só para todas as versões: o
que muda é o `config.json`. Os IDs (T01…, F01…) são fixos por bloco, para que os decks
sejam comparáveis entre versões; bloco que não roda deixa o buraco na numeração.

O título e o "O que mostra" de cada item saem dos modelos de
`analises_exploratorias/_modelos/textos_blocos.json`, preenchidos com os `campos` que o
motor tira das próprias tabelas gravadas (todo número citado é uma célula do CSV do item,
ou do CSV-fonte, no caso das figuras).

Reaproveita, sem reescrever: a fatorial (`rodar_cenario`), os pesos (`fa.pesos_indice`),
o índice, as faixas, a elegibilidade e as AUC de `scripts/ivs_especificacoes.py` e o
rastreio da renda de `src/ivs_censo/renda.py`.
"""
import json
import sqlite3
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'src', RAIZ / 'scripts'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from ivs_censo.fatorial import reparticao, rodar_cenario  # noqa: E402
from ivs_censo.indicadores import POP_60MAIS  # noqa: E402
from ivs_censo.renda import rastrear_outliers_renda  # noqa: E402
import fatorial_ampliada as fa  # noqa: E402
import ivs_especificacoes as ie  # noqa: E402

BANCO = RAIZ / 'banco_de_dados'
QUADRO = BANCO / 'entrega_orientadora' / 'Quadro_Indicadores.csv'
REF_SETOR = BANCO / 'eda' / 'ivs_especificacoes' / 'ivs_referencia_por_setor.csv'
MODELOS = RAIZ / 'analises_exploratorias' / '_modelos' / 'textos_blocos.json'

TINTA, PETROLEO, ARGILA, CINZA = '#1A1A1A', '#1F4E4A', '#A83A2C', '#666666'
REGIOES = {'1': 'Norte', '2': 'Nordeste', '3': 'Sudeste', '4': 'Sul', '5': 'Centro-Oeste'}
CORES_REGIAO = {'Norte': PETROLEO, 'Nordeste': ARGILA, 'Sudeste': TINTA, 'Sul': CINZA,
                'Centro-Oeste': '#8A9A5B'}
CORES_FAIXA = ['#D9D9D9', '#8FB3AE', '#C9826F', ARGILA]
DIVERGENTE = LinearSegmentedColormap.from_list('ivs', [PETROLEO, '#FFFFFF', ARGILA])
SEQUENCIAL = LinearSegmentedColormap.from_list('ivs_seq', ['#FFFFFF', ARGILA])
DIMS = ['Saneamento', 'Socioeconômica', 'Morfologia', 'Demografia']
EXTRAS = {'renda_media_sem_extremo': 'Socioeconômica', 'renda_media_mediana_mun': 'Socioeconômica',
          'banheiro_graduado': 'Saneamento'}
ROT = {
    'pct_agua_inad': 'Água inadequada', 'pct_esgoto_inad': 'Esgoto inadequado',
    'pct_lixo_inad': 'Lixo inadequado', 'razao_moradores': 'Razão de moradores',
    'pct_analfab': 'Analfabetismo 15+', 'renda_media': 'Renda média',
    'renda_inv': 'Renda (invertida)', 'pct_raca_pretpardind': 'Cor/raça PPI',
    'pct_dom_improv': 'Domicílio improvisado', 'pct_hab_precaria': 'Habitação precária',
    'pct_moradia_convencional': 'Moradia convencional',
    'pct_moradia_nao_convencional': 'Moradia não convencional',
    'pct_apartamento': 'Apartamento', 'pct_casa': 'Casa',
    'pct_casa_vila_condominio': 'Casa de vila/condomínio',
    'pct_sem_agua_canalizada': 'Sem água canalizada', 'pct_agua_nao_encanada': 'Água não chega',
    'pct_agua_so_terreno': 'Água só no terreno', 'pct_sem_banheiro': 'Sem banheiro',
    'pct_sem_banheiro_nem_sanitario': 'Sem banheiro nem sanitário',
    'pct_so_sanitario': 'Só sanitário', 'pct_banheiro_comum': 'Banheiro de uso comum',
    'pct_resp_feminino': 'Responsável mulher', 'pct_crianca_0a4': 'Crianças 0–4',
    'pct_pop_0a14': 'População 0–14', 'pct_idoso_60mais': 'Pessoas 60+',
    'iep_setor': 'Índice de envelhecimento', 'rdi_setor': 'Dependência idosa',
    'prop_70mais_entre_60mais': '70+ entre 60+',
    'renda_media_sem_extremo': 'Renda sem o extremo',
    'renda_media_mediana_mun': 'Renda (mediana mun.)', 'banheiro_graduado': 'Banheiro graduado',
}
ie.ROT.update({c: r for c, r in ROT.items() if c not in ie.ROT})
ENVELHECIMENTO = ['pct_idoso_60mais', 'iep_setor', 'rdi_setor', 'prop_70mais_entre_60mais']
IDADES = [('V01031', '0–4'), ('V01032', '5–9'), ('V01033', '10–14'), ('V01034', '15–19'),
          ('V01035', '20–24'), ('V01036', '25–29'), ('V01037', '30–39'), ('V01038', '40–49'),
          ('V01039', '50–59'), ('V01040', '60–69'), ('V01041', '70+')]
TEXTO = {'CD_SETOR', 'SITUACAO', 'NM_MUN', 'NM_BAIRRO', 'CD_FCU', 'NM_FCU', 'Dados_sig', 'UF',
         'Moradia_Predominante', 'Moradia_Predominante_Agrupada'}
K = 3.0          # Tukey "extremo", o mesmo k da renda (src/ivs_censo/renda.py)
LIMIAR_PAR = 0.80
DESLOCAMENTO = 0.01   # média geométrica: soma-se 0,01 aos componentes (zero anularia o produto)

PADRAO = {
    'versao': '', 'titulo': '', 'pergunta': '',
    'base': 'entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db',
    'recorte': {'urbano': True, 'dados_sig': 'OK', 'piso_pop': None, 'municipios': None,
                'regioes': None, 'porte': None},
    'indicadores': 'todos',
    'indice': {'colunas': None, 'renda': 'original', 'rotacao': 'promax', 'metodo': '60_40',
               'normalizacao': 'municipal'},
    'blocos': list(range(1, 14)),
}


# ── Formatação pt-BR (o que vai para os campos; o verificador lê de volta) ─────
def br(v, d=4):
    if v is None or (isinstance(v, (float, np.floating)) and np.isnan(v)):
        return '—'
    return f'{float(v):,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def intbr(v):
    return br(v, 0)


def pctbr(v, d=1):
    return '—' if br(v, d) == '—' else br(v, d) + '%'


def dec(ind):
    return 2 if ind.startswith('renda') else 4


# ── Configuração e base ────────────────────────────────────────────────────────
def ler_config(pasta) -> dict:
    cfg = json.loads((Path(pasta) / 'config.json').read_text(encoding='utf-8'))
    out = {**PADRAO, **cfg}
    out['recorte'] = {**PADRAO['recorte'], **cfg.get('recorte', {})}
    if out['indice'] is not None:
        out['indice'] = {**PADRAO['indice'], **(cfg.get('indice') or {})}
        if not out['indice']['colunas']:
            out['indice']['colunas'] = fa._sem_lixo(fa.IVS7_INV) + ['banheiro_graduado']
    return out


def dimensoes() -> dict:
    q = pd.read_csv(QUADRO, sep=';', encoding='utf-8-sig')
    dim = {**dict(zip(q['indicador'], q['dimensao'])), **EXTRAS}
    return {c: dim[c] for d in DIMS for c in dim if dim[c] == d}


def montar_base(cfg: dict) -> SimpleNamespace:
    con = sqlite3.connect(f"file:{BANCO / cfg['base']}?mode=ro", uri=True)
    df = pd.read_sql('SELECT * FROM setores_censitarios', con)
    con.close()
    for c in df.columns:
        if c not in TEXTO:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.copy()
    df['CD_SETOR'] = df['CD_SETOR'].astype(str)
    df['regiao'] = df['CD_UF'].astype('Int64').astype(str).str[0].map(REGIOES)
    df['banheiro_graduado'] = ie.banheiro_graduado(df)
    # indicadores fora da base (config `indicadores_externos`): numerador por setor num CSV
    # já gravado, sobre um denominador da base
    for e in cfg.get('indicadores_externos', []):
        x = pd.read_csv(BANCO / e['arquivo'], sep=e.get('sep', ','), encoding='utf-8-sig', dtype={'CD_SETOR': str})
        df = df.merge(x[['CD_SETOR', e['numerador']]], on='CD_SETOR', how='left', validate='one_to_one')
        df[e['nome']] = df[e['numerador']] / df[e['denominador']].where(df[e['denominador']] > 0)
        ROT[e['nome']] = ie.ROT[e['nome']] = e['rotulo']
    renda = (cfg['indice'] or {}).get('renda', 'original')
    df['renda_inv'] = -df[fa.RENDAS[renda]]
    df['pop_60mais'] = df[POP_60MAIS].sum(axis=1, min_count=1)
    # porte = moradores do município somados em todos os setores da base, antes de qualquer filtro
    df['pop_municipio'] = df.groupby('NM_MUN')['v0001'].transform('sum')
    rc, funil = cfg['recorte'], [('Base completa', len(df), '')]
    if rc['urbano']:
        df = df[df['urbano'] == 1]
        funil.append(('Setores urbanos', len(df), 'setor rural'))
    if rc['dados_sig']:
        df = df[df['Dados_sig'] == rc['dados_sig']]
        funil.append((f"Dados_sig = {rc['dados_sig']}", len(df),
                      'setor sem dados divulgados (sigilo ou sem domicílio ocupado)'))
    if rc['piso_pop']:
        df = df[df['v0001'] >= rc['piso_pop']]
        funil.append((f"Pelo menos {rc['piso_pop']} moradores", len(df), 'abaixo do piso de população'))
    if rc.get('regioes'):
        df = df[df['regiao'].isin(rc['regioes'])]
        funil.append(('Região: ' + ', '.join(rc['regioes']), len(df), 'fora da região da versão'))
    if rc.get('porte'):
        lo, hi = rc['porte']
        df = df[(df['pop_municipio'] > lo) & ((hi is None) | (df['pop_municipio'] <= (hi or 0)))]
        funil.append(('Porte do município', len(df), 'município fora da faixa de porte'))
    if rc['municipios']:
        df = df[df['NM_MUN'].isin(rc['municipios'])]
        funil.append(('Municípios da versão', len(df), 'fora dos municípios da versão'))
    # indicadores compostos (config `indicadores_derivados`): média simples de colunas da base
    for e in cfg.get('indicadores_derivados', []):
        df[e['nome']] = df[e['media_de']].mean(axis=1, skipna=False)
        ROT[e['nome']] = ie.ROT[e['nome']] = e['rotulo']
    extras = cfg.get('indicadores_externos', []) + cfg.get('indicadores_derivados', [])
    dim = {**dimensoes(), **{e['nome']: e['dimensao'] for e in extras}}
    inds = list(dim) if cfg['indicadores'] == 'todos' else list(cfg['indicadores'])
    # tabelas "por município" dos blocos 2, 4 e 5: no Brasil (A6) agrupam por UF
    return SimpleNamespace(df=df.reset_index(drop=True), funil=funil, inds=inds, dim=dim,
                           grupo=cfg.get('grupo_descritivo', 'NM_MUN'))


def calcular_indice(df: pd.DataFrame, cfg: dict) -> SimpleNamespace:
    """O índice da versão com as funções do NB05; exclusão por lista nos componentes."""
    ic = cfg['indice']
    col = list(ic['colunas'])
    k = ic.get('k', 2)
    d = df.dropna(subset=col).reset_index(drop=True)
    r = rodar_cenario(d[col].to_numpy(), k=k, extracao=ic.get('extracao', 'acp'))
    if k == 2 and 'renda_inv' in col:
        M, rep = ie.reparticoes(r, col)[(ic['rotacao'], ic['metodo'])]
    else:
        # sem renda ou com k ≠ 2 não há "dimensão socioeconômica" para a regra 60/40:
        # o peso de cada fator vem da soma dos quadrados das cargas (pesos pela fatorial)
        M = {'sem_rotacao': r['sem_rotacao'], 'varimax': r['varimax'], 'promax': r['promax_padrao']}[ic['rotacao']]
        rep = reparticao(M)
    w = fa.pesos_indice(M, rep)
    if ic.get('pesos') == 'iguais':
        w = np.full(len(col), 1 / len(col))
    if ic.get('subindice'):
        dim = np.abs(M).argmax(axis=1)
        fr = ie.fator_renda(M, col)
        manter = (dim == fr) if ic['subindice'] == 'socioeconomico' else (dim != fr)
        w = np.where(manter, w, 0.0)
        w = w / w.sum()
    v = indice_versao(d, col, w, ic['normalizacao'], ic.get('agregacao', 'soma'))
    s = d[['CD_SETOR', 'NM_MUN', 'regiao', 'is_fcu', 'v0001', 'pop_60mais']].copy()
    s['ivs'] = v
    for regra in ('ivs_bh', 'quartis'):
        s[f'faixa_{regra}'] = ie.faixas(v, d['NM_MUN'], regra)
    return SimpleNamespace(d=d, col=col, r=r, M=M, rep=rep, w=w, setores=s,
                           eleg=ie.elegibilidade(r, ic['rotacao'], col),
                           auc=fa.auc_postos(v, d['is_fcu']),
                           auc_mun=ie.auc_municipal(v, d['is_fcu'], d['NM_MUN']))


def rho(a: pd.Series, b: pd.Series) -> float:
    """Spearman de dois vetores, nos pares completos (sem scipy: Pearson dos postos)."""
    m = a.notna() & b.notna()
    return float(a[m].rank().corr(b[m].rank())) if m.sum() > 2 else np.nan


def indice_versao(d, col, w, normalizacao, agregacao='soma') -> np.ndarray:
    """O índice: `ie.indice` (min-max municipal ou global, soma ponderada, como o NB05) ou,
    nas versões do eixo C, escore z, postos percentis no município e média geométrica."""
    if normalizacao in ('municipal', 'global') and agregacao == 'soma':
        return ie.indice(d, col, w, normalizacao)
    X, g = d[col], d['NM_MUN']
    if normalizacao == 'municipal':
        lo, hi = X.groupby(g).transform('min'), X.groupby(g).transform('max')
        Z = (X - lo) / (hi - lo)
    elif normalizacao == 'global':
        Z = (X - X.min()) / (X.max() - X.min())
    elif normalizacao == 'z_municipal':
        Z = (X - X.groupby(g).transform('mean')) / X.groupby(g).transform('std')
    elif normalizacao == 'z_global':
        Z = (X - X.mean()) / X.std()
    elif normalizacao == 'postos_municipal':
        Z = X.groupby(g).rank(pct=True)
    else:
        raise ValueError(f'normalização desconhecida: {normalizacao}')
    # componente constante no município (máx = mín, ou DP zero) vira 0, como na soma do
    # `ie.indice`; sem isso, a média geométrica pularia o NaN e o contaria como carência máxima
    Z = Z.fillna(0)
    if agregacao == 'geometrica':
        return np.exp((np.log(Z + DESLOCAMENTO) * w).sum(axis=1) / w.sum()).to_numpy()
    return (Z * w).sum(axis=1).to_numpy()


def kmedias(X, k, semente=42, n_init=5, iter_max=300):
    """k-médias (Lloyd, início k-means++) sem scikit-learn: rótulos e inércia."""
    X = np.asarray(X, dtype=float)
    rng = np.random.default_rng(semente)
    melhor = None
    for _ in range(n_init):
        c = X[rng.integers(len(X))][None, :]
        while len(c) < k:
            d2 = ((X[:, None, :] - c[None, :, :]) ** 2).sum(-1).min(axis=1)
            c = np.vstack([c, X[rng.choice(len(X), p=d2 / d2.sum())]])
        for _ in range(iter_max):
            rot = ((X[:, None, :] - c[None, :, :]) ** 2).sum(-1).argmin(axis=1)
            novo = np.array([X[rot == j].mean(axis=0) if (rot == j).any() else c[j] for j in range(k)])
            if np.allclose(novo, c):
                break
            c = novo
        inercia = float(((X - c[rot]) ** 2).sum())
        if melhor is None or inercia < melhor[1]:
            melhor = (rot, inercia, c)
    return melhor


def silhueta(X, rot, amostra=5000, semente=42) -> float:
    """Silhueta média numa amostra de setores (a conta inteira é quadrática no n)."""
    X, rot = np.asarray(X, dtype=float), np.asarray(rot)
    rng = np.random.default_rng(semente)
    i = rng.choice(len(X), size=min(amostra, len(X)), replace=False)
    X, rot = X[i], rot[i]
    q = (X ** 2).sum(axis=1)
    D = np.sqrt(np.maximum(q[:, None] + q[None, :] - 2 * X @ X.T, 0))
    s = []
    for j in range(len(X)):
        mesmo = rot == rot[j]
        if mesmo.sum() < 2:
            s.append(0.0)
            continue
        a = D[j, mesmo].sum() / (mesmo.sum() - 1)
        b = min(D[j, rot == g].mean() for g in np.unique(rot) if g != rot[j])
        s.append((b - a) / max(a, b))
    return float(np.mean(s))


def ordenar_grupos(rot, valor):
    """Renumera os grupos de 0 a k−1 pela média de `valor` (0 = menor)."""
    ordem = pd.Series(valor).groupby(rot).mean().sort_values().index
    return pd.Series(rot).map({g: i for i, g in enumerate(ordem)}).to_numpy()


def descritivas(s: pd.Series) -> dict:
    s = s.dropna()
    q = s.quantile([.1, .25, .5, .75, .9]) if len(s) else pd.Series(np.nan, index=[.1, .25, .5, .75, .9])
    m = s.mean()
    return {'n': len(s), 'media': m, 'dp': s.std(), 'cv_pct': s.std() / m * 100 if m else np.nan,
            'min': s.min(), 'p10': q[.1], 'p25': q[.25], 'mediana': q[.5], 'p75': q[.75],
            'p90': q[.9], 'max': s.max(), 'iq': q[.75] - q[.25], 'assim': s.skew(),
            'curt': s.kurtosis(), 'pct_zeros': 100 * (s == 0).mean() if len(s) else np.nan}


def tab_desc(df, inds, por=None) -> pd.DataFrame:
    if por is None:
        return pd.DataFrame([{'indicador': c, 'rotulo': ROT[c], **descritivas(df[c])} for c in inds])
    return pd.DataFrame([{por: g, 'indicador': c, 'rotulo': ROT[c], **descritivas(x[c])}
                         for g, x in df.groupby(por) for c in inds])


def extremos_grupo(t, grupo, ind, col='mediana') -> dict:
    x = t[t['indicador'] == ind].dropna(subset=[col])
    a, z = x.loc[x[col].idxmax()], x.loc[x[col].idxmin()]
    return {'ind': ROT[ind], 'grupo_max': a[grupo], 'val_max': br(a[col], dec(ind)),
            'grupo_min': z[grupo], 'val_min': br(z[col], dec(ind))}


def maior_par(C: pd.DataFrame) -> dict:
    A = C.abs().to_numpy().copy()
    np.fill_diagonal(A, -1)
    if A.size < 4 or np.all(np.isnan(A) | (A < 0)):
        return {'par_a': '—', 'par_b': '—', 'rho': '—'}
    i, j = np.unravel_index(np.nanargmax(A), A.shape)
    return {'par_a': ROT[C.index[i]], 'par_b': ROT[C.columns[j]], 'rho': br(C.iat[i, j], 4)}


# ── Saída: tabelas, figuras e catálogo ─────────────────────────────────────────
class _Seguro(dict):
    def __missing__(self, k):
        return '{' + k + '}'


class Saida:
    def __init__(self, pasta: Path, textos: dict):
        self.pasta, self.itens, self.linhas, self.avisos = pasta, textos['itens'], [], []
        for sub, ext in (('tabelas', 'csv'), ('figuras', 'png')):
            (pasta / sub).mkdir(parents=True, exist_ok=True)
            for f in (pasta / sub).glob(f'*.{ext}'):
                f.unlink()

    def _linha(self, id_, tipo, bloco, chave, arq, fonte, campos):
        t = self.itens.get(chave, {})
        self.linhas.append({
            'id': id_, 'tipo': tipo, 'bloco': bloco, 'chave': chave,
            'titulo': t.get('titulo', id_).format_map(_Seguro(campos)),
            'o_que_mostra': t.get('o_que_mostra', '').format_map(_Seguro(campos)),
            'arquivo': arq, 'fonte': fonte, 'campos': json.dumps(campos, ensure_ascii=False),
            'slide': ''})

    def tabela(self, id_, nome, bloco, chave, df, campos, index=False):
        arq = f'tabelas/{id_}_{nome}.csv'
        df.to_csv(self.pasta / arq, index=index)
        self._linha(id_, 'tabela', bloco, chave, arq, id_, campos)

    def figura(self, id_, nome, bloco, chave, fig, fonte, campos):
        arq = f'figuras/{id_}_{nome}.png'
        fig.savefig(self.pasta / arq, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        self._linha(id_, 'figura', bloco, chave, arq, fonte, campos)

    def fechar(self):
        pd.DataFrame(self.linhas).to_csv(self.pasta / 'catalogo.csv', index=False)


def estilo(ax, xlabel='', ylabel=''):
    for lado in ('top', 'right'):
        ax.spines[lado].set_visible(False)
    ax.tick_params(colors=TINTA, labelsize=8)
    ax.set_xlabel(xlabel, color=TINTA, fontsize=9)
    ax.set_ylabel(ylabel, color=TINTA, fontsize=9)


def grade(n, w=3.2, h=2.4):
    nc = min(4, n)
    nr = -(-n // nc)
    fig, axs = plt.subplots(nr, nc, figsize=(w * nc, h * nr), squeeze=False)
    axs = list(axs.flat)
    for ax in axs[n:]:
        ax.set_visible(False)
    return fig, axs[:n]


def mapa_calor(ax, M, xl, yl, cmap, vmin, vmax, fs=6):
    im = ax.imshow(M, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto')
    ax.set_xticks(range(len(xl)), xl, rotation=90, fontsize=fs)
    ax.set_yticks(range(len(yl)), yl, fontsize=fs)
    plt.colorbar(im, ax=ax, fraction=0.03)


def regioes_presentes(df):
    return [r for r in REGIOES.values() if r in set(df['regiao'].dropna())]


# ── Bloco 1. Recorte ──────────────────────────────────────────────────────────
def bloco1(b, ix, S):
    linhas, ant = [], None
    for etapa, n, motivo in b.funil:
        linhas.append({'etapa': etapa, 'setores': n, 'saem': 0 if ant is None else ant - n,
                       'motivo_da_saida': motivo})
        ant = n
    if ix is not None:
        n = len(ix.d)
        linhas.append({'etapa': 'Componentes do índice completos', 'setores': n, 'saem': ant - n,
                       'motivo_da_saida': 'faltante em algum componente do índice (exclusão por lista)'})
    t = pd.DataFrame(linhas)
    c = {'n_base': intbr(t['setores'].iloc[0]), 'n_recorte': intbr(t['setores'].iloc[len(b.funil) - 1]),
         'n_indice': intbr(t['setores'].iloc[-1]), 'saem_indice': intbr(t['saem'].iloc[-1])}
    S.tabela('T01', 'funil', 1, 'funil_tab', t, c)
    fig, ax = plt.subplots(figsize=(9, 0.6 * len(t) + 1.2))
    ax.barh(range(len(t)), t['setores'], color=PETROLEO)
    ax.invert_yaxis()
    ax.set_yticks(range(len(t)), t['etapa'])
    for i, v in enumerate(t['setores']):
        ax.text(v, i, ' ' + intbr(v), va='center', fontsize=9, color=TINTA)
    estilo(ax, 'Setores censitários')
    S.figura('F01', 'funil', 1, 'funil_fig', fig, 'T01', c)

    df = b.df
    t = pd.DataFrame([{'indicador': i, 'rotulo': ROT[i], 'dimensao': b.dim.get(i, ''),
                       'n_validos': int(df[i].notna().sum()), 'n_faltantes': int(df[i].isna().sum()),
                       'pct_faltantes': 100 * df[i].isna().mean()} for i in b.inds])
    mx, mn = t.loc[t['pct_faltantes'].idxmax()], t.loc[t['pct_faltantes'].idxmin()]
    S.tabela('T02', 'perdas_por_indicador', 1, 'perdas', t,
             {'ind_max': mx['rotulo'], 'pct_max': pctbr(mx['pct_faltantes']),
              'ind_min': mn['rotulo'], 'pct_min': pctbr(mn['pct_faltantes'])})


# ── Bloco 2. Descritivas ───────────────────────────────────────────────────────
def bloco2(b, ix, S):
    df, inds = b.df, b.inds
    foco = 'renda_media' if 'renda_media' in inds else inds[0]
    t = tab_desc(df, inds)
    a, z = t.loc[t['assim'].idxmax()], t.loc[t['pct_zeros'].idxmax()]
    S.tabela('T03', 'descritivas_global', 2, 'desc_global', t,
             {'ind_assim': a['rotulo'], 'assim_max': br(a['assim'], 2),
              'ind_zeros': z['rotulo'], 'pct_zeros': pctbr(z['pct_zeros'])})
    b.t03 = t
    t = tab_desc(df, inds, 'regiao')
    b.t04 = t
    S.tabela('T04', 'descritivas_regiao', 2, 'desc_regiao', t, extremos_grupo(t, 'regiao', foco))
    t = tab_desc(df, inds, b.grupo)
    S.tabela('T05', 'descritivas_municipio', 2, 'desc_municipio', t, extremos_grupo(t, b.grupo, foco))
    if b.cfg.get('comparar_com_70'):
        brasil_x_70(b, S)


def brasil_x_70(b, S):
    """T35: cada indicador no recorte da versão e nos setores dele que estão no recorte dos
    70 municípios (urbanos, Dados_sig = OK), lado a lado."""
    con = sqlite3.connect(f"file:{BANCO / PADRAO['base']}?mode=ro", uri=True)
    elsi = pd.read_sql("SELECT CD_SETOR FROM setores_censitarios WHERE urbano = 1 AND Dados_sig = 'OK'", con)
    con.close()
    dentro = b.df['CD_SETOR'].isin(set(elsi['CD_SETOR'].astype(str)))
    linhas = []
    for c in b.inds:
        x, y = descritivas(b.df[c]), descritivas(b.df.loc[dentro, c])
        linhas.append({'indicador': c, 'rotulo': ROT[c], 'n_versao': x['n'], 'mediana_versao': x['mediana'],
                       'media_versao': x['media'], 'n_70': y['n'], 'mediana_70': y['mediana'], 'media_70': y['media'],
                       'diferenca_media': y['media'] - x['media']})
    t = pd.DataFrame(linhas)
    t['dif_abs'] = (t['diferenca_media'] / t['media_versao']).abs()
    a = t.loc[t['dif_abs'].idxmax()]
    t = t.drop(columns='dif_abs')
    d = dec(a['indicador'])
    S.tabela('T35', 'versao_x_70_municipios', 2, 'brasil_x_70', t,
             {'n_versao': intbr(t['n_versao'].max()), 'n_70': intbr(t['n_70'].max()), 'ind': a['rotulo'],
              'media_versao': br(a['media_versao'], d), 'media_70': br(a['media_70'], d)})


# ── Bloco 3. Distribuições ─────────────────────────────────────────────────────
def bloco3(b, ix, S):
    df = b.df
    t03 = b.t03 if hasattr(b, 't03') else tab_desc(df, b.inds)
    t04 = b.t04 if hasattr(b, 't04') else tab_desc(df, b.inds, 'regiao')
    regs = regioes_presentes(df)
    for k, dim in enumerate(DIMS):
        cols = [c for c in b.inds if b.dim.get(c) == dim]
        if not cols:
            continue
        slug = dim.lower().replace('ô', 'o')
        ids = [f'F{2 + 3 * k:02d}', f'F{3 + 3 * k:02d}', f'F{4 + 3 * k:02d}']
        x = t03[t03['indicador'].isin(cols)]
        a = x.loc[x['assim'].idxmax()]
        fig, axs = grade(len(cols))
        for ax, c in zip(axs, cols):
            s = df[c].dropna()
            s = s[s <= s.quantile(.995)]
            ax.hist(s, bins=50, color=PETROLEO)
            ax.set_title(ROT[c], fontsize=9, color=TINTA)
            estilo(ax)
        fig.tight_layout()
        S.figura(ids[0], f'histogramas_{slug}', 3, 'hist', fig, 'T03',
                 {'dim': dim, 'ind': a['rotulo'], 'assim': br(a['assim'], 2)})
        cr = {'dim': dim, **extremos_grupo(t04, 'regiao', cols[0])}
        fig, axs = grade(len(cols))
        for ax, c in zip(axs, cols):
            ax.boxplot([df.loc[df['regiao'] == r, c].dropna() for r in regs], showfliers=False,
                       medianprops={'color': ARGILA})
            ax.set_xticks(range(1, len(regs) + 1), [r[:2] for r in regs])
            ax.set_title(ROT[c], fontsize=9, color=TINTA)
            estilo(ax)
        fig.tight_layout()
        S.figura(ids[1], f'boxplots_regiao_{slug}', 3, 'box', fig, 'T04', cr)
        fig, axs = grade(len(cols))
        for ax, c in zip(axs, cols):
            s = df[c].dropna()
            lo, hi = s.quantile(.005), s.quantile(.995)
            if hi <= lo:
                hi = lo + 1
            for r in regs:
                h, e = np.histogram(df.loc[df['regiao'] == r, c].dropna(), bins=60, range=(lo, hi), density=True)
                ax.plot((e[1:] + e[:-1]) / 2, np.convolve(h, np.ones(3) / 3, mode='same'),
                        color=CORES_REGIAO[r], lw=1.2, label=r)
            ax.set_title(ROT[c], fontsize=9, color=TINTA)
            estilo(ax)
        axs[0].legend(fontsize=6, frameon=False)
        fig.tight_layout()
        S.figura(ids[2], f'densidades_regiao_{slug}', 3, 'dens', fig, 'T04', cr)


# ── Bloco 4. Faltantes e sigilo ────────────────────────────────────────────────
def bloco4(b, ix, S):
    df, inds = b.df, b.inds
    f = (df[inds].isna().groupby(df[b.grupo]).mean() * 100)
    pilha = f.stack()
    mun, ind = pilha.idxmax()
    c = {'mun_max': mun, 'ind_max': ROT[ind], 'pct_max': pctbr(pilha.max())}
    S.tabela('T06', 'faltantes_por_municipio', 4, 'falt_municipio', f.reset_index(), c)
    fig, ax = plt.subplots(figsize=(12, 14))
    mapa_calor(ax, f.to_numpy(), [ROT[i] for i in f.columns], list(f.index), SEQUENCIAL, 0, 100)
    S.figura('F14', 'mapa_faltantes', 4, 'falt_mapa', fig, 'T06', c)

    decil = pd.qcut(df['v0001'].rank(method='first'), 10, labels=range(1, 11))
    t = df.groupby(decil, observed=True).agg(
        setores=('CD_SETOR', 'size'), moradores_min=('v0001', 'min'), moradores_max=('v0001', 'max'),
        pct_falt_renda=('renda_media', lambda s: 100 * s.isna().mean()),
        pct_falt_analfab=('pct_analfab', lambda s: 100 * s.isna().mean()),
        pct_fcu=('is_fcu', lambda s: 100 * s.fillna(0).mean())).reset_index(names='decil_moradores')
    c = {'renda_d1': pctbr(t['pct_falt_renda'].iloc[0]), 'renda_d10': pctbr(t['pct_falt_renda'].iloc[-1]),
         'analf_d1': pctbr(t['pct_falt_analfab'].iloc[0]), 'analf_d10': pctbr(t['pct_falt_analfab'].iloc[-1])}
    S.tabela('T07', 'sigilo_por_porte_do_setor', 4, 'sigilo_porte_tab', t, c)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t['decil_moradores'].astype(int), t['pct_falt_renda'], 'o-', color=ARGILA, label='Renda média')
    ax.plot(t['decil_moradores'].astype(int), t['pct_falt_analfab'], 's-', color=PETROLEO, label='Analfabetismo 15+')
    ax.set_xticks(range(1, 11))
    ax.legend(frameon=False, fontsize=8)
    estilo(ax, 'Décimo de moradores do setor (1 = menores)', '% de setores com faltante')
    S.figura('F15', 'sigilo_por_porte_do_setor', 4, 'sigilo_porte_fig', fig, 'T07', c)


# ── Bloco 5. Extremos ──────────────────────────────────────────────────────────
def bloco5(b, ix, S):
    df, inds = b.df, b.inds
    marcas, crit, classes = {}, [], None
    for c in inds:
        s = df[c]
        v = s.dropna()
        q1, q3 = v.quantile([.25, .75])
        iq = q3 - q1
        li = ls = np.nan
        if c == 'renda_media':
            rs = rastrear_outliers_renda(df)
            classes = rs['classe_renda'][s.notna()]
            fl = rs['classe_renda'].ne('NORMAL') & s.notna()
            criterio = 'renda: Tukey k=3 no município + coerência do perfil do setor'
        elif v.median() == 0 or iq == 0:
            nz = v[v > 0]
            if len(nz):
                a, z = nz.quantile([.25, .75])
                ls = z + K * (z - a)
            fl = s > ls
            criterio = 'inflação de zeros: Tukey k=3 só entre os valores acima de zero'
        else:
            li, ls = q1 - K * iq, q3 + K * iq
            fl = (s < li) | (s > ls)
            criterio = 'Tukey k=3 (intervalo interquartil)'
        marcas[c] = fl.fillna(False).astype(bool)
        crit.append({'indicador': c, 'rotulo': ROT[c], 'criterio': criterio, 'limite_inferior': li,
                     'limite_superior': ls, 'n_validos': len(v), 'pct_zeros': 100 * (v == 0).mean(),
                     'n_extremos': int(marcas[c].sum()), 'pct_extremos': 100 * marcas[c].sum() / max(len(v), 1)})
    t = pd.DataFrame(crit)
    mx = t.loc[t['pct_extremos'].idxmax()]
    c8 = {'ind_max': mx['rotulo'], 'pct_max': pctbr(mx['pct_extremos']), 'criterio': mx['criterio']}
    S.tabela('T08', 'extremos_por_indicador', 5, 'extremos_criterio', t, c8)

    m = pd.DataFrame(marcas).groupby(df[b.grupo]).sum()
    m['total'] = m.sum(axis=1)
    m = m.sort_values('total', ascending=False).reset_index()
    S.tabela('T09', 'extremos_por_municipio', 5, 'extremos_municipio', m,
             {'mun_max': m[b.grupo].iloc[0], 'n_max': intbr(m['total'].iloc[0])})

    lista = []
    for c in inds:
        x = df.loc[marcas[c], ['CD_SETOR', 'NM_MUN', c]].copy()
        x['distancia'] = (x[c] - df[c].median()).abs()
        for _, r in x.nlargest(10, 'distancia').iterrows():
            lista.append({'indicador': c, 'rotulo': ROT[c], 'CD_SETOR': r['CD_SETOR'],
                          'NM_MUN': r['NM_MUN'], 'valor': r[c], 'mediana_global': df[c].median()})
    t = pd.DataFrame(lista, columns=['indicador', 'rotulo', 'CD_SETOR', 'NM_MUN', 'valor', 'mediana_global'])
    foco = t[t['indicador'] == 'renda_media'] if (t['indicador'] == 'renda_media').any() else t
    c = ({'ind': foco['rotulo'].iloc[0], 'mun': foco['NM_MUN'].iloc[0],
          'valor': br(foco['valor'].iloc[0], dec(foco['indicador'].iloc[0]))} if len(foco)
         else {'ind': '—', 'mun': '—', 'valor': '—'})
    S.tabela('T10', 'extremos_lista', 5, 'extremos_lista', t, c)

    if classes is not None:
        t = classes.value_counts().rename_axis('classe').reset_index(name='setores')
        t['pct'] = 100 * t['setores'] / t['setores'].sum()
        g = t.set_index('classe')
        S.tabela('T11', 'renda_classes', 5, 'renda_classes', t,
                 {'n_suspeito': intbr(g['setores'].get('SUSPEITO', 0)),
                  'n_extremo': intbr(g['setores'].get('EXTREMO', 0)),
                  'pct_suspeito': pctbr(g['pct'].get('SUSPEITO', 0), 2)})
    else:
        S.avisos.append('T11 não gerada: a renda média não está na versão')

    t = pd.DataFrame(crit).sort_values('pct_extremos')
    cor = [ARGILA if x.startswith('renda') else (CINZA if x.startswith('inflação') else PETROLEO)
           for x in t['criterio']]
    fig, ax = plt.subplots(figsize=(8, 0.28 * len(t) + 1))
    ax.barh(t['rotulo'], t['pct_extremos'], color=cor)
    estilo(ax, '% de setores marcados como extremo')
    S.figura('F16', 'extremos_por_indicador', 5, 'extremos_fig', fig, 'T08', c8)


# ── Bloco 6. Correlações ───────────────────────────────────────────────────────
def agrupar(D):
    """Agrupamento hierárquico por ligação média (sem scipy): uniões e ordem das folhas."""
    grupos, uniao, prox = {i: [i] for i in range(len(D))}, [], len(D)
    while len(grupos) > 1:
        ks = list(grupos)
        d, a, z = min((D[np.ix_(grupos[a], grupos[z])].mean(), a, z)
                      for i, a in enumerate(ks) for z in ks[i + 1:])
        grupos[prox] = grupos.pop(a) + grupos.pop(z)
        uniao.append((a, z, d, prox))
        prox += 1
    return uniao, grupos[prox - 1]


# famílias de variantes: um par dentro da mesma família não é achado (mede a mesma coisa)
FAMILIAS = {'agua': ['pct_agua_inad', 'pct_agua_nao_encanada', 'pct_sem_agua_canalizada', 'pct_agua_so_terreno'],
            'banheiro': ['banheiro_graduado', 'pct_sem_banheiro', 'pct_sem_banheiro_nem_sanitario', 'pct_so_sanitario',
                         'pct_banheiro_comum'],
            'renda': ['renda_media', 'renda_media_sem_extremo', 'renda_media_mediana_mun'],
            'moradia': ['pct_moradia_nao_convencional', 'pct_hab_precaria', 'pct_moradia_convencional']}
FAMILIA = {c: f for f, cs in FAMILIAS.items() for c in cs}
DEMANDAS = ['pct_lixo_inad', 'pct_agua_nao_encanada', 'pct_sem_agua_canalizada', 'pct_agua_so_terreno',
            'pct_sem_banheiro', 'pct_moradia_nao_convencional']   # as variáveis das demandas de setembro


def mapa_correlacao(C: pd.DataFrame, ordem, separador=None, tam=None):
    """Matriz de correlação com o valor de ρ escrito em cada célula do triângulo inferior
    (o superior repete o inferior e fica em branco), na paleta divergente do projeto."""
    n = len(ordem)
    M = C.loc[ordem, ordem].to_numpy(dtype=float)
    vis = np.where(np.tril(np.ones((n, n), dtype=bool)), M, np.nan)
    lado = tam or max(6.0, 0.42 * n + 2)
    fig, ax = plt.subplots(figsize=(lado + 1.2, lado))
    im = ax.imshow(vis, cmap=DIVERGENTE, vmin=-1, vmax=1)
    fs = 10 if n <= 12 else (8 if n <= 18 else 6)
    for i in range(n):
        for j in range(i + 1):
            v = M[i, j]
            if not np.isnan(v):
                ax.text(j, i, f'{v:.2f}'.replace('.', ',').replace('-', '−'), ha='center', va='center', fontsize=fs,
                        color='white' if abs(v) >= 0.6 else TINTA)
    rot = [ROT[c] for c in ordem]
    ax.set_xticks(range(n), rot, rotation=60, ha='right', fontsize=fs + 1)
    ax.set_yticks(range(n), rot, fontsize=fs + 1)
    for lado_ in ('top', 'right'):
        ax.spines[lado_].set_visible(False)
    if separador:      # só no triângulo com valores: separa componentes e variáveis novas
        c = separador - 0.5
        ax.plot([-0.5, c], [c, c], color=TINTA, lw=1.5)
        ax.plot([c, c], [c, n - 0.5], color=TINTA, lw=1.5)
    cb = plt.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label('ρ de Spearman', fontsize=fs + 1)
    fig.tight_layout()
    return fig


def bloco6(b, ix, S):
    X = b.df[b.inds]
    sp, pe = X.corr(method='spearman'), X.corr()
    cs = maior_par(sp)
    S.tabela('T12', 'correlacao_spearman', 6, 'spearman', sp, cs, index=True)
    S.tabela('T13', 'correlacao_pearson', 6, 'pearson', pe, maior_par(pe), index=True)
    pares = [{'a': b.inds[i], 'b': b.inds[j], 'rotulo_a': ROT[b.inds[i]], 'rotulo_b': ROT[b.inds[j]],
              'spearman': sp.iat[i, j], 'pearson': pe.iat[i, j]}
             for i in range(len(b.inds)) for j in range(i + 1, len(b.inds))
             if max(abs(sp.iat[i, j]), abs(pe.iat[i, j])) >= LIMIAR_PAR]
    t = pd.DataFrame(pares, columns=['a', 'b', 'rotulo_a', 'rotulo_b', 'spearman', 'pearson'])
    t = t.reindex(t['spearman'].abs().sort_values(ascending=False).index)
    c = ({'par_a': t['rotulo_a'].iloc[0], 'par_b': t['rotulo_b'].iloc[0],
          'rho_s': br(t['spearman'].iloc[0]), 'rho_p': br(t['pearson'].iloc[0])} if len(t)
         else {'par_a': '—', 'par_b': '—', 'rho_s': '—', 'rho_p': '—'})
    S.tabela('T14', 'pares_acima_de_080', 6, 'pares', t, c)
    if len(b.inds) < 2:
        return
    uniao, ordem = agrupar(np.nan_to_num(1 - sp.abs().to_numpy(), nan=1.0))
    rot = [ROT[b.inds[i]] for i in ordem]
    S.figura('F17', 'mapa_spearman', 6, 'mapa_spearman', mapa_correlacao(sp, [b.inds[i] for i in ordem]), 'T12', cs)
    if ix is not None:
        comp = [c if c != 'renda_inv' else 'renda_media' for c in ix.col]
        foco = [c for c in comp if c in b.inds]
        novas = [c for c in DEMANDAS if c in b.inds and c not in foco]
        if len(foco) + len(novas) >= 3:
            # destaque: o par mais forte entre uma variável nova e um componente, de famílias diferentes
            pares = [(abs(sp.at[a, c]), a, c) for a in novas for c in foco if FAMILIA.get(a, a) != FAMILIA.get(c, c)]
            if pares:
                _, a, c = max(pares)
                cf = {'par_a': ROT[a], 'par_b': ROT[c], 'rho': br(sp.at[a, c])}
            else:
                cf = maior_par(sp.loc[foco, foco])
            S.figura('F31', 'mapa_spearman_componentes', 6, 'mapa_spearman_foco',
                     mapa_correlacao(sp, foco + novas, separador=len(foco) if novas else None), 'T12', cf)
    for k, dim in enumerate(DIMS):            # F32–F35: uma matriz por dimensão, legível no slide
        cols = [c for c in b.inds if b.dim.get(c) == dim]
        if len(cols) >= 3:
            sub = sp.loc[cols, cols]
            S.figura(f'F{32 + k}', f"mapa_spearman_{dim.lower().replace('ô', 'o')}", 6, 'mapa_spearman_dim',
                     mapa_correlacao(sp, cols), 'T12', {'dim': dim, **maior_par(sub)})
    fig, ax = plt.subplots(figsize=(8, 0.3 * len(ordem) + 1))
    pos, alt = {f: i for i, f in enumerate(ordem)}, {f: 0.0 for f in ordem}
    for a, z, d, k in uniao:
        ax.plot([alt[a], d, d, alt[z]], [pos[a], pos[a], pos[z], pos[z]], color=PETROLEO, lw=1)
        pos[k], alt[k] = (pos[a] + pos[z]) / 2, d
    ax.set_yticks(range(len(ordem)), rot)
    estilo(ax, 'Distância (1 − |ρ de Spearman|), ligação média')
    S.figura('F18', 'dendrograma', 6, 'dendrograma', fig, 'T12', cs)


# ── Bloco 7. Favelas (FCU) ─────────────────────────────────────────────────────
def bloco7(b, ix, S):
    df, y = b.df, b.df['is_fcu']
    if y.fillna(0).sum() == 0:
        S.avisos.append('Bloco 7 não gerado: nenhum setor de FCU no recorte')
        return
    linhas = []
    for c in b.inds:
        m = df[c].notna() & y.notna()
        s, yy = df.loc[m, c], y[m]
        linhas.append({'indicador': c, 'rotulo': ROT[c], 'n_fcu': int((yy == 1).sum()),
                       'n_nao_fcu': int((yy == 0).sum()), 'mediana_fcu': s[yy == 1].median(),
                       'mediana_nao_fcu': s[yy == 0].median(),
                       'diferenca': s[yy == 1].median() - s[yy == 0].median(),
                       'auc': fa.auc_postos(s, yy)})
    t = pd.DataFrame(linhas).sort_values('auc', ascending=False)
    a, z = t.iloc[0], t.iloc[-1]
    c = {'ind_max': a['rotulo'], 'auc_max': br(a['auc']), 'med_fcu': br(a['mediana_fcu'], dec(a['indicador'])),
         'med_nao': br(a['mediana_nao_fcu'], dec(a['indicador'])), 'ind_min': z['rotulo'], 'auc_min': br(z['auc'])}
    S.tabela('T15', 'fcu_por_indicador', 7, 'fcu_tab', t, c)
    p = t[t['indicador'].str.startswith(('pct_', 'prop_', 'banheiro'))].sort_values('diferenca')
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 0.3 * len(t) + 1.5))
    u = t.sort_values('auc')
    a1.barh(u['rotulo'], u['auc'] - 0.5, left=0.5, color=[ARGILA if v > .5 else PETROLEO for v in u['auc']])
    a1.axvline(0.5, color=CINZA, lw=0.8)
    estilo(a1, 'AUC do indicador sozinho contra FCU')
    yy = np.arange(len(p))
    a2.barh(yy + 0.2, p['mediana_fcu'], height=0.4, color=ARGILA, label='FCU')
    a2.barh(yy - 0.2, p['mediana_nao_fcu'], height=0.4, color=PETROLEO, label='Fora de FCU')
    a2.set_yticks(yy, p['rotulo'])
    a2.legend(frameon=False, fontsize=8)
    estilo(a2, 'Mediana (proporção)')
    fig.tight_layout()
    S.figura('F19', 'fcu_por_indicador', 7, 'fcu_fig', fig, 'T15', c)


# ── Bloco 8. Envelhecimento ────────────────────────────────────────────────────
def bloco8(b, ix, S):
    df = b.df
    cols = [v for v, _ in IDADES]
    tot = pd.DataFrame({'Total': df[cols].sum()})
    reg = df.groupby('regiao')[cols].sum().T
    t = pd.concat([tot, reg[[r for r in REGIOES.values() if r in reg.columns]]], axis=1)
    t = 100 * t / t.sum()
    t.index = [r for _, r in IDADES]
    t = t.rename_axis('faixa_etaria').reset_index()
    so_reg = t.drop(columns=['faixa_etaria', 'Total']).set_index(t['faixa_etaria'])
    rmax = so_reg.loc['70+'].idxmax()
    c16 = {'faixa_max': t.loc[t['Total'].idxmax(), 'faixa_etaria'], 'pct_max': pctbr(t['Total'].max()),
           'pct_70_global': pctbr(t.set_index('faixa_etaria').loc['70+', 'Total']),
           'reg_70_max': rmax, 'pct_70_max': pctbr(so_reg.loc['70+', rmax])}
    S.tabela('T16', 'estrutura_etaria', 8, 'etaria', t, c16)
    fig, ax = plt.subplots(figsize=(8, 5))
    yy = np.arange(len(t))
    ax.barh(yy, t['Total'], color=PETROLEO, alpha=0.85, label='Total')
    for r in so_reg.columns:
        ax.plot(so_reg[r].to_numpy(), yy, 'o', ms=4, color=CORES_REGIAO[r], label=r)
    ax.set_yticks(yy, t['faixa_etaria'])
    ax.legend(frameon=False, fontsize=7)
    estilo(ax, '% da população', 'Faixa etária')
    S.figura('F20', 'piramide_etaria', 8, 'piramide', fig, 'T16', c16)

    env = [c for c in ENVELHECIMENTO if c in b.inds]
    if not env:
        S.avisos.append('T17, T18 e F21 não gerados: sem indicadores de envelhecimento')
        return
    linhas = [{'escopo': 'Total', 'indicador': c, 'rotulo': ROT[c], **descritivas(df[c])} for c in env]
    linhas += [{'escopo': r, 'indicador': c, 'rotulo': ROT[c], **descritivas(x[c])}
               for r, x in df.groupby('regiao') for c in env]
    t = pd.DataFrame(linhas)
    e = extremos_grupo(t[t['escopo'] != 'Total'], 'escopo', env[0])
    iep = t[(t['escopo'] == 'Total') & (t['indicador'] == 'iep_setor')]['mediana']
    S.tabela('T17', 'envelhecimento_por_regiao', 8, 'envelhecimento', t,
             {'reg_max': e['grupo_max'], 'med_max': e['val_max'], 'reg_min': e['grupo_min'],
              'med_min': e['val_min'], 'iep_med': br(iep.iloc[0]) if len(iep) else '—'})
    outros = [c for c in b.inds if c not in env]
    C = df[env + outros].corr(method='spearman').loc[env, outros]
    t = C.rename_axis('indicador').reset_index()
    linha = C.loc[env[0]]
    k = linha.abs().idxmax()
    rr = br(C.loc[env[0], 'renda_media']) if 'renda_media' in outros else '—'
    S.tabela('T18', 'envelhecimento_correlacoes', 8, 'env_correl', t,
             {'ind': ROT[k], 'rho': br(linha[k]), 'rho_renda': rr})
    eixo = 'renda_media' if 'renda_media' in outros else k
    m = df[[env[0], eixo]].dropna()
    m = m[m[eixo] > 0] if eixo.startswith('renda') else m
    fig, ax = plt.subplots(figsize=(7, 5))
    hb = ax.hexbin(np.log10(m[eixo]) if eixo.startswith('renda') else m[eixo], m[env[0]],
                   gridsize=50, cmap=SEQUENCIAL, mincnt=1)
    plt.colorbar(hb, ax=ax, label='setores')
    estilo(ax, ROT[eixo] + (' (log10 R$)' if eixo.startswith('renda') else ''), ROT[env[0]])
    S.figura('F21', 'dispersao_60mais', 8, 'dispersao_60', fig, 'T18', {'rho_renda': rr})


# ── Bloco 9. Adequação fatorial ────────────────────────────────────────────────
def bloco9(b, ix, S):
    r, col = ix.r, ix.col
    t = pd.DataFrame([('setores (n)', r['n']), ('variáveis (p)', r['p']), ('KMO', r['kmo']),
                      ('Bartlett qui-quadrado', r['bartlett_qui2']), ('Bartlett graus de liberdade', r['bartlett_gl']),
                      ('determinante de R', r['det_R']), ('fatores pelo critério de Kaiser', r['kaiser']),
                      ('fatores pela análise paralela de Horn', r['horn_retidos']),
                      (f"variância explicada por {r['sem_rotacao'].shape[1]} fatores (%)", r['var_explicada_k'])], columns=['medida', 'valor'])
    S.tabela('T19', 'adequacao_fatorial', 9, 'adequacao', t,
             {'kmo': br(r['kmo']), 'n': intbr(r['n']), 'kaiser': intbr(r['kaiser']),
              'horn': intbr(r['horn_retidos']), 'var_k': br(r['var_explicada_k'], 1),
              'k_fatores': intbr(r['sem_rotacao'].shape[1])})
    t = pd.DataFrame({'variavel': col, 'rotulo': [ROT[c] for c in col], 'msa': r['msa'],
                      'comunalidade': r['comunalidade'], 'comunalidade_obliqua': r['comunalidade_obliqua']})
    for nome, M in (('sem_rotacao', r['sem_rotacao']), ('varimax', r['varimax']),
                    ('promax_padrao', r['promax_padrao']), ('promax_estrutura', r['promax_estrutura'])):
        for j in range(M.shape[1]):
            t[f'{nome}_f{j + 1}'] = M[:, j]
    a, z = t.loc[t['msa'].idxmin()], t.loc[t['comunalidade_obliqua'].idxmin()]
    S.tabela('T20', 'variaveis_cargas', 9, 'variaveis', t,
             {'var_msa_min': a['rotulo'], 'msa_min': br(a['msa']), 'var_h2_min': z['rotulo'],
              'h2_min': br(z['comunalidade_obliqua'])})
    f1, f2 = t['promax_padrao_f1'].abs().idxmax(), t['promax_padrao_f2'].abs().idxmax()
    c23 = {'var_f1': t.at[f1, 'rotulo'], 'carga_f1': br(t.at[f1, 'promax_padrao_f1']),
           'var_f2': t.at[f2, 'rotulo'], 'carga_f2': br(t.at[f2, 'promax_padrao_f2'])}
    val = r['autovalores']
    t21 = pd.DataFrame({'componente': np.arange(1, len(val) + 1), 'autovalor': val, 'horn': r['horn'],
                        'pct_variancia': 100 * val / len(val), 'pct_acumulado': 100 * np.cumsum(val) / len(val)})
    c21 = {'autov1': br(val[0]), 'autov2': br(val[1]) if len(val) > 1 else '—',
           'horn2': br(r['horn'][1]) if len(val) > 1 else '—',
           'pct_acum2': br(t21['pct_acumulado'].iloc[min(1, len(val) - 1)], 1)}
    S.tabela('T21', 'autovalores', 9, 'autovalores', t21, c21)
    phi = r['phi']
    t = pd.DataFrame(phi, index=[f'F{j + 1}' for j in range(len(phi))], columns=[f'F{j + 1}' for j in range(len(phi))])
    S.tabela('T22', 'phi', 9, 'phi', t, {'phi': br(phi[0, 1]) if len(phi) > 1 else '—'}, index=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(t21['componente'], val, 'o-', color=PETROLEO, label='Autovalores')
    ax.plot(t21['componente'], r['horn'], '--', color=ARGILA, label='Análise paralela de Horn')
    ax.axhline(1, color=CINZA, lw=0.8, ls=':', label='Kaiser (autovalor 1)')
    ax.legend(frameon=False, fontsize=8)
    estilo(ax, 'Componente', 'Autovalor')
    S.figura('F22', 'sedimentacao_horn', 9, 'sedimentacao', fig, 'T21', c21)
    M = r['promax_padrao']
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color=CINZA, lw=0.6))
    ax.axhline(0, color=CINZA, lw=0.5)
    ax.axvline(0, color=CINZA, lw=0.5)
    for i, c in enumerate(col):
        ax.annotate('', (M[i, 0], M[i, 1] if M.shape[1] > 1 else 0), (0, 0),
                    arrowprops={'arrowstyle': '->', 'color': PETROLEO})
        ax.text(M[i, 0], (M[i, 1] if M.shape[1] > 1 else 0) + 0.03, ROT[c], fontsize=8, color=TINTA)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')
    estilo(ax, 'F1 (carga padrão, promax)', 'F2 (carga padrão, promax)')
    S.figura('F23', 'mapa_cargas', 9, 'cargas', fig, 'T20', c23)


# ── Bloco 10. O índice da versão ───────────────────────────────────────────────
def rotulo_faixa(f):
    return ie.FAIXAS[f] if f >= 0 else 'indefinida'


def bloco10(b, ix, S):
    col, M, s = ix.col, ix.M, ix.setores
    socio = 'renda_inv' in col and M.shape[1] > 1
    fr = ie.fator_renda(M, col) if socio else 0
    dim = np.abs(M).argmax(axis=1)
    nome = (lambda j: (f'F{j + 1} (socioeconômica)' if j == fr else
                       (f'F{j + 1} (saneamento)' if M.shape[1] == 2 else f'F{j + 1}'))
            if socio else f'F{j + 1}')
    t = pd.DataFrame({'variavel': col, 'rotulo': [ROT[c] for c in col], 'dimensao': [nome(j) for j in dim],
                      'carga': [M[i, j] for i, j in enumerate(dim)], 'peso_dimensao': [100 * ix.rep[j] for j in dim],
                      'peso': 100 * ix.w})
    a = t.loc[t['peso'].idxmax()]
    S.tabela('T23', 'pesos', 10, 'pesos', t, {'var_max': a['rotulo'], 'peso_max': br(a['peso'], 1),
                                               'dim_principal': nome(fr), 'peso_socio': br(100 * ix.rep[fr], 1)})
    linhas = [{'escopo': 'Total', **descritivas(s['ivs'])}]
    linhas += [{'escopo': r, **descritivas(x['ivs'])} for r, x in s.groupby('regiao')]
    t = pd.DataFrame(linhas)
    S.tabela('T24', 'indice_descritivas', 10, 'indice_desc', t,
             {'n': intbr(t['n'].iloc[0]), 'mediana': br(t['mediana'].iloc[0]), 'p90': br(t['p90'].iloc[0])})
    linhas = []
    for regra in ('ivs_bh', 'quartis'):
        vc = s[f'faixa_{regra}'].value_counts().sort_index()
        for f, n in vc.items():
            linhas.append({'regra': regra, 'faixa': rotulo_faixa(f), 'setores': int(n), 'pct': 100 * n / len(s)})
    t = pd.DataFrame(linhas)
    g = t.set_index(['regra', 'faixa'])['pct']
    c25 = {'pct_baixo_bh': pctbr(g.get(('ivs_bh', 'baixo'), 0)),
           'pct_muito_bh': pctbr(g.get(('ivs_bh', 'muito_elevado'), 0)),
           'pct_muito_q': pctbr(g.get(('quartis', 'muito_elevado'), 0))}
    S.tabela('T25', 'faixas', 10, 'faixas', t, c25)
    e = ix.eleg
    t = pd.DataFrame([
        ('AUC global contra FCU', ix.auc, ''), ('AUC municipal (mediana)', ix.auc_mun[0], ''),
        ('municípios na AUC municipal', ix.auc_mun[1], f'ao menos {ie.MIN_GRUPO} setores de FCU e fora'),
        (f'peso da dimensão {nome(fr)} (%)', 100 * ix.rep[fr], ''),
        ('KMO ≥ 0,70', int(e['kmo_ok']), 'sim' if e['kmo_ok'] else 'não'),
        ('MSA ≥ 0,50 em todas', int(e['msa_ok']), 'sim' if e['msa_ok'] else 'não'),
        ('comunalidade mínima', e['comunalidade_min'], e['comunalidade_min_variavel']),
        ('comunalidade ≥ 0,30 em todas', int(e['comunalidade_ok']), 'sim' if e['comunalidade_ok'] else 'não'),
        ('maior carga mínima', e['carga_max_min'], e['carga_max_min_variavel']),
        ('carga ≥ 0,40 em todas', int(e['cargas_ok']), 'sim' if e['cargas_ok'] else 'não'),
        ('elegível pelos critérios do NB05', int(e['elegivel']), 'sim' if e['elegivel'] else 'não'),
    ], columns=['medida', 'valor', 'detalhe'])
    c26 = {'auc_global': br(ix.auc), 'auc_mun': br(ix.auc_mun[0]), 'n_mun': intbr(ix.auc_mun[1]),
           'elegivel': 'elegível' if e['elegivel'] else 'não elegível'}
    S.tabela('T26', 'auc_e_elegibilidade', 10, 'auc_elegib', t, c26)
    t = ie.auc_grupos(s['ivs'], s['is_fcu'], s['NM_MUN']).rename_axis('NM_MUN').reset_index()
    t['entra_na_mediana'] = (t['n1'] >= ie.MIN_GRUPO) & (t['n0'] >= ie.MIN_GRUPO)
    t = t.sort_values('auc', ascending=False)
    u = t[t['entra_na_mediana']]
    S.tabela('T27', 'auc_por_municipio', 10, 'auc_municipio', t,
             {'mun_max': u['NM_MUN'].iloc[0] if len(u) else '—', 'auc_max': br(u['auc'].iloc[0]) if len(u) else '—',
              'mun_min': u['NM_MUN'].iloc[-1] if len(u) else '—', 'auc_min': br(u['auc'].iloc[-1]) if len(u) else '—'})
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bins = np.linspace(np.nanmin(s['ivs']), np.nanmax(s['ivs']), 50)
    ax.hist([s.loc[s['faixa_ivs_bh'] == f, 'ivs'] for f in range(4)], bins=bins, stacked=True,
            color=CORES_FAIXA, label=ie.ROT_FAIXA)
    ax.legend(frameon=False, fontsize=8, title='Faixa (regra do IVS-BH)', title_fontsize=8)
    estilo(ax, 'IVS da versão (0 a 1, normalizado no município)', 'Setores')
    S.figura('F24', 'histograma_por_faixa', 10, 'hist_faixa', fig, 'T25', c25)
    m = s.dropna(subset=['ivs', 'is_fcu'])
    o = np.argsort(-m['ivs'].to_numpy(), kind='mergesort')
    y = m['is_fcu'].to_numpy()[o]
    tp, fp = np.cumsum(y), np.cumsum(1 - y)
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.plot(np.r_[0, fp / fp[-1]], np.r_[0, tp / tp[-1]], color=ARGILA, lw=1.5)
    ax.plot([0, 1], [0, 1], ':', color=CINZA)
    ax.set_aspect('equal')
    estilo(ax, 'Proporção de setores fora de FCU acima do corte', 'Proporção de setores de FCU acima do corte')
    S.figura('F25', 'curva_roc', 10, 'roc', fig, 'T26', c26)


# ── Bloco 11. Quem está em risco ───────────────────────────────────────────────
def bloco11(b, ix, S):
    s = ix.setores.assign(faixa=lambda x: x['faixa_ivs_bh'].map(rotulo_faixa))
    g = s.groupby(['NM_MUN', 'faixa']).agg(setores=('ivs', 'size'), pessoas=('v0001', 'sum'),
                                          pessoas_60mais=('pop_60mais', 'sum')).unstack(fill_value=0)
    g.columns = [f'{a}_{f}' for a, f in g.columns]
    p = g[[c for c in g.columns if c.startswith('pessoas_') and not c.startswith('pessoas_60')]]
    alto = [c for c in ('pessoas_elevado', 'pessoas_muito_elevado') if c in g.columns]
    g['pct_pessoas_elevado_ou_mais'] = 100 * g[alto].sum(axis=1) / p.sum(axis=1)
    g = g.sort_values('pct_pessoas_elevado_ou_mais', ascending=False).reset_index()
    c28 = {'mun_max': g['NM_MUN'].iloc[0], 'pct_max': pctbr(g['pct_pessoas_elevado_ou_mais'].iloc[0]),
           'mun_min': g['NM_MUN'].iloc[-1], 'pct_min': pctbr(g['pct_pessoas_elevado_ou_mais'].iloc[-1])}
    S.tabela('T28', 'risco_por_municipio', 11, 'risco_municipio', g, c28)
    t = s.groupby('faixa').agg(setores=('ivs', 'size'), pessoas=('v0001', 'sum'),
                               pessoas_60mais=('pop_60mais', 'sum'))
    t = t.reindex([f for f in ie.FAIXAS + ['indefinida'] if f in t.index])
    t['pct_pessoas'] = 100 * t['pessoas'] / t['pessoas'].sum()
    t['pct_pessoas_60mais'] = 100 * t['pessoas_60mais'] / t['pessoas_60mais'].sum()
    mu = t.loc['muito_elevado'] if 'muito_elevado' in t.index else None
    S.tabela('T29', 'risco_total', 11, 'risco_total', t.reset_index(),
             {'pessoas_muito': intbr(mu['pessoas']) if mu is not None else '—',
              'pct_muito': pctbr(mu['pct_pessoas']) if mu is not None else '—',
              'p60_muito': intbr(mu['pessoas_60mais']) if mu is not None else '—'})
    fig, ax = plt.subplots(figsize=(9, 0.2 * len(g) + 1.5))
    esq = np.zeros(len(g))
    tot = g[p.columns].sum(axis=1).to_numpy()
    for f, cor, rot in zip(ie.FAIXAS, CORES_FAIXA, ie.ROT_FAIXA):
        if f'pessoas_{f}' in g.columns:
            v = 100 * g[f'pessoas_{f}'].to_numpy() / tot
            ax.barh(g['NM_MUN'], v, left=esq, color=cor, label=rot)
            esq += v
    ax.invert_yaxis()
    ax.tick_params(axis='y', labelsize=6)
    ax.legend(frameon=False, fontsize=7, ncol=4, loc='lower center', bbox_to_anchor=(0.5, 1.0))
    estilo(ax, '% dos moradores do município, por faixa do IVS (regra do IVS-BH)')
    S.figura('F26', 'risco_por_municipio', 11, 'risco_barras', fig, 'T28', c28)


# ── Bloco 12. Desigualdade interna ─────────────────────────────────────────────
def gini(x):
    x = np.sort(x)
    n = len(x)
    return float(2 * np.sum(np.arange(1, n + 1) * x) / (n * x.sum()) - (n + 1) / n) if n and x.sum() > 0 else np.nan


def theil(x):
    mu = x.mean()
    if not len(x) or mu <= 0:
        return np.nan
    r = x / mu
    return float(np.mean(np.where(r > 0, r * np.log(np.where(r > 0, r, 1)), 0)))


def bloco12(b, ix, S):
    linhas = []
    for mun, x in ix.setores.groupby('NM_MUN'):
        v = x['ivs'].dropna().to_numpy()
        p10, p90 = (np.quantile(v, [.1, .9]) if len(v) else (np.nan, np.nan))
        linhas.append({'NM_MUN': mun, 'setores': len(v), 'media': v.mean() if len(v) else np.nan,
                       'p10': p10, 'p90': p90, 'p90_p10': p90 / p10 if p10 > 0 else np.nan,
                       'gini': gini(v), 'theil': theil(v)})
    t = pd.DataFrame(linhas).sort_values('gini', ascending=False)
    u = t.dropna(subset=['gini'])
    c = {'mun_gini_max': u['NM_MUN'].iloc[0], 'gini_max': br(u['gini'].iloc[0]),
         'mun_gini_min': u['NM_MUN'].iloc[-1], 'gini_min': br(u['gini'].iloc[-1])}
    S.tabela('T30', 'desigualdade_interna', 12, 'desigualdade_tab', t, c)
    fig, ax = plt.subplots(figsize=(8, 0.2 * len(u) + 1.5))
    ax.barh(u['NM_MUN'], u['gini'], color=PETROLEO)
    ax.plot(u['theil'], u['NM_MUN'], 'o', ms=3, color=ARGILA, label='Theil')
    ax.invert_yaxis()
    ax.tick_params(axis='y', labelsize=6)
    ax.legend(frameon=False, fontsize=7)
    estilo(ax, 'Gini do IVS dentro do município (barras) e Theil (pontos)')
    S.figura('F27', 'desigualdade_interna', 12, 'desigualdade_fig', fig, 'T30', c)


# ── Bloco 13. Comparação com a referência ──────────────────────────────────────
def bloco13(b, ix, S):
    ref = pd.read_csv(REF_SETOR, dtype={'CD_SETOR': str})
    m = ix.setores.merge(ref[['CD_SETOR', 'ivs_referencia', 'faixa_ivs_bh']].rename(
        columns={'faixa_ivs_bh': 'faixa_referencia'}), on='CD_SETOR', how='inner')
    m['faixa_versao'] = m['faixa_ivs_bh'].map(rotulo_faixa)
    linhas = [{'escopo': 'Total', 'setores_comuns': len(m), 'spearman': rho(m['ivs'], m['ivs_referencia'])}]
    linhas += [{'escopo': mun, 'setores_comuns': len(x),
                'spearman': rho(x['ivs'], x['ivs_referencia'])}
               for mun, x in m.groupby('NM_MUN')]
    t = pd.DataFrame(linhas)
    u = t.iloc[1:].dropna(subset=['spearman'])
    u = u.loc[[u['spearman'].idxmin()]] if len(u) else u
    S.tabela('T31', 'spearman_com_referencia', 13, 'comp_spearman', t,
             {'rho_global': br(t['spearman'].iloc[0]),
              'mun_rho_min': u['escopo'].iloc[0] if len(u) else '—', 'rho_min': br(u['spearman'].iloc[0]) if len(u) else '—'})
    ordem = ie.FAIXAS + ['indefinida']
    ct = pd.crosstab(m['faixa_referencia'], m['faixa_versao'])
    ct = ct.reindex(index=[f for f in ordem if f in ct.index], columns=[f for f in ordem if f in ct.columns], fill_value=0)
    t = ct.stack().rename('setores').reset_index()
    t['pct_do_total'] = 100 * t['setores'] / max(len(m), 1)
    fora = t[(t['faixa_referencia'] != t['faixa_versao']) & (t['setores'] > 0)]
    c32 = ({'de': fora.loc[fora['setores'].idxmax(), 'faixa_referencia'], 'para': fora.loc[fora['setores'].idxmax(), 'faixa_versao'],
            'setores': intbr(fora['setores'].max())} if len(fora) else {'de': '—', 'para': '—', 'setores': intbr(0)})
    S.tabela('T32', 'matriz_de_faixas', 13, 'comp_matriz_tab', t, c32)
    m['muda'] = m['faixa_referencia'] != m['faixa_versao']
    linhas = [{'NM_MUN': 'Todos', 'setores_comuns': len(m), 'mudam_faixa': int(m['muda'].sum()),
               'pct_mudam': 100 * m['muda'].mean() if len(m) else np.nan}]
    linhas += sorted(({'NM_MUN': mun, 'setores_comuns': len(x), 'mudam_faixa': int(x['muda'].sum()),
                       'pct_mudam': 100 * x['muda'].mean()} for mun, x in m.groupby('NM_MUN')),
                     key=lambda d: -d['pct_mudam'])
    t = pd.DataFrame(linhas)
    c33 = {'pct_global': pctbr(t['pct_mudam'].iloc[0]),
           'mun_max': t['NM_MUN'].iloc[1] if len(t) > 1 else '—',
           'pct_max': pctbr(t['pct_mudam'].iloc[1]) if len(t) > 1 else '—'}
    S.tabela('T33', 'municipios_que_mudam', 13, 'comp_municipios_tab', t, c33)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.imshow(ct.to_numpy(), cmap=SEQUENCIAL)
    for i in range(ct.shape[0]):
        for j in range(ct.shape[1]):
            ax.text(j, i, intbr(ct.iat[i, j]), ha='center', va='center', fontsize=8, color=TINTA)
    ax.set_xticks(range(ct.shape[1]), ct.columns, fontsize=8)
    ax.set_yticks(range(ct.shape[0]), ct.index, fontsize=8)
    ax.set_xlabel('Faixa nesta versão', fontsize=9)
    ax.set_ylabel('Faixa na referência', fontsize=9)
    S.figura('F28', 'matriz_de_faixas', 13, 'comp_matriz_fig', fig, 'T32', c32)
    top = t.iloc[1:21]
    fig, ax = plt.subplots(figsize=(8, 0.3 * len(top) + 1.2))
    ax.barh(top['NM_MUN'], top['pct_mudam'], color=ARGILA)
    ax.invert_yaxis()
    ax.tick_params(axis='y', labelsize=7)
    estilo(ax, '% dos setores que mudam de faixa (regra do IVS-BH)')
    S.figura('F29', 'municipios_que_mudam', 13, 'comp_municipios_fig', fig, 'T33', c33)


def sensibilidade(b, ix, cfg, S):
    """T34: a versão com cada valor alternativo de um parâmetro exploratório (config
    `sensibilidade`: lista de {rotulo, recorte}), comparada com o valor-padrão."""
    linhas = [{'rotulo': 'valor-padrão desta versão', 'setores_recorte': len(b.df), 'setores_indice': len(ix.d),
               'kmo': ix.r['kmo'], 'auc_global': ix.auc, 'auc_municipal': ix.auc_mun[0],
               'elegivel': int(ix.eleg['elegivel']), 'spearman_com_padrao': 1.0, 'pct_mudam_faixa': 0.0}]
    for alt in cfg['sensibilidade']:
        c2 = json.loads(json.dumps(cfg))
        c2['recorte'].update(alt.get('recorte', {}))
        c2['indice'].update(alt.get('indice', {}))
        b2 = montar_base(c2)
        i2 = calcular_indice(b2.df, c2)
        m = ix.setores.merge(i2.setores[['CD_SETOR', 'ivs', 'faixa_ivs_bh']], on='CD_SETOR', suffixes=('', '_alt'))
        linhas.append({'rotulo': alt['rotulo'], 'setores_recorte': len(b2.df), 'setores_indice': len(i2.d),
                       'kmo': i2.r['kmo'], 'auc_global': i2.auc, 'auc_municipal': i2.auc_mun[0],
                       'elegivel': int(i2.eleg['elegivel']), 'spearman_com_padrao': rho(m['ivs'], m['ivs_alt']),
                       'pct_mudam_faixa': 100 * (m['faixa_ivs_bh'] != m['faixa_ivs_bh_alt']).mean()})
    t = pd.DataFrame(linhas)
    a = t.iloc[-1]
    S.tabela('T34', 'sensibilidade', 10, 'sensibilidade', t,
             {'rotulo_alt': a['rotulo'], 'n_alt': intbr(a['setores_indice']), 'n_padrao': intbr(t['setores_indice'].iloc[0]),
              'rho': br(a['spearman_com_padrao']), 'pct_mudam': pctbr(a['pct_mudam_faixa']),
              'auc_alt': br(a['auc_municipal'])})


def faixas_alternativas(ix, S):
    """C5: as faixas do mesmo índice por outras regras — quintis e quebras naturais
    (k-médias 1D com 4 classes) dentro do município, e agrupamento dos setores pelos
    componentes normalizados (k pela silhueta entre 3 e 6, e sempre 4)."""
    s, d, col = ix.setores, ix.d, ix.col
    g = s['NM_MUN']
    regras = {'IVS-BH (média ± DP)': s['faixa_ivs_bh'].to_numpy(), 'quartis': s['faixa_quartis'].to_numpy(),
              'quintis': np.clip(np.ceil(5 * s['ivs'].groupby(g).rank(pct=True)) - 1, 0, 4).astype(int).to_numpy()}
    qn = pd.Series(-1, index=s.index)
    for _, x in s.groupby('NM_MUN'):
        if len(x) >= 8:
            rot = kmedias(x[['ivs']].to_numpy(), 4)[0]
            qn.loc[x.index] = ordenar_grupos(rot, x['ivs'].to_numpy())
    regras['quebras naturais (4 classes)'] = qn.to_numpy()
    Z = ((d[col] - d[col].groupby(d['NM_MUN']).transform('min'))
         / (d[col].groupby(d['NM_MUN']).transform('max') - d[col].groupby(d['NM_MUN']).transform('min'))).fillna(0).to_numpy()
    sil = []
    rots = {}
    for k in range(3, 7):
        rot = kmedias(Z, k)[0]
        rots[k] = ordenar_grupos(rot, s['ivs'].to_numpy())
        sil.append({'k': k, 'silhueta': silhueta(Z, rot)})
    t38 = pd.DataFrame(sil)
    kmelhor = int(t38.loc[t38['silhueta'].idxmax(), 'k'])
    regras[f'agrupamento (k = {kmelhor}, silhueta)'] = rots[kmelhor]
    if kmelhor != 4:
        regras['agrupamento (k = 4)'] = rots[4]
    linhas, conc = [], []
    for nome, f in regras.items():
        vc = pd.Series(f).value_counts().sort_index()
        for c, n in vc.items():
            linhas.append({'regra': nome, 'classe': int(c) + 1 if c >= 0 else 'indefinida', 'setores': int(n), 'pct': 100 * n / len(f)})
        ok = (f >= 0) & (regras['IVS-BH (média ± DP)'] >= 0)
        conc.append({'regra': nome, 'classes': int(f.max()) + 1,
                     'spearman_com_ivs_bh': rho(pd.Series(f[ok]).astype(float), pd.Series(regras['IVS-BH (média ± DP)'][ok]).astype(float)),
                     'pct_mesma_classe': 100 * (f[ok] == regras['IVS-BH (média ± DP)'][ok]).mean() if f.max() == 3 else np.nan})
    t37 = pd.DataFrame(conc)
    t36 = pd.DataFrame(linhas).merge(t37[['regra', 'spearman_com_ivs_bh']], on='regra', how='left')
    u = t37.iloc[1:].dropna(subset=['spearman_com_ivs_bh'])
    z = u.loc[u['spearman_com_ivs_bh'].idxmin()]
    c36 = {'regra_min': z['regra'], 'rho_min': br(z['spearman_com_ivs_bh'])}
    S.tabela('T36', 'faixas_alternativas', 10, 'faixas_alt_tab', t36, c36)
    S.tabela('T37', 'faixas_concordancia', 10, 'faixas_concordancia', t37, c36)
    S.tabela('T38', 'silhueta', 10, 'silhueta', t38, {'k': intbr(kmelhor), 'sil': br(t38['silhueta'].max())})
    fig, ax = plt.subplots(figsize=(9, 0.5 * len(regras) + 1.2))
    for i, (nome, f) in enumerate(regras.items()):
        vc = pd.Series(f[f >= 0]).value_counts(normalize=True).sort_index()
        esq = 0
        for c, p in vc.items():
            cor = plt.cm.Reds(0.2 + 0.7 * c / max(vc.index.max(), 1))
            ax.barh(i, 100 * p, left=esq, color=cor, edgecolor='white')
            esq += 100 * p
    ax.set_yticks(range(len(regras)), list(regras))
    ax.invert_yaxis()
    estilo(ax, '% dos setores em cada classe (da mais clara, menos vulnerável, à mais escura)')
    S.figura('F30', 'faixas_alternativas', 10, 'faixas_alt_fig', fig, 'T37', c36)


BLOCOS = {1: bloco1, 2: bloco2, 3: bloco3, 4: bloco4, 5: bloco5, 6: bloco6, 7: bloco7,
          8: bloco8, 9: bloco9, 10: bloco10, 11: bloco11, 12: bloco12, 13: bloco13}


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit('uso: eda_versoes.py analises_exploratorias/<versao>')
    t0 = time.time()
    pasta = Path(sys.argv[1]).resolve()
    cfg = ler_config(pasta)
    S = Saida(pasta, json.loads(MODELOS.read_text(encoding='utf-8')))
    b = montar_base(cfg)
    b.cfg = cfg
    ix = calcular_indice(b.df, cfg) if cfg['indice'] else None
    for n in cfg['blocos']:
        if n >= 9 and ix is None:
            S.avisos.append(f'bloco {n} não gerado: a versão não tem índice')
            continue
        BLOCOS[n](b, ix, S)
    if cfg.get('faixas_alternativas') and ix is not None:
        faixas_alternativas(ix, S)
    if cfg.get('sensibilidade') and ix is not None:
        sensibilidade(b, ix, cfg, S)
    S.fechar()
    if ix is not None:
        ix.setores.to_csv(pasta / 'setores_indice.csv', index=False)
    cat = pd.DataFrame(S.linhas)
    print(f"Versão {cfg['versao'] or pasta.name} — {cfg['titulo']}")
    print(f"Recorte: {intbr(len(b.df))} setores · {len(b.inds)} indicadores · "
          f"{b.df['NM_MUN'].nunique()} municípios")
    if ix is not None:
        r, e = ix.r, ix.eleg
        fr = ie.fator_renda(ix.M, ix.col) if 'renda_inv' in ix.col and ix.M.shape[1] > 1 else 0
        print(f"Índice: {intbr(len(ix.d))} setores · {len(ix.col)} componentes · KMO {br(r['kmo'])} · "
              f"Kaiser {r['kaiser']} · Horn {r['horn_retidos']} · var. {r['sem_rotacao'].shape[1]} fatores {br(r['var_explicada_k'], 1)}%")
        print(f"Peso socioeconômico {br(100 * ix.rep[fr], 1)}% · AUC global {br(ix.auc)} · "
              f"AUC municipal {br(ix.auc_mun[0])} ({ix.auc_mun[1]} municípios) · "
              f"{'elegível' if e['elegivel'] else 'NÃO elegível'}")
        vc = ix.setores['faixa_ivs_bh'].value_counts(normalize=True).sort_index()
        print('Faixas (IVS-BH): ' + ' · '.join(f'{rotulo_faixa(f)} {pctbr(100 * p)}' for f, p in vc.items()))
    print(f"Blocos: {', '.join(map(str, cfg['blocos']))} · tabelas {int((cat['tipo'] == 'tabela').sum())} · "
          f"figuras {int((cat['tipo'] == 'figura').sum())} · {time.time() - t0:.0f} s")
    for a in S.avisos[:8]:
        print('Aviso: ' + a)


if __name__ == '__main__':
    main()
