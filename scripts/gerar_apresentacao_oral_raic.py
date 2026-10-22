"""Apresentação oral da RAIC 2026 sobre o template da Coordic.

Segue o roteiro (`relatorio_parcial_raic/ROTEIRO_APRESENTACAO_ORAL.md`): 11 slides de fala e
6 de reserva para a arguição. As falas do roteiro entram nas notas do apresentador — editar a
fala é editar o roteiro e rodar de novo. Um ponto que ainda dependa da orientadora pode sair com
marca-texto amarelo (`confirmar`). Inclui as edições que o Pedro fez à mão no _ENVIO em 19/10:
grupo NESPE, objetivo sem a marca de provisório, sem a linha da fatorial no slide 10 e sem a R7.

Números: os mesmos arquivos que alimentaram o relatório parcial (pecas.json, Tabela 1, T03, T04)
e, onde o relatório os escreveu à mão, a mesma constante com a linha de origem.

Uso:  ./.venv/bin/python scripts/gerar_apresentacao_oral_raic.py
Saída: relatorio_parcial_raic/Apresentacao_Oral_RAIC_2026_Pedro.pptx (com as falas nas notas),
       ..._ENVIO.pptx (sem notas, para o envio) e figuras/oral_*.png
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Cm, Pt

from pecas_relatorio_raic import br  # mesmo arredondamento (NBR 5891) do relatório

RAIZ = Path(__file__).resolve().parents[1]
PASTA = RAIZ / 'relatorio_parcial_raic'
DADOS = PASTA / 'dados'
FIGURAS = PASTA / 'figuras'
MODELO = PASTA / 'modelos' / 'APRESENTACAO_ORAL_Coordic.pptx'
ROTEIRO = PASTA / 'ROTEIRO_APRESENTACAO_ORAL.md'
SAIDA = PASTA / 'Apresentacao_Oral_RAIC_2026_Pedro.pptx'
SAIDA_ENVIO = PASTA / 'Apresentacao_Oral_RAIC_2026_Pedro_ENVIO.pptx'  # sem as notas, para a Coordic
TABELAS = RAIZ / 'analises_exploratorias' / '00_referencia' / 'tabelas'

PECAS = json.loads((DADOS / 'pecas.json').read_text(encoding='utf-8'))
R = PECAS['figura1']['R']
ROB = PECAS['robustez_figura1']


def ler_csv(caminho: Path, sep: str = ',') -> list[dict]:
    with open(caminho, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f, delimiter=sep))


T03 = {r['indicador']: r for r in ler_csv(TABELAS / 'T03_descritivas_global.csv')}
T04 = ler_csv(TABELAS / 'T04_descritivas_regiao.csv')
TAB1 = ler_csv(DADOS / 'tabela1_descritivas.csv')
MUNICIPIOS = ler_csv(RAIZ / 'dados' / 'municipios_elsi_brasil.csv', sep=';')
RURAL = ler_csv(RAIZ / 'banco_de_dados' / 'eda' / 'exclusao_rural_conferencia.csv', sep=';')
EXTREMO = next(r for r in ler_csv(RAIZ / 'banco_de_dados' / 'eda' / 'renda_outliers_rastreados.csv', sep=';')
               if r['CD_SETOR'] == '310620005650366')

# Escritos à mão no relatório (scripts/gerar_relatorio_raic.py:445): medianas recalculadas no .db
# na base sem o setor extremo.
RENDA_MEDIANA_COM_DADO, RENDA_MEDIANA_SIGILO = 2313.87, 6092.84
# Analfabetismo (scripts/gerar_relatorio_raic.py:444): média observada e a média com 1 analfabeto em cada
# setor suprimido — a real fica entre as duas.
MEDIA_ANALFAB_OBS, MEDIA_ANALFAB_MIN = 3.64, 3.14
N_ANALFAB = 87556
N_RECORTE = PECAS['setores_no_recorte']

# Paleta tirada do template (cabeçalho da Coordic).
TEAL, TEAL_CLARO, CORAL, LARANJA = '3B848E', '79BCC4', 'D8634E', 'E8813A'
LAVANDA, FUNDO, TEXTO, CINZA, CINZA_CLARO = 'E1D6E9', 'E9F4F4', '1F2A33', '6B7780', 'D9DEE1'
AMARELO = 'FFFF00'

# Calibri, como o template; o Office instala a fonte dentro do próprio app.
for pasta in ('/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts',
              '/Applications/Microsoft Outlook.app/Contents/Resources/DFonts'):
    for nome in ('Calibri.ttf', 'Calibrib.ttf'):
        if (Path(pasta) / nome).exists():
            font_manager.fontManager.addfont(str(Path(pasta) / nome))
FONTE_FIG = 'Calibri' if 'Calibri' in {f.name for f in font_manager.fontManager.ttflist} else 'Arial'
plt.rcParams.update({'font.family': FONTE_FIG, 'font.size': 15, 'axes.edgecolor': '#' + CINZA})


def cor(h: str) -> str:
    return '#' + h


# ---------------------------------------------------------------- figuras

def fig_zeros() -> Path:
    """Slide 6: % de setores sem nenhum domicílio registrado com o problema (T03, pct_zeros)."""
    itens = [('Água inadequada', 'pct_agua_inad'), ('Esgoto inadequado', 'pct_esgoto_inad'),
             ('Lixo inadequado', 'pct_lixo_inad')]
    fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=200)
    for i, (rotulo, col) in enumerate(reversed(itens)):
        z = float(T03[col]['pct_zeros'])
        ax.barh(i, z, color=cor(TEAL), height=0.62)
        ax.barh(i, 100 - z, left=z, color=cor(CINZA_CLARO), height=0.62)
        ax.text(z - 2, i, f'{br(z, 0)}%', va='center', ha='right', color='white', fontsize=30, weight='bold')
        ax.text(-2, i, rotulo, va='center', ha='right', fontsize=18, color=cor(TEXTO))
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, 2.9)
    ax.axis('off')
    ax.text(0, 2.62, 'setores sem nenhum domicílio registrado com o problema', color=cor(TEAL), fontsize=14,
            weight='bold')
    ax.text(100, 2.62, 'demais setores', color=cor(CINZA), fontsize=14, ha='right')
    fig.subplots_adjust(left=0.27, right=0.98, top=0.98, bottom=0.02)
    caminho = FIGURAS / 'oral_zeros_saneamento.png'
    fig.savefig(caminho, transparent=True)
    plt.close(fig)
    return caminho


def fig_sigilo() -> Path:
    """Slide 7: renda mediana do responsável onde o analfabetismo existe × onde está sob sigilo."""
    n_sig = N_RECORTE - N_ANALFAB
    rot = [f'Analfabetismo\ndisponível\n({br(N_ANALFAB, 0)} setores)',
           f'Analfabetismo\nsob sigilo\n({br(n_sig, 0)} setores)']
    val = [RENDA_MEDIANA_COM_DADO, RENDA_MEDIANA_SIGILO]
    fig, ax = plt.subplots(figsize=(7.2, 5.6), dpi=200)
    barras = ax.bar(rot, val, color=[cor(TEAL_CLARO), cor(CORAL)], width=0.58)
    for b, v in zip(barras, val):
        ax.text(b.get_x() + b.get_width() / 2, v + 120, f'R$ {br(v, 2)}', ha='center', va='bottom',
                fontsize=28, weight='bold', color=cor(TEXTO))
    ax.set_ylim(0, 7600)
    ax.set_yticks([])
    for lado in ('top', 'right', 'left'):
        ax.spines[lado].set_visible(False)
    ax.tick_params(axis='x', labelsize=16, length=0, pad=8)
    ax.set_title('Renda mediana do responsável no setor', fontsize=17, color=cor(CINZA), pad=14)
    fig.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.2)
    caminho = FIGURAS / 'oral_sigilo_analfabetismo.png'
    fig.savefig(caminho, transparent=True)
    plt.close(fig)
    return caminho


def fig_correlacoes() -> Path:
    """Slide 8: o bloco renda × cor/raça × analfabetismo e o lixo à parte (Figura 1, Spearman)."""
    renda, raca, analf, lixo = 'renda_media_sem_extremo', 'pct_raca_pretpardind', 'pct_analfab', 'pct_lixo_inad'
    pos = {renda: (0.0, 1.0), raca: (-0.95, -0.45), analf: (0.95, -0.45), lixo: (2.75, 0.25)}
    nome = {renda: 'Renda\n(invertida)', raca: 'Cor/raça\npreta, parda\nou indígena',
            analf: 'Analfabetismo', lixo: 'Lixo\ninadequado'}
    fig, ax = plt.subplots(figsize=(10.4, 5.6), dpi=200)
    for a, b in ((renda, raca), (renda, analf), (analf, raca)):
        r = R[a][b]
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.plot([x1, x2], [y1, y2], color=cor(TEAL), lw=4 + 14 * (r - 0.5), solid_capstyle='round', zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, br(r, 2), ha='center', va='center', fontsize=22, weight='bold',
                color=cor(TEXTO), bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none'), zorder=3)
    outros = ['pct_agua_inad', 'pct_esgoto_inad', 'razao_moradores', analf, renda, raca]
    rs = [R[lixo][o] for o in outros]
    for n, (x, y) in pos.items():
        isolado = n == lixo
        ax.scatter([x], [y], s=12500, color=cor(LAVANDA if isolado else TEAL_CLARO), zorder=2,
                   edgecolors=cor(CINZA if isolado else TEAL), linewidths=2, linestyle='--' if isolado else '-')
        ax.text(x, y, nome[n], ha='center', va='center', fontsize=14, weight='bold', color=cor(TEXTO), zorder=4)
    ax.text(pos[lixo][0], pos[lixo][1] - 0.78,
            f'com os outros 6 indicadores\ndo IVS: de {br(min(rs), 2)} a {br(max(rs), 2)}',
            ha='center', va='top', fontsize=14, color=cor(CINZA))
    ax.set_xlim(-1.7, 3.6)
    ax.set_ylim(-1.35, 1.55)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    caminho = FIGURAS / 'oral_correlacoes.png'
    fig.savefig(caminho, transparent=True)
    plt.close(fig)
    return caminho


# ---------------------------------------------------------------- pptx: utilidades

def rgb(h: str) -> RGBColor:
    return RGBColor.from_string(h)


def _marca_texto(run) -> None:
    """Marca-texto amarelo no run (a:highlight vem antes de a:latin no esquema do DrawingML)."""
    rpr = run._r.get_or_add_rPr()
    hl = rpr.makeelement(qn('a:highlight'), {})
    clr = hl.makeelement(qn('a:srgbClr'), {'val': AMARELO})
    hl.append(clr)
    latin = rpr.find(qn('a:latin'))
    if latin is not None:
        latin.addprevious(hl)
    else:
        rpr.append(hl)


def escrever(tf, paragrafos, tamanho=18, cor_txt=TEXTO, alinhar=PP_ALIGN.LEFT, espaco=6) -> None:
    """paragrafos: lista de parágrafos; cada um é str ou lista de (texto, {bold, cor, tamanho, confirmar})."""
    tf.clear()
    tf.word_wrap = True
    for i, par in enumerate(paragrafos):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if alinhar is not None:
            p.alignment = alinhar
        p.space_after = Pt(espaco)
        for texto, op in ([(par, {})] if isinstance(par, str) else par):
            r = p.add_run()
            r.text = texto
            f = r.font
            f.name = 'Calibri'
            f.size = Pt(op.get('tamanho', tamanho))
            f.bold = op.get('bold', False)
            f.color.rgb = rgb(op.get('cor', cor_txt))
            if op.get('confirmar'):
                _marca_texto(r)


def caixa(slide, x, y, w, h, paragrafos, fundo=None, borda=None, ancora=MSO_ANCHOR.TOP, forma=MSO_SHAPE.RECTANGLE,
          **kw):
    s = slide.shapes.add_shape(forma, Cm(x), Cm(y), Cm(w), Cm(h))
    if fundo:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fundo)
    else:
        s.fill.background()
    if borda:
        s.line.color.rgb = rgb(borda)
        s.line.width = Pt(1.5)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    tf = s.text_frame
    tf.vertical_anchor = ancora
    for lado in ('margin_left', 'margin_right'):
        setattr(tf, lado, Cm(0.35))
    tf.margin_top = tf.margin_bottom = Cm(0.15)
    escrever(tf, paragrafos, **kw)
    return s


def texto(slide, x, y, w, h, paragrafos, **kw):
    return caixa(slide, x, y, w, h, paragrafos, **kw)


def confirmar(t: str) -> tuple[str, dict]:
    return (t, {'confirmar': True, 'bold': True})


def titulo(slide, t: str, secao: str | None = None) -> None:
    """Título-afirmação; `secao` põe a etiqueta do edital (Metodologia, Resultados, Conclusões) acima."""
    if secao:
        texto(slide, 0.56, 2.2, 20.0, 0.75, [[(secao.upper(), {'bold': True, 'cor': TEAL})]], tamanho=13,
              espaco=0)
    texto(slide, 0.56, 2.85 if secao else 2.35, 32.8, 1.7 if secao else 1.9, [t], tamanho=26, cor_txt=TEXTO,
          ancora=MSO_ANCHOR.MIDDLE, espaco=0).text_frame.paragraphs[0].runs[0].font.bold = True


def fonte(slide, t: str = 'Fonte: IBGE, Censo Demográfico 2022 — 104.108 setores urbanos dos 70 municípios '
                          'do ELSI-Brasil.') -> None:
    texto(slide, 0.56, 18.05, 32.8, 0.8, [t], tamanho=11, cor_txt=CINZA)


def notas(slide, t: str) -> None:
    slide.notes_slide.notes_text_frame.text = t


def falas_do_roteiro() -> dict[int, str]:
    """Fala de cada slide (### N.), sem a marcação de Markdown."""
    md = ROTEIRO.read_text(encoding='utf-8').split('## Reserva')[0]
    falas = {}
    for bloco in re.split(r'^### ', md, flags=re.M)[1:]:
        n = int(bloco.split('.')[0])
        m = re.search(r'\*\*Fala[^*]*\*\*:?\s*(.*?)(?=\n- \*\*|\n\s*\n|\Z)', bloco, re.S)
        t = re.sub(r'\*\*\(decorar\)\*\*\s*', '[DECORAR] ', m[1]) if m else ''
        t = re.sub(r'\*\(([^)]*)\)\*', r'[\1]', t).replace('*', '').replace('==', '')
        falas[n] = re.sub(r'\s+', ' ', t).strip()
    return falas


def tabela(slide, x, y, w, linhas, larguras, tamanho=13, altura=0.85):
    t = slide.shapes.add_table(len(linhas), len(linhas[0]), Cm(x), Cm(y), Cm(w), Cm(altura * len(linhas))).table
    for j, lw in enumerate(larguras):
        t.columns[j].width = Cm(lw)
    for i, lin in enumerate(linhas):
        for j, v in enumerate(lin):
            c = t.cell(i, j)
            c.fill.solid()
            c.fill.fore_color.rgb = rgb(TEAL if i == 0 else ('FFFFFF' if i % 2 else FUNDO))
            c.margin_left = c.margin_right = Cm(0.2)
            c.margin_top = c.margin_bottom = Cm(0.05)
            escrever(c.text_frame, [[(v, {'bold': i == 0, 'cor': 'FFFFFF' if i == 0 else TEXTO})]],
                     tamanho=tamanho, espaco=0, alinhar=PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER)
    return t


# ---------------------------------------------------------------- slides

def capa(s) -> None:
    caixas = {sh.name: sh for sh in s.shapes}
    escrever(caixas['CaixaDeTexto 1'].text_frame,
             ['Índice de vulnerabilidade à saúde das cidades brasileiras: dados do censo demográfico de 2022'],
             tamanho=22, alinhar=PP_ALIGN.CENTER, espaco=0)
    caixas['CaixaDeTexto 1'].text_frame.paragraphs[0].runs[0].font.bold = True
    escrever(caixas['CaixaDeTexto 3'].text_frame,
             [[('Aluno: Pedro Dias Soares', {'bold': True})],
              [('Orientadora: Amanda Cristina de Souza Andrade', {'bold': True})],
              [('Coorientador(a): não se aplica', {'bold': True})]],
             tamanho=16, alinhar=PP_ALIGN.CENTER, espaco=0)
    escrever(caixas['CaixaDeTexto 4'].text_frame,
             [[('Grupo de Pesquisa no Programa: ', {}),
               ('NESPE', {'bold': True})]],
             tamanho=16, alinhar=PP_ALIGN.CENTER, espaco=0)
    escrever(caixas['CaixaDeTexto 6'].text_frame,
             ['Data de ingresso no Programa: 06/03/2026', 'Programa de vínculo: FAPEMIG'],
             tamanho=16, alinhar=PP_ALIGN.CENTER, espaco=0)


def s2_media(s) -> None:
    titulo(s, 'A média da cidade esconde o que acontece dentro dela')
    caixa(s, 1.6, 5.2, 6.6, 6.6, [[('média', {'bold': True, 'cor': 'FFFFFF', 'tamanho': 26})]],
          fundo=CINZA, alinhar=PP_ALIGN.CENTER, ancora=MSO_ANCHOR.MIDDLE)
    texto(s, 0.6, 12.1, 8.6, 1.2, [[('1 cidade, 1 número', {'bold': True})]], tamanho=20,
          alinhar=PP_ALIGN.CENTER)
    seta = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Cm(8.8), Cm(7.8), Cm(2.4), Cm(1.4))
    seta.fill.solid()
    seta.fill.fore_color.rgb = rgb(LARANJA)
    seta.line.fill.background()
    tons = [FUNDO, TEAL_CLARO, TEAL, LAVANDA, CORAL]
    lado, x0, y0 = 0.66, 11.7, 5.2
    for i in range(10):
        for j in range(10):
            t = tons[(i * 7 + j * 3 + (i * j) % 5) % len(tons)]
            q = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x0 + j * lado), Cm(y0 + i * lado), Cm(lado - 0.06),
                                   Cm(lado - 0.06))
            q.fill.solid()
            q.fill.fore_color.rgb = rgb(t)
            q.line.fill.background()
    texto(s, 10.2, 12.1, 9.6, 1.9, [[('centenas de setores censitários', {'bold': True})]], tamanho=20,
          alinhar=PP_ALIGN.CENTER)
    texto(s, 10.2, 14.1, 9.6, 0.8, ['esquema ilustrativo — não são dados'], tamanho=12, cor_txt=CINZA,
          alinhar=PP_ALIGN.CENTER)
    pars = []
    for cab, txt in [('Setor censitário', 'a menor área com dados do Censo: como um quarteirão, ou poucos'),
                     ('Vulnerabilidade à saúde', 'condições do lugar (saneamento, renda, escolaridade) que deixam '
                                                 'os moradores mais expostos a adoecer'),
                     ('Para quê', 'achar, dentro da cidade, as áreas com condições mais desfavoráveis '
                                  '(IVS de Belo Horizonte, 2012)'),
                     ('Lacuna', 'não havia esse índice com o Censo 2022 para os municípios estudados')]:
        pars += [[(cab, {'bold': True, 'tamanho': 19, 'cor': TEAL})], txt]
    caixa(s, 20.6, 4.6, 12.5, 12.6, pars, fundo=FUNDO, tamanho=17, espaco=4, ancora=MSO_ANCHOR.MIDDLE)


def s3_objetivos(s) -> None:
    titulo(s, 'O projeto quer medir a vulnerabilidade onde ela acontece')
    caixa(s, 0.9, 4.6, 32.0, 3.7,
          [[('Objetivo geral do projeto da orientadora', {'bold': True, 'cor': TEAL, 'tamanho': 19})],
           [('Avaliar as desigualdades intraurbanas por meio da construção de um Índice de Vulnerabilidade '
             'à Saúde (IVS) de cidades brasileiras.', {})]],
          fundo=FUNDO, tamanho=20)
    for k, (num, txt, status, cor_st) in enumerate([
            ('1', 'Construir o IVS intraurbano com o Censo 2022', 'em andamento', LARANJA),
            ('2', 'Analisar a distribuição espacial do IVS (mapas)', 'a iniciar', CINZA)]):
        x = 0.9 + k * 16.2
        caixa(s, x, 8.9, 15.8, 4.9,
              [[('Meu objetivo ' + num, {'bold': True, 'cor': TEAL, 'tamanho': 19})],
               [(txt, {'bold': True, 'tamanho': 24})]], borda=TEAL_CLARO, tamanho=19)
        caixa(s, x + 0.35, 12.5, 4.4, 1.0, [[(status, {'bold': True, 'cor': 'FFFFFF'})]], fundo=cor_st,
              tamanho=16, alinhar=PP_ALIGN.CENTER, ancora=MSO_ANCHOR.MIDDLE, forma=MSO_SHAPE.ROUNDED_RECTANGLE)
    caixa(s, 0.9, 14.5, 32.0, 2.4,
          [[('Hoje: ', {'bold': True, 'cor': TEAL}),
            ('a etapa que vem antes do índice — o que o Censo 2022 me obrigou a decidir, e como cada decisão '
             'muda o resultado', {})]],
          fundo=LAVANDA, tamanho=21, alinhar=PP_ALIGN.CENTER, ancora=MSO_ANCHOR.MIDDLE)


def s4_base(s) -> None:
    titulo(s, 'Reconstruí o IVS de 2012 com o Censo 2022 nos 70 municípios do ELSI-Brasil', 'Metodologia')
    for k, (dim, cor_d, itens) in enumerate([
            ('Saneamento', TEAL, ['água inadequada', 'esgoto inadequado', 'lixo inadequado']),
            ('Socioeconômica', CORAL, ['moradores por domicílio', 'analfabetismo (15 anos ou mais)',
                                       'renda do responsável (invertida)', 'pessoas pretas, pardas ou indígenas'])]):
        x = 0.9 + k * 8.6
        caixa(s, x, 4.7, 8.2, 1.3, [[(dim, {'bold': True, 'cor': 'FFFFFF'})]], fundo=cor_d, tamanho=20,
              alinhar=PP_ALIGN.CENTER, ancora=MSO_ANCHOR.MIDDLE)
        caixa(s, x, 6.0, 8.2, 8.6, ['• ' + i for i in itens], fundo=FUNDO, tamanho=20, espaco=10)
    texto(s, 0.9, 14.9, 16.8, 2.2,
          ['↑ valor = ↑ vulnerabilidade. As variáveis do IVS 2012 que existem no Censo 2022, com adaptações '
           '(reserva R1).'], tamanho=16, cor_txt=CINZA)
    passos = [('109.032 setores', 'nos 70 municípios', FUNDO, TEXTO),
              ('− 1.736 sem moradores  ·  − 1.015 com sigilo', None, None, CINZA),
              ('106.281 setores', None, FUNDO, TEXTO),
              ('− 2.173 rurais (2,04%) — o índice é urbano', None, None, CINZA),
              ('104.108 setores urbanos', '52,1 milhões de moradores', TEAL, 'FFFFFF')]
    y = 4.7
    for forte, fraco, fundo_p, cor_p in passos:
        h = 2.1 if fraco else (1.8 if fundo_p else 1.0)
        pars = [[(forte, {'bold': fundo_p is not None, 'cor': cor_p, 'tamanho': 22 if fundo_p else 16})]]
        if fraco:
            pars.append([(fraco, {'cor': cor_p, 'tamanho': 17})])
        caixa(s, 18.6, y, 14.3, h, pars, fundo=fundo_p, alinhar=PP_ALIGN.CENTER, ancora=MSO_ANCHOR.MIDDLE,
              espaco=0)
        y += h + 0.2
    mais10 = sum(float(r['pct_excluido']) > 10 for r in RURAL)
    texto(s, 18.6, y + 0.1, 14.3, 1.6,
          [[(f'A exclusão rural é desigual: passa de 10% em {mais10} dos 70 municípios (R6).', {'bold': True})]],
          tamanho=16, cor_txt=CORAL, alinhar=PP_ALIGN.CENTER)
    fonte(s, 'Fonte: IBGE, Censo Demográfico 2022. ELSI-Brasil: Estudo Longitudinal da Saúde dos Idosos '
             'Brasileiros (Lima-Costa et al., 2018).')


def s5_validacao(s) -> None:
    titulo(s, 'Antes de confiar nos dados, conferi o processamento com os números oficiais', 'Metodologia')
    for k, (grande, leg) in enumerate([
            ('203.080.756', 'pessoas: o código reproduz a população oficial do Brasil (468.099 setores)'),
            ('79,99  ×  80,0', 'índice de envelhecimento do Brasil: meu cálculo × o publicado pelo IBGE')]):
        x = 0.9 + k * 16.2
        caixa(s, x, 4.8, 15.8, 6.2,
              [[(grande, {'bold': True, 'tamanho': 48, 'cor': TEAL})], [(leg, {'tamanho': 20})]],
              fundo=FUNDO, alinhar=PP_ALIGN.CENTER, ancora=MSO_ANCHOR.MIDDLE, espaco=8)
    e = EXTREMO
    caixa(s, 0.9, 11.6, 32.0, 4.0,
          [[('Uma decisão no caminho', {'bold': True, 'cor': CORAL, 'tamanho': 20})],
           [('Um setor de favela em Belo Horizonte com renda média de ', {}),
            (f'R$ {br(float(e["renda_media_setor"]), 2)}', {'bold': True}),
            (f' por mês — {br(float(e["razao_mediana_mun"]), 1)} vezes a mediana do município. Incoerente com o '
             'perfil do setor: retirado da análise descritiva.', {})]],
          borda=CORAL, tamanho=20)
    texto(s, 0.9, 15.9, 32.0, 1.4,
          ['Outras adequações ao Censo 2022: denominador dos domicílios · analfabetismo a partir de 15 anos · '
           'dados sob sigilo tratados como ausentes · caçamba como destino inadequado do lixo (reserva R1).'],
          tamanho=15, cor_txt=CINZA)
    fonte(s, 'Fonte: IBGE, Censo Demográfico 2022.')


def s6_zeros(s, fig: Path) -> None:
    titulo(s, f'Em {br(float(T03["pct_agua_inad"]["pct_zeros"]), 0)}% dos setores, nenhum domicílio foi '
              'registrado com água inadequada', 'Resultados')
    s.shapes.add_picture(str(fig), Cm(0.6), Cm(4.6), width=Cm(21.2))
    texto(s, 0.9, 16.0, 20.6, 1.2, ['Parte dos zeros vem de parcelas pequenas suprimidas pelo IBGE, que entram '
                                    'como zero.'], tamanho=14, cor_txt=CINZA)
    t1 = {r['indicador']: r for r in TAB1}['renda_media_sem_extremo']
    media = float(t1['Média'].replace('.', '').replace(',', '.'))
    mediana = float(t1['Mediana'].replace('.', '').replace(',', '.'))
    caixa(s, 22.6, 4.8, 10.4, 5.2,
          [[('A renda também', {'bold': True, 'cor': TEAL, 'tamanho': 19})],
           [(f'média {br((media / mediana - 1) * 100, 0)}% acima da mediana', {'bold': True, 'tamanho': 24})],
           [('poucos setores muito ricos puxam a média', {'tamanho': 17, 'cor': CINZA})]],
          fundo=FUNDO, espaco=6)
    caixa(s, 22.6, 10.6, 10.4, 5.4,
          [[('O que isso muda', {'bold': True, 'cor': CORAL, 'tamanho': 19})],
           'O índice põe tudo na mesma régua, de 0 a 1. Com tantos zeros, quase todos os setores ficariam '
           'espremidos num canto dela.'],
          borda=CORAL, tamanho=18)
    fonte(s)


def s7_sigilo(s, fig: Path) -> None:
    titulo(s, 'O dado que falta também diz alguma coisa', 'Resultados')
    s.shapes.add_picture(str(fig), Cm(0.9), Cm(4.4), height=Cm(13.4))
    pct = br((N_RECORTE - N_ANALFAB) / N_RECORTE * 100, 0)
    caixa(s, 19.2, 4.7, 13.8, 5.6,
          [[(f'{pct}%', {'bold': True, 'tamanho': 44, 'cor': CORAL}),
            ('  dos setores sem o dado de analfabetismo', {'bold': True, 'tamanho': 20})],
           'Sigilo: quando há pouquíssima gente numa categoria, o IBGE esconde o número para ninguém ser '
           'identificado.'],
          fundo=FUNDO, tamanho=17, espaco=6)
    caixa(s, 19.2, 10.8, 13.8, 5.8,
          [[('O que isso muda', {'bold': True, 'cor': CORAL, 'tamanho': 19})],
           [('Média observada ', {}), (f'{br(MEDIA_ANALFAB_OBS, 2)}%', {'bold': True}), ('; a real fica entre ', {}),
            (f'{br(MEDIA_ANALFAB_MIN, 2)}%', {'bold': True}), (' e ', {}),
            (f'{br(MEDIA_ANALFAB_OBS, 2)}%', {'bold': True}), ('.', {})],
           'O efeito é pequeno, mas o sigilo não é aleatório: precisa de tratamento próprio.'],
          borda=CORAL, tamanho=18)
    fonte(s)


def s8_correlacoes(s, fig: Path) -> None:
    titulo(s, 'Renda, cor/raça e analfabetismo andam juntos; o lixo anda sozinho', 'Resultados')
    s.shapes.add_picture(str(fig), Cm(0.6), Cm(4.4), width=Cm(22.6))
    caixa(s, 23.8, 4.8, 9.2, 5.2,
          [[('Como ler', {'bold': True, 'cor': TEAL, 'tamanho': 19})],
           'Correlação: 0 = nenhuma relação; 1 = as duas ordenam os setores do mesmo jeito.',
           [('As três medem a posição social do setor.', {'bold': True})]],
          fundo=FUNDO, tamanho=17, espaco=6)
    caixa(s, 23.8, 10.6, 9.2, 6.4,
          [[('Hipótese a testar', {'bold': True, 'cor': CORAL, 'tamanho': 19})],
           'Seguindo o IVS 2012, o projeto conta a caçamba como destino inadequado (o Censo só registra o '
           'destino). Ela pode refletir o jeito de coletar da cidade, não a vulnerabilidade.'],
          borda=CORAL, tamanho=16)
    fonte(s, f'Correlação de Spearman nos {br(PECAS["figura1"]["n_dados_completos"], 0)} setores com os 12 '
             'indicadores completos (Figura 1 do relatório); renda invertida. Fonte: IBGE, Censo 2022.')


def s9_desigualdade(s) -> None:
    titulo(s, 'Dentro das cidades, renda mais alta anda junto com mais idosos', 'Resultados')
    neg, tot = ROB['municipios_idoso_renda_negativa'], ROB['municipios_30mais']
    caixa(s, 0.9, 4.8, 19.4, 11.0,
          [[(f'{neg} de {tot}', {'bold': True, 'tamanho': 88, 'cor': CORAL})],
           [('municípios em que a proporção de idosos é maior nos setores de renda mais alta',
             {'tamanho': 22})],
           [(f'mediana municipal da correlação: {br(ROB["mediana_municipal_idoso_renda"], 2)}',
             {'tamanho': 16, 'cor': CINZA})]],
          fundo=FUNDO, alinhar=PP_ALIGN.CENTER, ancora=MSO_ANCHOR.MIDDLE, espaco=10)
    idoso = R['pct_idoso_60mais']['renda_media_sem_extremo']
    crianca = R['pct_pop_0a14']['renda_media_sem_extremo']
    caixa(s, 20.9, 4.8, 12.1, 11.0,
          [[('No conjunto dos setores', {'bold': True, 'cor': TEAL, 'tamanho': 19})],
           [('idosos × renda invertida', {'tamanho': 18})],
           [(br(idoso, 2), {'bold': True, 'tamanho': 40, 'cor': TEAL})],
           [('crianças × renda invertida', {'tamanho': 18})],
           [(('+' if crianca > 0 else '') + br(crianca, 2), {'bold': True, 'tamanho': 40, 'cor': CORAL})],
           [('mais idosos onde a renda é maior; mais crianças onde é menor', {'tamanho': 16, 'cor': CINZA})]],
          borda=TEAL_CLARO, alinhar=PP_ALIGN.CENTER, ancora=MSO_ANCHOR.MIDDLE, espaco=4)
    texto(s, 0.9, 16.2, 32.0, 1.6,
          [[('Associação entre áreas, não entre pessoas.', {'bold': True})],
           [(f'Municípios com pelo menos 30 setores com dados completos ({tot} dos 70). Spearman; renda '
             'invertida.', {'tamanho': 13, 'cor': CINZA})]],
          tamanho=17, cor_txt=TEXTO, alinhar=PP_ALIGN.CENTER, espaco=0)
    fonte(s)


def s10_conclusao(s) -> None:
    titulo(s, 'Conclusões e próximos passos', 'Conclusões')
    conc = ['Montar o IVS com o Censo 2022 exige decisões explícitas sobre zeros, sigilo e valores extremos.',
            'O sigilo se concentra nos setores mais ricos e precisa de tratamento próprio.',
            'O lixo se comporta à parte e será testado na análise fatorial.']
    caixa(s, 0.9, 4.6, 18.6, 9.4,
          [[('Conclusões', {'bold': True, 'cor': 'FFFFFF', 'tamanho': 21})]] +
          [[(f'{k}  ', {'bold': True, 'cor': 'FFFFFF'}), (c, {'cor': 'FFFFFF'})] for k, c in enumerate(conc, 1)],
          fundo=TEAL, tamanho=20, espaco=10)
    passos = ['Análise fatorial', 'Pesos das variáveis', 'Faixas de vulnerabilidade', 'Mapas no QGIS', 'Artigo']
    caixa(s, 20.1, 4.6, 12.8, 1.2, [[('Próximos passos', {'bold': True, 'cor': TEAL})]], tamanho=21,
          ancora=MSO_ANCHOR.MIDDLE)
    for k, p in enumerate(passos):
        caixa(s, 20.1, 5.9 + k * 1.62, 12.8, 1.42, [[(f'{k + 1}  {p}', {'bold': True})]], fundo=LAVANDA,
              tamanho=18, ancora=MSO_ANCHOR.MIDDLE)
    caixa(s, 0.9, 15.5, 32.0, 2.3,
          [[('Com dados, cada decisão muda o resultado — por isso cada uma está justificada e registrada.',
             {'bold': True, 'tamanho': 21, 'cor': TEAL})],
           [('Limitação: estudo ecológico — dados de áreas, não de pessoas.', {'tamanho': 16, 'cor': CINZA})]],
          borda=TEAL_CLARO, alinhar=PP_ALIGN.CENTER, ancora=MSO_ANCHOR.MIDDLE, espaco=2)


# ---------------------------------------------------------------- reserva

def r1_adequacoes(s) -> None:
    titulo(s, 'Reserva R1 · Como as variáveis de 2012 foram reconstruídas no Censo 2022')
    linhas = [['Componente', 'Censo 2022', 'Denominador'],
              ['Água inadequada', 'V00112 a V00118', 'V00001 (domicílios part. perm. ocupados)'],
              ['Esgoto inadequado', 'V00312 a V00316', 'V00001'],
              ['Lixo inadequado (caçamba incluída)', 'V00398 a V00402', 'V00001'],
              ['Razão de moradores', '(V00005 + V00006)', 'V00001 + V00002 (inclui improvisados)'],
              ['Analfabetismo 15+ (2012: 5+)', 'V00901', 'V00900 + V00901'],
              ['Renda do responsável (invertida)', 'V06004 (média, já calculada pelo IBGE)', '—'],
              ['Preta, parda ou indígena', 'V01318 + V01320 + V01321', 'população total']]
    tabela(s, 0.9, 4.7, 32.0, linhas, [10.5, 10.5, 11.0], tamanho=15, altura=1.15)
    texto(s, 0.9, 14.4, 32.0, 2.6,
          ['Sigilo: se o IBGE suprimiu todas as parcelas de um numerador, o indicador fica ausente, nunca zero; '
           'parcelas suprimidas em parte entram como zero, o que subestima saneamento e cor/raça '
           '(na água, a média real pode ser até 14,9% maior).'],
          tamanho=15, cor_txt=CINZA)
    fonte(s, 'Fonte: dicionário de dados dos agregados por setores censitários do Censo 2022 (IBGE); '
             'IVS 2012 (SMS-BH, 2013).')


def r2_matriz(s) -> None:
    titulo(s, 'Reserva R2 · Correlação de Spearman entre os 12 indicadores')
    s.shapes.add_picture(str(FIGURAS / 'fig1_correlacao.png'), Cm(9.0), Cm(4.3), height=Cm(13.6))
    fonte(s, f'n = {br(PECAS["figura1"]["n_dados_completos"], 0)} setores com os 12 indicadores completos; '
             'renda invertida. Figura 1 do relatório parcial.')


def r3_tabela1(s) -> None:
    titulo(s, 'Reserva R3 · Estatísticas descritivas dos 12 indicadores (Tabela 1)')
    linhas = [['Indicador', 'n', 'Média', 'Mediana', 'p75', 'Máx', 'Assim.']]
    linhas += [[r['Indicador'], r['n'], r['Média'], r['Mediana'], r['p75'], r['Máx'], r['Assim.']] for r in TAB1]
    tabela(s, 0.9, 4.4, 32.0, linhas, [9.2, 3.6, 3.8, 3.8, 3.8, 4.0, 3.8], tamanho=13, altura=1.0)
    fonte(s, 'Proporções de 0 a 1, exceto razão de moradores e renda (R$). n = setores com o dado; ausentes por '
             'sigilo do IBGE. Renda sem o setor extremo.')


def r4_regioes(s) -> None:
    titulo(s, 'Reserva R4 · Médias por região dos 7 indicadores do IVS')
    ordem = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    inds = [('pct_agua_inad', 'Água inadequada', 3), ('pct_esgoto_inad', 'Esgoto inadequado', 3),
            ('pct_lixo_inad', 'Lixo inadequado', 3), ('razao_moradores', 'Razão de moradores', 2),
            ('pct_analfab', 'Analfabetismo 15+', 3), ('renda_media_sem_extremo', 'Renda média (R$)', 0),
            ('pct_raca_pretpardind', 'Preta, parda ou indígena', 3)]
    med = {(r['regiao'], r['indicador']): float(r['media']) for r in T04}
    nmun = {g: sum(m['regiao'] == g for m in MUNICIPIOS) for g in ordem}
    nset = {r['regiao']: r['n'] for r in T04 if r['indicador'] == 'pct_agua_inad'}
    linhas = [['Indicador'] + [f'{g} ({nmun[g]} mun.)' for g in ordem]]
    linhas += [[rot] + [br(med[(g, col)], c) for g in ordem] for col, rot, c in inds]
    linhas += [['Setores'] + [br(int(nset[g]), 0) for g in ordem]]
    tabela(s, 0.9, 4.6, 32.0, linhas, [8.5, 4.7, 4.7, 4.7, 4.7, 4.7], tamanho=14, altura=1.1)
    fonte(s, 'Médias simples entre setores. Os contrastes descrevem os municípios estudados, não as regiões.')


def r5_extremo(s) -> None:
    titulo(s, 'Reserva R5 · O setor com renda média de R$ 170.418,06')
    e = EXTREMO
    caixa(s, 0.9, 4.7, 32.0, 6.6,
          [[(f'{e["NM_MUN"]} · {e["NM_BAIRRO"]} — setor de favela (FCU {e["NM_FCU"]})', {'bold': True,
                                                                                        'cor': TEAL})],
           f'Renda média do responsável: R$ {br(float(e["renda_media_setor"]), 2)} — '
           f'{br(float(e["razao_mediana_mun"]), 1)} vezes a mediana do município (R$ {br(float(e["renda_p50_mun"]), 2)})',
           f'{br(float(e["populacao"]), 0)} moradores em {br(float(e["n_domicilios"]), 0)} domicílios · '
           f'analfabetismo {br(float(e["pct_analfab"]) * 100, 1)}% · preta, parda ou indígena '
           f'{br(float(e["pct_raca_pretpardind"]) * 100, 1)}%',
           'O perfil do setor não combina com a renda: tratado como valor incoerente e retirado da análise '
           'descritiva. Os demais valores extremos ficaram na base (máximo restante: R$ 140.172,64).'],
          fundo=FUNDO, tamanho=19, espaco=10)
    fonte(s, 'Fonte: IBGE, Censo 2022; rastreamento de extremos de renda (banco_de_dados/eda/'
             'renda_outliers_rastreados.csv).')


def r6_criterio53(s) -> None:
    titulo(s, 'Reserva R6 · Por que 53 municípios, e não 70')
    mais10 = sum(float(r['pct_excluido']) > 10 for r in RURAL)
    mais50 = sum(float(r['pct_excluido']) > 50 for r in RURAL)
    caixa(s, 0.9, 4.7, 15.6, 6.4,
          [[('Correlação dentro de cada município', {'bold': True, 'cor': TEAL})],
           f'Calculada só onde há pelo menos 30 setores com os 12 indicadores completos: '
           f'{ROB["municipios_30mais"]} dos 70 municípios.',
           f'Idosos × renda invertida: negativa em {ROB["municipios_idoso_renda_negativa"]} deles; mediana '
           f'municipal {br(ROB["mediana_municipal_idoso_renda"], 2)}.'],
          fundo=FUNDO, tamanho=19, espaco=10)
    caixa(s, 17.3, 4.7, 15.6, 6.4,
          [[('A exclusão dos setores rurais é desigual', {'bold': True, 'cor': CORAL})],
           f'No total saem 2,04% dos setores, mas {mais10} dos 70 municípios perdem mais de 10% e {mais50} '
           'perdem mais da metade.',
           'Municípios pequenos ficam com poucos setores urbanos — isso entra nas limitações.'],
          borda=CORAL, tamanho=19, espaco=10)
    fonte(s, 'Fonte: IBGE, Censo 2022; conferência da exclusão rural por município (banco_de_dados/eda/'
             'exclusao_rural_conferencia.csv).')


NOTAS_RESERVA = {
    'R1': 'Pergunta: "É comparável com o IVS de 2012?" — Mesmas dimensões, com adaptações documentadas: '
          'analfabetismo a partir de 15 anos (2012: 5+) e renda média do responsável no lugar das faixas de '
          'salário mínimo, que o Censo 2022 não traz por setor.',
    'R2': 'Pergunta: "E as correlações dos complementares?" — Água canalizada acompanha a água inadequada; '
          'moradia não convencional é praticamente independente; idosos e crianças vão em direções opostas.',
    'R3': 'Pergunta: "Quais as descritivas?" — Mediana zero nos três de saneamento; n menor no analfabetismo '
          'e no banheiro por causa do sigilo.',
    'R4': 'Pergunta: "E as diferenças regionais? Dá para generalizar?" — A proporção média de domicílios com '
          'água inadequada por setor é 16 vezes maior nos municípios do Norte (0,323) que nos do Sul (0,020); '
          'esgoto 8×, pretos/pardos/indígenas 3×. Não dá para generalizar: o Norte tem 6 municípios, e os '
          'contrastes descrevem a amostra, não as regiões.',
    'R5': 'Pergunta: "Por que tirar só esse setor?" — A renda média é 55,7 vezes a mediana do município, num '
          'setor de favela com 7% de analfabetismo: incoerente com o perfil do setor. Os demais extremos ficaram.',
    'R6': 'Pergunta: "Por que 53, se são 70?" — Para calcular a correlação dentro de cada município, adotei o '
          'mínimo de 30 setores com todos os dados; municípios pequenos ficam com poucos setores após o recorte '
          'urbano.',
}


# ---------------------------------------------------------------- montagem

def mover_para(prs, slide, posicao: int) -> None:
    lista = prs.slides._sldIdLst
    el = next(e for e in lista if prs.slides.get(int(e.get('id'))) is slide)
    lista.remove(el)
    lista.insert(posicao, el)


def main() -> None:
    FIGURAS.mkdir(exist_ok=True)
    figs = {'zeros': fig_zeros(), 'sigilo': fig_sigilo(), 'correlacoes': fig_correlacoes()}

    prs = Presentation(str(MODELO))
    capa_s, exemplo, final_s = prs.slides[0], prs.slides[1], prs.slides[2]
    conteudo = next(l for l in prs.slide_layouts if l.name == 'Conteúdo')
    falas = falas_do_roteiro()

    capa(capa_s)
    notas(capa_s, falas[1])
    montar = [s2_media, s3_objetivos, s4_base, s5_validacao, lambda s: s6_zeros(s, figs['zeros']),
              lambda s: s7_sigilo(s, figs['sigilo']), lambda s: s8_correlacoes(s, figs['correlacoes']),
              s9_desigualdade, s10_conclusao]
    for n, f in enumerate(montar, start=2):
        s = prs.slides.add_slide(conteudo)
        f(s)
        notas(s, falas[n])
    mover_para(prs, final_s, len(prs.slides) - 1)
    notas(final_s, falas[11])

    for chave, f in [('R1', r1_adequacoes), ('R2', r2_matriz), ('R3', r3_tabela1), ('R4', r4_regioes),
                     ('R5', r5_extremo), ('R6', r6_criterio53)]:
        s = prs.slides.add_slide(conteudo)
        f(s)
        notas(s, NOTAS_RESERVA[chave])

    # O slide-exemplo ("Lorem ipsum") sai só agora: removido antes, o próximo slide criado
    # herdaria o nome de arquivo do slide final e o pacote ficaria com duas partes iguais.
    lista = prs.slides._sldIdLst
    el = next(e for e in lista if prs.slides.get(int(e.get('id'))) is exemplo)
    prs.part.drop_rel(el.rId)
    lista.remove(el)
    prs.save(str(SAIDA))
    print(f'{SAIDA.relative_to(RAIZ)}: {len(prs.slides)} slides (11 de fala + 6 de reserva)')

    # Versão de envio: os mesmos slides, sem as páginas de notas (as falas e as marcas de ensaio ficam
    # só no arquivo do Pedro).
    envio = Presentation(str(SAIDA))
    for s in envio.slides:
        for r_id, rel in list(s.part.rels.items()):
            if rel.reltype.endswith('/notesSlide'):
                s.part.drop_rel(r_id)
    envio.save(str(SAIDA_ENVIO))
    print(f'{SAIDA_ENVIO.relative_to(RAIZ)}: {len(envio.slides)} slides, sem notas')


if __name__ == '__main__':
    main()
