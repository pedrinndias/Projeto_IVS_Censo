# E2_estabilidade

**O que é:** Não é uma versão do índice: reestima os pesos da referência 70 vezes, cada vez sem um município, e 1.000 vezes em reamostragens dos setores com reposição (semente 42, parâmetro exploratório), e recalcula o índice de todos os setores com cada conjunto de pesos.

**Regenerar** (~14 min):

```bash
./.venv/bin/python scripts/eda_transversais.py analises_exploratorias/E2_estabilidade
node scripts/gerar_deck_versao.js analises_exploratorias/E2_estabilidade
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/E2_estabilidade
```
