# Prompt: versão 4 do relatório descritivo, a apresentação reserva da reunião

Data: 09/10/2026. Executor: Sonnet (receita pronta); a redação das respostas de método passa por Opus.

## 1. O pedido (palavras do Pedro)

> "Minha reunião será de forma remota, quero preparar uma apresentação reserva que contenha coisas a
> mais no slide para me explicar para me auxiliar em possíveis perguntas que minha professora
> orientadora possa fazer. Quero uma versão 4 da apresentação/relatório descritivo que em CADA slide
> tenha possíveis perguntas e suas respectivas respostas que minha professora orientadora possa
> fazer e uma explicação da matéria/conteúdo tratado no slide, exemplo, em slides de análise
> fatorial, o que seria análise fatorial, o que seria KMO, AUC, etc."

**Leitura.** A v3 é o que a orientadora vê, compartilhado na tela. A v4 é só do Pedro: fica aberta
em outra tela (ou no tablet, em PDF) e serve de cola. **A v3 não muda.**

## 2. Decisões (o padrão vale até o Pedro mudar)

| # | Decisão | Padrão |
|---|---|---|
| D1 | Onde fica o apoio | Um **slide de apoio logo depois de cada slide** da v3, para os 140, o que dá 280 slides na mesma ordem. O mesmo texto vai também nas **notas** do slide original, para quem usar o Modo de Apresentador. |
| D2 | Base | A `…_v3.pptx` **com o DS16 corrigido** ("Entra na referência proposta?" = "Sim, como renda invertida"; ver §9). Se a v3 tiver sido editada à mão (hash diferente do registrado), parte da editada. |
| D3 | Voz | Primeira pessoa do Pedro ("eu rodei", "eu li"), em frases curtas para falar em voz alta. Sem jargão que ele não consiga explicar. |
| D4 | Marca | Faixa no topo de todo slide de apoio, "APOIO · NÃO COMPARTILHAR", em fundo de outra cor. Os arquivos levam `_APOIO` no nome, para não serem enviados por engano. |
| D5 | Extras | Duas seções novas: **P00 Perguntas gerais** (no início: andamento, prazos, o que falta, uso de ferramentas) e **G Glossário** (no fim, um termo por bloco). |
| D6 | Saída | `relatorio_descritivo/Relatorio_Descritivo_IVS_2026-10_v4_APOIO.pptx` e o `.pdf` correspondente. |

## 3. O slide de apoio (um por slide da v3)

Ocupa o slide inteiro, em três blocos e em fonte de pelo menos 11 pt. Se não couber, corta o
excedente; não diminui a fonte.

1. **O que é** (máximo 5 linhas). Explica o conteúdo do slide anterior como se fosse para um
   colega de outra área: o conceito (por exemplo, "KMO mede se as variáveis têm correlação
   suficiente para a fatorial; vai de 0 a 1; acima de 0,70 é aceitável") e o que o slide mostra.
   Termo técnico novo só com uma frase de definição; o detalhe vai para o glossário (G).
2. **Perguntas prováveis** (2 a 4). Cada uma com:
   - **P:** a pergunta como a orientadora faria;
   - **R:** a resposta em até 3 linhas, com o número exato do slide quando houver;
   - **De onde:** uma linha curta (tabela, arquivo de resultado ou leitura com página) para o Pedro
     conferir na hora. Esta linha vai só para as notas, e não para o slide de apoio, se o slide
     ficar cheio.
3. **Ter na ponta da língua** (3 a 5 itens). Os números e nomes do slide anterior que ele deve
   saber sem olhar: n, KMO, pesos, quantos saem e por quê.

Os tipos de pergunta a cobrir em cada parte estão no §5.

## 4. Fontes permitidas: nada inventado

A ordem é de precedência. Toda resposta tem de sair de uma destas fontes, e a linha "De onde" diz
qual.

1. Números: o texto e as tabelas do próprio slide da v3, `relatorio_descritivo/dados/numeros.json`,
   `versoes_fatorial/dados/numeros.json` e os CSVs de `banco_de_dados/eda/` e
   `analises_exploratorias/00_referencia/tabelas/`. **Nenhum número digitado à mão.** O script lê o
   número da fonte.
2. Por que cada coisa foi feita assim: `relatorio_descritivo/INTERPRETACAO.md`, `CORRECOES.md`,
   `relatorio_descritivo/dados/notas_fontes_v2.md`, `docs/prompts/estado_demandas_2026-09.md`,
   `docs/prompts/estado_nb05_2026-09.md`, `GUIA_DO_PROJETO.md` e `docs/relatorios/`.
3. Conceitos de método:
   - as leituras **concluídas** do Pedro na planilha
     `Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx` (abas Artigos e Anotacoes,
     com página): Matos 2019 (Enap), Figueiredo Filho 2010, IVS-BH 2012 e nota metodológica, IBGE
     FCU 2024, Allik 2020, Gioia 2020, Lima-Costa 2003;
   - os guias em `docs/metodologia/`.
4. Conceito sem leitura concluída (Horn 1965, promax de Hendrickson & White 1964, Spearman,
   AUC/ROC, matriz padrão × estrutura, Nardo/OECD 2008):
   - a explicação geral, de livro-texto, é permitida, marcada **[leitura pendente: ARTxxx]**;
   - essa marca aparece **só nas notas**, para o Pedro saber o que estudar antes, e não no slide.
5. Sem fonte não há resposta inventada. A resposta sugerida é honesta: "Isso eu não testei; posso
   rodar e te mando" ou "Essa escolha ficou como proposta; queria decidir com você". Essas
   perguntas entram na lista **A CONFERIR** do ESTADO.

Decisões de método nunca aparecem como tomadas: a referência do NB05 é "proposta", e a escolha é
dela. A resposta modelo é: "eu propus X por tal motivo; você prefere Y?".

## 5. Perguntas a cobrir, por parte (lista mínima; acrescentar o que o slide pedir)

- **A01–A03, P00 (abertura e geral):**
  - em que pé está;
  - o que falta e qual o próximo passo;
  - quanto tempo levou;
  - como conferiu os números contra os dela;
  - que ferramentas usou: scripts em Python e a resposta honesta sobre o uso de IA, que o Pedro
    escreve ou aprova.
- **DM (demandas):**
  - por que leu o pedido desse jeito;
  - por que não fez de outro jeito;
  - o que o contorno muda no resultado;
  - se a demanda está mesmo concluída.
- **DS (cada indicador):**
  - o que mede e por que este numerador e este denominador;
  - por que tantos zeros e o que é o sigilo;
  - por que há faltantes;
  - o que significa a assimetria ou o CV;
  - por que entra ou não no IVS-7 e na referência;
  - as diferenças por região e entre FCU e demais setores (DS-2).
- **DC (correlações):**
  - por que Spearman e não Pearson;
  - o que é correlação alta e o que fazer com ela (redundância);
  - por que Sem banheiro × Banheiro graduado dá 1,000.
- **FA (fatorial da referência):**
  - o que é a análise fatorial e para que serve no índice;
  - KMO, MSA, Bartlett, comunalidade;
  - Kaiser e Horn: quantos fatores;
  - carga;
  - rotação sem, Varimax e promax; matriz padrão × estrutura; Φ;
  - como as cargas viram pesos e por que 60/40;
  - normalização municipal;
  - as faixas pela regra do IVS-BH e por quartis;
  - validação contra FCU, AUC e por que a mediana municipal.
- **FC/FP (cenários e demandas da fatorial):**
  - o que é cada cenário e por que perde setores;
  - por que o lixo forma fator próprio;
  - por que 2 fatores se Kaiser e Horn dão 4 no S6;
  - por que a renda sozinha vence o índice na AUC (FP13) e o que isso implica.
- **VP (108 versões):**
  - por que 108;
  - o que é a amostra comum;
  - por que só 24 passam;
  - qual escolher (resposta: "não escolhi; o VP14 só ordena pelos critérios; a decisão é sua");
  - o que é estabilidade e parcimônia;
  - por que o desempate é o IVS-BH 2012.

Para cada **G** (glossário, um slide por 2 ou 3 termos), use esta lista de termos:

- setor censitário, Dados_sig e sigilo, FCU;
- proporção × razão, complemento, exclusão por lista, imputação pela mediana;
- assimetria, CV, P10/P90;
- Spearman, Pearson;
- análise fatorial, componente × fator, autovalor, Kaiser, Horn;
- KMO, MSA, Bartlett;
- comunalidade, carga, rotação, Varimax, promax, Φ, matriz padrão, matriz estrutura;
- peso, normalização min-max, normalização municipal, faixas, quartil;
- ROC, AUC, AUC municipal;
- formativo × reflexivo.

## 6. Arquivos e passos

1. `relatorio_descritivo/apoio/apoio.json`:
   - o conteúdo, por ID de slide: `o_que_e`, `perguntas[{p, r, de_onde}]`, `ponta_da_lingua[]`,
     `leitura_pendente[]`;
   - os números entram como **referência** (`{"num": "numeros.json:FA03:kmo"}`), resolvida pelo
     script, e não como texto.
2. `scripts/montar_apoio_relatorio.py` (python-pptx, sobre a v3; nunca regera nem altera a v3):
   - insere o slide de apoio depois de cada original;
   - escreve o mesmo texto nas notas do original;
   - acrescenta P00 e G;
   - grava a v4 e o PDF (LibreOffice).
3. `scripts/verificar_apoio_relatorio.py`:
   - os 140 originais estão idênticos à v3 (4.670 células de tabela e o texto);
   - cada original tem exatamente um apoio logo depois;
   - cada apoio tem de 2 a 4 perguntas, cada uma com "De onde";
   - todo número do apoio existe na fonte citada;
   - todo termo do glossário que aparece num apoio tem verbete em G;
   - não aparece "a escolha é" nem "melhor versão" como decisão;
   - nenhuma fonte abaixo de 11 pt;
   - nenhum texto saindo do slide (altura estimada);
   - folha de contato de 12 páginas.

## 7. Lotes e paradas

Cada lote termina com o verificador verde e um relatório de no máximo 15 linhas.

1. **Lote 1 (amostra para aprovar layout e tom):** P00, A01–A03, DM00–DM14, FA03 (KMO), FA14 (AUC)
   e 6 verbetes do glossário. **Para e mostra a folha de contato.**
2. Lote 2: DS e DS-2 (62 slides). Lote 3: DC e FA. Lote 4: FC, FP e VP. Lote 5: glossário completo.
   Depois da aprovação do lote 1 seguem sem parar, se o Pedro disser "sem parar".
3. No fim, o PDF e a lista **A CONFERIR**: perguntas sem fonte e leituras pendentes que o Pedro
   precisa fazer antes da reunião.

## 8. Proibido

- Mexer na v3, nos números ou nos decks editados à mão: grava sempre arquivo novo.
- Abrir subagentes, ligar hook, cron ou watcher, ou invocar skill sem pedido.
- Inventar fonte, página, número ou conclusão. Pôr na boca do Pedro uma leitura que ele não fez,
  sem a marca [leitura pendente].
- Vocabulário proibido: "vale destacar", "é importante notar", "em suma", "robusto", "abrangente".

## 9. Antes de começar

- Corrigir o DS16 na v3, se o Pedro aprovar: o slide diz "Entra na referência proposta? Não", e
  a referência usa a renda média invertida (`renda_inv` na T20).
- Corrigir também a origem em `scripts/dados_relatorio_descritivo.py`: a REFERENCIA não mapeia
  `renda_inv` → `renda_media`.
- Gerar de novo a v3 e o PDF, e registrar como C-08.
- Registrar este pedido em `relatorio_descritivo/INTERPRETACAO.md` (R19) e o andamento em
  `ESTADO.md`.
