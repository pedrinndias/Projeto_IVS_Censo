#!/usr/bin/env python
"""Dados do deck para a orientadora: EDA unificada, EDA final, fatorial e os catálogos visuais.

    ./.venv/bin/python scripts/dados_deck_orientadora.py
    node scripts/gerar_deck_orientadora.js

Monta, slide a slide, `analises_exploratorias/00_sintese/unificada/deck_orientadora.json`, que
o gerador só diagrama. Todo número sai de um CSV já gravado (versões, `banco_de_dados/eda/`)
e é formatado aqui; as duas tabelas novas da parte 1 (recortes e variantes testadas) são
gravadas em `00_sintese/unificada/` antes de entrar no deck. As miniaturas das partes 4 e 5
vão para uma pasta temporária (não versionada).

Partes: 1 EDA unificada (todas as versões) · 2 EDA da versão final (referência, demandas) ·
3 análise fatorial (demandas 3 e 5 a 11, NB05, referência, robustez) · 4 catálogo visual da
EDA · 5 catálogo visual da fatorial e do índice.
"""
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eda_versoes as ev  # noqa: E402
from eda_versoes import br, intbr, pctbr  # noqa: E402

RAIZ = ev.RAIZ
A = RAIZ / 'analises_exploratorias'
E = RAIZ / 'banco_de_dados' / 'eda'
SAIDA = A / '00_sintese' / 'unificada'
MINI = Path(tempfile.gettempdir()) / 'deck_orientadora_miniaturas'
MOD = json.loads(ev.MODELOS.read_text(encoding='utf-8'))
BLOCOS_EDA = {1, 2, 3, 4, 5, 6, 7, 8, 19}          # o resto (9–18, 20) é fatorial e índice
SLIDES = []


# ── Leitura ───────────────────────────────────────────────────────────────────
def tab(versao, id_):
    return pd.read_csv(next((A / versao / 'tabelas').glob(f'{id_}_*.csv')))


def cat(versao):
    return pd.read_csv(A / versao / 'catalogo.csv', dtype=str, keep_default_na=False).set_index('id')


def csv_eda(rel):
    return pd.read_csv(E / rel, sep=';', encoding='utf-8-sig')


def sim(x):
    return 'sim' if x in (1, 1.0, True, 'True') else ('não' if x in (0, 0.0, False, 'False') else '—')


# ── Slides ────────────────────────────────────────────────────────────────────
def secao(num, titulo, sub, nota):
    SLIDES.append({'tipo': 'secao', 'num': num, 'titulo': titulo, 'sub': sub, 'nota': nota})


def texto(titulo, itens, nota='', fonte=''):
    SLIDES.append({'tipo': 'texto', 'titulo': titulo, 'itens': itens, 'nota': nota or '\n'.join(itens), 'fonte': fonte})


def numeros(titulo, nums, texto_, nota='', fonte=''):
    SLIDES.append({'tipo': 'numeros', 'titulo': titulo, 'nums': nums, 'texto': texto_, 'nota': nota or texto_, 'fonte': fonte})


def figura(titulo, img, como_ler, mostra, nota, fonte, chave='', larga=False):
    SLIDES.append({'tipo': 'figura_larga' if larga else 'figura', 'titulo': titulo, 'img': str(img), 'como_ler': como_ler,
                   'mostra': mostra, 'nota': nota, 'fonte': fonte, 'chave': chave})


def tabela(titulo, cab, linhas, colW, como_ler, mostra, nota, fonte, larga=False):
    SLIDES.append({'tipo': 'tabela', 'titulo': titulo, 'cab': cab, 'linhas': [[str(c) for c in l] for l in linhas],
                   'colW': colW, 'como_ler': como_ler, 'mostra': mostra, 'nota': nota, 'fonte': fonte, 'larga': larga})


def item(versao, id_, titulo=None, larga=False):
    """Um item já gravado por uma versão: título, 'Como ler', 'O que mostra' e nota dos modelos."""
    r = cat(versao).loc[id_]
    m = MOD['itens'].get(r['chave'], {})
    campos = json.loads(r['campos'])
    preencher = lambda t: str(t or '').format_map(ev._Seguro(campos))
    figura(titulo or r['titulo'], A / versao / r['arquivo'], preencher(m.get('como_ler')), r['o_que_mostra'],
           preencher(m.get('nota')), f"{versao} · {id_} · {r['arquivo']}", chave=r['chave'], larga=larga)


def figura_eda(rel, titulo, como_ler, mostra, nota, chave=''):
    figura(titulo, E / rel, como_ler, mostra, nota, f'banco_de_dados/eda/{rel}', chave=chave)


# ── Parte 1 — EDA unificada ───────────────────────────────────────────────────
def parte1():
    secao('1', 'A EDA unificada', 'Todas as versões das análises exploratórias, comparadas contra a mesma referência',
          'Cada versão é a referência proposta no NB05 com uma coisa mudada: que setores entram (eixo A), que indicadores '
          'entram (B), como o índice é construído (C), índices novos ao lado do IVS (D). O eixo E atravessa as versões. '
          'Esta parte põe tudo lado a lado; nada aqui escolhe versão.')
    t61 = tab('00_sintese', 'T61')
    t60 = tab('00_sintese', 'T60')
    tot = t61[t61['eixo'] == 'Todas'].iloc[0]
    texto('Como as versões foram construídas', [
        'Cada versão é a referência proposta no NB05 com uma coisa mudada, para que a comparação responda a uma pergunta só.',
        'A — que setores entram: com rurais, piso de população, Belo Horizonte, por região, por porte e o Brasil inteiro.',
        'B — que indicadores entram: as três rendas, as definições de água, banheiro, esgoto e moradia, lixo, cor ou raça e os complementares.',
        'C — como o índice é construído: rotação e pesos, extração, normalização, agregação, regras de faixa e pesos iguais.',
        'D — índices novos: subíndices, IVS-Idoso, índice de moradia, IBP aproximado e pesos de especialista × dados.',
        'E — análises que atravessam as versões: incerteza, estabilidade, desigualdade interna, população em risco, envelhecimento e tipologias.',
        f"São {intbr(tot['versoes'])} versões que constroem um índice; {intbr(tot['elegiveis'])} passam nos critérios de elegibilidade do NB05."],
        fonte='00_sintese · T61')
    tabela(f"{intbr(tot['elegiveis'])} de {intbr(tot['versoes'])} versões são elegíveis pelos critérios do NB05",
           ['Eixo', 'Versões', 'Elegíveis', 'AUC mun. mín.', 'AUC mun. máx.', '% muda faixa (máx.)'],
           [[r['eixo'], intbr(r['versoes']), intbr(r['elegiveis']), br(r['auc_municipal_min']), br(r['auc_municipal_max']),
             pctbr(r['pct_mudam_max'])] for _, r in t61.iterrows()], [3.0, 0.9, 0.9, 1.1, 1.1, 1.2],
           'Uma linha por eixo: versões, quantas são elegíveis, a menor e a maior AUC municipal contra as favelas e a maior troca de faixa em relação à referência.',
           f"A AUC municipal vai de {br(tot['auc_municipal_min'])} a {br(tot['auc_municipal_max'])} entre as versões.",
           MOD['itens']['sint_eixos']['nota'], '00_sintese · T61')
    tabela('Todas as versões lado a lado',
           ['Versão', 'Setores no índice', 'KMO', 'AUC mun.', 'Elegível', 'ρ com a referência', '% muda faixa'],
           [[r['versao'], intbr(r['setores_indice']), br(r['kmo']), br(r['auc_municipal']), sim(r['elegivel']),
             br(r['spearman_com_referencia']), pctbr(r['pct_mudam_faixa'])] for _, r in t60.iterrows()],
           [2.8, 1.1, 0.75, 0.85, 0.75, 1.0, 0.95],
           'Uma linha por versão. ρ é a correlação de postos entre o índice da versão e o da referência; % muda faixa é a parcela dos setores comuns que troca de faixa (regra do IVS-BH). Traço: a versão não roda aquele bloco.',
           cat('00_sintese').loc['T60', 'o_que_mostra'], MOD['itens']['sint_tabela']['nota'], '00_sintese · T60')
    item('00_sintese', 'F60')
    item('00_sintese', 'F61')

    # eixo A: os recortes lado a lado (tabela nova, gravada antes de entrar no deck)
    linhas = []
    for v in ['00_referencia', 'A1_com_rurais', 'A2_piso_populacional', 'A3_belo_horizonte', 'A4_por_regiao/norte',
              'A4_por_regiao/nordeste', 'A4_por_regiao/sudeste', 'A4_por_regiao/sul', 'A4_por_regiao/centro_oeste',
              'A5_por_porte/ate_100_mil', 'A5_por_porte/de_100_a_500_mil', 'A5_por_porte/mais_de_500_mil', 'A6_brasil']:
        t01, t03, t02 = tab(v, 'T01'), tab(v, 'T03').set_index('indicador'), tab(v, 'T02').set_index('indicador')
        linhas.append({'versao': v, 'setores_recorte': t01.iloc[-2]['setores'], 'setores_indice': t01.iloc[-1]['setores'],
                       'mediana_renda': t03.loc['renda_media', 'mediana'], 'media_analfab': t03.loc['pct_analfab', 'media'],
                       'media_esgoto_inad': t03.loc['pct_esgoto_inad', 'media'], 'media_agua_inad': t03.loc['pct_agua_inad', 'media'],
                       'pct_sem_analfab': t02.loc['pct_analfab', 'pct_faltantes']})
    u1 = pd.DataFrame(linhas)
    u1.to_csv(SAIDA / 'U01_recortes.csv', index=False)
    a, z = u1.loc[u1['mediana_renda'].idxmax()], u1.loc[u1['mediana_renda'].idxmin()]
    tabela('Os recortes mudam o retrato: a renda mediana vai de ' + br(z['mediana_renda'], 2) + ' a ' + br(a['mediana_renda'], 2),
           ['Versão', 'Recorte', 'Índice', 'Renda mediana (R$)', 'Analfab. (média)', 'Esgoto inad. (média)', 'Água inad. (média)', '% sem analfab.'],
           [[r['versao'], intbr(r['setores_recorte']), intbr(r['setores_indice']), br(r['mediana_renda'], 2), br(r['media_analfab']),
             br(r['media_esgoto_inad']), br(r['media_agua_inad']), pctbr(r['pct_sem_analfab'])] for _, r in u1.iterrows()],
           [2.5, 0.85, 0.8, 1.0, 0.85, 0.85, 0.85, 0.8],
           'Uma linha por recorte do eixo A (e a referência): setores no recorte e no índice, renda mediana, médias de analfabetismo, esgoto e água inadequados e o percentual de setores sem analfabetismo por sigilo.',
           f"Renda mediana mais alta: {a['versao']} ({br(a['mediana_renda'], 2)}); mais baixa: {z['versao']} ({br(z['mediana_renda'], 2)}).",
           'Os números vêm das tabelas T01, T02 e T03 de cada versão, reunidos em analises_exploratorias/00_sintese/unificada/U01_recortes.csv. As médias de proporção são médias entre setores, não razões agregadas.',
           '00_sintese/unificada/U01_recortes.csv')

    # todas as variantes testadas (as tabelas T34 das versões)
    linhas = []
    for f in sorted(A.glob('**/tabelas/T34_sensibilidade.csv')):
        v = str(f.parent.parent.relative_to(A))
        for _, r in pd.read_csv(f).iterrows():
            linhas.append({'versao': v, 'variante': r['rotulo'], 'setores_indice': r['setores_indice'], 'kmo': r['kmo'],
                           'auc_municipal': r['auc_municipal'], 'elegivel': r['elegivel']})
    u2 = pd.DataFrame(linhas)
    u2.to_csv(SAIDA / 'U02_variantes.csv', index=False)
    m = u2.loc[u2['auc_municipal'].idxmax()]
    tabela(f"{intbr(len(u2))} variantes testadas nas tabelas de sensibilidade, com AUC municipal de {br(u2['auc_municipal'].min())} a {br(u2['auc_municipal'].max())}",
           ['Versão', 'Variante', 'Índice', 'KMO', 'AUC mun.', 'Elegível'],
           [[r['versao'], r['variante'], intbr(r['setores_indice']), br(r['kmo']), br(r['auc_municipal']), sim(r['elegivel'])]
            for _, r in u2.iterrows()], [2.0, 3.0, 0.85, 0.75, 0.85, 0.7],
           'Uma linha por variante: a primeira de cada versão é o valor-padrão dela; as demais, as alternativas da tabela T34 (inclusive a referência, quando entra como alternativa).',
           f"A maior AUC municipal entre as variantes é a de “{m['variante']}” ({m['versao']}, {br(m['auc_municipal'])}).",
           'Reunido das tabelas T34 de todas as versões em analises_exploratorias/00_sintese/unificada/U02_variantes.csv.',
           '00_sintese/unificada/U02_variantes.csv')
    for v, i in [('E1_incerteza', 'F40'), ('E1_incerteza', 'F41'), ('E4_populacao_em_risco', 'F45'),
                 ('E3_desigualdade_intramunicipal', 'F44'), ('E5_ivs_e_envelhecimento', 'F46'), ('E5_ivs_e_envelhecimento', 'F47'),
                 ('E6_tipologias', 'F48')]:
        item(v, i)
    t41 = tab('E1_incerteza', 'T41').set_index('situacao')['pct']
    t48 = tab('E4_populacao_em_risco', 'T48')
    r48 = t48[t48['versao'] == '00_referencia'].iloc[0]
    t50 = tab('E5_ivs_e_envelhecimento', 'T50')
    texto('O que a EDA unificada mostra', [
        f"{intbr(tot['elegiveis'])} de {intbr(tot['versoes'])} versões passam nos critérios do NB05; quando falham, o motivo mais comum é o banheiro graduado.",
        f"A maior parte das versões fica perto da referência; a que mais se afasta é {t60.loc[t60['spearman_com_referencia'].idxmin(), 'versao']} (ρ = {br(t60['spearman_com_referencia'].min())}).",
        f"Entre as versões elegíveis, {pctbr(t41['nunca em risco elevado'])} dos setores nunca ficam em risco elevado, {pctbr(t41['sempre em risco elevado'])} ficam sempre e {pctbr(t41['às vezes'])} mudam conforme a versão.",
        f"Na referência, {pctbr(r48['pct_pessoas_alto'])} dos moradores vivem em setores de risco elevado ou muito elevado.",
        f"IVS e envelhecimento andam em sentidos opostos (ρ = {br(t50['rho_pct_idoso_60mais'].iloc[0])} com a proporção de 60+).",
        'Nada disso escolhe versão: a escolha é da orientadora.'], fonte='00_sintese · E1 · E4 · E5')


# ── Parte 2 — EDA da versão final ─────────────────────────────────────────────
def parte2():
    ref = pd.read_csv(E / 'ivs_especificacoes' / 'referencia.csv').query("leitura == 'principal'").iloc[0]
    secao('2', 'A EDA da versão final', 'O recorte da referência, com os 31 indicadores e as correções das demandas',
          'A versão final da EDA é a do recorte de análise (setores urbanos com Dados_sig = OK nos 70 municípios), com todos os '
          'indicadores e variantes pedidos nas demandas de setembro. O índice que a acompanha é a referência proposta no NB05, '
          'que continua proposta até a orientadora decidir.')
    texto('O que esta versão atende', [
        'Demanda 1 — renda com a mediana: coluna renda_media_mediana_mun, ao lado da renda original e da sem o extremo.',
        'Demanda 2 — quadro de indicadores: Quadro_Indicadores, gerado do código, com numerador, denominador e origem.',
        'Demandas 5 e 7 — água: “não chega”, sem canalização e só no terreno, comparadas com o IVS-7 e com as outras categorias.',
        'Demanda 6 — banheiro: V00495 (que já contém V00238) e as três partições V00236, V00237 e V00238, além do banheiro graduado.',
        'Demanda 9 — habitação: moradia não convencional, na direção da vulnerabilidade, com diagnóstico completo.',
        f"Índice que acompanha a EDA: {ref['id']} (referência proposta no NB05, não decidida)."],
        fonte='docs/prompts/estado_demandas_2026-09.md · ivs_especificacoes/referencia.csv')
    t01 = tab('00_referencia', 'T01')
    numeros(f"{intbr(t01.iloc[-1]['setores'])} setores chegam ao índice, de {intbr(t01.iloc[0]['setores'])} na base",
            [[intbr(t01.iloc[0]['setores']), 'setores na base completa'], [intbr(t01.iloc[-2]['setores']), 'setores no recorte (urbanos, Dados_sig = OK)'],
             [intbr(t01.iloc[-1]['setores']), 'setores com todos os componentes do índice']],
            MOD['itens']['funil_tab']['nota'], fonte='00_referencia · T01')
    q = pd.read_csv(ev.QUADRO, sep=';', encoding='utf-8-sig')
    ext = MOD['dicionario_extra']
    linhas = [[ev.ROT[r['indicador']], r['dimensao'], r['entra_no_ivs7'], r['o_que_mede']] for _, r in q.iterrows()]
    linhas += [[ev.ROT[k], ev.EXTRAS[k], 'Não', v['o_que_mede']] for k, v in ext.items()]
    tabela('Os 31 indicadores e variantes da versão final', ['Indicador', 'Dimensão', 'IVS-7', 'O que mede'], linhas,
           [2.1, 1.3, 0.6, 4.2], 'Uma linha por indicador: dimensão, se entra no IVS-7 e o que mede (texto do Quadro de Indicadores).',
           'O quadro completo, com numerador, denominador e arquivo do Censo, está em Quadro_Indicadores.xlsx.',
           'O quadro é gerado do código (scripts/gerar_quadro_indicadores.py), nunca digitado. As três variantes no fim (duas rendas e o banheiro graduado) foram criadas depois do quadro.',
           'entrega_orientadora/Quadro_Indicadores.csv')
    ra = csv_eda('atualizada/renda_imputacao_alternativas.csv')
    tabela('Demanda 1: a renda do setor extremo de BH, imputada por três medianas',
           ['Alternativa', 'Valor imputado (R$)', 'Média BH', 'DP BH', 'Máx. BH', 'Média 70 mun.'],
           [[r['alternativa'], br(r['valor_imputado'], 2), br(r['bh_media'], 2), br(r['bh_dp'], 2), br(r['bh_max'], 2),
             br(r['agregado_media'], 2)] for _, r in ra.iterrows()], [2.7, 1.2, 1.0, 1.0, 1.0, 1.1],
           'Uma linha por alternativa de imputação do setor 310620005650366: o valor posto no lugar e o efeito nas estatísticas de BH e do conjunto.',
           f"A mediana de BH sem o setor ({br(ra['valor_imputado'].iloc[0], 2)}) é a usada na coluna renda_media_mediana_mun; com qualquer alternativa, o máximo de BH cai para {br(ra['bh_max'].iloc[0], 2)}.",
           'A mediana do próprio setor (V06006) não existe no arquivo do Censo; por isso a imputação usa a mediana do município. As alternativas mostram que a escolha mexe pouco nas estatísticas.',
           'banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv')
    figura_eda('atualizada/figuras/extremo_bh.png', 'O setor extremo de Belo Horizonte e o efeito de tirá-lo',
               'A renda dos setores de Belo Horizonte e a escala normalizada, com e sem o setor extremo.',
               f"Sem o setor extremo, a maior renda média de setor em BH passa a ser {br(ra['bh_max'].iloc[0], 2)}.",
               'Figura da 2ª rodada da EDA (eda/atualizada). O setor extremo comprime a escala min-max de toda a cidade; por isso as variantes de renda existem.', chave='extremo_bh')
    t03 = tab('00_referencia', 'T03').set_index('indicador')
    sel = ['pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad', 'razao_moradores', 'pct_analfab', 'renda_media', 'pct_raca_pretpardind',
           'pct_sem_agua_canalizada', 'pct_agua_nao_encanada', 'pct_agua_so_terreno', 'pct_sem_banheiro', 'pct_sem_banheiro_nem_sanitario',
           'pct_so_sanitario', 'pct_banheiro_comum', 'banheiro_graduado', 'pct_moradia_nao_convencional',
           'renda_media_sem_extremo', 'renda_media_mediana_mun']
    d = lambda c: 2 if c.startswith('renda') else 4
    tabela('As descritivas do IVS-7 e dos indicadores das demandas',
           ['Indicador', 'n', 'Média', 'Mediana', 'P90', 'Máx.', 'Assim.', '% zeros'],
           [[ev.ROT[c], intbr(t03.loc[c, 'n']), br(t03.loc[c, 'media'], d(c)), br(t03.loc[c, 'mediana'], d(c)), br(t03.loc[c, 'p90'], d(c)),
             br(t03.loc[c, 'max'], d(c)), br(t03.loc[c, 'assim'], 2), pctbr(t03.loc[c, 'pct_zeros'])] for c in sel],
           [2.3, 0.85, 0.85, 0.85, 0.85, 0.95, 0.65, 0.75],
           'Uma linha por indicador: n, média, mediana, percentil 90, máximo, assimetria e percentual de setores com valor zero.',
           f"Os indicadores novos de água e banheiro têm mediana zero: sem banheiro tem {pctbr(t03.loc['pct_sem_banheiro', 'pct_zeros'])} de zeros e água não chega, {pctbr(t03.loc['pct_agua_nao_encanada', 'pct_zeros'])}.",
           MOD['itens']['desc_global']['nota'], '00_referencia · T03')
    x = csv_eda('fatorial_ampliada/comparacao_nao_chega_banheiro.csv')
    sp = x[(x['bloco'] == 'spearman') & (x['indicador'] == 'Água não chega')]
    tabela('Demandas 5 e 7: “não chega” se parece mais com as outras categorias de água do que com o IVS-7',
           ['Variável', 'ρ com “não chega”', 'n'], [[r['variavel'], br(r['valor']), intbr(r['n'])] for _, r in sp.iterrows()],
           [3.6, 1.6, 1.4], 'Correlação de Spearman entre “água não chega” e cada variável do IVS-7 e as outras categorias de água, nos pares completos.',
           f"Maior ρ: {sp.loc[sp['valor'].idxmax(), 'variavel']} ({br(sp['valor'].max())}).",
           'Leitura (a) e (b) da demanda 5: compara com as outras categorias de canalização e com o IVS-7. Com 85% de zeros, a correlação de postos fica achatada pelos empates.',
           'banco_de_dados/eda/fatorial_ampliada/comparacao_nao_chega_banheiro.csv')
    for ind in ['Água não chega', 'Sem banheiro']:
        pf = x[(x['bloco'] == 'perfil_mediana') & (x['indicador'] == ind)]
        lin = []
        for var, g in pf.groupby('variavel', sort=False):
            g = g.set_index('grupo')
            dd = 2 if var.startswith('Renda') else 4
            lin.append([var, br(g.loc['> 0', 'valor'], dd), intbr(g.loc['> 0', 'n']), br(g.loc['= 0', 'valor'], dd), intbr(g.loc['= 0', 'n'])])
        rr = pf[pf['variavel'] == 'Renda média'].set_index('grupo')['valor']
        tabela(f"“{ind}”: os setores com o problema têm renda mediana de {br(rr['> 0'], 2)}, contra {br(rr['= 0'], 2)} nos demais",
               ['Variável do IVS-7', f'Mediana com {ind.lower()} > 0', 'n', 'Mediana = 0', 'n'], lin, [2.4, 1.6, 0.9, 1.2, 0.9],
               f'Perfil: a mediana de cada variável do IVS-7 nos setores com “{ind.lower()}” acima de zero e nos setores com zero.',
               f"Renda mediana {br(rr['> 0'], 2)} nos setores com o problema e {br(rr['= 0'], 2)} nos demais.",
               'É a forma mais direta de comparar uma variável que é zero na maior parte dos setores: em vez de correlação, o perfil dos dois grupos.',
               'banco_de_dados/eda/fatorial_ampliada/comparacao_nao_chega_banheiro.csv')
    pj = x[x['bloco'] == 'prova_juncao'].iloc[0]
    car = csv_eda('fatorial_ampliada/cargas.csv')
    nc = car[(car['cenario'] == 'S5') & (car['variavel'] == 'pct_moradia_nao_convencional')].iloc[0]
    numeros('Demandas 6 e 9: banheiro e habitação não convencional',
            [[pctbr(100 * pj['valor'] / pj['n']), f"dos {intbr(pj['n'])} setores com as duas variáveis têm V00238 ≤ V00495 (a junção já está em V00495)"],
             [pctbr(t03.loc['pct_moradia_nao_convencional', 'pct_zeros']), 'dos setores com moradia não convencional igual a zero'],
             [br(nc['msa']), 'MSA da moradia não convencional (cenário S5)'],
             [br(nc['comunalidade']), 'comunalidade da moradia não convencional (S5)']],
            'Somar V00238 a V00495 contaria o mesmo domicílio duas vezes; a V00495 já é a junção. As partições V00236, V00237 e V00238 estão na base e formam o banheiro graduado. '
            'A moradia não convencional entra na direção da vulnerabilidade e não foi excluída por variância baixa: o diagnóstico está aqui para a decisão.',
            fonte='fatorial_ampliada/comparacao_nao_chega_banheiro.csv · cargas.csv · 00_referencia T03')
    for i in ['F02', 'F05', 'F03', 'F15', 'F16']:
        item('00_referencia', i)
    item('00_referencia', 'F31', larga=True)
    item('00_referencia', 'F17', larga=True)
    for i in ['F32', 'F33', 'F34', 'F35']:
        if i in cat('00_referencia').index:
            item('00_referencia', i, larga=True)
    for i in ['F18', 'F19', 'F20', 'F21']:
        item('00_referencia', i)
    t15 = tab('00_referencia', 'T15')
    t11 = tab('00_referencia', 'T11').set_index('classe')
    texto('O que a EDA da versão final mostra', [
        f"{intbr(t01.iloc[-2]['setores'])} setores no recorte e {intbr(t01.iloc[-1]['setores'])} na amostra do índice; a perda vem sobretudo do sigilo, que se concentra nos setores pequenos.",
        f"Os indicadores de saneamento têm mediana zero; o mais assimétrico é {ev.ROT[t03['assim'].idxmax()]} (assimetria {br(t03['assim'].max(), 2)}).",
        f"Contra as favelas, o indicador que mais separa sozinho é {t15.iloc[0]['rotulo']} (AUC {br(t15.iloc[0]['auc'])}).",
        f"A renda tem {intbr(t11.loc['SUSPEITO', 'setores'])} setores suspeitos e {intbr(t11.loc['EXTREMO', 'setores'])} extremos coerentes; as variantes de renda tratam o extremo de BH.",
        'As demandas 1, 2, 5, 6, 7 e 9 estão atendidas com os dados acima; o que entra no índice é decisão da orientadora.'],
        fonte='00_referencia · T01 · T03 · T11 · T15')


# ── Parte 3 — análise fatorial ────────────────────────────────────────────────
def parte3():
    secao('3', 'A análise fatorial', 'A grade ampliada das demandas, as especificações do NB05, a referência e a robustez',
          'Sem bootstrap, a pedido da orientadora: a estabilidade é medida por sensibilidade por município e por reamostragem '
          'apresentada como tal. Sem rotação, Varimax e promax lado a lado em todos os cenários.')
    c = csv_eda('fatorial_ampliada/cenarios.csv')
    linhas = lambda df: [[r['cenario'], r['descricao'], r['demanda'], intbr(r['n']), br(r['kmo']), intbr(r['fatores_kaiser']),
                          intbr(r['fatores_horn']), br(r['var_explicada_2f'], 1)] for _, r in df.iterrows()]
    cab = ['Cenário', 'Variáveis', 'Demanda', 'n', 'KMO', 'Kaiser', 'Horn', 'Var. 2 fatores (%)']
    w = [1.0, 3.2, 0.8, 0.85, 0.7, 0.65, 0.6, 1.0]
    s0, s6 = c.set_index('cenario').loc['S0'], c.set_index('cenario').loc['S6']
    tabela(f"A grade das demandas: com as quatro variáveis novas (S6), o KMO sobe para {br(s6['kmo'])} e Horn pede {intbr(s6['fatores_horn'])} fatores",
           cab, linhas(c.iloc[:8]), w,
           'Uma linha por cenário da grade: variáveis, demanda que responde, setores com todos os dados (n), KMO, fatores retidos por Kaiser e por Horn e variância explicada por 2 fatores.',
           f"S0 (IVS-7) tem n {intbr(s0['n'])} e KMO {br(s0['kmo'])}; S6 (tudo isso) tem n {intbr(s6['n'])}, KMO {br(s6['kmo'])} e {intbr(s6['fatores_horn'])} fatores por Horn.",
           'Método igual ao NB04 para ser comparável: Spearman, casos completos por cenário, componentes principais, renda invertida, sempre 2 fatores na solução apresentada.',
           'banco_de_dados/eda/fatorial_ampliada/cenarios.csv')
    tabela('As três rendas e os postos dentro do município, em S0, S1 e S6', cab, linhas(c.iloc[8:]), w,
           'Mesmas colunas: as variantes de renda (sem o extremo, com a mediana) e a fatorial com postos percentis dentro do município.',
           f"As rendas não mudam a estrutura; com postos no município, o MSA mínimo de S6 cai para {br(c.set_index('cenario').loc['S6_postos_mun', 'msa_min'])}.",
           'Os postos dentro do município tiram da matriz a diferença entre cidades: se a estrutura muda muito, parte dela vinha da diferença entre municípios.',
           'banco_de_dados/eda/fatorial_ampliada/cenarios.csv')
    av = csv_eda('fatorial_ampliada/autovalores.csv')
    a6 = av[av['cenario'] == 'S6'].set_index('componente')
    figura_eda('fatorial_ampliada/figuras/fa_correlacao_ampliada.png', 'A matriz de correlação ampliada: o IVS-7 e as quatro variáveis novas',
               'Correlação de Spearman entre as variáveis; a linha separa as quatro novas (não chega, sem canalização, sem banheiro, não convencional).',
               'As novas variáveis de água e banheiro se correlacionam com o bloco de saneamento; a moradia não convencional quase não se correlaciona com nada.',
               'No formato da imagem enviada pela orientadora.', chave='mapa_spearman_foco')
    figura_eda('fatorial_ampliada/figuras/fa_scree_s6.png', f"S6: {intbr((a6['autovalor'] > a6['horn']).sum())} autovalores acima da linha de Horn",
               'Autovalores de S6 em ordem decrescente, com a linha da análise paralela de Horn.',
               f"Primeiro autovalor {br(a6.loc[1, 'autovalor'])}, segundo {br(a6.loc[2, 'autovalor'])}; Horn no segundo componente: {br(a6.loc[2, 'horn'])}.",
               MOD['itens']['autovalores']['nota'], chave='sedimentacao')
    figura_eda('fatorial_ampliada/figuras/fa_plano_s6.png', 'Demandas 3 e 11: o plano fatorial de S6 sem rotação, com Varimax e com promax',
               'Três painéis com as cargas no plano dos fatores 1 e 2; o rótulo de cada eixo vem das cargas.',
               'As rotações redistribuem as variáveis entre os dois fatores; a promax permite que eles se correlacionem.',
               MOD['itens']['variaveis']['nota'], chave='cargas')
    p = csv_eda('fatorial_ampliada/pesos.csv')
    p = p[p['cenario'].isin(['S0', 'S1', 'S6', 'S7'])]
    tabela('O peso do fator 1 em cada rotação, nos cenários principais', ['Cenário', 'Rotação', 'Peso F1 (%)', 'Peso F2 (%)', 'Maior carga F1', 'Maior carga F2', 'Φ'],
           [[r['cenario'], r['rotacao'], br(r['peso_f1'], 2), br(r['peso_f2'], 2), r['f1_maior_carga'], r['f2_maior_carga'], br(r['phi'])]
            for _, r in p.iterrows()], [0.8, 1.6, 0.9, 0.9, 1.6, 1.6, 0.6],
           'Uma linha por cenário e rotação: repartição do peso entre os dois fatores (na promax, pela matriz padrão e pela estrutura), a variável de maior carga em cada fator e a correlação Φ entre fatores.',
           f"Em S1 (IVS-6), o peso do fator 1 fica entre {br(p[p['cenario'] == 'S1']['peso_f1'].min(), 2)}% e {br(p[p['cenario'] == 'S1']['peso_f1'].max(), 2)}% conforme a rotação.",
           'As duas métricas da repartição oblíqua (padrão e estrutura) são reportadas lado a lado, sem dizer que uma se afasta ou se aproxima da literatura.',
           'banco_de_dados/eda/fatorial_ampliada/pesos.csv')
    sm = csv_eda('fatorial_ampliada/sensibilidade_municipios.csv')
    g = sm.groupby('cenario').agg(mn=('peso_f1_varimax', 'min'), mx=('peso_f1_varimax', 'max'), lixo=('lixo_muda', 'sum'), n=('municipio_fora', 'size'))
    tabela('Demanda 10: o lixo forma fator próprio no IVS-7 e deixa de formar quando entram as variáveis novas',
           ['Cenário', 'Variáveis', 'Lixo em fator próprio (Varimax)'],
           [[r['cenario'], r['descricao'], sim(r['lixo_fator_proprio_varimax']) if pd.notna(r['lixo_fator_proprio_varimax']) else 'sem lixo']
            for _, r in c.iloc[:8].iterrows()], [1.0, 4.2, 2.4],
           'Uma linha por cenário: o lixo fica sozinho no seu fator na solução Varimax?',
           f"Tirando um município por vez em S0, o lixo muda de situação em {intbr(g.loc['S0', 'lixo'])} das {intbr(g.loc['S0', 'n'])} rodadas.",
           'Num índice intraurbano, um fator próprio do lixo pode refletir a cobertura de coleta de cada município, e não a vulnerabilidade do setor.',
           'fatorial_ampliada/cenarios.csv · sensibilidade_municipios.csv')
    figura_eda('fatorial_ampliada/figuras/fa_sensibilidade_municipios.png',
               f"Um município de fora por vez: o peso do fator 1 em S6 varia entre {br(g.loc['S6', 'mn'], 2)}% e {br(g.loc['S6', 'mx'], 2)}%",
               'O peso do fator 1 (Varimax) nas rodadas em que cada município sai da estimação, em S1 e S6.',
               f"S1: de {br(g.loc['S1', 'mn'], 2)}% a {br(g.loc['S1', 'mx'], 2)}%; S6: de {br(g.loc['S6', 'mn'], 2)}% a {br(g.loc['S6', 'mx'], 2)}%.",
               'Isto não é bootstrap: é sensibilidade por município, como pedido. Mostra se alguma cidade sozinha define os pesos.', chave='sensibilidade_mun')
    v = csv_eda('fatorial_ampliada/validacao_fcu.csv').pivot_table(index='cenario', columns='medida', values='auc')
    v = v.reindex([x for x in c['cenario'] if x in v.index])
    cols = list(v.columns)
    tabela('O que o índice acrescenta à renda: a AUC do índice ao lado da renda sozinha e da média de postos',
           ['Cenário'] + cols, [[i] + [br(x) for x in r] for i, r in v.iterrows()], [1.8] + [1.9] * len(cols),
           'Uma linha por cenário: AUC contra as favelas do índice (pesos Varimax), da média simples de postos e da renda invertida sozinha.',
           f"Em S0, índice {br(v.loc['S0', cols[0]])}, média de postos {br(v.loc['S0', cols[1]])} e renda sozinha {br(v.loc['S0', cols[2]])}.",
           'A AUC mede conteúdo socioeconômico, não valida pesos: a pergunta é o que o índice acrescenta à renda, e a tabela permite responder.',
           'banco_de_dados/eda/fatorial_ampliada/validacao_fcu.csv')
    esp = pd.read_csv(E / 'ivs_especificacoes' / 'especificacoes.csv')
    ava = pd.read_csv(E / 'ivs_especificacoes' / 'avaliacao.csv').drop_duplicates('id')
    eleg = ava['elegivel'].astype(str).isin(['True', '1', '1.0'])
    ref = pd.read_csv(E / 'ivs_especificacoes' / 'referencia.csv').query("leitura == 'principal'").iloc[0]
    numeros('O NB05: a grade de especificações e a referência proposta',
            [[intbr(len(esp)), 'especificações (renda × lixo × banheiro × rotação × pesos × normalização)'],
             [intbr(eleg.sum()), 'elegíveis pelos critérios fixados antes de rodar'], [br(ref['valor_b']), 'AUC municipal da referência proposta']],
            f"Referência proposta: {ref['id']}. Por quê: {ref['porque']}.", fonte='ivs_especificacoes/especificacoes.csv · avaliacao.csv · referencia.csv')
    for rel, tit, como in [('auc_por_especificacao.png', 'A AUC das especificações do NB05', 'A AUC contra as favelas de cada especificação.'),
                           ('peso_f1_por_especificacao.png', 'O peso do fator socioeconômico nas especificações do NB05', 'O peso do fator 1 em cada especificação e a amplitude entre municípios.'),
                           ('concordancia_faixas.png', 'A concordância das faixas entre especificações', 'Quanto as faixas de vulnerabilidade concordam entre especificações.')]:
        figura_eda(f'ivs_especificacoes/figuras/{rel}', tit, como, 'Ver as tabelas do NB05 em banco_de_dados/eda/ivs_especificacoes/.',
                   'Figura do NB05 (scripts/ivs_especificacoes.py).', chave='nb05_' + rel.split('_')[0])
    t19 = tab('00_referencia', 'T19').set_index('medida')['valor']
    numeros('A fatorial da referência proposta', [[br(t19['KMO']), 'KMO'], [intbr(t19['fatores pelo critério de Kaiser']), 'fatores por Kaiser'],
                                                    [intbr(t19['fatores pela análise paralela de Horn']), 'fatores por Horn'],
                                                    [br(t19['variância explicada por 2 fatores (%)'], 1) + '%', 'variância explicada por 2 fatores']],
            MOD['itens']['adequacao']['nota'], fonte='00_referencia · T19')
    for i in ['F22', 'F23']:
        item('00_referencia', i)
    t23 = tab('00_referencia', 'T23')
    tabela(cat('00_referencia').loc['T23', 'titulo'], ['Componente', 'Dimensão', 'Carga', 'Peso da dimensão (%)', 'Peso no índice (%)'],
           [[r['rotulo'], r['dimensao'], br(r['carga']), br(r['peso_dimensao'], 1), br(r['peso'], 1)] for _, r in t23.iterrows()],
           [2.2, 2.2, 1.0, 1.5, 1.4], MOD['itens']['pesos']['como_ler'], cat('00_referencia').loc['T23', 'o_que_mostra'],
           MOD['itens']['pesos']['nota'], '00_referencia · T23')
    for i in ['F25', 'F24']:
        item('00_referencia', i)
    for v_ in ['C1_rotacao_e_pesos', 'C2_extracao', 'D5_especialista_x_dados']:
        t = tab(v_, 'T34')
        tabela(cat(v_).loc['T34', 'titulo'], ['Esquema', 'KMO', 'AUC global', 'AUC mun.', 'Elegível', 'ρ com o padrão', '% muda faixa'],
               [[r['rotulo'], br(r['kmo']), br(r['auc_global']), br(r['auc_municipal']), sim(r['elegivel']), br(r['spearman_com_padrao']),
                 pctbr(r['pct_mudam_faixa'])] for _, r in t.iterrows()], [3.0, 0.7, 0.9, 0.85, 0.75, 1.0, 0.9],
               'Uma linha por esquema; a primeira é o valor-padrão da versão, as demais as alternativas. ρ e % muda faixa são em relação à primeira linha.',
               cat(v_).loc['T34', 'o_que_mostra'], json.loads((A / v_ / 'textos.json').read_text())['sintese'], f'{v_} · T34')
    item('E2_estabilidade', 'F43')
    item('E2_estabilidade', 'F42')
    texto('O que fica para a orientadora decidir', [
        'Que variáveis entram: lixo (fator próprio no IVS-7), as novas de água e banheiro, a moradia não convencional, a cor ou raça.',
        'Qual renda: original, sem o extremo ou com a mediana do município (mudam pouco o índice).',
        'Rotação e pesos: Varimax ou promax; regra 60/40 do IVS-BH ou pesos da fatorial (padrão ou estrutura).',
        'Normalização e faixas: min-max no município (referência) ou outra; regra do IVS-BH, quartis ou outra.',
        'Parâmetros exploratórios ainda abertos: piso de população, faixas de porte, composição do IVS-Idoso e do índice de moradia, número de grupos.',
        'Tudo com as alternativas documentadas: analises_exploratorias/PERGUNTAS.md e o Catalogo_Mestre.xlsx.'],
        fonte='analises_exploratorias/PERGUNTAS.md')


# ── Partes 4 e 5 — catálogos visuais ──────────────────────────────────────────
def miniatura(origem, chave):
    MINI.mkdir(parents=True, exist_ok=True)
    destino = MINI / (chave.replace('/', '__') + '.jpg')
    if not destino.exists():
        im = Image.open(origem).convert('RGB')
        im.thumbnail((720, 720))
        im.save(destino, 'JPEG', quality=82)
    return str(destino)


def figuras_catalogo(eda: bool):
    """Só a versão final (00_referencia): blocos 1–8 na EDA, 9–13 na fatorial e no índice."""
    itens = []
    for c in [A / '00_referencia' / 'catalogo.csv']:
        v = str(c.parent.relative_to(A))
        k = pd.read_csv(c, dtype=str, keep_default_na=False)
        k = k[(k['tipo'] == 'figura') & k['bloco'].astype(int).isin(BLOCOS_EDA if eda else set(range(9, 21)) - BLOCOS_EDA)]
        for _, r in k.iterrows():
            itens.append({'img': miniatura(c.parent / r['arquivo'], f"{v}__{r['id']}"), 'rotulo': f"{v} · {r['id']}",
                          'titulo': r['titulo'], 'arquivo': f"analises_exploratorias/{v}/{r['arquivo']}"})
    return itens


def catalogo(num, nome, eda):
    itens = figuras_catalogo(eda)
    secao(num, f'Catálogo visual: {nome}', f'As {intbr(len(itens))} figuras da versão final, identificadas pelo ID, para escolher o que vai para o artigo',
          'Só identificação: cada miniatura traz a versão e o ID do Catalogo_Mestre.xlsx (aba Catálogo mestre), onde se marca "Vai para o artigo?".')
    por = 6
    n = -(-len(itens) // por)
    for k in range(n):
        lote = itens[k * por:(k + 1) * por]
        SLIDES.append({'tipo': 'grade', 'titulo': f'{nome} — {k + 1} de {n}', 'cels': lote, 'nc': 3, 'nl': 2,
                       'nota': '\n'.join(f"{x['rotulo']} — {x['titulo']} — {x['arquivo']}" for x in lote),
                       'fonte': 'Catalogo_Mestre.xlsx'})


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    parte1()
    parte2()
    parte3()
    catalogo('4', 'EDA — versão final', True)
    catalogo('5', 'análise fatorial — versão final', False)
    capa = {'tipo': 'capa', 'kicker': 'PROJETO IVS · CENSO 2022 · ELSI-BRASIL',
            'titulo': 'Análises exploratórias e análise fatorial',
            'sub': 'A EDA unificada de todas as versões, a EDA e a fatorial da versão final, e os catálogos visuais para escolher o que vai para o artigo',
            'rodape': 'Pedro Dias Soares · outubro de 2026'}
    roteiro = {'tipo': 'texto', 'titulo': 'Roteiro', 'fonte': '', 'nota': '', 'itens': [
        '1 · A EDA unificada — todas as versões comparadas contra a mesma referência.',
        '2 · A EDA da versão final — o recorte de análise com os 31 indicadores e as demandas de setembro atendidas.',
        '3 · A análise fatorial — a grade das demandas, as especificações do NB05, a referência e a robustez.',
        '4 · Catálogo visual da EDA — as figuras da versão final, só identificadas, para escolher.',
        '5 · Catálogo visual da análise fatorial — as figuras da versão final, idem.']}
    deck = {'slides': [capa, roteiro] + SLIDES,
            'saida': str(RAIZ / 'docs' / 'Apresentacoes_IVS' / 'Apresentacao_Orientadora_EDA_Fatorial_2026-10.pptx')}
    (SAIDA / 'deck_orientadora.json').write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding='utf-8')
    tipos = pd.Series([s['tipo'] for s in deck['slides']]).value_counts().to_dict()
    print(f"deck_orientadora.json: {len(deck['slides'])} especificações de slide {tipos}")


if __name__ == '__main__':
    main()
