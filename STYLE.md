# Conversion Style Guide — Amtgard Rules of Play → Markdown

Source: `Amtgard Rules of Play.pdf` (Version 8, V8.7 "Soupy", dated 2025-07-26).
Goal: faithful, actionable markdown rules files that can be programmatically acted upon later.

## Decisions (locked)
1. **Exclude flavor text.** The rulebook contains in-world stories and italic quotes it
   explicitly marks as "not rules" (e.g. journal entries, character quotes with an em-dash
   attribution, section-break vignettes like *"On the Nature of Death in the World of Amtgard"*).
   Do **not** include these. They are decorative.
2. **Verbatim, restructured.** Preserve the exact rules wording. Do not paraphrase, summarize,
   or "improve" the language. You may only re-flow it into clean markdown structure
   (headings, lists, tables). Every rule sentence in the source must appear in the output.
3. **Split big sections.** One file per logical unit (per class, per ability group, etc.).

## "Made Easy" callouts
The book has "…Made Easy" boxes (pedagogical summaries with the Clippy mascot). These are NOT
flavor text — keep them, but render as a labeled blockquote at the point they appear:

```
> **Made Easy**
>
> <verbatim text of the Made Easy box>
```

## Source extraction (the PDF has a real text layer — no OCR needed)
For your assigned PDF page range `A`–`B`, run BOTH:

```bash
# Place your own copy of the V8.7 rulebook here; it is gitignored, not distributed.
PDF="$(git rev-parse --show-toplevel)/Amtgard Rules of Play.pdf"
pdftotext -layout -f A -l B "$PDF" -   # PRIMARY: preserves columns & tables spatially
pdftotext        -f A -l B "$PDF" -   # secondary cross-check for wording only
```

For the two-column stat-block sections, crop each column separately so reading order is
exact (the page is 612pt wide, so each column is 306pt):

```bash
pdftotext -layout -x 0   -W 306 -f A -l B "$PDF" -   # LEFT column
pdftotext -layout -x 306 -W 306 -f A -l B "$PDF" -   # RIGHT column
```

**The layout is two-column.** In the `-layout` output the LEFT and RIGHT columns sit
side-by-side on the same lines, separated by a wide run of spaces (a visual gutter).
You MUST read the **entire left column top-to-bottom first, then the entire right column.**
Do not read across the gutter. The no-layout output often scrambles multi-column reading
order, so use it only to confirm exact wording, never for sequence.

Ignore page furniture that is not rules content: running headers/footers like
`Amtgard 8 - <Section>`, the date stamp `07-26-2025`, and bare page numbers.

## Frontmatter (every file)
```yaml
---
title: <Human title>
section: <Table-of-Contents section name>
printed_pages: <e.g. 6-8>
pdf_pages: <e.g. 9-11>
rulebook_version: V8.7 "Soupy"
rulebook_date: 2025-07-26
source: Amtgard Rules of Play Version 8
---
```

## Formatting conventions
- `#` H1 = the file's title (matches frontmatter `title`).
- `##` / `###` for subsections, following the book's own heading hierarchy.
- Preserve the book's numbered lists as ordered lists and lettered sub-points as nested lists.
- Bold the inline "lead-in" labels the book bolds/italicizes, e.g. **Arm:**, **Slash:**,
  **Allowed:**, **Disallowed:**.
- Convert genuine tabular data (stat blocks, weapon length tables, spell-point lists) into
  markdown tables. Keep column headers verbatim.
- Preserve special terms' capitalization exactly (Strike-Legal, Enchantment, Magic Ball,
  Refresh, Incantation, Trait, etc.).
- Straight-quote normalization is fine (curly → straight) but do not change wording.
- End every file with a `---` rule followed by a one-line source note. Use the plural form
  for a range and the singular for a single page — never a degenerate range (`pp. 1–1`):
  - range: `*Source: Amtgard Rules of Play V8.7, printed pp. X–Y (PDF pp. A–B). Flavor text omitted.*`
  - single: `*Source: Amtgard Rules of Play V8.7, printed p. X (PDF p. A). Flavor text omitted.*`

  This one template covers every file in `rules/`, including the 180 generated ability
  files. The only exception is unnumbered front matter (PDF p. 2), which has no printed
  page number and so names the PDF page alone.

## Ability stat-block format (Classes & Magic and Abilities sections)
Abilities are printed as compact stat blocks, e.g.:
`Flame Blade  T: Enchantment  S: Flame  R: Self  I: "…" x3  ...`
Render each ability as a `###` heading (the ability name), followed by a definition-style
list of its fields (Type `T`, School `S`, Range `R`, Incantation `I`, Effect `E`, etc.)
exactly as labeled, then the prose description. Preserve the `xN` incantation-repeat counts.

Where a field's value contains a list the book sets as indented items (a `…:` lead-in
followed by `1.` `2.` `3.` or `-` entries), render it as a real markdown ordered or
bulleted list rather than inlining it into the paragraph. Any sentence the book sets flush
after the list belongs outside it, as a following paragraph.

The book's literal placeholders — `<Player>`, `<armor location>`, `<object name>` — must be
wrapped in backticks so markdown renderers do not swallow them as HTML tags.

See `rules/combat-rules.md` for a worked exemplar of all the above.
