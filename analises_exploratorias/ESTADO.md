# Estado da execução — análises exploratórias por versão

Prompt: `docs/prompts/prompt_analises_exploratorias_versoes_2026-10.md`

## Situação: **todos os lotes executados** (2b a 6 em sequência, a pedido de Pedro, 06/10/2026)

Nada commitado. 39 decks (2.042 slides), 1.212 itens no `Catalogo_Mestre.xlsx`; todos passam
no `verificar_versao.py`; suíte com 111 testes passando. A pasta tem ~310 MB (nenhum arquivo
acima de 50 MB). Pendências: a decisão de Pedro e da orientadora sobre o que vai para o artigo,
e as perguntas de `PERGUNTAS.md`.

## Lotes 2b a 6 (06/10/2026)

- **Lote 4a pulado por pedido de execução automática:** D2 e D4 rodaram com os valores-padrão
  da seção 2.3, rotulados como parâmetro exploratório e registrados em `PERGUNTAS.md`.
- `src/ivs_censo/fatorial.py`: `fatoracao_maxima_verossimilhanca` (EM) e `rodar_cenario(...,
  extracao='acp'|'eixo_principal'|'maxima_verossimilhanca')`, com 2 testes novos.
- Motor (`indice` no config): `k`, `extracao`, `pesos: 'iguais'`, `subindice:
  'socioeconomico'|'saneamento'`, `normalizacao` também `z_municipal|z_global|postos_municipal`,
  `agregacao: 'geometrica'` (deslocamento 0,01). Sem renda ou com k ≠ 2, pesos pela soma dos
  quadrados das cargas (`reparticao`). Config: `faixas_alternativas` (T36–T38, F30),
  `indicadores_derivados` (média de colunas). `kmedias`, `silhueta`, `ordenar_grupos` no motor.
- `scripts/eda_transversais.py` (E1–E6, blocos 14–19, T40–T57, F40–F49);
  `scripts/sintese_versoes.py` (00_sintese, bloco 20, T60–T61, F60–F61; `--catalogo` gera o
  `Catalogo_Mestre.xlsx` — feito aqui, não em `gerar_catalogo_analises.py`).
- Ordem de regeneração completa: versões (motor → deck → verificador) → E1–E6 →
  `sintese_versoes.py` → deck da 00_sintese → `sintese_versoes.py --catalogo`.
- Resultados principais estão em `00_sintese/tabelas/T60_todas_as_versoes.csv`. Não elegíveis:
  A3, A4 Norte/Nordeste/Centro-Oeste, B5, B8, C2, D2, D3, D4 (o banheiro graduado na maior parte).
- Destaques por município nas análises E só entre municípios com ≥ 30 setores.


## Lote 2a (06/10/2026)

- Desenho das versões B: o índice principal usa a variante trocada; as demais variantes (e a
  referência) vão para a T34 via `sensibilidade`, que agora aceita `indice` (ex.: `colunas`,
  `renda`) além de `recorte`. Blocos 2–7 com `indicadores` restritos à família.
- Config ganhou `indicadores_externos` (lista de {nome, rotulo, dimensao, arquivo relativo a
  banco_de_dados/, sep, numerador, denominador, o_que_mede, numerador_curto, denominador_curto});
  o gerador usa esses campos no dicionário.
- B1 renda: as três rendas diferem num setor; ρ 0,9995, 0,2% mudam. B2 água (sem canalizada):
  ρ 0,9503, 13,9% mudam, KMO 0,8019, AUC mun 0,8626. B3 sem banheiro: n 87.545, Kaiser/Horn 1,
  AUC mun 0,7845; variantes 11–14% de troca. B4 esgoto V00249–V00253 (é tipologia de habitação
  pelo dicionário IBGE; versão documenta o efeito): ρ 0,8803, 28,8% mudam, AUC mun 0,7696.
- Os 4 decks (61–62 slides) passam em todas as conferências; 109 testes.


## Lote 1b (06/10/2026)

- Formato escolhido para A4/A5 (Pedro não escolheu; registrado): **uma subpasta por estrato**,
  cada uma uma versão completa (`A4_por_regiao/<norte|nordeste|sudeste|sul|centro_oeste>/`,
  `A5_por_porte/<ate_100_mil|de_100_a_500_mil|mais_de_500_mil>/`). Lote 6 deve ler
  `analises_exploratorias/**/catalogo.csv` (dois níveis).
- Recorte ganhou `regioes` (lista) e `porte` ([mín, máx] de moradores do município, somados
  nos setores da base antes dos filtros; máx `null` = sem teto). Somas conferem: 70 municípios
  e 104.108 setores nas duas estratificações.
- Não elegíveis: Norte (MSA e comunalidade do banheiro graduado), Nordeste (KMO 0,63 e
  banheiro graduado), Centro-Oeste (banheiro graduado). Norte: AUC ~0,60 (Manaus, Belém) e
  31% mudam de faixa. Até 100 mil: nenhum município na AUC municipal.
- A6: `scripts/base_nacional_versoes.py` grava `banco_de_dados/nacional/Base_Brasil_Censo2022.db`
  (468.099 setores; 347.400 urbanos OK; ~2 min de leitura + gravação; no .gitignore). NM_MUN com
  "/UF". Nos 70 municípios reproduz a base da entrega (n e médias da T35 iguais às da 2ª rodada).
  Config ganhou `grupo_descritivo` ('UF' nos blocos 2, 4 e 5) e `comparar_com_70` (T35, bloco 2,
  chave `brasil_x_70`). A6: índice 249.404, KMO 0,7865, elegível, ρ com a referência 0,9983.
- Motor: 'UF' entra em TEXTO (senão vira NaN). Os 9 decks do lote passam em todas as conferências.


Deck piloto aprovado ("Continue", 06/10/2026), sem ajustes pedidos; F26/F27 pequenos e
tamanho > 90 slides seguem como pontos abertos.

## Lote 1a (06/10/2026)

- A1 com rurais: recorte 106.281, índice 75.096; ρ com a referência 0,9961; 3,7% mudam de faixa.
- A2 piso 50: recorte 103.280, índice 73.407; ρ 0,9940; 1,6% mudam; T34 (piso 100) ρ 0,9972.
- A3 Belo Horizonte: recorte 5.113, índice 3.499; ρ 0,9978; **não elegível** (banheiro
  graduado: comunalidade 0,018, carga 0,11); Kaiser 3, Horn 2.
- Motor ganhou `sensibilidade` no config (lista de {rotulo, recorte}) → T34 no bloco 10
  (chave `sensibilidade`, vista no gerador). `PERGUNTAS.md` criado (piso de população).
- Gerador: largura do título com a mesma conta do verificador (margem 0,2 e meio corpo);
  os 4 decks passam em todas as conferências, sem falso positivo.
- Para A4/A5 (estratos por região e por porte): o motor **não tem** chave de estrato; o
  caminho mais simples é uma subpasta-recorte por estrato ou `recorte.municipios` por estrato.
- Modelos de texto com município/região únicos ficam estranhos em A3 (ex.: "vai de X
  (Sudeste) a X (Sudeste)"); não corrigido.

## Lote 0b (06/10/2026)

- `scripts/gerar_deck_versao.js <pasta>` — lê `config.json`, `textos.json` (chaves `pergunta`,
  `o_que_muda`, `sintese`, `limitacoes` [lista]), `catalogo.csv`, `tabelas/` e os modelos;
  grava `<versao>.pptx` e preenche a coluna `slide` do catálogo. **Ordem obrigatória:** motor →
  deck → verificador (o motor regrava o catálogo e apaga os slides).
- Vistas das tabelas em `vista(chave, …)`: só escolhem linhas/colunas, pivotam e formatam;
  tabelas de 70 municípios vão com os 10 maiores e os 10 menores, ou os 16 primeiros, com aviso
  "recorte da tabela". Paginação equilibrada pela altura estimada.
- `scripts/folha_contato.swift <pdf> <png> [colunas] [largura] [páginas]` — folha de contato
  (PDFKit). PDF: `soffice --headless --convert-to pdf --outdir <scratch> <pptx>`.
- `dicionario_extra` em `textos_blocos.json` (as três variantes fora do Quadro).
- Verificador no piloto: tudo ok, exceto 3 slides apontados (19, 74, 83); **vistos e corretos**
  (falso positivo da estimativa de caixa). Ao ver uma página apontada, conferir antes de mexer.
- Pontos abertos para Pedro: 102 slides (acima de 40–90; a referência roda os 13 blocos);
  F26 e F27 (70 municípios numa figura alta) ficam com rótulos pequenos no slide.

## O que existe (lote 0a, 06/10/2026)

- `scripts/eda_versoes.py <pasta>` — motor, blocos 1–13. 00_referencia: 62 itens (33 tabelas,
  29 figuras), ~50 s. Grava `tabelas/`, `figuras/`, `catalogo.csv`, `setores_indice.csv`
  (CD_SETOR, NM_MUN, regiao, is_fcu, v0001, pop_60mais, ivs, faixa_ivs_bh, faixa_quartis;
  faixas 0–3, −1 indefinida). Apaga os CSV/PNG antigos da versão antes de gravar.
- `scripts/verificar_versao.py <pasta> [--sem-pytest]` — pytest, catálogo × arquivos, números
  dos campos × CSV, palavras proibidas; com deck: PDF (soffice) × slides, caixas estouradas e
  figuras fora do slide (estimativa pelo XML), slide do catálogo com o ID no texto.
- `analises_exploratorias/_modelos/textos_blocos.json` — `blocos["1".."13"]` {titulo,
  pergunta, nota} e `itens[chave]` {titulo, como_ler, o_que_mostra, nota}.
- `tests/test_eda_versoes.py` — 6 testes; suíte inteira: **109 passando**.
- `00_referencia/config.json` + saídas. Confere com o NB05: n 73.878, índice por setor
  (|Δ| < 1e-4), faixas, AUC municipal 0,8186 (31 municípios), KMO 0,7807, elegível.

## Contratos (não reler o código para descobrir isto)

- **config.json**: `versao, titulo, pergunta, base` (relativa a `banco_de_dados/`),
  `recorte {urbano, dados_sig, piso_pop, municipios}`, `indicadores` ("todos" ou lista),
  `indice {colunas, renda (original|sem_extremo|mediana_mun), rotacao (sem_rotacao|varimax|promax),
  metodo (unico|ss|ss_padrao|ss_estrutura|comunalidades|50_50|60_40), normalizacao
  (municipal|global)}` ou `null`, `blocos`. Eixos C/D/E (extração, agregação, faixas novas,
  estratos por região/porte) **ainda não têm chave**: o lote que precisar acrescenta no motor.
- **catalogo.csv**: `id, tipo, bloco, chave, titulo, o_que_mostra, arquivo, fonte, campos
  (JSON), slide` — `slide` vazio; o gerador do deck preenche. `titulo` e `o_que_mostra` já
  vêm preenchidos; `chave` aponta para `itens` do textos_blocos (como_ler, nota).
- **IDs fixos**: b1 T01 F01 T02 · b2 T03–T05 · b3 F02–F13 (hist/box/dens × Saneamento,
  Socioeconômica, Morfologia, Demografia) · b4 T06 T07 F14 F15 · b5 T08–T11 F16 · b6 T12–T14
  F17 F18 · b7 T15 F19 · b8 T16–T18 F20 F21 · b9 T19–T22 F22 F23 · b10 T23–T27 F24 F25 ·
  b11 T28 T29 F26 · b12 T30 F27 · b13 T31–T33 F28 F29.
- Tabelas grandes para paginar: T05 (2.170 linhas, longa), T06/T09 (70 × 31), T12/T13
  (31 × 31), T10 (até 310), T27/T28/T30/T31/T33 (70 linhas).

## Ambiente e armadilhas

- Sem scipy: `Series.corr(method='spearman')` quebra; usar `ev.rho` (DataFrame.corr serve).
- `eda/atualizada/descritivas_globais.csv`: `sep=';'`, `utf-8-sig`, e a linha `renda_media` é
  a renda **sem o extremo**.
- Sem python-pptx: o verificador lê o XML do pptx com zipfile.
- Folha de contato (0b): **não há** pdftoppm, ImageMagick nem Quartz no python do sistema;
  há `soffice` e `swift` (PDFKit pode rasterizar as páginas do PDF).
- Faixa "indefinida": 1 setor na referência (município com desvio-padrão indefinido).

## Histórico

| Lote | Data | Resultado |
|---|---|---|
| — | 06/10/2026 | Estado inicial gravado |
| 0a | 06/10/2026 | Motor, verificador, textos-modelo e testes; 00_referencia gerado e conferido |
| 0b | 06/10/2026 | Gerador de deck, folha de contato, deck piloto do 00_referencia (102 slides) |
| 1a | 06/10/2026 | A1 (85 slides), A2 (87), A3 (97, não elegível); T34 de sensibilidade |
| 2b–6 | 06/10/2026 | B5–B8, C1–C6, D1–D5, E1–E6, 00_sintese, Catalogo_Mestre.xlsx, README e X_bloqueadas |
| 2a | 06/10/2026 | B1–B4 (61–62 slides cada); T34 com trocas de componente; indicadores externos |
| 1b | 06/10/2026 | A4 (5 regiões, 82–83 slides; N, NE, CO não elegíveis), A5 (3 portes, 82–85), A6 Brasil (77; base nacional) |
| — | 22/10/2026 | **Regeradas** as 24 versões, E1–E6 e a 00_sintese com os erros da revisão corrigidos (IVS ausente, troca de faixa na amostra comum, E2 com reamostragem de municípios); a C5 volta a gerar T36–T38 e F30; 437 cópias " 2" apagadas. Números antes → depois e pendências em `docs/relatorios/Simplificacao_e_Correcoes_2026-10.md` |
