---
title: "Healer: duplicate check"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Healer: duplicate check

Every comparable entry on the Healer list against every other ability, spell and trait in the rulebook.

## [Abeyance](../profiles/abeyance.md)

Magic Ball ignoring armor: the player hit is Stunned for 60 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Stun](../profiles/stun.md) | Bard 6th, Healer 6th | Stuns: 60 s vs 30 s; property only in Abeyance: bypass-armor; delivery: magic-ball vs verbal; school: Subdual vs Sorcery; range: - vs 20' | “This Magic Ball ignores armor . Player hit” vs “Target player”; “60” vs “30” |

## [Ancestral Armor](../profiles/ancestral-armor.md)

Ignores Magic Ball, projectile and melee hits on the bearer's armor while that location has points; the armor loses one point instead. Reusable.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Ironskin](../profiles/ironskin.md) | Druid 5th | only Ancestral Armor: Ignores a hit (bearer, instant, if armor-has-points); only Ancestral Armor: Damages armor (bearer-equipment, points 1, instant, if armor-has-points); only Ironskin: Immune to Flame (bearer, while worn); only Ironskin: Grants Magic Armor (bearer, points 2, while worn); only Ironskin: Works as Ancestral Armor (bearer, while worn); property only in Ancestral Armor: reusable; range: Other, Self vs Other | “The effects of a” vs “Bearer is Immune to Flame and gains two points”; “Ball , projectile weapon , or melee weapon which just struck armor worn by the player are ignored , even if the object would not otherwise affect the armor” vs “Armor affected as per Ancestral Armor”; “The armor loses one point of value in the location struck . This effect will not trigger if the armor has no points left in the location struck . THIS is not expended after use and will continue to provide protection until removed with Dispel Magic or similar abilities . Engulfing Effects that do not strike the bearer's armor , abilities that ignore armor entirely , and abilities that have been entirely negated due to Ability Order do not trigger THIS . Phasing equipment interacts with armor worn by the bearer as though THIS was not present .” vs nothing |
| does less than | [Stoneskin](../profiles/stoneskin.md) | Druid 3rd | only Ancestral Armor: Ignores a hit (bearer, instant, if armor-has-points); only Ancestral Armor: Damages armor (bearer-equipment, points 1, instant, if armor-has-points); only Stoneskin: Grants Magic Armor (bearer, points 2, while worn); only Stoneskin: Works as Ancestral Armor (bearer, while worn); property only in Ancestral Armor: reusable; range: Other, Self vs Other | “The effects” vs “Bearer gains 2 points”; “a” vs nothing; “Ball , projectile weapon , or melee weapon which just struck armor worn by the player are ignored , even if the object would not otherwise affect the armor” vs “Armor affected as per Ancestral Armor”; and 1 more |

## [Astral Intervention](../profiles/astral-intervention.md)

A player within 20' (or the caster) becomes Insubstantial for 30 seconds; if self-cast, the caster may exit at any time.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Shadow Step](../profiles/shadow-step.md) | Assassin 1st, Scout 3rd | Makes Insubstantial: 30 s, if cast-on-self vs until removed; only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); property only in Shadow Step: castable-while-moving; school: Command vs Sorcery; range: 20' vs Self | “Target player” vs “Caster”; “for 30 seconds” vs nothing; “If” vs “THIS may be”; and 1 more |
| overlap | [Lost](../profiles/lost.md) | Bard 5th | Makes Insubstantial: 30 s, if cast-on-self vs until arrival, if cast-on-self; only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); ends when only in Lost: insubstantial-ends, on-arrival; property only in Lost: forced-movement | “for 30 seconds” vs “, must move directly to their base . Upon arrival , they must immediately end the effect as per Insubstantial”; nothing vs “the Insubstantial State is ended before reaching the base , the rest of the effect is ended as well . If THIS is”; nothing vs “This is a Forced Movement effect .” |
| overlap | [Teleport](../profiles/teleport.md) | Assassin 5th, Druid 4th, Healer 4th, Wizard 2nd | Makes Insubstantial: 30 s, if cast-on-self vs until arrival, if cast-on-self; only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; ends when only in Teleport: insubstantial-ends, on-arrival; property only in Teleport: forced-movement; school: Command vs Sorcery; range: 20' vs Self, Touch | nothing vs “willing”; “for 30 seconds” vs “and moves directly to a chosen location chosen by the caster at the time of casting . This must be a fixed location (not relative to a player or to a moveable object) . Upon arrival , they must immediately end the effect as per Insubstantial”; nothing vs “the player's Insubstantial State is removed before they have reached their destination , the effects of THIS end . If THIS is”; and 1 more |

## [Banish](../profiles/banish.md)

An Insubstantial player within 20' must return to base, their Insubstantial State replaced by Banish's, ending it on arrival.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Lost](../profiles/lost.md) | Bard 5th | only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Makes Insubstantial (caster, until arrival, if cast-on-self); requirement only in Banish: target-insubstantial; school: Spirit vs Command | nothing vs “player becomes”; “player” vs “,”; “return” vs “move directly”; and 1 more |
| overlap | [Summon Dead](../profiles/summon-dead.md) | Healer 2nd | only Banish: Sends to base (target, until arrival, if cast-on-other); only Banish: Sends to base (caster, until arrival, if cast-on-self); only Summon Dead: Brings to the caster (dead-target, until arrival); only Summon Dead: Moves where the player died (dead-target, instant); requirement only in Banish: target-insubstantial; requirement only in Summon Dead: target-dead, target-not-moved-5ft, target-willing; ends when only in Banish: exit-at-will, insubstantial-ends; property only in Banish: forced-movement; range: 20' vs 50' | “Insubstantial” vs “willing dead”; “return” vs “go directly”; “their base” vs “the caster”; and 7 more |
| overlap | [Teleport](../profiles/teleport.md) | Assassin 5th, Druid 4th, Healer 4th, Wizard 2nd | only Banish: Sends to base (target, until arrival, if cast-on-other); only Banish: Sends to base (caster, until arrival, if cast-on-self); only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Makes Insubstantial (caster, until arrival, if cast-on-self); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Banish: target-insubstantial; requirement only in Teleport: target-willing; school: Spirit vs Sorcery; range: 20' vs Self, Touch | nothing vs “willing player becomes”; nothing vs “and moves directly to a chosen location chosen by the caster at the time of casting . This must be a fixed location (not relative to a”; “must return” vs “or”; and 6 more |

## [Blessed Aura](../profiles/blessed-aura.md)

Bearer resists the next source that would wound, kill, apply a State or otherwise harm them or their carried equipment; not their own effects.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Blessing Against Harm](../profiles/blessing-against-harm.md) | Healer 4th, Wizard 5th | only Blessed Aura: Grants Resistance (bearer, until used); only Blessing Against Harm: Grants Resistance (bearer, until used); range: Other vs Other, Self | “negatively affect them or their carried equipment” vs “other negative effect” |

## [Blessing Against Harm](../profiles/blessing-against-harm.md)

Bearer is Resistant to the next source that would wound, kill, apply a State or cause another negative effect; not their own effects.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Blessed Aura](../profiles/blessed-aura.md) | Healer 5th | only Blessing Against Harm: Grants Resistance (bearer, until used); only Blessed Aura: Grants Resistance (bearer, until used); range: Other, Self vs Other | “other negative effect” vs “negatively affect them or their carried equipment” |

## [Blessing Against Wounds](../profiles/blessing-against-wounds.md)

Bearer is Resistant to wounds (the next wound); outside the Enchantment limit; not with other (m) Protection Enchantments.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Blood and Thunder](../profiles/blood-and-thunder.md) | Barbarian 6th | only Blessing Against Wounds: Grants Resistance (bearer, until used); only Blood and Thunder: Grants Blessing Against Wounds (caster, until used); requirement only in Blood and Thunder: immediately-after-kill; restriction only in Blessing Against Wounds: no-other-protection-enchantments; ends when only in Blessing Against Wounds: activates-once; property only in Blessing Against Wounds: exempt-from-enchantment-limit; property only in Blood and Thunder: kill-trigger, materials-required, uses-strips; delivery: enchantment vs verbal; school: Protection vs Spirit; range: Other vs Self | “Bearer is resistant to wounds . Does not count towards the bearer's Enchantment limit . May not be worn with any other Enchantments from the Protection School unless the other Enchantment is” vs “Caster gains Blessing Against Wounds”; nothing vs “Kill Trigger . Caster must still wear a white strip to denote Blessing Against Wounds .” |
| is given by | [Medium](../profiles/medium.md) | Monk 6th | only Blessing Against Wounds: Grants Resistance (bearer, until used); only Medium: Grants Blessing Against Wounds (bearer, permanent); only Medium: Grants Sever Spirit (bearer, permanent); only Medium: Grants Swift (bearer, permanent); only Medium: Changes how often abilities can be used (bearer, permanent); only Medium: May not wear armor (bearer, permanent); only Medium: May not wield great weapons (bearer, permanent); restriction only in Blessing Against Wounds: no-other-protection-enchantments; ends when only in Blessing Against Wounds: activates-once; property only in Blessing Against Wounds: exempt-from-enchantment-limit; delivery: enchantment vs archetype; school: Protection vs Neutral; range: Other vs - | “Bearer is resistant to wounds” vs “Gain Blessing Against Wounds (Touch) 1/Life (ex) , Sever Spirit 1/Life Charge x3 (ex) , and Swift 2/Life (ex)”; “Does not count towards” vs “Abilities in”; “bearer's Enchantment limit” vs “Spirit school become Charge x3”; and 1 more |

## [Dispel Magic](../profiles/dispel-magic.md)

Removes all Enchantments from a target within 20', regardless of Traits, States, Immunities or Enchantments, except Sleight of Mind; not on Invulnerable players.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Naturalize Magic](../profiles/naturalize-magic.md) | Druid 6th | only Dispel Magic: Removes Enchantments (target, instant); only Naturalize Magic: Casts Dispel Magic from strips (bearer, while worn); only Naturalize Magic: Uses up a strip (bearer, instant); requirement only in Dispel Magic: target-not-invulnerable; ends when only in Naturalize Magic: last-strip; property only in Dispel Magic: bypass-enchantments, bypass-immunities, bypass-ongoing-effects, bypass-states, bypass-traits; property only in Naturalize Magic: materials-required, uses-strips; delivery: verbal vs enchantment; range: 20' vs Self | “All Enchantments on target are” vs “Bearer may cast Dispel Magic (m) by incanting Player thou art dispelled and removing an enchantment strip . Enchantment is removed when the last strip is”; “Will always remove Enchantments if successfully cast on a valid target , regardless of the player's Traits , States , Immunities , Ongoing Effects , or Enchantments (except Sleight of Mind) . Does not affect Invulnerable players .” vs nothing |
| overlap | [Sever Spirit](../profiles/sever-spirit.md) | Healer 2nd, Monk 6th | only Sever Spirit: Curses (dead-target, until respawn); requirement only in Dispel Magic: target-not-invulnerable; requirement only in Sever Spirit: target-dead, target-dead-at-start; school: Sorcery vs Spirit | “All” vs “Target dead player is Cursed . Any”; “target” vs “the player”; “Enchantments” vs “enchantments”; and 2 more |

## [Enlightened Soul](../profiles/enlightened-soul.md)

Bearer is unaffected by Verbal Magical abilities used from beyond Touch, harmful or beneficial; (ex) and Touch-range uses still work.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Song of Interference](../profiles/song-of-interference.md) | Bard 6th | only Enlightened Soul: Unaffected by (bearer, while worn); only Enlightened Soul: Unaffected by (bearer, while worn); only Song of Interference: Works as Enlightened Soul (bearer, while chanting); ends when only in Song of Interference: chant-stops; property only in Song of Interference: chant; range: Other, Self vs Self | nothing vs “As per Enlightened Soul .”; nothing vs “must Chant THIS or sing a song about defeating/resisting the forces of magic . Singing in place of the normal Chant”; “unaffected by Verbal Magical abilities used at” vs “still”; and 2 more |

## [Entangle](../profiles/entangle.md)

Engulfing Magic Ball: the player struck is Stopped for 60 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Hold Person](../profiles/hold-person.md) | Assassin 4th, Scout 4th, Healer 2nd, Wizard 3rd | Stops: 60 s vs 30 s; property only in Entangle: engulfing; delivery: magic-ball vs verbal; school: Subdual vs Command; range: - vs 20' | “Player struck is” vs “Target player becomes”; “60” vs “30”; “Engulfing .” vs nothing |
| does less than | [Lightning Bolt](../profiles/lightning-bolt.md) | Wizard 3rd | only Lightning Bolt: Weapon Destroying (this magic ball) (struck-player, instant); only Lightning Bolt: Armor Breaking (this magic ball) (struck-player, instant); only Lightning Bolt: Inflicts a wound (struck-player, instant); school: Subdual vs Flame | nothing vs “This Magic Ball is Weapon Destroying and Armor Breaking . Player hit receives a wound to that hit location .” |
| same-effects-different-numbers | [Pinning Arrow](../profiles/pinning-arrow.md) | Archer 1st,3rd,5th, Scout 4th, Scout 5th | Stops: 60 s vs 30 s; delivery: magic-ball vs specialty-arrow; school: Subdual vs Sorcery | “Player” vs “A player”; nothing vs “by this arrow”; “60” vs “30” |
| overlap | [Song of Power](../profiles/song-of-power.md) | Bard 4th | only Entangle: Stops (struck-player, 60 s); only Song of Power: Speeds up Charging (friendly-players, while chanting); only Song of Power: Stops (bearer, while chanting); restriction only in Song of Power: players-benefit-once; ends when only in Song of Power: chant-stops, moves-from-start; property only in Entangle: engulfing; property only in Song of Power: chant; delivery: magic-ball vs enchantment; school: Subdual vs Protection; range: - vs Self | “Player struck” vs “Friendly players within 20' of the bearer have their Charge Incantation repetitions divided by 2 , rounded down , to a minimum of 1 . Bearer”; “for 60 seconds” vs nothing; “Engulfing” vs “Bearer must Chant THIS or sing an inspiring song”; and 1 more |

## [Extension](../profiles/extension.md)

Meta-Magic: the next 20' Verbal has its range extended to 50'.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Amplification](../profiles/amplification.md) | Bard 4th | only Extension: Modifies the next ability cast (caster, until used); only Amplification: Grants Extension (bearer, while worn); only Amplification: May not use other sources of ability (bearer, while worn); requirement only in Extension: only-verbals-20ft; restriction only in Amplification: excludes-other-sources; delivery: meta-magic vs enchantment; school: Neutral vs Sorcery; range: - vs Touch | “Verbal becomes 50'” vs “Bearer gains Extension 1/Refresh Charge x3 (m)”; “Only works on Verbals with a range” vs “Other sources”; “20'” vs “Extension may not be utilized while THIS is worn”; and 1 more |

## [Greater Harden](../profiles/greater-harden.md)

Shields and weapons wielded by the bearer are affected as per Harden (both, not one or the other).

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Harden](../profiles/harden.md) | Warrior 1st, Healer 1st | only Greater Harden: Works as Harden (bearer-equipment, while worn); only Greater Harden: Protects equipment (bearer-equipment, while worn); only Harden: Protects equipment (bearer-equipment, while worn); restriction only in Harden: only-one-option; property only in Harden: has-choice; range: Other vs Other, Self | “Shields and” vs “Bearer's wielded”; “wielded” vs “or shield may only be destroyed or damaged”; nothing vs “Magic Balls/Verbals which destroy objects e . g . Fireball or Pyrotechnics . Will only affect either the weapons or the shield of”; and 1 more |
| overlap | [Gift of Earth](../profiles/gift-of-earth.md) | Druid 2nd | only Greater Harden: Protects equipment (bearer-equipment, while worn); only Gift of Earth: Grants Magic Armor (bearer, points 1, while worn) | “Shields” vs “Bearer gains one point of Magic Armor”; “weapons wielded by the bearer are” vs “is” |

## [Greater Heal](../profiles/greater-heal.md)

Heals all wounds on a touched player, even if they are Cursed.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Heal](../profiles/heal.md) | Monk 4th, Scout 2nd,5th, Druid 2nd, Healer 1st, Monk 1st, Scout 1st | Heals wounds: amount all, instant vs amount one, instant; property only in Greater Heal: bypass-cursed | “All wounds are healed” vs “Target player heals a wound”; “Ignores the Cursed State .” vs nothing |
| overlap | [Adrenaline](../profiles/adrenaline.md) | Barbarian 3rd | only Greater Heal: Heals wounds (target, amount all, instant); only Adrenaline: Heals wounds (caster, amount one, instant); requirement only in Adrenaline: immediately-after-kill; property only in Greater Heal: bypass-cursed; property only in Adrenaline: kill-trigger; range: Touch vs Self | “All wounds are healed” vs “Caster heals a wound”; “Ignores the Cursed State” vs “Kill Trigger” |

## [Greater Release](../profiles/greater-release.md)

Removes all States and Ongoing Effects (caster may leave some) from a player within 20', including a dead player.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Release](../profiles/release.md) | Scout 2nd,5th, Bard 1st, Druid 2nd, Healer 1st, Wizard 2nd | only Greater Release: Removes States or Ongoing Effects (target, instant); only Greater Release: Removes States or Ongoing Effects (dead-target, instant); only Greater Release: Removes States or Ongoing Effects (target, instant); only Release: Removes States or Ongoing Effects (target, instant); only Release: Removes States or Ongoing Effects (target, instant); property only in Greater Release: bypass-cursed; range: 20' vs Touch | “All” vs “A single”; “Effects and States are” vs “Effect or State is”; “The caster may choose to leave some States or Effects in place” vs “Casters choice”; and 1 more |
| overlap | [Shake It Off](../profiles/shake-it-off.md) | Warrior 5th | only Greater Release: Removes States or Ongoing Effects (target, instant); only Greater Release: Removes States or Ongoing Effects (dead-target, instant); only Greater Release: Removes States or Ongoing Effects (target, instant); only Shake It Off: Removes States or Ongoing Effects (caster, instant); requirement only in Shake It Off: caster-alive; property only in Greater Release: bypass-cursed; property only in Shake It Off: works-while-suppressed; school: Sorcery vs Spirit; range: 20' vs Self | “All” vs “10 seconds after casting THIS the caster may remove from themselves any number of States or”; “and States are removed from the target . The caster may choose to leave some States or Effects in place” vs “of their choice”; “target Dead players” vs “be cast at any time the caster is alive , even while the caster would otherwise be prevented from casting abilities by Stunned , Suppressed , or similar”; and 4 more |

## [Greater Resurrect](../profiles/greater-resurrect.md)

Returns a willing dead player (within 5' of where they died) to life with wounds healed, regardless of States, removing Cursed; Enchantments kept.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Raise Dead](../profiles/raise-dead.md) | Healer 3rd | only Greater Resurrect: Ends Cursed (dead-target, instant); only Raise Dead: Removes Enchantments (dead-target, instant); only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); property only in Greater Resurrect: bypass-cursed, bypass-states; school: Spirit vs Death | nothing vs “and is Cursed . Target is also Suppressed for 30 seconds . Non-Persistent Enchantments on the player are removed before the player returns to life”; “Works regardless of any States on the target , and removes Cursed if present . Enchantments on the player are retained .” vs nothing |
| does more than | [Resurrect](../profiles/resurrect.md) | Monk 5th, Druid 5th, Healer 3rd | only Greater Resurrect: Ends Cursed (dead-target, instant); only Resurrect: Removes Enchantments (dead-target, instant); property only in Greater Resurrect: bypass-cursed, bypass-states | nothing vs “Non-Persistent Enchantments on the player are removed before the player returns to life .”; “Works regardless of any States on the target , and removes Cursed if present . Enchantments on the player are retained .” vs nothing |
| overlap | [True Grit](../profiles/true-grit.md) | Warrior 3rd | only Greater Resurrect: Returns to life (dead-target, instant); only Greater Resurrect: Heals wounds (dead-target, amount all, instant); only Greater Resurrect: Ends Cursed (dead-target, instant); only True Grit: Returns to life (caster, instant); only True Grit: Heals wounds (caster, amount all, instant); only True Grit: Freezes (caster, 30 s); requirement only in Greater Resurrect: target-dead, target-not-moved-5ft, target-willing; requirement only in True Grit: after-dying; property only in Greater Resurrect: bypass-cursed, bypass-states; range: Other vs Self | “Target willing dead player who has not moved more than 5' from where they died is returned” vs “Caster returns”; “. Any” vs “with their”; “on the player are” vs nothing; and 3 more |

## [Harden](../profiles/harden.md)

Bearer's wielded weapons or shield (one or the other) can only be destroyed or damaged by object-destroying Magic Balls or Verbals.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Gift of Earth](../profiles/gift-of-earth.md) | Druid 2nd | only Harden: Protects equipment (bearer-equipment, while worn); only Gift of Earth: Grants Magic Armor (bearer, points 1, while worn); only Gift of Earth: Works as Harden (bearer, while worn); restriction only in Harden: only-one-option; property only in Harden: has-choice; range: Other, Self vs Other | “Bearer's wielded weapons or shield may only be destroyed or damaged by” vs “Bearer gains one point of”; “Balls/Verbals which destroy objects e” vs “Armor and is affected as per Harden”; “g . Fireball or Pyrotechnics . Will only affect either the weapons or the shield of the bearer , not both .” vs nothing |
| does less than | [Greater Harden](../profiles/greater-harden.md) | Healer 3rd, Warrior 6th | only Harden: Protects equipment (bearer-equipment, while worn); only Greater Harden: Works as Harden (bearer-equipment, while worn); only Greater Harden: Protects equipment (bearer-equipment, while worn); restriction only in Harden: only-one-option; property only in Harden: has-choice; range: Other, Self vs Other | “Bearer's” vs “Shields and weapons”; “weapons or shield may only be destroyed or damaged” vs nothing; “Magic Balls/Verbals which destroy objects e . g . Fireball or Pyrotechnics . Will only affect either the weapons or the shield of” vs nothing; and 1 more |
| does less than | [Sacred Blades](../profiles/sacred-blades.md) | Paladin 6th | only Harden: Protects equipment (bearer-equipment, while worn); only Sacred Blades: Works as Harden (bearer-equipment, while worn); only Sacred Blades: Weapons ignore protections (bearer, while worn); only Sacred Blades: Weapons ignore protections (bearer, while worn); restriction only in Harden: only-one-option; property only in Harden: has-choice; property only in Sacred Blades: bypass-magic-armor, bypass-resistances; school: Protection vs Sorcery; range: Other, Self vs Self | “or shield may only be destroyed or damaged” vs “are affected as per Harden . Bearer's wielded melee weapons and any special effects delivered”; “Magic Balls/Verbals which destroy objects e” vs “them ignore magic armor and resistances that prevent wounds”; “g . Fireball or Pyrotechnics . Will only affect either the weapons or the shield of the bearer , not both .” vs nothing |

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

## [Hold Person](../profiles/hold-person.md)

A target within 20' is Stopped for 30 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Entangle](../profiles/entangle.md) | Druid 1st, Healer 2nd, Wizard 2nd | Stops: 30 s vs 60 s; property only in Entangle: engulfing; delivery: verbal vs magic-ball; school: Command vs Subdual; range: 20' vs - | “Target player becomes” vs “Player struck is”; “30” vs “60”; nothing vs “Engulfing .” |
| does less than | [Lightning Bolt](../profiles/lightning-bolt.md) | Wizard 3rd | Stops: 30 s vs 60 s; only Lightning Bolt: Weapon Destroying (this magic ball) (struck-player, instant); only Lightning Bolt: Armor Breaking (this magic ball) (struck-player, instant); only Lightning Bolt: Inflicts a wound (struck-player, instant); property only in Lightning Bolt: engulfing; delivery: verbal vs magic-ball; school: Command vs Flame; range: 20' vs - | “Target player becomes” vs “This Magic Ball is Weapon Destroying and Armor Breaking . Player hit receives a wound to that hit location . Player struck is”; “30” vs “60”; nothing vs “Engulfing .” |
| same-effects | [Pinning Arrow](../profiles/pinning-arrow.md) | Archer 1st,3rd,5th, Scout 4th, Scout 5th | property only in Pinning Arrow: engulfing; delivery: verbal vs specialty-arrow; school: Command vs Sorcery; range: 20' vs - | “Target” vs “A”; “becomes” vs “struck by this arrow is”; nothing vs “Engulfing .” |
| is given by | [Snaring Vines](../profiles/snaring-vines.md) | Druid 6th | only Hold Person: Stops (target, 30 s); only Snaring Vines: Casts Hold Person from strips (bearer, while worn); only Snaring Vines: Uses up a strip (bearer, instant); ends when only in Snaring Vines: last-strip; property only in Snaring Vines: materials-required, uses-strips; delivery: verbal vs enchantment; range: 20' vs Self | “Target player becomes Stopped for 30 seconds” vs “Bearer may cast Hold Person (m) by incanting Player stop at my command and removing an enchantment strip”; nothing vs “Enchantment is removed when the last strip is removed .” |
| overlap | [Song of Power](../profiles/song-of-power.md) | Bard 4th | only Hold Person: Stops (target, 30 s); only Song of Power: Speeds up Charging (friendly-players, while chanting); only Song of Power: Stops (bearer, while chanting); restriction only in Song of Power: players-benefit-once; ends when only in Song of Power: chant-stops, moves-from-start; property only in Song of Power: chant; delivery: verbal vs enchantment; school: Command vs Protection; range: 20' vs Self | “Target player becomes” vs “Friendly players within 20' of the bearer have their Charge Incantation repetitions divided by 2 , rounded down , to a minimum of 1 . Bearer is”; “for 30 seconds” vs nothing; nothing vs “Bearer must Chant THIS or sing an inspiring song . Singing in place of the normal Chant is still a Chant and must follow all Chant rules . Players can only benefit from one instance of THIS at a time . THIS ends if the bearer moves from their starting location .” |

## [Iceball](../profiles/iceball.md)

Engulfing Magic Ball: the player struck is Frozen for 60 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Icy Blast](../profiles/icy-blast.md) | Druid 3rd, Wizard 4th | Freezes: 60 s vs 30 s; property only in Iceball: engulfing; delivery: magic-ball vs verbal; school: Subdual vs Sorcery; range: - vs 20' | “Player struck is” vs “Target player becomes”; “60” vs “30”; “Engulfing .” vs nothing |
| overlap | [Force Barrier](../profiles/force-barrier.md) | Wizard 1st | only Iceball: Freezes (struck-player, 60 s); only Force Barrier: Freezes (caster, 10 s); property only in Iceball: engulfing; delivery: magic-ball vs verbal; school: Subdual vs Sorcery; range: - vs Self | “Player struck” vs “Caster”; “60” vs “10”; “Engulfing .” vs nothing |
| overlap | [Stoneform](../profiles/stoneform.md) | Druid 2nd | only Iceball: Freezes (struck-player, 60 s); only Stoneform: Freezes (caster, until removed); ends when only in Stoneform: exit-at-will; property only in Iceball: engulfing; property only in Stoneform: must-declare; delivery: magic-ball vs verbal; school: Subdual vs Protection; range: - vs Self | “Player struck” vs “Caster”; “for 60 seconds” vs nothing; “Engulfing” vs “May end this State at any time by saying The earth release me x2” |

## [Imbue](../profiles/imbue.md)

Bearer chooses shield or weapons: wielded equipment of that type cannot be destroyed or damaged and ignores Engulfing effects.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Guardian](../profiles/guardian.md) | Paladin 6th | only Imbue: Protects equipment (bearer-equipment, while worn); only Imbue: Ignores Engulfing effects (bearer-equipment, while worn); only Imbue: Ignores Engulfing effects (bearer-equipment, while worn); only Imbue: Protects equipment (bearer-equipment, while worn); only Guardian: Grants Imbue (bearer, permanent); only Guardian: Grants Martyr (bearer, permanent); only Guardian: Removes Protection from Evil (bearer, permanent); only Guardian: Removes Protection from Magic (bearer, permanent); only Guardian: Changes Imbue (bearer, permanent); restriction only in Imbue: only-one-option; restriction only in Guardian: one-active-per-caster; property only in Imbue: has-choice; delivery: enchantment vs archetype; school: Protection vs Neutral; range: Other vs - | “Bearer chooses either shield or weapons” vs “Gain Imbue (Touch) 1/Life (m) and Martyr (Other) 2/Life Charge x3 (ex)”; “Wielded equipment” vs “Lose all instances”; “the chosen type cannot be destroyed nor damaged” vs “Protection from Evil and Protection from Magic”; and 2 more |

## [Innate](../profiles/innate.md)

Meta-Magic: instantly Charges a single ability, named aloud, without the Charge Incantation.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects | [Momentum](../profiles/momentum.md) | Archer 6th, Barbarian 6th, Warrior 6th | requirement only in Momentum: immediately-after-kill; property only in Momentum: kill-trigger; delivery: meta-magic vs verbal; school: Neutral vs Sorcery; range: - vs Self | nothing vs “Kill Trigger” |
| overlap | [Confidence](../profiles/confidence.md) | Bard 1st | only Innate: Instantly Charges an ability (caster, instant); only Confidence: Instantly Charges an ability (target, instant); requirement only in Confidence: no-enemy-within-20ft; property only in Innate: must-declare; delivery: meta-magic vs verbal; school: Neutral vs Sorcery; range: - vs Other | “May be used to” vs “Target player may”; “by stating its name” vs nothing; nothing vs “May not be used within 20' of a living enemy .” |

## [Mass Healing](../profiles/mass-healing.md)

Self Enchantment with five strips: caster may Heal (m) a player at Touch by declaring "I grant thee healing" and removing a strip.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Battlefield Triage](../profiles/battlefield-triage.md) | Bard 3rd | only Mass Healing: Casts by declaration (bearer, while worn); property only in Mass Healing: castable-while-moving, declaration-not-incantation, must-declare, works-while-suppressed; range: Self vs Touch | “Caster” vs “Bearer”; nothing vs “cast”; “a player at Touch” vs nothing; and 2 more |
| gives its user | [Heal](../profiles/heal.md) | Monk 4th, Scout 2nd,5th, Druid 2nd, Healer 1st, Monk 1st, Scout 1st | only Mass Healing: Casts Heal from strips (bearer, while worn); only Mass Healing: Casts by declaration (bearer, while worn); only Mass Healing: Uses up a strip (bearer, instant); only Heal: Heals wounds (target, amount one, instant); ends when only in Mass Healing: last-strip; property only in Mass Healing: castable-while-moving, declaration-not-incantation, materials-required, must-declare, uses-strips, works-while-suppressed; delivery: enchantment vs verbal; range: Self vs Touch | “Caster may Heal (m)” vs “Target player heals”; “player at Touch by declaring I grant thee healing and removing an enchantment strip” vs “wound”; “Enchantment is removed when the last strip is removed . The declaration is not an incantation , and so is not stopped by being Suppressed , and may be used while moving , etc .” vs nothing |

## [Mend](../profiles/mend.md)

By touch, repairs a destroyed or damaged item, or repairs one point of armor in one location.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Greater Mend](../profiles/greater-mend.md) | Druid 3rd, Wizard 3rd, Archer 6th | Repairs armor: amount one-point-one-location, instant vs amount all-points-one-location, instant | “Destroyed or damaged item is repaired , or one point of” vs “Will restore all”; nothing vs “points”; “is repaired” vs “, repair one armor point in each location , or repair a damaged or broken item” |
| is given by | [Apex](../profiles/apex.md) | Scout 6th | only Mend: Repairs equipment (target-equipment, instant); only Mend: Repairs armor (hit-location, amount one-point-one-location, instant); only Apex: Grants Mend (bearer, permanent); only Apex: Grants Sleight of Mind (bearer, permanent); only Apex: Removes Evolution (bearer, permanent); only Apex: Removes Hold Person (bearer, permanent); only Apex: Removes Pinning Arrow (bearer, permanent); property only in Mend: has-choice, targets-equipment, targets-player-affects-equipment; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Touch vs - | “Destroyed or damaged item is repaired” vs “Gain Mend 1/Life (ex) and Sleight of Mind (Self) 1/Life (ex) . Lose all instances of Evolution”; “or one point of armor in one location is repaired .” vs “Hold Person , and Pinning Arrow” |
| is given by | [Sniper](../profiles/sniper.md) | Archer 6th | only Mend: Repairs equipment (target-equipment, instant); only Mend: Repairs armor (hit-location, amount one-point-one-location, instant); only Sniper: Allows equipment (bearer, permanent); only Sniper: Changes how often abilities can be used (bearer, permanent); only Sniper: Grants Momentum (bearer, permanent); only Sniper: Changes Look The Part (bearer, permanent); only Sniper: May not fire normal arrows (bearer, permanent); property only in Mend: has-choice, targets-equipment, targets-player-affects-equipment; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Touch vs - | “Destroyed or damaged item is repaired , or one point” vs “May physically carry any number”; “armor in one location is repaired” vs “Specialty Arrows of each type”; nothing vs “The frequency of each type of Specialty Arrow ability becomes 1 Arrow / Life Charge x3 . Gain Momentum Unlimited (ex) (Ambulant) . Look the Part becomes Mend 1/Life (ex) . May not fire normal arrows .” |
| overlap | [Scavenge](../profiles/scavenge.md) | Warrior 2nd | only Mend: Repairs equipment (target-equipment, instant); only Mend: Repairs armor (hit-location, amount one-point-one-location, instant); only Scavenge: Repairs equipment (bearer-equipment, instant); only Scavenge: Repairs armor (bearer-equipment, amount one-point-one-location, instant); requirement only in Scavenge: immediately-after-kill; property only in Mend: targets-equipment, targets-player-affects-equipment; property only in Scavenge: kill-trigger; range: Touch vs Self | “Destroyed” vs “A destroyed”; nothing vs “carried by the caster”; “location” vs “of the caster's hit locations”; and 1 more |
| overlap | [Word of Mending](../profiles/word-of-mending.md) | Druid 6th, Wizard 6th | Repairs armor: amount one-point-one-location, instant vs amount all-armor, instant; only Mend: Repairs equipment (target-equipment, instant); only Word of Mending: Repairs equipment (target, instant); requirement only in Word of Mending: no-enemy-within-20ft; property only in Mend: has-choice, targets-equipment | “Destroyed or damaged item is repaired , or one point of armor in one location” vs “All equipment carried by target player”; nothing vs “All armor worn by target player is restored to full value . May not be cast within 20' of a living enemy .” |

## [Phoenix Tears](../profiles/phoenix-tears.md)

Instead of dying, bearer heals all wounds and is Frozen 30s; then loses Cursed, non-persistent Enchantments and a strip, repairs equipment; +1 Persistent Protection Enchantment.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Juggernaut](../profiles/juggernaut.md) | Warrior 6th | only Phoenix Tears: Prevents death (bearer, while worn); only Phoenix Tears: Heals wounds (bearer, amount all, instant); only Phoenix Tears: Freezes (bearer, 30 s); only Phoenix Tears: Ends Cursed (bearer, instant, if still-enchanted); only Phoenix Tears: Repairs equipment (bearer-equipment, instant, if still-enchanted); only Phoenix Tears: Removes Enchantments (bearer, instant, if still-enchanted); only Phoenix Tears: Uses up a strip (bearer, instant, if still-enchanted); only Phoenix Tears: Allows extra Enchantments (bearer, count 1, while worn); only Phoenix Tears: Makes Enchantments Persistent (bearer, while worn); only Phoenix Tears: Removes Enchantments (bearer, instant); only Juggernaut: Grants Harden Armor (bearer, permanent); only Juggernaut: Grants Phoenix Tears (bearer, permanent); only Juggernaut: Replaces an ability (bearer, permanent); only Juggernaut: Removes Ancestral Armor (bearer, permanent); only Juggernaut: Removes True Grit (bearer, permanent); restriction only in Phoenix Tears: not-with-abilities; ends when only in Phoenix Tears: last-strip; property only in Phoenix Tears: bypass-cursed, has-choice, uses-strips; delivery: enchantment vs archetype; school: Spirit vs Neutral; range: Other vs - | “Bearer does not die as normal” vs “Gain Harden Armor (Self) 1/Life (ex) and Phoenix Tears (Self) 3/Refresh (ex) (Swift)”; “When” vs “Replace Harden with Greater Harden (Self) (ex) at”; “bearer would otherwise die they instead remove” vs “same frequency . Lose”; and 3 more |

## [Protection from Magic](../profiles/protection-from-magic.md)

Bearer is unaffected by Magical abilities of every School; when the bearer dies they are Cursed.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Assassinate](../profiles/assassinate.md) | Assassin 1st | only Protection from Magic: Unaffected by (bearer, while worn); only Protection from Magic: Curses (bearer, until respawn); only Assassinate: Curses (dead-target, until respawn); requirement only in Assassinate: immediately-after-kill, target-dead; property only in Assassinate: no-verbal-targeting; delivery: enchantment vs verbal; school: Protection vs Death; range: Other, Touch vs 50' | “Bearer is unaffected by Magical abilities from any school . Upon death the bearer” vs “The target”; “This effect” vs “May only be used immediately upon killing an enemy . THIS targets the killed enemy and”; “interact with other Enchantments worn by the bearer” vs “require verbal targeting” |

## [Protection from Projectiles](../profiles/protection-from-projectiles.md)

Bearer is unaffected by projectiles other than Magic Balls, including their Engulfing effects such as Pinning Arrow; equipment can still be affected.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Song of Deflection](../profiles/song-of-deflection.md) | Bard 4th | Unaffected by: while worn vs while chanting; Ignores Engulfing effects: while worn vs while chanting; ends when only in Song of Deflection: chant-stops; property only in Song of Deflection: chant; range: Other vs Self | nothing vs “Bearer must Chant THIS or sing a song of their acrobatic prowess . Singing in place of the normal Chant is still a Chant and must follow all Chant rules .” |

## [Raise Dead](../profiles/raise-dead.md)

Returns a willing dead player (within 5' of where they died) to life, healed but Cursed, Suppressed 30 seconds, losing non-Persistent Enchantments.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Greater Resurrect](../profiles/greater-resurrect.md) | Paladin 4th, Healer 5th | only Raise Dead: Removes Enchantments (dead-target, instant); only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); only Greater Resurrect: Ends Cursed (dead-target, instant); property only in Greater Resurrect: bypass-cursed, bypass-states; school: Death vs Spirit | “and is Cursed . Target is also Suppressed for 30 seconds . Non-Persistent Enchantments on the player are removed before the player returns to life” vs nothing; nothing vs “Works regardless of any States on the target , and removes Cursed if present . Enchantments on the player are retained .” |
| same plus a drawback or cost | [Resurrect](../profiles/resurrect.md) | Monk 5th, Druid 5th, Healer 3rd | only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); school: Death vs Spirit | “and is Cursed . Target is also Suppressed for 30 seconds” vs nothing |
| is given by | [Undead Minion](../profiles/undead-minion.md) | Healer 5th | only Raise Dead: Removes Enchantments (dead-target, instant); only Raise Dead: Returns to life (dead-target, instant); only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); only Raise Dead: Heals wounds (dead-target, amount all, instant); only Undead Minion: Curses (bearer, while worn); only Undead Minion: Prevents respawning (bearer, while worn); only Undead Minion: Grants Raise Dead (caster-of-enchantment, while worn); only Undead Minion: Changes Raise Dead (caster-of-enchantment, while worn); only Undead Minion: Changes Raise Dead (caster-of-enchantment, while worn); only Undead Minion: Acts as an Alternate Base (caster-of-enchantment, while worn); only Undead Minion: May not use alternate bases (caster-of-enchantment, while worn); requirement only in Raise Dead: target-dead, target-not-moved-5ft, target-willing; restriction only in Undead Minion: bearer-not-alternate-base, caster-may-not-use-alternate-bases, max-active-per-caster; property only in Undead Minion: active-while-dead, persistent; delivery: verbal vs enchantment | “Target willing dead player who has” vs “Bearer is Cursed and cannot Respawn . While the bearer is enchanted , the caster gains Raise Dead (Unlimited) (m) which can only be cast with the bearer as the target , and ignores the requirement for the bearer to have”; “more than 5'” vs nothing; nothing vs “. Bearer may treat the caster as an Alternate Base . This enchantment”; and 6 more |

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

## [Sever Spirit](../profiles/sever-spirit.md)

Curses a dead player within 20' and removes all their Enchantments, regardless of Traits, States, Immunities or Enchantments.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Medium](../profiles/medium.md) | Monk 6th | only Sever Spirit: Curses (dead-target, until respawn); only Sever Spirit: Removes Enchantments (dead-target, instant); only Medium: Grants Blessing Against Wounds (bearer, permanent); only Medium: Grants Sever Spirit (bearer, permanent); only Medium: Grants Swift (bearer, permanent); only Medium: Changes how often abilities can be used (bearer, permanent); only Medium: May not wear armor (bearer, permanent); only Medium: May not wield great weapons (bearer, permanent); requirement only in Sever Spirit: target-dead, target-dead-at-start; property only in Sever Spirit: bypass-enchantments, bypass-immunities, bypass-ongoing-effects, bypass-states, bypass-traits; delivery: verbal vs archetype; school: Spirit vs Neutral; range: 20' vs - | “Target dead player is Cursed” vs “Gain Blessing Against Wounds (Touch) 1/Life (ex) , Sever Spirit 1/Life Charge x3 (ex) , and Swift 2/Life (ex)”; “Any Enchantments on” vs “Abilities in”; “player are removed” vs “Spirit school become Charge x3”; and 2 more |
| overlap | [Assassinate](../profiles/assassinate.md) | Assassin 1st | only Sever Spirit: Removes Enchantments (dead-target, instant); requirement only in Sever Spirit: target-dead-at-start; requirement only in Assassinate: immediately-after-kill; property only in Sever Spirit: bypass-enchantments, bypass-immunities, bypass-ongoing-effects, bypass-states, bypass-traits; property only in Assassinate: no-verbal-targeting; school: Spirit vs Death; range: 20' vs 50' | “Target dead player” vs “The target”; “Any Enchantments on” vs “May only be used immediately upon killing an enemy . THIS targets”; “player are removed” vs “killed enemy and does not require verbal targeting”; and 1 more |
| overlap | [Dispel Magic](../profiles/dispel-magic.md) | Scout 3rd, Druid 3rd, Healer 4th, Wizard 3rd | only Sever Spirit: Curses (dead-target, until respawn); requirement only in Sever Spirit: target-dead, target-dead-at-start; requirement only in Dispel Magic: target-not-invulnerable; school: Spirit vs Sorcery | “Target dead player is Cursed . Any” vs “All”; “the player” vs “target”; “enchantments” vs “Enchantments”; and 2 more |

## [Shove](../profiles/shove.md)

Pushes a player within 20' back 20' in a straight line away from the caster, even if Stopped or Stunned; self-cast picks the direction.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Throw](../profiles/throw.md) | Wizard 3rd | Pushes away: feet 20, until arrival, if cast-on-other vs feet 50, until arrival, if cast-on-other; Pushes away: feet 20, until arrival, if cast-on-self vs feet 50, until arrival, if cast-on-self | “20'” vs “50'” |

## [Steal Life Essence](../profiles/steal-life-essence.md)

Curses a dead, non-Cursed player by Touch; the caster may then heal one wound or instantly Charge an ability.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Void Touched](../profiles/void-touched.md) | Wizard 5th, Anti-Paladin 6th | only Steal Life Essence: Curses (dead-target, until respawn); only Steal Life Essence: Heals wounds (caster, amount one, instant); only Steal Life Essence: Instantly Charges an ability (caster, instant); only Void Touched: Armor Breaking (bearer melee weapons) (bearer, while worn); only Void Touched: Grants Shadow Step (bearer, while worn); only Void Touched: Grants Steal Life Essence (bearer, while worn); only Void Touched: Unaffected by (bearer, while worn); only Void Touched: Curses (bearer, while worn); requirement only in Steal Life Essence: target-dead, target-not-cursed; property only in Steal Life Essence: bypass-enchantments, bypass-immunities, bypass-traits, caster-always-benefits, has-choice, must-declare; delivery: verbal vs enchantment; school: Death vs Sorcery; range: Touch vs Other | “Target dead player” vs “Bearer's wielded melee weapons are Armor Breaking . Bearer gains Shadow Step 1/Refresh Charge x30 (ex) , Steal Life Essence Unlimited (ex) , and is unaffected by Magical abilities from the Sorcery , Spirit , and Death Schools . Bearer”; “Caster may heal a wound or instantly Charge an ability” vs “This effect does not interact with other Enchantments worn by the bearer”; “Does not work on Cursed players . Caster will always benefit if successfully cast on a valid target , regardless of the caster's Traits , States , Immunities , Ongoing Effects , or Enchantments . In order to charge an ability , the name of the ability being charged must still be stated immediately after the incantation .” vs nothing |

## [Stun](../profiles/stun.md)

Stuns a player within 20' for 30 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Abeyance](../profiles/abeyance.md) | Healer 5th | Stuns: 30 s vs 60 s; property only in Abeyance: bypass-armor; delivery: verbal vs magic-ball; school: Sorcery vs Subdual; range: 20' vs - | “Target player” vs “This Magic Ball ignores armor . Player hit”; “30” vs “60” |

## [Summon Dead](../profiles/summon-dead.md)

A willing dead player within 50' must go directly to the caster; where they arrive is treated as where they died.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Banish](../profiles/banish.md) | Monk 2nd, Healer 1st, Wizard 1st | only Summon Dead: Brings to the caster (dead-target, until arrival); only Summon Dead: Moves where the player died (dead-target, instant); only Banish: Sends to base (target, until arrival, if cast-on-other); only Banish: Sends to base (caster, until arrival, if cast-on-self); requirement only in Summon Dead: target-dead, target-not-moved-5ft, target-willing; requirement only in Banish: target-insubstantial; ends when only in Banish: exit-at-will, insubstantial-ends; property only in Banish: forced-movement; range: 50' vs 20' | “willing dead” vs “Insubstantial”; “go directly” vs “return”; nothing vs “their base . Upon arrival , they must immediately end the effect as per Insubstantial . The target's Insubstantial State is replaced with a new Insubstantial State from THIS . If the Insubstantial State is ended before reaching the base , the rest of the effect is ended as well . If THIS is cast on self ,”; and 3 more |

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

## [Undead Minion](../profiles/undead-minion.md)

Bearer is Cursed and cannot respawn; caster gains unlimited Raise Dead on the bearer only; up to three per caster; Persistent.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Raise Dead](../profiles/raise-dead.md) | Healer 3rd | only Undead Minion: Curses (bearer, while worn); only Undead Minion: Prevents respawning (bearer, while worn); only Undead Minion: Grants Raise Dead (caster-of-enchantment, while worn); only Undead Minion: Changes Raise Dead (caster-of-enchantment, while worn); only Undead Minion: Changes Raise Dead (caster-of-enchantment, while worn); only Undead Minion: Acts as an Alternate Base (caster-of-enchantment, while worn); only Undead Minion: May not use alternate bases (caster-of-enchantment, while worn); only Raise Dead: Removes Enchantments (dead-target, instant); only Raise Dead: Returns to life (dead-target, instant); only Raise Dead: Curses (dead-target, until respawn); only Raise Dead: Suppresses (dead-target, 30 s); only Raise Dead: Heals wounds (dead-target, amount all, instant); requirement only in Raise Dead: target-dead, target-not-moved-5ft, target-willing; restriction only in Undead Minion: bearer-not-alternate-base, caster-may-not-use-alternate-bases, max-active-per-caster; property only in Undead Minion: active-while-dead, persistent; delivery: enchantment vs verbal | “Bearer is Cursed and cannot Respawn . While the bearer is enchanted , the caster gains Raise Dead (Unlimited) (m) which can only be cast with the bearer as the target , and ignores the requirement for the bearer to have” vs “Target willing dead player who has”; nothing vs “more than 5'”; nothing vs “is returned to life and is Cursed”; and 5 more |
