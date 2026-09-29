#!/usr/bin/env python3
"""Generate README.md (root navigable index) and rules/magic-and-abilities/INDEX.md
(master ability index + by-class grouping) from the converted markdown corpus."""
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rop_version as V
_A, _B = V.ABILITY_PAGES[0], V.ABILITY_PAGES[-1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MA = os.path.join(ROOT, "rules/magic-and-abilities")
# files in the abilities directory that are not abilities
NOT_ABILITIES = ("_overview.md", "INDEX.md")

def fm(path):
    t = open(path).read()
    m = re.search(r'^---\n(.*?)\n---', t, re.S)
    d = {}
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                d[k.strip()] = v.strip().strip('"')
    return d

# ---- abilities index ----
abilities = []
for f in sorted(glob.glob(os.path.join(MA, "*.md"))):
    if os.path.basename(f) in NOT_ABILITIES: continue
    d = fm(f)
    name = d.get("title", "")
    ca = d.get("class_availability", "[]")
    classes = re.findall(r'"([^"]+)"', ca)
    abilities.append((name, classes, os.path.basename(f)))
# sort by ability name, not by filename slug: '-' sorts before '.', which would put
# poison-glands.md ahead of poison.md and Shatter Weapon ahead of Shatter
abilities.sort(key=lambda a: a[0].lower())

def ability_index():
    out = ["---",
           'title: "Magic and Abilities — Index"',
           "section: Magic and Abilities",
           f"printed_pages: {_A-V.PRINT_OFFSET}-{_B-V.PRINT_OFFSET}",
           f"pdf_pages: {_A}-{_B}",
           f'rulebook_version: {V.NAME}',
           f"rulebook_date: {V.DATE}",
           "source: Amtgard Rules of Play Version 8",
           "---",
           "",
           "# Magic and Abilities — Index",
           "",
           f"All {len(abilities)} abilities from the *Magic and Abilities* section, one file each.",
           "See [`_overview.md`](_overview.md) for the section intro and format key.",
           "", "## All Abilities (alphabetical)", "",
           "| Ability | Available To | File |", "| --- | --- | --- |"]
    for name, classes, fn in abilities:
        out.append(f"| {name} | {', '.join(classes) if classes else '—'} | [{fn}]({fn}) |")
    # by-class grouping
    byclass = {}
    for name, classes, fn in abilities:
        for c in classes:
            cls, lvl = c.rsplit(" ", 1)
            byclass.setdefault(cls, []).append((int(lvl), name, fn))
    out += ["", "## By Class", ""]
    for cls in sorted(byclass):
        out.append(f"### {cls}")
        out.append("")
        out.append("| Lvl | Ability | File |")
        out.append("| --- | --- | --- |")
        for lvl, name, fn in sorted(byclass[cls]):
            out.append(f"| {lvl} | {name} | [{fn}]({fn}) |")
        out.append("")
    out += ["---",
            f"*Source: Amtgard Rules of Play {V.VERSION}, printed pp. {_A-V.PRINT_OFFSET}–{_B-V.PRINT_OFFSET} (PDF pp. {_A}–{_B}). "
            "Flavor text omitted.*"]
    return "\n".join(out) + "\n"

with open(os.path.join(MA, "INDEX.md"), "w") as f:
    f.write(ability_index())

# ---- root README ----
SECTIONS = [  # (book order) label, path (relative to root)
    ("This Rulebook Made Easy", "rules/this-rulebook-made-easy.md"),
    ("Introduction", "rules/introduction.md"),
    ("Amtgard the Organization", "rules/amtgard-the-organization.md"),
    ("Roleplaying in Amtgard", "rules/roleplaying-in-amtgard.md"),
    ("Combat Rules", "rules/combat-rules.md"),
    ("Armor", "rules/armor.md"),
    ("Weapons", "rules/weapons.md"),
    ("Weapon Types, Shields, and Equipment", "rules/weapon-types-shields-equipment.md"),
    ("Equipment Checking", "rules/equipment-checking.md"),
    ("Battlegames", "rules/battlegames.md"),
]
CLASSES = sorted(glob.glob(os.path.join(ROOT, "rules/classes/*.md")))
n_ab = len(abilities)

def readme():
    o = []
    o.append("# Amtgard Rules of Play — Markdown\n")
    o.append("Actionable markdown conversion of the **Amtgard Rules of Play, Version 8** "
             f'({V.NAME}, {V.DATE}). Each rules section is its own file; large sections '
             "(Classes, Magic and Abilities) are split one file per class / per ability.\n")
    o.append("- **Verbatim** rules text, restructured into clean markdown (headings, lists, tables).\n"
             "- **Flavor text excluded** (the rulebook's in-world stories/quotes).\n"
             "- Conversion conventions: [`STYLE.md`](STYLE.md).\n"
             "- Accuracy verification: [`VERIFICATION.md`](VERIFICATION.md) "
             f"({n_ab}/{n_ab} abilities token-for-token; all prose diffs explained).\n"
             f"- Total: **{len(glob.glob(os.path.join(ROOT,'rules/**/*.md'),recursive=True))} files**.\n")
    o.append("## Core Sections\n")
    for label, path in SECTIONS:
        o.append(f"- [{label}]({path})")
    o.append("")
    o.append("### Magic, Abilities, States and Special Effects\n")
    o.append("- [Mechanics & Definitions](rules/magic-states-effects/mechanics-and-definitions.md)")
    o.append("- [States Defined](rules/magic-states-effects/states.md)")
    o.append("- [Special Effects Defined](rules/magic-states-effects/special-effects.md)")
    o.append("")
    o.append("## Classes\n")
    o.append("- [Classes — Overview](rules/classes/_overview.md)")
    for c in CLASSES:
        b = os.path.basename(c)
        if b == "_overview.md": continue
        d = fm(c)
        o.append(f"- [{d.get('title', b)}](rules/classes/{b})")
    o.append("")
    o.append("## Magic and Abilities\n")
    o.append(f"- [Ability Index (all {n_ab}, + by-class)](rules/magic-and-abilities/INDEX.md)")
    o.append("- [Section Overview & Format Key](rules/magic-and-abilities/_overview.md)")
    o.append(f"- {n_ab} individual ability files in [`rules/magic-and-abilities/`](rules/magic-and-abilities/)")
    o.append("")
    o.append("## Reference & Appendices\n")
    o.append("- [Magic Items](rules/magic-items.md)")
    o.append("- [Rules Revision Process](rules/rules-revision-process.md)")
    o.append("- [Appendix A: Award Standards](rules/appendix-a-award-standards.md)")
    o.append("- [Appendix B: Kingdom Boundaries and Park Sponsorship](rules/appendix-b-kingdom-boundaries.md)")
    o.append("- [Amtgard International Policies](rules/amtgard-international-policies.md)")
    o.append("- [What changed in V8.08 vs V8.7](CHANGES-V8.08.md)")
    o.append("- [V8.7 change log (archived; V8.08 no longer prints one)](archive/v8.7-change-log.md)")
    o.append("")
    o.append("> The book's Index (printed p. 84) is intentionally omitted — it is a page-number "
             "index of the print edition, superseded by this file and the ability index.\n")
    o.append("## Copyright & Attribution\n")
    o.append("Copyright © 2014–2025 **Amtgard International**. All rights reserved. "
             '"Amtgard" and "Amtgard Rules of Play" are trademarks of Amtgard International '
             "([amtgard.com](https://www.amtgard.com)).\n")
    o.append("This repository restructures the Amtgard Rules of Play (" + V.NAME + ") into markdown. "
             "It was prepared by Avery W. Krouse as an Amtgard International volunteer under a "
             "Copyright Work for Hire and Transfer Agreement; all rights in the work product belong "
             "to Amtgard International. See [`LICENSE`](LICENSE) for reproduction terms. In any "
             "conflict, the official rulebook at [amtgard.com](https://www.amtgard.com) is authoritative.\n")
    o.append("## Interactive Viewer\n")
    o.append("- [`viewer/amtgard-rules-viewer.html`](viewer/amtgard-rules-viewer.html) \u2014 the whole "
             "rulebook as a single offline, cross-linked page: 253 pages, 3,172 inline links, "
             "search, deep links and both themes. See [`viewer/README.md`](viewer/README.md).\n")
    o.append("## Interoperability\n")
    o.append("- [`interoperability/`](interoperability/README.md) \u2014 per-ability and per-class reference: who has each ability at what level, "
             "who it works on or is blocked by (immunities), shared abilities, and which abilities name it. Built for "
             "\"what if we move this ability from 4th to 6th level\" questions. [Ability \u00d7 class matrix](interoperability/MATRIX.md).")
    o.append("- [`viewer/ability-chords.html`](viewer/ability-chords.html) \u2014 chord diagram of the same data (blue = shared, green = works, red = blocked).\n")
    o.append("## Ability metadata\n")
    o.append("- [`metadata/`](metadata/README.md) \u2014 a structured description of every ability, spell, trait, archetype, Meta-Magic and "
             "Equipment trait: each effect with who it lands on, for how long and under what conditions, requirements, limits, how it ends, "
             "properties and the names it references, with every rule sentence tied to a fact. Derived capabilities (causes death, holds in "
             "place, has a drawback ...), what can stop each ability, look-alikes and a per-class [duplicate check](metadata/dedupe/). "
             "Query with `scripts/meta_query.py`; tested against a [40-question acceptance battery](metadata/ACCEPTANCE.md).")
    o.append("- [`viewer/ability-explorer.html`](viewer/ability-explorer.html) \u2014 interactive explorer for the same data (filters, look-alikes, "
             "side-by-side compare).\n")
    o.append("## Regenerating\n")
    o.append(f"- `scripts/gen_abilities.py --write` — regenerate the {n_ab} ability files from the PDF.\n"
             "- `scripts/gen_interop.py` — regenerate `interoperability/`; `scripts/build_chord.py` — rebuild the chord diagram; "
             "`scripts/meta_check.py`, `scripts/meta_build.py`, `scripts/meta_acceptance.py` and `scripts/build_meta_explorer.py` — validate, "
             "rebuild, test and view `metadata/` (see [`metadata/README.md`](metadata/README.md)).\n"
             "- `scripts/gen_indexes.py` — regenerate this README and the ability index.\n"
             "- `scripts/verify_abilities.py` — check the ability files against the PDF "
             "(body text, class availability, spell-table completeness, counts).\n"
             "- `scripts/verify_prose.py` — token-multiset check of the prose and class files.\n"
             "- `scripts/lint_corpus.py` — structural lint: frontmatter, titles, page offsets, "
             "source notes, links, page coverage.\n"
             "- `scripts/build_viewer_data.py` then `scripts/build_viewer.py` — rebuild the "
             "interactive viewer from the markdown.\n")
    return "\n".join(o) + "\n"

with open(os.path.join(ROOT, "README.md"), "w") as f:
    f.write(readme())
print("Wrote README.md and rules/magic-and-abilities/INDEX.md")
print(f"abilities indexed: {n_ab}")
