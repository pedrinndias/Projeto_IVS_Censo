# Guia do Projeto IVS — Censo 2022

> **Documento mestre de retomada.** Reúne, num só lugar, o *porquê* científico, o *como*
> metodológico e o *estado atual* do código. Serve como ponto de partida para retomar o
> trabalho e como base de alinhamento entre o pesquisador e o assistente (Claude).
>
> **Atualizado em:** 22/05/2026 (revisão metodológica: denominador V00001 + taxa de analfabetismo)
> **Documentos relacionados no repositório:** [`README.md`](README.md) ·
> [`estrutura_projeto.md`](estrutura_projeto.md) ·
> [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md) ·
> [`Backup/DIAGNOSTICO_COMPLETO_PROJETO.md`](Backup/DIAGNOSTICO_COMPLETO_PROJETO.md) *(histórico)*

---

## 1. Identidade do Projeto

| Item | Detalhe |
|---|---|
| **Título** | Índice de Vulnerabilidade à Saúde (IVS) intraurbano — Censo Demográfico 2022 |
| **Tipo** | Iniciação Científica (bolsista) |
| **Instituição** | Fiocruz Minas — Instituto René Rachou (IRR) |
| **Área** | Saúde Coletiva — Saúde Urbana e Epidemiologia Espacial |
| **Pesquisador** | Pedro Dias Soares |
| **Período** | Março/2026 – Fevereiro/2027 |
| **Produto final** | Relatório Final de IC + artigo científico submetido a periódico |

---

## 2. Objetivo Científico

### Objetivo geral
Avaliar as desigualdades intraurbanas em saúde por meio da construção de um **Índice de
Vulnerabilidade à Saúde (IVS)** para um conjunto de cidades brasileiras, usando dados do
Censo Demográfico 2022.

### Objetivos específicos
1. Construir um IVS intraurbano, ao nível do **setor censitário**, para os **70 municípios
   da amostra do ELSI-Brasil** (Estudo Longitudinal da Saúde dos Idosos Brasileiros).
2. Analisar a **distribuição espacial** do IVS (mapas temáticos).
3. Descrever a distribuição das variáveis socioeconômicas e de saneamento por setor.
4. Comparar o perfil de vulnerabilidade entre municípios de diferentes regiões e portes.

### Pergunta de pesquisa (PICOS)
Qual a distribuição espacial da vulnerabilidade à saúde nos setores censitários dos
municípios do ELSI-Brasil, construída a partir das variáveis do Censo 2022, e quais padrões
intraurbanos de desigualdade emergem dessa distribuição?

| | |
|---|---|
| **P** — População | Setores censitários urbanos dos 70 municípios do ELSI-Brasil (Censo 2022) |
| **I** — Exposição | Variáveis de saneamento e socioeconômicas em nível de setor |
| **C** — Comparação | Distribuição do IVS entre setores e entre municípios/regiões |
| **O** — Desfecho | IVS contínuo (0–1) e categorizado em 4 faixas de risco |
| **S** — Estudo | Ecológico, com dados agregados por setor censitário |

### Hipóteses
- **H0:** não há padrão espacial sistemático do IVS dentro dos municípios.
- **H1:** setores periféricos apresentam IVS mais alto que áreas centrais (padrão
  centro-periferia descrito na literatura).

---

## 3. Fundamentação Metodológica

O projeto é um **estudo ecológico**. A unidade de análise é o **setor censitário** — a menor
unidade territorial do IBGE — o que permite enxergar desigualdades *dentro* de cada cidade
(análise intraurbana).

**Referências metodológicas centrais:**
- **IVS-BH 2012** (SMS-BH, 2013) — referência principal. Indicador composto que sintetiza
  variáveis de saneamento e socioeconômicas por setor censitário em Belo Horizonte.
- **ISU de Passarelli-Araujo (2023)** — Índice de Saúde Urbana aplicado a 6 capitais
  brasileiras; evidência empírica do padrão centro-periferia.
- **Caiaffa et al. (2021)** e **Buss & Pellegrini Filho (2007)** — determinantes sociais
  e territoriais da saúde.
- **Matos & Rodrigues (2019)** — referência sobre análise fatorial.

**A lacuna:** não existe um IVS padronizado e atualizado com dados do **Censo 2022** para o
conjunto de municípios do ELSI-Brasil. Os estudos anteriores usaram o Censo 2010.

### Etapas estatísticas planejadas
1. Análise descritiva (frequências, média, mediana, desvio-padrão) por município.
2. Padronização **min-max** de cada variável para escala 0–1.
3. **Análise fatorial / ACP** para identificar a estrutura latente e definir os pesos.
4. Cálculo do IVS como média ponderada das variáveis padronizadas (referência IVS-BH:
   dimensão socioeconômica ~60%, saneamento ~40%).
5. Categorização dos setores em 4 faixas (Baixo / Médio / Elevado / Muito Elevado).
6. Geoprocessamento e mapas temáticos no **QGIS**.

### Ética
Usa apenas dados secundários, públicos e anônimos do IBGE. Conforme a Resolução CNS
510/2016 (art. 1°, II e III), **não requer submissão ao CEP**. Segue a LGPD (Lei 13.709/2018).

---

## 4. As Variáveis do IVS

O IVS sintetiza **7 variáveis** em **2 dimensões**. A direção é sempre "↑ valor = ↑
vulnerabilidade" (a renda é invertida).

| Dimensão | Variável | Direção |
|---|---|---|
| **Saneamento** | % domicílios com abastecimento de água inadequado ou ausente | ↑ |
| | % domicílios com esgotamento sanitário inadequado ou ausente | ↑ |
| | % domicílios com destino do lixo inadequado ou ausente | ↑ |
| **Socioeconômica** | Razão de moradores por domicílio (densidade habitacional) | ↑ |
| | % de pessoas analfabetas | ↑ |
| | Rendimento nominal mensal médio das pessoas responsáveis | ↓ (invertido) |
| | % de pessoas de raça/cor preta, parda e indígena | ↑ |

### De-Para: Censo 2010 → Censo 2022

| Componente | IVS 2012 (Censo 2010) | Censo 2022 | Denominador (Relatório) |
|---|---|---|---|
| Água inadequada | V013–V015 | V00112 a V00118 (7 var.) | V00001 |
| Esgoto inadequado | V019–V028 | **V00312–V00316** ✅ (confirmado no dicionário oficial) | V00001 |
| Lixo inadequado | V037–V042 | V00398 a V00402 (5 var.) | V00001 |
| Analfabetismo (15+) | V068–V134 | V00901 / (V00900 + V00901) | V00900 + V00901 (pop. 15+) |
| Densidade habitacional | Pop. / dom. ocupados | (V00005 + V00006) / (V00001 + V00002) *(reproduz o V0005 do IBGE)* | V00001 + V00002 |
| Renda | % fam. ≤ 2 SM | V06004 (rendimento médio, invertido) | — |
| Raça/cor | Pretos + Pardos + Indígenas | V01318 + V01320 + V01321 | v0001 (pop. total) |

### Limitações do Censo 2022 documentadas
| O IVS 2012 pedia | Limitação no Censo 2022 | Solução adotada |
|---|---|---|
| % chefes com < 4 anos de estudo | Anos de instrução não disponíveis nos agregados | Taxa de analfabetismo (V00901) |
| % famílias ≤ 2 salários mínimos | Faixas salariais não disponíveis | Rendimento médio (V06004) invertido |
| Coef. óbitos cardiovasculares | IBGE registrou só se houve óbito, sem causa | Buscar DATASUS (SIM) futuramente |

---

## 5. O Código — Pipeline Ativa e Legados

A **pipeline ativa** vive em `notebooks/Fase3_EDA_ELSI/` e finalmente aplica o
recorte dos 70 municípios ELSI. As versões anteriores foram movidas para `Backup/`.

### Fase 3 — EDA com filtro ELSI *(ativa)*
`notebooks/Fase3_EDA_ELSI/` — 2 notebooks (01→02).

| Notebook | O que faz |
|---|---|
| `01_Extracao_Filtragem_ELSI` | Lê os 8 CSVs do Censo, cruza por (UF + nome normalizado) com `dados/municipios_elsi_brasil.csv`, filtra apenas os setores dos 70 municípios, faz o merge unificado, classifica morfologia urbana e roda auditoria de integridade. Saída: `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv`. |
| `02_Analises_Descritivas` | EDA completa seguindo o framework FIOCRUZ: tipagem com sigilo → `Dados_sig` → 7 proporções brutas com denominador **V00001** → descritivas globais/municípios/regiões → histogramas → boxplots por região → outliers (IQR) → mapa de missing → matriz de correlação (Pearson + Spearman). Saídas: CSVs e PNGs em `banco_de_dados/eda/`. |

Decisões metodológicas consolidadas (**revisão de 22/05/2026**):
- **Denominador domiciliar V00001** (Domicílios Particulares Permanentes Ocupados) —
  equivalente no Censo 2022 do `V002` do Censo 2010, padrão do IVS-BH 2012. O `V01042`
  (arquivo Parentesco) **foi descartado**: é uma contagem de *pessoas* responsáveis,
  não de domicílios. A leitura anterior do `Cálculo IVS2012.docx` (*"considerar o número
  de responsáveis como total de domicílios"*) só vale para detectar setores 100%
  coletivos, não como denominador.
- **Razão de moradores:** `(V00005 + V00006) / (V00001 + V00002)` — reproduz o V0005 do IBGE.
- **Taxa de analfabetismo:** `V00901 / (V00900 + V00901)` (o denominador é o total de
  pessoas com 15+ anos; a fórmula anterior `V00901 / V00900` era incorreta e gerava
  setores com taxa > 1).
- **Sigilo:** `X` do IBGE convertido para `NaN`. Em `pct_analfab`, o sigilo em V00901
  (~16% dos setores OK) é mantido como `NaN` (não imputado a zero).
- **`Dados_sig`:** `SIGILOSO` (`v0001` ou `V00001` sigilosos) / `COLETIVO`
  (`V00001 = 0` com `v0001 > 0`) / `ZERADO` (`v0001 = 0`) / `OK` (participa das análises).

### Legados em `Backup/`
- `Backup/Fase1_IVS_Basico/` — 5 notebooks; pipeline inicial (sem filtro ELSI), denominador V00001.
- `Backup/Fase2_IVS_Multidimensional/` — 4 notebooks; segunda iteração (sem filtro ELSI), introduziu V01042 e a Proxy de Extrema Pobreza Multidimensional.
- `Backup/ETL/`, `Backup/formatar/`, `Backup/banco_de_dados/` — scripts auxiliares e bases intermediárias antigas.
- `Backup/DIAGNOSTICO_COMPLETO_PROJETO.md` — diagnóstico histórico.

> ⚠️ **O que ainda falta para o IVS final:** análise fatorial (pesos), composição
> ponderada das duas dimensões e categorização em 4 faixas de risco. O notebook 02
> entrega as descritivas necessárias para alimentar essa próxima etapa.

---

## 6. Estrutura de Pastas

```
Projeto_IVS_Censo22/
│
├── README.md                          Apresentação geral
├── GUIA_DO_PROJETO.md                 Este documento (mestre de retomada)
├── estrutura_projeto.md               Arquitetura técnica
├── requirements.txt                   Dependências Python
├── LICENSE                            Licença MIT
│
├── dados/                             DADOS BRUTOS DO IBGE (~2.4 GB, imutáveis)
│   ├── Agregados_por_setores_*.csv     8 CSVs oficiais do Censo 2022
│   ├── municipios_elsi_brasil.csv     Lista oficial dos 70 municípios ELSI
│   ├── output/                        Outputs de scripts auxiliares
│   └── processed/                     Exports em Excel (legado)
│
├── banco_de_dados/                    OUTPUTS DA PIPELINE ATIVA (Fase 3)
│   ├── Base_ELSI_Bruta_Censo2022.csv  Saída do Notebook 01 (filtrada por ELSI)
│   └── eda/                           Saídas do Notebook 02 (descritivas + figuras)
│       ├── descritivas_globais.csv
│       ├── descritivas_por_municipio.csv
│       ├── descritivas_por_regiao.csv
│       ├── outliers.csv
│       ├── missing_por_municipio.csv
│       ├── correlacao_pearson.csv
│       ├── correlacao_spearman.csv
│       └── figuras/                   PNGs (histogramas, boxplots, correlação)
│
├── notebooks/Fase3_EDA_ELSI/          PIPELINE ATIVA
│   ├── 01_Extracao_Filtragem_ELSI.ipynb
│   ├── 02_Analises_Descritivas.ipynb
│   └── README.md
│
├── docs/                              DOCUMENTAÇÃO-FONTE
│   ├── Cálculo IVS2012.docx           Metodologia operacional do IVS-BH
│   ├── guia_analises.docx             Framework FIOCRUZ de EDA
│   ├── indice_vulnerabilidade2012 (2).pdf  IVS-BH 2012 oficial
│   ├── Estudo Longitudinal da Saúde dos Idosos Brasileiros.docx
│   ├── Plano de trabalho.pdf
│   └── Plano_Artigo_Cientifico_IC_Preenchido.docx
│
├── Backup/                            LEGADOS (Fases 1 e 2, scripts antigos)
│   ├── Fase1_IVS_Basico/              5 notebooks da pipeline inicial
│   ├── Fase2_IVS_Multidimensional/    4 notebooks da segunda iteração
│   ├── ETL/                           mapeamento_variaveis.py
│   ├── formatar/                      busca3.py, formatar3.py
│   ├── banco_de_dados/                CSVs intermediários antigos
│   └── DIAGNOSTICO_COMPLETO_PROJETO.md
│
└── tests/                             test_pipeline_fase3.py (16 testes sanity-check)
```

### Os 8 arquivos-fonte do Censo 2022

| Arquivo | Dimensão | Variáveis-chave |
|---|---|---|
| `..._basico_BR_20250417.csv` | Identificação + população | `CD_SETOR`, `NM_MUN`, `v0001`, `v0005` |
| `..._caracteristicas_domicilio1_BR.csv` | Denominador habitacional | `V00001`, `V00002`, `V00005`, `V00006` |
| `..._caracteristicas_domicilio2_BR_20250417.csv` | Saneamento | Água, esgoto, lixo, banheiro |
| `..._alfabetizacao_BR.csv` | Educação | `V00900` (alfabetizados 15+ — *sabe ler/escrever*), `V00901` (analfabetos 15+). Total 15+ = V00900 + V00901 |
| `..._cor_ou_raca_BR.csv` | Vulnerabilidade social | `V01318`, `V01320`, `V01321` |
| `..._renda_responsavel_BR.csv` | Renda | `V06004` (rendimento médio mensal) |
| `..._demografia_BR.csv` | Sobrecarga infantil (Fase 2) | `V01031`–`V01033` (pop. 0–14) |
| `..._parentesco_BR.csv` | Total de lares reais (Fase 2) | `V01042` (responsáveis) |

---

## 7. Estado Atual

| Etapa | Status |
|---|---|
| Obtenção dos dados brutos do Censo 2022 | ✅ Concluída |
| Mapeamento e dicionários de variáveis | ✅ Concluída |
| Pipeline ETL Fase 2 (sem filtro ELSI) | ⚠️ Legada — substituída pela Fase 3 |
| Lista oficial dos 70 municípios ELSI-Brasil | ✅ [`dados/municipios_elsi_brasil.csv`](dados/municipios_elsi_brasil.csv) |
| Fase 3 — Notebook 01 (extração + filtro ELSI) | ✅ [`notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb`](notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb) |
| Fase 3 — Notebook 02 (análises descritivas) | ✅ [`notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb`](notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb) — implementado |
| Normalização de renda por município | 🔴 Pendente |
| Validação das variáveis de esgoto | ✅ Concluída — V00312–V00316 confirmado no dicionário oficial do IBGE |
| Análise fatorial / pesos / cálculo do IVS final | 🔴 Pendente |
| Categorização em 4 faixas de risco | 🔴 Pendente |
| Mapas temáticos (QGIS) | 🔴 Pendente |
| Redação do artigo científico | 🟡 Plano preenchido, redação pendente |

A pipeline ativa agora é a **Fase 3** em `notebooks/Fase3_EDA_ELSI/`, que finalmente
aplica o recorte dos 70 municípios. As Fases 1 e 2 ficam preservadas como histórico.

---

## 8. Problemas Conhecidos

Detalhamento completo em [`Backup/DIAGNOSTICO_COMPLETO_PROJETO.md`](Backup/DIAGNOSTICO_COMPLETO_PROJETO.md) *(histórico)* e em [`docs/Relatorio_Integridade_Projeto.md`](docs/Relatorio_Integridade_Projeto.md).

| # | Problema | Gravidade |
|---|---|---|
| **0** | ~~**Ausência do filtro ELSI-Brasil**~~ — **resolvido na Fase 3**: `notebooks/Fase3_EDA_ELSI/01` filtra os 70 municípios ELSI (109.032 setores) antes de qualquer cálculo. | ✅ Resolvido |
| **1** | ~~**Variáveis de esgoto inconsistentes**~~ — **resolvido**: o dicionário oficial do IBGE (`dados/dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx` e o recorte em `docs/Apresentacoes_IVS/Dicionario_IBGE_Oficial_Variaveis_do_Projeto.xlsx`) confirma que **V00312–V00316** é o bloco de esgoto inadequado (fossa rudimentar, vala, rio/lago/mar, outra forma, inexistente). V00309–V00311 são adequadas (rede geral, fossa séptica). Os notebooks já usam V00312–V00316; o diagnóstico empírico está na célula `step4b` do Notebook 02. | ✅ Resolvido |
| **2** | **Normalização de renda global** — usa min/max de todos os setores do Brasil; deveria ser por município para capturar desigualdade intraurbana. | 🔴 Crítico |
| **3** | ~~Denominadores divergentes~~ — **resolvido em 22/05/2026**: consolidado **V00001** (Dom. Particulares Permanentes Ocupados) como denominador domiciliar, padrão do IVS-BH 2012. O **V01042 foi descartado** (é contagem de pessoas, não de domicílios). Decisão empiricamente validada: com V00001 nenhuma proporção de saneamento estoura 1,0. | ✅ Resolvido |
| **4** | ~~Duas pipelines paralelas~~ — **resolvido**: a Fase 3 é a oficial; as Fases 1 e 2 foram arquivadas em `Backup/` como histórico. | ✅ Resolvido |
| **5** | **~8 GB de dados duplicados/obsoletos** espalhados pelo projeto. | 🟡 Organizacional |
| **6** | ~~README/docs parcialmente desatualizados~~ — **resolvido**: `docs/Relatorio_EDA_Fase3_IVS_ELSI.md` foi regerado em 12/06/2026 sobre a metodologia V00001 e está consistente com os CSVs atuais; `Relatorio_Integridade_Projeto.md` revisado na mesma data. | ✅ Resolvido |
| **7** | ~~requirements.txt incorreto~~ — **resolvido**: lista `pandas`, `numpy`, `matplotlib`, `openpyxl`, `xlsxwriter`; sem módulos built-in. | ✅ Resolvido |
| **8** | **Código duplicado nos notebooks** — função `ler_csv_padronizado` definida duas vezes na Fase 2; auditoria duplicada na Fase 1. | 🟢 Menor |

---

## 9. Plano de Retomada — Próximos Passos

Ordem sugerida de ataque ao reentrar no projeto:

### Prioridade 0 — Desbloquear (filtro ELSI-Brasil) ✅ Concluída na Fase 3
- [x] Obter a lista oficial dos **70 municípios do ELSI-Brasil**
      (fonte: <https://elsi.cpqrr.fiocruz.br/amostra/>).
- [x] Criar `dados/municipios_elsi_brasil.csv`.
- [x] Adicionar o filtro no notebook de extração (Fase 3, Notebook 01).
- [x] Reprocessar a pipeline apenas com os setores dos 70 municípios.

### Prioridade 1 — Validação metodológica (em paralelo)
- [x] Resolver a inconsistência das variáveis de esgoto consultando o dicionário do IBGE — **V00312–V00316 confirmado** (dicionário oficial versionado).
- [x] Decidir e **documentar** o denominador de saneamento — **V00001** consolidado em 22/05/2026.
- [ ] Mudar a normalização de renda para **por município** (Notebook 03).
- [x] Validar a razão de moradores `(V00005+V00006)/(V00001+V00002)` — reproduz o V0005 do IBGE.

### Prioridade 2 — Completar o cálculo do IVS
- [ ] Implementar a **análise fatorial / ACP** para definir os pesos.
- [ ] Calcular o **IVS final** (média ponderada das variáveis padronizadas).
- [ ] Categorizar os setores em 4 faixas (Baixo / Médio / Elevado / Muito Elevado).

### Prioridade 3 — Limpeza e organização
- [ ] Remover `src/ETL/ficheiros_inuteis/` e demais duplicados (~8 GB).
- [ ] Decidir o destino da Fase 1 (arquivar ou remover).
- [ ] Corrigir `requirements.txt`, `.gitignore` e a documentação.

### Prioridade 4 — Geoprocessamento e artigo
- [ ] Mapas temáticos no QGIS (atualizar referência: usar QGIS 3.x, não 2.10.1).
- [ ] Definir o **periódico-alvo** (impacta toda a formatação do artigo).
- [ ] Avançar a redação seguindo o `Plano_Artigo_Cientifico_IC_Preenchido.docx`.

---

## 10. Cronograma do Bolsista

| Atividade | Período |
|---|---|
| Programa de Inserção do IRR + Curso Introdutório | Mar–Abr/2026 |
| Revisão bibliográfica (SciELO, PubMed) | Mar–Dez/2026 |
| Reuniões periódicas com a orientadora | Mar/2026–Fev/2027 |
| Análise da consistência do banco de dados | Mar–Jul/2026 |
| Análise dos dados (estatística + mapas) | Mar–Set/2026 |
| Cálculo do IVS (fatorial, padronização, ponderação) | Ago–Set/2026 |
| Mapas temáticos (QGIS) | Set/2026 |
| Trabalhos para congressos (RAIC, Saúde Coletiva) | Conforme chamadas |
| Redação do artigo (tabelas→resultados→discussão→introdução→resumo) | Out–Dez/2026 |
| Redação do Relatório Final de IC | Dez/2026–Fev/2027 |
| Submissão do artigo | Fev/2027 |

---

## 11. O Plano do Artigo — Estado das Fases

O `Plano_Artigo_Cientifico_IC_Preenchido.docx` segue a sequência de redação
**tabelas → método → resultados → discussão → introdução → resumo** (Pereira & Galvão;
checklist STROBE).

| Fase | Conteúdo | Completude |
|---|---|---|
| Brainstorm | Contextualização e lacuna | ~80% |
| Fase 0 | Objetivos e hipóteses | ~80% |
| Fase 1 | Tabelas e figuras planejadas | 100% |
| Fase 2 | Método | ~95% |
| Fase 3 | Resultados | ~40% (depende da análise) |
| Fase 4 | Discussão | ~60% |
| Fase 5 | Introdução | ~60% (verificar referências) |
| Fase 6 | Resumo | ~60% |
| Fase 7 | Checklist final | 100% |

**Pendências do plano a resolver:**
- Definir o **periódico-alvo** e suas normas (limite de palavras, referências, citação).
- Preencher: Pesquisador(a) Principal, objetivo refinado (versão final).
- Resolver as notas internas "Conferir isso ainda!" (Introdução) e "Verificar
  possibilidade!" (Tabela 6 da Discussão).
- Verificar a referência "Agero (2020)" — citada mas ausente da lista de referências-chave.
- Adicionar **nota de rodapé** explicando raça/cor como *proxy* de vulnerabilidade social
  estrutural (a Tabela 5 tem um asterisco sem explicação).
- Expandir a lista de referências (hoje 8) — incluir publicação de referência do
  ELSI-Brasil, metodologia do Censo 2022 e revisões internacionais recentes.
- Decidir o critério dos **pesos do IVS**: empíricos puros (análise fatorial) ou guiados
  pela literatura (~60% socioeconômica / ~40% saneamento, conforme IVS-BH 2012).

---

## 12. Como Executar

**Pré-requisitos:** Python 3.10+ e os 8 CSVs do Censo 2022 em `dados/`.

```bash
pip install -r requirements.txt
```

Executar os notebooks da **pipeline ativa (Fase 3)** na ordem numérica:

```
notebooks/Fase3_EDA_ELSI/  →  01 → 02
```

> O Notebook 01 extrai e filtra os 70 municípios ELSI (gera `Base_ELSI_Bruta_Censo2022.csv`);
> o Notebook 02 roda a EDA. As Fases 1 e 2 em `Backup/` são legado e não fazem parte da
> pipeline atual.

> A execução completa consome bastante RAM e tempo (~2.4 GB de CSVs brutos). Os notebooks
> leem apenas as colunas necessárias para proteger a memória.

---

## 13. Referências

- **SMS-BH.** *Índice de Vulnerabilidade da Saúde 2012.* Belo Horizonte: Secretaria
  Municipal de Saúde, 2013.
- **Passarelli-Araujo, H.** Mapeando as disparidades socioeconômicas de saúde urbana: um
  estudo comparativo entre seis capitais brasileiras. *Rev. Bras. Est. Pop.*, v. 40, 2023.
- **Caiaffa, W. T. et al.** *Saúde urbana, cidades e a interseção de sistemas.* Rio de
  Janeiro: Fiocruz, 2021.
- **Buss, P. M.; Pellegrini Filho, A.** A saúde e seus determinantes sociais. *Physis*,
  v. 17, n. 1, p. 77–93, 2007.
- **Gioia, T. B.; Pereira, A. C. F.; Raminelli, J. A.** Avaliação de métodos para
  construção de um índice de vulnerabilidade de saúde para Londrina-PR. *Hygeia*, v. 16,
  2020.
- **Matos, D. A. S.; Rodrigues, E. C.** *Análise fatorial.* Brasília: Enap, 2019.
- **Allik, M. et al.** *Developing a small-area deprivation measure for Brazil.* Glasgow:
  University of Glasgow, 2020.
- **Kalache, A.; Gatti, A. A.** Envelhecimento ativo: um paradigma para o século XXI.
  *Rev. Bras. Geriatr. Gerontol.*, v. 23, n. 1, 2020.
- **IBGE.** *Censo Demográfico 2022 — Agregados por Setores Censitários.* Rio de Janeiro:
  IBGE, 2022.
