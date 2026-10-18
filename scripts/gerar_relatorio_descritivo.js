/**
 * Deck do relatório descritivo do andamento (`relatorio_descritivo/`).
 *
 * Monta o deck inteiro, sempre do zero, a partir de `dados/numeros.json` — nenhum número
 * é digitado aqui. Cada tipo de slide tem um layout fixo (um por parte), escolhido pelo
 * forma dos dados. O ID vai no canto superior direito; a fonte, só nas notas do apresentador.
 *
 * Uso:  node scripts/gerar_relatorio_descritivo.js
 */
const fs = require('fs');
const path = require('path');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const PASTA = path.join(RAIZ, 'relatorio_descritivo');
const N = JSON.parse(fs.readFileSync(path.join(PASTA, 'dados', 'numeros.json'), 'utf8'));
const PRINCIPAL = path.join(PASTA, 'Relatorio_Descritivo_IVS_2026-10.pptx');
const BASE = path.join(PASTA, 'dados', 'ultimo_gerado.pptx');     // cópia intocada do último gerado
const HASH = path.join(PASTA, 'dados', 'gerado.sha256');
const arg = (k) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const SAIDA = arg('--saida') ? path.resolve(arg('--saida')) : PRINCIPAL;
const sha = (f) => require('crypto').createHash('sha256').update(fs.readFileSync(f)).digest('hex');

// Trava (08/10/2026): o Pedro edita o deck principal à mão. Regerar por cima apagaria as edições.
// Só sobrescreve o principal se ele for idêntico ao último gerado, ou com --sobrescrever.
if (SAIDA === PRINCIPAL && fs.existsSync(PRINCIPAL) && !process.argv.includes('--sobrescrever')) {
  const gravado = fs.existsSync(HASH) ? fs.readFileSync(HASH, 'utf8').trim() : '';
  if (sha(PRINCIPAL) !== gravado) {
    console.error('RECUSADO: o deck principal foi editado à mão (ou não há registro do último gerado).\n' +
      '  Rode scripts/comparar_edicoes_relatorio.py, leve as edições à origem e só então use --sobrescrever,\n' +
      '  ou gere noutro arquivo com --saida <caminho>.');
    process.exit(2);
  }
}

const d = criarDeck({ titulo: 'Relatório descritivo do andamento — IVS Censo 2022' });
const { cores: C, geo: { W, H, M } } = d;

function encaixe(fig, x, y, w, h) {
  const png = fs.readFileSync(path.join(PASTA, fig));
  const pw = png.readUInt32BE(16), ph = png.readUInt32BE(20), e = Math.min(w / pw, h / ph);
  return { x: x + (w - pw * e) / 2, y, w: pw * e, h: ph * e };
}
function marca(s, id) {
  s.addText(id, { x: W - M - 1.6, y: 0.16, w: 1.6, h: 0.3, fontFace: C.FONTE, fontSize: 11,
    color: C.ACENTO, bold: true, align: 'right', margin: 0 });
}
function figura(s, x, area) {
  s.addImage({ path: path.join(PASTA, x.figura), x: area.x, y: area.y,
    sizing: { type: 'contain', w: area.w, h: area.h } });
}
function rotulo(s, x, y, w, t) {
  s.addText(t, { x, y, w, h: 0.3, fontFace: C.FONTE, fontSize: 12, bold: true, color: C.TINTA, margin: 0 });
  return y + 0.34;
}
function paragrafo(s, x, y, w, entrada, texto, marcado) {
  const h = d.alturaTexto(entrada + '  ' + texto, w, 12.5, 16.5) + 0.12;
  d.bloco(s, x, y, w, entrada, texto, marcado, h);
  return y + h + 0.14;
}

// ── Layouts ─────────────────────────────────────────────────────────────────────
const LAYOUT = {
  A01(s, x) { d.capa(s, x.kicker, x.titulo, x.sub, x.rodape); },

  A02(s, x) {
    const y0 = d.titulo(s, x.titulo, x.sub) + 0.1;
    let y = y0;
    x.blocos.forEach(([e, t]) => { y = paragrafo(s, M, y, 5.6, e, t); });
    const y2 = rotulo(s, 6.9, y0, 5.6, 'As bases de cada parte');
    d.tabelaAjustada(s, x.cab, x.linhas, { x: 6.9, y: y2, colW: [2.1, 0.9, 1.9, 0.7], fontSize: 10.5 });
  },

  DM(s, x) {
    const y0 = d.titulo(s, x.titulo, x.sub) + 0.1;
    let y = y0;
    x.caixas.slice(0, 3).forEach(([e, t]) => { y = paragrafo(s, M, y, 5.9, e + '.', t); });
    let y2 = paragrafo(s, 7.05, y0, 5.43, x.caixas[3][0] + '.', x.caixas[3][1], true);
    y2 = rotulo(s, 7.05, y2, 5.43, 'Resultado');
    y2 = d.tabelaAjustada(s, x.cab, x.linhas, { x: 7.05, y: y2, colW: x.colW || [2.15, 1.1, 1.09, 1.09],
      fontSize: x.linhas.length > 6 ? 9 : 10, rowH: x.linhas.length > 6 ? 0.24 : 0.3 });
    paragrafo(s, 7.05, y2 + 0.12, 5.43, 'Resultado completo em', x.resultado_em + '.');
  },

  divisoria(s, x) { d.secao(s, x.numero, x.titulo, x.sub); },

  tabelaLarga(s, x) {
    const y = d.titulo(s, x.titulo, x.sub) + 0.1;
    const fs = x.linhas.length > 8 ? 9.5 : 10.5;
    const y2 = d.tabelaAjustada(s, x.cab, x.linhas, { x: M, y, colW: x.colW, fontSize: fs, rowH: 0.27 });
    if (x.frases) paragrafo(s, M, y2 + 0.25, 11.63, 'O que mostra.', x.frases.join(' '));
  },

  DS01(s, x) {
    const y = d.titulo(s, x.titulo, x.sub) + 0.1;
    const y2 = d.tabelaAjustada(s, x.cab, x.linhas, { x: M, y, colW: [2.6, 0.95, 0.85, 2.6], fontSize: 10.5 });
    paragrafo(s, M, y2 + 0.25, 7.0, 'O que mostra.', x.frases.join(' '));
    figura(s, x, { x: 8.15, y, w: 4.33, h: 3.9 });
    d.legendaFigura(s, y + 3.98, x.legenda, null, 8.15, 4.33);
  },

  DS(s, x) {
    s.addText(x.dimensao.toUpperCase(), { x: M, y: 0.16, w: 6, h: 0.3, fontFace: C.FONTE,
      fontSize: 10.5, color: C.CINZA, charSpacing: 2, margin: 0 });
    const y = d.titulo(s, x.titulo, x.sub) + 0.08;
    // esquerda: como é calculado (definição, arquivo de origem, local do cálculo)
    const tam = x.definicao.reduce((t, l) => t + String(l[1]).length, 0);
    let yl = rotulo(s, M, y, 3.75, 'Como é calculado');
    yl = d.tabelaAjustada(s, ['', ''], x.definicao, { x: M, y: yl - 0.3, colW: [1.15, 2.6],
      fontSize: tam > 650 ? 6.5 : (tam > 330 ? 8 : 9), rowH: 0.22 });
    if (x.observacao) {
      const h = d.alturaTexto(x.observacao, 3.75, 8.5, 10.5) + 0.05;
      s.addText(x.observacao, { x: M, y: yl + 0.06, w: 3.75, h, fontFace: C.FONTE, fontSize: 8.5,
        italic: true, color: C.CINZA, margin: 0, valign: 'top' });
    }
    // centro: a distribuição
    d.tabelaAjustada(s, x.cab, x.linhas, { x: 4.85, y, colW: [1.95, 1.3], fontSize: 10, rowH: 0.262 });
    // direita: o histograma deste indicador só, e o que ele mostra
    figura(s, x, { x: 8.35, y, w: 4.13, h: 2.85 });
    d.legendaFigura(s, y + 2.9, x.legenda, null, 8.35, 4.13);
    const hl = d.alturaTexto('Figura 00 — ' + x.legenda, 4.13, 10.5, 13) + 0.12;
    paragrafo(s, 8.35, y + 2.9 + hl, 4.13, 'O que mostra.', x.frases.join(' '));
  },

  FA(s, x) {
    const y = d.titulo(s, x.titulo, x.sub) + 0.1;
    const y2 = d.tabelaAjustada(s, x.cab, x.linhas, { x: M, y, colW: x.colW || [1.15, 1.05, 1.5, 1.3, 1.3],
      fontSize: x.linhas.length > 9 ? 9.5 : 10.5 });
    paragrafo(s, M, y2 + 0.25, 6.3, 'O que mostra.', x.frases.join(' '));
    figura(s, x, { x: 7.55, y, w: 4.93, h: 3.9 });
    d.legendaFigura(s, y + 3.98, x.legenda, null, 7.55, 4.93);
  },

  FP(s, x) {
    const y = d.titulo(s, x.titulo, x.sub) + 0.1;
    const n = x.linhas.length;
    const y2 = d.tabelaAjustada(s, x.cab, x.linhas, { x: M, y, colW: x.colW || [0.8, 3.15, 0.95, 0.7, 1.1, 1.1, 1.35, 2.48],
      fontSize: n > 12 ? 8.5 : (n > 8 ? 9.5 : 10), rowH: n > 12 ? 0.22 : 0.27 });
    if (x.frases) paragrafo(s, M, y2 + 0.25, 11.63, 'O que mostra.', x.frases.join(' '));
  },

  tabelaTexto(s, x) {
    const y = d.titulo(s, x.titulo, x.sub) + 0.1;
    const w = x.colW.reduce((a, b) => a + b, 0);
    d.tabelaAjustada(s, x.cab, x.linhas, { x: M, y, colW: x.colW, fontSize: x.linhas.length > 9 ? 9.5 : 10.5 });
    if (x.frases) paragrafo(s, M + w + 0.5, y, 11.63 - w - 0.5, 'O que mostra.', x.frases.join(' '));
  },

  duasTabelas(s, x) {
    const y = d.titulo(s, x.titulo, x.sub) + 0.05;
    const k = Math.ceil(x.linhas.length / 2), cw = [2.75, 1.0, 1.0, 0.85];
    d.tabelaAjustada(s, x.cab, x.linhas.slice(0, k), { x: M, y, colW: cw, fontSize: 9, rowH: 0.27 });
    d.tabelaAjustada(s, x.cab, x.linhas.slice(k), { x: M + 6.03, y, colW: cw, fontSize: 9, rowH: 0.27 });
  },

  // C-04 ─ encaixe da figura calculado pelo tamanho do PNG (o 'contain' do pptxgenjs sem ele erra)
  DSX(s, x) {
    s.addText((x.dimensao || '').toUpperCase(), { x: M, y: 0.16, w: 6, h: 0.3, fontFace: C.FONTE,
      fontSize: 10.5, color: C.CINZA, charSpacing: 2, margin: 0 });
    const y = d.titulo(s, x.titulo, x.sub) + 0.08;
    const f = encaixe(x.figura, M, y, 7.55, 3.75);
    s.addImage({ path: path.join(PASTA, x.figura), ...f });
    d.legendaFigura(s, f.y + f.h + 0.05, x.legenda, null, M, 7.55);
    d.tabelaAjustada(s, x.cab, x.linhas, { x: 8.6, y, colW: x.colW, fontSize: 10, rowH: 0.27 });
    paragrafo(s, M, f.y + f.h + 0.45, 11.63, 'O que mostra.', x.frases.join(' '));
  },

  figuraLarga(s, x) {
    const y = d.titulo(s, x.titulo, x.sub) + 0.05;
    const f = encaixe(x.figura, M, y, 8.4, 4.75);
    s.addImage({ path: path.join(PASTA, x.figura), ...f });
    paragrafo(s, M + 8.7, y + 0.1, 2.93, 'O que mostra.', x.frases.join(' '));
    d.legendaFigura(s, f.y + f.h + 0.05, x.legenda, null, M, 8.4);
  },

  FC(s, x) {
    // a primeira tabela à esquerda; as outras empilhadas à direita; o texto embaixo da primeira
    const y = d.titulo(s, x.titulo, x.sub) + 0.1;
    const t0 = x.tabelas[0], w0 = t0.colW.reduce((a, b) => a + b, 0);
    const fim0 = d.tabelaAjustada(s, t0.cab, t0.linhas, { x: M, y, colW: t0.colW, fontSize: 9.5, rowH: 0.24 });
    let yd = y;
    x.tabelas.slice(1).forEach(t => {
      yd = d.tabelaAjustada(s, t.cab, t.linhas, { x: M + w0 + 0.6, y: yd, colW: t.colW, fontSize: 9.5, rowH: 0.24 }) + 0.25;
    });
    paragrafo(s, M, fim0 + 0.2, w0, 'O que mostra.', x.frases.join(' '));
  },

  blocos(s, x) {
    let y = d.titulo(s, x.titulo, x.sub) + 0.1;
    x.blocos.forEach(([e, t]) => { y = paragrafo(s, M, y, 9.5, e, t); });
  },
};

/** O layout sai do ID (os de forma própria) ou da forma dos dados (os genéricos). */
function layoutDe(id, x) {
  if (['A01', 'A02', 'DS01'].includes(id)) return LAYOUT[id];
  if (id === 'DS02') return LAYOUT.duasTabelas;
  if (x.numero) return LAYOUT.divisoria;
  if (x.indicador_extra) return LAYOUT.DSX;
  if (x.tabelas) return LAYOUT.FC;
  if (x.figura && !x.cab) return LAYOUT.figuraLarga;
  if (x.blocos && !x.cab) return LAYOUT.blocos;
  if (x.caixas) return LAYOUT.DM;
  if (x.definicao) return LAYOUT.DS;
  if (x.figura) return LAYOUT.FA;
  if (x.parte === 'FP') return LAYOUT.FP;
  if (x.colW && x.colW.reduce((a, b) => a + b, 0) < 8) return LAYOUT.tabelaTexto;
  return LAYOUT.tabelaLarga;
}

N.ordem.forEach(id => {
  const x = N.slides[id];
  const s = d.S();
  layoutDe(id, x)(s, x);
  marca(s, id);
  // C-02: sem linha Fonte no slide; as fontes ficam só nas notas do apresentador.
  s.addNotes(`[${id}] ${x.titulo}\nRequisitos: ${x.requisito}\n` +
    (x.notas ? x.notas + '\n' : '') +
    (x.fonte_texto ? 'Textos tirados de: ' + x.fonte_texto.join('; ') + '\n' : '') +
    'Fontes: ' + x.fontes.join('; '));
});

d.p.writeFile({ fileName: SAIDA }).then(() => {
  if (SAIDA === PRINCIPAL) fs.writeFileSync(HASH, sha(PRINCIPAL) + '\n');
  if (SAIDA === PRINCIPAL) fs.copyFileSync(SAIDA, BASE);
  console.log(`${N.ordem.length} slides → ${path.relative(RAIZ, SAIDA)} (${N.versao})`);
});
