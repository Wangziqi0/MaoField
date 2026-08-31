#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'MANIFEST.sha256'
failed=[]
for line in manifest.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    h,rel=line.split('  ',1); p=ROOT/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h: failed.append(rel)
if failed:
    print('FAIL',failed); raise SystemExit(2)
print('PASS',len(manifest.read_text().splitlines()),'files')
