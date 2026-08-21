# Apresentações — Projeto IVS Censo 2022

**A apresentação atual é a que está na raiz desta pasta.** Tudo que estiver em `historico/`
já foi apresentado e ficou para trás — não use como fonte de número.

```
Apresentacoes_IVS/
├── EDA_Central_IVS_2026-08.pptx          ← use esta
├── Roteiro_EDA_Central_IVS_2026-08.docx  ← como apresentar, slide a slide
├── historico/                            ← 10 decks anteriores, em ordem cronológica
└── dicionarios/                          ← planilhas de variáveis (não são apresentações)
```

---

## A apresentação atual

| | |
|---|---|
| **Arquivo** | `EDA_Central_IVS_2026-08.pptx` — 47 slides |
| **Roteiro** | `Roteiro_EDA_Central_IVS_2026-08.docx` — fala sugerida, o que apontar em cada figura e as perguntas prováveis |
| **Recorte** | 104.108 setores urbanos elegíveis, 70 municípios do ELSI-Brasil |
| **Gerada por** | `scripts/gerar_deck_eda_central.js` |
| **Números** | extraídos por `scripts/eda_central_dados.py` das tabelas de `banco_de_dados/eda/` |

**Ela é gerada por script, não editada à mão.** Para atualizar depois de reexecutar a EDA:

```bash
./.venv/bin/python scripts/eda_central_dados.py banco_de_dados/eda/dados_deck.json
node scripts/gerar_deck_eda_central.js docs/Apresentacoes_IVS/EDA_Central_IVS_2026-08.pptx
```

Se editar o `.pptx` à mão, a próxima execução do script sobrescreve a edição. Mudanças
permanentes vão no gerador.

> Por que gerada por script: as apresentações anteriores eram montadas à mão, e a lista do
> que entrava vivia na cabeça de quem montava. Foi assim que o bloco de chefia feminina,
> presente no deck de junho, sumiu do de agosto sem ninguém notar.

---

## Histórico

Do mais recente para o mais antigo. O prefixo é a data do arquivo.

| Arquivo | Slides | O que era | Por que saiu de circulação |
|---|---|---|---|
| `2026-08-09_Andamento_rev2.pptx` | 30 | Andamento de agosto, revisão 2 — a última antes desta | Não cobria chefia feminina, habitação precária, banheiro nem morfologia |
| `2026-08-09_Andamento.pptx` | 29 | Mesma apresentação, revisão 1 | Superada pela rev2 no mesmo dia |
| `2026-08-09_Retomada_e_demandas.pptx` | 25 | Retomada do projeto e as demandas em aberto | Absorvida pelo Andamento |
| `2026-06-18_EDA_Fase3_seis_demandas.pptx` | 29 | EDA da Fase 3 + as **seis demandas de junho** | **Único deck que teve chefia feminina, habitação precária e morfologia** — recuperados na EDA Central |
| `2026-06-15_EDA_Fase3_revisada_V00001.pptx` | 22 | EDA revisada sobre o denominador V00001 | Superada pela versão com demandas, três dias depois |
| `2026-05-30_EDA_completa_corrigida.pptx` | 11 | EDA completa após as correções de maio | Superada pela revisão de junho |
| `2026-05-30_Comparativo_EDA_antiga_vs_nova.pptx` | 16 | Comparativo entre a EDA antiga e a corrigida | Documento de transição; a EDA antiga não existe mais |
| `2026-05-28_Correcoes_commit_2fb2e30.pptx` | 10 | Duas correções metodológicas de um commit específico | Correções já incorporadas |
| `2026-05-22_Revisao_denominador_analfabetismo.pptx` | 13 | A correção do denominador do analfabetismo | Correção já incorporada (`V00901 / (V00900 + V00901)`) |
| `2026-05-15_EDA_inicial_denominador_V01042.pptx` | 32 | A **primeira** EDA, sobre o denominador V01042 | **Metodologia abandonada.** V01042 é contagem de pessoas, não de domicílios — os números deste deck não valem |

### Cuidado ao consultar o histórico

Três coisas mudaram ao longo do caminho e tornam os números antigos incomparáveis:

1. **O denominador domiciliar** era `V01042` (pessoas) e passou a ser `V00001` (domicílios),
   em 22/05/2026. Tudo anterior a essa data está sobre a base errada.
2. **O recorte** passou a excluir setores rurais em 09/08/2026: de 106.281 para 104.108
   setores. Números de antes e de depois não se comparam linha a linha.
3. **O índice de envelhecimento** usava só a faixa de 0 a 4 anos no denominador e dava 299;
   corrigido para menores de 15 anos, dá 92,7.

---

## Dicionários

Não são apresentações — são planilhas de apoio que estavam misturadas aqui.

| Arquivo | O que é |
|---|---|
| `Dicionario_IBGE_Oficial_Variaveis_do_Projeto.xlsx` | Recorte do dicionário oficial do IBGE com as variáveis que o projeto usa. É a fonte que resolveu a dúvida do bloco de esgoto (V00312–V00316 × V00249–V00253) |
| `Dicionario_Variaveis_IVS_Censo2022.xlsx` | Dicionário do projeto, versão de junho de 2026 |

> O dicionário **corrente** do projeto não está aqui: é gerado por
> `scripts/gerar_tabela_variaveis.py` e sai em `banco_de_dados/entrega_orientadora/`.
> Os dois arquivos acima são versões congeladas.

---

## De onde vieram os nomes antigos

Mapeamento completo, para o caso de encontrar uma referência ao nome antigo em algum documento:

| Nome antigo | Nome atual |
|---|---|
| `1_APRESENTAR_Comparativo_EDA_antiga_vs_nova.pptx` | `historico/2026-05-30_Comparativo_EDA_antiga_vs_nova.pptx` |
| `2_EDA_Completa_Corrigida.pptx` | `historico/2026-05-30_EDA_completa_corrigida.pptx` |
| `EDA_Fase3_Completa_Revisada_V00001.pptx` | `historico/2026-06-15_EDA_Fase3_revisada_V00001.pptx` |
| `EDA_Fase3_Completa_Demandas.pptx` | `historico/2026-06-18_EDA_Fase3_seis_demandas.pptx` |
| `IVS_Retomada_e_Demandas_2026-08.pptx` | `historico/2026-08-09_Retomada_e_demandas.pptx` |
| `IVS_Andamento_2026-08.pptx` | `historico/2026-08-09_Andamento.pptx` |
| `IVS_Andamento_2026-08_rev2.pptx` | `historico/2026-08-09_Andamento_rev2.pptx` |
| `Versoes_anteriores/EDA_antiga_15-05_V01042.pptx` | `historico/2026-05-15_EDA_inicial_denominador_V01042.pptx` |
| `Versoes_anteriores/Revisao_Denominador_Analfabetismo_22-05.pptx` | `historico/2026-05-22_Revisao_denominador_analfabetismo.pptx` |
| `Versoes_anteriores/Correcoes_commit_2fb2e30.pptx` | `historico/2026-05-28_Correcoes_commit_2fb2e30.pptx` |

A pasta `Versoes_anteriores/` deixou de existir: ela separava três decks antigos enquanto
outros sete, igualmente antigos, ficavam na raiz. Agora todo deck fora de circulação está
em `historico/`.

---

## Onde guardar a próxima apresentação

1. A atual sai da raiz e vai para `historico/`, com o prefixo `AAAA-MM-DD_`.
2. A nova entra na raiz.
3. Acrescente a linha correspondente na tabela do histórico acima, dizendo **por que** ela
   saiu de circulação — é essa coluna que evita que alguém use número velho sem saber.
