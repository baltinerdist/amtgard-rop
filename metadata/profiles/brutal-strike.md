---
title: "Brutal Strike"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Brutal Strike

> Wound Trigger: the player just wounded (or killed) is Cursed indefinitely and Suppressed for 30 seconds; no verbal targeting.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Death |
| Range | Unlimited |
| Incantation | "And stay down!" |
| Materials | none |
| Magical | no |
| Roles | debuff, control, anti-magic · for: enemy |
| Capabilities | castable-while-moving, curses, silences |
| Rule text | [rules/magic-and-abilities/brutal-strike.md](../../rules/magic-and-abilities/brutal-strike.md) · [interoperability](../../interoperability/abilities/brutal-strike.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Anti-Paladin | 4th | - | - | 1/Life Charge x10 | 1 | life | x10 | (ex) | Unlimited | Ambulant |
| Barbarian | 5th | - | - | 1/Life Charge x3 | 1 | life | x3 | (ex) | Unlimited | Ambulant |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Curses** | target | harm | until respawn; after the caster wounds an enemy (Wound Trigger) — Cursed indefinitely. The target is the wounded or dead player (N1). The text says "indefinitely"; Cursed is removed on respawn (Cursed definition). | E1, L1, N1 |
| e2 | **Suppresses** | target | harm | 30 s; after the caster wounds an enemy (Wound Trigger) | E2, L1, N1 |

## Requirements

- **immediately-after-wound**: only immediately after the caster wounds an enemy *(L1)*

## Properties

- **wound-trigger**: Wound Trigger *(L1)*
- **no-verbal-targeting**: does not require verbal targeting *(N1)*

## Clarifications in the text

- Brutal Strike automatically targets the player just wounded, or killed, by the caster; no verbal targeting is needed. *(N1)*

## Names in the text

- state **cursed**: mentions *(E1)*
- state **suppressed**: mentions *(E2)*
- mechanic **trigger**: mentions *(L1)*

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
| overlap | [Assassinate](assassinate.md) | only Brutal Strike: Suppresses (target, 30 s); requirement only in Brutal Strike: immediately-after-wound; requirement only in Assassinate: immediately-after-kill, target-dead; property only in Brutal Strike: wound-trigger; range: Unlimited vs 50' |
| overlap | [Break Concentration](break-concentration.md) | Suppresses: 30 s vs 10 s; only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; school: Death vs Command; range: Unlimited vs 20' |
| overlap | [Suppress Aura](suppress-aura.md) | only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; school: Death vs Command; range: Unlimited vs 50' |
| overlap | [Suppression Arrow](suppression-arrow.md) | only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; property only in Suppression Arrow: engulfing; delivery: verbal vs specialty-arrow; school: Death vs Sorcery; range: Unlimited vs - |
| overlap | [Suppression Bolt](suppression-bolt.md) | Suppresses: 30 s vs 60 s; only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; property only in Suppression Bolt: engulfing; delivery: verbal vs magic-ball; school: Death vs Subdual; range: Unlimited vs - |

## Open questions

- N1 allows a dead target, but States normally cannot apply to dead players unless noted; unclear whether the 30-second Suppressed of E2 applies when the target is dead (Cursed persists after death).

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target player is Cursed indefinitely. | effect e1 (Curses); names cursed |
| E2 | Target player is also Suppressed for 30 seconds. | effect e2 (Suppresses); names suppressed |
| L1 | Wound Trigger. | effect e1 (Curses); effect e2 (Suppresses); requirement immediately-after-wound; property wound-trigger; names trigger |
| N1 | Brutal Strike targets the wounded or dead player and does not require verbal targeting. | effect e1 (Curses); effect e2 (Suppresses); property no-verbal-targeting; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/brutal-strike.json` and the V8.08 "Spongy" rules.*
