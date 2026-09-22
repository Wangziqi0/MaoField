"""Exact finite algebra checks for the HClose reconstruction.
These are not a Lean kernel run and do not reconstruct the full NS proof.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sympy as sp

def run():
    R,E,D,c=sp.symbols('R E D c', real=True)
    positive_case=sp.simplify((E+D*c)/R-(E+D*abs(c))/R).subs(c,sp.Symbol('k',positive=True))
    assert sp.simplify(positive_case) == 0
    k=sp.Symbol('k',nonnegative=True)
    neg_difference=sp.simplify(((E+D*abs(c))-(E+D*c)).subs(c,-k))
    assert sp.simplify(neg_difference-2*D*k)==0
    rational=[]
    for rv in [F(1,2),F(1),F(8)]:
      for ev in [F(0),F(1,3)]:
       for dv in [F(0),F(2)]:
        for cv in [F(-3),F(0),F(5,4)]:
         q=ev+dv*abs(cv);rho=q/rv+F(1,16)
         assert (ev+dv*cv)/rv<=q/rv<=rho
         rational.append({'R':str(rv),'E':str(ev),'D':str(dv),'c':str(cv),'Q':str(q),'rho':str(rho)})
    a,b,c0,d,x,y,t0,t1,s=sp.symbols('a b c d x y t0 t1 s',nonzero=True)
    H=sp.Matrix([[a,b],[c0,d]]);S=sp.diag(x,y);A=H*S;T=sp.Matrix([t0,t1])
    assert sp.simplify(A.det()-H.det()*x*y)==0
    inv_delta=sp.simplify(A.inv()*T-S.inv()*H.inv()*T)
    assert inv_delta==sp.zeros(2,1)
    assert sp.simplify((s*A).det()-s**2*x*y*H.det())==0
    return {'scope':'SOURCE_RELATIVE_HCLOSE_AND_COLUMN_SCALING_ALGEBRA',
      'rational_inequality_cases':len(rational),'rational_cases':rational,
      'zero_Q_included':True,'matrix_factorization_identity':'PASS',
      'inverse_column_identity':'PASS','normalised_determinant_identity':'PASS',
      'new_NS_theorem':False,'new_Lean_build':False,'full_NS_replication':False,
      'analytic_proofs':'SUBMISSION/supplementary_information.md, Notes 2 and 4'}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 a.out.parent.mkdir(parents=True,exist_ok=True);o=run();a.out.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');print(f"{o['rational_inequality_cases']} rational cases and 3 symbolic matrix identities: PASS")
