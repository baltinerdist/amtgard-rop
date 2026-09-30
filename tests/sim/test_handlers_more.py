"""Handlers added to raise effect coverage. One test (or a few) per handler, each on the real
ability record, with fixed seeds, in the style of test_handlers.py."""
import random

from sim.engine import effects as fx
from sim.engine.loadout import _add, _apply_loadout_effects, _archetype_purchase_rules, _buy
from sim.engine.state import INF, LOCATIONS, Cast, Player, Uses
from sim.rules import frequency
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


# ---------------------------------------------------------------- ability.grant

def test_enchantment_grants_uses_tracked_separately(rules):
    g = make_game(rules, [spec("Druid"), spec("Scout", level=2)], [spec("Warrior")])
    dru, sco, _ = g.players
    assert "heal" in sco.uses
    resolve(g, dru, "gift-of-water", sco)
    granted = sco.uses["heal@gift-of-water"]
    assert granted.per == "unlimited" and granted.magical and granted.range == "Self"
    assert sco.uses["heal"].granted_by is None, "the Scout's own Heal is untouched"
    resolve(g, dru, "dispel-magic", sco)
    assert "heal@gift-of-water" not in sco.uses and "heal" in sco.uses


def test_regeneration_heal_is_swift_and_not_near_enemies(rules):
    g, dru, war, ally = trio(rules, a="Druid")
    resolve(g, dru, "regeneration", ally)
    u = ally.uses["heal"]
    assert u.swift and u.extra_reqs == {"no-enemy-within-10ft"}
    ally.wounds.add("left_arm")
    war.target = ally.pid                       # an enemy is on them
    assert not g.start_cast(ally, u, ally)
    assert g.fails[("heal", "requirement:no-enemy-within-10ft")] == 1
    war.target = None
    assert g.start_cast(ally, u, ally) and ally.casting.remaining == 1.0


def test_troll_blood_as_per_regeneration(rules):
    g, dru, _, ally = trio(rules, a="Druid")
    resolve(g, dru, "troll-blood", ally)
    assert ally.uses["heal"].granted_by.ability.slug == "troll-blood"


def test_undead_minion_raise_dead_only_on_the_minion(rules):
    g = make_game(rules, [spec("Healer"), spec("Warrior"), spec("Warrior")], [spec("Wizard")])
    heal, minion, other, wiz = g.players
    resolve(g, heal, "undead-minion", minion)
    u = next(u for u in heal.uses.values() if u.slug == "raise-dead" and u.granted_by is not None)
    assert u.only_target == minion.pid and "target-not-moved-5ft" in u.drop_reqs and u.per == "unlimited"
    g.kill(minion, wiz, "test")
    g.kill(other, wiz, "test")
    assert not g.start_cast(heal, u, other)
    assert g.start_cast(heal, u, minion)


def test_stoneskin_magic_armor_as_per_ancestral_armor(rules):
    g, dru, war, ally = trio(rules, a="Druid")
    ally.armor = {l: 0 for l in LOCATIONS}
    resolve(g, dru, "stoneskin", ally)
    g.hit(ally, war, "melee", location="torso", specials=frozenset({"armor-destroying"}))
    assert ally.magic_armor["torso"] == 1, "one point lost, not destroyed"
    assert g.applied[("stoneskin", "ability.grant")] == 1


def test_song_of_interference_as_per_enlightened_soul(rules):
    g, bard, wiz, _ = trio(rules, b="Wizard")
    resolve(g, bard, "song-of-interference", bard, rng="Self")
    assert g.unaffected(bard, "verbal-magical-beyond-touch")
    resolve(g, wiz, "hold-person", bard)
    assert g.fails[("hold-person", "unaffected")] == 1 and not bard.has_state("stopped", g.t)


def kit(rules, cls, traits, bought=(), picked=(), copies=None, seed=5):
    """A player with purchased (Magic User) and picked (class level) abilities, then Archetype/Trait
    effects applied. bought/picked: (slug, frequency text, range)."""
    p = Player(pid=0, team=0, cls=cls, level=6, skill=0.0, role="caster")
    for slug, freq, rng in bought:
        _add(p, rules, slug, frequency.parse(freq), 1, True, rng, purchased=True)
    for slug, freq, rng in picked:
        _add(p, rules, slug, frequency.parse(freq), 1, False, rng)
    for t in traits:
        _add(p, rules, t, frequency.parse(""), (copies or {}).get(t, 1), False, "", purchased=True)
    _apply_loadout_effects(p, rules, random.Random(seed), rules.classes[cls])
    return p


def test_group_double_uses(rules):
    p = kit(rules, "Bard", ["dervish"], bought=[("insult", "1/Life", "20'"), ("song-of-power", "Unlimited", "Self")])
    assert p.uses["insult"].max == 2, "each Verbal purchased gives double the uses"
    w = kit(rules, "Wizard", ["warlock"], bought=[("lightning-bolt", "2 Balls / Unlimited", ""),
                                                  ("force-bolt", "3 Balls / Unlimited", ""),
                                                  ("finger-of-death", "1/Refresh", "20'"),
                                                  ("heat-weapon", "1/Life", "20'")])
    assert (w.uses["finger-of-death"].max, w.uses["heat-weapon"].max, w.uses["lightning-bolt"].max) == (2, 2, 4)
    assert w.uses["force-bolt"].max == 3, "a Sorcery ball is not a Death or Flame one"
    s = kit(rules, "Druid", ["summoner"], bought=[("stoneskin", "1/Life", "Other"), ("heat-weapon", "1/Life", "20'")])
    assert (s.uses["stoneskin"].max, s.uses["heat-weapon"].max) == (2, 1)
    h = kit(rules, "Healer", ["warder"], bought=[("harden", "1/Refresh", "Other"), ("heal", "Unlimited", "Touch")])
    assert h.uses["harden"].max == 2


def test_group_charge(rules):
    n = kit(rules, "Healer", ["necromancer"], bought=[("raise-dead", "1/Life", "Touch"), ("heal", "1/Life", "Touch")])
    assert n.uses["raise-dead"].charge == 3 and not n.uses["heal"].charge
    m = kit(rules, "Monk", ["medium"], picked=[("heal", "1/Life", "Touch")])
    assert m.uses["heal"].charge == 3 and m.uses["sever-spirit"].charge == 3


def test_priest_meta_magics_become_per_life_charge(rules):
    p = kit(rules, "Healer", ["priest"], bought=[("ambulant", "1/Refresh", ""), ("ambulant", "1/Refresh", "")])
    u = p.uses["ambulant"]
    assert (u.per, u.max, u.charge) == ("life", 2, 3), "ruling priest#1: 2 purchases give 2/Life Charge x3"


def test_sniper_and_artificer_arrows(rules):
    s = kit(rules, "Archer", ["sniper"], picked=[("pinning-arrow", "2 Arrows / Unlimited", ""),
                                                 ("phase-arrow", "1 Arrow / Unlimited", "")])
    u = s.uses["pinning-arrow"]
    assert (u.per, u.max, u.charge, u.unit) == ("life", 1, 3, None), "ruling sniper#1: one per type"
    a = kit(rules, "Archer", ["artificer"], picked=[("destruction-arrow", "1 Arrow / Unlimited", ""),
                                                    ("pinning-arrow", "1 Arrow / Unlimited", "")])
    assert "destruction-arrow" not in a.uses, "ruling artificer#1"
    assert (a.uses["pinning-arrow"].max, a.uses["phase-arrow"].max, a.uses["suppression-arrow"].max) == (3, 2, 2)


def test_marauder_ancestral_armor_not_chargeable(rules):
    p = kit(rules, "Warrior", ["marauder"], picked=[("ancestral-armor", "(Self) 3/Refresh Charge x10 (ex) (Swift)", "")])
    assert p.uses["ancestral-armor"].charge is None


def test_legend_doubles_each_extension(rules):
    p = kit(rules, "Bard", ["legend"], bought=[("extension", "1/Life", ""), ("extension", "1/Life", "")])
    assert p.uses["extension"].max == 4 and p.uses["extension"].per == "life"


def test_experienced_one_verbal_per_purchase(rules):
    p = kit(rules, "Wizard", ["experienced"], copies={"experienced": 2},
            bought=[("heat-weapon", "1/Life", "20'"), ("mend", "1/Life", "Touch"), ("lightning-bolt", "2 Balls / Unlimited", "")])
    assert sorted((s, u.charge) for s, u in p.uses.items() if u.charge) == [("heat-weapon", 5), ("mend", 5)]


# ---------------------------------------------------------------- ability.modify

def test_archetype_modify_pairs_apply_once(rules):
    spy = kit(rules, "Assassin", ["spy"], picked=[("blink", "2/Life", "Self"), ("shadow-step", "2/Life", "Self")])
    assert (spy.uses["blink"].charge, spy.uses["blink"].max, spy.uses["shadow-step"].charge) == (3, 2, 3)
    bm = kit(rules, "Wizard", ["battlemage"], bought=[("ambulant", "1/Life", "")])
    assert bm.uses["ambulant"].per == "unlimited"
    hunter = kit(rules, "Scout", ["hunter"], picked=[("pinning-arrow", "1 Arrow / Unlimited", "")])
    assert hunter.uses["pinning-arrow"].max == 2
    legend = kit(rules, "Bard", ["legend"], bought=[("extension", "1/Life", "")])
    assert legend.uses["extension"].max == 2, "doubled once, not by both records of the change"


def test_golem_mend_removes_a_wound(rules):
    g = make_game(rules, [spec("Wizard"), spec("Warrior")], [spec("Warrior")])
    wiz, war, _ = g.players
    resolve(g, wiz, "golem", war)
    war.wounds.add("left_arm")
    war.weapon_ok = False
    resolve(g, wiz, "mend", war, rng="Touch")
    assert not war.wounds and not war.weapon_ok, "a wound instead of a repair (ruling golem#1)"
    assert g.applied[("golem", "wound.heal")] == 1


def test_artificer_mend_on_equipment_is_free(rules):
    g = make_game(rules, [spec("Archer"), spec("Warrior")], [spec("Warrior")])
    arc, war, _ = g.players
    arc.traits.append(rules.abilities["artificer"])
    war.weapon_ok = False
    u = uses_of(g, "mend", magical=False, rng="Touch")
    u.max = u.left = 1
    arc.casting = Cast(u, war.pid, 0)
    g._complete(arc)
    assert war.weapon_ok and u.left == 1
    war.armor = {l: 0 for l in LOCATIONS}
    arc.casting = Cast(u, war.pid, 0)
    g._complete(arc)
    assert u.left == 0, "a Mend on armor still uses it up"


def test_guardian_one_imbue_and_necromancer_five_minions(rules):
    g = make_game(rules, [spec("Paladin", level=6), spec("Warrior"), spec("Warrior"), spec("Healer", level=6),
                          spec("Warrior"), spec("Warrior"), spec("Warrior"), spec("Warrior")], [spec("Warrior")])
    pal, a, b, heal, *minions, _ = g.players
    pal.traits.append(rules.abilities["guardian"])
    resolve(g, pal, "imbue", a, rng="Touch")
    resolve(g, pal, "imbue", b, rng="Touch")
    assert g.fails[("imbue", "per-caster-limit")] == 1
    for m in minions:
        resolve(g, heal, "undead-minion", m, rng="Other")
    assert g.fails[("undead-minion", "per-caster-limit")] == 1, "three per caster"
    heal.traits.append(rules.abilities["necromancer"])
    resolve(g, heal, "undead-minion", minions[-1], rng="Other")
    assert sum(e.ability.slug == "undead-minion" for q in g.players for e in q.enchantments) == 4


def test_cursed_adrenaline_only_with_vampirism(rules):
    g = make_game(rules, [spec("Wizard"), spec("Barbarian")], [spec("Warrior")])
    wiz, barb, war = g.players
    adr = uses_of(g, "adrenaline", magical=False, rng="Self")
    adr.per, adr.max, adr.left = "unlimited", None, None
    barb.uses = {"adrenaline": adr}
    barb.states["cursed"] = INF
    barb.wounds.add("left_arm")
    g.kill(war, barb, "melee")
    assert barb.wounds, "Cursed: Immune to Spirit, so Adrenaline has no effect"
    resolve(g, wiz, "vampirism", barb, rng="Other")
    war.alive = True
    g.kill(war, barb, "melee")
    assert not barb.wounds and g.applied[("vampirism", "ability.modify")] == 1


# ---------------------------------------------------------------- economy.purchase-restrict / economy.cost

def entry(rules, cls, slug):
    return next(c for c in rules.classes[cls].abilities if c.slug == slug)


def test_purchase_restrictions(rules):
    _, ok = _archetype_purchase_rules(rules.abilities["warlock"], rules)
    assert ok(entry(rules, "Wizard", "lightning-bolt")) and ok(entry(rules, "Wizard", "finger-of-death"))
    assert not ok(entry(rules, "Wizard", "force-bolt")) and ok(entry(rules, "Wizard", "void-touched")), "enchantments allowed"
    _, ok = _archetype_purchase_rules(rules.abilities["summoner"], rules)
    assert not ok(entry(rules, "Druid", "heat-weapon")), "a 20' Verbal"
    assert ok(entry(rules, "Druid", "mend")) and ok(entry(rules, "Druid", "equipment-shield-small"))
    assert not ok(entry(rules, "Druid", "equipment-weapon-long")), "equipment beyond 2nd level"
    _, ok = _archetype_purchase_rules(rules.abilities["battlemage"], rules)
    assert not ok(entry(rules, "Wizard", "void-touched")) and not ok(entry(rules, "Wizard", "fireball"))
    _, ok = _archetype_purchase_rules(rules.abilities["warder"], rules)
    assert not ok(entry(rules, "Healer", "undead-minion")) and ok(entry(rules, "Healer", "harden"))
    _, ok = _archetype_purchase_rules(rules.abilities["legend"], rules)
    assert not ok(entry(rules, "Bard", "swift")) and ok(entry(rules, "Bard", "extension"))


def test_archetype_costs(rules):
    cost, _ = _archetype_purchase_rules(rules.abilities["priest"], rules)
    assert cost(entry(rules, "Healer", "heal")) == 0 and cost(entry(rules, "Healer", "mend")) == 1
    cost, _ = _archetype_purchase_rules(rules.abilities["ranger"], rules)
    assert cost(entry(rules, "Druid", "equipment-weapon-great")) == 0
    assert cost(entry(rules, "Druid", "poison")) == 2, "Enchantment costs are doubled"
    cost, _ = _archetype_purchase_rules(rules.abilities["dervish"], rules)
    assert cost(entry(rules, "Bard", "equipment-shield-small")) == 4


def test_restricted_purchase_is_skipped(rules):
    cands = [entry(rules, "Wizard", s) for s in ("force-bolt", "lightning-bolt")]
    cost, ok = _archetype_purchase_rules(rules.abilities["warlock"], rules)
    bought = _buy(cands, {"force-bolt": 9.0, "lightning-bolt": 1.0}, {"force-bolt": 0.0, "lightning-bolt": 0.0},
                  {lv: 5 for lv in range(1, 7)}, 3, cost, ok)
    assert "force-bolt" not in bought and bought.get("lightning-bolt")


# ---------------------------------------------------------------- equipment.permit

def test_equipment_permits(rules):
    assert kit(rules, "Druid", ["ranger"]).has_bow
    s = kit(rules, "Archer", ["sniper"], picked=[("pinning-arrow", "2 Arrows / Unlimited", "")])
    assert s.uses["pinning-arrow"].unit is None
    names = set(rules.by_name)
    for slug in ("equipment-weapon-long", "equipment-shield-small"):
        ab = rules.abilities[slug]
        modes = {fx.handling(ab, e, names) for e in ab.effects if e.params.get("what") != "small-shield"}
        assert modes == {fx.OUT_OF_SCOPE}


# ---------------------------------------------------------------- state.apply

def test_brutal_strike_wound_trigger(rules):
    g = make_game(rules, [spec("Anti-Paladin", level=4)], [spec("Wizard"), spec("Wizard")])
    ap, wiz, wiz2 = g.players
    assert "brutal-strike" in ap.uses
    g.wound(wiz, "left_arm", ap, "melee")
    assert wiz.states["cursed"] == INF and wiz.states["suppressed"] == g.t + 30
    assert ap.uses["brutal-strike"].left == 0, "1/Life"
    ap.uses["brutal-strike"].restore(1)
    g.wound(wiz2, "torso", ap, "melee")          # a killing wound: only Cursed (ruling brutal-strike#1)
    assert not wiz2.alive and wiz2.has_state("cursed", g.t) and not wiz2.has_state("suppressed", g.t)
    assert g.casts["brutal-strike"] == 2


def test_brutal_strike_not_on_a_resisted_wound(rules):
    g = make_game(rules, [spec("Anti-Paladin", level=4), spec("Monk")], [spec("Wizard")])
    ap, monk, wiz = g.players
    resolve(g, monk, "blessing-against-wounds", wiz, magical=False, rng="Touch")
    g.wound(wiz, "left_arm", ap, "melee")
    assert not wiz.wounds and g.casts["brutal-strike"] == 0


def test_gift_of_air_options(rules):
    seen = set()
    for seed in range(8):
        g, heal, war, ally = trio(rules, a="Healer", seed=seed)
        resolve(g, heal, "gift-of-air", ally)
        g.hit(ally, war, "melee", location="torso")
        assert ally.alive and ally.has_state("insubstantial", g.t)
        assert any(e.ability.slug == "gift-of-air" for e in ally.enchantments), "stays on (ruling gift-of-air#1)"
        if ally.at_base_until > g.t:        # option 2: to base, Insubstantial until arrival, no early exit
            assert ally.states["insubstantial"] == ally.at_base_until == ally.exit_lock_until
            seen.add(2)
        else:                               # option 1: in place, exits at will (the self-exit assumption)
            assert ally.states["insubstantial"] == g.t + g.rules.a("policy.self_insubstantial_seconds")
            seen.add(1)
    assert seen == {1, 2}


def test_song_of_survival_option_and_removal(rules):
    g, bard, war, _ = trio(rules)
    resolve(g, bard, "song-of-survival", bard, rng="Self")
    g.kill(bard, war, "melee")
    assert bard.alive and bard.has_state("insubstantial", g.t)
    assert not any(e.ability.slug == "song-of-survival" for e in bard.enchantments)
    assert sum(n for (s, k), n in g.applied.items() if s == "song-of-survival" and k == "state.apply") == 1


def test_song_of_power_stops_the_bard_while_sung(rules):
    g, bard, _, _ = trio(rules)
    resolve(g, bard, "song-of-power", bard, rng="Self")
    assert bard.has_state("stopped", g.t)
    g.remove_enchantment(bard, bard.enchantments[-1])
    assert not bard.has_state("stopped", g.t)


def test_blood_and_thunder_enchants_the_killer(rules):
    g = make_game(rules, [spec("Barbarian", level=6)], [spec("Wizard")], seed=3)
    barb, wiz = g.players
    assert "blood-and-thunder" in barb.uses
    barb.uses = {"blood-and-thunder": barb.uses["blood-and-thunder"]}
    g.kill(wiz, barb, "melee")
    assert any(e.ability.slug == "blessing-against-wounds" and not e.magical for e in barb.enchantments)
    assert g.applied[("blood-and-thunder", "ability.grant")] == 1


def test_one_kill_trigger_per_kill(rules):
    g = make_game(rules, [spec("Barbarian", level=6)], [spec("Wizard")], seed=3)
    barb, wiz = g.players
    triggers = [s for s, u in barb.uses.items() if "kill-trigger" in u.ability.properties]
    assert len(triggers) > 1
    g.kill(wiz, barb, "melee")
    assert sum(g.casts[s] for s in triggers) == 1
