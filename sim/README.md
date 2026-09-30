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
Python 3.14, but **nothing uses it yet**. The pure-Python engine runs about 45–55 games/s on
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
machine. An ablation over 1,000 games runs the baseline once, then takes about 20 s for each
ability removed.

## Layout

| Path | What |
| --- | --- |
| `rules/compile.py` | Metadata + class sheets + rulings → immutable `Ability` / `ClassSheet` objects |
| `rules/build_classes.py` | Builds `data/classes.json` from `rules/classes/*.md` and the metadata's availability rows; each field cites its source file |
| `rules/rulings.py` | Loads `data/rulings.json` (answers to the metadata's 87 open questions) |
| `rules/coverage.py` | Which effect kinds the engine executes; writes `COVERAGE.md` |
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
  - Protection from Magic and Protection from Projectiles
  - Ancestral Armor, Gift of Air
  - death prevention: Phoenix Tears (including what happens when it thaws), Troll Blood, Song of Survival
- **Triggers:**
  - Kill Trigger abilities and "immediately after a kill" (Scavenge, Momentum, Adrenaline, Assassinate)
  - "immediately after dying" (True Grit)
- **Game types** (rules/battlegames.md):
  - Mutual Annihilation: individual lives, 150 s count, and the team-wipe rule
  - "attrition": unlimited lives, timed, most kills wins. This stands in for objective games.
- **Team balancing:** random, snake draft by skill, level-sum greedy, class mirror.

## What is not modeled (yet)

- **Space.** There is no map, terrain, line of sight, movement speed, formations or objectives. Range and reach are probabilities.
- **Effect coverage** (from `COVERAGE.md`):
  - **257 of 445** effect instances are executed (58%)
  - **89** abilities are fully handled, **53** partly, and **41** not at all
  - The biggest gaps are `action.restrict` (25 abilities, e.g. Insult, Awe), `economy.purchase-restrict` and `meta.modify-next` (Extension, Swift, Ambulant).
  - Anything unhandled is counted in the `noop` metric of every run. Policies never pick an ability with no handled effects on purpose.
- **Chosen options** are random, not strategic: School choices, the Pick-one options, and whether and which Archetype to take.
- **Magic User spell lists** (`policies/buy.py`) come from the usefulness score with personal taste (log-normal, sd `loadout.spell_taste_sd`), two favorite spells bought first (`loadout.favorite_spells`), and at most one Archetype at 6th level. Unlimited non-ammunition abilities (Heal, Bardic songs) score double. Abilities that do nothing in the engine are never bought, including the Archetypes that only modify unmodeled abilities (Battlemage, Evoker, Warlock, Legend). Every purchasable, modeled ability is held in at least 2.8% of 1,000 mixed games (`tests/sim/test_buying.py` requires 2%). Before this, 33 were never held.
- **Rulings are recorded but not interpreted.** Each of the 87 open questions keeps the reading the metadata already encodes. An answer changes the simulation only if its entry carries a `sim` block (see `rules/rulings.py`). A missing, partial or unreadable `data/rulings.json` is tolerated: each open question without an entry falls back to the metadata's reading, and the fallback is logged.
- **Weapons.** There are no thrown weapons, and no backup weapons after one is destroyed.
- **Player decisions** are scripted heuristics. A different policy can change the conclusions, so run any important question at more than one policy setting.

## Known limitations (from the face-validity suite)

`sim/analyze/validity.py` runs 15 statistical checks that a veteran player would call obviously
true (mirror matches are 50/50, skill wins, armor helps, more lives means longer games, Heal
doesn't hurt, …). All pass except one, which is a structural limit of Phase 1:

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
- **Charging runs long.** Druids still spend a large share of field time charging Barkskin
  (Charge ×10, about 80 s), because the Charge policy picks the most valuable spent ability
  whether or not it will be used.
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
- `loadout`: Look The Part, Archetype and armor-wearing shares; spell copy cap; Magic User taste spread (`spell_taste_sd`) and favorite spells (`favorite_spells`)
- `policy`: revive priority, offense and charge rates, self-Insubstantial and forced-move durations, abandoning a cast when attacked
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
