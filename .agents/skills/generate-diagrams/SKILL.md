---
name: generate-diagrams
description: >
  Add or change the deck's WebP diagrams in media/generate_diagrams.py
  (matplotlib, Inter and JetBrains Mono, Claude Code docs style): when to reuse
  a docs illustration instead, legibility and sizing rules, box and label
  helpers, colour constants, and the pre-commit checklist. Use before adding,
  editing or regenerating any diagram.
---

# Generate diagrams

## Reuse the docs first

Before drawing anything, check whether the
[Claude Code docs](https://code.claude.com/docs/en/overview) already illustrate
the idea (the `.md` version of a page lists its images). If one fits, save it
as `media/docs-<name>.svg`, give it the `.diagram` class, and
credit it in the slide's `.source` line as
`Illustration: [Claude Code docs, <page title>](<page url>)`.

## Our own diagrams

All diagrams use matplotlib at DPI=160 with `Inter` for labels and
`JetBrains Mono` for commands and paths (fonts live in `media/`). They mimic
the docs' diagrams: a warm panel, pastel boxes with a thin accent outline, and
dark text. `save()` crops each figure to its content plus a margin and writes
the WebP that `index.qmd` references. Regenerate with
`uv run python media/generate_diagrams.py`.

## Legibility rules

- **No in-image titles.** The slide heading is the title.
- **Design for the slide's width.** A diagram grows to fill the height the
  slide leaves free, but stays width-bound. Use `w=12` and `h` of about 3–4.5
  (roughly 2.7:1 to 4:1) and avoid empty bands inside the figure, which waste
  that height.
- **Font sizes.** Box labels 17–21 pt, sub-labels and annotations 14–17 pt.
  Nothing smaller than 14 pt.
- **Boxes.** Use `box(ax, x, y, w, h, col, label, sub=..., mono=...)`: pastel
  fill from `FILL[col]`, accent outline, dark semibold label, muted sub-label.
  Leave at least 0.3 units between boxes joined by an arrow.
- **Labels own their space.** `heading()` (uppercase eyebrow) and `lbl()` sit
  in their own band, never on top of an arrow or box.

## Colours

Always use these constants; never hard-code hex values in diagrams:

```text
BG=#F6F5EF  TXT=#171717  MUT=#5F5F5D  LINE=#8F8E8A
CLAY=#D97757  GRN=#6E9E6E  BLU=#6A8FBF  AMB=#D4A24C  PUR=#9C86C4  RED=#D07A70  GRY=#B5B3AC
```

Box text is always `TXT` or `MUT`, never an accent colour, so it keeps WCAG
AA contrast on the pastel fills. Coloured annotation text uses the darker ink
values already in the script (`#A3482A`, `#2F5C8F`, `#3F6B3F`, `#A83A2E`).

## Checklist before committing a diagram

- [ ] No docs illustration already covers the idea
- [ ] No text overlaps a box edge, arrow, or other text
- [ ] Every arrowhead is visible
- [ ] The WebP is visually inspected, and so is the rendered slide
- [ ] The slide's `fig-alt` text describes the new content
