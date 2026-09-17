# O código da análise fatorial, linha a linha

## E como a mesma análise se faz em R

**Projeto:** Índice de Vulnerabilidade à Saúde (IVS) intraurbano — Censo 2022 / ELSI-Brasil
**Módulo comentado:** [`src/ivs_censo/fatorial.py`](../src/ivs_censo/fatorial.py)
**Data:** 17 de setembro de 2026

> **Para que serve este documento.** Duas coisas. Primeiro, permitir explicar em reunião o
> que cada linha do código faz e por que ela está ali — a análise fatorial do projeto foi
> escrita à mão em numpy, e álgebra linear escrita à mão precisa ser defensável linha a
> linha. Segundo, dar a tradução para R, que é a linguagem em que a maior parte da
> bibliografia de análise fatorial está escrita, inclusive o livro da Enap.
>
> A ordem aqui é a ordem em que as coisas acontecem na análise, não a ordem em que
> aparecem no arquivo.

---

## Por que numpy puro, e não uma biblioteca pronta

A pergunta aparece sempre, e a resposta é de engenharia, não de gosto.

O `requirements.txt` do projeto tem cinco pacotes. Acrescentar o `factor_analyzer` traria
conveniência e traria também uma dependência a mais para instalar, versionar e justificar
numa dissertação — por um ganho que é de digitação, não de método. Tudo que a análise
precisa — KMO, Bartlett, componentes principais, Varimax, promax, eixo principal, escores
por regressão — é álgebra linear que o numpy já faz.

Há um ganho colateral que acabou sendo o mais importante: **quem escreve a conta à mão
precisa saber a conta.** Foi escrevendo o KMO que ficou claro que ele se apoia na matriz
anti-imagem, e foi escrevendo o promax que ficou claro por que existem duas matrizes de
carga numa solução oblíqua.

Em R a escolha seria outra, e razoável: o `psych` é padrão da área, está em toda a
bibliografia e não é dependência exótica. A seção final mostra como fazer tudo com ele.

---

## 1. Da base à matriz de correlação

```python
X = dados[colunas].dropna()
n, p = X.shape
R = X.corr(method=metodo).to_numpy()
```

| Linha | O que faz | Por que assim |
|---|---|---|
| `dropna()` | exclusão por lista | Tira o setor inteiro se faltar qualquer uma das variáveis. Custa 16.563 setores e o viés está declarado nas limitações — mas a alternativa, correlação par a par, produz uma matriz em que cada coeficiente vem de um conjunto diferente de setores, e essa matriz pode nem ser positiva definida |
| `n, p = X.shape` | guarda o tamanho | `n` entra no Bartlett; `p` é o número de variáveis, usado em quase tudo |
| `corr(method=metodo)` | matriz de correlação | `'spearman'` como referência e `'pearson'` como sensibilidade. Spearman é correlação de Pearson **sobre os postos** — a escolha está justificada pela assimetria de 3,42 na água e 3,74 na renda |
| `.to_numpy()` | sai do pandas | Daqui em diante é álgebra: rótulo de coluna só atrapalha |

**Em R:**

```r
X <- na.omit(d[, colunas])          # exclusão por lista
R <- cor(X, method = "spearman")    # a matriz-R do livro
```

`cor()` com `use = "complete.obs"` faria o mesmo sem o `na.omit`; com
`use = "pairwise.complete.obs"` faria a versão par a par, que é a que **não** se quer aqui.

---

## 2. Adequabilidade: KMO e MSA

```python
def kmo(R):
    Rinv = np.linalg.inv(R)
    d = np.sqrt(np.diag(Rinv))
    parcial = -Rinv / np.outer(d, d)
    np.fill_diagonal(parcial, 0.0)
    R0 = R.copy()
    np.fill_diagonal(R0, 0.0)
    soma_r, soma_p = (R0 ** 2).sum(), (parcial ** 2).sum()
    msa = (R0 ** 2).sum(axis=0) / ((R0 ** 2).sum(axis=0) + (parcial ** 2).sum(axis=0))
    return soma_r / (soma_r + soma_p), msa
```

A ideia do KMO em uma frase: **compara a correlação bruta entre duas variáveis com o que
sobra dela depois de descontar todas as outras.** Se sobra muito, as duas têm algo próprio
entre si e não um fator comum — e o KMO cai.

| Linha | O que faz |
|---|---|
| `Rinv = inv(R)` | A inversa da matriz de correlação. É dela que saem as correlações parciais — o resultado não é óbvio e é o coração do procedimento |
| `d = sqrt(diag(Rinv))` | Raiz dos elementos da diagonal, que é o fator de padronização |
| `parcial = -Rinv / outer(d, d)` | A fórmula da correlação parcial: `−rᵢⱼ / √(rᵢᵢ·rⱼⱼ)` sobre os elementos da inversa. O sinal negativo não é detalhe: sem ele o sinal de toda a matriz anti-imagem inverte |
| `fill_diagonal(parcial, 0)` | Zera a diagonal. A correlação de uma variável com ela mesma é 1 e entraria na soma inflando tudo |
| `R0` com diagonal zerada | Mesma razão, do lado das correlações brutas |
| `soma_r / (soma_r + soma_p)` | O KMO global: a fração da associação que **não** é parcial |
| `msa` com `axis=0` | O mesmo quociente coluna a coluna — o MSA de cada variável |

O retorno é uma tupla: global e por variável. O piso de Hair é 0,50; a escala de Friel
começa a chamar de "bom" a partir de 0,80. O projeto deu **0,783** com sete variáveis.

**Em R:** uma linha, e devolve as duas coisas.

```r
library(psych)
KMO(R)        # $MSA é o global; $MSAi são os individuais
```

---

## 3. O teste de Bartlett

```python
def bartlett(R, n):
    p = R.shape[0]
    sinal, logdet = np.linalg.slogdet(R)
    if sinal <= 0 or not np.isfinite(logdet):
        raise ValueError(...)
    qui = -(n - 1 - (2 * p + 5) / 6) * logdet
    gl = p * (p - 1) // 2
    return qui, gl, chi2_sf(qui, gl)
```

| Linha | O que faz |
|---|---|
| `slogdet(R)` | Sinal e **logaritmo** do determinante. Usar `log(det(R))` direto estoura em matriz grande: o determinante vira um número pequeno demais para o ponto flutuante representar |
| `if sinal <= 0` | Matriz que não é positiva definida devolveria um qui-quadrado sem significado. Melhor parar do que publicar |
| `qui = -(n - 1 - (2p+5)/6) · log|R|` | A estatística de Bartlett. O termo `(2p+5)/6` é a correção de Bartlett para a aproximação qui-quadrado |
| `gl = p(p-1)/2` | Graus de liberdade: o número de correlações fora da diagonal |

**A ressalva que precisa acompanhar o resultado.** Com 87.545 casos o teste rejeita a
hipótese nula por construção — o próprio livro diz isso na p. 43. O χ² de 235.084 não é
evidência de estrutura forte, é evidência de amostra grande.

**Em R:**

```r
cortest.bartlett(R, n = nrow(X))   # psych
```

---

## 4. Componentes principais

```python
def acp(R, k):
    val, vec = np.linalg.eigh(R)
    ordem = np.argsort(val)[::-1]
    val, vec = val[ordem], vec[:, ordem]
    cargas = vec[:, :k] * np.sqrt(np.maximum(val[:k], 0))
    return val, cargas
```

| Linha | O que faz |
|---|---|
| `eigh(R)` | Decomposição em autovalores e autovetores. O `h` é de *hermitian* — a versão para matriz simétrica, que é mais rápida e mais estável que a genérica. Matriz de correlação é sempre simétrica |
| `argsort(val)[::-1]` | O `eigh` devolve em ordem **crescente**; a análise fatorial lê em ordem decrescente. Sem esta linha, o "primeiro fator" seria o menos importante |
| `vec[:, :k] * sqrt(val[:k])` | **A carga fatorial é o autovetor escalado pela raiz do autovalor.** É a linha que transforma álgebra em interpretação: sem o escalonamento os autovetores têm norma 1 e não se leem como correlação |
| `maximum(val[:k], 0)` | Autovalor negativo por erro numérico viraria raiz de número negativo. Corta em zero |

O sinal de cada autovetor é **arbitrário** — o LAPACK escolhe um, e o oposto seria
igualmente válido. Por isso as cargas são viradas na leitura, para que "positivo" queira
dizer "mais vulnerável".

**Em R:**

```r
e <- eigen(R)                                    # equivalente direto
cargas <- e$vectors[, 1:2] %*% diag(sqrt(e$values[1:2]))

# ou, pronto e com toda a saída de diagnóstico:
acp <- principal(R, nfactors = 2, rotate = "none", n.obs = nrow(X))
```

---

## 5. Fatoração do eixo principal

```python
h = np.clip(smc(R), 0.0, teto_comunalidade)
for it in range(1, maxiter + 1):
    np.fill_diagonal(Rr, h)
    val, vec = np.linalg.eigh(Rr)
    ...
    h_novo = (cargas ** 2).sum(axis=1)
    delta = float(np.abs(h_novo - h).max())
    h = h_novo
    if delta < tol:
        convergiu = True
        break
```

**A diferença entre ACP e análise fatorial cabe numa linha:** o que vai na diagonal da
matriz decomposta. A ACP põe 1 e usa toda a variância de cada variável. A análise fatorial
põe a **comunalidade** e usa só a variância compartilhada.

O problema é que a comunalidade só se conhece **depois** de extrair os fatores. Daí a
iteração:

| Linha | O que faz |
|---|---|
| `h = smc(R)` | Chute inicial: a variância que as outras variáveis explicam de cada uma |
| `fill_diagonal(Rr, h)` | Põe a comunalidade estimada na diagonal |
| `eigh` + cargas | Extrai como na ACP |
| `h_novo = (cargas²).sum(axis=1)` | Recalcula a comunalidade a partir das cargas obtidas |
| `delta` e `break` | Para quando a comunalidade deixa de mudar. No projeto, 192 iterações |
| `teto_comunalidade = 0.999` | O **caso de Heywood**: comunalidade acima de 1 não tem sentido — implicaria variância residual negativa — e costuma indicar fatores demais extraídos. Quando o teto é acionado, isso é reportado, não escondido |

**Em R:**

```r
paf <- fa(R, nfactors = 2, fm = "pa", rotate = "varimax", n.obs = nrow(X))
paf$communality
```

`fm = "pa"` é *principal axis*. `fm = "ml"` seria máxima verossimilhança, que exige
otimização numérica e por isso ficou de fora da versão em Python.

---

## 6. Rotação Varimax

```python
R = np.eye(k)
for _ in range(maxiter):
    Lam = L @ R
    u, s, vt = np.linalg.svd(L.T @ (Lam ** 3 - Lam @ np.diag(np.diag(Lam.T @ Lam)) / p))
    R = u @ vt
    d = s.sum()
    if d_ant != 0 and d / d_ant < 1 + tol:
        break
    d_ant = d
return L @ R
```

Rotacionar é girar os eixos sem mudar as distâncias entre os pontos: a variância explicada
total não muda, só a repartição entre os fatores. O critério da Varimax é **maximizar a
variância dos quadrados das cargas dentro de cada fator** — o que empurra cada carga para
perto de 0 ou de 1 e produz a "estrutura simples".

| Linha | O que faz |
|---|---|
| `R = eye(k)` | Começa sem girar nada |
| `Lam = L @ R` | As cargas com a rotação atual |
| `Lam**3 - Lam @ diag(...)/p` | O gradiente do critério Varimax. O cubo vem da derivada da soma dos quadrados dos quadrados; o segundo termo subtrai a média por fator |
| `svd(...)`, `R = u @ vt` | O truque do procedimento: a matriz ortogonal mais próxima de uma matriz qualquer é `u @ vt` da sua SVD. Garante que a rotação continue ortogonal a cada passo |
| `d / d_ant < 1 + tol` | Para quando o critério deixa de crescer |

**Em R — e aqui há uma armadilha:**

```r
varimax(cargas, normalize = FALSE)   # equivale ao código acima
varimax(cargas)                      # NÃO equivale: normalize = TRUE é o padrão
```

A `varimax` do R aplica **normalização de Kaiser** por padrão: divide cada linha pela raiz
da comunalidade antes de girar e desfaz depois. É defensável e é o que o SPSS faz — mas
produz cargas ligeiramente diferentes. Para reproduzir os números deste projeto em R, é
preciso `normalize = FALSE`.

---

## 7. Rotação promax

```python
V = varimax(cargas)
alvo = np.sign(V) * np.abs(V) ** kappa
U, *_ = np.linalg.lstsq(V, alvo, rcond=None)
d = np.diag(np.linalg.inv(U.T @ U))
U = U @ np.diag(np.sqrt(d))
padrao = V @ U
phi = np.linalg.inv(U.T @ U)
estrutura = padrao @ phi
```

A promax parte da Varimax e deixa os eixos se inclinarem. O procedimento é engenhoso:

| Linha | O que faz |
|---|---|
| `V = varimax(cargas)` | Ponto de partida ortogonal |
| `alvo = sign(V)·|V|^kappa` | Constrói um **alvo exagerado**: com `kappa = 4`, uma carga de 0,9 vira 0,66 e uma de 0,3 vira 0,008. O contraste entre alto e baixo é ampliado |
| `lstsq(V, alvo)` | Acha por mínimos quadrados a transformação que leva `V` o mais perto possível do alvo. É aqui que a ortogonalidade se perde — e é isso que se quer |
| `d = diag(inv(UᵀU))`; `U @ diag(sqrt(d))` | Escala as colunas para que `Φ` saia com **diagonal 1**. Sem este passo Φ é covariância entre fatores, não correlação, e a comunalidade vaza |
| `padrao = V @ U` | A **matriz padrão**: coeficientes de regressão da variável no fator. É dela que saem os pesos |
| `phi = inv(UᵀU)` | A **correlação entre os fatores** — o objeto que a solução ortogonal não pode produzir |
| `estrutura = padrao @ phi` | A **matriz de estrutura**: correlações entre variável e fator |

**A checagem que precisa acompanhar:** numa solução oblíqua uma carga padrão pode passar
de 1 sem ser erro, porque é coeficiente de regressão. Se passar, testa-se a variância
residual: `1 − diag(padrão·Φ·padrãoᵀ)`. Negativa, a solução é inadmissível.

**Em R:**

```r
promax(cargas, m = 4)                                   # stats, base
obl <- fa(R, nfactors = 2, fm = "pa", rotate = "promax", n.obs = nrow(X))
obl$loadings    # matriz padrão
obl$Structure   # matriz de estrutura
obl$Phi         # correlação entre os fatores
```

---

## 8. Escores pelo método da regressão

```python
def escores_regressao(R, cargas):
    return np.linalg.solve(R, cargas)
```

Uma linha, e duas decisões dentro dela.

| Decisão | Por quê |
|---|---|
| `solve(R, A)` em vez de `inv(R) @ A` | Matematicamente igual, numericamente melhor: resolve o sistema sem construir a inversa, que é onde o erro de arredondamento se acumula |
| O que se multiplica depois | Os coeficientes se aplicam às variáveis **padronizadas**. E, como o modelo foi estimado sobre uma matriz de Spearman, se aplicam aos **postos** padronizados — aplicá-los aos valores brutos é erro de categoria, e o sintoma é que a variância dos escores deixa de ser exatamente 1 |

**Em R:**

```r
factor.scores(X, acp, method = "regression")$scores
# ou, em uma linha só: predict(acp, X)
```

---

## 9. Análise paralela de Horn

```python
def horn(n, p, sims=50, semente=42):
    rng = np.random.default_rng(semente)
    acc = np.zeros(p)
    for _ in range(sims):
        X = rng.standard_normal((n, p))
        acc += np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]
    return acc / sims
```

A pergunta que Horn responde: **que autovalor dados sem estrutura nenhuma produziriam?**
Gera dados aleatórios do mesmo tamanho, calcula os autovalores, repete, tira a média. Retém-se
só os fatores cujo autovalor supere esse patamar.

A semente é fixada em 42 porque resultado de simulação que muda a cada execução não é
reprodutível — e o projeto versiona os CSVs.

**Em R:**

```r
fa.parallel(X, fm = "pa", fa = "both", n.iter = 50)
```

Vale notar: a análise paralela **não está no livro da Enap**. Está em nota de rodapé em
Figueiredo & Silva (2010). É um critério mais moderno e mais robusto que o de Kaiser.

---

## O script completo em R

Reproduz a análise inteira. Testado quanto à sintaxe, não quanto aos números — as
diferenças esperadas estão listadas abaixo.

```r
# ── Pacotes ──────────────────────────────────────────────────────────────────
install.packages(c("psych", "GPArotation", "DBI", "RSQLite"))  # uma vez só
library(psych);  library(GPArotation);  library(DBI);  library(RSQLite)

# ── 1. Dados: o mesmo banco que o notebook usa ───────────────────────────────
con <- dbConnect(SQLite(),
  "banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db")
d <- dbGetQuery(con, "
  SELECT pct_agua_inad, pct_esgoto_inad, pct_lixo_inad, razao_moradores,
         pct_analfab, renda_media, pct_raca_pretpardind
  FROM setores_censitarios
  WHERE urbano = 1 AND Dados_sig = 'OK'")
dbDisconnect(con)

d$renda_inv <- -d$renda_media          # sentido único: maior = mais vulnerável
vars6 <- c("pct_agua_inad", "pct_esgoto_inad", "razao_moradores",
           "pct_analfab", "renda_inv", "pct_raca_pretpardind")
X <- na.omit(d[, vars6])               # exclusão por lista
nrow(X)                                # esperado: 87545

# ── 2. Matriz de correlação ──────────────────────────────────────────────────
R <- cor(X, method = "spearman")
round(R, 3)

# ── 3. Adequabilidade ────────────────────────────────────────────────────────
KMO(R)                                 # global e por variável
cortest.bartlett(R, n = nrow(X))       # com a ressalva de amostra grande
smc(R)                                 # multicolinearidade, livro p. 42

# ── 4. Quantos fatores ───────────────────────────────────────────────────────
eigen(R)$values                        # Kaiser: quantos passam de 1
fa.parallel(X, fm = "pa", fa = "fa", n.iter = 50, cor = "spearman")   # Horn

# ── 5. Extração: as duas técnicas, como manda a regra de Stevens ────────────
acp <- principal(R, nfactors = 2, rotate = "varimax", n.obs = nrow(X))
paf <- fa(R, nfactors = 2, fm = "pa", rotate = "varimax", n.obs = nrow(X))
round(cbind(acp$loadings[, 1:2], paf$loadings[, 1:2]), 3)

# ── 6. Rotação oblíqua: é a que o livro recomenda (p. 38) ───────────────────
obl <- fa(R, nfactors = 2, fm = "pa", rotate = "promax", n.obs = nrow(X))
obl$loadings                           # matriz padrão — é dela que saem os pesos
obl$Structure                          # matriz de estrutura
obl$Phi                                # correlação entre os fatores

# ── 7. Pesos: soma dos quadrados das cargas, por fator ──────────────────────
ss <- colSums(acp$loadings[, 1:2]^2)
round(100 * ss / sum(ss), 1)           # a repartição entre as dimensões

# ── 8. Escores ───────────────────────────────────────────────────────────────
escores <- factor.scores(as.matrix(X), acp, method = "regression")$scores
apply(escores, 2, var)                 # tem de dar ~1 com cargas de ACP

# ── 9. O plano dos fatores (a Figura 2 do livro) ────────────────────────────
L <- acp$loadings[, 1:2]
plot(L[, 1], L[, 2], xlim = c(-1, 1), ylim = c(-1, 1), pch = 19,
     xlab = "Fator 1", ylab = "Fator 2", asp = 1)
abline(h = 0, v = 0, col = "grey60")
text(L[, 1], L[, 2], labels = rownames(L), pos = 4, cex = 0.8)

# ── 10. Matriz de correlação como figura ────────────────────────────────────
cor.plot(R, numbers = TRUE, main = "Matriz de correlação de Spearman")
```

### O que esperar de diferente entre as duas implementações

| Ponto | Python (este projeto) | R (`psych`) | Consequência |
|---|---|---|---|
| Normalização da Varimax | sem normalização | `normalize = TRUE` por padrão | Cargas diferem na 2ª ou 3ª casa. Use `rotate = "none"` e depois `varimax(L, normalize = FALSE)` para bater |
| Sinal dos fatores | o que o LAPACK devolver | `psych` vira para que a soma das cargas seja positiva | Compare valores absolutos antes de concluir que divergiram |
| Ordem dos fatores | por autovalor decrescente | idem, mas `fa` pode reordenar após rotação | Confira pelo padrão de cargas, não pelo número do fator |
| Horn | 50 simulações, semente 42, normal padrão | reamostragem dos dados por padrão | Os patamares diferem um pouco; a decisão de quantos reter não deve mudar |
| Spearman | `pandas.corr(method='spearman')` | `cor(method="spearman")` | Idênticos: os dois usam posto médio nos empates |

**Se os números divergirem além disso, o problema é real e vale investigar** — não atribua
à diferença de linguagem sem antes conferir estes cinco pontos.

---

## Onde cada coisa está

| Arquivo | O que tem |
|---|---|
| [`src/ivs_censo/fatorial.py`](../src/ivs_censo/fatorial.py) | Todas as funções comentadas aqui |
| [`tests/test_fatorial.py`](../tests/test_fatorial.py) | 9 testes, incluindo a reprodução exata dos CSVs de agosto |
| [`notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb`](../notebooks/Fase3_EDA_ELSI/04_Analise_Fatorial.ipynb) | O uso: dez blocos, da carga à validação |
| [`scripts/diagnostico_fatorial.py`](../scripts/diagnostico_fatorial.py) | A interface de linha de comando, seis cenários |
