# exp019 · α=1 Confirmatory + 多样性-PPL 解耦扩展 · 预注册实验方案

**版本**:v1.0-draft(本文档)→ v1.1(Stage 0 填参,仅准改 §5 noise/power 字段)→ **LOCK**(PI 签字 + git commit on 36)
**状态**:设计稿。未 LOCK 前不得启动任何 GPU 训练。
**证据等级升级目标**:fact 3 三项 α=1 声明 [B+,n=1] → [A,N=6];fact 4 解耦声明 [A−,n=1] → [A,N=5]。
**实验 ID**:exp019(若已占用,LOCK 时顺延为下一空闲号,目录名同步改)。
**产物根目录**:`canonical/wip/exp019_alpha1_confirm_202606XX/`(LOCK 日期定名)。

(设计 agent: aea3e7766e4010e02,2026-06-10。事实基础 fact1-6 见主会话深挖报告。)

---

## 0. 一页摘要

| 项 | 决定 |
|---|---|
| 主实验 | **12 条新链 = α∈{0,1} × 6 个新 seed {101–106}**,seed 跨臂配对,按 seed 分块、块内臂序随机交错,22 号机 9070XT fp32 串行,每链 10 代全长 |
| 主判据 | 固定序列 gatekeeping:**E1 几何(g1)→ E2 PPL(g2)→ E3 path B(g2–g5 窗口)**,每个 one-sided α=0.05,配对 sign-flip 精确置换,**统计单位=链** |
| 旧 α=0 五链 | **不进 primary 检验**(时序混淆),只做噪声先验 + 漂移哨兵 + 漂移量化(exploratory) |
| 副实验 | 零训练:α=0 seeds 1–4 × g0–g9 多样性全曲线(36 CPU,~1.5h),判据 D1–D3,**≥4/5 链解耦成立** |
| 成本 | GPU 72h(48–96h);CPU 串行 ~12h(并行 wall ≤3h);日历 **9 天(7–12)** |
| 预注册 | 预测表 + falsification 二值句 + 分析脚本 commit hash,全部先于第一条 GPU 链 |

## 1. 待确证声明与设计逻辑

### 1.1 待确证声明(全部 [B+, n=1 seed42])
- **C1(几何)**:α=1 压低 gen1 末层几何跳变。s42 效应:PR_centered(L11, g1) 低 12.6(α=0 五 seed sd=1.28 的 ~10 倍)。
- **C2(早期 PPL)**:α=1 缓冲早期 PPL 驼峰。s42 效应:g1 69.3 vs α=0 [77.0, 79.3];g2 89.5 vs [105.3, 108.4]。
- **C3(path B)**:α=1 压低相邻代 KL −10%(三 val_seed:−11.6/−10.4/−8.4%),效应集中 gen1–5,plateau 期消失。
- **C4(解耦,[A−, n=1])**:生成多样性单调塌 vs PPL 驼峰回落解耦 → 推到 N=5(副实验,§6)。

### 1.2 为什么必须同跑新 α=0 对照
原 armb 实验 α 与训练时序完全混淆。若只跑新 α=1 链与旧 α=0 链比较,α 再次与"新/旧 epoch"完全混淆。**primary 比较只准用新 α=0 vs 新 α=1,交错跑**。
旧 α=0 五链三个新角色(全部非 primary):噪声先验源(Stage 0)、漂移哨兵(Gate 0)、漂移量化(exploratory S2)。

### 1.3 范围纪律
本实验只确证 α=1 这一个点,不含 α=5/α=10 臂。完成后 α=10 的 +18.7% [A级] 仍带原时序混淆烙印(§10 失败分支与 R12)。

## 2. 主实验设计

### 2.1 臂 × seed 矩阵
α∈{0,1} × 新 seed {101,102,103,104,105,106}(与历史 {42,1,2,3,4} 不相交,LOCK 时写死)。
同 seed 跨臂配对:gen0 ckpt 全臂相同(sha256 已验,gen0 与 α 无关)+ 同 seed → gen1 训练数据由同一 gen0 模型同 seed 生成,原则上跨臂逐位相同 → gen1 处为严格配对,gen2 起"同源分叉"。
不复跑 s42 α=1:新 seed 回答真问题;旧 s42 链只作先验,排除在确证统计外。

### 2.2 顺序随机化
块 = seed,6 块按 seed 升序;块内两臂顺序由预 commit 的 RNG 决定:
`python -c "import random; random.seed(20260610); print([random.choice(['01','10']) for _ in range(6)])"`
输出原样写进 prereg 并 commit。单 GPU 串行,块内两链间隔 ≤1 链时长。每链 manifest 记 wall-clock 起止。

### 2.3 训练协议 freeze
- 命令模板:`python exp018_cat/src/run_arm_b_alpha_scan.py --alpha {0|1} --seed {S} --num-generations 10 --config configs/cat_arm_b_fp32_9070XT.yaml`(实际 flag 名以脚本为准,LOCK 时核对写死)。
- config sha256 写进 prereg;实验期间 config 只读。
- **fp32 强制断言**:launcher 启动 assert dtype==fp32 且 GradScaler 关闭,违反 fail-fast。
- **gen0 锚断言**:每链启动前 assert gen0 ckpt sha256 == 历史记录值。
- **环境 freeze**:首链至末链,22 禁任何升级;每链 manifest 记 uname/rocminfo/pip freeze 哈希/git hash,12 链断言全相等。
- α=0 的 CAT 分支行为:LOCK 前读 runner,记录 α=0 时 CAT 分支是执行后零加权还是整体跳过——不改行为,只记录。

### 2.4 Run manifest(jsonl)
每链:{chain_id, arm, seed, order_index, block_id, ts_start, ts_end, host, git_hash, config_sha256, rocm_ver, torch_ver, pip_freeze_sha256, gen0_sha256, ckpt_sha256[g1..g9], syndata_sha256[g1..g9], restarts, watchdog_events, gpu_thermal_notes}。

### 2.5 失败/重启/减员政策(预注册)
- 看门狗:per-gen heartbeat;停滞>30min → kill 从最后完整 gen 重启;单链重启≥3 → 停链上报。
- 基础设施原因 → 同 seed 整链重跑并记录;训练动力学内因(loss NaN)→ 不重跑,这是数据,endpoint 记缺失。
- 减员:缺1对 → n=5(最小 p=1/32=0.031 可行);缺2对 → n=4 精确置换最小 p=0.0625 不可过 → 预注册 fallback 配对 t(df=3);缺≥3对 → invalid-underpowered。
- 含重启链照常进 primary;剔除版列 exploratory(S6)。

### 2.6 Stopping rule
n=6 对固定。中期可看 infra 日志,不许据 endpoint 数字加 seed/停跑/换阈值。事后追加链 = exploratory。

## 3. 测量协议(全管线版本锁定)

| 通道 | 脚本 | 输入 | 单位耗时 | 跑在 |
|---|---|---|---|---|
| PPL 离线统一 re-eval | exp018 eval 脚本(锁 commit) | 每链 g0–g9 | ~3–5 min/ckpt CPU | 36,8路并行 |
| L11 几何 panel | armb_geom*.py | 每链 g0–g9 | ~15 s/ckpt | 36 |
| path B/C KL | driver_s42.py + launch_dppl_bridge.py CPU 版 | 每链 9 transition × 3 val_seed | ~60 s/tuple | 36 |
| 生成+多样性 | forward_B/fb_*.py | 指定 (链,gen),128块/config | ~130 s/config | 36 |

- PPL:全部统一脚本离线 re-eval。一致性门:旧 α=0 链 g1/g2/g9 re-eval vs 历史值偏差 ≤±0.5 PPL,否则先修管线再 LOCK。
- path B 3 个 val_seed 与 deep-dive 相同,primary = 三 seed 均值,逐 seed 并报。
- 多样性(主实验内 exploratory):n=512 块。

## 4. Primary endpoints、阈值、统计检验

### 4.0 阈值通则
确证下限 = s42 点效应的 50%(n=1 先验 winner's-curse 收缩 + 防"显著但无意义")。三区判定:确证/不确定/伪。

### 4.1 endpoint 定义(方向预注册 α=1 更低)
**E1 几何(g1)**:Δ₁ = PR_centered(L11,g1) 配对差。确证 Δ̄₁≤−6.3 且 sign-flip one-sided p<0.05;伪 Δ̄₁≥0。(s42 先验 −12.6;sd=1.28)
**E2 早期 PPL(g2)**:Δ₂ = PPL(g2) 配对差(统一 re-eval)。确证 Δ̄₂≤−8.5 且 p<0.05;伪 ≥0。(s42 −17.1;sd≈1.33)secondary:g1 差 ≤−4.4。
**E3 path B(早期窗口)**:每链 r = mean{KL(g1→g2)..KL(g4→g5)}(先逐 val_seed 均值再三 seed 平均);配对量 ln(r_α1/r_α0)。确证 ≤ln0.95=−0.0513 且 p<0.05;伪 ≥0。(s42 −10%)窗口理由:α=10 在 g0→g1 无效应、α=1 效应集中 gen1–5 → 取交集安全区;g0→g1 列 exploratory。

### 4.2 检验方法
统计单位=链,n=6 配对。配对 sign-flip 精确置换(2⁶=64 全枚举),统计量=配对差均值,one-sided,精确 p(粒度 1/64≈0.0156)。CI:pairs-bootstrap B=10⁴。

### 4.3 多重比较:固定序列 gatekeeping
E1→E2→E3,每个 full α=0.05,首个未确证处停止,其后降 exploratory。FWER=0.05。
不用 Holm:最严层 0.0167 < n=6 最小 p 0.0156 仅完美分离擦线,掉1对即不可能;固定序列 n=5 仍可运作。排序按先验效应/噪声比降序:E1(~10σ)→E2(~13σ 但解释面宽)→E3(~1–1.4σ,最弱垫底)。

### 4.4 Gate 0 漂移哨兵
新 α=0 六链:PPL(g2) 均值∈[102.6,110.6](106.6±3sd)且 PR(L11,g1) 均值∈[201.2,208.8](205±3×1.28)。
不过 → 配对比较内部有效性不损,层级照走,结论挂"与历史量级不可直接比"+ 漂移进差异日志。

### 4.5 secondary/exploratory 清单(只报数不升级)
S1 plateau-null:path B g6→g9 配对 log-ratio,预测 |·|<0.05。S2 新旧 α=0 漂移量化。S3 PPL g1。S4 g0→g1 path B。E4 多样性 α 对比 g1,n=512,预测 null(|Δd2|<0.01)。E4b 内容重合率预测∈[25%,40%]。S5 gen1 syndata 哈希跨臂相等比例(诊断)。S6 重启敏感性。S7 g2/g9 几何、全 PPL 曲线。

## 5. 功效分析与 n 论证

### 5.1 噪声先验(Stage 0 输入)
PR(L11,g1) σ̂=1.28(已知);PPL(g2) σ̂≈1.33(range 3.1/2.33);PPL(g1) σ̂≈1.0;ln(path B 窗口) σ̂c **未知,Stage 0 必测**(旧 α=0 五链跑 path B 管线)。配对差 sd 保守 √2·σ̂c(ρ=0)。

### 5.2 功效(n=6,±10pp)
E1:真效应 −12.6 → power≈1.00;−6.3 → >0.99。E2:−17.1/−8.5 → ≈1.00/>0.99。E3:−10%,σ̂c=7%,ρ=0.5 → ≈0.78;ρ=0 → ≈0.55;−7% 收缩 → 0.35–0.55。
**E1/E2 近乎必检出;E3 公开承认弱功效(0.35–0.78)**,故排末位 + mixed-A 分支预设。

### 5.3 n=6 三重理由与升级规则
粒度(64 置换,0.05 临界域={1,2,3}/64);减员容差(坏1对仍合法);成本(72 GPU·h 可承受;n=8 只为 E3 提~10pp 默认不值)。
Stage 0 重校准:σ̂c 实测后,若 power(E3@−10%)<0.50 → PI 三选一:(a)照跑 (b)n→8 (c)E3 预降 exploratory。写入 v1.1 后 LOCK。

## 6. 副实验:解耦扩展(零训练)

### 6.1 配置
旧 α=0 seeds{1,2,3,4} × g0–g9 全 10 代(ckpt 全在 36)。管线 fb_*.py,decode/prompt/seed/n=128 与 s42 run 逐项相同(sha256 进 prereg)。指标:distinct-2(corpus)、rep-4、unigram JSD vs train;块级 bootstrap B=1000。若 s42 复算 bootstrap se(distinct-2)>0.015 → 升 256 块。成本 ~1.5h CPU。

### 6.2 单链判据(s42 先验)
D1 总降:d2(g9)−d2(g0)≤−0.10(s42 −0.201);D2 恢复期续降:d2(g9)−d2(g2)≤−0.05(s42 估≈−0.13);D3 重复率:rep4(g9)−rep4(g0)≥+0.05(s42 +0.132)。支持项:D2b、D4 Spearman ρ(gen,JSD)≥0.564。
**单链解耦 = D1∧D2∧D3。**

### 6.3 N=5 群体判据(含 s42)
5/5 → 升 [A];4/5 → [A−] 保级+例外归因;≤3/5 → 降 [B,seed 依赖]。群体 sign test 5/5 → p=1/32=0.031。完整性:seeds1–4 fb 指标从未算过 → 真预测;预测表 commit 先于第一次 fb 调用。

## 7. 预注册纪律

### 7.1 锁定时序(违序 → 全实验降 exploratory)
T0 prereg v1.0 commit → T1 Stage 0(σ̂c + PPL 一致性门 ±0.5)→ T2 v1.1 commit(只准填 §5)→ T3 分析脚本 commit + dry-run 两项 → T4 PI 签字 LOCK → T5 副实验(CPU)∥ 主实验块1(22)。

### 7.2 预测表(commit 于 T0)
P1 E1 Δ̄₁ 点预测 −9.0,80%CI[−15,−3.5],阈 ≤−6.3∧p<.05,P(确证)=0.65
P2 E2 Δ̄₂ −12,[−20,−5],≤−8.5∧p<.05,0.60
P3 E3 log-ratio −0.072,[−0.14,0],≤−0.0513∧p<.05,0.45–0.55
P4 全确证 0.35–0.45
P5 Gate0 新 α=0 PPL(g2) 均值 106.5,[104,109],∈[102.6,110.6],0.85
P6 E4 null |Δd2|<0.01,0.8
P7 副实验≥4/5,0.75
P8 S5 哈希相等 6/6,≥4/6,0.6
概率假设:P(s42 效应真实且泛化≈0.65–0.7)×条件 power。数据后只准下调。

### 7.3 Falsification 二值句
F1 E1 落伪区 → C1 撤回,s42 判 idiosyncratic。F2 E2 落伪区 → C2 撤回。F3 E3 落伪区 → C3 撤回;落不确定区 → 保 [B+] 标 confirmatory-inconclusive。F4 副实验 ≤3/5 → C4 降 [B,seed 依赖]。撤回入差异日志,不复活。

### 7.4 分析脚本锁定
新增唯一脚本 analysis_confirm_alpha1.py:manifest+jsonl → 配对表 → sign-flip 精确 p → 三区判定。阈值硬编码=prereg。dry-run:①合成 null 1000 次 type-I∈[0.03,0.05];②旧 s42 跑通全流程(non-confirmatory sanity)。LOCK 后只准 infra hotfix 入 amendment log;触判据=作废重注册。

## 8. 成本表
GPU(22 fp32 串行):12 链 × 4–8h(点 6h)= **72h(48–96)** + 首块烟雾 +0–12h。10 代全长不截断(S1/哨兵/多样性曲线需 g6–g9)。
CPU(36):PPL re-eval 135 ckpt ~9h(并行 1.5h);几何 135×15s ~35min;path B 324 tuple ~5.4h(1h);E4 ~1.7h;副实验 ~1.5h;Stage 0 ≤2.3h。合计 ~21h(wall ≤4h)。
存储:12 链 ≈70–80 GB;22 NVMe 无虞;raid1 预检 ≥150GB;**逐链完成即 rsync 进 canonical**(不等全程)。
人工:PI 0.5–1h 签字 + 0.5h Stage0 决策 + 0.5h 分支决策;agent 0.5–1 天定稿脚本 + ~2h 巡检 + 1 天分析报告。
日历:T0–T4 1.5–2 天 → GPU 3–5 天 → 测量+分析 1.5–2 天 → PI 复核 0.5 天 = **9 天(7–12)**。

## 9. 风险清单(R1–R15,带堵法)
R1 时序混淆复发→块内随机化+串行交错+旧链禁入 primary。R2 环境漂移→冻结+manifest 断言+Gate0+S2。R3 fp16 坑→fp32 断言 fail-fast。R4 val 依赖→3 val_seed 均值+逐报;PPL 统一 re-eval。R5 PPL 异源→单脚本+±0.5 门。R6 seed 泄漏→新集不相交+gen0 sha256 断言。R7 存储→预检+逐链 rsync。R8 22 挂死→看门狗+per-gen ckpt+≥3 停链。R9 多重比较→gatekeeping+exploratory 零升级。R10 E3 弱功效甩锅→功效预公开+三区+mixed-A 预登记。R11 多样性检出限→E4 512 块+null 预测;副实验 se>0.015→256 块。R12 α=10 旧混淆→本实验不背书;失败分支强制重审。R13 偷看→stopping rule。R14 减员→n=6 容 1;n=4 fallback t;≥3 invalid。R15 生成非决定论→S5 诊断;配对有效性靠 seed 块结构。

## 10. 决策树
Gate0 不过→可比性降级标注,继续。E1 伪/不确定→【失败】层级终止。E1 过→E2:不过→【混合-B】(P<0.1,两个~10σ 先验劈叉=异常,强制取证先于叙事);过→E3:确证→【成功】(P≈0.35–0.45,三项升 A,"小剂量阻尼器"positive 叙事,下一步剂量曲线/机制探针);不确定→【混合-A】(E1E2 升 A,E3 保 B+ inconclusive);伪→【混合-A′】(C3 撤回,剂量叙事降级)。
失败分支:α=1 线终结(不机械重跑),解耦线独立存活且叙事重心转移;α=10 [A级] 强制重审(R12);F1 撤回入警惕案例库。
副×主组合:主成功×解耦5/5=双声明并立;主失败×解耦≥4/5=单声明 paper(解耦)+α 章节 negative;解耦≤3/5=降 B+seed 异质性立新线索。

## 11. 资产引用与产物路径
复用:run_arm_b_alpha_scan.py + cat_arm_b_fp32_9070XT.yaml(22);四测量管线(36,wip/maofield_armb_deepdive_20260610/)。新写仅 analysis_confirm_alpha1.py。
产物:canonical/wip/exp019_.../{prereg.md, manifests/, raw/, measures/, secondary/, analysis/, amendments.log}。
LOCK 检查单:□阈值预测一致 □σ̂c 填入+n 决定 □管线+分析 hash 在档 □dry-run 过 □PPL 门过 □存储确认 □臂序随机表 commit □PI 签字。

**自检声明**:本文档是设计交付物,非"准备好跑"声明——LOCK 检查单 8 项 0 完成。已公开最大弱点:E3 功效 0.35–0.78、全确证概率 0.35–0.45 非讨好值。
