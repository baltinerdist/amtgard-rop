---
title: "Astral Intervention"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Astral Intervention

> A player within 20' (or the caster) becomes Insubstantial for 30 seconds; if self-cast, the caster may exit at any time.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Command |
| Range | 20' |
| Incantation | "I command thee to retreat into the aether" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | control, defense · for: any |
| Capabilities | makes-insubstantial, neutralizes, removes-from-play, self-protection-state |
| Rule text | [rules/magic-and-abilities/astral-intervention.md](../../rules/magic-and-abilities/astral-intervention.md) · [interoperability](../../interoperability/abilities/astral-intervention.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Healer | 3rd | 1 | - | 1/Life Charge x3 | 1 | life | x3 | (m) | 20' | - |
| Wizard | 2nd | 1 | - | 1/Life | 1 | life | - | (m) | 20' | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Makes Insubstantial** | target | depends | 30 s; only if the ability is cast on another player — When cast on another player: Insubstantial for 30 seconds with no early exit. May also be used to protect an ally. | E1 |
| e2 | **Makes Insubstantial** | caster | benefit | 30 s; only if the ability is cast on the caster — When cast on self; may end it at any time with the Insubstantial exit incantation. | E1, N1 |

## How it ends early

- **exit-at-will**: the subject may end it at any time (states how) — Only if cast on self: the caster may end the Insubstantial State at any time with the exit incantation for Insubstantial. *(N1)*

## Clarifications in the text

- When cast on self, the caster may end the Insubstantial State early using the Insubstantial exit incantation. *(N1)*

## Names in the text

- state **insubstantial**: mentions *(E1, N1)*
- mechanic **incantation**: mentions *(N1)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Song of Freedom](song-of-freedom.md) | Cannot receive stopped, frozen, insubstantial | Bard |
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

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| overlap | [Shadow Step](shadow-step.md) | Makes Insubstantial: 30 s, if cast-on-self vs until removed; only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); property only in Shadow Step: castable-while-moving; school: Command vs Sorcery; range: 20' vs Self |
| overlap | [Lost](lost.md) | Makes Insubstantial: 30 s, if cast-on-self vs until arrival, if cast-on-self; only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); ends when only in Lost: insubstantial-ends, on-arrival; property only in Lost: forced-movement |
| overlap | [Teleport](teleport.md) | Makes Insubstantial: 30 s, if cast-on-self vs until arrival, if cast-on-self; only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; ends when only in Teleport: insubstantial-ends, on-arrival; property only in Teleport: forced-movement |

## Open questions

- N1 only grants early exit when self-cast; a target other than the caster apparently may not exit early even if willing (Insubstantial's general exit rule needs them to have caused it).

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target player becomes Insubstantial for 30 seconds. | effect e1 (Makes Insubstantial); effect e2 (Makes Insubstantial); names insubstantial |
| N1 | If cast on self, the caster may end this Insubstantial State at any time by using the exit incantation for Insubstantial. | effect e2 (Makes Insubstantial); ends when exit-at-will; names insubstantial; names incantation; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/astral-intervention.json` and the V8.08 "Spongy" rules.*
