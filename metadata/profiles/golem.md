---
title: "Golem"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Golem

> Bearer is Immune to Death and Cursed, Mend removes their wounds, their Enchantments are Persistent, and they may respawn at or base on the caster.

| | |
| --- | --- |
| Type | Enchantment (enchantment) |
| School | Sorcery |
| Range | Other |
| Incantation | "From earth and clay I form thee" x3 |
| Materials | White strip and yellow strip |
| Magical | yes, (m) for at least one class |
| Roles | defense, healing, utility · for: ally |
| Capabilities | has-drawback, heals, protects, team-base |
| Drawbacks from limits | the bearer may not be treated as an Alternate Base, the caster may not use Alternate Bases |
| Rule text | [rules/magic-and-abilities/golem.md](../../rules/magic-and-abilities/golem.md) · [interoperability](../../interoperability/abilities/golem.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Druid | 4th | 1 | - | 1/Refresh | 1 | refresh | - | (m) | Other | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Immune to Death** | bearer | benefit | while worn; continuously while it is worn, chanted or in effect | E1 |
| e2 | **Curses** | bearer | harm | while worn; continuously while it is worn, chanted or in effect | E2 |
| e3 | **Changes Mend** | bearer | benefit | change Mend can remove a wound from the bearer; while worn; continuously while it is worn, chanted or in effect — Greater Mend and Word of Mending do not remove a wound (N1). | E3, N1 |
| e4 | **Heals wounds** | bearer | benefit | amount one; instant; continuously while it is worn, chanted or in effect — A wound on the bearer can be removed via Mend (E3); Greater Mend and Word of Mending will not remove it (N1). Text does not limit how often. | E3, N1 |
| e5 | **Acts as a respawn point** | caster-of-enchantment | neutral | for bearer-only; while worn; continuously while it is worn, chanted or in effect; only if while the caster is alive — Bearer may use the caster as an alternate respawn point while the caster is alive. | E4 |
| e6 | **Acts as an Alternate Base** | caster-of-enchantment | neutral | for bearer-only; while worn; continuously while it is worn, chanted or in effect | E5 |
| e7 | **Makes Enchantments Persistent** | bearer | benefit | which all-worn; while worn; continuously while it is worn, chanted or in effect — All Enchantments worn by the bearer, including Golem, are Persistent while Golem is worn. | E6 |
| e8 | **May not use alternate bases** | caster-of-enchantment | harm | what use-alternate-bases; while worn; continuously while it is worn, chanted or in effect — Drawback on the caster. | L1 |

**Drawbacks:** Curses (bearer); May not use alternate bases (caster-of-enchantment)

## Restrictions

- **one-active-per-caster**: a caster may only have one active at a time *(L1)*
- **caster-may-not-use-alternate-bases**: the caster may not use Alternate Bases *(L1)*
- **bearer-not-alternate-base**: the bearer may not be treated as an Alternate Base *(L2)*

## Properties

- **persistent**: the Enchantment is Persistent (returns after respawn) *(E6)*
- **active-while-dead**: remains active while the bearer is dead *(E7)*

## Clarifications in the text

- Greater Mend and Word of Mending will not remove a wound from the bearer; only Mend does. *(N1)*

## Names in the text

- ability **[Mend](mend.md)**: modifies *(E3)*
- ability **[Greater Mend](greater-mend.md)**: mentions *(N1)*
- ability **[Word of Mending](word-of-mending.md)**: mentions *(N1)*
- ability **[Immune to Death](immune-to-death.md)**: mentions *(E1)*
- state **cursed**: mentions *(E2)*
- mechanic **immune**: mentions *(E1)*
- mechanic **respawn**: mentions *(E4)*
- mechanic **alternate-base**: mentions *(E5, L1, L2)*
- mechanic **persistent**: mentions *(E6)*
- mechanic **enchantments**: mentions *(E6)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does more than | [Adrenaline](adrenaline.md) | only Golem: Immune to Death (bearer, while worn); only Golem: Curses (bearer, while worn); only Golem: Changes Mend (bearer, while worn); only Golem: Acts as a respawn point (caster-of-enchantment, while worn, if caster-alive); only Golem: Acts as an Alternate Base (caster-of-enchantment, while worn); only Golem: Makes Enchantments Persistent (bearer, while worn); only Golem: May not use alternate bases (caster-of-enchantment, while worn); requirement only in Adrenaline: immediately-after-kill |
| does more than | [Protection from Evil](protection-from-evil.md) | only Golem: Curses (bearer, while worn); only Golem: Changes Mend (bearer, while worn); only Golem: Heals wounds (bearer, amount one, instant); only Golem: Acts as a respawn point (caster-of-enchantment, while worn, if caster-alive); only Golem: Acts as an Alternate Base (caster-of-enchantment, while worn); only Golem: Makes Enchantments Persistent (bearer, while worn); only Golem: May not use alternate bases (caster-of-enchantment, while worn); restriction only in Golem: bearer-not-alternate-base, caster-may-not-use-alternate-bases |

## Open questions

- E3 does not say how many wounds or how often Mend removes one; recorded literally as one wound per Mend.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Bearer is Immune to Death. | effect e1 (Immune to Death); names Immune to Death; names immune |
| E2 | Bearer is Cursed. | effect e2 (Curses); names cursed |
| E3 | Bearer can remove a wound via Mend. | effect e3 (Changes Mend); effect e4 (Heals wounds); names Mend |
| E4 | Bearer may use the caster as an alternate respawn point while the caster is alive. | effect e5 (Acts as a respawn point); names respawn |
| E5 | Bearer may treat the caster as an Alternate Base. | effect e6 (Acts as an Alternate Base); names alternate-base |
| E6 | All Enchantments worn by the Bearer, including Golem, are Persistent while Golem is worn. | effect e7 (Makes Enchantments Persistent); property persistent; names persistent; names enchantments |
| E7 | Golem remains active while the bearer is dead. | property active-while-dead |
| L1 | A caster may only have a single Golem Enchantment at a time and may not use Alternate Bases. | effect e8 (May not use alternate bases); restriction one-active-per-caster; restriction caster-may-not-use-alternate-bases; names alternate-base |
| L2 | Bearer may not be treated as an Alternate Base. | restriction bearer-not-alternate-base; names alternate-base |
| N1 | Greater Mend and Word of Mending will not remove a wound. | effect e3 (Changes Mend); effect e4 (Heals wounds); names Greater Mend; names Word of Mending; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/golem.json` and the V8.08 "Spongy" rules.*
