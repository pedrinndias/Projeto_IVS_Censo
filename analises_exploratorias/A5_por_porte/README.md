# A5_por_porte

**O que muda em relação à referência:** os blocos 1–8, 10 e 13 rodados **separadamente em cada faixa de porte** do município (`recorte.porte`: até 100 mil, de 100 a 500 mil, mais de 500 mil habitantes — parâmetro exploratório, não é decisão), uma subpasta por faixa, cada uma com o seu deck.

Subpastas: `ate_100_mil/`, `de_100_a_500_mil/`, `mais_de_500_mil/` — cada uma com `config.json`, `textos.json`,
`tabelas/`, `figuras/`, `catalogo.csv`, `setores_indice.csv` e o deck.

**Regenerar uma subpasta:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/A5_por_porte/<subpasta>
node scripts/gerar_deck_versao.js analises_exploratorias/A5_por_porte/<subpasta>
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/A5_por_porte/<subpasta>
```
