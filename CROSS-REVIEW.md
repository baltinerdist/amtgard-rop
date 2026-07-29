# Cross-Review: Amtgard Rules of Play V8.7 markdown conversion vs. source PDF

*Systematic, sharded review of every file under `rules/` (plus `README.md`, `STYLE.md`,
`VERIFICATION.md`) against `Amtgard Rules of Play.pdf`. Every finding below was independently
re-verified by a second reviewer who re-read both the PDF page and the markdown file.*

---

## Resolution status: all 35 findings addressed

Findings 1–35 have been fixed. The defects that lived in generated files were fixed in the
generators (`scripts/gen_abilities.py`, `scripts/gen_indexes.py`) and the files regenerated, so
they cannot come back on the next run:

- **Pattern A** (#2, #3, #5–#8) — `gen_abilities.py::_body_end` now ends a stat block at a
  column boundary or a genuine layout gap, distinguishing the latter from a running-header
  break. **Pattern B** (#29), **C** (#20, #22, #24–#27), **D** (#19, #23, #28) and #4, #21 are
  likewise fixed in the generator, not by hand-editing the 180 outputs.
- **Pattern E** (#14–#16, #34) — one generator bug; `INDEX.md` no longer indexes itself, counts
  read 180, and abilities sort by name.
- **#1** — PDF p. 2 is now converted as `rules/this-rulebook-made-easy.md` (coverage 1.000).
- **Patterns F/G** (#10, #12, #17, #18, #30–#33, #35) — one source-note convention, documented
  in `STYLE.md`; `VERIFICATION.md` rewritten to match what the scripts actually do; the three
  hardcoded `~/Downloads` paths now resolve to the in-repo PDF.
- `scripts/verify_abilities.py` now implements the availability, completeness and count checks
  that `VERIFICATION.md` previously only claimed, and `scripts/lint_corpus.py` was added to
  hold the Pattern F conventions in place.

Two items resolved with a judgment call rather than a mechanical fix, both recorded in
`VERIFICATION.md`: **#12** takes the book's own page heading (`&`) as the title while `section:`
keeps the Table-of-Contents form (`and`); **#22**'s trailing sentences stay inside the final
bullet, because the source gives them the same indentation as that bullet's wrapped lines and
nothing distinguishes them automatically. No text is lost in either case.

Verified after the fixes: `verify_abilities.py` 180/180 body text, 180/180 availability, spell
tables complete both ways, 0 failures · `lint_corpus.py` 213 files, 93 PDF pages claimed,
0 problems · `verify_prose.py` unchanged apart from `armor.md` rising to 0.997 coverage.

The findings below are retained as the record of what was found and why.

---

## Verdict

The conversion is in good shape. Rule text is overwhelmingly verbatim and correctly attributed:
the 180 ability stat blocks match the PDF token-for-token in their field text, the +3 printed→PDF
page offset holds throughout, and no finding in this review reports a *changed* rule, a wrong
number inside a rule, or a silently dropped ability. The defects are almost entirely at the seams
— two-column gutter merges at page bottoms, PDF line-wrap artifacts, list structure flattened into
run-on paragraphs, and bookkeeping drift in the generated index/README/VERIFICATION metadata.

**35 distinct defects** (merged down from 47 verified reports; 12 were the same defect found by two
shards): **8 major, 10 minor, 17 cosmetic**. Nothing is critical.

The one substantive content gap is that PDF p.2 — the "This Rulebook Made Easy" box, seven numbered
rules-interpretation principles, plus the "Flavor Text in this Book" note — was never converted; it
appears in no file in the repo. Everything else is presentation, metadata, or excluded flavor text
that leaked *into* rule fields rather than rule text that leaked out.

The 8 major findings share a single root cause worth fixing first: at the bottom of six PDF pages,
`pdftotext` merged an excluded flavor vignette or sidebar into whatever rule field ended the
column, so mid-word-truncated in-world fiction is currently presented as mechanical rule text in
`destroy-armor.md`, `elemental-barrage.md`, `rogue.md`, `vampirism.md`, `warlock.md`, and
`wounding.md`. These are one-line truncations each.

---

## Summary: severity × category

| Category | Major | Minor | Cosmetic | **Total** |
| --- | ---: | ---: | ---: | ---: |
| artifact (PDF extraction / layout damage) | 6 | 3 | 13 | **22** |
| frontmatter / source-note metadata | 0 | 2 | 3 | **5** |
| alteration (wrong count or figure in repo docs) | 0 | 3 | 0 | **3** |
| omission (source content absent) | 1 | 1 | 0 | **2** |
| mislabeling (field or title mismatch) | 1 | 0 | 1 | **2** |
| extra-content (unsupported claim) | 0 | 1 | 0 | **1** |
| **Total** | **8** | **10** | **17** | **35** |

Severity key: **major** = non-rule text presented as rule text, or source rules content missing;
**minor** = wrong metadata, wrong count, or structure that changes how a rule reads;
**cosmetic** = spacing, list markup, escaping, or convention drift with no effect on meaning.

---

## Findings

### Critical

None.

---

### Major (8)

#### 1. PDF p.2 "This Rulebook Made Easy" + "Flavor Text in this Book" are missing from the repo

- **File:** *(no file — repo-wide coverage gap; filed against `/Users/averykrouse/GitHub/amtgard-rop/rules/introduction.md` and `/Users/averykrouse/GitHub/amtgard-rop/VERIFICATION.md`)*
- **Location:** unnumbered front matter, between the cover and the Table of Contents
- **PDF page:** 2
- **Category:** omission
- **What is wrong:** PDF p.2 carries seven numbered rules-application principles (including
  "Abilities only do explicitly what they say they do" and the no-gray-areas rule) and the
  "Flavor Text in this Book" note. No file in the repo contains any of it, and no file's
  `pdf_pages` frontmatter covers page 2. `grep -rn "gray areas\|Clippy\|play fair" rules/` returns
  nothing. STYLE.md mandates that "Made Easy" boxes be kept as `> **Made Easy**` blockquotes, and
  four other such boxes *are* kept. VERIFICATION.md's `## Result: PASS` / `## Scope note`
  ("across 100% of files") therefore overstates coverage. The audit premise that "PDF pp.1–3 are
  cover / credits / TOC" is false for p.2: p.1 is only the version stamp and p.3 is TOC + credits +
  copyright, but p.2 is substantive rules-interpretation guidance.

**Source:**

```
                       This Rulebook Made Easy
Rulebooks are confusing things. They are often written by people who know what they
are trying to accomplish but written for people who have no idea of the writers' goals.
[...]
4. Abilities only do explicitly what they say they do, and do not have additional powers beyond what is explicitly stated within the rules.
5. Read the rules in their entire context. [...]
6. Don't play in the gray areas of the rules. Gray areas and loopholes will not be considered or accepted
by reeves.
7. If a term is not defined in this rulebook, the commonly accepted definition of the term should be applied. [...]

Flavor Text in this Book
This rulebook also contains stories and quotes that provide historical tidbits and suggestions for how our game mechanics might be explained through role-play. These bits of flavor text are not rules and should not be used to justify rule interpretations.
```

**Markdown:** `<absent>`

**Suggested fix:** Add a file (e.g. `rules/this-rulebook-made-easy.md`, `pdf_page: 2`, no printed
page) containing the "This Rulebook Made Easy" box as a `> **Made Easy**` blockquote plus the
"Flavor Text in this Book" paragraph, and note the front-matter pages in VERIFICATION.md's scope.
(Union of all `pdf_page(s)` values leaves pp. 1, 2, 3, 87 uncovered; 1, 3 and the omitted Index at
87 are intentional — only p.2 is a real gap.)

---

#### 2. `rules/magic-and-abilities/destroy-armor.md` — flavor vignette merged into **Note:**

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/destroy-armor.md`
- **Location:** `**Note:**` field, end of line (line 26)
- **PDF page:** 65
- **Category:** artifact
- **What is wrong:** Gutter-clipped remnants of the intentionally-omitted page-foot flavor vignette
  (the in-world date stamp "E.P. 31, 90th" plus three mid-word-truncated lines of the Lotus
  Brighthawk quote) are appended to the Note as if they were rule text. The captured text is only
  the left-of-gutter half of each line and breaks mid-word at "do I hav".

**Source:**

```
                                     E.P. 31, 90th of Marching
      A sharp sword and a strong arm? What need do I have of these things? I command the very power of the
      planes. With a word I can summon fire and storms, kill you, or send your body to the Aether. I have no
      need of steel for I can take your immortal soul.
                                                                                      - Lotus Brighthawk, Archmage
```

**Markdown:**

```
cannot protect against Destroy Armor.     E.P. 31, 90th A sharp sword and a strong arm? What need do I hav planes. With a word I can summon fire and storms, need of steel for I can take your immortal soul.
```

**Suggested fix:** Truncate the Note at "...and thus cannot protect against Destroy Armor." and
delete everything from `     E.P. 31, 90th` onward.

---

#### 3. `rules/magic-and-abilities/elemental-barrage.md` — flavor vignette merged into **Note:**

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/elemental-barrage.md`
- **Location:** `**Note:**` field, end of line (line 28)
- **PDF page:** 65
- **Category:** artifact
- **What is wrong:** The complementary right-of-gutter half of the same p.65 vignette — including
  the fragment "th of Marching" and the attribution "- Lotus Brighthawk, Archmage" — is appended to
  the Note as if it were rule text.

**Source:**

```
th of Marching

ve of these things? I command the very power of the
 kill you, or send your body to the Aether. I have no

                       - Lotus Brighthawk, Archmage
```

**Markdown:**

```
**Note:** The effect is not an incantation, and so is not stopped by being Suppressed, and may be used while moving, etc.     th of Marching  ve of these things? I command the very power of the kill you, or send your body to the Aether. I have no  - Lotus Brighthawk, Archmage
```

**Suggested fix:** Truncate the Note at "...and may be used while moving, etc." and delete
everything from `     th of Marching` onward.

---

#### 4. `rules/magic-and-abilities/gift-of-air.md` — Note field folded into Limitations with a leaked `N:` label

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/gift-of-air.md`
- **Location:** `**Limitations:**` line
- **PDF page:** 67
- **Category:** mislabeling
- **What is wrong:** The source's separate `N:` (Note) field is concatenated into
  `**Limitations:**` with the raw `N:` token left inline, instead of being expanded into its own
  `**Note:**` field as every other ability file does. Permissive Note text now reads as a
  limitation.

**Source:**

```
  L: Bearer may not wield weapons or Shields.
  N:If the Insubstantial State is ended, the player is not
  required to continue returning to base. Bearer may end this
  Insubstantial State at any time by using the exit incantation
  for Insubstantial.
```

**Markdown:**

```
**Limitations:** Bearer may not wield weapons or Shields. N:If the Insubstantial State is ended, the player is not required to continue returning to base. Bearer may end this Insubstantial State at any time by using the exit incantation for Insubstantial.
```

**Suggested fix:** Split into two fields — `**Limitations:** Bearer may not wield weapons or
Shields.` and a separate `**Note:** If the Insubstantial State is ended, ...` — dropping the stray
`N:` token (the source has no space after `N:`).

---

#### 5. `rules/magic-and-abilities/rogue.md` — "Discovering Answers" vignette merged into **Limitations:**

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/rogue.md`
- **Location:** `**Limitations:**` field
- **PDF page:** 73
- **Category:** artifact
- **What is wrong:** The entire "Discovering Answers" flavor vignette — title, four paragraphs, and
  the "-Sir Render of the Mirage Mountains" attribution — is appended to Rogue's Limitations. In the
  PDF that vignette occupies the right column of p.73 and has no connection to Rogue, whose
  Limitations line ends at "May not wield Bows nor Long weapons." Roughly 80 words of
  excluded-by-policy flavor text are presented as part of a rule field.

**Source:**

```
Rogue                                                   As 6
 T: Archetype S: Neutral
 E: Regain a use of Coup de Grace upon killing a player with
 a thrown weapon.
 L: May not wield Bows nor Long weapons.
```

**Markdown:**

```
**Limitations:** May not wield Bows nor Long weapons. Discovering Answers In all my travels shifting through the plains and marching through the realms I found that few frustrations were constant.  One is foes with thickened skin or divine blessings that prevent blades from striking true.  I come to you with an answer from origins I could not say, for the memory was lost to me. But this ritual should work, even outside of the vanishing kingdom.  -Sir Render of the Mirage Mountains
```

**Suggested fix:** Truncate the field to `**Limitations:** May not wield Bows nor Long weapons.`
Cross-check: `rules/classes/assassin.md`'s inline Rogue block correctly stops at the limitation.

---

#### 6. `rules/magic-and-abilities/vampirism.md` — "Did you Know?" sidebar merged into **Effect:**

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/vampirism.md`
- **Location:** `**Effect:**` field
- **PDF page:** 77
- **Category:** artifact
- **What is wrong:** The page's "Did you Know?" sidebar (title plus all four sentences of Burning
  Lands / Royal Amtgard Navy flavor) was swept into the `**Effect:**` field, appended after
  "...work through their Cursed State." on the same line, so non-rule flavor text is presented as
  part of the ability's mechanical effect.

**Source:**

```
E: Player gains Adrenaline Unlimited (ex), is Immune to
Death, and is Cursed. Bearer's Adrenaline ability will work
through their Cursed State.

             Did you Know?

  Vampires have been illegal in the Kingdom of the
  Burning Lands ever since the infamous Edict of
  Ben's Living Room was passed over two decades
  ago.
  The task of hunting down and destroying these
  undead creatures has been the responsibility of
  the Royal Amtgard Navy. Fortunately for the
  undead, the RAN is rather lax and easily bribed.
```

**Markdown:**

```
**Effect:** Player gains Adrenaline Unlimited (ex), is Immune to Death, and is Cursed. Bearer's Adrenaline ability will work through their Cursed State.     Did you Know?     Vampires have been illegal in the Kingdom of the Burning Lands ever since the infamous Edict of Ben's Living Room was passed over two decades ago. The task of hunting down and destroying these undead creatures has been the responsibility of the Royal Amtgard Navy. Fortunately for the undead, the RAN is rather lax and easily bribed.
```

**Suggested fix:** Truncate the Effect at "...will work through their Cursed State." and drop the
"Did you Know?" sidebar (flavor, excluded per STYLE.md), or render it as a separate blockquote
outside the stat block.

---

#### 7. `rules/magic-and-abilities/warlock.md` — left half of the p.78 vignette merged into **Limitations:**

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/warlock.md`
- **Location:** `**Limitations:**` field (line 22)
- **PDF page:** 78
- **Category:** artifact
- **What is wrong:** The left-of-gutter half of the excluded page-bottom flavor vignette "Studying
  the Archives of the Schools" leaked into the Limitations field, appending roughly nine
  mid-word-truncated flavor fragments after the otherwise-verbatim limitation text.

**Source:**

```
L: Player may not purchase Verbals from any School other
than the Death and Flame Schools.

                                          Studying the Archives of the Schools

Amtgard 8 - Magic and Abilities
                                                    In times past, scholars taught about the Schools of Magic. Back then, they believed that similar effects would
```

**Markdown:**

```
**Limitations:** Player may not purchase Verbals from any School other than the Death and Flame Schools.     Studying the A     In times past, scholars taught about the School commonly fall under the same School, or that yo are likely to find yourself Suppressed by Comman the Protection School! Death may be used to wo mad with fear, or to even bring power and prote   It is better to see the Schools as weights on the sca into a specific School because of the effects it cau be due to some esoteric concept of Balance that
```

**Suggested fix:** Truncate the Limitations at "...than the Death and Flame Schools." and delete
everything from `     Studying the A` onward.

---

#### 8. `rules/magic-and-abilities/wounding.md` — right half of the p.78 vignette merged into **Note:**

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/wounding.md`
- **Location:** `**Note:**` field (line 26)
- **PDF page:** 78
- **Category:** artifact
- **What is wrong:** The complementary right-of-gutter half of the same "Studying the Archives of
  the Schools" vignette, including the "- Dantalion the Wizard" attribution, leaked into the Note
  field as mid-word fragments.

**Source:**

```
N: Wounding targets the player but affects the Hit Location.
Visibility can be drawn to any part of the player, not just the
desired Hit Location.

                                          Studying the Archives of the Schools
...
                                                                                                                                                 - Dantalion the Wizard
```

**Markdown:**

```
**Note:** Wounding targets the player but affects the Hit Location. Visibility can be drawn to any part of the player, not just the desired Hit Location.     Archives of the Schools ls of Magic. Back then, they believed that similar effects would ou could find some form of common trends. Utter hogwash! You nd, Death, Sorcery, Subdual, or until recent advancements, even ound or kill, yes, but also to chip away at armor and drive a foe mad with fear, or to even bring power and protection   ale of order in the Universe. Do not try to assume something falls uses, but because the Universe has decided that is where it should often escapes even the most wizened of scholars. - Dantalion the Wizard
```

**Suggested fix:** Truncate the Note at "...not just the desired Hit Location." and delete
everything from `     Archives of the Schools` onward.

---

### Minor (10)

#### 9. `rules/armor.md` — tier table drops the "Special / Ambiguous Armor" row

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/armor.md`
- **Location:** `## Armor Types and Modifiers` — Tier / Maximum Points / Armor Types table (last row)
- **PDF page:** 13 (printed p.10)
- **Category:** omission
- **What is wrong:** The table omits the source's final row, "Special" (Maximum Points cell blank) /
  "Ambiguous Armor". The accompanying Ambiguous Armor rule text is present elsewhere in the file, so
  only the row's tier classification is lost.

**Source:**

```
           Tier                     Maximum Points                                 Armor Types
            1                                2                                     Cloth/Padded
            2                                3                            Light Leather, Flexible Synthetic
            3                                4                     Heavy Leather, Butcher's Mail, Rigid Synthetic
            4                                5                                 Light Scale, Chainmail
            5                                6                      Heavy Scale, Butted Plate (Splint, Kikko, etc)
            6                                7                          Lamellar, Laminar, Brigandine, Plate

         Special                                                                 Ambiguous Armor
```

**Markdown:**

```
| Tier | Maximum Points | Armor Types |
| --- | --- | --- |
| 1 | 2 | Cloth/Padded |
...
| 6 | 7 | Lamellar, Laminar, Brigandine, Plate |
```

**Suggested fix:** Append `| Special |  | Ambiguous Armor |` (Maximum Points cell is blank in the
source).

---

#### 10. `rules/weapon-types-shields-equipment.md` — frontmatter page range contradicts its own footer

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/weapon-types-shields-equipment.md`
- **Location:** YAML frontmatter (lines 4–5) vs. the trailing source note (line 314)
- **PDF page:** 21
- **Category:** frontmatter
- **What is wrong:** Frontmatter says `printed_pages: 13-17` / `pdf_pages: 16-20`, undercounting by
  one page and contradicting the file's own footer, "printed pp. 13–18 (PDF pp. 16–21)". The file
  contains the full "Other Equipment" block (Sashes / Class Symbols / Strips, md lines 284–311),
  which prints on printed p.18 / PDF p.21. The footer is correct.

**Source:**

```
Other Equipment
Sashes
Sashes are used to denote certain classes by their color in
games where classes are used. All sashes must be at least
2” wide and be worn from shoulder to opposite hip across
the body.
```

**Markdown:**

```
printed_pages: 13-17
pdf_pages: 16-20
[...]
*Source: Amtgard Rules of Play V8.7, printed pp. 13–18 (PDF pp. 16–21). Flavor text omitted.*
```

**Suggested fix:** Change frontmatter to `printed_pages: 13-18` / `pdf_pages: 16-21`. (The
intentional overlap with `equipment-checking.md` on PDF p.21 is documented and fine.)

---

#### 11. `rules/classes/paladin.md` — one either/or archetype choice split into two rows

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/classes/paladin.md`
- **Location:** "Paladin Abilities By Level" table — 6th level rows
- **PDF page:** 48
- **Category:** artifact
- **What is wrong:** The single source header "Optional – Pick one:" is duplicated into two separate
  6th-level rows (one per archetype), inserting a line that appears only once in the PDF and blurring
  that Guardian and Inquisitor are one mutually exclusive choice. Inconsistent with
  `monk.md` / `anti-paladin.md` / `scout.md`, which keep one header and list both archetypes in a
  single cell. (The same file also splits the 1st-level traits over two rows both labelled "1st".)

**Source:**

```
6th    Protection from Magic (Touch) 2/Refresh (m)
       Optional – Pick one:
       Guardian (A)
       Inquisitor (A)
```

**Markdown:**

```
| 6th | Protection from Magic (Touch) 2/Refresh (m) |
| 6th | Optional – Pick one: Guardian (A) |
| 6th | Optional – Pick one: Inquisitor (A) |
```

**Suggested fix:** Collapse into one row using the `<br>` style the sibling files use:
`| 6th | Protection from Magic (Touch) 2/Refresh (m)<br>Optional – Pick one:<br>Guardian (A)<br>Inquisitor (A) |`
(matches `rules/classes/monk.md` line 36 and `rules/classes/anti-paladin.md` line 37).

---

#### 12. `rules/appendix-b-kingdom-boundaries.md` — H1 and frontmatter title disagree ("&" vs "and")

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/appendix-b-kingdom-boundaries.md`
- **Location:** frontmatter `title:` / `section:` vs. the H1 on line 11
- **PDF pages:** 86 (body heading) and 3 (Table of Contents)
- **Category:** frontmatter / mislabeling
- **What is wrong:** Frontmatter `title` and `section` read "…Kingdom Boundaries and Park
  Sponsorship" while the H1 reads "…Kingdom Boundaries & Park Sponsorship", violating STYLE.md's
  rule that the H1 match the frontmatter title. This is the only H1/title mismatch in the 212-file
  corpus. Both spellings are source-attested: PDF p.86's printed body heading uses "&" and the p.3
  Table of Contents uses "and", so the H1 is verbatim and only the internal consistency is at fault.
  Body text and page offsets (printed 83 / PDF 86) are correct.

**Source (p.86 body heading):**

```
Kingdom Boundaries                              s & Park Sponsorship
```

**Source (p.3 Table of Contents):**

```
                  Appendix B: Kingdom Boundaries and Park Sponsorship                                       83
```

**Markdown:**

```
title: "Appendix B: Kingdom Boundaries and Park Sponsorship"
section: "Appendix B: Kingdom Boundaries and Park Sponsorship"
[...]
# Appendix B: Kingdom Boundaries & Park Sponsorship
```

**Suggested fix:** Pick one form. Reviewers split on which: either set
`title: "Appendix B: Kingdom Boundaries & Park Sponsorship"` (page-heading form, keeping `section:`
as the TOC form), or change the H1 to `# Appendix B: Kingdom Boundaries and Park Sponsorship`.
Either resolves it; the page-heading form is the book's own heading.

---

#### 13. `rules/magic-and-abilities/_overview.md` is an unprocessed `pdftotext` dump

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/_overview.md`
- **Location:** whole file body (`# Magic and Abilities — Overview`)
- **PDF page:** 62 (printed p.59)
- **Category:** artifact
- **What is wrong:** PDF hard line-wraps are preserved verbatim; the section title is duplicated as
  body text under the H1; line 17 merges the two box headers across the gutter
  ("Abilities Format Key                Classes and Levels", the latter left with no content); the
  format key is unstructured; and the file lacks the mandated `---` + source-note footer.

**Source:**

```
Magic and Abilities
Abilities form the basis for class differentiation. In this
section is a listing of all the different abilities you might use
or encounter. Note: Traits are always on, and thus ignore any
incantation requirement listed in an ability.

Abilities Format Key                Classes and Levels
  T: Type S: School R: Range (if any)
  I: Incantation and gestures
  M: Materials needed
```

**Markdown:**

```
# Magic and Abilities — Overview
Magic and Abilities
Abilities form the basis for class differentiation. In this
section is a listing of all the different abilities you might use
or encounter. Note: Traits are always on, and thus ignore any
incantation requirement listed in an ability.
Abilities Format Key                Classes and Levels
T: Type S: School R: Range (if any)
I: Incantation and gestures
M: Materials needed
E: Effect
L: Limitations or Restrictions
N: Note

> **Note:** Individual abilities are in one file each in this directory.
```

**Suggested fix:** Re-flow the intro paragraph as continuous prose, drop the duplicated "Magic and
Abilities" line, split "Abilities Format Key" and "Classes and Levels" into their proper column
headings, render the format key as a list/table, and add the required `---` +
`*Source: Amtgard Rules of Play V8.7, printed p. 59 (PDF p. 62). Flavor text omitted.*` footer.

---

#### 14. `rules/magic-and-abilities/INDEX.md` lists itself as an ability

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/INDEX.md`
- **Location:** `## All Abilities (alphabetical)` — first table row (line 10)
- **PDF page:** 62
- **Category:** artifact
- **What is wrong:** `scripts/gen_indexes.py` globs `*.md` excluding only `_overview.md`, so
  INDEX.md enumerates itself as a 181st "ability": the alphabetical table's first data row has an
  empty name, an em-dash availability, and a self-link.

**Source (the row that *should* be first):**

```
Abeyance                                                   He 5
  T: Magic Ball S: Subdual
```

**Markdown:**

```
|  | — | [INDEX.md](INDEX.md) |
```

**Suggested fix:** Delete the row and fix the root cause — `scripts/gen_indexes.py` line 22 skips
only `_overview.md`; change to
`if os.path.basename(f) in ("_overview.md", "INDEX.md"): continue` and regenerate.

---

#### 15. `rules/magic-and-abilities/INDEX.md` — "All 181 abilities" (there are 180)

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/INDEX.md`
- **Location:** line 3, intro sentence
- **PDF page:** 62
- **Category:** alteration
- **What is wrong:** The claim of 181 abilities comes from `len(abilities)` in `gen_indexes.py`
  counting INDEX.md itself (see #14). Only 180 ability files exist.

**Source:**

```
=== T count 62-79
     181
```

**Markdown:**

```
All 181 abilities from the *Magic and Abilities* section, one file each.
```

**Suggested fix:** Change to "All 180 abilities". The PDF's 181 `T:` lines on pp. 62–79 include the
Abilities Format Key line (`T: Type S: School R: Range (if any)`), so the true count is 180 — as
VERIFICATION.md itself states.

---

#### 16. `README.md` — "181 abilities" contradicts its own "180/180"

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/README.md`
- **Location:** `## Magic and Abilities`, lines 47 and 49
- **PDF page:** 62
- **Category:** alteration
- **What is wrong:** Lines 47 and 49 say 181 abilities / 181 ability files, contradicting the same
  file's lines 8 and 69 ("180/180", "the 180 ability files") and the 180 files actually on disk.

**Source:**

```
=== T count 62-79
     181
```

**Markdown:**

```
- [Ability Index (all 181, + by-class)](rules/magic-and-abilities/INDEX.md)
- [Section Overview & Format Key](rules/magic-and-abilities/_overview.md)
- 181 individual ability files in [`rules/magic-and-abilities/`](rules/magic-and-abilities/)
```

**Suggested fix:** Fix the generator (`scripts/gen_indexes.py`, `n_ab`) to exclude INDEX.md, then
regenerate; both lines become 180.

---

#### 17. `VERIFICATION.md` — per-class spell counts wrong for Druid, Healer, Wizard

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/VERIFICATION.md`
- **Location:** `## Method` → 1. `verify_abilities.py` → "Independent completeness check" bullet
- **PDF page:** 61 (and pp. 54–61 for the four tables)
- **Category:** alteration
- **What is wrong:** The stated counts "(Bard 43, Druid 51, Healer 51, Wizard 53)" are wrong for
  three classes. The PDF tables and the converted class files both hold Druid 50, Healer 50,
  Wizard 52. Bard 43 is correct.

**Source (Wizard 6th-level block, PDF p.61):**

```
6th Level
 Battlemage                 2      1    -                     Archetype     Neutral      -
 Elemental Barrage          1      2    1/Refresh             Verbal        Sorcery          Self
 Evoker                     2      1    -                     Archetype     Neutral      -
 Finger of Death            1      -    1/Refresh             Verbal        Death        20'
 Persistent                 2      -    1/Refresh             Meta-Magic    Neutral      -
 Protection from Magic      1      -    1/Refresh             Enchantment   Protection   Other
 Sphere of Annihilation     2      1    1 Ball / Unlimited    Magic Ball    Sorcery      -
```

**Markdown:**

```
   - Independent completeness check: every spell in all four magic-user tables
     (Bard 43, Druid 51, Healer 51, Wizard 53) maps to a file with the correct class.
```

**Suggested fix:** Correct to "(Bard 43, Druid 50, Healer 50, Wizard 52)". Row counts extracted from
PDF pp. 54–55 / 56–57 / 58–59 / 60–61 are 43/50/50/52, matching `rules/classes/*.md` and INDEX.md's
By-Class tables exactly.

---

#### 18. `VERIFICATION.md` credits `verify_abilities.py` with checks it does not implement

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/VERIFICATION.md`
- **Location:** `## Method` → 1. `verify_abilities.py` (lines 13–21)
- **Category:** extra-content
- **What is wrong:** VERIFICATION.md attributes a `class_availability` cross-check, a four-table
  completeness check, and a `T:`-line count reconciliation to `scripts/verify_abilities.py`. The
  script implements none of them — it explicitly skips the `**Available to:**` line at line 44 — so
  the reported "180/180 availability correct" result is unsupported by any code in the repo.

**Source (what the script actually prints):**

```
    print(f"\n==== {perfect}/{len(blocks)} abilities: token-for-token IDENTICAL (field text) ====")
    print(f"==== {total_issues} abilities with any discrepancy ====")
```

**Markdown:**

```
   values in the written `.md`. Also cross-checks each file's `class_availability` against
   the uncropped source header line.
   - Independent completeness check: every spell in all four magic-user tables
     (Bard 43, Druid 51, Healer 51, Wizard 53) maps to a file with the correct class.
   - Count reconciliation: 181 `T:` type-lines − 1 format-key line = 180 abilities.
   - **Result: 180/180 body text identical; 180/180 availability correct.**
```

**Suggested fix:** Either add the availability/completeness checks to
`scripts/verify_abilities.py`, or move the claim to a separately documented one-off check. Running
the script today prints only `180/180 abilities: token-for-token IDENTICAL (field text)` and
`0 abilities with any discrepancy` — the body-text half of the claim is verified; the availability
half is not produced by any script under `scripts/`.

---

### Cosmetic (17)

#### 19. `rules/magic-and-abilities/ambulant.md` — "Meta- Magics" hyphen break

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/ambulant.md`
- **Location:** `**Note:**` — **PDF page:** 62 — **Category:** artifact
- **What is wrong:** PDF line-break damage at the real hyphen in the compound term "Meta-Magics"
  (cf. the same block's "T: Meta-Magic") left a stray space, rendering the defined term as a broken
  word.

**Source:** `N: Using Ambulant allows both the target indication and Ambulant to be said while moving, but not other MetaMagics.`

**Markdown:** `**Note:** Using Ambulant allows both the target indication and Ambulant to be said while moving, but not other Meta- Magics.`

**Suggested fix:** Change "other Meta- Magics." to "other Meta-Magics." (the rest of the book
consistently prints "Meta-Magics", e.g. "4. Meta-Magics do not affect other Meta-Magics").

---

#### 20. `rules/magic-and-abilities/artificer.md` — Specialty Arrow list flattened

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/artificer.md`
- **Location:** `**Limitations:**` (line 22) — **PDF page:** 63 — **Category:** artifact
- **What is wrong:** The source's three-item Specialty Arrow bullet list plus its trailing sentence
  is flattened into a single inline run-on using ` - ` separators. All text is verbatim and nothing
  is lost, but the list structure STYLE.md asks for is gone and "Look the Part becomes a fourth
  Pinning Arrow." visually trails the last bullet.

**Source:**

```
L: Rather than the normal amount of Specialty Arrows for
 an Archer, gain:
  - Pinning Arrow 3 Arrows / Unlimited (ex)
  - Phase Arrow 1 Arrow / Unlimited (ex)
  - Suppression Arrow 1 Arrow / Unlimited (ex)
 Look the Part becomes a fourth Pinning Arrow.
```

**Markdown:**

```
**Limitations:** Rather than the normal amount of Specialty Arrows for an Archer, gain: - Pinning Arrow 3 Arrows / Unlimited (ex) - Phase Arrow 1 Arrow / Unlimited (ex) - Suppression Arrow 1 Arrow / Unlimited (ex) Look the Part becomes a fourth Pinning Arrow.
```

**Suggested fix:** Render the three arrow entries as a markdown bullet list under the "…gain:"
lead-in, and put "Look the Part becomes a fourth Pinning Arrow." back on its own line outside the
list.

---

#### 21. Unescaped `<Player>` / `<armor location>` placeholders (5 files)

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/battlefield-triage.md` (+ 4 others, see below)
- **Location:** `**Effect:**` — **PDF page:** 63 — **Category:** artifact
- **What is wrong:** The literal placeholder `<Player>` is unescaped and will be swallowed as an
  HTML tag by markdown renderers. Present in five ability files: `battlefield-triage.md`,
  `discordia.md`, `naturalize-magic.md`, `corrosive-mist.md`, and `snaring-vines.md` (the last also
  contains `<armor location>`). The underlying text is verbatim to the PDF, so this is a rendering
  artifact only.

**Source:**

```
E: Bearer may cast Heal (m) by incanting “<Player> thou
 art made whole” and removing an enchantment strip.
```

**Markdown:**

```
**Effect:** Bearer may cast Heal (m) by incanting "<Player> thou art made whole" and removing an enchantment strip. Enchantment is removed when the last strip is removed.
```

**Suggested fix:** Escape or code-span the placeholder (`` `<Player>` `` or `\<Player\>`) in all five
files.

---

#### 22. `rules/magic-and-abilities/circle-of-protection.md` — "All targets:" list flattened

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/circle-of-protection.md`
- **Location:** `**Effect:**` — **PDF page:** 64 — **Category:** artifact
- **What is wrong:** The three-item bulleted sub-list under "All targets:" is collapsed into one
  run-on paragraph with literal inline `- ` markers instead of a markdown list. Text is complete and
  verbatim; only the list structure is lost.

**Source:**

```
E: The caster and up to five willing players within Touch
  range of the caster immediately have all States and Ongoing
  Effects removed and then become Insubstantial.
  All targets:
 - May not move from their starting location, and are
  unaffected by Blink and by Forced Movement effects.
 - May use abilities on players and their carried equipment
  who became Insubstantial due to the same casting of Circle
  of Protection as though they were not Insubstantial.
 - May end this Insubstantial State at any time by using the
  exit incantation for Insubstantial.
```

**Markdown:**

```
**Effect:** The caster and up to five willing players within Touch range of the caster immediately have all States and Ongoing Effects removed and then become Insubstantial. All targets: - May not move from their starting location, and are unaffected by Blink and by Forced Movement effects. - May use abilities on players and their carried equipment who became Insubstantial due to the same casting of Circle of Protection as though they were not Insubstantial. - May end this Insubstantial State at any time by using the exit incantation for Insubstantial. If the caster ends Circle of Protection by using the exit incantation for Insubstantial, the effect ends for all targets.
```

**Suggested fix:** Render the three "- May …" clauses as a real markdown bulleted list after
"All targets:", then resume the two trailing "If the caster …" sentences as a following paragraph.

---

#### 23. `rules/magic-and-abilities/juggernaut.md` — "3/ Refresh" spaced frequency token

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/juggernaut.md`
- **Location:** `**Effect:**` — **PDF page:** 69 — **Category:** artifact
- **What is wrong:** The PDF line-wrap between "3/" and "Refresh" was joined with a space instead of
  closed up. It is the only "/ Refresh" in the repo — every other file writes "N/Refresh" unspaced.

**Source:**

```
E: Gain Imbue Armor (T) and Phoenix Tears (Self) 3/
Refresh (ex) (Swift). Replace Harden with Greater Harden
(Self) (ex) at the same frequency.
```

**Markdown:**

```
**Effect:** Gain Imbue Armor (T) and Phoenix Tears (Self) 3/ Refresh (ex) (Swift). Replace Harden with Greater Harden (Self) (ex) at the same frequency.
```

**Suggested fix:** Close the gap: "Phoenix Tears (Self) 3/Refresh (ex) (Swift)".

---

#### 24. `rules/magic-and-abilities/hunter.md` — "Pick one:" list flattened with raw hyphens

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/hunter.md`
- **Location:** `**Effect:**` — **PDF page:** 69 — **Category:** artifact
- **What is wrong:** The two-item choice list is flattened into a run-on paragraph with the raw PDF
  hyphens left inline. The same ability is correctly rendered as a markdown list in `scout.md` and
  `amtgard-international-policies.md`.

**Source:**

```
E: May wield Great weapons and Javelins.
Pick one:
-Hold Person becomes 1/Life Charge x3 (m).
-Pinning Arrow becomes 2 Arrows / Unlimited (ex)
```

**Markdown:**

```
**Effect:** May wield Great weapons and Javelins. Pick one: -Hold Person becomes 1/Life Charge x3 (m). -Pinning Arrow becomes 2 Arrows / Unlimited (ex)
```

**Suggested fix:** Render as a list: "…Pick one:" followed by
"- Hold Person becomes 1/Life Charge x3 (m)." and
"- Pinning Arrow becomes 2 Arrows / Unlimited (ex)" as separate bullets.

---

#### 25. `rules/magic-and-abilities/lightning-bolt.md` — in-Effect numbered list inlined

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/lightning-bolt.md`
- **Location:** `**Effect:**` — **PDF page:** 70 — **Category:** artifact
- **What is wrong:** The indented three-item numbered sub-list is flattened to inline
  "1. … 2. … 3. …" text on one line, losing the ordered-list structure STYLE.md line 60 requires.
  All items and wording are verbatim, so no rule meaning changes. (Systematic — see Pattern C.)

**Source:**

```
 E: A player struck is subject to an Engulfing Stopped effect
 for 60 seconds. In addition Lightning Bolt will have one of
 the following effects on the object first struck:
  1. A weapon hit is destroyed
  2. Armor hit with Armor Points remaining is subject
     to Armor Breaking.
  3. A player hit receives a wound in that hit location.
```

**Markdown:**

```
**Effect:** A player struck is subject to an Engulfing Stopped effect for 60 seconds. In addition Lightning Bolt will have one of the following effects on the object first struck: 1. A weapon hit is destroyed 2. Armor hit with Armor Points remaining is subject to Armor Breaking. 3. A player hit receives a wound in that hit location.
```

**Suggested fix:** Re-flow the three enumerated outcomes as a markdown ordered list under the Effect
paragraph.

---

#### 26. `rules/magic-and-abilities/phoenix-tears.md` — six-item numbered list inlined

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/phoenix-tears.md`
- **Location:** `**Effect:**` — **PDF page:** 71 — **Category:** artifact
- **What is wrong:** The six-item numbered list inside the Effect is inlined into one paragraph
  instead of a markdown ordered list, contrary to STYLE.md line 60. All six items are present
  verbatim and in order with their numerals, so no rule content is lost.

**Source:**

```
E: Enchanted player does not die as normal. When the
player would otherwise die they instead become Frozen
for 30 seconds. If the player is still enchanted when the
Frozen State elapses or is removed:
 1. Remove all wounds.
 2. Remove all States that would be removed by death
    or respawning.
 3. Remove all Ongoing Effects with a timer.
 4. Repair all carried equipment.
 5. Remove all non-persistent enchantments other
    than Phoenix Tears.
 6. Remove a strip.
```

**Markdown:**

```
**Effect:** Enchanted player does not die as normal. When the player would otherwise die they instead become Frozen for 30 seconds. If the player is still enchanted when the Frozen State elapses or is removed: 1. Remove all wounds. 2. Remove all States that would be removed by death or respawning. 3. Remove all Ongoing Effects with a timer. 4. Repair all carried equipment. 5. Remove all non-persistent enchantments other than Phoenix Tears. 6. Remove a strip. Additionally, Phoenix Tears allows you to wear an extra Enchantment from the Protection School.
```

**Suggested fix:** Break the Effect after "…elapses or is removed:", render items 1–6 as a markdown
ordered list, then resume the "Additionally, Phoenix Tears allows you to wear an extra
Enchantment…" text as a following paragraph.

---

#### 27. `rules/magic-and-abilities/phase-bolt.md` — three-item numbered list inlined

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/phase-bolt.md`
- **Location:** `**Effect:**` — **PDF page:** 71 — **Category:** artifact
- **What is wrong:** The three-item numbered list of Phase Bolt effects is inlined into the Effect
  paragraph instead of a markdown ordered list. All three items are verbatim and in order.

**Source:**

```
E: This Magic Ball is Phasing. Additionally, will have one
of the following effects:
 1. A weapon hit is destroyed
 2. Armor hit with Armor Points remaining is subject
    to Armor Breaking.
 3. A player hit receives a wound in that hit location.
```

**Markdown:**

```
**Effect:** This Magic Ball is Phasing. Additionally, will have one of the following effects: 1. A weapon hit is destroyed 2. Armor hit with Armor Points remaining is subject to Armor Breaking. 3. A player hit receives a wound in that hit location.
```

**Suggested fix:** Break the Effect after "…one of the following effects:" and render the three
numbered options as a markdown ordered list.

---

#### 28. `rules/magic-and-abilities/summoner.md` — "2/ Life" spaced token

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/summoner.md`
- **Location:** `**Effect:**` (line 20, Example sentence) — **PDF page:** 76 — **Category:** artifact
- **What is wrong:** A PDF mid-token line wrap ("2/" + "Life") was rejoined with a space, producing
  "2/ Life becomes 4/Life" instead of "2/Life becomes 4/Life".

**Source:**

```
E: Each Enchantment purchased gives double the uses.
 Example: 1/Life Charge x3 becomes 2/Life Charge x3, 2/
 Life becomes 4/Life.
```

**Markdown:**

```
**Effect:** Each Enchantment purchased gives double the uses. Example: 1/Life Charge x3 becomes 2/Life Charge x3, 2/ Life becomes 4/Life.
```

**Suggested fix:** Change "2/ Life becomes 4/Life." to "2/Life becomes 4/Life." (the surrounding
text and the Druid 6th-level magic table both use the unspaced form).

---

#### 29. Mid-sentence multi-space runs from running-header breaks (5 files)

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/sanctuary.md` (+ 4 others)
- **Location:** `sanctuary.md:26` Limitations; `adaptive-protection.md:26` Effect;
  `elemental-barrage.md:24` Effect; `insult.md:24` Effect; `pyrotechnics.md:22` Incantation
- **PDF page:** 73 (sanctuary) — **Category:** artifact
- **What is wrong:** Five ability files retain a 4–5 space run mid-sentence where the PDF column was
  broken by the running header. No text is lost.

**Source:**

```
L: If the player is voluntarily touching (other than blocking) or carrying weapons in any fashion (tucked under arms, tied to thongs, etc) at any point during Sanctuary then they
[running header break]
may only voluntarily end Sanctuary within 20' of a friendly base, and must continue chanting until there.
```

**Markdown:**

```
**Limitations:** If the player is voluntarily touching (other than blocking) or carrying weapons in any fashion (tucked under arms, tied to thongs, etc) at any point during Sanctuary then they     may only voluntarily end Sanctuary within 20' of a friendly base, and must continue chanting until there.
```

**Suggested fix:** Collapse the multi-space runs to a single space in `sanctuary.md`
("then they may only"), `adaptive-protection.md` ("following Schools: Death, Flame"),
`elemental-barrage.md` ("immediately prior to throwing"), `insult.md` ("attack the offending
party"), and `pyrotechnics.md` (`thy belongings" x3`).

---

#### 30. All 180 ability files use a non-STYLE.md source-note format

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/abeyance.md` (identical pattern in all 180 ability files)
- **Location:** trailing source-note line — **PDF page:** 62 — **Category:** frontmatter
- **What is wrong:** The ability files insert the section name, invert the PDF/printed order, and end
  "Verbatim." instead of "Flavor text omitted.", so the repo carries two footer conventions.

**Source (STYLE.md):**

```
STYLE.md: End every file with a `---` rule followed by a one-line source note:
  `*Source: Amtgard Rules of Play V8.7, printed pp. X–Y (PDF pp. A–B). Flavor text omitted.*`
```

**Markdown:**

```
*Source: Amtgard Rules of Play V8.7, Magic and Abilities, PDF p. 62 (printed p. 59). Verbatim.*
```

**Suggested fix:** Normalize to
`*Source: Amtgard Rules of Play V8.7, printed p. 59 (PDF p. 62). Flavor text omitted.*` across all
180 ability files, or amend STYLE.md to sanction the second form (see #33).

---

#### 31. Single-page source notes are inconsistent three ways

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/weapons.md` (also `/Users/averykrouse/GitHub/amtgard-rop/rules/equipment-checking.md`)
- **Location:** trailing source-note line — **PDF page:** 15 — **Category:** frontmatter
- **What is wrong:** `weapons.md` and `equipment-checking.md` use "pp. 12" / "pp. 18" (plural, no
  range); four other single-page files use "p. 31"-style singular; `introduction.md` and
  `roleplaying-in-amtgard.md` use degenerate ranges "pp. 1–1" / "pp. 5–5".

**Source (STYLE.md):** `*Source: Amtgard Rules of Play V8.7, printed pp. X–Y (PDF pp. A–B). Flavor text omitted.*`

**Markdown:** `*Source: Amtgard Rules of Play V8.7, printed pp. 12 (PDF pp. 15). Flavor text omitted.*`

**Suggested fix:** Use "printed p. 12 (PDF p. 15)" in `rules/weapons.md` and "printed p. 18
(PDF p. 21)" in `rules/equipment-checking.md`, matching `rules/introduction.md` and the other
single-page files.

---

#### 32. `rules/magic-and-abilities/INDEX.md` has no frontmatter and no source note

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/INDEX.md`
- **Location:** top of file / end of file — **Category:** frontmatter
- **What is wrong:** INDEX.md is the only file under `rules/` with no YAML frontmatter, and it also
  lacks the trailing source note — though it is not unique on the second count:
  `rules/magic-and-abilities/_overview.md` is likewise missing the source note. All other 210 files
  under `rules/` have both.

**Source (STYLE.md):**

~~~
## Frontmatter (every file)
```yaml
---
title: <Human title>
section: <Table-of-Contents section name>
~~~

**Markdown:**

```
# Magic and Abilities — Index

All 181 abilities from the *Magic and Abilities* section, one file each.
```

**Suggested fix:** Have `scripts/gen_indexes.py` emit frontmatter
(`title: "Magic and Abilities — Index"`, `section: "Magic and Abilities"`,
`printed_pages: 59-76`, `pdf_pages: 62-79`, plus `rulebook_version`/`date`/`source`) and a trailing
`---` + source note. `_overview.md` currently ends with
`> **Note:** Individual abilities are in one file each in this directory.` and needs the footer too.

---

#### 33. `STYLE.md`'s source-note template does not describe the ability files

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/STYLE.md`
- **Location:** "End every file with a `---` rule followed by a one-line source note" (lines 68–69)
- **PDF page:** 62 — **Category:** mislabeling
- **What is wrong:** The template (`printed pp. X–Y (PDF pp. A–B). Flavor text omitted.`) matches the
  prose and class files but not the 180 ability files, which insert the section name, reverse the
  PDF/printed order, and end "Verbatim." (the other side of #30).

**Source:**

```
- End every file with a `---` rule followed by a one-line source note:
  `*Source: Amtgard Rules of Play V8.7, printed pp. X–Y (PDF pp. A–B). Flavor text omitted.*`
```

**Markdown:** `*Source: Amtgard Rules of Play V8.7, Magic and Abilities, PDF p. 62 (printed p. 59). Verbatim.*`

**Suggested fix:** Document the ability-file variant in STYLE.md rather than leaving 180 files
nominally non-conformant. The prose/class files do follow the stated template (e.g.
`rules/combat-rules.md`: `*Source: Amtgard Rules of Play V8.7, printed pp. 6–8 (PDF pp. 9–11). Flavor text omitted.*`).

---

#### 34. `rules/magic-and-abilities/INDEX.md` alphabetical table is sorted by filename, not ability name

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/rules/magic-and-abilities/INDEX.md`
- **Location:** `## All Abilities (alphabetical)` — rows for Poison Glands/Poison and Shatter Weapon/Shatter
- **PDF page:** 70 — **Category:** artifact
- **What is wrong:** `gen_indexes.py` uses `sorted(glob.glob(...))`, so the table is ordered by
  filename slug: "Poison Glands" precedes "Poison" and "Shatter Weapon" precedes "Shatter".

**Source:** `Poison                                                                         Ap 2, As 1, Dr 2`

**Markdown:**

```
| Poison Glands | Druid 5 | [poison-glands.md](poison-glands.md) |
| Poison | Anti-Paladin 2, Assassin 1, Druid 2 | [poison.md](poison.md) |
```

**Suggested fix:** In `scripts/gen_indexes.py`, sort `abilities` by `name.lower()` rather than
relying on `sorted(glob(...))` over filenames (`-` < `.` puts `poison-glands.md` before
`poison.md`).

---

#### 35. Hardcoded `~/Downloads` PDF path breaks reproducibility

- **File:** `/Users/averykrouse/GitHub/amtgard-rop/STYLE.md`
- **Location:** `## Source extraction` — the `PDF=` line (line 30); same path in
  `scripts/gen_abilities.py` line 7 and `scripts/verify_prose.py` line 15
- **Category:** artifact
- **What is wrong:** These three places hardcode `/Users/averykrouse/Downloads/Amtgard Rules of Play.pdf`
  rather than the in-repo copy STYLE.md line 3 names, breaking the reproducibility VERIFICATION.md
  claims. (`gen_indexes.py` similarly hardcodes an absolute `ROOT`.)

**Source:** `Source: `Amtgard Rules of Play.pdf` (Version 8, V8.7 "Soupy", dated 2025-07-26).`

**Markdown:** `PDF="/Users/averykrouse/Downloads/Amtgard Rules of Play.pdf"`

**Suggested fix:** Point the recipe and both scripts at the repo copy, e.g.
`PDF="$(git rev-parse --show-toplevel)/Amtgard Rules of Play.pdf"`. The Downloads path still
resolves on this machine (it is a hardlink to the same inode), so the scripts run today, but the
reference is not reproducible for anyone else who clones the repo.

---

## Systemic patterns

These are the same defect class recurring across files; each is fixable in bulk.

### Pattern A — Page-bottom flavor text merged into the last rule field on the page (6 files, all major)

`pdftotext` continues the two-column flow past the end of the ability stat blocks and appends the
page-foot vignette or sidebar to whichever field ended the column. Where the vignette spans the
gutter, each ability gets one half of every line, truncated mid-word. This produces the review's
only defects that put non-rule text inside a rule field.

| Finding | File | Field | PDF page | Absorbed text |
| --- | --- | --- | --- | --- |
| #2 | `rules/magic-and-abilities/destroy-armor.md` | Note | 65 | Lotus Brighthawk vignette, left half |
| #3 | `rules/magic-and-abilities/elemental-barrage.md` | Note | 65 | Lotus Brighthawk vignette, right half |
| #5 | `rules/magic-and-abilities/rogue.md` | Limitations | 73 | "Discovering Answers" vignette (full) |
| #6 | `rules/magic-and-abilities/vampirism.md` | Effect | 77 | "Did you Know?" sidebar (full) |
| #7 | `rules/magic-and-abilities/warlock.md` | Limitations | 78 | "Studying the Archives…", left half |
| #8 | `rules/magic-and-abilities/wounding.md` | Note | 78 | "Studying the Archives…", right half |

**Bulk fix:** truncate each field at the end of its last genuine sentence. Then add a guard to
`scripts/gen_abilities.py` (and a check to `verify_abilities.py`) that rejects any field containing
a run of 4+ spaces followed by capitalized non-rule prose, or any field text not matched by the
stat-block grammar — this pattern is exactly what a page-foot spillover looks like.

### Pattern B — Multi-space runs left where the PDF column was broken (5 files, cosmetic)

Finding #29: `sanctuary.md`, `adaptive-protection.md`, `elemental-barrage.md`, `insult.md`,
`pyrotechnics.md`. Same root cause as Pattern A but benign — the break is inside one field rather
than between a field and a vignette. A single whitespace-collapse pass over ability field text
fixes both this and the residual double-spaces left after Pattern A truncations.

### Pattern C — Lists inside ability fields flattened into run-on paragraphs (9+ files, cosmetic)

STYLE.md line 60 asks for real markdown lists; the ability generator inlines them. No text is lost
in any instance.

- Ordered lists inlined: `lightning-bolt.md` (#25), `phoenix-tears.md` (#26), `phase-bolt.md` (#27),
  and per the reviewers also `fireball.md`, `force-bolt.md`, `sphere-of-annihilation.md`.
- Bulleted / "Pick one" lists inlined: `artificer.md` (#20), `circle-of-protection.md` (#22),
  `hunter.md` (#24).

**Bulk fix:** teach the generator to detect a lead-in ending in `:` followed by `1.`/`-` tokens and
re-emit them as list items; then re-run for the whole directory. Note that the same abilities *are*
rendered as proper lists in the class files (`scout.md`) and in
`amtgard-international-policies.md`, so the corpus is currently inconsistent with itself.

### Pattern D — PDF line-wrap rejoined with a stray space inside a token (3 files, cosmetic)

`ambulant.md` "Meta- Magics" (#19), `juggernaut.md` "3/ Refresh" (#23), `summoner.md` "2/ Life"
(#28). All three are the only occurrences of their spaced form in the repo, so a targeted
find-and-replace is safe. A regex over `\d/\s+(Refresh|Life)\b` and `\w-\s+\w` would catch any
others.

### Pattern E — `scripts/gen_indexes.py` sweeps its own output into the index (4 findings)

One generator bug produces findings #14 (INDEX.md lists itself as a blank-named ability), #15
(INDEX.md says "All 181 abilities"), and #16 (README.md says 181 twice, contradicting its own
180/180). Finding #34 (sort by filename slug, not ability name) is in the same 30-line script.
Fixing the exclusion list, the count, and the sort key, then regenerating, closes all four.

### Pattern F — Source-note and frontmatter convention drift (5 findings)

The repo carries two footer conventions and several one-off spellings: the 180 ability files diverge
from STYLE.md (#30/#33), single-page notes are written three different ways (#31), INDEX.md and
`_overview.md` are missing footers/frontmatter entirely (#32), and
`weapon-types-shields-equipment.md`'s frontmatter contradicts its own footer (#10). Worth resolving
as one decision — pick the canonical form, amend STYLE.md, then normalize — rather than file by
file. A lint script asserting "every file under `rules/` has frontmatter, ends with `---` + a source
note, and the note's page range equals the frontmatter's" would keep it fixed.

### Pattern G — Repo documentation claims outrunning the repo (3 findings)

VERIFICATION.md's per-class counts are wrong (#17), it credits `verify_abilities.py` with checks
that script does not implement (#18), and its `PASS` / "100% of files" claim does not account for
the uncovered PDF p.2 (#1). README.md's 181/180 contradiction (#16) is adjacent. The verification
story is stronger than these overstatements need it to be — the body-text half of the claim really
does reproduce.

---

## Clean

Reviewed in this pass and no defect surfaced:

- **Rule text fidelity, everywhere.** Not one finding reports altered wording, a changed number
  inside a rule, a wrong range/frequency/school, or a dropped ability. Every content-level finding
  is either flavor text that leaked *in* (Pattern A) or the p.2 box that never came *in* (#1).
- **Page offsets.** The +3 printed→PDF offset holds in every file checked. The only page-range
  defect is one frontmatter range that undercounts by a page (#10) and disagrees with its own
  correct footer.
- **The 180 ability stat blocks' field text.** `scripts/verify_abilities.py` reproduces
  180/180 token-for-token identical field text with 0 discrepancies, confirmed by re-running it.
  All ability-file findings concern layout, spacing, list markup, or trailing spillover — never the
  rule text itself.
- **Ability-to-class availability.** The cross-consistency shard compared the four magic-user spell
  tables (Bard/Druid/Healer/Wizard) and the class-by-level tables against the individual ability
  files and found the mapping correct throughout; the only defect it raised was #5 (`rogue.md`
  spillover) and #11 (`paladin.md` row split). Counts are Bard 43, Druid 50, Healer 50, Wizard 52 —
  matching `rules/classes/*.md` and INDEX.md's By-Class tables exactly (only VERIFICATION.md's
  *description* of them is wrong, #17).
- **Class files.** All twelve class files under `rules/classes/` were reviewed;
  `rules/classes/paladin.md` (#11) is the sole finding. `anti-paladin.md`, `archer.md`,
  `assassin.md`, `barbarian.md`, `bard.md`, `druid.md`, `healer.md`, `monk.md`, `scout.md`,
  `warrior.md`, `wizard.md` and `_overview.md` are clean.
- **Prose rule files.** `rules/combat-rules.md`, `rules/battlegames.md`, `rules/magic-items.md`,
  `rules/amtgard-the-organization.md`, `rules/amtgard-international-policies.md`,
  `rules/rules-revision-process.md`, `rules/roleplaying-in-amtgard.md`, `rules/introduction.md`,
  `rules/equipment-checking.md`, `rules/appendix-a-award-standards.md`, and all three files under
  `rules/magic-states-effects/` (`states.md`, `special-effects.md`,
  `mechanics-and-definitions.md`) produced no body-text findings.
  `rules/armor.md` and `rules/weapons.md` / `rules/weapon-types-shields-equipment.md` produced only
  #9, #10 and #31.
- **H1 / frontmatter title agreement.** Verified across all 212 files;
  `rules/appendix-b-kingdom-boundaries.md` (#12) is the only mismatch in the corpus.
- **Frontmatter presence.** All 210 files under `rules/` except `INDEX.md` carry complete YAML
  frontmatter and a trailing source note (#32 covers the two exceptions).
- **Flavor-text exclusion policy.** Applied correctly everywhere except the six Pattern A spillovers;
  no case was found of flavor text being kept deliberately where STYLE.md says to drop it, nor of
  rules text being dropped as if it were flavor.
- **PDF page coverage.** Every PDF page from 4 through 86 is claimed by some file's `pdf_pages`
  frontmatter. Pages 1 (cover), 3 (TOC/credits/copyright) and 87 (Index) are intentionally omitted;
  only p.2 is a genuine gap (#1).

---

*Review scope: all 212 files under `rules/`, plus `README.md`, `STYLE.md`, `VERIFICATION.md` and
`scripts/`, against `Amtgard Rules of Play.pdf` (V8.7 "Soupy", 2025-07-26). 47 verified findings
merged to 35 distinct defects. No rules file was modified in producing this report.*
