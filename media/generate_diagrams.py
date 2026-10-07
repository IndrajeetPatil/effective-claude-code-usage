"""
Hand-drawn style diagrams for effective-claude-code-usage slides.
Font: Caveat (Google Fonts) — same family Excalidraw uses as its Virgil fallback.
Run from the project root: uv run python media/generate_diagrams.py
"""

import io
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Polygon
from PIL import Image, ImageChops

# ── Register Caveat font ──────────────────────────────────────
_here = os.path.dirname(os.path.abspath(__file__))
font_manager.fontManager.addfont(os.path.join(_here, 'Caveat.ttf'))
plt.rcParams['font.family'] = 'Caveat'

# ── Colour palette ────────────────────────────────────────────
BG   = '#0d1117'
GRN  = '#22c55e'
BLU  = '#38bdf8'
AMB  = '#f59e0b'
PUR  = '#a78bfa'
RED  = '#f87171'
TXT  = '#e6edf3'
MUT  = '#a8b3c1'
CARD = '#1c2128'


def tint(accent, amount=0.16):
    """Blend an accent into the background; dark fills keep accent text above WCAG AA."""
    a = [int(accent[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(BG[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(b[k] + (a[k] - b[k]) * amount):02x}' for k in range(3))


DPI = 160

# ── Drawing helpers ───────────────────────────────────────────

def new_fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.subplots_adjust(0, 0, 1, 1)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis('off')
    return fig, ax


def box(ax, x, y, w, h, col, label, fs=22, sub='', sfs=17, fc=None, lw=2.0, ls='-'):
    """Rounded box: accent border, tinted fill, accent label, optional muted sub-label."""
    p = FancyBboxPatch((x - w/2, y - h/2), w, h,
                       boxstyle='round,pad=0,rounding_size=0.12',
                       facecolor=tint(col) if fc is None else fc, edgecolor=col,
                       linewidth=lw, linestyle=ls, zorder=3)
    ax.add_patch(p)
    if sub:
        ax.text(x, y + h * 0.17, label, ha='center', va='center',
                fontsize=fs, color=col, zorder=4, linespacing=1.1)
        ax.text(x, y - h * 0.22, sub, ha='center', va='center',
                fontsize=sfs, color=TXT, zorder=4, linespacing=1.1)
    else:
        ax.text(x, y, label, ha='center', va='center',
                fontsize=fs, color=col, zorder=4, linespacing=1.1)


def diamond(ax, x, y, w, h, col, label, fs=20):
    """Diamond decision shape with centred label."""
    verts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
    ax.add_patch(Polygon(verts, closed=True, facecolor=tint(col), edgecolor=col,
                         linewidth=2.0, zorder=3))
    ax.text(x, y, label, ha='center', va='center', fontsize=fs, color=col,
            zorder=4)


def arr(ax, x1, y1, x2, y2, col=MUT, lw=2.0, rad=0.0, ms=16):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0,
                                connectionstyle=f'arc3,rad={rad}'),
                zorder=2)


def line(ax, xs, ys, col=MUT, lw=2.0, ls='-'):
    ax.plot(xs, ys, color=col, lw=lw, ls=ls, zorder=2, solid_capstyle='round')


def lbl(ax, x, y, text, col=MUT, fs=18, ha='center', **kw):
    ax.text(x, y, text, ha=ha, va='center', fontsize=fs, color=col,
            style='italic', zorder=5, **kw)


def heading(ax, x, y, text, col, fs=21, ha='center'):
    ax.text(x, y, text, ha=ha, va='center', fontsize=fs, color=col, zorder=5)


def bracket(ax, x1, x2, y, text, col=MUT, fs=18):
    """Horizontal bracket above a span, with its label above it."""
    line(ax, [x1, x1, x2, x2], [y - 0.12, y, y, y - 0.12], col=col, lw=1.6)
    lbl(ax, (x1 + x2) / 2, y + 0.22, text, col=col, fs=fs)


def save(fig, name):
    """Render, crop to the drawn content, and write a WebP next to this script."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=DPI, facecolor=BG)
    plt.close(fig)
    im = Image.open(buf).convert('RGB')
    diff = ImageChops.difference(im, Image.new('RGB', im.size, BG)).convert('L')
    left, top, right, bottom = diff.point(lambda p: 255 if p > 10 else 0).getbbox()
    pad = int(0.12 * DPI)
    im = im.crop((max(left - pad, 0), max(top - pad, 0),
                  min(right + pad, im.width), min(bottom + pad, im.height)))
    im.save(os.path.join(_here, name), 'WEBP', quality=90, method=6)
    print(f'  ok  {name}  {im.width}x{im.height}')


# ═══════════════════════════════════════════════════════════════
# 1 — Intelligence Spectrum
# ═══════════════════════════════════════════════════════════════
def make_01():
    fig, ax = new_fig(11, 4.7)

    arr(ax, 0.3, 4.45, 10.7, 4.45, col=MUT, lw=1.8)
    lbl(ax, 5.5, 4.18, 'more autonomy', fs=19)

    cols = [
        (1.85, MUT, 'Tab completion', ['Predicts next tokens', 'Sees the open file', 'You write the code']),
        (5.50, BLU, 'Chatbot',        ['Answers a prompt', 'Sees what you paste', 'You run the code']),
        (9.15, GRN, 'Agent (Claude Code)', ['Pursues a goal', 'Reads the whole repo', 'Runs and checks its work']),
    ]
    for x, col, head, items in cols:
        heading(ax, x, 3.68, head, col, fs=24)
        ax.add_patch(FancyBboxPatch((x - 1.7, 0.2), 3.4, 3.05,
                                    boxstyle='round,pad=0,rounding_size=0.15',
                                    facecolor=tint(col, 0.06), edgecolor=tint(col, 0.45),
                                    linewidth=1.4, zorder=1))
        for y, item in zip([2.7, 1.73, 0.76], items):
            box(ax, x, y, 3.0, 0.72, col, item, fs=21)

    save(fig, 'diag-01-intelligence-spectrum.webp')


# ═══════════════════════════════════════════════════════════════
# 2 — ReAct Agent Loop
# ═══════════════════════════════════════════════════════════════
def make_02():
    fig, ax = new_fig(11, 3.4)
    y, h = 2.25, 1.2

    box(ax, 0.75, y, 1.2, h, PUR, 'Task', fs=23)
    box(ax, 2.75, y, 1.8, h, BLU, 'Think', sub='choose next step')
    box(ax, 4.95, y, 1.8, h, AMB, 'Act', sub='call a tool')
    box(ax, 7.15, y, 1.8, h, GRN, 'Observe', sub='read the result')
    diamond(ax, 8.95, y, 1.25, 1.25, TXT, 'Done?')
    box(ax, 10.45, y, 1.0, h, GRN, 'Result', fs=21)

    for x1, x2 in [(1.35, 1.85), (3.65, 4.05), (5.85, 6.25), (8.05, 8.32)]:
        arr(ax, x1, y, x2, y, col=TXT)
    arr(ax, 9.575, y, 9.95, y, col=GRN)
    lbl(ax, 9.76, y + 0.32, 'yes', col=GRN, fs=18)

    loop_y = 0.75
    line(ax, [8.95, 8.95], [y - 0.625, loop_y])
    line(ax, [8.95, 2.75], [loop_y, loop_y])
    arr(ax, 2.75, loop_y, 2.75, y - h/2)
    lbl(ax, 5.85, loop_y - 0.3, 'no: loop again, often many tool calls per turn', fs=18)

    save(fig, 'diag-02-react-loop.webp')


# ═══════════════════════════════════════════════════════════════
# 4 — Context Window (what /context reports)
# ═══════════════════════════════════════════════════════════════
def make_04():
    fig, ax = new_fig(11, 4.4)
    x0, bh = 2.25, 0.95

    def bar(y, segments):
        x = x0
        for width, col, text in segments:
            dashed = col is None
            box(ax, x + width/2, y, width - 0.06, bh, MUT if dashed else col, text,
                fs=17, fc=BG if dashed else None, lw=1.6, ls='--' if dashed else '-')
            x += width
        return x

    startup = [(1.0, MUT, 'System\nprompt'), (1.3, PUR, 'CLAUDE.md\n+ memory'),
               (1.3, BLU, 'Skill + MCP\nindex')]
    work = [(1.2, GRN, 'Prompts\n+ replies'), (1.3, AMB, 'File reads'),
            (1.45, RED, 'Tool output')]

    heading(ax, 2.0, 2.65, 'Mid-session', TXT, fs=20, ha='right')
    bar(2.65, startup + work + [(1.15, None, 'free')])
    s_end = x0 + sum(w for w, *_ in startup)
    w_end = s_end + sum(w for w, *_ in work)
    bracket(ax, x0 + 0.03, s_end - 0.03, 3.3, 'loaded at startup')
    bracket(ax, s_end + 0.03, w_end - 0.03, 3.3, 'grows every turn')

    heading(ax, 2.0, 0.85, 'After /compact', TXT, fs=20, ha='right')
    bar(0.85, startup + [(1.25, GRN, 'Summary'), (3.85, None, 'free')])
    lbl(ax, s_end + 0.62, 1.62, 'history replaced by a summary', fs=18, ha='left')

    save(fig, 'diag-04-context-window.webp')


# ═══════════════════════════════════════════════════════════════
# 5 — CLAUDE.md Loading
# ═══════════════════════════════════════════════════════════════
def make_05():
    fig, ax = new_fig(11, 4.7)

    heading(ax, 0.35, 4.45, 'At launch: concatenated, broadest first', GRN, fs=21, ha='left')
    launch = [
        (1.45, MUT, 'Managed policy', 'organisation'),
        (4.15, BLU, '~/.claude/CLAUDE.md', 'you, every project'),
        (6.85, GRN, './CLAUDE.md', 'team, plus parent dirs'),
        (9.55, PUR, 'CLAUDE.local.md', 'you, this project'),
    ]
    for x, col, head, sub in launch:
        box(ax, x, 3.5, 2.3, 1.05, col, head, fs=19, sub=sub, sfs=17)
    for x1, x2 in [(2.6, 3.0), (5.3, 5.7), (8.0, 8.4)]:
        arr(ax, x1 + 0.02, 3.5, x2 - 0.02, 3.5, col=TXT)
    lbl(ax, 5.5, 2.68, '@path imports expand inline at launch (up to four hops)', fs=18)

    heading(ax, 0.35, 2.0, 'On demand: when Claude works with matching files', AMB, fs=21, ha='left')
    box(ax, 3.05, 1.0, 4.4, 1.05, AMB, 'subdir/CLAUDE.md', fs=19,
        sub='read or edit a file in that folder', sfs=17)
    box(ax, 7.95, 1.0, 4.4, 1.05, AMB, '.claude/rules/*.md  with  paths:', fs=19,
        sub='touch a file matching the glob', sfs=17)

    save(fig, 'diag-05-claude-md-loading.webp')


# ═══════════════════════════════════════════════════════════════
# 6 — Subagent Orchestration
# ═══════════════════════════════════════════════════════════════
def make_06():
    fig, ax = new_fig(11, 4.6)
    xs = [1.95, 5.5, 9.05]

    box(ax, 5.5, 4.1, 5.0, 0.75, PUR, 'Main session: holds the goal', fs=22)

    agents = [
        (BLU, 'Explore', 'find every auth call site\nread-only'),
        (GRN, 'general-purpose', 'update the API docs\ncan edit files'),
        (AMB, 'code-reviewer (custom)', 'review the diff\nyour tools + model'),
    ]
    for x, (col, head, sub) in zip(xs, agents):
        box(ax, x, 2.35, 3.15, 1.45, col, head, fs=21, sub=sub, sfs=17)
        arr(ax, 5.5 + (x - 5.5) * 0.45, 3.72, x, 3.1)
        arr(ax, x, 1.62, 5.5 + (x - 5.5) * 0.55, 1.03)
    lbl(ax, 9.55, 4.1, 'each subagent gets\nits own context window', fs=17)

    box(ax, 5.5, 0.65, 6.6, 0.75, GRN, 'Only summaries return to the main context', fs=21)

    save(fig, 'diag-06-subagent-orchestration.webp')


# ═══════════════════════════════════════════════════════════════
# 7 — Planning Mode Workflow
# ═══════════════════════════════════════════════════════════════
def make_07():
    fig, ax = new_fig(11, 3.7)
    y, h = 2.15, 1.15

    box(ax, 0.7, y, 1.15, h, PUR, 'Request', fs=20)
    box(ax, 2.55, y, 1.85, h, BLU, 'Explore', sub='read code')
    box(ax, 4.85, y, 1.85, h, AMB, 'Draft plan', sub='files, steps, risks')
    diamond(ax, 6.95, y, 1.55, 1.3, TXT, 'Approve?', fs=19)
    box(ax, 8.75, y, 1.3, h, GRN, 'Execute', fs=20)
    box(ax, 10.3, y, 1.15, h, GRN, 'Verify', fs=20)

    for x1, x2 in [(1.275, 1.625), (3.475, 3.925), (5.775, 6.175), (9.4, 9.725)]:
        arr(ax, x1, y, x2, y, col=TXT)
    arr(ax, 7.725, y, 8.1, y, col=GRN)
    lbl(ax, 7.91, y + 0.4, 'yes', col=GRN, fs=18)

    bracket(ax, 1.65, 7.7, 3.05, 'plan mode: nothing is edited yet', col=BLU)

    loop_y = 0.75
    line(ax, [6.95, 6.95], [y - 0.65, loop_y])
    line(ax, [6.95, 4.85], [loop_y, loop_y])
    arr(ax, 4.85, loop_y, 4.85, y - h/2)
    lbl(ax, 5.9, loop_y - 0.3, 'revise', fs=18)

    save(fig, 'diag-07-planning-mode.webp')


# ═══════════════════════════════════════════════════════════════
# 9 — Daily Workflow / Mental Model
# ═══════════════════════════════════════════════════════════════
def make_09():
    fig, ax = new_fig(11, 3.4)

    steps = [
        (1.45, PUR, '1. Set context',   'CLAUDE.md + skills\nintent + done criteria'),
        (4.15, BLU, '2. Choose depth',  'direct prompt\n/plan or subagents\nworktree per task'),
        (6.85, AMB, '3. Manage context', '/context to inspect\n/clear between tasks\n/compact when long'),
        (9.55, GRN, '4. Verify result', 'git diff\ntests + lint\nreview the PR'),
    ]
    for x, col, head, sub in steps:
        box(ax, x, 2.85, 2.3, 0.8, col, head, fs=22)
        ax.text(x, 2.22, sub, ha='center', va='top', fontsize=19, color=TXT,
                linespacing=1.3, zorder=4)
    for i in range(len(steps) - 1):
        arr(ax, steps[i][0] + 1.17, 2.85, steps[i + 1][0] - 1.17, 2.85, col=TXT)

    save(fig, 'diag-09-mental-model.webp')


# ═══════════════════════════════════════════════════════════════
# 11 — Git Worktrees: Parallel Isolation
# ═══════════════════════════════════════════════════════════════
def make_11():
    fig, ax = new_fig(11, 4.3)
    xs = [1.9, 5.5, 9.1]

    box(ax, 5.5, 3.85, 6.8, 0.7, MUT, '.git/  shared history, refs, and remotes', fs=21, fc=CARD)

    trees = [(GRN, 'ui'), (BLU, 'auth'), (AMB, 'bugfix')]
    for x, (col, name) in zip(xs, trees):
        box(ax, x, 2.35, 3.2, 1.05, col, f'.claude/worktrees/{name}', fs=20,
            sub=f'branch worktree-{name}', sfs=18)
        box(ax, x, 0.55, 3.2, 0.7, col, f'claude --worktree {name}', fs=20, fc=BG)
        arr(ax, x, 1.82, x, 0.92)
    arr(ax, 2.6, 3.49, 1.9, 2.9, rad=0.2)
    arr(ax, 5.5, 3.49, 5.5, 2.9)
    arr(ax, 8.4, 3.49, 9.1, 2.9, rad=-0.2)

    save(fig, 'diag-11-worktrees.webp')


# ═══════════════════════════════════════════════════════════════
# 12 — Workflow Orchestration (adversarial-verify pipeline)
# ═══════════════════════════════════════════════════════════════
def make_12():
    fig, ax = new_fig(11, 4.2)
    ys = [3.0, 2.0, 1.0]

    box(ax, 1.05, 2.0, 1.75, 1.5, PUR, 'Workflow\nscript', fs=22)
    heading(ax, 4.0, 3.85, 'Phase 1: review', BLU)
    heading(ax, 7.0, 3.85, 'Phase 2: verify', AMB)

    reviews = ['bugs reviewer', 'security reviewer', 'perf reviewer']
    for y, text in zip(ys, reviews):
        box(ax, 4.0, y, 2.3, 0.7, BLU, text, fs=19)
        box(ax, 7.0, y, 2.3, 0.7, AMB, 'challenge findings', fs=19)
        arr(ax, 1.95, 2.0 + (y - 2.0) * 0.35, 2.83, y)
        arr(ax, 5.17, y, 5.83, y)
        arr(ax, 8.17, y, 9.03, 2.0 + (y - 2.0) * 0.35)

    box(ax, 9.95, 2.0, 1.75, 1.5, GRN, 'Confirmed\nfindings', fs=22)

    save(fig, 'diag-12-workflows.webp')


# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('Generating diagrams...')
    make_01(); make_02(); make_04(); make_05(); make_06()
    make_07(); make_09(); make_11(); make_12()
    print('All done.')
