"""Record Phase 1 game digests (result + full event trace) for the NullSpace bit-identity test.

    PYTHONPATH=. .venv/bin/python tests/sim/data/record_digests.py tests/sim/data/phase1_digests.json

phase1_digests.json was recorded at 7294de4, before the spatial layer (sim/engine/space.py).
Re-record it only for a deliberate change to Phase 1 play, and say so in the commit.
"""
import hashlib
import json
import sys
import time

SEEDS = range(30)


def digest(rules, seed: int, cfg: dict, space: str | None = None) -> str:
    """sha256 of a game's result and its full event trace."""
    from sim.engine.game import Game
    from sim.scenarios import generate
    kw = {} if space is None else {"space": space}
    g = Game(rules, generate(seed, cfg, rules), seed, trace=True, **kw)
    res = g.run()
    blob = json.dumps({"result": res, "trace": g.trace}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()


def main(path: str) -> None:
    from sim.rules.compile import default_rules
    from sim.scenarios import load_config
    rules = default_rules()
    cfg = load_config("mixed")
    t0 = time.time()
    out = {str(s): digest(rules, s, cfg) for s in SEEDS}
    print(f"{time.time() - t0:.1f} s", file=sys.stderr)
    json.dump(out, open(path, "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main(sys.argv[1])
