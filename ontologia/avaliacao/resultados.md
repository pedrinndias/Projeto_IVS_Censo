# Avaliação da skill ontologia-dados no banco da entrega à orientadora

Cada rodada usa um agente novo, sem contexto do projeto: ele só pode ler a ontologia
indicada e consultar o banco em modo leitura. O gabarito sai de `gabarito.py`, calculado
pelo código do projeto (`calcular_indicadores`, `classificar_dados_sig`, `SETORES_RENDA_EXCLUIDA`).

| Rodada | Ontologia | Instrução lida primeiro |
|---|---|---|
| Linha de base | `ontologia_base.yaml` (826 linhas): skill antes das melhorias | o YAML |
| Nova | `ontologia_nova.yaml` (973 linhas) + `resumo_nova.md` (73 linhas): skill enriquecida | o resumo |

## Linha de base (skill antes das melhorias)

| Modelo | Acertos (convenção do projeto na Q09) | Acertos (renda original na Q09) | Tokens | Chamadas |
|---|---|---|---|---|
| Sonnet | 12/13 | 13/13 | 104.623 | 4 |
| Haiku | 12/13 | 13/13 | 109.333 | 5 |

Os dois responderam Q09 = 25.030 com `renda_media`. A convenção das análises desde
01/09/2026 é `renda_media_sem_extremo` (25.029), que eu só descobri depois desta rodada; por
isso o placar aparece com as duas leituras.

Lacunas apontadas pelos próprios agentes:
- `media_*` sem o recorte na expressão (só em texto): ao pé da letra, água daria 0,0827, não 0,0696.
- Sem sinônimo para "analisados pelo IVS", "analfabetismo", "idosos", "renda dos responsáveis".
- Nulos não avisados (`pct_analfab` nulo em 22,5% dos setores do recorte em BH).
- Variante de renda sem padrão definido.
- `NM_MUN`: `LIKE 'São Paulo%'` pegaria "São Paulo das Missões".

## Nova (skill enriquecida)

| Modelo | Acertos (convenção do projeto na Q09) | Tokens | Chamadas | vs. linha de base |
|---|---|---|---|---|
| Sonnet | 13/13 | 88.225 | 4 | −16% tokens |
| Haiku | 13/13 | 116.285 | 7 | +6% tokens, +2 chamadas |

Os dois responderam Q09 = 25.029 com `renda_media_sem_extremo`, seguindo a métrica `media_renda`
e o histórico dela. Usaram o recorte `analise` pelo glossário, filtraram município por igualdade
(armadilha de `NM_MUN`) e citaram os 22,5% de nulos de `pct_analfab` em BH.

## Conclusão

- **Acerto:** a única diferença é a Q09, e ela vem de uma convenção que a ontologia nova registra e a
  antiga não. Nas outras 12 perguntas, as duas versões acertam tudo: as perguntas não foram
  difíceis o bastante para separar as versões. Isso é limite da avaliação, não prova de que as
  melhorias são inúteis.
- **Custo:** inconclusivo (−16% no Sonnet, +6% no Haiku), com uma rodada por modelo.
- **Robustez (não medida pelas perguntas):** a expressão das métricas agora dá o número certo
  com os `filtros_obrigatorios`; `checar.py` passou a reprovar coluna inexistente em expressão,
  filtro e recorte, ciclo de substituição e glossário quebrado.
- **MCP (Fase 4):** não construir. O critério era haver erro que regra de texto não evita (filtro
  ignorado, métrica reinventada, tentativa de escrita) e nenhuma das 4 rodadas teve um.

## Para refazer

```bash
PYTHONPATH=src .venv/bin/python ontologia/avaliacao/gabarito.py
uv run --with pyyaml python ~/.claude/skills/ontologia-dados/scripts/checar.py
uv run --with pyyaml python ~/.claude/skills/ontologia-dados/scripts/resumo.py
```
