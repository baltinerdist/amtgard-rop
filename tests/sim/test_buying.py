"""Magic User spell buying (sim/policies/buy.py): every modeled spell gets held, builds stay sane."""
import random

import pytest

from sim.engine.effects import is_handled
from sim.engine.game import Game
from sim.engine.loadout import build_player
from sim.policies.buy import effective
from sim.scenarios import generate, load_config

# Every purchasable, engine-modeled ability must be held by someone in at least this share of
# 1,000 mixed games, so that an ablation can measure it. Why 2%: the rarest abilities belong to
# one class at 5th-6th level. A player like that is in only about 25-40% of mixed games and picks
# from ~30 spells, so a plausible buyer can't put them much higher without forcing weak spells into
# many builds. 2% is at least 20 holder games per 1,000 (100 in a 5,000-game ablation). The rarest
# today is Essence Graft at 2.8%. Before the buyer had taste and favorites, 33 were never held.
MIN_HELD_SHARE = 0.02
GAMES = 1000


def _purchasable_modeled(rules) -> set[str]:
    out = set()
    for sheet in rules.classes.values():
        if not sheet.magic_user:
            continue
        for c in sheet.abilities:
            ab = rules.abilities.get(c.slug)
            if c.kind in ("spell", "archetype") and c.cost and ab is not None \
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
    assert len(targets) > 90
    low = sorted((held_share.get(s, 0.0), s) for s in targets if held_share.get(s, 0.0) < MIN_HELD_SHARE)
    assert not low, f"held in < {MIN_HELD_SHARE:.0%} of {GAMES} mixed games: {low}"


def test_inert_abilities_are_never_bought(rules, held_share):
    """Archetypes whose handled effects only touch abilities the engine can't use are skipped.
    Evoker (Elemental Barrage), Warlock (Death and Flame purchases doubled) and Legend (Extension)
    now change play and are no longer inert; Battlemage's only benefit is Ambulant (needs-map)."""
    for slug in ("battlemage",):
        assert not effective(rules.abilities[slug], rules)
        assert held_share.get(slug, 0.0) == 0.0


def _builds(rules, cls, level, n=300):
    return [build_player(rules, 0, 0, cls, level, 0.0, random.Random(f"build:{cls}:{level}:{i}")) for i in range(n)]


@pytest.mark.parametrize("level", [1, 3, 6])
def test_core_spells_stay_near_universal(rules, level):
    """Taste varies the list but not the core: Healers take Heal, Wizards take Force Bolt."""
    healers = _builds(rules, "Healer", level)
    wizards = _builds(rules, "Wizard", level)
    assert sum("heal" in p.uses for p in healers) / len(healers) >= 0.9
    assert sum("force-bolt" in p.uses for p in wizards) / len(wizards) >= 0.9


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
