# Resumo da ontologia
Gerado por resumo.py a partir de ontologia/ontologia.yaml. Não edite: regere.
Descrição de cada coluna: ontologia.yaml (leia só a tabela envolvida).

**Domínio:** Censo 2022 (IBGE), agregados por setor censitário dos 70 municípios da amostra ELSI-Brasil, com os indicadores do IVS calculados pela pipeline do projeto.

## Tabelas
- `setores_censitarios` — Setor censitário: uma linha por setor censitário (chave CD_SETOR)
- `dicionario_variaveis` — Variável do dicionário: uma linha por coluna de setores_censitarios (chave coluna)
- `metadados` — Metadado da base: uma linha por chave (chave chave)

## Recortes (filtros com nome)
- `analise`: Setores que entram nas análises do IVS: urbanos e elegíveis. Regra de Dados_sig corrigida em 09/08/2026 (população zero avaliada antes do sigilo). → `setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK'` [certificado]

## Métricas vigentes (use a expressão; aplique os filtros obrigatórios)
- `n_setores_recorte`: `COUNT(setores_censitarios.CD_SETOR)` [certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Recorte definido em metadados.recorte_de_analise.
- `media_pct_agua_inad`: `AVG(setores_censitarios.pct_agua_inad)` [certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Sigilo do IBGE: X vira NULL. Se só algumas parcelas do numerador são sigilosas, entram valendo zero (viés para baixo); se todas são, o setor fica NULL e sai do AVG (no recorte: 0). Média simples entre setores.
- `media_pct_esgoto_inad`: `AVG(setores_censitarios.pct_esgoto_inad)` [certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Sigilo do IBGE: X vira NULL. Se só algumas parcelas do numerador são sigilosas, entram valendo zero (viés para baixo); se todas são, o setor fica NULL e sai do AVG (no recorte: 1). Média simples entre setores.
- `media_pct_lixo_inad`: `AVG(setores_censitarios.pct_lixo_inad)` [certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Sigilo do IBGE: X vira NULL. Se só algumas parcelas do numerador são sigilosas, entram valendo zero (viés para baixo); se todas são, o setor fica NULL e sai do AVG (no recorte: 0). Média simples entre setores.
- `media_pct_analfab`: `AVG(setores_censitarios.pct_analfab)` [certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Média simples entre setores; NULL fica fora do AVG. Só 87.556 dos 104.108 setores do recorte têm valor (sigilo no denominador, ver a coluna pct_analfab).
- `media_pct_raca_pretpardind`: `AVG(setores_censitarios.pct_raca_pretpardind)` [certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Média simples entre setores; NULL fica fora do AVG.
- `media_razao_moradores`: `AVG(setores_censitarios.razao_moradores)` [certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Média simples entre setores; NULL fica fora do AVG.
- `media_renda`: `AVG(setores_censitarios.renda_media_sem_extremo)` [certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Use renda_media_sem_extremo (padrão das análises). renda_media original só para reproduzir resultados anteriores a 01/09/2026; renda_media_mediana_mun é variante de sensibilidade. Média simples entre setores; NULL fica fora do AVG.

## Códigos
- `setores_censitarios.SITUACAO`: Urbana = setor urbano; Rural = setor rural; NULL = massa d'água
- `setores_censitarios.CD_SIT`: 1-3 = urbana; 5-8 = rural; 9 = massa d'água (população zero)
- `setores_censitarios.CD_TIPO`: 0 = setor não especial; 1 = Favela e Comunidade Urbana (FCU); 2-9 = outros setores especiais
- `setores_censitarios.CD_FCU`: . = setor fora de FCU (marca de ausência; a coluna não tem NULL)
- `setores_censitarios.Moradia_Predominante`: Casa = V00047; Casa de Vila/Condomínio = V00048; Apartamento = V00049; Cortiço/Casa de Cômodos = V00050; Maloca Indígena = V00051 (não ocorre na base); Estrutura Degradada/Inacabada = V00052; Indefinido/Sem Moradia = sem domicílio permanente (2.751 na base; nenhum no recorte)
- `setores_censitarios.Dados_sig`: OK = elegível; SIGILOSO = população ou domicílios sigilosos; ZERADO = setor sem população; COLETIVO = população só em domicílios coletivos
- `setores_censitarios.urbano`: 1 = SITUACAO = Urbana; 0 = caso contrário
- `setores_censitarios.is_fcu`: 1 = setor de favela/comunidade urbana (CD_TIPO = 1); 0 = não FCU
- `setores_censitarios.Moradia_Predominante_Agrupada`: Convencional = Casa, Casa de Vila/Condomínio, Apartamento; Não convencional = Cortiço/Casa de Cômodos, Maloca Indígena, Estrutura Degradada/Inacabada; Indefinido = Indefinido/Sem Moradia (nenhum no recorte)
- `dicionario_variaveis.origem`: Censo 2022 (IBGE) = lida dos agregados do IBGE (71 colunas); Calculado pela pipeline = indicador com fórmula (28 colunas); Derivado pela pipeline = classificação ou código derivado, sem fórmula (9 colunas)

## Colunas com armadilha
- `setores_censitarios.NM_MUN`: Filtre por igualdade (NM_MUN = 'São Paulo'), nunca LIKE: existe 'São Paulo das Missões'.
- `setores_censitarios.NM_BAIRRO`: NULL em 41.431 setores do recorte (39,8%); em 34 dos 70 municípios nenhum setor do recorte tem bairro. Contagens por bairro deixam esses setores de fora.
- `setores_censitarios.CD_FCU`: Não use CD_FCU para contar favela: no projeto, favela é CD_TIPO = '1' (is_fcu). No recorte, 19 setores têm CD_FCU preenchido e CD_TIPO = '0' (25 na base); contar por CD_FCU <> '.' dá 19.471 setores, não 19.452. A ausência é '.', não NULL.
- `setores_censitarios.NM_FCU`: Preenchido exatamente onde CD_FCU <> '.' (19.471 setores no recorte, incluindo os 19 com CD_TIPO = '0'). Para contar favela, use CD_TIPO = '1' (is_fcu).
- `setores_censitarios.v0001`: Minúsculo: total de pessoas. Não confundir com V00001 (domicílios). Pode ser NULL por sigilo.
- `setores_censitarios.V00001`: Denominador domiciliar padrão. NULL em todos os setores SIGILOSO (1.015) e ZERADO (1.736) da base; no recorte nunca é NULL.
- `setores_censitarios.Dados_sig`: Regra (avaliada nesta ordem): ZERADO se v0001 = 0; SIGILOSO se v0001 ou V00001 é NULL; COLETIVO se V00001 = 0 com v0001 > 0; OK nos demais. COLETIVO não ocorre nesta base (0 setores). Base: OK 106.281, SIGILOSO 1.015, ZERADO 1.736; entre os urbanos: OK 104.108, SIGILOSO 766, ZERADO 1.473. Os indicadores (pct_*, razao_moradores, renda_media) só são calculados para OK: nos demais setores ficam NULL.
- `setores_censitarios.pct_agua_inad`, `setores_censitarios.pct_lixo_inad`, `setores_censitarios.pct_hab_precaria`, `setores_censitarios.pct_moradia_convencional`, `setores_censitarios.pct_moradia_nao_convencional`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, nenhum setor fica NULL. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_esgoto_inad`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 1 setor fica NULL, pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_analfab`: NULL quando qualquer parcela do denominador é sigilosa (min_count_den=2): no recorte, 16.552 setores (15,9%) ficam sem valor; em BH, ~22%.
- `setores_censitarios.renda_media`: Valor original com o setor extremo 310620005650366; as análises usam renda_media_sem_extremo. No recorte, 12 setores ficam NULL (V06004 ausente).
- `setores_censitarios.renda_media_sem_extremo`: Padrão das análises desde 01/09/2026.
- `setores_censitarios.renda_media_mediana_mun`: Variante de sensibilidade; o padrão das análises é renda_media_sem_extremo. Difere de renda_media em um setor só: 310620005650366 recebe 3.058,23 (mediana de Belo Horizonte no recorte, sem ele). No recorte, 12 setores ficam NULL (os mesmos de renda_media).
- `setores_censitarios.pct_raca_pretpardind`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 2 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_dom_improv`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 5.139 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_apartamento`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 9.103 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_casa`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 4.466 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_casa_vila_condominio`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 12.804 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_sem_agua_canalizada`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 41 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_agua_nao_encanada`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 9.706 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_agua_so_terreno`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 15.897 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_sem_banheiro`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 12.196 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_sem_banheiro_nem_sanitario`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 2.969 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_so_sanitario`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 3.811 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_banheiro_comum`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 9.694 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_resp_feminino`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 147 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_crianca_0a4`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 1.820 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_pop_0a14`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 258 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.pct_idoso_60mais`: NULL quando o denominador é zero ou sigiloso, ou quando todas as parcelas do numerador são sigilosas (com uma variável só no numerador, basta ela ser sigilosa). No recorte, 285 setores ficam NULL, sempre pelo numerador. Se só algumas parcelas são sigilosas, elas entram valendo zero (viés para baixo). NULL fica fora do AVG.
- `setores_censitarios.iep_setor`: Escala ×100, sem corte: chega a 4.750 no recorte, onde há poucos menores de 15. No recorte, 992 setores ficam NULL: 774 sem menores de 15 (denominador zero ou sigiloso) e 218 com o numerador sigiloso.
- `setores_censitarios.rdi_setor`: Escala ×100, sem corte: chega a 1.000 no recorte. No recorte, 298 setores ficam NULL: 17 com denominador zero ou sigiloso e 281 com o numerador sigiloso.
- `setores_censitarios.prop_70mais_entre_60mais`: Escala ×100, sem corte: vai de 0 a 100, não de 0 a 1. No recorte, 2.136 setores ficam NULL: 594 sem pessoas de 60+ (denominador zero ou sigiloso) e 1.542 com V01041 sigiloso.
- `metadados.valor`: Tudo é texto, e os números têm vírgula de milhar ('109,032'): CAST(valor AS INTEGER) dá 109. Use CAST(REPLACE(valor, ',', '') AS INTEGER). A chave setores_excluidos_de_renda_media_sem_extremo guarda o código do setor excluído (310620005650366), não uma contagem. O script da entrega foi corrigido em 23/11/2026 (números sem separador; a chave passa a cd_setor_excluido_de_renda_media_sem_extremo), mas este banco é de 22/10: a armadilha vale até ele ser regerado.

## Glossário (palavra do usuário → item)
- favela → `tabelas.setores_censitarios.colunas.is_fcu`
- comunidade urbana → `tabelas.setores_censitarios.colunas.is_fcu`
- domicílios → `tabelas.setores_censitarios.colunas.V00001`
- população → `tabelas.setores_censitarios.colunas.v0001`
- recorte de análise → `recortes.analise`
- setores analisados → `recortes.analise`
- analisados pelo IVS → `recortes.analise`
- análises do IVS → `recortes.analise`
- analfabetismo → `metricas.media_pct_analfab`
- renda → `metricas.media_renda`
- renda dos responsáveis → `metricas.media_renda`
- idosos → `tabelas.setores_censitarios.colunas.pct_idoso_60mais`
- água inadequada → `metricas.media_pct_agua_inad`
- esgoto inadequado → `metricas.media_pct_esgoto_inad`
- lixo inadequado → `metricas.media_pct_lixo_inad`
