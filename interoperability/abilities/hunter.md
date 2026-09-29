---
title: "Hunter — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Hunter
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Hunter — Interoperability

[Rule text](../../rules/magic-and-abilities/hunter.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Scout 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Scout archetype: Great weapons and Javelins; Hold Person 1/Life Charge x3 or Pinning Arrow 2 Arrows/Unlimited (whichever taken at 4th); no shields; loses Evolution, Release.

| Effect | On | Details |
| --- | --- | --- |
| Allows equipment | bearer (benefit) | what great-weapon; permanent; continuously while it is worn, chanted or in effect |
| Allows equipment | bearer (benefit) | what javelins; permanent; continuously while it is worn, chanted or in effect |
| Changes Hold Person | bearer (benefit) | change becomes 1/Life Charge x3 (m); permanent; continuously while it is worn, chanted or in effect; choice g1 option 1 |
| Changes Pinning Arrow | bearer (benefit) | change becomes 2 Arrows / Unlimited (ex); permanent; continuously while it is worn, chanted or in effect; choice g1 option 2 |
| May not wield shields | bearer (harm) | what wield-shields; permanent; continuously while it is worn, chanted or in effect |
| Removes Evolution | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |
| Removes Release | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |
| Changes how often abilities can be used | bearer (benefit) | scope Hold Person; change charge-x3; permanent; continuously while it is worn, chanted or in effect; choice g1 option 1 |
| Changes how often abilities can be used | bearer (benefit) | scope Pinning Arrow; change double-uses; permanent; continuously while it is worn, chanted or in effect; choice g1 option 2 |

**Capabilities:** changes-frequency, has-drawback, more-uses · **Roles:** class-modifier, equipment, resource, control

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/hunter.md`](../../metadata/profiles/hunter.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Hunter names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Evolution](evolution.md) | removes | Scout |
| [Hold Person](hold-person.md) | changes its numbers | Assassin, Scout, Healer, Wizard |
| [Pinning Arrow](pinning-arrow.md) | changes its numbers | Archer, Scout |
| [Release](release.md) | removes | Scout, Bard, Druid, Healer, Wizard |

## If you change its level

**Its own text mentions a level:**
- “Gain the benefit of an option only if that ability was chosen at level 4.”

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
