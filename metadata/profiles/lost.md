---
title: "Lost"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Lost

> Target within 20' becomes Insubstantial and must go directly to their base, ending the State on arrival; a Forced Movement effect.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Command |
| Range | 20' |
| Incantation | "I command thee to be lost" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | control, mobility · for: any |
| Capabilities | makes-insubstantial, moves-others, moves-self, neutralizes, removes-from-play, self-protection-state |
| Rule text | [rules/magic-and-abilities/lost.md](../../rules/magic-and-abilities/lost.md) · [interoperability](../../interoperability/abilities/lost.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bard | 5th | 1 | - | 1/Life | 1 | life | - | (m) | 20' | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Makes Insubstantial** | target | harm | until arrival; only if the ability is cast on another player — Insubstantial while travelling to base; must end it immediately on arrival as per Insubstantial (E2). | E1, E2, N1 |
| e2 | **Sends to base** | target | harm | until arrival; only if the ability is cast on another player — Must move directly to their base; a Forced Movement effect (N3). Ends if the Insubstantial State ends first (N1). | E1, N1, N3 |
| e3 | **Makes Insubstantial** | caster | benefit | until arrival; only if the ability is cast on the caster — When cast on self: the caster is Insubstantial on the way to base and may end it at any time with the Insubstantial exit incantation (N2). | E1, N2 |
| e4 | **Sends to base** | caster | benefit | until arrival; only if the ability is cast on the caster — When cast on self: the caster travels directly to their base (Forced Movement). | E1, N2, N3 |

## How it ends early

- **on-arrival**: ends on reaching the destination — On arriving at base the player must immediately end the effect as per Insubstantial. *(E2)*
- **insubstantial-ends**: ends if the Insubstantial State from it ends — If the Insubstantial State ends before reaching base, the rest of the effect (the travel to base) ends too. *(N1)*
- **exit-at-will**: the subject may end it at any time (states how) — Only when Lost was cast on self: the caster may end the Insubstantial State at any time with the Insubstantial exit incantation. *(N2)*

## Properties

- **forced-movement**: the text says it is a Forced Movement effect *(N3)*

## Clarifications in the text

- Ending the Insubstantial State early also ends the requirement to keep travelling to base. *(N1)*
- Lost may be cast on self; then the caster may leave the Insubstantial State whenever they choose using its exit incantation. *(N2)*

## Names in the text

- state **insubstantial**: mentions *(E1, E2, N1, N2)*
- mechanic **base**: mentions *(E1, N1)*
- mechanic **forced-movement**: mentions *(N3)*
- mechanic **incantation**: mentions *(N2)*

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
| does more than | [Banish](banish.md) | only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Makes Insubstantial (caster, until arrival, if cast-on-self); requirement only in Banish: target-insubstantial; school: Command vs Spirit |
| overlap | [Teleport](teleport.md) | only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; school: Command vs Sorcery |
| overlap | [Astral Intervention](astral-intervention.md) | Makes Insubstantial: until arrival, if cast-on-self vs 30 s, if cast-on-self; only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); ends when only in Lost: insubstantial-ends, on-arrival; property only in Lost: forced-movement |
| overlap | [Shadow Step](shadow-step.md) | Makes Insubstantial: until arrival, if cast-on-self vs until removed; only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); ends when only in Lost: insubstantial-ends, on-arrival; property only in Lost: forced-movement; property only in Shadow Step: castable-while-moving; school: Command vs Sorcery |

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target player becomes Insubstantial, must move directly to their base. | effect e1 (Makes Insubstantial); effect e2 (Sends to base); effect e3 (Makes Insubstantial); effect e4 (Sends to base); names insubstantial; names base |
| E2 | Upon arrival, they must immediately end the effect as per Insubstantial. | effect e1 (Makes Insubstantial); ends when on-arrival; names insubstantial |
| N1 | If the Insubstantial State is ended before reaching the base, the rest of the effect is ended as well. | effect e1 (Makes Insubstantial); effect e2 (Sends to base); ends when insubstantial-ends; names insubstantial; names base; clarification |
| N2 | If Lost is cast on self, the caster may end this Insubstantial State at any time by using the exit incantation for Insubstantial. | effect e3 (Makes Insubstantial); effect e4 (Sends to base); ends when exit-at-will; names insubstantial; names incantation; clarification |
| N3 | This is a Forced Movement effect. | effect e2 (Sends to base); effect e4 (Sends to base); property forced-movement; names forced-movement |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/lost.json` and the V8.08 "Spongy" rules.*
