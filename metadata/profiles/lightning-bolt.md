---
title: "Lightning Bolt"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Lightning Bolt

> Magic Ball: wounds the hit location and Stops the player struck for 60 seconds; Weapon Destroying and Armor Breaking; Engulfing.

| | |
| --- | --- |
| Type | Magic Ball (magic-ball) |
| School | Flame |
| Range | - |
| Incantation | "The flame of storms is mine to evoke" x3 |
| Materials | Yellow Magic Ball |
| Magical | yes, (m) for at least one class |
| Roles | offense, control, equipment · for: enemy |
| Capabilities | attacks-equipment, defeats-armor, holds-in-place, wounds |
| Rule text | [rules/magic-and-abilities/lightning-bolt.md](../../rules/magic-and-abilities/lightning-bolt.md) · [interoperability](../../interoperability/abilities/lightning-bolt.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wizard | 3rd | 1 | 4 | 1 Ball / Unlimited | 1 balls | unlimited | - | (m) | - | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Weapon Destroying (this magic ball)** | struck-player | harm | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor | E1 |
| e2 | **Armor Breaking (this magic ball)** | struck-player | harm | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor | E1 |
| e3 | **Inflicts a wound** | struck-player | harm | location struck; instant; when a weapon, arrow or ball strikes the subject or their armor | E2 |
| e4 | **Stops** | struck-player | harm | 60 s; when a weapon, arrow or ball strikes the subject or their armor | E3 |

## Properties

- **engulfing**: Engulfing *(E4)*

## Names in the text

- state **stopped**: mentions *(E3)*
- special-effect **weapon-destroying**: mentions *(E1)*
- special-effect **armor-breaking**: mentions *(E1)*
- mechanic **engulfing**: mentions *(E4)*
- mechanic **magic-balls**: mentions *(E1)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Missile Block](missile-block.md) | Can block it by hand | Monk |
| [Song of Freedom](song-of-freedom.md) | Cannot receive stopped, frozen, insubstantial | Bard |
| [Flame Blade](flame-blade.md) | Immune | Anti-Paladin, Druid |
| [Gift of Fire](gift-of-fire.md) | Immune | Druid |
| [Immune to Flame](immune-to-flame.md) | Immune | Anti-Paladin |
| [Ironskin](ironskin.md) | Immune | Druid |
| [Adaptive Protection](adaptive-protection.md) | Immune (chosen School) | Healer, Scout |
| [Adaptive Blessing](adaptive-blessing.md) | Resistant (chosen School, next ability) | Healer |
| [Blessed Aura](blessed-aura.md) | Resistant to the next source | Healer |
| [Blessing Against Harm](blessing-against-harm.md) | Resistant to the next source | Healer, Wizard |
| [Blessing Against Wounds](blessing-against-wounds.md) | Resistant to the next wound | Healer, Monk |
| [Sanctuary](sanctuary.md) | Unaffected by hostile actions within 20ft | Monk |
| [Protection from Magic](protection-from-magic.md) | Unaffected by magical abilities | Healer, Paladin, Wizard |

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does more than | [Entangle](entangle.md) | only Lightning Bolt: Weapon Destroying (this magic ball) (struck-player, instant); only Lightning Bolt: Armor Breaking (this magic ball) (struck-player, instant); only Lightning Bolt: Inflicts a wound (struck-player, instant); school: Flame vs Subdual |
| does more than | [Force Bolt](force-bolt.md) | only Lightning Bolt: Stops (struck-player, 60 s); property only in Lightning Bolt: engulfing; school: Flame vs Sorcery |
| does more than | [Hold Person](hold-person.md) | Stops: 60 s vs 30 s; only Lightning Bolt: Weapon Destroying (this magic ball) (struck-player, instant); only Lightning Bolt: Armor Breaking (this magic ball) (struck-player, instant); only Lightning Bolt: Inflicts a wound (struck-player, instant); property only in Lightning Bolt: engulfing; delivery: magic-ball vs verbal; school: Flame vs Command; range: - vs 20' |
| does more than | [Pinning Arrow](pinning-arrow.md) | Stops: 60 s vs 30 s; only Lightning Bolt: Weapon Destroying (this magic ball) (struck-player, instant); only Lightning Bolt: Armor Breaking (this magic ball) (struck-player, instant); only Lightning Bolt: Inflicts a wound (struck-player, instant); delivery: magic-ball vs specialty-arrow; school: Flame vs Sorcery |
| overlap | [Phase Bolt](phase-bolt.md) | only Lightning Bolt: Stops (struck-player, 60 s); only Phase Bolt: Phasing (this magic ball) (struck-player, instant); property only in Lightning Bolt: engulfing; school: Flame vs Sorcery |

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | This Magic Ball is Weapon Destroying and Armor Breaking. | effect e1 (Weapon Destroying (this magic ball)); effect e2 (Armor Breaking (this magic ball)); names weapon-destroying; names armor-breaking; names magic-balls |
| E2 | Player hit receives a wound to that hit location. | effect e3 (Inflicts a wound) |
| E3 | Player struck is Stopped for 60 seconds. | effect e4 (Stops); names stopped |
| E4 | Engulfing. | property engulfing; names engulfing |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/lightning-bolt.json` and the V8.08 "Spongy" rules.*
