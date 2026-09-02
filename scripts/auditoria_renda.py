"""Rastreia os valores extremos de renda e roda a EDA duas vezes: com e sem eles.

Demandas da orientadora (ago/2026), itens 1, 1.1, 2, 4 e 7:

* **1** — identificar *todos* os extremos de renda, com município, setor censitário e
  se é favela; não só o de R$ 170 mil;
* **1.1** — duas análises exploratórias, uma com e outra sem esses setores, e a
  comparação entre elas;
* **2** — deixar o rastreamento de renda alta em setor pequeno à mostra na EDA;
* **4** — olhar os extremos do Sudeste e do Norte.

A regra de classificação vive em `src/ivs_censo/renda.py` — este script só a aplica
ao recorte urbano elegível e escreve as tabelas.

O que sai em `banco_de_dados/eda/`:

    renda_outliers_rastreados.csv       um por setor extremo, com identificação completa
    renda_classes_resumo.csv            quantos setores, população e domicílios por classe
    renda_criterio_global_vs_municipal.csv   por que o critério intraurbano é outro
    renda_eda_com_vs_sem.csv            descritivas das 7 componentes nas duas versões
    renda_correlacao_com_vs_sem.csv     correlações nas duas versões
    renda_normalizacao_impacto.csv      efeito na escala min-max, por município
    renda_setores_pequenos.csv          renda por faixa de tamanho do setor
    renda_extremos_por_regiao.csv       Sudeste e Norte lado a lado

Uso:
    ./.venv/bin/python scripts/auditoria_renda.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from ivs_censo import (INDICADORES_IVS, calcular_indicadores,        # noqa: E402
                       classificar_dados_sig, encontrar_raiz)
from ivs_censo.renda import (COLUNA_RENDA, EXTREMO, K_TUKEY, NORMAL,  # noqa: E402
                             SUSPEITO, rastrear_outliers_renda, resumo_por_classe)

COLS_TEXTO = ['CD_SETOR', 'CD_UF', 'CD_MUN', 'NM_MUN', 'NM_BAIRRO',
              'SITUACAO', 'CD_SIT', 'CD_TIPO', 'CD_FCU', 'NM_FCU',
              'Moradia_Predominante']
INDICADORES = [ind.nome for ind in INDICADORES_IVS]
ORDEM_REGIAO = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

# Faixas de tamanho do setor (demanda 2). O corte em 50 domicílios é o que a
# orientadora chama de "setor pequeno"; abaixo disso a média de renda se apoia em
# poucas declarações e oscila muito.
FAIXAS_DOM = [0, 50, 100, 200, 400, np.inf]
ROTULOS_DOM = ['1 a 50', '51 a 100', '101 a 200', '201 a 400', 'mais de 400']


def carregar(raiz: Path) -> pd.DataFrame:
    """Base do Notebook 01 -> recorte urbano elegível, com os 7 indicadores calculados."""
    base = raiz / 'banco_de_dados' / 'Base_ELSI_Bruta_Censo2022.csv'
    if not base.exists():
        raise SystemExit(f'Base não encontrada: {base}\nRode antes o Notebook 01 da Fase 3.')
    df = pd.read_csv(base, sep=';', dtype=str)
    cols_num = [c for c in df.columns if c not in COLS_TEXTO]
    df[cols_num] = df[cols_num].replace({'X': None, 'x': None})
    df[cols_num] = df[cols_num].apply(lambda c: c.astype(str).str.replace(',', '.', regex=False))
    df[cols_num] = df[cols_num].apply(pd.to_numeric, errors='coerce')
    df['Dados_sig'] = classificar_dados_sig(df)
    ref = pd.read_csv(raiz / 'dados' / 'municipios_elsi_brasil.csv', sep=';', dtype=str)
    df['regiao'] = df['CD_UF'].map(dict(zip(ref['uf_codigo'].str.zfill(2), ref['regiao'])))

    ok = df[(df['Dados_sig'] == 'OK') & (df['SITUACAO'] == 'Urbana')].copy()
    ok[INDICADORES] = calcular_indicadores(ok, INDICADORES_IVS)
    print(f'Recorte urbano elegível: {len(ok):,} setores em {ok["CD_MUN"].nunique()} municípios')
    return ok


def tabela_rastreamento(ok: pd.DataFrame, r: pd.DataFrame) -> pd.DataFrame:
    """Um registro por setor extremo, com tudo que identifica o caso (demanda 1)."""
    marcados = r['classe_renda'].isin([SUSPEITO, EXTREMO])
    t = pd.concat([
        ok.loc[marcados, ['CD_SETOR', 'NM_MUN', 'CD_MUN', 'NM_BAIRRO', 'regiao', 'CD_TIPO',
                          'NM_FCU', COLUNA_RENDA, 'V00001', 'v0001',
                          'pct_analfab', 'pct_raca_pretpardind']],
        r.loc[marcados, ['classe_renda', 'renda_p50_mun', 'razao_mediana_mun',
                         'renda_lim_sup_mun', 'outlier_global', 'outlier_municipio',
                         'razao_implausivel', 'cv_renda', 'motivos']],
    ], axis=1)
    t['e_favela'] = t['CD_TIPO'].astype(str).eq('1').map({True: 'sim', False: 'não'})
    t = t.rename(columns={COLUNA_RENDA: 'renda_media_setor', 'V00001': 'n_domicilios',
                          'v0001': 'populacao'})
    t['renda_media_setor'] = t['renda_media_setor'].round(2)
    t['razao_mediana_mun'] = t['razao_mediana_mun'].round(1)
    t['renda_p50_mun'] = t['renda_p50_mun'].round(2)
    t['renda_lim_sup_mun'] = t['renda_lim_sup_mun'].round(2)
    for c in ['pct_analfab', 'pct_raca_pretpardind']:
        t[c] = t[c].round(4)
    t['cv_renda'] = t['cv_renda'].round(2)
    ordem = ['classe_renda', 'CD_SETOR', 'NM_MUN', 'CD_MUN', 'NM_BAIRRO', 'regiao',
             'e_favela', 'NM_FCU', 'renda_media_setor', 'renda_p50_mun', 'razao_mediana_mun',
             'renda_lim_sup_mun', 'n_domicilios', 'populacao', 'pct_analfab',
             'pct_raca_pretpardind', 'outlier_global', 'outlier_municipio',
             'razao_implausivel', 'cv_renda', 'motivos']
    # SUSPEITO primeiro, e dentro de cada classe do valor mais absurdo para o menos.
    # Ordenar por `classe_renda` direto ordenava em ALFABÉTICA — EXTREMO, NORMAL,
    # SUSPEITO —, o que enterrava os 66 suspeitos no fim de 3.358 linhas, justamente as
    # linhas por causa das quais o arquivo existe.
    prioridade = {SUSPEITO: 0, EXTREMO: 1, NORMAL: 2}
    return (t[ordem]
            .assign(_ord=t['classe_renda'].map(prioridade))
            .sort_values(['_ord', 'razao_mediana_mun'], ascending=[True, False])
            .drop(columns='_ord')
            .reset_index(drop=True))


def tabela_criterios(ok: pd.DataFrame, r: pd.DataFrame) -> pd.DataFrame:
    """Global x municipal, por região — a demonstração de que não são o mesmo corte."""
    linhas = []
    for regiao in ORDEM_REGIAO:
        m = ok['regiao'] == regiao
        rg = r[m]
        n = int(m.sum())
        linhas.append({
            'regiao': regiao, 'n_setores': n,
            'outlier_global': int(rg['outlier_global'].sum()),
            'pct_global': round(rg['outlier_global'].mean() * 100, 2),
            'outlier_municipal': int(rg['outlier_municipio'].sum()),
            'pct_municipal': round(rg['outlier_municipio'].mean() * 100, 2),
            'concordam': int((rg['outlier_global'] & rg['outlier_municipio']).sum()),
            'so_global': int((rg['outlier_global'] & ~rg['outlier_municipio']).sum()),
            'so_municipal': int((~rg['outlier_global'] & rg['outlier_municipio']).sum()),
        })
    return pd.DataFrame(linhas)


def _descritivas(d: pd.DataFrame, rotulo: str) -> pd.DataFrame:
    """Média e mediana juntas — a distância entre elas é a medida da assimetria."""
    linhas = []
    for col in INDICADORES:
        s = d[col].dropna()
        linhas.append({
            'versao': rotulo, 'variavel': col, 'n': len(s),
            'media': s.mean(), 'mediana': s.median(), 'dp': s.std(),
            'p25': s.quantile(.25), 'p75': s.quantile(.75),
            'p99': s.quantile(.99), 'max': s.max(),
            'assimetria': s.skew(),
        })
    return pd.DataFrame(linhas)


def tabelas_com_vs_sem(ok: pd.DataFrame, r: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """As duas EDAs e a diferença entre elas (demanda 1.1).

    A versão "sem" retira apenas os SUSPEITO — os prováveis erros de dado. Os EXTREMO
    ficam: renda alta de verdade é informação, não ruído, e removê-la achataria a
    desigualdade que o índice existe para medir.
    """
    sem = ok[r['classe_renda'] != SUSPEITO]
    com_d, sem_d = _descritivas(ok, 'com_suspeitos'), _descritivas(sem, 'sem_suspeitos')

    dif = com_d.merge(sem_d, on='variavel', suffixes=('_com', '_sem'))
    for c in ['media', 'mediana', 'dp', 'p99', 'max', 'assimetria']:
        dif[f'delta_{c}'] = dif[f'{c}_sem'] - dif[f'{c}_com']
        dif[f'delta_{c}_pct'] = np.where(
            dif[f'{c}_com'].abs() > 1e-12,
            (dif[f'{c}_sem'] - dif[f'{c}_com']) / dif[f'{c}_com'].abs() * 100, np.nan)
    cols = ['variavel', 'n_com', 'n_sem'] + [
        f'{c}_{v}' for c in ['media', 'mediana', 'dp', 'p99', 'max', 'assimetria']
        for v in ['com', 'sem']] + [
        f'delta_{c}_pct' for c in ['media', 'mediana', 'dp', 'p99', 'max', 'assimetria']]
    descritivas = dif[cols].round(6)

    # correlações nas duas versões, para os dois métodos
    linhas = []
    for metodo in ['pearson', 'spearman']:
        c_com = ok[INDICADORES].corr(method=metodo)['renda_media'].drop('renda_media')
        c_sem = sem[INDICADORES].corr(method=metodo)['renda_media'].drop('renda_media')
        # log só faz sentido em Pearson: em Spearman o rank já é invariante a monotônica
        c_log = (ok.assign(renda_media=np.log(ok['renda_media']))[INDICADORES]
                 .corr(method=metodo)['renda_media'].drop('renda_media'))
        for var in c_com.index:
            linhas.append({'metodo': metodo, 'variavel': var,
                           'com_suspeitos': round(c_com[var], 4),
                           'sem_suspeitos': round(c_sem[var], 4),
                           'delta': round(c_sem[var] - c_com[var], 4),
                           'com_renda_em_log': round(c_log[var], 4)})
    return {'renda_eda_com_vs_sem': descritivas,
            'renda_correlacao_com_vs_sem': pd.DataFrame(linhas)}


def tabela_normalizacao(ok: pd.DataFrame, r: pd.DataFrame) -> pd.DataFrame:
    """O que os suspeitos fazem com a escala min-max por município.

    É o insumo do IVS: se quase todos os setores caem no primeiro decil da escala, a
    renda deixa de discriminar dentro da cidade — que é exatamente o que o índice
    precisa fazer.
    """
    sem_classe = r['classe_renda']
    linhas = []
    for (cd_mun, nm_mun), g in ok.groupby(['CD_MUN', 'NM_MUN']):
        s_com = g[COLUNA_RENDA].dropna()
        s_sem = g.loc[sem_classe.loc[g.index] != SUSPEITO, COLUNA_RENDA].dropna()
        if len(s_sem) < 10 or s_com.max() == s_com.min():
            continue

        def _comprimidos(s):
            return ((s - s.min()) / (s.max() - s.min()) < 0.1).mean() * 100

        linhas.append({
            'CD_MUN': cd_mun, 'NM_MUN': nm_mun, 'regiao': g['regiao'].iloc[0],
            'n_setores': len(g), 'n_suspeitos': int((sem_classe.loc[g.index] == SUSPEITO).sum()),
            'renda_max_com': round(s_com.max(), 2), 'renda_max_sem': round(s_sem.max(), 2),
            'pct_1o_decil_com': round(_comprimidos(s_com), 1),
            'pct_1o_decil_sem': round(_comprimidos(s_sem), 1),
        })
    t = pd.DataFrame(linhas)
    t['ganho_pp'] = (t['pct_1o_decil_com'] - t['pct_1o_decil_sem']).round(1)
    return t.sort_values('ganho_pp', ascending=False).reset_index(drop=True)


def tabela_setores_pequenos(ok: pd.DataFrame, r: pd.DataFrame) -> pd.DataFrame:
    """Renda por faixa de tamanho do setor (demanda 2).

    A pergunta da orientadora é se os valores exorbitantes se concentram em setores
    pequenos. A tabela responde com o dado, não com a intuição: se a hipótese valesse,
    a faixa "1 a 50" teria p99 e taxa de suspeitos muito acima das demais.
    """
    faixa = pd.cut(ok['V00001'], bins=FAIXAS_DOM, labels=ROTULOS_DOM, right=True)
    j = ok.assign(faixa_dom=faixa, classe_renda=r['classe_renda'],
                  razao_mediana_mun=r['razao_mediana_mun'])
    g = j.groupby('faixa_dom', observed=False)
    t = pd.DataFrame({
        'n_setores': g.size(),
        'pct_da_base': (g.size() / len(j) * 100).round(2),
        'renda_mediana': g[COLUNA_RENDA].median().round(2),
        'renda_media': g[COLUNA_RENDA].mean().round(2),
        'renda_p99': g[COLUNA_RENDA].quantile(.99).round(2),
        'renda_max': g[COLUNA_RENDA].max().round(2),
        'cv': (g[COLUNA_RENDA].std() / g[COLUNA_RENDA].mean()).round(3),
        'n_suspeitos': g.apply(lambda d: int((d['classe_renda'] == SUSPEITO).sum()), include_groups=False),
        'n_extremos': g.apply(lambda d: int((d['classe_renda'] == EXTREMO).sum()), include_groups=False),
    })
    t['pct_suspeitos'] = (t['n_suspeitos'] / t['n_setores'] * 100).round(3)
    t['pct_extremos'] = (t['n_extremos'] / t['n_setores'] * 100).round(2)
    return t.reset_index()


def tabela_por_regiao(ok: pd.DataFrame, r: pd.DataFrame) -> pd.DataFrame:
    """Perfil dos extremos região a região (demanda 4)."""
    linhas = []
    for regiao in ORDEM_REGIAO:
        g = ok[ok['regiao'] == regiao]
        rg = r.loc[g.index]
        s = g[COLUNA_RENDA].dropna()
        n_susp = int((rg['classe_renda'] == SUSPEITO).sum())
        n_extr = int((rg['classe_renda'] == EXTREMO).sum())
        favela_extremos = g.loc[rg['classe_renda'].isin([SUSPEITO, EXTREMO]), 'CD_TIPO'].astype(str).eq('1')
        linhas.append({
            'regiao': regiao, 'n_setores': len(g),
            'renda_mediana': round(s.median(), 2), 'renda_media': round(s.mean(), 2),
            'razao_media_mediana': round(s.mean() / s.median(), 2),
            'assimetria': round(s.skew(), 2),
            'renda_p99': round(s.quantile(.99), 2), 'renda_max': round(s.max(), 2),
            'max_sobre_mediana': round(s.max() / s.median(), 1),
            'n_suspeitos': n_susp, 'pct_suspeitos': round(n_susp / len(g) * 100, 3),
            'n_extremos': n_extr, 'pct_extremos': round(n_extr / len(g) * 100, 2),
            'extremos_em_favela': int(favela_extremos.sum()),
            'pct_extremos_em_favela': round(favela_extremos.mean() * 100, 1) if len(favela_extremos) else np.nan,
        })
    return pd.DataFrame(linhas)


def main() -> None:
    raiz = encontrar_raiz(Path(__file__).resolve().parent)
    destino = raiz / 'banco_de_dados' / 'eda'
    ok = carregar(raiz)
    r = rastrear_outliers_renda(ok, k=K_TUKEY)

    tabelas = {
        'renda_outliers_rastreados': tabela_rastreamento(ok, r),
        'renda_classes_resumo': resumo_por_classe(ok, r).reset_index(),
        'renda_criterio_global_vs_municipal': tabela_criterios(ok, r),
        'renda_normalizacao_impacto': tabela_normalizacao(ok, r),
        'renda_setores_pequenos': tabela_setores_pequenos(ok, r),
        'renda_extremos_por_regiao': tabela_por_regiao(ok, r),
    }
    tabelas.update(tabelas_com_vs_sem(ok, r))

    for nome, tabela in tabelas.items():
        tabela.to_csv(destino / f'{nome}.csv', sep=';', index=False, encoding='utf-8-sig')
        print(f'  {nome}.csv  ({len(tabela)} linhas)')
    print(f'\n{len(tabelas)} tabelas gravadas em {destino}')

    figuras = destino / 'figuras'
    figuras.mkdir(exist_ok=True)
    figura_boxplot_cidades(ok, r, figuras)
    figura_tamanho_vs_renda(ok, r, figuras)



# ─────────────────────────────────────────────────────────────────────────────
# Figuras (demanda 3)
#
# Forma: 70 cidades num único boxplot é ilegível — passa do teto de categorias
# distinguíveis. A saída é small multiples por região, com as cidades ordenadas
# pela mediana. O eixo é logarítmico porque a renda tem assimetria 3,74: em escala
# linear as caixas de 60 das 70 cidades colapsam contra a margem esquerda.
#
# Cor: as caixas são neutras — a região já está codificada pelo painel, então
# pintar por região seria redundante. A única cor é o vermelho de status nos
# setores SUSPEITOS, que é o que a figura existe para mostrar. Extremos coerentes
# entram como círculo vazado neutro, sem cor própria.
# ─────────────────────────────────────────────────────────────────────────────
SURFACE = '#fcfcfb'
TINTA = '#0b0b0b'
TINTA_2 = '#52514e'
CRITICO = '#d03b3b'      # status "critical" — contraste 4,68 no fundo claro
GRADE = '#e3e2df'


def figura_boxplot_cidades(ok: pd.DataFrame, r: pd.DataFrame, destino: Path) -> None:
    """Distribuição da renda por cidade, em painéis por região."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    j = ok.assign(classe_renda=r['classe_renda'])
    # uma linha por cidade, ordenadas pela mediana dentro de cada região
    por_regiao = {}
    for regiao in ORDEM_REGIAO:
        g = j[j['regiao'] == regiao]
        ordem = g.groupby('NM_MUN')[COLUNA_RENDA].median().sort_values()
        por_regiao[regiao] = [(nm, g[g['NM_MUN'] == nm]) for nm in ordem.index]

    alturas = [len(v) for v in por_regiao.values()]
    fig, axes = plt.subplots(len(ORDEM_REGIAO), 1, figsize=(11, 0.30 * sum(alturas) + 4.2),
                             gridspec_kw={'height_ratios': alturas}, facecolor=SURFACE)

    for ax, regiao in zip(axes, ORDEM_REGIAO):
        cidades = por_regiao[regiao]
        dados = [g[COLUNA_RENDA].dropna() for _, g in cidades]
        ax.set_facecolor(SURFACE)
        bp = ax.boxplot(dados, vert=False, widths=0.62, showfliers=False,
                        patch_artist=True, tick_labels=[nm for nm, _ in cidades])
        for caixa in bp['boxes']:
            caixa.set(facecolor='#ffffff', edgecolor=TINTA_2, linewidth=0.9)
        for peca in ('whiskers', 'caps'):
            for art in bp[peca]:
                art.set(color=TINTA_2, linewidth=0.9)
        for mediana in bp['medians']:
            mediana.set(color=TINTA, linewidth=1.6)

        # pontos: extremos coerentes em círculo vazado, suspeitos em vermelho cheio
        for i, (_, g) in enumerate(cidades, start=1):
            ext = g.loc[g['classe_renda'] == EXTREMO, COLUNA_RENDA].dropna()
            sus = g.loc[g['classe_renda'] == SUSPEITO, COLUNA_RENDA].dropna()
            if len(ext):
                ax.scatter(ext, np.full(len(ext), i), s=9, facecolors='none',
                           edgecolors=TINTA_2, linewidths=0.6, alpha=0.55, zorder=3)
            if len(sus):
                ax.scatter(sus, np.full(len(sus), i), s=34, color=CRITICO,
                           edgecolors=SURFACE, linewidths=0.8, zorder=5)

        ax.set_xscale('log')
        # 300, não 400: o menor setor da base tem R$ 318,88 e o bigode inferior de
        # São Paulo chega a R$ 366,67 — com o limite em 400 ele saía cortado
        ax.set_xlim(300, 260_000)
        ax.grid(axis='x', color=GRADE, linewidth=0.7)
        ax.set_axisbelow(True)
        for lado in ('top', 'right', 'left'):
            ax.spines[lado].set_visible(False)
        ax.spines['bottom'].set_color(GRADE)
        ax.tick_params(axis='y', length=0, labelsize=7.5, colors=TINTA_2)
        ax.tick_params(axis='x', labelsize=8, colors=TINTA_2)
        ax.set_ylabel(regiao, fontsize=10, color=TINTA, rotation=0,
                      ha='right', va='center', labelpad=76, weight='bold')

    for ax in axes[:-1]:
        ax.set_xticklabels([])
    axes[-1].set_xlabel('Renda média do responsável no setor (R$, escala log)',
                        fontsize=9, color=TINTA_2)

    # legenda no nível da figura — dentro do painel ela cobria um setor suspeito
    marca_sus = axes[0].scatter([], [], s=34, color=CRITICO, edgecolors=SURFACE)
    marca_ext = axes[0].scatter([], [], s=9, facecolors='none', edgecolors=TINTA_2)
    n_sus = int((r['classe_renda'] == SUSPEITO).sum())
    n_ext = f'{int((r["classe_renda"] == EXTREMO).sum()):,}'.replace(',', '.')
    fig.legend([marca_sus, marca_ext],
               [f'Setor suspeito — extremo e incoerente com o perfil ({n_sus})',
                f'Extremo coerente ({n_ext})'],
               loc='upper center', bbox_to_anchor=(0.5, 0.982), ncol=2,
               fontsize=8.5, frameon=False, labelcolor=TINTA_2)

    fig.suptitle('Renda por cidade — 70 municípios do ELSI, setores urbanos elegíveis',
                 fontsize=13, color=TINTA, y=1.0, ha='center')
    fig.tight_layout(rect=[0, 0, 1, 0.978])
    fig.savefig(destino / 'renda_boxplot_por_cidade.png', dpi=150,
                bbox_inches='tight', facecolor=SURFACE)
    plt.close(fig)
    print('  renda_boxplot_por_cidade.png')


def figura_tamanho_vs_renda(ok: pd.DataFrame, r: pd.DataFrame, destino: Path) -> None:
    """Renda contra tamanho do setor (demanda 2) — a pergunta é se o extremo mora no pequeno."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    classe = r['classe_renda']
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=SURFACE,
                                  gridspec_kw={'width_ratios': [2, 1]})

    normal = classe == NORMAL
    ax.set_facecolor(SURFACE)
    ax.scatter(ok.loc[normal, 'V00001'], ok.loc[normal, COLUNA_RENDA],
               s=2, color=GRADE, alpha=0.6, linewidths=0, zorder=1)
    ext = classe == EXTREMO
    ax.scatter(ok.loc[ext, 'V00001'], ok.loc[ext, COLUNA_RENDA],
               s=11, facecolors='none', edgecolors=TINTA_2, linewidths=0.6, alpha=0.6, zorder=2)
    sus = classe == SUSPEITO
    ax.scatter(ok.loc[sus, 'V00001'], ok.loc[sus, COLUNA_RENDA],
               s=40, color=CRITICO, edgecolors=SURFACE, linewidths=0.8, zorder=4)
    ax.axvline(50, color=TINTA_2, linewidth=0.9, linestyle=(0, (4, 3)), zorder=3)
    ax.annotate('50 domicílios — o corte\nde "setor pequeno"', xy=(50, 700),
                xytext=(56, 620), fontsize=8, color=TINTA_2, va='center')
    ax.set_yscale('log'); ax.set_xscale('log')
    ax.set_xlabel('Domicílios no setor (V00001, escala log)', fontsize=9, color=TINTA_2)
    ax.set_ylabel('Renda média do responsável (R$, escala log)', fontsize=9, color=TINTA_2)
    ax.set_title('Onde estão os extremos', fontsize=11, color=TINTA, loc='left')
    ax.grid(color=GRADE, linewidth=0.7); ax.set_axisbelow(True)
    for lado in ('top', 'right'):
        ax.spines[lado].set_visible(False)
    for lado in ('bottom', 'left'):
        ax.spines[lado].set_color(GRADE)
    ax.tick_params(colors=TINTA_2, labelsize=8)

    # painel direito: a taxa de suspeitos por faixa — a resposta da demanda 2
    faixa = pd.cut(ok['V00001'], bins=FAIXAS_DOM, labels=ROTULOS_DOM, right=True)
    taxa = (pd.DataFrame({'faixa': faixa, 'sus': (classe == SUSPEITO).values})
            .groupby('faixa', observed=False)['sus'].mean() * 100)
    ax2.set_facecolor(SURFACE)
    barras = ax2.barh(range(len(taxa)), taxa.values, height=0.6, color=CRITICO, zorder=2)
    ax2.set_yticks(range(len(taxa)), taxa.index, fontsize=8.5, color=TINTA_2)
    ax2.invert_yaxis()
    for i, (b, v) in enumerate(zip(barras, taxa.values)):
        ax2.text(v + 0.008, i, f'{v:.3f}%'.replace('.', ','), va='center',
                 fontsize=8.5, color=TINTA_2)
    ax2.set_xlim(0, taxa.max() * 1.35)
    ax2.set_xlabel('% de setores suspeitos na faixa', fontsize=9, color=TINTA_2)
    ax2.set_title('A taxa de suspeita cai com o tamanho', fontsize=11, color=TINTA, loc='left')
    ax2.grid(axis='x', color=GRADE, linewidth=0.7); ax2.set_axisbelow(True)
    for lado in ('top', 'right', 'left'):
        ax2.spines[lado].set_visible(False)
    ax2.spines['bottom'].set_color(GRADE)
    ax2.tick_params(axis='x', colors=TINTA_2, labelsize=8)
    ax2.tick_params(axis='y', length=0)

    fig.tight_layout()
    fig.savefig(destino / 'renda_tamanho_do_setor.png', dpi=150,
                bbox_inches='tight', facecolor=SURFACE)
    plt.close(fig)
    print('  renda_tamanho_do_setor.png')

if __name__ == '__main__':
    main()
