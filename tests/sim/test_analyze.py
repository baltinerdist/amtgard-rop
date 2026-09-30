"""Analysis layer: clustered intervals, complexity score, impact distance, greedy cut selection,
assumption overrides and merge substitution."""
import math
import random

import numpy as np
import pytest

from sim.analyze import complexity as cx
from sim.analyze.cut import merge_candidates, rank, select
from sim.analyze.impact import compare, holder_team
from sim.analyze.sensitivity import jaccard, parse_grid, settings, spearman
from sim.analyze.stats import bootstrap_weights, cluster_bootstrap_ci, cluster_ratio_ci, wilson
from sim.run import apply_assume, make_variant, parse_assume, parse_substitute, variant_rules


# ---------------------------------------------------------------- clustered intervals

def _correlated_games(n_games=300, size=20, seed=1):
    """Games where every player shares the game's outcome tendency (strong within-game correlation)."""
    rng = random.Random(seed)
    wins, ns, flat, clusters = [], [], [], []
    for g in range(n_games):
        p = 0.9 if rng.random() < 0.5 else 0.1
        outcomes = [1 if rng.random() < p else 0 for _ in range(size)]
        wins.append(sum(outcomes))
        ns.append(size)
        flat += outcomes
        clusters += [g] * size
    return wins, ns, flat, clusters


def test_clustered_interval_wider_than_naive_on_correlated_data():
    wins, ns, flat, clusters = _correlated_games()
    ci = cluster_ratio_ci(wins, ns)
    lo, hi = wilson(sum(wins), sum(ns))
    assert ci["hi"] - ci["lo"] > 2.5 * (hi - lo)
    assert ci["deff"] > 5
    boot = cluster_bootstrap_ci(flat, clusters, n_boot=400)
    assert boot["hi"] - boot["lo"] > 2.5 * (hi - lo)
    assert abs(boot["est"] - ci["est"]) < 1e-12


def test_clustered_interval_matches_naive_when_independent():
    rng = random.Random(2)
    outcomes = [1 if rng.random() < 0.4 else 0 for _ in range(4000)]
    ci = cluster_ratio_ci(outcomes, [1] * len(outcomes))   # one trial per cluster
    lo, hi = wilson(sum(outcomes), len(outcomes))
    assert ci["hi"] - ci["lo"] == pytest.approx(hi - lo, rel=0.05)
    assert ci["deff"] == pytest.approx(1.0, abs=0.01)


def test_clustered_interval_edge_cases():
    assert math.isnan(cluster_ratio_ci([], [])["est"])
    one = cluster_ratio_ci([3], [5])
    assert one["est"] == 0.6 and math.isnan(one["se"])
    clipped = cluster_ratio_ci([0, 0, 1], [10, 10, 10], bounds=(0.0, 1.0))
    assert clipped["lo"] >= 0.0


def test_bootstrap_weights_resample_all_clusters():
    w = bootstrap_weights(50, 20, seed=3)
    assert w.shape == (20, 50)
    assert np.all(w.sum(axis=1) == 50)


# ---------------------------------------------------------------- complexity

def test_complexity_components_and_score():
    rec = {"slug": "x", "title": "X",
           "incantation": {"words": 8, "repetitions": 3},
           "sentences": [{"text": "one two three"}, {"text": "four five"}],
           "requirements": [{"kind": "a"}], "restrictions": [], "termination": [{"kind": "b"}, {"kind": "c"}],
           "properties": [{"kind": "d"}], "references": [{}, {}, {}, {}], "clarifications": [{}],
           "open_questions": ["?", "?"],
           "availability": [{"cls": "Wizard", "levels": [1, 3]}, {"cls": "Druid", "levels": [2]}]}
    c = cx.counts(rec)
    assert c == {"sentences": 2, "words": 5, "incantation": 24, "requirements": 1, "restrictions": 0,
                 "endings": 2, "properties": 1, "references": 4, "clarifications": 1, "open_questions": 2,
                 "classes": 2, "class_levels": 3}
    s = cx.score(rec)
    assert s["score"] == pytest.approx(sum(cx.WEIGHTS[k] * c[k] for k in cx.COMPONENTS))
    assert s["points"]["incantation"] == pytest.approx(24 * cx.WEIGHTS["incantation"])
    only_sentences = cx.score(rec, {"sentences": 1.0})
    assert only_sentences["score"] == 2
    assert cx.own_text_score(s) == pytest.approx(
        s["score"] - s["points"]["classes"] - s["points"]["class_levels"])


def test_complexity_table_covers_metadata():
    tab = cx.table()
    assert len(tab) > 150
    assert all(e["score"] > 0 for e in tab.values())
    # no incantation -> no incantation points
    assert all(e["counts"]["incantation"] >= 0 for e in tab.values())


# ---------------------------------------------------------------- greedy optimizer

def _items():
    return [
        {"kind": "cut", "remove": "a", "keep": None, "impact": 0.00, "saved": 2.0},
        {"kind": "cut", "remove": "b", "keep": None, "impact": 0.01, "saved": 10.0},
        {"kind": "cut", "remove": "c", "keep": None, "impact": 0.05, "saved": 1.0},
        {"kind": "cut", "remove": "d", "keep": None, "impact": 0.30, "saved": 20.0},
        {"kind": "merge", "remove": "e", "keep": "d", "impact": 0.02, "saved": 5.0},
        {"kind": "merge", "remove": "b", "keep": "a", "impact": 0.00, "saved": 8.0},
    ]


def test_greedy_by_count_takes_smallest_impact_and_respects_conflicts():
    sel = select(_items(), universe_count=10, universe_complexity=100.0, target=0.3, by="count")
    removed = [it["remove"] for it in sel["chosen"]]
    assert sel["reached"] and sel["removed_count"] == 3
    # 'b>a' (impact 0, saves 8) sorts before cut 'a' (impact 0, saves 2); once a is kept it cannot be cut
    assert removed == ["b", "e"] + ["c"]
    assert "a" not in removed and "d" not in removed


def test_greedy_by_complexity_uses_impact_per_point():
    # ratios: b>a 0, a 0, b .001, e>d .004, d .015, c .05; merges keep a and d, so those cuts are skipped
    sel = select(_items(), universe_count=10, universe_complexity=100.0, target=0.13, by="complexity")
    assert sel["reached"] and sel["saved"] == 13
    assert [it["remove"] for it in sel["chosen"]] == ["b", "e"]
    # 15 points would need d or a, both kept by the chosen merges: the greedy reports it fell short
    short = select(_items(), universe_count=10, universe_complexity=100.0, target=0.15, by="complexity")
    assert not short["reached"] and short["saved"] == 14


def test_greedy_protect_and_unreachable_target():
    sel = select(_items(), universe_count=10, universe_complexity=100.0, target=0.9, by="count", protect=["b", "c"])
    removed = {it["remove"] for it in sel["chosen"]}
    assert not removed & {"b", "c"}
    assert not sel["reached"]
    with pytest.raises(ValueError):
        select(_items(), 10, 100.0, by="words")


def test_rank_orders_by_ratio():
    r = rank([it for it in _items() if it["kind"] == "cut"])
    assert [it["remove"] for it in r] == ["a", "b", "d", "c"]
    assert [it["rank"] for it in r] == [1, 2, 3, 4]


def test_merge_candidates_direction_and_filters():
    ctab = {s: cx.score_counts({"class_levels": lv, "sentences": sc}) for s, lv, sc in
            (("big", 5, 3), ("small", 1, 6), ("x", 1, 1), ("y", 1, 1))}
    cov = {s: {"status": "full"} for s in ctab}
    pairs = [{"a": "big", "b": "small", "relation": "same-effects", "score": 1},
             {"a": "x", "b": "y", "relation": "overlap", "score": 1}]
    m = merge_candidates(pairs, ctab, cov, set(ctab))
    assert [(c["remove"], c["keep"]) for c in m] == [("small", "big")]   # overlap is not a merge relation
    assert merge_candidates(pairs, ctab, cov, set(ctab), protect=["small"]) == []
    cov["big"] = {"status": "none"}
    assert merge_candidates(pairs, ctab, cov, set(ctab)) == []


# ---------------------------------------------------------------- impact distance

def _fake_game(seed, winner, duration, holders, casts):
    players = [{"pid": i, "team": i % 2, "cls": ("Warrior", "Wizard")[i // 2 % 2], "level": 1, "skill": 0.0,
                "role": "fighter", "kills": 1, "deaths": 1, "time_dead": 10.0, "won": int(i % 2 == winner)}
               for i in range(4)]
    return {"seed": seed, "winner": winner, "duration": duration, "players": players, "casts": casts,
            "applied": {}, "noops": {}, "fails": {}, "kill_sources": {}, "holdings": holders}


def test_impact_identical_runs_have_zero_distance():
    games = [_fake_game(s, s % 2, 300 + 10 * s, {"heal": [1, 0]}, {"heal": 2, "mend": 1}) for s in range(40)]
    row = compare(games, games, ["heal"], n_boot=100)
    assert row["distance"] == pytest.approx(0.0)
    assert row["holder_win_delta"] == 0.0
    assert row["games_with_holder"] == 40


def test_impact_detects_longer_games_and_holder_losses():
    base = [_fake_game(s, 0, 300 + 10 * s, {"heal": [1, 0]}, {"heal": 2, "mend": 1}) for s in range(40)]
    var = [_fake_game(s, 1, 600 + 10 * s, {"heal": [1, 0]}, {"mend": 3}) for s in range(40)]
    row = compare(base, var, ["heal"], n_boot=100)
    assert row["holder_win_delta"] == -1.0
    assert row["measures"]["duration"]["delta"] == pytest.approx(300.0)
    assert row["measures"]["use_mix"]["component"] == pytest.approx(2 / 3)
    assert row["distance"] > 1.0
    assert row["distance_lo"] <= row["distance"] <= row["distance_hi"] + 1e-9
    with pytest.raises(ValueError):
        compare(base, var[1:], ["heal"])


def test_holder_team_sums_over_removed_and_skips_ties():
    g = {"holdings": {"a": [2, 0], "b": [0, 1]}}
    assert holder_team(g, ["a"]) == 0
    assert holder_team(g, ["a", "b"]) == 0
    assert holder_team({"holdings": {"a": [1, 1]}}, ["a"]) is None
    assert holder_team(g, ["zzz"]) is None


# ---------------------------------------------------------------- overrides and substitution

def test_parse_assume_values():
    got = parse_assume(["melee.base_hit_per_second=0.3", "casting.engaged_casting_allowed=true",
                        "range.p_in_range.20'=0.4", "a.b=hello", "a.c={\"x\": 1}"])
    assert got == {"melee.base_hit_per_second": 0.3, "casting.engaged_casting_allowed": True,
                   "range.p_in_range.20'": 0.4, "a.b": "hello", "a.c": {"x": 1}}
    for bad in ("nokey", "melee=0.3", "=1"):
        with pytest.raises(ValueError):
            parse_assume([bad])


def test_apply_assume_sets_values_without_touching_the_original(rules):
    orig = rules.assumptions
    out = apply_assume(orig, {"melee.base_hit_per_second": 0.3, "range.p_in_range.20'": 0.4,
                              "melee.shield_logit.value.large": -1.0})
    assert out["melee"]["base_hit_per_second"]["value"] == 0.3
    assert out["range"]["p_in_range"]["value"]["20'"] == 0.4
    assert out["melee"]["shield_logit"]["value"]["large"] == -1.0
    assert orig["melee"]["base_hit_per_second"]["value"] != 0.3
    for bad in ({"melee.nope": 1}, {"nogroup.x": 1}, {"range.p_in_range.99'": 0.1},
                {"melee.base_hit_per_second": "fast"}, {"casting.engaged_casting_allowed": 1}):
        with pytest.raises(ValueError):
            apply_assume(orig, bad)


def test_variant_rules_apply_assume_and_substitution():
    r = variant_rules(make_variant({"melee.base_hit_per_second": 0.31}, {"icy-blast": "iceball"}))
    assert r.a("melee.base_hit_per_second") == 0.31
    for cls in r.classes.values():
        assert all(ca.slug != "icy-blast" for ca in cls.abilities)
    druid = [ca for ca in r.classes["Druid"].abilities if ca.slug == "iceball"]
    assert len(druid) == 1 and druid[0].levels == (3, 4)   # folded: buyable from Icy Blast's level
    assert variant_rules(make_variant()) is variant_rules()


def test_parse_substitute():
    assert parse_substitute("b:a, d:c") == {"b": "a", "d": "c"}
    assert parse_substitute("") == {}
    for bad in ("b", "b:", ":a", "a:a"):
        with pytest.raises(ValueError):
            parse_substitute(bad)


# ---------------------------------------------------------------- sensitivity helpers

def test_sensitivity_grid_and_rank_stats():
    grid = parse_grid(["melee.base_hit_per_second=0.18,0.26", "time.speech_words_per_second=2,3"])
    assert grid == {"melee.base_hit_per_second": [0.18, 0.26], "time.speech_words_per_second": [2, 3]}
    assert len(settings(grid)) == 4
    assert len(settings(grid, factorial=True)) == 4
    assert settings({"a.b": [1]}) == [{"a.b": 1}]
    assert spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)
    assert jaccard(["a", "b"], ["b", "c"]) == pytest.approx(1 / 3)
    assert jaccard([], []) == 1.0
