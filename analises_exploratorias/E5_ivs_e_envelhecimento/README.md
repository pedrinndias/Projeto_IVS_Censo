# E5_ivs_e_envelhecimento

**O que é:** Não é uma versão do índice: cruza o IVS da referência com os indicadores de envelhecimento por setor (proporção de 60+, índice de envelhecimento, razão de dependência idosa e 70+ entre os 60+).

**Regenerar** (depois das versões que ela lê):

```bash
./.venv/bin/python scripts/eda_transversais.py analises_exploratorias/E5_ivs_e_envelhecimento
node scripts/gerar_deck_versao.js analises_exploratorias/E5_ivs_e_envelhecimento
./.venv/bin/python scripts/verificar_versao.py analises_exploratorias/E5_ivs_e_envelhecimento
```
