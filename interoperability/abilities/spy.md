---
title: "Spy — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Spy
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Spy — Interoperability

[Rule text](../../rules/magic-and-abilities/spy.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Assassin 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Assassin archetype: Blink and Shadow Step become Charge x3 (ex); may not wear armor.

| Effect | On | Details |
| --- | --- | --- |
| Changes how often abilities can be used | bearer (benefit) | scope Blink; change charge-x3; permanent; continuously while it is worn, chanted or in effect |
| Changes Blink | bearer (benefit) | change becomes Charge x3 (ex); permanent; continuously while it is worn, chanted or in effect |
| Changes how often abilities can be used | bearer (benefit) | scope Shadow Step; change charge-x3; permanent; continuously while it is worn, chanted or in effect |
| Changes Shadow Step | bearer (benefit) | change becomes Charge x3 (ex); permanent; continuously while it is worn, chanted or in effect |
| May not wear armor | bearer (harm) | what wear-armor; permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** changes-frequency, has-drawback, more-uses · **Roles:** class-modifier, resource, mobility, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/spy.md`](../../metadata/profiles/spy.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Spy names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Blink](blink.md) | changes its numbers | Assassin |
| [Shadow Step](shadow-step.md) | changes its numbers | Assassin, Scout |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
