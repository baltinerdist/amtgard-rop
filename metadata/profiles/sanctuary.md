---
title: "Sanctuary"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Sanctuary

> While chanting, caster and carried equipment are unaffected by hostile actions from within 20'; may not approach enemy bases, touch objectives or impede play.

| | |
| --- | --- |
| Type | Verbal (verbal) |
| School | Protection |
| Range | Self |
| Incantation | "Sanctuary" |
| Materials | none |
| Magical | no |
| Roles | defense, utility, equipment · for: self |
| Capabilities | castable-while-moving, has-drawback, moves-self, protects |
| Drawbacks from limits | the subject may not impede play |
| Rule text | [rules/magic-and-abilities/sanctuary.md](../../rules/magic-and-abilities/sanctuary.md) · [interoperability](../../interoperability/abilities/sanctuary.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monk | 3rd | - | - | 1/Life Charge x5 | 1 | life | x5 | (ex) | Self | Ambulant |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Unaffected by** | caster | benefit | by hostile-actions-within-20ft; while chanting; continuously while it is worn, chanted or in effect — Covers the caster; their carried equipment is encoded separately (e6). | E1 |
| e2 | **May not approach enemy base** | caster | harm | what approach-enemy-base; while chanting; continuously while it is worn, chanted or in effect — May not come within 20' of an unfriendly base; must immediately move to avoid it. | L1 |
| e3 | **May not interact with game** | caster | harm | what interact-with-game; while chanting; continuously while it is worn, chanted or in effect — May not interact with game items or game objectives. | L1 |
| e4 | **May not impede play** | caster | harm | what impede-play; while chanting; continuously while it is worn, chanted or in effect — May not impede the play of other people in any manner; must immediately move to avoid such situations. | L1 |
| e5 | **May not exit early** | caster | harm | what exit-early; while chanting; continuously while it is worn, chanted or in effect; only if the subject voluntarily carried or touched a weapon (other than blocking) — After voluntarily carrying or touching a weapon (other than blocking) during Sanctuary, the caster may only voluntarily end it at base and must keep chanting until there. | L2 |
| e6 | **Unaffected by** | bearer-equipment | benefit | by hostile-actions-within-20ft; while chanting; continuously while it is worn, chanted or in effect — The caster's carried equipment is also unaffected. | E1 |
| e7 | **Moves freely** | caster | benefit | while chanting; continuously while it is worn, chanted or in effect — The caster may move about while in Sanctuary, subject to the limits in L1. | E1, L1 |

**Drawbacks:** May not approach enemy base (caster); May not interact with game (caster); May not impede play (caster); May not exit early (caster)

## Restrictions

- **may-not-impede-play**: the subject may not impede play — May not impede the play of other people in any manner; must immediately move to avoid such situations. *(L1)*
- **no-exit-early**: the subject may not end it early — Only after voluntarily carrying or touching a weapon (other than blocking): may then only end Sanctuary at base, chanting until there. *(L2)*

## How it ends early

- **chant-stops**: ends if the Chant stops *(E2)*
- **exit-at-will**: the subject may end it at any time (states how) — Cease chanting and declare "No longer in sanctuary", audible to 20 feet. Only at base after touching a weapon (L2). *(E3, N1)*
- **exit-only-at-base**: may only be ended at base (in the circumstances given in a condition or note) — If the caster voluntarily carried or touched a weapon (other than blocking), they may only voluntarily end Sanctuary at base and must continue chanting until there. *(L2)*

## Properties

- **chant**: requires a Chant — Chant "sanctuary". *(E2)*
- **must-declare**: the subject must make a declaration (give the words in note) — "No longer in sanctuary", audible out to 20 feet. *(E3, N1)*

## Clarifications in the text

- The exit declaration must be audible out to 20 feet. *(N1)*

## Names in the text

- mechanic **chant**: mentions *(E2, E3, L2)*
- mechanic **declaration**: mentions *(E3, N1)*
- mechanic **base**: mentions *(L1, L2)*
- mechanic **game-objectives**: mentions *(L1)*
- mechanic **weapon**: mentions *(L2)*

## Open questions

- 'Hostile actions originating from within 20'' is undefined (abilities and attacks alike, presumably).

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Caster and their carried equipment are unaffected by hostile actions originating from within 20'. | effect e1 (Unaffected by); effect e6 (Unaffected by); effect e7 (Moves freely) |
| E2 | Must Chant "sanctuary". | ends when chant-stops; property chant; names chant |
| E3 | Caster may end Sanctuary at any time by ceasing to chant and declaring "No longer in sanctuary". | ends when exit-at-will; property must-declare; names chant; names declaration |
| L1 | Caster may not come within 20' of an unfriendly base, interact with game items nor game objectives, nor impede the play of other people in any manner, and must immediately move to avoid such situations. | effect e2 (May not approach enemy base); effect e3 (May not interact with game); effect e4 (May not impede play); effect e7 (Moves freely); restriction may-not-impede-play; names base; names game-objectives |
| L2 | If the caster voluntarily carries or touches a weapon in any fashion (other than blocking) at any point during Sanctuary, they may only voluntarily end Sanctuary at base and must continue chanting until there. | effect e5 (May not exit early); restriction no-exit-early; ends when exit-only-at-base; names chant; names base; names weapon |
| N1 | The exit declaration must be audible out to 20 feet. | ends when exit-at-will; property must-declare; names declaration; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/sanctuary.json` and the V8.08 "Spongy" rules.*
