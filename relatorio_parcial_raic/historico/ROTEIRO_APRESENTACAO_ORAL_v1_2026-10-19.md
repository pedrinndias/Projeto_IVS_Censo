# Roteiro — apresentação oral RAIC 2026

**Base:** `Relatorio_Parcial_RAIC_2026_Pedro_corrigido.pdf` (13/10/2026). Todo número abaixo
está no relatório; nada novo entra sem decisão.
**Regras do edital:** até 10 min de fala + ~10 min de arguição (2 avaliadores doutores);
PowerPoint ou Canva no **template oral da Coordic** (ainda não baixado — o `MODELO BANNER.pptx`
não serve); envio para coordic.minas@fiocruz.br até **02/11/2026** (segunda, Finados — mirar
sexta, 30/10), assunto "Pedro Dias Soares – Oral".
**Orçamento:** 13 slides, **9 min 05 s** de fala (margem de ~55 s) + 6 slides de reserva para a
arguição.

Legenda: **[A CONFIRMAR]** = depende da orientadora ou de dado que não está no relatório.

---

## Slides da fala

### 1. Capa — 0:15
- **Tela:** Índice de vulnerabilidade à saúde das cidades brasileiras: dados do censo
  demográfico de 2022 · Pedro Dias Soares · Orientadora: Amanda Cristina de Souza Andrade ·
  Coorientador: não se aplica · Grupo de pesquisa: **[A CONFIRMAR — o relatório traz o núcleo
  NESPE; o edital pede o grupo de pesquisa]** · Ingresso: 06/03/2026 · Programa: FAPEMIG ·
  Fiocruz Minas — IRR · Ciência de Dados e IA, PUC Minas.
- **Fala:** só o nome e o título; os demais itens ficam na tela (são obrigatórios no edital).

### 2. Por que um IVS intraurbano — 0:45
- **Tela:** envelhecimento e urbanização como tendências (Agero et al., 2020; IBGE, 2022) ·
  o território como determinante de saúde (Caiaffa et al., 2021; Buss; Pellegrini Filho, 2007) ·
  referência: IVS de 2012 da SMS-BH · **lacuna:** não há IVS com o Censo 2022 para os municípios
  do ELSI-Brasil.
- **Visual:** três blocos curtos em sequência (contexto → referência → lacuna).
- **Fala:** médias municipais escondem desigualdade dentro da cidade; o setor censitário mostra.

### 3. Objetivos — 0:30
- **Tela:** objetivo geral **[A CONFIRMAR: o edital pede o objetivo geral do *projeto da
  orientadora*; placeholder = o do relatório]** "Avaliar as desigualdades intraurbanas por meio
  da construção de um IVS de cidades brasileiras" · específicos: (1) construir o IVS intraurbano
  com o Censo 2022 — **em andamento**; (2) analisar sua distribuição espacial — **a iniciar**.
- **Visual:** os dois específicos com selo de status.

### 4. Desenho e base de dados — 1:00
- **Tela:** estudo ecológico · unidade: setor censitário · 70 municípios da amostra do
  ELSI-Brasil · agregados por setor do Censo 2022.
- **Visual:** funil — 109.032 setores → −1.736 sem moradores → −1.015 com sigilo na população
  ou nos domicílios → 106.281 → −2.173 rurais (2,04%) → **104.108 setores urbanos**.
- **Fala, fechando:** "Para conferir o processamento, rodei as mesmas rotinas nos 468.099
  setores do Brasil: reproduzem a população oficial (203.080.756) e o índice de envelhecimento
  do IBGE (79,99 contra 80,0)."
- **Cuidado:** se citar 26% da população do país, dizer que é dos **70 municípios inteiros**;
  o recorte urbano tem 52,1 milhões (25,7%). Não pôr os dois números lado a lado sem isso.

### 5. As sete variáveis do IVS — 0:40
- **Tela:** Quadro 1 em duas colunas — **Saneamento:** água, esgoto, lixo inadequados ·
  **Socioeconômica:** razão de moradores, analfabetismo, renda do responsável, preta/parda/indígena.
  Seta "↑ valor = ↑ vulnerabilidade"; renda entra invertida.
- **Fala:** são as variáveis do IVS-BH 2012 que existem no Censo 2022.

### 6. Adequações ao Censo 2022 — 0:50
- **Tela (uma linha cada):** (a) denominador = domicílios particulares permanentes ocupados,
  como em 2012 · (b) analfabetismo só a partir de 15 anos (2012: 5+) · (c) renda média do
  responsável; retirado um setor de favela de BH com R$ 170.418,06 · (d) sigilo: tudo suprimido →
  ausente, nunca zero · (e) caçamba segue como destino inadequado do lixo.
- **Fala:** cada adequação é uma decisão documentada; a (d) volta no slide 8.

### 7. Muitos zeros e muita assimetria — 0:50
- **Visual (novo, a gerar):** barras horizontais com o % de setores com valor zero — sem
  banheiro 95,60 · moradia não convencional 92,95 · água 74,25 · esgoto 72,53 · sem água
  canalizada 69,70 · lixo 62,78.
- **Tela, ao lado:** renda média R$ 4.185,81 contra mediana R$ 2.572,39 (63% acima).
- **Fala:** os três indicadores de saneamento do IVS têm mediana zero; parte dos zeros vem do
  sigilo. Consequência: min-max comprimiria a maioria dos setores numa faixa estreita.

### 8. O sigilo não é aleatório — 0:45
- **Tela:** analfabetismo disponível em 84,10% dos setores · renda mediana do responsável:
  R$ 2.313,87 onde há o dado × **R$ 6.092,84** onde não há · média observada 3,64%; a real fica
  entre 3,14% e 3,64%.
- **Visual:** duas barras de renda mediana (com dado × suprimido).
- **Fala:** o IBGE suprime onde há poucos analfabetos, que são os setores mais ricos; excluir
  esses setores enviesaria o índice.

### 9. Diferenças regionais — 0:35
- **Tela:** Norte × Sul — água inadequada 16× (0,323 × 0,020) · esgoto 8× (0,238 × 0,029) ·
  preta/parda/indígena 3× (0,748 × 0,246) · analfabetismo com pico no Nordeste (0,062) · lixo não
  segue o padrão (0,091 a 0,154).
- **Ressalva na tela:** o Norte tem 6 municípios — descreve a amostra, não a região.

### 10. Como os indicadores se relacionam — 1:00
- **Visual:** recorte da Figura 1 só com os 7 indicadores do IVS (sai de
  `dados/matriz_spearman.csv`); a matriz 12×12 completa fica na reserva R2 — ilegível projetada.
  Destacar o bloco renda × cor/raça × analfabetismo e a linha do lixo.
- **Tela:** bloco socioeconômico: 0,79 · 0,76 · 0,63 · lixo fraco com todos (−0,05 a 0,21) ·
  água × esgoto 0,40, mas 0,22 dentro dos municípios.
- **Fala:** renda, cor/raça e analfabetismo parecem medir uma só dimensão; o lixo talvez meça a
  forma de coleta (caçamba), não vulnerabilidade — hipótese a verificar.

### 11. Envelhecimento e vulnerabilidade — 0:45
- **Tela:** idosos × renda invertida −0,52 (−0,54 dentro dos municípios) · crianças × renda
  invertida +0,62 · **negativa em 50 dos 53 municípios** com ≥ 30 setores completos.
- **Visual:** número grande "50 de 53".
- **Fala:** setores de melhor condição envelhecem mais; os de pior condição têm mais crianças.
  Média municipal esconderia isso — é o argumento a favor da escala intraurbana.

### 12. Conclusões e próximos passos — 1:00
- **Tela, esquerda (conclusões):** 7 variáveis calculadas para 104.108 setores e conferidas com
  o IBGE · zeros e assimetria pedem cuidado na padronização · sigilo do analfabetismo exige
  tratamento próprio · bloco socioeconômico coeso, lixo independente · estrutura etária
  acompanha a condição socioeconômica dentro das cidades.
- **Tela, direita (próximos passos):** análise fatorial (iniciada) → pesos → padronização
  municipal → IVS em faixas de vulnerabilidade → mapas no QGIS 3.x → artigo e relatório final.
- **Decisão [A CONFIRMAR com a orientadora]:** o edital pede "resultados alcançados até
  outubro de 2026", e a fatorial (17/09) e o NB05 (30/09) já existem. Este roteiro segue o
  relatório: fatorial como **iniciada**, sem números. Se ela quiser mostrar, entra um slide
  entre o 11 e o 12 e sai o 9.

### 13. Agradecimentos — 0:10
- **Tela:** FAPEMIG · orientadora · Fiocruz Minas/IRR · (contato).

**Total: 9 min 05 s.**

---

## Reserva para a arguição (fora dos 10 min)

| # | Slide | Para qual pergunta |
|---|---|---|
| R1 | Tabela 1 completa (12 indicadores) | "Quais as descritivas?" |
| R2 | Figura 1 completa, 12×12 | "E os complementares?" |
| R3 | De-para Censo 2010 → 2022 (códigos V) | "Como as variáveis foram reconstruídas?" |
| R4 | Quadro 2 — indicadores complementares | "Por que esses não entram no IVS?" |
| R5 | Setor extremo de BH (R$ 170.418,06) | "Por que tirar só um setor?" |
| R6 | Pontos a revisar: universo da renda (V06004) e caçamba | "O que ainda pode mudar?" |

## Perguntas prováveis da banca

1. **Por que não usar o desvio-padrão?** Com mediana zero e assimetria alta, p75 e assimetria
   descrevem melhor a dispersão.
2. **Por que padronizar por município?** O IVS de 2012 foi calculado para um só município e o
   índice é intraurbano: a régua é a própria cidade.
3. **O sigilo não compromete o índice?** Compromete se os setores forem excluídos; por isso o
   tratamento próprio — o viés é conhecido e tem direção (setores mais ricos).
4. **Raça/cor mede vulnerabilidade?** Entra como marcador de desigualdade social estrutural,
   como no IVS de 2012.
5. **Por que o ELSI-Brasil?** O projeto se integra ao estudo; os 70 municípios são a amostra
   dele e permitem ligar o território à saúde dos idosos.
6. **E os rurais?** O índice é intraurbano; a exclusão é desigual entre municípios e entra nas
   limitações.

## O que falta antes de montar o pptx

- [ ] Baixar o **template oral** do e-mail da Coordic (anexos "+2 mais").
- [ ] Confirmar **grupo de pesquisa** e **objetivo geral do projeto da orientadora** (slides 1 e 3).
- [ ] Decidir se a fatorial entra com números (slide 12).
- [ ] Gerar os dois visuais novos: barras de zeros (slide 7) e matriz 7×7 (slide 10).
- [ ] Ensaiar com cronômetro: alvo de 9 min.
