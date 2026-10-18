# A4_por_regiao

**O que muda em relação à referência:** os blocos 1–8, 10 e 13 rodados **separadamente em cada uma das cinco regiões** (`recorte.regioes`), uma subpasta por região, cada uma com o seu deck. A fatorial, os pesos e as faixas são recalculados em cada região. Norte, Nordeste e Centro-Oeste **não são elegíveis** pelos critérios do NB05 (registrado como falha).

Subpastas: `centro_oeste/`, `nordeste/`, `norte/`, `sudeste/`, `sul/` — cada uma com `config.json`, `textos.json`,
`tabelas/`, `figuras/`, `catalogo.csv`, `setores_indice.csv` e o deck.

**Regenerar uma subpasta:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/A4_por_regiao/<subpasta>
node scripts/gerar_deck_versao.js analises_exploratorias/A4_por_regiao/<subpasta>
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/A4_por_regiao/<subpasta>
```
