"""Same seed -> same game; paired ablation runs share scenarios and loadout draws."""
import random

from sim.engine.game import Game, play
from sim.engine.loadout import build_player
from sim.run import run_games
from sim.scenarios import generate, load_config


def test_same_seed_same_result(rules):
    cfg = load_config("mixed")
    for seed in (3, 11, 42):
        sc = generate(seed, cfg, rules)
        assert play(rules, sc, seed) == play(rules, sc, seed)


def test_different_seeds_differ(rules):
    cfg = load_config("mixed")
    a = play(rules, generate(1, cfg, rules), 1)
    b = play(rules, generate(2, cfg, rules), 2)
    assert a != b


def test_parallel_matches_serial():
    cfg = load_config("small")
    seeds = list(range(20))
    assert run_games(seeds, cfg, (), workers=1) == run_games(seeds, cfg, (), workers=2)


def test_scenario_is_seed_determined(rules):
    cfg = load_config("mixed")
    assert generate(7, cfg, rules) == generate(7, cfg, rules)


def test_ablation_keeps_rosters_and_other_draws(rules):
    for level in range(1, 7):
        base = build_player(rules, 0, 0, "Scout", level, 0.0, random.Random("x"))
        abl = build_player(rules, 0, 0, "Scout", level, 0.0, random.Random("x"), frozenset({"heal"}))
        assert "heal" not in abl.uses
        assert set(base.uses) - {"heal"} == set(abl.uses)
        assert (base.armor_max, base.shield, base.great_weapon) == (abl.armor_max, abl.shield, abl.great_weapon)


def test_ablated_ability_never_cast(rules):
    cfg = load_config("mixed")
    for seed in range(10):
        res = play(rules, generate(seed, cfg, rules), seed, frozenset({"lightning-bolt"}))
        assert "lightning-bolt" not in res["casts"]
        assert "lightning-bolt" not in res["holdings"]


def test_game_always_ends(rules):
    cfg = load_config("mixed")
    for seed in range(15):
        g = Game(rules, generate(seed, cfg, rules), seed)
        res = g.run()
        assert res["winner"] in (-1, 0, 1)
        assert res["duration"] <= g.sc["max_seconds"]
