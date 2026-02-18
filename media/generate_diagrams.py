"""
Hand-drawn style diagrams for effective-claude-code-usage slides.
Font: Caveat (Google Fonts) — same family Excalidraw uses as its Virgil fallback.
Run from the project root: uv run python media/generate_diagrams.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib import font_manager
import numpy as np
import os

# ── Register Caveat font ──────────────────────────────────────
_here = os.path.dirname(os.path.abspath(__file__))
font_manager.fontManager.addfont(os.path.join(_here, 'Caveat.ttf'))
plt.rcParams['font.family'] = 'Caveat'

# ── Colour palette ────────────────────────────────────────────
BG   = '#0d1117'
GRN  = '#22c55e'; DGRN = '#14532d'
BLU  = '#38bdf8'; DBLU = '#0c2a3a'
AMB  = '#f59e0b'; DAMB = '#3a2400'
PUR  = '#a78bfa'; DPUR = '#2d1b69'
RED  = '#f87171'; DRED = '#450a0a'
TXT  = '#e6edf3'
MUT  = '#8b949e'
CARD = '#1c2128'
DPI  = 150

# ── Drawing helpers ───────────────────────────────────────────

def new_fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, w); ax.set_ylim(0, h)
    ax.axis('off')
    return fig, ax


def box(ax, x, y, w, h, fc, label, fs=13, tc='auto', lw=2.0, ec=None, alpha=1.0):
    """Rounded rectangle with centred label."""
    if tc == 'auto':
        tc = BG if fc not in (CARD, BG, DGRN, DBLU, DAMB, DPUR, DRED) else TXT
    if ec is None:
        ec = TXT
    p = FancyBboxPatch((x - w/2, y - h/2), w, h,
                        boxstyle='round,pad=0.07',
                        facecolor=fc, edgecolor=ec,
                        linewidth=lw, alpha=alpha, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=fs, color=tc, fontweight='bold',
            zorder=4, linespacing=1.35)


def diamond(ax, x, y, w, h, fc, label, fs=12, tc='auto', lw=2.0):
    """Draw a diamond shape with label."""
    if tc == 'auto':
        tc = BG
    verts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
    poly = Polygon(verts, closed=True, facecolor=fc, edgecolor=TXT,
                   linewidth=lw, zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=fs, color=tc, fontweight='bold', zorder=4, linespacing=1.3)


def arr(ax, x1, y1, x2, y2, col=MUT, lw=2.0, rad=0.0, style='->', ms=16):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=col, lw=lw,
                                mutation_scale=ms,
                                connectionstyle=f'arc3,rad={rad}'),
                zorder=2)


def lbl(ax, x, y, text, col=MUT, fs=10, bold=False, ha='center'):
    ax.text(x, y, text, ha=ha, va='center', fontsize=fs, color=col,
            style='italic' if not bold else 'normal',
            fontweight='bold' if bold else 'normal')


def group_bg(ax, x, y, w, h, fc, ec, alpha=0.12, lw=1.5, label='', lfs=12):
    r = FancyBboxPatch((x - w/2, y - h/2), w, h,
                        boxstyle='round,pad=0.1',
                        facecolor=fc, edgecolor=ec,
                        linewidth=lw, alpha=alpha, zorder=1)
    ax.add_patch(r)
    if label:
        ax.text(x, y + h/2 - 0.22, label, ha='center', va='top',
                fontsize=lfs, color=ec, fontweight='bold', alpha=0.9, zorder=2)


def title(ax, w, h, text, col=GRN, fs=18, y_off=0.28):
    ax.text(w/2, h - y_off, text, ha='center', va='top',
            fontsize=fs, color=col, fontweight='bold', zorder=5)


def save(fig, name):
    path = os.path.join(_here, name)
    plt.tight_layout(pad=0.1)
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ✓  {name}')


# ═══════════════════════════════════════════════════════════════
# 1 — Intelligence Spectrum
# ═══════════════════════════════════════════════════════════════
def make_01():
    fig, ax = new_fig(11, 4.6)
    title(ax, 11, 4.6, 'Intelligence Spectrum', col=GRN)

    groups = [
        (1.85, MUT,  '#8b949e', 'Tab\nCompletion'),
        (5.50, BLU,  DBLU,      'Chatbot\n(LLM)'),
        (9.15, GRN,  DGRN,      'Agent\n(Claude Code)'),
    ]
    for gx, ec, fc, glbl in groups:
        group_bg(ax, gx, 2.05, 3.2, 2.9, fc, ec, alpha=0.14, label=glbl, lfs=13)

    # Tab Completion boxes
    box(ax, 1.85, 2.65, 2.6, 0.7, '#21262d', 'Predict next token', fs=12, tc=MUT, ec='#30363d')
    box(ax, 1.85, 1.65, 2.6, 0.7, '#21262d', 'No context / world state', fs=12, tc=MUT, ec='#30363d')

    # Chatbot boxes
    box(ax, 5.50, 2.65, 2.6, 0.7, DBLU, 'Understand prompt', fs=12, tc=BLU)
    box(ax, 5.50, 1.65, 2.6, 0.7, DBLU, 'One-shot response', fs=12, tc=BLU)

    # Agent boxes (3 items)
    box(ax, 9.15, 3.00, 2.6, 0.60, DGRN, 'Perceive context', fs=11, tc=GRN)
    box(ax, 9.15, 2.15, 2.6, 0.60, DGRN, 'Plan & use tools', fs=11, tc=GRN)
    box(ax, 9.15, 1.30, 2.6, 0.60, DGRN, 'Loop until done', fs=11, tc=GRN)

    # Progression arrow across the top
    ax.annotate('', xy=(10.5, 4.15), xytext=(0.5, 4.15),
                arrowprops=dict(arrowstyle='->', color=MUT, lw=2.0,
                                mutation_scale=18,
                                connectionstyle='arc3,rad=0.0'), zorder=2)
    lbl(ax, 5.5, 4.30, 'increasing capability  &  autonomy', col=MUT, fs=11)

    save(fig, 'diag-01-intelligence-spectrum.png')


# ═══════════════════════════════════════════════════════════════
# 2 — ReAct Agent Loop
# ═══════════════════════════════════════════════════════════════
def make_02():
    fig, ax = new_fig(11, 4.2)
    title(ax, 11, 4.2, 'The ReAct Agent Loop', col=GRN)

    nodes = [
        (0.9,  2.4, DPUR, PUR,  'New\nTask'),
        (2.55, 2.4, DBLU, BLU,  'Perceive\ncontext'),
        (4.20, 2.4, DGRN, GRN,  'Think\nreason'),
        (5.85, 2.4, DAMB, AMB,  'Act\nuse tool'),
        (7.50, 2.4, DBLU, BLU,  'Observe\noutput'),
    ]
    bw, bh = 1.40, 0.85
    for x, y, fc, tc, lbl_text in nodes:
        box(ax, x, y, bw, bh, fc, lbl_text, fs=12, tc=tc)

    # Forward arrows between nodes
    for i in range(len(nodes) - 1):
        x1 = nodes[i][0] + bw/2
        x2 = nodes[i+1][0] - bw/2
        arr(ax, x1, 2.4, x2, 2.4, col=TXT, lw=2.0)

    # Loop-back arc: Observe → Think
    loop_y = 1.35
    ax.plot([4.20, 4.20], [loop_y, 1.97], color=MUT, lw=1.8, zorder=2)
    ax.plot([7.50, 7.50], [loop_y, 1.97], color=MUT, lw=1.8, zorder=2)
    ax.plot([4.20, 7.50], [loop_y, loop_y], color=MUT, lw=1.8, zorder=2)
    ax.annotate('', xy=(4.20, 1.97), xytext=(4.20, loop_y + 0.01),
                arrowprops=dict(arrowstyle='->', color=MUT, lw=1.8,
                                mutation_scale=14), zorder=2)
    lbl(ax, 5.85, 1.08, 'not done — loop back', col=MUT, fs=10.5)

    # Done exit arrow + box
    arr(ax, 8.20, 2.4, 8.60, 2.4, col=GRN, lw=2.0)
    lbl(ax, 8.40, 2.72, 'done', col=GRN, fs=10)
    box(ax, 9.55, 2.4, 1.55, 0.75, DGRN, 'Return\nresult', fs=12, tc=GRN)

    # "done?" label at the branch point
    lbl(ax, 8.40, 2.4, '?', col=GRN, fs=14, bold=True)

    save(fig, 'diag-02-react-loop.png')


# ═══════════════════════════════════════════════════════════════
# 3 — Tool Ecosystem
# ═══════════════════════════════════════════════════════════════
def make_03():
    fig, ax = new_fig(11, 4.6)
    title(ax, 11, 4.6, 'Tool Ecosystem', col=GRN)

    # Centre hub
    cx, cy = 5.5, 2.2
    box(ax, cx, cy, 1.9, 1.0, DGRN, 'Claude\nCode', fs=15, tc=GRN, lw=2.5)

    # Tools: (x, y, fc, tc, title, subtitle)
    tools = [
        (1.5,  3.5, DBLU, BLU, 'File I/O',    'Read · Write\nEdit · Glob'),
        (1.5,  0.9, DAMB, AMB, 'Shell',         'Bash · any\nterminal cmd'),
        (5.5,  3.8, DPUR, PUR, 'Search',        'Grep · WebSearch\nWebFetch'),
        (9.5,  3.5, '#3a1515', RED, 'MCP',       'GitHub · Jira\nCustom servers'),
        (9.5,  0.9, DGRN, GRN, 'Agents',        'Task · spawn\nsubagents'),
    ]
    for tx, ty, fc, tc, t_title, t_sub in tools:
        # title box + subtitle text
        box(ax, tx, ty + 0.18, 2.6, 0.55, fc, t_title, fs=12.5, tc=tc, lw=1.8)
        ax.text(tx, ty - 0.28, t_sub, ha='center', va='center',
                fontsize=10, color=MUT, linespacing=1.3, zorder=4)
        # arrow from tool → Claude Code
        # compute start/end on borders
        dx = cx - tx; dy = cy - ty
        dist = (dx**2 + dy**2)**0.5
        # start slightly inside the tool box edge
        sx = tx + (dx/dist) * 1.35
        sy = ty + (dy/dist) * 0.55
        # end on the Claude Code box edge
        ex = cx - (dx/dist) * 1.0
        ey = cy - (dy/dist) * 0.55
        arr(ax, sx, sy, ex, ey, col=MUT, lw=1.6, ms=13)

    save(fig, 'diag-03-tool-ecosystem.png')


# ═══════════════════════════════════════════════════════════════
# 4 — Context Window
# ═══════════════════════════════════════════════════════════════
def make_04():
    fig, ax = new_fig(11, 3.6)
    title(ax, 11, 3.6, 'What Fills the Context Window?', col=GRN)

    inputs = [
        (1.35, 3.05, DPUR, PUR, 'CLAUDE.md'),
        (1.35, 2.38, DBLU, BLU, 'Conversation History'),
        (1.35, 1.71, DGRN, GRN, 'File Contents'),
        (1.35, 1.04, DAMB, AMB, 'Tool Outputs'),
        (1.35, 0.37, DRED, RED, 'Images'),
    ]
    iw, ih = 2.45, 0.5
    for ix, iy, fc, tc, ilbl in inputs:
        box(ax, ix, iy, iw, ih, fc, ilbl, fs=11.5, tc=tc, lw=1.8)

    # Context Window (big box)
    cwx, cwy = 6.2, 1.71
    box(ax, cwx, cwy, 2.6, 3.1, DGRN, 'Context\nWindow\n~200K tokens',
        fs=14, tc=GRN, lw=2.5)

    # Model box
    mx = 9.8
    box(ax, mx, cwy, 1.8, 0.8, DBLU, 'Model\nreasoning', fs=12, tc=BLU, lw=1.8)

    # Arrows: each input → context window
    for ix, iy, *_ in inputs:
        arr(ax, ix + iw/2, iy, cwx - 1.35, cwy + (iy - cwy) * 0.55,
            col=MUT, lw=1.5, ms=13)

    # Arrow: context → model
    arr(ax, cwx + 1.3, cwy, mx - 0.9, cwy, col=GRN, lw=2.0)

    save(fig, 'diag-04-context-window.png')


# ═══════════════════════════════════════════════════════════════
# 5 — CLAUDE.md Loading
# ═══════════════════════════════════════════════════════════════
def make_05():
    fig, ax = new_fig(9, 5.4)
    title(ax, 9, 5.4, 'How CLAUDE.md Is Loaded', col=GRN)

    # Invoke
    box(ax, 4.5, 4.85, 2.8, 0.65, DPUR, 'claude invoked', fs=13, tc=PUR, lw=2.2)

    # Two main branches
    box(ax, 2.0, 3.55, 3.2, 0.65, DBLU, '~/.claude/CLAUDE.md\n(global)', fs=12, tc=BLU)
    box(ax, 7.0, 3.55, 3.2, 0.65, DGRN, './CLAUDE.md\n(project root)', fs=12, tc=GRN)

    # Sub-branches from ./CLAUDE.md
    box(ax, 5.5, 2.15, 2.9, 0.65, DAMB, 'Subdirectory\nCLAUDE.md', fs=11.5, tc=AMB)
    box(ax, 8.5, 2.15, 2.7, 0.65, DBLU, '@import\nsnippets', fs=11.5, tc=BLU)

    # Merged system prompt
    box(ax, 4.5, 0.75, 5.5, 0.72, DGRN, 'Merged System Prompt  (injected every turn)',
        fs=12.5, tc=GRN, lw=2.5)

    # Arrows invoke → branches
    arr(ax, 3.35, 4.85, 2.0, 3.88, col=MUT, lw=1.8)
    arr(ax, 5.65, 4.85, 7.0, 3.88, col=MUT, lw=1.8)

    # Arrows ./CLAUDE.md → sub-branches
    arr(ax, 6.0, 3.22, 5.5, 2.48, col=MUT, lw=1.6)
    arr(ax, 8.0, 3.22, 8.5, 2.48, col=MUT, lw=1.6)

    # All four → merged
    for sx, sy in [(2.0, 3.22), (7.0, 3.22), (5.5, 1.82), (8.5, 1.82)]:
        arr(ax, sx, sy, 4.5 + (sx - 4.5)*0.15, 1.12, col=MUT, lw=1.6, ms=13)

    save(fig, 'diag-05-claude-md-loading.png')


# ═══════════════════════════════════════════════════════════════
# 6 — Subagent Orchestration
# ═══════════════════════════════════════════════════════════════
def make_06():
    fig, ax = new_fig(11, 4.8)
    title(ax, 11, 4.8, 'Subagent Orchestration', col=GRN)

    xs = [1.8, 4.2, 6.8, 9.2]
    task_labels  = ['Write\nunit tests', 'Update\ndocs', 'Refactor\nauth', 'Audit\ndeps']
    agent_labels = ['Subagent 1\nisolated ctx', 'Subagent 2\nisolated ctx',
                    'Subagent 3\nisolated ctx', 'Subagent 4\nisolated ctx']

    # Orchestrator
    cx = 5.5
    box(ax, cx, 4.25, 4.0, 0.72, DPUR, 'Orchestrator  (main Claude session)',
        fs=13, tc=PUR, lw=2.5)

    # Task boxes
    for x, lbl_text in zip(xs, task_labels):
        box(ax, x, 2.95, 1.85, 0.75, DBLU, lbl_text, fs=11.5, tc=BLU)
        arr(ax, cx + (x - cx)*0.38, 3.89, x, 3.33, col=MUT, lw=1.7, ms=13)

    # Subagent boxes
    for x, lbl_text in zip(xs, agent_labels):
        box(ax, x, 1.70, 1.85, 0.75, DGRN, lbl_text, fs=11, tc=GRN)
        arr(ax, x, 2.57, x, 2.08, col=MUT, lw=1.7, ms=13)

    # Merge Results
    box(ax, cx, 0.52, 4.8, 0.70, DGRN, 'Merge Results  —  back to Orchestrator',
        fs=12.5, tc=GRN, lw=2.2)
    for x in xs:
        arr(ax, x, 1.32, cx + (x - cx)*0.25, 0.88, col=MUT, lw=1.7, ms=13)

    save(fig, 'diag-06-subagent-orchestration.png')


# ═══════════════════════════════════════════════════════════════
# 7 — Planning Mode Workflow
# ═══════════════════════════════════════════════════════════════
def make_07():
    fig, ax = new_fig(11, 3.2)
    title(ax, 11, 3.2, 'Planning Mode Workflow', col=GRN)

    nodes = [
        (0.80, 1.80, DPUR, PUR,  'Request'),
        (2.35, 1.80, DGRN, GRN,  '/plan\nread-only'),
        (3.95, 1.80, DBLU, BLU,  'Explore\ncodebase'),
        (5.55, 1.80, DAMB, AMB,  'Draft\nplan'),
        (7.15, 1.80, '#1c2128', TXT, 'Human\nReview'),
        (8.75, 1.80, DGRN, GRN,  'Execute\nchanges'),
        (10.35,1.80, DGRN, GRN,  'Done!'),
    ]
    bw, bh = 1.35, 0.80
    for x, y, fc, tc, lbl_text in nodes:
        box(ax, x, y, bw, bh, fc, lbl_text, fs=11.5, tc=tc)

    for i in range(len(nodes) - 1):
        x1 = nodes[i][0] + bw/2
        x2 = nodes[i+1][0] - bw/2
        col = GRN if i >= 4 else TXT
        arr(ax, x1, 1.80, x2, 1.80, col=col, lw=1.9)

    # Refine loop: Review → Draft (below)
    ry, ry2 = 1.08, 1.38
    ax.plot([5.55, 5.55], [ry, ry2], color=AMB, lw=1.8, zorder=2)
    ax.plot([7.15, 7.15], [ry, ry2], color=AMB, lw=1.8, zorder=2)
    ax.plot([5.55, 7.15], [ry, ry], color=AMB, lw=1.8, zorder=2)
    ax.annotate('', xy=(5.55, ry2), xytext=(5.55, ry + 0.01),
                arrowprops=dict(arrowstyle='->', color=AMB, lw=1.8,
                                mutation_scale=13), zorder=2)
    lbl(ax, 6.35, 0.80, 'refine', col=AMB, fs=10.5)

    save(fig, 'diag-07-planning-mode.png')


# ═══════════════════════════════════════════════════════════════
# 8 — CLI vs MCP Token Cost
# ═══════════════════════════════════════════════════════════════
def make_08():
    fig, ax = new_fig(11, 4.0)
    title(ax, 11, 4.0, 'CLI vs MCP — Token Cost', col=GRN)

    # Task box (left)
    box(ax, 1.0, 2.05, 1.55, 0.75, DPUR, 'Same\nTask', fs=13, tc=PUR, lw=2.0)

    # ── CLI path (top) ──
    cli_y = 3.10
    group_bg(ax, 5.8, cli_y, 7.8, 1.05, GRN, GRN, alpha=0.08, lw=1.5,
             label='CLI path', lfs=11)
    box(ax, 3.5,  cli_y, 2.2, 0.62, DGRN, 'gh pr list\n--json ...', fs=11.5, tc=GRN)
    box(ax, 6.0,  cli_y, 2.2, 0.62, DGRN, '~100 tokens\nclean JSON', fs=11.5, tc=GRN)
    arr(ax, 1.78, 2.40, 2.40, cli_y, col=GRN, lw=1.8)
    arr(ax, 4.60, cli_y, 4.90, cli_y, col=GRN, lw=1.8)

    # ── MCP path (bottom) ──
    mcp_y = 1.0
    group_bg(ax, 5.8, mcp_y, 7.8, 1.05, RED, RED, alpha=0.08, lw=1.5,
             label='MCP path', lfs=11)
    box(ax, 3.5,  mcp_y, 2.2, 0.62, DRED, 'MCP server\ncall', fs=11.5, tc=RED)
    box(ax, 6.0,  mcp_y, 2.2, 0.62, DRED, 'Protocol +\nschema wrap', fs=11.5, tc=RED)
    box(ax, 8.5,  mcp_y, 2.2, 0.62, DRED, '2,000+\ntokens', fs=11.5, tc=RED)
    arr(ax, 1.78, 1.70, 2.40, mcp_y, col=RED, lw=1.8)
    arr(ax, 4.60, mcp_y, 4.90, mcp_y, col=RED, lw=1.8)
    arr(ax, 7.10, mcp_y, 7.40, mcp_y, col=RED, lw=1.8)

    # ── Same result (right) ──
    box(ax, 10.2, 2.05, 1.4, 0.75, CARD, 'Same\nresult', fs=12, tc=TXT,
        ec=MUT, lw=1.5)
    arr(ax, 7.10, cli_y, 9.50, 2.40, col=GRN, lw=1.8)
    arr(ax, 9.60, mcp_y, 9.50, 1.70, col=RED, lw=1.8)

    # Token labels
    lbl(ax, 6.0, cli_y + 0.55, 'cheap  (low cost)', col=GRN, fs=10.5)
    lbl(ax, 6.0, mcp_y - 0.45, 'expensive  (high cost)', col=RED, fs=10.5)

    save(fig, 'diag-08-cli-vs-mcp.png')


# ═══════════════════════════════════════════════════════════════
# 9 — Daily Workflow / Mental Model
# ═══════════════════════════════════════════════════════════════
def make_09():
    fig, ax = new_fig(9, 6.0)
    title(ax, 9, 6.0, 'Effective Usage — Mental Model', col=GRN)

    bw, bh = 2.6, 0.65

    # ── New Task ──
    box(ax, 4.5, 5.45, bw, bh, DPUR, 'New Task', fs=13, tc=PUR, lw=2.2)

    # ── CLAUDE.md current? ──
    diamond(ax, 4.5, 4.45, bw + 0.6, 0.80, DBLU, 'CLAUDE.md\ncurrent?',
            fs=11.5, tc=BLU)
    arr(ax, 4.5, 5.12, 4.5, 4.85, col=MUT, lw=1.8)

    # No → Update
    box(ax, 7.5, 4.45, 2.3, 0.65, DAMB, 'Update / /init', fs=12, tc=AMB)
    arr(ax, 5.80, 4.45, 6.34, 4.45, col=AMB, lw=1.8)
    lbl(ax, 6.05, 4.70, 'no', col=AMB, fs=10.5)
    # Update loops back down
    ax.plot([7.5, 8.55, 8.55, 4.5], [4.12, 4.12, 3.65, 3.65], color=AMB, lw=1.5, zorder=2, linestyle='--')

    # Yes → Task size?
    arr(ax, 4.5, 4.05, 4.5, 3.80, col=MUT, lw=1.8)
    lbl(ax, 4.15, 3.92, 'yes', col=GRN, fs=10.5)

    # ── Task size? ──
    diamond(ax, 4.5, 3.45, bw + 0.6, 0.80, DBLU, 'Task\ncomplexity?',
            fs=11.5, tc=BLU)

    # Simple → Direct
    box(ax, 1.3, 3.45, 2.15, 0.65, DGRN, 'Direct\nprompt', fs=12, tc=GRN)
    arr(ax, 3.20, 3.45, 2.38, 3.45, col=GRN, lw=1.8)
    lbl(ax, 2.82, 3.70, 'simple', col=GRN, fs=10)

    # Medium → /plan
    box(ax, 4.5, 2.55, 2.15, 0.65, DGRN, '/plan first', fs=12, tc=GRN)
    arr(ax, 4.5, 3.05, 4.5, 2.88, col=GRN, lw=1.8)
    lbl(ax, 4.15, 2.78, 'medium', col=GRN, fs=10)

    # Large → Subagents
    box(ax, 7.7, 3.45, 2.15, 0.65, DGRN, 'Subagents', fs=12, tc=GRN)
    arr(ax, 5.80, 3.45, 6.62, 3.45, col=GRN, lw=1.8)
    lbl(ax, 6.22, 3.70, 'large', col=GRN, fs=10)

    # All three → Context full?
    ctx_y = 1.75
    for sx, sy in [(1.3, 3.12), (4.5, 2.22), (7.7, 3.12)]:
        tx = 4.5 + (sx - 4.5) * 0.05
        arr(ax, sx, sy, tx, ctx_y + 0.42, col=MUT, lw=1.5, ms=12)

    # ── Context full? ──
    diamond(ax, 4.5, ctx_y, bw + 0.6, 0.80, DBLU, 'Context\nfull?',
            fs=11.5, tc=BLU)

    # Yes → /compact
    box(ax, 7.7, ctx_y, 2.15, 0.65, DAMB, '/compact', fs=13, tc=AMB)
    arr(ax, 5.80, ctx_y, 6.62, ctx_y, col=AMB, lw=1.8)
    lbl(ax, 6.22, ctx_y + 0.25, 'yes', col=AMB, fs=10.5)
    # compact loops back
    ax.plot([7.7, 8.55, 8.55, 4.5], [ctx_y - 0.33, ctx_y - 0.33, 0.88, 0.88],
            color=AMB, lw=1.5, linestyle='--', zorder=2)

    # No → Done
    arr(ax, 4.5, ctx_y - 0.40, 4.5, 0.78, col=GRN, lw=1.8)
    lbl(ax, 4.15, ctx_y - 0.55, 'no', col=GRN, fs=10.5)
    box(ax, 4.5, 0.52, 2.6, 0.65, DGRN, 'Done!', fs=14, tc=GRN, lw=2.5)

    save(fig, 'diag-09-mental-model.png')


# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('Generating diagrams...')
    make_01()
    make_02()
    make_03()
    make_04()
    make_05()
    make_06()
    make_07()
    make_08()
    make_09()
    print('All done.')
