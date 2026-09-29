---
title: "Lost — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Lost
type: Verbal
school: Command
targets_other_players: true
classes: ["Bard 5th"]
---

# Lost — Interoperability

[Rule text](../../rules/magic-and-abilities/lost.md) · **Verbal** · Command School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 8 of 12 classes.
- **Blocked on:** Anti-Paladin, Barbarian, Monk, Paladin.
- **On 1 class list:** Bard (5th).

## What it does

Target within 20' becomes Insubstantial and must go directly to their base, ending the State on arrival; a Forced Movement effect.

| Effect | On | Details |
| --- | --- | --- |
| Makes Insubstantial | target (harm) | until arrival; only if the ability is cast on another player |
| Sends to base | target (harm) | until arrival; only if the ability is cast on another player |
| Makes Insubstantial | caster (benefit) | until arrival; only if the ability is cast on the caster |
| Sends to base | caster (benefit) | until arrival; only if the ability is cast on the caster |

**Capabilities:** makes-insubstantial, moves-others, moves-self, neutralizes, removes-from-play, self-protection-state · **Roles:** control, mobility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/lost.md`](../../metadata/profiles/lost.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Bard](../classes/bard.md) | 5th | 1 | - | 1/Life | 20' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | **Blocked** | Immune to Command |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | **Blocked** | Immune to Command |
| [Monk](../classes/monk.md) | **Blocked** | Enlightened Soul: unaffected by Verbal Magical abilities used beyond Touch (still works if cast at Touch) |
| [Paladin](../classes/paladin.md) | **Blocked** | Immune to Command |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

No other ability's text names it, and it names no other ability.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Bard** lists it at 5th for 1 point. That level's table has 7 entries (9 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is already too high for it.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
