"""Reanalyse source-mapped review records. Offline, no model or Lean calls.

Visible-only SSE is a traceable minimized copy, not the complete original stream.
The complete originals and the transformation map remain in the private master.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re
from pathlib import Path
from assemble_lean import verify_raw,candidates

def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def stream(p):
    visible=[];usage=finish=None;done=False
    for line in p.read_text().splitlines():
        if not line.startswith('data:'):continue
        payload=line[5:].strip()
        if payload=='[DONE]':done=True;continue
        x=json.loads(payload)
        if x.get('usage') is not None:usage=x['usage']
        for c in x.get('choices',[]):
            assert c.get('index',0)==0
            delta=c.get('delta',{})
            assert not any(k in delta for k in ('reasoning','reasoning_content'))
            if delta.get('content'):visible.append(delta['content'])
            if c.get('finish_reason') is not None:finish=c['finish_reason']
    assert done and finish is not None and usage is not None
    return ''.join(visible),usage,finish

def run(raw,out):
    verification=verify_raw(raw);out.mkdir(parents=True,exist_ok=False)
    cm=candidates(raw);rows=[];arms={}
    template=(raw/'20_TASK_AND_RUNNER/PROOF_TEMPLATE.lean.txt').read_text();head,tail=template.split('    -- MODEL_PROOF_HERE',1)
    for arm in ('history','standard'):
        for i in range(3):
            d=raw/f'10_CURRENT_RUN/{arm}/requests/{i:04d}'
            req=load(d/'request.json');rec=load(d/'receipt.json');visible,usage,finish=stream(d/'wire.bin')
            assert visible.encode()==(d/'visible.utf8').read_bytes()
            assert usage==rec['usage'] and finish==rec['finish_reason']
            assert usage['prompt_tokens']+32768+1024<=262144
            assert req['max_tokens']==32768 and req['temperature']==1 and req['top_p']==.95
            for k in range(i):
                assert req['messages'][2+2*k]=={'role':'assistant','content':(raw/f'10_CURRENT_RUN/{arm}/requests/{k:04d}/visible.utf8').read_text()}
            c=next((c for c in cm if c['condition_original_label']==arm.upper() and c['original_request_number']==i+1),None)
            row={'arm':arm.upper(),'attempt':i+1,'original_request_number':i+1,'seed':req['seed'],
                 'prompt_tokens':usage['prompt_tokens'],'completion_tokens':usage['completion_tokens'],
                 'total_tokens':usage['total_tokens'],'finish_reason':finish,'visible_bytes':len(visible.encode()),
                 'visible_sha256':sha(d/'visible.utf8'),'model_seconds':rec['seconds'],
                 'candidate_name':c['candidate_name'] if c else None,
                 'visible_candidate_ordinal':c['visible_candidate_ordinal'] if c else None}
            if c:
                path=raw/c['source'];sub=path.parent
                assert path.read_text()==head+'\n'.join('    '+s for s in visible.splitlines())+tail
                log=(sub/'compile/stdout.bin').read_text();receipt=load(sub/'compile/receipt.json');result=load(sub/'RESULT.json')
                match=re.search(r"'Branch.Direct.completed' depends on axioms: \[([^\]]*)\]",log)
                assert match is not None
                axioms=[a.strip() for a in match.group(1).split(',') if a.strip()]
                assert axioms==result['axioms']
                accepted=receipt['returncode']==0 and 'Build completed successfully' in log and set(axioms)<={'propext','Classical.choice','Quot.sound'}
                assert accepted==(result['status']=='EXACT_LOCAL_GOAL_LEAN_ACCEPTED')
                row.update(outcome='LEAN_ACCEPTED' if accepted else 'LEAN_REJECTED',compiler_returncode=receipt['returncode'],axioms=axioms)
            else:
                assert arm=='standard' and i==0 and not visible and finish=='length'
                row.update(outcome='TRUNCATED_NO_BODY',compiler_returncode=None,axioms=[])
            rows.append(row)
        r=[x for x in rows if x['arm']==arm.upper()]
        arms[arm.upper()]={'calls':len(r),'prompt_tokens':sum(x['prompt_tokens'] for x in r),'completion_tokens':sum(x['completion_tokens'] for x in r),
                          'accepted_attempts':[x['attempt'] for x in r if x['outcome']=='LEAN_ACCEPTED']}
    h=load(raw/'10_CURRENT_RUN/history/requests/0000/request.json');s=load(raw/'10_CURRENT_RUN/standard/requests/0000/request.json')
    assert h['messages'][0]==s['messages'][0]
    assert {k:v for k,v in h.items() if k!='messages'}=={k:v for k,v in s.items() if k!='messages'}
    assert h['messages'][1]['content'].startswith(s['messages'][1]['content'])
    def tree(p):return {str(f.relative_to(p)):sha(f) for f in p.rglob('*') if f.is_file() and str(f.relative_to(p))!='Branch/Direct.lean'}
    same=tree(raw/'10_CURRENT_RUN/history/workspace')==tree(raw/'10_CURRENT_RUN/standard/workspace')
    assert same
    summary={'identity':'SOURCE_MAPPED_VISIBLE_RECORD_REANALYSIS_NOT_NEW_SAMPLING','input_verification':verification,
             'arms':arms,'requests':len(rows),'candidates':len(cm),'prompt_token_difference_first':rows[0]['prompt_tokens']-rows[3]['prompt_tokens'],
             'same_initial_system_and_sampling':True,'same_shared_upstream':same,
             'new_model_calls':0,'new_Lean_compilations':0,'independent_kernel':'NOT_RUN',
             'private_reasoning':'REMOVED_FROM_REVIEW_COPY_NOT_ANALYSED_HERE'}
    put(out/'audit_summary.json',summary);put(out/'attempts.json',rows);put(out/'candidate_manifest.json',cm)
    with (out/'attempts.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps(summary,indent=2))
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,default=Path(__file__).resolve().parent/'raw');p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();run(a.source,a.out)
