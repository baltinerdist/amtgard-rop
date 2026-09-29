---
title: "Golem — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Golem
type: Enchantment
school: Sorcery
targets_other_players: true
classes: ["Druid 4th"]
---

# Golem — Interoperability

[Rule text](../../rules/magic-and-abilities/golem.md) · **Enchantment** · Sorcery School · Range Other

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Druid (4th).

## What it does

Bearer is Immune to Death and Cursed, Mend removes their wounds, their Enchantments are Persistent, and they may respawn at or base on the caster.

| Effect | On | Details |
| --- | --- | --- |
| Immune to Death | bearer (benefit) | while worn; continuously while it is worn, chanted or in effect |
| Curses | bearer (harm) | while worn; continuously while it is worn, chanted or in effect |
| Changes Mend | bearer (benefit) | change Mend can remove a wound from the bearer; while worn; continuously while it is worn, chanted or in effect |
| Heals wounds | bearer (benefit) | amount one; instant; continuously while it is worn, chanted or in effect |
| Acts as a respawn point | caster-of-enchantment (neutral) | for bearer-only; while worn; continuously while it is worn, chanted or in effect; only if while the caster is alive |
| Acts as an Alternate Base | caster-of-enchantment (neutral) | for bearer-only; while worn; continuously while it is worn, chanted or in effect |
| Makes Enchantments Persistent | bearer (benefit) | which all-worn; while worn; continuously while it is worn, chanted or in effect |
| May not use alternate bases | caster-of-enchantment (harm) | what use-alternate-bases; while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** has-drawback, heals, protects, team-base · **Roles:** defense, healing, utility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/golem.md`](../../metadata/profiles/golem.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Druid](../classes/druid.md) | 4th | 1 | - | 1/Refresh | Other | yes | Spell table | - |

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

**Golem names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Greater Mend](greater-mend.md) | mentions | Druid, Wizard |
| [Mend](mend.md) | mentions | Archer, Bard, Druid, Healer, Wizard |
| [Persistent](persistent.md) | mentions | Healer, Wizard |
| [Word of Mending](word-of-mending.md) | mentions | Druid, Wizard |

**These abilities name Golem in their text** (auto-detected). If Golem is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Avatar of Nature](avatar-of-nature.md) | mentions | Druid |

**Grants immunity:** the effect text says the bearer is Immune to Death. That immunity would stop any targeting ability of that School.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Druid** lists it at 4th for 1 point. That level's table has 8 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). Archetype that names it: Avatar of Nature (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
