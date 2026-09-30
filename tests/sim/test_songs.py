"""Bardic songs: the Chant rules in the engine (sim/engine/game.py) and the situational song choice
(sim/policies/songs.py), on small hand-built games."""
import copy

import pytest

from sim.engine.state import LOCATIONS, Uses
from sim.policies import _enchant_targets, decide, songs
from sim.rules.compile import build_rules

from .conftest import make_game, resolve, spec


def _bare(g):
    for p in g.players:
        p.uses = {}
        p.enchantments = [e for e in p.enchantments if e.trait]


def _song(g, p, slug):
    ab = g.rules.abilities[slug]
    p.uses[slug] = Uses(ab, "unlimited", None, None, None, None, True, range="Self")
    return p.uses[slug]


def _spell(g, p, slug, rng="20'", n=3):
    ab = g.rules.abilities[slug]
    p.uses[slug] = Uses(ab, "life", n, n, None, None, True, range=rng)
    return p.uses[slug]


def _sings(p):
    return [e.ability.slug for e in p.chants()]


def _sing_now(g, p, slug):
    """Sing through the engine: start the incantation and let it finish."""
    u = p.uses.get(slug) or _song(g, p, slug)
    assert g.start_cast(p, u, p)
    while p.casting is not None:
        p.casting.remaining -= 1
        if p.casting.remaining <= 0:
            g._complete(p)


def _duo(rules):
    g = make_game(rules, [spec("Bard", 6), spec("Druid", 4)], [spec("Warrior"), spec("Wizard", 4)])
    _bare(g)
    return g, *g.players


# ---------------------------------------------------------------- the Chant rules in the engine

def test_casting_another_spell_ends_the_song(rules):
    g, bard, _, foe, _ = _duo(rules)
    _sing_now(g, bard, "song-of-battle")
    assert _sings(bard) == ["song-of-battle"]
    assert g.start_cast(bard, _spell(g, bard, "awe"), foe)
    assert _sings(bard) == [], "beginning a new incantation interrupts any Chant"
    assert g.chants_ended[("song-of-battle", "incantation")] == 1


def test_an_abandoned_incantation_still_ended_the_song(rules):
    g, bard, _, foe, _ = _duo(rules)
    _sing_now(g, bard, "song-of-determination")
    assert g.start_cast(bard, _spell(g, bard, "stun"), foe)
    g.interrupt(bard, "abandoned")
    assert _sings(bard) == []


def test_switching_songs_ends_the_old_then_sings_the_new(rules):
    g, bard, *_ = _duo(rules)
    _sing_now(g, bard, "song-of-determination")
    assert g.start_cast(bard, _song(g, bard, "song-of-battle"), bard)
    assert _sings(bard) == [], "silent while the new song's incantation is said"
    g._complete(bard)
    assert _sings(bard) == ["song-of-battle"]


def test_one_chant_at_a_time_even_with_a_spare_slot(rules):
    g, bard, druid, *_ = _duo(rules)
    resolve(g, druid, "attuned", bard, rng="Other")
    assert bard.ench_slots == 2
    _sing_now(g, bard, "song-of-determination")
    resolve(g, bard, "song-of-deflection", bard, rng="Self")     # skips start_cast
    assert _sings(bard) == ["song-of-deflection"]


def test_charging_ends_the_song(rules):
    g, bard, *_ = _duo(rules)
    _sing_now(g, bard, "song-of-battle")
    u = _spell(g, bard, "confidence", rng="Other", n=1)
    u.charge, u.left = 5, 0
    assert g.start_charge(bard, u)
    assert _sings(bard) == []


def test_the_song_ends_on_death_and_when_the_bard_cannot_speak(rules):
    g, bard, druid, foe, _ = _duo(rules)
    _sing_now(g, bard, "song-of-battle")
    g.apply_state(bard, "suppressed", g.t + 30)
    assert _sings(bard) == ["song-of-battle"], "Suppressed has no effect on Chants already in progress"
    g.apply_state(bard, "stunned", g.t + 10)
    assert _sings(bard) == [], "Stunned: may not speak"
    bard.states.clear()
    _sing_now(g, bard, "song-of-battle")
    g.kill(bard, foe, "melee")
    assert not bard.alive and _sings(bard) == []


def test_no_second_magical_enchantment_while_singing(rules):
    g, bard, druid, *_ = _duo(rules)
    _sing_now(g, bard, "song-of-determination")
    resolve(g, druid, "barkskin", bard, rng="Other")
    assert [e.ability.slug for e in bard.enchantments if e.magical] == ["song-of-determination"]
    assert g.fails[("barkskin", "enchantment-limit")] == 1


def test_a_bard_wearing_another_enchantment_cannot_sing(rules):
    g, bard, druid, *_ = _duo(rules)
    resolve(g, druid, "barkskin", bard, rng="Other")
    _sing_now(g, bard, "song-of-battle")
    assert _sings(bard) == [] and g.fails[("song-of-battle", "enchantment-limit")] == 1


def test_song_of_survival_once_per_life(rules):
    g, bard, druid, foe, _ = _duo(rules)
    _sing_now(g, bard, "song-of-survival")
    g.kill(bard, foe, "melee")
    assert bard.alive and _sings(bard) == [], "Survival activated and ended"
    assert not g.start_cast(bard, bard.uses["song-of-survival"], bard)
    assert g.fails[("song-of-survival", "requirement:once-per-life")] == 1
    bard.states.clear()
    g.kill(bard, foe, "melee")
    g.respawn(bard)
    assert g.start_cast(bard, bard.uses["song-of-survival"], bard), "a new life"


def test_song_of_power_ends_when_the_bard_is_moved(rules):
    g, bard, *_ = _duo(rules)
    _sing_now(g, bard, "song-of-power")
    g.send_to_base(bard)
    assert _sings(bard) == []
    _sing_now(g, bard, "song-of-battle")
    g.send_to_base(bard)
    assert _sings(bard) == ["song-of-battle"], "a Chant may be spoken while moving"


# ---------------------------------------------------------------- the song choice (sim/policies/songs.py)

ALL_SONGS = ("song-of-battle", "song-of-freedom", "song-of-determination", "song-of-deflection",
             "song-of-survival", "song-of-power", "song-of-interference", "song-of-visit")


@pytest.fixture(scope="module")
def near_rules(rules):
    """Every target in range, so choices are the policy's alone."""
    a = copy.deepcopy(rules.assumptions)
    a["range"]["p_in_range"]["value"] = {k: 1.0 for k in a["range"]["p_in_range"]["value"]}
    a["range"]["p_ally_nearby_for_touch"]["value"] = 1.0
    return build_rules(assumptions=a)


def _field(rules, n_mates=1, foes=("Warrior",), play="battle", level=6):
    """A Bard holding every song, n_mates teammates (Warriors), and these enemies, all unarmored
    and without abilities."""
    g = make_game(rules, [spec("Bard", level)] + [spec("Warrior")] * n_mates, [spec(c) for c in foes])
    _bare(g)
    bard = g.players[0]
    bard.play = play
    for s in ALL_SONGS:
        _song(g, bard, s)
    for q in g.players:
        q.armor = {l: 0 for l in LOCATIONS}
    return g, bard, g.players[1:1 + n_mates], g.players[1 + n_mates:]


def _chosen(g, bard):
    g.policy_cache.clear()
    assert songs.try_song(g, bard), "the Bard should start a song"
    return bard.casting.uses.slug


def _finish(g, p):
    g._complete(p)
    g.policy_cache.clear()


def test_battle_against_armored_enemies_in_melee(rules):
    g, bard, _, (foe,) = _field(rules)
    foe.armor = {l: 3 for l in LOCATIONS}
    bard.target, foe.target = foe.pid, bard.pid
    assert _chosen(g, bard) == "song-of-battle"


def test_no_battle_against_unarmored_enemies(rules):
    g, bard, _, (foe,) = _field(rules)
    bard.target, foe.target = foe.pid, bard.pid
    assert songs.song_utility(g, bard, rules.abilities["song-of-battle"]) == 0
    assert not songs.try_song(g, bard), "nothing to sing for: no song at all"


def test_freedom_against_stop_freeze_and_insubstantial(rules):
    g, bard, _, (wiz,) = _field(rules, foes=("Wizard",))
    _spell(g, wiz, "iceball")
    assert _chosen(g, bard) == "song-of-freedom"


def test_determination_against_command(rules):
    g, bard, _, (foe,) = _field(rules, foes=("Bard",))
    del bard.uses["song-of-interference"]          # Insult is also a ranged Verbal
    _spell(g, foe, "insult")
    assert _chosen(g, bard) == "song-of-determination"


def test_deflection_against_archers(rules):
    g, bard, _, (archer,) = _field(rules, foes=("Archer",))
    assert archer.has_bow
    assert _chosen(g, bard) == "song-of-deflection"


def test_interference_against_ranged_verbals(rules):
    g, bard, _, (wiz,) = _field(rules, foes=("Wizard",))
    _spell(g, wiz, "wounding")
    assert _chosen(g, bard) == "song-of-interference"


def test_a_caster_in_melee_is_no_casting_threat(rules):
    g, bard, (mate,), (wiz,) = _field(rules, foes=("Wizard",))
    _spell(g, wiz, "wounding")
    mate.target = wiz.pid                         # busy fighting the Bard's teammate
    assert songs.song_utility(g, bard, rules.abilities["song-of-interference"]) == 0


def test_survival_when_wounded_and_outnumbered(rules):
    g, bard, _, foes = _field(rules, foes=("Warrior", "Warrior"))
    for q in foes:
        q.armor = {l: 3 for l in LOCATIONS}
        q.target = bard.pid
    bard.target = foes[0].pid
    bard.wounds.add("left_arm")
    assert _chosen(g, bard) == "song-of-survival"


def test_power_for_charging_teammates_not_in_the_line(near_rules):
    g, bard, (mate,), _ = _field(near_rules, play="controller")
    u = _spell(g, mate, "confidence", rng="Other", n=1)
    u.charge, u.left = 5, 0
    assert g.start_charge(mate, u)
    assert _chosen(g, bard) == "song-of-power"
    g2, skald, (mate2,), _ = _field(near_rules, play="battle")
    u2 = _spell(g2, mate2, "confidence", rng="Other", n=1)
    u2.charge, u2.left = 5, 0
    assert g2.start_charge(mate2, u2)
    assert songs.song_utility(g2, skald, near_rules.abilities["song-of-power"]) == 0, \
        "Power Stops its bearer: not for a Bard who fights in the line"


def test_visit_is_never_sung(rules):
    g, bard, _, _ = _field(rules)
    assert songs.song_utility(g, bard, rules.abilities["song-of-visit"]) == 0
    for s in ALL_SONGS[:-1]:
        del bard.uses[s]
    assert not songs.try_song(g, bard)


def test_switches_when_the_situation_changes(rules):
    g, bard, _, (foe, wiz) = _field(rules, foes=("Warrior", "Wizard"))
    foe.armor = {l: 3 for l in LOCATIONS}
    bard.target, foe.target = foe.pid, bard.pid
    assert _chosen(g, bard) == "song-of-battle"
    _finish(g, bard)
    bard.target = foe.target = None               # the fight is over; an enemy caster steps up
    foe.alive = False
    for s in ("iceball", "entangle"):
        _spell(g, wiz, s)
    assert _chosen(g, bard) == "song-of-freedom"
    assert songs.worn_song(bard) is None, "the old song ended when the new incantation began"


def test_margin_covers_the_incantation(rules):
    g, *_ = _field(rules)
    h = rules.a("policy.song_switch_horizon_seconds")
    assert not songs.should_switch(g, 1.0, 1.05, 2), "5% better doesn't pay for 2 s of silence"
    assert songs.should_switch(g, 1.0, 1.0 * h / (h - 2) + 0.25, 2)
    assert not songs.should_switch(g, 0.10, 0.15, 2), "too small to be worth stopping for"


def test_margin_prevents_flip_flopping(rules):
    """Ten teammates, three Command casters and three Freezers: a fourth Freezer stepping in and out
    doesn't flip the song; four more do."""
    foes = ("Bard",) * 3 + ("Wizard",) * 8
    g, bard, _, enemies = _field(rules, n_mates=9, foes=foes)
    del bard.uses["song-of-interference"]
    for q in enemies[:3]:
        _spell(g, q, "insult")
    freezers = enemies[3:]
    for q in freezers:
        _spell(g, q, "iceball").left = 0
    for q in freezers[:3]:
        q.uses["iceball"].left = 1
    first = _chosen(g, bard)
    _finish(g, bard)
    assert first == "song-of-determination"       # a tie goes to the first in order
    switches = 0
    for tick in range(20):
        freezers[3].uses["iceball"].left = tick % 2
        g.policy_cache.clear()
        if songs.try_song(g, bard):
            switches += 1
            _finish(g, bard)
    assert switches == 0
    for q in freezers[3:]:
        q.uses["iceball"].left = 1
    assert _chosen(g, bard) == "song-of-freedom"


def test_casting_another_spell_ends_the_song_in_play(near_rules):
    g, bard, _, (foe,) = _field(near_rules, play="controller", foes=("Warrior",))
    _sing_now(g, bard, "song-of-determination")
    _spell(g, bard, "stun")
    g.policy_cache.clear()
    decide(g, bard)
    assert bard.casting.uses.slug == "stun" and bard.casting.target == foe.pid
    assert songs.worn_song(bard) is None


def test_a_song_that_matters_holds_weak_spells(rules):
    g, bard, _, enemies = _field(rules, play="controller", foes=("Bard", "Bard"))
    del bard.uses["song-of-interference"]
    for q in enemies:
        _spell(g, q, "insult")
    _sing_now(g, bard, "song-of-determination")
    g.policy_cache.clear()
    assert songs.song_utility(g, bard, rules.abilities["song-of-determination"]) == 1.0
    assert not songs.keeps_song(g, bard, _spell(g, bard, "insult")), "1 point < 2.5 points of song"
    assert songs.keeps_song(g, bard, _spell(g, bard, "stun")), "6 points > 5 points of song"
    for q in enemies:
        q.uses["insult"].left = 0                  # the threat is spent: the song matters little
    g.policy_cache.clear()
    assert songs.keeps_song(g, bard, bard.uses["insult"])


def test_no_teammate_enchants_a_singing_bard(rules):
    g, bard, _, (foe,) = _field(rules, foes=("Bard",))
    druid_game = make_game(rules, [spec("Druid", 4)], [spec("Warrior")])
    bark = _spell(druid_game, druid_game.players[0], "barkskin", rng="Other", n=1)
    _spell(g, foe, "insult")
    _sing_now(g, bard, "song-of-determination")
    assert bard not in _enchant_targets(g, g.players[1], bark, at_base=False)


def test_a_bard_turns_down_an_enchantment_worth_less_than_a_song(rules):
    g, bard, (mate,), foes = _field(rules, foes=("Bard", "Bard"))
    bark = _spell(g, mate, "barkskin", rng="Other", n=1)
    assert not songs.declines(g, bard, bark), "nothing to sing for: Barkskin is welcome"
    for q in foes:
        _spell(g, q, "insult")
    g.policy_cache.clear()
    assert songs.declines(g, bard, bark)
    assert bard not in _enchant_targets(g, mate, bark, at_base=False)
