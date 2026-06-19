# Saídas da EDA — `banco_de_dados/eda/`

Tabelas-resumo e figuras da Análise Exploratória da Fase 3. Os CSVs aqui são versionados
como **histórico de execução**; as bases grandes (`Base_*.csv`, `diagnostico_esgoto_*`,
`*_por_setor.csv`) ficam fora do git (ver `.gitignore`).

## Procedência dos arquivos

### ✅ Gerados pela pipeline (`notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb`)
Reexecutáveis rodando `01 → 02`:

| Arquivo | Célula do NB02 |
|---|---|
| `descritivas_globais.csv` · `descritivas_por_municipio.csv` · `descritivas_por_regiao.csv` | `step5`, `step6`, `step7` / `step13` |
| `outliers.csv` | `step10` |
| `missing_por_municipio.csv` | `step11` |
| `correlacao_pearson.csv` · `correlacao_spearman.csv` | `step12` |
| `elegibilidade_setores.csv` | `step3` / `step13` |
| `diagnostico_proporcoes_fora_intervalo.csv` · `extremos_razao_moradores.csv` | `step4` |
| `habitacao_precaria_{global,por_regiao,por_municipio}.csv` | `hab-precaria` |
| `inadequacao_banheiro_{global,por_regiao,por_municipio}.csv` | `banheiro-inad` |
| `resp_feminino_{global,por_regiao,por_municipio}.csv` | `resp-fem` |
| `estrutura_etaria_{global,por_regiao,por_municipio,contagem_por_municipio}.csv` | `idade-estrutura` |
| `figuras/*.png` (histogramas, boxplots, matriz_correlacao, missing) | `step8`, `step9`, `step11`, `step12` |

### ⚠️ Órfãos — gerados por código ad-hoc NÃO versionado (para as apresentações)
Estes CSVs foram commitados, mas **não há código na pipeline que os reproduza**. Antes de
reusá-los, confirmar a metodologia (ou regenerar com código versionado):

- `auditoria_analfabetismo_municipio.csv`, `auditoria_analfabetismo_v00900_bins.csv`
- `cobertura_por_municipio.csv`, `cobertura_por_regiao.csv`, `cobertura_total.csv`
- `morfologia_v00048_v00058_por_regiao.csv`
- `saneamento_categorias_por_regiao.csv`
- `situacao_urbano_rural_por_municipio.csv`, `_por_regiao.csv`, `_total.csv`
  (derivados da coluna `SITUACAO` do arquivo básico do IBGE — urbano/rural por setor)
- `resp_feminino_contagem_por_municipio.csv`, `resp_feminino_contagem_por_regiao.csv`

> **Pendência de organização:** mover o código gerador destes arquivos para o NB02 (ou um
> script versionado em `scripts/`) para que toda a pasta `eda/` seja reproduzível.
