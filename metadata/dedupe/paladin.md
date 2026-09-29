---
title: "Paladin: duplicate check"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Paladin: duplicate check

Every comparable entry on the Paladin list against every other ability, spell and trait in the rulebook.

## [Awe](../profiles/awe.md)

For 30 seconds a target within 20' may not attack or cast Magic at the caster or their equipment, and must stay 20' away.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Terror](../profiles/terror.md) | Anti-Paladin 5th, Bard 4th, Anti-Paladin 1st | Must keep away: feet 20, 30 s vs feet 50, 30 s; school: Command vs Death | “20'” vs “50'” |

## [Greater Heal](../profiles/greater-heal.md)

Heals all wounds on a touched player, even if they are Cursed.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Heal](../profiles/heal.md) | Monk 4th, Scout 2nd,5th, Druid 2nd, Healer 1st, Monk 1st, Scout 1st | Heals wounds: amount all, instant vs amount one, instant; property only in Greater Heal: bypass-cursed | “All wounds are healed” vs “Target player heals a wound”; “Ignores the Cursed State .” vs nothing |
| overlap | [Adrenaline](../profiles/adrenaline.md) | Barbarian 3rd | only Greater Heal: Heals wounds (target, amount all, instant); only Adrenaline: Heals wounds (caster, amount one, instant); requirement only in Adrenaline: immediately-after-kill; property only in Greater Heal: bypass-cursed; property only in Adrenaline: kill-trigger; range: Touch vs Self | “All wounds are healed” vs “Caster heals a wound”; “Ignores the Cursed State” vs “Kill Trigger” |

## [Greater Resurrect](../profiles/greater-resurrect.md)

Returns a willing dead player (within 5' of where they died) to life with wounds healed, regardless of States, removing Cursed; Enchantments kept.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Raise Dead](../profiles/raise-dead.md) | Healer 3rd | only Greater Resurrect: Ends Cursed (dead-target, instant); only Raise Dead: Removes Enchantments (dead-target, instant); only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); property only in Greater Resurrect: bypass-cursed, bypass-states; school: Spirit vs Death | nothing vs “and is Cursed . Target is also Suppressed for 30 seconds . Non-Persistent Enchantments on the player are removed before the player returns to life”; “Works regardless of any States on the target , and removes Cursed if present . Enchantments on the player are retained .” vs nothing |
| does more than | [Resurrect](../profiles/resurrect.md) | Monk 5th, Druid 5th, Healer 3rd | only Greater Resurrect: Ends Cursed (dead-target, instant); only Resurrect: Removes Enchantments (dead-target, instant); property only in Greater Resurrect: bypass-cursed, bypass-states | nothing vs “Non-Persistent Enchantments on the player are removed before the player returns to life .”; “Works regardless of any States on the target , and removes Cursed if present . Enchantments on the player are retained .” vs nothing |
| overlap | [True Grit](../profiles/true-grit.md) | Warrior 3rd | only Greater Resurrect: Returns to life (dead-target, instant); only Greater Resurrect: Heals wounds (dead-target, amount all, instant); only Greater Resurrect: Ends Cursed (dead-target, instant); only True Grit: Returns to life (caster, instant); only True Grit: Heals wounds (caster, amount all, instant); only True Grit: Freezes (caster, 30 s); requirement only in Greater Resurrect: target-dead, target-not-moved-5ft, target-willing; requirement only in True Grit: after-dying; property only in Greater Resurrect: bypass-cursed, bypass-states; range: Other vs Self | “Target willing dead player who has not moved more than 5' from where they died is returned” vs “Caster returns”; “. Any” vs “with their”; “on the player are” vs nothing; and 3 more |

## [Imbue](../profiles/imbue.md)

Bearer chooses shield or weapons: wielded equipment of that type cannot be destroyed or damaged and ignores Engulfing effects.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Guardian](../profiles/guardian.md) | Paladin 6th | only Imbue: Protects equipment (bearer-equipment, while worn); only Imbue: Ignores Engulfing effects (bearer-equipment, while worn); only Imbue: Ignores Engulfing effects (bearer-equipment, while worn); only Imbue: Protects equipment (bearer-equipment, while worn); only Guardian: Grants Imbue (bearer, permanent); only Guardian: Grants Martyr (bearer, permanent); only Guardian: Removes Protection from Evil (bearer, permanent); only Guardian: Removes Protection from Magic (bearer, permanent); only Guardian: Changes Imbue (bearer, permanent); restriction only in Imbue: only-one-option; restriction only in Guardian: one-active-per-caster; property only in Imbue: has-choice; delivery: enchantment vs archetype; school: Protection vs Neutral; range: Other vs - | “Bearer chooses either shield or weapons” vs “Gain Imbue (Touch) 1/Life (m) and Martyr (Other) 2/Life Charge x3 (ex)”; “Wielded equipment” vs “Lose all instances”; “the chosen type cannot be destroyed nor damaged” vs “Protection from Evil and Protection from Magic”; and 2 more |

## [Immune to Command](../profiles/immune-to-command.md)

Anti-Paladin, Barbarian and Paladin Trait: unaffected by Command School abilities; does not protect equipment or remove existing effects, and may still be targeted.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Song of Determination](../profiles/song-of-determination.md) | Bard 1st | Immune to Command: permanent vs while chanting; ends when only in Song of Determination: chant-stops; property only in Song of Determination: chant; delivery: trait vs enchantment; school: Command vs Protection; range: - vs Self | “The bearing player or object is unaffected by abilities from a given School . Immunity granted as a Trait does not prevent players from making use of their own class abilities . Unless otherwise noted , Immunities do not extend beyond the player or object that has them . Example : A player with Immunity to Flame can still have their armor destroyed by a Fireball . If a player” vs “Bearer”; “an effect which would remove” vs “Command . Bearer must Chant THIS or sing”; “State or Ongoing Effect , the State/Ongoing Effect is not removed” vs “song regarding their determination”; and 3 more |

## [Immune to Death](../profiles/immune-to-death.md)

Paladin Trait: unaffected by Death School abilities; does not protect equipment or remove existing effects, and may still be targeted.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Protection from Evil](../profiles/protection-from-evil.md) | Paladin 3rd | Immune to Death: permanent vs while worn; restriction only in Protection from Evil: one-active-per-caster; property only in Protection from Evil: active-while-dead, persistent; delivery: trait vs enchantment; school: Death vs Protection; range: - vs Other | “The bearing player or object is unaffected by abilities from a given School . Immunity granted as a Trait does not prevent players from making use of their own class abilities . Unless otherwise noted , Immunities do not extend beyond the player or object that has them . Example : A player with Immunity to Flame can still have their armor destroyed by a Fireball . If a player” vs “Bearer”; “an effect which would remove a State or Ongoing Effect ,” vs nothing; “State/Ongoing Effect is not removed . Example : A player who is Immune to Sorcery cannot be Released from Frozen , as they cannot be affected by Release , a Sorcery School ability . Players with Immunities may still be targeted by abilities of the given” vs “Death”; and 4 more |

## [Martyr](../profiles/martyr.md)

Takes a single State off a willing player by touch; the caster then suffers that State for 10 seconds. Not castable while Cursed.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Guardian](../profiles/guardian.md) | Paladin 6th | only Martyr: Removes States or Ongoing Effects (target, instant); only Martyr: Takes on a State (caster, 10 s); only Martyr: May not exit early (caster, 10 s); only Martyr: Makes Insubstantial (caster, 10 s); only Guardian: Grants Imbue (bearer, permanent); only Guardian: Grants Martyr (bearer, permanent); only Guardian: Removes Protection from Evil (bearer, permanent); only Guardian: Removes Protection from Magic (bearer, permanent); only Guardian: Changes Imbue (bearer, permanent); requirement only in Martyr: caster-not-cursed, target-willing; restriction only in Martyr: no-exit-early; restriction only in Guardian: one-active-per-caster; delivery: verbal vs archetype; school: Spirit vs Neutral; range: Other vs - | “A single State is removed” vs “Gain Imbue (Touch) 1/Life (m) and Martyr (Other) 2/Life Charge x3 (ex) . Lose all instances of Protection”; “target willing player” vs “Evil and Protection from Magic”; “The caster gains the removed State with” vs “May only have one instance of Imbue active at”; and 2 more |

## [Protection from Evil](../profiles/protection-from-evil.md)

Bearer is Immune to the Death School; Persistent and stays active while the bearer is dead; one active per caster.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Golem](../profiles/golem.md) | Druid 4th | only Golem: Curses (bearer, while worn); only Golem: Changes Mend (bearer, while worn); only Golem: Heals wounds (bearer, amount one, instant); only Golem: Acts as a respawn point (caster-of-enchantment, while worn, if caster-alive); only Golem: Acts as an Alternate Base (caster-of-enchantment, while worn); only Golem: Makes Enchantments Persistent (bearer, while worn); only Golem: May not use alternate bases (caster-of-enchantment, while worn); restriction only in Golem: bearer-not-alternate-base, caster-may-not-use-alternate-bases; school: Protection vs Sorcery | nothing vs “Death . Bearer is Cursed . Bearer can remove a wound via Mend . Bearer may use”; “Death School” vs “caster as an alternate respawn point while the caster is alive”; “This enchantment” vs “Bearer may treat the caster as an Alternate Base . All Enchantments worn by the Bearer , including THIS , are Persistent while THIS”; and 5 more |
| does less than | [Vampirism](../profiles/vampirism.md) | Wizard 4th | only Vampirism: Grants Adrenaline (bearer, while worn); only Vampirism: Curses (bearer, while worn); only Vampirism: Changes Adrenaline (bearer, while worn); restriction only in Protection from Evil: one-active-per-caster; property only in Protection from Evil: active-while-dead, persistent; property only in Vampirism: bypass-cursed; school: Protection vs Death | nothing vs “gains Adrenaline Unlimited (ex) ,”; “the” vs nothing; “School” vs “, and is Cursed”; and 2 more |
| overlap | [Immune to Death](../profiles/immune-to-death.md) | Paladin 1st | Immune to Death: while worn vs permanent; restriction only in Protection from Evil: one-active-per-caster; property only in Protection from Evil: active-while-dead, persistent; delivery: enchantment vs trait; school: Protection vs Death; range: Other vs - | “Bearer” vs “The bearing player or object is unaffected by abilities from a given School . Immunity granted as a Trait does not prevent players from making use of their own class abilities . Unless otherwise noted , Immunities do not extend beyond the player or object that has them . Example : A player with Immunity to Flame can still have their armor destroyed by a Fireball . If a player”; nothing vs “an effect which would remove a State or Ongoing Effect ,”; “Death” vs “State/Ongoing Effect is not removed . Example : A player who is Immune to Sorcery cannot be Released from Frozen , as they cannot be affected by Release , a Sorcery School ability . Players with Immunities may still be targeted by abilities of the given”; and 4 more |

## [Protection from Magic](../profiles/protection-from-magic.md)

Bearer is unaffected by Magical abilities of every School; when the bearer dies they are Cursed.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Assassinate](../profiles/assassinate.md) | Assassin 1st | only Protection from Magic: Unaffected by (bearer, while worn); only Protection from Magic: Curses (bearer, until respawn); only Assassinate: Curses (dead-target, until respawn); requirement only in Assassinate: immediately-after-kill, target-dead; property only in Assassinate: no-verbal-targeting; delivery: enchantment vs verbal; school: Protection vs Death; range: Other, Touch vs 50' | “Bearer is unaffected by Magical abilities from any school . Upon death the bearer” vs “The target”; “This effect” vs “May only be used immediately upon killing an enemy . THIS targets the killed enemy and”; “interact with other Enchantments worn by the bearer” vs “require verbal targeting” |

## [Sacred Blades](../profiles/sacred-blades.md)

Bearer's wielded weapons are Hardened, and their melee weapons (and Special Effects they deliver) ignore Magic Armor and wound-preventing Resistances.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Harden](../profiles/harden.md) | Warrior 1st, Healer 1st | only Sacred Blades: Works as Harden (bearer-equipment, while worn); only Sacred Blades: Weapons ignore protections (bearer, while worn); only Sacred Blades: Weapons ignore protections (bearer, while worn); only Harden: Protects equipment (bearer-equipment, while worn); restriction only in Harden: only-one-option; property only in Sacred Blades: bypass-magic-armor, bypass-resistances; property only in Harden: has-choice; school: Sorcery vs Protection; range: Self vs Other, Self | “are affected as per Harden” vs “or shield may only be destroyed or damaged by Magic Balls/Verbals which destroy objects e”; “Bearer's wielded melee” vs “g . Fireball or Pyrotechnics . Will only affect either the”; “and any special effects delivered by them ignore magic armor and resistances that prevent wounds” vs “or the shield of the bearer , not both” |
| is given by | [Inquisitor](../profiles/inquisitor.md) | Paladin 6th | only Sacred Blades: Works as Harden (bearer-equipment, while worn); only Sacred Blades: Weapons ignore protections (bearer, while worn); only Sacred Blades: Weapons ignore protections (bearer, while worn); only Inquisitor: Grants Sacred Blades (bearer, permanent); only Inquisitor: Removes Greater Resurrect (bearer, permanent); property only in Sacred Blades: bypass-magic-armor, bypass-resistances; delivery: enchantment vs archetype; school: Sorcery vs Neutral; range: Self vs - | “Bearer's wielded weapons are affected as per Harden” vs “Gain Sacred Blades (Self) 1/Life (ex) Lose all instances of Greater Resurrect”; “Bearer's wielded melee weapons and any special effects delivered by them ignore magic armor and resistances that prevent wounds .” vs nothing |
