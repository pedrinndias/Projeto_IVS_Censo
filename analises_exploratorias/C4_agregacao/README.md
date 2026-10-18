# C4_agregacao

**O que muda em relação à referência:** A agregação: média geométrica ponderada dos componentes normalizados no lugar da soma ponderada. Como o min-max põe zero no setor de menor valor do município, soma-se 0,01 a cada componente antes do produto (parâmetro exploratório). A soma ponderada da referência está na tabela T34.

Blocos 10, 11, 12, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/C4_agregacao
node scripts/gerar_deck_versao.js analises_exploratorias/C4_agregacao
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/C4_agregacao
```
