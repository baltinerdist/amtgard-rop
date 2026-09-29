---
title: "Guardian — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Guardian
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Guardian — Interoperability

[Rule text](../../rules/magic-and-abilities/guardian.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Paladin 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Paladin archetype: gains Imbue (Touch) 1/Life and Martyr (Other) 2/Life Charge x3; one Imbue active at a time; loses Protection from Evil and Magic.

| Effect | On | Details |
| --- | --- | --- |
| Grants Imbue | bearer (benefit) | how gains; frequency (Touch) 1/Life (m); permanent; continuously while it is worn, chanted or in effect |
| Grants Martyr | bearer (benefit) | how gains; frequency (Other) 2/Life Charge x3 (ex); permanent; continuously while it is worn, chanted or in effect |
| Removes Protection from Evil | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |
| Removes Protection from Magic | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |
| Changes Imbue | bearer (harm) | change only one instance of Imbue may be active at a time; permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** grants-abilities, has-drawback · **Roles:** class-modifier, equipment, defense, utility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/guardian.md`](../../metadata/profiles/guardian.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Guardian names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Imbue](imbue.md) | grants or gives | Healer |
| [Martyr](martyr.md) | grants or gives | Paladin |
| [Protection from Evil](protection-from-evil.md) | removes | Paladin |
| [Protection from Magic](protection-from-magic.md) | removes | Paladin, Healer, Wizard |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
