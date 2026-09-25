# Análise fatorial e os pesos do IVS

## Relatório do Notebook 04 — Fase 3

**Projeto:** Índice de Vulnerabilidade à Saúde (IVS) intraurbano — Censo Demográfico 2022 / ELSI-Brasil
**Instituição:** Fiocruz Minas — Instituto René Rachou (IRR) · Iniciação Científica
**Pesquisador:** Pedro Dias Soares
**Data:** 17 de setembro de 2026

**Referência metodológica principal:** MATOS, Daniel Abud Seabra; RODRIGUES, Erica Castilho. *Análise fatorial.* Brasília: Enap, 2019. 74 p.
**Referência anterior:** FIGUEIREDO FILHO, Dalson Britto; SILVA JÚNIOR, José Alexandre da. Visão além do alcance: uma introdução à análise fatorial. *Opinião Pública*, v. 16, n. 1, p. 160–185, 2010.

**Notebook:** `notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb` · **Módulo:** `src/ivs_censo/fatorial.py` · **Saídas:** `banco_de_dados/eda/fatorial/nb04_*`

---

## Sumário executivo

Dez achados, numerados para referência no artigo.

1. **Os pesos do IVS são 65,0% para a dimensão socioeconômica e 35,0% para saneamento**, contra os 60/40 do IVS-BH 2012. Cinco pontos percentuais de diferença entre o peso empírico e o da literatura.

2. **Esses pesos são estáveis à reamostragem de setores, sensíveis ao conjunto de municípios.** Mil reamostragens com reposição (setores, iid) devolvem intervalo de confiança de 95% entre 64,7% e 65,3% — amplitude de 0,59 ponto percentual. Mas os 87.545 setores vêm de 70 municípios, a unidade amostral do ELSI, e a sensibilidade por município (deixar um de fora por vez, no notebook 04b) mostra oscilação maior: só tirar São Paulo já leva o peso a 62,9/37,1. A crítica de instabilidade do livro (p. 23) não se materializa na reamostragem por setor, mas fica em aberto na reamostragem por município.

3. **A escolha entre 65/35 e 60/40 quase não importa para a classificação.** Trocando um pelo outro, 2.196 setores mudam de faixa — 2,5% dos 87.545. A correlação de Spearman entre as duas ordenações é 0,9993. A decisão nº 1 da §6.3 do `GUIA_DO_PROJETO.md` deixa de ser crítica.

4. **O conjunto de variáveis separa os territórios sabidamente vulneráveis; a AUC não valida o esquema de pesos.** Contra os 18.901 setores de Favela e Comunidade Urbana presentes no conjunto completo, a área sob a curva ROC é **0,813** para o índice 0–1 e **0,862** para o escore refinado. Como linha de base (Fase 0): a renda invertida sozinha tem AUC 0,8819 e a média de postos com pesos iguais tem AUC 0,8533 — as duas acima do índice oficial. O marcador é externo ao índice (nenhuma das seis variáveis foi usada para construí-lo), mas a AUC mede conteúdo socioeconômico, não confirma a estrutura fatorial nem os pesos 65/35.

5. **Os dois fatores são correlacionados a 0,522.** A rotação oblíqua, recomendada pela p. 38 do livro, produz a matriz Φ que a solução ortogonal não pode produzir. A magnitude é moderada e positiva, que é o que a teoria da vulnerabilidade prevê — territórios pobres têm pior saneamento.

6. **A repartição da rotação oblíqua não tem uma única resposta.** Pela matriz padrão, a repartição passa de 65,0/35,0 (ortogonal) para 65,8/34,2; pela matriz estrutura, para 59,6/40,4 — mais perto dos 60/40 do IVS-BH. Nenhuma das duas somas de quadrados é partição aditiva com fatores correlacionados, e não se conclui que a oblíqua "afasta" nem que "aproxima" os pesos da literatura.

7. **A concordância entre o índice 0–1 e o escore refinado é 0,924**, abaixo do corte de 0,95 fixado como validação. A causa é de escala, não de amostra: o índice é min-max de valores brutos e o modelo fatorial foi estimado sobre postos. O escore calculado sobre valores brutos — que é o incoerente — dá 0,945. Quanto mais coerente o escore fica com o modelo, mais se afasta do índice planejado.

8. **O indicador de lixo está fora do construto, e a análise fatorial propriamente dita diz isso com mais força que a ACP.** Na solução de sete variáveis, a fatoração do eixo principal atribui ao lixo comunalidade de **0,052**, contra 0,859 da ACP. O fator próprio que ele forma na ACP é variância específica, que a análise fatorial não conta.

9. **Nenhum par da matriz fatorada cruza o limiar de multicolinearidade.** Renda × cor/raça dá **0,784** na matriz listwise de 87.545 setores, abaixo dos 0,80 da p. 42. O −0,811 que os documentos do projeto citam é a correlação par a par da EDA, calculada sobre os 104.108 setores do recorte.

10. **Trocar a renda pela versão sem o valor extremo não muda a análise.** Com
    `renda_media_sem_extremo`, o KMO varia em 0,00003, as cargas batem até a quarta casa
    decimal (maior diferença 0,0000), a repartição dos pesos muda 0,0004 ponto percentual
    e **278 setores** dos 87.544 comparáveis mudam de faixa — 0,32%, com Spearman de
    0,999976 entre os dois índices. A pendência da 2ª rodada da EDA fica resolvida **para a
    fatorial**: Spearman é invariante a essa escala. Sob a normalização MUNICIPAL que o IVS
    vai usar (Notebook 03, não este), o efeito não é o mesmo: 774 de 87.544 setores mudam de
    faixa (NB4-11). Qual renda entra no índice final continua pendente.

11. **A base é adequada, e a adequação depende da escolha por Spearman.** KMO 0,783 e MSA mínimo 0,700 com Spearman; com Pearson, KMO 0,732 (passa, até no patamar "ideal" da Tabela 7), MSA mínimo 0,542 (passa) e apenas 33,3% dos coeficientes acima de 0,30 — a base reprovaria no critério da maioria acima de 0,30 (Etapa 1) e ficaria abaixo dos 60% de variância acumulada (Etapa 2, que a Tabela 7 não traz).

---

## 1. Método e as decisões que o sustentam

Cada decisão com a passagem que a sustenta. As páginas são as da numeração impressa do livro da Enap.

| Decisão | O que foi feito | Onde se apoia |
|---|---|---|
| Recorte | `urbano = 1` e `Dados_sig = 'OK'`; exclusão de casos por lista | §6.2.6 do Guia; o livro não trata de faltantes |
| Correlação | Spearman como referência, Pearson como sensibilidade | Fora do catálogo da p. 11–15, justificado pela assimetria documentada na §9 do relatório da EDA |
| Adequabilidade | KMO e MSA como base da conclusão; Bartlett citado por convenção | p. 43 — o teste "tende a rejeitar a hipótese nula para amostras grandes" |
| Número de fatores | Dois, por razão teórica declarada | p. 32 — a decisão final pode ser teórica; p. 29 — Kaiser é mais preciso com n > 250 e comunalidade média ≥ 0,6 (as duas satisfeitas aqui); Tabachnick & Fidell recomendam Kaiser entre 20 e 50 variáveis (não é o caso, são 6–7) |
| Extração | ACP como principal, eixo principal como sensibilidade | p. 27 — a regra de Stevens (1992) exige o teste quando há menos de 20 variáveis e comunalidades baixas |
| Rotação | Varimax e promax lado a lado, com Φ publicada | p. 38 — rotação ortogonal em Ciências Humanas exige prova de independência |
| Comunalidade | `razao_moradores` mantida com 0,380 | p. 58 — o corte de 0,50 "não deve ser utilizado isoladamente e de maneira muito rígida" |
| Escores | As duas versões calculadas, e a concordância reportada | p. 23–25 — a média ponderada é método "não refinado" |
| Pesos | Proporcionais ao quadrado da carga, dentro e entre dimensões | p. 71 — "quanto maior a carga fatorial, maior a contribuição do item" |
| Ordem NB03 → NB04 | Fatorar sobre os indicadores brutos | §4.4 do documento sobre Figueiredo: normalizar antes derruba o KMO de 0,783 para 0,720 |

**Sobre a nomenclatura.** O que foi feito é **análise fatorial exploratória com o número de fatores orientado pela teoria**, não análise fatorial confirmatória. O livro reserva "AFC" para modelagem de equações estruturais, e é mais rigoroso que Figueiredo & Silva (2010) nesse ponto. A expressão "AFC" não deve aparecer no artigo.

---

## 2. Resultados, bloco a bloco

### Bloco 1 — Carga e recorte

| | |
|---:|---|
| 109.032 | setores no banco da entrega |
| 104.108 | no recorte urbano elegível |
| 87.545 | completos nas sete variáveis |
| 16.563 | perdidos na exclusão por lista — 15,9% |

A perda é quase toda do sigilo do analfabetismo, e a §6.2.6 do Guia documenta que esse sigilo não é aleatório: incide nos setores de melhor situação. A amostra analisada é, portanto, enviesada para os setores mais vulneráveis.

### Bloco 2 — Adequabilidade

| Critério | 7 comp. Spearman | 7 comp. Pearson | 6 comp. Spearman |
|---|---:|---:|---:|
| Casos por variável | 12.506 : 1 | 12.506 : 1 | 14.591 : 1 |
| Coeficientes com \|r\| ≥ 0,30 | 57,1% | 33,3% | 80,0% |
| KMO | **0,7826** | 0,7318 | 0,7870 |
| MSA mínimo | 0,6995 | 0,5422 | 0,7153 |
| Bartlett χ² (21 g.l.) | 235.084,38 | 131.592,71 | 225.320,18 |

A SMC por variável, que a p. 42 recomenda como diagnóstico complementar, mostra o mesmo desenho: renda 0,735 e cor/raça 0,648 no alto; água 0,222 e razão de moradores 0,233 embaixo; e o lixo em **0,106**, o menor de todos — a variável que menos compartilha variância com as demais.

### Bloco 3 — Número de fatores

| Componente | Autovalor (7 var.) | Horn | Autovalor (6 var.) | Horn |
|---:|---:|---:|---:|---:|
| 1 | 3,2997 | 1,0259 | 3,2391 | 1,0232 |
| 2 | **1,0486** | 1,0155 | **0,9585** | 1,0119 |
| 3 | 0,9575 | 1,0075 | 0,7048 | 1,0031 |

Variância acumulada com dois fatores: **62,1%** com sete variáveis, **70,0%** com seis.

Na solução de sete variáveis, Kaiser e Horn retêm dois — mas a decisão se dá com folga de 0,09 entre o segundo autovalor e o terceiro. **Na solução de seis, os dois critérios retêm um só fator.** A retenção do segundo se apoia inteiramente na razão teórica, e isso precisa ser dito como escolha, não escondido atrás de um número.

### Bloco 4 — Extração comparada

Pela regra de Hair (acima de 30 variáveis, ou comunalidades acima de 0,60 na maioria) esperava-se convergência: 5 das 6 comunalidades passam de 0,60. Pela contagem de variáveis de Stevens (30 ou mais), esperava-se divergência. O teste, portanto, não era dispensável, e o resultado (abaixo) cai do lado da divergência, na água.

| Variável | ACP fator 2 | Eixo principal fator 2 | Diferença | Comunalidade ACP | Comunalidade AF |
|---|---:|---:|---:|---:|---:|
| Água inadequada | 0,754 | 0,513 | **0,241** | 0,822 | 0,450 |
| Esgoto inadequado | 0,413 | 0,315 | 0,099 | 0,615 | 0,431 |
| Renda (invertida) | −0,312 | −0,293 | 0,019 | 0,856 | 0,918 |

A divergência se concentra nas variáveis de SMC baixa — água (0,222) e razão de moradores (0,233). É exatamente o que Stevens previu. Nas de SMC alta, renda e cor/raça, as duas técnicas praticamente coincidem.

Na solução de **sete** variáveis a divergência é muito maior, e informativa: o lixo sai de comunalidade 0,859 na ACP para **0,052** no eixo principal. A ACP lhe dava um fator próprio; a análise fatorial mostra que aquele fator é variância específica, não variância comum. Achado nº 8.

### Bloco 5 — Rotação comparada

Solução de seis componentes, sem o lixo. Sinais ajustados para que carga positiva signifique maior vulnerabilidade.

| Variável | Varimax 1 | Varimax 2 | Padrão 1 | Padrão 2 | Estrutura 1 | Estrutura 2 | Var. residual |
|---|---:|---:|---:|---:|---:|---:|---:|
| Água inadequada | 0,087 | **0,903** | −0,211 | **0,999** | 0,310 | 0,889 | 0,178 |
| Esgoto inadequado | 0,392 | **0,679** | 0,207 | **0,656** | 0,549 | 0,764 | 0,385 |
| Razão de moradores | **0,532** | 0,312 | **0,490** | 0,198 | 0,593 | 0,454 | 0,620 |
| Analfabetismo 15+ | **0,868** | 0,127 | **0,930** | −0,111 | 0,873 | 0,374 | 0,230 |
| Renda (invertida) | **0,915** | 0,137 | **0,979** | −0,113 | 0,920 | 0,398 | 0,144 |
| Cor/raça PPI | **0,833** | 0,245 | **0,850** | 0,034 | 0,868 | 0,477 | 0,246 |

**Φ = 0,522.** A estrutura simples se mantém nas duas rotações: nenhuma variável carrega acima de 0,40 em dois fatores. A maior carga padrão em módulo é 0,999, e nenhuma passa de 1 — o teste de variância residual da p. 22 não chegou a ser necessário, e todas as residuais são positivas de qualquer modo.

Repartição do peso: **65,0 / 35,0** na ortogonal, **65,8 / 34,2** na oblíqua, contra **60 / 40** da literatura.

### Bloco 6 — Estabilidade

Mil reamostragens, semente 42. A carga mais instável é a da razão de moradores no segundo fator, com intervalo de 0,293 a 0,334 — amplitude de 0,041. Todas as demais têm amplitude abaixo de 0,026. A repartição entre dimensões fica em **[64,7; 65,3]**.

A incerteza por reamostragem de SETORES é desprezível. Mas os 87 mil setores vêm de 70 municípios, e a sensibilidade por município (04b) mostra oscilação maior no peso — o IC por município chega a incluir o 60/40 da literatura. O que limita esta análise não é só o número pequeno de variáveis: é também a unidade de reamostragem.

### Bloco 7 — Pesos e escores

| Variável | Dimensão | Carga | Peso |
|---|---|---:|---:|
| Água inadequada | Saneamento | 0,903 | **22,32%** |
| Esgoto inadequado | Saneamento | 0,679 | **12,64%** |
| Renda (invertida) | Socioeconômica | 0,915 | **21,21%** |
| Analfabetismo 15+ | Socioeconômica | 0,868 | **19,09%** |
| Cor/raça PPI | Socioeconômica | 0,833 | **17,57%** |
| Razão de moradores | Socioeconômica | 0,532 | **7,17%** |

O índice 0–1 vai de 0,065 a 0,830, com mediana 0,354. Os escores pelo método da regressão, calculados sobre os postos padronizados, têm variância exatamente 1 — o que confirma a implementação de B = R⁻¹A.

A concordância entre as duas medidas é **0,924** (escore sobre postos) e **0,945** (escore sobre valores brutos). Achado nº 7.

### Bloco 8 — Cenários

Métrica: quantos setores mudam de faixa, em quartis, contra o cenário de referência (dois fatores, pesos empíricos).

| Cenário | Setores que mudam de faixa | % | Spearman |
|---|---:|---:|---:|
| Pesos 60/40 em vez de 65/35 | 2.196 | 2,5% | 0,9993 |
| Sem o analfabetismo | 6.587 | 7,5% | 0,9948 |
| Um fator em vez de dois | 7.668 | 8,8% | 0,9830 |

O cenário sem o analfabetismo recupera 16.548 setores, chegando a 104.093 — praticamente o recorte inteiro.

### Bloco 9 — Validação externa

| Medida | AUC | Mediana nos setores de FCU | Mediana nos demais |
|---|---:|---:|---:|
| Índice 0–1 | **0,8131** | 0,4047 | 0,3385 |
| Escore refinado | **0,8616** | 0,7289 | −0,2523 |

18.901 setores de FCU contra 68.644. Ambos acima do corte de 0,75 fixado como separação nítida, e bem acima do 0,65 que seria problema de validade.

---

## 3. As decisões que vão para a orientação

Nenhuma foi fechada aqui. O custo de cada opção está medido.

| # | Decisão | As opções, e o que cada uma custa |
|---|---|---|
| 1 | **Pesos empíricos ou 60/40 da literatura** | Convergem. Trocar um pelo outro move 2,5% dos setores de faixa. O argumento a favor dos empíricos está na p. 71: itens contribuem de forma desigual, e pesos iguais dariam "três votos" à posição social sem escolha deliberada. O argumento a favor de 60/40 é a comparabilidade com o IVS-BH 2012 |
| 2 | **Destino do indicador de lixo** | Fora do índice: a variância acumulada sobe de 62,1% para 70,0%, a estrutura teórica aparece limpa, e a água sai de comunalidade 0,253 para 0,822. Dentro: fidelidade literal ao `Cálculo IVS2012.docx`, ao custo de dar peso a uma dimensão que não é vulnerabilidade — comunalidade de 0,052 pelo eixo principal |
| 3 | **Política do sigilo no analfabetismo** | Manter a variável: 16.548 setores ficam sem índice. Retirá-la: recupera-os, ao custo de 7,5% dos setores mudando de faixa e da perda de um componente do bloco socioeconômico |
| 4 | **Um fator ou dois** | Um: é o que Kaiser e Horn indicam na solução sem lixo, e dispensa toda a discussão de rotação (p. 69). Dois: preserva a estrutura do IVS-BH e a leitura por dimensões. Custo da troca: 8,8% dos setores mudam de faixa |
| 5 | **Rotação ortogonal ou oblíqua** | Oblíqua é a recomendada pela p. 38 e produz Φ = 0,522 como evidência de validação. Ortogonal é mais simples de reportar e é o que a literatura do IVS usa. Custo não bem definido: 0,8 p.p. no sentido oposto ao 60/40 pela matriz padrão, ou 5,4 p.p. no sentido do 60/40 pela matriz estrutura |
| 6 | **Índice 0–1 ou escore refinado** | O 0–1 é interpretável, comparável com o IVS-BH e reproduzível com sete números numa tabela. O refinado é estável e separa melhor as favelas (AUC 0,862 contra 0,813). A concordância de 0,924 ficou abaixo do corte que validaria o primeiro sem ressalva |

---

## 4. Limitações

1. **O Bartlett é vazio nesta escala.** Com 87.545 casos o teste rejeita H₀ por construção (p. 43). A adequabilidade se apoia no KMO e nos MSA individuais, que não crescem com o *n*.
2. **ACP sobre matriz de Spearman é ACP de postos.** As cargas descrevem posições relativas, não magnitudes. A solução de Pearson está reportada como sensibilidade. Esta limitação tem custo medido: é a causa do achado nº 7.
3. **Multicolinearidade.** Renda × cor/raça a 0,784 na matriz fatorada — abaixo do limiar de 0,80, mas alto. O −0,811 dos documentos do projeto é par a par, sobre outro conjunto de setores. O artigo precisa citar o número da matriz que foi fatorada, e dizer qual é qual.
4. **Viés não aleatório do sigilo.** 16.563 setores perdidos, incidindo nos de melhor situação. O livro da Enap não discute dados faltantes em nenhuma das 74 páginas; o tratamento adequado exigirá literatura que o projeto ainda não tem.
5. **Dependência espacial não tratada.** A análise fatorial pressupõe unidades independentes; setores vizinhos não são. A autocorrelação infla a covariação e, com ela, autovalores e cargas. O I de Moran dos escores, na etapa de geoprocessamento, dará a medida.
6. **Falácia ecológica.** As unidades são territórios. Toda carga descreve covariação entre setores e nada afirma sobre indivíduos.
7. **A padronização usada aqui é min-max global e provisória.** A normalização por município é do Notebook 03.
8. **Reflexivo ou formativo** — tratado na §5 abaixo. A análise fatorial pressupõe o modelo reflexivo; se o IVS for formativo, parte dos diagnósticos deste relatório não se aplica e a decisão sobre o lixo se inverte.

---

## 5. O IVS é construto reflexivo ou índice formativo?

É a objeção conceitual mais séria em aberto, e não se resolve com mais dados. Ela decide se
a análise fatorial é o instrumento certo.

**Num construto reflexivo, o latente causa os indicadores.** A vulnerabilidade existiria
como propriedade do território e se manifestaria em renda baixa, analfabetismo, saneamento
precário. Os indicadores são intercambiáveis, devem correlacionar-se alto, e retirar um não
muda o que o construto significa. É esse o modelo que a análise fatorial pressupõe — dele
vêm o KMO, o Bartlett, a comunalidade e a própria ideia de carga.

**Num índice formativo, os indicadores constituem o índice.** Vulnerabilidade *é* a
combinação de privações; cada indicador é uma faceta definidora. Eles não precisam
correlacionar-se, retirar um muda o significado, e os pesos viriam de teoria ou de decisão
política. Bollen & Lennox (1991) é a formulação canônica; o manual da OCDE/JRC (Nardo et
al., 2008), referência para indicadores compostos, os trata como formativos por padrão.

| Resultado deste relatório | Leitura reflexiva | Leitura formativa |
|---|---|---|
| Lixo com comunalidade 0,052 | não pertence ao construto: **retirar** | faceta de saneamento que as outras não cobrem: **manter** |
| Renda × cor/raça a 0,784 | bloco coeso, evidência do construto | multicolinearidade: atrapalha separar as contribuições |
| KMO 0,783 e Bartlett | provam adequabilidade | **não se aplicam** — não há modelo de fator comum a testar |
| Pesos 65/35 empíricos | saem da estrutura latente | teriam de sair de teoria ou de política pública |

**A decisão sobre o lixo se inverte entre as duas leituras.** É o exemplo mais claro de que
isto não é preciosismo terminológico.

### A saída que os dados sugerem

A estrutura encontrada aponta para um híbrido, e ele é defensável. *Dentro* de cada
dimensão o modelo se comporta como reflexivo: renda, analfabetismo e cor/raça
correlacionam-se de 0,63 a 0,78 e manifestam uma mesma posição social do território; água e
esgoto, a 0,41, manifestam infraestrutura de saneamento. *Entre* as duas dimensões a
composição é formativa: não há razão para supor um latente único que cause tanto a falta de
água quanto o analfabetismo — e a correlação Φ de 0,522 entre os fatores, longe de 1, é
consistente com isso.

Se esse for o modelo, a consequência já está medida neste relatório: a análise fatorial é
legítima para obter os pesos **dentro** de cada bloco, e a repartição **entre** blocos — o
65/35 — é decisão formativa, que os dados não têm como arbitrar. Isso explica, e justifica,
por que a escolha entre 65/35 e 60/40 custa apenas 2,5% dos setores: ela nunca foi uma
questão empírica.

**O que falta:** literatura própria. Bollen & Lennox (1991), Diamantopoulos & Winklhofer
(2001) e Edwards (2011) são o núcleo da discussão, e nenhum está lido no projeto. Nem o
IVS-BH 2012 nem o ISU de Passarelli-Araujo (2023) declaram a posição deles.

---

## 6. Reprodutibilidade

```
src/ivs_censo/fatorial.py          a matemática: KMO, MSA, Bartlett, Horn, ACP,
                                   eixo principal, Varimax, promax, SMC, escores,
                                   bootstrap — numpy e pandas apenas
tests/test_fatorial.py             8 testes, entre eles a reprodução exata dos CSVs
                                   de referência de agosto
scripts/diagnostico_fatorial.py    interface de linha de comando, seis cenários
notebooks/.../04_Analise_Fatorial.ipynb   os dez blocos deste relatório
```

Entrada: `banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db`, tabela `setores_censitarios`. Nenhum dado bruto do Censo é necessário.

Saídas em `banco_de_dados/eda/fatorial/`, prefixo `nb04_`, separador `;`, codificação `utf-8-sig`. Figuras em `figuras/`, 150 dpi.

```bash
./.venv/bin/python -m pytest tests/test_fatorial.py
jupyter execute notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb
```

O código está comentado linha a linha, com a tradução para R, em
[`Codigo_Analise_Fatorial_Comentado.md`](../metodologia/Codigo_Analise_Fatorial_Comentado.md).

O notebook trava em três pontos: o recorte de 104.108 setores, os 87.545 completos, e os valores de KMO, MSA e Bartlett do diagnóstico de agosto. Se qualquer um divergir, ele para.

---

## Referências

MATOS, D. A. S.; RODRIGUES, E. C. **Análise fatorial**. Brasília: Enap, 2019. 74 p. (Coleção Metodologias de Pesquisa).

FIGUEIREDO FILHO, D. B.; SILVA JÚNIOR, J. A. Visão além do alcance: uma introdução à análise fatorial. **Opinião Pública**, Campinas, v. 16, n. 1, p. 160–185, jun. 2010.

HORN, J. L. A rationale and test for the number of factors in factor analysis. **Psychometrika**, v. 30, p. 179–185, 1965.

STEVENS, J. P. **Applied Multivariate Statistics for the Social Sciences**. 2. ed. Hillsdale: Erlbaum, 1992.

TABACHNICK, B. G.; FIDELL, L. S. **Using Multivariate Statistics**. Needham Heights: Allyn & Bacon, 2007.

BOLLEN, K.; LENNOX, R. Conventional wisdom on measurement: a structural equation perspective. **Psychological Bulletin**, v. 110, n. 2, p. 305–314, 1991.

DIAMANTOPOULOS, A.; WINKLHOFER, H. M. Index construction with formative indicators: an alternative to scale development. **Journal of Marketing Research**, v. 38, n. 2, p. 269–277, 2001.

HENDRICKSON, A. E.; WHITE, P. O. Promax: a quick method for rotation to oblique simple structure. **British Journal of Statistical Psychology**, v. 17, n. 1, p. 65–70, 1964.

NARDO, M. et al. **Handbook on Constructing Composite Indicators**. Paris: OECD/JRC, 2008.

SECRETARIA MUNICIPAL DE SAÚDE DE BELO HORIZONTE. **Índice de Vulnerabilidade à Saúde 2012**. Belo Horizonte: SMS-BH, 2013.

---

*Documentos do projeto citados: `GUIA_DO_PROJETO.md` (§6.2.6, §6.2.8, §6.2.10, §6.3) · `docs/metodologia/Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md` · `docs/relatorios/Relatorio_EDA_Fase3_IVS_ELSI.md` (§9, §13, §15).*
