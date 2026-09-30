"""The usefulness score (sim/policies/value.py): enablers valued by what they enable, drawbacks
priced in context, no recursion blow-up, direct scores unchanged."""
import dataclasses
import math

import pytest

from sim.policies import buy
from sim.policies.value import Ctx, Held, Kit, breakdown, drawback_cost, stack_share, value
from sim.rules.compile import build_rules


@pytest.fixture(scope="module")
def fresh():
    """Rules with their own memo, so values here don't depend on what other tests computed."""
    return build_rules()


def _grant(rules, name: str, frequency: str):
    """Poison Glands with its grant pointed at another ability."""
    base = rules.abilities["poison-glands"]
    effs = tuple(dataclasses.replace(e, params={**e.params, "ability": name, "frequency": frequency})
                 if e.kind == "ability.grant" else e for e in base.effects)
    return dataclasses.replace(base, slug=f"test-grant-{name.lower().replace(' ', '-')}-{frequency}", effects=effs)


def _twenty_foot_verbal(rules) -> str:
    return next(s for s, a in sorted(rules.abilities.items())
                if a.delivery == "verbal" and a.range == "20'" and value(a, "caster", rules=rules) > 3)


# ---------------------------------------------------------------- enablers track their targets

def test_grant_of_a_stronger_ability_is_worth_more(fresh):
    strong, weak = fresh.abilities["fireball"], fresh.abilities["mend"]
    assert value(strong, "caster", rules=fresh) > value(weak, "caster", rules=fresh)
    g_strong = value(_grant(fresh, "Fireball", "1/Life (m)"), "caster", rules=fresh)
    g_weak = value(_grant(fresh, "Mend", "1/Life (m)"), "caster", rules=fresh)
    assert g_strong > g_weak > 0
    # the grant is the granted ability's value at the granted frequency
    assert g_strong == pytest.approx(value(strong, "caster", rules=fresh))


def test_grant_frequency_scales_the_value(fresh):
    one = value(_grant(fresh, "Heal", "1/Life (m)"), "fighter", rules=fresh)
    two = value(_grant(fresh, "Heal", "2/Life (m)"), "fighter", rules=fresh)
    unlimited = value(_grant(fresh, "Heal", "Unlimited (m)"), "fighter", rules=fresh)
    heal = value(fresh.abilities["heal"], "fighter", rules=fresh)
    assert one == pytest.approx(heal)
    assert two == pytest.approx(heal * (1 + buy.COPY_DECAY))
    assert unlimited == pytest.approx(heal * buy.UNLIMITED_FACTOR)


def test_named_enablers_follow_their_targets(fresh):
    # Regeneration grants Heal (Self) Unlimited; Troll Blood is "as per Regeneration"
    regen = value(fresh.abilities["regeneration"], "caster", rules=fresh)
    assert regen > 0
    parts = {i: c for i, _, c in breakdown(fresh.abilities["troll-blood"], "caster", rules=fresh)}
    assert parts["e5"] == pytest.approx(regen)
    # strips: the ability times held_worth(strips)
    triage = {i: c for i, _, c in breakdown(fresh.abilities["battlefield-triage"], "caster", rules=fresh)}
    heal = value(fresh.abilities["heal"], "caster", rules=fresh)
    assert triage["e1"] == pytest.approx(heal * (1 + 0.6 + 0.36))       # three strips


def test_extra_slot_is_worth_stacking_the_best_enchantment_the_caster_holds(fresh):
    attuned = fresh.abilities["attuned"]
    weak = Kit("caster", (Held("barkskin"),))
    strong = Kit("caster", (Held("barkskin"), Held("flame-blade")))
    none = Kit("caster", (Held("fireball"),))
    v_weak = value(attuned, "caster", Ctx(holder=weak), fresh)
    v_strong = value(attuned, "caster", Ctx(holder=strong), fresh)
    assert value(attuned, "caster", Ctx(holder=none), fresh) == 0.0
    # only the stacking counts: the filler could otherwise go on another teammate
    share = stack_share(fresh)
    assert 0.0 < share <= 1.0
    assert v_weak == pytest.approx(share * value(fresh.abilities["barkskin"], "caster", rules=fresh))
    assert v_strong == pytest.approx(share * value(fresh.abilities["flame-blade"], "caster", rules=fresh))


def test_refills_follow_the_spent_ability(fresh):
    confidence = fresh.abilities["confidence"]
    big = value(confidence, "caster", Ctx(spent="fireball"), fresh)
    small = value(confidence, "caster", Ctx(spent="mend"), fresh)
    assert big > small > 0


def test_meta_magic_follows_the_kit(fresh):
    ext = fresh.abilities["extension"]
    verbal = _twenty_foot_verbal(fresh)
    assert value(ext, "caster", Ctx(holder=Kit("caster", (Held("fireball"),))), fresh) == 0.0
    with_verbal = value(ext, "caster", Ctx(holder=Kit("caster", (Held(verbal, range="20'"),))), fresh)
    table = fresh.a("range.p_in_range")
    share = 1 - table["20'"] / table["50'"]
    assert with_verbal == pytest.approx(share * value(fresh.abilities[verbal], "caster", rules=fresh))


# ---------------------------------------------------------------- context changes the value

def test_amplification_is_worth_less_to_a_bearer_with_extension(fresh):
    amp = fresh.abilities["amplification"]
    verbal = _twenty_foot_verbal(fresh)
    plain = Kit("caster", (Held(verbal, range="20'"),))
    has_ext = Kit("caster", (Held(verbal, range="20'"), Held("extension")))
    without = value(amp, "caster", Ctx(bearer=plain), fresh)
    with_ext = value(amp, "caster", Ctx(bearer=has_ext), fresh)
    assert without > with_ext >= 0
    # the restriction costs exactly the bearer's own Extension
    ext = value(fresh.abilities["extension"], "caster", Ctx(holder=has_ext), fresh)
    assert drawback_cost(amp, "caster", ctx=Ctx(bearer=has_ext), rules=fresh) == pytest.approx(ext)
    assert drawback_cost(amp, "caster", ctx=Ctx(bearer=plain), rules=fresh) == 0.0
    # a bearer with no 20' Verbal gets nothing from it
    assert value(amp, "caster", Ctx(bearer=Kit("fighter")), fresh) == 0.0


# ---------------------------------------------------------------- drawbacks priced as described

def test_song_of_power_stopped_costs_little_for_a_backline_bard(fresh):
    sop = fresh.abilities["song-of-power"]
    back = Kit("caster", play="controller")
    line = Kit("caster", play="battle")
    cost_back = drawback_cost(sop, "caster", ctx=Ctx(holder=back), rules=fresh)
    cost_line = drawback_cost(sop, "caster", ctx=Ctx(holder=line), rules=fresh)
    assert cost_back < cost_line == pytest.approx(4.0)
    assert value(sop, "caster", Ctx(holder=back), fresh) > 0
    assert value(sop, "caster", rules=fresh) > 0


def test_dropping_enchantments_when_attuned_ends_costs_nothing_at_cast(fresh):
    assert drawback_cost(fresh.abilities["attuned"], "caster", rules=fresh) == 0.0
    graft = {i: c for i, _, c in breakdown(fresh.abilities["essence-graft"], "caster", rules=fresh)}
    assert graft["e3"] == 0.0          # the drop on removal
    assert graft["e2"] < 0             # "only (m) Enchantments from the caster" still costs


def test_undead_minion_prices_the_respawn_by_game_type(fresh):
    um = fresh.abilities["undead-minion"]
    ann = value(um, "support", Ctx(game_type="annihilation"), fresh)
    att = value(um, "support", Ctx(game_type="attrition"), fresh)
    mixed = value(um, "support", rules=fresh)
    assert ann > mixed > att > 0
    # the unlimited Raise Dead on one player is worth one copy of Raise Dead
    parts = {i: c for i, _, c in breakdown(um, "support", rules=fresh)}
    assert parts["e3"] == pytest.approx(value(fresh.abilities["raise-dead"], "support", rules=fresh))


def test_equipment_restrictions_use_the_real_kit(fresh):
    berserker = fresh.abilities["berserker"]
    armored = Kit("fighter", armor_max=3)
    bare = Kit("fighter", armor_max=0)
    assert drawback_cost(berserker, "fighter", ctx=Ctx(holder=bare, bearer=bare), rules=fresh) < \
        drawback_cost(berserker, "fighter", ctx=Ctx(holder=armored, bearer=armored), rules=fresh)
    # an Archetype that removes an ability costs only what the player holds
    apex = fresh.abilities["apex"]
    holds = Kit("fighter", (Held("hold-person"),))
    assert drawback_cost(apex, "fighter", ctx=Ctx(holder=holds, bearer=holds), rules=fresh) > \
        drawback_cost(apex, "fighter", ctx=Ctx(holder=Kit("fighter"), bearer=Kit("fighter")), rules=fresh)


# ---------------------------------------------------------------- safety

def test_no_recursion_blow_up(fresh):
    for role in ("fighter", "archer", "caster", "support"):
        for ab in fresh.abilities.values():
            v = value(ab, role, rules=fresh)
            assert math.isfinite(v) and abs(v) < 100, (ab.slug, role, v)


def test_self_referential_enablers_are_finite(fresh):
    # an Enchantment that grants itself, and Empower valued as a refill of Empower
    loop = _grant(fresh, "Poison Glands", "Unlimited (ex)")
    loop = dataclasses.replace(loop, slug="poison-glands")
    assert math.isfinite(value(loop, "caster", rules=fresh))
    assert math.isfinite(value(fresh.abilities["empower"], "caster", Ctx(spent="empower"), fresh))


def test_values_do_not_depend_on_call_order():
    a, b = build_rules(), build_rules()
    order = ["attuned", "essence-graft", "evolution", "troll-blood", "void-touched", "phoenix-tears"]
    first = {s: value(a.abilities[s], "caster", rules=a) for s in order}
    second = {s: value(b.abilities[s], "caster", rules=b) for s in reversed(order)}
    assert first == second


def test_direct_offense_and_healing_scores_are_unchanged(fresh):
    snapshot = {("fireball", "caster"): 18.0, ("heal", "support"): 6.0, ("heal", "caster"): 4.0,
                ("raise-dead", "support"): 12.5, ("resurrect", "support"): 17.5,
                ("call-lightning", "caster"): 13.0, ("lightning-bolt", "caster"): 13.5,
                ("flame-blade", "caster"): 9.5, ("barkskin", "caster"): 2.0, ("stun", "caster"): 6.0,
                ("greater-heal", "support"): 6.0, ("finger-of-death", "caster"): 13.0}
    some_kit = Ctx(holder=Kit("caster", (Held("attuned"), Held("extension"))), bearer=Kit("fighter", armor_max=3),
                   game_type="attrition")
    for (slug, role), v in snapshot.items():
        assert value(fresh.abilities[slug], role, rules=fresh) == pytest.approx(v), slug
        assert value(fresh.abilities[slug], role, some_kit, fresh) == pytest.approx(v), slug


def test_nothing_is_bought_only_for_a_drawback(fresh):
    assert not buy.effective(fresh.abilities["battlemage"], fresh)
    # and no drawback turns into a benefit: every drawback contribution is a cost or nothing
    for ab in fresh.abilities.values():
        for role in ("fighter", "caster", "support"):
            bd = breakdown(ab, role, rules=fresh)
            assert all(c <= 0 for i, _, c in bd if any(
                e.id == i and e.polarity == "harm" and e.subject in ("caster", "bearer", "bearer-equipment", "group")
                for e in ab.effects)), ab.slug
