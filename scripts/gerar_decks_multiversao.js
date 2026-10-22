/**
 * As 13 apresentações da fatorial multiversão: 12 de indicador e a final (Fases 5 a 7).
 *
 * Monta cada deck do zero a partir de `apresentacoes_multiversao/dados/<COD>.json`, gerado por
 * `scripts/dados_apresentacoes_multiversao.py` — nenhum número é digitado aqui. Cada slide de conteúdo tem
 * um visual à esquerda (gráfico ou tabela) e, à direita, a explicação: o que é, para que serve, como ler e
 * o que mostra. Padrão do relatório descritivo aprovado: ID no canto, fonte só nas notas, tabelas nativas.
 *
 * Uso:  node scripts/gerar_decks_multiversao.js <COD|todos|FIN> [--sobrescrever]
 *
 * Trava: se o Pedro editar um deck à mão, o gerador recusa sobrescrevê-lo (hash do último gerado em
 * dados/<COD>.sha256), salvo --sobrescrever.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const PASTA = path.join(RAIZ, 'apresentacoes_multiversao');
const CODIGOS = ['AGU', 'ESG', 'LIX', 'MOR', 'ANA', 'REN', 'PPI', 'CAN', 'BAN', 'MNC', 'IDO', 'CRI'];
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const LV = 7.3;          // largura do visual (pol.); a coluna de explicação fica com o resto

function gerar(cod) {
  const N = JSON.parse(fs.readFileSync(path.join(PASTA, 'dados', `${cod}.json`), 'utf8'));
  const saida = path.join(PASTA, N.arquivo);
  const hash = path.join(PASTA, 'dados', `${cod}.sha256`);
  if (fs.existsSync(saida) && !process.argv.includes('--sobrescrever') &&
      (!fs.existsSync(hash) || fs.readFileSync(hash, 'utf8').trim() !== sha(saida))) {
    console.error(`  ${N.arquivo} foi editado à mão depois da última geração. Use --sobrescrever para regerar.`);
    process.exitCode = 2;
    return Promise.resolve();
  }
  const d = criarDeck({ titulo: N.titulo });
  const { cores: C, geo: { W, H, M } } = d;
  const larg = W - 2 * M;

  const marca = (s, id) => s.addText(id, { x: W - M - 1.6, y: 0.16, w: 1.6, h: 0.3, fontFace: C.FONTE,
    fontSize: 11, color: C.ACENTO, bold: true, align: 'right', margin: 0 });

  /** Blocos "Entrada. texto" empilhados em (x, y, w), com o maior corpo que cabe até `fim`. */
  const textoAjustado = (s, blocos, x, y, w, fim, maior) => {
    const alt = (fs) => blocos.reduce((t, [e, tx]) => t + d.alturaTexto(`${e} ${tx}`, w, fs, fs * 1.3) + 0.12, 0);
    let fs = maior || 12;
    while (fs > 8 && y + alt(fs) > fim) fs -= 0.5;
    blocos.forEach(([e, tx]) => {
      const h = d.alturaTexto(`${e} ${tx}`, w, fs, fs * 1.3);
      const destaque = e === 'O que mostra.';
      s.addText([{ text: e + ' ', options: { bold: true, color: destaque ? C.ACENTO : C.TINTA } },
                 { text: tx, options: { color: C.TINTA } }],
                { x, y, w, h: h + 0.04, fontFace: C.FONTE, fontSize: fs, margin: 0, valign: 'top', lineSpacing: fs * 1.3 });
      y += h + 0.12;
    });
  };
  const encaixe = (fig, x, y, w, h) => {
    const png = fs.readFileSync(path.join(PASTA, fig));
    const pw = png.readUInt32BE(16), ph = png.readUInt32BE(20), e = Math.min(w / pw, h / ph);
    return { x: x + (w - pw * e) / 2, y, w: pw * e, h: ph * e };
  };
  /** Larguras das colunas, reduzidas na proporção para caber em `w`. */
  const colunas = (x, w) => {
    const cw = x.colW || x.cab.map(() => w / x.cab.length);
    const soma = cw.reduce((a, b) => a + b, 0);
    return soma > w ? cw.map((c) => c * w / soma) : cw;
  };
  const corpo = (n) => (n > 14 ? 8.5 : n > 9 ? 9.5 : 10.5);

  const LAYOUT = {
    capa(s, x) { d.capa(s, x.kicker, x.titulo, x.sub, x.rodape); },
    divisoria(s, x) { d.secao(s, x.numero, x.titulo, x.sub); },
    blocos(s, x) {
      const y = d.titulo(s, x.titulo) + 0.1;
      textoAjustado(s, x.blocos, M, y, larg - 1.0, H - 0.75, 13.5);
    },
    duas(s, x) {
      const y = d.titulo(s, x.titulo) + 0.05, k = Math.ceil(x.linhas.length / 2), w = larg / 2 - 0.3;
      const cw = colunas(x, w);
      d.tabelaAjustada(s, x.cab, x.linhas.slice(0, k), { x: M, y, colW: cw, fontSize: 8, rowH: 0.21 });
      d.tabelaAjustada(s, x.cab, x.linhas.slice(k), { x: M + w + 0.6, y, colW: cw, fontSize: 8, rowH: 0.21 });
    },
    matriz(s, x) {
      const y = d.titulo(s, x.titulo) + 0.05;
      const cw = [2.2, ...x.cab.slice(1).map(() => (larg - 2.2) / (x.cab.length - 1))];
      d.tabelaAjustada(s, x.cab.map((c, i) => (i ? c : '')), x.linhas, { x: M, y, colW: cw, fontSize: 7.5, rowH: 0.3 });
    },
    // o visual (gráfico ou tabela) à esquerda; a explicação à direita
    visual(s, x) {
      const y = d.titulo(s, x.titulo) + 0.08;
      if (x.figura) {
        const f = encaixe(x.figura, M, y, LV, H - y - 1.15);
        s.addImage({ path: path.join(PASTA, x.figura), ...f });
        d.legendaFigura(s, f.y + f.h + 0.06, x.legenda, null, M, LV);
      } else {
        d.tabelaAjustada(s, x.cab, x.linhas, { x: M, y, colW: colunas(x, LV), fontSize: corpo(x.linhas.length),
          rowH: x.linhas.length > 14 ? 0.22 : 0.27 });
      }
      const xe = M + LV + 0.3;
      s.addShape(d.p.ShapeType.line, { x: xe - 0.15, y, w: 0, h: H - y - 0.8, line: { color: C.REGUA, width: 0.75 } });
      textoAjustado(s, x.explica || [], xe, y, W - M - xe, H - 0.75, 11.5);
    },
  };
  const layoutDe = (x) => (x.capa ? 'capa' : x.numero ? 'divisoria' : x.blocos ? 'blocos' : x.duas ? 'duas'
    : x.matriz ? 'matriz' : 'visual');

  N.ordem.forEach((id) => {
    const x = N.slides[id];
    const s = d.S();
    LAYOUT[layoutDe(x)](s, x);
    marca(s, id);
    const exp = (x.explica || []).map(([e, t]) => `${e} ${t}`).join('\n');
    s.addNotes(`[${id}] ${x.titulo}\n${exp}\nFontes: ${(x.fontes || []).join('; ') || '—'}`);
  });
  fs.mkdirSync(path.dirname(saida), { recursive: true });
  return d.p.writeFile({ fileName: saida }).then(() => {
    fs.writeFileSync(hash, sha(saida) + '\n');
    console.log(`${N.ordem.length} slides → ${path.relative(RAIZ, saida)}`);
  });
}

const alvo = process.argv[2];
if (!alvo) { console.error('uso: node scripts/gerar_decks_multiversao.js <COD|todos|FIN> [--sobrescrever]'); process.exit(1); }
const lista = alvo === 'todos' ? CODIGOS : [alvo];
lista.reduce((p, c) => p.then(() => gerar(c)), Promise.resolve());
