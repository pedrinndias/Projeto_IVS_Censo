# Auditoria do projeto, do andamento e dos dados — 22/11/2026

**HEAD:** `6d8a3de` (branch `feat/ontologia-dados`) · **Base:** a revisão de ponta a ponta de 12/11/2026
([`Revisao_Ponta_a_Ponta_2026-11.md`](Revisao_Ponta_a_Ponta_2026-11.md)), que cobriu código, método, decks e rumo e deixou de
fora `dados/`, `Backup/` e as bases legadas.
**Como foi feita:** somente leitura. Um script de conferência fora do repositório, `pytest`, consultas `sqlite3 -readonly` e
`git`. Nada foi editado, regerado nem commitado além deste arquivo.

Esta auditoria não repete os 48 achados de 12/11 (A01–A14, P01–P10, C01–C11, E01–E06, U1–U5). Ela confere (1) o que mudou desde
então, (2) o que segue aberto e (3) todos os dados, que ficaram de fora da revisão.

---

## 1. Veredito

- **Dados: íntegros.** As três bases `.db` passam no `quick_check`; a base ELSI tem 109.032 setores únicos, 70 municípios iguais
  à lista oficial e os mesmos setores do CSV bruto; todos os números-chave de base, recorte, favela e cobertura de A e B foram
  refeitos a partir dos dados e batem.
- **Andamento: parado no caminho crítico.** Em 10 dias desde a revisão entrou um commit, o da ontologia. Nenhuma das 7 ações
  "até a próxima reunião" aparece no repositório; mapas, manuscrito e relatório final seguem sem início; o README está em 05/11 e
  ainda trata a RAIC como evento futuro.
- **Peso morto:** 5,7 GB de dados legados dentro do iCloud que nenhum código lê.
- **Ontologia: correta, mas nova e incompleta.** O recorte que ela define dá os 104.108 setores; porém nenhuma das 128 entradas
  foi certificada, e ela descreve o banco de 22/10, que não tem o IVS.

---

## 2. Andamento desde 12/11

| Item | Situação em 22/11 | Evidência |
|---|---|---|
| Commits | 1 (`6d8a3de`, ontologia, 18/11) na branch `feat/ontologia-dados`, ainda não juntada à `main`; a `main` está 2 commits à frente do `origin` | `git log 8e1e1ca..HEAD`; `git rev-list --count` |
| Plano de ação, itens 1–7 (até a reunião) | Nenhum feito no repositório. Respostas por e-mail ou reunião não foram vistas | `git log`; arquivos com data posterior a 12/11 |
| RAIC (U1–U5) | O evento era de 09 a 13/11. O `_ENVIO_v5.pptx` não mudou depois da revisão (12/11 14:46); se U2 e U3 foram corrigidos, foi em outro arquivo. Há um `~$..._v5.pptx` (trava do PowerPoint) | `ls -la relatorio_parcial_raic/` |
| E01: v4 sobrescrito pelo v5 | Aberto: v4 e v5 seguem com 1.900.192 bytes e a mesma hora; o v4 enviado só existe no git (`37feda9`, 01/11) | `git status`; `ls -la` |
| E02: cópias do iCloud | Aberto: `scripts/gerar_roteiro_word_raic 2.py`, `Roteiro_..._Pedro 2.docx` e **`.git/index 2`** | `find -name '* 2.*'` |
| E03: tags de entrega | Aberto: nenhuma tag | `git tag` |
| E04: `last_query_stamp` versionado | Aberto: segue sujando o `git status` | `git status` |
| E06: arquivos sem procedência | Aberto: `C04_pesos_final.png` e `_ENVIO_v4.pdf` fora do git | `git status` |
| C07: shebang do jupyter | Aberto: `.venv/bin/jupyter` aponta para `/Users/pedro/Code/Projeto_IVS_Censo22/.venv/bin/python` | `head -1 .venv/bin/jupyter` |
| C11: dependências | **Confirmado** (era suspeita): `reportlab` está no `requirements.txt`, é importado por 5 scripts e **não está instalado** no `.venv`; `pypdf` é usado por 4 scripts e não está declarado | `import reportlab` → `ModuleNotFoundError` |
| C09: urbano por `SITUACAO` × `CD_SIT` | **Fechado nos dados:** `CD_SIT` 1–3 = `Urbana` (106.347) e 5–8 = `Rural` (2.607), sem exceção. Falta só o teste | `crosstab(CD_SIT, SITUACAO)` |
| Testes | 170 passam em 27 s, igual a 12/11 | `pytest -q` |
| Mapas (objetivo 2) | Não iniciados: nenhum `.qgz`, `.gpkg`, `.shp` ou malha. Os arquivos `*_mapa*.png` são mapas de calor de cargas, não mapas geográficos | `find` |
| Manuscrito e relatório final | Não iniciados | `docs/` |

**Calendário:** o relatório final está previsto para dezembro a fevereiro e a submissão do artigo para fevereiro de 2027. Faltam
cerca de 10 semanas. Os mapas já estavam previstos até setembro.

---

## 3. Dados

### 3.1 Inventário

| Grupo | Onde | Tamanho | Usado pelo código? | No git? |
|---|---|---:|---|---|
| Agregados brutos do IBGE (8 temas) | `dados/Agregados_por_setores_*.csv` | 2,4 GB | **Sim** (`src/ivs_censo/fontes.py`) | Não (`.gitignore`) |
| Dicionários do IBGE | `dados/dicionario_*.xlsx` | 128 KB | Sim | Sim |
| Lista dos 70 municípios | `dados/municipios_elsi_brasil.csv` | — | Sim | Sim |
| Favelas e comunidades urbanas | `dados/FavelaseComunidadesUrbanas2022Setores_20250417.xlsx` | 1,3 MB | Sim (3 arquivos) | Sim |
| Base ELSI bruta | `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` | 27 MB | **Sim** (entrada da pipeline) | Não |
| Entrega à orientadora | `banco_de_dados/entrega_orientadora/*.db` (ELSI 45 MB, BH 2 MB) | 47 MB | Sim (21 e 2 arquivos) | Não |
| Base nacional | `banco_de_dados/nacional/Base_Brasil_Censo2022.db` | 169 MB | Sim (2 arquivos) | Não |
| Saídas das análises | `banco_de_dados/eda/`, `analises_exploratorias/`, `versoes_fatorial/`, `apresentacoes_multiversao/` | ~800 MB | Geradas | Em parte |
| **Legado: bancos SQL de março** | `dados/banco_de_dados/SQL/` (`Banco_Censo_Completo.db` 3,2 GB, `Banco_IVS.db` 1,3 GB, `Banco_IVS_Essencial.db` 57 MB) | 4,5 GB | **Não** | Não |
| **Legado: bases unificadas** | `dados/banco_de_dados/*.csv` e `.xlsx` (`Base_Censo_Completa_Unificada.csv` 1,0 GB, `temp_merge1.csv` 191 MB, mais 3) | 1,1 GB | **Não** | Não |
| **Legado: processadas** | `dados/processed/` | 85 MB | **Não** | Não |
| Backup | `Backup/banco_de_dados/` e mais | 306 MB | Não | 21 arquivos |
| Saída de busca antiga | `dados/output/` | 376 KB | Não verificado | — |

"Usado pelo código" foi apurado com `grep` do nome do arquivo em `src/`, `scripts/`, `notebooks/` e `tests/`.

### 3.2 Integridade (tudo refeito a partir dos dados)

| Verificação | Resultado |
|---|---|
| Base ELSI bruta: linhas × colunas | 109.032 × 74 |
| `CD_SETOR` únicos, 15 dígitos, prefixo igual ao `CD_MUN` | 109.032 únicos, 0 duplicados, todos com 15 dígitos e prefixo certo |
| Municípios × lista oficial | 70 = 70, nenhum sobrando nem faltando |
| Colunas 100% vazias | 0 |
| Sigilo (`X`) | 62 das 74 colunas têm `X`; no máximo 23.684 setores numa coluna |
| Recorte de análise (urbano com `V00001 > 0`) | **104.108** = declarado |
| Favela por `CD_TIPO = 1`: base / recorte | **19.507 (17,9%) / 19.452 (18,7%)** = declarado |
| `.db` da entrega (ELSI): `quick_check`, setores | ok; 109.032 setores, os mesmos do CSV bruto (0 de diferença nos dois sentidos) |
| `.db` de BH | ok; 5.166 setores |
| `.db` nacional | ok; 468.099 setores = linhas do agregado básico do IBGE |
| Agregados temáticos | 458.772 linhas cada um dos 7 temáticos; o básico tem 468.099 |
| `ivs_final_por_setor.csv` (corte 0,4) | 104.108 setores; A com 75.926, B com 87.511, anterior com 87.544 = declarado |
| `metadados` do `.db` × números do README | Todos batem (109.032; 106.347; 104.108; 19.507; 19.452) |

### 3.3 Achados dos dados

| id | Sev. | Evidência | Por que importa | Correção | Esf. |
|---|---|---|---|---|---|
| D01 | Médio | 5,7 GB em `dados/banco_de_dados/` e `dados/processed/` (bancos SQL e bases unificadas de março de 2026) sem nenhuma referência no código. | Ocupam o iCloud e multiplicam o risco de cópias `" 2"`; quem abre o projeto não sabe qual base vale. | Mover para um arquivo fora do repositório e fora do iCloud (disco externo), com um `LEIAME` dizendo de onde vieram. Não apagar antes de conferir se algum documento entregue cita esses arquivos. | P |
| D02 | Médio | Nenhum manifesto de hash dos agregados brutos foi encontrado em `dados/` nem nos `.md` de `docs/`; os nomes têm datas diferentes (`_20250417` em dois, sem data nos outros seis). | Se o IBGE republicar um tema, não há como provar com qual versão o índice foi calculado. | Um `dados/MANIFESTO.sha256` com `shasum -a 256 dados/Agregados_*.csv` e a data de download. | P |
| D03 | Baixo | No recorte, 19 setores têm `CD_FCU` preenchido e `CD_TIPO = 0`. | Quem contar favela por `CD_FCU` acha 19.471 setores, não 19.452. | Uma frase na nota metodológica: "favela = `CD_TIPO = 1`; 19 setores com código de FCU e `CD_TIPO = 0` ficam fora". | P |
| D04 | Baixo | Na tabela `metadados` do `.db`, os números estão em texto com vírgula de milhar ("109,032") e a chave `setores_excluidos_de_renda_media_sem_extremo` guarda um código de setor (`310620005650366`), não uma contagem. | Ambíguo para quem lê o banco, inclusive a orientadora e a ontologia. | Na próxima regeração da entrega, gravar números como número e renomear a chave para `cd_setor_excluido_...`. | P |
| D05 | Info | Os 7 agregados temáticos têm 9.327 setores a menos que o básico. | Esperado se o IBGE não publica temas para setores sem moradores. **Não conferido.** | Conferir com um `merge` antes de citar. | P |

---

## 4. Ontologia (`ontologia/`, commit `6d8a3de`)

| id | Sev. | Evidência | Por que importa | Correção | Esf. |
|---|---|---|---|---|---|
| O01 | Médio | 0 das 128 entradas com `certificado: true`; o resumo marca todas as métricas como "[não certificado]". | A ontologia ainda é uma proposta: nenhuma métrica foi conferida contra um número conhecido. | Rodar `/ontologia-dados certificar` usando como gabarito os números da seção 3.2 (já conferidos aqui). | P |
| O02 | Médio | A ontologia descreve o `.db` de 22/10, que não tem IVS nem faixa (só os 23 `pct_*` e as variáveis brutas). O IVS A/B mora em `banco_de_dados/eda/fatorial_corte_04/ivs_final_por_setor.csv`. | As perguntas que mais importam agora (cobertura, faixas, A × B por município) não são respondidas por ela. | Depois de congelar o IVS, incluir a tabela final na entrega e recompilar. Antes disso, não vale estender. | M |
| O03 | Baixo | Branch `feat/ontologia-dados` não juntada; `main` 2 commits à frente do `origin`. | Trabalho só local. | Juntar e enviar quando quiser. | P |

O que está certo: o recorte `analise` (`SITUACAO = 'Urbana' AND Dados_sig = 'OK'`) devolve exatamente 104.108 setores; as
armadilhas de sigilo e de `renda_media_sem_extremo` estão registradas; a avaliação deu 13/13 com Sonnet e Haiku.

---

## 5. O que fazer, em ordem

| # | Ação | Origem | Esf. |
|---|---|---|---|
| 1 | Seguir o plano de 12/11 a partir do item 2: confirmar a regra de sigilo no PDF do IBGE, rodar A e B com o sigilo imputado, página de perguntas com prazo de veto e reunião | Revisão §6 | M |
| 2 | Baixar a malha de setores 2022 do IBGE e fazer o primeiro mapa (não depende de decisão) | Revisão §5.2 | M |
| 3 | Atualizar o Status do README (RAIC concluída, data) | §2 | P |
| 4 | Restaurar o v4 enviado, nomear o v5, apagar a trava `~$`, comparar e remover as duas cópias `" 2"`; conferir o `.git/index 2` antes de qualquer coisa | E01, E02 | P |
| 5 | Tags `raic-2026` e `deck-corte-04-v2` | E03 | P |
| 6 | `requirements.txt`: tirar ou instalar `reportlab`, declarar `pypdf`; recriar o `.venv` para corrigir o shebang do jupyter | C11, C07 | P |
| 7 | Mover os 5,7 GB legados para fora do repositório e do iCloud | D01 | P |
| 8 | Manifesto de hash dos agregados brutos | D02 | P |
| 9 | Certificar a ontologia com os números da seção 3.2 | O01 | P |

Os itens 4 a 9 cabem numa tarde. Os itens 1 e 2 são o caminho crítico.

---

## 6. O que não foi verificado

- Respostas da orientadora fora do repositório e se a apresentação da RAIC aconteceu como planejado.
- O conteúdo dos 5,7 GB legados (só tamanho, data e ausência de referência no código); se algum documento já entregue cita esses
  arquivos.
- Os achados de método, decks e código de 12/11 que não dependem de arquivo novo: foram dados como abertos, sem reler.
- D05 (setores sem tema no IBGE) e a origem dos 9.327 setores.
- `dados/output/` e o conteúdo de `Backup/`.
- Os valores das colunas `pct_*` do `.db` contra a pipeline (só setores, contagens e metadados foram cruzados).
