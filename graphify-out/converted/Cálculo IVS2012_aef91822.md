<!-- converted from Cálculo IVS2012.docx -->











Baixar os dados do Censo 2022:
https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html


















Construção de indicadores para escolha daqueles que comporão o IVS 2012


A) Componente SANEAMENTO

# 1- Percentual de domicílios particulares permanentes com abastecimento de água inadequado ou ausente

Numerador Tabela: Domicilio01_UF.xls

(Agua_Inade)



Denominador Tabela: Domicilio01_UF.xls

(Dom_part



# 2- Percentual de domicílios particulares permanentes com esgotamento sanitário inadequado ou ausente

Numerador Tabela: Domicilio01_UF.xls

(Esg_Inadeq)

Denominador Tabela: Domicilio01_UF.xls

(Dom_part_p)


# 3- Percentual de domicílios particulares permanentes com destino do lixo de forma inadequada ou ausente

Numerador Tabela: Domicilio01_UF.xls

(Lixo_inad)

Denominador Tabela: Domicilio01_UF.xls

(Dom_part_p)






















B) Componente HABITAÇÃO

# 5- Razão de moradores por domicílio

Numerador Tabela: Pessoa13_UF.xls

(Res_part_p)


Denominador Tabela:

Domicílios particulares permanentes


Domicilio01_UF.xls

(Dom_part_p)


























C) Componente ESCOLARIDADE
# 6- Percentual de pessoas analfabetas = 1 – Numerador/Denominador


Numerador Tabela: Pessoa01_UF.xls

(Alfab_5_ma)

Denominador Tabela: Pessoa13_UF.xls

(Pop_5_mais)
























D) Componente RENDA

# 9- Percentual de domicílios particulares com rendimento per capita até ½ SM

Numerador Tabela: DomicílioRenda_UF.xls
(Rend_1_2)


Denominador Tabela:

Domicílios particulares permanentes + Total de domicílios particulares improvisados

Domicilio01_UF.xls

(Dom_part_p)


DomicilioRenda_UF.xls

( Dom_improv)


# 10- Rendimento nominal mensal médio das pessoas responsáveis (invertido) = 1 – (Renda média do setor /maior valor)

Variável (Renda_media)

Numerador Tabela: ResponsavelRenda_UF.xls
(Tot_rend_r)


Denominador Tabela: Pessoa13_UF.xls (Tot_resp)

E) Componente SOCIAL

# 12- Percentual de pessoas de raça/cor parda, preta ou indígena

Numerador Tabela: Pessoa03_UF.xls
(Neg_ind_Pard)


Denominador Tabela: Pessoa03_UF.xls

(Pop_total)























# ================
Tratamento dos dados
Campo identificando se setor tem dados sigilosos.  Os dados originalmente marcados como “X” foram convertidos para “-1”.
Conceito de domicílio coletivo é por leito e relações de parentesco.  Por exemplo, um asilo com 60 moradores (leitos) sem relação de parentesco conta como 60 domicílios coletivos.  Esse valor conta para a totalização dos domicílios do setor.
Assim, achamos melhor considerar o número de responsáveis como número total de domicílios do setor.
Devido a não disponibilização de alguns dados sobre os domicílios coletivos, optamos por não considerar os setores onde o percentual de domicílios coletivos fosse igual a 100% do total de domicílios do setor.
Consideramos o número de domicílios coletivos do setor =
Total de responsáveis – Domicílios particulares permanentes – Domicílios improvisados
Percentual de domicílios coletivos =
Domicílios coletivos / Total de responsáveis *100
Criamos uma coluna ( Dados_sig) para avaliar se o setor participa ou não da análise, baseando na disponibilidade de dados.
Setores com dados sigilosos (SIGILOSO) = não participam (57 setores)
Setores com 100% de domicílios coletivos (COLETIVO) = não participam (07 setores)
Setores com população = 0 (ZERADO) = não participam (41 setores)
Setores que participam (OK) (3831 setores)
Criamos a coluna observação para esclarecer sobre estes setores.
Cobertura do entorno estimada em 99,85% (= total de domicílios do entorno/ total de domicílios particulares permanentes)
V001 tabela Entorno01 / V002 tabela Domicilio01
Houve setores com até 75% de domicílios improvisados. Optamos por deixá-los incluídos na análise.

# CONVERSÃO DE ESCALA

Valor convertido = valor bruto   –   valor mínimo       	 	 	 valor máximo – valor mínimo
| V013 | Domicílios particulares permanentes com abastecimento de água de poço ou nascente na propriedade |
| --- | --- |
| V014 | Domicílios particulares permanentes com abastecimento de água da chuva armazenada em cisterna |
| V015 | Domicílios particulares permanentes com outra forma de abastecimento de água |
| V002 | Domicílios particulares permanentes |
| --- | --- |
| V019 | Domicílios particulares permanentes com banheiro de uso exclusivo dos moradores ou sanitário e esgotamento sanitário via fossa rudimentar |
| --- | --- |
| V020 | Domicílios particulares permanentes com banheiro de uso exclusivo dos moradores ou sanitário e esgotamento sanitário via vala |
| V021 | Domicílios particulares permanentes, com banheiro de uso exclusivo dos moradores ou sanitário e esgotamento sanitário via rio, lago ou mar |
| V022 | Domicílios particulares permanentes com banheiro de uso exclusivo dos moradores ou sanitário e esgotamento sanitário via outro escoadouro |
| V023 | Domicílios particulares permanentes sem banheiro de uso exclusivo dos moradores e nem sanitário |
| V037 | Domicílios particulares permanentes com lixo coletado em caçamba de serviço de limpeza |
| --- | --- |
| V038 | Domicílios particulares permanentes com lixo queimado na propriedade |
| V039 | Domicílios particulares permanentes com lixo enterrado na propriedade |
| V040 | Domicílios particulares permanentes com lixo jogado em terreno baldio ou logradouro |
| V041 | Domicílios particulares permanentes com lixo jogado em rio, lago ou mar |
| V042 | Domicílios particulares permanentes com outro destino do lixo |
| V002 | Domicílios particulares permanentes |
| --- | --- |
| V002 | Pessoas residentes em domicílios particulares permanentes |
| --- | --- |
| V002 | Domicílios particulares permanentes |
| --- | --- |
| V001 | Pessoas alfabetizadas com 5 ou mais anos de idade |
| --- | --- |
| V039 |  | Pessoas com 5 anos de idade |
| --- | --- | --- |
| V040 |  | Pessoas com 6 anos de idade |
|  | ... | ... |
| V133 |  | Pessoas com 99 anos de idade |
| V134 |  | Pessoas com 100 anos ou mais de idade |
| V005 | Domicílios particulares com rendimento nominal mensal domiciliar per capita de até 1/8 salário mínimo |
| --- | --- |
| V006 | Domicílios particulares com rendimento nominal mensal domiciliar per capita de mais de 1/8 a 1/4 salário mínimo |
| V007 | Domicílios particulares com rendimento nominal mensal domiciliar per capita de mais de 1/4 a 1/2 salário mínimo |
| V002 | Domicílios particulares permanentes |
| --- | --- |
| V001 | Total de domicílios particulares improvisados |
| --- | --- |
| V022 | Total do rendimento nominal mensal das pessoas responsáveis |
| --- | --- |
| V003 | Responsáveis pelos domicílios particulares |
| --- | --- |
| V003 | Pessoas Residentes e cor ou raça - preta |
| --- | --- |
| V005 | Pessoas Residentes e cor ou raça - parda |
| V006 | Pessoas Residentes e cor ou raça - indígena |
| V001 | Pessoas Residentes |
| --- | --- |