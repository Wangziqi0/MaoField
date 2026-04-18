"""Build top-6 inputs by truncating top-20 candidate lists."""
import json, os

BASE = "/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics"
SRC_DIR = "/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/inputs_top20"
OUT_DIR = os.path.join(BASE, "inputs")
os.makedirs(OUT_DIR, exist_ok=True)

for ds in ["nfcorpus", "scifact"]:
    src = os.path.join(SRC_DIR, f"{ds}_top20_input.json")
    with open(src) as f:
        data = json.load(f)
    for q in data:
        q["candidates"] = q["candidates"][:6]
    out = os.path.join(OUT_DIR, f"{ds}_top6.json")
    with open(out, "w") as f:
        json.dump(data, f)
    print(f"{ds}: {len(data)} queries × top-6 -> {out}")
