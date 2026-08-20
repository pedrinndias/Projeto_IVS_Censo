import pandas as pd
import os

lista_caminho = [
    'Agregados_por_setores_alfabetizacao_BR.csv',
    'Agregados_por_setores_basico_BR_20250417.csv',
    'Agregados_por_setores_caracteristicas_domicilio1_BR.csv',
    'Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv',
    'Agregados_por_setores_caracteristicas_domicilio3_BR_20250417.csv',
    'Agregados_por_setores_cor_ou_raca_BR.csv',
    'Agregados_por_setores_demografia_BR.csv',
    'Agregados_por_setores_domicilios_indigenas_BR.csv',
    'Agregados_por_setores_domicilios_quilombolas_BR.csv',
    'Agregados_por_setores_obitos_BR.csv',
    'Agregados_por_setores_parentesco_BR.csv',
    'Agregados_por_setores_pessoas_indigenas_BR.csv',
    'Agregados_por_setores_pessoas_quilombolas_BR.csv',
    'Agregados_por_setores_renda_responsavel_BR.csv'
]

print("Iniciando a varredura dos arquivos CSV de forma otimizada...")

dados_resumo = []

for arquivo in lista_caminho:
    if not os.path.exists(arquivo):
        print(f"Aviso: O arquivo {arquivo} nao foi encontrado na pasta.")
        continue
        
    try:
        # Tenta ler com utf-8 primeiro, se der erro de codec, muda para latin1
        encoding_usado = 'utf-8'
        try:
            df_cols = pd.read_csv(arquivo, sep=';', nrows=0, encoding=encoding_usado)
            if df_cols.shape[1] == 1:
                df_cols = pd.read_csv(arquivo, sep=',', nrows=0, encoding=encoding_usado)
        except UnicodeDecodeError:
            encoding_usado = 'latin1'
            df_cols = pd.read_csv(arquivo, sep=';', nrows=0, encoding=encoding_usado)
            if df_cols.shape[1] == 1:
                df_cols = pd.read_csv(arquivo, sep=',', nrows=0, encoding=encoding_usado)
        
        # Pega a lista de colunas
        lista_colunas = df_cols.columns.tolist()
        colunas_juntas = " | ".join(lista_colunas)
        
        # Conta as linhas sem carregar o arquivo na memoria do Pandas e ignorando erros de codec
        numero_linhas = 0
        with open(arquivo, 'r', encoding=encoding_usado, errors='ignore') as f:
            numero_linhas = sum(1 for _ in f) - 1  # Subtrai 1 para nao contar o cabecalho
        
        dados_resumo.append({
            'Arquivo': arquivo,
            'Numero_de_Linhas': numero_linhas,
            'Colunas': colunas_juntas
        })
        
        print(f"Lido com sucesso: {arquivo} - Linhas: {numero_linhas}")
        
    except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo}. Erro: {e}")

if dados_resumo:
    try:
        df_resultado = pd.DataFrame(dados_resumo)
        df_resultado.to_csv('informacoes_agregados.csv', index=False, sep=';', encoding='utf-8-sig')
        print("\nProcesso concluido! O arquivo informacoes_agregados.csv foi gerado com sucesso.")
    except PermissionError:
        print("\nERRO: O arquivo informacoes_agregados.csv esta aberto no Excel. Feche-o e rode o codigo novamente!")
else:
    print("\nNenhum dado foi processado.")