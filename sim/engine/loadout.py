"""Build a player's equipment and abilities from their class sheet and level."""
from __future__ import annotations

import heapq
import random
import re

from sim.engine.state import LOCATIONS, Player, Uses
from sim.policies.value import value
from sim.rules import frequency as freqmod
from sim.rules.compile import Ability, ClassAbility, ClassSheet, Rules

ROLE_BY_CLASS = {
    "Anti-Paladin": "fighter", "Assassin": "fighter", "Barbarian": "fighter", "Monk": "fighter",
    "Paladin": "fighter", "Scout": "fighter", "Warrior": "fighter",
    "Archer": "archer", "Bard": "caster", "Druid": "caster", "Wizard": "caster", "Healer": "support",
}
PASSIVE_DELIVERY = ("trait", "archetype")
_RANGE_KEYS = ("Unlimited", "50'", "20'", "Touch", "Other", "Self")


_PAREN_RANGE = re.compile(r"\s*\((Self|Touch|Other)\)")


def normalize_range(raw: str, ability: Ability) -> str:
    # a grant's frequency may start with its range, e.g. "(Self) 2/Refresh (m)"
    if raw and (m := _PAREN_RANGE.match(raw)):
        return m.group(1)
    for text in (raw, ability.range):
        for key in _RANGE_KEYS:
            if text and text.startswith(key):
                return key
    return "Self" if ability.delivery == "enchantment" else "20'"


def _uses(ability: Ability, freq: freqmod.Frequency, copies: int, magical_default: bool, rng_range: str) -> Uses:
    if freq.per in (None, "unlimited") and freq.unit is None:
        per, mx = ("unlimited" if freq.per == "unlimited" else None), None
    else:
        per, mx = (freq.per, (freq.uses or 1) * copies)
    magical = freq.magical if freq.magical is not None else magical_default
    return Uses(ability, per, mx, mx, freq.charge, freq.unit, magical, freq.ambulant, freq.swift,
                normalize_range(rng_range, ability))


def _add(p: Player, rules: Rules, slug: str, freq: freqmod.Frequency, copies: int, magical: bool, rng_range: str,
         trait: bool = False):
    ab = rules.abilities.get(slug)
    if ab is None:
        return
    if trait or ab.delivery in PASSIVE_DELIVERY or (ab.delivery == "" and not ab.words):
        if all(t.slug != slug for t in p.traits):
            p.traits.append(ab)
        return
    if slug in p.uses:
        u = p.uses[slug]
        extra = (freq.uses or 1) * copies
        if u.max is not None:
            u.max += extra
            u.left += extra
        if freq.charge and not u.charge:
            u.charge = freq.charge
        return
    p.uses[slug] = _uses(ab, freq, copies, magical, rng_range)


def _martial(p: Player, sheet: ClassSheet, rules: Rules, rng: random.Random):
    chosen: list[ClassAbility] = []
    groups: dict[tuple[str, int], list[ClassAbility]] = {}
    for ca in sheet.abilities:
        if ca.kind != "level":
            continue
        for lv in ca.levels:
            if lv > p.level:
                continue
            if ca.option:
                groups.setdefault((ca.option, lv), []).append(ca)
            else:
                chosen.append(ca)
    for (option, lv), cands in sorted(groups.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        k = 2 if option.lower().startswith("pick two") else 1
        cands = sorted(cands, key=lambda c: c.slug)
        chosen.extend(rng.sample(cands, min(k, len(cands))))
    for ca in chosen:
        _add(p, rules, ca.slug, ca.freq, 1, False, ca.range, ca.trait)
    if p.level >= 6:
        arch = sorted((c for c in sheet.abilities if c.kind == "archetype"), key=lambda c: c.slug)
        if arch and rng.random() < rules.a("loadout.archetype_share"):
            _add(p, rules, rng.choice(arch).slug, freqmod.parse(""), 1, False, "")


def _magic_user(p: Player, sheet: ClassSheet, rules: Rules, rng: random.Random, ablate: frozenset, ltp: bool):
    pools = {lv: 5 for lv in range(1, p.level + 1)}
    if ltp:
        pools[p.level] += 1
    cap = rules.a("loadout.magic_user_copy_cap")
    cands = [c for c in sheet.abilities if c.kind in ("spell", "archetype") and c.cost
             and min(c.levels) <= p.level and c.slug not in ablate]
    heap = []
    for c in cands:
        v = value(rules.abilities[c.slug], p.role) if c.slug in rules.abilities else 0.0
        if v > 0:
            # tiny seeded jitter breaks ties so equal-value spells vary between players
            heapq.heappush(heap, (-(v / c.cost) - rng.random() * 1e-3, c.slug, 0, c))
    bought: dict[str, int] = {}
    while heap:
        negv, slug, n, c = heapq.heappop(heap)
        limit = c.max if c.max is not None else cap
        if n >= limit:
            continue
        lv = min(c.levels)
        eligible = sorted(l for l in pools if l >= lv)
        if sum(pools[l] for l in eligible) < c.cost:
            continue
        due = c.cost
        for l in eligible:
            take = min(due, pools[l])
            pools[l] -= take
            due -= take
            if due == 0:
                break
        bought[slug] = n + 1
        heapq.heappush(heap, (negv * 0.6, slug, n + 1, c))
    for slug, n in bought.items():
        c = next(c for c in cands if c.slug == slug)
        _add(p, rules, slug, c.freq, n, True, c.range)


_SHIELD_ORDER = ("none", "small", "medium", "large")


def _apply_equipment_restrictions(p: Player) -> None:
    """Archetype/Trait drawbacks that forbid equipment (action.restrict): the player goes without it,
    or carries the largest shield still allowed."""
    for ab in p.traits:
        for eff in ab.effects:
            if eff.kind != "action.restrict" or eff.timing != "while-active":
                continue
            what = eff.params.get("what")
            if what == "wear-armor":
                p.armor_max = 0
            elif what == "wield-great-weapons":
                p.great_weapon = False
            elif what == "wield-shields":
                p.shield = "none"
            elif what == "wield-large-shields" and p.shield == "large":
                p.shield = "medium"
            elif what == "wield-bows":
                p.has_bow = False


def _apply_loadout_effects(p: Player, rules: Rules):
    # restrictions first, so a permit that depends on the equipment (Hunter: a Great weapon when no
    # shield is carried) sees the final kit, and again last so no permit re-grants forbidden gear
    _apply_equipment_restrictions(p)
    _apply_other_loadout_effects(p, rules)
    _apply_equipment_restrictions(p)


def _apply_other_loadout_effects(p: Player, rules: Rules):
    for ab in list(p.traits):
        for eff in ab.effects:
            if eff.timing != "while-active":
                continue
            kind, prm = eff.kind, eff.params
            if kind == "ability.grant" and prm.get("how") != "as-per":
                slug = rules.by_name.get(str(prm.get("ability", "")).lower())
                if slug:
                    f = freqmod.parse(prm.get("frequency", ""))
                    _add(p, rules, slug, f, 1, f.magical is True, prm.get("frequency", ""))
            elif kind == "ability.remove":
                slug = rules.by_name.get(str(prm.get("ability", "")).lower())
                p.uses.pop(slug, None)
                p.traits = [t for t in p.traits if t.slug != slug]
            elif kind == "ability.modify":
                slug = rules.by_name.get(str(prm.get("ability", "")).lower())
                change = str(prm.get("change", ""))
                if slug in p.uses and re.search(r"\bbecomes?\b.*\d+/(Life|Refresh)", change, re.I):
                    f = freqmod.parse(change)
                    u = p.uses[slug]
                    u.per, u.max, u.left, u.charge = f.per, f.uses, f.uses, f.charge or u.charge
            elif kind == "economy.frequency":
                slug = rules.by_name.get(str(prm.get("scope", "")).lower())
                u = p.uses.get(slug)
                change = str(prm.get("change", ""))
                if u is None:
                    continue
                if m := re.match(r"charge-x(\d+)", change):
                    u.charge = int(m.group(1))
                elif change == "double-uses" and u.max is not None:
                    u.max *= 2
                    u.left = u.max
                elif change == "unlimited":
                    u.max = u.left = None
                    u.per = "unlimited"
            elif kind == "equipment.permit":
                what = prm.get("what")
                order = _SHIELD_ORDER
                if what in ("small-shield", "medium-shield", "large-shield"):
                    size = what.split("-")[0]
                    if p.shield != "none" and order.index(size) > order.index(p.shield):
                        p.shield = size   # a player already carrying a shield carries the larger one
                elif what == "great-weapon" and p.shield == "none":
                    p.great_weapon = True
            elif kind == "armor.limit":
                pts = int(prm.get("points", 0))
                if prm.get("change") == "set":
                    p.armor_max = min(p.armor_max, pts) if p.armor_max else 0
                elif prm.get("change") == "increase":
                    p.armor_max += pts


def build_player(rules: Rules, pid: int, team: int, cls: str, level: int, skill: float,
                 rng: random.Random, ablate: frozenset = frozenset()) -> Player:
    """Deterministic for a given rng state. `ablate` removes abilities by slug: Martial classes
    make the same random choices and then lose the ability; Magic Users spend the points
    elsewhere (a real player would)."""
    sheet = rules.classes[cls]
    p = Player(pid=pid, team=team, cls=cls, level=level, skill=skill, role=ROLE_BY_CLASS[cls])
    # every draw below happens regardless of ablation so paired runs stay aligned
    wears_armor = rng.random() < rules.a("loadout.armor_worn_share")
    uses_shield = rng.random() < rules.a("melee.shield_use_share")
    great = rng.random() < rules.a("melee.great_weapon_share")
    ltp = rng.random() < rules.a("loadout.look_the_part_share")
    ltp_pick = rng.random()
    p.armor_max = sheet.armor if (sheet.armor and wears_armor) else 0
    p.shield = sheet.shield if (sheet.shield != "none" and uses_shield) else "none"
    p.great_weapon = sheet.all_melee and p.shield == "none" and great
    p.has_bow = p.role == "archer"
    if sheet.magic_user:
        _magic_user(p, sheet, rules, rng, ablate, ltp)
    else:
        _martial(p, sheet, rules, rng)
        opts = sheet.look_the_part.get("options") or []
        if ltp and opts:
            o = opts[int(ltp_pick * len(opts)) % len(opts)]
            _add(p, rules, o["slug"], freqmod.Frequency(**o["frequency"]), 1, False, "")
    p.traits = [t for t in p.traits if t.slug not in ablate]   # an ablated Archetype grants nothing
    _apply_loadout_effects(p, rules)
    for slug in ablate:
        p.uses.pop(slug, None)
    p.traits = [t for t in p.traits if t.slug not in ablate]
    p.armor = {l: p.armor_max for l in LOCATIONS}
    p.magic_armor = {l: 0 for l in LOCATIONS}
    return p
