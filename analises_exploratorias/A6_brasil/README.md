# A6_brasil

**O que muda em relação à referência:** a base é a do **Brasil inteiro** (setores urbanos com
`Dados_sig = OK`), montada por `scripts/base_nacional_versoes.py` em
`banco_de_dados/nacional/Base_Brasil_Censo2022.db` (não versionada; ~10 min). Tabelas por
município dos blocos 2, 4 e 5 agrupadas por UF (`grupo_descritivo`), e a T35 compara a versão com
os 70 municípios (`comparar_com_70`). Blocos 1–7, 9 e 13.

**n:** o funil está em `tabelas/T01_funil.csv`.

**Regenerar:**

```bash
./.venv/bin/python scripts/base_nacional_versoes.py
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/A6_brasil
node scripts/gerar_deck_versao.js analises_exploratorias/A6_brasil
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/A6_brasil
```
