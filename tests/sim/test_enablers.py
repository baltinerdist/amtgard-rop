"""Enablers cast by situational utility (sim/policies/enablers.py) and the engine's refill hook
(Game.name_refill), on small hand-built games: per group, the best target is chosen, the cast is
skipped when its utility is below what the time would earn otherwise, and refills never go to a
dead or locked-down teammate."""
import copy

import pytest

from sim.engine.state import LOCATIONS, Uses
from sim.policies import _try_enchant, _try_refill, enablers
from sim.policies.utility import utility
from sim.policies.value import KIND_WEIGHT
from sim.rules.compile import build_rules

from .conftest import make_game, resolve, spec


@pytest.fixture(scope="module")
def near_rules(rules):
    """Every target in range and every teammate within reach, so choices are the policy's alone."""
    a = copy.deepcopy(rules.assumptions)
    a["range"]["p_in_range"]["value"] = {k: 1.0 for k in a["range"]["p_in_range"]["value"]}
    a["range"]["p_ally_nearby_for_touch"]["value"] = 1.0
    return build_rules(assumptions=a)


def _game(rules, team0, team1):
    g = make_game(rules, [spec(c, lv) for c, lv in team0], [spec(c, lv) for c, lv in team1])
    for p in g.players:
        p.uses = {}
        p.enchantments = [e for e in p.enchantments if e.trait]
        p.armor = {l: 0 for l in LOCATIONS}
    return g


def give(g, p, slug, rng="20'", n=1, left=None, per="life", charge=None):
    ab = g.rules.abilities[slug]
    p.uses[slug] = Uses(ab, per, n, n if left is None else left, charge, None, True, range=rng)
    return p.uses[slug]


def U(g, p, slug, q):
    return utility(g, p, g.rules.abilities[slug], q)


def finish(g, p):
    """Complete p's incantation now."""
    g._complete(p)


def away(g, *foes):
    """These enemies are at base: none to fight, so nothing else competes for the caster's time."""
    for q in foes:
        q.at_base_until = g.t + 60


# ---------------------------------------------------------------- 1. refills

def test_empower_goes_to_the_most_valuable_spent_use_and_restores_only_it(near_rules):
    g = _game(near_rules, [("Bard", 6), ("Wizard", 6), ("Wizard", 6)], [("Warrior", 1)])
    bard, a, b, foe = g.players
    away(g, foe)
    give(g, bard, "empower", rng="Other", n=2, per="refresh")
    bolt = give(g, a, "lightning-bolt", left=0)
    hold = give(g, a, "hold-person", left=0)
    give(g, b, "hold-person", left=0)
    assert U(g, bard, "empower", a) > U(g, bard, "empower", b) > 0
    assert _try_refill(g, bard) and bard.casting.target == a.pid
    finish(g, bard)
    assert bolt.left == 1 and hold.left == 0, "Empower: one use of the ability named, not every use"


def test_restoration_skips_empower_confidence_and_restoration(near_rules):
    """restoration.md: "Does not function on Empower, Confidence, or Restoration." """
    g = _game(near_rules, [("Bard", 6), ("Bard", 6)], [("Warrior", 1)])
    bard, q, foe = g.players
    away(g, foe)
    give(g, bard, "restoration", rng="Other", per="refresh")
    bolt = give(g, q, "hold-person", left=0)
    excluded = [give(g, q, s, rng="Other", left=0) for s in ("empower", "confidence", "restoration")]
    assert _try_refill(g, bard) and bard.casting.target == q.pid
    finish(g, bard)
    assert bolt.left == 1
    assert all(u.left == 0 for u in excluded)


def test_no_refill_for_a_dead_or_locked_down_teammate(near_rules):
    g = _game(near_rules, [("Bard", 6), ("Wizard", 6), ("Wizard", 6), ("Wizard", 6), ("Warrior", 6)],
              [("Warrior", 1)])
    bard, low, stunned, dead, void, foe = g.players
    away(g, foe)
    give(g, bard, "restoration", rng="Other", per="refresh")
    give(g, low, "hold-person", left=0)
    for q in (stunned, dead, void):
        give(g, q, "fireball", n=2, left=0)
    resolve(g, low, "void-touched", void, rng="Other")      # unaffected by Sorcery: Restoration fails on them
    g.apply_state(stunned, "stunned", g.t + 10)
    g.kill(dead, foe, "melee")
    assert U(g, bard, "restoration", stunned) == 0 and U(g, bard, "restoration", dead) == 0
    assert _try_refill(g, bard) and bard.casting.target == low.pid


def test_a_refill_waits_while_attacking_is_worth_more(near_rules):
    g = _game(near_rules, [("Bard", 6), ("Wizard", 6)], [("Warrior", 1)])
    bard, mate, foe = g.players
    give(g, bard, "confidence", rng="Other", per="refresh", charge=5)
    give(g, bard, "lightning-bolt")
    give(g, mate, "hold-person", left=0, charge=3)
    x = U(g, bard, "confidence", mate)
    assert 0 < x < enablers.time_cost(g, bard, 1.0), "an instant Charge is worth 0.12 of a Hold Person"
    assert not _try_refill(g, bard)
    away(g, foe)
    g.policy_cache.clear()
    assert _try_refill(g, bard) and bard.casting.target == mate.pid


def test_innate_charges_the_casters_best_spent_ability(near_rules):
    g = _game(near_rules, [("Wizard", 6), ("Wizard", 6)], [("Warrior", 1)])
    mate, wiz, foe = g.players          # the teammate first: ties go to the lowest pid
    away(g, foe)
    give(g, wiz, "innate", rng="20'", per="refresh")     # a loadout gives Meta-Magics a range
    ball = give(g, wiz, "fireball", left=0, charge=3)
    hold = give(g, wiz, "hold-person", left=0, charge=3)
    give(g, mate, "fireball", n=3, left=0, charge=3)
    assert U(g, wiz, "innate", mate) == U(g, wiz, "innate", wiz) > 0, "Innate only ever Charges its caster"
    assert _try_refill(g, wiz) and wiz.casting.uses.slug == "innate" and wiz.casting.target == wiz.pid
    finish(g, wiz)
    assert ball.left == 1 and hold.left == 0


def test_steal_life_essence_heals_a_wound_unless_the_charge_is_worth_more(near_rules, monkeypatch):
    g = _game(near_rules, [("Wizard", 6)], [("Warrior", 1)])
    wiz, foe = g.players
    ball = give(g, wiz, "fireball", left=0, charge=3)
    g.kill(foe, wiz, "melee")
    wiz.wounds.add("left_arm")
    resolve(g, wiz, "steal-life-essence", foe, rng="Touch")
    assert not wiz.wounds and ball.left == 0, "a wound healed (4) beats 0.12 of a Fireball"
    foe.states.clear()
    wiz.wounds.add("left_arm")
    monkeypatch.setitem(KIND_WEIGHT, "wound.heal", 0.1)
    g.policy_cache.clear()
    resolve(g, wiz, "steal-life-essence", foe, rng="Touch")
    assert wiz.wounds and ball.left == 1, "the caster named Fireball: the Charge option, not the heal"


# ---------------------------------------------------------------- 2. extra Enchantment slots

def test_attuned_goes_where_one_more_enchantment_adds_most(near_rules):
    g = _game(near_rules, [("Druid", 6), ("Warrior", 6), ("Warrior", 6)], [("Warrior", 1)])
    druid, full, free, foe = g.players
    give(g, druid, "attuned", rng="Other", per="refresh")
    give(g, druid, "barkskin", rng="Other", n=2)
    resolve(g, druid, "stoneskin", full, rng="Other")
    assert full.magical_enchantment_count() == full.ench_slots
    assert U(g, druid, "attuned", full) > 0 == U(g, druid, "attuned", free), \
        "a free slot takes the Barkskin anyway; only the full one gains by the extra slot"
    q, _ = enablers.best_target(g, druid, druid.uses["attuned"], [full, free])
    assert q is full


def test_attuned_counts_only_a_slot_someone_will_fill(near_rules):
    g = _game(near_rules, [("Druid", 6), ("Warrior", 6), ("Wizard", 6)], [("Warrior", 1)])
    druid, fighter, wiz, foe = g.players
    give(g, druid, "attuned", rng="Other", per="refresh")
    resolve(g, druid, "stoneskin", fighter, rng="Other")
    assert U(g, druid, "attuned", fighter) == 0, "no filler held by the caster or a teammate"
    give(g, wiz, "barkskin", rng="Other")
    g.policy_cache.clear()
    assert U(g, druid, "attuned", fighter) > 0, "a teammate caster nearby holds one"


def test_extra_slot_waits_for_a_quiet_moment_on_the_field(near_rules):
    g = _game(near_rules, [("Druid", 6), ("Warrior", 6)], [("Warrior", 1)])
    druid, fighter, foe = g.players
    give(g, druid, "attuned", rng="Other", per="refresh")
    give(g, druid, "stoneskin", rng="Other")
    give(g, druid, "lightning-bolt")
    resolve(g, druid, "barkskin", fighter, rng="Other")
    x = U(g, druid, "attuned", fighter)
    assert 0 < x < enablers.time_cost(g, druid, enablers.cast_seconds(g, druid.uses["attuned"]))
    assert not _try_enchant(g, druid, False, prioritized=True)
    for q in (druid, fighter):
        q.at_base_until = g.t + 30
    assert _try_enchant(g, druid, True, prioritized=True) and druid.casting.uses.slug == "attuned", \
        "at base nothing else competes for the time"


def test_essence_graft_avoids_a_teammate_it_would_strip(near_rules):
    g = _game(near_rules, [("Druid", 6), ("Druid", 6), ("Warrior", 6), ("Warrior", 6)], [("Warrior", 1)])
    druid, other, worn, bare = g.players[:4]
    give(g, druid, "essence-graft", rng="Other", per="refresh")
    give(g, druid, "barkskin", rng="Other", n=2)
    give(g, druid, "stoneskin", rng="Other")
    resolve(g, other, "stoneskin", worn, rng="Other")
    assert U(g, druid, "essence-graft", worn) < 0, "the Graft drops another caster's Stoneskin"
    q, _ = enablers.best_target(g, druid, druid.uses["essence-graft"], [worn, bare])
    assert q is bare


# ---------------------------------------------------------------- 3. Enchantments that grant an ability

def test_amplification_goes_to_a_holder_of_20ft_verbals_with_uses_left(rules):
    g = _game(rules, [("Wizard", 6), ("Wizard", 6), ("Warrior", 6)], [("Warrior", 1)])
    caster, wiz, fighter, foe = g.players
    give(g, caster, "amplification", rng="Touch", per="refresh")
    bolt = give(g, wiz, "hold-person", n=2)
    assert U(g, caster, "amplification", wiz) > 0 == U(g, caster, "amplification", fighter)
    bolt.left = 0
    g.policy_cache.clear()
    assert U(g, caster, "amplification", wiz) == 0, "nothing left to extend"


def test_silver_tongue_goes_to_a_holder_of_swiftable_abilities(near_rules):
    g = _game(near_rules, [("Wizard", 6), ("Healer", 6), ("Warrior", 6)], [("Warrior", 1)])
    caster, healer, fighter, foe = g.players
    give(g, caster, "silver-tongue", rng="Touch", per="refresh")
    give(g, healer, "heal", rng="Touch", n=2)
    assert U(g, caster, "silver-tongue", healer) > U(g, caster, "silver-tongue", fighter)


@pytest.mark.parametrize("slug", ["regeneration", "gift-of-water", "battlefield-triage"])
def test_heal_granting_enchantments_go_to_who_will_use_the_heal(near_rules, slug):
    g = _game(near_rules, [("Druid", 6), ("Warrior", 6), ("Wizard", 6), ("Healer", 6)], [("Warrior", 1)])
    druid, fighter, wiz, battle = g.players[:4]
    battle.play = "battle"
    give(g, druid, slug, rng="Other")
    back, line, battler = (U(g, druid, slug, q) for q in (wiz, fighter, battle))
    assert back > line, "a fighter under attack rarely heals (calibrated fighter_heal)"
    assert back > battler, "a battle caster fights in the line: its Heal is priced as a fighter's"


def test_granted_heal_skipped_when_attacking_is_worth_more(near_rules):
    g = _game(near_rules, [("Druid", 6), ("Warrior", 6)], [("Warrior", 1)])
    druid, fighter, foe = g.players
    give(g, druid, "regeneration", rng="Other")
    give(g, druid, "fireball", n=3)
    assert U(g, druid, "regeneration", fighter) <= enablers.time_cost(
        g, druid, enablers.cast_seconds(g, druid.uses["regeneration"]))
    assert not _try_enchant(g, druid, False, prioritized=True) or druid.casting.uses.slug != "regeneration"


# ---------------------------------------------------------------- 4. Undead Minion

def test_undead_minion_goes_to_the_teammate_most_likely_to_die_again(near_rules):
    g = _game(near_rules, [("Healer", 6), ("Warrior", 6), ("Wizard", 6)], [("Warrior", 1)])
    healer, fighter, wiz, foe = g.players
    healer.play = "medic"
    give(g, healer, "undead-minion", rng="Other", per="refresh")
    line, back = U(g, healer, "undead-minion", fighter), U(g, healer, "undead-minion", wiz)
    assert line > back and line > 0
    wiz.deaths = 6
    g.policy_cache.clear()
    assert U(g, healer, "undead-minion", wiz) > line, "deaths seen outweigh the role prior"


def test_undead_minion_weighs_the_casters_own_survival(near_rules):
    g = _game(near_rules, [("Healer", 6), ("Warrior", 6)], [("Warrior", 1)])
    healer, fighter, foe = g.players
    give(g, healer, "undead-minion", rng="Other", per="refresh")
    safe = U(g, healer, "undead-minion", fighter)
    healer.deaths = 8
    g.policy_cache.clear()
    assert U(g, healer, "undead-minion", fighter) < safe, "a caster who dies often raises less"


def test_undead_minion_skipped_below_the_alternative_and_at_the_cap(near_rules):
    g = _game(near_rules, [("Healer", 6), ("Warrior", 6), ("Warrior", 6), ("Warrior", 6), ("Warrior", 6)],
              [("Warrior", 1)])
    healer, *mates, foe = g.players
    minion = give(g, healer, "undead-minion", rng="Other", per="refresh")
    give(g, healer, "fireball", n=3)
    x = U(g, healer, "undead-minion", mates[0])
    assert 0 < x < enablers.time_cost(g, healer, enablers.cast_seconds(g, minion))
    assert not _try_enchant(g, healer, False, prioritized=True) or healer.casting.uses is not minion
    for q in mates[:3]:
        resolve(g, healer, "undead-minion", q, rng="Other")
    g.policy_cache.clear()
    assert U(g, healer, "undead-minion", mates[3]) == 0, "three Undead Minions at most"


# ---------------------------------------------------------------- 5. Self Enchantments aimed at enemies

def test_snaring_vines_cast_when_enemies_it_can_hold_are_coming(near_rules):
    g = _game(near_rules, [("Druid", 6)], [("Warrior", 1), ("Warrior", 1)])
    druid, *foes = g.players
    give(g, druid, "snaring-vines", rng="Self", per="refresh")
    assert U(g, druid, "snaring-vines", druid) > 0
    assert _try_enchant(g, druid, True, prioritized=True) and druid.casting.uses.slug == "snaring-vines"
    finish(g, druid)
    assert "hold-person" in {u.slug for u in druid.uses.values() if u.ench is not None}
    for q in foes:
        q.out = True
        q.alive = False
    g.policy_cache.clear()
    assert U(g, druid, "snaring-vines", druid) == 0, "nobody left to hold"


def test_discordia_needs_enemies_who_cast_and_pays_for_the_song(near_rules):
    g = _game(near_rules, [("Bard", 6)], [("Warrior", 1), ("Wizard", 6)])
    bard, warrior, wiz = g.players
    bard.play = "controller"
    give(g, bard, "discordia", rng="Self", per="refresh")
    assert U(g, bard, "discordia", bard) == 0, "Break Concentration only matters to a caster"
    give(g, wiz, "lightning-bolt")
    g.policy_cache.clear()
    quiet = U(g, bard, "discordia", bard)
    assert quiet > 0
    assert _try_enchant(g, bard, True, prioritized=True) and bard.casting.uses.slug == "discordia"
    g.interrupt(bard, "abandoned")
    bard.uses["song-of-battle"] = Uses(g.rules.abilities["song-of-battle"], "unlimited", None, None, None, None,
                                       True, range="Self")
    warrior.armor = {l: 3 for l in LOCATIONS}
    bard.target, warrior.target = warrior.pid, bard.pid
    g.policy_cache.clear()
    assert U(g, bard, "discordia", bard) < quiet, "the Enchantment keeps the song off the slot"
