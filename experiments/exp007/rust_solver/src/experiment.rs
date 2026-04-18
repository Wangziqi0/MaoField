//! Exp007b: M2 stability verification + variant exploration.
//!
//! Conditions:
//!   A  × 3 runs: Fixed S (baseline stability)
//!   B2 × 3 runs: M2 S·u* (stability check)
//!   B2a:         M2 without renormalization (scale matters?)
//!   B2b:         M2 cumulative (= B2, confirmed)
//!   B2c:         M2 single update after round 0 only

use rayon::prelude::*;
use serde::Serialize;
use std::time::Instant;

use crate::adjoint::*;
use crate::field::*;
use crate::source::build_source;

const TEST_PAIRS: &[(&str, &str, &str)] = &[
    ("他打我要怎么判",
     "故意伤害他人身体的处三年以下有期徒刑拘役或者管制",
     "用人单位应当按照劳动合同约定和国家规定向劳动者及时足额支付劳动报酬"),
    ("偷东西会怎么样",
     "盗窃公私财物数额较大的或者多次盗窃的处三年以下有期徒刑",
     "离婚时夫妻共同财产由双方协议处理"),
    ("醉酒开车怎么处罚",
     "醉酒驾驶机动车的由公安机关交通管理部门约束至酒醒吊销机动车驾驶证",
     "承揽人应当以自己的设备技术和劳力完成主要工作"),
    ("杀人判几年",
     "故意杀人的处死刑无期徒刑或者十年以上有期徒刑",
     "当事人对合同条款的理解有争议的应当按照合同所使用的词句"),
    ("诈骗怎么判",
     "诈骗公私财物数额较大的处三年以下有期徒刑拘役或者管制并处或者单处罚金",
     "婚姻关系存续期间所得的工资奖金劳务报酬为夫妻共同财产"),
    ("离婚后房子怎么分",
     "离婚时夫妻共同财产由双方协议处理协议不成的由人民法院判决",
     "故意伤害他人身体的处三年以下有期徒刑拘役或者管制"),
    ("借钱不还怎么办",
     "借款人应当按照约定的期限返还借款",
     "盗窃公私财物数额较大的处三年以下有期徒刑"),
    ("租房合同到期房东不退押金",
     "租赁期限届满承租人应当返还租赁物出租人应当退还押金",
     "醉酒驾驶机动车的由公安机关吊销机动车驾驶证"),
    ("买到假货怎么维权",
     "经营者提供商品或者服务有欺诈行为的应当按照消费者的要求增加赔偿",
     "故意杀人的处死刑无期徒刑或者十年以上有期徒刑"),
    ("被公司辞退怎么赔偿",
     "用人单位违法解除劳动合同的应当按照经济补偿标准的二倍向劳动者支付赔偿金",
     "离婚时夫妻共同财产由双方协议处理"),
];

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
    let mut texts = rows;
    let mut rng: u64 = 42;
    for i in (1..texts.len()).rev() {
        rng = rng.wrapping_mul(6364136223846793005).wrapping_add(1);
        let j = (rng >> 33) as usize % (i + 1);
        texts.swap(i, j);
    }
    texts
}

fn precompute_sources(texts: &[String]) -> Vec<Field3D> {
    texts.par_iter().map(|t| build_source(t)).collect()
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
struct RunResult {
    run: usize,
    accuracy: f64,
    avg_delta: f64,
    pairs: Vec<PairResult>,
}

#[derive(Serialize)]
struct ConditionResult {
    name: String,
    update_mode: String,
    runs: Vec<RunResult>,
    mean_accuracy: f64,
    mean_avg_delta: f64,
}

/// Fuse two fields, return energy.
fn fuse_and_score(u_q: &Field3D, u_d: &Field3D, s_q: &Field3D, s_d: &Field3D) -> f64 {
    let mut u_fused: Field3D = u_q.iter().zip(u_d.iter()).map(|(a, b)| 0.5 * (a + b)).collect();
    let mut s_fused: Field3D = s_q.iter().zip(s_d.iter()).map(|(a, b)| a + b).collect();
    normalize(&mut s_fused);
    evolve(&mut u_fused, &s_fused, FUSION_STEPS);
    energy(&u_fused, &s_fused)
}

/// Process one pair.
fn process_pair(
    pair_idx: usize,
    query: &str,
    doc_m: &str,
    doc_mm: &str,
    mode: UpdateMode,
    corpus_sources: &[Field3D],
    seed_offset: u64,
) -> PairResult {
    let seed = seed_offset + pair_idx as u64;

    let mut s_q = build_source(query);
    let mut u_q = init_field(seed);
    evolve(&mut u_q, &s_q, INIT_STEPS);
    eprintln!("      Query adjoint:");
    let _ = adjoint_iteration(&mut u_q, &mut s_q, corpus_sources, mode);

    let mut s_m = build_source(doc_m);
    let mut u_m = init_field(seed + 100);
    evolve(&mut u_m, &s_m, INIT_STEPS);
    eprintln!("      Match doc adjoint:");
    let _ = adjoint_iteration(&mut u_m, &mut s_m, corpus_sources, mode);

    let mut s_mm = build_source(doc_mm);
    let mut u_mm = init_field(seed + 200);
    evolve(&mut u_mm, &s_mm, INIT_STEPS);
    eprintln!("      Mismatch doc adjoint:");
    let _ = adjoint_iteration(&mut u_mm, &mut s_mm, corpus_sources, mode);

    let e_m = fuse_and_score(&u_q, &u_m, &s_q, &s_m);
    let e_mm = fuse_and_score(&u_q, &u_mm, &s_q, &s_mm);

    let correct = e_m < e_mm;
    let delta = if e_mm != 0.0 {
        (e_mm - e_m) / e_mm.abs() * 100.0
    } else {
        0.0
    };

    let q_short: String = query.chars().take(10).collect();
    eprintln!(
        "      E_m={:.0} E_mm={:.0} {} Δ={:.1}%",
        e_m, e_mm, if correct { "✓" } else { "✗" }, delta
    );

    PairResult {
        query: q_short,
        e_match: e_m,
        e_mismatch: e_mm,
        correct,
        delta,
    }
}

/// Run one condition with n_runs repetitions.
fn run_condition(
    name: &str,
    mode: UpdateMode,
    corpus_sources: &[Field3D],
    n_runs: usize,
) -> ConditionResult {
    let mut runs = Vec::new();

    for run in 0..n_runs {
        let seed_offset = (run as u64 + 1) * 1000;
        eprintln!(
            "\n  --- {} ({}), run {}/{} (seed_offset={}) ---",
            name,
            mode.name(),
            run + 1,
            n_runs,
            seed_offset
        );

        let mut pairs = Vec::new();
        for (idx, &(q, m, mm)) in TEST_PAIRS.iter().enumerate() {
            let q_short: String = q.chars().take(10).collect();
            eprintln!("    Pair {}: '{}'", idx + 1, q_short);
            let r = process_pair(idx, q, m, mm, mode, corpus_sources, seed_offset);
            pairs.push(r);
        }

        let correct = pairs.iter().filter(|p| p.correct).count();
        let acc = correct as f64 / pairs.len() as f64;
        let avg_d = pairs.iter().map(|p| p.delta).sum::<f64>() / pairs.len() as f64;

        eprintln!(
            "  {} run {}: Accuracy={:.0}% Avg Δ={:.1}%",
            name,
            run + 1,
            acc * 100.0,
            avg_d
        );

        runs.push(RunResult {
            run: run + 1,
            accuracy: acc,
            avg_delta: avg_d,
            pairs,
        });
    }

    let mean_acc = runs.iter().map(|r| r.accuracy).sum::<f64>() / runs.len() as f64;
    let mean_delta = runs.iter().map(|r| r.avg_delta).sum::<f64>() / runs.len() as f64;

    eprintln!(
        "\n  {} MEAN: Accuracy={:.0}% Avg Δ={:.1}% (over {} runs)",
        name,
        mean_acc * 100.0,
        mean_delta,
        n_runs
    );

    ConditionResult {
        name: name.to_string(),
        update_mode: mode.name().to_string(),
        runs,
        mean_accuracy: mean_acc,
        mean_avg_delta: mean_delta,
    }
}

pub fn run_all() {
    eprintln!("============================================================");
    eprintln!("MaoField Exp007b: M2 Stability + Variants (Rust)");
    eprintln!("============================================================");

    let t0 = Instant::now();

    eprintln!("\nLoading corpus...");
    let corpus_texts = load_corpus();
    eprintln!("  Law corpus: {} texts", corpus_texts.len());

    eprintln!("\nPrecomputing source fields...");
    let tp = Instant::now();
    let corpus_sources = precompute_sources(&corpus_texts);
    eprintln!("  Done in {:.1}s", tp.elapsed().as_secs_f64());

    let mut all_results = Vec::new();

    // A × 3: Fixed S baseline stability
    all_results.push(run_condition("A_fixed", UpdateMode::Fixed, &corpus_sources, 3));

    // B2 × 3: M2 stability
    all_results.push(run_condition("B2_m2", UpdateMode::M2, &corpus_sources, 3));

    // B2a: M2 without normalization (1 run)
    all_results.push(run_condition("B2a_no_norm", UpdateMode::M2NoNorm, &corpus_sources, 1));

    // B2c: M2 single update only (1 run)
    all_results.push(run_condition("B2c_once", UpdateMode::M2Once, &corpus_sources, 1));

    // Summary
    let elapsed = t0.elapsed().as_secs_f64();
    eprintln!("\n============================================================");
    eprintln!("  SUMMARY");
    eprintln!("------------------------------------------------------------");
    for r in &all_results {
        let run_accs: Vec<String> = r.runs.iter().map(|rr| format!("{:.0}%", rr.accuracy * 100.0)).collect();
        eprintln!(
            "  {:15} ({:25}): mean={:.0}%  runs=[{}]  avg_Δ={:.1}%",
            r.name,
            r.update_mode,
            r.mean_accuracy * 100.0,
            run_accs.join(", "),
            r.mean_avg_delta
        );
    }

    let mean_a = all_results[0].mean_accuracy;
    let mean_b2 = all_results[1].mean_accuracy;
    let acc_b2a = all_results[2].mean_accuracy;
    let acc_b2c = all_results[3].mean_accuracy;

    eprintln!("\n  Key comparisons:");
    eprintln!(
        "    B2 mean ({:.0}%) vs A mean ({:.0}%): M2 {}",
        mean_b2 * 100.0,
        mean_a * 100.0,
        if mean_b2 > mean_a { "STABLE IMPROVEMENT" } else { "not stable" }
    );
    eprintln!(
        "    B2a_no_norm ({:.0}%) vs B2 ({:.0}%): Normalization {}",
        acc_b2a * 100.0,
        mean_b2 * 100.0,
        if acc_b2a > mean_b2 { "not needed" } else if acc_b2a < mean_b2 { "important" } else { "irrelevant" }
    );
    eprintln!(
        "    B2c_once ({:.0}%) vs B2 ({:.0}%): Multi-round update {}",
        acc_b2c * 100.0,
        mean_b2 * 100.0,
        if mean_b2 > acc_b2c { "HELPS" } else { "no effect" }
    );
    eprintln!("============================================================");

    // Output JSON
    let output = serde_json::json!({
        "meta": {
            "date": "2026-04-11",
            "experiment": "exp007b_m2_stability",
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
            }
        },
        "results": all_results,
        "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    // Write files
    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .join("results");
    let _ = std::fs::create_dir_all(&results_dir);

    let json_path = results_dir.join("exp007b_results.json");
    let _ = std::fs::write(&json_path, serde_json::to_string_pretty(&output).unwrap());
    eprintln!("Results saved to {}", json_path.display());

    let summary_path = results_dir.join("exp007b_summary.txt");
    let mut summary = String::from("Exp007b: M2 Stability + Variants (Rust)\n\n");
    for r in &all_results {
        let run_accs: Vec<String> = r.runs.iter().map(|rr| format!("{:.0}%", rr.accuracy * 100.0)).collect();
        summary.push_str(&format!(
            "{} ({}): mean={:.0}% runs=[{}] avg_Δ={:.1}%\n",
            r.name, r.update_mode,
            r.mean_accuracy * 100.0,
            run_accs.join(", "),
            r.mean_avg_delta
        ));
    }
    summary.push_str(&format!("\nTotal time: {:.0}s ({:.1}min)\n", elapsed, elapsed / 60.0));
    let _ = std::fs::write(&summary_path, summary);
    eprintln!("Summary saved to {}", summary_path.display());
}
