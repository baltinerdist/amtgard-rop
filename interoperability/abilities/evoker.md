---
title: "Evoker — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Evoker
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Evoker — Interoperability

[Rule text](../../rules/magic-and-abilities/evoker.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Wizard 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Wizard archetype: Elemental Barrage becomes Charge x10 (must still be purchased); may not purchase 20' or 50' Verbals.

| Effect | On | Details |
| --- | --- | --- |
| Changes Elemental Barrage | bearer (benefit) | change becomes Charge x10; permanent; continuously while it is worn, chanted or in effect |
| Changes how often abilities can be used | bearer (benefit) | scope Elemental Barrage; change charge-x10; permanent; continuously while it is worn, chanted or in effect |
| Forbids purchases | bearer (harm) | scope Verbals with a range of 20' or 50'; permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** changes-frequency, has-drawback, more-uses · **Roles:** class-modifier, resource

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/evoker.md`](../../metadata/profiles/evoker.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Evoker names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Elemental Barrage](elemental-barrage.md) | changes its numbers | Wizard |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
