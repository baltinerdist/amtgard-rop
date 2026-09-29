---
title: "Teleport"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Teleport

> A willing player becomes Insubstantial and travels directly to a fixed location the caster chose, ending it on arrival.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Sorcery |
| Range | Touch |
| Incantation | "I travel through the aether" x5 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | mobility · for: ally |
| Capabilities | makes-insubstantial, moves-ally, moves-others, moves-self, neutralizes, removes-from-play, self-protection-state |
| Rule text | [rules/magic-and-abilities/teleport.md](../../rules/magic-and-abilities/teleport.md) · [interoperability](../../interoperability/abilities/teleport.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Assassin | 5th | - | - | 2/Life | 2 | life | - | (ex) | Self | - |
| Druid | 4th | 1 | 2 | 1/Life | 1 | life | - | (m) | Touch | - |
| Healer | 4th | 1 | 2 | 1/Life | 1 | life | - | (m) | Touch | - |
| Wizard | 2nd | 1 | 2 | 1/Life | 1 | life | - | (m) | Touch | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Makes Insubstantial** | target | benefit | until arrival; only if the ability is cast on another player — Insubstantial while travelling; must end it immediately on arrival as per Insubstantial. | E1, E3, N1 |
| e2 | **Moves to a chosen location** | target | benefit | until arrival; only if the ability is cast on another player — Moves directly to a location chosen by the caster at the time of casting; it must be fixed, not relative to a player or a moveable object. A Forced Movement effect. | E1, E2, N3 |
| e3 | **Makes Insubstantial** | caster | benefit | until arrival; only if the ability is cast on the caster — Cast on self: the caster may end the Insubstantial State at any time with its exit incantation. | E1, N2 |
| e4 | **Moves to a chosen location** | caster | benefit | until arrival; only if the ability is cast on the caster | E1, E2, N2 |

## Requirements

- **target-willing**: target must be willing *(E1)*

## How it ends early

- **on-arrival**: ends on reaching the destination — Upon arrival they must immediately end the effect as per Insubstantial. *(E3)*
- **insubstantial-ends**: ends if the Insubstantial State from it ends — If the Insubstantial State is removed before the destination is reached, the effects of Teleport end. *(N1)*
- **exit-at-will**: the subject may end it at any time (states how) — Only when Teleport is cast on self: the caster may end the Insubstantial State at any time with the Insubstantial exit incantation. *(N2)*

## Properties

- **forced-movement**: the text says it is a Forced Movement effect *(N3)*

## Clarifications in the text

- The destination must be a fixed location chosen at the time of casting, not relative to a player or a moveable object. *(E2)*

## Names in the text

- state **insubstantial**: mentions *(E1, E3, N1, N2)*
- mechanic **forced-movement**: mentions *(N3)*
- mechanic **incantation**: mentions *(N2)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| overlap | [Lost](lost.md) | only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; school: Sorcery vs Command |
| overlap | [Astral Intervention](astral-intervention.md) | Makes Insubstantial: until arrival, if cast-on-self vs 30 s, if cast-on-self; only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); requirement only in Teleport: target-willing; ends when only in Teleport: insubstantial-ends, on-arrival; property only in Teleport: forced-movement |
| overlap | [Banish](banish.md) | only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Makes Insubstantial (caster, until arrival, if cast-on-self); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); only Banish: Sends to base (target, until arrival, if cast-on-other); only Banish: Sends to base (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; requirement only in Banish: target-insubstantial |
| overlap | [Shadow Step](shadow-step.md) | Makes Insubstantial: until arrival, if cast-on-self vs until removed; only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; ends when only in Teleport: insubstantial-ends, on-arrival; property only in Teleport: forced-movement; property only in Shadow Step: castable-while-moving |

## Open questions

- N2 lets a self-cast Teleport be ended early; the text does not say whether another player who was Teleported may end it before arrival (the general Insubstantial rule would require them to end it as per Teleport, i.e. on arrival).

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target willing player becomes Insubstantial and moves directly to a chosen location chosen by the caster at the time of casting. | effect e1 (Makes Insubstantial); effect e2 (Moves to a chosen location); effect e3 (Makes Insubstantial); effect e4 (Moves to a chosen location); requirement target-willing; names insubstantial |
| E2 | This must be a fixed location (not relative to a player or to a moveable object). | effect e2 (Moves to a chosen location); effect e4 (Moves to a chosen location); clarification |
| E3 | Upon arrival, they must immediately end the effect as per Insubstantial. | effect e1 (Makes Insubstantial); ends when on-arrival; names insubstantial |
| N1 | If the player's Insubstantial State is removed before they have reached their destination, the effects of Teleport end. | effect e1 (Makes Insubstantial); ends when insubstantial-ends; names insubstantial |
| N2 | If Teleport is cast on self, the caster may end this Insubstantial State at any time by using the exit incantation for Insubstantial. | effect e3 (Makes Insubstantial); effect e4 (Moves to a chosen location); ends when exit-at-will; names insubstantial; names incantation |
| N3 | This is a Forced Movement effect. | effect e2 (Moves to a chosen location); property forced-movement; names forced-movement |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/teleport.json` and the V8.08 "Spongy" rules.*
