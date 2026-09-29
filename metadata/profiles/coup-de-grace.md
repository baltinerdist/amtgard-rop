---
title: "Coup de Grace"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Coup de Grace

> Kills a target within 20' who was wounded when the Incantation began, even if healed before it ends.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Death |
| Range | 20' |
| Incantation | "Death shall come for thee" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | offense · for: enemy |
| Capabilities | can-be-lethal, causes-death |
| Rule text | [rules/magic-and-abilities/coup-de-grace.md](../../rules/magic-and-abilities/coup-de-grace.md) · [interoperability](../../interoperability/abilities/coup-de-grace.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Assassin | 6th | - | - | 1/Life | 1 | life | - | (m) | 20' | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Causes death** | target | harm | instant | E1, N1 |

## Requirements

- **target-wounded**: target must be wounded when the incantation begins — Checked when the caster begins the Incantation (N1: still dies if healed by the end). *(L1)*

## Clarifications in the text

- The target still dies even if they have no wounds by the end of the Incantation. *(N1)*

## Names in the text

- mechanic **incantation**: mentions *(L1, N1)*

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
| [Protection from Magic](protection-from-magic.md) | Unaffected by magical abilities | Healer, Paladin, Wizard |
| [Void Touched](void-touched.md) | Unaffected by schools | Anti-Paladin, Wizard |
| [Rage](rage.md) | Unaffected by verbal abilities | Barbarian |
| [Enlightened Soul](enlightened-soul.md) | Unaffected by verbal magical beyond touch | Healer, Monk |
| [Enlightened Soul](enlightened-soul.md) | Unaffected by verbal magical beyond touch | Healer, Monk |

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| same-effects | [Call Lightning](call-lightning.md) | requirement only in Coup de Grace: target-wounded; school: Death vs Flame |
| same-effects | [Dimensional Rift](dimensional-rift.md) | requirement only in Coup de Grace: target-wounded; requirement only in Dimensional Rift: target-insubstantial; school: Death vs Sorcery |
| same-effects | [Dragged Below](dragged-below.md) | requirement only in Coup de Grace: target-wounded; requirement only in Dragged Below: target-stopped |
| same-effects | [Finger of Death](finger-of-death.md) | requirement only in Coup de Grace: target-wounded |
| does less than | [Fireball](fireball.md) | only Fireball: Weapon Destroying (this magic ball) (struck-player, instant); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Fireball: Shield Destroying (this magic ball) (struck-player, instant); requirement only in Coup de Grace: target-wounded; delivery: verbal vs magic-ball; school: Death vs Flame; range: 20' vs - |
| same-effects | [Shatter](shatter.md) | requirement only in Coup de Grace: target-wounded; requirement only in Shatter: target-frozen; school: Death vs Sorcery |
| does less than | [Sphere of Annihilation](sphere-of-annihilation.md) | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Curses (struck-player, until respawn); requirement only in Coup de Grace: target-wounded; property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; delivery: verbal vs magic-ball; school: Death vs Sorcery; range: 20' vs - |

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target player dies. | effect e1 (Causes death) |
| L1 | Target must be wounded when the caster begins the Incantation. | requirement target-wounded; names incantation |
| N1 | Even if the target has no wounds at the end of the Incantation they will still die. | effect e1 (Causes death); names incantation; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/coup-de-grace.json` and the V8.08 "Spongy" rules.*
