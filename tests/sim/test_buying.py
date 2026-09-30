"""Magic User spell buying (sim/policies/buy.py): every modeled spell gets held, builds stay sane."""
import random

import pytest

from sim.engine.effects import is_handled
from sim.engine.game import Game
from sim.engine.loadout import build_player
from sim.policies.buy import effective
from sim.scenarios import generate, load_config

# Every purchasable, engine-modeled spell must be held by someone in at least this share of
# 1,000 mixed games, so that an ablation can measure it. Why 2%: the rarest spells belong to one
# class at 5th-6th level. A player like that is in only about 25-40% of mixed games and picks from
# ~30 spells, so a plausible buyer can't put them much higher without forcing weak spells into many
# builds. 2% is at least 20 holder games per 1,000 (100 in a 5,000-game ablation). Before the buyer
# had taste and favorites, 33 were never held.
#
# Archetypes are exempt: a Magic User's Archetype comes from their doctrine (sim/data/doctrines.json),
# and a martial player's is chosen by value (sim/policies/buy.py), so an Archetype whose restrictions
# cost more than they give in this model is rightly never taken by a martial player.
MIN_HELD_SHARE = 0.02
GAMES = 1000


def _purchasable_modeled(rules) -> set[str]:
    out = set()
    for sheet in rules.classes.values():
        if not sheet.magic_user:
            continue
        for c in sheet.abilities:
            ab = rules.abilities.get(c.slug)
            if c.kind == "spell" and c.cost and ab is not None \
                    and any(is_handled(ab, e) for e in ab.effects) and effective(ab, rules):
                out.add(c.slug)
    return out


@pytest.fixture(scope="module")
def held_share(rules):
    cfg = load_config("mixed")
    held: dict[str, int] = {}
    for seed in range(GAMES):
        g = Game(rules, generate(seed, cfg, rules), seed)   # rosters only; no play needed
        for slug, per_team in g.holdings().items():
            if sum(per_team):
                held[slug] = held.get(slug, 0) + 1
    return {s: n / GAMES for s, n in held.items()}


def test_every_modeled_purchasable_ability_is_held(rules, held_share):
    targets = _purchasable_modeled(rules)
    assert len(targets) > 80
    low = sorted((held_share.get(s, 0.0), s) for s in targets if held_share.get(s, 0.0) < MIN_HELD_SHARE)
    assert not low, f"held in < {MIN_HELD_SHARE:.0%} of {GAMES} mixed games: {low}"


def test_magic_user_archetypes_come_from_doctrines(rules, held_share):
    """Every Archetype a doctrine names is held, including Battlemage, which is bought for its plan
    (Ambulant on the run) although the engine models only its restriction."""
    assert not effective(rules.abilities["battlemage"], rules)
    for d in rules.doctrines.all():
        if d.archetype:
            assert held_share.get(d.archetype, 0.0) > 0.0, d.key


@pytest.mark.parametrize("arch,cls", [("warlock", "Wizard"), ("priest", "Healer"), ("summoner", "Druid")])
def test_builds_obey_archetype_purchase_rules(rules, arch, cls):
    """What the buyer buys under an Archetype obeys its restrictions and costs."""
    from sim.engine.loadout import _archetype_purchase_rules
    from sim.policies import buy
    cands = [c for c in rules.classes[cls].abilities if c.kind in ("spell", "archetype") and c.cost]
    entry = next(c for c in cands if c.slug == arch)
    cost, allowed = _archetype_purchase_rules(rules.abilities[arch], rules)
    spells = [c for c in cands if c.kind == "spell" and allowed(c) and effective(rules.abilities[c.slug], rules)]
    taste = {c.slug: 1.0 for c in cands}
    fav = {c.slug: i / len(cands) for i, c in enumerate(sorted(cands, key=lambda c: c.slug))}
    bought, _ = buy._build(entry, spells, cost, {lv: 5 for lv in range(1, 7)}, "caster", rules, taste, fav)
    assert bought.get(arch) == 1
    by_slug = {c.slug: c for c in cands}
    assert all(allowed(by_slug[s]) for s in bought if s != arch)
    assert sum(cost(by_slug[s]) * n for s, n in bought.items() if cost(by_slug[s]) > 0) <= 30
    if arch == "priest":
        assert bought.get("heal"), "Heal costs a Priest nothing"


def _builds(rules, cls, level, n=300):
    return [build_player(rules, 0, 0, cls, level, 0.0, random.Random(f"build:{cls}:{level}:{i}")) for i in range(n)]


@pytest.mark.parametrize("level", [1, 3, 6])
def test_core_spells_stay_near_universal(rules, level):
    """Taste varies the list but not the core: Healers take Heal (every Healer doctrine's first core
    spell), artillery and Evoker Wizards take Force Bolt."""
    healers = _builds(rules, "Healer", level)
    wizards = [p for p in _builds(rules, "Wizard", level) if p.doctrine in ("artillery", "evoker")]
    assert sum("heal" in p.uses for p in healers) / len(healers) >= 0.9
    assert wizards and sum("force-bolt" in p.uses for p in wizards) / len(wizards) >= 0.9


def test_builds_vary_and_respect_points(rules):
    builds = _builds(rules, "Druid", 6)
    assert len({tuple(sorted(p.uses)) for p in builds}) > len(builds) // 2
    for p in builds:
        archetypes = [t for t in p.traits if t.delivery == "archetype"]
        assert len(archetypes) <= 1


def test_bought_shield_is_carried(rules):
    for i in range(200):
        p = build_player(rules, 0, 0, "Healer", 3, 0.0, random.Random(f"shield:{i}"))
        slugs = {t.slug for t in p.traits}
        if "equipment-shield-medium" in slugs:
            assert p.shield == "medium"
        elif "equipment-shield-small" in slugs:
            assert p.shield == "small"
        else:
            assert p.shield == "none"
