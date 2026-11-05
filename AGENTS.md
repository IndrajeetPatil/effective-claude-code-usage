# AGENTS.md

A single-page [Quarto](https://quarto.org/) presentation rendered to
[RevealJS](https://revealjs.com/) slides and deployed as a static site via
GitHub Pages.

## Repository layout

```text
index.qmd            # All slide content (the only file you usually need to edit)
_quarto.yml          # Quarto project config (output dir, resources list)
_quarto-a11y.yml     # Opt-in profile enabling the axe accessibility checker (`just axe`)
accessibility.html   # Compatibility fixes supplementing the a11y extension
style.css            # Custom RevealJS theme (fonts, colours, component classes)
meta-tags.html       # OpenGraph, Twitter Card, JSON-LD, and analytics tags
justfile             # Command runner
media/               # Generated diagrams (and their script), screenshots, social card
llms.txt, llms-full.txt   # Machine-readable summaries (mirrored in .well-known/)
robots.txt, sitemap.xml   # Static crawl files; rarely change
pyproject.toml, uv.lock   # Python dependencies for Quarto's Jupyter engine (uv)
CLAUDE.md            # Imports this file for Claude Code
LICENSE              # CC0 dedication
```

`_site/`, `_extensions/`, `.quarto/` and `.venv/` are gitignored; never commit
them.

## Commands

```bash
just install   # Install Python dependencies and Quarto extensions
just update    # Update Python dependencies
just render    # Render index.qmd to _site/ (run after every change)
just preview   # Live-reload dev server
just clean     # Remove build artefacts
just check     # Verify Quarto and Python setup
just axe       # Preview with the axe accessibility checker enabled
```

## Key conventions

- **Single-file deck.** All slides live in `index.qmd`; do not split it. Slides
  are separated by `##` headings. Use Quarto's RevealJS dialect: fenced divs
  (`:::`), columns (`.columns` / `.column`), raw HTML blocks (`{=html}`), and
  the `{.smaller}` class for dense slides. Follow the layout patterns of
  neighbouring slides.
- **Theme and colours.** Keep the theme `black` and the format `revealjs`;
  restyle through `style.css`. Lay out content with the classes in `style.css`
  rather than inline styles: `.card-green`, `.card-blue`, `.card-amber`,
  `.card-purple`, `.card-red`, `.card-subtle` (plus `.card-compact`), and
  `.terminal-box` for terminal output. New widgets follow the naming patterns
  already in `style.css`.
- **Diagrams and text must not restate each other.** If a diagram already
  shows a concept, do not repeat its labels as cards or bullets below it.
  Text below a diagram is for what the diagram does not show: quantitative
  data, actionable guidance, caveats, or decision criteria. If removing the
  text loses no information, remove it.
- **Generated diagrams.** `media/generate_diagrams.py` produces the WebP
  diagrams with matplotlib and the Caveat font. Load the `generate-diagrams`
  skill before adding or changing one.
- **Sources.** Every factual claim has a source citation at the bottom of its
  slide in a small-font centred div. Keep this pattern.
- **Spelling and punctuation.** Use British spelling in prose (colour, licence,
  catalogue, artefact) and the Oxford comma in lists of three or more. Leave
  code, identifiers, file names, URLs, quotations, and proper names (`license`
  in YAML, `.well-known/api-catalog`) as they are.
- **Spoken notes.** The read-aloud control speaks the `.notes` content. Write
  complete, audience-facing narration; keep staging cues, private reminders,
  and delivery checklists outside these blocks.
- **Accessibility.** Images must have `fig-alt` text; raw HTML widgets use
  `role="img"` and `aria-label`. Load the `check-accessibility` skill before
  changing markup, styles, widgets or the a11y setup.
- **Icons.** Icons are HTML spans backed by only the required SVG path data in
  `style.css`; no icon font or Quarto icon extension. When adding one, add only
  its mask data, preserve the source licence attribution, and keep an
  accessible label where the icon conveys meaning.
- **No code execution.** The front matter sets `execute: eval: false`; code
  blocks are display-only. Do not enable `eval: true` unless the deck genuinely
  needs computed output.
- **Python dependencies.** The deck declares `jupyter: python3`; the virtualenv
  only satisfies Quarto's engine. Depend only on `ipykernel`, `nbclient` and
  `pyyaml`. Do not add the `jupyter` metapackage: it pulls in JupyterLab and
  Notebook and only attracts irrelevant security alerts.
- **Discoverability files.** Update `meta-tags.html` when the title,
  description, or social card changes, and `llms.txt` / `llms-full.txt` (and
  their `.well-known/` mirrors) when the content changes significantly.
- **No new top-level files** without a clear reason; the structure is flat.

## CI/CD

- `.github/workflows/build-presentation.yaml` calls a reusable workflow from
  `IndrajeetPatil/workflows`: pushes to `main` build and deploy to GitHub
  Pages, pull requests build without deploying. Do not inline or modify that
  workflow here.
- Reference reusable workflows as `@main`, never a commit SHA: they are
  first-party, and a pinned SHA once went five months stale.
- Dependabot updates GitHub Actions and `uv` dependencies weekly.
- `check-link-rot.yaml` checks external links on pushes, pull requests and
  weekly (Sunday 00:00 UTC); list false positives in `.lycheeignore`.

## Agent skills

Skills live in `.agents/skills/<name>/SKILL.md`. Load one before its task:

| Skill | Load before |
| --- | --- |
| `check-accessibility` | Changing slide markup, styles, widgets, menus or the a11y setup; any accessibility audit |
| `generate-diagrams` | Adding or changing a diagram in `media/generate_diagrams.py` |
