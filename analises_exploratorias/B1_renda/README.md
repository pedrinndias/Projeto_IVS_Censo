# B1_renda

**O que muda em relação à referência:** O componente de renda do índice: a renda sem o valor extremo de Belo Horizonte entra no lugar da renda original. A renda com o extremo trocado pela mediana do município e a original (referência) estão na tabela T34. Os blocos 2 a 7 descrevem só as três rendas.

Blocos 2–7, 9, 10 e 13; as alternativas estão na tabela T34 (`sensibilidade` no `config.json`).

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/B1_renda
node scripts/gerar_deck_versao.js analises_exploratorias/B1_renda
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/B1_renda
```
