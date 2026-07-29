# Verification — Character-for-Character Accuracy

Systematic verification of every converted file against the source PDF
(`Amtgard Rules of Play.pdf`, V8.7). Reproducible via the scripts noted below.

**The source PDF is not tracked in this repo** — it is the copyrighted rulebook, and `LICENSE`
limits who may reproduce it. The scripts resolve it relative to the repo root, so to re-run any
of them place your own copy of the V8.7 rulebook at `<repo root>/Amtgard Rules of Play.pdf`
(it is listed in `.gitignore`). Everything below was produced against that file.

## Result: PASS

- **180 ability files** — token-for-token identical to source field text; class availability
  correct on all 180; the four magic-user spell tables reconcile in both directions.
- **31 prose/class files** — no dropped rules, no altered numbers, no hallucinated content.
  Every residual difference is an intentional transformation (see "Explained differences").

## Method (all in `scripts/`)

1. **`verify_abilities.py`** — four independent checks, non-zero exit if any fails:

   a. **Body text.** For each of the 180 abilities, re-extract its raw source stat block
      (column-cropped) and compare token by token against the rule text actually written in
      the `.md` — including list items, not just `**Label:**` lines. Source lines are rejoined
      with the generator's own rule so a token the PDF wrapped mid-word (`Meta-` / `Magics`)
      is compared as the single token it really is.
   b. **Availability.** Each file's `class_availability` frontmatter *and* its
      **Available to:** line compared against the class codes on the source header line.
   c. **Completeness, both directions.** Every spell in the four magic-user spell tables maps
      to an ability file claiming that class at that level, *and* every class/level an ability
      file claims appears in that class's table. Levels are compared as sets, because a class
      may list the same ability at two levels (Bard buys *Equipment: Armor, 1 Point* at both
      2 and 6 — 43 table rows across 42 distinct names).
   d. **Count reconciliation.** 181 `T:` type-lines on PDF pp. 62–78 − 1 format-key line = 180
      abilities = 180 blocks parsed = 180 files on disk.

   **Current output:** `180/180` body text identical · `180/180` availability correct ·
   tables complete both ways (Bard 43, Druid 50, Healer 50, Wizard 52) · counts reconcile ·
   **0 failures**.

2. **`verify_prose.py`** — for each prose/class file, extracts the full source pages
   (tables intact) and compares token **multisets** (order- and table-independent):
   *coverage* = fraction of source tokens present in the md; *omitted spans* = consecutive
   source tokens absent from the md; *extra tokens* = md tokens absent from source.
   A follow-up pass isolates risky tokens (numbers, measurements, negations).
   31 files, mean coverage 0.941; every gap is accounted for below.

## Scope note — what these scripts do and do not catch

Verification is token/character level: it catches omissions, additions, altered numbers, and
dropped negations across 100% of the converted files.

It does **not** catch, on its own:

- **Meaning-preserving paraphrase.** The ability files are provably identical to source, and
  the prose files show no extra content phrases indicating rewording.
- **Content the source has but the conversion never claimed.** A page nobody assigned to a
  file is invisible to a per-file comparison — see the p. 2 gap below.
- **Non-rule text that leaked *into* a rule field.** Check 1a compares the md against the same
  extraction the generator consumed, so anything wrongly swallowed by both sides cancels out.
  This is a real blind spot and it hid a real defect; see below.

A full cross-review against the PDF, covering exactly what these scripts cannot, is in
[`CROSS-REVIEW.md`](CROSS-REVIEW.md).

## Bugs found and fixed

1. **`marauder.md`** — the source has a stray leading `.` on the effect line
   (`.    E: Gain Momentum…`, a PDF text-layer artifact). The parser didn't recognize `E:` as
   a field start and merged the Effect into the School value. Fixed by hardening the field
   parser to tolerate leading stray punctuation before a field label.

2. **Page-foot flavor swallowed into rule fields (6 files).** `pdftotext` continues past the
   last stat block in a column, so the book's in-world vignettes and "Did you Know?" sidebars
   were appended to whatever field ended the column — in `destroy-armor.md`,
   `elemental-barrage.md`, `rogue.md`, `vampirism.md`, `warlock.md` and `wounding.md`, some of
   it truncated mid-word. Check 1a could not see this (both sides had it). Fixed structurally
   in `gen_abilities.py::_body_end`, which now ends a block at either:
   - a **column boundary** — a stat block is typeset inside one column and never continues
     into another (exactly one ability tripped this: the p. 73 "Discovering Answers" vignette
     opening the right column after Rogue); or
   - a **layout gap** — a run of ≥2 blank lines followed by more text. A blank run that ends
     at a running header or date stamp is a page break, not a boundary, and does not cut: the
     sentence resumes right after it.

3. **PDF p. 2 was never converted.** The "This Rulebook Made Easy" box (seven numbered
   rules-interpretation principles) and the "Flavor Text in this Book" note sit on an
   unnumbered front-matter page that no file claimed, so no check ever looked at it. Now
   converted as [`rules/this-rulebook-made-easy.md`](rules/this-rulebook-made-easy.md)
   (coverage 1.000, 0 omitted spans, 0 extra tokens).

4. **`gen_indexes.py` indexed its own output.** `INDEX.md` listed itself as a 181st ability
   with a blank name, which propagated a wrong count ("all 181 abilities") into both
   `INDEX.md` and `README.md`. The index was also ordered by filename slug rather than
   ability name, putting *Poison Glands* before *Poison*. Both fixed and regenerated.

## Page coverage

Every PDF page carrying rules content is claimed by some file: p. 2 (front matter) and
pp. 4–86, plus pp. 88–96. Intentionally omitted: p. 1 (cover), p. 3 (table of contents,
credits, copyright), and p. 87 — the book's printed Index, a page-number index of the print
edition superseded by `README.md` and `rules/magic-and-abilities/INDEX.md`.

## Explained differences (not errors)

- **Flavor text** — every omitted span ≥3 tokens in the prose files is an in-world
  vignette/quote the project intentionally excludes (Makros journal, Megiddo quote, Jack the
  Scholar, Lazarus Scholar, etc.).
- **Small-caps / tokenization artifacts** — source small-caps headings extract as e.g.
  `R ating`; `Cloth/ Padded` vs `Cloth/Padded`; `strike legal` vs `Strike-Legal`. The md is
  the correct form. These also produce spurious "omitted spans" in the multiset diff, because
  a token present in a different form breaks an otherwise-consecutive run.
- **Two-column tables** — in `weapon-types-shields-equipment.md` (coverage 0.902) the
  full-page source extraction interleaves columns, so runs of source tokens are not
  consecutive in the md even though every token is present. The reported spans are
  reading-order artifacts, not dropped rules.
- **Content relocation** — the "Other Equipment" block (Sashes/Class Symbols/Strips) prints on
  PDF p. 21 but is placed in `weapon-types-shields-equipment.md` rather than
  `equipment-checking.md`, which is why the latter reads 0.538 alone. Combined coverage of
  PDF pp. 16–21 across the two files is 0.989 with **zero** omitted runs — content preserved,
  only the file boundary differs from the page boundary.

## Open judgment calls (content intentionally not carried over)

1. **Arrow-diagram figure legend** (weapon-types) — the illustration caption
   `(A) 2" diameter … (E) 1" Blunt (F) Minimal flat striking surface` was omitted as a picture
   caption. All the actual construction rules are present. Restore as a note if desired.
2. **Monster flavor framing** (classes overview) — the descriptive line
   "…the smallest, friendliest sprite, the largest most fearsome dragon… Examples: Centaurs,
   Dragons, Dwarves, Werewolves, Vampires, Deadly Slime." was dropped as flavor; all Monster
   *rules* are kept.
3. **`circle-of-protection.md`** — the two sentences the book sets after the "All targets:"
   list share the indentation of the preceding list item's wrapped lines, so no rule can
   separate them automatically; they render inside the final bullet. No text is lost.
