#!/usr/bin/env python3
from pathlib import Path
import csv, json, hashlib, subprocess, sys
REPO=Path(__file__).resolve().parents[2]
SD=REPO/'data'/'processed'/'source_data'
OUT=REPO/'outputs'; OUT.mkdir(exist_ok=True)

def read_csv(name):
    with (SD/name).open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))

checks=[]
# Phase 23 fixed values
eq=read_csv('Phase23_Exact_Equality.csv')
checks.append({'id':'PH23_EXACT_EQUALITY_ROWS','pass':len(eq)>0 and all(float(r['estimate'])==0 for r in eq)})
ctrl=read_csv('Phase23_Ordinary_Controls.csv')
checks.append({'id':'PH23_ORDINARY_0_OF_16','pass':len(ctrl)==6 and all(int(r['ordinary_successes'])==0 and int(r['ordinary_n'])==16 for r in ctrl)})
gap=read_csv('Phase23_Qwen_Channel_Gap.csv')
vals={r['stratum']:float(r['A_SIB_minus_R']) for r in gap}
checks.append({'id':'PH23_QWEN_GAP','pass':abs(vals.get('main48',99)+0.9792)<1e-8 and abs(vals.get('sealed16',99)+1.0)<1e-8})
# GLM controls and terminal claims
ordr=read_csv('GLM_Ordinary_Criteria.csv'); expected={'P':30,'ORDERED_O':23,'A_FT':26,'U':25}
checks.append({'id':'GLM_ORDINARY','pass':all(any(r['endpoint']==k and int(r['successes'])==v for r in ordr) for k,v in expected.items())})
formal=json.load(open(REPO/'data/processed/results/GLM53_FORMAL_RESULT.json'))
checks.append({'id':'GLM_CLAIMS_FALSE','pass':all(formal['claims'].get(k) is False for k in ['P1','P2','P3','P5','BOUNDED_ZERO'])})
# Generate figures.
subprocess.run([sys.executable,str(REPO/'src/figures/build_figures_base.py')],check=True)
subprocess.run([sys.executable,str(REPO/'src/figures/build_figure1_v3.py')],check=True)
subprocess.run([sys.executable,str(REPO/'src/figures/build_figure5_r1.py')],check=True)
summary={'schema':'maofield.offline_reproduction.v1','checks':checks,'all_pass':all(x['pass'] for x in checks),'provider_calls':0,'model_calls':0}
(OUT/'OFFLINE_REPRODUCTION_RECEIPT.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
if not summary['all_pass']:
    raise SystemExit('OFFLINE REPRODUCTION CHECK FAILED')
print(json.dumps(summary,indent=2))
