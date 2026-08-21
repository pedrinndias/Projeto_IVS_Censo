"""Rastreamento e classificação dos valores extremos de renda (`V06004`).

Por que este módulo existe
--------------------------
A renda do responsável é a componente do IVS com a distribuição mais torta
(assimetria 3,74 no recorte urbano). Os extremos dela não são todos da mesma
natureza: há **erro de dado** (o setor de favela com R$ 170 mil em Belo Horizonte),
há **extremo genuíno** (bairro rico de São Paulo) e há **setor pequeno com média
instável**. Tratar os três do mesmo jeito — excluindo todos ou mantendo todos —
perde informação nos dois sentidos.

Duas decisões de método
-----------------------
1. **A detecção é por município, não global.** O IVS é um índice *intraurbano*:
   compara setores dentro da mesma cidade. R$ 20 mil é um valor comum em São Paulo
   e uma anomalia em Autazes. Um corte global mede a distância entre cidades, que
   não é o objeto: ele marca 4,61% dos setores do Sudeste e só 1,32% dos do Norte —
   ou seja, encontra "anomalia" onde há riqueza, não onde há desvio local. O corte
   por município inverte isso (Norte 7,40%, Sudeste 2,22%), que é o retrato certo
   para um índice intraurbano. Os dois só coincidem em 1.673 dos ~4.000 setores que
   marcam juntos.

2. **Extremo suspeito ≠ extremo alto.** O que levanta suspeita não é o valor em si,
   mas a *incoerência* entre a renda declarada e o resto do perfil do setor. Um setor
   no topo da renda do município que também tem favela, analfabetismo acima da mediana
   local ou alta proporção de população preta, parda ou indígena é internamente
   contraditório — e é aí que mora o erro de dado.

Nada aqui remove observação. O módulo **rotula**; a decisão de excluir é de quem
analisa, e as duas versões da EDA (com e sem) ficam lado a lado para sustentá-la.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

COLUNA_RENDA = 'V06004'          # rendimento nominal médio mensal do responsável
K_TUKEY = 3.0                    # k=3 (outlier "extremo"); k=1.5 seria "moderado"
MIN_SETORES_MUNICIPIO = 20       # abaixo disso o quartil do município não é confiável

# Rótulos da coluna `classe_renda`, do mais grave ao benigno.
SUSPEITO = 'SUSPEITO'            # extremo E incoerente com o perfil do setor -> provável erro
EXTREMO = 'EXTREMO'              # extremo mas coerente -> renda alta de verdade
NORMAL = 'NORMAL'                # dentro da faixa do município


def limites_tukey(s: pd.Series, k: float = K_TUKEY) -> tuple[float, float]:
    """Limites inferior e superior de Tukey. `k=1.5` é o padrão do boxplot; `k=3` é o corte
    de outlier extremo, que é o que interessa aqui — não queremos rotular a cauda inteira."""
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


def rastrear_outliers_renda(df: pd.DataFrame, k: float = K_TUKEY) -> pd.DataFrame:
    """Rotula cada setor quanto à renda e devolve as colunas de rastreamento.

    Espera `df` com `V06004`, `CD_MUN`, e — para o teste de coerência — `CD_TIPO`,
    `pct_analfab` e `pct_raca_pretpardind` já calculados. Devolve um DataFrame com o
    mesmo índice de `df`.

    Colunas devolvidas:

    * `renda_p50_mun`, `renda_lim_sup_mun` — mediana e limite de Tukey do município
    * `razao_mediana_mun` — quantas vezes a renda do setor supera a mediana local;
      é a medida legível para o slide ("este setor tem 62× a mediana da cidade")
    * `outlier_global` / `outlier_municipio` — os dois critérios, para comparação
    * `incoerente` — o perfil do setor contradiz a renda declarada
    * `classe_renda` — SUSPEITO, EXTREMO ou NORMAL
    """
    renda = df[COLUNA_RENDA]
    saida = pd.DataFrame(index=df.index)

    # ── critério global, mantido só para comparação com o critério municipal ──
    lim_inf_g, lim_sup_g = limites_tukey(renda.dropna(), k)
    saida['outlier_global'] = renda.gt(lim_sup_g).fillna(False)

    # ── critério por município ────────────────────────────────────────────────
    g = renda.groupby(df['CD_MUN'])
    saida['renda_p50_mun'] = g.transform('median')
    n_mun = g.transform('size')
    lim_sup = g.transform(lambda s: limites_tukey(s.dropna(), k)[1])
    # municípios pequenos: o quartil é instável, então não se rotula por ele
    saida['renda_lim_sup_mun'] = lim_sup.where(n_mun >= MIN_SETORES_MUNICIPIO)
    saida['razao_mediana_mun'] = renda / saida['renda_p50_mun'].replace(0, np.nan)
    saida['outlier_municipio'] = renda.gt(saida['renda_lim_sup_mun']).fillna(False)

    # ── coerência: o resto do perfil do setor sustenta essa renda? ────────────
    # Cada teste compara o setor com o próprio município, não com o país.
    testes = pd.DataFrame(index=df.index)
    if 'CD_TIPO' in df.columns:
        testes['e_favela'] = df['CD_TIPO'].astype(str).eq('1')
    for col, quantil in [('pct_analfab', 0.5), ('pct_raca_pretpardind', 0.75)]:
        if col in df.columns:
            ref = df.groupby('CD_MUN')[col].transform(lambda s: s.quantile(quantil))
            testes[f'{col}_acima'] = df[col].gt(ref).fillna(False)
    saida['incoerente'] = testes.any(axis=1) if len(testes.columns) else False
    saida['motivos'] = (
        testes.apply(lambda linha: ' + '.join(c for c in testes.columns if linha[c]), axis=1)
        if len(testes.columns) else ''
    )

    # ── classificação final ───────────────────────────────────────────────────
    saida['classe_renda'] = np.select(
        [saida['outlier_municipio'] & saida['incoerente'], saida['outlier_municipio']],
        [SUSPEITO, EXTREMO],
        default=NORMAL,
    )
    saida.loc[renda.isna(), 'classe_renda'] = NORMAL   # sem renda não é outlier de renda
    return saida


def resumo_por_classe(df: pd.DataFrame, rastreio: pd.DataFrame) -> pd.DataFrame:
    """Quantos setores em cada classe, e o que eles representam em população e domicílios."""
    j = df.join(rastreio['classe_renda'])
    g = j.groupby('classe_renda')
    t = pd.DataFrame({
        'n_setores': g.size(),
        'pct_setores': (g.size() / len(j) * 100).round(3),
        'populacao': g['v0001'].sum(),
        'domicilios': g['V00001'].sum(),
        'renda_mediana': g[COLUNA_RENDA].median().round(2),
        'renda_media': g[COLUNA_RENDA].mean().round(2),
        'renda_max': g[COLUNA_RENDA].max().round(2),
    })
    return t.reindex([SUSPEITO, EXTREMO, NORMAL]).dropna(how='all')
