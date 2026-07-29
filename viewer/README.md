# Rules Viewer

A single-file, offline, cross-linked reading of the whole rulebook.

**[`amtgard-rules-viewer.html`](amtgard-rules-viewer.html)** — open it in a browser. No server,
no network, no dependencies.

Every rule term is a link, **everywhere it appears** rather than only on first mention: follow a
class to an ability, to the State that ability inflicts, to the rule defining that State. The path
you took stays visible along the top and is clickable back to any step.

| | |
| --- | ---: |
| Pages | 250 |
| Abilities | 180 |
| Defined terms (States, Special Effects, Mechanics) | 37 |
| Inline cross-links | 3,087 |
| Links resolving to a specific clause, not just a page | 110 |

Nothing here is retyped. Every page is generated from the markdown in [`../rules/`](../rules/) and
carries its source file and printed/PDF page number, so any line can be checked against the book.

## Using it

- **Search** — press <kbd>/</kbd>. Titles and full text, with arrow keys and <kbd>Enter</kbd>.
- **Index** — grouped by the book's own structure; the Abilities group collapses.
- **Deep links** — a route is `#<page-id>` or `#<page-id>$<section-anchor>`, e.g.
  `#page:armor$chainmail`. Both are shareable.
- **Themes** — follows your system by default; the toggle cycles light / dark / auto.
- Works down to phone widths; wide tables scroll inside their own column.

## Building

```bash
python3 scripts/build_viewer_data.py   # rules/*.md  -> viewer/wiki-data.json
python3 scripts/build_viewer.py        # template + data -> amtgard-rules-viewer.html
```

The first step needs only the markdown — not the PDF — so it runs from a fresh clone.
`wiki-data.json` is a build intermediate and is not tracked.

`build_viewer_data.py` fails the build rather than shipping a defect if: any page loses or gains a
word against its source markdown, a cross-link points at a page that does not exist, an anchor does
not resolve, HTML tags are unbalanced, or the autolinker disagrees with a link hand-authored in the
source. `build_viewer.py` refuses to write a file that is not pure ASCII, that left `__DATA__`
unsubstituted, or whose embedded JSON could break out of its `<script>` block.

## Design notes

- **Class stripes are the sashes.** Each class is marked with the colour of its actual sash, taken
  from its `**Garb:**` line: Archer orange, Wizard yellow, Warrior purple, Barbarian white,
  Assassin black, Anti-Paladin metallic silver, Paladin metallic gold, and so on. The two metallics
  get a sheen gradient; white, black and yellow get an outline in whichever theme would otherwise
  swallow them, so the colour stays true rather than being adjusted for legibility.
- **Structure encodes the book.** The home page ranks pages by inbound reference count — a factual
  statement about which rules the rest of the book leans on (Enchantments 101, Verbal 83, Charge 44).
- Text is verbatim; flavour text is excluded, per [`../STYLE.md`](../STYLE.md).

## A contradiction in the source

Building the viewer cross-checked every ability's `class_availability` against the class tables for
all twelve classes — including the martial classes, which the existing verification scripts never
covered. Three Scout entries disagree **in the rulebook itself**:

| Ability | Scout class table (PDF p. 50) | Ability stat block (PDF pp. 66–71) |
| --- | --- | --- |
| Hold Person | 4th | `Sc 5` |
| Pinning Arrow | 4th | `Sc 5` |
| Evolution | 5th | `Sc 4` |

The conversion is faithful to both sides, so this is errata in V8.7 rather than a conversion bug —
worth raising with the rules committee. (A fourth flag, Greater Harden at Warrior 6, is explainable:
it is granted by the Juggernaut archetype rather than by the level table.)
