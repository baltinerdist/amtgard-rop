---
title: "Mass Healing"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Mass Healing

> Self Enchantment with five strips: caster may Heal (m) a player at Touch by declaring "I grant thee healing" and removing a strip.

| | |
| --- | --- |
| Type | Enchantment (enchantment) |
| School | Spirit |
| Range | Self |
| Incantation | "Let the powers of healing flow through me" x3 |
| Materials | Five yellow strips |
| Magical | yes, (m) for at least one class |
| Roles | healing · for: ally |
| Capabilities | castable-while-moving, grants-abilities · through granted abilities: heals |
| Gives its user | [Heal](heal.md) [casts-via-strips] |
| Rule text | [rules/magic-and-abilities/mass-healing.md](../../rules/magic-and-abilities/mass-healing.md) · [interoperability](../../interoperability/abilities/mass-healing.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Healer | 6th | 1 | 1 | 1/Refresh | 1 | refresh | - | (m) | Self | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Casts Heal from strips** | bearer | benefit | while worn; continuously while it is worn, chanted or in effect — Text says 'Caster'; range is Self so caster and bearer are the same player. Heal (m) a player at Touch by removing an enchantment strip. Five yellow strips. | E1 |
| e2 | **Casts by declaration** | bearer | benefit | what Heal (m) at Touch, by declaring "I grant thee healing"; while worn; continuously while it is worn, chanted or in effect — The declaration is not an incantation: not stopped by Suppressed, usable while moving, etc. | E1, N1 |
| e3 | **Uses up a strip** | bearer | neutral | n 1; instant; when the bearer spends one of the Enchantment's strips — One strip removed per Heal. | E1 |

## How it ends early

- **last-strip**: removed when the last strip is removed — Enchantment is removed when the last strip is removed. *(E2)*

## Properties

- **uses-strips**: tracked with enchantment strips — Five yellow strips. *(E1, E2)*
- **declaration-not-incantation**: uses a declaration that is not an incantation — "I grant thee healing" is a declaration, not an incantation. *(E1, N1)*
- **must-declare**: the subject must make a declaration (give the words in note) — "I grant thee healing". *(E1)*
- **works-while-suppressed**: usable while Suppressed or Stunned — The declaration is not stopped by being Suppressed. *(N1)*
- **castable-while-moving**: may be cast or used while moving — The declaration may be used while moving. *(N1)*
- **materials-required**: requires specific materials (strips, covers) — Five yellow strips; one removed per Heal. *(E1)*

## Clarifications in the text

- The declaration is not an incantation, so it is not stopped by being Suppressed and may be used while moving, etc. *(N1)*

## Names in the text

- ability **[Heal](heal.md)**: casts-via-strips *(E1)*
- state **suppressed**: mentions *(N1)*
- mechanic **declaration**: mentions *(E1, N1)*
- mechanic **incantation**: mentions *(N1)*
- mechanic **strips**: mentions *(E1, E2)*
- mechanic **enchantments**: mentions *(E2)*
- mechanic **range**: mentions *(E1)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does more than | [Battlefield Triage](battlefield-triage.md) | only Mass Healing: Casts by declaration (bearer, while worn); property only in Mass Healing: castable-while-moving, declaration-not-incantation, must-declare, works-while-suppressed; range: Self vs Touch |
| gives its user | [Heal](heal.md) | only Mass Healing: Casts Heal from strips (bearer, while worn); only Mass Healing: Casts by declaration (bearer, while worn); only Mass Healing: Uses up a strip (bearer, instant); only Heal: Heals wounds (target, amount one, instant); ends when only in Mass Healing: last-strip; property only in Mass Healing: castable-while-moving, declaration-not-incantation, materials-required, must-declare, uses-strips, works-while-suppressed; delivery: enchantment vs verbal; range: Self vs Touch |

## Open questions

- N1 ends with 'etc.': other incantation rules (e.g. the empty-hand requirement) presumably do not apply either, but the text does not list them.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Caster may Heal (m) a player at Touch by declaring "I grant thee healing" and removing an enchantment strip. | effect e1 (Casts Heal from strips); effect e2 (Casts by declaration); effect e3 (Uses up a strip); property uses-strips; property declaration-not-incantation; property must-declare; property materials-required; names Heal; names declaration; names strips; names range |
| E2 | Enchantment is removed when the last strip is removed. | ends when last-strip; property uses-strips; names strips; names enchantments |
| N1 | The declaration is not an incantation, and so is not stopped by being Suppressed, and may be used while moving, etc. | effect e2 (Casts by declaration); property declaration-not-incantation; property works-while-suppressed; property castable-while-moving; names suppressed; names declaration; names incantation; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/mass-healing.json` and the V8.08 "Spongy" rules.*
