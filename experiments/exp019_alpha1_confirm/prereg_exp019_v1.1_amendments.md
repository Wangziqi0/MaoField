# exp019 prereg v1.0 → v1.1 修订清单(响应校验 7 必改项)

2026-06-10 晚。本文档 = v1.0-draft 的修订 diff,合并入正文由 36 主会话 commit 时执行(git 落点见修订 4)。
Stage 0 实测项(fp32 乘数)以占位符 `[SMOKE]` 标注,smoke 完成后填入。

## 修订 1(V3c)· E2/secondary 阈值改配对口径,全文统一
- E2 先验:s42 配对 = PPL(g2)|α=1 − PPL(g2)|α=0(同 seed)= 89.521 − 108.396 = **−18.88**(废弃组均口径 −17.1)。
- E2 确证阈:Δ̄₂ ≤ **−9.4**(50% of −18.88;废 −8.5)。
- secondary S3(g1):先验配对 69.311 − 77.519 = −8.21 → 阈 **≤ −4.1**(废 −4.4)。
- 预测表 P2 点预测改 **−13**,80%CI [−22, −5]。
- 全文检查:任何先验/阈值数字一律配对口径,禁组均。

## 修订 2(V3d)· Gate 0 区间重算,禁剔 s0
- PPL(g2) 哨兵:全六链 {s0,s1,s2,s3,s4,s42} mean 107.03, sd 1.978 → 区间 **[101.1, 113.0]**(废 [102.6,110.6],该区间系静默剔除 s0 所致)。
- PR(L11,g1) 哨兵:mean 204.45, sd 1.2847 → **[200.6, 208.3]**(废 [201.2,208.8])。注:PR 的"五 seed"= s1-4+s42,**被迫**(s0 ckpt 仅存 generation_0,无法补测 g1 几何),prereg 写明被迫性,与 PPL 哨兵的六链口径差异照实披露。
- 预测表 P5 阈值改 ∈[101.1,113.0]。

## 修订 3(V2b)· gen0 锚改构造保证
- 删除"assert gen0 sha256 == 历史记录值"(新 seed 无历史值,空集断言)。
- 改为:**每 seed 先训一次 gen0(在块内随机序的第一臂),完成后整目录复制到另一臂**(runner `_ckpt_complete` 查 model.safetensors → resume_from=1 跳过 gen0 训练,实证支持)。跨臂 gen0 相等从"确定性假设"变"构造保证"。
- 锚断言改为:块内两臂 gen0 ckpt sha256 一致(复制后校验)。
- 理由存档:fp32 + ROCm7.2 + 新 torch 下训练 bit 确定性无任何保证(runner 无 determinism flag;旧跨臂 sha256 相同是 May-stack fp16 实证,不可外推)。

## 修订 4(V8.2)· git 落点
- prereg(v1.0/v1.1/LOCK tag)、预测表、analysis_confirm_alpha1.py、测量管线 commit hash 记录:全部 commit 进 **projects/MaoField 主 repo**(36 单点写权)。
- `canonical/wip/exp019_.../` 只放运行产物(manifests/raw/measures/secondary/analysis)——canonical/.gitignore 白名单制下 wip 不入 git,锁定链不依赖它。

## 修订 5(V1+V8.1)· Stage 0 扩充 + 成本表修正
- Stage 0 增列(本修订发布时已在执行):
  - S0-a 22 环境重建:venv + torch ROCm wheel(index 现场试探 newest-first)+ transformers/datasets;HF 资源走 hf-mirror。【2026-06-10 晚启动】
  - S0-b fp32 单代 timing smoke(非实验 seed,如 999):实测每代时长 + VRAM 峰值。OOM → LOCK 前一次性定死 gc config 全 12 链,禁中途换 config。
  - S0-c s42 g2 多样性补测(36,fb 管线)→ D2 先验从内插变实测。【2026-06-10 晚启动】
  - S0-d σ̂c 预估改用 main_D22 现有数据(见修订 6),Stage 0 仅复核。
- 成本表:每链 fp16 实测锚 **4.6h**(α=0 与 α=1 无差);fp32 = 4.6 × [SMOKE 乘数,先验 1.2-2.0] ≈ **5.5-9.2h(点 7.5h)**;12 链 **66-110h(点 ~90h)**。日历 +1 天(环境重建)→ **10 天(8-13)**。
- 22 预检补:VRAM 现占 2.8GB(bge/llama 残留服务,**不杀**——纪律:不擅杀长驻服务;16GB − 2.8 = 13.2GB 可用,fp32 batch128 估 ~8GB 够)。备份澄清:22 历史数据在 raid1 全备份(armb ckpt 在 36 data/,candidate_c 86G + 5060 3G 在 maofield_ckpt_backup_20260529/),环境重建无数据风险。
- 19/5060 备用条款:跨 ROCm→CUDA 破环境恒定,预注册"换机 = 12 链全部重跑,禁混跑"。

## 修订 6(V6)· E3 先验改窗口口径 + 功效重写
- E3 s42 先验:设计窗口(KL g1→g2 .. g4→g5,三 val_seed)ln = **−0.177(−16.3%)**(废全程聚合 −10%)。
- 预测表 P3:点预测 **−0.12**,80%CI **[−0.22, 0]**。
- 确证阈 −0.0513 保留,标注改为"**最低有意义效应**(≥5% 压低)";50% 先验参考值 = −0.089。
- σ̂c 先验(main_D22 α=0/α=10 八链同窗口):跨链 ~**2.8%**,同 seed 配对 ~**2.0%** → power(E3 @ −16.3%)≈**1.0**,@ −0.089 亦 >0.99。废"E3 弱功效 0.35-0.78"全部论述;E3 排序末位的理由改为"与被正则量同族,解释面最窄"(机理排序不变:E1→E2→E3)。
- 预测表 P3 P(确证) 上调禁令:维持 0.45-0.55 不动(纪律:概率只准下调;功效上修不等于效应真实性上修——效应是否泛化出 s42 仍是同一个未知数)。
- P4 全确证维持 0.35-0.45。

## 修订 7(V7a/V5/V4a)· 小补丁三件
- s42 g2 多样性:Stage 0 实测(S0-c),实测值替换 D2 先验"估 ≈−0.13";阈 −0.05 维持(最坏凸界 −0.0895 仍过)。
- runner syndata 落盘补丁:armb runner 现不调 save_synthetic_to_disk → manifest 的 syndata_sha256 与 S5 判据依赖此补丁,列入 LOCK 前改动清单(infra 性质,不触判据)。
- 新代码清单更正:**3 件** = analysis_confirm_alpha1.py + PPL 统一 re-eval driver(薄封装 src/metrics.py 的 compute_perplexity_on_dataset)+ launcher wrapper(fp32 断言/manifest/心跳,基于 chain_watchdog.sh 改造)。
- PPL ±0.5 一致性门:已实测通过(36 CPU vs 历史 GPU 偏差 ≤0.011,50 倍裕度),Stage 0 该项降为例行复核。

## 校验确认无须修订的(留档)
置换算术(临界域 = 最极端 3/64;容 1 正号对 iff 该对 |d| 为最小或次小;n=5 仅全同号;n=4 不可过)· E1 阈 −6.3 与 sd=1.28 · E3 窗口选择(排除 g0→g1,实算无功效损失)· 存储(实测 ~60GB,余量充裕)· 副实验 ckpt 完整性 40/40 · α=0 CAT 整体跳过 = Shumailov 严格等价 · exp019 编号空闲。

## LOCK 检查单状态(v1.1 时点)
□ 阈值/预测与正文一致(本文档合并后 ✓)□ σ̂c 复核+n 决定(S0-d)□ [SMOKE] 乘数填入(S0-b)□ 三件新代码 + dry-run □ PPL 门复核 □ 存储确认 ✓ □ 臂序随机表 commit □ **PI 签字**

## S0-c 完成记录(2026-06-10 晚)
s42 g2 多样性实测(fb 管线,128 块,gen_a0.0_g2_n128.jsonl 已入 /tmp/forward_B,待拷 wip):distinct-2(corpus) g2 = **0.5042**。全轨迹 0.5775(g0)→0.5365(g1)→0.5042(g2)→0.4666(g5)→0.3771(g9) 单调。**D2 先验 = d2(g9)−d2(g2) = −0.127(实测,替换内插估 −0.13);阈 −0.05 维持。**
口径注:本次 rep4 复算用"重复 4-gram 占比"口径(g2=0.132),与 forward_B 原报告的 rep4 口径数值不同(g1: 0.108 vs 0.062)——D2/D3 判据各自锁定单一口径,D3 用 forward_B 原口径,禁混用。

## 修订 8(Stage 0 实测新增,2026-06-11)· gfx1201 LayerNorm backward kernel bug + 强制 patch
- **发现**:torch 2.12.0+rocm7.2 在 gfx1201 上 `native_layer_norm_backward` 的 γ/β 梯度归约**非确定性 NaN**(坏梯度清一色 LN weight/bias;fp32/bf16 同炸、eager/SDPA 无关、hipBLASLt 开关无关、deterministic 模式更糟 50/50 全层;基础 op 单测全过=完整计算图竞态指纹)。后果:fp32/bf16 训练第一个 optimizer step 即权重 NaN。**统一假说(待 fp16+GradScaler 2min 对照)**:5 月 fp16 "GradScaler 静默冻结" 与此同根因(scaler 吞 NaN 梯度→全程 skip)。
- **强制 workaround**:manual LayerNorm monkey-patch(分解 mean/var/affine 基本 op),验证 3/3 bad=0、十步 loss 4.63→3.50 干净下降、代价 +4%(2.63 vs 2.53 s/it)。**12 条 confirmatory 链必须全部经 `patch_ln_and_run.py` wrapper 启动**(= launcher wrapper 三件新代码之一),manifest 加字段 `ln_patch: manual_v1`。
- **环境补充规范**:`HIP_VISIBLE_DEVICES=0`(ROCm 7.2 暴露 512MB 核显,HF Trainer 会错误 DataParallel);transformers 钉 **4.49.0**(5.x 移除 evaluation_strategy 与 runner 不兼容);torch 重装防覆盖(pip 后续安装会用 PyPI CUDA 版覆盖 ROCm 版,凡 pip 操作后必须复验 `torch.__version__` 含 rocm)。
- **upstream issue 材料**:最小复现+定位链(diag_dtype/diag_ops/diag_anomaly/diag_repeat/diag_ln_shape/diag_lnpatch.py)已抢救至本目录 exp019_stage0/。发 issue 与否留 PI(对外动作)。
- smoke4(patch 版,2 代,覆盖生成段)运行中,[SMOKE] 乘数待其完成后填入。

## 修订 9(Stage 0 收官 + 考古输入,2026-06-11 晚)· 终定稿
**dtype 决定:fp16 + manual-LN patch**(config = cat_arm_b.yaml 原版,与 v8 主数据同 dtype)。依据:
- smoke5 实测(seed999,2 代):gen0 test=36.27 ✓、gen1 test=**78.67** ✓ 双双落历史区间;46.6min/2代 → **~6.2h/链,12 链 ≈75h(~3.5 GPU 天)**。fp32+patch 备选(22.9h/链,gen1=78.46 已验)。
- 考古关键修正:candidate_c(5/22-26)的环境 = 今天的环境(D21 5/21 装 torch2.12+rocm7.2)。其 180 ckpt 的 NaN 解剖学**无一例外落在 LayerNorm weight/bias** + 同输入字节分叉 + per-cell lottery = LN race 的 5 月指纹。**无 patch 的任何 dtype 均为抽奖,12 链强制 wrapper 启动(含 patch+断言+manifest)。**
- [SMOKE] 占位全部填实:fp16+patch 6.2h/链;fp32+patch 22.9h/链(乘数 5×,非估的 1.2-2×)。
**S5 改判**:runner 不落盘合成数据 → 不改 runner;S5(gen1 跨臂数据一致性)改为**事后从 gen0 ckpt 确定性重生成对比哈希**(fb 管线 batch 不变性已验 8/8)。12 链零训练代码改动。
**测量协议新增依据(考古)**:探针子集噪声 1e-3 为主导噪声源(candidate_c 噪声阶梯)→ path B 三 val_seed 固定的设计获得定量支撑;armb 链间真实信号 1e-2+ 安全。
**watchdog 新增**:单 gen 耗时 >2× 中位数 = GPU wedge 前兆(candidate_c hipErrorLaunchFailure 指纹),报警不杀。
**dry-run 记录(全过)**:① null-sim 10000 reps type-I=**0.0463**(理论 3/64=0.0469,带 [0.03,0.05] 内);② s42 sanity 管线全通(E1 −12.59/E2 −18.875/E3 −0.1228,n=1 正确判 INCONCLUSIVE,gate 行为正确);③ ppl_reeval 复现历史 s42 g2:108.4038 vs 108.3963(Δ0.0075,门 ±0.5 通过,52.5s/ckpt CPU)。
**臂序随机表 v2(平衡 3+3,random.seed(20260610) shuffle)**:101→α1 先 / 102→α1 先 / 103→α0 先 / 104→α0 先 / 105→α0 先 / 106→α1 先。
**新代码四件就位**(experiments/exp019_alpha1_confirm/scripts/):exp019_launch_chain.py(wrapper)/ run_exp019_all.sh(orchestrator,含 gen0 跨臂复制+逐链 rsync)/ analysis_confirm_alpha1.py(锁定分析,阈值硬编码 E1≤−6.3 / E2≤−9.4 / E3≤−0.0513)/ ppl_reeval.py。
