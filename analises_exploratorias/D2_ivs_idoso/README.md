# D2_ivs_idoso

**O que muda em relação à referência:** Três componentes de envelhecimento entram no índice — % de pessoas de 60 anos ou mais, índice de envelhecimento e razão de dependência idosa —, com três fatores e pesos pela fatorial (soma dos quadrados das cargas, promax). A composição é parâmetro exploratório. A mesma composição com dois fatores e a referência estão na tabela T34.

Blocos 8, 9, 10, 11, 12, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/D2_ivs_idoso
node scripts/gerar_deck_versao.js analises_exploratorias/D2_ivs_idoso
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/D2_ivs_idoso
```
