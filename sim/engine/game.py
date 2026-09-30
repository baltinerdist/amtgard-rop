"""Phase 1 game loop: non-spatial, one-second ticks.

Players are either at base, on the field, or dead. On the field, melee players pick an enemy
target (an "engagement"); every tick each attacker rolls to land a hit on its target. Casters
spend incantation time (words x repetitions / speech rate) and are interrupted by wounds, death,
action-preventing States, and sometimes by hits on armor. Range and positioning are abstracted
into probabilities from sim/data/assumptions.json.
"""
from __future__ import annotations

import heapq
import math
import random
from collections import Counter
from typing import Callable

from sim.engine import effects as fx
from sim.engine.effects import Ctx
from sim.engine.loadout import build_player
from sim.engine.state import ARMS, INF, LOCATIONS, Cast, Ench, Player, Uses
from sim.policies import decide, keep_casting
from sim.policies.value import value as ability_value
from sim.rules.compile import Ability, Rules

ARMOR_SPECIALS = ("armor-destroying", "armor-breaking")
GIFT_OF_AIR_EXCEPT = ("siege", "armor-breaking", "armor-destroying", "shield-crushing", "shield-destroying")
PASSIVE_UNAFFECTED = ("projectiles-except-magic-balls", "magical-abilities", "verbal-abilities",
                      "verbal-magical-beyond-touch")


def _logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


class Game:
    def __init__(self, rules: Rules, scenario: dict, seed: int, ablate: frozenset = frozenset(),
                 trace: bool = False):
        self.rules = rules
        self.sc = scenario
        self.seed = seed
        self.ablate = frozenset(ablate)
        self.rng = random.Random(f"{seed}:sim")
        self.t = 0.0
        self.dt = rules.a("time.tick_seconds")
        self.words_per_second = rules.a("time.speech_words_per_second")
        self.trace: list[tuple] | None = [] if trace else None
        self._events: list = []
        self._seq = 0
        # counters
        self.casts: Counter = Counter()
        self.applied: Counter = Counter()
        self.noops: Counter = Counter()
        self.fails: Counter = Counter()
        self.kill_sources: Counter = Counter()
        self._value_cache: dict = {}
        # players
        self.players: list[Player] = []
        lives = scenario.get("lives")
        prep = rules.a("respawn.pregame_prep_seconds")
        for team, roster in enumerate(scenario["teams"]):
            for spec in roster:
                pid = len(self.players)
                prng = random.Random(f"{seed}:loadout:{pid}")
                p = build_player(rules, pid, team, spec["cls"], spec["level"], spec["skill"], prng, self.ablate)
                p.lives_left = lives
                p.at_base_until = prep
                for ab in [ab for ab in p.traits if ab.delivery == "enchantment"]:
                    p.traits.remove(ab)
                    ench = Ench(ab, p.pid, False, ab.strips, True, trait=True)
                    p.enchantments.append(ench)
                    self._activate(p, ench)
                self.players.append(p)
        self.n_teams = len(scenario["teams"])
        self.next_refresh = scenario.get("refresh_seconds") or INF
        base = rules.a("melee.base_hit_per_second")
        self._base_logit = _logit(base)

    # ------------------------------------------------------------------ utilities

    def log(self, *event) -> None:
        if self.trace is not None:
            self.trace.append((self.t, *event))

    def at(self, when: float, fn: Callable[[], None]) -> None:
        self._seq += 1
        heapq.heappush(self._events, (when, self._seq, fn))

    def value(self, ability: Ability, p: Player) -> float:
        key = (ability.slug, p.role)
        if key not in self._value_cache:
            self._value_cache[key] = ability_value(ability, p.role)
        return self._value_cache[key]

    def enemies(self, p: Player) -> list[Player]:
        return [q for q in self.players if q.team != p.team]

    def allies(self, p: Player) -> list[Player]:
        return [q for q in self.players if q.team == p.team]

    def targetable(self, q: Player) -> bool:
        """On the field and open to combat and ordinary abilities."""
        return (q.on_field(self.t) and not q.has_state("frozen", self.t)
                and not q.has_state("insubstantial", self.t) and not q.has_state("invulnerable", self.t))

    def attackers_of(self, p: Player) -> list[Player]:
        return [q for q in self.players if q.target == p.pid and q.alive]

    def disengage(self, p: Player) -> None:
        p.target = None
        for q in self.players:
            if q.target == p.pid:
                q.target = None

    def interrupt(self, p: Player, why: str) -> None:
        if p.casting is not None:
            slug = p.casting.uses.slug if p.casting.uses else "charge"
            self.fails[(slug, f"interrupted:{why}")] += 1
            p.casting = None

    # ------------------------------------------------------------------ passives

    def _passive_sources(self, p: Player):
        """(ability, ench) pairs whose while-active effects apply to p right now."""
        for ab in p.traits:
            yield ab, None
        if p.alive:
            for e in p.enchantments:
                yield e.ability, e

    def immune(self, p: Player, school: str) -> bool:
        if not school:
            return False
        if school == "Spirit" and p.states.get("cursed", -1) > self.t:
            return True
        for ab, ench in self._passive_sources(p):
            for eff in ab.effects:
                if eff.kind == "defense.immunity" and eff.timing == "while-active":
                    s = eff.params.get("school")
                    if s == school or (s == "choice" and ench is not None and ench.choice == school):
                        return True
        return False

    def unaffected(self, p: Player, by: str) -> bool:
        for ab, _ in self._passive_sources(p):
            for eff in ab.effects:
                if eff.kind == "defense.unaffected" and eff.params.get("by") == by:
                    return True
        return False

    def consume_resistance(self, p: Player, kind: str, school: str = "") -> bool:
        for r in p.resist:
            to = r["to"]
            if (kind == "source" and to == "next-source") or (kind == "wound" and to == "wounds") \
                    or (kind == "school" and school and r.get("school") == school):
                p.resist.remove(r)
                ench = r.get("ench")
                if ench is not None and ench in p.enchantments:
                    self.remove_enchantment(p, ench)
                self.applied[(r["slug"], "defense.resistance")] += 1
                return True
        return False

    def melee_specials(self, p: Player) -> frozenset:
        specials = set()
        if p.great_weapon:
            specials.update(("armor-breaking", "shield-crushing"))
        for ab, _ in self._passive_sources(p):
            for eff in ab.effects:
                if eff.kind == "special-effect.grant" and eff.params.get("on") == "bearer-melee-weapons":
                    specials.add(eff.params.get("effect"))
        return frozenset(specials)

    def _enchant_with(self, p: Player, kind: str, **params) -> Ench | None:
        for e in p.enchantments:
            for eff in e.ability.effects:
                if eff.kind == kind and all(eff.params.get(k) == v for k, v in params.items()):
                    return e
        return None

    # ------------------------------------------------------------------ states and enchantments

    def apply_state(self, p: Player, state: str, until: float) -> None:
        p.states[state] = max(p.states.get(state, -1.0), until)
        self.log("state", p.pid, state, until)
        if state in ("frozen", "stunned", "insubstantial", "invulnerable"):
            self.interrupt(p, state)
            self.disengage(p)
        elif state == "suppressed" and p.casting is not None and p.casting.kind == "charge":
            self.interrupt(p, state)

    def attach_enchantment(self, target: Player, uses: Uses, caster: Player) -> bool:
        ab = uses.ability
        exempt = "exempt-from-enchantment-limit" in ab.properties
        if uses.magical and not exempt and target.magical_enchantment_count() >= target.ench_slots:
            self.fails[(ab.slug, "enchantment-limit")] += 1
            return False
        if any(e.ability.slug == ab.slug for e in target.enchantments):
            self.fails[(ab.slug, "already-worn")] += 1
            return False
        ench = Ench(ab, caster.pid, uses.magical, ab.strips, "persistent" in ab.properties)
        for eff in ab.effects:
            if eff.kind == "defense.immunity" and eff.params.get("school") == "choice":
                ench.choice = self.rng.choice(eff.params.get("options") or [""])
        target.enchantments.append(ench)
        self._activate(target, ench)
        ctx = Ctx(ab, caster, target, bearer=target, ench=ench)
        self.apply_effects(ab, ("on-cast",), ctx)
        self.log("enchant", caster.pid, target.pid, ab.slug)
        return True

    def _activate(self, p: Player, ench: Ench) -> None:
        ab = ench.ability
        for eff in ab.effects:
            if eff.timing != "while-active":
                continue
            k = eff.kind
            if k == "armor.magic":
                pts = int(eff.params.get("points", 1))
                for l in LOCATIONS:
                    p.magic_armor[l] = max(p.magic_armor.get(l, 0), pts)
            elif k == "defense.resistance":
                school = eff.params.get("to")
                if school == "chosen-school":
                    school = self.rng.choice(eff.params.get("options") or [""])
                    p.resist.append({"to": "school", "school": school, "ench": ench, "slug": ab.slug})
                else:
                    p.resist.append({"to": school, "ench": ench, "slug": ab.slug})
            elif k == "ability.cast-via-strips":
                slug = self.rules.by_name.get(str(eff.params.get("ability", "")).lower())
                if slug and slug not in p.uses and slug in self.rules.abilities:
                    n = ench.strips or 1
                    p.uses[slug] = Uses(self.rules.abilities[slug], None, n, n, None, None, True,
                                        range="Touch", ench=ench)
            elif k == "enchantment.extra-slot":
                p.ench_slots += int(eff.params.get("count", 1))
            elif k == "state.apply" and eff.duration_type in ("while-worn", "permanent"):
                self.apply_state(p, eff.params.get("state", ""), INF)

    def remove_enchantment(self, p: Player, ench: Ench) -> None:
        if ench not in p.enchantments or ench.trait:
            return
        p.enchantments.remove(ench)
        p.resist = [r for r in p.resist if r.get("ench") is not ench]
        for slug, u in list(p.uses.items()):
            if u.ench is ench:
                del p.uses[slug]
        for eff in ench.ability.effects:
            if eff.timing != "while-active":
                continue
            if eff.kind == "enchantment.extra-slot":
                p.ench_slots = max(1, p.ench_slots - int(eff.params.get("count", 1)))
            elif eff.kind == "state.apply" and eff.duration_type in ("while-worn", "permanent"):
                p.states.pop(eff.params.get("state", ""), None)
        self._recompute_magic_armor(p)

    def _recompute_magic_armor(self, p: Player) -> None:
        best = 0
        for e in p.enchantments:
            for eff in e.ability.effects:
                if eff.kind == "armor.magic":
                    best = max(best, int(eff.params.get("points", 1)))
        for l in LOCATIONS:
            p.magic_armor[l] = min(p.magic_armor.get(l, 0), best)

    def send_to_base(self, p: Player) -> None:
        self.interrupt(p, "moved")
        self.disengage(p)
        p.at_base_until = self.t + self.rules.a("respawn.rejoin_seconds")

    # ------------------------------------------------------------------ hits, wounds, death

    def _location(self) -> str:
        w = self.rules.a("melee.hit_location_weights")
        return self.rng.choices(LOCATIONS, weights=[w[l] for l in LOCATIONS])[0]

    def hit(self, p: Player, src: Player | None, slug: str, location: str | None = None,
            specials: frozenset = frozenset(), kind: str = "melee") -> None:
        """A weapon, arrow or Magic Ball strikes p."""
        if not self.targetable(p):  # dead, at base, Frozen, Insubstantial or Invulnerable
            return
        if kind == "arrow" and self.unaffected(p, "projectiles-except-magic-balls"):
            self.applied[("protection-from-projectiles", "defense.unaffected")] += 1
            return
        if self.consume_resistance(p, "source"):
            return
        loc = location or self._location()
        # Gift of Air: weapon and arrow hits turn the bearer Insubstantial and send them to base.
        if kind in ("melee", "arrow") and not (set(specials) & set(GIFT_OF_AIR_EXCEPT)):
            e = self._enchant_with(p, "defense.negate-hit", **{"from": "weapons-and-arrows"})
            if e is not None:
                self.applied[(e.ability.slug, "defense.negate-hit")] += 1
                self.remove_enchantment(p, e)
                self.apply_state(p, "insubstantial", self.t + self.rules.a("respawn.rejoin_seconds"))
                self.send_to_base(p)
                return
        worn, magic = p.armor.get(loc, 0), p.magic_armor.get(loc, 0)
        if worn > 0 and (e := self._enchant_with(p, "defense.negate-hit", **{"from": "hits-on-worn-armor"})):
            p.armor[loc] = worn - 1
            self.applied[(e.ability.slug, "defense.negate-hit")] += 1
            return
        if worn + magic > 0:
            if "armor-destroying" in specials or ("armor-breaking" in specials and worn + magic <= 3):
                p.armor[loc], p.magic_armor[loc] = 0, 0
            elif magic > 0:
                p.magic_armor[loc] = magic - 1
            else:
                p.armor[loc] = worn - 1
            if p.casting is not None and self.rng.random() < self.rules.a("casting.p_interrupt_on_armor_hit"):
                self.interrupt(p, "struck")
            return
        self.wound(p, loc, src, slug, specials)

    def wound(self, p: Player, loc: str, src: Player | None, slug: str, specials: frozenset = frozenset()) -> None:
        if not p.alive:
            return
        if self.consume_resistance(p, "wound"):
            return
        self.interrupt(p, "wounded")
        if "wounds-kill" in specials or loc == "torso" or p.wounds or p.has_state("fragile", self.t):
            self.kill(p, src, slug)
            return
        p.wounds.add(loc)
        self.log("wound", p.pid, loc, slug)

    def kill(self, p: Player, src: Player | None, slug: str) -> None:
        if not p.alive:
            return
        # Enchantments that prevent death (Phoenix Tears, Troll Blood, Song of Survival).
        for ench in list(p.enchantments):
            prevent = next((e for e in ench.ability.effects if e.kind == "death.prevent"), None)
            if prevent is None:
                continue
            caster = self.players[ench.caster]
            for s in list(p.states):
                if s != "cursed":
                    p.states.pop(s)
            self.interrupt(p, "death-prevented")
            self.disengage(p)
            self.applied[(ench.ability.slug, "death.prevent")] += 1
            ctx = Ctx(ench.ability, caster, p, bearer=p, ench=ench)
            self.apply_effects(ench.ability, ("on-death",), ctx)
            instead = prevent.params.get("instead")
            if instead == "insubstantial":
                self.remove_enchantment(p, ench)
                self.apply_state(p, "insubstantial", self.t + self.rules.a("respawn.rejoin_seconds"))
                self.send_to_base(p)
            elif instead == "heal-and-frozen":
                thaw = p.states.get("frozen", self.t)

                def on_thaw(p=p, ench=ench, caster=caster):
                    if p.alive and ench in p.enchantments:
                        self.apply_effects(ench.ability, ("on-expiry",), Ctx(ench.ability, caster, p, bearer=p, ench=ench))
                self.at(thaw, on_thaw)
            self.log("death-prevented", p.pid, ench.ability.slug)
            return
        p.alive = False
        p.deaths += 1
        p.dead_until = self.t + self.sc.get("respawn_seconds", 150)
        for s in list(p.states):
            if s != "cursed":
                p.states.pop(s)
        self.interrupt(p, "died")
        self.disengage(p)
        self.log("death", p.pid, src.pid if src else None, slug)
        if src is not None and src.team != p.team:
            src.kills += 1
            self.kill_sources[slug] += 1
            self._kill_trigger(src, p)
        # abilities used immediately after dying (True Grit)
        if not p.has_state("suppressed", self.t):
            for u in list(p.uses.values()):
                if "after-dying" in u.ability.requirements and u.available():
                    u.spend()
                    self.casts[u.slug] += 1
                    self.apply_effects(u.ability, ("on-cast",), Ctx(u.ability, p, p))
                    if p.alive:
                        break
        self._team_wipe_check(p.team)

    def _kill_trigger(self, k: Player, victim: Player) -> None:
        """Kill Trigger abilities and abilities cast immediately after a kill (Assassinate)."""
        if not k.alive or k.has_state("suppressed", self.t):
            return
        for u in list(k.uses.values()):
            ab = u.ability
            if not u.available():
                continue
            if "kill-trigger" in ab.properties:
                target = k
            elif "immediately-after-kill" in ab.requirements:
                target = victim
            else:
                continue
            if self.value(ab, k) <= 0:
                continue
            u.spend()
            self.casts[u.slug] += 1
            self.apply_effects(ab, ("on-kill", "on-cast"), Ctx(ab, k, target, bearer=k))

    def _team_wipe_check(self, team: int) -> None:
        """Mutual Annihilation: if everyone on a team is dead, dead players advance to their next life."""
        if self.sc.get("game_type") != "annihilation":
            return
        members = [q for q in self.players if q.team == team and not q.out]
        if members and all(not q.alive for q in members):
            for q in members:
                q.dead_until = self.t

    def revive(self, p: Player, src: Player, slug: str) -> None:
        p.alive = True
        p.dead_until = 0.0
        self.log("revive", p.pid, src.pid, slug)

    def respawn(self, p: Player) -> None:
        if p.lives_left is not None:
            p.lives_left -= 1
            if p.lives_left <= 0:
                p.out = True
                return
        p.alive = True
        p.wounds.clear()
        p.states.clear()
        p.armor = {l: p.armor_max for l in LOCATIONS}
        p.magic_armor = {l: 0 for l in LOCATIONS}
        for e in [e for e in p.enchantments if not e.persistent]:
            self.remove_enchantment(p, e)
        for e in p.enchantments:
            self._activate(p, e)
        for u in p.uses.values():
            if u.per == "life" and u.max is not None:
                u.left = u.max
        p.weapon_ok, p.shield_hits = True, 0
        p.target, p.casting = None, None
        p.at_base_until = self.t + self.rules.a("respawn.rejoin_seconds")
        self.log("respawn", p.pid)

    # ------------------------------------------------------------------ casting

    def check_requirements(self, ab: Ability, caster: Player, target: Player | None, start: bool) -> str | None:
        t = self.t
        for req in sorted(ab.requirements):  # sorted: frozenset order varies with the hash seed
            if req in ("target-dead", "target-dead-at-start"):
                if target is None or target.alive or target.out:
                    return req
            elif req == "target-wounded" and start:
                if target is None or not target.wounds:
                    return req
            elif req == "target-not-already-wounded":
                if target is None or target.wounds:
                    return req
            elif req in ("target-stopped", "target-frozen", "target-insubstantial"):
                if target is None or not target.has_state(req.split("-", 1)[1], t):
                    return req
            elif req == "target-not-cursed":
                if target is not None and target.has_state("cursed", t):
                    return req
            elif req == "caster-not-cursed":
                if caster.has_state("cursed", t):
                    return req
            elif req == "caster-not-stopped":
                if caster.has_state("stopped", t):
                    return req
            elif req in ("no-enemy-within-20ft", "no-enemy-within-10ft"):
                if caster.target is not None or self.attackers_of(caster):
                    return req
            elif req == "bearer-wears-armor":
                if target is None or target.armor_max <= 0:
                    return req
            elif req == "target-no-worn-armor":
                if target is not None and target.armor_max > 0:
                    return req
            elif req in ("immediately-after-kill", "after-dying"):
                return req  # only used through their triggers
        return None

    def blocked(self, uses: Uses, caster: Player, target: Player | None) -> str | None:
        """Why this ability has no effect on this target, if it doesn't."""
        ab = uses.ability
        if target is None:
            return None
        t = self.t
        state_ok = ({"target-frozen", "target-insubstantial"} & ab.requirements or ab.effects_of("state.remove")
                    or "bypass-states" in ab.properties)
        if target.has_state("frozen", t) and not state_ok:
            return "frozen"
        if target.has_state("insubstantial", t) and target is not caster and not state_ok:
            return "insubstantial"
        if ab.delivery != "enchantment" and "bypass-immunities" not in ab.properties and self.immune(target, ab.school):
            return "immune"
        if target is not caster:
            if uses.magical and self.unaffected(target, "magical-abilities"):
                return "unaffected"
            if ab.delivery == "verbal" and self.unaffected(target, "verbal-abilities"):
                return "unaffected"
            if ab.delivery == "verbal" and uses.magical and uses.range not in ("Touch", "Self", "Other") \
                    and self.unaffected(target, "verbal-magical-beyond-touch"):
                return "unaffected"
        harmful = any(e.polarity == "harm" for e in ab.effects)
        if harmful and target is not caster and "bypass-resistances" not in ab.properties:
            if self.consume_resistance(target, "school", ab.school) or self.consume_resistance(target, "source"):
                return "resisted"
        return None

    def start_cast(self, p: Player, uses: Uses, target: Player | None) -> bool:
        if not uses.available() or p.casting is not None:
            return False
        if p.has_state("suppressed", self.t) and "works-while-suppressed" not in uses.ability.properties:
            return False
        why = self.check_requirements(uses.ability, p, target, start=True)
        if why:
            self.fails[(uses.slug, f"requirement:{why}")] += 1
            return False
        secs = 1.0 if uses.swift else uses.ability.cast_seconds(self.words_per_second)
        p.casting = Cast(uses, target.pid if target is not None else None, secs)
        self.log("cast-start", p.pid, uses.slug, target.pid if target is not None else None)
        return True

    def start_charge(self, p: Player, uses: Uses) -> bool:
        if p.casting is not None or not uses.charge or p.has_state("suppressed", self.t):
            return False
        words = self.rules.a("time.charge_incantation_words")
        secs = math.ceil(uses.charge * words / self.words_per_second)
        p.casting = Cast(None, None, secs, kind="charge", charge_for=uses)
        return True

    def _complete(self, p: Player) -> None:
        c = p.casting
        p.casting = None
        if c.kind == "charge":
            c.charge_for.restore(1)
            self.applied[(c.charge_for.slug, "charge")] += 1
            return
        uses = c.uses
        ab = uses.ability
        if not uses.available():
            return
        uses.spend()
        if uses.ench is not None:
            uses.ench.strips = (uses.ench.strips or 1) - 1
            if uses.ench.strips <= 0:
                self.remove_enchantment(p, uses.ench)
        self.casts[ab.slug] += 1
        target = self.players[c.target] if c.target is not None else p
        if ab.delivery in ("magic-ball", "specialty-arrow"):
            self._projectile(p, uses, target)
            return
        why = self.check_requirements(ab, p, target, start=False) or self.blocked(uses, p, target)
        if why:
            self.fails[(ab.slug, why)] += 1
            return
        if ab.delivery == "enchantment":
            if not target.alive and "active-while-dead" not in ab.properties:
                self.fails[(ab.slug, "target-dead")] += 1
                return
            self.attach_enchantment(target, uses, p)
            return
        self.apply_effects(ab, ("on-cast",), Ctx(ab, p, target, bearer=p))

    def _projectile(self, p: Player, uses: Uses, target: Player) -> None:
        ab = uses.ability
        if uses.unit and uses.left == 0 and uses.max:
            u = uses
            self.at(self.t + self.rules.a("projectiles.magic_ball_retrieve_seconds"),
                    lambda u=u: setattr(u, "left", u.max))
        key = "projectiles.magic_ball_p_hit" if ab.delivery == "magic-ball" else "projectiles.arrow_p_hit"
        if not self.targetable(target) or self.rng.random() >= self.rules.a(key):
            self.fails[(ab.slug, "missed")] += 1
            return
        why = self.blocked(uses, p, target)
        if why:
            self.fails[(ab.slug, why)] += 1
            return
        specials = frozenset(e.params.get("effect") for e in ab.effects
                             if e.kind == "special-effect.grant" and e.params.get("on") in ("this-magic-ball", "this-arrow"))
        kind = "ball" if ab.delivery == "magic-ball" else "arrow"
        ctx = Ctx(ab, p, target, location=self._location(), specials=specials)
        if kind == "arrow" and self.unaffected(target, "projectiles-except-magic-balls"):
            self.fails[(ab.slug, "unaffected")] += 1
            return
        self.apply_effects(ab, ("on-struck", "on-cast"), ctx)

    def shoot(self, p: Player, target: Player) -> None:
        """A normal arrow: Armor Breaking and Weapon Destroying (rules/weapon-types-shields-equipment.md)."""
        p.next_shot_at = self.t + self.rules.a("projectiles.arrow_shot_seconds")
        if self.targetable(target) and self.rng.random() < self.rules.a("projectiles.arrow_p_hit"):
            self.hit(target, p, "arrow", specials=frozenset({"armor-breaking"}), kind="arrow")

    def apply_effects(self, ab: Ability, timings: tuple[str, ...], ctx: Ctx) -> None:
        # A Verbal with a choice (Mend, Release, Steal Life Essence) applies only the first effect
        # that works within each polarity group: e.g. Mend repairs a weapon, else a point of armor.
        choice = "has-choice" in ab.properties and ab.delivery == "verbal"
        chosen: set[str] = set()
        for eff in ab.effects:
            if choice and eff.polarity in chosen:
                continue
            if eff.timing not in timings:
                if eff.timing == "while-active" and ab.delivery not in fx.PASSIVE_DELIVERIES and "on-cast" in timings:
                    self.noops[(ab.slug, eff.kind)] += 1
                continue
            if not fx.is_handled(ab, eff):
                self.noops[(ab.slug, eff.kind)] += 1
                continue
            if fx.INSTANT[eff.kind](self, eff, ctx):
                self.applied[(ab.slug, eff.kind)] += 1
                if choice:
                    chosen.add(eff.polarity)

    # ------------------------------------------------------------------ the loop

    def _engage(self) -> None:
        t = self.t
        a = self.rules.a
        p_engage = a("engagement.p_engage_per_second")
        backline = a("engagement.backline_factor")
        caster_w = a("engagement.caster_weight_when_choosing_melee_target")
        p_dis = a("engagement.p_disengage_per_second")
        for p in self.players:
            if not p.can_act(t) or not p.on_field(t):
                p.target = None
                continue
            if p.target is not None:
                q = self.players[p.target]
                if not self.targetable(q) or self.rng.random() < p_dis:
                    p.target = None
                continue
            if p.casting is not None or p.kept_away_until > t:
                continue
            attackers = [q for q in self.attackers_of(p) if self.targetable(q)]
            if attackers:
                p.target = self.rng.choice(attackers).pid
                continue
            if p.role != "fighter" and not (p.role == "archer" and not p.has_bow):
                continue
            if self.rng.random() >= p_engage:
                continue
            foes = [q for q in self.enemies(p) if self.targetable(q) and q.kept_away_until <= t]
            if not foes:
                continue
            weights = [(backline * caster_w) if q.backline else 1.0 for q in foes]
            p.target = self.rng.choices(foes, weights=weights)[0].pid

    def _melee(self) -> None:
        t = self.t
        a = self.rules.a
        shield_logit = a("melee.shield_logit")
        k_skill = a("skill.logit_per_sd")
        gang = a("melee.gang_logit_per_extra_attacker")
        on_target = Counter(p.target for p in self.players if p.target is not None)
        order = list(self.players)
        self.rng.shuffle(order)
        for p in order:
            if p.target is None or not p.alive or not p.can_act(t) or p.casting is not None:
                continue
            if not p.weapon_ok or ("right_arm" in p.wounds and "left_arm" in p.wounds):
                continue
            d = self.players[p.target]
            if not self.targetable(d) and not d.has_state("stunned", t):
                p.target = None
                continue
            x = self._base_logit + k_skill * (p.skill - d.skill)
            x += shield_logit.get(d.shield, 0.0) if d.shield_usable() else 0.0
            x += gang * max(0, on_target[d.pid] - 1)
            if d.wounds & {"left_leg", "right_leg"}:
                x += a("melee.wounded_leg_logit")
            if "right_arm" in p.wounds:
                x += a("melee.wounded_weapon_arm_logit")
            if p.role != "fighter":
                x += a("melee.weak_weapon_logit")
            if d.has_state("stunned", t):
                x += a("melee.stunned_logit")
            specials = self.melee_specials(p)
            if self.rng.random() < _logistic(x):
                self.hit(d, p, "melee", specials=specials, kind="melee")
            elif "shield-crushing" in specials and d.shield_usable() \
                    and self.rng.random() < a("melee.p_shield_struck_on_miss"):
                d.shield_hits += 1

    def _upkeep(self) -> None:
        t = self.t
        while self._events and self._events[0][0] <= t:
            _, _, fn = heapq.heappop(self._events)
            fn()
        for p in self.players:
            if p.states:
                expired = [s for s, until in p.states.items() if until <= t]
                for s in expired:
                    del p.states[s]
            if not p.alive and not p.out:
                p.time_dead += self.dt
                if p.dead_until <= t:
                    self.respawn(p)
        if t >= self.next_refresh:
            for p in self.players:
                for u in p.uses.values():
                    if u.per == "refresh" and u.max is not None:
                        u.left = u.max
            self.next_refresh += self.sc["refresh_seconds"]

    def _progress_casts(self) -> None:
        t = self.t
        for p in self.players:
            c = p.casting
            if c is None:
                continue
            if not p.can_act(t):
                self.interrupt(p, "cannot-act")
                continue
            if c.kind == "cast" and p.has_state("suppressed", t) \
                    and "works-while-suppressed" not in c.uses.ability.properties:
                self.interrupt(p, "suppressed")
                continue
            c.remaining -= self.dt
            if c.remaining <= 0:
                self._complete(p)

    def _winner(self) -> int | None:
        """Team index, -1 for a draw, None while the game continues."""
        alive_teams = {p.team for p in self.players if not p.out}
        if len(alive_teams) == 1:
            return alive_teams.pop()
        if not alive_teams:
            return -1
        if self.t >= self.sc.get("max_seconds", self.rules.a("game.max_seconds")):
            if self.sc.get("game_type") == "annihilation":
                score = Counter()
                for p in self.players:
                    if not p.out:
                        score[p.team] += (p.lives_left or 0) - (0 if p.alive else 1)
            else:
                score = Counter()
                for p in self.players:
                    score[p.team] += p.kills
            ranked = sorted(((score[i], i) for i in range(self.n_teams)), reverse=True)
            return -1 if len(ranked) > 1 and ranked[0][0] == ranked[1][0] else ranked[0][1]
        return None

    def step(self) -> int | None:
        self.t += self.dt
        self._upkeep()
        order = list(self.players)
        self.rng.shuffle(order)
        for p in order:
            if p.alive and p.can_act(self.t):
                if p.casting is None:
                    decide(self, p)
                elif not keep_casting(self, p):
                    self.interrupt(p, "abandoned")
        self._engage()
        self._melee()
        self._progress_casts()
        return self._winner()

    def run(self) -> dict:
        self._start_holdings = self.holdings()
        winner = None
        while winner is None:
            winner = self.step()
        return self.result(winner)

    def result(self, winner: int) -> dict:
        return {
            "seed": self.seed,
            "winner": winner,
            "duration": self.t,
            "players": [
                {"pid": p.pid, "team": p.team, "cls": p.cls, "level": p.level, "skill": round(p.skill, 4),
                 "role": p.role, "kills": p.kills, "deaths": p.deaths, "time_dead": p.time_dead,
                 "won": int(p.team == winner)} for p in self.players],
            "casts": dict(self.casts),
            "applied": {f"{s}|{k}": n for (s, k), n in self.applied.items()},
            "noops": {f"{s}|{k}": n for (s, k), n in self.noops.items()},
            "fails": {f"{s}|{k}": n for (s, k), n in self.fails.items()},
            "kill_sources": dict(self.kill_sources),
            "holdings": getattr(self, "_start_holdings", None) or self.holdings(),
        }

    def holdings(self) -> dict[str, list[int]]:
        """How many players on each team started with each ability (for ablation analysis)."""
        out: dict[str, list[int]] = {}
        for p in self.players:
            slugs = set(p.uses) | {t.slug for t in p.traits} | {e.ability.slug for e in p.enchantments if e.trait}
            for s in slugs:
                out.setdefault(s, [0] * self.n_teams)[p.team] += 1
        return out


def play(rules: Rules, scenario: dict, seed: int, ablate: frozenset = frozenset(), trace: bool = False) -> dict:
    return Game(rules, scenario, seed, ablate, trace).run()
