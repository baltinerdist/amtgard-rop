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
import re
from collections import Counter
from typing import Callable

from sim.engine import effects as fx
from sim.engine.effects import Ctx
from sim.engine.loadout import _uses as make_uses
from sim.engine.loadout import build_player
from sim.engine.state import ARMS, INF, LOCATIONS, Cast, Ench, Player, Uses
from sim.policies import decide
from sim.policies.value import value as ability_value
from sim.rules import frequency as freqmod
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
        self._bars_cache: dict = {}
        self._as_per_cache: dict = {}
        self._kept_down: set = set()      # (pid, deaths) already counted as kept down by Undead Minion
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

    # ------------------------------------------------------------------ restrictions (engine queries)
    #
    # Policies choose targets; the engine enforces what a player may not do at the points where
    # attacks and casts are chosen (Game._engage, Game.start_cast, Game.shoot) and resolved
    # (Game._melee, Game._complete). Policies may consult these queries to avoid wasted choices.

    def can_attack(self, a: Player, b: Player) -> bool:
        """Whether a may attack b with a weapon blow or an arrow (Awe, Terror, Insult)."""
        if not a.restrictions:
            return True
        t = self.t
        for r in a.restrictions:
            if r.until <= t:
                continue
            if r.what == "attack-caster" and b.pid == r.src:
                return False
            if r.what == "attack-anyone-but-caster" and b.pid != r.src and b.pid not in r.allowed:
                return False
        return True

    def can_cast_at(self, a: Player, b: Player, uses: Uses) -> bool:
        """Whether a may cast this ability at b. Specialty Arrows are attacks (ruling awe#1); only
        Magical abilities are otherwise restricted, so Extraordinary ones stay allowed (awe#1, insult#3,
        terror#1). Insult's exception for others who attacked the target covers attacks only (insult#1)."""
        if uses.ability.delivery == "specialty-arrow":
            return self.can_attack(a, b)
        if not uses.magical or not a.restrictions:
            return True
        t = self.t
        for r in a.restrictions:
            if r.until <= t:
                continue
            if r.what == "cast-at-caster" and b.pid == r.src:
                return False
            if r.what == "cast-at-anyone-but-caster" and b.pid != r.src:
                return False
        return True

    def restricted_targets(self, a: Player) -> list[int]:
        """Enemies a may not attack right now (sorted pids)."""
        return [q.pid for q in self.enemies(a) if not self.can_attack(a, q)]

    def barred(self, p: Player, what: str) -> bool:
        """A while-active action.restrict on a worn Enchantment, Trait or Archetype (e.g. Gift of Air:
        may not wield weapons or shields; Sniper: may not fire normal arrows)."""
        for ab, _ in self._passive_sources(p):
            if what in self._bars(ab):
                return True
        return False

    def _bars(self, ab: Ability) -> frozenset:
        bars = self._bars_cache.get(ab.slug)
        if bars is None:
            bars = frozenset(e.params.get("what") for e in ab.effects
                             if e.kind == "action.restrict" and e.timing == "while-active" and fx.is_handled(ab, e))
            self._bars_cache[ab.slug] = bars
        return bars

    def shield_up(self, p: Player) -> bool:
        return p.shield_usable() and not self.barred(p, "wield-shields")

    def can_fire_normal_arrows(self, p: Player) -> bool:
        return p.has_bow and not self.barred(p, "fire-normal-arrows") and not self.barred(p, "wield-weapons")

    def _provoke(self, a: Player, b: Player, stage: str) -> None:
        """a attacks b ('attack'), begins casting a Magical ability at b ('cast-start'), or completes one
        on b ('cast-done'). Awe and Terror end if their caster attacks or begins casting at the target;
        an Insulted target may also attack anyone else who attacks or casts Magic on them (Insult E2)."""
        if not b.restrictions or a is b:
            return
        t = self.t
        if stage in ("attack", "cast-start"):
            gone = [r for r in b.restrictions if r.negate_on_provoke and r.src == a.pid and r.until > t]
            if gone:
                for r in gone:
                    if abs(b.kept_away_until - r.until) < 1e-9:   # the same casting's keep-away
                        b.kept_away_until = t
                slugs = [r.slug for r in gone]
                b.restrictions = [r for r in b.restrictions if not (r.src == a.pid and r.slug in slugs)]
                self.applied[(gone[0].slug, "action.restrict:negated")] += 1
                self.log("restrict-negated", b.pid, a.pid, gone[0].slug)
        if stage in ("attack", "cast-done"):
            for r in b.restrictions:
                if r.what == "attack-anyone-but-caster" and r.src != a.pid and r.until > t:
                    r.allowed.add(a.pid)

    def _end_restrictions_on_death(self, p: Player) -> None:
        """Ongoing Effects end when their bearer dies or avoids death; some end when their caster dies."""
        p.restrictions.clear()
        p.buffs.clear()
        p.prevented.clear()
        p.barrage = None
        for q in self.players:
            if q.restrictions:
                q.restrictions = [r for r in q.restrictions if not (r.ends_on_src_death and r.src == p.pid)]

    # ------------------------------------------------------------------ passives

    def _passive_sources(self, p: Player):
        """(ability, ench) pairs whose while-active effects apply to p right now."""
        for ab in p.traits:
            yield ab, None
        if p.alive:
            for e in p.enchantments:
                yield e.ability, e

    def _passive_effects(self, ab: Ability) -> tuple:
        """ab's effects plus the while-active effects of abilities it grants "as per" (Song of
        Interference as per Enlightened Soul, Troll Blood as per Regeneration)."""
        effs = self._as_per_cache.get(ab.slug)
        if effs is None:
            effs = list(ab.effects)
            for eff in ab.effects:
                if eff.kind == "ability.grant" and eff.params.get("how") == "as-per" \
                        and eff.params.get("ability") in fx.AS_PER_EXPAND and fx.is_handled(ab, eff):
                    other = self.rules.abilities.get(self.rules.by_name.get(str(eff.params["ability"]).lower(), ""))
                    if other is not None:
                        effs.extend(e for e in other.effects if e.timing == "while-active")
            effs = tuple(effs)
            self._as_per_cache[ab.slug] = effs
        return effs

    def immune(self, p: Player, school: str, ignore_cursed: bool = False) -> bool:
        if not school:
            return False
        if school == "Spirit" and not ignore_cursed and p.states.get("cursed", -1) > self.t:
            return True
        for ab, ench in self._passive_sources(p):
            for eff in self._passive_effects(ab):
                if eff.kind == "defense.immunity" and eff.timing == "while-active":
                    s = eff.params.get("school")
                    if s == school or (s == "choice" and ench is not None and ench.choice == school):
                        return True
        return False

    def unaffected(self, p: Player, by: str) -> bool:
        for ab, _ in self._passive_sources(p):
            for eff in self._passive_effects(ab):
                if eff.kind == "defense.unaffected" and eff.params.get("by") == by:
                    return True
        return any(b.effect.kind == "defense.unaffected" and b.effect.params.get("by") == by
                   for b in self._buffs(p))

    def _buffs(self, p: Player) -> list:
        """p's active Ongoing Effects from Verbals (Rage, Circle of Protection)."""
        if not p.buffs:
            return []
        t = self.t
        return [b for b in p.buffs if b.until > t and (b.rides_state is None or p.has_state(b.rides_state, t))]

    def unaffected_by_school(self, p: Player, school: str) -> Ability | None:
        """Void Touched: unaffected by Magical abilities from the listed Schools."""
        for ab, _ in self._passive_sources(p):
            for eff in ab.effects:
                if eff.kind == "defense.unaffected" and eff.params.get("by") == "schools" \
                        and school in (eff.params.get("schools") or ()):
                    return ab
        return None

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
            for eff in self._passive_effects(ab):
                if eff.kind == "special-effect.grant" and eff.params.get("on") == "bearer-melee-weapons":
                    specials.add(eff.params.get("effect"))
        for b in self._buffs(p):
            if b.effect.kind == "special-effect.grant" and b.effect.params.get("on") == "bearer-melee-weapons":
                specials.add(b.effect.params.get("effect"))
        return frozenset(specials)

    def equipment_protection(self, p: Player, item: str, object_destroying: bool = False) -> Ench | None:
        """The worn Enchantment protecting p's wielded 'weapon' or 'shield' from damage: Harden and the
        abilities affected as per Harden (except against object-destroying Magic Balls and Verbals),
        or Imbue (cannot be destroyed nor damaged at all)."""
        for e in p.enchantments:
            for eff in e.ability.effects:
                if eff.kind == "equipment.protect":
                    what, degree = eff.params.get("what"), eff.params.get("degree")
                elif eff.kind == "ability.grant" and eff.params.get("how") == "as-per" \
                        and eff.params.get("ability") == "Harden" and e.ability.slug in fx.AS_PER_HARDEN:
                    what, degree = fx.AS_PER_HARDEN[e.ability.slug], "except-object-destroying-abilities"
                else:
                    continue
                if object_destroying and degree != "indestructible":
                    continue
                if what == "weapons-and-shields" or (what == "weapons-or-shield" and e.choice == item) \
                        or (what in ("weapons", "shield") and what.rstrip("s") == item
                            and (e.choice is None or e.choice == item)):
                    return e
        return None

    def _worn_with(self, p: Player, kind: str, key: str, value: str) -> Ench | None:
        for e in p.enchantments:
            if any(eff.kind == kind and eff.params.get(key) == value for eff in e.ability.effects):
                return e
        return None

    def weapon_usable(self, p: Player) -> bool:
        """Not destroyed and not Heat Weapon'd."""
        return p.weapon_ok and p.weapon_hot_until <= self.t

    def _poison(self, p: Player) -> Ench | None:
        """A worn Enchantment making p's next melee wound Wounds Kill (Poison)."""
        for e in p.enchantments:
            for eff in e.ability.effects:
                if eff.kind == "special-effect.grant" and eff.params.get("on") == "next-wound":
                    return e
        return None

    def modifier(self, p: Player, phrase: str) -> Ability | None:
        """The worn Enchantment, Trait or Archetype carrying an engine-level ability.modify (see
        effects.ENGINE_MODIFIES), if p has one."""
        for ab, _ in self._passive_sources(p):
            for eff in ab.effects:
                if eff.kind == "ability.modify" and fx.engine_modify(str(eff.params.get("change", ""))) == phrase:
                    return ab
        return None

    @staticmethod
    def _modify_target(ab: Ability) -> str:
        """The ability name an engine-level ability.modify on ab refers to."""
        return next((str(e.params.get("ability", "")) for e in ab.effects
                     if e.kind == "ability.modify" and fx.engine_modify(str(e.params.get("change", "")))), "")

    def _ancestral_magic_armor(self, p: Player) -> Ench | None:
        for e in p.enchantments:
            if e.ability.effects_of("armor.magic") and any(
                    eff.kind == "ability.grant" and eff.params.get("how") == "as-per"
                    and eff.params.get("ability") == fx.AS_PER_MAGIC_ARMOR for eff in e.ability.effects):
                return e
        return None

    def _enchant_with(self, p: Player, kind: str, **params) -> Ench | None:
        for e in p.enchantments:
            for eff in e.ability.effects:
                if eff.kind == kind and all(eff.params.get(k) == v for k, v in params.items()):
                    return e
        return None

    # ------------------------------------------------------------------ states and enchantments

    def prevented(self, p: Player, state: str, own: bool = True) -> Ability | str | None:
        """Why p cannot gain this State now: Planar Grounding ('planar-grounding'), or Song of Freedom
        (unless the State is caused by p or an Enchantment p carries)."""
        if p.prevented.get(state, -1.0) > self.t:
            return "planar-grounding"
        if not own:
            for ab, _ in self._passive_sources(p):
                for eff in ab.effects:
                    if eff.kind == "state.prevent" and state in (eff.params.get("states") or ()) \
                            and eff.timing == "while-active":
                        return ab
        return None

    def apply_state(self, p: Player, state: str, until: float, own: bool = True) -> bool:
        why = self.prevented(p, state, own)
        if why is not None:
            slug = why if isinstance(why, str) else why.slug
            self.applied[(slug, "state.prevent")] += 1
            return False
        p.states[state] = max(p.states.get(state, -1.0), until)
        self.log("state", p.pid, state, until)
        if state in ("frozen", "stunned", "insubstantial", "invulnerable"):
            self.interrupt(p, state)
            self.disengage(p)
        elif state == "suppressed" and p.casting is not None and p.casting.kind == "charge":
            self.interrupt(p, state)
        return True

    def _grounded(self, p: Player, ench: Ench) -> bool:
        """Planar Grounding: an Enchantment that would make its bearer Insubstantial fails and is
        removed; the triggering event takes effect normally (ruling planar-grounding#1)."""
        if p.prevented.get("insubstantial", -1.0) <= self.t:
            return False
        self.remove_enchantment(p, ench)
        self.applied[("planar-grounding", "enchantment.remove")] += 1
        return True

    def attach_enchantment(self, target: Player, uses: Uses, caster: Player, persistent: bool = False) -> bool:
        ab = uses.ability
        exempt = "exempt-from-enchantment-limit" in ab.properties
        if uses.magical and not exempt and target.magical_enchantment_count() >= target.ench_slots:
            self.fails[(ab.slug, "enchantment-limit")] += 1
            return False
        if any(e.ability.slug == ab.slug for e in target.enchantments):
            self.fails[(ab.slug, "already-worn")] += 1
            return False
        cap = self._per_caster_cap(ab, caster)
        if cap is not None:
            active = sum(1 for q in self.players for e in q.enchantments
                         if e.ability.slug == ab.slug and e.caster == caster.pid)
            base = self.PER_CASTER_CAPS.get(ab.slug)
            if active >= cap:
                self.fails[(ab.slug, "per-caster-limit")] += 1
                if base is None or cap < base:          # Guardian's one-Imbue limit bit
                    self.applied[("guardian", "ability.modify")] += 1
                return False
            if base is not None and active >= base:     # Necromancer's extra Minions used
                self.applied[("necromancer", "ability.modify")] += 1
        # Essence Graft: the bearer may only wear (m) Enchantments from the Graft's caster
        if uses.magical:
            graft = next((e for e in target.enchantments
                          if "wear-others-magical-enchantments" in self._bars(e.ability)), None)
            if graft is not None and graft.caster != caster.pid:
                self.fails[(ab.slug, "restricted:essence-graft")] += 1
                return False
        ench = Ench(ab, caster.pid, uses.magical, ab.strips, persistent or "persistent" in ab.properties)
        if "wear-others-magical-enchantments" in self._bars(ab):
            # the new Graft's bearer drops (m) Enchantments from anyone else (reading of Essence Graft L1)
            for e in [e for e in target.enchantments if e.magical and e.caster != caster.pid]:
                self.remove_enchantment(target, e)
                self.applied[(ab.slug, "action.restrict")] += 1
        for eff in ab.effects:
            if eff.kind == "defense.immunity" and eff.params.get("school") == "choice":
                ench.choice = self.rng.choice(eff.params.get("options") or [""])
        if ("has-choice" in ab.properties and ab.effects_of("equipment.protect")) \
                or fx.AS_PER_HARDEN.get(ab.slug) == "weapons-or-shield":
            # Harden / Imbue: weapons or shield, chosen once when cast (rulings harden#1, imbue#1);
            # random like other choices, and weapons for a bearer without a shield
            ench.choice = self.rng.choice(("weapon", "shield")) if target.shield != "none" else "weapon"
        target.enchantments.append(ench)
        self._activate(target, ench)
        ctx = Ctx(ab, caster, target, bearer=target, ench=ench)
        self.apply_effects(ab, ("on-cast",), ctx)
        self.log("enchant", caster.pid, target.pid, ab.slug)
        return True

    def _grant(self, bearer: Player, ench: Ench, eff, effects: tuple) -> None:
        """An Enchantment's `ability.grant ... gains`: uses tracked separately from the player's own
        (Enchantments rule 6) and taken away when the Enchantment is removed. Modifiers of the granted
        ability recorded on the same Enchantment (Regeneration, Undead Minion) apply to these uses."""
        prm = eff.params
        name = str(prm.get("ability", ""))
        slug = self.rules.by_name.get(name.lower())
        if not slug or slug in self.ablate or not fx.is_handled(ench.ability, eff):
            return
        holder = self.players[ench.caster] if eff.subject == "caster-of-enchantment" else bearer
        if any(u.granted_by is ench and u.slug == slug for u in holder.uses.values()):
            return   # already granted (re-activation after a respawn with a Persistent Enchantment)
        raw = str(prm.get("frequency", ""))
        f = freqmod.parse(raw)
        u = make_uses(self.rules.abilities[slug], f, 1, f.magical is True, raw)
        u.swift = u.swift or prm.get("meta") == "Swift"
        u.granted_by = ench
        for m in effects:
            if m.kind != "ability.modify" or m.params.get("ability") != name:
                continue
            change = str(m.params.get("change", ""))
            if m.params.get("requirement"):
                u.extra_reqs = u.extra_reqs | {m.params["requirement"]}
            if "only be cast with the bearer as the target" in change:
                u.only_target = bearer.pid
            if "ignores the requirement that the target has not moved" in change:
                u.drop_reqs = u.drop_reqs | {"target-not-moved-5ft"}
        key = slug if slug not in holder.uses else f"{slug}@{ench.ability.slug}"
        holder.uses[key] = u

    # Per-caster limits written in the abilities' Limitations: Golem "a single Golem Enchantment at a
    # time", Undead Minion "not more than three".
    PER_CASTER_CAPS = {"golem": 1, "undead-minion": 3}

    def _per_caster_cap(self, ab: Ability, caster: Player) -> int | None:
        if ab.slug == "undead-minion" and self.modifier(caster, "combined total of five Undead Minion"):
            return 5      # Necromancer
        if ab.slug == "imbue" and self.modifier(caster, "only one instance of Imbue may be active"):
            return 1      # Guardian
        return self.PER_CASTER_CAPS.get(ab.slug)

    def _activate(self, p: Player, ench: Ench) -> None:
        ab = ench.ability
        effects = self._passive_effects(ab)
        for eff in effects:
            if eff.timing != "while-active":
                continue
            k = eff.kind
            if k == "ability.grant" and eff.params.get("how") != "as-per":
                self._grant(p, ench, eff, effects)
                continue
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
                if slug and slug in self.rules.abilities and not any(u.ench is ench for u in p.uses.values()):
                    n = ench.strips or 1
                    # tracked apart from the player's own uses of the same ability (Enchantments rule 6)
                    key = slug if slug not in p.uses else f"{slug}@{ab.slug}"
                    p.uses[key] = Uses(self.rules.abilities[slug], None, n, n, None, None, True,
                                       range="Touch", ench=ench)
                    decl = next((d for d in ab.effects if d.kind == "ability.declare-instead"), None)
                    if decl is not None and (m := re.search(r'"([^"]+)"', str(decl.params.get("what", "")))):
                        p.uses[key].declare_words = len(m.group(1).split())   # Mass Healing
            elif k == "enchantment.extra-slot":
                p.ench_slots += int(eff.params.get("count", 1))
            elif k == "state.apply" and eff.duration_type in fx.PASSIVE_STATE_DURATIONS and fx.is_handled(ab, eff):
                self.apply_state(p, eff.params.get("state", ""), INF)

    def remove_enchantment(self, p: Player, ench: Ench) -> None:
        if ench not in p.enchantments or ench.trait:
            return
        p.enchantments.remove(ench)
        p.resist = [r for r in p.resist if r.get("ench") is not ench]
        for holder in (p, self.players[ench.caster]):
            for slug, u in list(holder.uses.items()):
                if u.ench is ench or u.granted_by is ench:
                    del holder.uses[slug]
        for eff in ench.ability.effects:
            if eff.timing != "while-active":
                continue
            if eff.kind == "enchantment.extra-slot":
                p.ench_slots = max(1, p.ench_slots - int(eff.params.get("count", 1)))
            elif eff.kind == "state.apply" and eff.duration_type in fx.PASSIVE_STATE_DURATIONS and fx.is_handled(ench.ability, eff):
                p.states.pop(eff.params.get("state", ""), None)
        self._recompute_magic_armor(p)
        if any(e.timing == "on-removal" for e in ench.ability.effects):
            self.apply_effects(ench.ability, ("on-removal",),
                               Ctx(ench.ability, self.players[ench.caster], p, bearer=p, ench=ench))

    def _recompute_magic_armor(self, p: Player) -> None:
        best = 0
        for e in p.enchantments:
            for eff in e.ability.effects:
                if eff.kind == "armor.magic":
                    best = max(best, int(eff.params.get("points", 1)))
        for l in LOCATIONS:
            p.magic_armor[l] = min(p.magic_armor.get(l, 0), best)

    def arrival_time(self, p: Player) -> float:
        """When a player sent to base now gets there (the rejoin time stands for the walk)."""
        return self.t + self.rules.a("respawn.rejoin_seconds")

    def _insubstantial_choice(self, p: Player, ench: Ench) -> None:
        """Gift of Air / Song of Survival: right after activating, the bearer chooses option 1
        (Insubstantial in place, may exit at any time) or option 2 (Insubstantial return to base as
        Forced Movement, may not exit early, exits on arrival). The choice is random, like other
        chosen options. Option 2's lock is applied before its State."""
        ab = ench.ability
        want = self.rng.choice(("until-removed", "until-arrival"))
        effs = sorted((e for e in ab.effects if e.timing == "on-choice" and e.duration_type == want),
                      key=lambda e: e.kind != "action.restrict")
        ctx = Ctx(ab, p, p, bearer=p, ench=ench)   # the bearer's own choice and State
        for eff in effs:
            if fx.is_handled(ab, eff) and fx.INSTANT[eff.kind](self, eff, ctx):
                self.applied[(ab.slug, eff.kind)] += 1
        self.log("choice", p.pid, ab.slug, want)

    def send_to_base(self, p: Player) -> None:
        self.interrupt(p, "moved")
        self.disengage(p)
        p.at_base_until = self.t + self.rules.a("respawn.rejoin_seconds")

    # ------------------------------------------------------------------ hits, wounds, death

    def _location(self) -> str:
        w = self.rules.a("melee.hit_location_weights")
        return self.rng.choices(LOCATIONS, weights=[w[l] for l in LOCATIONS])[0]

    def hit(self, p: Player, src: Player | None, slug: str, location: str | None = None,
            specials: frozenset = frozenset(), kind: str = "melee") -> bool | None:
        """A weapon, arrow or Magic Ball strikes p. Truthy when p received a wound."""
        if not self.targetable(p):  # dead, at base, Frozen, Insubstantial or Invulnerable
            return
        if kind == "arrow" and self.unaffected(p, "projectiles-except-magic-balls"):
            self.applied[("protection-from-projectiles", "defense.unaffected")] += 1
            return
        if self.consume_resistance(p, "source"):
            return
        loc = location or self._location()
        # Gift of Air: the weapon or arrow hit is ignored and the bearer becomes Insubstantial, in place
        # or returning to base (their choice). It stays on for later hits (ruling gift-of-air#1).
        # Melee Siege/Armor-/Shield-breaking weapons don't trigger it; arrows always do (gift-of-air#3).
        if kind == "arrow" or (kind == "melee" and not (set(specials) & set(GIFT_OF_AIR_EXCEPT))):
            e = self._enchant_with(p, "defense.negate-hit", **{"from": "weapons-and-arrows"})
            if e is not None and not self._grounded(p, e):
                self.applied[(e.ability.slug, "defense.negate-hit")] += 1
                if worn := p.armor.get(loc, 0):      # worn armor is affected as normal (E2)
                    broken = "armor-destroying" in specials or ("armor-breaking" in specials and worn <= 3)
                    p.armor[loc] = 0 if broken else worn - 1
                self._insubstantial_choice(p, e)
                return
        worn, magic = p.armor.get(loc, 0), p.magic_armor.get(loc, 0)
        # Sacred Blades: the bearer's melee weapons ignore Magic Armor and Resistances to wounds
        sacred = self._worn_with(src, "weapon.ignore-protections", "against", "magic-armor") \
            if kind == "melee" and src is not None and src.enchantments else None
        if sacred is not None and magic > 0:
            magic = 0
            self.applied[(sacred.ability.slug, "weapon.ignore-protections")] += 1
        if worn > 0 and (e := self._enchant_with(p, "defense.negate-hit", **{"from": "hits-on-worn-armor"})):
            p.armor[loc] = worn - 1
            self.applied[(e.ability.slug, "defense.negate-hit")] += 1
            return
        if "armor-breaking" in specials and worn > 0 and magic == 0 \
                and (ha := self._worn_with(p, "armor.protect", "against", "armor-breaking")) is not None:
            # Harden Armor: Armor Breaking strikes to worn armor are regular strikes (not Magic Armor)
            specials = specials - {"armor-breaking"}
            self.applied[(ha.ability.slug, "armor.protect")] += 1
        if magic > 0 and (e := self._ancestral_magic_armor(p)) is not None:
            # Stoneskin / Ironskin: their Magic Armor is affected as per Ancestral Armor, so any hit
            # on it only removes one point, whatever its special effects
            p.magic_armor[loc] = magic - 1
            self.applied[(e.ability.slug, "ability.grant")] += 1
            if p.casting is not None and self.rng.random() < self.rules.a("casting.p_interrupt_on_armor_hit"):
                self.interrupt(p, "struck")
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
        pierce = sacred is not None and self._worn_with(src, "weapon.ignore-protections", "against",
                                                         "wound-resistances") is not None
        return self.wound(p, loc, src, slug, specials, ignore_resistance=pierce)

    def wound(self, p: Player, loc: str, src: Player | None, slug: str, specials: frozenset = frozenset(),
              ignore_resistance: bool = False) -> bool:
        if not p.alive:
            return False
        if ignore_resistance and any(r["to"] == "wounds" for r in p.resist):
            self.applied[("sacred-blades", "weapon.ignore-protections")] += 1
        elif self.consume_resistance(p, "wound"):
            return False
        self.interrupt(p, "wounded")
        if "wounds-kill" in specials or loc == "torso" or p.wounds or p.has_state("fragile", self.t):
            self.kill(p, src, slug)
        else:
            p.wounds.add(loc)
            self.log("wound", p.pid, loc, slug)
        self._wound_trigger(src, p)
        return True

    def _wound_trigger(self, src: Player | None, victim: Player) -> None:
        """Wound Trigger abilities (Brutal Strike): used immediately after the caster causes a wound to
        an enemy, even if it kills them, but not if the wound is not received (mechanics: Trigger)."""
        if src is None or src.team == victim.team or not src.alive or src.has_state("suppressed", self.t):
            return
        for u in list(src.uses.values()):
            ab = u.ability
            if "wound-trigger" not in ab.properties or not u.available() or self.value(ab, src) <= 0:
                continue
            u.spend()
            self.casts[ab.slug] += 1
            why = self.blocked(u, src, victim)
            if why:
                self.fails[(ab.slug, why)] += 1
            else:
                self.apply_effects(ab, ("on-wound",), Ctx(ab, src, victim))
            return

    def kill(self, p: Player, src: Player | None, slug: str) -> None:
        if not p.alive:
            return
        # Enchantments that prevent death (Phoenix Tears, Troll Blood, Song of Survival).
        for ench in list(p.enchantments):
            prevent = next((e for e in ench.ability.effects if e.kind == "death.prevent"), None)
            if prevent is None:
                continue
            if prevent.params.get("instead") == "insubstantial" and self._grounded(p, ench):
                continue
            caster = self.players[ench.caster]
            for s in list(p.states):
                if s != "cursed":
                    p.states.pop(s)
            p.restrictions.clear()   # Ongoing Effects end when an ability lets the player avoid death
            p.buffs.clear()
            p.prevented.clear()
            self.interrupt(p, "death-prevented")
            self.disengage(p)
            self.applied[(ench.ability.slug, "death.prevent")] += 1
            ctx = Ctx(ench.ability, caster, p, bearer=p, ench=ench)
            self.apply_effects(ench.ability, ("on-death",), ctx)
            instead = prevent.params.get("instead")
            if instead == "insubstantial":
                self.remove_enchantment(p, ench)     # Song of Survival ends at once (E3)
                self._insubstantial_choice(p, ench)
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
        self._end_restrictions_on_death(p)
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
        # "may only use one Kill Trigger ability per eligible killing blow": the most valuable usable one
        triggers = sorted((u for u in k.uses.values() if "kill-trigger" in u.ability.properties),
                          key=lambda u: (-self.value(u.ability, k), u.slug))
        for u in triggers:
            if self._fire_after_kill(k, u, k):
                break
        for u in list(k.uses.values()):
            if "kill-trigger" not in u.ability.properties and "immediately-after-kill" in u.ability.requirements:
                self._fire_after_kill(k, u, victim)

    def _fire_after_kill(self, k: Player, u: Uses, target: Player) -> bool:
        ab = u.ability
        if not u.available() or self.value(ab, k) <= 0:
            return False
        if target is k and "bypass-immunities" not in ab.properties and self.immune(k, ab.school):
            # e.g. a Cursed player is Immune to Spirit, so their own Adrenaline has no effect;
            # Vampirism's Adrenaline works through Cursed (ruling vampirism#1: any Adrenaline)
            vamp = self.modifier(k, "works through their Cursed State")
            if vamp is None or ab.name != self._modify_target(vamp) \
                    or self.immune(k, ab.school, ignore_cursed=True):
                return False
            self.applied[(vamp.slug, "ability.modify")] += 1
        u.spend()
        self.casts[u.slug] += 1
        self.apply_effects(ab, ("on-kill", "on-cast"), Ctx(ab, k, target, bearer=k))
        return True

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

    def _persisting(self, p: Player) -> list[Ench]:
        """Enchantments that return with p after respawning: Persistent ones, all of them while Golem
        is worn, and Phoenix Tears' extra Protection Enchantment while Phoenix Tears is worn (the
        most recently attached (m) Protection one, when the extra slot is in use)."""
        keep = [e for e in p.enchantments if e.persistent]
        golem = next((e for e in p.enchantments if any(x.kind == "enchantment.make-persistent" and
                                                       x.params.get("which") == "all-worn" for x in e.ability.effects)), None)
        if golem is not None:
            self.applied[(golem.ability.slug, "enchantment.make-persistent")] += 1
            return list(p.enchantments)
        pt = next((e for e in p.enchantments if any(x.kind == "enchantment.make-persistent" and
                                                    x.params.get("which") == "the-extra-enchantment" for x in e.ability.effects)), None)
        if pt is not None and p.magical_enchantment_count() >= p.ench_slots:
            extra = [e for e in p.enchantments if e is not pt and e.magical and e.ability.school == "Protection"
                     and "exempt-from-enchantment-limit" not in e.ability.properties]
            if extra and not extra[-1].persistent:
                keep.append(extra[-1])
                self.applied[(pt.ability.slug, "enchantment.make-persistent")] += 1
        return keep

    def _respawn_prevented(self, p: Player) -> bool:
        """Undead Minion: the bearer cannot respawn while enchanted. The engine keeps them down only
        while its caster is alive to Raise them; after that the bearer removes the Enchantment
        (Enchantments rule 8) and respawns, so a game cannot stall on a minion nobody can raise."""
        for e in p.enchantments:
            if e.ability.effects_of("life.prevent-respawn"):
                caster = self.players[e.caster]
                if caster.alive and caster is not p:
                    if (p.pid, p.deaths) not in self._kept_down:
                        self._kept_down.add((p.pid, p.deaths))
                        self.applied[(e.ability.slug, "life.prevent-respawn")] += 1
                    return True
                self.remove_enchantment(p, e)
        return False

    def respawn(self, p: Player) -> None:
        if p.lives_left is not None:
            p.lives_left -= 1
            if p.lives_left <= 0:
                p.out = True
                return
        p.alive = True
        p.wounds.clear()
        p.states.clear()
        p.restrictions.clear()
        p.buffs.clear()
        p.prevented.clear()
        p.barrage = None
        p.exit_lock_until = 0.0
        p.meta_armed.clear()
        p.armor = {l: p.armor_max for l in LOCATIONS}
        p.magic_armor = {l: 0 for l in LOCATIONS}
        keep = {id(e) for e in self._persisting(p)}
        for e in [e for e in p.enchantments if id(e) not in keep]:
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

    def check_requirements(self, ab: Ability, caster: Player, target: Player | None, start: bool,
                           uses: Uses | None = None) -> str | None:
        t = self.t
        reqs = ab.requirements
        if uses is not None and (uses.extra_reqs or uses.drop_reqs):
            reqs = (reqs | uses.extra_reqs) - uses.drop_reqs
        if uses is not None and uses.only_target is not None and (target is None or target.pid != uses.only_target):
            return "only-target"
        for req in sorted(reqs):  # sorted: frozenset order varies with the hash seed
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
        if ab.slug == "blink" and self.unaffected(target, "blink"):
            return "unaffected"          # Circle of Protection
        if target is not caster:
            if uses.magical and self.unaffected(target, "magical-abilities"):
                return "unaffected"
            if uses.magical and ab.delivery != "enchantment":
                # Void Touched; new Enchantments can still be applied (ruling void-touched#1)
                vt = self.unaffected_by_school(target, ab.school)
                if vt is not None:
                    self.applied[(vt.slug, "defense.unaffected")] += 1
                    return "unaffected"
            if ab.slug != "banish" and ("forced-movement" in ab.properties or ab.effects_of(
                    "move.push", "move.keep-away", "move.to-location", "move.to-caster", "move.to-base")) \
                    and self.unaffected(target, "forced-movement-except-banish"):
                return "unaffected"      # Circle of Protection
            if ab.delivery == "verbal" and self.unaffected(target, "verbal-abilities"):
                return "unaffected"
            if ab.delivery == "verbal" and uses.magical and uses.range not in ("Touch", "Self", "Other") \
                    and self.unaffected(target, "verbal-magical-beyond-touch"):
                return "unaffected"
        harmful = any(e.polarity == "harm" for e in ab.effects)
        if harmful and target is not caster and "bypass-resistances" not in ab.properties \
                and "targets-equipment" not in ab.properties:   # heat-weapon#1: the item is the target
            if self.consume_resistance(target, "school", ab.school) or self.consume_resistance(target, "source"):
                return "resisted"
        return None

    def start_cast(self, p: Player, uses: Uses, target: Player | None) -> bool:
        if not uses.available() or p.casting is not None:
            return False
        ab = uses.ability
        # a declaration instead of an incantation (Mass Healing's Heal, Elemental Barrage's balls) is
        # not stopped by Suppressed and takes only as long as the words said
        barrage = ab.delivery == "magic-ball" and p.barrage is not None and p.barrage.get(uses.slug, 0) > 0
        declare_words = uses.declare_words or (len(ab.name.split()) if barrage else None)
        if p.has_state("suppressed", self.t) and "works-while-suppressed" not in ab.properties \
                and declare_words is None:
            return False
        why = self.check_requirements(uses.ability, p, target, start=True, uses=uses)
        if why:
            self.fails[(uses.slug, f"requirement:{why}")] += 1
            return False
        aimed = target if target is not None else p
        if not self.can_cast_at(p, aimed, uses) or (uses.ability.delivery == "specialty-arrow" and (
                self.barred(p, "wield-weapons") or not self.weapon_usable(p))):
            self.fails[(uses.slug, "restricted")] += 1
            return False
        if declare_words is not None:
            secs, persistent = max(1.0, float(round(declare_words / self.words_per_second))), False
            if barrage:
                p.barrage[uses.slug] -= 1
                self.applied[("elemental-barrage", "ability.declare-instead")] += 1
            else:
                self.applied[(uses.ench.ability.slug if uses.ench else ab.slug, "ability.declare-instead")] += 1
        else:
            if p.barrage is not None and uses.magical:
                p.barrage = None          # Elemental Barrage ends on beginning any new Magical ability
            secs = 1.0 if uses.swift else ab.cast_seconds(self.words_per_second)
            secs, persistent = self._apply_meta_magic(p, uses, secs)
            self._begin_incantation(p)
        p.casting = Cast(uses, target.pid if target is not None else None, secs, persistent=persistent,
                         declared=declare_words is not None)
        if uses.magical and aimed is not p:
            self._provoke(p, aimed, "cast-start")
        self.log("cast-start", p.pid, uses.slug, target.pid if target is not None else None)
        return True

    def start_charge(self, p: Player, uses: Uses) -> bool:
        if p.casting is not None or not uses.charge or p.has_state("suppressed", self.t):
            return False
        words = self.rules.a("time.charge_incantation_words")
        reps = uses.charge
        song = self._song_of_power_near(p)
        if song is not None:
            # Song of Power: a friendly player within 20' of the singer halves their Charge repetitions
            reps = max(1, reps // 2)
            self.applied[(song.ability.slug, "ability.charge-faster")] += 1
        secs = math.ceil(reps * words / self.words_per_second)
        self._begin_incantation(p)
        p.casting = Cast(None, None, secs, kind="charge", charge_for=uses)
        return True

    # ------------------------------------------------------------------ Meta-Magic
    #
    # Scripted players never state a Meta-Magic, so the engine does when a cast starts: it uses one
    # whenever the Meta-Magic is allowed and helps (Swift when one iteration is quicker, Extension when
    # the target is beyond 20', Persistent on any Enchantment not already Persistent). Meta-Magics may
    # not modify abilities granted by Enchantments (Meta-Magic rule 6), and are spent even if the
    # ability then fails (rule 5). Their one-word incantations are not timed.

    def _meta_use(self, p: Player, name: str, target_ab: Ability) -> Uses | None:
        """A usable Meta-Magic of this name for target_ab, respecting Priest (Spirit abilities only),
        Legend (Swift may not be used) and Amplification / Silver Tongue (only their own grant)."""
        if self.modifier(p, "may only be used on Spirit abilities") and target_ab.school != "Spirit":
            return None
        if any(e.kind == "ability.remove" and str(e.params.get("ability", "")).lower() == name
               for t in p.traits for e in t.effects):
            return None
        cands = [u for u in p.uses.values() if u.ability.slug == name and u.available()]
        for e in p.enchantments:
            if "use-other-sources-of-ability" in self._bars_all(e.ability) and any(
                    x.kind == "ability.grant" and str(x.params.get("ability", "")).lower() == name
                    for x in e.ability.effects):
                cands = [u for u in cands if u.granted_by is e]
                if cands:
                    self.applied[(e.ability.slug, "action.restrict")] += 1
        return cands[0] if cands else None

    def _bars_all(self, ab: Ability) -> frozenset:
        return frozenset(e.params.get("what") for e in ab.effects if e.kind == "action.restrict")

    def _offer_extension(self, p: Player) -> None:
        """Advertise 50' for p's own 20' Verbals while p can state Extension for them (policies roll
        range from Uses.range); Game._apply_meta_magic settles whether Extension was needed."""
        ext = self._meta_ext_ready(p)
        for u in p.uses.values():
            if u.ability.delivery != "verbal" or u.granted_by is not None or u.ench is not None:
                continue
            if not u.base_range:
                u.base_range = u.range
            if u.base_range == "20'":
                u.range = "50'" if ext and self._meta_use(p, "extension", u.ability) else "20'"

    def _meta_ext_ready(self, p: Player) -> bool:
        return any(u.ability.slug == "extension" and u.available() for u in p.uses.values())

    def _apply_meta_magic(self, p: Player, uses: Uses, secs: float) -> tuple[float, bool]:
        ab = uses.ability
        armed = p.meta_armed
        persistent = False
        if uses.granted_by is not None or uses.ench is not None:
            return secs, False                               # rule 6
        if ab.delivery == "verbal" and uses.base_range == "20'" and uses.range == "50'":
            table = self.rules.a("range.p_in_range")
            if self.rng.random() >= table["20'"] / table["50'"]:     # the target was beyond 20'
                self._spend_meta(p, "extension", ab, armed)
        if not uses.swift and (uses.range in ("Touch", "Other", "Self") or ab.delivery == "magic-ball"):
            single = max(1.0, float(round(ab.words / self.words_per_second)))
            if single < secs and self._spend_meta(p, "swift", ab, armed):
                secs = single
        if ab.delivery == "enchantment" and "persistent" not in ab.properties:
            persistent = self._spend_meta(p, "persistent", ab, armed)
        armed.clear()
        return secs, persistent

    def _spend_meta(self, p: Player, name: str, ab: Ability, armed: set) -> bool:
        if name in armed:
            armed.discard(name)
            return True
        u = self._meta_use(p, name, ab)
        if u is None:
            return False
        u.spend()
        self.casts[u.slug] += 1
        self.applied[(u.slug, "meta.modify-next")] += 1
        return True

    def _song_of_power_near(self, p: Player) -> Ench | None:
        """A friendly singer of Song of Power (not p; ruling song-of-power#1) within 20', judged with
        the same range probability as a 20' ability."""
        for q in self.allies(p):
            if q is p or not q.alive or not q.on_field(self.t):
                continue
            song = next((e for e in q.enchantments if e.ability.effects_of("ability.charge-faster")), None)
            if song is not None:
                return song if self.rng.random() < self.rules.a("range.p_in_range")["20'"] else None
        return None

    def _begin_incantation(self, p: Player) -> None:
        """Starting an Incantation ends effects that say so (Rage)."""
        if p.buffs:
            p.buffs = [b for b in p.buffs if not b.ends_on_incantation]

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
        target = self.players[c.target] if c.target is not None else p
        if not self.can_cast_at(p, target, uses):
            # restricted since the incantation began (e.g. Insulted mid-cast): the player stops short
            self.fails[(ab.slug, "restricted")] += 1
            return
        uses.spend()
        if uses.ench is not None:
            # a strip is removed for the cast (the Enchantment's on-strip effect; one if none is recorded)
            ench = uses.ench
            if uses.ench.strips is None:
                uses.ench.strips = 1
            if not self.apply_effects(ench.ability, ("on-strip",), Ctx(ench.ability, p, p, bearer=p, ench=ench)):
                ench.strips -= 1
                if ench.strips <= 0:
                    self.remove_enchantment(p, ench)
        self.casts[ab.slug] += 1
        if ab.delivery in ("magic-ball", "specialty-arrow"):
            self._projectile(p, uses, target)
            return
        why = self.check_requirements(ab, p, target, start=False, uses=uses) or self.blocked(uses, p, target)
        if why:
            self.fails[(ab.slug, why)] += 1
            return
        if uses.magical and target is not p:
            self._provoke(p, target, "cast-done")
        if ab.delivery == "enchantment":
            if not target.alive and "active-while-dead" not in ab.properties:
                self.fails[(ab.slug, "target-dead")] += 1
                return
            self.attach_enchantment(target, uses, p, persistent=c.persistent)
            return
        if ab.slug == "mend" and target.wounds:
            golem = self.modifier(target, "Mend can remove a wound from the bearer")
            if golem is not None:
                # Golem: Mend removes one wound from the bearer, in place of a repair (ruling golem#1)
                target.wounds.discard(sorted(target.wounds)[0])
                self.applied[(golem.slug, "ability.modify")] += 1
                self.applied[(golem.slug, "wound.heal")] += 1
                return
        done = self.apply_effects(ab, ("on-cast",), Ctx(ab, p, target, bearer=p))
        if ab.slug == "mend" and "equipment.repair" in done:
            art = self.modifier(p, "does not consume a use of Mend")
            if art is not None:
                # Artificer: mending a weapon or shield gives the use back (one had to remain to cast)
                uses.restore(1)
                self.applied[(art.slug, "ability.modify")] += 1

    def _projectile(self, p: Player, uses: Uses, target: Player) -> None:
        ab = uses.ability
        if uses.unit and uses.left == 0 and uses.max:
            u = uses

            def retrieve(u=u, p=p):
                u.left = u.max
                p.barrage = None      # picking up any Magic Ball ends Elemental Barrage (elemental-barrage#1)
            self.at(self.t + self.rules.a("projectiles.magic_ball_retrieve_seconds"), retrieve)
        key = "projectiles.magic_ball_p_hit" if ab.delivery == "magic-ball" else "projectiles.arrow_p_hit"
        if ab.delivery == "specialty-arrow":
            self._provoke(p, target, "attack")
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
        if kind == "ball" and uses.magical:
            self._provoke(p, target, "cast-done")
        ctx = Ctx(ab, p, target, location=self._location(), specials=specials)
        if kind == "arrow" and "engulfing" in ab.properties:
            # Protection from Projectiles / Song of Deflection: Engulfing effects from projectiles other
            # than Magic Balls (e.g. Pinning Arrow) do not affect the bearer, whatever they strike
            guard = next((e for e in target.enchantments if any(
                x.kind == "defense.negate-engulfing" and x.subject == "bearer" for x in e.ability.effects)), None)
            if guard is not None:
                self.applied[(guard.ability.slug, "defense.negate-engulfing")] += 1
                self.fails[(ab.slug, "unaffected")] += 1
                return
        if kind == "arrow" and self.unaffected(target, "projectiles-except-magic-balls"):
            self.fails[(ab.slug, "unaffected")] += 1
            return
        self.apply_effects(ab, ("on-struck", "on-cast"), ctx)

    def shoot(self, p: Player, target: Player) -> None:
        """A normal arrow: Armor Breaking and Weapon Destroying (rules/weapon-types-shields-equipment.md)."""
        p.next_shot_at = self.t + self.rules.a("projectiles.arrow_shot_seconds")
        if not self.can_fire_normal_arrows(p) or not self.can_attack(p, target) or not self.weapon_usable(p):
            # the shooter looks for a shot and holds it (Sniper, Gift of Air, Awe/Terror/Insult)
            self.fails[("arrow", "restricted")] += 1
            return
        self._provoke(p, target, "attack")
        if self.targetable(target) and self.rng.random() < self.rules.a("projectiles.arrow_p_hit"):
            self.hit(target, p, "arrow", specials=frozenset({"armor-breaking"}), kind="arrow")

    def apply_effects(self, ab: Ability, timings: tuple[str, ...], ctx: Ctx) -> list[str]:
        """Run ab's handled effects with these timings; returns the kinds that took effect.
        A Verbal with a choice (Mend, Release, Steal Life Essence) applies only the first effect
        that works within each polarity group: e.g. Mend repairs a weapon, else a point of armor.
        action.restrict effects are never alternatives: Insult's has-choice is the target's choice
        (E2), and its two restrictions are parts of one effect."""
        choice = "has-choice" in ab.properties and ab.delivery == "verbal"
        chosen: set[str] = set()
        done: list[str] = []
        for eff in ab.effects:
            if choice and eff.polarity in chosen and eff.kind != "action.restrict":
                continue
            if eff.timing not in timings:
                if eff.timing == "after-delay" and "on-cast" in timings and fx.is_handled(ab, eff) \
                        and ab.slug in fx.AFTER_DELAY_SECONDS:
                    self._after_delay(ab, eff, ctx)
                    continue
                if eff.timing == "while-active" and ab.delivery not in fx.PASSIVE_DELIVERIES and "on-cast" in timings:
                    # a Verbal's ongoing effect: registered at cast when handled (Circle of Protection)
                    if fx.is_handled(ab, eff) and eff.kind in fx.INSTANT:
                        if fx.INSTANT[eff.kind](self, eff, ctx):
                            self.applied[(ab.slug, eff.kind)] += 1
                            done.append(eff.kind)
                    else:
                        self.noops[(ab.slug, fx.runtime_noop_detail(ab, eff))] += 1
                continue
            if not fx.is_handled(ab, eff):
                self.noops[(ab.slug, fx.runtime_noop_detail(ab, eff))] += 1
                continue
            if fx.INSTANT[eff.kind](self, eff, ctx):
                self.applied[(ab.slug, eff.kind)] += 1
                done.append(eff.kind)
                if choice:
                    chosen.add(eff.polarity)
        return done

    def _after_delay(self, ab: Ability, eff, ctx: Ctx) -> None:
        """Shake It Off: its effect happens a fixed time after casting, if the caster is still alive.
        Immunity only matters at the cast (N1); Cursed from an Enchantment stays (rule 7b)."""
        caster, life = ctx.caster, ctx.caster.deaths

        def fire() -> None:
            if caster.alive and caster.deaths == life and fx.INSTANT[eff.kind](self, eff, ctx):
                self.applied[(ab.slug, eff.kind)] += 1
        self.at(self.t + fx.AFTER_DELAY_SECONDS[ab.slug], fire)

    def enchantment_states(self, p: Player) -> set[str]:
        """States imparted by p's worn Enchantments and Traits, which cannot be removed while worn."""
        out = set()
        for ab, _ in self._passive_sources(p):
            for eff in ab.effects:
                if eff.kind == "state.apply" and eff.timing == "while-active" \
                        and eff.duration_type in fx.PASSIVE_STATE_DURATIONS:
                    out.add(eff.params.get("state", ""))
        return out

    # ------------------------------------------------------------------ the loop

    def _engage(self) -> None:
        t = self.t
        a = self.rules.a
        p_engage = a("engagement.p_engage_per_second")
        backline = a("engagement.backline_factor")
        caster_w = a("engagement.caster_weight_when_choosing_melee_target")
        p_dis = a("engagement.p_disengage_per_second")
        for p in self.players:
            if not p.can_act(t) or not p.on_field(t) or self.barred(p, "wield-weapons") or p.weapon_hot_until > t:
                p.target = None
                continue
            if p.target is not None:
                q = self.players[p.target]
                if not self.targetable(q) or not self.can_attack(p, q) or self.rng.random() < p_dis:
                    p.target = None
                continue
            if p.casting is not None or p.kept_away_until > t:
                continue
            attackers = [q for q in self.attackers_of(p) if self.targetable(q) and self.can_attack(p, q)]
            if attackers:
                p.target = self.rng.choice(attackers).pid
                continue
            if p.role != "fighter" and not (p.role == "archer" and not p.has_bow):
                continue
            if self.rng.random() >= p_engage:
                continue
            foes = [q for q in self.enemies(p) if self.targetable(q) and q.kept_away_until <= t
                    and self.can_attack(p, q)]
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
            if not self.weapon_usable(p) or ("right_arm" in p.wounds and "left_arm" in p.wounds):
                continue
            d = self.players[p.target]
            if (not self.targetable(d) and not d.has_state("stunned", t)) or not self.can_attack(p, d):
                p.target = None
                continue
            self._provoke(p, d, "attack")
            d_shield = self.shield_up(d)
            x = self._base_logit + k_skill * (p.skill - d.skill)
            x += shield_logit.get(d.shield, 0.0) if d_shield else 0.0
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
            poison = self._poison(p) if p.enchantments else None
            if poison is not None and not self.immune(d, poison.ability.school):
                specials = specials | {"wounds-kill"}
            if self.rng.random() < _logistic(x):
                if self.hit(d, p, "melee", specials=specials, kind="melee") and poison is not None:
                    # Poison is expended only when a wound is received (N1), even against a target
                    # Immune to Death (Enchantments rule 5)
                    self.applied[(poison.ability.slug, "special-effect.grant")] += 1
                    self.remove_enchantment(p, poison)
            elif "shield-crushing" in specials and d_shield \
                    and self.rng.random() < a("melee.p_shield_struck_on_miss"):
                guard = self.equipment_protection(d, "shield")
                if guard is not None:
                    self.applied[(guard.ability.slug, "equipment.protect")] += 1
                else:
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
            if p.restrictions:
                p.restrictions = [r for r in p.restrictions if r.until > t]
            if p.buffs:
                p.buffs = self._buffs(p)
            if not p.alive and not p.out:
                p.time_dead += self.dt
                if p.dead_until <= t and not self._respawn_prevented(p):
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
            if c.kind == "cast" and p.has_state("suppressed", t) and not c.declared \
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
            if p.alive and p.casting is None and p.can_act(self.t):
                if any(u.ability.slug == "extension" or (u.base_range and u.range != u.base_range)
                       for u in p.uses.values()):
                    self._offer_extension(p)
                decide(self, p)
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
