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
| `agua_canalizada_{global,por_regiao,por_municipio}.csv` | `agua-canal` *(7h)* |
| `figuras/*.png` (histogramas, boxplots, matriz_correlacao, missing) | `step8`, `step9`, `step11`, `step12` |

### ✅ Gerados por [`scripts/gerar_tabelas_auditoria.py`](../../scripts/gerar_tabelas_auditoria.py)
Tabelas de auditoria e de apresentação. **Não saem do Notebook 02**: usam o recorte
`Dados_sig = OK` **com os rurais** (106.281 setores), que é o que valia quando os slides
foram montados — o NB02, da seção 3b em diante, trabalha com os 104.108 urbanos.

```bash
./.venv/bin/python scripts/gerar_tabelas_auditoria.py
```

| Arquivo | O que mede |
|---|---|
| `cobertura_{total,por_regiao,por_municipio}.csv` | Setores com cobertura **integral** (indicador de inadequação = 0) de água, esgoto e lixo; os 3 juntos; setores com os 7 indicadores calculáveis; e coleta de lixo contando a caçamba (V00398) como recolhida |
| `saneamento_categorias_por_regiao.csv` | Distribuição dos setores em 0% · 1–49% · 50%+ de inadequação, por serviço e região |
| `morfologia_v00048_v00058_por_regiao.csv` | Tipo de espécie do domicílio (V00048–V00058) — conta **domicílios**, sobre V00001 + V00002 |
| `auditoria_analfabetismo_{municipio,v00900_bins}.csv` | Peso do sigilo em V00901, por município e por porte do setor |
| `resp_feminino_contagem_{por_regiao,por_municipio}.csv` | Responsáveis por sexo em **pessoas** (V01062/V01063) — não é a média das proporções por setor do NB02 |

> **Órfãos resolvidos em 20/08/2026.** Estes 9 arquivos vinham de código ad-hoc nunca
> versionado. O script acima os reproduz **valor a valor** contra o que estava commitado
> (conferido célula a célula). Única mudança: em `auditoria_analfabetismo_municipio.csv`
> os 11 municípios empatados em sigilo agora desempatam por nome — antes a ordem vinha do
> quicksort do pandas, que é instável, e mudava a cada execução sem mudar nenhum número.
>
> **Resolvidos em 09/08/2026:** os três `situacao_urbano_rural_*` — agora saem da célula
> `filtro-urbano` do NB02, com o mesmo esquema de colunas de antes.

### ✅ Gerados por [`scripts/auditoria_renda.py`](../../scripts/auditoria_renda.py)

A auditoria da renda de 02/09/2026, que produziu o critério de outlier e a coluna
`renda_media_sem_extremo`. A regra que estas tabelas descrevem vive em
[`src/ivs_censo/renda.py`](../../src/ivs_censo/renda.py), e o script a importa de lá —
o texto nunca descreve uma versão diferente da que roda.

| Arquivo | O que traz |
|---|---|
| `renda_outliers_rastreados.csv` | uma linha por setor avaliado, com a classe e os motivos |
| `renda_classes_resumo.csv` | quantos setores em cada classe (NORMAL, SUSPEITO, EXTREMO) |
| `renda_criterio_global_vs_municipal.csv` | o corte de Tukey por município contra o global |
| `renda_setores_pequenos.csv` | os municípios abaixo do piso mínimo de setores |
| `renda_extremos_por_regiao.csv` | onde os extremos se concentram |
| `renda_eda_com_vs_sem.csv` | as descritivas com e sem os suspeitos |
| `renda_correlacao_com_vs_sem.csv` | o efeito nas correlações |
| `renda_normalizacao_impacto.csv` | o efeito na normalização |

> **Registrados em 17/09/2026.** Estas oito tabelas estavam em `eda/` desde 02/09 sem
> entrada neste README — a auditoria integral as classificou como sem procedência
> declarada. O código que as gera sempre existiu; o que faltava era o registro.

## Outras pastas de saída

- **[`eda/fatorial/`](fatorial/)** — as 37 tabelas da análise fatorial, de duas gerações:
  o diagnóstico de 24/08 (`scripts/diagnostico_fatorial.py`) e o Notebook 04 de 17/09
  (prefixo `nb04_`). Índice próprio em [`fatorial/README.md`](fatorial/README.md).
- **[`eda/atualizada/`](atualizada/)** — as 16 tabelas da 2ª rodada da EDA, recalculadas
  com `renda_media_sem_extremo` (`scripts/eda_atualizada.py`). **Atenção:** os arquivos
  têm os mesmos nomes dos daqui e as linhas continuam rotuladas como `renda_media` — a
  única marca é o nome da pasta. Índice e a armadilha explicada em
  [`atualizada/README.md`](atualizada/README.md).
- **`banco_de_dados/nacional/`** — resultados do Brasil inteiro
  (`scripts/proporcoes_brasil.py`): proporções por recorte, região, UF e município, o
  comparativo Brasil × 70 municípios ELSI e a tabela de representatividade da amostra.
- **`banco_de_dados/entrega_orientadora/`** — pacote de entrega (CSV + SQLite + dicionário
  de variáveis), gerado por `scripts/gerar_entrega_orientadora.py`.
