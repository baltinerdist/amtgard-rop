"""Enablers cast by situational utility: refills, extra Enchantment slots, Enchantments that grant an
ability, Undead Minion, and Self Enchantments whose strips are cast at enemies.

Each utility is `(game, caster, target) -> value points`, registered by slug in `utility.UTILITY`,
in the units of the calibrated usefulness score (`value.py`). The caster scores its candidate
targets, takes the best (`best_target`), and casts when that beats `time_cost`, what its other
options would earn in the time the incantation takes (`worth_casting`; nothing at base).

| Ability | Utility for target q |
| --- | --- |
| Empower, Confidence, Innate (q = caster) | `refill_worth` of q's best spent use it can refill, if q acts soon |
| Restoration | the sum over q's spent per-life uses (a second missing use of one ability at COPY_DECAY), if q acts soon |
| Steal Life Essence | its Charge option: `refill_worth` of the caster's best spent chargeable use (`name_refill` weighs it against the heal) |
| Attuned, Essence Graft | `stack_share` x the fillers one more slot adds for q (beyond q's free slots); Graft less q's (m) Enchantments from others, which it drops |
| Amplification, Silver Tongue | the Enchantment's score over q's abilities that still have a use |
| Regeneration, Gift of Water, Battlefield Triage | the Enchantment's score to q, the granted Heal priced as a fighter's (calibrated `fighter_heal`) if q fights in the line |
| Undead Minion | q's expected deaths while the caster lives x (a Raise Dead that reaches q - the respawn it replaces), less Cursed |
| Discordia, Snaring Vines | the stripped spell's score x its expected casts (strips, or the enemies it can hit x its range chance), less the song kept off the slot |

Utilities don't draw from the game's random stream (utility.py); ties go to the lowest pid.
"""
from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

from sim.engine.effects import NOT_RESTORED  # Empower/Restoration limitation, kept with the handler
from sim.policies import songs
from sim.policies import value as V
from sim.policies.utility import cached, living, register, utility, value_of

if TYPE_CHECKING:
    from sim.engine.game import Game
    from sim.engine.state import Player, Uses
    from sim.rules.compile import Ability

REFILLS = ("ability.charge", "ability.restore-uses")
# Undead Minion: deaths per PRIOR_SECONDS assumed before any are seen (hand-set: a line fighter
# dies about twice as often as a backline player). Each death seen moves the rate toward q's own.
DEATH_PRIOR = {"line": 1.0, "back": 0.5}
PRIOR_SECONDS = 120.0
_TARGET_STATE_REQS = frozenset({"target-dead", "target-dead-at-start", "target-frozen", "target-insubstantial",
                                "target-stopped"})


# ---------------------------------------------------------------- shared helpers

def fights_in_line(q: "Player") -> bool:
    return q.role == "fighter" or q.play == "battle"


def acts_soon(g: "Game", q: "Player", magical: bool = False, field: bool = True) -> float:
    """1 if q will act soon, else 0: alive, lives left, on the field (`field=False`: or at base),
    not locked down (Frozen, Stunned, Insubstantial, Invulnerable) and, for magic, not Suppressed."""
    if not q.alive or q.out or (field and not q.on_field(g.t)) or not q.can_act(g.t):
        return 0.0
    return 0.0 if magical and q.has_state("suppressed", g.t) else 1.0


def cast_seconds(g: "Game", u: "Uses") -> float:
    return 1.0 if u.swift else u.ability.cast_seconds(g.words_per_second)


def _attack_rate(g: "Game", p: "Player") -> float:
    """Value points per second p's best attack earns now: its score over its incantation, times the
    chance a target is in range; 0 with no enemy to hit. Finishers (a State required) don't count."""
    from sim.policies import TRIGGERED, _is_offensive
    if not any(g.targetable(q) for q in g.enemies(p)):
        return 0.0
    best = 0.0
    for u in p.uses.values():
        ab = u.ability
        if not u.available() or u.range == "Self" or not _is_offensive(u) or ab.requirements & TRIGGERED \
                or ab.requirements & _TARGET_STATE_REQS or "kill-trigger" in ab.properties:
            continue
        v = g.value(ab, p)
        if v > 0:
            best = max(best, v / max(1.0, cast_seconds(g, u)) * g.space.p_any_in_range(p, u))
    return best


def time_cost(g: "Game", p: "Player", secs: float) -> float:
    """What p gives up by incanting for secs: its best attack's rate over that time plus the song it
    ends (songs.song_loss). Nothing at base, where there is nothing else to do."""
    if not p.on_field(g.t):
        return 0.0
    return cached(g, ("attack-rate", p.pid), lambda: _attack_rate(g, p)) * secs + songs.song_loss(g, p, secs)


def best_target(g: "Game", p: "Player", u: "Uses", targets) -> tuple["Player | None", float]:
    """The target with the highest utility above 0 (ties: the lowest pid), and that utility."""
    best, bu = None, 0.0
    for q in sorted(targets, key=lambda q: q.pid):
        x = utility(g, p, u.ability, q) or 0.0
        if x > bu:
            best, bu = q, x
    return best, bu


def worth_casting(g: "Game", p: "Player", u: "Uses", x: float, at_base: bool = False) -> bool:
    return x > (0.0 if at_base else time_cost(g, p, cast_seconds(g, u)))


def self_refill(ab: "Ability") -> bool:
    """The refill acts on its caster (Innate, Steal Life Essence), whatever its range says."""
    return all(e.subject == "caster" for e in ab.effects_of(*REFILLS))


def is_refill(ab: "Ability") -> bool:
    """Gives a teammate or oneself a spent use back (Empower, Restoration, Confidence, Innate)."""
    return ab.delivery in ("verbal", "meta-magic") and ab.beneficiary != "enemy" and bool(ab.effects_of(*REFILLS)) \
        and "kill-trigger" not in ab.properties


def spent(refill: "Ability", q: "Player") -> list["Uses"]:
    """q's uses this refill could give back: spent chargeable ones for a Charge, spent per-life ones
    (not Empower, Confidence or Restoration) for a restore. Strip uses are not refilled."""
    charge = bool(refill.effects_of("ability.charge"))
    return [u for u in q.uses.values() if u.left is not None and u.max and u.left < u.max and u.ench is None
            and (u.charge if charge else u.per == "life" and u.slug not in NOT_RESTORED)]


def refill_worth(g: "Game", refill: "Ability", q: "Player", u: "Uses") -> float:
    """A use of u back, to q: u's score in q's kit (value.py's refill with `Ctx.spent`), times
    `refill_factor` for an instant Charge (what one is worth in play, calibrated)."""
    v = max(0.0, g.value(u.ability, q))
    return v * V.refill_factor(g.rules) if refill.effects_of("ability.charge") else v


def best_spent(g: "Game", refill: "Ability", q: "Player") -> tuple["Uses | None", float]:
    """q's spent use worth most to get back through this refill (the first of equals), and its worth."""
    best, bw = None, -1.0
    for u in spent(refill, q):
        w = refill_worth(g, refill, q, u)
        if w > bw:
            best, bw = u, w
    return best, max(0.0, bw)


def name_refill(g: "Game", caster: "Player", refill: "Ability", q: "Player") -> "Uses | None":
    """Engine hook (Game.name_refill): the spent use a refill acts on, named by its caster when it
    resolves: the one worth most to q. For a refill offered beside a heal (Steal Life Essence: "heal
    a wound or instantly Charge an ability"), None when q is wounded and the heal is worth at least
    the Charge option (utility of the ability), so the heal is taken."""
    u, _ = best_spent(g, refill, q)
    if u is not None and q.wounds and refill.effects_of("wound.heal") and "has-choice" in refill.properties:
        if V.KIND_WEIGHT["wound.heal"] >= (utility(g, caster, refill, q) or 0.0):
            return None
    return u


def ench_worth(g: "Game", caster: "Player", ab: "Ability", q: "Player", kit: "V.Kit | None" = None) -> float:
    """ab's score cast by caster and worn by q, with both kits (value.py, as `_crippled` prices it);
    `kit` replaces q's own (its live abilities, or its role for pricing a Heal)."""
    bearer = kit if kit is not None else V.player_ctx(g, q).holder
    key = ("ench-worth", ab.slug, caster.pid, q.pid, bearer)
    v = g._value_cache.get(key)
    if v is None:
        ctx = V.Ctx(holder=V.player_ctx(g, caster).holder, bearer=bearer, game_type=g.sc.get("game_type"),
                    ablate=frozenset(g.ablate))
        v = g._value_cache[key] = V.value(ab, bearer.role, ctx, g.rules)
    return v


def live_kit(g: "Game", q: "Player") -> "V.Kit":
    """q's kit with only the abilities that still have a use: what a grant can act on now."""
    def calc():
        kit = V.player_ctx(g, q).holder
        gone = {u.slug for u in q.uses.values() if not u.available()}
        return dataclasses.replace(kit, held=tuple(h for h in kit.held if h.slug not in gone)) if gone else kit
    return cached(g, ("live-kit", q.pid), calc)


def heal_kit(g: "Game", q: "Player") -> "V.Kit":
    """q's kit, priced as a fighter's if q fights in the line: a Heal is worth to them what fighters
    make of one (calibrated `fighter_heal`: a player under attack rarely heals)."""
    kit = V.player_ctx(g, q).holder
    return dataclasses.replace(kit, role="fighter") if fights_in_line(q) and kit.role != "fighter" else kit


def death_rate(g: "Game", q: "Player") -> float:
    """q's deaths per second so far, starting from DEATH_PRIOR per PRIOR_SECONDS."""
    return (q.deaths + DEATH_PRIOR["line" if fights_in_line(q) else "back"]) / (g.t + PRIOR_SECONDS)


def _geometric(n: float) -> float:
    """held_worth for a fractional number of uses: sum of COPY_DECAY ** k over the first n."""
    return (1.0 - V.COPY_DECAY ** max(0.0, n)) / (1.0 - V.COPY_DECAY)


# ---------------------------------------------------------------- 1. refills

def _refill_one(slug: str):
    def fn(g: "Game", p: "Player", q: "Player") -> float:
        """The best spent use q gets back (the caster's own for Innate), if q will use it soon."""
        ab = g.rules.abilities[slug]
        q = p if self_refill(ab) else q
        u, w = best_spent(g, ab, q)
        return w * acts_soon(g, q, magical=u.magical) if u is not None else 0.0
    return fn


for _slug in ("empower", "confidence", "innate"):
    register(_slug)(_refill_one(_slug))


@register("restoration")
def _restoration(g: "Game", p: "Player", q: "Player") -> float:
    """Every spent per-life use back (the k-th missing use of one ability at COPY_DECAY ** k), if q acts soon."""
    ab = g.rules.abilities["restoration"]
    return acts_soon(g, q) * sum(refill_worth(g, ab, q, u) * V.held_worth(u.max - u.left) for u in spent(ab, q))


@register("steal-life-essence")
def _steal_life(g: "Game", p: "Player", _target) -> float:
    """The Charge option: the caster's best spent chargeable use back (name_refill weighs it against a heal)."""
    return best_spent(g, g.rules.abilities["steal-life-essence"], p)[1]


# ---------------------------------------------------------------- 2. extra Enchantment slots

def fillers(g: "Game", p: "Player", q: "Player", own_only: bool) -> list[float]:
    """Worth to q of each Enchantment that would fill an extra slot on q: the caster's own with a use
    left, and (unless only the caster's count) a teammate caster's, at the chance they reach q
    (Space.p_touch: Phase 1's p_ally_nearby_for_touch)."""
    from sim.policies import _is_offensive
    worn = {e.ability.slug for e in q.enchantments}
    best: dict[str, float] = {}
    for c in [p] + ([] if own_only else [a for a in living(g.allies(p)) if a is not p]):
        for u in c.uses.values():
            ab = u.ability
            if (not u.available() or ab.delivery != "enchantment" or ab.slug in worn or _is_offensive(u)
                    or (u.range or ab.range) == "Self" or "exempt-from-enchantment-limit" in ab.properties
                    or ab.effects_of("enchantment.extra-slot") or songs.is_song(ab) or (own_only and not u.magical)):
                continue
            w = max(0.0, ench_worth(g, c, ab, q)) * (1.0 if c is p else g.space.p_touch(c, q))
            best[ab.slug] = max(best.get(ab.slug, 0.0), w)
    return sorted(best.values(), reverse=True)


def _slot(slug: str):
    def fn(g: "Game", p: "Player", q: "Player") -> float:
        """stack_share x what one more slot adds for q (fillers beyond q's free slots, k-th at
        COPY_DECAY ** k); Essence Graft less q's (m) Enchantments from other casters, which it drops.
        0 if q has an extra slot already ("not in conjunction with itself or similar abilities")."""
        ab = g.rules.abilities[slug]
        if any(e.ability.effects_of("enchantment.extra-slot") for e in q.enchantments):
            return 0.0
        eff = ab.effects_of("enchantment.extra-slot")[0]
        graft = eff.params.get("only") == "magical-from-this-caster"
        free = max(0, q.ench_slots - q.magical_enchantment_count())
        vals = fillers(g, p, q, graft)[free:free + int(eff.params.get("count", 1) or 1)]
        added = V.stack_share(g.rules) * sum(x * V.COPY_DECAY ** k for k, x in enumerate(vals))
        lost = sum(max(0.0, ench_worth(g, g.players[e.caster], e.ability, q)) for e in q.enchantments
                   if graft and e.magical and not e.trait and e.caster != p.pid)
        return (added - lost) * acts_soon(g, q, field=False)
    return fn


for _slug in ("attuned", "essence-graft"):
    register(_slug)(_slot(_slug))


# ---------------------------------------------------------------- 3. Enchantments that grant an ability

def _granted(slug: str, heal: bool):
    def fn(g: "Game", p: "Player", q: "Player") -> float:
        """The Enchantment's score to q: over q's abilities with a use left, or with its Heal priced
        by how q would use it."""
        kit = heal_kit(g, q) if heal else live_kit(g, q)
        return ench_worth(g, p, g.rules.abilities[slug], q, kit) * acts_soon(g, q, field=False)
    return fn


for _slug in ("amplification", "silver-tongue"):
    register(_slug)(_granted(_slug, heal=False))
for _slug in ("regeneration", "gift-of-water", "battlefield-triage"):
    register(_slug)(_granted(_slug, heal=True))


# ---------------------------------------------------------------- 4. Undead Minion

@register("undead-minion")
def _minion(g: "Game", p: "Player", q: "Player") -> float:
    """q's deaths while the caster lives (their death rates' ratio; at most q's lives left or the
    time left) x (a Raise Dead by the caster, reaching q at Space.p_touch, less the
    respawn it replaces at value.late_share), less Cursed once. 0 once the caster has its cap."""
    ab = g.rules.abilities["undead-minion"]
    cap = g._per_caster_cap(ab, p)
    if cap is not None and sum(e.ability.slug == ab.slug and e.caster == p.pid
                               for a in g.players for e in a.enchantments) >= cap:
        return 0.0
    left = g.sc.get("max_seconds", g.rules.a("game.max_seconds")) - g.t
    deaths = min(death_rate(g, q) / death_rate(g, p), death_rate(g, q) * max(0.0, left))
    if q.lives_left is not None:
        deaths = min(deaths, q.lives_left)
    rd = g.rules.abilities.get("raise-dead")
    per = (max(0.0, g.value(rd, p)) if rd else 0.0) * g.space.p_touch(p, q) \
        - V.KIND_WEIGHT["life.revive"] * V.late_share(g.rules, g.sc.get("game_type"))
    return (deaths * per - V.STATE_WEIGHT["cursed"]) * acts_soon(g, q, field=False)


# ---------------------------------------------------------------- 5. Self Enchantments aimed at enemies

def _hittable(g: "Game", p: "Player", spell: "Ability", q: "Player") -> bool:
    """Enemy q is one the stripped spell would work on: not Immune to it or unaffected by Magic,
    and, for a Suppress, someone who casts."""
    from sim.policies import control_states
    if g.immune(q, spell.school) or g.unaffected(q, "magical-abilities") \
            or g.unaffected_by_school(q, spell.school) is not None:
        return False
    return control_states(spell) != {"suppressed"} or any(v.magical and v.available() for v in q.uses.values())


def _strips(slug: str):
    def fn(g: "Game", p: "Player", _target) -> float:
        """The stripped spell's score x its expected casts: the strips, or fewer when fewer enemies it
        can hit (living, on the field or coming back) are expected in its range; less the song the
        Enchantment keeps off p's slot for the song horizon."""
        ab = g.rules.abilities[slug]
        name = str(ab.effects_of("ability.cast-via-strips")[0].params.get("ability", "")).lower()
        spell = g.rules.abilities.get(g.rules.by_name.get(name, ""))
        if spell is None:
            return 0.0
        foes = [q for q in living(g.enemies(p)) if _hittable(g, p, spell, q)]
        casts = min(float(ab.strips or 1), g.space.expected_in_range(p, foes, spell.range))
        _, song = songs.best_song(g, p)
        return max(0.0, g.value(spell, p)) * _geometric(casts) \
            - value_of(g, song * g.rules.a("policy.song_switch_horizon_seconds"))
    return fn


for _slug in ("discordia", "snaring-vines"):
    register(_slug)(_strips(_slug))

