---
title: "Innate — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Innate
type: Meta-Magic
school: Neutral
targets_other_players: false
classes: ["Monk 6th", "Bard 2nd", "Druid 2nd", "Healer 2nd", "Wizard 2nd"]
---

# Innate — Interoperability

[Rule text](../../rules/magic-and-abilities/innate.md) · **Meta-Magic** · Neutral School

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 5 class lists:** Monk (6th), Bard (2nd), Druid (2nd), Healer (2nd), Wizard (2nd).

## What it does

Meta-Magic: instantly Charges a single ability, named aloud, without the Charge Incantation.

| Effect | On | Details |
| --- | --- | --- |
| Instantly Charges an ability | caster (benefit) | instant |

**Capabilities:** more-uses · **Roles:** resource

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/innate.md`](../../metadata/profiles/innate.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Monk](../classes/monk.md) | 6th | - | - | 2/Life | - | no (ex) | Level table | - |
| [Bard](../classes/bard.md) | 2nd | 1 | 4 | 1/Refresh | - | yes | Spell table | - |
| [Druid](../classes/druid.md) | 2nd | 1 | 4 | 1/Refresh | - | yes | Spell table | - |
| [Healer](../classes/healer.md) | 2nd | 2 | 2 | 1/Life | - | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 2nd | 1 | - | 1/Refresh | - | yes | Spell table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**Shared with:** [Monk](../classes/monk.md), [Bard](../classes/bard.md), [Druid](../classes/druid.md), [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Monk** lists it at 6th; nothing else is listed at that level.
- **Bard** lists it at 2nd for 1 point. That level's table has 7 entries (9 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Druid** lists it at 2nd for 1 point. That level's table has 9 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Healer** lists it at 2nd for 2 points. That level's table has 9 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Wizard** lists it at 2nd for 1 point. That level's table has 8 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
