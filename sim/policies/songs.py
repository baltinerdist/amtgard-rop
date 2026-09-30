"""Bardic songs: which song to sing, when to switch, and what another cast costs in song.

A song is a Self Enchantment sustained by a Chant. Beginning any other incantation (a spell, a
Charge, another song) ends it (`Game.end_chants`), so switching is ending the current song and then
saying the new one's incantation, silent in between.

**Utility per song** (threat units, `sim/policies/utility.py`). `reach(q)` is the chance enemy q
casts or shoots at the Bard soon: 0 while q is in melee (engaged players start no ranged
incantation and don't shoot), otherwise 1 / (the Bard's living teammates).

| Song | Utility now |
| --- | --- |
| battle | armored share (hit locations with 2+ armor points) of the Bard's melee target. A Bard who fights in the line (battle play) sings for the next fights too: the living enemies' average when not engaged, half target and half average when engaged |
| freedom | sum of reach over enemies who can Stop, Freeze or make Insubstantial |
| determination | sum of reach over enemies with a harmful Command-school ability |
| deflection | sum of reach over enemies with a usable bow |
| survival | enemies in melee with the Bard beyond the first, +1 if wounded, + how far the team is outnumbered (enemies / teammates - 1, when above 0); 0 once it has saved the Bard this life |
| power | per teammate: 1 while Charging, 0.5 with a spent chargeable ability, times the chance they are within 20'; 0 for a Bard who fights in the line (Power Stops the bearer) |
| interference | sum of reach over enemies with a harmful magical Verbal of range beyond Touch |
| visit | 0 (below) |

Only abilities an enemy can use now count (a use left, not Suppressed). Living enemies at base
count too: they are coming back.

**Switching** (`try_song`). Over the next `policy.song_switch_horizon_seconds` (H), the best other
song, after its silent incantation of t seconds, must be worth at least
`policy.song_switch_min_gain` value points more than keeping the current one:
value_of(U_new x (H - t) - U_now x H) >= min_gain (U_now = 0 with no song on). With H = 20 s and
a 2 s song, a new song must be over 11% better and gain at least a point, so neither a small shift
nor a single enemy stepping in and out of melee flips the Bard between songs.

**Casting other spells** (`keeps_song`). Another incantation costs the song for its own length plus
the time to sing it again. A Bard casts it only if its usefulness score (value.py) is at least
value_of(U_now x (t_cast + t_song)). A Bard whose song matters little casts freely; one whose song
matters holds weak spells. An escape (Blink) is taken whatever it costs.

**Other Enchantments** (`declines`). A Bard with a single free Magical Enchantment slot turns down
a teammate's Magical Enchantment (only willing players can be enchanted) when their best song
over H is worth more than its usefulness score.

Song of Visit (Stopped and Invulnerable, then an Invulnerable walk back to base) is a way of
leaving the fight, not of fighting: the engine leaves its effects out of scope (COVERAGE.md), and a
battlegame Bard sings it only to take a break. Its utility is 0, so it is never sung.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sim.engine.effects import is_handled
from sim.engine.state import LOCATIONS, Ench, Player, Uses
from sim.policies.utility import cached, in_melee, living, reach, register, utility, value_of

if TYPE_CHECKING:
    from sim.engine.game import Game
    from sim.rules.compile import Ability

LOCKDOWN = ("stopped", "frozen", "insubstantial")       # what Song of Freedom keeps off
_SLUG_TAGS: dict[str, frozenset] = {}


def is_song(ab: "Ability") -> bool:
    """A Self Enchantment kept up by a Chant: the Bardic songs."""
    return ab.delivery == "enchantment" and "chant" in ab.properties and ab.range == "Self"


def worn_song(p: Player) -> Ench | None:
    return next(iter(p.chants()), None) if p.enchantments else None


# ---------------------------------------------------------------- what enemies can do to the Bard

def _hostile(ab: "Ability") -> bool:
    return ab.beneficiary == "enemy" or ab.delivery in ("magic-ball", "specialty-arrow") or any(
        e.polarity == "harm" and e.subject in ("target", "struck-player") for e in ab.effects)


def _ability_tags(ab: "Ability") -> frozenset:
    """Threats this ability poses to an enemy Bard: 'command', 'lockdown', 'verbal'."""
    tags = _SLUG_TAGS.get(ab.slug)
    if tags is None:
        out = set()
        if ab.range != "Self" and _hostile(ab) and any(is_handled(ab, e) for e in ab.effects):
            if ab.school == "Command":
                out.add("command")
            if any(e.kind == "state.apply" and e.subject in ("target", "struck-player")
                   and e.params.get("state") in LOCKDOWN and is_handled(ab, e) for e in ab.effects):
                out.add("lockdown")
            if ab.delivery == "verbal":
                out.add("verbal")
        tags = _SLUG_TAGS[ab.slug] = frozenset(out)
    return tags


def threats(g: "Game", q: Player) -> frozenset:
    """What enemy q can do to a Bard now: 'command', 'lockdown', 'verbal' (a harmful magical
    Verbal beyond Touch, what Song of Interference stops) and 'bow'."""
    def calc() -> frozenset:
        out = set()
        if not q.has_state("suppressed", g.t):
            for u in q.uses.values():
                if not u.available():
                    continue
                tags = _ability_tags(u.ability)
                if not tags:
                    continue
                out |= tags - {"verbal"}
                if "verbal" in tags and u.magical and u.range not in ("Touch", "Self", "Other"):
                    out.add("verbal")
        if q.has_bow and g.can_fire_normal_arrows(q) and g.weapon_usable(q):
            out.add("bow")
        return frozenset(out)
    return cached(g, ("threats", q.pid), calc)


def _threat_sum(g: "Game", p: Player, tag: str) -> float:
    return sum(reach(g, p, q) for q in living(g.enemies(p)) if tag in threats(g, q))


# ---------------------------------------------------------------- utility per song

def armored(q: Player) -> float:
    """Share of q's hit locations with 2 or more armor points. Armor Breaking zeroes a location of
    3 or fewer, so it saves hits against 2 and 3 points (and more, once worn down)."""
    return sum(1 for l in LOCATIONS if q.armor.get(l, 0) + q.magic_armor.get(l, 0) >= 2) / len(LOCATIONS)


def _fights_in_line(p: Player) -> bool:
    return p.play == "battle" or p.role == "fighter"


@register("song-of-battle")
def _battle(g: "Game", p: Player, _target) -> float:
    if not g.weapon_usable(p) or g.barred(p, "wield-weapons"):
        return 0.0
    now = armored(g.players[p.target]) if p.target is not None else None
    if not _fights_in_line(p):
        return now or 0.0
    foes = living(g.enemies(p))
    ahead = sum(armored(q) for q in foes) / len(foes) if foes else 0.0
    # a Bard who fights in the line sings for this fight and the next ones
    return ahead if now is None else 0.5 * now + 0.5 * ahead


@register("song-of-freedom")
def _freedom(g: "Game", p: Player, _target) -> float:
    return _threat_sum(g, p, "lockdown")


@register("song-of-determination")
def _determination(g: "Game", p: Player, _target) -> float:
    return _threat_sum(g, p, "command")


@register("song-of-deflection")
def _deflection(g: "Game", p: Player, _target) -> float:
    return _threat_sum(g, p, "bow")


@register("song-of-interference")
def _interference(g: "Game", p: Player, _target) -> float:
    return _threat_sum(g, p, "verbal")


@register("song-of-survival")
def _survival(g: "Game", p: Player, _target) -> float:
    if "song-of-survival" in p.once_used:
        return 0.0
    foes = living(g.enemies(p))
    attackers = sum(1 for q in foes if in_melee(p, q))
    mates = len(living(g.allies(p)))
    outnumbered = max(0.0, len(foes) / max(1, mates) - 1.0)
    return max(0, attackers - 1) + (1.0 if p.wounds else 0.0) + outnumbered


@register("song-of-power")
def _power(g: "Game", p: Player, _target) -> float:
    if _fights_in_line(p):
        return 0.0
    mates, weights = [], []
    for a in g.allies(p):
        if a is p or not a.alive or not a.on_field(g.t):
            continue
        if a.casting is not None and a.casting.kind == "charge":
            mates.append(a)
            weights.append(1.0)
        elif any(u.charge and u.max and u.left is not None and u.left < u.max and g.value(u.ability, a) > 0
                 for u in a.uses.values()):
            mates.append(a)
            weights.append(0.5)
    return g.space.expected_in_range(p, mates, "20'", weights)


@register("song-of-visit")
def _visit(g: "Game", p: Player, _target) -> float:
    return 0.0


# ---------------------------------------------------------------- choosing and weighing

def song_utility(g: "Game", p: Player, ab: "Ability") -> float:
    return utility(g, p, ab, p) or 0.0


def _song_seconds(g: "Game", ab: "Ability") -> float:
    return ab.cast_seconds(g.words_per_second)


def best_song(g: "Game", p: Player, exclude: str = "") -> tuple[Uses | None, float]:
    """The song p could start now with the highest utility (above 0), and that utility."""
    best, best_u = None, 0.0
    for slug in sorted(p.uses):
        u = p.uses[slug]
        if slug == exclude or not is_song(u.ability) or not u.available():
            continue
        if g.check_requirements(u.ability, p, p, start=True, uses=u) is not None:
            continue
        x = song_utility(g, p, u.ability)
        if x > best_u:
            best, best_u = u, x
    return best, best_u


def switch_gain(g: "Game", now: float, new: float, new_seconds: float) -> float:
    """Value points gained over the horizon by switching: the new song after its silent
    incantation, less the current song kept for the whole horizon."""
    h = g.rules.a("policy.song_switch_horizon_seconds")
    return value_of(g, new * max(0.0, h - new_seconds) - now * h)


def should_switch(g: "Game", now: float, new: float, new_seconds: float) -> bool:
    return switch_gain(g, now, new, new_seconds) >= g.rules.a("policy.song_switch_min_gain")


def try_song(g: "Game", p: Player) -> bool:
    """Sing the song the situation needs, or switch to it (see the module docstring)."""
    worn = worn_song(p)
    if worn is None and p.magical_enchantment_count() >= p.ench_slots:
        return False            # another caster's Enchantment fills the slot
    u, new = best_song(g, p, exclude=worn.ability.slug if worn is not None else "")
    if u is None:
        return False
    now = song_utility(g, p, worn.ability) if worn is not None else 0.0
    if not should_switch(g, now, new, _song_seconds(g, u.ability)):
        return False
    return g.start_cast(p, u, p)


def declines(g: "Game", q: Player, u: Uses) -> bool:
    """A Bard keeps their last Magical Enchantment slot for a song (Enchantments may only be cast on
    willing players, rule 2): they turn down a teammate's Magical Enchantment when their best song
    over the horizon is worth more than its usefulness score."""
    if not u.magical or "exempt-from-enchantment-limit" in u.ability.properties \
            or q.ench_slots - q.magical_enchantment_count() != 1:
        return False
    if not any(is_song(v.ability) for v in q.uses.values()):
        return False
    _, best = best_song(g, q)
    h = g.rules.a("policy.song_switch_horizon_seconds")
    return value_of(g, best * h) > g.value(u.ability, q)


def song_loss(g: "Game", p: Player, seconds: float) -> float:
    """Value points of song lost by an incantation of this many seconds: the song's utility for
    that time plus the time to sing it again. 0 with no song on."""
    worn = worn_song(p)
    if worn is None:
        return 0.0
    return value_of(g, song_utility(g, p, worn.ability) * (seconds + _song_seconds(g, worn.ability)))


def keeps_song(g: "Game", p: Player, u: Uses) -> bool:
    """Whether casting u is worth the song it ends. Songs themselves are weighed by try_song, and a
    declaration (no incantation) ends no Chant."""
    if not p.enchantments or is_song(u.ability) or u.declare_words is not None:
        return True
    if worn_song(p) is None:
        return True
    secs = 1.0 if u.swift else u.ability.cast_seconds(g.words_per_second)
    return g.value(u.ability, p) >= song_loss(g, p, secs)
