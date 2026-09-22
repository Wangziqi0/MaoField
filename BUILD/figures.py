"""Build V6 scientific figures for MaoField Nature manuscript.
No new model/API/GPU experiments are executed.
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, csv, math, hashlib, textwrap, warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.ticker import FuncFormatter, FixedLocator
from matplotlib import font_manager
from PIL import Image

# Palette chosen for Nature-style clarity and grayscale separability.
BLUE = '#1f77b4'
ORANGE = '#d95f02'
INK = '#20252B'
GREY = '#6B7178'
MID = '#A9B1B7'
LIGHT = '#E7EBEF'
WHITE = '#FFFFFF'
FONT = 'DejaVu Sans'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': [FONT, 'Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 6.6,
    'text.color': INK,
    'axes.labelcolor': INK,
    'xtick.color': INK,
    'ytick.color': INK,
    'mathtext.fontset': 'custom',
    'mathtext.rm': FONT,
    'mathtext.it': FONT + ':italic',
    'mathtext.bf': FONT + ':bold',
    'mathtext.sf': FONT,
    'mathtext.fallback': 'stix',
    'svg.fonttype': 'none',
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'axes.linewidth': .6,
    'xtick.major.width': .6,
    'ytick.major.width': .6,
    'xtick.major.size': 2.5,
    'ytick.major.size': 2.5,
    'savefig.facecolor': WHITE,
    'legend.frameon': False,
})

ROOT: Path | None = None
LOG = []


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_doc(root: Path, name: str) -> Path:
    for folder in ('SUBMISSION', 'DOCUMENTATION'):
        p = root / folder / name
        if p.is_file():
            return p
    raise FileNotFoundError(name)


def canvas(height_mm: float):
    fig = plt.figure(figsize=(180/25.4, height_mm/25.4), facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 180)
    ax.set_ylim(height_mm, 0)
    ax.axis('off')
    return fig, ax


def text(ax, x, y, s, sz=6.6, bold=False, ha='left', va='center', color=INK, **kw):
    return ax.text(x, y, s, fontsize=max(sz, 7.4) if '$' in s else sz, fontweight='bold' if bold else 'normal',
                   ha=ha, va=va, color=color, **kw)


def panel_label(ax, x, y, letter, title):
    text(ax, x, y, letter, sz=8.0, bold=True)
    text(ax, x+7, y, title, sz=7.0, bold=True)


def rule(ax, x1, y1, x2, y2, color=LIGHT, lw=.55, ls='-'):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls)


def arrow(ax, start, end, color=GREY, lw=.8, ls='-', connectionstyle='arc3,rad=0', ms=7):
    patch = FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=ms,
                            linewidth=lw, linestyle=ls, color=color,
                            connectionstyle=connectionstyle)
    ax.add_patch(patch)
    return patch


def box(ax, x, y, w, h, title, sub=None, edge=GREY, dashed=False, fill=WHITE, title_size=6.8):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge,
                           linewidth=.55, linestyle='--' if dashed else '-'))
    text(ax, x+w/2, y+(h*.38 if sub else h/2), title, sz=title_size, bold=True, ha='center')
    if sub:
        text(ax, x+w/2, y+h*.72, sub, sz=6.2, ha='center')


def annotate_axis_zero(ax, ymin, ymax):
    ax.axhline(0, color=INK, lw=.6)
    ax.set_ylim(ymin, ymax)


def save(fig, name, root: Path, claims, inputs):
    out = root / 'FIGURES'
    out.mkdir(exist_ok=True)
    # Math text and logarithmic tick scripts must remain readable at final size.
    from matplotlib.text import Text
    for artist in fig.findobj(Text):
        if '$' in artist.get_text():
            artist.set_fontsize(max(artist.get_fontsize(), 7.4))
    fig.canvas.draw()
    fig.savefig(out / f'{name}.svg')
    # Preserve editable Unicode radical glyphs in SVG viewers without STIX installed.
    svg_path = out / f'{name}.svg'
    svg_path.write_text(svg_path.read_text().replace("font-family: 'STIXGeneral'", "font-family: 'DejaVu Sans'"))
    fig.savefig(out / f'{name}.pdf', metadata={'Creator': 'MaoField V8 scientific figure build'})
    fig.savefig(out / f'{name}.png', dpi=600)
    fig.savefig(out / f'{name}.tiff', dpi=600, pil_kwargs={'compression': 'tiff_lzw'})
    gray_dir = root / 'QA/FIGURE_GRAYSCALE'
    gray_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(out / f'{name}.png') as im:
        im.convert('L').save(gray_dir / f'{name}.png')
    widths = fig.get_size_inches() * 25.4
    LOG.append({
        'figure': name,
        'width_mm': float(widths[0]),
        'height_mm': float(widths[1]),
        'body_font_pt': [5.4, 7.0],
        'panel_font_pt': 8,
        'font_family': FONT,
        'source_inputs': [{'path': str(p.relative_to(root)), 'sha256': sha(p)} for p in inputs],
        'claims': claims,
        'formats': ['svg', 'pdf', 'png', 'tiff'],
        'pdf_sha256': sha(out / f'{name}.pdf'),
        'png_sha256': sha(out / f'{name}.png')
    })
    plt.close(fig)


def fig1(root: Path):
    fig, ax = canvas(136)
    ax.set_ylim(158, 0)
    panel_label(ax, 4, 6, 'a', 'A specified present readout is not sufficient')
    rule(ax, 4, 13, 176, 13, color=INK, lw=.7)
    text(ax, 90, 18, 'Same specified present readout', sz=8.6, bold=True, ha='center')
    text(ax, 90, 24, r'$r$ is matched, while complete state, target and required correction differ', sz=6.3, ha='center')

    # central readout node
    box(ax, 73, 29, 34, 12, r'Current readout  $r$', sub='same declared residual', edge=INK, title_size=7.2)

    # two states
    box(ax, 16, 47, 54, 24, 'State +', sub=r'$u=+v,\, z_+=1+v,\, p_+=z_+^2+r$', edge=BLUE)
    box(ax, 110, 47, 54, 24, 'State −', sub=r'$u=-v,\, z_-=1-v,\, p_-=z_-^2+r$', edge=ORANGE)
    arrow(ax, (90, 41), (43, 47), color=BLUE)
    arrow(ax, (90, 41), (137, 47), color=ORANGE)
    text(ax, 43, 82, r'$E_+(g)=g^2+2(1+v)g-r$', sz=7.0, ha='center')
    text(ax, 137, 82, r'$E_-(g)=g^2+2(1-v)g-r$', sz=7.0, ha='center')
    text(ax, 90, 92, 'One readout-only action g cannot close both targets', sz=7.0, bold=True, ha='center')
    text(ax, 90, 98, 'Compact retention of $(r,u)$ restores sufficiency', sz=6.5, ha='center')

    rule(ax, 4, 105, 176, 105, color=LIGHT, lw=.8)
    panel_label(ax, 4, 112, 'b', 'Two recorded entry points into common practice')
    box(ax, 10, 118, 75, 12, 'Recorded coefficient continuation',
        sub='formation → feedback revision → inherited reuse', edge=BLUE, title_size=6.8)
    box(ax, 95, 118, 75, 12, 'Recorded proof application',
        sub='shared declarations → generated premise → supplied consumer', edge=ORANGE, title_size=6.8)
    # arrows to figure numbers
    text(ax, 47.5, 133, 'Fig. 3', sz=6.8, bold=True, ha='center', color=BLUE)
    text(ax, 132.5, 133, 'Fig. 4', sz=6.8, bold=True, ha='center', color=ORANGE)
    text(ax, 90, 143, 'Humans, AI, feedback and adoption remain inside the research object', sz=6.1, ha='center')
    text(ax, 90, 151, 'Evidence identities remain separate: theorem, successor records and Lean proof record are not one identified causal loop',
         sz=5.8, ha='center')

    inputs = [source_doc(root, 'manuscript.md'), root/'SOURCE_DATA/figure2_analytic_curve.csv', root/'SOURCE_DATA/successor/audit_result.json']
    save(fig, 'figure1_core_non_sufficiency', root,
         ['Same readout r is insufficient; actual state/target and recorded entry points are distinguished.'], inputs)


def fig2(root: Path):
    fig = plt.figure(figsize=(180/25.4, 116/25.4), facecolor=WHITE)
    panel_font = 8.0
    title_font = 7.0
    fig.text(4/180, 1-6/116, 'a', fontsize=panel_font, fontweight='bold', va='center')
    fig.text(11/180, 1-6/116, 'A positive minimax gap under a readout-only rule', fontsize=title_font, fontweight='bold', va='center')
    ax1 = fig.add_axes([0.08, 0.23, 0.48, 0.56])
    ax1.spines[['top', 'right']].set_visible(False)

    with (root/'SOURCE_DATA/figure2_analytic_curve.csv').open() as fh:
        rows = list(csv.DictReader(fh))
    g = np.array([float(d['g']) for d in rows])
    r = float(rows[0]['r']); v = float(rows[0]['v'])
    ep = np.array([float(d['abs_E_plus']) for d in rows])
    em = np.array([float(d['abs_E_minus']) for d in rows])
    mx = np.array([float(d['worst_case']) for d in rows])
    g0 = math.sqrt(1+r) - 1
    lower = 2*v*g0
    ax1.plot(g, ep, color=BLUE, lw=1.1, label=r'$|E_+|$')
    ax1.plot(g, em, color=ORANGE, lw=1.1, ls='--', label=r'$|E_-|$')
    ax1.plot(g, mx, color=INK, lw=.9, ls=':', label='maximum')
    ax1.axhline(0, color=MID, lw=.6)
    ax1.scatter([g0], [lower], s=18, facecolor=WHITE, edgecolor=INK, zorder=5)
    ax1.annotate('', xy=(g0, lower), xytext=(g0, 0),
                 arrowprops=dict(arrowstyle='<->', color=INK, lw=.6))
    ax1.text(0.36, 0.78, r'$2v(\sqrt{1+r}-1)$', fontsize=7.4, transform=ax1.transAxes)
    ax1.annotate('minimum above zero', xy=(g0, lower), xytext=(0.36, 0.69), textcoords='axes fraction',
                 arrowprops=dict(arrowstyle='-', color=INK, lw=.55), fontsize=6.3)
    ax1.set_xlim(g.min(), g.max())
    ax1.set_ylim(0, mx.max()*1.08)
    ax1.set_xlabel('Common increment $g$', fontsize=6.6)
    ax1.set_ylabel('Absolute residual', fontsize=6.6)
    ax1.tick_params(labelsize=6.2)
    ax1.legend(loc='upper left', fontsize=6.2, handlelength=2)
    ax1.text(0.02, 1.03, r'$r=1/5,\,v=1/10,\,z_{\pm}=1\pm v,\,p_{\pm}=z_{\pm}^2+r$',
             transform=ax1.transAxes, fontsize=6.4)

    # panel b domain plot
    fig.text(0.63, 1-6/116, 'b', fontsize=panel_font, fontweight='bold', va='center')
    fig.text(0.67, 1-6/116, 'Compact repair and\ndeclared domain', fontsize=title_font, fontweight='bold', va='center')
    ax2 = fig.add_axes([0.64, 0.23, 0.30, 0.56])
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.set_xlim(-0.62, 0.62)
    ax2.set_ylim(-0.32, 0.32)
    ax2.set_xlabel('$r$', fontsize=6.6)
    ax2.set_ylabel('$u=z-1$', fontsize=6.6)
    ax2.tick_params(labelsize=6.2)
    ax2.plot([-0.62, -0.26], [0, 0], color=MID, lw=.5)
    ax2.plot([0.26, 0.62], [0, 0], color=MID, lw=.5)
    ax2.plot([0, 0], [-0.32, -0.26], color=MID, lw=.5)
    ax2.plot([0, 0], [0.126, 0.32], color=MID, lw=.5)
    outer = Rectangle((-0.5, -0.25), 1.0, 0.5, facecolor=LIGHT, edgecolor=GREY, lw=.8)
    inner = Rectangle((-0.25, -0.125), 0.5, 0.25, facecolor='#D7EAF8', edgecolor=BLUE, lw=.9)
    ax2.add_patch(outer)
    ax2.add_patch(inner)
    ax2.text(0, 0, 'inner core\nexact state-aware\nclosure', ha='center', va='center', fontsize=6.4)
    ax2.text(0.0, -0.19, 'outer support\nsmooth cutoff\nextension', ha='center', va='center', fontsize=5.9)
    fig.text(0.64, 0.060, 'outside support: return to\nsigned linear rule', ha='left', va='center', fontsize=6.2)
    ax2.annotate(r'$|r|\leq1/4,\ |u|\leq1/8$', xy=(0.25, 0.125), xytext=(0.03, 0.79), textcoords='axes fraction', fontsize=7.4,
                 arrowprops=dict(arrowstyle='-', color=INK, lw=.55))
    ax2.annotate(r'$|r|\leq1/2,\ |u|\leq1/4$', xy=(0.5, 0.25), xytext=(0.00, 1.035), textcoords='axes fraction', fontsize=7.4,
                 arrowprops=dict(arrowstyle='-', color=INK, lw=.55))
    fig.text(0.64, 0.115, 'inner rule:\ng(r,u) = √((1+u)² + r) − (1+u)', fontsize=6.5)
    fig.text(0.08, 0.020, 'Analytical curves and declared domains only: no empirical sample size and no claim about full Navier–Stokes field equality.', fontsize=6.0)

    inputs = [root/'SOURCE_DATA/figure2_analytic_curve.csv', source_doc(root, 'supplementary_information.md')]
    save(fig, 'figure2_minimax_and_domain', root,
         ['Positive lower bound and compact repair with inner/outer domain; analytical, not sampled.'], inputs)


def _format_small(x: float) -> str:
    if x == 0:
        return '0'
    s = f'{x:.3e}'
    base, exp = s.split('e')
    return f'{x:.3e}'


def fig3(root: Path):
    # New high-priority successor figure.
    with (root/'SOURCE_DATA/successor/selected_coordinates.csv').open() as fh:
        selected = list(csv.DictReader(fh))
    p00 = [r for r in selected if r['stage_id'] == 'P00_s0_W1']
    p07 = [r for r in selected if r['stage_id'] in ('P07_W1', 'P07_s0_W2') and r['kind'] in ('initial', 'effect')]
    audit = json.loads((root/'SOURCE_DATA/successor/audit_result.json').read_text())
    cohort = json.loads((root/'SOURCE_DATA/successor/cohort_status.json').read_text())
    eqs = json.loads((root/'SOURCE_DATA/successor/version_identity.json').read_text())
    inherit = json.loads((root/'SOURCE_DATA/successor/inheritance.json').read_text())

    fig = plt.figure(figsize=(180/25.4, 180/25.4), facecolor=WHITE)
    fig.text(4/180, 1-6/180, 'a', fontsize=8.0, fontweight='bold', va='center')
    fig.text(11/180, 1-6/180, 'One revised programme improves the whole relation by giving up a locally exact component', fontsize=7.0, fontweight='bold', va='center')
    ax1 = fig.add_axes([0.12, 1-67/180, 0.82, 46/180])
    ax1.spines[['top', 'right']].set_visible(False)
    versions = ['initial', 'draft', 'effect']
    x = np.arange(len(versions))
    w = 0.22
    pure = np.array([float(next(r['pure'] for r in p00 if r['kind']==k)) for k in versions])
    cross = np.array([float(next(r['cross'] for r in p00 if r['kind']==k)) for k in versions])
    whole = np.array([float(next(r['residual'] for r in p00 if r['kind']==k)) for k in versions])
    ax1.bar(x-w, pure, width=w, color='#94BBD4', edgecolor=BLUE, linewidth=.5, label='pure')
    ax1.bar(x, cross, width=w, color='#E5B28E', edgecolor=ORANGE, linewidth=.5, label='cross')
    ax1.bar(x+w, whole, width=w, facecolor=WHITE, edgecolor=INK, linewidth=1.1, label='whole')
    ax1.axhline(0, color=INK, lw=.6)
    ax1.set_yscale('symlog', linthresh=1e-12, linscale=1)
    ax1.set_ylim(-2.6e-6, 2.6e-6)
    ax1.set_xticks(x)
    ax1.set_xticklabels(['initial', 'draft', 'effect'], fontsize=6.4)
    ax1.set_ylabel('signed component value', fontsize=6.5)
    ax1.tick_params(axis='y', labelsize=7.4)
    ax1.legend(loc='lower right', bbox_to_anchor=(1, 1.04), ncol=3, fontsize=6.1, handlelength=1.4, columnspacing=1.0)
    ax1.text(0.0, 1.16, 'Same coordinate, same $r$, $u$, target and $z_{before}$ in P00_s0_W1', transform=ax1.transAxes, fontsize=6.2)
    # Annotations showing key logic.
    ax1.annotate('pure already 0\nwhole ≠ 0', xy=(x[0]-.35, -2.6e-6), xytext=(0.025, -0.26), textcoords='axes fraction', ha='center', fontsize=6.1,
                 arrowprops=dict(arrowstyle='-', color=INK, lw=.55))
    ax1.annotate('pure becomes non-zero\nand offsets cross', xy=(x[2]-w, pure[2]), xytext=(0.80, -0.24), textcoords='axes fraction', ha='center', fontsize=6.1,
                 arrowprops=dict(arrowstyle='-', color=INK, lw=.55))
    # Exact residual labels, including saved 1.81e-71.
    for i, val in enumerate(whole):
        if i < 2:
            ax1.annotate(_format_small(val), (x[i]+w, val), xytext=(-10, 7 if val >=0 else -12), textcoords='offset points', ha='center', fontsize=5.8)
        else:
            ax1.annotate('saved whole = 1.811136 × 10⁻⁷¹', (x[i]+w, val), xytext=(0.80, -0.37), textcoords='axes fraction', ha='center', fontsize=5.8)

    # middle panel: process and inheritance chain
    fig.text(4/180, 1-88/180, 'b', fontsize=8.0, fontweight='bold', va='center')
    fig.text(11/180, 1-88/180, 'Actual feedback, parent-state inheritance and changed-target reuse', fontsize=7.0, fontweight='bold', va='center')
    axb = fig.add_axes([0.03, 1-130/180, 0.94, 40/180]); axb.set_xlim(0, 180); axb.set_ylim(42, 0); axb.axis('off')
    box(axb, 2, 5, 28, 19, 'P00_W0', sub='formed rule', edge=GREY)
    box(axb, 38, 5, 43, 19, 'P00_s0_W1', sub='initial → draft → effect\nfeedback-driven revision', edge=BLUE)
    box(axb, 89, 5, 40, 19, 'P00_s0_W2', sub='changed target\nprogramme retained', edge=BLUE)
    box(axb, 137, 5, 41, 19, 'Reuse observed', sub='actual parent field\ninherited', edge=INK)
    arrow(axb, (30, 14), (38, 14), color=GREY)
    arrow(axb, (81, 14), (89, 14), color=BLUE)
    arrow(axb, (129, 14), (137, 14), color=INK)
    text(axb, 48, 28, 'actual feedback rows', sz=6.0, ha='center')
    text(axb, 127, 28, 'different target, same inherited state line', sz=6.0, ha='center')
    text(axb, 4, 35, r'$B_0=-1/[2(1+\sqrt{1+r})^2],\ C_0=0$', sz=5.9)
    text(axb, 4, 40, r'final $C$ = smooth secant expression; $B$ retained', sz=5.9)

    # bottom panel: P07 within-duty comparisons and cohort boundary.
    fig.text(4/180, 1-136/180, 'c', fontsize=8.0, fontweight='bold', va='center')
    fig.text(11/180, 1-136/180, 'Further revision is compared within, not across, duties', fontsize=7.0, fontweight='bold', va='center')
    ax2 = fig.add_axes([0.14, 1-163/180, 0.36, 23/180])
    ax2.spines[['top','right']].set_visible(False)
    duties = ['P07_W1\nfirst duty', 'P07_s0_W2\nsecond duty']
    init = [abs(float(next(r['residual'] for r in p07 if r['stage_id']=='P07_W1' and r['kind']=='initial'))),
            abs(float(next(r['residual'] for r in p07 if r['stage_id']=='P07_s0_W2' and r['kind']=='initial')))]
    eff = [abs(float(next(r['residual'] for r in p07 if r['stage_id']=='P07_W1' and r['kind']=='effect'))),
           abs(float(next(r['residual'] for r in p07 if r['stage_id']=='P07_s0_W2' and r['kind']=='effect')))]
    y = np.arange(2)
    for yy, a, b in zip(y, init, eff):
        ax2.plot([a, b], [yy, yy], color=INK, lw=.7)
    ax2.scatter(init, y, s=24, marker='o', facecolor=WHITE, edgecolor=INK, label='old programme', zorder=3)
    ax2.scatter(eff, y, s=24, marker='D', facecolor=BLUE, edgecolor=BLUE, label='revised programme', zorder=3)
    assert all(value > 0 for value in init + eff)
    ax2.set_xscale('log')
    ax2.set_xlim(1e-16, 1e-7)
    ax2.set_yticks(y)
    ax2.set_yticklabels(duties, fontsize=6.2)
    ax2.set_ylim(1.25, -0.25)
    ax2.tick_params(axis='x', labelsize=7.4)
    ax2.set_xlabel('absolute whole residual', fontsize=6.4, labelpad=0)
    ax2.legend(loc='lower center', bbox_to_anchor=(0.50, -0.64), ncol=2, fontsize=5.9)
    # right text block
    ax3 = fig.add_axes([0.55, 1-178/180, 0.42, 37/180]); ax3.axis('off')
    ax3.text(0, 0.97, f"52 recorded stages  •  {audit['historical_complete_requests']} complete returns", fontsize=6.15, fontweight='bold', va='top')
    ax3.text(0, 0.82, f"7/8 adoption pairs kept identical code\n• {sum(v['empty_programs'] for v in cohort.values())} empty final programmes", fontsize=5.85, linespacing=1.22, va='top')
    ax3.text(0, 0.64, 'P07 points are post-selected explanatory traces;\nthey do not establish an average gain.', fontsize=5.85, linespacing=1.22, va='top')
    ax3.text(0, 0.46, 'Do not join different targets into one learning curve.\nThe two duties use different inherited states and targets.', fontsize=5.85, linespacing=1.22, va='top')
    ax3.text(0, 0.25, '40 parent-state links were checked byte-for-byte.\nUnchanged versions, failures and the supplementary\nobservation remain in Source Data.', fontsize=5.85, linespacing=1.22, va='top')

    inputs = [root/'SOURCE_DATA/successor/selected_coordinates.csv', root/'SOURCE_DATA/successor/cohort_status.json',
              root/'SOURCE_DATA/successor/version_identity.json', root/'SOURCE_DATA/successor/inheritance.json',
              source_doc(root, 'manuscript.md')]
    save(fig, 'figure3_successor_continuation', root,
         ['Signed pure/cross/whole decomposition, actual revision/reuse chain, within-duty P07 comparisons, and cohort limits.'], inputs)


def fig4(root: Path):
    rows = json.loads((root/'SOURCE_DATA/attempts.json').read_text())
    fig = plt.figure(figsize=(180/25.4, 150/25.4), facecolor=WHITE)
    fig.text(4/180, 1-6/150, 'a', fontsize=8.0, fontweight='bold', va='center')
    fig.text(11/180, 1-6/150, 'A shared result must be transported into the consumer’s representation', fontsize=7.0, fontweight='bold', va='center')
    axa = fig.add_axes([0.025, 1-49/150, 0.95, 38/150]); axa.set_xlim(0, 180); axa.set_ylim(38, 0); axa.axis('off')
    box(axa, 1, 8, 55, 22, 'Shared declarations', sub='outer theorem + interval-error lemma\n+ $R_n^2=L_n$', edge=INK)
    box(axa, 67, 2, 45, 15, 'Transport 1', sub='interval membership\n[0, R_n²] → [0, L_n]', edge=GREY)
    box(axa, 67, 20, 45, 15, 'Transport 2', sub='whole dependent inequality\nL_n → R_n²', edge=GREY)
    box(axa, 123, 8, 54, 22, 'Consumer-ready premise', sub='|H̄(P)ᵢⱼ − H₀(ξ)ᵢⱼ| ≤ Q/Rₙ ≤ ρ', edge=INK)
    arrow(axa, (56, 16), (68, 12), color=GREY)
    arrow(axa, (56, 22), (68, 28), color=GREY)
    arrow(axa, (112, 12), (124, 16), color=GREY)
    arrow(axa, (112, 28), (124, 22), color=GREY)
    text(axa, 90, 40, 'Rewriting interval membership alone is not enough; the entire dependent conclusion must also be transported', sz=6.0, ha='center')

    fig.text(4/180, 1-54/150, 'b', fontsize=8.0, fontweight='bold', va='center')
    fig.text(11/180, 1-54/150, 'The generated proof object is actually used downstream', fontsize=7.0, fontweight='bold', va='center')
    axb = fig.add_axes([0.05, 1-80/150, 0.90, 23/150]); axb.set_xlim(0, 180); axb.set_ylim(28, 0); axb.axis('off')
    box(axb, 8, 8, 34, 12, 'generated hclose', sub='model output', edge=BLUE)
    box(axb, 57, 8, 34, 12, 'supplied hmargin', sub='pre-existing consumer', edge=GREY)
    box(axb, 106, 8, 60, 12, 'ZeroOrderBounds', sub='existing downstream theorem', edge=INK)
    arrow(axb, (42, 14), (57, 14), color=BLUE)
    arrow(axb, (91, 14), (106, 14), color=INK)
    text(axb, 74, 23, 'two transports above make hclose consumer-ready', sz=6.0, ha='center')

    fig.text(4/180, 1-86/150, 'c', fontsize=8.0, fontweight='bold', va='center')
    fig.text(11/180, 1-86/150, 'All six requests, five candidates and the truncated control request', fontsize=7.0, fontweight='bold', va='center')
    axc = fig.add_axes([0.20, 1-126/150, 0.74, 26/150])
    axc.set_xlim(-0.5, 2.5); axc.set_ylim(-0.5, 1.5)
    axc.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
    for yy in [-.5, .5, 1.5]:
        axc.axhline(yy, color=LIGHT, lw=.45)
    for xx in [-.5, .5, 1.5, 2.5]:
        axc.axvline(xx, color=LIGHT, lw=.45)
    axc.set_yticks([1, 0]); axc.set_yticklabels(['guided', 'declarations only'], fontsize=6.4)
    axc.set_xticks([0,1,2]); axc.set_xticklabels(['attempt 1', 'attempt 2', 'attempt 3'], fontsize=6.3)
    axc.tick_params(axis='x', pad=3)
    axc.set_xlabel('bounded local request sequence', fontsize=6.5)

    color_map = {'LEAN_REJECTED': ORANGE, 'LEAN_ACCEPTED': BLUE, 'TRUNCATED_NO_BODY': WHITE}
    marker_map = {'LEAN_REJECTED': 's', 'LEAN_ACCEPTED': 'o', 'TRUNCATED_NO_BODY': 'X'}
    labels_done = set()
    for row in rows:
        arm_y = 1 if row['arm'] == 'HISTORY' else 0
        x = row['attempt'] - 1
        face = color_map[row['outcome']]
        edge = INK if row['outcome'] == 'TRUNCATED_NO_BODY' else color_map[row['outcome']]
        axc.scatter([x-.27], [arm_y], s=70, marker=marker_map[row['outcome']], facecolor=face,
                    edgecolor=edge, linewidth=.8, zorder=3,
                    label=row['outcome'] if row['outcome'] not in labels_done else None)
        labels_done.add(row['outcome'])
        if row['outcome'] == 'TRUNCATED_NO_BODY':
            note = 'length limit\nno visible body'
        elif row['outcome'] == 'LEAN_ACCEPTED':
            note = f"candidate {row['attempt']}\naccepted"
        else:
            note = f"candidate {row['attempt']}\nrejected"
        axc.annotate(note, (x-.27, arm_y), xytext=(9, 0), textcoords='offset points', ha='left', va='center', fontsize=6.0)
    axc.legend(loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=3, fontsize=6.0)
    fig.text(0.04, 0.020, 'First declarations-only request was truncated and had no body;\nit was not a Lean rejection. Guidance added an application strategy\nand the downstream consumer was supplied.',
             fontsize=5.95, linespacing=1.2)
    fig.text(0.52, 0.020, 'This is one selected paired comparison: six requests and five candidates\nare not independent replications, and saved compilation acceptance\nis not upgraded here to new kernel certification.',
             fontsize=5.95, linespacing=1.2)


    inputs = [root/'SOURCE_DATA/attempts.json', source_doc(root, 'manuscript.md'), source_doc(root, 'supplementary_information.md')]
    save(fig, 'figure4_hclose_application', root,
         ['Dependent transport, actual downstream use, and all six proof-completion requests including the truncated first control request.'], inputs)


def ed1(root: Path):
    rows = json.loads((root/'SOURCE_DATA/attempts.json').read_text())
    fig = plt.figure(figsize=(180/25.4, 95/25.4), facecolor=WHITE)
    ax = fig.add_axes([.10, .22, .85, .65]); ax.spines[['top', 'right']].set_visible(False)
    x = np.arange(len(rows), dtype=float)
    x[3:] += .65
    inputs = np.array([r['prompt_tokens'] for r in rows])
    outputs = np.array([r['completion_tokens'] for r in rows])
    ax.bar(x-.17, inputs, .32, facecolor=WHITE, edgecolor=BLUE, linewidth=.9, label='input')
    ax.bar(x+.17, outputs, .32, color=BLUE, edgecolor=INK, linewidth=.4, label='output (including reasoning)')
    for i, n in enumerate(inputs):
        ax.text(x[i]-.17, n+550, f'{n:,}', ha='center', va='bottom', fontsize=6.0)
    for i, n in enumerate(outputs):
        ax.text(x[i]+.17, n+550, f'{n:,}', ha='center', va='bottom', fontsize=6.0)
    ax.set_ylim(0, 38500); ax.set_xlim(-.55, 6.20)
    ax.set_yticks([0, 10000, 20000, 30000]); ax.set_yticklabels(['0', '10,000', '20,000', '30,000'])
    ax.set_xticks(x)
    ax.set_xticklabels(['guided 1', 'guided 2', 'guided 3', 'decl. 1', 'decl. 2', 'decl. 3'], fontsize=6.2)
    ax.set_ylabel('recorded token count')
    ax.legend(loc='upper left', fontsize=6.2)
    fig.text(.025, .95, 'Extended Data Fig. 1 | Recorded resources in the selected proof-completion comparison', fontsize=7, fontweight='bold', va='center')
    fig.text(.105, .08, 'The first declarations-only request was truncated and produced no visible proof body.', fontsize=6.1)
    fig.text(.105, .035, 'Counts describe realised usage only; they are not a general efficiency comparison.', fontsize=6.1)
    save(fig, 'extended_data_figure1_resources', root,
         ['Exact input/output token counts and truncation; no efficiency inference.'], [root/'SOURCE_DATA/attempts.json'])


def edt(root: Path):
    with (root/'SOURCE_DATA/extended_data_table1_history.csv').open() as fh:
        rows = list(csv.DictReader(fh))
    fig, ax = canvas(127)
    text(ax, 4, 6, 'Extended Data Table 1 | Earlier workflows keep their original evidence identities', sz=7, bold=True)
    widths = [42, 82, 48]; xs = [4, 46, 128]; top = 16
    for x, label in zip(xs, ['Recorded workflow', 'Retained outcome', 'Evidence identity']):
        text(ax, x+1, top, label, sz=7, bold=True)
    rule(ax, 4, 21, 176, 21, color=INK, lw=.7)
    y = 24
    for row in rows:
        vals = [row['recorded_workflow'], row['retained_outcome'], row['evidence_status']]
        wrapped = [textwrap.wrap(v, width=w) for v, w in zip(vals, [27, 54, 31])]
        n = max(map(len, wrapped)); h = max(9, n*3.0 + 3)
        for x, lines in zip(xs, wrapped):
            text(ax, x+1, y, '\n'.join(lines), sz=6.6, va='top', linespacing=1.2)
        y += h
        rule(ax, 4, y-2, 176, y-2, lw=.4)
    text(ax, 4, y+3, 'Stopped, failed, unrun, diagnostic and reference-exposed records remain distinct; the final proof completion does not relabel them as one success process.', sz=6.0)
    save(fig, 'extended_data_table1_history', root,
         ['Original ten historical rows and evidence statuses remain separate.'], [root/'SOURCE_DATA/extended_data_table1_history.csv'])


def main(root: Path):
    root = root.resolve(); (root/'QA').mkdir(exist_ok=True)
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        for fn in [fig1, fig2, fig3, fig4, ed1, edt]:
            fn(root)
        notices = [str(w.message) for w in ws]
    (root/'QA/FIGURE_BUILD.json').write_text(json.dumps({
        'figures': LOG,
        'warnings': notices,
        'font': font_manager.findfont(FONT),
        'new_scientific_observations': 0
    }, ensure_ascii=False, indent=2))
    if any('missing from font' in s for s in notices):
        raise RuntimeError('MISSING_GLYPH: see FIGURE_BUILD.json')
    print(json.dumps({'figures': len(LOG), 'warnings': len(notices)}, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    a = p.parse_args()
    main(a.root)
