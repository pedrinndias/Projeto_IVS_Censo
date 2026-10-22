#!/usr/bin/env python
"""Guia de estudo do deck para a orientadora: cada slide explicado do zero.

    ./.venv/bin/python scripts/dados_deck_orientadora.py
    node scripts/gerar_deck_orientadora.js
    ./.venv/bin/python scripts/gerar_pdf_guia_deck_orientadora.py

Lê o mesmo JSON que gerou o deck (`00_sintese/unificada/deck_orientadora.json`) e o mapa de
slides que o gerador grava ao lado, converte o deck em PDF (LibreOffice) e cada página em
imagem (`scripts/folha_contato.swift`), e monta, para cada slide: a imagem, o que ele é, como
ler, o que mostra, a explicação do zero, o tipo de gráfico, os conceitos que aparecem nele e
uma sugestão de fala. Antes, um glossário com todos os conceitos; no fim, perguntas prováveis
com as respostas. Os números do texto saem dos mesmos CSVs do deck.
"""
import html
import json
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (CondPageBreak, Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer)

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from gerar_pdf_guia_decks_outubro import registrar_fontes  # noqa: E402
from eda_versoes import br, intbr, pctbr  # noqa: E402

RAIZ = AQUI.parent
UNI = RAIZ / 'analises_exploratorias' / '00_sintese' / 'unificada'
A = RAIZ / 'analises_exploratorias'
E = RAIZ / 'banco_de_dados' / 'eda'
SAIDA = RAIZ / 'docs' / 'Apresentacoes_IVS' / 'Guia_Estudo_Apresentacao_Orientadora_2026-10.pdf'
TINTA, PETROL, CLAY, CINZA, FUNDO = (colors.HexColor(c) for c in ('#1A1A1A', '#1F4E4A', '#A83A2C', '#666666', '#F2F0EC'))

# ── Glossário: (termo, padrões que o detectam num slide, explicação do zero) ──────────────
GLOSSARIO = [
    ('O projeto e os dados', [
        ('Setor censitário', r'setor', 'A menor área em que o IBGE divulga os dados do Censo: um pedaço de bairro, com algumas centenas de domicílios. É a unidade de análise do projeto: cada linha da base é um setor, e o índice dá um valor para cada setor.'),
        ('Censo 2022 e agregados por setor', r'Censo|V0\d{4}|V\d{5}', 'O IBGE publica, para cada setor, contagens de pessoas e domicílios com cada característica (as variáveis com códigos como V00495). O projeto não tem dados de pessoas individuais: tudo é contagem por setor.'),
        ('IVS — Índice de Vulnerabilidade Social', r'IVS|índice', 'Um número para cada setor que resume várias carências (renda, escolaridade, saneamento, moradia) num valor só, para mostrar onde a vulnerabilidade se concentra. O modelo do projeto é o IVS de Belo Horizonte de 2012 (IVS-BH).'),
        ('ELSI-Brasil e os 70 municípios', r'ELSI|70 municípios|municípios', 'O Estudo Longitudinal da Saúde dos Idosos Brasileiros acompanha pessoas de 50 anos ou mais em 70 municípios. O projeto calcula o IVS nos setores desses 70 municípios para, depois, cruzar com a saúde dos idosos.'),
        ('Recorte de análise', r'recorte', 'O conjunto de setores que entra nas contas: setores urbanos com Dados_sig = OK (com dados divulgados). Na referência são 104.108 setores.'),
        ('Sigilo e Dados_sig', r'sigilo|Dados_sig|faltante', 'Para proteger a privacidade, o IBGE esconde valores de setores com poucos domicílios. Dados_sig marca se o setor tem os dados divulgados (OK) ou não. O sigilo não é aleatório: atinge mais os setores pequenos.'),
        ('FCU — favelas e comunidades urbanas', r'FCU|favela', 'Áreas que o IBGE delimita como favelas e comunidades urbanas. O projeto usa como referência externa: um bom índice de vulnerabilidade deve dar valores mais altos a esses setores.'),
        ('Indicador, numerador e denominador', r'indicador|proporção', 'Um indicador é uma conta feita com as variáveis do Censo, quase sempre uma proporção: o numerador (por exemplo, domicílios sem banheiro) dividido pelo denominador (domicílios do setor). Vai de 0 (ninguém) a 1 (todos).'),
        ('Versão e referência', r'versão|versões|referência', 'A referência é a especificação do índice proposta no NB05 (renda original, sem lixo, banheiro graduado, promax, pesos 60/40, normalização no município). Cada versão é a referência com uma coisa mudada, para ver o efeito dessa mudança.'),
    ]),
    ('Estatística descritiva', [
        ('Análise exploratória de dados (EDA)', r'EDA|exploratória', 'A etapa de olhar os dados antes de modelar: valores típicos, dispersão, forma, faltantes, extremos e relações entre variáveis. Serve para saber se os dados se prestam ao que se quer fazer com eles.'),
        ('Média e mediana', r'média|mediana', 'A média soma os valores e divide pelo número deles; a mediana é o valor do meio quando os setores são ordenados. A média é puxada por valores extremos; a mediana, não. Quando as duas se afastam, a distribuição é assimétrica.'),
        ('Percentis e quartis', r'P10|P90|percentil|quartil|P25|P75', 'O percentil 90 (P90) é o valor abaixo do qual estão 90% dos setores. Os quartis dividem os setores em quatro partes iguais (P25, mediana, P75). O intervalo interquartil vai do P25 ao P75 e contém a metade central.'),
        ('Desvio-padrão e coeficiente de variação', r'DP|desvio|CV', 'O desvio-padrão mede o quanto os valores se afastam da média. O coeficiente de variação é o desvio dividido pela média (em %): permite comparar a dispersão de indicadores em escalas diferentes.'),
        ('Assimetria e curtose', r'assim|curtose', 'Assimetria positiva significa cauda longa à direita: muitos setores com valores baixos e poucos com valores muito altos. A curtose mede o peso das caudas (quantos extremos há).'),
        ('Inflação de zeros', r'zeros', 'Quando a maior parte dos setores vale exatamente zero (por exemplo, nenhum domicílio sem banheiro). Muda a leitura de tudo: a mediana é zero, o intervalo interquartil é zero e a correlação fica achatada pelos empates.'),
        ('Valor faltante e exclusão por lista', r'faltante|exclusão por lista|listwise|casos completos', 'Faltante é um setor sem valor num indicador. A exclusão por lista tira da análise o setor que falta em qualquer variável usada; por isso a amostra do índice é menor que o recorte.'),
        ('Extremo e critério de Tukey', r'extremo|Tukey|outlier', 'Um valor muito afastado dos demais. O critério de Tukey marca como extremo o que fica a mais de 3 intervalos interquartis além dos quartis. Extremo não é erro por definição: pode ser um setor realmente diferente.'),
    ]),
    ('Correlação', [
        ('Correlação de Pearson', r'Pearson', 'Mede a relação em linha reta entre dois indicadores, de −1 a 1. É sensível a valores extremos.'),
        ('Correlação de Spearman (ρ)', r'Spearman|ρ', 'Mede se dois indicadores ordenam os setores do mesmo jeito, de −1 (ordem invertida) a 1 (mesma ordem); 0 é nenhuma relação de ordem. Usa os postos (a ordem), não os valores, por isso resiste a extremos. É a correlação usada na fatorial do projeto.'),
        ('Matriz de correlação', r'matriz|mapa de calor', 'Uma tabela em que cada célula é a correlação entre a variável da linha e a da coluna; a diagonal é 1 (cada variável com ela mesma). Em cor, vira um mapa de calor.'),
        ('Dendrograma', r'dendrograma|agrupamento hierárquico', 'Uma árvore que junta, passo a passo, as variáveis mais parecidas. Quanto mais cedo (mais à esquerda) duas variáveis se unem, mais correlacionadas elas são.'),
    ]),
    ('Análise fatorial', [
        ('Análise fatorial', r'fatorial|fator', 'Técnica que resume várias variáveis correlacionadas em poucas dimensões (fatores). Se renda, analfabetismo e cor ou raça andam juntos, eles formam um fator — a dimensão socioeconômica. O IVS usa os fatores para decidir quanto cada variável pesa.'),
        ('Componentes principais (ACP)', r'ACP|componentes principais|componente', 'O método de extração usado no projeto: encontra as combinações das variáveis que resumem o máximo de variância. Alternativas: eixo principal e máxima verossimilhança (versão C2).'),
        ('Carga fatorial', r'carga', 'A correlação de uma variável com um fator. Carga alta (perto de 1) quer dizer que a variável é bem representada pelo fator. Critério do projeto: pelo menos 0,40 no fator principal.'),
        ('Comunalidade', r'comunalidade', 'A parte da variância de uma variável que os fatores explicam, de 0 a 1. Comunalidade baixa: a variável compartilha pouco com as outras. Critério do projeto: pelo menos 0,30.'),
        ('KMO e MSA', r'KMO|MSA', 'O KMO (Kaiser-Meyer-Olkin) diz se as variáveis compartilham informação suficiente para uma fatorial, de 0 a 1; o projeto exige pelo menos 0,70. O MSA é o mesmo índice para cada variável; o projeto exige pelo menos 0,50.'),
        ('Teste de Bartlett', r'Bartlett', 'Testa se as variáveis têm alguma correlação entre si. Com dezenas de milhares de setores, sempre rejeita a hipótese de nenhuma correlação: é condição necessária, não suficiente.'),
        ('Autovalor e variância explicada', r'autovalor|variância', 'O autovalor mede quanta variância um componente resume, em unidades de variável (autovalor 2 = duas variáveis inteiras). A variância explicada por 2 fatores diz quanto do total os dois primeiros resumem.'),
        ('Critério de Kaiser e análise paralela de Horn', r'Kaiser|Horn', 'Duas regras para decidir quantos fatores reter. Kaiser: autovalores acima de 1. Horn: autovalores acima do que dados aleatórios do mesmo tamanho produziriam — mais conservadora.'),
        ('Gráfico de sedimentação (scree)', r'sedimentação|scree', 'Os autovalores em ordem decrescente; os fatores que valem a pena ficam no "paredão", acima da linha de Horn.'),
        ('Rotação: Varimax e promax', r'Varimax|promax|rotação', 'Girar os fatores para que cada variável carregue forte em um só. Varimax mantém os fatores independentes; promax permite que se correlacionem (a correlação entre eles é Φ).'),
        ('Matriz padrão e matriz estrutura', r'padrão|estrutura', 'Na promax: a matriz padrão dá o efeito próprio de cada fator sobre a variável; a estrutura dá a correlação simples. O projeto reporta as duas.'),
        ('Pesos do índice e regra 60/40', r'peso|60/40|60_40', 'Cada variável vai para o fator em que carrega mais, e o peso do fator se reparte entre suas variáveis pelo quadrado das cargas. A regra 60/40 do IVS-BH dá 60% à dimensão socioeconômica e 40% ao saneamento.'),
        ('Elegibilidade (critérios do NB05)', r'elegív|elegibilidade', 'Uma versão é elegível quando passa em quatro critérios fixados antes de rodar: KMO ≥ 0,70, MSA ≥ 0,50, comunalidade ≥ 0,30 e carga ≥ 0,40 em todas as variáveis. É descritivo: não escolhe a versão.'),
    ]),
    ('O índice', [
        ('Normalização min-max', r'min-max|normaliz', 'Põe cada componente entre 0 e 1: 0 no menor valor, 1 no maior. Na referência é feita dentro de cada município, então o índice compara setores da mesma cidade. Alternativas: global, escore z, postos (versão C3).'),
        ('Agregação', r'agregação|soma ponderada|geométrica', 'Como os componentes viram um número só: soma ponderada (referência) ou média geométrica (versão C4), que pune componentes perto de zero.'),
        ('Faixas de vulnerabilidade', r'faixa', 'O índice é dividido em quatro faixas: baixo, médio, elevado, muito elevado. A regra do IVS-BH usa média e desvio-padrão do município; os quartis dividem cada município em quatro partes iguais.'),
        ('k-médias e silhueta', r'k-médias|agrupamento|silhueta|grupo', 'O k-médias junta setores (ou municípios) com perfis parecidos em k grupos. A silhueta mede se os grupos estão bem separados (−1 a 1); o projeto escolhe k entre 3 e 6 pela silhueta.'),
    ]),
    ('Validação e robustez', [
        ('AUC e curva ROC', r'AUC|ROC', 'A AUC é a probabilidade de um setor de favela, sorteado, ter índice maior que um setor de fora, também sorteado. 0,5 é o acaso; 1 é separação perfeita. A curva ROC mostra essa separação em todos os cortes possíveis. A AUC municipal é a mediana da AUC calculada dentro de cada município.'),
        ('Sensibilidade por município', r'município de fora|sensibilidade', 'Reestimar os pesos tirando um município por vez (70 rodadas) para ver se alguma cidade sozinha define o resultado. A orientadora pediu isso no lugar do bootstrap.'),
        ('Reamostragem (bootstrap)', r'reamostra|bootstrap', 'Sortear setores com reposição e refazer a análise muitas vezes, para ver quanto o resultado varia só pelo acaso da amostra. Na análise E2 foram 1.000 reamostragens.'),
        ('Mudança de faixa e correlação com a referência', r'muda|mudam', 'Duas formas de medir o efeito de uma versão: a correlação de postos entre o índice dela e o da referência, e o percentual de setores que trocam de faixa.'),
        ('Gini, Theil e P90/P10', r'Gini|Theil|P90/P10|desigualdade', 'Medidas de desigualdade do índice dentro de cada município. Gini vai de 0 (todos iguais) a 1 (tudo concentrado num setor); Theil é mais sensível à cauda alta; P90/P10 compara o setor do percentil 90 com o do 10.'),
        ('Envelhecimento: IEP, RDI, 60+', r'envelhecimento|IEP|RDI|60\+|idos', 'Índice de envelhecimento (IEP): pessoas de 60+ por pessoa de 0 a 14 anos. Razão de dependência idosa (RDI): 60+ por pessoa de 15 a 59. Proporção de 60+ e de 70+ entre os 60+.'),
    ]),
]
TERMOS = [(t, re.compile(p, re.I), x) for _, itens in GLOSSARIO for t, p, x in itens]

# ── Tipos de gráfico ──────────────────────────────────────────────────────────
GRAFICO = {
    'histograma': 'Histograma: o eixo horizontal é dividido em faixas de valor e a altura de cada barra é quantos setores caem nela. Mostra a forma da distribuição: onde os setores se concentram e se há cauda longa.',
    'boxplot': 'Diagrama de caixa (boxplot): a linha dentro da caixa é a mediana, a caixa vai do 1º ao 3º quartil (metade central dos setores) e as hastes mostram a extensão típica. Caixas que não se sobrepõem indicam grupos bem diferentes.',
    'densidade': 'Curvas de densidade: histogramas suavizados, um por grupo, com área igual a 1. Servem para comparar formas, não tamanhos.',
    'matriz': 'Mapa de calor de correlação: cada célula é a correlação entre duas variáveis, com o valor escrito e a cor dizendo o sinal (argila positiva, petróleo negativa) e a força (cor mais intensa, relação mais forte).',
    'dendrograma': 'Dendrograma: árvore que junta as variáveis da mais parecida para a menos parecida; uniões à esquerda são relações fortes.',
    'barras': 'Gráfico de barras: o comprimento de cada barra é o valor da categoria; as barras vêm ordenadas para destacar as maiores.',
    'barras_empilhadas': 'Barras empilhadas: cada barra soma 100% e é dividida em partes (as faixas); compara a composição entre categorias.',
    'linhas': 'Gráfico de linhas: mostra como um valor muda ao longo de uma sequência ordenada (aqui, os décimos de tamanho do setor).',
    'hexbin': 'Gráfico de hexágonos: cada hexágono conta quantos setores têm aquela combinação de valores; quanto mais escuro, mais setores. Substitui o gráfico de pontos quando há dezenas de milhares deles.',
    'scree': 'Gráfico de sedimentação: os autovalores em ordem; a linha tracejada é o limite de Horn. Componentes acima da linha valem ser retidos.',
    'plano': 'Plano fatorial: cada variável é um ponto (ou seta) nas cargas dos fatores 1 e 2. Variáveis perto do eixo horizontal pertencem ao fator 1; perto do vertical, ao fator 2.',
    'roc': 'Curva ROC: para cada corte do índice, a proporção de favelas acima do corte (vertical) contra a de setores de fora acima do corte (horizontal). Quanto mais a curva sobe para o canto superior esquerdo, melhor a separação; a diagonal é o acaso.',
    'contingencia': 'Matriz de contingência: cruza a faixa de cada setor na referência (linhas) com a faixa nesta versão (colunas); a diagonal é a concordância.',
    'dispersao': 'Gráfico de dispersão: cada ponto é uma versão, posicionada por duas medidas; serve para ver quais versões ficam perto da referência e quais separam melhor as favelas.',
    'piramide': 'Pirâmide etária de um lado só: barras com a porcentagem da população em cada faixa de idade (os agregados não separam por sexo); os pontos são as regiões.',
    'intervalo': 'Linhas de intervalo: para cada município, a linha vai do menor ao maior valor entre as versões e o ponto marca a referência.',
    'calor_perfis': 'Mapa de calor de perfis: linhas são grupos, colunas são componentes; a cor é o valor médio do componente no grupo.',
    'pontos': 'Pontos e caixas: a distribuição de um valor em várias rodadas; mostra quanto ele varia.',
}
TIPO = {'hist': 'histograma', 'box': 'boxplot', 'dens': 'densidade', 'mapa_spearman': 'matriz', 'dendrograma': 'dendrograma',
        'funil_fig': 'barras', 'extremos_fig': 'barras', 'fcu_fig': 'barras', 'sigilo_porte_fig': 'linhas', 'piramide': 'piramide',
        'dispersao_60': 'hexbin', 'e5_hex': 'hexbin', 'sedimentacao': 'scree', 'cargas': 'plano', 'roc': 'roc', 'hist_faixa': 'histograma',
        'risco_barras': 'barras_empilhadas', 'desigualdade_fig': 'barras', 'comp_matriz_fig': 'contingencia', 'comp_municipios_fig': 'barras',
        'sint_disp': 'dispersao', 'sint_barras': 'barras', 'e1_hist': 'histograma', 'e1_mun_fig': 'barras', 'e3_fig': 'intervalo',
        'e4_fig': 'barras', 'e5_box': 'boxplot', 'e6_fig_setores': 'calor_perfis', 'e2_pesos_fig': 'pontos', 'e2_loo_fig': 'barras',
        'sensibilidade_mun': 'pontos', 'nb05_auc': 'pontos', 'nb05_peso': 'pontos', 'nb05_concordancia': 'contingencia',
        'extremo_bh': 'histograma', 'falt_mapa': 'matriz'}

PARTES = {
    '1': 'A Parte 1 junta todas as versões das análises exploratórias. Cada versão é a referência com uma coisa mudada; aqui elas aparecem lado a lado, com as mesmas medidas, para mostrar o que muda o índice e o que não muda. Ao apresentar, a ideia central é: a maior parte das escolhas mexe pouco; algumas mexem muito, e são essas que a orientadora precisa decidir.',
    '2': 'A Parte 2 é a análise exploratória da versão final: o recorte de análise com todos os indicadores, já com as correções e os indicadores novos pedidos nas demandas de setembro. Ao apresentar, siga as demandas: para cada uma, mostre onde ela foi atendida e o que os dados dizem.',
    '3': 'A Parte 3 é a análise fatorial: primeiro a grade de cenários que responde às demandas 3 e 5 a 11, depois as especificações do NB05 e a referência proposta, a fatorial da referência e os testes de robustez. Ao apresentar, insista em duas coisas: a estrutura de dois fatores aparece em quase tudo, e as escolhas abertas estão listadas para ela decidir.',
    '4': 'A Parte 4 é um catálogo: as figuras da EDA da versão final, só identificadas pelo ID, para escolher o que vai para o artigo. Não precisa explicar cada uma; basta saber localizar no Catalogo_Mestre.xlsx.',
    '5': 'A Parte 5 é o mesmo catálogo para a análise fatorial e o índice da versão final.',
}
O_QUE_E = {
    'capa': 'A capa: o título do deck, o que ele cobre e o autor.',
    'texto': 'Um slide de texto: lista os pontos principais de uma etapa. Cada número citado foi puxado de uma tabela gerada por script.',
    'secao': 'Uma divisória: abre uma das cinco partes do deck.',
    'numeros': 'Um slide de números em destaque: poucos números grandes, cada um com o que ele mede logo abaixo, e um parágrafo de leitura.',
    'figura': 'Um slide de figura: o gráfico à esquerda e, à direita, como ler e o que ele mostra. O rodapé diz de que arquivo a figura saiu.',
    'figura_larga': 'Um slide de figura larga: a figura ocupa a largura toda (usada nas matrizes de correlação) e a leitura fica embaixo.',
    'tabela': 'Um slide de tabela: a tabela à esquerda e, à direita, como ler e o que ela mostra. Tabelas longas continuam no slide seguinte.',
    'grade': 'Uma página do catálogo visual: miniaturas das figuras com a versão e o ID, para escolher no Catalogo_Mestre.xlsx o que vai para o artigo.',
}


def esc(t):
    return html.escape(str(t or ''), quote=False)


def estilos():
    base = dict(fontName='Serif', fontSize=10.5, leading=14.5, textColor=TINTA, alignment=TA_JUSTIFY)
    return {
        'capa': ParagraphStyle('capa', fontName='Serif-B', fontSize=26, leading=31, textColor=TINTA),
        'capa_sub': ParagraphStyle('capa_sub', fontName='Serif', fontSize=13, leading=18, textColor=CINZA),
        'h1': ParagraphStyle('h1', fontName='Serif-B', fontSize=18, leading=23, textColor=TINTA, spaceBefore=6, spaceAfter=8),
        'h2': ParagraphStyle('h2', fontName='Serif-B', fontSize=13, leading=17, textColor=PETROL, spaceBefore=10, spaceAfter=4),
        'rot': ParagraphStyle('rot', fontName='Sans-B', fontSize=8.5, leading=11, textColor=CLAY, spaceBefore=6, spaceAfter=1),
        'corpo': ParagraphStyle('corpo', **base, spaceAfter=4),
        'termo': ParagraphStyle('termo', **{**base, 'fontSize': 10}, spaceAfter=5, leftIndent=0),
        'pequeno': ParagraphStyle('pequeno', fontName='Serif-I', fontSize=8.5, leading=11, textColor=CINZA),
    }


def numeros_respostas():
    t60 = pd.read_csv(next((A / '00_sintese' / 'tabelas').glob('T60_*.csv'))).set_index('versao')
    t61 = pd.read_csv(next((A / '00_sintese' / 'tabelas').glob('T61_*.csv'))).set_index('eixo')
    v = pd.read_csv(E / 'fatorial_ampliada' / 'validacao_fcu.csv', sep=';', encoding='utf-8-sig').query("cenario == 'S0'").set_index('medida')['auc']
    t45 = pd.read_csv(next((A / 'E2_estabilidade' / 'tabelas').glob('T45_*.csv'))).set_index('medida')
    ref = pd.read_csv(E / 'ivs_especificacoes' / 'referencia.csv').query("leitura == 'principal'").iloc[0]
    t01 = pd.read_csv(next((A / '00_referencia' / 'tabelas').glob('T01_*.csv')))
    r = t60.loc['00_referencia']
    return [
        ('Por que esta referência e não outra?', f"Ela foi proposta no NB05 entre as especificações elegíveis por critério fixado antes: {esc(ref['porque'])}. É proposta, não decisão: as outras versões estão aqui justamente para comparar."),
        ('Quantos setores ficam fora do índice, e por quê?', f"O recorte tem {intbr(t01.iloc[-2]['setores'])} setores; o índice usa {intbr(t01.iloc[-1]['setores'])}. Saem os que não têm algum componente, quase sempre por sigilo do IBGE, que atinge mais os setores pequenos."),
        ('O índice acrescenta alguma coisa à renda?', f"No IVS-7 da grade ampliada (S0), a AUC contra as favelas é {br(v.loc['indice_01 (pesos Varimax)'])} para o índice e {br(v.loc['renda invertida sozinha'])} para a renda sozinha. A AUC mede só a parte socioeconômica: o índice traz saneamento e moradia, que a renda não mede. A pergunta de quanto ele acrescenta continua em aberto e é dela."),
        ('Os pesos são estáveis?', f"Sim: em 1.000 reamostragens, a AUC municipal ficou entre {br(t45.loc['auc_municipal', 'p2_5'])} e {br(t45.loc['auc_municipal', 'p97_5'])}, e o peso de cada componente variou menos de dois pontos percentuais (análise E2). Tirar um município por vez também mexe pouco."),
        ('Quantas versões passam nos critérios?', f"{intbr(t61.loc['Todas', 'elegiveis'])} de {intbr(t61.loc['Todas', 'versoes'])}. Quando falham, o motivo mais comum é o banheiro graduado, que compartilha pouca variância com os outros componentes em alguns recortes."),
        ('Por que tirar o lixo?', f"Com o lixo, os dados pedem três fatores e a versão deixa de ser elegível (B5, AUC municipal {br(t60.loc['B5_lixo', 'auc_municipal'])}). No IVS-7 o lixo forma fator próprio, o que pode refletir a coleta de cada município e não a vulnerabilidade do setor."),
        ('Por que normalizar dentro do município?', f"Porque o índice compara setores da mesma cidade. Com min-max global (C3), a AUC municipal cai para {br(t60.loc['C3_normalizacao', 'auc_municipal'])}, contra {br(r['auc_municipal'])} na referência."),
        ('E o IVS-Idoso?', f"Somar envelhecimento ao índice (D2) apaga a vulnerabilidade: a AUC municipal cai para {br(t60.loc['D2_ivs_idoso', 'auc_municipal'])} e metade dos setores muda de faixa, porque setores mais envelhecidos tendem a ter renda maior. O cruzamento (E5) preserva as duas informações."),
        ('Por que sem bootstrap?', 'Porque ela pediu. A estabilidade é mostrada por sensibilidade por município (um de fora por vez) e, separadamente, pela reamostragem da análise E2, apresentada como reamostragem.'),
        ('Os setores rurais mudam alguma coisa?', f"Pouco: com rurais (A1), a correlação com a referência é {br(t60.loc['A1_com_rurais', 'spearman_com_referencia'])} e {pctbr(t60.loc['A1_com_rurais', 'pct_mudam_faixa'])} dos setores mudam de faixa."),
    ]


def paginas_do_deck(pptx: Path) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix='guia_orientadora_'))
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(tmp), str(pptx)], capture_output=True, check=True)
    subprocess.run(['swift', str(AQUI / 'folha_contato.swift'), str(tmp / (pptx.stem + '.pdf')), str(tmp) + '/pag/', '1', '1400'],
                   capture_output=True, check=True)
    return tmp / 'pag'


def main():
    registrar_fontes()
    S = estilos()
    dados = json.loads((UNI / 'deck_orientadora.json').read_text(encoding='utf-8'))
    mapa = json.loads((UNI / 'deck_orientadora_slides.json').read_text(encoding='utf-8'))
    pasta = paginas_do_deck(Path(dados['saida']))
    total = sum(len(m['slides']) for m in mapa)
    hist = []
    P = lambda t, e='corpo': hist.append(Paragraph(t, S[e]))

    # capa e como usar
    hist += [Spacer(1, 5 * cm)]
    P('Guia de estudo da apresentação', 'capa')
    P('Análises exploratórias e análise fatorial do IVS — cada slide explicado do zero', 'capa_sub')
    hist += [Spacer(1, 1 * cm)]
    P(f'{total} slides · Pedro Dias Soares · {date.today().strftime("%d/%m/%Y")}', 'pequeno')
    hist.append(PageBreak())
    P('Como usar este guia', 'h1')
    for t in ['Este guia acompanha o deck <i>Apresentacao_Orientadora_EDA_Fatorial_2026-10.pptx</i>, slide a slide, e supõe que você não sabe nada do assunto.',
              'Comece pelo glossário: ele explica, do zero, cada conceito que aparece nos slides. Depois, para cada slide, há a imagem do slide e seis blocos: <b>o que é</b> (o tipo de slide), <b>como ler</b>, <b>o que mostra</b> (o achado, com os números), <b>explicação</b> (o porquê, com os termos técnicos explicados), <b>tipo de gráfico</b> (quando há figura), <b>conceitos</b> (os termos do glossário que aparecem no slide) e <b>o que dizer</b> (uma sugestão de fala).',
              'No fim, perguntas que a orientadora pode fazer, com respostas apoiadas nos números do projeto.',
              'Todo número deste guia e do deck sai de um arquivo gerado por script; nenhum foi digitado. Se um número mudar, basta regerar os dois.']:
        P(t)
    P('As cinco partes', 'h2')
    for k, t in PARTES.items():
        P(f'<b>Parte {k}.</b> {esc(t)}')
    hist.append(PageBreak())

    # glossário
    P('Glossário — os conceitos do zero', 'h1')
    for grupo, itens in GLOSSARIO:
        P(esc(grupo), 'h2')
        for t, _, x in itens:
            P(f'<b>{esc(t)}.</b> {esc(x)}', 'termo')
    hist.append(PageBreak())

    # slide a slide
    for i, sl in enumerate(dados['slides']):
        nums = mapa[i]['slides']
        faixa = f'Slide {nums[0]}' if len(nums) == 1 else f'Slides {nums[0]} a {nums[-1]}'
        titulo = sl.get('titulo', '')
        if sl['tipo'] == 'secao':
            hist.append(CondPageBreak(12 * cm))
            P(f"Parte {esc(sl['num'])} — {esc(titulo)}", 'h1')
            P(esc(PARTES.get(sl['num'], '')))
        bloco = [Paragraph(f'{faixa} — {esc(titulo)}', S['h2'])]
        img = pasta / f'pagina_{nums[0]:03d}.png'
        if img.exists():
            bloco.append(Image(str(img), width=16 * cm, height=9 * cm))
        bloco.append(Spacer(1, 4))
        hist.append(KeepTogether(bloco))
        P('O QUE É', 'rot')
        P(esc(O_QUE_E.get(sl['tipo'], '')) + (f' Este conteúdo ocupa {len(nums)} slides seguidos.' if len(nums) > 1 else ''))
        if sl.get('como_ler'):
            P('COMO LER', 'rot')
            P(esc(sl['como_ler']))
        if sl.get('mostra'):
            P('O QUE MOSTRA', 'rot')
            P(esc(sl['mostra']))
        if sl['tipo'] in ('texto',):
            P('O QUE ESTÁ ESCRITO', 'rot')
            for t in sl['itens']:
                P('• ' + esc(t))
        if sl['tipo'] == 'numeros':
            P('OS NÚMEROS', 'rot')
            for v, r in sl['nums']:
                P(f'<b>{esc(v)}</b> — {esc(r)}')
        nota = sl.get('nota') or sl.get('texto') or ''
        if nota and sl['tipo'] not in ('texto', 'grade'):
            P('EXPLICAÇÃO', 'rot')
            P(esc(nota.split('\nComo ler:')[0]).replace('\n', '<br/>'))
        chave = sl.get('chave', '')
        g = next((TIPO[k] for k in sorted(TIPO, key=len, reverse=True) if chave.startswith(k) or chave == k), None)
        if g:
            P('TIPO DE GRÁFICO', 'rot')
            P(esc(GRAFICO[g]))
        if sl['tipo'] == 'grade':
            P('AS FIGURAS DESTA PÁGINA', 'rot')
            for c in sl['cels']:
                P(f"<b>{esc(c['rotulo'])}</b> — {esc(c['titulo'])}")
        texto_slide = ' '.join(str(sl.get(k, '')) for k in ('titulo', 'como_ler', 'mostra', 'nota', 'texto')) + ' '.join(sl.get('itens', []))
        conceitos = [t for t, p, _ in TERMOS if p.search(texto_slide)]
        if conceitos and sl['tipo'] not in ('capa', 'grade'):
            P('CONCEITOS DESTE SLIDE (VER O GLOSSÁRIO)', 'rot')
            P(esc(' · '.join(conceitos[:12])))
        if sl['tipo'] in ('figura', 'figura_larga', 'tabela', 'numeros'):
            P('O QUE DIZER', 'rot')
            fala = sl.get('mostra') or sl.get('texto', '')
            P('“' + esc((sl.get('como_ler', '').split('.')[0] + '. ') if sl.get('como_ler') else '') + esc(fala) + '”')
        hist.append(Spacer(1, 10))

    # perguntas prováveis
    hist.append(PageBreak())
    P('Perguntas que a orientadora pode fazer', 'h1')
    for q, r in numeros_respostas():
        P(f'<b>{esc(q)}</b>', 'corpo')
        P(r)

    def rodape(c, doc):
        c.saveState()
        c.setFont('Serif-I', 8.5)
        c.setFillColor(CINZA)
        c.drawString(2 * cm, 1.2 * cm, 'Guia de estudo · Análises exploratórias e análise fatorial do IVS')
        c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, str(doc.page))
        c.restoreState()

    doc = SimpleDocTemplate(str(SAIDA), pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm,
                            bottomMargin=2 * cm, title='Guia de estudo da apresentação', author='Pedro Dias Soares')
    doc.build(hist, onFirstPage=rodape, onLaterPages=rodape)
    print(f'{SAIDA.relative_to(RAIZ)}: {doc.page} páginas, {total} slides')


if __name__ == '__main__':
    main()
