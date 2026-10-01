# Battlegame simulator (Phase 1, and Phase 2 stage 1: the field)

A Monte Carlo model of Amtgard class battlegames, built on the repo's own rule data
(`metadata/abilities.json`, `rules/classes/*.md`). It is meant for **comparisons** — "does the game
change if this ability is removed?" — not for predicting real win rates. Every number that isn't a
rule is an assumption in `sim/data/assumptions.json`.

Phase 1 has **no map**: players are at base, on the field, or dead, and distance is represented by
probabilities (for example, the chance that a target is within 20'). That is still the default.
`--space on` puts players on a field with positions and movement (see "Phase 2: the field").

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
.venv/bin/python -m sim.run --games 1000 --space on                     # on the field (Phase 2 stage 1)
.venv/bin/python -m sim.run --games 1000 --assume melee.base_hit_per_second=0.3 \
    --assume "range.p_in_range.20'=0.4"                         # override assumptions for one run
.venv/bin/python -m sim.analyze.winrate                         # latest run: class win rates, balance methods
.venv/bin/python -m sim.analyze.doctrines                       # latest run: caster doctrines, assists -> sim/out/doctrines.json
.venv/bin/python -m sim.analyze.doctrines --level 6             # one level only (Archetype doctrines exist at 6th)
.venv/bin/python -m sim.rules.doctrines                         # validate sim/data/doctrines.json
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
.venv/bin/python -m sim.reports.build_report                    # -> sim/out/report.html (doctrine section if doctrines.json exists)
.venv/bin/python -m sim.analyze.validity                        # face-validity checks, pass/fail table (~3 min)
.venv/bin/python -m sim.analyze.calibrate                       # measure the score's anchor weights (~2 h 30 min)
.venv/bin/python -m sim.analyze.calibrate --weights             # every weight in use: hand, calibrated, source
.venv/bin/python -m sim.analyze.calibrate --from-raw            # re-summarize the saved pairs without playing
.venv/bin/python -m sim.analyze.validity --only level --set time.speech_words_per_second=2.5
.venv/bin/python -m sim.rules.build_classes                     # rebuild sim/data/classes.json
.venv/bin/python -m sim.rules.coverage                          # rebuild sim/COVERAGE.md
.venv/bin/python -m pytest tests/sim                            # includes the validity checks at half scale
SIM_VALIDITY_SCALE=1 .venv/bin/python -m pytest tests/sim/test_validity.py
```

Results are appended to `sim/out/runs.duckdb` (gitignored). It has four tables:

- `runs`
- `games`
- `players`: one row per player and game. Besides class, level, skill, kills, deaths and the result:
  `doctrine` and `play` (a Magic User's build plan and play style; empty for martial classes),
  `lives` played, `enchant_assists`, `control_assists`, `saves` (see Caster doctrines) and `bought`
  (a Magic User's purchases, `slug:copies,...`). Columns added since a database was created are
  added to it on the next run, with NULL for older rows.
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
23 s to 29–31 s on a shared machine (about 33 games/s). With caster doctrines (play styles, finishers, assist bookkeeping) the smoke run takes about 20 s
(50 games/s) and 2,000 mixed games 47 s on 10 cores. An ablation over 1,000 games runs
the baseline once, then takes about 20 s for each ability removed.

## Layout

| Path | What |
| --- | --- |
| `rules/compile.py` | Metadata + class sheets + rulings → immutable `Ability` / `ClassSheet` objects |
| `rules/build_classes.py` | Builds `data/classes.json` from `rules/classes/*.md` and the metadata's availability rows; each field cites its source file |
| `rules/doctrines.py` | Loads and validates `data/doctrines.json` (caster build plans); `Rules.doctrines` |
| `rules/rulings.py` | Loads `data/rulings.json` (answers to the metadata's 87 open questions) |
| `rules/coverage.py` | Which effect kinds the engine executes, and which are needs-map / out-of-scope and why; writes `COVERAGE.md` |
| `engine/state.py` | Player, ability uses, enchantments, casts |
| `engine/loadout.py` | Equipment and abilities from class and level. Martial classes use the level table and option picks. Magic Users spend 5 points per level as `policies/buy.py` chooses. |
| `engine/effects.py` | One handler per effect kind, plus the passive and loadout registries |
| `engine/game.py` | The tick loop: engagement, melee, casting, hits, wounds, death, respawn, refresh |
| `engine/space.py` | Where players are: the `Space` interface every distance question goes through; `NullSpace` (Phase 1) and `FieldSpace` (the field, `--space on`) |
| `policies/` | Scripted behavior per role (fighter / archer) and per doctrine play style (striker, controller, enchanter, medic, battle, archer), whether to keep casting under attack, the ability value score, and Magic User spell buying by doctrine (`buy.py`) |
| `scenarios/` | Player count, class and level mix, skill spread, team balancing, game type |
| `run.py` | Parallel runner and DuckDB storage |
| `analyze/stats.py` | Wilson, game-clustered (sandwich) and cluster-bootstrap intervals, paired intervals |
| `analyze/field.py` | Deaths per minute by kind of player and rejoin time after respawn, for a stored run |
| `analyze/winrate.py` | Class win rates with game-clustered intervals (naive Wilson kept for comparison) |
| `analyze/doctrines.py` | Per class and doctrine: share, win rate, kills, assists and saves per life, most-bought spells |
| `analyze/impact.py` | Paired gameplay-change measures and the distance D |
| `analyze/ablation.py` | Paired ablation / merge harness |
| `analyze/complexity.py` | Complexity cost per ability from the metadata (weights at the top of the file) |
| `analyze/cut.py` | Cut ranking, merge proposals, greedy cut set, combined re-simulation |
| `analyze/sensitivity.py` | Re-runs the cut (or win-rate) analysis over a grid of assumption settings |
| `reports/` | `build_report.py` + `report-template.html` → `sim/out/report.html` |
| `analyze/validity.py` | Face-validity suite: pass/fail table of checks a veteran player would expect to hold |
| `analyze/calibrate.py` | Calibration harness: paired gifts to team 0, per-unit win change per anchor, → `data/value-calibration.json` |
| `policies/calibration.py` | Builds value.py's weight tables from `data/value-calibration.json` (calibrated or hand, with sources); the staleness check |
| `policies/utility.py` | Situational utility: per-ability functions `(game, caster, target) -> utility`, registered by slug |
| `policies/songs.py`, `policies/enablers.py` | The utility functions: Bardic songs; refills, extra slots, grant Enchantments, Undead Minion, Self strip Enchantments |
| `engine/gifts.py` | Calibration-only gifts injected into a game from their own random stream (armor, a shield, ability uses, a State on enemies, ...) |

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
  - a refill (an instant Charge, a restored use) acts on the spent ability its caster names when it
    resolves (`Game.name_refill`, the policy's choice); Empower gives back one use of it
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

- **Space.** With `--space off` (the default) there is no map, terrain, line of sight, movement speed, formations or objectives, and range and reach are probabilities. `--space on` adds positions and movement (see "Phase 2: the field"), still without terrain, line of sight or objectives.
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
- **Loadout choices** (`policies/buy.py`). A Magic User builds to a **doctrine** (see Caster
  doctrines below): the doctrine's Archetype first, then its core spells in order, then a greedy
  fill by usefulness score (benefits minus drawbacks, `policies/value.py`; an enabler such as
  Attuned or Extension scored against the spells already bought) times personal taste
  (log-normal, sd `loadout.spell_taste_sd`) times the doctrine's weights, after a few favorite
  spells (one at 1st level up to `loadout.favorite_spells` = 3 at 6th). Unlimited non-ammunition
  abilities (Heal, Bardic songs) score double. **Martial Archetypes are chosen by value**: a
  6th-level martial player who considers one at all (`loadout.archetype_share`) takes the one whose
  gain for their own kit (the armor Berserker takes away) is largest, or none. Every purchasable,
  modeled spell is held in at least 2% of games (`tests/sim/test_buying.py`).
- **Rulings are recorded but not interpreted.** Each of the 87 open questions keeps the reading the metadata already encodes. An answer changes the simulation only if its entry carries a `sim` block (see `rules/rulings.py`). A missing, partial or unreadable `data/rulings.json` is tolerated: each open question without an entry falls back to the metadata's reading, and the fallback is logged.
- **Weapons.** There are no thrown weapons, no weapon types other than Great weapons, and no backup weapons after one is destroyed.
- **Player decisions** are scripted heuristics. A different policy can change the conclusions, so run any important question at more than one policy setting.

## Phase 2: the field (stage 1)

`sim/PHASE2.md` is the design. Stage 1, the geometry core, is built: every distance question goes
through one interface, `Game.space` (`sim/engine/space.py`), with two implementations.

- **`--space off` (the default): `NullSpace`, Phase 1 exactly.** Each method draws the same
  probability from the same random stream in the same order as the code it replaced (`range.p_in_range`,
  `range.p_ally_nearby_for_touch`, `engagement.*` and the backline weight, `respawn.rejoin_seconds`).
  `tests/sim/test_space.py` compares the result and full event trace of 30 mixed games with digests
  recorded before the change (`tests/sim/data/phase1_digests.json`), and the face-validity table is
  unchanged line for line.
- **`--space on`: `FieldSpace`, positions and movement.** The default stays off in stage 1, because
  the value calibration (`data/value-calibration.json`) was measured without the map. A run with
  space on prints a warning saying so; it does not raise a stale-calibration error, because the
  calibration's fingerprint leaves out the `space` assumption group, which space-off play never
  reads. `ENGINE_VERSION` is unchanged.

```sh
.venv/bin/python -m sim.run --games 2000 --seed 1 --space on
.venv/bin/python -m sim.analyze.validity --space on
.venv/bin/python -m sim.analyze.ablation --ability heal --games 1000 --space on
.venv/bin/python -m sim.analyze.cut --games 300 --space on          # recorded in cut.json; sensitivity follows it
.venv/bin/python -m sim.analyze.field                                # deaths per minute by kind, rejoin time
.venv/bin/python -m pytest tests/sim/test_space.py
```

The mode is stored in `runs.space`; space-on runs add `games.rejoin_n` and `games.rejoin_sum`.

### What the field does

- **The field.** A 60 m × 40 m rectangle with a base at each short end, no obstacles. Each team
  forms near its own base: line fighters on a line 6 m out, everyone else behind them.
- **Time.** 0.5 s ticks for movement, engagement and melee (per-second hit chances become per-tick
  chances). Incantations and Charges still count in seconds. Each player's brain (`decide`, the
  utilities, the songs; unchanged) runs once a second, staggered across players, as in Phase 1.
- **Ranges** are geometric: 20' = 6.1 m, 50' = 15.2 m, Touch and Other 1 m. They are checked when the
  incantation starts and again when it completes ("If the incantation is completed and the target is
  not in range, the ability fails but is still expended"; recorded as an `out-of-range` failure).
  The policies pick only targets in range. Melee reach is by weapon: 1.2 m for a Magic User's or
  archer's short weapon, 1.5 m standard, 2.1 m for a Great weapon. "No enemy within 20'/10'" is
  measured, and so is Song of Power's 20'.
- **Movement.** Walking speed is 1.4 m/s (taking position, walking back from base) and running 4 m/s
  (charging, retreating, reaching a wounded teammate). States and wounds as the rules say:
  - incanting or Charging players don't move their feet (a Chant may move)
  - Stopped, Frozen, Stunned and Insubstantial players don't move
  - a leg wound moves on the knees (0.3 m/s) with a living enemy within 20', and otherwise hobbles,
    one step a second (0.5 m/s) (combat-rules.md, Hit Locations notes 4 and 6)
  - a player a teammate is incanting a Touch ability on stands still for it
- **Engagement from proximity.** A line fighter charges when an enemy is within 8 m. It runs at the
  enemy it can reach soonest: running time, plus 1.5 s per teammate already on that enemy, less
  1 s for a caster, healer or archer. It fights once within reach. An attacked player strikes back,
  and a pair breaks when farther apart than the longer reach plus half a metre. Melee itself (hit
  chance, locations, wounds) is unchanged.
- **Respawn** is at base, followed by a walk back; there is no rejoin timer. A player sent to base is
  off the field for the walk there. Nobody starts a melee with a player who hasn't yet left their
  base zone (5 m) since arriving. After a team wipe in Mutual Annihilation everyone is set back to
  base (battlegames.md).
- **Play styles as positions** (`FieldSpace._want`; each is an assumption in the `space` group):

  | Who | Where they go |
  | --- | --- |
  | line fighters (fighters, battle casters, archers without a bow) | a slot in the team's line (2 m apart). The line walks forward as a body, waits for its fighters and stops 8 m short of the enemy, and the fighters then charge |
  | strikers and controllers | 5.5 m from the nearest enemy (inside 20'), at least 2 m behind their own fighting front |
  | medics | run to the nearest teammate out of melee who is wounded (or dead, if they hold a revive); otherwise 8 m back, 4 m behind the front |
  | enchanters | run to the nearest free teammate with an open Enchantment slot while they hold one to give; otherwise just behind the front |
  | archers | 15 m from the nearest enemy, 4 m behind the front |
  | anyone not in the line | retreats at a run, and starts no incantation, while a free enemy line fighter is within 6 m |

### What isn't spatial yet

These are stage 2 and are left as Phase 1 had them:

- **Projectiles** keep their flat hit chances (`projectiles.*_p_hit`). They can only be thrown within
  12 m (Magic Balls) or shot within 30 m (arrows), and thrown balls don't land anywhere.
- **Forced movement** (Shove, Throw, Lost, Banish, keep-away, Agoraphobia) still uses Phase 1's
  `kept_away_until` timer, and `send_to_base` is a walk off the field.
- **The other needs-map effects** are not modeled: Teleport, Blink's 10', Summon Dead, Ambulant
  (only the `Uses.ambulant` flag is honored), alternate bases and respawn points, Heart of the
  Swarm, Sanctuary.
- **The usefulness score** (`policies/value.py`) still prices range and mobility with the Phase 1
  tables (Extension, Song of Power, MOBILITY), and the calibration is Phase 1's.
- **The game itself** has no terrain, line of sight, objectives or player collision; players can
  pass through each other.

### Results, space off vs on

Face validity (`sim.analyze.validity`, full scale):

| Check | Space off | Space on |
| --- | --- | --- |
| mirror | 0.495 | 0.518 |
| seat-swap | 0.484 vs 0.499 | 0.475 vs 0.487 |
| no-abilities | 0.484 | 0.478 |
| skill | 0.927 | 0.888 |
| skill-vs-class | 0.608 | 0.729 |
| **class-stack** | **0.865 (FAIL, known limit)** | **0.634 (PASS)** |
| numbers | 0.887 | 0.884 |
| armor | 1.000 | 1.000 |
| level | 0.686 | 0.639 |
| healer-added | 0.573 | 0.539 |
| heal-not-harmful | attrition 0.521, annihilation 0.496 | attrition 0.543, annihilation 0.517 |
| archers-vs-armor | 9.65 vs 4.32 kills per archer | 19.63 vs 12.17 |
| control-scales | small +0.007, large +0.090 | small −0.012, large −0.030 |
| more-lives | 239 / 417 / 746 s | 389 / 551 / 969 s |
| healer-behavior | 0.0% / 3.5% / 1.4% | 0.1% / 2.1% / 1.9% |
| passed | 14/15 | 15/15 |

2,000 mixed games (`sim.run --games 2000 --seed 1`), class win rates [game-clustered 95% interval]:

| Class | Space off | Space on |
| --- | --- | --- |
| Warrior | 0.564 | 0.547 |
| Anti-Paladin | 0.546 | 0.517 |
| Paladin | 0.541 | 0.522 |
| Barbarian | 0.533 | 0.513 |
| Archer | 0.500 | **0.624** [0.612, 0.636] |
| Assassin | 0.495 | 0.477 |
| Scout | 0.490 | 0.488 |
| Monk | 0.487 | 0.473 |
| Bard | 0.475 | 0.476 |
| Druid | 0.472 | 0.458 |
| Wizard | 0.454 | 0.464 |
| Healer | 0.445 | 0.444 |

| | Space off | Space on |
| --- | --- | --- |
| games/s, 10 cores (mixed preset) | 29.3 | 11.1 |
| deaths per minute alive: fighters / casters / battle casters / archers | 0.513 / 0.540 / 0.642 / 0.458 | 0.523 / 0.418 / 0.640 / 0.176 |
| rejoin after respawn | 20 s (by construction) | 9.7 s mean (until within 50' of an enemy) |
| annihilation game length | 662 s | 943 s |

**Reading it.**

- **Casters now die less often per minute than fighters**, as the design predicted (0.418 against
  0.523; with space off they died slightly more often).
- **class-stack falls from 0.865 to 0.634, but much of that is the archers.** In the class-stack
  games a mixed team's Archers make 12.3 kills each and die 1.4 times (Phase 1: 2.3 and 3.9). Arrows
  are 14.7% of all kills, against 1.3% in Phase 1. Their 15 m standoff keeps fighters off them, and
  stage 1's flat hit chance holds out to 30 m. As a sensitivity check (not a change), the same
  games give 0.734 with half the arrow hit chance and 0.783 with a 15 m bow range. Stage 2's
  distance curve is what will settle this.
- **Caster classes' win rates hardly move** in the mixed preset (Healer 0.445 → 0.444, Wizard
  0.454 → 0.464, Druid 0.472 → 0.458, Bard 0.475 → 0.476). The fighters' loss goes to the Archers.
  Casters survive more but kill no more: they hold back to keep their distance, and range now fails
  at completion when targets move (Entangle 15%, Hold Person 19%, Insult 22%, Fireball 15%,
  Force Bolt 3%). Most of their value still sits
  in a score calibrated without the map.
- **Rejoin is shorter than Phase 1's 20 s**, because it is measured until a player is within 50'
  of an enemy, and fights drift toward a losing team's base. On an empty field it grows with length:
  5.0, 12.5 and 19.5 s on 40, 60 and 80 m fields (the test's setup).
- **control-scales passes only within tolerance.** Removing one side's control abilities now
  slightly helps that side (−0.012 small, −0.030 large). The control spells are priced and chosen as
  in Phase 1, and they now fail out of range when targets move.

## Caster doctrines

Casters don't build spell lists from whatever scores well alone. They build to a plan, and much of a
caster's list exists to help fighters: Enchantments that arm or armor teammates, and control that
locks an enemy down for a teammate to kill. `data/doctrines.json` writes those plans down: per Magic
User class, doctrines with a **stance** (offense, control, support, sustain, hybrid), a **play
style**, an ordered **core** list, **prefer** and **avoid** lists, set-up-and-finish **combos**, and
**shares**. Everything in it beyond slugs, costs and Archetype rules is an assumption about real
players, the shares especially. `rules/doctrines.py` loads and validates it (`python -m
sim.rules.doctrines`; `tests/sim/test_doctrines.py`).

**Buying** (`policies/buy.py`):

1. Below 6th level a caster draws a base doctrine by `share`. At 6th level each Archetype doctrine
   is drawn by its `share_at_6` (0.4 in total per class) and the rest draw a base doctrine by
   `share`. Magic Users no longer compare builds under every Archetype: the doctrine's Archetype
   is the one they take.
2. The Archetype first; then each core entry in order, up to its listed copies, skipping entries
   above the player's level, forbidden by the Archetype or ablated (their points go to the fill).
   Core entries are bought even where the engine models nothing about them (a weapon, Ambulant):
   the plan pays for them.
3. Then the fill, as before (free spells, favorites, greedy by score per point), with the score
   multiplied by `DOCTRINE_WEIGHTS`: ×1.6 for a preferred or core spell, ×0.25 for an avoided one,
   ×1.25 when the spell's metadata roles match the stance (`STANCE_ROLES`). Taste stays, at half the
   spread for core spells, and a player skips a core entry whose taste is in their bottom 10%, so
   builds still vary.

Every draw happens in a fixed order whatever is ablated (the doctrine draw replaced the old
consider-an-Archetype draw), so paired ablations stay aligned. The Player records `doctrine`, `play`
and `combos`; the `players` table stores `doctrine`, `play` and `bought`.

**Play styles** (`policies/__init__.py`, `PLAY_ROUTINES`):

| Play | What the caster does |
| --- | --- |
| striker | Stays back: self-buffs, finishers, its own combo set-ups, then offense; support last |
| controller | Finishers, then locks down the enemy most dangerous to a teammate: one engaged with an ally first, then the one with most kill potential (role, skill, kills so far) in range; skips enemies already locked down (Stunned, Frozen, Stopped, Insubstantial, or already under what the spell does) or immune; Suppresses only casters. Kills only when nothing needs locking down |
| enchanter | Enchants out-of-melee teammates on the field every free moment, refills their uses, then revives, heals, cleanses; casts at enemies last |
| medic | The old support routine: revive, heal, cleanse from behind the line |
| battle | Starts melee like a fighter (`Game._engage`), isn't treated as backline, keeps self-buffs up, casts only when free |
| archer | A Ranger with a bow shoots and casts between shots; without a bow, a striker |

Every Magic User places Enchantments by benefit, at base and on the field: weapon Enchantments
(Flame Blade, Poison, Contagion) to the best melee fighter, armor and protection to the front line.
An Enchantment that gives a teammate nothing, or whose drawbacks cost that teammate more than it
gives, goes to someone else (`_crippled`, priced with both kits). Enablers (extra slots, grant
Enchantments, Undead Minion, refills) go where their situational utility is highest, in every play
style (see "Deciding casts by situational utility"). A caster
holding a **finisher** (Dragged Below on a Stopped target, Shatter on a Frozen one, Dimensional Rift
on an Insubstantial one, any wound on a Fragile one) uses it first, preferring a target whose State
it applied itself (`Player.state_src`).

**Credit for helping** (`players` table, `Game._credit_assists`):

- **enchant assists**: kills made by a teammate while wearing an Enchantment this player cast
- **control assists**: a teammate's kill of an enemy who was under a State this player applied
  (Stunned, Frozen, Stopped, Suppressed, Fragile, Insubstantial) or an Awe, Terror or Insult
  restriction from them, at the moment of death or within the 10 s before it (the engine records
  who controls whom every tick). The caster's own kill is not an assist.
- **saves**: a teammate's death prevented (Phoenix Tears, Troll Blood, Song of Survival), a revive,
  or a heal that removed a wound from a teammate (a Resurrect's revive and heal count once).
  Healing yourself is not a save.

These are attribution, not cause: a Barkskin on a fighter earns an enchant assist for every kill
that fighter makes, whether or not the Barkskin mattered. `python -m sim.analyze.doctrines` reports
per class and doctrine the share of players, win rate (game-clustered interval), own kills, enchant
assists, control assists and saves per life, the assist share and the most-bought spells, for all
levels and for 6th level alone; it writes `sim/out/doctrines.json`, which `reports/build_report.py`
turns into a section of the report.

**Results, 2,000 mixed games (`--seed 1`).** Win rate [game-clustered 95% interval], per life:

| Class | Doctrine | Stance | Share | Win rate | Kills | Ench. assists | Ctrl assists | Saves | Assist share |
| --- | --- | --- | --: | --- | --: | --: | --: | --: | --: |
| Wizard | artillery | offense | 33% | 0.479 [0.453, 0.504] | 0.65 | 0.00 | 0.09 | 0.00 | 12% |
| Wizard | lockdown-killer | offense | 24% | 0.455 [0.425, 0.486] | 0.61 | 0.01 | 0.22 | 0.00 | 28% |
| Wizard | controller | control | 28% | 0.430 [0.402, 0.459] | 0.28 | 0.03 | 0.27 | 0.00 | 52% |
| Wizard | armorer | support | 9% | 0.419 [0.368, 0.470] | 0.38 | 0.44 | 0.08 | 0.00 | 58% |
| Wizard | battlemage (6th) | offense | 2% | 0.545 [0.436, 0.654] | 0.97 | 0.00 | 0.38 | 0.01 | 28% |
| Wizard | evoker (6th) | offense | 1.5% | 0.424 [0.304, 0.544] | 0.77 | 0.45 | 0.21 | 0.00 | 46% |
| Wizard | warlock (6th) | offense | 2% | 0.439 [0.342, 0.536] | 0.65 | 0.38 | 0.35 | 0.00 | 53% |
| Healer | medic | sustain | 39% | 0.449 [0.425, 0.472] | 0.07 | 1.28 | 0.06 | 0.68 | 95% |
| Healer | protector | support | 28% | 0.434 [0.406, 0.463] | 0.06 | 2.95 | 0.03 | 0.51 | 98% |
| Healer | battle-healer | hybrid | 27% | 0.451 [0.422, 0.480] | 0.36 | 0.46 | 0.11 | 0.29 | 62% |
| Healer | warder (6th) | support | 2% | 0.469 [0.360, 0.578] | 0.05 | 6.49 | 0.00 | 0.81 | 99% |
| Healer | priest (6th) | sustain | 2% | 0.404 [0.306, 0.503] | 0.05 | 2.03 | 0.11 | 1.76 | 98% |
| Healer | necromancer (6th) | sustain | 1% | 0.426 [0.283, 0.568] | 0.05 | 0.16 | 0.08 | 1.32 | 83% |
| Druid | enchanter | support | 38% | 0.467 [0.443, 0.491] | 0.15 | 4.27 | 0.12 | 0.19 | 97% |
| Druid | elementalist | control | 32% | 0.467 [0.441, 0.493] | 0.10 | 2.59 | 0.30 | 0.12 | 97% |
| Druid | battle-druid | hybrid | 24% | 0.436 [0.405, 0.466] | 0.35 | 0.96 | 0.08 | 0.10 | 75% |
| Druid | summoner (6th) | support | 2% | 0.500 [0.387, 0.613] | 0.14 | 9.36 | 0.05 | 1.42 | 99% |
| Druid | avatar-of-nature (6th) | hybrid | 2% | 0.467 [0.366, 0.569] | 0.84 | 1.64 | 0.06 | 0.42 | 67% |
| Druid | ranger (6th) | offense | 1.6% | 0.516 [0.392, 0.639] | 1.07 | 2.34 | 0.30 | 0.23 | 71% |
| Bard | controller | control | 34% | 0.470 [0.444, 0.496] | 0.06 | 0.12 | 0.36 | 0.00 | 89% |
| Bard | force-multiplier | support | 28% | 0.431 [0.402, 0.460] | 0.07 | 0.31 | 0.10 | 0.00 | 86% |
| Bard | skald | hybrid | 32% | 0.487 [0.461, 0.512] | 0.62 | 0.10 | 0.12 | 0.00 | 26% |
| Bard | combat-caster (6th) | hybrid | 2% | 0.545 [0.447, 0.644] | 0.94 | 0.35 | 0.45 | 0.00 | 46% |
| Bard | dervish (6th) | control | 2% | 0.538 [0.435, 0.642] | 0.07 | 0.28 | 0.78 | 0.00 | 94% |
| Bard | legend (6th) | control | 1.6% | 0.478 [0.359, 0.596] | 0.08 | 0.19 | 0.73 | 0.00 | 92% |

- **Support and control against offense.** Wizards are the only class with offense doctrines, and
  there the control and support doctrines win less (controller 0.430, armorer 0.419) than artillery
  (0.479), with a half or less of its own kills. In the other classes, control and support
  doctrines win as often as the rest with almost no kills of their own: the Druid enchanter and
  elementalist (0.467 each) beat the battle druid (0.436), and the Bard controller (0.470) is level
  with the skald (0.487); only the Bard force multiplier (0.431) lags. Unreliable where it matters:
  with no map, a controller can't stay out of reach, and the Stopped State (Hold Person, Entangle)
  stops no one closing to melee, so Stop-based control is undervalued.
- **Assists.** Near all of the Healer, Druid and Bard support and control doctrines' part in kills
  comes through teammates (assist share 86–99%): the Druid summoner (9.4 enchant assists per life),
  Warder (6.5) and Druid enchanter (4.3) most; Dervish (0.78) and Legend (0.73) earn the most
  control assists. Offense Wizards (12–28%) and the skald (26%) mostly kill for themselves.
- **Archetypes against their base doctrines at 6th level** (`--level 6`): Dervish 0.538 vs
  controller 0.485, Summoner 0.500 vs enchanter 0.483, Warder 0.469 vs protector 0.434, Avatar of
  Nature 0.467 vs battle druid 0.384, Combat caster 0.545 vs skald 0.510, Ranger 0.516 vs
  elementalist 0.420, Battlemage 0.545 vs lockdown-killer 0.492 and artillery 0.504. Evoker (0.424)
  and Warlock (0.439), Priest (0.404) and Necromancer (0.426) do worse than artillery (0.504) and
  medic (0.440). With 50–150 player-games per Archetype doctrine every interval overlaps its
  counterpart's: a tendency, not a result.
- **Class win rates hardly move.** In the same run Healers win 0.444, Wizards 0.454, Druids 0.461
  and Bards 0.468, against 0.54–0.56 for Warriors, Paladins, Anti-Paladins and Barbarians: the
  melee-over-casters limit below is unchanged by doctrines.

## Usefulness score: enablers and drawbacks in context

`policies/value.py` gives every ability one usefulness score, benefits minus drawbacks. Direct
effects (a kill, a wound, a heal, a State on an enemy, Magic Armor) score from flat tables, now
measured in play where a calibration exists (see "Calibrating the score by measurement").
Two things changed; the module docstring has the full pricing table, with the rule text behind
each choice.

- **Enablers are valued by what they enable**, with the same function, so the value follows the
  target:
  - a grant is worth the granted ability at the granted frequency (uses count like copies,
    Unlimited ×2, a Charge +30%: the buyer's own rules in `value.frequency_factor`, which `buy.py`
    now imports)
  - a frequency change is worth the gain on the abilities it changes
  - a Charge or restore is worth the ability it refills
  - an extra Enchantment slot is worth the stacking only: the best Enchantments that could fill
    it times `stack_share` (the filler could usually have gone on another teammate; calibrated)
  - Song of Power is worth the Charge seconds it saves, at `charge_second` (calibrated, floored at
    `policy.value_per_threat_second`)
  - Extension, Swift and Persistent are worth their share of what they modify
  - strips are worth the ability times the strips

  An enabled ability counts at no less than 0. A choice between a refill and something else
  (Steal Life Essence: heal a wound *or* Charge) counts the better option only.
- **Drawbacks are priced by what the bearer actually loses**:
  - a self-imposed Stopped (a singing Bard) costs little to a backline caster and in full to a line
    fighter
  - "drop Enchantments when this ends" costs nothing at cast
  - "can't use other sources" costs the bearer's own copies
  - Undead Minion's no-respawn costs the respawn it replaces: the chance the caster doesn't raise
    the bearer before a respawn would have come, by game type
  - equipment restrictions and removed abilities cost what the player holds
- **Context** (`value.Ctx`, optional): the holder's and bearer's kits, the spent ability, the game
  type and the ablated abilities. Without it, each kit is a typical player of the role. It is
  used:
  - by the buyer (the spells bought so far; a kit-dependent spell is re-scored when its turn
    comes)
  - by `Game.value` (the player's own kit)
  - by the Enchantment-placement check (both kits)
  - by the martial Archetype choice (`archetype_gain` is the Archetype's value in the player's
    context)

  Values are memoized per rules object and context. A loop (an Enchantment filling its own slot)
  counts as nothing, and results don't depend on call order (`tests/sim/test_value.py`).

`python -m sim.analyze.value_changes` compares the score with the version before (f736d6a) and
writes `sim/out/value-changes.csv`: slug, holder role, old and new value, and the effect that moved
it most. 58 of 183 abilities changed. 23 changed sign, all from ≤ 0 to > 0. Among the spells:

- Attuned −1 → 14.5 and Essence Graft −2 → 23.1 (Druid list's best Enchantments)
- Undead Minion −3.5 → 8.0 (Raise Dead, less 2.0 for Cursed and 2.5 for the respawn)
- Regeneration −0.5 → 7.0 (Heal (Self) Unlimited)
- Song of Power −3.5 → 4.6
- Silver Tongue −0.5 → 2.9 and Amplification −0.5 → 2.4

The rest are Archetypes. The biggest moves, apart from Archetypes, are Void Touched 4 → 17.3
(Steal Life Essence Unlimited), Mass Healing 8.5 → 18.3 (Heal ×5 strips), Gift of Water
2.5 → 10, Troll Blood 8 → 14.5 and Rogue 2 → 10 (a use of Coup de Grace). Steal Life Essence falls
from 8 to 6 (its heal and Charge are one choice). Fireball, Heal, Raise Dead, Lightning Bolt and
the other direct scores are unchanged.

**Effect in 2,000 mixed games (`--seed 1`)**, against the same run before:

- **Newly cast:** Amplification (772 casts), Regeneration (1,448), Undead Minion (327) and
  Silver Tongue (262), all bought before but never cast. Momentum went from 5 casts to 1,295,
  through the Archetype picks below. No ability is newly bought; none stopped being cast.
- **Bought more:**
  - Gift of Water 240 → 1,116 players and Regeneration 158 → 876
  - Essence Graft 99 → 472 (casts 223 → 1,733) and Void Touched 135 → 414
  - Song of Power 456 → 997, Swift 494 → 778 and Restoration 508 → 877
- **Bought less:** Innate 1,944 → 1,609 (still never cast) and Teleport 2,858 → 2,539.
- **Win rates:**
  - Doctrine shares are identical (the doctrine draw is unchanged).
  - Every doctrine's new interval overlaps its old one. Only Healer protector ends just below
    its old interval: 0.450 → 0.420 [0.392, 0.448], against [0.421, 0.478] before.
  - The largest moves are on 30–70 players: Legend 0.597 → 0.493, Necromancer 0.489 → 0.426,
    Dervish 0.495 → 0.549. Bard skald went 0.466 → 0.481.
  - Enchant assists rose where the new Enchantments are cast: Wizard warlock 0.37 → 1.19, evoker
    0.30 → 1.20 and controller 0.03 → 0.20 per life, mostly Void Touched; Necromancer
    0.40 → 1.09.
  - Class win rates moved by at most 0.012 (Barbarian 0.544 → 0.532).
- **Martial Archetypes changed** (6th-level players who consider one, 400 per class):
  - Barbarian Berserker 54 → 245 (Momentum Unlimited now refills Rage and Brutal Strike)
  - Warrior Juggernaut 0 → 239 and Marauder 78 → 1 (Phoenix Tears 3/Refresh counts three uses)
  - Anti-Paladin Corruptor 0 → 106 (Infernal 229 → 123)
  - Monk Medium 48 → 120 (Mystic 189 → 117)
  - Scout Hunter 45 → 0 (it removes Release and Evolution, now priced by what the Scout holds)
- **One policy fix:** the revive routine now honors a granted revive's only target (Undead
  Minion's Raise Dead may only be cast on its bearer) and checks requirements with the use. Before,
  it drew a random dead ally for every revive.

## Calibrating the score by measurement

The flat weights under the score (a kill 10, a heal 4, 2 per point of armor, a State 3–6) were set by
hand, and the compositional enabler values inherit whatever they get wrong. `analyze/calibrate.py`
measures them in play instead, and `policies/value.py` uses the measured weights
(`policies/calibration.py` builds the tables).

**Method.**

- **Paired gifts.** Each anchor is given to team 0 (`engine/gifts.py`) and team 0's result (win 1,
  draw 0.5, loss 0) is compared with the same seed without the gift. A gift draws from its own random
  stream (`random.Random(f"{seed}:gift:{i}")`), so both games of a pair share the scenario, every
  loadout and the play until the gift first matters. Magic Users have already bought, so a gift
  changes no purchase.
- **Recipients.** Half of the eligible players of team 0 get the gift (at least one; a State: that
  many 30 s applications on random enemies), and the change is reported per unit: per recipient,
  per point, per application. A gift to one player of a 30-player team moves the result by
  thousandths, below what any affordable run resolves. A pilot in small annihilation games gave the
  same per-unit value for one recipient and for every eligible one, within the intervals (Finger of
  Death 0.015 ± 0.014 and 0.025 ± 0.004; a point of armor 0.028 ± 0.013 and 0.031 ± 0.006).
- **Contexts.** Six: the small, mixed and large presets, each as annihilation and as attrition.
  The game counts per context are in `CONTEXTS`: 6,000 / 4,500 small, 2,250 / 1,500 mixed, 900 / 450
  large.
- **Scale.** One reference converts win change to score: a Finger of Death per life (a 20' Verbal
  whose only effect is `death.cause`) = 10, its hand weight. The pooled score is the ratio of the
  per-unit changes summed over the six contexts; intervals are percentile intervals from resampling
  seeds within each context, jointly for every anchor, so the reference's own noise is in them.
- **Residuals.** Where the gift is an ability with other effects (Raise Dead's heal and drawbacks,
  the death ward's heal and Frozen), those are subtracted at the calibrated weights, so value.py
  scores that ability at what was measured.
- **Under the hand weights.** The games are played with `SIM_CALIBRATION=off`, so a measurement
  doesn't depend on the previous calibration. (It isn't iterated to a fixed point; see Known
  limitations.)

**Rerunning.** `python -m sim.analyze.calibrate` plays 374,400 games: 148 minutes on 10 cores. It
writes `sim/data/value-calibration.json` and keeps every pair in
`sim/out/calibration-raw.json.gz`, so `--from-raw` re-summarizes without playing (seconds).
`--scale 0.1` is a quick look; `--contexts` and `--anchors` pick subsets; `--dry-run` estimates the
time. The file records the SHA-256 of `data/assumptions.json` and `sim.engine.ENGINE_VERSION`
(bump it for any change that alters play). If either has changed, importing value.py raises
`StaleCalibration`. Rerun the calibration, or set `SIM_CALIBRATION=stale-ok` (use it anyway, with
a warning) or `SIM_CALIBRATION=off` (hand weights). With no file, value.py warns and uses the hand
weights. `--assume` and `--set` overrides at run time don't trigger the check.

**Map flags.** Phase 1 has no map, so any value that comes from position is undervalued here, and
because casters can't keep distance, melee is overvalued. Each anchor carries a flag, used when
the weights are built:

- `fair`: the measurement stands.
- `may-overstate`: it wins melee, which decides more games here than on a field with room to kite.
  Used as measured, because armor at 2 per point is plainly wrong in any case; see Known
  limitations.
- `may-understate`: the calibrated weight is used only above the hand weight, a floor. This
  applies to Frozen and Insubstantial (Phase 1 counts time out of the fight, not ground left open),
  to a second of Charge saved (a player Charges behind the line on a field; here fighters Charge
  only in a lull), and to Heal and a wound. Most of a wound's cost in play is mobility: a leg wound
  means kneeling, and Phase 1 has none of that (Known limitations: "Wounds cost little"). Heal and
  the wound ball were given this flag after the results were in (both measured near zero). The
  reason is recorded in each anchor's `why`.
- `needs-map`: the measurement is kept, but the hand weight is used, "uncalibrated, needs map". This
  applies to Stopped, which does nothing at all without a map. I chose this over a floor so that
  the file doesn't imply a measurement of something the engine can't express.

A calibrated per-use weight never goes below 0.5 (`calibration.MIN_WEIGHT`, the unpriced weight):
at or below zero, every ability with that effect would be worthless, and no policy casts an
ability worth nothing.

**Results** (`python -m sim.analyze.calibrate --report sim/data/value-calibration.json` prints the
per-context scores too):

| Anchor (unit) | Per unit, pooled [95%] | Score [95%] | Map flag | Weight: hand → in use (source) |
| --- | --: | --: | --- | --- |
| kill (a use of Finger of Death per life) | +0.0135 [+0.0122, +0.0148] | 10.00 [10.00, 10.00] | fair | `kind.death.cause` 10 → 10 (calibrated) |
| armor (a point of armor on every location) | +0.0240 [+0.0220, +0.0258] | 17.74 [16.22, 19.43] | may-overstate | `scalar.armor_point` 2 → 17.74 (calibrated) |
| armor-3-bare (a point of armor, 0 to 3 for a fighter wearing none) | +0.0290 [+0.0265, +0.0315] | 21.47 [19.45, 23.60] | may-overstate | `scalar.armor_loss_point` 2 → 21.47 (calibrated) |
| magic-armor (Magic Armor 1 on a fighter, every life) | +0.0217 [+0.0198, +0.0235] | 16.05 [14.60, 17.68] | may-overstate | `scalar.magic_armor_point` 2 → 16.05 (calibrated) |
| shield-small (a small shield) | +0.0043 [+0.0023, +0.0062] | 3.17 [1.73, 4.53] | may-overstate | `equipment.small-shield` 2 → 3.17 (calibrated) |
| shield-medium (a medium shield) | +0.0092 [+0.0070, +0.0113] | 6.80 [5.42, 8.17] | may-overstate | `equipment.medium-shield` 3 → 6.8 (calibrated) |
| shield-large (a large shield) | +0.0152 [+0.0130, +0.0173] | 11.21 [9.89, 12.71] | may-overstate | `equipment.large-shield` 3.5 → 11.21 (calibrated) |
| heal (a Heal per life) | -0.0004 [-0.0014, +0.0005] | -0.32 [-1.08, 0.36] | may-understate | `kind.wound.heal` 4 → 4 (hand (floor)) |
| heal-fighter (a Heal per life held by a fighter) | -0.0022 [-0.0038, -0.0006] | -1.62 [-2.91, -0.42] | fair | `scalar.fighter_heal` — → 0.5 (calibrated (at the minimum)) |
| revive (a Raise Dead per refresh (per game in annihilation)) | +0.0033 [+0.0022, +0.0045] | 2.47 [1.68, 3.23] | fair | `kind.life.revive` 9 → 3.24 (calibrated; residual -0.77) |
| death-ward (one death prevented per life (Phoenix Tears' way)) | +0.0105 [+0.0093, +0.0117] | 7.79 [6.92, 8.69] | fair | `kind.death.prevent` 7 → 8.01 (calibrated; residual -0.22) |
| wound-ball (a Force Bolt per life) | +0.0023 [+0.0011, +0.0035] | 1.72 [0.86, 2.51] | may-understate | `kind.wound.inflict` 5 → 5 (hand (floor)) |
| state-stunned (stunned for 30 s on a random enemy) | +0.0053 [+0.0041, +0.0064] | 3.91 [3.14, 4.65] | fair | `state.stunned` 6 → 3.91 (calibrated) |
| state-frozen (frozen for 30 s on a random enemy) | +0.0064 [+0.0053, +0.0075] | 4.72 [3.99, 5.47] | may-understate | `state.frozen` 4 → 4.72 (calibrated (floor)) |
| state-stopped (stopped for 30 s on a random enemy) | +0.0005 [-0.0004, +0.0015] | 0.40 [-0.27, 1.06] | needs-map | `state.stopped` 4 → 4 (hand (needs map)) |
| state-suppressed (suppressed for 30 s on a random enemy) | +0.0010 [+0.0000, +0.0020] | 0.77 [0.01, 1.47] | fair | `state.suppressed` 3 → 0.77 (calibrated) |
| state-fragile (fragile for 30 s on a random enemy) | +0.0012 [+0.0001, +0.0022] | 0.86 [0.09, 1.62] | fair | `state.fragile` 4 → 0.86 (calibrated) |
| state-insubstantial (insubstantial for 30 s on a random enemy) | +0.0042 [+0.0031, +0.0053] | 3.12 [2.36, 3.85] | may-understate | `state.insubstantial` 3 → 3.12 (calibrated (floor)) |
| armor-breaking (Armor Breaking on a fighter's weapon, every life) | +0.0208 [+0.0188, +0.0228] | 15.34 [13.91, 16.90] | may-overstate | `special.armor-breaking` 2 → 15.34 (calibrated) |
| wounds-kill (Wounds Kill on a fighter's weapon, every life) | +0.0085 [+0.0067, +0.0103] | 6.29 [5.13, 7.50] | may-overstate | `special.wounds-kill` 6 → 6.29 (calibrated) |
| free-charge (an instant Charge of a spent chargeable ability) | +0.0006 [+0.0000, +0.0012] | 0.47 [0.03, 0.87] | fair | `factor.refill_factor` 1 → 0.12 (calibrated) |
| charge-time (a second of Charge incantation saved) | +0.0000 [-0.0000, +0.0001] | 0.03 [-0.03, 0.08] | may-understate | `scalar.charge_second` — → 0.5 (calibrated (floor)) |
| extra-slot (an extra Enchantment slot on a fighter) | +0.0004 [-0.0010, +0.0018] | 0.31 [-0.79, 1.32] | fair | `factor.stack_share` 0.5 → 0.025 (calibrated) |

- **Armor is worth far more than 2 per point.** A point of worn armor on a fighter scores 17.7,
  nearly two Finger of Death uses per life. Taking 3 points from a fighter costs 21.5 per point.
  Magic Armor scores 16.1, and Armor Breaking on a weapon 15.3. A large shield scores 11.2. Wounds
  Kill on a weapon (6.3) is worth less than Armor Breaking, because armor absorbs the blows that
  would wound.
- **States are worth less, except Frozen and Insubstantial.** Stunned scores 3.9 (hand 6),
  Suppressed 0.8 and Fragile 0.9. Frozen (4.7) and Insubstantial (3.1) measure above their hand
  weights, most of all in large annihilation games (15.3 and 12.4 there).
- **Revives and death prevention.** A Raise Dead scores 2.5, and `life.revive` 3.2 once its
  drawbacks are added back. A death prevented scores 7.8 (weight 8.0).
- **Heal is worth nothing measurable here** (−0.3 [−1.1, 0.4]), and in a fighter's hands it is
  slightly harmful (−1.6 [−2.9, −0.4]): a fighter holding a Heal spends free seconds healing
  teammates' limb wounds, which the engine prices at almost nothing. This isn't caused by the
  step-back policy below: with it switched off, the fighter's Heal measures −0.0044 against
  −0.0061 per unit in small annihilation, the same within noise.
- **Enabler factors.** An extra Enchantment slot on a fighter measures 0.3 [−0.8, 1.3], so an extra
  slot adds 0.025 of its filler's value (`stack_share`; hand 0.5). An instant Charge per life is
  worth 0.12 of the ability it refills (`refill_factor`): Momentum Unlimited falls from 8.3 to 1.7.
  A second of Charge saved measures 0.03, below the floor of 0.5.

**Changes in the score** (before this round → now, typical holder):

- Barkskin 2 → 16.1, Stoneskin 7 → 35.1, Flame Blade 9.5 → 22.8.
- Gift of Water 10 → 24.1 on a caster, 10 → 17.0 on a fighter (its Heal is worth 1 to a fighter).
- Regeneration 7 → 0 on a fighter, 7 on a caster.
- Stun 6 → 3.9, Iceball 4 → 4.7.
- Attuned 14.5 → 0.9 and Essence Graft 23.1 → 0.8. With the stacking share at its hand value
  (0.5) they were 7.3 and 11.1.
- Berserker for a Barbarian in 3 points of armor: its armor cost goes from 6 to 64.4, and
  Momentum Unlimited for a typical fighter from 8.3 to 1.7. The
direct offense scores keep their hand weights: `death.cause` is the reference and a wound is
floored, so Fireball, Lightning Bolt and Finger of Death score as before.
`python -m sim.analyze.calibrate --weights` lists every weight with its source. `value.breakdown`
labels each direct contribution `[calibrated]`, `[hand]`, `[hand (floor)]` and so on.

**Two symptoms.**

- **Barbarians and Berserker.** Berserker's "may not wear armor" now costs 21.5 per point, and
  Momentum is worth 0.12 of what it refills. Among 6th-level Barbarians in 2,000 mixed games
  (`--seed 1`), none takes Berserker, against 347 of 608 before. None takes Raider either: Raider
  was never chosen.
- **Unlimited self-Heal for fighters.** Instrumented casts per bearer-life of the Heal (Self)
  Unlimited that Gift of Water and Regeneration grant: 0.02 for fighters before, against 0.00–0.10
  for other roles. Wounds are taken in melee and a fighter stays engaged, so a wounded fighter was
  almost never free. The policy fix is real play: a wounded fighter or battle caster who holds a
  heal they can cast on themselves, and whom nobody is attacking, steps back out of melee and heals
  (`policies._try_step_back_heal`; tests in `test_policies.py`). That raised the fighters' use to
  0.04 (Gift of Water) and 0.08 (Regeneration). A fighter who is under attack can't step away in
  Phase 1, so the use stays low. The valuation then prices a fighter's Heal by that use:
  `scalar.fighter_heal` is measured (at its minimum, 0.5), so Gift of Water's Heal on a fighter is
  worth 1 rather than 8, and Regeneration (0 to a fighter now) goes to others. With the calibrated weights, fighters
  wearing Gift of Water heal themselves 0.05 times per life.

**Effect in play.**

- **Validity.** **level passes**: 0.642 over its 600 games. Over 3,000 games of the check's kind it
  is 0.646 with the calibrated weights, 0.524 with the hand weights plus this round's policy and
  extra-slot changes, and 0.511 at 31c27ac (standard error about 0.009). So the calibration itself
  carries the recovery. The other checks are unchanged in outcome: class-stack still fails as a
  known limit (0.875).
- **Martial Archetypes** (6th-level players, 2,000 mixed games, loadouts only):
  - Barbarian: Berserker 347 → 0.
  - Warrior: Juggernaut 345 → 348, Marauder 3 → 0.
  - Anti-Paladin: Corruptor 135 → 96, Infernal 206 → 245.
  - Monk: Medium 188 → 24, Mystic 170 → 334.
  - Archer: Artificer 381 → 386, Sniper 5 → 0.
  - Assassin Rogue (379) is unchanged; no Paladin or Scout takes one.
- **Doctrines** (`sim.analyze.doctrines`, run ea1552045998 against ff99269a8349):
  - Every doctrine's new interval overlaps its old one.
  - Up: Druid elementalist 0.450 → 0.502, battle druid 0.423 → 0.458, Wizard controller
    0.429 → 0.458, Healer protector 0.420 → 0.446, Bard force multiplier 0.443 → 0.467.
  - Down: Healer warder 0.506 → 0.420, priest 0.479 → 0.415, Wizard evoker 0.500 → 0.441,
    Bard dervish 0.549 → 0.473. These are 30–50-player samples.
  - Enchant assists rose where armor Enchantments are cast: Druid elementalist 2.58 → 3.77 per
    life, Ranger 2.70 → 5.24.
- **Class win rates:** Druids 0.452 → 0.477, Warriors 0.572 → 0.556; every other class moved by at
  most 0.011.
- **Buying and casting:**
  - Bought more: Song of Battle 1,102 → 2,517 players, Armor (1 point) 394 → 1,593, Gift of Earth
    1,208 → 2,333, Barkskin 2,885 → 3,707, Stoneskin 1,514 → 2,112.
  - Bought less: Essence Graft 472 → 99, Discordia 734 → 222, Innate 1,609 → 1,013.
  - Casts: Iceball 9,834 → 18,218, Stoneskin 2,520 → 5,202, Steal Life Essence 72,986 → 51,706,
    Momentum 1,295 → 0.

## Deciding casts by situational utility

The fixed usefulness score in `policies/value.py` answers "is this spell good?" once, with no
context. `policies/utility.py` is the replacement pattern: a per-ability function
`(game, caster, target) -> utility` registered by slug, which answers "is casting this now, on
this player, worth it?". Bardic songs are the first abilities decided this way
(`policies/songs.py`):

- The engine follows the Chant rules: one Chant at a time; beginning any incantation (another
  spell, a Charge, a new song) ends it; death, Frozen and Stunned end it.
- Each song's utility counts the threats it answers, weighted by how likely they are to act on the
  Bard soon: armored enemies in reach (Battle), enemy Stop, Freeze and Insubstantial casters
  (Freedom), Command threats (Determination), projectiles (Deflection), being wounded or
  outnumbered (Survival), teammates Charging nearby (Power), enemy Verbal casters (Interference).
- A Bard switches only when the new song, after its silent incantation, gains at least
  `policy.song_switch_min_gain` over `policy.song_switch_horizon_seconds`. Another cast must be
  worth the song time it costs; escapes always go. A Bard turns down a teammate's Enchantment worth
  less than their song.

In 2,000 mixed games Bards start about 1.6 songs per life. By share of songs started:
Determination 37%, Battle 34%, Survival 12%, Freedom 7%, Power 6%, Deflection 5%, Interference
under 1%. No Bard doctrine's win rate moved beyond its interval.

### Enablers

The enablers are decided the same way (`policies/enablers.py`). Their utility is in value points,
the calibrated usefulness score's scale, per cast. The caster scores each candidate target,
takes the best (ties: the lowest pid) and casts when that utility beats **the time the cast costs**
(`enablers.time_cost`): the caster's best attack right now (its score per second of incantation,
times the chance a target is in range; 0 with no enemy to hit) over the incantation, plus the song
the incantation ends. At base the time costs nothing. Enchantments with a utility compete with the
caster's other Enchantments by that utility (`_try_enchant`). Refills (`_try_refill`) are now tried
in every play style and martial role, not only by enchanters: before attacks for strikers,
controllers, archers and plain casters, beside heals for medics, battle casters and fighters.

| Ability | Utility for target q |
| --- | --- |
| Empower, Confidence | `refill_worth` of q's best spent use it can refill, if q acts soon |
| Innate | the same, for the caster (it Charges only its caster, whatever range the use reads) |
| Restoration | the sum over q's spent per-life uses (a second missing use of one ability at `COPY_DECAY`), if q acts soon |
| Steal Life Essence | its Charge option: `refill_worth` of the caster's best spent chargeable use. The caster names it instead of healing a wound only when it is worth more than a heal (`wound.heal`) |
| Attuned, Essence Graft | `stack_share` (calibrated, 0.025) × the Enchantments one more slot adds for q: the fillers beyond q's free slots, from the caster (with a use left) or a teammate caster nearby (× `p_ally_nearby_for_touch`); Essence Graft counts only the caster's own and subtracts q's (m) Enchantments from other casters, which it drops. 0 if q has an extra slot already |
| Amplification, Silver Tongue | the Enchantment's score to q over q's abilities that still have a use (20' Verbals for Extension; Touch, Other, Self and Magic Ball abilities for Swift) |
| Regeneration, Gift of Water, Battlefield Triage | the Enchantment's score to q, with its Heal priced as a fighter's (calibrated `fighter_heal`) if q fights in the line: a fighter under attack rarely heals |
| Undead Minion | q's expected deaths while the caster lives (their death rates' ratio, capped by q's lives and the time left) × (the caster's Raise Dead × `p_ally_nearby_for_touch` − the respawn it replaces, `value.late_share`), less Cursed once. 0 once the caster has its three |
| Discordia, Snaring Vines | the stripped spell's score × its expected casts: the strips, or fewer when fewer enemies it can hit are expected in its range (living, on the field or coming back; for Break Concentration only enemies who cast), less the song the Enchantment keeps off the Bard's slot for the song horizon. Hold Person keeps the hand Stopped weight (needs a map) |

Shared helpers: `acts_soon(q)` is 1 for a player who is alive, has lives left, is on the field (at
base counts for Enchantments) and is not Frozen, Stunned, Insubstantial or Invulnerable (or, for a
magical ability, Suppressed), else 0. So no refill goes to a dead, respawning or locked-down
teammate. `refill_worth(u, q)` is u's score in q's kit, the value of what is refilled (value.py's
refill with `Ctx.spent`), times the calibrated `refill_factor` (0.12) for an instant Charge.
`ench_worth` is an Enchantment's score with the caster's and the bearer's kits, as `_crippled`
prices it. Death rates start from a hand-set prior (`DEATH_PRIOR`: one death per 120 s for a player
in the line, half that behind it) and move with the deaths seen. No utility draws from the game's
random stream. Refills also skip teammates who would shrug them off (Void Touched, Rage: `_resists`).

**Engine hook.** The rules have the caster name the ability a refill acts on ("by stating its
name", Innate, Steal Life Essence). `Game.name_refill(caster, ability, recipient)` asks the policy
(`enablers.name_refill`: the spent use worth most to the recipient) when the refill resolves. The
Charge handler Charges that use; the restore handler gives back one use of it for Empower ("regains
one use of any per-life ability"; before, it restored every per-life use) and, for Restoration,
every per-life use except Empower, Confidence and Restoration, which both abilities' Limitations
exclude. For a refill offered as a choice beside a heal (Steal Life Essence),
`Game.apply_effects` skips the heal when the caster names an ability. Momentum and the calibration's
free Charge pick as before (the most valuable spent use).

**Casts per holder-life, 2,000 mixed games (`--seed 1`)**, before (run fa2aeeb5bbe6) and after
(8cb2b4f6de48). Holders are the Magic Users who bought the spell and the martial players whose class
gives it at their level:

| Ability | Holders | Casts before | per life | Casts after | per life |
| --- | --: | --: | --: | --: | --: |
| Empower | 1,327 | 1,972 | 0.26 | 3,809 | 0.50 |
| Restoration | 890 | 864 | 0.17 | 1,761 | 0.35 |
| Confidence | 1,224 | 3,899 | 0.55 | 4,485 | 0.63 |
| Innate | 1,594 | 0 | 0 | 1,801 | 0.19 |
| Steal Life Essence (Charges made) | 3,030 | 51,706 (39,547) | 3.06 | 49,029 (38,460) | 2.92 |
| Attuned | 775 | 1,175 | 0.26 | 911 | 0.20 |
| Essence Graft | 99 | 226 | 0.37 | 172 | 0.30 |
| Amplification | 530 | 757 | 0.26 | 759 | 0.25 |
| Silver Tongue | 162 | 252 | 0.26 | 250 | 0.27 |
| Battlefield Triage | 1,907 | 2,626 | 0.24 | 2,617 | 0.24 |
| Regeneration | 544 | 614 | 0.19 | 591 | 0.19 |
| Gift of Water | 1,305 | 2,581 | 0.35 | 2,503 | 0.34 |
| Undead Minion | 124 | 225 | 0.30 | 212 | 0.29 |
| Discordia | 222 | 0 | 0 | 84 | 0.06 |
| Snaring Vines | 142 | 0 | 0 | 140 | 0.17 |

Empower now gives back one use per cast, so it is cast about twice as often. Refills that failed
on a teammate unaffected by them ("unaffected": 265 Confidence, 44 Empower, 17 Restoration) are
down to 13. The Enchantments are cast about as often as before, but on other teammates (casts in
games 1–600, by bearer; "line" is a fighter or battle-play caster):

| Ability | Line | Other casters, support, archers | Self |
| --- | --- | --- | --- |
| Gift of Water | 631 → 148 | 156 → 620 | 22 → 18 |
| Battlefield Triage | 454 → 17 | 221 → 604 | 96 → 144 |
| Regeneration | 16 → 0 | 172 → 179 | — |
| Amplification | 103 → 75 | 71 → 93 | 57 → 62 |
| Attuned | 376 → 159 | 1 → 125 | 1 → 1 |
| Essence Graft | 92 → 38 | 0 → 37 | 1 → 0 |
| Undead Minion | 44 → 68 | 27 → 5 | — |

**Doctrines** (`sim.analyze.doctrines`, run 8cb2b4f6de48 against ea1552045998, the same games as
fa2aeeb5bbe6): every doctrine's win-rate interval overlaps its old one, at all levels and at 6th.
The largest moves are on 60–370 players: Druid ranger 0.516 → 0.609, Wizard armorer
0.411 → 0.457, warlock 0.378 → 0.418, Healer warder 0.420 → 0.457, Wizard controller
0.458 → 0.429, Bard combat caster 0.586 → 0.525. Bard enchant assists fall (controller 0.19 → 0.07
per life, combat caster 0.45 → 0.13, legend 0.38 → 0.12): their Battlefield Triage now goes to
Healers, who make few kills, instead of fighters. That is attribution, not effect: the Bard win
rates moved by at most 0.03 except the combat caster's. Class win rates moved by at most 0.008.

**Validity**: the same 14 of 15 pass. level 0.642 → 0.686, class-stack (the known limit)
0.875 → 0.865, control-scales' large-game edge +0.160 → +0.090 (still passes).

**Never cast** among the purchasable spells (2,000 games), with the reason:

| Spell | Bought by | Why |
| --- | --: | --- |
| Teleport | 2,503 | needs a map: the engine applies it (Insubstantial until arrival), but where to go is the point |
| Summon Dead | 1,083 | needs a map: it moves where a dead player died |
| Stoneform | 707 | policy gap: Frozen on oneself until the caster ends it; no routine decides when to go in or come out |
| Force Barrier | 420 | policy gap: Frozen on oneself for 10 s; no routine stalls a fight that way |
| Ambulant | 155 | needs a map: casting while moving |
| Heart of the Swarm | 0 | needs a map: a respawn point and Alternate Base |
| Song of Visit | 0 | unmodeled (out of scope; its utility is 0) |

Innate, Discordia and Snaring Vines left this list. Among martial abilities, Momentum (no one takes
Berserker), Martyr, Evolution and Sacred Blades (Archetype grants nobody chose, or always-on
Traits), Sanctuary, Reload's keep-away and the Scout's Teleport (needs a map) are never cast.

**What the remaining enablers still use.** Song of Power has its song utility; Extension, Swift and
Persistent are stated by the engine at cast start; Momentum and Troll Blood trigger on their own;
Mass Healing and Corrosive Mist keep the fixed score; Heart of the Swarm is worth 0 until there is
a map.

## Known limitations (from the face-validity suite)

`sim/analyze/validity.py` runs 15 statistical checks that a veteran player would call obviously
true (mirror matches are 50/50, skill wins, armor helps, more lives means longer games, Heal
doesn't hurt, …). **class-stack** fails as a structural limit of Phase 1. **level** passes again
with the calibrated weights: 0.642 over its 600 games, 0.646 over 3,000. It was 0.567 before the
context valuation and 0.512 after it (see "Calibrating the score" and below).
**no-abilities** now passes at full scale too (0.484, the same before and after the valuation).
The side bias described below had shown 0.453.

- **Level after the context valuation.** Over 3,000 games of the check's kind, 6th-level players
  beat the same classes at 1st level 0.511 of the time with the new usefulness score, against
  0.576 before it (standard error about 0.009 each). Putting back one piece of the old scoring at
  a time:

  | Old piece restored | Level |
  | --- | --: |
  | none (the new score) | 0.511 |
  | martial Archetype choice | 0.549 |
  | Barbarians' Berserker choice only | 0.564 |
  | Magic User buying | 0.529 |
  | values in play (`Game.value`) | 0.532 |
  | all three | 0.580 |

  - Most of the fall is Barbarians taking Berserker: 245 of 400 who consider an Archetype,
    against 54 before. They give up 3 armor points for Momentum Unlimited, which the score now
    values at what it refills (see "Enabler values sit on the flat tables' scale").
  - The rest is 6th-level casters spending on and casting enablers that help little in the engine:
    Heal grants to fighters, extra slots, Amplification.
  - 1st-level players have few enablers, so the gap closes from the top.

  No weight was changed to recover it; the fix belongs to the flat weights (armor) and to
  per-cast utility for the enablers. **Resolved by measurement**: with the calibrated weights
  (armor 21.5 per point taken away, an extra slot 0.025 of its filler, an instant Charge 0.12 of
  what it refills, a fighter's Heal 0.5), no Barbarian takes Berserker and the check is at 0.646.
- **Level after doctrines.** 6th-level players now beat the same classes at 1st level 0.569 of the
  time over the check's 600 games (expects ≥ 0.6; it was 0.618). Over 3,000 games of the same kind
  it is 0.560 with doctrines and 0.589 without them (plain greedy buying and the old role play), so
  the 600-game 0.618 was partly a lucky sample, and doctrines cost about 0.03. About three quarters of
  that comes from the play styles (0.582 with doctrine buying and the old play) and a quarter from
  the buying; the Druid doctrines move it most
  (0.586 when only Druids go without doctrines), while Bard doctrines widen the gap. Neither the
  Attuned rule nor Enchantment priorities is the cause (0.553 and 0.570 without them). The reading:
  a plan helps a 1st-level caster about as much as a 6th-level one (targeted control and
  enchanting with five points), and the core lists spend 6th-level points on things the engine
  doesn't model (weapons, Ambulant, Summon Dead, extra songs). The check is left as it is.
- **No-abilities side bias.** With every ability removed, team 0 wins less than team 1 on the check's
  rosters in either order: 0.453 as listed and 0.501 for the same rosters swapped (before doctrines:
  0.475 and 0.493; other seeds 0.472, before 0.469). The mirror and seat-swap checks, with abilities,
  show no side effect. A likely cause, not verified: `Game._engage` walks players in pid order
  (team 0 first), unlike the shuffled melee and decision orders.

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
  Every caster now refills (Confidence, Empower, Restoration, Innate) by utility, and Rangers (the
  Druid ranger doctrine) shoot. Still never cast in play: Teleport, Summon Dead, Force Barrier,
  Stoneform, Reload (see "Never cast" under "Deciding casts by situational utility").
- **Doctrine entries that do nothing here.** Some core entries are bought but never used, because
  the engine or the policies don't use them:
  - Ambulant (Battlemage, Priest; needs a map)
  - the weapon purchases (battle doctrines; weapon types are out of scope)
  - Summon Dead (medic; needs a map)
  - Stoneform (battle druid; no routine goes Frozen on purpose)

  Amplification, Silver Tongue, Undead Minion and Snaring Vines used to be on this list. The usefulness score
  now values them by what they grant, in context, and they are cast (see "Usefulness score"
  above). Battle casters also keep `melee.weak_weapon_logit`, whatever weapon they bought.
- **Enabler values sit on the flat tables' scale** (before the calibration; the first three points
  below are now measured, see "Calibrating the score"). An enabler is worth what it enables, so it
  inherits every miscalibration of the direct weights:
  - Berserker trades 2 points of value per armor point for Momentum Unlimited (Momentum is worth
    the mean of the Barbarian's Rage and Brutal Strike, doubled for Unlimited). The engine makes
    armor worth far more than that (melee decides most games), and Momentum only refills after a
    kill. This is the main cost to the level check (below).
  - A Heal granted to a fighter (Regeneration, Gift of Water, Troll Blood) is valued like any
    Heal, doubled for Unlimited. In play fighters stay in melee and rarely heal themselves, and
    wounds cost little (below).
  - An extra Enchantment slot is credited with the whole value of the Enchantment that fills it,
    though that Enchantment could often have gone to another teammate: the gain is stacking, not
    the Enchantment.
  - Discordia and Snaring Vines (strips of Break Concentration and Hold Person) score higher and
    are bought more (577 → 734, 147 → 190). Until the enabler utilities, no routine cast a Self
    Enchantment aimed at enemies, and Innate was never cast.
- **What the calibration can't settle.**
  - **Melee anchors may read high.** Armor, Magic Armor, shields and weapon specials are measured
    in an engine where melee decides most games (the class-stack limit), so they may be worth less
    on a real field. They are used as measured: nothing that could be measured here suggests 2
    per point.
  - **Heal and wounds keep hand floors.** Both measured near zero, which is the "wounds cost
    little" limit, not real play. The floors keep Healers healing. They were set after the results
    were seen, and the file says so.
  - **No fixed point.** The games were played under the hand weights. Under the calibrated weights
    Magic Users buy and place differently (more armor Enchantments), which could move the anchors
    again. One more pass would show how far; it wasn't run (2.5 h).
  - **Half the team, per unit.** Values are averages over gifts to half of the eligible players,
    so they include some interaction between recipients. The pilot showed none beyond noise.
  - **Still hand-set:**
    - Great weapons for a Magic User (the engine gives a bought Great weapon no effect). A lost
      Great weapon is priced as the Armor Breaking and Shield Crushing it gives.
    - Specials on one ball or arrow.
    - Swift's seconds and the songs' exchange rate `policy.value_per_threat_second`.
    - The role multipliers, drawbacks other than armor and shields, and the frequency factors.
  - **Song decisions moved.** A Stun (3.9) no longer outweighs about 5 points of song, and Bards
    now accept armor Enchantments over a song. `test_songs.py` tests the mechanism with spells
    whose values are anchored.
  - **Noisy contexts.** Large attrition has 450 pairs. Some per-context scores there and in large
    annihilation are far from the pooled value: a death ward scores −7.7 in large annihilation
    against 7.8 pooled. Read per-context scores with `--report`, not alone.
- **Enabler utilities (`policies/enablers.py`).**
  - **The calibration predates them.** `sim.engine.ENGINE_VERSION` should be bumped for a policy
    change that alters play, and this one does; it was left at 2 because a bump makes the
    calibration stale and every run refuse to start until it is re-measured (2.5 h). The anchors
    were measured under the old enabler policy (and the hand weights); rerun the calibration and
    bump the version together.
  - **Armor Enchantments leave the front line.** Gift of Water and Battlefield Triage now go mostly
    to casters, healers and archers, whose Heal is worth more (fighters' Heal is priced at the
    calibrated `fighter_heal`, 0.5). Gift of Water's Magic Armor is priced the same on everyone
    (16 per point, measured on fighters), though a backline caster is hit far less. An exposure
    weight on armor would send it back to the line; none is measured, so none is used.
  - **Extra slots are worth almost nothing.** With `stack_share` 0.025 an Attuned is worth about
    0.3–0.9, so it waits for a moment with nothing to attack (casts 1,175 → 911), and its target is
    chosen between very small numbers: now mostly players other than fighters (376 → 159 on the
    line in 600 games).
  - **Charges and restores are priced differently.** An instant Charge is scaled by the calibrated
    `refill_factor` (0.12); a restored use (Empower, Restoration) is not calibrated and counts at
    the full value of what it restores. So Confidence and Innate often lose to an attack and
    Empower rarely does.
  - **Hand-set pieces.** The death-rate prior for Undead Minion (`DEATH_PRIOR`), the song horizon
    for what Discordia keeps off a Bard's slot, and the time cost, which counts only attacks: a
    heal or another Enchantment competes through the routine's order, not the utility.
- **A counting quirk.** Amplification's "no other source of Extension" is counted as applied each
  time the engine checks the bearer's Extension (`Game._meta_use`, every tick from
  `_offer_extension`): 146,000 times in 2,000 games. It is accounting only; play is unaffected.
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
- `space`: the field (`--space on` only; see "Phase 2: the field"): size, tick, speeds, Touch and reach, throw and bow range, deployment and base zone, line spacing and charge distance, retreat trigger, preferred distances by play style, target choice. Left out of the calibration's staleness fingerprint.

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
