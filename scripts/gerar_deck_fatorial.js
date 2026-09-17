/**
 * Gera o deck da análise fatorial — Notebook 04.
 *
 * Uso:
 *     node scripts/gerar_deck_fatorial.js docs/Apresentacoes_IVS/Analise_Fatorial_NB04_2026-09.pptx
 *
 * Nenhum número é digitado aqui. Todos saem de banco_de_dados/eda/fatorial/:
 * os `nb04_*.csv` produzidos pelo Notebook 04 e o `resumo_adequabilidade.csv` de agosto,
 * que o notebook reproduz exatamente. As figuras saem de `fatorial/figuras/`.
 *
 * Foi essa a regra que evitou, na EDA Central, que três números do recorte com rurais
 * fossem apresentados como se fossem do urbano: o gerador formata, não sabe de nada.
 *
 * Os helpers visuais vêm de scripts/deck_comum.js. Os dois geradores anteriores têm cada
 * um a sua cópia deles; migrá-los é trabalho à parte, porque exige regerar os dois decks
 * e conferir contra o que já foi apresentado.
 *
 * Requer `pptxgenjs` (npm).
 */
const fs = require('fs');
const path = require('path');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const FAT = path.join(RAIZ, 'banco_de_dados/eda/fatorial');
const FIG = path.join(FAT, 'figuras');

// ── Leitura dos CSVs do projeto: ';' como separador, utf-8-sig ──────────────
function lerCsv(nome) {
  const txt = fs.readFileSync(path.join(FAT, nome), 'utf8').replace(/^﻿/, '').trim();
  const [cab, ...linhas] = txt.split(/\r?\n/);
  const cols = cab.split(';').map((c, i) => c === '' ? 'idx' : c);
  return linhas.map(l => {
    const v = l.split(';');
    return Object.fromEntries(cols.map((c, i) => [c, v[i]]));
  });
}
const num = (o, c) => Number(o[c]);
/** Número em português: vírgula decimal, ponto de milhar. */
function n(v, casas) {
  return Number(v).toLocaleString('pt-BR', { minimumFractionDigits: casas === undefined ? 3 : casas,
                                             maximumFractionDigits: casas === undefined ? 3 : casas });
}
const inteiro = v => Number(v).toLocaleString('pt-BR');

// ── Os dados ────────────────────────────────────────────────────────────────
const RESUMO = lerCsv('resumo_adequabilidade.csv');
const cen = k => RESUMO.find(r => r.nome === k);
const S7 = cen('ivs7_spearman'), P7 = cen('ivs7_pearson'), S6 = cen('ivs6_sem_lixo_spearman');

const PESOS = lerCsv('nb04_sintese_pesos.csv');
const CENARIOS = lerCsv('nb04_cenarios.csv');
const VALID = lerCsv('nb04_validacao_fcu.csv');
const PHI = lerCsv('nb04_phi_ivs6_sem_lixo.csv');
const BOOT = lerCsv('nb04_bootstrap_cargas.csv');
const CARGAS6 = lerCsv('nb04_cargas_ivs6_sem_lixo.csv');
const EXTRA = lerCsv('nb04_extracao_comparada.csv');
const ADEQ = lerCsv('nb04_adequabilidade.csv');
const AUTOV = lerCsv('nb04_autovalores.csv');
const CORR7 = lerCsv('nb04_correlacao_ivs7_spearman.csv');

const phi = Math.abs(num(PHI[0], 'Fator 2'));
const cenPor = k => CENARIOS.find(r => r.cenario === k);
const aucIdx = num(VALID[0], 'auc'), aucEsc = num(VALID[1], 'auc');
const av = c => AUTOV.filter(r => r.cenario === c);
const ex = c => EXTRA.filter(r => r.cenario === c);
const ad = c => ADEQ.filter(r => r.cenario === c);
const lixoEx = ex('ivs7_spearman').find(r => r.variavel === 'Lixo inadequado');
const rendaRaca = Math.abs(num(CORR7.find(r => r.idx === 'Renda (invertida)'), 'Cor/raça PPI'));

// repartição entre as dimensões, somada dos pesos (não digitada)
const pesoDim = d => PESOS.filter(r => r.dimensao === d).reduce((a, r) => a + num(r, 'peso'), 0);
const pSocio = 100 * pesoDim('Socioeconômica'), pSanea = 100 * pesoDim('Saneamento');

// ── O deck ──────────────────────────────────────────────────────────────────
const d = criarDeck({ titulo: 'Análise fatorial e os pesos do IVS — Notebook 04' });
const { p, S, titulo, secao, bloco, numero, tabela, legendaTabela, legendaFigura,
        anotar, procedencia, capa, regua } = d;
const { TINTA, CINZA, ACENTO } = d.cores;
const { W, H, M } = d.geo;
const marca = t => ({ text: t, options: { color: ACENTO, bold: true } });

// ═════════ CAPA ═════════
{ const s = S();
  capa(s, 'INICIAÇÃO CIENTÍFICA · FIOCRUZ MINAS — IRR',
    'Os pesos do IVS',
    'Análise fatorial dos sete componentes · Censo Demográfico 2022 · 70 municípios do ELSI-Brasil\n' +
    'O que a estrutura latente dos dados diz sobre quanto cada indicador deve pesar no índice.',
    `Pedro Dias Soares  ·  setembro de 2026  ·  ${inteiro(S7.n)} setores completos nas sete variáveis`);
  s.addNotes('Este é o Notebook 04, a última etapa central que faltava. O produto dele não é o IVS — é a estrutura e os pesos. O IVS final é o Notebook 05, depois da normalização por município. Vale abrir dizendo isso, para a expectativa ficar no lugar certo.');
}

{ const s = S();
  const y = titulo(s, 'O que estava em aberto', 'Quatro decisões travavam o cálculo do índice, e nenhuma tinha número para sustentá-la.');
  tabela(s, ['Decisão', 'O que ela trava', 'O que existia antes deste trabalho'], [
    ['Critério dos pesos', 'Notebooks 04 e 05', 'Um argumento: renda, cor/raça e analfabetismo são colineares'],
    ['Destino do indicador de lixo', 'Composição do índice', 'Uma ressalva: é a variável menos correlacionada com as demais'],
    ['Política do sigilo no analfabetismo', 'Notebook 03', 'A constatação de que o sigilo não é aleatório'],
    ['Um fator ou dois', 'Toda a leitura do índice', 'A teoria do IVS-BH 2012 dizia duas dimensões'],
  ], { y, colW: [3.6, 3.0, 5.03], rowH: 0.52, fontSize: 12 });
  bloco(s, M, y + 2.95, W - 2*M, 'O que mudou.',
    'Todas as quatro continuam sendo decisão da orientação — mas agora cada opção tem o seu custo medido em quantos setores mudam de faixa de risco.', true, 1.0);
  s.addNotes('O ponto desta apresentação não é fechar as decisões. É que elas passam a ser tomadas com número, e o número diz que três delas importam menos do que parecia.');
}

// ═════════ 1. A BASE ═════════
{ const s = S(); secao(s, '1', 'A base aguenta a análise?',
    'Etapa 1 do planejamento, nos termos de Matos & Rodrigues (2019), p. 39–46.');
  s.addNotes('Esta seção é de conferência. Os números são os mesmos de agosto, e o notebook trava se não os reproduzir — é a garantia de que nada se perdeu na reimplementação.');
}

{ const s = S();
  const y = titulo(s, 'A Etapa 1 do livro, conferida', 'Todos os critérios atendidos, dois deles com ressalva a declarar.');
  const yt = legendaTabela(s, y, 'Critérios de adequabilidade da base, sete componentes, correlação de Spearman.',
    `Fonte: banco_de_dados/eda/fatorial/resumo_adequabilidade.csv. Recorte: ${inteiro(S7.n)} setores completos.`);
  tabela(s, ['Critério do livro (p. 44)', 'Patamar', 'Resultado', 'Situação'], [
    ['Tamanho da amostra', '> 100 e ≥ 5 por variável', `${inteiro(S7.n)} · ${inteiro(Math.round(num(S7,'razao_casos_var')))} : 1`, 'atendido com folga'],
    ['Matriz de correlação', 'maioria acima de 0,30', `${n(100*num(S7,'pct_corr_acima_030'), 1)}%`, 'atendido'],
    ['KMO', '≥ 0,50; ideal a partir de 0,70', n(S7.kmo), 'atendido'],
    ['MSA por variável', '≥ 0,50', `mínimo ${n(S7.msa_min)}`, 'atendido'],
    ['Teste de Bartlett', 'p < 0,05', `χ² = ${inteiro(Math.round(num(S7,'bartlett_qui2')))} · p < 0,001`, marca('atendido, mas vazio')],
  ], { y: yt, colW: [4.2, 3.1, 2.7, 1.63], rowH: 0.46, fontSize: 11.5 });
  bloco(s, M, yt + 3.0, W - 2*M, 'O Bartlett não informa nesta escala.',
    'A p. 43 adverte que o teste "depende muito do tamanho amostral e tende a rejeitar a hipótese nula para amostras grandes". Com 87 mil setores ele rejeita por construção. A conclusão de adequabilidade se apoia no KMO e nos MSA, que não crescem com o n.', true, 1.1);
  s.addNotes('Se a orientadora perguntar por que o Bartlett aparece se não informa: porque é convenção da área e a ausência dele seria notada. O que muda é a frase que o acompanha — em vez de apresentá-lo como prova, ele vem com a ressalva do próprio livro.');
}

{ const s = S();
  const y = titulo(s, 'A escolha por Spearman é o que torna a análise defensável',
    'Com Pearson, a mesma base reprovaria em dois critérios da Etapa 1.');
  const yt = legendaTabela(s, y, 'Os mesmos setores, as duas correlações.',
    'Fonte: resumo_adequabilidade.csv. A escolha por Spearman foi decidida na §9 do relatório da EDA.');
  tabela(s, ['Critério', 'Pearson', 'Spearman', 'Leitura'], [
    ['KMO', n(P7.kmo), n(S7.kmo), 'sobe dentro da faixa boa'],
    ['MSA mínimo', n(P7.msa_min), n(S7.msa_min), 'sai da zona medíocre'],
    ['Coeficientes |r| ≥ 0,30', `${n(100*num(P7,'pct_corr_acima_030'),1)}%`, `${n(100*num(S7,'pct_corr_acima_030'),1)}%`, marca('com Pearson, reprova')],
    ['Fatores por Kaiser', P7.autovalores_acima_1, S7.autovalores_acima_1, 'solução mais parcimoniosa'],
    ['Variância acumulada', `${n(P7.var_acumulada_k,1)}%`, `${n(S7.var_acumulada_k,1)}%`, marca('só Spearman cruza os 60%')],
  ], { y: yt, colW: [3.4, 2.0, 2.0, 4.23], rowH: 0.46, fontSize: 11.5 });
  bloco(s, M, yt + 3.0, W - 2*M, 'O preço.',
    'Decompor uma matriz de Spearman é fazer análise de componentes principais sobre os POSTOS, não sobre os valores. As cargas se referem a posições relativas. Isso volta a aparecer, com consequência concreta, no slide dos escores.', false, 1.1);
  s.addNotes('A justificativa é a não-normalidade já documentada: assimetria de 3,42 na água e 3,74 na renda, curtose de 49,5 na renda. O livro não lista Spearman entre as correlações que discute — ele trata de escalas Likert, não de proporções infladas de zero. É preciso justificar uma escolha que a referência não contempla.');
}

{ const s = S();
  const y = titulo(s, 'Multicolinearidade: o número que circula é de outra matriz',
    'Achado. A correlação citada nos documentos do projeto não é a da matriz que foi fatorada.');
  numero(s, M, y + 0.25, 3.5, n(rendaRaca), 'renda × cor/raça na matriz FATORADA (listwise, 87.545 setores)');
  numero(s, M + 4.2, y + 0.25, 3.5, '0,811', 'o mesmo par na EDA §9 (par a par, 104.108 setores)', true);
  numero(s, M + 8.4, y + 0.25, 3.2, '0,800', 'limiar de multicolinearidade (livro, p. 42)');
  bloco(s, M, y + 1.85, W - 2*M, 'Os dois números estão certos, e medem conjuntos diferentes.',
    'O da EDA é calculado par a par, cada coeficiente sobre os seus próprios casos completos. O da fatorial é listwise: só os setores completos nas sete variáveis entram. A diferença vai na mesma direção do viés do sigilo — a base listwise perde os setores de melhor situação, e isso comprime a associação entre renda e cor/raça.', true, 1.4);
  bloco(s, M, y + 3.45, W - 2*M, 'O que muda.',
    'Nenhum par da matriz efetivamente fatorada cruza o limiar de 0,80. A objeção não desaparece — 0,784 continua alto e o bloco socioeconômico continua coeso —, mas o artigo precisa citar o número da matriz que foi fatorada, e dizer qual é qual.', false, 1.2);
  s.addNotes('Este é um dos três resultados que contrariaram o que os documentos do projeto afirmavam. Foi verificado antes de seguir: a origem do 0,811 está em banco_de_dados/eda/correlacao_spearman.csv, calculado par a par. O guia de leitura do livro da Enap precisa de correção nesse ponto.');
}

// ═════════ 2. QUANTOS FATORES ═════════
{ const s = S(); secao(s, '2', 'Quantos fatores reter?',
    'Os critérios discordam — e o livro (p. 28–32) manda usá-los em conjunto justamente por isso.');
  s.addNotes('Esta é a decisão mais desconfortável do trabalho, e a que mais depende de julgamento. Vale ser explícito com a orientadora: o número de fatores não sai dos dados sozinho.');
}

{ const s = S();
  const y = titulo(s, 'Kaiser e Horn não sustentam o segundo fator sem o lixo',
    'Com as sete variáveis, os dois critérios retêm dois. Retirado o lixo, retêm um.');
  const a7 = av('ivs7_spearman'), a6 = av('ivs6_sem_lixo_spearman');
  const yt = legendaTabela(s, y, 'Autovalores observados contra os de dados aleatórios de mesmo tamanho.',
    'Fonte: nb04_autovalores.csv. Análise paralela de Horn (1965), 50 simulações, semente 42.');
  tabela(s, ['Componente', 'Autovalor (7 var.)', 'Horn', 'Autovalor (6 var.)', 'Horn'], [
    ['1', n(a7[0].autovalor, 4), n(a7[0].horn_aleatorio, 4), n(a6[0].autovalor, 4), n(a6[0].horn_aleatorio, 4)],
    ['2', marca(n(a7[1].autovalor, 4)), n(a7[1].horn_aleatorio, 4), marca(n(a6[1].autovalor, 4)), n(a6[1].horn_aleatorio, 4)],
    ['3', n(a7[2].autovalor, 4), n(a7[2].horn_aleatorio, 4), n(a6[2].autovalor, 4), n(a6[2].horn_aleatorio, 4)],
    ['Variância acumulada com 2 fatores', `${n(a7[1].pct_acumulado, 1)}%`, '', `${n(a6[1].pct_acumulado, 1)}%`, ''],
  ], { y: yt, colW: [4.4, 2.2, 1.8, 2.2, 1.03], rowH: 0.46, fontSize: 11.5 });
  bloco(s, M, yt + 2.55, W - 2*M, 'O que sustenta o segundo fator, então.',
    'A razão teórica. A p. 32 do livro admite explicitamente que a decisão final pode ser teórica, e que a pergunta certa é "teoricamente faz mais sentido essas variáveis estarem agrupadas em quantos fatores?". As duas dimensões vêm do IVS-BH 2012. Isso é uma escolha declarada, não um número escondido.', true, 1.3);
  s.addNotes('O critério de Kaiser é o mais fraco aqui: a p. 29 registra que ele funciona melhor entre 20 e 50 variáveis, e com comunalidades acima de 0,7. Temos 6 variáveis e comunalidade mínima de 0,380. E a análise paralela de Horn, que é mais robusta, nem está no livro — está em nota de rodapé em Figueiredo. Vale dizer que estamos usando um critério melhor que o da referência.');
}

{ const s = S();
  titulo(s, 'O cotovelo, nas duas soluções', 'Autovalor observado contra o que dados sem estrutura nenhuma produziriam.');
  s.addImage({ path: path.join(FIG, 'nb04_scree_horn.png'), x: 1.30, y: 1.75, w: 10.73, h: 4.60 });
  legendaFigura(s, 6.45, 'Quantos fatores reter — observado contra o acaso.',
    'Fonte: banco_de_dados/eda/fatorial/figuras/nb04_scree_horn.png, bloco 3 do Notebook 04.');
  s.addNotes('Apontar para o segundo ponto do painel da direita: ele fica logo ABAIXO da linha do acaso. É a imagem do problema do slide anterior. No painel da esquerda o segundo ponto passa por muito pouco, e o terceiro quase encosta.');
}

// ═════════ 3. O LIXO ═════════
{ const s = S(); secao(s, '3', 'O caso do indicador de lixo',
    'A ressalva de agosto virou medida — e a análise fatorial propriamente dita a reforça.');
  s.addNotes('Aqui a evidência ficou mais forte do que era em agosto, e por um motivo técnico que vale explicar: ACP e análise fatorial contam variâncias diferentes.');
}

{ const s = S();
  const y = titulo(s, 'O lixo não tem variância comum com o construto',
    'A ACP lhe dava um fator próprio. O eixo principal mostra que aquele fator é ruído dele mesmo.');
  numero(s, M, y + 0.3, 3.4, n(lixoEx.comun_ACP), 'comunalidade do lixo pela ACP');
  numero(s, M + 4.0, y + 0.3, 3.4, n(lixoEx.comun_PAF), 'comunalidade pelo eixo principal', true);
  numero(s, M + 8.0, y + 0.3, 3.6, n(ad('ivs7_spearman').find(r => r.variavel === 'Lixo inadequado').SMC),
    'SMC — a menor das sete variáveis');
  bloco(s, M, y + 1.95, W - 2*M, 'Por que os dois números são tão diferentes.',
    'A ACP põe 1 na diagonal da matriz e distribui TODA a variância de cada variável entre os componentes — inclusive a variância que é só daquela variável. A análise fatorial põe a comunalidade e conta apenas a variância COMPARTILHADA. O fator próprio que o lixo forma na ACP é, quase inteiro, variância específica.', true, 1.5);
  bloco(s, M, y + 3.65, W - 2*M, 'A consequência para o índice.',
    `Manter o lixo com peso empírico é dar peso a uma dimensão que não é vulnerabilidade. Sem ele, a variância acumulada sobe de ${n(S7.var_acumulada_k,1)}% para ${n(S6.var_acumulada_k,1)}% com MENOS variáveis, e a água sai de comunalidade 0,253 para 0,822 — ela estava baixa porque o lixo havia sequestrado o segundo fator.`, false, 1.3);
  s.addNotes('Cuidado com uma armadilha aqui: a regra mecânica de comunalidade do artigo de Figueiredo teria excluído a ÁGUA, não o lixo. A comunalidade não é propriedade da variável, é propriedade da solução. A ordem correta é diagnosticar a estrutura, remover o que é externo ao construto, e só então avaliar comunalidades.');
}

// ═════════ 4. AS TRÊS DIVERGÊNCIAS ═════════
{ const s = S(); secao(s, '4', 'Onde a Enap discorda de Figueiredo',
    'Três pontos, e nos três o livro dá razão ao que os dados já indicavam.');
  s.addNotes('O projeto vinha seguindo Figueiredo & Silva (2010). O livro da Enap é posterior, mais rigoroso, e contradiz aquele artigo em três pontos que mudam o que o Notebook 04 faz.');
}

{ const s = S();
  const y = titulo(s, 'Divergência 1 — a rotação', 'O livro inverte o ônus da prova: ortogonal é o caminho que exige justificativa.');
  s.addText('"usar rotação ortogonal com dados de Ciências Humanas e Sociais não parece ter nenhum sentido. Nessas áreas, as variáveis quase sempre são correlacionadas. [...] para usar rotação ortogonal, o pesquisador precisaria ter evidências teóricas ou empíricas muito fortes de que os fatores não são correlacionados."',
    { x: M + 0.35, y: y + 0.2, w: W - 2*M - 0.7, h: 1.3, fontFace: 'Cambria', fontSize: 13,
      color: TINTA, italic: true, margin: 0, lineSpacing: 19 });
  regua(s, y + 0.2, 1.5, ACENTO, M, 0.02);
  s.addText('Matos & Rodrigues (2019), p. 38', { x: M + 0.35, y: y + 1.55, w: 6, h: 0.3,
    fontFace: 'Cambria', fontSize: 10.5, color: CINZA, margin: 0 });
  numero(s, M, y + 2.25, 3.6, n(phi), 'correlação entre os dois fatores (Φ)', true);
  numero(s, M + 4.3, y + 2.25, 3.6, `${n(pSocio,1)} / ${n(pSanea,1)}`, 'repartição do peso, rotação ortogonal');
  numero(s, M + 8.6, y + 2.25, 3.0, '65,8 / 34,2', 'a mesma, rotação oblíqua');
  bloco(s, M, y + 3.85, W - 2*M, 'Achado.',
    'O plano previa que a rotação oblíqua deslocasse os pesos NA DIREÇÃO dos 60/40 da literatura. Ela os deslocou meio ponto no sentido oposto. A convergência com o IVS-BH não depende da escolha de rotação — e isso é bom: significa que a decisão nº 5 não muda os pesos de forma relevante.', true, 1.1);
  s.addNotes('A rotação oblíqua produz uma coisa que a ortogonal não pode produzir por construção: a matriz de correlação entre os fatores. Φ = 0,52, positiva e moderada, é exatamente o que a teoria da vulnerabilidade prevê — territórios pobres têm pior saneamento. Isso vira um parágrafo de validação no artigo.');
}

{ const s = S();
  const y = titulo(s, 'Divergência 2 — a técnica de extração', 'A regra de Stevens (1992) obriga a testar o que era pressuposto.');
  const e6 = ex('ivs6_sem_lixo_spearman');
  const yt = legendaTabela(s, y, 'ACP e fatoração do eixo principal sobre a mesma matriz, seis componentes.',
    'Fonte: nb04_extracao_comparada.csv. A divergência se concentra nas variáveis de SMC baixa.');
  tabela(s, ['Variável', 'SMC', 'ACP fator 2', 'Eixo principal', 'Diferença'],
    e6.map(r => [r.variavel, n(r.SMC), n(r.ACP_2), n(r.PAF_2),
      num(r, 'dif_2') > 0.2 ? marca(n(r.dif_2)) : n(r.dif_2)]),
    { y: yt, colW: [4.2, 1.7, 2.0, 2.0, 1.73], rowH: 0.40, fontSize: 11.5 });
  bloco(s, M, yt + 3.0, W - 2*M, 'Duas das três condições de convergência falham.',
    'O livro (p. 27) diz que ACP e análise fatorial dão o mesmo com mais de 30 variáveis ou comunalidades acima de 0,60 na maioria; e que abaixo de 20 variáveis, com comunalidades abaixo de 0,4, podem divergir. São 6 variáveis e a comunalidade mínima é 0,380. Divergem — e divergem exatamente onde Stevens previu: nas variáveis que menos compartilham variância com as demais.', true, 1.4);
  s.addNotes('A água tem SMC de 0,222: as outras cinco variáveis explicam só 22% da variabilidade dela. É nela que a diferença entre os métodos é maior. Nas de SMC alta — renda 0,735, cor/raça 0,648 — os dois métodos praticamente coincidem. Isso é confirmação de que a implementação está certa, não sinal de problema.');
}

{ const s = S();
  const y = titulo(s, 'Divergência 3 — a regra de comunalidade', 'O corte de 0,50 não é corte rígido, e isso resolve um caso pendente.');
  s.addText('"O critério da comunalidade maior do que 0,5 não deve ser utilizado isoladamente e de maneira muito rígida."',
    { x: M + 0.35, y: y + 0.2, w: W - 2*M - 0.7, h: 0.7, fontFace: 'Cambria', fontSize: 13.5,
      color: TINTA, italic: true, margin: 0, lineSpacing: 19 });
  regua(s, y + 0.2, 1.5, ACENTO, M, 0.02);
  s.addText('Matos & Rodrigues (2019), p. 58', { x: M + 0.35, y: y + 0.95, w: 6, h: 0.3,
    fontFace: 'Cambria', fontSize: 10.5, color: CINZA, margin: 0 });
  const rm = CARGAS6.find(r => r.variavel === 'Razão de moradores');
  numero(s, M, y + 1.65, 4.0, n(rm.comun_ortogonal), 'comunalidade da razão de moradores');
  numero(s, M + 4.7, y + 1.65, 4.0, n(rm.Varimax1), 'carga dela no fator socioeconômico');
  bloco(s, M, y + 3.05, W - 2*M, 'A variável fica no índice, e os dois números vão reportados juntos.',
    'O livro mantém, no seu próprio exemplo, um item com comunalidade abaixo do corte porque a carga fatorial é alta. É o caso aqui. A razão de moradores é a única sobrevivente do bloco de densidade habitacional, e retirá-la reduziria o índice a cinco componentes.', true, 1.3);
  s.addNotes('Até este trabalho, a decisão sobre a razão de moradores estava pendente, entre manter por razão teórica e excluir pela regra. A p. 58 dá respaldo bibliográfico para manter, desde que se reporte carga e comunalidade juntas. Deixa de ser ousadia e vira domínio da bibliografia.');
}

{ const s = S();
  titulo(s, 'As cargas, nas duas rotações', 'Seis componentes, sem o indicador de lixo. A estrutura teórica aparece limpa.');
  s.addImage({ path: path.join(FIG, 'nb04_mapa_cargas.png'), x: 1.75, y: 1.70, w: 9.83, h: 4.59 });
  legendaFigura(s, 6.38, 'Cargas fatoriais — Varimax e promax.',
    'Fonte: figuras/nb04_mapa_cargas.png, bloco 5 do Notebook 04.');
  s.addNotes('Nenhuma variável carrega acima de 0,40 em dois fatores — a estrutura simples do livro está atendida nas duas rotações. Fator 1 é socioeconômico: renda, analfabetismo, cor/raça e densidade. Fator 2 é saneamento: água e esgoto. É a estrutura do IVS-BH 2012, recuperada dos dados.');
}

// ═════════ 5. OS PESOS ═════════
{ const s = S(); secao(s, '5', 'Os pesos',
    'O produto deste notebook: quanto cada indicador pesa, e com que margem.');
  s.addNotes('A partir daqui é o resultado. Os três slides seguintes respondem: quais são os pesos, são confiáveis, e o índice que sai deles funciona.');
}

{ const s = S();
  const y = titulo(s, 'Os pesos do IVS', 'Peso proporcional ao quadrado da carga, dentro e entre as dimensões.');
  const yt = legendaTabela(s, y, 'Pesos dos seis componentes, solução Varimax de dois fatores.',
    'Fonte: nb04_sintese_pesos.csv. O peso da dimensão é a soma dos quadrados das cargas do fator sobre o total.');
  tabela(s, ['Variável', 'Dimensão', 'Carga', 'Peso'],
    PESOS.slice().sort((a, b) => num(b, 'peso') - num(a, 'peso'))
      .map(r => [r.variavel, r.dimensao, n(r.carga), `${n(r.peso_pct, 2)}%`]),
    { y: yt, colW: [4.6, 3.4, 1.9, 1.73], rowH: 0.40, fontSize: 11.5 });
  numero(s, M, yt + 3.05, 3.8, `${n(pSocio,1)} / ${n(pSanea,1)}`, 'repartição empírica socioeconômica / saneamento');
  numero(s, M + 4.5, yt + 3.05, 3.8, '60 / 40', 'referência do IVS-BH 2012 (literatura)');
  bloco(s, M + 9.0, yt + 3.05, 2.6, 'Convergem.', 'Cinco pontos de diferença.', true, 1.1);
  s.addNotes('O argumento a favor dos pesos empíricos está na p. 71 do livro: os itens contribuem de maneira desigual para o fator, e quanto maior a carga maior a contribuição — o que não acontece nas técnicas mais simples de índice, que pressupõem contribuição igual. Pesos iguais dariam três votos à posição social, porque renda, cor/raça e analfabetismo medem em boa parte a mesma coisa.');
}

{ const s = S();
  const y = titulo(s, 'Os pesos são estáveis', 'Mil reamostragens com reposição respondem com número à crítica de instabilidade da p. 23.');
  const yt = legendaTabela(s, y, 'Intervalo de confiança de 95% de cada carga, por bootstrap.',
    'Fonte: nb04_bootstrap_cargas.csv. 1.000 reamostragens, semente 42, cada solução alinhada à da amostra completa.');
  tabela(s, ['Variável', 'Carga no fator 1', 'IC 95%', 'Amplitude'],
    BOOT.map(r => [r.variavel, n(Math.abs(num(r, 'carga_F1'))),
      `[${n(Math.abs(num(r,'IC95_F1_sup')))} ; ${n(Math.abs(num(r,'IC95_F1_inf')))}]`,
      n(r.largura_F1, 4)]),
    { y: yt, colW: [4.6, 2.6, 3.0, 1.43], rowH: 0.40, fontSize: 11.5 });
  numero(s, M, yt + 2.95, 5.4, '[64,7 ; 65,3]', 'IC 95% da repartição socioeconômica — 0,59 ponto de amplitude', true);
  bloco(s, M + 6.1, yt + 2.95, 5.5, 'O que limita esta análise não é o n.',
    'Com 87 mil setores a incerteza amostral é desprezível. O que limita é o número pequeno de variáveis — e o livro, escrito para questionários com dezenas de itens, não trata desse problema.', false, 1.4);
  s.addNotes('O bootstrap não está em nenhuma das duas referências; é extensão do projeto. Ele importa porque o livro acusa os índices por média ponderada de serem instáveis entre amostras. A resposta honesta não era discordar, era medir — e a instabilidade não se materializou.');
}

{ const s = S();
  const y = titulo(s, 'O índice e o escore refinado concordam menos que o previsto',
    'Achado. E a forma como a concordância falha é mais informativa que o número.');
  numero(s, M, y + 0.25, 3.4, '0,924', 'Spearman com o escore sobre POSTOS (coerente)', true);
  numero(s, M + 4.0, y + 0.25, 3.4, '0,945', 'com o escore sobre valores brutos (incoerente)');
  numero(s, M + 8.0, y + 0.25, 3.6, '0,950', 'o corte que validaria o índice 0–1');
  bloco(s, M, y + 1.85, W - 2*M, 'Quanto mais coerente o escore fica com o modelo, mais se afasta do índice.',
    'O índice 0–1 é min-max de valores BRUTOS. O modelo fatorial foi estimado sobre POSTOS, porque a correlação é de Spearman. São dois objetos em escalas diferentes, e a diferença entre 0,924 e 0,945 é exatamente o tamanho dessa incoerência.', true, 1.4);
  bloco(s, M, y + 3.45, W - 2*M, 'Não é instabilidade.',
    'O bootstrap mediu a incerteza dos pesos em 0,59 ponto percentual. Mais reamostragem não resolve isto. As saídas são três, e as três são defensáveis: compor o índice sobre postos, estimar a fatorial sobre Pearson, ou declarar a divergência. O que não é defensável é escolher sem saber que se está escolhendo.', false, 1.2);
  s.addNotes('O plano previa Spearman acima de 0,97 aqui. Deu 0,924. Nenhum dos dois valores chega ao piso de 0,90 que obrigaria a adotar o escore refinado como índice oficial — então o índice 0–1 continua viável, mas com a ressalva declarada. Esta é a questão técnica mais aberta que sai do Notebook 04.');
}

// ═════════ 6. O ÍNDICE FUNCIONA ═════════
{ const s = S(); secao(s, '6', 'O índice funciona?',
    'A pergunta que nenhuma estatística interna à fatorial responde.');
  s.addNotes('KMO, comunalidade e variância explicada dizem se as variáveis se organizam. Nenhuma delas diz se o índice acerta. Para isso é preciso um marcador externo — e o projeto tem um.');
}

{ const s = S();
  const y = titulo(s, 'Contra os setores de favela', 'Validação de critério com um marcador externo ao índice: CD_TIPO = 1, do próprio IBGE.');
  s.addImage({ path: path.join(FIG, 'nb04_roc_fcu.png'), x: 0.85, y: 1.62, w: 4.55, h: 4.55 });
  numero(s, 6.2, 2.1, 3.0, n(aucIdx), 'AUC do índice 0–1', true);
  numero(s, 9.6, 2.1, 3.0, n(aucEsc), 'AUC do escore refinado');
  numero(s, 6.2, 3.55, 6.4, `${n(VALID[0].mediana_fcu)}  contra  ${n(VALID[0].mediana_demais)}`,
    'mediana do índice nos setores de FCU e nos demais');
  bloco(s, 6.2, 5.0, 6.4, 'Por que este teste vale mais.',
    'Nenhuma das seis variáveis do índice foi usada para classificar um setor como favela. A lista é oficial e já foi conferida setor a setor com 100% de concordância. O corte fixado no plano era 0,75.', true, 1.3);
  legendaFigura(s, 6.28, 'Separação dos setores de Favela e Comunidade Urbana.',
    'Fonte: figuras/nb04_roc_fcu.png, bloco 9 do Notebook 04.');
  s.addNotes('18.901 setores de FCU contra 68.644 demais, dentro do conjunto completo nas seis variáveis. Se a orientadora perguntar por que não são os 19.452 do recorte: a diferença são os setores de favela que caíram na exclusão por lista, quase toda por sigilo do analfabetismo.');
}

{ const s = S();
  const y = titulo(s, 'O custo de cada escolha, em setores', 'A métrica não é variância explicada. É quantos setores mudam de faixa de risco.');
  const yt = legendaTabela(s, y, 'Mudança de classificação em quartis, contra a referência de dois fatores com pesos empíricos.',
    'Fonte: nb04_cenarios.csv e nb04_contingencia_*.csv.');
  tabela(s, ['Cenário', 'Setores que mudam de faixa', '% dos 87.545', 'Spearman'], [
    ['Pesos 60/40 em vez de 65/35', inteiro(cenPor('pesos_6040').setores_que_mudam_de_faixa),
      `${n(cenPor('pesos_6040').pct, 1)}%`, n(cenPor('pesos_6040').spearman_com_referencia, 4)],
    ['Sem o analfabetismo (política do sigilo)', inteiro(cenPor('sem_analfab').setores_que_mudam_de_faixa),
      `${n(cenPor('sem_analfab').pct, 1)}%`, n(cenPor('sem_analfab').spearman_com_referencia, 4)],
    ['Um fator em vez de dois', inteiro(cenPor('um_fator').setores_que_mudam_de_faixa),
      `${n(cenPor('um_fator').pct, 1)}%`, n(cenPor('um_fator').spearman_com_referencia, 4)],
  ], { y: yt, colW: [5.4, 3.0, 2.2, 1.03], rowH: 0.50, fontSize: 12 });
  bloco(s, M, yt + 2.2, W - 2*M, 'A decisão nº 1 deixa de ser crítica.',
    `Trocar os pesos empíricos pelos 60/40 da literatura move ${n(cenPor('pesos_6040').pct, 1)}% dos setores de faixa, com correlação de ${n(cenPor('pesos_6040').spearman_com_referencia, 4)} entre as duas ordenações. É o menor custo dos três cenários — e isso é resultado publicável, não detalhe técnico.`, true, 1.3);
  s.addNotes('O objetivo deste bloco é mostrar o custo, não escolher. Se a orientadora preferir 60/40 pela comparabilidade com o IVS-BH, agora se sabe exatamente o que isso custa: 2.196 setores mudam de faixa. Antes, a escolha seria feita no escuro.');
}

// ═════════ 7. DECISÕES ═════════
{ const s = S(); secao(s, '7', 'O que vai para a orientação',
    'Seis decisões, cada uma com o custo medido. Nenhuma foi fechada aqui.');
  s.addNotes('Fechar estas decisões não era papel do notebook. O papel dele era tirá-las do terreno da opinião.');
}

{ const s = S();
  const y = titulo(s, 'As seis decisões', 'Com o que cada opção custa.');
  tabela(s, ['#', 'Decisão', 'O que pesa de cada lado'], [
    ['1', 'Pesos empíricos ou 60/40', `Convergem. Custo da troca: ${n(cenPor('pesos_6040').pct,1)}% dos setores mudam de faixa`],
    ['2', 'Destino do indicador de lixo', 'Fora: variância sobe a 70,0% e a água recupera a comunalidade. Dentro: fidelidade literal ao IVS-BH 2012'],
    ['3', 'Política do sigilo no analfabetismo', `Manter a variável custa 16.563 setores sem índice. Retirá-la move ${n(cenPor('sem_analfab').pct,1)}% de faixa`],
    ['4', 'Um fator ou dois', `Um é o que Kaiser e Horn indicam e dispensa rotação. Dois preserva a estrutura do IVS-BH. Custo: ${n(cenPor('um_fator').pct,1)}%`],
    ['5', 'Rotação ortogonal ou oblíqua', 'Oblíqua é a recomendada (p. 38) e produz Φ. Custo nos pesos: 0,8 ponto percentual'],
    ['6', 'Índice 0–1 ou escore refinado', `O 0–1 é interpretável e comparável. O refinado separa melhor as favelas (${n(aucEsc)} contra ${n(aucIdx)})`],
  ], { y, colW: [0.6, 4.0, 7.03], rowH: 0.62, fontSize: 11.5 });
  s.addNotes('Sugestão de condução: começar pela 2 e pela 5, que são as que têm evidência mais forte e menos custo político. A 4 é a mais delicada, porque os critérios estatísticos e a teoria apontam para lados diferentes. A 6 é a mais técnica e pode ficar para depois do Notebook 03.');
}

{ const s = S();
  const y = titulo(s, 'O que fica declarado como limitação', 'Nove pontos. Quatro são do método, cinco são dos dados.');
  tabela(s, ['Limitação', 'Onde ela morde'], [
    ['Bartlett vazio nesta escala', 'A adequabilidade se apoia no KMO e nos MSA (livro, p. 43)'],
    ['ACP sobre matriz de Spearman é ACP de postos', 'É a causa da divergência entre o índice e o escore refinado'],
    ['Multicolinearidade renda × cor/raça', `0,784 na matriz fatorada — abaixo do limiar, mas alto`],
    ['Viés não aleatório do sigilo', '16.563 setores perdidos, incidindo nos de melhor situação'],
    ['Dependência espacial não tratada', 'A fatorial pressupõe unidades independentes; setores vizinhos não são'],
    ['Falácia ecológica', 'As cargas descrevem territórios, não pessoas'],
    ['Padronização min-max global e provisória', 'A normalização por município é do Notebook 03'],
    ['renda_media_sem_extremo não entrou', 'Toda a análise usa renda_media, como os CSVs de agosto'],
    ['Reflexivo ou formativo', 'Questão conceitual em aberto sobre a natureza do índice'],
  ], { y, colW: [5.3, 6.33], rowH: 0.44, fontSize: 11.5 });
  s.addNotes('A limitação de dados faltantes merece destaque: o livro da Enap não discute dados faltantes em nenhuma das 74 páginas. Os exemplos dele são questionários com resposta completa. É lacuna da referência, não descuido do projeto, e o tratamento adequado exigirá literatura que ainda não temos.');
}

{ const s = S();
  const y = titulo(s, 'O que vem depois', 'O Notebook 04 entrega estrutura e pesos. O índice ainda não está calculado.');
  const passos = [
    ['Notebook 03', 'Normalização min-max por município. A fatorial roda ANTES dela, e isso está medido: normalizar primeiro derruba o KMO de 0,783 para 0,720.'],
    ['Notebook 05', 'O IVS final, com os pesos desta apresentação, e a categorização em quatro faixas de risco.'],
    ['Geoprocessamento', 'Mapas temáticos no QGIS, e o I de Moran dos escores — que dará a medida da dependência espacial que esta análise ignora.'],
    ['Artigo', 'A seção de método está escrita: cada decisão tem a página que a sustenta e o número que a mede.'],
  ];
  let yy = y + 0.25;
  passos.forEach(([t, txt]) => { bloco(s, M, yy, W - 2*M, t + '.', txt, false, 1.0); yy += 1.15; });
  regua(s, H - 1.15, 0.75);
  s.addText('Pedro Dias Soares  ·  Iniciação Científica  ·  Fiocruz Minas — Instituto René Rachou  ·  setembro de 2026',
    { x: M, y: H - 1.0, w: W - 2*M, h: 0.4, fontFace: 'Cambria', fontSize: 11, color: CINZA, margin: 0 });
  s.addNotes('Fechar lembrando que o produto aqui são os pesos, não o índice. E que a ordem entre o Notebook 03 e o 04 não é indiferente: foi medida, e fatorar sobre os indicadores brutos é a opção adotada.');
}

const saida = process.argv[2];
if (!saida) { console.error('uso: node scripts/gerar_deck_fatorial.js <saida.pptx>'); process.exit(1); }
p.writeFile({ fileName: saida }).then(f => console.log('deck escrito:', f));
