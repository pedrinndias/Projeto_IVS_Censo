# C6_pesos_iguais

**O que muda em relação à referência:** Os pesos: cada componente pesa o mesmo, sem a análise fatorial. A média dos postos percentis no município (também com pesos iguais) e os pesos da fatorial da referência estão na tabela T34.

Blocos 10, 11, 12, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/C6_pesos_iguais
node scripts/gerar_deck_versao.js analises_exploratorias/C6_pesos_iguais
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/C6_pesos_iguais
```
