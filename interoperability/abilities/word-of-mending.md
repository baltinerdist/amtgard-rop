---
title: "Word of Mending — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Word of Mending
type: Verbal
school: Sorcery
targets_other_players: true
classes: ["Druid 6th", "Wizard 6th"]
---

# Word of Mending — Interoperability

[Rule text](../../rules/magic-and-abilities/word-of-mending.md) · **Verbal** · Sorcery School · Range Touch

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Druid (6th), Wizard (6th).

## What it does

Repairs all equipment a touched player carries and restores all their worn armor to full; not within 20' of a living enemy.

| Effect | On | Details |
| --- | --- | --- |
| Repairs equipment | target (benefit) | what all-carried-equipment; instant |
| Repairs armor | target (benefit) | amount all-armor; instant |

**Capabilities:** repairs · **Roles:** equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/word-of-mending.md`](../../metadata/profiles/word-of-mending.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Druid](../classes/druid.md) | 6th | 1 | - | 1/Refresh | Touch | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 6th | 1 | - | 1/Refresh | Touch | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works |  |
| [Paladin](../classes/paladin.md) | Works |  |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

Touch and Other range also need the target to be willing, dead, stunned, frozen or Insubstantial and unable to move. That applies to every class alike and is not modelled.

## Connected abilities

**These abilities name Word of Mending in their text** (auto-detected). If Word of Mending is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Golem](golem.md) | mentions | Druid |

**Shared with:** [Druid](../classes/druid.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Druid** lists it at 6th for 1 point. That level's table has 8 entries (11 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is already too high for it.
- **Wizard** lists it at 6th for 1 point. That level's table has 9 entries (14 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is already too high for it.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
