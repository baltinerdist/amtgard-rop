---
title: "Phoenix Tears — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Phoenix Tears
type: Enchantment
school: Spirit
targets_other_players: true
classes: ["Healer 6th"]
---

# Phoenix Tears — Interoperability

[Rule text](../../rules/magic-and-abilities/phoenix-tears.md) · **Enchantment** · Spirit School · Range Self (Wa) Other (He)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Healer (6th).

## What it does

Instead of dying, bearer heals all wounds and is Frozen 30s; then loses Cursed, non-persistent Enchantments and a strip, repairs equipment; +1 Persistent Protection Enchantment.

| Effect | On | Details |
| --- | --- | --- |
| Prevents death | bearer (benefit) | instead heal-and-frozen; while worn; when the subject would die |
| Heals wounds | bearer (benefit) | amount all; instant; when the subject would die |
| Freezes | bearer (harm) | 30 s; when the subject would die |
| Ends Cursed | bearer (benefit) | what specific-state; instant; when an earlier State from this ability ends; only if the bearer still has the Enchantment |
| Repairs equipment | bearer-equipment (benefit) | what all-carried-equipment; instant; when an earlier State from this ability ends; only if the bearer still has the Enchantment |
| Removes Enchantments | bearer (harm) | scope non-persistent-others; instant; when an earlier State from this ability ends; only if the bearer still has the Enchantment |
| Uses up a strip | bearer (neutral) | n 1; instant; when an earlier State from this ability ends; only if the bearer still has the Enchantment |
| Allows extra Enchantments | bearer (benefit) | count 1; only protection-school; while worn; continuously while it is worn, chanted or in effect |
| Makes Enchantments Persistent | bearer (benefit) | which the-extra-enchantment; while worn; continuously while it is worn, chanted or in effect |
| Removes Enchantments | bearer (harm) | scope chosen-to-meet-limit; instant; when the Enchantment is removed |

**Capabilities:** cleanses, extra-enchantments, has-drawback, heals, more-uses, repairs, survives-death · **Roles:** defense, healing, equipment, resource

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/phoenix-tears.md`](../../metadata/profiles/phoenix-tears.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Healer](../classes/healer.md) | 6th | 1 | - | 1/Refresh | Other | yes | Spell table | - |

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

**Phoenix Tears names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Attuned](attuned.md) | mentions | Druid |
| [Essence Graft](essence-graft.md) | mentions | Druid |
| [Persistent](persistent.md) | mentions | Healer, Wizard |

**These abilities name Phoenix Tears in their text** (auto-detected). If Phoenix Tears is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Evolution](evolution.md) | mentions | Scout |
| [Juggernaut](juggernaut.md) | grants or gives | Warrior |
| [Sphere of Annihilation](sphere-of-annihilation.md) | mentions | Wizard |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Healer** lists it at 6th for 1 point. That level's table has 9 entries (11 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
