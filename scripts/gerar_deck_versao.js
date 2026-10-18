#!/usr/bin/env node
/**
 * Gerador único dos decks das análises exploratórias por versão.
 *
 *     node scripts/gerar_deck_versao.js analises_exploratorias/<versao>
 *
 * Lê o `catalogo.csv`, as tabelas e o `textos.json` da versão, mais os modelos de
 * `analises_exploratorias/_modelos/textos_blocos.json`, e grava `<versao>/<versao>.pptx`.
 * Não calcula nada: todo número vem de um CSV gravado pelo motor (`scripts/eda_versoes.py`);
 * o gerador só escolhe linhas e colunas, reordena e formata. Ao fim, grava no
 * `catalogo.csv` o slide de cada item.
 *
 * Ordem do deck (seção 2.6 do prompt das versões): capa · o que muda · recorte · sumário ·
 * para cada bloco, a abertura e um slide por tabela e por figura (tabela longa vai
 * paginada) · síntese · candidatos ao artigo · limitações · dicionário dos indicadores.
 */
const fs = require('fs');
const path = require('path');
const { criarDeck } = require('./deck_comum');

const RAIZ = path.resolve(__dirname, '..');
const MODELOS = path.join(RAIZ, 'analises_exploratorias', '_modelos', 'textos_blocos.json');
const REFERENCIA = path.join(RAIZ, 'analises_exploratorias', '00_referencia');
const QUADRO = path.join(RAIZ, 'banco_de_dados', 'entrega_orientadora', 'Quadro_Indicadores.csv');
const REGIOES = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'];
const FAIXA = { baixo: 'baixo', medio: 'médio', elevado: 'elevado', muito_elevado: 'muito elevado',
                indefinida: 'indefinida' };
const MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto',
               'setembro', 'outubro', 'novembro', 'dezembro'];

// ── Leitura ──────────────────────────────────────────────────────────────────
function lerCSV(arq, sep = ',') {
  const txt = fs.readFileSync(arq, 'utf8').replace(/^﻿/, '');
  const linhas = [];
  let campo = '', linha = [], aspas = false;
  for (let i = 0; i < txt.length; i++) {
    const c = txt[i];
    if (aspas) {
      if (c === '"') { if (txt[i + 1] === '"') { campo += '"'; i++; } else aspas = false; }
      else campo += c;
    } else if (c === '"') aspas = true;
    else if (c === sep) { linha.push(campo); campo = ''; }
    else if (c === '\n') { linha.push(campo); linhas.push(linha); linha = []; campo = ''; }
    else if (c !== '\r') campo += c;
  }
  if (campo !== '' || linha.length) { linha.push(campo); linhas.push(linha); }
  const cab = linhas.shift();
  const rs = linhas.filter(l => l.length > 1 || l[0] !== '')
    .map(l => Object.fromEntries(cab.map((h, j) => [h, l[j] === undefined ? '' : l[j]])));
  rs.colunas = cab;
  return rs;
}

function gravarCSV(arq, rs, cab) {
  const q = v => { const s = String(v === undefined || v === null ? '' : v);
                   return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  fs.writeFileSync(arq, [cab.join(','), ...rs.map(r => cab.map(c => q(r[c])).join(','))].join('\n') + '\n');
}

// ── Formatação pt-BR ─────────────────────────────────────────────────────────
function br(v, d) {
  const x = Number(v);
  if (v === '' || v === undefined || v === null || Number.isNaN(x)) return '—';
  return x.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
}
function formatar(v, fmt, linha) {
  if (fmt === 't') return v === '' ? '—' : String(v);
  if (fmt === 'faixa') return FAIXA[v] || v;
  if (fmt === 'bool') return v === 'True' ? 'sim' : 'não';
  if (fmt === 'i') return br(v, 0);
  if (fmt === 'v') return br(v, String(linha.indicador || '').startsWith('renda') ? 2 : 4);
  if (fmt === 'auto') return v === '' || Number.isNaN(Number(v)) ? (v === '' ? '—' : String(v)) : (Number.isInteger(Number(v)) ? br(v, 0) : br(v, 4));
  if (fmt[0] === 'p') return br(v, +fmt[1]) === '—' ? '—' : br(v, +fmt[1]) + '%';
  return br(v, +fmt[1]);
}
const preencher = (t, campos) => String(t || '').replace(/\{(\w+)\}/g, (m, k) => (k in campos ? campos[k] : m));

// ── Vistas das tabelas: que linhas e colunas vão ao slide ────────────────────
const C = (campo, rot, fmt, w) => ({ campo, rot, fmt, w });
const pontas = (rs, k) => (rs.length <= 2 * k ? rs : [...rs.slice(0, k), { _sep: true }, ...rs.slice(-k)]);
const ordenar = (rs, campo, desc) => [...rs].sort((a, b) => (desc ? -1 : 1) * (Number(a[campo]) - Number(b[campo])));
const maiores = (rs, cols, k) => cols.map(c => [c, Math.max(...rs.map(r => Number(r[c]) || 0))])
  .sort((a, b) => b[1] - a[1]).slice(0, k).map(x => x[0]);

function pivot(rs, lin, col, val, ordemCols, rot, fmt) {
  const cols = ordemCols.filter(c => rs.some(r => r[col] === c));
  const chaves = [...new Set(rs.map(r => r[lin]))];
  const linhas = chaves.map(k => {
    const o = { [lin]: k };
    rs.filter(r => r[lin] === k).forEach(r => { o[r[col]] = r[val]; o.indicador = r.indicador; });
    return o;
  });
  return { linhas, cols: [C(lin, rot, 't', 2.4), ...cols.map(c => C(c, FAIXA[c] || c, fmt, 1.1))] };
}

function vista(chave, rs, campos, ctx) {
  const R = c => ctx.rot[c] || c;
  switch (chave) {
    case 'funil_tab': return { cols: [C('etapa', 'Etapa', 't', 2.6), C('setores', 'Setores', 'i', 1.0),
      C('saem', 'Saem', 'i', 0.9), C('motivo_da_saida', 'Motivo da saída', 't', 3.6)] };
    case 'perdas': return { cols: [C('rotulo', 'Indicador', 't', 2.6), C('dimensao', 'Dimensão', 't', 1.5),
      C('n_validos', 'Com valor', 'i', 1.2), C('n_faltantes', 'Sem valor', 'i', 1.1), C('pct_faltantes', '% sem valor', 'p1', 1.1)] };
    case 'desc_global': return { cols: [C('rotulo', 'Indicador', 't', 2.1), C('n', 'n', 'i', 0.85),
      C('media', 'Média', 'v', 0.85), C('dp', 'DP', 'v', 0.85), C('p10', 'P10', 'v', 0.8), C('mediana', 'Mediana', 'v', 0.85),
      C('p90', 'P90', 'v', 0.85), C('assim', 'Assim.', 'd2', 0.65), C('pct_zeros', '% zeros', 'p1', 0.75)] };
    case 'desc_regiao': {
      const p = pivot(rs, 'rotulo', 'regiao', 'mediana', REGIOES, 'Indicador — mediana por região', 'v');
      return { ...p, parcial: true };
    }
    case 'desc_municipio': return { linhas: pontas(ordenar(rs.filter(r => r.rotulo === campos.ind), 'mediana', true), 10),
      parcial: true, cols: [C(rs.colunas[0], `${rs.colunas[0] === 'UF' ? 'UF' : 'Município'} — ${campos.ind}`, 't', 3.0), C('n', 'n', 'i', 0.9), C('p10', 'P10', 'v', 1.1),
        C('mediana', 'Mediana', 'v', 1.1), C('p90', 'P90', 'v', 1.1)] };
    case 'falt_municipio': {
      const cols = maiores(rs, rs.colunas.slice(1), 5);
      return { linhas: ordenar(rs, cols[0], true).slice(0, 16), parcial: true,
        cols: [C(rs.colunas[0], `${rs.colunas[0] === 'UF' ? 'UF' : 'Município'} (% sem valor)`, 't', 2.2), ...cols.map(c => C(c, R(c), 'p1', 1.15))] };
    }
    case 'sigilo_porte_tab': return { cols: [C('decil_moradores', 'Décimo', 'i', 0.8), C('moradores_min', 'Moradores (mín.)', 'i', 1.2),
      C('moradores_max', 'Moradores (máx.)', 'i', 1.2), C('pct_falt_renda', '% sem renda', 'p1', 1.2),
      C('pct_falt_analfab', '% sem analfabetismo', 'p1', 1.4), C('pct_fcu', '% em FCU', 'p1', 1.0)] };
    case 'extremos_criterio': return { cols: [C('rotulo', 'Indicador', 't', 1.9), C('criterio', 'Critério', 't', 2.6),
      C('limite_superior', 'Limite sup.', 'v', 1.0), C('n_extremos', 'Extremos', 'i', 0.85), C('pct_extremos', '% extremos', 'p1', 0.9),
      C('pct_zeros', '% zeros', 'p1', 0.8)] };
    case 'extremos_municipio': {
      const cols = maiores(rs, rs.colunas.filter(c => c !== 'NM_MUN' && c !== 'total'), 4);
      return { linhas: rs.slice(0, 16), parcial: true, cols: [C(rs.colunas[0], rs.colunas[0] === 'UF' ? 'UF' : 'Município', 't', 2.2), C('total', 'Total', 'i', 0.9),
        ...cols.map(c => C(c, R(c), 'i', 1.2))] };
    }
    case 'extremos_lista': return { linhas: rs.filter((r, i) => i === 0 || rs[i - 1].indicador !== r.indicador), parcial: true,
      cols: [C('rotulo', 'Indicador', 't', 2.0), C('NM_MUN', 'Município', 't', 1.8), C('CD_SETOR', 'Setor', 't', 1.7),
        C('valor', 'Valor', 'v', 1.0), C('mediana_global', 'Mediana global', 'v', 1.1)] };
    case 'renda_classes': return { cols: [C('classe', 'Classe', 't', 2.0), C('setores', 'Setores', 'i', 1.3), C('pct', '%', 'p2', 1.1)] };
    case 'spearman': case 'pearson': {
      const k = rs.colunas[0];
      const sel = ctx.componentes.map(c => (c === 'renda_inv' ? 'renda_media' : c)).filter(c => rs.colunas.includes(c));
      return { linhas: rs.filter(r => sel.includes(r[k])).map(r => ({ ...r, _rot: R(r[k]) })), parcial: true,
        cols: [C('_rot', 'Componentes do índice', 't', 1.7), ...sel.map(c => C(c, R(c), 'd2', 0.88))] };
    }
    case 'pares': return { cols: [C('rotulo_a', 'Indicador', 't', 2.6), C('rotulo_b', 'Indicador', 't', 2.6),
      C('spearman', 'Spearman', 'd4', 1.2), C('pearson', 'Pearson', 'd4', 1.2)] };
    case 'fcu_tab': return { cols: [C('rotulo', 'Indicador', 't', 2.2), C('mediana_fcu', 'Mediana FCU', 'v', 1.15),
      C('mediana_nao_fcu', 'Mediana fora', 'v', 1.15), C('diferenca', 'Diferença', 'v', 1.1), C('auc', 'AUC', 'd4', 0.9),
      C('n_fcu', 'Setores FCU', 'i', 1.0)] };
    case 'etaria': return { cols: rs.colunas.map((c, i) => (i === 0 ? C(c, 'Faixa etária', 't', 1.4) : C(c, c, 'p1', 1.05))) };
    case 'envelhecimento': return { cols: [C('escopo', 'Escopo', 't', 1.4), C('rotulo', 'Indicador', 't', 2.3), C('n', 'n', 'i', 0.9),
      C('p25', 'P25', 'v', 1.0), C('mediana', 'Mediana', 'v', 1.0), C('p75', 'P75', 'v', 1.0)] };
    case 'env_correl': {
      const env = rs.map(r => r.indicador);
      const linhas = rs.colunas.slice(1).map(c => Object.assign({ _rot: R(c) }, ...rs.map(r => ({ [r.indicador]: r[c] }))));
      return { linhas, cols: [C('_rot', 'Indicador (ρ de Spearman)', 't', 2.4), ...env.map(e => C(e, R(e), 'd4', 1.3))] };
    }
    case 'adequacao': return { cols: [C('medida', 'Medida', 't', 4.2), C('valor', 'Valor', 'auto', 1.8)] };
    case 'variaveis': return { cols: [C('rotulo', 'Componente', 't', 1.9), C('msa', 'MSA', 'd4', 0.9),
      C('comunalidade_obliqua', 'Comunal.', 'd4', 0.95), C('promax_padrao_f1', 'Padrão F1', 'd4', 0.95),
      C('promax_padrao_f2', 'Padrão F2', 'd4', 0.95), C('promax_estrutura_f1', 'Estrut. F1', 'd4', 0.95),
      C('promax_estrutura_f2', 'Estrut. F2', 'd4', 0.95)] };
    case 'autovalores': return { cols: [C('componente', 'Componente', 'i', 1.2), C('autovalor', 'Autovalor', 'd4', 1.2),
      C('horn', 'Horn', 'd4', 1.2), C('pct_variancia', '% variância', 'd1', 1.2), C('pct_acumulado', '% acumulada', 'd1', 1.2)] };
    case 'phi': { const k = rs.colunas[0];
      return { cols: [C(k, 'Fator', 't', 1.2), ...rs.colunas.slice(1).map(c => C(c, c, 'd4', 1.2))] }; }
    case 'pesos': return { cols: [C('rotulo', 'Componente', 't', 2.0), C('dimensao', 'Dimensão', 't', 2.2), C('carga', 'Carga', 'd4', 0.95),
      C('peso_dimensao', 'Peso da dimensão (%)', 'd1', 1.4), C('peso', 'Peso no índice (%)', 'd1', 1.3)] };
    case 'indice_desc': return { cols: [C('escopo', 'Escopo', 't', 1.6), C('n', 'n', 'i', 1.0), C('media', 'Média', 'd4', 0.9),
      C('dp', 'DP', 'd4', 0.9), C('p10', 'P10', 'd4', 0.9), C('mediana', 'Mediana', 'd4', 0.95), C('p90', 'P90', 'd4', 0.9)] };
    case 'faixas': return { linhas: rs.map(r => ({ ...r, regra: r.regra === 'ivs_bh' ? 'IVS-BH' : 'Quartis' })),
      cols: [C('regra', 'Regra', 't', 1.4), C('faixa', 'Faixa', 'faixa', 1.8), C('setores', 'Setores', 'i', 1.2), C('pct', '%', 'p1', 1.0)] };
    case 'auc_elegib': return { cols: [C('medida', 'Medida', 't', 3.5), C('valor', 'Valor', 'auto', 1.2), C('detalhe', 'Detalhe', 't', 2.6)] };
    case 'auc_municipio': return { linhas: rs.filter(r => r.entra_na_mediana === 'True'), parcial: true,
      cols: [C('NM_MUN', 'Município (entra na mediana)', 't', 2.8), C('auc', 'AUC', 'd4', 1.0), C('n1', 'Setores FCU', 'i', 1.2),
        C('n0', 'Setores fora', 'i', 1.2)] };
    case 'risco_municipio': return { linhas: pontas(rs, 10), parcial: true, cols: [C('NM_MUN', 'Município', 't', 2.2),
      C('pessoas_elevado', 'Pessoas elevado', 'i', 1.2), C('pessoas_muito_elevado', 'Pessoas muito elevado', 'i', 1.3),
      C('pessoas_60mais_muito_elevado', '60+ muito elevado', 'i', 1.2), C('pct_pessoas_elevado_ou_mais', '% elevado ou mais', 'p1', 1.2)] };
    case 'risco_total': return { cols: [C('faixa', 'Faixa', 'faixa', 1.6), C('setores', 'Setores', 'i', 1.0),
      C('pessoas', 'Pessoas', 'i', 1.2), C('pessoas_60mais', 'Pessoas 60+', 'i', 1.2), C('pct_pessoas', '% pessoas', 'p1', 1.0),
      C('pct_pessoas_60mais', '% pessoas 60+', 'p1', 1.1)] };
    case 'desigualdade_tab': return { linhas: pontas(rs, 10), parcial: true, cols: [C('NM_MUN', 'Município', 't', 2.2),
      C('setores', 'Setores', 'i', 0.85), C('p10', 'P10', 'd4', 0.85), C('p90', 'P90', 'd4', 0.85), C('p90_p10', 'P90/P10', 'd2', 0.9),
      C('gini', 'Gini', 'd4', 0.85), C('theil', 'Theil', 'd4', 0.85)] };
    case 'comp_spearman': return { linhas: [rs[0], ...ordenar(rs.slice(1), 'spearman', false).slice(0, 15)], parcial: true,
      cols: [C('escopo', 'Escopo (menores ρ)', 't', 2.8), C('setores_comuns', 'Setores comuns', 'i', 1.4), C('spearman', 'ρ de Spearman', 'd4', 1.4)] };
    case 'comp_matriz_tab': {
      const ordem = Object.keys(FAIXA);
      const p = pivot(rs, 'faixa_referencia', 'faixa_versao', 'setores', ordem, 'Referência ↓ · versão →', 'i');
      p.linhas = ordem.filter(f => p.linhas.some(l => l.faixa_referencia === f))
        .map(f => p.linhas.find(l => l.faixa_referencia === f)).map(l => ({ ...l, faixa_referencia: FAIXA[l.faixa_referencia] }));
      return p;
    }
    case 'comp_municipios_tab': return { linhas: rs.slice(0, 16), parcial: true, cols: [C('NM_MUN', 'Município', 't', 2.8),
      C('setores_comuns', 'Setores comuns', 'i', 1.3), C('mudam_faixa', 'Mudam de faixa', 'i', 1.3), C('pct_mudam', '% que muda', 'p1', 1.1)] };
    case 'brasil_x_70': return { cols: [C('rotulo', 'Indicador', 't', 2.2), C('n_versao', 'n (versão)', 'i', 1.0),
      C('media_versao', 'Média (versão)', 'v', 1.05), C('mediana_versao', 'Mediana (versão)', 'v', 1.05), C('n_70', 'n (70 mun.)', 'i', 0.95),
      C('media_70', 'Média (70 mun.)', 'v', 1.05), C('mediana_70', 'Mediana (70 mun.)', 'v', 1.05)] };
    case 'faixas_alt_tab': return { cols: [C('regra', 'Regra', 't', 3.2), C('classe', 'Classe', 't', 0.9), C('setores', 'Setores', 'i', 1.2), C('pct', '%', 'p1', 1.0)] };
    case 'faixas_concordancia': return { cols: [C('regra', 'Regra', 't', 3.2), C('classes', 'Classes', 'i', 0.9),
      C('spearman_com_ivs_bh', 'ρ com IVS-BH', 'd4', 1.3), C('pct_mesma_classe', '% mesma classe', 'p1', 1.3)] };
    case 'silhueta': return { cols: [C('k', 'k', 'i', 1.0), C('silhueta', 'Silhueta', 'd4', 1.4)] };
    case 'sint_tabela': return { cols: [C('versao', 'Versão', 't', 2.5), C('setores_indice', 'Índice (n)', 'i', 0.9),
      C('kmo', 'KMO', 'd4', 0.7), C('auc_municipal', 'AUC mun.', 'd4', 0.8), C('elegivel', 'Elegível', 'auto', 0.7),
      C('spearman_com_referencia', 'ρ com a ref.', 'd4', 0.9), C('pct_mudam_faixa', '% muda faixa', 'p1', 0.9)] };
    case 'sint_eixos': return { cols: [C('eixo', 'Eixo', 't', 2.8), C('versoes', 'Versões', 'i', 0.8), C('elegiveis', 'Elegíveis', 'i', 0.85),
      C('auc_municipal_min', 'AUC mun. mín.', 'd4', 1.0), C('auc_municipal_max', 'AUC mun. máx.', 'd4', 1.0),
      C('pct_mudam_max', '% muda faixa (máx.)', 'p1', 1.1)] };
    case 'sensibilidade': return { cols: [C('rotulo', 'Valor', 't', 1.9), C('setores_recorte', 'Recorte', 'i', 0.9),
      C('setores_indice', 'Índice', 'i', 0.9), C('kmo', 'KMO', 'd4', 0.75), C('auc_global', 'AUC global', 'd4', 0.85),
      C('auc_municipal', 'AUC mun.', 'd4', 0.8), C('elegivel', 'Elegível', 'auto', 0.75), C('spearman_com_padrao', 'ρ com o padrão', 'd4', 0.9),
      C('pct_mudam_faixa', '% muda faixa', 'p1', 0.9)] };
    default: return { cols: rs.colunas.map(c => C(c, R(c) !== c ? R(c) : c.replace(/^pct_/, '% ').replace(/_/g, ' '),
      /^(pct|p\d)/.test(c) && !/^p(10|90|2_5|97_5)$/.test(c) ? 'p1' : 'auto', c === 'NM_MUN' || c === 'versao' || c === 'escopo' ? 2.4 : 1.1)) };
  }
}

// ── O deck ────────────────────────────────────────────────────────────────────
function main() {
  if (!process.argv[2]) { console.error('uso: gerar_deck_versao.js analises_exploratorias/<versao>'); process.exit(1); }
  const pasta = path.resolve(process.argv[2]);
  const nome = path.basename(pasta);
  const cfg = JSON.parse(fs.readFileSync(path.join(pasta, 'config.json'), 'utf8'));
  const cfgRef = JSON.parse(fs.readFileSync(path.join(REFERENCIA, 'config.json'), 'utf8'));
  const tx = JSON.parse(fs.readFileSync(path.join(pasta, 'textos.json'), 'utf8'));
  const mod = JSON.parse(fs.readFileSync(MODELOS, 'utf8'));
  const cat = lerCSV(path.join(pasta, 'catalogo.csv'));
  const cabCat = cat.colunas;
  const porId = Object.fromEntries(cat.map(r => [r.id, r]));
  const tab = id => { const f = fs.readdirSync(path.join(pasta, 'tabelas')).find(a => a.startsWith(id + '_'));
                      return f ? lerCSV(path.join(pasta, 'tabelas', f)) : null; };
  const campos = id => (porId[id] ? JSON.parse(porId[id].campos) : {});
  const rot = {};
  (tab('T02') || []).forEach(r => { rot[r.indicador] = r.rotulo; });
  (tab('T20') || []).forEach(r => { rot[r.variavel] = r.rotulo; });
  const ctx = { rot, componentes: (cfg.indice && cfg.indice.colunas) || [] };

  const d = criarDeck({ titulo: `${nome} — ${cfg.titulo}` });
  const { W, H, M } = d.geo;
  const K = d.cores;
  const XR = M + 8.15 + 0.35, WR = W - M - XR, WE = 8.15, Y_FIM = H - 0.85;
  let nS = 0;
  const novo = () => { nS++; return d.S(); };

  function tituloItem(s, t) {
    const larg = W - 2 * M;
    const cabe = f => Math.floor((larg - 0.2) * 72 / (f * 0.5));   // a mesma conta do verificador (margem interna e meio corpo)
    let f = t.length <= cabe(24) ? 24 : (t.length <= cabe(20) ? 20 : 0), y = 0.42, h = 0.62;
    if (!f) { f = Math.max(15, Math.min(20, Math.floor(2 * larg * 72 / (0.5 * t.length)))); y = 0.2; h = 0.86; }
    s.addText(t, { x: M, y, w: larg, h, fontFace: K.FONTE, fontSize: f, color: K.TINTA, bold: true, margin: 0, valign: 'bottom' });
    d.regua(s, 1.14, 1.0, K.TINTA);
    return 1.36;
  }

  // altura com folga: a estimativa usa meio corpo por caractere, como o verificador
  const altLateral = t => d.alturaTexto(t, WR, 12.5 * 0.5 / 0.45, 16.5) + 0.25;
  function lateral(s, y, comoLer, mostra) {
    const h1 = altLateral('Como ler   ' + comoLer);
    d.bloco(s, XR, y, WR, 'Como ler', comoLer, false, h1);
    const y2 = y + h1 + 0.3;
    d.bloco(s, XR, y2, WR, 'O que mostra', mostra, true, altLateral('O que mostra   ' + mostra));
  }

  // tabela booktabs paginada pela altura estimada de cada linha, com páginas equilibradas:
  // conta quantas páginas a tabela pede e procura a menor altura que ainda cabe nelas,
  // para a última página não ficar com uma linha só
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
  function larguras(cols, total) {
    const soma = cols.reduce((a, c) => a + c.w, 0);
    return cols.map(c => c.w * Math.min(1, total / soma));
  }
  const celulas = (cols, linhas) => linhas.map(r => (r._sep ? cols.map(() => '…') : cols.map(c => formatar(r[c.campo], c.fmt, r))));

  function rodape(s, txt) { d.procedencia(s, txt); }

  // 1. Capa
  const t01 = tab('T01') || [];
  const nRecorte = t01.length ? (t01.find(r => r.etapa === 'Componentes do índice completos') ? t01[t01.length - 2] : t01[t01.length - 1]).setores : '';
  const nIndice = t01.length ? t01[t01.length - 1].setores : '';
  const hoje = new Date();
  let s = novo();
  d.capa(s, `ANÁLISES EXPLORATÓRIAS POR VERSÃO · ${cfg.versao || nome}`, cfg.titulo, tx.pergunta || cfg.pergunta,
    `${MESES[hoje.getMonth()]} de ${hoje.getFullYear()}` + (t01.length ? `  ·  ${br(nRecorte, 0)} setores no recorte  ·  ${br(nIndice, 0)} na amostra do índice` : ''));
  s.addNotes(tx.pergunta || cfg.pergunta || '');

  // 2. O que muda nesta versão
  const descrRecorte = c => { const r = Object.assign({ urbano: true, dados_sig: 'OK' }, c.recorte || {});
    return [r.urbano ? 'setores urbanos' : 'setores urbanos e rurais', r.dados_sig ? `Dados_sig = ${r.dados_sig}` : 'todos os Dados_sig',
      r.piso_pop ? `pelo menos ${r.piso_pop} moradores` : '', r.municipios ? `municípios: ${r.municipios.join(', ')}` : ''].filter(Boolean).join('; '); };
  const ind = c => c.indice || {};
  const aspectos = [
    ['Base', c => c.base || ''], ['Recorte', descrRecorte],
    ['Indicadores', c => (c.indicadores === 'todos' || !c.indicadores ? 'todos os do quadro, com as variantes' : c.indicadores.map(i => rot[i] || i).join(', '))],
    ['Componentes do índice', c => (ind(c).colunas || []).map(i => rot[i] || i).join(', ') || 'sem índice'],
    ['Renda', c => ind(c).renda || '—'], ['Rotação', c => ind(c).rotacao || '—'], ['Pesos das dimensões', c => ind(c).metodo || '—'],
    ['Normalização', c => ind(c).normalizacao || '—'], ['Blocos', c => (c.blocos || []).join(', ')]];
  s = novo();
  let y = tituloItem(s, 'O que muda nesta versão');
  const linhasMuda = aspectos.map(([a, f]) => { const r = f(cfgRef), v = f(cfg);
    return [a, r, v === r ? { text: 'igual', options: { color: K.CINZA_C, italic: true } } : { text: v, options: { color: K.ACENTO, bold: true } }]; });
  y = d.tabelaAjustada(s, ['Aspecto', 'Referência (00_referencia)', 'Esta versão'], linhasMuda, { y, colW: [2.2, 4.7, 4.7], fontSize: 10.5 });
  d.bloco(s, M, y + 0.25, W - 2 * M, 'O que muda', tx.o_que_muda || '', true, Y_FIM - y - 0.3);
  s.addNotes(tx.o_que_muda || '');

  // 3. Recorte e n (só nas versões que têm o funil)
  if (t01.length) {
  s = novo();
  y = tituloItem(s, `${br(nIndice, 0)} setores chegam ao índice`);
  if (t01.length) {
    const w3 = (W - 2 * M - 0.8) / 3;
    d.numero(s, M, y + 0.3, w3, br(t01[0].setores, 0), 'setores na base completa');
    d.numero(s, M + w3 + 0.4, y + 0.3, w3, br(nRecorte, 0), 'setores no recorte da versão (descritivas, distribuições, correlações)');
    d.numero(s, M + 2 * (w3 + 0.4), y + 0.3, w3, br(nIndice, 0), 'setores na amostra do índice (fatorial e blocos 9 a 13)', true);
  }
  d.bloco(s, M, y + 1.95, W - 2 * M, 'Por que dois números', preencher(mod.itens.funil_tab.nota, campos('T01')), false, 2.4);
  rodape(s, 'T01 · tabelas/T01_funil.csv');
  s.addNotes(preencher(mod.itens.funil_tab.nota, campos('T01')));
  }

  // 4. Sumário
  const blocos = (cfg.blocos || []).filter(b => cat.some(r => +r.bloco === b));
  s = novo();
  y = tituloItem(s, 'Sumário: os blocos desta versão');
  const linhasSum = blocos.map(b => [String(b), mod.blocos[b].titulo, mod.blocos[b].pergunta,
    cat.filter(r => +r.bloco === b).map(r => r.id).join(', ')]);
  d.tabelaAjustada(s, ['Bloco', 'Título', 'Pergunta', 'Itens'], linhasSum, { y, colW: [0.7, 2.6, 5.4, 2.9], fontSize: 10 });

  // 5. Blocos e itens
  for (const b of blocos) {
    const mb = mod.blocos[b];
    s = novo();
    d.secao(s, String(b), mb.titulo, mb.pergunta);
    s.addText('Neste bloco: ' + cat.filter(r => +r.bloco === b).map(r => r.id).join(' · '),
      { x: M + 1.25, y: 4.75, w: W - 2 * M - 1.25, h: 0.4, fontFace: K.FONTE, fontSize: 12, color: K.CINZA, margin: 0 });
    s.addNotes(mb.nota);
    for (const it of cat.filter(r => +r.bloco === b)) {
      const m = mod.itens[it.chave] || {};
      const cp = JSON.parse(it.campos);
      const notas = [preencher(m.nota, cp), '', 'Como ler: ' + preencher(m.como_ler, cp), 'O que mostra: ' + it.o_que_mostra].join('\n');
      const pe = `${it.id} · ${it.arquivo}  ·  Bloco ${b}. ${mb.titulo}`;
      if (it.tipo === 'figura') {
        s = novo();
        it.slide = String(nS);
        y = tituloItem(s, it.titulo);
        const arq = path.join(pasta, it.arquivo);
        const b0 = fs.readFileSync(arq);
        const pw = b0.readUInt32BE(16), ph = b0.readUInt32BE(20);
        const esc = Math.min(WE / pw, (Y_FIM - y - 0.05) / ph);
        s.addImage({ path: arq, x: M + (WE - pw * esc) / 2, y, w: pw * esc, h: ph * esc });
        lateral(s, y + 0.05, preencher(m.como_ler, cp), it.o_que_mostra);
        rodape(s, pe);
        s.addNotes(notas);
        continue;
      }
      const rs = tab(it.id);
      const v = vista(it.chave, rs, cp, ctx);
      const linhas = v.linhas || rs;
      const colW = larguras(v.cols, WE);
      const fsz = 10;
      const cab = v.cols.map(c => c.rot);
      const corpo = celulas(v.cols, linhas);
      const hDisp = Y_FIM - 1.36 - (v.parcial ? 0.35 : 0.05);
      const pags = corpo.length ? paginas(cab, corpo, colW, fsz, hDisp) : [];
      if (!pags.length) {
        s = novo();
        it.slide = String(nS);
        y = tituloItem(s, it.titulo);
        d.bloco(s, M, y + 0.2, WE, 'Tabela vazia', 'Nenhuma linha atende ao critério desta tabela nesta versão.', false, 0.8);
        lateral(s, y + 0.05, preencher(m.como_ler, cp), it.o_que_mostra);
        rodape(s, pe);
        s.addNotes(notas);
        continue;
      }
      pags.forEach((pg, k) => {
        s = novo();
        if (k === 0) it.slide = String(nS);
        y = tituloItem(s, it.titulo);
        const yFim = d.tabelaAjustada(s, cab, pg, { y, colW, fontSize: fsz, rowH: 0.24 });
        if (v.parcial && k === pags.length - 1) {
          s.addText('Recorte da tabela para o slide; a tabela completa está no CSV indicado no rodapé.',
            { x: M, y: yFim + 0.08, w: WE, h: 0.26, fontFace: K.FONTE, fontSize: 9.5, color: K.CINZA_C, italic: true, margin: 0 });
        }
        lateral(s, y + 0.05, preencher(m.como_ler, cp), it.o_que_mostra);
        rodape(s, pe + (pags.length > 1 ? `  ·  parte ${k + 1} de ${pags.length}` : ''));
        s.addNotes(notas);
      });
    }
  }

  // 6. Síntese
  s = novo();
  y = tituloItem(s, 'Síntese da versão');
  const destaques = [['T01', 'n_indice', 'setores na amostra do índice'], ['T19', 'kmo', 'KMO dos componentes'],
    ['T26', 'auc_mun', 'AUC municipal contra FCU (mediana)'], ['T33', 'pct_global', 'setores que mudam de faixa em relação à referência']]
    .filter(([id, k]) => campos(id)[k] !== undefined);
  const w4 = (W - 2 * M - 0.4 * (destaques.length - 1)) / Math.max(destaques.length, 1);
  destaques.forEach(([id, k, r], i) => d.numero(s, M + i * (w4 + 0.4), y + 0.25, w4, campos(id)[k], `${r} (${id})`, i === destaques.length - 1));
  d.bloco(s, M, y + 1.9, W - 2 * M, 'O que esta versão mostra', tx.sintese || '', true, Y_FIM - y - 1.95);
  s.addNotes(tx.sintese || '');

  // 7. Candidatos ao artigo
  const linhasCand = cat.map(r => [r.id, r.bloco, r.titulo]);
  const colCand = [0.8, 0.8, 10.0];
  const cabCand = ['ID', 'Bloco', 'Título no deck'];
  const pagsCand = paginas(cabCand, linhasCand, colCand, 9.5, Y_FIM - 1.36 - 0.45);
  pagsCand.forEach((pg, k) => {
    s = novo();
    y = tituloItem(s, 'Candidatos ao artigo: as tabelas e figuras desta versão');
    s.addText('Marcar no catálogo (colunas “Vai para o artigo?”, “Seção” e “Comentários”); os IDs são os mesmos em todas as versões.',
      { x: M, y, w: W - 2 * M, h: 0.3, fontFace: K.FONTE, fontSize: 11, color: K.CINZA, italic: true, margin: 0 });
    d.tabelaAjustada(s, cabCand, pg, { y: y + 0.4, colW: colCand, fontSize: 9.5, rowH: 0.22 });
    rodape(s, `catalogo.csv${pagsCand.length > 1 ? `  ·  parte ${k + 1} de ${pagsCand.length}` : ''}`);
  });

  // 8. Limitações e parâmetros exploratórios
  s = novo();
  y = tituloItem(s, 'Limitações e parâmetros exploratórios');
  const par = Object.entries(cfg.parametros_exploratorios || {});
  const itens = [...(tx.limitacoes || []).map(t => ({ text: t, options: { bullet: true, breakLine: true } })),
    ...(par.length ? par.map(([k, v]) => ({ text: `${k}: ${v} — parâmetro exploratório — não é decisão`,
      options: { bullet: true, breakLine: true, color: K.ACENTO } }))
      : [{ text: 'Nenhum parâmetro exploratório nesta versão.', options: { bullet: true, breakLine: true, italic: true } }])];
  s.addText(itens, { x: M, y: y + 0.1, w: W - 2 * M, h: Y_FIM - y - 0.15, fontFace: K.FONTE, fontSize: 13, color: K.TINTA,
    margin: 0, valign: 'top', paraSpaceAfter: 8 });
  s.addNotes((tx.limitacoes || []).join('\n'));

  // 9. Apêndice: dicionário dos indicadores
  const quadro = Object.fromEntries(lerCSV(QUADRO, ';').map(r => [r.indicador, r]));
  const extra = Object.assign({}, mod.dicionario_extra || {},
    Object.fromEntries([...(cfg.indicadores_externos || []), ...(cfg.indicadores_derivados || [])].map(e => [e.nome, e])));
  const codigos = t => (String(t || '').match(/\b[Vv]\d{4,5}\b/g) || []).join(' + ') || '—';
  const linhasDic = (tab('T02') || []).map(r => { const q = quadro[r.indicador] || extra[r.indicador] || {};
    return [r.rotulo, r.dimensao, q.o_que_mede || '—', q.numerador_curto || codigos(q.numerador), q.denominador_curto || codigos(q.denominador)]; });
  const colDic = [2.0, 1.3, 4.6, 1.9, 1.8];
  const cabDic = ['Indicador', 'Dimensão', 'O que mede', 'Numerador', 'Denominador'];
  const pagsDic = paginas(cabDic, linhasDic, colDic, 9.5, Y_FIM - 1.36 - 0.05);
  pagsDic.forEach((pg, k) => {
    s = novo();
    y = tituloItem(s, 'Apêndice: dicionário dos indicadores');
    d.tabelaAjustada(s, cabDic, pg, { y, colW: colDic, fontSize: 9.5, rowH: 0.22 });
    rodape(s, `Quadro_Indicadores.csv (entrega à orientadora)${pagsDic.length > 1 ? `  ·  parte ${k + 1} de ${pagsDic.length}` : ''}`);
  });

  const saida = path.join(pasta, `${nome}.pptx`);
  d.p.writeFile({ fileName: saida }).then(() => {
    gravarCSV(path.join(pasta, 'catalogo.csv'), cat, cabCat);
    console.log(`${path.relative(RAIZ, saida)}: ${nS} slides; ${cat.filter(r => r.slide).length} de ${cat.length} itens com slide no catálogo`);
  });
}

main();
