---
title: "Banish"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Banish

> An Insubstantial player within 20' must return to base, their Insubstantial State replaced by Banish's, ending it on arrival.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Spirit |
| Range | 20' |
| Incantation | "The spirits banish thee from this place" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | control, mobility · for: any |
| Capabilities | moves-others, moves-self |
| Rule text | [rules/magic-and-abilities/banish.md](../../rules/magic-and-abilities/banish.md) · [interoperability](../../interoperability/abilities/banish.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monk | 2nd | - | - | 1/Life Charge x5 | 1 | life | x5 | (m) | 20' | - |
| Healer | 1st | 1 | - | 1/Life | 1 | life | - | (m) | 20' | - |
| Wizard | 1st | 1 | - | 1/Life | 1 | life | - | (m) | 20' | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Sends to base** | target | harm | until arrival; only if the ability is cast on another player — Must return to their base while Insubstantial from Banish (N1). A Forced Movement effect. When cast on another player; the self-cast case is e2. | E1, N1, N4 |
| e2 | **Sends to base** | caster | benefit | until arrival; only if the ability is cast on the caster — When cast on self (the caster must already be Insubstantial): the caster travels to their base (Forced Movement) and may end the Insubstantial State at any time with the Insubstantial exit incantation (N3). | E1, N3, N4 |

## Requirements

- **target-insubstantial**: target must be Insubstantial *(E1)*

## How it ends early

- **on-arrival**: ends on reaching the destination — Upon arrival they must immediately end the effect as per Insubstantial. *(E2)*
- **insubstantial-ends**: ends if the Insubstantial State from it ends — If the Insubstantial State ends before reaching the base, the rest of the effect ends as well. *(N2)*
- **exit-at-will**: the subject may end it at any time (states how) — Only when Banish is cast on self: the caster may end the Insubstantial State at any time with the Insubstantial exit incantation. *(N3)*

## Properties

- **forced-movement**: the text says it is a Forced Movement effect *(N4)*

## Clarifications in the text

- The target's existing Insubstantial State is replaced with a new Insubstantial State from Banish, so the State is now governed by Banish. *(N1)*

## Names in the text

- state **insubstantial**: requires *(E1, E2, N1, N2, N3)*
- mechanic **base**: mentions *(E1, N2)*
- mechanic **forced-movement**: mentions *(N4)*
- mechanic **incantation**: mentions *(N3)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
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
| does less than | [Lost](lost.md) | only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Makes Insubstantial (caster, until arrival, if cast-on-self); requirement only in Banish: target-insubstantial; school: Spirit vs Command |
| overlap | [Summon Dead](summon-dead.md) | only Banish: Sends to base (target, until arrival, if cast-on-other); only Banish: Sends to base (caster, until arrival, if cast-on-self); only Summon Dead: Brings to the caster (dead-target, until arrival); only Summon Dead: Moves where the player died (dead-target, instant); requirement only in Banish: target-insubstantial; requirement only in Summon Dead: target-dead, target-not-moved-5ft, target-willing; ends when only in Banish: exit-at-will, insubstantial-ends; property only in Banish: forced-movement |
| overlap | [Teleport](teleport.md) | only Banish: Sends to base (target, until arrival, if cast-on-other); only Banish: Sends to base (caster, until arrival, if cast-on-self); only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Makes Insubstantial (caster, until arrival, if cast-on-self); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Banish: target-insubstantial; requirement only in Teleport: target-willing |

## Open questions

- Convention 10 encodes Banish only as move.to-base; N1's replacement Insubstantial State is kept as a clarification rather than a state.apply effect.
- Beneficiary 'any': normally used on enemies, but N3 explicitly allows casting it on self (a quick return to base).

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target Insubstantial player must return to their base. | effect e1 (Sends to base); effect e2 (Sends to base); requirement target-insubstantial; names insubstantial; names base |
| E2 | Upon arrival, they must immediately end the effect as per Insubstantial. | ends when on-arrival; names insubstantial |
| N1 | The target's Insubstantial State is replaced with a new Insubstantial State from Banish. | effect e1 (Sends to base); names insubstantial; clarification |
| N2 | If the Insubstantial State is ended before reaching the base, the rest of the effect is ended as well. | ends when insubstantial-ends; names insubstantial; names base |
| N3 | If Banish is cast on self, the caster may end this Insubstantial State at any time by using the exit incantation for Insubstantial. | effect e2 (Sends to base); ends when exit-at-will; names insubstantial; names incantation |
| N4 | This is a Forced Movement effect. | effect e1 (Sends to base); effect e2 (Sends to base); property forced-movement; names forced-movement |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/banish.json` and the V8.08 "Spongy" rules.*
