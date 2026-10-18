# E1_incerteza

**O que é:** Não é uma versão do índice: cruza as versões elegíveis já geradas (com o índice por setor) e conta, para cada setor da referência, em quantas ele fica em risco elevado ou muito elevado.

**Regenerar** (depois das versões que ela lê):

```bash
./.venv/bin/python scripts/eda_transversais.py analises_exploratorias/E1_incerteza
node scripts/gerar_deck_versao.js analises_exploratorias/E1_incerteza
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/E1_incerteza
```
