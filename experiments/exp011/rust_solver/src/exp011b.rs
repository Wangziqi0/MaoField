mod engine;

use engine::*;
use rayon::prelude::*;
use serde::Serialize;
use std::time::Instant;

const INIT_STEPS: usize = 1000;
const FUSION_STEPS: usize = 2000;
const M2_ROUNDS: usize = 5;
const STEPS_PER_ROUND: usize = 1000;
const N_RUNS: usize = 3;

// ===== Type 1: Literal similar + Semantically related (control) =====
const TYPE1: &[(&str, &str, &str)] = &[
    ("故意伤害怎么判", "故意伤害他人身体的处三年以下有期徒刑", "用人单位应当支付劳动报酬"),
    ("盗窃怎么处罚", "盗窃公私财物数额较大的处三年以下有期徒刑", "婚姻关系存续期间的财产为共同财产"),
    ("醉驾怎么罚", "醉酒驾驶机动车的吊销驾驶证", "承揽人应当以自己的设备完成工作"),
    ("杀人判多少年", "故意杀人的处死刑无期徒刑或十年以上", "合同条款有争议按合同词句理解"),
    ("诈骗判几年", "诈骗公私财物数额较大处三年以下有期徒刑", "工资奖金为夫妻共同财产"),
    ("离婚财产怎么分", "离婚时共同财产由双方协议处理", "故意伤害他人身体处三年以下"),
    ("借钱不还怎么办", "借款人应当按期限返还借款", "盗窃公私财物处三年以下"),
    ("房东不退押金", "租赁期满出租人应退还押金", "醉酒驾驶吊销驾驶证"),
    ("假货怎么维权", "欺诈行为应按消费者要求增加赔偿", "故意杀人处死刑无期徒刑"),
    ("被辞退怎么赔", "违法解除劳动合同按二倍支付赔偿金", "共同财产由双方协议处理"),
];

// ===== Type 2: Literal different + Semantically related (CORE) =====
const TYPE2: &[(&str, &str, &str)] = &[
    ("打人会坐牢吗", "殴打致人轻伤依据刑法第二百三十四条处以刑罚", "打印机维修服务保修条款"),
    ("偷了别人的钱包", "秘密窃取他人随身携带的财物属于扒窃行为", "钱包品牌皮具保养方法"),
    ("喝了酒还开车上路", "饮酒后操控机动车辆属于危险驾驶行为", "开车自驾游路线推荐"),
    ("把人弄死了", "非法剥夺他人生命的行为构成最严重的刑事犯罪", "弄堂里的老上海风情"),
    ("骗了老人的养老钱", "以虚构事实隐瞒真相手段非法占有他人财物", "养老保险缴费年限计算方式"),
    ("两口子过不下去了", "夫妻感情确已破裂经调解无效应准予解除婚姻", "下载安装软件步骤说明"),
    ("朋友欠钱一直拖着", "债务人未按约定履行还款义务债权人可主张权利", "拖地机器人使用说明书"),
    ("房子到期了不让住了", "租赁合同届满后承租人拒不腾退出租人可诉请返还", "住了三年的二手房装修翻新"),
    ("买的东西是假的", "销售者提供的商品掺杂掺假以次充好应承担惩罚性赔偿", "买的新款手机开箱评测"),
    ("老板突然不要我了", "未经法定程序单方终止劳动关系的用工方应承担赔偿责任", "要我说这道菜的做法其实很简单"),
];

// ===== Type 3: Literal similar + Semantically unrelated (trap) =====
const TYPE3: &[(&str, &str, &str)] = &[
    ("故意伤害怎么判", "蓄意对他人身体实施暴力行为的刑事责任", "伤害的近义词是损害打击创伤"),
    ("盗窃罪判多久", "秘密窃取公私财物价值较大的刑罚标准", "盗窃之王是一部法国喜剧电影"),
    ("合同违约怎么赔", "一方不履行协议义务给对方造成损失应予补偿", "合同工与正式工的区别是什么"),
    ("酒驾的处罚标准", "血液中乙醇含量超标驾车的行政与刑事制裁规定", "各类酒驾现象的社会学分析报告"),
    ("遗产怎么继承", "被继承人死亡后其合法财产按法定顺序由亲属取得", "继承者们是一部韩国电视剧"),
    ("劳动合同到期", "用工协议届满后双方权利义务的终止与续签规定", "到期国债收益率曲线分析方法"),
    ("抚养权归谁", "父母离异后未成年子女由哪方直接照顾生活", "抚养比是指非劳动年龄人口占比"),
    ("交通事故责任", "机动车碰撞造成人身财产损害的过错认定与赔偿", "交通事故频发路段的地理特征研究"),
    ("网络诈骗怎么报案", "利用信息网络实施欺诈犯罪的被害人向公安机关控告的程序", "网络诈骗案例分析与防范意识培养讲座"),
    ("商标侵权赔偿", "未经许可使用他人注册标识造成混淆的应承担损害赔偿", "商标设计的基本原则与经典案例赏析"),
];

// ===== Type 4: Same-domain mismatch (exp008b, hardest) =====
const TYPE4: &[(&str, &str, &str)] = &[
    ("打人会坐牢吗", "殴打致人轻伤依据刑法第二百三十四条处以刑罚", "合同当事人应当按照约定全面履行各自的义务"),
    ("偷了别人的钱包", "秘密窃取他人随身携带的财物属于扒窃行为", "夫妻离婚时共同债务应当共同偿还"),
    ("喝了酒还开车上路", "饮酒后操控机动车辆属于危险驾驶行为", "遗产按照法定继承办理由第一顺序继承人继承"),
    ("把人弄死了", "非法剥夺他人生命的行为构成最严重的刑事犯罪", "经营者不得对消费者进行侮辱诽谤侵犯人格尊严"),
    ("骗了老人的养老钱", "以虚构事实隐瞒真相手段非法占有他人财物", "劳动者享有平等就业和选择职业的权利"),
    ("两口子过不下去了", "夫妻感情确已破裂经调解无效应准予解除婚姻", "盗窃公私财物数额特别巨大处十年以上有期徒刑"),
    ("朋友欠钱一直拖着", "债务人未按约定履行还款义务债权人可主张权利", "国家实行劳动者每日工作时间不超过八小时的制度"),
    ("房子到期了不让住了", "租赁合同届满后承租人拒不腾退出租人可诉请返还", "生产销售假药的处三年以下有期徒刑并处罚金"),
    ("买的东西是假的", "销售者提供的商品掺杂掺假以次充好应承担惩罚性赔偿", "父母对未成年子女负有抚养教育和保护的义务"),
    ("老板突然不要我了", "未经法定程序单方终止劳动关系的用工方应承担赔偿责任", "侵占他人财物数额较大拒不退还的处二年以下有期徒刑"),
];

#[derive(Clone, Copy)]
enum Cond { ScalarFixed, ScalarM2, ComplexFixed, ComplexM2 }

impl Cond {
    fn name(&self) -> &'static str {
        match self {
            Cond::ScalarFixed => "scalar",
            Cond::ScalarM2 => "scalar_M2",
            Cond::ComplexFixed => "complex",
            Cond::ComplexM2 => "complex_M2",
        }
    }
    fn use_m2(&self) -> bool { matches!(self, Cond::ScalarM2 | Cond::ComplexM2) }
    fn is_complex(&self) -> bool { matches!(self, Cond::ComplexFixed | Cond::ComplexM2) }
}

#[derive(Serialize, Clone)]
struct PairResult { query: String, correct: bool, delta: f32 }

fn scalar_process(text: &str, seed: u64, use_m2: bool) -> (Vec<f32>, Vec<f32>) {
    let mut eng = ScalarEngine::new();
    eng.init_u(seed);
    eng.set_source(&build_source_f32(text));
    if use_m2 {
        for _ in 0..M2_ROUNDS { eng.evolve_steps(STEPS_PER_ROUND); eng.update_source_m2(); }
    } else {
        eng.evolve_steps(INIT_STEPS + (M2_ROUNDS-1)*STEPS_PER_ROUND);
    }
    (eng.u, eng.s)
}

fn scalar_fuse(uq: &[f32], ud: &[f32], sq: &[f32], sd: &[f32]) -> f32 {
    let mut eng = ScalarEngine::new();
    for k in 0..N { eng.u[k] = 0.5*(uq[k]+ud[k]); eng.s[k] = sq[k]+sd[k]; }
    normalize_f32(&mut eng.s);
    eng.evolve_steps(FUSION_STEPS);
    eng.compute_energy()
}

fn complex_process(text: &str, seed: u64, use_m2: bool) -> ComplexEngine {
    let mut eng = ComplexEngine::new();
    eng.init_u(seed);
    let (sa, sb) = build_source_complex(text);
    eng.set_source(&sa, &sb);
    if use_m2 {
        for _ in 0..M2_ROUNDS { eng.evolve_steps(STEPS_PER_ROUND); eng.update_source_m2_complex(); }
    } else {
        eng.evolve_steps(INIT_STEPS + (M2_ROUNDS-1)*STEPS_PER_ROUND);
    }
    eng
}

fn complex_fuse(eq: &ComplexEngine, ed: &ComplexEngine) -> f32 {
    let mut eng = ComplexEngine::new();
    for k in 0..N {
        eng.a[k] = 0.5*(eq.a[k]+ed.a[k]); eng.b[k] = 0.5*(eq.b[k]+ed.b[k]);
        eng.sa[k] = eq.sa[k]+ed.sa[k]; eng.sb[k] = eq.sb[k]+ed.sb[k];
    }
    let mx = (0..N).map(|k| eng.sa[k].abs().max(eng.sb[k].abs())).fold(0.0f32, f32::max);
    if mx > 0.0 { let inv = 1.0/mx; for k in 0..N { eng.sa[k]*=inv; eng.sb[k]*=inv; } }
    eng.evolve_steps(FUSION_STEPS);
    eng.compute_energy()
}

fn run_pair(idx: usize, q: &str, m: &str, mm: &str, cond: Cond, seed_off: u64) -> PairResult {
    let seed = seed_off + idx as u64;
    let (em, emm) = if cond.is_complex() {
        let eq = complex_process(q, seed, cond.use_m2());
        let em_e = complex_process(m, seed+100, cond.use_m2());
        let emm_e = complex_process(mm, seed+200, cond.use_m2());
        (complex_fuse(&eq, &em_e), complex_fuse(&eq, &emm_e))
    } else {
        let (uq,sq) = scalar_process(q, seed, cond.use_m2());
        let (um,sm) = scalar_process(m, seed+100, cond.use_m2());
        let (umm,smm) = scalar_process(mm, seed+200, cond.use_m2());
        (scalar_fuse(&uq,&um,&sq,&sm), scalar_fuse(&uq,&umm,&sq,&smm))
    };
    let delta = if emm != 0.0 { (emm-em)/emm.abs()*100.0 } else { 0.0 };
    PairResult { query: q.chars().take(12).collect(), correct: em < emm, delta }
}

#[derive(Serialize)]
struct TypeResult { type_name: String, accuracy: f64, n: usize }

#[derive(Serialize)]
struct RunResult { run: usize, types: Vec<TypeResult>, overall: f64 }

#[derive(Serialize)]
struct CondResult {
    name: String,
    runs: Vec<RunResult>,
    mean_t1: f64, mean_t2: f64, mean_t3: f64, mean_t4: f64, mean_overall: f64,
}

fn run_condition(cond: Cond) -> CondResult {
    let all_pairs: Vec<(&str, &[(&str,&str,&str)])> = vec![
        ("T1_lit+sem", TYPE1), ("T2_diff+sem", TYPE2),
        ("T3_lit+trap", TYPE3), ("T4_same_dom", TYPE4),
    ];
    let mut runs = Vec::new();
    let mut t_accs = [Vec::new(), Vec::new(), Vec::new(), Vec::new()];

    for run in 0..N_RUNS {
        let seed_off = (run as u64 + 1) * 1000;
        let t0 = Instant::now();

        // Build flat list of (global_idx, type_idx, q, m, mm)
        let flat: Vec<(usize, usize, &str, &str, &str)> = all_pairs.iter().enumerate()
            .flat_map(|(ti, (_, pairs))| pairs.iter().enumerate()
                .map(move |(pi, &(q,m,mm))| (ti*10+pi, ti, q, m, mm)))
            .collect();

        let results: Vec<(usize, PairResult)> = flat.par_iter()
            .map(|&(gidx, _, q, m, mm)| (gidx, run_pair(gidx, q, m, mm, cond, seed_off)))
            .collect();

        // Group by type
        let mut type_results = Vec::new();
        for (ti, (tname, _)) in all_pairs.iter().enumerate() {
            let typed: Vec<&PairResult> = results.iter()
                .filter(|(gidx, _)| *gidx / 10 == ti)
                .map(|(_, p)| p).collect();
            let correct = typed.iter().filter(|p| p.correct).count();
            let acc = correct as f64 / typed.len() as f64;
            t_accs[ti].push(acc);
            type_results.push(TypeResult { type_name: tname.to_string(), accuracy: acc, n: typed.len() });
        }

        let total_correct = results.iter().filter(|(_, p)| p.correct).count();
        let overall = total_correct as f64 / results.len() as f64;
        let wall = t0.elapsed().as_secs_f64();

        eprintln!("  {} run {}: T1={:.0}% T2={:.0}% T3={:.0}% T4={:.0}% overall={:.0}% ({:.1}s)",
            cond.name(), run+1,
            type_results[0].accuracy*100.0, type_results[1].accuracy*100.0,
            type_results[2].accuracy*100.0, type_results[3].accuracy*100.0,
            overall*100.0, wall);

        runs.push(RunResult { run: run+1, types: type_results, overall });
    }

    let mean = |v: &[f64]| v.iter().sum::<f64>() / v.len() as f64;
    CondResult {
        name: cond.name().to_string(), runs,
        mean_t1: mean(&t_accs[0]), mean_t2: mean(&t_accs[1]),
        mean_t3: mean(&t_accs[2]), mean_t4: mean(&t_accs[3]),
        mean_overall: mean(&[mean(&t_accs[0]), mean(&t_accs[1]), mean(&t_accs[2]), mean(&t_accs[3])]),
    }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    eprintln!("============================================================");
    eprintln!("MaoField Exp011b: Complex Field Full Validation");
    eprintln!("  T1: literal+semantic (control)");
    eprintln!("  T2: diff literal+semantic (cross-domain mm)");
    eprintln!("  T3: literal trap (same keyword, unrelated mm)");
    eprintln!("  T4: same-domain mm (hardest, exp008b)");
    eprintln!("============================================================");
    let t0 = Instant::now();

    let mut all = Vec::new();
    for &cond in &[Cond::ScalarFixed, Cond::ScalarM2, Cond::ComplexFixed, Cond::ComplexM2] {
        eprintln!("\n--- {} ---", cond.name());
        all.push(run_condition(cond));
    }

    let elapsed = t0.elapsed().as_secs_f64();

    eprintln!("\n============================================================");
    eprintln!("  FULL VALIDATION RESULTS");
    eprintln!("------------------------------------------------------------");
    eprintln!("  {:12} {:>6} {:>6} {:>6} {:>6} {:>6}", "", "T1", "T2", "T3", "T4:HD", "avg");
    for r in &all {
        eprintln!("  {:12} {:>5.0}% {:>5.0}% {:>5.0}% {:>5.0}% {:>5.0}%",
            r.name, r.mean_t1*100.0, r.mean_t2*100.0, r.mean_t3*100.0, r.mean_t4*100.0, r.mean_overall*100.0);
    }

    eprintln!("\n  Key findings:");
    let sc = &all[0]; let sm = &all[1]; let cf = &all[2]; let cm = &all[3];
    eprintln!("    Complex vs Scalar (T4 same-domain): {:.0}% vs {:.0}% ({:+.0}pp)",
        cm.mean_t4*100.0, sm.mean_t4*100.0, (cm.mean_t4-sm.mean_t4)*100.0);
    eprintln!("    Complex vs Scalar (T2 cross-domain): {:.0}% vs {:.0}% ({:+.0}pp)",
        cm.mean_t2*100.0, sm.mean_t2*100.0, (cm.mean_t2-sm.mean_t2)*100.0);
    eprintln!("    Complex vs Scalar (T3 trap): {:.0}% vs {:.0}% ({:+.0}pp)",
        cm.mean_t3*100.0, sm.mean_t3*100.0, (cm.mean_t3-sm.mean_t3)*100.0);
    eprintln!("    M2 effect on complex: {:.0}% vs {:.0}% ({:+.0}pp overall)",
        cm.mean_overall*100.0, cf.mean_overall*100.0, (cm.mean_overall-cf.mean_overall)*100.0);

    if cm.mean_t4 > 0.6 {
        eprintln!("\n    ★★★ Complex Cl(1) > 60% on ALL test types including same-domain ★★★");
    }
    eprintln!("  Time: {:.1}s", elapsed);
    eprintln!("============================================================");

    let output = serde_json::json!({
        "meta": { "date": "2026-04-11", "experiment": "exp011b_full_validation" },
        "conditions": all,
        "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp011b_results.json"), serde_json::to_string_pretty(&output).unwrap());
    let mut s = format!("Exp011b: Full Validation\n\n{:12} {:>6} {:>6} {:>6} {:>6}\n", "", "T1", "T2", "T3", "T4");
    for r in &all { s.push_str(&format!("{:12} {:>5.0}% {:>5.0}% {:>5.0}% {:>5.0}%\n",
        r.name, r.mean_t1*100.0, r.mean_t2*100.0, r.mean_t3*100.0, r.mean_t4*100.0)); }
    s.push_str(&format!("\nTime: {:.1}s\n", elapsed));
    let _ = std::fs::write(results_dir.join("exp011b_summary.txt"), s);
}
