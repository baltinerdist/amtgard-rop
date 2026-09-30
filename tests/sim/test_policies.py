"""Scripted player choices (sim/policies): the situations each routine is for."""
import copy

import pytest

from sim.engine.state import Cast, Uses
from sim.policies import _enchant_targets, _try_charge, decide, keep_casting
from sim.rules.compile import build_rules

from .conftest import make_game, spec


def give(g, p, slug, rng="Self", n=1, unit=None, charge=None, clear=True):
    if clear:
        p.uses = {}
    ab = g.rules.abilities[slug]
    p.uses[slug] = Uses(ab, "life", n, n, charge, unit, True, range=rng)
    return p.uses[slug]


def decide_until_cast(g, p, tries=40):
    for _ in range(tries):
        decide(g, p)
        if p.casting is not None:
            return p.casting
    return None


def test_fighter_rages_before_a_fight(rules):
    g = make_game(rules, [spec("Barbarian", 3)], [spec("Warrior")])
    p = g.players[0]
    give(g, p, "rage")
    c = decide_until_cast(g, p)
    assert c is not None and c.uses.slug == "rage"


def test_caster_barrages_with_balls_in_hand(rules):
    g = make_game(rules, [spec("Wizard", 6)], [spec("Warrior")])
    p = g.players[0]
    give(g, p, "elemental-barrage")
    give(g, p, "lightning-bolt", n=3, unit="balls", clear=False)
    p.barrage = None
    decide(g, p)
    assert p.casting is not None and p.casting.uses.slug == "elemental-barrage"


def test_shake_it_off_when_stopped(rules):
    g = make_game(rules, [spec("Barbarian", 3)], [spec("Warrior")])
    p = g.players[0]
    give(g, p, "shake-it-off")
    g.apply_state(p, "stopped", g.t + 30)
    c = decide_until_cast(g, p)
    assert c is not None and c.uses.slug == "shake-it-off"


def test_caster_blinks_out_when_attacked_and_keeps_casting_it(rules):
    g = make_game(rules, [spec("Wizard", 3)], [spec("Warrior")])
    wiz, foe = g.players
    give(g, wiz, "blink")
    foe.target = wiz.pid
    decide(g, wiz)
    assert wiz.casting is not None and wiz.casting.uses.slug == "blink"
    assert keep_casting(g, wiz)


def test_attacked_caster_abandons_other_incantations(rules):
    g = make_game(rules, [spec("Wizard", 3)], [spec("Warrior")])
    wiz, foe = g.players
    u = give(g, wiz, "lightning-bolt", rng="20'", n=3, unit="balls")
    wiz.casting = Cast(u, foe.pid, 7)
    assert keep_casting(g, wiz)
    foe.target = wiz.pid
    assert not keep_casting(g, wiz)


def test_support_martyrs_for_a_stunned_fighter(rules):
    g = make_game(rules, [spec("Healer", 3), spec("Warrior")], [spec("Warrior")])
    healer, ally, _ = g.players
    give(g, healer, "martyr", rng="Other")
    g.apply_state(ally, "stunned", g.t + 30)
    c = decide_until_cast(g, healer)
    assert c is not None and c.uses.slug == "martyr" and c.target == ally.pid


def test_fighter_does_not_martyr(rules):
    g = make_game(rules, [spec("Paladin", 6), spec("Warrior")], [spec("Warrior")])
    pal, ally, _ = g.players
    give(g, pal, "martyr", rng="Other")
    g.apply_state(ally, "stunned", g.t + 30)
    assert decide_until_cast(g, pal) is None


def test_circle_of_protection_lifts_an_allys_state(rules):
    g = make_game(rules, [spec("Healer", 4), spec("Warrior")], [spec("Warrior")])
    healer, ally, _ = g.players
    give(g, healer, "circle-of-protection", rng="Touch")
    g.apply_state(ally, "stopped", g.t + 30)
    c = decide_until_cast(g, healer)
    assert c is not None and c.uses.slug == "circle-of-protection"


def test_mend_repairs_damaged_armor(rules):
    g = make_game(rules, [spec("Druid", 1), spec("Warrior")], [spec("Warrior")])
    druid, ally, _ = g.players
    give(g, druid, "mend", rng="Touch", n=2)
    ally.armor_max = 3
    ally.armor = {l: 3 for l in ally.armor}
    ally.armor["torso"] = 1
    c = decide_until_cast(g, druid)
    assert c is not None and c.uses.slug == "mend" and c.target == ally.pid


def test_caster_with_a_bow_shoots(rules):
    g = make_game(rules, [spec("Druid", 6)], [spec("Warrior")])
    p = g.players[0]
    p.uses = {}
    p.has_bow = True
    decide(g, p)
    assert p.next_shot_at > g.t


def test_gift_of_air_goes_to_casters_not_fighters(rules):
    g = make_game(rules, [spec("Druid", 5), spec("Warrior"), spec("Wizard")], [spec("Warrior")])
    druid, warrior, wizard, _ = g.players
    u = give(g, druid, "gift-of-air", rng="Other")
    for q in (warrior, wizard):
        q.enchantments = [e for e in q.enchantments if e.trait]
    targets = _enchant_targets(g, druid, u, at_base=False)
    assert wizard in targets and warrior not in targets


@pytest.fixture(scope="module")
def eager_rules(rules):
    a = copy.deepcopy(rules.assumptions)
    a["policy"]["p_charge_when_safe"]["value"] = 1.0
    return build_rules(assumptions=a)


def test_fighters_charge_only_in_a_lull(eager_rules):
    g = make_game(eager_rules, [spec("Anti-Paladin", 4)], [spec("Warrior")])
    ap, foe = g.players
    u = give(g, ap, "brutal-strike", rng="Unlimited", charge=10)
    u.left = 0
    assert not _try_charge(g, ap), "an enemy is on the field"
    foe.at_base_until = g.t + 60
    assert _try_charge(g, ap)
    assert ap.casting.kind == "charge"


def test_casters_leave_long_charges_for_a_lull(eager_rules):
    g = make_game(eager_rules, [spec("Druid", 1), spec("Warrior")], [spec("Warrior")])
    druid, ally, foe = g.players
    u = give(g, druid, "barkskin", rng="Other", charge=10)
    u.left = 0
    ally.enchantments = [e for e in ally.enchantments if e.trait]
    assert not _try_charge(g, druid), "Charge x10 is 80 s: wait for a lull"
    foe.at_base_until = g.t + 60
    assert _try_charge(g, druid)
