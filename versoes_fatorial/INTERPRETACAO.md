# Interpretação do pedido — as 108 versões da análise fatorial

Gravado em 08/10/2026, na sessão que escreveu `docs/prompts/prompt_versoes_fatorial_108_2026-10.md`.
**Toda sessão de execução ou de correção lê este arquivo antes de mexer em qualquer coisa.**
Se uma correção do Pedro contradisser algo daqui, vale a correção, e esta página é atualizada.

## 1. O pedido, nas palavras do Pedro

> (07/10) Na análise fatorial elenque possíveis versões, por exemplo, com os 3 tipos de rendas
> que nós geramos, renda com mediana, renda original, renda sem extremo. Análise fatorial dos 3
> tipos de rendas com versões com lixo e sem lixo. Elenque estes tipos, acho que vou querer executar.
>
> (07/10) Além dessas 6 versões novas, quero que adicione mais versões adicionando os
> indicadores trabalhados de canalização de água e com/sem banheiro, moradia convencional.
>
> (08/10) Como poderíamos fazer uma apresentação/relatório descritivo caso rodássemos as 108 versões?
>
> (08/10) Escreva o prompt com as 108 fichas, não modifique a apresentação do relatório
> descritivo, fiz algumas modificações e estou melhorando ele, sua criação está ótima daquela
> apresentação.

## 2. Requisitos

| R | Requisito | Como o prompt atende |
|---|---|---|
| V1 | As **108 versões** de `VERSOES.md`: renda (3) × lixo (2) × água canalizada (3) × banheiro (3) × moradia (2) | Motor novo, que reaproveita o do NB05 |
| V2 | **108 fichas**, uma versão por slide, mesmo layout | Caderno de fichas (`Caderno_Fichas_108.pptx`) |
| V3 | **Relatório descritivo** no estilo aprovado: uma unidade por slide, frases factuais, sem cruzamentos fora do que o eixo pede | Deck principal de cerca de 18 slides, mais o caderno |
| V4 | **Não modificar o relatório descritivo** (`relatorio_descritivo/`), que o Pedro está editando à mão | Proibição explícita; o gerador dele tem trava contra sobrescrita |
| V5 | **Fontes só nas notas do apresentador**, não no slide (C-02 do relatório) | Regra do prompt |
| V6 | **Tabelas editáveis** no PowerPoint e edições levadas à origem | Tabelas nativas e um comparador de edições |
| V7 | Ajudar a **escolher o que vai para o artigo** | Código V001–V108 em todo lugar; planilha com colunas de seleção |
| V8 | **Processo salvo**, correção sem alucinar | `ESTADO.md`, `CONSTRUCAO.md`, `CORRECOES.md`, manifesto, verificador |

## 3. Leituras adotadas (padrão até o Pedro dizer outra coisa)

| # | Ponto | Padrão | Alternativa |
|---|---|---|---|
| L1 | Método de cada versão | **Fixo, o da referência proposta:** promax, pesos 60/40, normalização municipal, 2 fatores | Os 18 métodos da grade (1.944 rodadas) |
| L2 | Amostra | **Fatorial na amostra própria** de cada versão; **comparações** (AUC, mudança de faixa, pares por eixo) **na amostra comum** às 108, como no NB05 | Tudo na própria |
| L3 | Renda | **As três**, porque o Pedro pediu 108 fichas. O deck principal mostra, com números, que elas quase não diferem | Só a original (36) |
| L4 | Água canalizada | **Somada** à água inadequada do IVS, sem substituí-la. "Não chega" e "sem canalização" nunca entram juntas, porque uma contém a outra | Substituir a água inadequada (como na versão B2 das análises exploratórias) |
| L5 | Moradia | Entra na direção da vulnerabilidade (**não convencional**), como na demanda 9 | Convencional |
| L6 | Número de fatores | **2 em todas**, como no NB05. Quando Kaiser ou Horn pedirem outro número, a ficha diz isso | Reter o que Horn indicar |
| L7 | Elegibilidade | **Critérios do NB05**, sem mudar nada: KMO ≥ 0,70; MSA ≥ 0,50; comunalidade ≥ 0,30; carga ≥ 0,40 | — |
