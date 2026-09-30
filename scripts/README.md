# `scripts/` — os executáveis versionados

Trinta scripts. A pipeline de análise **são os notebooks**; estes existem para o que
precisa rodar fora deles — o Brasil inteiro, o pacote de entrega, os decks e os
documentos.

> **A regra que vale para todos:** número que aparece num deck ou num documento sai de
> um arquivo gerado, nunca digitado no gerador. O projeto já apresentou três números do
> recorte errado por tê-los digitado à mão; desde então os geradores só formatam.

## Dados e pipeline

| Script | O que gera | Reexecutável? |
|---|---|---|
| [`proporcoes_brasil.py`](proporcoes_brasil.py) | `banco_de_dados/nacional/` — os indicadores para os ~468 mil setores do Brasil | sim · ~6,7 min |
| [`gerar_entrega_orientadora.py`](gerar_entrega_orientadora.py) | o pacote de entrega: CSV + SQLite, 108 colunas, 3 tabelas | sim · ~2 min |
| [`gerar_tabela_variaveis.py`](gerar_tabela_variaveis.py) | `Dicionario_Variaveis_Projeto.{csv,xlsx}` | sim |
| [`gerar_quadro_indicadores.py`](gerar_quadro_indicadores.py) | `Quadro_Indicadores.{csv,xlsx,md}` | sim |
| [`gerar_tabelas_auditoria.py`](gerar_tabelas_auditoria.py) | as 9 tabelas que eram "CSVs órfãos" até 20/08/2026 | sim |
| [`auditoria_renda.py`](auditoria_renda.py) | as 8 tabelas `renda_*` e o critério de outlier | sim |
| [`eda_atualizada.py`](eda_atualizada.py) | `eda/atualizada/` — a EDA recalculada com a renda sem o extremo | sim |
| [`eda_extremo_belo_horizonte.py`](eda_extremo_belo_horizonte.py) | `eda/atualizada/extremo_bh_*` — o mesmo extremo olhado de dentro de Belo Horizonte, e o efeito dele na normalização municipal | sim · ~3 s |
| [`diagnostico_fatorial.py`](diagnostico_fatorial.py) | `eda/fatorial/` — os seis cenários da adequabilidade | sim · ~3 s |
| [`fatorial_ampliada.py`](fatorial_ampliada.py) | `eda/fatorial_ampliada/` — a grade de cenários da fatorial ampliada, sem bootstrap (demandas 3, 5–11) | sim · ~30 s |
| [`dados_criterio_renda.py`](dados_criterio_renda.py) | o JSON que alimenta o deck do critério de renda | sim |
| [`eda_central_dados.py`](eda_central_dados.py) | o JSON que alimenta o deck e o resumo da EDA Central | sim |
| [`ivs_especificacoes.py`](ivs_especificacoes.py) | `banco_de_dados/eda/ivs_especificacoes/` — as 324 especificações do IVS final (Fase C) | sim · ~3 min |

## Apresentações

| Script | O que gera | Requer |
|---|---|---|
| [`deck_comum.js`](deck_comum.js) | **não gera nada** — é o módulo com os elementos visuais (régua, título, seção, tabela booktabs, número, código comentado) | — |
| [`gerar_deck_fatorial.js`](gerar_deck_fatorial.js) | o deck da análise fatorial | `pptxgenjs` |
| [`gerar_deck_eda_central.js`](gerar_deck_eda_central.js) | o deck da EDA Central, 1ª e 2ª rodadas | `pptxgenjs` |
| [`gerar_deck_criterio_renda.js`](gerar_deck_criterio_renda.js) | o deck do critério de outliers de renda | `pptxgenjs` |
| [`gerar_slides_extremo_bh.js`](gerar_slides_extremo_bh.js) | os 4 slides do extremo de BH, que são **anexados** ao deck da fatorial, não regeram ele | `pptxgenjs` |
| [`gerar_slides_fatorial_ampliada.js`](gerar_slides_fatorial_ampliada.js) | os slides da fatorial ampliada, **anexados** ao deck da fatorial por `juntar_decks.py` | `pptxgenjs` |
| [`gerar_slides_ivs_final.js`](gerar_slides_ivs_final.js) | os 8 slides do NB05 (especificação de referência do IVS final), **anexados** ao mesmo deck | `pptxgenjs` |
| [`juntar_decks.py`](juntar_decks.py) | funde os slides de um `.pptx` anexo ao fim de um `.pptx` base, sem regerar nenhum dos dois, e conserta a estrutura (masters/layouts) do resultado | — |

> `deck_comum.js` é usado **só** pelo gerador da fatorial. Os dois mais antigos carregam
> cada um a sua cópia dos mesmos helpers — migrá-los exige regerar os dois decks e
> conferir contra o que já foi apresentado, e é trabalho à parte. Dívida registrada.

## Documentos

| Script | O que gera | Requer |
|---|---|---|
| [`gerar_pdf_guia_fatorial.py`](gerar_pdf_guia_fatorial.py) | o guia dos slides marcados, com o vocabulário do zero | `reportlab` |
| [`gerar_pdf_plano_emergencia.py`](gerar_pdf_plano_emergencia.py) | o livro condensado, o roteiro da fala e as perguntas prováveis | `reportlab` |
| [`gerar_pdf_outliers_renda.py`](gerar_pdf_outliers_renda.py) | o critério de outlier de renda por extenso | `reportlab` |
| [`gerar_resumo_eda_central.py`](gerar_resumo_eda_central.py) | o resumo da EDA em Word | `python-docx` |
| [`atualizar_roteiro_2a_rodada.py`](atualizar_roteiro_2a_rodada.py) | migra o roteiro da 1ª para a 2ª rodada | `python-docx` |
| [`gerar_relatorio_ivs_final.py`](gerar_relatorio_ivs_final.py) | `docs/relatorios/Relatorio_IVS_Final_NB05.md` | — |
| [`gerar_notebook_ivs_final.py`](gerar_notebook_ivs_final.py) | `notebooks/Fase3_EDA_ELSI/05_Calculo_IVS_Final.ipynb`, por `nbformat`/`nbclient` | — |
| [`inventario_apresentacao.py`](inventario_apresentacao.py) | o mapa dos artefatos de apresentação (ATUAL/SUPERADO/HISTÓRICO) | `python-pptx`, `pandas` |

## Duas coisas que é preciso saber antes de rodar

**Cinco scripts exigem dependências que não estão no `requirements.txt`.** `reportlab` e
`python-docx` não estão declarados nem instalados no `.venv`; `pptxgenjs` está, mas no
`package.json`. Os cinco rodam assim:

```bash
uv run --with reportlab --with pandas python scripts/gerar_pdf_guia_fatorial.py <saida.pdf>
uv run --with python-docx python scripts/gerar_resumo_eda_central.py <saida.docx>
node scripts/gerar_deck_fatorial.js <saida.pptx>
```

A versão vem resolvida na hora, não fixada. Declará-las é dívida em aberto.

**`atualizar_roteiro_2a_rodada.py` NÃO é reexecutável.** É migração de mão única da 1ª
para a 2ª rodada do roteiro, que é o único artefato escrito à mão da pasta de
apresentações. Rodá-lo de novo corromperia o texto do autor. Ele fica versionado como
registro do que foi preciso mexer, caso haja uma 3ª rodada.

## Como conferir que um script continua honesto

Rode e confira se a árvore mudou:

```bash
./.venv/bin/python scripts/<script>.py && git status --porcelain
```

Arquivo que muda sem o código ter mudado é achado. As duas exceções conhecidas são o
`.xlsx` do dicionário e os `.db` da entrega, que carregam a data de geração dentro de
si — o conteúdo deles é idêntico, mas os bytes nunca são.
