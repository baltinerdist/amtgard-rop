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
Python 3.14, but **nothing uses it yet**. The pure-Python engine runs about 66 games/s on
10 cores, so no speed-up has been needed so far.

## Running

```sh
.venv/bin/python -m sim.run --games 1000                        # mixed scenarios, all cores
.venv/bin/python -m sim.run --games 500 --config small --seed 100
.venv/bin/python -m sim.run --games 1000 --ablate call-lightning   # remove an ability everywhere
.venv/bin/python -m sim.analyze.winrate                         # latest run: class win rates, balance methods
.venv/bin/python -m sim.analyze.ablation --ability heal,call-lightning --games 1000
.venv/bin/python -m sim.analyze.ablation --all --games 300 --csv sim/out/ablation.csv
.venv/bin/python -m sim.rules.build_classes                     # rebuild sim/data/classes.json
.venv/bin/python -m sim.rules.coverage                          # rebuild sim/COVERAGE.md
.venv/bin/python -m pytest tests/sim
```

Results are appended to `sim/out/runs.duckdb` (gitignored). It has four tables:

- `runs`
- `games`
- `players`
- `abilities` (casts, applied effects, no-ops, failures and kills per ability per game)

**Determinism.** The seed fixes everything about a game. The scenario, each player's loadout and
the play itself each draw from their own random stream derived from that seed. So a seed replays
exactly, including across processes and hash seeds (`tests/sim/test_determinism.py`).

**Performance.** The smoke run was 1,000 mixed games (10–40 players, average 24) in 15.1 s on
10 cores, about 66 games/s. An ablation over 1,000 games runs the baseline once, then takes about
15 s for each ability removed.

## Layout

| Path | What |
| --- | --- |
| `rules/compile.py` | Metadata + class sheets + rulings → immutable `Ability` / `ClassSheet` objects |
| `rules/build_classes.py` | Builds `data/classes.json` from `rules/classes/*.md` and the metadata's availability rows; each field cites its source file |
| `rules/rulings.py` | Loads `data/rulings.json` (answers to the metadata's 87 open questions) |
| `rules/coverage.py` | Which effect kinds the engine executes; writes `COVERAGE.md` |
| `engine/state.py` | Player, ability uses, enchantments, casts |
| `engine/loadout.py` | Equipment and abilities from class and level. Martial classes use the level table and option picks. Magic Users spend 5 points per level on the best-value spells. |
| `engine/effects.py` | One handler per effect kind, plus the passive and loadout registries |
| `engine/game.py` | The one-second tick loop: engagement, melee, casting, hits, wounds, death, respawn, refresh |
| `policies/` | Scripted behavior per role (fighter / caster / support / archer) and the ability value score |
| `scenarios/` | Player count, class and level mix, skill spread, team balancing, game type |
| `run.py` | Parallel runner and DuckDB storage |
| `analyze/` | Win rates with Wilson intervals and the paired ablation harness |

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
- **Rulings are recorded but not interpreted.** Each of the 87 open questions keeps the reading the metadata already encodes. An answer changes the simulation only if its entry carries a `sim` block (see `rules/rulings.py`). A missing, partial or unreadable `data/rulings.json` is tolerated: each open question without an entry falls back to the metadata's reading, and the fallback is logged.
- **Weapons.** There are no thrown weapons, and no backup weapons after one is destroyed.
- **Player decisions** are scripted heuristics. A different policy can change the conclusions, so run any important question at more than one policy setting.

## Assumption categories

All values are in `data/assumptions.json`, and each has a unit and a reason. Groups:

- `time`: tick length, speech rate
- `skill`: skill spread and effect size
- `melee`: base hit rate, shield, gang, wound, stunned and weak-weapon modifiers; hit-location weights; Great-weapon and shield use
- `engagement`: how fast melee pairs form and break; backline protection; target preference
- `range`: chance a target is in range
- `casting`: interrupts; casting while engaged
- `projectiles`: hit chances, shot time, ball retrieval
- `respawn`: rejoin time, pregame prep
- `loadout`: Look The Part, Archetype and armor-wearing shares; spell copy cap
- `policy`: revive priority, offense and charge rates, self-Insubstantial and forced-move durations
- `game`: time cap
- `population`: class and level mix. These are placeholders until ORK attendance data is available.

## Reading results

- **Player-level win rates** treat players in the same game as independent. The intervals are too narrow, so use them for ranking.
- **Team- and game-level measures** don't have that problem.
- **Ablation** compares the holder team's result with and without the ability, over the same seeds.
  - Paired seeds align the rosters, but play diverges once the ability would have mattered. That adds noise, not bias.
  - For Magic Users, the points freed by an ablated spell are re-spent. That's how a real player would respond.

**Early result:** removing Heal raised the holder team's win chance slightly (+0.03). In this model
a Heal takes 16 s (8 words × 5), and during that time the caster isn't fighting. That says as much
about the time and interrupt assumptions as about Heal.
