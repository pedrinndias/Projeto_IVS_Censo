# B5_lixo

**O que muda em relação à referência:** O lixo inadequado volta a ser componente do índice (oito componentes), como no IVS-BH 2012 e no NB04. O índice sem lixo da referência está na tabela T34.

Blocos 9, 10, 13; as alternativas estão na tabela T34.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/B5_lixo
node scripts/gerar_deck_versao.js analises_exploratorias/B5_lixo
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/B5_lixo
```
