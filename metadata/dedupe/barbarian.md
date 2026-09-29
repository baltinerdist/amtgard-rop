---
title: "Barbarian: duplicate check"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Barbarian: duplicate check

Every comparable entry on the Barbarian list against every other ability, spell and trait in the rulebook.

## [Adrenaline](../profiles/adrenaline.md)

Kill Trigger: the caster heals one wound.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Golem](../profiles/golem.md) | Druid 4th | only Golem: Immune to Death (bearer, while worn); only Golem: Curses (bearer, while worn); only Golem: Changes Mend (bearer, while worn); only Golem: Acts as a respawn point (caster-of-enchantment, while worn, if caster-alive); only Golem: Acts as an Alternate Base (caster-of-enchantment, while worn); only Golem: Makes Enchantments Persistent (bearer, while worn); only Golem: May not use alternate bases (caster-of-enchantment, while worn); requirement only in Adrenaline: immediately-after-kill; restriction only in Golem: bearer-not-alternate-base, caster-may-not-use-alternate-bases, one-active-per-caster; property only in Adrenaline: kill-trigger; property only in Golem: active-while-dead, persistent; delivery: verbal vs enchantment; school: Spirit vs Sorcery; range: Self vs Other | “Caster heals” vs “Bearer is Immune to Death . Bearer is Cursed . Bearer can remove a wound via Mend . Bearer may use the caster as an alternate respawn point while the caster is alive . Bearer may treat the caster as an Alternate Base . All Enchantments worn by the Bearer , including THIS , are Persistent while THIS is worn . THIS remains active while the bearer is dead . A caster may only have a single THIS Enchantment at a time and may not use Alternate Bases . Bearer may not be treated as an Alternate Base . Greater Mend and Word of Mending will not remove”; “Kill Trigger .” vs nothing |
| is given by | [Vampirism](../profiles/vampirism.md) | Wizard 4th | only Adrenaline: Heals wounds (caster, amount one, instant); only Vampirism: Grants Adrenaline (bearer, while worn); only Vampirism: Immune to Death (bearer, while worn); only Vampirism: Curses (bearer, while worn); only Vampirism: Changes Adrenaline (bearer, while worn); requirement only in Adrenaline: immediately-after-kill; property only in Adrenaline: kill-trigger; property only in Vampirism: bypass-cursed; delivery: verbal vs enchantment; school: Spirit vs Death; range: Self vs Other | “Caster heals a wound” vs “Bearer gains Adrenaline Unlimited (ex) , is Immune to Death , and is Cursed”; “Kill Trigger” vs “Bearer's Adrenaline ability will work through their Cursed State” |
| overlap | [Greater Heal](../profiles/greater-heal.md) | Paladin 2nd, Healer 4th | only Adrenaline: Heals wounds (caster, amount one, instant); only Greater Heal: Heals wounds (target, amount all, instant); requirement only in Adrenaline: immediately-after-kill; property only in Adrenaline: kill-trigger; property only in Greater Heal: bypass-cursed; range: Self vs Touch | “Caster heals a wound” vs “All wounds are healed”; “Kill Trigger” vs “Ignores the Cursed State” |
| overlap | [Heal](../profiles/heal.md) | Monk 4th, Scout 2nd,5th, Druid 2nd, Healer 1st, Monk 1st, Scout 1st | only Adrenaline: Heals wounds (caster, amount one, instant); only Heal: Heals wounds (target, amount one, instant); requirement only in Adrenaline: immediately-after-kill; property only in Adrenaline: kill-trigger; range: Self vs Touch | “Caster” vs “Target player”; “Kill Trigger .” vs nothing |

## [Bear Strength](../profiles/bear-strength.md)

Bearer's wielded melee weapons are Shield Crushing.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Flame Blade](../profiles/flame-blade.md) | Anti-Paladin 6th, Druid 4th | only Flame Blade: Armor Breaking (bearer melee weapons) (bearer, while worn); only Flame Blade: Immune to Flame (bearer, while worn); only Flame Blade: Immune to Flame (bearer-equipment, while worn); school: Sorcery vs Flame; range: Other vs Other, Self | nothing vs “Armor Breaking and”; nothing vs “Bearer and their wielded weapons are Immune to Flame .” |
| does less than | [Lycanthropy](../profiles/lycanthropy.md) | Druid 4th | only Lycanthropy: Grants Magic Armor (bearer, points 2, while worn); only Lycanthropy: Immune to Command (bearer, while worn); school: Sorcery vs Death | nothing vs “Bearer gains two points of magic armor .”; nothing vs “Bearer is Immune to Command .” |
| is given by | [Raider](../profiles/raider.md) | Barbarian 6th | only Bear Strength: Shield Crushing (bearer melee weapons) (bearer, while worn); only Raider: Grants Bear Strength (bearer, permanent); only Raider: Changes Look The Part (bearer, permanent); only Raider: Changes Brutal Strike (bearer, permanent); only Raider: Changes how often abilities can be used (bearer, permanent); only Raider: Removes Rage (bearer, permanent); delivery: enchantment vs archetype; school: Sorcery vs Neutral; range: Other vs - | “Bearer's wielded melee weapons are Shield Crushing” vs “Gain Bear Strength (Self) 1/Life (ex)”; nothing vs “Look the Part becomes an additional use of Brutal Strike . Lose all instances of Rage .” |

## [Berserk](../profiles/berserk.md)

Bearer's wielded melee weapons are Armor Breaking.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| does less than | [Flame Blade](../profiles/flame-blade.md) | Anti-Paladin 6th, Druid 4th | only Flame Blade: Shield Crushing (bearer melee weapons) (bearer, while worn); only Flame Blade: Immune to Flame (bearer, while worn); only Flame Blade: Immune to Flame (bearer-equipment, while worn); school: Sorcery vs Flame; range: Self vs Other, Self | nothing vs “and Shield Crushing”; nothing vs “Bearer and their wielded weapons are Immune to Flame .” |
| does less than | [Void Touched](../profiles/void-touched.md) | Wizard 5th, Anti-Paladin 6th | only Void Touched: Grants Shadow Step (bearer, while worn); only Void Touched: Grants Steal Life Essence (bearer, while worn); only Void Touched: Unaffected by (bearer, while worn); only Void Touched: Curses (bearer, while worn); range: Self vs Other | nothing vs “Bearer gains Shadow Step 1/Refresh Charge x30 (ex) , Steal Life Essence Unlimited (ex) , and is unaffected by Magical abilities from the Sorcery , Spirit , and Death Schools . Bearer is Cursed . This effect does not interact with other Enchantments worn by the bearer .” |
| overlap | [Song of Battle](../profiles/song-of-battle.md) | Bard 2nd | Armor Breaking (bearer melee weapons): while worn vs while chanting; ends when only in Song of Battle: chant-stops; property only in Song of Battle: chant; school: Sorcery vs Protection | nothing vs “Bearer must Chant THIS or sing a song regarding their martial prowess . Singing in place of the normal Chant is still a Chant and must follow all Chant rules .” |

## [Blood and Thunder](../profiles/blood-and-thunder.md)

Kill Trigger: the caster gains Blessing Against Wounds (ex), marked with a white strip.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| gives its user | [Blessing Against Wounds](../profiles/blessing-against-wounds.md) | Healer 1st, Monk 6th | only Blood and Thunder: Grants Blessing Against Wounds (caster, until used); only Blessing Against Wounds: Grants Resistance (bearer, until used); requirement only in Blood and Thunder: immediately-after-kill; restriction only in Blessing Against Wounds: no-other-protection-enchantments; ends when only in Blessing Against Wounds: activates-once; property only in Blood and Thunder: kill-trigger, materials-required, uses-strips; property only in Blessing Against Wounds: exempt-from-enchantment-limit; delivery: verbal vs enchantment; school: Spirit vs Protection; range: Self vs Other | “Caster gains Blessing Against Wounds” vs “Bearer is resistant to wounds . Does not count towards the bearer's Enchantment limit . May not be worn with any other Enchantments from the Protection School unless the other Enchantment is”; “Kill Trigger . Caster must still wear a white strip to denote Blessing Against Wounds .” vs nothing |

## [Brutal Strike](../profiles/brutal-strike.md)

Wound Trigger: the player just wounded (or killed) is Cursed indefinitely and Suppressed for 30 seconds; no verbal targeting.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Assassinate](../profiles/assassinate.md) | Assassin 1st | only Brutal Strike: Suppresses (target, 30 s); requirement only in Brutal Strike: immediately-after-wound; requirement only in Assassinate: immediately-after-kill, target-dead; property only in Brutal Strike: wound-trigger; range: Unlimited vs 50' | “Target player” vs “The target”; “indefinitely” vs nothing; “Target player is also Suppressed for 30 seconds . Wound Trigger” vs “May only be used immediately upon killing an enemy”; and 1 more |
| overlap | [Break Concentration](../profiles/break-concentration.md) | Bard 3rd, Wizard 2nd | Suppresses: 30 s vs 10 s; only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; school: Death vs Command; range: Unlimited vs 20' | “Cursed indefinitely . Target player is also” vs nothing; “30” vs “10”; “Wound Trigger . THIS targets the wounded or dead player and does not require verbal targeting .” vs nothing |
| overlap | [Suppress Aura](../profiles/suppress-aura.md) | Bard 4th, Wizard 4th | only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; school: Death vs Command; range: Unlimited vs 50' | “player” vs nothing; “Cursed indefinitely . Target player is also” vs nothing; “Wound Trigger . THIS targets the wounded or dead player and does not require verbal targeting .” vs nothing |
| overlap | [Suppression Arrow](../profiles/suppression-arrow.md) | Archer 4th | only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; property only in Suppression Arrow: engulfing; delivery: verbal vs specialty-arrow; school: Death vs Sorcery; range: Unlimited vs - | “Target” vs “A”; nothing vs “struck by this arrow”; “Cursed indefinitely . Target player is also” vs nothing; and 2 more |
| overlap | [Suppression Bolt](../profiles/suppression-bolt.md) | Wizard 2nd, Monk 6th | Suppresses: 30 s vs 60 s; only Brutal Strike: Curses (target, until respawn); requirement only in Brutal Strike: immediately-after-wound; property only in Brutal Strike: no-verbal-targeting, wound-trigger; property only in Suppression Bolt: engulfing; delivery: verbal vs magic-ball; school: Death vs Subdual; range: Unlimited vs - | “Target player” vs “Player struck”; “Cursed indefinitely . Target player is also” vs nothing; “30” vs “60”; and 2 more |

## [Immune to Command](../profiles/immune-to-command.md)

Anti-Paladin, Barbarian and Paladin Trait: unaffected by Command School abilities; does not protect equipment or remove existing effects, and may still be targeted.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Song of Determination](../profiles/song-of-determination.md) | Bard 1st | Immune to Command: permanent vs while chanting; ends when only in Song of Determination: chant-stops; property only in Song of Determination: chant; delivery: trait vs enchantment; school: Command vs Protection; range: - vs Self | “The bearing player or object is unaffected by abilities from a given School . Immunity granted as a Trait does not prevent players from making use of their own class abilities . Unless otherwise noted , Immunities do not extend beyond the player or object that has them . Example : A player with Immunity to Flame can still have their armor destroyed by a Fireball . If a player” vs “Bearer”; “an effect which would remove” vs “Command . Bearer must Chant THIS or sing”; “State or Ongoing Effect , the State/Ongoing Effect is not removed” vs “song regarding their determination”; and 3 more |

## [Momentum](../profiles/momentum.md)

Kill Trigger: caster instantly Charges one ability by stating its name.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| same-effects | [Innate](../profiles/innate.md) | Monk 6th, Bard 2nd, Druid 2nd, Healer 2nd, Wizard 2nd | requirement only in Momentum: immediately-after-kill; property only in Momentum: kill-trigger; delivery: verbal vs meta-magic; school: Sorcery vs Neutral; range: Self vs - | “Kill Trigger” vs nothing |
| is given by | [Berserker](../profiles/berserker.md) | Barbarian 6th | only Momentum: Instantly Charges an ability (caster, instant); only Berserker: Grants Momentum (bearer, permanent); only Berserker: May not wear armor (bearer, permanent); only Berserker: Removes Blood and Thunder (bearer, permanent); requirement only in Momentum: immediately-after-kill; property only in Momentum: kill-trigger, must-declare; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Self vs - | nothing vs “Gain Momentum Unlimited (ex) (Ambulant) .”; “be used to instantly Charge a single ability by stating its name” vs “not wear Armor , and lose all instances of Blood and Thunder”; “Kill Trigger” vs nothing |
| is given by | [Marauder](../profiles/marauder.md) | Warrior 6th | only Momentum: Instantly Charges an ability (caster, instant); only Marauder: Grants Momentum (bearer, permanent); only Marauder: Changes Insult (bearer, permanent); only Marauder: Changes how often abilities can be used (bearer, permanent); only Marauder: Changes the armor limit (bearer, points 4, permanent); only Marauder: May not wield large shields (bearer, permanent); only Marauder: Changes Ancestral Armor (bearer, permanent); only Marauder: Changes how often abilities can be used (bearer, permanent); requirement only in Momentum: immediately-after-kill; property only in Momentum: kill-trigger, must-declare; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Self vs - | nothing vs “Gain Momentum Unlimited (ex) (Ambulant) . Insult becomes 1/Life Charge x5 (m) (Ambulant) . Maximum Armor becomes 4pts .”; “be used to instantly Charge a single ability by stating its name” vs “not wield Large shields”; “Kill Trigger” vs “Ancestral Armor is no longer chargeable .” |
| is given by | [Sniper](../profiles/sniper.md) | Archer 6th | only Momentum: Instantly Charges an ability (caster, instant); only Sniper: Allows equipment (bearer, permanent); only Sniper: Changes how often abilities can be used (bearer, permanent); only Sniper: Grants Momentum (bearer, permanent); only Sniper: Changes Look The Part (bearer, permanent); only Sniper: May not fire normal arrows (bearer, permanent); requirement only in Momentum: immediately-after-kill; property only in Momentum: kill-trigger, must-declare; delivery: verbal vs archetype; school: Sorcery vs Neutral; range: Self vs - | “be used to instantly” vs “physically carry any number of Specialty Arrows of each type . The frequency of each type of Specialty Arrow ability becomes 1 Arrow / Life”; “a single ability by stating its name” vs “x3”; “Kill Trigger” vs “Gain Momentum Unlimited (ex) (Ambulant) . Look the Part becomes Mend 1/Life (ex) . May not fire normal arrows .” |
| overlap | [Confidence](../profiles/confidence.md) | Bard 1st | only Momentum: Instantly Charges an ability (caster, instant); only Confidence: Instantly Charges an ability (target, instant); requirement only in Momentum: immediately-after-kill; requirement only in Confidence: no-enemy-within-20ft; property only in Momentum: kill-trigger, must-declare; range: Self vs Other | “May be used to” vs “Target player may”; “by stating its name” vs nothing; “Kill Trigger” vs “May not be used within 20' of a living enemy .” |

## [Rage](../profiles/rage.md)

For seven seconds, counted aloud, caster is unaffected by Verbals and their melee weapons are Shield Crushing and Armor Breaking.

| Relation | Ability | On | Differences | Wording |
| --- | --- | --- | --- | --- |
| overlap | [Flame Blade](../profiles/flame-blade.md) | Anti-Paladin 6th, Druid 4th | Shield Crushing (bearer melee weapons): 7 s vs while worn; Armor Breaking (bearer melee weapons): 7 s vs while worn; only Rage: Unaffected by (caster, 7 s); only Flame Blade: Immune to Flame (bearer, while worn); only Flame Blade: Immune to Flame (bearer-equipment, while worn); ends when only in Rage: begins-incantation, fails-to-count; property only in Rage: count-aloud; delivery: verbal vs enchantment; school: Sorcery vs Flame; range: Self vs Other, Self | “Caster is unaffected by Verbal abilities and their” vs “Bearer's”; nothing vs “Armor Breaking and”; nothing vs “. Bearer”; and 2 more |
