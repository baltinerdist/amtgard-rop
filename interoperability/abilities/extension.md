---
title: "Extension — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Extension
type: Meta-Magic
school: Neutral
targets_other_players: false
classes: ["Bard 3rd", "Druid 3rd", "Healer 3rd", "Wizard 3rd"]
---

# Extension — Interoperability

[Rule text](../../rules/magic-and-abilities/extension.md) · **Meta-Magic** · Neutral School

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 4 class lists:** Bard (3rd), Druid (3rd), Healer (3rd), Wizard (3rd).

## What it does

Meta-Magic: the next 20' Verbal has its range extended to 50'.

| Effect | On | Details |
| --- | --- | --- |
| Modifies the next ability cast | caster (benefit) | mode extend-range-to-50ft; until used |

**Capabilities:** - · **Roles:** utility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/extension.md`](../../metadata/profiles/extension.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Bard](../classes/bard.md) | 3rd | 1 | 2 | 1/Life | - | yes | Spell table | - |
| [Druid](../classes/druid.md) | 3rd | 1 | 2 | 1/Life | - | yes | Spell table | - |
| [Healer](../classes/healer.md) | 3rd | 1 | 2 | 1/Life | - | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 3rd | 1 | 2 | 1/Life | - | yes | Spell table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**These abilities name Extension in their text** (auto-detected). If Extension is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Amplification](amplification.md) | grants or gives | Bard |
| [Legend](legend.md) | mentions | Bard |

**Shared with:** [Bard](../classes/bard.md), [Druid](../classes/druid.md), [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Bard** lists it at 3rd for 1 point. That level's table has 6 entries (7 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). Archetype that names it: Legend (archetypes are outside this model).
- **Druid** lists it at 3rd for 1 point. That level's table has 9 entries (9 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Healer** lists it at 3rd for 1 point. That level's table has 9 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Wizard** lists it at 3rd for 1 point. That level's table has 10 entries (10 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
