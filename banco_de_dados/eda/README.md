# Saídas da EDA — `banco_de_dados/eda/`

Tabelas-resumo e figuras da Análise Exploratória da Fase 3. Os CSVs aqui são versionados
como **histórico de execução**; as bases grandes (`Base_*.csv`, `diagnostico_esgoto_*`,
`*_por_setor.csv`) ficam fora do git (ver `.gitignore`).

> **Recorte a partir de 09/08/2026:** as tabelas geradas pelas seções 4 em diante do NB02
> referem-se a **setores urbanos elegíveis** (`Dados_sig = OK` e `SITUACAO = Urbana`),
> 104.108 setores. Antes eram 106.281 (com rurais). As tabelas de composição
> urbano/rural cobrem os 109.032 setores da base completa.

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
| `situacao_urbano_rural_{total,por_regiao,por_municipio}.csv` · `exclusao_rural_conferencia.csv` | `filtro-urbano` *(3b)* |
| `habitacao_precaria_{global,por_regiao,por_municipio}.csv` | `hab-precaria` *(7b)* |
| `inadequacao_banheiro_{global,por_regiao,por_municipio}.csv` | `banheiro-inad` *(7c)* |
| `resp_feminino_{global,por_regiao,por_municipio}.csv` | `resp-fem` *(7d)* |
| `estrutura_etaria_{global,por_regiao,por_municipio,contagem_por_municipio}.csv` · `indicadores_envelhecimento_{total,por_regiao}.csv` | `idade-estrutura` *(7e)* |
| `tipo_domicilio_{global,totais_por_grupo,por_regiao,por_municipio}.csv` · `moradia_predominante_agrupada_por_regiao.csv` | `tipo-domicilio` *(7f)* |
| `favelas_fcu_{total,por_regiao,por_municipio,comparativo_indicadores}.csv` | `favelas-fcu` *(7g)* |
| `figuras/*.png` (histogramas, boxplots, matriz_correlacao, missing) | `step8`, `step9`, `step11`, `step12` |

### ⚠️ Órfãos — gerados por código ad-hoc NÃO versionado (para as apresentações)
Estes CSVs foram commitados, mas **não há código na pipeline que os reproduza**. Antes de
reusá-los, confirmar a metodologia (ou regenerar com código versionado):

- `auditoria_analfabetismo_municipio.csv`, `auditoria_analfabetismo_v00900_bins.csv`
- `cobertura_por_municipio.csv`, `cobertura_por_regiao.csv`, `cobertura_total.csv`
- `morfologia_v00048_v00058_por_regiao.csv`
- `saneamento_categorias_por_regiao.csv`
- `resp_feminino_contagem_por_municipio.csv`, `resp_feminino_contagem_por_regiao.csv`

> **Resolvidos em 09/08/2026:** os três `situacao_urbano_rural_*` deixaram de ser órfãos —
> agora são gerados pela célula `filtro-urbano` do NB02, com o mesmo esquema de colunas de
> antes (setores e domicílios, contagens e percentuais).

## Outras pastas de saída

- **`banco_de_dados/nacional/`** — resultados do Brasil inteiro
  (`scripts/proporcoes_brasil.py`): proporções por recorte, região, UF e município, o
  comparativo Brasil × 70 municípios ELSI e a tabela de representatividade da amostra.
- **`banco_de_dados/entrega_orientadora/`** — pacote de entrega (CSV + SQLite + dicionário
  de variáveis), gerado por `scripts/gerar_entrega_orientadora.py`.
