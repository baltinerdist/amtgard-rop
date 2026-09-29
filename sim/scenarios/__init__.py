"""Scenario generation: who plays, at what level and skill, how teams are split, which game.

A scenario is a plain dict so it can be logged and replayed:
    {"game_type", "lives", "respawn_seconds", "refresh_seconds", "max_seconds",
     "balance", "skill_sd", "n_players", "teams": [[{"cls", "level", "skill"}, ...], ...]}

Game types follow rules/battlegames.md:
  annihilation - Mutual Annihilation: individual life pools, 150 s death count, last team standing
  attrition    - unlimited lives, timed; most kills wins (a stand-in for objective games)
"""
from __future__ import annotations

import copy
import json
import random
from pathlib import Path

from sim.rules.compile import Rules

GAME_TYPES = {
    "annihilation": {"lives": 4, "respawn_seconds": 150, "refresh_seconds": None, "max_seconds": 1800},
    "attrition": {"lives": None, "respawn_seconds": 60, "refresh_seconds": 900, "max_seconds": 1200},
}
BALANCE_METHODS = ("random", "snake-skill", "level-sum", "class-mirror")

PRESETS = {
    "mixed": {
        "players": [10, 40],
        "game_types": {"annihilation": 0.6, "attrition": 0.4},
        "balance_methods": list(BALANCE_METHODS),
        "skill_sd": [0.5, 1.5],
    },
    "small": {"players": [6, 12], "game_types": {"annihilation": 1.0},
              "balance_methods": ["random"], "skill_sd": [1.0, 1.0]},
    "large": {"players": [40, 80], "game_types": {"annihilation": 1.0},
              "balance_methods": ["random"], "skill_sd": [1.0, 1.0]},
}


def load_config(name_or_path: str | None) -> dict:
    if not name_or_path:
        return copy.deepcopy(PRESETS["mixed"])
    if name_or_path in PRESETS:
        return copy.deepcopy(PRESETS[name_or_path])
    return json.loads(Path(name_or_path).read_text())


def _weighted(rng: random.Random, weights: dict):
    keys = sorted(weights)
    return rng.choices(keys, weights=[float(weights[k]) for k in keys])[0]


def split(players: list[dict], method: str, rng: random.Random, n_teams: int = 2) -> list[list[dict]]:
    teams: list[list[dict]] = [[] for _ in range(n_teams)]
    if method == "random":
        pool = players[:]
        rng.shuffle(pool)
        for i, pl in enumerate(pool):
            teams[i % n_teams].append(pl)
    elif method == "snake-skill":
        pool = sorted(players, key=lambda pl: -pl["skill"])
        for i, pl in enumerate(pool):
            rnd, pos = divmod(i, n_teams)
            teams[pos if rnd % 2 == 0 else n_teams - 1 - pos].append(pl)
    elif method == "level-sum":
        pool = sorted(players, key=lambda pl: (-pl["level"], rng.random()))
        for pl in pool:
            open_teams = [t for t in teams if len(t) < -(-len(players) // n_teams)]
            min(open_teams, key=lambda t: (sum(x["level"] for x in t), len(t))).append(pl)
    elif method == "class-mirror":
        by_cls: dict[str, list[dict]] = {}
        for pl in players:
            by_cls.setdefault(pl["cls"], []).append(pl)
        leftovers = []
        for cls in sorted(by_cls):
            group = sorted(by_cls[cls], key=lambda pl: -pl["level"])
            full = len(group) - len(group) % n_teams
            for i, pl in enumerate(group[:full]):
                teams[i % n_teams].append(pl)
            leftovers += group[full:]
        rng.shuffle(leftovers)
        for pl in leftovers:
            min(teams, key=len).append(pl)
    else:
        raise ValueError(f"unknown balance method {method!r}")
    return teams


def generate(seed: int, config: dict, rules: Rules) -> dict:
    rng = random.Random(f"{seed}:scenario")
    lo, hi = config.get("players", [10, 40])
    n = rng.randint(lo, hi)
    n -= n % 2
    game_type = _weighted(rng, config.get("game_types", {"annihilation": 1.0}))
    method = rng.choice(config.get("balance_methods", ["random"]))
    sd_lo, sd_hi = config.get("skill_sd", [1.0, 1.0])
    skill_sd = rng.uniform(sd_lo, sd_hi)
    class_w = config.get("class_weights") or rules.a("population.class_weights")
    level_w = config.get("level_weights") or rules.a("population.level_weights")
    players = [{"cls": _weighted(rng, class_w), "level": int(_weighted(rng, level_w)),
                "skill": rng.gauss(0.0, skill_sd)} for _ in range(n)]
    for fixed in config.get("force", []):  # e.g. [{"team": 0, "cls": "Healer", "level": 6}]
        players.append({"cls": fixed["cls"], "level": fixed["level"], "skill": fixed.get("skill", 0.0),
                        "_team": fixed.get("team")})
    free = [pl for pl in players if pl.get("_team") is None]
    teams = split(free, method, rng)
    for pl in players:
        if pl.get("_team") is not None:
            teams[pl.pop("_team")].append(pl)
    sc = {"game_type": game_type, **GAME_TYPES[game_type], **config.get("overrides", {}),
          "balance": method, "skill_sd": round(skill_sd, 4), "n_players": len(players), "teams": teams}
    return sc
