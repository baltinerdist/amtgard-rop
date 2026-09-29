---
title: "Destroy Armor"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Destroy Armor

> Removes all armor points from a named hit location on a target within 20'; only armor-specific protections like Blessed Aura stop it.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Death |
| Range | 20' |
| Incantation | "Death destroys thy [hit location] armor" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | equipment, debuff · for: enemy |
| Capabilities | defeats-armor |
| Rule text | [rules/magic-and-abilities/destroy-armor.md](../../rules/magic-and-abilities/destroy-armor.md) · [interoperability](../../interoperability/abilities/destroy-armor.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wizard | 4th | 1 | - | 2/Refresh | 2 | refresh | - | (m) | 20' | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Destroys armor** | hit-location | harm | scope one-location; instant — The caster names the hit location in the Incantation. | E1, N1 |

## Properties

- **targets-player-affects-equipment**: targets the player but affects their equipment or armor — Targets the player but affects the armor on the hit location. *(N1)*
- **personal-protections-do-not-cover-equipment**: protections only stop it if they specifically extend to armor or equipment — Immunities, Resistances and other protections only protect the armor if they specifically extend to it (e.g. Blessed Aura). *(N3, N4, N5)*

## Clarifications in the text

- Visibility (line of sight) may be drawn to any part of the target player, not only the chosen hit location. *(N2)*
- Immunities, Resistances and other protections protect the armor only if they specifically extend to armor, such as Blessed Aura. *(N3)*
- Enlightened Soul, Protection from Magic and Adaptive Protection (Death) do not extend to armor and cannot protect against it. *(N4)*
- Ancestral Armor does not protect against verbal magic, so it cannot protect against Destroy Armor. *(N5)*

## Names in the text

- ability **[Blessed Aura](blessed-aura.md)**: countered-by *(N3)*
- ability **[Enlightened Soul](enlightened-soul.md)**: mentions *(N4)*
- ability **[Protection from Magic](protection-from-magic.md)**: mentions *(N4)*
- ability **[Adaptive Protection](adaptive-protection.md)**: mentions *(N4)*
- ability **[Ancestral Armor](ancestral-armor.md)**: mentions *(N5)*
- mechanic **armor**: mentions *(E1, N3)*
- mechanic **immune**: mentions *(N3)*
- mechanic **resistant**: mentions *(N3)*
- mechanic **verbal**: mentions *(N5)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Golem](golem.md) | Immune | Druid |
| [Immune to Death](immune-to-death.md) | Immune | Paladin |
| [Protection from Evil](protection-from-evil.md) | Immune | Paladin |
| [Vampirism](vampirism.md) | Immune | Wizard |
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
| is given by | [Corrosive Mist](corrosive-mist.md) | only Destroy Armor: Destroys armor (hit-location, instant); only Corrosive Mist: Casts Destroy Armor from strips (bearer, while worn); only Corrosive Mist: Uses up a strip (bearer, instant); ends when only in Corrosive Mist: last-strip; property only in Destroy Armor: personal-protections-do-not-cover-equipment, targets-player-affects-equipment; property only in Corrosive Mist: materials-required, uses-strips; delivery: verbal vs enchantment; range: 20' vs Touch |

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Remove all armor points from target hit location. | effect e1 (Destroys armor); names armor |
| N1 | Destroy Armor targets the player but affects the hit location. | effect e1 (Destroys armor); property targets-player-affects-equipment |
| N2 | Visibility can be drawn to any part of the player, not just the desired hit location. | clarification |
| N3 | Immunities, resistances, and other protections will only protect the armor from Destroy Armor if they specifically extend to the armor, such as Blessed Aura. | property personal-protections-do-not-cover-equipment; names Blessed Aura; names armor; names immune; names resistant; clarification |
| N4 | Abilities like Enlightened Soul, Protection from Magic, and Adaptive Protection (Death) do not extend to armor and thus cannot protect against Destroy Armor. | property personal-protections-do-not-cover-equipment; names Enlightened Soul; names Protection from Magic; names Adaptive Protection; clarification |
| N5 | Ancestral Armor does not protect against verbal magic and thus cannot protect against Destroy Armor. | property personal-protections-do-not-cover-equipment; names Ancestral Armor; names verbal; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/destroy-armor.json` and the V8.08 "Spongy" rules.*
