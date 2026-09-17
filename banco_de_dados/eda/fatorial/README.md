# `eda/fatorial/` — saídas da análise fatorial

Trinta e sete CSVs e cinco figuras, de **duas gerações diferentes**. Saber qual é qual
importa: elas respondem a perguntas diferentes e foram feitas em momentos diferentes.

## Geração 1 — o diagnóstico (24/08/2026)

**Gerados por:** `scripts/diagnostico_fatorial.py` · **Reexecutável:** `python scripts/diagnostico_fatorial.py`

Dezenove arquivos. Seis cenários, cada um com três tabelas (`_correlacao`,
`_autovalores`, `_cargas`), mais o `resumo_adequabilidade.csv` que traz uma linha por
cenário e é **a referência de conferência de todo o resto**.

| Prefixo do cenário | O que varia |
|---|---|
| `ivs7_spearman` | os 7 componentes, correlação de Spearman — **o cenário de referência** |
| `ivs7_pearson` | os mesmos 7, com Pearson, como análise de sensibilidade |
| `ivs6_sem_lixo_spearman` | sem o indicador de lixo — a solução recomendada |
| `ivs6_sem_analfab_spearman` | sem o analfabetismo, para medir o efeito do sigilo |
| `ivs7_minmax_municipal_spearman` | os 7, sobre os dados normalizados por município |
| `ivs6_sem_lixo_minmax_municipal_spearman` | idem, sem o lixo |

## Geração 2 — o Notebook 04 (17/09/2026)

**Gerados por:** `notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb` · Todos com prefixo `nb04_`

| Arquivo | O que traz | Bloco do NB04 |
|---|---|---|
| `nb04_adequabilidade.csv` | MSA e SMC por variável, nos dois cenários | 2 |
| `nb04_correlacao_ivs7_spearman.csv` | a matriz-R das sete variáveis | 2 |
| `nb04_autovalores.csv` | autovalores, Kaiser, Horn e variância acumulada | 3 |
| `nb04_extracao_comparada.csv` | ACP contra fatoração do eixo principal | 4 |
| `nb04_cargas_ivs6_sem_lixo.csv` · `nb04_cargas_ivs7.csv` | cargas Varimax, padrão e estrutura, com a variância residual | 5 |
| `nb04_phi_ivs6_sem_lixo.csv` | a correlação entre os fatores — só existe na solução oblíqua | 5 |
| `nb04_bootstrap_cargas.csv` | IC 95% de cada carga, em mil reamostragens | 6 |
| `nb04_pesos.csv` · `nb04_sintese_pesos.csv` | **os pesos do IVS** | 7 e 10 |
| `nb04_escores.csv` | uma linha por setor: índice 0–1 e escores fatoriais | 7 |
| `nb04_cenarios.csv` · `nb04_contingencia_*.csv` | quantos setores mudam de faixa em cada cenário | 8 |
| `nb04_renda_sem_extremo*.csv` | o efeito de trocar a coluna de renda | 8b |
| `nb04_validacao_fcu.csv` | AUC e medianas contra os setores de favela | 9 |

**Figuras** em `figuras/`, 150 dpi: `nb04_matriz_correlacao`, `nb04_scree_horn`,
`nb04_mapa_cargas`, `nb04_plano_fatorial` e `nb04_roc_fcu`.

## Como conferir que está tudo coerente

`tests/test_fatorial.py` reproduz `ivs7_spearman_cargas.csv` a partir do banco da
entrega, com tolerância de 1e-6. Se esse teste passa, as duas gerações concordam.

Formato de todos: separador `;`, codificação `utf-8-sig`, decimal com ponto.
