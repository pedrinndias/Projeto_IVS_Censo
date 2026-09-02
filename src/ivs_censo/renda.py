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

Três ressalvas que o resultado NÃO permite esconder
---------------------------------------------------
**A separação favela/não-favela entre as classes é definição, não achado.** `e_favela`
é um dos testes de incoerência, então todo setor de favela que for outlier municipal cai
obrigatoriamente em `SUSPEITO` e nenhum pode cair em `EXTREMO`. Dizer "nenhum dos
extremos coerentes é favela" é repetir a regra, não confirmá-la. O que a tabela mostra de
fato é *quantos* setores cada teste pegou — não que o teste esteja certo.

**O sinal do analfabetismo é fraco.** Estar acima da *mediana* do município é evento de
~50% por construção. Dos 66 suspeitos, 40 são flagrados só por esse teste. Eles merecem
inspeção individual antes de qualquer exclusão, não tratamento de bloco.

**Erro de dado em bairro rico é invisível para esta regra.** O setor `355030832000202`
(São Paulo, R$ 140.172,64 para 78 domicílios, 45× a mediana municipal) é o segundo maior
valor da base e sai classificado `EXTREMO`, porque o perfil do entorno é coerente com
renda alta. A regra detecta incoerência de contexto, não implausibilidade de magnitude.
Um segundo critério — razão sobre a mediana municipal acima de um limiar, sem depender do
perfil — pegaria esses casos.

Sobre "é só uma vírgula fora do lugar"
---------------------------------------
A leitura de que o valor de Belo Horizonte seria R$ 1.704 (170.418,06 ÷ 100) é **hipótese
não confirmada**, e o próprio arquivo do IBGE tem como testá-la: `V06005` traz a variância
do rendimento no setor. Com ela, CV = √V06005 ÷ V06004:

    mediana nacional do CV: 0,78   |   P99: 2,53   |   P99,9: 8,12
    BH 310620005650366: 5,26       |   SP 355030832000202: 6,85
    Belém 150140255000432: 8,66    |   Recife 261160605200257: 10,77

Se apenas a média tivesse deslizado uma casa decimal, o CV de BH seria ~526. Ele é 5,26:
a variância publicada é **coerente com a média alta**. Ou seja, o dado do IBGE não diz
"erro de digitação" — diz que o setor tem uma ou poucas declarações enormes puxando a
média. É uma afirmação mais defensável e de consequência diferente: não se corrige
dividindo por 100 nem se resolve excluindo 66 setores; argumenta-se por estatística
robusta (posto, log, mediana) para toda a variável.

`V06001` (nº de responsáveis) e `V06005` estão no mesmo CSV e passaram a ser extraídos
por causa disso. `V06006` (rendimento mediano) aparece no dicionário do IBGE mas **não
existe** nesta versão do arquivo — conferido no cabeçalho.

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
    * `cv_renda` — √V06005 ÷ V06004, quando a variância está disponível; mede o quanto a
      média do setor depende de poucas declarações (mediana nacional 0,78)
    * `razao_implausivel` — a renda supera `RAZAO_IMPLAUSIVEL` × a mediana do município,
      **independentemente** do perfil do entorno
    * `classe_renda` — SUSPEITO, EXTREMO ou NORMAL

    `razao_implausivel` é diagnóstico, **não** entra na classificação. É de propósito: a
    classificação em três classes já foi apresentada à orientadora, e trocar a regra por
    conta própria mudaria números que ela já viu. A coluna existe para mostrar o ponto
    cego — setor implausível por magnitude mas coerente por contexto sai como `EXTREMO` —
    e a decisão de promovê-la a critério é dela, não deste módulo.
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

    # ── diagnóstico de magnitude, sem depender do perfil do entorno ───────────
    # O teste de coerência não enxerga erro de dado em bairro rico: lá o entorno sustenta
    # a renda alta e o setor sai como EXTREMO. Estas duas colunas são o contrapeso.
    saida['razao_implausivel'] = saida['razao_mediana_mun'].gt(RAZAO_IMPLAUSIVEL).fillna(False)
    if COLUNA_VARIANCIA in df.columns:
        saida['cv_renda'] = np.sqrt(df[COLUNA_VARIANCIA]) / renda.replace(0, np.nan)
    else:
        saida['cv_renda'] = np.nan

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
