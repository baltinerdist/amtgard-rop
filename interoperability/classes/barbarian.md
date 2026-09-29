---
title: "Barbarian — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
kind: martial
immunities: ["Command", "Subdual"]
---

# Barbarian — Interoperability

[Class rules](../../rules/classes/barbarian.md) · Martial · 5 abilities on its list, 1 of which can affect another player.

## Defenses

- Immune to Command, Subdual. Any targeting ability from those Schools does not work on the player. Immunities do not extend to carried equipment or worn armor, and Enchantments still apply (Enchantments rule 3).

Archetypes (ignored in this model): Raider, Berserker.

Look The Part (available from 1st level): [Rage](../abilities/rage.md).

## Abilities by level

| Level | Ability | Cost | Max | Frequency | Type | School | Range | Affects others | Blocked on |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1st | [Berserk](../abilities/berserk.md) | - | - | - | Trait | Sorcery | Self | no | - |
| 1st | Immune to Command (Trait) | - | - | always on | Trait | Command | - | no | - |
| 1st | Immune to Subdual (Trait) | - | - | always on | Trait | Subdual | - | no | - |
| 2nd | [Rage](../abilities/rage.md) — Look The Part | - | - | 1/Refresh Charge x10 | Verbal | Sorcery | Self | no | - |
| 3rd | [Adrenaline](../abilities/adrenaline.md) | - | - | Unlimited | Verbal | Spirit | Self | no | - |
| 4th | [Rage](../abilities/rage.md) — Look The Part | - | - | 1/Refresh Charge x10 | Verbal | Sorcery | Self | no | - |
| 5th | [Brutal Strike](../abilities/brutal-strike.md) | - | - | 1/Life Charge x3 | Verbal | Death | Unlimited | yes | Paladin |
| 6th | [Blood and Thunder](../abilities/blood-and-thunder.md) | - | - | Unlimited | Verbal | Spirit | Self | no | - |

## What blocks on Barbarian

24 class-list entries across all classes cannot fully affect a Barbarian:

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
| [Abeyance](../abilities/abeyance.md) | Healer | Blocked | Immune to Subdual |
| [Entangle](../abilities/entangle.md) | Druid | Blocked | Immune to Subdual |
| [Entangle](../abilities/entangle.md) | Healer | Blocked | Immune to Subdual |
| [Entangle](../abilities/entangle.md) | Wizard | Blocked | Immune to Subdual |
| [Iceball](../abilities/iceball.md) | Druid | Blocked | Immune to Subdual |
| [Iceball](../abilities/iceball.md) | Healer | Blocked | Immune to Subdual |
| [Iceball](../abilities/iceball.md) | Wizard | Blocked | Immune to Subdual |
| [Suppression Bolt](../abilities/suppression-bolt.md) | Wizard | Blocked | Immune to Subdual |

## What Barbarian abilities do to each class

| Target class | Works | Blocked | Blocked abilities |
| --- | --- | --- | --- |
| [Anti-Paladin](anti-paladin.md) | 1 | 0 | - |
| [Archer](archer.md) | 1 | 0 | - |
| [Assassin](assassin.md) | 1 | 0 | - |
| [Barbarian](barbarian.md) | 1 | 0 | - |
| [Monk](monk.md) | 1 | 0 | - |
| [Paladin](paladin.md) | 0 | 1 | Brutal Strike |
| [Scout](scout.md) | 1 | 0 | - |
| [Warrior](warrior.md) | 1 | 0 | - |
| [Bard](bard.md) | 1 | 0 | - |
| [Druid](druid.md) | 1 | 0 | - |
| [Healer](healer.md) | 1 | 0 | - |
| [Wizard](wizard.md) | 1 | 0 | - |

## Abilities shared with other classes

| Class | Shared | Abilities |
| --- | --- | --- |
| [Anti-Paladin](anti-paladin.md) | 1 | [Brutal Strike](../abilities/brutal-strike.md) |

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`.*
