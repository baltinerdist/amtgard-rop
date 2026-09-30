"""Calibration gifts: a paired, test-only change to one team, injected into a Game.

A scenario may carry `"gifts"`, a list of dicts such as

    {"kind": "armor", "team": 0, "points": 1, "who": "fighter"}
    {"kind": "ability", "team": 0, "slug": "finger-of-death", "frequency": "1/Life"}
    {"kind": "state", "team": 0, "state": "stunned", "seconds": 30}

`Game.__init__` calls `apply(game)` once the players are built. Each gift draws its recipients,
times and targets from its own random stream, `random.Random(f"{seed}:gift:{i}")`, so every other
stream of the game (scenario, loadouts, play) is exactly that of the same seed without the gift:
the two games of a pair differ by the gift and by nothing else until it first matters. Magic Users
have already bought their spells, so a gift never changes what anyone buys.

Every gift takes `team` (default 0) and `n` (recipients, default 1; distinct players drawn among
those eligible) or `share` (that share of the eligible players, rounded up, at least one; for
`state`, of the enemy team's size). `who` narrows the recipients: "any" (default), "fighter" (fighter role), and the
kind's own condition (armor: may wear armor; shield: carries none; ...). A gift with no eligible
recipient is not given; `Game.gift_log` records who received what.

Kinds, and the engine facility each uses (no engine code knows about gifts except two lines):

| kind | what the recipient gets | through |
| --- | --- | --- |
| `armor` | `points` of worn armor on every location, for the whole game (`bare`: only players wearing none) | `Player.armor_max` |
| `magic-armor` | Magic Armor `points` on every location, every life: a Barkskin that is never removed and takes no Enchantment slot | a trait Enchantment, as class Traits that are Enchantments are |
| `shield` | a `size` shield, for a player carrying none and no Great weapon | `Player.shield` |
| `ability` | `copies` of `slug` at `frequency` (e.g. "1/Life"), added as a class table entry would be | `loadout._add` |
| `death-ward` | one death prevented per life, by Phoenix Tears' own prevention (all wounds healed, Frozen 30 s), without its extra slot or its other on-thaw effects | a non-magical Enchantment attached at the start of each life (a scheduled check every second) |
| `state` | a `state` for `seconds` on a random targetable enemy, at a uniform random time in the first `window` seconds after pregame prep (retried each second until someone is targetable) | `Game.apply_state` from a scheduled event |
| `weapon-special` | `effect` (armor-breaking, wounds-kill) on the recipient's melee weapons all game | a trait Enchantment granting it, as Flame Blade grants Armor Breaking |
| `free-charge` | once per life, the recipient's most valuable spent chargeable ability is Charged at once | a scheduled check every second |
| `charge-time` | every Charge the recipient starts takes `seconds` less (at least 1 s) | `Player.charge_seconds_saved`, read by `Game.start_charge` |
| `extra-slot` | `count` more (m) Enchantment slots, all game | `Player.ench_slots` |

Units: the calibration harness (`sim/analyze/calibrate.py`) divides the measured change by the
gift's units (points of armor, recipients, applications).
"""
from __future__ import annotations

import dataclasses
import math
import random
from typing import TYPE_CHECKING

from sim.engine.state import LOCATIONS, Ench

if TYPE_CHECKING:
    from sim.engine.game import Game
    from sim.engine.state import Player


def _barred(p: "Player", what: str) -> bool:
    return any(e.kind == "action.restrict" and e.params.get("what") == what and e.timing == "while-active"
               for ab in p.traits for e in ab.effects)


def _chargeable(p: "Player") -> bool:
    return any(u.charge and u.max for u in p.uses.values())


ELIGIBLE = {
    "any": lambda g, p, gift: True,
    "fighter": lambda g, p, gift: p.role == "fighter",
    "caster": lambda g, p, gift: p.role in ("caster", "support"),
}


def _kind_ok(g: "Game", p: "Player", gift: dict) -> bool:
    k = gift["kind"]
    if k == "armor":
        return not _barred(p, "wear-armor") and (not gift.get("bare") or p.armor_max == 0)
    if k == "shield":
        return p.shield == "none" and not p.great_weapon and not p.has_bow and not _barred(p, "wield-shields")
    if k == "weapon-special":
        eff = gift["effect"]
        return not _barred(p, "wield-weapons") and not (eff == "armor-breaking" and p.great_weapon)
    if k in ("free-charge", "charge-time"):
        return _chargeable(p)
    return True


def _count(gift: dict, pool_size: int) -> int:
    if "share" in gift:
        n = max(1, math.ceil(float(gift["share"]) * pool_size)) if pool_size else 0
    else:
        n = int(gift.get("n", 1))
    return min(n, pool_size)


def _recipients(g: "Game", gift: dict, rng: random.Random) -> list["Player"]:
    team = gift.get("team", 0)
    who = ELIGIBLE[gift.get("who", "any")]
    pool = [p for p in g.players if p.team == team and who(g, p, gift) and _kind_ok(g, p, gift)]
    n = _count(gift, len(pool))
    return rng.sample(pool, n) if n else []


def _synthetic(rules, base: str, slug: str, keep) -> object:
    """An existing ability with only some of its effects, under its own slug."""
    ab = rules.abilities[base]
    return dataclasses.replace(ab, slug=slug, name=slug, effects=tuple(e for e in ab.effects if keep(e)))


def death_ward_ability(rules):
    """Phoenix Tears' own death prevention (all wounds healed, Frozen 30 s, spent on thawing)
    without its extra slot, its Cursed removal, repair or other on-thaw effects; one strip."""
    keep = {"death.prevent", "wound.heal", "state.apply", "enchantment.spend-strip"}
    ab = _synthetic(rules, "phoenix-tears", "gift-death-ward", lambda e: e.kind in keep)
    return dataclasses.replace(ab, properties=ab.properties - {"has-choice"}, strips=1)


def _every_second(g: "Game", fn) -> None:
    """Call fn at every tick from the next one on (Game.at: no random draws)."""
    def tick():
        fn()
        g.at(g.t + g.dt, tick)
    g.at(g.t + g.dt, tick)


def _trait_enchantment(g: "Game", p: "Player", ab) -> None:
    ench = Ench(ab, p.pid, False, ab.strips, True, trait=True)
    p.enchantments.append(ench)
    g._activate(p, ench)


# ---------------------------------------------------------------- the kinds

def _armor(g, p, gift, rng):
    p.armor_max += int(gift.get("points", 1))
    p.armor = {l: p.armor_max for l in LOCATIONS}


def _magic_armor(g, p, gift, rng):
    pts = int(gift.get("points", 1))
    ab = _synthetic(g.rules, "barkskin", f"gift-magic-armor-{pts}", lambda e: e.kind == "armor.magic")
    ab = dataclasses.replace(ab, effects=tuple(dataclasses.replace(e, params={**e.params, "points": pts})
                                               for e in ab.effects))
    _trait_enchantment(g, p, ab)


def _shield(g, p, gift, rng):
    p.shield = gift["size"]


def _ability(g, p, gift, rng):
    from sim.engine.loadout import _add
    from sim.rules import frequency as freqmod
    f = freqmod.parse(gift.get("frequency", "1/Life"))
    ab = g.rules.abilities[gift["slug"]]
    _add(p, g.rules, ab.slug, f, int(gift.get("copies", 1)), f.magical is not False, gift.get("range", ""))


def _death_ward(g, p, gift, rng):
    ab = death_ward_ability(g.rules)
    warded = {"life": None}

    def check():
        if p.alive and not p.out and warded["life"] != p.deaths:
            warded["life"] = p.deaths
            ench = Ench(ab, p.pid, False, 1)
            p.enchantments.append(ench)
    check()
    _every_second(g, check)


def _state(g, p, gift, rng):
    """p is unused: the gift lands on a random enemy of the gift's team."""
    team = gift.get("team", 0)
    prep = g.rules.a("respawn.pregame_prep_seconds")
    when = prep + rng.uniform(0, float(gift.get("window", 300)))
    seconds = float(gift.get("seconds", 30))
    state = gift["state"]

    def fire():
        foes = [q for q in g.players if q.team != team and g.targetable(q)]
        if not foes:
            g.at(g.t + g.dt, fire)
            return
        q = rng.choice(foes)
        if g.apply_state(q, state, g.t + seconds, own=False):
            g.applied[(f"gift-{state}", "state.apply")] += 1
    g.at(when, fire)


def _weapon_special(g, p, gift, rng):
    eff = gift["effect"]
    base = g.rules.abilities["flame-blade"]
    first = next(e for e in base.effects if e.kind == "special-effect.grant")
    grant = dataclasses.replace(first, params={**first.params, "effect": eff})
    ab = dataclasses.replace(base, slug=f"gift-{eff}", name=f"gift-{eff}", effects=(grant,))
    _trait_enchantment(g, p, ab)


def _free_charge(g, p, gift, rng):
    used = {"life": None}

    def check():
        if not p.alive or used["life"] == p.deaths:
            return
        spent = [u for u in p.uses.values() if u.charge and u.max and u.left is not None and u.left < u.max]
        if spent:
            best = max(spent, key=lambda u: (g.value(u.ability, p), u.slug))
            best.restore(1)
            used["life"] = p.deaths
            g.applied[("gift-free-charge", "ability.charge")] += 1
    _every_second(g, check)


def _charge_time(g, p, gift, rng):
    p.charge_seconds_saved += float(gift.get("seconds", 8))


def _extra_slot(g, p, gift, rng):
    p.ench_slots += int(gift.get("count", 1))


KINDS = {"armor": _armor, "magic-armor": _magic_armor, "shield": _shield, "ability": _ability,
         "death-ward": _death_ward, "state": _state, "weapon-special": _weapon_special,
         "free-charge": _free_charge, "charge-time": _charge_time, "extra-slot": _extra_slot}
# kinds that act on the game rather than on a recipient of the gift's team
TEAMLESS = {"state"}


def apply(g: "Game", gifts: list[dict]) -> list[dict]:
    """Give each gift; returns the log (kind, pid, role, class, level per recipient)."""
    log = []
    for i, gift in enumerate(gifts):
        fn = KINDS[gift["kind"]]
        rng = random.Random(f"{g.seed}:gift:{i}")
        if gift["kind"] in TEAMLESS:
            enemies = sum(1 for q in g.players if q.team != gift.get("team", 0))
            for _ in range(_count(gift, enemies)):
                fn(g, None, gift, rng)
                log.append({"gift": i, "kind": gift["kind"], "pid": None, "role": "", "cls": "", "level": 0})
            continue
        for p in _recipients(g, gift, rng):
            fn(g, p, gift, rng)
            log.append({"gift": i, "kind": gift["kind"], "pid": p.pid, "role": p.role, "cls": p.cls,
                        "level": p.level})
    return log
