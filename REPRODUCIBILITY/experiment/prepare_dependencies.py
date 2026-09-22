"""Explicit, opt-in source fetch at the supplied Lake lock. No model calls.
Run only in a reviewed preparation environment, not the experiment container.
"""
from pathlib import Path
import argparse,json,subprocess,sys
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path,required=True);p.add_argument('--fetch',action='store_true');p.add_argument('--allow-network',action='store_true');a=p.parse_args()
lock=json.loads((a.project/'lake-manifest.json').read_text());rows=[]
if a.fetch and not a.allow_network:raise SystemExit('Explicit --allow-network is required for dependency fetch')
logdir=a.project/'dependency_preparation';logdir.mkdir(exist_ok=True)
for q in lock['packages']:
 root=a.project/'.lake/packages'/q['name']
 if a.fetch and not root.exists():
  root.parent.mkdir(parents=True,exist_ok=True)
  commands=[['git','init',str(root)],['git','-C',str(root),'remote','add','origin',q['url']],['git','-C',str(root),'fetch','--depth','1','origin',q['rev']],['git','-C',str(root),'checkout','--detach',q['rev']]]
  for i,cmd in enumerate(commands):
   r=subprocess.run(cmd,capture_output=True);(logdir/f'{q["name"]}_{i}.stdout').write_bytes(r.stdout);(logdir/f'{q["name"]}_{i}.stderr').write_bytes(r.stderr)
   if r.returncode:raise SystemExit('Dependency source fetch failed; see logs: '+q['name'])
 r=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True)
 actual=r.stdout.strip() if r.returncode==0 else None
 rows.append({'name':q['name'],'url':q['url'],'expected_commit':q['rev'],'actual_commit':actual,'matches':actual==q['rev'],'build_cache_present':(root/'.lake/build').exists()})
(logdir/'SOURCE_STATUS.json').write_text(json.dumps({'source_checks':rows,'network_requested':a.fetch,'new_model_calls':0},indent=2)+'\n')
print(json.dumps(rows,indent=2))
if a.fetch and not all(r['matches'] for r in rows):raise SystemExit(2)
