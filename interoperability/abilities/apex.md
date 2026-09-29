---
title: "Apex — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Apex
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Apex — Interoperability

[Rule text](../../rules/magic-and-abilities/apex.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Scout 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Scout archetype: gains Mend 1/Life and Sleight of Mind (Self) 1/Life; loses Evolution, Hold Person and Pinning Arrow.

| Effect | On | Details |
| --- | --- | --- |
| Grants Mend | bearer (benefit) | how gains; frequency 1/Life (ex); permanent; continuously while it is worn, chanted or in effect |
| Grants Sleight of Mind | bearer (benefit) | how gains; frequency (Self) 1/Life (ex); permanent; continuously while it is worn, chanted or in effect |
| Removes Evolution | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |
| Removes Hold Person | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |
| Removes Pinning Arrow | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** grants-abilities, has-drawback · **Roles:** class-modifier, equipment, defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/apex.md`](../../metadata/profiles/apex.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Apex names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Evolution](evolution.md) | removes | Scout |
| [Hold Person](hold-person.md) | removes | Assassin, Scout, Healer, Wizard |
| [Mend](mend.md) | grants or gives | Archer, Bard, Druid, Healer, Wizard |
| [Pinning Arrow](pinning-arrow.md) | removes | Archer, Scout |
| [Sleight of Mind](sleight-of-mind.md) | grants or gives | Bard |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
