//! Exp006 main experiment: 5 conditions (A, B1, B2, B3, C).

use rayon::prelude::*;
use serde::Serialize;
use std::time::Instant;

use crate::adjoint::adjoint_iteration;
use crate::config::*;
use crate::field::*;
use crate::source::build_source_mc;

// ===== Test pairs (same as exp004/exp005) =====
const TEST_PAIRS: &[(&str, &str, &str)] = &[
    (
        "他打我要怎么判",
        "故意伤害他人身体的处三年以下有期徒刑拘役或者管制",
        "用人单位应当按照劳动合同约定和国家规定向劳动者及时足额支付劳动报酬",
    ),
    (
        "偷东西会怎么样",
        "盗窃公私财物数额较大的或者多次盗窃的处三年以下有期徒刑",
        "离婚时夫妻共同财产由双方协议处理",
    ),
    (
        "醉酒开车怎么处罚",
        "醉酒驾驶机动车的由公安机关交通管理部门约束至酒醒吊销机动车驾驶证",
        "承揽人应当以自己的设备技术和劳力完成主要工作",
    ),
    (
        "杀人判几年",
        "故意杀人的处死刑无期徒刑或者十年以上有期徒刑",
        "当事人对合同条款的理解有争议的应当按照合同所使用的词句",
    ),
    (
        "诈骗怎么判",
        "诈骗公私财物数额较大的处三年以下有期徒刑拘役或者管制并处或者单处罚金",
        "婚姻关系存续期间所得的工资奖金劳务报酬为夫妻共同财产",
    ),
    (
        "离婚后房子怎么分",
        "离婚时夫妻共同财产由双方协议处理协议不成的由人民法院判决",
        "故意伤害他人身体的处三年以下有期徒刑拘役或者管制",
    ),
    (
        "借钱不还怎么办",
        "借款人应当按照约定的期限返还借款",
        "盗窃公私财物数额较大的处三年以下有期徒刑",
    ),
    (
        "租房合同到期房东不退押金",
        "租赁期限届满承租人应当返还租赁物出租人应当退还押金",
        "醉酒驾驶机动车的由公安机关吊销机动车驾驶证",
    ),
    (
        "买到假货怎么维权",
        "经营者提供商品或者服务有欺诈行为的应当按照消费者的要求增加赔偿",
        "故意杀人的处死刑无期徒刑或者十年以上有期徒刑",
    ),
    (
        "被公司辞退怎么赔偿",
        "用人单位违法解除劳动合同的应当按照经济补偿标准的二倍向劳动者支付赔偿金",
        "离婚时夫妻共同财产由双方协议处理",
    ),
];

/// Load corpus from SQLite.
fn load_corpus() -> Vec<String> {
    let conn = rusqlite::Connection::open(DB_PATH).expect("Failed to open DB");
    let mut stmt = conn
        .prepare("SELECT content FROM law_chunks ORDER BY RANDOM() LIMIT ?1")
        .unwrap();
    let rows: Vec<String> = stmt
        .query_map(rusqlite::params![CORPUS_SIZE], |row| row.get(0))
        .unwrap()
        .map(|r| r.unwrap())
        .collect();

    // Deterministic shuffle with seed=42
    let mut texts = rows;
    // Simple Fisher-Yates with fixed seed
    let mut rng: u64 = 42;
    for i in (1..texts.len()).rev() {
        rng = rng.wrapping_mul(6364136223846793005).wrapping_add(1);
        let j = (rng >> 33) as usize % (i + 1);
        texts.swap(i, j);
    }
    texts
}

/// Precompute source fields for corpus.
fn precompute_corpus(texts: &[String], n_comp: usize) -> Vec<Vec<Field3D>> {
    texts
        .par_iter()
        .map(|t| build_source_mc(t, n_comp))
        .collect()
}

#[derive(Serialize)]
struct PairResult {
    query: String,
    e_match: f64,
    e_mismatch: f64,
    correct: bool,
    delta: f64,
}

#[derive(Serialize)]
struct ConditionResult {
    name: String,
    n_components: usize,
    lambda: f64,
    accuracy: f64,
    avg_delta: f64,
    pairs: Vec<PairResult>,
}

/// Fuse two fields and compute energy.
fn fuse_and_score(
    u_q: &McField,
    u_d: &McField,
    s_q: &[Field3D],
    s_d: &[Field3D],
    lambdas: &Lambdas,
) -> f64 {
    let n_comp = u_q.len();
    let mut u_fused: McField = (0..n_comp)
        .map(|c| {
            u_q[c]
                .iter()
                .zip(u_d[c].iter())
                .map(|(a, b)| 0.5 * (a + b))
                .collect()
        })
        .collect();
    let s_fused: Vec<Field3D> = (0..n_comp)
        .map(|c| {
            let mut sf: Field3D = s_q[c].iter().zip(s_d[c].iter()).map(|(a, b)| a + b).collect();
            let mx = sf.iter().map(|v| v.abs()).fold(0.0f64, f64::max);
            if mx > 0.0 {
                for v in sf.iter_mut() {
                    *v /= mx;
                }
            }
            sf
        })
        .collect();
    evolve_mc(&mut u_fused, &s_fused, lambdas, FUSION_STEPS);
    energy_mc(&u_fused, &s_fused, lambdas)
}

/// Process a single test pair: init + adjoint + fuse for match & mismatch.
fn process_pair(
    pair_idx: usize,
    query: &str,
    doc_m: &str,
    doc_mm: &str,
    n_comp: usize,
    lambdas: &Lambdas,
    corpus_mc: &[Vec<Field3D>],
) -> PairResult {
    let s_q = build_source_mc(query, n_comp);
    let s_m = build_source_mc(doc_m, n_comp);
    let s_mm = build_source_mc(doc_mm, n_comp);

    // Unique seed per pair for reproducibility
    let seed = 1000 + pair_idx as u64;

    // Query
    eprintln!("      Query adjoint:");
    let mut u_q = init_field_mc(n_comp, seed);
    evolve_mc(&mut u_q, &s_q, lambdas, INIT_STEPS);
    let _ = adjoint_iteration(&mut u_q, &s_q, corpus_mc, lambdas, "q");

    // Match doc
    eprintln!("      Match doc adjoint:");
    let mut u_m = init_field_mc(n_comp, seed + 100);
    evolve_mc(&mut u_m, &s_m, lambdas, INIT_STEPS);
    let _ = adjoint_iteration(&mut u_m, &s_m, corpus_mc, lambdas, "m");

    // Mismatch doc
    eprintln!("      Mismatch doc adjoint:");
    let mut u_mm = init_field_mc(n_comp, seed + 200);
    evolve_mc(&mut u_mm, &s_mm, lambdas, INIT_STEPS);
    let _ = adjoint_iteration(&mut u_mm, &s_mm, corpus_mc, lambdas, "mm");

    let e_m = fuse_and_score(&u_q, &u_m, &s_q, &s_m, lambdas);
    let e_mm = fuse_and_score(&u_q, &u_mm, &s_q, &s_mm, lambdas);

    let correct = e_m < e_mm;
    let delta = if e_mm != 0.0 {
        (e_mm - e_m) / e_mm.abs() * 100.0
    } else {
        0.0
    };

    let q_short: String = query.chars().take(10).collect();
    eprintln!(
        "      E_m={:.0} E_mm={:.0} {} Δ={:.1}%",
        e_m,
        e_mm,
        if correct { "✓" } else { "✗" },
        delta
    );

    PairResult {
        query: q_short,
        e_match: e_m,
        e_mismatch: e_mm,
        correct,
        delta,
    }
}

/// Run one experimental condition.
fn run_condition(
    name: &str,
    n_comp: usize,
    lam_value: f64,
    corpus_mc: &[Vec<Field3D>],
) -> ConditionResult {
    let lambdas = if lam_value != 0.0 {
        Lambdas::new(n_comp, lam_value)
    } else {
        Lambdas::zero(n_comp)
    };

    let lam_str = if n_comp > 1 {
        format!("λ={}", lam_value)
    } else {
        "N/A".to_string()
    };
    eprintln!(
        "\n  --- Condition {}: {}-comp, {} ---",
        name, n_comp, lam_str
    );

    let mut pairs = Vec::new();
    for (idx, &(q, m, mm)) in TEST_PAIRS.iter().enumerate() {
        eprintln!("    Pair {}: '{}'", idx + 1, &q.chars().take(10).collect::<String>());
        let r = process_pair(idx, q, m, mm, n_comp, &lambdas, corpus_mc);
        pairs.push(r);
    }

    let correct = pairs.iter().filter(|p| p.correct).count();
    let acc = correct as f64 / pairs.len() as f64;
    let avg_d = pairs.iter().map(|p| p.delta).sum::<f64>() / pairs.len() as f64;

    eprintln!(
        "\n  Condition {}: Accuracy={:.0}% Avg Δ={:.1}%",
        name,
        acc * 100.0,
        avg_d
    );

    ConditionResult {
        name: name.to_string(),
        n_components: n_comp,
        lambda: lam_value,
        accuracy: acc,
        avg_delta: avg_d,
        pairs,
    }
}

/// Main entry: run all 5 conditions and output JSON.
pub fn run_all_conditions() {
    eprintln!("============================================================");
    eprintln!("MaoField Exp006: Multi-Component Field Verification (Rust)");
    eprintln!("============================================================");

    let t0 = Instant::now();

    // Load corpus
    eprintln!("\nLoading corpus...");
    let corpus_texts = load_corpus();
    eprintln!("  Law corpus: {} texts", corpus_texts.len());

    // Precompute source fields for each component count (in parallel)
    eprintln!("\nPrecomputing source fields...");
    let tp = Instant::now();
    let (corpus_1, (corpus_2, corpus_3)) = rayon::join(
        || precompute_corpus(&corpus_texts, 1),
        || {
            rayon::join(
                || precompute_corpus(&corpus_texts, 2),
                || precompute_corpus(&corpus_texts, 3),
            )
        },
    );
    eprintln!("  Done in {:.1}s", tp.elapsed().as_secs_f64());

    let mut all_results = Vec::new();

    // A: 1-component baseline
    all_results.push(run_condition("A", 1, 0.0, &corpus_1));
    // B1: 2-component, no coupling
    all_results.push(run_condition("B1", 2, 0.0, &corpus_2));
    // B2: 2-component, lambda=+0.1
    all_results.push(run_condition("B2", 2, 0.1, &corpus_2));
    // B3: 2-component, lambda=-0.1
    all_results.push(run_condition("B3", 2, -0.1, &corpus_2));
    // C: 3-component, lambda=+0.1
    all_results.push(run_condition("C", 3, 0.1, &corpus_3));

    // Summary
    let elapsed = t0.elapsed().as_secs_f64();
    eprintln!("\n============================================================");
    eprintln!("  SUMMARY");
    eprintln!("------------------------------------------------------------");
    for r in &all_results {
        eprintln!(
            "  {:20}: {:.0}%  avg_Δ={:.1}%  ({}-comp, λ={})",
            r.name,
            r.accuracy * 100.0,
            r.avg_delta,
            r.n_components,
            r.lambda
        );
    }
    eprintln!("\n  Key comparisons:");
    let acc = |i: usize| all_results[i].accuracy;
    eprintln!(
        "    B1 ({:.0}%) vs A ({:.0}%): Pure dimension {}",
        acc(1) * 100.0,
        acc(0) * 100.0,
        if acc(1) > acc(0) { "HELPS" } else { "no effect" }
    );
    eprintln!(
        "    B2 ({:.0}%) vs A ({:.0}%): Repulsive coupling {}",
        acc(2) * 100.0,
        acc(0) * 100.0,
        if acc(2) > acc(0) { "HELPS" } else { "no effect" }
    );
    eprintln!(
        "    B3 ({:.0}%) vs A ({:.0}%): Attractive coupling {}",
        acc(3) * 100.0,
        acc(0) * 100.0,
        if acc(3) > acc(0) { "HELPS" } else { "no effect" }
    );
    eprintln!(
        "    B2 ({:.0}%) vs B3 ({:.0}%): Struggle vs Identity {}",
        acc(2) * 100.0,
        acc(3) * 100.0,
        if (acc(2) - acc(3)).abs() > 0.01 {
            "DIFFERENT"
        } else {
            "same"
        }
    );
    eprintln!(
        "    C ({:.0}%) vs B2 ({:.0}%): More components {}",
        acc(4) * 100.0,
        acc(2) * 100.0,
        if acc(4) > acc(2) { "HELPS" } else { "no effect" }
    );
    if (acc(0) - acc(1)).abs() < 0.01
        && (acc(0) - acc(2)).abs() < 0.01
        && (acc(0) - acc(3)).abs() < 0.01
        && (acc(0) - acc(4)).abs() < 0.01
    {
        eprintln!("    ALL EQUAL → problem is NOT collision dimension, it's source field");
    }
    eprintln!("============================================================");

    // Output JSON to stdout
    let output = serde_json::json!({
        "meta": {
            "date": "2026-04-11",
            "experiment": "exp006_multicomponent_rust",
            "params": {
                "grid_size": GRID,
                "D": D_COEFF,
                "dt": DT,
                "init_steps": INIT_STEPS,
                "interact_steps": INTERACT_STEPS,
                "relax_steps": RELAX_STEPS,
                "fusion_steps": FUSION_STEPS,
                "max_rounds": MAX_ROUNDS,
                "top_k": TOP_K,
                "corpus_size": CORPUS_SIZE,
                "threads": TARGET_THREADS,
            }
        },
        "results": all_results,
        "total_time_s": elapsed,
    });

    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    // Also write summary text
    // Write results JSON
    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let json_path = results_dir.join("exp006_results.json");
    if let Ok(_) = std::fs::write(&json_path, serde_json::to_string_pretty(&output).unwrap()) {
        eprintln!("Results saved to {}", json_path.display());
    }

    let summary_path = results_dir.join("exp006_summary.txt");
    if let Ok(_) = std::fs::write(
        summary_path.to_str().unwrap(),
        format!(
            "Exp006: Multi-Component Field (Rust)\n\n{}\nTotal time: {:.0}s ({:.1}min)\n",
            all_results
                .iter()
                .map(|r| format!(
                    "{}: {:.0}% avg_Δ={:.1}% ({}-comp, λ={})",
                    r.name,
                    r.accuracy * 100.0,
                    r.avg_delta,
                    r.n_components,
                    r.lambda
                ))
                .collect::<Vec<_>>()
                .join("\n"),
            elapsed,
            elapsed / 60.0
        ),
    ) {
        eprintln!("\nSummary saved to {}", summary_path.display());
    }
}
