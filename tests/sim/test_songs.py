"""Bardic songs: the Chant rules in the engine (sim/engine/game.py) and the situational song choice
(sim/policies/songs.py), on small hand-built games."""
from sim.engine.state import Uses

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
