# Relatório de Integridade do Projeto IVS — Censo 2022 / ELSI-Brasil

> **Nota de revisão (12/06/2026):** o diagnóstico original é de 19/05/2026. Os achados de
> denominador, taxa de analfabetismo, regra `Dados_sig` e os números das tabelas foram
> **atualizados para a metodologia consolidada em 22/05/2026** (denominador **V00001** +
> taxa `V00901 / (V00900 + V00901)`). Fonte da verdade: [`GUIA_DO_PROJETO.md`](../GUIA_DO_PROJETO.md)
> e [`banco_de_dados/entrega_orientadora/README.md`](../banco_de_dados/entrega_orientadora/README.md).

> **Tipo:** Diagnóstico técnico — auditoria de notebooks, variáveis e outputs
> **Data:** 19 de maio de 2026 (revisado em 12/06/2026 para a metodologia V00001)
> **Escopo:** Pipeline ativa (Fase 3) + documentação + dicionário de variáveis
> **Pesquisador:** Pedro Dias Soares — IC Fiocruz Minas / IRR

## 0. Status das Correções Aplicadas (sessão de 19/05/2026)

| Item | Ação | Resultado |
|---|---|---|
| C1 — Clipping silencioso | Diagnóstico adicionado **antes** do clipping no Notebook 02 (célula `step4`); exporta [`diagnostico_proporcoes_fora_intervalo.csv`](../banco_de_dados/eda/diagnostico_proporcoes_fora_intervalo.csv) | ✅ Resolvido. **Achado (pós-revisão V00001):** com o denominador V00001 e a taxa de analfabetismo `V00901 / (V00900 + V00901)`, **nenhuma** proporção ultrapassa 1,0 (0 setores em todas as variáveis). Os 10 setores `pct_analfab > 1` que existiam eram artefato da fórmula antiga `V00901 / V00900`. |
| C2 — Variáveis de esgoto | Célula `step4b` adicionada com comparação empírica V00249–V00253 vs V00312–V00316; exporta [`diagnostico_esgoto_312_vs_249.csv`](../banco_de_dados/eda/diagnostico_esgoto_312_vs_249.csv) | 🟡 Diagnóstico pronto. **Decisão final depende da orientadora** após análise do CSV exportado. |
| C3 — README desatualizado | Reescrito para refletir Fase 3 ativa, **V00001 como denominador**, status real das etapas | ✅ Resolvido. |
| R4 — Extremos de razão de moradores | Diagnóstico no Notebook 02 (célula `step4`); exporta [`extremos_razao_moradores.csv`](../banco_de_dados/eda/extremos_razao_moradores.csv) | ✅ **Achados (pós-revisão V00001):** com o denominador `(V00001 + V00002)` o mínimo passou a **1,00** — o setor de Brasília com razão 0,17 era artefato do V01042 e deixou de existir. Persiste o máximo de 8,79 em Portel/PA (verificar população coletiva). |
| R5 — Regra COLETIVO | Regra ancorada em **`V00001 == 0` com `v0001 > 0`** (toda a população em domicílios coletivos) | ✅ Resolvido. **Achado:** 0 setores COLETIVO dentro dos 70 municípios ELSI (os candidatos caem em SIGILOSO, com `V00001` sigiloso). |
| R6 — IQR não informativa | Adicionadas colunas `p95`, `n_acima_p95`, `pct_acima_p95`, `iqr_nao_informativo` em [`outliers.csv`](../banco_de_dados/eda/outliers.csv) | ✅ Resolvido. **Confirma:** água/esgoto/lixo flagrados como IQR não-informativo. |
| Testes sanity | Criado [`tests/test_pipeline_fase3.py`](../tests/test_pipeline_fase3.py) (16 testes) | ✅ 15 passam, 1 skipped (esperado). |

**Pendências carregadas para a próxima fase (Notebook 03+):**
- R2 — Normalização de renda por município.
- R3 — Política de tratamento de sigilo variável a variável para o cálculo do IVS final.
- C2 — Decisão metodológica sobre faixa de esgoto (V00249–V00253 vs V00312–V00316), após análise do diagnóstico com a orientadora.

---

---

## 1. Sumário do Diagnóstico

| Bloco | Status | Síntese |
|---|---|---|
| Pipeline Fase 3 — Notebook 01 (Extração + Filtro ELSI) | 🟢 **Aprovado** | Filtro funciona, 70/70 municípios localizados, 109.032 setores extraídos, auditoria interna passa. |
| Pipeline Fase 3 — Notebook 02 (EDA) | 🟢 **Aprovado com ressalvas** | Cálculos consistentes com `Cálculo IVS2012.docx`; 6 ressalvas metodológicas a documentar. |
| Variáveis vs. dicionário IBGE | 🟡 **Pendência herdada** | Esgoto (V00312–V00316 vs V00249–V00253) não foi confrontado ainda com o dicionário oficial. |
| Outputs (CSVs + figuras) | 🟢 **Aprovado** | 8 artefatos esperados presentes, contagens batem (70 municípios × 7 vars = 490 linhas). |
| Documentação | 🟢 **Sincronizada** | `README.md`, `GUIA_DO_PROJETO.md` e `estrutura_projeto.md` alinhados à metodologia V00001 (revisão de 22/05). |
| Dependências (`requirements.txt`) | 🟢 **Adequado** | Cobre o uso real (`pandas`, `numpy`, `matplotlib`, `openpyxl`, `xlsxwriter`). |
| Bloqueante para o IVS final | 🔴 **Análise fatorial + categorização pendentes** | EDA entrega base para a próxima etapa, mas índice ainda não calculado. |

**Veredito geral para apresentação:** a EDA da Fase 3 é tecnicamente sólida e reprodutível; o caminho até o IVS está bem delineado. Após a revisão de 22/05 (denominador V00001), restam 2 pendências metodológicas antes da análise fatorial (validação da faixa de esgoto e normalização de renda por município).

---

## 2. Estrutura do Projeto — Inventário

### 2.1 Arquivos-fonte (`dados/`)
| Arquivo | Tamanho | Status |
|---|---|---|
| `Agregados_por_setores_basico_BR_20250417.csv` | 130 MB | ✅ Presente |
| `Agregados_por_setores_caracteristicas_domicilio1_BR.csv` | 177 MB | ✅ Presente |
| `Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv` | 747 MB | ✅ Presente |
| `Agregados_por_setores_alfabetizacao_BR.csv` | 701 MB | ✅ Presente |
| `Agregados_por_setores_cor_ou_raca_BR.csv` | 192 MB | ✅ Presente |
| `Agregados_por_setores_renda_responsavel_BR.csv` | 26 MB | ✅ Presente |
| `Agregados_por_setores_demografia_BR.csv` | 85 MB | ✅ Presente |
| `Agregados_por_setores_parentesco_BR.csv` | 346 MB | ✅ Presente |
| `municipios_elsi_brasil.csv` | 1,9 KB | ✅ 70 linhas + cabeçalho, chave única |

### 2.2 Notebooks da pipeline ativa
| Notebook | Linhas executadas | Status |
|---|---|---|
| `notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb` | 8 seções, todas com output | ✅ Executado com sucesso (saída: 109.032 × 47) |
| `notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb` | 13 seções, todas com output | ✅ Executado com sucesso (saída: 106.281 setores OK) |

### 2.3 Outputs gerados (`banco_de_dados/`)
| Arquivo | Esperado | Conferido | Status |
|---|---|---|---|
| `Base_ELSI_Bruta_Censo2022.csv` | 109.032 setores × 47 cols, 17,2 MB | 17,2 MB | ✅ |
| `eda/elegibilidade_setores.csv` | 2 linhas (OK/SIGILOSO) | OK=106.281; SIGILOSO=2.751 | ✅ |
| `eda/descritivas_globais.csv` | 7 linhas (1 por indicador) | 7 linhas | ✅ |
| `eda/descritivas_por_municipio.csv` | 70 × 7 = 490 linhas | 491 (490 + cabeçalho) | ✅ |
| `eda/descritivas_por_regiao.csv` | 5 × 7 = 35 linhas | 36 (35 + cabeçalho) | ✅ |
| `eda/outliers.csv` | 7 linhas | 7 + cabeçalho | ✅ |
| `eda/missing_por_municipio.csv` | 70 linhas | 71 (70 + cabeçalho) | ✅ |
| `eda/correlacao_pearson.csv` | 7×7 | 7×7 | ✅ |
| `eda/correlacao_spearman.csv` | 7×7 | 7×7 | ✅ |
| `eda/figuras/histogramas.png` | — | presente | ✅ |
| `eda/figuras/boxplots_por_regiao.png` | — | presente | ✅ |
| `eda/figuras/matriz_correlacao.png` | — | presente | ✅ |
| `eda/figuras/missing_por_municipio.png` | — | presente | ✅ |

---

## 3. Conformidade do Dicionário de Variáveis

### 3.1 Cruzamento (código no notebook ↔ uso metodológico)

| Componente IVS | Variáveis no notebook | Denominador | Conformidade |
|---|---|---|---|
| % água inadequada | `V00112` … `V00118` | `V00001` | ✅ Denominador padrão IVS-BH 2012 (Dom. Particulares Permanentes Ocupados). |
| % esgoto inadequado | `V00312` … `V00316` | `V00001` | 🟡 **Pendência** — numerador a confirmar: aba "De_Para" → V00312–V00316; aba "Mapa_de_Arquivos" → V00249–V00253. O denominador (V00001) está consolidado. |
| % lixo inadequado | `V00398` … `V00402` | `V00001` | ✅ Consistente. |
| Razão de moradores | `V00005 + V00006` | `V00001 + V00002` | ✅ Reproduz o V0005 do IBGE. |
| % analfabetismo (15+) | `V00901` | `V00900 + V00901` | ✅ Total de pessoas com 15+ anos. |
| Rendimento médio | `V06004` (uso direto, sem denominador) | — | ⚠️ Ainda **bruto**; normalização por município pendente. |
| % preta/parda/indígena | `V01318 + V01320 + V01321` | `v0001` | ✅ Consistente. |
| Identificação | `CD_SETOR` (15 d.), derivados `CD_UF` (2 d.), `CD_MUN` (7 d.) | — | ✅ |
| Sigilo / elegibilidade | `Dados_sig` ∈ {SIGILOSO, COLETIVO, ZERADO, OK} | — | ⚠️ COLETIVO e ZERADO definidos mas não ocorreram nos 70 municípios — somente SIGILOSO (2,52%). Confirmar que isto é esperado. |
| Morfologia urbana | `V00047`…`V00052` → categoria predominante | — | ✅ Funciona; 2.751 setores ficam "Indefinido/Sem Moradia" e correspondem exatamente aos SIGILOSO da etapa seguinte (coincidência consistente). |

### 3.2 Renomeações no notebook 01

As colunas-chave têm grafias diferentes entre os 8 CSVs do IBGE (`CD_SETOR`, `CD_setor`, `setor`). O notebook 01 padroniza tudo via `rename_cols` no `ler_csv_padronizado` — **conferido e correto**.

---

## 4. Achados Quantitativos da EDA

### 4.1 Universo amostral
- **70 municípios** (22 UFs, todas as 5 regiões; Sudeste 26, Nordeste 22, Sul 9, Centro-Oeste 7, Norte 6).
- **109.032 setores** extraídos (≈ 23,3% dos 468.099 setores brasileiros).
- **106.281 setores OK** após regras `Dados_sig` (97,48%).
- **2.751 setores SIGILOSO** (2,52%).
- **0 setores COLETIVO** e **0 ZERADO** — confirmar com a orientadora se é esperado.

### 4.2 Tabela 1 (proposta para o artigo) — descritivas globais
| Variável | n | Mediana | P25 / P75 | Média | DP | Assim. | Curt. |
|---|--:|--:|--:|--:|--:|--:|--:|
| pct_agua_inad | 106.281 | 0,000 | 0,000 / 0,017 | 0,083 | 0,221 | 3,07 | 8,46 |
| pct_esgoto_inad | 106.280 | 0,000 | 0,000 / 0,023 | 0,092 | 0,231 | 2,76 | 6,52 |
| pct_lixo_inad | 106.281 | 0,000 | 0,000 / 0,071 | 0,126 | 0,264 | 2,23 | 3,68 |
| razao_moradores | 106.281 | 2,72 | 2,48 / 2,93 | 2,70 | 0,40 | 0,09 | 3,90 |
| pct_analfab | 89.527 | 0,028 | 0,013 / 0,052 | 0,039 | 0,041 | 2,98 | 17,67 |
| renda_media (R$) | 106.262 | 2.546 | 1.735 / 4.755 | 4.141 | 4.124 | 3,76 | 49,94 |
| pct_raca_pretpardind | 106.279 | 0,576 | 0,356 / 0,708 | 0,530 | 0,229 | −0,39 | −0,81 |

→ As 5 proporções têm forte assimetria à direita e massa em zero; em todas, **mediana e IQR são preferíveis a média e DP** na redação do artigo.

### 4.3 Correlações (Spearman — mais robusta dada a assimetria)
| Par | ρ | Leitura |
|---|--:|---|
| renda_media × pct_raca_pretpardind | **−0,809** | Maior correlação absoluta. Reproduz o eixo racial-econômico clássico. |
| pct_analfab × renda_media | −0,754 | Forte. |
| pct_analfab × pct_raca_pretpardind | +0,625 | Forte. |
| pct_esgoto_inad × pct_analfab | +0,452 | Moderada — bloco saneamento ↔ socioeconômico. |
| pct_agua_inad × pct_esgoto_inad | +0,445 | Moderada — coesão da dimensão saneamento. |
| **pct_lixo_inad × razao_moradores** | **−0,036** | **Atenção:** quase nula. |

→ **Implicação para a análise fatorial:** `pct_lixo_inad` tende a carregar fraco. A estrutura de 2 fatores (saneamento + socioeconômico) sugerida pelo IVS-BH continua plausível, mas pode ser melhor verificá-la com **KMO** e **teste de esfericidade de Bartlett** antes da rotação.

### 4.4 Outliers (regra IQR clássica)
- `pct_agua_inad`, `pct_esgoto_inad`, `pct_lixo_inad`: ~20% setores classificados como outliers — **falso positivo metodológico**, pois P25=P50=0 colapsa o IQR. Não é problema dos dados, é limitação da regra IQR em distribuição zero-inflada. Documentar.
- `renda_media`: 10,2% outliers acima de R$ 9.285 — consistente com cauda longa de altíssima renda; máximo R$ 170.418 (1 setor) merece verificação manual.
- `razao_moradores`: 3,6% outliers — máximo 8,79 (verificar se é um setor com população coletiva não detectada).
- `pct_raca_pretpardind`: 0 outliers — distribuição mais simétrica (curtose negativa).

---

## 5. Achados Críticos (pente fino)

### 🔴 CRÍTICO

**C1. Clipping de proporções em [0, 1] — resolvido com V00001** ✅
- Local: [02_Analises_Descritivas.ipynb](notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb), célula `step4`, linha
  `df_ok[c] = df_ok[c].clip(lower=0, upper=1)`, precedida do diagnóstico que exporta
  [`diagnostico_proporcoes_fora_intervalo.csv`](../banco_de_dados/eda/diagnostico_proporcoes_fora_intervalo.csv).
- O `max=1,0000` exato em água/esgoto/lixo/raça é **legítimo** (existem setores 100% inadequados),
  não um valor truncado: o diagnóstico confirma **0 setores com proporção > 1** em todas as variáveis.
- Os 10 setores `pct_analfab > 1` (máx 5,33) que motivaram este achado eram artefato da fórmula
  antiga `V00901 / V00900`. Com `V00901 / (V00900 + V00901)` a taxa fica limitada a [0, 1] e o
  clipping passou a ser apenas uma salvaguarda inócua.

**C2. Variáveis de esgoto não validadas contra o dicionário oficial do IBGE**
- A escolha `V00312`–`V00316` foi herdada da Fase 2. O Relatório Metodológico tinha duas abas com codificação diferente (V00312–V00316 vs V00249–V00253). A Fase 3 não reabriu essa decisão.
- **Ação recomendada:** abrir `docs/dicionario_de_dados_agregados_por_setores_censitarios_20250417.xlsx` (presente em `dados/processed/` ou `docs/`), localizar a definição das duas faixas, e confirmar **antes** da análise fatorial. Esta variável carrega 0,45 (Pearson) com `pct_agua_inad` — alterar o intervalo muda o resultado do fator.

**C3. Documentação sincronizada** ✅
- `README.md`, `GUIA_DO_PROJETO.md` e `estrutura_projeto.md` foram alinhados à metodologia
  consolidada em 22/05/2026: filtro ELSI aplicado (Fase 3), **denominador V00001** (V01042 descartado),
  taxa de analfabetismo `V00901 / (V00900 + V00901)` e Fase 3 como pipeline ativa.
- A fonte da verdade da operacionalização é [`banco_de_dados/entrega_orientadora/README.md`](../banco_de_dados/entrega_orientadora/README.md).

### 🟡 RELEVANTE

**R1. Renda em escala global, ainda não normalizada por município**
- Documentado no GUIA como "Prioridade 1". A EDA já tratou a `renda_media` em sua escala bruta — apropriado para a EDA. Mas o IVS final exige normalização **por município** (recomendação central do plano).
- O notebook 02 não faz a normalização e não precisa fazer. Mas o Notebook 03 (a criar) precisa.

**R2. Missingness alta em `pct_analfab` (15,7%) concentrada nas grandes cidades**
- São Caetano do Sul 29,7%, Porto Alegre 27,5%, Curitiba 23,1%, BH 22,5%, Rio 20,0%, SP 19,7%, Campinas 19,9%, Pato Branco 18,2%, São Bernardo 18,5%, Araçatuba 18,5%.
- Causa provável: sigilo do IBGE em setores residenciais com **poucos moradores 15+** (apartamentos, etc.). Não é erro do código.
- **Risco:** se a análise fatorial usar pairwise complete, esses setores entram parcialmente; se usar listwise, descarta ~17 mil setores **das principais capitais**. Decisão metodológica a tomar com a orientadora.

**R3. Variáveis-base auxiliares fora da regra `Dados_sig`**
- A regra atual considera "OK" qualquer setor que tenha `v0001` e `V00001` não-sigilosos — mas o setor pode ter `V00900`/`V00901` (denominador do analfab.) ou `V06004` (renda) sigilosos, e nesse caso entra na análise com NaN.
- Isto é intencional na EDA (`min_count=1` preserva a transparência), mas vale tornar explícito no Relatório de EDA. Para o **IVS final** será necessário decidir como cada variável-componente trata o sigilo (imputação, exclusão da variável, exclusão do setor).

**R4. Extremos de `razao_moradores` — mínimo resolvido com V00001** ✅
- O mínimo de **0,17** descrito originalmente era artefato do denominador V01042. Com `(V00001 + V00002)`
  o mínimo passou a **1,00** (ao menos um morador por domicílio ocupado), que é o piso fisicamente correto.
- Persiste o máximo de **8,79** (≈ 9 moradores por domicílio) em Portel/PA — possível setor com moradias
  coletivas não capturado pela regra COLETIVO. **Ação:** inspecionar os setores mais extremos
  (`extremos_razao_moradores.csv`) quanto a população coletiva.

**R5. 0 setores COLETIVO e 0 ZERADO**
- A regra `COLETIVO` (revisada) marca o setor quando **`V00001 == 0` com `v0001 > 0`** — ou seja, há população mas nenhum domicílio particular permanente ocupado (toda a população em coletivos: presídios, asilos, alojamentos). Nenhum setor dos 70 municípios ELSI satisfaz isso.
- **Por quê 0:** os setores tipicamente coletivos chegam com `V00001` **sigiloso** (NaN) e caem em `SIGILOSO`, que é avaliado antes de `COLETIVO`. **Recomendação:** confirmar com a orientadora que nenhum setor 100% coletivo está entrando como `OK` indevidamente (cruzar `SITUACAO`/população coletiva do IBGE).

**R6. Outlier-rule IQR não informativa em distribuições zero-infladas**
- Como P25 e mediana são iguais a zero para água/esgoto/lixo, a regra 1,5×IQR rotula 18–20% dos setores como outliers. Não é problema dos dados — é a regra inadequada para essa forma de distribuição.
- **Ação:** no relatório do artigo, substituir a contagem de outliers nessas variáveis por **percentil 95** ou por uma análise visual com boxplot (já presente).

### 🟢 MENOR

- **M1.** `requirements.txt` está adequado para a Fase 3 (não falta nada). Os módulos built-in citados como problema no GUIA (`sqlite3`, `os`) já foram removidos.
- **M2.** Saídas CSV usam `utf-8-sig` (BOM) — bom para Excel; verificar se o QGIS lê corretamente quando importar shapefiles cruzados com esses CSVs (preferir sem BOM se houver problemas).
- **M3.** `Backup/Fase2_IVS_Multidimensional/` ainda contém legados que duplicam ~200 MB em `Backup/banco_de_dados/`. Não impacta a Fase 3, mas justifica limpeza futura.
- **M4.** Nenhum teste unitário (`tests/` vazio). Aceitável para escopo de IC, mas valeria adicionar 1–2 testes sanity-check para regressão (ex.: "70 municípios encontrados", "n_OK = 106.281").

---

## 6. O Que Está Funcionando Bem (mérito da implementação)

1. **Detecção automática da raiz do projeto** (`_find_project_root`) — torna os notebooks portáveis entre Windows e Linux, executáveis a partir de qualquer cwd.
2. **Encoding fallback** (`utf-8 → latin1 → cp1252`) — robusto contra a inconsistência real do IBGE.
3. **Leitura em chunks** dos 2 CSVs maiores (701 MB e 747 MB) — protege a RAM.
4. **Chave composta (UF + nome normalizado)** no filtro ELSI — necessária e implementada corretamente (testada com Tabatinga AM/SP).
5. **`min_count=1` no somatório de numeradores** — preserva o sigilo nas proporções calculadas (decisão correta para EDA, divergente da Fase 2 que zerava — mas a Fase 2 visava o índice final, contexto diferente).
6. **Tratamento de renda decimal com vírgula** (`'2453,03'` → `'2453.03'` antes de `to_numeric`) — sutil e correto; sem isso `V06004` viraria 99% NaN.
7. **Auditoria de integridade no Notebook 01** — 5 checks automáticos (linhas, unicidade da chave, sigilo preservado, variáveis essenciais, 70 municípios). Reproduzível.
8. **Separação de responsabilidades 01 → 02:** o 01 só extrai e filtra (sigilo preservado); o 02 trata e calcula. Boa engenharia.

---

## 7. O Que Falta — Roteiro até o IVS Final

Em ordem cronológica (alinhada com o GUIA_DO_PROJETO):

1. **Resolver C2** — confrontar V00312–V00316 com o dicionário oficial do IBGE (`.xlsx`/`.ods`). Se confirmar, encerrar a pendência no GUIA.
2. ~~Resolver C1~~ ✅ — com V00001 + taxa de analfabetismo corrigida, nenhuma proporção excede 1 (clipping é salvaguarda inócua).
3. **R5 (COLETIVO)** — confirmar com a orientadora que nenhum setor 100% coletivo entra como `OK` indevidamente.
4. ~~Atualizar README~~ ✅ — README, GUIA e estrutura_projeto sincronizados com a metodologia V00001.
5. **Notebook 03 (a criar)** — normalização min-max **por município** das 7 variáveis (invertendo renda). Saída: `Base_Padronizada_Municipal.csv`.
6. **Notebook 04 (a criar)** — análise fatorial / ACP. Verificar KMO e Bartlett; decidir entre 1 ou 2 fatores; calcular pesos.
7. **Notebook 05 (a criar)** — composição do IVS como média ponderada; categorização em 4 faixas (Baixo / Médio / Elevado / Muito Elevado, com cortes definidos via quartis ou via Jenks).
8. **Geoprocessamento (QGIS 3.x)** — join com a malha de setores do IBGE; mapas temáticos por município.
9. **Artigo** — preencher as 7 tabelas planejadas (a Tabela 1 já tem dados; Tabela 5 precisa da nota de rodapé sobre raça/cor como proxy).

---

## 8. Conclusão para Apresentação

A pipeline da Fase 3 está **tecnicamente sólida**: o filtro ELSI funciona, a base bruta foi gerada com integridade auditada, a EDA cobre todos os requisitos do framework FIOCRUZ e produz tabelas e figuras consistentes. As ressalvas listadas em §5 são **metodológicas**, não defeitos de implementação, e nenhuma invalida os resultados da EDA — todas têm caminho de resolução claro.

Para apresentar com segurança:
- Os números do §4 são **defensáveis**.
- A correlação Spearman renda × raça/cor = −0,81 e a estrutura geral das correlações sustentam o desenho da análise fatorial.
- O bloqueante histórico do projeto (ausência do filtro ELSI) está **resolvido e reproduzível**.
- O próximo marco mensurável é o Notebook 03 (normalização por município).

---
*Relatório produzido por revisão automatizada do código-fonte e dos artefatos em `banco_de_dados/eda/` no commit atual da branch `claude/angry-rosalind-57b969`.*
