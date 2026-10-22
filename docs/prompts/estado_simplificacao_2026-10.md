# Estado — simplificação e correções (out/2026)

Prompt: `docs/prompts/prompt_simplificacao_correcoes_2026-10.md` · ramo `simplificacao-codigo`

## Situação: fase 1 concluída (8 erros) — próximo: fase 2 (ruff F401/F541, depois S4, S6, S9, S7, S5, S2, S3, S1, S8, varredura, `/ponytail-review`)

## Commits
| Fase | Hash | Data |
|---|---|---|
| 0 | 7fcf56a | 2026-10-22 |

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

## Regeneração (Fase 3)
| Passo | Situação | Mudou fora do esperado? |
|---|---|---|

## Achados do /ponytail-review
| Achado | Corrigido / registrado |
|---|---|

## A investigar e decisões para o Pedro
