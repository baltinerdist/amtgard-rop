---
title: "Sever Spirit"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Sever Spirit

> Curses a dead player within 20' and removes all their Enchantments, regardless of Traits, States, Immunities or Enchantments.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Spirit |
| Range | 20' |
| Incantation | "The spirits lay a curse on thee." x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | debuff, anti-magic · for: enemy |
| Capabilities | curses, dispels |
| Rule text | [rules/magic-and-abilities/sever-spirit.md](../../rules/magic-and-abilities/sever-spirit.md) · [interoperability](../../interoperability/abilities/sever-spirit.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Healer | 2nd | 1 | - | 1/Life Charge x3 | 1 | life | x3 | (m) | 20' | - |
| Monk | 6th | - | - | - | - | - | - | - | - | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Curses** | dead-target | harm | until respawn — No duration given; per the Cursed State it persists after death and is removed on respawn. | E1 |
| e2 | **Removes Enchantments** | dead-target | harm | scope all; instant — Always removes Enchantments if successfully cast on a valid target, regardless of the player's Traits, States, Immunities, Ongoing Effects or Enchantments (E3). | E2, E3 |

## Requirements

- **target-dead**: target must be dead *(E1)*
- **target-dead-at-start**: target must be dead when the incantation begins *(L1)*

## Properties

- **bypass-traits**: works regardless of Traits — The Enchantment removal only. *(E3)*
- **bypass-states**: works regardless of States — The Enchantment removal only. *(E3)*
- **bypass-immunities**: works regardless of Immunities — The Enchantment removal only. *(E3)*
- **bypass-ongoing-effects**: works regardless of Ongoing Effects — The Enchantment removal only. *(E3)*
- **bypass-enchantments**: ignores Enchantments — The Enchantment removal only: the player's own Enchantments cannot stop it. *(E3)*

## Clarifications in the text

- If Sever Spirit is successfully cast on a valid target it always removes Enchantments, whatever the player's Traits, States, Immunities, Ongoing Effects or Enchantments. *(E3)*

## Names in the text

- state **cursed**: mentions *(E1)*
- mechanic **enchantments**: mentions *(E2, E3)*
- mechanic **traits**: mentions *(E3)*
- mechanic **immune**: mentions *(E3)*
- mechanic **ongoing-effects**: mentions *(E3)*
- mechanic **incantation**: mentions *(L1)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Sleight of Mind](sleight-of-mind.md) | Enchantments cannot be removed | Bard |
| [Blessed Aura](blessed-aura.md) | Resistant to the next source | Healer |
| [Blessing Against Harm](blessing-against-harm.md) | Resistant to the next source | Healer, Wizard |
| [Sanctuary](sanctuary.md) | Unaffected by hostile actions within 20ft | Monk |
| [Protection from Magic](protection-from-magic.md) | Unaffected by magical abilities | Healer, Paladin, Wizard |
| [Void Touched](void-touched.md) | Unaffected by schools | Anti-Paladin, Wizard |
| [Rage](rage.md) | Unaffected by verbal abilities | Barbarian |
| [Enlightened Soul](enlightened-soul.md) | Unaffected by verbal magical beyond touch | Healer, Monk |
| [Enlightened Soul](enlightened-soul.md) | Unaffected by verbal magical beyond touch | Healer, Monk |

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| is given by | [Medium](medium.md) | only Sever Spirit: Curses (dead-target, until respawn); only Sever Spirit: Removes Enchantments (dead-target, instant); only Medium: Grants Blessing Against Wounds (bearer, permanent); only Medium: Grants Sever Spirit (bearer, permanent); only Medium: Grants Swift (bearer, permanent); only Medium: Changes how often abilities can be used (bearer, permanent); only Medium: May not wear armor (bearer, permanent); only Medium: May not wield great weapons (bearer, permanent) |
| overlap | [Assassinate](assassinate.md) | only Sever Spirit: Removes Enchantments (dead-target, instant); requirement only in Sever Spirit: target-dead-at-start; requirement only in Assassinate: immediately-after-kill; property only in Sever Spirit: bypass-enchantments, bypass-immunities, bypass-ongoing-effects, bypass-states, bypass-traits; property only in Assassinate: no-verbal-targeting; school: Spirit vs Death; range: 20' vs 50' |
| overlap | [Dispel Magic](dispel-magic.md) | only Sever Spirit: Curses (dead-target, until respawn); requirement only in Sever Spirit: target-dead, target-dead-at-start; requirement only in Dispel Magic: target-not-invulnerable; school: Spirit vs Sorcery |

## Open questions

- E3's 'regardless of ...' guarantee is stated only for removing Enchantments, not for the Curse; the bypass properties are noted as applying to the removal only.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target dead player is Cursed. | effect e1 (Curses); requirement target-dead; names cursed |
| E2 | Any Enchantments on the player are removed. | effect e2 (Removes Enchantments); names enchantments |
| E3 | Will always remove enchantments if successfully cast on a valid target, regardless of the player's Traits, States, Immunities, Ongoing Effects, or Enchantments. | effect e2 (Removes Enchantments); property bypass-traits; property bypass-states; property bypass-immunities; property bypass-ongoing-effects; property bypass-enchantments; names enchantments; names traits; names immune; names ongoing-effects; clarification |
| L1 | Target must be dead when the caster begins the Incantation. | requirement target-dead-at-start; names incantation |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/sever-spirit.json` and the V8.08 "Spongy" rules.*
