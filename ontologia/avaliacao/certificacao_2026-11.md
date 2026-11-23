# Certificação da ontologia — evidência (nov/2026)

Fase 3 do [`prompt_ontologia_dados_2026-11.md`](../../docs/prompts/prompt_ontologia_dados_2026-11.md). Banco:
`banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db` (gerado em 22/10/2026), aberto em modo só leitura.

**Como foi conferido.** O SQL de cada métrica foi montado do próprio YAML: `expressao` + `filtros_obrigatorios` do recorte, sem
acrescentar nada. Ele foi comparado com três referências:
1. **Recálculo:** `calcular_indicadores` e `classificar_dados_sig` aplicados às variáveis brutas `V*`, sem ler as colunas `pct_*`
   gravadas, e `renda_sem_extremos` aplicado a `V06004`.
2. **`gabarito.json`:** regerado em 22/11 por `ontologia/avaliacao/gabarito.py`. Saiu idêntico ao versionado, e o recálculo confere
   com o banco. Cobre Q02 (recorte) e Q05 (água).
3. **Tabela aprovada:** a tabela descritiva aprovada pelo Pedro em 11/10, gravada como trava em
   `scripts/pecas_relatorio_raic.py:73-81` (n e média com 3 casas; renda com 2).

Tolerância: 0 em contagens; 0,0005 em médias (a tabela aprovada é comparada ao valor arredondado para as casas dela).

## Lote 1 — métricas, recorte e tabelas

| Item | SQL (ao pé da letra) | Valor | Gabarito | Diferença | Origem no código | Veredito |
|---|---|---:|---|---:|---|---|
| `recortes.analise` | `SELECT COUNT(*) FROM setores_censitarios WHERE SITUACAO = 'Urbana' AND Dados_sig = 'OK'` | 104.108 | Q02 = 104.108; recálculo 104.108 | 0 | `indicadores.py:244`; `gerar_entrega_orientadora.py:95` | BATE |
| `n_setores_recorte` | `SELECT COUNT(CD_SETOR) … WHERE <analise>` | 104.108 | Q02 = 104.108; recálculo 104.108 | 0 | `gerar_entrega_orientadora.py:95, 153-154` | BATE |
| `media_pct_agua_inad` | `SELECT AVG(pct_agua_inad) … WHERE <analise>` | 0,069611 | Q05 = 0,0696; aprovada 0,070 (n 104.108); recálculo 0,069611 | 1e-17 | `indicadores.py:78, 87, 211` | BATE |
| `media_pct_esgoto_inad` | `SELECT AVG(pct_esgoto_inad) … WHERE <analise>` | 0,081958 | aprovada 0,082 (n 104.107); recálculo 0,081958 | 0 | `indicadores.py:79, 90, 211` | BATE |
| `media_pct_lixo_inad` | `SELECT AVG(pct_lixo_inad) … WHERE <analise>` | 0,115803 | aprovada 0,116 (n 104.108); recálculo 0,115803 | 0 | `indicadores.py:83, 93, 211` | BATE |
| `media_pct_analfab` | `SELECT AVG(pct_analfab) … WHERE <analise>` | 0,036433 | aprovada 0,036 (n 87.556); recálculo 0,036433 | 0 | `indicadores.py:99, 211` | BATE |
| `media_pct_raca_pretpardind` | `SELECT AVG(pct_raca_pretpardind) … WHERE <analise>` | 0,526744 | aprovada 0,527 (n 104.106); recálculo 0,526744 | 0 | `indicadores.py:84, 105, 211` | BATE |
| `media_razao_moradores` | `SELECT AVG(razao_moradores) … WHERE <analise>` | 2,690929 | aprovada 2,691 (n 104.108); recálculo 2,690929 | 0 | `indicadores.py:96, 211` | BATE |
| `media_renda` | `SELECT AVG(renda_media_sem_extremo) … WHERE <analise>` | 4.185,81 | aprovada 4.185,81 (n 104.095); recálculo 4.185,81 | 0 | `indicadores.py:102`; `renda.py:90, 112`; `gerar_entrega_orientadora.py:83` | BATE |
| `setores_censitarios` (granularidade "uma linha por setor") | `SELECT COUNT(*), COUNT(DISTINCT CD_SETOR)` | 109.032 / 109.032 | Q01 = 109.032 | 0 | `gerar_entrega_orientadora.py:170` | BATE |
| `dicionario_variaveis` ("uma linha por coluna de setores_censitarios") | `COUNT(*)`, `COUNT(DISTINCT coluna)`; conjunto × `PRAGMA table_info` | 108 / 108; conjuntos iguais | 108 colunas em `setores_censitarios` | 0 | `gerar_entrega_orientadora.py:171` | BATE |
| `metadados` ("uma linha por chave") | `COUNT(*)`, `COUNT(DISTINCT chave)` | 16 / 16 | — | — | `gerar_entrega_orientadora.py:138-166, 172` | BATE (chave única; sem gabarito numérico) |

`n` da tabela aprovada × `COUNT(coluna)` no recorte: todos iguais (104.108, 104.107, 104.108, 87.556, 104.106, 104.108, 104.095).

**Ressalvas da validação (`/data:validate-data`):**
- As médias são **simples entre setores**, não proporções da população. Isso já é a definição do projeto e está nas armadilhas.
- Em `media_pct_analfab`, 15,9% dos setores do recorte ficam fora do AVG por sigilo, e o sigilo não é aleatório. A armadilha entra
  pela proposta.
- O `gabarito.json` e o recálculo saem do mesmo código. A conferência independente das 6 proporções está em recalcular a partir das
  variáveis brutas, não das colunas gravadas, e na tabela aprovada em 11/10. Para a renda, coluna e recálculo usam a mesma função
  `renda_sem_extremos`; o que a confere de forma independente é a tabela aprovada.

## Lote 2 — colunas usadas pelas métricas e pelo recorte

Perfil no recorte (104.108 setores):

| Coluna | Tipo gravado | Nulos | Distintos | Mín · Máx | Evidência |
|---|---|---:|---:|---|---|
| `CD_SETOR` | text | 0 | 104.108 | 130030005000001 · 530010805440143 | chave única na base (109.032/109.032) |
| `CD_MUN` | text | 0 | 70 | 1300300 · 5300108 | 70 municípios (metadados.n_municipios = 70) |
| `SITUACAO` | text | 0 | 1 | Urbana | filtro do recorte |
| `Dados_sig` | text | 0 | 1 | OK | regra em `indicadores.py:244`; base: OK 106.281 · SIGILOSO 1.015 · ZERADO 1.736 · COLETIVO 0 |
| `V00001` | real | 0 | 678 | 5 · 1.787 | denominador domiciliar (metadados.denominador_domiciliar) |
| `CD_TIPO` | text | 0 | 10 | '0' · '9' | '0' 84.340 · '1' 19.452 · '2'–'9' 316; `CD_TIPO = 1` e `= '1'` dão o mesmo (19.452) |
| `CD_FCU` | text | 0 | 5.919 | '.' · 53001080096 | ausência = '.'; D03: 19 com código e `CD_TIPO = '0'` |
| `is_fcu` | integer | 0 | 2 | 0 · 1 | 1 = 19.452; 0 divergências com `CD_TIPO = '1'` na base; `gerar_entrega_orientadora.py:70` |
| `pct_agua_inad` | real | 0 | 11.359 | 0 · 1 | `indicadores.py:87` |
| `pct_esgoto_inad` | real | 1 | 12.052 | 0 · 1 | `indicadores.py:90`; o NULL é o setor 292740805230032 (parcelas sigilosas) |
| `pct_lixo_inad` | real | 0 | 14.286 | 0 · 1 | `indicadores.py:93` |
| `pct_analfab` | real | 16.552 | 17.572 | 0 · 0,7255 | `indicadores.py:99` (`min_count_den=2`) |
| `pct_raca_pretpardind` | real | 2 | 63.118 | 0 · 1 | `indicadores.py:105` |
| `razao_moradores` | real | 0 | 35.544 | 1 · 6,913 | `indicadores.py:96` (sem clip em [0, 1]) |
| `renda_media_sem_extremo` | real | 13 | 94.225 | 318,88 · 140.172,64 | 12 sem renda + o setor 310620005650366 excluído (`renda.py:90`) |

Descrições do YAML conferidas no banco (base inteira, salvo indicação):
- `CD_SETOR`: os 109.032 códigos têm 15 dígitos. `CD_MUN` = `substr(CD_SETOR, 1, 7)` em todos (0 divergências).
- `SITUACAO` NULL só nos 78 setores com `CD_SIT = '9'`, todos com `v0001 = 0`; Urbana = `CD_SIT` 1–3; Rural = 5–8.
- Fórmulas das 5 proporções e de `razao_moradores`: recalculadas sem corte em [0, 1], nenhum valor bruto passa de 1 no recorte
  (o corte não altera nada aqui), e `razao_moradores` bate com a fórmula com diferença 0.
- `renda_media_sem_extremo`: o setor 310620005650366 é de Belo Horizonte, `CD_TIPO = '1'`, tem 186 domicílios, 518 pessoas,
  31 analfabetos e `renda_media` = 170.418,06; a coluna sem extremo está NULL. Tudo como diz a descrição.
- **`V00001` (divergência):** a armadilha diz "pode ser NULL por sigilo (setor fica SIGILOSO)", mas a coluna é NULL nos 1.015
  SIGILOSO **e** nos 1.736 ZERADO da base. No recorte nunca é NULL.

## Decisões do Pedro

| Lote | Data | Decisão | Itens certificados | Correções (`fonte: usuario`) | Rejeitados |
|---|---|---|---|---|---|
| 1 | 23/11/2026 | aprovado ("Aprovo o lote 1") | 12: as 8 métricas, `recortes.analise`, as 3 tabelas | nenhuma | nenhum |
| 2 | 23/11/2026 | aprovado com correção ("Aprovo, com a correção") | 15: as colunas do lote 2 | `V00001`: armadilha reescrita (NULL nos SIGILOSO e nos ZERADO; nunca no recorte) → `fonte: usuario` | nenhum |

Depois do lote 2, `checar.py` dá `certificado: 27/128 itens`, sem PROBLEMA.
