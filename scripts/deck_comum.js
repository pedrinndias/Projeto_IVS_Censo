/**
 * Os elementos visuais comuns aos decks do projeto, num lugar só.
 *
 * Por que este módulo existe
 * --------------------------
 * `gerar_deck_eda_central.js` e `gerar_deck_criterio_renda.js` carregam, cada um, a sua
 * própria cópia de `regua`, `titulo`, `tabela` e `numero`. Duas cópias já são o começo do
 * problema que o projeto resolveu em `src/ivs_censo/indicadores.py`: a primeira correção
 * que entrar em uma e não na outra faz os decks divergirem sem que ninguém perceba. Uma
 * terceira cópia, para o deck da análise fatorial, seria insistir no erro.
 *
 * Este módulo é usado **apenas** pelo gerador da fatorial. Os dois geradores antigos
 * continuam com as suas cópias, de propósito: migrá-los exige regerar os dois decks e
 * comparar o resultado com o que está publicado, e isso é trabalho à parte.
 *
 * Uso:
 *     const { criarDeck } = require('./deck_comum');
 *     const d = criarDeck({ titulo: '...', autor: '...' });
 *     const s = d.S();  d.titulo(s, 'Título', 'subtítulo');
 *     d.p.writeFile({ fileName: saida });
 *
 * A identidade é a mesma dos outros decks: folha de papel, serifada em tudo, um só acento
 * de carimbo, régua fina como único elemento decorativo. Sem preenchimento, sem canto
 * arredondado, sem cor de cabeçalho de tabela.
 */
let pptxgen;
try { pptxgen = require('pptxgenjs'); }
catch (e) {
  console.error('\n  pptxgenjs não encontrado:  npm install pptxgenjs\n');
  process.exit(1);
}

// ── Paleta enxuta, de papel: tinta quase preta, um acento de carimbo ─────────
const TINTA   = '1A1A18';
const CINZA   = '56534C';
const CINZA_C = '8B877E';
const REGUA   = 'C8C6C0';
const REGUA_F = 'E6E4DE';
const ACENTO  = '8C2F27';   // vermelho de correção — usado com parcimônia
const PAPEL   = 'FFFFFF';
const FONTE   = 'Cambria';  // serifada em tudo, como num artigo

const W = 13.33, H = 7.5, M = 0.85;

function criarDeck(meta) {
  const p = new pptxgen();
  p.layout = 'LAYOUT_WIDE';
  p.author = (meta && meta.autor) || 'Pedro Dias Soares';
  p.title = (meta && meta.titulo) || '';

  let nSlide = 0, nTabela = 0, nFigura = 0;

  /** Novo slide, com número no rodapé a partir do segundo. */
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

  /** Régua horizontal fina — o único elemento decorativo do deck. */
  function regua(s, y, espessura, cor, x, w) {
    s.addShape(p.ShapeType.line, { x: x === undefined ? M : x, y,
      w: w === undefined ? W - 2*M : w, h: 0,
      line: { color: cor || REGUA, width: espessura || 0.75 } });
  }

  /** Título de slide com subtítulo opcional; devolve o y onde o corpo pode começar. */
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

  /** Divisória de seção: numeral grande em acento, título ao lado. */
  function secao(s, num, t, sub) {
    s.addText(num, { x: M, y: 2.55, w: 1.2, h: 0.9, fontFace: FONTE, fontSize: 54,
      color: ACENTO, bold: true, margin: 0, valign: 'middle' });
    s.addText(t, { x: M + 1.25, y: 2.55, w: W - M - 2.1, h: 0.9, fontFace: FONTE,
      fontSize: 32, color: TINTA, bold: true, margin: 0, valign: 'middle' });
    regua(s, 3.58, 1.0, TINTA, M, W - 2*M);
    if (sub) s.addText(sub, { x: M + 1.25, y: 3.72, w: W - M - 2.6, h: 0.8,
      fontFace: FONTE, fontSize: 14, color: CINZA, margin: 0, italic: true });
  }

  /** Parágrafo com entrada em negrito. `marcado` põe a entrada no acento. */
  function bloco(s, x, y, w, entrada, texto, marcado, h) {
    if (marcado) regua(s, y - 0.06, 1.25, ACENTO, x, Math.min(w, 0.9));
    const alt = Math.min(h || 0.9, H - 0.72 - y);
    s.addText([
      { text: entrada + '  ', options: { bold: true, color: marcado ? ACENTO : TINTA } },
      { text: texto, options: { color: TINTA } },
    ], { x, y, w, h: alt, fontFace: FONTE, fontSize: 12.5, margin: 0, valign: 'top',
         lineSpacing: 16.5 });
  }

  /** Número em destaque, sem caixa: valor grande sobre filete, rótulo abaixo. */
  function numero(s, x, y, w, valor, rot, destaque) {
    regua(s, y, 1.0, destaque ? ACENTO : TINTA, x, w);
    s.addText(valor, { x, y: y + 0.08, w, h: 0.62, fontFace: FONTE, fontSize: 30,
      color: destaque ? ACENTO : TINTA, bold: true, margin: 0 });
    s.addText(rot, { x, y: y + 0.72, w, h: 0.42, fontFace: FONTE, fontSize: 10.5,
      color: CINZA, margin: 0 });
  }

  /** Tabela no padrão booktabs: três filetes, sem preenchimento nem cor de cabeçalho. */
  function tabela(s, cab, linhas, o) {
    o = Object.assign({ x: M, y: 2.0, w: W - 2*M, colW: null, fontSize: 11.5, rowH: 0.32 },
                      o || {});
    const head = cab.map(t => ({ text: t, options: { bold: true, color: TINTA,
      fontFace: FONTE, fontSize: o.fontSize - 0.5,
      border: [{ pt: 1.25, color: TINTA }, { type: 'none' },
               { pt: 0.75, color: TINTA }, { type: 'none' }] } }));
    const ult = linhas.length - 1;
    const corpo = linhas.map((ln, i) => ln.map(c => {
      const cel = (typeof c === 'object' && c !== null)
        ? { text: String(c.text), options: Object.assign({}, c.options) }
        : { text: String(c === null ? '—' : c), options: {} };
      cel.options = Object.assign({ fontFace: FONTE, fontSize: o.fontSize, color: TINTA,
        border: [{ type: 'none' }, { type: 'none' },
          i === ult ? { pt: 1.25, color: TINTA } : { type: 'none' }, { type: 'none' }] },
        cel.options);
      return cel;
    }));
    s.addTable([head, ...corpo], { x: o.x, y: o.y, w: o.w, colW: o.colW,
      autoPage: false, rowH: o.rowH, valign: 'middle' });
    return o.y + o.rowH * (linhas.length + 1);
  }

  /** Legenda de tabela — vai ACIMA dela, como em artigo. */
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

  /** Legenda de figura — vai ABAIXO dela. */
  function legendaFigura(s, y, texto, fonte) {
    nFigura++;
    s.addText([
      { text: `Figura ${nFigura} — `, options: { bold: true } },
      { text: texto + (fonte ? `  ${fonte}` : ''), options: {} },
    ], { x: M, y, w: W - 2*M, h: 0.34, fontFace: FONTE, fontSize: 10.5, color: CINZA,
         margin: 0 });
  }

  /** Anotação à mão: elipse vazada em torno de um valor, com nota puxada por uma linha. */
  function anotar(s, x, y, w, h, nota, nx, ny, nw) {
    s.addShape(p.ShapeType.ellipse, { x, y, w, h, fill: { type: 'none' },
      line: { color: ACENTO, width: 1.5 }, rotate: 355 });
    s.addShape(p.ShapeType.line, { x: x + w, y: y + h / 2, w: Math.max(nx - (x + w), 0.15),
      h: Math.abs(ny + 0.12 - (y + h / 2)), flipV: ny + 0.12 < y + h / 2,
      line: { color: ACENTO, width: 1.0 } });
    s.addText(nota, { x: nx, y: ny, w: nw || 3.0, h: 0.62, fontFace: FONTE, fontSize: 11,
      color: ACENTO, italic: true, margin: 0, valign: 'top' });
  }

  /** Procedência, no pé do slide: de qual arquivo saiu o que está sendo mostrado. */
  function procedencia(s, txt) {
    s.addText(txt, { x: M, y: H - 0.78, w: W - 2*M - 0.8, h: 0.36, fontFace: FONTE,
      fontSize: 9.5, color: CINZA_C, italic: true, margin: 0 });
  }

  /** Capa: folha de rosto, não banner. */
  function capa(s, kicker, tit, sub, rodape) {
    s.addText(kicker, { x: M, y: 1.35, w: W - 2*M, h: 0.34, fontFace: FONTE, fontSize: 11.5,
      color: CINZA, charSpacing: 2, margin: 0 });
    regua(s, 1.78, 1.0, TINTA);
    s.addText(tit, { x: M, y: 1.95, w: W - 2*M, h: 1.0, fontFace: FONTE, fontSize: 40,
      color: TINTA, bold: true, margin: 0 });
    s.addText(sub, { x: M, y: 3.05, w: 9.4, h: 1.1, fontFace: FONTE, fontSize: 14,
      color: CINZA, margin: 0, lineSpacing: 20 });
    regua(s, H - 1.35, 0.75);
    s.addText(rodape, { x: M, y: H - 1.2, w: W - 2*M, h: 0.5, fontFace: FONTE, fontSize: 11,
      color: CINZA, margin: 0 });
  }

  return { p, S, regua, titulo, secao, bloco, numero, tabela, legendaTabela,
           legendaFigura, anotar, procedencia, capa,
           cores: { TINTA, CINZA, CINZA_C, REGUA, REGUA_F, ACENTO, PAPEL, FONTE },
           geo: { W, H, M } };
}

module.exports = { criarDeck };
