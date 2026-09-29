---
title: "Rogue — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Rogue
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Rogue — Interoperability

[Rule text](../../rules/magic-and-abilities/rogue.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Assassin 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Assassin archetype: regains a use of Coup de Grace when killing an enemy with a thrown weapon; may not wield Bows or Long weapons.

| Effect | On | Details |
| --- | --- | --- |
| Restores used abilities | bearer (benefit) | amount one; ability Coup de Grace; instant; after the caster kills an enemy (Kill Trigger); only if the kill was made with a thrown weapon |
| May not wield bows | bearer (harm) | what wield-bows; permanent; continuously while it is worn, chanted or in effect |
| May not wield long weapons | bearer (harm) | what wield-long-weapons; permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** has-drawback, more-uses · **Roles:** class-modifier, resource, offense, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/rogue.md`](../../metadata/profiles/rogue.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Rogue names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Coup de Grace](coup-de-grace.md) | mentions | Assassin |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
