"""Replay unchanged saved Lean candidates in an offline, credential-free sandbox.

The public Lean toolchain and dependency cache are supplied explicitly. This
does not generate model responses or run an independent proof kernel.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, subprocess, time

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def save(p, v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--project',type=Path,required=True)
    ap.add_argument('--toolchain',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--timeout',type=int,default=1800)
    a=ap.parse_args()
    project=a.project.resolve(); tool=a.toolchain.resolve(); out=a.out.resolve()
    if out.exists(): raise SystemExit('Output must be a fresh directory')
    if not shutil.which('bwrap'): raise SystemExit('bubblewrap is required; no unsandboxed fallback')
    if os.getuid()==0: raise SystemExit('Use an ordinary non-root user')
    out.mkdir(parents=True)
    assembly=json.loads((project/'ASSEMBLY_RECEIPT.json').read_text())
    rows=json.loads((project/'candidate_manifest.json').read_text())
    for x in assembly['files']:
        if sha(project/x['assembled_path'])!=x['sha256']: raise SystemExit('Source identity mismatch: '+x['assembled_path'])
    for x in rows:
        if sha(project/'saved_candidates'/x['candidate_name'])!=x['sha256']: raise SystemExit('Candidate identity mismatch')
    cache=project/'.lake/packages'; locks=assembly['package_locks']
    lock_checks=[]
    for q in locks:
        p=cache/q['name']
        got=subprocess.run(['git','-C',str(p),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
        if got!=q['rev']: raise SystemExit('Dependency commit mismatch: '+q['name'])
        lock_checks.append({'name':q['name'],'commit':got,'build_cache_present':(p/'.lake/build').exists()})

    def sandbox(work, args, packages=True):
        cmd=['bwrap','--unshare-all','--die-with-parent','--new-session',
             '--ro-bind','/usr','/usr','--symlink','usr/bin','/bin',
             '--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64',
             '--ro-bind',str(tool),'/opt/lean','--bind',str(work),'/work',
             '--proc','/proc','--dev','/dev','--tmpfs','/tmp',
             '--clearenv','--setenv','HOME','/tmp','--setenv','XDG_CACHE_HOME','/tmp/cache',
             '--setenv','PATH','/opt/lean/bin:/usr/bin:/bin',
             '--setenv','LEAN_NUM_THREADS','4','--chdir','/work']
        if packages:
            cmd+=['--ro-bind',str(cache),'/work/.lake/packages']
            cmd+=['--setenv','GIT_CONFIG_COUNT',str(len(locks))]
            for i,q in enumerate(locks):
                cmd+=['--setenv',f'GIT_CONFIG_KEY_{i}','safe.directory','--setenv',f'GIT_CONFIG_VALUE_{i}',f'/work/.lake/packages/{q["name"]}']
        return cmd+args

    version=subprocess.run(sandbox(project,['/opt/lean/bin/lean','--version'],False),capture_output=True,text=True,check=True)
    if '4.34.0-rc2' not in version.stdout or '6a10ac8c22beadecabdbb0919c2b50214762f91d' not in version.stdout:
        raise SystemExit('Historical Lean version/commit mismatch')
    status={'kind':'OFFLINE_ORDINARY_LEAN_REPLAY','backend':'bubblewrap','network':'disabled',
            'source_assembly_sha256':sha(project/'ASSEMBLY_RECEIPT.json'),
            'lean_version':version.stdout.strip(),'dependency_checks':lock_checks,
            'new_model_calls':0,'independent_kernel':'NOT_RUN','results':[],'status':'RUNNING'}
    save(out/'STATUS.json',status)
    for row in rows:
        name=row['candidate_name']; work=out/('project_'+name.removesuffix('.lean'))
        shutil.copytree(project,work,ignore=shutil.ignore_patterns('.lake','.preparation*','dependency_preparation','saved_candidates'))
        (work/'Branch').mkdir(exist_ok=True); (work/'.lake/packages').mkdir(parents=True)
        # Reuse only the common-source cache built before any candidate replay.
        # Candidate-specific modules are never present in this preparation tree.
        if (project/'.lake/build').exists():
            if list((project/'.lake/build').rglob('Direct.olean')):
                raise SystemExit('Common cache contains a candidate-specific Direct module')
            shutil.copytree(project/'.lake/build',work/'.lake/build')
        shutil.copy2(project/'saved_candidates'/name,work/'Branch/Direct.lean')
        logs=out/name; logs.mkdir(); command=sandbox(work,['/opt/lean/bin/lake','build','+Branch.Direct'])
        started=time.monotonic(); timed_out=False
        with (logs/'stdout.log').open('wb') as stdout,(logs/'stderr.log').open('wb') as stderr:
            try: proc=subprocess.run(command,stdout=stdout,stderr=stderr,timeout=a.timeout); rc=proc.returncode
            except subprocess.TimeoutExpired: timed_out=True; rc=None
        text=(logs/'stdout.log').read_text(errors='replace')+(logs/'stderr.log').read_text(errors='replace')
        if timed_out: outcome='INFRASTRUCTURE_TIMEOUT'
        elif any(s in text.lower() for s in ['unknown module prefix','no such file','failed to fetch','could not resolve','unknown package','failed to download','read-only file system']): outcome='INFRASTRUCTURE_FAILURE'
        elif rc==0: outcome='ORDINARY_LEAN_REPLAY_ACCEPTED'
        elif re.search(r'(Branch/Direct\.lean:\d+|error: Branch\.Direct)',text): outcome='ORDINARY_LEAN_CANDIDATE_REJECTED'
        else: outcome='NONZERO_REQUIRES_REVIEW'
        item={**row,'returncode':rc,'replay_status':outcome,'elapsed_seconds':round(time.monotonic()-started,3),
              'candidate_sha256_after':sha(work/'Branch/Direct.lean'),
              'stdout_sha256':sha(logs/'stdout.log'),'stderr_sha256':sha(logs/'stderr.log')}
        if item['candidate_sha256_after']!=row['sha256']: raise SystemExit('Candidate changed during replay')
        status['results'].append(item); save(out/'STATUS.json',status)
        print(name, outcome, flush=True)
    status['new_Lean_compilations']=len(status['results'])
    status['status']='COMPLETED_ORDINARY_LEAN_REPLAY_NOT_INDEPENDENT_KERNEL' if all(x['replay_status'] in ['ORDINARY_LEAN_REPLAY_ACCEPTED','ORDINARY_LEAN_CANDIDATE_REJECTED'] for x in status['results']) else 'COMPLETED_WITH_INFRASTRUCTURE_FAILURE'
    save(out/'STATUS.json',status)
    return 0 if status['status']=='COMPLETED_ORDINARY_LEAN_REPLAY_NOT_INDEPENDENT_KERNEL' else 2

if __name__=='__main__': raise SystemExit(main())
