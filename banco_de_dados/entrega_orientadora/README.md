# Entrega para a orientadora — Bases do IVS Censo 2022

**Gerado em:** 22/05/2026
**Responsável:** Pedro Dias Soares (bolsista IC — Fiocruz Minas / IRR)

Quatro arquivos cobrindo dois recortes solicitados:

| Recorte | CSV | SQLite |
|---|---|---|
| 70 municípios da amostra ELSI-Brasil | `Base_ELSI_70Municipios_Censo2022.csv` | `Base_ELSI_70Municipios_Censo2022.db` |
| Apenas Belo Horizonte (MG) | `Base_BeloHorizonte_Censo2022.csv` | `Base_BeloHorizonte_Censo2022.db` |

---

## Volumetria

| Base | Setores | Municípios | Setores OK | Sigilosos | Tamanho CSV | Tamanho DB |
|---|---|---|---|---|---|---|
| ELSI 70 munic. | 109.032 | 70 | 106.281 (97,48%) | 2.751 (2,52%) | 33,26 MB | 19,47 MB |
| Belo Horizonte | 5.166 | 1 | 5.113 (99,0%) | 53 (1,0%) | 1,58 MB | 0,95 MB |

---

## Estrutura dos arquivos

Os dois formatos (CSV e SQLite) contêm exatamente o mesmo conteúdo principal: uma
tabela com **55 colunas** (47 variáveis brutas do IBGE + `Dados_sig` + 7
indicadores derivados do IVS).

### CSV
- Separador: `;` (ponto e vírgula)
- Encoding: UTF-8 com BOM (abre direto no Excel)
- Decimal: `.` (ponto)
- Valores ausentes / sigilo do IBGE: célula vazia

### SQLite (`.db`)
Três tabelas:

1. **`setores_censitarios`** — a tabela principal, 1 linha por setor censitário.
2. **`dicionario_variaveis`** — descrição de cada uma das 55 colunas (`coluna`, `descricao`).
3. **`metadados`** — informações sobre o recorte: fonte, data de extração,
   regra de elegibilidade, totais (`chave`, `valor`).

Para inspecionar com SQLite no terminal:

```bash
sqlite3 Base_ELSI_70Municipios_Censo2022.db
> .tables
> SELECT * FROM metadados;
> SELECT * FROM dicionario_variaveis LIMIT 10;
> SELECT NM_MUN, COUNT(*) FROM setores_censitarios GROUP BY NM_MUN ORDER BY 2 DESC LIMIT 5;
```

No Python:

```python
import sqlite3, pandas as pd
con = sqlite3.connect('Base_ELSI_70Municipios_Censo2022.db')
df = pd.read_sql('SELECT * FROM setores_censitarios WHERE Dados_sig = "OK"', con)
```

---

## Grupos de variáveis

| Grupo | Colunas |
|---|---|
| Identificação | `CD_SETOR`, `CD_UF`, `CD_MUN`, `NM_MUN`, `NM_BAIRRO`, `SITUACAO`, `Moradia_Predominante`, `Dados_sig` |
| População total | `v0001` |
| Domicílios (denominadores) | `V00001` (DPP Ocupados, denominador padrão IVS), `V00002` (DPI Ocupados), `V00005`, `V00006` (moradores) |
| Água inadequada — numerador | `V00112`, `V00113`, `V00114`, `V00115`, `V00116`, `V00117`, `V00118` |
| Esgoto inadequado — numerador | `V00312`, `V00313`, `V00314`, `V00315`, `V00316` |
| Lixo inadequado — numerador | `V00398`, `V00399`, `V00400`, `V00401`, `V00402` |
| Alfabetização (15+) | `V00900` (sabem ler/escrever), `V00901` (não sabem) |
| Cor/raça | `V01318` (preta), `V01320` (parda), `V01321` (indígena) |
| Renda | `V06004` (rendimento médio dos responsáveis, R$) |
| Demografia (apoio Fase 2) | `V01031`, `V01032`, `V01033` |
| Parentesco | `V01042` (responsáveis pelo domicílio — **não é** denominador) |
| Auxiliares (extraídas do Notebook 01) | `V00047`–`V00052`, `V00236`, `V00238` |
| **Indicadores IVS derivados** | `pct_agua_inad`, `pct_esgoto_inad`, `pct_lixo_inad`, `razao_moradores`, `pct_analfab`, `renda_media`, `pct_raca_pretpardind` |

---

## Indicadores IVS — fórmulas (revisão de 22/05/2026)

| Variável | Fórmula | Observação |
|---|---|---|
| `pct_agua_inad` | (V00112 + V00113 + V00114 + V00115 + V00116 + V00117 + V00118) / V00001 | Domicílios com fonte inadequada de água sobre DPP Ocupados |
| `pct_esgoto_inad` | (V00312 + V00313 + V00314 + V00315 + V00316) / V00001 | Domicílios com destino inadequado de esgoto sobre DPP Ocupados |
| `pct_lixo_inad` | (V00398 + V00399 + V00400 + V00401 + V00402) / V00001 | Domicílios com destino inadequado de lixo sobre DPP Ocupados |
| `razao_moradores` | (V00005 + V00006) / (V00001 + V00002) | Reproduz V0005 oficial do IBGE — média de moradores por DPO |
| `pct_analfab` | V00901 / (V00900 + V00901) | Taxa de analfabetismo entre pessoas com 15+ anos |
| `renda_media` | V06004 (direto) | Rendimento médio mensal dos responsáveis (R$) |
| `pct_raca_pretpardind` | (V01318 + V01320 + V01321) / v0001 | Pretos + pardos + indígenas sobre população total |

Setores com `Dados_sig` diferente de `OK` recebem `NaN` (CSV: célula vazia /
SQLite: `NULL`) nos sete indicadores derivados.

---

## Regra de elegibilidade `Dados_sig`

| Classe | Quando ocorre | ELSI 70 munic. | Belo Horizonte |
|---|---|---|---|
| **OK** | Setor válido para todas as análises | 106.281 (97,48%) | 5.113 (99,0%) |
| **SIGILOSO** | `v0001` ou `V00001` estão como sigilo (NaN) | 2.751 (2,52%) | 53 (1,0%) |
| **COLETIVO** | `V00001 = 0` com `v0001 > 0` (toda a população em coletivos) | 0 | 0 |
| **ZERADO** | `v0001 = 0` (setor sem população) | 0 | 0 |

Regra inspirada no `Cálculo IVS2012.docx` (SMS-BH, 2013). Para reproduzir a EDA
da Fase 3, filtrar `WHERE Dados_sig = 'OK'`.

---

## Tratamento de sigilo

Os valores `X` do IBGE (sigilo estatístico — contagens muito pequenas que não
podem ser divulgadas para preservar confidencialidade) foram convertidos para
`NaN`/`NULL`. Isso afeta especialmente `V00901` (analfabetos 15+): cerca de
**15,76% dos setores ELSI OK** têm sigilo nessa variável, concentrados em
capitais (São Paulo, Rio, BH, Porto Alegre). Em Belo Horizonte, a perda chega a
**22,5%** dos setores OK. Esses setores ficam com `pct_analfab = NULL` — vide
documento de revisão metodológica e auditoria detalhada em
`banco_de_dados/eda/auditoria_analfabetismo_*.csv`.

---

## Notas finais

- Os números completos das alterações metodológicas estão na apresentação
  `docs/Apresentacao_Revisao_Denominador_Analfabetismo.pptx` (sessão 22/05/2026).
- A pipeline geradora destes arquivos é reproduzível a partir do
  `Notebook 01` da Fase 3, da `Base_ELSI_Bruta_Censo2022.csv` e do script
  `scripts_temp/gerar_entregaveis_orientadora.py` (descartável, não versionado).
- Fonte oficial: IBGE, *Censo Demográfico 2022 — Agregados por Setores
  Censitários*, atualização de 17/04/2025.
