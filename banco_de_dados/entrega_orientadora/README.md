# Bases do IVS — Censo 2022

- **70 municípios do ELSI-Brasil:** `Base_ELSI_70Municipios_Censo2022.csv` / `.db`
- **Belo Horizonte:** `Base_BeloHorizonte_Censo2022.csv` / `.db`
- **Dicionário de variáveis:** `Dicionario_Variaveis_Projeto.csv` / `.xlsx`

Cada par CSV/DB tem exatamente o mesmo conteúdo. O CSV é pra abrir no Excel, o `.db` é um SQLite (dá pra consultar com qualquer ferramenta de SQL, ou pelo Python com `sqlite3`).

> **Reprodutibilidade:** tudo aqui é gerado por `scripts/gerar_entrega_orientadora.py` a partir de `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` (saída do Notebook 01). Até 09/08/2026 estes arquivos vinham de um script ad-hoc que não estava no repositório.

## Atualização de 09/08/2026

| Mudança | O que era | O que é agora |
|---|---|---|
| Colunas | 55 | **95** |
| Classificação territorial | só `SITUACAO` | `CD_SIT`, `CD_TIPO`, `CD_FCU`, `NM_FCU` — permite isolar **favelas e comunidades urbanas** |
| Faixas etárias | 0–4, 5–9, 10–14 | pirâmide completa (`V01031`–`V01041`) |
| Indicadores calculados | 7 (IVS) | **23** (os 7 do IVS + morfologia, banheiro, envelhecimento) |
| `dicionario_variaveis` | coluna + descrição | **+ tema, origem, arquivo-fonte do Censo e fórmula** |
| `Dados_sig` | massas d'água contavam como `SIGILOSO` | agora contam como `ZERADO` (1.736 setores) |

## Volumetria

| Base | Setores | Municípios | Setores OK | Urbanos na base | **Recorte de análise** | FCU na base | FCU no recorte |
|---|---:|---:|---:|---:|---:|---:|---:|
| ELSI (70 municípios) | 109.032 | 70 | 106.281 (97,5%) | 106.347 | **104.108** | 19.507 | 19.452 |
| Belo Horizonte | 5.166 | 1 | 5.113 (99,0%) | 5.166 | **5.113** | 702 | 702 |

> **"Urbanos na base" não é o recorte.** Ela conta `SITUACAO = Urbana` em todos os setores, inclusive zerados e sigilosos — por isso dá 106.347, número maior que os 106.281 elegíveis e impossível como recorte. O recorte é a interseção das duas condições, `Dados_sig='OK' AND urbano=1`, que é exatamente o que a consulta SQL recomendada abaixo devolve.

## Como abrir o .db

No terminal:
```
sqlite3 Base_ELSI_70Municipios_Censo2022.db
.tables
SELECT * FROM metadados;
SELECT coluna, descricao, arquivo_fonte FROM dicionario_variaveis;
```

No Python:
```python
import sqlite3, pandas as pd
con = sqlite3.connect("Base_ELSI_70Municipios_Censo2022.db")
# recorte de análise do IVS: setores urbanos elegíveis
df = pd.read_sql("SELECT * FROM setores_censitarios WHERE Dados_sig='OK' AND urbano=1", con)
```

Cada `.db` tem 3 tabelas:
- `setores_censitarios` — os dados (1 linha por setor, 104 colunas)
- `dicionario_variaveis` — **o que é cada coluna, de qual arquivo do Censo ela vem e como o indicador é calculado**
- `metadados` — fonte, data, totais, denominador adotado

## Colunas

### Identificação e classificação territorial (16)

`CD_SETOR`, `CD_UF`, `CD_MUN`, `NM_MUN`, `NM_BAIRRO`, `SITUACAO`, `CD_SIT`, `CD_TIPO`, `CD_FCU`, `NM_FCU`, `Moradia_Predominante`, `Moradia_Predominante_Agrupada`, `Dados_sig`, `urbano`, `is_fcu`, `regiao`.

Três delas resolvem demandas específicas:

| Coluna | Uso |
|---|---|
| `urbano` | `1` = setor urbano. **O recorte de análise do IVS é `Dados_sig='OK' AND urbano=1`** (104.108 setores). Os rurais ficam na base para auditoria, mas fora da análise. |
| `is_fcu` | `1` = setor de Favela e Comunidade Urbana (`CD_TIPO = 1`). São 19.507 em toda a base (17,9% de 109.032) e **19.452 no recorte de análise** (18,7% de 104.108) — use sempre o mesmo filtro do recorte ao calcular percentuais. |
| `CD_SIT` | Situação detalhada: 1–3 urbana, 5–8 rural, 9 massa d'água (população zero). |

### Variáveis brutas do IBGE (56)

Todas com descrição oficial e arquivo-fonte na tabela `dicionario_variaveis`. Em resumo:

- População: `v0001` · Domicílios: `V00001` (DPPO — **denominador padrão**), `V00002`, `V00005`, `V00006`
- Tipo de domicílio: `V00047`–`V00052` (permanentes) e `V00053`–`V00058` (improvisados)
- Água: `V00112`–`V00118` · Esgoto: `V00312`–`V00316` · Lixo: `V00398`–`V00402` · Banheiro: `V00236`, `V00238`, `V00495`
- Alfabetização 15+: `V00900` (sabem ler), `V00901` (não sabem)
- Cor/raça: `V01318` (preta), `V01320` (parda), `V01321` (indígena)
- Renda: `V06004` (rendimento médio dos responsáveis, R$), `V06001` (nº de responsáveis) e `V06005` (variância do rendimento) — as duas últimas servem para auditar a primeira
- Demografia: `V01031`–`V01041` (pirâmide etária completa, de 0–4 a 70+)
- Parentesco: `V01042` (pessoas responsáveis — *não* é denominador), `V01062`/`V01063` (responsáveis por sexo)

### Indicadores calculados (26)

**Os 7 componentes do IVS:**

| Variável | Fórmula |
|---|---|
| `pct_agua_inad` | (V00112+…+V00118) / V00001 |
| `pct_esgoto_inad` | (V00312+…+V00316) / V00001 |
| `pct_lixo_inad` | (V00398+…+V00402) / V00001 |
| `razao_moradores` | (V00005+V00006) / (V00001+V00002) |
| `pct_analfab` | V00901 / (V00900+V00901) |
| `renda_media` | V06004 |
| `pct_raca_pretpardind` | (V01318+V01320+V01321) / v0001 |

**`renda_media_sem_extremo`** — pedida em 01/09/2026. É a mesma coluna `renda_media`, com
**um único setor vazio**: o `310620005650366` (Belo Horizonte, Senhor dos Passos), que
declara R$ 170.418,06 — maior valor de toda a base, 55,7× a mediana do município, num setor
de favela com 186 domicílios e 518 pessoas. Ela fica encostada na `renda_media` no arquivo,
e a `renda_media` **não** foi alterada: as duas lado a lado é o que torna a exclusão
auditável. Em Belo Horizonte, no recorte de análise, a média cai de R$ 4.682,30 para
R$ 4.649,88 (−0,69%) e o máximo passa a ser R$ 45.385,44 (Belvedere).

> A exclusão é **nominal**, de um setor só, e não da classe `SUSPEITO` (66 setores) nem da
> `EXTREMO` (3.292). A lista está em `SETORES_RENDA_EXCLUIDA`, em `src/ivs_censo/renda.py`,
> e também na tabela `metadados` de cada `.db`. Excluir por classe seria outra decisão de
> método, e mudaria a EDA inteira.

**Morfologia e habitação:** `pct_moradia_convencional` (casa + vila/condomínio + apartamento), `pct_moradia_nao_convencional`, `pct_apartamento`, `pct_casa`, `pct_casa_vila_condominio`, `pct_dom_improv`, `pct_hab_precaria`.

**Banheiro:** `pct_sem_banheiro`, `pct_sem_banheiro_nem_sanitario`.

**Sociodemográficos:** `pct_resp_feminino`, `pct_crianca_0a4`, `pct_pop_0a14`, `pct_idoso_60mais`.

**Envelhecimento** (definições de Galvão et al., *Hygeia* v.21, e2106, 2025, Quadro 1):

| Variável | Fórmula | Observação |
|---|---|---|
| `iep_setor` | (60+ / menores de 15) × 100 | Índice de Envelhecimento Populacional |
| `rdi_setor` | (60+ / 15 a 59) × 100 | Razão de Dependência de Idosos |
| `prop_70mais_entre_60mais` | (70+ / 60+) × 100 | **Proxy** de longevidade — não é o LI, que exigiria a faixa 75+, inexistente nos agregados por setor |

Os indicadores ficam vazios (`NULL` no .db, célula em branco no CSV) para qualquer setor cuja `Dados_sig` não é `OK`.

## Dados_sig

A regra de elegibilidade vem do `Cálculo IVS2012.docx`:

- **OK** — setor entra na análise (106.281 setores).
- **SIGILOSO** — `v0001` ou `V00001` estão sigilosos (1.015 setores).
- **ZERADO** — `v0001 = 0`, setor sem população (1.736 setores, dos quais 78 são massas d'água com `CD_SIT = 9`).
- **COLETIVO** — `V00001 = 0` mas com população: todos moram em domicílio coletivo (asilo, presídio). Nenhum caso no recorte ELSI.

> A ordem de avaliação foi corrigida em 09/08/2026: população zero é checada **antes** do sigilo. Antes disso, 1.736 setores sem população apareciam como `SIGILOSO`, inflando a contagem de dados suprimidos pelo IBGE. Nenhum setor `OK` mudou de classe.

## Sigilo na variável de analfabetismo

O IBGE não publica `V00901` (analfabetos 15+) quando o valor é muito pequeno. Isso atinge **15,76% dos setores OK** no recorte ELSI e **23,5% dos setores OK** em Belo Horizonte. O sigilo não é aleatório: concentra-se justamente nos setores urbanos com poucos analfabetos absolutos. Nesses casos, `pct_analfab` fica vazio. A auditoria detalhada está em `banco_de_dados/eda/auditoria_analfabetismo_municipio.csv`.
