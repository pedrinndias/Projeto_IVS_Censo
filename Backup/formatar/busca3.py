import pandas as pd

print("Gerando o relatorio metodologico corrigido...")

# 1. Dados da Comparação de Variáveis (De/Para)
dados_comparacao = [
    {
        'Componente IVS': 'Saneamento: Água Inadequada',
        'O que o IVS 2012 pedia (Censo 2010)': 'V013 (poço/nascente), V014 (chuva), V015 (outra forma)',
        'Variáveis Censo 2022 Equivalentes': 'V00112 (poço profundo), V00113 (poço raso), V00114 (nascente), V00115 (carro-pipa), V00116 (chuva), V00117 (rios/lagos), V00118 (outra forma)',
        'Observação Metodológica': 'O IBGE detalhou as fontes no Censo 2022. O somatório destas 7 novas variáveis substitui as 3 antigas.'
    },
    {
        'Componente IVS': 'Saneamento: Esgoto Inadequado',
        'O que o IVS 2012 pedia (Censo 2010)': 'V019 a V028 (separava detalhadamente quem tinha banheiro e quem não tinha)',
        'Variáveis Censo 2022 Equivalentes': 'V00249 (fossa rudimentar), V00250 (vala), V00251 (rio/lago), V00252 (outra forma), V00253 (inexistente)',
        'Observação Metodológica': 'A questão do banheiro foi simplificada. O agrupamento destas 5 variáveis reflete o risco sanitário.'
    },
    {
        'Componente IVS': 'Saneamento: Lixo Inadequado',
        'O que o IVS 2012 pedia (Censo 2010)': 'V037 (caçamba), V038 (queimado), V039 (enterrado), V040 (baldio), V041 (rio/lago), V042 (outro)',
        'Variáveis Censo 2022 Equivalentes': 'V00398 (caçamba), V00399 (queimado), V00400 (enterrado), V00401 (terreno baldio/área pública), V00402 (outro destino)',
        'Observação Metodológica': 'Corrigido: Adicionada a variável V00398 referente a Lixo depositado em caçamba de serviço de limpeza.'
    },
    {
        'Componente IVS': 'Educação: Analfabetismo',
        'O que o IVS 2012 pedia (Censo 2010)': 'V068 a V134 (Contagem de moradores que não sabiam ler)',
        'Variáveis Censo 2022 Equivalentes': 'V00658 a V00671',
        'Observação Metodológica': 'Somatório de pessoas que não sabem ler e escrever agrupadas por faixas etárias a partir dos 15 anos.'
    },
    {
        'Componente IVS': 'Renda: Vulnerabilidade Econômica',
        'O que o IVS 2012 pedia (Censo 2010)': 'Percentual de famílias com renda até 2 salários mínimos e renda média',
        'Variáveis Censo 2022 Equivalentes': 'V06004 (Rendimento nominal médio mensal do responsável)',
        'Observação Metodológica': 'Adicionado setor de Renda. A divisão exata por faixas de salário mínimo não está na base, utilizaremos a média (V06004).'
    },
    {
        'Componente IVS': 'Habitação: Razão de Moradores',
        'O que o IVS 2012 pedia (Censo 2010)': 'Divisão da população total pelos domicílios ocupados',
        'Variáveis Censo 2022 Equivalentes': 'V0005 (Média de moradores em Domicílios Particulares Ocupados)',
        'Observação Metodológica': 'O IBGE entrega o cálculo exato da densidade domiciliar pronto nesta variável do arquivo básico.'
    },
    {
        'Componente IVS': 'Social: Cor ou Raça',
        'O que o IVS 2012 pedia (Censo 2010)': 'Somatório de pessoas declaradas pretas, pardas e indígenas',
        'Variáveis Censo 2022 Equivalentes': 'V01318 (preta), V01320 (parda), V01321 (indígena)',
        'Observação Metodológica': 'O conceito se manteve idêntico ao Censo 2010.'
    },
    {
        'Componente IVS': 'Denominadores Globais (As bases de cálculo)',
        'O que o IVS 2012 pedia (Censo 2010)': 'V001 (População Total) e V002 (Domicílios Particulares Permanentes)',
        'Variáveis Censo 2022 Equivalentes': 'v0001 (População - Arquivo Básico) e V00001 (Domicílios Permanentes - Arq. Domicilio1)',
        'Observação Metodológica': 'Variáveis obrigatórias que serão usadas para dividir os indicadores de risco e gerar as porcentagens.'
    }
]

# 2. Dados do que NÃO foi encontrado (Limitações)
dados_nao_encontrados = [
    {
        'Item Exigido no IVS 2012': 'Percentual de chefes de família com menos de 4 anos de estudo',
        'Limitação no Censo 2022 Agregado': 'Os dados de anos de instrução ainda não foram disponibilizados pelo IBGE nos arquivos agregados de 2022.',
        'Impacto no Projeto': 'Alto (Defasagem em Escolaridade)',
        'Solução Proposta': 'Substituir temporariamente pela taxa de analfabetismo geral (V00658 a V00671) para compor a dimensão educacional.'
    },
    {
        'Item Exigido no IVS 2012': 'Percentual de chefes de família com renda de até 2 salários mínimos',
        'Limitação no Censo 2022 Agregado': 'A contagem absoluta de domicílios dividida por faixas de salário mínimo não está na base preliminar.',
        'Impacto no Projeto': 'Alto',
        'Solução Proposta': 'Utilizar o Rendimento nominal médio (V06004) do setor como substituto para identificar áreas de menor renda.'
    },
    {
        'Item Exigido no IVS 2012': 'Coeficiente de óbitos por doenças cardiovasculares',
        'Limitação no Censo 2022 Agregado': 'O IBGE registrou apenas se houve óbito, não perguntando a causa mortis.',
        'Impacto no Projeto': 'Médio',
        'Solução Proposta': 'Capturar os dados de mortalidade via DATASUS (Sistema SIM) e cruzar espacialmente no QGIS.'
    }
]

# 3. Mapa de Arquivos (Aonde estão as variáveis)
dados_mapa_arquivos = [
    {
        'Arquivo do Censo 2022': 'Agregados_por_setores_caracteristicas_domicilio1_BR.csv',
        'Dimensão do IVS': 'Denominador Habitacional',
        'Variáveis Alvo a Extrair': 'V00001 (Total de Domicílios Permanentes)',
        'Descrição Resumida': 'Onde vamos buscar a base de divisão para as fórmulas de saneamento.'
    },
    {
        'Arquivo do Censo 2022': 'Agregados_por_setores_caracteristicas_domicilio2_BR.csv',
        'Dimensão do IVS': 'Saneamento Básico e Habitação',
        'Variáveis Alvo a Extrair': 'V00112 a V00118 (Água), V00249 a V00253 (Esgoto), V00398 a V00402 (Lixo)',
        'Descrição Resumida': 'Concentra os numeradores de infraestrutura e destinação de resíduos.'
    },
    {
        'Arquivo do Censo 2022': 'Agregados_por_setores_alfabetizacao_BR.csv',
        'Dimensão do IVS': 'Educação / Escolaridade',
        'Variáveis Alvo a Extrair': 'V00658 a V00671',
        'Descrição Resumida': 'Contagem de analfabetismo por idade.'
    },
    {
        'Arquivo do Censo 2022': 'Agregados_por_setores_cor_ou_raca_BR.csv',
        'Dimensão do IVS': 'Vulnerabilidade Social',
        'Variáveis Alvo a Extrair': 'V01318, V01320, V01321',
        'Descrição Resumida': 'Contagem de raças para a dimensão demográfica.'
    },
    {
        'Arquivo do Censo 2022': 'Agregados_por_setores_basico_BR_20250417.csv',
        'Dimensão do IVS': 'Filtros, Densidade e População Base',
        'Variáveis Alvo a Extrair': 'CD_SETOR, v0001 (Pop. Total), V0005 (Média moradores)',
        'Descrição Resumida': 'A espinha dorsal do banco para identificar as áreas e aplicar os filtros de exclusão.'
    },
    {
        'Arquivo do Censo 2022': 'Agregados_por_setores_renda_responsavel_BR.csv',
        'Dimensão do IVS': 'Vulnerabilidade Econômica',
        'Variáveis Alvo a Extrair': 'V06004',
        'Descrição Resumida': 'Base para a composição da renda média.'
    }
]

# Criando os DataFrames
df_comparacao = pd.DataFrame(dados_comparacao)
df_nao_encontrados = pd.DataFrame(dados_nao_encontrados)
df_mapa = pd.DataFrame(dados_mapa_arquivos)

arquivo_saida = 'Relatorio_Metodologico_IVS_2022_Corrigido.xlsx'

try:
    with pd.ExcelWriter(arquivo_saida, engine='xlsxwriter') as writer:
        df_comparacao.to_excel(writer, sheet_name='De_Para_Variaveis', index=False)
        df_nao_encontrados.to_excel(writer, sheet_name='Limitacoes_e_Ausencias', index=False)
        df_mapa.to_excel(writer, sheet_name='Mapa_de_Arquivos', index=False)
        
        workbook = writer.book
        formato_cabecalho = workbook.add_format({'bold': True, 'fg_color': '#1F497D', 'font_color': 'white', 'border': 1, 'text_wrap': True, 'valign': 'top'})
        formato_celula = workbook.add_format({'text_wrap': True, 'valign': 'top', 'border': 1})
        
        # Formatando Aba 1
        ws1 = writer.sheets['De_Para_Variaveis']
        for col_num, value in enumerate(df_comparacao.columns.values):
            ws1.write(0, col_num, value, formato_cabecalho)
        ws1.set_column('A:A', 30, formato_celula)
        ws1.set_column('B:B', 45, formato_celula)
        ws1.set_column('C:C', 55, formato_celula)
        ws1.set_column('D:D', 45, formato_celula)
        
        # Formatando Aba 2
        ws2 = writer.sheets['Limitacoes_e_Ausencias']
        for col_num, value in enumerate(df_nao_encontrados.columns.values):
            ws2.write(0, col_num, value, formato_cabecalho)
        ws2.set_column('A:A', 35, formato_celula)
        ws2.set_column('B:B', 50, formato_celula)
        ws2.set_column('C:C', 20, formato_celula)
        ws2.set_column('D:D', 50, formato_celula)
        
        # Formatando Aba 3
        ws3 = writer.sheets['Mapa_de_Arquivos']
        for col_num, value in enumerate(df_mapa.columns.values):
            ws3.write(0, col_num, value, formato_cabecalho)
        ws3.set_column('A:A', 50, formato_celula)
        ws3.set_column('B:B', 30, formato_celula)
        ws3.set_column('C:C', 45, formato_celula)
        ws3.set_column('D:D', 45, formato_celula)
        
    print("Sucesso! O relatorio corrigido foi gerado com todas as variaveis base inseridas.")
    
except Exception as e:
    print("Ocorreu um erro ao gerar o relatorio: " + str(e))