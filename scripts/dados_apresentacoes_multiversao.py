"""Números, textos e figuras das 13 apresentações da fatorial multiversão (Fase 4).

Prompt: `docs/prompts/prompt_fatorial_multiversao_2026-10.md`, seções 4.1 e 4.2.

    ./.venv/bin/python scripts/dados_apresentacoes_multiversao.py

Lê as saídas das camadas 1 a 3 (`banco_de_dados/eda/fatorial_multiversao/`), o `.db` da entrega e a
base nacional, e grava em `apresentacoes_multiversao/`: `dados/<COD>.json` (um por indicador),
`dados/FIN.json` (o deck final), `figuras/*.png` e `Fatorial_Multiversao_numeros.xlsx`.

Cada slide tem **um** visual (gráfico ou tabela) e, ao lado, a explicação em quatro partes: o que é,
para que serve, como ler e o que mostra (pedido do Pedro, 22/10/2026: "para cada slide quero que você
explique mais o que está acontecendo, o que é aquilo, para que aquilo serve, explique o gráfico").
Nenhum número é digitado: o "o que mostra" é montado aqui a partir das tabelas; as outras três partes
são texto de método, sem número de resultado.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'src', RAIZ / 'scripts'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import eda_versoes as ev  # noqa: E402
import fatorial_multiversao as fm  # noqa: E402
from ivs_censo import ARQUIVOS_CENSO, INDICADORES_POR_NOME, MAPA_VARIAVEL_ARQUIVO  # noqa: E402
from ivs_censo.fatorial import rodar_cenario  # noqa: E402

PASTA = RAIZ / 'apresentacoes_multiversao'
DADOS, FIG = PASTA / 'dados', PASTA / 'figuras'
MV = fm.SAIDA
NAC = RAIZ / 'banco_de_dados' / 'nacional' / 'Base_Brasil_Censo2022.db'
DB = 'banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db'
br, intbr = ev.br, ev.intbr
TINTA, PETROL, CLAY, CINZA, OCRE, SURF = '#1A1A1A', '#1F4E4A', '#A83A2C', '#8B877E', '#C9822B', '#FFFFFF'
WHIS = 1.5          # bigodes do boxplot (o padrão do matplotlib), citado no "como ler"
REGIOES = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
PORTES = ['até 100 mil', '100 a 500 mil', 'mais de 500 mil']
FAIXAS = ['baixo', 'médio', 'elevado', 'muito elevado']
NOME = {'AGU': 'Água inadequada', 'ESG': 'Esgoto inadequado', 'LIX': 'Lixo inadequado',
        'MOR': 'Razão de moradores', 'ANA': 'Analfabetismo (15 anos ou mais)',
        'REN': 'Renda média do responsável', 'PPI': 'Preta, parda ou indígena',
        'CAN': 'Sem água canalizada', 'BAN': 'Sem banheiro', 'MNC': 'Moradia não convencional',
        'IDO': 'Idosos (60 anos ou mais)', 'CRI': 'Crianças (0 a 14 anos)'}
ARQ = {'AGU': 'Agua_inadequada', 'ESG': 'Esgoto_inadequado', 'LIX': 'Lixo_inadequado',
       'MOR': 'Razao_de_moradores', 'ANA': 'Analfabetismo', 'REN': 'Renda', 'PPI': 'Preta_parda_indigena',
       'CAN': 'Sem_agua_canalizada', 'BAN': 'Sem_banheiro', 'MNC': 'Moradia_nao_convencional',
       'IDO': 'Idosos', 'CRI': 'Criancas'}
DIM = {'AGU': 'Saneamento', 'ESG': 'Saneamento', 'LIX': 'Saneamento', 'CAN': 'Saneamento',
       'BAN': 'Saneamento', 'MOR': 'Socioeconômica', 'ANA': 'Socioeconômica', 'REN': 'Socioeconômica',
       'PPI': 'Socioeconômica', 'MNC': 'Morfologia', 'IDO': 'Demografia', 'CRI': 'Demografia'}
UNIDADE = {'REN': 'reais por mês', 'MOR': 'moradores por domicílio'}
# por que o indicador importa para a vulnerabilidade à saúde (texto de método, sem número)
POR_QUE = {
    'AGU': 'Água que não vem da rede geral (poço, nascente, carro-pipa, rio) tem qualidade e regularidade '
           'incertas, e expõe os moradores a doenças de veiculação hídrica, como diarreias e hepatite A.',
    'ESG': 'Sem rede de esgoto ou fossa séptica, o dejeto fica em fossa rudimentar, vala ou curso d\'água, '
           'perto das casas: é a via de verminoses, leptospirose e doenças diarreicas.',
    'LIX': 'Lixo não coletado porta a porta (queimado, enterrado, jogado em terreno ou em caçamba) atrai '
           'vetores como ratos e mosquitos. No IVS de 2012 a caçamba conta como inadequada.',
    'MOR': 'Muitas pessoas por domicílio indicam adensamento: facilita a transmissão de doenças '
           'respiratórias e reflete restrição de renda para moradia.',
    'ANA': 'Não saber ler limita o acesso a informação de saúde, a receitas, a orientações e a serviços. É o '
           'substituto, no Censo 2022, da escolaridade do chefe usada em 2012.',
    'REN': 'A renda define o acesso a alimentação, moradia, transporte e cuidado. No índice ela entra '
           'invertida: quanto menor a renda, maior a vulnerabilidade.',
    'PPI': 'Pessoas pretas, pardas e indígenas enfrentam desigualdade estrutural no acesso a renda, '
           'moradia e serviços. Entra como marcador dessa desigualdade, como no IVS de 2012.',
    'CAN': 'Mesmo com rede geral, a água pode chegar só ao terreno ou não chegar encanada: mede a entrega '
           'da água dentro de casa, um eixo diferente da fonte medida em "água inadequada".',
    'BAN': 'Sem banheiro de uso exclusivo com chuveiro e vaso, a higiene pessoal e o destino dos dejetos '
           'ficam precários: é uma privação sanitária dentro do domicílio.',
    'MNC': 'Cortiço, maloca ou estrutura degradada: moradia precária, que expõe a risco estrutural, umidade '
           'e adensamento.',
    'IDO': 'A população de 60 anos ou mais é o foco do ELSI-Brasil. Não é vulnerabilidade em si: serve para '
           'ver onde moram os idosos em relação ao IVS.',
    'CRI': 'Crianças de 0 a 14 anos: com os idosos, descrevem a estrutura etária do setor. Não é '
           'vulnerabilidade em si; ajuda a ler o IVS pela composição etária.',
}
ADEQ = {
    'dom': ('Denominador', 'domicílios particulares permanentes ocupados (V00001), equivalente ao de 2012; '
            'moradores de domicílios coletivos não entram (relatório, item a).'),
    'sig': ('Sigilo parcial', 'quando o IBGE suprimiu só parte das parcelas do numerador, elas entram como zero, '
            'o que subestima o indicador; só fica ausente quando todas foram suprimidas (item d).'),
    'cac': ('Caçamba', 'o depósito em caçamba continua classificado como destino inadequado, como no IVS de '
            '2012 (item e). É a hipótese a testar: pode refletir a forma de coleta da cidade.'),
    'ana': ('Faixa etária', 'pessoas de 15 anos ou mais, porque os agregados de 2022 não têm alfabetização abaixo '
            'dessa idade; no IVS de 2012 eram 5 anos ou mais (item b).'),
    'ren': ('Universo e extremo', 'rendimento médio das pessoas responsáveis com rendimento (V06004), calculado '
            'pelo IBGE; um setor de favela de Belo Horizonte com valor incoerente foi retirado (item c).'),
    'mor': ('Denominador', 'domicílios particulares permanentes e improvisados ocupados, para reproduzir o V0005 '
            'publicado pelo IBGE (item a).'),
    'pop': ('Denominador', 'população residente total; moradores de domicílios coletivos entram (item a).'),
    'ida': ('Faixas de idade', 'grupos etários dos agregados por setor; idosos e crianças dividem o mesmo '
            'denominador e são o numerador e o denominador do índice de envelhecimento (Galvão et al., 2025).'),
    'fora': ('Fora do índice', 'indicador complementar do Quadro 2: descreve o setor, não compõe o IVS de 2012.'),
    'dem': ('Fora do índice', 'demografia, não vulnerabilidade: descreve a estrutura etária e serve para ler o '
            'IVS proposto pelo tema do ELSI-Brasil.'),
}
ADEQ_COD = {'AGU': ['dom', 'sig'], 'ESG': ['dom', 'sig'], 'LIX': ['dom', 'sig', 'cac'], 'MOR': ['mor'],
            'ANA': ['ana'], 'REN': ['ren'], 'PPI': ['pop', 'sig'], 'CAN': ['dom', 'fora'],
            'BAN': ['dom', 'fora'], 'MNC': ['dom', 'fora'], 'IDO': ['pop', 'ida', 'dem'],
            'CRI': ['pop', 'ida', 'dem']}
COMO_LER_BOX = (f'A caixa vai do percentil 25 ao 75 (metade central dos setores); a linha vermelha é a mediana; o '
                f'losango, a média; os bigodes vão até {br(WHIS, 1)} vez a altura da caixa. Os extremos além dos '
                'bigodes não são desenhados, para a escala não ficar presa a poucos setores.')


# ─────────────────────────────────────────────────────────────────────────────
# Utilitários
# ─────────────────────────────────────────────────────────────────────────────
def coluna(cod: str) -> str:
    """A coluna que se descreve (a renda em R$, não a invertida da fatorial)."""
    return 'renda_media_sem_extremo' if cod == 'REN' else fm.VARS[cod]


def casas(cod: str) -> int:
    return 2 if cod in ('REN', 'MOR') else 3


def fmt(cod: str, v) -> str:
    return ('R$ ' + br(v, 2)) if cod == 'REN' and br(v, 2) != '—' else br(v, casas(cod))


def pct(v, d=1) -> str:
    # quase todos (99,95% a 99,99%) não podem virar "100,0%", nem quase nenhum (até 0,1%) virar "0,0%"
    return ev.pctbr(100 * v, 2 if (0.9995 <= v < 1 or 0 < v < 0.001) else d)


def desc(s: pd.Series) -> dict:
    return ev.descritivas(s)


def unidade(cod: str) -> str:
    return UNIDADE.get(cod, 'proporção de 0 a 1')


def salvar(fig, nome: str) -> str:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / nome, dpi=150, bbox_inches='tight', facecolor=SURF)
    plt.close(fig)
    return f'figuras/{nome}'


def estilo(ax, xl='', yl=''):
    ax.set_facecolor(SURF)
    for lado in ('top', 'right'):
        ax.spines[lado].set_visible(False)
    ax.set_xlabel(xl, fontsize=9)
    ax.set_ylabel(yl, fontsize=9)
    ax.tick_params(labelsize=8)


def explica(oque=None, serve=None, ler=None, mostra=None) -> list:
    """As quatro partes da coluna de explicação, na ordem; parte vazia não entra."""
    return [[e, t] for e, t in (('O que é.', oque), ('Para que serve.', serve), ('Como ler.', ler),
                                ('O que mostra.', mostra)) if t]


class Deck:
    """Os slides de uma apresentação, na ordem, com a fonte de cada um."""

    def __init__(self, cod: str, titulo: str):
        self.cod, self.titulo, self.ordem, self.slides, self.tabelas = cod, titulo, [], {}, {}
        self.n_secao = 0

    def add(self, titulo: str, fontes: list[str], **campos) -> str:
        sid = f'{self.cod}-{len(self.ordem) + 1:02d}'
        self.ordem.append(sid)
        self.slides[sid] = {'titulo': titulo, 'fontes': fontes, **campos}
        if 'cab' in campos and campos.get('linhas'):
            self.tabelas[sid] = pd.DataFrame(campos['linhas'], columns=campos['cab'])
        return sid

    def secao(self, titulo: str, sub: str) -> str:
        self.n_secao += 1
        return self.add(titulo, [], numero=str(self.n_secao), sub=sub)

    def gravar(self) -> None:
        DADOS.mkdir(parents=True, exist_ok=True)
        arquivo = ('Analise_Fatorial_e_IVS_2026-10.pptx' if self.cod == 'FIN'
                   else f'fichas/{self.cod}_{ARQ[self.cod]}.pptx')
        (DADOS / f'{self.cod}.json').write_text(json.dumps(
            {'deck': self.cod, 'titulo': self.titulo, 'arquivo': arquivo, 'ordem': self.ordem, 'slides': self.slides},
            ensure_ascii=False, indent=1), encoding='utf-8')


def tabela_desc(grupos: list[tuple[str, pd.Series]], cod: str) -> tuple[list, list]:
    cab = ['Grupo', 'Setores', 'Média', 'Mediana', 'p75', '% zeros']
    return cab, [[g, intbr(len(s.dropna())), fmt(cod, s.mean()), fmt(cod, s.median()),
                  fmt(cod, s.quantile(.75)), pct((s.dropna() == 0).mean())] for g, s in grupos]


def boxplot(grupos: list[tuple[str, pd.Series]], nome: str, yl: str, figsize=(7.2, 4.2)) -> str:
    fig, ax = plt.subplots(figsize=figsize, facecolor=SURF)
    ax.boxplot([s.dropna() for _, s in grupos], tick_labels=[g for g, _ in grupos], whis=WHIS, showfliers=False,
               medianprops={'color': CLAY, 'lw': 1.6}, showmeans=True,
               meanprops={'marker': 'D', 'markerfacecolor': PETROL, 'markeredgecolor': PETROL, 'markersize': 4})
    estilo(ax, '', yl)
    return salvar(fig, nome)


def barras(rotulos, valores, nome: str, xl: str, cor=PETROL, figsize=(7.2, 4.2)) -> str:
    fig, ax = plt.subplots(figsize=figsize, facecolor=SURF)
    y = np.arange(len(rotulos))
    ax.barh(y, valores, color=cor)
    ax.set_yticks(y)
    ax.set_yticklabels(rotulos, fontsize=7.5)
    ax.invert_yaxis()
    estilo(ax, xl)
    return salvar(fig, nome)


def acumulada(ax, serie, cor, rot=None):
    xx = np.sort(serie.dropna().to_numpy())
    ax.plot(xx, np.arange(1, len(xx) + 1) / len(xx), color=cor, label=rot)


# ─────────────────────────────────────────────────────────────────────────────
# Base
# ─────────────────────────────────────────────────────────────────────────────
def carregar():
    df = fm.carregar()
    df['porte'] = pd.cut(df['pop_municipio'], [0, 100_000, 500_000, np.inf], labels=PORTES, right=True)
    for alvo, nome in (('renda_media_sem_extremo', 'decil_renda'), ('pct_raca_pretpardind', 'decil_ppi')):
        q = df.groupby('NM_MUN')[alvo].rank(pct=True)
        df[nome] = np.ceil(10 * q).clip(1, 10)
    con = sqlite3.connect(f'file:{NAC}?mode=ro', uri=True)
    cols = [coluna(c) for c in fm.VARS]
    nac = pd.read_sql(f"SELECT {', '.join(cols)} FROM setores_censitarios WHERE urbano = 1 AND Dados_sig = 'OK'", con)
    con.close()
    nac = nac.apply(pd.to_numeric, errors='coerce')
    ivs = pd.read_csv(MV / 'ivs_proposto_por_setor.csv', dtype={'CD_SETOR': str})
    fin = pd.read_csv(MV / 'camada3_finalistas.csv')
    return df, nac, ivs, fin


# ─────────────────────────────────────────────────────────────────────────────
# Os 12 decks de indicador (seção 4.1): parte A exploratória, parte B na fatorial
# ─────────────────────────────────────────────────────────────────────────────
def deck_indicador(cod: str, df: pd.DataFrame, nac: pd.DataFrame, ivs: pd.DataFrame, fin: pd.DataFrame,
                   ef: pd.DataFrame, est: pd.DataFrame, sub: pd.DataFrame) -> Deck:
    col, nome = coluna(cod), NOME[cod]
    s = df[col]
    D = Deck(cod, nome)
    no_ivs = cod in fm.NUCLEO
    ind = INDICADORES_POR_NOME['renda_media' if cod == 'REN' else col]
    q = desc(s)
    un = unidade(cod)
    eixo_x = f'{nome} ({un})'
    corte = s.quantile(.99) if cod == 'REN' else None     # a cauda da renda achata o resto do gráfico
    nota_corte = ' Eixo horizontal cortado no percentil 99.' if corte else ''
    mvp = lambda a: f'banco_de_dados/eda/fatorial_multiversao/{a}'  # noqa: E731

    D.add(nome, ['relatorio_parcial_raic/Relatorio_Parcial_RAIC_2026_Pedro_corrigido.pdf, Quadro 2'],
          capa=True, kicker=f'INDICADOR {cod} · {DIM[cod].upper()}', sub=ind.descricao + '. ' +
          ('Compõe o IVS (Quadro 1 do relatório).' if no_ivs else 'Indicador complementar (Quadro 2), fora do IVS de 2012.')
          + ' Parte A: análise exploratória. Parte B: o indicador na análise fatorial.',
          rodape='Fatorial multiversão e IVS · Censo Demográfico 2022 · 70 municípios do ELSI-Brasil · Pedro Dias Soares · out/2026')

    # ── Parte A ──────────────────────────────────────────────────────────────
    D.secao('Análise exploratória', 'O que o indicador mede, como se distribui nos setores, onde é mais alto e como se '
                                    'relaciona com renda, favela e o Brasil — antes de qualquer análise fatorial.')
    direcao = ('exceto a renda, que entra invertida no índice.' if cod == 'REN' else
               'no sentido de mais idosos, que não é vulnerabilidade em si.' if cod == 'IDO' else
               'no sentido de mais crianças, que não é vulnerabilidade em si.' if cod == 'CRI' else 'como no IVS de 2012.')
    D.add('O que o indicador mede e por que importa', ['src/ivs_censo/indicadores.py'], blocos=[
        ['O que mede.', ind.descricao + f', em {un}.'],
        ['Por que importa para a saúde.', POR_QUE[cod]],
        ['Direção.', 'Quanto maior, mais vulnerável — ' + direcao],
        ['No índice.', 'Compõe o IVS de 2012 e o núcleo desta análise (padrão P2).' if no_ivs else
         'Fora do IVS de 2012; entra na análise fatorial como indicador que pode ou não acrescentar.']])

    arquivo = lambda vs: '; '.join(sorted({ARQUIVOS_CENSO[MAPA_VARIAVEL_ARQUIVO[v]].arquivo for v in vs}))  # noqa: E731
    D.add('Como é calculado', ['src/ivs_censo/indicadores.py', 'src/ivs_censo/fontes.py'],
          cab=['Parte', 'Definição'], colW=[1.9, 5.3], linhas=[
              ['Numerador', ' + '.join(ind.numerador)],
              ['Denominador', ' + '.join(ind.denominador) if ind.denominador else 'sem denominador (média publicada pelo IBGE)'],
              ['Escala', un], ['Arquivos do IBGE', arquivo(ind.numerador + ind.denominador)],
              ['Na análise fatorial', 'entra invertida (maior = mais vulnerável)' if cod == 'REN' else 'entra como está']],
          explica=explica(
              oque='A receita do indicador: quais variáveis do Censo vão em cima (numerador) e em baixo (denominador) '
                   'da divisão, e de que arquivo do IBGE cada uma sai.',
              serve='Permite refazer a conta e conferir qualquer número. As variáveis "V0…" são os códigos do '
                    'dicionário oficial dos agregados por setor do Censo 2022.',
              ler='Uma soma no numerador junta categorias (por exemplo, todas as formas inadequadas). O cálculo é '
                  'por setor censitário, a menor área com dado do Censo.'))
    D.add('As adequações ao Censo 2022', ['relatorio_parcial_raic/Relatorio_Parcial_RAIC_2026_Pedro_corrigido.pdf, seção IV'],
          blocos=[list(ADEQ[k]) for k in ADEQ_COD[cod]] + [[
              'Por que existem.', 'O IVS de 2012 foi feito com o Censo 2010. Quando o Censo 2022 não traz a mesma '
                                  'variável, a troca é declarada aqui, como o relatório parcial faz na seção IV.']])

    tem = s.notna()
    falta = int((~tem).sum())
    frase_cob = (f'{intbr(tem.sum())} dos {intbr(len(df))} setores ({pct(tem.mean())}) têm o dado.' +
                 (f" Nos {intbr(falta)} sem o dado, a renda mediana do responsável é "
                  f"{fmt('REN', df.loc[~tem, 'renda_media_sem_extremo'].median())}, contra "
                  f"{fmt('REN', df.loc[tem, 'renda_media_sem_extremo'].median())} nos que têm: o ausente não é aleatório."
                  if falta >= 30 else ' A ausência é desprezível.'))
    D.add(f'{pct(tem.mean())} dos setores têm o dado', [DB],
          cab=['Setores', 'Quantidade', '% do recorte', 'Renda mediana', '% favela', '% Sudeste'],
          colW=[1.3, 1.1, 1.1, 1.5, 1.0, 1.1],
          linhas=[[g, intbr(len(x)), pct(len(x) / len(df)), fmt('REN', x['renda_media_sem_extremo'].median()),
                   pct(x['is_fcu'].mean()), pct((x['regiao'] == 'Sudeste').mean())]
                  for g, x in (('com o dado', df[tem]), ('sem o dado', df[~tem]))],
          explica=explica(
              oque='Quantos setores têm o indicador calculado e quantos ficaram sem ele, com o perfil de cada grupo.',
              serve='O IBGE esconde (sigilo) números muito pequenos para ninguém ser identificado. Se o dado falta mais '
                    'num tipo de setor, as médias ficam enviesadas — por isso o perfil dos dois grupos.',
              ler='Compare a renda mediana, a % de favela e a % de Sudeste entre "com o dado" e "sem o dado". Se forem '
                  'parecidas, a falta é próxima do acaso.', mostra=frase_cob))
    sem_reg = df.groupby('regiao')[col].apply(lambda x: x.isna().mean()).reindex(REGIOES)
    D.add('Onde falta o dado', [DB], figura=barras(REGIOES, 100 * sem_reg.to_numpy(), f'{cod}_ausente_regiao.png',
                                                    '% dos setores sem o dado', cor=CINZA),
          legenda=f'{nome}: proporção de setores sem o dado, por região.', explica=explica(
              oque='A proporção de setores sem o indicador em cada região.',
              serve='Mostra se a falta de dado se concentra numa parte do país, o que pesaria nas comparações regionais.',
              ler='Cada barra é uma região; quanto mais longa, mais setores sem o dado.',
              mostra=('Nenhum setor está sem o dado, em nenhuma região.' if sem_reg.max() == 0 else
                      f'A maior proporção sem dado é no {sem_reg.idxmax()} ({pct(sem_reg.max())}); a menor, no '
                      f'{sem_reg.idxmin()} ({pct(sem_reg.min())}).')))

    fr_ass = (f"A média ({fmt(cod, q['media'])}) e a mediana ({fmt(cod, q['mediana'])}) "
              f"{'estão próximas' if abs(q['assim']) < 1 else 'se afastam'}: assimetria de {br(q['assim'], 2)}.")
    fr_zero = f" Em {ev.pctbr(q['pct_zeros'])} dos setores o valor é zero." if q['pct_zeros'] > 20 else ''
    D.add('Estatísticas descritivas', [DB], cab=['Medida', 'Valor'], colW=[3.0, 2.2], linhas=[
        ['Setores com o dado', intbr(q['n'])], ['Média', fmt(cod, q['media'])], ['Desvio-padrão', fmt(cod, q['dp'])],
        ['Mínimo', fmt(cod, q['min'])], ['Percentil 10', fmt(cod, q['p10'])], ['Percentil 25', fmt(cod, q['p25'])],
        ['Mediana', fmt(cod, q['mediana'])], ['Percentil 75', fmt(cod, q['p75'])], ['Percentil 90', fmt(cod, q['p90'])],
        ['Máximo', fmt(cod, q['max'])], ['Assimetria', br(q['assim'], 2)], ['% de setores com zero', ev.pctbr(q['pct_zeros'])]],
        explica=explica(
            oque='O resumo numérico do indicador nos setores urbanos dos 70 municípios.',
            serve='A média é puxada por valores extremos; a mediana é o valor do setor do meio. O percentil 25 (ou 75) é '
                  'o valor abaixo do qual estão 25% (ou 75%) dos setores. A assimetria mede o quanto a distribuição '
                  'tem cauda longa para um lado.',
            ler='Assimetria perto de zero: distribuição equilibrada. Acima de 1: cauda longa à direita, poucos setores '
                'com valores muito altos. Muitos zeros e assimetria alta pedem cuidado ao padronizar.',
            mostra=fr_ass + fr_zero))

    v = s.dropna()
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    ax.hist(v[v <= corte] if corte else v, bins=60, color=PETROL)
    ax.axvline(q['media'], color=CLAY, lw=1.2, label='média')
    ax.axvline(q['mediana'], color=TINTA, lw=1.2, ls='--', label='mediana')
    ax.legend(fontsize=8, frameon=False)
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    estilo(ax, eixo_x, 'número de setores')
    D.add('O histograma', [DB], figura=salvar(fig, f'{cod}_histograma.png'),
          legenda=f'{nome}: número de setores em cada faixa de valor ({intbr(q["n"])} setores).{nota_corte}', explica=explica(
              oque='Os setores agrupados em faixas de valor do indicador; a altura de cada barra é quantos setores caem '
                   'naquela faixa.',
              serve='Mostra a forma da distribuição: onde está a maioria dos setores e se há cauda longa.',
              ler='Barra alta à esquerda e cauda à direita: muitos setores com valor baixo e poucos com valor alto. A '
                  'linha vermelha é a média; a tracejada, a mediana — quanto mais afastadas, mais assimétrica.',
              mostra=fr_ass + fr_zero))
    fig, ax = plt.subplots(figsize=(7.2, 2.8), facecolor=SURF)
    ax.boxplot(v, orientation='horizontal', widths=.5, whis=WHIS, flierprops={'markersize': 2, 'alpha': .3},
               medianprops={'color': CLAY, 'lw': 1.6})
    ax.set_yticks([])
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    estilo(ax, eixo_x)
    n_ext = int((v > q['p75'] + WHIS * q['iq']).sum())
    D.add('O boxplot', [DB], figura=salvar(fig, f'{cod}_boxplot.png'),
          legenda=f'{nome}: boxplot de todos os setores, com os valores extremos.', explica=explica(
              oque='Um resumo da distribuição numa figura: caixa, mediana, bigodes e pontos extremos.',
              serve='Mostra de uma vez onde está a metade central dos setores e quantos fogem do padrão.',
              ler=(f'A caixa vai do percentil 25 ao 75; a linha vermelha é a mediana; os bigodes vão até {br(WHIS, 1)} '
                   'vez a altura da caixa; cada ponto além deles é um setor extremo.'),
              mostra=(f'{intbr(n_ext)} setores ficam além do bigode direito.' if q['iq'] > 0 else
                      'O percentil 25 e o 75 são iguais (caixa sem altura): todo valor diferente deles aparece como extremo.')))
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    acumulada(ax, v, PETROL)
    if corte:
        ax.set_xlim(right=corte)
    for p_ in (.25, .5, .75):
        ax.axhline(p_, color=CINZA, lw=.5, ls=':')
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    estilo(ax, eixo_x, 'proporção acumulada de setores')
    D.add('A distribuição acumulada', [DB], figura=salvar(fig, f'{cod}_acumulada.png'),
          legenda=f'{nome}: proporção de setores com valor até cada ponto do eixo horizontal.{nota_corte}', explica=explica(
              oque='Para cada valor no eixo horizontal, a curva dá a proporção de setores com valor igual ou menor.',
              serve='Lê qualquer percentil direto no gráfico, sem depender das faixas do histograma.',
              ler='Escolha uma altura (as linhas pontilhadas marcam 25%, 50% e 75%) e desça até o eixo: é o valor daquele '
                  'percentil. Uma subida vertical no começo indica muitos setores com o mesmo valor (por exemplo, zero).',
              mostra=f"Metade dos setores tem até {fmt(cod, q['mediana'])}; três quartos, até {fmt(cod, q['p75'])}."))
    pcts = [.10, .25, .50, .75, .90, .99]
    vals = [v.quantile(p_) for p_ in pcts]
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    ax.bar([f'p{int(p_ * 100)}' for p_ in pcts], vals, color=PETROL)
    ax.axhline(q['media'], color=CLAY, lw=1.2, label='média')
    ax.legend(fontsize=8, frameon=False)
    estilo(ax, 'percentil', eixo_x)
    D.add('A régua dos percentis', [DB], figura=salvar(fig, f'{cod}_percentis.png'),
          legenda=f'{nome}: valor nos percentis 10, 25, 50, 75, 90 e 99, e a média.', explica=explica(
              oque='O valor do indicador em seis pontos da distribuição: do setor no percentil 10 ao do percentil 99.',
              serve='Mostra quanto o indicador cresce do setor típico para os mais altos — onde está a desigualdade.',
              ler='Barras que sobem devagar e explodem no fim (p90, p99): o problema se concentra em poucos setores. A '
                  'linha vermelha é a média.',
              mostra=f'Do percentil 50 ({fmt(cod, vals[2])}) ao 99 ({fmt(cod, vals[5])}).'))

    cab, linhas = tabela_desc([(r, df.loc[df['regiao'] == r, col]) for r in REGIOES], cod)
    med = df.groupby('regiao')[col].mean().reindex(REGIOES)
    fr_reg = (f'A maior média é a do {med.idxmax()} ({fmt(cod, med.max())}); a menor, a do {med.idxmin()} '
              f'({fmt(cod, med.min())}). O Norte tem só 6 municípios: os contrastes descrevem os municípios estudados, '
              'não a região inteira.')
    D.add('Por região: a tabela', [DB], cab=cab, linhas=linhas, colW=[1.5, 1.1, 1.3, 1.3, 1.2, 0.9], explica=explica(
        oque='As estatísticas do indicador separadas pelas cinco grandes regiões.',
        serve='Mostra se o indicador tem padrão regional, o que pesa na escolha da régua (dentro de cada município ou no '
              'conjunto).',
        ler='Compare média e mediana entre as linhas; "% zeros" é a parte dos setores sem nenhum domicílio ou pessoa na '
            'condição.', mostra=fr_reg))
    D.add('Por região: o boxplot', [DB], figura=boxplot([(r, df.loc[df['regiao'] == r, col]) for r in REGIOES],
                                                        f'{cod}_regiao.png', eixo_x),
          legenda=f'{nome} por região.', explica=explica(
              oque='Um boxplot por região, lado a lado.', serve='Compara não só a média, mas a dispersão de cada região.',
              ler=COMO_LER_BOX, mostra=fr_reg))

    cab, linhas = tabela_desc([(p, df.loc[df['porte'] == p, col]) for p in PORTES], cod)
    medp = df.groupby('porte', observed=True)[col].mean()
    fr_porte = (f'A maior média é a dos municípios de {medp.idxmax()} ({fmt(cod, medp.max())}); a menor, a dos de '
                f'{medp.idxmin()} ({fmt(cod, medp.min())}).')
    D.add('Por porte do município: a tabela', [DB], cab=cab, linhas=linhas, colW=[1.6, 1.1, 1.3, 1.3, 1.1, 0.8],
          explica=explica(
              oque='As estatísticas do indicador por tamanho do município (moradores somados nos setores da base).',
              serve='Testa se o indicador acompanha o tamanho da cidade — se sim, parte dele mede porte urbano, não '
                    'vulnerabilidade.',
              ler='Três grupos: até 100 mil, de 100 a 500 mil e mais de 500 mil moradores.', mostra=fr_porte))
    D.add('Por porte do município: o boxplot', [DB],
          figura=boxplot([(p, df.loc[df['porte'] == p, col]) for p in PORTES], f'{cod}_porte.png', eixo_x),
          legenda=f'{nome} por porte do município.', explica=explica(
              oque='Um boxplot por porte de município.', serve='Mostra se cidades maiores ou menores concentram o problema.',
              ler=COMO_LER_BOX, mostra=fr_porte))

    mun = (df.groupby('NM_MUN').agg(regiao=('regiao', 'first'), setores=(col, 'count'), mediana=(col, 'median'),
                                    media=(col, 'mean'), p25=(col, lambda x: x.quantile(.25)),
                                    p75=(col, lambda x: x.quantile(.75))).sort_values('media', ascending=False))
    lin = lambda t: [[m, r.regiao, intbr(r.setores), fmt(cod, r.media), fmt(cod, r.mediana)] for m, r in t.iterrows()]  # noqa: E731
    D.add('Os 70 municípios: maiores e menores médias', [DB],
          cab=['Município', 'Região', 'Setores', 'Média', 'Mediana'], colW=[2.4, 1.3, 0.9, 1.3, 1.3],
          linhas=lin(mun.head(10)) + lin(mun.tail(10)), explica=explica(
              oque='Os 10 municípios com a maior média do indicador e os 10 com a menor.',
              serve='Identifica onde o indicador é mais e menos presente. A tabela completa está no apêndice.',
              ler='Atenção à coluna "Setores": município com poucos setores tem média instável, que muda muito com um '
                  'setor a mais ou a menos.',
              mostra=(f'Maior média: {mun.index[0]} ({fmt(cod, mun.media.iloc[0])}, {intbr(mun.setores.iloc[0])} setores); '
                      f'menor: {mun.index[-1]} ({fmt(cod, mun.media.iloc[-1])}).')))
    fig, ax = plt.subplots(figsize=(7.4, 4.4), facecolor=SURF)
    m2 = mun.sort_values('mediana')
    x = np.arange(len(m2))
    ax.vlines(x, m2.p25, m2.p75, color=CINZA, lw=1)
    ax.plot(x, m2.mediana, 'o', color=PETROL, ms=3)
    ax.set_xticks(x)
    ax.set_xticklabels(m2.index, rotation=90, fontsize=4.5)
    estilo(ax, '', eixo_x)
    D.add('Os 70 municípios, ordenados pela mediana', [DB], figura=salvar(fig, f'{cod}_municipios.png'),
          legenda=f'{nome}: mediana (ponto) e intervalo entre os percentis 25 e 75 (traço) de cada município.',
          explica=explica(
              oque='Cada coluna é um município: o ponto é a mediana dos setores dele e o traço vai do percentil 25 ao 75.',
              serve='Mostra ao mesmo tempo o nível de cada cidade (o ponto) e a desigualdade dentro dela (o tamanho do '
                    'traço).',
              ler='Da esquerda para a direita, das cidades com mediana mais baixa às mais altas. Traço longo: setores '
                  'muito diferentes entre si na mesma cidade.',
              mostra=(f'{(m2.mediana == 0).sum()} dos 70 municípios têm mediana zero.' if (m2.mediana == 0).any()
                      else f'A mediana vai de {fmt(cod, m2.mediana.min())} a {fmt(cod, m2.mediana.max())}.')))

    g = df.groupby('NM_MUN')[col]
    des = pd.DataFrame({'setores': g.count(), 'mediana': g.median(), 'iq': g.quantile(.75) - g.quantile(.25),
                        'gini': g.apply(lambda x: ev.gini(x.dropna().to_numpy()) if x.min() >= 0 else np.nan)})
    des = des[des['setores'] >= fm.PISO_MUN].sort_values('gini', ascending=False)
    fr_des = (f'Entre os {len(des)} municípios com pelo menos {fm.PISO_MUN} setores, o Gini vai de {br(des.gini.min(), 3)} '
              f'({des.gini.idxmin()}) a {br(des.gini.max(), 3)} ({des.gini.idxmax()}).')
    D.add('A desigualdade dentro das cidades: a tabela', [DB],
          cab=['Município', 'Setores', 'Intervalo interquartil', 'Gini'], colW=[2.6, 1.0, 2.0, 1.2],
          linhas=[[m, intbr(r.setores), fmt(cod, r.iq), br(r.gini, 3)] for m, r in pd.concat([des.head(8), des.tail(4)]).iterrows()],
          explica=explica(
              oque='Duas medidas de quanto os setores de uma mesma cidade diferem entre si: o intervalo interquartil '
                   '(percentil 75 menos 25) e o Gini.',
              serve='O IVS é intraurbano: quer achar as diferenças dentro da cidade. Indicador que varia pouco dentro das '
                    'cidades contribui pouco para isso.',
              ler='O Gini vai de 0 (todos os setores iguais) a 1 (tudo concentrado num setor). Mostra os 8 municípios mais '
                  'desiguais e os 4 menos.', mostra=fr_des))
    fig, ax = plt.subplots(figsize=(7.2, 4.4), facecolor=SURF)
    ax.scatter(des['mediana'], des['gini'], s=np.clip(des['setores'] / 40, 8, 200), color=PETROL, alpha=.7)
    for m, r in pd.concat([des.head(3), des.tail(2)]).iterrows():
        ax.annotate(m, (r['mediana'], r['gini']), fontsize=6.5, xytext=(3, 3), textcoords='offset points')
    estilo(ax, f'mediana do município ({un})', 'Gini entre os setores')
    D.add('A desigualdade dentro das cidades: o gráfico', [DB], figura=salvar(fig, f'{cod}_desigualdade.png'),
          legenda=f'{nome}: mediana × Gini de cada município (tamanho do ponto = número de setores).', explica=explica(
              oque='Cada ponto é um município: na horizontal, o nível do indicador; na vertical, a desigualdade entre os '
                   'setores dele.',
              serve='Separa cidades com o problema espalhado (nível alto, Gini baixo) de cidades com o problema '
                    'concentrado em poucos setores (Gini alto).',
              ler='Pontos maiores são cidades com mais setores. Os nomes marcados são os extremos de desigualdade.',
              mostra=fr_des))

    fav, fora = df.loc[df['is_fcu'] == 1, col], df.loc[df['is_fcu'] == 0, col]
    a, b = fav.mean(), fora.mean()
    fr_fav = (f'Média de {fmt(cod, a)} nos setores de favela e de {fmt(cod, b)} fora delas'
              + (f' (razão de {br(a / b, 1)}).' if b and b > 0 else '.'))
    cab, linhas = tabela_desc([('Favela e comunidade urbana', fav), ('Fora de favela', fora)], cod)
    D.add('Favela e fora da favela: a tabela', [DB], cab=cab, linhas=linhas, colW=[2.3, 1.0, 1.2, 1.2, 1.0, 0.8],
          explica=explica(
              oque='As estatísticas do indicador nos setores de favela e comunidade urbana (classificação do IBGE) e nos '
                   'demais.',
              serve='Favela é um território sabidamente vulnerável: um indicador de vulnerabilidade deveria ser mais alto '
                    'nela. É uma checagem de bom senso, não uma validação.',
              ler='Compare as médias; a razão diz quantas vezes o valor na favela é o de fora.', mostra=fr_fav))
    D.add('Favela e fora da favela: o boxplot', [DB],
          figura=boxplot([('Favela', fav), ('Fora de favela', fora)], f'{cod}_favela.png', eixo_x),
          legenda=f'{nome}: setores de favela e fora de favela.', explica=explica(
              oque='Um boxplot para os setores de favela e outro para os demais.',
              serve='Mostra se a diferença está em todos os setores ou só em alguns.', ler=COMO_LER_BOX, mostra=fr_fav))

    xdec, rotdec = (('decil_ppi', 'decil de cor/raça (preta, parda ou indígena) no município') if cod == 'REN' else
                    ('decil_renda', 'decil de renda do setor no município (1 = mais pobre)'))
    curva = df.groupby(xdec)[col].agg(['mean', 'median'])
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    ax.plot(curva.index, curva['mean'], 'o-', color=PETROL, label='média')
    ax.plot(curva.index, curva['median'], 's--', color=CLAY, ms=3, label='mediana')
    ax.set_xticks(range(1, 11))
    ax.legend(fontsize=8, frameon=False)
    estilo(ax, rotdec, eixo_x)
    fr_grad = f"No decil 1 a média é {fmt(cod, curva['mean'].iloc[0])}; no decil 10, {fmt(cod, curva['mean'].iloc[-1])}."
    D.add('O indicador ao longo da renda' if cod != 'REN' else 'A renda ao longo da cor/raça', [DB],
          figura=salvar(fig, f'{cod}_gradiente.png'), legenda=f'{nome} por {rotdec}.', explica=explica(
              oque=('Os setores de cada município ordenados pela renda e divididos em 10 grupos iguais (decis); o gráfico '
                    'dá a média e a mediana do indicador em cada grupo.') if cod != 'REN' else
                   ('Os setores de cada município ordenados pela proporção de pessoas pretas, pardas e indígenas e '
                    'divididos em 10 grupos; o gráfico dá a renda média e mediana de cada grupo.'),
              serve='Mostra o gradiente social: se o indicador piora à medida que a renda cai. Como os decis são feitos '
                    'dentro de cada município, a comparação é sempre entre setores da mesma cidade.',
              ler='Linha descendente da esquerda para a direita: o indicador é maior nos setores mais pobres. Linha plana: '
                  'não depende da renda.', mostra=fr_grad))

    qn = desc(nac[col])
    fr_br = f"No Brasil urbano a média é {fmt(cod, qn['media'])}; nos 70 municípios, {fmt(cod, q['media'])}."
    fontes_br = [NAC.relative_to(RAIZ).as_posix(), DB]
    cab, linhas = tabela_desc([('Brasil, setores urbanos', nac[col]), ('70 municípios do ELSI', s)], cod)
    D.add('Os 70 municípios e o Brasil urbano: a tabela', fontes_br, cab=cab, linhas=linhas,
          colW=[2.3, 1.0, 1.2, 1.2, 1.0, 0.8], explica=explica(
              oque='O indicador nos setores urbanos de todo o Brasil e nos dos 70 municípios do ELSI-Brasil.',
              serve='Diz se o recorte do estudo é parecido com o país urbano, ou se há viés de seleção dos municípios.',
              ler='Médias próximas: o recorte representa bem o Brasil urbano neste indicador.', mostra=fr_br))
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    acumulada(ax, nac[col], CINZA, 'Brasil urbano')
    acumulada(ax, v, PETROL, '70 municípios')
    if corte:
        ax.set_xlim(right=corte)
    ax.legend(fontsize=8, frameon=False)
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    estilo(ax, eixo_x, 'proporção acumulada de setores')
    D.add('Os 70 municípios e o Brasil urbano: o gráfico', fontes_br, figura=salvar(fig, f'{cod}_brasil.png'),
          legenda=f'{nome}: distribuição acumulada no Brasil urbano e nos 70 municípios.{nota_corte}',
          explica=explica(oque='As duas distribuições acumuladas sobrepostas.',
                          serve='Compara a distribuição inteira, não só a média.',
                          ler='Curva mais à direita: valores mais altos. Curvas coladas: as duas populações de setores são '
                              'parecidas.', mostra=fr_br))

    top = df.loc[s.nlargest(10).index, ['NM_MUN', 'is_fcu', 'v0001', col]]
    p99 = s.quantile(.99)
    fr14 = f'O percentil 99 é {fmt(cod, p99)}; {intbr((s > p99).sum())} setores ficam acima dele.'
    if cod == 'REN':
        ex = df.loc[df['renda_media'].notna() & df['renda_media_sem_extremo'].isna(), ['NM_MUN', 'renda_media']]
        fr14 += (f' O setor retirado (item c do relatório) fica fora desta lista: {ex.NM_MUN.iloc[0]}, '
                 f'{fmt("REN", ex.renda_media.iloc[0])}.')
    D.add('Os valores extremos', [DB], cab=['Município', 'Favela', 'Moradores', 'Valor'], colW=[2.8, 1.0, 1.3, 1.9],
          linhas=[[r.NM_MUN, 'sim' if r.is_fcu == 1 else 'não', intbr(r.v0001), fmt(cod, r[col])] for _, r in top.iterrows()],
          explica=explica(
              oque='Os 10 setores com o maior valor do indicador.',
              serve='Ajuda a separar extremo verdadeiro (um setor realmente muito carente, ou muito rico) de erro de dado. '
                    'A coluna "Moradores" mostra setores pequenos, onde um domicílio muda muito a proporção.',
              ler='Proporção 1 quer dizer todos os domicílios (ou pessoas) do setor na condição.', mostra=fr14))

    # ── Parte B ──────────────────────────────────────────────────────────────
    D.secao('Na análise fatorial', 'Como o indicador se relaciona com os outros 11, quanto compartilha com eles, o que '
                                   'acontece quando entra ou sai e o peso que recebe no índice.')
    Rg = pd.read_csv(MV / 'camada1_12_global_correlacao.csv', index_col=0)
    Rm = pd.read_csv(MV / 'camada1_12_municipal_correlacao.csv', index_col=0)
    outros = [c for c in fm.VARS if c != cod]
    cor = pd.DataFrame({'g': Rg.loc[cod, outros], 'm': Rm.loc[cod, outros]}).sort_values('g', key=abs, ascending=False)
    fr_cor = (f'A correlação mais forte é com {NOME[cor.index[0]]}: {br(cor.g.iloc[0], 2)} no conjunto e '
              f'{br(cor.m.iloc[0], 2)} dentro dos municípios.')
    ler_cor = ('A correlação de Spearman vai de −1 a 1: perto de 1, os setores com valor alto num indicador também têm '
               'valor alto no outro; perto de 0, não há relação; negativa, um sobe quando o outro desce. "No conjunto" '
               'compara todos os setores; "dentro dos municípios", cada setor só com os da própria cidade.')
    fontes_cor = [mvp('camada1_12_global_correlacao.csv'), mvp('camada1_12_municipal_correlacao.csv')]
    D.add('Correlação com os outros 11: a tabela', fontes_cor, cab=['Indicador', 'No conjunto', 'Dentro dos municípios'],
          colW=[3.2, 1.6, 2.2], linhas=[[NOME[c], br(r.g, 2), br(r.m, 2)] for c, r in cor.iterrows()], explica=explica(
              oque='A correlação do indicador com cada um dos outros 11, nos setores que têm os 12.',
              serve='A análise fatorial agrupa os indicadores que andam juntos. Correlações altas dizem com quem este '
                    'indicador vai formar uma dimensão.', ler=ler_cor, mostra=fr_cor))
    fig, ax = plt.subplots(figsize=(7.2, 4.4), facecolor=SURF)
    y = np.arange(len(cor))
    ax.barh(y - .2, cor.g, .4, color=PETROL, label='no conjunto')
    ax.barh(y + .2, cor.m, .4, color=CLAY, label='dentro dos municípios')
    ax.set_yticks(y)
    ax.set_yticklabels([NOME[c] for c in cor.index], fontsize=7)
    ax.invert_yaxis()
    ax.axvline(0, color=TINTA, lw=.6)
    ax.legend(fontsize=7, frameon=False)
    estilo(ax, 'correlação de Spearman')
    D.add('Correlação com os outros 11: o gráfico', fontes_cor, figura=salvar(fig, f'{cod}_correlacao.png'),
          legenda='Spearman nos setores com os 12 indicadores; renda invertida.', explica=explica(
              oque='As mesmas correlações em barras: verde, no conjunto; vermelho, dentro dos municípios.',
              serve='Quando a barra vermelha encolhe, parte da relação vinha de diferenças entre cidades, não de diferenças '
                    'dentro delas.',
              ler='Barra para a direita: relação positiva; para a esquerda, negativa. Ordenado da mais forte para a mais '
                  'fraca.', mostra=fr_cor))

    cg = pd.read_csv(MV / 'camada1_12_global_cargas.csv').set_index('codigo').loc[cod]
    cm = pd.read_csv(MV / 'camada1_12_municipal_cargas.csv').set_index('codigo').loc[cod]
    medidas = [('MSA', 'msa'), ('Comunalidade', 'h2'), ('Sem rotação, F1', 'sem_rotacao_F1'), ('Sem rotação, F2', 'sem_rotacao_F2'),
               ('Varimax, F1', 'varimax_F1'), ('Varimax, F2', 'varimax_F2'), ('Promax padrão, F1', 'promax_padrao_F1'),
               ('Promax padrão, F2', 'promax_padrao_F2'), ('Promax estrutura, F1', 'promax_estrutura_F1'),
               ('Promax estrutura, F2', 'promax_estrutura_F2')]
    fr_fat = (f'Comunalidade de {br(cg.h2, 3)} no conjunto e {br(cm.h2, 3)} dentro dos municípios (critério: '
              f'{br(fm.CRIT["h2"], 2)}); MSA de {br(cg.msa, 3)} (critério: {br(fm.CRIT["msa"], 2)}).')
    fontes_c = [mvp('camada1_12_global_cargas.csv'), mvp('camada1_12_municipal_cargas.csv')]
    D.add('Na análise fatorial das 12: a tabela', fontes_c, cab=['Medida', 'No conjunto', 'Dentro dos municípios'],
          colW=[2.8, 1.6, 2.2], linhas=[[r, br(cg[k], 3), br(cm[k], 3)] for r, k in medidas], explica=explica(
              oque='O resultado da análise fatorial dos 12 indicadores juntos (eixo principal, 2 fatores), nas duas réguas.',
              serve='A carga diz quanto o indicador "pertence" a cada fator (F1, F2). A comunalidade é a parte da variação '
                    'dele explicada pelos fatores; o MSA, o quanto ele combina com os outros para uma fatorial.',
              ler=('Carga perto de 1 (ou −1): pertence ao fator; perto de 0, não. Comunalidade abaixo de '
                   f'{br(fm.CRIT["h2"], 2)} e MSA abaixo de {br(fm.CRIT["msa"], 2)} são os limites pré-registrados. '
                   'Varimax mantém os fatores independentes; promax deixa que se correlacionem.'), mostra=fr_fat))
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    rot = ['sem_rotacao', 'varimax', 'promax_padrao', 'promax_estrutura']
    xr, w_ = np.arange(len(rot)), .2
    for k, (c_, cor_, rg) in enumerate(((cg, PETROL, 'no conjunto'), (cm, CLAY, 'dentro dos municípios'))):
        ax.bar(xr - 1.5 * w_ + 2 * k * w_, [c_[f'{r}_F1'] for r in rot], w_, color=cor_, label=f'F1 — {rg}')
        ax.bar(xr - .5 * w_ + 2 * k * w_, [c_[f'{r}_F2'] for r in rot], w_, color=cor_, alpha=.45, label=f'F2 — {rg}')
    ax.set_xticks(xr)
    ax.set_xticklabels(['sem rotação', 'Varimax', 'promax padrão', 'promax estrutura'], fontsize=8)
    ax.axhline(0, color=TINTA, lw=.6)
    ax.legend(fontsize=7, frameon=False, ncol=2)
    estilo(ax, '', 'carga')
    D.add('Na análise fatorial das 12: as cargas', fontes_c, figura=salvar(fig, f'{cod}_cargas.png'),
          legenda=f'{nome}: carga em F1 (cor cheia) e F2 (cor clara), por rotação e régua.', explica=explica(
              oque='As cargas do indicador nos dois fatores, em cada forma de rotação, nas duas réguas.',
              serve='Mostra se o indicador fica sempre no mesmo fator, seja qual for a rotação — sinal de que a posição '
                    'dele na estrutura é estável.',
              ler='Barra alta em F1 e baixa em F2: o indicador pertence a F1. Barras parecidas nas quatro rotações: a '
                  'conclusão não depende do método.', mostra=fr_fat))

    e = ef[ef['codigo'] == cod].set_index('regua')
    fr_es = (f"Na régua municipal, em {pct(e.at['municipal', 'derruba_elegibilidade'])} dos pares a combinação era elegível "
             f"sem ele e deixa de ser com ele; ao entrar, custa na mediana {intbr(-e.at['municipal', 'delta_n_mediana'])} "
             f"setores e muda o KMO em {br(e.at['municipal', 'delta_kmo_mediana'], 3)}.")
    D.add('O que acontece quando ele entra ou sai', [mvp('camada1_efeito_variavel.csv')],
          cab=['Nas 4.017 combinações', 'No conjunto', 'Dentro dos municípios'], colW=[3.4, 1.5, 2.1], linhas=[
              ['Pares comparados', intbr(e.at['global', 'pares']), intbr(e.at['municipal', 'pares'])],
              ['Variação mediana do KMO', br(e.at['global', 'delta_kmo_mediana'], 3), br(e.at['municipal', 'delta_kmo_mediana'], 3)],
              ['Setores perdidos (mediana)', intbr(-e.at['global', 'delta_n_mediana']), intbr(-e.at['municipal', 'delta_n_mediana'])],
              ['% elegível sem ele', pct(e.at['global', 'elegivel_sem']), pct(e.at['municipal', 'elegivel_sem'])],
              ['% elegível com ele', pct(e.at['global', 'elegivel_com']), pct(e.at['municipal', 'elegivel_com'])],
              ['% dos pares em que derruba', pct(e.at['global', 'derruba_elegibilidade']), pct(e.at['municipal', 'derruba_elegibilidade'])],
              ['Comunalidade mediana', br(e.at['global', 'h2_mediana'], 3), br(e.at['municipal', 'h2_mediana'], 3)]],
          explica=explica(
              oque='Foram rodadas todas as 4.017 combinações de 3 ou mais dos 12 indicadores. Aqui se comparam os pares de '
                   'combinações que só diferem por este indicador.',
              serve='Isola o efeito de incluir este indicador: se melhora ou piora a adequação (KMO), quantos setores custa '
                    '(por sigilo) e se faz a combinação deixar de passar nos critérios.',
              ler=f'KMO vai de 0 a 1 e mede se os indicadores compartilham variação suficiente para uma fatorial; acima de '
                  f'{br(fm.CRIT["kmo"], 2)} é adequado. "Elegível" = passa nos quatro critérios pré-registrados.',
              mostra=fr_es))
    h2s = sub[sub[cod] == 1][['regua', f'h2_{cod}']].dropna()
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    for rg, cor_, rot_ in (('global', PETROL, 'no conjunto'), ('municipal', CLAY, 'dentro dos municípios')):
        ax.hist(h2s.loc[h2s.regua == rg, f'h2_{cod}'], bins=40, color=cor_, alpha=.6, label=rot_)
    ax.axvline(fm.CRIT['h2'], color=TINTA, lw=1, ls='--')
    ax.legend(fontsize=8, frameon=False)
    estilo(ax, 'comunalidade nas combinações em que entra', 'combinações')
    abaixo = (h2s.loc[h2s.regua == 'municipal', f'h2_{cod}'] < fm.CRIT['h2']).mean()
    D.add('A comunalidade dele nas 4.017 combinações', [mvp('camada1_subconjuntos.csv')],
          figura=salvar(fig, f'{cod}_comunalidade.png'),
          legenda=f'{nome}: comunalidade em cada combinação em que entra; tracejado: critério {br(fm.CRIT["h2"], 2)}.',
          explica=explica(
              oque='A comunalidade do indicador em cada uma das combinações em que ele entra, nas duas réguas.',
              serve='Mostra se o indicador compartilha variação com os outros de forma consistente, ou só em algumas '
                    'combinações.',
              ler='Histograma à direita da linha tracejada: o indicador costuma passar no critério. À esquerda: costuma '
                  'ficar de fora da estrutura comum.',
              mostra=f'Dentro dos municípios, fica abaixo do critério em {pct(abaixo)} das combinações em que entra.'))

    pc = f'peso_{cod}'
    lin_p = []
    for _, f in fin.iterrows():
        papel = f['papel'].replace('alternativa_', 'alt. ').replace('_', ' ')
        if pc in f and not pd.isna(f[pc]):
            ee = est.loc[est['id'] == f['id'], pc]
            lin_p.append([papel, f['id'], pct(abs(f[pc])), pct(abs(ee).min()), pct(abs(ee).max())])
        else:
            lin_p.append([papel, f['id'], 'fora', '—', '—'])
    fontes_p = [mvp('camada3_finalistas.csv'), mvp('camada3_estabilidade.csv')]
    if cod in ('IDO', 'CRI'):
        t = ivs.drop(columns=[col], errors='ignore').merge(df[['CD_SETOR', col]], on='CD_SETOR')
        mf = t[t['faixa_ivs_bh'] >= 0].groupby('faixa_ivs_bh')[col].mean()
        fr_p = (f'Fora do índice. Correlação de Spearman com o IVS proposto: {br(ev.rho(t["ivs"], t[col]), 2)}. Média por '
                'faixa, de baixo a muito elevado: ' + ' · '.join(fmt(cod, x) for x in mf) + '.')
    else:
        fr_p = (f'No IVS proposto o peso é {lin_p[0][2]}' + (f'; tirando um município por vez, vai de {lin_p[0][3]} a '
                                                            f'{lin_p[0][4]}.' if lin_p[0][2] != 'fora' else '.'))
    D.add('O peso no índice', fontes_p, cab=['Finalista', 'Especificação', 'Peso', 'Menor sem 1 município', 'Maior'],
          colW=[2.0, 1.1, 1.0, 1.9, 1.0], linhas=lin_p, explica=explica(
              oque='O peso do indicador no índice em cada especificação finalista (a proposta e as alternativas de maior '
                   'impacto), e o menor e o maior peso quando se tira um município por vez.',
              serve='Mostra quanto o indicador conta no IVS e se esse peso depende de uma cidade específica.',
              ler='Peso é a fração do índice que vem deste indicador (os pesos de todos somam 100%). "Fora": não entra '
                  'naquela especificação.', mostra=fr_p))
    if cod in ('IDO', 'CRI'):
        fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
        ax.bar(FAIXAS, mf.to_numpy(), color=PETROL)
        estilo(ax, 'faixa do IVS proposto', f'{nome} (média)')
        D.add('Ao longo das faixas do IVS proposto', [mvp('ivs_proposto_por_setor.csv')],
              figura=salvar(fig, f'{cod}_por_faixa.png'), legenda=f'{nome}: média por faixa do IVS proposto.',
              explica=explica(
                  oque='A média do indicador nos setores de cada faixa de vulnerabilidade do IVS proposto.',
                  serve='Responde à pergunta do ELSI: os idosos (ou as crianças) moram mais nos setores mais ou menos '
                        'vulneráveis?', ler='Barras que sobem para a direita: mais presentes nos setores mais vulneráveis.',
                  mostra=fr_p))
    elif lin_p[0][2] != 'fora':
        ee = 100 * est.loc[est['id'] == fin['id'].iloc[0], pc].abs()
        fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
        ax.hist(ee, bins=20, color=PETROL)
        ax.axvline(100 * abs(fin[pc].iloc[0]), color=CLAY, lw=1.2)
        estilo(ax, 'peso no índice (%), sem um município', 'rodadas')
        D.add('O peso sem um município por vez', [mvp('camada3_estabilidade.csv')],
              figura=salvar(fig, f'{cod}_peso_estabilidade.png'),
              legenda=f'{nome}: peso no IVS proposto em cada uma das 70 rodadas; linha vermelha: peso com todos.',
              explica=explica(
                  oque='O peso do indicador recalculado 70 vezes, cada vez sem um dos municípios.',
                  serve='É a medida de incerteza adotada (a reamostragem de setores subestimava). Se um município sozinho '
                        'muda muito o peso, a fatorial depende dele.',
                  ler='Histograma estreito em torno da linha vermelha: peso estável. Barras isoladas longe dela: um município '
                      'que puxa o peso.', mostra=fr_p))

    h2m = e.at['municipal', 'h2_mediana']
    crit = [h2m >= fm.CRIT['h2'], -e.at['municipal', 'delta_n_mediana'] <= 0.05 * len(df),
            e.at['municipal', 'derruba_elegibilidade'] <= .5]
    D.add('Síntese', ['seções anteriores deste deck'], blocos=[
        ['Distribuição.', fr_ass + fr_zero],
        ['Cobertura.', frase_cob],
        ['Onde é mais alto.', fr_reg],
        ['Gradiente social.', fr_grad],
        ['Relações.', fr_cor],
        ['Na fatorial.', f'Comunalidade mediana de {br(h2m, 3)} dentro dos municípios; atende a {sum(crit)} dos 3 critérios '
                         'da Fase 1 (comunalidade, perda de base, elegibilidade).'],
        ['Proposta.', 'Entra no IVS proposto (padrão P2: os 7 do Quadro 1).' if no_ivs else
         'Fica fora do IVS proposto (padrão P2); a decisão é da orientadora.']])

    todos = lin(mun)
    for k, parte in enumerate((todos[:35], todos[35:])):
        D.add(f'Apêndice: os 70 municípios ({k + 1} de 2)', [DB], cab=['Município', 'Região', 'Setores', 'Média', 'Mediana'],
              linhas=parte, duas=True)
    return D


# ─────────────────────────────────────────────────────────────────────────────
# O deck final (seção 4.2)
# ─────────────────────────────────────────────────────────────────────────────
def mapa_calor(M: pd.DataFrame, nome: str, vmin=-1, vmax=1, cmap='RdBu_r', rot=None) -> str:
    fig, ax = plt.subplots(figsize=(7.2, 6.0), facecolor=SURF)
    ax.imshow(M.to_numpy(dtype=float), cmap=cmap, vmin=vmin, vmax=vmax)
    rot = rot or NOME
    ax.set_xticks(range(len(M.columns)))
    ax.set_xticklabels([rot.get(c, c) for c in M.columns], rotation=60, ha='right', fontsize=7)
    ax.set_yticks(range(len(M)))
    ax.set_yticklabels([rot.get(c, c) for c in M.index], fontsize=7)
    meio, meia = (vmin + vmax) / 2, (vmax - vmin) / 2
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = float(M.iat[i, j])
            ax.text(j, i, br(v, 2), ha='center', va='center', fontsize=5.5,
                    color='white' if abs(v - meio) > .55 * meia else TINTA)
    return salvar(fig, nome)


def amplitude_texto(e: pd.DataFrame, cods: list[str]) -> str:
    """O indicador cujo peso mais varia ao tirar um município, com o menor e o maior peso."""
    a = pd.DataFrame({c: e[f'peso_{c}'].abs() for c in cods})
    c = (a.max() - a.min()).idxmax()
    return f'dentro das dimensões, o peso que mais varia é o de {NOME[c]} ({pct(a[c].min())} a {pct(a[c].max())})'


def matriz_linhas(M: pd.DataFrame) -> tuple[list, list]:
    return [''] + list(M.columns), [[NOME.get(i, i)] + [br(v, 2) for v in r] for i, r in M.iterrows()]


def montar_final(df: pd.DataFrame, ivs: pd.DataFrame, fin: pd.DataFrame) -> Deck:
    D = Deck('FIN', 'Análise fatorial multiversão e o IVS proposto')
    mv = lambda a: f'banco_de_dados/eda/fatorial_multiversao/{a}'  # noqa: E731
    sub = pd.read_csv(MV / 'camada1_subconjuntos.csv')
    ef = pd.read_csv(MV / 'camada1_efeito_variavel.csv')
    esp = pd.read_csv(MV / 'camada2_especificacoes.csv')
    esp['equivalente'] = esp['equivalente'].astype('boolean')     # vem do CSV com vazios: o ~ daria -1/-2
    eixos = pd.read_csv(MV / 'camada2_efeito_eixo.csv').set_index('eixo')
    est = pd.read_csv(MV / 'camada3_estabilidade.csv')
    rep = pd.read_csv(MV / 'camada3_replicacao.csv').set_index('id')
    perf = pd.read_csv(MV / 'camada3_perfil_perdidos.csv')
    prop = fin[fin['papel'] == 'proposta'].iloc[0]
    cods12 = list(fm.VARS)

    D.add('Análise fatorial multiversão e o IVS proposto', ['docs/prompts/prompt_fatorial_multiversao_2026-10.md'],
          capa=True, kicker='ÍNDICE DE VULNERABILIDADE À SAÚDE · CENSO 2022 · 70 MUNICÍPIOS DO ELSI-BRASIL',
          sub='A análise exploratória dos 12 indicadores, as matrizes, as 4.017 combinações, os métodos pedidos pela '
              'orientadora e o IVS calculado com as escolhas padrão — como proposta, com o custo de cada alternativa.',
          rodape='Pedro Dias Soares · Fiocruz Minas — IRR · out/2026')
    D.add('Como esta apresentação está organizada', ['docs/prompts/prompt_fatorial_multiversao_2026-10.md'], blocos=[
        ['O ponto de partida.', 'O relatório parcial corrigido, os 12 indicadores e o que as análises anteriores ensinaram.'],
        ['A análise exploratória.', 'Os 12 indicadores lado a lado: distribuição, zeros, dados faltantes, regiões e o '
                                    'gradiente de renda. Cada indicador tem, além disso, uma apresentação própria com a '
                                    'exploração completa.'],
        ['A análise fatorial.', 'As matrizes de correlação, o número de fatores, as 4.017 combinações de indicadores e os '
                                'métodos de rotação, peso, normalização e sigilo.'],
        ['O IVS proposto.', 'A solução com as escolhas padrão: cargas, pesos, estabilidade, faixas e quem mora em cada faixa.'],
        ['As decisões.', 'O que fica para a orientadora decidir, com o custo de cada opção.']])

    # 1. ponto de partida
    D.secao('Ponto de partida', 'O relatório parcial corrigido e os 12 indicadores do Quadro 2.')
    con = sqlite3.connect(f'file:{RAIZ / DB}?mode=ro', uri=True)
    base = pd.read_sql('SELECT urbano, Dados_sig FROM setores_censitarios', con)
    con.close()
    D.add('A base é a do relatório parcial', [DB], cab=['Etapa', 'Setores'], colW=[5.0, 1.6], linhas=[
        ['Setores dos 70 municípios', intbr(len(base))],
        ['Com moradores e sem sigilo (Dados_sig = OK)', intbr((base['Dados_sig'] == 'OK').sum())],
        ['Urbanos — recorte de análise', intbr(len(df))]], explica=explica(
            oque='O funil que leva dos setores censitários dos 70 municípios ao recorte desta análise.',
            serve='Garante que todos os números partem da mesma base da seção VI do relatório parcial.',
            ler='Saem os setores sem moradores, os que o IBGE escondeu por sigilo e os rurais (o índice é intraurbano).',
            mostra=f'O recorte tem {intbr(len(df))} setores urbanos.'))
    D.add('Os 12 indicadores', [DB], cab=['Código', 'Indicador', 'Dimensão', 'No IVS', 'Setores'],
          colW=[0.8, 2.9, 1.5, 0.8, 1.1],
          linhas=[[c, NOME[c], DIM[c], 'sim' if c in fm.NUCLEO else 'não', intbr(df[coluna(c)].notna().sum())] for c in cods12],
          explica=explica(
              oque='Os 12 indicadores do Quadro 2 do relatório: os 7 do IVS de 2012 e 5 complementares.',
              serve='O código de três letras identifica o indicador em todos os slides e nas 12 apresentações próprias.',
              ler='"No IVS" = compõe o IVS de 2012 (Quadro 1). "Setores" = setores com o dado; a diferença para o recorte é '
                  'sigilo do IBGE.'))
    aucr = esp.loc[esp['eixo'] == 'referencia'].iloc[0]
    D.add('O que as análises anteriores ensinaram', ['docs/prompts/prompt_fatorial_multiversao_2026-10.md, seção 1.3',
                                                     mv('camada2_especificacoes.csv')], blocos=[
        ['Grades grandes não decidem.', 'As grades de 324 e de 108 versões geraram material, não escolha. Aqui cada análise '
                                        'responde a uma das 5 perguntas, e a apresentação termina nas decisões.'],
        ['A estabilidade não escolhe.', 'Pesos fixos têm variação zero por construção; a estabilidade é reportada, nunca '
                                        'usada para ordenar.'],
        ['A AUC contra favela não valida pesos.', f"No IVS proposto, a AUC é {br(aucr['auc_fcu'], 3)}; a renda sozinha dá "
                                                  f"{br(aucr['auc_renda_sozinha'], 3)}. Ela aparece só como descrição."],
        ['A incerteza é por município.', 'Deixar um município de fora e comparar metades de municípios, não reamostrar setores.'],
        ['Perder setores é decisão.', 'Cada versão informa quantos setores perde e quem são eles.']])

    # 2. exploratória dos 12
    D.secao('A análise exploratória dos 12', 'Os 12 indicadores lado a lado, antes da fatorial. A exploração completa de '
                                             'cada um está na apresentação própria dele.')
    linhas = []
    for c in cods12:
        q = desc(df[coluna(c)])
        linhas.append([NOME[c], fmt(c, q['media']), fmt(c, q['mediana']), fmt(c, q['p75']), br(q['assim'], 2),
                       ev.pctbr(q['pct_zeros'])])
    D.add('Painel descritivo dos 12', [DB], cab=['Indicador', 'Média', 'Mediana', 'p75', 'Assim.', '% zeros'],
          colW=[2.5, 1.2, 1.2, 1.2, 0.7, 0.8], linhas=linhas, explica=explica(
              oque='Média, mediana, percentil 75, assimetria e % de setores com zero de cada indicador.',
              serve='Mostra de uma vez quais indicadores se concentram em poucos setores — o que pesa na padronização antes '
                    'do índice.',
              ler='Assimetria acima de 1 e muitos zeros: poucos setores concentram o problema. Proporções de 0 a 1; renda '
                  'em reais; razão de moradores em moradores por domicílio.',
              mostra='É a Tabela 1 do relatório parcial, com os 12 indicadores.'))
    fig, axs = plt.subplots(3, 4, figsize=(11, 7), facecolor=SURF)
    for ax, c in zip(axs.flat, cods12):
        ax.hist(df[coluna(c)].dropna(), bins=40, color=PETROL)
        ax.set_title(NOME[c], fontsize=8)
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(3))
        estilo(ax)
        ax.tick_params(labelsize=6)
    fig.tight_layout()
    D.add('As 12 distribuições', [DB], figura=salvar(fig, 'FIN_eda_histogramas.png'),
          legenda='Histograma de cada indicador nos setores urbanos dos 70 municípios.', explica=explica(
              oque='Um histograma por indicador: quantos setores caem em cada faixa de valor.',
              serve='Compara a forma das distribuições lado a lado, antes de pôr todas na mesma régua do índice.',
              ler='Cada painel tem a sua escala. Barra alta no começo e cauda à direita: muitos setores com valor baixo e '
                  'poucos com valor alto. Distribuição em sino: valores espalhados em torno do meio.'))
    zeros = pd.Series({c: (df[coluna(c)].dropna() == 0).mean() for c in cods12})
    falt = pd.Series({c: df[coluna(c)].isna().mean() for c in cods12})
    fig, ax = plt.subplots(figsize=(7.2, 4.4), facecolor=SURF)
    y = np.arange(12)
    ax.barh(y - .2, 100 * zeros, .4, color=PETROL, label='% de setores com zero')
    ax.barh(y + .2, 100 * falt, .4, color=CLAY, label='% de setores sem o dado')
    ax.set_yticks(y)
    ax.set_yticklabels([NOME[c] for c in cods12], fontsize=7)
    ax.invert_yaxis()
    ax.legend(fontsize=7, frameon=False)
    estilo(ax, '% dos setores')
    D.add('Zeros e dados faltantes', [DB], figura=salvar(fig, 'FIN_eda_zeros_faltantes.png'),
          legenda='Proporção de setores com valor zero e sem o dado, por indicador.', explica=explica(
              oque='Para cada indicador, quantos setores têm valor zero (verde) e quantos não têm o dado (vermelho).',
              serve='São os dois problemas que o relatório parcial apontou antes do índice: zeros demais distorcem a régua '
                    'de 0 a 1; dado faltante por sigilo não é aleatório.',
              ler='Barra verde longa: o indicador é zero na maioria dos setores. Barra vermelha: setores perdidos se o '
                  'indicador entrar no índice.',
              mostra=f'Mais zeros: {NOME[zeros.idxmax()]} ({pct(zeros.max())}). Mais faltantes: {NOME[falt.idxmax()]} '
                     f'({pct(falt.max())}).'))
    reg = pd.DataFrame({c: df.groupby('regiao')[coluna(c)].mean() / df[coluna(c)].mean() for c in cods12}).reindex(REGIOES).T
    rmax = reg.max(axis=1)
    D.add('Os 12 por região', [DB], figura=mapa_calor(reg, 'FIN_eda_regiao.png', 0, 2, 'PuOr_r'),
          legenda='Média de cada indicador em cada região dividida pela média dos 70 municípios (1 = igual à média).',
          explica=explica(
              oque='Cada célula é a média do indicador na região dividida pela média geral.',
              serve='Põe na mesma escala indicadores com unidades diferentes e mostra quais têm padrão regional forte.',
              ler='1 = igual à média dos 70 municípios; 2 = o dobro; 0,5 = a metade. Laranja: acima da média; roxo: abaixo.',
              mostra=f'Maior contraste: {NOME[rmax.idxmax()]} no {reg.loc[rmax.idxmax()].idxmax()} '
                     f'({br(rmax.max(), 1)} vezes a média).'))
    fig, axs = plt.subplots(3, 4, figsize=(11, 7), facecolor=SURF)
    for ax, c in zip(axs.flat, cods12):
        cur = df.groupby('decil_ppi' if c == 'REN' else 'decil_renda')[coluna(c)].mean()
        ax.plot(cur.index, cur.to_numpy(), 'o-', color=PETROL, ms=2.5)
        ax.set_title(NOME[c] + (' (por decil de cor/raça)' if c == 'REN' else ''), fontsize=7.5)
        estilo(ax)
        ax.tick_params(labelsize=6)
    fig.tight_layout()
    D.add('O gradiente de renda dos 12', [DB], figura=salvar(fig, 'FIN_eda_gradiente.png'),
          legenda='Média de cada indicador por decil de renda do setor no município (1 = mais pobre); a renda, por decil de '
                  'cor/raça.', explica=explica(
              oque='Os setores de cada município divididos em 10 grupos pela renda; cada painel mostra a média do indicador '
                   'em cada grupo.',
              serve='Mostra quais indicadores seguem o gradiente social dentro das cidades — candidatos naturais à dimensão '
                    'socioeconômica — e quais não seguem.',
              ler='Linha que desce da esquerda para a direita: o indicador é pior nos setores mais pobres. Linha plana: '
                  'independe da renda.'))

    # 3. matrizes
    D.secao('As matrizes', 'Correlação no conjunto e dentro dos municípios, anti-imagem e adequação.')
    Rg = pd.read_csv(MV / 'camada1_12_global_correlacao.csv', index_col=0)
    Rm = pd.read_csv(MV / 'camada1_12_municipal_correlacao.csv', index_col=0)
    ag = pd.read_csv(MV / 'camada1_12_global_adequacao.csv').iloc[0]
    am = pd.read_csv(MV / 'camada1_12_municipal_adequacao.csv').iloc[0]
    par = lambda R: max(((a, b) for a in R.index for b in R.columns if a < b), key=lambda p: abs(R.at[p]))  # noqa: E731
    ler_mapa = ('Cada célula é a correlação entre o indicador da linha e o da coluna, de −1 a 1. Vermelho forte: andam '
                'juntos; azul: andam em sentidos opostos; branco: sem relação. A diagonal é sempre 1. A renda entra '
                'invertida, para que "mais" seja sempre "mais vulnerável".')
    pg, pm = par(Rg), par(Rm)
    D.add('Correlação no conjunto dos setores', [mv('camada1_12_global_correlacao.csv')],
          figura=mapa_calor(Rg, 'FIN_correlacao_global.png'),
          legenda=f"Spearman entre os 12 indicadores, {intbr(ag['n'])} setores com todos os dados.", explica=explica(
              oque='A matriz de correlação de Spearman entre os 12 indicadores, comparando todos os setores dos 70 '
                   'municípios.',
              serve='É a matéria-prima da análise fatorial: a fatorial procura grupos de indicadores muito correlacionados '
                    'entre si (os fatores).', ler=ler_mapa,
              mostra=f'O par mais forte é {NOME[pg[0]]} × {NOME[pg[1]]} ({br(Rg.at[pg], 2)}).'))
    D.add('Correlação dentro dos municípios', [mv('camada1_12_municipal_correlacao.csv')],
          figura=mapa_calor(Rm, 'FIN_correlacao_municipal.png'),
          legenda='Correlação entre as posições (postos) de cada setor dentro do próprio município.', explica=explica(
              oque='A mesma matriz, mas cada setor é comparado só com os setores da própria cidade (posição de 0 a 1 '
                   'dentro do município).',
              serve='O IVS é intraurbano. Esta matriz mostra a estrutura que sobra quando se tiram as diferenças entre '
                    'cidades — a que importa para achar desigualdade dentro delas.', ler=ler_mapa,
              mostra=f'O par mais forte é {NOME[pm[0]]} × {NOME[pm[1]]} ({br(Rm.at[pm], 2)}).'))
    dif = Rm - Rg
    pares = sorted(((a, b) for a in dif.index for b in dif.columns if a < b), key=lambda p: -abs(dif.at[p]))[:10]
    fr_dif = (f'A maior mudança é em {NOME[pares[0][0]]} × {NOME[pares[0][1]]}: de {br(Rg.at[pares[0]], 2)} para '
              f'{br(Rm.at[pares[0]], 2)}.')
    fontes_r = [mv('camada1_12_global_correlacao.csv'), mv('camada1_12_municipal_correlacao.csv')]
    D.add('O que muda ao comparar dentro da cidade: o mapa', fontes_r,
          figura=mapa_calor(dif, 'FIN_correlacao_diferenca.png', -.5, .5),
          legenda='Diferença: correlação dentro dos municípios menos correlação no conjunto.', explica=explica(
              oque='A diferença entre as duas matrizes anteriores, célula a célula.',
              serve='Mostra quais relações vinham de diferenças entre cidades (somem dentro delas) e quais existem também '
                    'dentro das cidades.',
              ler='Azul: a relação enfraquece dentro das cidades — parte dela era diferença entre cidades. Vermelho: fica '
                  'mais forte dentro delas. Branco: não muda.', mostra=fr_dif))
    D.add('O que muda ao comparar dentro da cidade: os pares', fontes_r,
          cab=['Par', 'No conjunto', 'Dentro', 'Diferença'], colW=[3.6, 1.2, 1.1, 1.1],
          linhas=[[f'{NOME[a]} × {NOME[b]}', br(Rg.at[a, b], 2), br(Rm.at[a, b], 2), br(dif.at[a, b], 2)] for a, b in pares],
          explica=explica(oque='Os 10 pares de indicadores cuja correlação mais muda entre as duas réguas.',
                          serve='Aponta onde a escolha da régua (no conjunto ou dentro do município) mais pesa.',
                          ler='Diferença negativa: a relação era, em boa parte, diferença entre cidades.', mostra=fr_dif))
    cab, lin = matriz_linhas(Rg)
    D.add('Tabela: correlação no conjunto', [mv('camada1_12_global_correlacao.csv')], cab=cab, linhas=lin, matriz=True)
    Ag = pd.read_csv(MV / 'camada1_12_global_antiimagem.csv', index_col=0)
    dg = np.diag(Ag.to_numpy())
    D.add('Matriz anti-imagem e o MSA de cada indicador', [mv('camada1_12_global_antiimagem.csv')],
          figura=mapa_calor(Ag, 'FIN_antiimagem.png'), legenda='Fora da diagonal, correlações parciais com sinal trocado; na '
                                                                 'diagonal, o MSA.',
          explica=explica(
              oque='Fora da diagonal, a correlação entre dois indicadores depois de descontar o efeito de todos os outros '
                   '(correlação parcial). Na diagonal, o MSA de cada indicador.',
              serve='Numa boa fatorial, o que dois indicadores têm em comum vem dos fatores, então as parciais devem ser '
                    'pequenas. O MSA resume isso por indicador.',
              ler=f'Fora da diagonal: quanto mais branco, melhor. Na diagonal: MSA de 0 a 1; abaixo de {br(fm.CRIT["msa"], 2)} '
                  'o indicador não combina com os outros.',
              mostra=f'MSA de {br(dg.min(), 2)} ({NOME[Ag.index[dg.argmin()]]}) a {br(dg.max(), 2)} ({NOME[Ag.index[dg.argmax()]]}).'))
    adq = []
    for nome_c, a in (('12, no conjunto', ag), ('12, dentro dos municípios', am),
                      ('núcleo (7), no conjunto', pd.read_csv(MV / 'camada1_nucleo_global_adequacao.csv').iloc[0]),
                      ('núcleo (7), dentro', pd.read_csv(MV / 'camada1_nucleo_municipal_adequacao.csv').iloc[0])):
        adq.append([nome_c, intbr(a['n']), br(a['kmo'], 3), intbr(a['bartlett_qui2']), br(a['det_R'], 5),
                    intbr(a['kaiser']), intbr(a['horn'])])
    D.add('Adequação da matriz: KMO, Bartlett e determinante', [mv('camada1_12_global_adequacao.csv'), mv('camada1_nucleo_global_adequacao.csv')],
          cab=['Conjunto', 'Setores', 'KMO', 'Bartlett', 'Determ.', 'Kaiser', 'Horn'],
          colW=[2.2, 0.9, 0.7, 1.0, 1.0, 0.7, 0.7], linhas=adq, explica=explica(
              oque='Três testes de se a matriz serve para uma análise fatorial, e duas regras para o número de fatores.',
              serve='KMO: quanto da correlação é compartilhada (0 a 1). Bartlett: testa se a matriz difere de "nenhuma '
                    'correlação". Determinante perto de zero: indicadores redundantes. Kaiser e Horn: quantos fatores reter.',
              ler=f'KMO acima de {br(fm.CRIT["kmo"], 2)} é adequado. Com dezenas de milhares de setores o Bartlett sempre '
                  'rejeita, então pouco informa. Kaiser conta autovalores acima de 1; Horn, os acima do esperado em dados '
                  'aleatórios.',
              mostra=f"KMO dos 12 no conjunto: {br(ag['kmo'], 3)}; dentro dos municípios: {br(am['kmo'], 3)}."))

    # 4. quantos fatores
    D.secao('Quantos fatores', 'Autovalores, scree plot, Kaiser e a análise paralela de Horn.')
    for nome_c, rot_c in (('12', 'os 12 indicadores'), ('nucleo', 'o núcleo (os 7 do Quadro 1)')):
        fig, ax = plt.subplots(1, 2, figsize=(10, 3.9), facecolor=SURF)
        for k, regua in enumerate(fm.REGUAS):
            a = pd.read_csv(MV / f'camada1_{nome_c}_{regua}_autovalores.csv')
            ax[k].plot(a.componente, a.autovalor, 'o-', color=PETROL, label='observado')
            ax[k].plot(a.componente, a.horn, 's--', color=CLAY, ms=3, label='Horn (dados aleatórios)')
            ax[k].axhline(1, color=CINZA, lw=.6)
            ax[k].set_title('no conjunto' if regua == 'global' else 'dentro dos municípios', fontsize=9)
            ax[k].legend(fontsize=7, frameon=False)
            estilo(ax[k], 'componente', 'autovalor')
        hg = pd.read_csv(MV / f'camada1_{nome_c}_global_adequacao.csv').iloc[0]['horn']
        hm = pd.read_csv(MV / f'camada1_{nome_c}_municipal_adequacao.csv').iloc[0]['horn']
        D.add(f'Autovalores: {rot_c}', [mv(f'camada1_{nome_c}_global_autovalores.csv'), mv(f'camada1_{nome_c}_municipal_autovalores.csv')],
              figura=salvar(fig, f'FIN_scree_{nome_c}.png'),
              legenda='Autovalores observados (verde) e médios de dados aleatórios (vermelho); linha cinza em 1.', explica=explica(
                  oque='O scree plot: cada ponto é um componente, e a altura (autovalor) diz quanta variação ele resume.',
                  serve='Decide quantos fatores a análise deve ter. Poucos fatores resumem muitos indicadores; fatores demais '
                        'só reproduzem ruído.',
                  ler='Kaiser: retém os pontos acima da linha 1. Horn: retém os pontos verdes acima da linha vermelha — o '
                      'que dados sem estrutura nenhuma produziriam. O "cotovelo" da curva também sugere o número.',
                  mostra=f'Horn retém {intbr(hg)} fatores no conjunto e {intbr(hm)} dentro dos municípios.'))
    t = sub.groupby(['regua', 'horn']).size().unstack(0).fillna(0)
    D.add('Quantos fatores as 4.017 combinações pedem', [mv('camada1_subconjuntos.csv')],
          cab=['Fatores (Horn)', 'No conjunto', 'Dentro dos municípios'], colW=[2.0, 1.8, 2.4],
          linhas=[[intbr(h), intbr(r.get('global', 0)), intbr(r.get('municipal', 0))] for h, r in t.iterrows()],
          explica=explica(oque='Em quantas combinações de indicadores o critério de Horn indica 1, 2 ou 3 fatores.',
                          serve='Diz se a estrutura em duas dimensões (saneamento e socioeconômica), herdada do IVS de 2012, '
                                'aparece nos dados ou é imposta.',
                          ler='Cada linha é um número de fatores; as colunas contam combinações.',
                          mostra=f"Dois fatores em {pct((sub['horn'] == 2).mean())} das combinações (duas réguas somadas)."))

    # 5. a explosão
    D.secao('As 4.017 combinações', 'Todas as combinações de 3 ou mais dos 12 indicadores, cada uma com uma fatorial.')
    el = sub.groupby('regua')['elegivel'].mean()
    D.add('Como as 4.017 combinações foram rodadas', [mv('camada1_subconjuntos.csv')], blocos=[
        ['O pedido.', 'Versões com e sem cada um dos 12 indicadores: todas as combinações de 3 a 12 deles.'],
        ['O quê.', f"{intbr(sub['codigos'].nunique())} combinações, cada uma em duas réguas: posição do setor no conjunto e "
                   f"dentro do município ({intbr(len(sub))} fatoriais)."],
        ['Como.', 'Eixo principal, 2 fatores, rotação promax; cada combinação nos setores que têm todos os indicadores dela.'],
        ['Critério.', f"Elegível com KMO ≥ {br(fm.CRIT['kmo'], 2)}, MSA ≥ {br(fm.CRIT['msa'], 2)}, comunalidade ≥ "
                      f"{br(fm.CRIT['h2'], 2)} e carga ≥ {br(fm.CRIT['carga'], 2)}, fixado antes de rodar."],
        ['Resultado.', f"Elegíveis: {pct(el.get('global', np.nan))} no conjunto e {pct(el.get('municipal', np.nan))} dentro "
                       'dos municípios.'],
        ['Como resumir 4.017.', 'Em vez de ler combinação por combinação, comparam-se os pares que só diferem por um '
                                'indicador: isso isola o efeito de cada um (próximos slides).']])
    for regua, rot_r in (('global', 'no conjunto'), ('municipal', 'dentro dos municípios')):
        e = ef[ef['regua'] == regua].sort_values('derruba_elegibilidade', ascending=False)
        D.add(f'O efeito de cada indicador, {rot_r}', [mv('camada1_efeito_variavel.csv')],
              cab=['Indicador', 'Δ KMO', 'Setores perdidos', 'Derruba', 'h² mediana'], colW=[2.6, 0.9, 1.4, 1.0, 1.2],
              linhas=[[NOME[r.codigo], br(r.delta_kmo_mediana, 3), intbr(-r.delta_n_mediana), pct(r.derruba_elegibilidade),
                       br(r.h2_mediana, 3)] for r in e.itertuples()], explica=explica(
                  oque='Para cada indicador, o que muda quando ele entra numa combinação (mediana sobre os pares).',
                  serve='Resume as 4.017 combinações numa linha por indicador: quem melhora a fatorial, quem custa setores e '
                        'quem a faz deixar de passar nos critérios.',
                  ler='Δ KMO positivo: melhora a adequação. "Derruba": % dos pares em que a combinação passava sem ele e '
                      'deixa de passar com ele. h²: comunalidade mediana dele.',
                  mostra=f'O que mais derruba a elegibilidade é {NOME[e.codigo.iloc[0]]} ({pct(e.derruba_elegibilidade.iloc[0])} '
                         'dos pares).'))
    fig, ax = plt.subplots(figsize=(7.2, 4.4), facecolor=SURF)
    w_ = ef.pivot(index='codigo', columns='regua', values='h2_mediana').reindex(cods12)
    x = np.arange(12)
    ax.bar(x - .2, w_['global'], .4, color=PETROL, label='no conjunto')
    ax.bar(x + .2, w_['municipal'], .4, color=CLAY, label='dentro dos municípios')
    ax.axhline(fm.CRIT['h2'], color=TINTA, lw=.8, ls='--')
    ax.set_xticks(x)
    ax.set_xticklabels([NOME[c] for c in cods12], rotation=40, ha='right', fontsize=6.5)
    ax.legend(fontsize=7, frameon=False)
    estilo(ax, '', 'comunalidade mediana')
    abaixo = [NOME[c] for c in cods12 if w_.at[c, 'municipal'] < fm.CRIT['h2']]
    D.add('A comunalidade de cada indicador nas combinações', [mv('camada1_efeito_variavel.csv')],
          figura=salvar(fig, 'FIN_efeito_h2.png'),
          legenda=f'Comunalidade mediana de cada indicador nas combinações em que entra; tracejado: critério {br(fm.CRIT["h2"], 2)}.',
          explica=explica(
              oque='A comunalidade típica de cada indicador: a parte da variação dele que os fatores explicam.',
              serve='É o critério que mais elimina combinações. Indicador com comunalidade baixa não compartilha muito com os '
                    'outros: ou mede outra coisa, ou é ruído.',
              ler='Barras acima do tracejado passam no critério. Verde: no conjunto; vermelho: dentro dos municípios.',
              mostra=('Abaixo do critério dentro dos municípios: ' + ', '.join(abaixo) + '.') if abaixo else
              'Todos acima do critério dentro dos municípios.'))
    t = sub.groupby(['p', 'regua'])['elegivel'].mean().unstack()
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    ax.plot(t.index, 100 * t['global'], 'o-', color=PETROL, label='no conjunto')
    ax.plot(t.index, 100 * t['municipal'], 's-', color=CLAY, label='dentro dos municípios')
    ax.legend(fontsize=8, frameon=False)
    estilo(ax, 'número de indicadores na combinação', '% de combinações elegíveis')
    D.add('Elegibilidade pelo número de indicadores', [mv('camada1_subconjuntos.csv')],
          figura=salvar(fig, 'FIN_elegibilidade_p.png'), legenda='Proporção de combinações elegíveis por tamanho.',
          explica=explica(oque='A proporção de combinações que passa nos critérios, para cada número de indicadores.',
                          serve='Mostra se é mais fácil ter uma fatorial adequada com poucos ou com muitos indicadores.',
                          ler='Curva que cai para a direita: quanto mais indicadores, mais chance de entrar um que não combina '
                              'com os outros.',
                          mostra=f"Com 3 indicadores, {pct(t['global'].iloc[0])} elegíveis no conjunto; com 12, "
                                 f"{pct(t['global'].iloc[-1])}."))
    top = sub[(sub.regua == 'municipal') & sub.elegivel].sort_values('kmo', ascending=False).head(10)
    D.add('As combinações elegíveis de maior KMO (dentro dos municípios)', [mv('camada1_subconjuntos.csv')],
          cab=['Indicadores', 'Setores', 'KMO', 'h² mínima'], colW=[3.6, 1.1, 0.8, 1.7],
          linhas=[[r.codigos.replace('+', ' · '), intbr(r.n), br(r.kmo, 3), f'{br(r.h2_min, 3)} ({r.h2_min_var})']
                  for r in top.itertuples()], explica=explica(
              oque='As 10 combinações elegíveis com a maior adequação (KMO), comparando dentro dos municípios.',
              serve='Mostra quais conjuntos de indicadores formam a estrutura mais limpa — informação para a decisão P2.',
              ler='Os códigos de três letras estão no slide "Os 12 indicadores". h² mínima: a menor comunalidade e de quem é.',
              mostra='Lista descritiva, não escolha: KMO alto não diz se o conjunto é o certo para o índice.'))

    # 6. os métodos
    D.secao('Os métodos', 'Rotação × peso, normalização, sigilo e conjunto: o que muda o IVS e o que não muda.')
    rot_eixo = {'conjunto': 'Conjunto de indicadores (núcleo ± 1)', 'rotacao_peso': 'Rotação e método de peso',
                'normalizacao': 'Normalização (régua)', 'sigilo': 'Sigilo do analfabetismo'}
    D.add('Como os métodos foram comparados', [mv('camada2_especificacoes.csv')], blocos=[
        ['A referência.', 'O IVS proposto: os 7 do Quadro 1, rotação promax, pesos 60/40, régua municipal, analfabetismo '
                          'sigiloso deixado ausente.'],
        ['Um eixo por vez.', 'Cada alternativa muda só uma dessas escolhas e é comparada com a referência, nos setores que as '
                             'duas têm.'],
        ['Duas medidas.', 'A correlação de Spearman dentro de cada município (a ordem dos setores muda?) e a % de setores que '
                          'trocam de faixa de vulnerabilidade (o resultado prático muda?).'],
        ['A regra, fixada antes.', f'Equivalente = Spearman ≥ {br(fm.EQUIV["spearman"], 2)} e menos de '
                                   f'{pct(fm.EQUIV["troca"], 0)} de troca. Se todas as alternativas de um eixo forem '
                                   'equivalentes, a escolha "tanto faz"; senão, é decisão da orientadora.'],
        ['Total.', f'{intbr(len(esp))} especificações: 13 conjuntos × 9 métodos de rotação e peso × 3 normalizações, mais o '
                   'eixo do sigilo.']])
    D.add('O veredito de cada eixo', [mv('camada2_efeito_eixo.csv')],
          cab=['Eixo', 'Alternativas', 'Equivalentes', 'Veredito', 'Maior troca'], colW=[2.6, 1.0, 1.0, 1.5, 1.1],
          linhas=[[rot_eixo[e], intbr(r.alternativas), intbr(r.equivalentes),
                   'tanto faz' if r.veredito == 'equivalentes' else 'decisão necessária', pct(r.maior_troca_faixa)]
                  for e, r in eixos.iterrows()], explica=explica(
              oque='Para cada eixo de escolha, quantas alternativas dão o mesmo resultado que a referência.',
              serve='Separa as escolhas que mudam o IVS das que não mudam — as primeiras vão para a orientadora.',
              ler='"Maior troca": a % de setores que mudam de faixa na alternativa mais distante.',
              mostra=f"{intbr((eixos['veredito'] == 'equivalentes').sum())} de {len(eixos)} eixos dão \"tanto faz\"."))
    rotulo_esp = {'conjunto': lambda r: r.conjunto, 'rotacao_peso': lambda r: f'{r.rotacao} · {r.metodo}',
                  'normalizacao': lambda r: r.normalizacao, 'sigilo': lambda r: r.sigilo}
    ler_eixo = {'conjunto': '"nucleo-X": o núcleo sem o indicador X; "nucleo+X": com X a mais.',
                'rotacao_peso': '"ss": pesos pela soma dos quadrados das cargas (dos dados); "50_50" e "60_40": divisão fixa '
                                'entre as dimensões; "comunalidades": pela variação explicada de cada indicador.',
                'normalizacao': '"municipal": de 0 a 1 dentro de cada município; "global": de 0 a 1 nos 70 juntos; '
                                '"postos_municipal": posição do setor no município, o que trata zeros e assimetria.',
                'sigilo': '"piso": o setor sigiloso recebe o menor valor possível (um analfabeto); "zero": recebe zero.'}
    for e in ('conjunto', 'rotacao_peso', 'normalizacao', 'sigilo'):
        g = esp[esp['eixo'] == e].sort_values('troca_faixa')
        fr = (f'Contra o IVS proposto ({prop["id"]}). ' + ('Todas equivalentes.' if g['equivalente'].all() else
              f"{intbr((~g['equivalente']).sum())} de {len(g)} não equivalentes; a mais distante troca a faixa de "
              f"{pct(g['troca_faixa'].max())} dos setores."))
        D.add(f'Eixo: {rot_eixo[e].lower()} — a tabela', [mv('camada2_especificacoes.csv')],
              cab=['Alternativa', 'Setores', 'Spearman', 'Troca de faixa', 'Peso socioec.'], colW=[2.4, 1.1, 1.0, 1.3, 1.3],
              linhas=[[rotulo_esp[e](r), intbr(r.n), br(r.spearman_mun, 3), pct(r.troca_faixa), pct(r.peso_F1 / 100)]
                      for r in g.itertuples()], explica=explica(
                  oque=f'Cada alternativa do eixo "{rot_eixo[e].lower()}", comparada com o IVS proposto.',
                  serve='Mostra o custo de escolher diferente da referência neste eixo.', ler=ler_eixo[e], mostra=fr))
        fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
        y = np.arange(len(g))
        ax.barh(y, 100 * g['troca_faixa'], color=[PETROL if q_ else CLAY for q_ in g['equivalente']])
        ax.set_yticks(y)
        ax.set_yticklabels([rotulo_esp[e](r) for r in g.itertuples()], fontsize=7)
        ax.axvline(100 * fm.EQUIV['troca'], color=TINTA, lw=.8, ls='--')
        estilo(ax, '% de setores que trocam de faixa')
        D.add(f'Eixo: {rot_eixo[e].lower()} — o gráfico', [mv('camada2_especificacoes.csv')],
              figura=salvar(fig, f'FIN_eixo_{e}.png'), legenda='Verde: equivalente à referência; vermelho: não equivalente.',
              explica=explica(oque='A % de setores que trocam de faixa em cada alternativa do eixo.',
                              serve='Visualiza quais alternativas mudam o resultado prático do índice.',
                              ler=f'Tracejado: o limite de {pct(fm.EQUIV["troca"], 0)} da regra de equivalência. Barras '
                                  'vermelhas também podem falhar pela correlação, mesmo abaixo do tracejado.', mostra=fr))
    t = esp.groupby(['conjunto', 'normalizacao'])['elegivel'].sum().unstack()
    D.add('Quantas especificações são elegíveis', [mv('camada2_especificacoes.csv')],
          cab=['Conjunto', 'Municipal', 'Global', 'Postos'], colW=[2.4, 1.3, 1.3, 1.3],
          linhas=[[c, intbr(r.get('municipal', 0)), intbr(r.get('global', 0)), intbr(r.get('postos_municipal', 0))]
                  for c, r in t.iterrows()], explica=explica(
              oque='Quantas das especificações de cada conjunto passam nos critérios pré-registrados, por normalização.',
              serve='Mostra se existe alguma combinação de escolhas que satisfaz os critérios fixados antes de rodar.',
              ler='Cada célula conta especificações elegíveis (todas as rotações, pesos e políticas de sigilo daquele conjunto).',
              mostra=f"{intbr(esp['elegivel'].sum())} de {intbr(len(esp))} especificações são elegíveis."))

    # 7. a solução proposta
    D.secao('A solução proposta', 'As cinco escolhas padrão: híbrido, os 7 do Quadro 1, sigilo ausente, régua municipal, '
                                  'promax 60/40.')
    cods = prop['codigos'].split('+')
    cols = [fm.VARS[c] for c in cods]
    d = fm.com_sigilo(df, prop['sigilo']).dropna(subset=cols)
    X, metodo = fm.matriz_entrada(d, cols, prop['normalizacao'])
    r = rodar_cenario(X, metodo=metodo, com_horn=True, extracao=fm.EXTRACAO)
    D.add('A especificação proposta', [mv('camada3_finalistas.csv')], blocos=[
        ['Indicadores.', ', '.join(NOME[c] for c in cods) + '.'],
        ['Método.', f"Eixo principal, 2 fatores, rotação {prop['rotacao']}, pesos {prop['metodo'].replace('_', '/')}, "
                    f"normalização {prop['normalizacao']}, analfabetismo sigiloso {prop['sigilo']}."],
        ['Base.', f"{intbr(prop['n'])} setores ({pct(prop['pct_recorte'])} do recorte)."],
        ['Adequação.', f"KMO {br(prop['kmo'], 3)}; MSA mínimo {br(prop['msa_min'], 3)}; comunalidade mínima "
                       f"{br(prop['h2_min'], 3)}; {'elegível' if prop['elegivel'] else 'não elegível pelos critérios pré-registrados'}."],
        ['Por que é a proposta.', 'Não é a "melhor": é a combinação das escolhas padrão até a orientadora decidir. As '
                                  'alternativas e o custo de cada uma estão na parte 6.']])
    nomes = [NOME[c] for c in cods]
    for titulo, mats, oq in (
            ('Matriz de cargas: sem rotação e Varimax', (('Sem rot.', r['sem_rotacao']), ('Varimax', r['varimax'])),
             'As cargas antes da rotação e depois da rotação Varimax, que mantém os fatores independentes.'),
            ('Matriz de cargas: promax padrão e estrutura', (('Padrão', r['promax_padrao']), ('Estrutura', r['promax_estrutura'])),
             'As cargas da rotação promax, que deixa os fatores se correlacionarem. "Padrão": o efeito próprio do fator '
             '(coeficiente de regressão); "estrutura": a correlação entre indicador e fator.')):
        D.add(titulo, [mv('camada3_finalistas.csv')], cab=['Indicador'] + [f'{n} F{j + 1}' for n, _ in mats for j in range(2)],
              colW=[2.6, 1.15, 1.15, 1.15, 1.15],
              linhas=[[nomes[i]] + [br(M[i, j], 3) for _, M in mats for j in range(2)] for i in range(len(cods))],
              explica=explica(oque=oq, serve='As cargas definem a que dimensão cada indicador pertence e, por isso, como o '
                                             'peso da dimensão se reparte entre os indicadores.',
                              ler='Carga perto de 1: o indicador pertence ao fator. F1 é a dimensão em que a renda carrega '
                                  'mais (socioeconômica); F2, a outra (saneamento).'))
    P = r['promax_padrao']
    fig, ax = plt.subplots(figsize=(6.0, 4.4), facecolor=SURF)
    ax.imshow(P, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    ax.set_yticks(range(len(cods)))
    ax.set_yticklabels(nomes, fontsize=7)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['F1', 'F2'])
    for i in range(len(cods)):
        for j in range(2):
            ax.text(j, i, br(P[i, j], 2), ha='center', va='center', fontsize=7, color='white' if abs(P[i, j]) > .55 else TINTA)
    D.add('As cargas em mapa de calor', [mv('camada3_finalistas.csv')], figura=salvar(fig, 'FIN_cargas_mapa.png'),
          legenda='Cargas da matriz padrão da promax no IVS proposto.', explica=explica(
              oque='A matriz padrão da promax em cores.', serve='Mostra de relance a que fator cada indicador pertence.',
              ler='Vermelho forte numa coluna: o indicador pertence àquele fator. Células claras nas duas colunas: o '
                  'indicador não pertence bem a nenhum.'))
    D.add('Comunalidades, MSA e correlação entre fatores', [mv('camada3_finalistas.csv')],
          cab=['Indicador', 'Comunalidade', 'MSA'], colW=[3.0, 1.6, 1.2],
          linhas=[[nomes[i], br(r['comunalidade'][i], 3), br(r['msa'][i], 3)] for i in range(len(cods))], explica=explica(
              oque='A comunalidade e o MSA de cada indicador na solução proposta.',
              serve='Comunalidade baixa: o indicador fica quase fora da estrutura e recebe pouco peso. Φ (fi) é a correlação '
                    'entre os dois fatores.',
              ler=f'Critérios: comunalidade ≥ {br(fm.CRIT["h2"], 2)}, MSA ≥ {br(fm.CRIT["msa"], 2)}. Φ perto de 1 seria um '
                  'fator só; perto de 0, dois fatores independentes.',
              mostra=f"Φ = {br(r['phi'][0, 1], 3)}. Variância comum explicada pelos 2 fatores: {ev.pctbr(r['var_explicada_k'])}. "
                     f"Horn retém {intbr(r['horn_retidos'])}; Kaiser, {intbr(r['kaiser'])}."))
    fig, ax = plt.subplots(figsize=(7.2, 5.0), facecolor=SURF)
    ax.axhline(0, color=CINZA, lw=.6)
    ax.axvline(0, color=CINZA, lw=.6)
    ax.scatter(P[:, 0], P[:, 1], color=PETROL)
    for i, n_ in enumerate(nomes):
        ax.annotate(n_, (P[i, 0], P[i, 1]), fontsize=7, xytext=(4, 4), textcoords='offset points')
    estilo(ax, 'carga em F1 (socioeconômica)', 'carga em F2 (saneamento)')
    D.add('O plano fatorial', [mv('camada3_finalistas.csv')], figura=salvar(fig, 'FIN_plano_fatorial.png'),
          legenda='Cargas da matriz padrão da promax no IVS proposto.', explica=explica(
              oque='Cada ponto é um indicador, posicionado pelas cargas nos dois fatores.',
              serve='Mostra os grupos que a fatorial encontrou: indicadores próximos medem a mesma coisa.',
              ler='Perto do eixo horizontal e à direita: dimensão socioeconômica. Perto do eixo vertical e no alto: '
                  'saneamento. Perto da origem: o indicador quase não se explica pelos fatores.'))

    # 8. os pesos
    D.secao('Os pesos', 'Por dimensão e por indicador, a estabilidade por município e a replicação entre metades.')
    base_p = esp[(esp['conjunto'] == prop['conjunto']) & (esp['sigilo'] == prop['sigilo']) & (esp['normalizacao'] == prop['normalizacao'])]
    sel = lambda m: pct(base_p.loc[(base_p.rotacao == 'promax') & (base_p.metodo == m), 'peso_F1'].iloc[0] / 100)  # noqa: E731
    D.add('O peso da dimensão socioeconômica em cada método', [mv('camada2_especificacoes.csv')],
          cab=['Rotação', 'Método de peso', 'Peso socioeconômico'], colW=[2.0, 2.4, 2.2],
          linhas=[[x.rotacao, x.metodo, pct(x.peso_F1 / 100)] for x in base_p.itertuples()], explica=explica(
              oque='Quanto do índice vem da dimensão socioeconômica em cada forma de calcular os pesos.',
              serve='O IVS de 2012 usa 60% socioeconômica e 40% saneamento. Aqui se vê quanto os dados dariam.',
              ler='Métodos "ss" e "comunalidades" saem dos dados; "50_50" e "60_40" são fixos. Sem rotação há um fator só, '
                  'que leva tudo.',
              mostra=f'Pelos dados (promax, soma dos quadrados da padrão): {sel("ss_padrao")}; pela estrutura: '
                     f'{sel("ss_estrutura")}. A divisão entre as dimensões é decisão (P1), não resultado.'))
    pesos = pd.Series({c: prop[f'peso_{c}'] for c in cods})
    e = est[est['id'] == prop['id']]
    fr_peso = f'O maior peso é o de {NOME[pesos.abs().idxmax()]} ({pct(pesos.abs().max())}).'
    D.add('O peso de cada indicador: a tabela', [mv('camada3_finalistas.csv'), mv('camada3_estabilidade.csv')],
          cab=['Indicador', 'Peso', 'Menor sem 1 mun.', 'Maior'], colW=[2.8, 1.1, 1.6, 1.1],
          linhas=[[NOME[c], pct(abs(w)), pct(e[f'peso_{c}'].abs().min()), pct(e[f'peso_{c}'].abs().max())] for c, w in pesos.items()],
          explica=explica(
              oque='A fração do IVS proposto que vem de cada indicador, e o menor e o maior valor ao tirar um município.',
              serve='É o que define o índice: IVS = soma de cada indicador padronizado vezes o seu peso.',
              ler='Dentro de cada dimensão, o peso se reparte pelo quadrado das cargas: quem carrega mais pesa mais.',
              mostra=fr_peso))
    D.add('O peso de cada indicador: o gráfico', [mv('camada3_finalistas.csv')],
          figura=barras([NOME[c] for c in pesos.index], 100 * pesos.abs().to_numpy(), 'FIN_pesos.png', 'peso no índice (%)'),
          legenda='Pesos no IVS proposto.', explica=explica(
              oque='Os mesmos pesos em barras.', serve='Mostra quem domina o índice.',
              ler='Barras longas: indicadores que mais determinam a posição de um setor no IVS.', mostra=fr_peso))
    fig, ax = plt.subplots(figsize=(7.4, 4.2), facecolor=SURF)
    ax.boxplot([100 * e[f'peso_{c}'].abs() for c in cods], tick_labels=nomes, whis=WHIS, medianprops={'color': CLAY})
    ax.tick_params(axis='x', labelrotation=30)
    estilo(ax, '', 'peso (%) sem 1 município')
    D.add('A estabilidade: um município de fora por vez', [mv('camada3_estabilidade.csv')],
          figura=salvar(fig, 'FIN_estabilidade.png'), legenda=f'Peso de cada indicador nas {len(e)} rodadas, cada uma sem um município.',
          explica=explica(
              oque='Os pesos recalculados 70 vezes, cada vez sem um dos municípios.',
              serve='É a medida de incerteza adotada: os municípios são a unidade de replicação do ELSI. Reamostrar setores '
                    'subestimava a incerteza.',
              ler='Caixa estreita: peso estável. Pontos isolados: um município que, sozinho, muda o peso.',
              mostra=(f"O peso socioeconômico fica em {pct(prop['peso_F1_min'] / 100)} por construção (pesos fixos); "
                      if prop['amp_peso_F1'] == 0 else
                      f"O peso socioeconômico vai de {pct(prop['peso_F1_min'] / 100)} a {pct(prop['peso_F1_max'] / 100)}; ")
              + amplitude_texto(e, cods) + '.'))
    D.add('A replicação entre metades dos municípios', [mv('camada3_replicacao.csv')],
          cab=['Finalista', 'Papel', 'Tucker F1', 'Tucker F2'], colW=[1.1, 3.0, 1.2, 1.2],
          linhas=[[f['id'], f['papel'].replace('_', ' '), br(rep.at[f['id'], 'tucker_F1'], 3), br(rep.at[f['id'], 'tucker_F2'], 3)]
                  for _, f in fin.iterrows()], explica=explica(
              oque='Os municípios foram divididos em duas metades sorteadas dentro de cada região; a fatorial rodou em cada '
                   'metade e as cargas foram comparadas pelo coeficiente de Tucker.',
              serve='Testa se a estrutura é dos dados ou de um grupo de municípios: se as duas metades dão as mesmas cargas, '
                    'o resultado se replica.',
              ler='Tucker de 0,95 ou mais: fator replicado; de 0,85 a 0,94: parecido; abaixo: diferente.',
              mostra=f"Na proposta: {br(rep.at[prop['id'], 'tucker_F1'], 3)} (F1) e {br(rep.at[prop['id'], 'tucker_F2'], 3)} (F2)."))

    # 9. o IVS proposto
    D.secao('O IVS proposto', 'Calculado com as escolhas padrão. É proposta: a escolha final é da orientadora.')
    v = ivs.merge(df[['CD_SETOR', 'porte']], on='CD_SETOR')
    q = desc(v['ivs'])
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    ax.hist(v['ivs'].dropna(), bins=60, color=PETROL)
    estilo(ax, 'IVS proposto (0 a 1, régua do município)', 'setores')
    D.add('A distribuição do IVS proposto', [mv('ivs_proposto_por_setor.csv')], figura=salvar(fig, 'FIN_ivs_hist.png'),
          legenda='IVS proposto por setor.', explica=explica(
              oque='O histograma do IVS proposto: cada setor recebe um valor de 0 a 1.',
              serve='É o índice final. 0 = o setor menos vulnerável da sua cidade em todos os indicadores; 1 = o mais.',
              ler='Como a régua é de cada município, o valor diz onde o setor fica dentro da própria cidade.',
              mostra=f"{intbr(q['n'])} setores com IVS (média {br(q['media'], 3)}, mediana {br(q['mediana'], 3)}); "
                     f"{intbr(len(df) - q['n'])} ficam sem, por dado ausente num componente."))
    ok = v[v['faixa_ivs_bh'] >= 0].astype({'faixa_ivs_bh': int, 'faixa_quartis': int})
    g = ok.groupby('faixa_ivs_bh')
    t = pd.DataFrame({'setores': g.size(), 'pop': g['v0001'].sum(), 'p60': g['pop_60mais'].sum(),
                      'idoso': g['pct_idoso_60mais'].mean(), 'fcu': g['is_fcu'].mean()})
    ler_fx = ('Regra do IVS-BH 2012, dentro de cada município: médio = média ± 0,5 desvio-padrão; elevado até +1,5; '
              'acima, muito elevado; abaixo de −0,5, baixo.')
    D.add('As quatro faixas: setores e moradores', [mv('ivs_proposto_por_setor.csv')],
          cab=['Faixa', 'Setores', '% setores', 'Moradores', '% moradores'], colW=[1.6, 1.2, 1.1, 1.6, 1.3],
          linhas=[[FAIXAS[i], intbr(x.setores), pct(x.setores / t.setores.sum()), intbr(x['pop']), pct(x['pop'] / t['pop'].sum())]
                  for i, x in t.iterrows()], explica=explica(
              oque='Quantos setores e quantos moradores ficam em cada faixa de vulnerabilidade.',
              serve='As faixas são o produto que vai para os mapas e para a gestão: onde priorizar.', ler=ler_fx,
              mostra=f"{intbr(t['pop'].iloc[-2:].sum())} moradores em setores de faixa elevada ou muito elevada."))
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    ax.bar(FAIXAS, t['pop'] / 1e6, color=[CINZA, PETROL, OCRE, CLAY])
    estilo(ax, 'faixa do IVS proposto', 'moradores (milhões)')
    D.add('As quatro faixas: o gráfico', [mv('ivs_proposto_por_setor.csv')], figura=salvar(fig, 'FIN_faixas.png'),
          legenda='Moradores por faixa do IVS proposto.', explica=explica(
              oque='Os moradores de cada faixa, em milhões.', serve='Dá a dimensão da população em cada nível.', ler=ler_fx))
    ct = pd.crosstab(ok['faixa_ivs_bh'], ok['faixa_quartis'])
    D.add('Faixas pela regra do IVS-BH e por quartis', [mv('ivs_proposto_por_setor.csv')],
          cab=['IVS-BH \\ quartis'] + [FAIXAS[int(c)] if c >= 0 else 'indef.' for c in ct.columns],
          colW=[1.8] + [1.0] * len(ct.columns),
          linhas=[[FAIXAS[i]] + [intbr(x) for x in rr] for i, rr in ct.iterrows()], explica=explica(
              oque='O cruzamento das duas regras de faixa: a do IVS-BH (pelo desvio-padrão) e os quartis (25% dos setores de '
                   'cada município em cada faixa).',
              serve='Mostra o quanto a regra de corte muda a classificação — uma decisão a mais para a orientadora.',
              ler='Na diagonal, as duas regras concordam. "Indef.": municípios com menos de 4 setores, sem quartis.',
              mostra=f"As duas regras concordam em {pct((ok['faixa_ivs_bh'] == ok['faixa_quartis']).mean())} dos setores."))
    fr_ido = (f"{intbr(t.p60.iloc[-2:].sum())} idosos moram em setores de faixa elevada ou muito elevada "
              f"({pct(t.p60.iloc[-2:].sum() / t.p60.sum())} dos idosos com IVS).")
    D.add('Os idosos em cada faixa: a tabela', [mv('ivs_proposto_por_setor.csv')],
          cab=['Faixa', 'Pessoas 60+', '% dos idosos', '% idosos no setor'], colW=[1.6, 1.6, 1.5, 1.8],
          linhas=[[FAIXAS[i], intbr(x.p60), pct(x.p60 / t.p60.sum()), pct(x.idoso)] for i, x in t.iterrows()], explica=explica(
              oque='Quantas pessoas de 60 anos ou mais moram em cada faixa e a proporção média de idosos nos setores.',
              serve='É a pergunta do ELSI-Brasil: onde moram os idosos em relação à vulnerabilidade do território.',
              ler='"% dos idosos": distribuição dos idosos entre as faixas. "% idosos no setor": quanto da população dos '
                  'setores daquela faixa é idosa.', mostra=fr_ido))
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
    ax.bar(FAIXAS, 100 * t['idoso'], color=[CINZA, PETROL, OCRE, CLAY])
    estilo(ax, 'faixa do IVS proposto', '% de idosos no setor (média)')
    D.add('Os idosos em cada faixa: o gráfico', [mv('ivs_proposto_por_setor.csv')], figura=salvar(fig, 'FIN_idosos_faixa.png'),
          legenda='Proporção média de idosos nos setores de cada faixa.', explica=explica(
              oque='A proporção média de pessoas de 60 anos ou mais nos setores de cada faixa.',
              serve='Mostra se os setores mais vulneráveis são mais jovens ou mais envelhecidos.',
              ler='Barras que caem para a direita: os setores mais vulneráveis têm menos idosos proporcionalmente.',
              mostra=fr_ido))
    D.add('As favelas em cada faixa', [mv('ivs_proposto_por_setor.csv')],
          cab=['Faixa', 'Setores', '% de setores de favela'], colW=[1.8, 1.6, 2.4],
          linhas=[[FAIXAS[i], intbr(x.setores), pct(x.fcu)] for i, x in t.iterrows()], explica=explica(
              oque='A proporção de setores de favela e comunidade urbana em cada faixa.',
              serve='Checagem de bom senso: favela deveria se concentrar nas faixas mais altas.',
              ler='Descrição, não validação: o critério de favela do IBGE já incorpora moradia, então a relação é '
                  'parcialmente circular.',
              mostra=f"Na faixa muito elevada, {pct(t.fcu.iloc[-1])} dos setores são de favela; na baixa, {pct(t.fcu.iloc[0])}."))
    for por, rot_p, ordem in (('regiao', 'Por região', REGIOES), ('porte', 'Por porte do município', PORTES)):
        ct = pd.crosstab(ok[por], ok['faixa_ivs_bh'], normalize='index').reindex(ordem)
        fig, ax = plt.subplots(figsize=(7.2, 4.0), facecolor=SURF)
        esq = np.zeros(len(ct))
        for j, cor_ in enumerate([CINZA, PETROL, OCRE, CLAY]):
            ax.barh(ordem, 100 * ct[j], left=esq, color=cor_, label=FAIXAS[j])
            esq += 100 * ct[j].to_numpy()
        ax.invert_yaxis()
        ax.legend(fontsize=7, frameon=False, ncol=4, loc='lower center', bbox_to_anchor=(.5, 1.0))
        estilo(ax, '% dos setores')
        D.add(f'{rot_p}: a distribuição das faixas', [mv('ivs_proposto_por_setor.csv')],
              figura=salvar(fig, f'FIN_faixas_{por}.png'), legenda=f'Distribuição das faixas {rot_p.lower()}.',
              explica=explica(
                  oque='A parte dos setores em cada faixa, para cada grupo.',
                  serve='Mostra se algum grupo concentra setores nas faixas altas.',
                  ler='Com a régua do município, a faixa diz onde o setor fica dentro da própria cidade. Comparar grupos '
                      'descreve a forma das distribuições internas, não o nível de vulnerabilidade de cada região.',
                  mostra='% de setores em faixa muito elevada: ' + '; '.join(f'{i} {pct(x)}' for i, x in ct[3].items()) + '.'))
    m = ok.groupby('NM_MUN').agg(setores=('ivs', 'size'), elev=('faixa_ivs_bh', lambda x: (x >= 2).sum()),
                                 pop_elev=('v0001', lambda x: x[ok.loc[x.index, 'faixa_ivs_bh'] >= 2].sum()))
    m = m.sort_values('pop_elev', ascending=False)
    D.add('Os municípios com mais moradores em faixa elevada ou muito elevada', [mv('ivs_proposto_por_setor.csv')],
          cab=['Município', 'Setores', 'Setores elev.', 'Moradores'], colW=[2.6, 1.2, 1.4, 1.6],
          linhas=[[i, intbr(x.setores), intbr(x.elev), intbr(x.pop_elev)] for i, x in m.head(15).iterrows()], explica=explica(
              oque='Os 15 municípios com mais moradores em setores de faixa elevada ou muito elevada.',
              serve='Mostra onde está, em números absolutos, a população que o índice aponta como mais vulnerável.',
              ler='São contagens, não médias: a média de um índice padronizado por município não se compara entre cidades.'))
    D.add('Os finalistas lado a lado', [mv('camada3_finalistas.csv')],
          cab=['Id', 'Papel', 'Conjunto', 'Método', 'Régua', 'Troca'], colW=[0.8, 1.6, 1.3, 1.6, 1.4, 0.8],
          linhas=[[f.id, f.papel.replace('alternativa_', 'alt. ').replace('_', ' '), f.conjunto, f'{f.rotacao} {f.metodo}',
                   f.normalizacao, '—' if f.papel == 'proposta' else pct(f.troca_faixa)] for f in fin.itertuples()],
          explica=explica(oque='A proposta e, para cada eixo que muda o resultado, a alternativa de maior impacto.',
                          serve='São as especificações que a orientadora precisa ver para decidir.',
                          ler='"Troca": % de setores que mudam de faixa em relação à proposta.'))

    # 10. sensibilidade
    D.secao('Sensibilidade', 'Quanto o IVS muda com cada alternativa.')
    cols_ivs = ['ivs'] + [c for c in ivs.columns if c.startswith('ivs_E')]
    Rf = ivs[cols_ivs].rank().corr()
    rotf = {c: ('proposta' if c == 'ivs' else c.replace('ivs_', '')) for c in cols_ivs}
    D.add('Concordância entre os finalistas', [mv('ivs_proposto_por_setor.csv')],
          figura=mapa_calor(Rf, 'FIN_concordancia.png', 0, 1, 'Greens', rot=rotf),
          legenda='Spearman entre os IVS dos finalistas.', explica=explica(
              oque='A correlação de Spearman entre os IVS de cada par de finalistas.',
              serve='Mostra o quanto as alternativas ordenam os setores do mesmo jeito.',
              ler='1 = mesma ordem dos setores; quanto mais claro, mais as duas versões discordam.'))
    D.add('A AUC contra favela, como descrição', [mv('camada3_finalistas.csv')],
          cab=['Finalista', 'AUC índice', 'AUC renda', 'AUC no município'], colW=[1.4, 1.6, 1.6, 2.0],
          linhas=[[f.id, br(f.auc_fcu, 3), br(f.auc_renda_sozinha, 3), br(f.auc_fcu_mun, 3)] for f in fin.itertuples()],
          explica=explica(
              oque='A AUC mede o quanto o índice separa os setores de favela dos demais: 0,5 = acaso; 1 = separação perfeita.',
              serve='Era usada como validação nas versões anteriores. Fica aqui como descrição.',
              ler='Compare com a renda sozinha: se ela separa tão bem quanto o índice, a AUC mede o conteúdo socioeconômico, '
                  'não a qualidade dos pesos.'))
    pp = perf[perf['grupo'] == 'perdidos']
    D.add('Quem são os setores que cada finalista perde', [mv('camada3_perfil_perdidos.csv')],
          cab=['Finalista', 'Perdidos', '% recorte', 'Renda mediana', '% favela'], colW=[1.2, 1.3, 1.1, 1.8, 1.1],
          linhas=[[x.id, intbr(x.setores), pct(x.pct_recorte), fmt('REN', x.renda_mediana), pct(x.pct_fcu)] for x in pp.itertuples()],
          explica=explica(
              oque='Os setores do recorte que ficam sem IVS em cada finalista, por dado ausente num componente.',
              serve='Perder setores é decisão: se os perdidos são diferentes dos mantidos, o índice fica enviesado.',
              ler='Compare a renda mediana dos perdidos com a dos mantidos.',
              mostra=f"Nos setores mantidos pela proposta, a renda mediana é "
                     f"{fmt('REN', perf[(perf.grupo == 'mantidos') & (perf.id == prop['id'])].renda_mediana.iloc[0])}."))

    # 11. decisões
    D.secao('As decisões', 'As cinco perguntas para a orientadora, com o que os dados mostram.')
    ver = lambda e_: 'tanto faz' if eixos.at[e_, 'veredito'] == 'equivalentes' else f"muda: até {pct(eixos.at[e_, 'maior_troca_faixa'])} de troca de faixa"  # noqa: E731
    D.add('As cinco decisões', [mv('camada2_efeito_eixo.csv'), 'docs/prompts/estado_fatorial_multiversao_2026-10.md'],
          cab=['#', 'Pergunta', 'O que os dados mostram', 'Padrão'], colW=[0.5, 2.1, 3.0, 1.5], linhas=[
              ['P1', 'Reflexivo, formativo ou híbrido?', f"Φ entre os fatores = {br(r['phi'][0, 1], 2)} (1 seria um fator só); "
                                                       f"Horn retém {intbr(r['horn_retidos'])}", 'híbrido'],
              ['P2', 'Quais indicadores entram?', ver('conjunto'), 'os 7 do Quadro 1'],
              ['P3', 'Sigilo do analfabetismo?', ver('sigilo'), 'ausente'],
              ['P4', 'Que régua?', ver('normalizacao'), 'min-max municipal'],
              ['P5', 'Rotação e peso?', ver('rotacao_peso'), 'promax, 60/40']], explica=explica(
              oque='As cinco escolhas que definem o índice, o que a análise mostrou sobre cada uma e o padrão usado na proposta.',
              serve='É o que a orientadora precisa decidir. Com as escolhas dela, o motor recalcula o IVS.',
              ler='P1: se o IVS é um construto único (reflexivo), uma soma de facetas (formativo) ou um híbrido (a fatorial '
                  'pesa dentro de cada dimensão; a divisão entre dimensões é escolha).'))
    D.add('Limitações', ['relatorio_parcial_raic/Relatorio_Parcial_RAIC_2026_Pedro_corrigido.pdf'], blocos=[
        ['Estudo ecológico.', 'As relações são entre setores, não entre pessoas.'],
        ['Autocorrelação espacial.', 'Setores vizinhos não são independentes; o I de Moran fica para o geoprocessamento.'],
        ['Sigilo.', 'O ausente não é aleatório: cai nos setores de renda mais alta.'],
        ['Amostras diferentes.', 'Cada versão roda nos setores com todos os seus indicadores; as comparações usam a amostra comum.'],
        ['Validação externa.', 'Desfechos de saúde do ELSI-Brasil não estão no projeto; a AUC contra favela é só descrição.']])
    D.add('Próximos passos', ['docs/prompts/prompt_fatorial_multiversao_2026-10.md'], blocos=[
        ['1.', 'Levar as cinco decisões à orientadora.'],
        ['2.', 'Recalcular o IVS com as escolhas dela (o motor roda qualquer combinação).'],
        ['3.', 'Mapas temáticos no QGIS 3.x e I de Moran.'],
        ['4.', 'Redação do artigo e do relatório final.']])

    cab, lin = matriz_linhas(Rm)
    D.add('Apêndice: correlação dentro dos municípios', [mv('camada1_12_municipal_correlacao.csv')], cab=cab, linhas=lin, matriz=True)
    for regua, rot_r in (('global', 'no conjunto'), ('municipal', 'dentro dos municípios')):
        c = pd.read_csv(MV / f'camada1_12_{regua}_cargas.csv')
        D.add(f'Apêndice: cargas dos 12, {rot_r}', [mv(f'camada1_12_{regua}_cargas.csv')], matriz=True,
              cab=['Indicador', 'MSA', 'h²', 'Sem rot. F1', 'Sem rot. F2', 'Varimax F1', 'Varimax F2', 'Promax F1', 'Promax F2'],
              linhas=[[NOME[x.codigo], br(x.msa, 2), br(x.h2, 2), br(x.sem_rotacao_F1, 2), br(x.sem_rotacao_F2, 2),
                       br(x.varimax_F1, 2), br(x.varimax_F2, 2), br(x.promax_padrao_F1, 2), br(x.promax_padrao_F2, 2)]
                      for x in c.itertuples()])
    mm = ok.groupby('NM_MUN').agg(setores=('ivs', 'size'), media=('ivs', 'mean'),
                                  elev=('faixa_ivs_bh', lambda x: (x >= 2).mean())).reset_index()
    linhas = [[x.NM_MUN, intbr(x.setores), br(x.media, 3), pct(x.elev)] for x in mm.itertuples()]
    for k, parte in enumerate((linhas[:35], linhas[35:])):
        D.add(f'Apêndice: o IVS proposto nos 70 municípios ({k + 1} de 2)', [mv('ivs_proposto_por_setor.csv')],
              cab=['Município', 'Setores', 'IVS médio', '% elevado ou muito'], linhas=parte, duas=True)
    return D


def main() -> None:
    df, nac, ivs, fin = carregar()
    ef = pd.read_csv(MV / 'camada1_efeito_variavel.csv')
    est = pd.read_csv(MV / 'camada3_estabilidade.csv')
    sub = pd.read_csv(MV / 'camada1_subconjuntos.csv')
    for f in FIG.glob('*.png'):          # figuras de uma rodada anterior com outros nomes não podem sobrar
        f.unlink()
    xlsx = {}
    for cod in fm.VARS:
        D = deck_indicador(cod, df, nac, ivs, fin, ef, est, sub)
        D.gravar()
        xlsx.update(D.tabelas)
        print(f'{cod}: {len(D.ordem)} slides')
    D = montar_final(df, ivs, fin)
    D.gravar()
    xlsx.update(D.tabelas)
    print(f'FIN: {len(D.ordem)} slides')
    with pd.ExcelWriter(PASTA / 'Fatorial_Multiversao_numeros.xlsx') as w:
        for sid, t in xlsx.items():
            t.to_excel(w, sheet_name=sid[:31], index=False)


if __name__ == '__main__':
    main()
