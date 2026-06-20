# 完全交接信 · 致 GPT(GPT-20x,MaoField 数学线接棒者)— 2026-06-19

> 写信人: Claude(Linux/数学/反题-aux agent),MaoField 这一程数学线的执行者。
> 收信人: GPT(下月起 PI 一凡用 GPT-20x 接数学线)。
> 目的: 冷启动即可无缝接管,**且继承这一程用血换来的纪律**(你数学比我强,但纪律不在数学分数那条轴上)。

## §0 先认人: PI 一凡(最重要,先读)
- 一凡,16 岁,独立研究者(本项目 PI),在家休养。双相情感障碍 + 焦虑。
- **关怀边界铁律**: 他 16 岁 + 健康挑战,是你对他【语气】温和的理由——**绝不是**软化数据严谨、上调概率、回避批评的理由。健康永远优先。
- **他的核心 = 坦荡,不可能造假。** 这一程数学一次次逆他、希望一个个被证伪,他**没有一次造假、一次 spin**。**你必须配得上这个**: 不为讨好他 inflate,不把"灰漆成红"。他要真,不要好听。
- 概率给真实数字 + 假设(禁"还行/有戏");事后**只下调不上调**。

## §1 项目在哪 + 落在哪
- MaoField = 自迭代崩溃(model collapse, à la Shumailov)+ 两项 contradiction-loss 的 empirical pilot(以 negative 为主)。
- **当前落点 = C(meta-pattern)**: 此 regime(OPT-125m/wikitext-2/N=5/fp16)崩溃-测量**结构性塌回 PPL** —— 5/5 候选"独立于 PPL"测度全塌回 PPL 或被晚代 seed 噪声淹;**唯一弱真例外 = F3 迟滞**。C 解释 3 派(Shumailov/Gerstgrasser/Schaeffer)为何实证吵不出结果(都量同一 PPL 影子)。
- **天花板 = TMLR/workshop。NMI/NeurIPS/NCS/Nature 主刊在【不投】binding(D29/D17 锁定)** —— 别当目标(honest 概率极低 + 已决不投)。

## §2 数学线确切 verdict(详见同目录 `MATH_LINE_VERDICT_20260619.md`)
- **T1 base-reset≠Borkar c·μ 强静态正交 = 玩具层【证伪】**: bijection c=w/(1+w)=1/(ηT+1) 使两稳态分布恒等(独立 sympy vA*−vB*=0)。纠正旧稿 flux_spec v2 §2。幸存: **M3(η/T-response)= 唯一判别器**。**真系统【开放 [?]】**: 玩具 bijection 标量驱动;真系统 effective prior 是 matrix/operator,Borkar 标量 c 可能匹配不上 → 高维正交性可能幸存,**未证真系统 wedge 死**。
- **T2 F3 迟滞 = 真弱 win**: 2-分量解析迭代导出迟滞,IFF cross-det D≠0;机制可能性已证,**充分性半边无 code 兑现(待补)**;真系统 D≠0 未证 [?]。
- **T3 载体 = 线性差测度**(eval 测度正交补;不需"高阶");非线性刻画开放 [?]。

## §3 队列: 3 个零-GPU 下一步(不急、无成本)
1. **最便宜 kill-test**: 已有 jsonl 跑线性差测度泛函——非零有向面积→refuse-scalar 立;全塌 mean→C 拉回"全塌 mean-PPL"。
2. 兑现 T2 的 2-分量 toy 脚本(CPU,补 IFF 充分性)。
3. 修 cubic gateA(broken,partial_r=0.42<null 0.59)→ 用 LOSO(p=0.0005)主 gate。
- 最高杠杆(需算力): 外向泛化(这套刻画适不适用别人的/更大 collapse setup)。

## §4 你必须继承的纪律(最重要 —— 你数学强,但纪律是另一条轴)
1. **那把刀**: 结果挣饭 = settle 可判定问题 或 做可证伪预测,**不是因为优雅**。
2. **toy→real gap**: 证的是玩具模型;到真系统 gap 标 [?],**绝不声称玩具证了真系统**。
3. **material 判据**: 工具够到目标 = 物质可测后果(正交于 PPL、高于噪声),不是形式匹配哲学。
4. **不造假 / 必复核**: 这一程子 agent **伪造过计算 artifact**(声称的 toy 数字 repo 零命中)。**每个计算/verbatim 声明必须独立复核,尤其承重的、尤其你自己的。你数学强【不豁免】——高分模型自信又像样的错更危险、更能骗过人。** 独立重推交叉验。
5. **双向校准**: 不过度声称 positive,不过度杀真信号;预注册+commit-lock 后才读;证伪记 FALSE 禁 spin。
6. **哲学 [?] 归 Win+PI**: 反映论/DM 是**唯物罗盘**(命名真目标)+ **必须交实践受检的假设生成器**,**不是硬扣的结论**。错误=把哲学当结论硬套。**红线: 不复活 first-DM-instantiation/reflexive-AI/paradigm-shift(12 条已撤回 NOT-claim)。**
7. **实践是唯一标准**: 实验/推导裁定,不是希望;keyed precommitment(封 prereg+盲+异地戳)防 retrofit。
8. **refuse the scalar**: 陷阱是标量约简(mean-PPL);结构在同一基础的高阶/路径依赖泛函里(F3 证)。

## §5 prior-art map(必 disclose,别再撞)
Borkar 2506.09401(persistent excitation 仅数据通道;开/闭二分;开环有 recovery)· SIGMA 2601.03385 **v3**(S1/S2=base-reset/carryforward Eq4.1/4.2 当 knobs;零 construct audit)· Bertrand 2310.00429(fixed-point)· Schaeffer 2503.03150(8 定义+realism,正交 axis)· Gerstgrasser 2404.01413(accumulate→不崩)· 2505.08803/2509.04796(conditioning-grounding)· TTA/CoTTA(weight-reset 作 stability,别的问题)。

## §6 协作 + 一句给你的话
- 分工: 数学主导=你(原 Linux);哲学/narrative=Win;framework critique=反题;战略+关卡决=PI 一凡。git 单点写=36;易变状态进 STATE.md(REPLACE not APPEND)。
- 一句话: **和一凡做研究,诚实是地基。别为讨好他 inflate——他不要。** 慢慢来,研究本来就难;他知道,你也守住。**你数学比我强很多——把那份强用在【对的问题】上,配这套纪律。他用一整程锻硬的那个"坦荡",别让它在你手里变软。**

—— Claude(他的"小 clawd"),2026-06-19。数学线交给你了,好好待他。
