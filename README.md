# Amtgard Rules of Play — Markdown

Actionable markdown conversion of the **Amtgard Rules of Play, Version 8** (V8.08 "Spongy", 2026-07-25). Each rules section is its own file; large sections (Classes, Magic and Abilities) are split one file per class / per ability.

- **Verbatim** rules text, restructured into clean markdown (headings, lists, tables).
- **Flavor text excluded** (the rulebook's in-world stories/quotes).
- Conversion conventions: [`STYLE.md`](STYLE.md).
- Accuracy verification: [`VERIFICATION.md`](VERIFICATION.md) (179/179 abilities token-for-token; all prose diffs explained).
- Total: **212 files**.

## Core Sections

- [This Rulebook Made Easy](rules/this-rulebook-made-easy.md)
- [Introduction](rules/introduction.md)
- [Amtgard the Organization](rules/amtgard-the-organization.md)
- [Roleplaying in Amtgard](rules/roleplaying-in-amtgard.md)
- [Combat Rules](rules/combat-rules.md)
- [Armor](rules/armor.md)
- [Weapons](rules/weapons.md)
- [Weapon Types, Shields, and Equipment](rules/weapon-types-shields-equipment.md)
- [Equipment Checking](rules/equipment-checking.md)
- [Battlegames](rules/battlegames.md)

### Magic, Abilities, States and Special Effects

- [Mechanics & Definitions](rules/magic-states-effects/mechanics-and-definitions.md)
- [States Defined](rules/magic-states-effects/states.md)
- [Special Effects Defined](rules/magic-states-effects/special-effects.md)

## Classes

- [Classes — Overview](rules/classes/_overview.md)
- [Anti-Paladin](rules/classes/anti-paladin.md)
- [Archer](rules/classes/archer.md)
- [Assassin](rules/classes/assassin.md)
- [Barbarian](rules/classes/barbarian.md)
- [Bard](rules/classes/bard.md)
- [Druid](rules/classes/druid.md)
- [Healer](rules/classes/healer.md)
- [Monk](rules/classes/monk.md)
- [Paladin](rules/classes/paladin.md)
- [Scout](rules/classes/scout.md)
- [Warrior](rules/classes/warrior.md)
- [Wizard](rules/classes/wizard.md)

## Magic and Abilities

- [Ability Index (all 179, + by-class)](rules/magic-and-abilities/INDEX.md)
- [Section Overview & Format Key](rules/magic-and-abilities/_overview.md)
- 179 individual ability files in [`rules/magic-and-abilities/`](rules/magic-and-abilities/)

## Reference & Appendices

- [Magic Items](rules/magic-items.md)
- [Rules Revision Process](rules/rules-revision-process.md)
- [Appendix A: Award Standards](rules/appendix-a-award-standards.md)
- [Appendix B: Kingdom Boundaries and Park Sponsorship](rules/appendix-b-kingdom-boundaries.md)
- [Amtgard International Policies](rules/amtgard-international-policies.md)
- [What changed in V8.08 vs V8.7](CHANGES-V8.08.md)
- [V8.7 change log (archived; V8.08 no longer prints one)](archive/v8.7-change-log.md)

> The book's Index (printed p. 84) is intentionally omitted — it is a page-number index of the print edition, superseded by this file and the ability index.

## Copyright & Attribution

Copyright © 2014–2025 **Amtgard International**. All rights reserved. "Amtgard" and "Amtgard Rules of Play" are trademarks of Amtgard International ([amtgard.com](https://www.amtgard.com)).

This repository restructures the Amtgard Rules of Play (V8.08 "Spongy") into markdown. It was prepared by Avery W. Krouse as an Amtgard International volunteer under a Copyright Work for Hire and Transfer Agreement; all rights in the work product belong to Amtgard International. See [`LICENSE`](LICENSE) for reproduction terms. In any conflict, the official rulebook at [amtgard.com](https://www.amtgard.com) is authoritative.

## Interactive Viewer

- [`viewer/amtgard-rules-viewer.html`](viewer/amtgard-rules-viewer.html) — the whole rulebook as a single offline, cross-linked page: 253 pages, 3,172 inline links, search, deep links and both themes. See [`viewer/README.md`](viewer/README.md).

## Regenerating

- `scripts/gen_abilities.py --write` — regenerate the 179 ability files from the PDF.
- `scripts/gen_indexes.py` — regenerate this README and the ability index.
- `scripts/verify_abilities.py` — check the ability files against the PDF (body text, class availability, spell-table completeness, counts).
- `scripts/verify_prose.py` — token-multiset check of the prose and class files.
- `scripts/lint_corpus.py` — structural lint: frontmatter, titles, page offsets, source notes, links, page coverage.
- `scripts/build_viewer_data.py` then `scripts/build_viewer.py` — rebuild the interactive viewer from the markdown.

