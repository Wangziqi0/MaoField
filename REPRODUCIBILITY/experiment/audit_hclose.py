"""Read-only independent audit of the supplied HClose handoff.
No model client, Lean invocation, Docker call, or network access is implemented.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re
from pathlib import Path

ALLOWED = {'propext','Classical.choice','Quot.sound'}
def sha(data: bytes)->str:return hashlib.sha256(data).hexdigest()
def load(p:Path):return json.loads(p.read_text(encoding='utf-8'))
def dump(p:Path,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def require(x:bool,msg:str):
    if not x:raise AssertionError(msg)
def parse_sse(data:bytes):
    visible=[]; reasoning=[]; legacy_reasoning=[]; mirrored_chunks=0; usage=None; finish=None; done=False; response_ids=set(); tool_deltas=[]
    for line in data.decode('utf-8').splitlines():
        if not line.startswith('data:'):continue
        payload=line[5:].strip()
        if payload=='[DONE]':done=True;continue
        obj=json.loads(payload)
        if obj.get('id'):response_ids.add(obj['id'])
        if obj.get('usage') is not None:usage=obj['usage']
        for choice in obj.get('choices',[]):
            require(choice.get('index',0)==0,'Unexpected multi-choice stream')
            delta=choice.get('delta',{})
            if delta.get('content'):visible.append(delta['content'])
            rr=delta.get('reasoning'); rc=delta.get('reasoning_content')
            if rr is not None and rc is not None:
                require(rr==rc,'Inconsistent duplicated reasoning fields'); mirrored_chunks+=1
            for value in (rr,rc):
                if isinstance(value,str):legacy_reasoning.append(value)
            if rr is not None or rc is not None:reasoning.append(rr if rr is not None else rc)
            if delta.get('tool_calls'):tool_deltas.extend(delta['tool_calls'])
            if choice.get('finish_reason') is not None:finish=choice['finish_reason']
    require(done and usage is not None and finish is not None,'Incomplete SSE')
    return {'visible':''.join(visible),'reasoning':''.join(reasoning),'usage':usage,'finish_reason':finish,
            'response_ids':sorted(response_ids),'tool_deltas':tool_deltas,
            'legacy_reasoning':''.join(legacy_reasoning),'mirrored_reasoning_chunks':mirrored_chunks}

def audit(source:Path,out:Path):
    source=source.resolve(); out.mkdir(parents=True,exist_ok=True)
    mf=load(source/'PACKAGE_MANIFEST.json')
    paths=[]
    for row in mf['files']:
        p=source/row['path'];require(p.is_file(),'Missing '+row['path'])
        b=p.read_bytes();require(len(b)==row['bytes'],'Size '+row['path']);require(sha(b)==row['sha256'],'Hash '+row['path']);paths.append(row['path'])
    actual={str(p.relative_to(source)) for p in source.rglob('*') if p.is_file()}
    require(actual==set(paths)|{'PACKAGE_MANIFEST.json'},'Manifest closure')
    plan=load(source/'10_CURRENT_RUN/PLAN.json')
    for n,h in plan['package_files'].items():require(sha((source/'20_TASK_AND_RUNNER'/n).read_bytes())==h,'Plan package mismatch '+n)
    template=(source/'20_TASK_AND_RUNNER/PROOF_TEMPLATE.lean.txt').read_text()
    head,foot=template.split('    -- MODEL_PROOF_HERE',1)
    rows=[];checks=[];by_arm={};sources=[]
    for arm in ['history','standard']:
        subs=sorted((source/f'10_CURRENT_RUN/{arm}/submissions').glob('*'))
        sub_by_body={sha((p/'body.lean.txt').read_bytes()):p for p in subs}
        for idx in range(3):
            q=source/f'10_CURRENT_RUN/{arm}/requests/{idx:04d}'
            rec=load(q/'receipt.json');req=load(q/'request.json'); parsed=parse_sse((q/'wire.bin').read_bytes())
            require(sha((q/'request.json').read_bytes())==rec['request_sha256'],'Request hash')
            require(parsed['visible'].encode()==(q/'visible.utf8').read_bytes(),'Visible bytes')
            require(parsed['legacy_reasoning'].encode()==(q/'reasoning.utf8').read_bytes(),'Saved reasoning collector bytes')
            require(len(parsed['legacy_reasoning'])==2*len(parsed['reasoning']),'Unexpected mirrored reasoning collection')
            require(parsed['usage']==rec['usage'],'Usage mismatch')
            require(parsed['finish_reason']==rec['finish_reason'],'Finish mismatch')
            require(req['seed']==plan['seed']+idx,'Seed drift')
            require(req['max_tokens']==32768 and req['temperature']==1.0 and req['top_p']==.95,'Sampling drift')
            require(all(set(m)=={'role','content'} for m in req['messages']),'Unexpected replayed message fields')
            for prior in range(idx):
                expected=(source/f'10_CURRENT_RUN/{arm}/requests/{prior:04d}/visible.utf8').read_text()
                require(req['messages'][2+2*prior]=={'role':'assistant','content':expected},'Replayed assistant differs from visible-only body')
            require(not parsed['tool_deltas'],'Unexpected model tools')
            tk=load(source/f'10_CURRENT_RUN/{arm}/tokenizer/{idx:04d}.json')
            require(tk['count']==rec['usage']['prompt_tokens'],'Tokenizer receipt mismatch')
            require(tk['count']+32768+1024<=262144,'Context bound')
            body=(q/'visible.utf8').read_text()
            row={'arm':arm.upper(),'attempt':idx+1,'seed':req['seed'],'finish_reason':rec['finish_reason'],
                 'prompt_tokens':rec['usage']['prompt_tokens'],'completion_tokens':rec['usage']['completion_tokens'],
                 'total_tokens':rec['usage']['total_tokens'],'model_seconds':rec['seconds'],
                 'visible_bytes':len(body.encode()),'visible_characters':len(body),
                 'mirrored_reasoning_chunks':parsed['mirrored_reasoning_chunks'],
                 'canonical_reasoning_characters':len(parsed['reasoning']),
                 'saved_reasoning_characters':len(parsed['legacy_reasoning']),
                 'start_utc':rec['start_utc'],'end_utc':rec['end_utc'],'request_sha256':rec['request_sha256'],
                 'visible_sha256':sha(body.encode()),'source':str(q.relative_to(source))}
            if rec['finish_reason']=='length':
                require(not body and sha(body.encode()) not in sub_by_body,'Truncated body compiled')
                row.update(outcome='TRUNCATED_NO_BODY',compiler_returncode='',compiler_seconds='',axioms='')
            else:
                sub=sub_by_body.get(sha(body.encode()));require(sub is not None,'No matching submission')
                require((sub/'candidate.lean').read_text()==head+'\n'.join('    '+line for line in body.splitlines())+foot,'Template changed')
                result=load(sub/'RESULT.json');stdout=(sub/'compile/stdout.bin').read_text();crec=load(sub/'compile/receipt.json')
                m=re.search(r"'Branch.Direct.completed' depends on axioms: \[([^\]]*)\]",stdout)
                require(m is not None,'No axiom readout');axs=[a.strip() for a in m.group(1).split(',') if a.strip()]
                require(axs==result['axioms'],'Axiom readout mismatch')
                code=crec.get('returncode',crec.get('code',None));require(code is not None,'No compile code')
                accepted=code==0 and 'Build completed successfully' in stdout and set(axs)<=ALLOWED
                require(accepted==(result['status']=='EXACT_LOCAL_GOAL_LEAN_ACCEPTED'),'Acceptance mismatch')
                require(sha((sub/'candidate.lean').read_bytes())==result['candidate_sha256'],'Candidate hash mismatch')
                row.update(outcome='LEAN_ACCEPTED' if accepted else 'LEAN_REJECTED',compiler_returncode=code,
                    compiler_seconds=crec.get('seconds',''),axioms=';'.join(axs),compiler_source=str(sub.relative_to(source)))
            rows.append(row)
            sources.append({'file':str((q/'wire.bin').relative_to(source)),'sha256':sha((q/'wire.bin').read_bytes())})
        ar=[x for x in rows if x['arm']==arm.upper()]
        by_arm[arm.upper()]={'calls':len(ar),'prompt_tokens':sum(x['prompt_tokens'] for x in ar),
           'completion_tokens':sum(x['completion_tokens'] for x in ar),'model_seconds':sum(x['model_seconds'] for x in ar),
           'accepted_attempts':[x['attempt'] for x in ar if x['outcome']=='LEAN_ACCEPTED'],
           'completed':any(x['outcome']=='LEAN_ACCEPTED' for x in ar)}
    h=load(source/'10_CURRENT_RUN/history/requests/0000/request.json');s=load(source/'10_CURRENT_RUN/standard/requests/0000/request.json')
    require({k:v for k,v in h.items() if k!='messages'}=={k:v for k,v in s.items() if k!='messages'},'First request config differs')
    require(h['messages'][0]==s['messages'][0],'System prompt differs')
    ht=h['messages'][1]['content'];st=s['messages'][1]['content']
    require(ht.startswith(st),'Base user prompt differs')
    addon=ht[len(st):];note=(source/'20_TASK_AND_RUNNER/ADDITIONAL_INFORMATION.md').read_text()
    require(note in addon,'Added note differs')
    # Every byte in the permitted upstream project is identical across arms.
    htroot=source/'10_CURRENT_RUN/history/workspace';stroot=source/'10_CURRENT_RUN/standard/workspace'
    def tree(p):return {str(x.relative_to(p)):sha(x.read_bytes()) for x in p.rglob('*') if x.is_file() and str(x.relative_to(p))!='Branch/Direct.lean'}
    require(tree(htroot)==tree(stroot),'Shared upstream source mismatch')
    # Verify actual code calls and exact reported final failure, without re-running Lean.
    hv=(source/'10_CURRENT_RUN/history/requests/0002/visible.utf8').read_text()
    sv=(source/'10_CURRENT_RUN/standard/requests/0002/visible.utf8').read_text()
    require(all(t in hv and t in sv for t in ['normalizedPair_entry_error','slotRadius_sq']),'Lemma use not shared')
    require('simpa [hsl_eq] using h' in hv and "exact hratio j' i' v' hv''" in sv,'Rewrite trace differs from interpretation')
    err=(subs[-1]/'compile/stdout.bin').read_text()
    require('Type mismatch' in err and 'slotRadius r0 h n ^ 2' in err and 'ChartScales.slotLength' in err,'Expected recorded mismatch absent')
    summary={'source_manifest_files':len(paths),'manifest_closure':'PASS','SSE_complete':6,'compiled_candidates':5,
        'new_model_calls':0,'new_Lean_builds':0,'new_independent_kernel_checks':0,
        'arms':by_arm,'prompt_token_difference_first':rows[0]['prompt_tokens']-rows[3]['prompt_tokens'],
        'same_initial_system_and_sampling':True,'same_initial_user_prefix':True,'additional_note_only_difference':True,
        'same_upstream_workspace_except_candidate':True,'upstream_file_count':len(tree(htroot)),
        'reasoning_artifact_collector_duplicates_mirrored_fields':True,
        'reasoning_not_replayed_in_subsequent_messages':True,
        'both_final_candidates_use_key_lemmas':True,'standard_final_error':'equality transported in interval membership, but not conclusion',
        'total_prompt_tokens':sum(x['prompt_tokens'] for x in rows),'total_completion_tokens':sum(x['completion_tokens'] for x in rows),
        'total_tokens':sum(x['total_tokens'] for x in rows),
        'interpretation':'One post-selection paired case, not a general effect estimate or full NS proof.'}
    dump(out/'audit_summary.json',summary);dump(out/'attempts.json',rows);dump(out/'wire_sources.json',sources)
    fields=sorted(set().union(*(r.keys() for r in rows)))
    with (out/'attempts.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    (out/'actual_prompt_addition.txt').write_text(addon)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();audit(args.source,args.out)
