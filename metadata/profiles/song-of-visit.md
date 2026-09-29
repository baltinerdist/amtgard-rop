---
title: "Song of Visit"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Song of Visit

> While chanting, the bearer is Stopped and Invulnerable; when the song ends they stay Invulnerable and must go directly to base.

| | |
| --- | --- |
| Type | Enchantment (enchantment) |
| School | Protection |
| Range | Self |
| Incantation | "I sing to entertain friend and foe" x3 |
| Materials | none |
| Magical | yes, (m) for at least one class |
| Roles | defense, utility · for: self |
| Capabilities | has-drawback, moves-self, self-protection-state |
| Drawbacks from limits | the subject may not impede play |
| Rule text | [rules/magic-and-abilities/song-of-visit.md](../../rules/magic-and-abilities/song-of-visit.md) · [interoperability](../../interoperability/abilities/song-of-visit.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bard | 2nd | 1 | 1 | Unlimited | - | unlimited | - | (m) | Self | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Stops** | bearer | harm | while chanting; continuously while it is worn, chanted or in effect — Drawback on the bearer. | E1 |
| e2 | **Makes Invulnerable** | bearer | benefit | while chanting; continuously while it is worn, chanted or in effect | E1 |
| e3 | **Makes Invulnerable** | bearer | benefit | until arrival; when the Enchantment is removed — Immediately when Song of Visit is removed; removed when the bearer arrives at base and declares "I return from my visit". | E4, E5 |
| e4 | **Sends to base** | bearer | harm | until arrival; when the Enchantment is removed — Drawback: when the song is removed the bearer must move directly to their base as a Forced Movement effect; ends on the arrival declaration. | E4, E5 |
| e5 | **May not impede play** | bearer | harm | what impede-play; while chanting; continuously while it is worn, chanted or in effect — Drawback: bearer may not impede play. | L1 |

**Drawbacks:** Stops (bearer); Sends to base (bearer); May not impede play (bearer)

## Restrictions

- **may-not-impede-play**: the subject may not impede play *(L1)*

## How it ends early

- **chant-stops**: ends if the Chant stops — Must follow all Chant rules; the song ends when the Chant stops, which starts the return to base (E4). *(E3)*
- **on-arrival**: ends on reaching the destination — On arrival at base the bearer declares "I return from my visit"; Invulnerable is removed and the Forced Movement ends. *(E5)*

## Properties

- **chant**: requires a Chant — Chant "Song of Visit" or sing a song regarding their general good nature and friendly disposition. *(E2, E3)*
- **forced-movement**: the text says it is a Forced Movement effect — The return to base after the song is removed. *(E4, E5)*
- **must-declare**: the subject must make a declaration (give the words in note) — "I return from my visit" on arrival at base. *(E5)*

## Clarifications in the text

- Singing in place of the normal Chant is still a Chant and must follow all Chant rules (stopping the Chant ends the song). *(E3)*

## Names in the text

- state **stopped**: mentions *(E1)*
- state **invulnerable**: mentions *(E1, E4, E5)*
- mechanic **chant**: mentions *(E2, E3)*
- mechanic **base**: mentions *(E4)*
- mechanic **forced-movement**: mentions *(E4, E5)*
- mechanic **declaration**: mentions *(E5)*

## Open questions

- E4 'when Song of Visit is removed' is read as any removal (Chant stopping, Dispel Magic or similar).
- L1 'Bearer may not impede play' is encoded for while the song is worn; the text does not say whether it also binds the Invulnerable return to base.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Bearer is Stopped and Invulnerable. | effect e1 (Stops); effect e2 (Makes Invulnerable); names stopped; names invulnerable |
| E2 | Bearer must Chant "Song of Visit" or sing a song regarding their general good nature and friendly disposition. | property chant; names chant |
| E3 | Singing in place of the normal Chant is still a Chant and must follow all Chant rules. | ends when chant-stops; property chant; names chant; clarification |
| E4 | Immediately when Song of Visit is removed, the bearer becomes Invulnerable and must move directly to their base as a Forced Movement effect. | effect e3 (Makes Invulnerable); effect e4 (Sends to base); property forced-movement; names invulnerable; names base; names forced-movement |
| E5 | Upon arrival, bearer must declare "I return from my visit," at which point the Invulnerable state is removed and the Forced Movement effect ends. | effect e3 (Makes Invulnerable); effect e4 (Sends to base); ends when on-arrival; property forced-movement; property must-declare; names invulnerable; names forced-movement; names declaration |
| L1 | Bearer may not impede play. | effect e5 (May not impede play); restriction may-not-impede-play |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/song-of-visit.json` and the V8.08 "Spongy" rules.*
