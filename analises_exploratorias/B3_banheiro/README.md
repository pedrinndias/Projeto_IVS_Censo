# B3_banheiro

**O que muda em relação à referência:** O índice sem o componente de banheiro (seis componentes, como no NB04 sem o lixo). V00495 e as três partições (nem banheiro nem sanitário, só sanitário, banheiro de uso comum), cada uma no lugar do banheiro, e o banheiro graduado da referência estão na tabela T34. Os blocos 2 a 7 descrevem só as variáveis de banheiro.

Blocos 2–7, 9, 10 e 13; as alternativas estão na tabela T34 (`sensibilidade` no `config.json`).

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/B3_banheiro
node scripts/gerar_deck_versao.js analises_exploratorias/B3_banheiro
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/B3_banheiro
```
