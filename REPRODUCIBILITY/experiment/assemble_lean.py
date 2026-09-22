"""Assemble the exact preserved hclose project. Offline; no Lean/model execution.

The source workspace is a documented, modified slice of the pinned NS repository.
It must not be overwritten with the full original solution tree.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil
from pathlib import Path

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write_json(p: Path, value) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+'\n')

def default_raw() -> Path:
    root=Path(__file__).resolve().parents[2]
    for p in (root/'INTERNAL/RAW_HCLOSE', Path(__file__).resolve().parent/'raw'):
        if p.is_dir(): return p
    raise FileNotFoundError('Supply --raw with the preserved source-mapped record tree')

def verify_raw(raw: Path) -> dict:
    mf=raw/'PACKAGE_MANIFEST.json'
    if not mf.exists(): mf=raw/'SHAREABLE_MANIFEST.json'
    if not mf.exists(): raise FileNotFoundError('Input manifest missing')
    m=json.loads(mf.read_text())
    checked=0
    for row in m['files']:
        rel=Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts: raise ValueError('Unsafe manifest path')
        p=raw/rel
        if p.is_symlink() or not p.is_file(): raise ValueError('Non-regular source: '+str(rel))
        if sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:
            raise ValueError('Source identity mismatch: '+str(rel))
        checked+=1
    return {'manifest':mf.name,'manifest_sha256':sha(mf),'verified_files':checked}

def candidates(raw: Path) -> list[dict]:
    """Derive request numbers by exact visible-body matching, not filename ordinal."""
    result=[]
    for arm in ('history','standard'):
        root=raw/'10_CURRENT_RUN'/arm
        requests={}
        for p in sorted((root/'requests').glob('[0-9][0-9][0-9][0-9]')):
            body=p/'visible.utf8'
            if body.is_file() and body.stat().st_size:
                requests.setdefault(sha(body), []).append(int(p.name)+1)
        for ordinal, sub in enumerate(sorted((root/'submissions').iterdir()),1):
            if not sub.is_dir(): continue
            body=sub/'body.lean.txt'; candidate=sub/'candidate.lean'
            match=requests.get(sha(body),[])
            if len(match)!=1: raise ValueError('Candidate/request match is not unique')
            receipt=json.loads((sub/'RESULT.json').read_text())
            if receipt['candidate_sha256']!=sha(candidate): raise ValueError('Candidate hash mismatch')
            result.append({'condition_original_label':arm.upper(),
                'visible_candidate_ordinal':ordinal,'original_request_number':match[0],
                'request_directory':f'10_CURRENT_RUN/{arm}/requests/{match[0]-1:04d}',
                'candidate_name':f'{arm}_{ordinal}.lean',
                'source':str(candidate.relative_to(raw)), 'sha256':sha(candidate),
                'body_sha256':sha(body),'original_result_status_raw':receipt['status'],
                'historical_compiler_returncode':json.loads((sub/'compile/receipt.json').read_text()).get('returncode'),
                'historical_observed_outcome':('ACCEPTED' if json.loads((sub/'compile/receipt.json').read_text()).get('returncode')==0 else 'CANDIDATE_REJECTED_BY_SAVED_COMPILER')})
    if len(result)!=5: raise ValueError('Expected five preserved candidates, not six requests')
    return result

def assemble(raw: Path, out: Path) -> dict:
    raw=raw.resolve(); out=out.resolve()
    if out.exists(): raise FileExistsError('Assembly output must be a new directory')
    verification=verify_raw(raw)
    rows=candidates(raw)
    w=raw/'10_CURRENT_RUN/history/workspace'; pub=raw/'10_CURRENT_RUN/history/public'
    out.mkdir(parents=True)
    mapping=[]
    for origin, tree in [('workspace',w),('public',pub)]:
        for src in sorted(tree.rglob('*')):
            if src.is_symlink(): raise ValueError('Symlink source is not supported')
            if not src.is_file(): continue
            rel=src.relative_to(tree)
            if any(s in ('.git','.lake') for s in rel.parts): raise ValueError('Cache must not be in source tree')
            if str(rel)=='Branch/Direct.lean': continue # historical terminal is not a common input
            dest=out/rel
            if dest.exists() and sha(dest)!=sha(src): raise ValueError('Workspace/public collision: '+str(rel))
            dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dest)
            mapping.append({'assembled_path':str(rel),'source':str(src.relative_to(raw)),
                            'origin':origin,'sha256':sha(src),'bytes':src.stat().st_size})
    for rel in ('Checkpoint/NodeGoal.lean','lakefile.toml','lake-manifest.json','lean-toolchain','LICENSE'):
        if not (out/rel).is_file(): raise ValueError('Assembly missing '+rel)
    imports=[];missing=[]
    for f in sorted(out.rglob('*.lean')):
        for name in re.findall(r'^\s*import\s+([A-Za-z0-9_.]+)',f.read_text(),re.M):
            imports.append(name)
            if name.startswith(('NavierStokes.','Checkpoint.','GoalSpec')):
                if not (out/Path(*name.split('.'))).with_suffix('.lean').exists():missing.append(name)
    if missing: raise ValueError('Unresolved local imports: '+repr(sorted(set(missing))))
    croot=out/'saved_candidates'; croot.mkdir()
    for row in rows: shutil.copyfile(raw/row['source'],croot/row['candidate_name'])
    write_json(out/'candidate_manifest.json',rows)
    write_json(out/'request_to_candidate.json',[
        {'condition_original_label':arm,'original_request_number':n,
         'candidate_name':next((r['candidate_name'] for r in rows if r['condition_original_label']==arm and r['original_request_number']==n),None),
         'no_candidate_reason':'TRUNCATED_NO_VISIBLE_BODY_NOT_COMPILED' if arm=='STANDARD' and n==1 else None}
        for arm in ('HISTORY','STANDARD') for n in (1,2,3)])
    lock=json.loads((out/'lake-manifest.json').read_text())
    tool=json.loads((raw/'22_ENVIRONMENT/TOOLCHAIN_ORIGIN.json').read_text())
    status={'status':'SOURCE_ASSEMBLED_NOT_COMPILED','original_source_commit':'f9e8bc5b38b6e212696e8a30e3e91517af887bbd',
      'source_slice_notice':'SOURCE_NOTICE.md','input_verification':verification,'files':mapping,
      'toolchain':tool,'package_locks':lock['packages'],'candidate_count':len(rows),
      'local_imports_checked':len(imports),'unresolved_local_imports':[],
      'new_model_calls':0,'new_Lean_compilations':0,'independent_kernel':'NOT_RUN'}
    write_json(out/'ASSEMBLY_RECEIPT.json',status)
    return status

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--raw',type=Path);p.add_argument('--out',required=True,type=Path)
    a=p.parse_args();s=assemble(a.raw or default_raw(),a.out)
    print(json.dumps({k:v for k,v in s.items() if k not in ('files','package_locks')},indent=2))
