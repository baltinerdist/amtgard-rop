# Phase 2: the field

Phase 1 has no map. Distance is a set of probabilities (`range.p_in_range`, `range.p_ally_nearby_for_touch`),
who fights whom is a per-second draw (`engagement.*`), casters are "backline" by a weight, and a
respawned player rejoins after a fixed `respawn.rejoin_seconds`. That is the largest source of error
left, measured, not guessed:

- **Fighter-stacked teams win 87–89%** against equal-skill mixed teams (the `class-stack` known limit):
  casters can't keep their distance, so whoever reaches them wins.
- **Stopped is worth almost nothing** (calibrated 0.4 against a kill at 10) and Heal about zero:
  most of their real value is movement (a Stopped player can't close or run; a leg wound can't chase).
- **23 effects are "needs-map"** (Teleport, Summon Dead, Ambulant, Blink's 10', Shove and Throw
  distances, Agoraphobia, Lost, Banish, alternate bases, Heart of the Swarm, respawn points...).
- **Calibration inherits all of it**: armor measured at 17.7 against a kill at 10 because melee decides
  nearly everything in Phase 1.

## Design

One engine, with a spatial layer behind a single interface, so Phase 1 stays available for comparison
(`--space off`) and every existing handler keeps working.

**Field.** A rectangle (default 60 m × 40 m, an assumption), bases at the two short ends. Positions
are continuous `(x, y)` in metres; 20' = 6.1 m, 50' = 15.2 m, Touch = within 1 m (the rule's six inches
plus arm's reach), melee reach by weapon (about 1.5 m, longer for Long and Great weapons). No
obstacles in stage 1.

**Time.** 0.5 s ticks when spatial (movement needs them; incantations already count in seconds).

**The `Space` interface** (`sim/engine/space.py`), which replaces every probability proxy:
`distance(p, q)`, `in_range(p, q, range)`, `within(p, metres, team)`, `can_reach(p, q)` (melee),
`nearest(p, candidates)`, `move_toward(p, point)`, `move_away(p, point)`, `step(p)`. A `NullSpace`
reproduces Phase 1 exactly (it draws the same probabilities), so `--space off` stays identical.

**Movement rules from the rulebook.** Walking and running speed (assumption); a leg wound (one leg:
may not walk, only move on knees or hop per `rules/combat-rules.md`; read it) slows to a crawl; Stopped
may not move their feet; Frozen, Stunned and Insubstantial as their States say. Incanting players
don't move their feet unless Ambulant. Chanting players may move. Players carried by forced
movement (Shove 20', Throw 50', Lost to base) move as the ability says.

**Engagement from geometry.** A fighter picks a target it can reach soonest (distance, attackers
already on it, caster priority), walks to it and fights when within reach. Gang-ups, flanking and a
battle line emerge instead of being drawn. Melee resolution itself (hit chance, locations, wounds)
is unchanged.

**Play styles become positions.** Fighters form and hold a line, then push. Strikers and controllers
keep a preferred distance behind the line inside their spell range (20' Verbals from about 5–6 m,
balls from farther). Medics move to the wounded behind the line. Enchanters work at base and just
behind the line. Archers keep range. Every caster retreats when a fighter closes. These are simple
steering rules with a few assumptions each, documented like the rest.

**Projectiles.** Magic Balls and arrows hit with a chance that falls with distance (an assumption
curve replacing `projectiles.*_p_hit`), can be thrown only within throwing range, and land where
they fall (retrieval walks there).

**Respawn.** A player respawns at base and walks back; `rejoin_seconds` goes away.

## Stages

1. **Geometry core.** `Space`, field, movement, geometric range, Touch and reach, engagement from
   proximity, movement States and leg wounds, respawn travel, the positional play styles. Every
   proxy routes through `Space`; `NullSpace` keeps Phase 1 bit-identical (a test proves it).
   Validity suite runs in both modes. Speed target: at least 10 games/s on 10 cores.
2. **Projectiles and forced movement, and the needs-map effects.** Distance-based ball and arrow
   hits, landing and retrieval; Shove, Throw, Lost, Banish, Agoraphobia, keep-away; Teleport,
   Summon Dead, Blink, Ambulant, alternate bases and respawn points, Heart of the Swarm, Sanctuary.
   COVERAGE.md's needs-map list goes to zero or to a stated reason.
3. **Validate, recalibrate, switch.** New face-validity checks (below), then bump `ENGINE_VERSION`,
   re-run the calibration under the spatial engine, make `--space on` the default, and re-run the
   doctrine table and the full cut analysis.

## What should change if the map works (new validity checks)

- `class-stack` falls well below 0.87 (a mixed team with casters behind a line holds).
- Stopped and Frozen gain calibrated value; Heal rises above zero.
- A caster dies less often per minute than a fighter in the same game.
- Respawning players take time to rejoin that grows with the field length.
- Shove and Throw break up gang-ups; Teleport and Summon Dead do something measurable.
- Small games stay skill-dominated; large games give area control more value.

## Assumptions to be added (all flagged, all overridable with `--assume`)

Field size, walking and running speed, crawl speed, melee reach by weapon, throw range and the hit
chance curve, preferred caster distance by play style, line spacing, retreat trigger distance.
