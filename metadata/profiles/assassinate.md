---
title: "Assassinate"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Assassinate

> Immediately after killing an enemy, Curses that dead enemy (within 50'); no verbal targeting needed.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Death |
| Range | 50' |
| Incantation | "Assassinate" |
| Materials | none |
| Magical | no |
| Roles | debuff · for: enemy |
| Capabilities | castable-while-moving, curses |
| Rule text | [rules/magic-and-abilities/assassinate.md](../../rules/magic-and-abilities/assassinate.md) · [interoperability](../../interoperability/abilities/assassinate.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Assassin | 1st | - | - | Unlimited | - | unlimited | - | (ex) | 50' | Ambulant |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Curses** | dead-target | harm | until respawn; after the caster kills an enemy (Kill Trigger) — Targets the enemy just killed. No duration is given; per the Cursed State rules it persists after death and is removed on respawn. | E1, L1, N1 |

## Requirements

- **immediately-after-kill**: only immediately after the caster kills an enemy *(L1)*
- **target-dead**: target must be dead — Targets the killed enemy. *(N1)*

## Properties

- **no-verbal-targeting**: does not require verbal targeting *(N1)*

## Clarifications in the text

- Assassinate automatically targets the enemy just killed; the caster does not need to verbally target them. *(N1)*

## Names in the text

- state **cursed**: mentions *(E1)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Golem](golem.md) | Immune | Druid |
| [Immune to Death](immune-to-death.md) | Immune | Paladin |
| [Protection from Evil](protection-from-evil.md) | Immune | Paladin |
| [Vampirism](vampirism.md) | Immune | Wizard |
| [Adaptive Protection](adaptive-protection.md) | Immune (chosen School) | Healer, Scout |
| [Adaptive Blessing](adaptive-blessing.md) | Resistant (chosen School, next ability) | Healer |
| [Blessed Aura](blessed-aura.md) | Resistant to the next source | Healer |
| [Blessing Against Harm](blessing-against-harm.md) | Resistant to the next source | Healer, Wizard |
| [Sanctuary](sanctuary.md) | Unaffected by hostile actions within 20ft | Monk |
| [Rage](rage.md) | Unaffected by verbal abilities | Barbarian |

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does less than | [Sphere of Annihilation](sphere-of-annihilation.md) | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Causes death (struck-player, instant); requirement only in Assassinate: immediately-after-kill, target-dead; property only in Assassinate: no-verbal-targeting; property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; delivery: verbal vs magic-ball; school: Death vs Sorcery |
| overlap | [Brutal Strike](brutal-strike.md) | only Brutal Strike: Suppresses (target, 30 s); requirement only in Assassinate: immediately-after-kill, target-dead; requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: wound-trigger; range: 50' vs Unlimited |
| overlap | [Protection from Magic](protection-from-magic.md) | only Assassinate: Curses (dead-target, until respawn); only Protection from Magic: Unaffected by (bearer, while worn); only Protection from Magic: Curses (bearer, until respawn); requirement only in Assassinate: immediately-after-kill, target-dead; property only in Assassinate: no-verbal-targeting; delivery: verbal vs enchantment; school: Death vs Protection; range: 50' vs Other, Touch |
| overlap | [Sever Spirit](sever-spirit.md) | only Sever Spirit: Removes Enchantments (dead-target, instant); requirement only in Assassinate: immediately-after-kill; requirement only in Sever Spirit: target-dead-at-start; property only in Assassinate: no-verbal-targeting; property only in Sever Spirit: bypass-enchantments, bypass-immunities, bypass-ongoing-effects, bypass-states, bypass-traits; school: Death vs Spirit; range: 50' vs 20' |

## Open questions

- L1 says 'immediately upon killing an enemy' but does not call it a Kill Trigger; no kill-trigger property recorded (Kill Trigger rules such as 30 seconds and 10' from enemies are not stated). Timing on-kill used.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | The target is Cursed. | effect e1 (Curses); names cursed |
| L1 | May only be used immediately upon killing an enemy. | effect e1 (Curses); requirement immediately-after-kill |
| N1 | Assassinate targets the killed enemy and does not require verbal targeting. | effect e1 (Curses); requirement target-dead; property no-verbal-targeting; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/assassinate.json` and the V8.08 "Spongy" rules.*
