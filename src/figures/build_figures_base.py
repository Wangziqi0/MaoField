from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap

REPO=Path(__file__).resolve().parents[2]
SD=REPO/'data'/'processed'/'source_data'
OUT=REPO/'outputs'
FIG=OUT/'figures'; ED=OUT/'extended_data'
FIG.mkdir(parents=True,exist_ok=True); ED.mkdir(parents=True,exist_ok=True)

plt.rcParams.update({
    'font.family':'sans-serif','font.sans-serif':['Arial','Liberation Sans','DejaVu Sans'],
    'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,
    'font.size':6.5,'axes.titlesize':7.3,'axes.labelsize':6.5,
    'xtick.labelsize':5.7,'ytick.labelsize':5.7,'legend.fontsize':5.6,
    'axes.linewidth':0.6,'lines.linewidth':0.9,
    'xtick.major.width':0.6,'ytick.major.width':0.6,
    'xtick.major.size':2.4,'ytick.major.size':2.4,
    'savefig.transparent':False
})
# Okabe-Ito/Nature-safe semantics
INK='#1F2937'; MID='#64748B'; GRID='#CBD5E1'; LIGHT='#F8FAFC'; GREY='#F1F5F9'
BLUE='#0072B2'; SKY='#56B4E9'; ORANGE='#E69F00'; GREEN='#009E73'; RED='#D55E00'; PURPLE='#CC79A7'
PBLUE='#E8F2F8'; PGREEN='#E5F5EF'; PORANGE='#FFF4D8'; PRED='#FBEAE5'; PPURPLE='#F7EAF2'
WIDE=7.0

def panel(ax,l): ax.text(-.075,1.035,l,transform=ax.transAxes,ha='left',va='top',fontsize=9,fontweight='bold',color=INK)
def clean(ax,grid='x'):
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(MID); ax.spines['bottom'].set_color(MID)
    if grid: ax.grid(axis=grid,color=GRID,lw=.45,alpha=.55,zorder=0)
    ax.set_axisbelow(True)
def box(ax,x,y,w,h,text,fc='white',ec=MID,fs=5.9,bold=False,lw=.7):
    p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.02',facecolor=fc,edgecolor=ec,lw=lw)
    ax.add_patch(p); ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,fontweight='bold' if bold else 'normal',color=INK,linespacing=1.12,wrap=True); return p
def arrow(ax,a,b,c=MID,lw=.8): ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=8,color=c,lw=lw,shrinkA=2,shrinkB=2))
def save(fig,name,folder):
    fig.savefig(folder/f'{name}.svg',bbox_inches='tight',facecolor='white')
    fig.savefig(folder/f'{name}.pdf',bbox_inches='tight',facecolor='white')
    fig.savefig(folder/f'{name}.png',dpi=300,bbox_inches='tight',facecolor='white')
    plt.close(fig)

ph_eq=pd.read_csv(SD/'Phase23_Exact_Equality.csv')
ph_ctrl=pd.read_csv(SD/'Phase23_Ordinary_Controls.csv')
ph_gap=pd.read_csv(SD/'Phase23_Qwen_Channel_Gap.csv')
glm_ord=pd.read_csv(SD/'GLM_Ordinary_Criteria.csv')
glm_struct=pd.read_csv(SD/'GLM_Structure_Criterion.csv').iloc[0]
glm_direct=pd.read_csv(SD/'GLM_Direct_Contrasts.csv')
glm_sib=pd.read_csv(SD/'GLM_Sibling_Contrasts.csv')
glm_fail=pd.read_csv(SD/'GLM_Trajectory_Failures.csv')
glm_res=pd.read_csv(SD/'GLM_Resources.csv')
props=pd.read_csv(SD/'Final_Proposition_Matrix.csv')

endpoint_order=['U','A_FT','P','ORDERED_O']; elab={'U':'U','A_FT':r'$A_{FT}$','P':'P','ORDERED_O':'ordered O'}
cont_order=['S_DN_UF','C_DN_UF','C_MINUS_S','R0_DN_UF','R1_DN_UF','R1_MINUS_R0','C_DN_X','C_DN_CO','C_DN_N0','R1_DN_X','R1_DN_CO','R1_DN_N0']
clab={'S_DN_UF':'S: DN−UF','C_DN_UF':'C: DN−UF','C_MINUS_S':'C−S','R0_DN_UF':'R0: DN−UF','R1_DN_UF':'R1: DN−UF','R1_MINUS_R0':'R1−R0','C_DN_X':'C: DN−X','C_DN_CO':'C: DN−CO','C_DN_N0':'C: DN−N0','R1_DN_X':'R1: DN−X','R1_DN_CO':'R1: DN−CO','R1_DN_N0':'R1: DN−N0'}

# Figure 1
fig=plt.figure(figsize=(WIDE,4.45)); gs=fig.add_gridspec(2,2,height_ratios=[1.05,.95],hspace=.34,wspace=.28)
ax=fig.add_subplot(gs[0,:]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'a')
items=[(.02,.18,'History H\n(R, P, E, S, K)',PORANGE,ORANGE,'practice-grounded'),(.275,.18,'Current state\nC(H)',PBLUE,BLUE,'typed atoms + conclusion'),(.53,.18,'Future response\n'+r'$\Psi_h(i)$',PGREEN,GREEN,'tools + tests + terminal state'),(.785,.18,'Evaluator readout\n'+r'$K_{i\#}\Psi_h(i)$',PPURPLE,PURPLE,'scores + reports')]
for x,w,t,fc,ec,sub in items:
    box(ax,x,.61,w,.19,t,fc,ec,5.8,True)
    ax.text(x+w/2,.565,sub,ha='center',va='top',fontsize=5.0,color=INK)
for i in range(3): arrow(ax,(items[i][0]+items[i][1],.705),(items[i+1][0],.705),INK)
ax.plot([.24,.70],[.42,.42],color=BLUE,lw=1.2); ax.text(.47,.35,'System-side historical sufficiency',ha='center',fontsize=7,fontweight='bold',color=BLUE); ax.text(.47,.23,'Does C(H) preserve the response laws\nneeded under future interventions?',ha='center',fontsize=5.9)
ax.plot([.70,.98],[.42,.42],color=PURPLE,lw=1.2); ax.text(.84,.35,'Evaluator-side identifiability',ha='center',fontsize=7,fontweight='bold',color=PURPLE); ax.text(.84,.23,'Can the evaluator distinguish\nthose response laws?',ha='center',fontsize=5.9)
box(ax,.10,.025,.80,.105,'Equality of current evaluator outputs does not establish equality under future intervention.',LIGHT,INK,6.25,True,.85)
ax=fig.add_subplot(gs[1,0]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'b'); ax.text(.02,.94,'Two defects, not one',fontsize=7.2,fontweight='bold')
box(ax,.03,.61,.94,.21,r'System: $D_{\mathcal{I}}(C)=\sup_{C(h)=C(h^{\prime})}\sup_i d_Y(\Psi_h(i),\Psi_{h^{\prime}}(i))$',PBLUE,BLUE,6.0)
box(ax,.03,.31,.94,.21,r'Evaluator: $D^K_{\mathcal{I}}(C)=\sup_{C(h)=C(h^{\prime})}\sup_i d_Z(K_{i\#}\Psi_h(i),K_{i\#}\Psi_{h^{\prime}}(i))$',PPURPLE,PURPLE,5.75)
box(ax,.12,.05,.76,.13,r'$D^K_{\mathcal{I}}(C)\leq D_{\mathcal{I}}(C)$; the converse needs a separating evaluator.',PORANGE,ORANGE,5.95,True)
ax=fig.add_subplot(gs[1,1]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'c'); ax.text(.02,.94,'Calibration is claim-specific',fontsize=7.2,fontweight='bold')
rows=[('Objective world tests','P1 / P5',PGREEN,GREEN),('Ordinary behaviour','bounded behavioural null',PBLUE,BLUE),('Independent A / R siblings','P2 / P3',PPURPLE,PURPLE)]
for i,(l,r,fc,ec) in enumerate(rows):
    y=.69-i*.22; box(ax,.03,y,.43,.14,l,fc,ec,5.8,True); arrow(ax,(.47,y+.07),(.56,y+.07),ec); box(ax,.58,y,.39,.14,r,'white',ec,5.45,True)
box(ax,.05,.04,.90,.13,'Extreme or stable statistics may remain\nscientifically non-identifying.',PRED,RED,5.5,True)
save(fig,'Figure_1_System_and_Evaluator',FIG)

# Figure 2
fig=plt.figure(figsize=(WIDE,5.25)); gs=fig.add_gridspec(2,2,height_ratios=[.95,1.1],hspace=.32,wspace=.30)
ax=fig.add_subplot(gs[0,:]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'a')
pipe=[(.01,.17,'Predecessor\npractice',PORANGE,ORANGE),(.215,.17,'History carrier\n(R, P, E, S, K)',PBLUE,BLUE),(.42,.20,'Randomised history\nDN · UF · X · CO · N0',PPURPLE,PURPLE),(.655,.15,'Clean successor\nfresh, arm-blind',PGREEN,GREEN),(.84,.15,'Future practice\nprobe → action → tests',PORANGE,ORANGE)]
for x,w,t,fc,ec in pipe: box(ax,x,.59,w,.22,t,fc,ec,5.8,True)
for i in range(4): arrow(ax,(pipe[i][0]+pipe[i][1],.70),(pipe[i+1][0],.70),INK)
box(ax,.03,.29,.44,.14,'Matched before response\ntyped atoms, conclusion and future substrate',LIGHT,MID,5.65)
box(ax,.53,.29,.44,.14,'Arm-invariant outcome\nrepository, catalogues, tests and scorers',LIGHT,MID,5.65)
box(ax,.24,.055,.52,.10,'Only the registered practice-grounded relation changes.',PORANGE,ORANGE,6.0,True)
ax=fig.add_subplot(gs[1,0]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'b'); ax.text(.02,.96,'Five arms and four future duties',fontsize=7.2,fontweight='bold')
arms=[('DN',GREEN),('UF',BLUE),('X',PURPLE),('CO',ORANGE),('N0',MID)]
for i,(a,c) in enumerate(arms):
    x=.012+i*.198
    box(ax,x,.80,.182,.09,a,'white',c,5.9,True)
ax.text(.50,.735,'DN complete relation   ·   UF rewired relation   ·   X wrong grounding',ha='center',va='center',fontsize=4.95,color=INK)
ax.text(.50,.690,'CO conclusion only   ·   N0 no history',ha='center',va='center',fontsize=4.95,color=INK)
for i,(code,name,duty) in enumerate([('S','Stable','equivalence'),('C','Continuity','history-specific benefit'),('R0','Reopening inactive','no premature reopening'),('R1','Reopening active','selective reopening')]):
    y=.54-i*.125; box(ax,.03,y,.15,.085,code,PBLUE,BLUE,5.8,True); ax.text(.215,y+.043,name,va='center',fontsize=5.65,fontweight='bold'); ax.text(.57,y+.043,duty,va='center',fontsize=5.35)
box(ax,.025,.010,.95,.11,'Full HFI is an intersection.\nNo endpoint, cell or model rescues a failed constituent.',PRED,RED,4.95,True)
ax=fig.add_subplot(gs[1,1]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'c'); ax.text(.02,.96,'Endpoint hierarchy and nonblocking controls',fontsize=7.2,fontweight='bold')
rows=[('Primary objective','U: sealed hidden-test utility',PGREEN,GREEN),('Objective secondary',r'$A_{FT}$, P, ordered O, resources and trajectory',PBLUE,BLUE),('Mechanism siblings',r'$A_{SIB}$ and R; both valid for P2/P3',PPURPLE,PURPLE),('Auxiliary diagnostics','K1, DSQ and interface checks;\nnever a Direct gate',PORANGE,ORANGE)]
for i,(l,r,fc,ec) in enumerate(rows):
    y=.77-i*.17; box(ax,.025,y,.34,.115,l,fc,ec,5.25,True); box(ax,.395,y,.58,.115,r,'white',ec,5.15)
box(ax,.035,.025,.93,.12,'Main-96 froze before sealed-32 was read.\nNOT_IDENTIFIED is never a strict null.',PORANGE,ORANGE,5.35,True)
save(fig,'Figure_2_Causal_Protocol',FIG)

# Figure 3
fig=plt.figure(figsize=(WIDE,5.15)); gs=fig.add_gridspec(2,2,hspace=.44,wspace=.34)
ax=fig.add_subplot(gs[0,0]); panel(ax,'a')
models=['QWEN3_14B','PHI4','QWEN3_8B_SECONDARY']; mlab=['Qwen3-14B','Phi-4','Qwen3-8B']; cols=[]
for ep in endpoint_order: cols += [(ep,'main'),(ep,'sealed')]
ax.imshow(np.zeros((3,8)),cmap=ListedColormap([PBLUE]),vmin=0,vmax=1,aspect='auto')
for i in range(3):
    for j in range(8): ax.text(j,i,'0',ha='center',va='center',fontsize=6.0,color=BLUE,fontweight='bold')
ax.set_yticks(range(3),mlab); ax.set_xticks(range(8),['main','sealed']*4,rotation=45,ha='right')
for k,ep in enumerate(endpoint_order): ax.text(k*2+.5,-.83,elab[ep],ha='center',fontsize=6.2,fontweight='bold',clip_on=False)
for k in range(1,4): ax.axvline(k*2-.5,color='white',lw=2)
ax.tick_params(length=0); [s.set_visible(False) for s in ax.spines.values()]; ax.set_title('Finite-manifest exact equality',loc='left',pad=9)
ax.set_xlabel('Every registered contrast and reported interval centre was 0')
ax=fig.add_subplot(gs[0,1]); panel(ax,'b')
order=['QWEN3_14B','MISTRAL_NEMO','PHI4','QWEN3_8B_SECONDARY','DS_V4_FLASH_NONTHINKING','DS_V4_FLASH_THINKING_HIGH']; lab=['Qwen3-14B','Mistral-Nemo','Phi-4','Qwen3-8B','DeepSeek NT','DeepSeek TH']; d=ph_ctrl.set_index('condition').loc[order]; y=np.arange(6)
ax.hlines(y,0,16,color=GRID,lw=1); ax.scatter(d.ordinary_successes,y,s=28,facecolor='white',edgecolor=RED,lw=1.2,zorder=3)
for yi in y: ax.text(.35,yi,'0/16',va='center',fontsize=5.7,color=RED)
ax.set_xlim(-.5,16.5); ax.set_yticks(y,lab); ax.invert_yaxis(); ax.set_xlabel('Ordinary-control successes'); ax.set_title('Operating range was not established',loc='left'); clean(ax,'x')
ax=fig.add_subplot(gs[1,0]); panel(ax,'c')
for idx,row in ph_gap.iterrows():
    yv=1-idx; col,mk=(BLUE,'o') if row.stratum=='main48' else (ORANGE,'s'); ax.errorbar(row.A_SIB_minus_R,yv,xerr=[[row.A_SIB_minus_R-row.ci_lower],[row.ci_upper-row.A_SIB_minus_R]],fmt=mk,color=col,ms=5,capsize=3,lw=1)
ax.axvline(0,color=INK,lw=.7); ax.axvline(-1,color=GRID,lw=.7,ls='--'); ax.set_yticks([1,0],['main-48','sealed-16']); ax.set_xlim(-1.12,.08); ax.set_xlabel(r'$A_{SIB}-R$ (simultaneous interval)'); ax.set_title('Near-saturated apparent channel gap',loc='left'); clean(ax,'x')
ax=fig.add_subplot(gs[1,1]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'d'); ax.text(.02,.96,'Frozen adjudication',fontsize=7.2,fontweight='bold')
box(ax,.03,.70,.42,.15,'Action criterion\n0/16',PRED,RED,6.0,True); box(ax,.55,.70,.42,.15,'Structure criterion\n0/48',PRED,RED,6.0,True); arrow(ax,(.24,.68),(.44,.49),RED); arrow(ax,(.76,.68),(.56,.49),RED)
box(ax,.22,.36,.56,.15,'P2/P3 dual-validity condition failed',PORANGE,ORANGE,6.0,True); arrow(ax,(.50,.34),(.50,.22),INK)
box(ax,.13,.06,.74,.14,'APPARENT GAP — NOT A CAUSAL DISSOCIATION',PPURPLE,PURPLE,5.85,True)
save(fig,'Figure_3_Phase23_Opposed_Extremes',FIG)

# helper forest
def forest(ax,df,title,channels=None):
    for i,c in enumerate(cont_order):
        yv=len(cont_order)-1-i
        for st,off,col,mk in [('main96',.13,BLUE,'o'),('sealed32',-.13,ORANGE,'s')]:
            r=df[(df.stratum==st)&(df.contrast==c)]
            if r.empty: continue
            r=r.iloc[0]; ax.errorbar(r.estimate,yv+off,xerr=[[max(0,r.estimate-r.missing_lower)],[max(0,r.missing_upper-r.estimate)]],fmt=mk,color=col,ms=3,capsize=2,lw=.8)
    ax.axvspan(-.10,.10,color=GREY,zorder=0); ax.axvline(0,color=INK,lw=.7); ax.axvline(.10,color=MID,lw=.55,ls='--'); ax.axvline(.15,color=MID,lw=.55,ls=':')
    ax.set_yticks(range(len(cont_order)),[clab[c] for c in cont_order[::-1]]); ax.set_xlim(-.36,.36); ax.set_title(title,loc='left'); ax.set_xlabel('Contrast; bars = typed-missingness bounds'); clean(ax,'x')

# Figure 4
fig=plt.figure(figsize=(WIDE,5.25)); gs=fig.add_gridspec(2,2,height_ratios=[1.08,.92],hspace=.45,wspace=.35)
ax=fig.add_subplot(gs[0,0]); panel(ax,'a'); o=['P','ORDERED_O','A_FT','U']; do=glm_ord.set_index('endpoint').loc[o]; x=np.arange(4); ax.bar(x,do.successes,color=GREEN,width=.62)
for i,(v,t) in enumerate(zip(do.successes,do.threshold)): ax.hlines(t,i-.34,i+.34,color=INK,lw=1); ax.text(i,v+.8,f'{int(v)}/32',ha='center',fontsize=5.8,fontweight='bold')
ax.set_xticks(x,[elab[e] for e in o]); ax.set_ylim(0,34); ax.set_ylabel('Successful ordinary controls'); ax.set_title('Behavioural operating-range controls passed',loc='left'); clean(ax,'y')
ax=fig.add_subplot(gs[0,1]); panel(ax,'b'); forest(ax,glm_direct[glm_direct.endpoint=='U'],'No complete HFI signature or bounded zero')
ax.legend(handles=[Line2D([0],[0],marker='o',color=BLUE,lw=0,label='main-96'),Line2D([0],[0],marker='s',color=ORANGE,lw=0,label='sealed-32')],frameon=False,loc='lower right')
ax=fig.add_subplot(gs[1,0]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'c'); ax.text(.02,.97,'Registered terminal branches',fontsize=7.2,fontweight='bold')
ax.text(.02,.875,'Structure criterion: 31/32, but one renderer mismatch',fontsize=5.1,color=PURPLE)
ax.text(.02,.835,'and one typed missing made the frozen criterion invalid.',fontsize=5.1,color=PURPLE)
branches=[('P1 Direct HFI','not supported',RED,PRED),('P5 finite nonclosure','not established',ORANGE,PORANGE),('Bounded objective zero','not established',ORANGE,PORANGE),('P2 action–structure','not identified',PURPLE,PPURPLE),('P3 structure–operation','not identified',PURPLE,PPURPLE)]
for i,(name,status,c,fc) in enumerate(branches):
    y=.68-i*.12; box(ax,.03,y,.58,.08,name,'white',MID,5.25); box(ax,.66,y,.31,.08,status,fc,c,5.15,True)
box(ax,.035,.015,.93,.105,'Passing ordinary behaviour excluded global incapacity;\nit did not validate historical or structural claims.',PGREEN,GREEN,5.1,True)
ax=fig.add_subplot(gs[1,1]); panel(ax,'d'); piv=glm_fail.pivot_table(index='failure_code',columns='stratum',values='count',aggfunc='sum',fill_value=0); piv['total']=piv.sum(axis=1); piv=piv.sort_values('total').tail(7); y=np.arange(len(piv)); h=.32
labels={'TOOL_NOT_ALLOWED_THIS_TURN':'Tool-call order','Y_MISSING_TRANSPORT':'Transport missing','SCHEMA_VIOLATION':'Schema violation','NON_JSON_CONTENT':'Non-JSON content','ARGUMENT_SCHEMA_VIOLATION':'Argument schema','Y_MISSING_TRANSPORT_HTTP_500':'HTTP 500','ACTION_NOT_IN_CATALOGUE':'Action catalogue','RECOVERED_UNCOMMITTED_TYPED_FAILURE_METADATA_PARTIAL':'Recovered metadata','Y_MISSING_TRANSPORT_HTTP_400':'HTTP 400'}
ax.barh(y+h/2,piv.get('main96',0),height=h,color=BLUE,label='main-96'); ax.barh(y-h/2,piv.get('sealed32',0),height=h,color=ORANGE,label='sealed-32'); ax.set_yticks(y,[labels.get(v,v.replace('_',' ').title()) for v in piv.index]); ax.set_xlabel('Typed failure events (events may co-occur)'); ax.set_title('Execution remained partially missing and heterogeneous',loc='left'); ax.legend(frameon=False,loc='lower right'); clean(ax,'x')
save(fig,'Figure_4_GLM_Terminal_Branch',FIG)

# Figure 5
fig=plt.figure(figsize=(WIDE,5.0)); gs=fig.add_gridspec(2,2,height_ratios=[.9,1.1],hspace=.34,wspace=.30)
ax=fig.add_subplot(gs[0,:]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'a')
obs=[('Phase 23\nexact equality',PBLUE,BLUE),('Phase 23\nnear-saturated gap',PPURPLE,PURPLE),('GLM ordinary\nbehaviour valid',PGREEN,GREEN),('GLM structure\ncriterion invalid',PRED,RED)]
for i,(t,fc,ec) in enumerate(obs):
    x=.02+i*.24; box(ax,x,.64,.20,.20,t,fc,ec,5.8,True); arrow(ax,(x+.10,.62),(.50,.44),ec,.7)
box(ax,.31,.29,.38,.17,'Claim-specific identification boundary\ncalibration supports only the response family it exercises',PORANGE,ORANGE,5.9,True); arrow(ax,(.50,.27),(.50,.16),INK)
box(ax,.10,.02,.80,.12,'Current or evaluator equality does not establish equality under future intervention.',LIGHT,INK,6.2,True,.85)
ax=fig.add_subplot(gs[1,0]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'b'); ax.text(.02,.96,'Final proposition matrix',fontsize=7.2,fontweight='bold')
colors={'PARTIAL':SKY,'NOT_SUPPORTED; ABSENCE NOT IDENTIFIED':RED,'NOT_IDENTIFIED':PURPLE,'NOT_ESTABLISHED':ORANGE,'PARTIAL—STRENGTHENED':SKY,'SUPPORTED WITH FINITE-PROTOCOL CEILING':GREEN,'SUPPORTED AS CLAIM-SPECIFIC CALIBRATION RESULT':GREEN,'SUPPORTED AS IDENTIFICATION PRINCIPLE':GREEN}
show=props[['proposition','status']]
for i,(_,r) in enumerate(show.iterrows()):
    y=.84-i*.075; c=colors.get(r.status,MID); box(ax,.02,y,.17,.055,r.proposition,'white',c,5.25,True); box(ax,.23,y,.74,.055,str(r.status).replace('; ',';\n'),GREY,c,4.8,True)
ax=fig.add_subplot(gs[1,1]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'c'); ax.text(.02,.97,'What the GLM replication changed',fontsize=7.2,fontweight='bold')
box(ax,.02,.70,.43,.17,'Before GLM\nPhase 23 ordinary\ncontrols failed',PRED,RED,5.4,True); arrow(ax,(.46,.785),(.53,.785),INK); box(ax,.55,.70,.43,.17,'GLM\nall four behavioural\ncontrols passed',PGREEN,GREEN,5.4,True)
box(ax,.06,.45,.88,.13,'Global incapacity became an insufficient explanation.',PBLUE,BLUE,5.7,True); box(ax,.06,.25,.88,.14,'Still unresolved: full historical signature,\nbounded zero and criterion-valid structure.',PORANGE,ORANGE,5.5,True); box(ax,.06,.04,.88,.14,'Calibration is endpoint- and claim-specific,\nnot a transferable certificate.',PPURPLE,PURPLE,5.7,True)
save(fig,'Figure_5_Integrated_Identification_Boundary',FIG)

# Extended Data 1
fig=plt.figure(figsize=(WIDE,4.8)); ax=fig.add_subplot(111); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'a')
conditions=['QWEN3_14B','MISTRAL_NEMO','PHI4','QWEN3_8B_SECONDARY','DS_V4_FLASH_NONTHINKING','DS_V4_FLASH_THINKING_HIGH']; labels=['Qwen3-14B','Mistral-Nemo','Phi-4','Qwen3-8B','DeepSeek NT','DeepSeek TH']; cols=['Objective behaviour','Ordinary control','Structure channel','Final adjudication']; xs=[.18,.37,.55,.75]; ws=[.17,.16,.18,.22]
cells={
'QWEN3_14B':['exact equality','0/16 invalid','gap; criterion invalid','operating range unresolved'],
'MISTRAL_NEMO':['non-evaluable','0/16 not identified','R not identified','objective non-evaluable'],
'PHI4':['exact equality','0/16 invalid','strict-zero; invalid','operating range unresolved'],
'QWEN3_8B_SECONDARY':['exact equality','0/16 invalid','strict-zero; invalid','operating range unresolved'],
'DS_V4_FLASH_NONTHINKING':['non-evaluable','0/16 not identified','R not identified','objective non-evaluable'],
'DS_V4_FLASH_THINKING_HIGH':['non-evaluable','0/16 not identified','R not identified','objective non-evaluable']}
fc={'exact equality':PBLUE,'non-evaluable':GREY,'0/16 invalid':PRED,'0/16 not identified':PORANGE,'gap; criterion invalid':PPURPLE,'strict-zero; invalid':PPURPLE,'R not identified':PORANGE,'operating range unresolved':PORANGE,'objective non-evaluable':GREY}; ec={'exact equality':BLUE,'non-evaluable':MID,'0/16 invalid':RED,'0/16 not identified':ORANGE,'gap; criterion invalid':PURPLE,'strict-zero; invalid':PURPLE,'R not identified':ORANGE,'operating range unresolved':ORANGE,'objective non-evaluable':MID}
for j,c in enumerate(cols): ax.text(xs[j]+ws[j]/2,.92,c,ha='center',fontsize=6.1,fontweight='bold')
for i,(cond,lab) in enumerate(zip(conditions,labels)):
    y=.79-i*.125; ax.text(.02,y+.045,lab,va='center',fontsize=6.0,fontweight='bold')
    for j,val in enumerate(cells[cond]): box(ax,xs[j],y,ws[j],.09,val,fc[val],ec[val],5.05,True)
ax.text(.02,.03,'Frozen condition labels; no cross-model pooling.',fontsize=5.9)
save(fig,'Extended_Data_Figure_1_Phase23_Condition_Matrix',ED)

# ED2 direct forest
fig=plt.figure(figsize=(WIDE,6.1)); gs=fig.add_gridspec(2,2,hspace=.48,wspace=.30)
for k,ep in enumerate(endpoint_order):
    ax=fig.add_subplot(gs[k//2,k%2]); panel(ax,chr(97+k)); forest(ax,glm_direct[glm_direct.endpoint==ep],elab[ep])
fig.legend(handles=[Line2D([0],[0],marker='o',color=BLUE,lw=0,label='main'),Line2D([0],[0],marker='s',color=ORANGE,lw=0,label='sealed')],loc='upper center',ncol=2,frameon=False,bbox_to_anchor=(.5,.997))
save(fig,'Extended_Data_Figure_2_GLM_Direct_Forest',ED)

# ED3 siblings
fig=plt.figure(figsize=(WIDE,3.7)); gs=fig.add_gridspec(1,3,wspace=.35)
for k,(ch,title) in enumerate([('A_SIB',r'$A_{SIB}$'),('R','R'),('R_MINUS_A',r'$R-A_{SIB}$')]):
    ax=fig.add_subplot(gs[0,k]); panel(ax,chr(97+k)); q=glm_sib[glm_sib.channel==ch]; cs=[c for c in cont_order if c in set(q.contrast)]
    for i,c in enumerate(cs):
        yv=len(cs)-1-i
        for st,off,col,mk in [('main48',.12,BLUE,'o'),('sealed16',-.12,ORANGE,'s')]:
            r=q[(q.stratum==st)&(q.contrast==c)]
            if r.empty: continue
            r=r.iloc[0]; ax.errorbar(r.estimate,yv+off,xerr=[[max(0,r.estimate-r.missing_lower)],[max(0,r.missing_upper-r.estimate)]],fmt=mk,color=col,ms=2.7,capsize=1.7,lw=.7)
    ax.axvline(0,color=INK,lw=.65); ax.set_yticks(range(len(cs)),[clab[c] for c in cs[::-1]]); ax.set_xlim(-1.05,1.05); ax.set_title(title,loc='left'); ax.set_xlabel('Contrast; bars = bounds'); clean(ax,'x')
fig.legend(handles=[Line2D([0],[0],marker='o',color=BLUE,lw=0,label='main'),Line2D([0],[0],marker='s',color=ORANGE,lw=0,label='sealed')],loc='upper center',ncol=2,frameon=False,bbox_to_anchor=(.5,.997))
save(fig,'Extended_Data_Figure_3_GLM_Siblings',ED)

# ED4 failures
fig=plt.figure(figsize=(WIDE,3.55)); gs=fig.add_gridspec(1,2,wspace=.42); labels_f={'TOOL_NOT_ALLOWED_THIS_TURN':'Tool-call order','Y_MISSING_TRANSPORT':'Transport missing','SCHEMA_VIOLATION':'Schema violation','NON_JSON_CONTENT':'Non-JSON content','ARGUMENT_SCHEMA_VIOLATION':'Argument schema','Y_MISSING_TRANSPORT_HTTP_500':'HTTP 500','ACTION_NOT_IN_CATALOGUE':'Action catalogue','RECOVERED_UNCOMMITTED_TYPED_FAILURE_METADATA_PARTIAL':'Recovered metadata','Y_MISSING_TRANSPORT_HTTP_400':'HTTP 400'}
for k,st in enumerate(['main96','sealed32']):
    ax=fig.add_subplot(gs[0,k]); panel(ax,chr(97+k)); d=glm_fail[glm_fail.stratum==st].sort_values('count').tail(8); ax.barh(range(len(d)),d['count'],color=BLUE if st=='main96' else ORANGE); ax.set_yticks(range(len(d)),[labels_f.get(v,v.replace('_',' ').title()) for v in d.failure_code]); ax.set_xlabel('Typed failure events'); ax.set_title('main-96' if st=='main96' else 'sealed-32',loc='left'); clean(ax,'x')
fig.text(.5,.015,'Events may co-occur within a registered row; counts do not replace ITT bounds.',ha='center',fontsize=5.7)
save(fig,'Extended_Data_Figure_4_GLM_Failures',ED)

# ED5 resources
fig=plt.figure(figsize=(WIDE,2.75)); gs=fig.add_gridspec(1,3,wspace=.38)
for k,(col,title) in enumerate([('raw_calls_sum','Raw provider calls'),('tool_cost_sum','Tool-cost units'),('normalized_budget_ratio_mean','Mean normalised budget')]):
    ax=fig.add_subplot(gs[0,k]); panel(ax,chr(97+k)); vals=[glm_res.loc[glm_res.stratum=='main96',col].iloc[0],glm_res.loc[glm_res.stratum=='sealed32',col].iloc[0]]; ax.bar([0,1],vals,color=[BLUE,ORANGE],width=.62); ax.set_xticks([0,1],['main-96','sealed-32']); ax.set_title(title,loc='left'); clean(ax,'y')
save(fig,'Extended_Data_Figure_5_GLM_Resources',ED)

# ED6 lineage
fig=plt.figure(figsize=(WIDE,2.65)); ax=fig.add_subplot(111); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'a')
steps=[('R4','excluded\nincomplete runtime',PORANGE,ORANGE),('R5','excluded\nterminated preimage',PORANGE,ORANGE),('R6 base','immutable\nscientific prefix',PBLUE,BLUE),('R6R1C1','interrupted\nno replay',PGREEN,GREEN),('R6R1C2','terminal pass\n18,156 attempts',PGREEN,GREEN)]
for i,(a,b,fc0,ec0) in enumerate(steps):
    x=.02+i*.195; box(ax,x,.51,.17,.22,a+'\n'+b,fc0,ec0,5.55,True)
    if i<4: arrow(ax,(x+.17,.62),(x+.195,.62),INK)
box(ax,.06,.16,.88,.15,'Science-bearing bytes were unchanged; provider calls were not replayed; main-96 froze before sealed-32.',LIGHT,INK,5.9,True)
save(fig,'Extended_Data_Figure_6_GLM_Lineage',ED)

# ED7 counterexample
fig=plt.figure(figsize=(WIDE,3.0)); ax=fig.add_subplot(111); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'a')
box(ax,.04,.61,.38,.20,'Perfect structure recovery\nDN “true” → correct\nUF “false” → correct',PGREEN,GREEN,5.9,True); box(ax,.58,.61,.38,.20,'Arm-blind constant “true”\nDN correct\nUF incorrect',PRED,RED,5.9,True); arrow(ax,(.23,.59),(.23,.40),GREEN,.9); arrow(ax,(.77,.59),(.77,.40),RED,.9); box(ax,.10,.25,.26,.13,r'$R_{DN}=1,\ R_{UF}=1$'+'\ncontrast = 0',PBLUE,BLUE,6.0,True); box(ax,.64,.25,.26,.13,r'$R_{DN}=1,\ R_{UF}=0$'+'\ncontrast = 1',PPURPLE,PURPLE,6.0,True); box(ax,.12,.04,.76,.12,'A zero accuracy contrast need not imply absent structure; a maximal contrast need not imply represented structure.',LIGHT,INK,5.9,True)
save(fig,'Extended_Data_Figure_7_R_Estimand_Counterexample',ED)

# ED8 result tree
fig=plt.figure(figsize=(WIDE,3.7)); ax=fig.add_subplot(111); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); panel(ax,'a')
for i,(t,fc0,ec0) in enumerate([('Execution / custody valid?',GREY,MID),('Objective behaviour evaluable?',PBLUE,BLUE),('Ordinary behaviour calibrated?',PGREEN,GREEN),('Structure criterion valid?',PPURPLE,PURPLE)]):
    x=.02+i*.245; box(ax,x,.78,.21,.12,t,fc0,ec0,5.35,True)
    if i<3: arrow(ax,(x+.21,.84),(x+.245,.84),INK,.7)
box(ax,.03,.47,.27,.14,'Direct full signature + calibration\n→ P1 / P5 candidate',PGREEN,GREEN,5.5,True); box(ax,.365,.47,.27,.14,'Direct strict zero + valid calibration\n→ bounded-zero candidate',PBLUE,BLUE,5.4,True); box(ax,.70,.47,.27,.14,'Valid A and R + positive/strict-null + gap\n→ P2/P3 candidate',PPURPLE,PURPLE,5.3,True)
for x in [.165,.50,.835]: arrow(ax,(x,.45),(.50,.28),INK,.7)
box(ax,.19,.12,.62,.14,'Otherwise: mixed/inconclusive, objective non-evaluable, or measurement/structure boundary.\nNOT_IDENTIFIED is never a strict null.',PORANGE,ORANGE,5.65,True)
save(fig,'Extended_Data_Figure_8_Result_Tree',ED)

manifest=[]
for folder in [FIG,ED]:
    for p in sorted(folder.glob('*')):
        manifest.append({'file':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(OUT/'FIGURE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('generated',len(manifest),'figure files')

