/**
 * Gera os slides da análise do setor extremo de renda em Belo Horizonte.
 *
 * Saem num .pptx separado, de propósito: o deck principal foi EDITADO À MÃO (slides
 * removidos, marcações "EXPLICAR SLIDE") e depois teve a EDA Central anexada. Regerá-lo
 * apagaria tudo isso. Estes slides são então ANEXADOS ao deck, pelo mesmo caminho que a
 * EDA Central seguiu.
 *
 * Nenhum número é digitado: todos saem de banco_de_dados/eda/atualizada/extremo_bh_*.csv.
 *
 * Uso:
 *     node scripts/gerar_slides_extremo_bh.js <saida.pptx>
 */
const fs = require('fs');
const path = require('path');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const ATU = path.join(RAIZ, 'banco_de_dados/eda/atualizada');

function lerCsv(nome) {
  const txt = fs.readFileSync(path.join(ATU, nome), 'utf8').replace(/^﻿/, '').trim();
  const [cab, ...linhas] = txt.split(/\r?\n/);
  const cols = cab.split(';').map(c => (c === '' ? 'idx' : c));
  return linhas.map(l => Object.fromEntries(cols.map((c, i) => [c, l.split(';')[i]])));
}
const n = (v, c) => Number(v).toFixed(c === undefined ? 2 : c).replace('.', ',');
const inteiro = v => Math.round(Number(v)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');

const DESC = lerCsv('extremo_bh_descritivas.csv');
const NORM = lerCsv('extremo_bh_normalizacao.csv')[0];
const RANK = lerCsv('extremo_bh_ranking.csv');
const val = (rec, med, col) => DESC.find(r => r.recorte === rec && r.medida === med)[col];
const bh = (med, col) => val('Belo Horizonte', med, col);
const elsi = (med, col) => val('70 municípios ELSI', med, col);
const mudaram = RANK.filter(r => Number(r.mudou) !== 0).length;

const d = criarDeck({ titulo: 'O setor extremo de renda em Belo Horizonte' });
const { p, S, titulo, secao, bloco, numero, tabela, legendaTabela, legendaFigura, capa } = d;
const { TINTA, CINZA, ACENTO } = d.cores;
const { W, H, M } = d.geo;
const marca = t => ({ text: t, options: { color: ACENTO, bold: true } });

// ── divisória ───────────────────────────────────────────────────────────────
{ const s = S();
  secao(s, '+', 'O extremo de renda, por dentro',
    'A demanda da orientação, levada até onde ela de fato morde: o município do setor.');
  s.addNotes('Esta análise é posterior à 2ª rodada da EDA. A 2ª rodada mediu o efeito do extremo no AGREGADO dos 70 municípios, onde ele é quase nulo. Faltava medir dentro de Belo Horizonte, que é onde o setor está — e faltava a consequência metodológica, que é a mais séria.');
}

// ── slide 1: o efeito muda de ordem de grandeza conforme o recorte ──────────
{ const s = S();
  const y = titulo(s, 'O mesmo setor, dois efeitos de tamanhos diferentes',
    'No agregado dos 70 municípios ele quase não aparece. Dentro do município dele, aparece muito.');
  const yt = legendaTabela(s, y, 'Efeito de excluir o setor 310620005650366, por recorte.',
    'Fonte: banco_de_dados/eda/atualizada/extremo_bh_descritivas.csv · variação percentual ao retirar o setor.');
  tabela(s, ['Medida', 'Belo Horizonte', '70 municípios ELSI', 'quantas vezes maior em BH'], [
    ['Média', `${n(bh('media','variacao_pct'))}%`, `${n(elsi('media','variacao_pct'))}%`,
      `${n(Math.abs(bh('media','variacao_pct') / elsi('media','variacao_pct')), 0)}×`],
    ['Desvio-padrão', marca(`${n(bh('dp','variacao_pct'))}%`), `${n(elsi('dp','variacao_pct'))}%`,
      `${n(Math.abs(bh('dp','variacao_pct') / elsi('dp','variacao_pct')), 0)}×`],
    ['Coef. de variação', marca(`${n(bh('cv_pct','variacao_pct'))}%`), `${n(elsi('cv_pct','variacao_pct'))}%`,
      `${n(Math.abs(bh('cv_pct','variacao_pct') / elsi('cv_pct','variacao_pct')), 0)}×`],
    ['Máximo', `${n(bh('max','variacao_pct'))}%`, `${n(elsi('max','variacao_pct'))}%`, '—'],
    ['Mediana', `${n(bh('mediana','variacao_pct'))}%`, `${n(elsi('mediana','variacao_pct'))}%`, '—'],
  ], { y: yt, colW: [3.2, 2.7, 2.9, 2.83], rowH: 0.44, fontSize: 11.5 });
  numero(s, M, yt + 2.95, 4.0, 'R$ ' + inteiro(170418), 'a renda do setor, por responsável', true);
  numero(s, M + 4.6, yt + 2.95, 4.0, 'R$ ' + inteiro(3058), 'a mediana de Belo Horizonte sem ele');
  numero(s, M + 9.2, yt + 2.95, 2.4, '56×', 'a razão entre as duas');
  s.addNotes(`A leitura é esta: o efeito de um único setor depende inteiramente do recorte em que se olha. Em ${inteiro(elsi('n','com_extremo'))} setores ele move a média em 0,04% e por isso a 2ª rodada concluiu, com razão, que o agregado é robusto. Mas dentro de Belo Horizonte ele derruba o desvio-padrão em 14% e o máximo em 73%. A mediana quase não se move nos dois casos, o que é a assinatura de um outlier: ele desloca média e dispersão, não o centro.`);
}

// ── slide 2: a consequência metodológica ────────────────────────────────────
{ const s = S();
  const y = titulo(s, 'A consequência que ninguém tinha medido',
    'O IVS normaliza a renda por min-max DENTRO de cada município. Um máximo distorcido comprime todo o resto.');
  bloco(s, M, y + 0.2, W - 2*M, 'Por que isto importa mais do que a descritiva.',
    `O índice é intraurbano: cada variável é posta numa escala de 0 a 1 usando o mínimo e o máximo DAQUELE município. Se o máximo de Belo Horizonte é R$ 170 mil e o segundo maior é R$ ${Number(bh('max','sem_extremo')).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}, todos os outros 5 mil setores são empurrados contra o zero — e deixam de se distinguir entre si.`, true, 1.15);
  numero(s, M, y + 1.6, 3.8, n(NORM.norm_media_com, 4).replace('0,', '0,'),
    'renda normalizada média em BH, COM o extremo');
  numero(s, M + 4.3, y + 1.6, 3.8, n(NORM.norm_media_sem, 4),
    'a mesma, SEM o extremo', true);
  numero(s, M + 8.6, y + 1.6, 3.0, `${n(Number(NORM.norm_media_sem)/Number(NORM.norm_media_com), 1)}×`,
    'quanto a escala se abre');
  const yt = legendaTabela(s, y + 2.95, 'Setores de Belo Horizonte comprimidos contra o zero.',
    'Fonte: extremo_bh_normalizacao.csv · min-max municipal sobre ' + inteiro(NORM.setores_de_bh) + ' setores.');
  tabela(s, ['', 'Com o extremo', 'Sem o extremo', 'diferença'], [
    ['Setores abaixo de 0,05 na escala',
      inteiro(NORM.setores_abaixo_de_0_05_com), inteiro(NORM.setores_abaixo_de_0_05_sem),
      marca(inteiro(Number(NORM.setores_abaixo_de_0_05_com) - Number(NORM.setores_abaixo_de_0_05_sem)) + ' setores')],
    ['Amplitude usada na normalização',
      'R$ ' + inteiro(NORM.amplitude_usada_com), 'R$ ' + inteiro(NORM.amplitude_usada_sem),
      `−${n(100*(1 - Number(NORM.amplitude_usada_sem)/Number(NORM.amplitude_usada_com)), 0)}%`],
  ], { y: yt, colW: [4.8, 2.4, 2.4, 2.03], rowH: 0.42, fontSize: 11.5 });
  s.addNotes(`Este é o achado da análise, e ele é metodológico, não descritivo. Um único dado provavelmente errado estava achatando a escala de renda de ${inteiro(NORM.setores_abaixo_de_0_05_com - NORM.setores_abaixo_de_0_05_sem)} setores de Belo Horizonte — que apareciam como se tivessem renda praticamente idêntica quando não têm. Como o IVS classifica território em quatro faixas, achatar a escala de ${n(100*(NORM.setores_abaixo_de_0_05_com - NORM.setores_abaixo_de_0_05_sem)/NORM.setores_de_bh, 0)}% do município tem consequência direta sobre quem seria apontado como vulnerável. Vale dizer também o que NÃO muda: no ranking dos 70 municípios por renda média, Belo Horizonte continua em 7º e nenhum município troca de posição. O agregado é robusto; o intramunicipal não era.`);
}

// ── slide 3: a figura ───────────────────────────────────────────────────────
{ const s = S();
  titulo(s, 'O extremo e o que ele faz com a escala',
    'À esquerda, a renda de Belo Horizonte. À direita, o efeito na normalização municipal.');
  s.addImage({ path: path.join(ATU, 'figuras', 'extremo_bh.png'), x: 0.9, y: 1.6, w: 11.53, h: 4.51 });
  legendaFigura(s, 6.25, 'A renda por setor em Belo Horizonte e a escala normalizada, com e sem o extremo.',
    'Fonte: eda/atualizada/figuras/extremo_bh.png · scripts/eda_extremo_belo_horizonte.py.');
  s.addNotes('No painel da esquerda, o extremo nem cabe no quadro: o eixo vai até R$ 30 mil e ele está em R$ 170 mil. No da direita está o argumento inteiro — a distribuição vermelha, com o extremo, é um pico esmagado contra o zero; a verde, sem ele, se espalha e volta a distinguir os setores entre si. É a mesma cidade, medida duas vezes.');
}

const saida = process.argv[2];
if (!saida) { console.error('uso: node scripts/gerar_slides_extremo_bh.js <saida.pptx>'); process.exit(1); }
p.writeFile({ fileName: saida }).then(f => console.log('slides escritos:', f));
