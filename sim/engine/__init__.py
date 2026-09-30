"""The Phase 1 game engine.

`ENGINE_VERSION` names the behavior of the engine and the policies as a whole. Bump it whenever a
change alters play (a rule handled differently, a policy choice, a new routine), not for
refactors or comments: the measured value calibration (`sim/data/value-calibration.json`) records
the version it was measured under, and `sim/policies/calibration.py` refuses a calibration made
under another version.
"""

ENGINE_VERSION = 2   # 2: wounded fighters step back to heal (policies._try_step_back_heal); value calibration
