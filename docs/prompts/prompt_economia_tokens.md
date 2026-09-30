# Prompt — uso inteligente de tokens e de modelos no Claude Code

**Para quem executa:** qualquer sessão de Claude Code neste projeto. Cole no início da sessão
ou instale a versão curta (no fim) no `CLAUDE.md`.
**Base:** o que foi **medido** em setembro de 2026, quando o limite de uso foi atingido cinco
vezes.

---

## O que foi medido

- **O custo cresce com o número de turnos, não com o número de arquivos.** Cada chamada de
  ferramenta relê o contexto inteiro. Uma revisão com 8 agentes fez 861 turnos e releu
  **145,5 milhões de tokens** de cache; um único agente, com 227 turnos, releu 41 milhões.
- **Disparar muitos agentes de uma vez não economiza: esgota o limite junto.** Uma tentativa
  com 15 agentes em paralelo gastou 2,3 milhões de tokens e não entregou nada — todos
  caíram no limite antes de terminar.
- **Agentes enxutos custam pouco.** Com teto de chamadas, receita pronta e Sonnet, uma fase
  inteira custou de 100 a 400 mil tokens.
- **Quatro das cinco quedas aconteceram com agentes em Opus:** as duas tentativas da revisão
  geral, que herdaram o modelo da sessão, e o começo de duas fases de método. A quinta, em
  Sonnet, veio depois de horas de uso acumulado. Em Sonnet, com instruções precisas, as
  fases que tinham caído terminaram.
- **Uma conversa longa encarece tudo o que vem depois:** cada passo do agente principal relê
  o histórico inteiro.

---

## 1. Sessão

1. **Uma tarefa por sessão.** Terminou uma fase ou mudou de assunto: grave o estado num
   arquivo e abra uma sessão nova (`/clear`). É a economia mais barata que existe.
2. **Comece lendo só o arquivo de estado** e a seção do prompt da vez — nunca o histórico
   inteiro de um projeto.
3. **Não releia o que já leu.** Anote no estado o que vai reaproveitar.
4. Se a conversa precisar continuar longa, use `/compact` antes de ela ficar pesada.

## 2. Chamadas de ferramenta — a alavanca principal

1. **Uma verificação = um script.** Junte dez checagens num arquivo Python e rode uma vez;
   dez chamadas custam dez releituras do contexto.
2. **Saída sempre truncada** (`| head -60`). Nunca imprima um arquivo inteiro: `.ipynb` se lê
   carregando o JSON e imprimindo só as células necessárias; CSV, com pandas e filtro;
   Markdown longo, com `grep -n` e `sed -n` em intervalos curtos.
3. **`grep` com escopo:** exclua `graphify-out/`, `.venv/`, `node_modules/` e
   `banco_de_dados/`. Um `git grep` sem escopo já desperdiçou chamadas lendo o grafo.
4. **Pergunte ao grafo antes de abrir arquivos:** `graphify query "<pergunta>" --budget 1500`.
5. **Imagens só quando o trabalho é visual**, e uma olhada por entrega — cada captura de
   tela custa caro.
6. **Rode por último o que é pesado** (pipeline de 8 GB, regeração de decks) e só uma vez.

## 3. Modelo — escolher pelo tipo de trabalho

| Trabalho | Modelo | Por quê |
|---|---|---|
| Listar, inventariar, procurar, renomear, formatar | **Haiku** | mecânico; não precisa de raciocínio |
| Implementar com especificação clara; editar documentos; rodar testes | **Sonnet** | executa bem com receita pronta; foi o que terminou as fases |
| Decidir método, revisar raciocínio estatístico, planejar | **Opus** | só onde o julgamento é o produto — e um agente por vez |

- Na sessão principal, troque com `/model` conforme a etapa.
- Em subagentes e workflows, **declare o modelo em cada etapa**; não deixe herdar.
- **Esforço de raciocínio baixo ou médio** para tarefas mecânicas; alto só para método.
- O modo rápido não economiza: é o mesmo Opus, respondendo mais depressa.

## 4. Subagentes e workflows

1. **Só quando eu pedir.** Um agente novo começa do zero e relê o que precisa.
2. **Mas, para trabalho longo, um agente de contexto limpo sai mais barato** do que seguir
   numa conversa principal comprida — prefira isso a estender a conversa.
3. **No máximo 2 a 4 em paralelo**, em ondas retomáveis: se o limite bater, as ondas
   concluídas ficam guardadas.
4. **Cada agente recebe:** teto de chamadas, a regra "ao chegar a 85% do teto, grave o
   estado e pare", e a **receita pronta** — caminhos, intervalos de linha, comandos exatos.
   Agente que explora o repositório estoura o teto.
5. **Sem verificadores em cascata** (um verificador por achado, refutadores por erro). Os
   achados graves são conferidos pelo agente principal com comandos pontuais.
6. **Ponha um teto de tokens no pedido** quando for grande (ex.: "+300k"): o workflow para
   ao atingir.

## 5. O que pesa em toda chamada

- **Skills:** neste projeto, 86 skills estão escondidas do modelo por `skillOverrides` em
  `.claude/settings.json`; continuam chamáveis por `/nome`. Mantenha assim.
- **Conectores e plugins sem uso** (data, finance, productivity) acrescentam ferramentas a
  toda sessão: desligue nas configurações do app.
- **`CLAUDE.md` curto:** tudo o que está nele é relido a cada chamada.

## 6. Resposta

- Relatório de fim de etapa em **no máximo 15–20 linhas**.
- Não repita o que já foi dito; não resuma o que eu acabei de ler.
- Documento e slide saem de script a partir dos dados — nunca reescritos à mão.

## 7. Quando o limite bater

1. Não relance tudo.
2. Veja se ficou alteração pela metade (`git status`) antes de retomar.
3. Retome do ponto em que parou, com cache (workflow com `resumeFromRunId`, ou o estado em
   disco).
4. Se uma fase em Opus cair duas vezes, rode-a em Sonnet com instrução mais precisa.

## 8. Antes de começar qualquer tarefa grande — 30 segundos

- Quantos agentes × quantos turnos cada? Se passar de ~200 turnos no total, divida.
- Qual modelo em cada etapa?
- Onde fica o arquivo de estado?
- Em que pontos o trabalho para e me mostra o resultado?

---

## Versão curta para o `CLAUDE.md`

```markdown
# Economia de tokens e de modelo
- Uma tarefa por sessão; ao mudar de assunto, grave o estado e abra sessão nova.
- Comece lendo só o arquivo de estado; não releia o que já leu.
- Uma verificação = um script; saída truncada (head -60); nunca imprimir arquivo inteiro.
- grep com escopo: fora graphify-out/, .venv/, node_modules/, banco_de_dados/.
- Antes de abrir arquivos: graphify query "<pergunta>" --budget 1500.
- Modelo por tipo: Haiku mecânico; Sonnet execução com receita; Opus só método, um por vez.
- Subagentes só quando eu pedir; no máximo 2–4 em paralelo, em ondas retomáveis; teto de
  chamadas e receita pronta em cada um; sem verificadores em cascata.
- Relatório de etapa em no máximo 15–20 linhas.
- Limite de uso: não relançar tudo; conferir git status; retomar do ponto parado.
```
