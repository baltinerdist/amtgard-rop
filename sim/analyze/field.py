"""Field numbers for a stored run: deaths per minute by kind of player, and rejoin time.

    .venv/bin/python -m sim.analyze.field                 # latest run
    .venv/bin/python -m sim.analyze.field --run 3e411838f261

Deaths per minute are deaths over minutes alive (game length less time dead, the pregame included),
per player, by kind: line fighters (the fighter role), Magic Users who stay back (Bard, Druid,
Wizard and Healer doctrines other than battle play), battle casters, and Archers. sim/PHASE2.md
expects a caster to die less often per minute than a fighter in the same games once there is a map.

Rejoin time (space on only): seconds from a respawn at base until the player is first within 50' of
an enemy on the field, averaged over respawns (games.rejoin_n / rejoin_sum). With space off it is
`respawn.rejoin_seconds` by construction.
"""
from __future__ import annotations

import argparse

from sim.paths import OUT

KINDS = """case when p.role = 'fighter' then 'fighter'
               when p.role = 'archer' then 'archer'
               when p.play = 'battle' then 'battle caster'
               else 'caster' end"""


def summary(con, run_id: str) -> dict:
    space = "off"
    cols = {r[0] for r in con.execute(
        "select column_name from information_schema.columns where table_name = 'runs'").fetchall()}
    if "space" in cols:
        space = con.execute("select coalesce(space, 'off') from runs where run_id = ?", [run_id]).fetchone()[0]
    rows = con.execute(f"""
        select {KINDS} as kind, count(*) as players, sum(p.deaths) as deaths,
               sum(g.duration - p.time_dead) / 60.0 as alive_min
        from players p join games g using (run_id, seed)
        where p.run_id = ? group by kind order by kind""", [run_id]).fetchall()
    out = {"run_id": run_id, "space": space,
           "deaths_per_min": {k: (d / m if m else 0.0, n) for k, n, d, m in rows}}
    gcols = {r[0] for r in con.execute(
        "select column_name from information_schema.columns where table_name = 'games'").fetchall()}
    if "rejoin_n" in gcols:
        n, s = con.execute("select sum(rejoin_n), sum(rejoin_sum) from games where run_id = ?", [run_id]).fetchone()
        out["rejoin"] = (s / n, int(n)) if n else None
    return out


def main(argv=None) -> int:
    import duckdb
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--db", default=str(OUT / "runs.duckdb"))
    ap.add_argument("--run", default=None, help="run id (default: the latest)")
    args = ap.parse_args(argv)
    con = duckdb.connect(args.db, read_only=True)
    run_id = args.run or con.execute("select run_id from runs order by started desc limit 1").fetchone()[0]
    s = summary(con, run_id)
    print(f"run {run_id} (space {s['space']})")
    for kind, (rate, n) in s["deaths_per_min"].items():
        print(f"  {kind:14s} {rate:.3f} deaths per minute alive  ({n} player-games)")
    if s.get("rejoin"):
        mean, n = s["rejoin"]
        print(f"  rejoin after respawn: {mean:.1f} s on average over {n} respawns")
    elif s["space"] == "off":
        print("  rejoin after respawn: respawn.rejoin_seconds (Phase 1, by construction)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
