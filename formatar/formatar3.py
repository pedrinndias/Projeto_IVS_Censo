import pandas as pd
import os

print("Iniciando a criacao do relatorio modular...")

try:
    caminho_dic_geral = 'dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx'
    caminho_dic_renda = 'dicionario_de_dados_renda_responsavel.xlsx'

    abas_geral = ['Dicionário Básico', 'Dicionário não PCT', 'Dicionário PCT - Indígenas', 'Dicionário PCT - Quilombolas']
    lista_dicionarios = []

    for aba in abas_geral:
        try:
            df_temp = pd.read_excel(caminho_dic_geral, sheet_name=aba)
            if 'Variável' in df_temp.columns and 'Descrição' in df_temp.columns:
                colunas_pegar = ['Variável', 'Descrição']
                if 'Tema' in df_temp.columns:
                    colunas_pegar.append('Tema')
                lista_dicionarios.append(df_temp[colunas_pegar])
        except Exception as e:
            pass

    try:
        df_renda = pd.read_excel(caminho_dic_renda, sheet_name='Dicionário Renda Responsável')
        if 'Variável' in df_renda.columns and 'Descrição' in df_renda.columns:
            colunas_pegar = ['Variável', 'Descrição']
            if 'Tema' in df_renda.columns:
                colunas_pegar.append('Tema')
            lista_dicionarios.append(df_renda[colunas_pegar])
    except Exception as e:
        pass

    df_dic_unificado = pd.concat(lista_dicionarios, ignore_index=True)
    df_dic_unificado = df_dic_unificado.drop_duplicates(subset=['Variável'])
    
    mapa_descricoes = dict(zip(df_dic_unificado['Variável'], df_dic_unificado['Descrição']))
    if 'Tema' in df_dic_unificado.columns:
        mapa_temas = dict(zip(df_dic_unificado['Variável'], df_dic_unificado['Tema']))
    else:
        mapa_temas = {}

    df_info = pd.read_csv('informacoes_agregados.csv', sep=';')
    
    nome_saida = 'Relatorio_Modular_Variaveis.xlsx'
    
    with pd.ExcelWriter(nome_saida, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        formato_cabecalho = workbook.add_format({
            'bold': True, 'fg_color': '#1F497D', 'font_color': 'white', 'border': 1
        })
        formato_celula = workbook.add_format({'text_wrap': True, 'valign': 'top', 'border': 1})
        
        for index, row in df_info.iterrows():
            arquivo = row['Arquivo']
            colunas = str(row['Colunas']).split(' | ')
            
            nome_aba = arquivo.replace('Agregados_por_setores_', '').replace('_BR.csv', '').replace('_BR_20250417.csv', '').replace('.csv', '')
            # O Excel tem limite de 31 caracteres para o nome da aba
            nome_aba = nome_aba[:31]
            
            dados_aba = []
            for col in colunas:
                col_limpa = col.strip()
                descricao = mapa_descricoes.get(col_limpa, 'Sem descricao no dicionario')
                tema = mapa_temas.get(col_limpa, 'Geral')
                
                # Identifica se é uma coluna geográfica/texto ou numérica (a maioria)
                if col_limpa in ['CD_setor', 'CD_SETOR', 'AREA_KM2', 'NOME_UF', 'CD_UF']:
                    tipo_resposta = 'Texto/Geografico (Identificador)'
                    descricao = 'Coluna de identificacao territorial'
                else:
                    tipo_resposta = 'Numero (Contagem ou Media)'
                    
                dados_aba.append({
                    'Código da Variável': col_limpa,
                    'Tema Original': tema,
                    'Descrição / Significado': descricao,
                    'Tipo de Resposta': tipo_resposta
                })
                
            df_aba = pd.DataFrame(dados_aba)
            df_aba.to_excel(writer, sheet_name=nome_aba, index=False)
            
            worksheet = writer.sheets[nome_aba]
            for col_num, value in enumerate(df_aba.columns.values):
                worksheet.write(0, col_num, value, formato_cabecalho)
                
            worksheet.set_column('A:A', 20, formato_celula)
            worksheet.set_column('B:B', 30, formato_celula)
            worksheet.set_column('C:C', 85, formato_celula)
            worksheet.set_column('D:D', 30, formato_celula)
            worksheet.freeze_panes(1, 0)
            worksheet.autofilter(0, 0, len(df_aba), len(df_aba.columns) - 1)

    print("Sucesso! O arquivo " + nome_saida + " foi criado em modulos separados.")

except PermissionError:
    print("ERRO: O arquivo Excel de saida esta aberto no seu computador. Feche-o e tente de novo.")
except Exception as e:
    print("Ocorreu um erro inesperado: " + str(e))