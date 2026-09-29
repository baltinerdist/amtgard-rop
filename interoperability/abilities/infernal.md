---
title: "Infernal — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Infernal
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Infernal — Interoperability

[Rule text](../../rules/magic-and-abilities/infernal.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Anti-Paladin 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Anti-Paladin archetype: gains Fireball 2 Balls/Unlimited; Flame Blade becomes (Self) 2/Refresh Charge x5; no shields; loses Steal Life Essence.

| Effect | On | Details |
| --- | --- | --- |
| Grants Fireball | bearer (benefit) | how gains; frequency 2 Balls / Unlimited (m); permanent; continuously while it is worn, chanted or in effect |
| Changes Flame Blade | bearer (benefit) | change becomes (Self) 2/Refresh Charge x5; permanent; continuously while it is worn, chanted or in effect |
| May not wield shields | bearer (harm) | what wield-shields; permanent; continuously while it is worn, chanted or in effect |
| Removes Steal Life Essence | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |
| Changes how often abilities can be used | bearer (benefit) | scope Flame Blade; change charge-x5; permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** changes-frequency, grants-abilities, has-drawback, more-uses · **Roles:** class-modifier, offense, equipment, resource

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/infernal.md`](../../metadata/profiles/infernal.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Infernal names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Fireball](fireball.md) | grants or gives | Wizard |
| [Flame Blade](flame-blade.md) | changes its numbers | Anti-Paladin, Druid |
| [Steal Life Essence](steal-life-essence.md) | removes | Anti-Paladin, Healer, Wizard |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
