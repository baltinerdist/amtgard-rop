---
title: "Trickery — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Trickery
type: Enchantment
school: Sorcery
targets_other_players: false
classes: ["Assassin 1st"]
---

# Trickery — Interoperability

[Rule text](../../rules/magic-and-abilities/trickery.md) · **Enchantment** · Sorcery School · Range Self

## Summary

- **Can affect another player:** no (it is a Trait), so it has no works/blocked results. It can still be shared between classes.
- **Indirect effects:** it grants [Teleport](teleport.md), which can affect other players; see those files for who they work on. This model does not compute the indirect effect itself.
- **On 1 class list:** Assassin (1st).

## What it does

Bearer may cast Blink, Shadow Step and Teleport on themselves while already Insubstantial from a State they caused and entered voluntarily.

| Effect | On | Details |
| --- | --- | --- |
| Casts while Insubstantial | bearer (benefit) | abilities Blink, Shadow Step, Teleport; on self; permanent; continuously while it is worn, chanted or in effect; only if the caster caused (and voluntarily entered) the existing State |
| Ends Insubstantial | bearer (neutral) | what specific-state; instant; when the bearer makes a stated choice |

**Capabilities:** cleanses · **Roles:** mobility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/trickery.md`](../../metadata/profiles/trickery.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Assassin](../classes/assassin.md) | 1st | - | - | - | Self | n/a (Trait) | Level table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**Trickery names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Blink](blink.md) | grants or gives | Assassin |
| [Shadow Step](shadow-step.md) | grants or gives | Assassin, Scout |
| [Teleport](teleport.md) | grants or gives | Assassin, Druid, Healer, Wizard |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Assassin** lists it at 1st; 2 other entries share that level: Assassinate, Shadow Step.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
