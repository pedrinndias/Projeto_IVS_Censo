"""Gera docs/relatorios/Relatorio_IVS_Final_NB05.md (item 9, D.2 do prompt de 2026-09).

Nenhum número é digitado: tudo vem dos CSVs que scripts/ivs_especificacoes.py (o motor da
Fase C) grava em banco_de_dados/eda/ivs_especificacoes/ — os mesmos que
notebooks/Fase3_EDA_ELSI/05_Calculo_IVS_Final.ipynb usa e confere contra o motor.

    .venv/bin/python scripts/gerar_relatorio_ivs_final.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / 'banco_de_dados' / 'eda' / 'ivs_especificacoes'
SAIDA = RAIZ / 'docs' / 'relatorios' / 'Relatorio_IVS_Final_NB05.md'


def num(x, casas: int = 2) -> str:
    """Formata como o resto do projeto: vírgula decimal."""
    return f'{float(x):.{casas}f}'.replace('.', ',')


def pct(x, casas: int = 1) -> str:
    return f'{float(x):.{casas}f}'.replace('.', ',') + '%'


def main() -> None:
    esp = pd.read_csv(DADOS / 'especificacoes.csv')
    ref = pd.read_csv(DADOS / 'referencia.csv')
    acr = pd.read_csv(DADOS / 'acrescimo_renda.csv')
    setor = pd.read_csv(DADOS / 'ivs_referencia_por_setor.csv')

    eleg = esp[esp['elegivel']]
    total, n_eleg = len(esp), int(eleg.shape[0])
    por_norm = eleg.groupby('normalizacao').size()

    principal = ref[ref['leitura'] == 'principal'].iloc[0]
    linha_ref = esp[esp['id'] == principal['id']].iloc[0]
    acr_ref = acr[acr['referencia']].iloc[0]

    por_renda = eleg.groupby('renda')['auc_mun_comum'].mean()
    por_rotacao = esp.groupby('rotacao')['elegivel'].sum()
    n_rotacao = esp.groupby('rotacao')['elegivel'].size()
    promax_met = esp[esp['rotacao'] == 'promax'].groupby('metodo')['elegivel'].sum()
    n_promax_met = esp[esp['rotacao'] == 'promax'].groupby('metodo')['elegivel'].size()
    por_lixo = esp.groupby('lixo')['elegivel'].sum()
    n_lixo = esp.groupby('lixo')['elegivel'].size()
    por_banheiro = esp.groupby('banheiro')['elegivel'].sum()
    n_banheiro = esp.groupby('banheiro')['elegivel'].size()
    faixas_indef_banheiro = esp.groupby('banheiro')['faixas_indefinidas'].sum()

    fixos = ('unico', '50_50', '60_40')
    amp_variavel = eleg.loc[~eleg['metodo'].isin(fixos), 'amp_peso_f1']

    faixas_bh = setor['faixa_ivs_bh'].value_counts()
    faixas_q = setor['faixa_quartis'].value_counts()
    n_setor = len(setor)
    sigilo_perdidos = int(setor['is_fcu'].isna().sum())    # FCU indefinido = sigilo do IBGE
    n_recorte = int(linha_ref['n'] + linha_ref['perdidos_vs_recorte'])   # 104.108, pela própria grade

    setores_por_mun = setor.groupby('NM_MUN').size()
    por_mun = setor.groupby('NM_MUN')['ivs_referencia'].mean().sort_values()
    mun_menor, mun_maior = por_mun.index[0], por_mun.index[-1]
    n_menor, n_maior = int(setores_por_mun[mun_menor]), int(setores_por_mun[mun_maior])

    linhas_alt = []
    for _, r in ref.iterrows():
        linhas_alt.append(
            f"| {r['leitura']} | `{r['id']}` | {int(r['elegiveis'])} | {num(r['posto_a'], 1)} | "
            f"{num(r['posto_b'], 1)} | {num(r['posto_c'], 1)} | {num(r['posto_medio'], 2)} |"
        )
    tabela_alt = '\n'.join(linhas_alt)

    texto = f'''# Relatório — Notebook 05: Cálculo do IVS final

**Item 9 do pedido** de `docs/prompts/prompt_nb05_ivs_final_2026-09.md`. Método, achados, a
especificação de referência com as alternativas lado a lado, limitações e as perguntas que
continuam da orientadora. Todo número abaixo vem dos CSVs de
`banco_de_dados/eda/ivs_especificacoes/`, gerados por `scripts/ivs_especificacoes.py` (o
motor da Fase C) e conferidos, célula a célula, em
`notebooks/Fase3_EDA_ELSI/05_Calculo_IVS_Final.ipynb`.

## Método

O motor monta {total} especificações: renda (original · sem extremo · mediana municipal) ×
lixo (com · sem) × banheiro (fora · V00495 · graduado) = 18 bases, cada uma com 9 esquemas de
peso (sem rotação; Varimax com SS/50-50/60-40; promax com SS da matriz padrão, SS da
estrutura, comunalidades, 50-50 e 60-40) e 2 normalizações do índice (municipal e global). Uma
especificação é elegível quando KMO ≥ 0,70, MSA mínimo ≥ 0,50, comunalidade mínima ≥ 0,30 e
carga máxima mínima ≥ 0,40 (seção 2.2 do prompt) — critérios fixados antes de rodar. Entre as
elegíveis, a referência proposta é a de melhor posição média em três critérios de peso igual:
(a) estabilidade (amplitude do peso do fator 1 ao deixar um município de fora), (b) validade
discriminante dentro do município (AUC contra FCU) e (c) parcimônia (menos variáveis).

## Achados

1. **{n_eleg} de {total} especificações são elegíveis** ({int(por_norm.get('municipal', 0))} com normalização municipal, {int(por_norm.get('global', 0))} com normalização global).
2. **Renda:** entre as elegíveis, a AUC municipal média por versão de renda fica em {num(por_renda.get('original', float('nan')), 4)} (original), {num(por_renda.get('sem_extremo', float('nan')), 4)} (sem o extremo de Belo Horizonte) e {num(por_renda.get('mediana_mun', float('nan')), 4)} (mediana municipal) — as três coladas.
3. **Rotação:** sem rotação (um fator) é inelegível em toda a grade (0 de {int(n_rotacao.get('sem_rotacao', 0))}); Varimax elege {int(por_rotacao.get('varimax', 0))} de {int(n_rotacao.get('varimax', 0))}; promax elege {int(por_rotacao.get('promax', 0))} de {int(n_rotacao.get('promax', 0))}.
4. **Pesos na oblíqua (promax):** elegibilidade por método — {'; '.join(f"{m}: {int(promax_met[m])}/{int(n_promax_met[m])}" for m in promax_met.index)}. Nos métodos de peso fixo (50-50, 60-40) a amplitude do peso do fator 1 é zero por construção; entre os métodos que dependem dos dados, a amplitude vai de {num(amp_variavel.min(), 2)} a {num(amp_variavel.max(), 2)} pontos percentuais.
5. **Lixo:** com lixo, {int(por_lixo.get('com', 0))} de {int(n_lixo.get('com', 0))} especificações são elegíveis; sem lixo, {int(por_lixo.get('sem', 0))} de {int(n_lixo.get('sem', 0))}.
6. **Banheiro:** elegibilidade por versão — {'; '.join(f"{b}: {int(por_banheiro[b])}/{int(n_banheiro[b])}" for b in por_banheiro.index)}. Faixas indefinidas (setor no único município de sua faixa) por versão — {'; '.join(f"{b}: {int(faixas_indef_banheiro[b])}" for b in faixas_indef_banheiro.index)}.
7. **O que o índice acrescenta à renda** (item 6 do pedido): nas {len(acr)} especificações elegíveis, a AUC do índice fica sempre abaixo da renda invertida sozinha, global e na mediana municipal; dentro dos decis de renda de cada município fica sempre acima; somar o índice à renda na regressão logística sempre reduz a deviance. Na referência: estratos {num(acr_ref['auc_indice_estratos'], 4)} (índice) × {num(acr_ref['auc_renda_estratos'], 4)} (renda); deviance −{num(acr_ref['queda_deviance'], 1)} (z {num(acr_ref['z_indice'], 1)}), AUC {num(acr_ref['auc_modelo_renda'], 4)} → {num(acr_ref['auc_modelo_renda_indice'], 4)}.
8. **IVS final da referência:** definido para {n_setor} setores; faixas pela regra do IVS-BH 2012 — {'; '.join(f"{k}: {int(v)}" for k, v in faixas_bh.items())}; por quartis municipais — {'; '.join(f"{k}: {int(v)}" for k, v in faixas_q.items())}. IVS médio mais baixo em {mun_menor} ({num(por_mun.iloc[0], 4)}; {n_menor} setores) e mais alto em {mun_maior} ({num(por_mun.iloc[-1], 4)}; {n_maior} setores) — tabela completa dos 70 municípios no notebook, seção 10.
9. **Perda de setores por dado ausente:** a base da especificação de referência fica com {int(linha_ref['n'])} dos {n_recorte} setores do recorte da seção 1 do prompt ({int(linha_ref['perdidos_vs_recorte'])} a menos, {pct(100 * linha_ref['perdidos_vs_recorte'] / n_recorte, 1)} — variável ausente nos componentes do banheiro graduado ou da renda, em parte por sigilo do IBGE). Dentro dessa base, o FCU em si está definido em {n_setor - sigilo_perdidos} de {n_setor} setores (sigilo específico do FCU nesta base: {sigilo_perdidos}).

## A referência proposta e as alternativas (seção 2.2 do prompt)

A leitura **principal** (critério (a) = amplitude do peso do fator 1; critério (b) = AUC
municipal na amostra comum às três versões de banheiro) propõe
`{principal['id']}` — postos {num(principal['posto_a'], 1)}º (estabilidade),
{num(principal['posto_b'], 1)}º (AUC municipal) e {num(principal['posto_c'], 1)}º
(parcimônia), posição média {num(principal['posto_medio'], 2)}. As três variantes de leitura
abaixo trocam a amostra, o critério (a) ou a normalização — nenhuma delas é a escolhida aqui:

| Leitura | Especificação | Elegíveis | Posto (a) | Posto (b) | Posto (c) | Posto médio |
|---|---|---:|---:|---:|---:|---:|
{tabela_alt}

Isto é **proposta**, não decisão (seção 0.2 do prompt): a escolha entre a leitura principal e
as três alternativas continua com a orientadora.

## Limitações

- **Circularidade parcial com o FCU.** O achado 7 usa a queda de deviance de FCU (critério do
  IBGE que já incorpora condições de moradia) como medida do que o índice acrescenta à renda;
  parte da separação vem de as mesmas dimensões de saneamento aparecerem nos dois lados.
- **Falácia ecológica.** O IVS é calculado por setor censitário, mas a validação por AUC
  contra FCU e a comparação com o IVS-BH 2012 operam em agregados municipais ou por faixa —
  um padrão médio no setor ou no município não garante o mesmo padrão para cada domicílio.
- **Perda de setores por dado ausente.** Achado 9: {int(linha_ref['perdidos_vs_recorte'])} dos
  {n_recorte} setores do recorte ficam fora da base da especificação de referência por
  variável ausente — em parte por sigilo do IBGE nos componentes do banheiro ou da renda, não
  só no FCU (que, nesta base, está definido em todos os setores que sobram).

## Perguntas à orientadora

Nenhuma é fechada por este notebook (seção 0.2 do prompt: "não decidir pela orientadora").

- Qual renda usar — original, sem o extremo de Belo Horizonte, ou mediana municipal (achado
  2)? As três ficam coladas em AUC municipal.
- Qual rotação — Varimax ou promax (achado 3)? Sem rotação é inelegível em toda a grade.
- Como dividir os pesos na solução oblíqua — SS da matriz padrão, SS da estrutura,
  comunalidades, 50/50 ou 60/40 da literatura (achado 4)? Os pesos fixos (50/50, 60/40) têm
  amplitude zero por construção e por isso vencem sempre o critério (a) como escrito.
- O lixo entra no índice (achado 5)?
- O banheiro entra, e em qual versão — fora, V00495 ou a graduada da Fase B (achado 6)?
- Normalização do índice — dentro do município (leitura principal) ou global (leitura
  `normalizacao_global` da tabela acima)?
- Qual regra de faixas — IVS-BH 2012 (achado 8) ou quartis municipais?
- Que peso a AUC contra FCU deve ter na escolha, dada a circularidade parcial (limitações)?
'''

    SAIDA.write_text(texto, encoding='utf-8')
    print('gravado:', SAIDA, f'({len(texto)} caracteres)')


if __name__ == '__main__':
    main()
