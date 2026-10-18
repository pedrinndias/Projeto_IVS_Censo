# A1_com_rurais

**O que muda em relação à referência:** Entram também os setores **rurais** com `Dados_sig = OK` dos 70 municípios (`recorte.urbano = false`). Blocos 1–8, 10 e 13.

**n:** o funil está em `tabelas/T01_funil.csv` (recorte e amostra do índice).

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/A1_com_rurais
node scripts/gerar_deck_versao.js analises_exploratorias/A1_com_rurais
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/A1_com_rurais
```

Arquivos: `config.json`, `textos.json`, `tabelas/`, `figuras/`, `catalogo.csv`,
`setores_indice.csv` e `A1_com_rurais.pptx`.
