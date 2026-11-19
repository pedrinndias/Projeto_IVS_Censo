# Resumo da ontologia
Gerado por resumo.py a partir de ontologia/ontologia.yaml. Não edite: regere.
Descrição de cada coluna: ontologia.yaml (leia só a tabela envolvida).

**Domínio:** Censo 2022 (IBGE), agregados por setor censitário dos 70 municípios da amostra ELSI-Brasil, com os indicadores do IVS calculados pela pipeline do projeto.

## Tabelas
- `setores_censitarios` — Setor censitário: uma linha por setor censitário (chave CD_SETOR)
- `dicionario_variaveis` — Variável do dicionário: uma linha por coluna de setores_censitarios (chave coluna)
- `metadados` — Metadado da base: uma linha por chave (chave chave)

## Recortes (filtros com nome)
- `analise`: Setores que entram nas análises do IVS: urbanos e elegíveis. Regra de Dados_sig corrigida em 09/08/2026 (população zero avaliada antes do sigilo). → `setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK'` [não certificado]

## Métricas vigentes (use a expressão; aplique os filtros obrigatórios)
- `n_setores_recorte`: `COUNT(setores_censitarios.CD_SETOR)` [não certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Recorte definido em metadados.recorte_de_analise.
- `media_pct_agua_inad`: `AVG(setores_censitarios.pct_agua_inad)` [não certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Sigilo do IBGE: X vira NULL; parcelas sigilosas entram valendo zero no numerador (viés para baixo). Média simples entre setores; NULL fica fora do AVG.
- `media_pct_esgoto_inad`: `AVG(setores_censitarios.pct_esgoto_inad)` [não certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Sigilo do IBGE: X vira NULL; parcelas sigilosas entram valendo zero no numerador (viés para baixo). Média simples entre setores; NULL fica fora do AVG.
- `media_pct_lixo_inad`: `AVG(setores_censitarios.pct_lixo_inad)` [não certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Sigilo do IBGE: X vira NULL; parcelas sigilosas entram valendo zero no numerador (viés para baixo). Média simples entre setores; NULL fica fora do AVG.
- `media_pct_analfab`: `AVG(setores_censitarios.pct_analfab)` [não certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Média simples entre setores; NULL fica fora do AVG.
- `media_pct_raca_pretpardind`: `AVG(setores_censitarios.pct_raca_pretpardind)` [não certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Média simples entre setores; NULL fica fora do AVG.
- `media_razao_moradores`: `AVG(setores_censitarios.razao_moradores)` [não certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Média simples entre setores; NULL fica fora do AVG.
- `media_renda`: `AVG(setores_censitarios.renda_media_sem_extremo)` [não certificado]
  - filtros obrigatórios: analise (setores_censitarios.SITUACAO = 'Urbana' AND setores_censitarios.Dados_sig = 'OK')
  - armadilhas: Use renda_media_sem_extremo (padrão das análises). renda_media original só para reproduzir resultados anteriores a 01/09/2026; renda_media_mediana_mun é variante de sensibilidade. Média simples entre setores; NULL fica fora do AVG.

## Códigos
- `setores_censitarios.SITUACAO`: Urbana = setor urbano; Rural = setor rural; NULL = massa d'água
- `setores_censitarios.CD_SIT`: 1-3 = urbana; 5-8 = rural; 9 = massa d'água (população zero)
- `setores_censitarios.CD_TIPO`: 0 = setor não especial; 1 = Favela e Comunidade Urbana (FCU); 2-9 = outros setores especiais
- `setores_censitarios.Dados_sig`: OK = elegível; SIGILOSO = população ou domicílios sigilosos; ZERADO = setor sem população; COLETIVO = população só em domicílios coletivos
- `setores_censitarios.urbano`: 1 = SITUACAO = Urbana; 0 = caso contrário
- `setores_censitarios.is_fcu`: 1 = setor de favela/comunidade urbana (CD_TIPO = 1); 0 = não FCU

## Colunas com armadilha
- `setores_censitarios.NM_MUN`: Filtre por igualdade (NM_MUN = 'São Paulo'), nunca LIKE: existe 'São Paulo das Missões'.
- `setores_censitarios.v0001`: Minúsculo: total de pessoas. Não confundir com V00001 (domicílios). Pode ser NULL por sigilo.
- `setores_censitarios.V00001`: Denominador domiciliar padrão. Pode ser NULL por sigilo (setor fica SIGILOSO).
- `setores_censitarios.pct_agua_inad`, `setores_censitarios.pct_esgoto_inad`, `setores_censitarios.pct_lixo_inad`, `setores_censitarios.pct_raca_pretpardind`, `setores_censitarios.pct_dom_improv`, `setores_censitarios.pct_hab_precaria`, `setores_censitarios.pct_moradia_convencional`, `setores_censitarios.pct_moradia_nao_convencional`, `setores_censitarios.pct_apartamento`, `setores_censitarios.pct_casa`, `setores_censitarios.pct_casa_vila_condominio`, `setores_censitarios.pct_sem_agua_canalizada`, `setores_censitarios.pct_agua_nao_encanada`, `setores_censitarios.pct_agua_so_terreno`, `setores_censitarios.pct_sem_banheiro`, `setores_censitarios.pct_sem_banheiro_nem_sanitario`, `setores_censitarios.pct_so_sanitario`, `setores_censitarios.pct_banheiro_comum`, `setores_censitarios.pct_resp_feminino`, `setores_censitarios.pct_crianca_0a4`, `setores_censitarios.pct_pop_0a14`, `setores_censitarios.pct_idoso_60mais`: NULL quando o denominador é zero ou sigiloso; parcelas sigilosas do numerador entram valendo zero (viés para baixo).
- `setores_censitarios.pct_analfab`: NULL quando qualquer parcela do denominador é sigilosa (min_count_den=2): em BH, ~22% dos setores do recorte ficam sem valor.
- `setores_censitarios.renda_media`: Valor original com o setor extremo 310620005650366; as análises usam renda_media_sem_extremo.
- `setores_censitarios.renda_media_sem_extremo`: Padrão das análises desde 01/09/2026.

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
