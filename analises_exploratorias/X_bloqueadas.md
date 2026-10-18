# Versões bloqueadas — dependem de dado que não temos

Nenhuma delas foi rodada. Cada uma diz o que falta e o que destravaria.

| Versão | O que falta | Como destravar |
|---|---|---|
| Análise espacial e mapas (autocorrelação espacial, LISA, mapas das faixas) | A malha geográfica dos setores censitários de 2022 (IBGE); não existe no computador (verificado em 05/10/2026) | Baixar a malha de setores do IBGE (pedido explícito de Pedro) e juntar por `CD_SETOR` |
| Comparação com o IVS-BH de 2010 | Compatibilização dos setores de 2010 com os de 2022 (mudaram de código e de limite) | Tabela de correspondência 2010–2022 do IBGE ou sobreposição das duas malhas |
| Validação com óbitos | O arquivo de óbitos dos agregados do Censo 2022 (93 variáveis por setor); não está em `dados/` | Baixar o arquivo de óbitos do IBGE (pedido explícito de Pedro) |
| Sigilosos imputados (renda e analfabetismo) | A decisão do método de imputação (mediana municipal, regressão, imputação múltipla) | Decisão da orientadora; o motor já aceita uma coluna nova por `indicadores_externos` |
| Domicílio, parte 3 | O arquivo de características do domicílio, parte 3; não está em `dados/` | Baixar o arquivo do IBGE (pedido explícito de Pedro) |
