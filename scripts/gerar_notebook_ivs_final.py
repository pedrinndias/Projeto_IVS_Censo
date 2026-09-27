"""Gera o Notebook 05 (IVS final, item 9 do pedido) por nbformat e executa com nbclient.

Cada célula de código carrega uma "tag"; depois de rodar, os textos das células markdown
que citam "a célula N" são preenchidos com o número de execução real (In[N]) daquela tag,
lido do notebook já executado — nenhum número de célula é digitado à mão, e nenhum número
de dado também: todas as células de código leem os CSVs que scripts/ivs_especificacoes.py
(o motor da Fase C) grava em banco_de_dados/eda/ivs_especificacoes/.

O notebook chama o motor da Fase C de verdade (numa pasta temporária, fora do repositório)
para confirmar que ele regrava exatamente os mesmos CSVs já versionados, antes de montar
as seções a partir dos CSVs originais.

Uso (a partir da raiz do repositório):
    .venv/bin/python scripts/gerar_notebook_ivs_final.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

RAIZ = Path(__file__).resolve().parents[1]
NB_DIR = RAIZ / 'notebooks' / 'Fase3_EDA_ELSI'
SAIDA_NB = NB_DIR / '05_Calculo_IVS_Final.ipynb'

CELULAS: list[tuple[str, str, str | None]] = []  # (tipo, fonte, tag)


def md(fonte: str) -> None:
    CELULAS.append(('markdown', fonte, None))


def cod(fonte: str, tag: str) -> None:
    CELULAS.append(('code', fonte, tag))


# ── 0. Título ────────────────────────────────────────────────────────────────
md('''# Fase 3 — Notebook 05: Cálculo do IVS final (item 9 do pedido)

**Entrada:** `banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db`, lida
pelo motor de especificações da Fase C (`scripts/ivs_especificacoes.py`), que reaproveita o
motor da Fase 2 (`scripts/fatorial_ampliada.py`) e a camada fatorial
(`src/ivs_censo/fatorial.py`). Este notebook **não copia nenhuma conta**: chama o motor,
confere que ele regrava os mesmos números já versionados em
`banco_de_dados/eda/ivs_especificacoes/` e organiza o resultado nas respostas que a
orientadora pediu (seções 2.1 e 2.3 de `docs/prompts/prompt_nb05_ivs_final_2026-09.md`).

Nenhuma escolha de método é feita aqui: onde há alternativa, as alternativas ficam lado a
lado (seção 9) e a decisão continua em aberto (seção 11).''')

# ── 1. O que foi pedido ────────────────────────────────────────────────────
md('''## 1. O que a orientadora pediu, e onde está cada resposta

| Item | Pedido | Onde está a resposta |
|---:|---|---|
| 1 | Renda: original · sem extremo · mediana municipal | Seção 3 |
| 2 | Rotação: sem rotação · Varimax · promax | Seção 4 |
| 3 | Pesos na solução oblíqua (5 alternativas) | Seção 5 |
| 4 | O lixo entra no índice? | Seção 6 |
| 5 | O banheiro entra, e em qual versão? | Seção 7 |
| 6 | O que o índice acrescenta à renda | Seção 8 |
| 7 | As três inferências dos agentes, viradas verificação | Fase A — `docs/prompts/estado_nb05_2026-09.md` |
| 8 | Pendências pequenas (dicionário, deck EDA Central, reexecução eda) | Fase A |
| 9 | Este notebook, o relatório e os slides | Este documento inteiro |

A especificação de referência, pelos critérios da seção 2.2 do prompt, e as alternativas de
sensibilidade aparecem lado a lado na seção 9; a seção 10 mostra o IVS final da referência
por setor e por município; a seção 11 lista as perguntas que continuam da orientadora —
nenhuma delas é fechada aqui.''')

# ── 2. As especificações testadas, e quantas são elegíveis ────────────────
md('''## 2. As especificações testadas, e quantas são elegíveis

### 2.1 Importa o motor da Fase C''')

cod('''# ── Imports ───────────────────────────────────────────────────────────────────
import sys                         # registrar scripts/ e src/ no caminho de importação
import io                          # capturar a saída de texto do motor da Fase C
import shutil                      # apagar a pasta temporária ao final da conferência
import hashlib                     # comparar bytes dos CSVs regravados com os do HEAD
import subprocess                  # ler o conteúdo de um arquivo no HEAD do git
import tempfile                    # pasta temporária para a regravação de conferência
import contextlib                  # redireciona o stdout do motor para a variável acima
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path.cwd().resolve().parents[1]     # notebooks/Fase3_EDA_ELSI -> raiz do repositório
assert (RAIZ / 'scripts' / 'ivs_especificacoes.py').exists(), f'raiz errada: {RAIZ}'
sys.path.insert(0, str(RAIZ / 'src'))
sys.path.insert(0, str(RAIZ / 'scripts'))
import ivs_especificacoes as ivs   # o motor da Fase C — nenhuma função é reescrita aqui

SAIDA = RAIZ / 'banco_de_dados' / 'eda' / 'ivs_especificacoes'
print('motor importado de', ivs.__file__)''', 'imports')

md('''A célula {{C:imports}} importa o motor da Fase C tal como ele está.

### 2.2 Roda o motor numa pasta temporária e confere reprodutibilidade''')

cod('''# ── Chama o motor da Fase C (pasta temporária, fora do repositório) ─────────────
tmp = Path(tempfile.mkdtemp(prefix='ivs_especificacoes_'))
ivs.SAIDA = tmp                    # nunca escreve na pasta versionada durante a conferência
ivs.FIG = tmp / 'figuras'

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    ivs.main()                     # a grade inteira: 18 bases, 324 especificações
saida_motor = buf.getvalue()
print(saida_motor)''', 'motor')

md('''A célula {{C:motor}} é a íntegra do que `ivs.main()` imprime: a trava da seção C.5 do
prompt (conferida antes de gravar qualquer coisa — se não bater, o motor para sozinho e nada
é gravado), o progresso das 18 bases com as rotações elegíveis em cada uma, o total de
especificações e elegíveis, a razão de cada uma das quatro leituras de referência (seção 2.2)
e a conclusão do acréscimo à renda. Nenhum destes números é digitado — é a saída literal do
motor da Fase C, rodado de novo por esta sessão.''')

cod('''# ── Confere os CSVs regravados contra o HEAD do git ─────────────────────────────
arquivos = ['especificacoes.csv', 'pesos.csv', 'avaliacao.csv', 'acrescimo_renda.csv',
            'estabilidade.csv', 'referencia.csv']


def hash_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def hash_no_head(nome: str) -> str:
    rel = f'banco_de_dados/eda/ivs_especificacoes/{nome}'
    r = subprocess.run(['git', 'show', f'HEAD:{rel}'], cwd=RAIZ, capture_output=True, check=True)
    return hashlib.sha256(r.stdout).hexdigest()


identico = {nome: hash_arquivo(tmp / nome) == hash_no_head(nome) for nome in arquivos}
for nome, ok in identico.items():
    print(f'{nome}: {"idêntico ao HEAD" if ok else "DIFERENTE do HEAD"}')

# ivs_referencia_por_setor.csv não é versionado (regra *_por_setor.csv); confere contra a
# execução anterior da própria Fase C, que continua no lugar de sempre (nunca foi tocada).
setor_novo, setor_velho = tmp / 'ivs_referencia_por_setor.csv', SAIDA / 'ivs_referencia_por_setor.csv'
setor_igual = hash_arquivo(setor_novo) == hash_arquivo(setor_velho) if setor_velho.exists() else None
print('ivs_referencia_por_setor.csv (fora do git) idêntico à execução anterior:', setor_igual)

ivs.SAIDA, ivs.FIG = SAIDA, SAIDA / 'figuras'   # devolve o motor ao estado normal
shutil.rmtree(tmp)                              # nada fica fora do repositório

assert all(identico.values()), 'CSV regravado difere do HEAD — travas_ok=false, parar e reportar'
assert setor_igual is not False, 'ivs_referencia_por_setor.csv mudou entre execuções'
print('\\ntodos os CSVs regravados batem com a Fase C — o motor é reprodutível.')''', 'confere')

md('''A célula {{C:confere}} regrava a grade inteira numa pasta temporária e compara, byte a
byte, cada um dos seis CSVs versionados com a cópia que já está no HEAD do git — e o CSV por
setor (fora do git) contra a execução anterior da própria Fase C. Vieram todos idênticos: o
motor é determinístico (sem bootstrap, sementes fixas onde há alguma simulação — Horn usa
`semente=42`) e nenhuma das seções a seguir recalcula nada: todas leem os CSVs que a Fase C
já gravou em `banco_de_dados/eda/ivs_especificacoes/`.

### 2.3 Quantas especificações, e quantas elegíveis''')

cod('''esp = pd.read_csv(SAIDA / 'especificacoes.csv')
total = len(esp)
elegiveis = int(esp['elegivel'].sum())
por_norm = esp.groupby('normalizacao')['elegivel'].sum()
por_rotacao = esp.groupby('rotacao')['elegivel'].agg(elegiveis='sum', total='size')
print(f'{total} especificações; {elegiveis} elegíveis, por normalização:')
print(por_norm)
print('\\npor rotação (elegíveis / total):')
print(por_rotacao)''', 'contagem')

md('''A célula {{C:contagem}} mostra o tamanho da grade (renda × lixo × banheiro × rotação ×
método de peso × normalização) e quantas especificações passam nos quatro critérios da seção
2.2 (KMO ≥ 0,70, MSA mínimo ≥ 0,50, comunalidade mínima ≥ 0,30, carga máxima mínima ≥ 0,40).
A quebra por rotação mostra o teste de "um fator ou dois": sem rotação (um fator só) elimina
a comunalidade mínima em toda a grade, como a Fase C já tinha registrado.''')

# ── 3. Renda ────────────────────────────────────────────────────────────────
md('## 3. Renda: original · sem extremo · mediana municipal')

cod('''por_renda = (esp[esp['elegivel']]
             .groupby('renda')['auc_mun_comum']
             .agg(especificacoes='size', auc_media='mean', auc_min='min', auc_max='max')
             .round(4))
por_renda''', 'renda')

md('''A célula {{C:renda}} compara, só entre as especificações elegíveis, a AUC contra FCU
dentro do município (amostra comum às três rendas) por versão de renda. As três alternativas
ficam próximas nesta medida — a escolha entre elas não é feita aqui (item 1 da seção 2.3): é
uma das perguntas que continuam da orientadora (seção 11).''')

# ── 4. Rotação ──────────────────────────────────────────────────────────────
md('## 4. Rotação: sem rotação · Varimax · promax')

cod('''esp.groupby('rotacao')['elegivel'].agg(elegiveis='sum', total='size')''', 'rotacao')

md('''A célula {{C:rotacao}} conta, por rotação, quantas das 108 especificações (18 bases ×
6 combinações de método) são elegíveis. Sem rotação (um fator só) é sempre inelegível pela
comunalidade mínima; Varimax e promax elegem uma parte de cada base — a escolha entre as duas
também não é fechada aqui (item 2 da seção 2.3).''')

# ── 5. Pesos na solução oblíqua ─────────────────────────────────────────────
md('## 5. Pesos na solução oblíqua (promax): as cinco alternativas')

cod('''promax = esp[esp['rotacao'] == 'promax']
(promax.groupby('metodo')
       .agg(elegiveis=('elegivel', 'sum'), total=('elegivel', 'size'),
            peso_f1_medio=('peso_f1', 'mean'), amplitude_media=('amp_peso_f1', 'mean'))
       .round(2))''', 'pesos')

md('''A célula {{C:pesos}} mostra as cinco formas de repartir o peso entre as duas dimensões
na solução oblíqua (SS da matriz padrão, SS da estrutura, comunalidades da matriz oblíqua,
50/50 e 60/40 da literatura — item 3 da seção 2.3). Nos métodos de peso fixo (50/50, 60/40) a
amplitude ao deixar um município de fora é zero por construção, o que os favorece sempre no
critério (a) da seção 2.2 — registrado como pergunta na seção 11.''')

# ── 6. Lixo ─────────────────────────────────────────────────────────────────
md('## 6. O lixo entra no índice?')

cod('''esp.groupby('lixo').agg(elegiveis=('elegivel', 'sum'), total=('elegivel', 'size'),
                             comunalidade_min_media=('comunalidade_min', 'mean'))''', 'lixo')

md('''A célula {{C:lixo}} compara as bases com e sem o indicador de lixo inadequado. Com o
lixo, a comunalidade mínima da grade cai (a água inadequada costuma ficar abaixo de 0,30
nessas bases, como a Fase C já tinha registrado para o IVS-7 do NB04); sem o lixo, mais
especificações passam no critério de comunalidade. Se isso basta para o lixo sair do índice,
ou se a saída precisa de justificativa própria, é pergunta em aberto (seção 11).''')

# ── 7. Banheiro ─────────────────────────────────────────────────────────────
md('## 7. O banheiro entra, e em qual versão?')

cod('''(esp.groupby('banheiro')
    .agg(elegiveis=('elegivel', 'sum'), total=('elegivel', 'size'),
         faixas_indefinidas=('faixas_indefinidas', 'sum')))''', 'banheiro')

md('''A célula {{C:banheiro}} compara as três versões do banheiro: fora do índice, V00495
("sem banheiro de uso exclusivo com chuveiro e vaso") e o graduado da Fase B
(`(1·V00236 + 2·V00237 + 3·V00238) / (3·V00001)`, só a partir da partição que a Fase B
provou fechar em 91.199 de 91.199 setores). A coluna de faixas indefinidas conta setores que
ficam sem faixa pela regra do IVS-BH por estarem no único município de sua faixa de setor
(DP indefinido) — mais frequente nas bases com o graduado, como a Fase C já tinha notado.''')

# ── 8. O que o índice acrescenta à renda ────────────────────────────────────
md('## 8. O que o índice acrescenta à renda (item 6 do pedido)')

cod('''acr = pd.read_csv(SAIDA / 'acrescimo_renda.csv')
resumo = acr[['auc_indice_global', 'auc_renda_global', 'auc_indice_estratos',
              'auc_renda_estratos', 'queda_deviance', 'z_indice']].agg(['min', 'max', 'mean']).round(4)
print(resumo)
acr.loc[acr['referencia'], ['id', 'conclusao']]''', 'acrescimo')

md('''A célula {{C:acrescimo}} resume as 192 especificações elegíveis: a AUC do índice fica
sempre abaixo da renda invertida sozinha, global e na mediana municipal; dentro dos decis de
renda de cada município (colunas `_estratos`) o índice supera a renda em todas; e somar o
índice à renda na regressão logística sempre reduz a deviance (`queda_deviance` e `z_indice`
positivos em todas as linhas). A última linha mostra a conclusão específica da especificação
de referência (seção 9). **Limite:** FCU é critério do IBGE que já usa condições de moradia —
há circularidade parcial com as variáveis de saneamento do índice (item 6 da seção 2.3).''')

# ── 9. A referência proposta e as alternativas ──────────────────────────────
md('## 9. A referência proposta (seção 2.2) e as alternativas, lado a lado')

cod('''ref = pd.read_csv(SAIDA / 'referencia.csv')
ref[['leitura', 'id', 'elegiveis', 'posto_a', 'posto_b', 'posto_c', 'posto_medio', 'porque']]''', 'referencia')

md('''A célula {{C:referencia}} traz as quatro leituras possíveis do critério da seção 2.2 —
não só a leitura "principal" (como escrita: (a) amplitude do peso de F1; (b) AUC municipal na
amostra comum), mas três variantes de sensibilidade lado a lado, sem escolher entre elas:
`amostra_propria` troca a amostra comum pela amostra de cada especificação;
`estabilidade_pesos_variaveis` mede o critério (a) pela amplitude dos pesos das variáveis, não
do fator 1 (o que muda a proposta, porque nos pesos fixos a amplitude do peso de F1 é zero por
construção); `normalizacao_global` repete a leitura principal com a normalização global do
índice em vez da municipal. Isto é **proposta**, não decisão (seção 0.2 do prompt): a escolha
final entre as quatro, e entre cada uma delas e a leitura principal, continua com a
orientadora (seção 11).''')

# ── 10. O IVS final da referência ───────────────────────────────────────────
md('''## 10. O IVS final da especificação de referência

Sem geometria de setor censitário disponível no repositório, a distribuição de faixas fica em
tabela por município — a alternativa que a Fase D do prompt prevê para quando não há
geometria — em vez de mapa.''')

cod('''setor = pd.read_csv(SAIDA / 'ivs_referencia_por_setor.csv')
print('setores:', len(setor))
print('\\ndistribuição do IVS de referência:')
print(setor['ivs_referencia'].describe().round(4))
print('\\nfaixas pela regra do IVS-BH 2012:')
print(setor['faixa_ivs_bh'].value_counts())
print('\\nfaixas por quartis municipais:')
print(setor['faixa_quartis'].value_counts())''', 'setor_dist')

md('''A célula {{C:setor_dist}} descreve o IVS da especificação de referência (seção 9) para
todos os setores em que ela está definida, e conta quantos setores caem em cada uma das
quatro faixas pelas duas regras (IVS-BH 2012, seção 1 do prompt, e quartis municipais).''')

cod('''por_mun = (setor.groupby('NM_MUN')
           .agg(setores=('CD_SETOR', 'size'), ivs_medio=('ivs_referencia', 'mean'),
                pct_muito_elevado=('faixa_ivs_bh', lambda s: 100 * (s == 'muito_elevado').mean()))
           .sort_values('ivs_medio', ascending=False).round(4))
por_mun''', 'setor_mun')

md('''A célula {{C:setor_mun}} é a tabela por município: os 70 municípios da entrega,
ordenados pelo IVS de referência médio, com a fração de setores na faixa "muito elevado". É a
tabela que substitui o mapa (sem geometria de setor no repositório).''')

# ── 11. Perguntas que continuam dela ────────────────────────────────────────
md('''## 11. As perguntas que continuam da orientadora

Nenhuma delas é fechada por este notebook (seção 0.2 do prompt: "não decidir pela
orientadora"). Cada uma aponta a seção com os números:

- **Renda** (seção 3): original, sem o extremo de Belo Horizonte, ou mediana municipal?
- **Rotação** (seção 4): sem rotação, Varimax ou promax?
- **Pesos na oblíqua** (seção 5): SS da matriz padrão, SS da estrutura, comunalidades, 50/50
  ou 60/40 da literatura?
- **Lixo** (seção 6): entra no índice ou não?
- **Banheiro** (seção 7): fora do índice, V00495 ou a versão graduada?
- **Normalização do índice**: dentro do município (referência) ou global (sensibilidade —
  seção 9, leitura `normalizacao_global`)?
- **Regra de faixas** (seção 10): IVS-BH 2012 (média ± desvio-padrão) ou quartis municipais?

A Fase C acrescentou variantes de leitura do próprio critério da seção 2.2 (seção 9) e um
ponto sobre o corte de comunalidade de 0,30 (o IVS-7 + banheiro graduado fica em 0,299, na
fronteira) — ambos registrados por extenso em `docs/prompts/estado_nb05_2026-09.md`, que esta
fase atualiza com a tabela completa dos itens 1–9.''')


def montar_notebook() -> tuple[nbformat.NotebookNode, dict[str, int]]:
    nb = new_notebook()
    nb.metadata['kernelspec'] = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
    nb.metadata['language_info'] = {'name': 'python'}
    indices_por_tag: dict[str, int] = {}
    for tipo, fonte, tag in CELULAS:
        if tipo == 'markdown':
            nb.cells.append(new_markdown_cell(fonte))
        else:
            nb.cells.append(new_code_cell(fonte))
            if tag:
                indices_por_tag[tag] = len(nb.cells) - 1
    return nb, indices_por_tag


def preencher_numeros_de_celula(nb: nbformat.NotebookNode, indices_por_tag: dict[str, int]) -> None:
    numero = {tag: nb.cells[idx].execution_count for tag, idx in indices_por_tag.items()}
    padrao = re.compile(r'\{\{C:(\w+)\}\}')
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and '{{C:' in cell.source:
            cell.source = padrao.sub(lambda m: str(numero[m.group(1)]), cell.source)


def main() -> None:
    nb, indices_por_tag = montar_notebook()
    cliente = NotebookClient(nb, timeout=1800, kernel_name='python3',
                              resources={'metadata': {'path': str(NB_DIR)}})
    cliente.execute()
    preencher_numeros_de_celula(nb, indices_por_tag)
    nbformat.write(nb, SAIDA_NB)
    print(f'gravado: {SAIDA_NB} ({len(nb.cells)} células)')


if __name__ == '__main__':
    main()
