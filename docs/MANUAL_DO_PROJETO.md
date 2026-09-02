# Manual do Projeto IVS — Censo 2022

> **Para que serve este documento.** Duas coisas: encontrar qualquer arquivo do
> repositório sem precisar caçar, e apresentar o projeto para a orientação sabendo de onde
> vem cada número. É o documento para abrir depois de um tempo sem mexer no projeto.
>
> **Atualizado em:** 10 de agosto de 2026
> **Documento mestre (o porquê científico):** [`GUIA_DO_PROJETO.md`](../GUIA_DO_PROJETO.md)
> **Relatório técnico da EDA:** [`Relatorio_EDA_Fase3_IVS_ELSI.md`](Relatorio_EDA_Fase3_IVS_ELSI.md)

---

## Sumário

- [Parte A — Mapa do repositório](#parte-a--mapa-do-repositório)
- [Parte B — Onde está cada número da apresentação](#parte-b--onde-está-cada-número-da-apresentação)
- [Parte C — Como cada demanda foi feita: decisão, arquivos e reprodução](#parte-c--como-cada-demanda-foi-feita-decisão-arquivos-e-reprodução)
- [Parte D — Roteiro da apresentação, slide a slide](#parte-d--roteiro-da-apresentação-slide-a-slide)
- [Parte E — Perguntas que podem vir, e as respostas](#parte-e--perguntas-que-podem-vir-e-as-respostas)
- [Parte F — Como rodar tudo do zero](#parte-f--como-rodar-tudo-do-zero)
- [Parte G — Glossário](#parte-g--glossário)

---

# Parte A — Mapa do repositório

## A.1 Por onde começar, dependendo do que você precisa

| Se você quer… | Abra |
|---|---|
| Relembrar o projeto inteiro | `GUIA_DO_PROJETO.md` |
| Encontrar um arquivo | este manual, Parte A.2 |
| Entender um resultado da EDA | `docs/Relatorio_EDA_Fase3_IVS_ELSI.md` |
| Saber o que uma variável do Censo significa | `banco_de_dados/entrega_orientadora/Dicionario_Variaveis_Projeto.xlsx` |
| Ver como um indicador é calculado | `src/ivs_censo/indicadores.py` |
| Saber por que uma decisão foi tomada, e como refazê-la | este manual, Parte C |
| Refazer a base do zero | `notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb` |
| Preparar a reunião de orientação | Partes D e E deste manual |

## A.2 Pasta por pasta

### Raiz

| Arquivo | O que é |
|---|---|
| `GUIA_DO_PROJETO.md` | **Documento mestre.** Objetivo científico, metodologia, estado e plano. É o canônico: se algo divergir entre documentos, vale este. |
| `README.md` | Apresentação geral do repositório, com a tabela de status das etapas. |
| `estrutura_projeto.md` | Arquitetura técnica: árvore de diretórios e fluxo da pipeline. |
| `requirements.txt` | Dependências Python, com versões mínimas fixadas. |
| `LICENSE` | MIT. |

### `dados/` — entrada bruta do IBGE

Não versionado (2,4 GB). Se o repositório for clonado noutra máquina, é preciso baixar os
CSVs do IBGE de novo.

| Arquivo | Tamanho | O que traz |
|---|---:|---|
| `Agregados_por_setores_basico_BR_20250417.csv` | 137 MB | Identificação, `SITUACAO`, `CD_SIT`, `CD_TIPO`, `CD_FCU`, `NM_FCU`, população `v0001` |
| `Agregados_por_setores_caracteristicas_domicilio1_BR.csv` | 186 MB | `V00001`, `V00002`, `V00005`, `V00006`, tipos de domicílio `V00047`–`V00058` |
| `Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv` | 784 MB | Água, esgoto, lixo e banheiro |
| `Agregados_por_setores_alfabetizacao_BR.csv` | 735 MB | `V00900`, `V00901` |
| `Agregados_por_setores_cor_ou_raca_BR.csv` | 201 MB | `V01318`, `V01320`, `V01321` |
| `Agregados_por_setores_demografia_BR.csv` | 89 MB | Pirâmide etária `V01031`–`V01041` |
| `Agregados_por_setores_parentesco_BR.csv` | 362 MB | `V01042`, `V01062`, `V01063` |
| `Agregados_por_setores_renda_responsavel_BR.csv` | 27 MB | `V06004` |
| `municipios_elsi_brasil.csv` | 2 KB | **Versionado.** Lista oficial dos 70 municípios. |
| `dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx` | 118 KB | **Versionado.** Dicionário oficial do IBGE. |
| `dicionario_de_dados_renda_responsavel_20260508.xlsx` | 10 KB | **Versionado.** Dicionário do bloco de renda. |

> As subpastas `dados/output/`, `dados/processed/` e `dados/banco_de_dados/` são resíduo
> das Fases 1 e 2. Não são usadas pela pipeline atual.

### `notebooks/Fase3_EDA_ELSI/` — a pipeline ativa

| Arquivo | O que faz | Saída |
|---|---|---|
| `01_Extracao_Filtragem_ELSI.ipynb` | Lê os 8 CSVs, cruza com a lista ELSI por UF + nome normalizado, filtra, faz o merge, classifica morfologia e roda a auditoria | `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` |
| `02_Analises_Descritivas.ipynb` | Tipagem e sigilo, elegibilidade, recorte urbano, os 7 indicadores, 6 blocos descritivos, figuras e correlações | CSVs e PNGs em `banco_de_dados/eda/` |
| `README.md` | Convenções da fase e estrutura das seções do NB02 | — |

**Células do NB02 que importam** (o `id` aparece nos metadados de cada célula):

| Célula | Seção | O que faz |
|---|---|---|
| `step2` | 2 | Tipagem, sigilo `X` → nulo, vírgula decimal |
| `step3` | 3 | Classificação `Dados_sig` |
| `filtro-urbano` | 3b | **Recorte urbano** e tabelas de conferência |
| `step4` | 4 | Os 7 indicadores do IVS |
| `step4b` | 4b | Diagnóstico da faixa de esgoto |
| `step5`–`step7` | 5–7 | Descritivas global, por município, por região |
| `hab-precaria` | 7b | Habitação precária |
| `banheiro-inad` | 7c | Inadequação de banheiro |
| `resp-fem` | 7d | Responsável do sexo feminino |
| `idade-estrutura` | 7e | **Envelhecimento: IEP, RDI, % 60+** |
| `tipo-domicilio` | 7f | **Moradia convencional e apartamento** |
| `favelas-fcu` | 7g | **Favelas e comunidades urbanas** |
| `step8`–`step12` | 8–12 | Histogramas, boxplots, outliers, faltantes, correlações |
| `step13` | 13 | Exportação das tabelas principais |

### `src/ivs_censo/` — código compartilhado

Existe para que o cálculo nacional use exatamente as mesmas fórmulas do notebook, sem
copiar código.

| Arquivo | O que contém | Quando abrir |
|---|---|---|
| `fontes.py` | Os 8 arquivos do Censo, a chave do setor em cada um e quais variáveis o projeto lê de cada | Para saber de qual arquivo vem uma variável |
| `indicadores.py` | Definição declarativa dos 26 indicadores (numerador, denominador, escala) + `calcular_indicadores` e `classificar_dados_sig` | **Para conferir a fórmula de qualquer indicador** |
| `dicionario.py` | Monta a tabela de variáveis a partir dos dicionários oficiais | Para regenerar o dicionário |

### `scripts/` — executáveis versionados

| Script | O que gera | Tempo |
|---|---|---:|
| `gerar_tabela_variaveis.py` | `Dicionario_Variaveis_Projeto.csv` e `.xlsx` | segundos |
| `gerar_entrega_orientadora.py` | O pacote de entrega: CSV + SQLite com 104 colunas | ~1 min |
| `proporcoes_brasil.py` | Os indicadores para os 468 mil setores do país | ~7 min |

### `banco_de_dados/` — saídas

```
banco_de_dados/
├── Base_ELSI_Bruta_Censo2022.csv       saída do NB01 · 109.032 × 68 · não versionado
├── eda/                                 saídas do NB02
│   ├── figuras/                         os 4 PNGs da apresentação
│   └── (34 CSVs)                        tabelas descritivas
├── nacional/                            saídas do cálculo Brasil inteiro
└── entrega_orientadora/                 o pacote de entrega
```

**`eda/` — onde está cada tabela:**

| Assunto | Arquivos |
|---|---|
| Elegibilidade | `elegibilidade_setores.csv` |
| Recorte urbano | `situacao_urbano_rural_{total,por_regiao,por_municipio}.csv`, `exclusao_rural_conferencia.csv` |
| Descritivas dos 7 | `descritivas_{globais,por_municipio,por_regiao}.csv` |
| Outliers | `outliers.csv` |
| Dados faltantes | `missing_por_municipio.csv` |
| Correlações | `correlacao_{pearson,spearman}.csv` |
| Habitação precária | `habitacao_precaria_{global,por_regiao,por_municipio}.csv` |
| Banheiro | `inadequacao_banheiro_{global,por_regiao,por_municipio}.csv` |
| Chefia feminina | `resp_feminino_{global,por_regiao,por_municipio}.csv` |
| Envelhecimento | `indicadores_envelhecimento_{total,por_regiao}.csv`, `estrutura_etaria_{global,por_regiao,por_municipio,contagem_por_municipio}.csv` |
| Tipo de domicílio | `tipo_domicilio_{global,totais_por_grupo,por_regiao,por_municipio}.csv`, `moradia_predominante_agrupada_por_regiao.csv` |
| Favelas | `favelas_fcu_{total,por_regiao,por_municipio,comparativo_indicadores}.csv` |
| Auditorias | `diagnostico_proporcoes_fora_intervalo.csv`, `diagnostico_esgoto_312_vs_249.csv`, `extremos_razao_moradores.csv` |

> ⚠️ Alguns CSVs da pasta são **órfãos**: foram commitados mas não há código que os
> reproduza (`auditoria_analfabetismo_*`, `cobertura_*`, `morfologia_v00048_v00058_por_regiao`,
> `saneamento_categorias_por_regiao`, `resp_feminino_contagem_*`). Confirmar a metodologia
> antes de reusar. A procedência arquivo a arquivo está em `banco_de_dados/eda/README.md`.

**`entrega_orientadora/` — o que entregar:**

| Arquivo | Conteúdo |
|---|---|
| `Base_ELSI_70Municipios_Censo2022.csv` / `.db` | 109.032 setores × 104 colunas |
| `Base_BeloHorizonte_Censo2022.csv` / `.db` | 5.166 setores, mesmo esquema |
| `Dicionario_Variaveis_Projeto.csv` / `.xlsx` | As 72 variáveis com descrição oficial e arquivo-fonte |
| `README.md` | Como abrir os `.db` e o que é cada coluna |

Cada `.db` tem três tabelas: `setores_censitarios`, `dicionario_variaveis` e `metadados`.
Para o recorte de análise:

```sql
SELECT * FROM setores_censitarios WHERE Dados_sig = 'OK' AND urbano = 1;
```

### `docs/` — documentação e fontes

| Arquivo | O que é |
|---|---|
| `MANUAL_DO_PROJETO.md` | Este documento |
| `Relatorio_EDA_Fase3_IVS_ELSI.md` | Relatório técnico da EDA, reescrito sobre o recorte urbano |
| `Relatorio_EDA_Fase3_IVS_ELSI.docx` | ⚠️ Versão antiga, ainda sobre o recorte com rurais |
| `Relatorio_Integridade_Projeto.md` | Diagnóstico técnico de maio, com nota de revisão no topo |
| `Cálculo IVS2012.docx` | **Metodologia-fonte.** Define denominadores, `Dados_sig` e quais formas são inadequadas |
| `indice_vulnerabilidade2012 (2).pdf` | IVS-BH 2012 oficial |
| `guia_analises.docx` | Framework FIOCRUZ de EDA |
| `Plano_Artigo_Cientifico_IC_Preenchido.docx` | Plano do artigo, por fases |
| `Plano de trabalho.pdf` | Cronograma da IC |
| `Apresentacoes_IVS/` | Apresentação atual na raiz + `historico/` e `dicionarios/`. Índice em `Apresentacoes_IVS/README.md` |

### `tests/`

| Arquivo | O que cobre |
|---|---|
| `test_pipeline_fase3.py` | Os artefatos gerados: contagens, colunas, coerência entre tabelas |
| `test_ivs_censo.py` | As fórmulas, com dados sintéticos |

```bash
python -m pytest tests/ -v
```

São 65 testes. Se todos passam, a pipeline está íntegra.

### `Backup/` — legado

Fases 1 e 2, scripts antigos. Não faz parte da pipeline. Só abrir para consultar histórico.

---

# Parte B — Onde está cada número da apresentação

Se alguém perguntar "de onde saiu esse número", esta é a tabela.

| Slide | Número | Arquivo de origem |
|---|---|---|
| 3 | 70 municípios · 104.108 setores · 26 indicadores | `exclusao_rural_conferencia.csv` · `src/ivs_censo/indicadores.py` |
| 3 | 65 testes | `pytest tests/` |
| 7 | Tamanho dos 8 arquivos | `dados/` |
| 8 e 9 | As 28 variáveis e seus arquivos | `Dicionario_Variaveis_Projeto.csv` |
| 11 | Elegibilidade (1.736 / 1.015 / 0 / 106.281) | `elegibilidade_setores.csv` |
| 11 | Funil 109.032 → 106.281 → 104.108 | `exclusao_rural_conferencia.csv` |
| 11 | 29 municípios perdem >10%, 14 perdem >50% | `exclusao_rural_conferencia.csv` |
| 13 | 37 → 43 células | o próprio `.ipynb` |
| 14 | Figura dos histogramas | `figuras/histogramas.png` |
| 15 | Descritivas dos 7 indicadores | `descritivas_globais.csv` |
| 16 | Figura dos boxplots · médias regionais | `figuras/boxplots_por_regiao.png` · `descritivas_por_regiao.csv` |
| 17 | Figura da matriz de correlação | `figuras/matriz_correlacao.png` |
| 18 | −0,81 · −0,76 e demais | `correlacao_spearman.csv` |
| 19 | Figura de faltantes · BH 22,5% | `figuras/missing_por_municipio.png` · `missing_por_municipio.csv` |
| 20 | Outliers e limites do IQR | `outliers.csv` |
| 22 | 19.507 setores · 5.903 favelas · 10,07 mi | `favelas_fcu_total.csv` |
| 22 | Percentuais por região | `favelas_fcu_por_regiao.csv` |
| 23 | Razões favela ÷ não-favela | `favelas_fcu_comparativo_indicadores.csv` |
| 24 | IEP 92,7 · RDI 25,5 · por região | `indicadores_envelhecimento_{total,por_regiao}.csv` |
| 24 | IEP Brasil 79,99 · população 203.080.756 | `nacional/proporcoes_por_recorte.csv` · `nacional/representatividade_elsi_no_brasil.csv` |
| 25 | Representatividade e comparativo | `nacional/representatividade_elsi_no_brasil.csv` · `nacional/comparativo_brasil_vs_elsi.csv` |
| 27 | 99,19% convencional · 31,5% apartamento | `tipo_domicilio_totais_por_grupo.csv` · `tipo_domicilio_global.csv` |

**Todos os números da apresentação foram conferidos contra estes arquivos** por um script
de auditoria: 218 valores checados, nenhuma divergência.

---

# Parte C — Como cada demanda foi feita: decisão, arquivos e reprodução

> **Este documento e o relatório se dividem assim.** A [seção 12 do relatório da EDA](Relatorio_EDA_Fase3_IVS_ELSI.md)
> traz a *argumentação*: por que decidi como decidi, quais alternativas descartei e o que
> verifiquei. Esta parte traz a *operação*: quais arquivos foram tocados, qual célula faz o
> quê, como reproduzir e como conferir. Se a pergunta é "por quê", vá ao relatório; se é
> "onde está" ou "como rodo de novo", fique aqui.

---

## C.1 Demanda 1 — Índice de envelhecimento

**A decisão.** O denominador do Índice de Envelhecimento passou de crianças de 0 a 4 anos
para a população com **menos de 15 anos**, conforme o Quadro 1 de Galvão et al. (2025).
Acrescentei a Razão de Dependência de Idosos e o percentual de 60 anos ou mais. Descartei
usar o corte de 65 anos porque o IBGE agrega a faixa como "60 a 69", sem separar 65.

**O que mudou no repositório:**

| Arquivo | O que mudou |
|---|---|
| `notebooks/Fase3_EDA_ELSI/01_...ipynb`, célula `demais-defs` | `usecols` do bloco `demog` ganhou `V01034`–`V01039` (faixas de 15 a 59) |
| `notebooks/Fase3_EDA_ELSI/02_...ipynb`, células `idade-md` e `idade-estrutura` | seção 7e reescrita com IEP, RDI e % 60+, em versão agregada e por setor |
| `src/ivs_censo/indicadores.py` | indicadores `iep_setor`, `rdi_setor` e `prop_70mais_entre_60mais` |
| `tests/test_pipeline_fase3.py` | teste que trava o denominador em 0–14 |

**Saídas geradas:** `indicadores_envelhecimento_{total,por_regiao}.csv` e
`estrutura_etaria_{global,por_regiao,por_municipio,contagem_por_municipio}.csv`.

**Como reproduzir.** Precisa rodar o **Notebook 01 antes**, porque as faixas de 15 a 59 não
existiam na base. Depois o Notebook 02.

**Como conferir.** Duas travas: a soma das 11 faixas etárias tem que reproduzir `v0001`
(a auditoria do NB01 imprime isso — 99.957 setores comparáveis, nenhuma divergência), e o
IEP nacional tem que dar 79,99 contra os 80,0 do IBGE (`nacional/proporcoes_por_recorte.csv`).

**Se perguntarem por que não tem Longevidade:** porque o LI exige a faixa de 75 anos ou
mais e o topo da pirâmide publicada por setor é `V01041` = "70 anos ou mais". O que existe
é a proporção de 70+ entre os 60+, que **não é o LI** e está rotulada como tal.

---

## C.2 Demanda 2 — Tabela de variáveis com significado e fonte

**A decisão.** As descrições vêm dos **dicionários oficiais do IBGE**, não de texto meu.
Onde o IBGE não descreve — as dez colunas de identificação e classificação territorial —
escrevi a descrição, mas marquei na coluna `origem_da_descricao` para o leitor saber
distinguir.

**O que mudou no repositório:**

| Arquivo | O que faz |
|---|---|
| `src/ivs_censo/fontes.py` | fonte única de procedência: qual arquivo do Censo traz cada variável e qual o nome da chave do setor naquele arquivo |
| `src/ivs_censo/dicionario.py` | lê as três abas dos dois dicionários oficiais e cruza com a procedência |
| `scripts/gerar_tabela_variaveis.py` | gera o CSV e o XLSX |
| `scripts/gerar_entrega_orientadora.py` | embute a mesma tabela na tabela `dicionario_variaveis` dos `.db` |

**Saídas:** `banco_de_dados/entrega_orientadora/Dicionario_Variaveis_Projeto.csv` e `.xlsx`
(este com uma aba por arquivo do Censo).

**Como reproduzir:**

```bash
python scripts/gerar_tabela_variaveis.py
```

Não depende dos notebooks — lê os dicionários direto de `dados/`.

**Como conferir.** São 72 variáveis de 8 arquivos: 62 descrições do dicionário oficial e 10
da documentação do projeto. Nenhuma linha pode sair como `(sem descrição)`.

**Detalhe que costuma confundir.** O IBGE grafa a chave do setor de três formas diferentes
(`CD_SETOR`, `CD_setor`, `setor`), então as três aparecem na tabela como variáveis
distintas. É proposital: a tabela documenta o que existe em cada arquivo. A pipeline
padroniza tudo em `CD_SETOR` na leitura.

---

## C.3 Demanda 3 — Excluir setores rurais

**A decisão.** O filtro é aplicado **no notebook de análise, não na extração**. A base bruta
continua com os 109.032 setores. Isso mantém a exclusão auditável, reversível e permite a
tabela de conferência que foi pedida junto.

**O que mudou no repositório:**

| Arquivo | O que mudou |
|---|---|
| `02_...ipynb`, célula `step3` | ordem das condições do `Dados_sig` corrigida (população zero antes de sigilo) |
| `02_...ipynb`, células `filtro-urbano-md` e `filtro-urbano` | **seção 3b, nova**: composição urbano/rural, aplicação do filtro e conferência |
| `02_...ipynb`, célula `step2` | `CD_SIT` entra na lista de colunas de texto |
| `tests/test_pipeline_fase3.py` | testes do recorte e da conferência |

**Saídas:** `situacao_urbano_rural_{total,por_regiao,por_municipio}.csv` e
`exclusao_rural_conferencia.csv`.

**Onde o filtro acontece exatamente.** Na célula `filtro-urbano`, a linha
`df_ok = df_ok[mask_urbano].copy()`. Antes dela, `df_ok_com_rural` guarda o conjunto
anterior. **Tudo que vem depois no notebook usa o recorte urbano** — as descritivas, as
correlações e as figuras.

**Como desfazer, se precisar.** Comentar essa única linha. Não é preciso reprocessar o
Notebook 01 nem tocar na base bruta.

**Como conferir.** `exclusao_rural_conferencia.csv` tem que somar 106.281 em `n_ok_total` e
104.108 em `n_ok_urbano`, com 70 municípios.

---

## C.4 Demanda 4 — Agrupar as moradias convencionais

**A decisão.** Três grupos, com o critério de **adequação da edificação como moradia** e não
de tipologia arquitetônica: convencional (`V00047`–`V00049`), não convencional
(`V00050`–`V00052`) e improvisado (`V00053`–`V00058`). Denominador `V00001`.

**O que mudou no repositório:**

| Arquivo | O que mudou |
|---|---|
| `02_...ipynb`, células `tipo-domicilio-md` e `tipo-domicilio` | **seção 7f, nova**: os cinco indicadores de tipo de domicílio e a versão agrupada da moradia predominante |
| `src/ivs_censo/indicadores.py` | `pct_moradia_convencional`, `pct_moradia_nao_convencional`, `pct_casa`, `pct_casa_vila_condominio` |
| `tests/test_pipeline_fase3.py` | teste de coerência da soma dos grupos |

**Saídas:** `tipo_domicilio_{global,totais_por_grupo,por_regiao,por_municipio}.csv` e
`moradia_predominante_agrupada_por_regiao.csv`.

**Como conferir.** A própria célula imprime a verificação do denominador: a soma dos seis
tipos de DPPO não pode ultrapassar `V00001` em nenhum setor. Se aparecer "soma > V00001"
diferente de zero, a interpretação das variáveis está errada — hoje dá zero, com déficit
máximo de 6 domicílios por sigilo.

---

## C.5 Demanda 5 — Indicador de apartamento

**A decisão.** `pct_apartamento = V00049 ÷ V00001`, mantido **fora dos sete componentes do
IVS**. O motivo é que ele não tem direção de vulnerabilidade definida: verticalização
aparece tanto em área central rica quanto em conjunto habitacional popular. Serve para
caracterizar o território, não para pontuá-lo.

**Onde está.** Mesma célula `tipo-domicilio` da demanda anterior, e em
`src/ivs_censo/indicadores.py` na lista `INDICADORES_COMPLEMENTARES` — **não** em
`INDICADORES_IVS`. Essa separação no código é o que impede que ele entre no índice por
descuido.

**Saídas:** as mesmas tabelas de tipo de domicílio; o ranking municipal sai de
`tipo_domicilio_por_municipio.csv` filtrando `variavel == 'pct_apartamento'`.

---

## C.6 Demanda 6 — Setores de vilas e favelas

**A decisão.** O critério é `CD_TIPO = 1`, o campo oficial de classificação do setor.
Testei contra a alternativa ("tem `NM_FCU` preenchido") nos 468.099 setores do país e os
dois coincidem em 33.272 setores. No recorte ELSI há 25 setores com nome de FCU mas
`CD_TIPO ≠ 1`; a célula os isola e eles seguem o critério oficial.

**O que mudou no repositório:**

| Arquivo | O que mudou |
|---|---|
| `01_...ipynb`, célula `basico-load` | `col_basico` ganhou `CD_SIT`, `CD_TIPO`, `CD_FCU`, `NM_FCU` |
| `01_...ipynb`, célula `basico-md` | documentação dos códigos e da correspondência `CD_SIT` × `SITUACAO` |
| `01_...ipynb`, célula `audit` | auditoria passou a conferir `CD_TIPO = 1` contra `NM_FCU` preenchido |
| `02_...ipynb`, célula `step2` | as quatro colunas entram em `COLS_TEXTO` |
| `02_...ipynb`, células `favelas-md` e `favelas-fcu` | **seção 7g, nova**: contagem e comparação de indicadores |

**Saídas:** `favelas_fcu_{total,por_regiao,por_municipio,comparativo_indicadores}.csv`.

**Por que as quatro colunas são texto e não número.** São códigos de classificação. Se
fossem convertidas para número, `CD_TIPO = 0` viraria zero numérico e perderia o sentido de
categoria, e códigos com zero à esquerda seriam truncados. A linha que garante isso é a
lista `COLS_TEXTO` da célula `step2`.

**Como reproduzir.** Precisa do **Notebook 01 antes** — as colunas não existiam na base.

**Como conferir.** A auditoria do NB01 imprime a contagem de `CD_TIPO = 1` e as
divergências contra `NM_FCU`. Esperado: 19.507 e 25.

---

## C.7 Demanda 7 — Proporções para o Brasil todo

**A decisão.** Em vez de copiar o código do Notebook 02 e tirar o filtro de municípios,
extraí as definições dos indicadores para um módulo. Duas cópias da mesma fórmula divergem
na primeira correção feita em uma só delas, e aí Brasil e ELSI deixam de ser comparáveis —
que é justamente o objetivo da demanda.

**O que mudou no repositório:**

| Arquivo | O que contém |
|---|---|
| `src/ivs_censo/fontes.py` | os 8 arquivos, a chave de cada um e as variáveis lidas |
| `src/ivs_censo/indicadores.py` | os 26 indicadores como objetos declarativos, mais `calcular_indicadores` e `classificar_dados_sig` |
| `src/ivs_censo/dicionario.py` | a tabela de variáveis |
| `scripts/proporcoes_brasil.py` | lê os 8 arquivos, monta a base nacional e calcula os indicadores |
| `tests/test_ivs_censo.py` | testa as fórmulas com dados sintéticos |

**Saídas:** `banco_de_dados/nacional/` — `proporcoes_por_recorte.csv`,
`proporcoes_brasil_por_{regiao,uf,municipio}.csv`, `comparativo_brasil_vs_elsi.csv`,
`representatividade_elsi_no_brasil.csv`.

**Como reproduzir:**

```bash
python scripts/proporcoes_brasil.py
```

Leva cerca de 7 minutos e lê os 2,4 GB de `dados/`. Não depende dos notebooks.

**Como conferir.** Dois totais travados em teste: a população do Brasil tem que dar
**203.080.756** e os setores **468.099**. Se algum dos dois mudar, alguma coisa quebrou na
leitura.

> ⚠️ **Não troque `float64` por `float32` para economizar memória.** Já tentei: a soma da
> população dava 203.080.736, vinte pessoas a menos. Irrelevante nas proporções, mas os
> totais são exatamente por onde alguém confere o trabalho. Há um teste que trava isso.

---

## C.8 As decisões que não vieram de demanda

**Denominador `V00001`.** Está declarado em `src/ivs_censo/indicadores.py`, no campo
`denominador` de cada indicador, e nas fórmulas da célula `step4` do NB02. O `V01042`
continua sendo extraído, mas só para auditoria de setores coletivos — não é denominador de
nada. A verificação que sustenta a escolha: nenhuma proporção ultrapassa 1,0.

**Ordem das condições do `Dados_sig`.** Célula `step3` do NB02 e função
`classificar_dados_sig` em `src/ivs_censo/indicadores.py`. A ordem correta é
`[cond_zerado, cond_sig, cond_col]` — população zero **antes** de sigilo. Se alguém
inverter, o sigilo volta a ser reportado como 2.751 em vez de 1.015.

**Caçamba de lixo (`V00398`).** Entra como destino inadequado, por fidelidade ao
`Cálculo IVS2012.docx`. Há um comentário no código da célula `step4` avisando para não
remover sem decisão metodológica explícita. **A ressalva:** as análises indicam que essa
escolha pode estar fazendo o indicador capturar porte urbano — ver §11 e §12.9 do relatório.

---

## C.9 O que precisa rodar quando você mexe em quê

| Se você mexer em… | Precisa rodar |
|---|---|
| `dados/municipios_elsi_brasil.csv` ou nos `usecols` do NB01 | NB01 → NB02 → os três scripts |
| Fórmula de indicador no NB02 | NB02 (e conferir se a mesma fórmula está em `src/`) |
| `src/ivs_censo/indicadores.py` | `proporcoes_brasil.py` e `gerar_entrega_orientadora.py` |
| `src/ivs_censo/fontes.py` ou `dicionario.py` | `gerar_tabela_variaveis.py` e `gerar_entrega_orientadora.py` |
| Dicionários oficiais em `dados/` | `gerar_tabela_variaveis.py` |
| Qualquer coisa | `python -m pytest tests/ -v` |

> ⚠️ **Duplicação conhecida entre o notebook e o módulo.** O Notebook 02 **não importa**
> `src/ivs_censo` — ele define as fórmulas nas próprias células. O módulo existe para o
> cálculo nacional e para os scripts. Na prática isso significa que **as fórmulas vivem em
> dois lugares**, e mudar uma sem mudar a outra faz o recorte ELSI divergir do nacional
> em silêncio. Enquanto essa duplicação existir, toda mudança de fórmula precisa ser feita
> nos dois. Unificar (fazer o notebook importar o módulo) é uma melhoria pendente, e o
> teste de fórmulas em `tests/test_ivs_censo.py` cobre só o lado do módulo.

---

# Parte D — Roteiro da apresentação, slide a slide

O arquivo é `docs/Apresentacoes_IVS/historico/2026-08-09_Andamento.pptx` (arquivado em 21/08/2026; a apresentação corrente é `EDA_Central_IVS_2026-09_rev2.pptx`). **Todos os 30 slides têm
notas do apresentador** — o que está abaixo é o roteiro em prosa, com o encadeamento.

## Bloco 1 · Abertura (slides 1 a 5) — 4 minutos

**Slide 2 · O que trago.** Anuncie os cinco blocos. Deixe claro desde o início que o
objetivo da reunião é chegar às quatro decisões do slide 28.

**Slide 3 · Relembrando o projeto.** Cinco números e a definição em uma frase: índice
composto para comparar setores **dentro** de cada cidade. O ponto a martelar é a unidade de
análise — setor censitário, cerca de 300 domicílios.

**Slide 4 · A pergunta e o desenho.** PICOS e hipóteses. Mencione que o desenho é ecológico,
porque isso volta nas limitações.

**Slide 5 · Onde parei e o que fiz.** É o slide de prestação de contas. Separe claramente
o que já existia em julho, o que acrescentou em agosto e o que ainda não fez. Encerre com a
frase-chave: *a base está madura, o que falta agora é estatística, não tratamento de dado*.

## Bloco 2 · Dados e método (slides 6 a 11) — 5 minutos

É recapitulação. **Passe rápido**, a menos que perguntem.

**Slide 7 · Os oito arquivos.** Mostre a escala (2,4 GB) e as três armadilhas — sigilo,
codificação, vírgula decimal.

**Slides 8 e 9 · As variáveis, uma a uma.** Aqui vale ir devagar: são as 28 variáveis com
nome, descrição e arquivo de origem. Se a orientação quiser conferir alguma escolha
metodológica, é neste slide que a conversa acontece. Chame atenção para duas coisas: a
caçamba (`V00398`) contar como lixo inadequado, e o analfabetismo ser o único indicador em
que a mesma variável aparece no numerador e no denominador.

**Slide 10 · O que o Censo não permite.** As três substituições em relação ao IVS-BH.
Antecipa a crítica de que "isso não é o IVS-BH": é uma adaptação declarada.

**Slide 11 · Quais setores entram.** Elegibilidade, funil e as duas caixas de baixo: a
correção da ordem da regra e a desigualdade da exclusão rural. Se houver pouco tempo, a
caixa da direita é a mais importante — ela vira limitação do artigo.

## Bloco 3 · A análise exploratória (slides 12 a 20) — 8 minutos

É o núcleo técnico.

**Slide 13 · O que mudei na EDA.** Tabela das seções alteradas. Serve para mostrar o
escopo do trabalho de agosto.

**Slide 14 · Histogramas.** A mensagem é a **forma** das distribuições: saneamento colado
no zero, renda com cauda longa, razão de moradores simétrica. Diga que isso condiciona a
normalização.

**Slide 15 · Descritivas.** Números que sustentam o slide anterior. Destaque o n menor do
analfabetismo.

**Slide 16 · Boxplots por região.** O gradiente Norte-Sul e as duas exceções: analfabetismo
com pico no Nordeste e lixo plano.

**Slides 17 e 18 · Correlação.** Primeiro a figura completa, depois a leitura. Este é o
slide para provocar a discussão metodológica: se renda, cor/raça e analfabetismo se
correlacionam a −0,81 e −0,76, elas entram no índice com três pesos ou com um?

**Slide 19 · Dados faltantes.** O ponto não é "faltam 15,9%", é **onde** faltam. O sigilo é
informativo: falta mais onde há menos analfabetos. Por isso não imputa zero.

**Slide 20 · Outliers.** Explique por que a regra do IQR não vale para o saneamento. Sem
isso, os 20% de "outliers" parecem problema de qualidade de dado.

## Bloco 4 · Os achados (slides 21 a 25) — 6 minutos

**Slides 22 e 23 · Favelas.** O achado mais forte. Primeiro o retrato (19.507 setores,
metade dos setores do Norte), depois a comparação (esgoto 4,14× pior, renda a um terço).
Feche com o argumento de validação: quando o índice existir, comparar sua distribuição
entre favela e não-favela é o teste de validade mais direto disponível.

**Slide 24 · Envelhecimento.** Primeiro o que estava errado (denominador 0 a 4), depois o
que está certo (menores de 15), depois o que é impossível (Longevidade, porque não há faixa
de 75+). Encerre com a validação: 79,99 contra 80,0 do IBGE.

**Slide 25 · Brasil × ELSI.** A amostra representa o Brasil urbano de grande porte, não o
Brasil. E a anomalia do lixo, que conecta com o slide 18.

## Bloco 5 · Demandas e caminho (slides 26 a 30) — 5 minutos

**Slide 27 · As sete demandas.** Um cartão por demanda, com o resultado. É o slide de
prestação de contas do bloco.

**Slide 28 · O que está em aberto.** Seja direto sobre o que não está resolvido. As quatro
caixas de baixo são o objetivo da reunião.

**Slide 29 · O caminho até o índice.** A sequência NB03 → NB04 → NB05 → mapas, com as
dependências. Proponha começar pelo NB03 imediatamente, já que ele não depende de nenhuma
das quatro decisões.

**Slide 30 · Em resumo.** Retome as quatro decisões e encerre.

> **Tempo total estimado:** 28 minutos de fala, sem contar as perguntas.
> Se tiver só 15 minutos: slides 3, 5, 11, 15, 18, 23, 24, 27, 28, 29.

---

# Parte E — Perguntas que podem vir, e as respostas

**"Por que V00001 e não o número de responsáveis?"**
Porque `V01042` conta pessoas responsáveis, não domicílios. O `V00001` é o equivalente
exato, no Censo 2022, do `V002` que o IVS-BH 2012 usou no Censo 2010. Prova empírica: com
`V00001` nenhuma proporção ultrapassa 1,0 em nenhum dos 104 mil setores.

**"Por que a caçamba conta como lixo inadequado?"**
Porque o `Cálculo IVS2012.docx` define assim: só a coleta porta a porta (`V00397`) é
adequada. É metodologia herdada, não escolha minha. Mas há um indício empírico de que essa
escolha esteja distorcendo o indicador — ver a anomalia do slide 25 — e por isso trago a
decisão.

**"Esse índice é comparável com o IVS-BH original?"**
Parcialmente. Três componentes não são reprodutíveis com os agregados do Censo 2022: anos
de estudo dos chefes, faixas de renda familiar e óbitos cardiovasculares. As substituições
estão no slide 10 e precisam ir para os métodos do artigo.

**"Por que excluir os rurais se o município inteiro faz parte da amostra ELSI?"**
Porque o índice é intraurbano por definição, e setores rurais têm padrões de saneamento que
não se comparam aos urbanos. A exclusão está documentada município a município, e a base
bruta preserva todos os setores para auditoria.

**"Quantos setores você perdeu com o sigilo?"**
1.015 setores saem por sigilo em população ou domicílios, menos de 1%. O sigilo relevante é
outro: 15,9% dos setores não têm a taxa de analfabetismo, e de forma não aleatória.

**"O que garante que a sua pipeline está certa?"**
Três coisas: 65 testes automatizados; a soma das faixas etárias reproduzir exatamente a
população em todos os setores comparáveis; e o cálculo nacional reproduzir o índice de
envelhecimento publicado pelo IBGE (79,99 contra 80,0) e a população do Censo
(203.080.756, exato).

**"Quando sai o índice?"**
O cronograma reserva agosto e setembro. O NB03 pode começar imediatamente; NB04 e NB05
dependem da decisão sobre os pesos.

---

# Parte F — Como rodar tudo do zero

```bash
pip install -r requirements.txt
```

1. **Notebook 01** (`notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb`) — ~4 min.
   Gera `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv`. Só precisa rodar de novo se a lista
   de municípios, os dados-fonte ou o conjunto de colunas extraídas mudarem.
2. **Notebook 02** (`02_Analises_Descritivas.ipynb`) — ~2 min. Gera todas as tabelas e
   figuras da EDA.
3. **Scripts**, em qualquer ordem:
   ```bash
   python scripts/gerar_tabela_variaveis.py
   python scripts/gerar_entrega_orientadora.py
   python scripts/proporcoes_brasil.py
   ```
4. **Testes**:
   ```bash
   python -m pytest tests/ -v
   ```

**Convenções que precisam ser respeitadas:**

- Os notebooks são versionados **sem outputs**. Limpe antes de commitar.
- No JSON do `.ipynb`, células de código são string única e markdown é lista de linhas.
  Manter isso evita diffs enormes.
- Os CSVs do projeto usam `;` como separador e `utf-8-sig` como codificação, para abrirem
  direto no Excel em português.

---

# Parte G — Glossário

**Setor censitário.** Menor unidade territorial do IBGE, cerca de 300 domicílios. É a
unidade de análise do projeto.

**Agregados por setores.** Conjunto de arquivos em que o IBGE publica contagens por setor,
sem microdados individuais.

**DPPO.** Domicílio Particular Permanente Ocupado. É o `V00001`, denominador padrão.

**DPIO.** Domicílio Particular Improvisado Ocupado (`V00002`).

**Sigilo.** Supressão de contagens pequenas pelo IBGE, marcada com `X`. Vira nulo na
análise, nunca zero.

**`Dados_sig`.** Coluna criada pela pipeline que classifica cada setor em `OK`, `SIGILOSO`,
`ZERADO` ou `COLETIVO`.

**Recorte urbano.** `Dados_sig = 'OK'` e `SITUACAO = 'Urbana'`. São os 104.108 setores que
entram na análise.

**FCU.** Favela e Comunidade Urbana — categoria que o Censo 2022 criou no lugar de
"aglomerado subnormal". Marcada em `CD_TIPO = 1`.

**IEP.** Índice de Envelhecimento Populacional: pessoas de 60 anos ou mais divididas pelas
de menos de 15, vezes 100.

**RDI.** Razão de Dependência de Idosos: 60 anos ou mais divididos pela população de 15 a
59, vezes 100.

**PPI.** Pretos, pardos e indígenas — a soma `V01318 + V01320 + V01321`.

**Razão agregada.** Soma dos numeradores dividida pela soma dos denominadores de um grupo.
Trata o território como um só. Diferente da média entre setores, que dá peso igual a cada
setor.

**Falácia ecológica.** Erro de atribuir a indivíduos uma associação observada em dados
agregados. É a limitação central de todo estudo ecológico.
