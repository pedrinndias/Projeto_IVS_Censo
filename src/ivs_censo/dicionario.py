"""Tabela de variáveis do projeto: descrição oficial do IBGE + arquivo-fonte.

Atende à demanda da orientadora: *"ajustar tabela para mostrar o que significa cada
variável e a fonte da planilha do censo"*.

As descrições vêm dos dicionários oficiais do IBGE versionados em `dados/`:

* `dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx`
  — abas `Dicionário Básico` (v0001…) e `Dicionário não PCT` (todas as demais);
* `dicionario_de_dados_renda_responsavel_20260508.xlsx` — bloco V060xx.

As colunas de identificação/classificação territorial (`CD_SETOR`, `SITUACAO`,
`CD_SIT`, `CD_TIPO`, `CD_FCU`, `NM_FCU`, …) não constam desses dicionários; para elas
a descrição é do próprio projeto e vem marcada como tal na coluna
`origem_da_descricao`.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .fontes import ARQUIVOS_CENSO, MAPA_VARIAVEL_ARQUIVO
from .indicadores import USO_DAS_VARIAVEIS

DIC_AGREGADOS = 'dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx'
DIC_RENDA = 'dicionario_de_dados_renda_responsavel_20260508.xlsx'

# Colunas de identificação e classificação territorial — ausentes do dicionário oficial.
DESCRICOES_DO_PROJETO: dict[str, str] = {
    'CD_SETOR':  'Geocódigo do setor censitário (15 dígitos): UF(2) + município(5) + distrito, subdistrito e setor',
    # O IBGE escreve o nome da chave de forma diferente em cada arquivo; a pipeline padroniza tudo em CD_SETOR.
    'CD_setor':  'Geocódigo do setor censitário — mesma chave que CD_SETOR, grafada assim neste arquivo do IBGE',
    'setor':     'Geocódigo do setor censitário — mesma chave que CD_SETOR, grafada assim neste arquivo do IBGE',
    'CD_UF':     'Código IBGE da Unidade da Federação (2 primeiros dígitos do CD_SETOR) — derivado pela pipeline',
    'CD_MUN':    'Código IBGE do município (7 primeiros dígitos do CD_SETOR) — derivado pela pipeline',
    'NM_MUN':    'Nome do município',
    'NM_BAIRRO': 'Nome do bairro, quando o setor pertence a um bairro delimitado',
    'SITUACAO':  'Situação do setor: Urbana ou Rural (vazia nos setores de massa d\'água)',
    'CD_SIT':    'Código da situação do setor: 1-3 = urbana; 5-8 = rural; 9 = massa d\'água (população zero)',
    'CD_TIPO':   'Tipo de setor. 1 = Favela e Comunidade Urbana (FCU); 0 = setor não especial; demais códigos = outros setores especiais',
    'CD_FCU':    'Código da Favela ou Comunidade Urbana à qual o setor pertence',
    'NM_FCU':    'Nome da Favela ou Comunidade Urbana à qual o setor pertence',
}

# Variáveis que a pipeline lê mas que não entram em indicador nenhum. Sem esta lista
# elas apareceriam na tabela como "(identificação/auxiliar)", que é falso: são
# contagens do Censo, lidas de propósito, cada uma por um motivo. Dizer o motivo é o
# que impede que a próxima pessoa as remova por parecerem sobra.
USO_AUXILIAR: dict[str, str] = {
    'V06001': '(auditoria da renda) quantas pessoas responsáveis sustentam a média do V06004',
    'V06005': '(auditoria da renda) variância do rendimento; CV = √V06005/V06004 separa '
              'setor rico de setor com poucas declarações enormes',
    'V01042': '(conferência) total de pessoas responsáveis; confere V01062+V01063 e '
              'documenta o denominador ABANDONADO em 22/05/2026 — é contagem de pessoas, não de domicílios',
    'V00236': '(conferência) banheiro de uso comum; completa o bloco de banheiro junto de V00238 e V00495',
}


def carregar_dicionario_oficial(caminho_dados: Path) -> pd.DataFrame:
    """Lê os dois dicionários oficiais do IBGE e devolve `[variavel, tema, descricao]`."""
    caminho_dados = Path(caminho_dados)
    partes = []

    ag = pd.read_excel(caminho_dados / DIC_AGREGADOS, sheet_name='Dicionário Básico')
    partes.append(ag.rename(columns={'Variável': 'variavel', 'Tema': 'tema', 'Descrição': 'descricao'})
                  [['variavel', 'tema', 'descricao']])

    nao_pct = pd.read_excel(caminho_dados / DIC_AGREGADOS, sheet_name='Dicionário não PCT')
    partes.append(nao_pct.rename(columns={'Variável': 'variavel', 'Tema': 'tema', 'Descrição': 'descricao'})
                  [['variavel', 'tema', 'descricao']])

    renda = pd.read_excel(caminho_dados / DIC_RENDA, sheet_name='Dicionário Renda Responsável')
    partes.append(renda.rename(columns={'Variável': 'variavel', 'Tema': 'tema', 'Descrição': 'descricao'})
                  [['variavel', 'tema', 'descricao']])

    dic = pd.concat(partes, ignore_index=True).dropna(subset=['variavel'])
    dic['variavel'] = dic['variavel'].astype(str).str.strip().str.upper()   # chave em caixa alta p/ casar com v0001
    dic['descricao'] = dic['descricao'].astype(str).str.strip()
    return dic.drop_duplicates(subset='variavel', keep='first')


def tabela_variaveis(caminho_dados: Path) -> pd.DataFrame:
    """Monta a tabela final: cada variável usada pelo projeto, o que ela significa,
    de qual arquivo do Censo ela vem e em quais indicadores é usada."""
    dic = carregar_dicionario_oficial(caminho_dados).set_index('variavel')

    linhas = []
    for chave, fonte in ARQUIVOS_CENSO.items():
        for var in fonte.colunas:
            if any(l['variavel'] == var for l in linhas):        # a chave do setor repete entre arquivos
                continue
            oficial = dic.loc[var.upper()] if var.upper() in dic.index else None
            if oficial is not None:
                descricao, tema, origem = oficial['descricao'], oficial['tema'], 'Dicionário oficial IBGE'
            else:
                descricao = DESCRICOES_DO_PROJETO.get(var, '(sem descrição)')
                tema, origem = fonte.tema, 'Documentação do projeto'
            linhas.append({
                'variavel': var,
                'descricao_oficial': descricao,
                'tema_ibge': tema,
                'bloco_do_projeto': fonte.rotulo,
                'arquivo_fonte': fonte.arquivo,
                'chave_do_setor_no_arquivo': fonte.chave,
                'usada_nos_indicadores': (', '.join(USO_DAS_VARIAVEIS.get(var, []))
                                          or USO_AUXILIAR.get(var)
                                          or '(identificação/auxiliar)'),
                'origem_da_descricao': origem,
            })

    tabela = pd.DataFrame(linhas)
    ordem_arquivos = {f.arquivo: i for i, f in enumerate(ARQUIVOS_CENSO.values())}
    return (tabela.assign(_ord=tabela['arquivo_fonte'].map(ordem_arquivos))
            .sort_values(['_ord', 'variavel']).drop(columns='_ord').reset_index(drop=True))
