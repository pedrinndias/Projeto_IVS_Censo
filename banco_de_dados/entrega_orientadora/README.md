# Bases do IVS — Censo 2022

- **70 municípios do ELSI-Brasil:** `Base_ELSI_70Municipios_Censo2022.csv` / `.db`
- **Belo Horizonte:** `Base_BeloHorizonte_Censo2022.csv` / `.db`

Cada par CSV/DB tem exatamente o mesmo conteúdo. O CSV é pra abrir no Excel, o `.db` é um SQLite (dá pra consultar com qualquer ferramenta de SQL, ou pelo Python com `sqlite3`).

## Volumetria

| Base | Setores | Municípios | Setores OK | Sigilosos |
|---|---:|---:|---:|---:|
| ELSI (70 municípios) | 109.032 | 70 | 106.281 (97,5%) | 2.751 (2,5%) |
| Belo Horizonte | 5.166 | 1 | 5.113 (99,0%) | 53 (1,0%) |

## Como abrir o .db

No terminal:
```
sqlite3 Base_ELSI_70Municipios_Censo2022.db
.tables
SELECT * FROM metadados;
```

No Python:
```python
import sqlite3, pandas as pd
con = sqlite3.connect("Base_ELSI_70Municipios_Censo2022.db")
df = pd.read_sql("SELECT * FROM setores_censitarios WHERE Dados_sig='OK'", con)
```

Cada `.db` tem 3 tabelas:
- `setores_censitarios` — os dados (1 linha por setor, 55 colunas)
- `dicionario_variaveis` — descrição de cada coluna
- `metadados` — fonte, data, totais

## Colunas

São 55 no total. Os grupos:

**Identificação (8):** `CD_SETOR`, `CD_UF`, `CD_MUN`, `NM_MUN`, `NM_BAIRRO`, `SITUACAO`, `Moradia_Predominante`, `Dados_sig`.

**Brutas do IBGE (40):**
- População: `v0001`
- Domicílios: `V00001` (DPP Ocupados — denominador padrão), `V00002`, `V00005`, `V00006`
- Água: `V00112` a `V00118`
- Esgoto: `V00312` a `V00316`
- Lixo: `V00398` a `V00402`
- Alfabetização 15+: `V00900` (sabem ler), `V00901` (não sabem)
- Cor/raça: `V01318` (preta), `V01320` (parda), `V01321` (indígena)
- Renda: `V06004` (rendimento médio dos responsáveis em R$)
- Demografia: `V01031`, `V01032`, `V01033`
- Parentesco: `V01042` (pessoas responsáveis — *não* é denominador)
- Auxiliares: `V00047`–`V00052`, `V00236`, `V00238`

**Indicadores IVS já calculados (7):**

| Variável | Fórmula |
|---|---|
| `pct_agua_inad` | (V00112+...+V00118) / V00001 |
| `pct_esgoto_inad` | (V00312+...+V00316) / V00001 |
| `pct_lixo_inad` | (V00398+...+V00402) / V00001 |
| `razao_moradores` | (V00005+V00006) / (V00001+V00002) |
| `pct_analfab` | V00901 / (V00900+V00901) |
| `renda_media` | V06004 |
| `pct_raca_pretpardind` | (V01318+V01320+V01321) / v0001 |

Os indicadores ficam vazios (`NULL` no .db, célula em branco no CSV) para qualquer setor cuja `Dados_sig` não é `OK`.

## Dados_sig

A regra de elegibilidade vem do `Cálculo IVS2012.docx`:

- **OK** — setor entra na análise.
- **SIGILOSO** — `v0001` ou `V00001` estão sigilosos (o IBGE preserva o anonimato em contagens muito pequenas).
- **COLETIVO** — `V00001 = 0` mas com população: toda a gente do setor mora em domicílio coletivo (asilo, presídio).
- **ZERADO** — `v0001 = 0`, setor sem população.

Não apareceram setores COLETIVO ou ZERADO nos 70 municípios do ELSI.

## Sigilo na variável de analfabetismo

O IBGE não publica `V00901` (analfabetos 15+) quando o valor é muito pequeno. Isso atinge **15,76% dos setores OK** no recorte ELSI e **23,5% dos setores OK** em Belo Horizonte. O sigilo não é aleatório: concentra-se justamente nos setores urbanos com poucos analfabetos absolutos. Nesses casos, `pct_analfab` fica vazio. A auditoria detalhada está em `banco_de_dados/eda/auditoria_analfabetismo_municipio.csv`.

