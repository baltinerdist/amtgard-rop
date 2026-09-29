---
title: "Gift of Air — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Gift of Air
type: Enchantment
school: Protection
targets_other_players: true
classes: ["Druid 5th"]
---

# Gift of Air — Interoperability

[Rule text](../../rules/magic-and-abilities/gift-of-air.md) · **Enchantment** · Protection School · Range Other

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Druid (5th).

## What it does

Ignores a weapon or arrow hit on the bearer, who becomes Insubstantial in place or returning to base; bearer may not wield weapons or Shields.

| Effect | On | Details |
| --- | --- | --- |
| Ignores a hit | bearer (benefit) | from weapons-and-arrows; except effects siege, armor-breaking, armor-destroying, shield-crushing, shield-destroying; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Makes Insubstantial | bearer (benefit) | until removed; when the bearer makes a stated choice; choice g1 option 1 |
| Makes Insubstantial | bearer (benefit) | until arrival; when the bearer makes a stated choice; choice g1 option 2 |
| Sends to base | bearer (benefit) | until arrival; when the bearer makes a stated choice; choice g1 option 2 |
| May not exit early | bearer (harm) | what exit-early; until arrival; when the bearer makes a stated choice; choice g1 option 2 |
| May not wield weapons | bearer (harm) | what wield-weapons; while worn; continuously while it is worn, chanted or in effect |
| May not wield shields | bearer (harm) | what wield-shields; while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** has-drawback, makes-insubstantial, moves-self, protects, self-protection-state · **Roles:** defense, mobility, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/gift-of-air.md`](../../metadata/profiles/gift-of-air.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Druid](../classes/druid.md) | 5th | 1 | 2 | 1/Refresh | Other | yes | Spell table | - |

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

**These abilities name Gift of Air in their text** (auto-detected). If Gift of Air is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Planar Grounding](planar-grounding.md) | mentions | Wizard |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Druid** lists it at 5th for 1 point. That level's table has 9 entries (14 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
