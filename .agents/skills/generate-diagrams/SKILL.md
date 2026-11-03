---
name: generate-diagrams
description: >
  Add or change the deck's WebP diagrams in media/generate_diagrams.py
  (matplotlib + Caveat font): legibility and sizing rules, box and label
  helpers, colour constants, font-glyph limits, and the pre-commit checklist.
  Use before adding, editing or regenerating any diagram.
---

# Generate diagrams

All diagrams use matplotlib and the Caveat font at DPI=160. `save()` renders
each figure, crops it to the drawn content plus a small margin, and writes the
WebP that `index.qmd` references. Regenerate with
`uv run python media/generate_diagrams.py`.

## Legibility rules

- **No in-image titles.** The slide heading is the title. Empty bands are
  cropped away, so any reserved space would only shrink the diagram.
- **Design for the slide's width, not its height.** Slide CSS caps images at
  480px tall and the slide's content width. Aim for width:height of roughly
  2.3:1 or wider (`w=11`, `h` about 3.4–4.7) so the diagram is width-bound and
  its text renders at about 20px or more. Tall layouts shrink every label.
- **Font sizes.** Box labels 19–24 pt, sub-labels and annotations 17–19 pt.
  Nothing smaller.
- **Boxes.** Use `box(ax, x, y, w, h, col, label, sub=...)`: accent border,
  dark tinted fill, accent label, and an optional `TXT` sub-label. Do not use
  white borders. Leave at least 0.3 units between boxes joined by an arrow, or
  the arrowhead disappears.
- **Labels own their space.** Section headers, bracket labels, and edge
  annotations (`heading()`, `bracket()`, `lbl()`) each sit in their own
  horizontal band, never on top of an arrow or box. Put column headers above
  background panels, not inside them.

## Colours

Always use these constants; never hard-code hex values in diagrams:

```text
BG=#0d1117  GRN=#22c55e  BLU=#38bdf8  AMB=#f59e0b  PUR=#a78bfa  RED=#f87171
TXT=#e6edf3  MUT=#a8b3c1  CARD=#1c2128
```

Box fills come from `tint(accent)`, which blends 16% of the accent into `BG`.
These dark fills keep accent-coloured text above WCAG AA contrast; do not
brighten them.

## Font glyphs

`Caveat.ttf` has no Unicode check marks (✓ U+2713) or other special symbols,
and no bold weight. Use plain ASCII alternatives: `+`, `-`, `>`, `x`, `ok`.

## Checklist before committing a diagram

- [ ] No text overlaps a box edge, arrow, or other text
- [ ] Every arrowhead is visible
- [ ] Printed size is width-bound (see the aspect rule above)
- [ ] The WebP is visually inspected (convert with `dwebp` if needed), and so
      is the rendered slide
- [ ] The slide's `fig-alt` text describes the new content
