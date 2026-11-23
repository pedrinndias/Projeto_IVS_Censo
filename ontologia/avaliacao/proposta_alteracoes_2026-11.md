# Proposta de alterações na ontologia — nov/2026

Fase 2 do [`prompt_ontologia_dados_2026-11.md`](../../docs/prompts/prompt_ontologia_dados_2026-11.md). Toda evidência vem de
consulta ao `.db` (aberto em modo só leitura) ou do código do projeto. A auditoria de 22/11 só indicou onde olhar.

## Fatos conferidos no banco (recorte `analise`)

| Fato | Consulta | Resultado |
|---|---|---|
| `Dados_sig` entre os urbanos | `GROUP BY Dados_sig WHERE SITUACAO='Urbana'` | OK 104.108 · SIGILOSO 766 · ZERADO 1.473 · COLETIVO 0 |
| `Dados_sig` na base | `GROUP BY Dados_sig` | OK 106.281 · SIGILOSO 1.015 · ZERADO 1.736 |
| D03: `CD_FCU` preenchido × `CD_TIPO` (recorte) | `CD_FCU <> '.'` | `CD_TIPO='0'`: 19 · `'1'`: 19.452 (base: 25 e 19.507) |
| Ausência em `CD_FCU` | `GROUP BY CD_FCU` | `'.'` em 89.500 setores; nenhum NULL |
| `is_fcu` = (`CD_TIPO = '1'`) | divergentes na base | 0 |
| D04: `metadados.valor` | `SELECT chave, valor, typeof(valor)` | tudo `text`; `n_setores = '109,032'`; `CAST('109,032' AS INTEGER) = 109` |
| D04: chave de renda | `setores_excluidos_de_renda_media_sem_extremo` | `310620005650366` (código de setor) |
| `urbano` sozinho | `metadados.n_setores_urbanos` | 106.347, não o recorte (104.108) |
| `pct_analfab` NULL no recorte | `SUM(pct_analfab IS NULL)` | 16.552 (15,9%) |

O que cada valor de `Dados_sig` significa, no código: `src/ivs_censo/indicadores.py:244-258` (`classificar_dados_sig`). ZERADO =
`v0001 = 0`; SIGILOSO = `v0001` ou `V00001` NULL; COLETIVO = `V00001 = 0` com população; OK = demais. Os indicadores só são
calculados para OK: `scripts/gerar_entrega_orientadora.py:73-78`.

## Origem de cada métrica e do recorte

| Item | Origem (`arquivo:linha`) |
|---|---|
| recorte `analise` | `indicadores.py:244` (`classificar_dados_sig`); `gerar_entrega_orientadora.py:68-69` (Dados_sig, urbano), `:95` (recorte) |
| `n_setores_recorte` | `gerar_entrega_orientadora.py:95`, `:153-154` |
| `media_pct_agua_inad` | `indicadores.py:78` (AGUA), `:87`, `:211` (`calcular_indicadores`) |
| `media_pct_esgoto_inad` | `indicadores.py:79` (ESGOTO), `:90`, `:211` |
| `media_pct_lixo_inad` | `indicadores.py:83` (LIXO), `:93`, `:211` |
| `media_pct_analfab` | `indicadores.py:99` (`min_count_den=2`), `:211` |
| `media_pct_raca_pretpardind` | `indicadores.py:84` (RACA_PPI), `:105`, `:211` |
| `media_razao_moradores` | `indicadores.py:96` (sem clip), `:211` |
| `media_renda` | `indicadores.py:102` (V06004); `renda.py:90` (`SETORES_RENDA_EXCLUIDA`), `:112`; `gerar_entrega_orientadora.py:83` |

`graphify query` não apontou o código (devolveu READMEs e relatórios); as linhas vieram de `grep` em `src/` e `scripts/`.

## Alterações propostas no YAML

1. **`CD_FCU` (D03):** `valores` com `'.'` = fora de FCU e armadilha: favela é `CD_TIPO = '1'` (`is_fcu`); 19 setores do
   recorte têm código de FCU e `CD_TIPO = '0'`; contar por `CD_FCU` dá 19.471.
2. **`metadados.valor` (D04):** armadilha sobre texto com vírgula de milhar (`CAST` direto dá 109) e sobre a chave que guarda um
   código de setor. A correção do formato fica para `scripts/gerar_entrega_orientadora.py` (fora do escopo).
3. **`referencia` com `arquivo:linha`** nas 8 métricas e no recorte (tabela acima). O campo `fonte` continua `dicionario`,
   porque a skill só aceita `dicionario | usuario | amostra`; o `arquivo:linha` vai em `referencia`.
4. **`Dados_sig`:** os quatro valores já estão em `valores`. Entra a regra, a ordem, as contagens, o aviso de que COLETIVO não
   ocorre nesta base e o de que os indicadores ficam NULL fora de OK.
5. **Descrições que o dado contradiz:**
   - `urbano` dizia "(recorte de análise do IVS)": sozinho dá 106.347; o recorte é `urbano` + `Dados_sig = 'OK'`.
   - `pct_analfab` e `media_pct_analfab`: a armadilha só citava BH; no recorte inteiro, 15,9% dos setores ficam NULL
     (87.556 com valor).

O diff completo está na parada 1 e em `certificacao_2026-11.md`.
