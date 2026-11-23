# Auditoria da regeração do banco da entrega (23/11/2026)

**O quê:** `scripts/gerar_entrega_orientadora.py` rodado com a correção do D04 (commit `c32b7c9`): números de `metadados` sem
separador de milhar e a chave `setores_excluidos_de_renda_media_sem_extremo` renomeada para
`cd_setor_excluido_de_renda_media_sem_extremo`. Pedido do Pedro em 23/11: regerar e auditar se o código continua estável.
**Como:** cópia dos dois `.db` de 22/10 guardada antes de rodar. Depois, comparação tabela a tabela, suíte de testes completa,
verificadores do projeto e conferências da ontologia.

## Dados

| Verificação | Resultado |
|---|---|
| Regeração | 23 s, exit 0; elegibilidade, recorte e FCU iguais aos de 22/10 (OK 106.281, recorte 104.108, FCU 19.452 no recorte) |
| CSVs (`Base_ELSI_70Municipios`, `Base_BeloHorizonte`) | **byte a byte idênticos** aos versionados (o git não marca mudança) |
| Esquema dos dois `.db` (tabelas, colunas, tipos, índices) | idêntico |
| `setores_censitarios` (109.032 × 108 e 5.166 × 108) | idêntica: valores, NULL, ordem das linhas e das colunas, `typeof` de cada coluna |
| `dicionario_variaveis` (108 × 6) | idêntica |
| `metadados` (16 chaves) | só as mudanças esperadas: `gerado_em` 2026-10-22 → 2026-11-23; 7 números (6 em BH) sem vírgula; chave renomeada |
| Cópias " 2" (iCloud) | nenhuma |

## Código

| Verificação | Resultado |
|---|---|
| `pytest` (suíte inteira) | 1 falha na primeira rodada: `test_coluna_de_renda_sem_o_extremo_de_belo_horizonte` lia a chave pelo nome antigo. O teste foi atualizado para o nome novo (a mudança de nome foi intencional, D04; o valor esperado é o mesmo). Depois: **170/170** |
| `scripts/verificar_versoes_fatorial.py` | itens 1, 2, 3 (refeito do `.db`), 5 e 6 OK. Item 4 FALHA em células dos decks (VP09, VP10, VP11): compara o texto dos `.pptx` com o `numeros.json`, sem ler o banco, e nenhum dos dois está alterado no diretório de trabalho. **Não é efeito da regeração** |
| `scripts/verificar_relatorio_descritivo.py` | `IndexError` ao ler os slides (linha 90), antes do item que lê o banco. Pendência já registrada (C09 da revisão de ponta a ponta de nov/2026). **Não é efeito da regeração** |
| Outros consumidores da pasta da entrega (18 scripts) | leem `setores_censitarios`, `dicionario_variaveis` ou os CSVs, que estão idênticos; ninguém além do teste lia a chave renomeada |
| `ruff` em `gerar_entrega_orientadora.py` | os mesmos 5 avisos de antes da mudança |

## Ontologia

| Verificação | Resultado |
|---|---|
| `perfil.py` regerado | só mudam as amostras de `metadados` (números, data, nome da chave) |
| `checar.py` | 128/128 certificados, sem PROBLEMA |
| `gabarito.py` | o recálculo confere com o banco; `gabarito.json` inalterado |
| 8 métricas e recorte (SQL ao pé da letra) | todos BATEM |
| `metadados.valor` | armadilha reescrita para o banco atual (CAST funciona: 104108); o D04 fica como histórico |

**Conclusão:** o banco regerado tem os mesmos dados de 22/10, e o código continua estável. A única quebra foi o teste que lia o nome
antigo da chave, já corrigido. As duas falhas de verificador são anteriores e vêm dos decks, não do banco.

**Atenção para a orientadora:** o `.db` que ela tem (de 22/10) traz os metadados no formato antigo. Os dados são os mesmos; só a
tabela `metadados` mudou.
