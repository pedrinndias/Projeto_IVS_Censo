# Análise fatorial no Projeto IVS — por onde começar

Índice do material sobre a etapa de análise fatorial (Notebook 04), que é a única etapa
central ainda pendente do projeto. **Comece por aqui.**

**Estado em 16/09/2026:** estudo e planejamento concluídos e versionados. **Implementação
não iniciada.**

---

## Se você tem 5 minutos

Leia a §4 de [`Analise_Fatorial_Enap2019_Guia_de_Leitura.md`](Analise_Fatorial_Enap2019_Guia_de_Leitura.md)
— "As cinco revisões que a leitura obriga". É a lista do que muda no projeto por causa
do livro da Enap.

## Se você vai implementar

Abra [`prompt_nb04_analise_fatorial.md`](../prompts/prompt_nb04_analise_fatorial.md) e siga.
Ele diz o que ler, em que ordem, o que construir e com quais skills.

## Se você vai apresentar para a orientadora

Os dois PDFs diagramados, e a Parte 4b do prompt, que gera o deck.

---

## Os documentos

| Arquivo | O que é | Quando usar |
|---|---|---|
| **[`Analise_Fatorial_LEIAME.md`](Analise_Fatorial_LEIAME.md)** | Este índice | Para achar o resto |
| [`Analise_Fatorial_Enap2019_Guia_de_Leitura.md`](Analise_Fatorial_Enap2019_Guia_de_Leitura.md) | **O estudo do livro da Enap**, seção por seção, com os números do projeto ao lado de cada regra. Traz as cinco revisões que a leitura obriga (§4) e os cinco limites do livro diante do projeto (§5) | Ao ler o livro; ao justificar uma decisão metodológica |
| [`Analise_Fatorial_NB04_Plano_de_Implementacao.md`](Analise_Fatorial_NB04_Plano_de_Implementacao.md) | **As 16 ideias** com custo e veredito, a arquitetura em 10 blocos, os resultados esperados e a prioridade se só der para fazer três | Ao planejar o trabalho; ao decidir o que entra no escopo |
| [`prompt_nb04_analise_fatorial.md`](../prompts/prompt_nb04_analise_fatorial.md) | **O prompt** para colar numa sessão do Claude Code, com as skills por fase | Ao começar a implementar |
| [`Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md`](Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md) | A análise **já rodada** nos dados, interpretada contra Figueiredo & Silva (2010). Checklist de 15 passos com status | Para saber o que já foi medido e o que ele significa |

### Versões em PDF

Mesma substância dos `.md`, diagramadas para leitura impressa e para a orientadora.
Para uma sessão de Claude Code, prefira os `.md` — são greppáveis.

- [`Guia_Leitura_Analise_Fatorial_Enap2019.pdf`](Guia_Leitura_Analise_Fatorial_Enap2019.pdf)
- [`Implementacao_Fatorial_NB04_Brainstorm_e_Prompt.pdf`](Implementacao_Fatorial_NB04_Brainstorm_e_Prompt.pdf)

As fontes que os geram estão em [`fontes_pdf/`](fontes_pdf) — os PDFs são **gerados**,
não editados à mão. Mudanças permanentes vão nas fontes.

---

## Os dados e o código

| Onde | O que é |
|---|---|
| `scripts/diagnostico_fatorial.py` | 219 linhas em numpy puro: KMO, MSA por matriz anti-imagem, Bartlett, autovalores, análise paralela de Horn, ACP e Varimax. **É a base do Notebook 04, não um rascunho.** |
| `banco_de_dados/eda/fatorial/` | 19 CSVs com seis cenários já calculados. `resumo_adequabilidade.csv` é a referência de conferência. |
| `banco_de_dados/entrega_orientadora/*.db` | SQLite versionado, tabela `setores_censitarios`, com as 7 variáveis calculadas. O NB04 roda sem os 2,4 GB do Censo. |
| `src/ivs_censo/indicadores.py` | Definição canônica dos indicadores. O NB04 importa daqui. |

**O livro em si não está versionado** (é material de terceiros). Anexe o PDF à sessão
quando precisar conferir uma passagem.

---

## O estado da questão, em cinco linhas

A base **é adequada** à análise fatorial (KMO 0,783; Bartlett p ≈ 0; 57,1% dos
coeficientes acima de 0,30). O indicador de **lixo forma um fator só dele** e não pertence
ao construto. Sem ele, a solução explica **70,0%** da variância com dois fatores e os
pesos empíricos dão **65/35**, contra os 60/40 da literatura — convergência, não conflito.
Falta decidir a **rotação** (o livro desaconselha a Varimax que foi usada), calcular os
**escores**, e **validar** o índice contra os setores de favela.

---

## As decisões em aberto

Quatro são da orientadora, uma é técnica e uma é conceitual.

| # | Decisão | Onde está discutida | Status |
|---|---|---|---|
| 1 | Critério dos pesos: empíricos ou 60/40 da literatura | Guia §4.3 do doc. Figueiredo | Convergem (65/35 × 60/40) — decisão facilitada |
| 2 | Destino do indicador de lixo | Guia §4.1 do doc. Figueiredo | Evidência forte para retirar do índice |
| 3 | Política do sigilo no analfabetismo | Plano, ideia B4 | Estrutura não muda; magnitude a medir |
| 4 | Um fator ou dois | Guia de leitura §3.F | Kaiser e Horn dizem 1; teoria diz 2 |
| 5 | Rotação ortogonal ou oblíqua | Guia de leitura §3.H | **Recomendação: oblíqua** (livro p. 38) |
| 6 | O IVS é construto reflexivo ou índice formativo? | Guia de leitura §5.1 · Plano §4 | **Em aberto.** Objeção séria, de parecer único não revisado — precisa de literatura e decisão da orientação |

---

*Mantido junto com `docs/MANUAL_DO_PROJETO.md`, que é o mapa geral do repositório. Este
índice cobre apenas a etapa de análise fatorial.*
