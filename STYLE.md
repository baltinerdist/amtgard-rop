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
PDF="/Users/averykrouse/Downloads/Amtgard Rules of Play.pdf"
pdftotext -layout -f A -l B "$PDF" -   # PRIMARY: preserves columns & tables spatially
pdftotext        -f A -l B "$PDF" -   # secondary cross-check for wording only
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
- End every file with a `---` rule followed by a one-line source note:
  `*Source: Amtgard Rules of Play V8.7, printed pp. X–Y (PDF pp. A–B). Flavor text omitted.*`

## Ability stat-block format (Classes & Magic and Abilities sections)
Abilities are printed as compact stat blocks, e.g.:
`Flame Blade  T: Enchantment  S: Flame  R: Self  I: "…" x3  ...`
Render each ability as a `###` heading (the ability name), followed by a definition-style
list of its fields (Type `T`, School `S`, Range `R`, Incantation `I`, Effect `E`, etc.)
exactly as labeled, then the prose description. Preserve the `xN` incantation-repeat counts.

See `rules/combat-rules.md` for a worked exemplar of all the above.
