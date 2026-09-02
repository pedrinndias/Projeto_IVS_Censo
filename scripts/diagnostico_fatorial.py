"""Diagnóstico de adequabilidade dos dados à análise fatorial (Figueiredo Filho & Silva Júnior, 2010).

Roda os testes do **primeiro e do segundo estágio** do planejamento de uma análise
fatorial sobre os 7 componentes do IVS, no recorte de análise (urbano + `Dados_sig = OK`):

  1. tamanho da amostra e razão casos/variáveis;
  2. padrão de correlação (proporção de coeficientes |r| >= 0,30);
  3. KMO global e MSA por variável (matriz anti-imagem);
  4. Bartlett Test of Sphericity;
  5. autovalores, variância acumulada, critério de Kaiser, análise paralela de Horn;
  6. comunalidades e cargas fatoriais (ACP), sem e com rotação Varimax.

É **diagnóstico**, não o cálculo do IVS: roda sobre os indicadores brutos, antes da
padronização min-max por município (Notebook 03) e da definição dos pesos (Notebook 04).

Uso:
    python scripts/diagnostico_fatorial.py

Saídas: `banco_de_dados/eda/fatorial/*.csv` e um resumo no stdout.
Depende apenas de pandas e numpy (as mesmas do `requirements.txt`).
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BASE = RAIZ / 'banco_de_dados' / 'entrega_orientadora' / 'Base_ELSI_70Municipios_Censo2022.csv'
SAIDA = RAIZ / 'banco_de_dados' / 'eda' / 'fatorial'

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
# Estatísticas
# ─────────────────────────────────────────────────────────────────────────────
def chi2_sf(x: float, k: int) -> float:
    """Cauda superior da qui-quadrado por Wilson–Hilferty (exata o bastante com df alto)."""
    z = ((x / k) ** (1 / 3) - (1 - 2 / (9 * k))) / math.sqrt(2 / (9 * k))
    return 0.5 * math.erfc(z / math.sqrt(2))


def bartlett(R: np.ndarray, n: int) -> tuple[float, int, float]:
    """BTS: testa H0 de que a matriz de correlação é a identidade."""
    p = R.shape[0]
    sinal, logdet = np.linalg.slogdet(R)
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


def varimax(cargas: np.ndarray, tol: float = 1e-6, maxiter: int = 500) -> np.ndarray:
    """Rotação ortogonal Varimax (Kaiser), sem normalização."""
    L = cargas.copy()
    p, k = L.shape
    if k < 2:
        return L
    R = np.eye(k)
    d_ant = 0.0
    for _ in range(maxiter):
        Lam = L @ R
        u, s, vt = np.linalg.svd(
            L.T @ (Lam ** 3 - Lam @ np.diag(np.diag(Lam.T @ Lam)) / p))
        R = u @ vt
        d = s.sum()
        if d_ant != 0 and d / d_ant < 1 + tol:
            break
        d_ant = d
    return L @ R


def acp(R: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    """Componentes principais a partir da matriz de correlação: autovalores e cargas."""
    val, vec = np.linalg.eigh(R)
    ordem = np.argsort(val)[::-1]
    val, vec = val[ordem], vec[:, ordem]
    cargas = vec[:, :k] * np.sqrt(np.maximum(val[:k], 0))
    return val, cargas


def horn(n: int, p: int, sims: int = 50, semente: int = 42) -> np.ndarray:
    """Análise paralela de Horn (1965): autovalores médios de dados aleatórios n × p."""
    rng = np.random.default_rng(semente)
    acc = np.zeros(p)
    for _ in range(sims):
        X = rng.standard_normal((n, p))
        acc += np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]
    return acc / sims


# ─────────────────────────────────────────────────────────────────────────────
# Um cenário = um conjunto de variáveis × um tipo de correlação
# ─────────────────────────────────────────────────────────────────────────────
def diagnosticar(dados: pd.DataFrame, colunas: list[str], metodo: str, k: int, nome: str) -> dict:
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


def main() -> None:
    uso = ['CD_SETOR', 'NM_MUN', 'urbano', 'Dados_sig'] + IVS7
    df = pd.read_csv(BASE, sep=';', usecols=uso, low_memory=False)
    df = df[(df['urbano'].astype(str) == '1') & (df['Dados_sig'] == 'OK')].copy()
    df['renda_inv'] = -df['renda_media']

    # Versão padronizada min-max **por município** — a normalização prevista para o
    # Notebook 03. Como é uma transformação afim com escala diferente por grupo, ela
    # **muda** a matriz de correlação global e, portanto, toda a análise fatorial: a
    # ordem NB03 -> NB04 não é indiferente. Este cenário mede o tamanho do efeito.
    def minmax_municipal(col: pd.Series) -> pd.Series:
        g = df.groupby('NM_MUN')[col.name]
        lo, hi = g.transform('min'), g.transform('max')
        return (col - lo) / (hi - lo).replace(0, np.nan)

    sete = [c if c != 'renda_media' else 'renda_inv' for c in IVS7]
    for c in sete:
        df[c + '_mm'] = minmax_municipal(df[c])
    seis = [c for c in sete if c != 'pct_lixo_inad']
    seis_sem_analfab = [c for c in sete if c != 'pct_analfab']

    cenarios = [
        (sete, 'spearman', 2, 'ivs7_spearman'),
        (sete, 'pearson', 2, 'ivs7_pearson'),
        (seis, 'spearman', 2, 'ivs6_sem_lixo_spearman'),
        (seis_sem_analfab, 'spearman', 2, 'ivs6_sem_analfab_spearman'),
        ([c + '_mm' for c in sete], 'spearman', 2, 'ivs7_minmax_municipal_spearman'),
        ([c + '_mm' for c in seis], 'spearman', 2, 'ivs6_sem_lixo_minmax_municipal_spearman'),
    ]

    SAIDA.mkdir(parents=True, exist_ok=True)
    resumo = []
    for colunas, metodo, k, nome in cenarios:
        r = diagnosticar(df, colunas, metodo, k, nome)
        for arq, tab in r.pop('tabelas').items():
            tab.to_csv(SAIDA / f'{arq}.csv', sep=';', encoding='utf-8-sig')
        resumo.append(r)
        print(f"\n── {nome} ({metodo}) ─────────────────────────────")
        print(f"   n = {r['n']:,}  ·  p = {r['p']}  ·  casos/variável = {r['razao_casos_var']:,.0f}")
        print(f"   |r| >= 0,30: {100*r['pct_corr_acima_030']:.1f}% dos coeficientes")
        print(f"   KMO = {r['kmo']:.3f}  (MSA mínimo = {r['msa_min']:.3f})")
        print(f"   BTS: qui2 = {r['bartlett_qui2']:,.0f}  gl = {r['bartlett_gl']}  p = {r['bartlett_p']:.3g}")
        print(f"   Kaiser: {r['autovalores_acima_1']} fator(es) · Horn: {r['autovalores_acima_horn']}")
        print(f"   variância acumulada com {k} fatores: {r['var_acumulada_k']:.1f}%")
        print(f"   comunalidade mínima: {r['comunalidade_min']:.3f}")

    pd.DataFrame(resumo).round(4).to_csv(
        SAIDA / 'resumo_adequabilidade.csv', sep=';', index=False, encoding='utf-8-sig')
    print(f"\nTabelas em {SAIDA.relative_to(RAIZ)}/")


if __name__ == '__main__':
    main()
