"""Álgebra da análise fatorial do IVS, em numpy puro.

Este módulo é a matemática que o **Notebook 04** usa para estimar a estrutura latente
dos componentes do IVS e definir os pesos do índice. Ele nasce de
`scripts/diagnostico_fatorial.py` (24/08/2026), que fica sendo a interface de linha de
comando: as funções migraram para cá sem alteração de comportamento, para que o
notebook e o script partam do mesmo código — a mesma correção que o Notebook 02 sofreu
em 20/08/2026, quando as fórmulas duplicadas viraram `indicadores.py`.

O que veio do script, inalterado: `chi2_sf`, `bartlett`, `kmo`, `varimax`, `acp`,
`horn` e `diagnosticar`. Os CSVs em `banco_de_dados/eda/fatorial/` continuam sendo a
referência de conferência, e `tests/test_fatorial.py` verifica que ainda batem.

O que é novo, e por quê — cada item decorre de uma passagem de MATOS & RODRIGUES,
*Análise fatorial* (Enap, 2019), que o projeto adotou como referência metodológica
principal depois de Figueiredo & Silva (2010):

* `smc` — a p. 42 recomenda a *Squared Multiple Correlation* por variável como
  diagnóstico complementar de multicolinearidade, e fixa em 0,80 o limiar de
  correlação a partir do qual "fica inviável separar o peso delas em cada um dos
  fatores". No IVS, renda × cor/raça dá −0,811 em Spearman: está acima do limiar.
* `fatoracao_eixo_principal` — a p. 27 traz a advertência de Stevens (1992): com menos
  de 20 variáveis e comunalidades abaixo de 0,4, ACP e análise fatorial podem divergir.
  O IVS tem 6 variáveis e comunalidade mínima de 0,380 na solução sem o lixo, de modo
  que a equivalência entre as duas técnicas deixou de ser pressuposto e virou hipótese
  a testar.
* `rotacao_promax` — a p. 38 afirma que rotação ortogonal em Ciências Humanas "não
  parece ter nenhum sentido" sem evidência forte de que os fatores sejam
  independentes. A Varimax herdada de Figueiredo passa a ser o caminho que exige prova.
  A rotação oblíqua produz, além disso, a matriz de correlação entre os fatores — uma
  evidência de validação que a solução ortogonal, por construção, não pode dar.
* `escores_regressao` — a p. 23 classifica a média ponderada pelas cargas (o plano
  atual do IVS) como método "não refinado" e instável, e ensina o método da regressão
  como alternativa refinada.
* `bootstrap_cargas` — não está em nenhuma das duas referências. É a resposta direta à
  crítica de instabilidade da p. 23: com 87 mil setores, mil reamostragens dão
  intervalo de confiança para cada carga e para a repartição do peso entre as
  dimensões.

**Restrição de projeto:** apenas `numpy` e `pandas`. Nada aqui exige scipy, sklearn ou
factor_analyzer — é tudo álgebra linear. O `requirements.txt` não cresce.

**Convenção de sinal:** o sinal de um autovetor é arbitrário. As funções devolvem o que
o LAPACK devolve, sem normalizar; quem interpreta é que decide o sentido ("carga
positiva = mais vulnerável") e inverte a coluna inteira. Os CSVs de referência guardam
o sinal cru.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

# Os 7 componentes do IVS. A renda entra invertida (−renda) para que todas as variáveis
# apontem no mesmo sentido: valor maior = mais vulnerável. A inversão não muda |r|,
# autovalores, KMO nem comunalidades — muda só o sinal das cargas, e por isso a leitura.
IVS7 = ['pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad', 'razao_moradores',
        'pct_analfab', 'renda_media', 'pct_raca_pretpardind']
ROTULOS = {
    'pct_agua_inad': 'Água inadequada',
    'pct_esgoto_inad': 'Esgoto inadequado',
    'pct_lixo_inad': 'Lixo inadequado',
    'razao_moradores': 'Razão de moradores',
    'pct_analfab': 'Analfabetismo 15+',
    'renda_inv': 'Renda (invertida)',
    'pct_raca_pretpardind': 'Cor/raça PPI',
}


# ─────────────────────────────────────────────────────────────────────────────
# Adequabilidade da base (Etapa 1 do livro, p. 39-46)
# ─────────────────────────────────────────────────────────────────────────────
def chi2_sf(x: float, k: int) -> float:
    """Cauda superior da qui-quadrado por Wilson–Hilferty (exata o bastante com df alto)."""
    z = ((x / k) ** (1 / 3) - (1 - 2 / (9 * k))) / math.sqrt(2 / (9 * k))
    return 0.5 * math.erfc(z / math.sqrt(2))


def bartlett(R: np.ndarray, n: int) -> tuple[float, int, float]:
    """BTS: testa H0 de que a matriz de correlação é a identidade.

    Leia o resultado com a ressalva da p. 43: o teste "depende muito do tamanho
    amostral e tende a rejeitar a hipótese nula para amostras grandes". Com 87 mil
    setores ele rejeita H0 por construção, e a conclusão de adequabilidade tem de se
    apoiar no KMO e nos MSA individuais, que não crescem com o n.
    """
    p = R.shape[0]
    sinal, logdet = np.linalg.slogdet(R)
    # Matriz não positiva definida devolve sinal <= 0 e logdet infinito ou nulo — e daí
    # sai um qui-quadrado sem significado, que iria para o CSV como se fosse número. Uma
    # matriz de Spearman com muitos empates, ou montada por exclusão par a par, pode cair
    # nesse caso. Melhor parar aqui do que publicar o resultado.
    if sinal <= 0 or not np.isfinite(logdet):
        raise ValueError('matriz de correlação não é positiva definida: '
                         f'sinal do determinante = {sinal}, log|R| = {logdet}')
    qui = -(n - 1 - (2 * p + 5) / 6) * logdet
    gl = p * (p - 1) // 2
    return qui, gl, chi2_sf(qui, gl)


def kmo(R: np.ndarray) -> tuple[float, np.ndarray]:
    """KMO global e MSA por variável, a partir das correlações parciais (anti-imagem)."""
    Rinv = np.linalg.inv(R)
    d = np.sqrt(np.diag(Rinv))
    parcial = -Rinv / np.outer(d, d)          # correlações parciais
    np.fill_diagonal(parcial, 0.0)
    R0 = R.copy()
    np.fill_diagonal(R0, 0.0)
    soma_r, soma_p = (R0 ** 2).sum(), (parcial ** 2).sum()
    msa = (R0 ** 2).sum(axis=0) / ((R0 ** 2).sum(axis=0) + (parcial ** 2).sum(axis=0))
    return soma_r / (soma_r + soma_p), msa


def smc(R: np.ndarray) -> np.ndarray:
    """*Squared Multiple Correlation* por variável: 1 − 1/diag(R⁻¹).

    Quanto da variabilidade de cada variável as demais explicam. O livro (p. 42, citando
    Yong & Pearce, 2013) usa a SMC como estimativa inicial da comunalidade e como
    diagnóstico: SMC perto de zero indica variável independente das outras — candidata a
    sair; SMC perto de um indica redundância — o lado da multicolinearidade.
    """
    return 1.0 - 1.0 / np.diag(np.linalg.inv(R))


# ─────────────────────────────────────────────────────────────────────────────
# Extração (Etapa 2 do livro, p. 32-34)
# ─────────────────────────────────────────────────────────────────────────────
def acp(R: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    """Componentes principais a partir da matriz de correlação: autovalores e cargas."""
    val, vec = np.linalg.eigh(R)
    ordem = np.argsort(val)[::-1]
    val, vec = val[ordem], vec[:, ordem]
    cargas = vec[:, :k] * np.sqrt(np.maximum(val[:k], 0))
    return val, cargas


def fatoracao_eixo_principal(R: np.ndarray, k: int, tol: float = 1e-7,
                             maxiter: int = 1000,
                             teto_comunalidade: float = 0.999
                             ) -> tuple[np.ndarray, np.ndarray, dict]:
    """Fatoração do eixo principal: ACP iterada com as comunalidades na diagonal.

    A diferença entre AF e ACP é o que entra na diagonal da matriz decomposta. A ACP usa
    1 — toda a variância de cada variável. A análise fatorial propriamente dita usa só a
    variância **compartilhada**, estimada pela comunalidade (p. 26-27). Como a
    comunalidade só se conhece depois de extrair os fatores, o método itera: começa pela
    SMC, extrai, recalcula, repõe na diagonal, repete.

    O teto em `teto_comunalidade` trata o caso de Heywood — comunalidade estimada acima
    de 1, que não tem sentido (implicaria variância residual negativa) e costuma indicar
    fatores demais extraídos. Quando ele é acionado, `info['heywood']` fica `True`: é
    resultado a reportar, não detalhe de implementação.

    Devolve `(cargas, comunalidades, info)`, com `info` trazendo `convergiu`, `iteracoes`,
    `delta` (a maior variação de comunalidade na última iteração) e `heywood`.
    """
    p = R.shape[0]
    Rr = R.copy().astype(float)
    h = np.clip(smc(R), 0.0, teto_comunalidade)   # estimativa inicial (p. 42)
    heywood = False
    convergiu = False
    delta = np.inf
    it = 0
    cargas = np.zeros((p, k))
    val = np.zeros(p)
    for it in range(1, maxiter + 1):
        np.fill_diagonal(Rr, h)
        val, vec = np.linalg.eigh(Rr)
        ordem = np.argsort(val)[::-1]
        val, vec = val[ordem], vec[:, ordem]
        cargas = vec[:, :k] * np.sqrt(np.maximum(val[:k], 0))
        h_novo = (cargas ** 2).sum(axis=1)
        if (h_novo > teto_comunalidade).any():
            heywood = True
            h_novo = np.minimum(h_novo, teto_comunalidade)
        delta = float(np.abs(h_novo - h).max())
        h = h_novo
        if delta < tol:
            convergiu = True
            break
    info = {'convergiu': convergiu, 'iteracoes': it, 'delta': delta,
            'heywood': heywood, 'autovalores': val, 'p': p}
    return cargas, h, info


def horn(n: int, p: int, sims: int = 50, semente: int = 42) -> np.ndarray:
    """Análise paralela de Horn (1965): autovalores médios de dados aleatórios n × p.

    Critério de retenção mais robusto que o de Kaiser, e ausente do livro da Enap — está
    em nota de rodapé em Figueiredo & Silva (2010). Reter só os fatores cujo autovalor
    supera o que dados sem estrutura nenhuma produziriam.
    """
    rng = np.random.default_rng(semente)
    acc = np.zeros(p)
    for _ in range(sims):
        X = rng.standard_normal((n, p))
        acc += np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]
    return acc / sims


# ─────────────────────────────────────────────────────────────────────────────
# Rotação (Etapa 3 do livro, p. 34-39)
# ─────────────────────────────────────────────────────────────────────────────
def varimax(cargas: np.ndarray, tol: float = 1e-10, maxiter: int = 10_000) -> np.ndarray:
    """Rotação ortogonal Varimax (Kaiser), sem normalização.

    Mantida por reprodutibilidade — é o que gerou os CSVs de referência — e como termo de
    comparação. Para a solução oficial, ver `rotacao_promax` e a p. 38.

    Parada pela variação da própria rotação R (não pela razão de valores singulares,
    que estabilizava cedo demais e deixava erro de 5,5e-4 nas cargas em 6 variáveis).
    """
    L = cargas.copy()
    p, k = L.shape
    if k < 2:
        return L
    R = np.eye(k)
    for _ in range(maxiter):
        R_ant = R
        Lam = L @ R
        u, s, vt = np.linalg.svd(
            L.T @ (Lam ** 3 - Lam @ np.diag(np.diag(Lam.T @ Lam)) / p))
        R = u @ vt
        if np.max(np.abs(R - R_ant)) < tol:
            break
    return L @ R


def rotacao_promax(cargas: np.ndarray, kappa: int = 4,
                   tol: float = 1e-6, maxiter: int = 500
                   ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Rotação oblíqua promax (Hendrickson & White, 1964).

    Varimax seguida de uma transformação oblíqua ajustada por mínimos quadrados a um
    alvo `sinal(v)·|v|^kappa`, que exagera o contraste entre cargas altas e baixas e
    assim permite que os eixos se inclinem para onde as variáveis realmente estão. O
    livro (p. 38) nomeia `oblimin` como a oblíqua geralmente mais indicada e `promax`
    como a alternativa rápida para bases muito grandes — que é o caso aqui, com 87 mil
    setores.

    Devolve três coisas, e a distinção entre as duas primeiras importa (p. 21-22):

    * **padrão** — coeficientes de regressão da variável no fator. É a matriz que a maior
      parte dos pesquisadores interpreta, e é dela que saem os pesos do índice.
    * **estrutura** — correlações entre variáveis e fatores (padrão · Φ).
    * **Φ** — a matriz de correlação entre os fatores, com diagonal unitária. Não existe
      na solução ortogonal, e é a evidência de validação que o projeto hoje não tem.

    Com fatores correlacionados uma carga padrão pode passar de 1 sem ser erro, por ser
    coeficiente de regressão (p. 22). Se isso acontecer, o teste é a variância residual da
    variável: `1 − diag(padrão·Φ·padrãoᵀ)`. Negativa, a solução é inadmissível e sugere
    fatores demais. Use `comunalidades_obliquas` para esse cheque.
    """
    V = varimax(cargas, tol=tol, maxiter=maxiter)
    k = V.shape[1]
    if k < 2:
        return V, V.copy(), np.eye(k)
    alvo = np.sign(V) * np.abs(V) ** kappa          # sinal(v)·|v|^kappa
    U, *_ = np.linalg.lstsq(V, alvo, rcond=None)    # U = (VᵀV)⁻¹Vᵀ·alvo
    # Escala as colunas de U para que inv(UᵀU) tenha diagonal 1 — é o que faz Φ ser uma
    # matriz de correlação, e não apenas de covariância entre fatores.
    d = np.diag(np.linalg.inv(U.T @ U))
    U = U @ np.diag(np.sqrt(d))
    padrao = V @ U
    phi = np.linalg.inv(U.T @ U)
    estrutura = padrao @ phi
    return padrao, estrutura, phi


def comunalidades_obliquas(padrao: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """Comunalidade numa solução oblíqua: diag(padrão·Φ·padrãoᵀ).

    Ao contrário do caso ortogonal, não é a soma dos quadrados das cargas — parte da
    variância é compartilhada entre os fatores correlacionados e seria contada duas
    vezes. `1 − esta comunalidade` é a variância residual do teste da p. 22.
    """
    return np.einsum('ij,jk,ik->i', padrao, phi, padrao)


# ─────────────────────────────────────────────────────────────────────────────
# Escores fatoriais (p. 22-26)
# ─────────────────────────────────────────────────────────────────────────────
def escores_regressao(R: np.ndarray, cargas: np.ndarray) -> np.ndarray:
    """Coeficientes do método da regressão: B = R⁻¹A.

    Aplicados às variáveis **padronizadas** (Z @ B), dão os escores fatoriais pelo método
    refinado que o livro recomenda na p. 25, em oposição à média ponderada pelas cargas,
    que ele classifica como "não refinada" e instável (p. 23).

    Uma propriedade útil para testar a implementação: quando `cargas` vêm de uma ACP
    (`acp`), com ou sem rotação ortogonal depois, os escores resultantes têm variância
    exatamente 1 — porque B se reduz a Vₖ·Λₖ^(−1/2). Com cargas de fatoração do eixo
    principal isso não vale: a variância cai abaixo de 1 e o que ela mede é a
    determinação do escore, isto é, o quadrado da correlação entre o escore estimado e o
    fator que ele estima.
    """
    return np.linalg.solve(R, cargas)


# ─────────────────────────────────────────────────────────────────────────────
# Correlação e estabilidade
# ─────────────────────────────────────────────────────────────────────────────
def postos(X: np.ndarray) -> np.ndarray:
    """Postos por coluna, com média nos empates — o mesmo que o pandas usa no Spearman.

    Existe para que o bootstrap não precise passar por `DataFrame.corr` mil vezes. Os
    empates são muitos: as proporções de saneamento têm massa concentrada em zero.
    """
    X = np.asarray(X, dtype=float)
    if not np.isfinite(X).all():
        # `argsort` joga NaN para o fim e o posto sairia como se fosse o maior valor —
        # uma matriz de correlação plausível e errada, que é o pior defeito possível aqui.
        # O projeto trata faltante por exclusão de casos antes de chegar na álgebra; se
        # chegou faltante até aqui, é engano de quem chamou.
        raise ValueError('há valores ausentes ou infinitos: trate-os antes '
                         '(o projeto usa exclusão por lista) — o posto de NaN não existe')
    n = X.shape[0]
    saida = np.empty_like(X)
    for j in range(X.shape[1]):
        x = X[:, j]
        ordem = np.argsort(x, kind='mergesort')
        xs = x[ordem]
        novo = np.r_[True, xs[1:] != xs[:-1]]      # início de cada grupo de empate
        grupo = novo.cumsum() - 1                  # índice do grupo de cada posição
        limites = np.r_[np.nonzero(novo)[0], n]    # posições onde cada grupo começa/termina
        medias = 0.5 * (limites[grupo] + limites[grupo + 1] + 1)
        saida[ordem, j] = medias
    return saida


def matriz_correlacao(X: np.ndarray, metodo: str = 'spearman') -> np.ndarray:
    """Matriz de correlação de uma matriz n × p, por Pearson ou Spearman."""
    if metodo == 'spearman':
        X = postos(X)
    elif metodo != 'pearson':
        raise ValueError(f"método desconhecido: {metodo!r} (use 'spearman' ou 'pearson')")
    return np.corrcoef(X, rowvar=False)


def alinhar_cargas(cargas: np.ndarray, referencia: np.ndarray) -> np.ndarray:
    """Põe as colunas de `cargas` na ordem e no sinal de `referencia`.

    Sem isso o bootstrap não significa nada: a cada reamostragem o LAPACK pode devolver
    os fatores em outra ordem ou com o sinal trocado, e a média das cargas ficaria perto
    de zero por cancelamento — um artefato que pareceria instabilidade.
    """
    k = cargas.shape[1]
    saida = np.zeros_like(cargas)
    livres = list(range(k))
    for j in range(k):
        # entre as colunas ainda não usadas, a de maior congruência absoluta com a j-ésima
        # coluna da referência
        pontos = [abs(float(cargas[:, c] @ referencia[:, j])) for c in livres]
        escolhida = livres.pop(int(np.argmax(pontos)))
        coluna = cargas[:, escolhida]
        if coluna @ referencia[:, j] < 0:
            coluna = -coluna
        saida[:, j] = coluna
    return saida


def bootstrap_cargas(X: np.ndarray, k: int, n_rep: int = 1000, seed: int = 42,
                     metodo: str = 'spearman', rotacao: str = 'varimax',
                     ) -> dict:
    """Intervalo de confiança das cargas e da repartição dos pesos, por reamostragem.

    Reamostra os setores com reposição, refaz a matriz de correlação, a extração e a
    rotação, e alinha cada solução à da amostra completa antes de acumular. Responde à
    crítica de instabilidade da p. 23 com um número em vez de uma opinião.

    `rotacao` aceita `'varimax'` (ortogonal) ou `'promax'` (oblíqua, devolve a matriz
    padrão). A repartição do peso entre as dimensões é a soma dos quadrados das cargas de
    cada fator sobre o total — a mesma conta que produziu o 65/35 da solução ortogonal.

    Devolve as cargas e a repartição da amostra completa, os percentis 2,5 e 97,5 de cada
    uma sobre as reamostragens, e as matrizes completas para quem quiser outro percentil.
    """
    X = np.asarray(X, dtype=float)
    n = X.shape[0]

    def solucao(dados: np.ndarray) -> np.ndarray:
        R = matriz_correlacao(dados, metodo)
        _, cargas = acp(R, k)
        if rotacao == 'varimax':
            return varimax(cargas)
        if rotacao == 'promax':
            return rotacao_promax(cargas)[0]
        raise ValueError(f"rotação desconhecida: {rotacao!r}")

    def repartir(cargas: np.ndarray) -> np.ndarray:
        ss = (cargas ** 2).sum(axis=0)
        return ss / ss.sum()

    ref = solucao(X)
    rng = np.random.default_rng(seed)
    cargas_rep = np.empty((n_rep,) + ref.shape)
    pesos_rep = np.empty((n_rep, k))
    for i in range(n_rep):
        amostra = X[rng.integers(0, n, size=n)]
        alinhada = alinhar_cargas(solucao(amostra), ref)
        cargas_rep[i] = alinhada
        pesos_rep[i] = repartir(alinhada)

    return {
        'cargas': ref,
        'cargas_ic': (np.percentile(cargas_rep, 2.5, axis=0),
                      np.percentile(cargas_rep, 97.5, axis=0)),
        'cargas_reamostragens': cargas_rep,
        'repartição': repartir(ref),
        'repartição_ic': (np.percentile(pesos_rep, 2.5, axis=0),
                          np.percentile(pesos_rep, 97.5, axis=0)),
        'repartição_reamostragens': pesos_rep,
        'n_rep': n_rep, 'seed': seed, 'metodo': metodo, 'rotacao': rotacao,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Um cenário = um conjunto de variáveis × um tipo de correlação
# ─────────────────────────────────────────────────────────────────────────────
def diagnosticar(dados: pd.DataFrame, colunas: list[str], metodo: str, k: int, nome: str) -> dict:
    """Roda os dois primeiros estágios do planejamento sobre um recorte de variáveis.

    Saída idêntica à do `scripts/diagnostico_fatorial.py` de 24/08/2026 — é o que permite
    conferir qualquer reimplementação contra `banco_de_dados/eda/fatorial/`. Extensões
    novas (SMC, eixo principal, promax) ficam **fora** daqui de propósito: mexer nesta
    função invalidaria a referência de conferência.
    """
    X = dados[colunas].dropna()
    n, p = X.shape
    R = X.corr(method=metodo).to_numpy()

    fora = R[~np.eye(p, dtype=bool)]
    acima30 = float((np.abs(fora) >= 0.30).mean())

    kmo_global, msa = kmo(R)
    qui, gl, pval = bartlett(R, n)
    val, cargas = acp(R, k)
    comun = (cargas ** 2).sum(axis=1)
    rot = varimax(cargas)
    hval = horn(min(n, 20000), p)

    rot_nomes = [ROTULOS.get(c.removesuffix('_mm'), c.removesuffix('_mm')) for c in colunas]
    tabelas = {
        f'{nome}_correlacao': pd.DataFrame(R, index=rot_nomes, columns=rot_nomes).round(3),
        f'{nome}_autovalores': pd.DataFrame({
            'componente': np.arange(1, p + 1),
            'autovalor': val.round(4),
            'pct_variancia': (100 * val / p).round(2),
            'pct_acumulado': (100 * np.cumsum(val) / p).round(2),
            'autovalor_aleatorio_horn': hval.round(4),
        }),
        f'{nome}_cargas': pd.DataFrame(
            np.column_stack([cargas, rot, comun, msa]),
            index=rot_nomes,
            columns=[f'CP{i+1}' for i in range(k)] + [f'Varimax{i+1}' for i in range(k)]
                    + ['comunalidade', 'MSA']).round(3),
    }
    return {
        'nome': nome, 'n': n, 'p': p, 'razao_casos_var': n / p,
        'metodo': metodo, 'pct_corr_acima_030': acima30,
        'kmo': kmo_global, 'msa_min': float(msa.min()),
        'bartlett_qui2': qui, 'bartlett_gl': gl, 'bartlett_p': pval,
        'autovalores_acima_1': int((val > 1).sum()),
        'autovalores_acima_horn': int((val > hval).sum()),
        'var_acumulada_k': float(100 * val[:k].sum() / p),
        'comunalidade_min': float(comun.min()),
        'tabelas': tabelas,
    }
