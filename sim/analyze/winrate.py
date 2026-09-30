"""Win rates from a stored run.

    .venv/bin/python -m sim.analyze.winrate                 # latest run
    .venv/bin/python -m sim.analyze.winrate --run <run_id> --by cls,level

Player-level rates count each player-game as one trial, but players in the same game share its
outcome, so the interval (`ci_low`/`ci_high`) is **game-clustered**: a cluster-robust (sandwich)
interval with each game as one cluster (`sim.analyze.stats.cluster_ratio_ci`). `naive_low` /
`naive_high` is the Wilson interval that treats players as independent, kept for comparison, and
`deff` is the design effect (clustered variance / naive variance; 1 means no correlation).
Draws are left out of player-level rates. Team-level rates (`game_summary`) are one row per game.
"""
from __future__ import annotations

import argparse

from sim.analyze.stats import cluster_ratio_ci, wilson
from sim.paths import OUT


def latest_run(con) -> str:
    return con.execute("select run_id from runs order by started desc limit 1").fetchone()[0]


def winrates_from_frame(df, by: list[str]):
    """df: one row per player-game with columns `by`, `seed`, `won`, and optionally kills/deaths.
    Returns one row per group with the clustered and the naive interval."""
    import pandas as pd
    per_game = df.groupby(by + ["seed"], sort=True).agg(wins=("won", "sum"), n=("won", "size")).reset_index()
    rows = []
    for key, grp in per_game.groupby(by, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        ci = cluster_ratio_ci(grp["wins"].to_numpy(), grp["n"].to_numpy(), bounds=(0.0, 1.0))
        wins, n = int(grp["wins"].sum()), int(grp["n"].sum())
        naive = wilson(wins, n)
        rows.append({**dict(zip(by, key)), "n": n, "games": ci["clusters"], "wins": wins,
                     "win_rate": ci["est"], "ci_low": ci["lo"], "ci_high": ci["hi"],
                     "naive_low": naive[0], "naive_high": naive[1], "deff": ci["deff"]})
    out = pd.DataFrame(rows)
    extra = [c for c in ("kills", "deaths") if c in df.columns]
    if extra and len(out):
        means = df.groupby(by, sort=True)[extra].mean().reset_index()
        out = out.merge(means, on=by, how="left")
    return out


def players_frame(results: list[dict]):
    """Player-game rows (decisive games only) from in-memory results of sim.run.run_games."""
    import pandas as pd
    rows = [{"seed": r["seed"], **p} for r in results if r["winner"] >= 0 for p in r["players"]]
    return pd.DataFrame(rows)


def player_winrates(con, run_id: str, by: list[str]):
    df = con.execute(f"""
        select {", ".join(by)}, seed, won, kills, deaths
        from players p join games g using (run_id, seed)
        where run_id = ? and g.winner >= 0""", [run_id]).df()
    return winrates_from_frame(df, by)


def game_summary(con, run_id: str, by: str):
    df = con.execute(f"""
        select {by}, count(*) as games, avg(duration) as avg_seconds,
               sum(case when winner = 0 then 1 else 0 end) as team0_wins,
               sum(case when winner = -1 then 1 else 0 end) as draws
        from games where run_id = ? group by {by} order by {by}""", [run_id]).df()
    df["team0_rate"] = df["team0_wins"] / (df["games"] - df["draws"]).clip(lower=1)
    return df


def main(argv=None) -> int:
    import duckdb
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(OUT / "runs.duckdb"))
    ap.add_argument("--run", default=None)
    ap.add_argument("--by", default="cls")
    args = ap.parse_args(argv)
    con = duckdb.connect(args.db, read_only=True)
    run_id = args.run or latest_run(con)
    import pandas as pd
    pd.set_option("display.width", 180)
    print(f"run {run_id}  (ci_* = game-clustered 95% interval; naive_* = Wilson, players independent)")
    print(player_winrates(con, run_id, args.by.split(",")).round(3).to_string(index=False))
    for by in ("game_type", "balance"):
        print()
        print(game_summary(con, run_id, by).round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
