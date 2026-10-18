# Construção — as 108 versões

## Comandos, sempre nesta ordem

```
./.venv/bin/python scripts/versoes_fatorial.py               # ~12 min; resultados em banco_de_dados/eda/versoes_fatorial/
./.venv/bin/python scripts/dados_versoes_fatorial.py         # numeros.json, manifesto, figuras VP05–VP07, xlsx
node scripts/gerar_versoes_fatorial.js                       # os dois decks (trava contra sobrescrita)
./.venv/bin/python scripts/verificar_versoes_fatorial.py     # itens 1–7
./.venv/bin/python -m pytest -q tests/test_versoes_fatorial.py
```

`versoes_fatorial.py --so V023,V010` roda só essas versões, sem gravar nada (serve para medir
tempo e testar).

## Como cada peça nasce

- **Ficha (V001–V108):** `ficha(r)` em `dados_versoes_fatorial.py`; layout `L.ficha` no JS:
  - selo no alto (passa ou o critério que falha; "referência proposta" na V023);
  - três tabelas: A versão, Adequação e Cargas e pesos;
  - a faixa Validação e faixas;
  - duas frases-modelo.
- **Deck principal:** `principal()`. Os slides VP05–VP07 vêm da figura `grade()`, com 6 linhas
  (renda × lixo) e 18 colunas (água × banheiro × moradia). VP08–VP12 vêm de `pares_por_eixo.csv`.
  O VP13 quebra em VP13-2… a cada 16 linhas. O VP14 usa `ie.ordenar` com a maior variação de peso
  de uma variável (o peso de F1 é fixo em 60/40) e a AUC no município.
- **Layout pela forma dos dados:** `kicker` → capa; `cargas` → ficha; `figura` → figura larga;
  `cab` → tabela; senão, blocos de texto.
- **Fontes:** só nas notas (`notas`).
- **Edições à mão:** `scripts/comparar_edicoes_versoes.py principal|caderno [cópia]`.
