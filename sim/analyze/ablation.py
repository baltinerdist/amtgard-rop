"""Paired ablation: remove abilities from every loadout and replay the same seeds.

    .venv/bin/python -m sim.analyze.ablation --ability call-lightning --games 2000
    .venv/bin/python -m sim.analyze.ablation --ability heal,mend --together --games 1000   # one set
    .venv/bin/python -m sim.analyze.ablation --merge icy-blast:iceball --games 1000       # B:A substitution
    .venv/bin/python -m sim.analyze.ablation --all --games 300 --csv sim/out/ablation.csv

Common random numbers: each seed fixes the scenario (players, levels, skill, teams) and every
player's loadout draws, so baseline and ablated games start from the same rosters. The play
itself uses one random stream, so once the removed ability would have been used the two games
diverge; that adds noise but no bias.

Measures (see sim/analyze/impact.py for definitions):
- holder-team win change: holder result without the ability - with it (win 1, draw 0.5, loss 0),
  over games where one team holds more copies, with a **paired-by-seed** 95% interval.
- gameplay change distance D (weighted RMS of six standardised components: holder win, game
  length, time dead, kills per player, class win-rate spread, ability-use mix), with a paired
  bootstrap interval, its noise floor, and the bias-corrected `distance_adj`.
"""
from __future__ import annotations

import argparse
import csv

from sim.analyze.impact import compare, flat
from sim.run import apply_assume, parse_assume, parse_substitute, run_games


def ablate_one(base, seeds, config, workers, removed=(), merge: dict | None = None, assume=None) -> dict:
    """Run one variant (abilities removed and/or B:A merges) over `seeds` and compare with `base`."""
    var = run_games(seeds, config, tuple(removed), workers, assume, merge or None)
    gone = list(removed) + list((merge or {}).keys())
    row = compare(base, var, gone)
    row["ablate"] = ",".join(sorted(removed))
    row["merge"] = ",".join(f"{b}:{a}" for b, a in sorted((merge or {}).items()))
    return row


def fmt(row: dict) -> str:
    label = row["ablate"] or row["merge"]
    return (f"{label[:40]:40s} present {row['games_present']:5d}  holder win "
            f"{row['holder_win_delta']:+.3f} [{row['holder_ci_low']:+.3f}, {row['holder_ci_high']:+.3f}]  "
            f"D {row['distance']:.3f} [{row['distance_lo']:.3f}, {row['distance_hi']:.3f}] "
            f"adj {row['distance_adj']:.3f}  casts/game {row['casts_per_game_present']:.2f}")


def main(argv=None) -> int:
    from sim.rules.compile import default_rules
    from sim.scenarios import load_config
    ap = argparse.ArgumentParser()
    ap.add_argument("--ability", default="", help="comma-separated slugs (each ablated separately)")
    ap.add_argument("--together", action="store_true", help="ablate the --ability list as one set")
    ap.add_argument("--merge", default="", help="comma-separated B:A merges (each simulated separately)")
    ap.add_argument("--all", action="store_true", help="every ability held in the baseline games")
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--config", default="mixed")
    ap.add_argument("--assume", action="append", default=[], metavar="KEY=VALUE")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--csv", default="")
    args = ap.parse_args(argv)
    rules = default_rules()
    config = load_config(args.config)
    try:
        assume = parse_assume(args.assume)
        apply_assume(rules.assumptions, assume)
        merges = parse_substitute(args.merge)
    except ValueError as exc:
        ap.error(str(exc))
    seeds = list(range(args.seed, args.seed + args.games))
    workers = args.workers or None
    base = run_games(seeds, config, (), workers, assume)
    slugs = sorted({s for r in base for s in r["holdings"]}) if args.all else [s for s in args.ability.split(",") if s]
    bad = [s for s in (*slugs, *merges, *merges.values()) if s not in rules.abilities]
    if bad:
        ap.error(f"unknown slug(s): {', '.join(bad)}")
    sets = [tuple(slugs)] if args.together and slugs else [(s,) for s in slugs]
    rows = []
    for removed in sets:
        rows.append(ablate_one(base, seeds, config, workers, removed, assume=assume))
        print(fmt(rows[-1]))
    for b, a in merges.items():
        rows.append(ablate_one(base, seeds, config, workers, (), {b: a}, assume))
        print(fmt(rows[-1]))
    if args.csv and rows:
        flats = [flat(r) for r in rows]
        with open(args.csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(flats[0]))
            w.writeheader()
            w.writerows(flats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
