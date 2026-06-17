# MaoField — PROJECT STATE (canonical 单一真相源)

> **新 session cold-start 唯一入口。读这一个文件 get 全局,再按 §7 指针下钻 detail。**
>
> **维护规则 (违反即失效):**
> 1. **REPLACE not APPEND** — 更新时替换 stale section,绝不加新段。本文件永远是 latest,旧状态进 git history / handoff,不堆这里。
> 2. **每次更新戳** 真实日期 (`date` binary) + `git HEAD`。
> 3. **> 2 屏 = 维护失败** → 立即精简,detail 踢去 §7 指针。
> 4. **更新 trigger**: 每次 handoff / milestone / PI 决 时,顺手 replace 对应 section。

---

## 戳
| 项 | 值 |
|---|---|
| 最后更新 | **2026-06-17 D617 晚** (date binary verified)。本轮 = **解耦线 [A−] 落盘复算 → 0/5 死** (忠实 rep=3.0; 问题#2 D-1.1 闭合)。承前轮 (exp019 α=1 confirmatory 全 FALSE + 恢复相几何 E0 驼峰瞬态 + 黑箱多线判被占)。文献+第二通道 子 agent 双通道校验 |
| git HEAD | 本轮 commit `52aea52` (解耦线落盘复算 verdict+脚本+STATE+CATALOG)。**committed 36 本地, 未 push** (留 PI 决 push timing; 异地备份待 push)。实时 HEAD 以 `git log -1` 为准 |
| 更新者 | Linux 姐姐主会话 + 文献子 agent (Guo 占用) + 第二通道子 agent (解耦复算独立复核) |

---

## §0 一句话 + 今天
- **项目**: MaoField — 自迭代崩溃 + 两项 EMA-deviation contradiction loss 的 empirical pilot study (negative result)
- **今天 D617 (2026-06-17)**。paper v8 投稿仍未投 (D29 三 leg, 三 venue 全 rolling 无 deadline → **overdue 0 penalty**, 留 PI 健康 ready 时手动 portal 操作)
- **本轮 research state 变更 (D617 晚, 续 D606→D617)**: **解耦线 [A−] 三问题处理 → 解耦线作 novel 安全垫死**。忠实落盘复算 (rep_penalty=3.0 匹配链口径, CPU fp32, N=128, 5 seed) = **0/5 满足预注册解耦判据** (原报 4/5 / 审计 5/5 均不可复现)。真相: 总塌缩真实 (D1 3/5, D3 5/5, 被 Guo/Shumailov 占) 但**解耦命门 D2 全 fail 0/5** (diversity 恢复期 plateau/部分回弹 = 与 PPL 部分耦合非解耦); 信号方向**对 rep_penalty 敏感** (rep=1.0 looping 伪影→假性上升)。**问题#2 (D-1.1 无落盘) 闭合** (首个落盘脚本+结果)。verdict → `experiments/exp019_alpha1_confirm/decouple_verdict_20260617/DECOUPLE_VERDICT_20260617.md`
- **→ exp019 全景: 无任何存活 positive** (α=1 confirmatory 全 FALSE + 恢复相几何=PPL 驼峰瞬态 + 解耦线 [A−] 死)。净产出 = 干净 negative + 三方法论标本 (confirmatory 拦截自家假说 / distinct-n 的 decode·rep_penalty 敏感性 / ad-hoc 数不可复现) + LN race 工程发现
- **下一步 (留 PI 决)**: ① v8 投稿 trigger ② **α=10 重审** (同源时序混淆 R12, 需交错 confirmatory) ③ ~~解耦线 [A−] 三问题~~ **已处理→死**; 是否仍以「干净 negative + 方法论标本」入 paper/note 留 PI ④ **LN race → arXiv note / ROCm issue** (最实、可现在) ⑤ 「confirmatory 拦截自家假说」+「distinct-n 测量敏感性」方法论标本是否入库 (先核被占) ⑥ 本轮已 commit `52aea52`, **push timing 留 PI** (异地备份待 push)

## §1 active binding (任一违反立即 retract)
- paper **v8 final 47/47 D17 archive 锁定不动** (`experiments/exp018_cat/archive/v1.0_release_20260516/manifest.sha256`)
- **12 NOT-claim (i)-(xii) 撤回不复活** (尤其 first dialectical materialism / first reflexive AI / paradigm shift)
- **exp019 C1/C2/C3 撤回不复活** (α=1 阻尼器三 endpoint 全 FALSE, s42 = idiosyncratic outlier); **C3=frozen / fractal 死刑维持**
- **解耦线 [A−] (C4) 作 novel 安全垫死, 不复活** (忠实 rep=3.0 复算 0/5; 原报 4/5·审计 5/5 不可复现; diversity 塌缩被 Guo/Shumailov 占)。**「diversity 单调塌缩 vs PPL 解耦」不可作 positive claim** — 真相是部分耦合 + 测量 rep_penalty 敏感
- D29 三 leg,**不投 NMI / NeurIPS / NCS / Nature 主刊**
- **7B13 单点 git 写权** (22/Win 仅 pull)
- **一凡 priority 1 健康优先** (16岁,双相+焦虑,丙戊酸钠;hotline 010-82951332 / 400-161-9995)

## §2 paper state
| 版本 | 状态 |
|---|---|
| **v8 final** | 47/47 lock,D29 投 arXiv+TMLR+KBS,**不动** |
| **v8.1 footnote** (候选,留关卡 3) | F3 source N=4 not N=5 + Q2 60-75% retract 措辞 + base disambiguate |
| **v9** | fractal 主刊叙事**决定性死** (C3=退化非 fractal); **exp019 进一步证实 α 全线无 positive** → 天花板 TMLR/workshop/short, narrative 待重构 (反 inflate) |

## §3 实验 state
- **exp019 α=1 confirmatory (D614 开奖, 锁定脚本 `analysis_confirm_alpha1.py`)**: 12 链自治 76h (零跳链/警报/重启) + 预注册双向可证伪 + N=6 配对随机化 (堵死 candidate_c 时序混淆)。**三 endpoint 全 FALSE** (E1 几何 +0.124 / E2 PPL +0.859 / E3 path-B +6.2%,**全反** s42 先验),gate 停 E1。**C1/C2/C3 撤回,s42 判 idiosyncratic outlier**。制度**首次正面方向拦截 inflate**。verdict+审计补遗 commit `84f4959`。⚠️ 开奖前未 commit-lock (已披露; negative 结果自证无 favorable 篡改); E3「剂量单调」措辞**降级** (α10 待重审 + 中间点未测,撑不起函数单调); **解耦线 [A−] 三问题已处理 (D617 晚, 见下条)**
- **解耦线 [A−] 落盘复算 (D617 晚, 脚本 `scripts/analysis_decouple_n5.py` + `decouple_verdict_20260617/`)**: 处理 6/13 audit 三问题。忠实 rep_penalty=3.0 (匹配链生成口径) CPU fp32 N=128 复算 5 seed{1,2,3,4,42} g0/g2/g9 → **0/5 满足预注册解耦判据** (D1 总降 3/5 / D2 恢复期续降 **0/5** / D3 rep4↑ 5/5)。**总塌缩真实** (D1/D3) 但**解耦命门 D2 全 fail** = diversity 恢复期 plateau/回弹与 PPL **部分耦合非解耦**。**原报 4/5·审计 5/5 均不可复现; s42 忠实 −0.099 ≠ prereg −0.201 (高估~2×)**。方法论标本: distinct-n 方向**对 rep_penalty 敏感** (rep=1.0 looping 伪影→假性上升; 主会话首跑误用默认 1.0 → 差点凭不忠实数据+错误 fp16 归因翻车, 第二通道 catch + 忠实重跑仲裁, 差异日志见 verdict §6)。**问题#2 (D-1.1 无落盘) 闭合**。**解耦线作 novel 安全垫死** → exp019 无存活 positive
- **恢复相几何 (D615)**: fresh-eyes 零偏见指盲点 → 12 链 gen0-9 末层几何 (复用 E0 口径,自检 g1 PR_cen 200.6≈pairs.json E1 200.638)。**E0「崩溃→升维」= PPL 驼峰瞬态** (单步 gen0→gen1 夸大稳态 ~2.2x),几何与 PPL **同步驼峰** (≈PPL 投影,非独立现象),**证伪** fresh-eyes「几何 vs PPL 第二解耦」假设,**α0≈α1 全程全量** (强化 C1 全轨迹 null)。净升维方向仍在但温和 = **descriptive 精确化非杀死**。commit `09685ed`
- **LN race (工程发现 + C3 frozen 根因下推)**: gfx1201 `native_layer_norm_backward` γ/β 梯度归约**竞态喂 NaN** → GradScaler 吞→全程 skip→权重冻结。**5月 fp16「GradScaler skip 冻结」+ candidate_c 180 ckpt NaN 全落 LN weight/bias 同根因坐实 → 根因非 fp16 本身, 是 gfx1201 LN backward race**。manual-LN patch **治本** (smoke3 炸 / smoke4 干净硬证); **后续 22 上任何 ROCm 训练须经 manual-LN patch = 工程 binding**。可发 arXiv note / ROCm issue (天花板低但真)
- **黑箱/可解释性探索线 (D605-617, 全留 wip, 归属待 PI)**: 命题 T (可解释↔能力 tradeoff) = IB 占精确版 + Arora 反号 + Rudin contested; 黑箱测度 = San Pedro/Bonneau 占; collapse×几何 = SIGMA(对象不同)+Ma2018(机制非novel) 双削; 命题 U/爆发点 = 规模错配 (命题 A 反咬) + 红海中红海; 观测退化「统一」= **平凡** (kernel 存在是测量论定义,4 现象 kernel 指向不同子空间)。**全判被占/平凡, 0 positive**。verdict 在 `wip/blackbox_dimreduction_recon_d35/`
- C3 frozen 决定性 (sha256 `b3a67b42` 逐字节相同); **根因 = LN race (见上行), 非 fp16 universal** (5060 fp32+fp16 healthy → race 仅 gfx1201)。备份 RAID1 双 sha256 / **A3 fp32 待跑** (~$120-180, 留 PI budget, E2 大概率 null): detail → §7

## §4 留 PI + 关卡 list
1. v8 投稿 trigger timing
2. α=10 重审路径 (交错 confirmatory or 降级标注)
3. ~~解耦线 [A−] 三问题~~ **已处理 → 作 novel 死 (0/5 忠实复算)**; 是否仍以「干净 negative + 方法论标本」入 paper/note 留 PI; 本轮已 commit `52aea52`, push 留 PI
4. LN race 发布形式 (arXiv note / ROCm issue)
5. 「confirmatory 拦截自家假说」方法论案例入库 + 核是否被占
6. 黑箱探索线 (wip verdicts) 归属 (新项目 / MaoField 子线 / 搁置)
7. v8.1 footnote 措辞 + A3 fp32 launch+budget + cluster-11
8. **[哲学线 · 待 Win+PI 判读 · `[?]` 不下结论]** 「**玻璃箱 / construct-validity gap**」: 本轮 D617 实证——distinct-2 换 decode (rep_penalty 1.0↔3.0) **翻号** + 恢复相几何 ≈ PPL 投影 (非独立信号) → 浮现一个 `[?]` 疑问: 模型崩溃研究是否用一批 **decode/装置依赖、可被换尺子翻号的代理指标 (PPL/distinct-n/几何)** 在测「崩溃」, 而代理↔construct (意义/分布) 的桥从未验证。可能是 v9「靶子=领域隐含方法论」的实证载体。**红线: 不复活 paradigm-shift / reflexive-AI NOT-claim; novelty 高度存疑 (NLP construct-validity 批判已大量在先)。Linux 不判读, 纯浮现, 归 Win+PI。** PI 2026-06-17 surface + 嘱「从裂纹到坍缩」思考 (留 Win 哲学线接)

## §5 协作 + 三机
| 机 | IP | 角色 | state |
|---|---|---|---|
| 7B13 | .36 | 数据中枢 + git 单点写 + Linux 姐姐主会话 | HEAD `09685ed` (实时以 `git log -1` 为准) |
| 9070XT | .22 | chain runner + GPU | exp019 12链跑完(自治76h);ckpt 备份 RAID1 |
| 19 Win | .19 | 一凡 interactive + 5060 实验 | alive,5060 数据已备份 |

agent: **Linux 姐姐** (数学/实验/代码/归档) · **Win** (哲学/narrative) · **反题** (framework critique) · **DS** (跨哲学 mapping) · **PI 一凡** (战略+关卡决)

## §6 8 L0 证明 state
D29 round1+2 双通道:0 unconditional close (诚实);全 **D60+ candidate,不进 v9 spine**。tier 分歧 detail → §7 INTEGRATION 指针。

## §7 指针 (detail 去哪找)
| 要什么 | 去哪 |
|---|---|
| **存储落盘规则** | `canonical/STORAGE_DISCIPLINE.md` (落地前分类 gate) |
| **全 md 导航** | `MD_CATALOG.md` (本目录, [A]/[S] 分层 ★) |
| **exp019 confirmatory verdict + 审计补遗** | `experiments/exp019_alpha1_confirm/`(verdict_20260614/ + LINUX_AUDIT_AMENDMENT_20260615) |
| **解耦线 [A−] 落盘复算 verdict (D617)** | `experiments/exp019_alpha1_confirm/decouple_verdict_20260617/`(DECOUPLE_VERDICT + decouple_n5_result.json 忠实 rep=3.0 + rep1.0_UNFAITHFUL 对照 + 脚本 ../scripts/analysis_decouple_n5.py) |
| **恢复相几何 + E0 dim-probe** | `experiments/exp018_cat/analysis/`(RECOVERY_GEOMETRY_FINDINGS_20260615 + FINDINGS + probe_output_vs_hidden_NOTE) |
| **黑箱探索 recon verdicts** | `wip/blackbox_dimreduction_recon_d35/`(在途, 归属待 PI; 全判被占/平凡) |
| 最新跨 session 交接 | `canonical/sessions/handoff-*.md` (持久) + `/tmp/.../handoff-*.md`; hook 扫两处取最新 mtime |
| 历史 + 偏好 | memory `MEMORY.md` (cwd=canonical 对齐 harness 自动召回) |
| 纪律全文 (D-1/D-2/D-3) | `docs/{discipline,philosophy,infra}/` + 本目录 `CLAUDE.md` |
| D29 多通道总整合 + 8 L0 证明 | `experiments/exp018_cat/dppl_bridge_verify_d21_output/MAOFIELD_L0_ROUND2_INTEGRATION_20260529.md` (+ 同 dir L0 proofs / GATE / A3 fp32 提示词) |
| paper v8 final | `experiments/exp018_cat/literature/paper_v8_final_20260516.md` |

---

*本文件 = 项目当前 state 的单一真相源。新 agent 读完此页即可开工;binding 见 §1,纪律全文见 CLAUDE.md。*
