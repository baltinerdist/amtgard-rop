# Verification — Character-for-Character Accuracy

Systematic verification of every converted file against the source PDF
(`Amtgard Rules of Play.pdf`, V8.7). Reproducible via the scripts noted below.

## Result: PASS

- **180 ability files** — token-for-token identical to source; **1 real bug found and fixed** (see below).
- **30 prose/class files** — no dropped rules, no altered numbers, no hallucinated content.
  Every residual difference is an intentional transformation (see "Explained differences").

## Method (all in `scripts/`)

1. **`verify_abilities.py`** — for each of the 180 abilities, re-extracts its raw source
   stat block (column-cropped) and compares, token by token, against the rendered field
   values in the written `.md`. Also cross-checks each file's `class_availability` against
   the uncropped source header line.
   - Independent completeness check: every spell in all four magic-user tables
     (Bard 43, Druid 51, Healer 51, Wizard 53) maps to a file with the correct class.
   - Count reconciliation: 181 `T:` type-lines − 1 format-key line = 180 abilities.
   - **Result: 180/180 body text identical; 180/180 availability correct.**

2. **`verify_prose.py`** — for each prose/class file, extracts the full source pages
   (tables intact) and compares token **multisets** (order- and table-independent):
   - *coverage* = fraction of source tokens present in the md,
   - *omitted spans* = consecutive source tokens absent from the md,
   - *extra tokens* = md tokens absent from source.
   - A follow-up pass isolates risky tokens (numbers, measurements, negations).

## The one real bug (fixed)

**`marauder.md`** — the source has a stray leading `.` on the effect line
(`.    E: Gain Momentum…`, a PDF text-layer artifact). The parser didn't recognize `E:` as
a field start and merged the Effect into the School value. Fixed by hardening the field
parser (`gen_abilities.py`) to tolerate leading stray punctuation before a field label;
regenerated; re-verified 180/180 clean.

## Explained differences (not errors)

- **Flavor text** — every omitted span ≥3 tokens is an in-world vignette/quote the project
  intentionally excludes (Makros journal, Megiddo quote, Jack the Scholar, Lazarus Scholar, etc.).
- **Label expansion** — ability stat blocks render `T:/S:/R:/I:/M:/E:/L:/N:` as
  `Type:/School:/Range:/…`; the single-letter source tokens vs expanded md words account for
  the martial-class coverage gap (no dropped content).
- **Small-caps / tokenization artifacts** — source small-caps headings extract as e.g.
  `R ating`; `Cloth/ Padded` vs `Cloth/Padded`. The md is the correct form.
- **Content relocation** — the "Other Equipment" block (Sashes/Class Symbols/Strips) prints on
  PDF p.21 but was placed in `weapon-types-shields-equipment.md` rather than
  `equipment-checking.md`. Combined coverage of PDF pp.16–21 across the two files is 0.989
  with **zero** omitted runs — content preserved, only the file boundary differs from the page boundary.

## Open judgment calls (content intentionally not carried over)

1. **Arrow-diagram figure legend** (weapon-types) — the illustration caption
   `(A) 2" diameter … (E) 1" Blunt (F) Minimal flat striking surface` was omitted as a picture
   caption. All the actual construction rules are present. Restore as a note if desired.
2. **Monster flavor framing** (classes overview) — the descriptive line
   "…the smallest, friendliest sprite, the largest most fearsome dragon… Examples: Centaurs,
   Dragons, Dwarves, Werewolves, Vampires, Deadly Slime." was dropped as flavor; all Monster
   *rules* are kept.

## Scope note

Verification is token/character level: it catches omissions, additions, altered numbers, and
dropped negations across 100% of files. It does not, on its own, catch meaning-preserving
paraphrase — but the ability files are provably identical to source, and the prose files show
no extra content phrases indicating rewording.
