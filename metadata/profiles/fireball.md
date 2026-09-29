---
title: "Fireball"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Fireball

> Magic Ball: the player hit dies; Weapon, Armor and Shield Destroying.

| | |
| --- | --- |
| Type | Magic Ball (magic-ball) |
| School | Flame |
| Range | - |
| Incantation | "The flame of fire is mine to evoke" x3 |
| Materials | Red Magic Ball |
| Magical | yes, (m) for at least one class |
| Roles | offense, equipment · for: enemy |
| Capabilities | attacks-equipment, can-be-lethal, causes-death, defeats-armor |
| Rule text | [rules/magic-and-abilities/fireball.md](../../rules/magic-and-abilities/fireball.md) · [interoperability](../../interoperability/abilities/fireball.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wizard | 4th | 1 | 4 | 1 Ball / Unlimited | 1 balls | unlimited | - | (m) | - | - |
| Anti-Paladin | 6th | - | - | - | - | - | - | - | - | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Weapon Destroying (this magic ball)** | struck-player | harm | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor | E1 |
| e2 | **Armor Destroying (this magic ball)** | struck-player | harm | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor | E1 |
| e3 | **Shield Destroying (this magic ball)** | struck-player | harm | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor | E1 |
| e4 | **Causes death** | struck-player | harm | instant; when a weapon, arrow or ball strikes the subject or their armor | E2 |

## Names in the text

- special-effect **weapon-destroying**: mentions *(E1)*
- special-effect **armor-destroying**: mentions *(E1)*
- special-effect **shield-destroying**: mentions *(E1)*
- mechanic **magic-balls**: mentions *(E1)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Missile Block](missile-block.md) | Can block it by hand | Monk |
| [Flame Blade](flame-blade.md) | Immune | Anti-Paladin, Druid |
| [Gift of Fire](gift-of-fire.md) | Immune | Druid |
| [Immune to Flame](immune-to-flame.md) | Immune | Anti-Paladin |
| [Ironskin](ironskin.md) | Immune | Druid |
| [Adaptive Protection](adaptive-protection.md) | Immune (chosen School) | Healer, Scout |
| [Adaptive Blessing](adaptive-blessing.md) | Resistant (chosen School, next ability) | Healer |
| [Blessed Aura](blessed-aura.md) | Resistant to the next source | Healer |
| [Blessing Against Harm](blessing-against-harm.md) | Resistant to the next source | Healer, Wizard |
| [Sanctuary](sanctuary.md) | Unaffected by hostile actions within 20ft | Monk |
| [Protection from Magic](protection-from-magic.md) | Unaffected by magical abilities | Healer, Paladin, Wizard |

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does more than | [Call Lightning](call-lightning.md) | only Fireball: Weapon Destroying (this magic ball) (struck-player, instant); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Fireball: Shield Destroying (this magic ball) (struck-player, instant); delivery: magic-ball vs verbal; range: - vs 20' |
| does more than | [Coup de Grace](coup-de-grace.md) | only Fireball: Weapon Destroying (this magic ball) (struck-player, instant); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Fireball: Shield Destroying (this magic ball) (struck-player, instant); requirement only in Coup de Grace: target-wounded; delivery: magic-ball vs verbal; school: Flame vs Death; range: - vs 20' |
| does more than | [Dimensional Rift](dimensional-rift.md) | only Fireball: Weapon Destroying (this magic ball) (struck-player, instant); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Fireball: Shield Destroying (this magic ball) (struck-player, instant); requirement only in Dimensional Rift: target-insubstantial; delivery: magic-ball vs verbal; school: Flame vs Sorcery; range: - vs 20' |
| does more than | [Dragged Below](dragged-below.md) | only Fireball: Weapon Destroying (this magic ball) (struck-player, instant); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Fireball: Shield Destroying (this magic ball) (struck-player, instant); requirement only in Dragged Below: target-stopped; delivery: magic-ball vs verbal; school: Flame vs Death; range: - vs 20' |
| does more than | [Finger of Death](finger-of-death.md) | only Fireball: Weapon Destroying (this magic ball) (struck-player, instant); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Fireball: Shield Destroying (this magic ball) (struck-player, instant); delivery: magic-ball vs verbal; school: Flame vs Death; range: - vs 20' |
| does more than | [Shatter](shatter.md) | only Fireball: Weapon Destroying (this magic ball) (struck-player, instant); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Fireball: Shield Destroying (this magic ball) (struck-player, instant); requirement only in Shatter: target-frozen; delivery: magic-ball vs verbal; school: Flame vs Sorcery; range: - vs 20' |
| is given by | [Infernal](infernal.md) | only Fireball: Weapon Destroying (this magic ball) (struck-player, instant); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Fireball: Shield Destroying (this magic ball) (struck-player, instant); only Fireball: Causes death (struck-player, instant); only Infernal: Grants Fireball (bearer, permanent); only Infernal: Changes Flame Blade (bearer, permanent); only Infernal: May not wield shields (bearer, permanent); only Infernal: Removes Steal Life Essence (bearer, permanent) |
| overlap | [Sphere of Annihilation](sphere-of-annihilation.md) | only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Curses (struck-player, until respawn); property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; school: Flame vs Sorcery |

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | This Magic Ball is Weapon Destroying, Armor Destroying, and Shield Destroying. | effect e1 (Weapon Destroying (this magic ball)); effect e2 (Armor Destroying (this magic ball)); effect e3 (Shield Destroying (this magic ball)); names weapon-destroying; names armor-destroying; names shield-destroying; names magic-balls |
| E2 | Player hit dies. | effect e4 (Causes death) |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/fireball.json` and the V8.08 "Spongy" rules.*
