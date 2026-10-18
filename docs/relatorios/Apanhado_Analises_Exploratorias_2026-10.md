# Apanhado das análises exploratórias — março a outubro de 2026

Tudo o que o projeto já analisou, num lugar só. **Nenhuma análise nova**: este documento
lê o que existe e diz o que cada coisa é, quando foi feita, onde está e se ainda vale.

O companheiro dele é a planilha
[`Catalogo_Analises_Exploratorias.xlsx`](Catalogo_Analises_Exploratorias.xlsx), que
lista **arquivo por arquivo** (tabelas, figuras, decks, notebooks, relatórios) e tem três
colunas em branco para a escolha do que vai para o artigo: *Vai para o artigo?*,
*Seção do artigo* e *Comentários*. Ela é gerada por
`scripts/gerar_catalogo_analises.py` a partir dos próprios arquivos e READMEs.

---

## 1. Em números

| Item | Quantidade |
|---|---:|
| Indicadores e variantes catalogados | 31 |
| Tabelas (CSV/JSON) | 144 |
| — vigentes | 108 |
| — superadas ou históricas | 34 |
| Figuras | 25 |
| Decks | 16 (1 atual, 4 complementos, 11 no histórico) |
| Notebooks e relatórios | 20 (5 notebooks vigentes, 6 relatórios, 9 notebooks das Fases 1 e 2) |

Por tema, as 144 tabelas se dividem assim: índice e análise fatorial 55 · renda 20 ·
saneamento 11 · panorama dos indicadores 10 · moradia e domicílio 9 · envelhecimento e
estrutura etária 7 · chefia feminina 6 · favelas (FCU) 6 · Brasil × ELSI 6 · qualidade dos
dados 6 · urbano e rural 4 · analfabetismo e sigilo 2 · insumos de deck 2.

---

## 2. A linha do tempo

| Quando | Rodada | Recorte | O que trouxe | Onde está | Situação |
|---|---|---|---|---|---|
| mar–mai | Fase 1 (IVS básico) e Fase 2 (IVS multidimensional) | Brasil inteiro | Primeiro cálculo dos indicadores, sem o filtro dos 70 municípios | `Backup/Fase1_*`, `Backup/Fase2_*` | **Superada** — não aplicava o recorte ELSI |
| 15/05 | EDA da Fase 3, primeira versão | 70 municípios | NB01 (extração) e NB02 (EDA), com denominador V01042 | deck `historico/2026-05-15_*` | **Superada** pela troca de denominador |
| 22–30/05 | Revisão do denominador do analfabetismo e correções | idem | Comparativo EDA antiga × nova | 4 decks em `historico/` | Histórico |
| 12–18/06 | EDA revisada (V00001) e as seis demandas | idem, ainda com rurais | Envelhecimento (IEP, RDI), tabela de variáveis, moradias convencionais, apartamento, favelas | `Relatorio_EDA_Fase3_IVS_ELSI.md` (12/06), decks de 15/06 e 18/06 | O relatório `.md` foi atualizado depois e vale; os decks são histórico |
| 09/08 | Retomada | **104.108 setores urbanos** (`Dados_sig = OK`) | Recorte urbano, pacote de entrega à orientadora, Brasil inteiro (468.099 setores) | `entrega_orientadora/`, `nacional/` | **Vigente** — é o recorte da EDA |
| 21/08 | EDA Central, 1ª rodada | 104.108 | Blocos de renda e de água canalizada; matriz de correlação 10×10 | tabelas da raiz de `eda/`, deck `historico/2026-08-21_*` | **Superada** nas tabelas que dependem da renda |
| 24/08 | Diagnóstico fatorial | setores completos | Seis cenários: 7 ou 6 variáveis, Spearman ou Pearson, sem lixo, sem analfabetismo, normalização municipal | `eda/fatorial/` (sem prefixo) | Histórico — a fatorial definitiva é a do NB04 |
| 02/09 | Auditoria da renda e 2ª rodada da EDA | 104.108 | Critério de outlier (NORMAL, SUSPEITO, EXTREMO), o extremo de BH e a EDA refeita com `renda_media_sem_extremo` | `eda/` (`renda_*`), `eda/atualizada/`, deck do critério | **Vigente** |
| 17/09 | Notebook 04 — análise fatorial | 87.545 setores completos | Pesos 65/35, Φ = 0,522, bootstrap, cenários de faixa, AUC 0,813 contra FCU | `eda/fatorial/nb04_*`, relatório NB04, deck atual | **Vigente** |
| 25/09 | Fatorial ampliada (demandas de setembro) | por cenário | Sem rotação × Varimax × promax, banheiro, lixo, sensibilidade por município | `eda/fatorial_ampliada/`, NB04b | **Vigente** |
| 27/09 | Notebook 05 — grade do IVS | 73.878 na referência | 324 especificações, 192 elegíveis, referência proposta, o que o índice acrescenta à renda | `eda/ivs_especificacoes/`, relatório NB05 | **Vigente** — a escolha final é da orientadora |
| out | Decks de cronologia e de demandas, guia de apoio | — | Apresentação do que já existia; nenhuma análise nova | `complementos/` | Complemento |

---

## 3. O que foi analisado, dado por dado

A coluna "tabelas" diz em quantas das 144 tabelas o indicador aparece pelo nome — é um
termômetro de quanto ele foi explorado. A lista completa, com os nomes das tabelas, está
na aba *Indicadores* do catálogo.

### Os sete componentes do IVS

| Indicador | O que mede | Tabelas | Análises feitas |
|---|---|---:|---|
| `pct_agua_inad` | Água inadequada ou ausente | 16 | Descritivas (global, região, município), outliers, faltantes, correlações, FCU, Brasil, fatorial, grade |
| `pct_esgoto_inad` | Esgoto inadequado | 16 | Idem, mais o diagnóstico das duas definições (312 × 249) |
| `pct_lixo_inad` | Lixo inadequado | 16 | Idem; a fatorial o põe fora do construto e a grade testa com e sem ele |
| `razao_moradores` | Moradores por domicílio | 16 | Idem, mais os extremos da razão |
| `pct_analfab` | Analfabetismo, 15 anos ou mais | 18 | Idem, mais a auditoria do sigilo por município e por porte |
| `renda_media` | Renda média do responsável | 23 | Idem, mais a auditoria inteira da renda e a 2ª rodada |
| `pct_raca_pretpardind` | Pretos, pardos e indígenas | 18 | Idem |

### Os indicadores complementares

| Bloco | Indicadores | Tabelas | O que foi feito |
|---|---|---:|---|
| Chefia feminina | `pct_resp_feminino` | 9 | Proporção por setor e contagem de responsáveis por sexo (V01062/V01063) nos três níveis |
| Envelhecimento | `pct_idoso_60mais`, `iep_setor`, `rdi_setor`, `prop_70mais_entre_60mais`, `pct_pop_0a14`, `pct_crianca_0a4` | 2 a 9 | Estrutura etária e os índices de Galvão et al. (2025); o IEP agregado do Brasil bateu com o do IBGE |
| Água, outras definições | `pct_sem_agua_canalizada`, `pct_agua_nao_encanada`, `pct_agua_so_terreno` | 2 cada | Só o bloco 7h do NB02 |
| Banheiro | `pct_sem_banheiro`, `pct_sem_banheiro_nem_sanitario`, `pct_so_sanitario`, `pct_banheiro_comum` | 0 a 2 | Bloco 7c, a partição do V00495 e o banheiro graduado da grade |
| Moradia | `pct_dom_improv`, `pct_hab_precaria`, `pct_moradia_convencional`, `pct_moradia_nao_convencional`, `pct_apartamento`, `pct_casa`, `pct_casa_vila_condominio` | 2 a 4 | Blocos 7b e 7f e a morfologia V00048–V00058 |
| Renda, variantes | `renda_media_sem_extremo`, `renda_media_mediana_mun` | 0 a 1 | Entram na 2ª rodada (com o rótulo antigo, ver a seção 6) e na grade |

### As classificações do território

Urbano × rural (com a conferência da exclusão), favelas e comunidades urbanas (FCU, nos
três níveis e no comparativo de indicadores), moradia predominante agrupada, região,
município e a classificação `Dados_sig` (elegibilidade). O Brasil inteiro entra como
comparação, com a tabela de representatividade dos 70 municípios.

---

## 4. Os índices construídos e testados

| Índice | O que varia | Onde | Situação |
|---|---|---|---|
| IVS-BH 2012 (referência externa) | Duas dimensões, pesos 60/40, regra de faixas | `docs/referencias/` | Referência de comparação |
| Diagnóstico fatorial | 6 cenários de variáveis e correlação | `eda/fatorial/` | Histórico |
| IVS do NB04 | Pesos empíricos 65/35, eixo principal, Varimax e promax, escores | `eda/fatorial/nb04_*` | Vigente |
| Fatorial ampliada | Rotação, banheiro, lixo, sensibilidade por município | `eda/fatorial_ampliada/` | Vigente |
| Grade do NB05 | Renda (3) × lixo (2) × banheiro (3) × rotação e peso (9) × normalização (2) = 324 | `eda/ivs_especificacoes/` | Vigente; 192 elegíveis; referência proposta, não decidida |

Em todos eles, a validação externa é a mesma: a AUC contra os setores de favela.

---

## 5. As análises de qualidade dos dados

Feitas ao longo do caminho e importantes para a seção de método do artigo:

- **Sigilo do IBGE e `Dados_sig`**: que setores são elegíveis e por quê.
- **Denominador**: a troca de V01042 para V00001 em maio, que refez a EDA.
- **Esgoto**: as duas definições comparadas (312 × 249 setores divergentes).
- **Proporções fora do intervalo 0–1** e extremos da razão de moradores.
- **Analfabetismo**: 15,9% de faltantes, não aleatórios — o sigilo cai onde há poucos
  analfabetos. Limitação aceita no relatório da EDA.
- **Renda**: o critério de outlier e o setor extremo de BH (provável erro de dado),
  medidos na EDA, na fatorial e na normalização.
- **Validação da pipeline contra o IBGE**: no Brasil inteiro, o índice de envelhecimento
  deu 79,99 contra 80,0 publicado, e a população bateu com a oficial.

---

## 6. O que vale hoje, o que foi superado e as armadilhas

1. **A pasta `eda/atualizada/` substitui 15 tabelas da raiz de `eda/` com o mesmo nome.**
   As linhas continuam rotuladas `renda_media`, mas medem a renda sem o extremo. Ao citar
   um número, conferir de qual pasta ele saiu. No catálogo, as da raiz estão marcadas
   *Superado pela 2ª rodada*.
2. **Nove tabelas de auditoria usam o recorte com rurais (106.281 setores)**, não os
   104.108 da EDA. Não dá para pôr lado a lado sem dizer isso.
3. **O tamanho da base muda de uma análise para outra**: 104.108 setores na EDA, 87.545
   na fatorial (casos completos dos sete componentes) e 73.878 na referência do NB05 (o
   banheiro graduado perde setores). O artigo precisa dizer qual base sustenta cada número.
4. **As 19 tabelas do diagnóstico de 24/08 não são a fatorial definitiva.** Elas usam só
   componentes principais com Varimax; o NB04 compara componentes principais com eixo
   principal e acrescenta a rotação oblíqua, o bootstrap e a validação. Para o artigo,
   valem as `nb04_*`.
5. **O `Relatorio_EDA_Fase3_IVS_ELSI.docx` é a versão antiga**, ainda com os rurais. O
   `.md` é o que vale.
6. **O deck da 1ª rodada no histórico tem 40 slides**, mas o gerador hoje produz 47; ficou
   arquivado como foi apresentado.
7. **Indicadores calculados e pouco ou nada explorados**: `pct_so_sanitario` e
   `pct_banheiro_comum` não aparecem em nenhuma tabela; as três definições alternativas de
   água, a moradia e o RDI aparecem em só duas. São candidatos naturais a ficar fora do
   artigo, ou a material suplementar.
8. **As Fases 1 e 2 (em `Backup/`) não aplicavam o recorte ELSI.** Nenhum número delas
   deve ir para o artigo.

---

## 7. Como usar o catálogo para escolher

1. Abrir a aba *Indicadores* e marcar quais entram no artigo — os sete do IVS são o
   núcleo; os complementares são a decisão.
2. Na aba *Tabelas*, filtrar a coluna *situacao* por "Vigente" e marcar as candidatas,
   indicando a seção do artigo (método, resultados, suplementar).
3. Fazer o mesmo na aba *Figuras*.
4. Levar a planilha marcada para a reunião com a orientadora e anotar as decisões na
   coluna *Comentários*.

Se algum arquivo mudar, basta rodar de novo o gerador — as marcações feitas à mão,
porém, ficam só na cópia em que foram feitas.
