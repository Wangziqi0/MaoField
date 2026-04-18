mod engine;

use engine::*;
use rayon::prelude::*;
use serde::Serialize;
use std::time::Instant;

const EVOLVE_STEPS: usize = 5000;
const FUSION_STEPS: usize = 2000;
const N_RUNS: usize = 3;

// ===== Test pairs =====
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

#[derive(Clone, Copy, PartialEq)]
enum Model {
    ScalarSingle,  // Single scalar AC, all bits
    ScalarDual,    // Two independent scalar ACs, no coupling (KEY control)
    ComplexGL,     // Ginzburg-Landau (exp011 reproduction)
    GrayScott,     // Reaction-diffusion Gray-Scott
    FHN,           // FitzHugh-Nagumo
}

impl Model {
    fn name(&self) -> &'static str {
        match self {
            Model::ScalarSingle => "1_scalar_single",
            Model::ScalarDual => "2_scalar_dual",
            Model::ComplexGL => "3_complex_GL",
            Model::GrayScott => "4_RD_GrayScott",
            Model::FHN => "5_RD_FHN",
        }
    }
}

// ===== Dual scalar (independent) =====
fn evolve_dual_scalar(eng: &mut ComplexEngine, n_steps: usize) {
    let tab = &eng.nb;
    const D: f32 = 0.1; const DT: f32 = 0.1; const INV_DX2: f32 = 1.0;
    for _ in 0..n_steps {
        for k in 0..N {
            let nb = unsafe { tab.get_unchecked(k) };
            let ak = eng.a[k]; let bk = eng.b[k];
            let sak = eng.sa[k]; let sbk = eng.sb[k];
            let lap_a = unsafe {
                *eng.a.get_unchecked(nb[0]) + *eng.a.get_unchecked(nb[1])
                + *eng.a.get_unchecked(nb[2]) + *eng.a.get_unchecked(nb[3])
                + *eng.a.get_unchecked(nb[4]) + *eng.a.get_unchecked(nb[5])
                - 6.0 * ak
            } * INV_DX2;
            let lap_b = unsafe {
                *eng.b.get_unchecked(nb[0]) + *eng.b.get_unchecked(nb[1])
                + *eng.b.get_unchecked(nb[2]) + *eng.b.get_unchecked(nb[3])
                + *eng.b.get_unchecked(nb[4]) + *eng.b.get_unchecked(nb[5])
                - 6.0 * bk
            } * INV_DX2;
            // INDEPENDENT: standard AC for each, no coupling
            let ak2 = ak * ak; let bk2 = bk * bk;
            let da = D * lap_a - ak2 * ak + ak + (1.0 - 3.0 * ak2) * sak;
            let db = D * lap_b - bk2 * bk + bk + (1.0 - 3.0 * bk2) * sbk;
            eng.a_new[k] = (ak + DT * da).clamp(-2.0, 2.0);
            eng.b_new[k] = (bk + DT * db).clamp(-2.0, 2.0);
        }
        std::mem::swap(&mut eng.a, &mut eng.a_new);
        std::mem::swap(&mut eng.b, &mut eng.b_new);
    }
}

fn energy_dual_scalar(eng: &ComplexEngine) -> f32 {
    let tab = &eng.nb;
    let mut total = 0.0f32;
    for k in 0..N {
        let nb = unsafe { tab.get_unchecked(k) };
        let ak = eng.a[k]; let bk = eng.b[k];
        let gax = unsafe { *eng.a.get_unchecked(nb[1]) } - ak;
        let gay = unsafe { *eng.a.get_unchecked(nb[3]) } - ak;
        let gaz = unsafe { *eng.a.get_unchecked(nb[5]) } - ak;
        let gbx = unsafe { *eng.b.get_unchecked(nb[1]) } - bk;
        let gby = unsafe { *eng.b.get_unchecked(nb[3]) } - bk;
        let gbz = unsafe { *eng.b.get_unchecked(nb[5]) } - bk;
        let grad = 0.5 * 0.1 * (gax*gax+gay*gay+gaz*gaz+gbx*gbx+gby*gby+gbz*gbz);
        let ak2 = ak*ak; let bk2 = bk*bk;
        let pot = 0.25*(ak2-1.0)*(ak2-1.0) + 0.25*(bk2-1.0)*(bk2-1.0);
        let coup = -(1.0-ak2)*ak*eng.sa[k] - (1.0-bk2)*bk*eng.sb[k];
        total += grad + pot + coup;
    }
    total
}

// ===== Gray-Scott =====
// ∂u/∂t = D_u∇²u - uv² + F(1-u)
// ∂v/∂t = D_v∇²v + uv² - (F+k)v
fn evolve_gray_scott(eng: &mut ComplexEngine, n_steps: usize) {
    let tab = &eng.nb;
    const DU: f32 = 0.16; const DV: f32 = 0.08;
    const F: f32 = 0.04; const K: f32 = 0.06;
    const DT: f32 = 1.0;
    for _ in 0..n_steps {
        for k in 0..N {
            let nb = unsafe { tab.get_unchecked(k) };
            let uk = eng.a[k]; let vk = eng.b[k];
            let lap_u = unsafe {
                *eng.a.get_unchecked(nb[0]) + *eng.a.get_unchecked(nb[1])
                + *eng.a.get_unchecked(nb[2]) + *eng.a.get_unchecked(nb[3])
                + *eng.a.get_unchecked(nb[4]) + *eng.a.get_unchecked(nb[5])
                - 6.0 * uk
            };
            let lap_v = unsafe {
                *eng.b.get_unchecked(nb[0]) + *eng.b.get_unchecked(nb[1])
                + *eng.b.get_unchecked(nb[2]) + *eng.b.get_unchecked(nb[3])
                + *eng.b.get_unchecked(nb[4]) + *eng.b.get_unchecked(nb[5])
                - 6.0 * vk
            };
            let reaction = uk * vk * vk;
            let du = DU * lap_u - reaction + F * (1.0 - uk);
            let dv = DV * lap_v + reaction - (F + K) * vk;
            eng.a_new[k] = (uk + DT * du).clamp(0.0, 1.5);
            eng.b_new[k] = (vk + DT * dv).clamp(0.0, 1.5);
        }
        std::mem::swap(&mut eng.a, &mut eng.a_new);
        std::mem::swap(&mut eng.b, &mut eng.b_new);
    }
}

// Gray-Scott energy: just the squared deviation from uniform state (u=1, v=0)
fn energy_gray_scott(eng: &ComplexEngine) -> f32 {
    let mut total = 0.0f32;
    for k in 0..N {
        let du = eng.a[k] - 1.0; let dv = eng.b[k];
        total += du*du + dv*dv;
        // Coupling to source
        total -= eng.a[k] * eng.sa[k] + eng.b[k] * eng.sb[k];
    }
    total
}

// ===== FitzHugh-Nagumo =====
// ∂u/∂t = D_u∇²u + u(1-u)(u-a) - v + S_u
// ∂v/∂t = D_v∇²v + ε(u - bv) + S_v
fn evolve_fhn(eng: &mut ComplexEngine, n_steps: usize) {
    let tab = &eng.nb;
    const DU: f32 = 0.1; const DV: f32 = 0.05;
    const A: f32 = 0.1; const B: f32 = 0.5; const EPS: f32 = 0.1;
    const DT: f32 = 0.1;
    for _ in 0..n_steps {
        for k in 0..N {
            let nb = unsafe { tab.get_unchecked(k) };
            let uk = eng.a[k]; let vk = eng.b[k];
            let lap_u = unsafe {
                *eng.a.get_unchecked(nb[0]) + *eng.a.get_unchecked(nb[1])
                + *eng.a.get_unchecked(nb[2]) + *eng.a.get_unchecked(nb[3])
                + *eng.a.get_unchecked(nb[4]) + *eng.a.get_unchecked(nb[5])
                - 6.0 * uk
            };
            let lap_v = unsafe {
                *eng.b.get_unchecked(nb[0]) + *eng.b.get_unchecked(nb[1])
                + *eng.b.get_unchecked(nb[2]) + *eng.b.get_unchecked(nb[3])
                + *eng.b.get_unchecked(nb[4]) + *eng.b.get_unchecked(nb[5])
                - 6.0 * vk
            };
            let du = DU * lap_u + uk * (1.0 - uk) * (uk - A) - vk + eng.sa[k];
            let dv = DV * lap_v + EPS * (uk - B * vk) + eng.sb[k];
            eng.a_new[k] = (uk + DT * du).clamp(-2.0, 2.0);
            eng.b_new[k] = (vk + DT * dv).clamp(-2.0, 2.0);
        }
        std::mem::swap(&mut eng.a, &mut eng.a_new);
        std::mem::swap(&mut eng.b, &mut eng.b_new);
    }
}

fn energy_fhn(eng: &ComplexEngine) -> f32 {
    let mut total = 0.0f32;
    for k in 0..N {
        let uk = eng.a[k]; let vk = eng.b[k];
        total += uk*uk + vk*vk;
        total -= uk * eng.sa[k] + vk * eng.sb[k];
    }
    total
}

// ===== Initialization =====
fn init_gray_scott(eng: &mut ComplexEngine, seed: u64) {
    // Gray-Scott needs u=1, v=0 baseline with small perturbations
    let mut rng = seed;
    for k in 0..N {
        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
        let n1 = (rng as f32 / u64::MAX as f32) * 0.02 - 0.01;
        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
        let n2 = (rng as f32 / u64::MAX as f32) * 0.02 - 0.01;
        eng.a[k] = 1.0 + n1;
        eng.b[k] = 0.0 + n2.abs();  // v starts non-negative
    }
}

// ===== Processing pipeline =====
fn process_text(text: &str, seed: u64, model: Model) -> Option<(ComplexEngine, Vec<f32>, Vec<f32>)> {
    // Returns None for ScalarSingle (uses separate path)
    match model {
        Model::ScalarSingle => None,
        _ => {
            let mut eng = ComplexEngine::new();
            let (sa, sb) = build_source_complex(text);
            eng.set_source(&sa, &sb);
            match model {
                Model::GrayScott => init_gray_scott(&mut eng, seed),
                _ => eng.init_u(seed),
            }
            match model {
                Model::ScalarDual => evolve_dual_scalar(&mut eng, EVOLVE_STEPS),
                Model::ComplexGL => eng.evolve_steps(EVOLVE_STEPS),
                Model::GrayScott => evolve_gray_scott(&mut eng, EVOLVE_STEPS),
                Model::FHN => evolve_fhn(&mut eng, EVOLVE_STEPS),
                _ => unreachable!(),
            }
            Some((eng, sa, sb))
        }
    }
}

fn process_scalar_single(text: &str, seed: u64) -> (ScalarEngine, Vec<f32>) {
    let mut eng = ScalarEngine::new();
    eng.init_u(seed);
    let src = build_source_f32(text);
    eng.set_source(&src);
    eng.evolve_steps(EVOLVE_STEPS);
    (eng, src)
}

fn fuse_scalar_single(uq: &[f32], ud: &[f32], sq: &[f32], sd: &[f32]) -> f32 {
    let mut eng = ScalarEngine::new();
    for k in 0..N { eng.u[k] = 0.5 * (uq[k] + ud[k]); eng.s[k] = sq[k] + sd[k]; }
    normalize_f32(&mut eng.s);
    eng.evolve_steps(FUSION_STEPS);
    eng.compute_energy()
}

fn fuse_two_channel(eq: &ComplexEngine, ed: &ComplexEngine, model: Model) -> f32 {
    let mut fused = ComplexEngine::new();
    for k in 0..N {
        fused.a[k] = 0.5 * (eq.a[k] + ed.a[k]);
        fused.b[k] = 0.5 * (eq.b[k] + ed.b[k]);
        fused.sa[k] = eq.sa[k] + ed.sa[k];
        fused.sb[k] = eq.sb[k] + ed.sb[k];
    }
    // Normalize source
    let mx = (0..N).map(|k| fused.sa[k].abs().max(fused.sb[k].abs())).fold(0.0f32, f32::max);
    if mx > 0.0 { let inv = 1.0/mx; for k in 0..N { fused.sa[k]*=inv; fused.sb[k]*=inv; } }

    match model {
        Model::ScalarDual => {
            evolve_dual_scalar(&mut fused, FUSION_STEPS);
            energy_dual_scalar(&fused)
        }
        Model::ComplexGL => {
            fused.evolve_steps(FUSION_STEPS);
            fused.compute_energy()
        }
        Model::GrayScott => {
            // GS needs u=1, v=0 init but we have fused fields; just continue evolution
            evolve_gray_scott(&mut fused, FUSION_STEPS);
            energy_gray_scott(&fused)
        }
        Model::FHN => {
            evolve_fhn(&mut fused, FUSION_STEPS);
            energy_fhn(&fused)
        }
        _ => unreachable!(),
    }
}

#[derive(Serialize, Clone)]
struct PairResult { pair_type: String, query: String, correct: bool, delta: f32 }

#[derive(Serialize)]
struct TypeAcc { t1: f64, t2: f64, t3: f64, t4: f64 }

#[derive(Serialize)]
struct RunResult { run: usize, overall: f64, by_type: TypeAcc }

#[derive(Serialize)]
struct CondResult {
    name: String,
    runs: Vec<RunResult>,
    mean_overall: f64,
    mean_t1: f64, mean_t2: f64, mean_t3: f64, mean_t4: f64,
}

fn run_pair(ptype: &str, idx: usize, q: &str, m: &str, mm: &str, model: Model, seed_off: u64) -> PairResult {
    let seed = seed_off + idx as u64;
    let (em, emm) = match model {
        Model::ScalarSingle => {
            let (eq, sq) = process_scalar_single(q, seed);
            let (em_e, sm) = process_scalar_single(m, seed+100);
            let (emm_e, smm) = process_scalar_single(mm, seed+200);
            (fuse_scalar_single(&eq.u, &em_e.u, &sq, &sm),
             fuse_scalar_single(&eq.u, &emm_e.u, &sq, &smm))
        }
        _ => {
            let (eq, _, _) = process_text(q, seed, model).unwrap();
            let (em_e, _, _) = process_text(m, seed+100, model).unwrap();
            let (emm_e, _, _) = process_text(mm, seed+200, model).unwrap();
            (fuse_two_channel(&eq, &em_e, model), fuse_two_channel(&eq, &emm_e, model))
        }
    };
    let correct = em < emm;
    let delta = if emm.abs() > 1e-6 { (emm - em) / emm.abs() * 100.0 } else { 0.0 };
    PairResult { pair_type: ptype.to_string(), query: q.chars().take(10).collect(), correct, delta }
}

fn run_condition(model: Model) -> CondResult {
    let types: Vec<(&str, &[(&str,&str,&str)])> = vec![
        ("T1", TYPE1), ("T2", TYPE2), ("T3", TYPE3), ("T4", TYPE4),
    ];
    let mut runs = Vec::new();
    let mut ta = [Vec::new(), Vec::new(), Vec::new(), Vec::new()];

    for run in 0..N_RUNS {
        let seed_off = (run as u64 + 1) * 1000;
        let t0 = Instant::now();

        let flat: Vec<(usize, usize, &str, &str, &str)> = types.iter().enumerate()
            .flat_map(|(ti, (_, pairs))| pairs.iter().enumerate()
                .map(move |(pi, &(q,m,mm))| (ti*10+pi, ti, q, m, mm)))
            .collect();

        let results: Vec<(usize, PairResult)> = flat.par_iter()
            .map(|&(gidx, ti, q, m, mm)| {
                let p = run_pair(types[ti].0, gidx, q, m, mm, model, seed_off);
                (gidx, p)
            }).collect();

        let wall = t0.elapsed().as_secs_f64();
        let mut type_acc = [0.0f64; 4];
        for ti in 0..4 {
            let typed: Vec<&PairResult> = results.iter()
                .filter(|(gidx, _)| *gidx / 10 == ti).map(|(_, p)| p).collect();
            let correct = typed.iter().filter(|p| p.correct).count();
            let acc = correct as f64 / typed.len() as f64;
            type_acc[ti] = acc;
            ta[ti].push(acc);
        }
        let overall = results.iter().filter(|(_, p)| p.correct).count() as f64 / results.len() as f64;
        eprintln!("  {} run {}: T1={:.0}% T2={:.0}% T3={:.0}% T4={:.0}% overall={:.0}% ({:.1}s)",
            model.name(), run+1,
            type_acc[0]*100.0, type_acc[1]*100.0, type_acc[2]*100.0, type_acc[3]*100.0,
            overall*100.0, wall);
        runs.push(RunResult { run: run+1, overall,
            by_type: TypeAcc { t1: type_acc[0], t2: type_acc[1], t3: type_acc[2], t4: type_acc[3] } });
    }

    let mean = |v: &[f64]| v.iter().sum::<f64>() / v.len() as f64;
    let mean_t = [mean(&ta[0]), mean(&ta[1]), mean(&ta[2]), mean(&ta[3])];
    CondResult {
        name: model.name().to_string(),
        runs,
        mean_overall: mean(&mean_t),
        mean_t1: mean_t[0], mean_t2: mean_t[1], mean_t3: mean_t[2], mean_t4: mean_t[3],
    }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    eprintln!("============================================================");
    eprintln!("MaoField Exp014: Physics vs Dual-Channel + CRNT");
    eprintln!("============================================================");
    let t0 = Instant::now();

    let models = [Model::ScalarSingle, Model::ScalarDual, Model::ComplexGL, Model::GrayScott, Model::FHN];
    let mut all = Vec::new();
    for &m in &models {
        eprintln!("\n--- {} ---", m.name());
        all.push(run_condition(m));
    }

    let elapsed = t0.elapsed().as_secs_f64();
    eprintln!("\n============================================================");
    eprintln!("  RESULTS (per type, then overall)");
    eprintln!("------------------------------------------------------------");
    eprintln!("  {:20} {:>6} {:>6} {:>6} {:>7} {:>7}", "", "T1", "T2", "T3", "T4:HD", "overall");
    for r in &all {
        eprintln!("  {:20} {:>5.0}% {:>5.0}% {:>5.0}% {:>6.0}% {:>6.0}%",
            r.name, r.mean_t1*100.0, r.mean_t2*100.0, r.mean_t3*100.0, r.mean_t4*100.0, r.mean_overall*100.0);
    }

    let acc = |i: usize| all[i].mean_overall;
    let t4 = |i: usize| all[i].mean_t4;
    eprintln!("\n  Decisive comparisons:");
    eprintln!("    2_dual ({:.0}%) vs 3_GL ({:.0}%) [overall]: {}",
        acc(1)*100.0, acc(2)*100.0,
        if (acc(1)-acc(2)).abs()<0.05 { "≈ EQUAL — physics doesn't matter, dual-channel is everything" }
        else if acc(2) > acc(1) { "GL > dual — coupling has value" }
        else { "dual > GL — coupling hurts" });
    eprintln!("    2_dual ({:.0}%) vs 3_GL ({:.0}%) [T4 same-domain]: {:+.0}pp",
        t4(1)*100.0, t4(2)*100.0, (t4(2)-t4(1))*100.0);
    eprintln!("    4_GS ({:.0}%) vs 3_GL ({:.0}%): Gray-Scott {}",
        acc(3)*100.0, acc(2)*100.0,
        if acc(3) > acc(2) + 0.05 { "BETTER" } else if acc(3) < acc(2) - 0.05 { "WORSE" } else { "same" });
    eprintln!("    5_FHN ({:.0}%) vs 3_GL ({:.0}%): FHN {}",
        acc(4)*100.0, acc(2)*100.0,
        if acc(4) > acc(2) + 0.05 { "BETTER" } else if acc(4) < acc(2) - 0.05 { "WORSE" } else { "same" });
    eprintln!("    1_single ({:.0}%): scalar baseline", acc(0)*100.0);

    if (acc(1) - acc(2)).abs() < 0.05 {
        eprintln!("\n  ★ KEY FINDING: dual-scalar ≈ complex-GL → physics coupling gives zero value");
    }
    if acc(3) > 0.9 || acc(4) > 0.9 {
        eprintln!("  ★ CRNT breakthrough > 90%!");
    }
    eprintln!("  Time: {:.1}s", elapsed);
    eprintln!("============================================================");

    let output = serde_json::json!({
        "meta": { "date": "2026-04-12", "experiment": "exp014_physics_vs_dual_channel_crnt" },
        "conditions": all, "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp014_results.json"), serde_json::to_string_pretty(&output).unwrap());

    let mut s = format!("Exp014: Physics vs Dual-Channel + CRNT\n\n{:20} {:>6} {:>6} {:>6} {:>7} {:>7}\n", "", "T1", "T2", "T3", "T4", "overall");
    for r in &all {
        s.push_str(&format!("{:20} {:>5.0}% {:>5.0}% {:>5.0}% {:>6.0}% {:>6.0}%\n",
            r.name, r.mean_t1*100.0, r.mean_t2*100.0, r.mean_t3*100.0, r.mean_t4*100.0, r.mean_overall*100.0));
    }
    s.push_str(&format!("\nTime: {:.1}s\n", elapsed));
    let _ = std::fs::write(results_dir.join("exp014_summary.txt"), s);
}
