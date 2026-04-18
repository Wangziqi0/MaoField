#!/usr/bin/env node
'use strict';
/**
 * MaoField Exp005: Electromagnetic Chamfer Benchmark
 *
 * Token 电磁力模型 — 把 token 当带电粒子，用库仑力替代 cosine 距离。
 *
 * 5 个变体:
 *   0 = EuclideanDistance  欧氏距离对照
 *   1 = Attraction         引力（异号相吸）
 *   2 = Repulsion          排斥力（同号相斥）
 *   3 = Tension            矛盾张力（吸引-排斥差）
 *   4 = Hybrid             alpha*cosine + (1-alpha)*tension
 *
 * 用法: RAYON_NUM_THREADS=70 node exp005_em_chamfer_bench.js [top_n]
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

async function main() {
  console.log('\n=== MaoField Exp005: Electromagnetic Chamfer ===');
  console.log(`Dataset: NFCorpus, top_n=${TOP_N}\n`);

  const { LawVexus } = require('/home/amd/HEZIMENG/law-vexus');
  const v = new LawVexus('/tmp/maofield_exp005');

  process.stdout.write('Loading clouds... ');
  v.loadClouds(path.join(DATA_DIR, 'clouds.sqlite'));
  v.loadTokenCloudsSqlite(
    path.join(DATA_DIR, 'token_clouds.sqlite'),
    path.join(DATA_DIR, 'query_token_clouds.sqlite')
  );
  console.log('done');

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

  // Schemes
  const schemes = [
    { name: 'pq_chamfer_baseline', em: false },
    { name: 'A_euclidean', mode: 0, alpha: 0, eps: 1e-6 },
    { name: 'B_attraction', mode: 1, alpha: 0, eps: 1e-6 },
    { name: 'C_repulsion', mode: 2, alpha: 0, eps: 1e-6 },
    { name: 'D_tension', mode: 3, alpha: 0, eps: 1e-6 },
    { name: 'E_hybrid_07', mode: 4, alpha: 0.7, eps: 1e-6 },
    { name: 'E_hybrid_05', mode: 4, alpha: 0.5, eps: 1e-6 },
    { name: 'E_hybrid_03', mode: 4, alpha: 0.3, eps: 1e-6 },
  ];

  const results = {};

  for (const scheme of schemes) {
    console.log(`--- ${scheme.name} ---`);
    const t0 = Date.now();
    let ndcgSum = 0, n = 0;

    for (let qi = 0; qi < qids.length; qi++) {
      const qid = qids[qi];
      const qrel = qrels[qid];
      const qFileId = queryIdToFileId[qid];

      try {
        let h;
        if (scheme.em === false) {
          h = v.tokenChamferTwoStage(qFileId, 100, TOP_N);
        } else {
          h = v.emChamferTwoStage(qFileId, 100, TOP_N, scheme.mode, scheme.alpha, scheme.eps);
        }
        const ranked = h.map(x => rev[x[0]]).filter(Boolean);
        ndcgSum += computeNDCG(ranked, qrel, K);
        n++;
      } catch (e) {
        if (qi === 0) console.error(`  ERROR: ${e.message}`);
      }

      if ((qi + 1) % 80 === 0 || qi === qids.length - 1) {
        process.stdout.write(`\r  ${qi + 1}/${qids.length} NDCG@10=${(ndcgSum / n).toFixed(4)}`);
      }
    }

    const elapsed = (Date.now() - t0) / 1000;
    const avg = n > 0 ? ndcgSum / n : 0;
    console.log(`\n  Final: NDCG@10 = ${avg.toFixed(4)} (${n}q, ${elapsed.toFixed(1)}s)\n`);

    results[scheme.name] = {
      ndcg_at_10: +avg.toFixed(4),
      n_queries: n,
      time_s: +elapsed.toFixed(1),
      ...(scheme.mode !== undefined && { mode: scheme.mode }),
      ...(scheme.alpha !== undefined && { alpha: scheme.alpha }),
    };
  }

  // Summary
  console.log('='.repeat(60));
  console.log('  MaoField Exp005 — Electromagnetic Chamfer');
  console.log('-'.repeat(60));
  const baseline = results.pq_chamfer_baseline.ndcg_at_10;
  const sorted = Object.entries(results).sort((a, b) => b[1].ndcg_at_10 - a[1].ndcg_at_10);
  for (const [name, res] of sorted) {
    const delta = name === 'pq_chamfer_baseline'
      ? '(baseline)'
      : `${((res.ndcg_at_10 - baseline) / baseline * 100).toFixed(2)}%`;
    console.log(`  ${name.padEnd(24)} ${res.ndcg_at_10.toFixed(4).padEnd(10)} ${delta}`);
  }
  console.log('='.repeat(60));

  // Save
  const outPath = path.join(EXP_DIR, 'exp005_results.json');
  fs.writeFileSync(outPath, JSON.stringify({
    meta: {
      dataset: 'nfcorpus',
      top_n: TOP_N,
      date: '2026-04-08',
      experiment: 'electromagnetic chamfer — coulomb force model'
    },
    results
  }, null, 2));
  console.log(`\nSaved: ${outPath}`);
}

main().catch(e => { console.error(e); process.exit(1) });
