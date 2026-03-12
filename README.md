# Projeto_IVS_Censo

## Objetivo
Projeto para processamento, análise e cálculo do Índice de Vulnerabilidade Social (IVS) a partir dos dados do Censo 2022. Inclui etapas de ETL, auditoria, extração de variáveis, cálculo de indicadores e geração de relatórios.

## Estrutura de Pastas
- **data/**: Dados intermediários/processados
- **banco_de_dados/**: Dados brutos e bases analíticas
- **dados/**: Dados agregados por setor censitário
- **processed/**: Dados finais e formatados
- **output/**: Resultados, relatórios e arquivos gerados
- **src/**: Scripts e código-fonte (ETL, formatação, tradução, etc)
- **notebooks/**: Jupyter Notebooks para cada etapa do fluxo
- **docs/**: Documentação, dicionários e relatórios metodológicos
- **tests/**: Scripts de teste (se houver)
- **requirements.txt**: Dependências Python
- **estrutura_projeto.md**: Detalhes da estrutura

## Principais Notebooks
- **01_Unificacao_Base_Censo.ipynb**: Unificação das tabelas do censo e criação do banco SQLite
- **02_Extracao_Variaveis_Alvo.ipynb**: Extração e exportação das variáveis alvo
- **03_Auditoria_Dados.ipynb**: Auditoria de integridade dos arquivos
- **04_Calculo_Final_IVS.ipynb**: Cálculo dos indicadores IVS
- **05_Formatacao_e_Dicionarios.ipynb**: Geração de dicionários, validação estatística e exportação para Excel

## Scripts Importantes
- **src/ETL/mapeamento_variaveis.py**: Mapeamento de variáveis do censo
- **src/formatador_excel.py**: Formatação avançada de arquivos Excel
- **src/tradutor_ibge.py**: Tradução e busca de variáveis nos dicionários do IBGE
- **unificar.py**: Unificação de arquivos CSV e geração de base final

## Como Executar
1. Instale as dependências:
	```
	pip install -r requirements.txt
	```
2. Execute os notebooks na ordem sugerida para processar os dados e gerar os resultados.
3. Utilize os scripts em src/ para tarefas específicas de formatação, tradução e auditoria.

## Dados e Resultados
- Dados brutos: banco_de_dados/, dados/
- Dados processados: processed/, data/
- Resultados finais: output/
- Documentação e dicionários: docs/

## Créditos
Autor: Pedro Dias Soares
Licença: MIT (ver LICENSE)

---
Para dúvidas ou sugestões, consulte a documentação em docs/ ou entre em contato.