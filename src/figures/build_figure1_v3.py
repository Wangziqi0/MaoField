from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

REPO=Path(__file__).resolve().parents[2]
OUT=REPO/'outputs'/'figures'
OUT.mkdir(parents=True,exist_ok=True)

plt.rcParams.update({
    'font.family':'sans-serif','font.sans-serif':['Arial','Liberation Sans','DejaVu Sans'],
    'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,
    'font.size':6.5,'axes.titlesize':7.3,'axes.labelsize':6.5,
    'savefig.transparent':False
})
INK='#1F2937'; MID='#64748B'; LIGHT='#F8FAFC'
BLUE='#0072B2'; ORANGE='#E69F00'; GREEN='#009E73'; PURPLE='#CC79A7'; RED='#D55E00'
PBLUE='#E8F2F8'; PGREEN='#E5F5EF'; PORANGE='#FFF4D8'; PPURPLE='#F7EAF2'; PRED='#FBEAE5'

def panel(ax,l):
    ax.text(-.035,1.025,l,transform=ax.transAxes,ha='left',va='top',fontsize=9,fontweight='bold',color=INK)
def box(ax,x,y,w,h,text,fc='white',ec=MID,fs=5.8,bold=False,lw=.8):
    p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.02',facecolor=fc,edgecolor=ec,lw=lw)
    ax.add_patch(p)
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,fontweight='bold' if bold else 'normal',color=INK,linespacing=1.12,wrap=True)
    return p
def arrow(ax,a,b,c=INK,lw=.85):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=8,color=c,lw=lw,shrinkA=2,shrinkB=2))
def save(fig,name):
    fig.savefig(OUT/f'{name}.svg',bbox_inches='tight',facecolor='white')
    fig.savefig(OUT/f'{name}.pdf',bbox_inches='tight',facecolor='white')
    fig.savefig(OUT/f'{name}.png',dpi=300,bbox_inches='tight',facecolor='white')
    plt.close(fig)

fig=plt.figure(figsize=(7.0,4.45))
gs=fig.add_gridspec(2,2,height_ratios=[1.05,.95],hspace=.34,wspace=.28)

# a — system/evaluator chain
ax=fig.add_subplot(gs[0,:]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'a')
items=[(.02,.18,'History H\n(R, P, E, S, K)',PORANGE,ORANGE,'practice-grounded'),
       (.275,.18,'Current content\nCvis(H)',PBLUE,BLUE,'prespecified visible map'),
       (.53,.18,'True future response\nΨh(i)',PGREEN,GREEN,'tools + tests + terminal state'),
       (.785,.18,'Evaluator readout\nKi[Ψh(i)]',PPURPLE,PURPLE,'scores + reports')]
for x,w,t,fc,ec,sub in items:
    box(ax,x,.61,w,.19,t,fc,ec,5.7,True)
    ax.text(x+w/2,.565,sub,ha='center',va='top',fontsize=5.0,color=INK)
for i in range(3):
    arrow(ax,(items[i][0]+items[i][1],.705),(items[i+1][0],.705),INK)
ax.plot([.24,.70],[.42,.42],color=BLUE,lw=1.2)
ax.text(.47,.35,'System-side historical sufficiency',ha='center',fontsize=7,fontweight='bold',color=BLUE)
ax.text(.47,.23,'Does the visible coarse state preserve the response laws\nneeded under future interventions?',ha='center',fontsize=5.75)
ax.plot([.70,.98],[.42,.42],color=PURPLE,lw=1.2)
ax.text(.84,.35,'Evaluator-side identifiability',ha='center',fontsize=7,fontweight='bold',color=PURPLE)
ax.text(.84,.23,'Can the evaluator distinguish\nthose response laws?',ha='center',fontsize=5.75)
box(ax,.08,.025,.84,.105,'Evaluator-visible current-content equality does not establish intervention equivalence.',LIGHT,INK,6.15,True,.85)

# b — two distinct defects, with readable plain notation
ax=fig.add_subplot(gs[1,0]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'b')
ax.text(.02,.94,'Two defects, not one',fontsize=7.2,fontweight='bold')
box(ax,.03,.61,.94,.21,'System defect\nDsys(C) = supremum over equal C(h) and interventions\nof distance between true future response laws',PBLUE,BLUE,5.65,False)
box(ax,.03,.31,.94,.21,'Evaluator-visible defect\nDeval(C) = supremum over equal C(h) and interventions\nof distance between evaluator readout laws',PPURPLE,PURPLE,5.65,False)
box(ax,.09,.05,.82,.13,'Observed defect ≤ true defect.\nA converse requires a separating evaluator.',PORANGE,ORANGE,5.9,True)

# c — claim-specific calibration
ax=fig.add_subplot(gs[1,1]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'c')
ax.text(.02,.94,'Calibration is claim-specific',fontsize=7.2,fontweight='bold')
rows=[('Objective world tests','P1 / P5',PGREEN,GREEN),
      ('Ordinary behaviour','bounded behavioural null',PBLUE,BLUE),
      ('Independent A / R siblings','P2 / P3',PPURPLE,PURPLE)]
for i,(l,r,fc,ec) in enumerate(rows):
    y=.69-i*.22
    box(ax,.03,y,.43,.14,l,fc,ec,5.8,True)
    arrow(ax,(.47,y+.07),(.56,y+.07),ec)
    box(ax,.58,y,.39,.14,r,'white',ec,5.45,True)
box(ax,.05,.04,.90,.13,'Extreme or stable statistics may remain\nscientifically non-identifying.',PRED,RED,5.5,True)

save(fig,'Figure_1_System_and_Evaluator')
print('Figure 1 V3 generated')
