"""Dados do relatório descritivo do andamento (`relatorio_descritivo/`).

Lê só tabelas já conferidas — `analises_exploratorias/00_referencia/tabelas/`,
`banco_de_dados/eda/` e o Quadro de Indicadores — e grava, para o gerador do deck:
`dados/numeros.json` (todo número e texto que vai a slide, por ID), `dados/manifesto.csv`
(uma linha por slide) e `figuras/<ID>.png`. Nenhum indicador é recalculado: a base do
`.db` serve só aos histogramas, montada pelo mesmo `montar_base` da `00_referencia`.

Os textos das demandas citam o registro (arquivo:linhas). O verificador confere que todo
número de um texto aparece nessas linhas ou nas tabelas do slide.

Uso:  ./.venv/bin/python scripts/dados_relatorio_descritivo.py
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
import eda_versoes as ev  # noqa: E402
from eda_versoes import ARGILA, CINZA, PETROLEO, TINTA, br, intbr, plt  # noqa: E402

SAIDA = RAIZ / 'relatorio_descritivo'
DADOS, FIG = SAIDA / 'dados', SAIDA / 'figuras'
REF = RAIZ / 'analises_exploratorias' / '00_referencia'
TAB = REF / 'tabelas'
AMPL = RAIZ / 'banco_de_dados' / 'eda' / 'fatorial_ampliada'
ESTADO_DEM = 'docs/prompts/estado_demandas_2026-09.md'
VERSAO = 'v5'

# Variáveis da referência proposta do NB05 (T20) — para "Entra na referência proposta?".
REFERENCIA = set(pd.read_csv(TAB / 'T20_variaveis_cargas.csv')['variavel'])


def na_referencia(ind: str) -> str:
    """C-08: a referência usa a renda média invertida (renda_inv na T20), não a coluna renda_media."""
    if ind in REFERENCIA:
        return 'Sim'
    return 'Sim, como renda invertida' if ind == 'renda_media' and 'renda_inv' in REFERENCIA else 'Não'
QUADRO = pd.read_csv(RAIZ / 'banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv',
                     sep=';', encoding='utf-8-sig').set_index('indicador')
T03 = pd.read_csv(TAB / 'T03_descritivas_global.csv').set_index('indicador')
T02 = pd.read_csv(TAB / 'T02_perdas_por_indicador.csv').set_index('indicador')
# C-01: arquivo de origem e local do cálculo, da aba Indicadores da planilha de gerenciamento.
GERENCIAMENTO = RAIZ.parent / 'Relatorios e Andamento' / 'gerenciamento_artigos_cientificos_IC.xlsx'
FONTE_GER = 'Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx, aba Indicadores'
GER = pd.read_excel(GERENCIAMENTO, sheet_name='Indicadores').set_index('Indicador (código)')

# Definições que não estão no Quadro (28 linhas): fonte citada no slide.
EXTRAS = {
    'banheiro_graduado': dict(
        o_que_mede='Grau de inadequação do banheiro: 0 = todos com banheiro, 1 = todos sem banheiro nem sanitário',
        numerador='1·V00236 + 2·V00237 + 3·V00238', denominador='3·V00001',
        entra_no_ivs7='Não', fonte='scripts/ivs_especificacoes.py:58-62'),
    'renda_media_sem_extremo': dict(
        o_que_mede='Renda média das pessoas responsáveis, com o setor extremo de BH vazio',
        numerador='renda_media, sem o setor 310620005650366', denominador='—',
        entra_no_ivs7='Não', fonte='src/ivs_censo/renda.py:113-127'),
    'renda_media_mediana_mun': dict(
        o_que_mede='Renda média das pessoas responsáveis, com o setor extremo de BH substituído pela mediana do município',
        numerador='renda_media, com imputação no setor 310620005650366', denominador='—',
        entra_no_ivs7='Não', fonte='src/ivs_censo/renda.py:130-144'),
}


# ── Formatação ─────────────────────────────────────────────────────────────────
def tipo(ind: str) -> str:
    obs = str(QUADRO['observacao'].get(ind, '')) if ind in QUADRO.index else ''
    if '×100' in obs or 'x100' in obs:                 # já vem por 100 (IEP, RDI, 70+ entre 60+)
        return 'razao'
    if ind.startswith('renda'):
        return 'renda'
    if ind.startswith(('pct_', 'prop_')):
        return 'proporcao'
    if ind == 'banheiro_graduado':
        return 'grau'
    return 'razao'                       # razao_moradores, iep_setor, rdi_setor


def fmt(ind: str, v) -> str:
    """Valor do indicador no formato do slide (§2.6 do prompt)."""
    t = tipo(ind)
    if t == 'proporcao':
        return br(100 * v, 2) + '%'
    if t == 'renda':
        return 'R$ ' + br(v, 2)
    return br(v, 3 if t == 'grau' else 2)


def unidade(ind: str) -> str:
    t = tipo(ind)
    obs = str(QUADRO['observacao'].get(ind, '')) if ind in QUADRO.index else ''
    return {'proporcao': 'proporção, mostrada em %', 'renda': 'reais (R$)',
            'grau': 'escala de 0 a 1'}.get(t, 'por 100' if '×100' in obs else 'razão')


# ── Ordem dos indicadores e IDs ─────────────────────────────────────────────────
def ordem_ds() -> list[str]:
    """Ordem da T03, com as duas rendas alternativas logo depois de `renda_media`."""
    o = [i for i in T03.index if i not in ('renda_media_sem_extremo', 'renda_media_mediana_mun')]
    k = o.index('renda_media') + 1
    return o[:k] + ['renda_media_sem_extremo', 'renda_media_mediana_mun'] + o[k:]


ID_DS = {ind: f'DS{3 + k:02d}' for k, ind in enumerate(ordem_ds())}

# Slides já construídos, na ordem do deck. Cresce lote a lote (CONSTRUCAO.md).
SLIDES = (['A01', 'A02', 'A03'] + [f'DM{k:02d}' for k in range(16)]
          + [x for k in range(35) for x in ([f'DS{k:02d}', f'DS{k:02d}-2'] if 3 <= k <= 33 else [f'DS{k:02d}'])]
          + [f'DC{k:02d}' for k in range(8)]
          + [f'FA{k:02d}' for k in range(17)] + ['FP00'] + [f'FC{k:02d}' for k in range(1, 10)]
          + [f'FP{k:02d}' for k in range(1, 14)] + ['Z02'])
# C-04 (08/10/2026): slides novos — um segundo slide por indicador (DSxx-2), as correlações (DC) e
# os cenários da fatorial (FC). Entram no deck do Pedro por scripts/inserir_no_relatorio.py.
NOVOS_C04 = [x for x in SLIDES if x.endswith('-2') or x.startswith(('DC', 'FC'))]


# ── Figuras ─────────────────────────────────────────────────────────────────────
def histograma(serie: pd.Series, ind: str, rotulo: str, arq: Path) -> dict:
    """Histograma do indicador sozinho, com um boxplot fino em cima. Devolve o que a
    legenda precisa dizer (corte do eixo, zeros fora do histograma)."""
    v = serie.dropna().astype(float)
    escala = 100 if tipo(ind) == 'proporcao' else 1
    v = v * escala
    nota = {}
    pz = (v == 0).mean() * 100
    if pz >= 50:                                   # §2.4: só os positivos, zeros na legenda
        nota['zeros_fora'] = int((v == 0).sum())
        v = v[v > 0]
    p99 = v.quantile(0.99)
    if v.max() > 3 * p99 and p99 > 0:              # cauda longa: eixo até o P99, dito na legenda
        nota['acima_p99'] = int((v > p99).sum())
        nota['p99'] = float(p99 / escala)
        v_plot = v[v <= p99]
    else:
        v_plot = v
    fig, (a0, a1) = plt.subplots(2, 1, figsize=(4.6, 3.9), dpi=150, sharex=True,
                                 gridspec_kw={'height_ratios': [1, 5], 'hspace': 0.05})
    a0.boxplot(v_plot, orientation='horizontal', widths=0.6, showfliers=False, patch_artist=True,
               boxprops=dict(facecolor='white', edgecolor=TINTA, linewidth=0.9),
               medianprops=dict(color=ARGILA, linewidth=1.4),
               whiskerprops=dict(color=TINTA, linewidth=0.8), capprops=dict(color=TINTA, linewidth=0.8))
    a0.axis('off')
    a1.hist(v_plot, bins=50, color=PETROLEO, edgecolor='white', linewidth=0.3)
    a1.axvline(v.median(), color=ARGILA, linewidth=1.0, linestyle='--')
    xl = {'proporcao': f'{rotulo} (%)', 'renda': f'{rotulo} (R$)'}.get(tipo(ind), rotulo)
    ev.estilo(a1, xl, 'setores')
    a1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: intbr(x)))
    fig.savefig(arq, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return nota


def copiar_figura(origem: str, sid: str) -> str:
    shutil.copyfile(REF / 'figuras' / origem, FIG / f'{sid}.png')
    return f'figuras/{sid}.png'


# ── Slides ──────────────────────────────────────────────────────────────────────
def a01() -> dict:
    return dict(titulo='Relatório descritivo do andamento', parte='A', requisito='R1, R14',
                kicker='IVS · CENSO 2022 · 70 MUNICÍPIOS DO ELSI-BRASIL',
                sub='As demandas de setembro e como foram cobertas, a descritiva de cada '
                    'indicador e a análise fatorial — para conferência com os resultados da orientadora',
                rodape=f'Pedro Dias Soares · outubro de 2026 · deck {VERSAO}',
                fontes=['—'])


def a02() -> dict:
    f = pd.read_csv(TAB / 'T01_funil.csv')
    s0 = pd.read_csv(AMPL / 'cenarios.csv', sep=';', encoding='utf-8-sig').set_index('cenario').loc['S0']
    bases = [
        ['Descritiva dos indicadores', intbr(f.loc[f['etapa'] == 'Dados_sig = OK', 'setores'].iloc[0]),
         'Urbanos com Dados_sig = OK', 'DS'],
        ['Fatorial da referência proposta (NB05)', intbr(f['setores'].iloc[-1]),
         'Os mesmos, com os 7 componentes completos', 'FA'],
        ['Fatorial do NB04 e cenários S0–S7', intbr(s0['n']),
         'IVS-7 completo (S0); cada cenário tem o seu n', 'FP'],
    ]
    return dict(titulo='Como ler', parte='A', requisito='R10, R13',
                sub='Cada slide tem um código e uma base declarada',
                blocos=[
                    ['Código.', 'No canto superior direito (DM, DS, FA, FP). Para pedir correção '
                     'ou marcar o que vai para o artigo, basta citar o código.'],
                    ['Números.', 'Proporções em % com duas casas; renda em R$; razões com duas '
                     'casas. Os valores com precisão total ficam no anexo xlsx.'],
                    ['A CONFERIR.', 'Marca o que não tem fonte no projeto. Nada foi preenchido por suposição.'],
                ],
                cab=['Parte', 'Setores', 'Quais', 'Códigos'], linhas=bases,
                fontes=['analises_exploratorias/00_referencia/tabelas/T01_funil.csv',
                        'banco_de_dados/eda/fatorial_ampliada/cenarios.csv (S0, coluna n)'])


def dm02() -> dict:
    alt = pd.read_csv(RAIZ / 'banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv',
                      sep=';', encoding='utf-8-sig')
    linhas = [[r.alternativa, 'R$ ' + br(r.valor_imputado, 3), 'R$ ' + br(r.bh_media, 2),
               'R$ ' + br(r.agregado_media, 2)] for r in alt.itertuples()]
    return dict(titulo='Demanda 1 — a renda com a mediana', parte='DM', requisito='R2, R3',
                sub='Redação do registro: "coluna de renda com a mediana" · estado: concluída',
                caixas=[
                    ['Pedido', 'Coluna de renda com a mediana (redação do registro).'],
                    ['Como lemos', 'A mediana do próprio setor não existe no arquivo bruto do Censo '
                     '(vêm V06001–V06005, não V06006). Lemos como: no setor extremo de Belo Horizonte, '
                     'pôr a mediana do município calculada sem ele.'],
                    ['O que foi feito', 'Função renda_imputada_mediana_municipal em src/ivs_censo/renda.py; '
                     'coluna nova renda_media_mediana_mun na entrega (o banco passa de 104 para 105 colunas); '
                     'CSV de sensibilidade com três alternativas.'],
                    ['O que contornamos', 'Obstáculo: falta a mediana do setor (V06006). Saída: imputação pela '
                     'mediana do município, só no setor excluído a pedido da orientadora em 01/09/2026 '
                     '(310620005650366, R$ 170.418,06). Efeito: 1 setor difere de renda_media.'],
                ],
                cab=['Alternativa', 'Valor imputado', 'Média em BH', 'Média nos 70'], linhas=linhas,
                resultado_em=f"{ID_DS['renda_media_mediana_mun']} (a coluna nova) e FP01 (o efeito na fatorial)",
                fonte_texto=[f'{ESTADO_DEM}:16', f'{ESTADO_DEM}:35-38', f'{ESTADO_DEM}:105-120',
                             'src/ivs_censo/renda.py:91-97'],
                fontes=[f'{ESTADO_DEM}:16, 35-38, 105-120',
                        'banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv'])


def ds01() -> dict:
    f = pd.read_csv(TAB / 'T01_funil.csv')
    linhas = [[r.etapa, intbr(r.setores), '—' if r.saem == 0 else intbr(r.saem),
               r.motivo_da_saida if isinstance(r.motivo_da_saida, str) else '—'] for r in f.itertuples()]
    return dict(titulo='A base', parte='DS', requisito='R6, R10',
                sub='De 109.032 setores dos 70 municípios aos que entram em cada parte',
                cab=['Etapa', 'Setores', 'Saem', 'Por quê'], linhas=linhas,
                figura=copiar_figura('F01_funil.png', 'DS01'),
                legenda='O funil do recorte, etapa a etapa.',
                frases=[f"A descritiva usa {intbr(f['setores'].iloc[2])} setores (urbanos com Dados_sig = OK).",
                        f"A fatorial da referência proposta usa {intbr(f['setores'].iloc[3])}: "
                        f"saem {intbr(f['saem'].iloc[3])} com algum componente faltante."],
                fontes=['analises_exploratorias/00_referencia/tabelas/T01_funil.csv', 'F01_funil.png'])


def ds(ind: str, base) -> dict:
    sid = ID_DS[ind]
    r, p = T03.loc[ind], T02.loc[ind]
    q = QUADRO.loc[ind].to_dict() if ind in QUADRO.index else EXTRAS[ind]
    fonte_def = ('banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv'
                 if ind in QUADRO.index else EXTRAS[ind]['fonte'])
    nota = histograma(base.df[ind], ind, r['rotulo'], FIG / f'{sid}.png')
    linhas = [
        ['Setores com valor', intbr(p['n_validos'])],
        ['Faltantes', f"{intbr(p['n_faltantes'])} ({br(p['pct_faltantes'], 2)}%)"],
        ['Média', fmt(ind, r['media'])], ['Desvio-padrão', fmt(ind, r['dp'])],
        ['Coeficiente de variação', br(r['cv_pct'], 1) + '%'],
        ['Mínimo', fmt(ind, r['min'])], ['P10', fmt(ind, r['p10'])], ['P25', fmt(ind, r['p25'])],
        ['Mediana', fmt(ind, r['mediana'])], ['P75', fmt(ind, r['p75'])], ['P90', fmt(ind, r['p90'])],
        ['Máximo', fmt(ind, r['max'])], ['Setores com zero', br(r['pct_zeros'], 2) + '%'],
        ['Assimetria', br(r['assim'], 2)],
    ]
    zeros = ('nenhum setor tem valor zero' if r['pct_zeros'] == 0
             else f"{br(r['pct_zeros'], 2)}% dos setores têm valor zero")
    frases = [f"Metade dos setores tem até {fmt(ind, r['mediana'])}; um em cada quatro tem mais de "
              f"{fmt(ind, r['p75'])}.",
              f"Entre o P10 e o P90, vai de {fmt(ind, r['p10'])} a {fmt(ind, r['p90'])}; {zeros}."]
    leg = 'Histograma nos setores com valor; tracejado = mediana.'
    if 'zeros_fora' in nota:
        leg += f" Fora do histograma: {intbr(nota['zeros_fora'])} setores com zero."
    if 'acima_p99' in nota:
        leg += (f" Eixo até o P99 ({fmt(ind, nota['p99'])}); {intbr(nota['acima_p99'])} setores "
                f"acima dele ficam fora do desenho, não da tabela.")
    return dict(titulo=r['rotulo'], parte='DS', requisito='R4, R5, R6, R10', indicador=ind,
                sub=q['o_que_mede'], dimensao=ev.dimensoes().get(ind, 'A CONFERIR'),
                definicao=[['Numerador', q['numerador']], ['Denominador', q['denominador']],
                           ['Arquivo do Censo', GER.loc[ind, 'Arquivo do Censo de origem']],
                           ['Calculado em', GER.loc[ind, 'Calculado em']],
                           ['Unidade', unidade(ind)], ['Entra no IVS-7?', q['entra_no_ivs7']],
                           ['Entra na referência proposta?', na_referencia(ind)]],
                observacao=(q.get('observacao') if q.get('observacao') not in (None, '(sem observação)') else ''),
                cab=['Distribuição nos setores da base', ''], linhas=linhas, frases=frases,
                figura=f'figuras/{sid}.png', legenda=leg,
                notas=f'Gerado por ds() em scripts/dados_relatorio_descritivo.py. Coluna no .db: {ind} '
                      f'(tabela setores_censitarios, recorte urbano == 1 e Dados_sig = OK). '
                      f'Conferir: T03 e T02 da 00_referencia, linha {ind}.',
                fontes=['analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv',
                        'T02_perdas_por_indicador.csv', fonte_def, FONTE_GER])


def fa05() -> dict:
    t = pd.read_csv(TAB / 'T21_autovalores.csv')
    linhas = [[int(x.componente), br(x.autovalor, 3), br(x.horn, 3), br(x.pct_variancia, 2) + '%',
               br(x.pct_acumulado, 2) + '%'] for x in t.itertuples()]
    kaiser = int((t['autovalor'] > 1).sum())
    horn = int((t['autovalor'] > t['horn']).cumprod().sum())     # consecutivos acima da referência
    return dict(titulo='Autovalores e análise paralela de Horn', parte='FA', requisito='R7',
                sub='Referência proposta do NB05 (proposta, não escolhida) · 7 variáveis · 73.878 setores',
                cab=['Componente', 'Autovalor', 'Referência de Horn', '% da variância', '% acumulado'],
                linhas=linhas, figura=copiar_figura('F22_sedimentacao_horn.png', 'FA05'),
                legenda='Autovalores observados e a referência da análise paralela.',
                frases=[f'{kaiser} autovalores passam de 1 (critério de Kaiser); {horn} ficam acima da '
                        f'referência de Horn.',
                        f"Os dois primeiros componentes somam {br(t['pct_acumulado'].iloc[1], 2)}% da variância."],
                fontes=['analises_exploratorias/00_referencia/tabelas/T21_autovalores.csv',
                        'F22_sedimentacao_horn.png'])


def fp08() -> dict:
    c = pd.read_csv(AMPL / 'cenarios.csv', sep=';', encoding='utf-8-sig').set_index('cenario')
    sel = c.loc[['S0', 'S1', 'S6', 'S7']]

    def lixo(v):
        return '—' if pd.isna(v) or v == '' else ('Sim' if str(v) == 'True' else 'Não')
    linhas = [[k, x['descricao'], intbr(x['n']), br(x['kmo'], 3), int(x['fatores_kaiser']),
               int(x['fatores_horn']), br(x['var_explicada_2f'], 2) + '%',
               lixo(x['lixo_fator_proprio_varimax'])] for k, x in sel.iterrows()]
    s0, s1 = c.loc['S0'], c.loc['S1']
    return dict(titulo='Demanda 10 — testar o lixo', parte='FP', requisito='R8',
                sub='Redação do registro: "testar lixo" · cenários com e sem o lixo inadequado',
                cab=['Cenário', 'Descrição', 'Setores', 'KMO', 'Fatores (Kaiser)', 'Fatores (Horn)',
                     'Variância, 2 fatores', 'Lixo forma fator próprio (Varimax)'],
                linhas=linhas,
                frases=[f"Com o lixo (S0), Kaiser e Horn indicam {int(s0['fatores_kaiser'])} e "
                        f"{int(s0['fatores_horn'])} fatores, e o lixo forma fator próprio na Varimax.",
                        f"Sem o lixo (S1), indicam {int(s1['fatores_kaiser'])} e {int(s1['fatores_horn'])}."],
                fontes=['banco_de_dados/eda/fatorial_ampliada/cenarios.csv '
                        '(colunas n, kmo, fatores_kaiser, fatores_horn, var_explicada_2f, '
                        'lixo_fator_proprio_varimax)', f'{ESTADO_DEM}:25'])


# ── Parte DM (lote 1) ────────────────────────────────────────────────────────────
E = ESTADO_DEM
NB05 = 'docs/prompts/estado_nb05_2026-09.md'
MAPA = 'docs/Apresentacoes_IVS/MAPA_APRESENTACAO_FINAL.md'


def _linhas(arq: str, a: int, b: int) -> list[str]:
    return (RAIZ / arq).read_text(encoding='utf-8').splitlines()[a - 1:b]


def demandas() -> pd.DataFrame:
    """As 11 demandas, lidas da tabela do registro (estado_demandas, linhas 16–26)."""
    out = []
    for ln in _linhas(E, 16, 26):
        c = [x.strip() for x in ln.strip('|').split('|')]
        out.append(dict(n=int(c[0]), demanda=c[1], fase=c[2], estado=c[3], onde=c[4]))
    return pd.DataFrame(out)


def cenarios() -> pd.DataFrame:
    return pd.read_csv(AMPL / 'cenarios.csv', sep=';', encoding='utf-8-sig').set_index('cenario')


def linhas_cenarios(ids, cols):
    c = cenarios().loc[ids]
    f = {'n': intbr, 'perdidos_vs_S0': intbr, 'kmo': lambda v: br(v, 3),
         'var_explicada_2f': lambda v: br(v, 2) + '%', 'fatores_kaiser': lambda v: str(int(v)),
         'fatores_horn': lambda v: str(int(v))}
    return [[k, x['descricao']] + [f[col](x[col]) for col in cols] for k, x in c.iterrows()]


def pesos_cenario(cen: str):
    p = pd.read_csv(AMPL / 'pesos.csv', sep=';', encoding='utf-8-sig')
    nome = {'sem_rotacao': 'Sem rotação', 'varimax': 'Varimax', 'promax_padrao': 'Promax, padrão',
            'promax_estrutura': 'Promax, estrutura'}
    return [[nome[r.rotacao], br(r.peso_f1, 2) + '%', br(r.peso_f2, 2) + '%',
             '—' if pd.isna(r.phi) else br(r.phi, 3)] for r in p[p['cenario'] == cen].itertuples()]


def dm(n: int, caixas, cab, linhas, colW, resultado_em, fonte_texto, fontes) -> dict:
    d = demandas().set_index('n').loc[n]
    return dict(titulo=f'Demanda {n} — {d["demanda"]}', parte='DM', requisito='R2, R3',
                sub=f'Redação do registro: "{d["demanda"]}" · estado: {d["estado"]}',
                caixas=[['Pedido', f'{d["demanda"][0].upper() + d["demanda"][1:]} (redação do registro).']]
                + caixas, cab=cab, linhas=linhas, colW=colW, resultado_em=resultado_em,
                fonte_texto=[f'{E}:{15 + n}'] + fonte_texto, fontes=[f'{E}:{15 + n}'] + fontes)


def dm03():
    q = QUADRO.groupby('dimensao')['entra_no_ivs7'].agg(total='size', ivs=lambda s: (s == 'Sim').sum())
    linhas = [[k, int(r.total), int(r.ivs)] for k, r in q.iterrows()]
    linhas.append(['Total', int(q['total'].sum()), int(q['ivs'].sum())])
    return dm(2, [['Como lemos', 'Uma leitura só.'],
                  ['O que foi feito', 'scripts/gerar_quadro_indicadores.py monta o Quadro_Indicadores '
                   '(csv, xlsx e md) a partir de TODOS_INDICADORES, com numerador, denominador e a '
                   'descrição oficial do IBGE por código V.'],
                  ['O que contornamos', 'Nenhum contorno. O quadro foi ampliado no NB05: TODOS_INDICADORES '
                   'sobe de 26 para 28, com pct_so_sanitario e pct_banheiro_comum.']],
              ['Dimensão', 'Indicadores', 'No IVS-7'], linhas, [2.83, 1.3, 1.3],
              f'{ID_DS[ordem_ds()[0]]}–{ID_DS[ordem_ds()[-1]]} (a definição em cada slide)',
              [f'{E}:122-125', f'{NB05}:1', f'{NB05}:234-245'],
              [f'{E}:122-125', 'banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv'])


def dm04():
    return dm(3, [['Como lemos', 'Qual rotação? Rodamos as duas: sem rotação, Varimax e promax lado a '
                   'lado (a demanda 11 já pede isso).'],
                  ['O que foi feito', 'rodar_cenario em src/ivs_censo/fatorial.py (um cenário inteiro, com o '
                   'sinal orientado em sem rotação, Varimax e promax) e scripts/fatorial_ampliada.py, com a '
                   'grade de 15 cenários.'],
                  ['O que contornamos', 'O bootstrap saiu, como pedido. Para a incerteza entrou a '
                   'sensibilidade de um município de fora por vez (S0, S1, S6).']],
              ['Rotação (S0)', 'Peso F1', 'Peso F2', 'Φ'], pesos_cenario('S0'), [2.03, 1.2, 1.2, 1.0],
              'FP02 e FP09', [f'{E}:28-61', f'{E}:140-148'],
              [f'{E}:39-40, 140-148', 'banco_de_dados/eda/fatorial_ampliada/pesos.csv (S0)'])


def dm05():
    cont, sec = {}, None
    for ln in _linhas(MAPA, 1, 200):
        if ln.startswith('## '):
            sec = ln[3:].strip()
        elif sec in ('ATUAL', 'SUPERADO', 'HISTÓRICO') and ln.startswith('| ') and not ln.startswith('| arquivo'):
            cont[sec] = cont.get(sec, 0) + 1
    linhas = [[k, v] for k, v in cont.items()]
    return dm(4, [['Como lemos', 'Uma leitura só: classificar cada material em ATUAL, SUPERADO ou HISTÓRICO, '
                   'sem mover nem apagar nada. Quem decide é o Pedro.'],
                  ['O que foi feito', 'scripts/inventario_apresentacao.py gerou o MAPA_APRESENTACAO_FINAL.md; '
                   'o deck da fatorial (98 slides) foi corrigido e ganhou o bloco da fatorial ampliada; '
                   'guia de apoio em PDF.'],
                  ['O que contornamos', 'O deck de 98 slides não é 100% reproduzível por script (base gerada, '
                   'slides anexados e edição manual). O bloco novo foi anexado ao fim pelo juntador, sem '
                   'regerar o deck.']],
              ['Classe', 'Arquivos'], linhas, [3.43, 2.0], 'o mapa da apresentação final (documento do projeto)',
              [f'{MAPA}:1-79'], [f'{MAPA} (contagem das três tabelas)'])


def dm06():
    c = pd.read_csv(AMPL / 'comparacao_nao_chega_banheiro.csv', sep=';', encoding='utf-8-sig')
    sp = c[(c['bloco'] == 'spearman') & (c['indicador'] == 'Água não chega')]
    linhas = [[r.variavel, br(r.valor, 3), intbr(r.n)] for r in sp.itertuples()]
    return dm(5, [['Como lemos', 'Duas leituras, as duas feitas: (a) contra as outras categorias de '
                   'canalização; (b) contra os indicadores do IVS-7.'],
                  ['O que foi feito', 'Cenário S2 (IVS-7 + não chega) na grade; Spearman de "água não chega" '
                   'com o IVS-7 e com as outras categorias de água; perfil dos setores com valor > 0 × = 0.'],
                  ['O que contornamos', 'Os 85,7% de zeros citados antes usavam os 104.108 setores como '
                   'denominador, contando o faltante como não zero. Sobre os valores presentes, são 94,5%.']],
              ['Água não chega × …', 'Spearman', 'Setores'], linhas, [3.13, 1.1, 1.2], 'FP03',
              [f'{E}:28-61', f'{E}:288-293'],
              [f'{E}:41-42, 290-293', 'banco_de_dados/eda/fatorial_ampliada/comparacao_nao_chega_banheiro.csv (bloco spearman)'])


def dm07():
    c = pd.read_csv(AMPL / 'comparacao_nao_chega_banheiro.csv', sep=';', encoding='utf-8-sig')
    pj = c[c['bloco'] == 'prova_juncao'].iloc[0]
    bp = pd.read_csv(AMPL / 'banheiro_particao.csv', sep=None, engine='python', encoding='utf-8-sig')
    col = [k for k in bp.columns if k.startswith('bate')][0]
    bate = bp[col].astype(str).str.lower().isin(['true', '1', 'sim'])
    linhas = [['V00238 ≤ V00495', intbr(pj['valor'])],
              ['V00495 = V00236 + V00237 + V00238', f'{intbr(bate.sum())} de {intbr(bp[col].notna().sum() if bp[col].dtype == bool else bate.sum() + (bp[col].astype(str).str.lower().isin(["false", "0", "não"])).sum())}']]
    return dm(6, [['Como lemos', 'Usamos a V00495, que já contém a V00238 (conferido no banco). A versão '
                   'graduada, com V00237, exigia reextração do NB01 e ficou em aberto na época.'],
                  ['O que foi feito', 'Cenário S4 (IVS-7 + sem banheiro, V00495) e a prova V00238 ≤ V00495. '
                   'Depois, no NB05, a V00237 foi extraída e o banheiro graduado entrou na grade.'],
                  ['O que contornamos', 'Obstáculo: a V00237 não estava na base. Saída: reextração no NB01, '
                   'sem gravar o notebook. A partição V00495 = V00236 + V00237 + V00238 fecha em 91.199 de '
                   '91.199 setores.']],
              ['Teste', 'Setores em que vale'], linhas, [3.43, 2.0],
              f"FP04 e {ID_DS['banheiro_graduado']} (o banheiro graduado)",
              [f'{E}:28-61', f'{NB05}:1', f'{NB05}:195-245'],
              [f'{E}:43-45', f'{NB05}:195-245', 'comparacao_nao_chega_banheiro.csv (prova_juncao)',
               'banco_de_dados/eda/fatorial_ampliada/banheiro_particao.csv'])


def dm08():
    return dm(7, [['Como lemos', 'Uma variável nova por vez sobre o IVS-7: não chega (S2), sem canalização '
                   '(S3), sem banheiro (S4).'],
                  ['O que foi feito', 'Três cenários na grade da fatorial ampliada, cada um uma fatorial '
                   'completa sobre a mesma regra de setores.'],
                  ['O que contornamos', 'Cada variável nova perde setores diferentes; cada cenário tem o seu '
                   'n, comparado com o S0 na coluna perdidos_vs_S0.']],
              ['Cenário', 'Descrição', 'Setores', 'Perdidos', 'KMO'],
              linhas_cenarios(['S0', 'S2', 'S3', 'S4'], ['n', 'perdidos_vs_S0', 'kmo']),
              [0.85, 1.98, 0.9, 0.9, 0.8], 'FP05', [f'{E}:140-148'],
              ['banco_de_dados/eda/fatorial_ampliada/cenarios.csv (n, perdidos_vs_S0, kmo)'])


def dm09():
    return dm(8, [['Como lemos', 'IVS-7 + não chega + sem canalização + sem banheiro + não convencional '
                   '(pergunta 6, sem confirmação registrada).'],
                  ['O que foi feito', 'S6 (as quatro juntas) e S7 (S6 sem lixo); o S6 também com as três '
                   'rendas e com postos dentro do município.'],
                  ['O que contornamos', 'Nenhum contorno de dado. A leitura de "tudo isso" é nossa e está '
                   'registrada como pergunta à orientadora.']],
              ['Cenário', 'Descrição', 'Setores', 'KMO', 'Var. 2 f.'],
              linhas_cenarios(['S6', 'S7', 'S6_renda_sem_extremo', 'S6_renda_mediana_mun', 'S6_postos_mun'],
                              ['n', 'kmo', 'var_explicada_2f']),
              [1.45, 1.53, 0.85, 0.7, 0.9], 'FP06', [f'{E}:28-61'],
              ['banco_de_dados/eda/fatorial_ampliada/cenarios.csv (n, kmo, var_explicada_2f)'])


def dm10():
    c = pd.read_csv(AMPL / 'cargas.csv', sep=';', encoding='utf-8-sig')
    m = c[(c['variavel'] == 'pct_moradia_nao_convencional') & c['cenario'].isin(['S5', 'S6'])]
    linhas = [[r.cenario, br(r.msa, 3), br(r.comunalidade, 3), br(r.pct_zeros, 2) + '%',
               br(r.varimax_f1, 3)] for r in m.itertuples()]
    return dm(9, [['Como lemos', 'Entrou na direção da vulnerabilidade (moradia não convencional), com '
                   'diagnóstico completo, sem excluir por variância baixa.'],
                  ['O que foi feito', 'Cenários S5 (IVS-7 + não convencional) e S6; MSA, comunalidade e % de '
                   'zeros em cargas.csv.'],
                  ['O que contornamos', 'A variável tem variância baixa. Em vez de excluí-la, mostramos o '
                   'diagnóstico; manter ou não é decisão da orientadora.']],
              ['Cenário', 'MSA', 'Comunalidade', '% de zeros', 'Carga Varimax F1'], linhas,
              [0.9, 0.8, 1.2, 1.1, 1.43], 'FP07', [f'{E}:28-61', f'{E}:318-324'],
              [f'{E}:46-48, 318-324', 'banco_de_dados/eda/fatorial_ampliada/cargas.csv (moradia não convencional)'])


def dm11():
    return dm(10, [['Como lemos', 'Uma leitura só: rodar com e sem o lixo.'],
                   ['O que foi feito', 'S1 (IVS-7 sem lixo) e S7 (S6 sem lixo); se o lixo forma fator '
                    'próprio na Varimax e se isso muda ao tirar um município (lixo_muda).'],
                   ['O que contornamos', 'Nenhum contorno. Registro: em S0, o lixo muda de fator em duas '
                    'rodadas de um município de fora.']],
               ['Cenário', 'Descrição', 'Setores', 'Kaiser', 'Horn'],
               linhas_cenarios(['S0', 'S1'], ['n', 'fatores_kaiser', 'fatores_horn']),
               [0.85, 2.28, 0.9, 0.7, 0.7], 'FP08', [f'{E}:288-306'],
               ['banco_de_dados/eda/fatorial_ampliada/cenarios.csv', f'{E}:301'])


def dm12():
    return dm(11, [['Como lemos', 'Varimax e promax; na promax, as duas métricas (matriz padrão e matriz '
                    'estrutura), sem dizer que uma se afasta ou se aproxima da literatura.'],
                   ['O que foi feito', 'pesos.csv com Varimax e promax (padrão e estrutura) e Φ, em todos os '
                    'cenários; figura fa_plano_s6.png.'],
                   ['O que contornamos', 'O posicionador de rótulos da figura veio do NB04; a figura foi '
                    'conferida rótulo a rótulo antes de ir para slide.']],
               ['Rotação (S1)', 'Peso F1', 'Peso F2', 'Φ'], pesos_cenario('S1'), [2.03, 1.2, 1.2, 1.0],
               'FP09', [f'{E}:28-61', f'{E}:288-306', f'{E}:343-347'],
               [f'{E}:53-55, 302-304, 344-347', 'banco_de_dados/eda/fatorial_ampliada/pesos.csv (S1)'])


DM_SLIDE = {n: f'DM{n + 1:02d}' for n in range(1, 12)}
RESULTADO = {1: f"{ID_DS['renda_media_mediana_mun']}, FP01", 2: 'DS03–DS33', 3: 'FP02, FP09', 4: 'MAPA',
             5: 'FP03', 6: 'FP04', 7: 'FP05', 8: 'FP06', 9: 'FP07', 10: 'FP08', 11: 'FP09'}


def dm00():
    return dict(titulo='As demandas e como foram cobertas', parte='DM', requisito='R2, R3', numero='1',
                sub='As 11 demandas de setembro, uma por slide: o pedido, como lemos, o que foi feito, '
                    'o que contornamos e onde está o resultado', fontes=[f'{E}:16-26'])


def dm01():
    d = demandas()
    linhas = [[r.n, r.demanda, r.estado, DM_SLIDE[r.n], RESULTADO[r.n]] for r in d.itertuples()]
    return dict(titulo='As 11 demandas', parte='DM', requisito='R2',
                sub='Redação do registro, estado e onde está cada uma', cab=['Nº', 'Demanda (registro)',
                'Estado', 'Slide', 'Resultado em'], linhas=linhas, colW=[0.5, 3.6, 4.1, 0.9, 2.53],
                fontes=[f'{E}:16-26'])


def dm13():
    linhas = []
    for ln in _linhas(NB05, 23, 31):
        c = [x.strip().replace('**', '') for x in ln.strip('|').split('|')]
        linhas.append([c[0], c[1], c[2]])
    return dict(titulo='Os desdobramentos no NB05', parte='DM', requisito='R2',
                sub='Origem: estado do NB05 — não são demandas diretas da orientadora (A CONFERIR com o Pedro)',
                cab=['Item', 'O que é', 'Fase e estado'], linhas=linhas, colW=[0.6, 5.6, 5.43],
                fontes=[f'{NB05}:23-31'])


def dm14(slides: dict):
    linhas = []
    for n in range(1, 12):
        x = slides[DM_SLIDE[n]]
        txt = dict(x['caixas'])['O que contornamos']
        if txt.startswith('Nenhum contorno.') and len(txt) < 20:
            continue
        linhas.append([n, x['titulo'].split(' — ', 1)[1], txt, DM_SLIDE[n]])
    return dict(titulo='Tudo o que contornamos', parte='DM', requisito='R3',
                sub='O obstáculo, a saída adotada e o efeito, demanda a demanda (o mesmo texto dos slides DM02–DM12)',
                cab=['Nº', 'Demanda', 'Obstáculo, saída e efeito', 'Slide'], linhas=linhas,
                colW=[0.5, 2.3, 7.93, 0.9], fontes=['caixas "O que contornamos" de DM02–DM12'])


def dm15():
    itens, atual = [], None
    for ln in _linhas(E, 28, 61):
        m = re.match(r'^(\d)\. \*\*(.+?):\*\* ?(.*)$', ln.strip())
        if m:
            atual = [m.group(1), m.group(2), m.group(3)]
            itens.append(atual)
        elif atual and ln.startswith('   ') and ln.strip():
            atual[2] += ' ' + ln.strip()
        elif not ln.strip() or ln.startswith('E três') or ln.startswith('Abraço'):
            atual = None
    linhas = [[a, b.replace('**', ''), c.replace('**', '')] for a, b, c in itens]
    return dict(titulo='As perguntas à orientadora', parte='DM', requisito='R2, R3',
                sub='Enviadas na Fase 0, com o padrão seguido em cada uma. Nenhuma resposta registrada (A CONFERIR)',
                cab=['Nº', 'Ponto', 'Padrão seguido enquanto não há resposta'], linhas=linhas,
                colW=[0.45, 2.6, 8.58], fontes=[f'{E}:28-61', f'{E}:63 (Decisões tomadas: vazia)'])


def a03():
    f = pd.read_csv(TAB / 'T01_funil.csv').set_index('etapa')['setores']
    n0 = intbr(cenarios().loc['S0', 'n'])
    linhas = [['1', 'As demandas e como foram cobertas', 'DM00–DM15', '—'],
              ['2', 'Descritiva dos indicadores, um por slide', 'DS00–DS34', intbr(f['Dados_sig = OK'])],
              ['3', 'Descritiva da análise fatorial (referência proposta)', 'FA00–FA16',
               intbr(f['Componentes do índice completos'])],
              ['4', 'O que a orientadora pediu da fatorial', 'FP00–FP13', f'{n0} (S0) e o n de cada cenário'],
              ['—', 'Fechamento: o que está em aberto', 'Z02', '—']]
    return dict(titulo='Roteiro', parte='A', requisito='R1, R13', sub='Quatro partes, cada uma com os seus códigos',
                cab=['Parte', 'O que tem', 'Códigos', 'Setores'], linhas=linhas, colW=[0.8, 5.6, 1.7, 3.53],
                fontes=['analises_exploratorias/00_referencia/tabelas/T01_funil.csv',
                        'banco_de_dados/eda/fatorial_ampliada/cenarios.csv (S0)'])


# ── Lotes 2 a 5 ──────────────────────────────────────────────────────────────────
T = lambda nome: pd.read_csv(next(TAB.glob(f'{nome}_*.csv')))
ESP = RAIZ / 'banco_de_dados' / 'eda' / 'ivs_especificacoes'
F_T = 'analises_exploratorias/00_referencia/tabelas/'
SELO = 'Referência proposta no NB05 — proposta, não escolhida; a escolha é da orientadora'
ROT_IVS = {r.variavel: r.rotulo for r in T('T20').itertuples()}


def divisoria(num, titulo, sub, fontes, parte, req):
    return dict(titulo=titulo, parte=parte, requisito=req, numero=num, sub=sub, fontes=fontes)


def vertical(pares, cab):
    return dict(cab=cab, linhas=[[a, b] for a, b in pares])


# ── DS ──
def ds00():
    return divisoria('2', 'Descritiva dos indicadores', 'Um indicador por slide, nos 104.108 setores urbanos '
                     'com Dados_sig = OK: como é calculado, de que arquivo vem e como se distribui. Sem cruzar '
                     'indicadores.', [F_T + 'T03_descritivas_global.csv'], 'DS', 'R4, R5')


def ds02():
    linhas = [[T02.loc[i, 'rotulo'], intbr(T02.loc[i, 'n_validos']), intbr(T02.loc[i, 'n_faltantes']),
               br(T02.loc[i, 'pct_faltantes'], 2) + '%'] for i in ordem_ds()]
    return dict(titulo='Setores com valor, indicador a indicador', parte='DS', requisito='R4, R10',
                sub='Faltante = setor da base sem o dado (sigilo ou denominador zero)',
                cab=['Indicador', 'Com valor', 'Faltantes', '%'], linhas=linhas,
                fontes=[F_T + 'T02_perdas_por_indicador.csv'])


def ds34():
    return dict(titulo='Por município e por região', parte='DS', requisito='R4, R10',
                sub='As mesmas estatísticas, por recorte, ficam no anexo — sem gráfico',
                blocos=[['Anexo.', 'A planilha Relatorio_Descritivo_numeros.xlsx, entregue junto com este relatório.'],
                        ['Aba Por_municipio.', f'Os 31 indicadores nos 70 municípios ({intbr(len(pd.read_csv(TAB / "T05_descritivas_municipio.csv")))} linhas), '
                         'com as mesmas colunas da tabela dos slides DS.'],
                        ['Aba Por_regiao.', 'Os 31 indicadores nas cinco regiões.'],
                        ['Aba Descritivas.', 'A tabela dos slides DS com precisão total, mais a definição, o '
                         'arquivo do Censo e o local do cálculo.']],
                fontes=[F_T + 'T04_descritivas_regiao.csv', F_T + 'T05_descritivas_municipio.csv'])


# ── FA ──
def _base_fatorial(base):
    cols = list(T('T20')['variavel'])
    d = base.df.dropna(subset=cols)
    assert len(d) == int(T('T01')['setores'].iloc[-1]), 'amostra da fatorial não bate com a T01'
    return d, cols


def fa00():
    r = pd.read_csv(ESP / 'referencia.csv').set_index('leitura').loc['principal']
    txt = (f"Renda {r['renda']} · lixo {r['lixo']} · banheiro {r['banheiro']} · rotação {r['rotacao']} · "
           f"pesos {r['metodo'].replace('_', '/')} · normalização {r['normalizacao']}. {SELO}.")
    return divisoria('3', 'Descritiva da análise fatorial', txt,
                     ['banco_de_dados/eda/ivs_especificacoes/referencia.csv (leitura principal)'], 'FA', 'R7')


def fa01():
    f = T('T01')
    linhas = [[ROT_IVS[v], intbr(T02.loc[v if v != 'renda_inv' else 'renda_media', 'n_faltantes'])]
              for v in T('T20')['variavel']]
    return dict(titulo='A amostra da fatorial', parte='FA', requisito='R7', sub=SELO,
                cab=['Variável', 'Faltantes nos 104.108'], linhas=linhas, colW=[3.4, 2.4],
                frases=[f"Entram {intbr(f['setores'].iloc[-1])} setores: os {intbr(f['setores'].iloc[-2])} da "
                        f"descritiva menos {intbr(f['saem'].iloc[-1])} com algum dos sete componentes faltante.",
                        'Um setor sai se faltar qualquer um deles (exclusão por lista).'],
                fontes=[F_T + 'T01_funil.csv', F_T + 'T02_perdas_por_indicador.csv',
                        F_T + 'T20_variaveis_cargas.csv (variáveis)'])


def fa02(d, cols):
    from ivs_censo.fatorial import matriz_correlacao
    R = matriz_correlacao(d[cols].to_numpy(), 'spearman')
    rot = [ROT_IVS[c] for c in cols]
    curto = [x.split(' (')[0][:14] for x in rot]
    linhas = [[rot[i]] + ['1' if i == j else br(R[i, j], 3) for j in range(len(cols))] for i in range(len(cols))]
    iu = np.triu_indices(len(cols), 1)
    k = int(np.argmax(np.abs(R[iu])))
    a, b = iu[0][k], iu[1][k]
    return dict(titulo='A matriz de correlação de entrada', parte='FA', requisito='R7',
                sub=f'Spearman, {intbr(len(d))} setores · {SELO}', cab=[''] + curto, linhas=linhas,
                colW=[2.3] + [1.333] * 7,
                frases=[f'A maior correlação fora da diagonal, em módulo, é {br(R[a, b], 3)}, entre '
                        f'{rot[a]} e {rot[b]}.', 'A fatorial usa a correlação de Spearman.'],
                notas='Recalculada por fa02() com matriz_correlacao(X, "spearman") de src/ivs_censo/fatorial.py:394, '
                      'na base de montar_base(00_referencia) com os sete componentes completos.',
                fontes=['src/ivs_censo/fatorial.py:394-400 (matriz_correlacao) e 579-594 (rodar_cenario)',
                        'base: Base_ELSI_70Municipios_Censo2022.db, recorte da 00_referencia'])


def fa03():
    t = T('T19').set_index('medida')['valor']
    fm = {'setores (n)': intbr, 'variáveis (p)': intbr, 'KMO': lambda v: br(v, 4),
          'Bartlett qui-quadrado': lambda v: br(v, 2), 'Bartlett graus de liberdade': intbr,
          'determinante de R': lambda v: br(v, 4)}
    pares = [(k, fm.get(k, lambda v: br(v, 2))(v)) for k, v in t.items()]
    return dict(titulo='Adequação dos dados à fatorial', parte='FA', requisito='R7', sub=SELO,
                **vertical(pares, ['Medida', 'Valor']), colW=[3.8, 2.2],
                frases=[f"KMO de {br(t['KMO'], 4)}; Bartlett com qui-quadrado de {br(t['Bartlett qui-quadrado'], 2)} "
                        f"e {intbr(t['Bartlett graus de liberdade'])} graus de liberdade."],
                fontes=[F_T + 'T19_adequacao_fatorial.csv'])


def _t20(cols, cab, fmt=lambda v: br(v, 3)):
    t = T('T20')
    return [[r['rotulo']] + [fmt(r[c]) for c in cols] for _, r in t.iterrows()], ['Variável'] + cab


def fa04():
    linhas, cab = _t20(['msa', 'comunalidade', 'comunalidade_obliqua'], ['MSA', 'Comunalidade', 'Comunalidade (oblíqua)'])
    t = T('T20')
    i, j = t['msa'].idxmin(), t['comunalidade'].idxmin()
    return dict(titulo='MSA e comunalidade por variável', parte='FA', requisito='R7', sub=SELO,
                cab=cab, linhas=linhas, colW=[2.4, 1.1, 1.4, 1.8],
                frases=[f"Menor MSA: {t.loc[i, 'rotulo']} ({br(t.loc[i, 'msa'], 3)}).",
                        f"Menor comunalidade: {t.loc[j, 'rotulo']} ({br(t.loc[j, 'comunalidade'], 3)})."],
                fontes=[F_T + 'T20_variaveis_cargas.csv (msa, comunalidade, comunalidade_obliqua)'])


def fa06():
    t = T('T19').set_index('medida')['valor']
    k = T('T23')['dimensao'].nunique()
    pares = [('Critério de Kaiser (autovalor > 1)', intbr(t['fatores pelo critério de Kaiser'])),
             ('Análise paralela de Horn', intbr(t['fatores pela análise paralela de Horn'])),
             ('Retidos na solução', intbr(k))]
    return dict(titulo='Quantos fatores', parte='FA', requisito='R7', sub=SELO,
                **vertical(pares, ['Critério', 'Fatores']), colW=[4.2, 1.6],
                frases=[f"Kaiser e Horn indicam {intbr(t['fatores pelo critério de Kaiser'])} e "
                        f"{intbr(t['fatores pela análise paralela de Horn'])}; a solução retém {intbr(k)}, que "
                        f"explicam {br(t['variância explicada por 2 fatores (%)'], 2)}% da variância."],
                fontes=[F_T + 'T19_adequacao_fatorial.csv', F_T + 'T23_pesos.csv (dimensões)'])


def _cargas(sid, pref, nome):
    linhas, cab = _t20([f'{pref}_f1', f'{pref}_f2'], ['F1', 'F2'])
    t = T('T20')
    f1 = t.loc[t[f'{pref}_f1'].abs().idxmax(), 'rotulo']
    f2 = t.loc[t[f'{pref}_f2'].abs().idxmax(), 'rotulo']
    return dict(titulo=f'Cargas {nome}', parte='FA', requisito='R7', sub=SELO, cab=cab, linhas=linhas,
                colW=[2.6, 1.2, 1.2], frases=[f'Maior carga em F1: {f1}. Maior carga em F2: {f2}.'],
                fontes=[F_T + f'T20_variaveis_cargas.csv ({pref}_f1, {pref}_f2)'])


def fa07():
    return _cargas('FA07', 'sem_rotacao', 'sem rotação')


def fa08():
    return _cargas('FA08', 'varimax', 'Varimax')


def fa09():
    linhas, cab = _t20(['promax_padrao_f1', 'promax_padrao_f2', 'promax_estrutura_f1', 'promax_estrutura_f2'],
                       ['Padrão F1', 'Padrão F2', 'Estrutura F1', 'Estrutura F2'])
    return dict(titulo='Cargas promax: matriz padrão e matriz estrutura', parte='FA', requisito='R7', sub=SELO,
                cab=cab, linhas=linhas, colW=[1.9, 1.1, 1.1, 1.15, 1.15],
                figura=copiar_figura('F23_mapa_cargas.png', 'FA09'), legenda='Mapa das cargas da referência.',
                frases=['A matriz padrão dá o efeito próprio de cada fator; a estrutura, a correlação da '
                        'variável com o fator. As duas são reportadas (pergunta 7 à orientadora).'],
                fontes=[F_T + 'T20_variaveis_cargas.csv (promax_*)', 'F23_mapa_cargas.png'])


def fa10():
    t = pd.read_csv(TAB / 'T22_phi.csv', index_col=0)
    linhas = [[i] + [br(v, 3) for v in r] for i, r in t.iterrows()]
    return dict(titulo='Correlação entre os fatores (Φ)', parte='FA', requisito='R7', sub=SELO,
                cab=[''] + list(t.columns), linhas=linhas, colW=[1.2, 1.4, 1.4],
                frases=[f"Na promax, F1 e F2 têm correlação de {br(t.iloc[0, 1], 3)}."],
                fontes=[F_T + 'T22_phi.csv'])


def fa11():
    t = T('T23')
    linhas = [[r.rotulo, r.dimensao, br(r.carga, 3), br(r.peso_dimensao, 0) + '%', br(r.peso, 2) + '%']
              for r in t.itertuples()]
    return dict(titulo='Os pesos do índice', parte='FA', requisito='R7', sub=SELO,
                cab=['Variável', 'Dimensão', 'Carga', 'Peso da dimensão', 'Peso no índice'], linhas=linhas,
                colW=[2.4, 2.2, 0.9, 1.6, 1.5],
                frases=[f"As dimensões pesam {' e '.join(br(v, 0) + '%' for v in t.groupby('dimensao')['peso_dimensao'].first())}; "
                        f"o maior peso no índice é de {t.loc[t['peso'].idxmax(), 'rotulo']} "
                        f"({br(t['peso'].max(), 2)}%)."],
                fontes=[F_T + 'T23_pesos.csv'])


def fa12():
    r = T('T24').set_index('escopo').loc['Total']
    pares = [('Setores', intbr(r['n'])), ('Média', br(r['media'], 4)), ('Desvio-padrão', br(r['dp'], 4)),
             ('Mínimo', br(r['min'], 4)), ('P10', br(r['p10'], 4)), ('P25', br(r['p25'], 4)),
             ('Mediana', br(r['mediana'], 4)), ('P75', br(r['p75'], 4)), ('P90', br(r['p90'], 4)),
             ('Máximo', br(r['max'], 4)), ('Assimetria', br(r['assim'], 2))]
    return dict(titulo='O índice da referência proposta', parte='FA', requisito='R7', sub=SELO,
                **vertical(pares, ['Estatística', 'Valor']), colW=[2.6, 1.6],
                figura=copiar_figura('F24_histograma_por_faixa.png', 'FA12'),
                legenda='Histograma do índice, colorido pela faixa.',
                frases=[f"Metade dos setores tem índice até {br(r['mediana'], 4)}; entre o P10 e o P90, vai de "
                        f"{br(r['p10'], 4)} a {br(r['p90'], 4)}. As regiões estão no anexo (aba Fatorial)."],
                fontes=[F_T + 'T24_indice_descritivas.csv (Total)', 'F24_histograma_por_faixa.png'])


def fa13():
    t = T('T25')
    nome = {'ivs_bh': 'IVS-BH', 'quartis': 'Quartis'}
    fx = {'indefinida': 'indefinida', 'baixo': 'baixo', 'medio': 'médio', 'elevado': 'elevado',
          'muito_elevado': 'muito elevado'}
    linhas = [[nome[r.regra], fx[r.faixa], intbr(r.setores), br(r.pct, 2) + '%'] for r in t.itertuples()]
    me = t[(t['regra'] == 'ivs_bh') & (t['faixa'] == 'muito_elevado')].iloc[0]
    return dict(titulo='As faixas, pelas duas regras', parte='FA', requisito='R7', sub=SELO,
                cab=['Regra', 'Faixa', 'Setores', '%'], linhas=linhas, colW=[1.5, 1.8, 1.3, 1.2],
                frases=[f"Pela regra do IVS-BH, {intbr(me['setores'])} setores ({br(me['pct'], 2)}%) ficam na "
                        f"faixa muito elevada; pelos quartis, cada faixa tem cerca de um quarto."],
                fontes=[F_T + 'T25_faixas.csv'])


def fa14():
    t = T('T26').set_index('medida')
    pares = [('AUC global contra FCU', br(t.loc['AUC global contra FCU', 'valor'], 4)),
             ('AUC municipal (mediana)', br(t.loc['AUC municipal (mediana)', 'valor'], 4)),
             ('Municípios na AUC municipal', intbr(t.loc['municípios na AUC municipal', 'valor']))]
    return dict(titulo='Validação contra as favelas (FCU)', parte='FA', requisito='R7', sub=SELO,
                **vertical(pares, ['Medida', 'Valor']), colW=[3.6, 1.6],
                figura=copiar_figura('F25_curva_roc.png', 'FA14'), legenda='Curva ROC do índice contra FCU.',
                frases=[f"Critério da AUC municipal: {t.loc['municípios na AUC municipal', 'detalhe']}."],
                fontes=[F_T + 'T26_auc_e_elegibilidade.csv', 'F25_curva_roc.png'])


def fa15():
    t = T('T27')
    e = t[t['entra_na_mediana'] == True].sort_values('auc')  # noqa: E712
    fig, ax = plt.subplots(figsize=(4.6, 4.2), dpi=150)
    ax.scatter(e['auc'], range(len(e)), s=14, color=PETROLEO)
    ax.axvline(e['auc'].median(), color=ARGILA, linestyle='--', linewidth=1)
    ax.set_yticks(range(len(e)))
    ax.set_yticklabels(e['NM_MUN'], fontsize=5.5)
    ev.estilo(ax, 'AUC contra FCU', '')
    fig.savefig(FIG / 'FA15.png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    pares = [('Municípios com AUC calculada', intbr(t['auc'].notna().sum())),
             ('Entram na mediana', intbr(len(e))), ('Mediana', br(e['auc'].median(), 4)),
             ('Menor', f"{br(e['auc'].min(), 4)} ({e.iloc[0]['NM_MUN']})"),
             ('Maior', f"{br(e['auc'].max(), 4)} ({e.iloc[-1]['NM_MUN']})")]
    return dict(titulo='AUC por município', parte='FA', requisito='R7', sub=SELO,
                **vertical(pares, ['Medida', 'Valor']), colW=[2.8, 2.4], figura='figuras/FA15.png',
                legenda='Os municípios que entram na mediana; tracejado = mediana. A lista completa está no anexo.',
                frases=['Entram na mediana só os municípios com ao menos 30 setores de FCU e 30 fora.'],
                fontes=[F_T + 'T27_auc_por_municipio.csv', F_T + 'T26_auc_e_elegibilidade.csv'])


def fa16():
    t = T('T26').iloc[3:]
    linhas = [[r.medida, br(r.valor, 4) if r.valor not in (0.0, 1.0) or 'peso' in r.medida else ('sim' if r.valor == 1 else 'não'),
               '' if pd.isna(r.detalhe) else r.detalhe] for r in t.itertuples()]
    return dict(titulo='Elegibilidade pelos critérios do NB05', parte='FA', requisito='R7', sub=SELO,
                cab=['Critério', 'Valor', 'Detalhe'], linhas=linhas, colW=[4.2, 1.4, 3.0],
                frases=['Os critérios foram fixados antes de rodar a grade do NB05.'],
                fontes=[F_T + 'T26_auc_e_elegibilidade.csv'])


# ── FP ──
def fp00():
    return divisoria('4', 'O que a orientadora pediu da fatorial', 'Um slide por pedido, na ordem das demandas. '
                     'Aqui a comparação entre cenários é o próprio pedido.', [f'{ESTADO_DEM}:16-26'], 'FP', 'R8')


CEN = {'n': ('Setores', intbr), 'kmo': ('KMO', lambda v: br(v, 3)), 'msa_min': ('MSA mín.', lambda v: br(v, 3)),
       'fatores_kaiser': ('Kaiser', lambda v: str(int(v))), 'fatores_horn': ('Horn', lambda v: str(int(v))),
       'var_explicada_2f': ('Var. 2 fatores', lambda v: br(v, 2) + '%'),
       'perdidos_vs_S0': ('Perdidos vs S0', intbr)}


def tab_cen(ids, cols):
    c = cenarios().loc[ids]
    return (['Cenário', 'Descrição'] + [CEN[k][0] for k in cols],
            [[i, x['descricao']] + [CEN[k][1](x[k]) for k in cols] for i, x in c.iterrows()])


def fp_slide(n, titulo, cab, linhas, colW, frases, fontes):
    d = demandas().set_index('n').loc[n] if n else None
    sub = f'Redação do registro: "{d["demanda"]}"' if n else 'Pedido derivado das perguntas à orientadora'
    return dict(titulo=titulo, parte='FP', requisito='R8', sub=sub, cab=cab, linhas=linhas, colW=colW,
                frases=frases, fontes=fontes)


F_A = 'banco_de_dados/eda/fatorial_ampliada/'


def frase_rendas(v: pd.Series) -> str:
    lo, hi = br(v.min(), 2), br(v.max(), 2)
    if lo == hi:
        return (f'O peso de F1 na Varimax é {lo}% nas três rendas (igual até a segunda casa): a troca '
                f'afeta um setor só.')
    return f'O peso de F1 na Varimax vai de {lo}% a {hi}% entre as três rendas.'


def fp01():
    cab, linhas = tab_cen(['S0', 'S0_renda_sem_extremo', 'S0_renda_mediana_mun'], ['n', 'kmo', 'var_explicada_2f'])
    p = pd.read_csv(AMPL / 'pesos.csv', sep=';', encoding='utf-8-sig')
    p = p[p['rotacao'] == 'varimax'].set_index('cenario')['peso_f1']
    cab.append('Peso F1 (Varimax)')
    for ln in linhas:
        ln.append(br(p[ln[0]], 2) + '%')
    return fp_slide(1, 'Demanda 1 — o efeito das três rendas na fatorial', cab, linhas,
                    [2.3, 3.6, 1.2, 0.9, 1.6, 2.03],
                    [frase_rendas(p[['S0', 'S0_renda_sem_extremo', 'S0_renda_mediana_mun']])],
                    [F_A + 'cenarios.csv', F_A + 'pesos.csv (varimax)'])


def fp02():
    c = pd.read_csv(AMPL / 'cargas.csv', sep=';', encoding='utf-8-sig')
    c = c[c['cenario'] == 'S0']
    linhas = [[r.rotulo, br(r.sem_rotacao_f1, 3), br(r.sem_rotacao_f2, 3), br(r.varimax_f1, 3), br(r.varimax_f2, 3),
               br(r.promax_padrao_f1, 3), br(r.promax_padrao_f2, 3)] for r in c.itertuples()]
    return fp_slide(3, 'Demanda 3 — sem bootstrap, sem e com rotação', ['Variável (S0)', 'Sem rot. F1', 'Sem rot. F2',
                    'Varimax F1', 'Varimax F2', 'Promax F1', 'Promax F2'], linhas, [2.6, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
                    ['As três soluções lado a lado no S0 (IVS-7, NB04); os pesos de cada rotação estão no DM04 e no FP09.'],
                    [F_A + 'cargas.csv (S0)'])


def fp03():
    c = pd.read_csv(AMPL / 'comparacao_nao_chega_banheiro.csv', sep=';', encoding='utf-8-sig')
    p = c[(c['bloco'] == 'perfil_mediana') & (c['indicador'] == 'Água não chega')]
    pv = p.pivot_table(index='variavel', columns='grupo', values='valor', aggfunc='first')
    nn = p.groupby('grupo')['n'].first()
    linhas = [[v] + [br(pv.loc[v, g], 2 if 'Renda' in v else 4) for g in pv.columns] for v in pv.index]
    return fp_slide(5, 'Demanda 5 — o perfil dos setores com e sem "água não chega"',
                    ['Mediana de'] + [f'{g} (n = {intbr(nn[g])})' for g in pv.columns], linhas,
                    [3.4] + [2.6] * len(pv.columns),
                    ['Leitura (a), contra as outras categorias de canalização, e (b), contra o IVS-7: o Spearman está no DM06.'],
                    [F_A + 'comparacao_nao_chega_banheiro.csv (bloco perfil_mediana)'])


def fp04():
    e = pd.read_csv(ESP / 'especificacoes.csv')
    g = e.groupby('banheiro')['elegivel'].agg(['size', 'sum'])
    cab, linhas = tab_cen(['S0', 'S4'], ['n', 'perdidos_vs_S0', 'kmo', 'fatores_kaiser', 'fatores_horn'])
    grade = '; '.join(f"banheiro {k}: {intbr(r['size'])} especificações, {intbr(r['sum'])} elegíveis" for k, r in g.iterrows())
    return fp_slide(6, 'Demanda 6 — o "sem banheiro" na fatorial', cab, linhas, [0.8, 4.0, 1.2, 1.6, 0.9, 0.9, 0.9],
                    ['S4 usa a V00495. No NB05, as três versões do banheiro entram na grade (' + grade + ') e o '
                     'graduado vai para a referência proposta.'],
                    [F_A + 'cenarios.csv', 'banco_de_dados/eda/ivs_especificacoes/especificacoes.csv (banheiro, elegivel)'])


def fp05():
    cab, linhas = tab_cen(['S0', 'S2', 'S3', 'S4'], ['n', 'kmo', 'msa_min', 'fatores_kaiser', 'fatores_horn', 'var_explicada_2f'])
    return fp_slide(7, 'Demanda 7 — canalização e sem banheiro, uma por vez', cab, linhas,
                    [0.8, 3.3, 1.1, 0.9, 1.1, 0.9, 0.9, 1.6],
                    ['Cada cenário acrescenta uma variável ao IVS-7 (S0) e perde os setores sem ela.'], [F_A + 'cenarios.csv'])


def fp06():
    ids = ['S0', 'S6', 'S7', 'S6_renda_sem_extremo', 'S6_renda_mediana_mun', 'S6_postos_mun']
    cab, linhas = tab_cen(ids, ['n', 'kmo', 'fatores_kaiser', 'fatores_horn', 'var_explicada_2f'])
    c = cenarios()
    return fp_slide(8, 'Demanda 8 — tudo isso junto', cab, linhas, [2.3, 3.3, 1.1, 0.9, 0.9, 0.9, 1.6],
                    [f"No S6, Kaiser e Horn indicam {int(c.loc['S6', 'fatores_kaiser'])} e {int(c.loc['S6', 'fatores_horn'])} fatores; "
                     f"a solução fica com 2 em todos os cenários."], [F_A + 'cenarios.csv', f'{ESTADO_DEM}:298-299'])


def fp07():
    cab, linhas = tab_cen(['S0', 'S5', 'S6'], ['n', 'kmo', 'msa_min', 'var_explicada_2f'])
    return fp_slide(9, 'Demanda 9 — a moradia não convencional', cab, linhas, [0.8, 4.2, 1.2, 1.1, 1.2, 1.6],
                    ['O diagnóstico da variável (MSA, comunalidade, % de zeros) está no DM10.'], [F_A + 'cenarios.csv'])


def fp09():
    p = pd.read_csv(AMPL / 'pesos.csv', sep=';', encoding='utf-8-sig')
    p = p[p['cenario'].isin(['S0', 'S1', 'S6'])]
    nome = {'sem_rotacao': 'Sem rotação', 'varimax': 'Varimax', 'promax_padrao': 'Promax, padrão',
            'promax_estrutura': 'Promax, estrutura'}
    linhas = [[r.cenario, nome[r.rotacao], br(r.peso_f1, 2) + '%', br(r.peso_f2, 2) + '%',
               '—' if pd.isna(r.phi) else br(r.phi, 3), r.f1_maior_carga, r.f2_maior_carga] for r in p.itertuples()]
    return fp_slide(11, 'Demanda 11 — as duas rotações', ['Cenário', 'Rotação', 'Peso F1', 'Peso F2', 'Φ',
                    'Maior carga F1', 'Maior carga F2'], linhas, [0.9, 1.8, 1.1, 1.1, 0.8, 2.9, 3.03],
                    ['Promax reportada pelas duas matrizes (padrão e estrutura); Φ só existe na oblíqua.'],
                    [F_A + 'pesos.csv (S0, S1, S6)'])


def fp10():
    s = pd.read_csv(AMPL / 'sensibilidade_municipios.csv', sep=';', encoding='utf-8-sig')
    linhas = []
    for cen, g in s.groupby('cenario', sort=False):
        cheio = g[g['municipio_fora'] == '(nenhum)'].iloc[0]
        r = g[g['municipio_fora'] != '(nenhum)']
        lo, hi = r.loc[r['peso_f1_varimax'].idxmin()], r.loc[r['peso_f1_varimax'].idxmax()]
        linhas.append([cen, intbr(len(r)), br(cheio['peso_f1_varimax'], 2) + '%',
                       f"{br(lo['peso_f1_varimax'], 2)}% (sem {lo['municipio_fora']})",
                       f"{br(hi['peso_f1_varimax'], 2)}% (sem {hi['municipio_fora']})", intbr(r['lixo_muda'].sum())])
    return fp_slide(0, 'Incerteza: um município de fora por vez', ['Cenário', 'Rodadas', 'Peso F1 cheio',
                    'Menor peso F1', 'Maior peso F1', 'Lixo muda'], linhas, [1.0, 1.0, 1.6, 3.0, 3.0, 1.03],
                    ['No lugar do bootstrap (pergunta 9): cada rodada tira um município e refaz a Varimax.'],
                    [F_A + 'sensibilidade_municipios.csv', f'{ESTADO_DEM}:28-61'])


def fp11():
    v = pd.read_csv(AMPL / 'validacao_fcu.csv', sep=';', encoding='utf-8-sig')
    pv = v.pivot_table(index='cenario', columns='medida', values='auc', aggfunc='first', sort=False)
    n = v.groupby('cenario', sort=False)['n'].first()
    linhas = [[c, intbr(n[c])] + [br(pv.loc[c, m], 4) for m in pv.columns] for c in pv.index]
    return fp_slide(0, 'Validação contra FCU, cenário a cenário', ['Cenário', 'Setores'] + list(pv.columns),
                    linhas, [2.4, 1.1] + [8.13 / len(pv.columns)] * len(pv.columns),
                    ['AUC contra os setores de FCU: o índice, a renda invertida sozinha e a média simples de postos.'],
                    [F_A + 'validacao_fcu.csv'])


def fp12():
    e = pd.read_csv(ESP / 'especificacoes.csv')
    linhas = [['Total', '—', intbr(len(e)), intbr(e['elegivel'].sum())]]
    for dim, nome in [('renda', 'Renda'), ('lixo', 'Lixo'), ('banheiro', 'Banheiro'), ('rotacao', 'Rotação'),
                      ('normalizacao', 'Normalização')]:
        for k, g in e.groupby(dim):
            linhas.append([nome, k, intbr(len(g)), intbr(g['elegivel'].sum())])
    return fp_slide(0, 'A grade do NB05', ['Dimensão', 'Opção', 'Especificações', 'Elegíveis'], linhas,
                    [2.4, 3.4, 2.0, 2.0],
                    [f"{intbr(e['elegivel'].sum())} das {intbr(len(e))} especificações passam nos critérios fixados antes de rodar."],
                    ['banco_de_dados/eda/ivs_especificacoes/especificacoes.csv (elegivel)'])


def fp13():
    a = pd.read_csv(ESP / 'acrescimo_renda.csv')
    r = a[a['referencia'] == True].iloc[0]  # noqa: E712
    pares = [('AUC global: índice', br(r['auc_indice_global'], 4)), ('AUC global: renda sozinha', br(r['auc_renda_global'], 4)),
             ('AUC global: média de postos', br(r['auc_postos_global'], 4)),
             ('AUC no município: índice', br(r['auc_indice_mun'], 4)), ('AUC no município: renda', br(r['auc_renda_mun'], 4)),
             ('AUC nos estratos de renda: índice', br(r['auc_indice_estratos'], 4)),
             ('AUC nos estratos de renda: renda', br(r['auc_renda_estratos'], 4)),
             ('Queda da deviance ao somar o índice à renda', br(r['queda_deviance'], 2)), ('z do índice', br(r['z_indice'], 2))]
    k = int((a['auc_indice_global'] > a['auc_renda_global']).sum())
    return dict(titulo='A renda sozinha contra o índice', parte='FP', requisito='R8',
                sub='Pedido derivado do NB05 (item 6 do estado): o que o índice acrescenta à renda',
                **vertical(pares, ['Medida (referência proposta)', 'Valor']), colW=[5.0, 1.8],
                frases=[f'Nas {intbr(len(a))} especificações avaliadas, o índice supera a renda sozinha na AUC global em {intbr(k)}.'],
                fontes=['banco_de_dados/eda/ivs_especificacoes/acrescimo_renda.csv'])


# ── Z ──
def z01(slides: dict):
    linhas = []
    for parte, nome in [('A', 'Abertura'), ('DM', 'Demandas'), ('DS', 'Descritiva'), ('FA', 'Fatorial'),
                        ('FP', 'Pedidos da fatorial')]:
        ids = [k for k, x in slides.items() if x['parte'] == parte]
        fontes = sorted({f.split(' (')[0].split(':')[0] for k in ids for f in slides[k]['fontes'] if '/' in f})
        linhas.append([nome, f'{ids[0]}–{ids[-1]}', '; '.join(f.split('/')[-1] for f in fontes[:6])])
    return dict(titulo='Onde está cada número', parte='Z', requisito='R12, R13',
                sub='Por parte; slide a slide, na aba Indice_slides do anexo e no manifesto',
                cab=['Parte', 'Códigos', 'Arquivos de origem'], linhas=linhas, colW=[2.0, 1.6, 8.03],
                fontes=['relatorio_descritivo/dados/manifesto.csv'])


def z02():
    r = pd.read_csv(ESP / 'referencia.csv')
    linhas = [[x.leitura, x.id, intbr(x.elegiveis)] for x in r.itertuples()]
    return dict(titulo='O que está em aberto', parte='Z', requisito='R2, R7',
                sub='Decisões da orientadora: as perguntas do DM15 e qual especificação adotar',
                cab=['Leitura dos critérios', 'Especificação de melhor posição média', 'Elegíveis'], linhas=linhas,
                colW=[2.4, 7.6, 1.63],
                frases=['As 9 perguntas do DM15 seguem sem resposta registrada. A especificação descrita na parte FA '
                        'é a da leitura principal; as outras três leituras levam às especificações acima.'],
                fontes=['banco_de_dados/eda/ivs_especificacoes/referencia.csv', f'{ESTADO_DEM}:28-63'])


def anexo(slides: dict, manifesto: list) -> None:
    desc = T03.reset_index()
    desc['definicao_numerador'] = [QUADRO.loc[i, 'numerador'] if i in QUADRO.index else EXTRAS[i]['numerador'] for i in desc['indicador']]
    desc['definicao_denominador'] = [QUADRO.loc[i, 'denominador'] if i in QUADRO.index else EXTRAS[i]['denominador'] for i in desc['indicador']]
    desc['arquivo_do_censo'] = [GER.loc[i, 'Arquivo do Censo de origem'] for i in desc['indicador']]
    desc['calculado_em'] = [GER.loc[i, 'Calculado em'] for i in desc['indicador']]
    desc.insert(0, 'slide', [ID_DS[i] for i in desc['indicador']])
    idx = pd.DataFrame(manifesto)[['id', 'parte', 'titulo', 'fontes', 'figura']]
    for c in ['Vai para o artigo? (Sim/Talvez/Não)', 'Seção do artigo', 'Comentários']:
        idx[c] = ''
    with pd.ExcelWriter(SAIDA / 'Relatorio_Descritivo_numeros.xlsx', engine='openpyxl') as w:
        idx.to_excel(w, sheet_name='Indice_slides', index=False)
        desc.to_excel(w, sheet_name='Descritivas', index=False)
        pd.read_csv(TAB / 'T05_descritivas_municipio.csv').to_excel(w, sheet_name='Por_municipio', index=False)
        pd.read_csv(TAB / 'T04_descritivas_regiao.csv').to_excel(w, sheet_name='Por_regiao', index=False)
        pd.read_csv(TAB / 'T12_correlacao_spearman.csv', index_col=0).to_excel(w, sheet_name='Correlacao_Spearman')
        pd.read_csv(TAB / 'T13_correlacao_pearson.csv', index_col=0).to_excel(w, sheet_name='Correlacao_Pearson')
        lin = 0
        for nome in ['T19', 'T20', 'T21', 'T22', 'T23', 'T24', 'T25', 'T26', 'T27']:
            arq = next(TAB.glob(f'{nome}_*.csv'))
            pd.DataFrame([[arq.name]]).to_excel(w, sheet_name='Fatorial', startrow=lin, index=False, header=False)
            t = pd.read_csv(arq)
            t.to_excel(w, sheet_name='Fatorial', startrow=lin + 1, index=False)
            lin += len(t) + 4
        for ws in w.book.worksheets:
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width = min(48, max(10, max(len(str(c.value or '')) for c in col[:60]) + 2))


# ── C-04: mais gráficos por indicador, correlações e cenários da fatorial ─────────
REGIOES_ORD = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
IVS7_COLS = ['pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad', 'razao_moradores', 'pct_analfab',
             'renda_media', 'pct_raca_pretpardind']


def ds_extra(ind: str, base) -> dict:
    """O mesmo indicador por recorte: regiões, os 70 municípios, setores de FCU e os demais.
    Com metade ou mais dos setores em zero, a mediana é zero em quase todo recorte: aí o slide
    mostra a % de setores com valor acima de zero e a média, em vez da caixa e da mediana."""
    sid = ID_DS[ind] + '-2'
    rot = T03.loc[ind, 'rotulo']
    esc = 100 if tipo(ind) == 'proporcao' else 1
    zeros = T03.loc[ind, 'pct_zeros'] >= 50
    df = base.df[[ind, 'regiao', 'is_fcu', 'NM_MUN']].dropna(subset=[ind])
    t4 = pd.read_csv(TAB / 'T04_descritivas_regiao.csv')
    t4 = t4[t4['indicador'] == ind].set_index('regiao')
    t5 = pd.read_csv(TAB / 'T05_descritivas_municipio.csv')
    t5 = t5[t5['indicador'] == ind]
    t15 = pd.read_csv(TAB / 'T15_fcu_por_indicador.csv').set_index('indicador').loc[ind]
    regs = [r for r in REGIOES_ORD if r in t4.index]
    fcu = {'FCU': df[df['is_fcu'] == 1][ind], 'demais': df[df['is_fcu'] == 0][ind]}
    fig, ax = plt.subplots(1, 3, figsize=(10.5, 3.9), dpi=150, gridspec_kw={'width_ratios': [1.15, 1.3, 0.75]})
    if zeros:
        pos = 100 - t4.loc[regs, 'pct_zeros']
        ax[0].barh(regs, pos, color=PETROLEO)
        ax[0].invert_yaxis()
        ev.estilo(ax[0], '% de setores com valor > 0, por região', '')
        t5 = t5.assign(pos=100 - t5['pct_zeros']).sort_values('pos')
        m = t5['pos'].to_numpy()
        ax[1].scatter(m, range(len(m)), s=9, color=PETROLEO)
        ev.estilo(ax[1], '% com valor > 0 em cada município (70)', '')
        pf = [100 * float((fcu[k] > 0).mean()) for k in ('FCU', 'demais')]
        ax[2].barh(['FCU', 'demais'], pf, color=[ARGILA, CINZA])
        ax[2].invert_yaxis()
        ev.estilo(ax[2], '% com valor > 0', '')
    else:
        caixa = dict(patch_artist=True, showfliers=False, widths=0.55, orientation='horizontal',
                     boxprops=dict(facecolor='white', edgecolor=TINTA, linewidth=0.8),
                     medianprops=dict(color=ARGILA, linewidth=1.3), whiskerprops=dict(color=TINTA, linewidth=0.7),
                     capprops=dict(color=TINTA, linewidth=0.7))
        ax[0].boxplot([df.loc[df['regiao'] == r, ind] * esc for r in regs], tick_labels=regs, **caixa)
        ax[0].invert_yaxis()
        ev.estilo(ax[0], 'por região', '')
        t5 = t5.sort_values('mediana')
        m = t5['mediana'].to_numpy() * esc
        ax[1].scatter(m, range(len(m)), s=9, color=PETROLEO)
        ev.estilo(ax[1], 'mediana de cada município (70)', '')
        ax[2].boxplot([fcu['FCU'] * esc, fcu['demais'] * esc], tick_labels=['FCU', 'demais'], **caixa)
        ax[2].invert_yaxis()
        ev.estilo(ax[2], 'favela (FCU) e demais', '')
    ax[1].set_yticks([0, len(m) - 1])
    ax[1].set_yticklabels([t5['NM_MUN'].iloc[0], t5['NM_MUN'].iloc[-1]], fontsize=7)
    for a in ax:
        a.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(FIG / f'{sid}.png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    lo_m, hi_m = t5.iloc[0], t5.iloc[-1]
    if zeros:
        fm = (lambda v: br(v, 4)) if tipo(ind) == 'grau' else (lambda v: fmt(ind, v))   # 0–1 com média pequena
        linhas = [[r, intbr(t4.loc[r, 'n']), fm(t4.loc[r, 'media']), br(100 - t4.loc[r, 'pct_zeros'], 1) + '%']
                  for r in regs]
        linhas += [[f'Setores de {k}' if k == 'FCU' else 'Demais setores', intbr(len(v)), fm(v.mean()),
                    br(100 * (v > 0).mean(), 1) + '%'] for k, v in fcu.items()]
        cab, colW = ['Recorte', 'Setores', 'Média', '% > 0'], [1.45, 0.85, 0.9, 0.78]
        hi = (100 - t4['pct_zeros']).idxmax()
        lo = (100 - t4['pct_zeros']).idxmin()
        frases = [f"Mais da metade dos setores tem valor zero. A maior proporção de setores com valor acima de zero "
                  f"é a do {hi} ({br(100 - t4.loc[hi, 'pct_zeros'], 1)}%); a menor, a do {lo} ({br(100 - t4.loc[lo, 'pct_zeros'], 1)}%).",
                  f"Nos setores de FCU, {br(100 * (fcu['FCU'] > 0).mean(), 1)}% têm valor acima de zero; nos demais, "
                  f"{br(100 * (fcu['demais'] > 0).mean(), 1)}%.",
                  f"Entre os municípios, vai de {br(lo_m['pos'], 1)}% ({lo_m['NM_MUN']}) a {br(hi_m['pos'], 1)}% ({hi_m['NM_MUN']})."]
        leg = 'Barras e pontos: % de setores com valor acima de zero.'
    else:
        linhas = [[r, intbr(t4.loc[r, 'n']), fmt(ind, t4.loc[r, 'mediana'])] for r in regs]
        linhas += [['Setores de FCU', intbr(t15['n_fcu']), fmt(ind, t15['mediana_fcu'])],
                   ['Demais setores', intbr(t15['n_nao_fcu']), fmt(ind, t15['mediana_nao_fcu'])]]
        cab, colW = ['Recorte', 'Setores', 'Mediana'], [2.0, 1.1, 1.2]
        hi, lo = t4['mediana'].idxmax(), t4['mediana'].idxmin()
        frases = [f"A maior mediana regional é a do {hi} ({fmt(ind, t4.loc[hi, 'mediana'])}); a menor, a do {lo} "
                  f"({fmt(ind, t4.loc[lo, 'mediana'])}).",
                  f"Nos setores de FCU a mediana é {fmt(ind, t15['mediana_fcu'])}; nos demais, "
                  f"{fmt(ind, t15['mediana_nao_fcu'])}.",
                  f"Entre os municípios, a mediana vai de {fmt(ind, lo_m['mediana'])} ({lo_m['NM_MUN']}) a "
                  f"{fmt(ind, hi_m['mediana'])} ({hi_m['NM_MUN']})."]
        leg = 'Caixas sem os pontos extremos; traço vermelho = mediana.'
    return dict(titulo=f'{rot}: por região, município e FCU', parte='DS', requisito='R4, C-04',
                indicador_extra=ind, sub=rot + (' — % de setores com valor acima de zero e média' if zeros
                                                 else ' em cada recorte, sozinho'),
                dimensao=ev.dimensoes().get(ind, ''), cab=cab, linhas=linhas, colW=colW,
                figura=f'figuras/{sid}.png', legenda=leg, frases=frases,
                notas=f'Gerado por ds_extra() em scripts/dados_relatorio_descritivo.py (C-04); '
                      f'{"metade ou mais em zero: % > 0 e média" if zeros else "mediana"}. Números de T04, T05, T15 '
                      f'e, para FCU com zeros, da base da 00_referencia.',
                fontes=[F_T + 'T04_descritivas_regiao.csv', F_T + 'T05_descritivas_municipio.csv',
                        F_T + 'T15_fcu_por_indicador.csv'])


RENDAS_TRIO = {'renda_media', 'renda_media_sem_extremo', 'renda_media_mediana_mun'}


def _par_extremo(R: pd.DataFrame) -> tuple:
    """Par de maior e de menor correlação, fora da diagonal e fora dos pares entre as três
    versões da renda (que medem a mesma coisa e dão 1,000)."""
    M = R.to_numpy().copy()
    np.fill_diagonal(M, np.nan)
    for i, a in enumerate(R.index):
        for j, b in enumerate(R.columns):
            if a in RENDAS_TRIO and b in RENDAS_TRIO:
                M[i, j] = np.nan
    i, j = np.unravel_index(np.nanargmax(M), M.shape)
    k, l_ = np.unravel_index(np.nanargmin(M), M.shape)
    return (R.index[i], R.columns[j], M[i, j]), (R.index[k], R.columns[l_], M[k, l_])


def mapa_corr(R: pd.DataFrame, arq: Path, anotar: bool) -> None:
    rot = [T03.loc[c, 'rotulo'] for c in R.index]
    n = len(R)
    fig, ax = plt.subplots(figsize=(min(10.5, 1.6 + 0.62 * n), min(6.4, 1.0 + 0.5 * n)), dpi=150)
    ax.imshow(R.to_numpy(), cmap=ev.DIVERGENTE, vmin=-1, vmax=1)
    ax.set_xticks(range(n))
    ax.set_xticklabels(rot, rotation=60, ha='right', fontsize=6 if n > 12 else 7.5)
    ax.set_yticks(range(n))
    ax.set_yticklabels(rot, fontsize=6 if n > 12 else 7.5)
    if anotar:
        for i in range(n):
            for j in range(n):
                v = R.iloc[i, j]
                ax.text(j, i, br(v, 2), ha='center', va='center', fontsize=6.5,
                        color='white' if abs(v) > 0.6 else TINTA)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.savefig(arq, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def dc(sid: str, titulo: str, cols: list[str], anotar=True, tabela=False) -> dict:
    T12 = pd.read_csv(TAB / 'T12_correlacao_spearman.csv', index_col=0)
    R = T12.loc[cols, cols]
    mapa_corr(R, FIG / f'{sid}.png', anotar)
    (a, b, v), (c, d_, w) = _par_extremo(R)
    rot = lambda x: T03.loc[x, 'rotulo']
    frases = [f'Maior correlação: {rot(a)} e {rot(b)} ({br(v, 3)}).',
              f'Menor: {rot(c)} e {rot(d_)} ({br(w, 3)}).' if w < 0 else
              f'A mais baixa: {rot(c)} e {rot(d_)} ({br(w, 3)}).']
    x = dict(titulo=titulo, parte='DS', requisito='C-04', sub=f'Spearman, nos 104.108 setores (pares com valor) · {len(cols)} indicadores',
             figura=f'figuras/{sid}.png', legenda='Correlação de Spearman; vermelho = positiva, verde = negativa.',
             frases=frases, fontes=[F_T + 'T12_correlacao_spearman.csv'])
    curto = [rot(c_).split(' (')[0][:13] for c_ in cols]
    corpo = [[rot(r)] + ['1' if r == c_ else br(R.loc[r, c_], 2 if not tabela else 3) for c_ in cols] for r in cols]
    if tabela:
        x.update(cab=[''] + curto, linhas=corpo, colW=[2.3] + [1.333] * len(cols))
        x.pop('figura')
    elif len(cols) <= 7:     # C-05: a tabela ao lado do mapa, quando cabe; colunas numeradas como as linhas
        corpo = [[f'{k} {ln[0]}'] + ln[1:] for k, ln in enumerate(corpo, 1)]
        x.update(cab=[''] + [str(k) for k in range(1, len(cols) + 1)], linhas=corpo,
                 colW=[1.85] + [0.6] * len(cols))
    return x


def dc_slides() -> dict:
    dims = ev.dimensoes()
    por = lambda d: [c for c in ordem_ds() if dims.get(c) == d]
    return {'DC00': dict(titulo='Correlações entre os indicadores', parte='DS', requisito='C-04', numero='2b',
                         sub='Depois da descritiva de cada indicador, as correlações: os componentes do IVS, cada tema e os 31 juntos',
                         fontes=[F_T + 'T12_correlacao_spearman.csv']),
            'DC01': dc('DC01', 'Os componentes do IVS-7', IVS7_COLS, tabela=True),
            'DC02': dc('DC02', 'Os componentes do IVS-7: mapa', IVS7_COLS),
            'DC03': dc('DC03', 'Saneamento', por('Saneamento')),
            'DC04': dc('DC04', 'Socioeconômica', por('Socioeconômica')),
            'DC05': dc('DC05', 'Morfologia', por('Morfologia')),
            'DC06': dc('DC06', 'Demografia', por('Demografia')),
            'DC07': dc('DC07', 'Os 31 indicadores', ordem_ds(), anotar=False)}


def fc_slides(base) -> dict:
    """Os cenários da fatorial ampliada: variáveis, setores que ficam e saem, setores por região."""
    import fatorial_ampliada as fa_
    df = fa_.carregar()
    reg = base.df.set_index('CD_SETOR')['regiao']
    c = cenarios()
    out = {}
    for k, (cen, cols, desc, dem) in enumerate(fa_.CENARIOS, 1):
        d, _ = fa_.montar(df, cols, 'original')
        assert len(d) == int(c.loc[cen, 'n']), f'{cen}: n não bate com cenarios.csv'
        falt = [[fa_.ROT.get(v, v), intbr(df[v if v != 'renda_inv' else 'renda_media'].isna().sum())] for v in cols]
        r = reg.reindex(d['CD_SETOR']).value_counts().reindex(REGIOES_ORD).fillna(0)
        rl = [[x, intbr(r[x])] for x in REGIOES_ORD]
        # C-05: dos setores do S0, quantos saem por causa de cada variável nova (e só dela)
        s0_cols = fa_.CENARIOS[0][1]
        novas = [v for v in cols if v not in s0_cols]
        d0, _ = fa_.montar(df, s0_cols, 'original')
        falta = df.loc[d0.index, novas].isna() if novas else pd.DataFrame(index=d0.index)
        saem = int(falta.any(axis=1).sum()) if novas else 0
        assert saem == int(c.loc[cen, 'perdidos_vs_S0']), f'{cen}: saídas por variável não somam perdidos_vs_S0'
        pv = [[fa_.ROT.get(v, v), intbr(falta[v].sum()), intbr((falta[v] & (falta.sum(axis=1) == 1)).sum())]
              for v in novas]
        pv.append(['Total que sai (alguma delas)', intbr(saem), ''])
        out[f'FC{k:02d}'] = dict(
            titulo=f'Cenário {cen}: {desc}', parte='FP', requisito='C-04',
            sub=f"{len(cols)} variáveis · {intbr(len(d))} setores · demanda {dem}",
            tabelas=[dict(cab=['Variável', 'Faltantes nos 104.108'], linhas=falt, colW=[3.0, 1.7])]
                    + ([dict(cab=['Sai do S0 por causa de', 'Setores sem o dado', 'Só por ela'], linhas=pv,
                             colW=[2.9, 1.5, 1.1])] if novas else [])
                    + [dict(cab=['Região', 'Setores no cenário'], linhas=rl, colW=[2.0, 1.6])],
            frases=[f"Entram os setores urbanos com dados divulgados e com todas as {len(cols)} variáveis: "
                    f"{intbr(len(d))} dos {intbr(len(df))}.",
                    (f"Em relação ao S0, saem {intbr(saem)}: os que não têm alguma das variáveis novas. "
                     f"Um setor pode faltar em mais de uma; a coluna \"só por ela\" conta os que saem por uma única."
                     if novas else "Nenhum setor do S0 sai: as variáveis deste cenário estão todas no S0.")],
            fontes=['banco_de_dados/eda/fatorial_ampliada/cenarios.csv', 'scripts/fatorial_ampliada.py (CENARIOS, carregar, montar)'])
    var = [[v, c.loc[v, 'descricao'], intbr(c.loc[v, 'n'])] for v in c.index if '_' in v]
    out['FC09'] = dict(titulo='As variantes dos cenários', parte='FP', requisito='C-04',
                       sub='Mesmos setores do cenário de origem; muda a renda ou a escala (postos dentro do município)',
                       cab=['Variante', 'Descrição', 'Setores'], linhas=var, colW=[2.6, 7.5, 1.53],
                       frases=['As variantes de renda trocam só o setor extremo de Belo Horizonte; a de postos usa os mesmos setores.'],
                       fontes=['banco_de_dados/eda/fatorial_ampliada/cenarios.csv'])
    return out




# C-02 (v3): sem linha Fonte no rodapé de nenhum slide (as fontes vão às notas); estes mudaram também no texto.
ALTERADOS = {k: 'v3 (C-02)' for k in ('A02', 'A03', 'DM05', 'DS34', 'FA02')}


def criada(sid: str) -> str:
    """Versão do deck em que o slide entrou: v0 (piloto), v1 (lote 1), v2 (lotes 2 a 5)."""
    if sid in ('A01', 'A02', 'DM02', 'DS01', 'DS20', 'DS31', 'FA05', 'FP08'):
        return 'v0'
    if sid in NOVOS_C04:
        return 'v4'
    return 'v1' if sid == 'A03' or sid.startswith('DM') else 'v2'


def main() -> None:
    DADOS.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    base = ev.montar_base(ev.ler_config(REF))
    inv = {v: k for k, v in ID_DS.items()}
    g = globals()
    construtores = {sid: g[sid.lower()] for sid in SLIDES if sid.lower() in g and sid not in ('DM14', 'Z01', 'FA02')}
    d_fa, cols_fa = _base_fatorial(base)
    extra = {**dc_slides(), **fc_slides(base)}
    numeros, manifesto = {'versao': VERSAO, 'slides': {}}, []
    for sid in SLIDES:
        fn = construtores.get(sid)
        if sid in ('DM14', 'Z01'):
            fn = dm14 if sid == 'DM14' else z01
            d = fn(numeros['slides'])
        elif sid == 'FA02':
            fn = fa02
            d = fa02(d_fa, cols_fa)
        elif sid.endswith('-2'):
            fn = ds_extra
            d = ds_extra(inv[sid[:-2]], base)
        elif sid in extra:
            fn = dc if sid.startswith('DC') else fc_slides
            d = extra[sid]
        else:
            d = fn() if fn else ds(inv[sid], base)
        d['id'] = sid
        numeros['slides'][sid] = d
        manifesto.append(dict(id=sid, parte=d['parte'], titulo=d['titulo'], requisito=d['requisito'],
                              fontes=' | '.join(d['fontes']), figura=d.get('figura', ''),
                              funcao_geradora=(fn.__name__ if fn else 'ds') + '()',
                              versao_criada=criada(sid), versao_alterada=ALTERADOS.get(sid, '')))
    numeros['ordem'] = SLIDES
    anexo(numeros['slides'], manifesto)
    (DADOS / 'insercoes_c04.json').write_text(json.dumps({'ordem': SLIDES, 'novos': NOVOS_C04}, indent=1),
                                              encoding='utf-8')
    (DADOS / 'numeros.json').write_text(json.dumps(numeros, ensure_ascii=False, indent=1,
                                                   default=lambda o: o.item() if hasattr(o, 'item') else str(o)),
                                        encoding='utf-8')
    pd.DataFrame(manifesto).to_csv(DADOS / 'manifesto.csv', index=False, encoding='utf-8-sig')
    print(f'{len(SLIDES)} slides: ' + ', '.join(SLIDES))


if __name__ == '__main__':
    main()
