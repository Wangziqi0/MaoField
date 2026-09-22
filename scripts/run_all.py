"""Deterministic offline reproduction from immutable raw data. No model endpoint."""
from pathlib import Path
import sys,json,hashlib,subprocess,zipfile,datetime,shutil
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 mode=sys.argv[1];out=R/'WORK'/('run_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'));out.mkdir(parents=True)
 status={'kind':'DETERMINISTIC_RAW_RECORD_AND_MATH_REPRODUCTION','new_model_calls':0,'independent_kernel':'NOT_RUN','steps':[],'status':'RUNNING'}
 def save(): (out/'STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
 def run(name,args):
  with (out/(name+'.stdout')).open('wb') as so,(out/(name+'.stderr')).open('wb') as se:
   p=subprocess.run([sys.executable,*map(str,args)],stdout=so,stderr=se)
  status['steps'].append({'name':name,'returncode':p.returncode});save()
  print(name, 'PASS' if p.returncode==0 else 'FAIL',flush=True)
  if p.returncode:raise RuntimeError(f'{name}: see {out}')
 try:
  raw=out/'raw';raw.mkdir()
  for f in json.loads((R/'data/raw/MANIFEST.json').read_text()):
   p=R/'data/raw'/f['path']
   if 'parts' in f:
    p=out/f['path']
    with p.open('wb') as joined:
     for part in f['parts']:
      q=R/'data/raw'/part['path'];assert sha(q)==part['sha256']
      with q.open('rb') as src:shutil.copyfileobj(src,joined)
   assert sha(p)==f['sha256']
   with zipfile.ZipFile(p) as z:
    for member in z.infolist():
     dest=(raw/member.filename).resolve();assert dest.is_relative_to(raw.resolve())
     assert (member.external_attr>>16)&0o170000 != 0o120000
    z.extractall(raw)
  run('math_and_mapped_records',[R/'REPRODUCIBILITY/reproduce.py','--out',out/'mapped'])
  run('raw_hclose',[R/'REPRODUCIBILITY/experiment/audit_hclose.py','--source',raw/'HCLOSE','--out',out/'raw_hclose'])
  run('raw_successor',[R/'REPRODUCIBILITY/successor/audit_successor.py','--raw-root',raw/'SUCCESSOR','--inputs',out/'exported_successor','--out',out/'raw_successor'])
  for name in ['cohort_status.json','inheritance.json','main_contrasts.json','version_identity.json','selected_witnesses.json','symbolic_successor.json']:
   assert (out/'raw_successor'/name).read_bytes()==(out/'mapped/successor'/name).read_bytes(),name
  run('source_assembly',[R/'REPRODUCIBILITY/experiment/assemble_lean.py','--raw',raw/'HCLOSE','--out',out/'source_assembly'])
  if mode=='--full':
   env=R/'WORK/environment'
   # Check that the packaged common cache belongs to the fresh raw-source assembly.
   for x in json.loads((out/'source_assembly/ASSEMBLY_RECEIPT.json').read_text())['files']:
    target=env/'lean_project'/x['assembled_path']
    if target.exists():assert sha(target)==x['sha256']
    else:assert target.suffix not in ('.lean','.toml') and target.name!='lean-toolchain', x['assembled_path']
   run('ordinary_lean_replay',[R/'REPRODUCIBILITY/experiment/replay_bwrap.py','--project',env/'lean_project','--toolchain',env/'lean-4.34.0-rc2-linux','--out',out/'lean'])
   s=json.loads((out/'lean/STATUS.json').read_text());expected={'history_1.lean':'ORDINARY_LEAN_CANDIDATE_REJECTED','history_2.lean':'ORDINARY_LEAN_CANDIDATE_REJECTED','history_3.lean':'ORDINARY_LEAN_REPLAY_ACCEPTED','standard_1.lean':'ORDINARY_LEAN_CANDIDATE_REJECTED','standard_2.lean':'ORDINARY_LEAN_CANDIDATE_REJECTED'}
   assert {x['candidate_name']:x['replay_status'] for x in s['results']}==expected
   status['new_Lean_compilations']=5
  else:status['new_Lean_compilations']=0;status['lean']='NOT_RUN_ANALYSIS_ONLY'
  status['status']='PASS'
 except Exception as e:
  status['status']='FAIL';status['error']=str(e);raise
 finally:save();print('Report:',out,flush=True)
if __name__=='__main__':main()
