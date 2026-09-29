---
title: "Marauder — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Marauder
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Marauder — Interoperability

[Rule text](../../rules/magic-and-abilities/marauder.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Warrior 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Warrior archetype: gains Momentum Unlimited (Ambulant); Insult becomes 1/Life Charge x5; armor max 4pts; no Large shields; Ancestral Armor not chargeable.

| Effect | On | Details |
| --- | --- | --- |
| Grants Momentum | bearer (benefit) | how gains; frequency Unlimited (ex); meta Ambulant; permanent; continuously while it is worn, chanted or in effect |
| Changes Insult | bearer (benefit) | change becomes 1/Life Charge x5 (m) (Ambulant); permanent; continuously while it is worn, chanted or in effect |
| Changes how often abilities can be used | bearer (benefit) | scope Insult; change charge-x5; permanent; continuously while it is worn, chanted or in effect |
| Changes the armor limit | bearer (harm) | points 4; change set; permanent; continuously while it is worn, chanted or in effect |
| May not wield large shields | bearer (harm) | what wield-large-shields; permanent; continuously while it is worn, chanted or in effect |
| Changes Ancestral Armor | bearer (harm) | change is no longer chargeable; permanent; continuously while it is worn, chanted or in effect |
| Changes how often abilities can be used | bearer (harm) | scope Ancestral Armor; change other; permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** changes-frequency, grants-abilities, has-drawback, more-uses · **Roles:** class-modifier, resource, equipment, control

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/marauder.md`](../../metadata/profiles/marauder.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Marauder names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Ancestral Armor](ancestral-armor.md) | mentions | Warrior, Healer |
| [Insult](insult.md) | changes its numbers | Warrior, Bard |
| [Momentum](momentum.md) | grants or gives | Archer, Barbarian, Warrior |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
