---
title: "Monk: duplicate check"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Monk: duplicate check

Every comparable entry on the Monk list against every other ability, spell and trait in the rulebook.

## [Banish](../profiles/banish.md)

An Insubstantial player within 20' must return to base, their Insubstantial State replaced by Banish's, ending it on arrival.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Lost](../profiles/lost.md) | Bard 5th | only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Makes Insubstantial (caster, until arrival, if cast-on-self); requirement only in Banish: target-insubstantial; school: Spirit vs Command | nothing vs “player becomes”; “player” vs “,”; “return” vs “move directly”; and 1 more |
| overlap | [Summon Dead](../profiles/summon-dead.md) | Healer 2nd | only Banish: Sends to base (target, until arrival, if cast-on-other); only Banish: Sends to base (caster, until arrival, if cast-on-self); only Summon Dead: Brings to the caster (dead-target, until arrival); only Summon Dead: Moves where the player died (dead-target, instant); requirement only in Banish: target-insubstantial; requirement only in Summon Dead: target-dead, target-not-moved-5ft, target-willing; ends when only in Banish: exit-at-will, insubstantial-ends; property only in Banish: forced-movement; range: 20' vs 50' | “Insubstantial” vs “willing dead”; “return” vs “go directly”; “their base” vs “the caster”; and 7 more |
| overlap | [Teleport](../profiles/teleport.md) | Assassin 5th, Druid 4th, Healer 4th, Wizard 2nd | only Banish: Sends to base (target, until arrival, if cast-on-other); only Banish: Sends to base (caster, until arrival, if cast-on-self); only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Makes Insubstantial (caster, until arrival, if cast-on-self); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Banish: target-insubstantial; requirement only in Teleport: target-willing; school: Spirit vs Sorcery; range: 20' vs Self, Touch | nothing vs “willing player becomes”; nothing vs “and moves directly to a chosen location chosen by the caster at the time of casting . This must be a fixed location (not relative to a”; “must return” vs “or”; and 6 more |

## [Blessing Against Wounds](../profiles/blessing-against-wounds.md)

Bearer is Resistant to wounds (the next wound); outside the Enchantment limit; not with other (m) Protection Enchantments.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Blood and Thunder](../profiles/blood-and-thunder.md) | Barbarian 6th | only Blessing Against Wounds: Grants Resistance (bearer, until used); only Blood and Thunder: Grants Blessing Against Wounds (caster, until used); requirement only in Blood and Thunder: immediately-after-kill; restriction only in Blessing Against Wounds: no-other-protection-enchantments; ends when only in Blessing Against Wounds: activates-once; property only in Blessing Against Wounds: exempt-from-enchantment-limit; property only in Blood and Thunder: kill-trigger, materials-required, uses-strips; delivery: enchantment vs verbal; school: Protection vs Spirit; range: Other vs Self | “Bearer is resistant to wounds . Does not count towards the bearer's Enchantment limit . May not be worn with any other Enchantments from the Protection School unless the other Enchantment is” vs “Caster gains Blessing Against Wounds”; nothing vs “Kill Trigger . Caster must still wear a white strip to denote Blessing Against Wounds .” |
| is given by | [Medium](../profiles/medium.md) | Monk 6th | only Blessing Against Wounds: Grants Resistance (bearer, until used); only Medium: Grants Blessing Against Wounds (bearer, permanent); only Medium: Grants Sever Spirit (bearer, permanent); only Medium: Grants Swift (bearer, permanent); only Medium: Changes how often abilities can be used (bearer, permanent); only Medium: May not wear armor (bearer, permanent); only Medium: May not wield great weapons (bearer, permanent); restriction only in Blessing Against Wounds: no-other-protection-enchantments; ends when only in Blessing Against Wounds: activates-once; property only in Blessing Against Wounds: exempt-from-enchantment-limit; delivery: enchantment vs archetype; school: Protection vs Neutral; range: Other vs - | “Bearer is resistant to wounds” vs “Gain Blessing Against Wounds (Touch) 1/Life (ex) , Sever Spirit 1/Life Charge x3 (ex) , and Swift 2/Life (ex)”; “Does not count towards” vs “Abilities in”; “bearer's Enchantment limit” vs “Spirit school become Charge x3”; and 1 more |

## [Enlightened Soul](../profiles/enlightened-soul.md)

Bearer is unaffected by Verbal Magical abilities used from beyond Touch, harmful or beneficial; (ex) and Touch-range uses still work.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Song of Interference](../profiles/song-of-interference.md) | Bard 6th | only Enlightened Soul: Unaffected by (bearer, while worn); only Enlightened Soul: Unaffected by (bearer, while worn); only Song of Interference: Works as Enlightened Soul (bearer, while chanting); ends when only in Song of Interference: chant-stops; property only in Song of Interference: chant; range: Other, Self vs Self | nothing vs “As per Enlightened Soul .”; nothing vs “must Chant THIS or sing a song about defeating/resisting the forces of magic . Singing in place of the normal Chant”; “unaffected by Verbal Magical abilities used at” vs “still”; and 2 more |

## [Force Bolt](../profiles/force-bolt.md)

Magic Ball: wounds the hit location; Weapon Destroying and Armor Breaking.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Lightning Bolt](../profiles/lightning-bolt.md) | Wizard 3rd | only Lightning Bolt: Stops (struck-player, 60 s); property only in Lightning Bolt: engulfing; school: Sorcery vs Flame | nothing vs “Player struck is Stopped for 60 seconds . Engulfing .” |
| does less than | [Phase Bolt](../profiles/phase-bolt.md) | Wizard 5th | only Phase Bolt: Phasing (this magic ball) (struck-player, instant) | nothing vs “Phasing ,”; nothing vs “,” |
| is given by | [Mystic](../profiles/mystic.md) | Monk 6th | only Force Bolt: Weapon Destroying (this magic ball) (struck-player, instant); only Force Bolt: Armor Breaking (this magic ball) (struck-player, instant); only Force Bolt: Inflicts a wound (struck-player, instant); only Mystic: Grants Force Bolt (bearer, permanent); only Mystic: Grants Phase Bolt (bearer, permanent); only Mystic: Grants Suppression Bolt (bearer, permanent); only Mystic: May not wield heavy thrown (bearer, permanent); only Mystic: Removes Resurrect (bearer, permanent); delivery: magic-ball vs archetype; school: Sorcery vs Neutral | “This Magic” vs “Gain Force Bolt 3 Balls / Unlimited (m) , Phase Bolt 1”; “is Weapon Destroying” vs “/ Unlimited (m) ,”; “Armor Breaking” vs “Suppression Bolt 2 Balls / Unlimited (m)”; and 2 more |

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

## [Innate](../profiles/innate.md)

Meta-Magic: instantly Charges a single ability, named aloud, without the Charge Incantation.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects | [Momentum](../profiles/momentum.md) | Archer 6th, Barbarian 6th, Warrior 6th | requirement only in Momentum: immediately-after-kill; property only in Momentum: kill-trigger; delivery: meta-magic vs verbal; school: Neutral vs Sorcery; range: - vs Self | nothing vs “Kill Trigger” |
| overlap | [Confidence](../profiles/confidence.md) | Bard 1st | only Innate: Instantly Charges an ability (caster, instant); only Confidence: Instantly Charges an ability (target, instant); requirement only in Confidence: no-enemy-within-20ft; property only in Innate: must-declare; delivery: meta-magic vs verbal; school: Neutral vs Sorcery; range: - vs Other | “May be used to” vs “Target player may”; “by stating its name” vs nothing; nothing vs “May not be used within 20' of a living enemy .” |

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

## [Suppression Bolt](../profiles/suppression-bolt.md)

Engulfing Magic Ball: the player struck is Suppressed (cannot cast abilities or Charge) for 60 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Break Concentration](../profiles/break-concentration.md) | Bard 3rd, Wizard 2nd | Suppresses: 60 s vs 10 s; property only in Suppression Bolt: engulfing; delivery: magic-ball vs verbal; school: Subdual vs Command; range: - vs 20' | “Player struck” vs “Target player”; “60” vs “10”; “Engulfing .” vs nothing |
| same-effects-different-numbers | [Suppress Aura](../profiles/suppress-aura.md) | Bard 4th, Wizard 4th | Suppresses: 60 s vs 30 s; property only in Suppression Bolt: engulfing; delivery: magic-ball vs verbal; school: Subdual vs Command; range: - vs 50' | “Player struck” vs “Target”; “60” vs “30”; “Engulfing .” vs nothing |
| same-effects-different-numbers | [Suppression Arrow](../profiles/suppression-arrow.md) | Archer 4th | Suppresses: 60 s vs 30 s; delivery: magic-ball vs specialty-arrow; school: Subdual vs Sorcery | “Player” vs “A player”; nothing vs “by this arrow”; “60” vs “30” |
| is given by | [Mystic](../profiles/mystic.md) | Monk 6th | only Suppression Bolt: Suppresses (struck-player, 60 s); only Mystic: Grants Force Bolt (bearer, permanent); only Mystic: Grants Phase Bolt (bearer, permanent); only Mystic: Grants Suppression Bolt (bearer, permanent); only Mystic: May not wield heavy thrown (bearer, permanent); only Mystic: Removes Resurrect (bearer, permanent); property only in Suppression Bolt: engulfing; delivery: magic-ball vs archetype; school: Subdual vs Neutral | “Player struck is Suppressed for 60 seconds” vs “Gain Force Bolt 3 Balls / Unlimited (m) , Phase Bolt 1 Ball / Unlimited (m) , and Suppression Bolt 2 Balls / Unlimited (m)”; “Engulfing” vs “May not wield Heavy Thrown”; nothing vs “Lose all instances of Resurrect .” |
| overlap | [Brutal Strike](../profiles/brutal-strike.md) | Anti-Paladin 4th, Barbarian 5th | Suppresses: 60 s vs 30 s; only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Suppression Bolt: engulfing; property only in Brutal Strike: no-verbal-targeting, wound-trigger; delivery: magic-ball vs verbal; school: Subdual vs Death; range: - vs Unlimited | “Player struck” vs “Target player”; nothing vs “Cursed indefinitely . Target player is also”; “60” vs “30”; and 2 more |

## [Swift](../profiles/swift.md)

Meta-Magic: the next Touch, Other, Self or Magic Ball ability needs only one iteration of its incantation (last line if multi-line).

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Medium](../profiles/medium.md) | Monk 6th | only Swift: Modifies the next ability cast (caster, until used); only Medium: Grants Blessing Against Wounds (bearer, permanent); only Medium: Grants Sever Spirit (bearer, permanent); only Medium: Grants Swift (bearer, permanent); only Medium: Changes how often abilities can be used (bearer, permanent); only Medium: May not wear armor (bearer, permanent); only Medium: May not wield great weapons (bearer, permanent); requirement only in Swift: not-on-charge-incantation, only-touch-other-self-or-balls; delivery: meta-magic vs archetype | nothing vs “Gain Blessing Against Wounds (Touch) 1/Life (ex) , Sever Spirit 1/Life Charge x3 (ex) , and Swift 2/Life (ex) .”; “require only a single iteration of” vs “in”; “incantation . For multi-line Incantations use the last line . May only be used on abilities at a range of Touch , Other , Self , or on Magic Balls” vs “Spirit school become Charge x3”; and 1 more |
| is given by | [Silver Tongue](../profiles/silver-tongue.md) | Bard 6th | only Swift: Modifies the next ability cast (caster, until used); only Silver Tongue: Grants Swift (bearer, while worn); only Silver Tongue: May not use other sources of ability (bearer, while worn); requirement only in Swift: not-on-charge-incantation, only-touch-other-self-or-balls; restriction only in Silver Tongue: excludes-other-sources; delivery: meta-magic vs enchantment; school: Neutral vs Sorcery; range: - vs Touch | “Abilities require only a single iteration” vs “Bearer gains Swift 1/Refresh Charge x3 (m) . Other sources”; “the incantation . For multi-line Incantations use the last line . May only be used on abilities at a range of Touch , Other , Self , or on Magic Balls . May” vs “Swift may”; “used on the Charge Incantation” vs “utilized while THIS is worn”; and 1 more |
