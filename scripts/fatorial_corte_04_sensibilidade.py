"""Sensibilidade do corte de carga < 0,4: o quanto a lista depende de escolhas de método.

O sem banheiro, que separa as propostas A e B, fica perto do 0,4. Aqui o corte é refeito mudando uma
escolha por vez: normalização de Kaiser (SPSS e R usam; `varimax` do módulo não), kappa da promax,
matriz de estrutura, postos dentro do município e 3 fatores. Depois, a reamostragem dos municípios
(com reposição) mostra o quanto o resultado depende de quais municípios entram: não é erro amostral,
porque o Censo não é amostra. Por fim, cada indicador retirado volta sozinho à lista de cada proposta.

Lê a base e grava em `banco_de_dados/eda/fatorial_corte_04/`: `sensibilidade_corte.csv`,
`sensibilidade_reamostragem.csv` e `sensibilidade_reentrada.csv`.

    ./.venv/bin/python scripts/fatorial_corte_04_sensibilidade.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'src', RAIZ / 'scripts'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import fatorial_corte_04 as fc  # noqa: E402
import fatorial_multiversao as fm  # noqa: E402
from ivs_censo.fatorial import fatoracao_eixo_principal, postos, rotacao_promax, varimax  # noqa: E402

REPLICAS = 1000


def varimax_kaiser(L: np.ndarray) -> np.ndarray:
    h = np.sqrt((L ** 2).sum(axis=1, keepdims=True))
    return varimax(L / h) * h


def promax_variante(L: np.ndarray, kappa: int, normalizacao: str) -> np.ndarray:
    """Matriz padrão da promax. 'nenhuma' é a do módulo; 'r', Varimax normalizada e alvo nas cargas
    devolvidas à escala original (`promax` do R); 'spss', Varimax e alvo nas cargas normalizadas."""
    h = np.sqrt((L ** 2).sum(axis=1, keepdims=True))
    V = {'nenhuma': varimax(L), 'r': varimax_kaiser(L), 'spss': varimax(L / h)}[normalizacao]
    U = np.linalg.lstsq(V, np.sign(V) * np.abs(V) ** kappa, rcond=None)[0]
    U = U @ np.diag(np.sqrt(np.diag(np.linalg.inv(U.T @ U))))
    return V @ U * (h if normalizacao == 'spss' else 1)


# variante: (rótulo, cargas a partir da solução sem rotação, régua da correlação, número de fatores)
VARIANTES = {
    'varimax': ('Varimax (proposta B)', varimax, 'global', 2),
    'varimax_kaiser': ('Varimax com Kaiser', varimax_kaiser, 'global', 2),
    'promax': ('promax, kappa 4 (proposta A)', lambda L: rotacao_promax(L)[0], 'global', 2),
    'promax_estrutura': ('promax, matriz de estrutura', lambda L: rotacao_promax(L)[1], 'global', 2),
    **{f'promax_k{k}_{n}': (f'promax, kappa {k}' + {'nenhuma': '', 'r': ', Kaiser (R)', 'spss': ', Kaiser (SPSS)'}[n],
                            lambda L, k=k, n=n: promax_variante(L, k, n), 'global', 2)
       for k in (2, 3, 4, 5) for n in ('nenhuma', 'r', 'spss') if (k, n) != (4, 'nenhuma')},
    'varimax_municipal': ('Varimax, postos no município', varimax, 'municipal', 2),
    'promax_municipal': ('promax, postos no município', lambda L: rotacao_promax(L)[0], 'municipal', 2),
    'varimax_3f': ('Varimax, 3 fatores', varimax, 'global', 3),
    'promax_3f': ('promax, 3 fatores', lambda L: rotacao_promax(L)[0], 'global', 3),
}


def cortar_R(matriz, codigos: list[str], cargas, k: int = 2) -> tuple[list[str], dict, bool]:
    """O corte de `fc.cortar` com a matriz e as cargas dadas. `matriz(lista)` devolve R. Devolve os
    que ficam, a última carga de cada indicador e se houve Heywood ou falta de convergência."""
    atuais, ultima, alerta = list(codigos), {}, False
    while True:
        L, _, info = fatoracao_eixo_principal(matriz(atuais), k)
        alerta |= info['heywood'] or not info['convergiu']
        carga = np.abs(cargas(L)).max(axis=1)
        ultima.update(zip(atuais, carga))
        i = int(carga.argmin())
        if carga[i] >= fc.CORTE or len(atuais) <= fc.MINIMO:
            return atuais, ultima, alerta
        atuais.pop(i)


def variantes(df: pd.DataFrame) -> pd.DataFrame:
    regs, cache = [], {}

    def matriz_de(regua):
        def matriz(lista):
            chave = (regua, tuple(lista))
            if chave not in cache:
                cols = [fm.VARS[c] for c in lista]
                cache[chave] = fm.matriz(df.dropna(subset=cols), cols, regua)
            return cache[chave]
        return matriz

    familias = {**fc.FAMILIAS, 'sem_idade_sem_banheiro': [c for c in fc.FAMILIAS['12_sem_idade'] if c != 'BAN']}
    for nome, (rotulo, cargas, regua, k) in VARIANTES.items():
        for fam, codigos in familias.items():
            if fam == 'sem_idade_sem_banheiro' and nome != 'promax':
                continue
            ficam, ultima, alerta = cortar_R(matriz_de(regua), codigos, cargas, k)
            n = len(df.dropna(subset=[fm.VARS[c] for c in ficam]))
            regs.append({'variante': nome, 'rotulo': rotulo, 'familia': fam, 'fatores': k, 'mantidos': '+'.join(ficam),
                         'p': len(ficam), 'n': n, 'ban_fica': 'BAN' in ficam, 'ban_carga': ultima.get('BAN', np.nan),
                         'carga_min': min(ultima[c] for c in ficam), 'alerta': alerta})
        print(f'  {nome}', flush=True)
    return pd.DataFrame(regs)


def reamostragem(df: pd.DataFrame) -> pd.DataFrame:
    """Municípios sorteados com reposição, nos setores com os 10 indicadores da família: refaz o corte
    (sem recalcular os postos) e lê a carga do sem banheiro com os 8 indicadores da proposta A."""
    codigos = fc.FAMILIAS['12_sem_idade']
    cols = [fm.VARS[c] for c in codigos]
    d = df.dropna(subset=cols)
    P, mun = postos(d[cols].to_numpy()), d['NM_MUN'].to_numpy()
    grupos = {m: np.flatnonzero(mun == m) for m in np.unique(mun)}
    nomes, rng = list(grupos), np.random.default_rng(fm.SEMENTE)
    oito = [c for c in codigos if c not in ('LIX', 'MNC')]
    rots = {'varimax': varimax, 'promax': lambda L: rotacao_promax(L)[0]}
    regs = []
    for _ in range(REPLICAS):
        R = np.corrcoef(P[np.concatenate([grupos[m] for m in rng.choice(nomes, len(nomes))])], rowvar=False)

        def matriz(lista):
            i = [codigos.index(c) for c in lista]
            return R[np.ix_(i, i)]
        for rot, cargas in rots.items():
            ficam = cortar_R(matriz, codigos, cargas)[0]
            L = fatoracao_eixo_principal(matriz(oito), 2)[0]
            regs.append({'rotacao': rot, 'ban_fica': 'BAN' in ficam,
                         'carga_ban': np.abs(cargas(L)).max(axis=1)[oito.index('BAN')]})
    t = pd.DataFrame(regs)
    return t.groupby('rotacao').agg(replicas=('ban_fica', 'size'), ban_fica=('ban_fica', 'mean'),
                                    carga_mediana=('carga_ban', 'median'),
                                    carga_p025=('carga_ban', lambda s: s.quantile(.025)),
                                    carga_p975=('carga_ban', lambda s: s.quantile(.975))).reset_index()


def reentrada(df: pd.DataFrame, listas: dict) -> pd.DataFrame:
    """Cada indicador retirado volta sozinho à lista final: a carga dele com a amostra que essa lista dá."""
    regs = []
    for papel, rot in (('a', 'promax'), ('b', 'varimax')):
        for c in (x for x in fc.FAMILIAS['12_sem_idade'] if x not in listas[papel]):
            atuais = listas[papel] + [c]
            cols = [fm.VARS[x] for x in atuais]
            L = fatoracao_eixo_principal(fm.matriz(df.dropna(subset=cols), cols, 'global'), 2)[0]
            carga = np.abs(VARIANTES[rot][1](L)).max(axis=1)[-1]
            regs.append({'proposta': papel, 'codigo': c, 'carga': carga, 'passa': carga >= fc.CORTE})
    return pd.DataFrame(regs)


def main() -> None:
    df = fm.carregar()
    v = variantes(df)
    v.to_csv(fc.SAIDA / 'sensibilidade_corte.csv', index=False, float_format='%.6g')
    r = reamostragem(df)
    r.to_csv(fc.SAIDA / 'sensibilidade_reamostragem.csv', index=False, float_format='%.6g')
    f = pd.read_csv(fc.SAIDA / 'finalistas.csv').set_index('papel')
    e = reentrada(df, {x: f.at[x, 'codigos'].split('+') for x in fc.PROPOSTAS})
    e.to_csv(fc.SAIDA / 'sensibilidade_reentrada.csv', index=False, float_format='%.6g')
    print(r.round(3).to_string(index=False))
    print(e.round(3).to_string(index=False))


if __name__ == '__main__':
    main()
