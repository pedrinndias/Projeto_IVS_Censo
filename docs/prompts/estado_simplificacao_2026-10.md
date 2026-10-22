# Estado — simplificação e correções (out/2026)

Prompt: `docs/prompts/prompt_simplificacao_correcoes_2026-10.md` · ramo `simplificacao-codigo`

## Situação: fase 2 concluída (commit abaixo) — próximo: fase 3 (regeneração, passo 1: NB01 em background; conferir o sha256 da base bruta)

## Commits
| Fase | Hash | Data |
|---|---|---|
| 0 | 7fcf56a | 2026-10-22 |
| 1 | 537fc52 | 2026-10-22 |
| 2 | ver `git log --oneline simplificacao-codigo` (refactor: simplificação sem mudança de saída) | 2026-10-22 |

## Linha de base (Fase 0)
- 98 figuras `* 2.png` apagadas (cmp idêntico, sem citação em .json/.js/.py/.md).
- `.baseline/` (fora do git via `.git/info/exclude`): `ivs_referencia_por_setor.csv`, `ivs_proposto_por_setor.csv`, `sha256.txt`, `medidas.txt`, `provas/`.
- Antes: src 1429 · scripts .py 23007 · scripts .js 5607 · tests 1908 linhas; pytest 125 verdes; ruff F541=16 B007=13 F401=12 F841=2 B023=1 (44).
- Deleção de `relatorio_parcial_raic/Apresentacao_Oral_RAIC_2026_Pedro.pptx` mantida fora de todos os commits.

## Erros (Fase 1)
| # | Situação (corrigido / revertido / xfail) | Teste | Observação |
|---|---|---|---|
| E1 | corrigido | `test_auc_postos_e_spearman_descartam_ausentes`; `test_faixas_alternativas_aguenta_ivs_ausente` | `fa.auc_postos` e `ie.spearman` descartam pares ausentes (o `ie.spearman` já faz o que a S4 pede; mantém `np.corrcoef`); `faixas_alternativas` (quintis -1, k-médias sem ausente); `ie.main`: logística dos dois modelos na mesma amostra `okv` (o modelo só da renda foi para dentro do ramo). Sem teste unitário para o trecho da logística do `ie.main` (inline): validar na Fase 3 que `acrescimo_renda.csv` não tem `nan`. C5 rodou numa cópia: gera T36–T38 e F30 |
| E2 | corrigido | `test_comparar_nao_confunde_amostra_com_metodo` (migrou de `fm` para `ie`, ganhou `quartis`) | `ie.comparar(a, b, mun, regra)` com `spearman_mun` (usa `MIN_GRUPO`=30); `fm.comparar` removida (`PISO_MUN = ie.MIN_GRUPO`); `ie.main`, `versoes_fatorial` (`pares`, `*_v023_comum`; `FX`/`spearman` mortos removidos), `eda_versoes` (`bloco13` refaz faixas pelo valor, `sensibilidade`). A2 rodou numa cópia: T33 `Todos` 1,56% → 1,46%. **Registrado, não mexido:** `fig_concordancia` do `ie.main` ainda usa as faixas gravadas de cada especificação na amostra comum |
| E3 | corrigido | `test_replicacao_usa_a_rotacao_do_finalista`; `verificar_multiversao --fase 3` | `fm.tucker_metades` usa `pesos_de` (matriz da rotação do finalista); `tucker_F2` ausente com 1 fator. A conferência nova falha nas saídas antigas e passa depois da Fase 3 |
| E5 | corrigido | `test_bootstrap_sorteia_municipios_inteiros` (arquivo novo `tests/test_eda_transversais.py`) | `et.sortear_municipios`; textos de `textos_blocos.json` (bloco 15, `e2_pesos`, `e2_medidas`) |
| E8 | corrigido | `test_nb01_conta_municipio_faltando_como_erro` | edição cirúrgica do texto do `.ipynb` (2+/1-), sem `NotebookEdit` para não reformatar o arquivo; `erros += 1` no ramo do município faltando |
| E7 | corrigido | `tests/test_decks_caminho_obrigatorio.py` | ESTADO.md não nomeia o deck de trabalho: caminho obrigatório nos 2 `.py` (`uso:` e `SystemExit`) e `--saida` obrigatório no `.js` (sem ele recriava um "principal" fantasma e regravava hash/`ultimo_gerado.pptx`) |
| E4 | corrigido (só texto) | `verificar_multiversao --fase 4` | aviso no "Como ler" do eixo normalização (tabela e gráfico, FIN-39/40) e linha nova em "Limitações" (FIN-75); método intocado. A conferência nova falha no `FIN.json` antigo |
| E6 | corrigido (teste) | `tests/test_numeros_raic.py` (29 casos) | todos os números cobertos batem com os dados; **nenhum xfail**. Não cobertos (sem fonte simples): 79,99 × 80,0, 14,9%, 52,1 milhões, medianas 2.313,87 e 6.092,84, médias 3,64 e 3,14, 99,98, Tabela 1/Figura 1 (`pecas.json`) |

## Simplificações (Fase 2)
| # | Situação (feito / não simplificado: motivo) | Linhas a menos | Prova |
|---|---|---|---|
| lint | feito: F401/F541 (28, `ruff --fix` fora dos 4 arquivos da RAIC), F841 `nf`, B007 (10), `COLUNA_N_RESP`, `BART`/`A7` de `gerar_pdf_plano_emergencia`. Restam 4 avisos: 2 B007 de `fatorial.py` (`it` é lido depois do laço), B023 de `renda.py`, 1 F841 em arquivo congelado | ~45 | pytest; ruff 44 → 4 |
| S4 | feito: `eda_versoes.rho = ie.spearman`; `vf.spearman` removida | ~10 | `.baseline/provas/prova_s4.py`: 1.494 comparações na base real, 0 diferentes. Contrato novo: pareia por posição (docstring) |
| S6 | feito: `ie.CRIT` e `ie.cargas_rotacao`; `fm.CRIT = ie.CRIT`, `fm.elegivel` usa o helper. **`ie.elegibilidade` e `fm.elegivel` não juntadas:** as colunas dos CSVs são outras e exigiriam adaptador | ~12 | `prova_s6_s9.py`: 24 comparações, 0 diferentes |
| S9 | feito: `fm.diagnostico` devolve o MSA; a `camada1` não recalcula o KMO | 1 (e metade do KMO da camada 1) | `prova_s6_s9.py`: 28 comparações, 0 diferentes |
| S7 | feito: `relatar(gerado, editado, ident, saida)` no script do relatório; o de versões só a chama | ~55 | `prova_s7.py`: stdout e CSV iguais byte a byte nos 3 decks reais (CSVs versionados restaurados) |
| S5 | **não simplificado:** nenhuma das 8 `br` tem a semântica de `eda_versoes.br` (casas padrão 2/3/4, ausente → `—` ou `nan`; a de `gerar_pdf_guia_decks_outubro` nem tem milhar; a da RAIC fica por regra) | 0 | — |
| S2 | feito: `fontes.para_numero`, `fontes.ler_base_bruta`, `COLS_TEXTO_BASE_BRUTA` (4 cópias → 1); `preparar_base`, `auditoria_renda.carregar`, `carregar_setores_ok`, NB02 célula `step2`. `para_numero` **não** faz `astype(float64)` (as leituras da base bruta mantêm o dtype de antes; o `float64` ficou em `proporcoes_brasil`, com a nota) | ~35 | `prova_s1_s2_s3.py`: iguais (`assert_frame_equal` exato) |
| S3 | feito: `fontes.normaliza_nome`. Muda só para nome ausente (`''` no lugar de `'nan'`): 2 setores do Brasil sem `NM_MUN`; `is_elsi` igual nos 468.099 setores | ~10 | `prova_s1b.py` |
| S1 | feito: `fontes.ler_csv_ibge(caminho, usecols, tratar, chunksize, limite_chunks)` devolve (pedaços, encoding); NB01 (`ler_csv_padronizado` sem os 4 parâmetros que ninguém passava, `ler_filtrado`), NB02 `step4b`, `proporcoes_brasil.ler_arquivo_nacional` | ~70 | `prova_s1_s2_s3.py`/`prova_s1b.py`: 3 arquivos nacionais (2 chunks) + 7 `ler_filtrado` + `ler_csv_padronizado`, log igual; laço do NB02 igual |
| S8 | feito: `_desc_long` definido uma vez (`step6`), usado em `step6`, `step7`, `hab-precaria`, `banheiro-inad`, `resp-fem`, `agua-canal`; releitura de `mapa_regiao` removida da `step7`. Edição pela estrutura JSON (round-trip idêntico verificado), sem `NotebookEdit` | NB02: 961 → ~856 linhas de código | **ainda sem prova**: Fase 3, passo 2 (CSVs de `eda/` idênticos) |
| S10 | feito (ver lint) | | |
| S11 | feito na Fase 0 (98 PNG, `cmp` idêntico) | | |
| varredura | funções de corpo igual: `sid` (4 scripts, mas cada um com `ID` próprio) e `item` (2 verificadores): **registrado, não mexido**. Definições sem referência: só as 2 acima. Parâmetros opcionais que ninguém passa: afinações de algoritmos (`tol`, `maxiter`, `kappa`, `semente`) e de formato: **registrado, não mexido**. `dados_relatorio_descritivo.py` (funções a01…z02) é despachado por `globals()`: não é código morto | 2 | `.baseline/provas/varredura.py` e `params.py` |

Linhas (de `.baseline/medidas.txt`): src 1429 → 1483 (+54: os helpers novos de `fontes.py`), scripts `.py` 23007 → 22913, `.js` 5607 → 5613, tests 1908 → 2084 (+176: testes novos), código dos NB01+NB02 1250 → 1146. O ganho é de cópias, não de linhas.

## Regeneração (Fase 3)
| Passo | Situação | Mudou fora do esperado? |
|---|---|---|

## Achados do /ponytail-review
| Achado | Corrigido / registrado |
|---|---|
| 1. `comparar` usava `MIN_GRUPO` (significado do AUC) como piso de setores por município | corrigido: `ie.PISO_MUN`, `fm.PISO_MUN = ie.PISO_MUN` |
| 2. helpers novos de `fontes.py` sem teste no repositório | corrigido: 3 testes em `tests/test_ivs_censo.py` (latin1, pedaços com filtro e limite, `para_numero`, `normaliza_nome`) |
| 3. `ie.spearman` pareia por posição; o `rho` antigo alinhava por índice | corrigido: docstring. Os chamadores atuais conferidos um a um (mesmo DataFrame, ou `reindex` na mesma ordem) |
| 4. `test_numeros_raic` quebrava a coleta se faltasse um CSV | corrigido: `CASOS = []` e o teste é pulado |
| 5. `acrescimo_renda.csv` coluna `n` conta `ok`, e a logística usa `okv` (1 setor a menos quando falta o índice) | registrado (só metadado) |
| 6. `ie.main` chama `comparar` uma vez por regra e recalcula o Spearman duas vezes por amostra | registrado; medir o tempo na Fase 3 |
| 7. `fig_concordancia` do `ie.main` ainda usa as faixas gravadas de cada especificação | registrado (E2, só figura) |

## A investigar e decisões para o Pedro
