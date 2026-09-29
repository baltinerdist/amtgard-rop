---
title: "Juggernaut — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Juggernaut
type: Archetype
school: Neutral
targets_other_players: false
classes: []
---

# Juggernaut — Interoperability

[Rule text](../../rules/magic-and-abilities/juggernaut.md) · **Archetype** · Neutral School

## Summary

- **Archetype.** Chosen at 6th level (Warrior 6). Archetypes are outside this model, so it has no works/blocked results here.

## What it does

Warrior archetype: gains Harden Armor (Self) 1/Life and Phoenix Tears (Self) 3/Refresh (Swift); Harden becomes Greater Harden; loses Ancestral Armor and True Grit.

| Effect | On | Details |
| --- | --- | --- |
| Grants Harden Armor | bearer (benefit) | how gains; frequency (Self) 1/Life (ex); permanent; continuously while it is worn, chanted or in effect |
| Grants Phoenix Tears | bearer (benefit) | how gains; frequency (Self) 3/Refresh (ex); meta Swift; permanent; continuously while it is worn, chanted or in effect |
| Replaces an ability | bearer (benefit) | ability Harden; with Greater Harden; note Greater Harden (Self) (ex) at the same frequency as the replaced Harden; permanent; continuously while it is worn, chanted or in effect |
| Removes Ancestral Armor | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |
| Removes True Grit | bearer (harm) | permanent; continuously while it is worn, chanted or in effect |

**Capabilities:** grants-abilities, has-drawback · **Roles:** class-modifier, defense, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/juggernaut.md`](../../metadata/profiles/juggernaut.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. 

## Connected abilities

**Juggernaut names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Ancestral Armor](ancestral-armor.md) | removes | Warrior, Healer |
| [Greater Harden](greater-harden.md) | grants or gives | Healer |
| [Harden](harden.md) | replaces | Warrior, Healer |
| [Harden Armor](harden-armor.md) | grants or gives | Druid |
| [Phoenix Tears](phoenix-tears.md) | grants or gives | Healer |
| [True Grit](true-grit.md) | removes | Warrior |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
