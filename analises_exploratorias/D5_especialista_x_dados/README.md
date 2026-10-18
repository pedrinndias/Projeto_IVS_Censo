# D5_especialista_x_dados

**O que muda em relação à referência:** O peso das dimensões vem dos dados (soma dos quadrados das cargas padrão da promax), em vez da regra de especialista do IVS-BH (60% socioeconômica, 40% saneamento). As outras repartições pelos dados (estrutura, comunalidades) e a regra 60/40 da referência estão na tabela T34.

Blocos 10, 11, 12, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/D5_especialista_x_dados
node scripts/gerar_deck_versao.js analises_exploratorias/D5_especialista_x_dados
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/D5_especialista_x_dados
```
