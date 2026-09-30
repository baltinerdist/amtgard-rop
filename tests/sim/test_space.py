"""The spatial layer (sim/engine/space.py): Phase 1 unchanged behind NullSpace, and the field's
geometry, movement rules, steering and determinism."""
import copy
import importlib.util
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import pytest

from sim.engine.game import Game
from sim.engine.space import FOOT, FieldSpace, NullSpace, style
from sim.paths import ASSUMPTIONS_JSON
from sim.rules.compile import build_rules
from sim.scenarios import load_config

from .conftest import scenario, spec

DATA = Path(__file__).parent / "data"
ROOT = Path(__file__).resolve().parents[2]


def _recorder():
    s = importlib.util.spec_from_file_location("record_digests", DATA / "record_digests.py")
    mod = importlib.util.module_from_spec(s)
    s.loader.exec_module(mod)
    return mod


def _rules(**space):
    a = copy.deepcopy(json.loads(ASSUMPTIONS_JSON.read_text()))
    for k, v in space.items():
        a["space"][k]["value"] = v
    return build_rules(assumptions=a)


@pytest.fixture(scope="module")
def field_rules():
    return _rules()


def field_game(rules, team0, team1, seed=1, ablate=frozenset(), **kw):
    """A field game past the pregame, everyone on the field."""
    g = Game(rules, scenario(team0, team1, **kw), seed, ablate=ablate, space="on")
    g.t = 100.0
    for p in g.players:
        p.at_base_until = 0.0
    g.space._fresh.clear()
    return g


def place(g, p, x, y=20.0):
    g.space.x[p.pid], g.space.y[p.pid] = x, y
    g.space._d = None


# ---------------------------------------------------------------- Phase 1 behind NullSpace

def test_null_space_is_phase1_bit_for_bit(rules):
    """Space off plays exactly as the engine did before the spatial layer: the result and full
    event trace of 30 mixed games match digests recorded at 7294de4."""
    want = json.loads((DATA / "phase1_digests.json").read_text())
    rec = _recorder()
    cfg = load_config("mixed")
    got = {str(s): rec.digest(rules, s, cfg) for s in rec.SEEDS}
    assert got == want


def test_space_off_is_the_default(rules):
    g = Game(rules, scenario([spec("Warrior")], [spec("Wizard")]), 1)
    assert isinstance(g.space, NullSpace) and not g.space.spatial and g.dt == 1
    assert g.per_tick(0.22) == 0.22


def test_unknown_space_mode_rejected(rules):
    with pytest.raises(ValueError):
        Game(rules, scenario([spec("Warrior")], [spec("Wizard")]), 1, space="maybe")


# ---------------------------------------------------------------- geometry

def test_ranges_in_metres(field_rules):
    g = field_game(field_rules, [spec("Wizard")], [spec("Warrior")])
    s = g.space
    assert isinstance(s, FieldSpace) and s.spatial and g.dt == 0.5
    assert s.metres("20'") == pytest.approx(6.1, abs=0.01)
    assert s.metres("50'") == pytest.approx(15.2, abs=0.05)
    assert s.metres("Touch") == s.metres("Other") == 1.0
    assert s.metres("", "magic-ball") == s.throw_m and s.metres("", "specialty-arrow") == s.bow_m
    wiz, war = g.players
    wiz_uses = next(iter(wiz.uses.values()))
    for d, label, inside in ((6.0, "20'", True), (6.2, "20'", False), (15.1, "50'", True), (15.3, "50'", False),
                             (0.9, "Touch", True), (1.1, "Touch", False)):
        place(g, wiz, 10.0)
        place(g, war, 10.0 + d)
        assert (s.distance(wiz, war) <= s.metres(label)) is inside
        assert s.completes_in_range(wiz, war, label, "verbal") is inside
        assert (s.p_in_range(wiz, war, label) == 1.0) is inside
    place(g, war, 10.0 + 6.0)
    wiz_uses.range = "20'"
    assert s.roll_in_range(wiz, war, wiz_uses) and s.in_range_filter(wiz, [war], wiz_uses) == [war]
    wiz_uses.range = "Touch"
    assert not s.roll_touch(wiz, war, wiz_uses) and s.touch_filter(wiz, [war], wiz_uses) == []


def test_melee_reach_by_weapon(field_rules):
    g = field_game(field_rules, [spec("Warrior"), spec("Wizard")], [spec("Warrior")])
    war, wiz, foe = g.players
    s = g.space
    assert s.reach[war.pid] == 1.5 and s.reach[wiz.pid] == 1.2
    war.great_weapon = True
    assert s._reach_of(war) == 2.1
    place(g, foe, 20.0)
    place(g, wiz, 21.3)
    assert not s.can_reach(wiz, foe) and s.can_reach(foe, wiz)
    place(g, wiz, 21.1)
    assert s.can_reach(wiz, foe)


def test_engagement_from_proximity(field_rules):
    """A line fighter engages an enemy within its reach, not one farther away; a pair breaks when
    they are farther apart than the longer reach plus half a metre."""
    g = field_game(field_rules, [spec("Warrior")], [spec("Warrior")])
    a, b = g.players
    place(g, a, 20.0)
    place(g, b, 22.0)
    g.space.engage()
    assert a.target is None and b.target is None
    place(g, b, 21.4)
    g.space.engage()
    assert a.target == b.pid and b.target == a.pid
    place(g, b, 23.0)
    g.space.engage()
    assert a.target is None and b.target is None


def _moved_in_one_tick(g, p):
    x0, y0 = g.space.x[p.pid], g.space.y[p.pid]
    g.t += g.dt
    g.space.move()
    return math.hypot(g.space.x[p.pid] - x0, g.space.y[p.pid] - y0)


def test_charge_runs_and_the_line_walks(field_rules):
    s_run, s_walk, dt = field_rules.a("space.run_speed_mps"), field_rules.a("space.walk_speed_mps"), 0.5
    g = field_game(field_rules, [spec("Warrior")], [spec("Warrior")])
    a, b = g.players
    place(g, a, 20.0)
    place(g, b, 27.0)          # within charge distance: a runs at b
    assert _moved_in_one_tick(g, a) == pytest.approx(s_run * dt)
    g = field_game(field_rules, [spec("Warrior")], [spec("Warrior")])
    a, b = g.players
    place(g, a, 10.0)
    place(g, b, 50.0)          # far: a walks forward with its line
    g.space.line_u = [30.0, 30.0]
    assert _moved_in_one_tick(g, a) == pytest.approx(s_walk * dt)


@pytest.mark.parametrize("state", ["stopped", "frozen", "stunned", "insubstantial"])
def test_movement_states_keep_feet_still(field_rules, state):
    g = field_game(field_rules, [spec("Warrior")], [spec("Warrior")])
    a, b = g.players
    place(g, a, 20.0)
    place(g, b, 27.0)
    g.apply_state(a, state, g.t + 60)
    assert g.space._speed_cap(a) == 0.0
    assert _moved_in_one_tick(g, a) == 0.0


def test_incanting_player_stands_chanting_player_moves(field_rules):
    from sim.engine.state import Cast
    g = field_game(field_rules, [spec("Warrior")], [spec("Warrior")])
    a, b = g.players
    place(g, a, 20.0)
    place(g, b, 27.0)
    u = next(iter(a.uses.values())) if a.uses else None
    a.casting = Cast(u, b.pid, 5.0)
    assert _moved_in_one_tick(g, a) == 0.0
    a.casting = None
    assert _moved_in_one_tick(g, a) > 0.0      # a Chant is an Enchantment, not a cast: no hold


def test_leg_wound_crawls_near_enemies_and_hobbles_away_from_them(field_rules):
    """combat-rules.md, Hit Locations: a leg wound kneels (moves on the knees) or posts; with no
    living enemy within 20' the player may hobble, one step a second."""
    g = field_game(field_rules, [spec("Warrior")], [spec("Warrior")])
    a, b = g.players
    a.wounds.add("left_leg")
    place(g, a, 20.0)
    place(g, b, 25.0)
    assert g.space._speed_cap(a) == field_rules.a("space.crawl_speed_mps")
    assert _moved_in_one_tick(g, a) == pytest.approx(field_rules.a("space.crawl_speed_mps") * g.dt)
    place(g, b, 40.0)
    assert g.space._speed_cap(a) == field_rules.a("space.hobble_speed_mps")
    a.wounds.clear()
    assert g.space._speed_cap(a) == field_rules.a("space.run_speed_mps")


def _rejoin_seconds(rules):
    """A Warrior respawns at base and walks back; an enemy stands Stopped at midfield. Seconds
    until the Warrior is within 50' of it."""
    g = field_game(rules, [spec("Warrior")], [spec("Warrior")], game_type="attrition", lives=None)
    a, b = g.players
    place(g, b, g.space.L / 2)
    g.apply_state(b, "stopped", 10_000)
    g.space.line_u = [g.space.deploy_m, g.space.deploy_m]
    a.alive = False
    g.respawn(a)
    assert a.on_field(g.t) and g.space.u_of(a.pid, 0) <= 2.0          # at base, not a timer
    for _ in range(400):
        g.step()
        if g.space.rejoins:
            return g.space.rejoins[0]
    raise AssertionError("never rejoined")


def test_respawn_travel_time_grows_with_field_length():
    short, long_ = _rejoin_seconds(_rules(field_length_m=40.0)), _rejoin_seconds(_rules(field_length_m=80.0))
    assert long_ > short + 10.0
    # about the extra 20 m to midfield at walking pace
    assert long_ - short == pytest.approx(20.0 / 1.4, rel=0.25)


def test_send_to_base_takes_the_walk(field_rules):
    g = field_game(field_rules, [spec("Warrior")], [spec("Warrior")])
    a, _ = g.players
    place(g, a, 28.0)
    assert g.arrival_time(a) == pytest.approx(g.t + 28.0 / field_rules.a("space.walk_speed_mps"))
    g.send_to_base(a)
    assert not a.on_field(g.t) and g.space.u_of(a.pid, 0) <= 2.0


# ---------------------------------------------------------------- steering

def test_caster_keeps_distance_from_an_approaching_fighter(field_rules):
    """A Wizard (no abilities, so only steering acts) backs off from a Warrior running at them and
    is never caught while there is room to retreat."""
    everything = frozenset(field_rules.abilities)
    g = field_game(field_rules, [spec("Wizard")], [spec("Warrior")], ablate=everything)
    wiz, war = g.players
    assert style(wiz) == "caster" and style(war) == "line"
    place(g, wiz, 40.0)
    place(g, war, 52.0)
    xs, gaps, retreats = [], [], 0
    for _ in range(12):            # 6 s: the Warrior closes to charge range, the Wizard retreats
        g.step()
        xs.append(g.space.x[wiz.pid])
        gaps.append(g.space.distance(wiz, war))
        retreats += g.space.retreating(wiz)
        assert war.target is None and wiz.target is None
    assert retreats > 0
    assert xs[-1] < 40.0                                    # toward their own base
    assert min(gaps) >= g.space.reach[war.pid]             # never within the Warrior's reach
    assert gaps[-1] >= field_rules.a("space.retreat_trigger_m") - field_rules.a("space.run_speed_mps")


def test_retreating_caster_starts_no_incantation(field_rules):
    g = field_game(field_rules, [spec("Wizard", level=6)], [spec("Warrior")])
    wiz, war = g.players
    place(g, wiz, 40.0)
    place(g, war, 44.0)
    assert g.space.retreating(wiz)
    for _ in range(4):
        g.step()
        assert wiz.casting is None


def test_base_protects_fresh_arrivals_only(field_rules):
    g = field_game(field_rules, [spec("Warrior")], [spec("Warrior")])
    a, b = g.players
    place(g, a, 2.0)
    g.space._fresh.add(a.pid)
    assert g.space.in_base(a)
    place(g, a, 10.0)
    assert not g.space.in_base(a)
    place(g, a, 2.0)
    assert not g.space.in_base(a)                           # running back to base is no refuge


# ---------------------------------------------------------------- runs, determinism, calibration

def test_field_game_plays_and_reports(field_rules):
    from sim.scenarios import generate
    cfg = load_config("small")
    g = Game(field_rules, generate(3, cfg, field_rules), 3, space="on")
    res = g.run()
    assert res["winner"] in (-1, 0, 1) and res["space"]["rejoin_n"] >= 0
    assert all(0.0 <= x <= g.space.L for x in g.space.x) and all(0.0 <= y <= g.space.W for y in g.space.y)


_DIGEST_SNIPPET = """
import importlib.util, json, sys
s = importlib.util.spec_from_file_location("r", "tests/sim/data/record_digests.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
from sim.rules.compile import default_rules
from sim.scenarios import load_config
r = default_rules(); cfg = load_config("small")
print(json.dumps([m.digest(r, seed, cfg, space="on") for seed in (1, 2, 3)]))
"""


def test_field_is_deterministic_across_hash_seeds():
    outs = []
    for hs in ("0", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": hs, "PYTHONPATH": str(ROOT)}
        out = subprocess.run([sys.executable, "-c", _DIGEST_SNIPPET], cwd=ROOT, env=env, check=True,
                             capture_output=True, text=True).stdout
        outs.append(json.loads(out.strip().splitlines()[-1]))
    assert outs[0] == outs[1]


def test_run_games_with_space_on_carries_the_flag():
    from sim.run import run_games
    res = run_games([1, 2], load_config("small"), workers=1, space="on")
    assert all("space" in r for r in res)
    off = run_games([1, 2], load_config("small"), workers=1)
    assert all("space" not in r for r in off)


def test_space_group_does_not_make_the_calibration_stale(tmp_path):
    """The calibration fingerprint leaves out the space group: editing it doesn't make the space-off
    calibration stale, and a run with space on warns instead."""
    from sim.policies import calibration
    a = json.loads(ASSUMPTIONS_JSON.read_text())
    before = calibration.fingerprint()
    a["space"]["run_speed_mps"]["value"] = 9.9
    p = tmp_path / "assumptions.json"
    p.write_text(json.dumps(a, indent=2) + "\n")
    assert calibration.fingerprint(p) == before
    a["melee"]["base_hit_per_second"]["value"] = 0.5
    p.write_text(json.dumps(a, indent=2) + "\n")
    assert calibration.fingerprint(p) != before
    assert calibration.space_warning("on") and calibration.space_warning("off") is None


def test_space_assumptions_are_documented():
    group = json.loads(ASSUMPTIONS_JSON.read_text())["space"]
    for name, entry in group.items():
        if name.startswith("_"):
            continue
        assert {"value", "unit", "assumption", "why"} <= set(entry), name
        assert entry["assumption"] is True and entry["why"], name
    assert 20 * FOOT == pytest.approx(6.096)
