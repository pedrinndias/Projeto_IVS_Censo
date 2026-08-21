# Prompt para atualizar o grafo do graphify

> ## ⚠️ Estado da execução de 10/08/2026 — **parcial**
>
> A atualização foi rodada e **interrompida no meio** por limite de sessão. O que ficou:
>
> | | Situação |
> |---|---|
> | Código (`src/`, `scripts/`, testes) | ✅ indexado — 113 nós de AST |
> | As 4 figuras da EDA | ✅ reextraídas sobre o recorte urbano — 66 nós |
> | **Os 16 documentos** | ❌ **pendentes** — o subagente caiu antes de gravar |
>
> O grafo foi de 188 para **316 nós** e de 258 para **496 arestas**. O manifesto **não**
> foi atualizado de propósito, então basta rodar `/graphify . --update` de novo: ele vai
> detectar os pendentes, e o cache já cobre figuras e código (não reprocessa).
>
> **Os documentos ainda estão representados pela versão de julho no grafo** — ou seja, as
> afirmações desatualizadas da tabela da seção 2 abaixo continuam lá. Enquanto a segunda
> parte não rodar, não confie no grafo para números do recorte.


O grafo em `graphify-out/` foi construído em **08/07/2026** e indexou 28 arquivos. Desde
então o projeto mudou bastante: 20 arquivos rastreados foram modificados, 22 são novos, e
várias afirmações que o grafo aprendeu ficaram **factualmente erradas**.

Este documento tem duas partes: o **prompt para colar** numa sessão do Claude Code, e o
**inventário do que mudou**, que serve de referência caso a atualização precise ser
conferida.

---

## Parte 1 — O prompt

> Copie tudo dentro do bloco abaixo e cole numa sessão do Claude Code aberta na raiz do
> projeto.

```
/graphify . --update

Depois de reconstruir, preciso que você trate estes pontos, porque o grafo foi
construído em 08/07/2026 e o projeto mudou desde então.

## 1. Arquivos que nunca foram indexados e precisam entrar

Os dois notebooks da pipeline ativa ficaram de fora da indexação anterior, embora sejam
o coração do projeto. Inclua explicitamente:

- notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb
- notebooks/Fase3_EDA_ELSI/02_Analises_Descritivas.ipynb

Também é a primeira vez que o projeto tem código Python versionado fora de Backup/.
Indexe como código de primeira classe:

- src/ivs_censo/__init__.py, fontes.py, indicadores.py, dicionario.py
- scripts/gerar_tabela_variaveis.py, gerar_entrega_orientadora.py, proporcoes_brasil.py
- tests/test_ivs_censo.py

E os documentos novos:

- docs/MANUAL_DO_PROJETO.md
- banco_de_dados/nacional/README.md

## 2. Fatos que mudaram — o grafo aprendeu a versão antiga

Trate estes como correções, não como informação nova. Onde houver conflito entre o que
o grafo já afirma e o que está abaixo, o correto é o de baixo:

| Assunto | O grafo aprendeu | O correto agora |
|---|---|---|
| Recorte de análise | 106.281 setores elegíveis | 104.108 setores urbanos elegíveis |
| Filtro rural | não existia | aplicado no NB02, seção 3b, não na extração |
| Dados_sig | 2.751 SIGILOSO, 0 ZERADO | 1.015 SIGILOSO, 1.736 ZERADO (ordem da regra corrigida) |
| Colunas da base bruta | 58 | 68 |
| Colunas do pacote de entrega | 55 | 95 |
| Indicadores calculados | 7 | 23 |
| Testes | 16 | 43 |
| Índice de envelhecimento | 60+ dividido por crianças de 0 a 4 anos | 60+ dividido por menores de 15 anos |
| Entregáveis .db | gerados por script não versionado | gerados por scripts/gerar_entrega_orientadora.py |
| Relatório da EDA | descrevia o recorte com rurais | reescrito sobre o recorte urbano |

## 3. Conceitos que devem existir como nós depois da atualização

- Recorte urbano (SITUACAO Urbana, CD_SIT 1 a 3) e sua tabela de conferência
- Favela e Comunidade Urbana: CD_TIPO, CD_FCU, NM_FCU, e os 19.507 setores do recorte
- Indicadores de envelhecimento: IEP, RDI, percentual de 60 anos ou mais, e o motivo de
  a Longevidade ser inviável nos agregados por setor
- Tipo de domicílio: moradia convencional agrupada e pct_apartamento
- O módulo src/ivs_censo como fonte única das fórmulas, e a relação dele com o NB02
- Cálculo nacional e representatividade da amostra ELSI no Brasil
- As sete demandas da orientadora de julho de 2026 como um conjunto

## 4. Referências bibliográficas a incorporar

Dois artigos entraram no projeto e não estão no grafo. Se a extração de PDF estiver
disponível, adicione-os; se não, registre-os como nós de referência a partir do que o
GUIA_DO_PROJETO.md diz sobre eles:

- Galvão, S. M. et al. Envelhecimento populacional em Mato Grosso. Hygeia, v.21, e2106,
  2025. Define IEP, RDI, LI e percentual de 60+. É a fonte do ajuste do índice de
  envelhecimento.
- Lima-Costa, M. F.; Barreto, S. M. Tipos de estudos epidemiológicos. Epidemiol. Serv.
  Saúde, v.12, n.4, 2003. Base da seção de limitações: falácia ecológica, viés de
  sobrevivência e exclusão de institucionalizados.

## 5. Depois de terminar

Rode estas consultas e me mostre o resultado, para eu conferir se o grafo entendeu as
mudanças:

/graphify query "onde e por que o filtro de setores rurais é aplicado?"
/graphify query "quais variáveis do Censo compõem o índice de envelhecimento?"
/graphify query "o que conecta CD_TIPO ao cálculo dos indicadores de vulnerabilidade?"
/graphify explain "src/ivs_censo/indicadores.py"
/graphify path "02_Analises_Descritivas.ipynb" "proporcoes_brasil.py"

Se alguma consulta devolver a informação antiga (por exemplo, 106.281 setores ou o
denominador de 0 a 4 anos), me avise em vez de corrigir por conta própria: quero saber
se sobrou resíduo da versão anterior no grafo.
```

---

## Parte 2 — Inventário do que mudou

### Arquivos indexados que foram modificados

`GUIA_DO_PROJETO.md` · `README.md` · `estrutura_projeto.md` ·
`banco_de_dados/eda/README.md` · `banco_de_dados/entrega_orientadora/README.md` ·
`docs/Relatorio_EDA_Fase3_IVS_ELSI.md` (reescrito) · `docs/Relatorio_Integridade_Projeto.md` ·
`notebooks/Fase3_EDA_ELSI/README.md` · `tests/test_pipeline_fase3.py` ·
as quatro figuras de `banco_de_dados/eda/figuras/` (regeneradas sobre o recorte urbano).

### Arquivos novos

**Código:** `src/ivs_censo/` (4 arquivos) · `scripts/` (3 arquivos) ·
`tests/test_ivs_censo.py`

**Documentação:** `docs/MANUAL_DO_PROJETO.md` ·
`docs/Apresentacoes_IVS/historico/2026-08-09_Andamento_rev2.pptx` ·
`banco_de_dados/nacional/README.md`

**Dados:** 12 CSVs novos em `banco_de_dados/eda/` (favelas, envelhecimento, tipo de
domicílio, exclusão rural) · 6 arquivos em `banco_de_dados/nacional/` ·
`Dicionario_Variaveis_Projeto.csv` e `.xlsx`

### Arquivos que nunca foram indexados

Os dois `.ipynb` da Fase 3. Como o grafo anterior só tinha o `README.md` da pasta, ele
conhece a pipeline por descrição, não pelo código. Corrigir isso é a melhoria mais
relevante desta atualização.

### Comunidades do grafo antigo

O grafo tinha 16 comunidades rotuladas. Estas devem mudar de conteúdo:

| # | Rótulo | Por quê |
|---|---|---|
| 1 | Variáveis-Componente e Decisões Metodológicas | ganha os 16 indicadores complementares |
| 4 | Pipeline de Dados e Histórico do Projeto | ganha `src/` e `scripts/` |
| 5 | Testes da Pipeline (Fase 3) | de 16 para 43 testes, em dois arquivos |
| 6 a 8, 11 | as quatro figuras | regeneradas sobre o recorte urbano |
| 9 | Redação e Saídas da EDA | relatório reescrito, 12 CSVs novos |
| 12 | Regra IQR e Tratamento de Outliers | segue válida, mas agora sobre 104.108 setores |

Devem surgir comunidades novas em torno de favelas/FCU, envelhecimento e cálculo nacional.

### Custo da execução anterior

417 mil tokens de entrada para 28 arquivos. Com os notebooks e o código novo, espere algo
maior. Se quiser reduzir, `--no-viz` pula a geração do HTML.
