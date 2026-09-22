"""Offline only: exact algebra and retained-record reanalysis. No model calls."""
from pathlib import Path
import argparse,subprocess,sys,json,hashlib
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
commands=[('math',[sys.executable,str(R/'math/exact_checks.py'),'--out',str(a.out/'math.json')]),('records',[sys.executable,str(R/'experiment/audit_shareable.py'),'--source',str(R/'experiment/raw'),'--out',str(a.out/'records')])]
commands.append(('hclose_math',[sys.executable,str(R/'experiment/math_checks.py'),'--out',str(a.out/'hclose_math.json')]))
commands.append(('successor',[sys.executable,str(R/'successor/audit_successor.py'),'--inputs',str(R/'successor/inputs'),'--out',str(a.out/'successor')]))
results=[]
for name,cmd in commands:
 q=subprocess.run(cmd,capture_output=True)
 (a.out/(name+'.stdout')).write_bytes(q.stdout);(a.out/(name+'.stderr')).write_bytes(q.stderr)
 results.append({'step':name,'returncode':q.returncode})
 if q.returncode:raise SystemExit(q.returncode)
(a.out/'STATUS.json').write_text(json.dumps({'kind':'DETERMINISTIC_REPRODUCTION_NOT_NEW_SAMPLING','steps':results,'new_model_calls':0,'new_Lean_compilations':0},indent=2)+'\n')
print(json.dumps(results,indent=2))
