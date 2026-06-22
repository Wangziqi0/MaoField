# MaoField 的真实代码数学与玻璃箱审判

## 证据边界与交叉核验

这份报告只承认三类证据：一是直接读取到的 GitHub 仓库代码与配置；二是落盘的 JSON / JSONL 结果与 verdict 文件；三是从这些对象严格推出的数学结论。`GPT55_PRO_RESEARCH_INDEX_20260622.md`、`交接索引_GPT_20260626.md`、`MD_CATALOG.md`、`STATE.md` 在这里被当作导航与交叉核验入口，不当作终局证据；真正承重的仍然是 `contradiction_loss.py`、`cat_trainer.py`、`train_one_generation.py`、`run_arm_b_alpha_scan.py`、两套 `cat_arm_b*.yaml`、`locked_verdict.json`、`decouple_n5_result.json`、`highorder_result.json` 及其验证脚本。仓库自己的交接文本也明确要求把 “RAG/交接索引” 与 “代码/JSON/可复现结论”分开对待。fileciteturn2file0L13-L26 fileciteturn3file0L4-L4 fileciteturn4file0L4-L4 fileciteturn9file0L7-L9

先说一个我在交叉核验中发现的、会影响数学重建的细节：历史 handoff 文件把 “`kl_history_K=1` 来自 YAML schema 缺字段、`getattr(...,1)` 兜底” 作为链路解释的一部分；但当前仓库里的 `config.py` 已经把 `T_2_form`、`kl_history_K`、`m_eff` 明确放进了 `CATYamlConfig` 默认字段里，而 `train_one_generation.py` 的 `CATConfig` 旧框架默认值仍是 `relu_dpp / K=1 / m_eff=1.0`。这意味着：**“当前仓库中 schema 缺字段”这个解释已经过时，但“历史链条实际跑成 relu_dpp + K=1”这个结果仍然成立**，因为旧 `cat_arm_b.yaml` 本身就没有提供这些字段，而包装层默认值正好就是旧框架值。这个差别很小，但如果不指出，就会把“历史为何如此”与“当前代码现在长什么样”混成一团。fileciteturn22file0L107-L123 fileciteturn19file0L42-L58 fileciteturn20file0L4-L4 fileciteturn8file0L4-L4

## 真实代码数学

### 形式化定义

设训练内步为 \(t\)，仅在每个 `kl_update_every` 的时刻抽出一个 KL 更新索引 \(n\)。当前模型参数为 \(\theta_t\)，参数 EMA 为 \(\bar\theta_t\)。在辅助验证 loader 的一个 batch 上，代码构造当前模型分布 \(p_{\theta_t}\) 与 EMA 模型分布 \(q_{\bar\theta_t}\)，并计算

\[
D_n
=
\frac{1}{M_n}
\sum_{b,t'}
m_{b,t'}
\sum_v
q_{n,b,t'}(v)\bigl(\log q_{n,b,t'}(v)-\log p_{n,b,t'}(v)\bigr),
\quad
M_n=\sum_{b,t'} m_{b,t'}.
\]

这就是在 mask 后的 token 位置上，对 **EMA 模型到当前模型** 的 \(\mathrm{KL}(q\|p)\) 平均。梯度只穿过当前模型的 `log_p`，而 \(q\) 由 EMA 模型给出并 `detach`。在取值层面，这是一个**标量** \(D_n\)，不是向量场，不是 token-group 张量，也不是 hidden-state 函数。当前 fetched 的 operative 路径里，没有 JS divergence，也没有任何对称化散度；真正被实例化并回传的是这一个 KL。fileciteturn25file0L4-L4

代码还定义了两个 EMA。参数 EMA 为

\[
\bar\theta_{t+1}=\beta_\theta \bar\theta_t + (1-\beta_\theta)\theta_t,
\]

并且是在 `training_step` 结束后更新；KL 标量的 EMA 为

\[
\bar D_{n+1}=\beta_D \bar D_n+(1-\beta_D)D_n,
\]

它在 `compute_loss` 内部、无梯度地更新。历史项 \(D_{n-1},D_{n-2}\) 也都被 `detach` 后缓存，因此**不存在跨代梯度链**。训练器真正加到总损失里的形式是

\[
L_{\text{total},t}
=
L_{\text{LM},t}
+
\alpha\,L_{\text{cont},n(t)}\cdot \mathbf 1\{t>0,\ t\bmod k=0\},
\quad k=\texttt{kl\_update\_every},
\]

所以大多数训练步根本没有 contradiction term，只有每 10 步一次的稀疏附加。fileciteturn6file0L103-L147 fileciteturn6file0L149-L165

### 当前默认实现与历史链条实现

按 `contradiction_loss.py` 当前默认值，generic 形式是

\[
L_{\text{cont}}^{\text{current}}
=
\lambda_1(\Delta D_n)^2
+
\lambda_2(D_n-\bar D_n)^2
+
\lambda_3 T_{2,n},
\]

其中 \(\Delta D_n=D_n-D_{n-1}\)，而 \(T_{2,n}\) 在当前默认分支里是 \(D_n^2/2\)；Volterra 历史和 \(\chi(k)=e^{-m_{\text{eff}}k}\) 只做 logging metric，不进 loss。当前默认参数是 \(\beta_\theta=0.999849\)、\(\beta_D=0.8090\)、\(\lambda_1=2.3585\)、\(\lambda_2=0.1060\)、\(\lambda_3=0.2120\)、`T_2_form="quadratic"`、`kl_history_K=9`。fileciteturn25file0L4-L4

但**历史 5/10–5/12 主链条不是这个东西**。`train_one_generation.py` 的旧 `CATConfig` 默认就是 `beta_model=0.999`、`beta_kl=0.9`、`\lambda_i=1`、`T_2_form="relu_dpp"`、`kl_history_K=1`、`m_eff=1.0`；`cat_arm_b.yaml` 也只显式给出旧 \(\beta,\lambda\) 而不提供新 dialectical 字段；`phase1_robust_chain.sh` 又明确把链条运行锁到 `configs/cat_arm_b.yaml`，并将 JSONL / master log 都按这条旧链打出。也就是说，历史主链条跑的是旧框架口径，不是新默认口径。fileciteturn19file0L42-L58 fileciteturn20file0L4-L4 fileciteturn26file0L71-L89

进一步，由于历史链条 \(K=1\)，`D_history` 最多保留一个过去值，于是二阶差分分支永远走不到 `len(D_history)>=2` 的情形。结果是 \(D''_n\equiv 0\)，`relu_dpp` 的第三项恒为零，历史链条实际 loss 精确退化为

\[
L_{\text{cont}}^{\text{chain-actual}}
=
(D_n-D_{n-1})^2
+
(D_n-\bar D_n)^2.
\]

这不是猜测，不是叙事润色，而是仓库内 code-first audit 明写出来并与链条日志绑定的结论。所谓“三项 higher-order / Volterra contradiction loss”在这条历史主链上并没有真正存在；真正存在的是一个**两项、标量、EMA-deviation 平滑器**。fileciteturn8file0L4-L4

### 真实存在的对象与纯叙事对象

| 类别 | 仓库中真实存在的数学对象 | 结论 |
|---|---|---|
| 训练内真实对象 | 当前 logits、EMA logits、标量 \(D_n=\mathrm{KL}(q_{\text{EMA}}\|p_{\text{current}})\)、`D_history`、标量 \(\bar D_n\)、参数 EMA、每 10 步一次的 \(L_{\text{LM}}+\alpha L_{\text{cont}}\) | 这些对象直接在代码里运作。fileciteturn25file0L4-L4 fileciteturn6file0L103-L147 |
| metric-only 对象 | `volterra_sum_K`、`GradNormMonitor`、`F1_var/F1_tail/F3_slice_gap` 这类高阶 eval 泛函 | 它们被记录、分析、分支裁决，但不是训练约束。fileciteturn25file0L4-L4 fileciteturn6file0L149-L165 fileciteturn13file0L7-L15 |
| 历史链条中不存在的对象 | 真正进入 optimizer 的 Volterra path term、跨代 chain rule 梯度、训练中的 high-order/reflexive gate、训练中的 slice-gap 向量场 | 这些要么只是注释/论文叙事，要么只在 post-hoc 分析里出现。fileciteturn8file0L4-L4 fileciteturn25file0L4-L4 |
| 必须视为叙事而非数学结果的对象 | first dialectical materialism / first reflexive AI / paradigm shift 之类 prestige claim | 仓库自己的纪律文件和状态文件都要求不复活。fileciteturn4file0L32-L37 fileciteturn2file0L23-L26 |

## 玻璃箱缺口

### 严格判据

如果一个方法要“打破玻璃箱”，至少要满足下面三个条件中的前两个，最好同时满足第三个：

\[
\text{更新不可约}:\quad
\nabla_\theta L_{\text{aux}}
\notin
\text{span}\{\nabla_\theta L_{\text{LM}},\ \nabla_\theta s(\theta)\}
\]

其中 \(s(\theta)\) 属于“单一标量代理类”，例如 mean log-prob、PPL 或其低阶差分；并且这个不可约性要在**未见 seed / 未见 run**上持续，而不是只在同一批伪复制里成立。换成更直白的话：它不能只是一个对单一标量的平滑、打表或装饰性惩罚；它必须对更新轨迹、表征轨迹或泛化行为施加一个**不可被单标量重写掉**的约束。当前仓库自己已经承认：独立于 PPL 的多类候选测度，不是塌回到 PPL/logit 兄弟量，就是落到 seed 噪声地板以下，或者被 decode 选项翻号；高阶线现阶段唯一剩下的是 F3 的弱例外，而且作者自己也要求把 cubic gate 降权、改用 LOSO。fileciteturn10file0L11-L15 fileciteturn9file0L26-L36

### 最小失败点

当前历史主链条的最小失败点只有一句话：**它对模型的约束被压缩成了一个标量 \(D_n\) 的瞬时平滑，而不是对分布结构的多分量约束。** 这件事有两个直接数学后果。

第一个后果是“稳态塌缩可逃逸”。设从某个 KL 更新开始，\(D_n\equiv D^\star\) 进入标量平台期。对历史链条实际 loss，

\[
L_{\text{cont},n}^{\text{chain-actual}}
=
(D_n-D_{n-1})^2 + (D_n-\bar D_n)^2.
\]

此时第一项立刻变成 0；第二项满足 \(E_n:=D^\star-\bar D_n=\beta_D E_{n-1}\)，因此几何收缩到 0。也就是说，**任何“标量 KL 已平台化”的状态——无论它对应健康、塌缩还是坏稳态——最终都会让历史 contradiction loss 消失。** 这说明历史链条 loss 不是 anti-collapse barrier，只是过渡态的 transient smoother。fileciteturn8file0L4-L4

第二个后果是“训练外指标不进更新”。`GradNormMonitor` 在 `training_step` 之后只是记录；高阶 F1/F3 脚本完全是 CPU fp32、固定真 eval blocks、禁触模型自生成的 post-hoc 测量。它们能当诊断器，不能被误写成已经进入训练的“自反性约束”。所以，如果你问现在的 MaoField 是否已经从 dashboard 变成了真正的 update law，答案是：**没有**。高阶指标最多是分析层的候选测量学；它们还没有转化成训练中的多分量约束。fileciteturn6file0L149-L165 fileciteturn13file0L7-L15

### 当前状态判定

因此，当前状态应判为：

- **历史主链条**：装饰性更强，属于“标量 KL 平滑器”，不是打破玻璃箱的训练机制。fileciteturn8file0L4-L4
- **当前默认实现**：比历史链条多了一个常驻的 \(D_n^2/2\) 项与 `K=9` metric logging，但本质上仍是对单标量 \(D_n\) 的作用；没有任何 fetched 证据表明它已经把不可约的分布结构写进更新律。fileciteturn25file0L4-L4
- **经验层结果**：\(\alpha=1\) confirmatory 三 endpoint 全 FALSE；所谓 decouple 安全垫 0/5 死；独立 collapse measure inventory 在仓库自己的 synthesis 中也被判成 PPL/noise/decode 的失败清单。凭这些证据，任何“现有方法已突破玻璃箱”的说法都应该判死。fileciteturn16file0L11-L42 fileciteturn11file0L11-L16 fileciteturn10file0L11-L15

## 零 GPU 数学推进

### T2 两分量 mixture 的充分性与反例

先给最硬的可证伪版本。

设两分量模型为

\[
p_\lambda = \lambda r + (1-\lambda)s,\qquad
q_{\bar\lambda}=\bar\lambda r + (1-\bar\lambda)s,
\]

并假设 \(r,s\) 支持不交、分量形状固定、所谓“collapse”只通过 mixture weight \(\lambda\) 改变。那么

\[
D(\bar\lambda,\lambda)
=
\mathrm{KL}(q_{\bar\lambda}\|p_\lambda)
=
\bar\lambda\log\frac{\bar\lambda}{\lambda}
+
(1-\bar\lambda)\log\frac{1-\bar\lambda}{1-\lambda},
\]

也就是一个 Bernoulli KL。于是有下面三个结论。

| 候选结论 | 必要假设 | 结论本身 | 证明草图 |
|---|---|---|---|
| 引理 | 支持不交；只变 mixture weight | 当前 scalar \(D_n\) 只看得到 mixture weight 偏离，不看得到分量内部发生了什么 | 把 KL 在两块支持上拆开，直接化成 Bernoulli KL |
| 推论 | 再加“小偏离” \(\delta=\lambda-\bar\lambda\) | \(D=\frac{\delta^2}{2\bar\lambda(1-\bar\lambda)}+O(\delta^3)\)，所以它一阶上只看“平方距离”，方向先天丢失 | 对 Bernoulli KL 在 \(\delta=0\) 泰勒展开 |
| 反例 | \(\bar\lambda=1/2\) | \(D(0.5,0.4)=D(0.5,0.6)\)。同一个 \(D\) 同时对应“向频繁分量塌”和“向稀有分量塌”两种相反机制 | 代入 Bernoulli KL 直接算即可 |

这意味着：**在最有利于它的两分量世界里，当前 scalar contradiction/deviation 指标充其量只对 mixture weight 的“偏离幅度”敏感，不对方向敏感，更不对分量内部结构敏感。** 所以它绝不可能单独充当 “mixture collapse 的充分判别器”。只有在“支持可辨、分量固定、只沿一维 mixture-weight 运动、并且你还知道当前在 \(\bar\lambda\) 哪一侧”这种强假设下，\(D_n\) 才对 \(\lambda_n\) 有单支可逆性。仓库的数学线文件其实已经把这个方向推进到 “F3 迟滞的两分量机制可能性证明”，并明确承认充分性半边目前没有 repo 内 code artifact 落地。fileciteturn9file0L20-L25

更致命的反例与当前历史链条直接相连：如果 \(\lambda_n\equiv \lambda^\star\) 已经卡在某个塌缩平台上，那么上节已经证明，历史两项 loss 会自动衰减到 0。于是即便两分量塌缩真实存在，当前链条 loss 也不会持续反对它。这个反例不需要 toy philosophy，只需要代码。fileciteturn8file0L4-L4

最小 Python 检查脚本草案如下：

```python
import math
import numpy as np

def bern_kl(q, p):
    return q * math.log(q / p) + (1 - q) * math.log((1 - q) / (1 - p))

# counterexample: same scalar D, opposite mechanism directions
q = 0.5
for p in [0.4, 0.6]:
    print(p, bern_kl(q, p))

# local quadratic approximation
q = 0.37
deltas = np.array([-0.05, -0.02, 0.02, 0.05])
for d in deltas:
    p = q + d
    exact = bern_kl(q, p)
    approx = d * d / (2 * q * (1 - q))
    print(d, exact, approx)

# stationary-collapse escape in chain-actual loss
beta_D = 0.9
D_star = 0.08
D_ema = 0.00
for n in range(10):
    loss = (D_star - D_ema) ** 2
    print(n, D_ema, loss)
    D_ema = beta_D * D_ema + (1 - beta_D) * D_star
```

### T3 线性差分 kill-test

仓库自己已经给出方向：最便宜的 kill-test 是在已有结果上跑线性差测度，修掉 broken cubic gate，并把 LOSO 当主 gate。`highorder_ppl_run.py` 的当前 gate A 只是把 \(F\) 和 `gen` 分别对 cubic(mean_lp) 残差化再做相关；gate B 则是把跨代信号和 5-seed 的 bootstrap 标准差上界比较。`MATH_LINE_VERDICT_20260619.md` 已经明确承认 cubic gate A broken，要求改成 LOSO-first。fileciteturn13file0L13-L15 fileciteturn13file0L44-L57 fileciteturn9file0L26-L36

我建议把 kill-test 写成下面这个完全零 GPU 的、足以杀死大部分“高阶/自反”叙事的版本。对每个目标指标 \(Y\in\{\text{F1\_var},\text{F1\_tail},\text{F3\_gap}\}\)，定义低阶基函数

\[
X_{\text{low}}
=
\left[
1,\,
m,\,
m^2,\,
m^3,\,
\Delta m,\,
|\Delta m|,\,
\Delta^2 m,\,
g,\,
g^2
\right],
\]

其中 \(m=\text{mean\_lp}_{s,g}\)，\(\Delta m=m_{s,g}-m_{s,g-1}\)，\(\Delta^2m=m_{s,g}-2m_{s,g-1}+m_{s,g-2}\)。如果有 JSONL 中的 `test_perplexity`、`val_perplexity`、`contradiction/D_n`、`contradiction/loss` 等字段，还可以把它们加入 \(X_{\text{low}}\)。然后做 leave-one-seed-out：

\[
\widehat f_{-s}=\arg\min_{f\in\mathcal F_{\text{lin}}}\sum_{s'\neq s}(Y_{s',g}-f(X_{s',g}))^2,
\qquad
R^2_{\text{LOSO}}(s)=1-\frac{\sum_g(Y_{s,g}-\widehat f_{-s}(X_{s,g}))^2}{\sum_g(Y_{s,g}-\bar Y_s)^2}.
\]

**杀死准则**可以写得很冷酷：

\[
\text{Kill}(Y)
\Longleftrightarrow
\operatorname{median}_s R^2_{\text{LOSO}}(s)\ge 0.9
\ \land\
\operatorname{median}_s M_\varepsilon(s)\approx \tfrac12,
\]

其中 \(M_\varepsilon(s)\) 是 matched-mean pair test：在 holdout seed 内，挑出 \(|m_i-m_j|<\varepsilon\) 的成对点，检查 \((Y_i-Y_j)\) 是否仍和 \((g_i-g_j)\) 有稳定方向。如果这个 matched-mean 方向性消失，那么“高阶/自反”指标就只是 mean、低阶差分、loss scale 或方差的改写；故事应立即判死。这个检验与仓库中现有的 `highorder_2ndchannel_check.py` 是同向的：那份脚本已经从零重写了“纯 mean-lp null 校准”“flexible residualization”“matched-mean pairs”“LOSO-CV 比较”，本质上就是对当前 gate 的严厉升级版。fileciteturn15file0L4-L4

最小 Python 草案：

```python
import json
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score

rows = json.load(open("highorder_result.json"))["rows"]

def lag(arr, k, fill=np.nan):
    out = np.full_like(arr, fill, dtype=float)
    out[k:] = arr[:-k]
    return out

# flatten rows
seed = np.array([r["seed"] for r in rows], dtype=int)
gen  = np.array([r["gen"] for r in rows], dtype=int)
m    = np.array([r["mean_lp"] for r in rows], dtype=float)

order = np.lexsort((gen, seed))
seed, gen, m = seed[order], gen[order], m[order]

# per-seed low-order differences
dm = np.full_like(m, np.nan)
d2m = np.full_like(m, np.nan)
for s in np.unique(seed):
    idx = np.where(seed == s)[0]
    dm[idx[1:]] = m[idx[1:]] - m[idx[:-1]]
    d2m[idx[2:]] = m[idx[2:]] - 2 * m[idx[1:-1]] + m[idx[:-2]]

def design(mask):
    X = np.column_stack([
        np.ones(mask.sum()),
        m[mask], m[mask]**2, m[mask]**3,
        np.nan_to_num(dm[mask], nan=0.0),
        np.nan_to_num(np.abs(dm[mask]), nan=0.0),
        np.nan_to_num(d2m[mask], nan=0.0),
        gen[mask], gen[mask]**2,
    ])
    return X

for key in ["F1_var", "F1_tail", "F3_slice_gap"]:
    y = np.array([r[key] for r in rows], dtype=float)[order]
    scores = []
    for s in np.unique(seed):
        tr = seed != s
        te = seed == s
        model = Ridge(alpha=1e-6).fit(design(tr), y[tr])
        pred = model.predict(design(te))
        scores.append(r2_score(y[te], pred))
    print(key, "median_LOSO_R2 =", np.median(scores))
```

### LOSO-first 替代 high-order gate

我建议直接把现有 high-order gate 换成下面这个定义，而不是继续修补 cubic gate A。

设 \(Y\) 是待检验指标，\(m\) 是 mean log-prob，\(\mathcal F_{\text{low}}\) 是所有“只允许使用 mean、低阶差分与尺度变量”的低阶模型类。定义

\[
T_{\text{LOSO}}(Y)
=
\operatorname{median}_{s}
\Bigl[
R^2_{\text{holdout }s}(Y;\,\mathcal F_{\text{low}}+\{g,g^2\})
-
R^2_{\text{holdout }s}(Y;\,\mathcal F_{\text{low}})
\Bigr].
\]

再定义 matched-mean 方向统计量

\[
M_\varepsilon(Y)
=
\operatorname{median}_{s}
\left[
\frac{1}{N_s(\varepsilon)}
\sum_{|m_i-m_j|<\varepsilon}
\mathbf 1\!\left((Y_i-Y_j)(g_i-g_j)>0\right)
\right].
\]

主 gate 只接受

\[
T_{\text{LOSO}}(Y)>\tau
\quad\text{且}\quad
M_\varepsilon(Y)>\frac12+\delta
\]

并要求至少 \(4/5\) holdout seeds 同号。这样做比当前 high-order gate 强得多，原因非常简单：当前 gate A/B 都在**同一批 seeds 上反复看曲线**，容易被 pseudo-replication、U-shape 曲率与 mean-lp/gen 共线性骗过去；LOSO 则问的是“你离开这颗 seed 以后还站得住吗”。仓库自己的数学线 verdict 已经等于承认这一点。fileciteturn13file0L13-L15 fileciteturn9file0L26-L36

### 面向玻璃箱的候选新工具

仓库当前最接近“非标量结构”的东西，是 F3 的 freq/rare slice gap：在固定真 eval blocks 上，`highorder_ppl_run.py` 把 target token 按 g0 频率 top/bottom 20% 切片，分别计算两组 mean log-prob，并取 gap；`highorder_verify_hysteresis.py` 又把 gen1 与 gen4 的近同 mean、异 gap 作为 decisive check。也就是说，**仓库自己已经给出了一个从纯标量走向向量化观测的接口，只是还没把它写进训练。** fileciteturn13file0L9-L15 fileciteturn14file0L16-L30

基于这一点，我给出三件可以直接数学化、并且可证伪的“专有工具”提案：

| 工具 | 定义 | 它解决什么 | 如何被证伪 |
|---|---|---|---|
| **切片矛盾场** | 把标量 \(D_n\) 升成向量 \(\mathbf D_n=(D_n^{(1)},\dots,D_n^{(m)})\)，每个分量是一个固定 token slice 的 groupwise KL 或 true-token loss | 打破单一标量 \(D_n\) 的不可辨识性 | 若投影到去均值子空间后稳健秩仍为 1，则失败 |
| **标量零空间投影器** | \(P_\perp=I-\frac{11^\top}{m}\)，训练只惩罚 \(P_\perp(\mathbf D_n-\bar{\mathbf D}_n)\) 与 \(P_\perp \Delta \mathbf D_n\) | 明确剔除“全局 mean-PPL 模式”，只打击正交 residual | 若 projected signal 在 LOSO 中消失，则只是 mean mode 假余量 |
| **分支判别量** | \(B_n=\operatorname{sign}(D_n^{\text{freq}}-D_n^{\text{rare}})\) 或同类 slice-gap 方向量 | 解决当前 Bernoulli-KL 只看幅度不看方向的问题 | 若 matched-mean pair 上方向统计量回到 1/2，则失败 |

如果要把 MaoField 真正推进到“不是玻璃箱”，我认为**唯一靠谱的短路径**就是把训练约束从 scalar \(D_n\) 升格成一个去除 mean mode 的向量场，再用 LOSO 去问这个向量 residual 是否跨 seed 站得住。否则再漂亮的 dialectical 说法也只是哲学补叙事。这个判断不是反哲学，而是反偷换。它正好回应了仓库里“真正的难题是玻璃箱”的隐含数学对立面：**不是没有现象，而是现象被标量化后失去机制辨识力。** 这件事只能靠秩、投影、可逆性与跨 seed 泛化来解决。fileciteturn10file0L11-L15 fileciteturn9file0L33-L37

## 可执行研究交接

### 成立

| 数学事实 | 结论 | 证据 |
|---|---|---|
| 操作性散度 | 训练中真正实例化的是 \(\mathrm{KL}(q_{\text{EMA}}\|p_{\text{current}})\)，梯度只穿过当前模型 | fileciteturn25file0L4-L4 |
| 历史主链 loss 形态 | 5/10–5/12 主链条实际 loss 退化成两项：\((D_n-D_{n-1})^2+(D_n-\bar D_n)^2\) | fileciteturn8file0L4-L4 |
| 稀疏注入 | contradiction loss 只在每 10 个 train step 注入一次，其余步是纯 LM loss | fileciteturn6file0L103-L147 |
| metric-only 身份 | `GradNormMonitor`、Volterra accumulator、高阶 F1/F3 都是 post-hoc/metric 层，不是训练约束 | fileciteturn6file0L149-L165 fileciteturn25file0L4-L4 fileciteturn13file0L7-L15 |
| α=1 confirmatory | 三个 locked endpoint 全 FALSE，gate 停在 E1 | fileciteturn16file0L11-L42 |
| decouple 线 | 预注册 decouple criterion 忠实复算 0/5，不成立 | fileciteturn11file0L11-L16 |
| C meta-pattern | 仓库当前最强 synthesis 是：独立于 PPL 的候选 collapse measures 多数塌回 PPL/noise/decode | fileciteturn10file0L11-L15 |
| F3 弱余量 | 在固定真 eval 上，仓库里确实存在“近同 mean、异 gap”的 F3 观察，但仅是弱例外，不是已成方法贡献 | fileciteturn14file0L16-L30 fileciteturn9file0L20-L29 |

### 不成立或应撤回

| 命题 | 判定 | 证据 |
|---|---|---|
| “主链条实际训练的是三项 higher-order / Volterra contradiction loss” | 不成立 | fileciteturn8file0L4-L4 |
| “跨代 chain rule / Volterra path 已经进 optimizer” | 不成立 | fileciteturn25file0L4-L4 |
| “α=1 contradiction loss 带来 confirmatory 正面结果” | 不成立 | fileciteturn16file0L11-L42 |
| “distinct-n 与 PPL 恢复解耦，形成独立 novelty 安全垫” | 不成立，应撤回 | fileciteturn11file0L11-L16 |
| “所有 collapse 都只是 mean-PPL” | 过强，应撤回 | fileciteturn10file0L13-L15 fileciteturn14file0L16-L30 |
| first-DM / first-reflexive-AI / paradigm-shift 类 claim | 不应复活 | fileciteturn4file0L32-L37 |

### 可推进

| 零 GPU 任务 | 产出形式 | 为什么现在就能做 |
|---|---|---|
| 两分量 mixture 反例与局部可逆性证明 | 一个 lemma、一个 counterexample、一个 30 行 sympy/numpy 脚本 | 仓库数学线已经把方向推到 “T2 弱真 + 充分性半边待补”；无需新实验 | fileciteturn9file0L20-L25 |
| F3 的 LOSO-first kill-test | 一个 holdout-seed 表、matched-mean 对照表、kill/ survive 判定 | `highorder_result.json` 已落盘，仓库也已承认现 gate 要改 LOSO | fileciteturn9file0L26-L36 fileciteturn15file0L4-L4 |
| 线性差分 kill-test | 一个 baseline family 与 LOSO-R² 表 | `highorder_result.json` 已含每 seed×gen 的 mean_lp/F1/F3 行数据 | fileciteturn12file0L4-L4 |
| 历史链条“平台逃逸”证明 | 一个短 lemma + 数值示例 | 纯由当前代码可导出 | fileciteturn8file0L4-L4 |
| distinct-2 再核验 | 一个 collinearity / decode-confound 复算脚本 | 仓库已有 `verify_gate5_distinct2_collinear.py` 方向 | fileciteturn23file0L5-L23 |

### 必须新增实验

| 命题 | 为什么现有证据不够 | 需要什么新增实验 |
|---|---|---|
| 当前 default `quadratic + K=9` 版本是否真的优于历史两项链条 | 现有主 verdict 针对的是旧链条；没有锁定对比实验 | 同条件、同 seed、只换 auxiliary law 的 confirmatory 对照 |
| 向量化 slice-resolved contradiction field 是否能真正改变训练轨迹 | 仓库当前没有把 F3/slice-gap 写进训练，只是分析 | 一次最小新训练：标量 loss vs 去均值向量 loss |
| “真系统高维 wedge” 是否存活 | T1 只把标量玩具层的强静态形式证伪了，高维 operator 版本仍 open | 至少 2 维可控线性系统或小模型实验 |
| F3 是否脱离 gen0-reset / real-prompt channel 仍存活 | 当前 arm B 仍有 real prompt 与 gen0 reset 通道 | 去掉这些 channel 的新实验或 2×2 ablation |

## 严格结论

MaoField 当前最强、最诚实的数学命题，不是“自反 AI”、不是“first dialectical materialism”，甚至也不是“高阶矛盾损失已被实现”。**它最强的命题是一个负命题加一个代码命题：历史主链条实际只实现了两项、标量、瞬态的 EMA-deviation KL 正则；而在仓库已完成的多轮检验里，候选的独立 collapse measure 大多塌回 PPL/noise/decode confound，\(\alpha=1\) confirmatory 与 decouple 线都死了，只剩一个需要 LOSO 再审判的 F3 弱例外。** 这才是现在最硬、也最不丢人的说法。fileciteturn8file0L4-L4 fileciteturn16file0L11-L42 fileciteturn11file0L11-L16 fileciteturn10file0L11-L15

通往“打破玻璃箱”的最短路径也很清楚：**先别再包装当前标量 \(D_n\)**。先用零 GPU 把 F3 弱余量用 LOSO-first + matched-mean pair test 判成死或活；如果它死，MaoField 作为“独立测度”故事就应彻底收缩成干净 negative / methodology note；如果它活，再把这个 slice-resolved 结构写进训练，构造一个去掉 global mean mode 的向量矛盾场。没有这一步，所谓 glass-box breakthrough 只是在摘要里存在。fileciteturn9file0L33-L37 fileciteturn14file0L16-L30

最可能一刀杀死整个故事的单一检验，就是 **F3 的 LOSO 线性差分 kill-test**。原因非常直接：仓库当前所有其他正面口都已经死了，F3 是唯一还被保留为“弱真例外”的东西；一旦它在 holdout seed 上被 mean、低阶差分和 matched-mean null 吃掉，MaoField 就只剩“独立测度普遍失败”的 negative empirical note，再没有“玻璃箱有裂缝”的余量。fileciteturn9file0L26-L36 fileciteturn10file0L13-L15

最可能把它从经验观察推进到可发表数学/方法贡献的单一检验，是 **F3 在 LOSO 与 matched-mean 双检下仍稳定存活**。如果这件事成立，那么你至少能发表一个干净的 measurement lemma：在固定真评测集上，mean-PPL 不是充分统计量，freq/rare slice-gap 提供一个跨 seed 的正交残差；进一步的 method 才有资格进入下一步——把这种向量 residual 写进训练约束。若这一步不成立，就别谈方法创新；若成立，也先只能谈 measurement contribution，不能直接膨胀成 paradigm story。fileciteturn14file0L16-L30 fileciteturn15file0L4-L4

最后一句，按严格数学教授口径：**MaoField 现在还没有打破玻璃箱。它目前做出的最可靠工作，是把自己许多更大的说法杀掉。** 这不是失败；但如果再把这件事包装成已经实现的 higher-order reflexive method，那就是失败。