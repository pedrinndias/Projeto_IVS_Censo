# Simplificação do código e correção dos erros da revisão de 22/10/2026

Ramo `simplificacao-codigo` (a partir de `b0863ce`). Prompt: `docs/prompts/prompt_simplificacao_correcoes_2026-10.md`;
estado: `docs/prompts/estado_simplificacao_2026-10.md`. Nada foi enviado ao GitHub, e a `main` não foi tocada.

| Fase | Commit | O quê |
|---|---|---|
| 0 | `7fcf56a` | linha de base: trabalho pendente, 98 figuras `* 2.png` duplicadas apagadas |
| 1 | `537fc52` | os 8 erros (E1–E8), cada um com teste |
| 2 | `eebb6e0` | simplificação com prova de equivalência |
| 3 | `ae11a98`, `85ced4a` | saídas regeradas (399 arquivos) e notebook 05 |
| 4 | este commit | relatório, documentação, grafo |

**Resultado em uma frase:** os 8 erros estão corrigidos e as saídas regeradas; testes de 125 para 165 (todos verdes), avisos do
`ruff` de 44 para 4; as cópias do código foram unificadas sem mudar nenhuma saída que não devesse mudar.

---

## 1. Simplificação

### Linhas antes × depois

| Pasta | Antes (`7fcf56a`) | Depois | Variação |
|---|---:|---:|---:|
| `src/ivs_censo/*.py` | 1.429 | 1.483 | +54 (as funções compartilhadas novas de `fontes.py`) |
| `scripts/*.py` (57 arquivos) | 23.007 | 22.915 | −92 |
| `scripts/*.js` (14 arquivos) | 5.607 | 5.613 | +6 |
| `tests/*.py` | 1.908 | 2.114 | +206 (testes novos) |
| NB01, código das células | 289 | 254 | −35 |
| NB02, código das células | 961 | 892 | −69 |
| `ruff` (F, E9, B, PLE) | 44 avisos | 4 | −40 |

O ganho é de **cópias**, não de linhas: o que antes existia em até quatro lugares passou a existir em um. Em `src` o código cresceu
porque as funções compartilhadas agora moram lá e os scripts e notebooks as chamam.

### O que foi juntado (cada item com prova de equivalência na base real, sem tolerância)

| # | Antes | Agora | Prova |
|---|---|---|---|
| S1 | leitura de CSV do IBGE com tentativa utf-8 → latin1 em 4 lugares (NB01 ×2, NB02, `proporcoes_brasil`) | `fontes.ler_csv_ibge` | 3 arquivos nacionais (2 pedaços), 7 `ler_filtrado`, `ler_csv_padronizado` e o laço do NB02: `assert_frame_equal` exato e log idêntico |
| S2 | conversão "X → ausente, vírgula → ponto, número" e leitura da base bruta em 5 lugares; `COLS_TEXTO` em 4 cópias | `fontes.para_numero`, `fontes.ler_base_bruta`, `COLS_TEXTO_BASE_BRUTA` | os 3 carregadores antigos × `ler_base_bruta`: iguais |
| S3 | normalização do nome do município em 2 lugares | `fontes.normaliza_nome` | `is_elsi` igual nos 468.099 setores (muda só o nome ausente: `''` no lugar de `'nan'`, 2 setores) |
| S4 | Spearman em 3 versões | `ie.spearman` (descarta pares ausentes); `eda_versoes.rho` é alias | 1.494 comparações em todos os pares de indicadores, global e por município: 0 diferentes |
| S6 | limiares de elegibilidade em 3 lugares | `ie.CRIT` e `ie.cargas_rotacao` | 24 comparações: 0 diferentes. `ie.elegibilidade` e `fm.elegivel` **não** foram juntadas (colunas diferentes dos CSVs) |
| S7 | `comparar_edicoes_versoes.py` 86% igual ao do relatório | `relatar(...)` no do relatório; o de versões só a chama | stdout e CSV iguais byte a byte nos 3 decks reais |
| S8 | 5 laços "por região / por município" no NB02 | `_desc_long` definido uma vez e usado em todas as seções; releitura de `mapa_regiao` removida | NB02 reexecutado: **nenhum CSV de `eda/` mudou** |
| S9 | KMO calculado 2× por combinação na camada 1 | `fm.diagnostico` devolve o MSA | 28 comparações: 0 diferentes |
| S10 | 28 imports e f-strings sem uso, variáveis mortas | `ruff --fix` e ajustes | pytest |
| S11 | 98 figuras `* 2.png` idênticas | apagadas na Fase 0 (`cmp`) | — |

Apagados, por não ter nenhuma referência: `COLUNA_N_RESP`, as constantes `BART` e `A7` de `gerar_pdf_plano_emergencia.py`, `fm.comparar`,
`vf.spearman`, e o `FX` de `versoes_fatorial.py` (ficou sem uso depois do E2).

### O que ficou registrado sem mexer, e por quê

* **S5 (formatação pt-BR):** nenhuma das 8 funções `br` tem a mesma semântica de `eda_versoes.br`. Mudam as casas padrão (2, 3 ou 4) e o tratamento de
  ausente (`—` ou `nan`); a de `gerar_pdf_guia_decks_outubro.py` nem tem separador de milhar; a da RAIC fica por regra. Juntar exigiria adaptador.
* **`sid` (4 scripts) e `item` (2 verificadores):** corpo igual, mas cada arquivo usa o seu próprio regex `ID` ou estado.
* **Parâmetros opcionais que ninguém passa** (`tol`, `maxiter`, `kappa`, `semente`, casas): são afinações documentadas de algoritmos e de formato.
* **`dados_relatorio_descritivo.py`:** as funções `a01…z02` parecem sem chamador, mas são despachadas por `globals()`.
* **Fora do escopo do prompt:** os dois `gerar_deck_*.js` que ainda não usam `deck_comum.js`, os scripts de passo único e `Backup/`.

---

## 2. Os 8 erros

Cada correção de código tem um teste que falha antes dela (verificado contra o código antigo). O E4 (só texto) é coberto por uma conferência nova do `verificar_multiversao.py`, que falha nas saídas antigas, e o E6 é um teste de leitura que passa. Os números "antes" são os das saídas versionadas no commit da Fase 0; os "depois"
são as saídas regeradas. Parte da diferença vem da correção de 22/10 (setor único sem régua municipal fica com IVS ausente), que ainda não tinha sido regerada.

### E1. O IVS ausente não era tratado por quem consome o índice

* **Causa:** a correção de 22/10 deixa o IVS ausente num município sem variação, mas `auc_postos` contava o ausente como "fora de favela", a logística
  do NB05 saía toda `nan` e a versão C5 quebrava com `IntCastingNaNError`.
* **Correção:** `fa.auc_postos` e `ie.spearman` descartam pares ausentes (conserta todos os chamadores de uma vez); `faixas_alternativas` trata o
  ausente como faixa −1; no `ie.main` os dois modelos da logística usam a mesma amostra.
* **Testes:** `test_auc_postos_e_spearman_descartam_ausentes`, `test_faixas_alternativas_aguenta_ivs_ausente`.
* **Números:** `acrescimo_renda.csv` sai com **0** células `nan` nas colunas da logística; a C5 volta a gerar T36–T38 e F30. A AUC global mudou em
  108 das 648 linhas de `avaliacao.csv`, e a maior mudança foi **0,000003**. A AUC municipal da referência continua 0,8186.
* **Sem teste unitário:** o trecho da logística dentro do `ie.main` (inline); a verificação foi a Fase 3.

### E2. "% que muda de faixa" comparava faixas de amostras diferentes

* **Causa:** cada versão calculava as faixas na própria amostra, e setores a mais mudam a média do município. A troca medida era da amostra, não do método.
* **Correção:** uma só função, `ie.comparar(a, b, mun, regra)`, que refaz as faixas das duas versões na amostra comum; `fm.comparar` foi removida, e `ie.main`,
  `versoes_fatorial` e `eda_versoes` (bloco 13 e T34) passaram a usá-la.
* **Teste:** `test_comparar_nao_confunde_amostra_com_metodo` (agora também com `regra='quartis'`).
* **Números (NB05, elegíveis, amostra comum, mediana, antes → depois):**

| Troca de faixa pela regra do IVS-BH | Antes | Depois |
|---|---:|---:|
| normalização municipal | 9,72% | 7,18% |
| normalização global | 16,23% | 15,19% |
| rotação promax | 12,12% | 10,11% |
| rotação varimax | 14,55% | 12,01% |
| por quartis, municipal | 8,53% | 5,00% |
| por quartis, global | 14,72% | 13,04% |

* **Por versão (T33, "Todos"):** A1 3,74% → 1,64%; B3 12,95% → 8,90%; B2 13,90% → 13,88%; as demais mudam menos de 0,4 ponto, e `D2` 49,80% → 49,86%.
* **108 versões (mediana da troca por par):** banheiro fora → graduado 11,33% → 6,57%; fora → v00495 9,75% → 6,84%; v00495 → graduado 2,64% → 1,59%;
  água nenhuma → nao_chega 16,31% → 14,99%; lixo com → sem 8,23% → 8,39%. A troca de V002 em relação à V023 vai de 38,6% para 36,8%.

### E3. A replicação entre metades usava sempre a promax

* **Causa:** `camada3` calculava o Tucker com `promax_padrao` mesmo quando o finalista era sem rotação (1 fator), e por isso o E0001 mostrava o Tucker da proposta.
* **Correção:** `fm.tucker_metades` usa a matriz da rotação do finalista; com 1 fator, `tucker_F2` fica ausente e o slide mostra "—".
* **Testes:** `test_replicacao_usa_a_rotacao_do_finalista`; `verificar_multiversao.py --fase 3` (confere o F2 ausente).
* **Números:** só o E0001 mudou: F1 0,967 → **0,996** e F2 0,924 → **—**. A proposta (E0009) e os outros finalistas ficaram iguais.

### E4. O eixo "normalização" troca duas coisas juntas

* **Decisão do prompt:** o método não muda (o pré-registro não muda depois da Fase 1). Corrigi só o texto: o "Como ler" dos slides do eixo (FIN-39 e FIN-40) e a
  limitação nova no FIN-75 dizem que a alternativa por postos troca a matriz da fatorial (calculada dentro do município) junto com a régua, e que os 31,8% não são só efeito da régua.
* **Conferência:** `verificar_multiversao.py --fase 4`.

### E5. A E2 reamostrava setores

* **Causa:** o próprio projeto concluiu que reamostrar setores subestima a incerteza (FIN-06 e FIN-55): a unidade é o município.
* **Correção:** `et.sortear_municipios` sorteia municípios com reposição (mesmas 1.000 réplicas e semente); os textos de `textos_blocos.json` foram ajustados.
* **Teste:** `test_bootstrap_sorteia_municipios_inteiros`.
* **Números (intervalo de 95% do peso no índice, antes → depois):**

| Componente | Referência | Antes | Depois |
|---|---:|---|---|
| Água inadequada | 17,3% | [16,8; 17,9] | [14,0; 22,2] |
| Esgoto inadequado | 7,8% | [7,3; 8,3] | [3,6; 12,0] |
| Razão de moradores | 7,5% | [7,1; 7,8] | [3,2; 10,8] |
| Analfabetismo 15+ | 17,4% | [17,2; 17,5] | [15,0; 20,0] |
| Renda (invertida) | 19,3% | [19,1; 19,5] | [16,4; 23,5] |
| Cor/raça PPI | 15,9% | [15,8; 16,0] | [13,9; 20,2] |
| Banheiro graduado | 14,9% | [13,9; 15,8] | [4,8; 24,2] |

  KMO [0,7777; 0,7835] → [0,7220; 0,8121]; Spearman com a referência [0,9999; 1,0000] → [0,9944; 0,9999]; AUC municipal [0,8163; 0,8208] → [0,8045; 0,8298].
  **A amplitude do intervalo ficou de 8 a 23 vezes maior** (água 1,08 → 8,24 pontos; banheiro graduado 1,86 → 19,43), e o peso do banheiro graduado é o menos estável.

### E6. Números digitados à mão nos geradores da RAIC

* **O teste:** `tests/test_numeros_raic.py` (somente leitura) calcula cada número dos CSVs, formata em pt-BR e confere que aparece no texto do gerador.
  Os geradores congelados não foram tocados.
* **Resultado:** os 29 casos cobertos **batem com os dados** (o funil 109.032 → 104.108, os R$ 170.418,06 e R$ 140.172,64, o Brasil × ELSI e a cobertura do analfabetismo). Não houve `xfail`.
* **Não cobertos** (sem fonte simples de dados): 79,99 × 80,0, 14,9% (água), 52,1 milhões, as medianas 2.313,87 e 6.092,84, as médias 3,64 e 3,14, 99,98%, a Tabela 1 e a Figura 1.

### E7. Caminhos padrão de decks que não existem mais

* **Correção:** o `ESTADO.md` não nomeia o deck de trabalho, então o caminho virou argumento obrigatório em `comparar_edicoes_relatorio.py` e
  `anexar_versoes_ao_relatorio.py`, e `--saida` é obrigatório em `gerar_relatorio_descritivo.js`. Sem isso, o gerador recriava um "principal" fantasma e regravava o hash e o `ultimo_gerado.pptx`.
* **Testes:** `tests/test_decks_caminho_obrigatorio.py`.

### E8. Município faltando passava como "BASE APROVADA"

* **Correção:** no NB01, o ramo "município faltando" conta como erro (`erros += 1`). Edição de 2 linhas no texto do `.ipynb`.
* **Teste:** `test_nb01_conta_municipio_faltando_como_erro`. O NB01 foi reexecutado: o sha256 da base bruta e do `.db` nacional **não mudou**.

---

## 3. Entregáveis afetados e não regerados

Os decks abaixo têm trava (edição à mão) e **não foram regerados**; os dados (`.json`, `.xlsx`, figuras) foram.

| Entregável | Slides cujo número mudou | Valor novo |
|---|---|---|
| Relatório descritivo (v3, v4_APOIO e derivados) | **FA12** | 73.878 → **73.877** setores no IVS final |
| | **FA13** | tabela das faixas por quartis: aparece "indefinida: 1 setor"; "muito elevado" 18.493 → **18.492** |
| | **FP13** | queda da deviance ao somar o índice à renda 135,45 → **134,34**; z do índice 17,48 → **17,44** |
| | **DS16** (só no v4_APOIO) | 2 textos de apoio |
| Decks das 108 versões, principal | **VP08 a VP13** | a frase-resumo do eixo da renda cita agora "renda original → sem extremo" (antes, "renda original → mediana"); células: VP09 `8,4% [4,5%; 35,5%]`, VP10 `15,0% [4,4%; 34,3%]`, `12,4% [3,9%; 27,9%]`, `4,7% [2,7%; 10,2%]`, VP11 `6,8% [4,1%; 25,0%]` |
| Decks das 108 versões, caderno | **97 das 108 fichas** (V001 a V106) | Spearman e "troca de faixa" em relação à V023, ex.: V001 0,7962 → 0,7963; V002 38,6% → 36,8%; V020 15,8% → 12,3%; V021 2,8% → 1,0% |

Regerados sem recusa de trava: o deck final da multiversão (FIN-39, FIN-40, FIN-56 e FIN-75 mudaram) e os 12 decks de indicador (só mudaram de bytes). Os decks das 24 versões, das 6 transversais e da `00_sintese` também foram regerados.
A RAIC não é afetada (congelada; o teste de números passa). O `Relatorio_IVS_Final_NB05.md` e o notebook 05 foram regerados.

---

## 4. A investigar (saíram fora da lista esperada, ou eram defeitos anteriores)

1. **`banco_de_dados/nacional/*.csv`:** ganharam linhas de dois indicadores que o código já tinha e os arquivos de 25/09 não (`pct_banheiro_comum`, `pct_so_sanitario`). Nas
   linhas antigas, **nada mudou**. Não vem da refatoração; os arquivos estavam defasados.
2. **Ruído de ponto flutuante** (≤ 1e-15): `versoes_fatorial/cargas.csv` (18–20 linhas), `estabilidade.csv`, `versoes.csv` (5 colunas) e `pares_detalhe.csv` (`d_var_2f`). Nenhuma linha passa do ruído. Provável diferença de BLAS ou de threads; o código não foi tocado.
3. **B5 e B3:** `verificar_versao.py` acusa "T19: `k_fatores = 2` não está em `T19_adequacao_fatorial.csv`". O gerador já tinha o campo desde 18/10, mas os catálogos versionados eram de antes dele, e nas outras 22 versões o "2" provavelmente
   aparece por coincidência no T19. Uma cópia do `HEAD` passa porque o catálogo antigo não tinha o campo. Correção possível: o verificador ignorar `k_fatores`, ou o T19 trazer o k.
4. **`verificar_relatorio_descritivo.py`:** sem argumento abre `dados/ultimo_gerado.pptx` (86 slides) e quebra com `IndexError` contra o manifesto (134). O manifesto e o arquivo não mudaram, então já falhava; contra os decks de 140 slides editados também não serve.
5. **`verificar_versoes_fatorial.py`:** vermelho em VP09–VP11, que é o esperado até os decks serem regerados.
6. **`Relatorio_IVS_Final_NB05.md`:** o item 6 diz "faixas indefinidas (setor no único município de sua faixa)" e agora conta também setor sem régua municipal e município com menos de 4 setores (fora: 324; graduado: 216; v00495: 324). A explicação entre parênteses ficou desatualizada.
7. **Cópias " 2" (iCloud):** a pasta do projeto fica em `Documents`, e ao regerar centenas de arquivos apareceram **437 cópias com sufixo " 2"** (já havia 98 na Fase 0). O nome é o de cópia de conflito do macOS (provavelmente a sincronização do iCloud); não verifiquei a causa. Verifiquei byte a byte: 302 eram iguais ao arquivo atual e 135 iguais à versão antiga do `HEAD`; apaguei todas. Sem apagá-las, o verificador de catálogo falha ("43 itens, 84 arquivos"). Convém excluir o projeto da sincronização do iCloud ou pausá-la ao regerar.
8. **Coluna `n` de `acrescimo_renda.csv`** ainda conta os setores com rótulo de favela, e a logística usa um setor a menos quando falta o índice (só metadado).
9. **`fig_concordancia` do `ie.main`** usa as faixas gravadas de cada especificação na amostra comum, o mesmo defeito do E2, mas só numa figura.
10. **Tempo do `ie.main`:** cerca de 6,5 min no notebook 05 com a máquina livre (o README estimava ~3 min). Não medi quanto vem do `comparar`, que agora roda 4 vezes por especificação.
11. **`./.venv/bin/jupyter` e `jupyter-execute`** têm shebang apontando para `/Users/pedro/Code/...`. Rodei com `./.venv/bin/python .venv/bin/jupyter-execute`.
12. **`README.md`, decisão 3 da tabela de pendências** ainda cita "Notebook 03", que não existe.
13. **Figuras novas F31–F35** (mapas de Spearman) apareceram em A1, A2, A3, A6 e B2: o gerador já as produzia e o `HEAD` não as tinha. Foram commitadas.

**Um deslize meu:** depois da Fase 3 não rodei a suíte logo em seguida, e `test_indice_da_referencia` estava vermelho porque o arquivo publicado da referência passou a ter 73.877 setores (sai o de São Raimundo). Atualizei o teste para dizer isso e a suíte voltou a 165 verdes.

---

## 5. Decisões para o Pedro

1. **E4 — separar a matriz da régua?** O eixo "normalização" por postos muda a matriz da fatorial e a régua ao mesmo tempo. Se a pergunta for só sobre a régua, o eixo precisaria de uma alternativa que mude uma coisa por vez. O método não foi alterado, só o texto.
2. **E6 — os números da RAIC:** nenhum dos 29 casos cobertos estava errado. Restam sem fonte simples 79,99 × 80,0, 14,9%, 52,1 milhões, as medianas de renda e as médias 3,64 e 3,14; mexer num entregável enviado é decisão sua.
3. **Regerar ou não os decks com trava** (relatório descritivo e 108 versões), ou só corrigir à mão os slides da seção 3.
4. **Tirar o projeto da sincronização do iCloud** (se for ela a causa) durante as regerações (item 7 acima).

Como revisar o ramo:

```bash
git log --oneline main..simplificacao-codigo
git diff --stat main simplificacao-codigo
```
