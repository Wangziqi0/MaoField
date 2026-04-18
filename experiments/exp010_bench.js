#!/usr/bin/env node
'use strict';
/**
 * MaoField Exp010: Query Evolution Benchmark
 *
 * Loads evolved query token clouds and runs PQ-Chamfer via Rust engine.
 * Compares with baseline (original query tokens).
 *
 * Usage: RAYON_NUM_THREADS=70 node exp010_bench.js <variant_name>
 * Example: node exp010_bench.js evolve-16-50
 *
 * If no variant given, runs all found evolved_query_*.sqlite files.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const TOP_N = 55;
const K = 10;
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

async function runBenchmark(variantName, queryDbPath) {
  console.log(`\n--- ${variantName} ---`);

  const { LawVexus } = require('/home/amd/HEZIMENG/law-vexus');
  const v = new LawVexus(`/tmp/maofield_exp010_${variantName}`);

  // Load doc clouds (same for all variants)
  v.loadClouds(path.join(DATA_DIR, 'clouds.sqlite'));

  // Load token clouds with evolved query
  v.loadTokenCloudsSqlite(
    path.join(DATA_DIR, 'token_clouds.sqlite'),
    queryDbPath
  );

  // Load eval data
  const qrels = {};
  const ql = fs.readFileSync(path.join(DATA_DIR, 'qrels.tsv'), 'utf-8').trim().split('\n');
  for (let i = 1; i < ql.length; i++) {
    const p = ql[i].split('\t');
    if (!qrels[p[0]]) qrels[p[0]] = {};
    qrels[p[0]][p[1]] = parseInt(p[2]);
  }

  const idMap = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'id_map.json'), 'utf-8'));
  const rev = {};
  for (const [s, i] of Object.entries(idMap)) rev[i] = s;

  const queryVecs = {};
  for (const o of await loadJsonl(path.join(DATA_DIR, 'query_vectors.jsonl')))
    queryVecs[o._id] = new Float32Array(o.vector);

  const queriesRaw = await loadJsonl(path.join(DATA_DIR, 'queries.jsonl'));
  const queryIdToFileId = {};
  for (let i = 0; i < queriesRaw.length; i++) queryIdToFileId[queriesRaw[i]._id] = i;

  let qids = Object.keys(qrels).filter(q => queryVecs[q]);

  const t0 = Date.now();
  let ndcgSum = 0, n = 0;

  for (let qi = 0; qi < qids.length; qi++) {
    const qid = qids[qi];
    const qrel = qrels[qid];
    const qFileId = queryIdToFileId[qid];

    try {
      const h = v.tokenChamferTwoStage(qFileId, 100, TOP_N);
      const ranked = h.map(x => rev[x[0]]).filter(Boolean);
      ndcgSum += computeNDCG(ranked, qrel, K);
      n++;
    } catch (e) {
      if (qi === 0) console.error(`  ERROR: ${e.message}`);
    }
  }

  const elapsed = (Date.now() - t0) / 1000;
  const avg = n > 0 ? ndcgSum / n : 0;
  console.log(`  NDCG@10 = ${avg.toFixed(4)} (${n}q, ${elapsed.toFixed(1)}s)`);

  return { ndcg_at_10: +avg.toFixed(4), n_queries: n, time_s: +elapsed.toFixed(1) };
}

async function main() {
  console.log('=== MaoField Exp010: Query Evolution Benchmark ===\n');

  const specificVariant = process.argv[2];

  // Find all evolved query sqlite files
  let variants = [];
  if (specificVariant) {
    variants.push({
      name: specificVariant,
      db: path.join(EXP_DIR, `evolved_query_${specificVariant}.sqlite`)
    });
  } else {
    const files = fs.readdirSync(EXP_DIR).filter(f => f.startsWith('evolved_query_') && f.endsWith('.sqlite'));
    for (const f of files.sort()) {
      const name = f.replace('evolved_query_', '').replace('.sqlite', '');
      variants.push({ name, db: path.join(EXP_DIR, f) });
    }
  }

  // Always run baseline first
  console.log('Running baseline (original query tokens)...');
  const baselineResult = await runBenchmark('baseline',
    path.join(DATA_DIR, 'query_token_clouds.sqlite'));

  const results = { baseline: baselineResult };

  for (const variant of variants) {
    if (!fs.existsSync(variant.db)) {
      console.log(`  SKIP: ${variant.db} not found`);
      continue;
    }
    results[variant.name] = await runBenchmark(variant.name, variant.db);
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('  MaoField Exp010 — Query Evolution Results');
  console.log('-'.repeat(60));
  const baseline = results.baseline.ndcg_at_10;
  const sorted = Object.entries(results).sort((a, b) => b[1].ndcg_at_10 - a[1].ndcg_at_10);
  for (const [name, res] of sorted) {
    const delta = name === 'baseline'
      ? '(baseline)'
      : `${((res.ndcg_at_10 - baseline) / baseline * 100).toFixed(2)}%`;
    console.log(`  ${name.padEnd(24)} ${res.ndcg_at_10.toFixed(4).padEnd(10)} ${delta}`);
  }
  console.log('='.repeat(60));

  const outPath = path.join(EXP_DIR, 'exp010_results.json');
  fs.writeFileSync(outPath, JSON.stringify({
    meta: { dataset: 'nfcorpus', top_n: TOP_N, date: '2026-04-09' },
    results
  }, null, 2));
  console.log(`\nSaved: ${outPath}`);
}

main().catch(e => { console.error(e); process.exit(1) });
