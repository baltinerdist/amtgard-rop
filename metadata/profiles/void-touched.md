---
title: "Void Touched"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Void Touched

> Armor Breaking melee weapons, Shadow Step 1/Refresh Charge x30, Steal Life Essence Unlimited, unaffected by Sorcery, Spirit and Death Magic; bearer is Cursed.

| | |
| --- | --- |
| Type | Enchantment (enchantment) |
| School | Sorcery |
| Range | Other (Wi) Self (Ap) |
| Incantation | "Embrace the old ones and surrender thyself " x3 |
| Materials | Red strip and white strip |
| Magical | yes, (m) for at least one class |
| Roles | offense, equipment, defense, anti-magic, healing · for: ally |
| Capabilities | defeats-armor, grants-abilities, has-drawback, protects · through granted abilities: castable-while-moving, curses, heals, makes-insubstantial, more-uses, self-protection-state |
| Gives its user | [Shadow Step](shadow-step.md), [Steal Life Essence](steal-life-essence.md) |
| Rule text | [rules/magic-and-abilities/void-touched.md](../../rules/magic-and-abilities/void-touched.md) · [interoperability](../../interoperability/abilities/void-touched.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wizard | 5th | 1 | 2 | 1/Refresh | 1 | refresh | - | (m) | Other | - |
| Anti-Paladin | 6th | - | - | - | - | - | - | - | - | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Armor Breaking (bearer melee weapons)** | bearer | benefit | on bearer-melee-weapons; while worn; continuously while it is worn, chanted or in effect — Wielded melee weapons. | E1 |
| e2 | **Grants Shadow Step** | bearer | benefit | how gains; frequency 1/Refresh Charge x30 (ex); while worn; continuously while it is worn, chanted or in effect | E2 |
| e3 | **Grants Steal Life Essence** | bearer | benefit | how gains; frequency Unlimited (ex); while worn; continuously while it is worn, chanted or in effect | E2 |
| e4 | **Unaffected by** | bearer | benefit | by schools; schools Sorcery, Spirit, Death; while worn; continuously while it is worn, chanted or in effect — Magical abilities only from the Sorcery, Spirit and Death Schools (Extraordinary ones still affect the bearer). Per N1 this does not interact with other Enchantments the bearer wears. | E2, N1 |
| e5 | **Curses** | bearer | harm | while worn; continuously while it is worn, chanted or in effect — Drawback on the bearer. | E3 |

**Drawbacks:** Curses (bearer)

## Clarifications in the text

- The 'unaffected by Magical abilities' effect does not interact with (remove or block) other Enchantments already worn by the bearer. *(N1)*

## Names in the text

- ability **[Shadow Step](shadow-step.md)**: grants *(E2)*
- ability **[Steal Life Essence](steal-life-essence.md)**: grants *(E2)*
- state **cursed**: mentions *(E3)*
- special-effect **armor-breaking**: mentions *(E1)*
- mechanic **charge**: mentions *(E2)*
- mechanic **refresh**: mentions *(E2)*
- mechanic **school**: mentions *(E2)*
- mechanic **enchantments**: mentions *(N1)*
- mechanic **weapon**: mentions *(E1)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does more than | [Berserk](berserk.md) | only Void Touched: Grants Shadow Step (bearer, while worn); only Void Touched: Grants Steal Life Essence (bearer, while worn); only Void Touched: Unaffected by (bearer, while worn); only Void Touched: Curses (bearer, while worn); range: Other vs Self |
| is given by | [Corruptor](corruptor.md) | only Void Touched: Armor Breaking (bearer melee weapons) (bearer, while worn); only Void Touched: Grants Shadow Step (bearer, while worn); only Void Touched: Grants Steal Life Essence (bearer, while worn); only Void Touched: Unaffected by (bearer, while worn); only Void Touched: Curses (bearer, while worn); only Corruptor: Grants Void Touched (bearer, permanent); only Corruptor: Changes Terror (bearer, permanent); only Corruptor: Changes how often abilities can be used (bearer, permanent) |
| gives its user | [Shadow Step](shadow-step.md) | only Void Touched: Armor Breaking (bearer melee weapons) (bearer, while worn); only Void Touched: Grants Shadow Step (bearer, while worn); only Void Touched: Grants Steal Life Essence (bearer, while worn); only Void Touched: Unaffected by (bearer, while worn); only Void Touched: Curses (bearer, while worn); only Shadow Step: Makes Insubstantial (caster, until removed); ends when only in Shadow Step: exit-at-will; property only in Shadow Step: castable-while-moving |
| gives its user | [Steal Life Essence](steal-life-essence.md) | only Void Touched: Armor Breaking (bearer melee weapons) (bearer, while worn); only Void Touched: Grants Shadow Step (bearer, while worn); only Void Touched: Grants Steal Life Essence (bearer, while worn); only Void Touched: Unaffected by (bearer, while worn); only Void Touched: Curses (bearer, while worn); only Steal Life Essence: Curses (dead-target, until respawn); only Steal Life Essence: Heals wounds (caster, amount one, instant); only Steal Life Essence: Instantly Charges an ability (caster, instant) |

## Open questions

- N1 'This effect does not interact with other Enchantments worn by the bearer' does not say which effect; read as the unaffected-by-Sorcery/Spirit/Death clause (so e.g. Sorcery or Spirit Enchantments already worn keep working).

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Bearer's wielded melee weapons are Armor Breaking. | effect e1 (Armor Breaking (bearer melee weapons)); names armor-breaking; names weapon |
| E2 | Bearer gains Shadow Step 1/Refresh Charge x30 (ex), Steal Life Essence Unlimited (ex), and is unaffected by Magical abilities from the Sorcery, Spirit, and Death Schools. | effect e2 (Grants Shadow Step); effect e3 (Grants Steal Life Essence); effect e4 (Unaffected by); names Shadow Step; names Steal Life Essence; names charge; names refresh; names school |
| E3 | Bearer is Cursed. | effect e5 (Curses); names cursed |
| N1 | This effect does not interact with other Enchantments worn by the bearer. | effect e4 (Unaffected by); names enchantments; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/void-touched.json` and the V8.08 "Spongy" rules.*
