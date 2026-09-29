---
title: "Flame Blade — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Flame Blade
type: Enchantment
school: Flame
targets_other_players: true
classes: ["Anti-Paladin 6th", "Druid 4th"]
---

# Flame Blade — Interoperability

[Rule text](../../rules/magic-and-abilities/flame-blade.md) · **Enchantment** · Flame School · Range Self (Ap) Other (Dr)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Anti-Paladin (6th), Druid (4th).

## What it does

Bearer's wielded melee weapons are Armor Breaking and Shield Crushing; bearer and their wielded weapons are Immune to Flame.

| Effect | On | Details |
| --- | --- | --- |
| Armor Breaking (bearer melee weapons) | bearer (benefit) | on bearer-melee-weapons; while worn; continuously while it is worn, chanted or in effect |
| Shield Crushing (bearer melee weapons) | bearer (benefit) | on bearer-melee-weapons; while worn; continuously while it is worn, chanted or in effect |
| Immune to Flame | bearer (benefit) | while worn; continuously while it is worn, chanted or in effect |
| Immune to Flame | bearer-equipment (benefit) | while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** attacks-equipment, defeats-armor, protects · **Roles:** offense, equipment, defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/flame-blade.md`](../../metadata/profiles/flame-blade.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | 6th | - | - | 2/Refresh | Self | no (ex) | Level table | - |
| [Druid](../classes/druid.md) | 4th | 2 | 2 | 1/Refresh | Other | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works | Enchantments apply despite Immunity (Enchantments rule 3) |
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

**These abilities name Flame Blade in their text** (auto-detected). If Flame Blade is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Corruptor](corruptor.md) | removes | Anti-Paladin |
| [Infernal](infernal.md) | changes its numbers | Anti-Paladin |
| [Pyrotechnics](pyrotechnics.md) | mentions | Wizard |

**Shared with:** [Anti-Paladin](../classes/anti-paladin.md), [Druid](../classes/druid.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

**Grants immunity:** the effect text says the bearer is Immune to Flame. That immunity would stop any targeting ability of that School.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Anti-Paladin** lists it at 6th; nothing else is listed at that level. Archetypes that name it: Infernal, Corruptor (archetypes are outside this model).
- **Druid** lists it at 4th for 2 points. That level's table has 8 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
