"""Handlers added to raise effect coverage. One test (or a few) per handler, each on the real
ability record, with fixed seeds, in the style of test_handlers.py."""
import random

from sim.engine import effects as fx
from sim.engine.loadout import _apply_loadout_effects
from sim.engine.state import LOCATIONS, Player, Uses
from tests.sim.conftest import make_game, resolve, spec


def trio(rules, a="Bard", b="Warrior", c="Warrior", seed=1):
    """a is on team 0 with c; b is the lone enemy on team 1."""
    g = make_game(rules, [spec(a), spec(c)], [spec(b)], seed=seed)
    return g, g.players[0], g.players[2], g.players[1]


def uses_of(g, slug, magical=True, rng="20'"):
    return Uses(g.rules.abilities[slug], None, None, None, None, None, magical, range=rng)


def archetype_player(rules, cls, archetype, **kit):
    p = Player(pid=0, team=0, cls=cls, level=6, skill=0.0, role="fighter")
    for k, v in kit.items():
        setattr(p, k, v)
    p.traits.append(rules.abilities[archetype])
    _apply_loadout_effects(p, rules)
    return p


# ---------------------------------------------------------------- action.restrict

def test_awe_bars_attacking_and_casting_at_the_caster(rules):
    g, bard, war, ally = trio(rules)
    resolve(g, bard, "awe", war)
    assert not g.can_attack(war, bard) and g.can_attack(war, ally)
    assert not g.can_cast_at(war, bard, uses_of(g, "lightning-bolt"))
    assert g.can_cast_at(war, bard, uses_of(g, "lightning-bolt", magical=False)), "ruling awe#1: (ex) allowed"
    assert g.restricted_targets(war) == [bard.pid]
    assert g.applied[("awe", "action.restrict")] == 2
    war.target = bard.pid
    g._melee()
    assert war.target is None, "the engine drops a melee target the player may not attack"


def test_awe_negated_when_caster_attacks_target(rules):
    g, bard, war, _ = trio(rules)
    resolve(g, bard, "awe", war)
    assert war.kept_away_until == g.t + 30
    g._provoke(bard, war, "attack")
    assert g.can_attack(war, bard) and not war.restrictions
    assert war.kept_away_until == g.t, "the same casting's keep-away ends with it"


def test_terror_ends_when_caster_dies(rules):
    g, bard, war, _ = trio(rules)
    resolve(g, bard, "terror", war)
    assert not g.can_attack(war, bard)
    g.kill(bard, war, "test")
    assert not war.restrictions


def test_restriction_blocks_start_cast(rules):
    g, bard, wiz, _ = trio(rules, b="Wizard")
    resolve(g, bard, "awe", wiz)
    bolt = uses_of(g, "lightning-bolt")
    bolt.left = bolt.max = 1
    assert not g.start_cast(wiz, bolt, bard)
    assert g.fails[("lightning-bolt", "restricted")] == 1 and bolt.left == 1


def test_insult_only_the_caster_until_others_attack(rules):
    g, bard, war, ally = trio(rules)
    resolve(g, bard, "insult", war)
    assert g.can_attack(war, bard) and not g.can_attack(war, ally)
    assert not g.can_cast_at(war, ally, uses_of(g, "heal"))
    assert not g.can_cast_at(war, war, uses_of(g, "heal")), "literal reading: nobody but the caster"
    assert g.can_cast_at(war, bard, uses_of(g, "lightning-bolt"))
    g._provoke(ally, war, "attack")   # Insult E2: the target may now attack the offender too
    assert g.can_attack(war, ally)
    assert not g.can_cast_at(war, ally, uses_of(g, "lightning-bolt")), "ruling insult#1: attacks only"


def test_insult_ends_when_either_dies(rules):
    g, bard, war, ally = trio(rules)
    resolve(g, bard, "insult", war)
    g.kill(bard, ally, "test")
    assert g.can_attack(war, ally) and not war.restrictions


def test_restrictions_expire(rules):
    g, bard, war, _ = trio(rules)
    resolve(g, bard, "awe", war)
    g.t += 31
    g._upkeep()
    assert not war.restrictions and g.can_attack(war, bard)


def test_martyr_locks_the_transferred_state(rules):
    g, pal, war, _ = trio(rules, a="Paladin", b="Wizard")
    resolve(g, pal, "martyr", pal, magical=False, rng="Other")
    assert pal.exit_lock_until == g.t + 10


def test_archetype_equipment_drawbacks(rules):
    assert archetype_player(rules, "Barbarian", "berserker", armor_max=3).armor_max == 0
    assert archetype_player(rules, "Assassin", "spy", armor_max=2).armor_max == 0
    medium = archetype_player(rules, "Monk", "medium", armor_max=1, great_weapon=True)
    assert medium.armor_max == 0 and not medium.great_weapon
    assert not archetype_player(rules, "Anti-Paladin", "corruptor", great_weapon=True).great_weapon
    assert archetype_player(rules, "Anti-Paladin", "infernal", shield="large").shield == "none"
    assert archetype_player(rules, "Warrior", "marauder", shield="large").shield == "medium"
    hunter = archetype_player(rules, "Scout", "hunter", shield="small")
    assert hunter.shield == "none" and hunter.great_weapon, "no shield, so the Great weapon permit applies"
    assert not archetype_player(rules, "Assassin", "rogue", has_bow=True).has_bow


def test_gift_of_air_bars_weapons_and_shields(rules):
    g, heal, war, _ = trio(rules, a="Healer", b="Warrior")
    war.shield = "large"
    resolve(g, heal, "gift-of-air", war)
    assert g.barred(war, "wield-weapons") and not g.shield_up(war)
    war.target = heal.pid
    g._engage()
    assert war.target is None


def test_sniper_may_not_fire_normal_arrows(rules):
    g = make_game(rules, [spec("Archer")], [spec("Warrior")])
    arc, war = g.players
    arc.traits.append(rules.abilities["sniper"])
    assert not g.can_fire_normal_arrows(arc)
    g.shoot(arc, war)
    assert g.fails[("arrow", "restricted")] == 1 and arc.next_shot_at > g.t


def test_essence_graft_only_wears_the_grafters_magic(rules):
    g = make_game(rules, [spec("Wizard"), spec("Druid"), spec("Warrior")], [spec("Warrior")])
    wiz, dru, war, _ = g.players
    resolve(g, dru, "stoneskin", war)
    resolve(g, wiz, "essence-graft", war)
    slugs = [e.ability.slug for e in war.enchantments]
    assert "essence-graft" in slugs and "stoneskin" not in slugs, "others' (m) Enchantments are dropped"
    resolve(g, dru, "barkskin", war)
    assert g.fails[("barkskin", "restricted:essence-graft")] == 1
    resolve(g, wiz, "barkskin", war)
    assert "barkskin" in [e.ability.slug for e in war.enchantments]


def test_unmodeled_effects_have_explicit_modes(rules):
    names = set(rules.by_name)
    ab = rules.abilities["golem"]
    assert fx.handling(ab, next(e for e in ab.effects if e.kind == "action.restrict"), names) == fx.NEEDS_MAP
    ab = rules.abilities["mystic"]
    assert fx.handling(ab, next(e for e in ab.effects if e.kind == "action.restrict"), names) == fx.OUT_OF_SCOPE
    assert not fx.is_handled(ab, next(e for e in ab.effects if e.kind == "action.restrict"))
