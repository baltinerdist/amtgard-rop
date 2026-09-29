---
title: "Insult"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Insult

> For 30 seconds or until either dies, a target within 20' may attack or cast Magic only at the caster, unless others attack them.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Command |
| Range | 20' |
| Incantation | "I command thy attention" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | control · for: enemy |
| Capabilities | castable-while-moving, restricts-others |
| Rule text | [rules/magic-and-abilities/insult.md](../../rules/magic-and-abilities/insult.md) · [interoperability](../../interoperability/abilities/insult.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Warrior | 4th | - | - | 1/Life | 1 | life | - | (m) | 20' | Ambulant |
| Bard | 1st | 1 | - | 1/Life | 1 | life | - | (m) | 20' | - |
| Warrior | 1st | - | - | - | - | - | - | - | - | Look The Part |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **May not attack anyone but caster** | target | harm | what attack-anyone-but-caster; 30 s — May attack only the caster or the caster's carried equipment. Per E2, anyone other than the caster who attacks the target or casts Magical abilities on the target or their carried equipment may also be attacked, at the target's choice. | E1, E2 |
| e2 | **May not cast at anyone but caster** | target | harm | what cast-at-anyone-but-caster; 30 s — Magical abilities only; may cast only at the caster or their carried equipment. Charging and throwing Magic Balls at the caster remain allowed (N1). | E1, N1 |

## How it ends early

- **either-dies**: ends if the caster or the target dies — Ends if the caster or the target dies. *(E1)*

## Properties

- **has-choice**: the subject chooses between options — Once attacked or cast on by someone other than the caster, the target may choose to attack that offending party as well. *(E2)*

## Clarifications in the text

- If someone other than the caster attacks the target or casts Magical abilities on them or their carried equipment, the target may choose to attack that offending party as well. *(E2)*
- The target may still charge and throw Magic Balls at the caster. *(N1)*

## Names in the text

- mechanic **charge**: mentions *(N1)*
- mechanic **magic-balls**: mentions *(N1)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Immune to Command](immune-to-command.md) | Immune | Anti-Paladin, Barbarian, Paladin |
| [Lycanthropy](lycanthropy.md) | Immune | Druid |
| [Song of Determination](song-of-determination.md) | Immune | Bard |
| [Adaptive Protection](adaptive-protection.md) | Immune (chosen School) | Healer, Scout |
| [Adaptive Blessing](adaptive-blessing.md) | Resistant (chosen School, next ability) | Healer |
| [Blessed Aura](blessed-aura.md) | Resistant to the next source | Healer |
| [Blessing Against Harm](blessing-against-harm.md) | Resistant to the next source | Healer, Wizard |
| [Sanctuary](sanctuary.md) | Unaffected by hostile actions within 20ft | Monk |
| [Protection from Magic](protection-from-magic.md) | Unaffected by magical abilities | Healer, Paladin, Wizard |
| [Rage](rage.md) | Unaffected by verbal abilities | Barbarian |
| [Enlightened Soul](enlightened-soul.md) | Unaffected by verbal magical beyond touch | Healer, Monk |
| [Enlightened Soul](enlightened-soul.md) | Unaffected by verbal magical beyond touch | Healer, Monk |

## Open questions

- E2 lets the target 'attack' the offending party; it does not say whether the target may also cast Magical abilities at them. Encoded literally (attack only).
- N1 'charge' may mean the Charge incantation or physically charging at the caster; referenced the charge mechanic.
- E1 restricts only Magical abilities; Extraordinary abilities cast at others are not restricted, literally.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target is unable to attack or cast Magical abilities at anyone other than the caster or their carried equipment for 30 seconds, or until either party dies. | effect e1 (May not attack anyone but caster); effect e2 (May not cast at anyone but caster); ends when either-dies |
| E2 | If the target of Insult is attacked or has Magical abilities cast on them or their carried equipment by someone other than the caster, the target of Insult becomes able to choose to attack the offending party as well. | effect e1 (May not attack anyone but caster); property has-choice; clarification |
| N1 | The target may still charge and throw Magic Balls at the caster. | effect e2 (May not cast at anyone but caster); names charge; names magic-balls; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/insult.json` and the V8.08 "Spongy" rules.*
