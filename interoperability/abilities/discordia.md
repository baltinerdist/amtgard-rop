---
title: "Discordia — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Discordia
type: Enchantment
school: Command
targets_other_players: false
classes: ["Bard 5th"]
---

# Discordia — Interoperability

[Rule text](../../rules/magic-and-abilities/discordia.md) · **Enchantment** · Command School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **Indirect effects:** it grants [Break Concentration](break-concentration.md), which can affect other players; see those files for who they work on. This model does not compute the indirect effect itself.
- **On 1 class list:** Bard (5th).

## What it does

Self Enchantment with five strips: bearer may cast Break Concentration (m) by incanting and removing a strip; removed with the last strip.

| Effect | On | Details |
| --- | --- | --- |
| Casts Break Concentration from strips | bearer (benefit) | while worn; continuously while it is worn, chanted or in effect |
| Uses up a strip | bearer (neutral) | n 1; instant; when the bearer spends one of the Enchantment's strips |

**Capabilities:** grants-abilities · **Roles:** control, anti-magic

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/discordia.md`](../../metadata/profiles/discordia.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Bard](../classes/bard.md) | 5th | 1 | 1 | 1/Refresh | Self | yes | Spell table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**Discordia names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Break Concentration](break-concentration.md) | grants or gives | Bard, Wizard |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Bard** lists it at 5th for 1 point. That level's table has 7 entries (9 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
