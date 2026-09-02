"""Testes sanity-check da pipeline Fase 3.

Executar:
    python -m pytest tests/ -v

Estes testes não rodam a pipeline; eles apenas verificam que os artefatos
finais (Base_ELSI_Bruta_Censo2022.csv + CSVs em banco_de_dados/eda/) estão
presentes e com as características esperadas.
"""
from __future__ import annotations          # permite anotações de tipo "adiadas" (ex.: -> pd.DataFrame sem aspas) em Python antigo
from pathlib import Path                     # caminhos como objetos
import pandas as pd                          # leitura dos CSVs a verificar
import pytest                                # framework de testes (asserts, skip, parametrize)

ROOT = Path(__file__).resolve().parents[1]   # raiz do projeto = 1 nível acima da pasta tests/ (parents[1])
BD = ROOT / 'banco_de_dados'                 # pasta de saídas da pipeline
EDA = BD / 'eda'                             # subpasta com os CSVs da EDA

# Conjunto esperado dos 7 indicadores-componente do IVS (usado em vários testes)
ESPERADOS_INDICADORES = {
    'pct_agua_inad', 'pct_esgoto_inad', 'pct_lixo_inad',
    'razao_moradores', 'pct_analfab', 'renda_media', 'pct_raca_pretpardind',
}


def _read(p: Path) -> pd.DataFrame:          # helper: lê um CSV no padrão do projeto
    return pd.read_csv(p, sep=';', encoding='utf-8-sig')  # separador ';' e encoding utf-8-sig (com BOM)


def test_lista_elsi_tem_70_municipios():     # TESTE: a lista oficial tem exatamente 70 municípios e sem nulos nas chaves
    df = pd.read_csv(ROOT / 'dados' / 'municipios_elsi_brasil.csv', sep=';', dtype=str)
    assert len(df) == 70                      # tem que ter 70 linhas
    assert df['nm_municipio'].notna().all()   # nenhum nome de município nulo
    assert df['uf_codigo'].notna().all()      # nenhum código de UF nulo


def test_base_bruta_existe_e_tem_109032_setores():  # TESTE: a base bruta tem 109.032 setores e 70 municípios
    base = BD / 'Base_ELSI_Bruta_Censo2022.csv'
    if not base.exists():                     # a base não é versionada (~17 MB); se não foi gerada localmente...
        pytest.skip(                          # ...pula o teste (não falha) com uma mensagem explicativa
            f'Base bruta não está versionada (~17 MB) e não foi gerada localmente: {base}. '
            'Rode notebooks/Fase3_EDA_ELSI/01_Extracao_Filtragem_ELSI.ipynb antes do teste.'
        )
    df = pd.read_csv(base, sep=';', dtype=str)
    assert len(df) == 109_032, f'Esperado 109.032 setores, obtido {len(df)}'  # contagem exata de setores
    assert df['CD_MUN'].nunique() == 70       # exatamente 70 municípios distintos


def test_descritivas_globais_tem_7_indicadores():  # TESTE: o CSV global lista exatamente os 7 indicadores esperados
    df = _read(EDA / 'descritivas_globais.csv')
    df = df.rename(columns={df.columns[0]: 'variavel'})  # a 1ª coluna (índice exportado) vira 'variavel'
    assert set(df['variavel']) == ESPERADOS_INDICADORES  # o conjunto de variáveis bate com o esperado


def test_descritivas_por_municipio_tem_490_linhas():  # TESTE: 70 municípios × 7 indicadores = 490 linhas
    df = _read(EDA / 'descritivas_por_municipio.csv')
    # 70 municípios × 7 indicadores = 490
    assert len(df) == 490                     # contagem total de linhas
    assert df['NM_MUN'].nunique() == 70       # 70 municípios distintos


def test_descritivas_por_regiao_tem_35_linhas():  # TESTE: 5 regiões × 7 indicadores = 35 linhas
    df = _read(EDA / 'descritivas_por_regiao.csv')
    # 5 regiões × 7 indicadores
    assert len(df) == 35                       # contagem total de linhas
    assert df['regiao'].nunique() == 5         # 5 regiões distintas


def test_correlacoes_simetricas():            # TESTE: as matrizes são quadradas, simétricas e com diagonal = 1
    # Desde ago/2026 a matriz tem 10 variáveis: as 7 do IVS mais idosos 60+, menores de 5
    # e chefia feminina (demanda da orientadora). As 3 são descritivas, não componentes.
    descritivas = {'pct_idoso_60mais', 'pct_crianca_0a4', 'pct_resp_feminino'}
    for f in ['correlacao_pearson.csv', 'correlacao_spearman.csv']:  # testa as duas matrizes
        df = pd.read_csv(EDA / f, sep=';', index_col=0)  # 1ª coluna é o índice (nomes das variáveis)
        assert df.shape[0] == df.shape[1]     # quadrada
        assert set(df.columns) == set(df.index)                      # mesmas variáveis nos dois eixos
        assert ESPERADOS_INDICADORES <= set(df.columns), 'faltou uma componente do IVS'
        assert descritivas <= set(df.columns), 'faltou uma das descritivas pedidas em ago/2026'
        # Diagonal igual a 1
        for c in df.columns:                  # para cada variável...
            assert abs(df.loc[c, c] - 1.0) < 1e-9  # correlação consigo mesma = 1 (tolerância p/ float)
        # Simetria
        for i in df.columns:                  # corr(i, j) deve ser igual a corr(j, i)
            for j in df.columns:
                assert abs(df.loc[i, j] - df.loc[j, i]) < 1e-9  # simetria (tolerância p/ float)


def test_elegibilidade_setores_soma_109032():  # TESTE: a soma das classes Dados_sig devolve os 109.032 setores
    df = _read(EDA / 'elegibilidade_setores.csv')
    df = df.rename(columns={df.columns[0]: 'Dados_sig'})  # 1ª coluna (índice exportado) vira 'Dados_sig'
    assert df['n_setores'].sum() == 109_032   # soma de todas as classes = total de setores


@pytest.mark.parametrize('arquivo', [         # TESTE parametrizado: roda uma vez por arquivo da lista abaixo
    'descritivas_globais.csv',
    'descritivas_por_municipio.csv',
    'descritivas_por_regiao.csv',
    'outliers.csv',
    'missing_por_municipio.csv',
    'correlacao_pearson.csv',
    'correlacao_spearman.csv',
    'elegibilidade_setores.csv',
])
def test_arquivos_eda_existem(arquivo):       # verifica que cada CSV esperado da EDA existe
    assert (EDA / arquivo).exists(), f'Faltando: {arquivo}'


def test_figuras_eda_existem():               # TESTE: as 4 figuras esperadas da EDA existem
    fig_dir = EDA / 'figuras'
    for png in ['histogramas.png', 'boxplots_por_regiao.png',
                'matriz_correlacao.png', 'missing_por_municipio.png']:
        assert (fig_dir / png).exists(), f'Faltando figura: {png}'


# ─────────────────────────────────────────────────────────────────────────────
# Demandas da orientadora (revisão de 09/08/2026)
# ─────────────────────────────────────────────────────────────────────────────

def test_base_bruta_tem_colunas_territoriais_e_pirâmide_etaria():
    """A base do NB01 precisa trazer a classificação territorial (favelas/rural) e as
    faixas de 15 a 59 anos, sem as quais RDI e contagem de FCU não são calculáveis."""
    base = BD / 'Base_ELSI_Bruta_Censo2022.csv'
    if not base.exists():
        pytest.skip(f'Base bruta não versionada e não gerada localmente: {base}')
    cols = set(pd.read_csv(base, sep=';', dtype=str, nrows=1).columns)
    for c in ['CD_SIT', 'CD_TIPO', 'CD_FCU', 'NM_FCU']:        # classificação territorial
        assert c in cols, f'Coluna territorial ausente na base: {c}'
    for n in range(1031, 1042):                                 # V01031 a V01041 (pirâmide completa)
        assert f'V0{n}' in cols, f'Faixa etária ausente na base: V0{n}'


def test_elegibilidade_separa_zerado_de_sigiloso():
    """Setores sem população têm que aparecer como ZERADO, não como SIGILOSO."""
    df = _read(EDA / 'elegibilidade_setores.csv')
    df = df.rename(columns={df.columns[0]: 'Dados_sig'}).set_index('Dados_sig')
    assert 'ZERADO' in df.index, 'Nenhum setor ZERADO — a ordem da regra Dados_sig regrediu?'
    assert df.loc['OK', 'n_setores'] == 106_281                 # o conjunto elegível não muda com a correção
    assert df['n_setores'].sum() == 109_032


@pytest.mark.parametrize('arquivo', [         # artefatos criados pelas seções novas do Notebook 02
    'exclusao_rural_conferencia.csv',                  # 3b — recorte urbano
    'situacao_urbano_rural_total.csv',
    'indicadores_envelhecimento_total.csv',            # 7e — envelhecimento
    'indicadores_envelhecimento_por_regiao.csv',
    'tipo_domicilio_global.csv',                       # 7f — tipo de domicílio
    'tipo_domicilio_totais_por_grupo.csv',
    'favelas_fcu_total.csv',                           # 7g — favelas
    'favelas_fcu_por_municipio.csv',
    'favelas_fcu_comparativo_indicadores.csv',
])
def test_artefatos_das_demandas_existem(arquivo):
    assert (EDA / arquivo).exists(), f'Faltando: {arquivo}'


def test_recorte_urbano_mantem_os_70_municipios():
    """O filtro rural não pode zerar nenhum município da amostra ELSI."""
    conf = _read(EDA / 'exclusao_rural_conferencia.csv')
    assert len(conf) == 70                                       # uma linha por município
    assert (conf['n_ok_urbano'] > 0).all(), 'Algum município ficou sem setores urbanos'
    assert conf['n_ok_total'].sum() == 106_281                   # soma dos elegíveis antes do filtro
    assert conf['n_ok_urbano'].sum() == 104_108                  # conjunto de análise final


def test_indice_de_envelhecimento_usa_denominador_0a14():
    """IEP = 60+ / menores de 15 (Galvão et al., 2025). Recalcula a partir das contagens
    exportadas e confere com a coluna publicada — pega qualquer regressão do denominador."""
    tot = _read(EDA / 'indicadores_envelhecimento_total.csv').iloc[0]
    esperado = tot['n_idoso_60mais'] / tot['n_pop_0a14'] * 100
    assert abs(tot['IEP'] - esperado) < 0.1, 'IEP não bate com 60+ / menores de 15'
    # o denominador antigo (só 0 a 4 anos) daria um valor ~3x maior — garante que não voltou
    antigo = tot['n_idoso_60mais'] / tot['n_crianca_0a4'] * 100
    assert abs(tot['IEP'] - antigo) > 100, 'IEP parece estar usando o denominador antigo (0 a 4 anos)'
    assert 0 < tot['IEP'] < 500 and 0 < tot['RDI'] < 200         # faixas plausíveis


def test_contagem_de_setores_de_favela():
    """CD_TIPO = 1 identifica Favela e Comunidade Urbana; a contagem tem que bater
    entre a tabela total, a de regiões e a de municípios.

    As tabelas trazem os DOIS universos, e é isso que este teste protege: 19.507 na base
    completa (109.032 setores) e 19.452 no recorte de análise (104.108 urbanos
    elegíveis). Foi a confusão entre os dois que fez a apresentação de agosto anunciar
    "17,9% do recorte" — percentual que é da base, não do recorte, onde dá 18,7%.
    """
    total = _read(EDA / 'favelas_fcu_total.csv')
    por_reg = _read(EDA / 'favelas_fcu_por_regiao.csv')
    por_mun = _read(EDA / 'favelas_fcu_por_municipio.csv')

    base = total[total['universo'].str.startswith('base')].iloc[0]
    recorte = total[total['universo'].str.startswith('recorte')].iloc[0]
    assert base['n_setores_fcu'] == 19_507
    assert base['n_setores'] == 109_032
    assert recorte['n_setores_fcu'] == 19_452
    assert recorte['n_setores'] == 104_108
    # o percentual do recorte é maior porque o denominador dele não tem setor rural,
    # zerado nem sigiloso — nenhum dos quais pode ser favela
    assert recorte['pct_setores_fcu'] > base['pct_setores_fcu']

    # a linha da base tem que continuar em primeiro: testes e gerador do deck leem iloc[0]
    assert total.iloc[0]['n_setores_fcu'] == 19_507

    for universo, esperado in [('base', 19_507), ('recorte', 19_452)]:
        fatia = por_reg[por_reg['universo'].str.startswith(universo)]
        assert len(fatia) == 5, f'faltou região no universo {universo}'
        assert fatia['n_setores_fcu'].sum() == esperado

    assert por_mun['n_setores_fcu'].sum() == 19_507      # por município: só a base completa
    assert len(por_mun) == 70


def test_calculo_nacional_bate_com_o_censo():
    """Demanda 7: o total do país tem que reproduzir os números publicados pelo IBGE.

    Vale como teste de regressão de precisão: com `float32` a soma da população dava
    203.080.736 em vez de 203.080.756.
    """
    caminho = BD / 'nacional' / 'representatividade_elsi_no_brasil.csv'
    if not caminho.exists():
        pytest.skip('Cálculo nacional não executado localmente — rode scripts/proporcoes_brasil.py')
    rep = _read(caminho).set_index('metrica')
    assert rep.loc['população (v0001)', 'Brasil'] == 203_080_756      # Censo 2022, população residente
    assert rep.loc['setores (todos)', 'Brasil'] == 468_099            # setores do arquivo básico
    assert rep.loc['setores (todos)', 'ELSI_70'] == 109_032           # o recorte do projeto
    assert rep.loc['municípios', 'ELSI_70'] == 70


def test_comparativo_brasil_vs_elsi_cobre_os_indicadores():
    caminho = BD / 'nacional' / 'comparativo_brasil_vs_elsi.csv'
    if not caminho.exists():
        pytest.skip('Cálculo nacional não executado localmente — rode scripts/proporcoes_brasil.py')
    comp = _read(caminho)
    assert ESPERADOS_INDICADORES <= set(comp['indicador'])             # os 7 do IVS estão lá
    assert comp['razao_agregada__BR_urbano'].notna().all()
    assert comp['razao_agregada__ELSI70_urbano'].notna().all()


def test_tipo_domicilio_soma_coerente():
    """Convencional + não convencional não pode passar de 100% dos DPPO (V00001)."""
    grupos = _read(EDA / 'tipo_domicilio_totais_por_grupo.csv').set_index('grupo')
    soma_dppo = grupos.loc['Convencional', 'pct_sobre_V00001'] + grupos.loc['Não convencional', 'pct_sobre_V00001']
    assert soma_dppo <= 100.0, f'Soma dos tipos de DPPO passou de 100%: {soma_dppo}'
    assert soma_dppo > 99.0, f'Soma dos tipos de DPPO baixa demais ({soma_dppo}) — sigilo excessivo?'


def test_tabelas_de_auditoria_usam_o_recorte_com_rurais():
    """As tabelas de `scripts/gerar_tabelas_auditoria.py` são do recorte PRÉ-filtro urbano.

    Elas sustentam números já apresentados à orientadora (106.281 setores). Se alguém
    regerá-las sobre o recorte urbano (104.108), as apresentações antigas deixam de bater
    — este teste é o alarme.
    """
    total = _read(EDA / 'cobertura_total.csv').iloc[0]
    assert total['n_setores_OK'] == 106_281
    por_reg = _read(EDA / 'cobertura_por_regiao.csv')
    por_mun = _read(EDA / 'cobertura_por_municipio.csv')
    assert por_reg['n_setores_OK'].sum() == total['n_setores_OK']     # regiões particionam o total
    assert por_mun['n_setores_OK'].sum() == total['n_setores_OK']     # municípios também
    assert len(por_mun) == 70


def test_cobertura_de_saneamento_e_internamente_coerente():
    """Ter os 3 serviços integrais é mais raro que ter cada um deles, e coleta de lixo
    (sem caçamba no numerador) é sempre mais frequente que lixo totalmente adequado."""
    t = _read(EDA / 'cobertura_total.csv').iloc[0]
    assert t['saneamento_3_100'] <= min(t['agua_adeq_100'], t['esgoto_adeq_100'], t['lixo_adeq_100'])
    assert t['coleta_lixo_100'] >= t['lixo_adeq_100']                 # caçamba conta como coletado
    for col in ['agua_adeq_100', 'esgoto_adeq_100', 'lixo_adeq_100', 'dados_7vars_100', 'coleta_lixo_100']:
        assert 0 < t[col] <= t['n_setores_OK']


def test_auditoria_de_analfabetismo_fecha_as_contagens():
    """n_validos = n_setores - n_sigilo em todo município, e a tabela por porte de setor
    cobre exatamente os mesmos 106.281 setores."""
    mun = _read(EDA / 'auditoria_analfabetismo_municipio.csv')
    assert len(mun) == 70
    assert (mun['n_validos'] == mun['n_setores'] - mun['n_sigilo']).all()
    assert mun['pct_sigilo_v901'].is_monotonic_decreasing            # ordenada por gravidade do sigilo
    bins = _read(EDA / 'auditoria_analfabetismo_v00900_bins.csv')
    assert bins['n_setores'].sum() == mun['n_setores'].sum() == 106_281
    assert bins['n_v901_sigilo'].sum() == mun['n_sigilo'].sum()


def test_particao_da_agua_canalizada_fecha():
    """V00199 + V00200 + V00201 = V00001 é uma partição definida pelo IBGE.

    É o que autoriza medir 'sem canalização' pelo complemento de V00199 — que tem 0,04% de
    ausentes — em vez de somar V00200+V00201, que perde 21,9% dos setores para o sigilo.
    Se este teste falhar, a substituição deixa de ser válida.
    """
    base = BD / 'Base_ELSI_Bruta_Censo2022.csv'
    if not base.exists():
        pytest.skip('Base bruta não gerada localmente — rode o Notebook 01 da Fase 3')
    df = pd.read_csv(base, sep=';', dtype=str, usecols=['V00001', 'V00199', 'V00200', 'V00201'])
    for c in df.columns:
        df[c] = pd.to_numeric(df[c].replace({'X': None, 'x': None}), errors='coerce')
    soma = df[['V00199', 'V00200', 'V00201']].sum(axis=1, min_count=3)   # exige as três
    conferiveis = soma.notna()
    assert conferiveis.sum() > 50_000, 'poucos setores conferíveis — algo mudou na extração'
    fecham = (soma[conferiveis] - df.loc[conferiveis, 'V00001']).abs() <= 0.5
    assert fecham.all(), f'{(~fecham).sum()} setores em que a trinca não soma V00001'


def test_agua_canalizada_exportada_e_coerente():
    """As proporções regionais somam 100% e o gradiente Norte-Sul aparece."""
    reg = _read(EDA / 'agua_canalizada_por_regiao.csv')
    assert len(reg) == 5
    # As três categorias NÃO somam 100%: onde o IBGE sigila V00200/V00201 a contagem some
    # do numerador e V00001 continua inteiro no denominador. A soma tem que ficar logo
    # abaixo de 100, e a diferença é exatamente a massa suprimida que a coluna registra.
    soma = reg['pct_dentro_casa'] + reg['pct_so_terreno'] + reg['pct_nao_encanada']
    assert (soma <= 100.001).all(), f'soma acima de 100%: {soma.tolist()}'
    assert (soma > 99.0).all(), f'sigilo alto demais para a razão agregada: {soma.tolist()}'
    esperado = 100 - reg['pct_dentro_casa']
    assert ((reg['pct_sem_canalizacao'] - esperado).abs() < 0.011).all(), \
        'pct_sem_canalizacao devia ser o complemento de pct_dentro_casa, não a soma das parcelas'
    assert (reg['pct_suprimido'] >= 0).all()
    norte = reg.loc[reg['regiao'] == 'Norte', 'pct_sem_canalizacao'].iloc[0]
    sul = reg.loc[reg['regiao'] == 'Sul', 'pct_sem_canalizacao'].iloc[0]
    assert norte > sul, 'o gradiente Norte-Sul do saneamento sumiu — conferir a extração'


# ─────────────────────────────────────────────────────────────────────────────
# Regressões da auditoria de 24/08/2026
# ─────────────────────────────────────────────────────────────────────────────

def test_marcacao_de_favela_bate_com_a_lista_oficial_do_ibge():
    """`CD_TIPO = 1` tem que reproduzir a lista oficial de setores de FCU do IBGE.

    A apresentação de agosto afirmava que `CD_TIPO = 1` coincidia com ter `NM_FCU`
    preenchido. Não coincide: são 33.272 contra 33.321 no país, 19.507 contra 19.532 no
    recorte. Quem erra é o `NM_FCU` — os divergentes não constam da lista oficial. Este
    teste trava a conferência que de fato vale.
    """
    base = BD / 'Base_ELSI_Bruta_Censo2022.csv'
    planilha = ROOT / 'dados' / 'FavelaseComunidadesUrbanas2022Setores_20250417.xlsx'
    if not base.exists():
        pytest.skip(f'Base bruta não gerada localmente: {base}')
    if not planilha.exists():
        pytest.skip(f'Lista oficial de FCU do IBGE não encontrada: {planilha}')

    oficial = set(pd.read_excel(planilha, sheet_name='Setores_FCUs', dtype=str)['CD_SETOR'].str.strip())
    assert len(oficial) == 33_272, 'a lista oficial do IBGE mudou de tamanho'

    df = pd.read_csv(base, sep=';', dtype=str, usecols=['CD_SETOR', 'CD_TIPO', 'NM_FCU'])
    marcados = set(df.loc[df['CD_TIPO'].eq('1'), 'CD_SETOR'])
    no_recorte = oficial & set(df['CD_SETOR'])

    assert marcados == no_recorte, 'CD_TIPO=1 deixou de coincidir com a lista oficial do IBGE'
    assert len(marcados) == 19_507

    # e o NM_FCU continua NÃO servindo como critério — é o que a afirmação antiga supunha
    com_nome = set(df.loc[df['NM_FCU'].notna(), 'CD_SETOR'])
    assert com_nome != marcados, 'se NM_FCU passou a coincidir, revisar o texto das apresentações'
    assert not (com_nome - marcados) <= oficial or (com_nome - marcados) - oficial, \
        'os setores com NM_FCU e sem CD_TIPO=1 não deveriam estar na lista oficial'


def test_razao_agregada_mede_numerador_e_denominador_nos_mesmos_setores():
    """A razão agregada não pode somar cada lado num conjunto diferente de setores.

    `resumir()` somava o numerador pulando os setores sigilosos e o denominador somando
    todos — o setor saía do numerador mas continuava no denominador, e a razão vinha baixa
    demais: −8,9% em `pct_apartamento`, −13,1% em `pct_sem_banheiro`. O teste refaz a
    conta a partir da base e confere contra o que o script publicou.
    """
    import sys
    caminho = BD / 'nacional' / 'proporcoes_por_recorte.csv'
    base = BD / 'Base_ELSI_Bruta_Censo2022.csv'
    if not caminho.exists():
        pytest.skip('Cálculo nacional não executado — rode scripts/proporcoes_brasil.py')
    if not base.exists():
        pytest.skip(f'Base bruta não gerada localmente: {base}')

    sys.path.insert(0, str(ROOT / 'src'))
    from ivs_censo import INDICADORES_POR_NOME, classificar_dados_sig

    df = pd.read_csv(base, sep=';', dtype=str)
    texto = ['CD_SETOR', 'CD_UF', 'CD_MUN', 'NM_MUN', 'NM_BAIRRO', 'SITUACAO',
             'CD_SIT', 'CD_TIPO', 'CD_FCU', 'NM_FCU', 'Moradia_Predominante']
    num_cols = [c for c in df.columns if c not in texto]
    df[num_cols] = (df[num_cols].replace({'X': None, 'x': None})
                    .apply(lambda c: c.astype(str).str.replace(',', '.', regex=False))
                    .apply(pd.to_numeric, errors='coerce'))
    ok = df[(classificar_dados_sig(df) == 'OK') & df['SITUACAO'].eq('Urbana')]

    publicado = pd.read_csv(caminho, sep=';', encoding='utf-8-sig')
    elsi = publicado[publicado['recorte'].str.startswith('ELSI')].set_index('indicador')

    # pct_apartamento e pct_sem_banheiro são os que mais sofriam: numerador de uma
    # variável só, que o IBGE sigila com frequência
    for nome in ['pct_apartamento', 'pct_sem_banheiro', 'pct_casa_vila_condominio', 'pct_agua_inad']:
        ind = INDICADORES_POR_NOME[nome]
        n = ok[ind.numerador].sum(axis=1, min_count=1)
        d = ok[ind.denominador].sum(axis=1, min_count=ind.min_count_den)
        par = n.notna() & d.notna()
        esperado = n[par].sum() / d[par].sum()
        obtido = elsi.loc[nome, 'razao_agregada']
        assert abs(obtido - esperado) < 1e-6, (
            f'{nome}: razão agregada {obtido:.6f} != {esperado:.6f} medido nos mesmos setores')


def test_auditoria_de_renda_poe_os_suspeitos_primeiro_e_expoe_a_magnitude():
    """O arquivo existe por causa dos suspeitos — eles têm que estar no topo.

    Ordenar por `classe_renda` direto dava ordem alfabética (EXTREMO, NORMAL, SUSPEITO) e
    enterrava os 66 suspeitos no fim de 3.358 linhas. E `razao_implausivel` é o contrapeso
    do teste de coerência, que não enxerga erro de dado em bairro rico: o setor de São
    Paulo com 45× a mediana municipal sai como EXTREMO e só esta coluna o denuncia.
    """
    caminho = EDA / 'renda_outliers_rastreados.csv'
    if not caminho.exists():
        pytest.skip('Auditoria de renda não executada — rode scripts/auditoria_renda.py')
    t = _read(caminho)

    for col in ['razao_implausivel', 'cv_renda']:
        assert col in t.columns, f'coluna de diagnóstico ausente: {col}'

    assert t.iloc[0]['classe_renda'] == 'SUSPEITO', 'os suspeitos deixaram de vir primeiro'
    primeira_extremo = t['classe_renda'].tolist().index('EXTREMO')
    assert 'SUSPEITO' not in t['classe_renda'].tolist()[primeira_extremo:], \
        'as classes estão intercaladas — a ordenação por prioridade se perdeu'

    # dentro de cada classe, do mais absurdo para o menos
    for classe in ['SUSPEITO', 'EXTREMO']:
        fatia = t[t['classe_renda'] == classe]['razao_mediana_mun']
        assert fatia.is_monotonic_decreasing, f'{classe} não está ordenada por razão'

    # o ponto cego que a coluna existe para mostrar
    implausiveis_extremos = t[(t['classe_renda'] == 'EXTREMO') & t['razao_implausivel']]
    assert len(implausiveis_extremos) > 0, (
        'nenhum EXTREMO implausível: ou a base mudou, ou razao_implausivel parou de ser calculada')

    # CV alto é a assinatura da média puxada por poucas declarações
    assert t.loc[t['classe_renda'] == 'SUSPEITO', 'cv_renda'].max() > 3, \
        'CV dos suspeitos baixo demais — V06005 está sendo lida?'


def test_entrega_separa_urbanos_da_base_do_recorte_de_analise():
    """Os metadados do entregável não podem anunciar 106.347 como recorte de análise.

    `n_setores_urbanos` conta SITUACAO='Urbana' na base inteira e dá 106.347 — número
    maior que os 106.281 elegíveis, impossível como recorte. O recorte é a interseção com
    Dados_sig='OK' e dá 104.108, que é o que a consulta SQL recomendada devolve.
    """
    import sqlite3
    db = BD / 'entrega_orientadora' / 'Base_ELSI_70Municipios_Censo2022.db'
    if not db.exists():
        pytest.skip('Entregável não gerado — rode scripts/gerar_entrega_orientadora.py')

    with sqlite3.connect(db) as con:
        meta = dict(con.execute('SELECT chave, valor FROM metadados').fetchall())
        n_sql = con.execute(
            "SELECT COUNT(*) FROM setores_censitarios WHERE Dados_sig='OK' AND urbano=1"
        ).fetchone()[0]

    assert meta['n_setores_recorte_analise'].replace(',', '') == '104108'
    assert meta['n_setores_urbanos'].replace(',', '') == '106347'
    assert n_sql == 104_108, 'a consulta recomendada no README não devolve o recorte anunciado'
    assert meta['n_setores_favela_fcu_no_recorte'].replace(',', '') == '19452'


