/**
 * Os dois decks das 108 versões da análise fatorial (`versoes_fatorial/`): o principal e o
 * caderno de fichas. Montados sempre do zero a partir de `dados/numeros.json` — nenhum
 * número é digitado aqui. O ID vai no canto superior direito; a fonte, só nas notas.
 *
 * Os layouts copiam o estilo aprovado do relatório descritivo (`gerar_relatorio_descritivo.js`,
 * que não é importado: ele executa ao ser carregado).
 *
 * Trava: o Pedro pode editar os decks à mão. Um deck só é sobrescrito se for idêntico ao último
 * gerado (sha256 em dados/), ou com --sobrescrever. A cópia intocada do último gerado fica em
 * dados/ultimo_gerado_<deck>.pptx, para `comparar_edicoes_versoes.py`.
 *
 * Uso:  node scripts/gerar_versoes_fatorial.js [--so principal|caderno] [--sobrescrever]
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const PASTA = path.join(RAIZ, 'versoes_fatorial');
const N = JSON.parse(fs.readFileSync(path.join(PASTA, 'dados', 'numeros.json'), 'utf8'));
const ARQ = { principal: 'Versoes_Fatorial_Principal.pptx', caderno: 'Caderno_Fichas_108.pptx',
  parte: path.join('dados', 'parte_relatorio.pptx') };   // parte 5 do relatório descritivo (anexada por script)
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const arg = (k) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };

function montar(deck) {
  const d = criarDeck({ titulo: deck === 'principal' ? 'As 108 versões da análise fatorial' : 'Caderno de fichas — 108 versões' });
  const { cores: C, geo: { W, H, M } } = d;
  const marca = (s, id) => s.addText(id, { x: W - M - 1.6, y: 0.16, w: 1.6, h: 0.3, fontFace: C.FONTE,
    fontSize: 11, color: C.ACENTO, bold: true, align: 'right', margin: 0 });
  const rotulo = (s, x, y, w, t) => {
    s.addText(t, { x, y, w, h: 0.3, fontFace: C.FONTE, fontSize: 12, bold: true, color: C.TINTA, margin: 0 });
    return y + 0.34;
  };
  const paragrafo = (s, x, y, w, e, t, fs = 12.5) => {
    const h = d.alturaTexto(e + '  ' + t, w, fs, fs * 1.32) + 0.12;
    s.addText([{ text: e + '  ', options: { bold: true } }, { text: t }],
      { x, y, w, h, fontFace: C.FONTE, fontSize: fs, color: C.TINTA, margin: 0, valign: 'top' });
    return y + h + 0.12;
  };
  const L = {
    capa(s, x) { d.capa(s, x.kicker, x.titulo, x.sub, x.rodape); },
    divisoria(s, x) { d.secao(s, x.numero, x.titulo, x.sub); },
    blocos(s, x) {
      let y = d.titulo(s, x.titulo, x.sub) + 0.1;
      x.blocos.forEach(([e, t]) => { y = paragrafo(s, M, y, 10.5, e, t); });
    },
    tabela(s, x) {
      const y = d.titulo(s, x.titulo, x.sub) + 0.1;
      const n = x.linhas.length;
      const y2 = d.tabelaAjustada(s, x.cab, x.linhas, { x: M, y, colW: x.colW,
        fontSize: n > 12 ? 8.5 : (n > 8 ? 9.5 : 10.5), rowH: n > 12 ? 0.22 : 0.27 });
      if (x.frases) paragrafo(s, M, y2 + 0.22, 11.63, 'O que mostra.', x.frases.join(' '));
    },
    figura(s, x) {
      const y = d.titulo(s, x.titulo, x.sub) + 0.05;
      // encaixe calculado à mão: o 'contain' do pptxgenjs precisa do tamanho original da imagem
      const png = fs.readFileSync(path.join(PASTA, x.figura));
      const pw = png.readUInt32BE(16), ph = png.readUInt32BE(20);
      const esc = Math.min(11.63 / pw, 4.0 / ph);
      s.addImage({ path: path.join(PASTA, x.figura), x: M + (11.63 - pw * esc) / 2, y, w: pw * esc, h: ph * esc });
      d.legendaFigura(s, y + 4.05, x.legenda, null);
      if (x.frases) paragrafo(s, M, y + 4.45, 11.63, 'O que mostra.', x.frases.join(' '));
    },
    ficha(s, x) {
      s.addText(x.selo, { x: M, y: 0.16, w: 9.5, h: 0.3, fontFace: C.FONTE, fontSize: 10.5, bold: true,
        color: x.passa ? C.TINTA : C.ACENTO, charSpacing: 1.5, margin: 0 });
      const y = d.titulo(s, x.titulo, x.sub) + 0.05;
      let y1 = rotulo(s, M, y, 3.2, 'A versão');
      d.tabelaAjustada(s, ['', ''], x.versao, { x: M, y: y1 - 0.3, colW: [1.75, 1.45], fontSize: 9, rowH: 0.24 });
      let y2 = rotulo(s, 4.2, y, 3.7, 'Adequação');
      d.tabelaAjustada(s, ['', ''], x.adequacao, { x: 4.2, y: y2 - 0.3, colW: [2.3, 1.45], fontSize: 9, rowH: 0.24 });
      let y3 = rotulo(s, 8.1, y, 4.38, 'Cargas e pesos (promax, matriz padrão)');
      const fim = d.tabelaAjustada(s, x.cab_cargas, x.cargas, { x: 8.1, y: y3, colW: [1.63, 0.58, 0.58, 0.95, 0.64],
        fontSize: x.cargas.length > 8 ? 8 : 8.5, rowH: 0.22 });
      const yb = Math.max(fim, y2 + 2.75) + 0.15;
      rotulo(s, M, yb, 6, 'Validação e faixas');
      const yv = d.tabelaAjustada(s, x.cab_valid, x.valid, { x: M, y: yb + 0.34,
        colW: [1.25, 1.25, 1.6, 1.15, 1.15, 1.15, 1.35, 1.35, 1.38], fontSize: 8.5, rowH: 0.24 });
      paragrafo(s, M, yv + 0.12, 11.63, 'O que mostra.', x.frases.join(' '), 11);
    },
  };
  const layout = (id, x) => x.kicker ? L.capa : x.numero ? L.divisoria : x.cargas ? L.ficha : x.figura ? L.figura
    : x.cab ? L.tabela : L.blocos;
  N[deck].ordem.forEach(id => {
    const x = N[deck].slides[id];
    const s = d.S();
    layout(id, x)(s, x);
    marca(s, id);
    s.addNotes(`[${id}] ${x.titulo}\n${x.notas || ''}`);
  });
  return d;
}

const decks = arg('--so') ? [arg('--so')] : ['principal', 'caderno', 'parte'];
decks.forEach(deck => {
  const saida = path.join(PASTA, ARQ[deck]);
  const hash = path.join(PASTA, 'dados', `gerado_${deck}.sha256`);
  const base = path.join(PASTA, 'dados', `ultimo_gerado_${deck}.pptx`);
  if (fs.existsSync(saida) && !process.argv.includes('--sobrescrever')) {
    const gravado = fs.existsSync(hash) ? fs.readFileSync(hash, 'utf8').trim() : '';
    if (sha(saida) !== gravado) {
      console.error(`RECUSADO: ${ARQ[deck]} foi editado à mão. Rode comparar_edicoes_versoes.py e use --sobrescrever.`);
      process.exitCode = 2;
      return;
    }
  }
  montar(deck).p.writeFile({ fileName: saida }).then(() => {
    fs.writeFileSync(hash, sha(saida) + '\n');
    fs.copyFileSync(saida, base);
    console.log(`${deck}: ${N[deck].ordem.length} slides → ${path.relative(RAIZ, saida)} (${N.versao})`);
  });
});
