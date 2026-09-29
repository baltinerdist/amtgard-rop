---
title: "Shove"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Shove

> Pushes a player within 20' back 20' in a straight line away from the caster, even if Stopped or Stunned; self-cast picks the direction.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Sorcery |
| Range | 20' |
| Incantation | "My power shoves thee" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | control, mobility · for: any |
| Capabilities | moves-others, moves-self |
| Rule text | [rules/magic-and-abilities/shove.md](../../rules/magic-and-abilities/shove.md) · [interoperability](../../interoperability/abilities/shove.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bard | 1st | 1 | - | 1/Life | 1 | life | - | (m) | 20' | - |
| Healer | 2nd | 1 | - | 1/Life | 1 | life | - | (m) | 20' | - |
| Wizard | 1st | 1 | - | 1/Life Charge x3 | 1 | life | x3 | (m) | 20' | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Pushes away** | target | harm | feet 20; until arrival; only if the ability is cast on another player — Moved back 20' in a straight line away from the caster; a Forced Movement effect. | E1, N1 |
| e2 | **Pushes away** | caster | benefit | feet 20; until arrival; only if the ability is cast on the caster — If the caster is the target, they move 20' in a direction of their choice. | E3, N1 |

## How it ends early

- **other-forced-movement**: ends if another Forced Movement effect affects the subject *(N2)*
- **subject-gains-state**: ends if the subject becomes Frozen, Insubstantial, Invulnerable or Stunned (list them) — Ends if the target becomes Frozen, Insubstantial, Invulnerable or Stunned (a target who is already Stunned when it is cast is still moved, per E2). *(N2)*

## Properties

- **forced-movement**: the text says it is a Forced Movement effect *(N1)*
- **bypass-states**: works regardless of States — Works on Stopped and Stunned players, an exception to the Forced Movement rule that such effects fail on Stopped players. *(E2)*
- **has-choice**: the subject chooses between options — Only when the caster targets themselves: they choose the direction. *(E3)*

## Clarifications in the text

- Shove works on players who are Stopped or Stunned when it is cast. *(E2)*

## Names in the text

- mechanic **forced-movement**: mentions *(N1, N2)*
- state **stopped**: mentions *(E2)*
- state **stunned**: mentions *(E2, N2)*
- state **frozen**: mentions *(N2)*
- state **insubstantial**: mentions *(N2)*
- state **invulnerable**: mentions *(N2)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
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
| same-effects-different-numbers | [Throw](throw.md) | Pushes away: feet 20, until arrival, if cast-on-other vs feet 50, until arrival, if cast-on-other; Pushes away: feet 20, until arrival, if cast-on-self vs feet 50, until arrival, if cast-on-self |

## Open questions

- E2 says Shove works on Stunned players while N2 ends it when the target becomes Stunned; read as: already Stunned when cast is moved, becoming Stunned during the movement ends it.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target player is moved back 20' in a straight line away from the caster. | effect e1 (Pushes away) |
| E2 | Works on Stopped and Stunned players. | property bypass-states; names stopped; names stunned; clarification |
| E3 | If the caster is the target, the caster may choose the direction they move. | effect e2 (Pushes away); property has-choice |
| N1 | This is a Forced Movement effect. | effect e1 (Pushes away); effect e2 (Pushes away); property forced-movement; names forced-movement |
| N2 | This effect is ended if the target is affected by another Forced Movement effect or becomes Frozen, Insubstantial, Invulnerable, or Stunned. | ends when other-forced-movement; ends when subject-gains-state; names forced-movement; names stunned; names frozen; names insubstantial; names invulnerable |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/shove.json` and the V8.08 "Spongy" rules.*
