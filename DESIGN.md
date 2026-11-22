---
version: beta
name: Effective Claude Code Usage
description: >-
  Light documentation look modelled on the Claude Code docs site: warm cream
  canvas, serif display titles, Inter body, uppercase eyebrow labels, pastel
  diagrams with thin accent borders, and hairline cards.
colors:
  primary: "{colors.clay}"
  bg-canvas: "#fdfdf7"
  bg-panel: "#f6f5ef"
  bg-surface: "#ffffff"
  bg-code: "#f0efea"
  text-primary: "#171717"
  text-muted: "#5f5f5d"
  border-subtle: "#e2e1da"
  border-strong: "#cfcfcb"
  clay: "#d97757"
  clay-ink: "#a3482a"
  tint-clay: "#fbeee6"
  tint-green: "#eaf1e6"
  tint-blue: "#e8eff7"
  tint-amber: "#faf0dc"
  tint-purple: "#efeaf7"
  tint-red: "#f8e5e2"
typography:
  heading-1:
    fontFamily: Source Serif 4, Georgia, serif
    fontSize: 3em
    fontWeight: 400
  heading-2:
    fontFamily: Source Serif 4, Georgia, serif
    fontSize: 1.75em
    fontWeight: 400
  eyebrow:
    fontFamily: Inter, system-ui, sans-serif
    fontSize: 0.56em
    fontWeight: 600
    textTransform: uppercase
  body:
    fontFamily: Inter, system-ui, sans-serif
    fontSize: 31px
    fontWeight: 400
    lineHeight: 1.5
  mono:
    fontFamily: JetBrains Mono, ui-monospace, monospace
rounded:
  sm: 6px
  md: 12px
components:
  page:
    backgroundColor: "{colors.bg-canvas}"
    textColor: "{colors.text-primary}"
  card-green:
    backgroundColor: "{colors.tint-green}"
    borderColor: "{colors.border-subtle}"
    rounded: "{rounded.md}"
  card-blue:
    backgroundColor: "{colors.tint-blue}"
    borderColor: "{colors.border-subtle}"
    rounded: "{rounded.md}"
  card-amber:
    backgroundColor: "{colors.tint-amber}"
    borderColor: "{colors.border-subtle}"
    rounded: "{rounded.md}"
  card-purple:
    backgroundColor: "{colors.tint-purple}"
    borderColor: "{colors.border-subtle}"
    rounded: "{rounded.md}"
  card-red:
    backgroundColor: "{colors.tint-red}"
    borderColor: "{colors.border-subtle}"
    rounded: "{rounded.md}"
  card-subtle:
    backgroundColor: "{colors.bg-surface}"
    borderColor: "{colors.border-subtle}"
    rounded: "{rounded.md}"
---

# DESIGN.md

The visual design specification of the Effective Claude Code Usage presentation deck.

## Overview

The deck follows the look and feel of the [Claude Code documentation](https://code.claude.com/docs/en/overview): a warm cream page, large serif titles, a quiet sans-serif body, small uppercase eyebrow labels above titles, light code panels, and pastel diagrams on a slightly darker panel.

The format is Quarto RevealJS (`theme: black` as the base, restyled entirely through `style.css`). Code blocks use Quarto's `github` highlight style, with token colours pinned in `style.css` to the docs' light code palette.

## Content principles

- **Advice, not a feature tour.** Each slide answers "what should I do differently?". Leave out reference material (command lists, tool catalogues) that the docs already cover.
- **Show, then caption.** Lead with a diagram, comparison, tiles, or a short code block. Add at most one or two short cards for what the visual does not show.
- **Fill the frame.** No slide should leave a large empty band. Content slides are flex columns: the diagram grows into the free height, fill widgets stretch, and the source line sits on the bottom edge. Prefer cutting or splitting a slide over shrinking text.
- **Reuse docs illustrations.** When the Claude Code docs already have an illustration of the idea, use it (stored as `media/docs-*.svg`) and credit it in the slide's source line as `Illustration: [Claude Code docs, <page>](url)`. Draw our own only when no docs illustration fits.

## Colours

- **Surfaces:**
  - `bg-canvas` (`#fdfdf7`): slide background, the docs' page colour.
  - `bg-panel` (`#f6f5ef`): diagram panels, code-block filename tabs, and terminal title bars.
  - `bg-surface` (`#ffffff`): code blocks, tiles, and `.card-subtle`.
  - `bg-code` (`#f0efea`): inline code.
- **Text and lines:**
  - `text-primary` (`#171717`): headings, body, and links.
  - `text-muted` (`#5f5f5d`): lead paragraphs, tile text, and source lines.
  - `border-subtle` (`#e2e1da`) and `border-strong` (`#cfcfcb`): hairlines on cards, code, and table rows.
- **Accent:** `clay` (`#d97757`) for the progress bar and decorative marks; `clay-ink` (`#a3482a`) wherever clay must carry text.
- **Tints:** `tint-clay`, `tint-green`, `tint-blue`, `tint-amber`, `tint-purple`, and `tint-red` are pale backgrounds for cards and diagram boxes. Text on a tint stays `text-primary`.

## Typography

- **Titles:** `Source Serif 4`, weight 400, an open stand-in for the docs' serif display face. Slide titles are 1.75em; section titles are 3em.
- **Eyebrow:** set a slide's `data-eyebrow` attribute (for example `{data-eyebrow="Part 2 · Check"}`) to print a small uppercase Inter label above its title.
- **Body:** `Inter`, 31px base on a 1280×720 slide with a 0.03 margin, line height 1.5. Bold is weight 600.
- **Code:** `JetBrains Mono` for inline code, code blocks, terminal boxes, and the slide number. Commands, flags, keys, model names, settings, hook events, and config files are always mono, in slides and diagrams alike.

## Layout and components

- **Section slides** (`#` headings): left-aligned docs page header with an eyebrow, a large serif title, one muted lead sentence, and a `.symptom` card ("You'll notice …") naming the problem the part fixes.
- **Lead** (`.lead`): the muted one-line description below a title.
- **Diagrams** (`.diagram`): rounded images on the panel colour that grow to fill the height left by the title, cards, and source line.
- **Cards** (`.card-green`, `.card-blue`, `.card-amber`, `.card-purple`, `.card-red`, `.card-subtle`, plus `.card-compact`): faint tint, neutral hairline, 12px radius. Open each card with a bold lead phrase and a middle dot.
- **Code blocks:** fenced code with `filename="…"` renders a docs-style filename tab.
- **Terminal box** (`.terminal-box`, optional `data-title`): a hand-written prompt or transcript, using `.tk-prompt`, `.tk-muted`, and `.tk-ok` for colour.
- **Compare** (`.compare` with `.compare-head`, `.compare-weak`, `.compare-strong`): "instead of" versus "try" prompts.
- **Tiles** (`.tiles` with `.tile`, `.tile-heading`, `.tile-value`, `.tile-title`, `.tile-text`, `.tile-num`; four columns by default, `.tiles-3` or `.tiles-5` for three or five): short facts or numbered questions in a grid. `.tile-heading` is a prose heading; `.tile-value` is always mono, for a command or setting. `.tile-clay`, `.tile-green`, `.tile-blue`, and `.tile-amber` tint a tile.
- **Fill slides** (`.fill-tiles`, `.fill-compare` on the slide heading): stretch the slide's tiles or comparison to the full free height.
- **Link list** (`.link-list` of `.link-row` blocks): full-width rows with a linked title and a mono URL on the left, a muted description on the right, and a clay arrow. Only the title is a link, so the accessibility extension's underline marks just the title.
- **Closing slide** (`.closing` on the heading, with `.closing-icons`): centred title, line, and contact icons. `.closing-line` is a centred one-line card.
- **Retired** (`.retired` with `.retired-head` and `.retired-old`): outdated advice struck through beside the reason.
- **Source** (`.source`): the small centred citation line at the bottom of a slide.
- **Tables:** no fill; bold header with a stronger hairline, light row dividers.

## Do's and Don'ts

- **Do** use the classes above rather than inline styles, and keep new widgets in the same naming pattern.
- **Do** keep diagram text from restating the cards, and vice versa.
- **Don't** return to dark backgrounds or neon accents; the deck is light throughout.
- **Don't** hard-code hex colours in `index.qmd`.
- **Don't** give cards, callouts, blockquotes, or other text boxes coloured edges: no accent borders, left accent bars, or glows. Diagram boxes are the exception, because the docs' own diagrams use a thin accent outline.
- **Don't** copy Anthropic logos or wordmarks.
