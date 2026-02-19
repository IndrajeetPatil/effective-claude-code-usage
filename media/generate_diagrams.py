"""
Hand-drawn style diagrams for effective-claude-code-usage slides.
Font: Caveat (Google Fonts) — same family Excalidraw uses as its Virgil fallback.
Run from the project root: uv run python media/generate_diagrams.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib import font_manager
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

# Lower DPI so RevealJS scaling makes text appear larger, not tinier.
# At DPI=100, an 11-inch figure = 1100 px → displayed at ~95% native in a 1050px slide.
DPI = 100

# ── Drawing helpers ───────────────────────────────────────────

def new_fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis('off')
    return fig, ax


def box(ax, x, y, w, h, fc, label, fs=18, tc='auto', lw=2.2, ec=None):
    """Rounded rectangle with centred label. fs is in points."""
    if tc == 'auto':
        tc = BG if fc not in (CARD, BG, DGRN, DBLU, DAMB, DPUR, DRED) else TXT
    if ec is None:
        ec = TXT
    p = FancyBboxPatch((x - w/2, y - h/2), w, h,
                        boxstyle='round,pad=0.04',
                        facecolor=fc, edgecolor=ec,
                        linewidth=lw, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=fs, color=tc, fontweight='bold',
            zorder=4, linespacing=1.2)


def diamond(ax, x, y, w, h, fc, label, fs=17, tc='auto', lw=2.2):
    """Diamond decision shape with centred label."""
    if tc == 'auto':
        tc = BG
    verts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
    poly = Polygon(verts, closed=True, facecolor=fc, edgecolor=TXT,
                   linewidth=lw, zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=fs, color=tc, fontweight='bold',
            zorder=4, linespacing=1.2)


def arr(ax, x1, y1, x2, y2, col=MUT, lw=2.2, rad=0.0, ms=18):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=col, lw=lw,
                                mutation_scale=ms,
                                connectionstyle=f'arc3,rad={rad}'),
                zorder=2)


def lbl(ax, x, y, text, col=MUT, fs=14):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fs, color=col, style='italic', zorder=5)


def group_bg(ax, x, y, w, h, fc, ec, alpha=0.12, lw=1.5, label='', lfs=17):
    r = FancyBboxPatch((x - w/2, y - h/2), w, h,
                        boxstyle='round,pad=0.1',
                        facecolor=fc, edgecolor=ec,
                        linewidth=lw, alpha=alpha, zorder=1)
    ax.add_patch(r)
    if label:
        ax.text(x, y + h/2 - 0.18, label, ha='center', va='top',
                fontsize=lfs, color=ec, fontweight='bold', alpha=0.9, zorder=2)


def title(ax, w, h, text, col=GRN, fs=26, y_off=0.25):
    ax.text(w/2, h - y_off, text, ha='center', va='top',
            fontsize=fs, color=col, fontweight='bold', zorder=5)


def save(fig, name):
    path = os.path.join(_here, name)
    plt.tight_layout(pad=0.05)
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  ok  {name}')


# ═══════════════════════════════════════════════════════════════
# 1 — Intelligence Spectrum
# ═══════════════════════════════════════════════════════════════
def make_01():
    fig, ax = new_fig(11, 5.0)
    title(ax, 11, 5.0, 'Intelligence Spectrum')

    # Group backgrounds
    groups = [
        (1.85, MUT,  '#8b949e', 'Tab Completion'),
        (5.50, BLU,  DBLU,      'Chatbot (LLM)'),
        (9.15, GRN,  DGRN,      'Agent (Claude Code)'),
    ]
    for gx, ec, fc, glbl in groups:
        group_bg(ax, gx, 2.15, 3.2, 3.2, fc, ec, alpha=0.14, label=glbl, lfs=17)

    # Tab Completion
    box(ax, 1.85, 2.80, 2.65, 0.80, '#21262d', 'Predict next token', fs=17, tc=MUT, ec='#30363d')
    box(ax, 1.85, 1.65, 2.65, 0.80, '#21262d', 'No context\nor world state', fs=17, tc=MUT, ec='#30363d')

    # Chatbot
    box(ax, 5.50, 2.80, 2.65, 0.80, DBLU, 'Understand prompt', fs=17, tc=BLU)
    box(ax, 5.50, 1.65, 2.65, 0.80, DBLU, 'One-shot response', fs=17, tc=BLU)

    # Agent (3 boxes)
    box(ax, 9.15, 3.10, 2.65, 0.70, DGRN, 'Perceive context', fs=16, tc=GRN)
    box(ax, 9.15, 2.25, 2.65, 0.70, DGRN, 'Plan & use tools', fs=16, tc=GRN)
    box(ax, 9.15, 1.40, 2.65, 0.70, DGRN, 'Loop until done',  fs=16, tc=GRN)

    # Progression arrow
    ax.annotate('', xy=(10.6, 4.55), xytext=(0.4, 4.55),
                arrowprops=dict(arrowstyle='->', color=MUT, lw=2.0,
                                mutation_scale=18, connectionstyle='arc3,rad=0.0'),
                zorder=2)
    lbl(ax, 5.5, 4.72, 'increasing capability  &  autonomy', col=MUT, fs=14)

    save(fig, 'diag-01-intelligence-spectrum.png')


# ═══════════════════════════════════════════════════════════════
# 2 — ReAct Agent Loop
# ═══════════════════════════════════════════════════════════════
def make_02():
    fig, ax = new_fig(11, 4.5)
    title(ax, 11, 4.5, 'The ReAct Agent Loop')

    nodes = [
        (0.95, 2.55, DPUR, PUR, 'New\nTask'),
        (2.65, 2.55, DBLU, BLU, 'Perceive\ncontext'),
        (4.35, 2.55, DGRN, GRN, 'Think\nreason'),
        (6.05, 2.55, DAMB, AMB, 'Act\nuse tool'),
        (7.75, 2.55, DBLU, BLU, 'Observe\noutput'),
    ]
    bw, bh = 1.45, 1.00
    for x, y, fc, tc, lbl_text in nodes:
        box(ax, x, y, bw, bh, fc, lbl_text, fs=18, tc=tc)

    for i in range(len(nodes) - 1):
        arr(ax, nodes[i][0] + bw/2, 2.55, nodes[i+1][0] - bw/2, 2.55, col=TXT)

    # Loop-back
    loop_y = 1.28
    ax.plot([4.35, 4.35], [loop_y, 2.05], color=MUT, lw=2.0, zorder=2)
    ax.plot([7.75, 7.75], [loop_y, 2.05], color=MUT, lw=2.0, zorder=2)
    ax.plot([4.35, 7.75], [loop_y, loop_y], color=MUT, lw=2.0, zorder=2)
    ax.annotate('', xy=(4.35, 2.05), xytext=(4.35, loop_y + 0.01),
                arrowprops=dict(arrowstyle='->', color=MUT, lw=2.0, mutation_scale=15),
                zorder=2)
    lbl(ax, 6.05, 0.95, 'not done — loop back', col=MUT, fs=14)

    # Done exit
    arr(ax, 8.48, 2.55, 8.85, 2.55, col=GRN, lw=2.2)
    lbl(ax, 8.65, 2.92, 'done', col=GRN, fs=13)
    box(ax, 10.05, 2.55, 1.85, 0.90, DGRN, 'Return\nresult', fs=18, tc=GRN)

    save(fig, 'diag-02-react-loop.png')


# ═══════════════════════════════════════════════════════════════
# 3 — Tool Ecosystem
# ═══════════════════════════════════════════════════════════════
def make_03():
    fig, ax = new_fig(11, 5.2)
    title(ax, 11, 5.2, 'Tool Ecosystem')

    cx, cy = 5.5, 2.55
    box(ax, cx, cy, 2.1, 1.10, DGRN, 'Claude\nCode', fs=22, tc=GRN, lw=2.8)

    tools = [
        (1.55, 3.90, DBLU, BLU, 'File I/O',  'Read · Write\nEdit · Glob'),
        (1.55, 1.20, DAMB, AMB, 'Shell',      'Bash · any\nterminal cmd'),
        (5.50, 4.55, DPUR, PUR, 'Search',     'Grep · WebSearch\nWebFetch'),
        (9.45, 3.90, DRED, RED, 'MCP',        'GitHub · Jira\nCustom servers'),
        (9.45, 1.20, DGRN, GRN, 'Agents',     'Task · spawn\nsubagents'),
    ]
    for tx, ty, fc, tc, t_title, t_sub in tools:
        box(ax, tx, ty + 0.22, 2.65, 0.70, fc, t_title, fs=18, tc=tc, lw=2.0)
        ax.text(tx, ty - 0.38, t_sub, ha='center', va='center',
                fontsize=14, color=MUT, linespacing=1.2, zorder=4)
        dx, dy = cx - tx, cy - ty
        dist = (dx**2 + dy**2)**0.5
        sx = tx + (dx/dist) * 1.40
        sy = ty + (dy/dist) * 0.62
        ex = cx - (dx/dist) * 1.10
        ey = cy - (dy/dist) * 0.60
        arr(ax, sx, sy, ex, ey, col=MUT, lw=1.8, ms=14)

    save(fig, 'diag-03-tool-ecosystem.png')


# ═══════════════════════════════════════════════════════════════
# 4 — Context Window
# ═══════════════════════════════════════════════════════════════
def make_04():
    fig, ax = new_fig(11, 4.2)
    title(ax, 11, 4.2, 'What Fills the Context Window?')

    inputs = [
        (1.40, 3.50, DPUR, PUR, 'CLAUDE.md'),
        (1.40, 2.75, DBLU, BLU, 'Conversation History'),
        (1.40, 2.00, DGRN, GRN, 'File Contents'),
        (1.40, 1.25, DAMB, AMB, 'Tool Outputs'),
        (1.40, 0.50, DRED, RED, 'Images'),
    ]
    iw, ih = 2.55, 0.62
    for ix, iy, fc, tc, ilbl in inputs:
        box(ax, ix, iy, iw, ih, fc, ilbl, fs=17, tc=tc, lw=2.0)

    # Context Window
    cwx, cwy = 6.30, 2.00
    box(ax, cwx, cwy, 2.75, 3.60, DGRN, 'Context\nWindow\n~200K tokens',
        fs=19, tc=GRN, lw=2.8)

    # Model
    box(ax, 10.05, cwy, 1.75, 0.90, DBLU, 'Model\nreasoning', fs=17, tc=BLU, lw=2.0)

    for ix, iy, *_ in inputs:
        arr(ax, ix + iw/2, iy, cwx - 1.40, cwy + (iy - cwy) * 0.50,
            col=MUT, lw=1.8, ms=14)

    arr(ax, cwx + 1.38, cwy, 10.05 - 0.88, cwy, col=GRN, lw=2.2)

    save(fig, 'diag-04-context-window.png')


# ═══════════════════════════════════════════════════════════════
# 5 — CLAUDE.md Loading
# ═══════════════════════════════════════════════════════════════
def make_05():
    fig, ax = new_fig(9, 6.0)
    title(ax, 9, 6.0, 'How CLAUDE.md Is Loaded')

    box(ax, 4.5, 5.40, 3.0, 0.75, DPUR, 'claude invoked', fs=19, tc=PUR, lw=2.5)

    box(ax, 2.0, 4.00, 3.4, 0.80, DBLU, '~/.claude/CLAUDE.md\n(global)', fs=17, tc=BLU)
    box(ax, 7.0, 4.00, 3.4, 0.80, DGRN, './CLAUDE.md\n(project root)', fs=17, tc=GRN)

    box(ax, 5.4, 2.50, 3.0, 0.80, DAMB, 'Subdirectory\nCLAUDE.md', fs=17, tc=AMB)
    box(ax, 8.3, 2.50, 2.85, 0.80, DBLU, '@import\nsnippets', fs=17, tc=BLU)

    box(ax, 4.5, 1.00, 6.2, 0.80, DGRN, 'Merged System Prompt  (injected every turn)',
        fs=17, tc=GRN, lw=2.8)

    arr(ax, 3.35, 5.40, 2.0, 4.40, col=MUT)
    arr(ax, 5.65, 5.40, 7.0, 4.40, col=MUT)

    arr(ax, 6.15, 3.60, 5.4, 2.90, col=MUT, lw=1.8)
    arr(ax, 7.85, 3.60, 8.3, 2.90, col=MUT, lw=1.8)

    for sx, sy in [(2.0, 3.60), (7.0, 3.60), (5.4, 2.10), (8.3, 2.10)]:
        arr(ax, sx, sy, 4.5 + (sx - 4.5) * 0.12, 1.40, col=MUT, lw=1.8, ms=14)

    save(fig, 'diag-05-claude-md-loading.png')


# ═══════════════════════════════════════════════════════════════
# 6 — Subagent Orchestration
# ═══════════════════════════════════════════════════════════════
def make_06():
    fig, ax = new_fig(11, 5.5)
    title(ax, 11, 5.5, 'Subagent Orchestration')

    xs = [1.55, 3.95, 6.55, 9.15]
    task_labels  = ['Write\nunit tests', 'Update\ndocs', 'Refactor\nauth', 'Audit\ndeps']
    agent_labels = ['Subagent 1\nisolated ctx', 'Subagent 2\nisolated ctx',
                    'Subagent 3\nisolated ctx', 'Subagent 4\nisolated ctx']
    cx = 5.35

    box(ax, cx, 4.90, 4.8, 0.82, DPUR, 'Orchestrator  (main Claude session)',
        fs=18, tc=PUR, lw=2.8)

    bw, bh = 2.05, 0.90
    for x, lbl_text in zip(xs, task_labels):
        box(ax, x, 3.45, bw, bh, DBLU, lbl_text, fs=16, tc=BLU)
        arr(ax, cx + (x - cx) * 0.42, 4.49, x, 3.90, col=MUT, lw=1.8, ms=14)

    for x, lbl_text in zip(xs, agent_labels):
        box(ax, x, 2.00, bw, bh, DGRN, lbl_text, fs=15, tc=GRN)
        arr(ax, x, 3.00, x, 2.45, col=MUT, lw=1.8, ms=14)

    box(ax, cx, 0.65, 5.5, 0.82, DGRN, 'Merge Results  —  back to Orchestrator',
        fs=17, tc=GRN, lw=2.5)
    for x in xs:
        arr(ax, x, 1.55, cx + (x - cx) * 0.22, 1.07, col=MUT, lw=1.8, ms=14)

    save(fig, 'diag-06-subagent-orchestration.png')


# ═══════════════════════════════════════════════════════════════
# 7 — Planning Mode Workflow
# ═══════════════════════════════════════════════════════════════
def make_07():
    fig, ax = new_fig(11, 3.8)
    title(ax, 11, 3.8, 'Planning Mode Workflow')

    nodes = [
        (0.80,  2.05, DPUR, PUR, 'Request'),
        (2.40,  2.05, DGRN, GRN, '/plan\nread-only'),
        (4.00,  2.05, DBLU, BLU, 'Explore\ncodebase'),
        (5.60,  2.05, DAMB, AMB, 'Draft\nplan'),
        (7.20,  2.05, CARD, TXT, 'Human\nReview'),
        (8.80,  2.05, DGRN, GRN, 'Execute\nchanges'),
        (10.40, 2.05, DGRN, GRN, 'Done!'),
    ]
    bw, bh = 1.38, 0.95
    for x, y, fc, tc, lbl_text in nodes:
        box(ax, x, y, bw, bh, fc, lbl_text, fs=16, tc=tc)

    for i in range(len(nodes) - 1):
        col = GRN if i >= 4 else TXT
        arr(ax, nodes[i][0] + bw/2, 2.05, nodes[i+1][0] - bw/2, 2.05, col=col)

    # Refine loop below
    ry, ry2 = 1.15, 1.57
    ax.plot([5.60, 5.60], [ry, ry2], color=AMB, lw=2.0, zorder=2)
    ax.plot([7.20, 7.20], [ry, ry2], color=AMB, lw=2.0, zorder=2)
    ax.plot([5.60, 7.20], [ry, ry], color=AMB, lw=2.0, zorder=2)
    ax.annotate('', xy=(5.60, ry2), xytext=(5.60, ry + 0.01),
                arrowprops=dict(arrowstyle='->', color=AMB, lw=2.0, mutation_scale=14),
                zorder=2)
    lbl(ax, 6.40, 0.82, 'refine', col=AMB, fs=13)

    save(fig, 'diag-07-planning-mode.png')


# ═══════════════════════════════════════════════════════════════
# 8 — CLI vs MCP Token Cost
# ═══════════════════════════════════════════════════════════════
def make_08():
    fig, ax = new_fig(11, 4.8)
    title(ax, 11, 4.8, 'CLI vs MCP — Token Cost')

    box(ax, 1.10, 2.45, 1.65, 0.90, DPUR, 'Same\nTask', fs=18, tc=PUR)

    # CLI path
    cli_y = 3.65
    group_bg(ax, 6.20, cli_y, 8.40, 1.20, GRN, GRN, alpha=0.09, lw=1.5,
             label='CLI path', lfs=15)
    box(ax, 3.60, cli_y, 2.50, 0.80, DGRN, 'gh pr list\n--json ...', fs=17, tc=GRN)
    box(ax, 6.50, cli_y, 2.50, 0.80, DGRN, '~100 tokens\nclean JSON', fs=17, tc=GRN)
    arr(ax, 1.93, 2.90, 2.35, cli_y, col=GRN)
    arr(ax, 4.85, cli_y, 5.25, cli_y, col=GRN)

    # MCP path
    mcp_y = 1.25
    group_bg(ax, 6.20, mcp_y, 8.40, 1.20, RED, RED, alpha=0.09, lw=1.5,
             label='MCP path', lfs=15)
    box(ax, 3.60, mcp_y, 2.50, 0.80, DRED, 'MCP server\ncall', fs=17, tc=RED)
    box(ax, 6.50, mcp_y, 2.50, 0.80, DRED, 'Protocol +\nschema wrap', fs=17, tc=RED)
    box(ax, 9.40, mcp_y, 2.50, 0.80, DRED, '2,000+\ntokens', fs=17, tc=RED)
    arr(ax, 1.93, 2.00, 2.35, mcp_y, col=RED)
    arr(ax, 4.85, mcp_y, 5.25, mcp_y, col=RED)
    arr(ax, 7.75, mcp_y, 8.15, mcp_y, col=RED)

    # Same result
    box(ax, 10.45, 2.45, 1.65, 0.90, CARD, 'Same\nresult', fs=17, tc=TXT, ec=MUT)
    arr(ax, 7.75, cli_y, 9.62, 2.90, col=GRN)
    arr(ax, 10.65, mcp_y, 10.10, 2.00, col=RED)

    lbl(ax, 6.50, cli_y + 0.68, 'cheap  (low cost)',      col=GRN, fs=13)
    lbl(ax, 6.50, mcp_y - 0.55, 'expensive  (high cost)', col=RED, fs=13)

    save(fig, 'diag-08-cli-vs-mcp.png')


# ═══════════════════════════════════════════════════════════════
# 9 — Daily Workflow / Mental Model
# ═══════════════════════════════════════════════════════════════
def make_09():
    fig, ax = new_fig(9, 8.5)
    title(ax, 9, 8.5, 'Effective Usage — Mental Model')

    bw, bh   = 2.80, 0.80
    dw, dh   = 3.20, 0.95   # diamond dims

    # New Task
    box(ax, 4.5, 7.75, bw, bh, DPUR, 'New Task', fs=19, tc=PUR, lw=2.5)

    # CLAUDE.md current?
    diamond(ax, 4.5, 6.60, dw, dh, DBLU, 'CLAUDE.md\ncurrent?', fs=16, tc=BLU)
    arr(ax, 4.5, 7.35, 4.5, 7.08, col=MUT)

    # No → Update
    box(ax, 7.75, 6.60, 2.50, 0.80, DAMB, 'Update / /init', fs=17, tc=AMB)
    arr(ax, 6.10, 6.60, 6.50, 6.60, col=AMB)
    lbl(ax, 6.28, 6.90, 'no', col=AMB, fs=13)
    ax.plot([7.75, 8.85, 8.85, 4.5], [6.20, 6.20, 5.55, 5.55],
            color=AMB, lw=1.8, zorder=2, linestyle='--')

    # Yes → Task size?
    arr(ax, 4.5, 6.12, 4.5, 5.80, col=MUT)
    lbl(ax, 4.10, 5.96, 'yes', col=GRN, fs=13)

    # Task size?
    diamond(ax, 4.5, 5.30, dw, dh, DBLU, 'Task\ncomplexity?', fs=16, tc=BLU)

    # Simple → Direct
    box(ax, 1.30, 5.30, 2.35, 0.80, DGRN, 'Direct\nprompt', fs=17, tc=GRN)
    arr(ax, 3.10, 5.30, 2.47, 5.30, col=GRN)
    lbl(ax, 2.82, 5.62, 'simple', col=GRN, fs=12)

    # Medium → /plan
    box(ax, 4.50, 4.10, 2.35, 0.80, DGRN, '/plan first', fs=17, tc=GRN)
    arr(ax, 4.50, 4.82, 4.50, 4.90, col=GRN)
    lbl(ax, 4.05, 4.50, 'medium', col=GRN, fs=12)

    # Large → Subagents
    box(ax, 7.70, 5.30, 2.35, 0.80, DGRN, 'Subagents', fs=17, tc=GRN)
    arr(ax, 5.90, 5.30, 6.52, 5.30, col=GRN)
    lbl(ax, 6.22, 5.62, 'large', col=GRN, fs=12)

    # All three → Context full?
    ctx_y = 2.80
    for sx, sy in [(1.30, 4.90), (4.50, 3.70), (7.70, 4.90)]:
        tx = 4.5 + (sx - 4.5) * 0.05
        arr(ax, sx, sy, tx, ctx_y + 0.50, col=MUT, lw=1.8, ms=14)

    # Context full?
    diamond(ax, 4.5, ctx_y, dw, dh, DBLU, 'Context\nfull?', fs=16, tc=BLU)

    # Yes → /compact
    box(ax, 7.70, ctx_y, 2.35, 0.80, DAMB, '/compact', fs=18, tc=AMB)
    arr(ax, 6.10, ctx_y, 6.52, ctx_y, col=AMB)
    lbl(ax, 6.28, ctx_y + 0.32, 'yes', col=AMB, fs=13)
    ax.plot([7.70, 8.85, 8.85, 4.5], [ctx_y - 0.40, ctx_y - 0.40, 1.30, 1.30],
            color=AMB, lw=1.8, linestyle='--', zorder=2)

    # No → Done
    arr(ax, 4.5, ctx_y - 0.48, 4.5, 1.20, col=GRN)
    lbl(ax, 4.08, ctx_y - 0.65, 'no', col=GRN, fs=13)
    box(ax, 4.5, 0.80, 2.80, 0.80, DGRN, 'Done!', fs=20, tc=GRN, lw=2.8)

    save(fig, 'diag-09-mental-model.png')


# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('Generating diagrams...')
    make_01(); make_02(); make_03()
    make_04(); make_05(); make_06()
    make_07(); make_08(); make_09()
    print('All done.')
