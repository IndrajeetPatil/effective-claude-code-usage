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
_quarto-a11y.yml     # Opt-in profile enabling the axe accessibility checker (`just axe`)
accessibility.html  # Compatibility fixes supplementing the a11y extension
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
_extensions/         # Latest a11y extension, installed by `just install` and CI (gitignored)
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
- **Sources.** Every factual claim has a source citation at the bottom of its slide in a small-font centred div. Keep this pattern.
- **Accessibility.** Images must have `fig-alt` text. Raw HTML widgets use `role="img"` and `aria-label`. Keep these.
  Verify with `just axe`, which appends an "Accessibility Report" slide listing axe-core violations. Keep `axe` in
  `_quarto-a11y.yml`, not `index.qmd`, so production builds exclude the audit payload. CLI metadata such as
  `-M axe:true` cannot override this deck's `format:` block. Links inside muted text need a non-colour cue such as an underline.
  Inspect all slides, revealed fragments, and tab panels in both presentation and scroll view; the initial report alone does not exercise every state.
  The `a11y` extension supplies zoom, focus indicators, link underlines, reduced motion,
  slide isolation, and screen-reader announcements. Keep `accessibility.html` for
  code scrolling, menu focus, vertical-slide semantics, and tabset keyboard navigation.
  This deck has no tabsets today, so the tabset branch of that helper is inert here, but
  the code stays: `accessibility.html` is kept identical across the fleet by hand.
  Never trim it for this deck; add tabsets freely
  and the arrow/Home/End handling already works.
  Disable the extension's slide-menu patch and settings menu as in the reference
  deck: version 0.2.3 introduces ARIA and contrast failures in those components.
- **Icons.** Icons use lightweight HTML spans backed by only the required SVG path data in the custom stylesheet; no icon-font or Quarto icon extension is needed.
  When adding an icon, add only its mask data, preserve the source licence attribution, keep an accessible label where the icon conveys meaning, and render the deck to verify it.
- **Mermaid performance boundary.** Keep Mermaid diagrams as Mermaid source. Do not replace them with pre-rendered SVGs solely to reduce the website bundle.
- **No code execution.** The YAML front matter sets `execute: eval: false`. Code blocks are for display only; they are not executed during render.
- **Compute engine.** Python decks declare `jupyter: python3` in the front matter; R decks declare `engine: knitr`. The virtualenv or renv exists to satisfy Quarto's engine, not to run slide code.
- **Generated diagrams.** `media/generate_diagrams.py` produces cropped WebP diagrams using matplotlib and the Caveat font. See [Diagram generation](#diagram-generation-mediagenerate_diagramspy) below for legibility rules, colour constants, and sizing constraints.

## Commands

All commands use [just](https://github.com/casey/just). The recipes are the same across decks; only the dependency backend differs:

```bash
just install   # Install language dependencies and the latest a11y extension
just sync      # Alias for install
just update    # Update language dependencies
just render    # Render index.qmd to _site/
just preview   # Live-reload dev server
just open      # Alias for preview (live-reload dev server over localhost)
just clean     # Remove build artefacts
just check     # Verify Quarto and Python setup
just axe       # Preview with the axe accessibility checker enabled
```

This deck renders with Quarto. Python dependencies are managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`); CI installs them with `uv sync --frozen`. Slides live in `index.qmd`.

Python decks wrap Quarto in `uv run`, which syncs the environment against `uv.lock` and puts `.venv/bin` on `PATH` so Quarto discovers the project interpreter. R decks call `quarto render` directly (R is discovered automatically). See the `justfile` for exact commands.

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

- The GitHub Actions workflow in `.github/workflows/` renders the deck and deploys to GitHub Pages on push to `main`. It calls a reusable workflow from `IndrajeetPatil/workflows` (Python and R decks use different workflow files). Do not inline the workflow.
- **Reference the first-party reusable workflow as `@main`.** This intentionally receives upstream fixes immediately, including stable Quarto builds and removal of the unused FontAwesome installation. Do not pin it to a commit SHA.
- Install the latest a11y extension directly from upstream with
  `quarto add mcanouil/quarto-revealjs-a11y --no-prompt` in both `justfile` and CI.
  This extension is trusted; do not add version pins, vendoring, or checksum checks.
- Dependabot keeps GitHub Actions dependencies up to date weekly. Python decks also have Dependabot configured for `uv`; R decks do not use Dependabot for R packages.

## What not to do

- Do not add new top-level files without a clear reason; the project intentionally has a flat structure.
- Do not split `index.qmd` into multiple files.
- Do not change the Quarto theme from `simple` or the output format from `revealjs`.
- Do not enable code execution (`eval: true`) unless the presentation genuinely needs computed output.
- Do not commit `_site/`, `_extensions/`, or `.quarto/` (all gitignored). For Python decks, `.venv/` is also gitignored; for R decks, `renv/library/` and `renv/staging/` are gitignored.
- Do not modify the reusable CI workflow inline; it lives in a separate repository.

## Diagram generation (media/generate_diagrams.py)

All diagrams use matplotlib + the Caveat font at DPI=160. `save()` renders each figure,
crops it to the drawn content plus a small margin, and writes the WebP that `index.qmd`
references. Regenerate with `uv run python media/generate_diagrams.py`.

### Legibility rules

**No in-image titles.** The slide heading is the title. Empty bands are cropped away, so
any reserved space would only shrink the diagram on the slide.

**Design for the slide's width, not its height.** Slide CSS caps images at 480px tall and
the slide's content width. A diagram is only as legible as its aspect ratio allows: aim
for width:height of roughly 2.3:1 or wider (`w=11`, `h` about 3.4–4.7) so it is
width-bound and its text renders at about 20px or more. Tall layouts shrink every label.

**Font sizes.** Box labels 19–24 pt, sub-labels and annotations 17–19 pt. Nothing smaller.

**Boxes.** Use `box(ax, x, y, w, h, accent, label, sub=...)`: accent border, dark tinted fill,
accent label, and an optional `TXT` sub-label. Do not use white borders. Leave at least
0.3 units between boxes joined by an arrow, or the arrowhead disappears.

**Labels own their space.** Section headers, bracket labels, and edge annotations
(`heading()`, `bracket()`, `lbl()`) each sit in their own horizontal band, never on top
of an arrow or box. Put column headers above background panels, not inside them.

**Checklist before committing a diagram**
- [ ] No text overlaps a box edge, arrow, or other text
- [ ] Every arrowhead is visible
- [ ] Printed size is width-bound (see aspect rule above)
- [ ] Visually inspect the WebP (convert with `dwebp` if needed) via the `Read` tool,
      and on the rendered slide
- [ ] The slide's `fig-alt` text describes the new content

### Colours (always use these constants — never hardcode hex in diagrams)
```
BG=#0d1117  GRN=#22c55e  BLU=#38bdf8  AMB=#f59e0b  PUR=#a78bfa  RED=#f87171
TXT=#e6edf3  MUT=#a8b3c1  CARD=#1c2128
```
Box fills come from `tint(accent)`, which blends 16% of the accent into `BG`. These dark
fills keep accent-coloured text above WCAG AA contrast; do not brighten them.

### Font glyphs
- Caveat.ttf does not contain Unicode check marks (✓ U+2713) or other special symbols,
  and has no bold weight. Use plain ASCII alternatives: `+`, `-`, `>`, `x`, `ok`.

## Slide content principle

**Diagrams and text must not restate each other.**
- If a diagram already shows a concept visually (e.g. the three columns of Intelligence
  Spectrum label their own content), do not repeat those same labels as cards or bullet
  points below the diagram. Remove the text.
- Acceptable text below a diagram: quantitative data not shown in the diagram,
  actionable "how to" guidance, caveats, or decisions criteria.
- When in doubt: if removing the text loses zero information (because the diagram
  shows it), remove it.

- **Spelling and punctuation.** Use British spelling in prose (colour, licence, catalogue, artefact) and the Oxford comma in lists of three or more. Leave code, identifiers, file names, URLs, quotations, and proper names (`license` in YAML, `.well-known/api-catalog`) as they are.
