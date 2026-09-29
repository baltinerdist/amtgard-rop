---
title: "Persistent — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Persistent
type: Meta-Magic
school: Neutral
targets_other_players: false
classes: ["Healer 6th", "Wizard 6th"]
---

# Persistent — Interoperability

[Rule text](../../rules/magic-and-abilities/persistent.md) · **Meta-Magic** · Neutral School

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 2 class lists:** Healer (6th), Wizard (6th).

## What it does

Meta-Magic: the caster's next Enchantment returns with its bearer after respawning until otherwise removed, keeping remaining uses.

| Effect | On | Details |
| --- | --- | --- |
| Modifies the next ability cast | caster (benefit) | mode persistent-enchantment; until used |

**Capabilities:** - · **Roles:** utility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/persistent.md`](../../metadata/profiles/persistent.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Healer](../classes/healer.md) | 6th | 1 | - | 1/Life | - | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 6th | 2 | - | 1/Refresh | - | yes | Spell table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**Persistent names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Corrosive Mist](corrosive-mist.md) | mentions | Druid |
| [Mass Healing](mass-healing.md) | mentions | Healer |
| [Resurrect](resurrect.md) | mentions | Monk, Druid, Healer |

**These abilities name Persistent in their text** (auto-detected). If Persistent is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Golem](golem.md) | mentions | Druid |
| [Phoenix Tears](phoenix-tears.md) | mentions | Healer |
| [Protection from Evil](protection-from-evil.md) | mentions | Paladin |
| [Undead Minion](undead-minion.md) | mentions | Healer |

**Shared with:** [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Healer** lists it at 6th for 1 point. That level's table has 9 entries (11 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Wizard** lists it at 6th for 2 points. That level's table has 9 entries (14 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
