# Prompt para auditar o projeto de ponta a ponta

**Para que serve.** Colar numa sessão nova do Claude Code, aberta na raiz do repositório,
quando for preciso verificar o projeto inteiro — dados, código, análises, interpretações e
documentos — antes de uma entrega, de uma submissão de artigo ou de uma reunião decisiva.

**Quanto custa.** É uma auditoria longa. Rodar a pipeline inteira leva dezenas de minutos e
a leitura crítica dos documentos é a parte cara. Reserve a sessão.

**O que já existe e não deve ser refeito do zero.** O
[`Relatorio_Integridade_Projeto.md`](Relatorio_Integridade_Projeto.md) é a auditoria de
19/05/2026, revisada em 12/06 e 09/08. Ele resolveu C1 a C5 e R1 a R5. Esta auditoria parte
dele: o que lá está marcado como resolvido é para **reconferir por amostragem**, não para
reinvestigar.

---

## O prompt

> Copie tudo dentro do bloco e cole numa sessão nova.

```
Você vai auditar o Projeto IVS — Censo 2022 / ELSI-Brasil de ponta a ponta. Trabalhe em
português. O objetivo NÃO é melhorar o projeto: é descobrir onde ele está errado, onde
está frágil, e onde afirma mais do que mediu. Seja adversarial com o trabalho, não com
quem o fez.

Você tem permissão para rodar qualquer script, notebook e teste do repositório. NÃO altere
nenhum arquivo versionado sem me perguntar: a saída desta auditoria é um relatório, não um
patch.

═══════════════════════════════════════════════════════════════════════
REGRA QUE VALE O TEMPO TODO
═══════════════════════════════════════════════════════════════════════

Todo número afirmado em qualquer documento tem de ser rastreável até um arquivo gerado
por código versionado. Quando encontrar um número que não consegue rastrear, isso é um
achado — mesmo que o número esteja certo. O projeto já teve o problema dos "CSVs órfãos"
e dos números digitados à mão num gerador de deck; é a falha recorrente da casa.

Não conserte silenciosamente. Registre, classifique e siga.

Classifique cada achado em:
  ERRO       o número ou a conclusão estão errados
  FRÁGIL     está certo hoje e quebra sozinho amanhã
  ÓRFÃO      não é rastreável até código versionado
  DIVERGENTE dois documentos do projeto dizem coisas diferentes
  EXAGERO    a afirmação é mais forte do que a evidência sustenta
  LACUNA     falta uma verificação que deveria existir

═══════════════════════════════════════════════════════════════════════
FASE 1 — MAPEAR (não rode nada ainda)
═══════════════════════════════════════════════════════════════════════

Leia, nesta ordem:

  1. GUIA_DO_PROJETO.md — o documento mestre. É a fonte da verdade declarada.
  2. docs/MANUAL_DO_PROJETO.md — o mapa do repositório e de onde vem cada número.
  3. docs/Relatorio_Integridade_Projeto.md — a auditoria anterior e o que ela resolveu.
  4. README.md e estrutura_projeto.md.
  5. git log --oneline -40, para saber o que mudou por último.

Ao final, produza o INVENTÁRIO: que artefatos existem (scripts, notebooks, módulos,
CSVs, bancos, documentos, decks), quais estão na pipeline ativa e quais são histórico.
Marque explicitamente o que está em Backup/ e o que a documentação chama de legado —
isso NÃO entra na auditoria, mas precisa estar identificado para não ser confundido com
material vivo.

Pare e me mostre o inventário antes de seguir.

═══════════════════════════════════════════════════════════════════════
FASE 2 — REPRODUZIR
═══════════════════════════════════════════════════════════════════════

A pergunta desta fase é uma só: rodar tudo de novo devolve os mesmos arquivos?

  a) ./.venv/bin/python -m pytest tests/ -q
  b) Rode cada script de scripts/ que gera artefato versionado. Depois de cada um,
     `git status --porcelain` na pasta de saída. Arquivo que mudou sem que o código
     tenha mudado é achado — pode ser semente não fixada, ordenação instável de
     dicionário, timestamp embutido ou dependência de versão de biblioteca.
  c) Execute os notebooks da pipeline ativa (notebooks/Fase3_EDA_ELSI/) com
     `jupyter execute` ou nbclient, e repita a conferência.
  d) Registre as versões: python --version, e as de pandas, numpy e matplotlib no .venv,
     contra o que requirements.txt declara.

Relate: o que reproduziu exatamente, o que reproduziu com diferença, o que não roda.

═══════════════════════════════════════════════════════════════════════
FASE 3 — OS DADOS
═══════════════════════════════════════════════════════════════════════

Confira contra o banco, não contra a documentação:

  • 109.032 setores na base bruta; 104.108 no recorte urbano elegível; 87.545 completos
    nas 7 variáveis do IVS; 19.507 setores de FCU, 19.452 deles no recorte.
  • A regra Dados_sig: a ordem das condições importa e já foi corrigida uma vez
    (população zero antes de sigilo). Reproduza a classificação e confira as contagens.
  • O denominador de cada indicador é V00001, e a taxa de analfabetismo é
    V00901 / (V00900 + V00901). Confira em src/ivs_censo/indicadores.py, não no texto.
  • Nenhuma proporção fora de [0, 1] antes do clipping.
  • Sigilo: o módulo soma numeradores com min_count=1, então parcela sigilosa entra
    valendo ZERO. O docstring de indicadores.py quantifica o viés. Confira essa conta.
  • renda_media × renda_media_sem_extremo: quais artefatos usam qual coluna? Há mistura
    das duas na mesma tabela ou no mesmo deck?
  • Os dois .db de banco_de_dados/entrega_orientadora/ dizem o mesmo que os .csv
    equivalentes? Compare linha a linha, não só a contagem.

═══════════════════════════════════════════════════════════════════════
FASE 4 — O CÓDIGO
═══════════════════════════════════════════════════════════════════════

Leia src/ivs_censo/ inteiro e scripts/ inteiro. Procure especificamente:

  • Fórmula duplicada entre módulo, script e notebook — a dívida que o projeto já pagou
    uma vez, em 20/08/2026. Se a mesma conta existe em dois lugares, elas divergem?
  • Álgebra linear escrita à mão em src/ivs_censo/fatorial.py: KMO por matriz
    anti-imagem, Bartlett, Horn, promax, eixo principal, escores por regressão. Confira
    cada uma contra a definição na literatura, não contra a intuição. É onde erro
    silencioso mora.
  • Valor ausente: cada função diz o que faz com NaN? Alguma trata NaN como número?
  • Semente aleatória fixada em tudo que reamostra ou simula.
  • Caminho absoluto, dependência de diretório de trabalho, locale — o projeto já teve
    um caminho fixo que quebrava em outra máquina.
  • Comparação de ponto flutuante por igualdade; astype(str) em coluna numérica.
  • Teste que não pode falhar: para cada teste em tests/, pergunte que mudança de código
    o faria falhar. Se não houver nenhuma, é teste decorativo.

═══════════════════════════════════════════════════════════════════════
FASE 5 — AS ANÁLISES E AS INTERPRETAÇÕES
═══════════════════════════════════════════════════════════════════════

Esta é a fase que importa mais e a que é mais fácil pular.

Para CADA afirmação interpretativa dos documentos — GUIA_DO_PROJETO.md,
docs/Relatorio_EDA_Fase3_IVS_ELSI.md, docs/Analise_Fatorial_*.md,
docs/Relatorio_Analise_Fatorial_NB04.md — faça três perguntas:

  1. De qual arquivo gerado sai o número que a sustenta?
  2. A afirmação é do tamanho da evidência? ("indica" × "prova"; "sugere" × "demonstra")
  3. Sobre qual conjunto de casos o número foi calculado? Recorte inteiro, urbano
     elegível, completos por lista, ou par a par? Duas tabelas do projeto já usam
     conjuntos diferentes para a mesma correlação — renda × cor/raça dá 0,811 par a par
     e 0,784 por exclusão de casos, e a diferença muda a leitura do limiar de
     multicolinearidade.

Confira também:
  • Toda correlação e toda carga fatorial descrevem SETORES, não pessoas. Alguma
    passagem escorrega para a leitura individual? É falácia ecológica.
  • Teste estatístico apresentado sem ressalva de tamanho amostral.
  • Conclusão que depende de uma escolha metodológica não declarada (Spearman × Pearson,
    exclusão por lista, normalização antes ou depois de fatorar).
  • Decisão que o projeto tomou sozinho e deveria ser da orientação, ou o contrário.

═══════════════════════════════════════════════════════════════════════
FASE 6 — COERÊNCIA ENTRE DOCUMENTOS
═══════════════════════════════════════════════════════════════════════

Monte uma tabela dos números-chave e onde cada um aparece: nos documentos, nos decks de
docs/Apresentacoes_IVS/ e nos CSVs. Pelo menos: os quatro tamanhos de recorte, KMO,
Bartlett, as correlações do bloco socioeconômico, a repartição dos pesos, o AUC da
validação, as contagens de favela e de sigilo.

Onde o mesmo conceito aparece com dois valores, determine qual está certo e por quê.
Decks em historico/ estão fora: eles são registro do que foi apresentado no dia.

═══════════════════════════════════════════════════════════════════════
FASE 7 — O RELATÓRIO
═══════════════════════════════════════════════════════════════════════

Escreva docs/Auditoria_Integral_<AAAA-MM>.md com:

  • Sumário executivo: no máximo 10 linhas, dizendo se o projeto está íntegro e o que o
    ameaça.
  • Tabela de achados, ordenada por gravidade, com classificação, arquivo, linha quando
    couber, e o que exatamente está errado.
  • Para cada ERRO: o comando que o reproduz.
  • O que foi verificado e passou — importa tanto quanto o que falhou, e é o que permite
    a próxima auditoria não refazer tudo.
  • O que você NÃO conseguiu verificar, e por quê.

Não proponha correções no mesmo documento. A lista de correções é conversa separada,
depois de eu ler os achados.

═══════════════════════════════════════════════════════════════════════
O QUE NÃO FAZER
═══════════════════════════════════════════════════════════════════════

• Não auditar Backup/, notebooks/Fase1*, Fase2* nem historico/ — é material congelado
  de propósito.
• Não reescrever documento, não "melhorar" texto, não refatorar código.
• Não confiar em número que está só em documento. Se não achou o arquivo que o gera,
  o achado é ÓRFÃO, mesmo que o número pareça certo.
• Não inventar achado para encher relatório. Auditoria que acha problema em tudo não é
  lida.
• Se discordar de uma decisão metodológica que está declarada e justificada, isso não é
  achado — é opinião. Registre em seção separada, no fim.

Comece pela FASE 1 e me mostre o inventário antes de seguir.
```

---

## Depois de rodar

O relatório da auditoria é insumo, não veredito. A ordem sugerida para tratar os achados:

1. **ERRO** que afeta número publicado em deck ou relatório — corrigir e regerar.
2. **DIVERGENTE** — decidir qual número vale e alinhar todos os documentos.
3. **ÓRFÃO** — escrever o código que gera o número, ou remover a afirmação.
4. **EXAGERO** — reescrever a frase.
5. **FRÁGIL** e **LACUNA** — entram na fila de trabalho normal.
