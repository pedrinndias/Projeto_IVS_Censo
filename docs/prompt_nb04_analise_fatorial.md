# Prompt para implementar o Notebook 04 — análise fatorial e pesos do IVS

> **Estado em 16/09/2026 — não executado.** O estudo e o plano estão prontos e versionados;
> a implementação não começou. Este documento existe para ser colado numa sessão do
> Claude Code aberta na raiz do projeto.

Este documento tem três partes: o **contexto** que a sessão precisa ter, o **prompt para
colar**, e as **skills** que ela deve usar em cada fase.

---

## Parte 1 — O que já existe (leia antes de colar)

Nada aqui parte do zero. A análise fatorial já foi rodada uma vez.

| Onde | O que é |
|---|---|
| `docs/Analise_Fatorial_Enap2019_Guia_de_Leitura.md` | O estudo do livro da Enap, seção por seção, com os números do projeto ao lado. **As cinco revisões que a leitura obriga estão na §4.** |
| `docs/Analise_Fatorial_NB04_Plano_de_Implementacao.md` | As 16 ideias com custo e veredito, a arquitetura em 10 blocos, os resultados esperados. |
| `docs/Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md` | A análise já rodada e interpretada, com checklist de 15 passos. Itens 13, 14 e 15 = escopo do NB04. |
| `scripts/diagnostico_fatorial.py` | 219 linhas em numpy puro: KMO, MSA, Bartlett, Horn, ACP, Varimax. **É a base do trabalho.** |
| `banco_de_dados/eda/fatorial/` | 19 CSVs com os seis cenários já calculados. `resumo_adequabilidade.csv` é a referência de conferência. |
| `banco_de_dados/entrega_orientadora/*.db` | SQLite versionado com as 7 variáveis calculadas. O NB04 roda sem os 2,4 GB do Censo. |

**Os dois PDFs** (`Guia_Leitura_Analise_Fatorial_Enap2019.pdf` e
`Implementacao_Fatorial_NB04_Brainstorm_e_Prompt.pdf`) têm a mesma substância dos `.md`,
diagramados para impressão. Para a sessão de Claude Code, use os `.md` — são greppáveis.

**O livro em si** (`Livro_Analise_Fatorial.pdf`, 74 p.) **não está versionado no repositório.**
Anexe-o à sessão, ou aponte o caminho local dele no prompt.

---

## Parte 2 — O prompt

> Copie tudo dentro do bloco abaixo e cole numa sessão do Claude Code aberta na raiz do
> projeto. Anexe o PDF do livro da Enap antes de enviar.

```
Você vai implementar o Notebook 04 do Projeto IVS — a análise fatorial que define os
pesos do índice. Trabalhe em português. Não comece a escrever código antes de concluir
a FASE 1.

═══════════════════════════════════════════════════════════════════════
FASE 1 — ESTUDO (não escreva código nesta fase)
═══════════════════════════════════════════════════════════════════════

Leia, nesta ordem:

  1. docs/Analise_Fatorial_Enap2019_Guia_de_Leitura.md
     O estudo do livro da Enap feito para este projeto. A §4 lista as cinco revisões
     que a leitura obriga; a §5 lista os cinco limites do livro diante do projeto.

  2. docs/Analise_Fatorial_NB04_Plano_de_Implementacao.md
     As 16 ideias com veredito, a arquitetura em 10 blocos, e os resultados esperados
     (§3) — use-os para saber se um resultado é achado ou é bug.

  3. docs/Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md
     A análise já rodada. Checklist de 15 passos; itens 13, 14 e 15 são o escopo.

  4. scripts/diagnostico_fatorial.py
     JÁ IMPLEMENTA: KMO, MSA por matriz anti-imagem, Bartlett, autovalores, análise
     paralela de Horn, ACP e rotação Varimax, tudo em numpy puro.
     NÃO REESCREVA O QUE JÁ ESTÁ AQUI.

  5. banco_de_dados/eda/fatorial/resumo_adequabilidade.csv — os seis cenários.
     src/ivs_censo/indicadores.py — definição canônica dos 7 indicadores.
     GUIA_DO_PROJETO.md §6.3 — as quatro decisões em aberto.

  6. O PDF anexo do livro, se precisar conferir alguma passagem citada. As páginas que
     importam: 22-26 (escores, refinados x não refinados), 26-28 (AF x ACP, regra de
     Stevens), 34-39 (rotação; a recomendação contra Varimax), 42 (multicolinearidade
     acima de 0,80), 43 (Bartlett em amostras grandes), 58 (a comunalidade de 0,50 não
     é corte rígido), 67-71 (Exemplo 2: índice de NSE — é o molde do nosso caso).

Ao final da FASE 1, apresente em no máximo 15 linhas: (a) o que o diagnostico_fatorial.py
já resolve; (b) o que falta; (c) qualquer divergência que você tenha encontrado entre os
documentos. Só então siga.

═══════════════════════════════════════════════════════════════════════
FASE 2 — O MÓDULO
═══════════════════════════════════════════════════════════════════════

Crie src/ivs_censo/fatorial.py seguindo o padrão de src/ivs_censo/indicadores.py
(docstring extenso, funções puras, nomes em português, comentários que explicam a
decisão e não o óbvio). Migre para lá o que está em scripts/diagnostico_fatorial.py e
acrescente:

  - rotacao_promax(cargas, kappa=4)   -> cargas padrão, cargas de estrutura,
                                         matriz de correlação entre fatores
  - fatoracao_eixo_principal(R, k)    -> ACP iterada com comunalidades na diagonal,
                                         critério de parada e máximo de iterações
                                         explícitos
  - escores_regressao(R, cargas)      -> B = R^-1 A
  - smc(R)                            -> 1 - 1/diag(R^-1)
  - bootstrap_cargas(X, k, n_rep=1000, seed=42)

RESTRIÇÃO FIRME: apenas numpy e pandas. Não adicione scipy, sklearn nem factor_analyzer
ao requirements.txt. Tudo acima é álgebra linear que o numpy faz. Se julgar alguma
função inviável sem dependência nova, PARE e pergunte — não instale.

Escreva testes em tests/test_fatorial.py. No mínimo:
  (a) ACP + Varimax do módulo novo reproduz ivs7_spearman_cargas.csv (tolerância 1e-6);
  (b) promax sobre fatores ortogonais por construção devolve correlação ~0 entre eles;
  (c) escores por regressão têm variância ~1.

Ao terminar a FASE 2, rode /code-review no diff antes de seguir.

═══════════════════════════════════════════════════════════════════════
FASE 3 — O NOTEBOOK
═══════════════════════════════════════════════════════════════════════

Crie notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb com dez blocos. Cada bloco:
célula markdown explicando a decisão metodológica com a página do livro que a sustenta,
depois o código, depois a leitura do resultado. Siga o estilo do
02_Analises_Descritivas.ipynb.

 1. CARGA — lê banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db,
    tabela setores_censitarios, filtro urbano=1 AND Dados_sig='OK'. Importa os
    indicadores de src/ivs_censo. Inverte a renda. CONFIRA: 104.108 setores no recorte,
    87.545 completos nas 7 variáveis. Se não bater, pare e investigue.

 2. ADEQUABILIDADE — correlação (Spearman; Pearson como sensibilidade), KMO, MSA,
    Bartlett, e acrescente SMC por variável.
    TRAVA: tem de reproduzir resumo_adequabilidade.csv exatamente — KMO 0,7826;
    MSA mín 0,6995; Bartlett 235084,38. Se divergir, pare: há erro na migração.
    Registre que renda x cor/raça = -0,811 está acima do limiar de 0,80 (livro p.42).

 3. NÚMERO DE FATORES — autovalores, Kaiser, Horn, variância acumulada.
    Figura: scree plot com a linha de Horn sobreposta.
    Registre que na solução sem lixo Kaiser retém UM fator (2º autovalor = 0,9585) e
    que a retenção do segundo se apoia na razão teórica (livro p.32).

 4. EXTRAÇÃO COMPARADA — ACP e fatoração do eixo principal, lado a lado, com a maior
    diferença absoluta entre cargas. Contexto: com 6 variáveis e comunalidade mínima
    0,380, duas das três condições de Stevens falham.

 5. ROTAÇÃO COMPARADA — Varimax e promax. Publique a matriz de correlação entre os
    fatores. Recalcule a repartição dos pesos na solução oblíqua e compare com os
    65/35 da ortogonal. Verifique se alguma carga passa de 1; se passar, confira a
    variância residual (livro p.22: residual negativa = solução inadmissível).

 6. ESTABILIDADE — bootstrap de 1.000 reamostragens, IC 95% para cada carga e para a
    repartição entre dimensões.

 7. PESOS E ESCORES — fixe os pesos. Calcule as DUAS versões: (a) índice 0-1 por média
    ponderada das variáveis padronizadas; (b) escore pelo método da regressão. Reporte
    a correlação de Spearman entre os dois rankings.

 8. CENÁRIOS — índice sob: 1 x 2 fatores; pesos empíricos x 60/40 do IVS-BH; com e sem
    os setores de sigilo. Tabelas de contingência entre as classificações em 4 faixas
    (quartis). A MÉTRICA É QUANTOS SETORES MUDAM DE FAIXA, não variância explicada.
    Objetivo: mostrar o custo de cada escolha, não escolher.

 9. VALIDAÇÃO EXTERNA — separação dos 19.452 setores de FCU (CD_TIPO = 1) contra os
    demais: distribuição do índice, diferença de medianas, curva ROC. É a validação
    mais forte disponível, porque o marcador é externo ao índice.

10. SÍNTESE — tabela final de pesos; o que fica decidido; o que vai para a orientadora;
    e as limitações declaradas: Bartlett vazio nesta escala, ACP sobre matriz de
    Spearman é ACP de postos, multicolinearidade renda x cor/raça, viés não aleatório
    do sigilo (16.563 setores, 15,9%), dependência espacial não tratada, falácia
    ecológica, e a questão reflexivo x formativo (plano §4).

Saídas em banco_de_dados/eda/fatorial/, prefixo nb04_, sep=';', encoding utf-8-sig.
Figuras em .../figuras/, dpi 150, matplotlib puro, paleta do projeto
(tinta #1A1A1A, petrol #1F4E4A, clay #A83A2C, cinza #666666).
Para as figuras, use a skill /dataviz antes de escrever o código dos gráficos.

═══════════════════════════════════════════════════════════════════════
FASE 4 — RELATÓRIO E APRESENTAÇÃO
═══════════════════════════════════════════════════════════════════════

4a. docs/Relatorio_Analise_Fatorial_NB04.md — sumário executivo com os achados
    numerados; método e as decisões com a página do livro que sustenta cada uma;
    resultados bloco a bloco; decisões que vão para a orientadora com o custo de cada
    opção; limitações; reprodutibilidade.

4b. Deck para a orientadora, com a skill /pptx:
    docs/Apresentacoes_IVS/Analise_Fatorial_NB04_<AAAA-MM>.pptx

    IMPORTANTE: o projeto gera decks por SCRIPT, não à mão — veja
    scripts/gerar_deck_eda_central.js e docs/Apresentacoes_IVS/README.md. Crie
    scripts/gerar_deck_fatorial.js reusando os helpers daquele arquivo (capa, titulo,
    secao, tabela booktabs, numero, regua, anotar) e a mesma paleta (TINTA 1A1A18,
    CINZA 56534C, REGUA C8C6C0, ACENTO 8C2F27, fonte Cambria). Os números NÃO são
    digitados no gerador: leia-os dos CSVs nb04_*.
    Escreva notas do apresentador (addNotes) em TODOS os slides — o deck serve para
    estudar, não só para projetar.

    Estrutura sugerida (~22 slides): o problema (os pesos em aberto) · a Etapa 1 do
    livro conferida · Pearson x Spearman · número de fatores e o caso do lixo · as
    cinco revisões que o livro obriga · reflexivo x formativo · os resultados do NB04 ·
    as decisões para a orientadora.

═══════════════════════════════════════════════════════════════════════
REGRAS QUE VALEM O TEMPO TODO
═══════════════════════════════════════════════════════════════════════

• NÃO decida o que é da orientadora: destino do indicador de lixo, número de fatores,
  política do sigilo, e a questão reflexivo x formativo. Produza a evidência e o custo
  de cada opção; não feche a questão.

• NÃO calcule o IVS final. Isso é o Notebook 05, depois da normalização municipal do
  Notebook 03. Aqui o produto são os PESOS e a estrutura.

• NÃO redefina os indicadores. Importe de src/ivs_censo/indicadores.py.

• NÃO invente número. Todo valor citado sai de um arquivo gerado por código versionado.
  Se precisar de um dado que não existe, calcule-o e diga onde gravou.

• Se um resultado contrariar o que os documentos do projeto afirmam, PARE e avise antes
  de seguir. Pode ser descoberta, pode ser erro de migração — e a diferença importa.

• Fatorar sobre os indicadores BRUTOS, não sobre os normalizados por município. Já está
  medido que normalizar antes derruba o KMO de 0,783 para 0,720 e muda os pesos de
  65/35 para 56/44.

• Commits pequenos, um por fase, mensagem em português explicando a DECISÃO, não só o
  arquivo tocado.

Comece pela FASE 1 e apresente o resultado dela antes de seguir para a FASE 2.
```

---

## Parte 3 — Skills, por fase

| Fase | Skill | Para quê |
|---|---|---|
| 1 — Estudo | `/graphify` | O projeto tem grafo em `graphify-out/`. A skill orienta tratar perguntas sobre o repositório como consulta ao grafo primeiro. Útil para "onde está X". **Atenção:** o grafo está desatualizado desde 10/08/2026 (ver `prompt_graphify_atualizacao.md`) — não confie nele para números. |
| 2 — Módulo | `/code-review` | Rodar no diff antes de seguir para a Fase 3. Álgebra linear escrita à mão é onde erro silencioso mora. |
| 3 — Notebook | `/dataviz` | **Ler antes de escrever o código dos gráficos.** Scree plot, mapa de cargas e curva ROC. A skill exige ser carregada antes da primeira linha de código de gráfico. |
| 4a — Relatório | `/docx` | Se a orientadora quiser a versão Word, como nos relatórios anteriores. O `.md` é o original versionado. |
| 4b — Deck | `/pptx` | O deck. **Mas o padrão do projeto é gerar por script** (`pptxgenjs` em Node) — a skill ajuda na estrutura e no conteúdo dos slides, o gerador continua sendo o artefato versionado. |
| Qualquer | `/llm-council` | Para a questão reflexivo × formativo (plano §4), que é exatamente o tipo de decisão com trade-off real que a skill serve. **Rode até o fim** — um conselho interrompido não é um conselho. |

### Skills a não usar aqui

- `/init` — o projeto não tem `CLAUDE.md`, e criar um agora, no meio de uma tarefa, misturaria escopos. Se quiser um, faça em sessão separada.
- `/simplify` — o código do NB04 é novo; simplificar antes de existir não faz sentido.
- `/security-review` — não há superfície de segurança nesta tarefa.

---

## Parte 4 — Como conferir que deu certo

Ao final, estes artefatos devem existir:

```
src/ivs_censo/fatorial.py                          módulo novo
tests/test_fatorial.py                             3 testes no mínimo
notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb 10 blocos
banco_de_dados/eda/fatorial/nb04_*.csv             saídas
banco_de_dados/eda/fatorial/figuras/*.png          scree plot, cargas, ROC
docs/Relatorio_Analise_Fatorial_NB04.md            relatório
scripts/gerar_deck_fatorial.js                     gerador do deck
docs/Apresentacoes_IVS/Analise_Fatorial_NB04_*.pptx  deck
```

E estas três perguntas devem ter resposta com número e referência:

1. **Quais são os pesos do IVS, e por quê?**
2. **Quão sensível é a classificação dos setores a essa escolha?**
3. **O índice separa os territórios que sabidamente são vulneráveis?**

Se as três tiverem resposta, o Notebook 04 cumpriu o papel.
