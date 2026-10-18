# B4_esgoto

**O que muda em relação à referência:** O componente de esgoto do índice: a soma de V00249 a V00253 entra no lugar de V00312 a V00316. Atenção: pelo dicionário oficial do IBGE, V00249–V00253 é tipologia de habitação, não esgoto (Relatório de Integridade do projeto). A versão mostra o efeito de usar a definição descartada; o esgoto da referência está na tabela T34.

Blocos 2–7, 9, 10 e 13; as alternativas estão na tabela T34 (`sensibilidade` no `config.json`).

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/B4_esgoto
node scripts/gerar_deck_versao.js analises_exploratorias/B4_esgoto
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/B4_esgoto
```
