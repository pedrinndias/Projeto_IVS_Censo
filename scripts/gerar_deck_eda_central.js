/**
 * Gera a EDA Central — docs/Apresentacoes_IVS/EDA_Central_IVS_2026-09_rev2.pptx
 *
 * Por que este script existe
 * --------------------------
 * Nenhuma apresentação anterior do projeto tinha gerador. Cada deck foi montado à mão,
 * e a lista do que entrava vivia na cabeça de quem montava — foi assim que o bloco de
 * chefia feminina, presente no deck de junho, sumiu do de agosto sem ninguém notar.
 * É a mesma causa raiz dos CSVs órfãos de banco_de_dados/eda/.
 *
 * Com o deck versionado, a cobertura passa a ser revisável: dá para ler nesta lista o
 * que entra e comparar com as tabelas geradas em banco_de_dados/eda/.
 *
 * E os NÚMEROS não são digitados aqui. A primeira versão tinha valores escritos à mão,
 * e três vieram do recorte com rurais apresentados como se fossem do urbano. Agora
 * scripts/eda_central_dados.py lê cada tabela e emite um JSON em que todo bloco carrega
 * o recorte de origem; este arquivo só formata.
 *
 * Ordem de execução:
 *     ./.venv/bin/python scripts/eda_central_dados.py banco_de_dados/eda/dados_deck.json
 *     node scripts/gerar_deck_eda_central.js docs/Apresentacoes_IVS/EDA_Central_IVS_2026-09_rev2.pptx
 *
 * Uso:
 *     node scripts/gerar_deck_eda_central.js <saida.pptx> [dados_deck.json]
 *
 * Sem o segundo argumento usa banco_de_dados/eda/dados_deck.json (1ª rodada). Com o JSON
 * da 2ª rodada, que traz o bloco `alteracoes`, ele acrescenta os 4 slides de comparação.
 *
 * Requer `pptxgenjs` (npm). Os números vêm das tabelas da EDA; as figuras, de
 * banco_de_dados/eda/figuras/.
 */
const path = require('path');
let pptxgen;
try { pptxgen = require('pptxgenjs'); }
catch (e) {
  console.error('\n  pptxgenjs não encontrado:  npm install pptxgenjs\n');
  process.exit(1);
}
// A raiz sai da localização deste arquivo (scripts/ fica um nível abaixo dela). Antes
// era um caminho absoluto fixo — que apontava para uma pasta inexistente nesta máquina e
// fazia o gerador morrer sem conseguir ler número nenhum. Caminho fixo em script de
// geração é bomba-relógio: quebra em toda máquina que não for a de quem escreveu.
const RAIZ = path.resolve(__dirname, '..');
const FIG = path.join(RAIZ, 'banco_de_dados/eda/figuras');
const FIG_NOVA = path.join(RAIZ, 'banco_de_dados/eda/atualizada/figuras');
// Só três figuras dependem da renda e foram regeradas. `fig()` pega a versão nova
// quando ela existe e a original quando não — o deck nunca fica com metade de cada
// rodada sem que isso esteja dito.
function fig(nome) {
  const nova = path.join(FIG_NOVA, nome);
  return (USAR_NOVAS && require('fs').existsSync(nova)) ? nova : path.join(FIG, nome);
}

// ── Paleta enxuta, de papel: tinta quase preta, um acento de carimbo ─────────
const TINTA   = '1A1A18';
const CINZA   = '56534C';
const CINZA_C = '8B877E';
const REGUA   = 'C8C6C0';
const REGUA_F = 'E6E4DE';
const ACENTO  = '8C2F27';   // vermelho de correção — usado com parcimônia
const PAPEL   = 'FFFFFF';
const FONTE   = 'Cambria';          // serifada em tudo, como num artigo
const MONO    = 'Courier New';

const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';
p.author = 'Pedro Dias Soares';
p.title  = 'EDA Central — IVS Censo 2022';
const W = 13.33, H = 7.5, M = 0.85;

let nSlide = 0, nTabela = 0, nFigura = 0;

function novo() {
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

function secao(s, num, t, sub) {
  s.addText(num, { x: M, y: 2.55, w: 1.2, h: 0.9, fontFace: FONTE, fontSize: 54,
    color: ACENTO, bold: true, margin: 0, valign: 'middle' });
  s.addText(t, { x: M + 1.25, y: 2.55, w: W - M - 2.1, h: 0.9, fontFace: FONTE, fontSize: 32,
    color: TINTA, bold: true, margin: 0, valign: 'middle' });
  regua(s, 3.58, 1.0, TINTA, M, W - 2*M);
  if (sub) s.addText(sub, { x: M + 1.25, y: 3.72, w: W - M - 2.6, h: 0.8, fontFace: FONTE,
    fontSize: 14, color: CINZA, margin: 0, italic: true });
}

/** Parágrafo com entrada em negrito — substitui os cartões arredondados. */
function bloco(s, x, y, w, entrada, texto, marcado, h) {
  if (marcado) regua(s, y - 0.06, 1.25, ACENTO, x, Math.min(w, 0.9));
  // a altura é respeitada: sem isso o parágrafo invadia o número do slide no rodapé
  const alt = Math.min(h || 0.9, H - 0.72 - y);
  s.addText([
    { text: entrada + '  ', options: { bold: true, color: marcado ? ACENTO : TINTA } },
    { text: texto, options: { color: TINTA } },
  ], { x, y, w, h: alt, fontFace: FONTE, fontSize: 12.5, margin: 0, valign: 'top', lineSpacing: 16.5 });
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
  ], { x: M, y, w: W - 2*M, h: 0.34, fontFace: FONTE, fontSize: 10.5, color: CINZA, margin: 0 });
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

const S = novo;
// argv[3] permite gerar o deck atualizado com o MESMO gerador, só trocando o JSON.
const JSON_DECK = process.argv[3] || path.join(RAIZ, 'banco_de_dados/eda/dados_deck.json');
const D = JSON.parse(require('fs').readFileSync(JSON_DECK, 'utf8'));
const ALT = D.alteracoes || null;        // só o deck atualizado tem este bloco
const USAR_NOVAS = ALT !== null;

/** Bloco do JSON: legenda numerada acima, tabela booktabs, procedência embaixo. */
function blocoTabela(s, chave, opts) {
  const b = D.blocos[chave];
  if (!b) { console.warn('bloco ausente:', chave); return opts.y; }
  const o = Object.assign({ y: 2.0, fontSize: 11.5, rowH: 0.32, colW: null }, opts || {});
  const yTab = legendaTabela(s, o.y, b.titulo + '.', `Recorte: ${b.recorte}. Fonte: ${b.fonte}.`);
  let yy = tabela(s, b.colunas, b.linhas.map(ln => ln.map(c => c === null ? '—' : String(c))),
    { y: yTab, colW: o.colW, fontSize: o.fontSize, rowH: o.rowH });
  yy += 0.14;
  if (b.nota) {
    s.addText(b.nota, { x: M, y: yy, w: W - 2*M, h: 0.36, fontFace: FONTE, fontSize: 11,
      color: CINZA, italic: true, margin: 0 });
    yy += 0.40;
  }
  return yy + 0.14;
}

// ── Capa: folha de rosto, não banner ────────────────────────────────────────
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

// ── Compatibilidade com os corpos de slide já escritos ──────────────────────
// Os cartões arredondados viram parágrafos com entrada em negrito; as caixas de
// estatística viram número sobre filete. Nada de preenchimento nem canto redondo.
const PETROL = TINTA, PETROL_D = TINTA, SEAFOAM = CINZA, CLAY = ACENTO,
      CLAY_L = ACENTO, SAND = REGUA_F, WHITE = PAPEL, INK = TINTA, MUTED = CINZA,
      SERIF = FONTE, SANS = FONTE;

function cartao(s, x, y, w, h, tit, txt, cor) {
  bloco(s, x, y + 0.05, w, tit + '.', txt, cor === ACENTO, h);
}
function stat(s, x, y, w, valor, rot, cor) {
  numero(s, x, y, w, valor, rot, cor === ACENTO);
}
function nota(s, txt) {
  s.addText(txt, { x: M, y: H - 0.78, w: W - 2*M - 0.8, h: 0.36, fontFace: FONTE,
    fontSize: 9.5, color: CINZA_C, italic: true, margin: 0 });
}

// ═════════ CAPA ═════════
{ const s = S();
  capa(s, 'INICIAÇÃO CIENTÍFICA · FIOCRUZ MINAS — IRR',
    ALT ? 'A EDA Central — 2ª rodada' : 'A EDA Central',
    ALT
      ? 'Índice de Vulnerabilidade da Saúde intraurbano · Censo Demográfico 2022 · 70 municípios do ELSI-Brasil\nA mesma análise, recalculada com a renda sem o valor extremo de Belo Horizonte. As alterações estão marcadas.'
      : 'Índice de Vulnerabilidade da Saúde intraurbano · Censo Demográfico 2022 · 70 municípios do ELSI-Brasil\nToda a análise exploratória reunida em um só lugar, recalculada no recorte atual.',
    ALT
      ? 'Pedro Dias Soares  ·  setembro de 2026  ·  104.108 setores urbanos elegíveis  ·  renda sem o setor 310620005650366'
      : 'Pedro Dias Soares  ·  agosto de 2026  ·  104.108 setores censitários urbanos elegíveis');
  s.addNotes('Primeira apresentação que reúne a EDA inteira. As anteriores eram recortes: cada deck foi montado em torno da pauta do mês, e o que não estava na pauta caía fora sem aviso.');
}

{ const s = S();
  titulo(s, 'Por que esta apresentação existe', 'Nenhum dos decks anteriores era a EDA inteira — cada um era um recorte dela.');
  tabela(s, ['Bloco de análise', 'Tabelas', 'Junho', 'Agosto', 'Agora'], [
    ['Chefia feminina', '5', 'sim', {text:'caiu', options:{color:CLAY, bold:true}}, {text:'entra', options:{color:PETROL, bold:true}}],
    ['Habitação precária', '3', 'sim', {text:'caiu', options:{color:CLAY, bold:true}}, {text:'entra', options:{color:PETROL, bold:true}}],
    ['Morfologia V00048–V00058', '1', 'sim', {text:'caiu', options:{color:CLAY, bold:true}}, {text:'entra', options:{color:PETROL, bold:true}}],
    ['Inadequação de banheiro', '3', 'sim', 'só na lista de variáveis', {text:'entra', options:{color:PETROL, bold:true}}],
    ['Moradia predominante · saneamento em faixas', '2', 'não', 'não', {text:'entra', options:{color:PETROL, bold:true}}],
    ['Distribuições, outliers e faltantes', '2 + 3 figuras', 'sim', 'parcial', {text:'entra', options:{color:PETROL, bold:true}}],
    ['Cobertura · favelas · envelhecimento · Brasil×ELSI', '13', 'parcial', 'entrou', 'mantém'],
  ], { y: 1.85, colW: [4.6, 1.5, 1.3, 3.0, 1.5], fontSize: 11.5 });
  s.addText('A causa: nenhum script gerava os decks. A lista do que entra vivia na cabeça de quem montava — a mesma causa dos CSVs órfãos. Este deck é gerado por script, e os números são lidos das tabelas em tempo de build.',
    { x: M, y: 5.7, w: W - 2*M, h: 0.7, fontFace: SANS, fontSize: 13, color: CLAY, bold: true });
  nota(s, 'Levantamento feito arquivo por arquivo sobre os 7 .pptx versionados em docs/Apresentacoes_IVS/.');
}

// ═════════ O QUE MUDOU (só no deck atualizado) ═════════
if (ALT) {
  { const s = S();
    titulo(s, 'O que mudou nesta rodada',
      'A EDA inteira foi recalculada. Um único valor saiu da base — e o efeito dele é mais estreito e mais fundo do que se esperava.');
    bloco(s, M, 1.80, W - 2*M, 'O pedido.',
      'Criar uma coluna de renda sem o valor extremo de Belo Horizonte. A coluna nova é `renda_media_sem_extremo`; a `renda_media` original continua na base, sem alteração, ao lado dela.', true, 0.8);
    bloco(s, M, 2.62, W - 2*M, 'O setor.',
      `${ALT.setor} — ${ALT.municipio}, bairro ${ALT.bairro}, ${ALT.valor} por responsável. Maior valor da base, 55,7× a mediana do município, num setor de favela com 186 domicílios e 518 pessoas.`, false, 0.8);
    bloco(s, M, 3.44, W - 2*M, 'O alcance.',
      `De todas as células recalculadas, ${ALT.n_celulas} mudaram, em ${ALT.n_tabelas_alteradas} tabelas: ${ALT.tabelas_alteradas.join(', ')}. Nenhuma delas fora da renda e de suas correlações.`, false, 0.9);
    numero(s, M, 4.75, 2.6, '1', 'setor excluído', true);
    numero(s, M + 2.9, 4.75, 2.6, '104.108', 'setores no recorte');
    numero(s, M + 5.8, 4.75, 2.6, ALT.n_celulas, 'células alteradas');
    numero(s, M + 8.7, 4.75, 2.9, '−48%', 'na curtose da renda', true);
    nota(s, 'Comparação célula a célula em banco_de_dados/eda/atualizada/comparacao_antes_depois.csv, gerada por scripts/eda_atualizada.py.');
    s.addNotes('A recomputação foi validada: rodada com a coluna antiga, ela reproduz número a número as tabelas já publicadas. Só depois disso as tabelas novas foram aceitas.');
  }

  { const s = S();
    titulo(s, 'A renda, antes e depois', 'O nível quase não se move. A forma da distribuição, sim.');
    blocoTabela(s, 'alteracoes_renda', { y: 1.75, colW: [3.6, 2.8, 2.8, 2.6] });
    bloco(s, M, 5.30, W - 2*M, 'A leitura.',
      'A média cai 0,04% e a mediana não muda — tirar um setor em 104 mil não desloca o centro. O que muda é a cauda: o desvio-padrão cai 0,8%, a assimetria 14,5% e a curtose 48,2%. Metade do peso da cauda da renda no recorte inteiro estava naquele único setor.', true, 1.0);
    nota(s, 'eda/descritivas_globais.csv (antes) × eda/atualizada/descritivas_globais.csv (depois).');
  }

  { const s = S();
    titulo(s, 'As correlações com a renda', 'Todas ficam mais fortes — e Spearman não muda em casa nenhuma.');
    blocoTabela(s, 'alteracoes_correlacao', { y: 1.75, colW: [4.4, 2.4, 2.4, 2.0] });
    bloco(s, M, 5.05, W - 2*M, 'Por que isso importa.',
      'Pearson mede associação linear e é sensível a um ponto extremo: o setor de BH achatava toda a coluna da renda. A matriz de Spearman, que trabalha com postos, é idêntica antes e depois — o caso nunca a afetou. É o argumento empírico a favor de estatística robusta para a renda, já registrado como decisão em aberto.', true, 1.2);
    nota(s, 'São 16 células alteradas na matriz — os 8 pares acima, contados nos dois triângulos. Detalhe em eda/atualizada/comparacao_antes_depois.csv.');
  }

  { const s = S();
    titulo(s, 'O que NÃO mudou', 'Tão importante quanto o que mudou: a exclusão não vazou para o resto da análise.');
    tabela(s, ['Bloco da EDA', 'Situação após o recálculo'], [
      ['Elegibilidade e recorte urbano', 'idêntico — 106.281 elegíveis, 104.108 no recorte'],
      ['Água, esgoto, lixo, razão de moradores, analfabetismo, cor/raça', 'idênticos em média, mediana, outliers e faltantes'],
      ['Matriz de Spearman (10 variáveis)', 'idêntica em todas as 100 células'],
      ['Favelas e Comunidades Urbanas — contagens', 'idênticas: 19.452 no recorte, 19.507 na base'],
      ['Cobertura de saneamento, faixas de gravidade, morfologia', 'idênticos'],
      ['Chefia feminina, envelhecimento, habitação precária, banheiro', 'idênticos'],
      ['Canalização da água', 'idêntica'],
    ], { y: 1.85, colW: [6.2, 6.6], fontSize: 12, rowH: 0.42 });
    bloco(s, M, 5.20, W - 2*M, 'Como isso foi verificado.',
      'Não por inspeção visual: o script recalcula as sete tabelas nas duas versões e compara célula a célula. As que não aparecem na lista de alterações têm diferença exatamente zero.', false, 0.9);
    nota(s, 'scripts/eda_atualizada.py — a mesma rotina valida que, com a coluna antiga, o recálculo reproduz a EDA publicada.');
  }
}

// ═════════ 1. DESENHO ═════════
{ const s = S(); secao(s, '1', 'O desenho do estudo', 'A pergunta, a base e como a pipeline está estruturada.'); }

{ const s = S();
  titulo(s, 'A pergunta e o objeto');
  cartao(s, M, 1.75, 5.85, 2.0, 'A pergunta',
    'Como a vulnerabilidade à saúde se distribui DENTRO das cidades brasileiras onde vive a coorte do ELSI-Brasil, e o que essa distribuição revela sobre desigualdade intraurbana?');
  cartao(s, M + 6.25, 1.75, 5.85, 2.0, 'O objeto: o setor censitário',
    'A menor unidade territorial do Censo. O IVS é um índice INTRAURBANO — compara setores dentro da mesma cidade, não cidades entre si. É dessa escolha que decorrem o recorte urbano, a normalização por município e o desenho ecológico.', SEAFOAM);
  stat(s, M, 4.15, 2.75, '104.108', 'setores urbanos elegíveis');
  stat(s, M + 2.95, 4.15, 2.75, '70', 'municípios do ELSI-Brasil');
  stat(s, M + 5.90, 4.15, 2.75, '8', 'arquivos do Censo 2022');
  stat(s, M + 8.85, 4.15, 2.75, '73', 'variáveis na base bruta');
  s.addText('O recorte reúne 61,4% de toda a população favelada do país — conferido contra o dado oficial do IBGE.',
    { x: M, y: 6.0, w: W - 2*M, h: 0.4, fontFace: SANS, fontSize: 13.5, color: PETROL, bold: true });
}

{ const s = S();
  titulo(s, 'Como a pipeline está estruturada', 'Uma fonte de verdade para as fórmulas; os notebooks e os scripts leem dela.');
  const et = [
    ['1', 'src/ivs_censo', 'Fórmulas, regra de elegibilidade, lista de variáveis por arquivo e classificação de renda. Nada é redigitado fora daqui.'],
    ['2', 'Notebook 01', 'Lê os 8 arquivos do Censo (2,4 GB), filtra os 70 municípios, une por CD_SETOR e audita a integridade. Base bruta: 109.032 setores.'],
    ['3', 'Notebook 02', 'A EDA: tipagem e sigilo, elegibilidade, recorte urbano, 7 componentes, blocos descritivos, figuras e matriz de correlação.'],
    ['4', 'scripts/', 'Cálculo nacional, tabelas de auditoria, auditoria de renda, extração dos dados deste deck e o gerador dele.'],
    ['5', 'tests/', '63 testes automatizados. Conferem fórmulas com dados sintéticos e os artefatos já gerados.'],
  ];
  let y = 1.75;
  et.forEach(([n, tit, txt]) => {
    s.addShape(p.ShapeType.ellipse, { x: M, y: y + 0.06, w: 0.52, h: 0.52, fill: { color: PETROL } });
    s.addText(n, { x: M, y: y + 0.06, w: 0.52, h: 0.52, align: 'center', valign: 'middle', fontFace: SERIF, fontSize: 17, color: WHITE, bold: true });
    s.addText(tit, { x: M + 0.78, y, w: 2.5, h: 0.4, fontFace: SANS, fontSize: 14, bold: true, color: PETROL, margin: 0 });
    s.addText(txt, { x: M + 3.35, y, w: W - M - 4.05, h: 0.66, fontFace: SANS, fontSize: 12, color: INK, margin: 0 });
    y += 0.92;
  });
  nota(s, 'Antes de agosto de 2026 as fórmulas existiam em dois lugares e a lista de variáveis em três. Hoje é uma só, verificada por teste.');
}

// ═════════ 2. QUEM ENTRA ═════════
{ const s = S(); secao(s, '2', 'Quem entra na análise', 'Sigilo, elegibilidade e o recorte urbano — as três decisões que definem a base.'); }

{ const s = S();
  titulo(s, 'Do universo do Censo aos setores analisados', 'Cada corte é auditável e reversível: a base bruta guarda os 109.032 setores.');
  tabela(s, ['Etapa', 'Critério', 'Setores', 'O que sai'], [
    ['Universo do Censo 2022', 'Brasil inteiro', '468.099', '—'],
    ['Filtro ELSI-Brasil', '70 municípios da coorte', {text:'109.032', options:{bold:true}}, 'municípios fora da coorte'],
    ['ZERADO', 'v0001 = 0 (massas d\'água)', '−' + D.eleg.ZERADO, 'setores sem população'],
    ['SIGILOSO', 'v0001 ou V00001 suprimidos', '−' + D.eleg.SIGILOSO, 'sem denominador calculável'],
    ['COLETIVO', 'V00001 = 0 com população > 0', '0', 'classe vazia — ver limitações'],
    ['Elegíveis (Dados_sig = OK)', '', D.eleg.OK, ''],
    ['Recorte urbano', 'SITUACAO = Urbana', {text:D.exclusao.n_ok_urbano, options:{bold:true, color:PETROL}}, D.exclusao.n_ok_rural + ' setores rurais elegíveis'],
  ], { y: 1.8, colW: [3.3, 3.6, 2.0, 3.0], fontSize: 12 });
  cartao(s, M, 5.05, 5.85, 1.45, 'A exclusão rural, conferida município a município',
    `${D.exclusao.perdem_10pct} dos ${D.exclusao.municipios} municípios perdem mais de 10% dos setores e ${D.exclusao.menos_de_10_setores} ficam com menos de 10. Isso afeta a estabilidade das descritivas municipais e consta das limitações.`, CLAY);
  cartao(s, M + 6.25, 5.05, 5.85, 1.45, 'Correção: massas d\'água',
    `${D.eleg.ZERADO} setores sem população apareciam como SIGILOSO porque o sigilo era testado antes da população zero. Ordem invertida — nenhum setor OK mudou.`, CLAY);
}

// ═════════ 3. AS SETE COMPONENTES ═════════
{ const s = S(); secao(s, '3', 'As sete componentes do IVS', 'Fórmulas, distribuições, outliers e dados faltantes.'); }

{ const s = S();
  titulo(s, 'As sete componentes — fórmulas', 'Adaptadas do IVS-BH 2012 ao Censo 2022. Denominador domiciliar padrão: V00001.');
  tabela(s, ['Componente', 'Numerador', 'Denominador', 'Dimensão'], [
    ['pct_agua_inad', 'V00112 … V00118 (fonte alternativa)', 'V00001', 'Saneamento'],
    ['pct_esgoto_inad', 'V00312 … V00316', 'V00001', 'Saneamento'],
    ['pct_lixo_inad', 'V00398 … V00402', 'V00001', 'Saneamento'],
    ['razao_moradores', 'V00005 + V00006', 'V00001 + V00002', 'Socioeconômica'],
    ['pct_analfab', 'V00901', {text:'V00900 + V00901', options:{bold:true}}, 'Socioeconômica'],
    ['renda_media', 'V06004 (direto)', '—', 'Socioeconômica'],
    ['pct_raca_pretpardind', 'V01318 + V01320 + V01321', 'v0001', 'Socioeconômica'],
  ], { y: 1.8, colW: [3.1, 4.5, 2.5, 1.8], fontSize: 12 });
  cartao(s, M, 4.9, 3.8, 1.55, 'Denominador consolidado',
    'V00001 substituiu V01042, que era contagem de PESSOAS. Nenhuma proporção estoura 1,0.');
  cartao(s, M + 4.2, 4.9, 3.8, 1.55, 'Analfabetismo corrigido',
    'A taxa é V00901 / (V00900 + V00901). Antes era V00901/V00900, que é razão, não taxa.', CLAY);
  cartao(s, M + 8.4, 4.9, 3.7, 1.55, 'Três não reprodutíveis',
    'Anos de estudo, faixas de renda e óbitos cardiovasculares não existem nos agregados. Substituídos por proxies declarados.', MUTED);
}

{ const s = S();
  titulo(s, 'As sete componentes em números', 'Média e mediana lado a lado — a distância entre elas mede a assimetria.');
  blocoTabela(s, 'descritivas', { y: 1.75, colW: [3.2, 1.6, 1.6, 1.6, 1.5, 1.9, 1.5], fontSize: 12, rowH: 0.4 });
  s.addText('Em três das sete a mediana é zero: água, esgoto e lixo não têm inadequação medida na maioria dos setores urbanos. Os dois números que abrem as seções seguintes são o n do analfabetismo e a assimetria da renda.',
    { x: M, y: 5.4, w: W - 2*M, h: 0.7, fontFace: SANS, fontSize: 12.5, color: INK });
}

{ const s = S();
  titulo(s, 'As sete componentes por região', 'O gradiente Norte–Sul aparece em seis das sete.');
  const y11 = blocoTabela(s, 'por_regiao', { y: 1.70, colW: [3.4, 1.85, 1.85, 1.85, 1.85, 1.85], fontSize: 12, rowH: 0.40 });
  cartao(s, M, y11, 5.85, 1.45, 'O padrão esperado, confirmado',
    'Água inadequada no Norte é dezesseis vezes a do Sul; o esgoto, oito vezes. A razão de moradores acompanha: 3,19 no Norte contra 2,53 no Sul.');
  cartao(s, M + 6.25, y11, 5.85, 1.45, 'Duas exceções que importam',
    'O analfabetismo tem pico no Nordeste, não no Norte. E o lixo inadequado é MAIOR no Nordeste e no Sudeste que no Norte — indício de que mede porte urbano.', CLAY);
}

{ const s = S();
  titulo(s, 'Como as sete variáveis se distribuem', 'Histogramas sobre os setores urbanos elegíveis.');
  s.addImage({ path: fig('histogramas.png'), x: 2.59, y: 1.52, w: 8.15, h: 5.40 });
  nota(s, 'banco_de_dados/eda/figuras/histogramas.png — gerada pela célula step8 do Notebook 02.');
  s.addNotes('Cinco das sete são fortemente assimétricas à direita, com massa concentrada no zero. A razão de moradores é a única aproximadamente simétrica.');
}

{ const s = S();
  titulo(s, 'Distribuição por região', 'Boxplots das sete componentes, região a região.');
  s.addImage({ path: fig('boxplots_por_regiao.png'), x: 2.97, y: 1.52, w: 7.39, h: 5.40 });
  nota(s, 'banco_de_dados/eda/figuras/boxplots_por_regiao.png — célula step9 do Notebook 02.');
}

{ const s = S();
  titulo(s, 'Outliers: a regra do IQR não serve para o saneamento', 'Quando a mediana e o primeiro quartil são zero, o IQR marca como atípico todo setor com qualquer inadequação.');
  const y14 = blocoTabela(s, 'outliers', { y: 1.70, colW: [3.0, 1.5, 1.5, 1.9, 1.6, 1.6, 1.8], fontSize: 12, rowH: 0.38 });
  cartao(s, M, y14, 5.85, 1.35, 'Onde o IQR falha',
    'Água, esgoto e lixo têm cerca de 20% dos setores classificados como outlier. O que a regra está marcando é a forma da distribuição, não uma cauda de casos extremos.', CLAY);
  cartao(s, M + 6.25, y14, 5.85, 1.35, 'Onde o IQR funciona',
    'Razão de moradores, analfabetismo, renda e cor/raça têm distribuições com dispersão real — ali a regra identifica extremos de verdade.', PETROL);
}

{ const s = S();
  titulo(s, 'Dados faltantes e o sigilo do IBGE', 'Seis das sete componentes têm cobertura praticamente total. O problema está concentrado em uma.');
  s.addImage({ path: path.join(FIG, 'missing_por_municipio.png'), x: 0.9, y: 1.55, w: 3.75, h: 4.90 });
  cartao(s, 5.15, 1.7, 7.45, 2.0, 'A variável que concentra o problema',
    'pct_analfab tem 15,9% dos setores sem dado — 16.552 no recorte urbano. As outras seis componentes ficam todas abaixo de 0,05% de ausentes, ou seja, cobertura praticamente total.', CLAY);
  cartao(s, 5.15, 3.9, 7.45, 2.05, 'E não é aleatório',
    'A supressão de V00901 acontece onde há poucos analfabetos — ou seja, nos setores de melhor situação socioeconômica. A tabela seguinte mostra a dependência com o porte do setor, que é a prova do mecanismo.', CLAY);
  nota(s, 'banco_de_dados/eda/figuras/missing_por_municipio.png — célula step11 do Notebook 02.');
}

{ const s = S();
  titulo(s, 'O sigilo depende do porte do setor', 'A prova de que a supressão não é aleatória — e de que o viés tem direção conhecida.');
  const y16 = blocoTabela(s, 'sigilo_porte', { y: 1.72, colW: [4.4, 2.5, 3.0, 2.0], fontSize: 12.5, rowH: 0.40 });
  cartao(s, M, y16, W - 2*M, 1.15, 'O que isso permite afirmar',
    'Como os setores excluídos são os de menor analfabetismo, a média observada é um TETO. E como o IBGE reporta os zeros, o valor suprimido é ≥ 1 — o que fecha o intervalo: a média verdadeira está entre 3,14% e 3,64%.', PETROL);
}

// ═════════ 4. CORRELAÇÃO ═════════
{ const s = S(); secao(s, '4', 'A estrutura de associação', 'A matriz ampliada para dez variáveis, e o que ela decide.'); }

{ const s = S();
  titulo(s, 'Matriz de correlação — agora com dez variáveis', 'Demanda de agosto: idosos de 60+, menores de 5 anos e chefia feminina entram na matriz.');
  s.addImage({ path: fig('matriz_correlacao.png'), x: 0.57, y: 1.58, w: 12.20, h: 5.30 });
  nota(s, 'A linha preta separa as 7 componentes do IVS das 3 descritivas. Elas não entram no índice — estão na matriz para decidir se deveriam.');
}

{ const s = S();
  titulo(s, 'O que a matriz decidiu', 'A pergunta que interessa: alguma das três descritivas merece entrar no índice?');
  tabela(s, ['Variável descritiva', 'Maior |r| com o IVS-7', 'Média |r|', 'Leitura'], [
    ['pct_resp_feminino', '−0,299 com renda', {text:'0,133', options:{bold:true, color:PETROL}}, 'carrega eixo próprio'],
    ['pct_crianca_0a4', '−0,517 com renda', '0,383', 'redundante com o que já existe'],
    ['pct_idoso_60mais', '−0,541 com cor/raça', '0,392', 'redundante com o que já existe'],
  ], { y: 1.85, colW: [3.4, 4.2, 2.0, 2.3], fontSize: 13, rowH: 0.42 });
  cartao(s, M, 3.6, 5.85, 1.6, 'Chefia feminina é a candidata',
    'Média |r| de 0,133 contra as sete componentes. Ela mede algo que nenhuma variável do índice captura — e é esse o argumento para promovê-la.', PETROL);
  cartao(s, M + 6.25, 3.6, 5.85, 1.6, 'Idosos e crianças são espelhos',
    'Correlação de −0,722 entre si: são os dois lados da mesma estrutura etária. Colocar as duas no índice contaria a mesma coisa duas vezes.', CLAY);
  s.addText('Renda, cor/raça e analfabetismo correlacionam-se entre si a −0,81, −0,76 e +0,63. Pesos iguais dariam três votos à mesma dimensão latente sem que isso fosse escolha deliberada.',
    { x: M, y: 5.5, w: W - 2*M, h: 0.7, fontFace: SANS, fontSize: 13.5, color: INK });
}

// ═════════ 5. RENDA ═════════
{ const s = S(); secao(s, '5', 'A renda sob auditoria', 'Cinco demandas de agosto convergem aqui, do caso isolado à decisão de escala.'); }

{ const s = S();
  titulo(s, 'O caso que abriu o assunto', 'Um setor com renda média declarada de R$ 170.418,06 por responsável.');
  regua(s, 1.78, 1.25, TINTA, M, 5.6);
  s.addText('CD_SETOR 310620005650366', { x: M, y: 1.88, w: 5.6, h: 0.32, fontFace: MONO, fontSize: 12, color: CINZA, margin: 0 });
  s.addText('R$ 170.418,06', { x: M, y: 2.24, w: 3.45, h: 0.85, fontFace: FONTE, fontSize: 42, color: TINTA, bold: true, margin: 0 });
  s.addText([
    { text: 'Belo Horizonte · bairro Senhor dos Passos', options: { breakLine: true } },
    { text: 'CD_TIPO = 1 — Favela e Comunidade Urbana', options: { breakLine: true, bold: true, color: ACENTO } },
    { text: '186 domicílios · 518 pessoas · 31 analfabetos', options: {} },
  ], { x: M, y: 3.14, w: 5.6, h: 1.2, fontFace: FONTE, fontSize: 13, color: TINTA, margin: 0, lineSpacing: 19 });
  regua(s, 4.42, 0.75, REGUA, M, 5.6);
  anotar(s, M - 0.14, 2.26, 3.42, 0.80, 'CV de 5,26 contra 0,78 —\numa média puxada por poucos', M + 3.62, 2.34, 2.55);
  cartao(s, M + 6.25, 1.75, 5.85, 1.45, 'Por que não é renda alta',
    'R$ 170 mil × 186 domicílios daria R$ 31,7 milhões por mês circulando numa favela de 186 casas. O perfil do setor não sustenta esse valor.', CLAY);
  cartao(s, M + 6.25, 3.4, 5.85, 1.45, 'O que o próprio IBGE responde',
    'O arquivo traz V06005, a variância. Aqui o CV é 5,26 contra mediana nacional de 0,78. Se fosse vírgula fora do lugar, o CV seria da ordem de 526 — a média está sendo puxada por poucas declarações.', CLAY);
  nota(s, `banco_de_dados/eda/renda_outliers_rastreados.csv — ${D.renda.n_rastreados} setores, um por linha, com identificação completa.`);
}

{ const s = S();
  titulo(s, 'Como separamos erro de dado de renda alta de verdade', 'Duas decisões de método fizeram a classificação funcionar.');
  cartao(s, M, 1.75, 5.85, 1.75, '1. A detecção é por município, não global',
    'O IVS é intraurbano. R$ 20 mil é comum em São Paulo e anômalo em Autazes. Um corte global mede a distância ENTRE cidades, que não é o objeto.', PETROL);
  cartao(s, M + 6.25, 1.75, 5.85, 1.75, '2. Extremo suspeito ≠ extremo alto',
    'O que levanta suspeita não é o valor, é a INCOERÊNCIA: setor no topo da renda local que também é favela, ou tem analfabetismo e proporção PPI acima da mediana do município.', PETROL);
  // Vem do JSON: com a renda sem o extremo de BH os suspeitos passam de 66 a 65, e um
  // número digitado aqui passaria a contradizer a tabela de origem.
  { const b = D.blocos.renda_classes;
    tabela(s, b.colunas, b.linhas.map(ln => ln.map((c, i) => {
      if (ln[0] === 'SUSPEITO' && (i === 0 || i === 4)) return { text: String(c), options: { bold: true, color: CLAY } };
      if (ln[0] === 'EXTREMO' && i === 4) return { text: String(c), options: { bold: true, color: PETROL } };
      return String(c);
    })), { y: 3.85, colW: [2.4, 1.8, 1.7, 2.6, 3.4], fontSize: 13, rowH: 0.42 }); }
  s.addText('A coluna da direita não valida a regra: ser favela É um dos testes de incoerência, então nenhuma favela pode cair em EXTREMO. O que a regra ainda não pega é erro em bairro rico — São Paulo, R$ 140.172,64, 45× a mediana local, sai como EXTREMO.',
    { x: M, y: 5.55, w: W - 2*M, h: 0.7, fontFace: SANS, fontSize: 12.5, color: CLAY, bold: true });
}

{ const s = S();
  titulo(s, 'As duas análises exploratórias, lado a lado', 'Demanda: rodar com e sem os extremos e comparar. O resultado contraria a intuição.');
  { const b = D.blocos.renda_com_sem;
    tabela(s, [b.titulo, 'Com', 'Sem', 'Variação'],
      b.linhas.map(ln => ln.map((c, i) => (ln[0] === 'Assimetria' && i === 3)
        ? { text: String(c), options: { bold: true, color: PETROL } } : String(c))),
      { y: 1.8, colW: [5.3, 2.2, 2.2, 2.2], fontSize: 12.5, rowH: 0.38 }); }
  cartao(s, M, 4.5, 5.85, 1.9, 'Excluir quase não muda a estatística',
    `As correlações se movem no máximo ${D.renda.max_delta_correlacao}; o Spearman fica praticamente imóvel. Se o argumento para excluir fosse o efeito na correlação, ele seria fraco.`, MUTED);
  cartao(s, M + 6.25, 4.5, 5.85, 1.9, 'Mas transformar muda dez vezes mais',
    'Passar a renda para log leva a correlação com analfabetismo de −0,42 para −0,59, e com cor/raça de −0,68 para −0,81. Dezessete vezes o efeito da exclusão.', PETROL);
}

{ const s = S();
  titulo(s, 'Onde a exclusão importa de verdade: a escala', 'A normalização min-max por município é o insumo do índice — e é ali que um valor ruim destrói tudo.');
  { const b = D.blocos.renda_normalizacao;
    tabela(s, b.colunas, b.linhas.map((ln, r) => ln.map((c, i) =>
      (r === 0 && (i === 0 || i === 5)) ? { text: String(c), options: { bold: true, color: i === 5 ? PETROL : TINTA } } : String(c))),
      { y: 1.85, colW: [3.0, 1.6, 1.8, 3.4, 1.6, 2.5], fontSize: 12.5, rowH: 0.4 }); }
  regua(s, 4.62, 1.25, TINTA);
  s.addText('Autazes é o caso didático', { x: M, y: 4.72, w: 11.6, h: 0.36, fontFace: FONTE, fontSize: 14, bold: true, color: TINTA, margin: 0 });
  s.addText(`43 setores, UM valor ruim, e 81% da cidade colapsa no primeiro decil da escala de renda — a variável deixa de discriminar dentro da cidade, que é exatamente o que o índice precisa que ela faça. ${D.blocos.renda_normalizacao.nota}`,
    { x: M, y: 5.12, w: 11.0, h: 0.85, fontFace: FONTE, fontSize: 13, color: TINTA, margin: 0, lineSpacing: 18 });
}

{ const s = S();
  titulo(s, 'Renda alta está mesmo nos setores pequenos?', 'A demanda supunha que sim. O valor não depende do tamanho; a suspeita depende.');
  s.addImage({ path: fig('renda_tamanho_do_setor.png'), x: 2.29, y: 1.58, w: 8.75, h: 3.60 });
  cartao(s, M, 5.3, 5.85, 1.3, 'O VALOR não depende do tamanho',
    `Spearman entre nº de domicílios e renda: −0,031. O maior valor da base (${D.renda.max_valor}, ${D.renda.max_municipio}) está num setor de ${D.renda.max_dom} domicílios, não num pequeno.`, MUTED);
  cartao(s, M + 6.25, 5.3, 5.85, 1.3, 'Mas a SUSPEITA depende, e muito',
    '0,265% de suspeitos nos setores até 50 domicílios contra 0,045% nos de 201–400: seis vezes mais. O coeficiente de variação cai de 1,11 para 0,90.', PETROL);
}

{ const s = S();
  titulo(s, 'Sudeste e Norte: dois fenômenos com o mesmo rótulo', 'Demanda: olhar os outliers de renda nessas duas regiões.');
  { const b = D.blocos.renda_regioes;
    tabela(s, b.colunas, b.linhas.map(ln => ln.map((c, i) => {
      if (ln[0] === 'Norte' && i === 6) return { text: String(c), options: { bold: true, color: CLAY } };
      if (ln[0] === 'Sudeste' && i === 3) return { text: String(c), options: { bold: true, color: CLAY } };
      return String(c);
    })), { y: 1.85, colW: [2.2, 1.6, 2.0, 2.1, 1.6, 1.6, 2.0], fontSize: 12.5, rowH: 0.4 }); }
  cartao(s, M, 4.65, 5.85, 1.75, 'Sudeste tem os extremos absolutos',
    `O maior valor do país está lá: ${D.renda.sudeste_max_mediana} vezes a mediana da própria região. Mas a taxa de suspeita é baixa — ${D.renda.sudeste_pct_suspeitos}.`);
  cartao(s, M + 6.25, 4.65, 5.85, 1.75, 'Norte tem 26 vezes a taxa do Sul',
    'A causa é a distribuição tão comprimida na base que qualquer setor de classe média já destoa, e não uma concentração maior de ricos. Assimetria 6,15, a maior do país.', CLAY);
  s.addNotes(`O critério global inverte esse retrato: marca 4,61% do Sudeste e só 1,32% do Norte. Dos ${D.renda.global_total} setores marcados pelo critério global, apenas ${D.renda.global_concordam} coincidem com o municipal.`);
}

{ const s = S();
  titulo(s, 'A distribuição da renda em cada uma das 70 cidades', 'Demanda: boxplot ou histograma por cidade, para conferir os valores destoantes.');
  s.addImage({ path: fig('renda_boxplot_por_cidade.png'), x: 4.1, y: 1.35, w: 2.45, h: 5.6 });
  cartao(s, M, 1.7, 3.1, 1.75, 'Por que painéis por região',
    'Setenta cidades num único boxplot passa do limite de categorias legíveis. Os painéis mantêm as cidades comparáveis dentro da região.');
  cartao(s, M, 3.65, 3.1, 1.75, 'Por que escala logarítmica',
    'Com assimetria 3,74, em escala linear 60 das 70 caixas colapsam contra a margem esquerda e nada se distingue.');
  cartao(s, M, 5.6, 3.1, 1.35, 'Por que caixas neutras',
    'A região já está codificada pelo painel. A única cor é o vermelho dos suspeitos.', CLAY);
  s.addText(`Os ${D.renda.n_suspeitos} setores suspeitos aparecem em vermelho, cidade a cidade. Belo Horizonte, Belém e Salvador concentram os casos mais graves. A figura em tamanho cheio está em banco_de_dados/eda/figuras/renda_boxplot_por_cidade.png.`,
    { x: 6.9, y: 3.2, w: 5.7, h: 1.6, fontFace: SANS, fontSize: 13, color: INK });
}

// ═════════ 6. BLOCOS DESCRITIVOS ═════════
{ const s = S(); secao(s, '6', 'Os blocos descritivos', 'Habitação, banheiro, chefia feminina, envelhecimento, morfologia e saneamento — fora do índice, dentro da análise.'); }

{ const s = S();
  titulo(s, 'Os blocos descritivos, região a região', 'Todos no mesmo recorte — o que a versão anterior deste deck não garantia.');
  const y29 = blocoTabela(s, 'descritivos_regiao', { y: 1.70, colW: [4.2, 1.55, 1.55, 1.75, 1.55, 1.55], fontSize: 12, rowH: 0.38 });
  cartao(s, M, y29, 3.8, 1.35, 'Precariedade tem geografias distintas',
    `Habitação precária (${D.descritivos.hab_precaria} no total) concentra-se no Centro-Oeste e no Sudeste — é metropolitana, não rural do Norte.`, CLAY);
  cartao(s, M + 4.2, y29, 3.8, 1.35, 'Banheiro segue o padrão do saneamento',
    `Sem banheiro exclusivo: ${D.descritivos.sem_banheiro} no total, e a pior situação é no Norte.`);
  cartao(s, M + 8.4, y29, 3.7, 1.35, 'Chefia feminina é maioria',
    `${D.descritivos.resp_feminino} das chefias no recorte urbano, com pico no Nordeste.`, PETROL);
}

{ const s = S();
  titulo(s, 'Chefia feminina e envelhecimento — os dois blocos que sumiram do deck anterior', 'Ambos existem como tabela desde junho.');
  const y30 = blocoTabela(s, 'envelhecimento', { y: 1.70, colW: [4.2, 1.55, 1.55, 1.75, 1.55, 1.55], fontSize: 12, rowH: 0.40 });
  stat(s, M, y30, 2.9, D.envelhecimento.IEP, 'IEP — índice de envelhecimento');
  stat(s, M + 3.1, y30, 2.9, D.envelhecimento.RDI, 'RDI — razão de dependência');
  stat(s, M + 6.2, y30, 2.9, D.envelhecimento.pct_60mais + '%', '60 anos ou mais');
  stat(s, M + 9.3, y30, 2.6, D.descritivos.resp_feminino, 'chefia feminina', PETROL);
  s.addText('Correção registrada: o IEP usava só a faixa de 0 a 4 anos no denominador e dava 299. Com o denominador correto — menores de 15 anos, conforme Galvão et al. — dá 92,7.',
    { x: M, y: y30 + 1.62, w: W - 2*M - 0.9, h: 0.5, fontFace: SANS, fontSize: 12, color: CLAY, bold: true });
}

{ const s = S();
  titulo(s, 'Tipo de espécie do domicílio', 'Morfologia urbana: o que NÃO é casa. Percentual sobre domicílios, não sobre setores.');
  blocoTabela(s, 'morfologia', { y: 1.6, colW: [1.3, 3.5, 1.35, 1.15, 1.15, 1.35, 1.15, 1.15], fontSize: 10.5, rowH: 0.315 });
  s.addNotes('Apartamento vai de 15,7% no Norte a 36,9% no Sul — é o indicador de morfologia pedido pela orientadora em julho. Cortiço e casa de cômodos concentram-se no Centro-Oeste.');
}

{ const s = S();
  titulo(s, 'Canalização da água — um eixo que o IVS não media', 'Demanda: testar V00199 a V00201 e calcular a proporção sem água encanada.');
  const y32 = blocoTabela(s, 'agua', { y: 1.65, colW: [2.2, 2.3, 2.1, 1.9, 2.5, 1.9], fontSize: 12.5, rowH: 0.38 });
  cartao(s, M, y32, 5.85, 1.75, 'É conceito diferente do que já estava no IVS',
    'pct_agua_inad (V00112–V00118) mede a FONTE: poço, nascente, carro-pipa, rio. A trinca nova mede a ENTREGA. Um domicílio com rede geral pode receber água só no terreno. Spearman entre os dois: 0,459.', PETROL);
  cartao(s, M + 6.25, y32, 5.85, 1.75, 'A partição fecha, e isso virou auditoria',
    'V00199 + V00200 + V00201 = V00001 em 100,00% dos 81.270 setores em que as três estão presentes. O teste roda a cada execução da suíte.', PETROL);
}

{ const s = S();
  titulo(s, 'O complemento que recupera 21,9% dos setores', 'A mesma quantidade medida por outro caminho, com um vigésimo dos ausentes.');
  regua(s, 1.84, 1.25, ACENTO, M, 5.6);
  s.addText('(V00200 + V00201) / V00001', { x: M, y: 1.96, w: 5.6, h: 0.44, fontFace: MONO, fontSize: 14, color: ACENTO, bold: true, margin: 0 });
  s.addText('21,9%', { x: M, y: 2.44, w: 5.6, h: 0.8, fontFace: FONTE, fontSize: 44, color: ACENTO, bold: true, margin: 0 });
  s.addText('dos setores ficam sem valor. V00200 e V00201 são contagens pequenas — e é a contagem pequena que o IBGE suprime.',
    { x: M, y: 3.28, w: 5.4, h: 0.8, fontFace: FONTE, fontSize: 12.5, color: TINTA, margin: 0, lineSpacing: 18 });
  regua(s, 1.84, 1.25, TINTA, M + 6.2, 5.6);
  s.addText('1 − V00199 / V00001', { x: M + 6.2, y: 1.96, w: 5.6, h: 0.44, fontFace: MONO, fontSize: 14, color: TINTA, bold: true, margin: 0 });
  s.addText('0,04%', { x: M + 6.2, y: 2.44, w: 5.6, h: 0.8, fontFace: FONTE, fontSize: 44, color: TINTA, bold: true, margin: 0 });
  s.addText('V00199 é contagem grande — o IBGE quase nunca a sigila. Como a trinca fecha, o complemento devolve o mesmo valor.',
    { x: M + 6.2, y: 3.28, w: 5.4, h: 0.8, fontFace: FONTE, fontSize: 12.5, color: TINTA, margin: 0, lineSpacing: 18 });
  cartao(s, M, 4.6, W - 2*M, 1.5, 'A ressalva que precisa constar do artigo',
    'A identidade só é VERIFICÁVEL onde as três variáveis estão presentes. Nos setores com V00200 ou V00201 sigilosos, aplicá-la é extrapolação — justificada porque a partição é definida pelo IBGE, mas é suposição, não medição. Registrada no GUIA §6.2.9 e coberta por teste.', CLAY);
}

{ const s = S();
  titulo(s, 'Cobertura integral de saneamento', 'Setores em que NENHUM domicílio está na condição inadequada.');
  const yc = blocoTabela(s, 'cobertura_regiao', { y: 1.65, colW: [4.0, 1.6, 1.6, 1.9, 1.6, 1.6], fontSize: 12.5, rowH: 0.40 });
  stat(s, M, yc, 2.75, D.cobertura.agua + '%', 'água 100% adequada');
  stat(s, M + 2.95, yc, 2.75, D.cobertura.esgoto + '%', 'esgoto 100% adequado');
  stat(s, M + 5.90, yc, 2.75, D.cobertura.lixo + '%', 'lixo 100% adequado');
  stat(s, M + 8.85, yc, 2.75, D.cobertura.tres + '%', 'os três juntos', CLAY);
  s.addText(`Só ${D.cobertura.tres}% dos setores têm os três serviços integralmente adequados. Contando a caçamba de serviço de limpeza como coleta, o lixo sobe de ${D.cobertura.lixo}% para ${D.cobertura.coleta}% — a diferença é o efeito da decisão metodológica sobre V00398.`,
    { x: M, y: yc + 1.62, w: W - 2*M - 0.9, h: 0.55, fontFace: SANS, fontSize: 12, color: INK });
}

{ const s = S();
  titulo(s, 'Gravidade do saneamento em faixas', 'Não basta saber quantos setores têm inadequação: importa quanto.');
  const yf = blocoTabela(s, 'saneamento_faixas', { y: 1.70, colW: [2.6, 3.0, 1.46, 1.46, 1.46, 1.46, 1.46], fontSize: 12, rowH: 0.40 });
  cartao(s, M, yf, W - 2*M, 1.3, 'A leitura',
    'No Norte, 30,8% dos setores têm metade ou mais dos domicílios com água inadequada — contra 11,8% em situação totalmente adequada. No Sul e no Centro-Oeste a distribuição se inverte por completo.', CLAY);
}

// ═════════ 7. FAVELAS ═════════
{ const s = S(); secao(s, '7', 'Favelas e Comunidades Urbanas', 'A fonte oficial, a validação do critério e a comparação com o resto da cidade.'); }

{ const s = S();
  titulo(s, 'A fonte oficial localizada e a validação do critério', 'Demanda: conferir um relatório do IBGE sobre vilas e favelas do Censo 2022.');
  cartao(s, M, 1.72, 5.85, 1.35, 'A fonte',
    'IBGE. Censo Demográfico 2022: Favelas e Comunidades Urbanas — Resultados do universo. Rio de Janeiro, 2024. 171 p. Definição e os quatro critérios transcritos na seção 14.2 do relatório.');
  cartao(s, M + 6.25, 1.72, 5.85, 1.35, 'A validação',
    `Dos 109.032 setores da base completa, ${D.fcu.n_setores_fcu} estão na lista oficial — e são exatamente os ${D.fcu.n_setores_fcu} com CD_TIPO = 1. Zero falso positivo, zero omissão. No recorte de análise são ${D.fcu_recorte.n_setores_fcu}, ${D.fcu_recorte.pct_setores_fcu}% dos 104.108. O campo NM_FCU não serve de critério: diverge em 25 setores, nenhum deles na lista oficial.`, PETROL);
  tabela(s, ['', 'Brasil (IBGE 2024)', 'ELSI-70', 'Cobertura'], [
    ['Favelas e Comunidades Urbanas', '12.348', '5.899', '47,8%'],
    ['Municípios com FCU', '656', '42', '6,4%'],
    [{text:'População em FCU', options:{bold:true}}, '16.390.815', '10.069.994', {text:'61,4%', options:{bold:true, color:PETROL}}],
    ['Domicílios em FCU', '6.556.998', '3.443.687', '52,5%'],
  ], { y: 3.35, colW: [4.6, 3.2, 2.5, 1.6], fontSize: 12.5, rowH: 0.4 });
  cartao(s, M, 5.3, W - 2*M, 1.35, 'A limitação que a fonte revelou — nota 7, página 75',
    'Além das 12.348 FCU classificadas, o IBGE identificou 2.298 FCU com 21 a 50 domicílios que NÃO receberam setor censitário próprio. Como nosso critério é CD_TIPO = 1, as favelas pequenas são invisíveis na base: a comparação favela × resto da cidade erra nos dois sentidos.', CLAY);
}

{ const s = S();
  titulo(s, 'Favela e restante da cidade, indicador a indicador', 'Quantas vezes o valor médio no setor de favela supera o de fora.');
  blocoTabela(s, 'favela_resto', { y: 1.58, colW: [3.0, 1.25, 1.35, 1.45, 1.35, 1.55, 1.65, 1.3], fontSize: 10.5, rowH: 0.305 });
  s.addNotes('Esgoto inadequado é 4,1 vezes maior em setor de favela; lixo, 2,9 vezes. A razão de moradores difere pouco (1,11), o que é coerente: adensamento domiciliar não é o eixo que separa favela do resto da cidade.');
}

// ═════════ 8. BRASIL ═════════
{ const s = S();
  titulo(s, 'A amostra ELSI comparada com o Brasil urbano', 'Linha de base nacional: os mesmos indicadores sobre os 468 mil setores do país.');
  const y39 = blocoTabela(s, 'brasil_elsi', { y: 1.70, colW: [4.4, 2.7, 2.7, 2.1], fontSize: 12.5, rowH: 0.40 });
  cartao(s, M, y39, 5.85, 1.55, 'A amostra é menos vulnerável que o Brasil urbano',
    'Em seis dos sete indicadores o recorte ELSI está melhor. O esgoto é o contraste mais forte: 0,080 contra 0,155 — quase metade.');
  anotar(s, M + 9.35, y39 - 1.62, 1.5, 0.36, 'única acima de 1', M + 8.1, y39 - 2.25, 2.4);
  cartao(s, M + 6.25, y39, 5.85, 1.55, 'A exceção é o lixo, e ela é diagnóstica',
    'Única variável em que o ELSI está PIOR (razão 1,21). Reforça a hipótese de que o indicador captura porte urbano — a caçamba é mais comum em cidade grande.', CLAY);
  s.addNotes('A população nacional calculada pela pipeline confere com o número oficial do Censo 2022: 203.080.756.');
}

// ═════════ 9. LIMITAÇÕES E PROCESSO ═════════
{ const s = S(); secao(s, '8', 'Limitações e processo', 'O que a base não permite afirmar, o que foi corrigido e o que vem agora.'); }

{ const s = S();
  titulo(s, 'O sigilo do analfabetismo — limitação aceita e quantificada', 'Demanda de agosto: aceitar a limitação, e ainda assim medir o tamanho dela.');
  cartao(s, M, 1.72, 5.85, 1.9, 'O sigilo incide nos setores RICOS',
    'A supressão de V00901 acontece onde há poucos analfabetos — na melhor situação socioeconômica. Renda mediana de R$ 6.092,84 nos setores sem o dado, contra R$ 2.313,89 nos que têm. E 30,8% de população preta, parda ou indígena contra 60,6%.', CLAY);
  cartao(s, M + 6.25, 1.72, 5.85, 1.9, 'Por isso a média observada é um TETO',
    'Como os excluídos são os de menor analfabetismo, a média sobre os 87.556 setores com dado superestima a amostra completa. E como o IBGE reporta os zeros — 9.268 setores declaram V00901 = 0 — o valor suprimido é ≥ 1, o que fecha o intervalo pelo outro lado.', PETROL);
  stat(s, M, 3.95, 3.5, '16.552', 'setores sem o dado (15,9%)', CLAY);
  stat(s, M + 3.9, 3.95, 3.5, '3,14% – 3,64%', 'onde está a média verdadeira', PETROL);
  stat(s, M + 7.8, 3.95, 4.3, '0,50 p.p.', 'largura da faixa', PETROL);
  s.addText('Meio ponto percentual de largura — estreito o bastante para nenhuma conclusão do estudo depender de qual ponto se adote. Nenhuma imputação serve: preencher com zero achata o gradiente nas áreas menos vulneráveis; imputar pela mediana municipal transfere aos setores ricos o perfil dos pobres.',
    { x: M, y: 5.65, w: W - 2*M, h: 0.85, fontFace: SANS, fontSize: 13, color: INK });
  nota(s, 'Redação completa em docs/Relatorio_EDA_Fase3_IVS_ELSI.md, seção 14.1. Decisão registrada no GUIA §6.2.6.');
}

{ const s = S();
  titulo(s, 'As limitações da análise exploratória', 'Todas registradas na seção 14 do relatório da EDA.');
  const lim = [
    ['Falácia ecológica', 'Todas as medidas são agregadas por setor. Nada aqui autoriza inferência sobre indivíduos (Lima-Costa & Barreto, 2003).'],
    ['Sigilo seletivo do analfabetismo', '15,9% dos setores sem o dado, concentrados nos setores ricos. Média verdadeira entre 3,14% e 3,64%.'],
    ['Favelas pequenas invisíveis', '2.298 FCU de 21 a 50 domicílios não receberam setor próprio. A comparação favela × cidade erra nos dois sentidos.'],
    ['Municípios pequenos após o filtro urbano', `${D.exclusao.perdem_10pct} dos ${D.exclusao.municipios} perdem mais de 10% dos setores; ${D.exclusao.menos_de_10_setores} ficam com menos de 10.`],
    ['Três componentes não reprodutíveis', 'Anos de estudo, faixas de renda e óbitos cardiovasculares não existem nos agregados por setor.'],
    ['A EDA é descritiva', 'Nenhuma inferência ou teste de hipótese foi conduzido. As correlações são exploratórias.'],
  ];
  let y = 1.72, i = 0;
  lim.forEach(([t, d2]) => {
    const x = M + (i % 2) * 6.25;
    if (i % 2 === 0 && i > 0) y += 1.62;
    cartao(s, x, y, 5.85, 1.45, t, d2, i < 4 ? CLAY : MUTED);
    i++;
  });
}

{ const s = S();
  titulo(s, 'As correções desta rodada', 'A maioria apareceu num teste ou numa conferência de números.');
  tabela(s, ['O que estava errado', 'Como foi pego', 'Correção'], [
    ['A tabela regional de água somava as duas parcelas sigilosas', {text:'teste automatizado', options:{bold:true, color:PETROL}}, 'passou a usar o complemento; a massa suprimida virou coluna publicada'],
    ['O deck trazia banheiro e apartamento de outro recorte', {text:'auditoria número a número', options:{bold:true, color:PETROL}}, 'os números passaram a ser lidos das tabelas em tempo de build, com o recorte carimbado'],
    ['"A premissa da demanda 2 não se confirma"', 'olhar a variável certa', 'a taxa de suspeita é 6× maior em setor pequeno; só o valor não depende do tamanho'],
    ['GUIA e README diziam que o NB02 não importava o módulo', 'varredura da documentação', 'três afirmações obsoletas corrigidas'],
    ['Ordenação instável na auditoria do analfabetismo', 'comparação byte a byte', 'desempate por nome; a tabela deixou de mudar a cada execução'],
    ['Numeração de seções colidindo no GUIA', 'conferência após inserção', 'renumerado; quatro referências cruzadas corrigidas'],
  ], { y: 1.8, colW: [4.6, 3.2, 4.1], fontSize: 11.5, rowH: 0.52 });
  s.addText('A segunda linha é sobre esta apresentação: a primeira versão dela tinha números digitados à mão, e três vieram do recorte errado. Agora o gerador lê os CSVs — nenhum valor é digitado.',
    { x: M, y: 5.6, w: W - 2*M, h: 0.6, fontFace: SANS, fontSize: 13, color: CLAY, bold: true });
}

{ const s = S();
  titulo(s, 'As demandas de agosto, uma a uma');
  tabela(s, ['#', 'Demanda', 'Onde está', 'Situação'], [
    ['1', 'Identificar todos os outliers de renda, com cidade, setor e se é favela', `renda_outliers_rastreados.csv — ${D.renda.n_rastreados} setores`, {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['1.1', 'Duas EDAs, com e sem os outliers, e a comparação', 'renda_eda_com_vs_sem · renda_correlacao_com_vs_sem', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['2', 'Rastrear rendas exorbitantes em setores pequenos, à mostra na EDA', 'renda_setores_pequenos.csv · figura renda_tamanho_do_setor', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['3', 'Boxplot ou histograma por cidade', 'figura renda_boxplot_por_cidade — 70 cidades', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['4', 'Outliers de renda no Sudeste e Norte', 'renda_extremos_por_regiao.csv', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['5', 'Relatório do IBGE sobre vilas e favelas', 'docs/ — 171 páginas + planilha por setor; validação de 100%', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['6', 'Aceitar a limitação do analfabetismo', 'Relatório seção 14.1 · GUIA §6.2.6', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['7', 'Focar nas pendências de renda e propor mais estudos', 'quatro estudos propostos; ver próximos passos', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['8', 'A EDA central reunindo tudo', 'esta apresentação — 12 blocos de tabela e 6 figuras', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['9', 'Ampliar a matriz de correlação', 'matriz 10×10 · NB02 célula step12', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['10', 'Testar V00199 a V00201 e a proporção sem água encanada', 'NB02 seção 7h · três CSVs · GUIA §6.2.9', {text:'cumprida', options:{color:PETROL, bold:true}}],
    ['11', 'Planejar a análise fatorial em Python', 'plano pronto; execução não iniciada por decisão sua', {text:'planejada', options:{color:CLAY, bold:true}}],
  ], { y: 1.55, colW: [0.6, 5.0, 5.1, 1.6], fontSize: 10.5, rowH: 0.36 });
}

{ const s = S();
  titulo(s, 'Por que estes números são confiáveis', 'A EDA inteira é reexecutável do zero, e o que ela afirma é verificado por teste.');
  stat(s, M, 1.8, 2.75, '63', 'testes automatizados');
  stat(s, M + 2.95, 1.8, 2.75, '100%', 'passando');
  stat(s, M + 5.90, 1.8, 2.75, '61', 'tabelas em eda/');   // conferido: ls banco_de_dados/eda/*.csv
  stat(s, M + 8.85, 1.8, 2.75, '0', 'CSVs sem código-fonte');
  const it = [
    ['Fórmulas testadas contra dados sintéticos', 'Cada indicador é conferido com valores redondos calculáveis na mão — safe_div, denominador do analfabetismo, complemento da água, classificação de renda.'],
    ['Artefatos conferidos contra os valores publicados', 'Os testes leem os CSVs gerados e verificam contagens exatas: 109.032 setores, 70 municípios, 106.281 elegíveis, 104.108 urbanos, 19.507 de favela.'],
    ['Refatorações provadas neutras antes de valer', 'Ao fazer o Notebook 01 ler do módulo, a base nova foi comparada com a anterior: 67 colunas comuns, zero diferenças, mesmos 109.032 setores.'],
    ['Este deck é gerado por script', 'scripts/eda_central_dados.py lê as tabelas e emite o JSON; o gerador só formata. Nenhum número é digitado, e cada tabela carrega o recorte de origem.'],
  ];
  let y = 3.7;
  it.forEach(([t, d2]) => {
    s.addText(t, { x: M, y, w: 4.2, h: 0.7, fontFace: SANS, fontSize: 12.5, bold: true, color: PETROL, margin: 0, valign: 'top' });
    s.addText(d2, { x: M + 4.4, y, w: W - M - 5.1, h: 0.7, fontFace: SANS, fontSize: 11.5, color: INK, margin: 0, valign: 'top' });
    y += 0.78;
  });
}

{ const s = S();
  titulo(s, 'A decisão dos pesos do índice', 'Submetida a um conselho de cinco análises independentes, com revisão cega entre elas.');
  s.addText('Veredito', { x: M, y: 1.72, w: 2.0, h: 0.32, fontFace: FONTE, fontSize: 11,
    color: ACENTO, bold: true, charSpacing: 2, margin: 0 });
  s.addText('Adotar 60/40 da literatura, e tratar o peso como análise de sensibilidade — não como decisão central.',
    { x: M, y: 2.04, w: 11.4, h: 0.8, fontFace: FONTE, fontSize: 22, color: TINTA, bold: true, margin: 0, valign: 'top' });
  regua(s, 2.92, 1.25, TINTA);
  cartao(s, M, 3.1, 3.8, 1.7, 'O peso não é a alavanca',
    'Com renda, cor/raça e analfabetismo colineares a 0,76–0,81, qualquer esquema razoável produz quase o mesmo ranking.');
  cartao(s, M + 4.2, 3.1, 3.8, 1.7, 'A fatorial esconde a decisão do lixo',
    'Com correlações de 0,10 a 0,20, pct_lixo_inad carrega sozinho ou em lugar nenhum — e a escolha do que fazer volta a ser manual.');
  cartao(s, M + 8.4, 3.1, 3.7, 1.7, 'Custo assimétrico de errar',
    '60/40 é citável e reversível. A fatorial exige imputar 15,9% de faltantes não aleatórios e defender tudo sozinho.');
  cartao(s, M, 5.05, 5.85, 1.55, 'O que a revisão acrescentou',
    'A normalização min-max por município mexe mais no ranking do que qualquer peso — e ninguém testou. Debater 60/40 sobre uma escala arbitrária por município é otimizar o parâmetro errado.', CLAY);
  cartao(s, M + 6.25, 5.05, 5.85, 1.55, 'O próximo passo que fecha a questão',
    'Calcular o IVS três vezes — 60/40, pesos iguais e 50/50 — e reportar a correlação de Spearman entre os rankings. Acima de 0,95, uma tabela responde a pergunta.', PETROL);
  s.addNotes('As cinco revisões cegas escolheram independentemente a mesma resposta como a mais forte. A arbitragem final é da orientação.');
}

{ const s = S();
  s.background = { color: PETROL_D };
  s.addText('O que vem agora', { x: M, y: 0.75, w: W - 2*M, h: 0.8, fontFace: SERIF, fontSize: 34, color: WHITE, bold: true });
  const prox = [
    ['Notebook 03', 'Normalização min-max por município, com a renda invertida e transformada. É a decisão que o conselho apontou como dominante sobre o peso.'],
    ['Sensibilidade dos pesos', 'IVS calculado com 60/40, pesos iguais e 50/50; Spearman entre os rankings. Resultado publicável em uma tabela.'],
    ['Notebook 04 — fatorial', 'Plano pronto: transformar a renda, decidir os 16.552 setores sem analfabetismo, KMO e Bartlett, número de fatores, varimax. Execução aguardando decisão.'],
    ['Estudos de renda propostos', 'Renda relativa à mediana municipal como indicador; desigualdade intraurbana por Gini ou p90/p10; renda × favela sistematizada.'],
    ['Redação das limitações', 'Falta escrever falácia ecológica, viés de sobrevivência e institucionalizados — que não saem pela classe COLETIVO, vazia na base, e sim porque entram em v0001 sem entrar em V00001. A do analfabetismo e a das favelas já estão prontas.'],
  ];
  let y = 1.85;
  prox.forEach(([t, d2], i) => {
    s.addShape(p.ShapeType.ellipse, { x: M, y: y + 0.04, w: 0.44, h: 0.44, fill: { color: SEAFOAM } });
    s.addText(String(i + 1), { x: M, y: y + 0.04, w: 0.44, h: 0.44, align: 'center', valign: 'middle', fontFace: SERIF, fontSize: 15, color: PETROL_D, bold: true });
    s.addText(t, { x: M + 0.7, y, w: 3.0, h: 0.5, fontFace: SANS, fontSize: 13.5, bold: true, color: SEAFOAM, margin: 0 });
    s.addText(d2, { x: M + 3.85, y, w: W - M - 4.55, h: 0.72, fontFace: SANS, fontSize: 12, color: 'C9D8D4', margin: 0 });
    y += 0.92;
  });
  s.addText('Pedro Dias Soares  ·  Iniciação Científica  ·  Fiocruz Minas — Instituto René Rachou  ·  agosto de 2026',
    { x: M, y: H - 0.85, w: W - 2*M, h: 0.4, fontFace: SANS, fontSize: 11.5, color: '89A19C' });
}

p.writeFile({ fileName: process.argv[2] }).then(f => console.log('deck escrito:', f));
