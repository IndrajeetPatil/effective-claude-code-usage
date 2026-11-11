---
version: alpha
name: Effective Claude Code Usage
description: >-
  Dark terminal visual identity: GitHub dark-inspired palette (#0d1117),
  terminal glows, Space Grotesk headings and body, Space Mono code and chrome,
  and color-accented cards.
colors:
  primary: "{colors.accent-green}"
  bg-primary: "#0d1117"
  bg-secondary: "#161b22"
  bg-card: "#1c2128"
  bg-card-hover: "#21262d"
  accent-green: "#22c55e"
  accent-blue: "#38bdf8"
  accent-amber: "#f59e0b"
  accent-purple: "#a78bfa"
  accent-red: "#f87171"
  text-primary: "#e6edf3"
  text-muted: "#8b949e"
  border-subtle: "#30363d"
typography:
  heading-1:
    fontFamily: Space Grotesk, system-ui, sans-serif
    fontSize: 1.85em
    fontWeight: 700
  heading-2:
    fontFamily: Space Grotesk, system-ui, sans-serif
    fontSize: 1.24em
    fontWeight: 700
  body:
    fontFamily: Space Grotesk, system-ui, sans-serif
    fontSize: 30px
    fontWeight: 400
    lineHeight: 1.34
  mono:
    fontFamily: Space Mono, JetBrains Mono, Fira Code, monospace
rounded:
  sm: 4px
  md: 8px
glows:
  green: "0 0 18px rgba(34, 197, 94, 0.28)"
  blue: "0 0 18px rgba(56, 189, 248, 0.28)"
  amber: "0 0 18px rgba(245, 158, 11, 0.22)"
  purple: "0 0 18px rgba(167, 139, 250, 0.28)"
  red: "0 0 18px rgba(248, 113, 113, 0.22)"
components:
  page:
    backgroundColor: "{colors.bg-primary}"
    textColor: "{colors.text-primary}"
  card-green:
    backgroundColor: "{colors.bg-card}"
    borderColor: "{colors.accent-green}"
    boxShadow: "{glows.green}"
    rounded: "{rounded.md}"
  card-blue:
    backgroundColor: "{colors.bg-card}"
    borderColor: "{colors.accent-blue}"
    boxShadow: "{glows.blue}"
    rounded: "{rounded.md}"
  card-amber:
    backgroundColor: "{colors.bg-card}"
    borderColor: "{colors.accent-amber}"
    boxShadow: "{glows.amber}"
    rounded: "{rounded.md}"
  card-purple:
    backgroundColor: "{colors.bg-card}"
    borderColor: "{colors.accent-purple}"
    boxShadow: "{glows.purple}"
    rounded: "{rounded.md}"
  card-red:
    backgroundColor: "{colors.bg-card}"
    borderColor: "{colors.accent-red}"
    boxShadow: "{glows.red}"
    rounded: "{rounded.md}"
  card-subtle:
    backgroundColor: "{colors.bg-card}"
    borderColor: "{colors.border-subtle}"
    rounded: "{rounded.md}"
---

# DESIGN.md

The visual design specification of the Effective Claude Code Usage presentation deck.

## Overview

The visual design is a dark terminal aesthetic inspired by modern developer tooling: a dark slate canvas (`#0d1117`), GitHub dark palette components, terminal glows, Space Grotesk typography for body text and headings, and Space Mono for terminal chrome, code, and slide numbers.

The presentation format is Quarto RevealJS (`theme: black`). Custom styling is layered via `style.css` and mirrored in the front matter above.

## Colours

- **Canvas & Backgrounds:**
  - `bg-primary` (`#0d1117`): Slide background.
  - `bg-secondary` (`#161b22`): Table header rows and darker surfaces.
  - `bg-card` (`#1c2128`): Default background for cards, code blocks, and callouts.
  - `bg-card-hover` (`#21262d`): Hover state for interactive table rows and cards.
- **Accents & Terminal Glows:**
  - `accent-green` (`#22c55e`): Primary brand accent, title heading (`h1`), inline code, and positive cards (`.card-green`).
  - `accent-blue` (`#38bdf8`): Section slide titles (`h2`), links, table headers, and info cards (`.card-blue`).
  - `accent-amber` (`#f59e0b`): Subheadings (`h3`) and warning cards (`.card-amber`).
  - `accent-purple` (`#a78bfa`): Major section dividers (`level1 h1`), blockquotes, and guidance cards (`.card-purple`).
  - `accent-red` (`#f87171`): Negative examples and caution cards (`.card-red`).
- **Text & Borders:**
  - `text-primary` (`#e6edf3`): Crisp white-grey for high-contrast reading.
  - `text-muted` (`#8b949e`): Subdued text for footers, citations, and secondary metadata.
  - `border-subtle` (`#30363d`): Subtle divider lines, card borders, and table borders.

## Typography

- **Headings & Body:** `Space Grotesk` (weights 300 to 700). Bold headings: h1 in glowing green, h2 in bright blue with a subtle bottom rule, and h3 in amber.
- **Code & Terminal:** `Space Mono` (weights 400 and 700). Monospace font used for code blocks, inline code, terminal simulations (`.terminal-box`), and slide numbers.

## Layout & Components

- **Cards:** Rounded 8px containers with a 1px border and a 4px left accent bar:
  - `.card-green`, `.card-blue`, `.card-amber`, `.card-purple`, `.card-red`.
  - `.card-subtle`: Neutral card with subtle grey border.
  - `.card-compact`: Reduced padding variant for dense multi-column slides.
- **Terminal Box:** `.terminal-box` simulating a CLI terminal window with monospace output.
- **Tables:** Integrated dark card tables with subtle borders, blue headers, and hoverable rows.
- **Callouts:** Standard Quarto callouts styled to match the dark terminal theme with colored left accent borders.

## Do's and Don'ts

- **Do** use predefined CSS classes from `style.css` (`.card-green`, `.card-blue`, etc.) rather than inline styles.
- **Do** ensure text below diagrams provides non-redundant, quantitative or actionable guidance rather than repeating diagram labels.
- **Don't** use light-mode backgrounds or unstyled light cards; keep the dark terminal theme intact across all slides.
- **Don't** hard-code ad-hoc hex colors directly in `index.qmd`.
