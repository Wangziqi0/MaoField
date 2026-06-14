# exp019 prereg v1.0-draft 对抗校验报告(校验 agent ac85d16e962f6c416,2026-06-10)

总判:**修订后可 LOCK**——设计骨架(配对+交错+gatekeeping+旧链降级+三区判定)实查后站得住;7 项必改,未改完不得 LOCK。

## 必改 7 项
1. **E2/secondary 阈值改配对口径**:E2 先验=89.521−108.396=−18.88(非组均 −17.1)→ 阈 **−9.4**;secondary g1 先验 −8.21 → 阈 −4.1。全文统一配对口径。
2. **Gate 0 区间重算,禁剔 s0**:正确(全六链)PPL(g2) mean 107.03, sd 1.978 → **[101.1, 113.0]**;PR mean 204.45, sd 1.2847 → **[200.6, 208.3]**。v1.0 的 [102.6,110.6] 系静默剔除 s0(g2=110.18 六链最大,数据完好无剔除理由)。
3. **gen0 锚改"每 seed 训一次 → 跨臂复制"**:新 seed 无历史 gen0,"assert==历史值"是空集断言。runner 的 resume 逻辑(_ckpt_complete 查 model.safetensors → 跳过训练)实证支持复制方案;跨臂 gen0 相等从假设变构造保证。fp32+新 torch 下训练 bit 确定性无任何保证(代码无 determinism flag;旧跨臂 sha256 相同是 May-stack fp16 实证)。
4. **prereg/预测表/分析脚本 commit 进 projects/MaoField repo**:canonical/.gitignore 白名单制,**wip/ 整个被 ignore**(check-ignore 实证)→ v1.0 的锁定时序(T0/T2/T3 靠 commit hash)字面执行=空操作。wip 只放运行产物。
5. **Stage 0 增列:22 训练环境重建 + fp32 单代 timing smoke**:22 的 exp018_cat 现状=无 .venv、无 torch、data/ ckpt 全清、ROCm 已 7.2.0——"复用现成 runner"实为从零重建(install_rocm_torch.sh 在,5 月版本无记录)。fp32 在 22 **零成功记录**(5/10 三连 crash rc=134 后回滚 fp16,当时 llama-server 占 10.4GB;现 VRAM 占 2.8GB 需预检清场)。若 OOM → LOCK 前一次性定死 gc config 全 12 链,禁中途换。成本表改 **~90h(66–110)**(fp16 实测锚 4.6h/链 × 减速 1.2–2.0×),日历 +1 天。
6. **P3/E3 先验改窗口口径**:s42 设计窗口效应 ln=−0.177(−16.3%),非全程聚合的 −10%;P3 点预测改 ~−0.12、CI [−0.22,0];阈 −0.0513 保留但标注改"最低有意义效应"。σ̂c 可用 main_D22 现数据预估:跨链 ~2.8%、配对 ~2.0% → **E3 真实 power≈1.0**,"弱功效"叙事将被 Stage 0 推翻(无害方向)。
7. **补测 s42 g2 多样性(130s)把 D2 先验从内插变实测**;runner 补 syndata 落盘(现 armb runner 不调 save_synthetic_to_disk,S5/syndata_sha256 依赖此补丁);新代码清单改为 ≥3 件(analysis + PPL eval driver + launcher wrapper)。

## 校验中的实测背书(好消息)
- PPL ±0.5 一致性门**实跑通过**:36 CPU re-eval vs 历史 GPU 值偏差 ≤0.011(跨 device+dtype+transformers 4.49→5.9),50 倍裕度。
- 单位耗时全部安全方向:PPL 43s/ckpt(设计 3-5min)、几何 13s、path B 14s/tuple。
- 存储实测单代 483MB(fp16 也存 fp32 master weights → 新链同体积),12 链 ~60GB,raid1 余 12T。
- E3 窗口选择(排除 g0→g1)维持正确:含 B[1] 点效应反而略小(0.847 弱于窗口均值 0.827),无功效损失;α=10 在 B[1] 无效应实证成立(比值 0.992-1.069)。
- 副实验 ckpt 完整性 40/40;exp019 号空闲;fp16 每链实测 4h33-40m(α=0 与 α=1 wall-clock 无差,生成主导)。

## 其他记录
- α=0 时 CAT 整体跳过(enabled=alpha>0 → 纯 HF Trainer)= Shumailov baseline 严格等价,prereg 照实记录。
- n=6 置换临界域精确说法:容 1 个正号对当且仅当该对 |d| 是全组最小或次小;2 个正号对必死(p≥0.0625)。n=5 仅全同号可过;n=4 永不可过(fallback t 必要)。
- E1 sd=1.28 的"五 seed"=s1-4+s42(s0 ckpt 仅剩 1 代无法补测),prereg 写明被迫性。
- 19/5060(8GB)技术上可跑 fp32 batch64+accum2,但跨 ROCm→CUDA 破环境恒定:预注册"换机=12 链全重跑,禁混跑"。
- E4b 重合率 [25,40]% 无数据支撑,纯猜,标注 exploratory。

设计稿:同目录 prereg_exp019_draft_v1.md(设计 agent aea3e7766e4010e02)。

## 补注(2026-06-10 晚,PI 澄清后核实)
V8.1 的"22 data/ckpt 全清"须限定:**数据资产零损失**——armb 旧链 ckpt 全在 36 `data/checkpoints_armb/`(本日全部测量的基础),candidate_c 86G + 5060 3G 在 `raid1/maofield_ckpt_backup_20260529/`。22 本地清理 ≠ 丢失。
缺口仅剩**软件环境**:备份无 venv/pip freeze,install_rocm_torch.sh 不钉版本(动态 index 装 latest),armb jsonl 无版本打印,且 22 的 ROCm 已 6.x→7.2.0 —— 5 月软件栈不可精确复刻。后果已被设计兜住:Gate 0 哨兵(新 α=0 落 [101.1,113.0] 即环境漂移不致命;不落仅降历史可比性,不伤配对内部有效性)。必改项 5 维持(环境重建+fp32 smoke),但定性从"风险"降为"已兜住的已知项"。
