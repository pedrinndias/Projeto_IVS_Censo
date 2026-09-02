"""Os 8 arquivos do Censo 2022 e quais variáveis o projeto usa de cada um.

Este módulo é a **fonte única de verdade** sobre a procedência das variáveis: qual
arquivo do IBGE traz cada coluna, qual é o nome da chave do setor naquele arquivo
(o IBGE alterna entre `CD_SETOR`, `CD_setor` e `setor`) e para que serve cada bloco.

É daqui que sai a coluna "arquivo-fonte" da tabela de variáveis pedida pela
orientadora, e é daqui que os scripts sabem o que ler.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class FonteCenso:
    """Um dos arquivos `Agregados_por_setores_*.csv` do Censo 2022."""

    rotulo: str            # nome curto usado nas tabelas e relatórios
    arquivo: str           # nome do arquivo como veio do IBGE
    chave: str             # nome da coluna de código do setor NESTE arquivo
    tema: str              # tema do dicionário oficial do IBGE
    identificacao: list[str] = field(default_factory=list)  # colunas de identificação/classificação (texto)
    variaveis: list[str] = field(default_factory=list)      # variáveis numéricas usadas pelo projeto

    @property
    def colunas(self) -> list[str]:
        """Todas as colunas que o projeto lê deste arquivo, com a chave à frente."""
        return [self.chave, *self.identificacao, *self.variaveis]


# ─────────────────────────────────────────────────────────────────────────────
# Os 8 arquivos, na ordem em que a pipeline os lê.
# ─────────────────────────────────────────────────────────────────────────────
ARQUIVOS_CENSO: dict[str, FonteCenso] = {
    'basico': FonteCenso(
        rotulo='Básico',
        arquivo='Agregados_por_setores_basico_BR_20250417.csv',
        chave='CD_SETOR',
        tema='Básico',
        identificacao=['SITUACAO', 'CD_SIT', 'CD_TIPO', 'CD_FCU', 'NM_FCU',
                       'NM_MUN', 'NM_BAIRRO'],
        variaveis=['v0001'],
    ),
    'dom1': FonteCenso(
        rotulo='Domicílio 1',
        arquivo='Agregados_por_setores_caracteristicas_domicilio1_BR.csv',
        chave='CD_setor',
        tema='Características do Domicílio - Parte 1',
        variaveis=[
            'V00001', 'V00002', 'V00005', 'V00006',                          # denominadores e moradores
            'V00047', 'V00048', 'V00049', 'V00050', 'V00051', 'V00052',      # tipo de espécie (DPPO)
            'V00053', 'V00054', 'V00055', 'V00056', 'V00057', 'V00058',      # tipo de espécie (DPIO)
        ],
    ),
    'dom2': FonteCenso(
        rotulo='Domicílio 2',
        arquivo='Agregados_por_setores_caracteristicas_domicilio2_BR_20250417.csv',
        chave='setor',
        tema='Características do Domicílio - Parte 2',
        variaveis=[
            'V00112', 'V00113', 'V00114', 'V00115', 'V00116', 'V00117', 'V00118',  # água inadequada
            'V00312', 'V00313', 'V00314', 'V00315', 'V00316',                       # esgoto inadequado
            'V00398', 'V00399', 'V00400', 'V00401', 'V00402',                       # lixo inadequado
            'V00236', 'V00238', 'V00495',                                           # banheiro
            # Canalização da água — eixo DIFERENTE do bloco V00112-V00118, que é a
            # *fonte* (poço, rio, carro-pipa). Aqui é a *entrega*: um domicílio pode ter
            # rede geral e ainda assim receber água só no terreno. Acrescentadas em
            # 21/08/2026 a pedido da orientadora. As três formam partição de V00001.
            'V00199', 'V00200', 'V00201',
        ],
    ),
    'alfab': FonteCenso(
        rotulo='Alfabetização',
        arquivo='Agregados_por_setores_alfabetizacao_BR.csv',
        chave='CD_setor',
        tema='Alfabetização',
        variaveis=['V00900', 'V00901'],
    ),
    'raca': FonteCenso(
        rotulo='Cor ou Raça',
        arquivo='Agregados_por_setores_cor_ou_raca_BR.csv',
        chave='CD_SETOR',
        tema='Cor ou Raça',
        variaveis=['V01318', 'V01320', 'V01321'],
    ),
    'renda': FonteCenso(
        rotulo='Renda do Responsável',
        arquivo='Agregados_por_setores_renda_responsavel_BR.csv',
        chave='CD_SETOR',
        tema='Renda do Responsável',
        # V06004 é a média que entra no IVS. V06001 e V06005 não entram em indicador
        # nenhum: existem para AUDITAR o V06004, e foram acrescentadas em 24/08/2026
        # porque sem elas não dá para distinguir "setor rico" de "setor com uma
        # declaração enorme". V06005 é a variância — com ela, CV = √V06005/V06004
        # mostra que os setores de renda absurda têm CV de 5 a 11 contra mediana
        # nacional de 0,78, ou seja, média puxada por poucos casos, e não erro de
        # digitação de fator 100. V06001 dá quantas pessoas sustentam cada média.
        # V06006 (rendimento mediano) está no dicionário do IBGE mas NÃO existe nesta
        # versão do CSV — o cabeçalho tem só V06001 a V06005.
        variaveis=['V06001', 'V06004', 'V06005'],
    ),
    'demog': FonteCenso(
        rotulo='Demografia',
        arquivo='Agregados_por_setores_demografia_BR.csv',
        chave='CD_setor',
        tema='Demografia',
        variaveis=['V01031', 'V01032', 'V01033',                               # menores de 15
                   'V01034', 'V01035', 'V01036', 'V01037', 'V01038', 'V01039',  # 15 a 59
                   'V01040', 'V01041'],                                         # 60 ou mais
    ),
    'parent': FonteCenso(
        rotulo='Parentesco',
        arquivo='Agregados_por_setores_parentesco_BR.csv',
        chave='CD_SETOR',
        tema='Parentesco',
        variaveis=['V01042', 'V01062', 'V01063'],
    ),
}

# variável -> chave do arquivo de origem (ex.: 'V00312' -> 'dom2')
MAPA_VARIAVEL_ARQUIVO: dict[str, str] = {
    var: chave
    for chave, fonte in ARQUIVOS_CENSO.items()
    for var in (*fonte.identificacao, *fonte.variaveis)
}


def colunas_do_arquivo(chave: str) -> list[str]:
    """Colunas que o projeto lê do arquivo identificado por `chave` ('dom2', 'demog'…)."""
    return ARQUIVOS_CENSO[chave].colunas


def encontrar_raiz(inicio: Path | None = None) -> Path:
    """Sobe a árvore de diretórios até achar a raiz do projeto.

    Mesma heurística usada nos notebooks: a raiz é a primeira pasta que tem
    `requirements.txt`, `dados/` e `docs/`.
    """
    atual = (inicio or Path.cwd()).resolve()
    for d in [atual, *atual.parents]:
        if (d / 'requirements.txt').is_file() and (d / 'dados').is_dir() and (d / 'docs').is_dir():
            return d
    raise RuntimeError(f'Raiz do projeto não encontrada a partir de: {atual}')
