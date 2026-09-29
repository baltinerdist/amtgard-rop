---
title: "Paladin — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
kind: martial
immunities: ["Command", "Death"]
---

# Paladin — Interoperability

[Class rules](../../rules/classes/paladin.md) · Martial · 5 abilities on its list, 5 of which can affect another player.

## Defenses

- Immune to Command, Death. Any targeting ability from those Schools does not work on the player. Immunities do not extend to carried equipment or worn armor, and Enchantments still apply (Enchantments rule 3).

Archetypes (ignored in this model): Guardian, Inquisitor.

Look The Part (available from 1st level): [Awe](../abilities/awe.md).

## Abilities by level

| Level | Ability | Cost | Max | Frequency | Type | School | Range | Affects others | Blocked on |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1st | Immune to Command (Trait) | - | - | always on | Trait | Command | - | no | - |
| 1st | Immune to Death (Trait) | - | - | always on | Trait | Death | - | no | - |
| 2nd | [Greater Heal](../abilities/greater-heal.md) | - | - | 1/Life Charge x3 | Verbal | Spirit | Touch | yes | - |
| 3rd | [Protection from Evil](../abilities/protection-from-evil.md) | - | - | 1/Refresh Charge x5 | Enchantment | Protection | Other | yes | - |
| 4th | [Greater Resurrect](../abilities/greater-resurrect.md) | - | - | 1/Life | Verbal | Spirit | Other | yes | - |
| 5th | [Awe](../abilities/awe.md) — Look The Part | - | - | 1/Life | Verbal | Command | 20' | yes | Anti-Paladin, Barbarian, Monk, Paladin |
| 6th | [Protection from Magic](../abilities/protection-from-magic.md) | - | - | 2/Refresh | Enchantment | Protection | Touch | yes | - |

## What blocks on Paladin

33 class-list entries across all classes cannot fully affect a Paladin:

| Ability | From class | Result | Why |
| --- | --- | --- | --- |
| [Agoraphobia](../abilities/agoraphobia.md) | Bard | Blocked | Immune to Command |
| [Astral Intervention](../abilities/astral-intervention.md) | Healer | Blocked | Immune to Command |
| [Astral Intervention](../abilities/astral-intervention.md) | Wizard | Blocked | Immune to Command |
| [Awe](../abilities/awe.md) | Bard | Blocked | Immune to Command |
| [Awe](../abilities/awe.md) | Paladin | Blocked | Immune to Command |
| [Break Concentration](../abilities/break-concentration.md) | Bard | Blocked | Immune to Command |
| [Break Concentration](../abilities/break-concentration.md) | Wizard | Blocked | Immune to Command |
| [Hold Person](../abilities/hold-person.md) | Assassin | Blocked | Immune to Command |
| [Hold Person](../abilities/hold-person.md) | Healer | Blocked | Immune to Command |
| [Hold Person](../abilities/hold-person.md) | Scout | Blocked | Immune to Command |
| [Hold Person](../abilities/hold-person.md) | Wizard | Blocked | Immune to Command |
| [Insult](../abilities/insult.md) | Bard | Blocked | Immune to Command |
| [Insult](../abilities/insult.md) | Warrior | Blocked | Immune to Command |
| [Lost](../abilities/lost.md) | Bard | Blocked | Immune to Command |
| [Suppress Aura](../abilities/suppress-aura.md) | Bard | Blocked | Immune to Command |
| [Suppress Aura](../abilities/suppress-aura.md) | Wizard | Blocked | Immune to Command |
| [Assassinate](../abilities/assassinate.md) | Assassin | Blocked | Immune to Death |
| [Brutal Strike](../abilities/brutal-strike.md) | Anti-Paladin | Blocked | Immune to Death |
| [Brutal Strike](../abilities/brutal-strike.md) | Barbarian | Blocked | Immune to Death |
| [Coup de Grace](../abilities/coup-de-grace.md) | Assassin | Blocked | Immune to Death |
| [Dragged Below](../abilities/dragged-below.md) | Wizard | Blocked | Immune to Death |
| [Finger of Death](../abilities/finger-of-death.md) | Wizard | Blocked | Immune to Death |
| [Raise Dead](../abilities/raise-dead.md) | Healer | Blocked | Immune to Death |
| [Ravage](../abilities/ravage.md) | Wizard | Blocked | Immune to Death |
| [Steal Life Essence](../abilities/steal-life-essence.md) | Anti-Paladin | Blocked | Immune to Death |
| [Steal Life Essence](../abilities/steal-life-essence.md) | Healer | Blocked | Immune to Death |
| [Steal Life Essence](../abilities/steal-life-essence.md) | Wizard | Blocked | Immune to Death |
| [Terror](../abilities/terror.md) | Anti-Paladin | Blocked | Immune to Death |
| [Terror](../abilities/terror.md) | Bard | Blocked | Immune to Death |
| [Wounding](../abilities/wounding.md) | Wizard | Blocked | Immune to Death |
| [Undead Minion](../abilities/undead-minion.md) | Healer | Partly blocked: enchantment applies, granted Raise Dead cannot | Immune to Death. The enchantment itself applies (Enchantments rule 3), but the Raise Dead it grants is affected normally by Immunity (rule 3b) |
| [Poison Arrow](../abilities/poison-arrow.md) | Archer | Partly blocked: arrow still lands as a normal hit | Immune to Death. Wounds Kill is Death School so it does nothing, but a Specialty Arrow still counts as a normal arrow hit (Specialty Arrows rule 5) |
| [Poison Arrow](../abilities/poison-arrow.md) | Assassin | Partly blocked: arrow still lands as a normal hit | Immune to Death. Wounds Kill is Death School so it does nothing, but a Specialty Arrow still counts as a normal arrow hit (Specialty Arrows rule 5) |

## What Paladin abilities do to each class

| Target class | Works | Blocked | Blocked abilities |
| --- | --- | --- | --- |
| [Anti-Paladin](anti-paladin.md) | 4 | 1 | Awe |
| [Archer](archer.md) | 5 | 0 | - |
| [Assassin](assassin.md) | 5 | 0 | - |
| [Barbarian](barbarian.md) | 4 | 1 | Awe |
| [Monk](monk.md) | 4 | 1 | Awe |
| [Paladin](paladin.md) | 4 | 1 | Awe |
| [Scout](scout.md) | 5 | 0 | - |
| [Warrior](warrior.md) | 5 | 0 | - |
| [Bard](bard.md) | 5 | 0 | - |
| [Druid](druid.md) | 5 | 0 | - |
| [Healer](healer.md) | 5 | 0 | - |
| [Wizard](wizard.md) | 5 | 0 | - |

## Abilities shared with other classes

| Class | Shared | Abilities |
| --- | --- | --- |
| [Bard](bard.md) | 1 | [Awe](../abilities/awe.md) |
| [Healer](healer.md) | 3 | [Greater Heal](../abilities/greater-heal.md), [Greater Resurrect](../abilities/greater-resurrect.md), [Protection from Magic](../abilities/protection-from-magic.md) |
| [Wizard](wizard.md) | 1 | [Protection from Magic](../abilities/protection-from-magic.md) |

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`.*
