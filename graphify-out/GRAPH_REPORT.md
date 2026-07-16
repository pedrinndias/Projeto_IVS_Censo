# Graph Report - .  (2026-07-07)

## Corpus Check
- 28 files · ~144,464 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 188 nodes · 258 edges · 16 communities (15 shown, 1 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.88)
- Token cost: 417,007 input · 0 output

## Community Hubs (Navigation)
- Metodologia IVS-BH e Referências
- Variáveis-Componente e Decisões Metodológicas
- Métodos Estatísticos e Análise Fatorial
- Desenho Amostral ELSI e Plano do Artigo
- Pipeline de Dados e Histórico do Projeto
- Testes da Pipeline (Fase 3)
- Figura: Histogramas das Variáveis
- Figura: Boxplots Regionais
- Figura: Matriz de Correlação
- Redação e Saídas da EDA
- Dicionário de Dados do Censo 2022
- Figura: Heatmap de Dados Faltantes
- Regra IQR e Tratamento de Outliers

## God Nodes (most connected - your core abstractions)
1. `Notebook 02 — Análises Descritivas (EDA)` - 15 edges
2. `Plano de trabalho do bolsista (IC Fiocruz Minas)` - 15 edges
3. `Histogramas — 7 variáveis-componente do IVS (setores OK, 70 municípios ELSI)` - 11 edges
4. `Notebook 01 — Extração e Filtragem ELSI` - 10 edges
5. `Relatório de EDA Fase 3 — IVS Censo 2022 / ELSI (versão convertida)` - 10 edges
6. `Figura: Boxplots por região — variáveis-componente do IVS` - 10 edges
7. `Matriz de Correlação Pearson/Spearman dos Indicadores de Vulnerabilidade` - 10 edges
8. `Projeto IVS Censo 2022` - 9 edges
9. `IVS-BH 2012 (SMS Belo Horizonte, 2013)` - 9 edges
10. `GUIA_DO_PROJETO — documento mestre de retomada` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Plano de trabalho do bolsista (IC Fiocruz Minas)` --semantically_similar_to--> `GUIA_DO_PROJETO — documento mestre de retomada`  [INFERRED] [semantically similar]
  docs/Plano de trabalho.pdf → GUIA_DO_PROJETO.md
- `Ponderação participativa par-a-par (IVS-BH)` --semantically_similar_to--> `Análise fatorial / ACP para definição dos pesos do IVS`  [INFERRED] [semantically similar]
  docs/indice_vulnerabilidade2012 (2).pdf → GUIA_DO_PROJETO.md
- `Plano de trabalho do bolsista (IC Fiocruz Minas)` --references--> `ELSI-Brasil — amostra dos 70 municípios`  [EXTRACTED]
  docs/Plano de trabalho.pdf → README.md
- `Plano de trabalho do bolsista (IC Fiocruz Minas)` --cites--> `Caiaffa et al. 2021 — Saúde urbana, cidades e a interseção de sistemas`  [EXTRACTED]
  docs/Plano de trabalho.pdf → README.md
- `GUIA_DO_PROJETO — documento mestre de retomada` --references--> `Categorização do IVS em 4 faixas de risco`  [EXTRACTED]
  GUIA_DO_PROJETO.md → docs/indice_vulnerabilidade2012 (2).pdf

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **As 7 variáveis-componente do IVS** — banco_de_dados_entrega_orientadora_readme_pct_agua_inad, banco_de_dados_entrega_orientadora_readme_pct_esgoto_inad, banco_de_dados_entrega_orientadora_readme_pct_lixo_inad, banco_de_dados_entrega_orientadora_readme_razao_moradores, banco_de_dados_entrega_orientadora_readme_pct_analfab, banco_de_dados_entrega_orientadora_readme_renda_media, banco_de_dados_entrega_orientadora_readme_pct_raca_pretpardind, readme_ivs_intraurbano [EXTRACTED 1.00]
- **Fluxo de dados da pipeline Fase 3** — estrutura_projeto_8_csvs_censo2022, dados_municipios_elsi_brasil, notebooks_fase3_eda_elsi_01_extracao_filtragem_elsi, banco_de_dados_base_elsi_bruta_censo2022, notebooks_fase3_eda_elsi_02_analises_descritivas, banco_de_dados_eda_readme_saidas_eda [EXTRACTED 1.00]
- **Fundamentação metodológica central do projeto** — docs_indice_vulnerabilidade2012__2__ivs_bh_2012, readme_isu_passarelli_araujo_2023, readme_caiaffa_2021, readme_buss_pellegrini_2007, readme_matos_rodrigues_2019 [EXTRACTED 1.00]
- **Desenho amostral complexo do ELSI-Brasil** — elsi_amostra_desenho_estagios, elsi_amostra_lavallee_hidiroglou, elsi_amostra_amostragem_inversa, elsi_amostra_ponderacao [EXTRACTED 1.00]
- **Eixo socioeconômico latente (renda × analfabetismo × raça/cor)** — rel_eda_conv_renda_ppi_correlacao, rel_eda_conv_dois_fatores_latentes, plano_artigo_raca_proxy, plano_artigo_analise_fatorial [INFERRED 0.85]
- **Pipeline metodológico do IVS (dicionário → decisões → EDA → índice)** — dic_agregados_v00001, rel_eda_conv_denominador_v00001, rel_eda_conv_setores_ok, plano_artigo_analise_fatorial, plano_artigo_categorizacao_4_faixas [INFERRED 0.85]

## Communities (16 total, 1 thin omitted)

### Community 0 - "Metodologia IVS-BH e Referências"
Cohesion: 0.10
Nodes (28): Avaliação do IVS-BH por desfechos de saúde (gradiente dose-resposta), Categorização do IVS em 4 faixas de risco, IVS-BH 2012 (SMS Belo Horizonte, 2013), Padronização min-max 0-1, Ponderação participativa par-a-par (IVS-BH), Plano de trabalho do bolsista (IC Fiocruz Minas), Agero et al. 2020 — Desafios do envelhecimento populacional, Allik et al. 2020 — Small-area deprivation measure for Brazil (+20 more)

### Community 1 - "Variáveis-Componente e Decisões Metodológicas"
Cohesion: 0.11
Nodes (27): Inconsistência histórica das variáveis de esgoto (V00312-V00316 vs V00249-V00253), Normalização de renda global (problema), pct_agua_inad — % domicílios com água inadequada, pct_analfab — taxa de analfabetismo 15+, pct_esgoto_inad — % domicílios com esgoto inadequado, pct_lixo_inad — % domicílios com lixo inadequado, pct_raca_pretpardind — % pretos, pardos e indígenas, razao_moradores — razão de moradores por domicílio (+19 more)

### Community 2 - "Métodos Estatísticos e Análise Fatorial"
Cohesion: 0.10
Nodes (23): Dicionário de dados Renda do Responsável (Censo 2022 IBGE), V06004 — Valor do rendimento nominal médio mensal das pessoas responsáveis, Quarteto de Anscombe e Datasaurus — visualizar sempre antes de confiar em estatísticas, Box plot — leitura de assimetria por mediana e quartis; regra 1,5·IQR para outliers, Coeficiente de correlação de Pearson (r) — associação linear paramétrica, Coeficiente de correlação de Spearman (rₛ) — não-paramétrico, robusto à assimetria, Guia completo de Análise Exploratória e Estatística (FIOCRUZ, Módulos 2 e 3), Análise Exploratória de Dados (EDA) — etapa prévia à modelagem (+15 more)

### Community 3 - "Desenho Amostral ELSI e Plano do Artigo"
Cohesion: 0.10
Nodes (22): Componente Saneamento (água, esgoto, lixo inadequados) — IVS-BH, Componentes socioeconômicos (habitação, escolaridade, renda, social) — IVS-BH, Conversão de escala min-max: (valor bruto − mínimo) / (máximo − mínimo), Classificação Dados_sig (SIGILOSO / COLETIVO / ZERADO / OK) para elegibilidade do setor, Cálculo IVS 2012 (documento operacional SMS-BH), Tratamento de domicílios coletivos: usa número de responsáveis como total de domicílios; exclui setores 100% coletivos, Lixo em caçamba de serviço de limpeza (V037) contabilizado no destino inadequado — decisão intencional do IVS-BH, 70 municípios ELSI-Brasil em 5 regiões e 22 UFs (~10.000 participantes 50+) (+14 more)

### Community 4 - "Pipeline de Dados e Histórico do Projeto"
Cohesion: 0.13
Nodes (19): Diagnóstico Completo do Projeto (histórico, 06/05/2026), Ausência do filtro ELSI-Brasil (bloqueante histórico), Fase 1 — IVS Básico (legado), Fase 2 — IVS Multidimensional (legado), Base_ELSI_Bruta_Censo2022.csv (109.032 setores × 47 colunas), README entrega_orientadora — fonte da verdade da metodologia, Base_BeloHorizonte_Censo2022 (CSV + SQLite), Base_ELSI_70Municipios_Censo2022 (CSV + SQLite) (+11 more)

### Community 5 - "Testes da Pipeline (Fase 3)"
Cohesion: 0.19
Nodes (8): DataFrame, Path, Testes sanity-check da pipeline Fase 3.  Executar:     python -m pytest tests/ -, _read(), test_descritivas_globais_tem_7_indicadores(), test_descritivas_por_municipio_tem_490_linhas(), test_descritivas_por_regiao_tem_35_linhas(), test_elegibilidade_setores_soma_109032()

### Community 6 - "Figura: Histogramas das Variáveis"
Cohesion: 0.29
Nodes (12): Assimetria à direita das variáveis de saneamento e renda, Recorte dos 70 municípios ELSI, Histogramas — 7 variáveis-componente do IVS (setores OK, 70 municípios ELSI), IVS — Índice de Vulnerabilidade à Saúde, pct_agua_inad (percentual de abastecimento de água inadequado), pct_analfab (percentual de analfabetismo), pct_esgoto_inad (percentual de esgotamento sanitário inadequado), pct_lixo_inad (percentual de destino do lixo inadequado) (+4 more)

### Community 7 - "Figura: Boxplots Regionais"
Cohesion: 0.33
Nodes (11): Figura: Boxplots por região — variáveis-componente do IVS, Insight: Norte concentra as maiores medianas de inadequação de água e esgoto; distribuições muito assimétricas com longas caudas de outliers; pct_raca_pretpardind é maior no Norte/Nordeste e menor no Sul, IVS — Índice de Vulnerabilidade à Saúde, Macrorregiões do Brasil (Norte, Nordeste, Sudeste, Sul, Centro-Oeste), pct_agua_inad (% domicílios com abastecimento de água inadequado), pct_analfab (% de analfabetismo), pct_esgoto_inad (% domicílios com esgotamento sanitário inadequado), pct_lixo_inad (% domicílios com destino do lixo inadequado) (+3 more)

### Community 8 - "Figura: Matriz de Correlação"
Cohesion: 0.29
Nodes (11): Matriz de Correlação Pearson/Spearman dos Indicadores de Vulnerabilidade, Correlação de Pearson, Correlação de Spearman, Gradiente socioeconômico-racial da vulnerabilidade (renda_media inversamente associada a pct_raca_pretpardind r_s=-0.81 e pct_analfab r_s=-0.75), Indicador pct_agua_inad (abastecimento de água inadequado), Indicador pct_analfab (taxa de analfabetismo), Indicador pct_esgoto_inad (esgotamento sanitário inadequado), Indicador pct_lixo_inad (coleta de lixo inadequada) (+3 more)

### Community 9 - "Redação e Saídas da EDA"
Cohesion: 0.33
Nodes (6): Sequência de redação Pereira & Galvão + checklist STROBE, CSVs órfãos da EDA (código ad-hoc não versionado), Saídas da EDA (banco_de_dados/eda/ — tabelas e figuras), Plano_Artigo_Cientifico_IC_Preenchido.docx, Relatório EDA Fase 3 IVS/ELSI (12/06/2026), Framework FIOCRUZ de EDA (guia_analises.docx)

### Community 10 - "Dicionário de Dados do Censo 2022"
Cohesion: 0.40
Nodes (6): Dicionário Básico (V0001–V0009: total de pessoas, domicílios, média de moradores), Dicionário não-PCT (V00001+: características do domicílio, tipo de espécie, moradores), Dicionário de dados agregados por setores censitários (Censo 2022 IBGE), Siglas de domicílio (DPPO, DPIO, DPPV, DPPUO, DCCM, DCSM, DPO), V00001 — Domicílios Particulares Permanentes Ocupados (denominador padrão do IVS Censo 2022), Decisão: denominador V00001 (DPPO); V01042 descartado por ser contagem de responsáveis, não domicílios

### Community 11 - "Figura: Heatmap de Dados Faltantes"
Cohesion: 0.83
Nodes (4): Análise de dados faltantes (missingness) nos indicadores por município, Heatmap: Dados faltantes (%) por município × variável, Conjunto de indicadores avaliados (pct_agua_inad, pct_esgoto_inad, pct_lixo_inad, razao_moradores, pct_analfab, renda_media, pct_raca_pretpardind), Variável pct_analfab (taxa de analfabetismo) — concentra quase todo o missing (~5% a ~28%, pior em São Caetano do Sul e Porto Alegre)

## Knowledge Gaps
- **42 isolated node(s):** `Censo Demográfico 2022 — Agregados por Setores Censitários (IBGE)`, `Fiocruz Minas — Instituto René Rachou (IRR)`, `municipios_elsi_brasil.csv — lista oficial dos 70 municípios ELSI`, `estrutura_projeto — arquitetura técnica do repositório`, `Os 8 CSVs-fonte do Censo 2022 (dados/, ~2.4 GB)` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Relatório de Integridade do Projeto (19/05/2026, rev. 12/06/2026)` connect `Pipeline de Dados e Histórico do Projeto` to `Metodologia IVS-BH e Referências`, `Variáveis-Componente e Decisões Metodológicas`, `Testes da Pipeline (Fase 3)`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `Notebook 02 — Análises Descritivas (EDA)` connect `Variáveis-Componente e Decisões Metodológicas` to `Redação e Saídas da EDA`, `Pipeline de Dados e Histórico do Projeto`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `Plano de trabalho do bolsista (IC Fiocruz Minas)` connect `Metodologia IVS-BH e Referências` to `Pipeline de Dados e Histórico do Projeto`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **What connects `Testes sanity-check da pipeline Fase 3.  Executar:     python -m pytest tests/ -`, `Censo Demográfico 2022 — Agregados por Setores Censitários (IBGE)`, `Fiocruz Minas — Instituto René Rachou (IRR)` to the rest of the system?**
  _52 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Metodologia IVS-BH e Referências` be split into smaller, more focused modules?**
  _Cohesion score 0.10052910052910052 - nodes in this community are weakly interconnected._
- **Should `Variáveis-Componente e Decisões Metodológicas` be split into smaller, more focused modules?**
  _Cohesion score 0.10541310541310542 - nodes in this community are weakly interconnected._
- **Should `Métodos Estatísticos e Análise Fatorial` be split into smaller, more focused modules?**
  _Cohesion score 0.10276679841897234 - nodes in this community are weakly interconnected._