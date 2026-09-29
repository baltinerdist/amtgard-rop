---
title: "Raise Dead"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Raise Dead

> Returns a willing dead player (within 5' of where they died) to life, healed but Cursed, Suppressed 30 seconds, losing non-Persistent Enchantments.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Death |
| Range | Touch |
| Incantation | "Rise and fight again" x5 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | revival, healing · for: ally |
| Capabilities | curses, dispels, has-drawback, heals, revives, silences |
| Rule text | [rules/magic-and-abilities/raise-dead.md](../../rules/magic-and-abilities/raise-dead.md) · [interoperability](../../interoperability/abilities/raise-dead.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Healer | 3rd | 1 | - | 1/Life | 1 | life | - | (m) | Other | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Removes Enchantments** | dead-target | harm | scope non-persistent; instant — Removed before the player returns to life. | E3 |
| e2 | **Returns to life** | dead-target | benefit | instant | E1 |
| e3 | **Curses** | dead-target | harm | until respawn — Drawback. No duration given; per the Cursed State it persists after death and is removed on respawn. | E1 |
| e4 | **Suppresses** | dead-target | harm | 30 s | E2 |
| e5 | **Heals wounds** | dead-target | benefit | amount all; instant | E4 |

**Drawbacks:** Removes Enchantments (dead-target); Curses (dead-target); Suppresses (dead-target)

## Requirements

- **target-willing**: target must be willing *(E1)*
- **target-dead**: target must be dead *(E1)*
- **target-not-moved-5ft**: dead target must not have moved more than 5' (or be at respawn when stated) — Has not moved more than 5' from where they died. *(E1)*

## Names in the text

- state **cursed**: mentions *(E1)*
- state **suppressed**: mentions *(E2)*
- mechanic **persistent**: mentions *(E3)*
- mechanic **enchantments**: mentions *(E3)*

## What can stop or blunt it

Derived from the other records: abilities and traits that make their bearer immune, resistant or unaffected in a way that covers this ability.

| Protection | How | Who has it |
| --- | --- | --- |
| [Sleight of Mind](sleight-of-mind.md) | Enchantments cannot be removed | Bard |
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

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does less than | [Greater Resurrect](greater-resurrect.md) | only Raise Dead: Removes Enchantments (dead-target, instant); only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); only Greater Resurrect: Ends Cursed (dead-target, instant); property only in Greater Resurrect: bypass-cursed, bypass-states; school: Death vs Spirit |
| same plus a drawback or cost | [Resurrect](resurrect.md) | only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); school: Death vs Spirit |
| is given by | [Undead Minion](undead-minion.md) | only Raise Dead: Removes Enchantments (dead-target, instant); only Raise Dead: Returns to life (dead-target, instant); only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); only Raise Dead: Heals wounds (dead-target, amount all, instant); only Undead Minion: Curses (bearer, while worn); only Undead Minion: Prevents respawning (bearer, while worn); only Undead Minion: Grants Raise Dead (caster-of-enchantment, while worn) |

## Open questions

- Subject after revival is a living player; 'dead-target' used for all effects because the ability targets a dead player.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target willing dead player who has not moved more than 5' from where they died is returned to life and is Cursed. | effect e2 (Returns to life); effect e3 (Curses); requirement target-willing; requirement target-dead; requirement target-not-moved-5ft; names cursed |
| E2 | Target is also Suppressed for 30 seconds. | effect e4 (Suppresses); names suppressed |
| E3 | Non-Persistent Enchantments on the player are removed before the player returns to life. | effect e1 (Removes Enchantments); names persistent; names enchantments |
| E4 | Any wounds on the player are healed. | effect e5 (Heals wounds) |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/raise-dead.json` and the V8.08 "Spongy" rules.*
