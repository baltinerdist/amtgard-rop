"""Doctrine play styles (sim/policies) and assist attribution (sim/engine/game.py) on small,
hand-built games."""
import copy

import pytest

from sim.policies import _enchant_priority, _try_control, _try_finish, _try_setup, decide
from sim.rules.compile import build_rules

from .conftest import make_game, resolve, spec
from .test_policies import give


@pytest.fixture(scope="module")
def near_rules(rules):
    """Every target in range, so the choice of target is the policy's alone."""
    a = copy.deepcopy(rules.assumptions)
    a["range"]["p_in_range"]["value"] = {k: 1.0 for k in a["range"]["p_in_range"]["value"]}
    a["range"]["p_ally_nearby_for_touch"]["value"] = 1.0
    return build_rules(assumptions=a)


def _clear(g):
    for p in g.players:
        p.uses = {}
        p.enchantments = [e for e in p.enchantments if e.trait]


def _controller_game(near_rules):
    g = make_game(near_rules, [spec("Wizard", 4), spec("Warrior")],
                  [spec("Wizard"), spec("Warrior", skill=1.0), spec("Warrior")])
    _clear(g)
    wiz, mate, foe_caster, strong, engaged = g.players
    wiz.play = "controller"
    give(g, wiz, "hold-person", rng="20'", n=3)
    return g, wiz, mate, foe_caster, strong, engaged


def test_controller_locks_down_the_enemy_on_a_teammate(near_rules):
    g, wiz, mate, _, strong, engaged = _controller_game(near_rules)
    engaged.target = mate.pid                # fighting the controller's teammate
    assert _try_control(g, wiz)
    assert wiz.casting.uses.slug == "hold-person" and wiz.casting.target == engaged.pid


def test_controller_otherwise_takes_the_most_dangerous_enemy(near_rules):
    g, wiz, _, foe_caster, strong, _ = _controller_game(near_rules)
    assert _try_control(g, wiz)
    assert wiz.casting.target == strong.pid, "a skilled fighter before a caster or a weaker fighter"


def test_controller_skips_locked_down_and_immune_enemies(near_rules):
    g, wiz, mate, foe_caster, strong, engaged = _controller_game(near_rules)
    engaged.target = mate.pid
    g.apply_state(engaged, "stopped", g.t + 30)                           # already locked down
    school = near_rules.abilities["hold-person"].school
    strong.traits.append(next(a for a in near_rules.abilities.values() if a.delivery == "trait" and any(
        e.kind == "defense.immunity" and e.params.get("school") == school for e in a.effects)))
    assert g.immune(strong, school)
    assert _try_control(g, wiz)
    assert wiz.casting.target not in (engaged.pid, strong.pid)


def test_finisher_goes_first_on_the_casters_own_set_up(near_rules):
    g = make_game(near_rules, [spec("Wizard", 4), spec("Wizard", 4)], [spec("Warrior"), spec("Warrior")])
    _clear(g)
    wiz, mate, a, b = g.players
    wiz.play = "striker"
    give(g, wiz, "force-bolt", rng="20'", n=3, unit="balls")
    give(g, wiz, "dragged-below", rng="20'", clear=False)
    resolve(g, mate, "hold-person", a)          # a teammate's Stop
    resolve(g, wiz, "hold-person", b)           # the caster's own
    assert a.has_state("stopped", g.t) and b.state_src["stopped"] == wiz.pid
    decide(g, wiz)
    assert wiz.casting.uses.slug == "dragged-below" and wiz.casting.target == b.pid


def test_any_wound_finishes_a_fragile_enemy(near_rules):
    g = make_game(near_rules, [spec("Wizard", 4)], [spec("Warrior"), spec("Warrior", skill=2.0)])
    _clear(g)
    wiz, fragile, strong = g.players
    give(g, wiz, "wounding", rng="20'")
    g.apply_state(fragile, "fragile", g.t + 60)
    assert _try_finish(g, wiz)
    assert wiz.casting.target == fragile.pid, "the Fragile enemy, not the more dangerous one"


def test_combo_doctrine_sets_up_its_own_finisher(near_rules):
    g = make_game(near_rules, [spec("Wizard", 4)], [spec("Warrior")])
    _clear(g)
    wiz, foe = g.players
    wiz.play, wiz.combos = "striker", (("hold-person", "dragged-below"),)
    give(g, wiz, "hold-person", rng="20'")
    give(g, wiz, "dragged-below", rng="20'", clear=False)
    assert not _try_finish(g, wiz), "nothing to finish yet"
    assert _try_setup(g, wiz) and wiz.casting.uses.slug == "hold-person"
    g._complete(wiz)
    assert foe.state_src["stopped"] == wiz.pid
    decide(g, wiz)
    assert wiz.casting.uses.slug == "dragged-below" and wiz.casting.target == foe.pid


def test_enchantments_go_to_who_benefits_most(near_rules):
    g = make_game(near_rules, [spec("Druid", 4), spec("Wizard"), spec("Warrior", skill=-1.0),
                               spec("Warrior", skill=1.0)], [spec("Warrior")])
    _clear(g)
    druid, wiz, weak, best, _ = g.players
    targets = [druid, wiz, weak, best]
    flame = give(g, druid, "flame-blade", rng="Other")
    bark = give(g, druid, "barkskin", rng="Other", clear=False)
    assert _enchant_priority(g, flame, targets) is best, "a weapon Enchantment to the best melee fighter"
    wiz.play = "battle"                          # a battle caster stands in the front line too
    assert _enchant_priority(g, bark, [druid, wiz, weak]) in (wiz, weak)
    assert _enchant_priority(g, bark, [druid, weak]) is weak, "armor to the front line"


# ---------------------------------------------------------------- assists and saves

def _trio(rules):
    g = make_game(rules, [spec("Druid", 4), spec("Warrior"), spec("Wizard", 4)], [spec("Warrior"), spec("Warrior")])
    return g, g.players


def test_enchant_assist(rules):
    g, (druid, warrior, wiz, foe, foe2) = _trio(rules)
    resolve(g, druid, "barkskin", warrior, rng="Other")
    assert any(e.ability.slug == "barkskin" and e.caster == druid.pid for e in warrior.enchantments)
    g.kill(foe, warrior, "melee")
    assert (warrior.kills, druid.enchant_assists, wiz.enchant_assists) == (1, 1, 0)
    g.kill(warrior, foe2, "melee")               # an enemy's kill earns the druid nothing
    assert druid.enchant_assists == 1


def test_control_assist_at_death_and_within_ten_seconds(rules):
    g, (druid, warrior, wiz, foe, foe2) = _trio(rules)
    resolve(g, wiz, "hold-person", foe)
    assert foe.state_src["stopped"] == wiz.pid
    g.kill(foe, warrior, "melee")
    assert wiz.control_assists == 1 and druid.control_assists == 0
    # a State lifted early still counts for 10 s, not after
    resolve(g, wiz, "hold-person", foe2)
    g._upkeep()
    foe2.states.pop("stopped")
    g.t += 9
    g.kill(foe2, warrior, "melee")
    assert wiz.control_assists == 2
    g.respawn(foe2)
    resolve(g, wiz, "hold-person", foe2)
    g._upkeep()
    foe2.states.pop("stopped")
    g.t += 11
    g.kill(foe2, warrior, "melee")
    assert wiz.control_assists == 2


def test_no_control_assist_for_the_casters_own_kill(rules):
    g, (druid, warrior, wiz, foe, _) = _trio(rules)
    resolve(g, wiz, "hold-person", foe)
    g.kill(foe, wiz, "dragged-below")
    assert wiz.kills == 1 and wiz.control_assists == 0


def test_restriction_counts_as_control(rules):
    g = make_game(rules, [spec("Bard", 4), spec("Warrior")], [spec("Warrior")])
    bard, warrior, foe = g.players
    resolve(g, bard, "insult", foe)
    assert any(r.src == bard.pid for r in foe.restrictions)
    g.kill(foe, warrior, "melee")
    assert bard.control_assists == 1


def test_saves_heal_revive_and_death_prevented(rules):
    g = make_game(rules, [spec("Healer", 6), spec("Warrior"), spec("Druid", 6)], [spec("Warrior")])
    healer, warrior, druid, foe = g.players
    warrior.wounds.add("left_arm")
    resolve(g, healer, "heal", warrior, rng="Touch")
    assert not warrior.wounds and healer.saves == 1
    healer.wounds.add("left_leg")
    resolve(g, healer, "heal", healer, rng="Self")
    assert healer.saves == 1, "healing yourself is not a save"
    warrior.wounds.add("left_leg")
    g.kill(warrior, foe, "melee")
    resolve(g, healer, "resurrect", warrior, rng="Touch")
    assert warrior.alive and healer.saves == 2, "a revive with its heal is one save"
    resolve(g, druid, "troll-blood", warrior, rng="Other")
    g.kill(warrior, foe, "melee")
    assert warrior.alive and druid.saves == 1
    assert foe.kills == 1


def test_assists_reach_the_results(rules):
    g, (druid, warrior, wiz, foe, _) = _trio(rules)
    resolve(g, druid, "barkskin", warrior, rng="Other")
    resolve(g, wiz, "hold-person", foe)
    g.kill(foe, warrior, "melee")
    rows = {r["pid"]: r for r in g.result(-1)["players"]}
    assert rows[druid.pid]["enchant_assists"] == 1 and rows[wiz.pid]["control_assists"] == 1
    assert rows[foe.pid]["lives"] == 2, "one death and not out: on the second life"
    assert rows[druid.pid]["doctrine"] == druid.doctrine
