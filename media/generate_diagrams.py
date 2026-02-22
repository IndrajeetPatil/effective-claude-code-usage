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


def box(ax, x, y, w, h, fc, label, fs=23, tc='auto', lw=2.2, ec=None):
    """Rounded rectangle with centred label."""
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


def diamond(ax, x, y, w, h, fc, label, fs=22, tc='auto', lw=2.2):
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


def lbl(ax, x, y, text, col=MUT, fs=18):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fs, color=col, style='italic', zorder=5)


def group_bg(ax, x, y, w, h, fc, ec, alpha=0.12, lw=1.5, label='', lfs=21):
    """Semi-transparent group background. Label sits inside at the top edge."""
    r = FancyBboxPatch((x - w/2, y - h/2), w, h,
                        boxstyle='round,pad=0.1',
                        facecolor=fc, edgecolor=ec,
                        linewidth=lw, alpha=alpha, zorder=1)
    ax.add_patch(r)
    if label:
        ax.text(x, y + h/2 - 0.18, label, ha='center', va='top',
                fontsize=lfs, color=ec, fontweight='bold', alpha=0.9, zorder=2)


def title(ax, w, h, text, col=GRN, fs=32, y_off=0.55):
    """Title at the top of the figure — y_off reserves clear space above content."""
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
    fig, ax = new_fig(11, 6.0)
    title(ax, 11, 6.0, 'Intelligence Spectrum')

    # Capability arrow — in the band between title and column headers
    ax.annotate('', xy=(10.6, 4.78), xytext=(0.4, 4.78),
                arrowprops=dict(arrowstyle='->', color=MUT, lw=2.0,
                                mutation_scale=18, connectionstyle='arc3,rad=0.0'),
                zorder=2)
    ax.text(5.5, 4.56, 'increasing capability  &  autonomy',
            ha='center', va='center', fontsize=18, color=MUT,
            style='italic', zorder=5)

    # Column headers as standalone text — positioned ABOVE the group rects,
    # well clear of both the capability arrow and the group boxes
    col_headers = [
        (1.85, MUT,  'Tab Completion'),
        (5.50, BLU,  'Chatbot (LLM)'),
        (9.15, GRN,  'Agent (Claude Code)'),
    ]
    for hx, hc, ht in col_headers:
        ax.text(hx, 4.18, ht, ha='center', va='center',
                fontsize=20, color=hc, fontweight='bold', zorder=5)

    # Group backgrounds WITHOUT embedded labels (labels are drawn above)
    group_bg(ax, 1.85, 2.20, 3.2, 3.0, '#8b949e', '#8b949e', alpha=0.14)
    group_bg(ax, 5.50, 2.20, 3.2, 3.0, DBLU,      BLU,       alpha=0.14)
    group_bg(ax, 9.15, 2.20, 3.2, 3.0, DGRN,      GRN,       alpha=0.14)

    # Tab Completion boxes
    box(ax, 1.85, 2.85, 2.65, 0.85, '#21262d', 'Predict next token',   fs=21, tc=MUT, ec='#30363d')
    box(ax, 1.85, 1.70, 2.65, 0.85, '#21262d', 'No context\nor world state', fs=21, tc=MUT, ec='#30363d')

    # Chatbot boxes
    box(ax, 5.50, 2.85, 2.65, 0.85, DBLU, 'Understand prompt', fs=21, tc=BLU)
    box(ax, 5.50, 1.70, 2.65, 0.85, DBLU, 'One-shot response', fs=21, tc=BLU)

    # Agent boxes (3) — enough internal room since groups have no embedded label
    box(ax, 9.15, 3.08, 2.65, 0.78, DGRN, 'Perceive context', fs=20, tc=GRN)
    box(ax, 9.15, 2.20, 2.65, 0.78, DGRN, 'Plan & use tools', fs=20, tc=GRN)
    box(ax, 9.15, 1.32, 2.65, 0.78, DGRN, 'Loop until done',  fs=20, tc=GRN)

    save(fig, 'diag-01-intelligence-spectrum.png')


# ═══════════════════════════════════════════════════════════════
# 2 — ReAct Agent Loop
# ═══════════════════════════════════════════════════════════════
def make_02():
    fig, ax = new_fig(11, 5.2)
    title(ax, 11, 5.2, 'The ReAct Agent Loop')

    nodes = [
        (0.95, 2.80, DPUR, PUR, 'New\nTask'),
        (2.65, 2.80, DBLU, BLU, 'Perceive\ncontext'),
        (4.35, 2.80, DGRN, GRN, 'Think\nreason'),
        (6.05, 2.80, DAMB, AMB, 'Act\nuse tool'),
        (7.75, 2.80, DBLU, BLU, 'Observe\noutput'),
    ]
    bw, bh = 1.45, 1.05
    for x, y, fc, tc, lbl_text in nodes:
        box(ax, x, y, bw, bh, fc, lbl_text, fs=22, tc=tc)

    for i in range(len(nodes) - 1):
        arr(ax, nodes[i][0] + bw/2, 2.80, nodes[i+1][0] - bw/2, 2.80, col=TXT)

    # Loop-back
    loop_y = 1.50
    ax.plot([4.35, 4.35], [loop_y, 2.27], color=MUT, lw=2.0, zorder=2)
    ax.plot([7.75, 7.75], [loop_y, 2.27], color=MUT, lw=2.0, zorder=2)
    ax.plot([4.35, 7.75], [loop_y, loop_y], color=MUT, lw=2.0, zorder=2)
    ax.annotate('', xy=(4.35, 2.27), xytext=(4.35, loop_y + 0.01),
                arrowprops=dict(arrowstyle='->', color=MUT, lw=2.0, mutation_scale=15),
                zorder=2)
    lbl(ax, 6.05, 1.18, 'not done — loop back', col=MUT, fs=18)

    # Done exit
    arr(ax, 8.48, 2.80, 8.85, 2.80, col=GRN, lw=2.2)
    lbl(ax, 8.65, 3.22, 'done', col=GRN, fs=17)
    box(ax, 10.05, 2.80, 1.85, 0.95, DGRN, 'Return\nresult', fs=22, tc=GRN)

    save(fig, 'diag-02-react-loop.png')


# ═══════════════════════════════════════════════════════════════
# 3 — Tool Ecosystem
# ═══════════════════════════════════════════════════════════════
def make_03():
    fig, ax = new_fig(11, 6.8)
    title(ax, 11, 6.8, 'Tool Ecosystem')

    cx, cy = 5.5, 2.80
    box(ax, cx, cy, 2.1, 1.15, DGRN, 'Claude\nCode', fs=26, tc=GRN, lw=2.8)

    tools = [
        (1.55, 4.10, DBLU, BLU, 'File I/O',  'Read · Write\nEdit · Glob'),
        (1.55, 1.50, DAMB, AMB, 'Shell',      'Bash · any\nterminal cmd'),
        (5.50, 4.75, DPUR, PUR, 'Search',     'Grep · WebSearch\nWebFetch'),
        (9.45, 4.10, DRED, RED, 'MCP',        'GitHub · Jira\nCustom servers'),
        (9.45, 1.50, DGRN, GRN, 'Agents',     'Task · spawn\nsubagents'),
    ]
    for tx, ty, fc, tc, t_title, t_sub in tools:
        box(ax, tx, ty + 0.22, 2.65, 0.75, fc, t_title, fs=22, tc=tc, lw=2.0)
        ax.text(tx, ty - 0.42, t_sub, ha='center', va='center',
                fontsize=18, color=MUT, linespacing=1.2, zorder=4)
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
    fig, ax = new_fig(11, 5.8)
    title(ax, 11, 5.8, 'What Fills the Context Window?')

    inputs = [
        (1.40, 3.90, DPUR, PUR, 'CLAUDE.md'),
        (1.40, 3.10, DBLU, BLU, 'Conversation History'),
        (1.40, 2.30, DGRN, GRN, 'File Contents'),
        (1.40, 1.50, DAMB, AMB, 'Tool Outputs'),
        (1.40, 0.70, DRED, RED, 'Images'),
    ]
    iw, ih = 2.65, 0.68
    for ix, iy, fc, tc, ilbl in inputs:
        box(ax, ix, iy, iw, ih, fc, ilbl, fs=21, tc=tc, lw=2.0)

    # Context Window
    cwx, cwy = 6.30, 2.30
    box(ax, cwx, cwy, 2.80, 4.00, DGRN, 'Context\nWindow\n~200K tokens',
        fs=23, tc=GRN, lw=2.8)

    # Model
    box(ax, 10.05, cwy, 1.80, 0.95, DBLU, 'Model\nreasoning', fs=21, tc=BLU, lw=2.0)

    for ix, iy, *_ in inputs:
        arr(ax, ix + iw/2, iy, cwx - 1.42, cwy + (iy - cwy) * 0.50,
            col=MUT, lw=1.8, ms=14)

    arr(ax, cwx + 1.42, cwy, 10.05 - 0.90, cwy, col=GRN, lw=2.2)

    save(fig, 'diag-04-context-window.png')


# ═══════════════════════════════════════════════════════════════
# 5 — CLAUDE.md Loading
# ═══════════════════════════════════════════════════════════════
def make_05():
    # Increased height so title (at h-0.55) clears the top box
    fig, ax = new_fig(9, 7.5)
    title(ax, 9, 7.5, 'How CLAUDE.md Is Loaded')

    box(ax, 4.5, 5.75, 3.0, 0.80, DPUR, 'claude invoked', fs=23, tc=PUR, lw=2.5)

    box(ax, 2.0, 4.25, 3.5, 0.88, DBLU, '~/.claude/CLAUDE.md\n(global)', fs=21, tc=BLU)
    box(ax, 7.0, 4.25, 3.5, 0.88, DGRN, './CLAUDE.md\n(project root)', fs=21, tc=GRN)

    box(ax, 5.4, 2.65, 3.0, 0.88, DAMB, 'Subdirectory\nCLAUDE.md', fs=21, tc=AMB)
    box(ax, 8.3, 2.65, 2.85, 0.88, DBLU, '@import\nsnippets', fs=21, tc=BLU)

    box(ax, 4.5, 1.05, 6.4, 0.88, DGRN, 'Merged System Prompt  (injected every turn)',
        fs=21, tc=GRN, lw=2.8)

    arr(ax, 3.35, 5.75, 2.0, 4.69, col=MUT)
    arr(ax, 5.65, 5.75, 7.0, 4.69, col=MUT)

    arr(ax, 6.15, 3.81, 5.4, 3.09, col=MUT, lw=1.8)
    arr(ax, 7.85, 3.81, 8.3, 3.09, col=MUT, lw=1.8)

    for sx, sy in [(2.0, 3.81), (7.0, 3.81), (5.4, 2.21), (8.3, 2.21)]:
        arr(ax, sx, sy, 4.5 + (sx - 4.5) * 0.12, 1.49, col=MUT, lw=1.8, ms=14)

    save(fig, 'diag-05-claude-md-loading.png')


# ═══════════════════════════════════════════════════════════════
# 6 — Subagent Orchestration
# ═══════════════════════════════════════════════════════════════
def make_06():
    # Increased height so title clears the Orchestrator box
    fig, ax = new_fig(11, 6.8)
    title(ax, 11, 6.8, 'Subagent Orchestration')

    xs = [1.55, 3.95, 6.55, 9.15]
    task_labels  = ['Write\nunit tests', 'Update\ndocs', 'Refactor\nauth', 'Audit\ndeps']
    agent_labels = ['Subagent 1\nisolated ctx', 'Subagent 2\nisolated ctx',
                    'Subagent 3\nisolated ctx', 'Subagent 4\nisolated ctx']
    cx = 5.35

    box(ax, cx, 5.10, 4.8, 0.88, DPUR, 'Orchestrator  (main Claude session)',
        fs=22, tc=PUR, lw=2.8)

    bw, bh = 2.05, 0.95
    for x, lbl_text in zip(xs, task_labels):
        box(ax, x, 3.60, bw, bh, DBLU, lbl_text, fs=20, tc=BLU)
        arr(ax, cx + (x - cx) * 0.42, 4.66, x, 4.08, col=MUT, lw=1.8, ms=14)

    for x, lbl_text in zip(xs, agent_labels):
        box(ax, x, 2.10, bw, bh, DGRN, lbl_text, fs=19, tc=GRN)
        arr(ax, x, 3.12, x, 2.58, col=MUT, lw=1.8, ms=14)

    box(ax, cx, 0.70, 5.5, 0.88, DGRN, 'Merge Results  —  back to Orchestrator',
        fs=21, tc=GRN, lw=2.5)
    for x in xs:
        arr(ax, x, 1.62, cx + (x - cx) * 0.22, 1.14, col=MUT, lw=1.8, ms=14)

    save(fig, 'diag-06-subagent-orchestration.png')


# ═══════════════════════════════════════════════════════════════
# 7 — Planning Mode Workflow
# ═══════════════════════════════════════════════════════════════
def make_07():
    fig, ax = new_fig(11, 4.5)
    title(ax, 11, 4.5, 'Planning Mode Workflow')

    nodes = [
        (0.70,  2.20, DPUR, PUR, 'Request'),
        (2.10,  2.20, DGRN, GRN, '/plan\nread-only'),
        (3.50,  2.20, DBLU, BLU, 'Research\ncodebase'),
        (4.90,  2.20, DAMB, AMB, 'Draft\nplan'),
        (6.30,  2.20, CARD, TXT, 'Annotate\n+ Revise'),
        (7.70,  2.20, DGRN, GRN, 'Execute\nchanges'),
        (9.10,  2.20, DGRN, GRN, 'Done!'),
    ]
    bw, bh = 1.22, 1.02
    for x, y, fc, tc, lbl_text in nodes:
        box(ax, x, y, bw, bh, fc, lbl_text, fs=19, tc=tc)

    for i in range(len(nodes) - 1):
        col = GRN if i >= 5 else TXT
        arr(ax, nodes[i][0] + bw/2, 2.20, nodes[i+1][0] - bw/2, 2.20, col=col)

    # Annotation loop below nodes (Draft → Annotate+Revise)
    ry, ry2 = 1.22, 1.69
    ax.plot([4.90, 4.90], [ry, ry2], color=AMB, lw=2.0, zorder=2)
    ax.plot([6.30, 6.30], [ry, ry2], color=AMB, lw=2.0, zorder=2)
    ax.plot([4.90, 6.30], [ry, ry], color=AMB, lw=2.0, zorder=2)
    ax.annotate('', xy=(4.90, ry2), xytext=(4.90, ry + 0.01),
                arrowprops=dict(arrowstyle='->', color=AMB, lw=2.0, mutation_scale=14),
                zorder=2)
    lbl(ax, 5.60, 0.90, '1-6x', col=AMB, fs=17)

    # Annotation below Done node
    ax.text(9.10, 1.50, 'plan.md = living checklist', ha='center', va='center',
            fontsize=15, color=MUT, style='italic', zorder=5)

    save(fig, 'diag-07-planning-mode.png')


# ═══════════════════════════════════════════════════════════════
# 8 — CLI vs MCP Token Cost
# ═══════════════════════════════════════════════════════════════
def make_08():
    fig, ax = new_fig(11, 5.5)
    title(ax, 11, 5.5, 'CLI vs MCP — Token Cost')

    box(ax, 1.10, 2.80, 1.65, 0.95, DPUR, 'Same\nTask', fs=22, tc=PUR)

    # ── CLI path ──────────────────────────────────────────────
    # Standalone section label — sits in a gap row, clear of title and boxes
    ax.text(6.50, 4.25, 'CLI path', ha='center', va='center',
            fontsize=20, color=GRN, fontweight='bold', zorder=5)
    ax.plot([2.0, 10.8], [4.05, 4.05], color=GRN, lw=1.2, alpha=0.30, zorder=1)

    cli_y = 3.50
    box(ax, 3.60, cli_y, 2.50, 0.85, DGRN, 'gh pr list\n--json ...', fs=21, tc=GRN)
    box(ax, 6.50, cli_y, 2.50, 0.85, DGRN, '~100 tokens\nclean JSON', fs=21, tc=GRN)
    arr(ax, 1.93, 2.80, 2.35, cli_y, col=GRN)
    arr(ax, 4.85, cli_y, 5.25, cli_y, col=GRN)

    # ── MCP path ──────────────────────────────────────────────
    ax.text(6.50, 2.40, 'MCP path', ha='center', va='center',
            fontsize=20, color=RED, fontweight='bold', zorder=5)
    ax.plot([2.0, 10.8], [2.20, 2.20], color=RED, lw=1.2, alpha=0.30, zorder=1)

    mcp_y = 1.45
    box(ax, 3.60, mcp_y, 2.50, 0.85, DRED, 'MCP server\ncall', fs=21, tc=RED)
    box(ax, 6.50, mcp_y, 2.50, 0.85, DRED, 'Protocol +\nschema wrap', fs=21, tc=RED)
    box(ax, 9.40, mcp_y, 2.50, 0.85, DRED, '2,000+\ntokens', fs=21, tc=RED)
    arr(ax, 1.93, 2.80, 2.35, mcp_y, col=RED)
    arr(ax, 4.85, mcp_y, 5.25, mcp_y, col=RED)
    arr(ax, 7.75, mcp_y, 8.15, mcp_y, col=RED)

    # ── Same result ───────────────────────────────────────────
    box(ax, 10.45, 2.80, 1.65, 0.95, CARD, 'Same\nresult', fs=21, tc=TXT, ec=MUT)
    arr(ax, 7.75, cli_y, 9.62, 2.80, col=GRN)
    arr(ax, 10.65, mcp_y, 10.10, 2.80, col=RED)

    save(fig, 'diag-08-cli-vs-mcp.png')


# ═══════════════════════════════════════════════════════════════
# 9 — Daily Workflow / Mental Model
# ═══════════════════════════════════════════════════════════════
def make_09():
    # Increased height so title clears the "New Task" box at top
    fig, ax = new_fig(9, 10.2)
    title(ax, 9, 10.2, 'Effective Usage — Mental Model')

    bw, bh   = 2.80, 0.85
    dw, dh   = 3.20, 1.00

    # New Task — now well below the title
    box(ax, 4.5, 8.20, bw, bh, DPUR, 'New Task', fs=23, tc=PUR, lw=2.5)

    # CLAUDE.md current?
    diamond(ax, 4.5, 6.98, dw, dh, DBLU, 'CLAUDE.md\ncurrent?', fs=20, tc=BLU)
    arr(ax, 4.5, 7.77, 4.5, 7.48, col=MUT)

    # No → Update
    box(ax, 7.75, 6.98, 2.50, 0.85, DAMB, 'Update / /init', fs=21, tc=AMB)
    arr(ax, 6.10, 6.98, 6.50, 6.98, col=AMB)
    lbl(ax, 6.28, 7.30, 'no', col=AMB, fs=17)
    ax.plot([7.75, 8.85, 8.85, 4.5], [6.55, 6.55, 5.88, 5.88],
            color=AMB, lw=1.8, zorder=2, linestyle='--')

    # Yes → Task size?
    arr(ax, 4.5, 6.48, 4.5, 6.10, col=MUT)
    lbl(ax, 4.10, 6.30, 'yes', col=GRN, fs=17)

    # Task size?
    diamond(ax, 4.5, 5.60, dw, dh, DBLU, 'Task\ncomplexity?', fs=20, tc=BLU)

    # Simple → Direct
    box(ax, 1.30, 5.60, 2.35, 0.85, DGRN, 'Direct\nprompt', fs=21, tc=GRN)
    arr(ax, 3.10, 5.60, 2.47, 5.60, col=GRN)
    lbl(ax, 2.82, 5.95, 'simple', col=GRN, fs=16)

    # Medium → /plan
    box(ax, 4.50, 4.35, 2.35, 0.85, DGRN, '/plan first', fs=21, tc=GRN)
    arr(ax, 4.50, 5.10, 4.50, 5.20, col=GRN)
    lbl(ax, 4.05, 4.78, 'medium', col=GRN, fs=16)

    # Large → Subagents
    box(ax, 7.70, 5.60, 2.35, 0.85, DGRN, 'Subagents', fs=21, tc=GRN)
    arr(ax, 5.90, 5.60, 6.52, 5.60, col=GRN)
    lbl(ax, 6.22, 5.95, 'large', col=GRN, fs=16)

    # All three → Context full?
    ctx_y = 3.00
    for sx, sy in [(1.30, 5.17), (4.50, 3.92), (7.70, 5.17)]:
        tx = 4.5 + (sx - 4.5) * 0.05
        arr(ax, sx, sy, tx, ctx_y + 0.52, col=MUT, lw=1.8, ms=14)

    # Context full?
    diamond(ax, 4.5, ctx_y, dw, dh, DBLU, 'Context\nfull?', fs=20, tc=BLU)

    # Yes → /compact
    box(ax, 7.70, ctx_y, 2.35, 0.85, DAMB, '/compact', fs=22, tc=AMB)
    arr(ax, 6.10, ctx_y, 6.52, ctx_y, col=AMB)
    lbl(ax, 6.28, ctx_y + 0.35, 'yes', col=AMB, fs=17)
    ax.plot([7.70, 8.85, 8.85, 4.5], [ctx_y - 0.42, ctx_y - 0.42, 1.42, 1.42],
            color=AMB, lw=1.8, linestyle='--', zorder=2)

    # No → Done
    arr(ax, 4.5, ctx_y - 0.50, 4.5, 1.30, col=GRN)
    lbl(ax, 4.08, ctx_y - 0.68, 'no', col=GRN, fs=17)
    box(ax, 4.5, 0.88, 2.80, 0.85, DGRN, 'Done!', fs=24, tc=GRN, lw=2.8)

    save(fig, 'diag-09-mental-model.png')


# ═══════════════════════════════════════════════════════════════
# 10 — Quality Guardrails
# Three-layer layout: each layer uses a plain colored text header
# (no group_bg so no occlusion issues), then a row of item boxes.
# ═══════════════════════════════════════════════════════════════
def make_10():
    fig, ax = new_fig(11, 9.5)
    title(ax, 11, 9.5, 'Quality Guardrails — Three Layers')

    xs = [1.20, 3.30, 5.50, 7.70, 9.80]   # x centres for 5-item rows
    bw_item = 1.90                          # item box width

    # ── Agent ────────────────────────────────────────────────
    box(ax, 5.5, 7.20, 3.4, 0.88, DPUR, 'Agent writes code', fs=23, tc=PUR, lw=2.5)
    arr(ax, 5.5, 6.76, 5.5, 6.52, col=BLU, lw=2.2)

    # Layer 1 header — standalone text + thin rule, never overlaps boxes
    ax.text(5.5, 6.30, 'Layer 1 — Agent Instructions  (CLAUDE.md)',
            ha='center', va='center', fontsize=21, color=BLU,
            fontweight='bold', zorder=5)
    ax.plot([0.5, 10.5], [6.10, 6.10], color=BLU, lw=1.5, alpha=0.35, zorder=2)

    # Layer 1 boxes
    l1 = ['Coding\nconventions', '"Never do"\nrules', 'Run tests\nbefore done',
          'Lint / format\non every edit', 'Definition\nof done']
    for lx, ltxt in zip(xs, l1):
        box(ax, lx, 5.42, bw_item, 0.82, DBLU, ltxt, fs=19, tc=BLU, lw=1.8)

    arr(ax, 5.5, 5.01, 5.5, 4.77, col=AMB, lw=2.2)

    # Layer 2 header
    ax.text(5.5, 4.55, 'Layer 2 — Local QA Tools',
            ha='center', va='center', fontsize=21, color=AMB,
            fontweight='bold', zorder=5)
    ax.plot([0.5, 10.5], [4.35, 4.35], color=AMB, lw=1.5, alpha=0.35, zorder=2)

    # Layer 2 boxes
    l2 = ['Linter\n(ESLint/ruff)', 'Type checker\n(tsc/mypy)', 'Formatter\n(Prettier/black)',
          'Unit tests\n(jest/pytest)', 'Pre-commit\nhooks']
    for lx, ltxt in zip(xs, l2):
        box(ax, lx, 3.67, bw_item, 0.82, DAMB, ltxt, fs=18, tc=AMB, lw=1.8)

    arr(ax, 5.5, 3.26, 5.5, 3.02, col=GRN, lw=2.2)

    # Layer 3 header
    ax.text(5.5, 2.80, 'Layer 3 — CI / CD Safety Net',
            ha='center', va='center', fontsize=21, color=GRN,
            fontweight='bold', zorder=5)
    ax.plot([0.5, 10.5], [2.60, 2.60], color=GRN, lw=1.5, alpha=0.35, zorder=2)

    # Layer 3 boxes
    l3 = ['Branch\nprotection', 'PR checks\n(lint + test)', 'Coverage\nthreshold',
          'Security\nscan', 'Required\nreviewer']
    for lx, ltxt in zip(xs, l3):
        box(ax, lx, 1.92, bw_item, 0.82, DGRN, ltxt, fs=18, tc=GRN, lw=1.8)

    arr(ax, 5.5, 1.51, 5.5, 1.27, col=GRN, lw=2.2)

    # Ship
    box(ax, 5.5, 0.78, 3.4, 0.80, DGRN, 'Merge  +  Ship', fs=23, tc=GRN, lw=2.8)

    save(fig, 'diag-10-qa-scaffold.png')


# ═══════════════════════════════════════════════════════════════
# 11 — Git Worktrees: Parallel Isolation
# Layout: w=11, h=9.0
#   title at y=8.45 (h-0.55)
#   safe zone: top edge ≤ 9.0-1.05 = 7.95
#   git store center y=7.5, top=7.925 ≤ 7.95 ✓
#   worktrees center y=5.8, h=1.2, top=6.4
#   sessions center y=3.5, h=0.85, top=3.925
#   annotation at y=2.2

def make_11():
    fig, ax = new_fig(11, 9.0)
    title(ax, 11, 9.0, 'Git Worktrees — Parallel Isolation')

    # ── Shared git object store ───────────────────────────────────
    # center y=7.5, h=0.85 → top=7.925 ≤ 7.95 ✓, bottom=7.075
    box(ax, 5.5, 7.50, 6.0, 0.85, CARD,
        '.git/  ·  shared objects, refs, history, remote connections',
        fs=20, tc=TXT, lw=2.0, ec=MUT)

    # ── Arrows: git store → worktrees (fan out) ──────────────────
    # worktree tops = 5.8 + 0.60 = 6.40
    arr(ax, 3.0, 7.075, 1.8, 6.40, col=MUT, lw=1.8, rad=-0.22)
    arr(ax, 5.5, 7.075, 5.5, 6.40, col=MUT, lw=1.8)
    arr(ax, 8.0, 7.075, 9.2, 6.40, col=MUT, lw=1.8, rad=0.22)

    # ── Worktree directory boxes ──────────────────────────────────
    # center y=5.8, h=1.2, top=6.4, bottom=5.2
    wt_xs     = [1.8,           5.5,                  9.2]
    wt_labels = ['main\nbranch: main',
                 'feature-auth\nbranch: feature-auth',
                 'bugfix-123\nbranch: bugfix-123']
    wt_cols   = [(DGRN, GRN), (DBLU, BLU), (DAMB, AMB)]

    for wx, wlbl, (wfc, wec) in zip(wt_xs, wt_labels, wt_cols):
        box(ax, wx, 5.80, 2.80, 1.20, wfc, wlbl, fs=20, tc=wec, lw=2.2, ec=wec)

    # ── Arrows: worktrees → sessions ─────────────────────────────
    # worktree bottom = 5.2, session top = 3.5 + 0.425 = 3.925
    for wx in wt_xs:
        arr(ax, wx, 5.20, wx, 3.925, col=MUT, lw=1.8)

    # ── Claude Code session boxes ─────────────────────────────────
    # center y=3.5, h=0.85, top=3.925, bottom=3.075
    sess_labels = ['claude -w main',
                   'claude -w\nfeature-auth',
                   'claude -w\nbugfix-123']

    for wx, slbl, (sfc, sec) in zip(wt_xs, sess_labels, wt_cols):
        box(ax, wx, 3.50, 2.80, 0.85, sfc, slbl, fs=20, tc=sec, lw=2.2, ec=sec)

    # ── Column labels — standalone text above each worktree ───────
    col_header_y = 6.85  # above worktree tops (6.40), below git bottom (7.075)
    for wx, (_, wec), lbl_txt in zip(wt_xs, wt_cols,
                                      ['Session A', 'Session B', 'Session C']):
        ax.text(wx, col_header_y, lbl_txt,
                ha='center', va='center', fontsize=18, color=wec,
                fontweight='bold', alpha=0.70, zorder=5)

    # ── Bottom annotation ─────────────────────────────────────────
    ax.text(5.5, 2.22,
            'Isolated files · own branch · no conflicts · shared history',
            ha='center', va='center', fontsize=19, color=MUT,
            style='italic', zorder=5)

    save(fig, 'diag-11-worktrees.png')


# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('Generating diagrams...')
    make_01(); make_02(); make_03()
    make_04(); make_05(); make_06()
    make_07(); make_08(); make_09()
    make_10(); make_11()
    print('All done.')
