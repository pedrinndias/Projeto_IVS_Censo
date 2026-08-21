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
    entre a tabela total, a de regiões e a de municípios."""
    total = _read(EDA / 'favelas_fcu_total.csv').iloc[0]
    por_reg = _read(EDA / 'favelas_fcu_por_regiao.csv')
    por_mun = _read(EDA / 'favelas_fcu_por_municipio.csv')
    assert total['n_setores_fcu'] == 19_507
    assert por_reg['n_setores_fcu'].sum() == total['n_setores_fcu']
    assert por_mun['n_setores_fcu'].sum() == total['n_setores_fcu']
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
