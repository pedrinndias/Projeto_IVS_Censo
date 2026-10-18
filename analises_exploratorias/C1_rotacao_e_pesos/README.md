# C1_rotacao_e_pesos

**O que muda em relação à referência:** A rotação: Varimax (fatores independentes) no lugar da promax, com os mesmos pesos 60/40 entre as dimensões. Os outros oito esquemas de rotação e peso — sem rotação, Varimax e promax com soma dos quadrados, comunalidades, 50/50 e a referência — estão na tabela T34.

Blocos 9, 10, 11, 12, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/C1_rotacao_e_pesos
node scripts/gerar_deck_versao.js analises_exploratorias/C1_rotacao_e_pesos
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/C1_rotacao_e_pesos
```
