"""Definição e cálculo dos indicadores do projeto, em um só lugar.

As fórmulas aqui são as **mesmas** implementadas no Notebook 02 da Fase 3 — este
módulo existe para que elas possam ser aplicadas a qualquer recorte (o Brasil
inteiro, uma UF, um município) sem duplicar código.

Convenções herdadas da pipeline:

* **Sigilo**: o `X` do IBGE vira `NaN`. Somas de numerador usam `min_count=1`: o
  indicador só vira `NaN` quando *todas* as parcelas estão sigilosas.

  **O que isso implica, e é preciso dizer com todas as letras:** quando *algumas* das
  parcelas estão sigilosas e outras não, as sigilosas entram na soma **valendo zero**.
  Num numerador de 7 variáveis como o da água, basta uma delas vir `X` para o setor ser
  medido a menos. Não é caso raro — no recorte urbano elegível:

  | numerador | setores com ≥1 parcela sigilosa | com todas sigilosas |
  |---|---:|---:|
  | água (7 variáveis)      | 30.302 (29,1%) | 0 |
  | esgoto (5 variáveis)    | 29.606 (28,4%) | 1 |
  | lixo (5 variáveis)      | 28.239 (27,1%) | 0 |
  | cor/raça PPI (3 vars)   | 24.226 (23,3%) | 2 |

  O viés é sempre **para baixo** e é limitado, porque o IBGE só sigila contagem pequena:
  supondo que cada `X` valha de 1 a 4 domicílios, a média da água sobe de 0,0696 para
  algo entre 0,0723 e 0,0800 (+3,9% a +14,9%); esgoto +3,2% a +12,5%; lixo +2,0% a +7,9%.

  A alternativa — `min_count` igual ao número de parcelas — trocaria o viés por perda de
  casos: exigir as 7 variáveis da água deixaria 29,1% dos setores sem indicador nenhum.
  Entre subestimar pouco e perder um terço da base, a escolha foi subestimar; mas ela é
  escolha, não neutralidade, e tem que aparecer nas limitações do artigo.

  Consequência prática para a leitura: um setor com `pct_agua_inad == 0` e alguma parcela
  sigilosa **não** é um setor comprovadamente adequado — é um setor sem inadequação
  *medida*. Dos setores que aparecem com zero, têm ao menos uma parcela sigilosa 22,6%
  (água), 22,1% (esgoto) e 30,5% (lixo).
* **Divisão**: `safe_div` devolve `NaN` (não `inf`, não zero) quando o denominador é
  zero ou nulo.
* **Denominador domiciliar padrão**: `V00001` (Domicílios Particulares Permanentes
  Ocupados), equivalente no Censo 2022 ao `V002` do Censo 2010 usado pelo IVS-BH 2012.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


def safe_div(num, den):
    """Divide evitando divisão por zero: onde `den <= 0` ou é nulo, devolve `NaN`."""
    num = np.asarray(num, dtype=float)
    den = np.asarray(den, dtype=float)
    out = np.full(num.shape, np.nan)          # resultado padrão: NaN
    np.divide(num, den, out=out, where=den > 0)  # só divide onde o denominador é positivo
    return out


@dataclass(frozen=True)
class Indicador:
    """Um indicador = numerador / denominador, com metadados para as tabelas."""

    nome: str                                  # nome da coluna gerada
    numerador: list[str]                       # variáveis somadas no numerador
    denominador: list[str]                     # variáveis somadas no denominador ([] = sem denominador)
    descricao: str                             # texto para a tabela de variáveis e o relatório
    dimensao: str                              # 'Saneamento', 'Socioeconômica', 'Morfologia', 'Demografia'
    no_ivs: bool = False                       # entra nos 7 componentes do IVS?
    escala: float = 1.0                        # 100 nos índices expressos por 100 (IEP, RDI)
    limitar_0_1: bool = True                   # aplicar clip em [0, 1] (proporções)
    min_count_den: int = 1                     # exigir TODAS as parcelas do denominador? (2 = sim, no analfabetismo)
    complemento: bool = False                  # devolver 1 - (num/den); ver pct_sem_agua_canalizada


# ─────────────────────────────────────────────────────────────────────────────
# Os 7 componentes do IVS (IVS-BH 2012 adaptado ao Censo 2022)
# ─────────────────────────────────────────────────────────────────────────────
AGUA = ['V00112', 'V00113', 'V00114', 'V00115', 'V00116', 'V00117', 'V00118']
ESGOTO = ['V00312', 'V00313', 'V00314', 'V00315', 'V00316']
# V00398 (lixo em caçamba de serviço de limpeza) é inadequado no IVS-BH 2012 —
# só a coleta porta-a-porta (V00397) conta como adequada. Não remover sem decisão
# metodológica explícita.
LIXO = ['V00398', 'V00399', 'V00400', 'V00401', 'V00402']
RACA_PPI = ['V01318', 'V01320', 'V01321']

INDICADORES_IVS: list[Indicador] = [
    Indicador('pct_agua_inad', AGUA, ['V00001'],
              'Proporção de domicílios com abastecimento de água inadequado ou ausente',
              'Saneamento', no_ivs=True),
    Indicador('pct_esgoto_inad', ESGOTO, ['V00001'],
              'Proporção de domicílios com esgotamento sanitário inadequado ou ausente',
              'Saneamento', no_ivs=True),
    Indicador('pct_lixo_inad', LIXO, ['V00001'],
              'Proporção de domicílios com destino do lixo inadequado ou ausente',
              'Saneamento', no_ivs=True),
    Indicador('razao_moradores', ['V00005', 'V00006'], ['V00001', 'V00002'],
              'Razão de moradores por domicílio (reproduz o V0005 do IBGE)',
              'Socioeconômica', no_ivs=True, limitar_0_1=False),
    Indicador('pct_analfab', ['V00901'], ['V00900', 'V00901'],
              'Taxa de analfabetismo entre pessoas de 15 anos ou mais',
              'Socioeconômica', no_ivs=True, min_count_den=2),
    Indicador('renda_media', ['V06004'], [],
              'Rendimento nominal médio mensal das pessoas responsáveis (R$)',
              'Socioeconômica', no_ivs=True, limitar_0_1=False),
    Indicador('pct_raca_pretpardind', RACA_PPI, ['v0001'],
              'Proporção de pessoas de cor/raça preta, parda ou indígena',
              'Socioeconômica', no_ivs=True),
]

# ─────────────────────────────────────────────────────────────────────────────
# Indicadores complementares (descritivos, fora dos 7 componentes do IVS)
# ─────────────────────────────────────────────────────────────────────────────
PRECARIA = ['V00050', 'V00052', 'V00053', 'V00054', 'V00055', 'V00056', 'V00057', 'V00058']
CONVENCIONAL = ['V00047', 'V00048', 'V00049']
NAO_CONVENCIONAL = ['V00050', 'V00051', 'V00052']
POP_0A14 = ['V01031', 'V01032', 'V01033']
POP_15A59 = ['V01034', 'V01035', 'V01036', 'V01037', 'V01038', 'V01039']
POP_60MAIS = ['V01040', 'V01041']

INDICADORES_COMPLEMENTARES: list[Indicador] = [
    # -- habitação e morfologia --
    Indicador('pct_dom_improv', ['V00002'], ['V00001', 'V00002'],
              'Proporção de domicílios particulares improvisados', 'Morfologia'),
    Indicador('pct_hab_precaria', PRECARIA, ['V00001', 'V00002'],
              'Proporção de domicílios em habitação precária (cortiço, estrutura degradada, improvisados)',
              'Morfologia'),
    Indicador('pct_moradia_convencional', CONVENCIONAL, ['V00001'],
              'Proporção de moradias convencionais (casa, casa de vila/condomínio, apartamento)',
              'Morfologia'),
    Indicador('pct_moradia_nao_convencional', NAO_CONVENCIONAL, ['V00001'],
              'Proporção de moradias não convencionais (cortiço, maloca, estrutura degradada)',
              'Morfologia'),
    Indicador('pct_apartamento', ['V00049'], ['V00001'],
              'Proporção de domicílios do tipo apartamento', 'Morfologia'),
    Indicador('pct_casa', ['V00047'], ['V00001'],
              'Proporção de domicílios do tipo casa', 'Morfologia'),
    Indicador('pct_casa_vila_condominio', ['V00048'], ['V00001'],
              'Proporção de domicílios do tipo casa de vila ou em condomínio', 'Morfologia'),
    # -- canalização da água (V00199-V00201, acrescentadas em 21/08/2026) --
    # Eixo distinto do bloco de FONTE da água (V00112-V00118, que entra no IVS): um
    # domicílio pode ter rede geral e mesmo assim receber água só no terreno. Spearman
    # entre os dois é 0,459 — parentes, não gêmeos.
    #
    # Por que o principal usa `complemento` em vez de somar V00200+V00201:
    # as três formam partição de V00001 (conferido: fecham em 100,00% dos 81.270 setores
    # em que as três estão presentes). Mas V00200 e V00201 são contagens pequenas, que o
    # IBGE sigila — juntas deixam 21,9% dos setores sem valor. V00199 é contagem grande e
    # quase nunca é sigilada. Pelo complemento o mesmo número sai com 0,04% de ausentes.
    #
    # RESSALVA: a identidade só é *verificável* onde as três estão presentes. Nos setores
    # com V00200/V00201 sigilosos, usá-la é extrapolação — justificada porque a partição é
    # definida pelo IBGE, mas é suposição, não medição.
    Indicador('pct_sem_agua_canalizada', ['V00199'], ['V00001'],
              'Proporção de domicílios em que a água não chega encanada até dentro do domicílio '
              '(complemento de V00199; equivale a V00200+V00201 sobre V00001)',
              'Saneamento', complemento=True),
    Indicador('pct_agua_nao_encanada', ['V00201'], ['V00001'],
              'Proporção de domicílios em que a água não chega encanada ao domicílio (V00201)',
              'Saneamento'),
    Indicador('pct_agua_so_terreno', ['V00200'], ['V00001'],
              'Proporção de domicílios em que a água chega encanada apenas ao terreno (V00200)',
              'Saneamento'),
    # -- saneamento complementar --
    Indicador('pct_sem_banheiro', ['V00495'], ['V00001'],
              'Proporção de domicílios sem banheiro de uso exclusivo com chuveiro e vaso sanitário',
              'Saneamento'),
    Indicador('pct_sem_banheiro_nem_sanitario', ['V00238'], ['V00001'],
              'Proporção de domicílios sem banheiro nem sanitário', 'Saneamento'),
    # -- sociodemográficos --
    Indicador('pct_resp_feminino', ['V01063'], ['V01062', 'V01063'],
              'Proporção de domicílios com pessoa responsável do sexo feminino', 'Socioeconômica'),
    Indicador('pct_crianca_0a4', ['V01031'], ['v0001'],
              'Proporção de crianças de 0 a 4 anos na população residente', 'Demografia'),
    Indicador('pct_pop_0a14', POP_0A14, ['v0001'],
              'Proporção de pessoas com menos de 15 anos na população residente', 'Demografia'),
    Indicador('pct_idoso_60mais', POP_60MAIS, ['v0001'],
              'Proporção de pessoas de 60 anos ou mais na população residente', 'Demografia'),
    # -- índices de envelhecimento (Galvão et al., Hygeia 2025, Quadro 1) --
    Indicador('iep_setor', POP_60MAIS, POP_0A14,
              'Índice de Envelhecimento Populacional: 60+ por 100 menores de 15 anos',
              'Demografia', escala=100.0, limitar_0_1=False),
    Indicador('rdi_setor', POP_60MAIS, POP_15A59,
              'Razão de Dependência de Idosos: 60+ por 100 pessoas de 15 a 59 anos',
              'Demografia', escala=100.0, limitar_0_1=False),
    Indicador('prop_70mais_entre_60mais', ['V01041'], POP_60MAIS,
              'Proporção de pessoas de 70+ entre os de 60+ (proxy de longevidade; NÃO é o LI, '
              'que exigiria a faixa 75+, inexistente nos agregados por setor)',
              'Demografia', escala=100.0, limitar_0_1=False),
]

TODOS_INDICADORES: list[Indicador] = INDICADORES_IVS + INDICADORES_COMPLEMENTARES

# acesso por nome — usado pelo Notebook 02 para pedir só os indicadores de cada seção
INDICADORES_POR_NOME: dict[str, Indicador] = {ind.nome: ind for ind in TODOS_INDICADORES}

# variável do Censo -> indicadores em que ela aparece (usado na tabela de variáveis)
USO_DAS_VARIAVEIS: dict[str, list[str]] = {}
for _ind in TODOS_INDICADORES:
    for _v in (*_ind.numerador, *_ind.denominador):
        USO_DAS_VARIAVEIS.setdefault(_v, [])
        if _ind.nome not in USO_DAS_VARIAVEIS[_v]:
            USO_DAS_VARIAVEIS[_v].append(_ind.nome)


def calcular_indicadores(df: pd.DataFrame, indicadores: list[Indicador] | None = None,
                        limitar: bool = True) -> pd.DataFrame:
    """Calcula os indicadores pedidos e devolve um DataFrame com uma coluna por indicador.

    Espera `df` já numérico (sigilo convertido em `NaN`). Colunas ausentes são
    ignoradas com aviso — assim dá para calcular só o que o recorte permite.

    `limitar=False` devolve as proporções **sem** o corte em [0, 1]. Serve para
    auditoria: o diagnóstico C1 do Notebook 02 precisa ver o valor bruto para
    detectar proporções impossíveis — se medisse o valor já cortado, nunca acharia
    nenhuma.
    """
    indicadores = indicadores if indicadores is not None else TODOS_INDICADORES
    saida = {}
    for ind in indicadores:
        faltando = [c for c in (*ind.numerador, *ind.denominador) if c not in df.columns]
        if faltando:
            print(f'  [aviso] {ind.nome}: colunas ausentes {faltando} — indicador não calculado')
            continue
        num = df[ind.numerador].sum(axis=1, min_count=1)                   # numerador (NaN só se tudo sigiloso)
        if not ind.denominador:                                            # indicadores diretos (renda_media)
            valores = num.astype(float)
        else:
            den = df[ind.denominador].sum(axis=1, min_count=ind.min_count_den)
            valores = pd.Series(safe_div(num, den) * ind.escala, index=df.index)
        if ind.complemento:
            valores = 1 - valores          # o complemento vem ANTES do clip: cortar depois inverteria o corte
        if ind.limitar_0_1 and limitar:
            valores = valores.clip(lower=0, upper=1)
        saida[ind.nome] = valores
    return pd.DataFrame(saida, index=df.index)


def classificar_dados_sig(df: pd.DataFrame) -> pd.Series:
    """Classifica a elegibilidade de cada setor (regra do `Cálculo IVS2012.docx`).

    Ordem das condições (corrigida em 09/08/2026): população zero é avaliada **antes**
    do sigilo, senão setores sem população (massas d'água) com `V00001` vazio são
    rotulados `SIGILOSO` e inflam a contagem de dados suprimidos.
    """
    cond_zerado = df['v0001'].fillna(-1) == 0                               # setor sem população
    cond_sig = df[['v0001', 'V00001']].isna().any(axis=1)                   # população ou domicílios sigilosos
    cond_col = (df['V00001'].fillna(-1) == 0) & ~cond_zerado                # população só em domicílios coletivos
    return pd.Series(
        np.select([cond_zerado, cond_sig, cond_col],
                  ['ZERADO', 'SIGILOSO', 'COLETIVO'], default='OK'),
        index=df.index, name='Dados_sig',
    )
