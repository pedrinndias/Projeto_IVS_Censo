# Cálculo nacional — `banco_de_dados/nacional/`

Saídas de [`scripts/proporcoes_brasil.py`](../../scripts/proporcoes_brasil.py), que aplica
**as mesmas fórmulas da pipeline ELSI** (via `src/ivs_censo`) aos ~468 mil setores
censitários do Brasil inteiro.

> **Isto não é o recorte de análise do projeto.** O IVS continua sendo calculado para os
> setores urbanos dos 70 municípios do ELSI-Brasil. O Brasil entra aqui como **linha de
> base de representatividade**: serve para dizer o quanto a amostra ELSI se parece (ou
> não) com o país, o que a discussão do artigo precisa declarar.

## Como reproduzir

```bash
python scripts/proporcoes_brasil.py
```

Leva cerca de 10 minutos e exige os 8 CSVs do Censo em `dados/` (~2,4 GB). A opção
`--salvar-setores` grava também o resultado por setor (~200 MB, não versionado);
`--limite-chunks N` roda uma amostra parcial, só para teste.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `proporcoes_por_recorte.csv` | Os 26 indicadores em três recortes: **Brasil (todos)**, **Brasil (urbano)** e **ELSI 70 (urbano)** |
| `proporcoes_brasil_por_regiao.csv` | Idem, por região (Brasil urbano) |
| `proporcoes_brasil_por_uf.csv` | Idem, por Unidade da Federação |
| `proporcoes_brasil_por_municipio.csv` | Idem, por município (5.572 municípios × 26 indicadores) |
| `comparativo_brasil_vs_elsi.csv` | **Entregável central**: lado a lado Brasil urbano × ELSI-70 urbano, com a razão entre os dois |
| `representatividade_elsi_no_brasil.csv` | Que fatia do país a amostra ELSI representa (setores, municípios, população, domicílios, favelas) |

## Duas leituras de cada indicador

Cada tabela traz o mesmo indicador resumido de duas maneiras, porque elas respondem a
perguntas diferentes e costumam divergir:

| Coluna | O que é | Quando usar |
|---|---|---|
| `media_entre_setores`, `mediana`, `p25`, `p75` | trata **cada setor como uma observação** | leitura intraurbana — é a que dialoga com as descritivas do Notebook 02 |
| `razao_agregada` | soma dos numeradores ÷ soma dos denominadores | trata o recorte como **um território único** — é o número comparável com estatísticas publicadas pelo IBGE |

A diferença entre as duas não é erro: a média entre setores dá o mesmo peso a um setor de
50 e a um de 5.000 domicílios; a razão agregada pondera pelo tamanho.

## Regras aplicadas (idênticas às do Notebook 02)

- sigilo `X` do IBGE → `NaN`; somas de numerador com `min_count=1` (nunca zero silencioso);
- elegibilidade `Dados_sig` com população zero avaliada antes do sigilo;
- recorte urbano por `SITUACAO = Urbana`;
- denominador domiciliar `V00001`.

> **Precisão:** os valores são calculados em `float64` de propósito. Com `float32` a soma
> da população do país erra por arredondamento acumulado (dá 203.080.736 em vez dos
> 203.080.756 do Censo 2022) — as proporções não mudam, mas os totais deixam de bater com
> o IBGE.
