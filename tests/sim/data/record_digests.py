"""Record Phase 1 game digests (result + full event trace) for the NullSpace bit-identity test."""
import hashlib, json, sys, time
from sim.engine.game import Game
from sim.rules.compile import default_rules
from sim.scenarios import generate, load_config

def digest(rules, seed, cfg):
    g = Game(rules, generate(seed, cfg, rules), seed, trace=True)
    res = g.run()
    blob = json.dumps({"result": res, "trace": g.trace}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()

rules = default_rules()
cfg = load_config("mixed")
t0 = time.time()
out = {str(s): digest(rules, s, cfg) for s in range(30)}
print(time.time() - t0, file=sys.stderr)
json.dump(out, open(sys.argv[1], "w"), indent=1, sort_keys=True)
