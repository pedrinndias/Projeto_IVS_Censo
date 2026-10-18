#!/usr/bin/env node
/**
 * Deck para a orientadora: EDA unificada, EDA da versão final, análise fatorial e os dois
 * catálogos visuais.
 *
 *     ./.venv/bin/python scripts/dados_deck_orientadora.py
 *     node scripts/gerar_deck_orientadora.js
 *
 * Só diagrama: lê `analises_exploratorias/00_sintese/unificada/deck_orientadora.json`, em que
 * cada slide já vem com título, tabelas formatadas e textos com os números dos CSVs. Tipos:
 * capa · texto · secao · numeros · figura · tabela (paginada) · grade (12 miniaturas).
 */
const fs = require('fs');
const path = require('path');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const DADOS = path.join(RAIZ, 'analises_exploratorias', '00_sintese', 'unificada', 'deck_orientadora.json');

function main() {
  const dados = JSON.parse(fs.readFileSync(DADOS, 'utf8'));
  const d = criarDeck({ titulo: 'Análises exploratórias e análise fatorial — IVS Censo 2022' });
  const { W, H, M } = d.geo;
  const K = d.cores;
  const XR = M + 8.15 + 0.35, WR = W - M - XR, WE = 8.15, Y_FIM = H - 0.85;

  function tituloItem(s, t) {
    const larg = W - 2 * M;
    const cabe = f => Math.floor((larg - 0.2) * 72 / (f * 0.5));
    let f = t.length <= cabe(24) ? 24 : (t.length <= cabe(20) ? 20 : 0), y = 0.42, h = 0.62;
    if (!f) { f = Math.max(14, Math.min(20, Math.floor(2 * (larg - 0.2) * 72 / (0.5 * t.length)))); y = 0.2; h = 0.86; }
    s.addText(t, { x: M, y, w: larg, h, fontFace: K.FONTE, fontSize: f, color: K.TINTA, bold: true, margin: 0, valign: 'bottom' });
    d.regua(s, 1.14, 1.0, K.TINTA);
    return 1.36;
  }
  const altLateral = t => d.alturaTexto(t, WR, 12.5 * 0.5 / 0.45, 16.5) + 0.25;
  function lateral(s, y, comoLer, mostra) {
    const h1 = altLateral('Como ler   ' + comoLer);
    d.bloco(s, XR, y, WR, 'Como ler', comoLer, false, h1);
    d.bloco(s, XR, y + h1 + 0.3, WR, 'O que mostra', mostra, true, altLateral('O que mostra   ' + mostra));
  }
  function paginas(cab, linhas, colW, fsz, hDisp) {
    const alt = ln => Math.max(0.24, ...ln.map((c, j) => d.alturaTexto(String(c), colW[j] - 0.22, fsz, fsz * 1.22) + 0.1));
    const hCab = alt(cab), hs = linhas.map(alt);
    const quebrar = lim => {
      const pags = [];
      let atual = [], h = hCab;
      linhas.forEach((ln, i) => {
        if (atual.length && h + hs[i] > lim) { pags.push(atual); atual = []; h = hCab; }
        atual.push(ln); h += hs[i];
      });
      pags.push(atual);
      return pags;
    };
    let melhor = quebrar(hDisp);
    for (let lim = hDisp - 0.1; lim > hCab; lim -= 0.1) {
      const p = quebrar(lim);
      if (p.length > melhor.length) break;
      melhor = p;
    }
    return melhor;
  }
  const escala = (colW, total) => { const s = colW.reduce((a, b) => a + b, 0); return colW.map(w => w * Math.min(1, total / s)); };
  const pngTam = arq => { const b = fs.readFileSync(arq); return [b.readUInt32BE(16), b.readUInt32BE(20)]; };
  const jpgTam = arq => {            // dimensões de um JPEG: procura o marcador SOF
    const b = fs.readFileSync(arq);
    let i = 2;
    while (i < b.length) {
      const m = b[i + 1], len = b.readUInt16BE(i + 2);
      if (m >= 0xC0 && m <= 0xC3) return [b.readUInt16BE(i + 7), b.readUInt16BE(i + 5)];
      i += 2 + len;
    }
    return [4, 3];
  };
  const tam = arq => (arq.endsWith('.png') ? pngTam(arq) : jpgTam(arq));

  const mapa = [];          // especificação → slides, para o guia em PDF
  let nS = 0;
  const novo = () => { nS++; return d.S(); };
  dados.slides.forEach((sl, i) => {
    const antes = nS;
    let s, y;
    switch (sl.tipo) {
      case 'capa':
        s = novo();
        d.capa(s, sl.kicker, sl.titulo, sl.sub, sl.rodape);
        break;
      case 'secao':
        s = novo();
        d.secao(s, sl.num, sl.titulo, sl.sub);
        s.addNotes(sl.nota);
        break;
      case 'texto':
        s = novo();
        y = tituloItem(s, sl.titulo);
        s.addText(sl.itens.map(t => ({ text: t, options: { bullet: true, breakLine: true } })),
          { x: M, y: y + 0.1, w: W - 2 * M, h: Y_FIM - y - 0.15, fontFace: K.FONTE, fontSize: 14, color: K.TINTA,
            margin: 0, valign: 'top', paraSpaceAfter: 9 });
        if (sl.fonte) d.procedencia(s, sl.fonte);
        if (sl.nota) s.addNotes(sl.nota);
        break;
      case 'numeros': {
        s = novo();
        y = tituloItem(s, sl.titulo);
        const n = sl.nums.length, w = (W - 2 * M - 0.4 * (n - 1)) / n;
        sl.nums.forEach(([v, r], i) => d.numero(s, M + i * (w + 0.4), y + 0.3, w, v, r, i === n - 1));
        d.bloco(s, M, y + 1.95, W - 2 * M, 'Leitura', sl.texto, false, Y_FIM - y - 2.0);
        d.procedencia(s, sl.fonte);
        s.addNotes(sl.nota);
        break;
      }
      case 'figura': {
        s = novo();
        y = tituloItem(s, sl.titulo);
        const [pw, ph] = tam(sl.img);
        const e = Math.min(WE / pw, (Y_FIM - y - 0.05) / ph);
        s.addImage({ path: sl.img, x: M + (WE - pw * e) / 2, y, w: pw * e, h: ph * e });
        lateral(s, y + 0.05, sl.como_ler, sl.mostra);
        d.procedencia(s, sl.fonte);
        s.addNotes([sl.nota, '', 'Como ler: ' + sl.como_ler, 'O que mostra: ' + sl.mostra].join('\n'));
        break;
      }
      case 'tabela': {
        const largura = sl.larga ? W - 2 * M : WE;
        const colW = escala(sl.colW, largura);
        const pags = paginas(sl.cab, sl.linhas, colW, 10, Y_FIM - 1.36 - 0.05);
        pags.forEach((pg, k) => {
          s = novo();
          y = tituloItem(s, sl.titulo);
          d.tabelaAjustada(s, sl.cab, pg, { y, colW, fontSize: 10, rowH: 0.24 });
          if (!sl.larga) lateral(s, y + 0.05, sl.como_ler, sl.mostra);
          d.procedencia(s, sl.fonte + (pags.length > 1 ? `  ·  parte ${k + 1} de ${pags.length}` : ''));
          s.addNotes([sl.nota, '', 'Como ler: ' + sl.como_ler, 'O que mostra: ' + sl.mostra].join('\n'));
        });
        break;
      }
      case 'figura_larga': {
        s = novo();
        y = tituloItem(s, sl.titulo);
        const [pw, ph] = tam(sl.img);
        const hMax = Y_FIM - y - 0.6, wMax = W - 2 * M;
        const e = Math.min(wMax / pw, hMax / ph);
        s.addImage({ path: sl.img, x: M + (wMax - pw * e) / 2, y, w: pw * e, h: ph * e });
        s.addText([{ text: 'Como ler  ', options: { bold: true } }, { text: sl.como_ler + '  ' },
                   { text: 'O que mostra  ', options: { bold: true, color: K.ACENTO } }, { text: sl.mostra }],
          { x: M, y: Y_FIM - 0.55, w: wMax, h: 0.55, fontFace: K.FONTE, fontSize: 9.5, color: K.TINTA, margin: 0, valign: 'top' });
        d.procedencia(s, sl.fonte);
        s.addNotes([sl.nota, '', 'Como ler: ' + sl.como_ler, 'O que mostra: ' + sl.mostra].join('\n'));
        break;
      }
      case 'grade': {
        s = novo();
        s.addText(sl.titulo, { x: M, y: 0.3, w: W - 2 * M, h: 0.45, fontFace: K.FONTE, fontSize: 18, color: K.TINTA, bold: true, margin: 0 });
        d.regua(s, 0.8, 0.75, K.TINTA);
        const nc = sl.nc || 4, nl = sl.nl || 3, x0 = 0.5, y0 = 0.95, gx = 0.25, gy = 0.15;
        const cw = (W - 2 * x0 - gx * (nc - 1)) / nc, ch = (H - 0.85 - y0 - gy * (nl - 1)) / nl;
        const hRot = nc <= 3 ? 0.5 : 0.42, hImg = ch - hRot;
        sl.cels.forEach((c, i) => {
          const x = x0 + (i % nc) * (cw + gx), yy = y0 + Math.floor(i / nc) * (ch + gy);
          const [pw, ph] = tam(c.img);
          const e = Math.min(cw / pw, hImg / ph);
          s.addImage({ path: c.img, x: x + (cw - pw * e) / 2, y: yy, w: pw * e, h: ph * e });
          s.addText([{ text: c.rotulo, options: { bold: true, color: K.ACENTO, breakLine: true } },
                     { text: c.titulo.length > 78 ? c.titulo.slice(0, 77) + '…' : c.titulo, options: { color: K.CINZA } }],
            { x, y: yy + hImg + 0.02, w: cw, h: hRot, fontFace: K.FONTE, fontSize: nc <= 3 ? 9 : 7, margin: 0, valign: 'top' });
        });
        d.procedencia(s, sl.fonte);
        s.addNotes(sl.nota);
        break;
      }
      default:
        throw new Error('tipo de slide desconhecido: ' + sl.tipo);
    }
    mapa.push({ especificacao: i, slides: Array.from({ length: nS - antes }, (_, k) => antes + k + 1) });
  });
  fs.writeFileSync(DADOS.replace('.json', '_slides.json'), JSON.stringify(mapa));
  d.p.writeFile({ fileName: dados.saida }).then(() =>
    console.log(`${path.relative(RAIZ, dados.saida)}: ${nS} slides de ${dados.slides.length} especificações`));
}

main();
