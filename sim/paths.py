"""Filesystem locations used across the simulator."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SIM = REPO / "sim"
DATA = SIM / "data"
OUT = SIM / "out"

ABILITIES_JSON = REPO / "metadata" / "abilities.json"
CLASSES_DIR = REPO / "rules" / "classes"
CLASSES_JSON = DATA / "classes.json"
RULINGS_JSON = DATA / "rulings.json"
ASSUMPTIONS_JSON = DATA / "assumptions.json"
