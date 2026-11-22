---
name: documentation-illustrations
description: >
  Create illustrations that match the look of Anthropic's own documentation
  and website: clean technical diagrams in the Claude Code docs style, and
  editorial collage art in the anthropic.com style. Covers when to reuse an
  existing docs image, the palette, typography, composition rules, and
  ready-to-fill image-generation prompts. Use before generating or drawing
  any diagram, hero image, or concept illustration for docs or slides.
---

# Documentation illustrations

Anthropic's sites use two illustration families. Pick one per image and never
mix them.

| Family | Use for | Looks like |
| --- | --- | --- |
| **Technical diagram** | Flows, loops, architectures, precedence, "what loads when" | Flat boxes and arrows on a warm off-white panel, small sans labels |
| **Editorial collage** | Title slides, section openers, blog-style heroes, abstract ideas | Flat muted field, grid-paper shapes, engraving cut-outs, ink line drawings |

## Step 0: reuse before you generate

Search the Claude Code docs first. Each page's Markdown (`<page>.md`, indexed
at `https://code.claude.com/docs/llms.txt`) lists its images on
`mintcdn.com`. If an existing image shows the idea, download it, store it
locally, and credit it in a single line: `Illustration: Claude Code docs,
<page title>` linked to the page. Generate only what no existing image covers.

Never reproduce Anthropic or Claude logos, the asterisk mark, wordmarks, or
product screenshots in generated art.

## Family A: technical diagram

### Palette

| Role | Hex |
| --- | --- |
| Panel background | `#F9F9F7` (page behind it `#FDFDF7`) |
| Neutral box fill | `#E8E8E4` (secondary `#EDEDEB`, `#F0F0EC`) |
| Primary text | `#1E1E1E` |
| Secondary text, arrows, connectors | `#757575` (light lines `#B0B0B0`, `#D0D0CC`) |
| Green "active / Claude does this" box | fill `#D4E4D8`, stroke or text `#4A8C5C` |
| Clay "you / external input" box | fill `#FDF6F2` or `#FCEEE0`, stroke `#D4A27F` |
| Lavender "service / gateway" box | fill `#EDE8F4`, text `#6B5A88` |
| Butter "note / verification" box | fill `#FFF8E1` |
| Rose "blocked / stop" box | fill `#F8D7D7`-ish, stroke `#D07A70` |
| Steel blue (rare emphasis) | `#6AA8D0` fill or `#7A8BA8` line |

Most boxes are neutral grey. Use colour only to encode meaning, at most three
accent hues per diagram, and keep text dark (`#1E1E1E`) on every fill.

### Shapes and lines

- Rounded rectangles, radius 4–8px; many boxes have **no stroke at all**, just
  a fill. When stroked, use a 1–1.5px line in the box's accent.
- Grouping containers: a large rounded rectangle with a dashed `#D0D0CC`
  outline (`5 3` dash) and a small grey label in its top-left or top-centre
  ("agentic loop", "Your infrastructure", "VPC").
- Optional or external items: dashed outline, white or transparent fill,
  muted text.
- Arrows: straight or orthogonal (right-angle) connectors, 1.5px `#757575`,
  small solid triangular heads. Highlight the main loop with a thicker 2px
  green `#4A8C5C` arrow; show human intervention as a dashed clay arrow.
- Edge labels: tiny grey sans text sitting beside the line, never on it.
- Columns: headers in grey semibold above each column ("Session start",
  "On use", "Isolated"), separated by faint dashed vertical rules.
- A legend of small swatches along the bottom when fills encode categories.

### Typography

- Sans-serif (system UI or Inter). Box titles 12–14px semibold `#1E1E1E`;
  sub-labels 10–11px regular `#757575` on a second line.
- Commands, file names, and API calls in a monospace face.
- Optional diagram title: centred, semibold, 14–15px, at the top of the panel.
- Sentence case everywhere; uppercase only for a rare spaced-out container
  label (for example "AGENTIC LOOP" in clay).

### Composition

- Wide landscape, roughly 2.5:1 to 3:1 (720×280 is typical), flat panel with
  8px rounded corners and generous padding.
- Read left to right; loops return underneath the main row.
- No shadows, gradients, 3D, icons, emoji, or decorative illustration.
- One idea per diagram; 3–8 boxes is the sweet spot.

### Prefer code over pixels

Image generators blur small text. For any diagram with labels, write SVG (or
draw with a plotting library) using the values above, then rasterise if
needed. Use image generation only when the target agent cannot write vector
output, and then keep labels to a few large words.

### Prompt template (if you must generate)

```text
A clean, flat technical diagram in the style of modern developer
documentation. Warm off-white panel (#F9F9F7) with softly rounded corners.
Left-to-right flow of rounded rectangles: <BOX 1>, <BOX 2>, <BOX 3>.
Most boxes are flat light grey (#E8E8E4) with no outline; <ACTIVE BOXES> are
pale sage green (#D4E4D8). Thin grey arrows (#757575) with small solid
arrowheads; a green arrow loops back underneath labelled "<LOOP LABEL>".
A dashed light-grey container groups <GROUP> with a small grey label.
Dark charcoal sans-serif labels in sentence case, crisp and legible.
No shadows, no gradients, no icons, no logos, no 3D, lots of white space.
Wide 3:1 aspect ratio.
```

## Family B: editorial collage

### Palette

| Role | Hex |
| --- | --- |
| Olive field (signature) | `#75855B` (lighter `#899A6B`) |
| Cream paper | `#E9DFC8`, `#D6CFBF` |
| Ink black | `#23292A` |
| Coral / pink | `#E8857A`, `#E9A3A8` |
| Cobalt blue | `#1F6FC0`, `#4881BA` |
| Marigold | `#E8A23A` |
| Teal | `#4D7478`, `#599082` |
| Lavender field | `#CFC6E6` |
| Lemon accent | `#F2E640` |

### Ingredients

- A single flat, slightly muted background colour filling the frame (olive
  is the most recognisable; also sky blue, lavender, cream).
- Geometric shapes (circles, bars, rectangles) filled with saturated flat
  colour and overprinted with a fine **graph-paper grid** of thin dark lines.
- Cut-out fragments of vintage engravings, technical drawings, or
  black-and-white archival photos (lab equipment, drafting compasses,
  geometry constructions), placed with hard paper edges.
- Loose, single-weight hand-inked line drawings (mountains, curves, simple
  creatures) in black or cobalt.
- Paper textures: marbled endpapers, risograph grain, slight misregistration.
- Overlapping translucent shapes that mix where they cross (Venn-style).

### Composition

- Calm and sparse: one focal idea, lots of empty field.
- Strong horizontals or a centred cluster; shapes often stepped or repeated
  to suggest a sequence or scale (small → large circles).
- No text, no UI, no people's faces as the focus, no gradients, no glossy 3D,
  no robots, no glowing brains, no circuit boards.

### Prompt template

```text
Editorial collage illustration for a technology essay. Flat muted olive green
background (#75855B). <CENTRAL METAPHOR expressed as simple geometric shapes>,
each filled with flat <coral / cobalt / marigold / deep green> and overlaid
with a fine graph-paper grid. Add a cut-out fragment of a vintage engraving
of <RELATED OBJECT> with crisp paper edges, and a few loose hand-inked black
lines. Subtle risograph grain and paper texture. Sparse, balanced
composition with generous empty space. No text, no logos, no gradients,
no 3D rendering, no robots. <ASPECT RATIO>.
```

Example metaphors: steps of a process → stepped grid-paper bars of
increasing length; isolation → separate circles on their own grid tiles;
growth or scale → a row of circles growing left to right; review → a drafting
compass over a grid.

## Checklist

- [ ] Checked the docs for an existing image first, and credited any reuse
- [ ] One family only, with the palette above
- [ ] Diagram labels are vector text, legible at slide size, and sentence case
- [ ] Colour encodes meaning; three accents or fewer
- [ ] No logos, wordmarks, shadows, gradients, or decorative icons
- [ ] Alt text describes what the image shows, not how it looks
