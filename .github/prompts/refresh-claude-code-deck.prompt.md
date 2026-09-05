---
name: refresh-claude-code-deck
description: Audit this Claude Code slide deck against the latest docs and model releases, fix stale or wrong advice, tidy diagrams, and open a PR.
argument-hint: (no args needed; optionally name a section or diagram to focus on)
agent: agent
---

You are updating this repository's Quarto/RevealJS presentation about using
Claude Code effectively. The deck lives in `index.qmd`; diagrams are generated
by `media/generate_diagrams.py` and committed as `.webp`. Read `AGENTS.md` and
`AGENTS.md` first — they hold the layout rules, colour constants, and diagram
constraints you must follow.

## Goal

Check the deck's advice against the **current** state of Claude Code and the
Anthropic model lineup, then correct what is wrong. Your knowledge may be out of
date, so treat the live docs as the source of truth — not your training data and
not memory.

## Step 1 — Research the current state (parallelize)

Fetch the latest facts before touching anything. Cover at least:

- **Claude Code features** — permission modes, sandboxing, slash commands,
  skills, subagents / background agents / agent teams / workflows, hooks,
  worktrees, AGENTS.md loading, and auto memory. Primary source:
  <https://code.claude.com/docs/en/> (the `.md` variant of each page is easiest
  to grep, e.g. `https://code.claude.com/docs/en/permission-modes.md`).
- **Model lineup** — current Opus / Sonnet / Haiku / Fable versions, model IDs,
  what `/model` exposes, and any fast-mode / effort behaviour. Source:
  <https://platform.claude.com/docs/en/models/overview>.

Delegate this to subagents (e.g. the `claude-code-guide` agent or a
`general-purpose` researcher) and ask each for **doc-cited** findings.

## Step 2 — Verify before you edit (do not skip)

Research agents get things wrong. **Before changing any claim in the deck**,
confirm it yourself against the primary doc — fetch the page and grep for the
exact command, flag, or status. Two real examples from past runs:

- An agent reported `/rewind` and `/stats` as nonexistent. Both are real
  (`/stats` is an alias for `/usage`). Editing on the agent's word would have
  *introduced* an error.
- The deck deliberately never hardcodes model version names, so a flurry of new
  model releases required **zero** content changes. Don't invent work.

Only change a line when the current doc contradicts it. When in doubt, leave the
deck as-is and note the uncertainty.

## Step 3 — Classify and apply changes

Sort every discrepancy into:

- **Bad** — advice that is now misleading or wrong → fix or remove it.
- **Outdated** — correct once, stale now (e.g. a "research preview" label on a
  feature that shipped as default) → update it.
- **Missing** — see the bar below before adding anything.

Preserve the deck's conventions: source-citation div at the bottom of factual
slides, `fig-alt` on every image, the existing card/column palette, and the
principle in `AGENTS.md` that diagrams and text must not restate each other.

### The bar for NEW features

Add a new feature **only if it dramatically changes the day-to-day development
workflow** — not merely because it exists. This deck is intentionally lean. A new
slash command, config knob, or incremental option does **not** qualify. A shift
in how someone fundamentally works with Claude Code might. When unsure, leave it
out and mention it in the PR description as a suggestion for the author to weigh.

## Step 4 — Diagrams (only if they can be made clearer)

Regenerate diagrams from `media/generate_diagrams.py`; never hand-edit the
`.webp`. Fix genuine defects — crossing edges, touching boxes, orphaned/
disconnected shapes, factual errors — but don't restyle for its own sake.
Workflow:

1. Edit the relevant `make_NN()` function.
2. Run the generator (it emits PNGs):
   `QUARTO_PYTHON=.venv/bin/python .venv/bin/python media/generate_diagrams.py`
3. Convert **only the changed** diagrams to WebP: `cwebp -q 90 in.png -o out.webp`
4. Read each changed `.webp` with the image viewer and confirm it looks right.
5. Delete the PNG intermediates — the repo tracks only `.webp`.

## Step 5 — Verify and open a PR

- Run `just render` and confirm `Output created: _site/index.html`.
- `git status` should show only the files you intended to change.
- Work on a branch; write a commit message explaining the *why*.
- Open a PR whose body lists what changed, and — just as important — what you
  **verified as still accurate and intentionally left unchanged**, so the author
  can trust the audit was thorough. Flag any out-of-scope new features as
  suggestions rather than silently adding them.

## Guardrails

- Don't hardcode model version names into slides; the deck's future-proofing
  depends on staying version-agnostic.
- Don't split `index.qmd`, change the RevealJS format, or enable code execution.
- Keep edits surgical. A clean 4-file diff that fixes one real problem beats a
  sprawling rewrite.
