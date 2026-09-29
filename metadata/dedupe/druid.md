---
title: "Druid: duplicate check"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Druid: duplicate check

Every comparable entry on the Druid list against every other ability, spell and trait in the rulebook.

## [Attuned](../profiles/attuned.md)

Lets another player wear one additional Enchantment; Attuned itself does not count towards their Enchantment limit.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Essence Graft](../profiles/essence-graft.md) | Druid 5th | only Attuned: Allows extra Enchantments (bearer, count 1, while worn); only Essence Graft: Allows extra Enchantments (bearer, count 3, while worn); only Essence Graft: May not wear others magical enchantments (bearer, while worn); restriction only in Essence Graft: magical-enchantments-only-from-caster | “May” vs “Bearer may”; “an” vs “up to three”; “Enchantment” vs “Enchantments”; and 1 more |
| overlap | [Evolution](../profiles/evolution.md) | Scout 1st, Scout 4th | Allows extra Enchantments: count 1, while worn vs count 1, permanent; only Attuned: Removes Enchantments (bearer, instant); restriction only in Attuned: not-with-itself-or-similar; property only in Attuned: has-choice; range: Other vs Self | “may not be used” vs “does work”; “itself” vs “Attuned , Essence Graft ,”; “any” vs “Phoenix Tears so long as the”; and 2 more |

## [Barkskin](../profiles/barkskin.md)

Bearer gains one point of Magic Armor.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Gift of Earth](../profiles/gift-of-earth.md) | Druid 2nd | only Gift of Earth: Works as Harden (bearer, while worn) | nothing vs “and is affected as per Harden” |
| does less than | [Gift of Water](../profiles/gift-of-water.md) | Druid 4th | only Gift of Water: Grants Heal (bearer, while worn); school: Protection vs Sorcery | nothing vs “and Heal (Self) Unlimited (m)” |
| does less than | [Ironskin](../profiles/ironskin.md) | Druid 5th | Grants Magic Armor: points 1, while worn vs points 2, while worn; only Ironskin: Immune to Flame (bearer, while worn); only Ironskin: Works as Ancestral Armor (bearer, while worn) | nothing vs “is Immune to Flame and”; “one point of” vs “two points”; nothing vs “affected as per Ancestral Armor” |
| does less than | [Lycanthropy](../profiles/lycanthropy.md) | Druid 4th | Grants Magic Armor: points 1, while worn vs points 2, while worn; only Lycanthropy: Shield Crushing (bearer melee weapons) (bearer, while worn); only Lycanthropy: Immune to Command (bearer, while worn); school: Protection vs Death | “one point” vs “two points”; “Magic Armor” vs “magic armor”; nothing vs “Bearer's wielded melee weapons are Shield Crushing . Bearer is Immune to Command .” |
| does less than | [Stoneskin](../profiles/stoneskin.md) | Druid 3rd | Grants Magic Armor: points 1, while worn vs points 2, while worn; only Stoneskin: Works as Ancestral Armor (bearer, while worn) | “one point” vs “2 points”; nothing vs “affected as per Ancestral Armor” |

## [Bear Strength](../profiles/bear-strength.md)

Bearer's wielded melee weapons are Shield Crushing.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Flame Blade](../profiles/flame-blade.md) | Anti-Paladin 6th, Druid 4th | only Flame Blade: Armor Breaking (bearer melee weapons) (bearer, while worn); only Flame Blade: Immune to Flame (bearer, while worn); only Flame Blade: Immune to Flame (bearer-equipment, while worn); school: Sorcery vs Flame; range: Other vs Other, Self | nothing vs “Armor Breaking and”; nothing vs “Bearer and their wielded weapons are Immune to Flame .” |
| does less than | [Lycanthropy](../profiles/lycanthropy.md) | Druid 4th | only Lycanthropy: Grants Magic Armor (bearer, points 2, while worn); only Lycanthropy: Immune to Command (bearer, while worn); school: Sorcery vs Death | nothing vs “Bearer gains two points of magic armor .”; nothing vs “Bearer is Immune to Command .” |
| is given by | [Raider](../profiles/raider.md) | Barbarian 6th | only Bear Strength: Shield Crushing (bearer melee weapons) (bearer, while worn); only Raider: Grants Bear Strength (bearer, permanent); only Raider: Changes Look The Part (bearer, permanent); only Raider: Changes Brutal Strike (bearer, permanent); only Raider: Changes how often abilities can be used (bearer, permanent); only Raider: Removes Rage (bearer, permanent); delivery: enchantment vs archetype; school: Sorcery vs Neutral; range: Other vs - | “Bearer's wielded melee weapons are Shield Crushing” vs “Gain Bear Strength (Self) 1/Life (ex)”; nothing vs “Look the Part becomes an additional use of Brutal Strike . Lose all instances of Rage .” |

## [Call Lightning](../profiles/call-lightning.md)

Kills a target within 20'.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects | [Coup de Grace](../profiles/coup-de-grace.md) | Assassin 6th | requirement only in Coup de Grace: target-wounded; school: Flame vs Death | nothing vs “Target must be wounded when the caster begins the Incantation . Even if the target has no wounds at the end of the Incantation they will still die .” |
| same-effects | [Dimensional Rift](../profiles/dimensional-rift.md) | Wizard 4th | requirement only in Dimensional Rift: target-insubstantial; school: Flame vs Sorcery | nothing vs “Insubstantial” |
| same-effects | [Dragged Below](../profiles/dragged-below.md) | Wizard 3rd | requirement only in Dragged Below: target-stopped; school: Flame vs Death | nothing vs “Stopped” |
| identical | [Finger of Death](../profiles/finger-of-death.md) | Wizard 6th | school: Flame vs Death | same |
| does less than | [Fireball](../profiles/fireball.md) | Wizard 4th, Anti-Paladin 6th | only Fireball: Weapon Destroying (this magic ball) (struck-player, instant); only Fireball: Armor Destroying (this magic ball) (struck-player, instant); only Fireball: Shield Destroying (this magic ball) (struck-player, instant); delivery: verbal vs magic-ball; range: 20' vs - | “Target player” vs “This Magic Ball is Weapon Destroying , Armor Destroying , and Shield Destroying . Player hit” |
| same-effects | [Shatter](../profiles/shatter.md) | Wizard 4th | requirement only in Shatter: target-frozen; school: Flame vs Sorcery | nothing vs “Frozen” |
| does less than | [Sphere of Annihilation](../profiles/sphere-of-annihilation.md) | Wizard 6th | only Sphere of Annihilation: Weapon Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Shield Destroying (this magic ball) (struck-player, instant); only Sphere of Annihilation: Curses (struck-player, until respawn); property only in Sphere of Annihilation: bypass-armor, bypass-enchantments; delivery: verbal vs magic-ball; school: Flame vs Sorcery; range: 20' vs - | “Target” vs “This Magic Ball is Weapon Destroying , Shield Destroying , and ignores armor and Enchantments . Player hit dies and is Cursed . Because THIS ignores Enchantments , a”; “dies” vs “enchanted with Phoenix Tears would remain dead after being killed , and an Imbued Shield would still be destroyed” |

## [Corrosive Mist](../profiles/corrosive-mist.md)

Three strips: bearer may cast Destroy Armor (m) by removing a strip; the Enchantment ends when the last strip is removed.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Destroy Armor](../profiles/destroy-armor.md) | Wizard 4th | only Corrosive Mist: Casts Destroy Armor from strips (bearer, while worn); only Corrosive Mist: Uses up a strip (bearer, instant); only Destroy Armor: Destroys armor (hit-location, instant); ends when only in Corrosive Mist: last-strip; property only in Corrosive Mist: materials-required, uses-strips; property only in Destroy Armor: personal-protections-do-not-cover-equipment, targets-player-affects-equipment; delivery: enchantment vs verbal; range: Touch vs 20' | “Bearer may cast Destroy Armor (m) by incanting Player” vs “Remove all armor points from target hit location . THIS targets”; “mists” vs “player but affects the hit location . Visibility can be drawn to any part”; “corrosion destroy thine” vs “the player , not just the desired hit location . Immunities , resistances , and other protections will only protect the”; and 3 more |

## [Dispel Magic](../profiles/dispel-magic.md)

Removes all Enchantments from a target within 20', regardless of Traits, States, Immunities or Enchantments, except Sleight of Mind; not on Invulnerable players.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Naturalize Magic](../profiles/naturalize-magic.md) | Druid 6th | only Dispel Magic: Removes Enchantments (target, instant); only Naturalize Magic: Casts Dispel Magic from strips (bearer, while worn); only Naturalize Magic: Uses up a strip (bearer, instant); requirement only in Dispel Magic: target-not-invulnerable; ends when only in Naturalize Magic: last-strip; property only in Dispel Magic: bypass-enchantments, bypass-immunities, bypass-ongoing-effects, bypass-states, bypass-traits; property only in Naturalize Magic: materials-required, uses-strips; delivery: verbal vs enchantment; range: 20' vs Self | “All Enchantments on target are” vs “Bearer may cast Dispel Magic (m) by incanting Player thou art dispelled and removing an enchantment strip . Enchantment is removed when the last strip is”; “Will always remove Enchantments if successfully cast on a valid target , regardless of the player's Traits , States , Immunities , Ongoing Effects , or Enchantments (except Sleight of Mind) . Does not affect Invulnerable players .” vs nothing |
| overlap | [Sever Spirit](../profiles/sever-spirit.md) | Healer 2nd, Monk 6th | only Sever Spirit: Curses (dead-target, until respawn); requirement only in Dispel Magic: target-not-invulnerable; requirement only in Sever Spirit: target-dead, target-dead-at-start; school: Sorcery vs Spirit | “All” vs “Target dead player is Cursed . Any”; “target” vs “the player”; “Enchantments” vs “enchantments”; and 2 more |

## [Entangle](../profiles/entangle.md)

Engulfing Magic Ball: the player struck is Stopped for 60 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Hold Person](../profiles/hold-person.md) | Assassin 4th, Scout 4th, Healer 2nd, Wizard 3rd | Stops: 60 s vs 30 s; property only in Entangle: engulfing; delivery: magic-ball vs verbal; school: Subdual vs Command; range: - vs 20' | “Player struck is” vs “Target player becomes”; “60” vs “30”; “Engulfing .” vs nothing |
| does less than | [Lightning Bolt](../profiles/lightning-bolt.md) | Wizard 3rd | only Lightning Bolt: Weapon Destroying (this magic ball) (struck-player, instant); only Lightning Bolt: Armor Breaking (this magic ball) (struck-player, instant); only Lightning Bolt: Inflicts a wound (struck-player, instant); school: Subdual vs Flame | nothing vs “This Magic Ball is Weapon Destroying and Armor Breaking . Player hit receives a wound to that hit location .” |
| same-effects-different-numbers | [Pinning Arrow](../profiles/pinning-arrow.md) | Archer 1st,3rd,5th, Scout 4th, Scout 5th | Stops: 60 s vs 30 s; delivery: magic-ball vs specialty-arrow; school: Subdual vs Sorcery | “Player” vs “A player”; nothing vs “by this arrow”; “60” vs “30” |
| overlap | [Song of Power](../profiles/song-of-power.md) | Bard 4th | only Entangle: Stops (struck-player, 60 s); only Song of Power: Speeds up Charging (friendly-players, while chanting); only Song of Power: Stops (bearer, while chanting); restriction only in Song of Power: players-benefit-once; ends when only in Song of Power: chant-stops, moves-from-start; property only in Entangle: engulfing; property only in Song of Power: chant; delivery: magic-ball vs enchantment; school: Subdual vs Protection; range: - vs Self | “Player struck” vs “Friendly players within 20' of the bearer have their Charge Incantation repetitions divided by 2 , rounded down , to a minimum of 1 . Bearer”; “for 60 seconds” vs nothing; “Engulfing” vs “Bearer must Chant THIS or sing an inspiring song”; and 1 more |

## [Essence Graft](../profiles/essence-graft.md)

Lets another player wear up to three additional Enchantments, but all their Magical Enchantments must come from the caster of Essence Graft.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Attuned](../profiles/attuned.md) | Druid 3rd | only Essence Graft: Allows extra Enchantments (bearer, count 3, while worn); only Essence Graft: May not wear others magical enchantments (bearer, while worn); only Attuned: Allows extra Enchantments (bearer, count 1, while worn); restriction only in Essence Graft: magical-enchantments-only-from-caster | “Bearer may” vs “May”; “up to three” vs “an”; “Enchantments” vs “Enchantment”; and 1 more |

## [Extension](../profiles/extension.md)

Meta-Magic: the next 20' Verbal has its range extended to 50'.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Amplification](../profiles/amplification.md) | Bard 4th | only Extension: Modifies the next ability cast (caster, until used); only Amplification: Grants Extension (bearer, while worn); only Amplification: May not use other sources of ability (bearer, while worn); requirement only in Extension: only-verbals-20ft; restriction only in Amplification: excludes-other-sources; delivery: meta-magic vs enchantment; school: Neutral vs Sorcery; range: - vs Touch | “Verbal becomes 50'” vs “Bearer gains Extension 1/Refresh Charge x3 (m)”; “Only works on Verbals with a range” vs “Other sources”; “20'” vs “Extension may not be utilized while THIS is worn”; and 1 more |

## [Flame Blade](../profiles/flame-blade.md)

Bearer's wielded melee weapons are Armor Breaking and Shield Crushing; bearer and their wielded weapons are Immune to Flame.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Bear Strength](../profiles/bear-strength.md) | Druid 3rd, Barbarian 6th | only Flame Blade: Armor Breaking (bearer melee weapons) (bearer, while worn); only Flame Blade: Immune to Flame (bearer, while worn); only Flame Blade: Immune to Flame (bearer-equipment, while worn); school: Flame vs Sorcery; range: Other, Self vs Other | “Armor Breaking and” vs nothing; “Bearer and their wielded weapons are Immune to Flame .” vs nothing |
| does more than | [Berserk](../profiles/berserk.md) | Barbarian 1st | only Flame Blade: Shield Crushing (bearer melee weapons) (bearer, while worn); only Flame Blade: Immune to Flame (bearer, while worn); only Flame Blade: Immune to Flame (bearer-equipment, while worn); school: Flame vs Sorcery; range: Other, Self vs Self | “and Shield Crushing” vs nothing; “Bearer and their wielded weapons are Immune to Flame .” vs nothing |
| overlap | [Rage](../profiles/rage.md) | Barbarian 2nd,4th, Barbarian 1st | Armor Breaking (bearer melee weapons): while worn vs 7 s; Shield Crushing (bearer melee weapons): while worn vs 7 s; only Flame Blade: Immune to Flame (bearer, while worn); only Flame Blade: Immune to Flame (bearer-equipment, while worn); only Rage: Unaffected by (caster, 7 s); ends when only in Rage: begins-incantation, fails-to-count; property only in Rage: count-aloud; delivery: enchantment vs verbal; school: Flame vs Sorcery; range: Other, Self vs Self | “Bearer's” vs “Caster is unaffected by Verbal abilities and their”; nothing vs “Shield Crushing and”; “and Shield Crushing” vs “for seven seconds”; and 3 more |

## [Force Bolt](../profiles/force-bolt.md)

Magic Ball: wounds the hit location; Weapon Destroying and Armor Breaking.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Lightning Bolt](../profiles/lightning-bolt.md) | Wizard 3rd | only Lightning Bolt: Stops (struck-player, 60 s); property only in Lightning Bolt: engulfing; school: Sorcery vs Flame | nothing vs “Player struck is Stopped for 60 seconds . Engulfing .” |
| does less than | [Phase Bolt](../profiles/phase-bolt.md) | Wizard 5th | only Phase Bolt: Phasing (this magic ball) (struck-player, instant) | nothing vs “Phasing ,”; nothing vs “,” |
| is given by | [Mystic](../profiles/mystic.md) | Monk 6th | only Force Bolt: Weapon Destroying (this magic ball) (struck-player, instant); only Force Bolt: Armor Breaking (this magic ball) (struck-player, instant); only Force Bolt: Inflicts a wound (struck-player, instant); only Mystic: Grants Force Bolt (bearer, permanent); only Mystic: Grants Phase Bolt (bearer, permanent); only Mystic: Grants Suppression Bolt (bearer, permanent); only Mystic: May not wield heavy thrown (bearer, permanent); only Mystic: Removes Resurrect (bearer, permanent); delivery: magic-ball vs archetype; school: Sorcery vs Neutral | “This Magic” vs “Gain Force Bolt 3 Balls / Unlimited (m) , Phase Bolt 1”; “is Weapon Destroying” vs “/ Unlimited (m) ,”; “Armor Breaking” vs “Suppression Bolt 2 Balls / Unlimited (m)”; and 2 more |

## [Gift of Air](../profiles/gift-of-air.md)

Ignores a weapon or arrow hit on the bearer, who becomes Insubstantial in place or returning to base; bearer may not wield weapons or Shields.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Shadow Step](../profiles/shadow-step.md) | Assassin 1st, Scout 3rd | only Gift of Air: Ignores a hit (bearer, instant); only Gift of Air: Sends to base (bearer, until arrival); only Gift of Air: May not exit early (bearer, until arrival); only Gift of Air: May not wield weapons (bearer, while worn); only Gift of Air: May not wield shields (bearer, while worn); restriction only in Gift of Air: no-exit-early; ends when only in Gift of Air: insubstantial-ends, on-arrival; property only in Gift of Air: forced-movement, has-choice, must-declare; property only in Shadow Step: castable-while-moving; delivery: enchantment vs verbal; school: Protection vs Sorcery; range: Other vs Self | “The effects of any weapon or arrow which just struck the bearer are ignored , instead the bearer declares THIS and” vs “Caster”; “If the bearer is wearing armor it is affected as normal in addition to triggering” vs nothing; nothing vs “may be cast while moving”; and 1 more |
| overlap | [Song of Survival](../profiles/song-of-survival.md) | Bard 5th | only Gift of Air: Ignores a hit (bearer, instant); only Gift of Air: May not wield weapons (bearer, while worn); only Gift of Air: May not wield shields (bearer, while worn); only Song of Survival: Prevents death (bearer, until used); only Song of Survival: Ignores a hit (bearer, instant); restriction only in Song of Survival: once-per-life; ends when only in Song of Survival: activates-once, chant-stops; property only in Song of Survival: chant; range: Other vs Self | “The effects of any weapon or arrow which just struck” vs “When”; “are ignored” vs “would otherwise die”; nothing vs “they”; and 15 more |

## [Gift of Earth](../profiles/gift-of-earth.md)

Bearer gains 1 point of Magic Armor, and their wielded weapons or shield are protected as per Harden.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Barkskin](../profiles/barkskin.md) | Druid 1st | only Gift of Earth: Works as Harden (bearer, while worn) | “and is affected as per Harden” vs nothing |
| does more than | [Harden](../profiles/harden.md) | Warrior 1st, Healer 1st | only Gift of Earth: Grants Magic Armor (bearer, points 1, while worn); only Gift of Earth: Works as Harden (bearer, while worn); only Harden: Protects equipment (bearer-equipment, while worn); restriction only in Harden: only-one-option; property only in Harden: has-choice; range: Other vs Other, Self | “Bearer gains one point” vs “Bearer's wielded weapons or shield may only be destroyed or damaged by Magic Balls/Verbals which destroy objects e . g . Fireball or Pyrotechnics . Will only affect either the weapons or the shield”; “Magic Armor and is affected as per Harden” vs “the bearer , not both” |
| overlap | [Greater Harden](../profiles/greater-harden.md) | Healer 3rd, Warrior 6th | only Gift of Earth: Grants Magic Armor (bearer, points 1, while worn); only Greater Harden: Protects equipment (bearer-equipment, while worn) | “Bearer gains one point of Magic Armor” vs “Shields”; “is” vs “weapons wielded by the bearer are” |

## [Gift of Fire](../profiles/gift-of-fire.md)

Bearer gains Heat Weapon 1/Refresh Charge x3 (m) and is Immune to Flame.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Heat Weapon](../profiles/heat-weapon.md) | Druid 1st, Wizard 1st | only Gift of Fire: Grants Heat Weapon (bearer, while worn); only Gift of Fire: Immune to Flame (bearer, while worn); only Heat Weapon: Disables equipment (target-equipment, 30 s); requirement only in Heat Weapon: target-is-equipment; property only in Heat Weapon: targets-equipment; delivery: enchantment vs verbal; range: Other vs 20' | “Bearer gains Heat Weapon 1/Refresh Charge x3 (m) and is” vs “Target weapon may not be wielded for 30 seconds . Players who are”; nothing vs “may continue to wield the weapon”; nothing vs “The equipment , not the person , is the target of THIS . The equipment is the only thing required to be within range and visible for this ability to affect it .” |
| overlap | [Immune to Flame](../profiles/immune-to-flame.md) | Anti-Paladin 1st | Immune to Flame: while worn vs permanent; only Gift of Fire: Grants Heat Weapon (bearer, while worn); delivery: enchantment vs trait; range: Other vs - | “Bearer gains Heat Weapon 1/Refresh Charge x3 (m) and” vs “The bearing player or object is unaffected by abilities from a given School . Immunity granted as a Trait does not prevent players from making use of their own class abilities . Unless otherwise noted , Immunities do not extend beyond the player or object that has them . Example : A player with Immunity to Flame can still have their armor destroyed by a Fireball . If a player”; nothing vs “an effect which would remove a State or Ongoing Effect , the State/Ongoing Effect is not removed . Example : A player who is Immune to Sorcery cannot be Released from Frozen , as they cannot be affected by Release , a Sorcery School ability . Players with Immunities may still be targeted by abilities of the given School . Example : A player with Immunity to”; nothing vs “can still be the target of Pyrotechnics which would still destroy their equipment (as Immunities do not extend to equipment unless noted)”; and 1 more |

## [Gift of Water](../profiles/gift-of-water.md)

Bearer gains 1 point of Magic Armor and Heal (Self) Unlimited (m).

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Barkskin](../profiles/barkskin.md) | Druid 1st | only Gift of Water: Grants Heal (bearer, while worn); school: Sorcery vs Protection | “and Heal (Self) Unlimited (m)” vs nothing |
| does more than | [Regeneration](../profiles/regeneration.md) | Druid 3rd | only Gift of Water: Grants Magic Armor (bearer, points 1, while worn); only Gift of Water: Grants Heal (bearer, while worn); only Regeneration: Grants Heal (bearer, while worn); only Regeneration: Changes Heal (bearer, while worn); property only in Regeneration: must-declare; school: Sorcery vs Spirit | “one point of Magic Armor and” vs nothing; nothing vs “(Swift)”; nothing vs “The Heal granted by THIS may not be used within 10' of a living enemy . Bearer must state Swift normally .” |
| gives its user | [Heal](../profiles/heal.md) | Monk 4th, Scout 2nd,5th, Druid 2nd, Healer 1st, Monk 1st, Scout 1st | only Gift of Water: Grants Magic Armor (bearer, points 1, while worn); only Gift of Water: Grants Heal (bearer, while worn); only Heal: Heals wounds (target, amount one, instant); delivery: enchantment vs verbal; school: Sorcery vs Spirit; range: Other vs Touch | “Bearer gains one point of Magic Armor and Heal (Self) Unlimited (m)” vs “Target player heals a wound” |

## [Golem](../profiles/golem.md)

Bearer is Immune to Death and Cursed, Mend removes their wounds, their Enchantments are Persistent, and they may respawn at or base on the caster.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Adrenaline](../profiles/adrenaline.md) | Barbarian 3rd | only Golem: Immune to Death (bearer, while worn); only Golem: Curses (bearer, while worn); only Golem: Changes Mend (bearer, while worn); only Golem: Acts as a respawn point (caster-of-enchantment, while worn, if caster-alive); only Golem: Acts as an Alternate Base (caster-of-enchantment, while worn); only Golem: Makes Enchantments Persistent (bearer, while worn); only Golem: May not use alternate bases (caster-of-enchantment, while worn); requirement only in Adrenaline: immediately-after-kill; restriction only in Golem: bearer-not-alternate-base, caster-may-not-use-alternate-bases, one-active-per-caster; property only in Golem: active-while-dead, persistent; property only in Adrenaline: kill-trigger; delivery: enchantment vs verbal; school: Sorcery vs Spirit; range: Other vs Self | “Bearer is Immune to Death . Bearer is Cursed . Bearer can remove a wound via Mend . Bearer may use the caster as an alternate respawn point while the caster is alive . Bearer may treat the caster as an Alternate Base . All Enchantments worn by the Bearer , including THIS , are Persistent while THIS is worn . THIS remains active while the bearer is dead . A caster may only have a single THIS Enchantment at a time and may not use Alternate Bases . Bearer may not be treated as an Alternate Base . Greater Mend and Word of Mending will not remove” vs “Caster heals”; nothing vs “Kill Trigger .” |
| does more than | [Protection from Evil](../profiles/protection-from-evil.md) | Paladin 3rd | only Golem: Curses (bearer, while worn); only Golem: Changes Mend (bearer, while worn); only Golem: Heals wounds (bearer, amount one, instant); only Golem: Acts as a respawn point (caster-of-enchantment, while worn, if caster-alive); only Golem: Acts as an Alternate Base (caster-of-enchantment, while worn); only Golem: Makes Enchantments Persistent (bearer, while worn); only Golem: May not use alternate bases (caster-of-enchantment, while worn); restriction only in Golem: bearer-not-alternate-base, caster-may-not-use-alternate-bases; school: Sorcery vs Protection | nothing vs “the”; nothing vs “School”; “Bearer” vs “This enchantment”; and 6 more |

## [Greater Mend](../profiles/greater-mend.md)

By touch, restores all armor points in one location, one armor point in every location, or repairs a damaged or broken item.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Mend](../profiles/mend.md) | Archer 2nd, Bard 2nd, Druid 1st, Healer 3rd, Wizard 1st | Repairs armor: amount all-points-one-location, instant vs amount one-point-one-location, instant | “Will restore all” vs “Destroyed or damaged item is repaired , or one point of”; “points” vs nothing; “, repair one armor point in each location , or repair a damaged or broken item” vs “is repaired” |
| is given by | [Artificer](../profiles/artificer.md) | Archer 6th | only Greater Mend: Repairs armor (hit-location, amount all-points-one-location, instant); only Greater Mend: Repairs armor (target, amount one-point-each-location, instant); only Greater Mend: Repairs equipment (target-equipment, instant); only Artificer: Allows equipment (bearer, permanent); only Artificer: Grants Greater Mend (bearer, permanent); only Artificer: Changes Mend (bearer, permanent); only Artificer: Changes Mend (bearer, permanent); only Artificer: Changes how often abilities can be used (bearer, permanent); only Artificer: Changes how often abilities can be used (bearer, permanent); only Artificer: Changes how often abilities can be used (bearer, permanent); only Artificer: Grants Pinning Arrow (bearer, permanent); only Artificer: Grants Phase Arrow (bearer, permanent); only Artificer: Grants Suppression Arrow (bearer, permanent); only Artificer: Changes Look The Part (bearer, permanent); requirement only in Artificer: needs-remaining-use; property only in Greater Mend: has-choice, targets-equipment, targets-player-affects-equipment; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Touch vs - | “Will restore all armor points in one location” vs “May wield a Small shield . Gain Greater Mend 2/Refresh Charge x10 (ex) . Mend becomes 2/Life Charge x3 (ex) . Casting Mend on weapons or shields does not consume a use of Mend . Rather than the normal amount of Specialty Arrows for an Archer”; “repair one armor point in each location ,” vs “gain : - Pinning Arrow 3 Arrows / Unlimited (ex) - Phase Arrow 2 Arrows / Unlimited (ex) - Suppression Arrow 2 Arrows / Unlimited (ex) Look the Part becomes a fourth Pinning Arrow . Must still have a use of Mend remaining to cast on weapons”; “repair a damaged or broken item” vs “shields” |
| overlap | [Scavenge](../profiles/scavenge.md) | Warrior 2nd | only Greater Mend: Repairs armor (hit-location, amount all-points-one-location, instant); only Greater Mend: Repairs armor (target, amount one-point-each-location, instant); only Greater Mend: Repairs equipment (target-equipment, instant); only Scavenge: Repairs equipment (bearer-equipment, instant); only Scavenge: Repairs armor (bearer-equipment, amount one-point-one-location, instant); requirement only in Scavenge: immediately-after-kill; property only in Greater Mend: targets-equipment, targets-player-affects-equipment; property only in Scavenge: kill-trigger; range: Touch vs Self | “Will restore all” vs “A destroyed or damaged item carried by the caster is repaired , or one point of”; “points” vs nothing; “location , repair one armor point in each location , or repair a damaged or broken item” vs “of the caster's hit locations is repaired”; and 1 more |
| overlap | [Word of Mending](../profiles/word-of-mending.md) | Druid 6th, Wizard 6th | Repairs armor: amount all-points-one-location, instant vs amount all-armor, instant; only Greater Mend: Repairs equipment (target-equipment, instant); only Word of Mending: Repairs equipment (target, instant); requirement only in Word of Mending: no-enemy-within-20ft; property only in Greater Mend: has-choice, targets-equipment | “Will restore all” vs “All equipment carried by target player is repaired . All”; “points in one location , repair one armor point in each location , or repair” vs “worn by target player is restored to full value . May not be cast within 20' of”; “damaged or broken item” vs “living enemy” |

## [Harden Armor](../profiles/harden-armor.md)

Armor Breaking strikes to the bearer's worn armor count as regular strikes; does not apply to Magic Armor.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Juggernaut](../profiles/juggernaut.md) | Warrior 6th | only Harden Armor: Protects armor (bearer-equipment, while worn); only Juggernaut: Grants Harden Armor (bearer, permanent); only Juggernaut: Grants Phoenix Tears (bearer, permanent); only Juggernaut: Replaces an ability (bearer, permanent); only Juggernaut: Removes Ancestral Armor (bearer, permanent); only Juggernaut: Removes True Grit (bearer, permanent); requirement only in Harden Armor: bearer-wears-armor; delivery: enchantment vs archetype; school: Protection vs Neutral; range: Other vs - | nothing vs “Gain Harden”; “Breaking strikes to” vs “(Self) 1/Life (ex) and Phoenix Tears (Self) 3/Refresh (ex) (Swift) . Replace Harden with Greater Harden (Self) (ex) at”; “bearer's armor are treated as regular strikes” vs “same frequency”; and 2 more |

## [Heal](../profiles/heal.md)

Heals one wound on a player by Touch (self or another).

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Greater Heal](../profiles/greater-heal.md) | Paladin 2nd, Healer 4th | Heals wounds: amount one, instant vs amount all, instant; property only in Greater Heal: bypass-cursed | “Target player heals a wound” vs “All wounds are healed”; nothing vs “Ignores the Cursed State .” |
| is given by | [Battlefield Triage](../profiles/battlefield-triage.md) | Bard 3rd | only Heal: Heals wounds (target, amount one, instant); only Battlefield Triage: Casts Heal from strips (bearer, while worn); only Battlefield Triage: Uses up a strip (bearer, instant); ends when only in Battlefield Triage: last-strip; property only in Battlefield Triage: materials-required, uses-strips; delivery: verbal vs enchantment | “Target player heals a wound” vs “Bearer may cast Heal (m) by incanting Thou art made whole and removing an enchantment strip”; nothing vs “Enchantment is removed when the last strip is removed .” |
| is given by | [Gift of Water](../profiles/gift-of-water.md) | Druid 4th | only Heal: Heals wounds (target, amount one, instant); only Gift of Water: Grants Magic Armor (bearer, points 1, while worn); only Gift of Water: Grants Heal (bearer, while worn); delivery: verbal vs enchantment; school: Spirit vs Sorcery; range: Touch vs Other | “Target player heals a wound” vs “Bearer gains one point of Magic Armor and Heal (Self) Unlimited (m)” |
| is given by | [Mass Healing](../profiles/mass-healing.md) | Healer 6th | only Heal: Heals wounds (target, amount one, instant); only Mass Healing: Casts Heal from strips (bearer, while worn); only Mass Healing: Casts by declaration (bearer, while worn); only Mass Healing: Uses up a strip (bearer, instant); ends when only in Mass Healing: last-strip; property only in Mass Healing: castable-while-moving, declaration-not-incantation, materials-required, must-declare, uses-strips, works-while-suppressed; delivery: verbal vs enchantment; range: Touch vs Self | “Target” vs “Caster may Heal (m) a”; “heals a wound” vs “at Touch by declaring I grant thee healing and removing an enchantment strip”; nothing vs “Enchantment is removed when the last strip is removed . The declaration is not an incantation , and so is not stopped by being Suppressed , and may be used while moving , etc .” |
| is given by | [Regeneration](../profiles/regeneration.md) | Druid 3rd | only Heal: Heals wounds (target, amount one, instant); only Regeneration: Grants Heal (bearer, while worn); only Regeneration: Changes Heal (bearer, while worn); property only in Regeneration: must-declare; delivery: verbal vs enchantment; range: Touch vs Other | “Target player heals” vs “Bearer gains Heal (Self) Unlimited (m) (Swift) . The Heal granted by THIS may not be used within 10' of”; “wound” vs “living enemy”; nothing vs “Bearer must state Swift normally .” |
| overlap | [Adrenaline](../profiles/adrenaline.md) | Barbarian 3rd | only Heal: Heals wounds (target, amount one, instant); only Adrenaline: Heals wounds (caster, amount one, instant); requirement only in Adrenaline: immediately-after-kill; property only in Adrenaline: kill-trigger; range: Touch vs Self | “Target player” vs “Caster”; nothing vs “Kill Trigger .” |

## [Heat Weapon](../profiles/heat-weapon.md)

A targeted weapon within 20' cannot be wielded for 30 seconds, except by players Immune to Flame.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Gift of Fire](../profiles/gift-of-fire.md) | Druid 3rd | only Heat Weapon: Disables equipment (target-equipment, 30 s); only Gift of Fire: Grants Heat Weapon (bearer, while worn); only Gift of Fire: Immune to Flame (bearer, while worn); requirement only in Heat Weapon: target-is-equipment; property only in Heat Weapon: targets-equipment; delivery: verbal vs enchantment; range: 20' vs Other | “Target weapon may not be wielded for 30 seconds . Players who are” vs “Bearer gains Heat Weapon 1/Refresh Charge x3 (m) and is”; “may continue to wield the weapon” vs nothing; “The equipment , not the person , is the target of THIS . The equipment is the only thing required to be within range and visible for this ability to affect it .” vs nothing |

## [Iceball](../profiles/iceball.md)

Engulfing Magic Ball: the player struck is Frozen for 60 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Icy Blast](../profiles/icy-blast.md) | Druid 3rd, Wizard 4th | Freezes: 60 s vs 30 s; property only in Iceball: engulfing; delivery: magic-ball vs verbal; school: Subdual vs Sorcery; range: - vs 20' | “Player struck is” vs “Target player becomes”; “60” vs “30”; “Engulfing .” vs nothing |
| overlap | [Force Barrier](../profiles/force-barrier.md) | Wizard 1st | only Iceball: Freezes (struck-player, 60 s); only Force Barrier: Freezes (caster, 10 s); property only in Iceball: engulfing; delivery: magic-ball vs verbal; school: Subdual vs Sorcery; range: - vs Self | “Player struck” vs “Caster”; “60” vs “10”; “Engulfing .” vs nothing |
| overlap | [Stoneform](../profiles/stoneform.md) | Druid 2nd | only Iceball: Freezes (struck-player, 60 s); only Stoneform: Freezes (caster, until removed); ends when only in Stoneform: exit-at-will; property only in Iceball: engulfing; property only in Stoneform: must-declare; delivery: magic-ball vs verbal; school: Subdual vs Protection; range: - vs Self | “Player struck” vs “Caster”; “for 60 seconds” vs nothing; “Engulfing” vs “May end this State at any time by saying The earth release me x2” |

## [Icy Blast](../profiles/icy-blast.md)

Freezes a player within 20' for 30 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Iceball](../profiles/iceball.md) | Druid 4th, Healer 3rd, Wizard 3rd | Freezes: 30 s vs 60 s; property only in Iceball: engulfing; delivery: verbal vs magic-ball; school: Sorcery vs Subdual; range: 20' vs - | “Target player becomes” vs “Player struck is”; “30” vs “60”; nothing vs “Engulfing .” |
| overlap | [Force Barrier](../profiles/force-barrier.md) | Wizard 1st | only Icy Blast: Freezes (target, 30 s); only Force Barrier: Freezes (caster, 10 s); range: 20' vs Self | “Target player becomes” vs “Caster is”; “30” vs “10” |
| overlap | [Stoneform](../profiles/stoneform.md) | Druid 2nd | only Icy Blast: Freezes (target, 30 s); only Stoneform: Freezes (caster, until removed); ends when only in Stoneform: exit-at-will; property only in Stoneform: must-declare; school: Sorcery vs Protection; range: 20' vs Self | “Target player becomes” vs “Caster is”; “for 30 seconds” vs nothing; nothing vs “May end this State at any time by saying The earth release me x2 .” |

## [Innate](../profiles/innate.md)

Meta-Magic: instantly Charges a single ability, named aloud, without the Charge Incantation.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects | [Momentum](../profiles/momentum.md) | Archer 6th, Barbarian 6th, Warrior 6th | requirement only in Momentum: immediately-after-kill; property only in Momentum: kill-trigger; delivery: meta-magic vs verbal; school: Neutral vs Sorcery; range: - vs Self | nothing vs “Kill Trigger” |
| overlap | [Confidence](../profiles/confidence.md) | Bard 1st | only Innate: Instantly Charges an ability (caster, instant); only Confidence: Instantly Charges an ability (target, instant); requirement only in Confidence: no-enemy-within-20ft; property only in Innate: must-declare; delivery: meta-magic vs verbal; school: Neutral vs Sorcery; range: - vs Other | “May be used to” vs “Target player may”; “by stating its name” vs nothing; nothing vs “May not be used within 20' of a living enemy .” |

## [Ironskin](../profiles/ironskin.md)

Bearer is Immune to Flame and gains 2 points of Magic Armor that work as per Ancestral Armor.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Ancestral Armor](../profiles/ancestral-armor.md) | Warrior 6th, Healer 6th | only Ironskin: Immune to Flame (bearer, while worn); only Ironskin: Grants Magic Armor (bearer, points 2, while worn); only Ironskin: Works as Ancestral Armor (bearer, while worn); only Ancestral Armor: Ignores a hit (bearer, instant, if armor-has-points); only Ancestral Armor: Damages armor (bearer-equipment, points 1, instant, if armor-has-points); property only in Ancestral Armor: reusable; range: Other vs Other, Self | “Bearer” vs “The effects of a Magic Ball , projectile weapon , or melee weapon which just struck armor worn by the player are ignored , even if the object would not otherwise affect the armor . The armor loses one point of value in the location struck . This effect will not trigger if the armor has no points left in the location struck . THIS”; “Immune” vs “not expended after use and will continue”; “Flame” vs “provide protection until removed with Dispel Magic or similar abilities . Engulfing Effects that do not strike the bearer's armor , abilities that ignore armor entirely ,”; and 2 more |
| does more than | [Barkskin](../profiles/barkskin.md) | Druid 1st | Grants Magic Armor: points 2, while worn vs points 1, while worn; only Ironskin: Immune to Flame (bearer, while worn); only Ironskin: Works as Ancestral Armor (bearer, while worn) | “is Immune to Flame and” vs nothing; “two points” vs “one point of”; “affected as per Ancestral Armor” vs nothing |
| does more than | [Stoneskin](../profiles/stoneskin.md) | Druid 3rd | only Ironskin: Immune to Flame (bearer, while worn) | “is Immune to Flame and” vs nothing; “two” vs “2”; nothing vs “of” |

## [Lycanthropy](../profiles/lycanthropy.md)

Bearer gains 2 points of Magic Armor, Shield Crushing wielded melee weapons, and Immunity to Command.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Barkskin](../profiles/barkskin.md) | Druid 1st | Grants Magic Armor: points 2, while worn vs points 1, while worn; only Lycanthropy: Shield Crushing (bearer melee weapons) (bearer, while worn); only Lycanthropy: Immune to Command (bearer, while worn); school: Death vs Protection | “two points” vs “one point”; “magic armor” vs “Magic Armor”; “Bearer's wielded melee weapons are Shield Crushing . Bearer is Immune to Command .” vs nothing |
| does more than | [Bear Strength](../profiles/bear-strength.md) | Druid 3rd, Barbarian 6th | only Lycanthropy: Grants Magic Armor (bearer, points 2, while worn); only Lycanthropy: Immune to Command (bearer, while worn); school: Death vs Sorcery | “Bearer gains two points of magic armor .” vs nothing; “Bearer is Immune to Command .” vs nothing |

## [Mend](../profiles/mend.md)

By touch, repairs a destroyed or damaged item, or repairs one point of armor in one location.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Greater Mend](../profiles/greater-mend.md) | Druid 3rd, Wizard 3rd, Archer 6th | Repairs armor: amount one-point-one-location, instant vs amount all-points-one-location, instant | “Destroyed or damaged item is repaired , or one point of” vs “Will restore all”; nothing vs “points”; “is repaired” vs “, repair one armor point in each location , or repair a damaged or broken item” |
| is given by | [Apex](../profiles/apex.md) | Scout 6th | only Mend: Repairs equipment (target-equipment, instant); only Mend: Repairs armor (hit-location, amount one-point-one-location, instant); only Apex: Grants Mend (bearer, permanent); only Apex: Grants Sleight of Mind (bearer, permanent); only Apex: Removes Evolution (bearer, permanent); only Apex: Removes Hold Person (bearer, permanent); only Apex: Removes Pinning Arrow (bearer, permanent); property only in Mend: has-choice, targets-equipment, targets-player-affects-equipment; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Touch vs - | “Destroyed or damaged item is repaired” vs “Gain Mend 1/Life (ex) and Sleight of Mind (Self) 1/Life (ex) . Lose all instances of Evolution”; “or one point of armor in one location is repaired .” vs “Hold Person , and Pinning Arrow” |
| is given by | [Sniper](../profiles/sniper.md) | Archer 6th | only Mend: Repairs equipment (target-equipment, instant); only Mend: Repairs armor (hit-location, amount one-point-one-location, instant); only Sniper: Allows equipment (bearer, permanent); only Sniper: Changes how often abilities can be used (bearer, permanent); only Sniper: Grants Momentum (bearer, permanent); only Sniper: Changes Look The Part (bearer, permanent); only Sniper: May not fire normal arrows (bearer, permanent); property only in Mend: has-choice, targets-equipment, targets-player-affects-equipment; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Touch vs - | “Destroyed or damaged item is repaired , or one point” vs “May physically carry any number”; “armor in one location is repaired” vs “Specialty Arrows of each type”; nothing vs “The frequency of each type of Specialty Arrow ability becomes 1 Arrow / Life Charge x3 . Gain Momentum Unlimited (ex) (Ambulant) . Look the Part becomes Mend 1/Life (ex) . May not fire normal arrows .” |
| overlap | [Scavenge](../profiles/scavenge.md) | Warrior 2nd | only Mend: Repairs equipment (target-equipment, instant); only Mend: Repairs armor (hit-location, amount one-point-one-location, instant); only Scavenge: Repairs equipment (bearer-equipment, instant); only Scavenge: Repairs armor (bearer-equipment, amount one-point-one-location, instant); requirement only in Scavenge: immediately-after-kill; property only in Mend: targets-equipment, targets-player-affects-equipment; property only in Scavenge: kill-trigger; range: Touch vs Self | “Destroyed” vs “A destroyed”; nothing vs “carried by the caster”; “location” vs “of the caster's hit locations”; and 1 more |
| overlap | [Word of Mending](../profiles/word-of-mending.md) | Druid 6th, Wizard 6th | Repairs armor: amount one-point-one-location, instant vs amount all-armor, instant; only Mend: Repairs equipment (target-equipment, instant); only Word of Mending: Repairs equipment (target, instant); requirement only in Word of Mending: no-enemy-within-20ft; property only in Mend: has-choice, targets-equipment | “Destroyed or damaged item is repaired , or one point of armor in one location” vs “All equipment carried by target player”; nothing vs “All armor worn by target player is restored to full value . May not be cast within 20' of a living enemy .” |

## [Naturalize Magic](../profiles/naturalize-magic.md)

Self Enchantment with three strips: bearer may cast Dispel Magic (m) by incanting and removing a strip; removed with the last strip.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Dispel Magic](../profiles/dispel-magic.md) | Scout 3rd, Druid 3rd, Healer 4th, Wizard 3rd | only Naturalize Magic: Casts Dispel Magic from strips (bearer, while worn); only Naturalize Magic: Uses up a strip (bearer, instant); only Dispel Magic: Removes Enchantments (target, instant); requirement only in Dispel Magic: target-not-invulnerable; ends when only in Naturalize Magic: last-strip; property only in Naturalize Magic: materials-required, uses-strips; property only in Dispel Magic: bypass-enchantments, bypass-immunities, bypass-ongoing-effects, bypass-states, bypass-traits; delivery: enchantment vs verbal; range: Self vs 20' | “Bearer may cast Dispel Magic (m) by incanting Player thou art dispelled and removing an enchantment strip . Enchantment is removed when the last strip is” vs “All Enchantments on target are”; nothing vs “Will always remove Enchantments if successfully cast on a valid target , regardless of the player's Traits , States , Immunities , Ongoing Effects , or Enchantments (except Sleight of Mind) . Does not affect Invulnerable players .” |

## [Poison](../profiles/poison.md)

The bearer's next wound dealt with a wielded melee weapon is Wounds Kill; not expended if the target does not actually receive the wound.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Poison Glands](../profiles/poison-glands.md) | Druid 5th | only Poison: Wounds Kill (next wound) (bearer, until used); only Poison Glands: Grants Poison (bearer, while worn); ends when only in Poison: activates-once; property only in Poison: not-expended-on-failure; range: Other, Self vs Other | “The next wound dealt by the bearer with a wielded melee weapon is Wounds Kill” vs “Bearer gains Poison (Self) 1/Refresh Charge x3 (ex)”; “If the target does not actually receive a wound , e . g . by a Resistance , THIS is not expended .” vs nothing |
| overlap | [Poison Arrow](../profiles/poison-arrow.md) | Archer 1st,3rd,5th, Assassin 2nd | only Poison: Wounds Kill (next wound) (bearer, until used); only Poison Arrow: Wounds Kill (this arrow) (struck-player, instant); ends when only in Poison: activates-once; property only in Poison: not-expended-on-failure; delivery: enchantment vs specialty-arrow; range: Other, Self vs - | “The next wound dealt by the bearer with a wielded melee weapon” vs “This arrow”; “If the target does not actually receive a wound , e . g . by a Resistance , THIS is not expended .” vs nothing |
| overlap | [Toxic Blades](../profiles/toxic-blades.md) | Druid 6th | only Poison: Wounds Kill (next wound) (bearer, until used); only Toxic Blades: Wounds Kill (bearer melee weapons) (bearer, while worn); ends when only in Poison: activates-once; property only in Poison: not-expended-on-failure; range: Other, Self vs Other | “The next wound dealt by the bearer with a” vs “Bearer's”; “weapon is” vs “weapons are”; “If the target does not actually receive a wound , e . g . by a Resistance , THIS is not expended .” vs nothing |
| overlap | [Contagion](../profiles/contagion.md) | Wizard 5th | only Poison: Wounds Kill (next wound) (bearer, until used); only Contagion: Wounds Kill (bearer melee weapons) (bearer, while worn); only Contagion: Makes Fragile (bearer, while worn); ends when only in Poison: activates-once; property only in Poison: not-expended-on-failure; range: Other, Self vs Other | “The next wound dealt by the bearer with a” vs “Bearers”; “weapon is” vs “weapons are”; “If the target does not actually receive a wound , e” vs “Bearer is Fragile”; and 1 more |

## [Poison Glands](../profiles/poison-glands.md)

Enchantment on another player: bearer gains Poison (Self) 1/Refresh Charge x3 (ex), making their next melee wound Wounds Kill.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Poison](../profiles/poison.md) | Anti-Paladin 2nd, Assassin 2nd, Druid 2nd, Assassin 1st | only Poison Glands: Grants Poison (bearer, while worn); only Poison: Wounds Kill (next wound) (bearer, until used); ends when only in Poison: activates-once; property only in Poison: not-expended-on-failure; range: Other vs Other, Self | “Bearer gains Poison (Self) 1/Refresh Charge x3 (ex)” vs “The next wound dealt by the bearer with a wielded melee weapon is Wounds Kill”; nothing vs “If the target does not actually receive a wound , e . g . by a Resistance , THIS is not expended .” |

## [Regeneration](../profiles/regeneration.md)

Bearer gains Heal (Self) Unlimited (m) with Swift, usable only with no living enemy within 10'.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Gift of Water](../profiles/gift-of-water.md) | Druid 4th | only Regeneration: Grants Heal (bearer, while worn); only Regeneration: Changes Heal (bearer, while worn); only Gift of Water: Grants Magic Armor (bearer, points 1, while worn); only Gift of Water: Grants Heal (bearer, while worn); property only in Regeneration: must-declare; school: Spirit vs Sorcery | nothing vs “one point of Magic Armor and”; “(Swift)” vs nothing; “The Heal granted by THIS may not be used within 10' of a living enemy . Bearer must state Swift normally .” vs nothing |
| does less than | [Troll Blood](../profiles/troll-blood.md) | Druid 5th | only Regeneration: Grants Heal (bearer, while worn); only Regeneration: Changes Heal (bearer, while worn); only Troll Blood: Prevents death (bearer, while worn); only Troll Blood: Ignores a hit (bearer, instant); only Troll Blood: Uses up a strip (bearer, instant); only Troll Blood: Freezes (bearer, 30 s); only Troll Blood: Works as Regeneration (bearer, while worn); ends when only in Troll Blood: last-strip; property only in Regeneration: must-declare; property only in Troll Blood: uses-strips; school: Spirit vs Protection | “gains Heal (Self) Unlimited (m) (Swift)” vs “does not die as normal . When the bearer would otherwise die they instead ignore the triggering effect as though it had not occurred , remove a strip , and become Frozen for 30 seconds”; “Heal granted by” vs “bearer is treated as though they have the effects of Regeneration in addition to the above .”; “may not be used within 10' of a living enemy” vs “is removed when the last strip is removed”; and 1 more |
| gives its user | [Heal](../profiles/heal.md) | Monk 4th, Scout 2nd,5th, Druid 2nd, Healer 1st, Monk 1st, Scout 1st | only Regeneration: Grants Heal (bearer, while worn); only Regeneration: Changes Heal (bearer, while worn); only Heal: Heals wounds (target, amount one, instant); property only in Regeneration: must-declare; delivery: enchantment vs verbal; range: Other vs Touch | “Bearer gains Heal (Self) Unlimited (m) (Swift)” vs “Target player heals a wound”; “The Heal granted by THIS may not be used within 10' of a living enemy . Bearer must state Swift normally .” vs nothing |

## [Release](../profiles/release.md)

By touch, removes one State or Ongoing Effect of the caster's choice (not Cursed), along with others from the same source.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Greater Release](../profiles/greater-release.md) | Bard 2nd, Healer 2nd | only Release: Removes States or Ongoing Effects (target, instant); only Release: Removes States or Ongoing Effects (target, instant); only Greater Release: Removes States or Ongoing Effects (target, instant); only Greater Release: Removes States or Ongoing Effects (dead-target, instant); only Greater Release: Removes States or Ongoing Effects (target, instant); property only in Greater Release: bypass-cursed; range: Touch vs 20' | “A single” vs “All”; “Effect or State is” vs “Effects and States are”; “Casters choice” vs “The caster may choose to leave some States or Effects in place”; and 1 more |
| overlap | [Shake It Off](../profiles/shake-it-off.md) | Warrior 5th | only Release: Removes States or Ongoing Effects (target, instant); only Release: Removes States or Ongoing Effects (target, instant); only Shake It Off: Removes States or Ongoing Effects (caster, instant); requirement only in Shake It Off: caster-alive; property only in Shake It Off: works-while-suppressed; school: Sorcery vs Spirit; range: Touch vs Self | “A single” vs “10 seconds after casting THIS the caster may remove from themselves any number of States or”; “Effect or State is removed from the target . Casters” vs “Effects of their”; “Cannot remove Cursed” vs “THIS may be cast at any time the caster is alive , even while the caster would otherwise be prevented from casting abilities by Stunned , Suppressed , or similar”; and 4 more |

## [Resurrect](../profiles/resurrect.md)

Returns a willing dead player (within 5' of where they died) to life with all wounds healed, removing non-Persistent Enchantments first.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Greater Resurrect](../profiles/greater-resurrect.md) | Paladin 4th, Healer 5th | only Resurrect: Removes Enchantments (dead-target, instant); only Greater Resurrect: Ends Cursed (dead-target, instant); property only in Greater Resurrect: bypass-cursed, bypass-states | “Non-Persistent Enchantments on the player are removed before the player returns to life .” vs nothing; nothing vs “Works regardless of any States on the target , and removes Cursed if present . Enchantments on the player are retained .” |
| same without the drawback or cost | [Raise Dead](../profiles/raise-dead.md) | Healer 3rd | only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); school: Spirit vs Death | nothing vs “and is Cursed . Target is also Suppressed for 30 seconds” |
| overlap | [True Grit](../profiles/true-grit.md) | Warrior 3rd | only Resurrect: Removes Enchantments (dead-target, instant); only Resurrect: Returns to life (dead-target, instant); only Resurrect: Heals wounds (dead-target, amount all, instant); only True Grit: Returns to life (caster, instant); only True Grit: Heals wounds (caster, amount all, instant); only True Grit: Freezes (caster, 30 s); requirement only in Resurrect: target-dead, target-not-moved-5ft, target-willing; requirement only in True Grit: after-dying; range: Other vs Self | “Target willing dead player who has not moved more than 5' from where they died is returned” vs “Caster returns”; nothing vs “with their wounds healed and is immediately Frozen for 30 seconds”; “Non-Persistent” vs nothing; and 3 more |

## [Snaring Vines](../profiles/snaring-vines.md)

Three strips: bearer may cast Hold Person (m) by removing a strip; the Enchantment ends when the last strip is removed.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Hold Person](../profiles/hold-person.md) | Assassin 4th, Scout 4th, Healer 2nd, Wizard 3rd | only Snaring Vines: Casts Hold Person from strips (bearer, while worn); only Snaring Vines: Uses up a strip (bearer, instant); only Hold Person: Stops (target, 30 s); ends when only in Snaring Vines: last-strip; property only in Snaring Vines: materials-required, uses-strips; delivery: enchantment vs verbal; range: Self vs 20' | “Bearer may cast Hold Person (m) by incanting Player stop at my command and removing an enchantment strip” vs “Target player becomes Stopped for 30 seconds”; “Enchantment is removed when the last strip is removed .” vs nothing |

## [Stoneform](../profiles/stoneform.md)

Caster Freezes themselves, protected from combat and most abilities, until they end it by saying "The earth release me" x2.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Force Barrier](../profiles/force-barrier.md) | Wizard 1st | Freezes: until removed vs 10 s; ends when only in Stoneform: exit-at-will; property only in Stoneform: must-declare; school: Protection vs Sorcery | nothing vs “for 10 seconds”; “May end this State at any time by saying The earth release me x2 .” vs nothing |
| overlap | [Iceball](../profiles/iceball.md) | Druid 4th, Healer 3rd, Wizard 3rd | only Stoneform: Freezes (caster, until removed); only Iceball: Freezes (struck-player, 60 s); ends when only in Stoneform: exit-at-will; property only in Stoneform: must-declare; property only in Iceball: engulfing; delivery: verbal vs magic-ball; school: Protection vs Subdual; range: Self vs - | “Caster” vs “Player struck”; nothing vs “for 60 seconds”; “May end this State at any time by saying The earth release me x2” vs “Engulfing” |
| overlap | [Icy Blast](../profiles/icy-blast.md) | Druid 3rd, Wizard 4th | only Stoneform: Freezes (caster, until removed); only Icy Blast: Freezes (target, 30 s); ends when only in Stoneform: exit-at-will; property only in Stoneform: must-declare; school: Protection vs Sorcery; range: Self vs 20' | “Caster is” vs “Target player becomes”; nothing vs “for 30 seconds”; “May end this State at any time by saying The earth release me x2 .” vs nothing |

## [Stoneskin](../profiles/stoneskin.md)

Bearer gains 2 points of Magic Armor that work as per Ancestral Armor.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Ancestral Armor](../profiles/ancestral-armor.md) | Warrior 6th, Healer 6th | only Stoneskin: Grants Magic Armor (bearer, points 2, while worn); only Stoneskin: Works as Ancestral Armor (bearer, while worn); only Ancestral Armor: Ignores a hit (bearer, instant, if armor-has-points); only Ancestral Armor: Damages armor (bearer-equipment, points 1, instant, if armor-has-points); property only in Ancestral Armor: reusable; range: Other vs Other, Self | “Bearer gains 2” vs “The effects of a Magic Ball , projectile weapon , or melee weapon which just struck armor worn by the player are ignored , even if the object would not otherwise affect the armor . The armor loses one point of value in the location struck . This effect will not trigger if the armor has no”; “of” vs “left in the location struck . THIS is not expended after use and will continue to provide protection until removed with Dispel”; “Armor affected” vs “or similar abilities . Engulfing Effects that do not strike the bearer's armor , abilities that ignore armor entirely , and abilities that have been entirely negated due to Ability Order do not trigger THIS . Phasing equipment interacts with armor worn by the bearer”; and 1 more |
| does more than | [Barkskin](../profiles/barkskin.md) | Druid 1st | Grants Magic Armor: points 2, while worn vs points 1, while worn; only Stoneskin: Works as Ancestral Armor (bearer, while worn) | “2 points” vs “one point”; “affected as per Ancestral Armor” vs nothing |
| does less than | [Ironskin](../profiles/ironskin.md) | Druid 5th | only Ironskin: Immune to Flame (bearer, while worn) | nothing vs “is Immune to Flame and”; “2” vs “two”; “of” vs nothing |

## [Swift](../profiles/swift.md)

Meta-Magic: the next Touch, Other, Self or Magic Ball ability needs only one iteration of its incantation (last line if multi-line).

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Medium](../profiles/medium.md) | Monk 6th | only Swift: Modifies the next ability cast (caster, until used); only Medium: Grants Blessing Against Wounds (bearer, permanent); only Medium: Grants Sever Spirit (bearer, permanent); only Medium: Grants Swift (bearer, permanent); only Medium: Changes how often abilities can be used (bearer, permanent); only Medium: May not wear armor (bearer, permanent); only Medium: May not wield great weapons (bearer, permanent); requirement only in Swift: not-on-charge-incantation, only-touch-other-self-or-balls; delivery: meta-magic vs archetype | nothing vs “Gain Blessing Against Wounds (Touch) 1/Life (ex) , Sever Spirit 1/Life Charge x3 (ex) , and Swift 2/Life (ex) .”; “require only a single iteration of” vs “in”; “incantation . For multi-line Incantations use the last line . May only be used on abilities at a range of Touch , Other , Self , or on Magic Balls” vs “Spirit school become Charge x3”; and 1 more |
| is given by | [Silver Tongue](../profiles/silver-tongue.md) | Bard 6th | only Swift: Modifies the next ability cast (caster, until used); only Silver Tongue: Grants Swift (bearer, while worn); only Silver Tongue: May not use other sources of ability (bearer, while worn); requirement only in Swift: not-on-charge-incantation, only-touch-other-self-or-balls; restriction only in Silver Tongue: excludes-other-sources; delivery: meta-magic vs enchantment; school: Neutral vs Sorcery; range: - vs Touch | “Abilities require only a single iteration” vs “Bearer gains Swift 1/Refresh Charge x3 (m) . Other sources”; “the incantation . For multi-line Incantations use the last line . May only be used on abilities at a range of Touch , Other , Self , or on Magic Balls . May” vs “Swift may”; “used on the Charge Incantation” vs “utilized while THIS is worn”; and 1 more |

## [Teleport](../profiles/teleport.md)

A willing player becomes Insubstantial and travels directly to a fixed location the caster chose, ending it on arrival.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Lost](../profiles/lost.md) | Bard 5th | only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; school: Sorcery vs Command; range: Self, Touch vs 20' | “willing” vs nothing; “and moves” vs “, must move”; “a chosen location chosen by the caster at the time of casting . This must be a fixed location (not relative to a player or to a moveable object)” vs “their base”; and 5 more |
| overlap | [Astral Intervention](../profiles/astral-intervention.md) | Healer 3rd, Wizard 2nd | Makes Insubstantial: until arrival, if cast-on-self vs 30 s, if cast-on-self; only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); requirement only in Teleport: target-willing; ends when only in Teleport: insubstantial-ends, on-arrival; property only in Teleport: forced-movement; school: Sorcery vs Command; range: Self, Touch vs 20' | “willing” vs nothing; “and moves directly to a chosen location chosen by the caster at the time of casting . This must be a fixed location (not relative to a player or to a moveable object) . Upon arrival , they must immediately end the effect as per Insubstantial” vs “for 30 seconds”; “the player's Insubstantial State is removed before they have reached their destination , the effects of THIS end . If THIS is” vs nothing; and 1 more |
| overlap | [Banish](../profiles/banish.md) | Monk 2nd, Healer 1st, Wizard 1st | only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Makes Insubstantial (caster, until arrival, if cast-on-self); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); only Banish: Sends to base (target, until arrival, if cast-on-other); only Banish: Sends to base (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; requirement only in Banish: target-insubstantial; school: Sorcery vs Spirit; range: Self, Touch vs 20' | “willing” vs “Insubstantial”; “becomes Insubstantial and moves directly” vs “must return”; “a chosen location chosen by the caster at the time of casting . This must be a fixed location (not relative to a player or to a moveable object)” vs “their base”; and 5 more |
| overlap | [Shadow Step](../profiles/shadow-step.md) | Assassin 1st, Scout 3rd | Makes Insubstantial: until arrival, if cast-on-self vs until removed; only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; ends when only in Teleport: insubstantial-ends, on-arrival; property only in Teleport: forced-movement; property only in Shadow Step: castable-while-moving; range: Self, Touch vs Self | “Target willing player” vs “Caster”; “and moves directly to a chosen location chosen by the caster at the time of casting” vs nothing; “This must” vs “THIS may”; and 3 more |

## [Toxic Blades](../profiles/toxic-blades.md)

Bearer's wielded melee weapons are Wounds Kill.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same without the drawback or cost | [Contagion](../profiles/contagion.md) | Wizard 5th | only Contagion: Makes Fragile (bearer, while worn) | “Bearer's” vs “Bearers”; nothing vs “Bearer is Fragile .” |
| overlap | [Poison](../profiles/poison.md) | Anti-Paladin 2nd, Assassin 2nd, Druid 2nd, Assassin 1st | only Toxic Blades: Wounds Kill (bearer melee weapons) (bearer, while worn); only Poison: Wounds Kill (next wound) (bearer, until used); ends when only in Poison: activates-once; property only in Poison: not-expended-on-failure; range: Other vs Other, Self | “Bearer's” vs “The next wound dealt by the bearer with a”; “weapons are” vs “weapon is”; nothing vs “If the target does not actually receive a wound , e . g . by a Resistance , THIS is not expended .” |
| overlap | [Poison Arrow](../profiles/poison-arrow.md) | Archer 1st,3rd,5th, Assassin 2nd | only Toxic Blades: Wounds Kill (bearer melee weapons) (bearer, while worn); only Poison Arrow: Wounds Kill (this arrow) (struck-player, instant); delivery: enchantment vs specialty-arrow; range: Other vs - | “Bearer's wielded melee weapons are” vs “This arrow is” |

## [Troll Blood](../profiles/troll-blood.md)

When the bearer would die they ignore it, lose one of three strips and are Frozen 30 seconds; bearer also has Regeneration.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Regeneration](../profiles/regeneration.md) | Druid 3rd | only Troll Blood: Prevents death (bearer, while worn); only Troll Blood: Ignores a hit (bearer, instant); only Troll Blood: Uses up a strip (bearer, instant); only Troll Blood: Freezes (bearer, 30 s); only Troll Blood: Works as Regeneration (bearer, while worn); only Regeneration: Grants Heal (bearer, while worn); only Regeneration: Changes Heal (bearer, while worn); ends when only in Troll Blood: last-strip; property only in Troll Blood: uses-strips; property only in Regeneration: must-declare; school: Protection vs Spirit | “does not die as normal . When the bearer would otherwise die they instead ignore the triggering effect as though it had not occurred , remove a strip , and become Frozen for 30 seconds” vs “gains Heal (Self) Unlimited (m) (Swift)”; “bearer is treated as though they have the effects” vs “Heal granted by THIS may not be used within 10'”; “Regeneration in addition to the above” vs “a living enemy”; and 1 more |

## [Word of Mending](../profiles/word-of-mending.md)

Repairs all equipment a touched player carries and restores all their worn armor to full; not within 20' of a living enemy.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Greater Mend](../profiles/greater-mend.md) | Druid 3rd, Wizard 3rd, Archer 6th | Repairs armor: amount all-armor, instant vs amount all-points-one-location, instant; only Word of Mending: Repairs equipment (target, instant); only Greater Mend: Repairs equipment (target-equipment, instant); requirement only in Word of Mending: no-enemy-within-20ft; property only in Greater Mend: has-choice, targets-equipment | “All equipment carried by target player is repaired” vs “Will restore all armor points in one location , repair one armor point in each location , or repair a damaged or broken item”; “All armor worn by target player is restored to full value . May not be cast within 20' of a living enemy .” vs nothing |
| overlap | [Mend](../profiles/mend.md) | Archer 2nd, Bard 2nd, Druid 1st, Healer 3rd, Wizard 1st | Repairs armor: amount all-armor, instant vs amount one-point-one-location, instant; only Word of Mending: Repairs equipment (target, instant); only Mend: Repairs equipment (target-equipment, instant); requirement only in Word of Mending: no-enemy-within-20ft; property only in Mend: has-choice, targets-equipment | “All equipment carried by target player” vs “Destroyed or damaged item is repaired , or one point of armor in one location”; “All armor worn by target player is restored to full value . May not be cast within 20' of a living enemy .” vs nothing |
| overlap | [Scavenge](../profiles/scavenge.md) | Warrior 2nd | only Word of Mending: Repairs equipment (target, instant); only Word of Mending: Repairs armor (target, amount all-armor, instant); only Scavenge: Repairs equipment (bearer-equipment, instant); only Scavenge: Repairs armor (bearer-equipment, amount one-point-one-location, instant); requirement only in Word of Mending: no-enemy-within-20ft; requirement only in Scavenge: immediately-after-kill; property only in Word of Mending: targets-player-affects-equipment; property only in Scavenge: has-choice, kill-trigger; range: Touch vs Self | “All equipment” vs “A destroyed or damaged item”; “target player” vs “the caster is repaired , or one point of armor in one of the caster's hit locations”; “All armor worn by target player is restored to full value” vs “Kill Trigger”; and 1 more |
