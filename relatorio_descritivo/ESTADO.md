# Estado — relatório descritivo do andamento

Prompt: `docs/prompts/prompt_relatorio_descritivo_2026-10.md` ·
Interpretação: `relatorio_descritivo/INTERPRETACAO.md`

## Situação: **lotes 0 a 5 concluídos** — próximas sessões são de correção (lote C)

**09/10/2026.** Entrega à orientadora: `…_v3.pptx` e `…_v3.pdf` (140 slides; C-06 a C-08). Apoio do
Pedro para a reunião: `…_v4_APOIO.pptx` e `.pdf` (295 slides; C-09), gerados por
`dados_apoio_relatorio.py` → `apoio/apoio.json` → `montar_apoio_relatorio.py`; conferência em
`verificar_apoio_relatorio.py` (verde). **A CONFERIR antes da reunião** (o verificador lista): a
resposta sobre ferramentas (P00), DM05 tirado, setor extremo de BH, causa dos faltantes do
analfabetismo, Duque de Caxias, perfil dos setores que saem nos cenários (FC03–FC08), variável que
falha na comunalidade (VP05). Leituras pendentes: Horn (ART024), promax (ART025), ROC/AUC,
matriz padrão × estrutura, formativo × reflexivo (ART020–022).
O histórico abaixo descreve as versões anteriores (v3 de 07/10 = 86 slides gerados; o deck atual
é a edição do Pedro com as partes acrescentadas).

Deck **v3**, 86 slides: A01–A03, DM00–DM15, DS00–DS34, FA00–FA16, FP00–FP13, Z02 (Z01 saiu na
C-02). Sem linha Fonte nos slides; fontes nas notas do apresentador.
Anexo `Relatorio_Descritivo_numeros.xlsx` com as abas Indice_slides, Descritivas,
Por_municipio, Por_regiao e Fatorial. Verificador verde (itens 1–6 e 8).

**Se o Pedro editou o deck à mão:** antes de qualquer regeneração, rode
`./.venv/bin/python scripts/comparar_edicoes_relatorio.py <cópia editada>`. Leve cada linha de
`dados/edicoes_do_pedro.csv` à origem como correção C-NN (seção 5 do prompt) e só então regere.

## Decisões do Pedro

| Leitura | Pergunta | Resposta | Data |
|---|---|---|---|
| — | Layout do piloto | **aprovado** | 07/10/2026 |
| — | Tabelas editáveis no PowerPoint; seguir os lotes 2 a 5 sem parar | **pedido** — tabelas são nativas; `comparar_edicoes_relatorio.py` leva as edições à origem | 07/10/2026 |
| L1 | As 11 demandas de setembro bastam, com os itens do NB05 como desdobramentos? | aguardando (DM13 segue marcado A CONFERIR) | — |
| L3 | A Parte FA usa a referência proposta do NB05 (73.878) ou a fatorial do NB04 (87.545)? Qual delas a orientadora rodou? | aguardando — FA feita com o padrão (NB05); trocar exige só mudar a fonte dos construtores fa* | — |

## Histórico

| Lote | Data | Resultado |
|---|---|---|
| — | 07/10/2026 | Interpretação e estado gravados; nenhum lote executado |
| 0 | 07/10/2026 | Piloto de 8 slides, verificador verde (itens 1–6; item 3 recalculou do .db pct_resp_feminino, iep_setor e pct_agua_nao_encanada); executado na sessão que escreveu o prompt, ~25 chamadas |
| 1 | 07/10/2026 | A03 e DM00–DM15 (DM14 montado a partir das caixas "O que contornamos"; DM15 lido das linhas 28–61 do registro); C-01 (arquivo de origem nos DS); verificador verde, item 8 novo; ~20 chamadas, mesma sessão |
| 2–5 | 07/10/2026 | DS00–DS34, FA00–FA16, FP00–FP13, Z01–Z02, anexo xlsx, READMEs, `comparar_edicoes_relatorio.py`; na folha de contato: escala dobrada do 70+ entre 60+ (já vinha ×100), definição longa do DS22, linhas do NB05 fora de coluna no FP04 e frase do FP01 — corrigidos; verificador verde; execução contínua, a pedido do Pedro |
| C-02 | 07/10/2026 | Fontes fora dos slides (só nas notas), Z01 removido; verificador verde; v3 |
| — | 08/10/2026 | **O Pedro edita o deck principal à mão** (deck no PowerPoint; 4 slides apagados: DM05, DM13, DM15, DS34). `gerar_relatorio_descritivo.js` ganhou trava: recusa sobrescrever o principal se ele difere do último gerado (`dados/gerado.sha256`), salvo `--sobrescrever`; a cópia intocada do último gerado é `dados/ultimo_gerado.pptx`. `comparar_edicoes_relatorio.py` agora casa slides pelo ID e, sem argumento, compara o principal com essa cópia: 19 células e 4 slides apagados registrados em `dados/edicoes_do_pedro.csv`, **não aplicados** — o Pedro ainda está editando |
| C-03 | 08/10/2026 | Análise das edições do Pedro; parte 5 (as 108 versões, VP00–VP14) anexada ao deck editado por `scripts/anexar_versoes_ao_relatorio.py`, em arquivo novo `Relatorio_Descritivo_IVS_2026-10_com_108_versoes.pptx` (97 slides, pé renumerado). O deck do Pedro não mudou. As edições dele seguem fora da origem (`dados_relatorio_descritivo.py`) |
| C-04 | 08/10/2026 | 48 slides novos (DSxx-2, DC00–DC07, FC01–FC09) inseridos no deck editado do Pedro: `Relatorio_Descritivo_IVS_2026-10_com_graficos_e_cenarios.pptx` (140 slides). A origem gera o deck completo (134, v4) só em arquivo temporário; o deck de trabalho do Pedro é o que ele edita |
