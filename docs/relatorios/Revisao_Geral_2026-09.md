# Revisão geral do Projeto IVS — Censo 2022 / ELSI-Brasil

**Data:** 25 de setembro de 2026
**Escopo:** o repositório inteiro — 333 arquivos versionados, inclusive o que a auditoria de 17/09 deixou de fora (`Backup/`, `graphify-out/`, `Apresentacoes_IVS/historico/`, configuração do repositório e histórico do git)
**Antecessora:** [`Auditoria_Integral_2026-09.md`](Auditoria_Integral_2026-09.md) (17/09/2026)

> **Como foi feita.** Oito frentes de revisão independentes, cada uma sem acesso às
> conclusões das outras: camada fatorial (matemática), Notebook 04 e seu relatório,
> commits posteriores à auditoria, higiene do repositório, cálculo dos indicadores e
> scripts de dados, Notebooks 01 e 02, documentação, deck e PDFs de apoio. Os achados
> classificados como ERRO nas frentes de maior risco foram **reconferidos por execução
> independente**; os da frente de commits passaram por um verificador adversarial. Cada
> achado do apêndice diz que verificação recebeu.
>
> **Limitação declarada.** Parte do material revisado — o NB04 e seus comentários, a
> análise do extremo de Belo Horizonte, os slides 95–98, os dois PDFs de apoio — foi
> escrita por mim. As frentes trabalharam sem acesso a esta linha de trabalho, o que é
> mais independência do que a auditoria de 17/09 teve, mas não substitui revisão humana.
> Nenhum arquivo versionado foi alterado: a saída desta revisão é este relatório.

---

## Sumário executivo

**O cálculo está certo.** A dúvida que a auditoria de 17/09 deixou em aberto — a camada
fatorial nunca tinha sido conferida contra uma implementação independente — está
resolvida: KMO, MSA, Bartlett, SMC, ACP, eixo principal, Varimax e promax coincidem com a
biblioteca `factor_analyzer` e com implementações escritas do zero, em diferenças de
1e-13 a 1e-4. Os CSVs do NB04 e do diagnóstico fatorial se reproduzem byte a byte. Os 74
testes passam. Os 70 municípios casam sem ambiguidade, a junção dos 8 arquivos do Censo não
perde setor, e três indicadores recalculados do zero a partir da base bruta batem sem
nenhuma divergência. No deck, 884 dos 898 números extraídos batem com os CSVs.

**O problema desta vez é de interpretação, e está no que vai à orientadora.** Quatro
conclusões do NB04 e do seu relatório não se sustentam como estão escritas:

1. **A AUC não valida o índice.** O relatório trata a AUC de 0,813 contra os setores de
   favela como "o que diz se o índice acerta". Mas a renda sozinha separa melhor (0,882), e
   pesos iguais também (0,853). A AUC confirma que as variáveis têm conteúdo
   socioeconômico; não confirma a estrutura fatorial nem os pesos 65/35. *(NB4-02)*
2. **"Os pesos são estáveis" depende de tratar 87 mil setores como independentes.** Tirar só
   São Paulo move o peso de 65,04 para 62,91; reamostrando municípios, o intervalo vai de
   58,2 a 68,2 e inclui os 60/40 da literatura. *(NB4-01)*
3. **"A rotação oblíqua afasta os pesos da literatura" é artefato da métrica.** Pela matriz
   padrão, 65,8/34,2; pela matriz estrutura, 59,6/40,4 — a outra escolha legítima inverte a
   conclusão. *(NB4-03)*
4. **O livro é citado ao contrário na p. 29.** O NB04 conclui que "o critério de Kaiser é o
   mais fraco neste caso"; a página diz que ele é mais preciso quando a amostra passa de 250
   e a comunalidade média passa de 0,6 — as duas condições que o projeto satisfaz. O mesmo
   ocorre com a p. 27 (ACP × análise fatorial). *(NB4-04)*

A esses somam-se cinco erros de fato no texto, na figura e nos comentários do NB04 — um
número de outra matriz, uma comparação entre fatores diferentes, um eixo rotulado errado,
dois comentários que descrevem a tabela ou o método ao contrário *(NB4-06 a NB4-10)*.

**Um erro em dado publicado.** A razão agregada de `pct_sem_agua_canalizada` sai invertida
nos quatro CSVs de `nacional/`: 0,986 onde o certo é cerca de 0,015. Não chega a nenhum
deck nem documento *(IND-1)*.

**Erros meus, recentes.** Os slides 96–97 do extremo de BH afirmam três números errados; o
guia de apoio repete os 16.563 setores que são, na verdade, 16.548; o `.gitignore` foi
corrompido no commit `4c476de`; o deck em circulação não se reproduz mais pelo gerador, e o
docstring do gerador manda gravar por cima dele. Dos 83 achados, **17 foram introduzidos
depois da auditoria de 17/09**.

**Histórico do git.** Dois commits ainda carregam o trailer `Claude-Session:` com a URL de
uma sessão — a reescrita de histórico removeu só o `Co-Authored-By`. E um arquivo de
configuração versionado pré-aprova `git commit` e `python -c` para quem clonar.

| Severidade | Achados únicos | Introduzidos depois de 17/09 |
|---|---:|---:|
| ERRO | 15 | 3 |
| DIVERGENTE | 20 | 7 |
| ÓRFÃO | 5 | 2 |
| FRÁGIL | 8 | 2 |
| LACUNA | 14 | 0 |
| HIGIENE | 14 | 3 |
| OPINIÃO | 7 | 0 |
| **Total** | **83** | **17** |

*92 achados brutos; 9 eram o mesmo defeito visto por duas frentes e foram fundidos.*

---

## Prioridade 1 — corrigir antes de apresentar à orientadora

| # | O que | Onde | Correção |
|---|---|---|---|
| NB4-02 | AUC tratada como validação dos pesos | NB04 célula 38; relatório item 4 e decisão 6 | Dizer o que ela mede e mostrar as comparações: renda sozinha 0,882, pesos iguais 0,853, índice 0,813 |
| NB4-01 | "Pesos estáveis" sob bootstrap que ignora os municípios | NB04 células 24–25; relatório linhas 23 e 141–143 | Relatar a sensibilidade por município (sem São Paulo: 62,91/37,09) e retirar "incerteza desprezível" |
| NB4-03 | Conclusão nº 6 depende da métrica | NB04 células 18, 19, 44; relatório linhas 31, 137, 193 | Relatar as duas métricas ou retirar a conclusão |
| NB4-04 · NB4-05 | Livro citado ao contrário (p. 27, p. 29) e Tabela 7 lida com um critério a mais | NB04 células 6, 11, 15; relatório linhas 46, 59, 106, 110 | Citar as condições completas; "reprova em um critério da Etapa 1", não dois |
| NB4-06 a NB4-10 | −0,454 da matriz errada; 0,836 entre fatores diferentes; eixo "Fator 2 — saneamento" no painel onde o fator 2 é o lixo; comentário sobre SMC; comentário sobre Horn | NB04 células 12, 16, 18, 22, 44 | Um por um, no apêndice |
| NB4-11 | Bloco 8b diz "sem consequência"; sob a normalização municipal, mudam 774 setores de faixa, 387 em BH | NB04 bloco 8b; relatório item 10; README de `atualizada/` | Restringir a conclusão à fatorial ("os pesos não mudam") |
| AUD-07 | Slides 96–97: "segundo maior na casa dos R$ 30 mil" (é R$ 45.385), "87 mil setores" (são 104.096), "um quinto do município" (é 37%) | deck, slides 96–97 | Ler os três valores dos CSVs `extremo_bh_*` |
| AUD-08 | "Retirar o analfabetismo recupera 16.563 setores": são 16.548 | Guia de apoio; relatório do NB04:191; gerador do deck | 16.563 é a perda total por listwise, não a do analfabetismo |
| DEC-1 | Slides 68 e 91 citam 3.357 setores com o caminho do arquivo da raiz, que tem 3.358 | deck | O número é o da 2ª rodada; corrigir o caminho |
| FAT-02 | A tradução para R documentada não reproduziria o Φ = 0,522 | `Codigo_Analise_Fatorial_Comentado.md` | Só importa se a tradução for mostrada; o apêndice diz o que trocar |

## Prioridade 2 — dados e código

- **IND-1 · IND-2** — razão agregada invertida em `nacional/`, e o teste que deveria pegá-la
  não cobre o único indicador com complemento.
- **FAT-01** — a Varimax para antes de convergir: erro de 5,5e-4 nas cargas da solução de 6
  variáveis. Não muda nenhuma conclusão, mas os CSVs publicam casas que não são a solução.
- **FAT-04** — `escores_regressao` aceita a matriz padrão numa solução oblíqua e devolve
  escores errados sem avisar; o NB04 hoje não cai nisso.
- **FAT-06 · FAT-12** — o eixo principal marca "convergiu" num caso de Heywood; o p-valor do
  qui-quadrado erra por ordens de grandeza na cauda (os p-valores publicados são ≈ 0 de
  qualquer jeito).
- **FAT-07** — a suíte da camada fatorial deixa passar 12 de 21 mutações plausíveis.
- **HIG-05** — com o piso `numpy>=1.26` declarado no `requirements.txt`, um teste falha por
  troca de sinal.
- **F2 (piorou)** — o padrão `astype(str) == '1'` está agora em cinco lugares; um deles, o script
  do extremo de BH, entrou depois da auditoria.
- **IND-3** — o dicionário da entrega documenta 70 das 104 colunas; faltam justamente os 26
  indicadores.
- **NBS-3 · NBS-4 · NBS-1** — o NB02 não declara que agrega por média de proporções nem que
  a correlação é par a par (diferença de até 0,033); e cita "106 mil" onde o universo é de
  104 mil.

## Prioridade 3 — documentação e rastreabilidade

- **AUD-09** — o GUIA diz que a fatorial está concluída; o README, o MANUAL e a lista de
  prioridades do próprio GUIA dizem que está pendente.
- **AUD-03** — o README de `Apresentacoes_IVS` se contradiz sobre qual deck é o atual.
- **AUD-02** — o deck de 98 slides não se reproduz pelo gerador, e o uso documentado do
  gerador o sobrescreve.
- **AUD-04** — o deck e o guia ainda citam caminhos anteriores à reorganização de `docs/`.
- **AUD-05** — o README de `atualizada/` atribui as 8 tabelas `renda_*` ao script errado.
- **AUD-06 · O3 (piorou)** — os geradores recentes voltaram a digitar medições no texto.
- **AUD-12 · AUD-13 · HIG-11 · HIG-13** — documentos dizem que o NB01 e o NB02 não importam o
  módulo (importam desde 21/08); contagens de testes defasadas; `estrutura_projeto.md` com a
  árvore antiga; commits citados que não existem.
- **HIG-09** — o dicionário do projeto dá V00398 como "queimado"; o dicionário do IBGE e o
  código dizem caçamba.
- **FAT-08 · FAT-09 · NB4-13** — o README de `fatorial/` promete um teste que cobre 1 de 37
  CSVs; o módulo chama o promax de "solução oficial" e o NB04 adota a Varimax; a limitação 8
  diz que o bloco 8b ainda não foi feito.
- **DEC-2 · DEC-3 · DEC-4** — o guia de apoio, escrito para quem não sabe análise fatorial,
  nunca define autovalor, matriz padrão × estrutura, nem MSA.
- **DOC-1** — a p. 58 do livro é generalizada além do exemplo para manter a razão de
  moradores com comunalidade 0,380.
- **AUD-14** — o relatório da EDA cita um "script de auditoria" com 286 valores conferidos
  que nunca foi versionado.

## Prioridade 4 — repositório e histórico

- **AUD-01** — a linha 2 do `.gitignore` perdeu a regra `banco_de_dados/*.csv`.
- **HIG-03** — `.claude/settings.local.json` está versionado apesar do `.gitignore`, e
  pré-aprova `git commit` e `python -c` para quem clonar. Não contém segredo.
- **AUD-10** — `package.json` está no `.gitignore`: quem clona não consegue regerar nenhum
  deck.
- **HIG-18** — `Claude-Session:` com URL em `a1b13d2` e `a6f05ca`. Removê-lo exige outra
  reescrita de histórico e novo *force push*: decisão sua.
- **HIG-17 · HIG-23** — 3 commits como "Pedro Soares" e 95 como "Pedro Dias Soares" (mesmo
  e-mail, mesma conta no GitHub); os 2 mais recentes ainda não foram enviados.
- **HIG-07 · HIG-08** — 597 MB em 5 worktrees órfãs da época do Windows, em
  `.claude/worktrees/` (fora do git). **Antes de apagá-las:** o único gerador do
  `Dicionario_Variaveis_IVS_Censo2022.xlsx` só existe dentro de uma delas.
- **HIG-16 · HIG-06 · HIG-02 · HIG-15** — 20 MiB de base morta no `.git`; `graphify-out/`
  com nomes duplicados NFC/NFD e grafo anterior à reorganização; 17 regras mortas no
  `.gitignore`; os notebooks da Fase 2, se reexecutados, recriam as bases V01042 na pasta
  ativa.

---

## Estado dos 22 achados da auditoria de 17/09

A auditoria anunciou 20; são 22 (D1–D7, O1–O3, F1–F9, L1–L3).

| Estado | Achados |
|---|---|
| Resolvido | D2, F9 |
| Parcial | D1, D3, D6, F4, L1, O2 |
| Aberto | D4, D5, D7, F1, F3, F5, F6, F8, L2, L3, O1 |
| Piorou | **F2** (o padrão frágil se espalhou para scripts novos) · **O3** (mais medições digitadas do que antes) |
| Premissa falsa | F7 — o `.gitignore` reinclui a entrega de propósito, na linha 45 |

E o item 3 de "O que não consegui verificar" — a camada fatorial contra implementação
independente — está **feito**, com o resultado descrito no sumário.

---

## O que foi verificado e passou

Para a próxima revisão não refazer.

- **Fatorial.** KMO e MSA idênticos a `factor_analyzer` (1e-16); Bartlett idêntico (1e-15);
  SMC idêntica; ACP em 1e-13; eixo principal contra implementação própria e contra minres em
  1e-6; promax contra `factor_analyzer` em 1e-4 (Φ 0,5215 × 0,5216). Os 19 CSVs do
  diagnóstico e os 18 CSVs e 5 figuras do NB04 reproduzem byte a byte.
- **Indicadores.** Todos os códigos de variável dos 26 indicadores existem no dicionário do
  IBGE; `pct_agua_inad`, `pct_analfab` e `pct_idoso_60mais` recalculados da base bruta batem
  sem divergência, inclusive nos NaN; `safe_div` nunca devolve infinito.
- **Notebooks 01 e 02.** Os 70 municípios casam sem duplicidade; a junção preserva as 109.032
  linhas; `CD_SIT × SITUACAO`, `CD_TIPO` e as divergências de FCU conferem com os brutos do
  IBGE; `Dados_sig` recalculado bate.
- **Âncoras.** 109.032 × 104 no `.db`; OK 106.281 · ZERADO 1.736 · SIGILOSO 1.015; 104.108
  no recorte urbano; 87.545 casos completos; 19.507 e 19.452 setores de FCU.
- **Documentação.** 134 links relativos nos Markdown versionados, nenhum quebrado; as cerca de 18
  citações de página do livro nos documentos de metodologia conferem, exceto a da p. 58
  (DOC-1); os caminhos citados nos prompts existem.
- **Deck.** 884 dos 898 números extraídos batem com os CSVs; as tabelas Brasil × ELSI e
  favela × restante batem linha a linha; os blocos 95–98 e o deck do critério de renda
  regeneram idênticos.
- **Repositório.** Nenhum segredo nos 657 blobs de texto do histórico; `git fsck` sem erros;
  os 98 commits com o mesmo e-mail e nenhum `Co-Authored-By`; num clone novo, 69 testes
  passam e 5 são pulados com mensagem clara porque a base bruta não está versionada.

## O que esta revisão não cobriu

1. **A reprodução completa da pipeline** (NB01, NB02 e todos os scripts num ambiente limpo)
   não rodou, por custo. O que a substitui em parte: o NB04 e o diagnóstico fatorial
   reproduzidos byte a byte, e os 74 testes.
2. **Verificação adversarial das frentes de indicadores, notebooks 01/02, documentação, deck
   e higiene.** Os achados dessas frentes têm a evidência de quem os levantou; conferi por
   conta própria IND-1 e os de higiene sobre o histórico.
3. **Cobertura parcial declarada pelas frentes:** 23 dos 26 indicadores não foram
   recalculados do zero; as figuras do NB02 não foram abertas; o GUIA, o MANUAL e o README
   não foram lidos linha a linha nesta rodada (a auditoria de 17/09 o fez); os geradores de
   deck foram conferidos pela saída, não pelo código; os slides 79 e 88 ficaram sem conferência.
4. **O R não está instalado.** O que se diz sobre o `psych` em FAT-02 e FAT-03 vem de
   emulação do algoritmo publicado, com confiança média.

## Próximos passos, se quiser

1. **Prioridade 1 inteira** — é o que a orientadora vai ver. A maior parte é texto e uma
   figura; nenhum número do índice muda.
2. **IND-1** e o teste que o trava.
3. **Salvar o gerador do dicionário** que está na worktree órfã, antes de qualquer limpeza.
4. **`.gitignore`, `settings.local.json`, `package.json`** — três correções de uma linha cada.
5. **Os trailers `Claude-Session`** — só se quiser uma nova reescrita de histórico.

As decisões metodológicas que esta revisão levanta — a métrica da repartição oblíqua, a
unidade da reamostragem, o papel da AUC — são da orientação, não do código.

---

## Apêndice — todos os achados, com evidência

Gerado a partir dos resultados das frentes. Cada achado traz a verificação que recebeu: "agente principal" é conferência independente por execução; "verificador" é o verificador adversarial da frente; sem marca, o achado tem só a evidência de quem o levantou.

### Notebook 04 e relatório (NB4)

#### NB4-01 — Bootstrap iid sustenta 'pesos estáveis', mas por município os pesos oscilam 10 pontos e o IC inclui 60/40

- **ERRO · confiança media**
- **Agente principal:** PARCIAL: reproduzi a sensibilidade a São Paulo (peso F1 65,04 → 62,91). O IC por reamostragem de municípios não foi refeito.
- **Onde:** notebook célula 24 (md) e 25 (ipynb:1230, 1293); relatório linhas 23 e 141-143 (item 2, Bloco 6)
- **Evidência:** O bootstrap do NB04 reamostra os 87.545 setores como se fossem independentes: reproduzi bit a bit (v6_bootstrap.py: diff 0, IC [64,70; 65,30], amplitude 0,593 pp). Mas o próprio relatório declara dependência espacial (limitação 5) e os setores estão agrupados em 70 municípios, e é essa a unidade amostral do ELSI. v9_cluster_bs.py, reamostrando municípios (300 reps): 'peso F1 IC95 [58.2; 68.2] amplitude 9.98 pp'; largura do IC da razão de moradores 0,512 (F1) e 0,743 (F2); 'fração das reamostragens em que alguma variável troca de dimensão: 0.327'. Só tirar São Paulo leva o peso a 62,91/37,09, e a razão de moradores passa para a dimensão de saneamento (padrão de dimensões '222111' contra '221111').
- **Impacto:** As frases 'Esses pesos são estáveis', 'A crítica de instabilidade que o livro faz [...] não se materializa' e 'Com 87 mil setores a incerteza amostral é desprezível' (relatório, linhas 23 e 143) não se sustentam. Com o IC por município, o 60/40 da literatura fica dentro da incerteza, e a filiação da razão de moradores fica em aberto. É um dos números de manchete que vão para a orientadora.
- **Correção sugerida:** Reportar o bootstrap por conglomerado (município), ou pelo menos o leave-one-municipality-out, ao lado do iid. Rebaixar 'estáveis' para 'estáveis à reamostragem de setores, sensíveis ao conjunto de municípios'. Registrar a instabilidade da razão de moradores.

#### NB4-02 — A AUC contra FCU não valida os pesos: renda sozinha, pesos iguais e pesos aleatórios separam igual ou melhor

- **ERRO · confiança media**
- **Agente principal:** CONFIRMADO: AUC do índice 0,8131; renda invertida sozinha 0,8819; média de postos com pesos iguais 0,8533 (18.901 setores FCU em 87.545).
- **Onde:** notebook célula 38 (md, ipynb:1867, 1876) e 39; relatório linha 27 (item 4) e linha 194 (decisão 6)
- **Evidência:** A AUC está calculada certo: v3_auc.py dá 0,813111 e 0,861557 pela fórmula do NB04 e pela contagem direta de pares, a orientação está correta e o índice não tem empates. O problema é o que ela prova. AUCs no mesmo conjunto: renda_inv sozinha 0,8819; cor/raça 0,8249; analfabetismo 0,8023; água 0,5611. Pesos iguais: 0,8187. Um fator: 0,8378. Só as 4 socioeconômicas: 0,8548. Em 200 vetores de peso aleatórios (Dirichlet), a mediana é 0,8140, o p95 é 0,8456 e 52% ficam em 0,8131 ou mais. O índice oficial (0,8131) fica na mediana dos pesos aleatórios e abaixo de uma única componente dele.
- **Impacto:** A célula 38 diz 'só isto diz se o índice acerta' e 'vale mais do que qualquer estatística interna'. Os números mostram que a AUC confirma o conteúdo socioeconômico das variáveis (sobretudo a renda), não a estrutura fatorial nem os pesos 65/35. Acrescentar saneamento chega a reduzir a separação. Usar a AUC como validação da fatorial é conclusão errada. Nota: não há vazamento, porque CD_TIPO não entra nos pesos. A sobreposição conceitual com os critérios do IBGE (serviços precários) tem pouco efeito empírico, já que a água tem AUC de 0,56.
- **Correção sugerida:** Reportar a AUC junto com linhas de base (renda sozinha, pesos iguais, distribuição de pesos aleatórios) e reescrever a leitura: 'o conjunto de variáveis separa FCU; a validação não discrimina entre esquemas de ponderação'.

#### NB4-03 — 'A oblíqua afasta os pesos da literatura' depende de somar quadrados da matriz padrão; pela estrutura dá 59,6/40,4

- **ERRO · confiança media**
- **Agente principal:** CONFIRMADO: pela matriz padrão, 65,82/34,18 (soma 4,367 > Σh² 4,198); pela matriz estrutura, 59,64/40,36.
- **Onde:** notebook célula 19 (função repartir aplicada a padrao), célula 18 item 3, célula 44 item 2 (ipynb:2159); relatório linhas 31 (item 6), 137 e 193
- **Evidência:** rep6_obl = SS(padrão)/total = 65,82/34,18 (v1_reproducao.py). A soma de quadrados da matriz padrão ignora Φ: ela soma 4,3675, mais que a variância comum explicada, Σh² = 4,1977. Pela matriz estrutura, a mesma conta dá 59,644/40,356 (v1: 'rep estrutura [59.644 40.356]'). A própria célula 18 justifica recalcular porque 'parte da variância é compartilhada', e a conta escolhida é justamente a que descarta a parte compartilhada.
- **Impacto:** O achado nº 6 ('A rotação oblíqua afasta os pesos da literatura, não os aproxima') e o 'custo 0,8 ponto percentual' da decisão 5 são artefato da métrica: com fatores correlacionados, nenhuma soma de quadrados é partição aditiva, e a outra escolha legítima inverte a conclusão.
- **Correção sugerida:** Declarar que, na solução oblíqua, a repartição não é bem definida. Apresentar padrão (65,8/34,2) e estrutura (59,6/40,4) lado a lado, ou retirar o achado nº 6.

#### NB4-04 — Leitura seletiva do livro nas p. 27 e 29: omite justamente as condições que o projeto satisfaz

- **ERRO · confiança media**
- **Agente principal:** CONFIRMADO no PDF do livro (índice 30): Kaiser é mais preciso "quando o tamanho da amostra é maior do que 250 e a média da comunalidade é maior ou igual a 0,6".
- **Onde:** notebook célula 11 (ipynb:539) e célula 15 (ipynb:730); relatório linhas 59, 106 e 110
- **Evidência:** p. 29 (texto extraído do PDF): Stevens diz que Kaiser é mais preciso 'quando o tamanho da amostra é maior do que 250 e a média da comunalidade é maior ou igual a 0,6'. Aqui n = 87.545 e a média das comunalidades com 2 fatores é 0,6212 (7 variáveis) e 0,6996 (6 variáveis) (v5_cenarios.py). O NB04 cita só a outra condição e conclui 'O critério de Kaiser é o mais fraco neste caso'; o relatório (l. 59) diz 'Kaiser é fraco com poucas variáveis (p. 29)', mas a página diz que Kaiser é mais preciso com MENOS de 30 variáveis. p. 27: Hair diz que ACP e AF convergem 'se as comunalidades excederem 0,60 para a maioria das variáveis'. Aqui 5 de 6 passam de 0,60 (0,822; 0,615; 0,770; 0,856; 0,754). O relatório (l. 110) diz 'Duas das três condições [...] falham' e o notebook, 'Cai no lado da divergência'.
- **Impacto:** A argumentação sobre número de fatores e extração cita o livro ao contrário do que ele permite concluir, e isso vai ser mostrado à orientadora. Os números não mudam: o teste ACP x PAF foi feito e diverge na água.
- **Correção sugerida:** Citar as duas condições de Stevens (p. 29) e as duas de Hair (p. 27), dizer quais o projeto satisfaz e reformular: 'pela regra de Hair esperava-se convergência; empiricamente ela falha na água'.

#### NB4-05 — 'Com Pearson a base reprovaria em dois critérios da Etapa 1': pela Tabela 7 do livro, reprova em um

- **ERRO · confiança media**
- **Onde:** notebook célula 6 (ipynb:262); relatório linha 46 (item 11)
- **Evidência:** Tabela 7 (p. 44-45, síntese da Etapa 1): tamanho amostral; 'A maioria dos coeficientes [...] maiores do que 0,3'; Bartlett p<0,05; KMO '0,5 como valor mínimo aceitável, mas o ideal seria um valor a partir de 0,7'. Com Pearson: 33,3% dos |r| ≥ 0,30 (reprova), Bartlett significativo (passa), KMO 0,7318 (passa, até no 'ideal'). O MSA mínimo de 0,542 também fica acima de 0,5. O segundo 'critério' do Guia de Leitura (l. 88) é a variância acumulada de 60%, que é da Etapa 2 e não da 1.
- **Impacto:** Exagera o custo da escolha por Pearson, que é o argumento para Spearman.
- **Correção sugerida:** Trocar por 'reprovaria no critério da maioria acima de 0,30 (Etapa 1) e ficaria abaixo dos 60% de variância acumulada (Etapa 2)'.

#### NB4-06 — 'Esgoto com renda a −0,454' vem da matriz par a par da EDA; na matriz fatorada o valor é +0,436

- **ERRO · confiança alta**
- **Agente principal:** CONFIRMADO: −0,454 é o par a par da EDA; na matriz fatorada, 0,436. O 0,429 da mesma frase é da matriz fatorada.
- **Onde:** notebook célula 18, markdown (ipynb:853)
- **Evidência:** banco_de_dados/eda/correlacao_spearman.csv: pct_esgoto_inad × renda_media = −0.454 (par a par, 104.108; recalculado −0,4535). nb04_correlacao_ivs7_spearman.csv, com a renda invertida e listwise: Esgoto × Renda (invertida) = 0.436 (v1: 0,4364). A figura nb04_matriz_correlacao.png imprime 0,44 nessa célula. O texto diz 'as próprias correlações mostram'.
- **Impacto:** Repete, dentro do NB04, o mesmo erro de procedência que a célula 6 do próprio notebook denuncia (número par a par citado como se fosse da matriz fatorada), e ainda com o sinal da renda não invertida.
- **Correção sugerida:** Trocar por 'esgoto com renda (invertida) a 0,436', o valor da matriz fatorada.

#### NB4-07 — 'Divergência de 0,836 no lixo' compara fatores diferentes da ACP e do eixo principal

- **ERRO · confiança alta**
- **Agente principal:** CONFIRMADO: em IVS7, ACP_2 do lixo = 0,8799 e PAF_2 = 0,0435, fatores diferentes; a diferença de comunalidade é 0,807.
- **Onde:** notebook célula 44, 'Um quarto ponto' (ipynb:2166-2167); célula 16 (print 'maior diferença absoluta: 0.836 em Lixo inadequado / dif_2'); nb04_extracao_comparada.csv
- **Evidência:** Com 7 variáveis, o fator 2 da ACP é o lixo ([0.049 0.135 0.88 −0.496 ...]) e o fator 2 do eixo principal é saneamento ([0.445 0.378 0.043 ...]). A congruência de Tucker entre os dois é 0,13 (v5_cenarios.py); com 6 variáveis ela é 0,982. comparar_extracao só alinha o sinal, não a correspondência. O 0,836 é |0,880 − 0,043| entre fatores distintos. O texto soma isso à comunalidade ('0,052 contra 0,859. A divergência de 0,836 [...]'), mas a diferença de comunalidade é 0,807.
- **Impacto:** O número citado como 'a maior divergência da tabela' não mede divergência de método. A conclusão de que o lixo tem pouca variância comum continua de pé (SMC 0,106; PAF com 3 fatores dá comunalidade 0,176 ao lixo).
- **Correção sugerida:** Apoiar o argumento só nas comunalidades (0,859 x 0,052) e na SMC. Na tabela de 7 variáveis, anotar que o dif_2 compara fatores não correspondentes (ou emparelhar as colunas por congruência).

#### NB4-08 — Figura do plano fatorial: eixo 'Fator 2 — saneamento' no painel de 7 componentes, onde o fator 2 é o lixo

- **ERRO · confiança alta**
- **Agente principal:** CONFIRMADO: em IVS7, Varimax2 do lixo = 0,9195; água e esgoto carregam no fator 1.
- **Onde:** notebook célula 22, linha 70 (ipynb:1186); banco_de_dados/eda/fatorial/figuras/nb04_plano_fatorial.png (painel esquerdo)
- **Evidência:** plano_fatorial() fixa ax.set_ylabel('Fator 2 — saneamento') nos dois painéis. No de 7 componentes, Varimax2 = lixo 0,919, água 0,144, esgoto 0,261, razão −0,373 (nb04_cargas_ivs7.csv): água e esgoto carregam no fator 1. A legenda compara o lixo ao item 7 do livro ('distante dos dois grupos'), mas no livro o item 7 'não pertence a nenhum fator', enquanto aqui o lixo sozinho DEFINE o fator 2.
- **Impacto:** A figura que vai para a orientadora rotula errado o eixo em que está o achado principal (o lixo como fator próprio).
- **Correção sugerida:** Rotular o eixo do painel de 7 como 'Fator 2 — lixo' (ou só 'Fator 2') e ajustar a analogia com o item 7.

#### NB4-09 — Comentário e relatório: 'divergência grande nas de SMC baixa, pequena em renda e cor/raça' não bate com a tabela

- **ERRO · confiança alta · introduzido depois da auditoria**
- **Agente principal:** CONFIRMADO: razão de moradores (SMC 0,233) dif_2 0,062; cor/raça (SMC 0,648) 0,111; analfabetismo (SMC 0,597) 0,140.
- **Onde:** notebook célula 16, comentário LEITURA (ipynb:821, criado em d3ee10b); relatório linha 118
- **Evidência:** nb04_extracao_comparada.csv (6 var): dif_2 da razão de moradores (SMC 0,233) = 0,0621, o 2º menor; cor/raça (SMC 0,648) = 0,1106, maior que o esgoto (0,0985); analfabetismo (SMC 0,597) = 0,1398, o 2º maior. Pela diferença de comunalidade, a razão (0,120) também fica abaixo do esgoto (0,184) e do analfabetismo (0,132). O comentário ainda conclui que isso 'é sinal de que a implementação está certa', o que não decorre.
- **Impacto:** É um comentário novo que descreve o resultado de forma errada; o relatório diz que em cor/raça 'as duas técnicas praticamente coincidem'.
- **Correção sugerida:** Restringir a leitura ao que a tabela mostra: a maior divergência é a da água (SMC mais baixa) e a menor, a da renda (SMC mais alta). O resto não segue a SMC. Retirar 'sinal de que a implementação está certa'.

#### NB4-10 — Comentário de Horn: 'com 20 mil linhas os autovalores aleatórios já estabilizaram' é falso

- **ERRO · confiança alta**
- **Agente principal:** CONFIRMADO: horn(20000, 6) = 1,0232 / 1,0119; horn(87545, 6) = 1,0104 / 1,0057.
- **Onde:** notebook célula 12, linhas 6-8 (ipynb:606)
- **Evidência:** v1_reproducao.py: horn(20000, 6) = [1.0232 1.0119 ...]; horn(87545, 6) = [1.0104 1.0057 ...]. Com 7 variáveis: 1.0259/1.0155 contra 1.0126/1.0075. Os autovalores aleatórios dependem de n (tendem a 1) e, com 20 mil, o limiar sobe cerca de 0,013.
- **Impacto:** Não muda nenhuma decisão (0,9585 < 1; 1,0486 > ambos), mas o comentário justifica o atalho com um fato errado.
- **Correção sugerida:** Reescrever: 'limitar a 20 mil torna o limiar de Horn ligeiramente conservador (≈+0,01); não altera a decisão'.

#### NB4-11 — Bloco 8b 'sem consequência' x commit 694c306: sob a normalização municipal do IVS, a troca de renda pesa em BH

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- **Onde:** notebook célula 36, comentário 'praticamente inócua' (ipynb:1836); relatório linhas 39-44 (item 10); banco_de_dados/eda/atualizada/README.md:38-40 (ec8f220) x :58-60 (694c306)
- **Evidência:** O 8b mede só o min-max GLOBAL. v4_extremo.py: renda_media_sem_extremo difere de renda_media em 1 linha só (setor 310620005650366, BH, 170.418,06 → NaN); as 278 mudanças vêm 100% do reescalonamento do min-max ('(a) só retirar o setor e refazer o min-max [...]: 278'; '(b) só os pesos da alternativa [...]: 0'). Com min-max POR MUNICÍPIO, que é a normalização planejada, mudam 774 de 87.544, sendo 387 de 3.963 setores de BH (9,8%), ou 98 com quartis internos a BH. O commit 694c306 mostra a escala de BH abrindo 3,8 vezes; o README da atualizada/ cita o '278 de 87.544' do NB04 e, 20 linhas abaixo, 'o intramunicipal não era [robusto]'.
- **Impacto:** O relatório declara 'A pendência da 2ª rodada da EDA fica resolvida [...] sem consequência'. Isso vale para a fatorial, que é invariante por construção (Spearman sem um de 87.545 setores), mas não para o índice sob a normalização que o IVS vai usar.
- **Correção sugerida:** Restringir a conclusão do item 10 à fatorial ('os pesos não mudam') e remeter o efeito sobre a classificação à normalização municipal (694c306 / NB05). Corrigir o README da atualizada/.

#### NB4-12 — Comentários novos chamam Varimax de 'solução oficial' e dizem que os pesos saem da padrão; o módulo diz que a oficial é a promax

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- *Duplicado de FAT-09; mantido pela evidência adicional.*
- **Onde:** notebook célula 28 (ipynb:1401) x célula 19 (ipynb:937); src/ivs_censo/fatorial.py:208-209; notebook célula 0 e relatório decisão 5 (linha 193)
- **Evidência:** Célula 28: '# A SOLUÇÃO OFICIAL: Varimax, 6 componentes'. Célula 19: '# padrão = coeficientes de regressão (de onde saem os pesos)'. fatorial.py:208-209 (docstring de varimax): 'Para a solução oficial, ver `rotacao_promax`'. Célula 0: 'se a solução oficial será ortogonal ou oblíqua' é decisão da orientação. Os pesos publicados (nb04_pesos.csv) saem da Varimax.
- **Impacto:** Três artefatos dão três respostas sobre qual rotação é a oficial e de qual matriz saem os pesos, num notebook que declara a decisão como aberta.
- **Correção sugerida:** Trocar 'SOLUÇÃO OFICIAL' por 'solução de referência (decisão 5 em aberto)', corrigir o comentário da célula 19 ('a matriz de onde sairiam os pesos numa solução oblíqua') e alinhar a docstring do módulo.

#### NB4-13 — Limitação 8 do notebook diz que a renda sem extremo 'não entrou' e que refazê-la 'é trabalho de uma rodada'; o bloco 8b já fez

- **DIVERGENTE · confiança alta**
- **Onde:** notebook célula 44, limitação 8 (ipynb:2209-2212) x células 33-36 (bloco 8b); relatório item 10 e lista de limitações (que já não traz esse item)
- **Evidência:** Limitação 8: '`renda_media_sem_extremo` não entrou [...] refazer a fatorial sobre a renda sem extremo é trabalho de uma rodada'. O bloco 8b refaz exatamente isso, e o relatório (l. 43) declara a pendência 'resolvida'. O texto é anterior ao 8b (existia antes de d3ee10b) e não foi atualizado quando o 8b entrou (00c0ee0).
- **Impacto:** O notebook se contradiz na seção de limitações que vai para a orientadora.
- **Correção sugerida:** Reescrever a limitação 8 remetendo ao 8b (e à ressalva do NB4-11), ou removê-la, como o relatório já fez.

#### NB4-14 — README de fatorial/: 'Se esse teste passa, as duas gerações concordam'; o teste não toca nenhum nb04_*

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- *Duplicado de FAT-08; mantido pela evidência adicional.*
- **Onde:** banco_de_dados/eda/fatorial/README.md:48 (ec8f220)
- **Evidência:** tests/test_fatorial.py:33 e 57-95 comparam só ivs7_spearman_cargas.csv (geração 1) e as travas de KMO/MSA/Bartlett. `grep -rn nb04_ tests/` não devolve nada. Nenhum teste lê nb04_pesos.csv, nb04_validacao_fcu.csv etc.
- **Impacto:** O README de procedência, criado para resolver O2, promete uma verificação que não existe para os 18 CSVs da geração 2, que são os que carregam os pesos e a AUC.
- **Correção sugerida:** Corrigir o texto ('o teste confere a geração 1; a geração 2 depende das travas internas do NB04') ou criar o teste que reproduza nb04_pesos.csv e nb04_validacao_fcu.csv a partir do .db.

#### NB4-15 — Contagens e arredondamentos do relatório que não batem com o notebook e os CSVs

- **DIVERGENTE · confiança alta**
- **Onde:** docs/relatorios/Relatorio_Analise_Fatorial_NB04.md linhas 19, 92, 115, 130, 131, 191, 194, 266
- **Evidência:** l.19 'Dez achados': a lista tem 11. l.92 'Bartlett χ² (21 g.l.)' vale para as três colunas, mas a de 6 componentes tem 15 g.l. (resumo_adequabilidade.csv: bartlett_gl 15). l.194 'reproduzível com sete números': são 6 pesos (nb04_sintese_pesos.csv). l.266 '8 testes': test_fatorial.py tem 9 funções test_. l.191 'Retirá-la: recupera-os' (16.563): a base sem analfabetismo recupera 16.548 (104.093 − 87.545). l.130/131/115: 0,454, 0,873 e 0,099 vêm de arredondamento duplo a partir do CSV de 4 casas; a precisão total é 0,453470, 0,872467 e 0,0985 (0,098), como o notebook imprime.
- **Impacto:** Baixo individualmente, mas são números citados à orientadora que não se reproduzem pela saída do notebook.
- **Correção sugerida:** Corrigir as cinco contagens e gerar as tabelas do relatório a partir dos valores em precisão total.

#### NB4-16 — A varimax para antes de convergir: a 4ª casa das cargas é espúria, e o 'batem até a quarta casa' do 8b fica abaixo da precisão

- **FRAGIL · confiança alta**
- *Duplicado de FAT-01; mantido pela evidência adicional.*
- **Onde:** src/ivs_censo/fatorial.py:223 (critério d/d_ant < 1+1e-6); CSVs nb04_cargas_*, nb04_bootstrap_cargas.csv, nb04_renda_sem_extremo_cargas.csv; notebook célula 35 (ipynb:1778, comentário de d3ee10b); relatório linha 40
- **Evidência:** v8_varimax_conv.py: critério varimax 0,190705391 (módulo) x 0,190705641 (ótimo por busca do ângulo). 'max |módulo − grade| = 0.000555'; ex.: cor/raça F2 0,2446 x 0,2451; água F1 0,0869 x 0,0864. Com tol=1e-14 o erro cai para 2,4e-7. factor_analyzer (normalize=False) difere 2,5e-3 na varimax e 4,5e-4 na promax. No 8b, a saída impressa mostra 0,1369 x 0,1368, contra o comentário 'as cargas batem até a quarta casa'.
- **Impacto:** Números com 4 casas (e pesos com 6) dão precisão que o algoritmo não entrega. As larguras do IC do bootstrap (0,0038 na renda) ficam da ordem do ruído de convergência. A repartição muda pouco (65,038 x 65,011).
- **Correção sugerida:** Apertar a tolerância da varimax (por exemplo, 1e-10 sobre a variação da rotação) e regerar; ou publicar 3 casas e retirar 'até a quarta casa'. Obs.: mudar a tolerância quebra a igualdade com os CSVs de agosto (teste com atol 1e-6).

#### NB4-17 — Filtro urbano com astype(str)=='1' no NB04, mesmo padrão do F2, e o comentário novo diz que isso 'normaliza'

- **FRAGIL · confiança alta**
- **Onde:** notebook célula 4, linhas 15-16 (ipynb:208) e linha 7 (ipynb:200)
- **Evidência:** `df = bruto[(bruto['urbano'].astype(str) == '1') & ...]` com o comentário novo '`urbano` vem como inteiro; astype(str) o normaliza para comparar com '1''. Hoje urbano é int64 sem nulos (v1: 'dtypes urbano ... int64 | nulos urbano: 0'); um nulo futuro a promove a float e astype(str) dá '1.0'. O F2 da auditoria lista renda.py, proporcoes_brasil.py e diagnostico_fatorial.py, não o NB04. Na mesma célula, 'sqlite3.connect(CAMINHO_DB) # abre o SQLite (só leitura, na prática)': connect abre para escrita e cria um .db vazio se o caminho faltar.
- **Impacto:** O recorte pode zerar sem erro. Mas a trava assert len(df)==104_108, logo abaixo, pegaria o caso, o que reduz o risco.
- **Correção sugerida:** Usar pd.to_numeric(bruto['urbano'], errors='coerce').eq(1), como a célula 39 já faz com CD_TIPO, e abrir o banco com 'file:...?mode=ro' via uri=True. Corrigir o comentário.

#### NB4-18 — Número de fatores: com n=87 mil, Horn é quase o próprio Kaiser, e sob a normalização municipal os dois retêm 2 fatores

- **LACUNA · confiança alta**
- **Onde:** notebook célula 11 (ipynb:546), célula 31 (ipynb:1536), célula 44 decisão 4; relatório linhas 106 e 192
- **Evidência:** Horn com n=87.545: 1,0104 / 1,0057 (v1_reproducao.py), ou seja, Kaiser + 0,01. 'Kaiser e Horn concordam' é um critério contado duas vezes. resumo_adequabilidade.csv, cenário ivs6_sem_lixo_minmax_municipal_spearman: autovalores_acima_1 = 2 e autovalores_acima_horn = 2 (2º autovalor 1,1977 em ivs6_sem_lixo_minmax_municipal_spearman_autovalores.csv). Nada disso aparece na decisão 4 ('Kaiser e Horn dizem um na solução sem lixo; a teoria diz dois').
- **Impacto:** A orientadora recebe 'dois critérios empíricos contra a teoria', quando é um critério só e o resultado se inverte na escala em que o IVS vai ser calculado.
- **Correção sugerida:** Na decisão 4, registrar que Horn ≈ Kaiser com este n e que, sobre os dados normalizados por município, Kaiser e Horn retêm 2 fatores.

#### NB4-19 — A validação por FCU só é reportada no agregado; por município vai de 0,50 a 0,94

- **LACUNA · confiança alta**
- **Onde:** notebook célula 39; nb04_validacao_fcu.csv; relatório Bloco 9
- **Evidência:** v3_auc.py: 42 dos 70 municípios têm FCU; os 5 maiores concentram 59% dos setores FCU. AUC intramunicipal (só pares do mesmo município) = 0,8966, o que mostra que o agregado não está inflado. Por município: São Paulo 0,944, Rio 0,854, BH 0,919, mas Belém 0,583, Manaus 0,632, São José de Ribamar 0,584, Duque de Caxias 0,501. Com min-max municipal, a AUC agregada é 0,824.
- **Impacto:** A leitura 'o índice separa os territórios sabidamente vulneráveis' esconde que nas duas capitais do Norte com mais FCU a separação é fraca, o que é relevante para um índice intraurbano.
- **Correção sugerida:** Acrescentar a AUC intramunicipal e a distribuição por município (ao menos para os com mais de 100 setores FCU) ao CSV e ao relatório.

#### NB4-20 — Convenção de sinal diferente entre os CSVs nb04_: a mesma carga sai +0,0869 num e −0,0869 noutro

- **HIGIENE · confiança alta**
- *Duplicado de FAT-10; mantido pela evidência adicional.*
- **Onde:** banco_de_dados/eda/fatorial/nb04_bootstrap_cargas.csv e nb04_extracao_comparada.csv x nb04_cargas_ivs6_sem_lixo.csv e nb04_pesos.csv
- **Evidência:** nb04_cargas_ivs6_sem_lixo.csv: Água Varimax1 = 0.0869, Renda 0.9152 (com o sinal virado, 'positiva = mais vulnerável'). nb04_bootstrap_cargas.csv: Água carga_F1 = −0.0869, Renda −0.9152. nb04_extracao_comparada.csv: ACP_1 todo negativo. O relatório (l. 124) promete 'Sinais ajustados para que carga positiva signifique maior vulnerabilidade'.
- **Impacto:** Quem lê os CSVs direto (deck, R) encontra a mesma carga com sinais opostos, sem aviso no README.
- **Correção sugerida:** Aplicar a mesma convenção de sinal a todos os nb04_* ou declarar no README quais guardam o sinal cru.

#### NB4-21 — Comentário novo descreve uma dependência que não existe, e há um import morto

- **HIGIENE · confiança media · introduzido depois da auditoria**
- **Onde:** notebook célula 42, linhas 3-4 (ipynb:2060); célula 3, import (ipynb:122-125)
- **Evidência:** 'final = pesos.copy() # cópia: o original segue com a dimensão numérica, que os cenários do bloco 8 ainda usam': o bloco 8 (célula 32) já rodou antes da célula 42 e não é reexecutado. `matriz_correlacao` é importada e nunca usada; a única ocorrência é o nome do arquivo 'nb04_matriz_correlacao.png'.
- **Impacto:** Mínimo. É justamente o tipo de comentário que descreve o código errado.
- **Correção sugerida:** Trocar por 'cópia: não altera `pesos`, que é a tabela gravada em nb04_pesos.csv' e remover o import.

#### NB4-22 — Estimar os pesos nos brutos agregados e aplicá-los ao min-max municipal junta duas estruturas diferentes

- **OPINIAO · confiança media**
- **Onde:** notebook célula 27 (md) e limitação 7 (ipynb:1338, 2208); relatório linha 65
- **Evidência:** A decisão é declarada: 'normalizar antes derruba o KMO de 0,783 para 0,720 [...] por isso a fatorial roda sobre os brutos'. Os números conferem (resumo_adequabilidade.csv; 55,7/44,3 recalculado das cargas municipais). Mas v10_municipal.py mostra que a variância entre municípios é η² = 0,469 na água e 0,478 na cor/raça (postos), e a normalização municipal descarta exatamente essa parte. Na estrutura intramunicipal, o analfabetismo carrega 0,61/0,52 e a repartição é 55/45. Aplicar os pesos dos brutos em vez dos intramunicipais ao min-max municipal troca 6.654 setores de quartil (6.318 com quartis por município).
- **Impacto:** Escolher a base da fatorial por dar KMO maior, e não por coerência com a escala em que o índice será composto, é discutível. O custo é da mesma ordem que o do cenário 'sem analfabetismo'.
- **Correção sugerida:** Levar à orientação como decisão explícita, com esse custo medido, e não como 'já medido e resolvido'.

#### NB4-23 — O peso de cada dimensão inclui as cargas cruzadas de variáveis que não pertencem a ela

- **OPINIAO · confiança baixa**
- **Onde:** notebook célula 28 (montar_pesos com rep6_ort); célula 27, 'Composição dos pesos'
- **Evidência:** rep6_ort soma os quadrados de TODAS as cargas de cada fator: o F2 recebe 0,312² da razão e 0,245² da cor/raça, mas distribui o peso só entre água e esgoto. Contando só as variáveis-membro, a repartição seria 66,82/33,18 contra 65,04/34,96 (script inline em scratchpad).
- **Impacto:** Pequeno (1,8 ponto), mas mistura dois critérios. Está declarado e é defensável.
- **Correção sugerida:** Declarar a escolha e, se for mantida, justificar por que carga cruzada conta para a dimensão alheia.

#### NB4-24 — Seção reflexivo x formativo: 'explica e justifica' os 2,5% por um argumento que não decorre

- **OPINIAO · confiança baixa**
- **Onde:** notebook célula 43, parágrafos finais; relatório linhas 240-252
- **Evidência:** 'Isso explica, e agora justifica, por que a escolha entre 65/35 e 60/40 custa apenas 2,5% dos setores: ela nunca foi uma questão empírica.' O custo baixo decorre de os dois vetores de peso serem próximos e das dimensões serem correlacionadas (Φ = 0,522; Spearman 0,9993 entre os índices), não do estatuto formativo. Φ = 0,52 também é compatível com um fator reflexivo de 2ª ordem.
- **Impacto:** Argumento conceitual apresentado como consequência dos dados.
- **Correção sugerida:** Separar as duas coisas: o custo pequeno é empírico, e a legitimidade de 65/35 x 60/40 é conceitual.

### Camada fatorial (matemática) (FAT)

#### FAT-01 — A Varimax para antes de convergir: cargas da solução de 6 variáveis erradas na 4ª casa (e numa célula, na 3ª)

- **ERRO · confiança alta**
- **Agente principal:** CONFIRMADO por recálculo independente: max|dif| de 0,000555 em IVS6 e 0,000038 em IVS7; critério 0,19070539 × 0,19070564.
- **Onde:** src/ivs_censo/fatorial.py:205-226 (critério da linha 223); saídas: banco_de_dados/eda/fatorial/nb04_cargas_ivs6_sem_lixo.csv, nb04_bootstrap_cargas.csv, nb04_pesos.csv, nb04_sintese_pesos.csv, ivs6_sem_lixo_spearman_cargas.csv
- **Evidência:** $FAT/varimax_conv.py. Em R6 (6 variáveis), o critério da linha 223 (d/d_ant < 1+1e-6, com d = soma dos valores singulares) para na iteração 26; a convergência real leva 63. max|módulo − convergido| = 0,000555 (em R7, só 0,000038). Critério Varimax: 0,19070539 no módulo contra 0,19070564 no convergido; a busca exaustiva do ângulo dá 0,19070564, o que confirma que o módulo parou antes do ótimo. Cargas em 4 casas, módulo × convergido: Água F1 −0,0869 × −0,0864; Analfab. F2 0,1266 × 0,1271; Renda F2 0,1369 × 0,1374; Cor/raça F2 0,2446 × 0,2451. Em 3 casas, ivs6_sem_lixo_spearman_cargas.csv grava Água Varimax1 = −0,087, e o convergido é −0,08635, que arredonda para −0,086. Repartição: 65,038/34,962 × 65,011/34,989. Pesos: esgoto 0,1264 → 0,1266 e cor/raça 0,1757 → 0,1756 ($FAT/convencoes.py). No bootstrap ($FAT/boot_check.py), cada réplica erra em mediana 0,00055; os limites dos IC mudam até 0,00038; a amplitude do IC da repartição vai de 0,593 para 0,569 ponto percentual. O R, com o padrão eps=1e-5 de stats::varimax, difere 0,00247 do módulo em R6 ($FAT/convencoes.py). Isso contradiz docs/metodologia/Codigo_Analise_Fatorial_Comentado.md:249, que diz 'varimax(cargas, normalize = FALSE) # equivale ao código acima'.
- **Impacto:** Baixo nas conclusões: 65,0/35,0 se mantém com uma casa, e os pesos mudam na 4ª casa. Mas os CSVs publicam de 4 a 6 casas que não são a solução Varimax nessa precisão. O ruído de 5,5e-4 por réplica equivale a 12–15% da largura dos IC mais estreitos (renda F1 0,0038; analfab. F1 0,0046), e o deck cita '0,59 ponto de amplitude'. O teste de CSV compara com 3 casas e só no cenário de 7 variáveis, onde o erro é de 4e-5: por isso não detecta nada.
- **Correção sugerida:** Trocar o critério de parada por um que meça a variação da rotação (por exemplo, max|R_novo − R| < 1e-10) ou baixar tol para 1e-12 e subir maxiter. Depois, regenerar o diagnóstico e o NB04 e atualizar as travas. Se a decisão for manter tol=1e-6 para reproduzir agosto, declarar no docstring o erro de cerca de 5e-4 em IVS6 e publicar essas cargas com 3 casas. Corrigir também a linha 249 do documento R: para bater com o R, é preciso eps menor.

#### FAT-02 — A reprodução em R documentada não daria o Φ = 0,522 do NB04: ela troca a extração (PAF) e a normalização do promax, e a tabela de diferenças omite as duas coisas

- **DIVERGENTE · confiança alta**
- **Onde:** docs/metodologia/Codigo_Analise_Fatorial_Comentado.md:292-293, 399-402 e 423-434; scripts/gerar_deck_fatorial.js:483-485; src/ivs_censo/fatorial.py:229-267 (docstring de rotacao_promax); NB04, célula 19 (promax sobre cargas de ACP)
- **Evidência:** O NB04 aplica o promax sobre cargas de ACP, sem normalização de Kaiser em nenhuma etapa. O script R do documento roda fa(R, 2, fm='pa', rotate='promax'), que é fator comum mais promax com kaiser(). Executado ($FAT/phi_extracao.py), o Φ em IVS6 dá: ACP sem Kaiser 0,5215; ACP com Kaiser 0,5141; PAF sem Kaiser 0,6823; PAF com Kaiser 0,6400; factor_analyzer minres+promax (padrão) 0,6399, com max|carga padrão| = 1,062 (renda). Em IVS7: 0,1506 no NB04, 0,6842 no factor_analyzer. Emulando o laço fm='pa' do psych (min.err=0,001, max.iter=50), o Φ em IVS6 fica em 0,646 e as comunalidades diferem até 0,028 das do módulo ($FAT/psych_pa_h.py). O deck (linha 485) mapeia rotacao_promax a 'stats::promax(L, m = 4)', que usa varimax(normalize=TRUE): Φ 0,1097 contra 0,1506 em IVS7, e cargas padrão com diferença de até 0,045 ($FAT/convencoes.py). A tabela 'O que esperar de diferente' (linhas 423-431) não lista extração, normalização do promax nem critério de parada do PAF, e a linha 433 diz que qualquer divergência além dos 5 pontos 'é real'. O docstring de rotacao_promax não declara que o promax roda sem normalização de Kaiser, ao contrário do SPSS, do psych, do factor_analyzer e do stats::promax.
- **Impacto:** Quem rodar a conferência independente documentada vai achar Φ perto de 0,64 e uma carga padrão acima de 1 (renda ≈ 1,06), contra o que o relatório afirma: 'correlacionados a 0,522' (Relatorio_Analise_Fatorial_NB04.md:29) e 'nenhuma passa de 1' (:135). O documento o levará a tratar isso como erro. Há também um ponto substantivo: 0,522 é a correlação entre componentes principais rotacionados. No modelo de fator comum, a que se refere a recomendação de rotação oblíqua da p. 38, o valor fica entre 0,64 e 0,68.
- **Correção sugerida:** Escolher e declarar a convenção. Ou o script R usa principal(R, 2, rotate='none') seguido de promax com varimax(normalize=FALSE) implementado à mão, ou o NB04 publica também o Φ sob fator comum. Acrescentar à tabela de diferenças três linhas: extração ACP × PA; promax com e sem Kaiser; parada do PAF (psych: 0,001 na soma, 50 iterações; módulo: 1e-7 no máximo). Declarar no docstring de rotacao_promax a ausência de normalização e que Φ depende da extração.

#### FAT-03 — O Horn do script R (fa.parallel com fa='fa') não é o critério do módulo e, com n = 87 mil, reteria 3 ou 4 fatores, não 1 ou 2

- **DIVERGENTE · confiança media**
- **Onde:** docs/metodologia/Codigo_Analise_Fatorial_Comentado.md:391 e 430; src/ivs_censo/fatorial.py:187-199
- **Evidência:** O módulo compara autovalores de componentes principais (matriz com 1 na diagonal) com a média de dados normais. O script R usa fa.parallel(..., fa='fa'), que compara autovalores da matriz REDUZIDA. Emulado ($FAT/horn_fa.py, 30 simulações com o n real), em duas variantes de matriz reduzida (SMC na diagonal; comunalidades de PAF de 1 fator), a decisão é: IVS7 retém 4, pela média e pelo p95; IVS6 retém 3, pela média e pelo p95. Os autovalores reduzidos de IVS6 são 2,78, 0,31, 0,026… contra valores aleatórios de 0,011, 0,006, 0,002. Já o critério do módulo é robusto: 2 fatores em IVS7 e 1 em IVS6 com média ou p95, n=20.000 ou 87.545, normal ou permutação, e 20 sementes ($FAT/horn_sens.py). A linha 430 afirma que 'a decisão de quantos reter não deve mudar'.
- **Impacto:** O relatório apoia a retenção do 2º fator 'inteiramente na razão teórica', porque 'Kaiser e Horn retêm um só' (Relatorio_Analise_Fatorial_NB04.md:106). A conferência em R documentada diria outra coisa, e o documento promete que não diria.
- **Correção sugerida:** Trocar a linha 391 por fa.parallel(X, fa='pc', n.iter=50, cor='spearman') para reproduzir o critério do módulo, ou registrar que o FA-parallel com n grande retém mais e por quê. Corrigir a linha 430.

#### FAT-08 — O README de fatorial/ promete que um teste garante a concordância das duas gerações; o teste cobre 1 dos 37 CSVs

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- **Onde:** banco_de_dados/eda/fatorial/README.md:45-48
- **Evidência:** O README diz: 'tests/test_fatorial.py reproduz ivs7_spearman_cargas.csv… com tolerância de 1e-6. Se esse teste passa, as duas gerações concordam.' Mas test_acp_varimax_reproduz_csv lê um único arquivo, da geração 1 (tests/test_fatorial.py:33, 90-95), compara com 3 casas e não toca nenhum dos 18 nb04_*. Hoje as duas gerações de fato estão corretas: reexecutei cópias do diagnostico_fatorial.py e do NB04 gravando no scratch, e os 37 CSVs e as 5 PNGs saíram idênticos byte a byte. Mas não é o teste que garante isso.
- **Impacto:** Dá falsa segurança. Uma regressão que altere só as saídas do NB04 (promax, PAF, bootstrap, pesos, escores) passa no teste citado como garantia.
- **Correção sugerida:** Reescrever a frase: o teste garante que o módulo reproduz as cargas de ACP e Varimax de ivs7_spearman em 3 casas, e a coerência das saídas nb04_* só se confere reexecutando o NB04. Ou criar um teste que confira ao menos nb04_cargas_ivs6_sem_lixo.csv e nb04_phi_ivs6_sem_lixo.csv.

#### FAT-09 — O módulo chama o promax de 'solução oficial'; o NB04 e o relatório adotam a Varimax

- **DIVERGENTE · confiança alta**
- **Onde:** src/ivs_censo/fatorial.py:206-209 (e 27-29) × notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb, célula 28 (linha 1401 do JSON)
- **Evidência:** O docstring da varimax diz: 'Mantida por reprodutibilidade… e como termo de comparação. Para a solução oficial, ver `rotacao_promax`'. O NB04, célula 28, diz: '# A SOLUÇÃO OFICIAL: Varimax, 6 componentes, repartição empírica'. Os pesos em nb04_pesos.csv e nb04_sintese_pesos.csv saem da Varimax.
- **Impacto:** Quem lê o módulo conclui que os pesos vêm do promax, o que é falso. Isso agrava FAT-04, porque o mesmo docstring manda usar a matriz padrão.
- **Correção sugerida:** Alinhar o docstring à decisão do NB04 (Varimax oficial, promax como sensibilidade), ou registrar que a escolha segue em aberto (decisão 5 do relatório).

#### FAT-10 — Dois CSVs do NB04 publicam a mesma solução Varimax com sinais opostos

- **DIVERGENTE · confiança alta**
- **Onde:** banco_de_dados/eda/fatorial/nb04_bootstrap_cargas.csv × nb04_cargas_ivs6_sem_lixo.csv
- **Evidência:** nb04_cargas_ivs6_sem_lixo.csv traz Varimax1 = 0,0869 / 0,3921 / 0,5322 / 0,8684 / 0,9152 / 0,833, com o sinal invertido pelo NB04. nb04_bootstrap_cargas.csv traz carga_F1 = −0,0869 … −0,9152, com IC negativos, porque bootstrap_cargas devolve o sinal cru do LAPACK. O deck contorna com Math.abs e troca inf/sup (scripts/gerar_deck_fatorial.js:346-347).
- **Impacto:** Pequeno hoje. O contorno só funciona porque todas as cargas de F1 têm o mesmo sinal e nenhum IC cruza o zero. Um IC que cruzasse o zero sairia errado no deck, e quem lê os dois CSVs vê sinais conflitantes.
- **Correção sugerida:** Aplicar no NB04 a mesma convenção de sinal (soma positiva) a bs['cargas'] e aos limites dos IC antes de gravar, ou parametrizar a convenção em bootstrap_cargas.

#### FAT-04 — escores_regressao aceita a matriz padrão numa solução oblíqua e devolve escores errados; o certo é R⁻¹·estrutura

- **FRAGIL · confiança alta**
- **Onde:** src/ivs_censo/fatorial.py:283-297 (docstring 'B = R⁻¹A'); src/ivs_censo/fatorial.py:243-244 ('padrão… é dela que saem os pesos do índice')
- **Evidência:** Pelo estimador de regressão de Thurstone, W = R⁻¹S, com S = PΦ (Grice, 2001). O factor_analyzer 0.5.1 faz isso em FactorAnalyzer.transform ('use the structure matrix, if it exists', seguido de np.linalg.solve(self.corr_, structure)). Nos postos reais de IVS6 ($FAT/escores_obliquos.py): com R⁻¹P, variância 1,3736, corr(F1,F2) = +0,5215 com Φ = −0,5215 (sinal trocado) e max|corr(Z,escore) − estrutura| = 0,494; com R⁻¹S, variância 1,0000, corr = Φ exatamente e erro 0,0000. A leitura literal do livro, p. 25 ('pelo inverso da matriz de correlação entre os fatores quando eles são oblíquos'), dá variância 4,71 e corr +0,94. Nenhum teste cobre o caso oblíquo.
- **Impacto:** Hoje está correto, porque o NB04 calcula os escores com Varimax. A troca para rotação oblíqua é previsível: é a decisão nº 5 em aberto do relatório, e o módulo chama o promax de 'o caminho que exige prova'. Nessa troca, passar a padrão, que é a matriz que o próprio docstring manda usar, gera escores com variância errada e correlação entre fatores de sinal invertido, sem erro nenhum na tela.
- **Correção sugerida:** Acrescentar um parâmetro phi opcional (B = R⁻¹·P·Φ quando informado), ou documentar que em solução oblíqua deve entrar a ESTRUTURA. Acrescentar um teste: com promax sobre ACP, os escores têm variância 1 e correlação igual a Φ.

#### FAT-06 — No caso de Heywood, o eixo principal devolve cargas incoerentes com as comunalidades e ainda marca 'convergiu'

- **FRAGIL · confiança alta**
- **Onde:** src/ivs_censo/fatorial.py:172-184
- **Evidência:** $FAT/heywood.py, com R = [[1,.8,.7],[.8,1,.5],[.7,.5,1]] e k=1 (comunalidade exata 0,8·0,7/0,5 = 1,12): h = [0,999; 0,6017; 0,4550], mas a soma dos quadrados das cargas devolvidas dá [1,0228; …]; info = {convergiu: True, heywood: True}. As cargas vêm da decomposição anterior ao corte (linha 172), e só h é cortado (linha 176). Nenhum teste exercita o sinalizador: a mutação 'heywood = False' sobrevive ($FAT/mutantes.py).
- **Impacto:** Não afeta os dados reais: em IVS6 e IVS7 não há Heywood. Mas qualquer uso futuro (mais fatores, outro recorte) recebe uma carga acima de 1 numa solução ortogonal sem rotação, junto com h ≤ 0,999 e 'convergiu=True'. comunalidades_obliquas calculada sobre essas cargas também não bateria com h.
- **Correção sugerida:** Com o teto acionado, devolver cargas coerentes (reescalar as linhas para ||linha||² = h) ou devolver convergiu=False. Acrescentar um teste com a matriz 3×3 acima.

#### FAT-12 — chi2_sf (Wilson–Hilferty) erra por ordens de grandeza na cauda, com os gl que o projeto usa

- **FRAGIL · confiança alta**
- **Onde:** src/ivs_censo/fatorial.py:74-77
- **Evidência:** Contra scipy.stats.chi2.sf ($FAT/heywood.py): gl=21, x=105 dá 1,24e-12 contra 3,73e-13; gl=15, x=75 dá 1,30e-9 contra 5,66e-10; gl=1, x=30 dá 3,9e-7 contra 4,3e-8. Perto de 0,05 o erro fica entre 1% e 5%. O docstring diz 'exata o bastante com df alto', mas o projeto usa gl 15 e 21.
- **Impacto:** Nulo hoje: com qui-quadrado acima de 139 mil, o p sai 0,0. Passaria a importar num recorte pequeno (município, outro n) em que o p caia entre 1e-6 e 1e-12 e fosse citado.
- **Correção sugerida:** Implementar a função gama incompleta regularizada (série ou fração contínua, poucas linhas em math) ou declarar no docstring que o valor serve só para dizer 'p < 1e-6'.

#### FAT-05 — O cheque de admissibilidade da p. 22 é tautológico com cargas de ACP: a variância residual oblíqua não tem como ficar negativa

- **LACUNA · confiança alta**
- **Onde:** src/ivs_censo/fatorial.py:249-252 e 270-277; notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb, célula 19 (asserts de var_residual > 0)
- **Evidência:** Para qualquer transformação inversível T, P = LT e Φ = (TᵀT)⁻¹ dão diag(PΦPᵀ) = diag(LLᵀ). Medido: max|comun_obliqua − comun_ortogonal| = 1,1e-16 ($FAT/compara_fa.py), e o próprio test_promax_preserva_comunalidade_e_expoe_phi prova essa identidade. Com ACP, diag(LLᵀ) ≤ 1 sempre, logo 'var_residual' ≥ 0 por construção, e os asserts do NB04 não podem falhar. O teste da p. 22 (Matos & Rodrigues, citando Muthén) trata da variância residual ESTIMADA num modelo de fator comum. Sob PAF com promax, renda tem carga padrão de 1,06 ($FAT/phi_extracao.py): é justamente o caso em que o cheque seria necessário.
- **Impacto:** O relatório apresenta 'todas as residuais são positivas de qualquer modo' (Relatorio_Analise_Fatorial_NB04.md:135) como evidência de admissibilidade. Com a extração usada, o resultado é garantido de antemão e não informa nada.
- **Correção sugerida:** Declarar no docstring que, sobre ACP, o cheque é identicamente satisfeito e só tem conteúdo sobre uma extração de fator comum (PAF). Se a solução oblíqua for adotada, rodar o cheque sobre as cargas de PAF.

#### FAT-07 — A suíte da camada fatorial deixa passar 12 de 21 regressões plausíveis; promax, Horn, bootstrap e Bartlett (gl e p) não estão travados

- **LACUNA · confiança alta**
- **Onde:** tests/test_fatorial.py (as 9 funções)
- **Evidência:** $FAT/mutantes.py roda cada mutação numa cópia do módulo. Sobrevivem: promax com kappa=2; alvo do promax sem o sinal; estrutura = padrão; gl do Bartlett = p(p+1)/2; p-valor do Bartlett fixo em 1; chi2_sf com o sinal trocado; semente do Horn trocada; Horn devolvendo zeros; Heywood nunca sinalizado; alinhar_cargas sem inverter sinal; bootstrap sem alinhar; percentis 5/95 no lugar de 2,5/97,5; e Horn com n cheio no diagnosticar (13 itens; a do Heywood já está em FAT-06). São mortas: Varimax sem o termo /p; promax sem reescala; escores sem R⁻¹; KMO sem zerar a diagonal; PAF com uma iteração; comunalidade oblíqua como soma de quadrados; tol da Varimax = 1e-3; SMC com diag(R). Os testes de promax só verificam invariantes que valem para qualquer T (diag Φ = 1, comunalidade preservada, S = PΦ), além de Φ ≈ 0 numa matriz bloco-diagonal. Nenhum valor de Φ, P ou S está travado. O 'atol=1e-6' do teste de CSV compara valores já arredondados a 3 casas: a tolerância efetiva é o arredondamento. No bootstrap real, nenhuma das 1.000 réplicas veio com ordem ou sinal trocados ($FAT/boot_check.py), então o código de alinhamento nunca foi exercitado, nem nos dados nem nos testes.
- **Impacto:** Φ = 0,522, os IC do bootstrap, o número de fatores pelo Horn e o grau de liberdade do Bartlett podem mudar em silêncio. Os números citados no relatório e no deck não têm trava automática: o NB04 só verifica KMO, MSA mínimo e o qui-quadrado.
- **Correção sugerida:** Acrescentar, no mínimo: um teste de referência que trave P, S e Φ de IVS6 (0,5215) e as cargas do eixo principal; um teste de horn (valores com semente fixa, e a decisão 2/1); um teste de bootstrap_cargas com n_rep pequeno que force troca de sinal e de ordem (por exemplo, invertendo e permutando colunas antes de alinhar); e um teste do gl e do p do Bartlett contra um valor conhecido.

#### FAT-11 — A 'repartição oblíqua' (soma dos quadrados da matriz padrão) não é uma partição da variância quando os fatores se correlacionam

- **OPINIAO · confiança media**
- **Onde:** src/ivs_censo/fatorial.py:371-373 e 390-392 (bootstrap_cargas com rotacao='promax'); NB04, célula 19 (repartir(padrao))
- **Evidência:** Em IVS6, a soma das colunas de P² é 2,8746 + 1,4928 = 4,367, mas a soma das comunalidades é 4,198. A diferença é a contribuição conjunta 2Σφ·p_i1·p_i2, que é negativa. A razão também depende da convenção de normalização: 65,82/34,18 sem Kaiser contra 66,12/33,88 com Kaiser ($FAT/compara_fa.py).
- **Impacto:** O '65,8/34,2 na oblíqua' do relatório (linhas 31 e 137) é comparado ao 65,0/35,0 ortogonal como se fosse a mesma grandeza. A conclusão ('não aproxima da literatura') não muda.
- **Correção sugerida:** Declarar que, na oblíqua, a repartição usa as contribuições diretas (SS da padrão) e ignora a parte conjunta, ou reportar também a SS da estrutura.

#### FAT-13 — O Bartlett é aplicado a uma matriz de Spearman sem ressalva distribucional

- **OPINIAO · confiança baixa**
- **Onde:** src/ivs_censo/fatorial.py:80-99; scripts/diagnostico_fatorial.py:88
- **Evidência:** A aproximação qui-quadrado de −(n−1−(2p+5)/6)·ln|R| supõe correlações de Pearson sob normalidade multivariada. Aqui R é de Spearman, sobre variáveis com massa em zero. O docstring só traz a ressalva do n grande (p. 43).
- **Impacto:** Nenhum na decisão: o teste rejeita por qualquer critério com n = 87 mil. É uma questão de rigor no texto.
- **Correção sugerida:** Acrescentar uma frase ao docstring: sobre Spearman, a estatística é aproximação heurística.

### Cálculo dos indicadores (IND)

#### IND-1 — razao_agregada em proporcoes_brasil.py ignora `complemento` e sai invertida para pct_sem_agua_canalizada

- **ERRO · confiança alta**
- **Agente principal:** CONFIRMADO: razao_agregada de pct_sem_agua_canalizada = 0,986 (ELSI urbano), contra média por setor de 0,015. Não chega ao deck, que usa só as 7 variáveis do IVS.
- **Onde:** scripts/proporcoes_brasil.py:117-136 (função `resumir`, linhas 125-126 e 135); saída observada em banco_de_dados/nacional/proporcoes_por_recorte.csv e comparativo_brasil_vs_elsi.csv
- **Evidência:** A função `resumir()` recalcula a razão agregada direto do numerador/denominador brutos (`num_setor = df[ind.numerador].sum(...)`; `den_setor = df[ind.denominador].sum(...)`; `agregado = (num/den*ind.escala) if den else np.nan`) e nunca lê `ind.complemento`, diferente de `calcular_indicadores()` em src/ivs_censo/indicadores.py:231-232 (`if ind.complemento: valores = 1 - valores`). `pct_sem_agua_canalizada` é o único indicador com `complemento=True` (indicadores.py:154-157). Efeito real, já materializado no CSV gerado: `banco_de_dados/nacional/proporcoes_por_recorte.csv`, linha "ELSI 70 municípios (apenas urbanos);pct_sem_agua_canalizada;Saneamento;False;104067;0.014965;0.068538;0.000000;0.000000;0.004808;0.986233" — `media_entre_setores`=0,014965 (correto, vem da coluna do módulo) mas `razao_agregada`=0,986233 na MESMA linha: 65× maior e o valor complementar errado (é a proporção COM água canalizada, não sem). Recalculei também a partir da base bruta (V00199_sum/V00001_sum nacional ≈ 0,9848; 1−isso ≈ 0,0152), confirmando a direção do erro. O mesmo aparece em comparativo_brasil_vs_elsi.csv: "pct_sem_agua_canalizada;0.021788;0.014965;0.000000;0.000000;0.980313;0.986233;1.006000".
- **Impacto:** Qualquer leitura da coluna `razao_agregada` (ou de `comp['razao_ELSI_sobre_BR']`) para pct_sem_agua_canalizada nas tabelas nacionais/regionais/por-UF/por-município geradas por este script está com o sinal invertido — reporta ~98,6% de domicílios sem água canalizada quando o valor real é ~1,5%. Se algum slide, guia ou texto citar 'razão agregada' desse indicador (só ele tem complemento=True), o número está errado por construção.
- **Correção sugerida:** Em scripts/proporcoes_brasil.py, dentro de `resumir()`, após `agregado = (num / den * ind.escala) if den else np.nan`, adicionar `if ind.complemento: agregado = 1 - agregado if not np.isnan(agregado) else agregado`, espelhando a mesma regra de indicadores.py. Reexecutar o script (não fiz isso aqui, por orçamento) e regenerar os CSVs afetados.

#### IND-2 — Teste de regressão para razao_agregada não cobre (nem testaria) o caso com complemento

- **LACUNA · confiança alta**
- **Onde:** tests/test_pipeline_fase3.py:359-402 (`test_razao_agregada_mede_numerador_e_denominador_nos_mesmos_setores`)
- **Evidência:** O teste existe especificamente para blindar `resumir()` (mesma lógica do IND-1) mas só itera `for nome in ['pct_apartamento', 'pct_sem_banheiro', 'pct_casa_vila_condominio', 'pct_agua_inad']:` — nenhum deles tem `complemento=True`. Além disso, a fórmula "esperado" dentro do próprio teste (`n[par].sum() / d[par].sum()`) também não aplica `ind.complemento`, então mesmo adicionando 'pct_sem_agua_canalizada' à lista sem corrigir a fórmula esperada, o teste continuaria não pegando o bug do IND-1.
- **Impacto:** O único indicador do módulo com lógica de complemento (`pct_sem_agua_canalizada`) é justamente o que fica fora da rede de segurança que testa a razão agregada — explica por que o bug do IND-1 não foi pego antes de gerar os CSVs de entrega.
- **Correção sugerida:** Adicionar 'pct_sem_agua_canalizada' à lista testada em tests/test_pipeline_fase3.py:391 (aprox.) E ajustar a fórmula 'esperado' do teste para aplicar `1 - (n/d)` quando `ind.complemento` for True — só depois disso o teste realmente cobre o caso.

#### IND-3 — Dicionario_Variaveis_Projeto.csv documenta só 70 das 104 colunas da entrega — faltam todos os 26 indicadores calculados, 8 colunas derivadas, e não há coluna de unidade

- **LACUNA · confiança alta**
- **Onde:** banco_de_dados/entrega_orientadora/Dicionario_Variaveis_Projeto.csv; gerado por scripts/gerar_tabela_variaveis.py:26-71 via `tabela_variaveis()` em src/ivs_censo/dicionario.py:83-115
- **Evidência:** PRAGMA table_info(setores_censitarios) no .db retorna 104 colunas. O CSV (`;`-separado, utf-8-sig) tem 72 linhas de dados (header incluso = 73 linhas), das quais 2 ('CD_setor', 'setor') são grafias alternativas da mesma chave já unificada em 'CD_SETOR' no .db — 70 nomes únicos batem com colunas do .db. As 34 colunas do .db sem entrada no CSV são exatamente: os 26 indicadores de TODOS_INDICADORES (pct_agua_inad, pct_esgoto_inad, pct_lixo_inad, razao_moradores, pct_analfab, renda_media, pct_raca_pretpardind, pct_dom_improv, pct_hab_precaria, pct_moradia_convencional, pct_moradia_nao_convencional, pct_apartamento, pct_casa, pct_casa_vila_condominio, pct_sem_agua_canalizada, pct_agua_nao_encanada, pct_agua_so_terreno, pct_sem_banheiro, pct_sem_banheiro_nem_sanitario, pct_resp_feminino, pct_crianca_0a4, pct_pop_0a14, pct_idoso_60mais, iep_setor, rdi_setor, prop_70mais_entre_60mais) mais 8 colunas derivadas (CD_MUN, CD_UF, Dados_sig, Moradia_Predominante, Moradia_Predominante_Agrupada, is_fcu, urbano, renda_media_sem_extremo). O .xlsx irmão (Dicionario_Variaveis_Projeto.xlsx) tem, por código, uma aba extra 'Fórmulas dos indicadores' (scripts/gerar_tabela_variaveis.py:43-56) que cobre os 26 indicadores — mas essa aba não vai para o .csv, e mesmo ela não cobre as 8 derivadas. Já scripts/gerar_entrega_orientadora.py:48-52 tem um dicionário Python com descrições prontas para 5 dessas 8 (Moradia_Predominante, Moradia_Predominante_Agrupada, is_fcu, urbano, renda_media_sem_extremo) que nunca é exportado para o Dicionario_Variaveis_Projeto. Por fim, o CSV não tem nenhuma coluna de 'unidade' (%, R$, contagem, razão×100) para nenhuma das 104 colunas.
- **Impacto:** Quem abre o dicionário de variáveis da entrega (o artefato pensado para explicar 'o que significa cada variável') não encontra ali nem a definição dos indicadores do IVS nem das colunas administrativas derivadas — tem que ir ao código-fonte. Descrições que já existem em dois lugares diferentes do repositório (formulas em gerar_tabela_variaveis.py, DESCRICOES em gerar_entrega_orientadora.py) nunca chegam ao arquivo final.
- **Correção sugerida:** Em gerar_tabela_variaveis.py, concatenar `formulas` (já calculado) e um dicionário de descrições das 8 colunas derivadas (reaproveitando o que já existe em gerar_entrega_orientadora.py:48-52) à tabela final antes de gravar o .csv/.xlsx, e acrescentar uma coluna 'unidade'.

#### IND-4 — V00051 (maloca indígena) fica fora de PRECARIA mas dentro de NAO_CONVENCIONAL sem comentário explicando a assimetria

- **LACUNA · confiança media**
- **Onde:** src/ivs_censo/indicadores.py:113-115
- **Evidência:** `PRECARIA = ['V00050', 'V00052', 'V00053', 'V00054', 'V00055', 'V00056', 'V00057', 'V00058']` (V00051 ausente) vs `NAO_CONVENCIONAL = ['V00050', 'V00051', 'V00052']` (V00051 presente). Todo o resto do arquivo comenta explicitamente escolhas equivalentes (ex.: exclusão de V00398→inclusão intencional citando IVS-BH 2012, nas linhas 80-82); esta em particular não tem comentário.
- **Impacto:** Sem a justificativa registrada, a próxima pessoa a mexer no arquivo não sabe se a ausência de V00051 em PRECARIA foi decisão (ex.: não rotular habitação indígena tradicional como 'precária') ou descuido — risco de 'correção' inadvertida que mudaria pct_hab_precaria.
- **Correção sugerida:** Adicionar comentário de uma linha ao lado de PRECARIA explicando por que V00051 fica de fora (ou incluir, se for descuido).

### Notebooks 01 e 02 (NBS)

#### NBS-1 — Comentário da seção 7f cita o universo errado de setores (106 mil em vez de 104 mil)

- **ERRO · confiança alta**
- **Onde:** notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb — célula markdown 27 (texto) e célula de código 28 (checagem)
- **Evidência:** A célula markdown 27 afirma: 'Isto foi verificado empiricamente na base ELSI: a soma V00047+…+V00052 nunca ultrapassa V00001 em nenhum dos 106 mil setores elegíveis'. Mas nesse ponto do notebook df_ok já foi filtrado para urbano na célula 8 (df_ok = df_ok[mask_urbano], 106.281 → 104.108 setores). Recalculei a checagem sobre os 104.108 setores urbanos (não 106.281): 0 setores com soma > V00001, déficit máximo de 6 domicílios — o resultado bate, mas o texto descreve o universo checado como '106 mil' quando na verdade são 104.108 (104 mil) setores urbanos elegíveis.
- **Impacto:** Não afeta o resultado numérico (a checagem em si está correta), mas o texto descreve incorretamente qual conjunto de dados foi auditado, o que pode confundir quem tenta reproduzir a verificação usando o universo 'OK' (106.281) em vez do universo urbano (104.108) — os dois têm tamanhos e composições diferentes.
- **Correção sugerida:** Trocar '106 mil setores elegíveis' por '104 mil setores urbanos elegíveis' na célula markdown 27, para consistência com o restante da seção (que já opera sobre df_ok pós-filtro urbano desde a célula 8).

#### NBS-3 — Método de agregação por município/região (média de proporções por setor) não é declarado nas seções 5-7, 7b-7d, 7f

- **LACUNA · confiança alta**
- **Onde:** notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb — função desc_grupo (célula 16) usada pelas células 16, 18, 20, 22, 24, 28 e pelo helper _desc_long (célula 26) reaproveitado nas células 26, 28, 32
- **Evidência:** desc_grupo(grupo, col) faz s = grupo[col].dropna(); 'media': s.mean() — ou seja, tira a média dos valores de proporção JÁ calculados por setor (média de proporções), não uma razão agregada (soma do numerador / soma do denominador do grupo). O CONFIRA pede que se declare qual dos dois métodos foi usado. Isso SÓ é feito explicitamente em duas seções: 7e (célula markdown 25, que distingue 'agregado — razão das somas' de 'por setor — razão dentro de cada setor, depois descritivas', exportando as duas versões) e 7h (célula de código 32, comentário 'razão agregada (domicílios), que é o número comparável' para a tabela por região). Nas seções 5, 6, 7, 7b, 7c, 7d e na tabela por município de 7f, a mesma ambiguidade existe mas não é mencionada no markdown.
- **Impacto:** Média de proporções por setor e razão agregada podem divergir sensivelmente quando os setores têm tamanhos populacionais/domiciliares muito desiguais (setores pequenos pesam igual a grandes na média de proporções). Um leitor da Tabela 1 do artigo (que usa desc_mun/desc_reg, células 16-18) não tem como saber, sem ler o código-fonte, qual dos dois números está vendo — e o próprio notebook mostra, nas seções 7e/7h, que a equipe está ciente da diferença e a documenta lá, mas não replicou a mesma transparência nas tabelas principais do IVS.
- **Correção sugerida:** Acrescentar uma frase no markdown das seções 5-7 (e 7b-7d, 7f) esclarecendo que 'média' nas tabelas por município/região é a média das proporções por setor (não razão agregada), seguindo o padrão já adotado nas seções 7e e 7h.

#### NBS-4 — Matriz de correlação usa exclusão par-a-par (pairwise), não declarado, com efeito mensurável de até 0,033 frente ao listwise

- **LACUNA · confiança alta**
- **Onde:** notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb — célula markdown 41 (seção 12) e célula de código 42 (corr_p = df_ok[CORRELACAO_VARS].corr(method='pearson'))
- **Evidência:** pandas .corr() por padrão calcula correlação par-a-par, excluindo NaN por par de colunas (não listwise/linha-completa). O markdown da seção 12 não menciona esse detalhe. Recalculei a mesma matriz em modo listwise (só linhas com as 10 variáveis completas: 86.232 de 104.108 = 82,8% das linhas) e comparei com o par-a-par: maior diferença absoluta = 0,033 (razao_moradores × pct_raca_pretpardind: 0,473 par-a-par vs 0,440 listwise).
- **Impacto:** 0,033 não é um erro grave, mas não é desprezível para uma matriz que 'subsidia a análise fatorial' (texto da própria célula 41) — variáveis com correlação próxima de limiares de decisão podem trocar de leitura dependendo do método. Sem a declaração, o leitor não sabe que ~17% das linhas têm ao menos uma das 10 variáveis faltante e que isso é tratado par a par, não descartado em bloco.
- **Correção sugerida:** Acrescentar uma frase na célula markdown 41 informando que a correlação é par-a-par (pandas default) e citando a cobertura de dados completos (82,8% das linhas) como referência do que seria o listwise.

#### NBS-5 — Tabela de FCU por município só existe para a base completa; por região existem as duas versões (base completa e recorte de análise)

- **LACUNA · confiança media**
- **Onde:** notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb — célula de código 30 (seção 7g)
- **Evidência:** fcu_reg é o concat de fcu_reg (base completa) + fcu_reg_ok (recorte de análise urbano), com coluna 'universo' distinguindo as duas. fcu_mun é calculado só com df.groupby(...).apply(_resumo_fcu) — sobre a base completa (109.032 setores) — e exportado assim em favelas_fcu_por_municipio.csv, sem uma versão equivalente para df_ok (104.108 urbanos). O próprio comentário da célula alerta 'ATENÇÃO AO UNIVERSO' sobre a diferença entre os dois totais (19.507 vs 19.452 setores de FCU), mas essa atenção não se reflete na granularidade município.
- **Impacto:** Quem usa favelas_fcu_por_municipio.csv para comparar com outras tabelas municipais do NB02 (que são todas sobre o recorte urbano, df_ok) está comparando universos diferentes sem que isso seja sinalizado na própria tabela — o CSV não tem coluna 'universo' como os de região.
- **Correção sugerida:** Gerar também fcu_mun_ok (groupby sobre df_ok) e concatenar com a coluna 'universo', como já é feito para fcu_reg, ou ao menos documentar no header do CSV/README que a tabela por município é sobre a base completa, não sobre o recorte urbano.

#### NBS-6 — Correlação de Spearman '0,459' citada na seção 7h não identifica a qual das 3 variáveis de 'entrega' de água se refere

- **LACUNA · confiança alta**
- *Duplicado de O1 da auditoria anterior; mantido pela evidência adicional.*
- **Onde:** notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb — célula markdown 31 (seção 7h)
- **Evidência:** Texto: 'os dois eixos não são intercambiáveis — o Spearman entre eles é 0,459'. A seção define 3 variáveis de entrega (pct_sem_agua_canalizada, pct_agua_so_terreno, pct_agua_nao_encanada). Recalculei o Spearman de pct_agua_inad contra as 3: pct_sem_agua_canalizada=0,480, pct_agua_so_terreno=0,453, pct_agua_nao_encanada=0,459. O número citado (0,459) bate exatamente com pct_agua_nao_encanada ('o pedido literal da orientadora'), não com pct_sem_agua_canalizada (a fórmula efetivamente adotada, que é o foco do restante do parágrafo).
- **Impacto:** O número está correto para uma leitura específica, mas o texto não deixa claro qual par foi usado — um leitor pode presumir que 0,459 descreve a correlação com a variável adotada (pct_sem_agua_canalizada, na verdade 0,480), gerando uma citação levemente equivocada se usada em outro documento.
- **Correção sugerida:** Especificar explicitamente na célula markdown 31 que o Spearman de 0,459 é entre pct_agua_inad e pct_agua_nao_encanada (não pct_sem_agua_canalizada).

#### NBS-2 — Dois CSVs por-setor em banco_de_dados/eda/ não são produzidos por nenhuma célula do NB01 ou NB02 atuais

- **HIGIENE · confiança alta**
- *Reclassificado de ORFAO: os dois arquivos não são versionados; são sobras locais, como HIG-21.*
- **Onde:** banco_de_dados/eda/estrutura_etaria_contagem_por_setor.csv (8.028.171 bytes) e banco_de_dados/eda/resp_feminino_contagem_por_setor.csv (7.568.784 bytes)
- **Evidência:** grep -rn "contagem_por_setor" em todo o repositório (.py, .ipynb, .md, exceto os próprios nomes de arquivo em banco_de_dados/eda/) não retorna nenhuma ocorrência. A célula 26 do NB02 (seção 7e, envelhecimento) exporta apenas 'estrutura_etaria_contagem_por_municipio.csv' (a partir de env_mun) e o próprio print da célula lista explicitamente os artefatos gerados, sem citar '_por_setor'; o mesmo vale para a célula 24 (resp_feminino). Os dois arquivos estão listados no .gitignore (padrão banco_de_dados/**/*_por_setor.csv, linha 19) e nunca foram versionados. As datas de modificação (18/06/2026 para ambos) são anteriores ao commit 15521e5 (20/08/2026, criação do módulo compartilhado src/ivs_censo) e ao commit 880e8d1 (21/08/2026, que reescreveu a seção 7e/matriz de correlação) — são resíduos de uma versão anterior da pipeline, pré-módulo compartilhado.
- **Impacto:** Arquivos de ~7-8 MB cada, ocupando espaço no diretório de saída, sem rastreabilidade até nenhuma célula de código versionada. Um leitor que abra esses CSVs pode presumir que refletem a lógica atual do NB02 (Dados_sig, filtro urbano, indicadores do módulo), quando na verdade vêm de uma execução anterior e potencialmente desatualizada da pipeline.
- **Correção sugerida:** Apagar os dois arquivos (já estão fora do controle de versão) ou, se o dado por-setor for necessário, adicionar a célula que os gera explicitamente ao NB02, documentando a decisão no markdown da seção correspondente.

#### NBS-8 — Tabela CD_SIT × SITUACAO (markdown NB01) não é exaustiva: 2 setores do Brasil ficam de fora, soma 468.097 em vez de 468.099

- **HIGIENE · confiança media**
- **Onde:** notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb — célula markdown 5
- **Evidência:** A tabela cobre CD_SIT ∈ {1,2,3,5,6,7,8,9} = 354.965 (Urbana) + 112.031 (Rural) + 1.101 (vazia) = 468.097, mas o texto diz 'verificada nos 468.099 setores do Brasil'. Recomputando o crosstab CD_SIT × SITUACAO no arquivo bruto do IBGE (dados/Agregados_por_setores_basico_BR_20250417.csv), encontrei 2 setores adicionais com CD_SIT='.' e SITUACAO vazia, não mencionados na tabela.
- **Impacto:** Irrelevante para o recorte ELSI (nenhum dos 2 setores está nos 70 municípios, confirmado) e para qualquer conclusão do projeto — é uma imprecisão de 2 em 468.099 (0,0004%) na descrição do universo nacional.
- **Correção sugerida:** Ajustar a frase para '468.097 dos 468.099 setores' ou acrescentar uma linha 'outros/. : 2' na tabela, por completude.

#### NBS-7 — Nenhuma célula das duas notebooks tem output persistido — todas as afirmações numéricas do markdown dependem de reexecução para verificação

- **OPINIAO · confiança alta**
- *Reclassificado de LACUNA: o README da pasta declara que os notebooks são versionados sem saídas; é decisão, não lacuna.*
- **Onde:** notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb e 02_Analises_Descritivas.ipynb (arquivo inteiro)
- **Evidência:** Script Python sobre o JSON dos dois .ipynb: todas as células de código têm execution_count=None e outputs=[] (soma de outputs = 0 nas 21+45 células). O artefato versionado não guarda nenhuma evidência computacional das contagens citadas no markdown (109.032, 106.281, 104.108, 19.507, etc.).
- **Impacto:** Sem outputs persistidos, qualquer divergência entre o texto e o dado real só é detectável reexecutando a notebook ou recomputando externamente (como fiz nesta revisão) — o que esta revisão não pôde fazer sistematicamente por orçamento. Todos os números que verifiquei bateram exatamente, o que é uma evidência de qualidade forte, mas não é garantida pelo próprio artefato.
- **Correção sugerida:** Ao consolidar uma versão para entrega/publicação, rodar as notebooks do início ao fim e commitar com outputs, ou gerar um relatório .html/.pdf com outputs junto ao commit, para que os números fiquem auditáveis sem reexecução.

### Deck e PDFs de apoio (DEC)

#### DEC-1 — Slides 68 e 91 citam 3.357 setores para um arquivo que tem 3.358

- **DIVERGENTE · confiança alta**
- *Reclassificado de ERRO: 3.357 é o número certo da 2ª rodada (atualizada/); o erro é o caminho citado, que aponta para o arquivo da raiz.*
- **Onde:** docs/Apresentacoes_IVS/Analise_Fatorial_NB04_2026-09.pptx, slides 68 e 91
- **Evidência:** Texto extraído via python-pptx do slide 68: "banco_de_dados/eda/renda_outliers_rastreados.csv — 3.357 setores, um por linha, com identificação completa." (o caminho citado é explicitamente o da raiz, sem 'atualizada/'). Slide 91 repete '3.357 setores' para o mesmo arquivo. Contagem real de linhas de dados (pandas, sep=';', .venv do projeto): banco_de_dados/eda/renda_outliers_rastreados.csv = 3358 linhas; banco_de_dados/eda/atualizada/renda_outliers_rastreados.csv = 3357 linhas. O número do slide bate com a versão 'atualizada' (pós-remoção do setor extremo de BH), não com o arquivo cujo caminho aparece escrito no slide.
- **Impacto:** Quem for até o caminho impresso no slide 68 para conferir a lista completa de outliers de renda encontra 3.358 linhas, uma a mais do que o slide promete — quebra a correspondência número↔fonte citada, no mesmo tema (renda/extremo de BH) que já tem outros números sob suspeita em slides diferentes (95–98), mas aqui é um arquivo e uma seção distintos (EDA Central, slides 68/91) dos já levantados.
- **Correção sugerida:** Ajustar o slide 68 (e 91) para 3.358 setores, se o caminho citado for o da raiz; ou trocar o caminho para banco_de_dados/eda/atualizada/renda_outliers_rastreados.csv, se a intenção for reportar a versão sem o extremo de BH (3.357).

#### DEC-2 — Guia de Apoio nunca define autovalor, base dos critérios de Kaiser e Horn

- **LACUNA · confiança alta**
- **Onde:** docs/Apresentacoes_IVS/complementos/Guia_Apoio_Analise_Fatorial.pdf (13 páginas)
- **Evidência:** Busca (regex, case-insensitive) no texto extraído via pdfplumber: 'autovalor' e 'eigenvalue' = 0 ocorrências nas 13 páginas do Guia. 'Kaiser' aparece 1 vez e 'Horn' 1 vez, só relatando o resultado: "Na solução sem o lixo, tanto o critério de Kaiser quanto a análise paralela de Horn retêm um só fator" — valor conferido contra banco_de_dados/eda/fatorial/resumo_adequabilidade.csv, linha ivs6_sem_lixo_spearman: autovalores_acima_1=1, autovalores_acima_horn=1 (bate). Mas em nenhum ponto do Guia se explica o que é um autovalor nem o limiar de cada critério.
- **Impacto:** O Guia relata o resultado dos dois critérios que sustentam a decisão "um fator ou dois" (parte da lâmina EXPLICAR 42, 'As seis decisões'), mas quem não já souber o que é autovalor não consegue entender por que Kaiser e Horn concordam nem o que cada um mede.
- **Correção sugerida:** Acrescentar ao Guia uma definição curta de autovalor e do critério de Kaiser (autovalor > 1) e da lógica da análise paralela de Horn antes de citar o resultado sem-lixo.

#### DEC-3 — Nem o Guia nem o Plano de Emergência definem matriz padrão × matriz de estrutura

- **LACUNA · confiança alta**
- **Onde:** Guia_Apoio_Analise_Fatorial.pdf e Plano_Emergencia_Apresentacao.pdf (complementos/)
- **Evidência:** Busca por 'matriz padrão', 'matriz estrutura', 'pattern matrix' e 'structure matrix' no texto extraído (pdfplumber) dos dois PDFs (13 + 10 páginas): 0 ocorrências de cada termo, nos dois documentos.
- **Impacto:** O deck usa rotação promax (oblíqua) nos slides 17 ('As cargas, nas duas rotações') e 36 ('A rotação promax, linha a linha'), ambos marcados EXPLICAR. É justamente na rotação oblíqua que a distinção padrão × estrutura passa a importar, porque as cargas deixam de ser simultaneamente correlação e coeficiente de regressão. Sem essa definição em nenhum dos dois materiais de apoio, a leitura das cargas promax fica incompleta para quem for explicar esses dois slides.
- **Correção sugerida:** Acrescentar, na seção do Guia sobre a rotação promax, a definição de matriz padrão vs. matriz de estrutura e deixar explícito qual das duas o deck está reportando nas tabelas de carga.

#### DEC-4 — Guia define KMO mas nunca menciona MSA (adequação por variável)

- **LACUNA · confiança alta**
- **Onde:** Guia_Apoio_Analise_Fatorial.pdf, seção correspondente ao slide 33 ('O KMO, linha a linha', EXPLICAR)
- **Evidência:** Busca por 'MSA' no Guia: 0 ocorrências nas 13 páginas. No Plano de Emergência aparece 2 vezes, com números concretos: "com Pearson o KMO cai para 0,732, o MSA mínimo para 0,542" — valores conferidos contra banco_de_dados/eda/fatorial/resumo_adequabilidade.csv, linha ivs7_pearson: kmo=0.7318 (~0,732 ✓), msa_min=0.5422 (~0,542 ✓). O MSA por variável está calculado em banco_de_dados/eda/fatorial/nb04_adequabilidade.csv (coluna MSA; cenário ivs7_spearman: lixo=0,6995, que é o mínimo do cenário, batendo com msa_min=0,6995 em resumo_adequabilidade.csv).
- **Impacto:** O slide 33 promete explicar o KMO 'linha a linha', mas o Guia — o material dedicado a essa explicação — nunca trata do MSA individual, que é a peça que mostra por que uma variável específica (o lixo) pesa contra a adequação da base. Essa peça só aparece no Plano de Emergência, um documento diferente e com outro propósito (perguntas de plateia).
- **Correção sugerida:** Incluir no Guia a definição de MSA e, se possível, a tabela de valores por variável de nb04_adequabilidade.csv, já que o Plano de Emergência mostra que esse número é efetivamente usado para responder perguntas sobre o KMO.

### Documentação (DOC)

#### DOC-1 — Citação à Enap (p. 58) usada para autorizar manter razao_moradores (h²=0,380) generaliza além do exemplo do próprio livro

- **DIVERGENTE · confiança media**
- **Onde:** docs/metodologia/Analise_Fatorial_Enap2019_Guia_de_Leitura.md:246 e :297
- **Evidência:** O documento diz: 'A p. 58 autoriza manter variável abaixo de 0,50 quando a carga é alta (0,532)' (linha 246) e '5 | A razao_moradores fica com comunalidade 0,380? | p. 58 | Sim, citando a passagem que relativiza o corte' (linha 297). O texto extraído da p. 58 do PDF (Livro Análise Fatorial-2.pdf) diz: 'o critério da comunalidade maior do que 0,5 não deve ser utilizado isoladamente e de maneira muito rígida (...) temos variáveis no modelo com um valor um pouco abaixo desse critério, mas que apresentam cargas fatoriais altas (exemplo: item 8)'. O item 8 citado pelo próprio livro (Standardized loadings, p. 59) tem h²=0,46 — 8% abaixo do corte de 0,5. A razao_moradores do projeto tem h²=0,380 — 24% abaixo do corte, quase o triplo do desvio do exemplo do livro.
- **Impacto:** A citação está na direção certa (o livro de fato relativiza o corte de 0,5), mas o verbo 'autoriza' e o 'Sim' categórico no quadro de decisão emprestam à p. 58 um peso maior do que ela dá: a página ilustra um afrouxamento marginal do critério (item com h² pouco abaixo de 0,5), não uma licença geral para manter uma variável com h²=0,380. Se isso for usado como justificativa metodológica formal (ex.: na dissertação ou artigo), um revisor que confira a página vai achar a evidência mais fraca do que a redação sugere.
- **Correção sugerida:** Reescrever a citação declarando a diferença de grau: citar a p. 58 como precedente de que o corte de 0,5 não deve ser rígido, mas registrar explicitamente que o exemplo do livro (h²=0,46) é bem menos extremo que o caso do projeto (h²=0,380), e apoiar a decisão final também na carga alta (0,532) e/ou em outro critério, não só na página do livro.

### Commits posteriores à auditoria (AUD)

#### AUD-07 — Os slides do extremo de BH afirmam números errados: segundo maior 'na casa dos R$ 30 mil', '87 mil setores' e 'um quinto do município'

- **ERRO · confiança alta · introduzido depois da auditoria**
- **Verificador:** CONFIRMADO (ERRO). Os três números estão errados, e dois deles estão no deck em circulação. No corpo do S97, 'segundo maior na casa dos R$ 30 mil': o segundo maior de BH é R$ 45.385,44. Nas notas do S96, '87 mil setores': o agregado em que a média cai 0,04% tem 104.096 setores com renda. Nas notas do S97, 'um quinto do município': 1.909/5.112 = 37,3%. Um dado provavelmente explica o erro do segundo maior: a figura extremo_bh.png corta o histograma em v<40.000, e com isso esconde também o setor de R$ 45.385. O painel parece terminar em R$ 30 mil, e a anotação diz que só o extremo está fora do quadro. Autoria recente: 694c306 e 9452c32.
- **Onde:** scripts/gerar_slides_extremo_bh.js:79 (corpo do slide 97 do deck), :70 (notas do slide 96), :95 (notas do slide 97)
- **Evidência:** Slide 97: 'Se o máximo de Belo Horizonte é R$ 170 mil e o segundo maior está na casa dos R$ 30 mil'. No .db, recorte urbano OK, BH: top-5 da renda = [170418.06, 45385.44, 29327.0, 28000.11, 26856.85]. O segundo maior é R$ 45.385, o que também aparece em extremo_bh_descritivas.csv (max sem extremo = 45385.44). Notas do 96: 'Em 87 mil setores ele move a média em 0,04%'; mas extremo_bh_descritivas.csv dá n=104.096 no agregado dos 70 municípios (87 mil é o recorte da fatorial). Notas do 97: 'achatar a escala de um quinto do município'; o certo é 1.909/5.112 = 37,3%.
- **Impacto:** O corpo do slide 97 está no deck em circulação e subestima em 1/3 o segundo maior valor. As notas servem de roteiro de fala e trazem o universo errado e uma fração que é quase o dobro da dita.
- **Correção sugerida:** Ler o segundo maior e o n do agregado de extremo_bh_descritivas.csv, calcular a fração a partir de extremo_bh_normalizacao.csv e corrigir os três trechos no deck anexado.

#### AUD-08 — O guia de apoio diz que retirar o analfabetismo 'recupera os 16.563 setores'; o NB04 mede 16.548

- **ERRO · confiança alta · introduzido depois da auditoria**
- **Verificador:** PARCIAL (ERRO). O número está errado, mas o erro não é do guia e é mais antigo do que a auditoria. Os 16.563 são a perda total por listwise nas 7 variáveis. Os setores sem analfabetismo são 16.552, e retirar a variável recupera 16.548. A mesma confusão aparece em Relatorio_Analise_Fatorial_NB04.md:191 ('Manter a variável: 16.563 setores ficam sem índice. Retirá-la: recupera-os'), no gerador do deck gerar_deck_fatorial.js:678, que vai para o S42 do deck em circulação ('Manter a variável custa 16.563 setores sem índice'), e em gerar_pdf_plano_emergencia.py:542 ('a diferença são 16.563 setores em que o IBGE sigila o analfabetismo'). O guia só copiou. O próprio Relatorio_NB04 se contradiz: 16.548 na linha 170 e 16.563 na 191. Autoria: o erro nasceu em d190832, antes da auditoria; o guia e o plano o repetem em 27e05a7. A parte do IC também confirma: é um intervalo percentil de 2,5 a 97,5, não 'entre 64,7% e 65,3% nas mil repetições'.
- **Onde:** scripts/gerar_pdf_guia_fatorial.py:531-534 · complementos/Guia_Apoio_Analise_Fatorial.pdf
- **Evidência:** Texto do PDF: 'Exigir a variável custa 16.563 setores' e 'A favor de retirá-la: recupera os 16.563 setores.' O resumo_adequabilidade.csv dá n=104093 para ivs6_sem_analfab_spearman: 104.093 − 87.545 = 16.548. O Relatorio_Analise_Fatorial_NB04.md:170 e o GUIA:559 dizem 16.548. Menor: o guia (393) e o plano (561-562) leem o IC95 do bootstrap ('IC95 [64.7; 65.3]', NB04 ipynb:1264) como se fosse o intervalo das mil repetições ('ficou entre 64,7% e 65,3% nas mil repetições').
- **Impacto:** A diferença é pequena, mas o PDF diverge do relatório e do Guia num documento feito para responder perguntas da orientação. E a leitura do IC exagera a estabilidade (5% das reamostragens ficam fora).
- **Correção sugerida:** Ler o n de resumo_adequabilidade.csv e escrever 'intervalo de confiança de 95%' em vez de 'nas mil repetições'.

#### AUD-03 — O README de Apresentacoes_IVS se contradiz depois de 356c32b e 9452c32

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- **Verificador:** CONFIRMADO (DIVERGENTE). O README se contradiz. O topo, reescrito em 356c32b e 9452c32, diz que a apresentação atual é a da fatorial, com 98 slides. A seção '## A apresentação atual' (730b91b8/dc6daed3) continua apontando EDA_Central_IVS_2026-09_rev2.pptx, com 51 slides, e diz que ela é 'gerada por script, não editada à mão'. Um detalhe na descrição: a linha 79 fala do deck da EDA, então ela só contradiz as linhas 28-31 porque a seção se apresenta como 'a apresentação atual'. Há ainda uma contradição que o revisor não pegou: a linha 107 diz que o roteiro 'é o único artefato desta pasta escrito à mão', e o deck principal é editado à mão. Autoria recente: a contradição surgiu com 356c32b, que mudou o topo sem mexer na seção.
- **Onde:** docs/Apresentacoes_IVS/README.md:3-31 × :40-52, :79-80, :93-98; docs/MANUAL_DO_PROJETO.md:517
- **Evidência:** As linhas 8 e 14-17 (356c32b/9452c32) dizem que a apresentação atual é a da fatorial, com 98 slides. A seção '## A apresentação atual' (linhas 44-52, git blame 730b91b8/dc6daed3) continua dizendo 'Arquivo: EDA_Central_IVS_2026-09_rev2.pptx — 51 slides' e 'Ela é gerada por script, não editada à mão'. A linha 79 diz 'Se editar o .pptx à mão, a próxima execução do script sobrescreve a edição', contra as linhas 28-31. A tabela de complementos/ (93-98) cobre 7 dos 10 arquivos: faltam EDA_Central_IVS_2026-09_rev2.pptx, Guia_Apoio_Analise_Fatorial.pdf e Plano_Emergencia_Apresentacao.pdf. O parágrafo 24-26 aparece de novo em 28-29. O MANUAL:517 ainda diz 'a apresentação corrente é EDA_Central_IVS_2026-09_rev2.pptx'. Pré-existente: a linha 56 manda regerar dentro de historico/, contra a regra da linha 212.
- **Impacto:** A seção que responde 'qual é a apresentação atual' aponta o deck avulso e afirma que ele não é editado à mão, justo no arquivo criado para evitar abrir o deck errado.
- **Correção sugerida:** Reescrever a seção 'A apresentação atual' para o deck da fatorial, dizer que ele é editado à mão, completar a tabela de complementos/, apagar o parágrafo duplicado e corrigir o MANUAL:517.

#### AUD-04 — 4fb9afe reescreveu caminhos nos geradores, mas o deck e o PDF em circulação ainda citam caminhos que não existem

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- **Verificador:** CONFIRMADO (DIVERGENTE). Existe como descrito. 4fb9afe moveu os .md para docs/relatorios/ e docs/metodologia/ e corrigiu as strings nos geradores. Os artefatos versionados não foram regerados e continuam citando caminhos que não existem mais. Nos dois artefatos gerados (EDA avulsa e guia em PDF), a única diferença entre o regerado e o versionado é o caminho. Autoria recente: 4fb9afe.
- **Onde:** Analise_Fatorial_NB04_2026-09.pptx slides 39 e 88 · complementos/EDA_Central_IVS_2026-09_rev2.pptx slide 45 · complementos/Guia_Apoio_Analise_Fatorial.pdf
- **Evidência:** Texto extraído do deck atual: slide 39 'docs / Codigo_Analise_Fatorial_Comentado.md'; slide 88 'Redação completa em docs/Relatorio_EDA_Fase3_IVS_ELSI.md'. No PDF do guia: 'docs/Relatorio_Analise_Fatorial_NB04.md' e 'docs/Codigo_Analise_Fatorial_Comentado.md'. `test -e` → os três caminhos NÃO existem. Regenerados em scratch, o deck da EDA difere do versionado só nessa string do slide 45, e o guia só nessas duas linhas (diff do texto por pypdf: 4 linhas). Em ambos os casos o gerador foi corrigido e o artefato não foi regerado.
- **Impacto:** O material entregue manda o leitor a arquivos que não existem mais. E o gerador deixou de reproduzir o artefato versionado, o que desmente o 'reproduzem idênticos' da auditoria.
- **Correção sugerida:** Regerar o guia em PDF. No deck editado à mão, corrigir as duas strings (slides 39 e 88) diretamente no OOXML ou no PowerPoint; regerar o EDA_Central avulso.

#### AUD-09 — 0bef9ed sincronizou só o GUIA §5/§8: o GUIA diz que a fatorial está concluída e o README, o MANUAL e a própria lista de prioridades do GUIA dizem que está pendente

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- **Verificador:** CONFIRMADO (DIVERGENTE). Existe como descrito. 0bef9ed sincronizou o GUIA §5, §6.3 e §8. No README.md mexeu em 2 linhas, e o status da fatorial ficou 'Pendente'. O checklist de prioridades do GUIA, os blocos de ordem de execução, a tabela de notebooks do MANUAL, o README da Fase 3 e o estrutura_projeto.md continuam sem o NB04. Resta parte do D1, e agora GUIA e README se contradizem. Autoria recente: 0bef9ed criou a contradição.
- **Onde:** GUIA_DO_PROJETO.md:684 × README.md:29; GUIA:749, :829, :837; README.md:240-247; docs/MANUAL_DO_PROJETO.md:76-80; notebooks/Fase3_EDA_ELSI/README.md:9-16; estrutura_projeto.md:136, :216
- **Evidência:** GUIA:684 '✅ Concluída em 17/09/2026 ... Pesos 65/35; AUC 0,813'. Contra isso: README.md:29 'Análise fatorial / ACP — definição dos pesos | 🔴 Pendente (Notebook 04)'; GUIA:749 '- [ ] Implementar a análise fatorial / ACP'; GUIA:837 e README.md:240 'notebooks/Fase3_EDA_ELSI/  →  01 → 02'; GUIA:829 e README:247 `jupyter execute` só com 01 e 02; a tabela de notebooks do MANUAL (76-80) e a do README da Fase 3 não têm o 04, que também diz 'Executar na ordem 01 → 02'; estrutura_projeto.md:216 '5 | Análise fatorial + ... | 🔴 Pendente'. Antes de 0bef9ed todos diziam 'pendente'; agora GUIA e README se contradizem.
- **Impacto:** Resta metade do D1, e com um agravante: quem abre o README, porta de entrada do repositório, lê que a etapa não foi feita, enquanto a fonte da verdade diz que foi.
- **Correção sugerida:** Aplicar a mesma sincronização ao README (status e ordem de execução), à tabela de notebooks do MANUAL, ao README da Fase 3, ao estrutura_projeto.md e ao checklist de prioridades do GUIA.

#### AUD-11 — Afirmações das seções finais da auditoria que são falsas ou deixaram de ser

- **DIVERGENTE · confiança alta**
- **Verificador:** PARCIAL (DIVERGENTE). Os itens 2 a 5 se confirmam. O item 1 não é falso: '59 testes' é o número de funções de teste (9+21+29) e 74 é o número de casos coletados, com a parametrização. É inconsistência de unidade dentro da auditoria, não contagem errada. No item 2, o NB02 gera 42 CSVs e 4 PNGs; os outros 19 CSVs da raiz vêm de gerar_tabelas_auditoria (9), de auditoria_renda (8) e há 2 *_por_setor. No item 3, o NB04 grava 18 nb04_*.csv, e d3ee10b repete '16 CSVs'. No item 4, o deck da fatorial e o da EDA avulsa deixaram de reproduzir; o do critério segue idêntico. No item 5, a negação `!banco_de_dados/entrega_orientadora/*.csv` vence a regra e vem com o comentário '# Exceção: entregáveis específicos para a orientadora', então é deliberada. A premissa de F7 e da 3ª opinião está errada, e 4c476de a repete. Autoria: o texto é da auditoria (ad474aa); os itens 3 e 5 foram repetidos em commits recentes.
- **Onde:** docs/relatorios/Auditoria_Integral_2026-09.md:70, :94-99, :121, :161-163
- **Evidência:** (1) Linha 121, 'os 59 testes têm verificação real': pytest coleta 74, e a linha 93 da própria auditoria diz 74. (2) Linha 94, 'NB02 (61 CSVs + 7 PNGs)': o parse do ipynb dá 42 chamadas to_csv e 4 savefig; os 61 da raiz são 42 do NB02, 9 de gerar_tabelas_auditoria, 8 de auditoria_renda e 2 *_por_setor locais, e as 3 figuras renda_* vêm de outros scripts. (3) 'NB04 (16 CSVs + 5 PNGs)': são 18 nb04_*.csv (16 to_csv, sendo que nb04_contingencia_{nome} gera 3); d3ee10b repete '16 CSVs'. (4) Linhas 98-99, 'Os três decks reproduzem idênticos': hoje o da fatorial tem 98 slides contra os 44 do gerador (AUD-02) e o da EDA difere do gerador no slide 45 (AUD-04); só o do critério continua idêntico (16/16). (5) F7 (linha 70) e o 3º item da Opinião (161-163), 'regra e prática apontam para lados opostos': o .gitignore tem `!banco_de_dados/entrega_orientadora/*.csv` (hoje linha 45, em ad474aa linha 40), e `git check-ignore -v` mostra essa negação vencendo. A exceção é deliberada, não um conflito, mas o commit 4c476de repete a afirmação.
- **Impacto:** A seção 'para a próxima auditoria não refazer' manda não refazer verificações que deixaram de valer, e dois achados/opiniões partem de uma premissa falsa sobre o .gitignore.
- **Correção sugerida:** Anotar na auditoria uma errata com a data: 74 testes, as saídas reais de NB02 e NB04, a perda de reprodutibilidade dos decks e a retirada de F7 e da 3ª opinião.

#### AUD-12 — Documentos dizem que o NB01 (e, no MANUAL, o NB02) não importam o módulo; os dois importam desde 21/08, e a auditoria não viu

- **DIVERGENTE · confiança alta**
- **Verificador:** CONFIRMADO (DIVERGENTE). Existe. O NB01 e o NB02 importam de ivs_censo desde 880e8d1 (21/08), antes da auditoria. Mesmo assim, MANUAL:505-511, GUIA:546-550 e README.md:96 descrevem a duplicação como pendente. A parte extra também confere: o README da Fase 3 (linha 19) diz que os notebooks são versionados sem outputs, e o MANUAL:679 repete. O NB04 tem 20 células com saída e 25 saídas guardadas, tanto em ad474aa quanto em d3ee10b. Não é recente.
- **Onde:** docs/MANUAL_DO_PROJETO.md:505-511 · GUIA_DO_PROJETO.md:546-550 · README.md:96 · notebooks/Fase3_EDA_ELSI/README.md:19
- **Evidência:** O MANUAL:505 diz 'O Notebook 02 não importa src/ivs_censo'; o NB02 tem `from ivs_censo import (INDICADORES_IVS, ...` (ipynb:125). O GUIA:546 diz 'O Notebook 01 ainda não usa o módulo' e o README:96 'pendente no NB01'; o NB01 tem `from ivs_censo import ARQUIVOS_CENSO` (ipynb:104), e a linha 373 diz 'DERIVADO de src/ivs_censo/fontes.py'. `git log -S` situa as duas importações em 880e8d1 (21/08), anterior à auditoria. Extra: o README da Fase 3 diz que os notebooks são 'versionados sem outputs', mas o NB04 tem 25 saídas guardadas, tanto em ad474aa quanto em d3ee10b.
- **Impacto:** O MANUAL manda mudar as fórmulas 'nos dois lugares', em código que já não está duplicado. Dívida registrada que já foi paga.
- **Correção sugerida:** Atualizar as três passagens e o README da Fase 3.

#### AUD-13 — Contagens de testes defasadas fora do MANUAL

- **DIVERGENTE · confiança alta**
- **Verificador:** CONFIRMADO (DIVERGENTE). As três passagens existem como descritas. Uma ressalva: o '65 testes' do Relatorio_EDA:992 estava certo quando foi escrito, em 22bf011 (02/09). Na época eram 44+21 = 65, e o test_fatorial.py só entrou em ac0d531, em 17/09. É um número de relatório datado que caducou, não um erro original. Já o Relatorio_NB04:266 ('8 testes') contradiz o Codigo_Analise_Fatorial_Comentado.md:443 ('9 testes') no mesmo momento. O GUIA:229 omite test_fatorial.py. 0bef9ed diz ter corrigido '65 testes → 74' e deixou o Relatorio_EDA de fora. Não é recente.
- **Onde:** docs/relatorios/Relatorio_EDA_Fase3_IVS_ELSI.md:992 · docs/relatorios/Relatorio_Analise_Fatorial_NB04.md:266 · GUIA_DO_PROJETO.md:229
- **Evidência:** Relatorio_EDA:992 'Suíte de testes automatizados | 65 testes' (são 74). Relatorio_NB04:266 'tests/test_fatorial.py 8 testes', contra `grep -c '^def test_' tests/test_fatorial.py` → 9, e o Codigo_Analise_Fatorial_Comentado.md:443 diz 9. O GUIA:229 dá como 'Cobertura de testes' só test_pipeline_fase3.py e test_ivs_censo.py, sem test_fatorial.py. 0bef9ed diz ter corrigido '65 → 74 em cinco arquivos' e não pegou o Relatorio_EDA.
- **Impacto:** Resíduo do D2: dois relatórios e o GUIA contradizem a contagem real.
- **Correção sugerida:** Corrigir as três passagens.

#### AUD-05 — O README de atualizada/ atribui a eda_atualizada.py as 8 tabelas renda_* e 2 figuras que auditoria_renda.py --sem-extremo gera; e as contagens caducaram

- **ORFAO · confiança alta · introduzido depois da auditoria**
- **Verificador:** PARCIAL (DIVERGENTE). A atribuição errada existe: as 8 renda_* e as 2 figuras renda_* de atualizada/ saem de `auditoria_renda.py --sem-extremo`, não de eda_atualizada.py. O erro está em três documentos: atualizada/README.md:3, eda/README.md:88-89 e também scripts/README.md:20, que o revisor não citou. A parte das contagens está exagerada. O '16 CSVs e cinco figuras' do atualizada/README ainda vale para o conjunto da 2ª rodada (7+1+8 CSVs, 3+2 PNGs), porque os extremo_bh_* estão documentados à parte na seção das linhas 42 em diante. Só o MANUAL:128, que descreve a pasta inteira, está desatualizado (19 CSVs e 6 PNGs). Não é ORFAO: todos os arquivos saem de código versionado, e o docstring de eda_atualizada.py:10-13 diz corretamente que as tabelas de renda vêm de auditoria_renda.py. Além disso, o Apresentacoes_IVS/README.md:61-66 traz a sequência certa. É divergência entre documentos. Autoria recente: ec8f220/de3ce28/0bef9ed.
- **Onde:** banco_de_dados/eda/atualizada/README.md:3-5, :30 · banco_de_dados/eda/README.md:88-89 · docs/MANUAL_DO_PROJETO.md:128
- **Evidência:** O README diz 'Gerados por: scripts/eda_atualizada.py' para 'Dezesseis CSVs e cinco figuras', incluindo 'renda_*.csv (8 arquivos)'. Mas eda_atualizada.py:159-167 (TABELAS) grava só 7 tabelas, mais comparacao_antes_depois (linha 318) e 3 figuras. As 8 renda_* e as figuras renda_boxplot_por_cidade.png e renda_tamanho_do_setor.png saem de auditoria_renda.py:278-283 e 307 (destino = eda/atualizada quando --sem-extremo) e das linhas 311-314. O eda/README.md:88 repete 'as 16 tabelas da 2ª rodada (scripts/eda_atualizada.py)'. Contagem em disco depois de 694c306: atualizada/ tem 19 CSVs e 6 PNGs, e o MANUAL:128 ainda diz '16 CSVs + 5 PNGs'.
- **Impacto:** O README criado para resolver L1/O2 dá o comando errado para regerar metade da pasta: rodar só eda_atualizada.py não reconstrói as renda_*.
- **Correção sugerida:** Separar no README as duas origens, cada uma com seu comando (auditoria_renda.py --sem-extremo; eda_atualizada.py), e atualizar as contagens no MANUAL e no eda/README.

#### AUD-06 — Os três geradores novos digitam medições no texto, embora os commits digam que não

- **ORFAO · confiança alta · introduzido depois da auditoria**
- **Verificador:** CONFIRMADO (ORFAO). Existe. Os três geradores novos digitam medições no texto, enquanto as mensagens de commit (27e05a7:20-22, 9452c32:11) e os docstrings (gerar_pdf_guia_fatorial.py:14 e gerar_slides_extremo_bh.js:9) dizem que nenhum número é digitado. Não reproduzi a contagem exata do revisor (39/36). Com o meu regex, que conta linhas fora de comentário com decimal BR ou milhar, deu 32 no guia e 30 no plano. Os exemplos citados conferem todos. O 0,59 e o 64,7/65,3 aparecem só na saída impressa do NB04 (ipynb:1264-1266) e em nenhum CSV. É o O3 da auditoria se repetindo em material novo. Autoria recente: 27e05a7 e 9452c32.
- **Onde:** scripts/gerar_pdf_guia_fatorial.py · scripts/gerar_pdf_plano_emergencia.py · scripts/gerar_slides_extremo_bh.js:67-69, :70, :95
- **Evidência:** 27e05a7 diz 'Nenhum valor é digitado'; 9452c32 diz 'Nenhum número é digitado no gerador'. grep de literais em formato BR fora de comentário: guia 39, plano 36. Exemplos de medição digitada: guia:393-394 '64,7% e 65,3%' e '0,59 ponto percentual'; guia:403/415 '0,924, 0,945 e 0,950'; guia:531/534 '16.563'; plano:384-402 '0,253', '0,822', '0,859'; plano:317/501 '3,42', '3,74', '49,5'; plano:528-530 '−0,81' e '0,784'; plano:567 '0,783 para 0,720' e '65/35 para 56/44'. Em gerar_slides_extremo_bh.js, no corpo do slide: `inteiro(170418)`, `inteiro(3058)` e `'56×'` (linhas 67-69); nas notas, '87 mil', '0,04%', '14%', '73%', '1.909' e '7º'. Os valores 0,59 e 64,7/65,3 só existem na saída impressa do NB04 (ipynb:1264-1266), em nenhum CSV.
- **Impacto:** É o O3 se repetindo em material novo, agora com uma declaração explícita do contrário na mensagem de commit. Dois desses números digitados estão errados (ver AUD-07 e AUD-08).
- **Correção sugerida:** Ler esses valores dos CSVs (nb04_*, extremo_bh_*, descritivas_globais, resumo_adequabilidade) ou gravar em CSV o que hoje só é impresso pelo NB04, como o IC dos pesos.

#### AUD-14 — O relatório da EDA cita um 'script de auditoria' com 286 valores conferidos que não está versionado

- **ORFAO · confiança media**
- **Verificador:** CONFIRMADO (ORFAO). Não existe no repositório, nem em nenhum ramo do histórico, um script que confira 286 valores contra os CSVs. A linha também não está marcada como não reproduzível, o que o docs/relatorios/README.md:3-4 exige ('quando não sair, é achado e está marcado como tal'). O script pode existir fora do repositório; não verifiquei isso. Não é recente.
- **Onde:** docs/relatorios/Relatorio_EDA_Fase3_IVS_ELSI.md:993
- **Evidência:** 'Números dos relatórios e da apresentação | Script de auditoria contra os CSVs de origem | 286 valores conferidos, 0 divergências'. `grep -rlE 'valores conferidos|286' scripts src tests` → nada. A linha entrou em 15521e5, que só versiona gerar_entrega_orientadora.py, gerar_tabela_variaveis.py e proporcoes_brasil.py. O docs/relatorios/README.md diz que número sem código 'é achado e está marcado como tal'; este não está marcado.
- **Impacto:** A única verificação documento × CSV que o projeto alega (o que o L2 pede) não é reproduzível.
- **Correção sugerida:** Versionar o script, se ele existir, ou marcar a linha como não reproduzível.

#### AUD-01 — 4c476de corrompeu a linha 2 do .gitignore e apagou a regra banco_de_dados/*.csv

- **FRAGIL · confiança alta · introduzido depois da auditoria**
- **Agente principal:** CONFIRMADO (git show 4c476de).
- **Verificador:** CONFIRMADO (FRAGIL). Existe como descrito. Em 4c476de o texto novo sobre a Fase 2 foi colado no meio da linha 2 (`banco_de_` + `# Legado...`). A regra `banco_de_dados/*.csv` sumiu e sobrou um padrão literal que não casa com nada. Hoje nada acontece, porque o único CSV na raiz de banco_de_dados/ é pego pela regra 17 (`banco_de_dados/**/Base_*.csv`). O `dados/*.csv` agora aparece duas vezes. Autoria recente: 4c476de.
- **Onde:** .gitignore:2
- **Evidência:** Em ad474aa a linha 2 era `banco_de_dados/*.csv` (git show ad474aa:.gitignore). Hoje a linha 2 é `banco_de_# Legado da Fase 2, arquivado em 17/09/2026: 302 MB de bases cuja metodologia foi` (sed -n 2p .gitignore; od -c confirma). Como o # não abre a linha, ela vira um padrão literal que não casa com nada. Teste: `git check-ignore -v --no-index banco_de_dados/teste_novo.csv` → NAO ignorado. O diff de 4c476de reescreve as 137 linhas porque também converteu CRLF em LF, e `dados/*.csv` agora aparece duas vezes (grep -c → 2).
- **Impacto:** Hoje não há efeito: a única coisa na raiz de banco_de_dados/ é Base_ELSI_Bruta, que a regra 17 (banco_de_dados/**/Base_*.csv) cobre. Mas qualquer CSV novo gravado na raiz de banco_de_dados/ que não comece por Base_ passa a entrar no git sem aviso. É exatamente o caso das bases grandes que esse mesmo commit acabou de tirar do índice.
- **Correção sugerida:** Restaurar `banco_de_dados/*.csv` numa linha própria, com o comentário da Fase 2 numa linha separada; remover o `dados/*.csv` duplicado.

#### AUD-02 — O deck em circulação, com 98 slides, não se reproduz mais pelo gerador, e o uso documentado do gerador o sobrescreve

- **FRAGIL · confiança alta · introduzido depois da auditoria**
- **Verificador:** PARCIAL (FRAGIL). O centro do achado vale: o gerador produz 44 slides e o deck versionado tem 98. E o docstring de gerar_deck_fatorial.js:5 ainda manda gravar a saída por cima do deck em circulação. Mas não é verdade que as marcações e a remoção de slide ficaram 'sem registro'. A mensagem de d2473d6 diz: 'o deck estava EDITADO À MÃO: um slide removido e 21 marcações ... Rodar gerar_deck_fatorial.js apagaria tudo isso'. O mesmo aparece em gerar_slides_extremo_bh.js:4-7 e no README de Apresentacoes_IVS:28-31. Ou seja, a remoção do slide 44 foi citada. As edições que nenhum registro cita são as de título e subtítulo, e são mais do que o revisor listou. Além dos slides 10, 13, 26 e 42, o slide 9 perdeu a linha de fonte, o 14 perdeu o 'Achado.' inicial, o 15 perdeu a linha de fonte e o 40 perdeu um parágrafo inteiro. A parte da correção 'tratar como editado à mão' já está declarada no projeto. O que falta é o docstring e a lista das edições. Autoria recente: d2473d6.
- **Onde:** docs/Apresentacoes_IVS/Analise_Fatorial_NB04_2026-09.pptx · scripts/gerar_deck_fatorial.js:5
- **Evidência:** `node scripts/gerar_deck_fatorial.js <scratch>` gera 44 slides e 0 marcações; o arquivo versionado tem 98 slides, 98 notas e 21 marcações EXPLICAR. A versão d2473d6~1 tinha 44 slides e 0 marcações: as 21 marcações e a junção com a EDA entraram juntas em d2473d6, sem registro separado. A comparação slide a slide (deck_cmp.py) acha edições à mão que os commits não citam: o slide 10 perdeu título e subtítulo; os slides 13 e 26 perderam o subtítulo; o slide 42 ganhou 'O PORQUE DE CADA DECISAO'; o slide 44 do gerador ('O que vem depois') sumiu. O docstring do gerador (linha 5) manda `node scripts/gerar_deck_fatorial.js docs/Apresentacoes_IVS/Analise_Fatorial_NB04_2026-09.pptx`.
- **Impacto:** Quem seguir o docstring apaga os blocos da EDA e do extremo de BH e as marcações do autor. E a afirmação da auditoria 'Os três decks reproduzem idênticos' deixou de valer para o deck principal: é agora o mesmo caso do F8, só que no artefato mais importante.
- **Correção sugerida:** Trocar o caminho de saída no docstring por outro que não seja o deck em circulação, registrar no README a lista das edições manuais e tratar o .pptx atual como artefato editado à mão, como o roteiro.

#### AUD-15 — O padrão frágil do F2 (astype(str)=='1') foi copiado para o script novo do extremo de BH

- **FRAGIL · confiança alta · introduzido depois da auditoria**
- *Duplicado de NB4-17; mantido pela evidência adicional.*
- **Verificador:** PARCIAL (FRAGIL). O padrão frágil foi mesmo copiado para eda_extremo_belo_horizonte.py:44 em 694c306 (recente). Mas neste script a falha não seria silenciosa. Com um nulo, o filtro zera, e a linha 46 (`.iloc[0]` sobre série vazia) levanta IndexError antes de gravar qualquer extremo_bh_*. O script para com erro, não produz tabelas vazias. O alcance da correção também está incompleto. O mesmo padrão existe em scripts/auditoria_renda.py:89 e :257 (`CD_TIPO.astype(str).eq('1')`), que o F2 da auditoria não listou. Então não são 'os três pontos do F2': são cinco pré-existentes mais este.
- **Onde:** scripts/eda_extremo_belo_horizonte.py:44
- **Evidência:** `df = df[(df.urbano.astype(str) == '1') & (df.Dados_sig == 'OK')]`, criado em 694c306. Teste numa cópia em memória do .db: urbano é int64 e o filtro dá 104.108; com 1 nulo injetado, o dtype vira float64 e o filtro dá 0, sem erro.
- **Impacto:** Mesma falha silenciosa do F2, agora num quarto arquivo. Se o .db ganhar um nulo em urbano, as tabelas extremo_bh_* saem vazias ou quebram em .iloc[0].
- **Correção sugerida:** Usar `pd.to_numeric(df.urbano, errors='coerce').eq(1)` ou `df.urbano.eq(1)`, aqui e nos três pontos do F2.

#### AUD-10 — package.json é ignorado pelo git: pptxgenjs não está declarado no repositório, e a auditoria e o scripts/README dizem o contrário

- **LACUNA · confiança alta**
- **Agente principal:** CONFIRMADO: `.gitignore:79 package.json`.
- **Verificador:** CONFIRMADO (LACUNA). Existe. package.json e package-lock.json estão ignorados desde 91c2134, então não há manifesto nem versão da dependência JS no repositório. O F4 da auditoria ('pptxgenjs está no package.json') e o scripts/README.md:53-54, de de3ce28 (recente), dão a entender que a dependência está declarada no repositório. Um detalhe no impacto: o nome da dependência aparece em arquivos versionados (scripts/README.md:31-34, docstrings 'Requer pptxgenjs (npm)', comentário do .gitignore:76). O que falta é o manifesto com a versão.
- **Onde:** .gitignore:77-79 · docs/relatorios/Auditoria_Integral_2026-09.md:67 (F4) · scripts/README.md:55-57
- **Evidência:** `git check-ignore -v package.json` → '.gitignore:79:package.json'; `git ls-files | grep package` → vazio. O arquivo local tem '"pptxgenjs": "^4.0.1"'; ignorado desde 91c2134, antes da auditoria. A auditoria F4 diz 'O lado JavaScript está correto: pptxgenjs está no package.json'; o scripts/README.md (de3ce28) repete que pptxgenjs 'está, mas no package.json'.
- **Impacto:** Num clone limpo não existe declaração da dependência dos 4 geradores de deck, nem da versão. O F4 é mais amplo do que a auditoria registrou.
- **Correção sugerida:** Tirar package.json e package-lock.json do .gitignore e versioná-los, e corrigir a frase no scripts/README.

### Higiene do repositório e legado (HIG)

#### HIG-09 — O dicionário do projeto dá V00398 como "queimado"; o recorte oficial e o código dizem caçamba

- **DIVERGENTE · confiança media**
- **Onde:** docs/Apresentacoes_IVS/dicionarios/Dicionario_Variaveis_IVS_Censo2022.xlsx (abas Variaveis_Brutas_Censo e Componentes_IVS); docs/Apresentacoes_IVS/README.md:170
- **Evidência:** Aba Variaveis_Brutas_Censo: `V00398 | Destino do lixo — categoria inadequada 1 (queimado, etc.)`. Aba Componentes_IVS: categorias inadequadas "(queimado, enterrado, jogado em terreno baldio, rio/lago, outro)", sem caçamba. Já o Dicionario_IBGE_Oficial_Variaveis_do_Projeto.xlsx, na mesma pasta, diz `V00398 ... Lixo depositado em caçamba de serviço de limpeza` e `V00399 ... Lixo queimado na propriedade`, e src/ivs_censo/indicadores.py:80 diz `V00398 (lixo em caçamba de serviço de limpeza)`. O README, na linha 170, chama o arquivo de "versão de junho de 2026", mas o blob é o de 30/05 (0c9faaf), e a edição de junho (d41b73e) foi revertida (c9378fc).
- **Impacto:** Dois dicionários lado a lado na mesma pasta descrevem a mesma variável de dois jeitos. Quem consultar o "dicionário do projeto" lê errado a composição do indicador de lixo, justo o ponto em que a inclusão da caçamba é decisão em aberto (README.md, item 2 das decisões).
- **Correção sugerida:** Mover o xlsx para historico/ com o prefixo da data (2026-05-30) e trocar a descrição no README para "versão de 30/05/2026, com descrições de V00398–V00402 anteriores à conferência com o dicionário oficial". Outra saída é corrigir as descrições.

#### HIG-10 — Os "~8 GB obsoletos" não estão em Backup/, e o NB01 lê 2,5 GB, não 8 GB

- **DIVERGENTE · confiança alta**
- **Onde:** README.md:196; estrutura_projeto.md:215; GUIA_DO_PROJETO.md:706,754; docs/relatorios/Auditoria_Integral_2026-09.md:23,93
- **Evidência:** `du -sh Backup` = 302M, quase tudo em Backup/banco_de_dados/fase2_bases. `du -sh dados` = 8.0G, mas os 8 CSVs que fontes.py lê somam 2,521 GB (os.path.getsize) e dados/banco_de_dados/ soma 5,99 GB de legado da Fase 1 (SQL/Banco_Censo_Completo.db 3,18 GB, SQL/Banco_IVS.db 1,30 GB, Base_Censo_Completa_Unificada.csv 1,12 GB, temp_merge1.csv 0,20 GB etc.). Nenhum código ativo referencia dados/banco_de_dados (`grep` em src/, scripts/, notebooks/ e tests/ volta vazio). O próprio Backup/DIAGNOSTICO_COMPLETO_PROJETO.md:171-172 localizava o legado em `dados/banco_de_dados/` e `dados/banco_de_dados/SQL/`. A auditoria fala em "travessia de 8 GB de microdados" e "NB01 (lê 8 GB)", mas os microdados lidos têm 2,52 GB (README e estrutura dizem ~2,4 GB). GUIA_DO_PROJETO.md:754 manda "Remover src/ETL/ficheiros_inuteis/", pasta que não existe.
- **Impacto:** Quem limpar Backup/ seguindo o README recupera 0,3 GB, não 8 GB. Os 6 GB de bases mortas da Fase 1 continuam ao lado dos dados brutos que o NB01 lê. O número da auditoria infla em três vezes o volume da pipeline.
- **Correção sugerida:** Corrigir README:196, estrutura:215 e GUIA:706/754 para "~6 GB de bases da Fase 1 em dados/banco_de_dados/ (não usadas)" e corrigir "8 GB" para "2,5 GB" na auditoria. Avaliar mover dados/banco_de_dados/ para fora do repositório, como foi feito com a Fase 2.

#### HIG-11 — estrutura_projeto.md descreve a árvore de antes da reorganização de docs/ e do NB04

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- **Onde:** estrutura_projeto.md:3,21-94,136-137,216
- **Evidência:** O cabeçalho diz "Última atualização: 09/08/2026". Na árvore (linhas 75-83), `Cálculo IVS2012.docx`, `Relatorio_EDA_Fase3_IVS_ELSI.{md,docx}`, `Relatorio_Integridade_Projeto.md`, `Plano de trabalho.pdf` e outros aparecem direto em docs/, mas 4fb9afe os levou para docs/referencias/ e docs/relatorios/. Esse commit mexeu no arquivo só para trocar 2 links (`git show 4fb9afe -- estrutura_projeto.md`) e deixou a árvore como estava. A árvore lista 3 scripts, e há 20; 4 arquivos em src/ivs_censo, e há 6 (faltam fatorial.py e renda.py); 2 testes, e há 3 (falta test_fatorial.py); nenhum NB04. As linhas 136-137 dizem "(a criar) Notebook 03+ → ... análise fatorial" e a 216, "Análise fatorial ... 🔴 Pendente". A base bruta aparece como "~23 MB" (linha 51), o arquivo tem 26.521.455 bytes, e o skip do teste (tests/test_pipeline_fase3.py:40) diz "~17 MB". 0bef9ed, a sincronização com o NB04, não tocou este arquivo. GUIA:13 e MANUAL:48 remetem a ele como a "arquitetura técnica".
- **Impacto:** O documento indicado para entender a estrutura manda procurar arquivos em caminhos que não existem e dá a análise fatorial como não feita.
- **Correção sugerida:** Regerar a árvore a partir de `git ls-files` (ou reduzir o arquivo a um ponteiro para a seção do GUIA) e atualizar as linhas 136-137 e 216.

#### HIG-12 — O README de Apresentacoes_IVS se contradiz sobre qual deck é o atual e onde regerar

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- *Duplicado de AUD-03; mantido pela evidência adicional.*
- **Onde:** docs/Apresentacoes_IVS/README.md:8,24-31,40-50,56,73-77,212
- **Evidência:** A linha 8 (356c32b) diz que Analise_Fatorial_NB04_2026-09.pptx é "A APRESENTAÇÃO". A seção "## A apresentação atual" (linhas 40-50, de 730b91b) continua dizendo "**Arquivo** | `EDA_Central_IVS_2026-09_rev2.pptx` — 51 slides". A linha 56 manda rodar `node scripts/gerar_deck_eda_central.js docs/Apresentacoes_IVS/historico/2026-08-21_EDA_Central_1a_rodada.pptx`, que sobrescreve um arquivo do histórico, e as linhas 73-77 e 212 proíbem justamente isso ("regerá-lo agora produziria um arquivo que nunca existiu"). A linha 31 (9452c32) fala em "21 marcações EXPLICAR SLIDE", mas o deck tem 20 (slides 15, 16, 17, 20, 21, 22, 24, 25, 27, 31-39, 42, 43). A contagem, feita por regex no XML dos slides e das notas, dá 20 também em d2473d6. Os parágrafos das linhas 24-26 e 28-31 repetem a mesma explicação do rodapé "16" do slide 59.
- **Impacto:** Quem abrir a pasta com pressa lê na tabela o nome do deck errado. Quem seguir o comando da linha 56 destrói o arquivo da 1ª rodada, que o próprio README manda preservar (40 slides, contra 47 se regerado).
- **Correção sugerida:** Reescrever a seção "A apresentação atual" para o deck da fatorial (98 slides = 43 + 51 + 4) e passar a descrição da EDA para complementos/. Na linha 56, gravar a saída fora de historico/. Corrigir 21 para 20 e apagar o parágrafo repetido.

#### HIG-14 — A auditoria e o commit 4c476de dizem que o .gitignore exclui o Base_*.csv da entrega; a linha 45 o reinclui de propósito

- **DIVERGENTE · confiança alta · introduzido depois da auditoria**
- **Onde:** docs/relatorios/Auditoria_Integral_2026-09.md:66 (F7) e "Opinião" item 3; mensagem de 4c476de; .gitignore:43-47
- **Evidência:** `git check-ignore -v --no-index banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.csv` devolve `.gitignore:45:!banco_de_dados/entrega_orientadora/*.csv`, isto é, a regra que decide é a exceção, não `banco_de_dados/**/Base_*.csv`. O mesmo vale para o .db (linha 46). `git ls-files -ci --exclude-standard` só lista .claude/settings.local.json. A exceção vem com o comentário "# Exceção: entregáveis específicos para a orientadora (mantidos no histórico)" e já existia antes da auditoria (`git show 4c476de^:.gitignore`).
- **Impacto:** F7, a Opinião 3 e a mensagem de 4c476de ("regra e prática apontam para lados opostos, e qual das duas vale é decisão em aberto") registram uma contradição que não existe. A decisão já está escrita no .gitignore. Quem for "resolver" pode desversionar a entrega sem necessidade.
- **Correção sugerida:** Anotar na auditoria que o F7 não procede e citar a linha 45. Se ainda se quiser discutir o tamanho da entrega versionada, o tema é outro (HIG-16).

#### HIG-08 — O gerador do Dicionario_Variaveis_IVS_Censo2022.xlsx só existe numa worktree órfã

- **ORFAO · confiança alta**
- **Onde:** docs/Apresentacoes_IVS/dicionarios/Dicionario_Variaveis_IVS_Censo2022.xlsx; .claude/worktrees/flamboyant-davinci-bb1785/scripts/gerar_dicionario_variaveis.py
- **Evidência:** O script tem 932 linhas, é de 30/05/2026 e o docstring diz "Gera o Dicionario_Variaveis_IVS_Censo2022.xlsx", com as mesmas 7 abas do xlsx versionado (openpyxl lista Inicio, Componentes_IVS, Variaveis_Brutas_Censo, Variaveis_Derivadas, Guia_por_Arquivo, De_Para_2010_2022, Decisoes_Metodologicas; creator=openpyxl, modified=2026-05-30). `git log --all -S gerar_dicionario_variaveis` e `git grep gerar_dicionario_variaveis` voltam vazios: o script nunca foi commitado. O blob versionado hoje (18347df) é idêntico ao de 0c9faaf (30/05). Houve uma edição em d41b73e, desfeita em c9378fc.
- **Impacto:** Um xlsx versionado não se rastreia até código versionado, e o único gerador está numa pasta ignorada que é candidata natural a limpeza (HIG-07).
- **Correção sugerida:** Copiar o script para Backup/ (ou scripts/, se o dicionário continuar vivo) e commitar, com uma nota de que o xlsx é versão congelada. Outra saída é declarar no README de dicionarios/ que o gerador foi perdido.

#### HIG-13 — Documentos citam commits que não existem no histórico

- **ORFAO · confiança alta**
- **Onde:** docs/relatorios/Auditoria_Integral_2026-09.md:48 (D5); docs/Apresentacoes_IVS/historico/2026-05-28_Correcoes_commit_2fb2e30.pptx e README.md:138,193; graphify-out/graph.json (built_at_commit)
- **Evidência:** `git rev-parse --verify 7df66c4^{commit}` falha: é o commit que o D5 da auditoria diz ter trazido o resumo e o gerador "no mesmo commit (7df66c4, 02/09)", mas o commit real que adicionou os dois é 424bc68. `git cat-file -t 2fb2e30` dá "Not a valid object name", e os commits de 28/05 são 479e8b7 e 3c32d57. 4519cbf (built_at_commit do grafo) também não existe. Os commits de 02/09 têm autor = committer e foram criados em lote às 15:27:07-08, o que é compatível com histórico recriado depois de as referências terem sido escritas. Uma varredura de todos os hexadecimais de 7-8 caracteres nos .md versionados achou só 7df66c4 como referência inexistente (2fb2e30 aparece colado a `commit_` e o grep por palavra não o pegou).
- **Impacto:** As referências de rastreabilidade levam a lugar nenhum. Na auditoria, que é justamente o documento que cobra rastreabilidade, o hash não pode ser conferido.
- **Correção sugerida:** Trocar 7df66c4 por 424bc68 na auditoria. No README do histórico, anotar que 2fb2e30 é um hash anterior à recriação do histórico e apontar o commit equivalente (479e8b7 ou 3c32d57, a confirmar).

#### HIG-01 — Linha 2 do .gitignore corrompida: a regra banco_de_dados/*.csv se perdeu

- **FRAGIL · confiança alta · introduzido depois da auditoria**
- *Duplicado de AUD-01; mantido pela evidência adicional.*
- **Onde:** .gitignore:2-7 (commit 4c476de)
- **Evidência:** `git show 4c476de -- .gitignore`: a versão anterior tinha `banco_de_dados/*.csv` na linha 2. O bloco da Fase 2 foi colado depois de `banco_de_`, no meio do token. Resultado: a linha 2 virou `banco_de_# Legado da Fase 2, arquivado em 17/09/2026: 302 MB ...`, um padrão lixo que não casa com nada. A linha 7 `dados/*.csv` é o resto do token partido e duplica a linha 21. A primeira linha do comentário do bloco da Fase 2 também se perdeu. A regressão passou na revisão porque o mesmo commit converteu o arquivo de CRLF para LF (`git show 4c476de^:.gitignore | od -c` mostra `\r\n`), e o diff saiu como reescrita das 137 linhas. Efeito medido com `git check-ignore -v --no-index`: `banco_de_dados/teste_exportacao.csv` e `banco_de_dados/municipios_recorte.csv` ficam NÃO IGNORADOS. Num repositório de simulação com a regra restaurada, o mesmo caminho passa a casar com `.gitignore:2:banco_de_dados/*.csv`. Hoje nada escapa: o único CSV na raiz de banco_de_dados/ é Base_ELSI_Bruta_Censo2022.csv, que continua ignorado pela linha 17 (`banco_de_dados/**/Base_*.csv`), e `git status --porcelain` está vazio.
- **Impacto:** Hoje não vaza nada. Mas qualquer CSV novo na raiz de banco_de_dados/ cujo nome não comece com Base_ (uma exportação, uma tabela temporária) aparece como não rastreado e pode entrar num `git add .`.
- **Correção sugerida:** Trocar as linhas 2 a 7 por: `banco_de_dados/*.csv` e, em seguida, o bloco da Fase 2 com o seu comentário completo de duas linhas (`# Legado da Fase 2, arquivado em 17/09/2026: 302 MB de bases cuja metodologia foi` / `# abandonada (denominador V01042)...`). Apagar a linha 7 duplicada. Conferir com `git check-ignore -v --no-index banco_de_dados/x.csv`.

#### HIG-04 — package.json e package-lock.json ignorados: quem clona não regera nenhum deck

- **FRAGIL · confiança alta**
- *Duplicado de AUD-10; mantido pela evidência adicional.*
- **Onde:** .gitignore:78-79 (commit 91c2134); scripts/README.md:52-54 (commit de3ce28)
- **Evidência:** `git log --all -- package.json` volta vazio: o arquivo nunca foi versionado. `git check-ignore -v package.json` devolve `.gitignore:79`. Num clone novo (git clone --depth 1 para scratchpad), `node scripts/gerar_deck_fatorial.js saida.pptx` sai com código 1 e a mensagem `pptxgenjs não encontrado:  npm install pptxgenjs` (vem de deck_comum.js:27-30). Esse comando instala a versão mais recente, não a 4.0.1 que o package-lock.json local fixa (`"node_modules/pptxgenjs": {"version": "4.0.1"`). scripts/README.md:53-54 diz que o pptxgenjs está no package.json como se isso estivesse declarado, e a auditoria (F4) diz "O lado JavaScript está correto: pptxgenjs está no package.json". Para quem clona, os dois arquivos não existem.
- **Impacto:** A reprodutibilidade dos 4 geradores .js (três decks e os slides do extremo de BH), que a auditoria atestou byte a byte, só vale nesta máquina, porque depende do node_modules local. Um colaborador pega outra versão do pptxgenjs, ou nenhuma.
- **Correção sugerida:** Tirar `package.json` e `package-lock.json` do .gitignore (linhas 78-79), versionar os dois e manter só `node_modules/` ignorado. Trocar a mensagem de erro para `npm ci`. Corrigir scripts/README.md:53-54.

#### HIG-05 — Com o piso declarado numpy>=1.26, test_acp_varimax_reproduz_csv falha por troca de sinal

- **FRAGIL · confiança alta**
- **Onde:** src/ivs_censo/fatorial.py:129-135 (acp); tests/test_fatorial.py:57-95; banco_de_dados/eda/fatorial/ivs7_spearman_cargas.csv; requirements.txt:9
- **Evidência:** Rodado com `uv run --no-project` sobre um clone em scratchpad: Python 3.10 + numpy 1.26 + pandas 2.2 dá `1 failed, 29 passed` (test_acp_varimax_reproduz_csv, 14/42 elementos diferem, só no sinal das colunas CP2 e Varimax2). Python 3.12 + numpy 1.26 + pandas 2.2: FAILED. Python 3.12 + numpy 2.2 + pandas 2.3: passou. Python 3.13 + numpy 2.5.2 + pandas 3.0.5: passou. `acp()` devolve o autovetor de `np.linalg.eigh` com o sinal cru, e o próprio módulo declara isso na linha 43. O CSV de referência guarda esse sinal cru: a coluna CP1 é toda negativa. O NB04 normaliza o sinal para leitura (célula 19, soma das cargas positiva), mas o CSV e o teste não.
- **Impacto:** O requirements.txt permite um ambiente (numpy 1.26) em que o teste falha e em que o CSV sairia regerado com CP2 e Varimax2 de sinal trocado, sem erro de conteúdo. É o F3 da auditoria se concretizando: o piso declarado não reproduz o projeto.
- **Correção sugerida:** Fixar uma convenção de sinal na extração que grava o CSV (por exemplo, soma das cargas positiva, como no NB04) e regerar ivs7_spearman_cargas.csv. Ou, no mínimo, subir o piso para numpy>=2.2 (testado) e comparar no teste o valor absoluto, ou alinhar com alinhar_cargas().

#### HIG-15 — Rodar de novo os notebooks da Fase 2 recria as bases V01042 na pasta ativa, e o git não mostra

- **FRAGIL · confiança media**
- **Onde:** Backup/Fase2_IVS_Multidimensional/01_*.ipynb:48-49,213; 02_*.ipynb:41,255; 03_*.ipynb:40,86; 04_*.ipynb:37,72; Backup/formatar/busca3.py
- **Evidência:** Nos quatro notebooks da Fase 2, `caminho_bd = '../../banco_de_dados/'`. A partir de Backup/Fase2_IVS_Multidimensional/, isso resolve para a raiz do projeto/banco_de_dados, a pasta ativa. O NB01 lê `caminho_dados = '../../dados/'`, que resolve para os CSVs brutos reais, então roda. As saídas (Base_Bruta_Multidimensional_Censo2022.csv, Base_Analitica_Multidimensional_Calculada.csv, Base_Auditoria_Todos_Setores.csv, Base_IVS_Multidimensional_Formatada.xlsx, Relatorio_Metodologico_Fase2_Atualizado.xlsx) caem em banco_de_dados/ e ficam ignoradas pelas linhas 8 e 17 do .gitignore. Nenhum dos 9 notebooks de Backup/ tem aviso de legado (regex legado|arquivad|obsolet|abandonad: 0 ocorrências). O NB02 da Fase 2 cita V01042 12 vezes e se apresenta como a regra que transforma a base "num índice". busca3.py usa esgoto V00249–V00253, que é tipologia de habitação. Não executei os notebooks, porque gravariam no repositório.
- **Impacto:** 4c476de tirou da pasta ativa as bases da Fase 2 porque os números delas não se comparam com nada. Uma execução distraída as recoloca ali com os mesmos nomes, sem sinal no `git status`. O GUIA (§236-240) e o MANUAL marcam Backup/ como legado, o que atenua, mas quem abre o notebook direto (no GitHub, por exemplo) não vê aviso nenhum.
- **Correção sugerida:** Pôr uma célula markdown no topo de cada notebook de Backup/ ("ARQUIVO MORTO — metodologia V01042 abandonada em 22/05/2026; não executar"). Trocar `caminho_bd` para Backup/banco_de_dados/fase2_bases/, ou fazer a primeira célula de código levantar exceção. Criar um Backup/LEIAME.md na raiz da pasta.

#### HIG-02 — .gitignore com 17 regras mortas, uma linha repetida e negações sem efeito

- **HIGIENE · confiança alta**
- **Onde:** .gitignore:24,25,35,48,55-57,59,60-67 e 36-41
- **Evidência:** O script em scratchpad/revisao/HIG/regras.sh rodou `git ls-files -c/-o -i --exclude=<padrão>` para cada linha. Estas casam com zero arquivos, rastreados ou no disco: 24 `formatar/*.csv` e 35 `!formatar/*.py` (formatar/ foi para Backup/formatar/ em 813cf07, e com isso Backup/formatar/informacoes_agregados.csv passou a ser versionado); 25 `docs/*.xlsx` (a raiz de docs/ não tem mais xlsx depois de 4fb9afe); 48 `dados/banco_de_dados/Banco_IVS_Essencial.db` (o arquivo está em SQL/, que a linha 58 já cobre); 55 e 56 são a mesma linha `data/dicionario_..._20250417.xlsx`, e a pasta data/ nem existe; 57 `docs/Dicionario_de_dados_malha_agregados.ods`; 59 `arquivos_git.txt`; 60-67, oito linhas para `src/ETL/ficheiros_inuteis/*`, pasta que não existe. As negações `!README.md`, `!estrutura_projeto.md`, `!requirements.txt` e `!docs/*.md` não anulam regra nenhuma. `!src/**` e `!tests/**` (linhas 39 e 41) reincluem sob src/ e tests/ o que as linhas 26-30 ignoram (`~*`, `*.log`, `*.tmp`).
- **Impacto:** Quem tenta entender o que o .gitignore protege não consegue separar a regra viva da morta, e foi nesse ruído que a corrupção da linha 2 (HIG-01) passou despercebida.
- **Correção sugerida:** Apagar as linhas mortas (24, 25, 35, 48, 55-57, 59, 60-67) e as negações sem efeito. Trocar as linhas avulsas `dados/banco_de_dados/...` (49-54, 58, 68-69) por uma regra só, `dados/banco_de_dados/`. Rodar regras.sh de novo e confirmar que toda linha casa com alguma coisa ou é preventiva e comentada como tal.

#### HIG-03 — .claude/settings.local.json versionado pré-aprova python -c e git commit para quem clonar

- **HIGIENE · confiança alta**
- **Onde:** .claude/settings.local.json (commits 8339a01 e 15521e5)
- **Evidência:** `git ls-files -ci --exclude-standard` devolve só este arquivo; `.gitignore:33 .claude/` casa com ele, mas a regra entrou depois do commit 8339a01 (15/05/2026) e não desversiona o que já está no índice. Num clone novo em scratchpad o arquivo está presente. Conteúdo, 8 regras `allow`: `Bash(python -c ' *)`, `Bash(python -X utf8 -c ' *)`, `Bash(git add *)`, `Bash(git commit -m ' *)`, `Read(//d/Iniciação Cientifica/**)`, e comandos com `C:\\Users\\Pedro\\.claude\\projects\\D--Inicia--o-...\\memory` e com o worktree `nervous-brahmagupta-f87319`. Não há segredo nele: a varredura de 657 blobs de texto de todo o histórico (scratchpad/revisao/HIG/segredos.py) não achou token, chave nem senha.
- **Impacto:** O Claude Code carrega esse arquivo. Quem clona e usa o Claude Code no projeto herda a execução de Python arbitrário e `git add`/`git commit` sem pedido de permissão, e esta própria máquina também. Isso contraria a regra do autor de que nada roda sem ordem dele. Todos os caminhos são do Windows (D:, C:) e estão mortos no macOS. O arquivo expõe ainda o nome de usuário e a estrutura de pastas local.
- **Correção sugerida:** `git rm --cached .claude/settings.local.json` e commit. O arquivo continua no disco e a linha 33 passa a valer. Aproveitar para limpar as regras com caminho Windows e decidir, por escrito, se `git commit` deve ficar pré-aprovado.

#### HIG-06 — graphify-out/: nomes NFC/NFD duplicados, grafo parcial e cache com caminhos do Windows

- **HIGIENE · confiança alta**
- **Onde:** graphify-out/ (commits 78eb4e4 e 15521e5); graphify.md
- **Evidência:** (1) `git ls-files -s graphify-out/converted/` mostra dois pares com o mesmo blob e nomes que só diferem na normalização Unicode: `Cálculo IVS2012_aef91822.md` NFC e NFD (blob 70cc9bb), `Estudo Longitudinal da Saúde...` NFC e NFD (blob 72bb747). As versões NFD entraram em 15521e5. `git clone` para scratchpad avisa `the following paths have collided ... only one from the same colliding group is in the working tree`. (2) O grafo está velho: GRAPH_REPORT.md é de 2026-08-10, cost.json registra "update parcial ... 16 documentos pendentes", e graph.json aponta `built_at_commit` 4519cbf, que não existe no repositório (`git cat-file -t` falha). Das 35 fontes do grafo, 4 caminhos sumiram na reorganização 4fb9afe (docs/Relatorio_EDA_Fase3_IVS_ELSI.md, docs/Relatorio_Integridade_Projeto.md, docs/Plano de trabalho.pdf, docs/indice_vulnerabilidade2012 (2).pdf). 64 arquivos versionados de código ou documento ficaram fora do manifest, entre eles fatorial.py, renda.py, o NB04 e os 20 scripts (scratchpad/revisao/HIG/graphify_stale.py). (3) `.graphify_root` = `D:\Iniciação Cientifica\Projeto_IVS_Censo22`; `.graphify_python` = `C:\Users\Pedro\AppData\...\python.exe`; as chaves de cache/stat-index.json são caminhos absolutos do Windows e os ids do cache AST começam com `d_iniciação_cientifica_...`, então o cache não serve nesta máquina. (4) converted/ guarda cópias em texto de notebooks antigos e de documentos de terceiros, e um grep aplicado ao repositório inteiro retorna ocorrências nessas cópias velhas. graphify.md, na raiz, ensina comandos de PowerShell e nenhum documento aponta para ele.
- **Impacto:** Um clone no macOS fica com a árvore de trabalho inconsistente com o índice. Com a skill graphify ativa, um agente é instruído a consultar o grafo antes de ler os arquivos, e ele desconhece o NB04, fatorial.py e a reorganização de docs/. docs/prompts/prompt_graphify_atualizacao.md já avisa que o grafo é parcial.
- **Correção sugerida:** Decidir entre duas saídas: (a) tirar graphify-out/ do git (`git rm -r --cached graphify-out` e acrescentar a pasta ao .gitignore), porque é saída regenerável e dependente de máquina; (b) mantê-lo versionado, mas remover no mínimo as duas entradas NFD e cache/, e regerar o grafo nesta máquina. Mover graphify.md para docs/prompts/ ou apagá-lo.

#### HIG-07 — 597 MB em 5 worktrees órfãs em .claude/worktrees, presas a um .git do Windows

- **HIGIENE · confiança alta**
- **Onde:** .claude/worktrees/{flamboyant-davinci-bb1785,gracious-jennings-f0c0db,hopeful-mclean-e9914e,loving-grothendieck-85ff61,recursing-shtern-deac8c}
- **Evidência:** `du -sh .claude/worktrees` = 597M. Cada `.git` contém `gitdir: D:/Iniciação Cientifica/Projeto_IVS_Censo22/.git/worktrees/<nome>`. `git worktree list` mostra só a árvore principal e .git/worktrees não existe, então `git worktree prune` não as enxerga. Comparação por hash, depois de normalizar CRLF, contra todos os blobs do histórico (worktrees_check.sh): 119 de 120 arquivos de texto ou código já estão no histórico. A exceção é flamboyant-davinci-bb1785/scripts/gerar_dicionario_variaveis.py (ver HIG-08). O conteúdo está fora do git (.gitignore:33 e .git/info/exclude).
- **Impacto:** Ocupam espaço e guardam cópias antigas de GUIA, notebooks e bases com o mesmo nome dos arquivos vivos. Uma busca feita fora do git (Finder, grep sem respeitar .gitignore) devolve versões velhas. E a única cópia de um gerador está aí dentro, e se perde junto se as worktrees forem limpas.
- **Correção sugerida:** Primeiro resgatar scripts/gerar_dicionario_variaveis.py (HIG-08). Depois apagar as 5 pastas à mão (não são worktrees registradas).

#### HIG-16 — Três arquivos respondem por 71% dos 127 MiB do .git, incluindo 20 MiB de base morta

- **HIGIENE · confiança alta**
- **Onde:** .git (pack); banco_de_dados/entrega_orientadora/*; Backup/banco_de_dados/Base_Bruta_Multidimensional_Censo2022.csv (histórico)
- **Evidência:** `git count-objects -vH`: size-pack 126,80 MiB. Somando objectsize:disk por caminho (`git rev-list --objects --all | git cat-file --batch-check`): Base_ELSI_70Municipios_Censo2022.db, 3 versões, 41,3 MiB; o .csv correspondente, 3 versões, 28,7 MiB; Backup/banco_de_dados/Base_Bruta_Multidimensional_Censo2022.csv, 2 versões, 19,9 MiB, fora do índice desde 4c476de mas ainda no histórico. Blobs acima de 50 MB, o limite em que o GitHub emite aviso: 69,2 MB (csv da entrega), 67,2 e 66,7 MB (csv da Fase 2), 52,1 MB (db). A mensagem de 4c476de já declara o blob da Fase 2 como custo aceito.
- **Impacto:** Cada regeração da entrega põe de 20 a 40 MiB a mais no histórico, e todo clone paga pelos 20 MiB de uma base que o projeto declarou morta. Não trava nada hoje: nenhum blob passa dos 100 MB, o limite de bloqueio do GitHub.
- **Correção sugerida:** Não reescrever o histórico sem necessidade. Avaliar Git LFS ou a publicação da entrega como release/anexo, e parar de versionar a cada regeração, o que reforça a opinião da auditoria sobre os .db.

#### HIG-17 — Os 3 commits mais recentes saíram com o nome "Pedro Soares"; os outros 95, com "Pedro Dias Soares"

- **HIGIENE · confiança alta · introduzido depois da auditoria**
- **Agente principal:** CONFIRMADO: 95 commits "Pedro Dias Soares", 3 "Pedro Soares" (os desta sessão), mesmo e-mail.
- **Onde:** commits d3ee10b, 694c306, 9452c32; ~/.gitconfig
- **Evidência:** `git log --all --format='%an <%ae>' | sort | uniq -c`: 95 `Pedro Dias Soares <pedro3soares@gmail.com>`, 3 `Pedro Soares <pedro3soares@gmail.com>`. `git config --list --show-origin` mostra `user.name=Pedro Soares` vindo de /Users/pedro/.gitconfig. Não há .mailmap. O e-mail é o mesmo, e nenhum dos 98 commits tem trailer Co-Authored-By.
- **Impacto:** O shortlog e as estatísticas por autor dividem o autor em dois. É só cosmético, e a regra "todo commit é do Pedro" continua cumprida.
- **Correção sugerida:** Acertar user.name no ~/.gitconfig (ou num config local do repositório) e criar um .mailmap com a linha `Pedro Dias Soares <pedro3soares@gmail.com> Pedro Soares <pedro3soares@gmail.com>`.

#### HIG-18 — Dois commits carregam o trailer Claude-Session com a URL pública de uma sessão

- **HIGIENE · confiança media**
- **Agente principal:** CONFIRMADO: `Claude-Session:` em a1b13d2 e a6f05ca.
- **Onde:** commits a6f05ca (13/09) e a1b13d2 (16/09); também d99a242 e 8339a01
- **Evidência:** `git log --all --format='%(trailers:only,unfold)'`: 2 vezes `Claude-Session: https://claude.ai/code/session_01Mf8ZgKpcyc1VbLPnaCweoz`. d99a242 é o merge de `claude/nervous-brahmagupta-f87319`, e a mensagem de 8339a01 é só "Claude". Nenhum Co-Authored-By no histórico.
- **Impacto:** Não viola a regra de autoria (o autor é o Pedro em todos), mas atribui trabalho a uma sessão e, se o repositório for público (não verifiquei), publica o link da sessão. A mensagem "Claude" em 8339a01 não diz o que o commit faz.
- **Correção sugerida:** Não reescrever o histórico por isso. Só evitar o trailer daqui para a frente, por exemplo com um lembrete na memória do projeto.

#### HIG-19 — 25 arquivos rastreados com CRLF no índice, sem .gitattributes

- **HIGIENE · confiança alta**
- **Onde:** raiz do repositório (.gitattributes ausente)
- **Evidência:** `git ls-files --eol`: 207 i/lf, 25 i/crlf, entre eles .claude/settings.local.json, .vscode/settings.json, LICENSE, Backup/ETL/mapeamento_variaveis.py, Backup/formatar/*.py e *.csv, graphify.md e 14 arquivos de graphify-out/. O .gitignore era CRLF e foi convertido para LF em 4c476de, o que produziu o diff de arquivo inteiro que escondeu HIG-01.
- **Impacto:** Toda conversão de fim de linha gera diff de arquivo inteiro e esconde a mudança real, como aconteceu no .gitignore.
- **Correção sugerida:** Criar .gitattributes com `* text=auto eol=lf` e normalizar num commit isolado (`git add --renormalize .`), sem outra mudança junto.

#### HIG-20 — .DS_Store e .vscode/* dependem do ~/.gitignore_global do autor

- **HIGIENE · confiança media**
- **Onde:** .gitignore (ausência); .vscode/settings.json
- **Evidência:** `git check-ignore -v .DS_Store` devolve `/Users/pedro/.gitignore_global:2:.DS_Store`: a regra não está no .gitignore do projeto. Há .DS_Store na raiz, em dados/, docs/, docs/Apresentacoes_IVS/ e notebooks/. .vscode/settings.json está rastreado por `!.vscode/settings.json` do global e define `"python-envs.defaultEnvManager": "ms-python.python:system"`, isto é, o Python do sistema, enquanto README.md:226 e GUIA:823 mandam usar .venv.
- **Impacto:** Um colaborador no macOS sem esse global vê os .DS_Store como arquivos novos. O VS Code de quem clona tende a abrir com o Python do sistema, fora do .venv.
- **Correção sugerida:** Acrescentar `.DS_Store` ao .gitignore do projeto. Tirar a configuração do .vscode/settings.json ou apontá-la para o .venv (`python.defaultInterpreterPath`: `.venv/bin/python`).

#### HIG-21 — Sobras locais sem gerador em banco_de_dados/eda/ e uma cópia de conflito do iCloud no .git

- **HIGIENE · confiança baixa**
- **Onde:** banco_de_dados/eda/estrutura_etaria_contagem_por_setor.csv; banco_de_dados/eda/resp_feminino_contagem_por_setor.csv; .git/index 2
- **Evidência:** Os dois CSVs (8,0 MB e 7,6 MB, de 18/06) estão ignorados pela linha 19 (`*_por_setor.csv`), e `git grep contagem_por_setor` em scripts/, src/, notebooks/ e tests/ volta vazio: nenhum código atual os gera. `.git/index 2` (27 KB, 24/08) tem o padrão de nome de cópia de conflito do iCloud. `xattr -l ~/Documents` mostra `com.apple.file-provider-domain-id: com.apple.CloudDocs.iCloudDriveFileProvider/...`.
- **Impacto:** Tabelas sem procedência na pasta ativa, ao lado das rastreadas de mesmo prefixo. Um repositório git dentro de pasta sincronizada corre risco de corrupção do .git. O estado atual da sincronização (atributo `detached`) não foi confirmado.
- **Correção sugerida:** Apagar os dois CSVs ou movê-los para Backup/. Apagar `.git/index 2`. Se Documentos estiver sincronizado com o iCloud, mover o repositório para uma pasta fora da sincronização.

#### HIG-23 — Os dois commits mais recentes só existem na máquina local

- **HIGIENE · confiança media · introduzido depois da auditoria**
- **Agente principal:** CONFIRMADO: master está 2 commits à frente de origin/master.
- **Onde:** master × origin/master
- **Evidência:** `git log origin/master..master --oneline` mostra 9452c32 e 694c306 (FETCH_HEAD de 24/09 15:27). `git log master..origin/master` volta vazio.
- **Impacto:** A medição do extremo de BH e os 4 slides anexados ao deck não têm cópia fora desta máquina, que além disso pode estar numa pasta sincronizada (HIG-21).
- **Correção sugerida:** `git push` quando o autor decidir. É registro, não ação desta revisão.

#### HIG-22 — A licença MIT da raiz não distingue o código do material de terceiros versionado

- **OPINIAO · confiança baixa**
- **Onde:** LICENSE; docs/referencias/; graphify-out/converted/
- **Evidência:** LICENSE: MIT, "Copyright (c) 2026 Pedro Dias Soares", e README.md:274 diz "Licença: MIT". Em docs/referencias/ estão versionados a publicação do IBGE, o IVS-BH 2012 da PBH, o guia_analises da FIOCRUZ e o documento do ELSI. graphify-out/converted/ tem transcrições integrais de dois deles. docs/referencias/README.md diz que o livro da Enap "não foi versionado" por ser "material de terceiros com direito autoral", critério que não se aplicou aos demais.
- **Impacto:** Quem lê a raiz entende que todo o conteúdo do repositório está sob MIT, o que o autor não pode conceder sobre obras de terceiros.
- **Correção sugerida:** Acrescentar um parágrafo em README/LICENSE (ou um NOTICE) dizendo que a MIT cobre o código e os documentos do autor e que docs/referencias/ traz material de terceiros sob as licenças originais.
