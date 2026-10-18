"""Dados dos dois decks das 108 versões da análise fatorial (`versoes_fatorial/`).

Lê só os resultados de `scripts/versoes_fatorial.py` (banco_de_dados/eda/versoes_fatorial/) e
grava, para o gerador: `dados/numeros.json` (todo número e texto dos slides, por ID, nos dois
decks), `dados/manifesto.csv`, `figuras/VP05–VP07.png` (as grades) e a planilha
`Versoes_Fatorial_numeros.xlsx`. As fontes vão só às notas do apresentador.

Uso:  ./.venv/bin/python scripts/dados_versoes_fatorial.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
sys.path.insert(0, str(RAIZ / 'src'))
import ivs_especificacoes as ie  # noqa: E402
import versoes_fatorial as vf  # noqa: E402
from eda_versoes import ARGILA, CINZA, PETROLEO, TINTA, br, intbr, plt  # noqa: E402

RES = RAIZ / 'banco_de_dados' / 'eda' / 'versoes_fatorial'
PASTA = RAIZ / 'versoes_fatorial'
DADOS, FIG = PASTA / 'dados', PASTA / 'figuras'
VERSAO = 'v1'
F_RES = 'banco_de_dados/eda/versoes_fatorial/'

V = pd.read_csv(RES / 'versoes.csv', keep_default_na=False, na_values=[''])
C = pd.read_csv(RES / 'cargas.csv')
P = pd.read_csv(RES / 'pares_por_eixo.csv')
EST = pd.read_csv(RES / 'estabilidade.csv') if (RES / 'estabilidade.csv').exists() else None
V['elegivel'] = V['elegivel'].astype(str).str.lower().eq('true')
NOME_EIXO = {'renda': 'Renda', 'lixo': 'Lixo', 'agua': 'Água canalizada', 'banheiro': 'Banheiro', 'moradia': 'Moradia'}
ROT = {e: dict(n) for e, n in vf.EIXOS.items()}
FRASE_EIXO = {
    'renda': lambda v: f"renda {ROT['renda'][v]}",
    'lixo': lambda v: f'{v} lixo',
    'agua': lambda v: {'nenhuma': 'água: só a inadequada', 'nao_chega': '+ água não chega',
                       'sem_canalizacao': '+ sem água canalizada'}[v],
    'banheiro': lambda v: {'fora': 'banheiro fora', 'v00495': '+ sem banheiro', 'graduado': '+ banheiro graduado'}[v],
    'moradia': lambda v: {'nao': 'moradia fora', 'sim': '+ moradia não convencional'}[v],
}


# Nomes das opções para tabela (sem o "—" da lista, que só serve à grade de VERSOES.md).
OPCAO = {'renda': ROT['renda'], 'lixo': {'com': 'com lixo', 'sem': 'sem lixo'},
         'agua': {'nenhuma': 'só a inadequada', 'nao_chega': '+ não chega', 'sem_canalizacao': '+ sem canalização'},
         'banheiro': {'fora': 'fora', 'v00495': '+ sem banheiro (V00495)', 'graduado': '+ banheiro graduado'},
         'moradia': {'nao': 'fora', 'sim': '+ não convencional'}}


def descricao(r) -> str:
    return ' · '.join(FRASE_EIXO[e](r[e]) for e in vf.EIXOS)


def notas(fontes: list[str], extra: str = '') -> str:
    return (extra + '\n' if extra else '') + 'Fontes: ' + '; '.join(fontes)


# ── Caderno de fichas ────────────────────────────────────────────────────────────
def ficha(r) -> dict:
    c = C[C['id'] == r['id']].sort_values('ordem')
    est = EST.set_index('id').loc[r['id']] if EST is not None and r['id'] in set(EST['id']) else None
    selo = 'PASSA NOS CRITÉRIOS DO NB05' if r['elegivel'] else f"NÃO PASSA: {r['criterio_que_falhou']}"
    if r['id'] == vf.REFERENCIA:
        selo += ' · REFERÊNCIA PROPOSTA'
    versao = [['Renda', ROT['renda'][r['renda']]], ['Lixo', r['lixo']],
              ['Água canalizada', ROT['agua'][r['agua']]], ['Banheiro', ROT['banheiro'][r['banheiro']]],
              ['Moradia', ROT['moradia'][r['moradia']]], ['Variáveis', intbr(r['p'])],
              ['Setores (amostra própria)', intbr(r['n'])], ['Setores (amostra comum)', intbr(r['n_comum'])]]
    adeq = [['KMO', br(r['kmo'], 4)], ['Bartlett: qui-quadrado', br(r['bartlett_qui2'], 0)],
            ['Bartlett: graus de liberdade', intbr(r['bartlett_gl'])],
            ['MSA mínimo', f"{br(r['msa_min'], 3)} ({r['msa_min_variavel']})"],
            ['Fatores pelo critério de Kaiser', intbr(r['fatores_kaiser'])],
            ['Fatores pela análise de Horn', intbr(r['fatores_horn'])], ['Fatores retidos', '2'],
            ['Variância dos 2 fatores', br(r['var_explicada_2f'], 2) + '%'], ['Φ entre F1 e F2', br(r['phi'], 3)],
            ['Maior variação de peso (um município de fora)',
             br(est['amp_peso_var_max'], 2) + ' p.p.' if est is not None else 'A CONFERIR']]
    cargas = [[x.rotulo, br(x.f1, 3), br(x.f2, 3), br(x.comunalidade, 3), br(x.peso_indice, 2) + '%']
              for x in c.itertuples()]
    valid = [[br(r['auc_global_propria'], 4), br(r['auc_global_comum'], 4),
              f"{br(r['auc_mun_comum'], 4)} ({intbr(r['n_mun_comum'])})",
              br(r['pct_baixo'], 1) + '%', br(r['pct_medio'], 1) + '%', br(r['pct_elevado'], 1) + '%',
              br(r['pct_muito_elevado'], 1) + '%', br(r['spearman_v023_comum'], 4),
              br(r['muda_faixa_v023_comum'], 1) + '%']]
    f1 = c.loc[c['f1'].abs().idxmax(), 'rotulo']
    f2 = c.loc[c['f2'].abs().idxmax(), 'rotulo']
    frases = [f"Kaiser e Horn indicam {intbr(r['fatores_kaiser'])} e {intbr(r['fatores_horn'])} fatores; "
              f"a solução usa 2, que somam {br(r['var_explicada_2f'], 2)}% da variância.",
              f"A maior carga em F1 é de {f1}; em F2, de {f2}."]
    return dict(id=r['id'], parte='VF', titulo=f"Versão {r['id']}", sub=descricao(r), selo=selo,
                passa=bool(r['elegivel']), versao=versao, adequacao=adeq,
                cab_cargas=['Variável', 'F1', 'F2', 'Comunalidade', 'Peso'], cargas=cargas,
                cab_valid=['AUC global (própria)', 'AUC global (comum)', 'AUC no município (comum, nº mun.)',
                           'Faixa baixa', 'Faixa média', 'Faixa elevada', 'Faixa muito elevada',
                           'Spearman com a V023', 'Muda de faixa vs V023'],
                valid=valid, frases=frases,
                notas=notas([F_RES + 'versoes.csv (linha ' + r['id'] + ')', F_RES + 'cargas.csv',
                             F_RES + 'estabilidade.csv'], 'Gerada por ficha() em scripts/dados_versoes_fatorial.py.'),
                fontes=[F_RES + 'versoes.csv', F_RES + 'cargas.csv'])


def caderno() -> dict:
    s = {'VF00': dict(id='VF00', parte='VF', titulo='As 108 versões da análise fatorial',
                      kicker='IVS · CENSO 2022 · CADERNO DE FICHAS',
                      sub='Uma versão por página: renda × lixo × água canalizada × banheiro × moradia, todas com '
                          'promax, pesos 60/40 e normalização municipal',
                      rodape=f'Pedro Dias Soares · outubro de 2026 · caderno {VERSAO}', notas=notas([F_RES])),
         'VF01': dict(id='VF01', parte='VF', titulo='Como ler uma ficha', sub='O mesmo desenho nas 108 páginas',
                      blocos=[['Código.', 'V001 a V108, no canto superior direito; o mesmo da planilha e do deck principal.'],
                              ['Selo.', 'No alto, à esquerda: se a versão passa nos quatro critérios do NB05 (KMO ≥ 0,70; '
                               'MSA ≥ 0,50; comunalidade ≥ 0,30; carga ≥ 0,40) ou qual deles falha.'],
                              ['A versão.', 'Os cinco eixos e quantos setores entram. Amostra própria: os setores com '
                               'todas as variáveis da versão. Amostra comum: os que têm as variáveis de todas as 108.'],
                              ['Adequação.', 'KMO, Bartlett, o menor MSA, quantos fatores cada critério indica (a '
                               'solução usa sempre 2), a variância, a correlação Φ e quanto o maior peso varia '
                               'tirando um município por vez.'],
                              ['Cargas e pesos.', 'Matriz padrão da promax: F1 é o fator onde a renda carrega mais.'],
                              ['Validação e faixas.', 'AUC contra os setores de favela (FCU), a distribuição pelas '
                               'faixas do IVS-BH e a comparação com a V023, a referência proposta.']],
                      notas=notas(['versoes_fatorial/INTERPRETACAO.md']))}
    for _, r in V.iterrows():
        s[r['id']] = ficha(r)
    return {'ordem': list(s), 'slides': s}


# ── Deck principal ───────────────────────────────────────────────────────────────
def grade(col: str, arq: Path, titulo: str, fmt, cores) -> None:
    """6 linhas (renda × lixo) × 18 colunas (água × banheiro × moradia); célula = ID + valor."""
    lin = [(r, l) for r in vf.EIXOS['renda'] for l in vf.EIXOS['lixo']]
    colz = [(a, b, m) for a in vf.EIXOS['agua'] for b in vf.EIXOS['banheiro'] for m in vf.EIXOS['moradia']]
    idx = V.set_index(['renda', 'lixo', 'agua', 'banheiro', 'moradia'])
    fig, ax = plt.subplots(figsize=(13.5, 4.6), dpi=150)
    for i, (r, l) in enumerate(lin):
        for j, (a, b, m) in enumerate(colz):
            x = idx.loc[(r, l, a, b, m)]
            ax.add_patch(plt.Rectangle((j, i), 0.96, 0.92, color=cores(x)))
            claro = cores(x) in (PETROLEO, TINTA, ARGILA)
            ax.text(j + 0.48, i + 0.32, x['id'], ha='center', va='center', fontsize=6.5,
                    color='white' if claro else TINTA, fontweight='bold')
            ax.text(j + 0.48, i + 0.66, fmt(x), ha='center', va='center', fontsize=6,
                    color='white' if claro else TINTA)
    ax.set_xlim(0, 18)
    ax.set_ylim(6, -2.2)
    ax.axis('off')
    for i, (r, l) in enumerate(lin):
        ax.text(-0.1, i + 0.46, f"renda {ROT['renda'][r]} · {l} lixo", ha='right', va='center', fontsize=7.5, color=TINTA)
    for k, a in enumerate(vf.EIXOS['agua']):
        ax.text(6 * k + 3, -1.75, {'nenhuma': 'água: só a inadequada', 'nao_chega': '+ água não chega',
                                    'sem_canalizacao': '+ sem água canalizada'}[a], ha='center', fontsize=8,
                color=TINTA, fontweight='bold')
        ax.plot([6 * k + 0.1, 6 * k + 5.86], [-1.45, -1.45], color=CINZA, lw=0.6)
        for q, b in enumerate(vf.EIXOS['banheiro']):
            ax.text(6 * k + 2 * q + 1, -0.95, {'fora': 'banheiro fora', 'v00495': '+ sem banheiro',
                                                 'graduado': '+ graduado'}[b], ha='center', fontsize=7, color=TINTA)
            for t, m in enumerate(vf.EIXOS['moradia']):
                ax.text(6 * k + 2 * q + t + 0.48, -0.35, 'sem mor.' if m == 'nao' else '+ mor.', ha='center',
                        fontsize=6, color=CINZA)
    ax.set_title(titulo, fontsize=9, color=TINTA, loc='left')
    fig.savefig(arq, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def seq(v, lo, hi):
    """Escala de uma cor só (petróleo), do claro ao escuro."""
    t = 0 if hi == lo else (v - lo) / (hi - lo)
    rgb = np.array([0.93, 0.95, 0.94]) * (1 - t) + np.array([0x1F, 0x4E, 0x4A]) / 255 * t
    return tuple(rgb)


def principal() -> dict:
    s = {}
    ne = int(V['elegivel'].sum())
    s['VP01'] = dict(titulo='As 108 versões da análise fatorial', kicker='IVS · CENSO 2022 · 70 MUNICÍPIOS DO ELSI-BRASIL',
                     sub='Renda × lixo × água canalizada × banheiro × moradia, com o método da referência proposta: '
                         'promax, pesos 60/40, normalização municipal',
                     rodape=f'Pedro Dias Soares · outubro de 2026 · deck {VERSAO}', fontes=[F_RES + 'versoes.csv'])
    s['VP02'] = dict(titulo='Como ler', sub='Um código por versão; duas amostras; a escolha fica com a orientadora',
                     blocos=[['Código.', 'V001 a V108, o mesmo no caderno de fichas e na planilha. A V023 é a referência '
                              'proposta no NB05 — proposta, não escolhida.'],
                             ['Método fixo.', 'Todas as versões usam promax, pesos 60/40 e normalização municipal, com 2 '
                              'fatores. Muda só o que entra na fatorial.'],
                             ['Amostra própria.', 'Cada fatorial roda nos setores que têm todas as variáveis da versão.'],
                             ['Amostra comum.', f"As comparações entre versões usam os {intbr(V['n_comum'].max())} setores "
                              'que têm as variáveis de todas as 108.'],
                             ['Critérios.', 'Os do NB05, fixados antes: KMO ≥ 0,70; MSA ≥ 0,50; comunalidade ≥ 0,30; carga ≥ 0,40.']],
                     fontes=['versoes_fatorial/INTERPRETACAO.md'])
    eixos = [[NOME_EIXO[e], ' · '.join(OPCAO[e].values()), str(len(OPCAO[e]))] for e in vf.EIXOS]
    s['VP03'] = dict(titulo='Os cinco eixos', sub='3 × 2 × 3 × 3 × 2 = 108 versões, de 6 a 10 variáveis',
                     cab=['Eixo', 'Opções', 'Nº'], linhas=eixos, colW=[2.4, 8.2, 1.03],
                     frases=['Fixas em todas: água inadequada, esgoto, razão de moradores, analfabetismo, renda e cor/raça. '
                             '"Não chega" e "sem canalização" não entram juntas: uma contém a outra.'],
                     fontes=['versoes_fatorial/VERSOES.md'])
    am = []
    for e in vf.EIXOS:
        for k, rot in OPCAO[e].items():
            g = V[V[e] == k]
            am.append([NOME_EIXO[e], rot, intbr(g['n'].median()), intbr(g['n'].min()), intbr(g['n'].max())])
    s['VP04'] = dict(titulo='A amostra', sub='Setores na amostra própria, por opção de cada eixo',
                     cab=['Eixo', 'Opção', 'Mediana', 'Menor', 'Maior'], linhas=am, colW=[2.4, 4.0, 1.7, 1.7, 1.83],
                     frases=[f"Cada versão tem de {intbr(V['n'].min())} a {intbr(V['n'].max())} setores; a amostra comum "
                             f"às 108 tem {intbr(V['n_comum'].max())}."],
                     fontes=[F_RES + 'versoes.csv (n, n_comum)'])
    grade('elegivel', FIG / 'VP05.png', 'Passa nos critérios do NB05 (petróleo) ou não (cinza)',
          lambda x: 'passa' if x['elegivel'] else {'comunalidade': 'comun.'}.get(x['criterio_que_falhou'].split(' ')[0], x['criterio_que_falhou'].split(' ')[0]),
          lambda x: PETROLEO if x['elegivel'] else '#DADADA')
    lo, hi = V['kmo'].min(), V['kmo'].max()
    grade('kmo', FIG / 'VP06.png', 'KMO de cada versão', lambda x: br(x['kmo'], 3), lambda x: seq(x['kmo'], lo, hi))
    lo2, hi2 = V['auc_mun_comum'].min(), V['auc_mun_comum'].max()
    grade('auc', FIG / 'VP07.png', 'AUC contra FCU dentro dos municípios (amostra comum)',
          lambda x: br(x['auc_mun_comum'], 3), lambda x: seq(x['auc_mun_comum'], lo2, hi2))
    por_lixo = V.groupby('lixo')['elegivel'].sum()
    s['VP05'] = dict(titulo='As 108 de uma vez: quem passa nos critérios', sub=f'{ne} das 108 passam',
                     figura='figuras/VP05.png', legenda='Cada célula é uma versão; abaixo do código, "passa" ou o primeiro critério que falha (comun. = comunalidade < 0,30).',
                     frases=[f"Com lixo passam {intbr(por_lixo.get('com', 0))}; sem lixo, {intbr(por_lixo.get('sem', 0))}."],
                     fontes=[F_RES + 'versoes.csv (elegivel, criterio_que_falhou)'])
    s['VP06'] = dict(titulo='As 108 de uma vez: KMO', sub=f"De {br(lo, 3)} a {br(hi, 3)}",
                     figura='figuras/VP06.png', legenda='Quanto mais escura a célula, maior o KMO.',
                     frases=[f"O maior KMO é o da {V.loc[V['kmo'].idxmax(), 'id']} ({br(hi, 4)}); o menor, o da "
                             f"{V.loc[V['kmo'].idxmin(), 'id']} ({br(lo, 4)})."],
                     fontes=[F_RES + 'versoes.csv (kmo)'])
    s['VP07'] = dict(titulo='As 108 de uma vez: AUC no município', sub=f"De {br(lo2, 3)} a {br(hi2, 3)}, na amostra comum",
                     figura='figuras/VP07.png', legenda='Mediana da AUC contra FCU entre os municípios com ao menos 30 setores de FCU e 30 fora.',
                     frases=[f"A maior é a da {V.loc[V['auc_mun_comum'].idxmax(), 'id']} ({br(hi2, 4)}); a menor, a da "
                             f"{V.loc[V['auc_mun_comum'].idxmin(), 'id']} ({br(lo2, 4)})."],
                     fontes=[F_RES + 'versoes.csv (auc_mun_comum)'])

    def faixa(r, col, d, pct=False):
        f = (lambda v: br(0 if abs(v) < 0.5 * 10 ** -d else v, d) + ('%' if pct else ''))   # sem "-0,000"
        return f"{f(r[col + '_mediana'])} [{f(r[col + '_min'])}; {f(r[col + '_max'])}]"
    for k, e in enumerate(vf.EIXOS, 8):
        g = P[P['eixo'] == e]
        linhas = [[f"{FRASE_EIXO[e](x.de)} → {FRASE_EIXO[e](x.para)}", intbr(x.pares), faixa(x._asdict(), 'd_kmo', 3),
                   faixa(x._asdict(), 'd_kaiser', 0), faixa(x._asdict(), 'd_auc_mun_comum', 3),
                   faixa(x._asdict(), 'spearman', 3), faixa(x._asdict(), 'pct_muda_faixa', 1, True),
                   f"{intbr(x.elegiveis_de)} → {intbr(x.elegiveis_para)}"] for x in g.itertuples(index=False)]
        maior = g.loc[g['pct_muda_faixa_mediana'].idxmax()]
        s[f'VP{k:02d}'] = dict(
            titulo=f'Um eixo por vez: {NOME_EIXO[e].lower()}',
            sub='Pares de versões iguais em tudo, menos neste eixo: mediana [menor; maior] da diferença',
            cab=['Troca', 'Pares', 'Δ KMO', 'Δ fatores (Kaiser)', 'Δ AUC no município', 'Spearman entre os índices',
                 'Setores que mudam de faixa', 'Elegíveis antes → depois'],
            linhas=linhas, colW=[2.6, 0.7, 1.45, 1.25, 1.5, 1.5, 1.5, 1.13],
            frases=[f"Na troca {FRASE_EIXO[e](maior['de'])} → {FRASE_EIXO[e](maior['para'])}, metade dos pares tem até "
                    f"{br(maior['pct_muda_faixa_mediana'], 1)}% dos setores mudando de faixa, e o Spearman mediano é "
                    f"{br(maior['spearman_mediana'], 3)}."],
            fontes=[F_RES + 'pares_por_eixo.csv', F_RES + 'pares_detalhe.csv'])
    el = V[V['elegivel']].copy()
    el = el.assign(desc=[descricao(r) for _, r in el.iterrows()])
    lin = [[r['id'], r['desc'], intbr(r['n']), br(r['kmo'], 3), br(r['auc_mun_comum'], 3),
            br(r['spearman_v023_comum'], 3)] for _, r in el.iterrows()]
    blocos = [lin[i:i + 16] for i in range(0, len(lin), 16)] or [[]]
    for q, b in enumerate(blocos):
        sid = 'VP13' if q == 0 else f'VP13-{q + 1}'
        s[sid] = dict(titulo='As versões que passam nos critérios' + ('' if q == 0 else f' ({q + 1})'),
                      sub=f'{ne} versões; lista em ordem de código, sem ordenar por resultado',
                      cab=['Código', 'Versão', 'Setores', 'KMO', 'AUC no município', 'Spearman com a V023'],
                      linhas=b, colW=[0.8, 6.6, 1.0, 0.8, 1.2, 1.23], fontes=[F_RES + 'versoes.csv (elegivel)'])
    if EST is not None and 'amp_peso_var_max' in V:
        o = V.assign(normalizacao='municipal', rotacao='promax', metodo='60_40')
        o = ie.ordenar(o, 'municipal', 'amp_peso_var_max', 'auc_mun_comum').head(12)
        lin = [[r['id'], descricao(r), br(r['amp_peso_var_max'], 2), br(r['auc_mun_comum'], 3), intbr(r['p']),
                br(r['posto_medio'], 1)] for _, r in o.iterrows()]
        s['VP14'] = dict(titulo='A ordem das elegíveis pelos critérios do NB05',
                         sub='Posição média em estabilidade, AUC no município e parcimônia — uma ordem, não uma escolha',
                         cab=['Código', 'Versão', 'Maior variação de peso (p.p.)', 'AUC no município', 'Variáveis', 'Posição média'],
                         linhas=lin, colW=[0.8, 6.0, 1.5, 1.2, 0.9, 1.23],
                         frases=['Estabilidade lida pela maior variação do peso de uma variável (o peso de F1 é fixo em 60/40). '
                                 'Empates: a versão mais próxima do IVS-BH 2012.'],
                         fontes=[F_RES + 'versoes.csv', F_RES + 'estabilidade.csv', 'scripts/ivs_especificacoes.py:ordenar'])
    else:
        s['VP14'] = dict(titulo='A ordem das elegíveis', sub='A CONFERIR — estabilidade não calculada',
                         blocos=[['A CONFERIR.', 'Sem a estabilidade, a ordem do NB05 não se calcula.']], fontes=['—'])
    s['VP15'] = dict(titulo='O que está em aberto', sub='Escolhas que o deck não faz',
                     blocos=[['Método.', 'Todas as versões usam o método da referência proposta. Variar rotação, pesos e '
                              'normalização multiplicaria as 108 por até 18.'],
                             ['Número de fatores.', 'A solução usa 2 em todas, mesmo onde Kaiser ou Horn indicam outro número.'],
                             ['Água canalizada.', 'Entrou somada à água inadequada, não no lugar dela.'],
                             ['Moradia.', 'Entrou como não convencional, na direção da vulnerabilidade.'],
                             ['A versão do artigo.', 'É decisão da orientadora; a planilha anexa tem a coluna "Vai para o artigo?".']],
                     fontes=['versoes_fatorial/INTERPRETACAO.md'])
    for k, x in s.items():
        x.update(id=k, parte='VP', notas=notas(x['fontes']))
    return {'ordem': list(s), 'slides': s}


def parte_relatorio(pr: dict) -> dict:
    """O deck principal como parte 5 do relatório descritivo, no estilo das edições do Pedro
    (C-03): sem capa, sem "proposta, não escolhida" e sem o slide "O que está em aberto"."""
    import copy
    s = {'VP00': dict(id='VP00', parte='VP', titulo='As 108 versões da análise fatorial', numero='5',
                      sub='Renda × lixo × água canalizada × banheiro × moradia, todas com promax, pesos 60/40 e '
                          'normalização municipal: quem passa nos critérios e o que muda de um eixo para outro',
                      fontes=[F_RES + 'versoes.csv'])}
    for k in pr['ordem']:
        if k in ('VP01', 'VP15'):
            continue
        x = copy.deepcopy(pr['slides'][k])
        if k == 'VP02':
            x['sub'] = 'Um código por versão e duas amostras'
            x['blocos'][0][1] = 'V001 a V108, o mesmo no caderno de fichas e na planilha. A V023 é a referência proposta no NB05.'
        if k == 'VP14':
            x['sub'] = 'Posição média em estabilidade, AUC no município e parcimônia'
        s[k] = x
    for x in s.values():
        x['notas'] = notas(x['fontes'])
    return {'ordem': list(s), 'slides': s}


def planilha(man: list) -> None:
    x = V.copy()
    for c in ['Vai para o artigo? (Sim/Talvez/Não)', 'Seção do artigo', 'Comentários']:
        x[c] = ''
    with pd.ExcelWriter(PASTA / 'Versoes_Fatorial_numeros.xlsx', engine='openpyxl') as w:
        x.to_excel(w, sheet_name='Versoes', index=False)
        C.to_excel(w, sheet_name='Cargas', index=False)
        P.to_excel(w, sheet_name='Pares_por_eixo', index=False)
        if EST is not None:
            EST.to_excel(w, sheet_name='Estabilidade', index=False)
        pd.DataFrame(man).to_excel(w, sheet_name='Indice_slides', index=False)
        w.book['Versoes'].auto_filter.ref = w.book['Versoes'].dimensions
        for ws in w.book.worksheets:
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width = min(40, max(9, max(len(str(c.value or '')) for c in col[:40]) + 2))


def main() -> None:
    DADOS.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    N = {'versao': VERSAO, 'caderno': caderno(), 'principal': principal()}
    N['parte'] = parte_relatorio(N['principal'])
    man = [{'deck': deck, 'id': k, 'titulo': x['titulo'], 'fontes': ' | '.join(x.get('fontes', [])),
            'figura': x.get('figura', '')} for deck in ('principal', 'caderno')
           for k, x in N[deck]['slides'].items()]
    (DADOS / 'numeros.json').write_text(json.dumps(N, ensure_ascii=False, indent=1,
                                                   default=lambda o: o.item() if hasattr(o, 'item') else str(o)),
                                        encoding='utf-8')
    pd.DataFrame(man).to_csv(DADOS / 'manifesto.csv', index=False, encoding='utf-8-sig')
    planilha(man)
    print(f"principal: {len(N['principal']['ordem'])} slides; caderno: {len(N['caderno']['ordem'])} slides")


if __name__ == '__main__':
    main()
