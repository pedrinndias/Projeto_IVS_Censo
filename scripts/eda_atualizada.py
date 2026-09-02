"""Re-executa a EDA inteira com a renda sem o extremo de Belo Horizonte.

Por que este script existe
--------------------------
A coluna `renda_media_sem_extremo` (pedida em 01/09/2026) tira um valor da base. Dizer
"a EDA foi refeita" só vale se **todas** as tabelas forem recalculadas e comparadas com
as antigas — inclusive as que não deveriam mudar. É o teste mais direto de que a
exclusão fez o que se esperava e nada além disso.

Este arquivo cobre as tabelas que **não** são de renda (descritivas, outliers,
correlações, favelas, faltantes). As tabelas de renda saem de
`scripts/auditoria_renda.py --sem-extremo`, que é o mesmo código da rodada original
com outra coluna de entrada — nada foi duplicado.

A validação que sustenta o resto: rodando com a coluna ANTIGA, este script tem que
reproduzir número a número as tabelas que já estão em `banco_de_dados/eda/`. Se não
reproduzir, ele para. Só depois disso as tabelas novas significam alguma coisa.

Entrada:  banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.csv
Saída:    banco_de_dados/eda/atualizada/*.csv  +  comparacao_antes_depois.csv

Uso:
    ./.venv/bin/python scripts/eda_atualizada.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ivs_censo import encontrar_raiz                                    # noqa: E402
from ivs_censo.renda import SETORES_RENDA_EXCLUIDA                      # noqa: E402

RAIZ = encontrar_raiz(Path(__file__).resolve().parent)
EDA = RAIZ / 'banco_de_dados' / 'eda'
NOVA = EDA / 'atualizada'

RENDA_ANTIGA = 'renda_media'
RENDA_NOVA = 'renda_media_sem_extremo'

IVS7 = ['pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad', 'razao_moradores',
        'pct_analfab', 'renda_media', 'pct_raca_pretpardind']
# A matriz ampliada de agosto: as sete componentes mais as três descritivas que a
# orientadora pediu para testar como candidatas ao índice.
MATRIZ10 = IVS7 + ['pct_idoso_60mais', 'pct_crianca_0a4', 'pct_resp_feminino']
FCU12 = IVS7 + ['pct_moradia_convencional', 'pct_apartamento', 'pct_pop_0a14',
                'pct_idoso_60mais', 'iep_setor']
ORDEM_REGIAO = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']


def carregar() -> pd.DataFrame:
    """Recorte de análise (OK + urbano) a partir do entregável, com `regiao`."""
    caminho = (RAIZ / 'banco_de_dados' / 'entrega_orientadora'
               / 'Base_ELSI_70Municipios_Censo2022.csv')
    if not caminho.exists():
        raise SystemExit(f'Entregável não encontrado: {caminho}\n'
                         'Rode antes scripts/gerar_entrega_orientadora.py.')
    df = pd.read_csv(caminho, sep=';', encoding='utf-8-sig', low_memory=False,
                     dtype={'CD_SETOR': str, 'CD_UF': str, 'CD_MUN': str, 'CD_TIPO': str})
    ref = pd.read_csv(RAIZ / 'dados' / 'municipios_elsi_brasil.csv', sep=';', dtype=str)
    df['regiao'] = df['CD_UF'].map(dict(zip(ref['uf_codigo'].str.zfill(2), ref['regiao'])))
    ok = df[(df['Dados_sig'] == 'OK') & (df['urbano'] == 1)].copy()
    print(f'Recorte de análise: {len(ok):,} setores em {ok["CD_MUN"].nunique()} municípios')
    return ok


def _serie(ok: pd.DataFrame, var: str, renda: str) -> pd.Series:
    """A série de uma variável, trocando a renda pela coluna pedida."""
    col = renda if var == RENDA_ANTIGA else var
    return pd.to_numeric(ok[col], errors='coerce')


# ── as tabelas ──────────────────────────────────────────────────────────────

def descritivas_globais(ok: pd.DataFrame, renda: str) -> pd.DataFrame:
    linhas = {}
    for v in IVS7:
        s = _serie(ok, v, renda).dropna()
        q1, q3 = s.quantile(.25), s.quantile(.75)
        linhas[v] = {'n': float(len(s)), 'media': s.mean(), 'dp': s.std(),
                     'cv_pct': s.std() / s.mean() * 100, 'min': s.min(), 'p25': q1,
                     'mediana': s.median(), 'p75': q3, 'max': s.max(), 'iq': q3 - q1,
                     'assim': s.skew(), 'curt': s.kurtosis()}
    return pd.DataFrame(linhas).T.round(4)


def descritivas_por_regiao(ok: pd.DataFrame, renda: str) -> pd.DataFrame:
    linhas = []
    for reg, g in ok.groupby('regiao'):
        for v in sorted(IVS7):
            s = _serie(g, v, renda).dropna()
            linhas.append({'regiao': reg, 'variavel': v, 'n': float(len(s)),
                           'media': s.mean(), 'dp': s.std(), 'p25': s.quantile(.25),
                           'mediana': s.median(), 'p75': s.quantile(.75)})
    return pd.DataFrame(linhas)


def outliers(ok: pd.DataFrame, renda: str) -> pd.DataFrame:
    """Regra de Tukey com k=1,5 sobre a base inteira, mais o p95 — que é o critério
    apropriado onde q1 e mediana são zero e o IQR marca tudo como atípico."""
    linhas = {}
    for v in IVS7:
        s = _serie(ok, v, renda).dropna()
        q1, q3 = s.quantile(.25), s.quantile(.75)
        iq = q3 - q1
        lim_inf, lim_sup = q1 - 1.5 * iq, q3 + 1.5 * iq
        p95 = s.quantile(.95)
        # Empate no limite não é atipicidade. 39 setores têm esgoto = 1/22, que cai
        # EXATAMENTE sobre `lim_sup`; se a comparação for `>` crua, eles entram ou saem
        # conforme o último bit do float — o valor lido do CSV difere do calculado em
        # memória na 16ª casa. `np.isclose` faz o empate contar sempre para o mesmo lado.
        acima = (s > lim_sup) & ~np.isclose(s, lim_sup)
        abaixo = (s < lim_inf) & ~np.isclose(s, lim_inf)
        n_out = int(acima.sum() + abaixo.sum())
        linhas[v] = {'n_validos': len(s), 'q1': q1, 'q3': q3, 'iq': iq,
                     'lim_inf': lim_inf, 'lim_sup': lim_sup, 'n_outliers': n_out,
                     'pct_outliers': round(n_out / len(s) * 100, 2), 'p95': p95,
                     'n_acima_p95': int((s > p95).sum()),
                     'pct_acima_p95': round((s > p95).sum() / len(s) * 100, 2),
                     'iqr_nao_informativo': bool(s.median() == 0 and q1 == 0)}
    # from_dict(orient='index') em vez de DataFrame(...).T: a transposta devolve tudo
    # como `object` por causa da coluna booleana, e aí `select_dtypes('number')` volta
    # vazio — a tabela passava pela validação sem ser comparada, e aparecia como
    # "inalterada" por vacuidade.
    return pd.DataFrame.from_dict(linhas, orient='index')


def correlacoes(ok: pd.DataFrame, renda: str, metodo: str) -> pd.DataFrame:
    m = pd.DataFrame({v: _serie(ok, v, renda) for v in MATRIZ10})
    return m.corr(method=metodo).round(3)


def favelas_comparativo(ok: pd.DataFrame, renda: str) -> pd.DataFrame:
    fcu, resto = ok[ok['is_fcu'] == 1], ok[ok['is_fcu'] != 1]
    linhas = []
    for v in FCU12:
        a, b = _serie(fcu, v, renda).dropna(), _serie(resto, v, renda).dropna()
        linhas.append({'variavel': v, 'n_fcu': len(a), 'media_fcu': round(a.mean(), 4),
                       'mediana_fcu': round(a.median(), 4), 'n_nao_fcu': len(b),
                       'media_nao_fcu': round(b.mean(), 4),
                       'mediana_nao_fcu': round(b.median(), 4),
                       'razao_medias': round(a.mean() / b.mean(), 4) if b.mean() else np.nan})
    return pd.DataFrame(linhas)


def missing_por_municipio(ok: pd.DataFrame, renda: str) -> pd.DataFrame:
    linhas = []
    for mun, g in ok.groupby('NM_MUN'):
        linha = {'NM_MUN': mun}
        for v in IVS7:
            linha[v] = round(_serie(g, v, renda).isna().mean() * 100, 2)
        linhas.append(linha)
    return pd.DataFrame(linhas)


TABELAS = {
    'descritivas_globais': descritivas_globais,
    'descritivas_por_regiao': descritivas_por_regiao,
    'outliers': outliers,
    'correlacao_pearson': lambda ok, r: correlacoes(ok, r, 'pearson'),
    'correlacao_spearman': lambda ok, r: correlacoes(ok, r, 'spearman'),
    'favelas_fcu_comparativo_indicadores': favelas_comparativo,
    'missing_por_municipio': missing_por_municipio,
}
COM_INDICE = {'descritivas_globais', 'outliers', 'correlacao_pearson', 'correlacao_spearman'}


# ── validação: com a coluna antiga, tem que dar a tabela antiga ─────────────

def validar(ok: pd.DataFrame) -> None:
    """Sem isto, as tabelas novas não provam nada: podiam estar diferentes por bug."""
    print('\nValidação — recalculando com a coluna ANTIGA e conferindo contra a EDA atual:')
    problemas = []
    for nome, fn in TABELAS.items():
        novo = fn(ok, RENDA_ANTIGA)
        velho = pd.read_csv(EDA / f'{nome}.csv', sep=';', encoding='utf-8-sig',
                            index_col=0 if nome in COM_INDICE else None)
        if nome in COM_INDICE:
            novo_n = novo.select_dtypes('number')
            velho_n = velho.reindex(novo.index)[novo_n.columns].astype(float)
        else:
            chave = 'variavel' if 'variavel' in novo.columns else 'NM_MUN'
            ordem = [chave] + (['regiao'] if 'regiao' in novo.columns else [])
            novo_o = novo.sort_values(ordem).reset_index(drop=True)
            velho_o = velho.sort_values(ordem).reset_index(drop=True)
            novo_n = novo_o.select_dtypes('number')
            velho_n = velho_o[novo_n.columns].astype(float)
        if novo_n.empty:
            # comparação vazia não é comparação aprovada — foi assim que a tabela de
            # outliers passou sem ser conferida na primeira versão deste script
            print(f'  ✗ {nome:42s} nenhuma coluna numérica para comparar')
            problemas.append(nome)
            continue
        dif = (novo_n.astype(float) - velho_n.values).abs().max().max()
        ok_ = bool(dif < 0.01)
        print(f'  {"✓" if ok_ else "✗"} {nome:42s} maior diferença: {dif:.6f} '
              f'({novo_n.shape[0]}×{novo_n.shape[1]} células)')
        if not ok_:
            problemas.append(nome)
    if problemas:
        raise SystemExit(f'\nA recomputação NÃO reproduz a EDA atual em: {problemas}.\n'
                         'Corrigir antes de publicar qualquer número novo.')
    print('  todas reproduzidas — a recomputação é fiel à EDA publicada.')


# ── comparação antes × depois ──────────────────────────────────────────────

def comparar(ok: pd.DataFrame) -> pd.DataFrame:
    """Toda célula numérica das duas rodadas, lado a lado. É daqui que sai a lista de
    alterações do deck — e a prova de que os blocos sem renda ficaram intactos."""
    linhas = []
    for nome, fn in TABELAS.items():
        a, b = fn(ok, RENDA_ANTIGA), fn(ok, RENDA_NOVA)
        if nome in COM_INDICE:
            a, b = a.reset_index(), b.reset_index()
        chave = a.columns[0]
        for col in a.select_dtypes('number').columns:
            for i in range(len(a)):
                va, vb = a[col].iloc[i], b[col].iloc[i]
                if pd.isna(va) and pd.isna(vb):
                    continue
                if pd.isna(va) or pd.isna(vb) or abs(float(va) - float(vb)) > 1e-9:
                    linhas.append({'tabela': nome, 'linha': str(a[chave].iloc[i]),
                                   'coluna': col, 'antes': va, 'depois': vb,
                                   'delta': (float(vb) - float(va))
                                   if not (pd.isna(va) or pd.isna(vb)) else np.nan})
    return pd.DataFrame(linhas)


# ── figuras ────────────────────────────────────────────────────────────────
# Só as três que dependem da renda. As demais figuras de banco_de_dados/eda/figuras/
# continuam válidas: nenhuma variável delas mudou, e regerá-las produziria arquivos
# idênticos com data diferente.

def figuras(ok: pd.DataFrame, destino: Path) -> None:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    destino.mkdir(parents=True, exist_ok=True)

    # histogramas das 7 componentes
    fig, axes = plt.subplots(3, 3, figsize=(16, 12))
    for ax, v in zip(axes.flat, IVS7):
        s = _serie(ok, v, RENDA_NOVA).dropna()
        ax.hist(s, bins=50)
        ax.set_title(v if v != RENDA_ANTIGA else f'{RENDA_NOVA} (sem o extremo de BH)')
        ax.set_ylabel('frequência')
    for ax in axes.flat[len(IVS7):]:
        ax.axis('off')
    fig.suptitle('Histogramas — 7 variáveis-componente do IVS '
                 '(setores urbanos elegíveis, 70 municípios ELSI)', fontsize=14)
    fig.tight_layout()
    fig.savefig(destino / 'histogramas.png', dpi=110, bbox_inches='tight')
    plt.close(fig)

    # matriz de correlação, Pearson e Spearman lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(25, 11))
    for ax, metodo in zip(axes, ['pearson', 'spearman']):
        m = correlacoes(ok, RENDA_NOVA, metodo)
        im = ax.imshow(m.values, cmap='RdBu_r', vmin=-1, vmax=1)
        ax.set_xticks(range(len(m)), m.columns, rotation=45, ha='right')
        ax.set_yticks(range(len(m)), m.index)
        for i in range(len(m)):
            for j in range(len(m)):
                val = m.values[i, j]
                ax.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=9,
                        color='white' if abs(val) > 0.55 else 'black')
        ax.axhline(6.5, color='black', lw=1.2)      # separa as 7 do IVS das 3 descritivas
        ax.axvline(6.5, color='black', lw=1.2)
        ax.set_title(f'Correlação — {metodo.capitalize()}')
        fig.colorbar(im, ax=ax, shrink=0.82)
    fig.suptitle('Abaixo e à direita da linha preta: descritivas fora do IVS-7', y=0.02)
    fig.tight_layout()
    fig.savefig(destino / 'matriz_correlacao.png', dpi=110, bbox_inches='tight')
    plt.close(fig)

    # boxplots por região
    fig, axes = plt.subplots(3, 3, figsize=(16, 12))
    for ax, v in zip(axes.flat, IVS7):
        dados = [_serie(ok[ok['regiao'] == r], v, RENDA_NOVA).dropna() for r in ORDEM_REGIAO]
        ax.boxplot(dados, tick_labels=ORDEM_REGIAO, showfliers=False)
        ax.set_title(v if v != RENDA_ANTIGA else f'{RENDA_NOVA} (sem o extremo de BH)')
        ax.tick_params(axis='x', rotation=45)
    for ax in axes.flat[len(IVS7):]:
        ax.axis('off')
    fig.suptitle('Distribuição por região — 7 componentes do IVS', fontsize=14)
    fig.tight_layout()
    fig.savefig(destino / 'boxplots_por_regiao.png', dpi=110, bbox_inches='tight')
    plt.close(fig)

    print(f'  3 figuras em {destino}')


def main() -> None:
    ok = carregar()
    faltando = [c for c in (RENDA_ANTIGA, RENDA_NOVA) if c not in ok.columns]
    if faltando:
        raise SystemExit(f'Colunas ausentes no entregável: {faltando}')

    validar(ok)

    NOVA.mkdir(parents=True, exist_ok=True)
    print(f'\nRecalculando com {RENDA_NOVA} '
          f'({len(SETORES_RENDA_EXCLUIDA)} setor(es) excluído(s)):')
    for nome, fn in TABELAS.items():
        t = fn(ok, RENDA_NOVA)
        t.to_csv(NOVA / f'{nome}.csv', sep=';', encoding='utf-8-sig',
                 index=nome in COM_INDICE)
        print(f'  {nome}.csv ({len(t)} linhas)')

    figuras(ok, NOVA / 'figuras')

    cmp = comparar(ok)
    cmp.to_csv(NOVA / 'comparacao_antes_depois.csv', sep=';', index=False,
               encoding='utf-8-sig')

    print(f'\nCélulas que mudaram: {len(cmp)}')
    if len(cmp):
        print(cmp.groupby('tabela').size().to_string())
    intactas = sorted(set(TABELAS) - set(cmp['tabela'].unique() if len(cmp) else []))
    print(f'\nTabelas inalteradas ({len(intactas)}): {", ".join(intactas) or "nenhuma"}')
    print(f'\nSaídas em {NOVA}')


if __name__ == '__main__':
    main()
