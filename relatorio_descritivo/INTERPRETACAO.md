# Interpretação do pedido — relatório descritivo do andamento

Gravado em 07/10/2026, na sessão que arquitetou o prompt
`docs/prompts/prompt_relatorio_descritivo_2026-10.md`. **Toda sessão de construção ou de
correção lê este arquivo antes de mexer em qualquer slide.** Se uma correção do Pedro
contradisser algo daqui, vale a correção, e esta página é atualizada na mesma sessão.

## 1. O pedido, nas palavras do Pedro (07/10/2026)

> Minha professora solicitou um relatório do meu andamento no projeto desde que eu peguei
> para atender suas últimas demandas. Venho percebendo que você opta por gerar uma
> apresentação por temas e nunca uma apresentação descritiva. Preciso de uma apresentação em
> formato de relatório descritivo dessa vez para ela comparar meus resultados com os
> resultados dela.
>
> 1 — Se lembre das minhas últimas demandas. 1.1 — Primeira parte da apresentação/relatório
> descritivo: quero que você elenque todas as demandas e como nós cobrimos todas elas.
>
> 2 — [...] Algumas análises descritivas (índice de chefia feminina, índice de envelhecimento,
> índice de canalização de água, índice de moradia precária, moradia com banheiro): percebo
> que você insiste em criar gráficos comparando esses índices e eu não quero isso, por
> exemplo (índice de chefia feminina com índice de envelhecimento). É algo legal para
> acrescentar e enriquecer, mas primeiro precisamos cumprir a demanda descritiva antes de
> comparar com gráficos e tabelas.
>
> Quero que você monte um relatório da versão final do projeto, depois que corrigimos todas
> as últimas demandas, com cada slide sendo estes índices. A primeira parte será essa, mas
> depois vamos falar sobre a análise fatorial, que também será nessa pegada; porém, depois
> de expor toda a descritiva da fatorial, quero expor as coisas que minha professora
> solicitou especificamente da análise fatorial.
>
> Quero uma apresentação completa, porém direta ao ponto, sem enrolação, e que à medida que
> você constrói e me entrega esteja apta a analisar minha análise e corrigir sem alucinar.
> Salve os processos de construção e interpretação do que eu peço para que você não se perca
> nas correções que eu te encaminhar.
>
> [Este modelo ajuda] a escolhermos claramente um gráfico/tabela ou uma análise que geramos e
> que é pertinente levar para o artigo. Descreva também na apresentação o que contornamos a
> partir da última demanda para cumprir ela. Apresentação em PowerPoint.

## 2. Requisitos, numerados (cada slide e cada correção cita o R que atende)

| R | Requisito | Como o prompt atende |
|---|---|---|
| R1 | Formato **relatório descritivo**, não por temas: uma unidade por slide (uma demanda, um indicador, uma medida da fatorial), com o mesmo layout dentro de cada parte | §2 e §2.6 do prompt |
| R2 | Parte 1: **todas as demandas** da orientadora e **como cada uma foi coberta** | Parte DM |
| R3 | **O que contornamos** para cumprir as demandas, descrito na apresentação | caixa "O que contornamos" em cada DM e a tabela DM14 |
| R4 | Parte 2: **um indicador por slide**, só descritiva desse indicador | Parte DS |
| R5 | **Nenhum gráfico ou tabela comparando indicadores entre si** na descritiva (ex.: chefia feminina × envelhecimento) | §0.2, regra 7, e "O que nunca fazer" |
| R6 | **Versão atual**, depois de cumpridas as demandas de setembro | a base e as tabelas da `00_referencia` (§1) |
| R7 | Parte 3: **descritiva da fatorial**, uma medida por slide | Parte FA |
| R8 | Parte 4: **o que a orientadora pediu especificamente da fatorial**, depois da descritiva | Parte FP |
| R9 | **Completa, mas direta**: sem slides de transição, sem frases de enchimento | §2.6 |
| R10 | Números **comparáveis com os da orientadora**: estatísticas-padrão, base declarada, definição com códigos V, números com precisão no anexo | §2.6 e anexo xlsx |
| R11 | **Entrega por partes** e **correção sem alucinar** | lotes (§4) e protocolo de correção (§5) |
| R12 | **Processo salvo** (construção, interpretação, correções) | `INTERPRETACAO.md`, `CONSTRUCAO.md`, `CORRECOES.md`, `dados/manifesto.csv` |
| R13 | Facilitar a **escolha do que vai para o artigo** | ID estável em todo slide; aba `Indice_slides` do anexo, com colunas de seleção |
| R14 | Formato **PowerPoint** | `.pptx` gerado por script |
| R15 | (07/10) **Tabelas editáveis** no PowerPoint, para alterações pontuais do Pedro | tabelas nativas; `scripts/comparar_edicoes_relatorio.py` leva as edições à origem antes de regerar |
| R16 | (07/10) **Seguir os lotes 2 a 5 sem parar** | executado em sequência, com verificação e folha de contato no fim |
| R18 | (08/10, C-04) **"Tema" = indicador.** Cada indicador ganha um segundo slide (região, municípios, FCU), sempre sozinho. **As correlações entram num bloco próprio (DC), depois dos indicadores** — a regra R5 continua valendo para os slides DS | DSxx-2, DC00–DC07 |
| R19 | (09/10, C-09) **Apresentação reserva da reunião remota (v4), só para o Pedro.** Depois de cada slide da v3, um slide de apoio com o que é o conteúdo, as perguntas prováveis da orientadora com resposta e de onde vem, e os números de cor; P00 (perguntas gerais) e glossário. Prompt: `docs/prompts/prompt_apoio_reuniao_v4_2026-10.md` | apoio.json, v4_APOIO |
| R17 | (08/10, tirado das edições do Pedro, C-03) **Slide sem marcas de processo**: nada de "(redação do registro)", "estado: …", nome de script ou função, pergunta pendente, "proposta, não escolhida" repetido em cada slide; descrições de cenário curtas; nenhum slide só de processo (curadoria, desdobramentos, perguntas, aviso de anexo) | vale para todo slide novo; a parte 5 já saiu assim |

## 3. Pontos com mais de uma leitura — o padrão adotado

| # | Ponto | Leitura adotada (padrão) | Outra leitura possível | Estado |
|---|---|---|---|---|
| L1 | "Últimas demandas" | As **11 demandas de setembro** (`docs/prompts/estado_demandas_2026-09.md`, linhas 16–26). Os 9 itens do NB05 entram como desdobramentos, marcados como tal | Os itens do NB05 também como demandas dela | A CONFERIR com o Pedro no piloto |
| L2 | "Versão final" na **descritiva** | Base atual: urbanos com `Dados_sig = OK`, **104.108 setores**, indicadores do módulo corrigido | — | sem ambiguidade |
| L3 | "Versão final" na **fatorial** (FA02 resolvido: a correlação é de Spearman, `fatorial.py:394`) | A **referência proposta do NB05** (`original · lixo_sem · banheiro_graduado · promax · 60_40 · municipal`, 73.878 setores), sempre chamada de *proposta*, nunca de *final* | A fatorial do NB04 (IVS-7, 87.545 setores), que pode ser a que a orientadora replicou | **Perguntar ao Pedro qual ela rodou**. Se for a do NB04, a Parte FA troca de fonte (`nb04_*.csv`) |
| L4 | Recortes por município e por região | Ficam **só no anexo xlsx**. No slide, só o indicador nos 70 municípios juntos | Um segundo slide por indicador, por município | padrão até o Pedro pedir |
| L5 | As três rendas | Três slides, um por versão; nenhuma tabela pondo as três lado a lado na Parte DS. O efeito da troca fica na Parte FP (demanda 1) | Um slide só com as três | padrão |
| L6 | Redação das demandas | A do registro (`estado_demandas_2026-09.md`), marcada como "redação do registro" | O texto original da orientadora | se o Pedro colar o texto dela, ele substitui |
| L7 | "Interpretação" nos slides | Frases-modelo **factuais** com os números do slide; interpretação só com documento do projeto citado, senão uma caixa "[Pedro: interpretar]" | Texto interpretativo livre | padrão (é o que evita alucinação) |

## 4. Ideias do brainstorm que ficaram de fora (para depois da descritiva)

Pedro: "é algo legal para acrescentar e enriquecer, mas primeiro precisamos cumprir a
demanda descritiva". Ficam registradas para não se perderem, **e não entram neste relatório**:
- os cruzamentos entre indicadores (correlações, dispersões, chefia feminina × envelhecimento);
- os boxplots e as densidades por região, que já existem em `analises_exploratorias/00_referencia/figuras/`;
- as tipologias, a desigualdade interna e a população em risco das versões D e E;
- a comparação ELSI × Brasil (A6).
