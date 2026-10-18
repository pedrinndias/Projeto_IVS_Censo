"""Relatório parcial de atividades — RAIC 2026 (Anexo 1 do edital): gera o .docx e o PDF.

O texto segue `relatorio_parcial_raic/ARQUITETURA.md`:
  - Introdução, Objetivos, Metodologia, Quadro 1 e Referências são os do Plano de trabalho da
    orientadora, copiados literalmente; as únicas mudanças são correções de digitação e de
    citação, listadas em `relatorio_parcial_raic/NOTAS_PARA_ORIENTADORA.md`;
  - as adequações ao Censo 2022, os resultados e as conclusões são texto novo;
  - Figura 1, Tabela 1 e Quadro 2 e as correlações citadas saem de `scripts/pecas_relatorio_raic.py`
    (`relatorio_parcial_raic/dados/`). Os demais números vêm do relatório da EDA
    (`docs/relatorios/Relatorio_EDA_Fase3_IVS_ELSI.md`) e da T03, com a linha de origem anotada.
  - O que só o Pedro sabe fica como [[A PREENCHER …]], destacado em amarelo.

Monta um ODT plano (.fodt), converte em .docx com o LibreOffice e, do .docx, gera o PDF para
contar as páginas (limite do edital: 10).

Trava contra sobrescrever edição manual: se o .docx de saída existir e for diferente do último
gerado (`dados/gerado.sha256`), o script para. Use --sobrescrever para gerar mesmo assim.

Com --grifado, gera uma cópia de conferência (…_GRIFADO_conferencia.docx/.pdf) com cada trecho grifado pela
origem — verde: copiado do Plano de trabalho; laranja: correção dentro do trecho copiado; azul: texto novo
reescrito na revisão do conselho e na humanização; lilás: texto novo conferido e mantido. Não toca no .docx
de entrega.

Uso:
    ./.venv/bin/python scripts/pecas_relatorio_raic.py      # antes, se os dados mudarem
    ./.venv/bin/python scripts/gerar_relatorio_raic.py [--sobrescrever | --grifado]
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd
from pypdf import PdfReader

from pecas_relatorio_raic import br  # mesmo arredondamento (NBR 5891) das peças

RAIZ = Path(__file__).resolve().parents[1]
PASTA = RAIZ / 'relatorio_parcial_raic'
DADOS = PASTA / 'dados'
NOME = 'Relatorio_Parcial_RAIC_2026_Pedro_v1'
SAIDA_DOCX, SAIDA_PDF = PASTA / f'{NOME}.docx', PASTA / f'{NOME}.pdf'
HASH = DADOS / 'gerado.sha256'
T03 = RAIZ / 'analises_exploratorias' / '00_referencia' / 'tabelas' / 'T03_descritivas_global.csv'
LIMITE_PAGINAS = 10
GRIFAR = '--grifado' in sys.argv
GRIFOS = {  # estilo: (cor, legenda) — pedido do Pedro em 12/10/2026
    'G_Copia': ('#C6EFCE', 'Verde: copiado do Plano de trabalho da orientadora.'),
    'G_Corr': ('#FFC000', 'Laranja: correção feita dentro de um trecho copiado '
                          '(lista em NOTAS_PARA_ORIENTADORA.md, seção 1).'),
    'G_Revisado': ('#BDD7EE', 'Azul: texto gerado pelo Claude e reescrito na revisão do conselho e na humanização.'),
    'G_Gerado': ('#E4DFEC', 'Lilás: texto gerado pelo Claude, conferido na revisão e mantido sem reescrita '
                            '(títulos de subseção, legendas, notas, Quadro 2, Tabela 1 e referências acrescentadas).'),
}
CAT: str | None = None  # categoria de grifo do trecho em montagem
ESTILOS_GRIFO: set[tuple[str, str]] = set()  # (estilo de parágrafo, categoria) usados na cópia grifada

PECAS = json.loads((DADOS / 'pecas.json').read_text(encoding='utf-8'))
R = PECAS['figura1']['R']
N_FIG = PECAS['figura1']['n_dados_completos']
TAB1 = pd.read_csv(DADOS / 'tabela1_descritivas.csv', dtype=str, encoding='utf-8-sig')
QUADRO2 = pd.read_csv(DADOS / 'quadro2_indicadores.csv', dtype=str, encoding='utf-8-sig')
ZEROS = pd.read_csv(T03).set_index('indicador')['pct_zeros']


def r(a: str, b: str) -> str:
    """Correlação da Figura 1, com 2 casas."""
    return br(R[a][b], 2)


def z(col: str) -> str:
    """% de setores com valor zero (T03)."""
    return br(ZEROS[col], 2) + '%'


def n(col: str) -> str:
    return TAB1.set_index('indicador').loc[col, 'n']


def t1(col: str, coluna: str) -> str:
    return TAB1.set_index('indicador').loc[col, coluna]


# ── marcação mínima: **negrito**, ~~itálico~~, [[pendência]], \t = tabulação ─────────────────────────────
def inline(texto: str) -> str:
    s = escape(texto)
    s = re.sub(r'\*\*\^\^(.+?)\^\^\*\*',
               r'<text:span text:style-name="G_Corr_Negrito">\1</text:span>' if GRIFAR else r'**\1**', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<text:span text:style-name="Negrito">\1</text:span>', s)
    s = re.sub(r'~~(.+?)~~', r'<text:span text:style-name="Italico">\1</text:span>', s)
    s = s.replace('\t', '<text:tab/>')
    s = re.sub(r'\[\[(.+?)\]\]', r'<text:span text:style-name="Pendente">[\1]</text:span>', s)
    s = re.sub(r'\^\^(.+?)\^\^', r'<text:span text:style-name="G_Corr">\1</text:span>' if GRIFAR else r'\1', s)
    return s


def cat(nome: str | None) -> None:
    global CAT
    CAT = nome


def grifo(estilo: str, categoria: str | None = '…') -> str:
    """Na cópia grifada, o parágrafo inteiro recebe o fundo da categoria (estilo derivado do original)."""
    c = CAT if categoria == '…' else categoria
    if not (GRIFAR and c):
        return estilo
    ESTILOS_GRIFO.add((estilo, c))
    return f'{estilo}__{c}'


CORPO: list[str] = []


def p(texto: str, estilo: str = 'Corpo') -> None:
    CORPO.append(f'<text:p text:style-name="{grifo(estilo)}">{inline(texto)}</text:p>')


def h1(texto: str, estilo: str = 'Heading_20_1') -> None:
    CORPO.append(f'<text:h text:style-name="{estilo}" text:outline-level="1">{inline(texto)}</text:h>')


def h2(texto: str) -> None:
    # títulos de subseção criados no texto novo não foram reescritos na humanização: lilás
    c = 'G_Gerado' if CAT == 'G_Revisado' else CAT
    CORPO.append(f'<text:h text:style-name="{grifo("Heading_20_2", c)}" text:outline-level="2">{inline(texto)}</text:h>')


def celula(texto: str, estilo_cel: str, estilo_p: str, linhas: int = 1, categoria: str | None = '…') -> str:
    span = f' table:number-rows-spanned="{linhas}"' if linhas > 1 else ''
    return (f'<table:table-cell table:style-name="{estilo_cel}" office:value-type="string"{span}>'
            f'<text:p text:style-name="{grifo(estilo_p, categoria)}">{inline(texto)}</text:p></table:table-cell>')


COLUNAS_TAB: list[str] = []  # estilos automáticos de coluna, um por tabela


def tabela(nome: str, larguras: list[float], cabecalho: list[str], linhas: list[list[str]],
           numericas: set[int] = frozenset(), grade: bool = False, mesclar_col0: bool = False,
           cat_cab: str | None = '…') -> None:
    """Tabela (bordas só em cima e embaixo, ABNT/IBGE) ou quadro (grade fechada)."""
    for i, w in enumerate(larguras):
        COLUNAS_TAB.append(f'<style:style style:name="{nome}.c{i}" style:family="table-column">'
                           f'<style:table-column-properties style:column-width="{w}cm"/></style:style>')
    COLUNAS_TAB.append(f'<style:style style:name="{nome}" style:family="table"><style:table-properties '
                       f'style:width="{sum(larguras)}cm" table:align="center" fo:margin-top="0cm" fo:margin-bottom="0cm" '
                       f'style:may-break-between-rows="false" fo:keep-with-next="always"/></style:style>')
    x = [f'<table:table table:name="{nome}" table:style-name="{nome}">']
    x += [f'<table:table-column table:style-name="{nome}.c{i}"/>' for i in range(len(larguras))]

    def estilo_p(j: int, cab: bool) -> str:
        if cab:
            return 'Tab_CabNum' if j in numericas else 'Tab_Cab'
        return 'Tab_Num' if j in numericas else 'Tab_Texto'

    cel_cab = 'C_GradeCab' if grade else 'C_Cab'
    x.append('<table:table-header-rows><table:table-row>')
    x += [celula(t, cel_cab, estilo_p(j, True), categoria=cat_cab) for j, t in enumerate(cabecalho)]
    x.append('</table:table-row></table:table-header-rows>')
    # mesclagem da 1ª coluna (dimensão) em quadros: conta as repetições consecutivas
    spans, i = {}, 0
    while i < len(linhas):
        k = i
        while mesclar_col0 and k + 1 < len(linhas) and linhas[k + 1][0] == linhas[i][0]:
            k += 1
        spans[i] = k - i + 1
        i = k + 1
    for i, linha in enumerate(linhas):
        ultima = i == len(linhas) - 1
        cel = 'C_Grade' if grade else ('C_Fim' if ultima else 'C_Corpo')
        x.append('<table:table-row>')
        for j, t in enumerate(linha):
            if j == 0 and mesclar_col0:
                if i in spans:
                    x.append(celula(t, cel, 'Tab_Texto', spans[i]))
                else:
                    x.append('<table:covered-table-cell/>')
                continue
            x.append(celula(t, cel, estilo_p(j, False)))
        x.append('</table:table-row>')
    x.append('</table:table>')
    CORPO.append(''.join(x))


def legenda(texto: str) -> None:
    p(texto, 'Legenda')


def fonte(texto: str) -> None:
    p(texto, 'Fonte_Nota')


def figura(caminho: Path, largura_cm: float) -> None:
    dados = caminho.read_bytes()
    w, h = int.from_bytes(dados[16:20], 'big'), int.from_bytes(dados[20:24], 'big')  # cabeçalho PNG
    altura = largura_cm * h / w
    CORPO.append(
        f'<text:p text:style-name="Figura"><draw:frame draw:style-name="fr_fig" draw:name="{caminho.stem}" '
        f'text:anchor-type="as-char" svg:width="{largura_cm}cm" svg:height="{altura:.2f}cm" draw:z-index="0">'
        f'<draw:image><office:binary-data>{base64.b64encode(dados).decode()}</office:binary-data>'
        f'</draw:image></draw:frame></text:p>')


def item(texto: str) -> None:
    p('•\t' + texto, 'Lista')


# ══════════════════════════════════════════════════════════════════════════════════════
# CONTEÚDO
# ══════════════════════════════════════════════════════════════════════════════════════
def conteudo() -> None:
    if GRIFAR:
        cat(None)
        p('CÓPIA DE CONFERÊNCIA — não é a versão de entrega', 'Grifo_Topo')
        p('Cada trecho do relatório está grifado conforme a origem:', 'Capa_Campo')
        for estilo, (_, descricao) in GRIFOS.items():
            CORPO.append(f'<text:p text:style-name="Capa_Campo"><text:span text:style-name="{estilo}">'
                         f'{escape(descricao)}</text:span></text:p>')
        p('Sem grifo: títulos exigidos pelo Anexo 1, folha de rosto, texto do bolsista (Outras atividades e Apoio), '
          'pendências (amarelo) e a Figura 1, que é imagem. A ordem alfabética das referências também é ajuste '
          'feito no texto copiado.', 'Capa_Campo')
    # ── I. IDENTIFICAÇÃO (folha de rosto) ──────────────────────────────────────────────
    p('FUNDAÇÃO OSWALDO CRUZ — INSTITUTO RENÉ RACHOU FIOCRUZ MINAS', 'Capa_Instituicao')
    p('Relatório parcial de atividades — RAIC 2026', 'Capa_Centro')
    p('ÍNDICE DE VULNERABILIDADE À SAÚDE (IVS) INTRAURBANO — CENSO DEMOGRÁFICO 2022', 'Capa_Titulo')
    h1('I. IDENTIFICAÇÃO')
    campos = [
        ('Título do trabalho', 'Índice de Vulnerabilidade à Saúde (IVS) intraurbano — Censo Demográfico 2022'),
        ('Bolsista', 'Pedro Dias Soares'),
        ('Orientadora', 'Amanda Cristina de Souza Andrade'),
        ('Coorientador(es)', 'Não se aplica'),
        ('Unidade / Departamento / Laboratório ou Núcleo ou Programa',
         'Fiocruz Minas — Instituto René Rachou'),
        ('Programa ao qual está vinculado', 'FAPEMIG'),
        ('Área de conhecimento', 'Saúde Coletiva'),
        ('Data de Início no Programa', '06 de março de 2026'),
        ('Palavras-Chave', 'Vulnerabilidade em Saúde; Saúde Urbana; Indicadores Socioeconômicos; Censos; '
                           'Desigualdades em Saúde'),
        ('Universidade/Curso de Graduação', 'Pontifícia Universidade Católica de Minas Gerais / Ciência de Dados & '
                                            'Inteligência Artificial.'),
    ]
    for rotulo, valor in campos:
        p(f'**{rotulo}:** {valor}', 'Capa_Campo')
    p('Belo Horizonte, 12 de outubro de 2026.', 'Capa_Data')

    # ── II. INTRODUÇÃO ─────────────────────────────────────────────────────────────────
    h1('II. INTRODUÇÃO', 'H1_NovaPagina')
    # Plano de trabalho, "Justificativa" (literal; correções em NOTAS_PARA_ORIENTADORA.md)
    cat('G_Copia')
    p('O envelhecimento populacional e a urbanização configuram tendências globais, com projeções de '
      'crescimento acentuadas especialmente em países de renda baixa e média, como o Brasil (Agero ^^et al.^^, '
      '2020; IBGE, 2022). O aumento da população idosa suscita preocupações quanto à capacidade dos sistemas '
      'de saúde, de planejamento urbano e à organização social em responder adequadamente a essa nova demanda '
      '(Kalache; Gatti, 2020). Nesse contexto, indicadores que incorporem variáveis sociais e ambientais são '
      'ferramentas importantes no planejamento de políticas públicas (Passarelli-Araujo, 2023; Gioia et al., '
      '2020; Allik et al., 2020).')
    p('O contexto socioeconômico e as características do espaço urbano são determinantes centrais da saúde '
      'das populações, uma vez que os atributos físicos e sociais das cidades podem atuar como exposições que '
      'influenciam positiva ou negativamente a saúde dos indivíduos. A incorporação de variáveis '
      'socioeconômicas e territoriais é essencial para a compreensão do processo saúde-doença e para o '
      'aprimoramento das políticas públicas (Caiaffa et al., 2021; Buss; ^^Pellegrini^^ Filho, 2007). A construção '
      'de indicadores sínteses, em escala intraurbana, pode contribuir ^^para^^ as evidências empíricas sobre '
      'desigualdades e determinantes de saúde nas cidades (Passarelli-Araujo, 2023; Gioia et al., 2020; '
      'Allik et al., 2020).')
    # texto novo: liga a justificativa ao objetivo e ao recorte do relatório
    cat('G_Revisado')
    p('Este projeto toma como referência o Índice de Vulnerabilidade da Saúde (IVS) de 2012, criado pela '
      'Secretaria Municipal de Saúde de Belo Horizonte (SMS, 2013), e propõe reconstruí-lo com os dados do Censo '
      'Demográfico 2022 para os setores censitários dos 70 municípios da amostra do Estudo Longitudinal da Saúde '
      'dos Idosos Brasileiros (ELSI-Brasil). Este relatório cobre o trabalho feito até outubro de 2026: a montagem '
      'da base de dados, o cálculo dos indicadores e a análise exploratória. A análise fatorial começou nesse '
      'período e está em desenvolvimento.')

    # ── III. OBJETIVOS (Plano de trabalho, literal) ────────────────────────────────────
    h1('III. OBJETIVOS')
    cat('G_Copia')
    h2('Objetivo geral')
    p('Avaliar as desigualdades intraurbanas por meio da construção de um Índice de Vulnerabilidade à Saúde '
      '(IVS) de cidades brasileiras.')
    h2('Objetivos específicos')
    p('^^1.^^\tConstruir um Índice de Vulnerabilidade à Saúde (IVS) intraurbano com dados do censo demográfico '
      '2022 de um conjunto de cidades brasileiras.', 'Lista')
    p('^^2.^^\tAnalisar a distribuição espacial do IVS.', 'Lista')

    # ── IV. METODOLOGIA ────────────────────────────────────────────────────────────────
    h1('IV. METODOLOGIA')
    # Plano de trabalho, "Metodologia" (literal; correções em NOTAS_PARA_ORIENTADORA.md)
    cat('G_Copia')
    p('Estudo ecológico com dados dos agregados por setores censitários do censo demográfico 2022 (básico, '
      'população, domicílio e rendimento) de municípios brasileiros selecionados (IBGE, 2022). Serão '
      'selecionados os 70 municípios ^^que^^ compõem a amostra do Estudo Longitudinal da Saúde dos Idosos '
      'Brasileiros (ELSI-Brasil) que avaliou adultos com 50 anos ou mais residentes na comunidade '
      '(https://elsi.cpqrr.fiocruz.br/amostra/).')
    p('As variáveis serão obtidas em nível de setor censitário que corresponde ^^à^^ menor unidade territorial, '
      'formada por área contínua, integralmente contida em área urbana ou rural, com dimensão adequada à '
      'operação de pesquisas (IBGE, 2011).')
    p('O IVS para o conjunto de cidades brasileiras será construído com base nas variáveis que estão '
      'disponíveis no censo demográfico de 2022 e ^^compõem^^ o IVS de 2012 elaborado pela Secretaria Municipal '
      'de Saúde de Belo Horizonte, cujo objetivo foi evidenciar as desigualdades no perfil epidemiológico de '
      'grupos sociais distintos e propiciar a identificação de áreas com condições socioeconômicas '
      'desfavoráveis dentro do espaço urbano (SMS, 2013). As variáveis são apresentadas no Quadro 1.')
    legenda('Quadro 1 – Variáveis selecionadas do censo demográfico de 2022.')
    q1 = [
        ['Saneamento', 'Percentual de domicílios particulares permanentes com abastecimento de água '
                       'inadequado ou ausente'],
        ['Saneamento', 'Percentual de domicílios particulares permanentes com esgotamento sanitário '
                       'inadequado ou ausente'],
        ['Saneamento', 'Percentual de domicílios particulares permanentes com destino do lixo de forma '
                       'inadequada ou ausente'],
        ['Socioeconômica', 'Razão de moradores por domicílio'],
        ['Socioeconômica', 'Percentual de pessoas analfabetas'],
        ['Socioeconômica', 'Rendimento nominal mensal médio das pessoas responsáveis'],
        ['Socioeconômica', 'Percentual de pessoas de raça/cor preta, parda e indígena'],
    ]
    tabela('Quadro1', [3.6, 13.4], ['Dimensão', 'Variável'], q1, grade=True, mesclar_col0=True,
           cat_cab='G_Gerado')  # o cabeçalho do quadro não existe no Plano
    cat('G_Gerado')
    fonte('Fonte: SMS (2013).')
    cat('G_Copia')
    p('A técnica de análise fatorial será utilizada para evidenciar a relação entre as variáveis (Matos; '
      'Rodrigues, 2019). Serão realizadas análises descritivas com medidas de frequências, medidas de '
      'tendência central (média) e dispersão (desvio padrão). As técnicas para Geoprocessamento serão '
      'realizadas por meio do software Qgis 2.10.1 (https://qgis.org/pt_BR/site/).')
    p('Este estudo será realizado de acordo com a Resolução 510/2016 do Conselho Nacional ^^de^^ Saúde, art. 1°, '
      'II e III, que indicam que para as informações de domínio público, acesso público e preservação de '
      'dados não há necessidade de submissão ao Conselho de Ética, sendo assim, atendendo os preceitos éticos '
      'de pesquisa, nos termos ^^da Lei 13.709/2018^^ – Lei Geral de Proteção de Dados Pessoais (LGPD) '
      'respeitando diretrizes e normas das pesquisas envolvendo seres humanos.')

    # texto novo: o que foi executado e como o Censo 2022 obrigou a adaptar o IVS de 2012
    cat('G_Revisado')
    h2('Procedimentos executados e adequações ao Censo Demográfico 2022')
    # números: EDA §2–3.4 (109.032; 1.736; 1.015; 0; 106.281; 2.173 = 2,04%; 104.108)
    p('A base reúne os arquivos dos agregados por setores censitários do Censo Demográfico 2022 '
      'para os 109.032 setores dos 70 municípios do ELSI-Brasil (Lima-Costa et al., 2018). Como no '
      'IVS de 2012, cada setor foi classificado quanto à participação na análise. Saíram 1.736 setores sem '
      'moradores e 1.015 setores em que o IBGE suprimiu, por sigilo, a população ou o número de domicílios. '
      'Nenhum setor foi classificado como formado apenas por domicílios coletivos. Dos 106.281 setores restantes, '
      'saíram também os 2.173 setores rurais (2,04%), porque o índice é intraurbano. Ficaram 104.108 setores '
      'urbanos, que formam o recorte de análise.')
    # EDA §4.3 (15+), §4.4 e §4.4.1 (V06004; setor 310620005650366, SUSPEITO = extremo e incoerente),
    # §3.1 e §14.3 (sigilo parcial), GUIA (caçamba)
    p('Para usar o Censo 2022 nas variáveis do Quadro 1, foram necessárias cinco adequações:')
    p('(a)\tDenominador: os indicadores domiciliares usam o número de domicílios particulares permanentes '
      'ocupados (V00001), equivalente ao de 2012. A exceção é a razão de moradores, cujo denominador inclui os '
      'domicílios improvisados. Os moradores de domicílios coletivos entram nos indicadores de cor/raça, idosos '
      'e crianças, mas não nos indicadores domiciliares.', 'Lista_Letra')
    p('(b)\tAnalfabetismo: calculado para as pessoas de 15 anos ou mais, porque os agregados por setor de 2022 '
      'não têm dados de alfabetização abaixo dessa idade. No IVS de 2012, a referência era a população de 5 anos '
      'ou mais.', 'Lista_Letra')
    p('(c)\tRenda: rendimento nominal médio mensal das pessoas responsáveis com rendimento (V06004), já '
      'calculado pelo IBGE. Na análise descritiva foi retirado só o setor de maior renda da base, um setor de '
      'favela de Belo Horizonte com média de R$ 170.418,06, valor incoerente com o perfil do próprio setor. Os '
      'demais valores extremos ficaram na base.', 'Lista_Letra')
    p('(d)\tSigilo: quando o IBGE suprimiu todas as parcelas de um numerador, o indicador ficou ausente, nunca '
      'zero. Quando suprimiu só parte delas, essas parcelas entraram na soma como zero, o que subestima os '
      'indicadores de saneamento e de cor/raça (na água, a média real pode ser até 14,9% maior que a '
      'observada).', 'Lista_Letra')
    p('(e)\tLixo: o depósito em caçamba continua classificado como destino inadequado, como no IVS de 2012 '
      '(SMS, 2013).', 'Lista_Letra')
    p('Além das sete variáveis do Quadro 1, foram calculados indicadores complementares para descrever os '
      'setores. Cinco deles entram nesta análise (Quadro 2): domicílios sem água canalizada até o interior, sem '
      'banheiro de uso exclusivo e em moradia não convencional, e as proporções de idosos (60 anos ou mais) e de '
      'crianças (0 a 14 anos) na população. Idosos e crianças são o numerador e o denominador do índice de '
      'envelhecimento populacional (Galvão et al., 2025).')
    cat('G_Gerado')
    legenda('Quadro 2 – Indicadores analisados, por dimensão.')
    por_dim = QUADRO2['Dimensão'].value_counts()
    q2 = [[f"{x['Dimensão']} ({por_dim[x['Dimensão']]})", x['Indicador'], x['O que mede'], x['IVS-7']]
          for _, x in QUADRO2.iterrows()]
    tabela('Quadro2', [2.9, 3.9, 8.4, 1.8], ['Dimensão', 'Indicador', 'O que mede', 'Compõe o IVS'], q2,
           grade=True, mesclar_col0=True)
    fonte('Fonte: elaborado pelo autor a partir de IBGE (2022).')
    cat('G_Revisado')
    p('A análise exploratória usou média, mediana, percentil 75, valor máximo, coeficiente de assimetria e '
      'percentual de setores com valor zero. Como a maioria dos setores tem zero nos indicadores de saneamento, a '
      'dispersão foi descrita pelo percentil 75 e pela assimetria, que nesse caso informam mais do que o desvio '
      'padrão. Também foram analisados os dados faltantes e as diferenças entre regiões. A relação entre os '
      'indicadores foi medida pela correlação de Spearman, adequada a distribuições assimétricas, nos setores com '
      'os 12 indicadores completos. A renda entra com sinal invertido, para que valores maiores indiquem mais '
      'vulnerabilidade. O processamento foi feito em Python, e os mapas temáticos serão feitos '
      'no QGIS 3.x, versão atual do software previsto no projeto.')

    # ── V. OBJETIVOS ALCANÇADOS ────────────────────────────────────────────────────────
    h1('V. OBJETIVOS ALCANÇADOS DO SUBPROJETO DO BOLSISTA')
    p('**Objetivo específico 1** (construir o IVS intraurbano): em andamento. A base dos 70 municípios está '
      'montada, os sete indicadores do Quadro 1 e os complementares estão calculados e a análise exploratória '
      'está concluída (seção VI). A análise fatorial, que vai orientar a ponderação das variáveis, já se iniciou. '
      'Faltam a padronização das variáveis, a definição dos pesos e o cálculo final do índice.')
    p('**Objetivo específico 2** (analisar a distribuição espacial do IVS): a iniciar. Depende do índice final, '
      'e os mapas temáticos passaram para a próxima etapa.')

    # ── VI. RESULTADOS ─────────────────────────────────────────────────────────────────
    h1('VI. RESULTADOS')
    h2('Recorte analisado')
    # EDA Sumário (52,1 mi no recorte), §2 (Sudeste 61.989), §11 e A6/T35 (26,0% = 52.732.704 / 203.080.756;
    # 30,0% = 104.108 / 347.400), §12.10 (validação: população e IEP nacionais)
    p('O recorte de análise tem 104.108 setores urbanos e 52,1 milhões de moradores. O Sudeste representa '
      '61.989 desses setores (59,5%), e por isso médias simples entre setores pesam mais para as grandes cidades '
      'dessa região. Considerados por inteiro, com 52,7 milhões de habitantes, os 70 municípios representam 26,0% da '
      'população do país e 30,0% dos setores urbanos elegíveis do país. Para conferir o processamento, as mesmas '
      'rotinas foram aplicadas aos 468.099 setores do Brasil e reproduziram a população oficial do Censo 2022 '
      '(203.080.756 pessoas) e o índice de envelhecimento nacional publicado pelo IBGE (79,99, contra 80,0).')

    h2('Distribuição dos indicadores')
    renda_med, renda_mediana = t1('renda_media_sem_extremo', 'Média'), t1('renda_media_sem_extremo', 'Mediana')
    a_mais = br((float(renda_med.replace('.', '').replace(',', '.'))
                 / float(renda_mediana.replace('.', '').replace(',', '.')) - 1) * 100, 0)
    p('A Tabela 1 resume os 12 indicadores. Os três indicadores de saneamento do IVS têm mediana zero. Em '
      f'{z("pct_agua_inad")} dos setores, nenhum domicílio com abastecimento de água inadequado foi registrado; '
      f'para o esgoto, o percentual de setores com zero é de {z("pct_esgoto_inad")} e, para o lixo, de '
      f'{z("pct_lixo_inad")}. Parte desses zeros vem de parcelas suprimidas pelo IBGE (item d da seção IV). Nos '
      'indicadores complementares de infraestrutura, os zeros são ainda mais frequentes em sem banheiro '
      f'({z("pct_sem_banheiro")}) e moradia não convencional ({z("pct_moradia_nao_convencional")}); em sem água '
      f'canalizada, ficam em {z("pct_sem_agua_canalizada")}. Os três têm assimetria alta: '
      f'{t1("pct_sem_banheiro", "Assim.")}, {t1("pct_moradia_nao_convencional", "Assim.")} e '
      f'{t1("pct_sem_agua_canalizada", "Assim.")}, respectivamente. A renda do responsável também é assimétrica, '
      f'com média (R$ {renda_med}) {a_mais}% acima da mediana (R$ {renda_mediana}). Já a razão de moradores, a '
      f'cor/raça e os grupos etários têm assimetria baixa, entre {t1("pct_raca_pretpardind", "Assim.")} e '
      f'{t1("pct_idoso_60mais", "Assim.")}. Em média, idosos são '
      f'{br(float(t1("pct_idoso_60mais", "Média").replace(",", ".")) * 100, 1)}% e crianças '
      f'{br(float(t1("pct_pop_0a14", "Média").replace(",", ".")) * 100, 1)}% da população dos setores.')
    cat('G_Gerado')
    legenda('Tabela 1 – Estatísticas descritivas dos indicadores nos setores urbanos dos 70 municípios do '
            'ELSI-Brasil, Censo Demográfico 2022.')
    linhas = [[x['Indicador'], x['n'], x['Média'], x['Mediana'], x['p75'], x['Máx'], x['Assim.']]
              for _, x in TAB1.iterrows()]
    tabela('Tabela1', [5.0, 1.9, 1.9, 1.9, 1.9, 2.3, 1.5],
           ['Indicador', 'n', 'Média', 'Mediana', 'p75', 'Máx', 'Assim.'], linhas, numericas={1, 2, 3, 4, 5, 6})
    fonte('Fonte: elaborado pelo autor a partir de IBGE (2022). Nota: valores em proporção (0 a 1), exceto a '
          'razão de moradores (moradores por domicílio) e a renda (R$). n = setores com o dado; os valores '
          'ausentes decorrem de sigilo do IBGE. Renda sem o setor com valor extremo (R$ 170.418,06). '
          'p75 = percentil 75; Assim. = coeficiente de assimetria.')
    cat('G_Revisado')

    h2('Dados faltantes e sigilo')
    # EDA §8 e §14.1 (84,10%; média observada 3,64%; 3,14% com V00901 = 1 em cada setor suprimido).
    # Medianas recalculadas no .db na base sem o setor extremo (a da Tabela 1): R$ 2.313,87 × R$ 6.092,84.
    cob_banheiro = br(int(n('pct_sem_banheiro').replace('.', '')) / 104_108 * 100, 1)
    p('Seis dos sete indicadores do IVS têm dados para mais de 99,98% dos setores. A exceção é o analfabetismo, '
      f'disponível em {n("pct_analfab")} setores (84,10%): nos demais, o IBGE suprimiu o número de analfabetos '
      'por sigilo. A supressão acontece quando há poucos analfabetos no setor, e esses setores têm renda mais '
      'alta: a renda mediana do responsável é de R$ 2.313,87 onde há o dado e de R$ 6.092,84 onde não há. Por '
      'isso, a média observada (3,64%) tende a superestimar a real. Atribuindo a cada setor suprimido o menor '
      'valor possível, um analfabeto, a média cairia para 3,14%; a média real deve ficar entre esses dois valores. Entre '
      'os complementares, o sigilo afeta sobretudo a ausência de banheiro, disponível em '
      f'{n("pct_sem_banheiro")} setores ({cob_banheiro}%).')

    h2('Diferenças regionais')
    # EDA §2 (Norte: 6 municípios) e §5 (médias entre setores por região); Brasília: pecas.json (centro_oeste)
    co = PECAS['centro_oeste']
    p('As médias por região são mais altas no Norte e mais baixas no Sul em quatro indicadores: água, esgoto, '
      'razão de moradores e cor/raça. A proporção de domicílios com abastecimento de água inadequado é 16 vezes '
      'maior no Norte (0,323) do que no Sul (0,020); a de esgoto inadequado, 8 vezes (0,238 contra 0,029); e a '
      'de pessoas pretas, pardas ou indígenas, três vezes (0,748 contra 0,246). A renda é mais baixa no Norte e '
      f'no Nordeste, mas a maior média é a do Centro-Oeste, onde Brasília reúne {br(co["brasilia"], 0)} dos '
      f'{br(co["setores"], 0)} setores. O analfabetismo tem pico no Nordeste (0,062), e o lixo inadequado não '
      'segue o padrão: as médias regionais vão de 0,091 a 0,154, com Norte e Sul praticamente iguais. Como o '
      'Norte tem 6 municípios na amostra, esses contrastes descrevem os municípios estudados, e não as regiões '
      'como um todo.')

    h2('Correlação entre os indicadores')
    A, E, L, M, AN = 'pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad', 'razao_moradores', 'pct_analfab'
    RE, PPI, CAN, BAN = 'renda_media_sem_extremo', 'pct_raca_pretpardind', 'pct_sem_agua_canalizada', 'pct_sem_banheiro'
    MNC, ID, CR = 'pct_moradia_nao_convencional', 'pct_idoso_60mais', 'pct_pop_0a14'
    ivs = [A, E, L, M, AN, RE, PPI]
    lixo = [R[L][c] for c in ivs if c != L]
    mnc = max(abs(R[MNC][c]) for c in R if c != MNC)
    rob = PECAS['robustez_figura1']  # pares completos e postos dentro do município (pecas_relatorio_raic.py)

    def rp(a: str, b: str) -> str:
        return br(rob['pares'][f'{a}|{b}'], 2)

    def ri(a: str, b: str) -> str:
        return br(rob['intra'][f'{a}|{b}'], 2)

    cat('G_Gerado')
    legenda(f'Figura 1 – Correlação de Spearman entre os indicadores nos setores urbanos dos 70 municípios do '
            f'ELSI-Brasil (n = {br(N_FIG, 0)} setores com dados completos).')
    figura(PASTA / 'figuras' / 'fig1_correlacao.png', 12.5)
    fonte('Fonte: elaborado pelo autor a partir de IBGE (2022).')
    cat('G_Revisado')
    p(f'A Figura 1 mostra a correlação de Spearman entre os 12 indicadores nos {br(N_FIG, 0)} setores com '
      'todos os dados, o que deixa de fora sobretudo os setores com sigilo no analfabetismo ou na ausência de '
      'banheiro. O coeficiente entre idosos e renda invertida quase não muda quando se usam todos os setores '
      f'disponíveis para cada par ({rp(ID, RE)}) nem quando a correlação é calculada dentro de cada município '
      f'({ri(ID, RE)}).')
    p(f'Renda, cor/raça e analfabetismo formam um bloco: renda invertida × cor/raça {r(RE, PPI)}, renda invertida × '
      f'analfabetismo {r(AN, RE)} e analfabetismo × cor/raça {r(AN, PPI)}. Água e esgoto inadequados têm '
      f'correlação moderada ({r(A, E)}), que cai para {ri(A, E)} dentro dos municípios: a associação vem sobretudo '
      f'das diferenças entre cidades. A falta de água canalizada acompanha a água inadequada ({r(A, CAN)}). O lixo '
      f'inadequado tem correlações fracas com os demais indicadores do IVS (de {br(min(lixo), 2)} a '
      f'{br(max(lixo), 2)}), e a moradia não convencional é praticamente independente de todos (no máximo '
      f'{br(mnc, 2)} em valor absoluto).')
    p('Os grupos etários vão em direções opostas. A proporção de idosos tem correlação negativa com os demais '
      f'indicadores ({r(ID, RE)} com a renda invertida e {r(ID, PPI)} com a cor/raça; com a moradia não '
      f'convencional, praticamente nula). A de crianças tem correlação positiva ({r(CR, RE)} com a renda '
      f'invertida e {r(CR, M)} com a razão de moradores). Entre si, as duas têm {r(ID, CR)}, em parte por '
      'construção, já que dividem o mesmo denominador.')

    h2('Discussão dos resultados')
    p('Três achados da análise exploratória mudam o cálculo do índice. O primeiro é a combinação de muitos '
      'zeros no saneamento com forte assimetria no saneamento e na renda: com ela, uma padronização min-max comprimiria a '
      'maioria dos setores numa faixa estreita da escala, e a assimetria terá de ser tratada antes do cálculo, '
      'por método ainda a definir. A padronização será feita dentro de cada município, como no IVS de 2012, '
      'calculado para um único município, e de acordo com o caráter intraurbano do índice. O segundo é o sigilo '
      'do analfabetismo, concentrado nos setores de melhor condição: excluir esses setores enviesaria o índice, o '
      'que exige um tratamento próprio para os valores ausentes. O terceiro é a estrutura das correlações. Renda, '
      'cor/raça e analfabetismo parecem medir uma mesma dimensão socioeconômica, enquanto o lixo inadequado, '
      'pouco ligado aos demais indicadores, pode refletir mais a forma de coleta (a caçamba) do que a '
      'vulnerabilidade, hipótese ainda a verificar. A análise fatorial vai testar essa estrutura e orientar a '
      'ponderação (Matos; Rodrigues, 2019).')
    p('A relação inversa entre idosos e os indicadores de vulnerabilidade é compatível com um envelhecimento mais '
      'avançado nos setores de melhor condição socioeconômica; nos de pior condição, as crianças são uma fatia maior '
      f'da população. O padrão aparece dentro das próprias cidades: em {rob["municipios_idoso_renda_negativa"]} '
      f'dos {rob["municipios_30mais"]} municípios com pelo menos 30 setores completos, a correlação entre idosos e '
      'renda invertida é negativa. Médias municipais esconderiam essa diferença, o que mostra o valor de '
      'indicadores em escala intraurbana (Passarelli-Araujo, 2023; Gioia et al., 2020; Allik et al., 2020).')

    h2('Início da análise fatorial')
    p('A análise fatorial, prevista no projeto para evidenciar a relação entre as variáveis (Matos; '
      'Rodrigues, 2019), começou entre agosto e setembro de 2026, com os testes de adequação da matriz de '
      'correlação e a comparação de métodos de extração e de rotação. Os resultados ainda são preliminares, estão '
      'em discussão com a orientadora e serão apresentados no relatório final.')

    # ── VII. CONCLUSÕES ────────────────────────────────────────────────────────────────
    h1('VII. CONCLUSÕES')
    item('Com o Censo Demográfico 2022, as sete variáveis do Quadro 1 foram calculadas para 104.108 setores '
         'urbanos dos 70 municípios do ELSI-Brasil, com as adequações documentadas. O processamento foi conferido '
         'com a população e o índice de envelhecimento oficiais do IBGE.')
    item('Saneamento e infraestrutura domiciliar têm valor zero na maioria dos setores e distribuição muito '
         'assimétrica, assim como a renda. Isso pede cuidado na padronização.')
    item('O sigilo do IBGE retira o dado de analfabetismo de 15,9% dos setores, sobretudo dos de renda mais '
         'alta, o que exige um tratamento próprio para os valores ausentes.')
    item('Renda, cor/raça e analfabetismo andam juntos, e o lixo inadequado se comporta de forma independente. '
         'A análise fatorial em curso vai testar essa estrutura.')
    item('A estrutura etária acompanha as condições socioeconômicas, também dentro das cidades: há mais idosos '
         'nos setores de melhor condição socioeconômica e mais crianças nos de pior condição.')

    # ── BIBLIOGRAFIA (Plano de trabalho + novas; ordem alfabética) ───────────────────────
    h1('BIBLIOGRAFIA')
    for ref in [
        'AGERO, P. ~~et al.~~ Desafios do envelhecimento populacional e políticas públicas. **^^Rev. Bras. '
        'Geriatr. Gerontol.^^**, Rio de Janeiro, v. 23, n. 4, p. 1–12, 2020.',
        'ALLIK, M. ~~et al.~~ **Developing a small-area deprivation measure for Brazil**. Glasgow: University '
        'of Glasgow, 2020.',
        'BRASIL. Conselho Nacional de Saúde. Resolução nº 510, de 7 de abril de 2016. **Diário Oficial da '
        'União**: seção 1, Brasília, DF, 24 maio 2016.',
        'BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). '
        '**Diário Oficial da União**: seção 1, Brasília, DF, 15 ago. 2018.',
        'BUSS, P. M.; PELLEGRINI FILHO, ^^A.^^ A saúde e seus determinantes sociais. **Physis: Revista de Saúde '
        'Coletiva**, v. 17, n. 1, p. 77–93, jan. 2007.',
        'CAIAFFA, W. T. ~~et al.~~ **Saúde urbana, cidades e a interseção de sistemas: panorama, agendas, gaps '
        'e oportunidades rumo à equidade, sustentabilidade, resiliência e promoção à saúde**. Rio de Janeiro: '
        'Fiocruz, 2021. 34 p.',
        'GALVÃO, S. M. ~~et al.~~ Envelhecimento populacional em Mato Grosso e sua relação com indicadores '
        'demográficos e econômicos. **Hygeia: Revista Brasileira de Geografia Médica e da Saúde**, v. 21, '
        'e2106, 2025.',
        'GIOIA, T. B.; PEREIRA, A. C. F.; RAMINELLI, J. A. Avaliação de métodos para construção de um índice de '
        'vulnerabilidade de saúde para Londrina-PR. **^^Hygeia: Revista Brasileira de Geografia Médica e da '
        'Saúde^^**, v. 16, p. 282–298, 2020.',
        'INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Sinopse do censo 2010 e resultados '
        'preliminares do universo**. Rio de Janeiro: IBGE, 2011.',
        'INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Censo demográfico 2022**. ^^Rio de Janeiro: IBGE, '
        '2022.^^ Disponível em: '
        'https://www.ibge.gov.br/estatisticas/sociais/trabalho/22827-censo-demografico-2022.html. Acesso em: '
        '30 jan. 2026.',
        'KALACHE, A.; GATTI, A. A. Envelhecimento ativo: um paradigma para o século XXI. **^^Rev. Bras. Geriatr. '
        'Gerontol.^^**, Rio de Janeiro, v. 23, n. 1, p. e200325, 2020.',
        'LIMA-COSTA, M. F. ~~et al.~~ The Brazilian Longitudinal Study of Aging (ELSI-Brazil): objectives and '
        'design. **American Journal of Epidemiology**, v. 187, n. 7, p. 1345–1353, 2018.',
        'MATOS, D. A. S.; RODRIGUES, E. C. **Análise fatorial**. Brasília: Enap, 2019. 74 p.',
        'PASSARELLI-ARAUJO, H. Mapeando as disparidades socioeconômicas de saúde urbana: um estudo comparativo '
        'entre seis capitais brasileiras. **Revista Brasileira de Estudos de População**, [S. l.], v. 40, '
        'p. 1–25, 2023. DOI: 10.20947/S0102-3098a0251.',
        'SMS - Secretaria Municipal de Saúde. **Índice de vulnerabilidade da saúde.** Belo Horizonte: '
        'Secretaria Municipal de Saúde, 2013. 15 p.',
    ]:
        cat('G_Gerado' if ref.startswith(('BRASIL.', 'GALVÃO', 'LIMA-COSTA')) else 'G_Copia')
        p(ref, 'Referencia')

    # ── blocos sem numeração do Anexo 1 ───────────────────────────────────────────────
    h1('MATÉRIA ENCAMINHADA PARA PUBLICAÇÃO')
    cat('G_Revisado')
    p('Nenhuma matéria foi encaminhada para publicação até o momento.')

    h1('PERSPECTIVAS PARA O TRABALHO')
    for x in [
        'Tratar a assimetria dos indicadores de saneamento e da renda e padronizar as variáveis.',
        'Concluir a análise fatorial e definir, com a minha professora orientadora, a ponderação das variáveis.',
        'Calcular o IVS e classificar os setores censitários pelo grau de vulnerabilidade.',
        'Fazer os mapas temáticos no QGIS 3.x e analisar a distribuição espacial do IVS.',
        'Revisar dois pontos de operacionalização: o universo da renda (V06004, restrito aos responsáveis com '
        'rendimento) e a classificação da caçamba como destino inadequado do lixo.',
        'Submeter resumos a congressos, redigir o artigo científico e elaborar o relatório final.',
    ]:
        item(x)

    # texto do Pedro (edição no Word, 11/10); só a pontuação foi ajustada
    h1('OUTRAS ATIVIDADES DESENVOLVIDAS NO PERÍODO')
    cat(None)
    item('Reuniões semanais com a orientadora para discussão do delineamento e da condução do projeto, de março '
         'a outubro de 2026.')
    item('Participação no Programa de Inserção do IRR e no Curso Introdutório para Bolsistas do Programa de '
         'Iniciação Científica da Fiocruz Minas, de março a abril de 2026.')

    h1('AVALIAÇÃO')
    # texto do Pedro (12/10), só com "científica" e "minha orientadora" corrigidos
    p('A iniciação científica tem sido minha primeira experiência de pesquisa com dados reais de saúde pública e '
      'imersão no mundo da estatística. Vindo da graduação em Ciência de Dados e Inteligência Artificial, aprendi '
      'que trabalhar com o Censo 2022 exige mais do que saber programar. Cada decisão muda o resultado e precisa '
      'ser justificada e registrada: o denominador de um indicador, a exclusão dos setores rurais, o tratamento do '
      'sigilo do IBGE. As reuniões semanais com a minha orientadora foram o centro desse aprendizado, porque cada '
      'questão discutida virou uma decisão metodológica documentada. Também passei a conhecer a literatura '
      'científica, que eu ainda não tinha estudado.')
    # proposta de crítica e sugestão (o Anexo 1 pede as duas) — o Pedro troca pelas palavras dele
    cat('G_Revisado')
    p('Como crítica, o cronograma do plano subestimou o tempo necessário para preparar e conferir a base de dados, '
      'e por isso os mapas ficaram para a próxima etapa. Como sugestão, o programa poderia oferecer oficinas sobre '
      'bases de dados públicas e métodos quantitativos para bolsistas que chegam de outras áreas.')
    cat(None)

    h1('APOIO')
    p('FAPEMIG')

    h1('OBSERVAÇÃO')
    cat('G_Revisado')
    p('Os objetivos definidos no projeto não mudaram. As adequações metodológicas exigidas pelo Censo '
      'Demográfico 2022 são apresentadas na seção IV.')


# ══════════════════════════════════════════════════════════════════════════════════════
# ESTILOS E MONTAGEM
# ══════════════════════════════════════════════════════════════════════════════════════
NS = ('xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
      'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
      'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
      'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
      'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
      'xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" '
      'xmlns:xlink="http://www.w3.org/1999/xlink" '
      'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"')

FONTE = 'style:font-name="Times New Roman"'
BORDA = '0.75pt solid #000000'
FINA = '0.5pt solid #000000'


def ps(nome: str, par: str = '', txt: str = '', pai: str = 'Standard', extra: str = '') -> str:
    """Estilo de parágrafo."""
    return (f'<style:style style:name="{nome}" style:family="paragraph" style:parent-style-name="{pai}"{extra}>'
            f'<style:paragraph-properties {par}/><style:text-properties {txt}/></style:style>')


def estilos() -> str:
    return ''.join([
        '<style:default-style style:family="paragraph">'
        f'<style:text-properties {FONTE} fo:font-size="12pt" fo:language="pt" fo:country="BR"/></style:default-style>',
        '<style:style style:name="Standard" style:family="paragraph" style:class="text"><style:paragraph-properties '
        'fo:margin-top="0cm" fo:margin-bottom="0cm" fo:line-height="100%"/></style:style>',
        ps('Corpo', 'fo:text-align="justify" fo:text-indent="1.25cm" fo:margin-bottom="0.12cm" fo:line-height="108%"'),
        '<style:style style:name="Lista" style:family="paragraph" style:parent-style-name="Standard"><style:paragraph-properties '
        'fo:text-align="justify" fo:margin-left="0.9cm" fo:text-indent="-0.5cm" fo:margin-bottom="0.12cm" fo:line-height="108%">'
        '<style:tab-stops><style:tab-stop style:position="0cm"/></style:tab-stops></style:paragraph-properties></style:style>',
        # itens (a)–(e): o rótulo "(a)" é mais largo que o recuo da lista de marcadores
        '<style:style style:name="Lista_Letra" style:family="paragraph" style:parent-style-name="Standard"><style:paragraph-properties '
        'fo:text-align="justify" fo:margin-left="1.25cm" fo:text-indent="-0.75cm" fo:margin-bottom="0.12cm" fo:line-height="108%">'
        '<style:tab-stops><style:tab-stop style:position="0cm"/></style:tab-stops></style:paragraph-properties></style:style>',
        ps('Heading_20_1', 'fo:margin-top="0.45cm" fo:margin-bottom="0.22cm" fo:keep-with-next="always"',
           'fo:font-size="12pt" fo:font-weight="bold"',
           extra=' style:display-name="Heading 1" style:next-style-name="Corpo" style:default-outline-level="1" style:class="text"'),
        ps('Heading_20_2', 'fo:margin-top="0.3cm" fo:margin-bottom="0.15cm" fo:keep-with-next="always"',
           'fo:font-size="12pt" fo:font-weight="bold" fo:font-style="italic"',
           extra=' style:display-name="Heading 2" style:next-style-name="Corpo" style:default-outline-level="2" style:class="text"'),
        ps('Legenda', 'fo:margin-top="0.25cm" fo:margin-bottom="0.12cm" fo:keep-with-next="always" fo:text-align="justify"',
           'fo:font-size="11pt"'),
        ps('Fonte_Nota', 'fo:margin-top="0.08cm" fo:margin-bottom="0.3cm" fo:text-align="justify"', 'fo:font-size="10pt"'),
        ps('Figura', 'fo:text-align="center" fo:keep-with-next="always"'),
        ps('Tab_Texto', 'fo:text-align="start"', 'fo:font-size="10pt"'),
        ps('Tab_Num', 'fo:text-align="end"', 'fo:font-size="10pt"'),
        ps('Tab_Cab', 'fo:text-align="start"', 'fo:font-size="10pt" fo:font-weight="bold"'),
        ps('Tab_CabNum', 'fo:text-align="end"', 'fo:font-size="10pt" fo:font-weight="bold"'),
        ps('Referencia', 'fo:text-align="start" fo:margin-bottom="0.3cm"'),
        ps('Capa_Instituicao', 'fo:text-align="center" fo:margin-bottom="0.3cm"', 'fo:font-weight="bold"'),
        ps('Capa_Centro', 'fo:text-align="center" fo:margin-bottom="2.2cm"'),
        ps('Capa_Titulo', 'fo:text-align="center" fo:margin-bottom="2.2cm" fo:line-height="130%"',
           'fo:font-size="14pt" fo:font-weight="bold"'),
        ps('Capa_Campo', 'fo:text-align="start" fo:margin-bottom="0.32cm" fo:line-height="108%"'),
        ps('Capa_Data', 'fo:text-align="center" fo:margin-top="2cm"'),
        ps('Rodape', 'fo:text-align="center"', 'fo:font-size="10pt"'),
        '<style:style style:name="Negrito" style:family="text"><style:text-properties fo:font-weight="bold"/></style:style>',
        '<style:style style:name="Italico" style:family="text"><style:text-properties fo:font-style="italic"/></style:style>',
        *([f'<style:style style:name="{e}" style:family="text"><style:text-properties fo:background-color="{c}"/>'
            '</style:style>' for e, (c, _) in GRIFOS.items()] if GRIFAR else []),
        *(['<style:style style:name="G_Corr_Negrito" style:family="text"><style:text-properties '
           f'fo:background-color="{GRIFOS["G_Corr"][0]}" fo:font-weight="bold"/></style:style>'] if GRIFAR else []),
        '<style:style style:name="Pendente" style:family="text"><style:text-properties fo:background-color="#FFFF00" fo:font-weight="bold"/></style:style>',
    ])


def automaticos() -> str:
    def cel(nome: str, bordas: str, fundo: str = '') -> str:
        return (f'<style:style style:name="{nome}" style:family="table-cell"><style:table-cell-properties '
                f'fo:padding-top="0.06cm" fo:padding-bottom="0.06cm" fo:padding-left="0.12cm" fo:padding-right="0.12cm" '
                f'style:vertical-align="middle" {bordas} {fundo}/></style:style>')
    return ''.join([
        '<style:page-layout style:name="pm_capa"><style:page-layout-properties fo:page-width="21cm" fo:page-height="29.7cm" '
        'style:print-orientation="portrait" fo:margin-top="2.5cm" fo:margin-bottom="2cm" fo:margin-left="2.5cm" fo:margin-right="2.5cm"/>'
        '</style:page-layout>',
        '<style:page-layout style:name="pm_texto"><style:page-layout-properties fo:page-width="21cm" fo:page-height="29.7cm" '
        'style:print-orientation="portrait" fo:margin-top="1.8cm" fo:margin-bottom="1.5cm" fo:margin-left="1.5cm" fo:margin-right="1.5cm"/>'
        '<style:footer-style><style:header-footer-properties fo:min-height="0.6cm" fo:margin-top="0.3cm"/></style:footer-style>'
        '</style:page-layout>',
        ps('H1_NovaPagina', '', '', pai='Heading_20_1', extra=' style:master-page-name="Texto"'),
        ps('Grifo_Topo', 'fo:text-align="center" fo:margin-bottom="0.6cm"', 'fo:font-size="14pt" fo:font-weight="bold"',
           pai='Standard', extra=' style:master-page-name="Capa"'),
        ps('Capa_Inicio', 'fo:text-align="center" fo:margin-bottom="0.3cm"', 'fo:font-weight="bold"', pai='Capa_Instituicao',
           extra=' style:master-page-name="Capa"'),
        cel('C_Cab', f'fo:border-top="{BORDA}" fo:border-bottom="{FINA}" fo:border-left="none" fo:border-right="none"'),
        cel('C_Corpo', 'fo:border="none"'),
        cel('C_Fim', f'fo:border-bottom="{BORDA}" fo:border-top="none" fo:border-left="none" fo:border-right="none"'),
        cel('C_Grade', f'fo:border="{FINA}"'),
        cel('C_GradeCab', f'fo:border="{FINA}"', 'fo:background-color="#EDEDED"'),
        '<style:style style:name="fr_fig" style:family="graphic"><style:graphic-properties style:wrap="none" '
        'style:vertical-pos="top" style:vertical-rel="baseline" style:horizontal-pos="center" style:horizontal-rel="paragraph"/></style:style>',
        *COLUNAS_TAB,
        *[f'<style:style style:name="{e}__{c}" style:family="paragraph" style:parent-style-name="{e}">'
          f'<style:paragraph-properties fo:background-color="{GRIFOS[c][0]}"/></style:style>'
          for e, c in sorted(ESTILOS_GRIFO)],
    ])


def mestres() -> str:
    return ('<style:master-page style:name="Capa" style:page-layout-name="pm_capa"/>'
            '<style:master-page style:name="Texto" style:page-layout-name="pm_texto"><style:footer>'
            '<text:p text:style-name="Rodape"><text:page-number text:select-page="current"/></text:p>'
            '</style:footer></style:master-page>')


def montar_fodt() -> str:
    conteudo()
    i = next(k for k, x in enumerate(CORPO) if 'text:style-name="Capa_Instituicao"' in x)  # 1º parágrafo da capa
    CORPO[i] = CORPO[i].replace('text:style-name="Capa_Instituicao"', 'text:style-name="Capa_Inicio"', 1)
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            f'<office:document {NS} office:version="1.3" office:mimetype="application/vnd.oasis.opendocument.text">'
            '<office:font-face-decls><style:font-face style:name="Times New Roman" '
            'svg:font-family="&apos;Times New Roman&apos;" style:font-family-generic="roman"/></office:font-face-decls>'
            f'<office:styles>{estilos()}</office:styles>'
            f'<office:automatic-styles>{automaticos()}</office:automatic-styles>'
            f'<office:master-styles>{mestres()}</office:master-styles>'
            f'<office:body><office:text>{"".join(CORPO)}</office:text></office:body></office:document>')


def converter(origem: Path, filtro: str, destino_dir: Path, perfil: Path) -> Path:
    cmd = ['soffice', f'-env:UserInstallation=file://{perfil}', '--headless', '--convert-to', filtro,
           '--outdir', str(destino_dir), str(origem)]
    subprocess.run(cmd, check=True, capture_output=True, timeout=240)
    saida = destino_dir / (origem.stem + '.' + filtro.split(':')[0])
    if not saida.exists():
        sys.exit(f'o LibreOffice não gerou {saida.name}')
    return saida


def sha(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def main() -> None:
    saida_docx, saida_pdf = SAIDA_DOCX, SAIDA_PDF
    if GRIFAR:  # cópia de conferência: outro nome, sem trava nem hash
        saida_docx, saida_pdf = (PASTA / f'{NOME}_GRIFADO_conferencia{s}' for s in ('.docx', '.pdf'))
    elif SAIDA_DOCX.exists() and '--sobrescrever' not in sys.argv:
        if not HASH.exists() or HASH.read_text().strip() != sha(SAIDA_DOCX):
            sys.exit(f'{SAIDA_DOCX.name} foi editado depois da última geração. Use --sobrescrever para '
                     'substituí-lo (a edição manual se perde).')
    fodt = montar_fodt()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        origem = tmp / f'{saida_docx.stem}.fodt'
        origem.write_text(fodt, encoding='utf-8')
        docx = converter(origem, 'docx:MS Word 2007 XML', tmp, tmp / 'perfil')
        pdf = converter(docx, 'pdf', tmp / 'pdf', tmp / 'perfil')
        shutil.copyfile(docx, saida_docx)
        shutil.copyfile(pdf, saida_pdf)
    if not GRIFAR:
        HASH.write_text(sha(saida_docx))
    paginas = len(PdfReader(saida_pdf).pages)
    pendentes = fodt.count('text:style-name="Pendente"')
    print(f'{saida_docx.relative_to(RAIZ)}  ({paginas} páginas no PDF; limite {LIMITE_PAGINAS})')
    print(f'{saida_pdf.relative_to(RAIZ)}')
    print(f'Marcas [A PREENCHER]/[confirmar]: {pendentes}')
    if paginas > LIMITE_PAGINAS and not GRIFAR:  # a cópia grifada tem uma página de legenda a mais
        sys.exit(f'PASSOU DO LIMITE: {paginas} páginas')


if __name__ == '__main__':
    main()
