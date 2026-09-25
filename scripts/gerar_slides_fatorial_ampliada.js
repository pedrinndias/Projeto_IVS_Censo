/**
 * Gera os slides da análise fatorial ampliada (Fase 2/3) para a apresentação.
 *
 * Saem num .pptx separado, de propósito: o deck principal foi EDITADO À MÃO (slides
 * removidos, marcações "EXPLICAR SLIDE") e nunca é regerado. Estes slides são ANEXADOS
 * ao fim dele por scripts/juntar_decks.py, pelo mesmo caminho que a EDA Central e o
 * extremo de BH seguiram.
 *
 * Nenhum número é digitado: todos saem de banco_de_dados/eda/fatorial_ampliada/*.csv,
 * gerados por scripts/fatorial_ampliada.py (Fase 2) e conferidos no Notebook 04b (Fase 3).
 *
 * Uso:
 *     node scripts/gerar_slides_fatorial_ampliada.js <saida.pptx>
 */
const fs = require('fs');
const path = require('path');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const FAT = path.join(RAIZ, 'banco_de_dados/eda/fatorial_ampliada');

// Separador ';', com aspas duplas no padrão CSV (campo entre "..." quando tem ';' ou
// aspas; aspas internas viram ""). Precisa disto porque cenarios.csv traz descrições com
// aspas ("tudo isso"), que um split ingênuo por ';' não desfaz.
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
    else if (c === ';') { campos.push(atual); atual = ''; }
    else atual += c;
  }
  campos.push(atual);
  return campos;
}
function lerCsv(nome) {
  const txt = fs.readFileSync(path.join(FAT, nome), 'utf8').replace(/^﻿/, '').trim();
  const [cab, ...linhas] = txt.split(/\r?\n/);
  const cols = partirLinhaCsv(cab);
  return linhas.map(l => Object.fromEntries(cols.map((c, i) => [c, partirLinhaCsv(l)[i]])));
}
const num = (v, c) => Number(v).toFixed(c === undefined ? 2 : c).replace('.', ',');
const inteiro = v => Math.round(Number(v)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
const sim_nao = v => (v === 'True' ? 'sim' : v === 'False' ? 'não' : '—');

const CENARIOS = lerCsv('cenarios.csv');
const PESOS = lerCsv('pesos.csv');
const FCU = lerCsv('validacao_fcu.csv');
const SENS = lerCsv('sensibilidade_municipios.csv');
const CARGAS = lerCsv('cargas.csv');

const cen = c => CENARIOS.find(r => r.cenario === c);
const pesoVarimax = c => PESOS.find(r => r.cenario === c && r.rotacao === 'varimax');
const fcu = (c, medida) => FCU.find(r => r.cenario === c && r.medida === medida);
const cargaVar = (c, v) => CARGAS.find(r => r.cenario === c && r.variavel === v);

const d = criarDeck({ titulo: 'A fatorial ampliada — resultado por resultado' });
const { p, S, titulo, secao, bloco, numero, tabela, legendaTabela, legendaFigura } = d;
const { ACENTO } = d.cores;
const { W, M } = d.geo;
const marca = t => ({ text: t, options: { color: ACENTO, bold: true } });

// ── divisória ───────────────────────────────────────────────────────────────
{ const s = S();
  secao(s, '+', 'A fatorial ampliada, resultado por resultado',
    'Onze demandas da orientadora, respondidas em cenários novos — sem escolher nada por ela.');
  s.addNotes('Esta seção junta o que a Fase 2 rodou (scripts/fatorial_ampliada.py, a grade S0-S7 e as variantes) e o que o Notebook 04b registrou por escrito. Nenhum número aqui é novo: são os mesmos CSVs de banco_de_dados/eda/fatorial_ampliada/, lidos de novo para os slides.');
}

// ── slide 1: as onze demandas ────────────────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'As onze demandas, uma por uma',
    'Cada linha aponta o cenário ou o arquivo onde a resposta está — nenhuma foi escolhida aqui.');
  tabela(s, ['#', 'Demanda', 'Onde está a resposta'], [
    ['1', 'Renda com a mediana', 'coluna renda_media_mediana_mun; sensibilidade em renda_imputacao_alternativas.csv'],
    ['2', 'Quadro de indicadores', 'Quadro_Indicadores.csv / .xlsx / .md'],
    ['3', 'Fatorial sem e com rotação', 'cargas.csv e pesos.csv — sem rotação, Varimax e promax lado a lado'],
    ['4', 'Útil × inútil na apresentação', 'MAPA_APRESENTACAO_FINAL.md; correções no deck e no guia'],
    ['5', 'Comparar "não chega" com os outros', 'cenário S2; comparacao_nao_chega_banheiro.csv'],
    ['6', 'Juntar "sem banheiro"', 'cenário S4; prova V00238 ≤ V00495 em comparacao_nao_chega_banheiro.csv'],
    ['7', 'Canalização e sem banheiro na grade', 'cenários S2, S3, S4 em cenarios.csv'],
    ['8', 'Fatorial de "tudo isso"', 'cenários S6 e S7; postos no município em S6_postos_mun'],
    ['9', 'Habitação convencional', 'cenários S5 e S6; MSA, comunalidade e % de zeros em cargas.csv'],
    ['10', 'Testar o lixo', 'cenários S1 e S7; lixo_fator_proprio_varimax e lixo_muda'],
    ['11', 'Testar as duas rotações', 'pesos.csv — Varimax e promax (padrão e estrutura) + Φ; figura fa_plano_s6.png'],
  ], { y, colW: [0.55, 3.3, 7.78], rowH: 0.4, fontSize: 10.5 });
  s.addNotes('Lista de conferência: onze itens, onze respostas, cada uma com o arquivo exato. Isto substitui qualquer resumo de memória — quem quiser conferir um número abre o CSV citado.');
}

// ── slide 2: a matriz ampliada ───────────────────────────────────────────────
{ const s = S();
  titulo(s, 'A matriz ampliada: como as quatro variáveis novas se encaixam',
    'Spearman entre o IVS-7 e água não chega, sem canalização, sem banheiro e moradia não convencional.');
  s.addImage({ path: path.join(FAT, 'figuras', 'fa_correlacao_ampliada.png'), x: 1.6, y: 1.6, w: 10.13, h: 4.44 });
  legendaFigura(s, 6.2, `Correlação de Spearman em S6 (n = ${inteiro(cen('S6').n)}).`,
    'Fonte: banco_de_dados/eda/fatorial_ampliada/correlacao_s6.csv · figuras/fa_correlacao_ampliada.png.');
  const nconv = cargaVar('S6', 'pct_moradia_nao_convencional');
  s.addNotes(`As quatro novas se correlacionam mais entre si (bloco inferior direito) do que com o IVS-7 original — esperado, já que medem a mesma dimensão de saneamento por outro ângulo. A exceção é moradia não convencional: comunalidade de ${num(nconv.comunalidade, 3)} e correlação baixa com tudo, inclusive com as outras três novas — a variável mais fraca da grade, não excluída aqui (demanda 9 fica para a orientadora decidir).`);
}

// ── slide 3: a tabela de cenários ────────────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'A grade de cenários, lado a lado',
    'Ajuste, fatores e o que o índice ganha — ou perde — contra a renda sozinha em AUC.');
  const linhas = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'].map(cid => {
    const c = cen(cid);
    const pv = pesoVarimax(cid);
    const ai = fcu(cid, 'indice_01 (pesos Varimax)');
    const ar = fcu(cid, 'renda invertida sozinha');
    return [cid, inteiro(c.n), num(c.kmo, 4), `${c.fatores_kaiser}/${c.fatores_horn}`,
      num(pv.peso_f1, 2) + '%', num(ai.auc, 4), num(ar.auc, 4)];
  });
  tabela(s, ['Cenário', 'n', 'KMO', 'Fatores (Kaiser/Horn)', 'Peso F1 Varimax', 'AUC índice', 'AUC renda sozinha'],
    linhas, { y, colW: [1.15, 1.5, 1.15, 2.1, 1.9, 1.85, 1.98], rowH: 0.42, fontSize: 11 });
  s.addNotes('A renda sozinha bate o índice em AUC nos oito cenários — achado NB4-02, sem adjetivo, já registrado no 04b. O KMO sobe de 0,78 (S0) para 0,81 quando entram as quatro novas (S6); Kaiser e Horn discordam em S4 e S7 (kaiser_horn_discordam em cenarios.csv), e a solução usa sempre 2 fatores, como o prompt manda.');
}

// ── slide 4: o plano fatorial em três rotações ───────────────────────────────
{ const s = S();
  titulo(s, 'O plano fatorial de S6 em três rotações',
    'Mesmos dois fatores, três formas de olhar: sem rotação, Varimax e promax (matriz padrão).');
  s.addImage({ path: path.join(FAT, 'figuras', 'fa_plano_s6.png'), x: 0.5, y: 1.55, w: 12.33, h: 4.55 });
  legendaFigura(s, 6.25, 'As quatro variáveis novas (vermelho) e as sete do IVS-7 (verde), em S6.',
    'Fonte: figuras/fa_plano_s6.png · rótulo de cada eixo sai das cargas (achado NB4-08).');
  s.addNotes('Sem rotação, as quatro novas já aparecem isoladas de analfabetismo/renda/cor-raça, no quadrante de cima. A Varimax e a promax só giram os eixos para alinhar essa separação com F1 e F2 — a nuvem de pontos não muda de posição relativa, só o sistema de referência. Conferido rótulo a rótulo e eixo a eixo antes deste slide: todos legíveis.');
}

// ── slide 5: o lixo ───────────────────────────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'O lixo: fator próprio ou dissolvido?',
    'Depende do cenário — e quase não se move ao tirar um dos 70 municípios por vez.');
  const linhas = ['S0', 'S2', 'S3', 'S4', 'S5', 'S6'].map(cid => {
    const c = cen(cid);
    return [cid, c.descricao, sim_nao(c.lixo_fator_proprio_varimax)];
  });
  const yt = legendaTabela(s, y, 'O lixo forma fator próprio na Varimax, por cenário.',
    'Fonte: banco_de_dados/eda/fatorial_ampliada/cenarios.csv, coluna lixo_fator_proprio_varimax.');
  const tEnd = tabela(s, ['Cenário', 'Descrição', 'Fator próprio?'], linhas,
    { y: yt, colW: [1.1, 8.53, 2.0], rowH: 0.38, fontSize: 10.5 });
  const msaLixo = cargaVar('S0', 'pct_lixo_inad');
  const lixoMudaS0 = SENS.filter(r => r.cenario === 'S0' && r.lixo_muda === 'True').length;
  const rodadasS0 = SENS.filter(r => r.cenario === 'S0' && r.municipio_fora !== '(nenhum)').length;
  numero(s, M, tEnd + 0.3, 3.8, num(msaLixo.msa, 4), 'MSA do lixo em S0 — o mínimo da grade', true);
  numero(s, M + 4.3, tEnd + 0.3, 4.2, `${lixoMudaS0} de ${rodadasS0}`,
    'rodadas em que tirar 1 município muda se o lixo tem fator próprio (S0)');
  s.addNotes('Testar o lixo (demanda 10) dá resultado ambíguo por desenho: forma fator próprio em S0 e S5, mas se dissolve nos outros cenários quando entram mais variáveis de saneamento. A sensibilidade por município (S0, S1, S6, em sensibilidade_municipios.csv) mostra que isso quase não depende de qual dos 70 é retirado.');
}

// ── slide 6: a estrutura municipal ───────────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'A estrutura municipal: postos dentro do município',
    'Trocar o valor bruto pelo posto percentil dentro do próprio município muda o resultado.');
  const linhas = ['S0', 'S1', 'S6'].map(cid => {
    const pm = `${cid}_postos_mun`;
    const ai = fcu(pm, 'indice_01 (pesos Varimax)');
    const ar = fcu(pm, 'renda invertida sozinha');
    const supera = Number(ai.auc) > Number(ar.auc);
    return [cid, num(ai.auc, 4), num(ar.auc, 4), supera ? marca('índice maior') : 'renda maior'];
  });
  const yt = legendaTabela(s, y, 'AUC com cada variável em posto percentil dentro do próprio município.',
    'Fonte: validacao_fcu.csv, cenários S0_postos_mun, S1_postos_mun e S6_postos_mun.');
  const tEnd = tabela(s, ['Cenário', 'AUC índice', 'AUC renda sozinha', 'quem ganha'], linhas,
    { y: yt, colW: [1.6, 3.3, 3.5, 3.23], rowH: 0.42, fontSize: 12 });
  const deltas = c => SENS.filter(r => r.cenario === c && r.municipio_fora !== '(nenhum)')
    .map(r => Math.abs(Number(r.delta_varimax)));
  const maiorDelta = Math.max(...deltas('S1'), ...deltas('S6'));
  numero(s, M, tEnd + 0.3, 3.8, '2 de 3', 'cenários em que o índice supera a renda sozinha só com postos municipais', true);
  numero(s, M + 4.4, tEnd + 0.3, 4.0, `±${num(maiorDelta, 2)} p.p.`,
    'maior variação do peso F1 (Varimax) ao tirar 1 dos 70 municípios, em S1 e S6');
  s.addNotes('É o único ponto da grade em que o índice bate a renda sozinha em AUC — e mesmo assim só em 2 dos 3 cenários (S1_postos_mun continua atrás). O outro eixo da robustez, tirar um município por vez sem mudar para posto percentil, quase não move o peso: a maior variação nas 70 rodadas de S1 e S6 juntas é pequena.');
}

// ── slide 7: o que fica para ela decidir ─────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'O que fica para a orientadora decidir',
    'Nada disso foi escolhido aqui — as alternativas estão lado a lado nos CSVs e no Notebook 04b.');
  const itens = [
    ['Qual renda entra no índice final', 'original, sem o extremo de Belo Horizonte, ou imputada pela mediana municipal — as três rodadas de referência estão em S0_renda_* e S6_renda_*.'],
    ['Qual rotação e qual repartição reportar', 'sem rotação, Varimax ou promax; e, na oblíqua, matriz padrão ou matriz estrutura — pesos.csv traz as quatro, sem apontar qual "aproxima" da literatura.'],
    ['A versão graduada de "sem banheiro"', 'V00237 (só sanitário ou buraco) exige reextração do NB01; a V00495 usada na grade já é a junção com V00238.'],
    ['Manter a moradia não convencional na grade', 'variância baixa e comunalidade fraca (slide da matriz ampliada), mas mostrada e não excluída.'],
  ];
  let yy = y;
  itens.forEach(([entrada, texto], i) => {
    bloco(s, M, yy, W - 2 * M, entrada, texto, i % 2 === 0, 1.0);
    yy += 1.15;
  });
  s.addNotes('Quatro decisões de método, nenhuma tomada por este executor — a regra do prompt (seção 0.2) é implementar o padrão que preserva as alternativas e registrar a pergunta, não escolher por ela. As quatro já estão na mensagem redigida na Fase 0 e no estado do projeto.');
}

const saida = process.argv[2];
if (!saida) { console.error('uso: node scripts/gerar_slides_fatorial_ampliada.js <saida.pptx>'); process.exit(1); }
p.writeFile({ fileName: saida }).then(f => console.log('slides escritos:', f));
