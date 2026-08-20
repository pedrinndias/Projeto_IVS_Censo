# Graph Report - .  (2026-08-10)

## Corpus Check
- 29 files · ~164,535 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 316 nodes · 496 edges · 20 communities (17 shown, 3 thin omitted)
- Extraction: 87% EXTRACTED · 12% INFERRED · 1% AMBIGUOUS · INFERRED: 59 edges (avg confidence: 0.83)
- Token cost: 273,737 input · 0 output

## Community Hubs (Navigation)
- Metodologia IVS-BH e Variáveis-Componente
- Histórico do Projeto e Pendências
- Referências e Plano do Artigo
- Módulo de Indicadores (src/ivs_censo)
- Testes da Pipeline
- Dicionário de Variáveis e Arquivos-Fonte
- Figura: Boxplots e Achados Regionais
- Figura: Histogramas e Forma das Distribuições
- Figura: Correlações e Fator Socioeconômico
- Cálculo Nacional (Brasil inteiro)
- Figura: Dados Faltantes e Sigilo
- Pacote de Entrega (CSV + SQLite)
- Notebook 01 — Extração e Filtro ELSI
- Dicionários Oficiais do IBGE
- Outliers e Regra IQR
- Tipo pandas DataFrame
- Tipo pathlib Path

## God Nodes (most connected - your core abstractions)
1. `Notebook 02 — Análises Descritivas (EDA)` - 17 edges
2. `Figura: Boxplots por regiao - variaveis-componente do IVS (setores urbanos elegiveis)` - 17 edges
3. `Plano de trabalho do bolsista (IC Fiocruz Minas)` - 15 edges
4. `calcular_indicadores()` - 15 edges
5. `Figura: Histogramas das 7 variaveis-componente do IVS (setores urbanos elegiveis, 70 municipios ELSI)` - 15 edges
6. `_read()` - 14 edges
7. `Figura: Matriz de Correlacao Pearson vs Spearman dos Indicadores do IVS` - 12 edges
8. `Notebook 01 — Extração e Filtragem ELSI` - 10 edges
9. `Relatório de EDA Fase 3 — IVS Censo 2022 / ELSI (versão convertida)` - 10 edges
10. `Projeto IVS Censo 2022` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Plano de trabalho do bolsista (IC Fiocruz Minas)` --semantically_similar_to--> `GUIA_DO_PROJETO — documento mestre de retomada`  [INFERRED] [semantically similar]
  docs/Plano de trabalho.pdf → GUIA_DO_PROJETO.md
- `Ponderação participativa par-a-par (IVS-BH)` --semantically_similar_to--> `Análise fatorial / ACP para definição dos pesos do IVS`  [INFERRED] [semantically similar]
  docs/indice_vulnerabilidade2012 (2).pdf → GUIA_DO_PROJETO.md
- `Notebook 02 — Análises Descritivas (EDA)` --shares_data_with--> `Base analítica: 104.108 setores censitários urbanos elegíveis (70 municípios ELSI-Brasil, Censo 2022)`  [EXTRACTED]
  notebooks/Fase3_EDA_ELSI/README.md → banco_de_dados/eda/figuras/missing_por_municipio.png
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

## Communities (20 total, 3 thin omitted)

### Community 0 - "Metodologia IVS-BH e Variáveis-Componente"
Cohesion: 0.05
Nodes (45): Componente Saneamento (água, esgoto, lixo inadequados) — IVS-BH, Componentes socioeconômicos (habitação, escolaridade, renda, social) — IVS-BH, Conversão de escala min-max: (valor bruto − mínimo) / (máximo − mínimo), Classificação Dados_sig (SIGILOSO / COLETIVO / ZERADO / OK) para elegibilidade do setor, Cálculo IVS 2012 (documento operacional SMS-BH), Tratamento de domicílios coletivos: usa número de responsáveis como total de domicílios; exclui setores 100% coletivos, Lixo em caçamba de serviço de limpeza (V037) contabilizado no destino inadequado — decisão intencional do IVS-BH, Dicionário de dados Renda do Responsável (Censo 2022 IBGE) (+37 more)

### Community 1 - "Histórico do Projeto e Pendências"
Cohesion: 0.07
Nodes (41): Diagnóstico Completo do Projeto (histórico, 06/05/2026), Fase 1 — IVS Básico (legado), Fase 2 — IVS Multidimensional (legado), Inconsistência histórica das variáveis de esgoto (V00312-V00316 vs V00249-V00253), Sequência de redação Pereira & Galvão + checklist STROBE, Normalização de renda global (problema), Base_ELSI_Bruta_Censo2022.csv (109.032 setores × 47 colunas), CSVs órfãos da EDA (código ad-hoc não versionado) (+33 more)

### Community 2 - "Referências e Plano do Artigo"
Cohesion: 0.09
Nodes (31): Ausência do filtro ELSI-Brasil (bloqueante histórico), Avaliação do IVS-BH por desfechos de saúde (gradiente dose-resposta), Categorização do IVS em 4 faixas de risco, IVS-BH 2012 (SMS Belo Horizonte, 2013), Padronização min-max 0-1, Ponderação participativa par-a-par (IVS-BH), Plano de trabalho do bolsista (IC Fiocruz Minas), Agero et al. 2020 — Desafios do envelhecimento populacional (+23 more)

### Community 3 - "Módulo de Indicadores (src/ivs_censo)"
Cohesion: 0.10
Nodes (29): Series, calcular_indicadores(), classificar_dados_sig(), Indicador, DataFrame, Definição e cálculo dos indicadores do projeto, em um só lugar.  As fórmulas aqu, Calcula os indicadores pedidos e devolve um DataFrame com uma coluna por indicad, Classifica a elegibilidade de cada setor (regra do `Cálculo IVS2012.docx`). (+21 more)

### Community 4 - "Testes da Pipeline"
Cohesion: 0.09
Nodes (23): DataFrame, Path, Testes sanity-check da pipeline Fase 3.  Executar:     python -m pytest tests/ -, A base do NB01 precisa trazer a classificação territorial (favelas/rural) e as, Setores sem população têm que aparecer como ZERADO, não como SIGILOSO., O filtro rural não pode zerar nenhum município da amostra ELSI., IEP = 60+ / menores de 15 (Galvão et al., 2025). Recalcula a partir das contagen, CD_TIPO = 1 identifica Favela e Comunidade Urbana; a contagem tem que bater (+15 more)

### Community 5 - "Dicionário de Variáveis e Arquivos-Fonte"
Cohesion: 0.10
Nodes (21): main(), Gera a tabela de variáveis do projeto com descrição oficial do IBGE e arquivo-fo, carregar_dicionario_oficial(), DataFrame, Path, Tabela de variáveis do projeto: descrição oficial do IBGE + arquivo-fonte.  Aten, Lê os dois dicionários oficiais do IBGE e devolve `[variavel, tema, descricao]`., Monta a tabela final: cada variável usada pelo projeto, o que ela significa, (+13 more)

### Community 6 - "Figura: Boxplots e Achados Regionais"
Cohesion: 0.22
Nodes (20): Figura: Boxplots por regiao - variaveis-componente do IVS (setores urbanos elegiveis), Achado: analfabetismo mais alto e mais disperso no Nordeste (mediana ~0,05, outliers ate ~0,72) frente a Sul e Centro-Oeste, Achado: densidade domiciliar maior no Norte (mediana ~3,2 moradores) e menor no Sul (~2,6), com dispersao estreita e caudas longas, Achado: distribuicoes zero-infladas das variaveis de saneamento (mediana ~0 no Sudeste, Sul e Centro-Oeste, caixa colapsada e nuvem densa de outliers ate 1.0), Achado: gradiente racial regional na proporcao preta/parda/indigena - Norte (~0,77) > Nordeste (~0,74) > Centro-Oeste (~0,60) > Sudeste (~0,51) > Sul (~0,22), com maior dispersao intrarregional no Sudeste e Centro-Oeste, Achado: gradiente regional de inadequacao de saneamento - Norte e Nordeste concentram agua e esgoto inadequados, Implicacao metodologica: escalas heterogeneas (proporcoes 0-1, razao 1-7, renda em milhares) e assimetria exigem padronizacao/transformacao antes de compor o IVS, Achado sintese: heterogeneidade inter-regional sistematica das dimensoes do IVS (saneamento, educacao, renda, raca/cor) entre os setores urbanos elegiveis (+12 more)

### Community 7 - "Figura: Histogramas e Forma das Distribuições"
Cohesion: 0.23
Nodes (18): Achado: assimetria a direita em pct_analfab (moda proxima de zero, cauda ate ~0,7), Achado: forte assimetria a direita e cauda longa em renda_media (ate ~R$175.000), Achado: pct_raca_pretpardind com assimetria a esquerda, espalhada por todo o intervalo 0-1, moda ~0,65, Achado: razao_moradores aproximadamente simetrica/unimodal, moda ~2,7 moradores, Achado: inflacao de zeros nas tres variaveis de saneamento (agua, esgoto, lixo), Achado: pico secundario em 1,0 nas variaveis de saneamento (setores com 100% de inadequacao), Base de setores censitarios urbanos elegiveis (104.108 setores, 70 municipios ELSI, Censo 2022), Figura: Histogramas das 7 variaveis-componente do IVS (setores urbanos elegiveis, 70 municipios ELSI) (+10 more)

### Community 8 - "Figura: Correlações e Fator Socioeconômico"
Cohesion: 0.30
Nodes (16): Achado: eixo renda-raca-escolaridade e o bloco mais associado da matriz, Amostra: 104.108 setores censitarios urbanos elegiveis (70 municipios ELSI-Brasil, Censo 2022), Achado: Spearman supera sistematicamente Pearson, indicando relacoes monotonicas nao lineares e assimetria, Implicacao: fator latente socioeconomico unico (renda, raca, analfabetismo, adensamento) na analise fatorial, Implicacao: bloco de saneamento (agua, esgoto, lixo) forma fator secundario fraco e pouco coeso, Figura: Matriz de Correlacao Pearson vs Spearman dos Indicadores do IVS, Achado: pct_lixo_inad e quase independente dos demais indicadores (|r| <= 0.20), Notebook Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb (celula step12) (+8 more)

### Community 9 - "Cálculo Nacional (Brasil inteiro)"
Cohesion: 0.26
Nodes (14): ler_arquivo_nacional(), main(), montar_base_nacional(), _para_numero(), DataFrame, Path, Calcula os indicadores de proporção por setor censitário para o BRASIL INTEIRO e, Lê os 8 arquivos e devolve a base nacional unificada, indexada por CD_SETOR. (+6 more)

### Community 10 - "Figura: Dados Faltantes e Sigilo"
Cohesion: 0.27
Nodes (11): Figura: Dados faltantes (%) por município × variável (heatmap), Base analítica: 104.108 setores censitários urbanos elegíveis (70 municípios ELSI-Brasil, Censo 2022), Achado: gradiente urbano — capitais e municípios ricos com muito missing, municípios pequenos com quase zero, Método: heatmap município × variável de % faltante (7 variáveis IVS, 70 municípios ELSI), Implicação metodológica: imputar/tratar pct_analfab com cuidado; excluir enviesaria contra setores de baixo analfabetismo, Índice de Vulnerabilidade à Saúde (IVS) intraurbano, Conceito: o missing NÃO é aleatório (não é MCAR), Achado: Porto Alegre e São Caetano do Sul lideram o missing (~25-28%) (+3 more)

### Community 11 - "Pacote de Entrega (CSV + SQLite)"
Cohesion: 0.33
Nodes (10): gravar(), main(), montar_dicionario(), preparar_base(), DataFrame, Path, Regenera o pacote de entrega (CSV + SQLite) a partir da base atual da pipeline., Grava o par CSV + SQLite de um recorte. (+2 more)

### Community 12 - "Notebook 01 — Extração e Filtro ELSI"
Cohesion: 0.25
Nodes (8): municipios_elsi_brasil.csv — lista oficial dos 70 municípios ELSI, Morfologia urbana (V00047-V00052 → Moradia_Predominante), Os 8 CSVs-fonte do Censo 2022 (dados/, ~2.4 GB), Leitura em chunks dos CSVs grandes, Notebook 01 — Extração e Filtragem ELSI, _find_project_root — detecção da raiz do projeto, ler_csv_padronizado — leitura com fallback de encoding, Filtro ELSI por chave composta (UF + nome normalizado)

### Community 13 - "Dicionários Oficiais do IBGE"
Cohesion: 0.40
Nodes (6): Dicionário Básico (V0001–V0009: total de pessoas, domicílios, média de moradores), Dicionário não-PCT (V00001+: características do domicílio, tipo de espécie, moradores), Dicionário de dados agregados por setores censitários (Censo 2022 IBGE), Siglas de domicílio (DPPO, DPIO, DPPV, DPPUO, DCCM, DCSM, DPO), V00001 — Domicílios Particulares Permanentes Ocupados (denominador padrão do IVS Censo 2022), Decisão: denominador V00001 (DPPO); V01042 descartado por ser contagem de responsáveis, não domicílios

## Ambiguous Edges - Review These
- `Variavel pct_analfab (proporcao de analfabetos)` → `Variavel pct_raca_pretpardind (proporcao de pessoas pretas, pardas e indigenas)`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/boxplots_por_regiao.png · relation: conceptually_related_to
- `Achado: gradiente regional de inadequacao de saneamento - Norte e Nordeste concentram agua e esgoto inadequados` → `Achado: gradiente racial regional na proporcao preta/parda/indigena - Norte (~0,77) > Nordeste (~0,74) > Centro-Oeste (~0,60) > Sudeste (~0,51) > Sul (~0,22), com maior dispersao intrarregional no Sudeste e Centro-Oeste`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/boxplots_por_regiao.png · relation: semantically_similar_to
- `Base de setores censitarios urbanos elegiveis (104.108 setores, 70 municipios ELSI, Censo 2022)` → `Achado: pico secundario em 1,0 nas variaveis de saneamento (setores com 100% de inadequacao)`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/histogramas.png · relation: conceptually_related_to
- `Indicador pct_lixo_inad (destino do lixo inadequado)` → `Implicacao: bloco de saneamento (agua, esgoto, lixo) forma fator secundario fraco e pouco coeso`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/matriz_correlacao.png · relation: conceptually_related_to
- `Achado: gradiente urbano — capitais e municípios ricos com muito missing, municípios pequenos com quase zero` → `Mecanismo: supressão do IBGE de contagens pequenas gera o missing`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/missing_por_municipio.png · relation: rationale_for

## Knowledge Gaps
- **43 isolated node(s):** `Censo Demográfico 2022 — Agregados por Setores Censitários (IBGE)`, `Fiocruz Minas — Instituto René Rachou (IRR)`, `municipios_elsi_brasil.csv — lista oficial dos 70 municípios ELSI`, `estrutura_projeto — arquitetura técnica do repositório`, `Os 8 CSVs-fonte do Censo 2022 (dados/, ~2.4 GB)` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Variavel pct_analfab (proporcao de analfabetos)` and `Variavel pct_raca_pretpardind (proporcao de pessoas pretas, pardas e indigenas)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Achado: gradiente regional de inadequacao de saneamento - Norte e Nordeste concentram agua e esgoto inadequados` and `Achado: gradiente racial regional na proporcao preta/parda/indigena - Norte (~0,77) > Nordeste (~0,74) > Centro-Oeste (~0,60) > Sudeste (~0,51) > Sul (~0,22), com maior dispersao intrarregional no Sudeste e Centro-Oeste`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Base de setores censitarios urbanos elegiveis (104.108 setores, 70 municipios ELSI, Censo 2022)` and `Achado: pico secundario em 1,0 nas variaveis de saneamento (setores com 100% de inadequacao)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Indicador pct_lixo_inad (destino do lixo inadequado)` and `Implicacao: bloco de saneamento (agua, esgoto, lixo) forma fator secundario fraco e pouco coeso`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Achado: gradiente urbano — capitais e municípios ricos com muito missing, municípios pequenos com quase zero` and `Mecanismo: supressão do IBGE de contagens pequenas gera o missing`?**
  _Edge tagged AMBIGUOUS (relation: rationale_for) - confidence is low._
- **Why does `Notebook 02 — Análises Descritivas (EDA)` connect `Histórico do Projeto e Pendências` to `Figura: Dados Faltantes e Sigilo`, `Referências e Plano do Artigo`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `Relatório de Integridade do Projeto (19/05/2026, rev. 12/06/2026)` connect `Histórico do Projeto e Pendências` to `Referências e Plano do Artigo`, `Notebook 01 — Extração e Filtro ELSI`, `Testes da Pipeline`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._