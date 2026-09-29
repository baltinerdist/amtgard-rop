---
title: "Shadow Step"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Shadow Step

> Caster becomes Insubstantial in place, even while moving, until they use the Insubstantial exit incantation.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Sorcery |
| Range | Self |
| Incantation | "I step into the shadows" |
| Materials | none |
| Magical | no |
| Roles | defense · for: self |
| Capabilities | castable-while-moving, makes-insubstantial, self-protection-state |
| Rule text | [rules/magic-and-abilities/shadow-step.md](../../rules/magic-and-abilities/shadow-step.md) · [interoperability](../../interoperability/abilities/shadow-step.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Assassin | 1st | - | - | 2/Life | 2 | life | - | (ex) | Self | - |
| Scout | 3rd | - | - | 1/Life | 1 | life | - | (ex) | Self | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Makes Insubstantial** | caster | benefit | until removed — No duration is given; the State lasts until the caster exits it (N1) or it is removed. The text grants no movement, so the general Insubstantial rule (may not move from the starting location) applies. | E1, N1 |

## How it ends early

- **exit-at-will**: the subject may end it at any time (states how) — By using the exit incantation for Insubstantial ("I return to the physical world" x2). *(N1)*

## Properties

- **castable-while-moving**: may be cast or used while moving *(E2)*

## Clarifications in the text

- Casting while moving is an explicit exception to the usual requirement to stand still while incanting. *(E2)*

## Names in the text

- state **insubstantial**: mentions *(E1, N1)*
- mechanic **incantation**: mentions *(N1)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| overlap | [Astral Intervention](astral-intervention.md) | Makes Insubstantial: until removed vs 30 s, if cast-on-self; only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); property only in Shadow Step: castable-while-moving; school: Sorcery vs Command; range: Self vs 20' |
| does less than | [Gift of Air](gift-of-air.md) | only Gift of Air: Ignores a hit (bearer, instant); only Gift of Air: Sends to base (bearer, until arrival); only Gift of Air: May not exit early (bearer, until arrival); only Gift of Air: May not wield weapons (bearer, while worn); only Gift of Air: May not wield shields (bearer, while worn); restriction only in Gift of Air: no-exit-early; ends when only in Gift of Air: insubstantial-ends, on-arrival; property only in Shadow Step: castable-while-moving |
| is given by | [Void Touched](void-touched.md) | only Shadow Step: Makes Insubstantial (caster, until removed); only Void Touched: Armor Breaking (bearer melee weapons) (bearer, while worn); only Void Touched: Grants Shadow Step (bearer, while worn); only Void Touched: Grants Steal Life Essence (bearer, while worn); only Void Touched: Unaffected by (bearer, while worn); only Void Touched: Curses (bearer, while worn); ends when only in Shadow Step: exit-at-will; property only in Shadow Step: castable-while-moving |
| overlap | [Lost](lost.md) | Makes Insubstantial: until removed vs until arrival, if cast-on-self; only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); ends when only in Lost: insubstantial-ends, on-arrival; property only in Shadow Step: castable-while-moving; property only in Lost: forced-movement; school: Sorcery vs Command |
| overlap | [Teleport](teleport.md) | Makes Insubstantial: until removed vs until arrival, if cast-on-self; only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; ends when only in Teleport: insubstantial-ends, on-arrival; property only in Shadow Step: castable-while-moving; property only in Teleport: forced-movement |

## Open questions

- No duration or movement allowance is stated: the caster stays Insubstantial in place until they exit or the State is removed.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Caster becomes Insubstantial. | effect e1 (Makes Insubstantial); names insubstantial |
| E2 | Shadow Step may be cast while moving. | property castable-while-moving; clarification |
| N1 | Caster may end this Insubstantial State at any time by using the exit incantation for Insubstantial. | effect e1 (Makes Insubstantial); ends when exit-at-will; names insubstantial; names incantation |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/shadow-step.json` and the V8.08 "Spongy" rules.*
