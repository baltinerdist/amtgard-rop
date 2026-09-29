---
title: "Acceptance test"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_acceptance.py
---

# Acceptance test

Questions the platform must answer, each with an answer built independently from the rule text by four agents who did not see the platform's output. Where a later check of the rule text showed a tester was wrong, the expected answer was corrected and the reason is listed. `scripts/meta_acceptance.py` reruns every question and rewrites this page; it fails if any answer changes.

**39 of 39 pass**; 1 known gap(s) listed under question 40.

| # | Result | Detail |
| --- | --- | --- |
| 1 | pass | 9/9 |
| 2 | pass | 15/15 |
| 3 | pass | 11/11 |
| 4 | pass | 14/14 |
| 5 | pass | 12/12 |
| 6 | pass | 2/2 |
| 7 | pass | 13/13 |
| 8 | pass | 20/20 |
| 9 | pass | 5/5 |
| 10 | pass | 4/4 |
| 11 | pass | 12/12 |
| 12 | pass | 10/10 |
| 13 | pass | 9/9 |
| 14 | pass | 12/12 |
| 15 | pass | 7/7 |
| 16 | pass | 7/7 |
| 17 | pass | 7/7 |
| 18 | pass | 58/58 |
| 19 | pass | 3/3 |
| 20 | pass | 9/9 |
| 21 | pass | 11/11 |
| 22 | pass | 5/5 |
| 23 | pass | 6/6 |
| 24 | pass | 19/19 |
| 25 | pass | 17/17 |
| 26 | pass | 9/9 |
| 27 | pass | 13/13 |
| 28 | pass | 6/6 |
| 29 | pass | 11/11 |
| 30 | pass | 6/6 |
| 31 | pass | 22/22 |
| 32 | pass | 4/4 |
| 33 | pass | 7/7 |
| 34 | pass | 3/3 |
| 36 | pass | 9/9 |
| 37 | pass | 20/20 |
| 38 | pass | 8/8 |
| 39 | pass | 5/5 |
| 40 | pass | 38/39 pairs, 5 forbidden checked |

## 1. Every ability that causes death (the target dies).

`python3 scripts/meta_query.py --cap causes-death --include-granted`

**pass**: 9/9.

Expected: call-lightning, coup-de-grace, dimensional-rift, dragged-below, finger-of-death, fireball, infernal, shatter, sphere-of-annihilation

## 2. Every ability that can kill in any way: causes death, makes wounds lethal (Wounds Kill), makes the target Fragile, or Siege.

`python3 scripts/meta_query.py --cap can-be-lethal --include-granted`

**pass**: 15/15.

Expected: call-lightning, contagion, coup-de-grace, dimensional-rift, dragged-below, finger-of-death, fireball, infernal, poison, poison-arrow, poison-glands, ravage, shatter, sphere-of-annihilation, toxic-blades

## 3. Every ability that holds another player in place (Frozen, Stopped or Stunned, or otherwise unable to move from where they are).

`python3 scripts/meta_query.py --cap holds-in-place --include-granted`

**pass**: 11/11.

Expected: abeyance, artificer, circle-of-protection, entangle, hold-person, iceball, icy-blast, lightning-bolt, pinning-arrow, snaring-vines, stun

## 4. Every ability that stops another player from casting (Suppressed, Stunned or Frozen).

`python3 scripts/meta_query.py --cap silences --include-granted`

**pass**: 14/14.

Expected: abeyance, artificer, break-concentration, brutal-strike, discordia, iceball, icy-blast, mystic, raise-dead, stun, suppress-aura, suppression-arrow, suppression-bolt, undead-minion

## 5. Every ability that can make a player Insubstantial (self or another).

`python3 scripts/meta_query.py --cap makes-insubstantial --include-granted`

**pass**: 12/12.

Expected: astral-intervention, blink, circle-of-protection, corruptor, gift-of-air, guardian, lost, martyr, shadow-step, song-of-survival, teleport, void-touched

Corrections to the tester's answer:

- add **guardian**: Guardian gains Martyr, and Martyr can leave the caster Insubstantial (Martyr L2; record fixed after the test).

## 6. Every ability that makes a player Invulnerable.

`python3 scripts/meta_query.py --facet "Applies State=invulnerable"`

**pass**: 2/2.

Expected: reload, song-of-visit

## 7. Every ability that Curses a player (including drawbacks on the bearer).

`python3 scripts/meta_query.py --facet "Applies State=cursed" --include-granted`

**pass**: 13/13.

Expected: assassinate, brutal-strike, corruptor, golem, medium, protection-from-magic, raise-dead, sever-spirit, sphere-of-annihilation, steal-life-essence, undead-minion, vampirism, void-touched

## 8. Every ability that heals wounds (one or all).

`python3 scripts/meta_query.py --cap heals --include-granted`

**pass**: 20/20.

Expected: adrenaline, battlefield-triage, corruptor, gift-of-water, golem, greater-heal, greater-resurrect, heal, juggernaut, mass-healing, phoenix-tears, raise-dead, regeneration, resurrect, steal-life-essence, troll-blood, true-grit, undead-minion, vampirism, void-touched

## 9. Every ability that returns a dead player to life.

`python3 scripts/meta_query.py --cap revives --include-granted`

**pass**: 5/5.

Expected: greater-resurrect, raise-dead, resurrect, true-grit, undead-minion

## 10. Every ability that prevents the bearer from dying (they survive a killing effect).

`python3 scripts/meta_query.py --cap survives-death --include-granted`

**pass**: 4/4.

Expected: juggernaut, phoenix-tears, song-of-survival, troll-blood

## 11. Every ability that removes Enchantments from a player.

`python3 scripts/meta_query.py --effect "Removes Enchantments" --include-granted`

**pass**: 12/12.

Expected: attuned, dispel-magic, essence-graft, juggernaut, medium, naturalize-magic, phoenix-tears, planar-grounding, raise-dead, resurrect, sever-spirit, undead-minion

Corrections to the tester's answer:

- add **juggernaut**: Gains Phoenix Tears, which removes the bearer's other non-persistent Enchantments.
- add **medium**: Gains Sever Spirit, which removes Enchantments from the dead target.
- add **undead-minion**: Gains Raise Dead, which removes the target's Enchantments.

## 12. Every ability that removes a State or Ongoing Effect.

`python3 scripts/meta_query.py --cap cleanses`

**pass**: 10/10.

Expected: circle-of-protection, greater-release, greater-resurrect, martyr, phoenix-tears, planar-grounding, release, shake-it-off, tracking, trickery

## 13. Every ability that moves another player (pushes, sends to base, teleports, summons, keeps away).

`python3 scripts/meta_query.py --cap moves-others`

**pass**: 9/9.

Expected: agoraphobia, awe, banish, lost, shove, summon-dead, teleport, terror, throw

## 14. Every ability that lets the user or an ally move while protected or to a location.

`python3 scripts/meta_query.py --cap "moves-self|moves-ally"`

**pass**: 12/12.

Expected: banish, blink, gift-of-air, lost, reload, sanctuary, shove, song-of-survival, song-of-visit, summon-dead, teleport, throw

## 15. Every ability that requires a willing target.

`python3 scripts/meta_query.py --facet Requirement=target-willing`

**pass**: 7/7.

Expected: circle-of-protection, greater-resurrect, martyr, raise-dead, resurrect, summon-dead, teleport

## 16. Every ability that only works on (or targets) a dead player.

`python3 scripts/meta_query.py --facet Requirement=target-dead`

**pass**: 7/7.

Expected: assassinate, greater-resurrect, raise-dead, resurrect, sever-spirit, steal-life-essence, summon-dead

## 17. Every ability that only works on a target in a particular State (Frozen, Stopped, Insubstantial) or wounded.

`python3 scripts/meta_query.py --facet "Requirement=target-frozen|target-stopped|target-insubstantial|target-wounded|immediately-after-wound"`

**pass**: 7/7.

Expected: banish, brutal-strike, coup-de-grace, dimensional-rift, dragged-below, shatter, tracking

## 18. Every ability with a drawback for its own user or bearer (something bad that happens to them).

`python3 scripts/meta_query.py --cap has-drawback`

**pass**: 58/58.

Expected: adaptive-blessing, amplification, ancestral-armor, apex, attuned, battlemage, berserker, blessing-against-wounds, blink, circle-of-protection, contagion, corruptor, dervish, enlightened-soul, essence-graft, evoker, gift-of-air, golem, guardian, heart-of-the-swarm, hunter, infernal, inquisitor, ironskin, juggernaut, legend, marauder, martyr, medium, mystic, necromancer, phoenix-tears, priest, protection-from-magic, raider, raise-dead, ranger, regeneration, reload, resurrect, rogue, sanctuary, silver-tongue, sniper, song-of-interference, song-of-power, song-of-survival, song-of-visit, spy, stoneskin, summoner, troll-blood, true-grit, undead-minion, vampirism, void-touched, warder, warlock

Corrections to the tester's answer:

- add **ironskin**: Works as per Ancestral Armor, whose armor loses a point per blocked hit; Ancestral Armor itself is in the answer.
- add **stoneskin**: Same as Ironskin.

## 19. Every ability whose effect ends early if the caster attacks the target, casts at them, or dies.

`python3 scripts/meta_query.py --facet "Ends when=caster-dies|caster-attacks-or-casts-at-target"`

**pass**: 3/3.

Expected: awe, insult, terror

## 20. Every ability that requires a Chant.

`python3 scripts/meta_query.py --facet Property=chant`

**pass**: 9/9.

Expected: sanctuary, song-of-battle, song-of-deflection, song-of-determination, song-of-freedom, song-of-interference, song-of-power, song-of-survival, song-of-visit

## 21. Every ability that the text calls a Forced Movement effect.

`python3 scripts/meta_query.py --facet Property=forced-movement`

**pass**: 11/11.

Expected: agoraphobia, awe, banish, gift-of-air, lost, shove, song-of-survival, song-of-visit, teleport, terror, throw

## 22. Every ability with a Kill Trigger or a Wound Trigger.

`python3 scripts/meta_query.py --facet "Property=kill-trigger|wound-trigger"`

**pass**: 5/5.

Expected: adrenaline, blood-and-thunder, brutal-strike, momentum, scavenge

## 23. Every ability that grants Magic Armor, with how many points.

`python3 scripts/meta_query.py --effect "Grants Magic Armor"`

**pass**: 6/6.

Expected: barkskin, gift-of-earth, gift-of-water, ironskin, lycanthropy, stoneskin

## 24. Every ability that gives weapons, balls or arrows Armor Breaking or Armor Destroying, or otherwise defeats or ignores armor.

`python3 scripts/meta_query.py --cap defeats-armor --include-granted`

**pass**: 19/19.

Expected: abeyance, berserk, corrosive-mist, corruptor, destroy-armor, destruction-arrow, fireball, flame-blade, force-bolt, infernal, inquisitor, lightning-bolt, mystic, phase-bolt, rage, sacred-blades, song-of-battle, sphere-of-annihilation, void-touched

## 25. Every ability that destroys, damages or disables weapons or shields.

`python3 scripts/meta_query.py --cap attacks-equipment --include-granted`

**pass**: 17/17.

Expected: bear-strength, destruction-arrow, fireball, flame-blade, force-bolt, gift-of-fire, heat-weapon, infernal, lightning-bolt, lycanthropy, mystic, phase-bolt, pyrotechnics, rage, raider, shatter-weapon, sphere-of-annihilation

## 26. Every ability that repairs armor or equipment.

`python3 scripts/meta_query.py --cap repairs --include-granted`

**pass**: 9/9.

Expected: apex, artificer, greater-mend, juggernaut, mend, phoenix-tears, scavenge, sniper, word-of-mending

## 27. Every ability that grants Immunity to a School, and which School.

`python3 scripts/meta_query.py "immune"`

**pass**: 13/13.

Expected: adaptive-protection, flame-blade, gift-of-fire, golem, immune-to-command, immune-to-death, immune-to-flame, immune-to-subdual, ironskin, lycanthropy, protection-from-evil, song-of-determination, vampirism

## 28. Every ability that makes the bearer Resistant (to what).

`python3 scripts/meta_query.py --cap resists --include-granted`

**pass**: 6/6.

Expected: adaptive-blessing, blessed-aura, blessing-against-harm, blessing-against-wounds, blood-and-thunder, medium

## 29. Every ability that does not count towards the Enchantment limit, or lets the bearer wear extra Enchantments.

`python3 scripts/meta_query.py --cap extra-enchantments --include-granted`

**pass**: 11/11.

Expected: adaptive-blessing, apex, attuned, blessing-against-wounds, blood-and-thunder, essence-graft, evolution, juggernaut, medium, phoenix-tears, sleight-of-mind

## 30. Every Enchantment that lets the bearer cast another ability by removing strips, and which ability.

`python3 scripts/meta_query.py --facet "Casts from strips=*"`

**pass**: 6/6.

Expected: battlefield-triage, corrosive-mist, discordia, mass-healing, naturalize-magic, snaring-vines

## 31. Every ability that can be cast or used while moving.

`python3 scripts/meta_query.py --cap castable-while-moving --include-granted`

**pass**: 22/22.

Expected: ambulant, artificer, assassinate, berserker, blink, brutal-strike, corruptor, destruction-arrow, elemental-barrage, insult, marauder, mass-healing, phase-arrow, pinning-arrow, poison-arrow, rage, sanctuary, shadow-step, sniper, suppression-arrow, tracking, void-touched

Corrections to the tester's answer:

- remove **momentum**: Momentum is castable while moving only as granted by Berserker, Marauder and Sniper (Ambulant), which are counted.
- add **artificer**: Gains Pinning, Phase and Suppression Arrows; Specialty Arrows are shot while moving.
- add **corruptor**: Gains Void Touched, which gains Shadow Step (may be cast while moving).

## 32. Every ability that cannot be used within 10' or 20' of a living enemy.

`python3 scripts/meta_query.py --facet "Limit on use=no-enemy-within-10ft|no-enemy-within-20ft"`

**pass**: 4/4.

Expected: confidence, regeneration, troll-blood, word-of-mending

## 33. Every ability that charges another ability instantly or restores used abilities.

`python3 scripts/meta_query.py --effect "Instantly Charges an ability" --effect "Restores used abilities"`

**pass**: 7/7.

Expected: confidence, empower, innate, momentum, restoration, rogue, steal-life-essence

## 34. Every ability that makes a player a respawn point or Alternate Base.

`python3 scripts/meta_query.py --cap team-base`

**pass**: 3/3.

Expected: golem, heart-of-the-swarm, undead-minion

## 36. Every archetype that forbids wearing armor or wielding a type of weapon or shield.

`python3 scripts/meta_query.py --facet Delivery=archetype --facet "Drawback=May not wear armor|May not wield weapons|May not wield shields|May not wield great weapons|May not wield javelins|May not wield large shields|May not wield heavy thrown|May not wield bows|May not wield long weapons"`

**pass**: 9/9.

Expected: berserker, corruptor, hunter, infernal, marauder, medium, mystic, rogue, spy

## 37. Every archetype or ability that doubles uses or changes the frequency or Charge of other abilities.

`python3 scripts/meta_query.py --cap changes-frequency --include-granted`

**pass**: 20/20.

Expected: artificer, battlemage, corruptor, dervish, evoker, experienced, hunter, infernal, legend, marauder, medium, necromancer, priest, raider, sniper, song-of-power, spy, summoner, warder, warlock

Corrections to the tester's answer:

- add **raider**: Look the Part becomes an additional use of Brutal Strike: a change in how often Brutal Strike can be used.

## 38. Every ability that says it works regardless of Immunities, Traits, States or Enchantments, or that ignores Enchantments or Resistances.

`python3 scripts/meta_query.py --facet "Property=bypass-states|bypass-enchantments|bypass-immunities|bypass-traits|bypass-resistances"`

**pass**: 8/8.

Expected: dispel-magic, greater-resurrect, sacred-blades, sever-spirit, shove, sphere-of-annihilation, steal-life-essence, throw

Corrections to the tester's answer:

- add **shove**: "Works on Stopped and Stunned players" (E2), recorded as bypass-states.
- add **throw**: Same as Shove.

## 39. Every ability that names Heal, and how (grants it, casts it, modifies it).

`python3 scripts/meta_query.py --facet "Names ability=Heal"`

**pass**: 5/5.

Expected: battlefield-triage, gift-of-water, mass-healing, priest, regeneration

## 40. Which Druid spells do the same thing as another spell, trait or ability anywhere in the rulebook (or strictly less/more)? List pairs.

Druid list and its neighbours. 'subset' means a does less than b; 'plus-drawback' means a is b plus a cost to its own side; 'provides' means a gives its user b; 'any' accepts any relation.

**pass**: 38/39 pairs, 5 forbidden checked.

- call-lightning **identical** finger-of-death
- innate **same-effects|identical** momentum
- attuned **any** evolution
- naturalize-magic **provides** dispel-magic
- snaring-vines **provides** hold-person
- corrosive-mist **provides** destroy-armor
- poison-glands **provides** poison
- gift-of-fire **provides** heat-weapon
- stoneskin **subset** ironskin
- barkskin **subset** ironskin
- barkskin **subset** stoneskin
- barkskin **subset** gift-of-earth
- barkskin **subset** gift-of-water
- bear-strength **subset** flame-blade
- berserk **subset** flame-blade
- bear-strength **subset** lycanthropy
- barkskin **subset** lycanthropy
- poison **any** toxic-blades
- contagion **plus-drawback** toxic-blades
- mend **any** greater-mend
- greater-mend **any** word-of-mending
- mend **any** scavenge
- heal **any** greater-heal
- heal **any** adrenaline
- resurrect **subset** greater-resurrect
- release **any** greater-release
- icy-blast **any** iceball
- entangle **any** hold-person
- entangle **any** pinning-arrow
- entangle **subset** lightning-bolt
- force-bolt **subset** phase-bolt
- force-bolt **subset** lightning-bolt
- regeneration **any** gift-of-water
- regeneration **subset** troll-blood
- troll-blood **any** phoenix-tears
- stoneform **any** force-barrier
- gift-of-air **any** song-of-survival
- teleport **any** lost
- teleport **any** banish

Must not be reported:

- toxic-blades subset contagion: Contagion only adds a Fragile drawback on its own bearer.
- resurrect subset raise-dead: Raise Dead adds only harm to the revived ally.
- heal subset resurrect: Resurrect needs a dead target; Heal works on the living.
- heal subset greater-resurrect: Same.
- dispel-magic subset sever-spirit: Sever Spirit needs a dead target.

Known gaps:

- troll-blood any phoenix-tears (found: no pair) — known gap: Both prevent death, Freeze the bearer and spend a strip, but those are 3 of 14 distinct effect keys between them (overlap score 0.21, threshold 0.5).
