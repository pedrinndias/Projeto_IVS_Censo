# Fase 3 — EDA com filtro ELSI-Brasil

Pipeline ativa do projeto. **Aplica pela primeira vez o filtro dos 70 municípios do
ELSI-Brasil** — corrigindo o bloqueante metodológico das Fases 1 e 2 (que processavam o
Brasil inteiro).

## Notebooks

| # | Notebook | O que faz |
|---|---|---|
| 01 | [`01_Extracao_Filtragem_ELSI.ipynb`](01_Extracao_Filtragem_ELSI.ipynb) | Lê os 8 CSVs do Censo 2022, cruza com `dados/municipios_elsi_brasil.csv`, filtra apenas os setores dos 70 municípios e exporta `banco_de_dados/Base_ELSI_Bruta_Censo2022.csv` (109.032 setores × 68 colunas). |
| 02 | [`02_Analises_Descritivas.ipynb`](02_Analises_Descritivas.ipynb) | EDA completa da base filtrada — tipagem e sigilo, elegibilidade (`Dados_sig`), **recorte urbano**, cálculo das 7 proporções (denominador V00001), descritivas globais/por município/por região, variáveis complementares (habitação precária, banheiro, chefia feminina, envelhecimento, tipo de domicílio, favelas), histogramas, boxplots, outliers (IQR), missing e correlações (Pearson + Spearman). Exporta os CSVs e figuras de `banco_de_dados/eda/`. |

## Como usar

Executar na ordem `01 → 02`. O notebook 01 deve rodar uma única vez (ou sempre que a
lista ELSI, os dados-fonte ou o conjunto de colunas extraídas forem atualizados).

Os notebooks são versionados **sem outputs**. Para conferir a execução sem sujar o
`.ipynb`, dá para rodar as células como script.

## Convenções desta fase

- **Filtro ELSI:** chave composta `(uf_codigo, nm_municipio_normalizado)` — necessária
  porque há municípios homônimos em UFs diferentes (ex.: Tabatinga em AM e SP).
- **Recorte de análise:** setores **urbanos** elegíveis (`Dados_sig = OK` e
  `SITUACAO = Urbana`) — 104.108 dos 109.032. O filtro é aplicado no NB02 (seção 3b),
  não na extração: a base bruta guarda todos os setores para auditoria.
- **Sigilo preservado:** o marcador `X` do IBGE é mantido na base bruta. O tratamento
  (substituição/exclusão) é feito a jusante.
- **Encoding:** os CSVs do Censo vêm em encodings mistos (utf-8 e latin1); a função
  `ler_csv_padronizado` testa ambos automaticamente.
- **Filtragem em chunks:** os arquivos grandes (domicílio2 = 747 MB, alfabetização =
  701 MB) são lidos em chunks de 100 mil linhas para conter o uso de RAM.

## Estrutura do Notebook 02

| Seção | Conteúdo |
|---|---|
| 1–3 | Carregamento, tipagem/sigilo, elegibilidade (`Dados_sig`) |
| **3b** | **Recorte urbano** — exclusão dos setores rurais + tabela de conferência |
| 4–4b | As 7 proporções do IVS (denominador V00001) + diagnóstico do esgoto |
| 5–7 | Descritivas globais, por município e por região |
| 7b–7d | Habitação precária · banheiro · pessoa responsável do sexo feminino |
| **7e** | **Envelhecimento** — IEP, RDI e % 60+ (Galvão et al., *Hygeia*, 2025) |
| **7f** | **Tipo de domicílio** — moradias convencionais e indicador de apartamento |
| **7g** | **Vilas e favelas (FCU)** — contagem e comparação de indicadores |
| 8–13 | Histogramas, boxplots, outliers, missing, correlações e exportação |

## Diferenças em relação à Fase 2

| Aspecto | Fase 2 | Fase 3 |
|---|---|---|
| Escopo | Brasil inteiro (~468 mil setores) | 70 municípios ELSI, recorte urbano |
| Filtro de município | Inexistente | `dados/municipios_elsi_brasil.csv` |
| Foco | Cálculo dos indicadores compostos | EDA + futura análise fatorial |
| Cálculo do IVS | Calcula 7 indicadores 0–1 | Calcula as 7 proporções brutas na EDA; índice final pendente (fatorial, Notebooks 03+) |

> O Brasil inteiro voltou ao projeto por outro caminho: `scripts/proporcoes_brasil.py`
> calcula as mesmas proporções para os ~468 mil setores do país, como **linha de base de
> representatividade** da amostra ELSI — não como recorte de análise.
