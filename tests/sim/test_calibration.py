"""The value calibration: paired gifts (sim/engine/gifts.py), the harness (sim/analyze/calibrate.py)
and the weights value.py derives from its file (sim/policies/calibration.py)."""
import copy
import json

import pytest

from sim.analyze import calibrate
from sim.engine.game import Game
from sim.policies import calibration, value
from sim.rules.compile import build_rules
from sim.scenarios import generate

from .conftest import make_game, spec


# ---------------------------------------------------------------- the gifts are paired

def _game(rules, ctx, seed, gift=None):
    sc = generate(seed, calibrate.context_config(ctx), rules)
    if gift is not None:
        sc["gifts"] = [gift]
    return Game(rules, sc, seed)


def test_a_gift_nobody_can_receive_changes_nothing(rules):
    # the gift's random stream is its own: the paired game is the same game, draw for draw
    for seed in (3, 4):
        base = _game(rules, "small-annihilation", seed).run()
        none = _game(rules, "small-annihilation", seed,
                     {"kind": "armor", "points": 1, "who": "fighter", "team": 0, "n": 0}).run()
        assert none == {**base}


def test_the_harness_is_paired_and_deterministic():
    job = ("small-annihilation", "armor", 7)
    assert calibrate.play_job(job) == calibrate.play_job(job)
    base = calibrate.play_job(("small-annihilation", "", 7))
    assert base[3] in (0.0, 0.5, 1.0) and base[4] == 0.0
    # the baseline and the gifted game of a pair are generated from the same seed and scenario
    got = calibrate.play_job(job)
    assert got[4] > 0 and got[5] and set(got[5]) <= {"fighter"}


def test_gifts_do_what_they_say(rules):
    g = _game(rules, "small-annihilation", 11, {"kind": "armor", "points": 2, "who": "fighter", "team": 0, "n": 1})
    (entry,) = g.gift_log
    p = g.players[entry["pid"]]
    ref = _game(rules, "small-annihilation", 11).players[entry["pid"]]
    assert p.team == 0 and p.role == "fighter" and p.armor_max == ref.armor_max + 2
    g = _game(rules, "small-annihilation", 11, {"kind": "ability", "slug": "finger-of-death", "team": 0, "share": 1.0})
    assert len(g.gift_log) == sum(1 for p in g.players if p.team == 0)
    assert all("finger-of-death" in g.players[e["pid"]].uses for e in g.gift_log)


def test_death_ward_prevents_one_death_per_life(rules):
    g = make_game(rules, [spec("Warrior")], [spec("Warrior")])
    from sim.engine import gifts
    gifts.apply(g, [{"kind": "death-ward", "team": 0, "n": 1}])
    p = g.players[0]
    g.kill(p, g.players[1], "melee")
    assert p.alive and p.has_state("frozen", g.t)
    g.t += 31
    g._upkeep()
    g.kill(p, g.players[1], "melee")
    assert not p.alive


def test_state_gift_lands_on_an_enemy(rules):
    g = _game(rules, "small-annihilation", 5, {"kind": "state", "state": "stunned", "seconds": 30,
                                               "window": 1, "team": 0, "n": 1})
    prep = rules.a("respawn.pregame_prep_seconds")
    while g.t < prep + 10:
        g.step()
    assert g.applied[("gift-stunned", "state.apply")] == 1


def test_summary_per_unit_and_score():
    # two contexts, the reference doubles team 0's result change per unit of the other anchor
    raw = {}
    for ctx in ("a", "b"):
        raw[(ctx, "")] = {s: (0.0, 0.0, {}) for s in range(10)}
        raw[(ctx, "kill")] = {s: (1.0 if s < 4 else 0.0, 2.0, {"caster": 2}) for s in range(10)}
        raw[(ctx, "armor")] = {s: (1.0 if s < 2 else 0.0, 2.0, {"fighter": 2}) for s in range(10)}
    out = calibrate.summarize(raw, ["a", "b"], ["kill", "armor"], boot=200)
    a = out["armor"]["per_context"]["a"]
    assert a["dwin"] == pytest.approx(0.2) and a["per_unit"] == pytest.approx(0.1)
    assert out["armor"]["pooled"]["score"] == pytest.approx(5.0)
    assert out["kill"]["pooled"]["score"] == pytest.approx(10.0)


# ---------------------------------------------------------------- the weights value.py derives

def _doc(**over) -> dict:
    doc = {"fingerprint": calibration.fingerprint(), "anchors": {
        "kill": {"calibrates": "kind.death.cause", "map": "fair", "weight": {"value": 10.0}, "pooled": {}},
        "armor": {"calibrates": "scalar.armor_point", "map": "may-overstate", "weight": {"value": 7.5}, "pooled": {}},
        "state-stopped": {"calibrates": "state.stopped", "map": "needs-map", "weight": {"value": 0.1}, "pooled": {}},
        "state-frozen": {"calibrates": "state.frozen", "map": "may-understate", "weight": {"value": 1.0}, "pooled": {}},
        "state-stunned": {"calibrates": "state.stunned", "map": "fair", "weight": {"value": 2.5}, "pooled": {}},
    }}
    doc.update(over)
    return doc


def test_calibrated_weights_load_and_override():
    t = calibration.tables(value.HAND, _doc())
    assert t.weights["scalar"]["armor_point"] == 7.5 and t.sources["scalar.armor_point"] == "calibrated"
    assert t.weights["state"]["stunned"] == 2.5
    # needs-map: measured but the hand weight is used; may-understate: the hand weight is a floor
    assert t.weights["state"]["stopped"] == value.HAND_STATE_WEIGHT["stopped"]
    assert t.sources["state.stopped"] == "hand (needs map)"
    assert t.weights["state"]["frozen"] == value.HAND_STATE_WEIGHT["frozen"]
    assert t.sources["state.frozen"] == "hand (floor)"
    # anything not calibrated is the hand weight, and says so
    assert t.weights["kind"]["wound.heal"] == value.HAND_KIND_WEIGHT["wound.heal"]
    assert t.sources["kind.wound.heal"] == "hand"
    assert all(s for s in t.sources.values())


def test_calibrated_weights_change_the_score():
    rules = build_rules()
    with value.using(_doc()):
        berserker = value.breakdown(rules.abilities["berserker"], "fighter",
                                    value.Ctx(holder=value.Kit("fighter", armor_max=3),
                                              bearer=value.Kit("fighter", armor_max=3)), rules)
    # hand armor loss per point is 2; the test document leaves it uncalibrated, so still 2 x 3
    assert min(c for _, _, c in berserker) == pytest.approx(-6.0)
    doc = _doc()
    doc["anchors"]["bare"] = {"calibrates": "scalar.armor_loss_point", "map": "fair", "weight": {"value": 5.0},
                              "pooled": {}}
    rules = build_rules()
    with value.using(doc):
        berserker = value.breakdown(rules.abilities["berserker"], "fighter",
                                    value.Ctx(holder=value.Kit("fighter", armor_max=3),
                                              bearer=value.Kit("fighter", armor_max=3)), rules)
    assert min(c for _, _, c in berserker) == pytest.approx(-15.0)


def test_uncalibrated_fallback_is_the_hand_weights(tmp_path):
    assert calibration.load(tmp_path / "missing.json", how="on") is None
    t = calibration.tables(value.HAND, None)
    assert t.weights == {k: dict(v) for k, v in value.HAND.items()}
    assert set(t.sources.values()) == {"hand"}
    assert calibration.load(tmp_path / "missing.json", how="off") is None


def test_stale_calibration_fails_loudly(tmp_path):
    path = tmp_path / "cal.json"
    fresh = calibration.fingerprint()
    path.write_text(json.dumps(_doc()))
    assert calibration.load(path, how="on", current=fresh) is not None
    for bad in ({**fresh, "assumptions_sha256": "0" * 64}, {**fresh, "engine_version": -1}):
        path.write_text(json.dumps(_doc(fingerprint=bad)))
        with pytest.raises(calibration.StaleCalibration, match="stale"):
            calibration.load(path, how="on", current=fresh)
        with pytest.warns(UserWarning, match="stale"):
            assert calibration.load(path, how="stale-ok", current=fresh) is not None


def test_the_shipped_calibration_is_current():
    if not calibration.CALIBRATION_JSON.exists():
        pytest.skip("no calibration file")
    doc = json.loads(calibration.CALIBRATION_JSON.read_text())
    assert calibration.stale_reasons(doc) == [], "rerun python -m sim.analyze.calibrate"
