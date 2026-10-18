# Construção do relatório descritivo — a receita

Lido por todo lote depois do 0 e por toda correção. Atualizado ao fim de cada lote.

## Comandos, sempre nesta ordem

```
./.venv/bin/python scripts/dados_relatorio_descritivo.py      # numeros.json, manifesto.csv, figuras/
node scripts/gerar_relatorio_descritivo.js                    # o .pptx, inteiro, do zero
./.venv/bin/python scripts/verificar_relatorio_descritivo.py  # itens 1–7; sai com 1 se vermelho
```

Folha de contato (uma por lote, só dos slides novos): `soffice --headless --convert-to pdf` no
scratchpad, depois `swift scripts/folha_contato.swift <pdf> <png> 2 2400 [páginas]`.

## Como um slide nasce

1. **Função construtora** em `scripts/dados_relatorio_descritivo.py`. Uma por slide (`a01`,
   `dm02`, `fa05`…) ou uma por família (`ds(ind, base)` serve aos 31 indicadores). Ela devolve
   um dicionário com `titulo, parte, requisito, sub, fontes` e os campos do layout.
2. **ID na lista `SLIDES`** (ordem do deck), que cresce lote a lote; registre o construtor no
   dicionário `construtores` de `main()`. Slides que dependem de outros (o DM14 lê as caixas
   dos DM02–DM12) são montados em `main()` depois deles.
3. **Layout** em `scripts/gerar_relatorio_descritivo.js`, no objeto `LAYOUT`; o mapa `POR_ID`
   manda um ID para um layout genérico (`tabelaLarga`, `divisoria`). A chave é o ID
   exato (`A01`, `DS01`) ou o prefixo sem número (`DM`, `DS`, `FA`, `FP`). Slide novo de uma
   família existente não precisa de JS novo.
4. **Notas do apresentador:** saem sozinhas (ID, requisitos, `notas`, `fonte_texto`, fontes).

## IDs

- Os DS são calculados a partir da ordem da T03, com as duas rendas alternativas logo depois
  de `renda_media` (função `ordem_ds()`), e ficam de DS03 a DS33.
- Já fixados: DS20 = `pct_resp_feminino`, DS31 = `iep_setor`, DS18 = `renda_media_mediana_mun`.
- Para saber o ID de qualquer indicador: `ID_DS` no script de dados.

## Layouts aprovados no piloto (aguardando o OK do Pedro)

| Família | Disposição |
|---|---|
| A01 | Capa do `deck_comum` |
| A02 | Quatro blocos à esquerda; tabela das bases à direita |
| DM | Pedido, Como lemos e O que foi feito à esquerda. À direita: O que contornamos (com filete vermelho), a tabela de resultado e "Resultado completo em" |
| DS01 | Tabela do funil à esquerda com "O que mostra" embaixo; a figura F01 à direita |
| DS | Etiqueta da dimensão no topo. Três colunas: "Como é calculado" e "O que mostra"; a tabela de 14 linhas; o histograma com boxplot |
| FA | Tabela à esquerda com "O que mostra" embaixo; a figura à direita |
| FP | Tabela na largura toda, com "O que mostra" embaixo |

## Regras fixadas no piloto

- **Identidade visual.** O deck usa a do `deck_comum.js` (Cambria, tinta, acento vermelho). As
  figuras novas usam a paleta do projeto, pelas constantes `TINTA`, `PETROLEO` e `ARGILA` de
  `eda_versoes.py`.
- **Histograma DS: zeros.** Com 50% ou mais de zeros, o desenho mostra só os valores positivos,
  e a legenda diz quantos ficaram de fora.
- **Histograma DS: cauda longa.** Se o máximo passa de 3 vezes o P99, o eixo vai até o P99 e a
  legenda diz quantos setores ficam fora do desenho. Na tabela, todos ficam. Isso aconteceu no
  IEP: 1.027 setores acima de 633,33.
- **Figuras reaproveitadas da `00_referencia`:** só as de uma medida (F01 no DS01, F22 no FA05),
  copiadas como `figuras/<ID>.png`. As agrupadas por dimensão (F02–F13) estão proibidas.
- **Textos de demanda.** Ficam no construtor, com `fonte_texto` = lista de `arquivo:linhas`. O
  verificador, item 2, recusa número de texto que não esteja nessas linhas.
- **Verificador, item 3.** Lê o Quadro (códigos V do numerador e do denominador), roda SQL no
  `.db` com o recorte e soma com `min_count=1`. Usa ×100 quando a observação diz "×100". Sorteia,
  com semente 42, um indicador de saneamento de numerador simples (no piloto saiu
  `pct_agua_nao_encanada`). A partir do lote 2, troque os dois fixos pelos DS do lote.
- **Verificador, item 7.** O "A CONFERIR" do A02 é a explicação da marca, não uma pendência.
  Desconte-o.

## Lote 1 — o que ficou fixado

- **DM02–DM12:** construídos por `dm(n, caixas, cab, linhas, colW, resultado_em, fonte_texto,
  fontes)`. O título, o subtítulo e o Pedido saem da tabela do registro (linhas 16–26), pelo
  número da demanda. As caixas são texto escrito a partir das linhas citadas em `fonte_texto`,
  e o verificador recusa número que não esteja nelas.
- **DM01:** tabela lida do registro. **DM13:** linhas 23–31 do estado do NB05. **DM15:** os 9
  itens das linhas 28–61, montados por regex.
- **C-01:** os DS mostram "Arquivo do Censo" e "Calculado em", da aba Indicadores da planilha
  de gerenciamento (`GER`). O item 8 do verificador confere a aba contra o Quadro.
- **Tabela da direita no DM** com mais de 6 linhas: corpo 9 e linha 0,24. Coluna "Cenário"
  com pelo menos 0,85 pol.

## Lotes 2 a 5 — o que ficou fixado

- **Layout pela forma dos dados** (`layoutDe(id, x)` no JS):
  - por ID: A01, A02, DS01 e DS02 (duas tabelas lado a lado);
  - pelos campos: `numero` → divisória; `blocos` sem `cab` → blocos de texto; `caixas` → DM;
    `definicao` → DS; `figura` → tabela + figura;
  - os demais: parte FP → FP; tabela com largura < 8 pol. → `tabelaTexto` ("O que mostra" à
    direita); senão `tabelaLarga`.
- **DS:** "O que mostra" fica sob a figura. A definição usa corpo 9; com mais de 330
  caracteres, 8; com mais de 650, 6,5 (caso do DS22).
- **`tipo()`:** indicador cuja observação no Quadro diz "×100" é tratado como razão (por 100),
  não como proporção. São o IEP, o RDI e o 70+ entre 60+.
- **FA02:** correlação de Spearman (padrão de `rodar_cenario`), recalculada na base de
  `montar_base` com os sete componentes completos. A função para se o n não bater com a T01
  (73.878).
- **FA15:** figura nova (`figuras/FA15.png`), as AUCs dos municípios que entram na mediana.
- **Anexo:** `anexo()` no fim de `main()`.
- **Edições à mão:** `scripts/comparar_edicoes_relatorio.py <cópia>` compara as tabelas célula a
  célula, por ID, e grava em `dados/edicoes_do_pedro.csv`.

## Plano dos IDs

Todos construídos (87 slides). Mudanças agora só pelo protocolo de correção.
