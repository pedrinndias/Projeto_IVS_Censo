# Correções do relatório descritivo

Uma entrada por pedido do Pedro, com as palavras dele. Formato e protocolo: seção 5 do prompt
`docs/prompts/prompt_relatorio_descritivo_2026-10.md`.

## C-01 — 07/10/2026 — slides DS (todos; no deck: DS20, DS31)
Pedido (palavras do Pedro): "Layout aprovado, pode seguir com o lote 1, apenas insira em qual
arquivo esta localizado os indicadores, confira na tabela de gerenciamento"
Leitura: a "tabela de gerenciamento" é a aba Indicadores de
`Relatorios e Andamento/gerenciamento_artigos_cientificos_IC.xlsx` (gerada por
`scripts/planilha_indicadores_ic.py`). Cada slide DS ganha duas linhas em "Como é calculado":
"Arquivo do Censo" (coluna "Arquivo do Censo de origem") e "Calculado em" (coluna "Calculado
em"); a planilha entra na linha Fonte.
Mudança: `scripts/dados_relatorio_descritivo.py` — `GER` (leitura da aba) e `ds()` (duas
linhas na `definicao`); `scripts/verificar_relatorio_descritivo.py` — item 8 novo.
Verificação: item 8 — arquivo de origem igual ao do Quadro em 28 de 28 indicadores; a linha
"Calculado em" cita o indicador nos 31. Verificador verde (itens 1–6 e 8) · deck v1.

## C-02 — 07/10/2026 — todos os slides; texto também em A02, A03, DM05, DS34, FA02; Z01 removido
Pedido (palavras do Pedro): "Tire as fontes, minha professora nao vai entender, apenas eu"
Leitura: a linha "Fonte:" do pé de cada slide sai; as fontes continuam nas notas do
apresentador (que só o Pedro usa), no `manifesto.csv` e na aba Indice_slides do anexo. Pelo
mesmo motivo saem: o slide Z01 (lista de arquivos), o bloco "Fonte." do A02 e os caminhos de
arquivo ou nomes de função em frase visível (DM05, DS34, FA02). Mantidos "Arquivo do Censo" e
"Calculado em" nos DS, pedidos na C-01 — A CONFERIR com o Pedro se saem também.
Mudança: `scripts/gerar_relatorio_descritivo.js` — sem chamada de `procedencia`;
`scripts/dados_relatorio_descritivo.py` — `SLIDES` sem Z01, textos de A02/A03/DM05/DS34/FA02,
`ALTERADOS`; `scripts/verificar_relatorio_descritivo.py` — item 1 exige ID no slide, nenhuma
"Fonte:" no slide e "Fontes:" nas notas.
Verificação: verificador verde (itens 1–6 e 8) · deck v3, 86 slides.

## C-03 — 08/10/2026 — análise das edições à mão do Pedro + parte 5 (as 108 versões)
Pedido (palavras do Pedro): "Analise as alteração que eu fiz no relatorio dectirivo e adcione esta
apresentacao das 108 versoes na apresentacao do relatorio descritivo"
Leitura: (1) comparar o deck editado (82 slides, sha c46722c2…) com `dados/ultimo_gerado.pptx` em
texto, tabelas, notas, figuras e posição; (2) anexar o deck principal das 108 versões como parte 5,
entre FP13 e Z02, SEM regerar o relatório (regerar apagaria as edições) e sem gravar por cima do
arquivo do Pedro.
O que o Pedro mudou (nada levado à origem ainda):
- apagou DM05 (separar útil × inútil), DM13 (desdobramentos do NB05), DM15 (perguntas à orientadora)
  e DS34 (aviso do anexo);
- tirou "(redação do registro)" e o subtítulo "Redação do registro: … · estado: …" dos DM;
- tirou caixas com nome de script (DM03 e DM04 "O que foi feito"; DM03 "O que contornamos");
- tirou observações de processo: "(a demanda 11 já pede isso)", "(pergunta 6, sem confirmação
  registrada)", "a versão graduada … ficou em aberto na época", "a pedido da orientadora em 01/09/2026";
- encurtou descrições de cenário nas tabelas do DM08 e DM09 (sem "(referência, reproduz o NB04)" e
  "("tudo isso")"); "Fatorial de tudo isso" → "Fatorial de tudo";
- DM14: esvaziou as linhas das demandas 4 e 8 e encurtou o texto das 1 e 9;
- tirou os subtítulos do DM14, do DS02 e o selo "proposta, não escolhida" do FA00 ao FA06;
- DS01: figura do funil movida para baixo da tabela e legenda reduzida.
Pontos que parecem acidentais (avisados ao Pedro, não alterados):
- DM02: "só no setor excluído a (310620005650366, …" — sobrou o "a" da frase cortada;
- DM14: as linhas 4 e 8 ficaram vazias, mas continuam na tabela;
- FA07–FA16 ainda têm o selo que saiu do FA00–FA06;
- Z02 ainda cita "as 9 perguntas do DM15", slide apagado;
- A03 ainda lista DM00–DM15 e DS00–DS34;
- os números impressos no pé estavam errados em 74 slides depois das exclusões.
Mudança: `scripts/anexar_versoes_ao_relatorio.py` (novo) copia os 15 slides de
`versoes_fatorial/dados/parte_relatorio.pptx` para dentro do deck editado, acrescenta a linha 5 e
"Cinco partes" no A03 e renumera o pé de todos os slides; grava
`Relatorio_Descritivo_IVS_2026-10_com_108_versoes.pptx` (97 slides). A parte segue o estilo das
edições: sem capa, sem "proposta, não escolhida", sem slide "O que está em aberto".
Verificação: deck do Pedro com o mesmo sha antes e depois; folha de contato do A03, da parte e do Z02;
verificador das 108 versões verde.

## C-04 — 08/10/2026 — correlações, mais gráficos por indicador e os cenários da fatorial
Pedido (palavras do Pedro, colado na mensagem com o deck `…_com_108_versoes.pptx` editado): "Faltou
inserir as matrizes de correção, na Análise Exploratória / Faltou descrever os cenários trabalhos na
análise fatorial, quais setores incluídos em cada cenário / Mais gráficos descritivos de cada tema da
Análise Exploratória de dados". Depois: "Tema que eu me referia é tipo: "Lixo inadequado", ...,
"Banheiro graduado" essas coisas".
Leitura: tema = indicador. (1) Um segundo slide por indicador (DSxx-2): o indicador sozinho por região,
pelos 70 municípios e em FCU × demais; com metade ou mais dos setores em zero, % de setores com valor
> 0 e média em vez de caixa e mediana. (2) Bloco de correlações de Spearman no fim da Parte 2 (DC00–DC07:
componentes do IVS-7 em tabela e mapa, um mapa por dimensão, os 31 juntos); Pearson só no anexo.
(3) Um slide por cenário da fatorial ampliada no começo da Parte 4 (FC01–FC08: variáveis, faltantes de
cada uma no recorte, setores no cenário e por região) e as variantes (FC09).
Edições do Pedro nesta rodada (deck `…_com_108_versoes.pptx`, não levadas à origem): apagou A02, A03,
FP10, FP12 e Z02; tirou o rodapé do A01, os subtítulos "Redação do registro" do DM02 e FP01–FP13 e a
frase da V023 no VP02; acrescentou os critérios no VP05; FP00 virou "Demandas da da fatorial" (avisado).
Mudança: `dados_relatorio_descritivo.py` — `ds_extra`, `dc`, `dc_slides`, `fc_slides`, `SLIDES` e
`NOVOS_C04`, abas Correlacao_Spearman e Correlacao_Pearson no anexo, `dados/insercoes_c04.json`;
`gerar_relatorio_descritivo.js` — layouts DSX, figuraLarga e FC, encaixe de figura pelo PNG, cópia
de referência só quando grava o principal; `verificar_relatorio_descritivo.py` — aceita o caminho do
deck; `scripts/inserir_no_relatorio.py` (novo) — copia os 48 slides novos para dentro do deck editado,
cada um depois do seu antecessor na origem, e renumera o pé.
Saída: `Relatorio_Descritivo_IVS_2026-10_com_graficos_e_cenarios.pptx` (92 + 48 = 140 slides). O deck
editado `…_com_108_versoes.pptx` ficou intocado (sha 03b0909d…).
Verificação: deck completo gerado (134 slides, v4) verde nos itens 1–6 e 8; o FC confere o n de cada
cenário com `cenarios.csv` antes de gravar; folha de contato do DS03-2, DS13-2, DS22-2, DS33-2, DC00,
DC01, DC03, DC06, DC07, FC01, FC07, FC09.
Observação: `Relatorio_Descritivo_IVS_2026-10.pptx` foi gravado às 14:08:26 de 08/10 pelo PowerPoint
(o arquivo de trava `~$` sumiu na mesma hora); nenhum script desta rodada escreveu nele.

## C-05 — 08/10/2026 — o que faltava do plano dos itens 1 e 2
Pedido (palavras do Pedro, com o plano colado): "Isso pode fazer todas essas melhorias".
Leitura: os dois itens já estavam na C-04; faltavam (a) "a tabela ao lado [do mapa] quando couber" nos
temas e (b) "quantos saem em relação ao S0, e por causa de qual variável" nos cenários.
Mudança: `dc()` — tabela de Spearman ao lado do mapa nos temas com até 7 indicadores (DC04
socioeconômica, DC05 morfologia, DC06 demografia; saneamento, com 11, fica só no mapa), colunas
numeradas; `fc_slides()` — tabela "Sai do S0 por causa de": setores do S0 sem cada variável nova e
quantos saem só por ela, com o total; o script para se o total não bater com `perdidos_vs_S0`;
layout FC com a primeira tabela à esquerda e as outras empilhadas à direita. Deck completo v5.
Saída: `Relatorio_Descritivo_IVS_2026-10_com_graficos_e_cenarios.pptx` refeito a partir do deck
editado `…_com_108_versoes.pptx` (intocado); o anterior (14:20) não tinha edição do Pedro.
Verificação: verificador verde no deck completo (134 slides); total de saídas = `perdidos_vs_S0` em
todos os cenários; folha de contato do DC04, DC05, FC02 e FC07.

## C-06 — 08/10/2026 — versão 2: texto e voz, sem mudar número (37 regras, 51 slides tocados)
Pedido (palavras do Pedro): "Faca um arquivo versao 2 com todas as correcoes" — as do diagnóstico
de indícios de texto gerado (humanizer + conselho), veredito "cortes dirigidos, sem reescrever a voz".
Mudança (`scripts/revisar_texto_relatorio.py`, sobre o deck entregue, sem regerar):
- a orientadora sai da terceira pessoa (A01 "com os seus resultados"; DM09; DM10; FA09; FP11);
  selo "proposta, não escolhida; a escolha é da orientadora" removido dos FA07–FA16;
- bastidores fora do slide: "Calculado em src/…, linha N" vai para as notas (31 DS); saem
  cargas.csv, pesos.csv, fa_plano_s6.png, perdidos_vs_S0, TODOS_INDICADORES, lixo_muda, "NB01, sem
  gravar o notebook", "posicionador de rótulos", "min_count=1", "redação do registro", "Registro:",
  "renda sem_extremo/mediana_mun" nas descrições;
- frases quebradas: mediana zero nos 15 DS ("Metade… até 0,00%"), FP13 "em 0" → "Em nenhuma das
  192", "Menor" → "Correlação negativa mais forte" (6), FC06 "saem 0", "indicam 2 e 2" (4), FA05;
- restos de edição: "da da" (FP00), "excluído a (" (DM02), 2 linhas vazias e frase cortada (DM14);
- travessão nos títulos "Demanda N —" (19) e nas legendas DS-2 (15); legendas "Figura N —" mantidas.
Mantido: "Arquivo do Censo" nos DS (pedido na C-01); NB04/NB05; nomes de coluna do banco
(renda_media, Dados_sig); moldes "O que mostra." e o "nós" do Pedro.
Saída: `Relatorio_Descritivo_IVS_2026-10_v2.pptx` (140 slides); o deck de entrada fica intocado.
Verificação: toda regra bate com a contagem esperada; números por slide antes × depois: só saem
números de código, linha, NB, "0,00%" das frases de mediana zero e repetições ("2 e 2"); entra só
"V00237" (DM07, DM14); folha de contato de 9 slides.
Em aberto: DM01 ainda aponta a demanda 4 para o DM05, que o Pedro apagou.

## C-07 — 08/10/2026 — versão 3 e PDF: o arquivo que vai para a orientadora
Pedido (palavras do Pedro): "Faca a versao 3 com todas as correcoes e exporte o PDF" — as do segundo
diagnóstico (humanizer + conselho) sobre a v2.
Mudança (`scripts/preparar_entrega_relatorio.py`, sobre a v2, sem regerar):
- notas do apresentador dos 140 slides guardadas em `dados/notas_fontes_v2.md` e esvaziadas no deck
  (tinham "Requisitos: R…", "Gerado por ds() em scripts/…", caminhos de docs/prompts e títulos antigos);
- metadados: assunto e empresa sem "PptxGenJS"; título sem travessão; autor Pedro Dias Soares;
- texto alternativo das 77 figuras: a legenda (ou o título do slide) no lugar do caminho /Users/…;
- DS23: "um em cada quatro tem mais de 100,00%" → "Pelo menos metade dos setores tem 100,00%; o P10
  é 98,40%, e 0,01% dos setores têm valor zero.";
- PDF pelo LibreOffice (Cambria → Caladea, de mesmas medidas), metadados do PDF com título e autor.
Saída: `Relatorio_Descritivo_IVS_2026-10_v3.pptx` e `…_v3.pdf` (140 páginas); a v2 fica intocada.
Verificação: 4.670 células de tabela iguais à v2; texto igual em todos os slides menos o DS23; zero
ocorrências de PptxGenJS, /Users/, docs/, scripts/, Requisitos, "orientadora" e "Gerado por" no pacote
e no PDF; folha de contato de 9 páginas do PDF.
Não mexido (decisão do conselho): moldes "O que mostra.", "nós", vocabulário técnico; nomes internos
de forma ("Text 12"), que o PowerPoint não mostra no slide.

## C-08 — 09/10/2026 — DS16: a renda média entra na referência (invertida)
Achado na conferência com a aba Indicadores da planilha de gerenciamento: o DS16 dizia "Entra na
referência proposta? Não", e a referência usa a renda média invertida (`renda_inv` na T20); a
planilha estava certa ("Sim").
Mudança: `dados_relatorio_descritivo.na_referencia()` mapeia `renda_inv` → `renda_media` ("Sim, como
renda invertida"); numeros.json regerado (só o DS16 mudou); `preparar_entrega_relatorio.py` corrige a
célula na v3, e a v3 e o PDF foram regerados (a v3 em disco era a gerada em 08/10, sem edição).
Verificação: v3 antes × depois: uma célula diferente (DS16).

## C-09 — 09/10/2026 — v4: a apresentação reserva da reunião (R19)
Pedido (palavras do Pedro): "Execute todo o prompt de forma automatica" (prompt_apoio_reuniao_v4).
Saída: `Relatorio_Descritivo_IVS_2026-10_v4_APOIO.pptx` e `.pdf`, 295 slides: P00, os 140 da v3 (cada
um seguido do seu apoio) e 14 de glossário (42 termos); 445 perguntas. O apoio vai também nas notas
de cada original, com a linha "De onde" e as leituras pendentes.
Leitura: a linha "De onde" fica só nas notas (no slide, a fonte de 16 pt não deixaria espaço); os
números dos apoios de método foram escritos à mão e o verificador exige que cada um esteja no slide
original ou nos slides de `ver` (o prompt pedia referência resolvida por script; os modelos DS, DS-2,
FC, DC e eixos VP leem tudo do slide).
Verificação: `verificar_apoio_relatorio.py` verde (originais idênticos à v3, um apoio por slide, 2 a
4 perguntas com fonte, números com origem, glossário completo, sem escolha pela orientadora, fonte
≥ 11 pt); folhas de contato de 27 páginas.
