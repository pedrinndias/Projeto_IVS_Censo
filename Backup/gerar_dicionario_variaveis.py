"""
Gera o Dicionario_Variaveis_IVS_Censo2022.xlsx — guia consolidado das variáveis
do Censo 2022 selecionadas para o projeto IVS, alinhado aos notebooks 01 e 02 da
Fase 3 e às decisões metodológicas registradas em GUIA_DO_PROJETO.md.

Estrutura do arquivo (7 abas):
  1. Inicio                    — capa e sumário
  2. Componentes_IVS           — as 7 variáveis-componente do IVS (fórmula final)
  3. Variaveis_Brutas_Censo    — todas as variáveis brutas extraídas do Censo
  4. Variaveis_Derivadas       — colunas calculadas pela pipeline
  5. Guia_por_Arquivo          — qual arquivo do Censo contém cada variável
  6. De_Para_2010_2022         — equivalência IVS-BH 2012 (Censo 2010) → 2022
  7. Decisoes_Metodologicas    — log das decisões consolidadas
"""

from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


# -----------------------------------------------------------------------------
# Estilo
# -----------------------------------------------------------------------------
FONT_TITLE   = Font(name='Calibri', size=16, bold=True, color='FFFFFF')
FONT_H1      = Font(name='Calibri', size=13, bold=True, color='FFFFFF')
FONT_HEADER  = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
FONT_BODY    = Font(name='Calibri', size=10)
FONT_BODY_B  = Font(name='Calibri', size=10, bold=True)
FONT_NOTE    = Font(name='Calibri', size=9, italic=True, color='595959')

FILL_TITLE   = PatternFill('solid', fgColor='1F4E78')   # azul escuro
FILL_DIM_SAN = PatternFill('solid', fgColor='2E75B6')   # azul saneamento
FILL_DIM_SOC = PatternFill('solid', fgColor='C00000')   # vermelho socioeconômico
FILL_HEADER  = PatternFill('solid', fgColor='305496')   # azul cabeçalho
FILL_SUBHDR  = PatternFill('solid', fgColor='8EA9DB')   # azul claro
FILL_OK      = PatternFill('solid', fgColor='C6EFCE')   # verde claro
FILL_WARN    = PatternFill('solid', fgColor='FFEB9C')   # amarelo
FILL_REJ     = PatternFill('solid', fgColor='FFC7CE')   # vermelho claro
FILL_ZEBRA   = PatternFill('solid', fgColor='F2F2F2')   # cinza muito claro

ALIGN_WRAP   = Alignment(horizontal='left', vertical='top', wrap_text=True)
ALIGN_CTR    = Alignment(horizontal='center', vertical='center', wrap_text=True)

BORDER_THIN  = Border(
    left=Side(style='thin',  color='BFBFBF'),
    right=Side(style='thin', color='BFBFBF'),
    top=Side(style='thin',   color='BFBFBF'),
    bottom=Side(style='thin', color='BFBFBF'),
)


def write_header_row(ws, row, headers, widths=None, fill=FILL_HEADER, height=28):
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=row, column=col_idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = fill
        cell.alignment = ALIGN_CTR
        cell.border = BORDER_THIN
    ws.row_dimensions[row].height = height
    if widths:
        for col_idx, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(col_idx)].width = w


def write_body_row(ws, row, values, fill=None, font=FONT_BODY):
    for col_idx, v in enumerate(values, start=1):
        cell = ws.cell(row=row, column=col_idx, value=v)
        cell.font = font
        cell.alignment = ALIGN_WRAP
        cell.border = BORDER_THIN
        if fill is not None:
            cell.fill = fill


def write_title_block(ws, row, title, span, fill=FILL_TITLE, font=FONT_TITLE, height=36):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    c = ws.cell(row=row, column=1, value=title)
    c.font = font
    c.fill = fill
    c.alignment = ALIGN_CTR
    ws.row_dimensions[row].height = height


# -----------------------------------------------------------------------------
# Aba 1 — Início
# -----------------------------------------------------------------------------
def aba_inicio(wb):
    ws = wb.create_sheet('Inicio')
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 4
    ws.column_dimensions['B'].width = 28
    ws.column_dimensions['C'].width = 90

    write_title_block(ws, 1, 'Dicionário de Variáveis — Projeto IVS / Censo 2022', span=4)

    intro = [
        ('Projeto',
         'Índice de Vulnerabilidade à Saúde (IVS) intraurbano — 70 municípios do ELSI-Brasil. '
         'Estudo ecológico com setor censitário como unidade de análise. '
         'Iniciação Científica Fiocruz Minas (Mar/2026 – Fev/2027).'),
        ('Fonte primária',
         'Censo Demográfico 2022 (IBGE) — Agregados por Setores Censitários (8 arquivos CSV).'),
        ('Dicionário oficial',
         'dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx (IBGE).'),
        ('Pipeline ativa',
         'notebooks/Fase3_EDA_ELSI/ → Notebook 01 (extração e filtro ELSI) → Notebook 02 (EDA).'),
        ('Base bruta gerada',
         'banco_de_dados/Base_ELSI_Bruta_Censo2022.csv — 109.032 setores × 47 colunas (106.281 OK após filtro de elegibilidade).'),
        ('Quando atualizar este arquivo',
         'Sempre que o conjunto de variáveis selecionadas mudar (ex.: troca de denominador, '
         'inclusão de nova variável, mudança de fórmula).'),
    ]
    r = 3
    for k, v in intro:
        ws.cell(row=r, column=2, value=k).font = FONT_BODY_B
        ws.cell(row=r, column=2).alignment = ALIGN_WRAP
        ws.cell(row=r, column=3, value=v).font = FONT_BODY
        ws.cell(row=r, column=3).alignment = ALIGN_WRAP
        ws.row_dimensions[r].height = 38
        r += 1

    r += 1
    write_title_block(ws, r, 'Sumário das abas', span=4, fill=FILL_HEADER,
                      font=FONT_H1, height=28)
    r += 1
    abas = [
        ('Componentes_IVS',
         'As 7 variáveis-componente do IVS (3 saneamento + 4 socioeconômicas), com '
         'fórmula final, numeradores, denominadores e direção da vulnerabilidade.'),
        ('Variaveis_Brutas_Censo',
         'Todas as variáveis brutas extraídas dos 8 arquivos do Censo: código IBGE, '
         'descrição, arquivo-fonte, papel no projeto e observações de sigilo.'),
        ('Variaveis_Derivadas',
         'Colunas calculadas pela pipeline (proporções, razões, classificadores). '
         'É aqui que aparecem pct_agua_inad, razao_moradores, Dados_sig etc.'),
        ('Guia_por_Arquivo',
         'Cada um dos 8 arquivos do Censo e as variáveis-chave extraídas dele. '
         'Útil para reabrir um CSV bruto e localizar uma variável rapidamente.'),
        ('De_Para_2010_2022',
         'Equivalência entre as variáveis usadas no IVS-BH 2012 (Censo 2010) e suas '
         'contrapartes no Censo 2022, com nota sobre limitações.'),
        ('Decisoes_Metodologicas',
         'Log das decisões metodológicas consolidadas (denominador V00001, taxa de '
         'analfabetismo, variáveis de esgoto, sigilo em V00901, V01042 rejeitada).'),
    ]
    for nome, desc in abas:
        ws.cell(row=r, column=2, value=nome).font = FONT_BODY_B
        ws.cell(row=r, column=2).alignment = ALIGN_WRAP
        ws.cell(row=r, column=3, value=desc).font = FONT_BODY
        ws.cell(row=r, column=3).alignment = ALIGN_WRAP
        ws.row_dimensions[r].height = 36
        r += 1

    r += 1
    nota = ('Convenções: "↑ vulnerabilidade" = quanto maior o valor, maior a vulnerabilidade. '
            'Renda é a única variável invertida (↓). Denominadores em negrito são os adotados '
            'na decisão metodológica de 22/05/2026 (orientadora).')
    ws.cell(row=r, column=2, value='Notas').font = FONT_BODY_B
    ws.cell(row=r, column=3, value=nota).font = FONT_NOTE
    ws.cell(row=r, column=3).alignment = ALIGN_WRAP
    ws.row_dimensions[r].height = 36


# -----------------------------------------------------------------------------
# Aba 2 — Componentes IVS
# -----------------------------------------------------------------------------
COMPONENTES = [
    {
        'dim': 'Saneamento',
        'nome': 'pct_agua_inad',
        'rotulo': '% domicílios com abastecimento de água inadequado',
        'numerador': 'V00112 + V00113 + V00114 + V00115 + V00116 + V00117 + V00118',
        'arquivo_num': 'caracteristicas_domicilio2',
        'denominador': 'V00001',
        'arquivo_den': 'caracteristicas_domicilio1',
        'descricao_num': ('Soma das 7 categorias do bloco "Abastecimento de água" '
                          'consideradas inadequadas (poço raso, água da chuva, carro-pipa, '
                          'curso d\'água, outras formas não canalizadas).'),
        'descricao_den': 'Domicílios Particulares Permanentes Ocupados (DPPO).',
        'direcao': '↑ vulnerabilidade',
        'tipo': 'Proporção [0, 1]',
        'sigilo': 'Raro (~0% dos setores ELSI OK)',
        'fonte_metodologia': 'IVS-BH 2012 (V013–V015 do Censo 2010 → V00112–V00118 no Censo 2022).',
    },
    {
        'dim': 'Saneamento',
        'nome': 'pct_esgoto_inad',
        'rotulo': '% domicílios com esgotamento sanitário inadequado',
        'numerador': 'V00312 + V00313 + V00314 + V00315 + V00316',
        'arquivo_num': 'caracteristicas_domicilio2',
        'denominador': 'V00001',
        'arquivo_den': 'caracteristicas_domicilio1',
        'descricao_num': ('Bloco "Destinação do esgoto do banheiro ou sanitário" — '
                          'categorias inadequadas (fossa rudimentar, vala, rio/lago, outro). '
                          'Confirmado pelo dicionário oficial IBGE — NÃO confundir com '
                          'V00249–V00253 (tipologia de habitação).'),
        'descricao_den': 'Domicílios Particulares Permanentes Ocupados (DPPO).',
        'direcao': '↑ vulnerabilidade',
        'tipo': 'Proporção [0, 1]',
        'sigilo': 'Raro',
        'fonte_metodologia': 'IVS-BH 2012 (V019–V028 do Censo 2010 → V00312–V00316 no Censo 2022).',
    },
    {
        'dim': 'Saneamento',
        'nome': 'pct_lixo_inad',
        'rotulo': '% domicílios com destino do lixo inadequado',
        'numerador': 'V00398 + V00399 + V00400 + V00401 + V00402',
        'arquivo_num': 'caracteristicas_domicilio2',
        'denominador': 'V00001',
        'arquivo_den': 'caracteristicas_domicilio1',
        'descricao_num': ('Categorias do bloco "Destino do lixo" consideradas inadequadas '
                          '(queimado, enterrado, jogado em terreno baldio, rio/lago, outro).'),
        'descricao_den': 'Domicílios Particulares Permanentes Ocupados (DPPO).',
        'direcao': '↑ vulnerabilidade',
        'tipo': 'Proporção [0, 1]',
        'sigilo': 'Raro',
        'fonte_metodologia': 'IVS-BH 2012 (V037–V042 do Censo 2010 → V00398–V00402 no Censo 2022).',
    },
    {
        'dim': 'Socioeconômica',
        'nome': 'razao_moradores',
        'rotulo': 'Razão de moradores por domicílio (densidade habitacional)',
        'numerador': 'V00005 + V00006',
        'arquivo_num': 'caracteristicas_domicilio1',
        'denominador': 'V00001 + V00002',
        'arquivo_den': 'caracteristicas_domicilio1',
        'descricao_num': 'Moradores em DPP Ocupados + moradores em DPI Ocupados.',
        'descricao_den': ('Domicílios Particulares Permanentes Ocupados (DPPO) + '
                          'Domicílios Particulares Improvisados Ocupados (DPIO). '
                          'Reproduz a definição oficial do V0005 do IBGE.'),
        'direcao': '↑ vulnerabilidade',
        'tipo': 'Razão (≥ 1, sem teto)',
        'sigilo': 'Não aplicável (variáveis-base)',
        'fonte_metodologia': 'IVS-BH 2012 (Pop. / Dom. Ocupados) → razão equivalente no 2022.',
    },
    {
        'dim': 'Socioeconômica',
        'nome': 'pct_analfab',
        'rotulo': 'Taxa de analfabetismo (15+ anos)',
        'numerador': 'V00901',
        'arquivo_num': 'alfabetizacao',
        'denominador': 'V00900 + V00901',
        'arquivo_den': 'alfabetizacao',
        'descricao_num': 'Pessoas de 15 anos ou mais que NÃO sabem ler e escrever.',
        'descricao_den': ('Total de pessoas com 15 anos ou mais = alfabetizadas (V00900) + '
                          'analfabetas (V00901). NÃO usar V00900 sozinho no denominador '
                          '(erro matemático; corrigido em 22/05/2026).'),
        'direcao': '↑ vulnerabilidade',
        'tipo': 'Proporção [0, 1]',
        'sigilo': ('Crítico — ~15,76% dos setores ELSI OK têm V00901 sigilada. '
                   'Concentrado em capitais (BH 22%, Porto Alegre 27%, São Caetano do Sul 30%). '
                   'Decisão: manter NaN (transparente).'),
        'fonte_metodologia': ('IVS 2012 pedia % chefes < 4 anos de estudo; no Censo 2022 anos de '
                              'instrução não vêm nos agregados → substituído por taxa de analfabetismo.'),
    },
    {
        'dim': 'Socioeconômica',
        'nome': 'renda_media',
        'rotulo': 'Rendimento nominal mensal médio dos responsáveis',
        'numerador': 'V06004 (variável pronta)',
        'arquivo_num': 'renda_responsavel',
        'denominador': '—',
        'arquivo_den': '—',
        'descricao_num': ('Valor médio do rendimento nominal mensal das pessoas responsáveis '
                          'por domicílio particular permanente — em reais. Já vem agregado por setor.'),
        'descricao_den': 'Não há denominador — a variável é uma média pronta.',
        'direcao': '↓ vulnerabilidade (INVERTIDA na padronização)',
        'tipo': 'Valor monetário (R$/mês)',
        'sigilo': 'Baixo (~0% dos setores ELSI OK; alguns NaN por arredondamento).',
        'fonte_metodologia': ('IVS 2012 pedia % famílias ≤ 2 SM; faixas salariais não vêm nos '
                              'agregados do Censo 2022 → substituído por rendimento médio invertido.'),
    },
    {
        'dim': 'Socioeconômica',
        'nome': 'pct_raca_pretpardind',
        'rotulo': '% pessoas de raça/cor preta, parda ou indígena',
        'numerador': 'V01318 + V01320 + V01321',
        'arquivo_num': 'cor_ou_raca',
        'denominador': 'v0001',
        'arquivo_den': 'basico',
        'descricao_num': 'Pretos (V01318) + pardos (V01320) + indígenas (V01321).',
        'descricao_den': ('População residente total do setor (v0001). NÃO usar V00001 — esse é '
                          'denominador domiciliar; raça/cor é uma proporção populacional.'),
        'direcao': '↑ vulnerabilidade',
        'tipo': 'Proporção [0, 1]',
        'sigilo': 'Raro',
        'fonte_metodologia': ('Proxy de vulnerabilidade social estrutural — explicação em nota '
                              'de rodapé do artigo (Plano_Artigo, Tabela 5).'),
    },
]


def aba_componentes(wb):
    ws = wb.create_sheet('Componentes_IVS')
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = 'A4'

    write_title_block(ws, 1, 'As 7 variáveis-componente do IVS', span=10)
    sub = ('Cada linha é uma das 7 variáveis-componente do IVS. Cores: '
           'azul = dimensão Saneamento (3 variáveis); vermelho = dimensão Socioeconômica (4 variáveis).')
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=10)
    c = ws.cell(row=2, column=1, value=sub)
    c.font = FONT_NOTE
    c.alignment = ALIGN_WRAP
    ws.row_dimensions[2].height = 28

    headers = [
        'Dimensão', 'Nome (coluna)', 'Rótulo descritivo',
        'Numerador (vars IBGE)', 'Arquivo numerador',
        'Denominador (vars IBGE)', 'Arquivo denominador',
        'Direção', 'Tipo / Faixa', 'Sigilo & observações',
    ]
    widths = [16, 22, 36, 32, 24, 22, 24, 22, 18, 50]
    write_header_row(ws, 3, headers, widths)

    r = 4
    for comp in COMPONENTES:
        fill = FILL_DIM_SAN if comp['dim'] == 'Saneamento' else FILL_DIM_SOC
        # Coluna 1 (dimensão) — pinta com cor da dimensão e fonte branca
        ws.cell(row=r, column=1, value=comp['dim']).font = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
        ws.cell(row=r, column=1).fill = fill
        ws.cell(row=r, column=1).alignment = ALIGN_CTR
        ws.cell(row=r, column=1).border = BORDER_THIN

        values_rest = [
            comp['nome'], comp['rotulo'],
            comp['numerador'], comp['arquivo_num'],
            comp['denominador'], comp['arquivo_den'],
            comp['direcao'], comp['tipo'], comp['sigilo'],
        ]
        for col_idx, v in enumerate(values_rest, start=2):
            cell = ws.cell(row=r, column=col_idx, value=v)
            cell.font = FONT_BODY
            cell.alignment = ALIGN_WRAP
            cell.border = BORDER_THIN
        ws.row_dimensions[r].height = 78
        r += 1

    # Tabela complementar — descrições longas
    r += 2
    write_title_block(ws, r, 'Descrições estendidas e fonte metodológica',
                      span=10, fill=FILL_HEADER, font=FONT_H1, height=28)
    r += 1
    headers2 = ['Componente', 'Descrição do numerador', 'Descrição do denominador',
                'Fonte metodológica / De-Para']
    widths2 = [22, 60, 60, 60]
    # Aplica larguras só nas colunas relevantes (mantém as anteriores)
    for col_idx, w in enumerate(widths2, start=1):
        # respeitamos as larguras já amplas
        cur = ws.column_dimensions[get_column_letter(col_idx)].width
        if cur is None or cur < w:
            ws.column_dimensions[get_column_letter(col_idx)].width = w
    for col_idx, h in enumerate(headers2, start=1):
        cell = ws.cell(row=r, column=col_idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = ALIGN_CTR
        cell.border = BORDER_THIN
    ws.row_dimensions[r].height = 28
    r += 1

    for comp in COMPONENTES:
        write_body_row(ws, r, [comp['nome'], comp['descricao_num'],
                               comp['descricao_den'], comp['fonte_metodologia']])
        ws.row_dimensions[r].height = 60
        r += 1


# -----------------------------------------------------------------------------
# Aba 3 — Variáveis brutas do Censo
# -----------------------------------------------------------------------------
# Estrutura: (codigo, arquivo, descricao_ibge, papel_no_projeto, usado_em, obs)
VARS_BRUTAS = [
    # ---------------- Identificação / geografia / população ---------------
    ('CD_SETOR',  'basico', 'Código do setor censitário (15 dígitos: UF[2] + MUN[5] + DIST[2] + SUBDIST[2] + SETOR[4]).',
     'Chave primária da base; chave de merge entre os 8 arquivos.',
     'todas as tabelas', 'Texto. Não converter para int — perde zeros à esquerda.'),
    ('NM_MUN',    'basico', 'Nome do município conforme IBGE.',
     'Identificação; usado no cruzamento com a lista ELSI por (UF + nome normalizado).',
     'filtro ELSI (NB01), descritivas por município (NB02)',
     'Atenção a acentos/hífens — Notebook 01 normaliza para casar com a lista ELSI.'),
    ('NM_BAIRRO', 'basico', 'Nome do bairro (quando disponível).',
     'Contexto qualitativo; auditoria de extremos.',
     'auditoria razao_moradores (NB02)', 'Pode ser NaN — não é obrigatório.'),
    ('SITUACAO',  'basico', 'Situação do setor (urbano / rural, com subcategorias).',
     'Filtros futuros (análise restrita a urbano).', 'reservado para análises futuras',
     'Texto codificado pelo IBGE.'),
    ('v0001',     'basico', 'População residente total do setor.',
     'DENOMINADOR da proporção de raça/cor. Base do filtro Dados_sig (ZERADO se v0001 = 0).',
     'pct_raca_pretpardind, Dados_sig', 'Atenção: minúsculo no CSV original.'),

    # ---------------- Domicílio 1 — denominadores e moradia ---------------
    ('V00001', 'caracteristicas_domicilio1', 'Domicílios Particulares Permanentes Ocupados (DPPO).',
     'DENOMINADOR PADRÃO das 3 proporções domiciliares (água, esgoto, lixo). '
     'Equivalente ao V002 do Censo 2010 — padrão IVS-BH.',
     'pct_agua_inad, pct_esgoto_inad, pct_lixo_inad, razao_moradores, Dados_sig',
     'Decisão metodológica 22/05/2026 (orientadora): voltou a ser V00001, descartando V01042.'),
    ('V00002', 'caracteristicas_domicilio1', 'Domicílios Particulares Improvisados Ocupados (DPIO).',
     'Compõe o denominador da razão de moradores (V00001 + V00002).',
     'razao_moradores',
     'DPIO = barracos, tendas, embarcações. Raro em setores urbanos centrais.'),
    ('V00005', 'caracteristicas_domicilio1', 'Moradores em Domicílios Particulares Permanentes Ocupados.',
     'NUMERADOR da razão de moradores.', 'razao_moradores', '—'),
    ('V00006', 'caracteristicas_domicilio1', 'Moradores em Domicílios Particulares Improvisados Ocupados.',
     'Compõe o numerador da razão de moradores (V00005 + V00006).', 'razao_moradores', '—'),
    ('V00047', 'caracteristicas_domicilio1', 'Domicílios com espécie "Casa".',
     'Classificador de morfologia urbana predominante.', 'Moradia_Predominante', '—'),
    ('V00048', 'caracteristicas_domicilio1', 'Domicílios com espécie "Casa de Vila / Condomínio".',
     'Classificador de morfologia urbana.', 'Moradia_Predominante', '—'),
    ('V00049', 'caracteristicas_domicilio1', 'Domicílios com espécie "Apartamento".',
     'Classificador de morfologia urbana.', 'Moradia_Predominante', '—'),
    ('V00050', 'caracteristicas_domicilio1', 'Domicílios com espécie "Cortiço / Casa de Cômodos".',
     'Classificador de morfologia urbana — proxy de habitação precária.', 'Moradia_Predominante', '—'),
    ('V00051', 'caracteristicas_domicilio1', 'Domicílios com espécie "Maloca Indígena".',
     'Classificador de morfologia urbana.', 'Moradia_Predominante', '—'),
    ('V00052', 'caracteristicas_domicilio1', 'Domicílios com espécie "Estrutura Degradada / Inacabada".',
     'Classificador de morfologia urbana — proxy de habitação precária.', 'Moradia_Predominante', '—'),

    # ---------------- Domicílio 2 — saneamento (água, esgoto, lixo) -------
    ('V00112', 'caracteristicas_domicilio2', 'Abastecimento de água — categoria inadequada 1 (poço raso, etc.).',
     'NUMERADOR de pct_agua_inad.', 'pct_agua_inad', 'Verificar rótulo exato no dicionário IBGE.'),
    ('V00113', 'caracteristicas_domicilio2', 'Abastecimento de água — categoria inadequada 2.',
     'NUMERADOR de pct_agua_inad.', 'pct_agua_inad', '—'),
    ('V00114', 'caracteristicas_domicilio2', 'Abastecimento de água — categoria inadequada 3.',
     'NUMERADOR de pct_agua_inad.', 'pct_agua_inad', '—'),
    ('V00115', 'caracteristicas_domicilio2', 'Abastecimento de água — categoria inadequada 4.',
     'NUMERADOR de pct_agua_inad.', 'pct_agua_inad', '—'),
    ('V00116', 'caracteristicas_domicilio2', 'Abastecimento de água — categoria inadequada 5.',
     'NUMERADOR de pct_agua_inad.', 'pct_agua_inad', '—'),
    ('V00117', 'caracteristicas_domicilio2', 'Abastecimento de água — categoria inadequada 6.',
     'NUMERADOR de pct_agua_inad.', 'pct_agua_inad', '—'),
    ('V00118', 'caracteristicas_domicilio2', 'Abastecimento de água — categoria inadequada 7.',
     'NUMERADOR de pct_agua_inad.', 'pct_agua_inad', '—'),

    ('V00236', 'caracteristicas_domicilio2', 'Variável de banheiro/sanitário (uso futuro).',
     'Reservado — não compõe o IVS atual.', '—', 'Extraído por precaução; não é usado em NB02.'),
    ('V00238', 'caracteristicas_domicilio2', 'Variável de banheiro/sanitário (uso futuro).',
     'Reservado — não compõe o IVS atual.', '—', 'Extraído por precaução; não é usado em NB02.'),

    ('V00312', 'caracteristicas_domicilio2', 'Destinação do esgoto — categoria inadequada 1 (fossa rudimentar, etc.).',
     'NUMERADOR de pct_esgoto_inad.', 'pct_esgoto_inad',
     'NÃO confundir com V00249–V00253 (tipologia de habitação). Decisão confirmada pelo dicionário oficial IBGE.'),
    ('V00313', 'caracteristicas_domicilio2', 'Destinação do esgoto — categoria inadequada 2.',
     'NUMERADOR de pct_esgoto_inad.', 'pct_esgoto_inad', '—'),
    ('V00314', 'caracteristicas_domicilio2', 'Destinação do esgoto — categoria inadequada 3.',
     'NUMERADOR de pct_esgoto_inad.', 'pct_esgoto_inad', '—'),
    ('V00315', 'caracteristicas_domicilio2', 'Destinação do esgoto — categoria inadequada 4.',
     'NUMERADOR de pct_esgoto_inad.', 'pct_esgoto_inad', '—'),
    ('V00316', 'caracteristicas_domicilio2', 'Destinação do esgoto — categoria inadequada 5.',
     'NUMERADOR de pct_esgoto_inad.', 'pct_esgoto_inad', '—'),

    ('V00398', 'caracteristicas_domicilio2', 'Destino do lixo — categoria inadequada 1 (queimado, etc.).',
     'NUMERADOR de pct_lixo_inad.', 'pct_lixo_inad', '—'),
    ('V00399', 'caracteristicas_domicilio2', 'Destino do lixo — categoria inadequada 2.',
     'NUMERADOR de pct_lixo_inad.', 'pct_lixo_inad', '—'),
    ('V00400', 'caracteristicas_domicilio2', 'Destino do lixo — categoria inadequada 3.',
     'NUMERADOR de pct_lixo_inad.', 'pct_lixo_inad', '—'),
    ('V00401', 'caracteristicas_domicilio2', 'Destino do lixo — categoria inadequada 4.',
     'NUMERADOR de pct_lixo_inad.', 'pct_lixo_inad', '—'),
    ('V00402', 'caracteristicas_domicilio2', 'Destino do lixo — categoria inadequada 5.',
     'NUMERADOR de pct_lixo_inad.', 'pct_lixo_inad', '—'),

    # ---------------- Alfabetização ---------------------------------------
    ('V00900', 'alfabetizacao', 'Pessoas de 15 anos ou mais que sabem ler e escrever.',
     'Parte do DENOMINADOR de pct_analfab (junto com V00901).',
     'pct_analfab',
     'NÃO usar V00900 sozinho como denominador — erro matemático corrigido em 22/05/2026.'),
    ('V00901', 'alfabetizacao', 'Pessoas de 15 anos ou mais que NÃO sabem ler e escrever.',
     'NUMERADOR de pct_analfab; também integra o denominador.',
     'pct_analfab',
     'Sigilo sistemático: ~15,76% dos setores ELSI OK estão sigilados. Concentrado em capitais.'),

    # ---------------- Cor / raça ------------------------------------------
    ('V01318', 'cor_ou_raca', 'Pessoas declaradas de cor/raça preta.',
     'NUMERADOR de pct_raca_pretpardind.', 'pct_raca_pretpardind', '—'),
    ('V01320', 'cor_ou_raca', 'Pessoas declaradas de cor/raça parda.',
     'NUMERADOR de pct_raca_pretpardind.', 'pct_raca_pretpardind', '—'),
    ('V01321', 'cor_ou_raca', 'Pessoas declaradas de cor/raça indígena.',
     'NUMERADOR de pct_raca_pretpardind.', 'pct_raca_pretpardind',
     'V01319 (amarelos) e V01317 (brancos) NÃO entram no numerador.'),

    # ---------------- Renda -----------------------------------------------
    ('V06004', 'renda_responsavel', 'Rendimento nominal mensal médio das pessoas responsáveis por DPP (R$).',
     'Variável renda_media — única componente invertida no IVS.',
     'renda_media',
     'Vírgula como separador decimal no CSV — Notebook 02 troca por ponto antes de converter.'),

    # ---------------- Demografia (Fase 2 - legado) ------------------------
    ('V01031', 'demografia', 'População de 0 a 4 anos.',
     'Reservado — Fase 2 (Proxy de Extrema Pobreza Multidimensional, não usada na Fase 3).',
     '—', 'Extraído por compatibilidade com legado.'),
    ('V01032', 'demografia', 'População de 5 a 9 anos.',
     'Reservado — Fase 2.', '—', 'Idem.'),
    ('V01033', 'demografia', 'População de 10 a 14 anos.',
     'Reservado — Fase 2.', '—', 'Idem.'),

    # ---------------- Parentesco — V01042 REJEITADA -----------------------
    ('V01042', 'parentesco', 'Total de responsáveis (pessoas, NÃO domicílios).',
     'REJEITADA como denominador pela orientadora em 22/05/2026. Permanece na base bruta apenas para histórico/auditoria.',
     '— (não usada nos cálculos atuais)',
     'A Fase 2 usava V01042 como denominador; a Fase 3 corrigiu para V00001.'),
]


def aba_variaveis_brutas(wb):
    ws = wb.create_sheet('Variaveis_Brutas_Censo')
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = 'A4'

    write_title_block(ws, 1, 'Variáveis brutas extraídas do Censo 2022', span=6)
    sub = ('Lista completa das colunas brutas que a pipeline (Notebook 01) extrai dos 8 arquivos do '
           'Censo e leva para Base_ELSI_Bruta_Censo2022.csv. A coluna "Papel no projeto" diz para '
           'que cada variável serve no cálculo do IVS.')
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=6)
    c = ws.cell(row=2, column=1, value=sub)
    c.font = FONT_NOTE
    c.alignment = ALIGN_WRAP
    ws.row_dimensions[2].height = 28

    headers = ['Código (IBGE)', 'Arquivo-fonte', 'Descrição (Censo 2022)',
               'Papel no projeto IVS', 'Usado em (variável derivada)', 'Observações']
    widths = [14, 30, 55, 55, 38, 50]
    write_header_row(ws, 3, headers, widths)

    r = 4
    for idx, row in enumerate(VARS_BRUTAS):
        fill = FILL_ZEBRA if idx % 2 == 1 else None
        # Pintar de vermelho-claro se for V01042 (rejeitada)
        if row[0] == 'V01042':
            fill = FILL_REJ
        write_body_row(ws, r, list(row), fill=fill)
        # altura adaptativa
        max_len = max(len(str(v)) for v in row)
        ws.row_dimensions[r].height = max(28, min(120, max_len // 4 * 4))
        r += 1


# -----------------------------------------------------------------------------
# Aba 4 — Variáveis derivadas
# -----------------------------------------------------------------------------
DERIVADAS = [
    ('CD_UF', 'Identificação', 'CD_SETOR[:2]', 'Código IBGE da UF (2 dígitos).',
     'Mapeamento UF → região; agrupamentos.',
     'Derivada no Notebook 01.'),
    ('CD_MUN', 'Identificação', 'CD_SETOR[:7]', 'Código IBGE do município (7 dígitos).',
     'Agrupamentos por município.',
     'Derivada no Notebook 01.'),
    ('regiao', 'Identificação', 'mapa CD_UF → regiao via municipios_elsi_brasil.csv',
     'Região geográfica (Norte / Nordeste / Sudeste / Sul / Centro-Oeste).',
     'Descritivas por região; boxplots.',
     'Derivada no Notebook 02 a partir do CSV oficial dos 70 municípios.'),
    ('Moradia_Predominante', 'Classificador', 'argmax(V00047..V00052)',
     'Tipo de moradia predominante no setor: Casa, Casa de Vila/Condomínio, '
     'Apartamento, Cortiço/Casa de Cômodos, Maloca Indígena, Estrutura Degradada/Inacabada, '
     'ou "Indefinido/Sem Moradia" quando todos = 0.',
     'Análises de perfis morfológicos vs. vulnerabilidade.',
     'Derivada no Notebook 01.'),
    ('Dados_sig', 'Classificador', 'regra sobre v0001 e V00001',
     'Elegibilidade do setor: OK / SIGILOSO / COLETIVO / ZERADO. '
     'Apenas OK entra nas análises descritivas.',
     'Filtro de elegibilidade no Notebook 02.',
     'Revisado em 22/05/2026 — ancorado em V00001 (não mais V01042). '
     'Resultado ELSI: 106.281 OK / 2.751 SIGILOSO (97,48% / 2,52%).'),
    ('pct_agua_inad', 'Indicador IVS', '(V00112+...+V00118) / V00001',
     '% domicílios com água inadequada. Clipped em [0, 1].',
     'Componente 1 do IVS (saneamento).',
     'Sigilo: se TODAS as parcelas estiverem NaN, o indicador vira NaN (min_count=1).'),
    ('pct_esgoto_inad', 'Indicador IVS', '(V00312+...+V00316) / V00001',
     '% domicílios com esgoto inadequado.',
     'Componente 2 do IVS (saneamento).',
     'Confirmado V00312–V00316 (não V00249–V00253) pelo dicionário oficial IBGE.'),
    ('pct_lixo_inad', 'Indicador IVS', '(V00398+...+V00402) / V00001',
     '% domicílios com destino do lixo inadequado.',
     'Componente 3 do IVS (saneamento).', '—'),
    ('razao_moradores', 'Indicador IVS', '(V00005+V00006) / (V00001+V00002)',
     'Razão de moradores por domicílio (densidade habitacional). Reproduz V0005 do IBGE.',
     'Componente 4 do IVS (socioeconômica).',
     'Auditoria detectou extremos (Portel-PA com ~8,8) → preservados para análise.'),
    ('pct_analfab', 'Indicador IVS', 'V00901 / (V00900 + V00901)',
     'Taxa de analfabetismo (15+ anos).',
     'Componente 5 do IVS (socioeconômica).',
     'Decisão de 22/05/2026: V00901 sigilada (~16% dos setores OK) mantida como NaN.'),
    ('renda_media', 'Indicador IVS', 'V06004 (direto)',
     'Rendimento nominal mensal médio dos responsáveis (R$).',
     'Componente 6 do IVS (socioeconômica). ÚNICA invertida.',
     'Pendente: normalização min-max POR MUNICÍPIO (não global).'),
    ('pct_raca_pretpardind', 'Indicador IVS', '(V01318 + V01320 + V01321) / v0001',
     '% de pessoas de raça/cor preta, parda ou indígena.',
     'Componente 7 do IVS (socioeconômica).',
     'Denominador é v0001 (população total), não V00001.'),
]


def aba_variaveis_derivadas(wb):
    ws = wb.create_sheet('Variaveis_Derivadas')
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = 'A4'

    write_title_block(ws, 1, 'Variáveis derivadas / calculadas pela pipeline', span=6)
    sub = ('Colunas que NÃO vêm direto do Censo — são calculadas nos Notebooks 01 e 02. '
           'Inclui os 7 indicadores brutos do IVS, classificadores (Moradia_Predominante, '
           'Dados_sig) e códigos geográficos derivados.')
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=6)
    c = ws.cell(row=2, column=1, value=sub)
    c.font = FONT_NOTE
    c.alignment = ALIGN_WRAP
    ws.row_dimensions[2].height = 28

    headers = ['Nome', 'Categoria', 'Fórmula', 'Descrição', 'Uso no projeto', 'Observações']
    widths = [24, 18, 38, 55, 40, 55]
    write_header_row(ws, 3, headers, widths)

    r = 4
    for idx, row in enumerate(DERIVADAS):
        fill = FILL_ZEBRA if idx % 2 == 1 else None
        # Indicadores IVS em verde claro
        if row[1] == 'Indicador IVS':
            fill = FILL_OK
        write_body_row(ws, r, list(row), fill=fill)
        ws.row_dimensions[r].height = 60
        r += 1


# -----------------------------------------------------------------------------
# Aba 5 — Guia por arquivo do Censo
# -----------------------------------------------------------------------------
ARQUIVOS = [
    ('basico',
     'Agregados_por_setores_basico_BR_20250417.csv',
     '~468 mil linhas (1 por setor); ~140 MB',
     'Identificação geográfica e população residente.',
     'CD_SETOR, NM_MUN, NM_BAIRRO, SITUACAO, v0001',
     'Encoding: latin1. Coluna v0001 em minúsculas — atenção.'),
    ('caracteristicas_domicilio1',
     'Agregados_por_setores_caracteristicas_domicilio1_BR.csv',
     '~250 MB',
     'Denominadores habitacionais (DPPO, DPIO) e morfologia da habitação.',
     'V00001, V00002, V00005, V00006, V00047–V00052',
     'Coluna-chave: CD_setor (minúsculo) — renomeada para CD_SETOR no NB01.'),
    ('caracteristicas_domicilio2',
     'Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv',
     '~747 MB',
     'Saneamento (água, esgoto, lixo) e banheiros. Arquivo mais pesado da pipeline.',
     'V00112–V00118 (água), V00312–V00316 (esgoto), V00398–V00402 (lixo), V00236, V00238',
     'Lido em chunks de 100 mil linhas no NB01. Coluna-chave: "setor".'),
    ('alfabetizacao',
     'Agregados_por_setores_alfabetizacao_BR.csv',
     '~701 MB',
     'Alfabetização da população de 15 anos ou mais.',
     'V00900 (alfabetizados 15+), V00901 (analfabetos 15+)',
     'V00901 sigilada em ~16% dos setores ELSI OK — concentrada em capitais.'),
    ('cor_ou_raca',
     'Agregados_por_setores_cor_ou_raca_BR.csv',
     'porte médio',
     'Distribuição por cor/raça (componente do IVS).',
     'V01318 (pretos), V01320 (pardos), V01321 (indígenas)',
     'V01317 (brancos) e V01319 (amarelos) NÃO entram no numerador.'),
    ('renda_responsavel',
     'Agregados_por_setores_renda_responsavel_BR.csv',
     'pequeno',
     'Rendimento médio dos responsáveis.',
     'V06004 (rendimento nominal mensal médio em R$)',
     'Vírgula como separador decimal — converter antes de cast numérico.'),
    ('demografia',
     'Agregados_por_setores_demografia_BR.csv',
     'médio',
     'Composição etária da população.',
     'V01031 (0–4 anos), V01032 (5–9), V01033 (10–14)',
     'Usado na Fase 2 (Proxy de Extrema Pobreza Multidimensional). Não compõe a Fase 3.'),
    ('parentesco',
     'Agregados_por_setores_parentesco_BR.csv',
     'médio',
     'Relação de parentesco com a pessoa responsável.',
     'V01042 (Total de Responsáveis — pessoas, não domicílios)',
     'V01042 REJEITADA pela orientadora (22/05/2026). Permanece na base bruta para histórico.'),
]


def aba_guia_por_arquivo(wb):
    ws = wb.create_sheet('Guia_por_Arquivo')
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = 'A4'

    write_title_block(ws, 1, 'Guia: onde encontrar cada variável (8 arquivos do Censo 2022)',
                      span=6)
    sub = ('Cada linha é um dos 8 CSVs originais do IBGE em dados/. Use este guia para reabrir '
           'um arquivo bruto e localizar uma variável rapidamente.')
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=6)
    c = ws.cell(row=2, column=1, value=sub)
    c.font = FONT_NOTE
    c.alignment = ALIGN_WRAP
    ws.row_dimensions[2].height = 26

    headers = ['Rótulo (curto)', 'Nome do arquivo CSV', 'Tamanho aprox.',
               'Conteúdo', 'Variáveis extraídas pela pipeline', 'Observações técnicas']
    widths = [28, 60, 18, 55, 55, 55]
    write_header_row(ws, 3, headers, widths)

    r = 4
    for idx, row in enumerate(ARQUIVOS):
        fill = FILL_ZEBRA if idx % 2 == 1 else None
        write_body_row(ws, r, list(row), fill=fill)
        ws.row_dimensions[r].height = 60
        r += 1


# -----------------------------------------------------------------------------
# Aba 6 — De-Para 2010 → 2022
# -----------------------------------------------------------------------------
DE_PARA = [
    ('Saneamento — Água inadequada',
     'V013–V015 (3 categorias inadequadas)',
     'V00112 a V00118 (7 categorias inadequadas)',
     'V00001 (DPPO)',
     'Maior granularidade no 2022 (7 categorias vs 3).',
     'Implementado ✅'),
    ('Saneamento — Esgoto inadequado',
     'V019–V028',
     'V00312–V00316',
     'V00001 (DPPO)',
     'Resolvida inconsistência do relatório legado (V00249–V00253 era tipologia de habitação).',
     'Implementado ✅'),
    ('Saneamento — Lixo inadequado',
     'V037–V042',
     'V00398–V00402',
     'V00001 (DPPO)',
     'Mesma lógica do 2010 com códigos atualizados.',
     'Implementado ✅'),
    ('Densidade habitacional',
     'Pop. / Dom. ocupados',
     '(V00005 + V00006) / (V00001 + V00002)',
     '—',
     'Reproduz a definição oficial do V0005 do IBGE.',
     'Implementado ✅'),
    ('Educação — analfabetismo',
     'V068–V134 (chefes < 4 anos de estudo)',
     'V00901 / (V00900 + V00901)',
     'V00900 + V00901 (pop. 15+)',
     'Censo 2022 não traz anos de instrução nos agregados → substituído por taxa de analfabetismo.',
     'Implementado ✅ (denominador corrigido em 22/05/2026)'),
    ('Renda',
     '% famílias ≤ 2 salários mínimos',
     'V06004 (rendimento médio, invertido)',
     '— (variável pronta)',
     'Censo 2022 não traz faixas salariais nos agregados → rendimento médio é a melhor aproximação.',
     'Pendente: normalização por município, não global ⚠️'),
    ('Raça/cor',
     'Pretos + pardos + indígenas',
     '(V01318 + V01320 + V01321) / v0001',
     'v0001 (pop. total)',
     'Mesma definição operacional; códigos do IBGE atualizados.',
     'Implementado ✅'),
    ('Coef. óbitos cardiovasculares',
     'Indicador presente no IVS-BH 2012',
     '— (não disponível)',
     '—',
     'O Censo 2022 só registra se houve óbito, sem causa. Buscar no DATASUS (SIM) em fase futura.',
     'Excluído do escopo atual ❌'),
]


def aba_de_para(wb):
    ws = wb.create_sheet('De_Para_2010_2022')
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = 'A4'

    write_title_block(ws, 1, 'Equivalência IVS-BH 2012 (Censo 2010) → Censo 2022', span=6)
    sub = ('Componentes do IVS-BH 2012 originais (Censo 2010) e suas contrapartes adotadas no projeto '
           'sobre o Censo 2022. Acrescenta limitações documentadas e status de implementação.')
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=6)
    c = ws.cell(row=2, column=1, value=sub)
    c.font = FONT_NOTE
    c.alignment = ALIGN_WRAP
    ws.row_dimensions[2].height = 26

    headers = ['Componente', 'Variável original (Censo 2010)', 'Variável adotada (Censo 2022)',
               'Denominador', 'Limitação / Observação', 'Status']
    widths = [28, 38, 38, 22, 50, 30]
    write_header_row(ws, 3, headers, widths)

    r = 4
    for idx, row in enumerate(DE_PARA):
        status = row[5]
        if '✅' in status:
            fill = FILL_OK
        elif '⚠️' in status:
            fill = FILL_WARN
        elif '❌' in status:
            fill = FILL_REJ
        else:
            fill = FILL_ZEBRA if idx % 2 == 1 else None
        write_body_row(ws, r, list(row), fill=fill)
        ws.row_dimensions[r].height = 56
        r += 1


# -----------------------------------------------------------------------------
# Aba 7 — Decisões metodológicas
# -----------------------------------------------------------------------------
DECISOES = [
    ('Denominador domiciliar',
     'V01042 (Total de Responsáveis)',
     'V00001 (Domicílios Particulares Permanentes Ocupados)',
     '2026-05-22',
     'Orientadora',
     'V01042 é uma contagem de PESSOAS no arquivo Parentesco — não de domicílios. '
     'V00001 é o equivalente exato do V002 (Dom_part_p) do Censo 2010, padrão do IVS-BH 2012.',
     'Implementado'),
    ('Taxa de analfabetismo',
     'V00901 / V00900',
     'V00901 / (V00900 + V00901)',
     '2026-05-22',
     'Revisão metodológica',
     'V00900 = 15+ que sabem ler; V00901 = 15+ que não sabem. O denominador correto da taxa '
     'é o total da população 15+, soma das duas. A versão antiga gerava 10 setores com taxa > 1.',
     'Implementado'),
    ('Razão de moradores',
     '(V00005 + V00006) / V01042',
     '(V00005 + V00006) / (V00001 + V00002)',
     '2026-05-22',
     'Revisão metodológica',
     'Reproduz a definição oficial do V0005 do IBGE (média de moradores em DPP Ocupados).',
     'Implementado'),
    ('Variáveis de esgoto inadequado',
     'Inconsistência no relatório legado (V00249–V00253 vs V00312–V00316)',
     'V00312–V00316',
     'pré 2026-05-22',
     'Dicionário oficial IBGE',
     'Dicionário confirma: V00312–V00316 é o bloco "Destinação do esgoto"; V00249–V00253 '
     'é tipologia de habitação (não tem relação direta com esgoto).',
     'Implementado'),
    ('Tratamento de sigilo em V00901',
     'Conversão para zero (imputação)',
     'Manter como NaN (transparente)',
     '2026-05-22',
     'Orientadora / discussão',
     'V00901 sigilada em ~15,76% dos setores ELSI OK, concentrado em capitais (BH 22%, '
     'Porto Alegre 27%, São Caetano do Sul 30%). Imputar zero subestimaria o analfabetismo '
     'em áreas com baixa vulnerabilidade educacional. Auditoria gravada em '
     'banco_de_dados/eda/auditoria_analfabetismo_municipio.csv.',
     'Implementado'),
    ('Filtro de elegibilidade Dados_sig',
     'Baseado em V01042 (Fase 2)',
     'Baseado em V00001 (Fase 3): SIGILOSO / COLETIVO / ZERADO / OK',
     '2026-05-22',
     'Revisão metodológica',
     'OK = v0001 > 0 AND V00001 > 0 AND ambos não-sigilosos. Resultado: 106.281 OK / 2.751 '
     'SIGILOSO (97,48% / 2,52%) entre os 109.032 setores dos 70 municípios ELSI.',
     'Implementado'),
    ('Normalização da renda',
     'Min-max global (Brasil inteiro nas Fases 1 e 2)',
     'Min-max POR MUNICÍPIO (para capturar desigualdade intraurbana)',
     'pendente',
     'Plano metodológico',
     'A normalização global apaga o contraste intraurbano, que é justamente o objetivo do projeto. '
     'Implementar antes do cálculo final do IVS.',
     'Pendente'),
    ('Análise fatorial / pesos do IVS',
     'IVS-BH 2012: pesos predefinidos (~60% socioeconômica / ~40% saneamento)',
     'A definir — pesos empíricos (ACP/AF) OU pesos guiados pela literatura',
     'pendente',
     'Plano metodológico',
     'Decisão pendente — referência: Matos & Rodrigues (2019). Resolver antes da redação dos resultados.',
     'Pendente'),
]


def aba_decisoes(wb):
    ws = wb.create_sheet('Decisoes_Metodologicas')
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = 'A4'

    write_title_block(ws, 1, 'Log de decisões metodológicas', span=7)
    sub = ('Histórico das principais decisões tomadas até hoje sobre seleção de variáveis, '
           'denominadores, fórmulas e tratamento de sigilo. Atualizar este log sempre que '
           'mudar uma decisão.')
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=7)
    c = ws.cell(row=2, column=1, value=sub)
    c.font = FONT_NOTE
    c.alignment = ALIGN_WRAP
    ws.row_dimensions[2].height = 28

    headers = ['Tópico', 'Versão anterior', 'Versão atual',
               'Data da decisão', 'Origem', 'Justificativa', 'Status']
    widths = [24, 38, 42, 16, 24, 60, 18]
    write_header_row(ws, 3, headers, widths)

    r = 4
    for idx, row in enumerate(DECISOES):
        status = row[6]
        if status == 'Implementado':
            fill = FILL_OK
        elif status == 'Pendente':
            fill = FILL_WARN
        else:
            fill = FILL_ZEBRA if idx % 2 == 1 else None
        write_body_row(ws, r, list(row), fill=fill)
        ws.row_dimensions[r].height = 72
        r += 1


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    wb = Workbook()
    # Remove a sheet default
    default = wb.active
    wb.remove(default)

    aba_inicio(wb)
    aba_componentes(wb)
    aba_variaveis_brutas(wb)
    aba_variaveis_derivadas(wb)
    aba_guia_por_arquivo(wb)
    aba_de_para(wb)
    aba_decisoes(wb)

    # Caminho de saída — raiz do projeto / docs/
    here = Path(__file__).resolve()
    # scripts/ está na raiz do projeto
    root = here.parent.parent
    out = root / 'docs' / 'Dicionario_Variaveis_IVS_Censo2022.xlsx'
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f'OK -> {out}')
    print(f'    {len(wb.sheetnames)} abas: {wb.sheetnames}')


if __name__ == '__main__':
    main()
