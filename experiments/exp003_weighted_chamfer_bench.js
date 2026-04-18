#!/usr/bin/env node
'use strict';
/**
 * MaoField Exp003: Weighted PQ-Chamfer Benchmark
 *
 * 在 Rust 引擎的真实 PQ-Chamfer 上测试 4 种子空间权重方案：
 * 1. uniform:          均匀权重（现有 baseline）
 * 2. variance:         按子空间方差加权（显式优先）
 * 3. inverse_variance: 按方差反向加权（隐含优先）
 * 4. disagreement:     按 query-doc 活跃度分歧加权（矛盾信号）
 *
 * 用法: RAYON_NUM_THREADS=70 node exp003_weighted_chamfer_bench.js [top_n]
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const TOP_N = parseInt(process.argv[2] || '55');
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

// Normalize array to [0,1]
function normalize01(arr) {
  const mn = Math.min(...arr), mx = Math.max(...arr), rng = mx - mn || 1e-10;
  return arr.map(v => (v - mn) / rng);
}

async function main() {
  console.log('\n=== MaoField Exp003: Weighted PQ-Chamfer Benchmark ===');
  console.log(`Dataset: NFCorpus, top_n=${TOP_N}\n`);

  // Load exp001 results for subspace weights
  const exp001 = JSON.parse(fs.readFileSync(path.join(EXP_DIR, 'exp001_results.json'), 'utf-8'));
  const docVar = exp001.global_subspace_activity.doc_mean_variance;
  const queryVar = exp001.global_subspace_activity.query_mean_variance;

  // Build weight schemes (64-element arrays)
  const schemes = {};

  // 1. Uniform
  schemes.uniform = new Array(64).fill(1.0);

  // 2. Variance-weighted (explicit priority)
  schemes.variance = docVar.slice();

  // 3. Inverse-variance (implicit priority)
  schemes.inverse_variance = docVar.map(v => 1.0 / (v + 1e-6));

  // 4. Disagreement (contradiction signal)
  const docNorm = normalize01(docVar);
  const queryNorm = normalize01(queryVar);
  schemes.disagreement = docNorm.map((d, i) => Math.abs(d - queryNorm[i]) + 0.1);

  // 5. Per-pair dynamic disagreement (computed per query-doc pair)
  // This requires a different approach - will do after static schemes

  console.log('Weight schemes:');
  for (const [name, w] of Object.entries(schemes)) {
    const s = w.reduce((a, b) => a + b, 0);
    const mx = Math.max(...w), mn = Math.min(...w);
    console.log(`  ${name.padEnd(20)} sum=${s.toFixed(2)} min=${mn.toFixed(4)} max=${mx.toFixed(4)} ratio=${(mx/mn).toFixed(1)}x`);
  }

  // Load Rust engine
  const { LawVexus } = require('/home/amd/HEZIMENG/law-vexus');
  const v = new LawVexus('/tmp/maofield_exp003');

  process.stdout.write('\nLoading sentence clouds... ');
  const ci = v.loadClouds(path.join(DATA_DIR, 'clouds.sqlite'));
  console.log(`done (${ci})`);

  process.stdout.write('Loading token clouds... ');
  const ti = v.loadTokenCloudsSqlite(
    path.join(DATA_DIR, 'token_clouds.sqlite'),
    path.join(DATA_DIR, 'query_token_clouds.sqlite')
  );
  console.log(`done (${ti})`);

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
  console.log(`\n${qids.length} queries\n`);

  // Run all schemes
  const results = {};

  for (const [schemeName, weights] of Object.entries(schemes)) {
    console.log(`--- ${schemeName} ---`);
    const t0 = Date.now();
    let ndcgSum = 0, n = 0;

    for (let qi = 0; qi < qids.length; qi++) {
      const qid = qids[qi];
      const qrel = qrels[qid];
      const qFileId = queryIdToFileId[qid];

      try {
        let h;
        if (schemeName === 'uniform') {
          // Use the standard (faster) path for uniform
          h = v.tokenChamferTwoStage(qFileId, 100, TOP_N);
        } else {
          h = v.tokenChamferTwoStageWeighted(qFileId, 100, TOP_N, weights);
        }
        const ranked = h.map(x => rev[x[0]]).filter(Boolean);
        const ndcg = computeNDCG(ranked, qrel, K);
        ndcgSum += ndcg;
        n++;
      } catch (e) {
        if (qi === 0) console.error(`  ERROR: ${e.message}`);
      }

      if ((qi + 1) % 50 === 0 || qi === qids.length - 1) {
        process.stdout.write(`\r  ${qi + 1}/${qids.length} NDCG@10=${(ndcgSum/n).toFixed(4)}`);
      }
    }

    const elapsed = (Date.now() - t0) / 1000;
    const avg = n > 0 ? ndcgSum / n : 0;
    console.log(`\n  Final: NDCG@10 = ${avg.toFixed(4)} (${n} queries, ${elapsed.toFixed(1)}s)\n`);

    results[schemeName] = { ndcg_at_10: +avg.toFixed(4), n_queries: n, time_s: +elapsed.toFixed(1) };
  }

  // Summary
  console.log('='.repeat(60));
  console.log('  MaoField Exp003 Summary — NFCorpus NDCG@10');
  console.log('-'.repeat(60));
  const baseline = results.uniform.ndcg_at_10;
  const sorted = Object.entries(results).sort((a, b) => b[1].ndcg_at_10 - a[1].ndcg_at_10);
  for (const [name, res] of sorted) {
    const delta = name === 'uniform' ? '(baseline)' : `${((res.ndcg_at_10 - baseline) / baseline * 100).toFixed(2)}%`;
    console.log(`  ${name.padEnd(22)} ${res.ndcg_at_10.toFixed(4).padEnd(10)} ${delta}`);
  }
  console.log('='.repeat(60));

  // Save
  const outPath = path.join(EXP_DIR, 'exp003_results.json');
  fs.writeFileSync(outPath, JSON.stringify({
    meta: { dataset: 'nfcorpus', top_n: TOP_N, date: '2026-04-08' },
    weight_schemes: Object.fromEntries(
      Object.entries(schemes).map(([k, v]) => [k, v])
    ),
    results
  }, null, 2));
  console.log(`\nSaved: ${outPath}`);
}

main().catch(e => { console.error(e); process.exit(1) });
