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

## Os quatro arquivos `extremo_bh_*`, que têm outro dono

**Gerados por:** `scripts/eda_extremo_belo_horizonte.py` — **não** por `eda_atualizada.py`.
Moram aqui porque tratam do mesmo setor, mas são uma análise posterior e de outro recorte.

A 2ª rodada mediu o efeito do extremo no **agregado dos 70 municípios**, onde ele é quase
nulo (a média cai 0,04%). Estes quatro medem o efeito **dentro de Belo Horizonte**, que é
onde o setor está — e lá ele derruba o desvio-padrão em 14,34% e o máximo em 73,37%.

| Arquivo | O que traz |
|---|---|
| `extremo_bh_descritivas.csv` | as cinco medidas com e sem o setor, nos dois recortes, e a variação percentual |
| `extremo_bh_normalizacao.csv` | o achado: a escala min-max **municipal** com e sem o extremo, e quantos setores de BH ficam comprimidos contra o zero |
| `extremo_bh_ranking.csv` | o ranking dos 70 municípios por renda média, com e sem — nenhum troca de posição |
| `figuras/extremo_bh.png` | a renda de BH e a escala normalizada, lado a lado |

O número que importa está no segundo: sob a normalização municipal, **1.909 setores de
Belo Horizonte** saem de baixo de 0,05 na escala quando o extremo é retirado. O agregado
era robusto; o intramunicipal não era.

Os slides correspondentes saem de `scripts/gerar_slides_extremo_bh.js` e estão anexados
ao fim de `Analise_Fatorial_NB04_2026-09.pptx`.

Formato: separador `;`, codificação `utf-8-sig`.
