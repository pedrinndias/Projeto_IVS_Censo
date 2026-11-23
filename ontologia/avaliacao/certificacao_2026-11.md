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

## Lotes 3 em diante — evidência comum (23/11)

Script no scratchpad (`evid_lotes3.py`). Ele compara a descrição do YAML com a tabela `dicionario_variaveis` do banco e com os
dicionários oficiais do IBGE versionados em `dados/` (lidos por `carregar_dicionario_oficial`,
`src/ivs_censo/dicionario.py:60`), perfila cada coluna no recorte e recalcula as fórmulas com `calcular_indicadores`.

- 101 itens não certificados: 93 colunas de `setores_censitarios`, 6 de `dicionario_variaveis` e 2 de `metadados`.
- Das 93: 92 descrições iguais às do dicionário do banco. A exceção é `urbano`, corrigida na parada 1.
- As 62 colunas `V*`/`v*` têm descrição **idêntica** à do dicionário oficial do IBGE (62/62).
- 22 colunas com fórmula, recalculadas no recorte a partir das variáveis brutas: diferença máxima 0. Fórmula do YAML igual à do
  dicionário do banco em todas as calculadas.
- Nenhuma coluna numérica tem valor negativo no recorte.

**Achado: armadilha das `pct_*` incompleta.** O texto dizia "NULL quando o denominador é zero ou sigiloso". No recorte, **todos**
os NULL dessas 22 colunas vêm do numerador inteiro sigiloso, e nenhum vem do denominador. Com uma variável só no numerador, basta
ela ser sigilosa. Contagem por coluna: `pct_agua_so_terreno` 15.897, `pct_casa_vila_condominio` 12.804, `pct_sem_banheiro`
12.196, `pct_agua_nao_encanada` 9.706, `pct_banheiro_comum` 9.694, `pct_apartamento` 9.103, `pct_dom_improv` 5.139,
`pct_casa` 4.466, `pct_so_sanitario` 3.811, `pct_sem_banheiro_nem_sanitario` 2.969, `pct_crianca_0a4` 1.820,
`pct_idoso_60mais` 285, `pct_pop_0a14` 258, `pct_resp_feminino` 147, `pct_sem_agua_canalizada` 41, `pct_raca_pretpardind` 2,
`pct_esgoto_inad` 1; as demais, 0. Isso confere com `calcular_indicadores` (`indicadores.py:211`): o numerador soma com
`min_count=1`, então fica NaN só quando todas as parcelas são NaN.

### Lote 3 — 15 proporções complementares

Fórmula = dicionário do banco; recálculo com diferença 0; variáveis conferidas no dicionário oficial do IBGE.

| Coluna | Fórmula | NULL no recorte | Leitura das variáveis no IBGE |
|---|---|---:|---|
| `pct_dom_improv` | V00002 / (V00001 + V00002) | 5.139 | improvisados / (permanentes + improvisados) |
| `pct_hab_precaria` | (V00050 + V00052 + V00053…V00058) / (V00001 + V00002) | 0 | cortiço, estrutura degradada e os 6 tipos de improvisado |
| `pct_moradia_convencional` | (V00047 + V00048 + V00049) / V00001 | 0 | casa, casa de vila/condomínio, apartamento |
| `pct_moradia_nao_convencional` | (V00050 + V00051 + V00052) / V00001 | 0 | cortiço, habitação indígena sem paredes, estrutura degradada |
| `pct_apartamento` | V00049 / V00001 | 9.103 | apartamento |
| `pct_casa` | V00047 / V00001 | 4.466 | casa |
| `pct_casa_vila_condominio` | V00048 / V00001 | 12.804 | casa de vila ou em condomínio |
| `pct_sem_agua_canalizada` | 1 − V00199 / V00001 | 41 | complemento de "água encanada até dentro" |
| `pct_agua_nao_encanada` | V00201 / V00001 | 9.706 | água não chega encanada |
| `pct_agua_so_terreno` | V00200 / V00001 | 15.897 | encanada só até o terreno |
| `pct_sem_banheiro` | V00495 / V00001 | 12.196 | sem banheiro exclusivo com chuveiro e vaso |
| `pct_sem_banheiro_nem_sanitario` | V00238 / V00001 | 2.969 | nem banheiro nem sanitário |
| `pct_so_sanitario` | V00237 / V00001 | 3.811 | só sanitário ou buraco |
| `pct_banheiro_comum` | V00236 / V00001 | 9.694 | só banheiro de uso comum |
| `pct_resp_feminino` | V01063 / (V01062 + V01063) | 147 | responsável mulher / responsáveis |

## Decisões do Pedro

| Lote | Data | Decisão | Itens certificados | Correções (`fonte: usuario`) | Rejeitados |
|---|---|---|---|---|---|
| 1 | 23/11/2026 | aprovado ("Aprovo o lote 1") | 12: as 8 métricas, `recortes.analise`, as 3 tabelas | nenhuma | nenhum |
| 2 | 23/11/2026 | aprovado com correção ("Aprovo, com a correção") | 15: as colunas do lote 2 | `V00001`: armadilha reescrita (NULL nos SIGILOSO e nos ZERADO; nunca no recorte) → `fonte: usuario` | nenhum |
| 3–10 | 23/11/2026 | aprovado em bloco ("Siga todos os lotes de forma automática…") | 101: lotes 3 a 10 | 40 correções (ver abaixo) | nenhum |

Depois do lote 2, `checar.py` dava `certificado: 27/128 itens`; depois dos lotes 3 a 10, **128/128**, sem PROBLEMA.

## Lotes 3 a 10 — aprovação em bloco (23/11/2026)

**Decisão do Pedro:** "Siga todos os lotes de forma automática e vá fazendo as correções e documentando tudo". Os lotes 3 a 10
foram certificados sem revisão item a item. Cada correção abaixo tem evidência do banco ou do código. Os itens corrigidos ficaram
com `fonte: usuario`, e a `referencia` registra a fonte original e que a correção foi aprovada em bloco. Script:
`lotes3a10.py` (scratchpad); log: `log_lotes3a10.json`.

Conferências comuns a todos os itens: descrição do YAML × `dicionario_variaveis` (92/93 iguais; `urbano` foi corrigido antes
de propósito) × dicionário oficial do IBGE (62/62 `V*` idênticas); perfil no recorte; recálculo das 22 fórmulas (diferença 0).
Depois de tudo: `checar.py` → **128/128**, sem PROBLEMA; `gabarito.py` confere com o banco e o `gabarito.json` não mudou;
as 8 métricas e o recorte continuam BATENDO com o SQL ao pé da letra.

### Correções feitas (40)

| Item | Campo | Motivo (evidência) |
|---|---|---|
| `setores_censitarios.pct_agua_inad` | armadilhas | no recorte, os 0 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_esgoto_inad` | armadilhas | no recorte, os 1 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_lixo_inad` | armadilhas | no recorte, os 0 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_raca_pretpardind` | armadilhas | no recorte, os 2 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_dom_improv` | armadilhas | no recorte, os 5.139 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_hab_precaria` | armadilhas | no recorte, os 0 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_moradia_convencional` | armadilhas | no recorte, os 0 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_moradia_nao_convencional` | armadilhas | no recorte, os 0 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_apartamento` | armadilhas | no recorte, os 9.103 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_casa` | armadilhas | no recorte, os 4.466 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_casa_vila_condominio` | armadilhas | no recorte, os 12.804 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_sem_agua_canalizada` | armadilhas | no recorte, os 41 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_agua_nao_encanada` | armadilhas | no recorte, os 9.706 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_agua_so_terreno` | armadilhas | no recorte, os 15.897 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_sem_banheiro` | armadilhas | no recorte, os 12.196 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_sem_banheiro_nem_sanitario` | armadilhas | no recorte, os 2.969 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_so_sanitario` | armadilhas | no recorte, os 3.811 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_banheiro_comum` | armadilhas | no recorte, os 9.694 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_resp_feminino` | armadilhas | no recorte, os 147 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_crianca_0a4` | armadilhas | no recorte, os 1.820 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_pop_0a14` | armadilhas | no recorte, os 258 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `setores_censitarios.pct_idoso_60mais` | armadilhas | no recorte, os 285 NULL vêm todos do numerador inteiro sigiloso; nenhum do denominador |
| `metricas.media_pct_agua_inad` | armadilhas | armadilha não dizia que numerador todo sigiloso deixa o setor NULL |
| `metricas.media_pct_esgoto_inad` | armadilhas | armadilha não dizia que numerador todo sigiloso deixa o setor NULL |
| `metricas.media_pct_lixo_inad` | armadilhas | armadilha não dizia que numerador todo sigiloso deixa o setor NULL |
| `setores_censitarios.prop_70mais_entre_60mais` | descricao, armadilhas | descrição dizia 'proporção', mas o valor vai de 0 a 100 (escala 100 em indicadores.py); NULL tem duas causas |
| `setores_censitarios.iep_setor` | armadilhas | faltava avisar a escala sem corte e as causas do NULL |
| `setores_censitarios.rdi_setor` | armadilhas | faltava avisar a escala sem corte e as causas do NULL |
| `setores_censitarios.renda_media` | armadilhas | faltava a contagem de NULL no recorte |
| `setores_censitarios.renda_media_mediana_mun` | armadilhas, referencia | faltava dizer que só um setor muda e qual valor recebe (conferido: mediana de BH sem o extremo) |
| `setores_censitarios.NM_BAIRRO` | armadilhas | NULL frequente e concentrado por município, sem aviso |
| `setores_censitarios.NM_FCU` | armadilhas | mesma armadilha do D03, vista pelo nome |
| `setores_censitarios.Moradia_Predominante` | descricao, valores | faltavam os valores; no recorte coincide com o maior entre V00047..V00052 em 104.108 de 104.108 setores |
| `setores_censitarios.Moradia_Predominante_Agrupada` | valores, referencia | valores eram uma lista sem o que cada grupo reúne |
| `setores_censitarios.V00005` | unidade | conta moradores, não domicílios (V00005/V00001 dá 2,69 moradores por domicílio no recorte) |
| `setores_censitarios.V00006` | unidade | conta moradores, não domicílios (V00005/V00001 dá 2,69 moradores por domicílio no recorte) |
| `dicionario_variaveis.tema` | descricao | descrição listava 5 temas; o banco tem 12 |
| `dicionario_variaveis.origem` | descricao, valores | descrição citava 2 origens; o banco tem 3 |
| `dicionario_variaveis.arquivo_fonte` | descricao | descrição omitia o valor '(derivado)' |
| `dicionario_variaveis.formula` | descricao | faltava dizer quando é preenchida (conferido) |

Texto novo de cada correção: ver `ontologia/ontologia.yaml` (o diff do commit mostra antes e depois).

### Itens por lote

- **Lote 3** (15, proporções complementares): `pct_dom_improv`, `pct_hab_precaria`, `pct_moradia_convencional`, `pct_moradia_nao_convencional`, `pct_apartamento`, `pct_casa`, `pct_casa_vila_condominio`, `pct_sem_agua_canalizada`, `pct_agua_nao_encanada`, `pct_agua_so_terreno`, `pct_sem_banheiro`, `pct_sem_banheiro_nem_sanitario`, `pct_so_sanitario`, `pct_banheiro_comum`, `pct_resp_feminino`
- **Lote 4** (15, calculadas de idade, renda e identificação): `pct_crianca_0a4`, `pct_pop_0a14`, `pct_idoso_60mais`, `iep_setor`, `rdi_setor`, `prop_70mais_entre_60mais`, `renda_media`, `renda_media_mediana_mun`, `CD_UF`, `CD_SIT`, `NM_MUN`, `NM_BAIRRO`, `NM_FCU`, `urbano`, `Moradia_Predominante`
- **Lote 5** (15, Moradia_Predominante_Agrupada e V* (1/5)): `Moradia_Predominante_Agrupada`, `v0001`, `V00002`, `V00005`, `V00006`, `V00047`, `V00048`, `V00049`, `V00050`, `V00051`, `V00052`, `V00053`, `V00054`, `V00055`, `V00056`
- **Lote 6** (15, V* (2/5)): `V00057`, `V00058`, `V00112`, `V00113`, `V00114`, `V00115`, `V00116`, `V00117`, `V00118`, `V00199`, `V00200`, `V00201`, `V00236`, `V00237`, `V00238`
- **Lote 7** (15, V* (3/5)): `V00312`, `V00313`, `V00314`, `V00315`, `V00316`, `V00398`, `V00399`, `V00400`, `V00401`, `V00402`, `V00495`, `V00900`, `V00901`, `V01318`, `V01320`
- **Lote 8** (15, V* (4/5)): `V01321`, `V06001`, `V06004`, `V06005`, `V01031`, `V01032`, `V01033`, `V01034`, `V01035`, `V01036`, `V01037`, `V01038`, `V01039`, `V01040`, `V01041`
- **Lote 9** (3, V* (5/5)): `V01042`, `V01062`, `V01063`
- **Lote 10** (8, tabelas auxiliares): `dicionario_variaveis.coluna`, `dicionario_variaveis.descricao`, `dicionario_variaveis.tema`, `dicionario_variaveis.origem`, `dicionario_variaveis.arquivo_fonte`, `dicionario_variaveis.formula`, `metadados.chave`, `metadados.valor`

### Perfil no recorte das colunas dos lotes 4 a 9

| Coluna | Unidade | NULL | Mín | Máx | Corrigida? |
|---|---|---:|---:|---:|---|
| `pct_crianca_0a4` | proporção | 1.820 | 0 | 0,33 | sim |
| `pct_pop_0a14` | proporção | 258 | 0 | 0,49 | sim |
| `pct_idoso_60mais` | proporção | 285 | 0 | 0,86 | sim |
| `iep_setor` | índice ×100 | 992 | 0 | 4.750 | sim |
| `rdi_setor` | índice ×100 | 298 | 0 | 1.000 | sim |
| `prop_70mais_entre_60mais` | índice ×100 | 2.136 | 0 | 100 | sim |
| `renda_media` | BRL | 12 | 318,88 | 170.418,06 | sim |
| `renda_media_mediana_mun` | BRL | 12 | 318,88 | 140.172,64 | sim |
| `CD_UF` | — | 0 | 13 | 53 |  |
| `CD_SIT` | — | 0 | 1 | 3 |  |
| `NM_MUN` | — | 0 | Ananindeua | Água Preta |  |
| `NM_BAIRRO` | — | 41.431 | 35º BI | Átila de Paiva | sim |
| `NM_FCU` | — | 84.637 | 12 de Outubro | Índio Peri | sim |
| `urbano` | — | 0 | 1 | 1 |  |
| `Moradia_Predominante` | — | 0 | Apartamento | Estrutura Degradada/Inacabada | sim |
| `Moradia_Predominante_Agrupada` | — | 0 | Convencional | Não convencional | sim |
| `v0001` | pessoas | 0 | 6 | 4.703 |  |
| `V00002` | domicílios | 5.139 | 0 | 340 |  |
| `V00005` | pessoas | 0 | 6 | 4.703 | sim |
| `V00006` | pessoas | 3.240 | 0 | 891 | sim |
| `V00047` | domicílios | 4.466 | 0 | 973 |  |
| `V00048` | domicílios | 12.804 | 0 | 595 |  |
| `V00049` | domicílios | 9.103 | 0 | 1.425 |  |
| `V00050` | domicílios | 7.360 | 0 | 277 |  |
| `V00051` | domicílios | 4 | 0 | 0 |  |
| `V00052` | domicílios | 1.781 | 0 | 156 |  |
| `V00053` | domicílios | 1.263 | 0 | 196 |  |
| `V00054` | domicílios | 2.699 | 0 | 58 |  |
| `V00055` | domicílios | 843 | 0 | 324 |  |
| `V00056` | domicílios | 405 | 0 | 143 |  |
| `V00057` | domicílios | 619 | 0 | 255 |  |
| `V00058` | domicílios | 95 | 0 | 10 |  |
| `V00112` | domicílios | 10.221 | 0 | 669 |  |
| `V00113` | domicílios | 7.577 | 0 | 364 |  |
| `V00114` | domicílios | 3.072 | 0 | 467 |  |
| `V00115` | domicílios | 2.527 | 0 | 322 |  |
| `V00116` | domicílios | 1.920 | 0 | 74 |  |
| `V00117` | domicílios | 1.435 | 0 | 207 |  |
| `V00118` | domicílios | 11.816 | 0 | 349 |  |
| `V00199` | domicílios | 41 | 0 | 1.787 |  |
| `V00200` | domicílios | 15.897 | 0 | 905 |  |
| `V00201` | domicílios | 9.706 | 0 | 482 |  |
| `V00236` | domicílios | 9.694 | 0 | 263 |  |
| `V00237` | domicílios | 3.811 | 0 | 142 |  |
| `V00238` | domicílios | 2.969 | 0 | 117 |  |
| `V00312` | domicílios | 10.163 | 0 | 642 |  |
| `V00313` | domicílios | 7.142 | 0 | 647 |  |
| `V00314` | domicílios | 7.099 | 0 | 474 |  |
| `V00315` | domicílios | 10.135 | 0 | 413 |  |
| `V00316` | domicílios | 2.969 | 0 | 117 |  |
| `V00398` | domicílios | 17.909 | 0 | 929 |  |
| `V00399` | domicílios | 3.813 | 0 | 182 |  |
| `V00400` | domicílios | 940 | 0 | 92 |  |
| `V00401` | domicílios | 4.657 | 0 | 339 |  |
| `V00402` | domicílios | 4.824 | 0 | 266 |  |
| `V00495` | domicílios | 12.196 | 0 | 263 |  |
| `V00900` | pessoas | 0 | 3 | 3.382 |  |
| `V00901` | pessoas | 16.552 | 0 | 302 |  |
| `V01318` | pessoas | 1.903 | 0 | 941 |  |
| `V01320` | pessoas | 94 | 0 | 2.419 |  |
| `V01321` | pessoas | 22.423 | 0 | 551 |  |
| `V06001` | pessoas | 7 | 5 | 1.787 |  |
| `V06004` | BRL | 12 | 318,88 | 170.418,06 |  |
| `V06005` | BRL² | 19 | 6,86 | 922.591.172.683,59 |  |
| `V01031` | pessoas | 1.820 | 0 | 375 |  |
| `V01032` | pessoas | 1.579 | 0 | 692 |  |
| `V01033` | pessoas | 1.547 | 0 | 483 |  |
| `V01034` | pessoas | 1.233 | 0 | 800 |  |
| `V01035` | pessoas | 728 | 0 | 554 |  |
| `V01036` | pessoas | 646 | 0 | 579 |  |
| `V01037` | pessoas | 170 | 0 | 1.265 |  |
| `V01038` | pessoas | 197 | 0 | 810 |  |
| `V01039` | pessoas | 290 | 0 | 417 |  |
| `V01040` | pessoas | 657 | 0 | 281 |  |
| `V01041` | pessoas | 1.890 | 0 | 300 |  |
| `V01042` | pessoas | 0 | 5 | 1.787 |  |
| `V01062` | pessoas | 77 | 0 | 845 |  |
| `V01063` | pessoas | 147 | 0 | 1.253 |  |

Contagens `V*` são todas inteiras e não negativas no recorte. As exceções esperadas são `V06004` (média) e `V06005` (variância).

### O que fica para você revisar

- As 40 correções acima, em especial a mudança de `fonte` para `usuario` (mesmo critério do `V00001`).
- As armadilhas das 3 métricas de saneamento já certificadas no lote 1 foram reescritas (numerador todo sigiloso → NULL).
- `Moradia_Predominante`: a descrição diz que é a maior contagem entre V00047 e V00052. Bate em 104.108/104.108 setores do
  recorte, mas a regra de desempate do Notebook 01 não foi lida.
