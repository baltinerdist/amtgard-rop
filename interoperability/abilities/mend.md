---
title: "Mend — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Mend
type: Verbal
school: Sorcery
targets_other_players: true
classes: ["Archer 2nd", "Bard 2nd", "Druid 1st", "Healer 3rd", "Wizard 1st"]
---

# Mend — Interoperability

[Rule text](../../rules/magic-and-abilities/mend.md) · **Verbal** · Sorcery School · Range Touch

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 5 class lists:** Archer (2nd), Bard (2nd), Druid (1st), Healer (3rd), Wizard (1st).

## What it does

By touch, repairs a destroyed or damaged item, or repairs one point of armor in one location.

| Effect | On | Details |
| --- | --- | --- |
| Repairs equipment | target-equipment (benefit) | what one-item; instant; choice g1 option 1 |
| Repairs armor | hit-location (benefit) | amount one-point-one-location; instant; choice g1 option 2 |

**Capabilities:** repairs · **Roles:** equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/mend.md`](../../metadata/profiles/mend.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Archer](../classes/archer.md) | 2nd | - | - | 1/Life Charge x5 | Touch | no (ex) | Level table | - |
| [Bard](../classes/bard.md) | 2nd | 1 | - | 1/Life | Touch | yes | Spell table | - |
| [Druid](../classes/druid.md) | 1st | 1 | - | 1/Life | Touch | yes | Spell table | - |
| [Healer](../classes/healer.md) | 3rd | 1 | - | 1/Life | Touch | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 1st | 1 | - | 1/Life | Touch | yes | Spell table | - |

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

**These abilities name Mend in their text** (auto-detected). If Mend is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Apex](apex.md) | grants or gives | Scout |
| [Artificer](artificer.md) | changes its numbers | Archer |
| [Golem](golem.md) | mentions | Druid |
| [Sniper](sniper.md) | grants or gives | Archer |

**Shared with:** [Archer](../classes/archer.md), [Bard](../classes/bard.md), [Druid](../classes/druid.md), [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Archer** lists it at 2nd; nothing else is listed at that level. Archetypes that name it: Sniper, Artificer (archetypes are outside this model).
- **Bard** lists it at 2nd for 1 point. That level's table has 7 entries (9 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Druid** lists it at 1st for 1 point. That level's table has 7 entries (9 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Healer** lists it at 3rd for 1 point. That level's table has 9 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Wizard** lists it at 1st for 1 point. That level's table has 8 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
