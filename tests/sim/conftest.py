import copy
import json

import pytest

from sim.engine.game import Game
from sim.engine.state import Cast, Uses
from sim.paths import ASSUMPTIONS_JSON
from sim.rules.compile import build_rules, default_rules


@pytest.fixture(scope="session")
def rules():
    return default_rules()


@pytest.fixture(scope="session")
def sure_rules():
    """Rules where projectiles always hit and nothing is random about range or interrupts."""
    a = json.loads(ASSUMPTIONS_JSON.read_text())
    a = copy.deepcopy(a)
    a["projectiles"]["magic_ball_p_hit"]["value"] = 1.0
    a["projectiles"]["arrow_p_hit"]["value"] = 1.0
    a["casting"]["p_interrupt_on_armor_hit"]["value"] = 0.0
    return build_rules(assumptions=a)


def scenario(team0, team1, **kw):
    sc = {"game_type": "annihilation", "lives": 4, "respawn_seconds": 150, "refresh_seconds": None,
          "max_seconds": 1800, "teams": [team0, team1]}
    sc.update(kw)
    return sc


def spec(cls, level=1, skill=0.0):
    return {"cls": cls, "level": level, "skill": skill}


def make_game(rules, team0, team1, seed=1, **kw):
    g = Game(rules, scenario(team0, team1, **kw), seed)
    g.t = 100.0  # past pregame prep
    for p in g.players:
        p.at_base_until = 0.0
    return g


def resolve(g, caster, slug, target=None, magical=True, rng="20'"):
    """Complete a cast of `slug` by `caster` on `target` immediately, bypassing policy and time."""
    uses = Uses(g.rules.abilities[slug], None, None, None, None, None, magical, range=rng)
    caster.casting = Cast(uses, target.pid if target is not None else None, 0)
    g._complete(caster)
    return uses
