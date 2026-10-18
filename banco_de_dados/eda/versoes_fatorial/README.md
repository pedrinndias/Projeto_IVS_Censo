# As 108 versões da análise fatorial

Gerado por `scripts/versoes_fatorial.py` (08/10/2026). A lista das versões está em
`versoes_fatorial/VERSOES.md`, e as leituras adotadas em `versoes_fatorial/INTERPRETACAO.md`.

**Eixos:**
- renda (original · sem extremo · com mediana);
- lixo (com · sem);
- água canalizada, somada à água inadequada (nenhuma · não chega · sem canalização);
- banheiro (fora · V00495 · graduado);
- moradia não convencional (sem · com).

**Método fixo:** o da referência proposta do NB05 (promax, pesos 60/40, normalização municipal,
2 fatores), com as funções de `scripts/ivs_especificacoes.py` e `scripts/fatorial_ampliada.py`,
importadas sem edição.

**Amostras:**
- **Própria:** a de cada versão, com exclusão por lista nas variáveis dela.
- **Comum:** a dos setores com as variáveis de todas as versões. Vale para a AUC comum, o
  Spearman e a mudança de faixa contra a V023, e para os pares por eixo.

**Trava:** as 18 versões sem água canalizada e sem moradia têm de bater com
`../ivs_especificacoes/especificacoes.csv` (linha `…·promax·60_40·municipal`) em n, KMO, MSA
mínimo, fatores, peso de F1, AUC e elegibilidade; se não baterem, nada é gravado.

| Arquivo | Conteúdo |
|---|---|
| `versoes.csv` | Uma linha por versão: eixos, variáveis, n (própria e comum), KMO, Bartlett, MSA, fatores (Kaiser e Horn), variância, Φ, os 4 critérios e o que falhou, peso de F1, AUC (global e no município, própria e comum), % por faixa do IVS-BH, maior variação de peso (estabilidade), Spearman e mudança de faixa contra a V023 |
| `cargas.csv` | Versão × variável: promax padrão e estrutura (F1 = fator da renda), comunalidade oblíqua, MSA, peso no índice (%), dimensão |
| `pares_por_eixo.csv` | Para cada eixo e troca de nível, os pares de versões que só diferem nele: mediana, mínimo e máximo das diferenças; elegíveis antes e depois |
| `pares_detalhe.csv` | Cada par, uma linha |
| `estabilidade.csv` | Um município de fora por vez (70 rodadas por versão), resumido por versão |
