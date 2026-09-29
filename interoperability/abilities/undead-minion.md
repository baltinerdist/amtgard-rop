---
title: "Undead Minion — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Undead Minion
type: Enchantment
school: Death
targets_other_players: true
classes: ["Healer 5th"]
---

# Undead Minion — Interoperability

[Rule text](../../rules/magic-and-abilities/undead-minion.md) · **Enchantment** · Death School · Range Other

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Partly blocked on:** Paladin (enchantment applies, granted Raise Dead cannot).
- **On 1 class list:** Healer (5th).

## What it does

Bearer is Cursed and cannot respawn; caster gains unlimited Raise Dead on the bearer only; up to three per caster; Persistent.

| Effect | On | Details |
| --- | --- | --- |
| Curses | bearer (harm) | while worn; continuously while it is worn, chanted or in effect |
| Prevents respawning | bearer (harm) | while worn; continuously while it is worn, chanted or in effect |
| Grants Raise Dead | caster-of-enchantment (benefit) | how gains; frequency (Unlimited) (m); while worn; continuously while it is worn, chanted or in effect |
| Changes Raise Dead | caster-of-enchantment (benefit) | change the granted Raise Dead ignores the requirement that the target has not moved from where they died; while worn; continuously while it is worn, chanted or in effect |
| Changes Raise Dead | caster-of-enchantment (harm) | change the granted Raise Dead can only be cast with the bearer as the target; while worn; continuously while it is worn, chanted or in effect |
| Acts as an Alternate Base | caster-of-enchantment (neutral) | for bearer-only; while worn; continuously while it is worn, chanted or in effect |
| May not use alternate bases | caster-of-enchantment (harm) | what use-alternate-bases; while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** grants-abilities, has-drawback, team-base · **Roles:** revival, utility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/undead-minion.md`](../../metadata/profiles/undead-minion.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Healer](../classes/healer.md) | 5th | 2 | - | 1/Refresh | Other | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works |  |
| [Paladin](../classes/paladin.md) | **Partly blocked:** enchantment applies, granted Raise Dead cannot | Immune to Death. The enchantment itself applies (Enchantments rule 3), but the Raise Dead it grants is affected normally by Immunity (rule 3b) |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

Touch and Other range also need the target to be willing, dead, stunned, frozen or Insubstantial and unable to move. That applies to every class alike and is not modelled.

## Connected abilities

**Undead Minion names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Persistent](persistent.md) | mentions | Healer, Wizard |
| [Raise Dead](raise-dead.md) | grants or gives | Healer |

**These abilities name Undead Minion in their text** (auto-detected). If Undead Minion is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Necromancer](necromancer.md) | mentions | Healer |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Healer** lists it at 5th for 2 points. That level's table has 7 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). Archetype that names it: Necromancer (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
