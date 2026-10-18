# D1_subindices

**O que muda em relação à referência:** Em vez de um índice só, o subíndice socioeconômico: só os componentes do fator socioeconômico (razão de moradores, analfabetismo, renda e cor ou raça), com os pesos da referência renormalizados. O subíndice de saneamento e o índice completo da referência estão na tabela T34.

Blocos 10, 11, 12, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/D1_subindices
node scripts/gerar_deck_versao.js analises_exploratorias/D1_subindices
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/D1_subindices
```
