# Effective Claude Code Usage

Slides summarising patterns for using [Claude Code](https://docs.anthropic.com/en/docs/claude-code) effectively as a CLI agent — from tools, skills, and workflows to subagents, planning mode, and context management.

The slides can be seen here:<br>
<https://www.indrapatil.com/effective-claude-code-usage/>

[![introductory slide](media/social-media-card.png)](https://www.indrapatil.com/effective-claude-code-usage/)

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
just install  # Install Quarto extensions and Python dependencies
just update   # Update Quarto extensions and Python dependencies
just render   # Render slides to HTML
just preview  # Start a live preview with auto-reload
just open     # Open rendered slides in the default browser
just clean    # Remove generated files and caches
just check    # Check the Quarto and Python setup
just          # Install dependencies, render, and open slides
```

## Feedback

Feedback and suggestions are welcome in [the issue tracker](https://github.com/IndrajeetPatil/effective-claude-code-usage/issues).
