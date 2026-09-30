"""Caster doctrines in a stored run: how often each is played, how often it wins, and how it helps.

    .venv/bin/python -m sim.analyze.doctrines                   # latest run -> table, sim/out/doctrines.json
    .venv/bin/python -m sim.analyze.doctrines --run <run_id> --level 6 --top 8

Per class and doctrine (sim/data/doctrines.json; Magic Users only):
  share      the doctrine's share of the class's player-games
  win rate   with the game-clustered 95% interval (sim.analyze.stats.cluster_ratio_ci; draws left out)
  per life   own kills, enchant assists, control assists and saves, each summed over player-games and
             divided by lives played (deaths, plus one for a player still in the game at the end)
  assist %   (enchant + control assists) / (own kills + those assists): how much of the doctrine's
             part in kills comes through teammates
  bought     the spells most often bought by the doctrine's players (share of its players holding each)

Assists (sim/engine/game.py): an **enchant assist** is a kill made by a teammate while wearing an
Enchantment this player cast; a **control assist** is a teammate's kill of an enemy who was under a
State this player applied (Stunned, Frozen, Stopped, Suppressed, Fragile, Insubstantial) or an
Awe/Terror/Insult restriction from them at death or within the 10 s before it; a **save** is a
teammate's death prevented (Phoenix Tears, Troll Blood, Song of Survival), a revive, or a heal that
removed a wound from a teammate.

Archetype doctrines exist only at 6th level, so compare them with base doctrines at `--level 6`
(the "6th level" section of the default output does this).
"""
from __future__ import annotations

import argparse
import json
from collections import Counter

from sim.analyze.stats import cluster_ratio_ci
from sim.analyze.winrate import latest_run
from sim.paths import OUT

METRICS = ("kills", "enchant_assists", "control_assists", "saves")


def _frame(con, run_id: str):
    return con.execute("""
        select p.seed, p.cls, p.level, p.doctrine, p.play, p.won, p.kills, p.lives, p.enchant_assists,
               p.control_assists, p.saves, p.bought, g.winner
        from players p join games g using (run_id, seed)
        where run_id = ? and p.doctrine is not null and p.doctrine <> ''""", [run_id]).df()


def doctrine_table(df, rules=None, top: int = 6) -> list[dict]:
    """One row per (class, doctrine) from a player-game frame (columns as in `_frame`)."""
    from sim.rules.compile import default_rules
    rules = rules or default_rules()
    book = rules.doctrines
    rows = []
    class_n = df.groupby("cls").size().to_dict()
    for (cls, doc), grp in df.groupby(["cls", "doctrine"], sort=True):
        d = book.get(cls, doc)
        decisive = grp[grp["winner"] >= 0]
        per_game = decisive.groupby("seed").agg(wins=("won", "sum"), n=("won", "size"))
        ci = cluster_ratio_ci(per_game["wins"].to_numpy(), per_game["n"].to_numpy(), bounds=(0.0, 1.0))
        lives = max(1, int(grp["lives"].sum()))
        per_life = {m: float(grp[m].sum()) / lives for m in METRICS}
        assists = per_life["enchant_assists"] + per_life["control_assists"]
        held = Counter()
        for text in grp["bought"].fillna(""):
            for item in filter(None, text.split(",")):
                held[item.split(":")[0]] += 1
        n = len(grp)
        rows.append({
            "cls": cls, "doctrine": doc, "name": d.name if d else doc, "stance": d.stance if d else "",
            "play": d.play if d else "", "archetype": d.archetype if d else None,
            "players": n, "share": n / class_n[cls], "games": ci["clusters"],
            "win_rate": ci["est"], "ci_low": ci["lo"], "ci_high": ci["hi"],
            "kills_per_life": per_life["kills"], "enchant_assists_per_life": per_life["enchant_assists"],
            "control_assists_per_life": per_life["control_assists"], "saves_per_life": per_life["saves"],
            "assist_share": assists / (assists + per_life["kills"]) if assists + per_life["kills"] > 0 else float("nan"),
            "bought": [[s, c / n] for s, c in sorted(held.items(), key=lambda kv: (-kv[1], kv[0]))[:top]],
        })
    return rows


def _print(rows: list[dict], title: str) -> None:
    import pandas as pd
    if not rows:
        print(f"{title}: no Magic Users")
        return
    df = pd.DataFrame(rows)
    df["win [95% CI]"] = df.apply(lambda r: f"{r.win_rate:.3f} [{r.ci_low:.3f}, {r.ci_high:.3f}]", axis=1)
    df["bought"] = df["bought"].apply(lambda b: ", ".join(f"{s} {c:.0%}" for s, c in b))
    show = df[["cls", "doctrine", "stance", "play", "players", "share", "win [95% CI]", "kills_per_life",
               "enchant_assists_per_life", "control_assists_per_life", "saves_per_life", "assist_share"]].rename(
        columns={"kills_per_life": "kills/life", "enchant_assists_per_life": "ench/life",
                 "control_assists_per_life": "ctrl/life", "saves_per_life": "saves/life", "assist_share": "assist %"})
    print(title)
    print(show.round(3).to_string(index=False))
    print()
    for r in df.itertuples():
        print(f"  {r.cls}:{r.doctrine}: {r.bought}")
    print()


def main(argv=None) -> int:
    import duckdb
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--db", default=str(OUT / "runs.duckdb"))
    ap.add_argument("--run", default=None)
    ap.add_argument("--level", type=int, default=None, help="only players of this level")
    ap.add_argument("--top", type=int, default=6, help="most-bought spells listed per doctrine")
    ap.add_argument("--json", default=str(OUT / "doctrines.json"), help="also write the tables here ('' to skip)")
    args = ap.parse_args(argv)
    con = duckdb.connect(args.db, read_only=True)
    run_id = args.run or latest_run(con)
    cols = {r[0] for r in con.execute(
        "select column_name from information_schema.columns where table_name = 'players'").fetchall()}
    if "control_assists" not in cols:
        ap.error("this database has no doctrine or assist columns; run sim.run first")
    df = _frame(con, run_id)
    games = con.execute("select count(*) from games where run_id = ?", [run_id]).fetchone()[0]
    import pandas as pd
    pd.set_option("display.width", 220)
    print(f"run {run_id}: {games} games, {len(df)} Magic User player-games "
          "(win rate: game-clustered 95% interval, draws left out; per life = total / lives played)\n")
    if args.level is not None:
        df = df[df["level"] == args.level]
    everyone = doctrine_table(df, top=args.top)
    _print(everyone, "All levels" if args.level is None else f"Level {args.level}")
    at6 = doctrine_table(df[df["level"] == 6], top=args.top) if args.level is None else []
    if args.level is None:
        _print(at6, "6th level only (Archetype doctrines against base doctrines at the same level)")
    if args.json:
        out = {"run_id": run_id, "games": int(games), "all": everyone, "level6": at6,
               "definitions": (__doc__ or "").strip()}
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=1, default=float)
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
