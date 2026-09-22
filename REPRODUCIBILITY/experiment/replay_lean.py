"""Replay saved candidates only in an explicitly selected Docker environment.
Default is an offline probe. This does not run models or independent kernels.
"""
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess,sys
from assemble_lean import write_json,sha

def nonroot_user():
    uid, gid = os.getuid(), os.getgid()
    if uid == 0:
        raise ValueError('Run --execute as a non-root account that owns the prepared project; no root-container fallback')
    return f'{uid}:{gid}'

def invoke(argv,out:Path,timeout=600):
    out.mkdir(parents=True,exist_ok=True)
    try:
        p=subprocess.run(argv,capture_output=True,timeout=timeout)
        (out/'stdout.bin').write_bytes(p.stdout);(out/'stderr.bin').write_bytes(p.stderr)
        return {'status':'RETURNED','returncode':p.returncode,'argv':argv,
                'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()}
    except subprocess.TimeoutExpired as e:
        (out/'stdout.bin').write_bytes(e.stdout or b'');(out/'stderr.bin').write_bytes(e.stderr or b'')
        return {'status':'INFRASTRUCTURE_TIMEOUT','returncode':None,'argv':argv}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepared-project',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
    p.add_argument('--probe',action='store_true');p.add_argument('--execute',action='store_true')
    p.add_argument('--image',help='Pinned local Docker image ID sha256:... containing exact Lean/Lake')
    p.add_argument('--package-cache',type=Path,help='Dependency-ready .lake/packages with source git commits')
    p.add_argument('--timeout',type=int,default=1800)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    status={'kind':'SAVED_CANDIDATE_REPLAY','local_lean':shutil.which('lean'),'local_lake':shutil.which('lake'),
      'docker':shutil.which('docker'),'required_lean':'4.34.0-rc2','new_model_calls':0,
      'new_Lean_compilations':0,'independent_kernel':'NOT_RUN','status':'NOT_RUN_PROBE_ONLY'}
    try:
        assembly=json.loads((a.prepared_project/'ASSEMBLY_RECEIPT.json').read_text())
        rows=json.loads((a.prepared_project/'candidate_manifest.json').read_text())
        for row in assembly['files']:
            if sha(a.prepared_project/row['assembled_path'])!=row['sha256']:raise ValueError('Prepared source changed')
        for row in rows:
            if sha(a.prepared_project/'saved_candidates'/row['candidate_name'])!=row['sha256']:raise ValueError('Saved candidate changed')
        status['candidate_count']=len(rows);status['candidate_mapping']=rows
        if not a.execute:
            if not status['docker'] or not status['local_lean']:status['status']='NOT_RUN_TOOLCHAIN_AND_CONTAINER_UNAVAILABLE'
            return status
        if not status['docker']:raise RuntimeError('Docker runtime unavailable; no host fallback')
        user_id=nonroot_user()
        if not a.image or not re.fullmatch(r'sha256:[0-9a-f]{64}',a.image):raise ValueError('Supply a pinned local image ID')
        if not a.package_cache or not a.package_cache.is_dir():raise ValueError('Dependency-ready package cache required')
        locks=assembly['package_locks'];gitchecks=[]
        for package in locks:
            root=a.package_cache/package['name']
            c=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True)
            if c.returncode or c.stdout.strip()!=package['rev']:raise ValueError('Dependency commit mismatch: '+package['name'])
            if not (root/'.lake/build').exists():raise ValueError('Dependency build cache absent: '+package['name'])
            gitchecks.append({'name':package['name'],'commit':c.stdout.strip()})
        status['dependency_checks']=gitchecks
        def docker(work, command, packages=True):
            x=['docker','run','--rm','--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges',
               '--pids-limit','512','--memory','16g','--cpus','4','--user',user_id,
               '--tmpfs','/tmp:rw,nosuid,nodev,size=4g','-e','HOME=/tmp','-e','XDG_CACHE_HOME=/tmp','-e','LEAN_NUM_THREADS=4',
               '--mount',f'type=bind,src={work.resolve()},dst=/work','--workdir','/work']
            if packages:
                x+=['--mount',f'type=bind,src={a.package_cache.resolve()},dst=/work/.lake/packages,readonly']
                x+=['-e',f'GIT_CONFIG_COUNT={len(locks)}']
                for i,q in enumerate(locks):x+=['-e',f'GIT_CONFIG_KEY_{i}=safe.directory','-e',f'GIT_CONFIG_VALUE_{i}=/work/.lake/packages/{q["name"]}']
            return x+[a.image]+command
        version=invoke(docker(a.prepared_project,['lean','--version'],False),a.out/'version',60)
        v=(a.out/'version/stdout.bin').read_text(errors='replace')
        if version['returncode']!=0 or '4.34.0-rc2' not in v:raise ValueError('Container Lean version mismatch')
        status['container_version']=version;status['results']=[]
        for row in rows:
            work=a.out/('project_'+row['candidate_name'].removesuffix('.lean'))
            shutil.copytree(a.prepared_project,work,ignore=shutil.ignore_patterns('saved_candidates','.lake'))
            (work/'Branch').mkdir(exist_ok=True);shutil.copyfile(a.prepared_project/'saved_candidates'/row['candidate_name'],work/'Branch/Direct.lean')
            (work/'.lake/packages').mkdir(parents=True)
            rec=invoke(docker(work,['lake','build','+Branch.Direct']),a.out/row['candidate_name'],a.timeout)
            text=((a.out/row['candidate_name']/'stdout.bin').read_bytes()+(a.out/row['candidate_name']/'stderr.bin').read_bytes()).decode('utf-8','replace')
            if rec['status']=='INFRASTRUCTURE_TIMEOUT':state='INFRASTRUCTURE_TIMEOUT'
            elif any(k in text.lower() for k in ['unknown module prefix','no such file','failed to fetch','could not resolve','unknown package','failed to download']):state='INFRASTRUCTURE_FAILURE'
            elif rec['returncode']==0:state='ORDINARY_LEAN_REPLAY_ACCEPTED'
            elif re.search(r'(Branch/Direct\.lean:\d+|error: Branch\.Direct)',text):state='ORDINARY_LEAN_CANDIDATE_REJECTED'
            else:state='NONZERO_REQUIRES_INFRASTRUCTURE_REVIEW'
            status['results'].append({**row,**rec,'replay_status':state})
            status['new_Lean_compilations']+=1
        status['status']='EXECUTED_ORDINARY_LEAN_REPLAY_NOT_INDEPENDENT_KERNEL'
        if any(x['replay_status'] not in ('ORDINARY_LEAN_REPLAY_ACCEPTED','ORDINARY_LEAN_CANDIDATE_REJECTED') for x in status['results']):
            status['status']='EXECUTED_WITH_INFRASTRUCTURE_OR_UNCLASSIFIED_FAILURES'
    except Exception as e:
        status['status']='NOT_RUN_OR_PARTIAL_INFRASTRUCTURE_BLOCK';status['error']=str(e)
    finally:
        write_json(a.out/'replay_status.json',status)
        print(json.dumps(status,indent=2))
    return status
if __name__=='__main__':
    result=main()
    if '--execute' in sys.argv and result['status']!='EXECUTED_ORDINARY_LEAN_REPLAY_NOT_INDEPENDENT_KERNEL':
        raise SystemExit(2)
