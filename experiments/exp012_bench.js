#!/usr/bin/env node
'use strict';
/**
 * MaoField Exp012: Dialectical Query Expansion Benchmark
 * Runs all expanded_query_*.sqlite variants + baseline via Rust PQ-Chamfer.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const TOP_N = 55, K = 10;
const DATA_DIR = '/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus';
const EXP_DIR = '/home/amd/HEZIMENG/MaoField/experiments';

function loadJsonl(fp) {
  return new Promise((res, rej) => {
    const a = [];
    const r = readline.createInterface({ input: fs.createReadStream(fp), crlfDelay: Infinity });
    r.on('line', l => { if (l.trim()) try { a.push(JSON.parse(l)) } catch (_) {} });
    r.on('close', () => res(a));
    r.on('error', rej);
  });
}

function computeNDCG(ranked, qrel, k = 10) {
  let dcg = 0;
  for (let i = 0; i < Math.min(ranked.length, k); i++) {
    const r = qrel[ranked[i]] || 0;
    dcg += (Math.pow(2, r) - 1) / Math.log2(i + 2);
  }
  const ir = Object.values(qrel).sort((a, b) => b - a);
  let idcg = 0;
  for (let i = 0; i < Math.min(ir.length, k); i++) {
    idcg += (Math.pow(2, ir[i]) - 1) / Math.log2(i + 2);
  }
  return idcg > 0 ? dcg / idcg : 0;
}

async function runOne(name, queryDb) {
  const { LawVexus } = require('/home/amd/HEZIMENG/law-vexus');
  const v = new LawVexus(`/tmp/exp012_${name}`);
  v.loadClouds(path.join(DATA_DIR, 'clouds.sqlite'));
  v.loadTokenCloudsSqlite(path.join(DATA_DIR, 'token_clouds.sqlite'), queryDb);

  const qrels = {};
  const ql = fs.readFileSync(path.join(DATA_DIR, 'qrels.tsv'), 'utf-8').trim().split('\n');
  for (let i = 1; i < ql.length; i++) {
    const p = ql[i].split('\t');
    if (!qrels[p[0]]) qrels[p[0]] = {};
    qrels[p[0]][p[1]] = parseInt(p[2]);
  }
  const idMap = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'id_map.json'), 'utf-8'));
  const rev = {}; for (const [s, i] of Object.entries(idMap)) rev[i] = s;
  const queryVecs = {};
  for (const o of await loadJsonl(path.join(DATA_DIR, 'query_vectors.jsonl')))
    queryVecs[o._id] = true;
  const queriesRaw = await loadJsonl(path.join(DATA_DIR, 'queries.jsonl'));
  const qid2fid = {}; for (let i = 0; i < queriesRaw.length; i++) qid2fid[queriesRaw[i]._id] = i;
  const qids = Object.keys(qrels).filter(q => queryVecs[q]);

  const t0 = Date.now();
  let sum = 0, n = 0;
  for (const qid of qids) {
    try {
      const h = v.tokenChamferTwoStage(qid2fid[qid], 100, TOP_N);
      sum += computeNDCG(h.map(x => rev[x[0]]).filter(Boolean), qrels[qid], K);
      n++;
    } catch (_) {}
  }
  const avg = n > 0 ? sum / n : 0;
  return { ndcg_at_10: +avg.toFixed(4), n_queries: n, time_s: +((Date.now()-t0)/1000).toFixed(1) };
}

async function main() {
  console.log('=== MaoField Exp012: Query Expansion Benchmark ===\n');

  process.stdout.write('baseline... ');
  const bl = await runOne('baseline', path.join(DATA_DIR, 'query_token_clouds.sqlite'));
  console.log(`NDCG@10 = ${bl.ndcg_at_10.toFixed(4)}`);

  const results = { baseline: bl };

  const files = fs.readdirSync(EXP_DIR)
    .filter(f => f.startsWith('expanded_query_') && f.endsWith('.sqlite'))
    .sort();

  for (const f of files) {
    const name = f.replace('expanded_query_', '').replace('.sqlite', '');
    process.stdout.write(`${name}... `);
    const res = await runOne(name, path.join(EXP_DIR, f));
    console.log(`NDCG@10 = ${res.ndcg_at_10.toFixed(4)}`);
    results[name] = res;
  }

  console.log('\n' + '='.repeat(55));
  console.log('  Exp012 — Dialectical Query Expansion');
  console.log('-'.repeat(55));
  const base = results.baseline.ndcg_at_10;
  for (const [n, r] of Object.entries(results).sort((a, b) => b[1].ndcg_at_10 - a[1].ndcg_at_10)) {
    const d = n === 'baseline' ? '(baseline)' : `${((r.ndcg_at_10 - base) / base * 100).toFixed(2)}%`;
    console.log(`  ${n.padEnd(24)} ${r.ndcg_at_10.toFixed(4).padEnd(10)} ${d}`);
  }
  console.log('='.repeat(55));

  fs.writeFileSync(path.join(EXP_DIR, 'exp012_results.json'),
    JSON.stringify({ meta: { dataset: 'nfcorpus', date: '2026-04-09' }, results }, null, 2));
  console.log('\nSaved: exp012_results.json');
}

main().catch(e => { console.error(e); process.exit(1) });
