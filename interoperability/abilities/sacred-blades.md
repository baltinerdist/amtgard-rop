---
title: "Sacred Blades — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Sacred Blades
type: Enchantment
school: Sorcery
targets_other_players: false
classes: []
---

# Sacred Blades — Interoperability

[Rule text](../../rules/magic-and-abilities/sacred-blades.md) · **Enchantment** · Sorcery School · Range Self

## Summary

- **Not on any class list.** It is only available through other abilities (Inquisitor); frontmatter availability: Paladin 6.

## What it does

Bearer's wielded weapons are Hardened, and their melee weapons (and Special Effects they deliver) ignore Magic Armor and wound-preventing Resistances.

| Effect | On | Details |
| --- | --- | --- |
| Works as Harden | bearer-equipment (benefit) | how as-per; while worn; continuously while it is worn, chanted or in effect |
| Weapons ignore protections | bearer (benefit) | against magic-armor; while worn; continuously while it is worn, chanted or in effect |
| Weapons ignore protections | bearer (benefit) | against wound-resistances; while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** defeats-armor, grants-abilities, protects · **Roles:** offense, equipment, defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/sacred-blades.md`](../../metadata/profiles/sacred-blades.md).

## Effect on each class

Not modelled: it is not on a class list, so the works/blocked results are not computed here. Its range is Self; see the abilities that grant it under Connected abilities.

## Connected abilities

**Sacred Blades names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Harden](harden.md) | borrows its effect | Warrior, Healer |

**These abilities name Sacred Blades in their text** (auto-detected). If Sacred Blades is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Inquisitor](inquisitor.md) | grants or gives | Paladin |

## If you change its level

Not on a class list, so its level is set by whatever grants it (see above).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
