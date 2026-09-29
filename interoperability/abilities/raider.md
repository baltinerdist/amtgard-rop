---
title: "Raider — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Raider
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Raider — Interoperability

[Rule text](../../rules/magic-and-abilities/raider.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Barbarian 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Barbarian archetype: gains Bear Strength (Self) 1/Life; Look the Part becomes an extra use of Brutal Strike; loses all Rage.

| Effect | On | Details |
| --- | --- | --- |
| Grants Bear Strength | bearer (benefit) | how gains; frequency (Self) 1/Life (ex); permanent; continuously while it is worn, chanted or in effect |
| Changes Look The Part | bearer (benefit) | ability Brutal Strike; how extra-use-of; permanent; continuously while it is worn, chanted or in effect |
| Changes Brutal Strike | bearer (benefit) | change gains an additional use, in place of Look the Part; permanent; continuously while it is worn, chanted or in effect |
| Changes how often abilities can be used | bearer (benefit) | scope Brutal Strike; change other; permanent; continuously while it is worn, chanted or in effect |
| Removes Rage | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** changes-frequency, grants-abilities, has-drawback, more-uses · **Roles:** class-modifier, equipment, control, debuff

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/raider.md`](../../metadata/profiles/raider.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Raider names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Bear Strength](bear-strength.md) | grants or gives | Druid |
| [Brutal Strike](brutal-strike.md) | grants or gives | Anti-Paladin, Barbarian |
| [Rage](rage.md) | removes | Barbarian |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
