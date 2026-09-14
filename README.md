# Effective Claude Code Usage

Slides summarising patterns for using [Claude Code](https://code.claude.com/docs/en/overview) effectively as a CLI agent — from tools, skills, and workflows to subagents, planning mode, and context management.

The slides can be seen here:<br>
<https://www.indrapatil.com/effective-claude-code-usage/>

[![introductory slide](media/social-media-card.webp)](https://www.indrapatil.com/effective-claude-code-usage/)

## Development

This project uses Python 3.14 (see `.python-version`) with [uv](https://docs.astral.sh/uv/) for dependency management, [Quarto](https://quarto.org/) for rendering slides, and [just](https://github.com/casey/just) as a command runner.

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
just install  # Install Python dependencies and the a11y extension
just update   # Update Python dependencies
just render   # Render slides to HTML
just preview  # Start a live preview with auto-reload
just open     # Alias for preview (live-reload dev server over localhost)
just clean    # Remove generated files and caches
just check    # Check the Quarto and Python setup
just axe      # Preview with an Accessibility Report slide
just          # Install dependencies and start live-reload preview
```

`just axe` enables the opt-in `a11y` profile. It accepts preview options, for example `just axe --no-browser --port 8834`. Inspect slide and scroll views, including all fragments and tab panels. Run `just render` for the production deck, which excludes the audit payload and report.

### Accessibility

`just install` and the shared CI workflow install the latest
[`quarto-revealjs-a11y`](https://github.com/mcanouil/quarto-revealjs-a11y) directly
from upstream with `quarto add mcanouil/quarto-revealjs-a11y --no-prompt`.
The extension handles browser zoom, slide isolation, focus indicators, link
underlines, reduced motion, and screen-reader announcements.

Run `just install` again after `just clean`, which removes installed extensions.

The `accessibility.html` helper still handles scrollable code, slide-menu focus,
and vertical-slide semantics. Unused tabset handling has been removed.
The extension's slide-menu patch and accessibility settings panel are disabled
as in the reference deck: version 0.2.3 introduces ARIA and contrast failures in
those components.

Use `just axe` to inspect slides, fragments, and menu panels in presentation and
scroll views. Normal builds omit the axe checker.

## Feedback

Feedback and suggestions are welcome in [the issue tracker](https://github.com/IndrajeetPatil/effective-claude-code-usage/issues).
