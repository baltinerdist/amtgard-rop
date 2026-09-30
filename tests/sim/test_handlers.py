"""One test per engine handler, each on real ability records with fixed seeds."""
from sim.engine.state import INF, LOCATIONS
from tests.sim.conftest import make_game, resolve, spec


def pair(rules, a="Wizard", b="Warrior", seed=1):
    g = make_game(rules, [spec(a)], [spec(b)], seed=seed)
    return g, g.players[0], g.players[1]


def test_death_cause_kills(rules):
    g, wiz, war = pair(rules)
    resolve(g, wiz, "finger-of-death", war)
    assert not war.alive and war.deaths == 1 and wiz.kills == 1
    assert g.applied[("finger-of-death", "death.cause")] == 1


def test_immunity_trait_blocks_school(rules):
    g, wiz, pal = pair(rules, b="Paladin")
    assert g.immune(pal, "Death")
    resolve(g, wiz, "finger-of-death", pal)
    assert pal.alive
    assert g.fails[("finger-of-death", "immune")] == 1


def test_torso_wound_kills_and_limb_wound_does_not(rules):
    g, wiz, war = pair(rules)
    war.armor = {l: 0 for l in LOCATIONS}
    g.hit(war, wiz, "melee", location="left_leg")
    assert war.alive and war.wounds == {"left_leg"}
    g.hit(war, wiz, "melee", location="right_arm")
    assert not war.alive, "two wounds is a death"
    g2, wiz2, war2 = pair(rules)
    war2.armor = {l: 0 for l in LOCATIONS}
    g2.hit(war2, wiz2, "melee", location="torso")
    assert not war2.alive


def test_armor_absorbs_and_armor_breaking(rules):
    g, wiz, war = pair(rules)
    war.armor = {l: 3 for l in LOCATIONS}
    g.hit(war, wiz, "melee", location="torso")
    assert war.alive and war.armor["torso"] == 2
    g.hit(war, wiz, "melee", location="torso", specials=frozenset({"armor-breaking"}))
    assert war.alive and war.armor["torso"] == 0, "armor breaking zeroes 3 or fewer points"
    g.hit(war, wiz, "melee", location="torso")
    assert not war.alive


def test_magic_ball_wound_inflict(sure_rules):
    g, wiz, war = pair(sure_rules)
    war.armor = {l: 0 for l in LOCATIONS}
    resolve(g, wiz, "force-bolt", war)
    assert war.wounds or not war.alive
    assert g.applied[("force-bolt", "wound.inflict")] == 1


def test_state_apply_timed(rules):
    g, wiz, war = pair(rules)
    resolve(g, wiz, "hold-person", war)
    assert war.states["stopped"] == g.t + 30


def test_magic_ball_state(sure_rules):
    g, wiz, war = pair(sure_rules)
    resolve(g, wiz, "entangle", war)
    assert war.states["stopped"] == g.t + 60


def test_state_remove(rules):
    g, wiz, war = pair(rules)
    war.states["stopped"] = g.t + 30
    resolve(g, wiz, "release", war)
    assert "stopped" not in war.states


def test_wound_heal(rules):
    g, heal, war = pair(rules, a="Healer")
    war.wounds.add("left_arm")
    resolve(g, heal, "heal", war)
    assert not war.wounds


def test_life_revive(rules):
    g = make_game(rules, [spec("Healer"), spec("Warrior")], [spec("Wizard")])
    healer, war, wiz = g.players
    resolve(g, wiz, "finger-of-death", war)
    assert not war.alive
    resolve(g, healer, "resurrect", war)
    assert war.alive and not war.wounds


def test_armor_repair_and_destroy(rules):
    g, wiz, war = pair(rules)
    war.armor_max = 6
    war.armor = {l: 6 for l in LOCATIONS}
    resolve(g, wiz, "destroy-armor", war)
    assert sorted(war.armor.values())[0] == 0
    resolve(g, wiz, "mend", war)  # nothing broken, so Mend repairs a point of armor
    assert sorted(war.armor.values())[0] == 1


def test_mend_choice_repairs_weapon_first(rules):
    g, wiz, war = pair(rules)
    war.weapon_ok = False
    war.armor["torso"] = 0
    resolve(g, wiz, "mend", war)
    assert war.weapon_ok and war.armor["torso"] == 0


def test_enchantment_magic_armor_and_dispel(rules):
    g, heal, war = pair(rules, a="Druid")
    war.armor = {l: 0 for l in LOCATIONS}
    resolve(g, heal, "stoneskin", war)
    assert war.magic_armor["torso"] == 2
    g.hit(war, heal, "melee", location="torso")
    assert war.alive and war.magic_armor["torso"] == 1
    resolve(g, heal, "dispel-magic", war)
    assert not war.enchantments and war.magic_armor["torso"] == 0


def test_resistance_to_wounds(rules):
    g, monk, war = pair(rules, a="Monk")
    war.armor = {l: 0 for l in LOCATIONS}
    resolve(g, monk, "blessing-against-wounds", war, magical=False, rng="Touch")
    g.hit(war, monk, "melee", location="torso")
    assert war.alive, "resistant to the next wound"
    assert not war.enchantments, "used up"
    g.hit(war, monk, "melee", location="torso")
    assert not war.alive


def test_phoenix_tears_prevents_death_then_spends_strip(rules):
    g, wiz, war = pair(rules)
    resolve(g, war, "phoenix-tears", war, magical=False, rng="Self")
    ench = war.enchantments[-1]
    assert ench.ability.slug == "phoenix-tears" and ench.strips == 2
    g.kill(war, wiz, "test")
    assert war.alive and war.has_state("frozen", g.t)
    for _ in range(31):
        g.step()
    assert ench.strips == 1


def test_troll_blood_spends_strip_and_freezes(rules):
    g, dru, war = pair(rules, a="Druid")
    resolve(g, dru, "troll-blood", war)
    ench = next(e for e in war.enchantments if e.ability.slug == "troll-blood")
    g.kill(war, dru, "test")
    assert war.alive and war.states["frozen"] == g.t + 30 and ench.strips == 2


def test_ancestral_armor_negates_hit_on_armor(rules):
    g, wiz, war = pair(rules)
    war.armor = {l: 6 for l in LOCATIONS}
    resolve(g, war, "ancestral-armor", war, magical=False, rng="Self")
    g.hit(war, wiz, "melee", location="torso", specials=frozenset({"armor-destroying"}))
    assert war.armor["torso"] == 5


def test_move_to_base(rules):
    g, wiz, war = pair(rules)
    war.states["insubstantial"] = g.t + 30
    resolve(g, wiz, "banish", war)
    assert war.at_base_until > g.t


def test_kill_trigger_scavenge(rules):
    g = make_game(rules, [spec("Warrior", level=2)], [spec("Wizard")])
    war, wiz = g.players
    assert "scavenge" in war.uses
    war.armor_max = 6
    war.armor = {l: 6 for l in LOCATIONS}
    war.armor["torso"] = 0
    g.kill(wiz, war, "melee")
    assert war.armor["torso"] == 1
    assert g.casts["scavenge"] == 1


def test_true_grit_after_dying(rules):
    g = make_game(rules, [spec("Warrior", level=3)], [spec("Wizard")])
    war, wiz = g.players
    g.kill(war, wiz, "melee")
    assert war.alive and war.has_state("frozen", g.t)
    assert war.uses["true-grit"].left == 1


def test_unhandled_effect_is_logged_not_dropped(rules):
    # Sanctuary is explicitly not modeled (needs-map): its effects are still counted, under their mode
    g, war, wiz = pair(rules, a="Monk", b="Wizard")
    resolve(g, war, "sanctuary", war, magical=False, rng="Self")
    assert g.noops[("sanctuary", "needs-map:action.restrict")] == 4
    assert g.noops[("sanctuary", "needs-map:defense.unaffected")] == 2


def test_frozen_player_unaffected(rules):
    g, wiz, war = pair(rules)
    war.states["frozen"] = INF
    resolve(g, wiz, "finger-of-death", war)
    assert war.alive and g.fails[("finger-of-death", "frozen")] == 1
