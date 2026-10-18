# C3_normalizacao

**O que muda em relação à referência:** A normalização dos componentes: min-max global (todos os municípios juntos) no lugar de min-max dentro do município. Escore z no município, escore z global, postos percentis no município e o min-max municipal da referência estão na tabela T34. As faixas continuam calculadas dentro de cada município.

Blocos 10, 11, 12, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/C3_normalizacao
node scripts/gerar_deck_versao.js analises_exploratorias/C3_normalizacao
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/C3_normalizacao
```
