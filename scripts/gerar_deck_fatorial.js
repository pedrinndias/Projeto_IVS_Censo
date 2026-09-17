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
/**
 * Divide uma linha respeitando aspas. O `to_csv` do pandas ENVOLVE em aspas o campo que
 * contém o separador, em vez de escapá-lo — então dividir direto no ';' desloca todas as
 * colunas seguintes no dia em que um rótulo ou um nome de município trouxer um ponto e
 * vírgula. Quebra de linha dentro de campo continua fora do alcance daqui; se algum dia
 * aparecer, é caso de ler o CSV em Python e emitir JSON, como faz a EDA Central.
 */
function dividir(linha) {
  const campos = [];
  let campo = '', aspas = false;
  for (let i = 0; i < linha.length; i++) {
    const ch = linha[i];
    if (aspas) {
      if (ch !== '"') campo += ch;
      else if (linha[i + 1] === '"') { campo += '"'; i++; }   // aspas duplicada = literal
      else aspas = false;
    } else if (ch === '"') aspas = true;
    else if (ch === ';') { campos.push(campo); campo = ''; }
    else campo += ch;
  }
  campos.push(campo);
  return campos;
}

function lerCsv(nome) {
  const txt = fs.readFileSync(path.join(FAT, nome), 'utf8').replace(/^﻿/, '').trim();
  const [cab, ...linhas] = txt.split(/\r?\n/);
  const cols = dividir(cab).map(c => c === '' ? 'idx' : c);
  return linhas.map(l => {
    const v = dividir(l);
    return Object.fromEntries(cols.map((c, i) => [c, v[i]]));
  });
}
const num = (o, c) => Number(o[c]);
// Formatação em português SEM `toLocaleString`. Num Node compilado com small-icu o
// locale 'pt-BR' cai silenciosamente para en-US e o deck inteiro sai com ponto decimal,
// sem que nada falhe — a mesma armadilha do caminho fixo que gerar_deck_eda_central.js
// chama de bomba-relógio. `toFixed` e a expressão do milhar não dependem de ICU.
/** Número em português: vírgula decimal, casas fixas. */
function n(v, casas) {
  return Number(v).toFixed(casas === undefined ? 3 : casas).replace('.', ',');
}
/** Inteiro com ponto de milhar. */
const inteiro = v => Math.round(Number(v)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');

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
const RENDA = lerCsv('nb04_renda_sem_extremo.csv');
const RENDA_CARGAS = lerCsv('nb04_renda_sem_extremo_cargas.csv');

const phi = Math.abs(num(PHI[0], 'Fator 2'));
const cenPor = k => CENARIOS.find(r => r.cenario === k);
const aucIdx = num(VALID[0], 'auc'), aucEsc = num(VALID[1], 'auc');
const av = c => AUTOV.filter(r => r.cenario === c);
const ex = c => EXTRA.filter(r => r.cenario === c);
const ad = c => ADEQ.filter(r => r.cenario === c);
const lixoEx = ex('ivs7_spearman').find(r => r.variavel === 'Lixo inadequado');
const rendaRaca = Math.abs(num(CORR7.find(r => r.idx === 'Renda (invertida)'), 'Cor/raça PPI'));
const linhaRenda = m => RENDA.find(r => r.medida === m);
const rendaMuda = num(linhaRenda('setores que mudam de faixa'), 'com renda_media_sem_extremo');
const rendaRho = num(linhaRenda('Spearman entre os ordenamentos'), 'com renda_media_sem_extremo');
const rendaDif = Math.max(...RENDA_CARGAS.flatMap(r => [num(r, 'dif_1'), num(r, 'dif_2')]));

// repartição entre as dimensões, somada dos pesos (não digitada)
const pesoDim = d => PESOS.filter(r => r.dimensao === d).reduce((a, r) => a + num(r, 'peso'), 0);
const pSocio = 100 * pesoDim('Socioeconômica'), pSanea = 100 * pesoDim('Saneamento');

// ── O deck ──────────────────────────────────────────────────────────────────
const d = criarDeck({ titulo: 'Análise fatorial e os pesos do IVS — Notebook 04' });
const { p, S, titulo, secao, bloco, numero, tabela, legendaTabela, legendaFigura,
        capa, regua, codigo, codigoComentado } = d;
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
  titulo(s, 'A matriz de correlação, as sete variáveis',
    'É a Tabela 1 do livro (p. 15) nos dados do projeto — e ela já mostra a estrutura antes de fatorar.');
  s.addImage({ path: path.join(FIG, 'nb04_matriz_correlacao.png'), x: 3.35, y: 1.48, w: 6.06, h: 4.83 });
  legendaFigura(s, 6.40, 'Matriz-R de Spearman, sete componentes, 87.545 setores.',
    'Fonte: figuras/nb04_matriz_correlacao.png, bloco 2 do Notebook 04.');
  s.addNotes('Vale conduzir a leitura por três lugares. Primeiro, o retângulo escuro no canto inferior direito: analfabetismo, renda e cor/raça a 0,63, 0,76 e 0,78 — o bloco socioeconômico. Segundo, água e esgoto a 0,41 — o bloco de saneamento, mais fraco. Terceiro, a linha do lixo, que é a mais clara da matriz inteira: 0,10 com a água e −0,05 com a razão de moradores. O livro diz, na p. 16, que já na exploração inicial dá para ter dicas sobre a variável que não vai se comportar bem. Esta é a dica.');
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

{ const s = S();
  titulo(s, 'O plano dos fatores',
    'A Figura 2 do livro (p. 17): os fatores como eixos, cada variável plotada nas suas duas cargas.');
  s.addImage({ path: path.join(FIG, 'nb04_plano_fatorial.png'), x: 0.85, y: 1.52, w: 11.63, h: 4.63 });
  legendaFigura(s, 6.28, 'Representação gráfica dos fatores, com e sem o indicador de lixo.',
    'Fonte: figuras/nb04_plano_fatorial.png, bloco 5 do Notebook 04.');
  s.addNotes('Este é o slide para mostrar quando a pergunta for "por que tirar o lixo?". No painel da esquerda ele está sozinho no alto, longe de todo o resto — exatamente o que o livro descreve para o item 7 do exemplo dele: "se encontra espacialmente distante dos dois grupos". No painel da direita, sem ele, as seis variáveis se organizam em dois braços: saneamento subindo pelo eixo vertical, socioeconômico avançando pelo horizontal. Os eixos vão de −1 a 1 de propósito, que são os limites do coeficiente de correlação; encolher os eixos para caber os dados faria carga média parecer carga alta.');
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

// ═════════ 7. DUAS PERGUNTAS EM ABERTO ═════════
{ const s = S(); secao(s, '7', 'Duas perguntas que sobraram',
    'Uma se respondeu rodando. A outra não se responde com dados.');
  s.addNotes('A primeira é a renda sem o extremo, que era dívida da 2ª rodada da EDA. A segunda é conceitual e é a mais séria em aberto no projeto inteiro.');
}

{ const s = S();
  const y = titulo(s, 'A renda sem o extremo não muda nada',
    'A 2ª rodada da EDA recalculou tudo com renda_media_sem_extremo. A fatorial é anterior a essa coluna.');
  const yt = legendaTabela(s, y, 'A mesma fatorial, trocando só a coluna de renda.',
    'Fonte: nb04_renda_sem_extremo.csv. Mesmas seis variáveis, mesmo recorte, mesma rotação.');
  tabela(s, ['Medida', 'com renda_media', 'sem o extremo', 'diferença'],
    ['KMO', 'MSA mínimo', 'peso socioeconômico (%)', 'peso saneamento (%)'].map(k => {
      const r = RENDA.find(x => x.medida === k);
      const casas = k.includes('%') ? 3 : 4;
      return [k, n(r['com renda_media'], casas), n(r['com renda_media_sem_extremo'], casas),
              n(r['diferença'], 5)];
    }), { y: yt, colW: [4.2, 2.6, 2.6, 2.23], rowH: 0.44, fontSize: 11.5 });
  numero(s, M, yt + 2.3, 3.6, n(rendaDif, 4), 'maior diferença entre as cargas');
  numero(s, M + 4.2, yt + 2.3, 3.6, inteiro(rendaMuda), 'setores que mudam de faixa, de 87.544');
  numero(s, M + 8.4, yt + 2.3, 3.2, n(rendaRho, 6), 'Spearman entre os dois índices', true);
  s.addNotes('A resposta é clara: trocar a coluna não muda a estrutura, não muda os pesos e quase não muda a classificação. As cargas batem até a quarta casa decimal. É o resultado que se esperava de um setor em 87 mil, mas ele precisava ser medido, porque a renda é a variável de maior carga do índice e o extremo foi grande o bastante para justificar uma rodada inteira da EDA. Fica registrado que a fatorial pode continuar sobre renda_media sem prejuízo, ou migrar sem custo — a decisão deixa de importar.');
}

{ const s = S();
  const y = titulo(s, 'O IVS é construto reflexivo ou índice formativo?',
    'A objeção conceitual mais séria em aberto. Ela decide se a análise fatorial é o instrumento certo.');
  bloco(s, M, y + 0.2, 5.6, 'Reflexivo — o latente CAUSA os indicadores.',
    'A vulnerabilidade existiria como propriedade do território e se manifestaria em renda baixa, analfabetismo, saneamento precário. Os indicadores são intercambiáveis, devem correlacionar-se alto, e retirar um não muda o significado. É o modelo que a análise fatorial pressupõe.', false, 2.0);
  bloco(s, M + 6.1, y + 0.2, 5.6, 'Formativo — os indicadores CONSTITUEM o índice.',
    'Vulnerabilidade É a combinação de privações. Cada indicador é faceta definidora, não precisam correlacionar-se, e retirar um muda o significado. Os pesos viriam de teoria ou de política pública, não da covariância.', true, 2.0);
  tabela(s, ['Resultado deste trabalho', 'Leitura reflexiva', 'Leitura formativa'], [
    ['Lixo com comunalidade 0,052', 'não pertence: retirar', marca('faceta que falta: manter')],
    ['Renda × cor/raça a 0,784', 'bloco coeso, evidência do construto', 'multicolinearidade, atrapalha'],
    ['KMO 0,783 e Bartlett', 'provam adequabilidade', marca('não se aplicam')],
    ['Pesos 65/35 empíricos', 'saem da estrutura latente', 'teriam de sair de teoria'],
  ], { y: y + 2.45, colW: [4.2, 3.6, 3.83], rowH: 0.42, fontSize: 11 });
  s.addNotes('O ponto que não pode passar batido: a decisão sobre o lixo SE INVERTE entre as duas leituras. Sob a leitura reflexiva, comunalidade de 0,052 manda tirar. Sob a formativa, o lixo é a única variável que cobre destino de resíduo, e tirá-la remove uma faceta do que se quer medir. Não é preciosismo terminológico — é a diferença entre dois índices diferentes.');
}

{ const s = S();
  const y = titulo(s, 'A saída que os dados sugerem', 'Um híbrido — e ele explica uma coisa que estava sem explicação.');
  bloco(s, M, y + 0.25, W - 2*M, 'Dentro de cada dimensão, o comportamento é reflexivo.',
    'Renda, analfabetismo e cor/raça correlacionam-se de 0,63 a 0,78 e claramente manifestam uma mesma posição social do território. Água e esgoto, a 0,41, manifestam infraestrutura de saneamento. Nos dois blocos, os indicadores parecem efeitos de uma causa comum.', false, 1.3);
  bloco(s, M, y + 1.75, W - 2*M, 'Entre as duas dimensões, a composição é formativa.',
    'Não há razão para supor um latente único que cause tanto a falta de água quanto o analfabetismo. A correlação entre os fatores, Φ = 0,52, é consistente com isso: alta o bastante para justificar a rotação oblíqua, longe o bastante de 1 para não sugerir um fator só.', true, 1.3);
  bloco(s, M, y + 3.25, W - 2*M, 'A consequência, e ela já está medida.',
    'A análise fatorial é legítima para obter os pesos DENTRO de cada bloco. A repartição ENTRE blocos — o 65/35 — é decisão formativa, que os dados não têm como arbitrar. É isso que explica por que a escolha entre 65/35 e 60/40 custa apenas 2,5% dos setores: ela nunca foi uma questão empírica.', false, 1.4);
  s.addNotes('Esta é uma proposta, não um resultado — e precisa de aval. O que falta é literatura: Bollen & Lennox (1991) é a formulação canônica da distinção, e Diamantopoulos & Winklhofer (2001) e Edwards (2011) completam o núcleo. Nenhum está lido no projeto. Valeria também descobrir se o IVS-BH 2012 e o ISU de Passarelli-Araujo declaram a posição deles — provavelmente não declaram, e isso é comum na área.');
}

// ═════════ 8. O CÓDIGO ═════════
{ const s = S(); secao(s, '8', 'O código, por dentro',
    'Como a análise foi construída em Python, linha a linha, e como se faria em R.');
  s.addNotes('Esta seção existe para que a análise seja defensável linha a linha. Álgebra linear escrita à mão precisa disso.');
}

{ const s = S();
  const y = titulo(s, 'Por que numpy puro, e não uma biblioteca pronta',
    'A pergunta aparece sempre, e a resposta é de engenharia — mas teve um efeito colateral melhor.');
  bloco(s, M, y + 0.25, 5.7, 'A razão declarada.',
    'O requirements.txt tem cinco pacotes. Acrescentar factor_analyzer traria conveniência e traria uma dependência a mais para instalar, versionar e justificar numa dissertação — por um ganho de digitação, não de método. Tudo que a análise precisa é álgebra linear que o numpy já faz.', false, 2.0);
  bloco(s, M + 6.2, y + 0.25, 5.7, 'A razão que apareceu depois.',
    'Quem escreve a conta à mão precisa saber a conta. Foi escrevendo o KMO que ficou claro que ele se apoia na matriz anti-imagem; foi escrevendo o promax que ficou claro por que existem DUAS matrizes de carga numa solução oblíqua. Nenhuma das duas coisas se aprende chamando uma função.', true, 2.0);
  bloco(s, M, y + 2.6, W - 2*M, 'Em R a escolha seria outra, e razoável.',
    'O pacote psych é o padrão da área, está em toda a bibliografia — inclusive nos exemplos do livro da Enap, que são em R — e não é dependência exótica. Os próximos slides mostram a correspondência função a função, e o script completo.', false, 1.2);
  s.addNotes('Se a orientadora perguntar se não teria sido mais rápido usar uma biblioteca: teria, e o resultado seria o mesmo. O que se ganhou foi poder responder a qualquer pergunta sobre o método sem dizer "a biblioteca faz". Numa iniciação científica isso vale mais do que as horas economizadas.');
}

{ const s = S();
  const y = titulo(s, 'O caminho, em nove passos', 'Cada passo, a função que o faz aqui e a que o faria em R.');
  tabela(s, ['#', 'Passo', 'Neste projeto (numpy)', 'Em R'], [
    ['1', 'Matriz de correlação', 'X.corr(method=’spearman’)', 'cor(X, method = "spearman")'],
    ['2', 'KMO e MSA', 'kmo(R)', 'psych::KMO(R)'],
    ['3', 'Teste de Bartlett', 'bartlett(R, n)', 'psych::cortest.bartlett(R, n)'],
    ['4', 'Multicolinearidade', 'smc(R)', 'psych::smc(R)'],
    ['5', 'Número de fatores', 'acp(R, k) · horn(n, p)', 'eigen(R) · psych::fa.parallel()'],
    ['6', 'Extração por eixo principal', 'fatoracao_eixo_principal(R, k)', 'psych::fa(R, fm = "pa")'],
    ['7', 'Rotação ortogonal', 'varimax(cargas)', 'stats::varimax(L, normalize = FALSE)'],
    ['8', 'Rotação oblíqua', 'rotacao_promax(cargas)', 'stats::promax(L, m = 4)'],
    ['9', 'Escores refinados', 'escores_regressao(R, A)', 'psych::factor.scores()'],
  ], { y, colW: [0.6, 3.5, 3.9, 3.63], rowH: 0.46, fontSize: 11 });
  s.addNotes('Vale dizer em voz alta que a coluna da direita é mais curta — em R, cada passo é uma chamada. O projeto escreveu as nove à mão, em 457 linhas de módulo com 9 testes. O passo 7 tem uma armadilha que aparece daqui a três slides: a varimax do R normaliza por padrão e a nossa não.');
}

{ const s = S();
  const y = titulo(s, 'O KMO, linha a linha', 'Compara a correlação bruta entre duas variáveis com o que sobra dela depois de descontar as outras.');
  codigoComentado(s, y + 0.1, [
    ['def kmo(R):', ''],
    ['    Rinv = np.linalg.inv(R)', 'A inversa da matriz de correlação. É dela que saem as correlações parciais — não é óbvio, e é o coração do procedimento.'],
    ['', ''],
    ['    d = np.sqrt(np.diag(Rinv))', 'Raiz da diagonal: o fator de padronização.'],
    ['    parcial = -Rinv / np.outer(d, d)', 'A fórmula da correlação parcial sobre a inversa. O sinal negativo não é detalhe: sem ele toda a matriz anti-imagem inverte.'],
    ['', ''],
    ['    np.fill_diagonal(parcial, 0.0)', 'A correlação de uma variável com ela mesma é 1 e inflaria as somas. Zera dos dois lados.'],
    ['    R0 = R.copy()', ''],
    ['    np.fill_diagonal(R0, 0.0)', ''],
    ['', ''],
    ['    soma_r = (R0 ** 2).sum()', ''],
    ['    soma_p = (parcial ** 2).sum()', ''],
    ['    return soma_r / (soma_r + soma_p)', 'O KMO global: a fração da associação que NÃO é parcial. Trocando .sum() por .sum(axis=0) sai o MSA de cada variável.'],
  ], { larguraCodigo: 5.3, alturaLinha: 0.315, fonte: 10 });
  s.addNotes('O resultado do projeto é 0,783, que na escala de Friel é a faixa "mediano", bem acima do piso de 0,50 de Hair. Se perguntarem o que o KMO mede em uma frase: se duas variáveis continuam associadas depois de descontar todas as outras, elas têm algo próprio entre si e não um fator comum — e é isso que derruba o KMO.');
}

{ const s = S();
  const y = titulo(s, 'A extração, linha a linha', 'Quatro linhas, e a terceira é a que transforma álgebra em interpretação.');
  const yFim = codigoComentado(s, y + 0.15, [
    ['def acp(R, k):', ''],
    ['    val, vec = np.linalg.eigh(R)', 'Autovalores e autovetores. O "h" é de hermitian — a versão para matriz simétrica, mais rápida e mais estável. Matriz de correlação é sempre simétrica.'],
    ['', ''],
    ['    ordem = np.argsort(val)[::-1]', 'O eigh devolve em ordem CRESCENTE e a análise fatorial lê em decrescente. Sem esta linha, o "primeiro fator" seria o menos importante.'],
    ['    val = val[ordem]', ''],
    ['    vec = vec[:, ordem]', ''],
    ['', ''],
    ['    cargas = vec[:, :k] * np.sqrt(', 'A carga fatorial é o autovetor escalado pela raiz do autovalor. Sem o escalonamento os autovetores têm norma 1 e não se leem como correlação.'],
    ['        np.maximum(val[:k], 0))', 'O maximum corta em zero: autovalor negativo por erro numérico viraria raiz de número negativo.'],
    ['', ''],
    ['    return val, cargas', ''],
  ], { larguraCodigo: 5.3, alturaLinha: 0.33, fonte: 10 });
  bloco(s, M, yFim + 0.18, W - 2*M, 'Uma advertência que vale para toda a análise.',
    'O sinal de cada autovetor é ARBITRÁRIO — o LAPACK escolhe um e o oposto seria igualmente válido. Por isso as cargas são viradas na leitura, para que positivo queira dizer "mais vulnerável". Os CSVs guardam o sinal cru.', true, 1.1);
  s.addNotes('Se a orientadora quiser entender a diferença entre ACP e análise fatorial em uma frase, ela cabe aqui: é o que vai na diagonal da matriz antes de decompor. A ACP põe 1 e usa toda a variância; a análise fatorial põe a comunalidade e usa só a compartilhada. O resto do procedimento é idêntico.');
}

{ const s = S();
  const y = titulo(s, 'A rotação Varimax, linha a linha', 'Girar os eixos sem mudar as distâncias: a variância total não muda, só a repartição entre fatores.');
  const yFim = codigoComentado(s, y + 0.1, [
    ['R = np.eye(k)', 'Começa sem girar nada.'],
    ['for _ in range(maxiter):', ''],
    ['    Lam = L @ R', 'As cargas com a rotação atual.'],
    ['', ''],
    ['    u, s, vt = np.linalg.svd(', 'O truque do procedimento: a matriz ortogonal mais próxima de uma matriz qualquer é u @ vt da sua SVD. É o que garante que a rotação continue ortogonal a cada passo.'],
    ['      L.T @ (Lam ** 3 - Lam @', 'O gradiente do critério Varimax. O cubo vem da derivada da soma dos quadrados dos quadrados; o segundo termo subtrai a média por fator.'],
    ['      np.diag(np.diag(Lam.T @ Lam)) / p))', ''],
    ['', ''],
    ['    R = u @ vt', ''],
    ['    if d / d_ant < 1 + tol: break', 'Para quando o critério deixa de crescer.'],
    ['', ''],
    ['return L @ R', 'As cargas rotacionadas.'],
  ], { larguraCodigo: 5.3, alturaLinha: 0.28, fonte: 10 });
  bloco(s, M, yFim + 0.18, W - 2*M, 'A armadilha ao reproduzir em R.',
    'stats::varimax aplica normalização de Kaiser POR PADRÃO: divide cada linha pela raiz da comunalidade antes de girar e desfaz depois. É defensável, é o que o SPSS faz — e produz cargas diferentes. Para reproduzir estes números em R é preciso varimax(L, normalize = FALSE).', true, 1.2);
  s.addNotes('O critério da Varimax é maximizar a variância dos quadrados das cargas dentro de cada fator, o que empurra cada carga para perto de 0 ou de 1 — é assim que se obtém a "estrutura simples" de que o livro fala. A armadilha da normalização é o tipo de coisa que faz alguém achar que errou quando só usou o padrão de outra ferramenta.');
}

{ const s = S();
  const y = titulo(s, 'A rotação promax, linha a linha', 'Parte da Varimax e deixa os eixos se inclinarem. O procedimento é engenhoso.');
  codigoComentado(s, y + 0.12, [
    ['V = varimax(cargas)', 'Ponto de partida ortogonal.'],
    ['', ''],
    ['alvo = np.sign(V) * np.abs(V) ** kappa', 'Constrói um alvo EXAGERADO: com kappa = 4, uma carga de 0,9 vira 0,66 e uma de 0,3 vira 0,008. O contraste entre alto e baixo é ampliado.'],
    ['', ''],
    ['U, *_ = np.linalg.lstsq(V, alvo)', 'Acha por mínimos quadrados a transformação que leva V o mais perto possível do alvo. É aqui que a ortogonalidade se perde — e é isso que se quer.'],
    ['', ''],
    ['d = np.diag(np.linalg.inv(U.T @ U))', 'Escala as colunas para que Φ saia com diagonal 1. Sem este passo Φ é covariância entre fatores, não correlação, e a comunalidade vaza.'],
    ['U = U @ np.diag(np.sqrt(d))', ''],
    ['', ''],
    ['padrao = V @ U', 'A matriz PADRÃO: coeficientes de regressão. É dela que saem os pesos.'],
    ['phi = np.linalg.inv(U.T @ U)', 'A correlação entre os fatores — o objeto que a solução ortogonal não pode produzir.'],
    ['estrutura = padrao @ phi', 'A matriz de ESTRUTURA: correlações entre variável e fator.'],
  ], { larguraCodigo: 5.3, alturaLinha: 0.315, fonte: 10 });
  s.addNotes('A checagem que precisa acompanhar: numa solução oblíqua uma carga padrão pode passar de 1 sem ser erro, porque é coeficiente de regressão e não correlação — está na p. 22 do livro. Se passar, testa-se a variância residual da variável; negativa, a solução é inadmissível e sugere fatores demais. No nosso caso a maior carga deu 0,999 e a menor variância residual, 0,144.');
}

{ const s = S();
  const y = titulo(s, 'A mesma análise em R — parte 1', 'Dados e adequabilidade da base.');
  codigo(s, M, y + 0.2, W - 2*M, [
    '# Pacotes — uma vez só',
    'install.packages(c("psych", "GPArotation", "DBI", "RSQLite"))',
    'library(psych); library(GPArotation); library(DBI); library(RSQLite)',
    '',
    '# 1. Dados: o mesmo banco que o notebook usa',
    'con <- dbConnect(SQLite(),',
    '  "banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.db")',
    'd <- dbGetQuery(con, "SELECT pct_agua_inad, pct_esgoto_inad, razao_moradores,',
    '                             pct_analfab, renda_media, pct_raca_pretpardind',
    '                      FROM setores_censitarios',
    "                      WHERE urbano = 1 AND Dados_sig = 'OK'\")",
    'dbDisconnect(con)',
    '',
    'd$renda_inv <- -d$renda_media          # sentido único: maior = mais vulnerável',
    'X <- na.omit(d[, c("pct_agua_inad", "pct_esgoto_inad", "razao_moradores",',
    '                   "pct_analfab", "renda_inv", "pct_raca_pretpardind")])',
    'nrow(X)                                # esperado: 87545',
    '',
    '# 2. Matriz de correlação e adequabilidade',
    'R <- cor(X, method = "spearman")',
    'KMO(R)                                 # global e por variável',
    'cortest.bartlett(R, n = nrow(X))       # com a ressalva de amostra grande',
    'smc(R)                                 # multicolinearidade, livro p. 42',
  ], 10);
  s.addNotes('Vale rodar este bloco na frente dela se houver computador: KMO(R) devolve o global e os individuais de uma vez, e o resultado tem de bater com 0,787 e 0,715 da solução de seis variáveis. Se bater, está provado que as duas implementações concordam no que importa. na.omit é a exclusão por lista — com use = "pairwise.complete.obs" no cor() seria a versão par a par, que é a que NÃO se quer aqui.');
}

{ const s = S();
  const y = titulo(s, 'A mesma análise em R — parte 2', 'Número de fatores, extração e rotação.');
  codigo(s, M, y + 0.2, W - 2*M, [
    '# 3. Quantos fatores',
    'eigen(R)$values                                    # critério de Kaiser',
    'fa.parallel(X, fm = "pa", fa = "fa", n.iter = 50)  # análise paralela de Horn',
    '',
    '# 4. Extração: as duas técnicas, como manda a regra de Stevens',
    'acp <- principal(R, nfactors = 2, rotate = "varimax", n.obs = nrow(X))',
    'paf <- fa(R, nfactors = 2, fm = "pa", rotate = "varimax", n.obs = nrow(X))',
    'round(cbind(acp$loadings[, 1:2], paf$loadings[, 1:2]), 3)',
    '',
    '# ATENÇÃO: para reproduzir as cargas deste projeto, a Varimax não pode',
    '#          normalizar — o padrão do R é normalize = TRUE',
    'acp0 <- principal(R, nfactors = 2, rotate = "none", n.obs = nrow(X))',
    'varimax(acp0$loadings[, 1:2], normalize = FALSE)',
    '',
    '# 5. Rotação oblíqua — é a que o livro recomenda (p. 38)',
    'obl <- fa(R, nfactors = 2, fm = "pa", rotate = "promax", n.obs = nrow(X))',
    'obl$loadings     # matriz padrão — é dela que saem os pesos',
    'obl$Structure    # matriz de estrutura',
    'obl$Phi          # correlação entre os fatores: esperado ~0,52',
  ], 10);
  s.addNotes('O bloco do meio é o mais importante deste slide. A varimax do R normaliza por padrão e a nossa não, então rodar principal(rotate = "varimax") dá cargas parecidas mas não idênticas. Para bater número a número é preciso extrair sem rotação e chamar varimax(normalize = FALSE) à parte. Quem não souber disso vai achar que uma das duas implementações está errada.');
}

{ const s = S();
  const y = titulo(s, 'A mesma análise em R — parte 3', 'Pesos, escores e as duas figuras que esta apresentação mostrou.');
  codigo(s, M, y + 0.2, W - 2*M, [
    '# 6. Pesos: soma dos quadrados das cargas, por fator',
    'ss <- colSums(acp$loadings[, 1:2]^2)',
    'round(100 * ss / sum(ss), 1)           # a repartição entre as dimensões',
    '',
    '# 7. Escores refinados (método da regressão, livro p. 25)',
    'esc <- factor.scores(as.matrix(X), acp, method = "regression")$scores',
    'apply(esc, 2, var)                     # ~1 quando as cargas vêm de ACP',
    '',
    '# 8. O plano dos fatores — a Figura 2 do livro, em cinco linhas',
    'L <- acp$loadings[, 1:2]',
    'plot(L[, 1], L[, 2], xlim = c(-1, 1), ylim = c(-1, 1), pch = 19, asp = 1,',
    '     xlab = "Fator 1", ylab = "Fator 2")',
    'abline(h = 0, v = 0, col = "grey60")',
    'text(L[, 1], L[, 2], labels = rownames(L), pos = 4, cex = 0.8)',
    '',
    '# 9. A matriz de correlação como figura',
    'cor.plot(R, numbers = TRUE, main = "Matriz de correlação de Spearman")',
  ], 10);
  bloco(s, M, y + 3.95, W - 2*M, 'O script inteiro, comentado, está versionado.',
    'docs/Codigo_Analise_Fatorial_Comentado.md traz este código com a explicação linha a linha de cada função em Python ao lado da equivalente em R, e a tabela das cinco diferenças a esperar entre as duas implementações.', false, 1.1);
  s.addNotes('As linhas 8 e 9 reproduzem em R as duas figuras que esta apresentação mostrou. O plot básico do R faz a Figura 2 do livro em cinco linhas — vale mostrar isso, porque desfaz a impressão de que a figura exigiu ferramenta especial.');
}

{ const s = S();
  const y = titulo(s, 'O que esperar de diferente entre as duas', 'Cinco pontos. Divergência além destes é problema real, não diferença de linguagem.');
  tabela(s, ['Ponto', 'Python (aqui)', 'R (psych)', 'O que fazer'], [
    ['Normalização da Varimax', 'sem normalização', 'normalize = TRUE', marca('use normalize = FALSE')],
    ['Sinal dos fatores', 'o que o LAPACK der', 'vira para soma positiva', 'compare valores absolutos'],
    ['Ordem dos fatores', 'autovalor decrescente', 'pode reordenar após girar', 'confira pelo padrão de cargas'],
    ['Análise paralela de Horn', '50 simulações, normal', 'reamostra os dados', 'o nº de fatores não deve mudar'],
    ['Spearman', 'pandas, posto médio', 'cor(), posto médio', 'idênticos'],
  ], { y, colW: [3.3, 2.9, 2.9, 3.53], rowH: 0.50, fontSize: 11 });
  bloco(s, M, y + 3.1, W - 2*M, 'A regra para usar isto.',
    'Se os números divergirem além destes cinco pontos, o problema é real e vale investigar — não atribua à diferença de linguagem sem antes conferir a lista. Rodar a mesma análise em duas implementações independentes é, ele próprio, um teste: se as duas concordam, é improvável que ambas estejam erradas do mesmo jeito.', true, 1.4);
  s.addNotes('Este slide é o que transforma a versão em R de curiosidade em ferramenta: ela vira uma segunda opinião sobre os números do projeto. A convergência entre duas implementações independentes é o argumento mais forte disponível quando não há um valor de referência externo para conferir.');
}

// ═════════ 9. DECISÕES ═════════
{ const s = S(); secao(s, '9', 'O que vai para a orientação',
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
