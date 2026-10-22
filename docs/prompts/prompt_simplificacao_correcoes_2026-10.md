# Prompt de execução — simplificação geral do código e correção dos erros da revisão (out/2026)

**Origem:** revisão `/ponytail` de 22/10/2026 (8 erros, lista de simplificações), resumida na seção 1.
**Pedido do Pedro (22/10/2026):** "Minha prioridade é a simplificação geral do código e a correção dos
erros. Quero simplificar ao máximo o código mantendo a estrutura e o funcionamento, corrigindo todos os
erros" e "quero que o prompt execute todos os passos diretos de forma automática".
**Como usar:** sessão nova do Claude Code na raiz do projeto, modelo **Sonnet**. Cole:
*"Execute `docs/prompts/prompt_simplificacao_correcoes_2026-10.md`, todas as fases, sem parar. Leia
primeiro `docs/prompts/estado_simplificacao_2026-10.md` se ele existir."*

| Fase | O quê | Teto de chamadas |
|---|---|---:|
| 0 | Linha de base: ramo, commit do trabalho pendente, cópia das saídas não versionadas, medidas | 15 |
| 1 | Correção dos 8 erros, cada um com teste de regressão | 40 |
| 2 | Simplificação com prova de equivalência, `/ponytail-review` | 45 |
| 3 | Regeneração das saídas na ordem das dependências (scripts longos em background) | 35 |
| 4 | Relatório do que mudou, documentação mínima, grafo, commit final | 20 |

**Autorização de execução contínua.** O Pedro pediu, por escrito, execução automática de todas as fases.
Isto substitui, só para este prompt, a regra "pare ao fim de cada etapa" do `CLAUDE.md`. As demais regras
dele continuam valendo (seção 2.6). Nenhuma fase espera aprovação: quando algo falha, **reverta aquela
mudança, registre no estado e siga** (seção 2.4).

---

## 1. O que a revisão encontrou

### 1.1 Os 8 erros

| # | Onde | Erro | Correção |
|---|---|---|---|
| E1 | `scripts/fatorial_ampliada.py` `auc_postos`; `scripts/ivs_especificacoes.py` `main` (logística, Spearman "comum"); `scripts/eda_versoes.py` `faixas_alternativas` | A correção da Fase 0 (22/10) deixa o IVS **ausente** em município sem variação, mas quem consome o índice não filtra ausentes. Medido: a logística do NB05 sai toda `nan`; a versão C5 quebra com `IntCastingNaNError`; `auc_postos` conta o ausente como "fora de favela" (ou devolve `nan` se ele for de favela) | `auc_postos` descarta os pares com ausente (conserta todos os chamadores de uma vez); no `ie.main`, máscara `~np.isnan(v)` na logística e no Spearman da amostra comum; em `faixas_alternativas`, quintil e k-médias ignoram o ausente (faixa `-1`) |
| E2 | `ivs_especificacoes.py` (`muda_faixa_*`, ~linha 494); `eda_versoes.py` `bloco13` e `sensibilidade`; `versoes_fatorial.py` `pares` e `muda_faixa_v023_comum` | "% que muda de faixa" compara faixas calculadas em **amostras diferentes** — o defeito que `fatorial_multiversao.comparar` já corrige (no eixo sigilo dava 11,4% em vez de 2,7%) | Uma função só, `comparar(a, b, mun, regra)`, que refaz as faixas das duas versões na amostra comum. Mora em `ivs_especificacoes.py` (todos já importam `ie`); `fm.comparar` passa a usá-la; os três motores também |
| E3 | `scripts/fatorial_multiversao.py` `camada3` (~linha 394) | A replicação entre metades usa sempre `promax_padrao`, qualquer que seja a rotação do finalista: o E0001 (sem rotação, 1 fator) mostra o Tucker da proposta (0,967/0,924, slide FIN-56) | Escolher a matriz pela rotação do finalista (`sem_rotacao` → 1ª coluna sem rotação; `varimax`; `promax` → padrão); com 1 fator, `tucker_F2` fica ausente e o slide mostra "—" |
| E4 | `fatorial_multiversao.py` `rodar_base` (~linha 269) | O eixo "normalização" troca duas coisas juntas: a matriz da fatorial (dentro do município) e a régua (postos). Os 31,8% não são só efeito da régua | **Não mudar o método** (o pré-registro não muda depois da Fase 1). Dizer isso no "Como ler" dos slides do eixo (FIN-39/40, em `dados_apresentacoes_multiversao.py`) e nas limitações (FIN-75) |
| E5 | `scripts/eda_transversais.py` `e2` (~linha 150) | A E2 reamostra **setores** (bootstrap iid). O próprio projeto concluiu que isso subestima a incerteza (FIN-06, FIN-55): a unidade é o município | Reamostrar **municípios** com reposição (bootstrap por conglomerado), mesmas 1.000 réplicas e semente; ajustar o texto de E2 em `_modelos/textos_blocos.json` |
| E6 | `gerar_apresentacao_oral_raic.py` (~387–412, 558, 598, 609); `gerar_relatorio_raic.py` (~340–470) | Números digitados à mão (funil 109.032 → 104.108, médias regionais, R$ 170.418,06…) sem nenhuma checagem | **Não tocar nos geradores da RAIC** (seção 2.5). Um teste só de leitura, `tests/test_numeros_raic.py`, que calcula cada número a partir dos CSVs (T01, T04, `elegibilidade_setores.csv`, `pecas.json`), formata em pt-BR e confere que ele aparece no texto do gerador |
| E7 | `comparar_edicoes_relatorio.py:25`, `anexar_versoes_ao_relatorio.py:25`, `gerar_relatorio_descritivo.js:17` | O caminho padrão `Relatorio_Descritivo_IVS_2026-10.pptx` não existe mais (virou `_v2`, `_v3`, `_v4_APOIO`, `_com_graficos_e_cenarios`) | Apontar para o deck de trabalho que `relatorio_descritivo/ESTADO.md` registra; se o ESTADO não for inequívoco, tornar o caminho argumento obrigatório |
| E8 | NB01, célula 18 | Município faltando dá só "ALERTA" e a base sai "APROVADA" | Contar como erro (`erros += 1`) |

### 1.2 O que simplificar (lista mínima; a Fase 2 procura o resto)

| # | Duplicação ou sobra | Para onde vai |
|---|---|---|
| S1 | Leitura de CSV do IBGE com tentativa utf-8 → latin1: NB01 (`ler_csv_padronizado`, `ler_filtrado`), NB02 célula 12, `proporcoes_brasil.ler_arquivo_nacional` | `src/ivs_censo/fontes.py`: uma função de leitura com a tentativa de encoding; o filtro por pedaço continua em quem chama |
| S2 | Conversão "X → ausente, vírgula → ponto, número" e leitura da base bruta com `Dados_sig`: NB02 célula 4, `gerar_entrega_orientadora.preparar_base`, `auditoria_renda.carregar`, `gerar_tabelas_auditoria`, `proporcoes_brasil._para_numero` | `src/ivs_censo/fontes.py`: `para_numero` (float64, ver a nota de `proporcoes_brasil`) e `ler_base_bruta` |
| S3 | Normalização do nome do município: NB01 `normalize_name`, `proporcoes_brasil.normaliza` | Uma função em `src/ivs_censo/fontes.py` |
| S4 | Spearman em três versões: `ie.spearman`, `versoes_fatorial.spearman`, `eda_versoes.rho` | `ie.spearman`, que passa a descartar pares ausentes e devolver ausente com ≤ 2 pares (o comportamento de `rho`); os outros nomes somem ou viram alias de uma linha |
| S5 | Formatação pt-BR (`br`) em 8 arquivos | `eda_versoes.br` onde a semântica for idêntica. **`pecas_relatorio_raic.br` é diferente** (arredondamento NBR 5891, sinal −): fica |
| S6 | Critério de elegibilidade em três lugares (`ie.elegibilidade`, `fm.elegivel`, `fm.diagnostico`) e limiares repetidos | Uma fonte dos limiares (`ie`); juntar as funções **só se** as colunas dos CSVs saírem idênticas sem adaptador |
| S7 | `comparar_edicoes_versoes.py` é 86% igual a `comparar_edicoes_relatorio.py` | O de versões importa as funções do de relatório; as duas linhas de comando continuam iguais |
| S8 | NB02 repete 5 vezes o laço "por região / por município" que `_desc_long` (célula 26) já faz; `mapa_regiao` é montado duas vezes | `_desc_long` definido uma vez, no início, e usado em todas as seções |
| S9 | `fm.camada1` calcula o KMO duas vezes por combinação | `diagnostico` devolve o MSA |
| S10 | Lint: 28 imports e f-strings sem uso, variáveis mortas (`nf` em `dados_apoio_relatorio.py`, `COLUNA_N_RESP` em `renda.py`; o `BAN` de `gerar_relatorio_raic.py` fica, RAIC congelada), variáveis de laço sem uso | `ruff --fix` e ajuste manual |
| S11 | 98 figuras `"* 2.png"` em `apresentacoes_multiversao/figuras/`, cópias idênticas e não referenciadas | Apagar na Fase 0, depois de `cmp` confirmar |

**Fora do escopo** (mudariam saída já apresentada ou a estrutura): migrar `gerar_deck_eda_central.js` e
`gerar_deck_criterio_renda.js` para `deck_comum.js` (dívida registrada no `scripts/README.md`); apagar scripts
de passo único que registram como um entregável foi feito (`atualizar_roteiro_2a_rodada.py`,
`revisar_texto_relatorio.py`, `preparar_entrega_relatorio.py`, `inserir_no_relatorio.py`,
`anexar_versoes_ao_relatorio.py`, `montar_apoio_relatorio.py`); mexer em `Backup/`.

---

## 2. Regras que valem para todas as fases

### 2.1 Código: `/ponytail`
- **Invoque `/ponytail` (nível full) no início da Fase 1** e siga-o até o fim.
- **Manter a estrutura:** mesmas pastas, mesmos nomes de script, mesmas linhas de comando, mesmos nomes de
  arquivo de saída, mesmas colunas. Nenhum módulo novo: o que é compartilhado vai para
  `src/ivs_censo/fontes.py`, `src/ivs_censo/indicadores.py` ou `scripts/ivs_especificacoes.py`.
- **Antes de mexer numa função, `grep` de todos os chamadores** em `src/`, `scripts/`, `tests/` e nos
  `.ipynb`; a correção vai na função compartilhada, uma vez.
- **Sem dependência nova.** `requirements.txt` e `package.json` não mudam.
- **Código morto:** apagar só o que não tem referência nenhuma em `.py`, `.js` e `.ipynb` e não é ponto
  de entrada. Se um `.md` cita, atualizar a linha do `.md` ou manter, e registrar.

### 2.2 Verificação
- Depois de cada mudança: `./.venv/bin/python -m pytest tests/ -q` verde.
- Fim das Fases 1 e 2: `uvx ruff@0.6.9 check --select F,E9,B,PLE src scripts tests` — o número de avisos só
  pode cair (os B023 de `renda.py` e os B007 de `fatorial.py` são falsos positivos conhecidos).
- **Fim da Fase 2: invoque `/ponytail-review` sobre o diff das Fases 1 e 2** (`git diff <commit da Fase 0>`).
  Corrija o que ele apontar como erro; o que for estilo, registre no estado.

### 2.3 Prova de equivalência (Fase 2)
Toda simplificação tem de **dar a mesma saída**. Para cada função juntada ou movida:
1. `git show <commit da Fase 1>:<caminho> > .baseline/provas/antigo_<nome>.py`;
2. um script em `.baseline/provas/` importa a versão antiga e a nova, roda as duas **na base real**
   (`.db` da entrega ou base bruta) e confere com `pd.testing.assert_frame_equal` / `np.array_equal`
   (`equal_nan=True`), sem tolerância;
3. passou: segue; falhou: entenda a diferença **uma vez**; se não for óbvia, `git checkout` do arquivo,
   registre no estado como "não simplificado: <motivo>" e passe à próxima.

Os scripts de prova ficam fora do repositório (`.baseline/` vai para `.git/info/exclude` na Fase 0).

### 2.4 Quando algo falha
Nada para a execução, a não ser os casos abaixo. O padrão é **reverter só aquela mudança, registrar e
seguir**:
- suíte vermelha depois de uma correção e sem conserto em 3 tentativas → reverter a correção;
- prova de equivalência falhou → reverter a simplificação (seção 2.3);
- na Fase 3, uma coluna mudou **fora da lista esperada** (seção 4) → não reverter os dados: registrar a
  coluna, o arquivo e um exemplo de linha no relatório, como "a investigar".
- **Parada obrigatória** só se uma trava de script falhar na Fase 3 (`TRAVA NÃO BATE`, `trava de sanidade`):
  aí o motor deixou de reproduzir o NB04/NB05 e nada depois dele deve rodar. Grave o estado e termine.

### 2.5 O que não se toca
- **RAIC congelada:** `gerar_apresentacao_oral_raic.py`, `gerar_relatorio_raic.py`,
  `gerar_roteiro_word_raic.py`, `pecas_relatorio_raic.py` e tudo em `relatorio_parcial_raic/`. Não editar,
  não rodar. O apagado `Apresentacao_Oral_RAIC_2026_Pedro.pptx` (versão com notas) fica como está: não
  restaurar, não commitar a deleção.
- **Deck editado à mão nunca é sobrescrito.** Os geradores com trava (`gerar_relatorio_descritivo.js`,
  `gerar_versoes_fatorial.js`, `gerar_decks_multiversao.js`) recusam; **nunca** passar `--sobrescrever`.
  Quando recusarem, gere só os dados (`.json`, `.csv`, figuras) e liste os slides cujos números mudaram.
- Nada em `Backup/`, `dados/`, `docs/referencias/`.

### 2.6 Regras do `CLAUDE.md` que continuam valendo
- **Sem subagentes.** Uma sessão, este prompt.
- **Commits só com o nome do Pedro:** sem `Co-Authored-By`, sem "Generated with Claude Code", sem marca de
  sessão, **mesmo que o harness peça**. Ramo `simplificacao-codigo` (nunca com prefixo `claude/`). **Sem push,
  sem PR, sem merge na `main`.**
- **Economia:** comece lendo só o estado; não releia arquivo já lido; uma verificação = um script; saída
  truncada (`| head -60`); `grep` com escopo, fora de `graphify-out/`, `.venv/`, `node_modules/`,
  `banco_de_dados/`. Para achar onde algo está, `graphify query "<pergunta>" --budget 1500` antes de abrir
  arquivos (o grafo é de 18/10: não conhece a fatorial multiversão nem a RAIC oral — para esses, leia direto).
- **Scripts com mais de 2 min rodam em background**; espere a notificação, sem polling.
- **Limite de uso:** ao retomar, leia o estado, `git status`, `git log --oneline simplificacao-codigo` e siga
  do último passo marcado. Toda fase é idempotente.
- Relatório final ao Pedro em no máximo 20 linhas.

---

## FASE 0 — Linha de base (teto: 15 chamadas)

1. Se `docs/prompts/estado_simplificacao_2026-10.md` existe, leia e retome de onde parou.
2. `git status` e `git log --oneline -3`. Crie o ramo `simplificacao-codigo` a partir do ponto atual.
3. **S11:** confirme com `cmp` que cada `apresentacoes_multiversao/figuras/* 2.png` é idêntica à sem
   " 2" e que nenhum `.json`/`.js`/`.py` cita " 2.png"; apague as idênticas.
4. Crie `.baseline/` e acrescente `.baseline/` ao `.git/info/exclude` (não ao `.gitignore`). Copie para lá
   as saídas que o git não guarda e que a Fase 3 vai comparar:
   `banco_de_dados/eda/ivs_especificacoes/ivs_referencia_por_setor.csv`,
   `banco_de_dados/eda/fatorial_multiversao/ivs_proposto_por_setor.csv`. Grave em
   `.baseline/sha256.txt` o sha256 de `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` e de
   `banco_de_dados/nacional/Base_Brasil_Censo2022.db`.
5. Medidas iniciais em `.baseline/medidas.txt`: `wc -l` de `src/ivs_censo/*.py`, `scripts/*.py`,
   `scripts/*.js`, `tests/*.py` (totais por pasta); resultado do pytest; contagem do ruff.
6. Commit da linha de base com **todo o trabalho pendente** (fatorial multiversão, correção da Fase 0,
   ajustes da RAIC), **exceto** a deleção do deck com notas da RAIC:
   `git add -A -- . ':!relatorio_parcial_raic/Apresentacao_Oral_RAIC_2026_Pedro.pptx'`.
   Mensagem: `chore: linha de base antes da simplificação (fatorial multiversão e ajustes de out/2026)`.
   Use o mesmo pathspec em todos os commits seguintes.
7. Grave o estado (modelo na seção 5) com o hash deste commit.

## FASE 1 — Correção dos erros (teto: 40 chamadas)

Invoque `/ponytail`. Para cada erro, nesta ordem — **E1, E2, E3, E5, E8, E7, E4, E6**:
1. `grep` dos chamadores;
2. **teste que falha antes da correção** (no arquivo de teste do módulo; poucas linhas, dados sintéticos);
3. a correção mínima no código compartilhado;
4. pytest verde; marque o erro no estado.

Detalhes que importam:
- **E1.** A correção principal é em `auc_postos` (descartar pares com ausente em escore ou rótulo).
  Depois disso, confira cada uso de `ie.indice`, `ev.indice_versao` e `fa.indice_01` com normalização
  municipal: o índice pode ter ausente e quem consome tem de aguentar. O teste: `auc_postos` com um ausente
  no grupo positivo devolve o mesmo que sem esse setor.
- **E2.** `comparar(a, b, mun, regra='ivs_bh')` em `ivs_especificacoes.py`, a partir de
  `fatorial_multiversao.comparar` (que passa a chamá-la). Nos três motores, a troca de faixa e a matriz
  de faixas (`eda_versoes` T32/T33/T34; `versoes_fatorial` `pct_muda_faixa`, `muda_faixa_v023_comum`;
  `ie.main` `muda_faixa_ivs_bh_*` e `muda_faixa_quartis_*`) saem das faixas **refeitas na amostra comum**.
  No `bloco13`, a referência entra pelo valor (`ivs_referencia`), não pela faixa gravada. O teste de
  `fm.comparar` que já existe tem de continuar passando, agora sobre `ie.comparar`, e ganha um caso com
  `regra='quartis'`.
- **E3.** Teste com um finalista `sem_rotacao`: `tucker_F2` ausente e `tucker_F1` calculado sobre a coluna
  sem rotação.
- **E5.** Reamostrar municípios: sortear `len(municipios)` nomes com reposição e juntar as linhas pelos
  índices pré-calculados de cada município (sem `concat` de DataFrames dentro do laço). Texto da E2 em
  `textos_blocos.json`: "reamostragem de municípios".
- **E6.** O teste só lê arquivos. Se algum número digitado não bater com os dados, o teste falha e
  **o gerador não é corrigido**: marque o teste com `xfail` e o motivo, e registre no relatório (é decisão
  do Pedro mexer num entregável enviado).

Commit: `fix: erros da revisão de 22/10 (ausentes no índice, troca de faixa na amostra comum, replicação por rotação, bootstrap por município)`.

## FASE 2 — Simplificação (teto: 45 chamadas)

1. `uvx ruff@0.6.9 check --select F401,F541 --fix src scripts tests` (fora dos arquivos da RAIC, seção 2.5),
   depois F841 e B007 à mão.
2. **S1 a S9**, cada uma com prova de equivalência (seção 2.3). Ordem: S4, S6, S9, S7, S5, S2, S3, S1, S8
   (de menor risco para o que exige reler notebook).
   - S1, S2, S3 e S8 mexem nos notebooks 01 e 02. A prova delas é a Fase 3 (passos 1 e 2): saída
     byte a byte igual. Mantenha os comentários linha a linha dos notebooks; edite as células com o
     `NotebookEdit`, sem salvar saídas.
3. **Varredura do resto.** Com os critérios da seção 2.1, procure em `scripts/` e `src/`: funções
   idênticas em mais de um arquivo, código sem chamador, ramos que nunca rodam, parâmetros nunca passados.
   Cada item: prova de equivalência ou "registrado, não mexido".
4. pytest e ruff (seção 2.2); `/ponytail-review` sobre `git diff <commit da Fase 0>`; corrija os erros.
5. Atualize `.baseline/medidas.txt` com o `wc -l` novo. Commit: `refactor: simplificação sem mudança de saída (S1–S9 e varredura)`.

## FASE 3 — Regeneração das saídas (teto: 35 chamadas)

Rode na ordem abaixo; cada passo depende do anterior. Depois de cada passo, compare com a linha de base
(`git diff --stat` nas saídas versionadas; para as cópias de `.baseline/`, um script que diga quais
colunas mudaram e em quantas linhas). **Esperado** é o que está na seção 4; o resto vai para o relatório
como "a investigar" (seção 2.4).

| # | Comando | Tempo | Esperado |
|---|---|---|---|
| 1 | `./.venv/bin/jupyter execute notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb` | longo | `Base_ELSI_Bruta_Censo2022.csv` com o **mesmo sha256** |
| 2 | `./.venv/bin/jupyter execute notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb` | médio | CSVs de `banco_de_dados/eda/` **idênticos** (PNG pode mudar bytes) |
| 3 | `./.venv/bin/python scripts/gerar_entrega_orientadora.py` | ~2 min | idêntico, salvo `gerado_em` nos metadados |
| 4 | `./.venv/bin/python scripts/proporcoes_brasil.py` | ~7 min | `banco_de_dados/nacional/*.csv` idênticos |
| 5 | `auditoria_renda.py` e `auditoria_renda.py --sem-extremo`; `gerar_tabelas_auditoria.py` | curto | idêntico |
| 6 | `./.venv/bin/python scripts/ivs_especificacoes.py` | ~3 min | seção 4.1 |
| 7 | `gerar_relatorio_ivs_final.py`; `gerar_notebook_ivs_final.py` | curto | números do NB05 que vêm das colunas da 4.1 |
| 8 | `./.venv/bin/python scripts/versoes_fatorial.py` | ~11 min | seção 4.2 |
| 9 | Para cada pasta de `analises_exploratorias/` com `config.json` que não começa com `E` nem é `00_sintese` (primeiro `00_referencia`): `eda_versoes.py <pasta>`, `node scripts/gerar_deck_versao.js <pasta>`, `verificar_versao.py <pasta> --sem-pytest` | longo | seção 4.3 |
| 10 | `eda_transversais.py` em `E1_…` a `E6_…`, deck e verificador de cada; `sintese_versoes.py`; deck da `00_sintese`; `sintese_versoes.py --catalogo` | longo | seção 4.3 |
| 11 | `fatorial_multiversao.py --camada 3`; `dados_apresentacoes_multiversao.py`; `node scripts/gerar_decks_multiversao.js todos` e `FIN`; `verificar_multiversao.py --fase 3` a `--fase 7` | ~10 min | seção 4.4 |
| 12 | `dados_versoes_fatorial.py`; `dados_relatorio_descritivo.py`; `dados_apoio_relatorio.py`; `verificar_versoes_fatorial.py`; `verificar_relatorio_descritivo.py` | curto | só dados; os decks desses dois não são regerados (seção 2.5) |

Os passos 1 e 2 leem os 2,4 GB de `dados/`; o 9 e o 10 somam a parte mais longa — rode cada um em background.
Commit: `chore(saidas): regeração com os erros corrigidos`.

## FASE 4 — Relatório, documentação e grafo (teto: 20 chamadas)

1. `docs/relatorios/Simplificacao_e_Correcoes_2026-10.md`:
   - **Simplificação:** linhas antes × depois por pasta (`.baseline/medidas.txt`), o que foi juntado e
     apagado, o que ficou registrado sem mexer e por quê.
   - **Cada erro:** causa, correção, teste, e os **números antes → depois** que importam (linha de base do
     commit da Fase 0 × agora): troca de faixa por eixo no NB05; % que muda de faixa por versão (T33) e por
     eixo nas 108; Tucker dos finalistas; intervalos da E2; AUC global (mudança ínfima, dizer de quanto).
   - **Entregáveis afetados e não regerados:** relatório descritivo v3/v4, decks das 108 versões, deck final
     da multiversão se a trava recusou — para cada um, os IDs de slide cujo número mudou e o valor novo.
   - **A investigar:** o que mudou fora do esperado (seção 2.4).
   - **Decisões para o Pedro:** E4 (separar matriz e régua?) e E6 (se algum número da RAIC não bateu).
2. Documentação mínima, só o que ficou falso: `README.md` (contagem de testes; "normalização de renda por
   município pendente no NB03" — o NB03 não existe e a normalização municipal está em `ie.indice`),
   `scripts/README.md` (contagem de scripts; as funções compartilhadas novas em `src/ivs_censo`), uma linha
   no `ESTADO.md` de cada pasta regerada (`analises_exploratorias/`, `versoes_fatorial/`,
   `relatorio_descritivo/`) e no `estado_fatorial_multiversao_2026-10.md`; uma linha neste índice
   (`docs/prompts/README.md`) marcando o prompt como executado.
3. `graphify update .` (só a parte de código, sem custo de modelo).
4. Commit: `docs: relatório da simplificação e das correções`. Grave o estado como concluído.
5. Mensagem final ao Pedro (até 20 linhas): linhas removidas, erros corrigidos, números que mudaram nos
   entregáveis, o que ficou para ele decidir, e o comando para revisar o ramo:
   `git log --oneline main..simplificacao-codigo` e `git diff --stat main simplificacao-codigo`.

---

## 4. O que pode mudar na Fase 3 (o resto tem de sair idêntico)

Além do que cada correção abaixo explica, a correção da Fase 0 (22/10, ainda não regerada) muda: o IVS de
São Raimundo do Doca Bezerra (1 setor) vira ausente com faixa `-1`, e municípios com menos de 4 setores
saem sem faixa nos quartis.

### 4.1 `banco_de_dados/eda/ivs_especificacoes/`
- `especificacoes.csv` e `avaliacao.csv`: `auc_global_*` nas especificações municipais (variação ínfima,
  E1); `spearman_ref_comum`; `muda_faixa_ivs_bh_*` e `muda_faixa_quartis_*` (E2); `faixas_indefinidas`.
- `acrescimo_renda.csv`: as colunas da logística e o texto `conclusao` (E1).
- `ivs_referencia_por_setor.csv`: o setor de São Raimundo e as faixas por quartis de municípios pequenos.
- **Têm de sair idênticos:** `pesos.csv`, `estabilidade.csv`, `referencia.csv` (a referência proposta não
  muda — o critério de escolha usa a AUC municipal, que já descartava ausentes). Se `referencia.csv`
  mudar, isso entra em "a investigar" com destaque.

### 4.2 `banco_de_dados/eda/versoes_fatorial/`
- `versoes.csv`: `auc_global_*`, `muda_faixa_v023_comum`, `pct_<faixa>`, `pct_indefinida`.
- `pares_por_eixo.csv` e `pares_detalhe.csv`: `pct_muda_faixa*` (E2), `d_auc_global_comum*`.
- **Idênticos:** `cargas.csv`, `estabilidade.csv`, e as colunas de KMO, MSA, cargas, pesos e elegibilidade.

### 4.3 `analises_exploratorias/`
- Em cada versão: T25 (faixas por quartis), T26 (AUC global), T31–T34 (E2), `setores_indice.csv`; os
  textos do catálogo que citam esses números.
- C5: passa a gerar T36–T38 e F30 (antes quebrava).
- E1–E6 e `00_sintese`: o que depende dos itens acima; E2 (T44, T45, F43) muda de método (E5).
- **Idênticos:** T01–T24 e T27–T30 de todas as versões, salvo o efeito do setor de São Raimundo.

### 4.4 `banco_de_dados/eda/fatorial_multiversao/` e `apresentacoes_multiversao/`
- `camada3_replicacao.csv` e `camada3_finalistas.csv`: `tucker_*` de finalista que não é promax (E3).
- `dados/FIN.json` e o deck final: FIN-56 e FIN-68 (E3); o "Como ler" de FIN-39/40 e as limitações em
  FIN-75 (E4). Os 12 decks de indicador só mudam se citarem Tucker.
- **Idênticos:** camadas 1 e 2 (não são regeradas).

---

## 5. Modelo do arquivo de estado (`docs/prompts/estado_simplificacao_2026-10.md`)

```markdown
# Estado — simplificação e correções (out/2026)

Prompt: `docs/prompts/prompt_simplificacao_correcoes_2026-10.md` · ramo `simplificacao-codigo`

## Situação: fase N, passo P — próximo: …

## Commits
| Fase | Hash | Data |
|---|---|---|

## Erros (Fase 1)
| # | Situação (corrigido / revertido / xfail) | Teste | Observação |
|---|---|---|---|

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
```
