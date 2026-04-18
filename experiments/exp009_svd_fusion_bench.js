#!/usr/bin/env node
'use strict';
/**
 * MaoField Exp009: SVD Same-Side Rate + PQ-Chamfer Fusion
 *
 * Uses Rust engine for real PQ-Chamfer (baseline 0.3220),
 * then fuses with SVD same-side rate computed in JS.
 *
 * SVD artifacts: pre-computed 16×4096 projection matrix + 4096 mean vector.
 * For each (query, doc) pair:
 *   1. Get PQ-Chamfer score from Rust engine
 *   2. Project all tokens to 16d SVD space
 *   3. Compute same-side rate across 16 modes
 *   4. Fuse: score = alpha * pq_chamfer + (1-alpha) * same_side_rate
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const TOP_N = parseInt(process.argv[2] || '55');
const K = 10;
const N_MODES = 16;
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

// Load SVD projection matrix (16×4096, f32) and mean (4096, f32)
function loadSvdArtifacts() {
  const projBuf = fs.readFileSync(path.join(EXP_DIR, 'svd_proj_16x4096.bin'));
  const meanBuf = fs.readFileSync(path.join(EXP_DIR, 'svd_mean_4096.bin'));

  const proj = new Float32Array(projBuf.buffer, projBuf.byteOffset, projBuf.byteLength / 4);  // 16*4096
  const mean = new Float32Array(meanBuf.buffer, meanBuf.byteOffset, meanBuf.byteLength / 4);  // 4096

  return { proj, mean };
}

// Project a single 4096d token to 16d SVD space
function projectToken(token, proj, mean) {
  const result = new Float32Array(N_MODES);
  for (let m = 0; m < N_MODES; m++) {
    let dot = 0;
    const off = m * 4096;
    for (let d = 0; d < 4096; d++) {
      dot += proj[off + d] * (token[d] - mean[d]);
    }
    result[m] = dot;
  }
  return result;
}

// Compute same-side rate between query tokens and doc tokens in SVD space
function sameSideRate(qProjections, dProjections) {
  const nq = qProjections.length;
  const nd = dProjections.length;
  let totalAgree = 0;
  let totalPairs = 0;

  for (let m = 0; m < N_MODES; m++) {
    for (let qi = 0; qi < nq; qi++) {
      const qSign = qProjections[qi][m] >= 0 ? 1 : -1;
      for (let di = 0; di < nd; di++) {
        const dSign = dProjections[di][m] >= 0 ? 1 : -1;
        if (qSign === dSign) totalAgree++;
        totalPairs++;
      }
    }
  }
  return totalAgree / totalPairs;
}

// Faster: per-mode average same-side rate (avoids O(nq*nd) per mode)
function sameSideRateFast(qProjections, dProjections) {
  const nq = qProjections.length;
  const nd = dProjections.length;
  let totalRate = 0;

  for (let m = 0; m < N_MODES; m++) {
    let qPos = 0, dPos = 0;
    for (let qi = 0; qi < nq; qi++) {
      if (qProjections[qi][m] >= 0) qPos++;
    }
    for (let di = 0; di < nd; di++) {
      if (dProjections[di][m] >= 0) dPos++;
    }
    const qNeg = nq - qPos;
    const dNeg = nd - dPos;
    // Same-side pairs = pos*pos + neg*neg
    const agree = qPos * dPos + qNeg * dNeg;
    totalRate += agree / (nq * nd);
  }
  return totalRate / N_MODES;
}

async function main() {
  console.log('\n=== MaoField Exp009: SVD Fusion Benchmark ===');
  console.log(`NFCorpus, top_n=${TOP_N}, ${N_MODES} SVD modes\n`);

  // Load SVD artifacts
  console.log('Loading SVD artifacts...');
  const { proj, mean } = loadSvdArtifacts();
  console.log(`  proj: ${proj.length} floats, mean: ${mean.length} floats`);

  // Load Rust engine
  const { LawVexus } = require('/home/amd/HEZIMENG/law-vexus');
  const v = new LawVexus('/tmp/maofield_exp009');

  process.stdout.write('Loading clouds... ');
  v.loadClouds(path.join(DATA_DIR, 'clouds.sqlite'));
  const tokenInfo = v.loadTokenCloudsSqlite(
    path.join(DATA_DIR, 'token_clouds.sqlite'),
    path.join(DATA_DIR, 'query_token_clouds.sqlite')
  );
  console.log('done');

  // We need raw token vectors for SVD projection
  // Load from sqlite directly
  console.log('Loading raw token vectors for SVD projection...');
  const sqlite3 = require('better-sqlite3');

  let docTokens = {};  // file_id -> [Float32Array, ...]
  {
    const db = new sqlite3(path.join(DATA_DIR, 'token_clouds.sqlite'), { readonly: true });
    const rows = db.prepare('SELECT file_id, vector FROM chunks ORDER BY file_id').all();
    db.close();
    for (const row of rows) {
      const fid = row.file_id;
      const vec = new Float32Array(row.vector.buffer, row.vector.byteOffset, row.vector.byteLength / 4);
      if (!docTokens[fid]) docTokens[fid] = [];
      docTokens[fid].push(vec);
    }
  }

  let queryTokens = {};
  {
    const db = new sqlite3(path.join(DATA_DIR, 'query_token_clouds.sqlite'), { readonly: true });
    const rows = db.prepare('SELECT file_id, vector FROM chunks ORDER BY file_id').all();
    db.close();
    for (const row of rows) {
      const fid = row.file_id;
      const vec = new Float32Array(row.vector.buffer, row.vector.byteOffset, row.vector.byteLength / 4);
      if (!queryTokens[fid]) queryTokens[fid] = [];
      queryTokens[fid].push(vec);
    }
  }
  console.log(`  Doc tokens: ${Object.keys(docTokens).length} docs`);
  console.log(`  Query tokens: ${Object.keys(queryTokens).length} queries`);

  // Pre-project all tokens to SVD space
  console.log('Projecting all tokens to SVD space...');
  const t_proj = Date.now();

  const docSvd = {};  // file_id -> [Float32Array(16), ...]
  for (const [fid, tokens] of Object.entries(docTokens)) {
    docSvd[fid] = tokens.map(t => projectToken(t, proj, mean));
  }

  const querySvd = {};
  for (const [fid, tokens] of Object.entries(queryTokens)) {
    querySvd[fid] = tokens.map(t => projectToken(t, proj, mean));
  }
  console.log(`  Projection done (${((Date.now() - t_proj) / 1000).toFixed(1)}s)`);

  // Free raw token memory
  docTokens = null;
  queryTokens = null;
  if (global.gc) global.gc();

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

  // Test schemes
  const alphas = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5];
  const results = {};

  for (const alpha of alphas) {
    const name = alpha === 1.0 ? 'baseline_pq' : `fuse_a${(alpha*10).toFixed(0)}`;
    console.log(`--- ${name} (alpha=${alpha}) ---`);
    const t0 = Date.now();
    let ndcgSum = 0, n = 0;

    for (let qi = 0; qi < qids.length; qi++) {
      const qid = qids[qi];
      const qrel = qrels[qid];
      const qFileId = queryIdToFileId[qid];

      try {
        // Get PQ-Chamfer scores from Rust (top_n=55 from coarse_top=100)
        const h = v.tokenChamferTwoStage(qFileId, 100, TOP_N);
        // h = [[doc_id, score], ...] where score = exp(-2*distance)

        if (alpha === 1.0) {
          // Pure baseline
          const ranked = h.map(x => rev[x[0]]).filter(Boolean);
          ndcgSum += computeNDCG(ranked, qrel, K);
          n++;
        } else {
          // Fuse with same-side rate
          const qSvdTokens = querySvd[qFileId];
          if (!qSvdTokens) { continue; }

          const fused = [];
          for (const [docId, pqScore] of h) {
            const dSvdTokens = docSvd[docId];
            if (!dSvdTokens) {
              fused.push({ id: docId, score: pqScore });
              continue;
            }
            const ssr = sameSideRateFast(qSvdTokens, dSvdTokens);
            fused.push({ id: docId, score: alpha * pqScore + (1 - alpha) * ssr });
          }

          fused.sort((a, b) => b.score - a.score);
          const ranked = fused.map(x => rev[x.id]).filter(Boolean);
          ndcgSum += computeNDCG(ranked, qrel, K);
          n++;
        }
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
    results[name] = { ndcg_at_10: +avg.toFixed(4), n_queries: n, alpha, time_s: +elapsed.toFixed(1) };
  }

  // Summary
  console.log('='.repeat(60));
  console.log('  MaoField Exp009 — SVD Same-Side Rate Fusion (Real NDCG)');
  console.log('-'.repeat(60));
  const baseline = results.baseline_pq.ndcg_at_10;
  const sorted = Object.entries(results).sort((a, b) => b[1].ndcg_at_10 - a[1].ndcg_at_10);
  for (const [name, res] of sorted) {
    const delta = name === 'baseline_pq'
      ? '(baseline)'
      : `${((res.ndcg_at_10 - baseline) / baseline * 100).toFixed(2)}%`;
    console.log(`  ${name.padEnd(20)} ${res.ndcg_at_10.toFixed(4).padEnd(10)} ${delta}`);
  }
  console.log('='.repeat(60));

  const outPath = path.join(EXP_DIR, 'exp009_results.json');
  fs.writeFileSync(outPath, JSON.stringify({
    meta: { dataset: 'nfcorpus', top_n: TOP_N, n_modes: N_MODES, date: '2026-04-08' },
    results
  }, null, 2));
  console.log(`\nSaved: ${outPath}`);
}

main().catch(e => { console.error(e); process.exit(1) });
