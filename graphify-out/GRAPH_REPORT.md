# Graph Report - Projeto_IVS_Censo22  (2026-09-30)

## Corpus Check
- 96 files · ~368,235 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1521 nodes · 2114 edges · 121 communities (94 shown, 23 thin omitted)
- Extraction: 96% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 73 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9924cb5d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- fatorial.py
- Notebook 02 — Análises Descritivas (EDA)
- MANUAL_DO_PROJETO.md
- test_ivs_censo.py
- _read
- __init__.py
- Figura: Boxplots por regiao - variaveis-componente do IVS (setores urbanos elegiveis)
- Figura: Histogramas das 7 variaveis-componente do IVS (setores urbanos elegiveis, 70 municipios ELSI)
- Figura: Matriz de Correlacao Pearson vs Spearman dos Indicadores do IVS
- proporcoes_brasil.py
- main
- gerar_entrega_orientadora.py
- gerar_deck_fatorial.js
- Prompt de execução — demandas da orientadora (setembro/2026) e correções da revisão geral
- Análise fatorial e o IVS do Censo 2022
- criarDeck
- 3. Companheiro de leitura, seção por seção
- Notebook 04 e relatório (NB4)
- Higiene do repositório e legado (HIG)
- Relatório de Integridade do Projeto IVS — Censo 2022 / ELSI-Brasil
- eda_atualizada.py
- gerar_deck_eda_central.js
- 2. Resultados, bloco a bloco
- gerar_tabelas_auditoria.py
- eda_central_dados.py
- gerar_deck_criterio_renda.js
- Commits posteriores à auditoria (AUD)
- atualizar_roteiro_2a_rodada.py
- Plano de implementação do Notebook 04
- O código da análise fatorial, linha a linha
- Relatório de Análise Exploratória de Dados (EDA)
- Camada fatorial (matemática) (FAT)
- gerar_resumo_eda_central.py
- `eda/atualizada/` — a 2ª rodada da EDA, com a renda sem o valor extremo
- gerar_pdf_outliers_renda.py
- gerar_slides_ivs_final.js
- gerar_pdf_guia_fatorial.py
- 12. Memória das decisões: como cada demanda foi atendida
- Apresentações — Projeto IVS Censo 2022
- rastrear_outliers_renda
- Auditoria integral do Projeto IVS — Censo 2022 / ELSI-Brasil
- Análise fatorial no Projeto IVS — por onde começar
- Parte 2 — Inventário do que mudou
- Notebooks 01 e 02 (NBS)
- Apêndice — todos os achados, com evidência
- Figura: Dados faltantes (%) por município × variável (heatmap)
- indicadores.py
- Revisão geral do Projeto IVS — Censo 2022 / ELSI-Brasil
- Projeto IVS Censo 2022
- 4. Análise por Variável
- gerar_pdf_plano_emergencia.py
- `scripts/` — os executáveis versionados
- Cálculo nacional — `banco_de_dados/nacional/`
- Notebook 01 — Extração e Filtragem ELSI
- Diagnóstico Completo do Projeto (histórico, 06/05/2026)
- Base_ELSI_70Municipios_Censo2022 (CSV + SQLite)
- 10. Blocos Descritivos Complementares
- ivs_especificacoes.py
- 3. Tratamento e Elegibilidade
- Deck e PDFs de apoio (DEC)
- Fontes dos PDFs de metodologia
- 14. Limitações da Análise Exploratória
- graphify.md
- FonteCenso
- 9. Estrutura de Correlações
- referencias/README.md
- Estudo ecológico com dados agregados
- Estado — NB05 (IVS final), 2026-09
- test_fatorial.py
- fatorial_ampliada.py
- Inconsistência histórica das variáveis de esgoto (V00312-V00316 vs V00249-V00253)
- juntar_decks.py
- gerar_slides_fatorial_ampliada.js
- Estado — demandas da orientadora (set/2026)
- gerar_slides_extremo_bh.js
- Prompt de execução — testes de especificação e o NB05 (IVS final)
- test_ivs_especificacoes.py
- gerar_dicionario_variaveis.py
- test_pipeline_fase3.py
- GUIA_DO_PROJETO — documento mestre de retomada
- test_juntar_decks.py
- prompts/README.md
- Prompt — uso inteligente de tokens e de modelos no Claude Code
- Prompt — atualizar o grafo de contexto do projeto (graphify), com custo controlado
- gerar_quadro_indicadores.py
- inventario_apresentacao.py
- chi2_sf
- gerar_notebook_ivs_final.py
- alinhar_cargas
- Fatorial ampliada, sem bootstrap — procedência
- Mapa da apresentação final
- Prompt para implementar o Notebook 04 — análise fatorial e pesos do IVS
- Relatório — Notebook 05: Cálculo do IVS final
- Motor de especificações do IVS (NB05, Fase C) — procedência
- Analise_Fatorial_LEIAME.md
- gerar_relatorio_ivs_final.py
- Nota — arquivo resgatado da worktree órfã `flamboyant-davinci-bb1785`
- Nota — arquivo resgatado da worktree órfã `gracious-jennings-f0c0db`
- dependencies
- NOTA_gerar_dicionario_variaveis.md
- test_base_bruta_tem_colunas_territoriais_e_pirâmide_etaria
- test_elegibilidade_separa_zerado_de_sigiloso
- test_recorte_urbano_mantem_os_70_municipios
- test_indice_de_envelhecimento_usa_denominador_0a14
- test_contagem_de_setores_de_favela
- test_calculo_nacional_bate_com_o_censo
- test_tipo_domicilio_soma_coerente
- test_tabelas_de_auditoria_usam_o_recorte_com_rurais
- test_cobertura_de_saneamento_e_internamente_coerente
- test_particao_da_agua_canalizada_fecha
- test_agua_canalizada_exportada_e_coerente
- test_razao_agregada_mede_numerador_e_denominador_nos_mesmos_setores
- test_entrega_separa_urbanos_da_base_do_recorte_de_analise
- test_coluna_de_renda_sem_o_extremo_de_belo_horizonte
- test_renda_sem_extremos_nao_zera_nem_derruba_linhas
- test_renda_imputada_mediana_municipal_usa_mediana_sem_o_excluido
- test_quadro_de_indicadores_cobre_todos_os_indicadores

## God Nodes (most connected - your core abstractions)
1. `Notebook 04 e relatório (NB4)` - 25 edges
2. `Higiene do repositório e legado (HIG)` - 24 edges
3. `main()` - 23 edges
4. `calcular_indicadores()` - 21 edges
5. `_read()` - 20 edges
6. `Relatório de Análise Exploratória de Dados (EDA)` - 20 edges
7. `criarDeck()` - 19 edges
8. `rodar_cenario()` - 19 edges
9. `Figura: Boxplots por regiao - variaveis-componente do IVS (setores urbanos elegiveis)` - 17 edges
10. `Commits posteriores à auditoria (AUD)` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Notebook 02 — Análises Descritivas (EDA)` --shares_data_with--> `Base analítica: 104.108 setores censitários urbanos elegíveis (70 municípios ELSI-Brasil, Censo 2022)`  [EXTRACTED]
  notebooks/Fase3_EDA_ELSI/README.md → banco_de_dados/eda/figuras/missing_por_municipio.png
- `Notebook 02 — Análises Descritivas (EDA)` --implements--> `Figura: Dados faltantes (%) por município × variável (heatmap)`  [EXTRACTED]
  notebooks/Fase3_EDA_ELSI/README.md → banco_de_dados/eda/figuras/missing_por_municipio.png
- `main()` --calls--> `encontrar_raiz()`  [INFERRED]
  scripts/auditoria_banheiro_particao.py → src/ivs_censo/fontes.py
- `carregar()` --calls--> `calcular_indicadores()`  [INFERRED]
  scripts/auditoria_renda.py → src/ivs_censo/indicadores.py
- `carregar()` --calls--> `classificar_dados_sig()`  [INFERRED]
  scripts/auditoria_renda.py → src/ivs_censo/indicadores.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fluxo de dados da pipeline Fase 3** — estrutura_projeto_8_csvs_censo2022, dados_municipios_elsi_brasil, notebooks_fase3_eda_elsi_01_extracao_filtragem_elsi, banco_de_dados_base_elsi_bruta_censo2022, notebooks_fase3_eda_elsi_02_analises_descritivas, banco_de_dados_eda_readme_saidas_eda [EXTRACTED 1.00]
- **As 7 variáveis-componente do IVS** — banco_de_dados_entrega_orientadora_readme_pct_agua_inad, banco_de_dados_entrega_orientadora_readme_pct_esgoto_inad, banco_de_dados_entrega_orientadora_readme_pct_lixo_inad, banco_de_dados_entrega_orientadora_readme_razao_moradores, banco_de_dados_entrega_orientadora_readme_pct_analfab, banco_de_dados_entrega_orientadora_readme_renda_media, banco_de_dados_entrega_orientadora_readme_pct_raca_pretpardind, readme_ivs_intraurbano [EXTRACTED 1.00]

## Communities (121 total, 23 thin omitted)

### Community 0 - "fatorial.py"
Cohesion: 0.10
Nodes (36): main(), Diagnóstico de adequabilidade dos dados à análise fatorial. Roda os testes do…, bartlett(), comunalidades_obliquas(), diagnosticar(), horn(), kmo(), matriz_correlacao() (+28 more)

### Community 1 - "Notebook 02 — Análises Descritivas (EDA)"
Cohesion: 0.29
Nodes (12): pct_agua_inad — % domicílios com água inadequada, pct_analfab — taxa de analfabetismo 15+, pct_esgoto_inad — % domicílios com esgoto inadequado, pct_lixo_inad — % domicílios com lixo inadequado, pct_raca_pretpardind — % pretos, pardos e indígenas, razao_moradores — razão de moradores por domicílio, renda_media — rendimento médio mensal dos responsáveis (V06004), Denominador domiciliar V00001 (DPP Ocupados) (+4 more)

### Community 2 - "MANUAL_DO_PROJETO.md"
Cohesion: 0.06
Nodes (34): A.1 Por onde começar, dependendo do que você precisa, A.2 Pasta por pasta, `Backup/` — legado, `banco_de_dados/` — saídas, Bloco 1 · Abertura (slides 1 a 5) — 4 minutos, Bloco 2 · Dados e método (slides 6 a 11) — 5 minutos, Bloco 3 · A análise exploratória (slides 12 a 20) — 8 minutos, Bloco 4 · Os achados (slides 21 a 25) — 6 minutos (+26 more)

### Community 3 - "test_ivs_censo.py"
Cohesion: 0.11
Nodes (30): calcular_indicadores(), Calcula os indicadores pedidos e devolve um DataFrame com uma coluna por…, _linha_sintetica(), Testes do módulo compartilhado `src/ivs_censo`. Diferente de…, Nenhum indicador pode depender de variável sem procedência declarada., O caso inverso do teste acima: V00900 sigiloso e V00901 presente. Descoberto…, `complemento=True` devolve 1 - num/den. É o que permite medir 'a água não chega…, A trinca é partição de V00001, então o complemento de V00199 tem que dar… (+22 more)

### Community 4 - "_read"
Cohesion: 0.17
Nodes (12): DataFrame, Path, n_validos = n_setores - n_sigilo em todo município, e a tabela por porte de…, O arquivo existe por causa dos suspeitos — eles têm que estar no topo. Ordenar…, _read(), test_auditoria_de_analfabetismo_fecha_as_contagens(), test_auditoria_de_renda_poe_os_suspeitos_primeiro_e_expoe_a_magnitude(), test_comparativo_brasil_vs_elsi_cobre_os_indicadores() (+4 more)

### Community 5 - "__init__.py"
Cohesion: 0.12
Nodes (20): main(), B.2 do prompt NB05 — testa se V00495 é exatamente a soma de…, main(), Gera a tabela de variáveis do projeto com descrição oficial do IBGE e arquivo-…, carregar_dicionario_oficial(), DataFrame, Path, Tabela de variáveis do projeto: descrição oficial do IBGE + arquivo-fonte.… (+12 more)

### Community 6 - "Figura: Boxplots por regiao - variaveis-componente do IVS (setores urbanos elegiveis)"
Cohesion: 0.22
Nodes (20): Figura: Boxplots por regiao - variaveis-componente do IVS (setores urbanos elegiveis), Achado: analfabetismo mais alto e mais disperso no Nordeste (mediana ~0,05, outliers ate ~0,72) frente a Sul e Centro-Oeste, Achado: densidade domiciliar maior no Norte (mediana ~3,2 moradores) e menor no Sul (~2,6), com dispersao estreita e caudas longas, Achado: distribuicoes zero-infladas das variaveis de saneamento (mediana ~0 no Sudeste, Sul e Centro-Oeste, caixa colapsada e nuvem densa de outliers ate 1.0), Achado: gradiente racial regional na proporcao preta/parda/indigena - Norte (~0,77) > Nordeste (~0,74) > Centro-Oeste (~0,60) > Sudeste (~0,51) > Sul (~0,22), com maior dispersao intrarregional no Sudeste e Centro-Oeste, Achado: gradiente regional de inadequacao de saneamento - Norte e Nordeste concentram agua e esgoto inadequados, Implicacao metodologica: escalas heterogeneas (proporcoes 0-1, razao 1-7, renda em milhares) e assimetria exigem padronizacao/transformacao antes de compor o IVS, Achado sintese: heterogeneidade inter-regional sistematica das dimensoes do IVS (saneamento, educacao, renda, raca/cor) entre os setores urbanos elegiveis (+12 more)

### Community 7 - "Figura: Histogramas das 7 variaveis-componente do IVS (setores urbanos elegiveis, 70 municipios ELSI)"
Cohesion: 0.23
Nodes (18): Achado: assimetria a direita em pct_analfab (moda proxima de zero, cauda ate ~0,7), Achado: forte assimetria a direita e cauda longa em renda_media (ate ~R$175.000), Achado: pct_raca_pretpardind com assimetria a esquerda, espalhada por todo o intervalo 0-1, moda ~0,65, Achado: razao_moradores aproximadamente simetrica/unimodal, moda ~2,7 moradores, Achado: inflacao de zeros nas tres variaveis de saneamento (agua, esgoto, lixo), Achado: pico secundario em 1,0 nas variaveis de saneamento (setores com 100% de inadequacao), Base de setores censitarios urbanos elegiveis (104.108 setores, 70 municipios ELSI, Censo 2022), Figura: Histogramas das 7 variaveis-componente do IVS (setores urbanos elegiveis, 70 municipios ELSI) (+10 more)

### Community 8 - "Figura: Matriz de Correlacao Pearson vs Spearman dos Indicadores do IVS"
Cohesion: 0.30
Nodes (16): Achado: eixo renda-raca-escolaridade e o bloco mais associado da matriz, Amostra: 104.108 setores censitarios urbanos elegiveis (70 municipios ELSI-Brasil, Censo 2022), Achado: Spearman supera sistematicamente Pearson, indicando relacoes monotonicas nao lineares e assimetria, Implicacao: fator latente socioeconomico unico (renda, raca, analfabetismo, adensamento) na analise fatorial, Implicacao: bloco de saneamento (agua, esgoto, lixo) forma fator secundario fraco e pouco coeso, Figura: Matriz de Correlacao Pearson vs Spearman dos Indicadores do IVS, Achado: pct_lixo_inad e quase independente dos demais indicadores (|r| <= 0.20), Notebook Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb (celula step12) (+8 more)

### Community 9 - "proporcoes_brasil.py"
Cohesion: 0.25
Nodes (14): ler_arquivo_nacional(), main(), montar_base_nacional(), _para_numero(), DataFrame, Path, Calcula os indicadores de proporção por setor censitário para o BRASIL INTEIRO…, Lê os 8 arquivos e devolve a base nacional unificada, indexada por CD_SETOR. (+6 more)

### Community 10 - "main"
Cohesion: 0.06
Nodes (47): carregar(), _descritivas(), figura_boxplot_cidades(), figura_tamanho_vs_renda(), main(), DataFrame, Path, Rastreia os valores extremos de renda e roda a EDA duas vezes: com e sem eles.… (+39 more)

### Community 11 - "gerar_entrega_orientadora.py"
Cohesion: 0.33
Nodes (10): gravar(), main(), montar_dicionario(), preparar_base(), DataFrame, Path, Regenera o pacote de entrega (CSV + SQLite) a partir da base atual da pipeline.…, Dicionário das colunas da entrega: IBGE + derivadas da pipeline + indicadores. (+2 more)

### Community 12 - "gerar_deck_fatorial.js"
Cohesion: 0.05
Nodes (34): ADEQ, aucEsc, aucIdx, AUTOV, BOOT, CARGAS6, CENARIOS, CORR7 (+26 more)

### Community 13 - "Prompt de execução — demandas da orientadora (setembro/2026) e correções da revisão geral"
Cohesion: 0.07
Nodes (29): 0.1 Orçamento de tokens — obrigatório, 0.2 Regras do projeto — não negociáveis, 0. Regras, 1. Fatos já verificados — não redescobrir, 2.1 O motor, 2.2 Os cenários, 2.3 O que cada cenário registra, 2.4 Comparações das demandas 5 e 6 (+21 more)

### Community 14 - "Análise fatorial e o IVS do Censo 2022"
Cohesion: 0.06
Nodes (33): 1.1 O problema que ele ataca, 1.2 Duas distinções que o artigo faz e que importam aqui, 1.3 Os três estágios do planejamento, 1.4 As estatísticas de leitura dos resultados, 1.5 O exemplo e a conclusão, 1. O artigo em síntese, 2.1 Ele é o manual da etapa que falta, 2.2 A correspondência é estrutural, não analógica (+25 more)

### Community 18 - "criarDeck"
Cohesion: 0.17
Nodes (7): criarDeck(), bloco(), capa(), numero(), regua(), secao(), titulo()

### Community 19 - "3. Companheiro de leitura, seção por seção"
Cohesion: 0.07
Nodes (27): 1. Como ler o livro, 2. O que o livro acrescenta ao que já foi feito, 3. Companheiro de leitura, seção por seção, 4. As cinco revisões que a leitura obriga, 5.1 Modelo reflexivo × formativo — o limite mais sério, 5.2 O livro mede um construto; o projeto precisa compor um índice, 5.3 Dados faltantes não aparecem no livro, 5.4 Dependência espacial (+19 more)

### Community 20 - "Notebook 04 e relatório (NB4)"
Cohesion: 0.08
Nodes (25): NB4-01 — Bootstrap iid sustenta 'pesos estáveis', mas por município os pesos oscilam 10 pontos e o IC inclui 60/40, NB4-02 — A AUC contra FCU não valida os pesos: renda sozinha, pesos iguais e pesos aleatórios separam igual ou melhor, NB4-03 — 'A oblíqua afasta os pesos da literatura' depende de somar quadrados da matriz padrão; pela estrutura dá 59,6/40,4, NB4-04 — Leitura seletiva do livro nas p. 27 e 29: omite justamente as condições que o projeto satisfaz, NB4-05 — 'Com Pearson a base reprovaria em dois critérios da Etapa 1': pela Tabela 7 do livro, reprova em um, NB4-06 — 'Esgoto com renda a −0,454' vem da matriz par a par da EDA; na matriz fatorada o valor é +0,436, NB4-07 — 'Divergência de 0,836 no lixo' compara fatores diferentes da ACP e do eixo principal, NB4-08 — Figura do plano fatorial: eixo 'Fator 2 — saneamento' no painel de 7 componentes, onde o fator 2 é o lixo (+17 more)

### Community 21 - "Higiene do repositório e legado (HIG)"
Cohesion: 0.08
Nodes (24): HIG-01 — Linha 2 do .gitignore corrompida: a regra banco_de_dados/*.csv se perdeu, HIG-02 — .gitignore com 17 regras mortas, uma linha repetida e negações sem efeito, HIG-03 — .claude/settings.local.json versionado pré-aprova python -c e git commit para quem clonar, HIG-04 — package.json e package-lock.json ignorados: quem clona não regera nenhum deck, HIG-05 — Com o piso declarado numpy>=1.26, test_acp_varimax_reproduz_csv falha por troca de sinal, HIG-06 — graphify-out/: nomes NFC/NFD duplicados, grafo parcial e cache com caminhos do Windows, HIG-07 — 597 MB em 5 worktrees órfãs em .claude/worktrees, presas a um .git do Windows, HIG-08 — O gerador do Dicionario_Variaveis_IVS_Censo2022.xlsx só existe numa worktree órfã (+16 more)

### Community 22 - "Relatório de Integridade do Projeto IVS — Censo 2022 / ELSI-Brasil"
Cohesion: 0.09
Nodes (22): 0. Status das Correções Aplicadas (sessão de 19/05/2026), 1. Sumário do Diagnóstico, 2.1 Arquivos-fonte (`dados/`), 2.2 Notebooks da pipeline ativa, 2.3 Outputs gerados (`banco_de_dados/`), 2. Estrutura do Projeto — Inventário, 3.1 Cruzamento (código no notebook ↔ uso metodológico), 3.2 Renomeações no notebook 01 (+14 more)

### Community 23 - "eda_atualizada.py"
Cohesion: 0.19
Nodes (21): carregar(), comparar(), correlacoes(), descritivas_globais(), descritivas_por_regiao(), favelas_comparativo(), figuras(), main() (+13 more)

### Community 24 - "gerar_deck_eda_central.js"
Cohesion: 0.13
Nodes (17): bloco(), blocoTabela(), capa(), cartao(), D, FIG, FIG_NOVA, legendaTabela() (+9 more)

### Community 25 - "2. Resultados, bloco a bloco"
Cohesion: 0.10
Nodes (20): 1. Método e as decisões que o sustentam, 2. Resultados, bloco a bloco, 3. As decisões que vão para a orientação, 4. Limitações, 5. O IVS é construto reflexivo ou índice formativo?, 6. Reprodutibilidade, A saída que os dados sugerem, Análise fatorial e os pesos do IVS (+12 more)

### Community 26 - "gerar_tabelas_auditoria.py"
Cohesion: 0.17
Nodes (19): carregar_setores_ok(), _cobertura(), main(), DataFrame, Path, Series, Regenera as tabelas de auditoria e de apresentação de `banco_de_dados/eda/`.…, Quantos setores do grupo têm cobertura *integral* de cada serviço. "Integral" =… (+11 more)

### Community 27 - "eda_central_dados.py"
Cohesion: 0.17
Nodes (15): bloco(), _corr(), _cs(), desc_regiao(), ler(), _linha_delta(), n2(), pct() (+7 more)

### Community 28 - "gerar_deck_criterio_renda.js"
Cohesion: 0.15
Nodes (13): bloco(), blocoTabela(), D, FIG, fs, legendaTabela(), numero(), p (+5 more)

### Community 29 - "Commits posteriores à auditoria (AUD)"
Cohesion: 0.12
Nodes (16): AUD-01 — 0b94c96 corrompeu a linha 2 do .gitignore e apagou a regra banco_de_dados/*.csv, AUD-02 — O deck em circulação, com 98 slides, não se reproduz mais pelo gerador, e o uso documentado do gerador o sobrescreve, AUD-03 — O README de Apresentacoes_IVS se contradiz depois de 7345386 e fa6f3b4, AUD-04 — 8d33c3e reescreveu caminhos nos geradores, mas o deck e o PDF em circulação ainda citam caminhos que não existem, AUD-05 — O README de atualizada/ atribui a eda_atualizada.py as 8 tabelas renda_* e 2 figuras que auditoria_renda.py --sem-extremo gera; e as contagens caducaram, AUD-06 — Os três geradores novos digitam medições no texto, embora os commits digam que não, AUD-07 — Os slides do extremo de BH afirmam números errados: segundo maior 'na casa dos R$ 30 mil', '87 mil setores' e 'um quinto do município', AUD-08 — O guia de apoio diz que retirar o analfabetismo 'recupera os 16.563 setores'; o NB04 mede 16.548 (+8 more)

### Community 30 - "atualizar_roteiro_2a_rodada.py"
Cohesion: 0.18
Nodes (15): br(), escrever(), ler(), main(), numeros(), par_depois(), DataFrame, Atualiza o roteiro da EDA Central da 1ª para a 2ª rodada. Por que este script… (+7 more)

### Community 31 - "Plano de implementação do Notebook 04"
Cohesion: 0.13
Nodes (15): 0. O ponto de partida, 1. Inventário de ideias, 2. Arquitetura recomendada, 3. Resultados esperados, 4. A objeção de fundo — reflexivo × formativo, 5. Prioridade, Análise fatorial, estrutura latente e definição dos pesos do IVS, Família A — Extensões do método (+7 more)

### Community 32 - "O código da análise fatorial, linha a linha"
Cohesion: 0.13
Nodes (15): 1. Da base à matriz de correlação, 2. Adequabilidade: KMO e MSA, 3. O teste de Bartlett, 4. Componentes principais, 5. Fatoração do eixo principal, 6. Rotação Varimax, 7. Rotação promax, 8. Escores pelo método da regressão (+7 more)

### Community 33 - "Relatório de Análise Exploratória de Dados (EDA)"
Cohesion: 0.14
Nodes (14): 11. Comparação com o Brasil, 13. Implicações para a Construção do IVS, 15. Próximos Passos, 1. Introdução, 2. Universo Amostral, 5. Análise Regional, 6. Heterogeneidade Municipal, 7. Análise de Outliers (+6 more)

### Community 34 - "Camada fatorial (matemática) (FAT)"
Cohesion: 0.14
Nodes (14): Camada fatorial (matemática) (FAT), FAT-01 — A Varimax para antes de convergir: cargas da solução de 6 variáveis erradas na 4ª casa (e numa célula, na 3ª), FAT-02 — A reprodução em R documentada não daria o Φ = 0,522 do NB04: ela troca a extração (PAF) e a normalização do promax, e a tabela de diferenças omite as duas coisas, FAT-03 — O Horn do script R (fa.parallel com fa='fa') não é o critério do módulo e, com n = 87 mil, reteria 3 ou 4 fatores, não 1 ou 2, FAT-04 — escores_regressao aceita a matriz padrão numa solução oblíqua e devolve escores errados; o certo é R⁻¹·estrutura, FAT-05 — O cheque de admissibilidade da p. 22 é tautológico com cargas de ACP: a variância residual oblíqua não tem como ficar negativa, FAT-06 — No caso de Heywood, o eixo principal devolve cargas incoerentes com as comunalidades e ainda marca 'convergiu', FAT-07 — A suíte da camada fatorial deixa passar 12 de 21 regressões plausíveis; promax, Horn, bootstrap e Bartlett (gl e p) não estão travados (+6 more)

### Community 35 - "gerar_resumo_eda_central.py"
Cohesion: 0.24
Nodes (13): bloco(), comentario(), corpo(), figura(), _fonte(), fonte_bloco(), procedencia(), Gera o resumo em Word da EDA Central: as tabelas e as figuras da análise, com… (+5 more)

### Community 36 - "`eda/atualizada/` — a 2ª rodada da EDA, com a renda sem o valor extremo"
Cohesion: 0.15
Nodes (11): A armadilha desta pasta, e ela é real, `eda/atualizada/` — a 2ª rodada da EDA, com a renda sem o valor extremo, O que consome estes arquivos, O que há aqui, Os quatro arquivos `extremo_bh_*`, que têm outro dono, Como conferir que está tudo coerente, `eda/fatorial/` — saídas da análise fatorial, Geração 1 — o diagnóstico (24/08/2026) (+3 more)

### Community 37 - "gerar_pdf_outliers_renda.py"
Cohesion: 0.15
Nodes (7): br(), figura_motivos(), ler(), DataFrame, Path, Gera o PDF que destrincha o critério de outlier de renda. O deck da EDA Central…, Formata número no padrão brasileiro.

### Community 38 - "gerar_slides_ivs_final.js"
Cohesion: 0.05
Nodes (42): RFC-4180, ACR, acrProposta, ampIvs6Max, ampIvs6Min, ampIvs7vMax, ampIvs7vMin, basesElegiveis (+34 more)

### Community 39 - "gerar_pdf_guia_fatorial.py"
Cohesion: 0.20
Nodes (7): br(), caixa(), P(), Gera o guia de apoio dos slides marcados com "EXPLICAR SLIDE" no deck da…, Um slide explicado, sempre na mesma ordem., Número em português: vírgula decimal, ponto de milhar., verbete()

### Community 40 - "12. Memória das decisões: como cada demanda foi atendida"
Cohesion: 0.18
Nodes (11): 12.10 Resumo das verificações, 12.1 Os três princípios que segui, 12.2 Demanda 1 — Ajustar o índice de envelhecimento, 12.3 Demanda 2 — Tabela de variáveis com o significado e a fonte, 12.4 Demanda 3 — Excluir setores rurais, 12.5 Demanda 4 — Agrupar as moradias convencionais, 12.6 Demanda 5 — Criar um indicador de apartamento, 12.7 Demanda 6 — Quantos setores são de vilas e favelas (+3 more)

### Community 41 - "Apresentações — Projeto IVS Censo 2022"
Cohesion: 0.18
Nodes (10): A apresentação atual, Apresentações — Projeto IVS Censo 2022, `complementos/` — apoio, não são a apresentação, Cuidado ao consultar o histórico, De onde vieram os nomes antigos, Dicionários, Histórico, O deck complementar — EDA Central avulsa (+2 more)

### Community 42 - "rastrear_outliers_renda"
Cohesion: 0.17
Nodes (16): rastrear_outliers_renda(), Rotula cada setor quanto à renda e devolve as colunas de rastreamento. Espera…, _cidade_sintetica(), Um município com N setores, para conferir a regra na mão., Renda alta num setor sem nenhum sinal contrário é EXTREMO, não erro de dado., O caso de Belo Horizonte: extremo de renda num setor de favela é incoerente., CD_TIPO numérico com um nulo no meio vira float64 (F2). O padrão antigo…, O mesmo valor é normal na cidade rica e extremo na cidade pobre — o IVS é… (+8 more)

### Community 43 - "Auditoria integral do Projeto IVS — Censo 2022 / ELSI-Brasil"
Cohesion: 0.20
Nodes (10): Achados, Auditoria integral do Projeto IVS — Censo 2022 / ELSI-Brasil, DIVERGENTE — dois documentos do projeto dizem coisas diferentes, FRÁGIL — está certo hoje e quebra sozinho amanhã, LACUNA — falta uma verificação que deveria existir, O que foi verificado e passou, O que não consegui verificar, Opinião, não achado (+2 more)

### Community 44 - "Análise fatorial no Projeto IVS — por onde começar"
Cohesion: 0.22
Nodes (9): Análise fatorial no Projeto IVS — por onde começar, As decisões em aberto, O estado da questão, em cinco linhas, Os dados e o código, Os documentos, Se você tem 5 minutos, Se você vai apresentar para a orientadora, Se você vai implementar (+1 more)

### Community 45 - "Parte 2 — Inventário do que mudou"
Cohesion: 0.25
Nodes (8): Arquivos indexados que foram modificados, Arquivos novos, Arquivos que nunca foram indexados, Comunidades do grafo antigo, Custo da execução anterior, Parte 1 — O prompt, Parte 2 — Inventário do que mudou, Prompt para atualizar o grafo do graphify

### Community 46 - "Notebooks 01 e 02 (NBS)"
Cohesion: 0.22
Nodes (9): NBS-1 — Comentário da seção 7f cita o universo errado de setores (106 mil em vez de 104 mil), NBS-2 — Dois CSVs por-setor em banco_de_dados/eda/ não são produzidos por nenhuma célula do NB01 ou NB02 atuais, NBS-3 — Método de agregação por município/região (média de proporções por setor) não é declarado nas seções 5-7, 7b-7d, 7f, NBS-4 — Matriz de correlação usa exclusão par-a-par (pairwise), não declarado, com efeito mensurável de até 0,033 frente ao listwise, NBS-5 — Tabela de FCU por município só existe para a base completa; por região existem as duas versões (base completa e recorte de análise), NBS-6 — Correlação de Spearman '0,459' citada na seção 7h não identifica a qual das 3 variáveis de 'entrega' de água se refere, NBS-7 — Nenhuma célula das duas notebooks tem output persistido — todas as afirmações numéricas do markdown dependem de reexecução para verificação, NBS-8 — Tabela CD_SIT × SITUACAO (markdown NB01) não é exaustiva: 2 setores do Brasil ficam de fora, soma 468.097 em vez de 468.099 (+1 more)

### Community 47 - "Apêndice — todos os achados, com evidência"
Cohesion: 0.25
Nodes (8): Apêndice — todos os achados, com evidência, Cálculo dos indicadores (IND), DOC-1 — Citação à Enap (p. 58) usada para autorizar manter razao_moradores (h²=0,380) generaliza além do exemplo do próprio livro, Documentação (DOC), IND-1 — razao_agregada em proporcoes_brasil.py ignora `complemento` e sai invertida para pct_sem_agua_canalizada, IND-2 — Teste de regressão para razao_agregada não cobre (nem testaria) o caso com complemento, IND-3 — Dicionario_Variaveis_Projeto.csv documenta só 70 das 104 colunas da entrega — faltam todos os 26 indicadores calculados, 8 colunas derivadas, e não há coluna de unidade, IND-4 — V00051 (maloca indígena) fica fora de PRECARIA mas dentro de NAO_CONVENCIONAL sem comentário explicando a assimetria

### Community 48 - "Figura: Dados faltantes (%) por município × variável (heatmap)"
Cohesion: 0.27
Nodes (11): Figura: Dados faltantes (%) por município × variável (heatmap), Base analítica: 104.108 setores censitários urbanos elegíveis (70 municípios ELSI-Brasil, Censo 2022), Achado: gradiente urbano — capitais e municípios ricos com muito missing, municípios pequenos com quase zero, Método: heatmap município × variável de % faltante (7 variáveis IVS, 70 municípios ELSI), Implicação metodológica: imputar/tratar pct_analfab com cuidado; excluir enviesaria contra setores de baixo analfabetismo, Índice de Vulnerabilidade à Saúde (IVS) intraurbano, Conceito: o missing NÃO é aleatório (não é MCAR), Achado: Porto Alegre e São Caetano do Sul lideram o missing (~25-28%) (+3 more)

### Community 49 - "indicadores.py"
Cohesion: 0.14
Nodes (13): classificar_dados_sig(), Indicador, DataFrame, Series, Definição e cálculo dos indicadores do projeto, em um só lugar. As fórmulas…, Classifica a elegibilidade de cada setor (regra do `Cálculo IVS2012.docx`).…, Divide evitando divisão por zero: onde `den <= 0` ou é nulo, devolve `NaN`., Um indicador = numerador / denominador, com metadados para as tabelas. (+5 more)

### Community 50 - "Revisão geral do Projeto IVS — Censo 2022 / ELSI-Brasil"
Cohesion: 0.20
Nodes (10): Estado dos 22 achados da auditoria de 17/09, O que esta revisão não cobriu, O que foi verificado e passou, Prioridade 1 — corrigir antes de apresentar à orientadora, Prioridade 2 — dados e código, Prioridade 3 — documentação e rastreabilidade, Prioridade 4 — repositório e histórico, Próximos passos, se quiser (+2 more)

### Community 51 - "Projeto IVS Censo 2022"
Cohesion: 0.20
Nodes (10): Análise fatorial / ACP para definição dos pesos do IVS, Hipótese centro-periferia (H1), Buss & Pellegrini Filho 2007 — A saúde e seus determinantes sociais, Caiaffa et al. 2021 — Saúde urbana, cidades e a interseção de sistemas, Censo Demográfico 2022 — Agregados por Setores Censitários (IBGE), Fiocruz Minas — Instituto René Rachou (IRR), ISU — Índice de Saúde Urbana (Passarelli-Araujo, 2023), Índice de Vulnerabilidade à Saúde (IVS) intraurbano (+2 more)

### Community 52 - "4. Análise por Variável"
Cohesion: 0.29
Nodes (7): 4.1 Saneamento, 4.2 Razão de moradores por domicílio, 4.3 Analfabetismo de 15 anos ou mais, 4.4.1 Auditoria dos extremos de renda, 4.4 Rendimento médio do responsável, 4.5 Cor ou raça preta, parda e indígena, 4. Análise por Variável

### Community 54 - "`scripts/` — os executáveis versionados"
Cohesion: 0.29
Nodes (6): Apresentações, Como conferir que um script continua honesto, Dados e pipeline, Documentos, Duas coisas que é preciso saber antes de rodar, `scripts/` — os executáveis versionados

### Community 55 - "Cálculo nacional — `banco_de_dados/nacional/`"
Cohesion: 0.33
Nodes (5): Arquivos, Como reproduzir, Cálculo nacional — `banco_de_dados/nacional/`, Duas leituras de cada indicador, Regras aplicadas (idênticas às do Notebook 02)

### Community 56 - "Notebook 01 — Extração e Filtragem ELSI"
Cohesion: 0.22
Nodes (9): Ausência do filtro ELSI-Brasil (bloqueante histórico), Os 8 CSVs-fonte do Censo 2022 (dados/, ~2.4 GB), Leitura em chunks dos CSVs grandes, Notebook 01 — Extração e Filtragem ELSI, _find_project_root — detecção da raiz do projeto, ler_csv_padronizado — leitura com fallback de encoding, Filtro ELSI por chave composta (UF + nome normalizado), Fase 3 — pipeline ativa (EDA com filtro ELSI) (+1 more)

### Community 57 - "Diagnóstico Completo do Projeto (histórico, 06/05/2026)"
Cohesion: 0.33
Nodes (7): Diagnóstico Completo do Projeto (histórico, 06/05/2026), Fase 1 — IVS Básico (legado), Fase 2 — IVS Multidimensional (legado), Sequência de redação Pereira & Galvão + checklist STROBE, Normalização de renda global (problema), Plano_Artigo_Cientifico_IC_Preenchido.docx, V01042 descartado como denominador

### Community 58 - "Base_ELSI_70Municipios_Censo2022 (CSV + SQLite)"
Cohesion: 0.40
Nodes (6): Base_ELSI_Bruta_Censo2022.csv (109.032 setores × 47 colunas), README entrega_orientadora — fonte da verdade da metodologia, Base_BeloHorizonte_Censo2022 (CSV + SQLite), Base_ELSI_70Municipios_Censo2022 (CSV + SQLite), Cálculo IVS2012.docx — metodologia operacional do IVS-BH, Dados_sig — classificação de elegibilidade dos setores

### Community 59 - "10. Blocos Descritivos Complementares"
Cohesion: 0.33
Nodes (6): 10.1 Habitação precária e banheiro, 10.2 Pessoa responsável do sexo feminino, 10.3 Indicadores de envelhecimento, 10.4 Tipo de domicílio, 10.5 Setores de favela e comunidade urbana, 10. Blocos Descritivos Complementares

### Community 60 - "ivs_especificacoes.py"
Cohesion: 0.09
Nodes (45): auc_estratos(), auc_grupos(), auc_municipal(), banheiro_graduado(), bases(), carregar_base(), elegibilidade(), estabilidade() (+37 more)

### Community 61 - "3. Tratamento e Elegibilidade"
Cohesion: 0.40
Nodes (5): 3.1 Sigilo do IBGE, 3.2 Separador decimal, 3.3 Classificação `Dados_sig`, 3.4 Recorte urbano, 3. Tratamento e Elegibilidade

### Community 62 - "Deck e PDFs de apoio (DEC)"
Cohesion: 0.40
Nodes (5): DEC-1 — Slides 68 e 91 citam 3.357 setores para um arquivo que tem 3.358, DEC-2 — Guia de Apoio nunca define autovalor, base dos critérios de Kaiser e Horn, DEC-3 — Nem o Guia nem o Plano de Emergência definem matriz padrão × matriz de estrutura, DEC-4 — Guia define KMO mas nunca menciona MSA (adequação por variável), Deck e PDFs de apoio (DEC)

### Community 63 - "Fontes dos PDFs de metodologia"
Cohesion: 0.50
Nodes (3): Como regerar, Fontes dos PDFs de metodologia, Identidade visual

### Community 64 - "14. Limitações da Análise Exploratória"
Cohesion: 0.50
Nodes (4): 14.1 O sigilo do analfabetismo — limitação aceita, 14.2 Favelas e Comunidades Urbanas — a fonte oficial e o que ela limita, 14.3 O sigilo parcial nos numeradores de várias parcelas, 14. Limitações da Análise Exploratória

### Community 65 - "graphify.md"
Cohesion: 0.50
Nodes (3): 🚀 Como usar, 📦 Extras opcionais (instale só se precisar), 🔧 Opcionais que valem a pena depois

### Community 66 - "FonteCenso"
Cohesion: 0.50
Nodes (3): FonteCenso, Um dos arquivos `Agregados_por_setores_*.csv` do Censo 2022., Todas as colunas que o projeto lê deste arquivo, com a chave à frente.

### Community 67 - "9. Estrutura de Correlações"
Cohesion: 0.67
Nodes (3): 9.1 Leitura, 9.2 Implicações para a análise fatorial, 9. Estrutura de Correlações

### Community 70 - "Estado — NB05 (IVS final), 2026-09"
Cohesion: 0.05
Nodes (36): A.7 — pytest, B.1 — Extração de V00237 e regeneração da entrega, B.2 — A partição do banheiro, B.3 — Os indicadores e o teste do graduado, B.4 — Regeneração dos geradores e das contagens citadas, C.1 — Leitura (só o que o bloco manda), C.2 — O motor: `scripts/ivs_especificacoes.py`, C.3 — Item 6: o que o índice acrescenta à renda (`acrescimo_renda.csv`) (+28 more)

### Community 71 - "test_fatorial.py"
Cohesion: 0.08
Nodes (36): acp(), escores_regressao(), fatoracao_eixo_principal(), *Squared Multiple Correlation* por variável: 1 − 1/diag(R⁻¹). Quanto da…, Componentes principais a partir da matriz de correlação: autovalores e cargas., Fatoração do eixo principal: ACP iterada com as comunalidades na diagonal. A…, Coeficientes do método da regressão: B = R⁻¹A. Aplicados às variáveis…, smc() (+28 more)

### Community 72 - "fatorial_ampliada.py"
Cohesion: 0.09
Nodes (31): auc_postos(), carregar(), comparacao(), figuras(), gravar(), indice_01(), lixo_fator_proprio(), main() (+23 more)

### Community 74 - "juntar_decks.py"
Cohesion: 0.18
Nodes (19): consertar_estrutura(), ler(), main(), Merge, ordem_dos_slides(), parse_rels(), proximo_indice(), proximo_rid_livre() (+11 more)

### Community 75 - "gerar_slides_fatorial_ampliada.js"
Cohesion: 0.10
Nodes (13): CARGAS, CENARIOS, { criarDeck }, d, FAT, FCU, fs, lerCsv() (+5 more)

### Community 76 - "Estado — demandas da orientadora (set/2026)"
Cohesion: 0.10
Nodes (19): Decisões tomadas (por quem, quando), Demandas da orientadora, Estado — demandas da orientadora (set/2026), Fase 0 — concluída (25/09/2026, sessão 2), Fase 2 — concluída (25/09/2026, execução automática), Fase 3 — concluída (25/09/2026, execução automática, em duas sessões), Fase 4 — concluída (25/09/2026, três sessões, execução automática), Fase 5, lote A (código frágil) — sessão 2: executado (+11 more)

### Community 77 - "gerar_slides_extremo_bh.js"
Cohesion: 0.14
Nodes (11): ATU, bh(), { criarDeck }, d, DESC, elsi(), fs, path (+3 more)

### Community 78 - "Prompt de execução — testes de especificação e o NB05 (IVS final)"
Cohesion: 0.13
Nodes (15): 0.1 Orçamento, 0.2 Projeto, 0. Regras, 1. Fatos verificados — não redescobrir, 2.1 As dimensões de especificação que o NB05 testa, 2.2 Critérios da especificação de referência — fixados ANTES de rodar, 2.3 Perguntas que continuam dela, 2. Decisões e critérios (+7 more)

### Community 79 - "test_ivs_especificacoes.py"
Cohesion: 0.18
Nodes (9): _dados(), skipif, Testes do motor de especificações do IVS (scripts/ivs_especificacoes.py)., Seis variáveis de dois fatores latentes, em dois municípios., IVS-6 sem lixo, renda original, Varimax SS, normalização global = o índice do…, test_indice_entre_0_e_1(), test_indice_municipal_usa_min_max_de_cada_municipio(), test_pesos_somam_1() (+1 more)

### Community 80 - "gerar_dicionario_variaveis.py"
Cohesion: 0.49
Nodes (12): aba_componentes(), aba_de_para(), aba_decisoes(), aba_guia_por_arquivo(), aba_inicio(), aba_variaveis_brutas(), aba_variaveis_derivadas(), main() (+4 more)

### Community 81 - "test_pipeline_fase3.py"
Cohesion: 0.17
Nodes (8): parametrize, Testes sanity-check da pipeline Fase 3. Executar: python -m pytest tests/ -v…, `CD_TIPO = 1` tem que reproduzir a lista oficial de setores de FCU do IBGE. A…, A coluna nova (renda_media_mediana_mun) difere de renda_media em exatamente um…, test_arquivos_eda_existem(), test_artefatos_das_demandas_existem(), test_coluna_de_renda_com_mediana_municipal(), test_marcacao_de_favela_bate_com_a_lista_oficial_do_ibge()

### Community 82 - "GUIA_DO_PROJETO — documento mestre de retomada"
Cohesion: 0.29
Nodes (5): municipios_elsi_brasil.csv — lista oficial dos 70 municípios ELSI, `docs/relatorios/` — o que o projeto produziu, estrutura_projeto — arquitetura técnica do repositório, GUIA_DO_PROJETO — documento mestre de retomada, Mapas temáticos no QGIS 3.x

### Community 83 - "test_juntar_decks.py"
Cohesion: 0.32
Nodes (11): _gravar_pacote(), _ids_e_layouts_por_master(), _master_xml(), _pacote_defeituoso(), Testes de scripts/juntar_decks.py — sobretudo de consertar_estrutura. Monta, em…, Lê o pacote e devolve (lista de todos os ids usados, lista dos masters citados…, Dict (ordenado) caminho -> texto, com os três defeitos., _rels() (+3 more)

### Community 84 - "prompts/README.md"
Cohesion: 0.22
Nodes (4): Depois de rodar, O prompt, Prompt para auditar o projeto de ponta a ponta, `docs/prompts/` — prompts executáveis

### Community 85 - "Prompt — uso inteligente de tokens e de modelos no Claude Code"
Cohesion: 0.18
Nodes (11): 1. Sessão, 2. Chamadas de ferramenta — a alavanca principal, 3. Modelo — escolher pelo tipo de trabalho, 4. Subagentes e workflows, 5. O que pesa em toda chamada, 6. Resposta, 7. Quando o limite bater, 8. Antes de começar qualquer tarefa grande — 30 segundos (+3 more)

### Community 86 - "Prompt — atualizar o grafo de contexto do projeto (graphify), com custo controlado"
Cohesion: 0.18
Nodes (11): Como usar o grafo depois — é para isto que ele existe, Onde está o custo — leia antes de rodar, Passo 1 — o que é de graça, Passo 2 — dizer ao grafo o que não ler, Passo 3 — pré-voo: quanto vai custar, Passo 4 — extração semântica, em ondas, Passo 5 — montar o grafo, Passo 6 — conferir (+3 more)

### Community 87 - "gerar_quadro_indicadores.py"
Cohesion: 0.29
Nodes (10): _descrever_codigos(), main(), montar_quadro(), _para_markdown(), DataFrame, Path, Gera o quadro de indicadores pedido pela orientadora, a partir do código.…, V00112 — descrição do IBGE | V00113 — ...', na ordem do indicador. (+2 more)

### Community 88 - "inventario_apresentacao.py"
Cohesion: 0.50
Nodes (8): classificar(), contar_slides_notas_explicar(), extrair_texto_pptx(), linha(), listar(), main(), Path, Inventário dos artefatos de apresentação (Fase 4, item 4.1). Lista cada .pptx…

### Community 89 - "chi2_sf"
Cohesion: 0.22
Nodes (9): chi2_sf(), _gamainc_p_serie(), _gamainc_q_fracao(), Cauda superior da qui-quadrado: Q(k/2, x/2), gama incompleta superior…, P(a, x) = gama incompleta inferior regularizada, por série (x < a + 1)., Q(a, x) = gama incompleta superior regularizada, por fração contínua de Lentz…, parametrize, FAT-12: Wilson–Hilferty errava por ordens de grandeza nesta região da cauda.… (+1 more)

### Community 90 - "gerar_notebook_ivs_final.py"
Cohesion: 0.36
Nodes (5): NotebookNode, main(), montar_notebook(), preencher_numeros_de_celula(), Gera o Notebook 05 (IVS final, item 9 do pedido) por nbformat e executa com…

### Community 91 - "alinhar_cargas"
Cohesion: 0.25
Nodes (8): alinhar_cargas(), bootstrap_cargas(), Põe as colunas de `cargas` na ordem e no sinal de `referencia`. Sem isso o…, Intervalo de confiança das cargas e da repartição dos pesos, por reamostragem.…, `alinhar_cargas` tem de devolver a referência mesmo com colunas trocadas e…, Os percentis do IC do bootstrap são 2,5/97,5, não 5/95 — e batem com o cálculo…, test_alinhar_cargas_desfaz_sinal_e_ordem(), test_bootstrap_cargas_percentis_sao_2_5_97_5()

### Community 92 - "Fatorial ampliada, sem bootstrap — procedência"
Cohesion: 0.29
Nodes (6): Arquivos, Cenários, Fatorial ampliada, sem bootstrap — procedência, Método (igual ao NB04, para ser comparável), Observação sobre o % de zeros, Trava de sanidade

### Community 93 - "Mapa da apresentação final"
Cohesion: 0.29
Nodes (6): ATUAL, Critério de classificação, HISTÓRICO, Mapa da apresentação final, Roteiro proposto para a apresentação final, SUPERADO

### Community 94 - "Prompt para implementar o Notebook 04 — análise fatorial e pesos do IVS"
Cohesion: 0.29
Nodes (6): Parte 1 — O que já existe (leia antes de colar), Parte 2 — O prompt, Parte 3 — Skills, por fase, Parte 4 — Como conferir que deu certo, Prompt para implementar o Notebook 04 — análise fatorial e pesos do IVS, Skills a não usar aqui

### Community 95 - "Relatório — Notebook 05: Cálculo do IVS final"
Cohesion: 0.29
Nodes (6): A referência proposta e as alternativas (seção 2.2 do prompt), Achados, Limitações, Método, Perguntas à orientadora, Relatório — Notebook 05: Cálculo do IVS final

### Community 96 - "Motor de especificações do IVS (NB05, Fase C) — procedência"
Cohesion: 0.33
Nodes (5): A grade, Arquivos, Motor de especificações do IVS (NB05, Fase C) — procedência, Método, Trava (C.5)

### Community 98 - "gerar_relatorio_ivs_final.py"
Cohesion: 0.47
Nodes (5): main(), num(), pct(), Gera docs/relatorios/Relatorio_IVS_Final_NB05.md (item 9, D.2 do prompt de…, Formata como o resto do projeto: vírgula decimal.

### Community 99 - "Nota — arquivo resgatado da worktree órfã `flamboyant-davinci-bb1785`"
Cohesion: 0.50
Nodes (3): Nota — arquivo resgatado da worktree órfã `flamboyant-davinci-bb1785`, O que a comparação célula a célula mostrou (openpyxl, mesmo método do item 8.1), Por que foi copiado para cá

### Community 100 - "Nota — arquivo resgatado da worktree órfã `gracious-jennings-f0c0db`"
Cohesion: 0.50
Nodes (3): Contexto, Nota — arquivo resgatado da worktree órfã `gracious-jennings-f0c0db`, Por que foi copiado para cá

### Community 101 - "dependencies"
Cohesion: 0.50
Nodes (3): dependencies, pptxgenjs, pptxgenjs

## Ambiguous Edges - Review These
- `Achado: gradiente urbano — capitais e municípios ricos com muito missing, municípios pequenos com quase zero` → `Mecanismo: supressão do IBGE de contagens pequenas gera o missing`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/missing_por_municipio.png · relation: rationale_for
- `Achado: gradiente racial regional na proporcao preta/parda/indigena - Norte (~0,77) > Nordeste (~0,74) > Centro-Oeste (~0,60) > Sudeste (~0,51) > Sul (~0,22), com maior dispersao intrarregional no Sudeste e Centro-Oeste` → `Achado: gradiente regional de inadequacao de saneamento - Norte e Nordeste concentram agua e esgoto inadequados`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/boxplots_por_regiao.png · relation: semantically_similar_to
- `Variavel pct_analfab (proporcao de analfabetos)` → `Variavel pct_raca_pretpardind (proporcao de pessoas pretas, pardas e indigenas)`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/boxplots_por_regiao.png · relation: conceptually_related_to
- `Achado: pico secundario em 1,0 nas variaveis de saneamento (setores com 100% de inadequacao)` → `Base de setores censitarios urbanos elegiveis (104.108 setores, 70 municipios ELSI, Censo 2022)`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/histogramas.png · relation: conceptually_related_to
- `Implicacao: bloco de saneamento (agua, esgoto, lixo) forma fator secundario fraco e pouco coeso` → `Indicador pct_lixo_inad (destino do lixo inadequado)`  [AMBIGUOUS]
  banco_de_dados/eda/figuras/matriz_correlacao.png · relation: conceptually_related_to

## Knowledge Gaps
- **580 isolated node(s):** `pptxgenjs`, `path`, `fs`, `RAIZ`, `FIG` (+575 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 907 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Achado: gradiente urbano — capitais e municípios ricos com muito missing, municípios pequenos com quase zero` and `Mecanismo: supressão do IBGE de contagens pequenas gera o missing`?**
  _Edge tagged AMBIGUOUS (relation: rationale_for) - confidence is low._
- **What is the exact relationship between `Achado: gradiente racial regional na proporcao preta/parda/indigena - Norte (~0,77) > Nordeste (~0,74) > Centro-Oeste (~0,60) > Sudeste (~0,51) > Sul (~0,22), com maior dispersao intrarregional no Sudeste e Centro-Oeste` and `Achado: gradiente regional de inadequacao de saneamento - Norte e Nordeste concentram agua e esgoto inadequados`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Variavel pct_analfab (proporcao de analfabetos)` and `Variavel pct_raca_pretpardind (proporcao de pessoas pretas, pardas e indigenas)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Achado: pico secundario em 1,0 nas variaveis de saneamento (setores com 100% de inadequacao)` and `Base de setores censitarios urbanos elegiveis (104.108 setores, 70 municipios ELSI, Censo 2022)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Implicacao: bloco de saneamento (agua, esgoto, lixo) forma fator secundario fraco e pouco coeso` and `Indicador pct_lixo_inad (destino do lixo inadequado)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Notebook 02 — Análises Descritivas (EDA)` connect `Notebook 02 — Análises Descritivas (EDA)` to `Figura: Dados faltantes (%) por município × variável (heatmap)`, `Base_ELSI_70Municipios_Censo2022 (CSV + SQLite)`, `Notebook 01 — Extração e Filtragem ELSI`, ``eda/atualizada/` — a 2ª rodada da EDA, com a renda sem o valor extremo`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `municipios_elsi_brasil.csv — lista oficial dos 70 municípios ELSI` connect `GUIA_DO_PROJETO — documento mestre de retomada` to `Notebook 01 — Extração e Filtragem ELSI`, `Analise_Fatorial_LEIAME.md`, `MANUAL_DO_PROJETO.md`, ``eda/atualizada/` — a 2ª rodada da EDA, com a renda sem o valor extremo`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._