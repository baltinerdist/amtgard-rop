---
title: "Terror — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Terror
type: Verbal
school: Death
targets_other_players: true
classes: ["Anti-Paladin 5th", "Bard 4th"]
---

# Terror — Interoperability

[Rule text](../../rules/magic-and-abilities/terror.md) · **Verbal** · Death School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 10 of 12 classes.
- **Blocked on:** Monk, Paladin.
- **On 2 class lists:** Anti-Paladin (5th), Bard (4th).

## What it does

For 30 seconds a target within 20' may not attack or cast Magical abilities at the caster or their equipment and must stay 50' away.

| Effect | On | Details |
| --- | --- | --- |
| May not attack caster | target (harm) | what attack-caster; 30 s |
| May not cast at caster | target (harm) | what cast-at-caster; 30 s |
| Must keep away | target (harm) | feet 50; from caster; except other-forced-movement; 30 s |

**Capabilities:** moves-others, restricts-others · **Roles:** control, defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/terror.md`](../../metadata/profiles/terror.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | 5th | - | - | 1/Life | 20' | yes | Level table | also the class's Look The Part, so the class has it from 1st level whatever level the table gives |
| [Bard](../classes/bard.md) | 4th | 1 | - | 1/Refresh | 20' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | **Blocked** | Enlightened Soul: unaffected by Verbal Magical abilities used beyond Touch (still works if cast at Touch) |
| [Paladin](../classes/paladin.md) | **Blocked** | Immune to Death |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

**These abilities name Terror in their text** (auto-detected). If Terror is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Corruptor](corruptor.md) | changes its numbers | Anti-Paladin |

**Shared with:** [Anti-Paladin](../classes/anti-paladin.md), [Bard](../classes/bard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Anti-Paladin** lists it at 5th; nothing else is listed at that level. It is also this class's Look The Part, so the class has it at 1st level regardless. Archetype that names it: Corruptor (archetypes are outside this model).
- **Bard** lists it at 4th for 1 point. That level's table has 9 entries (11 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
