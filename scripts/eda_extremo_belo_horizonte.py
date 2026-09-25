"""O efeito do setor extremo de renda DENTRO de Belo Horizonte.

Por que este script existe
--------------------------
A 2ª rodada da EDA (scripts/eda_atualizada.py) refez 16 tabelas com
`renda_media_sem_extremo`, mas `descritivas_por_municipio` não é uma delas — e é
justamente a que importa, porque o setor excluído está em Belo Horizonte.

No agregado dos 70 municípios o extremo move a média em 0,04%. Dentro do município
dele o efeito é outra ordem de grandeza. E há uma consequência metodológica que
nenhuma tabela do projeto mediu: o IVS normaliza a renda por MIN-MAX MUNICIPAL, então
um máximo distorcido comprime todos os demais setores daquele município contra o zero.
Este script mede as duas coisas.

Uso:
    ./.venv/bin/python scripts/eda_extremo_belo_horizonte.py
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'src'))
from ivs_censo.renda import SETORES_RENDA_EXCLUIDA  # noqa: E402

DB = RAIZ / 'banco_de_dados' / 'entrega_orientadora' / 'Base_ELSI_70Municipios_Censo2022.db'
SAIDA = RAIZ / 'banco_de_dados' / 'eda' / 'atualizada'
FIG = SAIDA / 'figuras'
TINTA, PETROL, CLAY, CINZA, SURF = '#1A1A1A', '#1F4E4A', '#A83A2C', '#666666', '#FCFCFB'

con = sqlite3.connect(DB)
df = pd.read_sql("""SELECT CD_SETOR, NM_MUN, urbano, Dados_sig,
                           renda_media, renda_media_sem_extremo
                    FROM setores_censitarios""", con)
con.close()
df = df[(pd.to_numeric(df.urbano, errors='coerce') == 1) & (df.Dados_sig == 'OK')].copy()
EXCLUIDO = sorted(SETORES_RENDA_EXCLUIDA)[0]
MUN = df.loc[df.CD_SETOR.astype(str).str.strip() == EXCLUIDO, 'NM_MUN'].iloc[0]
print(f'setor excluído: {EXCLUIDO} · município: {MUN}')


def descrever(s: pd.Series) -> dict:
    s = s.dropna()
    return {'n': len(s), 'media': s.mean(), 'mediana': s.median(), 'dp': s.std(),
            'cv_pct': 100 * s.std() / s.mean(), 'p99': s.quantile(0.99), 'max': s.max()}


# ── 1. O setor, e o que ele é diante do município ───────────────────────────
bh = df[df.NM_MUN == MUN]
alvo = bh[bh.CD_SETOR.astype(str).str.strip() == EXCLUIDO]
renda_alvo = float(alvo.renda_media.iloc[0])
bh_sem = bh[bh.CD_SETOR.astype(str).str.strip() != EXCLUIDO]
print(f'\nrenda do setor: R$ {renda_alvo:,.2f}')
print(f'mediana de {MUN} sem ele: R$ {bh_sem.renda_media.median():,.2f} '
      f'({renda_alvo / bh_sem.renda_media.median():.0f}x)')

# ── 2. Descritivas: o município contra o agregado ───────────────────────────
linhas = []
for rot, s_com, s_sem in (
        (f'{MUN}', bh.renda_media, bh.renda_media_sem_extremo),
        ('70 municípios ELSI', df.renda_media, df.renda_media_sem_extremo)):
    c, s = descrever(s_com), descrever(s_sem)
    for medida in ('n', 'media', 'mediana', 'dp', 'cv_pct', 'p99', 'max'):
        var = 100 * (s[medida] - c[medida]) / c[medida] if c[medida] else 0.0
        linhas.append({'recorte': rot, 'medida': medida, 'com_extremo': c[medida],
                       'sem_extremo': s[medida], 'variacao_pct': var})
desc = pd.DataFrame(linhas)
desc.round(4).to_csv(SAIDA / 'extremo_bh_descritivas.csv', sep=';', index=False,
                     encoding='utf-8-sig')
print('\n' + desc.pivot(index='medida', columns='recorte', values='variacao_pct')
      .round(2).to_string())

# ── 3. A normalização min-max municipal — a consequência metodológica ───────
# O IVS é intraurbano: a renda é normalizada DENTRO de cada município. Com um máximo
# distorcido, todos os demais setores daquele município são empurrados contra o zero.
def minmax(s):
    s = s.dropna()
    return (s - s.min()) / (s.max() - s.min())

norm_com, norm_sem = minmax(bh.renda_media), minmax(bh.renda_media_sem_extremo)
comum = norm_com.index.intersection(norm_sem.index)
desl = (norm_sem[comum] - norm_com[comum])
nrm = pd.DataFrame([{
    'setores_de_bh': len(comum),
    'norm_media_com': norm_com[comum].mean(), 'norm_media_sem': norm_sem[comum].mean(),
    'norm_mediana_com': norm_com[comum].median(), 'norm_mediana_sem': norm_sem[comum].median(),
    'deslocamento_medio': desl.mean(), 'deslocamento_maximo': desl.max(),
    'setores_abaixo_de_0_05_com': int((norm_com[comum] < 0.05).sum()),
    'setores_abaixo_de_0_05_sem': int((norm_sem[comum] < 0.05).sum()),
    'amplitude_usada_com': float(bh.renda_media.max() - bh.renda_media.min()),
    'amplitude_usada_sem': float(bh.renda_media_sem_extremo.max() - bh.renda_media_sem_extremo.min()),
}])
nrm.round(6).to_csv(SAIDA / 'extremo_bh_normalizacao.csv', sep=';', index=False,
                    encoding='utf-8-sig')
print(f"\nnormalização min-max em {MUN}: média {norm_com[comum].mean():.4f} -> "
      f"{norm_sem[comum].mean():.4f} · setores abaixo de 0,05: "
      f"{int((norm_com[comum] < 0.05).sum()):,} -> {int((norm_sem[comum] < 0.05).sum()):,}")

# ── 4. O ranking dos 70 municípios, com e sem ───────────────────────────────
rk = df.groupby('NM_MUN').agg(media_com=('renda_media', 'mean'),
                              media_sem=('renda_media_sem_extremo', 'mean')).dropna()
rk['posicao_com'] = rk.media_com.rank(ascending=False).astype(int)
rk['posicao_sem'] = rk.media_sem.rank(ascending=False).astype(int)
rk['mudou'] = rk.posicao_sem - rk.posicao_com
rk.sort_values('posicao_com').round(4).to_csv(SAIDA / 'extremo_bh_ranking.csv', sep=';',
                                              encoding='utf-8-sig')
print(f"\n{MUN} no ranking de renda média: {int(rk.loc[MUN,'posicao_com'])}º -> "
      f"{int(rk.loc[MUN,'posicao_sem'])}º de {len(rk)} · "
      f"municípios que mudam de posição: {int((rk.mudou != 0).sum())}")

# ── 5. A figura ─────────────────────────────────────────────────────────────
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.3), facecolor=SURF)
# esquerda: a renda de BH em escala log, com o extremo marcado
v = bh.renda_media.dropna()
a.hist(v[v < 40000], bins=60, color=PETROL, alpha=0.75)
a.axvline(bh_sem.renda_media.median(), color=TINTA, lw=1.4, ls='--')
a.annotate(f'mediana\nR$ {bh_sem.renda_media.median():,.0f}'.replace(',', '.'),
           (bh_sem.renda_media.median(), a.get_ylim()[1]*0.78),
           textcoords='offset points', xytext=(10, 0), color=TINTA, fontsize=9)
a.annotate(f'o extremo está em\nR$ {renda_alvo:,.0f} — fora do quadro'.replace(',', '.'),
           (0.97, 0.88), xycoords='axes fraction', ha='right', color=CLAY, fontsize=9.5)
a.set_title(f'Renda média por setor em {MUN}', color=TINTA, fontsize=11, loc='left')
# o cifrão precisa de escape: o matplotlib leria $...$ como fórmula matemática
a.set_xlabel(r'R\$ por responsável (recorte até R\$ 40 mil)', color=CINZA, fontsize=9)
# direita: o que a normalização municipal faz
b.hist(norm_com[comum], bins=50, color=CLAY, alpha=0.6, label='com o extremo')
b.hist(norm_sem[comum], bins=50, color=PETROL, alpha=0.6, label='sem o extremo')
b.set_title('Renda normalizada dentro do município', color=TINTA, fontsize=11, loc='left')
b.set_xlabel('min-max municipal (0 a 1)', color=CINZA, fontsize=9)
b.legend(frameon=False, fontsize=9, labelcolor=TINTA)
VIRGULA = plt.matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:g}'.replace('.', ','))
for ax in (a, b):
    ax.tick_params(colors=CINZA, labelsize=8.5)
    ax.xaxis.set_major_formatter(VIRGULA)   # decimal com vírgula, como no resto
    ax.grid(axis='y', color=CINZA, alpha=0.15, lw=0.8); ax.set_axisbelow(True)
    for lado in ('top', 'right'):
        ax.spines[lado].set_visible(False)
    for lado in ('left', 'bottom'):
        ax.spines[lado].set_color(CINZA)
    ax.set_facecolor(SURF)
fig.suptitle(f'O setor extremo e o que ele faz com {MUN}', color=TINTA, fontsize=12.5,
             x=0.007, ha='left', y=1.02)
FIG.mkdir(parents=True, exist_ok=True)
fig.savefig(FIG / 'extremo_bh.png', dpi=150, bbox_inches='tight', facecolor=SURF)
plt.close(fig)
print(f'\nfigura: {(FIG / "extremo_bh.png").relative_to(RAIZ)}')
print('extremo_bh_descritivas.csv · extremo_bh_normalizacao.csv · extremo_bh_ranking.csv')

# ── 6. Sensibilidade: alternativas de imputação da renda (demanda 1) ────────
# Não é o critério que a coluna da entrega usa (mediana de BH sem o setor); é o registro
# do efeito das alternativas, pedido no padrão da Fase 0 enquanto a orientadora não escolhe.
alvo_idx = alvo.index[0]
alternativas = [
    ('mediana de BH sem o setor', bh_sem.renda_media.median()),
    ('mediana de BH com o setor', bh.renda_media.median()),
    ('mediana dos 70 municípios sem o setor',
     df.loc[df.CD_SETOR.astype(str).str.strip() != EXCLUIDO, 'renda_media'].median()),
]
linhas_sens = []
for nome, valor in alternativas:
    ajustada = df.renda_media.copy()
    ajustada.loc[alvo_idx] = valor
    linha = {'alternativa': nome, 'valor_imputado': valor}
    for rotulo, serie in (('bh', ajustada.loc[bh.index]), ('agregado', ajustada)):
        d = descrever(serie)
        linha[f'{rotulo}_media'] = d['media']
        linha[f'{rotulo}_dp'] = d['dp']
        linha[f'{rotulo}_max'] = d['max']
    linhas_sens.append(linha)
sens = pd.DataFrame(linhas_sens)
sens.round(4).to_csv(SAIDA / 'renda_imputacao_alternativas.csv', sep=';', index=False,
                     encoding='utf-8-sig')
print('\nsensibilidade das alternativas de imputação (renda_imputacao_alternativas.csv):')
print(sens.round(2).to_string(index=False))

