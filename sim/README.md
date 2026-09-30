# Battlegame simulator (Phase 1)

A Monte Carlo model of Amtgard class battlegames, built on the repo's own rule data
(`metadata/abilities.json`, `rules/classes/*.md`). It is meant for **comparisons** — "does the game
change if this ability is removed?" — not for predicting real win rates. Every number that isn't a
rule is an assumption in `sim/data/assumptions.json`.

Phase 1 has **no map**: players are at base, on the field, or dead, and distance is represented by
probabilities (for example, the chance that a target is within 20').

## Setup

```sh
python3.14 -m venv .venv                      # .venv/ is gitignored
.venv/bin/pip install -r sim/requirements.txt
```

The packages are numpy, pandas, scipy, pytest, duckdb and numba. numba 0.67 installs on
Python 3.14, but **nothing uses it yet**. The pure-Python engine runs about 30–45 games/s on
10 cores, so no speed-up has been needed so far.

## Running

```sh
.venv/bin/python -m sim.run --games 1000                        # mixed scenarios, all cores
.venv/bin/python -m sim.run --games 500 --config small --seed 100
.venv/bin/python -m sim.run --games 1000 --ablate call-lightning,heal   # remove abilities everywhere
.venv/bin/python -m sim.run --games 1000 --substitute icy-blast:iceball  # merge: Icy Blast's holders get Iceball
.venv/bin/python -m sim.run --games 1000 --assume melee.base_hit_per_second=0.3 \
    --assume "range.p_in_range.20'=0.4"                         # override assumptions for one run
.venv/bin/python -m sim.analyze.winrate                         # latest run: class win rates, balance methods
.venv/bin/python -m sim.analyze.ablation --ability heal,call-lightning --games 1000
.venv/bin/python -m sim.analyze.ablation --ability heal,mend --together --games 1000   # as one set
.venv/bin/python -m sim.analyze.ablation --merge icy-blast:iceball --games 1000
.venv/bin/python -m sim.analyze.ablation --all --games 300 --csv sim/out/ablation.csv
.venv/bin/python -m sim.analyze.complexity                      # complexity cost per ability
.venv/bin/python -m sim.analyze.cut --games 300                 # cut ranking + 30% cut set -> sim/out/cut.json
.venv/bin/python -m sim.analyze.cut --games 200 --sample 15 --merges 3   # quick look
.venv/bin/python -m sim.analyze.cut --target 0.3 --by complexity --protect heal,mend
.venv/bin/python -m sim.analyze.sensitivity                     # re-check cut.json over an assumption grid
.venv/bin/python -m sim.analyze.sensitivity --grid melee.base_hit_per_second=0.18,0.26 --factorial
.venv/bin/python -m sim.analyze.sensitivity --analysis winrate --games 1000
.venv/bin/python -m sim.reports.build_report                    # -> sim/out/report.html
.venv/bin/python -m sim.analyze.validity                        # face-validity checks, pass/fail table (~3 min)
.venv/bin/python -m sim.analyze.validity --only level --set time.speech_words_per_second=2.5
.venv/bin/python -m sim.rules.build_classes                     # rebuild sim/data/classes.json
.venv/bin/python -m sim.rules.coverage                          # rebuild sim/COVERAGE.md
.venv/bin/python -m pytest tests/sim                            # includes the validity checks at half scale
SIM_VALIDITY_SCALE=1 .venv/bin/python -m pytest tests/sim/test_validity.py
```

Results are appended to `sim/out/runs.duckdb` (gitignored). It has four tables:

- `runs`
- `games`
- `players`
- `abilities` (casts, applied effects, no-ops, failures and kills per ability per game)

**Determinism.** The seed fixes everything about a game. The scenario, each player's loadout and
the play itself each draw from their own random stream derived from that seed. So a seed replays
exactly, including across processes and hash seeds (`tests/sim/test_determinism.py`).

**Performance.** The smoke run is 1,000 mixed games (10–40 players, average 24). Before the
validity fixes it took 15 s on 10 cores (66 games/s); it now takes 18–25 s (40–55 games/s). About
20% of that is the new code: shorter incantations mean more policy decisions, and casting players
are asked every tick whether to keep casting. The rest is load from other processes on the test
machine. Extending effect coverage from 257 to 398 instances costs about 4%: 56.2 games/s against
58.8 without it, run back to back on the same seeds (10 cores). The policy routines that use those
abilities (cleanses, repairs, buffs, escapes, value-per-second Charging) bring the smoke run from
23 s to 29–31 s on a shared machine (about 33 games/s). An ablation over 1,000 games runs
the baseline once, then takes about 20 s for each ability removed.

## Layout

| Path | What |
| --- | --- |
| `rules/compile.py` | Metadata + class sheets + rulings → immutable `Ability` / `ClassSheet` objects |
| `rules/build_classes.py` | Builds `data/classes.json` from `rules/classes/*.md` and the metadata's availability rows; each field cites its source file |
| `rules/rulings.py` | Loads `data/rulings.json` (answers to the metadata's 87 open questions) |
| `rules/coverage.py` | Which effect kinds the engine executes, and which are needs-map / out-of-scope and why; writes `COVERAGE.md` |
| `engine/state.py` | Player, ability uses, enchantments, casts |
| `engine/loadout.py` | Equipment and abilities from class and level. Martial classes use the level table and option picks. Magic Users spend 5 points per level as `policies/buy.py` chooses. |
| `engine/effects.py` | One handler per effect kind, plus the passive and loadout registries |
| `engine/game.py` | The one-second tick loop: engagement, melee, casting, hits, wounds, death, respawn, refresh |
| `policies/` | Scripted behavior per role (fighter / caster / support / archer), whether to keep casting under attack, the ability value score, and Magic User spell buying (`buy.py`) |
| `scenarios/` | Player count, class and level mix, skill spread, team balancing, game type |
| `run.py` | Parallel runner and DuckDB storage |
| `analyze/stats.py` | Wilson, game-clustered (sandwich) and cluster-bootstrap intervals, paired intervals |
| `analyze/winrate.py` | Class win rates with game-clustered intervals (naive Wilson kept for comparison) |
| `analyze/impact.py` | Paired gameplay-change measures and the distance D |
| `analyze/ablation.py` | Paired ablation / merge harness |
| `analyze/complexity.py` | Complexity cost per ability from the metadata (weights at the top of the file) |
| `analyze/cut.py` | Cut ranking, merge proposals, greedy cut set, combined re-simulation |
| `analyze/sensitivity.py` | Re-runs the cut (or win-rate) analysis over a grid of assumption settings |
| `reports/` | `build_report.py` + `report-template.html` → `sim/out/report.html` |
| `analyze/validity.py` | Face-validity suite: pass/fail table of checks a veteran player would expect to hold |

## What is modeled

- **Hit locations and wounds** (rules/combat-rules.md):
  - five locations
  - a torso wound, or any two wounds, is a death
  - a wounded arm or leg changes hit chances
- **Armor** (rules/magic-states-effects/special-effects.md, rules/weapon-types-shields-equipment.md):
  - class maximum on every location, and Magic Armor
  - special effects: Armor Breaking (zeroes 3 points or fewer), Armor Destroying, Shield Crushing (three hits break a shield), Wounds Kill
  - arrows are Armor Breaking
  - two-handed Great weapons get Armor Breaking and Shield Crushing
- **Casting** (rules/magic-states-effects/mechanics-and-definitions.md):
  - incantation time is words × repetitions ÷ speech rate
  - a use is spent on completion even if the ability fails
  - interrupted by wounds, death and states that stop action; sometimes by hits on armor
  - a caster attacked in melee breaks off the incantation (or Charge) to defend unless it finishes this second (`policies.keep_casting`)
  - healers heal themselves or allies out of melee that no one else is healing and who can receive it (not Cursed, Frozen or Insubstantial)
  - Charge takes the 28-word Charge incantation × N
- **Frequencies:**
  - per-life (restored at respawn) and per-refresh (restored on the scenario's refresh timer)
  - Unlimited
  - Magic Balls and Specialty Arrows, which have to be retrieved once none are left
- **Enchantments:**
  - one Magical enchantment per player, with extra slots from abilities such as Attuned or Evolution
  - exempt enchantments, strips, persistence
  - class Traits that are Enchantments (Berserk, Evolution, …) are always on
- **States** (rules/magic-states-effects/states.md):
  - Frozen and Insubstantial players can't be affected except by abilities that work on those states
  - Stunned players can't act and are easy to hit
  - Suppressed players can't cast
  - Cursed makes a player Immune to Spirit
  - Fragile players die on the next wound
- **Defenses:**
  - Immunity and Resistance (by School, next source, or wounds)
  - Protection from Magic and Protection from Projectiles (including Engulfing arrows), Void Touched, Rage
  - Ancestral Armor (and Stoneskin/Ironskin Magic Armor as per it), Harden Armor
  - Gift of Air and Song of Survival, with the bearer's choice of Insubstantial in place or a return to base (random, like other choices); Gift of Air stays on (ruling gift-of-air#1)
  - death prevention: Phoenix Tears (including what happens when it thaws), Troll Blood, Song of Survival
  - Planar Grounding and Song of Freedom prevent States; Sleight of Mind stops Dispel Magic
- **Equipment:** Harden, Greater Harden and Imbue protect weapons or shields (Harden not against
  object-destroying abilities such as Pyrotechnics); Heat Weapon puts a weapon out of use for 30 s;
  Sacred Blades ignore Magic Armor and wound Resistances.
- **Restrictions on players** (`action.restrict`), enforced by the engine where attacks and casts
  are chosen and resolved:
  - Awe and Terror (no attacking or Magic at the caster; negated when the caster attacks or casts at
    the target, or dies), Insult (only the caster, plus anyone who attacks the target)
  - Archetype drawbacks (no armor, no Great weapons, no shields or Large shields, no bows, no normal
    arrows), Gift of Air (no weapons or shields), Essence Graft (only the grafter's (m) Enchantments)
- **Enchantment grants:** abilities an Enchantment grants (Gift of Water's Heal, Void Touched,
  Undead Minion's Raise Dead on the caster, …) are separate uses, removed with it; "as per"
  grants take on the other ability's effects.
- **Archetypes and Traits at loadout:** group frequency changes (Dervish, Summoner, Warder, Warlock,
  Medium, Necromancer, Priest, Sniper, Experienced), purchase restrictions and cost changes for Magic
  Users (the buyer is replayed under the Archetype's rules), Look the Part changes (Artificer,
  Raider, Sniper), range and ability replacements (Avatar of Nature, Juggernaut).
- **Meta-Magic:** the engine states Swift, Extension and Persistent for a player when they are
  allowed and help (scripted players never do); never on abilities granted by Enchantments.
- **Triggers:**
  - Kill Trigger abilities (one per kill, the most valuable usable one) and "immediately after a
    kill" (Scavenge, Momentum, Adrenaline, Assassinate); a self-targeted trigger has no effect
    through the caster's Immunity, except Vampirism's Adrenaline through Cursed
  - Wound Triggers (Brutal Strike)
  - "immediately after dying" (True Grit)
- **Game types** (rules/battlegames.md):
  - Mutual Annihilation: individual lives, 150 s count, and the team-wipe rule
  - "attrition": unlimited lives, timed, most kills wins. This stands in for objective games.
- **Team balancing:** random, snake draft by skill, level-sum greedy, class mirror.

## What is not modeled (yet)

- **Space.** There is no map, terrain, line of sight, movement speed, formations or objectives. Range and reach are probabilities.
- **Effect coverage** (from `COVERAGE.md`):
  - **398 of 445** effect instances are executed (89%); none is an unexplained no-op
  - **23** are **needs-map** (Alternate Bases and respawn points, free movement, Blink's 10' exit
    rule, Sanctuary, Trickery, Ambulant, Summon Dead's death location, Reload's keep-away) and **24**
    are **out-of-scope** (spare equipment and weapon types Phase 1 doesn't tell apart, thrown
    weapons, hands, Missile Block's blocking skill, Imbue's equipment-only Engulfing protection,
    Song of Visit, Circle of Protection's group). `COVERAGE.md` gives the reason for each.
  - **159** abilities are fully handled, **15** partly, and **9** not at all (all needs-map or out-of-scope)
  - Anything not executed is counted in the `noop` metric of every run; explicitly unmodeled effects
    under the detail `needs-map:<kind>` or `out-of-scope:<kind>`. Policies never pick an ability
    with no handled effects on purpose.
- **Chosen options** are random, not strategic: School choices and the Pick-one options. Archetypes are chosen by value (below).
- **Loadout choices** (`policies/buy.py`). A Magic User's list comes from the usefulness score (benefits
  minus drawbacks, `policies/value.py`) with personal taste (log-normal, sd `loadout.spell_taste_sd`)
  and a few favorite spells bought first (one at 1st level up to `loadout.favorite_spells` = 3 at
  6th, drawn from any spell that helps the buyer's side in the engine). Unlimited non-ammunition
  abilities (Heal, Bardic songs) score double. An ability whose only handled effects are drawbacks
  (Battlemage's purchase restriction) is never bought. **Archetypes are chosen by value**: a
  6th-level player who considers one at all (`loadout.archetype_share`) takes it only if the build
  under it (its purchase restrictions and costs), plus what it adds, beats the build without it;
  martial players weigh its gain against their own kit (the armor Berserker takes away). In 1,000
  mixed games Summoner, Dervish, Warder and Necromancer are taken; Priest, Evoker, Warlock, Legend,
  Ranger and Avatar of Nature never are, because their restrictions cost more than they give in
  this model (Warlock and Evoker forbid most of a Wizard's kill spells). Every purchasable spell is
  held in at least 2% of games (`tests/sim/test_buying.py`).
- **Rulings are recorded but not interpreted.** Each of the 87 open questions keeps the reading the metadata already encodes. An answer changes the simulation only if its entry carries a `sim` block (see `rules/rulings.py`). A missing, partial or unreadable `data/rulings.json` is tolerated: each open question without an entry falls back to the metadata's reading, and the fallback is logged.
- **Weapons.** There are no thrown weapons, no weapon types other than Great weapons, and no backup weapons after one is destroyed.
- **Player decisions** are scripted heuristics. A different policy can change the conclusions, so run any important question at more than one policy setting.

## Known limitations (from the face-validity suite)

`sim/analyze/validity.py` runs 15 statistical checks that a veteran player would call obviously
true (mirror matches are 50/50, skill wins, armor helps, more lives means longer games, Heal
doesn't hurt, …). One fails: **class-stack**, a structural limit of Phase 1.

- **Level (fixed).** When effect coverage went from 257 to 398 instances, 6th level stopped beating
  1st level (0.428; the check expects ≥ 0.6). The cause was scripted choices that didn't weigh
  costs. The fixes, in the policies: drawbacks count as costs in `value.py` and are ignored by
  `buy.effective`; Archetypes are chosen by value instead of a coin flip (0.428 → 0.555); a Charge
  is chosen by value per second, only for something that will be used, and a Charge longer than
  `policy.max_field_charge_seconds` (30 s) waits for a lull with no enemy on the field (fighters
  and archers Charge only in a lull); Enchantments whose drawbacks cost the bearer more than they
  give (Gift of Air on a fighter) go to someone else (0.555 → 0.637). With the new ability routines
  below the check is at 0.618.
- **Melee classes are too strong against casters.** At equal skill, a small team stacked with
  Warriors, Barbarians, Paladins and Anti-Paladins beats a mixed team about 89% of the time (the
  check expects 50–80%). In the 1,000-game smoke run Warriors win 56% and Healers and Wizards 44–45%.
  Melee causes about 95% of kills when fighters meet casters. Things that were ruled out:
  a stronger `backline_factor`, skill-based ranged accuracy and making Stopped block engagement
  each moved the fighters-vs-casters result by at most 2 points. The likely cause is the missing
  map: casters can't keep distance or kite, and whoever reaches them wins. Two engine gaps add to
  it and belong to the engine, not the policies:
  - `engagement.backline_factor` is applied as a relative weight among foes in `Game._engage`,
    not as a slower approach rate. When every enemy is a caster, the weights are equal and fighters
    reach them at the full rate.
  - The **Stopped** State (Hold Person, Entangle, Lightning Bolt) has no effect on play: nothing
    stops a Stopped player from closing to melee.
  - Skill affects melee only. Magic Balls and arrows hit at a flat rate, whoever throws or shoots.
- **Wounds cost little.** A healed player dies again within 60 s about a third of the time, and a
  limb wound only shifts hit chances slightly. Heal is now neutral in the paired ablation
  (+0.001 [−0.018, +0.020]) rather than positive. Wounded fighters also never step back to be
  healed; they stay in melee, where no one heals them.
- **Handled abilities in play.** Roles now use abilities by what their effects do: Self buffs
  before a fight (Rage; Elemental Barrage with two or more balls in hand), escapes when attacked by
  a non-fighter or a wounded fighter (Blink, Shadow Step), cleanses on self or an ally out of melee
  (Release, Greater Release, Shake It Off, Circle of Protection; Martyr only by a non-fighter for a
  fighter or archer), repairs (Mend, Greater Mend, Word of Mending), and casters with a bow shoot.
  Still never cast in play: Teleport, Astral Intervention, Confidence, Empower, Restoration, Summon
  Dead, Force Barrier, Stoneform, Reload, Innate, and the Self-range Enchantments aimed at enemies
  (Discordia, Snaring Vines). A Ranger never appears because the value model never takes the
  Archetype, so caster bow use is covered by `tests/sim/test_policies.py` only.
- **Healers slipped slightly.** After this round's fixes Healers win 0.430 in the smoke run (0.447
  before; the intervals overlap). It is not the Archetypes (0.427 with none). Likely causes: Raise
  Dead and Phoenix Tears score lower now that their drawbacks count, and Healers spend time
  cleansing and mending. In the heal-not-harmful check the side with Heal scores 0.476 in
  annihilation (0.497 before), still inside the tolerance.

### Engine queries for policies

The engine enforces restrictions itself where attacks and casts are chosen and resolved, so a
policy that ignores them only wastes a choice (counted as a `restricted` failure). Policies can
avoid that with: `Game.can_attack(a, b)`, `Game.can_cast_at(a, b, uses)`,
`Game.restricted_targets(a)`, `Game.barred(p, what)` (e.g. `"wield-weapons"`),
`Game.can_fire_normal_arrows(p)`, `Game.weapon_usable(p)` (Heat Weapon), `Game.shield_up(p)`,
`Game.equipment_protection(p, item)` and `Game.prevented(p, state)`.

### Interpretations made by the handlers

Where a rule's text left a choice, the handlers read it as follows (ruling ids where one applies):
Insult bars Magic at anyone but the caster, the target and their allies included, and its exception
for attackers covers attacks only (insult#1); Awe/Terror/Insult leave (ex) abilities other than
Specialty Arrows allowed (awe#1, insult#3, terror#1); Awe's keep-away ends with it when negated; an
Essence Graft drops the bearer's (m) Enchantments from other casters; Experienced takes the
per-life option when a Verbal qualifies; a Magic User holds at most one Archetype; zero-cost
spells (Priest's Heal) are taken at their Max; the extra Protection Enchantment Phoenix Tears keeps
is the most recently attached one; an Undead Minion is kept down only while its caster lives to
raise it, then removes the Enchantment (Enchantments rule 8); Golem's Mend removes a wound instead
of repairing (golem#1); Shake It Off's 10 s delay comes from its text (E1), not the effect record;
Martyr takes the worst State by the engine's State order (martyr#1); Harden and Imbue pick weapons
or shield at random when the bearer has a shield (harden#1, imbue#1); Song of Power's 20' is the
20' range probability.
- The **control-scales** check passes, but only because control is worth about nothing in small
  games. There are no lines to break and no clumps for area effects to hit.

## Assumption categories

All values are in `data/assumptions.json`, and each has a unit and a reason. To change one for a single run without editing the file, pass `--assume group.name=value` to `sim.run`, `analyze.ablation` or `analyze.cut`. Add sub-keys to reach inside a dict value (`--assume melee.shield_logit.large=-0.8`). The flag can be repeated; unknown keys and type changes are rejected. Groups:

- `time`: tick length, speech rate (3.5 words/s; was 2.5, see below)
- `skill`: skill spread and effect size
- `melee`: base hit rate, shield, gang, wound, stunned and weak-weapon modifiers; hit-location weights; Great-weapon and shield use
- `engagement`: how fast melee pairs form and break; backline protection; target preference
- `range`: chance a target is in range
- `casting`: interrupts; casting while engaged
- `projectiles`: hit chances, shot time, ball retrieval
- `respawn`: rejoin time, pregame prep
- `loadout`: Look The Part and armor-wearing shares; the share of 6th-level players who consider an Archetype; spell copy cap; Magic User taste spread (`spell_taste_sd`) and favorite spells (`favorite_spells`)
- `policy`: revive priority, offense and charge rates, the longest Charge started mid-battle, self-Insubstantial and forced-move durations, abandoning a cast when attacked
- `game`: time cap
- `population`: class and level mix. These are placeholders until ORK attendance data is available.

## Reading results

- **Player-level win rates** use **game-clustered** intervals: players in the same game share its outcome, so each game is one cluster (a cluster-robust sandwich estimate). The naive Wilson interval is still printed next to it. The design effect (`deff`) is the ratio of the clustered variance to the naive one.
  - For **class** win rates the clustered interval is slightly *narrower* (deff ≈ 0.6–0.9 in the mixed preset). In about half the games a class has players on both teams, and one of them wins while the other loses, so the correlation within a game is negative. A cluster bootstrap agrees to within 0.002.
  - Groupings that sit on one team (for example team or balance method) get the wider interval you would expect.
- **Team- and game-level measures** are one row per game already.
- **Ablation** compares the holder team's result with and without the ability, over the same seeds, with a **paired-by-seed** interval.
  - Paired seeds align the rosters, but play diverges once the ability would have mattered. That adds noise, not bias.
  - For Magic Users, the points freed by an ablated spell are re-spent. That's how a real player would respond.
  - Several abilities can be removed at once (`--ablate a,b`, `ablation --together`).
- **Gameplay change distance D** (`analyze/impact.py`) summarises how much the whole game moved. It is the weighted RMS of six standardised components:
  - holder-team win change ÷ 0.5
  - game length ÷ its baseline sd
  - share of time dead ÷ its baseline sd
  - kills per player ÷ its baseline sd
  - relative change in the spread of class win rates
  - total variation distance of the ability-use mix

  Every component and D has a paired bootstrap interval. `distance_adj` subtracts the noise floor, and it is what the cut ranking uses. The component weights are `DISTANCE_WEIGHTS` in `impact.py`.

## Cut analysis: which ~30% could go?

`analyze/cut.py` answers the question in seven steps. It writes `sim/out/cut.json`, and the report is built from that file.

1. **Complexity** per ability (`analyze/complexity.py`) is a weighted count of the ability's rules material. The weights are the `WEIGHTS` dict at the top of the file; a point is roughly one rule sentence. It counts:
   - rule sentences and words
   - incantation words × repetitions
   - requirements, restrictions, ending conditions and properties
   - references to other rules, clarifications and open questions
   - the classes and class-levels that carry the ability
2. **Single ablations** of every measurable ability, paired against one baseline. Abilities the engine cannot execute are listed but **not ranked**, because their impact would read as zero whatever they really do. `--include-unmodeled` overrides this.
3. **Merges** come from similar pairs in `metadata/abilities.json` `pairs` (also shown in `metadata/SIMILARITY.md`) with one of these relations: identical, same effects, same effects with different numbers, or plus a drawback.
   - The ability carried by more class-levels is kept.
   - The other is replaced by it for its holders, using `sim.run --substitute`.
4. **Ranking** is by impact per point of complexity.
5. **Greedy selection** picks cuts and merges until the target is met: `--target 0.3 --by count|complexity`. `--protect` lists abilities that must stay.
6. **Combined re-simulation** removes the chosen set together, because single impacts don't add up.
7. **Sensitivity** (`analyze/sensitivity.py`) re-runs steps 2–6 at each setting of a small grid of `--assume` overrides. It reports whether each ability stays picked (or in the bottom 30% of the ranking) at every setting.

**Cost.** Each ability and each merge is one run of `--games` games:

- On 10 cores, `--games 200 --sample 15 --merges 3` (20 runs, 4,000 games) took **89 s**.
- A full run is about 145 runs (110 measurable abilities, 33 merges, the baseline and the combined check). That is about **11 min at 200 games per run** and **about 55 min at 1,000**.
- The default sensitivity grid (6 settings) multiplies the cost by 6.

At 200 games most abilities sit at the noise floor (`distance_adj` = 0). Use 1,000 or more games before reading much into the ranking.

**Heal, and what the first smoke run got wrong.** In the first smoke run, removing Heal raised the
holder team's win chance (+0.027 [+0.007, +0.046] over 2,000 paired games). Instrumenting 400 games
showed the cause was mainly the policy, with the speech rate as a secondary factor:

- 36% of Heal starts targeted an ally someone else was already healing, and 40% targeted an ally
  in melee. Heal is Touch, so the healer has to stand next to the target for the whole
  incantation. 26% of completed Heals landed on a Cursed ally, who is Immune to Spirit.
  Only 26% of the Healers' Heals removed a wound, 0.21 per Healer life.
- The engine never asked a casting player anything, so a caster attacked mid-incantation (or mid-Charge)
  kept talking and never struck back until a wound interrupted them.
- At 2.5 words/s a Heal took 16 s and a Magic Ball 10 s.

The fixes:

- The policy heals itself or allies out of melee that no one else is healing and who can receive it.
- The engine now asks `policies.keep_casting` each tick, and an attacked caster breaks off to defend.
- The speech rate is 3.5 words/s.

With them, removing Heal changes the holder team's result by +0.001 [−0.018, +0.020]: neutral.
In the face-validity check where one side of a mirror match loses Heal, the side with Heal now
scores 0.52 (attrition) and 0.51 (annihilation); it was 0.46 and 0.42. Heal is neutral rather than
clearly helpful because wounds cost little in this model (see Known limitations).

**Speech rate sensitivity.** In the validity check "level", 6th-level players beat the same
classes at 1st level 52% of the time with the original code (2.5 words/s). With the policy fixes it
is 56% at 2.5 words/s, 66–68% at 3.5 and 73% at 4.5 (the 4.5 figure is from a half-scale run). Rerun an important question with
`--set time.speech_words_per_second=…` on the validity suite, or edit the assumption.
