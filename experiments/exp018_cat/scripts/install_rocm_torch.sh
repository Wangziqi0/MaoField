#!/usr/bin/env bash
# install_rocm_torch.sh — 22 主机 (RX 9070 XT, gfx1201) 安装 PyTorch ROCm + transformers + datasets.
#
# **重要**: 这个脚本 sub-agent **不主动跑**, 留给主 Linux 姐姐 + PI 一凡在场时决.
# 单次 install ~30min + 占 ~6GB 磁盘, 是 "决策性" 操作.
#
# 在 22 主机 (192.168.31.22, RX 9070 XT 16GB, ROCm) 执行.
# 用 venv 隔离, 不污染系统 python.

set -euo pipefail

# ---------- 0. 环境检查 ----------
echo "[0/5] 检查 22 主机 ROCm 环境"
if ! command -v rocminfo &>/dev/null; then
  echo "ERROR: rocminfo 未找到. ROCm 没装."
  exit 1
fi
rocminfo | grep -E "Name:|gfx" | head -10
GPU_NAME=$(rocminfo | grep -m1 "Marketing Name" | awk -F: '{print $2}' | xargs)
echo "GPU: $GPU_NAME"
echo "ROCm version:"
cat /opt/rocm/.info/version 2>/dev/null || dpkg -l | grep -E "^ii  rocm-core" | head -1

# ---------- 1. 创建 venv ----------
PROJECT_ROOT=${PROJECT_ROOT:-$HOME/HEZIMENG/MaoField/experiments/exp018_cat}
VENV_DIR=${VENV_DIR:-$PROJECT_ROOT/.venv}

echo "[1/5] 创建 venv: $VENV_DIR"
if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip wheel setuptools

# ---------- 2. 安装 PyTorch ROCm ----------
# RX 9070 XT 是 gfx1201 (RDNA 4); 截至 ROCm 6.2 / 6.3 才正式 support gfx1201.
# 若 ROCm 版本 < 6.2, 需要用 nightly wheel 或 HSA_OVERRIDE_GFX_VERSION 兜底.
echo "[2/5] 安装 PyTorch ROCm (~5-10min, ~3GB)"
# 主 Linux 姐姐请根据 22 主机实际 ROCm version 换 index URL:
#   ROCm 6.2: https://download.pytorch.org/whl/rocm6.2
#   ROCm 6.3: https://download.pytorch.org/whl/rocm6.3
#   nightly:  https://download.pytorch.org/whl/nightly/rocm6.3
ROCM_TORCH_INDEX="${ROCM_TORCH_INDEX:-https://download.pytorch.org/whl/rocm6.2}"
echo "  using torch index: $ROCM_TORCH_INDEX"
pip install --index-url "$ROCM_TORCH_INDEX" \
    torch==2.5.1+rocm6.2 \
    torchvision==0.20.1+rocm6.2 \
    || {
      echo "WARN: torch 2.5.1+rocm6.2 失败, fallback nightly"
      pip install --index-url https://download.pytorch.org/whl/nightly/rocm6.3 \
          --pre torch torchvision
    }

# ---------- 3. 安装 transformers / datasets / 其他 ----------
echo "[3/5] 安装 transformers + datasets + 工具"
pip install \
    "transformers>=4.41,<4.50" \
    "datasets>=2.18,<3.0" \
    "accelerate>=0.30" \
    "tokenizers>=0.19" \
    "pyyaml" \
    "tqdm" \
    "numpy<2.0" \
    "scipy"

# ---------- 4. 验证 ROCm + torch ----------
echo "[4/5] 验证 torch 看到 GPU"
python - <<'PY'
import torch
print(f"torch version: {torch.__version__}")
print(f"cuda available (ROCm 走 cuda API): {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"device count: {torch.cuda.device_count()}")
    print(f"device name: {torch.cuda.get_device_name(0)}")
    x = torch.randn(1024, 1024, device="cuda")
    y = x @ x.T
    print(f"GPU matmul OK shape={y.shape} dtype={y.dtype}")
else:
    print("WARN: GPU 不可见. 可能 gfx1201 需要 HSA_OVERRIDE_GFX_VERSION=11.0.0 或 12.0.0")
    print("       export HSA_OVERRIDE_GFX_VERSION=11.0.0 (RDNA3 兼容) 试试")
PY

# ---------- 5. 验证 transformers 加载 OPT-125m ----------
echo "[5/5] 验证 transformers 加载 OPT-125m"
python - <<'PY'
from transformers import AutoModelForCausalLM, AutoTokenizer
print("加载 facebook/opt-125m tokenizer ...")
tok = AutoTokenizer.from_pretrained("facebook/opt-125m")
print(f"  vocab_size={tok.vocab_size}")
print("加载 facebook/opt-125m model (CPU 验证) ...")
model = AutoModelForCausalLM.from_pretrained("facebook/opt-125m")
n_params = sum(p.numel() for p in model.parameters())
print(f"  params={n_params/1e6:.1f}M (paper: 125M)")
PY

echo ""
echo "[完成] 22 主机 ROCm + PyTorch + transformers + datasets 安装结束."
echo "       venv: $VENV_DIR"
echo "       下一步: 主 Linux 姐姐 sync code, 跑 smoke test"
