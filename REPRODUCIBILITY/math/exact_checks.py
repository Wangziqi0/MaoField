"""Local exact checks; no model, network, Lean or data-generation calls.
The all-quantifier minimax result also needs the written piecewise proof.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import sympy as s

def compute():
 r,u,g,phi,B,C=s.symbols('r u g phi B C',real=True)
 v,q,t=s.symbols('v q t',positive=True)
 z=1+u;p=z*z+r;E=(z+g)**2-p
 rows=[]
 def check(name,expr):
  actual=s.simplify(expr)
  rows.append({'check':name,'computed_remainder':str(actual),'passed':actual==0})
  if actual!=0:raise AssertionError(f'{name}: {actual}')
 check('complete_residual_decomposition',E-(2*g+g*g-r+2*u*g))
 ep=(1+v+g)**2-((1+v)**2+r);em=(1-v+g)**2-((1-v)**2+r)
 check('same_r_different_z_difference',ep-em-4*v*g)
 check('root_parameterization',(q+1)**2-1-(q*q+2*q))
 check('minimax_candidate_two_residuals',(ep.subs({g:q,r:q*q+2*q})-2*v*q)**2+(em.subs({g:q,r:q*q+2*q})+2*v*q)**2)
 check('no_common_exact_action_resultant',s.resultant(ep,em,g)+16*v*v*r)
 check('negative_outer_action_reflection',(-2-t)**2+2*(-2-t)-(t*t+2*t))
 check('linear_complete_residual',E.subs(g,r/2)-(u*r+r*r/4))
 w,Z=s.symbols('w Z',positive=True);rr=w*w-Z*Z
 check('state_aware_root_rationalization',rr/(2*Z)-rr*rr/(2*Z*(w+Z)**2)-(w-Z))
 check('state_aware_linear_compensation',r/(2*z)-(r/2-u*r/(2*z)))
 check('closed_rectangle_positive_radicand_margin',s.Rational(3,4)**2-s.Rational(1,2)-s.Rational(1,16))
 h=r*r*B+u*r*C
 check('two_variable_cutoff_residual',E.subs(g,r/2+phi*h)-(u*r+r*r/4+phi*(2+2*u+r)*h+phi*phi*h*h))
 check('zero_source_update',E.subs({r:0,g:0}))
 gl=s.Rational(1,10);gh=s.sqrt(s.Rational(6,5))-1;zz=s.Rational(9,10);pp=s.Rational(101,100)
 check('successor_counterexample',((zz+gl)**2-pp+s.Rational(1,100))**2+((zz+gh)**2-pp-(s.Rational(1,5)-s.sqrt(30)/25))**2)
 h11,h12,h21,h22=s.symbols('h11 h12 h21 h22');a1,a2,l1,l2=s.symbols('a1 a2 l1 l2',nonzero=True)
 H=s.Matrix([[h11,h12],[h21,h22]]);L=s.diag(l1*l1,l2*l2);y=s.Matrix([a1*a1,a2*a2]);yp=s.Matrix([a1*a1/(l1*l1),a2*a2/(l2*l2)])
 check('consistent_basis_rescaling',sum(x*x for x in H*L*yp-H*y))
 return {'kind':'V3_DETERMINISTIC_EXACT_ALGEBRA_NOT_NEW_EXPERIMENT','checks':rows,'passed':sum(x['passed'] for x in rows),'failed':sum(not x['passed'] for x in rows),'sympy_version':s.__version__,'new_model_generations':0,'scope':'Algebraic identities and boundary calculations; written analysis supplies global domains and minimax proof.'}

def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);args=a.parse_args();res=compute();args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print(json.dumps(res,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
