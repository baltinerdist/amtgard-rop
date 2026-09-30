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
| `engine/game.py` | The one-second tick loop: engagement, melee, casting, hits, wounds, death, respawn, refresh |
| `policies/` | Scripted behavior per role (fighter / archer) and per doctrine play style (striker, controller, enchanter, medic, battle, archer), whether to keep casting under attack, the ability value score, and Magic User spell buying by doctrine (`buy.py`) |
| `scenarios/` | Player count, class and level mix, skill spread, team balancing, game type |
| `run.py` | Parallel runner and DuckDB storage |
| `analyze/stats.py` | Wilson, game-clustered (sandwich) and cluster-bootstrap intervals, paired intervals |
| `analyze/winrate.py` | Class win rates with game-clustered intervals (naive Wilson kept for comparison) |
| `analyze/doctrines.py` | Per class and doctrine: share, win rate, kills, assists and saves per life, most-bought spells |
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
| enchanter | Enchants out-of-melee teammates on the field every free moment, refills their uses (Empower, Restoration, Confidence), then revives, heals, cleanses; casts at enemies last |
| medic | The old support routine: revive, heal, cleanse from behind the line |
| battle | Starts melee like a fighter (`Game._engage`), isn't treated as backline, keeps self-buffs up, casts only when free |
| archer | A Ranger with a bow shoots and casts between shots; without a bow, a striker |

Every Magic User places Enchantments by benefit, at base and on the field: weapon Enchantments
(Flame Blade, Poison, Contagion) to the best melee fighter, armor and protection to the front line,
and Attuned or Essence Graft first on a fighter when there are Enchantments to fill the slot. An
Enchantment that gives a teammate nothing (Amplification on a player with no 20' Verbal), or whose
drawbacks cost that teammate more than it gives, goes to someone else (`_crippled`, priced with
both kits). A caster
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
effects (a kill, a wound, a heal, a State on an enemy, Magic Armor) still score from flat tables.
Two things changed; the module docstring has the full pricing table, with the rule text behind
each choice.

- **Enablers are valued by what they enable**, with the same function, so the value follows the
  target:
  - a grant is worth the granted ability at the granted frequency (uses count like copies,
    Unlimited ×2, a Charge +30%: the buyer's own rules in `value.frequency_factor`, which `buy.py`
    now imports)
  - a frequency change is worth the gain on the abilities it changes
  - a Charge or restore is worth the ability it refills
  - an extra Enchantment slot is worth the best Enchantments that could fill it
  - Song of Power is worth the Charge seconds it saves, at `policy.value_per_threat_second`
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

- **Newly cast:** Amplification (773 casts), Regeneration (1,445), Undead Minion (327) and
  Silver Tongue (262), all bought before but never cast. Momentum went from 5 casts to 1,296,
  through the Archetype picks below. No ability is newly bought; none stopped being cast.
- **Bought more:**
  - Gift of Water 240 → 1,116 players and Regeneration 158 → 876
  - Essence Graft 99 → 472 (casts 223 → 1,733) and Void Touched 135 → 414
  - Song of Power 456 → 997, Swift 494 → 778 and Restoration 508 → 877
- **Bought less:** Innate 1,944 → 1,609 (still never cast) and Teleport 2,858 → 2,539.
- **Win rates:**
  - Doctrine shares are identical (the doctrine draw is unchanged). No doctrine's win rate moved
    outside its interval.
  - The largest moves are on 30–70 players: Legend 0.597 → 0.493, Necromancer 0.489 → 0.404,
    Dervish 0.495 → 0.538. Among the base doctrines: Healer protector 0.450 → 0.422, Bard skald
    0.466 → 0.481.
  - Enchant assists rose where the new Enchantments are cast: Wizard warlock 0.37 → 1.21, evoker
    0.30 → 1.21 and controller 0.03 → 0.20 per life, mostly Void Touched; Necromancer
    0.40 → 1.08.
  - Class win rates moved by at most 0.011.
- **Martial Archetypes changed** (6th-level players who consider one, 400 per class):
  - Barbarian Berserker 54 → 245 (Momentum Unlimited now refills Rage and Brutal Strike)
  - Warrior Juggernaut 0 → 239 and Marauder 78 → 1 (Phoenix Tears 3/Refresh counts three uses)
  - Anti-Paladin Corruptor 0 → 106 (Infernal 229 → 123)
  - Monk Medium 48 → 120 (Mystic 189 → 117)
  - Scout Hunter 45 → 0 (it removes Release and Evolution, now priced by what the Scout holds)
- **One policy fix:** the revive routine now honors a granted revive's only target (Undead
  Minion's Raise Dead may only be cast on its bearer) and checks requirements with the use. Before,
  it drew a random dead ally for every revive.

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

**Where the enablers' context values plug in (next step).** The other enablers are still cast by
the fixed score, which now carries their value in the caster's context. A utility function for each
would take the same pieces from the game state instead of a typical kit:

| Enabler | Context value now (`value.py`) | What its utility function would read |
| --- | --- | --- |
| Attuned, Essence Graft | `extra_slot`: best Enchantments the caster holds | the fillers the caster has uses left for, the bearer's current Enchantments and free slots |
| Amplification, Silver Tongue | `grant` on the bearer's kit, less the "other sources" drawback | the bearer's 20' Verbals (Touch/Self/Magic Ball incantations for Swift) with uses left; the bearer's own Extension or Swift uses |
| Song of Power | `charge_faster`: a typical Charge | already `songs._power`: teammates Charging or with a spent chargeable ability within 20' |
| Undead Minion | Raise Dead grant, less `late_share(game type)` | the bearer's expected deaths, lives left, whether the caster is near enough to raise them |
| Confidence, Innate, Empower, Restoration, Momentum | `refill` with `Ctx.spent` | the target's actual spent uses (`_refill_need` already finds them); pass each as `Ctx.spent` |
| Extension, Swift, Persistent | `meta` over the holder's kit | the ability being started now (the engine applies them automatically at cast start) |
| Regeneration, Gift of Water, Troll Blood | Heal (Self) Unlimited on the bearer | the bearer's wounds and how often they are out of melee |
| Battlefield Triage, Mass Healing, Corrosive Mist, Discordia, Snaring Vines | the stripped ability × strips | the stripped ability's own utility per use |
| Heart of the Swarm | 0 (its benefits need a map) | respawn distance, once there is a map |

## Known limitations (from the face-validity suite)

`sim/analyze/validity.py` runs 15 statistical checks that a veteran player would call obviously
true (mirror matches are 50/50, skill wins, armor helps, more lives means longer games, Heal
doesn't hurt, …). **class-stack** fails as a structural limit of Phase 1. Since caster doctrines,
**level** fails (0.569; see below), and at full scale **no-abilities** fails (0.453) because of a
side bias that predates doctrines (below). At half scale (`pytest`) no-abilities passes.

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
  per-cast utility for the enablers.
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
  Enchanters now cast Confidence, Empower and Restoration, and Rangers (the Druid ranger doctrine)
  shoot. Still never cast in play: Teleport, Summon Dead, Force Barrier, Stoneform, Reload, Innate,
  and the Self-range Enchantments aimed at enemies (Discordia, Snaring Vines).
- **Doctrine entries that do nothing here.** Some core entries are bought but never used, because
  the engine or the policies don't use them:
  - Ambulant (Battlemage, Priest; needs a map)
  - the weapon purchases (battle doctrines; weapon types are out of scope)
  - Summon Dead (medic; needs a map)
  - Stoneform (battle druid)
  - Snaring Vines (elementalist)

  Amplification, Silver Tongue and Undead Minion used to be on this list. The usefulness score
  now values them by what they grant, in context, and they are cast (see "Usefulness score"
  above). Battle casters also keep `melee.weak_weapon_logit`, whatever weapon they bought.
- **Enabler values sit on the flat tables' scale.** An enabler is worth what it enables, so it
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
    are bought more (577 → 734, 147 → 190), but no routine casts a Self Enchantment aimed at
    enemies. Innate is bought by 1,609 Magic Users and never cast: no routine states a Meta-Magic
    that refills.
- **A counting quirk.** Amplification's "no other source of Extension" is counted as applied each
  time the engine checks the bearer's Extension (`Game._meta_use`, every tick from
  `_offer_extension`): 147,000 times in 2,000 games. It is accounting only; play is unaffected.
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
