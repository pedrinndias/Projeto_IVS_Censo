# Perguntas para a orientadora — parâmetros exploratórios

Cada linha é um parâmetro que ninguém fixou. A versão roda com o valor-padrão do prompt
(seção 2.3), rotulado no deck como **parâmetro exploratório — não é decisão**.

| Versão | Parâmetro | Valor usado | Alternativa registrada | Pergunta |
|---|---|---|---|---|
| A2_piso_populacional | Piso de população do setor | 50 moradores | 100 moradores (tabela T34) | Deve haver piso de população para o setor entrar no índice? Se sim, qual? |
| A5_por_porte | Faixas de porte do município | até 100 mil, de 100 a 500 mil, mais de 500 mil habitantes | — | As faixas de porte servem? A população é a soma dos moradores dos setores da base (Censo 2022). |
| C4_agregacao | Deslocamento da média geométrica | 0,01 somado a cada componente normalizado | — | Média geométrica serve? Com que tratamento para os zeros do min-max? |
| C5_faixas | Número de grupos do agrupamento | o da silhueta entre 3 e 6 (e sempre 4) | quebras naturais por k-médias 1D com 4 classes | Faz sentido classificar por agrupamento em vez de por regra? Quantas classes? |
| D2_ivs_idoso | Composição do IVS-Idoso | 7 componentes + % 60+, IEP e RDI; 3 fatores; pesos pela fatorial | 2 fatores (T34) | O envelhecimento entra como dimensão do índice ou como estrato/cruzamento (E5)? |
| D3_indice_moradia | Composição do índice de moradia | razão de moradores, improvisado, habitação precária, não convencional, banheiro de uso comum | — | Que variáveis definem moradia inadequada para o projeto? |
| D4_ibp_aproximado | Variáveis do IBP aproximado | renda do responsável, analfabetismo 15+, saneamento médio | — | As aproximações servem? Faltam renda per capita até ½ SM e analfabetismo 7+ nos agregados de 2022. |
| E2_estabilidade | Reamostragens | 1.000, semente 42 | — | O número de reamostragens é suficiente? |
| E6_tipologias | Número de grupos | o da silhueta entre 3 e 6 (e sempre 4) | — | Tipologias entram no artigo? Com quantos grupos? |
