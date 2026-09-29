---
title: "Mass Healing — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Mass Healing
type: Enchantment
school: Spirit
targets_other_players: false
classes: ["Healer 6th"]
---

# Mass Healing — Interoperability

[Rule text](../../rules/magic-and-abilities/mass-healing.md) · **Enchantment** · Spirit School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **Indirect effects:** it grants [Heal](heal.md), which can affect other players; see those files for who they work on. This model does not compute the indirect effect itself.
- **On 1 class list:** Healer (6th).

## What it does

Self Enchantment with five strips: caster may Heal (m) a player at Touch by declaring "I grant thee healing" and removing a strip.

| Effect | On | Details |
| --- | --- | --- |
| Casts Heal from strips | bearer (benefit) | while worn; continuously while it is worn, chanted or in effect |
| Casts by declaration | bearer (benefit) | what Heal (m) at Touch, by declaring "I grant thee healing"; while worn; continuously while it is worn, chanted or in effect |
| Uses up a strip | bearer (neutral) | n 1; instant; when the bearer spends one of the Enchantment's strips |

**Capabilities:** castable-while-moving, grants-abilities · **Roles:** healing

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/mass-healing.md`](../../metadata/profiles/mass-healing.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Healer](../classes/healer.md) | 6th | 1 | 1 | 1/Refresh | Self | yes | Spell table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**Mass Healing names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Heal](heal.md) | grants or gives | Monk, Scout, Druid, Healer |

**These abilities name Mass Healing in their text** (auto-detected). If Mass Healing is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Persistent](persistent.md) | mentions | Healer, Wizard |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Healer** lists it at 6th for 1 point. That level's table has 9 entries (11 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
