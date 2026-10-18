# 00_referencia — a base de comparação

**O que muda em relação à referência:** nada. Recorte da EDA (setores urbanos com
`Dados_sig = OK`, 70 municípios), os 31 indicadores e variantes, e o IVS da referência proposta
no NB05: `original·lixo_sem·banheiro_graduado·promax·60_40·municipal`.

**n:** o funil está em `tabelas/T01_funil.csv` (recorte e amostra do índice).

**Conferência:** a amostra do índice, o valor por setor, as faixas e a AUC municipal batem com
`banco_de_dados/eda/ivs_especificacoes/` (`tests/test_eda_versoes.py`).

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/00_referencia
node scripts/gerar_deck_versao.js analises_exploratorias/00_referencia
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/00_referencia
```

Arquivos: `config.json` (a definição), `textos.json` (pergunta, o que muda, síntese,
limitações), `tabelas/`, `figuras/`, `catalogo.csv` (um item por linha, com o slide),
`setores_indice.csv` (o índice e as faixas por setor) e `00_referencia.pptx`.
