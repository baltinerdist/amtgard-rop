---
title: "Circle of Protection"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Circle of Protection

> The caster and up to five willing players in Touch lose States and Ongoing Effects and become Insubstantial in place, safe from most Forced Movement.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Protection |
| Range | Touch |
| Incantation | "Circle of Protection" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | defense, team · for: team |
| Capabilities | cleanses, has-drawback, holds-in-place, makes-insubstantial, neutralizes, protects, removes-from-play, restricts-others |
| Rule text | [rules/magic-and-abilities/circle-of-protection.md](../../rules/magic-and-abilities/circle-of-protection.md) · [interoperability](../../interoperability/abilities/circle-of-protection.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Healer | 4th | 1 | 1 | 1/Refresh Charge x10 | 1 | refresh | x10 | (m) | Touch | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Removes States or Ongoing Effects** | group | benefit | what all-states-and-effects; instant — Caster and up to five willing players within Touch range: all States and Ongoing Effects removed, then they become Insubstantial. Caster plus up to five willing players (max_targets counts the other players). | E1 |
| e2 | **Makes Insubstantial** | group | benefit | until removed — Caster plus up to five willing players (max_targets counts the other players). | E1, E2 |
| e3 | **May not move from start** | group | harm | what move-from-start; until removed; continuously while it is worn, chanted or in effect — Caster plus up to five willing players (max_targets counts the other players). | E2, E3 |
| e4 | **Unaffected by** | group | benefit | by blink; until removed; continuously while it is worn, chanted or in effect — Caster plus up to five willing players (max_targets counts the other players). | E2, E3 |
| e5 | **Unaffected by** | group | benefit | by forced-movement-except-banish; until removed; continuously while it is worn, chanted or in effect — Caster plus up to five willing players (max_targets counts the other players). | E2, E3 |
| e6 | **Casts while Insubstantial** | group | benefit | on same-casting-targets; until removed; continuously while it is worn, chanted or in effect — Any abilities, on players (and their carried equipment) made Insubstantial by the same casting, as though they were not Insubstantial. Caster plus up to five willing players (max_targets counts the other players). | E2, E4 |

**Drawbacks:** May not move from start (group)

## Requirements

- **target-willing**: target must be willing — The other players must be willing. *(E1)*

## Restrictions

- **limited-targets**: may only be cast on particular targets (explain in note) (5) — Caster plus up to five willing players within Touch range of the caster. *(E1)*

## How it ends early

- **exit-at-will**: the subject may end it at any time (states how) — Each target may end this Insubstantial State with the exit incantation for Insubstantial. *(E2, E5)*
- **caster-ends-for-all**: the caster ending it ends it for everyone — If the caster exits with the incantation, it ends for all targets. *(E6)*
- **insubstantial-ends**: ends if the Insubstantial State from it ends — When a target's Insubstantial State ends, the Ongoing Effects of Circle of Protection no longer apply to them. *(E7)*

## Properties

- **affects-caster-and-target**: can affect the caster and others *(E1)*

## Clarifications in the text

- A player who is prevented from becoming Insubstantial is unaffected by Circle of Protection entirely. *(N1)*

## Names in the text

- state **insubstantial**: mentions *(E1, E4, E5, E6, E7, N1)*
- ability **[Blink](blink.md)**: protects-against *(E3)*
- ability **[Banish](banish.md)**: mentions *(E3)*
- mechanic **forced-movement**: protects-against *(E3)*
- mechanic **incantation**: mentions *(E5, E6)*
- mechanic **ongoing-effects**: mentions *(E1, E7)*
- mechanic **range**: mentions *(E1)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Song of Freedom](song-of-freedom.md) | Cannot receive stopped, frozen, insubstantial | Bard |
| [Blessed Aura](blessed-aura.md) | Resistant to the next source | Healer |
| [Blessing Against Harm](blessing-against-harm.md) | Resistant to the next source | Healer, Wizard |
| [Sanctuary](sanctuary.md) | Unaffected by hostile actions within 20ft | Monk |
| [Protection from Magic](protection-from-magic.md) | Unaffected by magical abilities | Healer, Paladin, Wizard |
| [Rage](rage.md) | Unaffected by verbal abilities | Barbarian |

## Open questions

- E1 removes all States and Ongoing Effects before applying Insubstantial; whether Enchantments count as Ongoing Effects here is not stated.
- N1 implies a player prevented from Insubstantial also keeps their States/Ongoing Effects (unaffected entirely); encoded as a clarification only.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | The caster and up to five willing players within Touch range of the caster immediately have all States and Ongoing Effects removed and then become Insubstantial. | effect e1 (Removes States or Ongoing Effects); effect e2 (Makes Insubstantial); requirement target-willing; restriction limited-targets; property affects-caster-and-target; names insubstantial; names ongoing-effects; names range |
| E2 | All targets: | effect e2 (Makes Insubstantial); effect e3 (May not move from start); effect e4 (Unaffected by); effect e5 (Unaffected by); effect e6 (Casts while Insubstantial); ends when exit-at-will |
| E3 | - May not move from their starting location, and are unaffected by Blink and by Forced Movement effects other than Banish. | effect e3 (May not move from start); effect e4 (Unaffected by); effect e5 (Unaffected by); names Blink; names Banish; names forced-movement |
| E4 | - May use abilities on players and their carried equipment who became Insubstantial due to the same casting of Circle of Protection as though they were not Insubstantial. | effect e6 (Casts while Insubstantial); names insubstantial |
| E5 | - May end this Insubstantial State at any time by using the exit incantation for Insubstantial. | ends when exit-at-will; names insubstantial; names incantation |
| E6 | If the caster ends Circle of Protection by using the exit incantation for Insubstantial, the effect ends for all targets. | ends when caster-ends-for-all; names insubstantial; names incantation |
| E7 | If the Insubstantial State is ended for a target, the Ongoing Effects of Circle of Protection no longer apply to that player. | ends when insubstantial-ends; names insubstantial; names ongoing-effects |
| N1 | If a player is prevented from becoming Insubstantial, they are unaffected by Circle of Protection. | names insubstantial; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/circle-of-protection.json` and the V8.08 "Spongy" rules.*
