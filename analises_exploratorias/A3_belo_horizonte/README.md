# A3_belo_horizonte

**O que muda em relação à referência:** A base é a de **Belo Horizonte** (`Base_BeloHorizonte_Censo2022.db`); fatorial, pesos e faixas calculados só com a cidade. Todos os blocos. **Não elegível** pelos critérios do NB05 (banheiro graduado com comunalidade e carga baixas) — registrado como falha.

**n:** o funil está em `tabelas/T01_funil.csv` (recorte e amostra do índice).

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/A3_belo_horizonte
node scripts/gerar_deck_versao.js analises_exploratorias/A3_belo_horizonte
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/A3_belo_horizonte
```

Arquivos: `config.json`, `textos.json`, `tabelas/`, `figuras/`, `catalogo.csv`,
`setores_indice.csv` e `A3_belo_horizonte.pptx`.
