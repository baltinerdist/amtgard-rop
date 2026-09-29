---
title: "Circle of Protection — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Circle of Protection
type: Verbal
school: Protection
targets_other_players: true
classes: ["Healer 4th"]
---

# Circle of Protection — Interoperability

[Rule text](../../rules/magic-and-abilities/circle-of-protection.md) · **Verbal** · Protection School · Range Touch

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Healer (4th).

## What it does

The caster and up to five willing players in Touch lose States and Ongoing Effects and become Insubstantial in place, safe from most Forced Movement.

| Effect | On | Details |
| --- | --- | --- |
| Removes States or Ongoing Effects | group (benefit) | what all-states-and-effects; instant |
| Makes Insubstantial | group (benefit) | until removed |
| May not move from start | group (harm) | what move-from-start; until removed; continuously while it is worn, chanted or in effect |
| Unaffected by | group (benefit) | by blink; until removed; continuously while it is worn, chanted or in effect |
| Unaffected by | group (benefit) | by forced-movement-except-banish; until removed; continuously while it is worn, chanted or in effect |
| Casts while Insubstantial | group (benefit) | on same-casting-targets; until removed; continuously while it is worn, chanted or in effect |

**Capabilities:** cleanses, has-drawback, holds-in-place, makes-insubstantial, neutralizes, protects, removes-from-play, restricts-others · **Roles:** defense, team

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/circle-of-protection.md`](../../metadata/profiles/circle-of-protection.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Healer](../classes/healer.md) | 4th | 1 | 1 | 1/Refresh Charge x10 | Touch | yes | Spell table | - |

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

**Circle of Protection names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Banish](banish.md) | mentions | Monk, Healer, Wizard |
| [Blink](blink.md) | mentions | Assassin |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Healer** lists it at 4th for 1 point. That level's table has 8 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
