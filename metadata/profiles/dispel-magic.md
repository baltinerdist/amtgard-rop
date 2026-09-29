---
title: "Dispel Magic"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Dispel Magic

> Removes all Enchantments from a target within 20', regardless of Traits, States, Immunities or Enchantments, except Sleight of Mind; not on Invulnerable players.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Sorcery |
| Range | 20' |
| Incantation | "By my power I dispel thy magic" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | anti-magic · for: any |
| Capabilities | dispels |
| Rule text | [rules/magic-and-abilities/dispel-magic.md](../../rules/magic-and-abilities/dispel-magic.md) · [interoperability](../../interoperability/abilities/dispel-magic.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Scout | 3rd | - | - | 1/Refresh Charge x5 | 1 | refresh | x5 | (ex) | 20' | - |
| Druid | 3rd | 1 | - | 1/Refresh | 1 | refresh | - | (m) | 20' | - |
| Healer | 4th | 1 | - | 1/Refresh | 1 | refresh | - | (m) | 20' | - |
| Wizard | 3rd | 1 | - | 1/Refresh Charge x3 | 1 | refresh | x3 | (m) | 20' | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Removes Enchantments** | target | harm | scope all; instant — Polarity 'harm' for the usual use against an enemy; it can also be used to strip a friendly player's Enchantments. | E1, E2 |

## Requirements

- **target-not-invulnerable**: does not affect Invulnerable targets *(N1)*

## Properties

- **bypass-traits**: works regardless of Traits *(E2)*
- **bypass-states**: works regardless of States *(E2)*
- **bypass-immunities**: works regardless of Immunities *(E2)*
- **bypass-enchantments**: ignores Enchantments — Regardless of the target's Enchantments, except Sleight of Mind. *(E2)*
- **bypass-ongoing-effects**: works regardless of Ongoing Effects *(E2)*

## Clarifications in the text

- If successfully cast on a valid target it always removes Enchantments, whatever the player's Traits, States, Immunities, Ongoing Effects or Enchantments, except Sleight of Mind. *(E2)*

## Names in the text

- ability **[Sleight of Mind](sleight-of-mind.md)**: countered-by *(E2)*
- state **invulnerable**: mentions *(N1)*
- mechanic **enchantments**: mentions *(E1, E2)*
- mechanic **traits**: mentions *(E2)*
- mechanic **immune**: mentions *(E2)*
- mechanic **ongoing-effects**: mentions *(E2)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Sleight of Mind](sleight-of-mind.md) | Enchantments cannot be removed | Bard |
| [Adaptive Protection](adaptive-protection.md) | Immune (chosen School) | Healer, Scout |
| [Adaptive Blessing](adaptive-blessing.md) | Resistant (chosen School, next ability) | Healer |
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
| is given by | [Naturalize Magic](naturalize-magic.md) | only Dispel Magic: Removes Enchantments (target, instant); only Naturalize Magic: Casts Dispel Magic from strips (bearer, while worn); only Naturalize Magic: Uses up a strip (bearer, instant); requirement only in Dispel Magic: target-not-invulnerable; ends when only in Naturalize Magic: last-strip; property only in Dispel Magic: bypass-enchantments, bypass-immunities, bypass-ongoing-effects, bypass-states, bypass-traits; property only in Naturalize Magic: materials-required, uses-strips; delivery: verbal vs enchantment |
| overlap | [Sever Spirit](sever-spirit.md) | only Sever Spirit: Curses (dead-target, until respawn); requirement only in Dispel Magic: target-not-invulnerable; requirement only in Sever Spirit: target-dead, target-dead-at-start; school: Sorcery vs Spirit |

## Open questions

- E2 says it works regardless of the target's States, but N1 says it does not affect Invulnerable players (Invulnerable is a State); encoded N1 as the requirement target-not-invulnerable as the specific exception.
- E2 'valid target' is not defined further.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | All Enchantments on target are removed. | effect e1 (Removes Enchantments); names enchantments |
| E2 | Will always remove Enchantments if successfully cast on a valid target, regardless of the player's Traits, States, Immunities, Ongoing Effects, or Enchantments (except Sleight of Mind). | effect e1 (Removes Enchantments); property bypass-traits; property bypass-states; property bypass-immunities; property bypass-enchantments; property bypass-ongoing-effects; names Sleight of Mind; names enchantments; names traits; names immune; names ongoing-effects; clarification |
| N1 | Does not affect Invulnerable players. | requirement target-not-invulnerable; names invulnerable |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/dispel-magic.json` and the V8.08 "Spongy" rules.*
