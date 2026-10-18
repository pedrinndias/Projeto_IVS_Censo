# E3_desigualdade_intramunicipal

**O que é:** Não é uma versão do índice: calcula o Gini do índice dentro de cada município em todas as versões com normalização min-max no município e soma ponderada, e compara níveis e posições.

**Regenerar** (depois das versões que ela lê):

```bash
./.venv/bin/python scripts/eda_transversais.py analises_exploratorias/E3_desigualdade_intramunicipal
node scripts/gerar_deck_versao.js analises_exploratorias/E3_desigualdade_intramunicipal
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/E3_desigualdade_intramunicipal
```
