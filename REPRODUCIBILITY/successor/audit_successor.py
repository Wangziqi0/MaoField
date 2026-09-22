"""Read-only reconstruction of previously executed successor records; no model calls.

Use --raw-root for the safely extracted original archive, or --inputs to rerun
from the source-mapped, exported mathematical records. No result is sampled.
"""
from pathlib import Path
import argparse,ast,csv,hashlib,json,shutil
from collections import Counter
from decimal import Decimal, localcontext
import mpmath as mp

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def load(p): return json.loads(p.read_text())

def evaluate(s,env):
    node=ast.parse(s,mode='eval')
    def rec(n):
        if isinstance(n,ast.Expression): return rec(n.body)
        if isinstance(n,ast.Constant) and type(n.value) in (int,float): return mp.mpf(str(n.value))
        if isinstance(n,ast.Name) and n.id in env:return env[n.id]
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            x=rec(n.operand);return x if isinstance(n.op,ast.UAdd) else -x
        if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow)):
            a,b=rec(n.left),rec(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
            if isinstance(n.op,ast.Div):return a/b
            if abs(b)>100: raise ValueError('Exponent outside audit allowance')
            return a**b
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('sqrt','abs') and len(n.args)==1:
            return (mp.sqrt if n.func.id=='sqrt' else abs)(rec(n.args[0]))
        raise ValueError('Unrecognised expression: '+ast.dump(n))
    return rec(node)

def table(path, rows):
    if not rows:return
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def check_historical_provenance(raw=None):
    base=Path(__file__).resolve().parent/'provenance'
    manifest=load(base/'MANIFEST.json');values={};hashes={}
    for item in manifest:
        p=(raw/'rounds/20260918_ns_r6_ab_execution/supplement_a_r3'/item['source']) if raw else base/item['file']
        assert sha(p)==item['sha256'],item['source']
        hashes[item['source']]=sha(p)
        if p.suffix=='.json':
            value=load(p);values[item['source']]=value
            for key,expected in item['predicates'].items():
                assert value[key]==expected and type(value[key])==type(expected),(item['source'],key)
    original='analysis_view/science_A/pre_supplement_failure/P01_s1_W2/'
    complete=values['remote_raw/COMPLETE.json']
    assert hashes[original+'request_01/request.json']==hashes['remote_raw/request_01/request.json']==complete['payload_sha256']
    return {'original_status':values[original+'STATUS.json']['status'],
        'original_completion':values[original+'STATUS.json']['reason'],
        'original_effect_applied':values[original+'RETURNED_NOT_APPLIED.json']['effect_applied'],
        'no_replay':values[original+'request_01/parent_timeout.json']['no_replay'],
        'supplement_status':complete['status'],'old_unknown_resolved':complete['old_unknown_resolved'],
        'requests_sent':complete['cumulative_A_sent'],'requests_complete':complete['cumulative_A_complete'],
        'source_receipt_hashes':hashes,'authority_receipt_verified':True}

def analyse(inputs,out,raw=None):
    out.mkdir(parents=True,exist_ok=True);mp.mp.dps=100
    catalog=load(inputs/'catalog.json')
    for x in catalog['files']:
        p=inputs/x['export_path'];assert p.is_file() and sha(p)==x['sha256'],x
    phases={p:load(inputs/p/'PLAN.json') for p in ('A','B')}
    all_rows=[];stats={};inherit=[];summary=[];equal=[];witness=[];symbolic=[]
    for phase,plan in phases.items():
        count=Counter();effects={};metas={s['id']:s for s in plan['stages']}
        for s in plan['stages']:
            sid=s['id'];sr=inputs/phase/'stages'/sid
            artifact=load(sr/'artifact.json');effect=load(sr/'effect.json');effects[sid]=effect
            assert sha(sr/'terminal.utf8')==artifact['terminal_sha256']
            assert artifact.get('program')==effect.get('program')
            if artifact.get('program'):
                import re
                visible=(sr/'terminal.utf8').read_text().strip()
                if visible.startswith('```'):
                    visible=re.sub(r'^```(?:json)?\s*','',visible);visible=re.sub(r'\s*```$','',visible)
                vv=json.loads(visible)
                assert {'B':vv['B_expression'],'C':vv['C_expression']}==artifact['program']

            count['stages']+=1;count['nonempty_programs']+=bool(artifact.get('program'))
            for row in effect['rows']:
                z,g,p=map(mp.mpf,[row['z_before'],row['increment'],row['target']])
                calc=(z+g)**2-p;stored=mp.mpf(row['residual'])
                err=abs(calc-stored)/(1+abs(calc))
                assert err<mp.mpf('1e-65'),(sid,row['id'],str(err))
                r,u=map(mp.mpf,[row['r'],row['u']]);assert abs(r-(p-z*z))/(1+abs(r))<mp.mpf('1e-65')
                assert abs(u-(z-1))<mp.mpf('1e-65')
                all_rows.append({'phase':phase,'stage_id':sid,'parent_id':s['parent_id'],
                  'stage':s['stage'],'arm':s.get('arm') or 'common','id':row['id'],
                  'family':row['family'],'tau':row['tau'],'x':row['x'],'slot':row['slot'],
                  'target':row['target'],'z_before':row['z_before'],'increment':row['increment'],
                  'z_after':row['z_after'],'r':row['r'],'u':row['u'],'pure':row['pure'],
                  'cross':row['cross'],'residual':row['residual'],'abs_residual':row['abs_residual'],
                  'status':row['status'],'program_sha256':artifact.get('program_sha256')})
            packet=load(sr/'parent_snapshot.json')
            if packet.get('actual_parent_meta'):
                pm=packet['actual_parent_meta'];par=pm['stage_id'];old=load(inputs/phase/'stages'/par/'effect.json')
                original_hash=next(x['sha256'] for x in catalog['files'] if x['export_path']==f'{phase}/stages/{par}/effect.json')
                assert pm['effect_sha256']==original_hash
                current={r['id']:r['z'] for r in packet['actual_state']['rows']}
                assert current=={r['id']:r['z_after'] for r in old['rows']}
                assert effect['parent_sha256']==original_hash
                inherit.append({'phase':phase,'stage_id':sid,'parent_stage':par,'parent_effect_sha256':original_hash,
                    'actual_state_byte_strings_match':True,'rows':len(current)})
            for q in sorted(sr.glob('result_*.json')):
                rr=load(q);count['complete_returns']+=1;count['stop_returns']+=rr.get('finish_reason')=='stop'
                us=rr.get('usage',{});count['input_tokens']+=us.get('prompt_tokens',0);count['output_tokens']+=us.get('completion_tokens',0)
        count['empty_programs']=count['stages']-count['nonempty_programs'];stats[phase]=dict(count)
        for stage in (['W1','W2'] if phase=='A' else ['W2']):
            t,c=('NS','NUMERIC') if phase=='A' else ('REVISED','INITIAL')
            for fam in ['ZERO','UNIFORM','LEFT','RIGHT','BOTH']:
                diffs=[]
                for parent in plan['parents']:
                    candidates=[s for s in plan['stages'] if s['parent_id']==parent['id'] and s['stage']==stage]
                    ts=next(s for s in candidates if s['arm']==t);cs=next(s for s in candidates if s['arm']==c)
                    er={r['id']:r for r in effects[cs['id']]['rows']}
                    for row in effects[ts['id']]['rows']:
                        if row['family']==fam and row['tau'] in ('1/128','1/512'):
                            diffs.append(mp.mpf(row['abs_residual'])-mp.mpf(er[row['id']]['abs_residual']))
                summary.append({'phase':phase,'stage':stage,'family':fam,'treatment':t,'control':c,
                    'mean_absolute_residual_difference':mp.nstr(sum(diffs)/len(diffs),35),
                    'paired_positions':len(diffs),'formation_histories':len(plan['parents']),
                    'post_adaptation':True,'supplementary_observation':phase=='A' and stage=='W2'})
        if phase=='B':
            for p in plan['parents']:
                d0=load(inputs/phase/'stages'/(p['id']+'_W0')/'artifact.json')['program']
                d1=load(inputs/phase/'stages'/(p['id']+'_W1')/'artifact.json')['program']
                equal.append({'parent_id':p['id'],'identical_code':d0==d1,'initial':d0,'revised':d1})
    point='UNIFORM:t=1/64:x=1/8:s=0'
    sels=[('A','P00_s0_W1','initial'),('A','P00_s0_W1','draft'),('A','P00_s0_W1','effect'),
          ('A','P00_s0_W2','initial'),('A','P00_s0_W2','effect'),
          ('B','P07_W1','initial'),('B','P07_W1','effect'),('B','P07_s0_W2','initial'),('B','P07_s0_W2','effect')]
    max_err=mp.mpf('0')
    for phase,sid,kind in sels:
        d=load(inputs/phase/'stages'/sid/(kind+'.json'));r=next(r for r in d['rows'] if r['id']==point)
        env={k:mp.mpf(r[k]) for k in ('r','u')};B=evaluate(d['program']['B'],env);C=evaluate(d['program']['C'],env)
        g=env['r']/2+env['r']**2*B+env['u']*env['r']*C
        calc=(1+env['u']+g)**2-mp.mpf(r['target'])
        err=abs(calc-mp.mpf(r['residual']))/(1+abs(calc));max_err=max(max_err,err)
        assert r['local_region']=='SAFE' and err<mp.mpf('1e-65')
        witness.append({'phase':phase,'stage_id':sid,'kind':kind,'coordinate':point,'program':d['program'],
            'program_sha256':d.get('program_sha256'), 'r':r['r'],'u':r['u'],'target':r['target'],
            'z_before':r['z_before'],'increment':r['increment'],'pure':r['pure'],'cross':r['cross'],
            'residual':r['residual'],'z_after':r['z_after'],'recomputed_100_digits':mp.nstr(calc,100),
            'source':f'{phase}/stages/{sid}/{kind}.json'})
    import sympy as sp
    r,u,a,b,t=sp.symbols('r u a b t',real=True)
    Cs=[-sp.Rational(1,2),(-1+u)/2,(-1+u-u*u)/2]
    for i,c in enumerate(Cs):
        g=r/2-r*r/8+u*r*c;E=sp.expand(2*(1+u)*g+g*g-r)
        ser=sp.series(E.subs({u:a*t,r:b*t**3}),t,0,8).removeO().expand()
        symbolic.append({'version':i,'C':str(c),'whole_residual':str(E),'series_through_order_7':str(ser)})
    dump(out/'cohort_status.json',stats);dump(out/'inheritance.json',inherit);dump(out/'main_contrasts.json',summary)
    dump(out/'version_identity.json',equal);dump(out/'selected_witnesses.json',witness);dump(out/'symbolic_successor.json',symbolic)
    table(out/'complete_effects.csv',all_rows);table(out/'main_contrasts.csv',summary)
    table(out/'selected_coordinates.csv',[{k:v for k,v in x.items() if k!='program'} for x in witness])
    result={'historical_only':True,'new_model_calls':0,'effects_recomputed':len(all_rows),'stages':sum(x['stages'] for x in stats.values()),
        'historical_complete_requests':sum(x['complete_returns'] for x in stats.values()),'parent_state_links_checked':len(inherit),
        'selected_coordinate_programs_recomputed':len(witness),'maximum_selected_normalised_difference':mp.nstr(max_err,18),
        'unchanged_B_versions':sum(x['identical_code'] for x in equal),
        'selection_identity':'Post-selection explanatory traces, not replacement endpoints or independent confirmations',
        'A_historical_unknown_request':check_historical_provenance(raw)}
    dump(out/'audit_result.json',result);return result

def export(raw,out):
    root=raw/'rounds/20260918_ns_r6_ab_execution'
    roots={'A':root/'supplement_a_r3/analysis_view/science_A','B':root/'continuation_r2/remote_final/science_B'}
    out.mkdir(parents=True,exist_ok=True);files=[];derived=[]
    def copy(p,rel):
        q=out/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
        files.append({'export_path':rel,'original_member':p.relative_to(raw).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
    for phase,base in roots.items():
        copy(base/'PLAN.json',f'{phase}/PLAN.json');plan=load(base/'PLAN.json')
        for st in plan['stages']:
            sid=st['id'];sr=base/'stages'/sid
            for filename in ['artifact.json','terminal.utf8']:
                copy(sr/filename,f'{phase}/stages/{sid}/{filename}')
            copy(base/'effects'/sid/'output.json',f'{phase}/stages/{sid}/effect.json')
            for kind,name in [('initial','initial_calculation'),('draft','draft_calculation')]:
                p=sr/name/'output.json'
                if p.exists():copy(p,f'{phase}/stages/{sid}/{kind}.json')
            for q in sorted(sr.glob('request_*/result.json')):
                # Result objects are exported with transport metadata removed: content/math/usage unchanged.
                d=load(q);clean={k:d[k] for k in ('finish_reason','usage','message') if k in d}
                # The selected visible response is enough for review; private reasoning remains in original archive.
                if 'message' in clean:clean['message']={k:v for k,v in clean['message'].items() if k in ('role','content')}
                rel=f'{phase}/stages/{sid}/result_{q.parent.name.split("_")[-1]}.json';dump(out/rel,clean)
                derived.append({'export_path':rel,'original_member':q.relative_to(raw).as_posix(),'original_sha256':sha(q),
                    'change':'Preserve visible content, finish and usage; exclude private reasoning/transport fields','sha256':sha(out/rel)})
            ip=sr/'initial_packet.json';d=load(ip)
            keep={k:d[k] for k in ('actual_parent_meta','actual_state','program_library','active_program') if k in d}
            rel=f'{phase}/stages/{sid}/parent_snapshot.json';dump(out/rel,keep)
            derived.append({'export_path':rel,'original_member':ip.relative_to(raw).as_posix(),'original_sha256':sha(ip),
                            'change':'Project only actual state, parent hashes and programme inventory; no prompts/private text','sha256':sha(out/rel)})
    for x in derived:files.append({k:x[k] for k in ('export_path','original_member','sha256')} | {'transformed':True})
    dump(out/'catalog.json',{'source_archive':'NS_R6_AB_RAW_WITH_A_SUPPLEMENT_20260919_UNDER100MB.tar.xz',
        'source_sha256':'9b8fde263413edceb5a980de182a347e4aa10995afc20c982e8e8f78dcb43ba4','files':files,'transformations':derived})
    return len(files)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--raw-root',type=Path);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.raw_root: export(a.raw_root,a.inputs)
    print(json.dumps(analyse(a.inputs,a.out,a.raw_root),indent=2))
