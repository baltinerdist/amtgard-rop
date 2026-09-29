"""Win rates from a stored run.

    .venv/bin/python -m sim.analyze.winrate                 # latest run
    .venv/bin/python -m sim.analyze.winrate --run <run_id> --by cls,level

Player-level rates treat each player-game as one trial. Players in the same game are not
independent, so the intervals are narrower than they should be; use them to rank, not to test.
Team-level rates (--by balance / game_type) are per game and do not have that problem.
"""
from __future__ import annotations

import argparse

from sim.analyze.stats import wilson
from sim.paths import OUT


def latest_run(con) -> str:
    return con.execute("select run_id from runs order by started desc limit 1").fetchone()[0]


def player_winrates(con, run_id: str, by: list[str]):
    cols = ", ".join(by)
    df = con.execute(f"""
        select {cols}, count(*) as n, sum(won) as wins, avg(kills) as kills, avg(deaths) as deaths
        from players p join games g using (run_id, seed)
        where run_id = ? and g.winner >= 0
        group by {cols} order by {cols}""", [run_id]).df()
    lo_hi = [wilson(int(w), int(n)) for w, n in zip(df["wins"], df["n"])]
    df["win_rate"] = df["wins"] / df["n"]
    df["ci_low"] = [a for a, _ in lo_hi]
    df["ci_high"] = [b for _, b in lo_hi]
    return df


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
    pd.set_option("display.width", 160)
    print(f"run {run_id}")
    print(player_winrates(con, run_id, args.by.split(",")).round(3).to_string(index=False))
    for by in ("game_type", "balance"):
        print()
        print(game_summary(con, run_id, by).round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
