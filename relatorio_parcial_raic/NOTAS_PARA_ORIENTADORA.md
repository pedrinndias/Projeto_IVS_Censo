# Notas para a orientadora — relatório parcial RAIC 2026 (v1)

Arquivo: `Relatorio_Parcial_RAIC_2026_Pedro_v1.docx`, gerado por `scripts/gerar_relatorio_raic.py`.
A Introdução (1º e 2º parágrafos), os Objetivos, a Metodologia (até o parágrafo sobre ética),
o Quadro 1 e as Referências foram **copiados do Plano de trabalho**. Abaixo está tudo o que
mudou em relação ao texto original, para conferência.

## 1. Correções feitas no texto copiado

| # | No Plano | No relatório | Motivo |
|---|---|---|---|
| 1 | (Agero, 2020; IBGE, 2022) | (Agero et al., 2020; IBGE, 2022) | a referência é "AGERO, P. et al." |
| 2 | (Buss; Pellegrinni Filho, 2007) | (Buss; Pellegrini Filho, 2007) | grafia da referência |
| 3 | pode contribuir paras as evidências | pode contribuir para as evidências | digitação |
| 4 | os 70 municípios compõem a amostra | os 70 municípios que compõem a amostra | faltava "que" |
| 5 | corresponde a menor unidade territorial | corresponde à menor unidade territorial | crase |
| 6 | disponíveis no censo … e compõe o IVS de 2012 | … e compõem o IVS de 2012 | concordância |
| 7 | Conselho Nacional da Saúde | Conselho Nacional de Saúde | nome oficial |
| 8 | nos termos do artigo da Lei 13,709/2018 | nos termos da Lei 13.709/2018 | faltava o número do artigo; se houver um artigo específico, reinserir |
| 9 | objetivos específicos com travessão | numerados 1 e 2 | a seção V se refere a eles pelo número |
| 10 | Quadro 1 sem fonte | "Fonte: SMS (2013)." | as variáveis são as do IVS de 2012 |
| 11 | Quadro 1 sem linha de cabeçalho | cabeçalho "Dimensão / Variável" | mesmo padrão do Quadro 2 |

Nas **referências**:
- foram postas em ordem alfabética (AGERO antes de ALLIK; GIOIA antes de INSTITUTO);
- "PELLEGRINI FILHO, A.." perdeu o ponto duplicado;
- o periódico de Agero e o de Kalache (*Rev. Bras. Geriatr. Gerontol.*) ganharam o negrito que os demais periódicos já tinham;
- o nome do periódico de Gioia ficou todo em negrito;
- a entrada do IBGE "Censo demográfico 2022" ganhou "Rio de Janeiro: IBGE, 2022.", porque não tinha local, editora nem data de publicação (NBR 6023).

## 2. Mantido como no Plano, mas vale confirmar

- **"Gioia et al., 2020"**: a obra tem três autores. Pela NBR 10520:2023, "et al." é para quatro ou mais. Manter assim ou citar os três?
- **Verbos no futuro na Metodologia** ("Serão selecionados", "será construído"): mantidos como no Plano. O que foi executado está na subseção nova "Procedimentos executados e adequações ao Censo Demográfico 2022".
- **"Qgis 2.10.1"**: mantido. A subseção nova informa que os mapas serão feitos no QGIS 3.x.
- **"(básico, população, domicílio e rendimento)"**: mantido. A subseção nova lista os arquivos efetivamente usados.
- **Resolução 510/2016 e LGPD**: estão na bibliografia, mas no texto aparecem só pelo nome, sem "(Brasil, 2016)" nem "(Brasil, 2018)". Acrescentar as citações?
- **"SMS - Secretaria Municipal de Saúde"**: pela NBR 6023, um órgão da administração direta entra como "BELO HORIZONTE. Secretaria Municipal de Saúde." A mudança exigiria trocar "(SMS, 2013)" por "(Belo Horizonte, 2013)" em 4 lugares. Não foi feita.
- **Referência da fonte de dados**: a bibliografia só tem a página geral do Censo 2022. Se preferir citar especificamente os "agregados por setores censitários" do IBGE, indicar qual referência usar (ano e URL da publicação).

## 3. Referências acrescentadas

| Referência | Por quê |
|---|---|
| BRASIL, Res. CNS 510/2016 | citada no texto do Plano, sem entrada na lista |
| BRASIL, Lei 13.709/2018 (LGPD) | idem |
| LIMA-COSTA et al., 2018 (ELSI-Brasil, *Am J Epidemiol*) | o ELSI só aparecia por URL. **Confirmar se é a referência preferida** |
| GALVÃO et al., 2025 (*Hygeia*) | definição dos grupos etários do índice de envelhecimento, a mesma usada no projeto |

## 4. Texto novo (não estava no Plano)

- Introdução: 3º parágrafo, que liga a justificativa ao objetivo e diz o que o relatório cobre.
- Metodologia: a subseção de procedimentos e adequações e o Quadro 2.
- Seções V, VI e VII.
- Perspectivas, Outras atividades e Observação.

Todos os números da Tabela 1, da Figura 1 e do Quadro 2 saem de
`scripts/pecas_relatorio_raic.py`. Os demais vêm do relatório da EDA.

## 5. Uma correção nos números já mostrados

O máximo do analfabetismo na Tabela 1 é **0,725**, e não 0,726: o valor exato é
37/51 = 0,72549…; o 0,726 vinha de arredondar duas vezes.

## 6. O que falta preencher (em amarelo no .docx)

1. Orientador(a).
2. Coorientador(es) ou "Não se aplica".
3. Laboratório ou grupo de pesquisa.
4. Programa de vínculo.
5. Dia de início em março/2026.
6. Universidade e curso.
7. Dia da data da capa.
8. Matéria encaminhada: confirmar "nenhuma".
9. Outras atividades: Programa de Inserção, Curso Introdutório, eventos.
10. Avaliação: texto do bolsista.
11. Apoio: órgão financiador.

O título do trabalho também precisa ser confirmado: foi usado o do guia do projeto.

## 7. Revisão de 11/10 (conselho de revisores + texto mais direto)

O texto **novo** foi reescrito para ficar mais direto, com frases mais curtas e sem fórmulas. O
texto copiado do Plano não mudou: as 12 frases literais foram conferidas uma a uma. Nenhum dado
saiu: os números foram comparados antes e depois da reescrita. Mudanças de conteúdo:

- **Correlações (Figura 1).** Entraram duas checagens de robustez, geradas por `scripts/pecas_relatorio_raic.py`.
  - Com todos os setores disponíveis para cada par, os coeficientes quase não mudam (idosos × renda: −0,52).
  - Dentro de cada município, também não (−0,54). Em 50 dos 53 municípios com 30 ou mais setores completos, idosos × renda é negativa.
  - A exceção é água × esgoto: 0,40 no conjunto, mas 0,22 dentro dos municípios. A associação vem sobretudo das diferenças entre cidades.
- **Discussão.**
  - A padronização dentro de cada município passou a ser justificada pelo caráter intraurbano do índice, e não pela assimetria.
  - A assimetria fica como ponto a tratar, com método a definir.
  - Sobre idosos, o texto agora diz "é compatível com", e não "indica".
  - O −0,79 entre idosos e crianças é em parte construído, porque as duas proporções têm o mesmo denominador.
- **Regiões.**
  - O gradiente Norte–Sul agora é descrito em 4 indicadores, e não em 5.
  - O texto diz que Brasília tem 4.924 dos 9.490 setores do Centro-Oeste.
  - Como o Norte tem 6 municípios na amostra, os contrastes descrevem os municípios estudados.
- **Conclusões.** O processamento foi "conferido com a população e o índice de envelhecimento do IBGE", e não "validado".
- **Folha de rosto.** O campo "Coorientador(es): Não se aplica" voltou, porque o Anexo 1 o exige. O Pedro tinha retirado a linha.
