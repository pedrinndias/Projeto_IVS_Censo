# E6_tipologias

**O que é:** Não é uma versão do índice: agrupa setores (pelos componentes normalizados no município) e municípios (pelas medianas dos componentes) por k-médias, com o número de grupos indicado pela silhueta entre 3 e 6 (parâmetro exploratório).

**Regenerar** (depois das versões que ela lê):

```bash
./.venv/bin/python scripts/eda_transversais.py analises_exploratorias/E6_tipologias
node scripts/gerar_deck_versao.js analises_exploratorias/E6_tipologias
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/E6_tipologias
```
