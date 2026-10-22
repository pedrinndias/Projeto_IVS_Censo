# `scripts/` — os executáveis versionados

Trinta e um scripts. A pipeline de análise **são os notebooks**; estes existem para o que
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
| [`gerar_deck_cronologia.js`](gerar_deck_cronologia.js) | `complementos/Cronologia_Projeto_IVS_2026-10.pptx` — a cronologia do projeto, do `git log` e dos CSVs | `pptxgenjs`, `git` |
| [`gerar_deck_demandas_setembro.js`](gerar_deck_demandas_setembro.js) | `complementos/Demandas_Setembro_IVS_2026-10.pptx` — as demandas de setembro, números só de CSV | `pptxgenjs` |
| [`juntar_decks.py`](juntar_decks.py) | funde os slides de um `.pptx` anexo ao fim de um `.pptx` base, sem regerar nenhum dos dois, e conserta a estrutura (masters/layouts) do resultado | — |

> `deck_comum.js` é usado pelo gerador da fatorial, pelos três de slides anexados e pelos
> dois decks de outubro (cronologia e demandas de setembro). Os dois mais antigos carregam
> cada um a sua cópia dos mesmos helpers — migrá-los exige regerar os dois decks e
> conferir contra o que já foi apresentado, e é trabalho à parte. Dívida registrada.

## Documentos

| Script | O que gera | Requer |
|---|---|---|
| [`gerar_pdf_guia_fatorial.py`](gerar_pdf_guia_fatorial.py) | o guia dos slides marcados, com o vocabulário do zero | `reportlab` |
| [`gerar_pdf_plano_emergencia.py`](gerar_pdf_plano_emergencia.py) | o livro condensado, o roteiro da fala e as perguntas prováveis | `reportlab` |
| [`gerar_pdf_outliers_renda.py`](gerar_pdf_outliers_renda.py) | o critério de outlier de renda por extenso | `reportlab` |
| [`gerar_pdf_guia_decks_outubro.py`](gerar_pdf_guia_decks_outubro.py) | `complementos/Guia_Apoio_Cronologia_e_Demandas.pdf` — os dois decks de outubro explicados slide a slide, com as miniaturas; os textos ficam em `guia_outubro_base.py`, `guia_outubro_cronologia.py` e `guia_outubro_demandas.py`, que não geram nada sozinhos | `reportlab`, `pypdf`, LibreOffice |
| [`gerar_resumo_eda_central.py`](gerar_resumo_eda_central.py) | o resumo da EDA em Word | `python-docx` |
| [`atualizar_roteiro_2a_rodada.py`](atualizar_roteiro_2a_rodada.py) | migra o roteiro da 1ª para a 2ª rodada | `python-docx` |
| [`gerar_relatorio_ivs_final.py`](gerar_relatorio_ivs_final.py) | `docs/relatorios/Relatorio_IVS_Final_NB05.md` | — |
| [`gerar_notebook_ivs_final.py`](gerar_notebook_ivs_final.py) | `notebooks/Fase3_EDA_ELSI/05_Calculo_IVS_Final.ipynb`, por `nbformat`/`nbclient` | — |
| [`inventario_apresentacao.py`](inventario_apresentacao.py) | o mapa dos artefatos de apresentação (ATUAL/SUPERADO/HISTÓRICO) | `python-pptx`, `pandas` |
| [`gerar_catalogo_analises.py`](gerar_catalogo_analises.py) | `docs/relatorios/Catalogo_Analises_Exploratorias.xlsx` — cada tabela, figura, deck e relatório já produzido, com situação, tema e onde aparece cada indicador | `pandas`, `openpyxl`, `git` |
| [`dados_relatorio_descritivo.py`](dados_relatorio_descritivo.py) | `relatorio_descritivo/dados/` (`numeros.json`, `manifesto.csv`), `relatorio_descritivo/figuras/` e `Relatorio_Descritivo_numeros.xlsx` — os números e textos do relatório descritivo, lidos das tabelas da `00_referencia` e do registro das demandas | `pandas`, `matplotlib`, `openpyxl` |
| [`pecas_relatorio_raic.py`](pecas_relatorio_raic.py) | `relatorio_parcial_raic/figuras/fig1_correlacao.png` e `relatorio_parcial_raic/dados/` (`tabela1_descritivas.csv`, `quadro2_indicadores.csv`, `matriz_spearman.csv`, `pecas.json`) — Figura 1, Tabela 1 e Quadro 2 do relatório parcial RAIC 2026, com os 12 indicadores da matriz; três travas (reproduz a S6, confere a T03 contra o `.db` e a tabela aprovada, confere a contagem do quadro) | `pandas`, `matplotlib` |
| [`gerar_relatorio_descritivo.js`](gerar_relatorio_descritivo.js) | `relatorio_descritivo/Relatorio_Descritivo_IVS_2026-10.pptx` — o deck inteiro, do zero, a partir do `numeros.json` | `pptxgenjs`, `deck_comum.js` |
| [`verificar_relatorio_descritivo.py`](verificar_relatorio_descritivo.py) | Conferência do relatório descritivo (IDs, números contra as tabelas e o registro, recálculo direto do `.db`, origem dos indicadores) | `pandas` |
| [`comparar_edicoes_relatorio.py`](comparar_edicoes_relatorio.py) | `relatorio_descritivo/dados/edicoes_do_pedro.csv` — as células de tabela mudadas à mão numa cópia do deck, por ID de slide | `pandas` |
| [`versoes_fatorial.py`](versoes_fatorial.py) | `banco_de_dados/eda/versoes_fatorial/` — as 108 versões da fatorial (renda × lixo × água canalizada × banheiro × moradia) com o método da referência proposta, estabilidade e pares por eixo; trava contra as 18 do NB05 | `pandas`, `numpy`, motor do NB05 |
| [`dados_versoes_fatorial.py`](dados_versoes_fatorial.py) | `versoes_fatorial/dados/`, `figuras/` e `Versoes_Fatorial_numeros.xlsx` — números e textos dos dois decks das 108 versões | `pandas`, `matplotlib`, `openpyxl` |
| [`gerar_versoes_fatorial.js`](gerar_versoes_fatorial.js) | `versoes_fatorial/Versoes_Fatorial_Principal.pptx` e `Caderno_Fichas_108.pptx`, com trava contra sobrescrita | `pptxgenjs`, `deck_comum.js` |
| [`verificar_versoes_fatorial.py`](verificar_versoes_fatorial.py) | Conferência das 108 versões e dos dois decks (enumerador, trava, recálculo pelo `.db`, fichas contra os CSVs) | `pandas` |
| [`revisar_texto_relatorio.py`](revisar_texto_relatorio.py) | v2 do relatório descritivo: correções de texto e de voz sem mudar número (C-06) | `python-pptx` |
| [`preparar_entrega_relatorio.py`](preparar_entrega_relatorio.py) | v3 do relatório descritivo e PDF: notas guardadas e esvaziadas, metadados, texto alternativo, DS23 e DS16 (C-07, C-08) | `python-pptx`, `pypdf`, LibreOffice |
| [`dados_apoio_relatorio.py`](dados_apoio_relatorio.py) | Conteúdo da v4 (apoio da reunião): perguntas, respostas, de onde vem e glossário → `relatorio_descritivo/apoio/apoio.json` | `python-pptx` |
| [`montar_apoio_relatorio.py`](montar_apoio_relatorio.py) | Monta a v4: um slide de apoio depois de cada slide da v3, P00 e glossário; PDF | `python-pptx`, `pypdf`, LibreOffice |
| [`verificar_apoio_relatorio.py`](verificar_apoio_relatorio.py) | Conferência da v4: originais intactos, um apoio por slide, números com origem, glossário | `python-pptx` |
| [`comparar_edicoes_versoes.py`](comparar_edicoes_versoes.py) | `versoes_fatorial/dados/edicoes_do_pedro_<deck>.csv` — células mudadas à mão nos decks das 108 versões, por ID | `pandas` |
| [`anexar_versoes_ao_relatorio.py`](anexar_versoes_ao_relatorio.py) | `relatorio_descritivo/Relatorio_Descritivo_IVS_2026-10_com_108_versoes.pptx` — o relatório descritivo editado pelo Pedro com a parte 5 (as 108 versões) copiada para dentro, sem regerar; renumera o pé | `python-pptx` (via `uv run --with`) |
| [`inserir_no_relatorio.py`](inserir_no_relatorio.py) | Copia slides novos do relatório (lista em `relatorio_descritivo/dados/insercoes_<rodada>.json`) para dentro do deck editado pelo Pedro, sem regerar; grava arquivo novo e renumera o pé | `python-pptx` (via `uv run --with`) |

## Fatorial multiversão (out/2026)

Prompt e estado em `docs/prompts/*fatorial_multiversao_2026-10.md`. Ordem: motor (camadas 1 → 2 → 3) → números → decks → verificador.

| Script | O que gera |
|---|---|
| [`fatorial_multiversao.py`](fatorial_multiversao.py) `--camada 1\|2\|3` | `banco_de_dados/eda/fatorial_multiversao/` — as 4.017 combinações (~22 min), as 999 especificações (~5 min), os finalistas e o IVS proposto (~1 min) |
| [`dados_apresentacoes_multiversao.py`](dados_apresentacoes_multiversao.py) | `apresentacoes_multiversao/dados/*.json`, `figuras/` e `Fatorial_Multiversao_numeros.xlsx` |
| [`gerar_decks_multiversao.js`](gerar_decks_multiversao.js) `<COD\|todos\|FIN>` | os 12 decks de indicador (`fichas/`) e o deck final, com trava contra sobrescrita |
| [`verificar_multiversao.py`](verificar_multiversao.py) `--fase N` | conferência de cada fase (1 a 7) |

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
