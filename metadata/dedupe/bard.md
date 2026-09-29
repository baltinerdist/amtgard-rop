---
title: "Bard: duplicate check"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Bard: duplicate check

Every comparable entry on the Bard list against every other ability, spell and trait in the rulebook.

## [Amplification](../profiles/amplification.md)

Bearer gains Extension 1/Refresh Charge x3 (m) without using purchased Extension; other sources of Extension cannot be used while worn.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Extension](../profiles/extension.md) | Bard 3rd, Druid 3rd, Healer 3rd, Wizard 3rd | only Amplification: Grants Extension (bearer, while worn); only Amplification: May not use other sources of ability (bearer, while worn); only Extension: Modifies the next ability cast (caster, until used); requirement only in Extension: only-verbals-20ft; restriction only in Amplification: excludes-other-sources; delivery: enchantment vs meta-magic; school: Sorcery vs Neutral; range: Touch vs - | “Bearer gains Extension 1/Refresh Charge x3 (m)” vs “Verbal becomes 50'”; “Other sources” vs “Only works on Verbals with a range”; “Extension may not be utilized while THIS is worn” vs “20'”; and 1 more |

## [Awe](../profiles/awe.md)

For 30 seconds a target within 20' may not attack or cast Magic at the caster or their equipment, and must stay 20' away.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Terror](../profiles/terror.md) | Anti-Paladin 5th, Bard 4th, Anti-Paladin 1st | Must keep away: feet 20, 30 s vs feet 50, 30 s; school: Command vs Death | “20'” vs “50'” |

## [Battlefield Triage](../profiles/battlefield-triage.md)

Touch Enchantment with three strips: bearer may cast Heal (m) by incanting "Thou art made whole" and removing a strip; removed with the last strip.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Mass Healing](../profiles/mass-healing.md) | Healer 6th | only Mass Healing: Casts by declaration (bearer, while worn); property only in Mass Healing: castable-while-moving, declaration-not-incantation, must-declare, works-while-suppressed; range: Touch vs Self | “Bearer” vs “Caster”; “cast” vs nothing; nothing vs “a player at Touch”; and 2 more |
| gives its user | [Heal](../profiles/heal.md) | Monk 4th, Scout 2nd,5th, Druid 2nd, Healer 1st, Monk 1st, Scout 1st | only Battlefield Triage: Casts Heal from strips (bearer, while worn); only Battlefield Triage: Uses up a strip (bearer, instant); only Heal: Heals wounds (target, amount one, instant); ends when only in Battlefield Triage: last-strip; property only in Battlefield Triage: materials-required, uses-strips; delivery: enchantment vs verbal | “Bearer may cast Heal (m) by incanting Thou art made whole and removing an enchantment strip” vs “Target player heals a wound”; “Enchantment is removed when the last strip is removed .” vs nothing |

## [Break Concentration](../profiles/break-concentration.md)

A target within 20' is Suppressed for 10 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Suppress Aura](../profiles/suppress-aura.md) | Bard 4th, Wizard 4th | Suppresses: 10 s vs 30 s; range: 20' vs 50' | “player” vs nothing; “10” vs “30” |
| same-effects-different-numbers | [Suppression Arrow](../profiles/suppression-arrow.md) | Archer 4th | Suppresses: 10 s vs 30 s; property only in Suppression Arrow: engulfing; delivery: verbal vs specialty-arrow; school: Command vs Sorcery; range: 20' vs - | “Target” vs “A”; nothing vs “struck by this arrow”; “10” vs “30”; and 1 more |
| same-effects-different-numbers | [Suppression Bolt](../profiles/suppression-bolt.md) | Wizard 2nd, Monk 6th | Suppresses: 10 s vs 60 s; property only in Suppression Bolt: engulfing; delivery: verbal vs magic-ball; school: Command vs Subdual; range: 20' vs - | “Target player” vs “Player struck”; “10” vs “60”; nothing vs “Engulfing .” |
| is given by | [Discordia](../profiles/discordia.md) | Bard 5th | only Break Concentration: Suppresses (target, 10 s); only Discordia: Casts Break Concentration from strips (bearer, while worn); only Discordia: Uses up a strip (bearer, instant); ends when only in Discordia: last-strip; property only in Discordia: materials-required, uses-strips; delivery: verbal vs enchantment; range: 20' vs Self | “Target player” vs “Bearer may cast Break Concentration (m) by incanting Player thou art suppressed and removing an enchantment strip . Enchantment”; “Suppressed for 10 seconds” vs “removed when the last strip is removed” |
| overlap | [Brutal Strike](../profiles/brutal-strike.md) | Anti-Paladin 4th, Barbarian 5th | Suppresses: 10 s vs 30 s; only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; school: Command vs Death; range: 20' vs Unlimited | nothing vs “Cursed indefinitely . Target player is also”; “10” vs “30”; nothing vs “Wound Trigger . THIS targets the wounded or dead player and does not require verbal targeting .” |

## [Confidence](../profiles/confidence.md)

Another player may instantly Charge one ability; cannot be used within 20' of a living enemy.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Innate](../profiles/innate.md) | Monk 6th, Bard 2nd, Druid 2nd, Healer 2nd, Wizard 2nd | only Confidence: Instantly Charges an ability (target, instant); only Innate: Instantly Charges an ability (caster, instant); requirement only in Confidence: no-enemy-within-20ft; property only in Innate: must-declare; delivery: verbal vs meta-magic; school: Sorcery vs Neutral; range: Other vs - | “Target player may” vs “May be used to”; nothing vs “by stating its name”; “May not be used within 20' of a living enemy .” vs nothing |
| overlap | [Momentum](../profiles/momentum.md) | Archer 6th, Barbarian 6th, Warrior 6th | only Confidence: Instantly Charges an ability (target, instant); only Momentum: Instantly Charges an ability (caster, instant); requirement only in Confidence: no-enemy-within-20ft; requirement only in Momentum: immediately-after-kill; property only in Momentum: kill-trigger, must-declare; range: Other vs Self | “Target player may” vs “May be used to”; nothing vs “by stating its name”; “May not be used within 20' of a living enemy .” vs “Kill Trigger” |

## [Discordia](../profiles/discordia.md)

Self Enchantment with five strips: bearer may cast Break Concentration (m) by incanting and removing a strip; removed with the last strip.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Break Concentration](../profiles/break-concentration.md) | Bard 3rd, Wizard 2nd | only Discordia: Casts Break Concentration from strips (bearer, while worn); only Discordia: Uses up a strip (bearer, instant); only Break Concentration: Suppresses (target, 10 s); ends when only in Discordia: last-strip; property only in Discordia: materials-required, uses-strips; delivery: enchantment vs verbal; range: Self vs 20' | “Bearer may cast Break Concentration (m) by incanting Player thou art suppressed and removing an enchantment strip” vs “Target player is Suppressed for 10 seconds”; “Enchantment is removed when the last strip is removed .” vs nothing |

## [Empower](../profiles/empower.md)

Another player regains one use of an expended per-life ability, up to its maximum; not Empower, Confidence or Restoration.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Restoration](../profiles/restoration.md) | Bard 4th | Restores used abilities: amount one, instant vs amount all, instant | “regains one use” vs “has all uses”; “any” vs “their”; “ability they have expended” vs “abilities restored”; and 3 more |

## [Extension](../profiles/extension.md)

Meta-Magic: the next 20' Verbal has its range extended to 50'.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Amplification](../profiles/amplification.md) | Bard 4th | only Extension: Modifies the next ability cast (caster, until used); only Amplification: Grants Extension (bearer, while worn); only Amplification: May not use other sources of ability (bearer, while worn); requirement only in Extension: only-verbals-20ft; restriction only in Amplification: excludes-other-sources; delivery: meta-magic vs enchantment; school: Neutral vs Sorcery; range: - vs Touch | “Verbal becomes 50'” vs “Bearer gains Extension 1/Refresh Charge x3 (m)”; “Only works on Verbals with a range” vs “Other sources”; “20'” vs “Extension may not be utilized while THIS is worn”; and 1 more |

## [Greater Release](../profiles/greater-release.md)

Removes all States and Ongoing Effects (caster may leave some) from a player within 20', including a dead player.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Release](../profiles/release.md) | Scout 2nd,5th, Bard 1st, Druid 2nd, Healer 1st, Wizard 2nd | only Greater Release: Removes States or Ongoing Effects (target, instant); only Greater Release: Removes States or Ongoing Effects (dead-target, instant); only Greater Release: Removes States or Ongoing Effects (target, instant); only Release: Removes States or Ongoing Effects (target, instant); only Release: Removes States or Ongoing Effects (target, instant); property only in Greater Release: bypass-cursed; range: 20' vs Touch | “All” vs “A single”; “Effects and States are” vs “Effect or State is”; “The caster may choose to leave some States or Effects in place” vs “Casters choice”; and 1 more |
| overlap | [Shake It Off](../profiles/shake-it-off.md) | Warrior 5th | only Greater Release: Removes States or Ongoing Effects (target, instant); only Greater Release: Removes States or Ongoing Effects (dead-target, instant); only Greater Release: Removes States or Ongoing Effects (target, instant); only Shake It Off: Removes States or Ongoing Effects (caster, instant); requirement only in Shake It Off: caster-alive; property only in Greater Release: bypass-cursed; property only in Shake It Off: works-while-suppressed; school: Sorcery vs Spirit; range: 20' vs Self | “All” vs “10 seconds after casting THIS the caster may remove from themselves any number of States or”; “and States are removed from the target . The caster may choose to leave some States or Effects in place” vs “of their choice”; “target Dead players” vs “be cast at any time the caster is alive , even while the caster would otherwise be prevented from casting abilities by Stunned , Suppressed , or similar”; and 4 more |

## [Innate](../profiles/innate.md)

Meta-Magic: instantly Charges a single ability, named aloud, without the Charge Incantation.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects | [Momentum](../profiles/momentum.md) | Archer 6th, Barbarian 6th, Warrior 6th | requirement only in Momentum: immediately-after-kill; property only in Momentum: kill-trigger; delivery: meta-magic vs verbal; school: Neutral vs Sorcery; range: - vs Self | nothing vs “Kill Trigger” |
| overlap | [Confidence](../profiles/confidence.md) | Bard 1st | only Innate: Instantly Charges an ability (caster, instant); only Confidence: Instantly Charges an ability (target, instant); requirement only in Confidence: no-enemy-within-20ft; property only in Innate: must-declare; delivery: meta-magic vs verbal; school: Neutral vs Sorcery; range: - vs Other | “May be used to” vs “Target player may”; “by stating its name” vs nothing; nothing vs “May not be used within 20' of a living enemy .” |

## [Lost](../profiles/lost.md)

Target within 20' becomes Insubstantial and must go directly to their base, ending the State on arrival; a Forced Movement effect.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Banish](../profiles/banish.md) | Monk 2nd, Healer 1st, Wizard 1st | only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Makes Insubstantial (caster, until arrival, if cast-on-self); requirement only in Banish: target-insubstantial; school: Command vs Spirit | nothing vs “Insubstantial”; “becomes Insubstantial ,” vs nothing; “move directly” vs “return”; and 1 more |
| overlap | [Teleport](../profiles/teleport.md) | Assassin 5th, Druid 4th, Healer 4th, Wizard 2nd | only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); only Teleport: Makes Insubstantial (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (target, until arrival, if cast-on-other); only Teleport: Moves to a chosen location (caster, until arrival, if cast-on-self); requirement only in Teleport: target-willing; school: Command vs Sorcery; range: 20' vs Self, Touch | nothing vs “willing”; “, must move” vs “and moves”; “their base” vs “a chosen location chosen by the caster at the time of casting . This must be a fixed location (not relative to a player or to a moveable object)”; and 5 more |
| overlap | [Astral Intervention](../profiles/astral-intervention.md) | Healer 3rd, Wizard 2nd | Makes Insubstantial: until arrival, if cast-on-self vs 30 s, if cast-on-self; only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); only Astral Intervention: Makes Insubstantial (target, 30 s, if cast-on-other); ends when only in Lost: insubstantial-ends, on-arrival; property only in Lost: forced-movement | “, must move directly to their base . Upon arrival , they must immediately end the effect as per Insubstantial” vs “for 30 seconds”; “the Insubstantial State is ended before reaching the base , the rest of the effect is ended as well . If THIS is” vs nothing; “This is a Forced Movement effect .” vs nothing |
| overlap | [Shadow Step](../profiles/shadow-step.md) | Assassin 1st, Scout 3rd | Makes Insubstantial: until arrival, if cast-on-self vs until removed; only Lost: Makes Insubstantial (target, until arrival, if cast-on-other); only Lost: Sends to base (target, until arrival, if cast-on-other); only Lost: Sends to base (caster, until arrival, if cast-on-self); ends when only in Lost: insubstantial-ends, on-arrival; property only in Lost: forced-movement; property only in Shadow Step: castable-while-moving; school: Command vs Sorcery; range: 20' vs Self | “Target player” vs “Caster”; “, must move directly to their base” vs nothing; “Upon arrival , they must immediately end the effect as per Insubstantial” vs “THIS may be cast while moving”; and 2 more |

## [Mend](../profiles/mend.md)

By touch, repairs a destroyed or damaged item, or repairs one point of armor in one location.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Greater Mend](../profiles/greater-mend.md) | Druid 3rd, Wizard 3rd, Archer 6th | Repairs armor: amount one-point-one-location, instant vs amount all-points-one-location, instant | “Destroyed or damaged item is repaired , or one point of” vs “Will restore all”; nothing vs “points”; “is repaired” vs “, repair one armor point in each location , or repair a damaged or broken item” |
| is given by | [Apex](../profiles/apex.md) | Scout 6th | only Mend: Repairs equipment (target-equipment, instant); only Mend: Repairs armor (hit-location, amount one-point-one-location, instant); only Apex: Grants Mend (bearer, permanent); only Apex: Grants Sleight of Mind (bearer, permanent); only Apex: Removes Evolution (bearer, permanent); only Apex: Removes Hold Person (bearer, permanent); only Apex: Removes Pinning Arrow (bearer, permanent); property only in Mend: has-choice, targets-equipment, targets-player-affects-equipment; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Touch vs - | “Destroyed or damaged item is repaired” vs “Gain Mend 1/Life (ex) and Sleight of Mind (Self) 1/Life (ex) . Lose all instances of Evolution”; “or one point of armor in one location is repaired .” vs “Hold Person , and Pinning Arrow” |
| is given by | [Sniper](../profiles/sniper.md) | Archer 6th | only Mend: Repairs equipment (target-equipment, instant); only Mend: Repairs armor (hit-location, amount one-point-one-location, instant); only Sniper: Allows equipment (bearer, permanent); only Sniper: Changes how often abilities can be used (bearer, permanent); only Sniper: Grants Momentum (bearer, permanent); only Sniper: Changes Look The Part (bearer, permanent); only Sniper: May not fire normal arrows (bearer, permanent); property only in Mend: has-choice, targets-equipment, targets-player-affects-equipment; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Touch vs - | “Destroyed or damaged item is repaired , or one point” vs “May physically carry any number”; “armor in one location is repaired” vs “Specialty Arrows of each type”; nothing vs “The frequency of each type of Specialty Arrow ability becomes 1 Arrow / Life Charge x3 . Gain Momentum Unlimited (ex) (Ambulant) . Look the Part becomes Mend 1/Life (ex) . May not fire normal arrows .” |
| overlap | [Scavenge](../profiles/scavenge.md) | Warrior 2nd | only Mend: Repairs equipment (target-equipment, instant); only Mend: Repairs armor (hit-location, amount one-point-one-location, instant); only Scavenge: Repairs equipment (bearer-equipment, instant); only Scavenge: Repairs armor (bearer-equipment, amount one-point-one-location, instant); requirement only in Scavenge: immediately-after-kill; property only in Mend: targets-equipment, targets-player-affects-equipment; property only in Scavenge: kill-trigger; range: Touch vs Self | “Destroyed” vs “A destroyed”; nothing vs “carried by the caster”; “location” vs “of the caster's hit locations”; and 1 more |
| overlap | [Word of Mending](../profiles/word-of-mending.md) | Druid 6th, Wizard 6th | Repairs armor: amount one-point-one-location, instant vs amount all-armor, instant; only Mend: Repairs equipment (target-equipment, instant); only Word of Mending: Repairs equipment (target, instant); requirement only in Word of Mending: no-enemy-within-20ft; property only in Mend: has-choice, targets-equipment | “Destroyed or damaged item is repaired , or one point of armor in one location” vs “All equipment carried by target player”; nothing vs “All armor worn by target player is restored to full value . May not be cast within 20' of a living enemy .” |

## [Release](../profiles/release.md)

By touch, removes one State or Ongoing Effect of the caster's choice (not Cursed), along with others from the same source.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Greater Release](../profiles/greater-release.md) | Bard 2nd, Healer 2nd | only Release: Removes States or Ongoing Effects (target, instant); only Release: Removes States or Ongoing Effects (target, instant); only Greater Release: Removes States or Ongoing Effects (target, instant); only Greater Release: Removes States or Ongoing Effects (dead-target, instant); only Greater Release: Removes States or Ongoing Effects (target, instant); property only in Greater Release: bypass-cursed; range: Touch vs 20' | “A single” vs “All”; “Effect or State is” vs “Effects and States are”; “Casters choice” vs “The caster may choose to leave some States or Effects in place”; and 1 more |
| overlap | [Shake It Off](../profiles/shake-it-off.md) | Warrior 5th | only Release: Removes States or Ongoing Effects (target, instant); only Release: Removes States or Ongoing Effects (target, instant); only Shake It Off: Removes States or Ongoing Effects (caster, instant); requirement only in Shake It Off: caster-alive; property only in Shake It Off: works-while-suppressed; school: Sorcery vs Spirit; range: Touch vs Self | “A single” vs “10 seconds after casting THIS the caster may remove from themselves any number of States or”; “Effect or State is removed from the target . Casters” vs “Effects of their”; “Cannot remove Cursed” vs “THIS may be cast at any time the caster is alive , even while the caster would otherwise be prevented from casting abilities by Stunned , Suppressed , or similar”; and 4 more |

## [Restoration](../profiles/restoration.md)

Another player has all uses of their per-life abilities restored; not Empower, Confidence or Restoration.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Empower](../profiles/empower.md) | Bard 2nd | Restores used abilities: amount all, instant vs amount one, instant | “has all uses” vs “regains one use”; “their” vs “any”; “abilities restored” vs “ability they have expended”; and 3 more |

## [Shove](../profiles/shove.md)

Pushes a player within 20' back 20' in a straight line away from the caster, even if Stopped or Stunned; self-cast picks the direction.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Throw](../profiles/throw.md) | Wizard 3rd | Pushes away: feet 20, until arrival, if cast-on-other vs feet 50, until arrival, if cast-on-other; Pushes away: feet 20, until arrival, if cast-on-self vs feet 50, until arrival, if cast-on-self | “20'” vs “50'” |

## [Silver Tongue](../profiles/silver-tongue.md)

Bearer gains Swift 1/Refresh Charge x3 (m) without using purchased Swift, but may not use other sources of Swift while it is worn.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Swift](../profiles/swift.md) | Bard 4th, Druid 4th, Healer 4th, Wizard 4th, Monk 6th | only Silver Tongue: Grants Swift (bearer, while worn); only Silver Tongue: May not use other sources of ability (bearer, while worn); only Swift: Modifies the next ability cast (caster, until used); requirement only in Swift: not-on-charge-incantation, only-touch-other-self-or-balls; restriction only in Silver Tongue: excludes-other-sources; delivery: enchantment vs meta-magic; school: Sorcery vs Neutral; range: Touch vs - | “Bearer gains Swift 1/Refresh Charge x3 (m)” vs “Abilities require only a single iteration of the incantation”; nothing vs “For multi-line Incantations use the last line . May only be used on abilities at a range of Touch ,”; “sources of Swift may” vs “, Self , or on Magic Balls . May”; and 2 more |

## [Sleight of Mind](../profiles/sleight-of-mind.md)

The bearer's other Enchantments cannot be removed by Dispel Magic or similar abilities; Sleight of Mind does not count towards the Enchantment limit.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Apex](../profiles/apex.md) | Scout 6th | only Sleight of Mind: Protects Enchantments (bearer, while worn); only Apex: Grants Mend (bearer, permanent); only Apex: Grants Sleight of Mind (bearer, permanent); only Apex: Removes Evolution (bearer, permanent); only Apex: Removes Hold Person (bearer, permanent); only Apex: Removes Pinning Arrow (bearer, permanent); property only in Sleight of Mind: exempt-from-enchantment-limit; delivery: enchantment vs archetype; school: Sorcery vs Neutral; range: Other vs - | “Enchantments worn by the bearer” vs “Gain Mend 1/Life (ex) and Sleight of Mind (Self) 1/Life (ex) . Lose all instances of Evolution”; “other than THIS” vs “Hold Person”; “are not removed by Dispel Magic or similar abilities . Does not count towards the bearer's Enchantment Limit .” vs “and Pinning Arrow” |

## [Song of Battle](../profiles/song-of-battle.md)

While chanting, the bearer's wielded melee weapons are Armor Breaking.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Berserk](../profiles/berserk.md) | Barbarian 1st | Armor Breaking (bearer melee weapons): while chanting vs while worn; ends when only in Song of Battle: chant-stops; property only in Song of Battle: chant; school: Protection vs Sorcery | “Bearer must Chant THIS or sing a song regarding their martial prowess . Singing in place of the normal Chant is still a Chant and must follow all Chant rules .” vs nothing |

## [Song of Deflection](../profiles/song-of-deflection.md)

While chanting, the bearer is unaffected by projectiles other than Magic Balls and their Engulfing effects; equipment can still be affected.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Protection from Projectiles](../profiles/protection-from-projectiles.md) | Healer 4th | Unaffected by: while chanting vs while worn; Ignores Engulfing effects: while chanting vs while worn; ends when only in Song of Deflection: chant-stops; property only in Song of Deflection: chant; range: Self vs Other | “Bearer must Chant THIS or sing a song of their acrobatic prowess . Singing in place of the normal Chant is still a Chant and must follow all Chant rules .” vs nothing |

## [Song of Determination](../profiles/song-of-determination.md)

While chanting, the bearer is Immune to the Command School.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Immune to Command](../profiles/immune-to-command.md) | Anti-Paladin 1st, Barbarian 1st, Paladin 1st | Immune to Command: while chanting vs permanent; ends when only in Song of Determination: chant-stops; property only in Song of Determination: chant; delivery: enchantment vs trait; school: Protection vs Command; range: Self vs - | “Bearer” vs “The bearing player or object is unaffected by abilities from a given School . Immunity granted as a Trait does not prevent players from making use of their own class abilities . Unless otherwise noted , Immunities do not extend beyond the player or object that has them . Example : A player with Immunity to Flame can still have their armor destroyed by a Fireball . If a player”; “Command” vs “an effect which would remove a State or Ongoing Effect , the State/Ongoing Effect is not removed”; “Bearer must Chant THIS or sing” vs “Example : A player who is Immune to Sorcery cannot be Released from Frozen , as they cannot be affected by Release ,”; and 5 more |

## [Song of Interference](../profiles/song-of-interference.md)

While chanting, works as Enlightened Soul: the bearer is unaffected by Verbal Magical abilities used from beyond Touch.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does more than | [Enlightened Soul](../profiles/enlightened-soul.md) | Monk 1st, Healer 5th | only Song of Interference: Works as Enlightened Soul (bearer, while chanting); only Enlightened Soul: Unaffected by (bearer, while worn); only Enlightened Soul: Unaffected by (bearer, while worn); ends when only in Song of Interference: chant-stops; property only in Song of Interference: chant; range: Self vs Other, Self | “As per Enlightened Soul” vs “Bearer is unaffected by Verbal Magical abilities used at a Range greater than Touch”; “Bearer must Chant THIS or sing” vs “Affects beneficial as well as harmful Magical abilities . Does not affect (ex) abilities , abilities with”; “song about defeating/resisting the forces” vs “Range”; and 2 more |

## [Song of Power](../profiles/song-of-power.md)

While chanting, friendly players within 20' halve their Charge Incantation repetitions (rounded down, minimum 1); the bearer is Stopped.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Entangle](../profiles/entangle.md) | Druid 1st, Healer 2nd, Wizard 2nd | only Song of Power: Speeds up Charging (friendly-players, while chanting); only Song of Power: Stops (bearer, while chanting); only Entangle: Stops (struck-player, 60 s); restriction only in Song of Power: players-benefit-once; ends when only in Song of Power: chant-stops, moves-from-start; property only in Song of Power: chant; property only in Entangle: engulfing; delivery: enchantment vs magic-ball; school: Protection vs Subdual; range: Self vs - | “Friendly players within 20' of the bearer have their Charge Incantation repetitions divided by 2 , rounded down , to a minimum of 1 . Bearer” vs “Player struck”; nothing vs “for 60 seconds”; “Bearer must Chant THIS or sing an inspiring song” vs “Engulfing”; and 1 more |
| overlap | [Hold Person](../profiles/hold-person.md) | Assassin 4th, Scout 4th, Healer 2nd, Wizard 3rd | only Song of Power: Speeds up Charging (friendly-players, while chanting); only Song of Power: Stops (bearer, while chanting); only Hold Person: Stops (target, 30 s); restriction only in Song of Power: players-benefit-once; ends when only in Song of Power: chant-stops, moves-from-start; property only in Song of Power: chant; delivery: enchantment vs verbal; school: Protection vs Command; range: Self vs 20' | “Friendly players within 20' of the bearer have their Charge Incantation repetitions divided by 2 , rounded down , to a minimum of 1” vs “Target player becomes Stopped for 30 seconds”; “Bearer is Stopped . Bearer must Chant THIS or sing an inspiring song . Singing in place of the normal Chant is still a Chant and must follow all Chant rules . Players can only benefit from one instance of THIS at a time . THIS ends if the bearer moves from their starting location .” vs nothing |
| overlap | [Pinning Arrow](../profiles/pinning-arrow.md) | Archer 1st,3rd,5th, Scout 4th, Scout 5th | only Song of Power: Speeds up Charging (friendly-players, while chanting); only Song of Power: Stops (bearer, while chanting); only Pinning Arrow: Stops (struck-player, 30 s); restriction only in Song of Power: players-benefit-once; ends when only in Song of Power: chant-stops, moves-from-start; property only in Song of Power: chant; property only in Pinning Arrow: engulfing; delivery: enchantment vs specialty-arrow; school: Protection vs Sorcery; range: Self vs - | “Friendly players within 20' of the bearer have their Charge Incantation repetitions divided” vs “A player struck”; “2 , rounded down , to a minimum of 1 . Bearer” vs “this arrow”; nothing vs “for 30 seconds”; and 2 more |

## [Song of Survival](../profiles/song-of-survival.md)

While chanting, when the bearer would die they ignore it and become Insubstantial, in place or returning to base; once per life.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Gift of Air](../profiles/gift-of-air.md) | Druid 5th | only Song of Survival: Prevents death (bearer, until used); only Song of Survival: Ignores a hit (bearer, instant); only Gift of Air: Ignores a hit (bearer, instant); only Gift of Air: May not wield weapons (bearer, while worn); only Gift of Air: May not wield shields (bearer, while worn); restriction only in Song of Survival: once-per-life; ends when only in Song of Survival: activates-once, chant-stops; property only in Song of Survival: chant; range: Self vs Other | “When” vs “The effects of any weapon or arrow which just struck”; “would otherwise die” vs “are ignored”; “they” vs nothing; and 14 more |

## [Stun](../profiles/stun.md)

Stuns a player within 20' for 30 seconds.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Abeyance](../profiles/abeyance.md) | Healer 5th | Stuns: 30 s vs 60 s; property only in Abeyance: bypass-armor; delivery: verbal vs magic-ball; school: Sorcery vs Subdual; range: 20' vs - | “Target player” vs “This Magic Ball ignores armor . Player hit”; “30” vs “60” |

## [Suppress Aura](../profiles/suppress-aura.md)

Suppresses a target within 50' for 30 seconds, so they cannot cast abilities or Charge.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Break Concentration](../profiles/break-concentration.md) | Bard 3rd, Wizard 2nd | Suppresses: 30 s vs 10 s; range: 50' vs 20' | nothing vs “player”; “30” vs “10” |
| same-effects | [Suppression Arrow](../profiles/suppression-arrow.md) | Archer 4th | property only in Suppression Arrow: engulfing; delivery: verbal vs specialty-arrow; school: Command vs Sorcery; range: 50' vs - | “Target” vs “A player struck by this arrow”; nothing vs “Engulfing .” |
| same-effects-different-numbers | [Suppression Bolt](../profiles/suppression-bolt.md) | Wizard 2nd, Monk 6th | Suppresses: 30 s vs 60 s; property only in Suppression Bolt: engulfing; delivery: verbal vs magic-ball; school: Command vs Subdual; range: 50' vs - | “Target” vs “Player struck”; “30” vs “60”; nothing vs “Engulfing .” |
| overlap | [Brutal Strike](../profiles/brutal-strike.md) | Anti-Paladin 4th, Barbarian 5th | only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; school: Command vs Death; range: 50' vs Unlimited | nothing vs “player”; nothing vs “Cursed indefinitely . Target player is also”; nothing vs “Wound Trigger . THIS targets the wounded or dead player and does not require verbal targeting .” |

## [Swift](../profiles/swift.md)

Meta-Magic: the next Touch, Other, Self or Magic Ball ability needs only one iteration of its incantation (last line if multi-line).

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| is given by | [Medium](../profiles/medium.md) | Monk 6th | only Swift: Modifies the next ability cast (caster, until used); only Medium: Grants Blessing Against Wounds (bearer, permanent); only Medium: Grants Sever Spirit (bearer, permanent); only Medium: Grants Swift (bearer, permanent); only Medium: Changes how often abilities can be used (bearer, permanent); only Medium: May not wear armor (bearer, permanent); only Medium: May not wield great weapons (bearer, permanent); requirement only in Swift: not-on-charge-incantation, only-touch-other-self-or-balls; delivery: meta-magic vs archetype | nothing vs “Gain Blessing Against Wounds (Touch) 1/Life (ex) , Sever Spirit 1/Life Charge x3 (ex) , and Swift 2/Life (ex) .”; “require only a single iteration of” vs “in”; “incantation . For multi-line Incantations use the last line . May only be used on abilities at a range of Touch , Other , Self , or on Magic Balls” vs “Spirit school become Charge x3”; and 1 more |
| is given by | [Silver Tongue](../profiles/silver-tongue.md) | Bard 6th | only Swift: Modifies the next ability cast (caster, until used); only Silver Tongue: Grants Swift (bearer, while worn); only Silver Tongue: May not use other sources of ability (bearer, while worn); requirement only in Swift: not-on-charge-incantation, only-touch-other-self-or-balls; restriction only in Silver Tongue: excludes-other-sources; delivery: meta-magic vs enchantment; school: Neutral vs Sorcery; range: - vs Touch | “Abilities require only a single iteration” vs “Bearer gains Swift 1/Refresh Charge x3 (m) . Other sources”; “the incantation . For multi-line Incantations use the last line . May only be used on abilities at a range of Touch , Other , Self , or on Magic Balls . May” vs “Swift may”; “used on the Charge Incantation” vs “utilized while THIS is worn”; and 1 more |

## [Terror](../profiles/terror.md)

For 30 seconds a target within 20' may not attack or cast Magical abilities at the caster or their equipment and must stay 50' away.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects-different-numbers | [Awe](../profiles/awe.md) | Paladin 5th, Bard 3rd, Paladin 1st | Must keep away: feet 50, 30 s vs feet 20, 30 s; school: Death vs Command | “50'” vs “20'” |
