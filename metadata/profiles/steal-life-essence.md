---
title: "Steal Life Essence"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Steal Life Essence

> Curses a dead, non-Cursed player by Touch; the caster may then heal one wound or instantly Charge an ability.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Death |
| Range | Touch |
| Incantation | "Steal life" |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | debuff, healing, resource · for: enemy |
| Capabilities | curses, heals, more-uses |
| Rule text | [rules/magic-and-abilities/steal-life-essence.md](../../rules/magic-and-abilities/steal-life-essence.md) · [interoperability](../../interoperability/abilities/steal-life-essence.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Anti-Paladin | 3rd | - | - | 1/Life Charge x5 | 1 | life | x5 | (m) | Touch | - |
| Healer | 5th | 1 | 2 | 1/Life | 1 | life | - | (m) | Touch | - |
| Wizard | 5th | 1 | 2 | 1/Life | 1 | life | - | (m) | Touch | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Curses** | dead-target | harm | until respawn — No duration given; per the Cursed State it persists after death and is removed on respawn. | E1 |
| e2 | **Heals wounds** | caster | benefit | amount one; instant; choice g1 option 1 — Caster heals one of their own wounds. | E2, N1 |
| e3 | **Instantly Charges an ability** | caster | benefit | instant; choice g1 option 2 — The name of the ability being Charged must be stated immediately after the incantation (N2). | E2, N1, N2 |

## Requirements

- **target-dead**: target must be dead *(E1)*
- **target-not-cursed**: target must not be Cursed *(L1)*

## Properties

- **has-choice**: the subject chooses between options — Caster may heal a wound or instantly Charge an ability. *(E2)*
- **caster-always-benefits**: the caster benefits regardless of their own Traits, States, Immunities, etc. — If successfully cast on a valid target, regardless of the caster's Traits, States, Immunities, Ongoing Effects or Enchantments. *(N1)*
- **must-declare**: the subject must make a declaration (give the words in note) — To Charge, the caster states the name of the ability immediately after the incantation. *(N2)*
- **bypass-traits**: works regardless of Traits — The caster's benefit is not blocked by their own Traits, States, Immunities, Ongoing Effects or Enchantments. *(N1)*
- **bypass-immunities**: works regardless of Immunities — The caster's benefit is not blocked by their own Traits, States, Immunities, Ongoing Effects or Enchantments. *(N1)*
- **bypass-enchantments**: ignores Enchantments — The caster's benefit is not blocked by their own Traits, States, Immunities, Ongoing Effects or Enchantments. *(N1)*

## Clarifications in the text

- The caster's benefit applies whenever the ability is successfully cast on a valid target, whatever the caster's own Traits, States, Immunities, Ongoing Effects or Enchantments. *(N1)*
- Charging via Steal Life Essence still requires naming the ability immediately after the incantation. *(N2)*

## Names in the text

- state **cursed**: mentions *(E1, L1)*
- mechanic **charge**: mentions *(E2, N2)*
- mechanic **incantation**: mentions *(N2)*
- mechanic **traits**: mentions *(N1)*
- mechanic **immune**: mentions *(N1)*
- mechanic **ongoing-effects**: mentions *(N1)*
- mechanic **enchantments**: mentions *(N1)*
- mechanic **declaration**: mentions *(N2)*

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

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| is given by | [Void Touched](void-touched.md) | only Steal Life Essence: Curses (dead-target, until respawn); only Steal Life Essence: Heals wounds (caster, amount one, instant); only Steal Life Essence: Instantly Charges an ability (caster, instant); only Void Touched: Armor Breaking (bearer melee weapons) (bearer, while worn); only Void Touched: Grants Shadow Step (bearer, while worn); only Void Touched: Grants Steal Life Essence (bearer, while worn); only Void Touched: Unaffected by (bearer, while worn); only Void Touched: Curses (bearer, while worn) |

## Open questions

- Beneficiary set to 'enemy' (cast on an enemy corpse, per convention 20) although the payoff is to the caster; E1 does not literally restrict the target to enemies.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Target dead player is Cursed. | effect e1 (Curses); requirement target-dead; names cursed |
| E2 | Caster may heal a wound or instantly Charge an ability. | effect e2 (Heals wounds); effect e3 (Instantly Charges an ability); property has-choice; names charge |
| L1 | Does not work on Cursed players. | requirement target-not-cursed; names cursed |
| N1 | Caster will always benefit if successfully cast on a valid target, regardless of the caster's Traits, States, Immunities, Ongoing Effects, or Enchantments. | effect e2 (Heals wounds); effect e3 (Instantly Charges an ability); property caster-always-benefits; property bypass-traits; property bypass-immunities; property bypass-enchantments; names traits; names immune; names ongoing-effects; names enchantments; clarification |
| N2 | In order to charge an ability, the name of the ability being charged must still be stated immediately after the incantation. | effect e3 (Instantly Charges an ability); property must-declare; names charge; names incantation; names declaration; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/steal-life-essence.json` and the V8.08 "Spongy" rules.*
