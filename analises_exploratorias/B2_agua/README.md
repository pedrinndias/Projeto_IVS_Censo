# B2_agua

**O que muda em relação à referência:** O componente de água do índice: a falta de água canalizada entra no lugar da água inadequada. As outras definições (água não chega ao domicílio, água só no terreno) e a água inadequada da referência estão na tabela T34. Os blocos 2 a 7 descrevem só as quatro definições de água.

Blocos 2–7, 9, 10 e 13; as alternativas estão na tabela T34 (`sensibilidade` no `config.json`).

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/B2_agua
node scripts/gerar_deck_versao.js analises_exploratorias/B2_agua
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/B2_agua
```
