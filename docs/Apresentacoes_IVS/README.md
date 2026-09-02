# Apresentações — Projeto IVS Censo 2022

**A apresentação atual é a que está na raiz desta pasta.** Tudo que estiver em `historico/`
já foi apresentado e ficou para trás — não use como fonte de número.

```
Apresentacoes_IVS/
├── EDA_Central_IVS_2026-09_rev2.pptx   ← A APRESENTAÇÃO. É a única coisa na raiz.
├── complementos/                        ← documentos de apoio do deck atual
├── historico/                           ← 11 decks fora de circulação, em ordem cronológica
└── dicionarios/                         ← planilhas de variáveis (não são apresentações)
```

**A raiz tem um arquivo só, e é de propósito.** Quem abre a pasta com pressa pega o que está
na raiz; se houver quatro arquivos ali, um deles vai ser aberto por engano. Foi o que
aconteceu em agosto, quando roteiro, resumo e o deck do critério de renda foram parar na
raiz junto do deck.

---

## A apresentação atual

| | |
|---|---|
| **Arquivo** | `EDA_Central_IVS_2026-09_rev2.pptx` — 51 slides |
| **O que mudou** | A EDA inteira foi recalculada com `renda_media_sem_extremo` (renda sem o setor `310620005650366`, Belo Horizonte). Os 4 slides novos, logo depois da abertura, dizem o que mudou e o que ficou igual. |
| **1ª rodada** | `historico/2026-08-21_EDA_Central_1a_rodada.pptx` — com a renda completa |
| **Roteiro** | `complementos/Roteiro_EDA_Central_2a_rodada.docx` — fala sugerida slide a slide, o que apontar em cada figura e as perguntas prováveis. Cobre os 51 slides |
| **Recorte** | 104.108 setores urbanos elegíveis, 70 municípios do ELSI-Brasil |
| **Gerada por** | `scripts/gerar_deck_eda_central.js` |
| **Números** | extraídos por `scripts/eda_central_dados.py` das tabelas de `banco_de_dados/eda/` |

**Ela é gerada por script, não editada à mão.** Para atualizar depois de reexecutar a EDA:

```bash
./.venv/bin/python scripts/eda_central_dados.py banco_de_dados/eda/dados_deck.json
node scripts/gerar_deck_eda_central.js docs/Apresentacoes_IVS/historico/2026-08-21_EDA_Central_1a_rodada.pptx
```

Para regerar a **2ª rodada** (renda sem o extremo), a sequência inteira é:

```bash
./.venv/bin/python scripts/auditoria_renda.py --sem-extremo
./.venv/bin/python scripts/eda_atualizada.py
./.venv/bin/python scripts/eda_central_dados.py banco_de_dados/eda/dados_deck_atualizado.json --atualizada
node scripts/gerar_deck_eda_central.js docs/Apresentacoes_IVS/EDA_Central_IVS_2026-09_rev2.pptx banco_de_dados/eda/dados_deck_atualizado.json
```

**É um gerador só para os dois decks.** O que muda é o JSON: `--atualizada` faz cada tabela
ser lida de `banco_de_dados/eda/atualizada/` quando ela existe lá, e da pasta normal quando
não existe — só as tabelas que a renda afeta foram reescritas. O bloco `alteracoes` no JSON
é o que liga os 4 slides de comparação; sem ele, o gerador produz a 1ª rodada como antes.

> **O arquivo da 1ª rodada em `historico/` tem 40 slides, mas o gerador dele produz 47.**
> Ele é anterior às últimas mudanças do gerador e nunca foi regerado. Ficou arquivado
> **como estava**, que é o papel de `historico/` — regerá-lo agora produziria um arquivo
> que nunca existiu naquele dia. Se em algum momento for preciso a versão completa da 1ª
> rodada, o comando acima a reconstrói.

Se editar o `.pptx` à mão, a próxima execução do script sobrescreve a edição. Mudanças
permanentes vão no gerador.

> Por que gerada por script: as apresentações anteriores eram montadas à mão, e a lista do
> que entrava vivia na cabeça de quem montava. Foi assim que o bloco de chefia feminina,
> presente no deck de junho, sumiu do de agosto sem ninguém notar.

---

## `complementos/` — apoio, não são a apresentação

Documentos que acompanham o deck sem serem o deck. Estavam na raiz e confundiam quem
procurava a apresentação.

| Arquivo | O que é | Gerado por |
|---|---|---|
| `Roteiro_EDA_Central_2a_rodada.docx` | **O roteiro em uso.** Fala sugerida slide a slide, o que apontar em cada figura, perguntas prováveis — os 51 slides | à mão, atualizado por `scripts/atualizar_roteiro_2a_rodada.py` |
| `Roteiro_EDA_Central_1a_rodada.docx` / `.pdf` | O mesmo roteiro na versão de 47 slides, guardado como origem da atualização | à mão |
| `Resumo_EDA_Central_2026-08.docx` / `.pdf` | As tabelas e figuras da EDA em texto corrido, com um comentário embaixo de cada uma | `scripts/gerar_resumo_eda_central.py` |
| `Criterio_Outliers_Renda.pptx` / `.pdf` | Abre a regra de classificação de outlier de renda inteira: corte de Tukey por município, os três testes de coerência, os dois diagnósticos que ficam de fora de propósito | `scripts/gerar_deck_criterio_renda.js` e `scripts/gerar_pdf_outliers_renda.py` |

> **O resumo e o critério de renda continuam na 1ª rodada.** O critério diz 66 suspeitos e
> 3.358 setores rastreados; na 2ª rodada são 65 e 3.357, porque o setor de Belo Horizonte
> saiu da coluna de renda. A **regra** que esses documentos descrevem não mudou — só as
> contagens. Os geradores dos dois ainda não aceitam `--atualizada`.

### Por que o roteiro não é gerado

Ele é o único artefato desta pasta escrito à mão, e é assim de propósito: o que ele tem de
valioso não são os números, é o julgamento — quais slides não podem cair se o tempo apertar,
o que dizer em cada um, que pergunta a orientadora provavelmente fará. Isso não sai de
tabela nenhuma.

Por isso a passagem de uma rodada para a outra é feita por
`scripts/atualizar_roteiro_2a_rodada.py`, que renumera os slides, insere as seções dos 4
novos e troca **só** os números que mudaram — cada um lido de
`banco_de_dados/eda/atualizada/`, nenhum digitado no script. O texto do autor sobrevive
palavra por palavra, e o arquivo fica como registro do que foi preciso mexer se houver uma
3ª rodada.

O `.pdf` do roteiro da 2ª rodada ainda não existe: a conversão sai do Word, e esta máquina
não tem LibreOffice para automatizá-la.

---

## Histórico

Do mais recente para o mais antigo. O prefixo é a data do arquivo.

| Arquivo | Slides | O que era | Por que saiu de circulação |
|---|---|---|---|
| `2026-08-21_EDA_Central_1a_rodada.pptx` | 40 | A EDA Central, 1ª rodada — primeira apresentação gerada por script | Superada pela 2ª rodada, com a renda sem o extremo de Belo Horizonte |
| `2026-08-09_Andamento_rev2.pptx` | 30 | Andamento de agosto, revisão 2 | Não cobria chefia feminina, habitação precária, banheiro nem morfologia |
| `2026-08-09_Andamento.pptx` | 29 | Mesma apresentação, revisão 1 | Superada pela rev2 no mesmo dia |
| `2026-08-09_Retomada_e_demandas.pptx` | 25 | Retomada do projeto e as demandas em aberto | Absorvida pelo Andamento |
| `2026-06-18_EDA_Fase3_seis_demandas.pptx` | 29 | EDA da Fase 3 + as **seis demandas de junho** | **Único deck que teve chefia feminina, habitação precária e morfologia** — recuperados na EDA Central |
| `2026-06-15_EDA_Fase3_revisada_V00001.pptx` | 22 | EDA revisada sobre o denominador V00001 | Superada pela versão com demandas, três dias depois |
| `2026-05-30_EDA_completa_corrigida.pptx` | 11 | EDA completa após as correções de maio | Superada pela revisão de junho |
| `2026-05-30_Comparativo_EDA_antiga_vs_nova.pptx` | 16 | Comparativo entre a EDA antiga e a corrigida | Documento de transição; a EDA antiga não existe mais |
| `2026-05-28_Correcoes_commit_2fb2e30.pptx` | 10 | Duas correções metodológicas de um commit específico | Correções já incorporadas |
| `2026-05-22_Revisao_denominador_analfabetismo.pptx` | 13 | A correção do denominador do analfabetismo | Correção já incorporada (`V00901 / (V00900 + V00901)`) |
| `2026-05-15_EDA_inicial_denominador_V01042.pptx` | 32 | A **primeira** EDA, sobre o denominador V01042 | **Metodologia abandonada.** V01042 é contagem de pessoas, não de domicílios — os números deste deck não valem |

> **Atenção à cópia fora do repositório.** Existe um `IVS_Andamento_2026-08_rev2.pptx` em
> `Iniciacao Cientifica/Relatorios e Andamento/` que **não** é o mesmo arquivo do
> `2026-08-09_Andamento_rev2.pptx` acima: tem 27 slides em vez de 30 e foi editado em
> 12/08. Ele passou pelas correções de 24/08 (contagens de teste e de indicadores, universo
> das favelas, o extremo de renda, `CD_TIPO` × `NM_FCU`) e está factualmente alinhado com a
> EDA Central. A versão em `historico/` continua como estava no dia em que foi apresentada,
> que é o papel dela.

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
| `EDA_Central_IVS_2026-08.pptx` | `historico/2026-08-21_EDA_Central_1a_rodada.pptx` |
| `Roteiro_EDA_Central_IVS_2026-08.docx` | `complementos/Roteiro_EDA_Central_1a_rodada.docx` |
| `Resumo_EDA_Central_2026-08.docx` | `complementos/Resumo_EDA_Central_2026-08.docx` |
| `Criterio_Outliers_Renda.pptx` | `complementos/Criterio_Outliers_Renda.pptx` |

A pasta `Versoes_anteriores/` deixou de existir: ela separava três decks antigos enquanto
outros sete, igualmente antigos, ficavam na raiz. Agora todo deck fora de circulação está
em `historico/`.

---

## Onde guardar a próxima apresentação

1. A atual sai da raiz e vai para `historico/`, com o prefixo `AAAA-MM-DD_`.
2. A nova entra na raiz — **sozinha**. Roteiro, resumo e qualquer documento de apoio vão
   para `complementos/`.
3. Acrescente a linha correspondente na tabela do histórico acima, dizendo **por que** ela
   saiu de circulação — é essa coluna que evita que alguém use número velho sem saber.
4. Arquive o deck **como ele estava**. Regerar na hora de arquivar produz um arquivo que
   nunca foi apresentado.
