---
title: "Greater Mend — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Greater Mend
type: Verbal
school: Sorcery
targets_other_players: true
classes: ["Druid 3rd", "Wizard 3rd"]
---

# Greater Mend — Interoperability

[Rule text](../../rules/magic-and-abilities/greater-mend.md) · **Verbal** · Sorcery School · Range Touch

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Druid (3rd), Wizard (3rd).

## What it does

By touch, restores all armor points in one location, one armor point in every location, or repairs a damaged or broken item.

| Effect | On | Details |
| --- | --- | --- |
| Repairs armor | hit-location (benefit) | amount all-points-one-location; instant; choice g1 option 1 |
| Repairs armor | target (benefit) | amount one-point-each-location; instant; choice g1 option 2 |
| Repairs equipment | target-equipment (benefit) | what one-item; instant; choice g1 option 3 |

**Capabilities:** repairs · **Roles:** equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/greater-mend.md`](../../metadata/profiles/greater-mend.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Druid](../classes/druid.md) | 3rd | 1 | - | 1/Refresh | Touch | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 3rd | 1 | - | 1/Refresh | Touch | yes | Spell table | - |

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

**These abilities name Greater Mend in their text** (auto-detected). If Greater Mend is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Artificer](artificer.md) | grants or gives | Archer |
| [Golem](golem.md) | mentions | Druid |

**Shared with:** [Druid](../classes/druid.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Druid** lists it at 3rd for 1 point. That level's table has 9 entries (9 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Wizard** lists it at 3rd for 1 point. That level's table has 10 entries (10 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
