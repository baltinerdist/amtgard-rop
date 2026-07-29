#!/usr/bin/env python3
"""Generate README.md (root navigable index) and rules/magic-and-abilities/INDEX.md
(master ability index + by-class grouping) from the converted markdown corpus."""
import glob, re, os
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
           "printed_pages: 59-75",
           "pdf_pages: 62-78",
           'rulebook_version: V8.7 "Soupy"',
           "rulebook_date: 2025-07-26",
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
            "*Source: Amtgard Rules of Play V8.7, printed pp. 59–75 (PDF pp. 62–78). "
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
             '(V8.7 "Soupy", 2025-07-26). Each rules section is its own file; large sections '
             "(Classes, Magic and Abilities) are split one file per class / per ability.\n")
    o.append("- **Verbatim** rules text, restructured into clean markdown (headings, lists, tables).\n"
             "- **Flavor text excluded** (the rulebook's in-world stories/quotes).\n"
             "- Conversion conventions: [`STYLE.md`](STYLE.md).\n"
             "- Accuracy verification: [`VERIFICATION.md`](VERIFICATION.md) "
             "(180/180 abilities token-for-token; all prose diffs explained).\n"
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
    o.append("")
    o.append("> The book's Index (printed p. 84) is intentionally omitted — it is a page-number "
             "index of the print edition, superseded by this file and the ability index.\n")
    o.append("## Copyright & Attribution\n")
    o.append("Copyright © 2014–2025 **Amtgard International**. All rights reserved. "
             '"Amtgard" and "Amtgard Rules of Play" are trademarks of Amtgard International '
             "([amtgard.com](https://www.amtgard.com)).\n")
    o.append("This repository restructures the Amtgard Rules of Play (V8.7 \"Soupy\") into markdown. "
             "It was prepared by Avery W. Krouse as an Amtgard International volunteer under a "
             "Copyright Work for Hire and Transfer Agreement; all rights in the work product belong "
             "to Amtgard International. See [`LICENSE`](LICENSE) for reproduction terms. In any "
             "conflict, the official rulebook at [amtgard.com](https://www.amtgard.com) is authoritative.\n")
    o.append("## Regenerating\n")
    o.append("- `scripts/gen_abilities.py --write` — regenerate the 180 ability files from the PDF.\n"
             "- `scripts/gen_indexes.py` — regenerate this README and the ability index.\n"
             "- `scripts/verify_abilities.py` — check the ability files against the PDF "
             "(body text, class availability, spell-table completeness, counts).\n"
             "- `scripts/verify_prose.py` — token-multiset check of the prose and class files.\n"
             "- `scripts/lint_corpus.py` — structural lint: frontmatter, titles, page offsets, "
             "source notes, links, page coverage.\n")
    return "\n".join(o) + "\n"

with open(os.path.join(ROOT, "README.md"), "w") as f:
    f.write(readme())
print("Wrote README.md and rules/magic-and-abilities/INDEX.md")
print(f"abilities indexed: {n_ab}")
