# Effective Claude Code Usage

Slides summarising patterns for using [Claude Code](https://docs.anthropic.com/en/docs/claude-code) effectively as a CLI agent — from tool use and slash commands to subagents, planning mode, and context management.

The slides can be seen here:<br>
<https://www.indrapatil.com/effective-claude-code-usage/>

# Development

This project uses Python 3.14+ with [uv](https://docs.astral.sh/uv/) for dependency management, [Quarto](https://quarto.org/) for rendering slides, and [just](https://github.com/casey/just) as a command runner. GitHub Pages deployment is automatic via GitHub Actions on push to main.

## Prerequisites

```bash
# Install just (macOS)
brew install just
```

## Setup

```bash
# Install dependencies
just install

# Or update to latest versions
just update
```

## Common Commands

```bash
just help      # Show all available commands
just render    # Render slides to HTML
just preview   # Live preview with auto-reload
just open      # Open rendered slides in browser
just clean     # Remove generated files
just check     # Check Quarto and Python setup
just           # Install, render, and open slides (default)
```

# Feedback

Thoughts and comments welcome [here](https://github.com/IndrajeetPatil/effective-claude-code-usage/issues).

# Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](https://www.contributor-covenant.org/version/3/0/code_of_conduct/). By contributing to this project, you agree to abide by its terms.
