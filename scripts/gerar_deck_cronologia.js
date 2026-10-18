/**
 * Gera o deck da cronologia do projeto: o processo inteiro, em ordem — as alterações, os
 * fatos e a organização do repositório —, do primeiro commit até o dia em que roda.
 *
 * De onde vem cada coisa
 * ----------------------
 * - Datas e contagens de commits: `git log`, lido na hora. Nenhuma contagem digitada.
 * - Números de resultado: os CSVs que os próprios scripts gravam (linha de base do NB04,
 *   cenários da fatorial ampliada, grade do NB05, partição do banheiro) e o grafo.
 * - Fatos que só existem em documento (decisões de método, demandas, achados de
 *   auditoria): o documento que os registra, citado no pé do slide ou nas anotações.
 * - As anotações de cada página do diário levam os commits do dia, com o hash, para ir
 *   do slide ao histórico sem procurar.
 *
 * A identidade é a de scripts/deck_comum.js, a mesma dos outros decks.
 *
 * Uso:
 *     node scripts/gerar_deck_cronologia.js [saida.pptx]
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const SAIDA = process.argv[2] || path.join(RAIZ,
  'docs/Apresentacoes_IVS/complementos/Cronologia_Projeto_IVS_2026-10.pptx');
const arq = rel => path.join(RAIZ, rel);
const sh = cmd => execSync(cmd, { cwd: RAIZ, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024,
  stdio: ['ignore', 'pipe', 'ignore'] }).trim();

// ── Formatação brasileira ────────────────────────────────────────────────────
const num = (v, c = 2) => Number(v).toFixed(c).replace('.', ',');
const mil = v => Math.round(Number(v)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
const reais = v => 'R$ ' + Number(v).toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.');
const dm = iso => `${iso.slice(8, 10)}/${iso.slice(5, 7)}`;
const dma = iso => `${dm(iso)}/${iso.slice(0, 4)}`;
const agora = new Date();
const HOJE = `${agora.getFullYear()}-${String(agora.getMonth() + 1).padStart(2, '0')}-`
           + String(agora.getDate()).padStart(2, '0');

// ── CSV ──────────────────────────────────────────────────────────────────────
// Campo entre aspas quando tem separador ou aspas (RFC4180, o padrão do pandas). O
// separador é ';' nos CSVs da EDA e da fatorial ampliada e ',' nos do NB05: descobre
// pelo cabeçalho.
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

// ── O histórico do git ───────────────────────────────────────────────────────
const LOG = sh('git log --reverse --date=short --format=%ad%x09%h%x09%s').split('\n')
  .map(l => { const [data, hash, ...r] = l.split('\t'); return { data, hash, msg: r.join('\t') }; });
const PRIMEIRO = LOG[0].data, ULTIMO = LOG[LOG.length - 1].data;

/**
 * Uma entrada do diário. `iso` é a data do fato. As anotações levam a fonte e os commits
 * do dia; `filtro` (regex sobre a mensagem) separa os do item quando o dia teve muitos.
 * Commit cuja mensagem fala da ferramenta de trabalho, e não do projeto, entra só pelo hash.
 */
const DE_FERRAMENTA = /prompt|token|claude|teto de chamadas/i;
const citar = c => DE_FERRAMENTA.test(c.msg) ? c.hash : `${c.hash} “${c.msg}”`;
function E(iso, fato, detalhe, fonte, filtro) {
  const doDia = LOG.filter(c => c.data === iso);
  const doItem = filtro ? doDia.filter(c => filtro.test(c.msg)) : (doDia.length <= 10 ? doDia : []);
  let nota = fonte ? `Fonte: ${fonte}.` : '';
  if (!doDia.length) nota += `\nNenhum commit em ${dma(iso)}: o registro é o documento citado.`;
  else nota += `\n${doDia.length} commit(s) em ${dma(iso)}` + (doItem.length
    ? '; deste item: ' + doItem.map(citar).join(' · ') : '.');
  return { data: dm(iso), fato, detalhe, nota: nota.trim() };
}

// ── Números lidos dos arquivos ───────────────────────────────────────────────
const BASE = Object.fromEntries(lerCsv('banco_de_dados/eda/fatorial_ampliada/linha_de_base_nb04.csv')
  .map(r => [r.medida, Number(r.valor)]));
const CEN = lerCsv('banco_de_dados/eda/fatorial_ampliada/cenarios.csv');
const cen = id => CEN.find(r => r.cenario === id);
const ESP = lerCsv('banco_de_dados/eda/ivs_especificacoes/especificacoes.csv');
const REF = lerCsv('banco_de_dados/eda/ivs_especificacoes/referencia.csv');
const ACR = lerCsv('banco_de_dados/eda/ivs_especificacoes/acrescimo_renda.csv');
const IMP = lerCsv('banco_de_dados/eda/atualizada/renda_imputacao_alternativas.csv');
const QUADRO = lerCsv('banco_de_dados/entrega_orientadora/Quadro_Indicadores.csv');

const eleg = ESP.filter(r => r.elegivel === 'True');
const idRef = REF.find(r => r.leitura === 'principal').id;
const espRef = ESP.find(r => r.id === idRef);
const nBases = new Set(ESP.map(r => `${r.renda}|${r.lixo}|${r.banheiro}`)).size;
const nEsquemas = new Set(ESP.map(r => `${r.rotacao}|${r.metodo}`)).size;
const nNorm = new Set(ESP.map(r => r.normalizacao)).size;
// O IVS-7 do NB04 é a base renda original · com lixo · sem banheiro; a comunalidade
// mínima não depende do esquema de peso, então basta a linha da Varimax.
const ivs7 = ESP.find(r => r.renda === 'original' && r.lixo === 'com' && r.banheiro === 'fora'
                           && r.rotacao === 'varimax' && r.metodo === 'ss');
const rendaVenceGlobal = ACR.filter(r => +r.auc_renda_global > +r.auc_indice_global).length;
const rendaVenceMun = ACR.filter(r => +r.auc_renda_mun > +r.auc_indice_mun).length;
const indiceVenceEstratos = ACR.filter(r => +r.auc_indice_estratos > +r.auc_renda_estratos).length;
const medianaMun = IMP.find(r => r.alternativa === 'mediana de BH sem o setor').valor_imputado;

// Partição do banheiro: V00495 = V00236 + V00237 + V00238, setor a setor.
const PART = fs.readFileSync(arq('banco_de_dados/eda/fatorial_ampliada/banheiro_particao.csv'), 'utf8')
  .replace(/^﻿/, '').trim().split(/\r?\n/);
const iBate = PART[0].split(';').indexOf('bate_com_v00495');
let nSetoresBase = PART.length - 1, nPresentes = 0, nBate = 0;
PART.slice(1).forEach(l => {
  const v = l.split(';')[iBate];
  if (v === 'True' || v === 'False') nPresentes++;
  if (v === 'True') nBate++;
});

// Colunas da entrega: só o cabeçalho, sem ler a base inteira.
function colunasDe(rel) {
  const fd = fs.openSync(arq(rel), 'r');
  const buf = Buffer.alloc(65536);
  const n = fs.readSync(fd, buf, 0, buf.length, 0);
  fs.closeSync(fd);
  const cab = buf.toString('utf8', 0, n).split(/\r?\n/)[0];
  return cab.split(cab.includes(';') ? ';' : ',').length;
}
const nColunasEntrega = colunasDe('banco_de_dados/entrega_orientadora/Base_ELSI_70Municipios_Censo2022.csv');

const GRAFO = JSON.parse(fs.readFileSync(arq('graphify-out/graph.json'), 'utf8'));
const gNos = GRAFO.nodes.length;
const gArestas = (GRAFO.links || GRAFO.edges).length;
const gComunidades = new Set(GRAFO.nodes.map(n => n.community).filter(c => c !== undefined)).size;

const slidesDe = rel => {
  try { return (sh(`unzip -l "${arq(rel)}"`).match(/ppt\/slides\/slide\d+\.xml/g) || []).length; }
  catch (e) { return null; }
};
const DECK_ATUAL = 'docs/Apresentacoes_IVS/Analise_Fatorial_NB04_2026-09.pptx';
const nSlidesDeckAtual = slidesDe(DECK_ATUAL);

const noGit = dir => sh(`git ls-files -- "${dir}"`).split('\n').filter(Boolean).length;

// Testes: a contagem do pytest (conta os parametrizados); sem ele, as funções test_.
let nTestes = null;
try {
  const m = sh('.venv/bin/python -m pytest --collect-only -q').match(/(\d+) tests? collected/);
  if (m) nTestes = Number(m[1]);
} catch (e) { /* sem ambiente: cai na contagem estática */ }
if (nTestes === null) {
  nTestes = fs.readdirSync(arq('tests')).filter(f => f.endsWith('.py'))
    .reduce((n, f) => n + (fs.readFileSync(arq(`tests/${f}`), 'utf8').match(/^\s*def test_/gm) || []).length, 0);
}

// ── O deck ───────────────────────────────────────────────────────────────────
const d = criarDeck({ titulo: 'Cronologia do Projeto IVS — Censo 2022' });
const { p, S, regua, titulo, secao, bloco, procedencia, capa, alturaTexto, tabelaAjustada,
        diario, cores, geo } = d;
const { TINTA, CINZA, CINZA_C, REGUA_F, ACENTO, FONTE } = cores;
const { W, H, M } = geo;

// 1 · Capa
capa(S(), 'PROJETO IVS · CENSO 2022 · FIOCRUZ MINAS — INSTITUTO RENÉ RACHOU',
  'Cronologia do projeto',
  'O processo inteiro, em ordem: o que mudou, quando, por quê, o que se descobriu e como o '
  + 'repositório foi organizado — de março a outubro de 2026.',
  `Pedro Dias Soares · Iniciação Científica · ${LOG.length} commits, de ${dma(PRIMEIRO)} a ${dma(ULTIMO)}`);

// 2 · Como ler
{
  const s = S();
  titulo(s, 'Como ler este deck', 'De onde vem cada data e cada número');
  const w = 5.55, x2 = M + 6.05;
  bloco(s, M, 1.85, w, 'As datas.', 'São as do commit no git, salvo quando o documento registra '
    + 'outra — trabalho feito antes de ir ao git, como as demandas de julho, implementadas em '
    + '09/08 e commitadas em 20 e 21/08. Nesses casos o slide diz qual documento.', false, 1.9);
  bloco(s, x2, 1.85, w, 'Os números.', 'Saem dos CSVs que os scripts gravam, lidos na hora em '
    + 'que este deck é gerado: linha de base do NB04, cenários da fatorial ampliada, grade do '
    + 'NB05, partição do banheiro, grafo. Os que só existem em documento citam o documento.',
    false, 1.9);
  bloco(s, M, 3.95, w, 'As anotações.', 'Cada página do diário leva, nas anotações do '
    + 'apresentador, a fonte de cada item e os commits do dia com o hash — para ir do slide '
    + 'ao histórico sem procurar.', false, 1.9);
  bloco(s, x2, 3.95, w, 'A ordem.', 'Sete capítulos em ordem de data, de março a outubro; '
    + 'depois três leituras transversais — as decisões de método, os achados e a organização '
    + 'do repositório — e, no fim, onde o projeto está e o que vem.', true, 1.9);
  s.addNotes(`Deck gerado por scripts/gerar_deck_cronologia.js em ${dma(HOJE)}. O histórico `
    + `do git tem ${LOG.length} commits, de ${dma(PRIMEIRO)} a ${dma(ULTIMO)}. `
    + 'As datas de commit são as datas em que o trabalho '
    + 'entrou no git; quando um documento registra outra data para o mesmo fato, vale a do documento, e o slide diz qual.');
}

// 3 · O projeto
{
  const s = S();
  const y = titulo(s, 'O projeto em uma página', 'Identidade, objetivo e pergunta');
  tabelaAjustada(s, ['Item', 'Detalhe'], [
    ['Título', 'Índice de Vulnerabilidade à Saúde (IVS) intraurbano — Censo Demográfico 2022'],
    ['Tipo', 'Iniciação Científica (bolsista)'],
    ['Instituição', 'Fiocruz Minas — Instituto René Rachou (IRR)'],
    ['Período', 'março de 2026 a fevereiro de 2027'],
    ['Unidade', 'Setor censitário'],
    ['Recorte', 'Setores urbanos dos 70 municípios da amostra do ELSI-Brasil'],
    ['Referência', 'IVS-BH 2012, da Secretaria Municipal de Saúde de Belo Horizonte'],
    ['Produto', 'Relatório Final de IC e artigo submetido a periódico'],
  ], { y: y + 0.1, colW: [1.45, 4.1], fontSize: 12.5 });
  const x = M + 6.0, w = W - M - x;
  bloco(s, x, y + 0.2, w, 'Objetivo.', 'Construir um IVS intraurbano por setor censitário para os '
    + '70 municípios do ELSI-Brasil, com o Censo 2022, e analisar a sua distribuição espacial.',
    false, 1.0);
  bloco(s, x, y + 1.35, w, 'Pergunta.', 'Como se distribui a vulnerabilidade à saúde nos setores '
    + 'desses municípios, e que padrões intraurbanos de desigualdade aparecem?', false, 1.0);
  bloco(s, x, y + 2.5, w, 'Hipótese.', 'Setores periféricos têm IVS mais alto que as áreas '
    + 'centrais (o padrão centro-periferia da literatura); a nula é a ausência de padrão espacial.',
    false, 1.0);
  bloco(s, x, y + 3.65, w, 'Desenho.', 'Estudo ecológico; IVS contínuo de 0 a 1, depois '
    + 'categorizado em quatro faixas de risco.', true, 0.8);
  procedencia(s, 'Fonte: GUIA_DO_PROJETO.md, §1 e §2.');
  s.addNotes('A unidade de análise é o setor censitário, e o índice de referência é o IVS-BH '
    + '2012 da SMSA-BH, refeito com o Censo 2022 e estendido aos 70 municípios do ELSI-Brasil '
    + '(Estudo Longitudinal da Saúde dos Idosos Brasileiros). Cronograma do bolsista: análise de '
    + 'dados de março a setembro, cálculo do IVS em agosto e setembro, mapas em setembro, artigo de '
    + 'outubro a dezembro, relatório final de dezembro a fevereiro.');
}

// 4 · Os dados
{
  const s = S();
  const y = titulo(s, 'Os dados: oito arquivos do Censo 2022', 'Agregados por setor censitário, publicados pelo IBGE');
  tabelaAjustada(s, ['Arquivo (Agregados por Setores, Censo 2022)', 'Dimensão', 'Variáveis-chave'], [
    ['…_basico_BR_20250417.csv', 'Identificação e população', 'CD_SETOR, NM_MUN, v0001, v0005'],
    ['…_caracteristicas_domicilio1_BR.csv', 'Denominador habitacional', 'V00001, V00002, V00005, V00006'],
    ['…_caracteristicas_domicilio2_BR_20250417.csv', 'Saneamento', 'Água, esgoto, lixo, banheiro'],
    ['…_alfabetizacao_BR.csv', 'Educação', 'V00900 (sabe ler, 15+), V00901 (não sabe, 15+)'],
    ['…_cor_ou_raca_BR.csv', 'Cor ou raça', 'V01318, V01320, V01321'],
    ['…_renda_responsavel_BR.csv', 'Renda', 'V06004 (rendimento médio mensal do responsável)'],
    ['…_demografia_BR.csv', 'Idade', 'V01031–V01033 (0 a 14 anos)'],
    ['…_parentesco_BR.csv', 'Responsáveis', 'V01042 (o denominador abandonado em maio)'],
  ], { y: y + 0.1, colW: [4.6, 2.7, 4.33], fontSize: 12.5, rowH: 0.36 });
  procedencia(s, 'Fonte: GUIA_DO_PROJETO.md, §7 (os 8 arquivos-fonte).');
  s.addNotes('São os oito arquivos da publicação do IBGE de agregados por setor. A base do '
    + 'projeto junta os oito pelo código do setor e filtra os 70 municípios do ELSI-Brasil no '
    + 'Notebook 01. A V00237 (só sanitário ou buraco), usada no banheiro graduado, foi extraída do '
    + `arquivo de domicílio 2 em 26/09; a entrega à orientadora tem hoje ${nColunasEntrega} colunas.`);
}

// 5 · O funil de setores
{
  const s = S();
  const y = titulo(s, 'Quantos setores ficam a cada etapa', 'Da base dos 70 municípios ao IVS final');
  const etapas = [
    ['Base ELSI: todos os setores dos 70 municípios', nSetoresBase, 'banheiro_particao.csv (uma linha por setor)'],
    ['Recorte urbano (SITUACAO = Urbana)', 104108, 'GUIA_DO_PROJETO.md §2 e §6.4'],
    ['IVS-7: as sete variáveis presentes', Number(cen('S0').n), 'fatorial_ampliada/cenarios.csv, S0'],
    ['IVS final: a especificação de referência do NB05', Number(espRef.n), 'ivs_especificacoes/especificacoes.csv'],
  ];
  const xL = M, wL = 3.9, xB = M + 4.05, wB = 5.6, xV = xB + wB + 0.15;
  etapas.forEach(([rot, n, fonte], i) => {
    const yy = y + 0.35 + i * 1.02;
    s.addText(rot, { x: xL, y: yy, w: wL, h: 0.5, fontFace: FONTE, fontSize: 12.5, bold: true,
      color: TINTA, margin: 0, valign: 'top' });
    s.addText(fonte, { x: xL, y: yy + 0.5, w: wL, h: 0.3, fontFace: FONTE, fontSize: 9.5,
      italic: true, color: CINZA_C, margin: 0, valign: 'top' });
    const w = wB * n / nSetoresBase;
    s.addShape(p.ShapeType.rect, { x: xB, y: yy + 0.05, w, h: 0.42,
      fill: { color: i === etapas.length - 1 ? ACENTO : TINTA }, line: { type: 'none' } });
    s.addText([
      { text: mil(n), options: { bold: true, color: TINTA } },
      { text: `  ${num(100 * n / nSetoresBase, 1)}%`, options: { color: CINZA } },
    ], { x: xV, y: yy + 0.04, w: W - M - xV, h: 0.44, fontFace: FONTE, fontSize: 13, margin: 0,
      valign: 'middle' });
  });
  s.addText('No país inteiro são 468.099 setores (GUIA §6.2.8): é a base da comparação '
    + 'Brasil × ELSI. A perda até o IVS final é dado ausente — sobretudo sigilo do IBGE na renda '
    + 'e nas partes do banheiro graduado.', { x: M, y: y + 4.5, w: W - 2 * M, h: 0.55,
    fontFace: FONTE, fontSize: 12.5, color: CINZA, margin: 0, valign: 'top' });
  s.addNotes(`Base: ${mil(nSetoresBase)} setores nos 70 municípios. Recorte urbano: 104.108 (o filtro `
    + 'é aplicado na análise, não na extração — GUIA §6.2.5). IVS-7 com as sete variáveis: '
    + `${mil(cen('S0').n)}. Especificação de referência do NB05 (${idRef}): ${mil(espRef.n)} `
    + 'setores. A queda do recorte até a referência vem de variável ausente nos componentes do '
    + 'banheiro graduado ou da renda, em parte por sigilo (Relatorio_IVS_Final_NB05.md, achado 9).');
}

// 6 · A linha do tempo numa página
{
  const s = S();
  titulo(s, 'A linha do tempo em uma página', 'Os marcos de cada mês; o número abaixo do mês é o de commits');
  const COLS = [
    ['Março e abril', '2026-03-01', '2026-04-30', [['12/3', 'Repositório e a primeira pipeline'], ['16/3', 'Auditoria em SQLite'], ['25/3', 'Variáveis multidimensionais'], ['abr', 'Inserção no IRR e curso introdutório']]],
    ['Maio', '2026-05-01', '2026-05-31', [['06', 'Fase 2: o fluxo multidimensional'], ['14', 'O GUIA do projeto'], ['15', 'Fase 3: filtro ELSI e a 1ª EDA'], ['22', 'Denominador V00001'], ['25', 'Bases à orientadora']]],
    ['Junho', '2026-06-01', '2026-06-30', [['12', 'EDA refeita com V00001'], ['18', 'Indicadores novos; a caçamba'], ['19', 'Pipeline comentada']]],
    ['Julho', '2026-07-01', '2026-07-31', [['08', 'Primeiro grafo do projeto'], ['', 'Sete demandas da orientadora']]],
    ['Agosto', '2026-08-01', '2026-08-31', [['09', 'Demandas de julho feitas'], ['20', 'Módulo src/ivs_censo'], ['21', 'Água pelo V00199; EDA Central'], ['24', '1º diagnóstico fatorial']]],
    ['Set. 1–17', '2026-09-01', '2026-09-17', [['02', 'Auditoria; renda sem o extremo'], ['13', 'O livro da Enap'], ['17', 'NB04: a fatorial; auditoria integral']]],
    ['Set. 18–30', '2026-09-18', '2026-09-30', [['25', 'Revisão geral; demandas de setembro'], ['26', 'V00237: banheiro graduado'], ['27', 'NB05: o IVS final'], ['30', 'Estrutura do deck consertada']]],
    ['Outubro', '2026-10-01', '2026-10-31', [['01', 'O grafo lê os documentos; branch main'], [HOJE.slice(8, 10), 'Estas apresentações']]],
  ];
  const cw = (W - 2 * M) / COLS.length;
  COLS.forEach(([rot, de, ate, itens], i) => {
    const x = M + i * cw, wt = cw - 0.14;
    const n = LOG.filter(c => c.data >= de && c.data <= ate).length;
    s.addText(rot, { x, y: 1.62, w: wt, h: 0.3, fontFace: FONTE, fontSize: 12.5, bold: true,
      color: TINTA, margin: 0 });
    s.addText(n ? `${n} commit${n > 1 ? 's' : ''}` : 'sem commit', { x, y: 1.92, w: wt, h: 0.26,
      fontFace: FONTE, fontSize: 10, color: n ? CINZA : CINZA_C, italic: !n, margin: 0 });
    regua(s, 2.24, 1.0, TINTA, x, cw - 0.1);
    if (i > 0) s.addShape(p.ShapeType.line, { x: x - 0.05, y: 1.62, w: 0, h: 4.9,
      line: { color: REGUA_F, width: 0.5 } });
    let y = 2.38;
    itens.forEach(([dia, txt]) => {
      const h = alturaTexto(`${dia}  ${txt}`, wt, 11.5, 14.5);
      s.addText([
        ...(dia ? [{ text: dia + '  ', options: { bold: true, color: ACENTO } }] : []),
        { text: txt, options: { color: TINTA } },
      ], { x, y, w: wt, h, fontFace: FONTE, fontSize: 11.5, margin: 0, valign: 'top',
        lineSpacing: 14.5 });
      y += h + 0.16;
    });
  });
  procedencia(s, 'Fonte: git log (commits por período); sem commit: GUIA_DO_PROJETO.md §6.4 e §11; graphify-out/cost.json.');
  s.addNotes('Abril não tem commit: é o mês do Programa de Inserção do IRR e do Curso '
    + 'Introdutório (cronograma do bolsista, GUIA §11). Julho tem um commit (16/07, o grafo); as '
    + 'demandas de julho foram implementadas em 09/08 e commitadas em 20 e 21/08. Setembro está '
    + 'partido em dois porque concentra quase metade do histórico.');
}

// 7 · O ritmo do trabalho
{
  const s = S();
  titulo(s, 'O ritmo do trabalho', `${LOG.length} commits: por mês e por tipo de mudança`);
  const meses = [];
  for (let dt = new Date(PRIMEIRO.slice(0, 7) + '-01T12:00:00'); ; dt.setMonth(dt.getMonth() + 1)) {
    const k = `${dt.getFullYear()}-${String(dt.getMonth() + 1).padStart(2, '0')}`;
    meses.push(k);
    if (k >= ULTIMO.slice(0, 7)) break;
  }
  const NOMES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
  s.addText('Commits por mês', { x: M, y: 1.6, w: 6, h: 0.3, fontFace: FONTE, fontSize: 12,
    bold: true, color: TINTA, margin: 0 });
  s.addChart(p.ChartType.bar, [{ name: 'Commits', labels: meses.map(k => NOMES[+k.slice(5) - 1]),
    values: meses.map(k => LOG.filter(c => c.data.startsWith(k)).length) }], {
    x: M - 0.1, y: 1.9, w: 6.2, h: 3.9, barDir: 'col', chartColors: [TINTA], barGapWidthPct: 45,
    catAxisLabelFontFace: FONTE, catAxisLabelFontSize: 11, catAxisLabelColor: CINZA,
    catAxisLineShow: true, valAxisHidden: true, valGridLine: { style: 'none' },
    showValue: true, dataLabelFontFace: FONTE, dataLabelFontSize: 11, dataLabelColor: TINTA,
    dataLabelPosition: 'outEnd', dataLabelFormatCode: '0', showLegend: false,
  });
  const TIPOS = { docs: 'docs — documentação', feat: 'feat — funcionalidade nova', fix: 'fix — correção',
    chore: 'chore — manutenção', data: 'data — dados regerados', test: 'test — testes',
    refactor: 'refactor — reorganização', merge: 'merge', revert: 'revert',
    'sem prefixo': 'sem prefixo (os primeiros)' };
  const tipoDe = msg => {
    const m = msg.match(/^([A-Za-z]+)(\([^)]*\))?!?:/);
    if (!m) return /^merge/i.test(msg) ? 'merge' : 'sem prefixo';
    const t = m[1].toLowerCase();
    return { teste: 'test', dados: 'data' }[t] || t;
  };
  const cont = {};
  LOG.forEach(c => { const t = tipoDe(c.msg); cont[t] = (cont[t] || 0) + 1; });
  const ordem = Object.keys(cont).sort((a, b) => cont[b] - cont[a]);
  s.addText('Commits por tipo de mudança', { x: M + 6.45, y: 1.6, w: 5, h: 0.3, fontFace: FONTE,
    fontSize: 12, bold: true, color: TINTA, margin: 0 });
  s.addChart(p.ChartType.bar, [{ name: 'Commits', labels: ordem.map(t => TIPOS[t] || t),
    values: ordem.map(t => cont[t]) }], {
    x: M + 6.35, y: 1.9, w: 5.4, h: 3.9, barDir: 'bar', chartColors: [CINZA], barGapWidthPct: 35,
    catAxisOrientation: 'maxMin', catAxisLabelFontFace: FONTE, catAxisLabelFontSize: 10.5,
    catAxisLabelColor: TINTA, catAxisLineShow: false, valAxisHidden: true,
    valGridLine: { style: 'none' }, showValue: true, dataLabelFontFace: FONTE,
    dataLabelFontSize: 10.5, dataLabelColor: TINTA, dataLabelPosition: 'outEnd',
    dataLabelFormatCode: '0', showLegend: false,
  });
  const dias = {};
  LOG.forEach(c => { dias[c.data] = (dias[c.data] || 0) + 1; });
  const top = Object.entries(dias).sort((a, b) => b[1] - a[1]).slice(0, 5);
  s.addText([
    { text: 'Os cinco dias mais intensos: ', options: { bold: true } },
    { text: top.map(([dt, n]) => `${dm(dt)} (${n})`).join(' · ') },
  ], { x: M, y: 6.0, w: W - 2 * M, h: 0.4, fontFace: FONTE, fontSize: 12, color: TINTA, margin: 0 });
  procedencia(s, 'Fonte: git log; o tipo é o prefixo da mensagem do commit (feat, fix, docs…).');
  s.addNotes('O tipo vem do prefixo convencional da mensagem; os primeiros commits, de março, '
    + 'ainda não usavam prefixo. ' + top.map(([dt, n]) => `${dma(dt)}: ${n} commits`).join('; ')
    + '. O pico de 25/09 é a execução das demandas de setembro e da revisão geral, em seis fases.');
}

// 8 · As apresentações pelo caminho
{
  const s = S();
  const y = titulo(s, 'As apresentações que ficaram pelo caminho', 'docs/Apresentacoes_IVS/historico/ — cada uma como estava no dia');
  const HIST = fs.readdirSync(arq('docs/Apresentacoes_IVS/historico')).filter(f => f.endsWith('.pptx')).sort();
  const linhas = HIST.map(f => [dma(f.slice(0, 10)),
    f.slice(11, -5).replace(/_/g, ' '),
    String(slidesDe(`docs/Apresentacoes_IVS/historico/${f}`) || '—')]);
  const yFim = tabelaAjustada(s, ['Data', 'Apresentação', 'Slides'], linhas,
    { y: y + 0.05, colW: [1.3, 8.9, 1.4], fontSize: 12, rowH: 0.31 });
  s.addText([
    { text: 'Hoje, na raiz da pasta: ', options: { bold: true } },
    { text: `${path.basename(DECK_ATUAL)} (${nSlidesDeckAtual} slides) — a apresentação atual, com a `
      + 'EDA Central, a fatorial ampliada e o IVS final anexados. Estes dois decks novos ficam em complementos/.' },
  ], { x: M, y: yFim + 0.2, w: W - 2 * M, h: 0.6, fontFace: FONTE, fontSize: 11.5, color: TINTA,
    margin: 0, valign: 'top' });
  procedencia(s, 'Fonte: a pasta historico/ (data do nome do arquivo); slides contados no pacote .pptx.');
  s.addNotes('Os nomes antigos de cada deck estão em docs/Apresentacoes_IVS/README.md ("De onde '
    + 'vieram os nomes antigos"). Os decks do histórico não são regerados: ficam como foram '
    + 'apresentados. O de 15/05 ainda usa o denominador V01042, trocado em 22/05.');
}

// ── Capítulos em ordem de data ───────────────────────────────────────────────
function capitulo(n, tit, sub, nota) {
  const s = S();
  secao(s, String(n), tit, sub);
  if (nota) s.addNotes(nota);
}

capitulo(1, 'Março a maio — a base', 'Do repositório vazio à primeira EDA com o filtro ELSI e à troca do denominador.');
diario('Março a maio', 'A primeira pipeline, a Fase 3 e o denominador', [
  E('2026-03-12', 'Repositório criado com a primeira versão da pipeline',
    'Notebooks de auditoria de integridade, de cálculo do índice e de formatação final — a Fase 1, hoje guardada em Backup/ como legado.',
    'git log; GUIA_DO_PROJETO.md §5'),
  E('2026-03-16', 'Auditoria em SQLite: a contagem de colunas esperada é corrigida', null, 'git log'),
  E('2026-03-25', 'Variáveis multidimensionais', null, 'git log'),
  { data: 'mar–abr', fato: 'Programa de Inserção do IRR e Curso Introdutório',
    detalhe: 'Atividade do cronograma do bolsista; não deixa rastro no git.',
    nota: 'Fonte: GUIA_DO_PROJETO.md §11 (cronograma do bolsista).' },
  E('2026-05-06', 'Fase 2: o fluxo da análise multidimensional',
    'Extração, processamento e metodologia organizados; README reescrito; documentadas as inconsistências entre as variáveis de esgoto e os denominadores.',
    'git log'),
  E('2026-05-14', 'O GUIA_DO_PROJETO.md vira o documento mestre',
    'É onde cada decisão de método passa a ser registrada, com justificativa, verificação e status.',
    'git log; GUIA_DO_PROJETO.md'),
  E('2026-05-15', 'Fase 3: o filtro dos 70 municípios do ELSI-Brasil e a primeira EDA',
    'O Notebook 01 extrai e filtra os setores; o Notebook 02 faz a EDA pelo guia FIOCRUZ e pela metodologia oficial; renda com vírgula decimal e sigilo preservado nas proporções; relatório técnico (Markdown e Word) e o primeiro deck — ainda com o denominador V01042. Os legados vão para Backup/.',
    'git log'),
  E('2026-05-19', 'Correções de integridade depois da auditoria',
    'Com o relatório técnico de integridade (docs/relatorios/Relatorio_Integridade_Projeto.md).', 'git log'),
  E('2026-05-22', 'O denominador muda de V01042 para V00001; o analfabetismo vira taxa',
    'V00001 (domicílios particulares permanentes ocupados) é o equivalente exato do V002 que o IVS-BH 2012 usou no Censo 2010. O analfabetismo passa a V00901 ÷ (V00900 + V00901): a fórmula antiga, V00901 ÷ V00900, era razão e passava de 1 em alguns setores. Deck da revisão metodológica.',
    'git log; GUIA_DO_PROJETO.md §6.2.1 e §6.2.2'),
  E('2026-05-25', 'As bases dos 70 municípios e de Belo Horizonte vão para a orientadora',
    'Em banco_de_dados/entrega_orientadora/, com o README reescrito em tom mais direto.', 'git log'),
  E('2026-05-28', 'Deck das correções (commit 2fb2e30) e refatoração', null,
    'historico/2026-05-28_Correcoes_commit_2fb2e30.pptx; git log'),
  E('2026-05-30', 'Comparativo entre a EDA antiga e a nova; a EDA completa corrigida',
    'Dois decks, hoje em docs/Apresentacoes_IVS/historico/.', 'historico/; git log'),
], { fonte: 'Fonte: git log; GUIA_DO_PROJETO.md. Commits do dia nas anotações.' });

capitulo(2, 'Junho — a EDA cresce', 'O denominador novo em tudo, os indicadores descritivos e a caçamba que saiu e voltou.');
diario('Junho', 'Sincronização com V00001 e os indicadores novos', [
  E('2026-06-12', 'Tudo sincronizado com o denominador V00001',
    'Relatório de EDA regenerado (md e docx); Relatório de Integridade corrigido; divisão segura sem aviso; assimetria, curtose e duas correlações alinhadas ao CSV e à figura; deck completo revisado (o de 15/06 no histórico).',
    'git log'),
  E('2026-06-18', 'O dicionário oficial do IBGE entra no projeto',
    'As descrições das variáveis passam a vir da fonte oficial.', 'git log', /dicionario oficial/),
  E('2026-06-18', 'A caçamba (V00398) sai do lixo inadequado e volta no mesmo dia',
    'Fica como destino inadequado por fidelidade ao Cálculo IVS2012, em que só a coleta porta a porta (V00397) é adequada. A ressalva fica registrada: o lixo é a variável menos correlacionada com as demais.',
    'git log; GUIA_DO_PROJETO.md §6.2.10', /cacamba/),
  E('2026-06-18', 'Indicadores descritivos novos',
    'Habitação precária (domicílios improvisados e degradados), sem banheiro, responsável do sexo feminino (V01063), estrutura etária (crianças até 4 anos e idosos de 60 ou mais).',
    'git log', /^feat\(fase3\)/),
  E('2026-06-18', 'Cobertura, urbano/rural e morfologia',
    'Setores com 100% de cobertura (saneamento, dados, coleta de lixo); tabela urbano/rural (SITUACAO) nos três níveis; categorias de saneamento por banda e morfologia V00048–V00058 por região.',
    'git log', /^data\(eda\)/),
  E('2026-06-18', 'O deck extenso da EDA Fase 3, com as seis demandas adicionais', null,
    'historico/2026-06-18_EDA_Fase3_seis_demandas.pptx', /apresentacao/),
  E('2026-06-19', 'A pipeline comentada linha a linha; as versões fixadas',
    'Notebooks com outputs limpos; dependências com versão; procedência dos CSVs da EDA documentada.', 'git log'),
], { fonte: 'Fonte: git log; GUIA_DO_PROJETO.md §6.2. Commits do dia nas anotações.' });

capitulo(3, 'Julho e agosto — retomada e módulo', 'O primeiro grafo, as sete demandas de julho e o código que sai dos notebooks.');
diario('Julho e agosto', 'As demandas de julho, o módulo e a água', [
  E('2026-07-08', 'O primeiro grafo de conhecimento do projeto (graphify)',
    '28 arquivos lidos; o grafo entra no git em 16/07, com a documentação de uso.',
    'graphify-out/cost.json; git log'),
  { data: 'julho', fato: 'As sete demandas de julho da orientadora',
    detalhe: 'Índice de envelhecimento; tabela de variáveis com a fonte; excluir setores rurais; agrupar as moradias convencionais; indicador de apartamento; vilas e favelas; proporções para o Brasil todo.',
    nota: 'Fonte: GUIA_DO_PROJETO.md §6.4; docs/MANUAL_DO_PROJETO.md, parte C (uma subseção por demanda).' },
  E('2026-08-09', 'As sete demandas, implementadas',
    'IEP passa a 60+ ÷ menores de 15 (92,7 no recorte); 72 variáveis de 8 arquivos na tabela; recorte urbano com 104.108 setores (2,04% excluídos), aplicado na análise; 99,19% de moradias convencionais; apartamento (31,5%) fica fora do índice por não ter direção; FCU por CD_TIPO = 1: 19.452 setores no recorte (18,7%); a população do Brasil confere: 203.080.756.',
    'GUIA_DO_PROJETO.md §6.4; historico/2026-08-09_*.pptx'),
  E('2026-08-10', 'Atualização parcial do grafo',
    'Código e quatro figuras; dezesseis documentos ficaram pendentes.', 'graphify-out/cost.json'),
  E('2026-08-20', 'O módulo compartilhado src/ivs_censo',
    'As fórmulas dos indicadores num lugar só, em forma declarativa: o NB02, o cálculo nacional e a entrega usam a mesma definição.',
    'git log; GUIA_DO_PROJETO.md §6.2.12'),
  E('2026-08-21', 'Ambiente reprodutível; a água canalizada pelo complemento de V00199',
    'V00199, V00200 e V00201 fecham 100,00% de V00001 nos 81.270 setores com as três presentes; somar V00200 e V00201, que o IBGE sigila, deixaria 21,9% dos setores sem valor. Os notebooks passam a ler do módulo; o NB02 ganha a matriz 10 × 10.',
    'git log; GUIA_DO_PROJETO.md §6.2.9', /ambiente|canaliza|notebooks/),
  E('2026-08-21', 'Auditoria de renda, CSVs órfãos recuperados, testes de 43 para 59',
    'Tabelas da EDA regeneradas com os blocos de renda e de água; a publicação do IBGE sobre favelas e a planilha de FCU por setor nas fontes; a EDA Central (1ª rodada), com roteiro; as decisões de agosto registradas.',
    'git log', /scripts|test|data|fontes|apresentacoes|decisões/),
  E('2026-08-24', 'O primeiro diagnóstico fatorial (geração 1)',
    'scripts/diagnostico_fatorial.py mede a adequabilidade das bases candidatas à análise fatorial (resumo_adequabilidade.csv).',
    'banco_de_dados/eda/fatorial/README.md'),
], { fonte: 'Fonte: git log; GUIA_DO_PROJETO.md; graphify-out/cost.json. Commits do dia nas anotações.' });

capitulo(4, 'Setembro, primeira quinzena', 'A auditoria de agosto, a renda sem o extremo e a análise fatorial do NB04.');
diario('Setembro, 1 a 17', 'Auditoria, renda e o Notebook 04', [
  E('2026-09-02', 'A auditoria de agosto',
    'Proporções nacionais com numerador e denominador medidos nos mesmos setores; renda auditada com V06001/V06005 e o viés do sigilo parcial; a base de favelas completa separada do recorte de análise; regressões em teste.',
    'git log', /nacional|auditoria|favelas|test/),
  E('2026-09-02', 'A renda sem o extremo',
    'O setor 310620005650366, de Belo Horizonte, tinha renda média de R$ 170.418,06 por responsável: entra na entrega a coluna renda_media_sem_extremo; a 2ª rodada da EDA sai sem o extremo, com o seu deck, o critério de renda por extenso e o roteiro.',
    'git log; banco_de_dados/eda/atualizada/README.md', /renda|2ª rodada|roteiro|diagnóstico/),
  E('2026-09-02', 'A raiz de docs/Apresentacoes_IVS passa a ter um arquivo só',
    'O deck atual na raiz; o resto em complementos/ e em historico/, datado.', 'git log', /raiz/),
  E('2026-09-13', 'O livro da Enap e o plano do Notebook 04',
    'Guia de leitura da análise fatorial (Enap, 2019) e o plano de implementação do NB04.', 'git log'),
  E('2026-09-16', 'Estudo e plano de execução do NB04 registrados', null, 'git log'),
  E('2026-09-17', 'O NB04: a análise fatorial completa',
    `Módulo com rotação oblíqua, eixo principal e escores; KMO ${num(BASE.kmo, 4)}; IVS-6 com Varimax: `
    + `${num(BASE.pesos_ivs6_varimax_socioeconomica, 2)}% socioeconômica e ${num(BASE.pesos_ivs6_varimax_saneamento, 2)}% `
    + `saneamento; Φ da promax ${num(BASE.phi_promax, 4)}; AUC contra FCU: índice ${num(BASE.auc_indice, 4)} `
    + `× renda sozinha ${num(BASE.auc_renda_invertida_sozinha, 4)}.`,
    'banco_de_dados/eda/fatorial_ampliada/linha_de_base_nb04.csv', /fatorial|nb04/i),
  E('2026-09-17', 'Relatório, deck e as correções da primeira revisão',
    'Renda sem o extremo, reflexivo × formativo e o código em R; dois documentos de apoio (o guia e o plano de emergência); a EDA Central anexada ao fim do deck da fatorial; o extremo de renda medido por dentro de BH (4 slides).',
    'git log', /deck|apoio|anexa|extremo|reflexivo/),
  E('2026-09-17', 'A auditoria integral, de ponta a ponta',
    '22 achados, registrados em docs/relatorios/Auditoria_Integral_2026-09.md.',
    'git log; Revisao_Geral_2026-09.md ("Estado dos 22 achados")', /auditoria integral/),
  E('2026-09-17', 'docs/ em quatro subpastas, e a casa arrumada',
    'metodologia, relatorios, prompts e referencias; as bases da Fase 2 arquivadas; a procedência de 61 CSVs; o índice dos 18 executáveis; o NB04 comentado linha a linha.',
    'git log', /organiza|backup|procedência|índice|comenta/),
], { fonte: 'Fonte: git log; linha_de_base_nb04.csv. Commits do dia nas anotações.' });

capitulo(5, '25 de setembro — a revisão e as demandas', 'Um dia, 44 commits: a revisão geral e as seis fases das demandas de setembro.');
diario('25 de setembro', 'A revisão geral e as demandas de setembro', [
  E('2026-09-25', 'A revisão geral do repositório inteiro',
    '83 achados (92 brutos, 9 fundidos por serem o mesmo defeito visto de duas frentes); 17 deles introduzidos depois da auditoria de 17/09.',
    'docs/relatorios/Revisao_Geral_2026-09.md', /revisão geral/),
  E('2026-09-25', 'O plano de execução das demandas de setembro, em seis fases',
    'Da Fase 0 (linha de base) à Fase 5 (o resto da revisão, em lotes); o estado de cada fase em estado_demandas_2026-09.md.',
    'git log', /prompt/),
  E('2026-09-25', 'Fase 0 — linha de base e destravamentos',
    'A Varimax passa a parar pela variação da rotação (máx |ΔR| < 10⁻¹⁰), não antes de convergir; a razão agregada nacional de pct_sem_agua_canalizada passa a aplicar o complemento (0,986 → 0,0138); a regra banco_de_dados/*.csv volta ao .gitignore; a linha de base do NB04 é gravada.',
    'estado_demandas_2026-09.md', /Varimax|complemento|gitignore|linha de base/),
  E('2026-09-25', 'Fases 1 e 2 — renda, quadro e a fatorial ampliada',
    `A renda imputada com a mediana municipal (${reais(medianaMun)} no setor extremo); o quadro de ${QUADRO.length} indicadores; a grade de cenários S0–S7 sem bootstrap, com as três rendas e os postos no município.`,
    'estado_demandas_2026-09.md', /mediana|quadro|rodar_cenario|grade/),
  E('2026-09-25', 'Fases 3 e 4 — o NB04 corrigido, o 04b e os slides',
    'O NB04 regerado com a Varimax corrigida; o Notebook 04b em sete blocos; inventário e roteiro do deck; o juntador de decks recriado; três números errados corrigidos nos slides (AUD-07, DEC-1, AUD-04) e o guia de apoio com 16.548 no lugar de 16.563 (AUD-08); o bloco da fatorial ampliada anexado.',
    'estado_demandas_2026-09.md', /nb04|04b|apresentacao|Fase 3|Fase 4/),
  E('2026-09-25', 'Fase 5 — o resto da revisão, em quatro lotes',
    'A: escores oblíquos, Heywood e cauda do qui-quadrado (FAT-04, FAT-06, FAT-12) e astype(str) == \'1\' trocado por comparação numérica em cinco lugares. B: testes da promax, de Bartlett, de Horn e do bootstrap. C: documentação. D: package.json versionado, dependências declaradas, o gerador do dicionário resgatado.',
    'estado_demandas_2026-09.md', /Fase 5|^fix\(F2\)|FAT-|^teste|HIG-(0[89]|1\d)|lote|package|requirements/),
], { fonte: 'Fonte: git log; Revisao_Geral_2026-09.md; estado_demandas_2026-09.md.',
     abertura: 'Os 44 commits de 25/09 estão divididos pelos itens; cada nota lista os do item.' });

capitulo(6, '26 e 27 de setembro — os testes e o IVS final', 'Os nove itens da etapa seguinte: as variantes de cada escolha, o banheiro graduado e o Notebook 05.');
diario('26 e 27 de setembro', 'Fases A a D: do banheiro graduado ao NB05', [
  E('2026-09-26', 'O plano dos testes de especificação e do NB05',
    'Nove itens: as rendas, as rotações, os pesos na solução oblíqua, o lixo, o banheiro graduado, o motor de especificações, o que estava inferido sem verificação, as pendências pequenas e o Notebook 05.',
    'estado_nb05_2026-09.md', /prompt/),
  E('2026-09-26', 'Fase A — o que estava inferido vira verificação; as pendências pequenas',
    'O caminho de saída do gerador do dicionário; o slide 45 da EDA Central; os scripts eda reexecutados depois da troca do filtro; os arquivos únicos das worktrees órfãs resgatados.',
    'estado_nb05_2026-09.md', /HIG-08|EDA-Central|Fase A|worktrees/),
  E('2026-09-26', 'Fase B — a V00237 e o banheiro graduado',
    `A V00237 extraída do Censo; a partição fecha: V00495 = V00236 + V00237 + V00238 em ${mil(nBate)} `
    + `de ${mil(nPresentes)} setores com as quatro presentes; o indicador graduado é (1·V00236 + 2·V00237 + 3·V00238) `
    + `÷ (3·V00001); a entrega regenerada com ${nColunasEntrega} colunas.`,
    'banco_de_dados/eda/fatorial_ampliada/banheiro_particao.csv', /banheiro|entrega|contagens/),
  E('2026-09-27', 'Fase C — o motor de especificações',
    `${ESP.length} especificações (${nBases} bases × ${nEsquemas} esquemas de peso × ${nNorm} normalizações); `
    + `${eleg.length} elegíveis pelos critérios fixados antes de rodar; a referência proposta e três leituras alternativas.`,
    'banco_de_dados/eda/ivs_especificacoes/especificacoes.csv', /motor|especificacoes|Fase C/),
  E('2026-09-27', 'Fase D — o Notebook 05, o relatório e os slides',
    `O NB05 gerado e executado por nbformat e nbclient; o relatório com números só de CSV; os slides do IVS final anexados ao deck da fatorial (hoje com ${nSlidesDeckAtual} slides).`,
    'git log', /nb05|relatorio|NB05|Fase D/),
  E('2026-09-27', 'As cinco worktrees órfãs vão para a Lixeira',
    '597 MB, movidos pelo Terminal (mv, nunca rm), depois de resgatados os dois arquivos únicos.',
    'estado_nb05_2026-09.md, pós-Fase D', /worktree/),
], { fonte: 'Fonte: git log; estado_nb05_2026-09.md; CSVs de ivs_especificacoes/. Commits do dia nas anotações.' });

capitulo(7, 'De 30/09 até hoje', 'A estrutura do deck, o grafo do projeto e estas duas apresentações.');
diario('De 30/09 até hoje', 'O deck consertado e o grafo que lê os documentos', [
  E('2026-09-30', 'A estrutura do deck consertada',
    'Master registrado duas vezes, colisão de identificador e layouts órfãos; juntar_decks.py ganha a etapa que conserta a estrutura e três testes.',
    'git log', /juntar|deck/),
  E('2026-09-30', 'O grafo do código e o que o grafo não lê',
    '.graphifyignore: dados, figuras, arquivos do Office, PDFs gerados e o Backup/ ficam de fora.', 'git log', /graphify/),
  E('2026-10-01', 'O grafo lê os documentos',
    `${mil(gNos)} nós, ${mil(gArestas)} arestas e ${gComunidades} comunidades: o código, os documentos e os dois PDFs de referência num mapa só.`,
    'graphify-out/graph.json', /graphify/),
  { data: '01/10', fato: 'O branch principal passa a se chamar main', detalhe: null,
    nota: 'Fonte: git reflog ("checkout: moving from master to main", 01/10/2026).' },
  { data: dm(HOJE), fato: 'Estas duas apresentações',
    detalhe: 'A cronologia (esta) e a das demandas de setembro, geradas por script a partir do git e dos CSVs.',
    nota: 'scripts/gerar_deck_cronologia.js e scripts/gerar_deck_demandas_setembro.js.' },
], { fonte: 'Fonte: git log; graphify-out/graph.json. Commits do dia nas anotações.' });

// ── Leituras transversais ────────────────────────────────────────────────────
capitulo(8, 'As decisões de método, em ordem', 'O que foi decidido, quando, e o que ficou para a orientadora.');
{
  const s = S();
  const y = titulo(s, 'As decisões consolidadas do GUIA', 'GUIA_DO_PROJETO.md §6.2 — a data é a do commit ou a registrada no GUIA');
  tabelaAjustada(s, ['§', 'Decisão', 'Quando'], [
    ['6.2.1', 'Denominador domiciliar: V00001, não V01042', '22/05'],
    ['6.2.2', 'Analfabetismo: V00901 ÷ (V00900 + V00901), uma taxa', '22/05'],
    ['6.2.3', 'Razão de moradores: (V00005 + V00006) ÷ (V00001 + V00002), como o V0005 do IBGE', '—'],
    ['6.2.4', 'Dados_sig avaliado na ordem ZERADO → SIGILOSO → COLETIVO → OK', '—'],
    ['6.2.5', 'Recorte urbano aplicado na análise, não na extração', '09/08'],
    ['6.2.6', 'Sigilo do IBGE vira ausente, nunca zero; o analfabetismo não é imputado', '—'],
    ['6.2.7', 'Envelhecimento: IEP = 60+ ÷ menores de 15 (Galvão et al., 2025)', '09/08'],
    ['6.2.8', 'Favela e comunidade urbana: CD_TIPO = 1', '09/08'],
    ['6.2.9', 'Água canalizada pelo complemento de V00199', '21/08'],
    ['6.2.10', 'A caçamba (V00398) é destino inadequado, como no IVS-BH 2012', '18/06'],
    ['6.2.11', 'Indicadores descritivos ficam fora do índice', '09/08'],
    ['6.2.12', 'As fórmulas vivem no módulo compartilhado src/ivs_censo', '20/08'],
  ], { y: y + 0.02, colW: [0.85, 9.3, 1.48], fontSize: 12.5, rowH: 0.33 });
  procedencia(s, 'Fonte: GUIA_DO_PROJETO.md §6.2; “—”: o GUIA não registra a data e nenhum commit a isola.');
  s.addNotes('Cada decisão tem, no GUIA, a justificativa, a alternativa descartada e a verificação. '
    + 'Três princípios orientam todas (GUIA §6.1), o primeiro deles a fidelidade à metodologia-fonte, '
    + 'o IVS-BH 2012 — é por ele que a caçamba ficou como destino inadequado, apesar da ressalva empírica.');
}
{
  const s = S();
  const y = titulo(s, 'As regras de setembro, e o que não é decisão minha', 'Fixadas antes de rodar a grade do NB05');
  const w = 5.55, x2 = M + 6.05;
  bloco(s, M, y + 0.15, w, 'Elegibilidade.', 'KMO ≥ 0,70; MSA mínimo ≥ 0,50; comunalidade mínima '
    + '≥ 0,30; maior carga de cada variável ≥ 0,40. Especificação que falha em um critério não entra.',
    false, 1.3);
  bloco(s, M, y + 1.55, w, 'Escolha.', 'Entre as elegíveis, a de melhor posição média em três '
    + 'critérios de peso igual: estabilidade (deixando um município de fora), AUC contra FCU dentro '
    + 'do município e parcimônia.', false, 1.3);
  bloco(s, M, y + 2.95, w, 'Incerteza.', 'Sensibilidade por município, deixando um de fora por vez, '
    + 'em vez de bootstrap. Números só de CSV, em todo documento e slide.', false, 1.1);
  bloco(s, x2, y + 0.15, w, 'Fica com a orientadora.', 'Qual renda (original, sem o extremo, '
    + 'mediana municipal); qual rotação; como dividir os pesos na solução oblíqua; se o lixo entra; '
    + 'se o banheiro entra, e em qual versão; a normalização (no município ou global); a regra das '
    + 'faixas (IVS-BH 2012 ou quartis). O NB05 responde cada uma com números, sem fechar nenhuma.',
    true, 2.4);
  procedencia(s, 'Fonte: Relatorio_IVS_Final_NB05.md (Método); estado_nb05_2026-09.md.');
  s.addNotes('Os critérios de elegibilidade e de escolha foram escritos no plano do NB05 antes '
    + 'de a grade rodar, para não escolher a especificação pelo resultado. O critério de '
    + 'estabilidade, porém, degenera nos pesos fixos (50/50 e 60/40): a amplitude do peso de F1 é '
    + 'zero por construção — é a principal razão para desconfiar da referência proposta.');
}

capitulo(9, 'Os achados, em ordem', 'O que se descobriu sobre os dados e sobre o próprio código, na ordem em que apareceu.');
diario('Os achados', 'Dos dados e do código, na ordem em que apareceram', [
  E('2026-05-22', 'A taxa de analfabetismo antiga passava de 1',
    'V00901 ÷ V00900 é razão entre analfabetos e alfabetizados, não taxa.', 'GUIA_DO_PROJETO.md §6.2.2'),
  E('2026-06-18', 'O lixo é a variável que menos conversa com as outras',
    'A única em que o recorte ELSI está pior que o Brasil urbano; a ressalva acompanha a decisão da caçamba.',
    'GUIA_DO_PROJETO.md §6.2.10', /cacamba/),
  E('2026-08-09', 'Quase um em cada cinco setores urbanos do recorte é favela ou comunidade urbana',
    '19.452 setores (18,7%); CD_TIPO = 1 e NM_FCU coincidem nos 468.099 setores do país.',
    'GUIA_DO_PROJETO.md §6.2.8 e §6.4'),
  E('2026-08-21', 'Água: as três variáveis fecham o total',
    'V00199 + V00200 + V00201 = V00001 em 100,00% dos 81.270 setores com as três presentes.',
    'GUIA_DO_PROJETO.md §6.2.9', /canaliza/),
  E('2026-09-02', 'Um setor de BH com renda média de R$ 170.418,06',
    'Sozinho, ele muda o reescalonamento min-max da renda de todos os setores; daí a coluna sem o extremo e, em setembro, a mediana municipal.',
    'banco_de_dados/eda/atualizada/README.md; Revisao_Geral_2026-09.md', /renda/),
  E('2026-09-17', 'O índice do NB04 separa as favelas pior que a renda sozinha',
    `AUC ${num(BASE.auc_indice, 4)} contra ${num(BASE.auc_renda_invertida_sozinha, 4)}; a média simples dos postos, `
    + `sem peso nenhum, fica em ${num(BASE.auc_media_postos_pesos_iguais, 4)}.`,
    'linha_de_base_nb04.csv', /nb04/i),
  E('2026-09-25', 'A Varimax parava antes de convergir',
    'FAT-01: agora para quando a rotação deixa de variar (máx |ΔR| < 10⁻¹⁰); o NB04 foi regerado.',
    'Revisao_Geral_2026-09.md; estado_demandas_2026-09.md', /Varimax/),
  E('2026-09-25', 'A proporção nacional de “sem água canalizada” saía pelo avesso',
    'A razão agregada não aplicava o complemento: 0,986 em vez de 0,0138 (IND-1).',
    'estado_demandas_2026-09.md', /complemento/),
  E('2026-09-25', 'Sem o lixo, a fatorial pede um fator só',
    (cen('S1').fatores_kaiser === cen('S1').fatores_horn
      ? `No IVS-6 (S1), Kaiser e Horn indicam ${cen('S1').fatores_kaiser} fator; `
      : `No IVS-6 (S1), Kaiser indica ${cen('S1').fatores_kaiser} e Horn ${cen('S1').fatores_horn}; `)
    + 'com o lixo (S0), ele forma um fator próprio.', 'fatorial_ampliada/cenarios.csv', /grade/),
  E('2026-09-26', 'A partição do banheiro é exata',
    `V00495 = V00236 + V00237 + V00238 em ${mil(nBate)} de ${mil(nPresentes)} setores.`,
    'fatorial_ampliada/banheiro_particao.csv', /banheiro/),
  E('2026-09-27', 'O IVS-7 do NB04 não passa nos critérios',
    `A comunalidade da água fica em ${num(ivs7.comunalidade_min, 3)}, abaixo de 0,30; sem o lixo, ou com a V00495, a fatoração passa.`,
    'ivs_especificacoes/especificacoes.csv', /motor|especificacoes/),
  E('2026-09-27', 'A renda sozinha vence o índice em todas as especificações elegíveis',
    `Global em ${rendaVenceGlobal} de ${ACR.length} e no município em ${rendaVenceMun} de ${ACR.length}; `
    + `dentro dos decis de renda de cada município, o índice separa melhor em ${indiceVenceEstratos} de ${ACR.length}.`,
    'ivs_especificacoes/acrescimo_renda.csv', /especificacoes/),
  E('2026-09-27', 'O critério de estabilidade degenera nos pesos fixos',
    'Com 50/50 ou 60/40 a amplitude do peso de F1 é zero por construção — e é isso que decide a referência proposta.',
    'ivs_especificacoes/referencia.csv; Relatorio_IVS_Final_NB05.md', /especificacoes/),
], { fonte: 'Fonte: nas anotações, item a item.' });

capitulo(10, 'A organização, em ordem', 'Como o repositório chegou à forma de hoje: pastas, módulo, testes, documentação e apresentações.');
diario('A organização', 'Do notebook solto ao repositório que se explica', [
  E('2026-05-14', 'Um documento mestre', 'O GUIA_DO_PROJETO.md concentra identidade, método, decisões e plano.', 'git log'),
  E('2026-05-15', 'O legado vai para Backup/',
    'As Fases 1 e 2 ficam como histórico; a pipeline ativa passa a ser notebooks/Fase3_EDA_ELSI/.',
    'git log; GUIA_DO_PROJETO.md §5', /Backup|backup|legados/),
  E('2026-06-19', 'Versões fixadas e procedência dos CSVs', null, 'git log', /versoes/),
  E('2026-08-20', 'O código sai dos notebooks', 'src/ivs_censo para as fórmulas; scripts/ para os executáveis.', 'git log'),
  E('2026-08-21', 'O ambiente roda do zero; 59 testes', null, 'git log', /ambiente|test/),
  E('2026-09-02', 'Uma apresentação na raiz; o resto datado', 'complementos/ para o apoio, historico/ para o que saiu de circulação.', 'git log', /raiz/),
  E('2026-09-17', 'docs/ por tipo de uso',
    'metodologia/, relatorios/, prompts/, referencias/ e Apresentacoes_IVS/; o índice dos executáveis em scripts/README.md; a procedência de 61 CSVs.',
    'git log', /organiza|índice|procedência/),
  E('2026-09-25', 'O repositório limpo',
    'package.json versionado; estrutura_projeto.md regerada a partir de git ls-files.',
    'git log', /package|estrutura_projeto/),
  E('2026-09-27', 'As worktrees órfãs fora; os decks montados por script',
    'O juntador de decks acrescenta blocos ao deck atual sem regerá-lo.', 'estado_nb05_2026-09.md', /D\.3/),
  E('2026-10-01', 'O grafo do projeto e o branch main', 'Um mapa navegável do código e dos documentos, para achar onde cada coisa está.', 'git log', /graphify/),
], { fonte: 'Fonte: git log. Commits do dia nas anotações.' });
{
  const s = S();
  const y = titulo(s, 'O repositório hoje', `Pastas, o que guardam e quantos arquivos têm no git (${dma(HOJE)})`);
  const PASTAS = [
    ['notebooks/Fase3_EDA_ELSI/', 'A pipeline ativa: NB01, NB02, NB04, NB04b e NB05'],
    ['src/ivs_censo/', 'Código compartilhado: fontes, indicadores, renda, fatorial'],
    ['scripts/', 'Executáveis: entrega, auditorias, fatorial, NB05, decks'],
    ['tests/', `Testes (pytest): ${nTestes} coletados`],
    ['banco_de_dados/', 'Saídas: entrega à orientadora, EDA, fatorial, NB05, nacional'],
    ['docs/metodologia/', 'Guias de leitura e notas de método'],
    ['docs/relatorios/', 'Relatórios: EDA, integridade, NB04, NB05, auditorias'],
    ['docs/prompts/', 'Planos de execução e os arquivos de estado de cada fase'],
    ['docs/referencias/', 'Material de terceiros (IVS-BH 2012, plano de trabalho)'],
    ['docs/Apresentacoes_IVS/', 'O deck atual na raiz; complementos/ e historico/'],
    ['Backup/', 'Legado: Fases 1 e 2, denominador V01042'],
    ['graphify-out/', 'O grafo de conhecimento do projeto'],
  ];
  tabelaAjustada(s, ['Pasta', 'O que guarda', 'Arquivos no git'],
    PASTAS.map(([dir, txt]) => [dir, txt, String(noGit(dir))]),
    { y: y + 0.02, colW: [3.3, 6.6, 1.73], fontSize: 12.5, rowH: 0.33 });
  procedencia(s, 'Fonte: git ls-files, na hora da geração; testes: pytest --collect-only.');
  s.addNotes('A pasta dados/ (entrada bruta do IBGE, 2,4 GB) não está no git. O mapa completo, '
    + 'pasta por pasta, está em docs/MANUAL_DO_PROJETO.md, parte A, e a árvore em estrutura_projeto.md.');
}

capitulo(11, 'Onde o projeto está', 'O cronograma contra o que foi feito, e o que vem depois.');
{
  const s = S();
  const y = titulo(s, 'O cronograma contra o realizado', `Situação em ${dma(HOJE)}`);
  tabelaAjustada(s, ['Etapa', 'Previsto', 'Onde está'], [
    ['Consistência do banco de dados', 'mar–jul', 'Feita: auditorias de maio, agosto e setembro; revisão geral com 83 achados'],
    ['Análise descritiva (EDA)', 'mar–set', 'Feita: NB02 e a EDA Central em duas rodadas'],
    ['Demandas de julho (7)', '—', 'Feitas em 09/08'],
    ['Demandas de setembro (11) e os 9 itens seguintes', '—', 'Feitos de 25 a 27/09; respostas da orientadora pendentes'],
    ['Cálculo do IVS: fatorial, pesos, normalização', 'ago–set', `NB04, NB04b e NB05: ${eleg.length} especificações elegíveis e uma referência proposta; as escolhas são da orientadora`],
    ['Faixas de risco', 'set', 'Calculadas no NB05 para a referência, pelas duas regras; a regra a decidir'],
    ['Mapas temáticos (QGIS)', 'set', 'Pendentes'],
    ['Artigo científico', 'out–dez', 'Plano preenchido; redação pendente'],
    ['Relatório Final de IC', 'dez–fev', 'A começar'],
  ], { y: y + 0.02, colW: [4.0, 1.25, 6.38], fontSize: 12.5, rowH: 0.36 });
  procedencia(s, 'Fonte: GUIA_DO_PROJETO.md §8 e §11; Relatorio_IVS_Final_NB05.md.');
  s.addNotes('O GUIA §8 ainda marca o NB05, a normalização municipal e as faixas como pendentes; '
    + 'o NB05 já calcula as três coisas para a especificação de referência. O que falta é a '
    + 'escolha — e ela é da orientadora.');
}
{
  const s = S();
  const y = titulo(s, 'O que vem depois', 'Na ordem em que um passo destrava o seguinte');
  const passos = [
    ['1. As escolhas da orientadora.', 'Renda, rotação, pesos na oblíqua, lixo, banheiro, normalização e faixas — com os números do NB05 ao lado de cada pergunta.'],
    ['2. O IVS final fechado.', 'Rodar a especificação escolhida, gravar o índice e as faixas por setor e conferir contra a referência proposta.'],
    ['3. Os mapas temáticos.', 'O IVS e as faixas por setor no QGIS, município a município.'],
    ['4. O artigo.', 'Na ordem do plano: tabelas, método, resultados, discussão, introdução e resumo (checklist STROBE).'],
    ['5. O relatório final de IC.', 'De dezembro a fevereiro, com a submissão do artigo em fevereiro de 2027.'],
  ];
  let yy = y + 0.12;
  passos.forEach(([e, t], i) => {
    bloco(s, M, yy, W - 2 * M - 1.0, e, t, i === 0, 0.7);
    yy += 0.86;
  });
  procedencia(s, 'Fonte: GUIA_DO_PROJETO.md §10–§12; Relatorio_IVS_Final_NB05.md (perguntas à orientadora).');
  s.addNotes('As perguntas à orientadora, com os números de cada uma, estão no deck das demandas '
    + 'de setembro (complementos/Demandas_Setembro_IVS_2026-10.pptx) e no relatório do NB05.');
}

// Fecho: de onde saiu este deck
{
  const s = S();
  const y = titulo(s, 'De onde saiu esta cronologia', 'Para refazer, conferir ou continuar');
  tabelaAjustada(s, ['Fonte', 'O que deu'], [
    ['git log', `${LOG.length} commits, de ${dma(PRIMEIRO)} a ${dma(ULTIMO)}; datas, contagens, tipos e as notas de cada item`],
    ['GUIA_DO_PROJETO.md', 'Identidade, objetivo, decisões de método (§6.2), demandas de julho (§6.4), cronograma (§11)'],
    ['fatorial_ampliada/*.csv', 'Linha de base do NB04, cenários S0–S7, partição do banheiro'],
    ['ivs_especificacoes/*.csv', 'Grade do NB05, referência proposta, o índice contra a renda'],
    ['estado_demandas e estado_nb05 (2026-09)', 'O que cada fase de setembro fez, e quando'],
    ['docs/relatorios/', 'Revisão geral, auditoria integral, relatórios do NB04 e do NB05'],
    ['graphify-out/', 'O tamanho do grafo do projeto e as datas das suas leituras'],
  ], { y: y + 0.05, colW: [3.2, 8.43], fontSize: 12.5, rowH: 0.36 });
  s.addText(`Gerado por scripts/gerar_deck_cronologia.js em ${dma(HOJE)}. Para refazer: `
    + 'node scripts/gerar_deck_cronologia.js', { x: M, y: H - 1.35, w: W - 2 * M, h: 0.4,
    fontFace: FONTE, fontSize: 11, italic: true, color: CINZA, margin: 0 });
  s.addNotes('O deck não tem número digitado que exista em CSV: se um CSV mudar, basta rodar o '
    + 'gerador de novo. Os fatos que só existem em documento estão citados no pé de cada slide.');
}

d.p.writeFile({ fileName: SAIDA }).then(f => console.log('deck escrito:', f));
