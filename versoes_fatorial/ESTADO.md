# Estado — as 108 versões da análise fatorial

Prompt: `docs/prompts/prompt_versoes_fatorial_108_2026-10.md` · Interpretação: `INTERPRETACAO.md` ·
Lista: `VERSOES.md`

## Situação: **lotes 0 a 5 concluídos** (08/10/2026, sem parar, a pedido do Pedro) — próximas sessões são de correção

- **Resultados:** `banco_de_dados/eda/versoes_fatorial/`.
  - 108 versões, 24 elegíveis: 3 com lixo e 21 sem; 8 por renda.
  - Estabilidade calculada em todas (70 rodadas cada; ~6 s por versão; rodada inteira, 653 s).
  - Trava contra as 18 do NB05: OK.
- **Decks v1:**
  - `Versoes_Fatorial_Principal.pptx` (16 slides: VP01–VP15, com VP13 em duas partes);
  - `Caderno_Fichas_108.pptx` (110 slides: VF00, VF01, V001–V108).
- **Planilha:** `Versoes_Fatorial_numeros.xlsx`, com as abas Versoes (filtro e colunas de seleção),
  Cargas, Pares_por_eixo, Estabilidade e Indice_slides.
- **Verificação:** verificador verde (1–6); `pytest` com 117 testes, todos passando (3 novos).
- **Se o Pedro editar um deck:** rode `scripts/comparar_edicoes_versoes.py principal|caderno` antes de
  regerar. O gerador recusa sobrescrever deck editado, salvo `--sobrescrever`.

## Decisões do Pedro

| Ponto | Resposta | Data |
|---|---|---|
| 108 fichas (as três rendas) ou 36 | **108 fichas** | 08/10/2026 |
| Não modificar o relatório descritivo | **pedido** — `relatorio_descritivo/` fora do escopo | 08/10/2026 |
| L1 método fixo · L2 amostra · L4 água somada | aguardando (padrão do `INTERPRETACAO.md`) | — |

## Histórico

| Lote | Data | Resultado |
|---|---|---|
| — | 08/10/2026 | Lista, interpretação, estado e prompt gravados; nada rodado |
| 0–5 | 08/10/2026 | Motor, trava, 108 versões com estabilidade, pares por eixo, decks, planilha, READMEs. Na folha de contato: figura de grade pequena (o "contain" do pptxgenjs sem o tamanho original — encaixe calculado à mão), "—" nas trocas de eixo (passou a frase do eixo), "-0,000" (zerado), "comunalidade" estourando a célula da grade e o cabeçalho da ficha — corrigidos. Item 6 do verificador aceitava "não escolhida" como erro — regra ajustada para a negação |
| — | 22/10/2026 | **Dados e CSVs regerados** (108 versões, trava das 18 do NB05 OK) com a troca de faixa refeita na amostra comum. Os decks têm trava e **não** foram regerados: mudaram o principal (VP08–VP13) e 97 fichas do caderno. Lista e valores em `docs/relatorios/Simplificacao_e_Correcoes_2026-10.md` |
