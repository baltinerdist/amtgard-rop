---
title: "Sphere of Annihilation"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Sphere of Annihilation

> Magic Ball ignoring armor and Enchantments: the player hit dies and is Cursed; Weapon and Shield Destroying.

| | |
| --- | --- |
| Type | Magic Ball (magic-ball) |
| School | Sorcery |
| Range | - |
| Incantation | "The power of void is mine to evoke" x3 |
| Materials | Black Magic Ball |
| Magical | yes, (m) for at least one class |
| Roles | offense, equipment, debuff · for: enemy |
| Capabilities | attacks-equipment, can-be-lethal, causes-death, curses, defeats-armor |
| Rule text | [rules/magic-and-abilities/sphere-of-annihilation.md](../../rules/magic-and-abilities/sphere-of-annihilation.md) · [interoperability](../../interoperability/abilities/sphere-of-annihilation.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wizard | 6th | 2 | 1 | 1 Ball / Unlimited | 1 balls | unlimited | - | (m) | - | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Weapon Destroying (this magic ball)** | struck-player | harm | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor | E1 |
| e2 | **Shield Destroying (this magic ball)** | struck-player | harm | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor — Enchantments do not help: an Imbued Shield is still destroyed (N1). | E1, N1 |
| e3 | **Causes death** | struck-player | harm | instant; when a weapon, arrow or ball strikes the subject or their armor — Enchantments do not help: a player with Phoenix Tears stays dead (N1). | E2, N1 |
| e4 | **Curses** | struck-player | harm | until respawn; when a weapon, arrow or ball strikes the subject or their armor — No duration given; per the Cursed State it persists after death and is removed on respawn. | E2 |

## Properties

- **bypass-armor**: ignores armor *(E1)*
- **bypass-enchantments**: ignores Enchantments — e.g. Phoenix Tears does not save the player and an Imbued Shield is still destroyed (N1). *(E1, N1)*

## Clarifications in the text

- Because it ignores Enchantments, a player enchanted with Phoenix Tears stays dead and an Imbued Shield is still destroyed. *(N1)*

## Names in the text

- special-effect **weapon-destroying**: mentions *(E1)*
- special-effect **shield-destroying**: mentions *(E1)*
- state **cursed**: mentions *(E2)*
- ability **[Phoenix Tears](phoenix-tears.md)**: example *(N1)*
- ability **[Imbue](imbue.md)**: example *(N1)*
- mechanic **magic-balls**: mentions *(E1)*
- mechanic **armor**: mentions *(E1)*
- mechanic **enchantments**: mentions *(E1, N1)*
- mechanic **shield**: mentions *(N1)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Missile Block](missile-block.md) | Can block it by hand | Monk |
| [Adaptive Protection](adaptive-protection.md) | Immune (chosen School) | Healer, Scout |
| [Adaptive Blessing](adaptive-blessing.md) | Resistant (chosen School, next ability) | Healer |
| [Blessed Aura](blessed-aura.md) | Resistant to the next source | Healer |
| [Blessing Against Harm](blessing-against-harm.md) | Resistant to the next source | Healer, Wizard |
| [Sanctuary](sanctuary.md) | Unaffected by hostile actions within 20ft | Monk |
| [Protection from Magic](protection-from-magic.md) | Unaffected by magical abilities | Healer, Paladin, Wizard |
| [Void Touched](void-touched.md) | Unaffected by schools | Anti-Paladin, Wizard |

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does more than | [Assassinate](assassinate.md) | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Causes death (struck-player, instant); requirement only in Assassinate: immediately-after-kill, target-dead; property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; property only in Assassinate: no-verbal-targeting; delivery: magic-ball vs verbal; school: Sorcery vs Death |
| does more than | [Call Lightning](call-lightning.md) | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Curses (struck-player, until respawn); property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; delivery: magic-ball vs verbal; school: Sorcery vs Flame; range: - vs 20' |
| does more than | [Coup de Grace](coup-de-grace.md) | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Curses (struck-player, until respawn); requirement only in Coup de Grace: target-wounded; property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; delivery: magic-ball vs verbal; school: Sorcery vs Death; range: - vs 20' |
| does more than | [Dimensional Rift](dimensional-rift.md) | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Curses (struck-player, until respawn); requirement only in Dimensional Rift: target-insubstantial; property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; delivery: magic-ball vs verbal; range: - vs 20' |
| does more than | [Dragged Below](dragged-below.md) | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Curses (struck-player, until respawn); requirement only in Dragged Below: target-stopped; property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; delivery: magic-ball vs verbal; school: Sorcery vs Death; range: - vs 20' |
| does more than | [Finger of Death](finger-of-death.md) | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Curses (struck-player, until respawn); property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; delivery: magic-ball vs verbal; school: Sorcery vs Death; range: - vs 20' |
| does more than | [Shatter](shatter.md) | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Curses (struck-player, until respawn); requirement only in Shatter: target-frozen; property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; delivery: magic-ball vs verbal; range: - vs 20' |
| overlap | [Fireball](fireball.md) | only Sphere of Annihilation: Curses (struck-player, until respawn); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; school: Sorcery vs Flame |

## Open questions

- 'Ignores armor' does not say whether Magic Armor from a Trait (not an Enchantment) is ignored; bypass-magic-armor was not recorded.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | This Magic Ball is Weapon Destroying, Shield Destroying, and ignores armor and Enchantments. | effect e1 (Weapon Destroying (this magic ball)); effect e2 (Shield Destroying (this magic ball)); property bypass-armor; property bypass-enchantments; names weapon-destroying; names shield-destroying; names magic-balls; names armor; names enchantments |
| E2 | Player hit dies and is Cursed. | effect e3 (Causes death); effect e4 (Curses); names cursed |
| N1 | Because Sphere of Annihilation ignores Enchantments, a player enchanted with Phoenix Tears would remain dead after being killed, and an Imbued Shield would still be destroyed. | effect e2 (Shield Destroying (this magic ball)); effect e3 (Causes death); property bypass-enchantments; names Phoenix Tears; names Imbue; names enchantments; names shield; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/sphere-of-annihilation.json` and the V8.08 "Spongy" rules.*
