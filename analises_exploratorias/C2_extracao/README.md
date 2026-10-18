# C2_extracao

**O que muda em relação à referência:** O método de extração dos fatores: fatoração do eixo principal no lugar de componentes principais (ACP), com a mesma rotação promax e os mesmos pesos 60/40. A máxima verossimilhança e a ACP da referência estão na tabela T34. Os autovalores para Kaiser e Horn continuam os da ACP. A variância explicada da tabela T19 é a soma das comunalidades do eixo principal, só a variância comum, e por isso fica abaixo da da ACP; as duas não se comparam diretamente.

Blocos 9, 10, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/C2_extracao
node scripts/gerar_deck_versao.js analises_exploratorias/C2_extracao
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/C2_extracao
```
