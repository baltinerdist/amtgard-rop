"""Build a player's equipment and abilities from their class sheet and level."""
from __future__ import annotations

import heapq
import random
import re

from sim.engine import effects as fx
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
    u = Uses(ability, per, mx, mx, freq.charge, freq.unit, magical, freq.ambulant, freq.swift,
             normalize_range(rng_range, ability))
    u.copies = copies
    return u


def _add(p: Player, rules: Rules, slug: str, freq: freqmod.Frequency, copies: int, magical: bool, rng_range: str,
         trait: bool = False, purchased: bool = False):
    ab = rules.abilities.get(slug)
    if ab is None:
        return
    if trait or ab.delivery in PASSIVE_DELIVERY or (ab.delivery == "" and not ab.words):
        if all(t.slug != slug for t in p.traits):
            p.traits.append(ab)
        p.trait_copies[slug] = p.trait_copies.get(slug, 0) + copies
        return
    if slug in p.uses:
        u = p.uses[slug]
        extra = (freq.uses or 1) * copies
        if u.max is not None:
            u.max += extra
            u.left += extra
        if freq.charge and not u.charge:
            u.charge = freq.charge
        u.copies += copies
        u.purchased = u.purchased or purchased
        return
    p.uses[slug] = _uses(ab, freq, copies, magical, rng_range)
    p.uses[slug].purchased = purchased


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
    vals: dict[str, float] = {}
    jitter: dict[str, float] = {}
    for c in cands:
        v = value(rules.abilities[c.slug], p.role) if c.slug in rules.abilities else 0.0
        if v > 0:
            vals[c.slug] = v
            jitter[c.slug] = rng.random() * 1e-3   # tiny seeded jitter breaks ties between players
    bought = _buy(cands, vals, jitter, dict(pools), cap, lambda c: c.cost, lambda c: True)
    arch = next((s for s in bought if rules.abilities[s].delivery == "archetype"), None)
    if arch is not None:
        # A player has at most one Archetype, and its purchase rules (economy.purchase-restrict,
        # economy.cost) bind every other purchase: buy again with the Archetype bought first.
        ac = next(c for c in cands if c.slug == arch)
        cost, allowed = _archetype_purchase_rules(rules.abilities[arch], rules)
        pools2 = dict(pools)
        _pay(pools2, ac, ac.cost)
        rest = [c for c in cands if rules.abilities[c.slug].delivery != "archetype"]
        bought = {arch: 1, **_buy(rest, vals, jitter, pools2, cap, cost, allowed)}
    for slug, n in bought.items():
        c = next(c for c in cands if c.slug == slug)
        _add(p, rules, slug, c.freq, n, True, c.range, purchased=True)


def _pay(pools: dict[int, int], c: ClassAbility, cost: int) -> bool:
    eligible = sorted(l for l in pools if l >= min(c.levels))
    if sum(pools[l] for l in eligible) < cost:
        return False
    due = cost
    for l in eligible:
        if due == 0:
            break
        take = min(due, pools[l])
        pools[l] -= take
        due -= take
    return True


def _buy(cands: list[ClassAbility], vals: dict, jitter: dict, pools: dict, cap: int, cost, allowed) -> dict[str, int]:
    """Greedy purchase by value per point: best first, each further copy worth 0.6 of the last."""
    heap = []
    for c in cands:
        if c.slug in vals and allowed(c):
            heapq.heappush(heap, (-(vals[c.slug] / max(cost(c), 0.01)) - jitter[c.slug], c.slug, 0, c))
    bought: dict[str, int] = {}
    while heap:
        negv, slug, n, c = heapq.heappop(heap)
        limit = c.max if c.max is not None else cap
        if n >= limit or not _pay(pools, c, cost(c)):
            continue
        bought[slug] = n + 1
        heapq.heappush(heap, (negv * 0.6, slug, n + 1, c))
    return bought


def _archetype_purchase_rules(arch: Ability, rules: Rules):
    """(cost, allowed) functions over class-table entries for a Magic User's Archetype."""
    mults = []
    banned = []
    for eff in arch.effects:
        if not fx.loadout_handled(eff):
            continue
        if eff.kind == "economy.cost":
            mults.append((fx.COST_SCOPES[eff.params["scope"]], fx.COST_CHANGES[eff.params["change"]]))
        elif eff.kind == "economy.purchase-restrict":
            banned.append(fx.PURCHASE_RESTRICT[eff.params["scope"]])

    def cost(c: ClassAbility) -> int:
        ab = rules.abilities[c.slug]
        n = c.cost
        for applies, mult in mults:
            if applies(ab):
                n *= mult
        return n

    def allowed(c: ClassAbility) -> bool:
        ab = rules.abilities[c.slug]
        rng = normalize_range(c.range, ab)
        return not any(b(c, ab, rng) for b in banned)

    return cost, allowed


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


def _apply_loadout_effects(p: Player, rules: Rules, rng: random.Random | None = None,
                           sheet: ClassSheet | None = None):
    # restrictions first, so a permit that depends on the equipment (Hunter: a Great weapon when no
    # shield is carried) sees the final kit, and again last so no permit re-grants forbidden gear
    _apply_equipment_restrictions(p)
    _apply_other_loadout_effects(p, rules, rng or random.Random(f"loadout-effects:{p.pid}"), sheet)
    _apply_equipment_restrictions(p)


def _set_charge(u: Uses, change: str) -> bool:
    if m := re.fullmatch(r"charge-x(\d+)", change):
        u.charge = int(m.group(1))
        return True
    return False


def _double(u: Uses) -> None:
    if u.max is not None:
        u.max *= 2
        u.left = u.max


def _economy_frequency(p: Player, rules: Rules, rng: random.Random, sheet: ClassSheet | None, ab: Ability, prm: dict):
    scope, change = str(prm.get("scope", "")), str(prm.get("change", ""))
    if scope == "Archer Specialty Arrows" and change == "other":
        # Artificer: the Archer's class Specialty Arrows are replaced by the archetype's own
        # allotment (granted by its later effects); ruling artificer#1
        for slug in [s for s, u in p.uses.items() if u.ability.delivery == "specialty-arrow"]:
            del p.uses[slug]
        return
    if scope == "Brutal Strike" and change == "other":
        return    # Raider: the extra use in place of Look the Part, applied by its class.look-the-part record
    if scope == "Ancestral Armor" and change == "other":
        u = p.uses.get(rules.by_name.get("ancestral armor", ""))
        if u is not None:
            u.charge = None   # Marauder: no longer chargeable
        return
    if scope in fx.EXPERIENCED_SCOPES:
        return    # applied per purchase by _apply_experienced
    group = fx.FREQUENCY_GROUPS.get(scope)
    if group is not None:
        targets = [u for _, u in sorted(p.uses.items()) if group(u)]
    else:
        u = p.uses.get(rules.by_name.get(scope.lower(), ""))
        targets = [u] if u is not None else []
        if change == "double-uses" and any(
                e.kind == "ability.modify" and e.params.get("ability") == scope
                and (fx.modify_change(str(e.params.get("change", ""))) or "").startswith(("frequency", "arrows-"))
                for e in ab.effects):
            return   # the ability.modify twin states the resulting frequency ("becomes 2/Life ...")
    how = fx.FREQUENCY_SET.get(scope)
    for u in targets:
        if how == "per-purchase":
            u.per, u.max, u.left, u.unit = "life", u.copies, u.copies, None
        elif how == "one":
            u.per, u.max, u.left, u.unit = "life", 1, 1, None
        if _set_charge(u, change):
            continue
        if change == "double-uses":
            _double(u)
        elif change == "unlimited":
            u.max = u.left = None
            u.per = "unlimited"


def _ability_modify(p: Player, rules: Rules, ab: Ability, prm: dict) -> None:
    """An Archetype changing a named ability's frequency. Most are recorded twice (as ability.modify
    and economy.frequency, metadata convention 34); setting a Charge or a frequency is idempotent,
    and a doubling is applied once, by the economy.frequency twin when there is one."""
    name = str(prm.get("ability", ""))
    u = p.uses.get(rules.by_name.get(name.lower(), ""))
    change = str(prm.get("change", ""))
    how = fx.modify_change(change)
    if u is None or how is None:
        return
    if how == "frequency":
        f = freqmod.parse(change)
        u.per, u.max, u.left, u.charge = f.per, f.uses, f.uses, f.charge or u.charge
    elif how == "no-charge":
        u.charge = None
    elif how == "unlimited":
        u.max = u.left = None
        u.per = "unlimited"
    elif how.startswith("charge-x"):
        _set_charge(u, how)
    elif how.startswith("arrows-"):
        u.max = u.left = int(how.split("-")[1])
    elif how == "double-uses":
        twin = any(e.kind == "economy.frequency" and e.params.get("change") == "double-uses"
                   and str(e.params.get("scope", "")).startswith(name) for e in ab.effects)
        if not twin:
            _double(u)


def _range_change(p: Player, sheet: ClassSheet | None, prm: dict) -> None:
    """Avatar of Nature: the player's Enchantments of level 4 and below (except Golem) become range Self."""
    group = str(prm.get("group", ""))
    top = int(re.search(r"Enchantments of level (\d+)", group).group(1))
    exceptions = {s.strip().lower() for s in re.findall(r"except ([A-Z][A-Za-z' ]+)\)", group)}
    for slug, u in sorted(p.uses.items()):
        if u.ability.delivery != "enchantment" or u.ability.name.lower() in exceptions:
            continue
        levels = [min(c.levels) for c in sheet.abilities if c.slug == u.slug] if sheet else []
        if levels and min(levels) <= top:
            u.range = u.base_range = prm["to"]


def _replace(p: Player, rules: Rules, prm: dict) -> None:
    """Juggernaut: Harden is replaced by Greater Harden (Self) (ex) at the same frequency."""
    old = rules.by_name.get(str(prm.get("ability", "")).lower())
    new = rules.by_name.get(str(prm.get("with", "")).lower())
    u = p.uses.pop(old, None) if old else None
    if u is None or new is None:
        return
    note = str(prm.get("note", ""))
    u.ability = rules.abilities[new]
    if m := _PAREN_RANGE.search(note):
        u.range = m.group(1)
    if "(ex)" in note:
        u.magical = False
    p.uses[new] = u


def _look_the_part(p: Player, rules: Rules, prm: dict) -> None:
    """An Archetype changing the Look the Part bonus (Artificer: a fourth Pinning Arrow; Raider: an
    extra use of Brutal Strike; Sniper: Mend 1/Life (ex)). Only players who earned Look the Part
    (the loadout.look_the_part_share assumption) have a bonus to change."""
    if p.ltp is None:
        return
    slug, added, created = p.ltp
    u = p.uses.get(slug)
    if u is not None:              # take the class's Look the Part bonus back
        if created or u.max is None:
            del p.uses[slug]
        else:
            u.max -= added
            u.left = min(u.left, u.max)
    p.ltp = None
    target = rules.by_name.get(str(prm.get("ability", "")).lower())
    if prm.get("how") == "replaced-by":
        _add(p, rules, target, freqmod.parse("1/Life (ex)"), 1, False, "")
    elif target in p.uses and p.uses[target].max is not None:
        p.uses[target].max += 1
        p.uses[target].left += 1


def _experienced(p: Player, rng: random.Random, sheet: ClassSheet | None, per: str, change: str) -> bool:
    """One Experienced option: a random purchased Verbal of 4th level or lower with this period and
    no Charge yet becomes chargeable. False when no Verbal qualifies."""
    def level(u: Uses) -> int:
        if sheet is None:
            return 1
        return min((min(c.levels) for c in sheet.abilities if c.slug == u.slug), default=99)

    cands = [s for s, u in sorted(p.uses.items()) if u.purchased and u.ability.delivery == "verbal"
             and u.per == per and not u.charge and level(u) <= 4]
    if not cands:
        return False
    return _set_charge(p.uses[rng.choice(cands)], change)


def _apply_experienced(p: Player, rng: random.Random, sheet: ClassSheet | None, ab: Ability) -> None:
    """Experienced: each purchase applies to its own Verbal, chosen before the game, using either
    option (ruling experienced#1). The engine takes the per-life option (Charge x5) when a Verbal
    qualifies, else the per-refresh one (Charge x10); the Verbal is picked at random, like other
    chosen options."""
    options = [(fx.EXPERIENCED_SCOPES[str(e.params.get("scope"))], str(e.params.get("change")))
               for e in ab.effects if e.kind == "economy.frequency" and e.params.get("scope") in fx.EXPERIENCED_SCOPES]
    for _ in range(p.trait_copies.get(ab.slug, 1)):
        for per, change in options:
            if _experienced(p, rng, sheet, per, change):
                break


def _apply_other_loadout_effects(p: Player, rules: Rules, rng: random.Random, sheet: ClassSheet | None):
    for ab in list(p.traits):
        if ab.slug == "experienced":
            _apply_experienced(p, rng, sheet, ab)
            continue
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
                _ability_modify(p, rules, ab, prm)
            elif kind == "class.look-the-part" and fx.loadout_handled(eff):
                _look_the_part(p, rules, prm)
            elif kind == "ability.range-change" and fx.loadout_handled(eff):
                _range_change(p, sheet, prm)
            elif kind == "ability.replace" and fx.loadout_handled(eff):
                _replace(p, rules, prm)
            elif kind == "economy.frequency":
                if fx.loadout_handled(eff):
                    _economy_frequency(p, rules, rng, sheet, ab, prm)
            elif kind == "equipment.permit":
                what = prm.get("what")
                order = _SHIELD_ORDER
                if what in ("small-shield", "medium-shield", "large-shield"):
                    size = what.split("-")[0]
                    if p.shield != "none" and order.index(size) > order.index(p.shield):
                        p.shield = size   # a player already carrying a shield carries the larger one
                elif what == "great-weapon" and p.shield == "none":
                    p.great_weapon = True
                elif what == "bows":
                    p.has_bow = True      # Ranger (Game.shoot allows it; see README on policies)
                elif what == "any-number-of-specialty-arrows":
                    for u in p.uses.values():
                        if u.ability.delivery == "specialty-arrow":
                            u.unit = None     # Sniper: carries enough arrows never to retrieve them
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
            f = freqmod.Frequency(**o["frequency"])
            created = o["slug"] not in p.uses
            _add(p, rules, o["slug"], f, 1, False, "")
            p.ltp = (o["slug"], f.uses or 1, created)
    p.traits = [t for t in p.traits if t.slug not in ablate]   # an ablated Archetype grants nothing
    _apply_loadout_effects(p, rules, rng, sheet)
    for slug in ablate:
        p.uses.pop(slug, None)
    p.traits = [t for t in p.traits if t.slug not in ablate]
    p.armor = {l: p.armor_max for l in LOCATIONS}
    p.magic_armor = {l: 0 for l in LOCATIONS}
    return p
