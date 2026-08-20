"""Definição e cálculo dos indicadores do projeto, em um só lugar.

As fórmulas aqui são as **mesmas** implementadas no Notebook 02 da Fase 3 — este
módulo existe para que elas possam ser aplicadas a qualquer recorte (o Brasil
inteiro, uma UF, um município) sem duplicar código.

Convenções herdadas da pipeline:

* **Sigilo**: o `X` do IBGE vira `NaN`. Somas de numerador usam `min_count=1`, ou seja,
  só resultam `NaN` quando *todas* as parcelas estão sigilosas — nunca zero silencioso.
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

# variável do Censo -> indicadores em que ela aparece (usado na tabela de variáveis)
USO_DAS_VARIAVEIS: dict[str, list[str]] = {}
for _ind in TODOS_INDICADORES:
    for _v in (*_ind.numerador, *_ind.denominador):
        USO_DAS_VARIAVEIS.setdefault(_v, [])
        if _ind.nome not in USO_DAS_VARIAVEIS[_v]:
            USO_DAS_VARIAVEIS[_v].append(_ind.nome)


def calcular_indicadores(df: pd.DataFrame, indicadores: list[Indicador] | None = None) -> pd.DataFrame:
    """Calcula os indicadores pedidos e devolve um DataFrame com uma coluna por indicador.

    Espera `df` já numérico (sigilo convertido em `NaN`). Colunas ausentes são
    ignoradas com aviso — assim dá para calcular só o que o recorte permite.
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
        if ind.limitar_0_1:
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
