---
title: "Song of Survival — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Song of Survival
type: Enchantment
school: Protection
targets_other_players: false
classes: ["Bard 5th"]
---

# Song of Survival — Interoperability

[Rule text](../../rules/magic-and-abilities/song-of-survival.md) · **Enchantment** · Protection School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 1 class list:** Bard (5th).

## What it does

While chanting, when the bearer would die they ignore it and become Insubstantial, in place or returning to base; once per life.

| Effect | On | Details |
| --- | --- | --- |
| Prevents death | bearer (benefit) | instead insubstantial; until used; when the subject would die |
| Makes Insubstantial | bearer (benefit) | until removed; when the bearer makes a stated choice; choice g1 option 1 |
| Makes Insubstantial | bearer (benefit) | until arrival; when the bearer makes a stated choice; choice g1 option 2 |
| Sends to base | bearer (benefit) | until arrival; when the bearer makes a stated choice; choice g1 option 2 |
| Ignores a hit | bearer (benefit) | from lethal-event; instant; when the subject would die |
| May not exit early | bearer (harm) | what exit-early; until arrival; when the bearer makes a stated choice; choice g1 option 2 |

**Capabilities:** has-drawback, makes-insubstantial, moves-self, protects, self-protection-state, survives-death · **Roles:** defense, mobility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/song-of-survival.md`](../../metadata/profiles/song-of-survival.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Bard](../classes/bard.md) | 5th | 1 | 1 | Unlimited | Self | yes | Spell table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

No other ability's text names it, and it names no other ability.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Bard** lists it at 5th for 1 point. That level's table has 7 entries (9 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
