/**
 * Gera os slides do NB05 (a especificação de referência do IVS final) para o deck da
 * análise fatorial.
 *
 * Saem num .pptx separado, no mesmo padrão de scripts/gerar_slides_fatorial_ampliada.js:
 * o deck principal (106 slides, marcações "EXPLICAR SLIDE") nunca é regerado, só recebe
 * este bloco anexado por scripts/juntar_decks.py, a partir da versão do HEAD.
 *
 * Nenhum número é digitado: todos saem de banco_de_dados/eda/ivs_especificacoes/*.csv,
 * gerados por scripts/ivs_especificacoes.py (Fase C) e conferidos no Notebook 05 (Fase D).
 *
 * Uso:
 *     node scripts/gerar_slides_ivs_final.js <saida.pptx>
 */
const fs = require('fs');
const path = require('path');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const DIR = path.join(RAIZ, 'banco_de_dados/eda/ivs_especificacoes');

// Separador ',', padrão pandas.to_csv (RFC4180): campo entre "..." quando tem ',' ou
// aspas; aspas internas viram "". Diferente do ';' dos CSVs de fatorial_ampliada/.
function partirLinhaCsv(linha) {
  const campos = [];
  let atual = '', entreAspas = false;
  for (let i = 0; i < linha.length; i++) {
    const c = linha[i];
    if (entreAspas) {
      if (c === '"' && linha[i + 1] === '"') { atual += '"'; i++; }
      else if (c === '"') { entreAspas = false; }
      else atual += c;
    } else if (c === '"') { entreAspas = true; }
    else if (c === ',') { campos.push(atual); atual = ''; }
    else atual += c;
  }
  campos.push(atual);
  return campos;
}
function lerCsv(nome) {
  const txt = fs.readFileSync(path.join(DIR, nome), 'utf8').replace(/^﻿/, '').trim();
  const [cab, ...linhas] = txt.split(/\r?\n/);
  const cols = partirLinhaCsv(cab);
  return linhas.map(l => Object.fromEntries(cols.map((c, i) => [c, partirLinhaCsv(l)[i]])));
}
const num = (v, c) => Number(v).toFixed(c === undefined ? 2 : c).replace('.', ',');
const inteiro = v => Math.round(Number(v)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');

const ESP = lerCsv('especificacoes.csv');
const ACR = lerCsv('acrescimo_renda.csv');
const EST = lerCsv('estabilidade.csv');
const PES = lerCsv('pesos.csv');
const REF = lerCsv('referencia.csv');

const porId = id => ESP.find(r => r.id === id);
const eleg = ESP.filter(r => r.elegivel === 'True');
const elegMun = eleg.filter(r => r.normalizacao === 'municipal');

const idPrincipal = REF.find(r => r.leitura === 'principal').id;
const idPrincipalGlobal = idPrincipal.replace(/municipal$/, 'global');
const proposta = porId(idPrincipal);
const propostaGlobal = porId(idPrincipalGlobal);
const ivs7 = porId('original·lixo_com·banheiro_fora·varimax·ss·municipal');
const ivs7graduado = porId('original·lixo_com·banheiro_graduado·varimax·ss·municipal');
const ivs6 = porId('original·lixo_sem·banheiro_fora·varimax·ss·municipal');
const acrProposta = ACR.find(r => r.id === idPrincipal);
const pesosProposta = PES.find(r => r.renda === 'original' && r.lixo === 'sem' &&
  r.banheiro === 'graduado' && r.rotacao === 'promax' && r.metodo === '60_40');

const semRotacao = ESP.filter(r => r.rotacao === 'sem_rotacao');
const comunSemRotMin = Math.min(...semRotacao.map(r => Number(r.comunalidade_min)));
const comunSemRotMax = Math.max(...semRotacao.map(r => Number(r.comunalidade_min)));
const kmoMin = Math.min(...ESP.map(r => Number(r.kmo)));
const msaMin = Math.min(...ESP.map(r => Number(r.msa_min)));

const basesElegiveis = new Set(eleg.map(r => `${r.renda}|${r.lixo}|${r.banheiro}`));
const basesTotais = new Set(ESP.map(r => `${r.renda}|${r.lixo}|${r.banheiro}`));

const postoAMin = Math.min(...elegMun.map(r => Number(r.posto_a)));
const empatePesoFixo = elegMun.filter(r => Number(r.posto_a) === postoAMin).length;
const top8 = elegMun.slice().sort((a, b) => Number(a.posto_medio) - Number(b.posto_medio)).slice(0, 8);
const top8Fixos6040 = top8.filter(r => r.metodo === '60_40').length;

const dinamico = r => r.metodo !== '50_50' && r.metodo !== '60_40';
const estIvs6 = EST.filter(r => r.lixo === 'sem' && r.banheiro === 'fora' && dinamico(r));
const ampIvs6Min = Math.min(...estIvs6.map(r => Number(r.amp_peso_f1)));
const ampIvs6Max = Math.max(...estIvs6.map(r => Number(r.amp_peso_f1)));
const estIvs7v = EST.filter(r => r.lixo === 'com' && r.banheiro === 'v00495' && dinamico(r));
const ampIvs7vMin = Math.min(...estIvs7v.map(r => Number(r.amp_peso_f1)));
const ampIvs7vMax = Math.max(...estIvs7v.map(r => Number(r.amp_peso_f1)));

// Três leituras de renda no mesmo desenho da leitura principal (sem lixo, banheiro
// graduado, promax, 60/40, normalização municipal): só a coluna renda muda.
const rendaTrio = ['original', 'sem_extremo', 'mediana_mun'].map(rd =>
  porId(`${rd}·lixo_sem·banheiro_graduado·promax·60_40·municipal`));
const aucRendaSpread = Math.max(...rendaTrio.map(r => Number(r.auc_mun_comum))) -
                       Math.min(...rendaTrio.map(r => Number(r.auc_mun_comum)));
// Em pontos percentuais, para não exibir "0,0000" — a diferença é real, só pequena.
const aucRendaSpreadPP = aucRendaSpread * 100;

const d = criarDeck({ titulo: 'O NB05 — a especificação de referência do IVS final' });
const { S, titulo, secao, bloco, numero, tabela, legendaTabela } = d;
const { ACENTO } = d.cores;
const { W, M } = d.geo;
const marca = t => ({ text: t, options: { color: ACENTO, bold: true } });

// ── divisória ───────────────────────────────────────────────────────────────
{ const s = S();
  secao(s, '+', 'O NB05: a especificação de referência do IVS final',
    '324 especificações testadas por critérios fixados antes de rodar — a orientadora escolhe, o motor mede.');
  s.addNotes('Esta seção junta o motor da Fase C (scripts/ivs_especificacoes.py, banco_de_dados/eda/ivs_especificacoes/*.csv) e o Notebook 05 (notebooks/Fase3_EDA_ELSI/05_Calculo_IVS_Final.ipynb). Nenhum número aqui é novo: são os mesmos CSVs, lidos de novo para os slides.');
}

// ── slide 1: a grade e a elegibilidade ───────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'A grade: 324 especificações, 192 elegíveis',
    'Três critérios fixados antes de rodar (seção 2.2) decidem quem entra na comparação.');
  numero(s, M, y, 2.7, inteiro(ESP.length), 'especificações — 3 rendas × 2 lixo × 3 banheiro × 9 pesos × 2 normalizações');
  numero(s, M + 2.9, y, 2.7, `${inteiro(eleg.length)} de ${inteiro(ESP.length)}`, 'elegíveis (96 por normalização): KMO, MSA e comunalidade acima do corte, 2 fatores interpretáveis', true);
  numero(s, M + 5.8, y, 2.7, `${basesElegiveis.size} de ${basesTotais.size}`, 'bases (renda×lixo×banheiro) com ao menos uma especificação elegível');
  numero(s, M + 8.7, y, 2.9, `≥ ${num(kmoMin, 3)}`, `KMO em toda a grade — MSA sempre ≥ ${num(msaMin, 3)}`);
  const yt = legendaTabela(s, y + 1.2, 'Por que as demais ficam de fora.',
    'Fonte: banco_de_dados/eda/ivs_especificacoes/especificacoes.csv.');
  tabela(s, ['Base ou esquema', 'Variável crítica', 'Comunalidade'], [
    ['IVS-7 (água, esgoto, lixo, moradores, analfabetismo, renda, cor/raça)', ivs7.comunalidade_min_variavel, `${num(ivs7.comunalidade_min, 4)} < 0,30`],
    ['IVS-7 + banheiro graduado', ivs7graduado.comunalidade_min_variavel, `${num(ivs7graduado.comunalidade_min, 4)} < 0,30 (a ${num(0.30 - Number(ivs7graduado.comunalidade_min), 4)} do corte)`],
    ['Sem rotação (1 fator), as 36 bases', 'varia por base', `entre ${num(comunSemRotMin, 4)} e ${num(comunSemRotMax, 4)}`],
  ], { y: yt, colW: [5.3, 3.8, 2.53], rowH: 0.5, fontSize: 10.5 });
  s.addNotes('Elegibilidade não é escolha: é a regra da seção 2.2 aplicada às 324 linhas de especificacoes.csv. Kaiser e Horn indicam 1 fator no IVS-6, mas o fator único reprova em toda a grade pela comunalidade — por isso a comparação de referência sempre usa 2 fatores.');
}

// ── slide 2: renda ────────────────────────────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'Renda: as três versões, coladas',
    'Original, sem o extremo de Belo Horizonte e mediana municipal — mesmo desenho, resultado quase idêntico.');
  const nomes = { original: 'Original', sem_extremo: 'Sem o extremo de BH', mediana_mun: 'Mediana municipal' };
  const linhas = rendaTrio.map(r => [nomes[r.renda], num(r.auc_mun_comum, 4), num(r.posto_medio, 2),
    r.id === idPrincipal ? marca('leitura principal') : '—']);
  const yt = legendaTabela(s, y, 'Mesma especificação (sem lixo, banheiro graduado, promax, 60/40, normalização municipal) — só a renda muda.',
    'Fonte: especificacoes.csv, colunas auc_mun_comum e posto_medio.');
  const tEnd = tabela(s, ['Renda', 'AUC municipal (amostra comum)', 'Posto médio', ''], linhas,
    { y: yt, colW: [3.0, 3.6, 2.23, 2.8], rowH: 0.42, fontSize: 12 });
  numero(s, M, tEnd + 0.3, 4.6, `${num(aucRendaSpreadPP, 4)} p.p.`, 'de diferença entre a maior e a menor AUC municipal, nas três rendas (pontos percentuais)', true);
  numero(s, M + 4.9, tEnd + 0.3, 4.6, `${num(rendaTrio[0].posto_a, 1)}º / ${num(rendaTrio[0].posto_b, 1)}º / ${num(rendaTrio[0].posto_c, 1)}º`,
    'posto da leitura principal nos três critérios — estabilidade, AUC municipal, parcimônia');
  s.addNotes('A escolha da renda quase não move o resultado agregado: a AUC contra FCU, dentro do município, é igual até a 4ª casa decimal nas três versões — a ordem entre elas no ranking de 96 especificações sai de diferenças menores que essa. O critério da seção 2.2 não resolve sozinho qual renda usar: a escolha continua sendo da orientadora.');
}

// ── slide 3: rotação e pesos na oblíqua ──────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'Rotação e pesos: o critério de estabilidade degenera nos pesos fixos',
    'Sem rotação nunca passa; entre Varimax e promax, quem decide é como o peso entre os dois fatores é medido.');
  numero(s, M, y, 3.6, `${empatePesoFixo} de ${elegMun.length}`, 'elegíveis (normalização municipal) empatam no critério (a) — pesos fixos, amplitude zero por construção', true);
  numero(s, M + 3.9, y, 3.6, `${top8Fixos6040} de ${top8.length}`, 'das 8 primeiras posições da leitura principal usam o peso 60/40 da literatura');
  numero(s, M + 7.8, y, 3.83, `${num(ampIvs6Min, 2)}–${num(ampIvs6Max, 2)} p.p.`, 'amplitude do peso de F1 ao tirar 1 dos 70 municípios, métodos que dependem dos dados (IVS-6 sem banheiro)');
  const yt = legendaTabela(s, y + 1.3, `Pesos da leitura principal — fator 1 = ${num(pesosProposta.peso_f1, 1)}%, fator 2 = ${num(pesosProposta.peso_f2, 1)}% (peso 60/40 da literatura).`,
    'Fonte: pesos.csv.');
  tabela(s, ['Variável', 'Peso (%)'], [
    ['Água inadequada', num(pesosProposta.peso_pct_agua_inad, 2)],
    ['Esgoto inadequado', num(pesosProposta.peso_pct_esgoto_inad, 2)],
    ['Razão de moradores', num(pesosProposta.peso_razao_moradores, 2)],
    ['Analfabetismo 15+', num(pesosProposta.peso_pct_analfab, 2)],
    ['Renda (invertida)', num(pesosProposta.peso_renda_inv, 2)],
    ['Cor/raça PPI', num(pesosProposta.peso_pct_raca_pretpardind, 2)],
    ['Banheiro graduado', num(pesosProposta.peso_banheiro_graduado, 2)],
  ], { y: yt, colW: [7.0, 4.63], rowH: 0.3, fontSize: 10.5 });
  s.addNotes(`O critério (a) da seção 2.2 (menor amplitude do peso de F1 ao tirar 1 município) empata trivialmente nos pesos fixos — amplitude zero por construção, não por robustez medida; é por isso que a leitura alternativa "estabilidade pelos pesos das variáveis" (referencia.csv) muda a proposta. Na base com mais variáveis (IVS-7 + V00495) a mesma amplitude sobe para ${num(ampIvs7vMin, 2)}–${num(ampIvs7vMax, 2)} p.p. — mais variáveis, mais sensível a qual município sai. Fator único (sem rotação) nunca chega a este ponto: já caiu na comunalidade.`);
}

// ── slide 4: lixo e banheiro ──────────────────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'Lixo e banheiro: quatro bases elegíveis, duas não',
    'O lixo não reprova sozinho; o banheiro decide quem entra — fora, V00495 ou o graduado da Fase B.');
  const yt = legendaTabela(s, y, 'As seis combinações de lixo × banheiro; elegível = alguma rotação/peso passa nos três cortes.',
    'Fonte: especificacoes.csv, agregado por renda·lixo·banheiro (renda original).');
  tabela(s, ['Base', 'Lixo', 'Banheiro', 'Elegível em alguma rotação?'], [
    ['IVS-6 (sem lixo) + fora', 'sem', 'fora', 'sim'],
    ['IVS-6 + V00495', 'sem', 'V00495', 'sim'],
    ['IVS-6 + graduado', 'sem', 'graduado', 'sim'],
    ['IVS-7 (com lixo) + fora — índice do NB04', 'com', 'fora', 'não'],
    ['IVS-7 + V00495', 'com', 'V00495', 'sim'],
    ['IVS-7 + graduado', 'com', 'graduado', 'não'],
  ], { y: yt, colW: [5.3, 1.6, 2.13, 2.6], rowH: 0.42, fontSize: 11 });
  s.addNotes(`O lixo em si não é o problema: IVS-6 (sem lixo) passa nas três versões de banheiro, e IVS-7 + V00495 (com lixo) também passa — quem reprova o IVS-7 puro é a comunalidade da água (${num(ivs7.comunalidade_min, 4)}), não o lixo. O banheiro graduado só reprova quando junto do lixo (IVS-7 + graduado, comunalidade ${num(ivs7graduado.comunalidade_min, 4)} — a ${num(0.30 - Number(ivs7graduado.comunalidade_min), 4)} do corte de 0,30); sozinho, com o IVS-6, ele passa.`);
}

// ── slide 5: o que o índice acrescenta à renda ───────────────────────────────
{ const s = S();
  const y = titulo(s, 'O que o índice acrescenta à renda',
    'Renda sozinha separa mais no agregado; o índice separa mais dentro do estrato de renda do próprio município.');
  const yt = legendaTabela(s, y, 'AUC contra FCU, na leitura principal — índice, renda sozinha e média de postos, em três recortes.',
    'Fonte: acrescimo_renda.csv, linha da leitura principal (referencia=True).');
  const tEnd = tabela(s, ['Recorte', 'Índice', 'Renda sozinha', 'Média de postos'], [
    ['Global', num(acrProposta.auc_indice_global, 4), num(acrProposta.auc_renda_global, 4), num(acrProposta.auc_postos_global, 4)],
    ['Mediana municipal (31 municípios)', num(acrProposta.auc_indice_mun, 4), num(acrProposta.auc_renda_mun, 4), num(acrProposta.auc_postos_mun, 4)],
    [`Dentro dos ${inteiro(acrProposta.n_estratos)} estratos de renda`, marca(num(acrProposta.auc_indice_estratos, 4)), num(acrProposta.auc_renda_estratos, 4), num(acrProposta.auc_postos_estratos, 4)],
  ], { y: yt, colW: [4.5, 2.5, 2.7, 2.93], rowH: 0.5, fontSize: 11.5 });
  numero(s, M, tEnd + 0.3, 3.9, `−${num(acrProposta.queda_deviance, 1)}`, `queda de deviance ao somar o índice à renda na logística (z = ${num(acrProposta.z_indice, 1)})`, true);
  numero(s, M + 4.2, tEnd + 0.3, 4.5, `${num(acrProposta.auc_modelo_renda, 4)} → ${num(acrProposta.auc_modelo_renda_indice, 4)}`, 'AUC do modelo logístico, só renda → renda + índice');
  s.addNotes('A renda bate o índice em AUC no agregado e por município — mas dentro dos estratos de renda do próprio município (mesma faixa, municípios diferentes) o índice separa mais FCU que a renda. Limite: FCU já é critério do IBGE que usa condições de moradia, então há circularidade parcial com as variáveis de saneamento do índice.');
}

// ── slide 6: a referência proposta e as alternativas ─────────────────────────
{ const s = S();
  const y = titulo(s, 'A referência proposta, e três leituras alternativas dos mesmos critérios',
    'Mesma seção 2.2; muda só como medir "estabilidade" e qual amostra usar — muda a proposta.');
  const nomeLeitura = { principal: 'Leitura principal', amostra_propria: 'Amostra própria',
    estabilidade_pesos_variaveis: 'Estabilidade por pesos', normalizacao_global: 'Normalização global' };
  const linhas = REF.map(r => [nomeLeitura[r.leitura] || r.leitura, r.id.replace(/·/g, ' · '), num(r.posto_medio, 2)]);
  const yt = legendaTabela(s, y, 'A especificação de melhor posto médio em cada leitura dos critérios (a), (b) e (c).',
    'Fonte: referencia.csv.');
  const tEnd = tabela(s, ['Leitura', 'Especificação', 'Posto médio'], linhas,
    { y: yt, colW: [2.6, 7.23, 1.8], rowH: 0.5, fontSize: 9.5 });
  const comparacoes = [
    ['Índice do NB04 (IVS-7 Varimax SS municipal)', ivs7],
    ['A mesma proposta, com normalização global', propostaGlobal],
    ['IVS-6 Varimax SS municipal (sem lixo, sem banheiro)', ivs6],
  ];
  let yy = tEnd + 0.2;
  comparacoes.forEach(([nome, r], i) => {
    bloco(s, M, yy, W - 2 * M, nome,
      `Spearman ${num(r.spearman_ref_comum, 3)} com a proposta; muda de faixa (regra do IVS-BH) ${num(r.muda_faixa_ivs_bh_comum, 1)}% dos setores.`,
      i === 0, 0.48);
    yy += 0.5;
  });
  s.addNotes('A proposta muda pouco de faixa em relação a outras leituras plausíveis do mesmo critério (10,2% a 10,4%) e muito mais em relação ao índice hoje em uso no NB04 (33,0%) — a maior parte da diferença vem de trocar renda, lixo e banheiro juntos, não de uma peça isolada.');
}

// ── slide 7: o que fica para a orientadora decidir ───────────────────────────
{ const s = S();
  const y = titulo(s, 'O que fica para a orientadora decidir',
    'Nada foi escolhido aqui — as alternativas estão lado a lado no Notebook 05 e nos CSVs desta pasta.');
  const itens = [
    ['Qual renda', `as três (original, sem extremo, mediana municipal) empatam em AUC municipal até a 4ª casa (diferença real de ${num(aucRendaSpreadPP, 4)} p.p.) — a escolha é conceitual, não estatística.`],
    ['O corte de comunalidade 0,30 é rígido?', `o banheiro graduado com lixo fica a ${num(0.30 - Number(ivs7graduado.comunalidade_min), 4)} do corte (${num(ivs7graduado.comunalidade_min, 4)}) — a regra da seção 2.2, como escrita, não abre exceção de fronteira.`],
    ['Como medir "estabilidade" no critério (a)', 'pela amplitude do peso de F1 (degenera nos pesos fixos, decide pela proposta com 60/40) ou pela amplitude dos pesos das variáveis (muda a proposta para promax·comunalidades).'],
    ['Normalização e faixas', `municipal ou global — trocar muda de faixa ${num(propostaGlobal.muda_faixa_ivs_bh_comum, 1)}% dos setores; a regra de faixas usada aqui é a do IVS-BH 2012, com quartis municipais como sensibilidade.`],
  ];
  let yy = y;
  itens.forEach(([entrada, texto], i) => { bloco(s, M, yy, W - 2 * M, entrada, texto, i % 2 === 0, 1.05); yy += 1.2; });
  s.addNotes('Quatro decisões de método, nenhuma tomada por este executor — a regra do prompt (seção 0.2) é calcular todas as alternativas e registrar a pergunta. A lista completa, com as herdadas do pedido original, está na seção 11 do Notebook 05 e no Relatorio_IVS_Final_NB05.md.');
}

const saida = process.argv[2];
if (!saida) { console.error('uso: node scripts/gerar_slides_ivs_final.js <saida.pptx>'); process.exit(1); }
d.p.writeFile({ fileName: saida }).then(f => console.log('slides escritos:', f));
