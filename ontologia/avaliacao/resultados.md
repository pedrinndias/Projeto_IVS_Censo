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

## Reavaliação com a ontologia certificada (23/11/2026)

Mesmo protocolo: agente novo, sem contexto do projeto, proibido de abrir `ontologia/avaliacao/`; lê `ontologia/resumo.md`
primeiro e o YAML só por trecho; consulta o banco com `sqlite3 -readonly`. Ontologia: 128/128 itens certificados (commit
`9a30bab`). Diferença de contexto: o projeto agora tem um `CLAUDE.md` com o bloco "Dados", carregado pelos agentes.

| Modelo | Acertos | Tokens | Chamadas | vs. rodada "Nova" (18/11) |
|---|---|---|---|---|
| Sonnet | 13/13 | 73.822 | 3 | −16% tokens (88.225), −1 chamada |
| Haiku | 13/13 | 86.392 | 7 | −26% tokens (116.285), mesmas chamadas |

As respostas batem com `gabarito.json`: Q09 = 25.029 com `renda_media_sem_extremo`, Q12 e Q13 sem dado. Os dois usaram
`is_fcu` em vez de `CD_FCU`, igualdade em `NM_MUN` e o recorte certificado, e citaram as armadilhas de NULL.

O que os agentes apontaram:
- O `resumo.md` só marca certificação em recortes e métricas, não em colunas. O Sonnet não viu que `is_fcu`, `v0001` e `NM_MUN`
  estão certificadas; o Haiku abriu o YAML para ver. A mudança seria no `resumo.py` da skill, fora deste projeto.
- Não há métrica pronta para idosos nem para esgoto por grupo (favela × demais); os agentes compuseram a consulta com a
  coluna e o recorte.
- Para Q12 e Q13, a ausência foi concluída por busca no YAML. A ontologia não lista explicitamente o que o banco não tem.

**Leitura:** o acerto continua 13/13, então as perguntas ainda não separam as versões. Os tokens caíram nos dois modelos, mas é
uma rodada por modelo e com o `CLAUDE.md` novo junto: não dá para atribuir a queda só à certificação.

## Para refazer

```bash
PYTHONPATH=src .venv/bin/python ontologia/avaliacao/gabarito.py
uv run --with pyyaml python ~/.claude/skills/ontologia-dados/scripts/checar.py
uv run --with pyyaml python ~/.claude/skills/ontologia-dados/scripts/resumo.py
```
