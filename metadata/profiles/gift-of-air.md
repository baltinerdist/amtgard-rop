---
title: "Gift of Air"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Gift of Air

> Ignores a weapon or arrow hit on the bearer, who becomes Insubstantial in place or returning to base; bearer may not wield weapons or Shields.

| | |
| --- | --- |
| Type | Enchantment (enchantment) |
| School | Protection |
| Range | Other |
| Incantation | "I grant thee a gift of the air" x3 |
| Materials | White strip |
| Magical | yes, (m) for at least one class |
| Roles | defense, mobility, equipment · for: ally |
| Capabilities | has-drawback, makes-insubstantial, moves-self, protects, self-protection-state |
| Rule text | [rules/magic-and-abilities/gift-of-air.md](../../rules/magic-and-abilities/gift-of-air.md) · [interoperability](../../interoperability/abilities/gift-of-air.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Druid | 5th | 1 | 2 | 1/Refresh | 1 | refresh | - | (m) | Other | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Ignores a hit** | bearer | benefit | from weapons-and-arrows; except effects siege, armor-breaking, armor-destroying, shield-crushing, shield-destroying; instant; when a weapon, arrow or ball strikes the subject or their armor — The effects of any weapon or arrow that just struck the bearer are ignored. Melee weapons with Siege, Armor Breaking, Armor Destroying, Shield Crushing or Shield Destroying affect the bearer as normal and do not trigger it (E7). Worn armor is still affected as normal (E2). | E1, E2, E7 |
| e2 | **Makes Insubstantial** | bearer | benefit | until removed; when the bearer makes a stated choice; choice g1 option 1 — Option 1: Insubstantial in place; may exit at any time with the Insubstantial exit incantation. | E1, E3, E4 |
| e3 | **Makes Insubstantial** | bearer | benefit | until arrival; when the bearer makes a stated choice; choice g1 option 2 — Option 2: Insubstantial while returning to base; may not exit early (E5); must exit immediately on reaching base (E6). | E1, E3, E5, E6 |
| e4 | **Sends to base** | bearer | benefit | until arrival; when the bearer makes a stated choice; choice g1 option 2 — Option 2 (chosen by the bearer): must return to their base as a Forced Movement effect. | E3, E5 |
| e7 | **May not exit early** | bearer | harm | what exit-early; until arrival; when the bearer makes a stated choice; choice g1 option 2 — Option 2: may not exit Insubstantial early. Contradicted by N2 (may end at any time); see open questions. | E5 |
| e5 | **May not wield weapons** | bearer | harm | what wield-weapons; while worn; continuously while it is worn, chanted or in effect — Drawback: bearer may not wield weapons. | L1 |
| e6 | **May not wield shields** | bearer | harm | what wield-shields; while worn; continuously while it is worn, chanted or in effect — Drawback: bearer may not wield Shields. | L1 |

**Drawbacks:** May not exit early (bearer); May not wield weapons (bearer); May not wield shields (bearer)

## Restrictions

- **no-exit-early**: the subject may not end it early — Option 2 only (return to base). N2 says the bearer may end this Insubstantial State at any time; see open questions. *(E5)*

## How it ends early

- **exit-at-will**: the subject may end it at any time (states how) — Option 1 (E4); N2 says the bearer may end this Insubstantial State at any time with the Insubstantial exit incantation, which conflicts with E5 for option 2. *(E4, N2)*
- **on-arrival**: ends on reaching the destination — Option 2: must exit Insubstantial immediately on reaching base. *(E6)*
- **insubstantial-ends**: ends if the Insubstantial State from it ends — If the Insubstantial State is ended, the player no longer has to continue returning to base. *(N1)*

## Properties

- **must-declare**: the subject must make a declaration (give the words in note) — Declares "Gift of Air" when it activates. *(E1)*
- **has-choice**: the subject chooses between options — Immediately after activating, bearer chooses option 1 (in place) or option 2 (return to base). *(E3)*
- **forced-movement**: the text says it is a Forced Movement effect — The return to base in option 2 is a Forced Movement effect. *(E5)*

## Clarifications in the text

- Armor worn by the bearer is still affected by the hit as normal, in addition to triggering Gift of Air. *(E2)*
- Melee weapons with Siege, Armor Breaking, Armor Destroying, Shield Crushing or Shield Destroying affect the bearer normally and do not trigger Gift of Air. *(E7)*

## Names in the text

- state **insubstantial**: mentions *(E1, E4, E5, E6, N1, N2)*
- special-effect **siege**: mentions *(E7)*
- special-effect **armor-breaking**: mentions *(E7)*
- special-effect **armor-destroying**: mentions *(E7)*
- special-effect **shield-crushing**: mentions *(E7)*
- special-effect **shield-destroying**: mentions *(E7)*
- mechanic **base**: mentions *(E5, E6, N1)*
- mechanic **forced-movement**: mentions *(E5)*
- mechanic **incantation**: mentions *(E4, N2)*
- mechanic **declaration**: mentions *(E1)*
- mechanic **armor**: mentions *(E2)*
- mechanic **weapon**: mentions *(E1, E7, L1)*
- mechanic **shield**: mentions *(L1)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| does more than | [Shadow Step](shadow-step.md) | only Gift of Air: Ignores a hit (bearer, instant); only Gift of Air: Sends to base (bearer, until arrival); only Gift of Air: May not exit early (bearer, until arrival); only Gift of Air: May not wield weapons (bearer, while worn); only Gift of Air: May not wield shields (bearer, while worn); restriction only in Gift of Air: no-exit-early; ends when only in Gift of Air: insubstantial-ends, on-arrival; property only in Gift of Air: forced-movement, has-choice, must-declare |
| overlap | [Song of Survival](song-of-survival.md) | only Gift of Air: Ignores a hit (bearer, instant); only Gift of Air: May not wield weapons (bearer, while worn); only Gift of Air: May not wield shields (bearer, while worn); only Song of Survival: Prevents death (bearer, until used); only Song of Survival: Ignores a hit (bearer, instant); restriction only in Song of Survival: once-per-life; ends when only in Song of Survival: activates-once, chant-stops; property only in Song of Survival: chant |

## Open questions

- The text never says whether Gift of Air is removed (expended) after it activates; the negation is recorded as an instant effect but the Enchantment's end is unstated.
- Contradiction: E5 says option 2 may not exit early, but N2 says the bearer may end this Insubstantial State at any time. Both encoded (restriction no-exit-early for option 2, termination exit-at-will citing N2).
- E7 limits the exception to melee weapons; arrows or thrown weapons carrying those Special Effects appear to still trigger Gift of Air.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | The effects of any weapon or arrow which just struck the bearer are ignored, instead the bearer declares "Gift of Air" and becomes Insubstantial. | effect e1 (Ignores a hit); effect e2 (Makes Insubstantial); effect e3 (Makes Insubstantial); property must-declare; names insubstantial; names declaration; names weapon |
| E2 | If the bearer is wearing armor it is affected as normal in addition to triggering Gift of Air. | effect e1 (Ignores a hit); names armor; clarification |
| E3 | Immediately after Gift of Air activates, bearer must choose one of the following: | effect e2 (Makes Insubstantial); effect e3 (Makes Insubstantial); effect e4 (Sends to base); property has-choice |
| E4 | 1. Bearer becomes Insubstantial in place, but may exit Insubstantial at any time using the exit incantation for Insubstantial. | effect e2 (Makes Insubstantial); ends when exit-at-will; names insubstantial; names incantation |
| E5 | 2. Bearer becomes Insubstantial and must return to their base as a Forced Movement effect, but may not exit early. | effect e3 (Makes Insubstantial); effect e4 (Sends to base); effect e7 (May not exit early); restriction no-exit-early; property forced-movement; names insubstantial; names base; names forced-movement |
| E6 | They must exit Insubstantial immediately upon reaching their base | effect e3 (Makes Insubstantial); ends when on-arrival; names insubstantial; names base |
| E7 | Melee weapons with the Siege, Armor Breaking, Armor Destroying, Shield Crushing, or Shield Destroying Special Effects will affect the bearer as normal and do not trigger Gift of Air. | effect e1 (Ignores a hit); names siege; names armor-breaking; names armor-destroying; names shield-crushing; names shield-destroying; names weapon; clarification |
| L1 | Bearer may not wield weapons or Shields. | effect e5 (May not wield weapons); effect e6 (May not wield shields); names weapon; names shield |
| N1 | If the Insubstantial State is ended, the player is not required to continue returning to base. | ends when insubstantial-ends; names insubstantial; names base |
| N2 | Bearer may end this Insubstantial State at any time by using the exit incantation for Insubstantial. | ends when exit-at-will; names insubstantial; names incantation |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/gift-of-air.json` and the V8.08 "Spongy" rules.*
