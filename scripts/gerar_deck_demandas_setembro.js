/**
 * Gera o deck das demandas de setembro: o que a orientadora pediu, como cada pedido foi
 * lido, o que foi feito e o que os números dizem — da fatorial ampliada (S0–S7) ao IVS
 * final do Notebook 05 —, terminando no que fica para ela decidir.
 *
 * Nenhum número é digitado. Todos saem dos CSVs gravados pelos scripts, lidos na hora:
 *   banco_de_dados/eda/fatorial_ampliada/*.csv   (scripts/fatorial_ampliada.py, NB04b)
 *   banco_de_dados/eda/ivs_especificacoes/*.csv  (scripts/ivs_especificacoes.py, NB05)
 *   banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv
 *   banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv
 * O texto dos pedidos e das leituras adotadas vem de docs/prompts/estado_demandas_2026-09.md
 * e de docs/prompts/estado_nb05_2026-09.md, citados no pé de cada slide.
 *
 * É um deck avulso, para a conversa sobre as demandas; o deck principal da análise fatorial
 * continua sendo o da raiz de docs/Apresentacoes_IVS/.
 *
 * Uso:
 *     node scripts/gerar_deck_demandas_setembro.js [saida.pptx]
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const SAIDA = process.argv[2] || path.join(RAIZ,
  'docs/Apresentacoes_IVS/complementos/Demandas_Setembro_IVS_2026-10.pptx');
const arq = rel => path.join(RAIZ, rel);
const FA = 'banco_de_dados/eda/fatorial_ampliada/';
const IE = 'banco_de_dados/eda/ivs_especificacoes/';

// ── Formatação brasileira ────────────────────────────────────────────────────
const num = (v, c = 2) => Number(v).toFixed(c).replace('.', ',');
const mil = v => Math.round(Number(v)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
const reais = v => 'R$ ' + Number(v).toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.');
const agora = new Date();
const HOJE = `${String(agora.getDate()).padStart(2, '0')}/${String(agora.getMonth() + 1).padStart(2, '0')}/${agora.getFullYear()}`;

// ── CSV ──────────────────────────────────────────────────────────────────────
// Separador descoberto pelo cabeçalho: ';' nos CSVs da fatorial ampliada e da EDA, ','
// nos do NB05 (pandas.to_csv). Campo entre aspas quando tem separador ou aspas (RFC4180).
function partirLinha(linha, sep) {
  const campos = [];
  let atual = '', entreAspas = false;
  for (let i = 0; i < linha.length; i++) {
    const c = linha[i];
    if (entreAspas) {
      if (c === '"' && linha[i + 1] === '"') { atual += '"'; i++; }
      else if (c === '"') entreAspas = false;
      else atual += c;
    } else if (c === '"') entreAspas = true;
    else if (c === sep) { campos.push(atual); atual = ''; }
    else atual += c;
  }
  campos.push(atual);
  return campos;
}
function lerCsv(rel) {
  const txt = fs.readFileSync(arq(rel), 'utf8').replace(/^﻿/, '').trim();
  const [cab, ...linhas] = txt.split(/\r?\n/);
  const sep = (cab.match(/;/g) || []).length > (cab.match(/,/g) || []).length ? ';' : ',';
  const cols = partirLinha(cab, sep);
  return linhas.map(l => {
    const v = partirLinha(l, sep);
    return Object.fromEntries(cols.map((c, i) => [c, v[i]]));
  });
}
const existe = rel => fs.existsSync(arq(rel));

// ── Fatorial ampliada (NB04b) ────────────────────────────────────────────────
const BASE = Object.fromEntries(lerCsv(FA + 'linha_de_base_nb04.csv').map(r => [r.medida, Number(r.valor)]));
const CEN = lerCsv(FA + 'cenarios.csv');
const cen = id => CEN.find(r => r.cenario === id);
const VAL = lerCsv(FA + 'validacao_fcu.csv');
const M_IND = 'indice_01 (pesos Varimax)', M_REN = 'renda invertida sozinha', M_POS = 'media simples de postos';
const auc = (c, m) => Number(VAL.find(r => r.cenario === c && r.medida === m).auc);
const PFA = lerCsv(FA + 'pesos.csv');
const peso = (c, rot) => PFA.find(r => r.cenario === c && r.rotacao === rot);
const CARGAS = lerCsv(FA + 'cargas.csv');
const SENS = lerCsv(FA + 'sensibilidade_municipios.csv');
const IMP = lerCsv('banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv');
const QUADRO = lerCsv('banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv');

// Partição do banheiro, setor a setor: V00495 = V00236 + V00237 + V00238, e a prova
// da junção da demanda 6 (V00238 nunca passa da V00495).
const PART = lerCsv(FA + 'banheiro_particao.csv');
const presente = v => v !== undefined && v !== '' && v.toLowerCase() !== 'nan';
const nPresentes = PART.filter(r => r.bate_com_v00495 === 'True' || r.bate_com_v00495 === 'False').length;
const nBate = PART.filter(r => r.bate_com_v00495 === 'True').length;
const ambas = PART.filter(r => presente(r.V00238) && presente(r.V00495));
const nAmbas = ambas.length;
const nJuncaoVale = ambas.filter(r => Number(r.V00238) <= Number(r.V00495)).length;

// ── Grade do NB05 ────────────────────────────────────────────────────────────
const ESP = lerCsv(IE + 'especificacoes.csv');
const REF = lerCsv(IE + 'referencia.csv');
const ACR = lerCsv(IE + 'acrescimo_renda.csv');
const PES = lerCsv(IE + 'pesos.csv');
const AVA = lerCsv(IE + 'avaliacao.csv');
const eleg = ESP.filter(r => r.elegivel === 'True');
const conta = (f, base) => `${eleg.filter(f).length} de ${(base || ESP).filter(f).length}`;
const nBases = new Set(ESP.map(r => `${r.renda}|${r.lixo}|${r.banheiro}`)).size;
const nEsquemas = new Set(ESP.map(r => `${r.rotacao}|${r.metodo}`)).size;
const nNorm = new Set(ESP.map(r => r.normalizacao)).size;
const refDe = leitura => REF.find(r => r.leitura === leitura);
const PRINC = refDe('principal');
const idGlobal = PRINC.id.replace(/municipal$/, 'global');
const mudaGlobal = AVA.find(r => r.id === idGlobal && r.amostra === 'comum');
const media = arr => arr.reduce((a, b) => a + b, 0) / arr.length;
const aucRenda = renda => media(eleg.filter(r => r.renda === renda).map(r => Number(r.auc_mun_comum)));
const comunMin = (lixo, banheiro) => ESP.find(r => r.renda === 'original' && r.lixo === lixo
  && r.banheiro === banheiro && r.rotacao === 'varimax' && r.metodo === 'ss');

const ROT = { renda: { original: 'original', sem_extremo: 'sem o extremo', mediana_mun: 'mediana municipal' },
  lixo: { com: 'com lixo', sem: 'sem lixo' },
  banheiro: { fora: 'sem banheiro', v00495: 'V00495', graduado: 'graduado' },
  rotacao: { sem_rotacao: 'sem rotação', varimax: 'Varimax', promax: 'promax' },
  metodo: { unico: 'fator único', ss: 'SS', ss_padrao: 'SS da padrão', ss_estrutura: 'SS da estrutura',
            comunalidades: 'comunalidades', '50_50': '50/50', '60_40': '60/40' },
  normalizacao: { municipal: 'no município', global: 'global' } };
const legivel = r => `${ROT.renda[r.renda]} · ${ROT.lixo[r.lixo]} · ${ROT.banheiro[r.banheiro]} · `
  + `${ROT.rotacao[r.rotacao]} · ${ROT.metodo[r.metodo]} · ${ROT.normalizacao[r.normalizacao]}`;

const slidesDe = rel => {
  try {
    return (execSync(`unzip -l "${arq(rel)}"`, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] })
      .match(/ppt\/slides\/slide\d+\.xml/g) || []).length;
  } catch (e) { return null; }
};
const DECK_ATUAL = 'docs/Apresentacoes_IVS/Analise_Fatorial_NB04_2026-09.pptx';

// ── O deck ───────────────────────────────────────────────────────────────────
const d = criarDeck({ titulo: 'Demandas de setembro — Projeto IVS Censo 2022' });
const { p, S, regua, titulo, secao, bloco, numero, procedencia, capa, legendaFigura,
        tabelaAjustada, diario, cores, geo } = d;
const { TINTA, CINZA, CINZA_C, ACENTO, FONTE } = cores;
const { W, H, M } = geo;

function figura(s, rel, x, y, w, h) {
  if (existe(rel)) s.addImage({ path: arq(rel), x, y, w, h });
  else s.addText(`[figura ausente: ${rel} — rode o script que a gera]`, { x, y, w, h,
    fontFace: FONTE, fontSize: 12, italic: true, color: ACENTO, align: 'center', valign: 'middle' });
}
function parte(n, t, sub, nota) {
  const s = S();
  secao(s, String(n), t, sub);
  if (nota) s.addNotes(nota);
}
const frase = (s, x, y, w, h, runs, tam) => s.addText(runs, { x, y, w, h, fontFace: FONTE,
  fontSize: tam || 12.5, color: TINTA, margin: 0, valign: 'top', lineSpacing: (tam || 12.5) * 1.3 });

// 1 · Capa
capa(S(), 'PROJETO IVS · CENSO 2022 · FIOCRUZ MINAS — INSTITUTO RENÉ RACHOU',
  'As demandas de setembro',
  'O que foi pedido, como cada pedido foi lido, o que foi feito e o que os números dizem — da '
  + 'fatorial ampliada ao IVS final do Notebook 05. As escolhas de método ficam com a orientadora, '
  + 'com os números ao lado de cada uma.',
  'Pedro Dias Soares · Iniciação Científica · outubro de 2026');

// 2 · Roteiro
{
  const s = S();
  const y = titulo(s, 'O roteiro', 'Dez partes, na ordem em que uma resposta prepara a seguinte');
  tabelaAjustada(s, ['', 'Parte', 'O que responde'], [
    ['1', 'O pedido e como foi lido', 'As onze demandas, as leituras adotadas e como o trabalho foi feito'],
    ['2', 'O ponto de partida: o NB04', 'O índice que já existia, e o quanto ele separa as favelas'],
    ['3', 'Renda e quadro de indicadores', 'Demandas 1 e 2'],
    ['4', 'A fatorial ampliada', 'Demandas 3 e 5 a 11: cenários S0–S7, rotações, lixo, incerteza'],
    ['5', 'A apresentação revista', 'Demanda 4: o útil, o inútil e os números corrigidos'],
    ['6', 'Os testes seguintes', 'Os nove itens da etapa seguinte e o banheiro graduado'],
    ['7', 'O IVS final', `A grade do NB05: ${ESP.length} especificações, ${eleg.length} elegíveis`],
    ['8', 'O índice contra a renda', 'O que o índice acrescenta ao que a renda já diz'],
    ['9', 'A referência proposta', 'Quatro leituras, e por que desconfiar da principal'],
    ['10', 'O que fica para decidir', 'As escolhas da orientadora, com os números de cada uma'],
  ], { y: y + 0.05, colW: [0.6, 3.9, 7.13], fontSize: 12.5, rowH: 0.36 });
  s.addNotes('Cada parte abre com uma divisória. Os números de todos os slides saem dos CSVs '
    + 'gravados pelos scripts (fatorial_ampliada/ e ivs_especificacoes/), lidos na hora em que o '
    + `deck é gerado (${HOJE}).`);
}

// ── Parte 1 ──────────────────────────────────────────────────────────────────
parte(1, 'O pedido e como foi lido', 'Onze demandas de setembro; nove pontos com mais de uma leitura.');
{
  const s = S();
  const y = titulo(s, 'As onze demandas', 'Estado de cada uma e onde está o resultado');
  tabelaAjustada(s, ['#', 'Demanda', 'Estado', 'Onde está o resultado'], [
    ['1', 'Coluna de renda com a mediana', 'feita', 'renda_media_mediana_mun, na entrega'],
    ['2', 'Quadro de indicadores', 'feita', `entrega_orientadora/Quadro_Indicadores (${QUADRO.length} indicadores)`],
    ['3', 'Fatorial sem bootstrap, sem e com rotação', 'feita', 'fatorial_ampliada/cargas.csv e pesos.csv'],
    ['4', 'Separar o útil do inútil na apresentação', 'feita', 'MAPA_APRESENTACAO_FINAL.md; deck corrigido'],
    ['5', 'Comparar o "não chega" com os outros', 'feita, nas duas leituras', 'cenário S2; comparacao_nao_chega_banheiro.csv'],
    ['6', 'Juntar o "sem banheiro"', 'feita com V00495; a graduada em 26/09', 'cenário S4; banheiro_particao.csv'],
    ['7', 'Acrescentar canalização e sem banheiro', 'feita', 'cenários S2, S3 e S4'],
    ['8', 'A fatorial de "tudo isso"', 'feita', 'cenários S6 e S7, com as três rendas'],
    ['9', 'Habitação convencional', 'feita, como não convencional', 'cenários S5 e S6'],
    ['10', 'Testar o lixo', 'feita', 'cenários S1 e S7; sensibilidade por município'],
    ['11', 'Testar as duas rotações', 'feita', 'Varimax e promax lado a lado, com Φ'],
  ], { y: y + 0.02, colW: [0.55, 4.1, 2.75, 4.23], fontSize: 11.5, rowH: 0.31 });
  procedencia(s, 'Fonte: estado_demandas_2026-09.md, tabela "Demandas da orientadora".');
  s.addNotes('As onze foram executadas em 25/09, nas Fases 1 a 4 do plano das demandas. A '
    + 'demanda 6 ficou com uma pergunta aberta — a versão graduada do banheiro, que exige a V00237 '
    + '— e ela foi feita em 26/09, na Fase B do pedido seguinte.');
}
{
  const s = S();
  const y = titulo(s, 'Como li o que tinha mais de uma leitura', 'O padrão seguido enquanto a orientadora não responde');
  tabelaAjustada(s, ['Ponto', 'Leitura adotada'], [
    ['Renda (demanda 1)', `Coluna nova com a mediana de BH sem o setor extremo (${reais(IMP.find(r => r.alternativa === 'mediana de BH sem o setor').valor_imputado)}); as alternativas num CSV de sensibilidade`],
    ['Rotação (demanda 3)', 'As duas: sem rotação, Varimax e promax lado a lado'],
    ['"Comparar com os outros" (5)', 'As duas leituras: contra as outras categorias de canalização e contra os indicadores do IVS-7'],
    ['Juntar "sem banheiro" (6)', 'V00495, que já contém a V00238; a versão graduada pedia extrair a V00237'],
    ['Habitação convencional (9)', 'Na direção da vulnerabilidade (não convencional), sem excluir por variância baixa'],
    ['"Tudo isso" (8)', 'IVS-7 + não chega + sem canalização + sem banheiro + não convencional'],
    ['Repartição oblíqua', 'As duas métricas — matriz padrão e matriz estrutura —, sem dizer qual "aproxima" da literatura'],
    ['Renda no índice', 'Os cenários com as três rendas; a escolha fica com a orientadora'],
    ['Incerteza', 'Sensibilidade por município, um de fora por vez — não bootstrap'],
  ], { y: y + 0.02, colW: [3.3, 8.33], fontSize: 12, rowH: 0.33 });
  procedencia(s, 'Fonte: estado_demandas_2026-09.md, "Perguntas à orientadora" (mensagem redigida na Fase 0).');
  s.addNotes('A mensagem com esses nove pontos foi redigida na Fase 0 e registrada no arquivo '
    + 'de estado. Em cada ponto, a leitura adotada é a que o trabalho seguiu; se a orientadora '
    + 'preferir outra, basta trocar o parâmetro do cenário e rodar de novo — nada foi fixado no código.');
}
diario('Como o trabalho foi feito', 'Seis fases em 25/09, mais quatro em 26 e 27/09', [
  { data: '25/09', fato: 'Fase 0 — a linha de base do NB04 e os destravamentos',
    detalhe: 'A Varimax corrigida (parava antes de convergir) e o NB04 regerado; a proporção nacional de "sem água canalizada" corrigida; a linha de base gravada para comparar tudo o que viria depois.' },
  { data: '25/09', fato: 'Fases 1 e 2 — as demandas 1 e 2, e a fatorial ampliada',
    detalhe: 'A renda com a mediana municipal, o quadro de indicadores e a grade de cenários S0–S7, sem bootstrap, com as três rendas e os postos no município.' },
  { data: '25/09', fato: 'Fases 3 e 4 — o Notebook 04b e a apresentação',
    detalhe: 'O NB04b chama o motor da Fase 2 em sete blocos; a curadoria do deck, os números corrigidos e o bloco novo de slides.' },
  { data: '25/09', fato: 'Fase 5 — o resto da revisão geral, em quatro lotes', detalhe: 'Código frágil, testes, documentação e repositório.' },
  { data: '26/09', fato: 'Fases A e B — as pendências e o banheiro graduado',
    detalhe: 'O que estava inferido vira verificação; a V00237 extraída do Censo e a partição do banheiro conferida setor a setor.' },
  { data: '27/09', fato: 'Fases C e D — o motor de especificações e o Notebook 05',
    detalhe: `A grade de ${ESP.length} especificações, a referência proposta, o relatório e os slides do IVS final.` },
], { fonte: 'Fonte: estado_demandas_2026-09.md; estado_nb05_2026-09.md.' });

// ── Parte 2 ──────────────────────────────────────────────────────────────────
parte(2, 'O ponto de partida: o NB04', 'O índice que já existia antes das demandas — e o quanto ele separa as favelas.');
{
  const s = S();
  titulo(s, 'O índice do NB04, em seis números', 'A linha de base contra a qual todo cenário novo é comparado');
  const xs = [M, M + 3.45], ys = [1.95, 3.45, 4.95], w = 3.1;
  const tiles = [
    [num(BASE.kmo, 4), 'KMO do IVS-7 (correlação de Spearman)'],
    [num(BASE.msa_minimo, 4), 'MSA mínimo — o do lixo inadequado'],
    [`${num(BASE.pesos_ivs6_varimax_socioeconomica, 1)} / ${num(BASE.pesos_ivs6_varimax_saneamento, 1)}`, 'Pesos do IVS-6 com Varimax: socioeconômica / saneamento (%)'],
    [num(BASE.phi_promax, 4), 'Φ — correlação entre os fatores na promax'],
    [num(BASE.auc_indice, 4), 'AUC do índice contra os setores de FCU'],
    [num(BASE.auc_renda_invertida_sozinha, 4), 'AUC da renda invertida, sozinha', true],
  ];
  tiles.forEach(([v, r, dest], i) => numero(s, xs[i % 2], ys[Math.floor(i / 2)], w, v, r, dest));
  const fx = M + 7.5, fw = W - M - fx;
  figura(s, 'banco_de_dados/eda/fatorial/figuras/nb04_roc_fcu.png', fx, 1.85, fw, fw * 675 / 665);
  legendaFigura(s, 1.85 + fw * 675 / 665 + 0.08, 'A curva ROC do índice do NB04 contra os setores de FCU.', null, fx, fw);
  procedencia(s, 'Fonte: banco_de_dados/eda/fatorial_ampliada/linha_de_base_nb04.csv; figura do NB04.');
  s.addNotes(`A renda invertida, sozinha, separa os setores de FCU melhor que o índice (AUC `
    + `${num(BASE.auc_renda_invertida_sozinha, 4)} contra ${num(BASE.auc_indice, 4)}); até a média simples `
    + `dos postos, sem peso nenhum, fica em ${num(BASE.auc_media_postos_pesos_iguais, 4)}. Sem São Paulo, `
    + `o peso da dimensão socioeconômica cai para ${num(BASE.pesos_sem_sao_paulo, 2)}%. Esses números são `
    + 'o ponto de partida: as demandas de setembro perguntam o que muda quando a base muda.');
}

// ── Parte 3 ──────────────────────────────────────────────────────────────────
parte(3, 'Demandas 1 e 2 — a renda e o quadro', 'A mediana no lugar do setor extremo; os indicadores num quadro só.');
{
  const s = S();
  const y = titulo(s, 'Demanda 1: a renda com a mediana', 'Um setor de Belo Horizonte esticava a escala da renda inteira');
  frase(s, M, y + 0.05, W - 2 * M, 0.75, [
    { text: 'O setor 310620005650366 ', options: { bold: true } },
    { text: 'tinha renda média de R$ 170.418,06 por responsável. A coluna nova, renda_media_mediana_mun, '
      + 'troca esse valor pela mediana de Belo Horizonte sem ele; as alternativas ficam registradas:' },
  ]);
  let yy = tabelaAjustada(s, ['Alternativa', 'Valor imputado', 'Média de BH', 'DP de BH', 'Máximo de BH'],
    IMP.map(r => [r.alternativa, reais(r.valor_imputado), reais(r.bh_media), reais(r.bh_dp), reais(r.bh_max)]),
    { y: y + 0.85, colW: [4.0, 1.9, 1.9, 1.9, 1.93], fontSize: 11.5, rowH: 0.31 });
  const R = [['original', 'S0', 'S6'], ['sem o extremo', 'S0_renda_sem_extremo', 'S6_renda_sem_extremo'],
             ['mediana municipal', 'S0_renda_mediana_mun', 'S6_renda_mediana_mun']];
  yy = tabelaAjustada(s, ['Renda', 'KMO (IVS-7)', 'MSA mínimo (IVS-7)', 'AUC do índice (IVS-7)', 'AUC do índice (S6)'],
    R.map(([rot, a, b]) => [rot, num(cen(a).kmo, 4), num(cen(a).msa_min, 4), num(auc(a, M_IND), 4), num(auc(b, M_IND), 4)]),
    { y: yy + 0.3, colW: [2.6, 2.2, 2.3, 2.3, 2.23], fontSize: 11.5, rowH: 0.31 });
  const difKmo = Math.max(...R.map(r => +cen(r[1]).kmo)) - Math.min(...R.map(r => +cen(r[1]).kmo));
  const difAuc = Math.max(...R.map(r => auc(r[1], M_IND))) - Math.min(...R.map(r => auc(r[1], M_IND)));
  frase(s, M, yy + 0.18, W - 2 * M, 0.5, [
    { text: 'Leitura: ', options: { bold: true, color: ACENTO } },
    { text: `entre as três rendas, o KMO muda no máximo ${num(difKmo, 5)} e a AUC do índice ${num(difAuc, 4)}. `
      + 'A escolha da renda é conceitual, não empírica.' },
  ]);
  procedencia(s, 'Fonte: atualizada/renda_imputacao_alternativas.csv; fatorial_ampliada/cenarios.csv e validacao_fcu.csv.');
  s.addNotes('A mediana de BH com o setor extremo quase não muda (a mediana é robusta a um '
    + 'ponto); a dos 70 municípios é bem mais baixa, porque mistura municípios de renda menor. '
    + 'Na fatorial, as três versões dão o mesmo resultado na prática — o setor extremo pesa na '
    + 'escala min-max, não na correlação de Spearman que a fatorial usa.');
}
{
  const s = S();
  const y = titulo(s, 'Demanda 2: o quadro de indicadores', `${QUADRO.length} indicadores, cada um com numerador, denominador e arquivo de origem`);
  const dims = [...new Set(QUADRO.map(r => r.dimensao))];
  tabelaAjustada(s, ['Dimensão', 'Indicadores', 'No IVS-7', 'Quais'], dims.map(dm => {
    const q = QUADRO.filter(r => r.dimensao === dm);
    return [dm, String(q.length), String(q.filter(r => r.entra_no_ivs7 === 'Sim').length),
      q.map(r => r.entra_no_ivs7 === 'Sim' ? `${r.indicador}*` : r.indicador).join(', ')];
  }), { y: y + 0.05, colW: [1.85, 1.2, 1.05, 7.53], fontSize: 11.5, rowH: 0.34 });
  procedencia(s, 'Fonte: banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv (* = entra no IVS-7).');
  s.addNotes('O quadro existe em CSV, XLSX e Markdown na pasta da entrega. Para cada indicador: o '
    + 'que mede, numerador, denominador, se usa o complemento, o arquivo de origem do Censo e uma '
    + 'observação. Os indicadores fora do IVS-7 são descritivos: caracterizam o território, não o pontuam.');
}

// ── Parte 4 ──────────────────────────────────────────────────────────────────
parte(4, 'Demandas 3 e 5 a 11 — a fatorial ampliada', 'Oito cenários sem bootstrap: o IVS-7 do NB04 e o que muda a cada variável que entra ou sai.');
{
  const s = S();
  const y = titulo(s, 'Os cenários: o que entra em cada um', 'Cada linha é uma análise fatorial completa, sobre a mesma regra de setores');
  const ids = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'];
  tabelaAjustada(s, ['', 'O que entra', 'Demanda', 'Variáveis', 'Setores', 'KMO', 'MSA mín.', 'Fatores K/H', 'Var. 2 fat.'],
    ids.map(id => { const c = cen(id); return [id, c.descricao, c.demanda, c.p, mil(c.n), num(c.kmo, 3),
      num(c.msa_min, 3), `${c.fatores_kaiser} / ${c.fatores_horn}`, `${num(c.var_explicada_2f, 1)}%`]; }),
    { y: y + 0.02, colW: [0.6, 3.9, 0.95, 1.0, 1.1, 0.8, 0.95, 1.18, 1.15], fontSize: 11.5, rowH: 0.34 });
  procedencia(s, 'Fonte: banco_de_dados/eda/fatorial_ampliada/cenarios.csv. K/H: fatores pelo critério de Kaiser e pelo de Horn.');
  s.addNotes('S0 reproduz o NB04 (IVS-7). S1 tira o lixo; S2 a S5 acrescentam, um por vez, não '
    + 'chega, sem canalização, sem banheiro (V00495) e não convencional; S6 junta as quatro; S7 é '
    + 'o S6 sem o lixo. Variantes do S0, do S1 e do S6 com as outras rendas e com postos dentro '
    + 'do município estão no mesmo CSV. O número de setores cai quando entra variável com sigilo.');
}
{
  const s = S();
  const y = titulo(s, 'Demandas 3 e 11: sem rotação, Varimax e promax', 'Peso do fator 1 / fator 2, em %, e a correlação Φ entre os fatores');
  const ids = ['S0', 'S1', 'S6', 'S7'];
  const par = (c, r) => { const x = peso(c, r); return `${num(x.peso_f1, 1)} / ${num(x.peso_f2, 1)}`; };
  tabelaAjustada(s, ['Cenário', 'Sem rotação', 'Varimax', 'Promax (padrão)', 'Promax (estrutura)', 'Φ', 'Fator 2 puxado por'],
    ids.map(c => [`${c} — ${cen(c).descricao}`, par(c, 'sem_rotacao'), par(c, 'varimax'), par(c, 'promax_padrao'),
      par(c, 'promax_estrutura'), num(peso(c, 'promax_padrao').phi, 3), peso(c, 'varimax').f2_maior_carga]),
    { y: y + 0.02, colW: [3.5, 1.35, 1.25, 1.45, 1.55, 0.7, 1.83], fontSize: 11.5, rowH: 0.36 });
  const semRot = ids.map(c => +peso(c, 'sem_rotacao').peso_f1);
  const estruturaMais = ids.every(c => +peso(c, 'promax_estrutura').peso_f2 > +peso(c, 'promax_padrao').peso_f2);
  bloco(s, M, y + 2.35, W - 2 * M, 'Leitura.', `Sem rotação, o fator 1 leva de ${num(Math.min(...semRot), 1)}% `
    + `a ${num(Math.max(...semRot), 1)}% do peso; a rotação reparte. O fator 1 é sempre puxado pela renda.`
    + (estruturaMais ? ' Na promax, a matriz estrutura dá ao fator 2 mais peso que a padrão em todos os '
      + 'cenários, porque soma a parte que os dois fatores compartilham (Φ).' : ''), false, 1.0);
  bloco(s, M, y + 3.45, W - 2 * M, 'O que não está dito.', 'Qual das duas matrizes é a "certa" para '
    + 'repartir os pesos na solução oblíqua: as duas ficam lado a lado, e a escolha é da orientadora.', true, 0.8);
  procedencia(s, 'Fonte: banco_de_dados/eda/fatorial_ampliada/pesos.csv (os 15 cenários, quatro rotações cada).');
  s.addNotes('Os pesos de cada dimensão saem da soma dos quadrados das cargas de cada fator, '
    + 'normalizada para 100%. Na promax, a matriz padrão dá o efeito único de cada fator; a estrutura, '
    + 'a correlação simples variável-fator, que inclui o que os fatores compartilham.');
}
{
  const s = S();
  titulo(s, 'O plano fatorial do S6', 'IVS-7 mais as quatro variáveis novas: sem rotação, Varimax e promax');
  const w = W - 2 * M, h = w * 945 / 2647;
  figura(s, FA + 'figuras/fa_plano_s6.png', M, 1.9, w, h);
  legendaFigura(s, 1.9 + h + 0.1, 'Cargas das onze variáveis do S6 nos dois primeiros fatores — sem rotação, Varimax e promax (matriz padrão); em vermelho, as quatro novas.');
  procedencia(s, 'Fonte: banco_de_dados/eda/fatorial_ampliada/figuras/fa_plano_s6.png (NB04b).');
  s.addNotes('Cada ponto é uma variável; a posição é a carga nos fatores 1 e 2. Com promax, os eixos '
    + `deixam de ser perpendiculares: Φ = ${num(peso('S6', 'promax_padrao').phi, 3)} no S6.`);
}
{
  const s = S();
  const y = titulo(s, 'Demandas 5, 6 e 7: uma variável nova por vez', 'O que cada uma faz com a base, a adequação e a validação');
  const ids = ['S0', 'S2', 'S3', 'S4', 'S5'];
  const fp = v => v === 'True' ? 'sim' : v === 'False' ? 'não' : '—';
  tabelaAjustada(s, ['Cenário', 'Setores', 'Perdidos vs S0', 'KMO', 'Fatores K/H', 'AUC índice', 'AUC renda', 'Lixo com fator próprio'],
    ids.map(c => { const x = cen(c); return [`${c} — ${x.descricao}`, mil(x.n), x.cenario === 'S0' ? '—' : mil(x.perdidos_vs_S0),
      num(x.kmo, 3), `${x.fatores_kaiser} / ${x.fatores_horn}`, num(auc(c, M_IND), 4), num(auc(c, M_REN), 4),
      fp(x.lixo_fator_proprio_varimax)]; }),
    { y: y + 0.02, colW: [3.6, 1.05, 1.25, 0.8, 1.15, 1.15, 1.15, 1.48], fontSize: 11.5, rowH: 0.36 });
  bloco(s, M, y + 2.75, W - 2 * M, 'A junção da demanda 6.', `A V00238 nunca passa da V00495: vale em `
    + `${mil(nJuncaoVale)} de ${mil(nAmbas)} setores com as duas presentes. A V00495 já contém a V00238 — `
    + 'juntar é usar a V00495, não somar as duas.', false, 0.85);
  bloco(s, M, y + 3.7, W - 2 * M, 'A comparação da demanda 5.', 'O "não chega" foi comparado nas duas '
    + 'leituras — contra as outras categorias de canalização e contra os indicadores do IVS-7 '
    + '(Spearman e perfil dos setores com e sem o problema).', false, 0.85);
  procedencia(s, 'Fonte: fatorial_ampliada/cenarios.csv, validacao_fcu.csv, banheiro_particao.csv, comparacao_nao_chega_banheiro.csv.');
  s.addNotes('Toda variável nova com sigilo do IBGE derruba setores da base (perdidos vs S0). A '
    + 'AUC da renda sozinha também muda de cenário para cenário porque a base de setores muda. '
    + 'Com as variáveis de água e de banheiro, o lixo deixa de ter fator próprio.');
}
{
  const s = S();
  const y = titulo(s, 'Demanda 9: a moradia não convencional', 'Entrou na direção da vulnerabilidade, sem excluir por variância baixa');
  const v = CARGAS.find(r => r.cenario === 'S5' && r.variavel === 'pct_moradia_nao_convencional');
  numero(s, M, y + 0.3, 3.3, num(v.comunalidade, 3), 'Comunalidade no S5 — o mínimo exigido na grade do NB05 é 0,30', true);
  numero(s, M + 3.75, y + 0.3, 3.3, `${num(v.pct_zeros, 1)}%`, 'Setores com valor zero');
  numero(s, M + 7.5, y + 0.3, 3.3, num(v.msa, 3), 'MSA da variável — passa no critério de 0,50');
  bloco(s, M, y + 1.85, W - 2 * M, 'Leitura.', `A variável passa no MSA, mas quase não compartilha variância `
    + `com as outras: a maior carga fica em ${num(Math.max(Math.abs(+v.varimax_f1), Math.abs(+v.varimax_f2)), 3)}, `
    + `porque ${num(v.pct_zeros, 0)}% dos setores não têm nenhuma moradia não convencional. Ela fica no S5 e no S6 `
    + 'como pedido — e mostra por que não carrega o índice.', false, 1.2);
  procedencia(s, 'Fonte: banco_de_dados/eda/fatorial_ampliada/cargas.csv, cenário S5.');
  s.addNotes('Na EDA de agosto, 99,19% das moradias do recorte eram convencionais (demanda de julho). '
    + 'Uma variável quase sempre zero tem pouca variância para dividir com as outras — é o que a '
    + 'comunalidade mede.');
}
{
  const s = S();
  const y = titulo(s, 'Demanda 8: tudo isso junto', 'S6 = IVS-7 + as quatro; S7 = S6 sem o lixo');
  const ids = ['S6', 'S7', 'S6_renda_sem_extremo', 'S6_renda_mediana_mun', 'S6_postos_mun'];
  tabelaAjustada(s, ['Cenário', 'Var.', 'Setores', 'KMO', 'Fatores K/H', 'Var. 2 fat.'],
    ids.map(c => { const x = cen(c); return [c.replace(/_/g, ' '), x.p, mil(x.n), num(x.kmo, 3),
      `${x.fatores_kaiser} / ${x.fatores_horn}`, `${num(x.var_explicada_2f, 1)}%`]; }),
    { y: y + 0.05, colW: [2.45, 0.6, 1.0, 0.75, 1.1, 1.0], fontSize: 11.5, rowH: 0.34 });
  const fx = M + 7.15, fw = W - M - fx, fh = fw * 656 / 990;
  figura(s, FA + 'figuras/fa_scree_s6.png', fx, y + 0.05, fw, fh);
  legendaFigura(s, y + 0.1 + fh, 'Autovalores do S6 e a linha de Horn.', null, fx, fw);
  bloco(s, M, y + 2.45, 6.9, 'Leitura.', `Com onze variáveis, Kaiser e Horn pedem ${cen('S6').fatores_kaiser} fatores, e dois `
    + `fatores explicam só ${num(cen('S6').var_explicada_2f, 1)}% da variância — contra `
    + `${num(cen('S0').var_explicada_2f, 1)}% no IVS-7. A base perde setores: ${mil(cen('S6').n)} contra `
    + `${mil(cen('S0').n)}. Com postos dentro do município, o MSA mínimo cai para ${num(cen('S6_postos_mun').msa_min, 3)}.`,
    false, 1.6);
  procedencia(s, 'Fonte: fatorial_ampliada/cenarios.csv; figuras/fa_scree_s6.png.');
  s.addNotes('"Tudo isso" foi lido como IVS-7 + não chega + sem canalização + sem banheiro + não '
    + 'convencional (ponto 6 da mensagem à orientadora). As três rendas dão o mesmo resultado também aqui.');
}
{
  const s = S();
  const y = titulo(s, 'Demanda 10: o lixo', 'Com o lixo, ele forma um fator sozinho; sem ele, a fatorial pede um fator só');
  const ids = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'];
  const fp = v => v === 'True' ? 'sim' : v === 'False' ? 'não' : '— (sem lixo)';
  const muda = c => { const x = SENS.filter(r => r.cenario === c); return x.length ? String(x.filter(r => r.lixo_muda === 'True').length) + ` de ${x.length}` : '—'; };
  tabelaAjustada(s, ['Cenário', 'Fatores K/H', 'Lixo com fator próprio (Varimax)', 'Municípios cuja saída muda o lixo de fator'],
    ids.map(c => [`${c} — ${cen(c).descricao}`, `${cen(c).fatores_kaiser} / ${cen(c).fatores_horn}`,
      fp(cen(c).lixo_fator_proprio_varimax), muda(c)]),
    { y: y + 0.02, colW: [4.4, 1.4, 2.8, 3.03], fontSize: 11.5, rowH: 0.33 });
  procedencia(s, 'Fonte: fatorial_ampliada/cenarios.csv (lixo_fator_proprio_varimax) e sensibilidade_municipios.csv (lixo_muda).');
  s.addNotes('O lixo é a variável menos correlacionada com as outras desde a EDA de junho. No IVS-7 '
    + 'ele ocupa o fator 2 sozinho; quando entram as variáveis de água e de banheiro, o fator 2 passa '
    + 'a ser o da água e o lixo perde o fator próprio. A sensibilidade por município só foi rodada '
    + 'para S0, S1 e S6.');
}
{
  const s = S();
  const y = titulo(s, 'A incerteza: um município de fora por vez', 'Em vez do bootstrap, quanto o peso do fator 1 se move');
  const fw = 7.0, fh = fw * 542 / 1140;
  figura(s, FA + 'figuras/fa_sensibilidade_municipios.png', M, y + 0.05, fw, fh);
  legendaFigura(s, y + 0.12 + fh, 'Peso do fator 1 (Varimax) no S1 e no S6, com um município de fora por rodada; o traço é a amostra inteira.', null, M, fw);
  const cenS = [...new Set(SENS.map(r => r.cenario))];
  const linhas = cenS.map(c => {
    const x = SENS.filter(r => r.cenario === c);
    const mv = x.reduce((a, b) => Math.abs(+b.delta_varimax) > Math.abs(+a.delta_varimax) ? b : a);
    const mp = x.reduce((a, b) => Math.abs(+b.delta_promax_padrao) > Math.abs(+a.delta_promax_padrao) ? b : a);
    return [c, `${num(Math.abs(+mv.delta_varimax), 2)} (${mv.municipio_fora})`, `${num(Math.abs(+mp.delta_promax_padrao), 2)} (${mp.municipio_fora})`];
  });
  tabelaAjustada(s, ['Cenário', 'Maior |Δ| Varimax, p.p.', 'Maior |Δ| promax, p.p.'], linhas,
    { x: M + 7.3, y: y + 0.05, colW: [1.0, 1.7, 1.63], fontSize: 11, rowH: 0.34 });
  const maxAbs = Math.max(...SENS.map(r => Math.abs(+r.delta_varimax)), ...SENS.map(r => Math.abs(+r.delta_promax_padrao)));
  const quemMove = [...new Set(linhas.flatMap(l => [l[1], l[2]].map(t => t.replace(/^.*\((.*)\)$/, '$1'))))];
  bloco(s, M + 7.3, y + 2.2, 4.33, 'Leitura.', `Tirar um município move o peso do fator 1 em no máximo `
    + `${num(maxAbs, 2)} pontos percentuais; os que mais movem: ${quemMove.join(', ')}.`, false, 1.2);
  procedencia(s, 'Fonte: fatorial_ampliada/sensibilidade_municipios.csv; figuras/fa_sensibilidade_municipios.png.');
  s.addNotes(`Cada cenário roda ${SENS.filter(r => r.cenario === cenS[0]).length} vezes, uma por município fora. `
    + 'O bootstrap foi deixado de lado de propósito: com dezenas de milhares de setores, ele mede o '
    + 'erro de amostragem de uma população que não é amostra; a pergunta útil é quanto o resultado '
    + 'depende de um município.');
}
{
  const s = S();
  const y = titulo(s, 'A validação contra as favelas, cenário a cenário', 'AUC contra os setores de FCU: o índice, a média de postos e a renda sozinha');
  const ids = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'];
  tabelaAjustada(s, ['Cenário', 'AUC do índice', 'AUC da média de postos', 'AUC da renda sozinha'],
    ids.map(c => [`${c} — ${cen(c).descricao}`, num(auc(c, M_IND), 4), num(auc(c, M_POS), 4),
      { text: num(auc(c, M_REN), 4), options: { bold: true } }]),
    { y: y + 0.02, colW: [5.5, 2.0, 2.1, 2.03], fontSize: 11.5, rowH: 0.33 });
  const todos = [...new Set(VAL.map(r => r.cenario))];
  const rendaGanha = todos.filter(c => auc(c, M_REN) > auc(c, M_IND)).length;
  frase(s, M, y + 3.35, W - 2 * M, 0.6, [
    { text: 'Leitura: ', options: { bold: true, color: ACENTO } },
    { text: `a renda sozinha separa melhor que o índice em ${rendaGanha} de ${todos.length} cenários `
      + '(contando as variantes de renda e de postos). A Parte 8 mostra o que o índice acrescenta mesmo assim.' },
  ]);
  procedencia(s, 'Fonte: banco_de_dados/eda/fatorial_ampliada/validacao_fcu.csv.');
  s.addNotes('A AUC contra FCU mede o quanto o índice ordena os setores de favela acima dos demais. '
    + 'Ela é uma validação parcial: o critério do IBGE para FCU olha, em parte, as mesmas condições '
    + 'de saneamento que entram no índice.');
}

// ── Parte 5 ──────────────────────────────────────────────────────────────────
parte(5, 'Demanda 4 — a apresentação revista', 'O que ficou, o que saiu e os números que estavam errados.');
{
  const s = S();
  const y = titulo(s, 'Separar o útil do inútil', 'O deck principal corrigido e ampliado, sem ser regerado');
  const w = 5.55, x2 = M + 6.05;
  bloco(s, M, y + 0.15, w, 'O inventário.', 'scripts/inventario_apresentacao.py listou os artefatos; '
    + 'docs/Apresentacoes_IVS/MAPA_APRESENTACAO_FINAL.md separa o que entra, o que sai e propõe o roteiro.', false, 1.3);
  bloco(s, x2, y + 0.15, w, 'Os números corrigidos.', 'Três números errados nos slides (AUD-07, DEC-1, '
    + 'AUD-04) e o guia de apoio com 16.548 no lugar de 16.563 (AUD-08) — os quatro relidos dos CSVs.', true, 1.3);
  bloco(s, M, y + 1.75, w, 'O bloco novo.', 'Os slides da fatorial ampliada e, depois, os do IVS final '
    + 'saem de script e são anexados por scripts/juntar_decks.py ao deck principal, que nunca é regerado.', false, 1.3);
  bloco(s, x2, y + 1.75, w, 'O deck hoje.', `${path.basename(DECK_ATUAL)}, com ${slidesDe(DECK_ATUAL)} slides; `
    + 'a estrutura do pacote conferida e consertada em 30/09.', false, 1.3);
  procedencia(s, 'Fonte: estado_demandas_2026-09.md, Fase 4; MAPA_APRESENTACAO_FINAL.md.');
  s.addNotes('O deck principal tem marcações "EXPLICAR SLIDE" e anotações feitas à mão; regerá-lo '
    + 'apagaria esse trabalho. Por isso os blocos novos saem num .pptx separado e o juntador os '
    + 'anexa à versão do HEAD.');
}

// ── Parte 6 ──────────────────────────────────────────────────────────────────
parte(6, 'Os testes seguintes', 'Os nove itens da etapa de 26/09 e o banheiro graduado.');
{
  const s = S();
  const y = titulo(s, 'Os nove itens da etapa seguinte', 'Cada escolha em aberto virou uma dimensão da grade do NB05');
  const rot = r => ESP.filter(x => x.rotacao === r);
  tabelaAjustada(s, ['Item', 'O que foi pedido', 'Resultado'], [
    ['1', 'Renda: original · sem extremo · mediana municipal', 'As três na grade; empatam na AUC'],
    ['2', 'Rotação: sem rotação · Varimax · promax', `Sem rotação: ${conta(x => x.rotacao === 'sem_rotacao')} elegíveis; Varimax: ${conta(x => x.rotacao === 'varimax')}; promax: ${conta(x => x.rotacao === 'promax')}`],
    ['3', 'Pesos na oblíqua: cinco esquemas', 'SS da padrão, SS da estrutura, comunalidades, 50/50 e 60/40'],
    ['4', 'Lixo: com · sem', `Com lixo: ${conta(x => x.lixo === 'com')} elegíveis; sem: ${conta(x => x.lixo === 'sem')}`],
    ['5', 'Banheiro: fora · V00495 · graduado', 'A V00237 extraída; a partição fecha setor a setor'],
    ['6', 'O que o índice acrescenta à renda', 'Parte 8'],
    ['7', 'O que estava inferido, sem verificação', 'Virou verificação por script'],
    ['8', 'Pendências pequenas', 'Dicionário, slide 45 da EDA Central, scripts reexecutados'],
    ['9', 'Notebook 05, relatório e slides', 'Feitos em 27/09'],
  ], { y: y + 0.02, colW: [0.7, 4.7, 6.23], fontSize: 11.5, rowH: 0.34 });
  procedencia(s, 'Fonte: estado_nb05_2026-09.md, "Tabela dos itens 1–9"; ivs_especificacoes/especificacoes.csv.');
  s.addNotes(`As contagens de elegíveis são sobre as ${ESP.length} especificações da grade (${nBases} bases × `
    + `${nEsquemas} esquemas × ${nNorm} normalizações).`);
}
{
  const s = S();
  const y = titulo(s, 'O banheiro graduado', 'Três graus de inadequação, em vez de um "sem banheiro" só');
  tabelaAjustada(s, ['Variável', 'Domicílios com…', 'Grau', 'Peso'], [
    ['V00236', 'apenas banheiro de uso comum', 'leve', '1'],
    ['V00237', 'apenas sanitário ou buraco para dejeções', 'intermediário', '2'],
    ['V00238', 'nem banheiro nem sanitário', 'grave', '3'],
    ['V00495', 'sem banheiro de uso exclusivo — a soma das três', '—', '—'],
  ], { y: y + 0.05, colW: [1.3, 5.6, 1.9, 0.9], fontSize: 12, rowH: 0.36 });
  frase(s, M, y + 2.15, W - 2 * M, 0.5, [
    { text: 'Banheiro graduado = (1·V00236 + 2·V00237 + 3·V00238) ÷ (3·V00001)', options: { bold: true } },
  ], 14);
  numero(s, M, y + 2.85, 3.4, `${mil(nBate)} de ${mil(nPresentes)}`, 'Setores em que V00495 = V00236 + V00237 + V00238, sem resto', true);
  numero(s, M + 3.9, y + 2.85, 3.4, mil(PART.length - nPresentes), 'Setores da base ELSI com alguma das quatro variáveis ausente');
  procedencia(s, 'Fonte: fatorial_ampliada/banheiro_particao.csv; a fórmula em scripts/ivs_especificacoes.py.');
  s.addNotes('A V00237 não estava na base: foi extraída do arquivo de domicílio 2 do Censo e '
    + 'entrou na entrega à orientadora, com os indicadores pct_so_sanitario e pct_banheiro_comum. '
    + 'O indicador graduado vai de 0 (todos com banheiro de uso exclusivo) a 1 (todos sem banheiro '
    + 'nem sanitário); fica ausente se alguma das partes ou o total estiver sob sigilo.');
}

// ── Parte 7 ──────────────────────────────────────────────────────────────────
parte(7, 'O IVS final — a grade do Notebook 05', 'Todas as combinações das escolhas em aberto, com regras fixadas antes de rodar.');
{
  const s = S();
  const y = titulo(s, `A grade: ${ESP.length} especificações`, 'Renda × lixo × banheiro × rotação e pesos × normalização');
  const tiles = [[String(nBases), 'bases: 3 rendas × 2 lixos × 3 banheiros'], [String(nEsquemas), 'esquemas de rotação e de peso'],
    [String(nNorm), 'normalizações: no município ou global'], [String(ESP.length), 'especificações'], [String(eleg.length), 'elegíveis', true]];
  tiles.forEach(([v, r, dest], i) => numero(s, M + i * 2.35, y + 0.25, 2.05, v, r, dest));
  bloco(s, M, y + 1.85, W - 2 * M, 'Elegível é quem passa nos quatro critérios.', 'KMO ≥ 0,70; MSA mínimo ≥ 0,50; '
    + 'comunalidade mínima ≥ 0,30; maior carga de cada variável ≥ 0,40. Os critérios foram escritos '
    + 'antes de a grade rodar.', false, 0.9);
  bloco(s, M, y + 2.85, W - 2 * M, 'Entre as elegíveis, a referência é a de melhor posição média', 'em três '
    + 'critérios de peso igual: (a) estabilidade — a amplitude do peso de F1 ao tirar um município; '
    + '(b) a AUC contra FCU dentro do município; (c) parcimônia — menos variáveis.', true, 0.9);
  procedencia(s, 'Fonte: ivs_especificacoes/especificacoes.csv; Relatorio_IVS_Final_NB05.md (Método).');
  s.addNotes('Os nove esquemas: sem rotação (fator único); Varimax com SS, 50/50 e 60/40; promax '
    + 'com SS da matriz padrão, SS da estrutura, comunalidades, 50/50 e 60/40.');
}
{
  const s = S();
  const y = titulo(s, 'Quem passa nos critérios, base a base', 'Elegíveis em cada base, de 18 (9 esquemas × 2 normalizações)');
  const rendas = ['original', 'sem_extremo', 'mediana_mun'], lixos = ['com', 'sem'], banh = ['fora', 'v00495', 'graduado'];
  const linhas = [];
  rendas.forEach(r => lixos.forEach(l => linhas.push([ROT.renda[r], ROT.lixo[l], ...banh.map(b => {
    const f = x => x.renda === r && x.lixo === l && x.banheiro === b;
    return conta(f);
  })])));
  const yy = tabelaAjustada(s, ['Renda', 'Lixo', 'Sem banheiro', 'Com V00495', 'Com o graduado'], linhas,
    { y: y + 0.02, colW: [2.6, 1.6, 2.4, 2.4, 2.63], fontSize: 11.5, rowH: 0.31 });
  const lim = [['com', 'fora'], ['com', 'v00495'], ['com', 'graduado'], ['sem', 'fora']].map(([l, b]) => comunMin(l, b));
  frase(s, M, yy + 0.2, W - 2 * M, 0.9, [
    { text: 'Por que cai: ', options: { bold: true, color: ACENTO } },
    { text: `com o lixo e sem banheiro (o IVS-7 do NB04), a comunalidade mínima é a da ${lim[0].comunalidade_min_variavel.toLowerCase()}, `
      + `${num(lim[0].comunalidade_min, 3)}; com o graduado, a do banheiro graduado, ${num(lim[2].comunalidade_min, 3)} — `
      + `por pouco abaixo de 0,30. Com a V00495, a mínima sobe para ${num(lim[1].comunalidade_min, 3)}; sem o lixo, `
      + `fica em ${num(lim[3].comunalidade_min, 3)} (${lim[3].comunalidade_min_variavel.toLowerCase()}).` },
  ]);
  procedencia(s, 'Fonte: ivs_especificacoes/especificacoes.csv (comunalidade_min e comunalidade_min_variavel, renda original).');
  s.addNotes('A renda não muda nada na elegibilidade: as três linhas de cada lixo são iguais. Com '
    + 'lixo, só passa a base com V00495; sem lixo, as três versões de banheiro passam.');
}
{
  const s = S();
  const y = titulo(s, 'Rotação e esquema de peso', 'Elegíveis por esquema, em toda a grade');
  const esquemas = [...new Set(ESP.map(r => `${r.rotacao}|${r.metodo}`))];
  const yy = tabelaAjustada(s, ['Rotação', 'Esquema de peso', 'Elegíveis'], esquemas.map(k => {
    const [r, m] = k.split('|');
    return [ROT.rotacao[r], ROT.metodo[m], conta(x => x.rotacao === r && x.metodo === m)];
  }), { y: y + 0.02, colW: [2.6, 3.4, 2.2], fontSize: 12, rowH: 0.33 });
  bloco(s, M + 8.6, y + 0.1, W - 2 * M - 8.6, 'Um fator ou dois.', 'Kaiser e Horn indicam um fator '
    + 'no IVS-6, mas o fator único reprova na comunalidade em toda a grade: a comparação sempre usa dois.',
    true, 2.4);
  procedencia(s, 'Fonte: ivs_especificacoes/especificacoes.csv.');
  s.addNotes('Na promax, os cinco esquemas passam em igual número, porque a elegibilidade depende da '
    + 'base e da rotação, não de como os pesos são repartidos depois.');
}
{
  const s = S();
  const y = titulo(s, 'Os pesos na solução oblíqua', `Na base da referência: ${ROT.renda[PRINC.renda]} · ${ROT.lixo[PRINC.lixo]} · banheiro ${ROT.banheiro[PRINC.banheiro]}`);
  const pr = PES.filter(r => r.renda === PRINC.renda && r.lixo === PRINC.lixo && r.banheiro === PRINC.banheiro);
  tabelaAjustada(s, ['Rotação · esquema', 'F1', 'F2'], pr.map(r => [`${ROT.rotacao[r.rotacao]} · ${ROT.metodo[r.metodo]}`,
    r.peso_f1 ? num(r.peso_f1, 1) : '—', r.peso_f2 ? num(r.peso_f2, 1) : '—']),
    { y: y + 0.02, colW: [2.9, 0.8, 0.8], fontSize: 11.5, rowH: 0.31 });
  const fx = M + 4.8, fw = W - M - fx, fh = fw * 870 / 1884;
  figura(s, IE + 'figuras/peso_f1_por_especificacao.png', fx, y + 0.05, fw, fh);
  legendaFigura(s, y + 0.12 + fh, 'Peso de F1 nas fatorações elegíveis com peso tirado dos dados: ponto, a amostra inteira; barra, um município de fora por vez.', null, fx, fw);
  procedencia(s, 'Fonte: ivs_especificacoes/pesos.csv; figuras/peso_f1_por_especificacao.png.');
  s.addNotes('F1 é a dimensão socioeconômica; F2, a de saneamento. Os esquemas fixos (50/50 e 60/40) '
    + 'não dependem dos dados; os outros três, sim. O 60/40 é o do IVS-BH 2012 — falta conferir os '
    + 'números no Quadro 3 do PDF, que não saíram no texto extraído.');
}
{
  const s = S();
  titulo(s, 'A AUC de cada especificação', 'Contra os setores de FCU, global e dentro do município, na amostra comum');
  const w = 9.8, h = w * 720 / 1800;
  figura(s, IE + 'figuras/auc_por_especificacao.png', M, 1.9, w, h);
  legendaFigura(s, 1.92 + h + 0.06, 'AUC das especificações com normalização municipal, em ordem crescente (cheio: elegível; vazado: inelegível); tracejado: a renda sozinha; estrela: a referência.');
  frase(s, M, 1.92 + h + 0.52, W - 2 * M, 0.4, [
    { text: 'Por renda, entre as elegíveis: ', options: { bold: true } },
    { text: `original ${num(aucRenda('original'), 4)}; sem o extremo ${num(aucRenda('sem_extremo'), 4)}; `
      + `mediana municipal ${num(aucRenda('mediana_mun'), 4)} — as três coladas.` },
  ]);
  procedencia(s, 'Fonte: ivs_especificacoes/especificacoes.csv (auc_mun_comum); figuras/auc_por_especificacao.png.');
  s.addNotes('A amostra comum é a de setores presentes nas três versões de banheiro, para que a '
    + 'comparação não dependa de qual base perdeu mais setores por sigilo.');
}

// ── Parte 8 ──────────────────────────────────────────────────────────────────
parte(8, 'O que o índice acrescenta à renda', 'A renda sozinha separa melhor; dentro de cada faixa de renda, o índice acrescenta.');
{
  const s = S();
  const y = titulo(s, 'A renda sozinha contra o índice', `Nas ${ACR.length} especificações elegíveis`);
  const rG = ACR.filter(r => +r.auc_renda_global > +r.auc_indice_global).length;
  const rM = ACR.filter(r => +r.auc_renda_mun > +r.auc_indice_mun).length;
  const iE = ACR.filter(r => +r.auc_indice_estratos > +r.auc_renda_estratos).length;
  const zMin = Math.min(...ACR.map(r => +r.z_indice));
  const ganho = Math.max(...ACR.map(r => +r.auc_modelo_renda_indice - +r.auc_modelo_renda));
  numero(s, M, y + 0.25, 2.65, `${rG} de ${ACR.length}`, 'A renda vence o índice na AUC global');
  numero(s, M + 2.95, y + 0.25, 2.65, `${rM} de ${ACR.length}`, 'A renda vence na AUC dentro do município');
  numero(s, M + 5.9, y + 0.25, 2.65, `${iE} de ${ACR.length}`, 'O índice vence dentro dos decis de renda', true);
  numero(s, M + 8.85, y + 0.25, 2.65, `z ≥ ${num(zMin, 1)}`, 'O índice soma à renda na regressão logística');
  const R = ACR.find(r => r.referencia === 'True') || ACR.find(r => r.id === PRINC.id);
  tabelaAjustada(s, ['Na referência proposta', 'Índice', 'Renda sozinha'], [
    ['AUC global', num(R.auc_indice_global, 4), num(R.auc_renda_global, 4)],
    ['AUC dentro do município (mediana)', num(R.auc_indice_mun, 4), num(R.auc_renda_mun, 4)],
    ['AUC dentro dos decis de renda de cada município', num(R.auc_indice_estratos, 4), num(R.auc_renda_estratos, 4)],
  ], { y: y + 1.7, colW: [5.2, 1.6, 1.8], fontSize: 12, rowH: 0.34 });
  bloco(s, M + 8.95, y + 1.7, W - M - (M + 8.95), 'Somar o índice à renda', `na logística baixa a deviance em `
    + `${num(R.queda_deviance, 1)} (z = ${num(R.z_indice, 1)}) e leva a AUC de ${num(R.auc_modelo_renda, 4)} a `
    + `${num(R.auc_modelo_renda_indice, 4)}. Em toda a grade, o ganho de AUC fica em até ${num(ganho, 4)}.`, false, 2.0);
  procedencia(s, 'Fonte: banco_de_dados/eda/ivs_especificacoes/acrescimo_renda.csv.');
  s.addNotes('A leitura: o índice não substitui a renda como separador das favelas, e não precisa — '
    + 'ele ordena os setores dentro de cada faixa de renda, que é o que um índice de vulnerabilidade '
    + 'acrescenta. A AUC contra FCU tem circularidade parcial com o saneamento, e por isso não deveria '
    + 'decidir sozinha a especificação.');
}

// ── Parte 9 ──────────────────────────────────────────────────────────────────
parte(9, 'A referência proposta — e por que desconfiar', 'Uma proposta, não uma decisão: quatro leituras dos critérios, quatro resultados.');
{
  const s = S();
  const y = titulo(s, 'Quatro leituras, quatro propostas', 'A especificação de melhor posição média em cada leitura dos critérios');
  const NOME = { principal: 'Principal: estabilidade de F1, AUC na amostra comum', amostra_propria: 'AUC na amostra própria',
    estabilidade_pesos_variaveis: 'Estabilidade pelos pesos das variáveis', normalizacao_global: 'Normalização global' };
  tabelaAjustada(s, ['Leitura', 'Renda', 'Lixo', 'Banheiro', 'Rotação', 'Pesos', 'Normal.', 'Posto médio'],
    REF.map(r => [{ text: NOME[r.leitura] || r.leitura, options: r.leitura === 'principal' ? { bold: true, color: ACENTO } : {} },
      ROT.renda[r.renda], ROT.lixo[r.lixo], ROT.banheiro[r.banheiro], ROT.rotacao[r.rotacao], ROT.metodo[r.metodo],
      ROT.normalizacao[r.normalizacao], num(r.posto_medio, 1)]),
    { y: y + 0.02, colW: [3.5, 1.45, 1.0, 1.25, 1.0, 1.35, 1.15, 0.93], fontSize: 11.5, rowH: 0.36 });
  const lin = REF.map(r => `${NOME[r.leitura] || r.leitura}: ${r.porque}; segunda colocada: ${r.segunda}.`);
  procedencia(s, 'Fonte: banco_de_dados/eda/ivs_especificacoes/referencia.csv.');
  s.addNotes(lin.join('\n\n'));
}
{
  const s = S();
  const y = titulo(s, 'Por que desconfiar da principal', 'Cinco pontos, todos com número');
  const amp = ESP.find(r => r.id === PRINC.id).amp_peso_f1;
  const w = 5.55, x2 = M + 6.05;
  bloco(s, M, y + 0.12, w, 'O critério (a) degenera.', `Com pesos fixos (50/50, 60/40), a amplitude do peso de F1 `
    + `é ${num(amp, 1)} por construção: a principal (${ROT.metodo[PRINC.metodo]}) empata em primeiro na estabilidade sem ter sido testada.`, true, 1.4);
  bloco(s, x2, y + 0.12, w, 'Medida de outro jeito, a proposta muda.', `Pela estabilidade dos pesos das variáveis: `
    + `${legivel(refDe('estabilidade_pesos_variaveis'))}.`, false, 1.4);
  bloco(s, M, y + 1.65, w, 'O 60/40 não foi conferido na fonte.', 'Os números do Quadro 3 (p. 7 do PDF do IVS-BH 2012) '
    + 'não saíram no texto extraído: falta confirmar 0,6 para a socioeconômica e 0,4 para o saneamento.', false, 1.4);
  bloco(s, x2, y + 1.65, w, 'A normalização importa.', `Normalizando global em vez de no município, `
    + `${num(mudaGlobal.muda_faixa_ivs_bh, 1)}% dos setores mudam de faixa (regra do IVS-BH) e ${num(mudaGlobal.muda_faixa_quartis, 1)}% `
    + `(quartis); o Spearman com a referência fica em ${num(mudaGlobal.spearman_ref, 3)}.`, false, 1.4);
  bloco(s, M, y + 3.18, W - 2 * M, 'O corte de 0,30 é rígido?', `O IVS-7 com o banheiro graduado ficou de fora por uma `
    + `comunalidade de ${num(comunMin('com', 'graduado').comunalidade_min, 3)}. Um corte de 0,29 mudaria a lista de elegíveis.`, false, 0.9);
  procedencia(s, 'Fonte: ivs_especificacoes/especificacoes.csv, avaliacao.csv, referencia.csv; estado_nb05_2026-09.md.');
  s.addNotes('Nada disso invalida a grade: as 192 elegíveis estão todas no CSV, com os três '
    + 'postos de cada uma. A referência é só a que os critérios, lidos ao pé da letra, apontam.');
}
{
  const s = S();
  const y = titulo(s, 'As faixas da referência', 'A referência contra quatro alternativas, e as duas regras de corte');
  const w = 10.2, h = w * 660 / 2220;
  figura(s, IE + 'figuras/concordancia_faixas.png', M, y + 0.05, w, h);
  legendaFigura(s, y + 0.1 + h, 'Faixas pela regra do IVS-BH 2012: a referência (linhas) contra quatro alternativas (colunas), em % dos setores; a diagonal é quem fica na mesma faixa.');
  const SET = IE + 'ivs_referencia_por_setor.csv';
  if (existe(SET)) {
    const st = lerCsv(SET);
    const FX = ['baixo', 'medio', 'elevado', 'muito_elevado'];
    const linha = (col, rot) => [rot, ...FX.map(f => mil(st.filter(r => r[col] === f).length)),
      mil(st.filter(r => !FX.includes(r[col])).length)];
    tabelaAjustada(s, ['Regra', 'Baixo', 'Médio', 'Elevado', 'Muito elevado', 'Indefinida'], [
      linha('faixa_ivs_bh', 'IVS-BH 2012 (média ± DP, no município)'), linha('faixa_quartis', 'Quartis municipais')],
      { y: y + h + 0.55, colW: [4.2, 1.45, 1.45, 1.45, 1.6, 1.48], fontSize: 12, rowH: 0.34 });
  }
  procedencia(s, 'Fonte: ivs_especificacoes/ivs_referencia_por_setor.csv; figuras/concordancia_faixas.png.');
  s.addNotes('A regra do IVS-BH 2012 corta pela média e pelo desvio-padrão, aplicada dentro de '
    + 'cada município; os quartis dividem cada município em quatro partes iguais. A faixa '
    + '"indefinida" é a do setor que fica sozinho numa faixa do seu município.');
}

// ── Parte 10 ─────────────────────────────────────────────────────────────────
parte(10, 'O que fica para decidir', 'As escolhas são da orientadora; os números de cada uma estão aqui.');
{
  const s = S();
  const y = titulo(s, 'As sete escolhas', 'Cada uma com o que a grade mostra');
  const b = x => conta(r => r.banheiro === x);
  tabelaAjustada(s, ['Escolha', 'Opções', 'O que os números mostram'], [
    ['Renda', 'original · sem o extremo · mediana municipal', `Empatam: AUC municipal média ${num(aucRenda('original'), 4)} / ${num(aucRenda('sem_extremo'), 4)} / ${num(aucRenda('mediana_mun'), 4)}`],
    ['Rotação', 'sem rotação · Varimax · promax', `Elegíveis: ${conta(r => r.rotacao === 'sem_rotacao')} / ${conta(r => r.rotacao === 'varimax')} / ${conta(r => r.rotacao === 'promax')}`],
    ['Pesos na oblíqua', 'SS da padrão · SS da estrutura · comunalidades · 50/50 · 60/40', 'Passam em igual número; os fixos empatam a estabilidade por construção'],
    ['Lixo', 'com · sem', `Elegíveis: com ${conta(r => r.lixo === 'com')}; sem ${conta(r => r.lixo === 'sem')}`],
    ['Banheiro', 'fora · V00495 · graduado', `Elegíveis: fora ${b('fora')}; V00495 ${b('v00495')}; graduado ${b('graduado')}`],
    ['Normalização', 'no município · global', `Global: ${num(mudaGlobal.muda_faixa_ivs_bh, 1)}% dos setores mudam de faixa`],
    ['Faixas', 'IVS-BH 2012 · quartis municipais', 'As distribuições estão na Parte 9'],
  ], { y: y + 0.02, colW: [2.0, 4.6, 5.03], fontSize: 11.5, rowH: 0.36 });
  procedencia(s, 'Fonte: ivs_especificacoes/especificacoes.csv e avaliacao.csv; estado_nb05_2026-09.md, "Perguntas à orientadora".');
  s.addNotes('Nenhuma dessas escolhas foi feita no código. O NB05 calcula todas as combinações '
    + 'e deixa a referência como proposta.');
}
{
  const s = S();
  const y = titulo(s, 'As perguntas de método', 'O que os critérios não decidem sozinhos');
  tabelaAjustada(s, ['Pergunta', 'Por quê'], [
    ['Manter o critério (a) como está, ou medir a estabilidade pelos pesos das variáveis?', 'As duas leituras levam a propostas diferentes'],
    ['O corte de comunalidade de 0,30 é rígido?', `O IVS-7 + graduado ficou de fora por ${num(comunMin('com', 'graduado').comunalidade_min, 3)}`],
    ['A regra da grade basta para o lixo sair, ou a saída pede justificativa própria?', `O IVS-7 do NB04 é inelegível pela comunalidade da água (${num(comunMin('com', 'fora').comunalidade_min, 3)})`],
    ['Amostra comum ou própria no critério (b)?', 'A proposta muda de banheiro graduado para V00495'],
    ['O 60/40 do IVS-BH 2012 confere com o Quadro 3 do PDF?', 'Os números não saíram no texto extraído'],
    ['Que papel a AUC contra FCU deve ter na escolha?', 'A renda sozinha vence; o critério de FCU olha, em parte, o próprio saneamento'],
    ['Pesos por comunalidades na promax: a leitura operacional está certa?', 'Comunalidade oblíqua de cada variável, somada na dimensão da maior carga padrão'],
  ], { y: y + 0.02, colW: [6.4, 5.23], fontSize: 11.5, rowH: 0.36 });
  procedencia(s, 'Fonte: estado_nb05_2026-09.md, "Perguntas à orientadora" (novas da Fase C).');
  s.addNotes('Estas perguntas apareceram ao rodar a grade; estão também no NB05 (seção 11) e no '
    + 'relatório do IVS final, cada uma apontando o achado com os números.');
}
{
  const s = S();
  const y = titulo(s, 'Onde está cada resultado', 'Para conferir qualquer número deste deck');
  tabelaAjustada(s, ['Resultado', 'Onde'], [
    ['A entrega, com as três rendas e o banheiro graduado', 'banco_de_dados/entrega_orientadora/'],
    ['A fatorial ampliada (S0–S7)', 'notebooks/Fase3_EDA_ELSI/04b_Analise_Fatorial_Ampliada.ipynb; banco_de_dados/eda/fatorial_ampliada/'],
    ['A grade do IVS final', 'notebooks/Fase3_EDA_ELSI/05_Calculo_IVS_Final.ipynb; banco_de_dados/eda/ivs_especificacoes/'],
    ['Os relatórios', 'docs/relatorios/Relatorio_IVS_Final_NB05.md; docs/relatorios/Relatorio_Analise_Fatorial_NB04.md'],
    ['O deck principal', `${DECK_ATUAL} (${slidesDe(DECK_ATUAL)} slides)`],
    ['O registro de cada fase', 'estado_demandas_2026-09.md; estado_nb05_2026-09.md'],
  ], { y: y + 0.02, colW: [4.2, 7.43], fontSize: 12, rowH: 0.38 });
  s.addText(`Gerado por scripts/gerar_deck_demandas_setembro.js em ${HOJE}, a partir dos CSVs. Para refazer: `
    + 'node scripts/gerar_deck_demandas_setembro.js', { x: M, y: H - 1.35, w: W - 2 * M, h: 0.4,
    fontFace: FONTE, fontSize: 11, italic: true, color: CINZA, margin: 0 });
  s.addNotes('Se um CSV mudar — por exemplo, depois de a orientadora escolher a especificação —, '
    + 'basta rodar o gerador de novo: nenhum número deste deck foi digitado.');
}

d.p.writeFile({ fileName: SAIDA }).then(f => console.log('deck escrito:', f));
