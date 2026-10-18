# A2_piso_populacional

**O que muda em relação à referência:** Só entram setores com pelo menos **50 moradores** (`recorte.piso_pop = 50`, parâmetro exploratório — não é decisão). A tabela T34 repete a versão com piso de 100. Blocos 1–8, 10 e 13.

**n:** o funil está em `tabelas/T01_funil.csv` (recorte e amostra do índice).

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/A2_piso_populacional
node scripts/gerar_deck_versao.js analises_exploratorias/A2_piso_populacional
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/A2_piso_populacional
```

Arquivos: `config.json`, `textos.json`, `tabelas/`, `figuras/`, `catalogo.csv`,
`setores_indice.csv` e `A2_piso_populacional.pptx`.
