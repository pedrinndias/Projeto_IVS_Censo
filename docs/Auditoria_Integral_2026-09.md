# Auditoria integral do Projeto IVS — Censo 2022 / ELSI-Brasil

**Data:** 17 de setembro de 2026
**Escopo:** pipeline ativa, módulo, scripts, dados, documentos e decks em circulação
**Fora do escopo:** `Backup/`, `notebooks/Fase1*`/`Fase2*`, `Apresentacoes_IVS/historico/`, `graphify-out/`
**Auditoria anterior:** [`Relatorio_Integridade_Projeto.md`](Relatorio_Integridade_Projeto.md) (19/05/2026, revisado em 12/06 e 09/08)

> **Limitação declarada do auditor.** Boa parte do que foi auditado — o módulo
> `src/ivs_censo/fatorial.py`, o Notebook 04, o relatório da análise fatorial, o gerador do
> deck fatorial e o próprio prompt desta auditoria — foi escrito por mim, em 16 e 17/09/2026.
> Auditar o próprio trabalho tem ponto cego que nenhuma disciplina elimina. Os achados sobre
> essa camada foram verificados por execução, não por leitura, sempre que possível; ainda
> assim, **uma revisão independente dessa parte continua necessária** e esta auditoria não a
> substitui. Onde um achado recai sobre código meu, está marcado com †.

---

## Sumário executivo

O projeto está íntegro no que mais importa: **a pipeline reproduz byte a byte**. Os três
notebooks, os dez scripts geradores e os três decks, reexecutados do zero, devolvem
arquivos idênticos aos versionados — inclusive um bootstrap de mil reamostragens e a
travessia de 8 GB de microdados. As contagens-âncora conferem contra o banco, a regra
`Dados_sig` recalcula idêntica nas 109.032 linhas, os dois `.db` batem com os `.csv` célula
a célula, e cada número do docstring de `indicadores.py` sobre o viés do sigilo se
reproduz. **Nenhum ERRO foi encontrado.**

O que ameaça o projeto não é o cálculo: é a **rastreabilidade**. O README de procedência
cobre 50 de 114 CSVs; três geradores de deck carregam cerca de cem medições digitadas à
mão no texto dos slides, e uma delas — a correlação 0,459 — não existe em arquivo nenhum;
um documento entregue à orientadora está mais pobre que o código que o gera; e toda a
camada de análise fatorial vive em dois documentos sem ter chegado ao `GUIA_DO_PROJETO.md`,
que é a fonte da verdade declarada. É a falha recorrente da casa, reaparecendo em material
novo.

---

## Achados

### DIVERGENTE — dois documentos do projeto dizem coisas diferentes

| # | Onde | O que está errado |
|---|---|---|
| D1 † | `GUIA_DO_PROJETO.md` §5, §8 · `docs/MANUAL_DO_PROJETO.md` · `README.md` | **A análise fatorial não chegou à documentação mestre.** O Guia diz "2 notebooks (01→02)" e lista "Análise fatorial / pesos / cálculo do IVS final" como 🔴 Pendente. Existem 3 notebooks e a etapa está feita. KMO, Bartlett, os 87.545 casos completos, os pesos 65/35 e o AUC 0,813 aparecem **apenas** em `Relatorio_Analise_Fatorial_NB04.md` e `Analise_Fatorial_Figueiredo2010_e_o_Projeto_IVS.md` |
| D2 | `docs/MANUAL_DO_PROJETO.md:197` | "São 65 testes. Se todos passam, a pipeline está íntegra." São **74** |
| D3 | `docs/MANUAL_DO_PROJETO.md`, mapa de `banco_de_dados/` | "(34 CSVs)" em `eda/`. São **114** em disco, 111 versionados. E "`figuras/` — os 4 PNGs da apresentação": são **17**, em três pastas |
| D4 | 7 documentos × 1 | **Renda × cor/raça:** o Guia, o Manual, o relatório da EDA e o doc. Figueiredo citam **−0,81**, calculado par a par sobre 104.108 setores. Na matriz que a fatorial decompõe (*listwise*, 87.545) o valor é **0,784** — abaixo do limiar de multicolinearidade de 0,80 que o livro fixa. Só o relatório do NB04 registra os dois |
| D5 | `complementos/Resumo_EDA_Central_2026-08.docx` × `scripts/gerar_resumo_eda_central.py` | **O documento entregue não corresponde ao seu gerador.** O regerado tem 1.015 parágrafos contra 943, 25 tabelas contra 21 e 26.784 caracteres de texto contra 17.525 — inclui a frase de procedência, a nota dos municípios instáveis e a explicação do denominador, que faltam no arquivo em circulação. Os dois entraram **no mesmo commit** (`7df66c4`, 02/09) |
| D6 | `banco_de_dados/eda/atualizada/*.csv` | As 16 tabelas da 2ª rodada rotulam a linha como **`renda_media`** medindo **`renda_media_sem_extremo`**. Em `descritivas_globais.csv` a mesma linha vale 4.187,4094 na pasta raiz e 4.185,8124 em `atualizada/`, sem nada no arquivo que explique a diferença — a procedência está só no nome da pasta |
| D7 | `GUIA_DO_PROJETO.md` §9 item 12 × `docs/MANUAL_DO_PROJETO.md` | O Guia declara os "CSVs órfãos" **✅ Resolvido em 20/08/2026**; o Manual, mais recente, ainda avisa que `auditoria_analfabetismo_*`, `cobertura_*`, `saneamento_categorias_*` e `resp_feminino_contagem_*` são órfãos e manda "confirmar a metodologia antes de reusar" |

### ÓRFÃO — não rastreável até código versionado

| # | Onde | O que está errado |
|---|---|---|
| O1 | `scripts/gerar_deck_eda_central.js:618` | **"Spearman entre os dois: 0,459"**, no slide da água canalizada. O valor não existe em nenhuma tabela versionada: `correlacao_spearman.csv` não inclui as variáveis de canalização e `agua_canalizada_global.csv` só traz descritivas. Recalculado, 0,459 é a correlação com **`pct_agua_nao_encanada`** (0,4591) — uma das três variáveis da "trinca", não a trinca. As outras duas dão 0,4802 e 0,4528. O número está certo para um par e é atribuído a três |
| O2 † | `banco_de_dados/eda/README.md` | O README de procedência — criado para encerrar o problema dos CSVs órfãos — cita 51 nomes e cobre 50 dos 61 CSVs da raiz. **Não menciona `atualizada/` nem `fatorial/`**, que somam 53 arquivos. Somando as 8 tabelas `renda_*` da raiz, **61 dos 114 CSVs não têm registro de procedência** |
| O3 † | os três `gerar_deck_*.js` | Cerca de **cem medições digitadas no texto dos slides** — 112 ocorrências no gerador da EDA Central, 23 no do critério de renda, 82 no da fatorial. Limiar de literatura (0,30, 0,50, k=1,5) é legítimo como texto; medição não é. Amostra conferida: "assimetria de 3,42 na água e 3,74 na renda" está correta (3,4167 e 3,7395 em `descritivas_globais.csv`) mas foi digitada, não lida |

### FRÁGIL — está certo hoje e quebra sozinho amanhã

| # | Onde | O que está errado |
|---|---|---|
| F1 | `entrega_orientadora/*.db` e `*.xlsx` | **`git status` não serve como teste de reprodutibilidade para 45 MB de binário.** Os `.db` sempre aparecem modificados após regerar, porque `metadados.gerado_em` carrega a data; o `.xlsx`, por causa de `docProps/core.xml`. As tabelas de dados batem por hash — mas uma mudança real de conteúdo ficaria visualmente idêntica à mudança de data, e treina quem olha a ignorar |
| F2 | `src/ivs_censo/renda.py:186` · `scripts/proporcoes_brasil.py:184` · `scripts/diagnostico_fatorial.py:50` | `df['CD_TIPO'].astype(str).eq('1')` e `df['urbano'].astype(str) == '1'`. Hoje as colunas são inteiras sem nulos e o filtro pega os 19.507 corretos. Um único nulo futuro promove a coluna a `float64`, `astype(str)` passa a devolver `'1.0'`, e o filtro devolve **zero setores sem erro nenhum** |
| F3 | `requirements.txt` | Só declara pisos. Instalado: **pandas 3.0.5**, uma *major* acima do que os próprios comentários do arquivo pressupõem ("pandas >= 2.2: o Notebook 02 usa `groupby().apply(..., include_groups=False)`"). Funciona hoje; nada garante amanhã |
| F4 | `scripts/gerar_resumo_eda_central.py`, `gerar_pdf_outliers_renda.py`, `atualizar_roteiro_2a_rodada.py` | Exigem **`python-docx` e `reportlab`, que não estão no `requirements.txt` nem no `.venv`**. Rodam por `uv run --with`, com versão resolvida na hora. O lado JavaScript está correto: `pptxgenjs` está no `package.json` |
| F5 | `gerar_deck_eda_central.js:386` · `gerar_resumo_eda_central.py:247` | As **fórmulas dos indicadores** (`V00112 … V00118`, `V00001`) são literais digitados. Conferem com `indicadores.py` hoje; se um bloco de numerador mudar no módulo, o deck continua imprimindo o antigo |
| F6 † | `banco_de_dados/eda/fatorial/nb04_escores.csv` | 6,5 MB, uma linha por setor — exatamente a forma que o `.gitignore` exclui pela regra `*_por_setor.csv`. Escapou pelo nome, não por decisão |
| F7 | `entrega_orientadora/Base_*.csv` | 72 MB e 3,5 MB **versionados**, apesar da regra `banco_de_dados/**/Base_*.csv` do `.gitignore` — que não desversiona o que já foi commitado |
| F8 | `scripts/atualizar_roteiro_2a_rodada.py` | Migração de mão única da 1ª para a 2ª rodada, não idempotente por desenho. **Não foi executado nesta auditoria**, e corretamente: rodá-lo de novo corromperia o roteiro escrito à mão. A consequência é que o roteiro em circulação não tem verificação de reprodutibilidade possível |
| F9 † | `docs/Apresentacoes_IVS/` | Dois decks na raiz — `EDA_Central_IVS_2026-09_rev2.pptx` e `Analise_Fatorial_NB04_2026-09.pptx` — contra a regra do próprio README daquela pasta: "A raiz tem um arquivo só, e é de propósito" |

### LACUNA — falta uma verificação que deveria existir

| # | Onde | O que falta |
|---|---|---|
| L1 | `banco_de_dados/eda/atualizada/` | Sem README de procedência, ao contrário de `eda/`. Dezesseis tabelas cuja única marca de origem é o nome da pasta |
| L2 | `tests/` | **Nenhum teste confere que os números dos documentos batem com os CSVs.** Os 74 testes cobrem fórmulas e artefatos; nada cobre a distância entre o que está calculado e o que está escrito — que é onde estão sete dos achados acima |
| L3 † | `tests/test_fatorial.py` | Não há teste que trave o par renda × cor/raça, nem que compare as duas procedências (par a par × *listwise*). D4 passaria despercebido de novo |

**Nenhum ERRO.** Não encontrei número ou conclusão errada. Registro isso como resultado, não
como ausência de esforço: a Fase 3 conferiu cinco contagens-âncora, recalculou `Dados_sig`
do zero, verificou os limites de todas as proporções e reproduziu os dez números do
docstring do sigilo; a Fase 2 reexecutou a pipeline inteira.

---

## O que foi verificado e passou

Para a próxima auditoria não refazer.

**Reprodutibilidade (Fase 2).** 74 testes em 11 s. NB01 (lê 8 GB) byte a byte em 32 s.
NB02 (61 CSVs + 7 PNGs) em 37 s. NB04 (16 CSVs + 5 PNGs, bootstrap de 1.000 reamostragens
com semente fixa) em 79 s. `proporcoes_brasil.py` (468 mil setores) em 6,7 min. Mais
`diagnostico_fatorial.py`, `gerar_tabelas_auditoria.py`, `auditoria_renda.py`,
`eda_atualizada.py`, `eda_central_dados.py`, `dados_criterio_renda.py`,
`gerar_entrega_orientadora.py`. Os três decks reproduzem idênticos em conteúdo (44, 51 e 16
slides). `Criterio_Outliers_Renda.pdf` idêntico. Árvore limpa ao final.

**Dados (Fase 3).** 109.032 na base bruta · 104.108 no recorte urbano elegível · 87.545
completos nas 7 variáveis · 19.507 setores de FCU, 19.452 no recorte — os cinco conferem
contra o banco. `Dados_sig` recalculada por `classificar_dados_sig` coincide nas **109.032
linhas** (OK 106.281 · ZERADO 1.736 · SIGILOSO 1.015, como a §9 do Guia afirma).
Denominador V00001 em todos os indicadores domiciliares; analfabetismo em
`V00901 / (V00900 + V00901)` com `min_count_den=2`. **Nenhuma proporção fora de [0,1] antes
do clipping.** Os dois `.db` são **idênticos célula a célula** aos `.csv` correspondentes
(109.032 × 104 e 5.166 × 104).

**O viés do sigilo, quantificado no docstring de `indicadores.py`, reproduz exatamente:**
30.302 setores com ao menos uma parcela sigilosa na água (29,1%), 29.606 no esgoto, 28.239
no lixo, 24.226 na cor/raça; 0, 1, 0 e 2 com todas sigilosas; 22,6%, 22,1% e 30,5% dos
setores com proporção zero têm ao menos uma parcela sigilosa; média da água 0,0696. Dez
números, dez confirmações.

**Código (Fase 4).** Nenhum caminho absoluto. Nenhuma dependência de diretório de trabalho.
Nenhuma dependência de *locale*. As duas únicas fontes de aleatoriedade (`horn` e
`bootstrap_cargas`) têm semente fixa. Nenhuma comparação de ponto flutuante por igualdade
em `src/`. `classificar_dados_sig` definida **uma só vez**; a regra de outlier de renda vive
em `renda.py` e é importada por `auditoria_renda.py`. Dezessete arquivos importam do módulo
compartilhado. **Nenhum teste decorativo**: os 59 testes têm verificação real.

**Interpretações (Fase 5).** A falácia ecológica está declarada nos quatro documentos
analíticos. O relatório da EDA adverte explicitamente contra inferência sobre indivíduos
(§ com Lima-Costa & Barreto, 2003). A ressalva de tamanho amostral do Bartlett está no
relatório do NB04, citando a p. 43 do livro. Não encontrei passagem que escorregue para
leitura individual nem verbo que afirme mais do que a evidência sustenta.

---

## O que não consegui verificar

1. **A camada fatorial, com independência.** Eu a escrevi. Verifiquei por execução e por
   reprodução dos CSVs de agosto, mas não posso ser o revisor independente dela.
2. **`atualizar_roteiro_2a_rodada.py`** — não executável sem risco (F8). O roteiro em
   circulação ficou sem conferência.
3. **A correção das fórmulas de álgebra linear contra a literatura**, item que o próprio
   prompt pede. Conferi promax, eixo principal e escores contra Hendrickson & White (1964) e
   contra o livro da Enap ao escrevê-las, e os testes checam propriedades algébricas — mas
   uma conferência contra uma implementação independente (`psych` em R) **não foi feita**.
   É o teste mais forte disponível e está documentado em
   [`Codigo_Analise_Fatorial_Comentado.md`](Codigo_Analise_Fatorial_Comentado.md); ninguém
   rodou.
4. **Os `.docx` e `.pdf` em `complementos/`** além do resumo e do critério de renda — não
   têm gerador reexecutável ou não foram abertos.
5. **A conformidade das 104 colunas da entrega com o dicionário oficial do IBGE.** A
   auditoria de maio cobriu isso (§3 do relatório de integridade) e eu não a refiz.

---

## Opinião, não achado

Separado de propósito: discordância sobre decisão declarada e justificada não é defeito.

- **A `renda_media_sem_extremo` convive com a `renda_media` em duas pastas paralelas.** A
  decisão está declarada e a 2ª rodada mediu a diferença. Mas duas árvores de tabelas com
  os mesmos nomes é um desenho que cobra atenção para sempre; uma coluna de cenário dentro
  de cada arquivo cobraria menos.
- **Versionar os `.db` de 45 MB** dá reprodutibilidade de entrega ao custo de um repositório
  que cresce a cada regeração. É escolha legítima, e F1 é o preço dela.
- **O `.gitignore` exclui `*_por_setor.csv` por tamanho, mas o projeto versiona
  `Base_*.csv` de 72 MB.** A regra e a prática apontam para lados opostos; qual das duas
  vale é decisão sua, não achado meu.
