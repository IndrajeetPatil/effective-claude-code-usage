"""
Diagrams for the effective-claude-code-usage slides, drawn in the style of the
Claude Code documentation: a warm light panel, pastel boxes with a thin accent
border, dark Inter labels, and JetBrains Mono for commands and file names.
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

# ── Register fonts ────────────────────────────────────────────
_here = os.path.dirname(os.path.abspath(__file__))
for _f in ('Inter-Regular.ttf', 'Inter-SemiBold.ttf', 'JetBrainsMono-Regular.ttf'):
    font_manager.fontManager.addfont(os.path.join(_here, _f))
plt.rcParams['font.family'] = 'Inter'
MONO = 'JetBrains Mono'

# ── Colour palette (mirrors DESIGN.md) ────────────────────────
BG   = '#F6F5EF'   # diagram panel
TXT  = '#171717'   # labels
MUT  = '#5F5F5D'   # sub-labels and annotations
LINE = '#8F8E8A'   # arrows and connectors
CLAY = '#D97757'   # brand accent
GRN  = '#6E9E6E'
BLU  = '#6A8FBF'
AMB  = '#D4A24C'
PUR  = '#9C86C4'
RED  = '#D07A70'
GRY  = '#B5B3AC'

FILL = {
    CLAY: '#FBEEE6', GRN: '#EAF1E6', BLU: '#E8EFF7', AMB: '#FAF0DC',
    PUR: '#EFEAF7', RED: '#F8E5E2', GRY: '#FFFFFF',
}

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


def box(ax, x, y, w, h, col, label, fs=20, sub='', sfs=17, mono=False,
        sub_mono=False, ls='-', lw=1.6):
    """Rounded pastel box with an accent hairline, dark label, optional sub-label."""
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                boxstyle='round,pad=0,rounding_size=0.1',
                                facecolor=FILL[col], edgecolor=col,
                                linewidth=lw, linestyle=ls, zorder=3))
    fam = MONO if mono else 'Inter'
    if sub:
        ax.text(x, y + h * 0.18, label, ha='center', va='center', fontsize=fs,
                color=TXT, weight=600, family=fam, zorder=4, linespacing=1.15)
        ax.text(x, y - h * 0.2, sub, ha='center', va='center', fontsize=sfs,
                color=MUT, family=MONO if sub_mono else 'Inter', zorder=4,
                linespacing=1.2)
    else:
        ax.text(x, y, label, ha='center', va='center', fontsize=fs, color=TXT,
                weight=600, family=fam, zorder=4, linespacing=1.15)


def diamond(ax, x, y, w, h, col, label, fs=18):
    verts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
    ax.add_patch(Polygon(verts, closed=True, facecolor=FILL[col], edgecolor=col,
                         linewidth=1.6, zorder=3))
    ax.text(x, y, label, ha='center', va='center', fontsize=fs, color=TXT,
            weight=600, zorder=4, linespacing=1.1)


def arr(ax, x1, y1, x2, y2, col=LINE, lw=1.8, rad=0.0, ls='-', ms=16):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=lw, ls=ls,
                                mutation_scale=ms, shrinkA=0, shrinkB=0,
                                connectionstyle=f'arc3,rad={rad}'),
                zorder=2)


def line(ax, xs, ys, col=LINE, lw=1.8, ls='-'):
    ax.plot(xs, ys, color=col, lw=lw, ls=ls, zorder=2, solid_capstyle='round')


def lbl(ax, x, y, text, col=MUT, fs=17, ha='center', mono=False, **kw):
    ax.text(x, y, text, ha=ha, va='center', fontsize=fs, color=col,
            family=MONO if mono else 'Inter', zorder=5, linespacing=1.25, **kw)


def heading(ax, x, y, text, fs=18, ha='center', col=MUT):
    """Small uppercase eyebrow label, as used for section labels in the docs."""
    ax.text(x, y, text.upper(), ha=ha, va='center', fontsize=fs, color=col,
            weight=600, zorder=5)


def save(fig, name):
    """Render, crop to the drawn content plus a margin, and write a WebP."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=DPI, facecolor=BG)
    plt.close(fig)
    im = Image.open(buf).convert('RGB')
    diff = ImageChops.difference(im, Image.new('RGB', im.size, BG)).convert('L')
    left, top, right, bottom = diff.point(lambda p: 255 if p > 10 else 0).getbbox()
    pad = int(0.22 * DPI)
    im = im.crop((max(left - pad, 0), max(top - pad, 0),
                  min(right + pad, im.width), min(bottom + pad, im.height)))
    im.save(os.path.join(_here, name), 'WEBP', quality=92, method=6)
    print(f'  ok  {name}  {im.width}x{im.height}')


# ═══════════════════════════════════════════════════════════════
# Symptom → fix map (agenda)
# ═══════════════════════════════════════════════════════════════
def make_failure_modes():
    fig, ax = new_fig(12, 4.9)
    rows = [
        ('Built the wrong thing, or rediscovers\nthe same fact every session', 'Tell Claude what it can\'t see', CLAY),
        ('Said it was done, and it wasn\'t', 'Give Claude a check to run', GRN),
        ('Did a "never", or skipped an "always"', 'Enforce rules with no exceptions', BLU),
        ('Got it right, but cost too much\ntime, tokens, or prompts', 'Change a default', AMB),
    ]
    heading(ax, 2.9, 4.65, 'What you see')
    heading(ax, 9.0, 4.65, 'What to fix')
    for i, (sym, fix, col) in enumerate(rows):
        y = 3.85 - i * 1.12
        box(ax, 2.9, y, 5.4, 0.92, GRY, sym, fs=17)
        arr(ax, 5.72, y, 6.28, y)
        box(ax, 9.0, y, 5.2, 0.92, col, f'{i + 1}.  {fix}', fs=19)
    save(fig, 'diag-01-failure-modes.webp')




# ═══════════════════════════════════════════════════════════════
# What to write down: the two-question test
# ═══════════════════════════════════════════════════════════════
def make_write_down():
    fig, ax = new_fig(12, 3.6)
    y = 2.3
    box(ax, 1.25, y, 2.1, 0.95, GRY, 'A fact about\nyour project', fs=17)
    diamond(ax, 4.15, y, 2.9, 1.55, BLU, 'Can Claude find it\nby reading the code?', fs=15)
    diamond(ax, 7.85, y, 2.9, 1.55, BLU, 'Would it actually\ngo and look?', fs=15)
    box(ax, 10.9, y, 1.9, 0.95, GRY, 'Leave it out', fs=18)
    arr(ax, 2.3, y, 2.7, y)
    arr(ax, 5.6, y, 6.4, y)
    lbl(ax, 6.0, y + 0.3, 'yes', fs=15)
    arr(ax, 9.3, y, 9.95, y)
    lbl(ax, 9.62, y + 0.3, 'yes', fs=15)
    box(ax, 6.0, 0.45, 5.2, 0.62, CLAY, 'Write it down', fs=18)
    arr(ax, 4.15, y - 0.775, 4.6, 0.76)
    arr(ax, 7.85, y - 0.775, 7.4, 0.76)
    lbl(ax, 4.05, 1.08, 'no', fs=15)
    lbl(ax, 7.95, 1.08, 'no', fs=15)
    save(fig, 'diag-03-write-down.webp')




# ═══════════════════════════════════════════════════════════════
# Brainstorm first: interview → spec → fresh build → review
# ═══════════════════════════════════════════════════════════════
def make_spec_flow():
    fig, ax = new_fig(12, 3.4)
    y = 2.2
    steps = [
        (1.5, PUR, '"Interview me"', 'Claude asks until\nit could write the spec'),
        (4.5, CLAY, 'SPEC.md', 'written definition\nof done'),
        (7.5, BLU, 'Fresh session', '/clear, then\nbuild from SPEC.md'),
        (10.5, GRN, 'Reviewer', 'diff checked\nagainst SPEC.md'),
    ]
    for x, col, head, sub in steps:
        box(ax, x, y, 2.5, 1.45, col, head, fs=19, sub=sub, sfs=15,
            mono=head == 'SPEC.md', sub_mono=head in ('Fresh session', 'Reviewer'))
    for i in range(3):
        arr(ax, steps[i][0] + 1.27, y, steps[i + 1][0] - 1.27, y)
    line(ax, [4.5, 4.5, 10.5], [y - 0.73, 0.75, 0.75], ls='--')
    arr(ax, 10.5, 0.75, 10.5, y - 0.73, ls='--')
    lbl(ax, 7.5, 0.48, 'the same spec is the review checklist', fs=15)
    save(fig, 'diag-05-spec-flow.webp')


# ═══════════════════════════════════════════════════════════════
# Check strictness ladder
# ═══════════════════════════════════════════════════════════════
def make_check_ladder():
    fig, ax = new_fig(12, 4.4)
    steps = [
        (2.0, 0.95, GRY, 'In the prompt', '"keep going until\nthe auth tests pass"'),
        (6.0, 2.0, AMB, '/goal', 'a separate model checks\nthe condition every turn'),
        (10.0, 3.05, GRN, 'Stop hook', 'exit code 2 sends\nClaude back to work'),
    ]
    for x, y, col, head, sub in steps:
        box(ax, x, y, 3.5, 1.2, col, head, fs=20, sub=sub, sfs=15,
            mono=head in ('/goal', 'Stop hook'))
    arr(ax, 3.8, 1.25, 4.2, 1.7)
    arr(ax, 7.8, 2.3, 8.2, 2.75)
    lbl(ax, 0.3, 3.75, 'Claude decides when it is done', ha='left', fs=16)
    lbl(ax, 11.7, 0.95, 'Claude Code enforces it', ha='right', fs=16)
    lbl(ax, 11.7, 0.6, '(the harness, not the model)', ha='right', fs=14)
    save(fig, 'diag-06-check-ladder.webp')


# ═══════════════════════════════════════════════════════════════
# Guidance vs enforcement
# ═══════════════════════════════════════════════════════════════
def make_two_kinds():
    fig, ax = new_fig(12, 4.3)
    heading(ax, 2.9, 4.05, 'Claude decides')
    heading(ax, 9.1, 4.05, 'Claude Code enforces')
    left = ['Your prompt', 'CLAUDE.md', 'Skills Claude picks up', 'Auto mode classifier']
    right = ['Hooks', 'Permission deny rules', 'Sandbox (strict mode)', 'Managed settings']
    for i, (l, r) in enumerate(zip(left, right)):
        y = 3.4 - i * 0.72
        box(ax, 2.9, y, 4.6, 0.58, CLAY, l, fs=17, mono=l == 'CLAUDE.md')
        box(ax, 9.1, y, 4.6, 0.58, BLU, r, fs=17)
    lbl(ax, 2.9, 0.55, 'followed almost every time', fs=16)
    lbl(ax, 9.1, 0.55, 'applied every time', fs=16)
    arr(ax, 5.5, 2.95, 6.5, 2.95, col=CLAY)
    lbl(ax, 6.0, 3.3, 'must never\nbend', fs=14, col='#A3482A')
    arr(ax, 6.5, 1.6, 5.5, 1.6, col=BLU)
    lbl(ax, 6.0, 1.25, 'only a\npreference', fs=14, col='#2F5C8F')
    save(fig, 'diag-07-two-kinds.webp')


# ═══════════════════════════════════════════════════════════════
# Permission spectrum
# ═══════════════════════════════════════════════════════════════
def make_permissions():
    fig, ax = new_fig(12, 3.8)
    line(ax, [0.6, 11.4], [2.9, 2.9], col=GRY, lw=6)
    pts = [
        (1.8, GRY, 'Manual', 'you approve every\nnon-read action'),
        (6.0, GRN, 'Auto  (default)', 'a classifier blocks\nrisky actions'),
        (10.2, RED, 'Bypass', 'approves everything\nnot denied'),
    ]
    for x, col, head, sub in pts:
        ax.add_patch(plt.Circle((x, 2.9), 0.17, facecolor=FILL[col], edgecolor=col,
                                lw=2, zorder=4))
        ax.text(x, 3.4, head, ha='center', va='center', fontsize=19, weight=600,
                color=TXT)
        lbl(ax, x, 2.15, sub, fs=15)
    lbl(ax, 1.8, 1.4, 'prompt fatigue: you stop reading', fs=14, col='#A83A2E')
    lbl(ax, 10.2, 1.4, 'disposable containers only', fs=14, col='#A83A2E')
    box(ax, 6.0, 0.55, 10.8, 0.6, BLU, 'Deny rules and the sandbox hold in every mode', fs=17)
    save(fig, 'diag-08-permissions.webp')


# ═══════════════════════════════════════════════════════════════
# Effort dial
# ═══════════════════════════════════════════════════════════════
def make_effort():
    fig, ax = new_fig(12, 3.3)
    levels = [
        ('low', GRY, 'quick back-and-forth,\nfirst sketches'),
        ('medium', GRN, 'default: everyday\nwork with clear scope'),
        ('high', AMB, 'easy-to-miss cases,\ncode you didn\'t write'),
        ('xhigh', AMB, 'flaky tests,\nschema changes'),
        ('max', RED, 'hard problems Claude\nworks on alone'),
    ]
    w = 2.25
    for i, (name, col, sub) in enumerate(levels):
        x = 0.45 + w / 2 + i * (w + 0.06)
        ax.add_patch(FancyBboxPatch((x - w/2, 2.15), w, 0.75,
                                    boxstyle='round,pad=0,rounding_size=0.08',
                                    facecolor=FILL[col], edgecolor=col, lw=1.6, zorder=3))
        ax.text(x, 2.52, name, ha='center', va='center', fontsize=19, family=MONO,
                color=TXT, zorder=4)
        lbl(ax, x, 1.45, sub, fs=14)
    arr(ax, 0.45, 0.55, 11.95, 0.55, lw=1.4)
    lbl(ax, 0.45, 0.25, 'faster, cheaper', ha='left', fs=14)
    lbl(ax, 11.95, 0.25, 'more checking, more tokens', ha='right', fs=14)
    save(fig, 'diag-09-effort.webp')


# ═══════════════════════════════════════════════════════════════
# Subagents: what they buy and what they cost
# ═══════════════════════════════════════════════════════════════
def make_subagents():
    fig, ax = new_fig(12, 4.2)
    box(ax, 6.0, 3.65, 5.0, 0.7, PUR, 'Main session', fs=19)
    agents = [
        (2.0, BLU, 'Parallel work', 'independent pieces\nfinish sooner'),
        (6.0, AMB, 'Noisy output', 'test runs and wide\nsearches stay out'),
        (10.0, GRN, 'Fresh reviewer', 'never saw how the\ncode was written'),
    ]
    for x, col, head, sub in agents:
        box(ax, x, 1.95, 3.4, 1.3, col, head, fs=19, sub=sub, sfs=15)
        arr(ax, 6.0 + (x - 6.0) * 0.4, 3.28, x, 2.62)
    box(ax, 6.0, 0.45, 11.0, 0.58, RED,
        'Cost: every subagent sends its own requests.  Same model, so not a smarter answer.', fs=15, ls='--')
    save(fig, 'diag-10-subagents.webp')


# ═══════════════════════════════════════════════════════════════
# Steering a session
# ═══════════════════════════════════════════════════════════════
def make_steer():
    fig, ax = new_fig(12, 2.9)
    y = 1.75
    box(ax, 1.5, y, 2.5, 1.2, GRY, 'Watch the\nfirst minute', fs=18)
    box(ax, 4.6, y, 2.6, 1.2, AMB, 'Esc', sub='stop, keep work,\nredirect', fs=20, sfs=14, mono=True)
    box(ax, 7.6, y, 2.6, 1.2, BLU, 'Esc Esc', sub='rewind code and\nconversation', fs=20, sfs=14, mono=True)
    box(ax, 10.6, y, 2.6, 1.2, CLAY, '/clear', sub='one better prompt,\nnot a third fix', fs=20, sfs=14, mono=True)
    arr(ax, 2.8, y, 3.25, y)
    arr(ax, 5.95, y, 6.25, y)
    arr(ax, 8.95, y, 9.25, y)
    lbl(ax, 3.05, y + 0.85, 'drifts?', fs=14)
    lbl(ax, 6.1, y + 0.85, 'wrong turn?', fs=14)
    lbl(ax, 9.1, y + 0.85, 'still wrong?', fs=14)
    lbl(ax, 6.0, 0.55, 'Checkpoints track Claude\'s file edits, not changes made by Bash commands; keep using git.', fs=14)
    save(fig, 'diag-11-steer.webp')


# ═══════════════════════════════════════════════════════════════
# Git worktrees: parallel isolation
# ═══════════════════════════════════════════════════════════════
def make_worktrees():
    fig, ax = new_fig(12, 4.1)
    xs = [2.1, 6.0, 9.9]
    box(ax, 6.0, 3.6, 7.0, 0.68, GRY, '.git/  shared history, refs, and remotes', fs=18, mono=True)
    for x, (col, name) in zip(xs, [(GRN, 'ui'), (BLU, 'auth'), (AMB, 'bugfix')]):
        box(ax, x, 2.1, 3.5, 1.05, col, f'.claude/worktrees/{name}', fs=15, mono=True,
            sub=f'own branch, own files', sfs=14)
        box(ax, x, 0.5, 3.5, 0.62, col, f'claude -w {name}', fs=16, mono=True)
        arr(ax, x, 1.57, x, 0.84)
    arr(ax, 3.2, 3.25, 2.1, 2.65, rad=0.15)
    arr(ax, 6.0, 3.25, 6.0, 2.65)
    arr(ax, 8.8, 3.25, 9.9, 2.65, rad=-0.15)
    save(fig, 'diag-12-worktrees.webp')




# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('Generating diagrams...')
    make_failure_modes(); make_write_down()
    make_spec_flow(); make_check_ladder(); make_two_kinds(); make_permissions()
    make_effort(); make_subagents(); make_steer(); make_worktrees()
    print('All done.')
