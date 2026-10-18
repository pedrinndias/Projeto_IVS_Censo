# D4_ibp_aproximado

**O que muda em relação à referência:** Uma réplica aproximada do Índice Brasileiro de Privação (Allik et al., 2020): três componentes — renda (invertida), analfabetismo e saneamento — padronizados em escore z sobre todos os setores e somados com pesos iguais, sem fatorial. Os componentes são aproximações (parâmetro exploratório): a renda per capita até meio salário mínimo e o analfabetismo de 7 anos ou mais não existem nos agregados por setor de 2022.

Blocos 10, 11, 12, 13.

**Regenerar:**

```bash
./.venv/bin/python scripts/eda_versoes.py analises_exploratorias/D4_ibp_aproximado
node scripts/gerar_deck_versao.js analises_exploratorias/D4_ibp_aproximado
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/D4_ibp_aproximado
```
