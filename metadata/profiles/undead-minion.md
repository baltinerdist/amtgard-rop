---
title: "Undead Minion"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Undead Minion

> Bearer is Cursed and cannot respawn; caster gains unlimited Raise Dead on the bearer only; up to three per caster; Persistent.

| | |
| --- | --- |
| Type | Enchantment (enchantment) |
| School | Death |
| Range | Other |
| Incantation | "Cheat thy death and arise, my undead minion!" x5 |
| Materials | Yellow strip |
| Magical | yes, (m) for at least one class |
| Roles | revival, utility · for: ally |
| Capabilities | grants-abilities, has-drawback, team-base · through granted abilities: curses, dispels, heals, revives, silences |
| Gives its user | [Raise Dead](raise-dead.md) |
| Drawbacks from limits | the bearer may not be treated as an Alternate Base, the caster may not use Alternate Bases |
| Rule text | [rules/magic-and-abilities/undead-minion.md](../../rules/magic-and-abilities/undead-minion.md) · [interoperability](../../interoperability/abilities/undead-minion.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Healer | 5th | 2 | - | 1/Refresh | 1 | refresh | - | (m) | Other | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Curses** | bearer | harm | while worn; continuously while it is worn, chanted or in effect | E1 |
| e2 | **Prevents respawning** | bearer | harm | while worn; continuously while it is worn, chanted or in effect | E1 |
| e3 | **Grants Raise Dead** | caster-of-enchantment | benefit | how gains; frequency (Unlimited) (m); while worn; continuously while it is worn, chanted or in effect — Only while the bearer is enchanted. | E2 |
| e4 | **Changes Raise Dead** | caster-of-enchantment | benefit | change the granted Raise Dead ignores the requirement that the target has not moved from where they died; while worn; continuously while it is worn, chanted or in effect | E2 |
| e5 | **Changes Raise Dead** | caster-of-enchantment | harm | change the granted Raise Dead can only be cast with the bearer as the target; while worn; continuously while it is worn, chanted or in effect — Limit on the granted ability. | E2 |
| e6 | **Acts as an Alternate Base** | caster-of-enchantment | neutral | for bearer-only; while worn; continuously while it is worn, chanted or in effect | E3 |
| e7 | **May not use alternate bases** | caster-of-enchantment | harm | what use-alternate-bases; while worn; continuously while it is worn, chanted or in effect — Drawback on the caster. | L1 |

**Drawbacks:** Curses (bearer); Prevents respawning (bearer); Changes Raise Dead (caster-of-enchantment); May not use alternate bases (caster-of-enchantment)

## Restrictions

- **max-active-per-caster**: a caster may have at most N active (give n) (3) *(L1)*
- **caster-may-not-use-alternate-bases**: the caster may not use Alternate Bases *(L1)*
- **bearer-not-alternate-base**: the bearer may not be treated as an Alternate Base *(L2)*

## Properties

- **persistent**: the Enchantment is Persistent (returns after respawn) *(E4)*
- **active-while-dead**: remains active while the bearer is dead *(E4)*

## Names in the text

- ability **[Raise Dead](raise-dead.md)**: grants *(E2)*
- ability **[Raise Dead](raise-dead.md)**: modifies *(E2)*
- state **cursed**: mentions *(E1)*
- mechanic **respawn**: mentions *(E1)*
- mechanic **alternate-base**: mentions *(E3, L1, L2)*
- mechanic **persistent**: mentions *(E4)*
- mechanic **enchantments**: mentions *(E4, L1)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| gives its user | [Raise Dead](raise-dead.md) | only Undead Minion: Curses (bearer, while worn); only Undead Minion: Prevents respawning (bearer, while worn); only Undead Minion: Grants Raise Dead (caster-of-enchantment, while worn); only Undead Minion: Changes Raise Dead (caster-of-enchantment, while worn); only Undead Minion: Changes Raise Dead (caster-of-enchantment, while worn); only Undead Minion: Acts as an Alternate Base (caster-of-enchantment, while worn); only Undead Minion: May not use alternate bases (caster-of-enchantment, while worn); only Raise Dead: Removes Enchantments (dead-target, instant) |

## Open questions

- E2 grants Raise Dead '(Unlimited)' without a range; presumably Raise Dead's own Touch range applies.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Bearer is Cursed and cannot Respawn. | effect e1 (Curses); effect e2 (Prevents respawning); names cursed; names respawn |
| E2 | While the bearer is enchanted, the caster gains Raise Dead (Unlimited) (m) which can only be cast with the bearer as the target, and ignores the requirement for the bearer to have not moved from where they died. | effect e3 (Grants Raise Dead); effect e4 (Changes Raise Dead); effect e5 (Changes Raise Dead); names Raise Dead; names Raise Dead |
| E3 | Bearer may treat the caster as an Alternate Base. | effect e6 (Acts as an Alternate Base); names alternate-base |
| E4 | This enchantment is Persistent, and remains active while the bearer is dead. | property persistent; property active-while-dead; names persistent; names enchantments |
| L1 | The caster may not have more than three Undead Minion Enchantments and may not use Alternate Bases. | effect e7 (May not use alternate bases); restriction max-active-per-caster; restriction caster-may-not-use-alternate-bases; names alternate-base; names enchantments |
| L2 | Bearer may not be treated as an Alternate Base. | restriction bearer-not-alternate-base; names alternate-base |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/undead-minion.json` and the V8.08 "Spongy" rules.*
