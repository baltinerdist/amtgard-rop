# Ability Metadata Platform — plan

## Goal

A complete, queryable description of every ability, spell, trait and archetype in the V8.08 Rules of Play, detailed enough to
answer questions such as *"every ability that causes death"*, *"every ability that holds a player in place"*, *"which Druid spells
duplicate another spell, trait or ability"*, or *"what changes if this moves from 4th to 6th level"*, and to support trimming and
simplifying the rulebook.

Source of truth is the markdown in `rules/` (the PDF is only a confirmation reference). Scope: the 179 entries in
`rules/magic-and-abilities/` (abilities, spells, traits, archetypes, meta-magic, equipment traits) plus the four class immunity
traits (Immune to Command, Death, Flame, Subdual). Magic Items and Quest Abilities are out of scope.

## What was wrong with the first attempt (`tags/`)

1. **Thin.** One flat list of effect records per ability. 238 of the 527 rule-text sentences were not tied to any record, so
   durations, limitations, ending conditions, drawbacks, requirements and rule clarifications were simply lost.
2. **Not in the reader's words.** Effects were stored as `kill:other`; nobody searches for that. "Causes death" must be a first-class,
   visible attribute, with synonyms (kill, die, slay, lethal).
3. **No rules semantics.** "Freezes a person in place" depends on what Frozen, Stopped and Stunned *mean*. States, Special Effects and
   mechanics were never encoded, so every derived answer was ad hoc.
4. **Missing dimensions:** how it is cast (delivery, incantation, triggers, moving, chanting), what it requires (willing, dead, wounded,
   distance from enemies), how long it lasts, what ends it, what it bypasses (armor, enchantments, immunities), what counters it,
   enchantment-limit rules, who benefits, drawbacks on the bearer, choices, per-class economics (frequency, charges, cost).
5. **No completeness guarantee.** Nothing forced every sentence of the rules to be accounted for.

## Design principles

* **Every sentence accounted for.** Rule text is split into numbered sentences (`E1`, `E2`, `L1`, `N1`). Every metadata fact cites the
  sentence IDs it comes from, and the validator fails any ability with an uncited sentence. A sentence that adds no new fact (a
  reminder or clarification) is still recorded as a `clarification`, so nothing is silently dropped.
* **Plain language on top, precision underneath.** Each effect has a *kind* with a human label ("Causes death", "Freezes",
  "Pushes away") and synonyms, plus structured parameters (seconds, feet, points, scope, who, conditions).
* **Rules semantics encoded once.** States, Special Effects and core mechanics are a glossary with machine-readable consequences
  (Frozen: cannot move, speak or act; only State-general abilities affect them). Derived answers ("immobilizes", "silences",
  "removes from play") come from the glossary, consistently.
* **Deterministic where possible.** Identity, class availability, frequency/charges/cost, incantation and materials are parsed by code
  from the markdown. Agents only do what needs reading comprehension.
* **Reviewed in layers.** Pilot, then sharded extraction, then independent correction with a different sharding, then per-topic
  consistency review across the whole corpus, then question-based acceptance tests answered independently from the rule text.

## Data model (one JSON file per ability in `metadata/source/records/`)

| Facet | Contents | Filled by |
| --- | --- | --- |
| identity | name, type, school, range (and per-class range), magical/extraordinary per class | code |
| availability | classes, levels, cost, max, frequency parsed (uses, per life/refresh/unlimited, charge xN, balls/arrows), Look The Part, pick-one groups | code |
| casting | incantation text, repetitions, words; materials (strip / cover colors); delivery (verbal, enchantment, magic ball, specialty arrow, trait, meta-magic, archetype) | code |
| sentences | numbered rule sentences (Effect, Limitations, Note) | code |
| **effects** | kind (controlled vocabulary with plain labels), subject (caster, bearer, target, struck player, dead player, allies, equipment, hit location), polarity for the subject (benefit, harm, neutral: drawbacks are harms to the bearer), parameters, duration (instant, timed, while worn, while chanting, until used, until arrival, indefinite, permanent), timing (on cast, while worn, on a trigger, after a delay), conditions, choice groups, evidence | agents |
| requirements | what must be true to cast or for it to work (target willing / dead / wounded / Stopped / Frozen / Insubstantial / not Cursed / not moved 5'; no enemy within 10' or 20'; only after a kill; caster not Cursed or Stopped) | agents |
| restrictions | limits on use or combination (not with other Protection Enchantments, not with Attuned, one active per caster, max per caster, class or purchase limits) | agents |
| termination | what ends an ongoing effect (exit at will, arrival, caster attacks the target, caster dies, another Forced Movement, becoming Frozen or Insubstantial, moving from the start, beginning an incantation, last strip, failing to chant) | agents |
| properties | Forced Movement, Engulfing, Chant, Kill/Wound Trigger, castable while moving, works while Suppressed, no verbal targeting, persistent, exempt from the Enchantment limit, bypasses (armor, enchantments, immunities, traits, resistances, Cursed) | agents |
| references | other abilities (grants, casts via strips, as per, modifies, removes, excludes, mentions), States, Special Effects, mechanics | agents (with code hints) |
| clarifications | sentences that explain an interaction rather than add an effect | agents |
| roles, beneficiary | offense, control, debuff, defense, healing, revival, mobility, anti-magic, equipment, resource, team, utility; self / ally / enemy / any | agents |
| counters | which classes' immunities stop it, Enlightened Soul, Protection from Magic / Projectiles, Missile Block, Cursed (Spirit), Sleight of Mind, Magic Armor rule 8, Frozen / Insubstantial / Invulnerable targets | code (from glossary + interoperability model) |
| summary | one plain sentence with the numbers | agents |

## Phases

| # | Phase | Who | Output |
| --- | --- | --- | --- |
| 0 | Foundation: vocabulary with labels and definitions, glossary of States / Special Effects / mechanics, sentence segmentation, deterministic facets, input packets, validator (schema, evidence, 100% sentence coverage, heuristics) | me | `scripts/meta_*.py`, `metadata/glossary/` |
| 1 | Pilot on ~16 deliberately hard, varied entries; review; adjust vocabulary before scaling | 1 agent + me | vocabulary v1 frozen |
| 2 | Extraction, sharded by type so similar entries are done together (10 shards) | 10 agents | `metadata/source/records/*.json`, validator clean |
| 3 | Independent review and correction, sharded alphabetically (different eyes on every entry) | 10 agents | corrected records + change log |
| 4 | Consistency review per topic across all entries (life and death; States, control and movement; equipment, armor and Special Effects; defense and protection; magic, enchantments and resources; casting, requirements, duration and termination) | 6 agents | patch sets, applied and re-validated |
| 5 | Build: database, per-ability profiles, indexes, glossary pages, similarity and per-class duplicate reports, query tool, explorer | me | `metadata/`, `scripts/meta_query.py`, explorer artifact |
| 6 | Acceptance: agents answer ~40 real questions from the rule text alone; answers compared with the platform; misses fixed | 4 agents + me | `metadata/ACCEPTANCE.md` |
| 7 | Report back | me | |

The first attempt's `tags/` layer has been removed; `metadata/` replaces it.
