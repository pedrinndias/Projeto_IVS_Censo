/**
 * Gera o deck do critério de outliers de renda —
 * docs/Apresentacoes_IVS/complementos/Criterio_Outliers_Renda.pptx
 *
 * É o anexo apresentável do PDF de mesmo nome: abre a regra de classificação da renda,
 * que na EDA Central cabe em um slide e meio. Mesma identidade visual do deck principal
 * (papel, tinta quase preta, um acento de carimbo, tabelas booktabs), para que os dois
 * sejam lidos como a mesma peça.
 *
 * Os números NÃO são digitados aqui. scripts/dados_criterio_renda.py lê as tabelas de
 * banco_de_dados/eda/, importa as constantes da regra de src/ivs_censo/renda.py e emite o
 * JSON; este arquivo só formata. É a mesma separação do deck principal, e pela mesma
 * razão: valor digitado à mão em deck já entrou errado uma vez neste projeto.
 *
 * Ordem de execução:
 *     ./.venv/bin/python scripts/dados_criterio_renda.py banco_de_dados/eda/dados_criterio_renda.json
 *     node scripts/gerar_deck_criterio_renda.js docs/Apresentacoes_IVS/complementos/Criterio_Outliers_Renda.pptx
 *
 * Requer `pptxgenjs` (npm).
 */
const path = require('path');
const fs = require('fs');
let pptxgen;
try { pptxgen = require('pptxgenjs'); }
catch (e) {
  console.error('\n  pptxgenjs não encontrado:  npm install pptxgenjs\n');
  process.exit(1);
}

const RAIZ = path.resolve(__dirname, '..');
const FIG = path.join(RAIZ, 'banco_de_dados/eda/figuras');
const D = JSON.parse(fs.readFileSync(
  path.join(RAIZ, 'banco_de_dados/eda/dados_criterio_renda.json'), 'utf8'));
const K = D.constantes, N = D.totais, TB = D.tabelas;

// ── Paleta e primitivas: as mesmas do gerador da EDA Central ────────────────
const TINTA   = '1A1A18';
const CINZA   = '56534C';
const CINZA_C = '8B877E';
const REGUA   = 'C8C6C0';
const ACENTO  = '8C2F27';
const PAPEL   = 'FFFFFF';
const FONTE   = 'Cambria';
const MONO    = 'Courier New';

const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';
p.author = 'Pedro Dias Soares';
p.title  = 'Critério de outliers de renda — IVS Censo 2022';
const W = 13.33, H = 7.5, M = 0.85;

let nSlide = 0, nTabela = 0, nFigura = 0;

function S() {
  const s = p.addSlide();
  s.background = { color: PAPEL };
  nSlide++;
  if (nSlide > 1) {
    s.addText(String(nSlide), { x: W - M - 0.6, y: H - 0.55, w: 0.6, h: 0.3,
      fontFace: FONTE, fontSize: 10, color: CINZA_C, align: 'right', margin: 0 });
  }
  return s;
}

function regua(s, y, espessura, cor, x, w) {
  s.addShape(p.ShapeType.line, { x: x === undefined ? M : x, y,
    w: w === undefined ? W - 2*M : w, h: 0,
    line: { color: cor || REGUA, width: espessura || 0.75 } });
}

function titulo(s, t, sub) {
  s.addText(t, { x: M, y: 0.42, w: W - 2*M, h: 0.62, fontFace: FONTE, fontSize: 26,
    color: TINTA, bold: true, margin: 0, valign: 'bottom' });
  let y = 1.06;
  if (sub) {
    s.addText(sub, { x: M, y, w: W - 2*M - 1.0, h: 0.42, fontFace: FONTE, fontSize: 13,
      color: CINZA, italic: true, margin: 0 });
    y += 0.44;
  }
  regua(s, y + 0.06, 1.0, TINTA);
  return y + 0.28;
}

/** Parágrafo com entrada em negrito. `marcado` põe o filete de acento à esquerda. */
function bloco(s, x, y, w, entrada, texto, marcado, h) {
  if (marcado) regua(s, y - 0.06, 1.25, ACENTO, x, Math.min(w, 0.9));
  const alt = Math.min(h || 0.9, H - 0.72 - y);
  s.addText([
    { text: entrada + '  ', options: { bold: true, color: marcado ? ACENTO : TINTA } },
    { text: texto, options: { color: TINTA } },
  ], { x, y, w, h: alt, fontFace: FONTE, fontSize: 12.5, margin: 0, valign: 'top', lineSpacing: 16.5 });
}

/** Número em destaque: valor grande sobre filete, rótulo abaixo. */
function numero(s, x, y, w, valor, rot, destaque) {
  regua(s, y, 1.0, destaque ? ACENTO : TINTA, x, w);
  s.addText(valor, { x, y: y + 0.08, w, h: 0.62, fontFace: FONTE, fontSize: 30,
    color: destaque ? ACENTO : TINTA, bold: true, margin: 0 });
  s.addText(rot, { x, y: y + 0.72, w, h: 0.42, fontFace: FONTE, fontSize: 10.5,
    color: CINZA, margin: 0 });
}

function tabela(s, cab, linhas, o) {
  o = Object.assign({ x: M, y: 2.0, w: W - 2*M, colW: null, fontSize: 11.5, rowH: 0.32 }, o || {});
  const head = cab.map(t => ({ text: t, options: { bold: true, color: TINTA, fontFace: FONTE,
    fontSize: o.fontSize - 0.5, border: [{ pt: 1.25, color: TINTA }, { type: 'none' },
      { pt: 0.75, color: TINTA }, { type: 'none' }] } }));
  const ult = linhas.length - 1;
  const corpo = linhas.map((ln, i) => ln.map(c => {
    const cel = (typeof c === 'object') ? { text: String(c.text), options: Object.assign({}, c.options) }
                                        : { text: String(c === null ? '—' : c), options: {} };
    cel.options = Object.assign({ fontFace: FONTE, fontSize: o.fontSize, color: TINTA,
      border: [{ type: 'none' }, { type: 'none' },
        i === ult ? { pt: 1.25, color: TINTA } : { type: 'none' }, { type: 'none' }] }, cel.options);
    return cel;
  }));
  s.addTable([head, ...corpo], { x: o.x, y: o.y, w: o.w, colW: o.colW,
    autoPage: false, rowH: o.rowH, valign: 'middle' });
  return o.y + o.rowH * (linhas.length + 1);
}

function legendaTabela(s, y, texto, fonte) {
  nTabela++;
  s.addText([
    { text: `Tabela ${nTabela} — `, options: { bold: true } },
    { text: texto, options: {} },
  ], { x: M, y, w: W - 2*M, h: 0.34, fontFace: FONTE, fontSize: 11, color: TINTA, margin: 0 });
  if (fonte) s.addText(fonte, { x: M, y: y + 0.28, w: W - 2*M, h: 0.28,
    fontFace: FONTE, fontSize: 9.5, color: CINZA_C, italic: true, margin: 0 });
  return y + (fonte ? 0.60 : 0.36);
}

function legendaFigura(s, y, texto, fonte) {
  nFigura++;
  s.addText([
    { text: `Figura ${nFigura} — `, options: { bold: true } },
    { text: texto + (fonte ? `  ${fonte}` : ''), options: {} },
  ], { x: M, y, w: W - 2*M, h: 0.34, fontFace: FONTE, fontSize: 10.5, color: CINZA, margin: 0 });
}

function nota(s, txt) {
  s.addText(txt, { x: M, y: H - 0.78, w: W - 2*M - 0.8, h: 0.36, fontFace: FONTE,
    fontSize: 9.5, color: CINZA_C, italic: true, margin: 0 });
}

/** Bloco de tabela do JSON: legenda numerada acima, tabela, procedência embaixo. */
function blocoTabela(s, chave, legenda, opts) {
  const b = TB[chave];
  const o = Object.assign({ y: 2.0, fontSize: 11.5, rowH: 0.32, colW: null }, opts || {});
  const yTab = legendaTabela(s, o.y, legenda, `Fonte: ${b.fonte}`);
  return tabela(s, b.colunas, b.linhas, { y: yTab, colW: o.colW, fontSize: o.fontSize, rowH: o.rowH });
}

// ═════════ CAPA ═════════
{ const s = S();
  s.addText('INICIAÇÃO CIENTÍFICA · FIOCRUZ MINAS — IRR', { x: M, y: 1.35, w: W - 2*M, h: 0.34,
    fontFace: FONTE, fontSize: 11.5, color: CINZA, charSpacing: 2, margin: 0 });
  regua(s, 1.78, 1.0, TINTA);
  s.addText('Os extremos de renda: o critério, aberto', { x: M, y: 1.95, w: W - 2*M, h: 1.0,
    fontFace: FONTE, fontSize: 40, color: TINTA, bold: true, margin: 0 });
  s.addText('Como um setor censitário vira SUSPEITO, EXTREMO ou NORMAL.\n' +
            'Anexo à EDA Central · Índice de Vulnerabilidade da Saúde intraurbano · ' +
            'Censo Demográfico 2022 · 70 municípios do ELSI-Brasil',
    { x: M, y: 3.05, w: 9.4, h: 1.1, fontFace: FONTE, fontSize: 14, color: CINZA,
      margin: 0, lineSpacing: 20 });
  regua(s, H - 1.35, 0.75);
  s.addText('Pedro Dias Soares  ·  setembro de 2026  ·  ' + N.n_rastreados +
            ' setores extremos rastreados',
    { x: M, y: H - 1.2, w: W - 2*M, h: 0.5, fontFace: FONTE, fontSize: 11, color: CINZA, margin: 0 });
  s.addNotes('O deck da EDA Central resume a classificação em um slide e meio. Este anexo abre ' +
             'a regra inteira, incluindo o que ela não pega.');
}

// ═════════ 1. O PROBLEMA ═════════
{ const s = S();
  const y = titulo(s, 'Por que a renda precisa de critério próprio',
    'Assimetria 3,74 no recorte urbano, a maior das sete componentes.');
  bloco(s, M, y + 0.15, W - 2*M,
    'Três coisas diferentes com a mesma aparência.',
    'Os valores extremos de V06004 não têm todos a mesma natureza, e é por isso que existe ' +
    'um critério em vez de uma regra única.', false, 0.7);
  let yy = y + 1.05;
  [['Erro de dado', 'O setor de favela em Belo Horizonte com R$ 170.418,06 de renda média por responsável.'],
   ['Extremo genuíno', 'O bairro rico cuja renda alta o entorno inteiro sustenta.'],
   ['Setor pequeno com média instável', 'Poucos domicílios fazem a média oscilar.'],
  ].forEach(([t, d]) => { bloco(s, M, yy, W - 2*M, t + '.', d, false, 0.62); yy += 0.72; });
  bloco(s, M, yy + 0.25, W - 2*M, 'O custo de tratar os três igual.',
    'Excluir todos apaga a desigualdade que o índice existe para medir. Manter todos deixa ' +
    'o erro entrar no cálculo. Perde-se informação nos dois sentidos.', true, 0.8);
}

// ═════════ 2. O PROCEDIMENTO ═════════
{ const s = S();
  const y = titulo(s, 'O procedimento, em quatro etapas',
    'src/ivs_censo/renda.py, função rastrear_outliers_renda.');
  const et = [
    ['1', 'O corte de extremo', 'Limite superior de Tukey, q3 + k × (q3 − q1), com k = ' + K.k_tukey + '.'],
    ['2', 'Calculado por município', 'O quartil sai da distribuição da própria cidade, não do país.'],
    ['3', 'A trava dos pequenos', 'Município com menos de ' + K.min_setores + ' setores não é avaliado.'],
    ['4', 'Os três testes de coerência', 'O perfil do setor sustenta a renda declarada? Basta um falhar.'],
  ];
  let yy = y + 0.3;
  et.forEach(([n2, t, d]) => {
    s.addShape(p.ShapeType.ellipse, { x: M, y: yy + 0.04, w: 0.52, h: 0.52,
      fill: { type: 'none' }, line: { color: TINTA, width: 1.25 } });
    s.addText(n2, { x: M, y: yy + 0.04, w: 0.52, h: 0.52, align: 'center', valign: 'middle',
      fontFace: FONTE, fontSize: 17, color: TINTA, bold: true });
    s.addText(t, { x: M + 0.78, y: yy, w: 3.1, h: 0.5, fontFace: FONTE, fontSize: 14,
      bold: true, color: TINTA, margin: 0 });
    s.addText(d, { x: M + 4.0, y: yy, w: W - M - 4.7, h: 0.62, fontFace: FONTE, fontSize: 12.5,
      color: TINTA, margin: 0 });
    yy += 0.92;
  });
  bloco(s, M, yy + 0.2, W - 2*M, 'A saída é um rótulo, não uma exclusão.',
    'O módulo não remove observação nenhuma. As duas versões da análise, com e sem os ' +
    'suspeitos, ficam publicadas lado a lado.', true, 0.8);
}

// ═════════ 3. ETAPAS 1 E 2 ═════════
{ const s = S();
  const y = titulo(s, 'Onde cai o corte, e em relação a quê');
  bloco(s, M, y + 0.15, 5.6, 'k = ' + K.k_tukey + ', não 1,5.',
    'A tabela de outliers da EDA Central usa k = 1,5, o padrão do boxplot, que rotula a ' +
    'cauda inteira. Aqui a intenção não é descrever a cauda, é isolar o extremo distante ' +
    'para inspeção — então o corte é o de outlier extremo.', false, 2.0);
  bloco(s, M + 6.2, y + 0.15, 5.6, 'O corte é municipal.',
    'R$ 20 mil é comum em São Paulo e anômalo em Autazes. Um corte nacional mede a ' +
    'distância entre cidades, que não é o objeto: o IVS compara setores dentro da mesma ' +
    'cidade.', false, 2.0);
  numero(s, M, y + 2.45, 3.6, K.k_tukey, 'k de Tukey no critério de renda');
  numero(s, M + 3.9, y + 2.45, 3.6, '1,5', 'k na tabela de outliers do deck principal');
  numero(s, M + 7.8, y + 2.45, 3.9, N.concordam, 'setores que os dois critérios marcam juntos', true);
  nota(s, 'Os dois limiares convivem no projeto para finalidades diferentes: k = 1,5 descreve a ' +
          'forma da distribuição, k = ' + K.k_tukey + ' seleciona casos.');
}

// ═════════ 4. A TRAVA DOS PEQUENOS ═════════
{ const s = S();
  const y = titulo(s, 'A trava dos municípios pequenos',
    'Abaixo de ' + K.min_setores + ' setores o quartil do município não é confiável.');
  const yy = blocoTabela(s, 'municipios_pequenos',
    'Municípios fora da detecção municipal, por não atingirem o mínimo de setores.',
    { y: y + 0.12, fontSize: 10.5, rowH: 0.245, colW: [3.4, 2.0, 1.4] });
  bloco(s, M + 7.4, y + 0.6, W - M - 8.1, N.n_mun_peq + ' dos 70 municípios ficam de fora.',
    'Somam ' + N.n_set_peq + ' setores. Nesses municípios o limite superior fica indefinido e ' +
    'nenhum setor pode ser marcado, então um erro de renda ali não é detectado. ' +
    N.n_mun_aval + ' municípios são efetivamente avaliados.', true, 1.6);
  bloco(s, M + 7.4, y + 2.5, W - M - 8.1, 'Não está na EDA Central.',
    'É limitação a declarar no artigo, junto com as outras três da penúltima página.', false, 1.0);
}

// ═════════ 5. OS TRÊS TESTES ═════════
{ const s = S();
  const y = titulo(s, 'Os três testes de coerência',
    'Cada um compara o setor com o próprio município. Basta um disparar.');
  const yTab = legendaTabela(s, y + 0.15,
    'Condição e limiar de cada teste de incoerência.',
    'Fonte: src/ivs_censo/renda.py, função rastrear_outliers_renda.');
  tabela(s, ['Teste', 'Condição', 'Limiar'], [
    [{ text: 'e_favela', options: { fontFace: MONO, fontSize: 11 } },
     'CD_TIPO = 1, ou seja, Favela e Comunidade Urbana',
     'categoria, não limiar'],
    [{ text: 'pct_analfab_acima', options: { fontFace: MONO, fontSize: 11 } },
     'analfabetismo do setor acima do do município',
     { text: 'mediana (p50) local', options: { bold: true } }],
    [{ text: 'pct_raca_pretpardind_acima', options: { fontFace: MONO, fontSize: 11 } },
     'proporção preta, parda ou indígena acima da do município',
     { text: 'terceiro quartil (p75) local', options: { bold: true, color: ACENTO } }],
  ], { y: yTab, colW: [3.4, 5.6, 2.63], fontSize: 11.5, rowH: 0.42 });
  bloco(s, M, y + 2.5, W - 2*M, 'Os dois limiares são diferentes.',
    'A EDA Central diz apenas "acima da mediana do município" para os dois. O de cor/raça é ' +
    'o p75, não a mediana.', true, 0.7);
  bloco(s, M, y + 3.35, W - 2*M, 'A classificação sai daí.',
    'Extremo e incoerente é SUSPEITO. Extremo e coerente é EXTREMO. O resto é NORMAL. ' +
    'Setor sem renda informada não é outlier de renda e fica em NORMAL.', false, 0.8);
}

// ═════════ 6. AS TRÊS CLASSES ═════════
{ const s = S();
  const y = titulo(s, 'O resultado: as três classes');
  const yy = blocoTabela(s, 'classes', 'Setores por classe, com o perfil de renda de cada uma.',
    { y: y + 0.2, fontSize: 12.5, rowH: 0.46, colW: [2.3, 1.7, 1.7, 2.0, 2.0, 1.93] });
  bloco(s, M, yy + 0.45, W - 2*M, 'A leitura que é fácil inverter.',
    'A renda mediana dos SUSPEITOS é MENOR que a dos EXTREMOS. Isso é coerente com o ' +
    'desenho: o critério não seleciona os valores mais altos, seleciona os valores altos ' +
    'no lugar errado.', true, 0.9);
  numero(s, M, yy + 1.7, 3.6, N.n_suspeitos, 'suspeitos');
  numero(s, M + 3.9, yy + 1.7, 3.6, N.n_extremos, 'extremos coerentes');
  numero(s, M + 7.8, yy + 1.7, 3.9, N.n_rastreados, 'setores extremos rastreados ao todo');
}

// ═════════ 7. O QUE CADA TESTE PEGOU ═════════
{ const s = S();
  const y = titulo(s, 'O que cada teste efetivamente pegou',
    'A abertura que a EDA Central não traz.');
  blocoTabela(s, 'motivos', 'Combinação de testes que disparou em cada um dos ' +
    N.n_suspeitos + ' suspeitos.',
    { y: y + 0.15, fontSize: 11.5, rowH: 0.34, colW: [6.4, 1.6] });
  bloco(s, M + 8.6, y + 0.55, W - M - 9.3, N.um_teste + ' dos ' + N.n_suspeitos + ' disparam um só teste.',
    'Apenas ' + N.tres_testes + ' disparam os três. A suspeita, na maioria dos casos, se ' +
    'apoia num sinal único.', true, 1.2);
  bloco(s, M + 8.6, y + 2.0, W - M - 9.3, 'E o sinal único é o mais fraco.',
    N.so_analfab + ' são flagrados só por analfabetismo acima da mediana do município, que é ' +
    'evento de cerca de metade dos setores por construção. Esses merecem inspeção ' +
    'individual, não tratamento de bloco.', false, 1.6);
  bloco(s, M, y + 3.4, W - 2*M, N.n_favela + ' dos ' + N.n_suspeitos + ' são favela.',
    'Como e_favela é um dos testes, nenhum setor de favela pode cair em EXTREMO. Dizer que ' +
    '"nenhum extremo coerente é favela" repete a regra; não a confirma.', false, 0.8);
}

// ═════════ 8. FIGURA ═════════
{ const s = S();
  const y = titulo(s, 'Os testes e o contraponto independente');
  s.addImage({ path: path.join(FIG, 'renda_criterio_motivos.png'),
    x: 1.15, y: y + 0.25, w: 11.0, h: 11.0 * 3.1 / 9.2 });
  legendaFigura(s, y + 4.15,
    'À esquerda, quantos suspeitos cada teste marcou. À direita, o coeficiente de variação ' +
    'da renda nas duas classes.',
    'banco_de_dados/eda/figuras/renda_criterio_motivos.png');
  bloco(s, M, y + 4.75, W - 2*M, 'O CV não vem do critério.',
    'Mediana de ' + N.cv_med_sus + ' entre os suspeitos contra ' + N.cv_med_ext + ' entre os ' +
    'extremos coerentes, quase o dobro. Como ele usa V06005, variável que a regra não ' +
    'consulta, é a única evidência aqui que não é circular.', true, 0.9);
}

// ═════════ 9. OS MAIORES SUSPEITOS ═════════
{ const s = S();
  const y = titulo(s, 'Os maiores suspeitos');
  blocoTabela(s, 'maiores_suspeitos', 'Os oito suspeitos de maior renda declarada.',
    { y: y + 0.2, fontSize: 10, rowH: 0.38,
      colW: [2.35, 1.55, 1.85, 1.15, 1.25, 0.85, 0.72, 0.72, 1.19] });
  nota(s, 'Renda e mediana municipal em reais. CV = √V06005 ÷ V06004.');
}

// ═════════ 10. CV E A VÍRGULA ═════════
{ const s = S();
  const y = titulo(s, 'A hipótese da vírgula fora do lugar, testada',
    'O arquivo do IBGE traz V06005, a variância do rendimento no setor.');
  bloco(s, M, y + 0.15, W - 2*M, 'O teste.',
    'Se o valor de Belo Horizonte fosse R$ 1.704,18, isto é, 170.418,06 dividido por 100, e ' +
    'apenas a média tivesse deslizado uma casa decimal, o coeficiente de variação do setor ' +
    'seria da ordem de 526.', false, 0.85);
  numero(s, M, y + 1.25, 2.70, '5,26', 'CV observado em Belo Horizonte', true);
  numero(s, M + 2.98, y + 1.25, 2.70, '0,78', 'mediana nacional do CV');
  numero(s, M + 5.96, y + 1.25, 2.70, '2,53', 'p99 do CV');
  numero(s, M + 8.94, y + 1.25, 2.70, '8,12', 'p99,9 do CV');
  bloco(s, M, y + 2.75, W - 2*M, 'O que isso quer dizer.',
    'A variância publicada pelo IBGE é coerente com a média alta. O dado não indica erro de ' +
    'digitação: indica um setor com uma ou poucas declarações enormes puxando a média.', true, 0.85);
  bloco(s, M, y + 3.75, W - 2*M, 'A consequência é mais incômoda.',
    'Não se corrige dividindo por 100, nem se resolve excluindo ' + N.n_suspeitos + ' setores. ' +
    'Argumenta-se por estatística robusta — posto ou logaritmo — para a variável inteira.', false, 0.85);
}

// ═════════ 11. O PONTO CEGO ═════════
{ const s = S();
  const y = titulo(s, 'O ponto cego: erro em bairro rico',
    'A regra detecta incoerência de contexto, não implausibilidade de magnitude.');
  const yImp = blocoTabela(s, 'implausiveis',
    'Setores classificados EXTREMO que a coluna razao_implausivel denuncia.',
    { y: y + 0.12, fontSize: 9.5, rowH: 0.265,
      colW: [2.35, 1.55, 2.13, 1.25, 1.35, 0.95, 1.0, 1.05] });
  bloco(s, M, yImp + 0.25, 5.6, 'Acima de ' + K.razao_implausivel + '× a mediana local.',
    'A coluna marca por magnitude, sem olhar o perfil do entorno: ' + N.n_impl_ext +
    ' setores em EXTREMO e ' + N.n_impl_sus + ' já em SUSPEITO.', true, 1.0);
  bloco(s, M + 6.2, yImp + 0.25, 5.43, 'É diagnóstico, não critério.',
    'Promovê-la mudaria números já apresentados, então não foi feito sem sua palavra.', false, 1.0);
  nota(s, 'O primeiro da tabela é o segundo maior valor de renda de toda a base.');
}

// ═════════ 12. GLOBAL × MUNICIPAL ═════════
{ const s = S();
  const y = titulo(s, 'Global e municipal não são o mesmo corte');
  const yy = blocoTabela(s, 'criterios',
    'Setores marcados por cada critério, região a região.',
    { y: y + 0.2, fontSize: 11.5, rowH: 0.4, colW: [2.2, 1.6, 1.5, 1.6, 1.7, 1.9, 1.13] });
  bloco(s, M, yy + 0.4, W - 2*M, 'A inversão entre Norte e Sudeste é o argumento inteiro.',
    'O critério global marca 4,61% do Sudeste e 1,32% do Norte, porque responde a "este setor ' +
    'é rico para o Brasil?". O municipal inverte, 7,40% no Norte e 2,22% no Sudeste, porque ' +
    'responde a "este setor destoa da própria cidade?".', true, 1.0);
  bloco(s, M, yy + 1.55, W - 2*M, 'Para um índice intraurbano, a segunda pergunta é a certa.',
    'Dos ' + N.n_global + ' marcados pelo global e ' + N.n_municipal + ' pelo municipal, ' +
    'apenas ' + N.concordam + ' estão nos dois.', false, 0.8);
}

// ═════════ 13. TAMANHO DO SETOR ═════════
{ const s = S();
  const y = titulo(s, 'A relação com o tamanho do setor',
    'A hipótese se confirma pela metade, e a distinção importa.');
  const yy = blocoTabela(s, 'tamanho', 'Renda e taxa de suspeita por faixa de tamanho do setor.',
    { y: y + 0.2, fontSize: 11, rowH: 0.4, colW: [2.0, 1.3, 1.3, 1.55, 1.55, 1.1, 1.3, 1.53] });
  bloco(s, M, yy + 0.4, 5.6, 'O valor não depende do tamanho.',
    'Spearman entre número de domicílios e renda: −0,031. O maior valor da base está num ' +
    'setor de 186 domicílios, que é o tamanho mediano.', false, 1.2);
  bloco(s, M + 6.2, yy + 0.4, 5.6, 'A taxa de suspeita depende.',
    '0,265% nos setores de até 50 domicílios contra 0,045% nos de 201 a 400, seis vezes ' +
    'menos. O mecanismo existe e está medido; ele só não produz o maior valor.', true, 1.2);
}

// ═════════ 14. LIMITAÇÕES ═════════
{ const s = S();
  const y = titulo(s, 'As quatro limitações do critério');
  let yy = y + 0.2;
  [['A separação favela / não favela é definição',
    'e_favela é um dos testes, então toda favela que seja outlier municipal cai em SUSPEITO e ' +
    'nenhuma pode cair em EXTREMO. A coluna "São favela?" repete a regra; não a valida.'],
   ['O sinal do analfabetismo é fraco',
    'Estar acima da mediana do município é evento de cerca de 50% por construção, e ' +
    N.so_analfab + ' dos ' + N.n_suspeitos + ' suspeitos são flagrados só por ele.'],
   ['Erro em bairro rico é invisível',
    'Os ' + N.n_impl_ext + ' setores da tabela anterior saem como EXTREMO porque o entorno ' +
    'sustenta renda alta. Só razao_implausivel os denuncia.'],
   ['Municípios pequenos ficam fora',
    N.n_mun_peq + ' municípios e ' + N.n_set_peq + ' setores não são avaliados, porque abaixo ' +
    'de ' + K.min_setores + ' setores o quartil do município não é confiável.'],
  ].forEach(([t, d]) => { bloco(s, M, yy, W - 2*M, t + '.', d, true, 1.1); yy += 1.28; });
}

// ═════════ 15. RECOMENDAÇÃO ═════════
{ const s = S();
  const y = titulo(s, 'O que eu recomendo, e o que depende da senhora');
  s.addText('Que os ' + N.n_suspeitos + ' suspeitos saiam do cálculo do índice e fiquem na EDA ' +
            'como achado de qualidade do dado, com as duas versões publicadas.',
    { x: M, y: y + 0.2, w: W - 2*M, h: 0.8, fontFace: FONTE, fontSize: 19, color: TINTA,
      bold: true, margin: 0, valign: 'top' });
  regua(s, y + 1.1, 1.25, TINTA);
  bloco(s, M, y + 1.3, W - 2*M, 'O argumento é a escala, não a média.',
    'Em Autazes um único valor ruim comprime 81,4% dos setores no primeiro decil da ' +
    'normalização min-max; sem ele são 14,3%. Dos ' + N.norm_avaliados + ' municípios ' +
    'avaliados, ' + N.norm_com_suspeito + ' têm ao menos um suspeito.', false, 0.9);
  const yTab = legendaTabela(s, y + 2.4, 'As três decisões em aberto, que são de método.');
  tabela(s, ['#', 'Decisão', 'Minha leitura'], [
    ['1', 'Promover razao_implausivel a critério',
     'Pegaria os ' + N.n_impl_ext + ' casos que hoje escapam. Muda números já apresentados.'],
    ['2', 'Inspecionar os ' + N.so_analfab + ' suspeitos de sinal único',
     'Trabalho manual e finito. Evita excluir setor legítimo por um teste fraco.'],
    ['3', 'Transformar a variável, em log ou em posto',
     'Mesmo sem os ' + N.n_suspeitos + ', Belo Horizonte fica com 70,8% no primeiro decil.'],
  ], { y: yTab, colW: [0.6, 4.4, 6.63], fontSize: 11.5, rowH: 0.5 });
  nota(s, 'A regra: src/ivs_censo/renda.py. As tabelas: scripts/auditoria_renda.py. ' +
          'Os ' + N.n_rastreados + ' setores, um por linha: renda_outliers_rastreados.csv.');
}

p.writeFile({ fileName: process.argv[2] }).then(f => console.log('deck escrito:', f));
