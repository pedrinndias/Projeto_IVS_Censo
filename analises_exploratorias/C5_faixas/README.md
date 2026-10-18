# C5_faixas

**O que muda em relação à referência:** Só as faixas: o índice é o da referência, classificado também por quartis, quintis, quebras naturais (por município) e agrupamento dos setores pelos componentes. As tabelas T36 a T38 e a figura F30 comparam as regras; os blocos 11 e 12 continuam com a regra do IVS-BH.

Blocos 10, 11, 12.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/C5_faixas
node scripts/gerar_deck_versao.js analises_exploratorias/C5_faixas
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/C5_faixas
```
