---
title: "Corruptor — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Corruptor
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Corruptor — Interoperability

[Rule text](../../rules/magic-and-abilities/corruptor.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Anti-Paladin 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Anti-Paladin archetype: gains Void Touched (Self) 2/Refresh; Terror becomes 1/Life Charge x10; no Great Weapons or Javelins; loses Flame Blade.

| Effect | On | Details |
| --- | --- | --- |
| Grants Void Touched | bearer (benefit) | how gains; frequency (Self) 2/Refresh (m); permanent; continuously while it is worn, chanted or in effect |
| Changes Terror | bearer (benefit) | change all uses become 1/Life Charge x10 (m); permanent; continuously while it is worn, chanted or in effect |
| Changes how often abilities can be used | bearer (benefit) | scope Terror; change charge-x10; permanent; continuously while it is worn, chanted or in effect |
| May not wield great weapons | bearer (harm) | what wield-great-weapons; permanent; continuously while it is worn, chanted or in effect |
| May not wield javelins | bearer (harm) | what wield-javelins; permanent; continuously while it is worn, chanted or in effect |
| Removes Flame Blade | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** changes-frequency, grants-abilities, has-drawback, more-uses · **Roles:** class-modifier, offense, control, resource, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/corruptor.md`](../../metadata/profiles/corruptor.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Corruptor names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Flame Blade](flame-blade.md) | removes | Anti-Paladin, Druid |
| [Terror](terror.md) | changes its numbers | Anti-Paladin, Bard |
| [Void Touched](void-touched.md) | grants or gives | Wizard |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
