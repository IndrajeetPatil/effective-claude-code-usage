# Effective Claude Code Usage — Project Notes

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

---

## Slide content principle

**Diagrams and text must not restate each other.**
- If a diagram already shows a concept visually (e.g. the three columns of Intelligence
  Spectrum label their own content), do not repeat those same labels as cards or bullet
  points below the diagram. Remove the text.
- Acceptable text below a diagram: quantitative data not shown in the diagram,
  actionable "how to" guidance, caveats, or decisions criteria.
- When in doubt: if removing the text loses zero information (because the diagram
  shows it), remove it.
