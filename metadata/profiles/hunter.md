---
title: "Hunter"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Hunter

> Scout archetype: Great weapons and Javelins; Hold Person 1/Life Charge x3 or Pinning Arrow 2 Arrows/Unlimited (whichever taken at 4th); no shields; loses Evolution, Release.

| | |
| --- | --- |
| Type | Archetype (archetype) |
| School | Neutral |
| Range | - |
| Incantation | none |
| Materials | none |
| Magical | no |
| Roles | class-modifier, equipment, resource, control · for: self |
| Capabilities | changes-frequency, has-drawback, more-uses |
| Rule text | [rules/magic-and-abilities/hunter.md](../../rules/magic-and-abilities/hunter.md) · [interoperability](../../interoperability/abilities/hunter.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Scout | 6th | - | - | - | - | - | - | - | - | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Allows equipment** | bearer | benefit | what great-weapon; permanent; continuously while it is worn, chanted or in effect | E1 |
| e2 | **Allows equipment** | bearer | benefit | what javelins; permanent; continuously while it is worn, chanted or in effect | E1 |
| e3 | **Changes Hold Person** | bearer | benefit | change becomes 1/Life Charge x3 (m); permanent; continuously while it is worn, chanted or in effect; choice g1 option 1 — Option 1; only if Hold Person was chosen at level 4. Scout's Hold Person is normally 1/Life (m). | E2, E3, N1 |
| e4 | **Changes Pinning Arrow** | bearer | benefit | change becomes 2 Arrows / Unlimited (ex); permanent; continuously while it is worn, chanted or in effect; choice g1 option 2 — Option 2; only if Pinning Arrow was chosen at level 4. Scout's Pinning Arrow is normally 1 Arrow / Unlimited (ex). | E2, E4, N1 |
| e5 | **May not wield shields** | bearer | harm | what wield-shields; permanent; continuously while it is worn, chanted or in effect — Drawback: may not wield shields. | L1 |
| e6 | **Removes Evolution** | bearer | harm | permanent; continuously while it is worn, chanted or in effect — Drawback: loses all instances of Evolution. | L2 |
| e7 | **Removes Release** | bearer | harm | permanent; continuously while it is worn, chanted or in effect — Drawback: loses all instances of Release. | L2 |
| e8 | **Changes how often abilities can be used** | bearer | benefit | scope Hold Person; change charge-x3; permanent; continuously while it is worn, chanted or in effect; choice g1 option 1 — Option 1: Hold Person becomes 1/Life Charge x3 (m); only if Hold Person was chosen at level 4. | E2, E3, N1 |
| e9 | **Changes how often abilities can be used** | bearer | benefit | scope Pinning Arrow; change double-uses; permanent; continuously while it is worn, chanted or in effect; choice g1 option 2 — Option 2: Pinning Arrow becomes 2 Arrows / Unlimited (ex) (Scout's 4th-level Pinning Arrow is 1 Arrow / Unlimited); only if Pinning Arrow was chosen at level 4. | E2, E4, N1 |

**Drawbacks:** May not wield shields (bearer); Removes Evolution (bearer); Removes Release (bearer)

## Requirements

- **chose-ability-at-level**: only if a listed ability was chosen at a given level — The benefit of an option applies only if that ability (Hold Person or Pinning Arrow) was chosen at level 4. *(N1)*

## Restrictions

- **only-one-option**: only one of the listed options may be chosen — Pick one of the two frequency upgrades. *(E2)*

## Properties

- **has-choice**: the subject chooses between options — Choose Hold Person or Pinning Arrow upgrade. *(E2)*

## Names in the text

- ability **[Hold Person](hold-person.md)**: modifies *(E3, N1)*
- ability **[Pinning Arrow](pinning-arrow.md)**: modifies *(E4, N1)*
- ability **[Evolution](evolution.md)**: removes *(L2)*
- ability **[Release](release.md)**: removes *(L2)*
- mechanic **charge**: mentions *(E3)*
- mechanic **weapon**: mentions *(E1)*
- mechanic **shield**: mentions *(L1)*
- mechanic **archetype**: mentions *(E1)*

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | May wield Great weapons and Javelins. | effect e1 (Allows equipment); effect e2 (Allows equipment); names weapon; names archetype |
| E2 | Pick one: | effect e3 (Changes Hold Person); effect e4 (Changes Pinning Arrow); effect e8 (Changes how often abilities can be used); effect e9 (Changes how often abilities can be used); restriction only-one-option; property has-choice |
| E3 | - Hold Person becomes 1/Life Charge x3 (m). | effect e3 (Changes Hold Person); effect e8 (Changes how often abilities can be used); names Hold Person; names charge |
| E4 | - Pinning Arrow becomes 2 Arrows / Unlimited (ex) | effect e4 (Changes Pinning Arrow); effect e9 (Changes how often abilities can be used); names Pinning Arrow |
| L1 | May not wield shields. | effect e5 (May not wield shields); names shield |
| L2 | Lose all instances of Evolution and Release. | effect e6 (Removes Evolution); effect e7 (Removes Release); names Evolution; names Release |
| N1 | Gain the benefit of an option only if that ability was chosen at level 4. | effect e3 (Changes Hold Person); effect e4 (Changes Pinning Arrow); effect e8 (Changes how often abilities can be used); effect e9 (Changes how often abilities can be used); requirement chose-ability-at-level; names Hold Person; names Pinning Arrow |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/hunter.json` and the V8.08 "Spongy" rules.*
