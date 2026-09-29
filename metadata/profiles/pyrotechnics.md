---
title: "Pyrotechnics"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Pyrotechnics

> Destroys all weapons and shields carried by a target within 50' when the Verbal completes; only equipment-specific protections stop it.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Flame |
| Range | 50' |
| Incantation | "I call upon the element of flame to destroy thy belongings" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | equipment · for: enemy |
| Capabilities | attacks-equipment |
| Rule text | [rules/magic-and-abilities/pyrotechnics.md](../../rules/magic-and-abilities/pyrotechnics.md) · [interoperability](../../interoperability/abilities/pyrotechnics.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wizard | 5th | 1 | 2 | 1/Refresh | 1 | refresh | - | (m) | 50' | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Destroys equipment** | target | harm | what weapons-and-shields; instant — Only weapons and shields carried when the Verbal is completed. | E1, L1, N1 |

## Properties

- **targets-player-affects-equipment**: targets the player but affects their equipment or armor *(N1)*
- **personal-protections-do-not-cover-equipment**: protections only stop it if they specifically extend to armor or equipment — Immunities, Resistances and other protections stop it only if they specifically extend to equipment (e.g. Blessed Aura, Flame Blade); Enlightened Soul, Protection from Magic and Adaptive Protection (Flame) do not. *(N2, N3)*

## Clarifications in the text

- Only shields and weapons carried at the moment the Verbal is completed are destroyed. *(L1)*
- Immunities, Resistances and other protections protect the equipment only if they specifically extend to equipment, such as Blessed Aura or Flame Blade. *(N2)*
- Enlightened Soul, Protection from Magic and Adaptive Protection (Flame) do not extend to equipment and cannot protect from it. *(N3)*

## Names in the text

- ability **[Blessed Aura](blessed-aura.md)**: countered-by *(N2)*
- ability **[Flame Blade](flame-blade.md)**: countered-by *(N2)*
- ability **[Enlightened Soul](enlightened-soul.md)**: mentions *(N3)*
- ability **[Protection from Magic](protection-from-magic.md)**: mentions *(N3)*
- ability **[Adaptive Protection](adaptive-protection.md)**: mentions *(N3)*
- mechanic **weapon**: mentions *(E1, L1)*
- mechanic **shield**: mentions *(E1, L1)*
- mechanic **immune**: mentions *(N2)*
- mechanic **resistant**: mentions *(N2)*
- mechanic **verbal**: mentions *(L1)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Flame Blade](flame-blade.md) | Immune | Anti-Paladin, Druid |
| [Gift of Fire](gift-of-fire.md) | Immune | Druid |
| [Immune to Flame](immune-to-flame.md) | Immune | Anti-Paladin |
| [Ironskin](ironskin.md) | Immune | Druid |
| [Adaptive Protection](adaptive-protection.md) | Immune (chosen School) | Healer, Scout |
| [Adaptive Blessing](adaptive-blessing.md) | Resistant (chosen School, next ability) | Healer |
| [Blessed Aura](blessed-aura.md) | Resistant to the next source | Healer |
| [Blessing Against Harm](blessing-against-harm.md) | Resistant to the next source | Healer, Wizard |
| [Sanctuary](sanctuary.md) | Unaffected by hostile actions within 20ft | Monk |
| [Protection from Magic](protection-from-magic.md) | Unaffected by magical abilities | Healer, Paladin, Wizard |
| [Rage](rage.md) | Unaffected by verbal abilities | Barbarian |
| [Enlightened Soul](enlightened-soul.md) | Unaffected by verbal magical beyond touch | Healer, Monk |
| [Enlightened Soul](enlightened-soul.md) | Unaffected by verbal magical beyond touch | Healer, Monk |

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | All shields and weapons carried by the target player are destroyed. | effect e1 (Destroys equipment); names weapon; names shield |
| L1 | Only affects shields and weapons carried when the Verbal is completed. | effect e1 (Destroys equipment); names weapon; names shield; names verbal; clarification |
| N1 | Pyrotechnics targets the player but affects their equipment. | effect e1 (Destroys equipment); property targets-player-affects-equipment |
| N2 | Immunities, resistances, and other protections will only protect the equipment from Pyrotechnics if they specifically extend to the equipment, such as Blessed Aura or Flame Blade. | property personal-protections-do-not-cover-equipment; names Blessed Aura; names Flame Blade; names immune; names resistant; clarification |
| N3 | Abilities like Enlightened Soul, Protection from Magic, and Adaptive Protection (Flame) do not extend to equipment and thus cannot protect from Pyrotechnics. | property personal-protections-do-not-cover-equipment; names Enlightened Soul; names Protection from Magic; names Adaptive Protection; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/pyrotechnics.json` and the V8.08 "Spongy" rules.*
