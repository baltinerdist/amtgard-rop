"""Paired ablation: remove an ability from every loadout and replay the same seeds.

    .venv/bin/python -m sim.analyze.ablation --ability call-lightning --games 2000
    .venv/bin/python -m sim.analyze.ablation --all --games 300 --csv sim/out/ablation.csv

Common random numbers: each seed fixes the scenario (players, levels, skill, teams) and every
player's loadout draws, so baseline and ablated games start from the same rosters. The play
itself uses one random stream, so once the removed ability would have been used the two games
diverge; that adds noise but no bias.

Main measure, per game where one team holds the ability more than the other ("holder team"):
    delta = holder result without the ability - holder result with it   (win 1, draw 0.5, loss 0)
Averaged over games with a normal-approximation 95% interval. A delta near zero with a tight
interval means removing the ability barely changes who wins.
"""
from __future__ import annotations

import argparse
import csv

from sim.analyze.stats import mean_ci
from sim.run import run_games


def _score(res: dict, team: int) -> float:
    return 0.5 if res["winner"] == -1 else float(res["winner"] == team)


def compare(slug: str, base: list[dict], ablated: list[dict]) -> dict:
    deltas, casts, present = [], [], 0
    for b, a in zip(base, ablated):
        assert b["seed"] == a["seed"]
        held = b["holdings"].get(slug)
        if not held or sum(held) == 0:
            continue
        present += 1
        casts.append(b["casts"].get(slug, 0))
        top = max(held)
        if held.count(top) > 1:
            continue  # both teams hold it equally: no holder team
        team = held.index(top)
        deltas.append(_score(a, team) - _score(b, team))
    m, lo, hi = mean_ci(deltas)
    return {"slug": slug, "games": len(base), "games_present": present, "games_with_holder": len(deltas),
            "holder_win_delta": m, "ci_low": lo, "ci_high": hi,
            "casts_per_game_present": (sum(casts) / len(casts)) if casts else 0.0}


def main(argv=None) -> int:
    from sim.rules.compile import default_rules
    from sim.scenarios import load_config
    ap = argparse.ArgumentParser()
    ap.add_argument("--ability", default="", help="comma-separated slugs (each ablated separately)")
    ap.add_argument("--all", action="store_true", help="every ability held in the baseline games")
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--config", default="mixed")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--csv", default="")
    args = ap.parse_args(argv)
    rules = default_rules()
    config = load_config(args.config)
    seeds = list(range(args.seed, args.seed + args.games))
    base = run_games(seeds, config, (), args.workers or None)
    if args.all:
        slugs = sorted({s for r in base for s in r["holdings"]})
    else:
        slugs = [s for s in args.ability.split(",") if s]
    bad = [s for s in slugs if s not in rules.abilities]
    if bad:
        ap.error(f"unknown slug(s): {', '.join(bad)}")
    rows = []
    for slug in slugs:
        abl = run_games(seeds, config, (slug,), args.workers or None)
        row = compare(slug, base, abl)
        rows.append(row)
        print(f"{slug:32s} present {row['games_present']:5d}  holder-team win change "
              f"{row['holder_win_delta']:+.3f} [{row['ci_low']:+.3f}, {row['ci_high']:+.3f}]  "
              f"casts/game {row['casts_per_game_present']:.2f}")
    if args.csv:
        with open(args.csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
