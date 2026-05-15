# 📋 Diagnóstico Completo — Projeto IVS Censo 2022

> **Data:** 06/05/2026  
> **Escopo:** Análise integral do Plano do Artigo Científico + Repositório de Código  
> **Metodologia:** Leitura de todos os 9 notebooks, 3 scripts Python, documentos de planejamento e todos os outputs gerados.

---

# PARTE 1 — ANÁLISE DO PLANO DO ARTIGO CIENTÍFICO

Documento analisado: `Plano_Artigo_Cientifico_IC_Preenchido.docx`

## 1.1 Visão Geral do Plano

O plano é um roteiro completo para construção de um **Índice de Vulnerabilidade à Saúde (IVS)** intraurbano, utilizando dados do **Censo Demográfico 2022** para os **70 municípios do ELSI-Brasil** (Estudo Longitudinal da Saúde dos Idosos Brasileiros). O plano segue a metodologia proposta por Pereira & Galvão (Epidemiologia e Serviços de Saúde, 2012-2014) e o checklist STROBE.

**Objetivo Principal (conforme o Plano):**  
Construir um IVS intraurbano, baseado em variáveis do Censo 2022, para os 70 municípios da amostra do ELSI-Brasil, e analisar a distribuição espacial da vulnerabilidade à saúde nesses territórios.

---

## 1.2 Pontos Fortes do Plano

### Estrutura Metodológica Sólida
- Segue a sequência não-convencional recomendada para redação científica: **Tabelas → Método → Resultados → Discussão → Introdução → Resumo**
- A estrutura PICOS (População, Intervenção, Comparação, Outcome, Study type) está bem definida
- Delineamento ecológico adequado e bem justificado

### Fundamentação Teórica Consistente
- **IVS-BH 2012** (SMS-BH, 2013) — referência metodológica principal
- **ISU de Passarelli-Araujo (2023)** — evidência empírica do padrão centro-periferia
- **Caiaffa et al. (2021)** e **Buss & Pellegrini Filho (2007)** — determinantes sociais de saúde
- A lacuna está bem identificada: não existe IVS com dados do Censo 2022 para os municípios ELSI-Brasil

### Variáveis Bem Definidas (7 variáveis em 2 dimensões)

| Dimensão | Variáveis |
|---|---|
| **Saneamento** (3 var.) | Água inadequada, esgoto inadequado, lixo inadequado |
| **Socioeconômica** (4 var.) | Densidade domiciliar, analfabetismo, renda (invertida), raça/cor |

### Autocrítica e Limitações Declaradas
- Falácia ecológica (inferência de áreas para indivíduos)
- Homogeneidade interna presumida dos setores
- Dados sigilosos do IBGE (setores < 5 domicílios)
- Ausência de variáveis de entorno no Censo 2022

### Cronograma Completo
O cronograma vai de **março/2026 a fevereiro/2027**, cobrindo desde a revisão bibliográfica até a submissão do artigo.

---

## 1.3 Pontos de Atenção no Plano

### Campos Pendentes de Preenchimento

| Campo | Fase | Status |
|---|---|---|
| Objetivo refinado (versão final) | Fase 0 | 🔴 Pendente |
| Periódico-alvo e suas normas | Fase 0.2 / Tabela 2 | 🔴 Pendente |
| Pesquisador(a) Principal | Tabela 1 | 🔴 Pendente |
| Resultados do Resumo | Fase 6 | 🟡 Depende da análise |
| Conclusão do Resumo | Fase 6 | 🟡 Depende da análise |
| Achado principal | Fase 3 | 🟡 Depende da análise |
| Estudos discordantes | Fase 4 | 🟡 Depende da revisão |
| Objetivo versão final (Introdução) | Fase 5 | 🟡 Depende da finalização |

**A escolha do periódico-alvo é crítica** e deveria ser priorizada, pois influencia: limite de palavras, limite de referências, formato de citação e processo de revisão.

### Notas Pendentes no Texto
- **"Conferir isso ainda!"** — na contextualização da Introdução (Fase 5), após o parágrafo com as referências Agero (2020), Gioia et al. (2020), Allik et al. (2020)
- **"Verificar possibilidade!"** — na Tabela 6 (Interpretação dos Achados), entre confundimento e relevância prática
- **Agero (2020)** — citado na Introdução mas não aparece na lista de referências-chave (Tabela 7). Verificar se o nome está correto.

### Variável de Raça/Cor — Asterisco sem Explicação
Na Tabela 5, a variável *"% pessoas de raça/cor preta, parda e indígena"* possui um asterisco (`*`) na direção de vulnerabilidade, mas **não há nota de rodapé explicativa**. Recomenda-se adicionar uma nota sobre por que raça/cor é incluída como *proxy* de vulnerabilidade social estrutural.

### Pesos do IVS — Pré-definidos vs. Empíricos
O plano menciona pesos derivados por análise fatorial, mas também cita os pesos do IVS-BH 2012 (~60% socioeconômica, ~40% saneamento). Definir *a priori* se os pesos serão puramente empíricos ou se haverá alguma restrição baseada na literatura.

### Software de Geoprocessamento
O plano menciona **QGIS 2.10.1** (versão de 2015, muito desatualizada). A versão estável atual é o **QGIS 3.x**. Atualizar a referência.

### Referências — Insuficientes
A Tabela 7 lista **8 referências**, provavelmente insuficiente para o artigo completo. Faltam:
- Referências internacionais recentes sobre índices compostos de vulnerabilidade
- Publicação de referência do **ELSI-Brasil** (Lima-Costa et al.)
- Referências sobre a metodologia específica do Censo 2022

---

## 1.4 Avaliação por Fase

| Fase | Descrição | Completude | Qualidade |
|---|---|---|---|
| **Brainstorm** | Contextualização e lacuna | 80% | ⭐⭐⭐⭐⭐ Excelente |
| **Fase 0** | Objetivos e hipóteses | 80% | ⭐⭐⭐⭐ Muito bom |
| **Fase 1** | Tabelas e figuras planejadas | 100% | ⭐⭐⭐⭐ Muito bom |
| **Fase 2** | Método | 95% | ⭐⭐⭐⭐⭐ Excelente |
| **Fase 3** | Resultados | 40% | 🟡 Depende dos dados |
| **Fase 4** | Discussão | 60% | ⭐⭐⭐⭐ Muito bom |
| **Fase 5** | Introdução | 60% | ⭐⭐⭐ Bom (verificar refs) |
| **Fase 6** | Resumo | 60% | ⭐⭐⭐⭐ Muito bom |
| **Fase 7** | Checklist final | 100% | ⭐⭐⭐⭐⭐ Excelente |

---
---

# PARTE 2 — DIAGNÓSTICO DO REPOSITÓRIO DE CÓDIGO

## 2.1 Resumo Geral do Repositório

| Métrica | Valor |
|---|---|
| **Tamanho total do projeto** | ~12.7 GB |
| **Notebooks** | 9 (5 na Fase 1 + 4 na Fase 2) |
| **Scripts Python** | 3 (`mapeamento_variaveis.py`, `busca3.py`, `formatar3.py`) |
| **CSVs brutos do Censo** | 8 arquivos em `dados/` (~2.4 GB) |
| **Bases de dados intermediárias** | ~4.5 GB (SQLite + CSVs em `dados/banco_de_dados/`) |
| **Arquivos marcados como inúteis** | 8 CSVs em `src/ETL/ficheiros_inuteis/` (~4.3 GB) |

---

## 2.2 Duas Pipelines Paralelas

O projeto tem **duas linhas de análise separadas** que coexistem sem integração:

### Fase 1 — IVS "Básico" (`notebooks/Fase1_IVS_Basico/`)
- **5 notebooks** (01 a 05)
- Usa **6 arquivos** do Censo (basico, dom1, dom2, alfab, raca, renda)
- Denominador de saneamento: **V00001** (domicílios particulares permanentes)
- Densidade habitacional: **v0005** (variável pronta do IBGE)
- Renda: normalização min-max invertida **global** (não por município)
- Indicador econômico: apenas renda invertida simples
- **7 indicadores finais** (0 a 1)
- Saída → `dados/banco_de_dados/Base_Analitica_IVS_Calculado.csv` (~50 MB)

### Fase 2 — IVS "Multidimensional" (`notebooks/Fase2_IVS_Multidimensional/`)
- **4 notebooks** (01 a 04)
- Usa **8 arquivos** do Censo (todos da Fase 1 + demografia + parentesco)
- Denominador de saneamento: **V01042** (total de responsáveis — "total de lares reais")
- Densidade habitacional: **(V00005 + V00006) / V01042** (cálculo manual)
- Renda: proxy multidimensional (renda 40% + falta banheiro 20% + improvisados 20% + sobrecarga infantil 20%)
- Classificação de elegibilidade: coluna `Dados_sig` (OK / SIGILOSO / COLETIVO / ZERADO)
- Coluna extra: `Moradia_Predominante` (morfologia urbana)
- **7 indicadores finais** (mesmos 6 + `ind_pobreza_multidimensional` no lugar de `ind_vulnerabilidade_renda`)
- Saída → `banco_de_dados/Base_Analitica_Multidimensional_Calculada.csv` (~74 MB)

**⚠️ As duas fases produzem resultados DIFERENTES para os mesmos indicadores (ex: saneamento) porque usam denominadores diferentes.**

---

## 2.3 Diagnóstico por Pasta

### 📁 Raiz (`/`)

| Arquivo | Status | Observação |
|---|---|---|
| `README.md` | ⚠️ Desatualizado | Menciona scripts que **não existem** (`src/formatador_excel.py`, `src/tradutor_ibge.py`, `unificar.py`). Não menciona a Fase 2. Referencia pasta `data/` que não existe. |
| `estrutura_projeto.md` | ⚠️ Desatualizado | Descreve a estrutura da Fase 1. Não menciona Fase 2, nem `banco_de_dados/` na raiz, nem os novos outputs. |
| `requirements.txt` | 🔴 Incorreto | Lista `sqlite3` e `os` (módulos built-in do Python). Faltam: `numpy`, `openpyxl`, `xlsxwriter`. |
| `.gitignore` | ⚠️ Inconsistente | O `banco_de_dados/` da raiz (Fase 2) não está coberto. |
| `Plano_Artigo_Cientifico_IC_Preenchido.docx` | ✅ OK | Documento de planejamento. |
| `arquivos_git.txt` / `objetos_git.txt` | ⚠️ Dispensáveis | Arquivos de debug do Git. |

### 📁 `dados/` — Dados Brutos do Censo (~2.4 GB)

| Conteúdo | Status | Ação |
|---|---|---|
| 8 CSVs agregados do IBGE | ✅ Correto | Dados-fonte oficiais. Preservar. |
| `dados/banco_de_dados/` | ⚠️ Legado (Fase 1) | Contém outputs da Fase 1 incluindo `Base_Censo_Completa_Unificada.csv` (1 GB!), `temp_merge1.csv` (191 MB) |
| `dados/banco_de_dados/SQL/` | ⚠️ Legado pesado (4.3 GB) | 3 bancos SQLite gerados pela Fase 1 |
| `dados/output/` | ⚠️ Legado | Outputs dos scripts `formatar/` |
| `dados/processed/` | ⚠️ Legado duplicado | Cópias em Excel de dados que também existem em CSV |

### 📁 `banco_de_dados/` (raiz) — Outputs da Fase 2 (~300 MB)

| Arquivo | Tamanho | Descrição |
|---|---|---|
| `Base_Analitica_Multidimensional_Calculada.csv` | 74 MB | Base final da Fase 2 (só setores OK) |
| `Base_Bruta_Multidimensional_Censo2022.csv` | 67 MB | Base bruta antes dos cálculos |
| `Base_Auditoria_Todos_Setores.csv` | 104 MB | Base com TODOS os setores |
| `Base_IVS_Multidimensional_Formatada.xlsx` | 57 MB | Excel formatado com 4 abas |
| `Relatorio_Metodologico_Fase2_Atualizado.xlsx` | 12 KB | Relatório De-Para + Limitações |

### 📁 `notebooks/`

| Subpasta | Status | Observação |
|---|---|---|
| `Fase1_IVS_Basico/` (5 notebooks) | ⚠️ Supersedido | Pipeline substituída pela Fase 2, mas ainda presente |
| `Fase2_IVS_Multidimensional/` (4 notebooks) | ✅ Pipeline ativa | Versão mais robusta |
| `banco_de_dados/` | ⚠️ CSV duplicado | Cópia de 67 MB da base bruta |

### 📁 `docs/` — Documentação

| Arquivo | Status |
|---|---|
| `dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx` | ✅ Referência IBGE |
| `dicionario_de_dados_renda_responsavel.xlsx` | ✅ Dicionário de renda |
| `Dicionario_de_dados_malha_agregados.ods` | ✅ Dicionário da malha |
| `Relatorio_Metodologico_IVS_2022_Corrigido.xlsx` | ⚠️ **Inconsistência interna**: aba "De_Para" lista esgoto como V00312–V00316, mas aba "Mapa_de_Arquivos" lista V00249–V00253. Também não menciona V01042 (usado na Fase 2). |
| `Relatorio_Modular_Variaveis.xlsx` | ⚠️ Útil como referência |

### 📁 `formatar/` — Scripts Auxiliares

| Arquivo | Status | Observação |
|---|---|---|
| `busca3.py` | ⚠️ Legado | É o script que **gerou** o `Relatorio_Metodologico_IVS_2022_Corrigido.xlsx`. Usa variáveis de esgoto V00249-V00253 na aba "Mapa_de_Arquivos", mas V00312-V00316 na aba "De_Para". A inconsistência do relatório vem daqui. |
| `formatar3.py` | ✅ Utilitário | Gera relatório modular cruzando dicionários com CSVs |
| `informacoes_agregados.csv` | ⚠️ Duplicado | Também existe em `dados/output/` |
| `~$*.xlsx` (2 arquivos) | 🔴 Lixo | Temporários do Excel |

### 📁 `src/ETL/`

| Item | Status | Observação |
|---|---|---|
| `mapeamento_variaveis.py` | ⚠️ Legado | Substituído pelos notebooks |
| `ficheiros_inuteis/` (**4.3 GB**) | 🔴 Desperdício | 8 CSVs enormes, sendo que `parentesco` e `demografia` estão duplicados aqui E em `dados/` |

### 📁 `tests/` — Vazia
Nenhum teste automatizado.

---

## 2.4 Problemas Técnicos nos Notebooks

### Fase 1

1. **`03_Auditoria_Dados.ipynb`** — Código **duplicado** (notebook inteiro aparece duas vezes). Número esperado de colunas é **inconsistente** (31 vs 32).

2. **`04_Calculo_Final_IVS.ipynb`** — Esgoto divide por **V00001** (domicílios permanentes), potencialmente incorreto. Normalização de renda **global** (todos os 468k setores do Brasil).

### Fase 2

1. **`01_Extracao_Base_Bruta_Completa.ipynb`** — Função `ler_csv_padronizado` **definida duas vezes** com assinaturas diferentes.

2. **`02_Tratamento_e_Calculo_Multidimensional.ipynb`** — A `razao_moradores_domicilio` usa `(V00005 + V00006) / V01042`. Comentário diz "moradores em casas e tendas" mas V00005/V00006 são "moradores em domicílios permanentes e improvisados". Verificar no dicionário. Normalização de renda continua **global**.

---
---

# PARTE 3 — PROBLEMA FUNDAMENTAL: AUSÊNCIA DO FILTRO ELSI-BRASIL

## 🚨 A falha mais grave de todo o projeto

O Plano do Artigo define **explicitamente** que a análise deve ser feita para os **70 municípios da amostra do ELSI-Brasil**. Porém, **nenhum notebook contém qualquer filtro por município ELSI.**

### Evidências verificadas

- A palavra **"ELSI" não aparece em nenhum arquivo** do repositório (notebooks, scripts, docs — zero ocorrências)
- A base final contém **450.088 setores** de **5.297 municípios** — ou seja, **todo o Brasil**
- **Não existe nenhum arquivo** com a lista dos 70 municípios ELSI
- **Não existe nenhum filtro** do tipo `df[df['NM_MUN'].isin(lista_elsi)]` em qualquer notebook

### O que isso significa na prática

| O que o Plano pede | O que foi feito |
|---|---|
| IVS para **70 municípios** ELSI-Brasil | IVS para **5.297 municípios** (Brasil inteiro) |
| Análise **intraurbana** comparando setores dentro de cada município | Análise **nacional** misturando setores de todos os municípios |
| Normalização que capture desigualdades **dentro** de cada cidade | Normalização min-max **global** (distorce tudo) |
| Base de ~50k–100k setores (estimativa para 70 municípios) | Base de **450.088 setores** |

### Consequências

1. **Todos os outputs atuais são inválidos para o artigo** — processaram o Brasil inteiro
2. **A normalização de renda está distorcida** — min/max global mistura setores de contextos completamente diferentes
3. **Os indicadores não representam análise intraurbana** — que é o objetivo central do artigo
4. **As bases precisam ser reprocessadas** do zero após obter a lista ELSI e aplicar o filtro

---
---

# PARTE 4 — TODOS OS PROBLEMAS CRÍTICOS (RESUMO)

| # | Problema | Gravidade | Impacto |
|---|---|---|---|
| **0** | **Ausência do filtro ELSI-Brasil** — analisou 5.297 municípios em vez de 70 | 🔴 Bloqueante | Todos os outputs são inválidos para o artigo |
| **1** | **Variáveis de esgoto inconsistentes** — o próprio Relatório Metodológico tem divergência interna: aba "De_Para" = V00312–V00316, aba "Mapa_de_Arquivos" = V00249–V00253. Notebooks usam V00312–V00316. | 🔴 Crítico | Cálculo do IVS pode estar incorreto |
| **2** | **Normalização de renda global** — min/max de todos os 450k setores do Brasil, não por município | 🔴 Crítico | Distorce comparações intraurbanas |
| **3** | **Denominadores divergentes** — Relatório Metodológico define V00001 (dom. permanentes), Fase 2 usa V01042 (responsáveis) sem documentação | 🔴 Crítico | Resultados da Fase 2 não estão alinhados com a metodologia documentada |
| **4** | **Duas pipelines paralelas** — Fase 1 e Fase 2 coexistem com resultados diferentes | 🟡 Confuso | Não se sabe qual é a "oficial" |
| **5** | **~8 GB de dados duplicados/obsoletos** espalhados pelo projeto | 🟡 Organizacional | Desperdício de espaço, risco de confusão |
| **6** | **README e docs desatualizados** — mencionam arquivos/scripts que não existem | 🟡 Documentação | Dificulta a compreensão do projeto |
| **7** | **requirements.txt incorreto** — lista módulos built-in, falta numpy/openpyxl/xlsxwriter | 🟢 Menor | Problema de reprodutibilidade |
| **8** | **Código duplicado** nos notebooks (função duplicada na Fase 2, auditoria duplicada na Fase 1) | 🟢 Menor | Manutenção |

---
---

# PARTE 5 — PLANO DE AÇÃO

## 🚨 Prioridade 0 — Filtro ELSI-Brasil (BLOQUEANTE)
- [ ] **Obter a lista oficial dos 70 municípios** do ELSI-Brasil (com códigos IBGE ou nomes exatos)
- [ ] **Criar arquivo de referência** `dados/municipios_elsi_brasil.csv` com colunas `CD_MUN`, `NM_MUN`, `UF`
- [ ] **Implementar filtro** no notebook de extração: filtrar setores cujo código de município esteja na lista ELSI
- [ ] **Reprocessar** toda a pipeline (extração → cálculo → formatação) apenas com os setores dos 70 municípios
- [ ] Todos os outputs atuais serão regenerados após o filtro

## Prioridade 1 — Validação Metodológica (em paralelo com P0)
- [ ] **Resolver inconsistência de esgoto**: a aba "De_Para" do Relatório Metodológico indica V00312–V00316, mas a aba "Mapa_de_Arquivos" indica V00249–V00253. Consultar o dicionário do IBGE (`docs/dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx`) para definir quais são as variáveis corretas
- [ ] **Decidir denominador de saneamento**: V00001 (dom. permanentes, conforme Relatório Metodológico original) vs V01042 (responsáveis, usado na Fase 2 sem documentação). Documentar a decisão
- [ ] **Decidir normalização da renda**: por município (recomendado para análise intraurbana)
- [ ] **Validar v0005**: confirmar que é a média de moradores por dom. particular ocupado (conforme Relatório)

## Prioridade 2 — Limpeza de Arquivos (~8 GB a recuperar)
- [ ] Apagar `src/ETL/ficheiros_inuteis/` inteiro (4.3 GB)
- [ ] Apagar `dados/banco_de_dados/temp_merge1.csv` (191 MB)
- [ ] Apagar `notebooks/banco_de_dados/Base_Bruta_Multidimensional_Censo2022.csv` (67 MB)
- [ ] Apagar `formatar/~$*.xlsx` (2 arquivos temporários do Excel)
- [ ] Avaliar manter ou apagar `dados/banco_de_dados/SQL/` (4.3 GB de SQLite da Fase 1)
- [ ] Avaliar manter ou apagar `dados/banco_de_dados/Base_Censo_Completa_Unificada.csv` (1 GB)

## Prioridade 3 — Reorganização da Estrutura
- [ ] Decidir: manter Fase 1 como arquivo histórico ou removê-la?
- [ ] Unificar saídas: todos os outputs finais em UM diretório
- [ ] Consolidar docs: mover relatórios metodológicos para `docs/`

## Prioridade 4 — Atualizar Documentação
- [ ] Reescrever `README.md`
- [ ] Reescrever `estrutura_projeto.md`
- [ ] Corrigir `requirements.txt` (remover `sqlite3` e `os`, adicionar `numpy`, `openpyxl`, `xlsxwriter`)
- [ ] Atualizar `.gitignore`

## Prioridade 5 — Corrigir o Código (após filtro ELSI + validações)
- [ ] Corrigir `01_Extracao_Base_Bruta_Completa.ipynb` — remover função duplicada + adicionar filtro ELSI
- [ ] Implementar normalização de renda **por município**
- [ ] Corrigir variáveis de esgoto (se necessário após validação)
- [ ] Descartar ou atualizar `busca3.py`
- [ ] Arquivar ou remover notebooks/outputs da Fase 1

## Recomendações para o Plano do Artigo
- [ ] Definir o **periódico-alvo** (impacta formatação inteira)
- [ ] Resolver as notas pendentes: "Conferir isso ainda!" e "Verificar possibilidade!"
- [ ] Adicionar **nota explicativa sobre raça/cor** como proxy de vulnerabilidade social
- [ ] Atualizar referência do **QGIS** para versão 3.x
- [ ] Expandir a **lista de referências** (incluir ELSI-Brasil, Censo 2022, revisões recentes)
- [ ] Definir critério de **pesos do IVS**: empíricos puros vs. guiados pela literatura

---
---

# PARTE 6 — ESTRUTURA PROPOSTA (Após Reorganização)

```
Projeto_IVS_Censo22/
├── README.md                          # Atualizado
├── requirements.txt                   # Corrigido
├── estrutura_projeto.md               # Reescrito
├── .gitignore                         # Atualizado
├── DIAGNOSTICO_COMPLETO_PROJETO.md    # Este documento
├── Plano_Artigo_Cientifico_IC_Preenchido.docx
│
├── dados/                             # Dados brutos do IBGE (imutáveis)
│   ├── Agregados_por_setores_*.csv    # 8 CSVs originais
│   └── municipios_elsi_brasil.csv     # Lista dos 70 municípios ELSI (A CRIAR)
│
├── banco_de_dados/                    # Outputs do pipeline ativo
│   ├── Base_Bruta_ELSI_Censo2022.csv
│   ├── Base_Analitica_IVS_ELSI.csv
│   ├── Base_Auditoria_Todos_Setores.csv
│   ├── Base_IVS_ELSI_Formatada.xlsx
│   └── Relatorio_Metodologico.xlsx
│
├── notebooks/                         # Pipeline de análise
│   ├── 01_Extracao_e_Filtro_ELSI.ipynb
│   ├── 02_Tratamento_e_Calculo_IVS.ipynb
│   ├── 03_Formatacao_e_Dicionarios.ipynb
│   ├── 04_Relatorio_e_Auditoria_Final.ipynb
│   └── _arquivo/                      # (opcional) Fase 1 arquivada
│       └── Fase1_IVS_Basico/
│
├── docs/                              # Documentação e dicionários
│   ├── dicionario_de_dados_*.xlsx
│   ├── Dicionario_de_dados_malha_agregados.ods
│   └── Relatorio_Metodologico_IVS_2022_Corrigido.xlsx
│
├── src/                               # Scripts auxiliares
│   └── ETL/
│       └── mapeamento_variaveis.py
│
└── tests/                             # (futuro) Testes automatizados
```

---

> **Próximo passo bloqueante:** Obter a lista oficial dos 70 municípios do ELSI-Brasil para implementar o filtro e reprocessar toda a análise.
