---
title: "Song of Visit — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Song of Visit
type: Enchantment
school: Protection
targets_other_players: false
classes: ["Bard 2nd"]
---

# Song of Visit — Interoperability

[Rule text](../../rules/magic-and-abilities/song-of-visit.md) · **Enchantment** · Protection School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 1 class list:** Bard (2nd).

## What it does

While chanting, the bearer is Stopped and Invulnerable; when the song ends they stay Invulnerable and must go directly to base.

| Effect | On | Details |
| --- | --- | --- |
| Stops | bearer (harm) | while chanting; continuously while it is worn, chanted or in effect |
| Makes Invulnerable | bearer (benefit) | while chanting; continuously while it is worn, chanted or in effect |
| Makes Invulnerable | bearer (benefit) | until arrival; when the Enchantment is removed |
| Sends to base | bearer (harm) | until arrival; when the Enchantment is removed |
| May not impede play | bearer (harm) | what impede-play; while chanting; continuously while it is worn, chanted or in effect |

**Capabilities:** has-drawback, moves-self, self-protection-state · **Roles:** defense, utility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/song-of-visit.md`](../../metadata/profiles/song-of-visit.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Bard](../classes/bard.md) | 2nd | 1 | 1 | Unlimited | Self | yes | Spell table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

No other ability's text names it, and it names no other ability.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Bard** lists it at 2nd for 1 point. That level's table has 7 entries (9 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
