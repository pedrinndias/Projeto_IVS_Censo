# D3_indice_moradia

**O que muda em relação à referência:** Um índice só de moradia, sem os componentes da referência: razão de moradores, domicílio improvisado, habitação precária, moradia não convencional e banheiro de uso comum, com pesos pela fatorial (promax, dois fatores). A composição é parâmetro exploratório.

Blocos 9, 10, 11, 12, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/D3_indice_moradia
node scripts/gerar_deck_versao.js analises_exploratorias/D3_indice_moradia
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/D3_indice_moradia
```
