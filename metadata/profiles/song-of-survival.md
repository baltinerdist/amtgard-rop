---
title: "Song of Survival"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Song of Survival

> While chanting, when the bearer would die they ignore it and become Insubstantial, in place or returning to base; once per life.

| | |
| --- | --- |
| Type | Enchantment (enchantment) |
| School | Protection |
| Range | Self |
| Incantation | "I sing of my numerous close calls" |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | defense, mobility · for: self |
| Capabilities | has-drawback, makes-insubstantial, moves-self, protects, self-protection-state, survives-death |
| Rule text | [rules/magic-and-abilities/song-of-survival.md](../../rules/magic-and-abilities/song-of-survival.md) · [interoperability](../../interoperability/abilities/song-of-survival.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bard | 5th | 1 | 1 | Unlimited | - | unlimited | - | (m) | Self | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Prevents death** | bearer | benefit | instead insubstantial; until used; when the subject would die — Activates once: the song then ends immediately and the bearer stops their Chant (E3); only while the song is worn. | E1, E2 |
| e2 | **Makes Insubstantial** | bearer | benefit | until removed; when the bearer makes a stated choice; choice g1 option 1 — Option 1: Insubstantial in place; may exit at any time with the Insubstantial exit incantation. | E1, E4, E5 |
| e3 | **Makes Insubstantial** | bearer | benefit | until arrival; when the bearer makes a stated choice; choice g1 option 2 — Option 2: may not exit early; must exit immediately on reaching base. | E1, E4, E6, E7 |
| e4 | **Sends to base** | bearer | benefit | until arrival; when the bearer makes a stated choice; choice g1 option 2 — Option 2 (chosen by the bearer): return to base as a Forced Movement effect. | E4, E6 |
| e5 | **Ignores a hit** | bearer | benefit | from lethal-event; instant; when the subject would die — The triggering event has no effect on the bearer other than triggering Song of Survival. | E2 |
| e6 | **May not exit early** | bearer | harm | what exit-early; until arrival; when the bearer makes a stated choice; choice g1 option 2 — Option 2: may not exit Insubstantial early (contradicted by N1; see open questions). | E6 |

**Drawbacks:** May not exit early (bearer)

## Restrictions

- **once-per-life**: may be used or activate only once per life — After it activates it may not be cast nor activated again on the same life. *(L1)*
- **no-exit-early**: the subject may not end it early — Option 2 only: may not exit Insubstantial before reaching base (N1 says the bearer may end it at any time; see open questions). *(E6)*

## How it ends early

- **activates-once**: ends after it activates once — Song of Survival immediately ends when it activates, and the bearer must stop their Chant. *(E3)*
- **chant-stops**: ends if the Chant stops — Must follow all Chant rules (stopping the Chant ends it). *(E9)*
- **exit-at-will**: the subject may end it at any time (states how) — Option 1 (E5): exit Insubstantial at any time with the Insubstantial exit incantation. N1 says the bearer may end it at any time with the standard incantation, which conflicts with E6 for option 2. *(E5, N1)*
- **on-arrival**: ends on reaching the destination — Option 2: must exit Insubstantial immediately on reaching base. *(E7)*
- **insubstantial-ends**: ends if the Insubstantial State from it ends — If the Insubstantial State ends by any means before reaching base, the rest of the effect ends. *(N2)*

## Properties

- **chant**: requires a Chant — Chant "Song of Survival" or sing a song about many escapes from certain doom. *(E8, E9)*
- **must-declare**: the subject must make a declaration (give the words in note) — Declares "Song of Survival" when it activates. *(E1)*
- **has-choice**: the subject chooses between options *(E4)*
- **forced-movement**: the text says it is a Forced Movement effect *(E6)*

## Clarifications in the text

- The triggering event is treated as having had no effect on the bearer other than triggering Song of Survival. *(E2)*
- Singing a song in place of the normal Chant still counts as a Chant and follows all Chant rules. *(E9)*

## Names in the text

- state **insubstantial**: mentions *(E1, E5, E6, E7, N1, N2)*
- mechanic **chant**: mentions *(E3, E8, E9)*
- mechanic **declaration**: mentions *(E1)*
- mechanic **forced-movement**: mentions *(E6)*
- mechanic **base**: mentions *(E6, E7, N2)*
- mechanic **incantation**: mentions *(E5, N1)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| overlap | [Gift of Air](gift-of-air.md) | only Song of Survival: Prevents death (bearer, until used); only Song of Survival: Ignores a hit (bearer, instant); only Gift of Air: Ignores a hit (bearer, instant); only Gift of Air: May not wield weapons (bearer, while worn); only Gift of Air: May not wield shields (bearer, while worn); restriction only in Song of Survival: once-per-life; ends when only in Song of Survival: activates-once, chant-stops; property only in Song of Survival: chant |

## Open questions

- N1 lets the bearer end the Insubstantial State at any time, but E6 says option 2 may not exit early.
- E2 says 'The caster' while the rest says 'bearer'; same person (Self range).

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | When the bearer would otherwise die, they instead declare "Song of Survival" and become Insubstantial. | effect e1 (Prevents death); effect e2 (Makes Insubstantial); effect e3 (Makes Insubstantial); property must-declare; names insubstantial; names declaration |
| E2 | The caster treats the triggering event as though it had no effect on them other than triggering Song of Survival. | effect e1 (Prevents death); effect e5 (Ignores a hit); clarification |
| E3 | Song of Survival immediately ends and bearer must stop their Chant. | ends when activates-once; names chant |
| E4 | Immediately after Song of Survival activates, bearer must choose one of the following: | effect e2 (Makes Insubstantial); effect e3 (Makes Insubstantial); effect e4 (Sends to base); property has-choice |
| E5 | 1. Bearer becomes Insubstantial in place, but may exit Insubstantial at any time using the exit incantation for Insubstantial. | effect e2 (Makes Insubstantial); ends when exit-at-will; names insubstantial; names incantation |
| E6 | 2. Bearer becomes Insubstantial and must return to their base as a Forced Movement effect, but may not exit early. | effect e3 (Makes Insubstantial); effect e4 (Sends to base); effect e6 (May not exit early); restriction no-exit-early; property forced-movement; names insubstantial; names forced-movement; names base |
| E7 | They must exit Insubstantial immediately upon reaching their base. | effect e3 (Makes Insubstantial); ends when on-arrival; names insubstantial; names base |
| E8 | Bearer must Chant "Song of Survival" or sing a song regarding their many escapes from certain doom. | property chant; names chant |
| E9 | Singing in place of the normal Chant is still a Chant and must follow all Chant rules. | ends when chant-stops; property chant; names chant; clarification |
| L1 | Once Song of Survival has activated to protect the bearer it may not be cast nor activated again on the same life. | restriction once-per-life |
| N1 | Bearer may end the Insubstantial State caused by Song of Survival at any time with the standard incantation. | ends when exit-at-will; names insubstantial; names incantation |
| N2 | If the Insubstantial State is ended by any means before reaching the base, the rest of the effect is ended as well. | ends when insubstantial-ends; names insubstantial; names base |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/song-of-survival.json` and the V8.08 "Spongy" rules.*
