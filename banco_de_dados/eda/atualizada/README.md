# `eda/atualizada/` — a 2ª rodada da EDA, com a renda sem o valor extremo

**Gerados por:** `scripts/eda_atualizada.py` · **Reexecutável:** `./.venv/bin/python scripts/eda_atualizada.py`

Dezesseis CSVs e cinco figuras. São as tabelas da EDA recalculadas trocando
`renda_media` por **`renda_media_sem_extremo`** — a renda sem o setor
`310620005650366`, de Belo Horizonte, que tinha R$ 170.418,06 de renda média por
responsável e é provável erro de dado.

## A armadilha desta pasta, e ela é real

**Os arquivos têm os mesmos nomes dos da pasta raiz, e as linhas continuam rotuladas
como `renda_media`.** A única marca de que são a 2ª rodada é o nome da pasta.

Exemplo concreto: em `descritivas_globais.csv`, a linha `renda_media` vale
**4.187,4094** em `eda/` e **4.185,8124** aqui. Mesma etiqueta, colunas diferentes.

> Ao citar um número desta pasta, **diga sempre que é da 2ª rodada.** Ao comparar com
> a pasta raiz, confira antes se as duas tabelas medem a mesma coluna de renda.

## O que há aqui

| Arquivo | O par na pasta raiz |
|---|---|
| `comparacao_antes_depois.csv` | **não tem par** — é exclusivo daqui, e é o que resume o efeito da troca |
| `descritivas_globais.csv` · `descritivas_por_regiao.csv` | os mesmos nomes em `eda/` |
| `correlacao_pearson.csv` · `correlacao_spearman.csv` | idem |
| `outliers.csv` · `missing_por_municipio.csv` | idem |
| `favelas_fcu_comparativo_indicadores.csv` | idem |
| `renda_*.csv` (8 arquivos) | os mesmos nomes em `eda/`, recalculados |

O script imprime, a cada execução, quais tabelas mudaram e quais ficaram idênticas —
na última execução, `correlacao_spearman` foi a única inalterada.

## O que consome estes arquivos

`scripts/eda_central_dados.py --atualizada` e, por meio dele, o deck
`EDA_Central_IVS_2026-09_rev2.pptx`. A análise fatorial **não** usa esta pasta: ela roda
sobre `renda_media`, e o efeito da troca está medido no bloco 8b do Notebook 04 —
278 setores de 87.544 mudam de faixa.

Formato: separador `;`, codificação `utf-8-sig`.
