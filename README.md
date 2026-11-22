# Effective Claude Code Usage

[![Build and Deploy Presentation](https://github.com/IndrajeetPatil/effective-claude-code-usage/actions/workflows/build-presentation.yaml/badge.svg)](https://github.com/IndrajeetPatil/effective-claude-code-usage/actions/workflows/build-presentation.yaml)

Slides with practical advice for getting reliable work out of [Claude Code](https://code.claude.com/docs/en/overview): tell it what it can't see, give it a check to run, enforce the rules that can't bend, and change a default only when it costs too much. The deck then covers steering a session, unattended runs, and advice you can stop following. Its look follows the Claude Code documentation site, and a few slides reuse the docs' own illustrations with attribution.

The slides can be seen here:<br>
<https://www.indrapatil.com/effective-claude-code-usage/>

[![Effective Claude Code Usage, a talk by Indrajeet Patil, with four fixes](media/social-media-card.webp)](https://www.indrapatil.com/effective-claude-code-usage/)

## Development

This project uses Python 3.15 (see `.python-version`) with [uv](https://docs.astral.sh/uv/) for dependency management, [Quarto](https://quarto.org/) for rendering slides, and [just](https://github.com/casey/just) as a command runner.

### Prerequisites

```bash
# Install just (macOS)
brew install just
```

### Setup

```bash
just install
```

### Just Commands

```bash
just help     # Show all available commands
just install  # Install Python dependencies and Quarto extensions
just update   # Update Python dependencies
just render   # Render slides to HTML
just preview  # Start a live preview with auto-reload
just open     # Alias for preview (live-reload dev server over localhost)
just clean    # Remove generated files and caches
just check    # Check the Quarto and Python setup
just axe      # Preview with an Accessibility Report slide
just          # Install dependencies and start live-reload preview
```

Diagrams come from `media/generate_diagrams.py` (`uv run python media/generate_diagrams.py`); the social card is a screenshot of `media/social-card-source.html` at 1600×900. See [DESIGN.md](DESIGN.md) for the visual system.

`just axe` enables the opt-in `a11y` profile. It accepts preview options, for example `just axe --no-browser --port 8834`. Inspect slide and scroll views, including all fragments and tab panels. Run `just render` for the production deck, which excludes the audit payload and report.

### Accessibility

`just install` and the shared CI workflow install the latest
[`quarto-revealjs-a11y`](https://github.com/mcanouil/quarto-revealjs-a11y) directly
from upstream with `quarto add mcanouil/quarto-revealjs-a11y --no-prompt`.
The extension handles browser zoom, slide isolation, focus indicators, link
underlines, reduced motion, and screen-reader announcements.

Run `just install` again after `just clean`, which removes installed extensions.

The `accessibility.html` helper handles scrollable code, slide-menu focus,
and vertical-slide semantics. The extension's slide-menu patch and accessibility
settings panel are disabled because they introduce ARIA and contrast failures.

Use `just axe` to inspect slides, fragments, and menu panels in presentation and
scroll views. Normal builds omit the axe checker.

## Feedback

Feedback and suggestions are welcome in [the issue tracker](https://github.com/IndrajeetPatil/effective-claude-code-usage/issues).

### Read aloud

Requires Quarto 1.11.9 or newer. `just install` installs the [Read Aloud extension](https://github.com/IndrajeetPatil/quarto-read-aloud). Select the speaker icon to hear the current slide’s notes, or the stop icon to cancel. Changing slides also stops speech. Voice availability depends on your browser and operating system.
