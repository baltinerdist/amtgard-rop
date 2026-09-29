---
title: "Iceball — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Iceball
type: Magic Ball
school: Subdual
targets_other_players: true
classes: ["Druid 4th", "Healer 3rd", "Wizard 3rd"]
---

# Iceball — Interoperability

[Rule text](../../rules/magic-and-abilities/iceball.md) · **Magic Ball** · Subdual School

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Blocked on:** Barbarian.
- **On 3 class lists:** Druid (4th), Healer (3rd), Wizard (3rd).

## What it does

Engulfing Magic Ball: the player struck is Frozen for 60 seconds.

| Effect | On | Details |
| --- | --- | --- |
| Freezes | struck-player (harm) | 60 s; when a weapon, arrow or ball strikes the subject or their armor |

**Capabilities:** holds-in-place, neutralizes, removes-from-play, silences · **Roles:** control

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/iceball.md`](../../metadata/profiles/iceball.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Druid](../classes/druid.md) | 4th | 1 | 2 | 1 Ball / Unlimited | - | yes | Spell table | - |
| [Healer](../classes/healer.md) | 3rd | 1 | 3 | 1 Ball / Unlimited | - | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 3rd | 1 | 3 | 1 Ball / Unlimited | - | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | **Blocked** | Immune to Subdual |
| [Monk](../classes/monk.md) | Works |  |
| [Paladin](../classes/paladin.md) | Works |  |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

Monks can block Magic Balls and arrows with Missile Block, but that needs an active block, so it is shown as working.

## Connected abilities

**Shared with:** [Druid](../classes/druid.md), [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Druid** lists it at 4th for 1 point. That level's table has 8 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Healer** lists it at 3rd for 1 point. That level's table has 9 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Wizard** lists it at 3rd for 1 point. That level's table has 10 entries (10 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
