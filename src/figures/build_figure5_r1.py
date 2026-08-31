from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT=Path(__file__).resolve().parents[2]/'outputs'/'figures'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({
 'font.family':'sans-serif','font.sans-serif':['Arial','Liberation Sans','DejaVu Sans'],
 'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,
 'font.size':5.8,'savefig.transparent':False
})
INK='#172B45'; MID='#6B7C93'; BLUE='#0B73B7'; PINK='#CC6FA5'; GREEN='#009E73'; ORANGE='#D55E00'; PALE='#F2F5F8'; LINE='#CBD6E2'; WHITE='#FFFFFF'

def rounded(ax,x,y,w,h,edge,lw=1.05,fc=PALE,r=.012):
 p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0.008,rounding_size={r}',fc=fc,ec=edge,lw=lw)
 ax.add_patch(p); return p

def arrow(ax,a,b,color=MID,lw=1.0,ms=8):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=ms,color=color,lw=lw,shrinkA=2,shrinkB=2))

def panel(ax,label,x=.005,y=.975): ax.text(x,y,label,fontsize=8.2,fontweight='bold',color=INK,ha='left',va='top')

fig=plt.figure(figsize=(7.0,5.0))
gs=fig.add_gridspec(2,2,height_ratios=[.50,.50],width_ratios=[.53,.47],left=.025,right=.985,top=.98,bottom=.045,wspace=.14,hspace=.12)

# A
ax=fig.add_subplot(gs[0,:]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'a',.002,.98)
ax.text(.067,.85,'Three-stage empirical evidence chain',fontsize=7.2,fontweight='bold',color=INK,ha='left',va='center')
xs=[.065,.365,.68]; ws=[.27,.27,.27]; cols=[BLUE,PINK,GREEN]
titles=['Phase 23 exact equality','Near-saturated channel gap','GLM calibration boundary']
bodies=[
 'U / A_FT / P / O\nmain96 + sealed32\nestimate = 0; intervals [0, 0]',
 'A_SIB − R\nmain48: −0.9792 [−1.0417, −0.8958]\nsealed16: −1.0000 [−1, −1]',
 'ordinary: P 30/32; O 23/32\nA_FT 26/32; U 25/32\nstructure 31/32; invalid'
]
for x,w,c,t,b in zip(xs,ws,cols,titles,bodies):
 rounded(ax,x,.20,w,.47,c,lw=1.05)
 ax.text(x+.035,.565,t,fontsize=6.4,fontweight='bold',color=c,ha='left',va='top')
 ax.text(x+.035,.44,b,fontsize=5.4,color=INK,ha='left',va='top',linespacing=1.20)
arrow(ax,(.335,.435),(.365,.435)); arrow(ax,(.635,.435),(.68,.435))
ax.text(.694,.15,'invalid: one renderer mismatch\n+ one typed missing',fontsize=5.0,color=INK,ha='left',va='top',linespacing=1.2)

# B
ax=fig.add_subplot(gs[1,0]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'b',.002,.99)
ax.text(.075,.91,'Post-hoc structure-estimand counterexample',fontsize=6.8,fontweight='bold',color=INK,ha='left',va='center')
headers=[('response rule',.08,'left'),('DN acc.',.49,'center'),('UF acc.',.69,'center'),('contrast',.89,'center')]
for t,x,ha in headers: ax.text(x,.70,t,fontsize=5.5,fontweight='bold',color=INK,ha=ha,va='center')
rows=[(.43,'perfect arm-specific recovery','1','1','0'),(.18,'arm-blind constant-true','1','0','+1')]
for y,rule,dn,uf,c in rows:
 rounded(ax,.06,y,.88,.19,LINE,lw=.75,fc=PALE,r=.008)
 ax.text(.095,y+.095,rule,fontsize=5.25,color=INK,ha='left',va='center')
 ax.text(.49,y+.095,dn,fontsize=5.8,fontweight='bold',color=INK,ha='center',va='center')
 ax.text(.69,y+.095,uf,fontsize=5.8,fontweight='bold',color=INK,ha='center',va='center')
 ax.text(.89,y+.095,c,fontsize=5.8,fontweight='bold',color=INK,ha='center',va='center')
ax.text(.08,.035,'Same DN/UF truth assignment; the derived contrast is not monotone in structural fidelity.',fontsize=4.75,color=INK,ha='left',va='bottom')

# C
ax=fig.add_subplot(gs[1,1]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'c',.002,.99)
ax.text(.075,.91,'Identification architecture and field implication',fontsize=6.8,fontweight='bold',color=INK,ha='left',va='center')
rounded(ax,.07,.48,.39,.28,BLUE,lw=1.05)
rounded(ax,.60,.48,.36,.28,ORANGE,lw=1.05)
ax.text(.105,.68,'Observed now',fontsize=6.2,fontweight='bold',color=BLUE,ha='left',va='center')
ax.text(.105,.595,'evaluator-visible Cvis(H)\nequality + evaluator-output\nequality',fontsize=5.0,color=INK,ha='left',va='top',linespacing=1.16)
ax.text(.64,.68,'Not established',fontsize=6.2,fontweight='bold',color=ORANGE,ha='left',va='center')
ax.text(.64,.595,'future intervention-response\nequality without a separating\nevaluator',fontsize=4.85,color=INK,ha='left',va='top',linespacing=1.16)
arrow(ax,(.465,.62),(.595,.62),ORANGE,lw=1.0,ms=8)
ax.text(.53,.775,'does not imply',fontsize=4.7,color=ORANGE,ha='center',va='center')
ax.text(.095,.39,'Field implication',fontsize=5.9,fontweight='bold',color=INK,ha='left',va='center')
ax.text(.095,.27,'Memory, self-evolving agents and AI scientists require\ninterventions and evaluators that separate candidate\nresponse laws; current-content/output equality alone is insufficient.',fontsize=4.85,color=INK,ha='left',va='top',linespacing=1.16)
ax.text(.095,.035,'Identification principle; not evidence that true response laws differed.',fontsize=4.55,color=MID,ha='left',va='bottom')

for ext in ['svg','pdf']:
 fig.savefig(OUT/f'Figure_5_Integrated_Identification_Boundary.{ext}',bbox_inches='tight',pad_inches=.02,facecolor='white')
fig.savefig(OUT/'Figure_5_Integrated_Identification_Boundary.png',dpi=300,bbox_inches='tight',pad_inches=.02,facecolor='white')
plt.close(fig)
