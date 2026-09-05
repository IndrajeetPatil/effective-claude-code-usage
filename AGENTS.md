# AGENTS.md

Project-level instructions for AI coding agents working on this repository —
Codex, GitHub Copilot (code review and coding agent), and other
`AGENTS.md`-aware tools read this file directly.

## What this is

A single-page [Quarto](https://quarto.org/) presentation rendered to [RevealJS](https://revealjs.com/) slides and deployed as a static site via GitHub Pages.

## Repository layout

```
index.qmd           # All slide content (the only file you usually need to edit)
_quarto.yml          # Quarto project config (output dir, resources list)
style.css            # Custom RevealJS theme (fonts, colours, component classes)
meta-tags.html       # OpenGraph, Twitter Card, JSON-LD, and analytics tags
justfile             # Command runner (install, render, preview, clean, etc.)
media/               # Images: diagrams, evidence screenshots, illustrations, social card
llms.txt             # Short machine-readable summary for LLM discovery
llms-full.txt        # Extended machine-readable summary
.well-known/         # Mirrors of llms.txt and llms-full.txt
robots.txt           # Crawl rules
sitemap.xml          # Sitemap for search engines
.github/             # CI workflow (reusable, from IndrajeetPatil/workflows) and Dependabot
_extensions/         # Optional Quarto extensions (gitignored; currently unused)
_site/               # Build output (gitignored)
```

### Language-specific files

Python-based decks also have:

```
pyproject.toml       # Project metadata and dependencies (managed by uv)
uv.lock              # Locked Python dependencies
.python-version      # Python version pin
.venv/               # Python virtualenv (gitignored)
```

R-based decks have instead:

```
renv.lock            # Locked R dependencies
renv/                # renv library and infrastructure (library/ is gitignored)
.Rprofile            # Bootstraps renv on session start
```

Check which set is present to know which language context applies.

## Key conventions

- **Single-file deck.** All slides live in `index.qmd`. There are no partial includes or multi-file splits.
- **Slide syntax.** Slides are separated by `##` headings. Use Quarto's RevealJS dialect: fenced divs (`:::`), columns (`.columns` / `.column`), raw HTML blocks (`{=html}`), and the `{.smaller}` class for dense slides.
- **Inline styling.** Visual design uses inline `style` attributes on fenced divs with a small palette of background colours (e.g. `#e3f2fd`, `#e8f5e9`, `#fff3e0`, `#ffebee`, `#FFFBC1`, `#f8f9fa`). The CSS maps these to the custom theme. Do not change these colour values without updating `style.css`.
- **Image classes.** Images may use semantic classes (e.g. `.hero`, `.artifact`, `.illustration`) that control border, shadow, and rounding in `style.css`. Check the existing CSS before adding new image classes.
- **Sources.** Every factual claim has a source citation at the bottom of its slide in a small-font centered div. Keep this pattern.
- **Accessibility.** Images must have `fig-alt` text. Raw HTML widgets use `role="img"` and `aria-label`. Keep these.
- **Icons.** Icons use lightweight HTML spans backed by only the required SVG path data in the custom stylesheet; no icon-font or Quarto icon extension is needed.
  When adding an icon, add only its mask data, preserve the source licence attribution, keep an accessible label where the icon conveys meaning, and render the deck to verify it.
- **Mermaid performance boundary.** Keep Mermaid diagrams as Mermaid source. Do not replace them with pre-rendered SVGs solely to reduce the website bundle.
- **No code execution.** The YAML front matter sets `execute: eval: false`. Code blocks are for display only; they are not executed during render.
- **Compute engine.** Python decks declare `jupyter: python3` in the front matter; R decks declare `engine: knitr`. The virtualenv or renv exists to satisfy Quarto's engine, not to run slide code.
- **Generated diagrams.** `media/generate_diagrams.py` produces PNG diagrams using matplotlib and the Caveat font. See [Diagram generation](#diagram-generation-mediagenerate_diagramspy) below for detailed layout rules, colour constants, and sizing constraints.

## Commands

All commands use [just](https://github.com/casey/just). The recipes are the same across decks; only the dependency backend differs:

```bash
just install   # Install language dependencies
just render    # Render index.qmd to _site/
just preview   # Live-reload dev server
just open      # Alias for preview (live-reload dev server over localhost)
just clean     # Remove build artifacts
just check     # Verify Quarto setup
just update    # Update language dependencies
```

Python decks prefix the render command with `QUARTO_PYTHON=.venv/bin/python`. R decks call `quarto render` directly (R is discovered automatically). See the `justfile` for exact commands.

## Editing slides

When modifying `index.qmd`:

1. Follow the existing card/column layout patterns visible in neighbouring slides.
2. Preserve the source-citation div at the bottom of each slide.
3. Use the established background-colour palette for info cards rather than inventing new colours.
4. Keep `fig-alt` on every image and `aria-label` on HTML widgets.
5. Run `just render` (or `just preview`) to verify changes compile without errors.

## Editing styles

`style.css` defines CSS custom properties under `:root` and component classes for complex HTML widgets. The variable names and widget classes vary per deck. When adding a new widget, follow the naming and structure patterns already present in the file.

## SEO and discoverability files

- `meta-tags.html` contains OpenGraph, Twitter Card, JSON-LD structured data, and Google Analytics. Update it when the title, description, or social card image changes.
- `llms.txt` and `llms-full.txt` are machine-readable summaries following the llms.txt convention. Update them when the deck content changes significantly.
- `sitemap.xml` and `robots.txt` are static and rarely need changes.

## CI/CD

- The GitHub Actions workflow in `.github/workflows/` renders the deck and deploys to GitHub Pages on push to `main`. It calls a reusable workflow from `IndrajeetPatil/workflows` (Python and R decks use different workflow files). Do not inline the workflow; update the ref SHA if the upstream workflow changes.
- Dependabot keeps GitHub Actions dependencies up to date weekly. Python decks also have Dependabot configured for `uv`; R decks do not use Dependabot for R packages.

## What not to do

- Do not add new top-level files without a clear reason; the project intentionally has a flat structure.
- Do not split `index.qmd` into multiple files.
- Do not change the Quarto theme from `simple` or the output format from `revealjs`.
- Do not enable code execution (`eval: true`) unless the presentation genuinely needs computed output.
- Do not commit `_site/`, `_extensions/`, or `.quarto/` (all gitignored). For Python decks, `.venv/` is also gitignored; for R decks, `renv/library/` and `renv/staging/` are gitignored.
- Do not modify the reusable CI workflow inline; it lives in a separate repository.

## Diagram generation (media/generate_diagrams.py)

All diagrams use matplotlib + Caveat font at DPI=100, rendered as PNG for RevealJS slides.

### Layout rules learned the hard way

**Title placement**
- The `title()` helper uses `y_off=0.55` (not the original 0.28). This reserves ~0.55 inches below
  the top edge for the title text (~0.44 inches tall at fs=32) plus a visible gap.
- The topmost content element's TOP EDGE must sit at `h - 0.55 - 0.50` or lower.
  Formula: `top_content_y + half_height ≤ h - 1.05`
- When adding a new diagram, compute this before placing any element. If the top element
  violates the constraint, increase the figure height — do NOT move `y_off`.

**Never embed group labels inside group backgrounds**
- `group_bg()` with `label=` places text at the inner-top of the rectangle (zorder=2).
  Child boxes drawn inside the group use zorder=3 and WILL overdraw the label text.
- Two safe alternatives (pick one):
  1. Place standalone `ax.text(...)` calls ABOVE the group rect, in a dedicated gap row.
  2. Skip `group_bg` labels entirely for diagrams where child boxes fill the group area,
     and use a separate row of styled text + thin `ax.plot` rule as a section divider
     (see `make_08`, `make_10`).
- The `group_bg(label=...)` parameter is only safe when no child box occupies
  the top portion of the group (i.e. boxes start >0.5 units below the group top edge).

**Column/section headers**
- When columns have colored background groups, put column header text as standalone
  `ax.text(...)` calls in a horizontal band ABOVE the group backgrounds, not inside them.
  See `make_01` for the pattern: headers at a fixed y above the groups, groups without labels.

**Checklist before saving each diagram**
- [ ] Title center y = `h - 0.55`; nothing has its top edge within 0.5 units of the title center
- [ ] No `group_bg` label is at a y where a child box top edge also exists
- [ ] All text labels (section headers, edge annotations) occupy their own horizontal band
- [ ] Visually inspect the PNG via `Read` tool immediately after generation

**How to check: calculate top edge of topmost element**
  ```
  element top edge = center_y + height/2
  safe if: element top edge ≤ (h - 0.55) - 0.50
  ```

### Figure sizing
- Use `w=11` for horizontal layouts, `w=9` for vertical flowcharts.
- When only increasing height to fix a title overlap, keep all content y-coordinates
  unchanged — the extra space accretes at the top, which is exactly what's needed.
- Do NOT change DPI (keep 100) — RevealJS scales images; lower DPI = larger apparent text.

### Colours (always use these constants — never hardcode hex in diagrams)
```
BG=#0d1117  GRN=#22c55e  DGRN=#14532d
BLU=#38bdf8  DBLU=#0c2a3a  AMB=#f59e0b  DAMB=#3a2400
PUR=#a78bfa  DPUR=#2d1b69  RED=#f87171  DRED=#450a0a
TXT=#e6edf3  MUT=#8b949e  CARD=#1c2128
```

### Font glyphs
- Caveat.ttf does not contain Unicode check marks (✓ U+2713) or other special symbols.
  Use plain ASCII alternatives: `+`, `-`, `>`, `x`, `ok`.

## Slide content principle

**Diagrams and text must not restate each other.**
- If a diagram already shows a concept visually (e.g. the three columns of Intelligence
  Spectrum label their own content), do not repeat those same labels as cards or bullet
  points below the diagram. Remove the text.
- Acceptable text below a diagram: quantitative data not shown in the diagram,
  actionable "how to" guidance, caveats, or decisions criteria.
- When in doubt: if removing the text loses zero information (because the diagram
  shows it), remove it.
