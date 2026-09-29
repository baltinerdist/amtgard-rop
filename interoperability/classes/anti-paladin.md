---
title: "Anti-Paladin — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
kind: martial
immunities: ["Command", "Flame"]
---

# Anti-Paladin — Interoperability

[Class rules](../../rules/classes/anti-paladin.md) · Martial · 5 abilities on its list, 3 of which can affect another player.

## Defenses

- Immune to Command, Flame. Any targeting ability from those Schools does not work on the player. Immunities do not extend to carried equipment or worn armor, and Enchantments still apply (Enchantments rule 3).

Archetypes (ignored in this model): Infernal, Corruptor.

Look The Part (available from 1st level): [Terror](../abilities/terror.md).

## Abilities by level

| Level | Ability | Cost | Max | Frequency | Type | School | Range | Affects others | Blocked on |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1st | Immune to Command (Trait) | - | - | always on | Trait | Command | - | no | - |
| 1st | Immune to Flame (Trait) | - | - | always on | Trait | Flame | - | no | - |
| 2nd | [Poison](../abilities/poison.md) | - | - | 1/Life Charge x3 | Enchantment | Death | Self | no | - |
| 3rd | [Steal Life Essence](../abilities/steal-life-essence.md) | - | - | 1/Life Charge x5 | Verbal | Death | Touch | yes | Paladin |
| 4th | [Brutal Strike](../abilities/brutal-strike.md) | - | - | 1/Life Charge x10 | Verbal | Death | Unlimited | yes | Paladin |
| 5th | [Terror](../abilities/terror.md) — Look The Part | - | - | 1/Life | Verbal | Death | 20' | yes | Monk, Paladin |
| 6th | [Flame Blade](../abilities/flame-blade.md) | - | - | 2/Refresh | Enchantment | Flame | Self | no | - |

## What blocks on Anti-Paladin

21 class-list entries across all classes cannot fully affect an Anti-Paladin:

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
| [Call Lightning](../abilities/call-lightning.md) | Druid | Blocked | Immune to Flame |
| [Heat Weapon](../abilities/heat-weapon.md) | Druid | Blocked | Immune to Flame. Its target is the weapon, but a Flame-Immune player may keep wielding it, so it has no effect on them |
| [Heat Weapon](../abilities/heat-weapon.md) | Wizard | Blocked | Immune to Flame. Its target is the weapon, but a Flame-Immune player may keep wielding it, so it has no effect on them |
| [Lightning Bolt](../abilities/lightning-bolt.md) | Wizard | Partly blocked: equipment still hit | Immune to Flame. Weapon Destroying and Armor Breaking still hit their equipment (Immune rule 2) |
| [Fireball](../abilities/fireball.md) | Wizard | Partly blocked: equipment still hit | Immune to Flame. Weapon, Armor and Shield Destroying still hit their equipment (Immune rule 2) |

## What Anti-Paladin abilities do to each class

| Target class | Works | Blocked | Blocked abilities |
| --- | --- | --- | --- |
| [Anti-Paladin](anti-paladin.md) | 3 | 0 | - |
| [Archer](archer.md) | 3 | 0 | - |
| [Assassin](assassin.md) | 3 | 0 | - |
| [Barbarian](barbarian.md) | 3 | 0 | - |
| [Monk](monk.md) | 2 | 1 | Terror |
| [Paladin](paladin.md) | 0 | 3 | Steal Life Essence, Brutal Strike, Terror |
| [Scout](scout.md) | 3 | 0 | - |
| [Warrior](warrior.md) | 3 | 0 | - |
| [Bard](bard.md) | 3 | 0 | - |
| [Druid](druid.md) | 3 | 0 | - |
| [Healer](healer.md) | 3 | 0 | - |
| [Wizard](wizard.md) | 3 | 0 | - |

## Abilities shared with other classes

| Class | Shared | Abilities |
| --- | --- | --- |
| [Assassin](assassin.md) | 1 | [Poison](../abilities/poison.md) |
| [Barbarian](barbarian.md) | 1 | [Brutal Strike](../abilities/brutal-strike.md) |
| [Bard](bard.md) | 1 | [Terror](../abilities/terror.md) |
| [Druid](druid.md) | 2 | [Poison](../abilities/poison.md), [Flame Blade](../abilities/flame-blade.md) |
| [Healer](healer.md) | 1 | [Steal Life Essence](../abilities/steal-life-essence.md) |
| [Wizard](wizard.md) | 1 | [Steal Life Essence](../abilities/steal-life-essence.md) |

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`.*
