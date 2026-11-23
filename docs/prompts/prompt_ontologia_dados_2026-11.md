# Prompt de execução — ontologia dos dados: checar, reforçar e certificar (nov/2026)

**Pedido do Pedro (22/11/2026):** "Desenvolva um prompt para realizar a ontologia dos dados com as skills elencadas com base na
auditoria."
**Base:** [`Auditoria_Projeto_e_Dados_2026-11-22.md`](../relatorios/Auditoria_Projeto_e_Dados_2026-11-22.md), seções 3 e 4
(achados D03, D04, O01, O02, O03) e a ontologia já compilada em `ontologia/` (commit `6d8a3de`, branch `feat/ontologia-dados`).
**Como usar:** sessão nova do Claude Code na raiz do projeto, na branch `feat/ontologia-dados`, modelo **Claude Sonnet 5.5**,
esforço **médio** (é execução com receita; a decisão é do Pedro nas paradas). Cole:
*"Execute `docs/prompts/prompt_ontologia_dados_2026-11.md`. Leia primeiro `docs/prompts/estado_ontologia_dados_2026-11.md` se
ele existir."*
**Saída:** `ontologia/ontologia.yaml` e `ontologia/resumo.md` atualizados, `ontologia/avaliacao/certificacao_2026-11.md` (a
evidência de cada item certificado) e o arquivo de estado.
**Custo:** baixo a médio, cerca de 70 chamadas até o fim do lote 2. Sem subagentes. A Fase 5 completa (reavaliar com modelos) é
opcional e custa mais.

**Esta não é uma execução sem parar.** A skill `ontologia-dados` proíbe certificar sem o Pedro aprovar cada lote. As fases 0 a 3
correm seguidas; a partir da parada 1 cada passo espera resposta.

| Fase | O quê | Skills | Teto | Para no fim? |
|---|---|---|---:|---|
| 0 | Linha de base | — | 6 | não |
| 1 | A fonte mudou desde 18/11? | `/ontologia-dados checar` | 6 | só se a fonte mudou |
| 2 | Evidência: significado das colunas e origem de cada métrica | `/data:explore-data`, `graphify query` | 15 | não |
| 3 | Validação: cada métrica ao pé da letra contra o gabarito | `/data:write-query`, `/data:validate-data` | 15 | **parada 1** |
| 4 | Certificação em lotes | `/ontologia-dados certificar` | 8 por lote | **parada a cada lote** |
| 5 | Regerar o gabarito e o resumo; reavaliação opcional | — (opcional: `/anthropic-skills:skill-creator`) | 6 | **parada 2** |
| 6 | Camada do IVS final (condicional) | `/ontologia-dados compilar` | 20 | só se o IVS estiver congelado |
| 7 | Fechamento | — | 5 | fim |

**Autorização.** O Pedro escolheu as skills da tabela ao pedir este prompt. Isso substitui, só aqui, a regra "nunca invoque uma
skill por conta própria" do `CLAUDE.md` global, e só para as skills da tabela. As demais regras dele valem, inclusive "pare ao fim
de cada etapa" nas paradas marcadas.

---

## 1. Regras para todas as fases

- **Pode escrever só:** `ontologia/ontologia.yaml`, `ontologia/resumo.md` (só via `resumo.py`), `ontologia/perfil.json` (só via
  `perfil.py`), `ontologia/avaliacao/` e o arquivo de estado. Scripts de conferência ficam no scratchpad.
- **Não toque** em dados, nos `.db`, em `src/`, em `scripts/` nem na pipeline. O D04 (formato da tabela `metadados`) se corrige no
  `scripts/gerar_entrega_orientadora.py`: aqui ele vira só armadilha no YAML.
- **Fonte:** `banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db`, sempre aberto em modo só leitura.
- **Evidência vale só se vier de código do projeto ou de consulta ao banco.** Texto da auditoria, de relatório ou de README pode
  apontar onde olhar, mas não é prova. Nunca grave `certificado: true` sem o "aprovo" do Pedro no chat, lote a lote.
- **Toda mudança no YAML:** mostre o diff, rode `checar.py`, depois `resumo.py`. `checar.py` com PROBLEMA: corrija antes de seguir.
- Comandos da skill (rode da raiz):
  ```bash
  S=~/.claude/skills/ontologia-dados/scripts
  uv run --with pyyaml python $S/checar.py
  uv run --with pyyaml python $S/resumo.py
  ```
- **Estado:** atualize `docs/prompts/estado_ontologia_dados_2026-11.md` ao fim de cada fase e de cada lote, com três partes: o que
  funcionou (com evidência), o que falhou, o que falta. Se a sessão cair, retome dali sem refazer.
- Relatório de fase no chat: no máximo 15 linhas. Saídas de comando truncadas (`| head -60`).
- Commits: só com OK do Pedro, só com o nome dele, sem trailer de IA.

---

## 2. Fases

### Fase 0 — Linha de base (sem skill)
1. `git status -sb` e `git log -3 --oneline`. Confirme a branch `feat/ontologia-dados`. Se não for ela, pare e pergunte.
2. Leia a seção 4 da auditoria e as linhas "Recortes" e "Métricas" de `ontologia/resumo.md`. Não leia o YAML inteiro.
3. Rode `checar.py` e anote a linha de certificação (esperado: `0/128 itens`).

### Fase 1 — A fonte mudou? (`/ontologia-dados checar`)
1. Regere o perfil **no scratchpad**, não por cima do versionado:
   `.venv/bin/python $S/perfil.py <fonte> --dicionario dicionario_variaveis --saida <scratchpad>/perfil_novo.json`
2. Compare tabelas, colunas e contagens com `ontologia/perfil.json` (esperado: 3 tabelas; `setores_censitarios` com 109.032
   linhas e 108 colunas).
3. Igual: siga. Diferente: liste o que mudou e **pare**. Recompilar é decisão do Pedro.

### Fase 2 — Evidência (`/data:explore-data`, `graphify query`)
Objetivo: para cada métrica, para o recorte e para as colunas que eles usam, achar **onde o código define** e **o que o dado mostra**.

1. **Origem no código.** Para cada uma das 8 métricas e para o recorte `analise`, rode
   `graphify query "onde é calculado <coluna>" --budget 1500` e confirme abrindo só a função apontada (esperado:
   `src/ivs_censo/indicadores.py`, `classificar_dados_sig` e `calcular_indicadores`; renda em `src/ivs_censo/renda.py`). Anote
   `arquivo:linha`.
2. **Perfil das colunas do lote 2** (lista na Fase 4) com `/data:explore-data`, só no recorte: nulos, mínimo, máximo, valores de
   baixa cardinalidade. Confira três fatos da auditoria:
   - `Dados_sig` entre os urbanos: OK 104.108, SIGILOSO 766, ZERADO 1.473. Confirme no código o que é cada valor.
   - **D03:** 19 setores do recorte têm `CD_FCU` preenchido e `CD_TIPO = 0`; a favela do projeto é `CD_TIPO = 1` (`is_fcu`).
   - **D04:** `metadados.valor` guarda números como texto com vírgula de milhar ("109,032"), e a chave
     `setores_excluidos_de_renda_media_sem_extremo` guarda um código de setor, não uma contagem.
3. Escreva a **proposta de alterações** em `ontologia/avaliacao/proposta_alteracoes_2026-11.md`, sem mexer no YAML ainda:
   - armadilha em `CD_FCU` (D03) e em `metadados.valor` (D04);
   - `fonte` com `arquivo:linha` em cada métrica e no recorte;
   - os significados de `Dados_sig` que faltarem em `valores`;
   - qualquer descrição que o dado contradiga.

### Fase 3 — Validação (`/data:write-query`, `/data:validate-data`)
1. Regere o gabarito com o código do projeto: `PYTHONPATH=src .venv/bin/python ontologia/avaliacao/gabarito.py`.
2. Com `/data:write-query`, escreva o SQL **ao pé da letra** de cada métrica: a `expressao` com os `filtros_obrigatorios` do recorte,
   sem acrescentar nada. Rode no `.db` em modo só leitura.
3. Com `/data:validate-data`, compare cada resultado com o `gabarito.json` e com o recálculo do `gabarito.py` (que confere o banco
   contra `calcular_indicadores`). Tolerância: 0 para contagens, 0,0005 para proporções.
4. Monte a tabela de evidência em `ontologia/avaliacao/certificacao_2026-11.md`: item · SQL · valor · gabarito · diferença · origem
   no código (`arquivo:linha`) · veredito (BATE / NÃO BATE / SEM GABARITO).

**Parada 1.** Mostre ao Pedro: a proposta de alterações (Fase 2), a tabela de evidência (Fase 3) e o diff que você aplicaria no YAML.
Com o OK, aplique, rode `checar.py` e `resumo.py`. Item que NÃO BATE não vai para certificação: fica registrado no estado com a causa.

### Fase 4 — Certificação (`/ontologia-dados certificar`)
Lotes de até 15, na ordem da skill (métricas primeiro). Em cada lote, mostre por item: a definição, o valor, o gabarito e a origem
no código. O Pedro aprova, corrige (`fonte: usuario`) ou rejeita. Só então grave `certificado: true`. Atualize o estado depois de
cada lote.

| Lote | Itens | Quantos |
|---|---|---:|
| 1 | as 8 métricas, o recorte `analise` e as 3 tabelas (termo, descrição, granularidade) | 12 |
| 2 | as colunas que as métricas e o recorte usam: `CD_SETOR`, `CD_MUN`, `SITUACAO`, `Dados_sig`, `V00001`, `CD_TIPO`, `CD_FCU`, `is_fcu`, `pct_agua_inad`, `pct_esgoto_inad`, `pct_lixo_inad`, `pct_analfab`, `pct_raca_pretpardind`, `razao_moradores`, `renda_media_sem_extremo` | 15 |
| 3 em diante | as outras ~101 colunas, a maioria copiada do dicionário do IBGE (`fonte: dicionario`) | ~7 lotes |

**Padrão:** pare depois do lote 2 e pergunte se segue para os lotes 3 em diante agora ou noutra sessão. Os lotes 1 e 2 cobrem tudo
o que as perguntas de análise usam.

### Fase 5 — Regerar e reavaliar
1. `gabarito.py`, `checar.py`, `resumo.py`. Anote a nova linha `certificado: n/128`.
2. **Opcional, só com OK do Pedro (custo alto, abre subagentes):** refazer a avaliação de `ontologia/avaliacao/resultados.md` (13
   perguntas, Sonnet e Haiku) com `/anthropic-skills:skill-creator`, para medir se a certificação mudou acertos ou tokens. Sem OK,
   pule e registre.

**Parada 2.** Mostre: itens certificados, itens rejeitados com a causa, a linha de certificação e o diff final do YAML.

### Fase 6 — Camada do IVS final (O02; condicional)
Só rode se o Pedro disser, nesta sessão, que o IVS foi congelado e qual arquivo é o final. Senão, registre "não executado: IVS
não congelado" e vá para a Fase 7.

Se rodar: compile uma ontologia separada, sem tocar na do banco da entrega:
```bash
.venv/bin/python $S/perfil.py <csv_final> --saida ontologia/ivs_final/perfil.json
# compilar conforme a skill, escrevendo em ontologia/ivs_final/ontologia.yaml
uv run --with pyyaml python $S/checar.py --ontologia ontologia/ivs_final/ontologia.yaml --perfil ontologia/ivs_final/perfil.json
uv run --with pyyaml python $S/resumo.py --ontologia ontologia/ivs_final/ontologia.yaml --saida ontologia/ivs_final/resumo.md
```
Relação com o banco da entrega por `CD_SETOR` (o CSV do corte tem 104.108 setores, todos contidos no banco). Armadilhas
obrigatórias: faixas gravadas fora da amostra comum (A13 da revisão de 12/11), cobertura de A e B diferente, setores sem índice
concentrados nos mais ricos (A09).

### Fase 7 — Fechamento
1. Estado final e um resumo de até 15 linhas no chat.
2. **Proponha** o bloco "Dados" da skill para um `CLAUDE.md` do projeto (o projeto ainda não tem um). Só grave com OK.
3. Lembre o O03: a branch `feat/ontologia-dados` não está na `main`, e a `main` está 2 commits à frente do `origin`. Não junte nem
   envie: pergunte.
4. Ofereça o commit das mudanças em `ontologia/` e do estado, com a mensagem pronta.

---

## 3. Fora do escopo

- Corrigir o formato da tabela `metadados` (D04) e regerar a entrega: é mudança de script e de dado.
- D05 (setores sem dados temáticos no IBGE): só afeta a base nacional, que esta ontologia não cobre.
- Compilar a base nacional ou a de BH: só se o Pedro pedir.
- `/data:data-context-extractor`: geraria uma skill paralela à ontologia, com o mesmo conteúdo.
