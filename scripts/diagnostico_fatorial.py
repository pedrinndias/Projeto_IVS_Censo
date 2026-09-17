"""Diagnóstico de adequabilidade dos dados à análise fatorial.

Roda os testes do **primeiro e do segundo estágio** do planejamento de uma análise
fatorial sobre os 7 componentes do IVS, no recorte de análise (urbano + `Dados_sig = OK`):

  1. tamanho da amostra e razão casos/variáveis;
  2. padrão de correlação (proporção de coeficientes |r| >= 0,30);
  3. KMO global e MSA por variável (matriz anti-imagem);
  4. Bartlett Test of Sphericity;
  5. autovalores, variância acumulada, critério de Kaiser, análise paralela de Horn;
  6. comunalidades e cargas fatoriais (ACP), sem e com rotação Varimax.

Referências: FIGUEIREDO FILHO & SILVA JÚNIOR (2010), que deu a sequência dos testes, e
MATOS & RODRIGUES, *Análise fatorial* (Enap, 2019), que a revisou em três pontos — ver o
docstring de `ivs_censo.fatorial`.

A matemática vive em `src/ivs_censo/fatorial.py` desde 16/09/2026; este script é a
interface de linha de comando e a definição dos cenários. A separação segue o padrão do
Notebook 02: fórmula em módulo testado, uso no script ou no notebook.

É **diagnóstico**, não o cálculo do IVS: roda sobre os indicadores brutos, antes da
padronização min-max por município (Notebook 03) e da definição dos pesos (Notebook 04).

Uso:
    python scripts/diagnostico_fatorial.py

Saídas: `banco_de_dados/eda/fatorial/*.csv` e um resumo no stdout.
Depende apenas de pandas e numpy (as mesmas do `requirements.txt`).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'src'))

from ivs_censo.fatorial import IVS7, diagnosticar  # noqa: E402

BASE = RAIZ / 'banco_de_dados' / 'entrega_orientadora' / 'Base_ELSI_70Municipios_Censo2022.csv'
SAIDA = RAIZ / 'banco_de_dados' / 'eda' / 'fatorial'


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
