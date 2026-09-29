---
title: "Ancestral Armor"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Ancestral Armor

> Ignores Magic Ball, projectile and melee hits on the bearer's armor while that location has points; the armor loses one point instead. Reusable.

| | |
| --- | --- |
| Type | Enchantment (enchantment) |
| School | Protection |
| Range | Other (He), Self (Wa) |
| Incantation | "May this armor protect thee from all forms of harm" x3 |
| Materials | White strip |
| Magical | yes, (m) for at least one class |
| Roles | defense, equipment · for: ally |
| Capabilities | has-drawback, protects |
| Rule text | [rules/magic-and-abilities/ancestral-armor.md](../../rules/magic-and-abilities/ancestral-armor.md) · [interoperability](../../interoperability/abilities/ancestral-armor.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Warrior | 6th | - | - | 3/Refresh Charge x10 | 3 | refresh | x10 | (ex) | Self | Swift |
| Healer | 6th | 1 | - | 1/Refresh | 1 | refresh | - | (m) | Other | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Ignores a hit** | bearer | benefit | from hits-on-worn-armor; except effects phasing; instant; when a weapon, arrow or ball strikes the subject or their armor; only if the struck armor still has points — Magic Ball, projectile weapon or melee weapon striking worn armor is ignored, even if the object would not otherwise affect the armor. Phasing equipment is not ignored (N2). Not expended after use. | E1, E3, N2 |
| e2 | **Damages armor** | bearer-equipment | harm | points 1; instant; when a weapon, arrow or ball strikes the subject or their armor; only if the struck armor still has points — The armor loses one point of value in the location struck (the cost of each ignored hit). | E2, E3 |

**Drawbacks:** Damages armor (bearer-equipment)

## Properties

- **reusable**: not used up when it triggers; keeps working until removed — Not expended after use; continues until removed with Dispel Magic or similar abilities. *(E4)*

## Clarifications in the text

- Does not trigger if the armor has no points left in the location struck. *(E3)*
- Not expended after use; keeps protecting until removed by Dispel Magic or similar abilities. *(E4)*
- Engulfing effects that do not strike the armor, abilities that ignore armor entirely, and abilities entirely negated by Ability Order do not trigger it. *(N1)*
- Phasing equipment interacts with the bearer's armor as though Ancestral Armor were not present. *(N2)*

## Names in the text

- ability **[Dispel Magic](dispel-magic.md)**: countered-by *(E4)*
- special-effect **phasing**: mentions *(N2)*
- mechanic **engulfing**: mentions *(N1)*
- mechanic **ability-order**: mentions *(N1)*
- mechanic **armor**: mentions *(E1, E2, E3)*
- mechanic **magic-balls**: mentions *(E1)*
- mechanic **weapon**: mentions *(E1)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does less than | [Ironskin](ironskin.md) | only Ancestral Armor: Ignores a hit (bearer, instant, if armor-has-points); only Ancestral Armor: Damages armor (bearer-equipment, points 1, instant, if armor-has-points); only Ironskin: Immune to Flame (bearer, while worn); only Ironskin: Grants Magic Armor (bearer, points 2, while worn); only Ironskin: Works as Ancestral Armor (bearer, while worn); property only in Ancestral Armor: reusable; range: Other, Self vs Other |
| does less than | [Stoneskin](stoneskin.md) | only Ancestral Armor: Ignores a hit (bearer, instant, if armor-has-points); only Ancestral Armor: Damages armor (bearer-equipment, points 1, instant, if armor-has-points); only Stoneskin: Grants Magic Armor (bearer, points 2, while worn); only Stoneskin: Works as Ancestral Armor (bearer, while worn); property only in Ancestral Armor: reusable; range: Other, Self vs Other |

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | The effects of a Magic Ball, projectile weapon, or melee weapon which just struck armor worn by the player are ignored, even if the object would not otherwise affect the armor. | effect e1 (Ignores a hit); names armor; names magic-balls; names weapon |
| E2 | The armor loses one point of value in the location struck. | effect e2 (Damages armor); names armor |
| E3 | This effect will not trigger if the armor has no points left in the location struck. | effect e1 (Ignores a hit); effect e2 (Damages armor); names armor; clarification |
| E4 | Ancestral Armor is not expended after use and will continue to provide protection until removed with Dispel Magic or similar abilities. | property reusable; names Dispel Magic; clarification |
| N1 | Engulfing Effects that do not strike the bearer's armor, abilities that ignore armor entirely, and abilities that have been entirely negated due to Ability Order do not trigger Ancestral Armor. | names engulfing; names ability-order; clarification |
| N2 | Phasing equipment interacts with armor worn by the bearer as though Ancestral Armor was not present. | effect e1 (Ignores a hit); names phasing; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/ancestral-armor.json` and the V8.08 "Spongy" rules.*
