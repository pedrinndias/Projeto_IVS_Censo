# Relatório parcial RAIC 2026 — arquitetura

**Estado em 11/10/2026 (domingo):** etapa 2 concluída. As 3 peças foram geradas por
`scripts/pecas_relatorio_raic.py`, com as travas 1–3 verdes (§10). Texto ainda não redigido.
Falta: respostas do §9 e então a v1 (etapa 3). Inscrição com o
relatório anexado fecha em **14/10/2026**; 12/10 é feriado.

Levantamento completo (desvios, inventário, crítica, com fonte `arquivo:linha` em cada item):
`relatorio_parcial_raic/levantamento_2026-10-11.json`. Esta página é o resumo operacional dele.

---

## 1. O pedido e a leitura adotada

- Relatório parcial de atividades no modelo do **Anexo 1 do edital RAIC 2026** (edital p.8),
  com no máximo **10 páginas**, cobrindo o projeto **até a análise exploratória**. A análise
  fatorial aparece só como **etapa iniciada**.
- A orientadora pediu que se **copie e cole** o que ela já escreveu no *Plano de trabalho* e no
  *Cálculo IVS2012* (em `~/Documents/Iniciacao Cientifica/2026/Março/Arquivos/`).
- "Neste modelo" tem duas leituras: **(a)** o Anexo 1, com I a VII e os objetivos num item só;
  **(b)** o relatório da colega Izabella, que divide os objetivos em III e IV e vai até VIII.
  **Adotada: (a)**, com os subtítulos "Objetivo geral" e "Objetivos específicos" dentro do III.
  Assim o relatório também tem o conteúdo que a apresentação oral pede (edital p.5).
- Enquadramento: o início em **março/2026** coloca o Pedro no grupo que ingressou até 31/03,
  que entrega o Anexo 1 e apresenta **oralmente** (até 10 min; slides até 02/11). **Falta
  confirmar o dia.** Se o ingresso for a partir de 01/04, o documento passa a ser
  subprojeto + mini-relatório e a apresentação vira pôster.

## 2. Política de cópia (o que entra literal e o que não pode)

| Fonte | Uso |
|---|---|
| Plano — Justificativa | **Literal** → II. Introdução |
| Plano — Objetivo geral e específicos | **Literal** → III. Objetivos (1 geral + 2 específicos). **Não** usar os 4 do GUIA |
| Plano — Metodologia | **Literal**, seguido de um parágrafo novo **"Adequações ao Censo 2022"** (§4) |
| Plano — Quadro 1 | Literal, **ampliado** com as colunas Numerador e Denominador do Censo 2022 |
| Plano — Referências | Literal, com as correções de §6 |
| Cálculo IVS2012 | **Não copiar o texto.** É a ficha do IVS-BH com códigos do Censo 2010 e números de BH. Aproveitar só a estrutura numerador ÷ denominador e a lógica de elegibilidade (Dados_sig), reescritas com os números de 2022 |

**O que não pode entrar literal** (detalhes em `levantamento…json → desvios.nao_copiar_literal`):
- tabelas `*_UF.xls`, códigos V0xx e rótulos `Agua_Inade` etc., que são do Censo 2010;
- os números de BH-2010: 57/07/41/3.831 setores, entorno 99,85% e "até 75% de improvisados";
- "X convertido para −1" (no projeto, o X vira ausente) e o uso de "responsáveis = domicílios";
- o item 9 do Cálculo (renda per capita até ½ SM), que não está no Quadro 1 e não existe em 2022;
- "QGIS 2.10.1" como ferramenta das análises (elas foram feitas em Python; os mapas virão no QGIS 3.x);
- o Quadro 1 dizendo "pessoas analfabetas" sem faixa etária (agora são 15 anos ou mais).

**Pergunta pendente P-cópia:** a orientadora aceita (i) o texto literal mais um parágrafo de
adequações (padrão adotado) ou (ii) o texto dela já ajustado (verbos no passado, QGIS, erros
de digitação)? Em qualquer caso, listar para ela cada correção feita.

## 3. Mapa seção a seção (orçamento de 10 páginas)

| Seção | Fonte | Conteúdo | Pág. |
|---|---|---|---:|
| I. Identificação | Pedro | 10 campos na ordem do Anexo + local e data. Sem resposta: `[A PREENCHER]` | 1,0 |
| II. Introdução | Plano (literal) | 2 parágrafos da Justificativa + a frase do Plano sobre o IVS-BH (SMS, 2013) | 0,5 |
| III. Objetivos | Plano (literal) | Objetivo geral; Objetivos específicos 1 e 2 | 0,25 |
| IV. Metodologia | Plano (literal) + §4 | Texto do Plano; adequações; Quadro 1 (literal); elegibilidade em texto corrido; **Quadro 2** (§10) | 1,75 |
| V. Objetivos alcançados | novo | Obj. 1 **em andamento** (base, 7 indicadores, EDA concluída, fatorial iniciada). Obj. 2 depende do índice final; mapas reprogramados. Não usar "atraso" | 0,25 |
| VI. Resultados | EDA Fase 3 + §10 | R1–R6 + **Tabela 1** + **Figura 1** (§10) + discussão + parágrafo da fatorial (§5) | 3,0 |
| VII. Conclusões | EDA, sumário executivo | 4–5 achados. **Não** usar a §13 da EDA, que são prescrições (vão para Perspectivas) | 0,5 |
| Bibliografia | Plano + novas | §6 | 0,75 |
| Matéria encaminhada | Pedro | Padrão: "Nenhuma até o momento; artigo em planejamento" | 0,1 |
| Perspectivas | GUIA / EDA §13–15 | NB03 (min-max por município), concluir a fatorial e os pesos com a orientadora, IVS final e faixas, mapas QGIS 3.x e Moran, universo da renda V06004, artigo | 0,4 |
| Outras atividades | Pedro | Programa de Inserção e Curso Introdutório (só se confirmados), reuniões, eventos | 0,3 |
| Avaliação | **Pedro escreve** | Aspectos importantes, críticas e sugestões | 0,4 |
| Apoio + Observação | Pedro / padrão | Observação: "Não houve mudança dos objetivos; as adequações metodológicas estão descritas na seção IV." | 0,1 |
| Folga | — | Quebras de página e figuras | 0,7 |

## 4. Metodologia — conteúdo novo (adequações ao Censo 2022)

**Códigos do Censo 2022 dos 7 componentes.** *Revisto em 11/10: isto é só referência para
redigir as adequações. Não vira quadro no relatório: o Quadro 1 fica literal, como a professora
escreveu, e a definição de cada indicador vai no Quadro 2 (§10). Os códigos completos estão no
`Quadro_Indicadores.xlsx` já entregue à orientadora.*

| Dimensão | Indicador | Numerador (Censo 2022) | Denominador |
|---|---|---|---|
| Saneamento | Água inadequada ou ausente | V00112–V00118 (tudo que não é rede geral) | V00001 (DPPO) |
| Saneamento | Esgoto inadequado ou ausente | V00312–V00316 | V00001 |
| Saneamento | Lixo inadequado ou ausente | V00398–V00402 (inclui caçamba, como no IVS 2012) | V00001 |
| Socioeconômica | Razão de moradores por domicílio | V00005 + V00006 | V00001 + V00002 |
| Socioeconômica | Analfabetismo, **15 anos ou mais** | V00901 | V00900 + V00901 |
| Socioeconômica | Rendimento médio do responsável | V06004 (média pronta do IBGE) | — |
| Socioeconômica | Cor/raça preta, parda e indígena | V01318 + V01320 + V01321 | v0001 |

Fonte do quadro: SMS (2013); IBGE (2022). Códigos: `src/ivs_censo/indicadores.py:78-98`.

**Adequações (uma frase cada):**
- recorte urbano (pedido da orientadora);
- denominador V00001, equivalente ao V002 de 2010;
- analfabetismo de 15 anos ou mais, porque 2022 não tem dados abaixo dessa idade;
- renda pelo V06004, que só conta responsáveis com rendimento;
- valores sigilosos ("X") tratados como ausentes, nunca como zero;
- caçamba mantida como lixo inadequado;
- processamento em Python; mapas no QGIS 3.x.

Não entram, por falta de espaço: improvisados na razão, troca de arquivos, ordem do Dados_sig,
entorno e os 21 indicadores complementares.

**Elegibilidade 2022** (EDA §3.3–3.4, conferido em 11/10). Vai **em texto corrido**, não em
tabela: as tabelas do relatório são as que o Pedro definiu (§10).

| Etapa | Setores |
|---|---:|
| Base bruta, 70 municípios | 109.032 |
| ZERADO (sem população) | 1.736 |
| SIGILOSO (população ou domicílios suprimidos) | 1.015 |
| COLETIVO | 0 |
| OK | 106.281 |
| Rurais excluídos | 2.173 (2,04% dos elegíveis) |
| **Recorte de análise (urbanos elegíveis)** | **104.108** |

Usar **só** essa ordem e esses números. A DS01 e o T01 usam outra ordem (106.347 e 2.685) e
não devem ser citados.

## 5. Resultados — blocos e números

Toda a análise usa os 104.108 setores urbanos. Antes de entrar no texto, cada número é
**reconferido contra a fonte**; a fonte e a linha estão no JSON (`inventario.resultados_eda`).

- **R1 Recorte**: 70 municípios, 104.108 setores. O Sudeste concentra 59% dos setores.
- **R2 Descritivas** → é a **Tabela 1** do §10 (12 indicadores, formato da imagem do Pedro).
- **R3 Forma**: os três indicadores de saneamento têm mediana 0 (zeros: 74,25%, 72,53% e
  62,78%). Renda **sem o setor extremo**, como na Tabela 1: média R$ 4.185,81 contra mediana
  R$ 2.572,39; assimetria 3,20. Não usar os R$ 4.187 / 3,74 da EDA, que incluem o extremo.
- **R4 Sigilo do analfabetismo**: cobertura de 84,10% (16.552 setores sem dado), e o sigilo
  não é aleatório: renda mediana R$ 2.313,89 nos setores com dado contra R$ 6.092,84 nos sem
  dado. **Não citar ranking municipal**: as fontes divergem.
- **R5 Correlações** → é a **Figura 1** do §10. O texto cita **só os números da Figura 1**:
  n = 75.629, exclusão por lista, renda invertida e, por isso, com sinais positivos. Não usar o
  −0,81 / −0,76 da EDA, que vem de outra base (pares disponíveis).
- **R6 Regional**: gradiente Norte → Sul em 5 dos 7 indicadores. **Só texto** (1–2 frases com
  números de `T04_descritivas_regiao.csv`), e só para os 12 indicadores da matriz.
- **Sigilo além do analfabetismo:** Sem banheiro também perde setores por sigilo (n = 91.912).
  Citar junto com o R4.
- **Uma frase cada**:
  - Brasil: os 70 municípios têm 26,0% da população e 30,0% dos setores urbanos elegíveis;
  - validação externa: população de 203.080.756 e IEP de 79,99 contra 80,0 do IBGE;
  - ~~favelas~~: sai, porque não é indicador da matriz (regra de escopo do §10);
  - envelhecimento: usar a linha "Idosos (60+)" da Tabela 1 (média entre setores de 0,175) e
    não os 16,65% da EDA, que é a proporção agregada (outra medida).
- **Fora**: outliers (R8) e heterogeneidade municipal (R12).
- **Discussão (~0,5 pág.)**: (a) implicações metodológicas dos achados; (b) diálogo com a
  literatura **só com obras que o Pedro leu**. Não atribuir achados a Passarelli-Araujo,
  Gioia ou Allik sem conferir.

**Parágrafo da fatorial (até 5 linhas, no fim do VI). Pode dizer:**
- a fatorial foi iniciada entre agosto e setembro de 2026 (GUIA:778), com base em Matos e Rodrigues (2019);
- a EDA indicou um bloco socioeconômico, um de saneamento e o lixo isolado;
- foram feitos testes de adequação da matriz (KMO, MSA, Bartlett) com Spearman e comparados
  métodos de extração e rotação;
- os resultados preliminares estão em discussão com a orientadora.

**Não pode dizer:**
- pesos (65/35, 60/40), número de fatores, KMO, AUC, Φ ou concordância;
- o n da fatorial (87.545 ou 73.878);
- que a fatorial está "concluída" (o GUIA:684 diz isso, mas contradiz o pedido);
- "AFC", IVS final ou faixas.

**Peças visuais:** definidas pelo Pedro em 11/10 (§10). São **Quadro 2, Tabela 1 e Figura 1**,
e nenhuma outra figura. As candidatas listadas antes (DC02, F15, painéis DS) saem do plano.
Quadro, Tabela e Figura são numerados em séries separadas.

## 6. Bibliografia

**Base:** as 13 referências do Plano, em ordem alfabética.

**Correções nas citações do texto copiado:**
- "Pellegrinni" → PELLEGRINI;
- "Agero, 2020" → Agero et al., 2020;
- "13,709" → 13.709;
- "paras as" → "para as";
- "compõem" (dois casos);
- "Gioia et al." com 3 autores: decidir com a orientadora.

**Acrescentar:**
- ELSI-Brasil, sem inventar (usar `docs/referencias/Estudo Longitudinal da Saúde dos Idosos
  Brasileiros.docx` ou a que a orientadora indicar);
- BRASIL, CNS Res. 510/2016;
- BRASIL, Lei 13.709/2018;
- IBGE, Agregados por setores censitários 2022 (com o ano);
- outras obras só se o texto as citar.

## 7. Produção

- **Pasta:** `relatorio_parcial_raic/`. Não mexer em `relatorio_descritivo/`, que é o deck de 140 slides.
- **Peças visuais:** um script novo, `scripts/pecas_relatorio_raic.py`, gera Figura 1,
  Tabela 1 e Quadro 2, além de `relatorio_parcial_raic/dados/pecas.json` com todo número que o
  texto cita (§10). Nenhum número é digitado à mão.
- **Ferramenta, sem instalar nada:** HTML → `soffice --convert-to docx` →
  `relatorio_parcial_raic/Relatorio_Parcial_RAIC_2026_Pedro_v1.docx`, depois `soffice
  --convert-to pdf` para contar páginas. O `.docx` passa a ser o original que o Pedro edita no Word.
- **Formatação padrão** (o edital não define): igual à da colega, Times New Roman 12,
  entrelinha ~1,1 e margens de 1,27–2 cm. Títulos em estilo de Título, não Normal.
  Quebra de página real depois da capa.
- **Critérios de pronto da v1:**
  - PDF com **≤ 10 páginas**;
  - os 15 itens do Anexo presentes, na ordem;
  - todo número conferido contra a fonte;
  - zero números de BH-2010;
  - todos os `[A PREENCHER]` listados no fim da entrega.

## 8. Etapas (cada uma para e mostra o resultado)

1. **Pedro**: respostas bloqueantes (§9). As imagens já foram definidas (§10).
2. ✅ **Gerar as peças** (§10): Figura 1, Tabela 1 e Quadro 2, com as travas. Feito em 11/10.
3. ✅ **v1 gerada em 11/10** por `scripts/gerar_relatorio_raic.py`: 9 páginas, verificada por 3 agentes (números, cópia, conformidade); correções aplicadas; NOTAS_PARA_ORIENTADORA.md atualizado. Revisão do conselho (5 conselheiros, 5 revisores e o presidente) e texto novo reescrito em 11/10: 9 páginas, conferidas visualmente; números comparados antes e depois; texto literal intacto. Edição do Pedro no Word preservada (backup em historico/). **12/10:** o Word tinha gravado a versão anterior ao conselho por cima da revisada; as edições do Pedro (nome da orientadora, Unidade, Introdução, Matéria, Perspectivas, Observação) foram levadas ao gerador e .docx, PDF e cópia grifada (`--grifado`) saíram da mesma versão (9 páginas). **12/10, tarde:** revisão final do Pedro (13:34, backup em historico/) levada ao gerador + correções do 2º conselho (Coorientador, Avaliação com proposta de crítica e sugestão, "Quadro 1" nas Conclusões, "condição socioeconômica" no lugar de "vulneráveis", viés do sigilo, assimetria dos coletivos). A orientadora pediu manter a fatorial como "iniciada". 9 páginas; sem pendências.
4. **Pedro**: Avaliação, Outras atividades e correções.
5. **Orientadora** revisa (13/10): enviar a v2 com a lista de correções feitas no texto dela.
6. **Pedro** gera o PDF final e faz a inscrição na plataforma módulos até 14/10.

## 9. Perguntas ao Pedro

**Bloqueiam a v1:**
1. Data exata de início na bolsa (e de ingresso no IRR).
2. Nome da orientadora; tem coorientador?
3. Unidade, laboratório ou grupo de pesquisa.
4. Programa de vínculo e financiador (PIBIC/CNPq, FAPEMIG…), que também preenche o Apoio.
5. Universidade e curso.
6. Título exato do subprojeto. Na falta dele, usar o do GUIA: "Índice de Vulnerabilidade à
   Saúde (IVS) intraurbano — Censo Demográfico 2022".
7. P-cópia (§2).
8. ~~Peças~~ — **resolvido em 11/10**: o relatório trabalha só com os 12 indicadores da matriz.
9. ~~Criança~~ — **resolvido em 11/10**: idosos e crianças são os dois componentes do índice
   de envelhecimento do projeto. Crianças = menores de 15 anos (`pct_pop_0a14`); idosos = 60+
   (`pct_idoso_60mais`).
10. ~~Quadro 2~~ — **resolvido em 11/10**: lista dos 12, com subtotal por dimensão.

**Podem ficar com padrão:**
- palavras-chave do Plano do Artigo (Vulnerabilidade em Saúde; Saúde Urbana; Indicadores
  Socioeconômicos; Censos; Desigualdades em Saúde);
- formatação (§7);
- formato de upload (PDF ou .docx);
- eventos, cursos e Programa de Inserção;
- quais referências ele leu, para a Discussão;
- corte dos resultados (§5);
- quais adequações declarar.

---

## 10. Peças visuais (definidas pelo Pedro em 11/10)

Origem: `~/Documents/Imagens e tabelas que vão entrar no registro.docx`, com 2 páginas, 3
imagens e 3 instruções. Há duas caixas de texto ocultas com "3", que não aparecem na
renderização; foram ignoradas.

| Peça do Pedro | No relatório | Origem no repositório | O que muda |
|---|---|---|---|
| Matriz "Spearman — IVS-7 e as quatro novas (S6, n = 69.458)" | **Figura 1** (VI) | `scripts/fatorial_ampliada.py`, `figuras()` → `banco_de_dados/eda/fatorial_ampliada/figuras/fa_correlacao_ampliada.png` | sai Água não chega; entram Idosos e Crianças; renda sem o extremo; título sem "S6" nem "quatro novas" |
| Tabela de descritivas dos 7 componentes | **Tabela 1** (VI) | `analises_exploratorias/00_referencia/tabelas/T03_descritivas_global.csv` (renda = `renda_media_sem_extremo`; os 7 batem com a imagem) | passa a ter os 12 indicadores da Figura 1 |
| Quadro "Dimensão × nº de indicadores" (28) | **Quadro 2** (IV) | `banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv` (`;`, 28 linhas; `gerar_quadro_indicadores.py`) | fica só com os 12 da matriz |

**Regra de escopo (o Pedro, 11/10): o relatório trabalha só com os indicadores da matriz de
correlação**, com as alterações pedidas. São 12, e Figura 1, Tabela 1, Quadro 2 e o texto usam
exatamente esses 12. Os outros 16 do quadro de 28 não aparecem: habitação precária,
apartamento, IEP, RDI, 0–14, 70+ entre 60+, responsável mulher, Água não chega etc.
- "Retirar Água não chega": sai.
- "Retirar Domicílios chefiados por mulheres" (`pct_resp_feminino`): não estava na matriz, e
  fica de fora de tudo.
- "Adicionar idoso e criança" (o Pedro, 11/10): são **os mesmos grupos do índice de
  envelhecimento do projeto**. O `iep_setor` = 60+ ÷ menores de 15 × 100 (Galvão et al.,
  *Hygeia*, 2025; Demanda 1, EDA §12.2). Entram como proporção da população residente (v0001):
  - **Idosos (60+)**: `pct_idoso_60mais` = V01040 (60–69) + V01041 (70+);
  - **Crianças (menores de 15)**: `pct_pop_0a14` = V01031 (0–4) + V01032 (5–9) + V01033 (10–14).
  - O `pct_crianca_0a4` (só 0–4) **não** entra. Era o denominador da versão antiga e errada do
    índice, corrigida na Demanda 1.
- "Monte esta tabela com os indicadores que estão na matriz": a Tabela 1 tem os mesmos 12, na
  mesma ordem da Figura 1.

**Os 12 indicadores**, na ordem da figura e da tabela:
- **IVS-7:** Água inadequada, Esgoto inadequado, Lixo inadequado, Razão de moradores,
  Analfabetismo 15+, Renda (invertida na figura, em R$ na tabela), Cor/raça PPI.
- **Complementares** (separados por uma linha na figura): Sem água canalizada (V00199),
  Sem banheiro (V00495), Moradia não convencional, Idosos (60+), Crianças (menores de 15).

**Teste de viabilidade feito em 11/10** (só leitura: `.venv`, `.db` em modo `ro`, nada gravado):
- **A matriz S6 se reproduz exatamente.** Usei Spearman do pandas, exclusão por lista e a renda
  com sinal trocado: n = 69.458; renda × PPI 0,79; analfabetismo × renda 0,76; água × esgoto
  0,39. Os valores são idênticos aos da imagem, então o método está confirmado.
- **Matriz nova** (renda sem o extremo, crianças menores de 15): **n = 75.629**. (Com 0–4,
  descartado, dava 74.721.)
- **Achado que a Discussão terá de tratar:** Idosos × renda invertida = **−0,52**, ou seja, os
  setores mais envelhecidos são os de renda maior. Crianças (<15) × renda invertida = +0,62;
  Idosos × Crianças = −0,79. Idoso e criança não apontam para o mesmo lado da
  vulnerabilidade. Isso dialoga diretamente com o foco do ELSI no envelhecimento.

### Especificação

**Figura 1 — Correlação de Spearman entre os indicadores (~0,75 p., 15–16 cm de largura).**
- Mesmo estilo da imagem: rampa vermelha (`rampa_divergente`), valores com vírgula e 2 casas,
  linha separando o IVS-7 dos 5 complementares.
- Sem título dentro da imagem. A legenda vai acima, no texto: "Figura 1 – Correlação de
  Spearman entre os indicadores nos setores urbanos dos 70 municípios do ELSI-Brasil
  (n = 75.629 setores com dados completos)".
- Abaixo: "Nota: renda com sinal invertido (valores maiores = renda menor). Fonte: elaborado
  pelo autor a partir de IBGE (2022)."
- PNG a 200 dpi.

**Tabela 1 — Estatísticas descritivas dos indicadores (~0,45 p.).**
- Colunas iguais às da imagem: Indicador | n | Média | Mediana | p75 | Máx | Assim.
- Formato dos números: proporções com 3 casas, como na imagem (e não em %); renda em R$ com
  2 casas; assimetria com 2 casas; vírgula decimal e ponto de milhar.
- Base: 104.108 setores urbanos. O n de cada linha é o número de setores com o dado.
- n das linhas novas, já na T03: Sem água canalizada 104.067; Sem banheiro 91.912; Moradia não
  convencional 104.108; Idosos 103.823; Crianças (menores de 15) 103.850.
- Nota da tabela, com três pontos:
  - a renda exclui 1 setor extremo (R$ 170.418,06, em BH);
  - as proporções vão de 0 a 1;
  - n menor indica sigilo do IBGE.
- A base é diferente da Figura 1 (lá, n = 75.629 com dados completos). Dizer isso no texto.

**Quadro 2 — Indicadores analisados, por dimensão (~0,4 p.).**
- Os **12** indicadores da matriz.
- Colunas: Dimensão | Indicador | O que mede | Compõe o IVS-7 (Sim/Não).
- Agrupado por dimensão, com subtotal na linha da dimensão (é a contagem da imagem do Pedro,
  agora para os 12; conferido no CSV em 11/10):
  - Saneamento 5: água, esgoto e lixo (IVS-7); sem água canalizada e sem banheiro;
  - Socioeconômica 4: razão de moradores, analfabetismo, renda e PPI (todos do IVS-7);
  - Morfologia 1: moradia não convencional;
  - Demografia 2: idosos (60+) e crianças (menores de 15);
  - total 12.
- Conteúdo tirado das colunas `dimensao`, `o_que_mede` e `entra_no_ivs7` do CSV. Ajuste de
  redação: tirar "(reproduz o V0005 do IBGE)" e "(complemento d…" do texto do quadro. Corpo de
  9–10 pt.
- O Quadro 1 da professora continua literal (7 variáveis). O Quadro 2 o complementa com os 5
  indicadores novos e a dimensão de cada um.

### Script `scripts/pecas_relatorio_raic.py` (novo; único que toca dados)

1. **Carga:** lê o `.db` em modo `ro`, com o mesmo filtro de `fatorial_ampliada.carregar()`
   (`urbano == 1` e `Dados_sig == 'OK'`): 104.108 setores.
2. **Trava 1:** com as colunas do S6 e a renda original, tem de dar n = 69.458 e
   renda × PPI = 0,79. Se não der, aborta.
3. **Figura 1:** gera a matriz dos 12 (renda sem extremo, invertida, exclusão por lista) →
   `relatorio_parcial_raic/figuras/fig1_correlacao.png` e `dados/matriz_spearman.csv` (com o n).
4. **Tabela 1:** 12 linhas lidas da T03 → `dados/tabela1_descritivas.csv`.
   **Trava 2:** as 7 linhas do IVS-7 têm de bater com a imagem do Pedro (n, média, mediana,
   p75, máx, assimetria).
5. **Quadro 2:** `Quadro_Indicadores.csv` filtrado para os 12 da matriz →
   `dados/quadro2_indicadores.csv`. **Trava 3:** a contagem tem de ser Saneamento 5,
   Socioeconômica 4, Morfologia 1 e Demografia 2, total 12. A lista tem de ser a mesma da
   Figura 1 e da Tabela 1.
6. **Números para o texto:** `dados/pecas.json` com todo número que o texto vai citar
   (correlações destacadas, n, contagens).
7. **Proibido no relatório:** "S6", "cenário", "quatro novas", "fatorial ampliada" e qualquer
   número do NB04 (§5).

### Resultado da geração (11/10)

- **Travas 1–3 verdes:** a S6 se reproduz (n = 69.458; 0,79); a T03 bate com o `.db` nos 12
  indicadores; a contagem do quadro é 5/4/1/2.
- **Figura 1:** n = **75.629**. Destaques: renda × PPI 0,79; analfabetismo × renda 0,76;
  água × esgoto 0,40 (era 0,39 na S6, por ter outra base); Idosos × renda −0,52;
  Crianças × renda +0,62; Idosos × Crianças −0,79.
- **Tabela 1:** igual à imagem do Pedro, com **uma correção**. O máximo do analfabetismo é
  **0,725** (37/51 = 0,72549…); a imagem trazia 0,726 por arredondamento duplo. O arredondamento
  segue a NBR 5891 (5 seguido de zeros vai para o par), o que mantém o p75 da renda em R$ 4.835,82.
- **Para o texto:** Sem banheiro e Moradia não convencional têm p75 = 0 e assimetria de 21,31 e
  13,01. São eventos raros, concentrados em poucos setores.
- **Saídas:** `figuras/fig1_correlacao.png` (200 dpi) e `dados/{tabela1_descritivas,
  quadro2_indicadores, matriz_spearman}.csv` + `dados/pecas.json`.
