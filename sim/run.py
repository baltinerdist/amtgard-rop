"""Run many games in parallel and store the results in DuckDB.

    .venv/bin/python -m sim.run --games 1000                      # mixed scenarios, all cores
    .venv/bin/python -m sim.run --games 500 --config small --seed 100 --ablate call-lightning

Each game is fully determined by its seed (scenario, loadouts and play all derive their own
random streams from it), so a seed replays exactly and paired runs share scenarios.

Tables (appended to; one row set per run_id):
  runs      run_id, started, games, seed, config, ablate, wall_seconds, workers
  games     run_id, seed, game_type, balance, n_players, skill_sd, winner, duration
  players   run_id, seed, pid, team, cls, level, skill, role, kills, deaths, time_dead, won
  abilities run_id, seed, slug, metric, detail, n     (metric: cast / applied / noop / fail / kill)
"""
from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from multiprocessing import Pool

from sim.paths import OUT

_RULES = None


def _rules():
    global _RULES
    if _RULES is None:
        from sim.rules.compile import default_rules
        _RULES = default_rules()
    return _RULES


def play_seed(args: tuple) -> dict:
    """Worker entry point: (seed, config, ablate) -> result dict with the scenario summary."""
    from sim.engine.game import play
    from sim.scenarios import generate
    seed, config, ablate = args
    rules = _rules()
    sc = generate(seed, config, rules)
    res = play(rules, sc, seed, frozenset(ablate))
    res["scenario"] = {k: v for k, v in sc.items() if k != "teams"}
    return res


def run_games(seeds: list[int], config: dict, ablate: tuple = (), workers: int | None = None) -> list[dict]:
    jobs = [(s, config, tuple(ablate)) for s in seeds]
    workers = workers or os.cpu_count() or 1
    if workers == 1:
        results = [play_seed(j) for j in jobs]
    else:
        with Pool(workers) as pool:
            results = list(pool.imap_unordered(play_seed, jobs, chunksize=max(1, len(jobs) // (workers * 8))))
    results.sort(key=lambda r: r["seed"])
    return results


def frames(results: list[dict], run_id: str):
    import pandas as pd
    games, players, abil = [], [], []
    for r in results:
        sc = r["scenario"]
        games.append({"run_id": run_id, "seed": r["seed"], "game_type": sc["game_type"], "balance": sc["balance"],
                      "n_players": sc["n_players"], "skill_sd": sc["skill_sd"], "winner": r["winner"],
                      "duration": r["duration"]})
        for p in r["players"]:
            players.append({"run_id": run_id, "seed": r["seed"], **p})
        for slug, n in r["casts"].items():
            abil.append((run_id, r["seed"], slug, "cast", "", n))
        for metric in ("applied", "noops", "fails"):
            for key, n in r[metric].items():
                slug, detail = key.split("|", 1)
                abil.append((run_id, r["seed"], slug, metric.rstrip("s"), detail, n))
        for slug, n in r["kill_sources"].items():
            abil.append((run_id, r["seed"], slug, "kill", "", n))
    return (pd.DataFrame(games), pd.DataFrame(players),
            pd.DataFrame(abil, columns=["run_id", "seed", "slug", "metric", "detail", "n"]))


def store(results: list[dict], run_meta: dict, db_path) -> None:
    import duckdb
    import pandas as pd
    g, p, a = frames(results, run_meta["run_id"])
    runs = pd.DataFrame([run_meta])
    con = duckdb.connect(str(db_path))
    for name, df in (("runs", runs), ("games", g), ("players", p), ("abilities", a)):
        con.register("df", df)
        exists = con.execute("select count(*) from information_schema.tables where table_name = ?", [name]).fetchone()[0]
        if exists:
            con.execute(f"insert into {name} by name select * from df")
        else:
            con.execute(f"create table {name} as select * from df")
        con.unregister("df")
    con.close()


def main(argv=None) -> int:
    from sim.scenarios import load_config
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=0, help="first seed; games use seed..seed+games-1")
    ap.add_argument("--config", default="mixed", help="preset name (mixed/small/large) or JSON file")
    ap.add_argument("--ablate", default="", help="comma-separated ability slugs to remove from every loadout")
    ap.add_argument("--workers", type=int, default=0, help="processes (default: all cores)")
    ap.add_argument("--db", default=str(OUT / "runs.duckdb"))
    args = ap.parse_args(argv)

    config = load_config(args.config)
    ablate = tuple(s for s in args.ablate.split(",") if s)
    from sim.rules.compile import default_rules
    unknown = [s for s in ablate if s not in default_rules().abilities]
    if unknown:
        ap.error(f"unknown ability slug(s): {', '.join(unknown)}")
    OUT.mkdir(parents=True, exist_ok=True)
    workers = args.workers or os.cpu_count() or 1
    seeds = list(range(args.seed, args.seed + args.games))
    t0 = time.perf_counter()
    results = run_games(seeds, config, ablate, workers)
    wall = time.perf_counter() - t0
    run_id = uuid.uuid4().hex[:12]
    meta = {"run_id": run_id, "started": time.strftime("%Y-%m-%dT%H:%M:%S"), "games": len(results),
            "seed": args.seed, "config": json.dumps(config, sort_keys=True), "ablate": ",".join(ablate),
            "wall_seconds": round(wall, 3), "workers": workers}
    store(results, meta, args.db)
    draws = sum(1 for r in results if r["winner"] == -1)
    print(f"run {run_id}: {len(results)} games in {wall:.1f}s on {workers} workers "
          f"({len(results) / wall:.1f} games/s); draws {draws}; stored in {args.db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
