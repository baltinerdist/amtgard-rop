# V8.7 "Soupy" → V8.08 "Spongy": what changed in this repo

The corpus was rebuilt from the official V8.08 rulebook PDF (July 25, 2026), not from the
condensed "New Rules Guide". The guide lists the headline changes; the rulebook contains more
(wording rewrites, moved text, new tables), and the PDF is authoritative. Every change below was
applied verbatim from the PDF and re-verified with `scripts/verify_abilities.py`,
`scripts/verify_prose.py` and `scripts/lint_corpus.py`.

## Structure
- **Abilities: 180 → 179 files.** Removed: Ward Self. Renamed (old file replaced by new):
  Imbue Armor → **Harden Armor**, Imbue Shield → **Imbue**, Imbue Weapon → **Toxic Blades**,
  Extend Immunities → **Protection from Evil**. No abilities were added.
- **Printed page numbers moved by one** (printed = PDF page − 2; it was − 3). All frontmatter and
  source notes were updated.
- **Change Log removed from the rulebook.** The V8.7 log is kept in `archive/v8.7-change-log.md`;
  the policies file now holds only the Youth, Whistleblower and Inclusion policies.
- **Quests** are still part of Battlegames; **"Weapon Types, Shields, and Equipment"** was dropped from the
  table of contents but its content is unchanged in scope, so the file split is kept.
- **Declarations** (new material and a "Declarations Made Easy" box) added to `special-effects.md`.

## Gameplay and definitions
- Casting Abilities: new section in *Magic, Abilities, States, and Special Effects*; Ability, Charge,
  Enchantments, Forced Movement, Incantation, Range, Specialty Arrows, Traits and Verbal reworded; new
  entries Alternate Base, Empty Hand and Ongoing Effects.
- Combat Rules: *Inflicting Wounds* → *Valid Strikes*; *Combat Notes* dissolved into Death and a new
  *Using Equipment* section; hobbling and Shot in Motion reworded.
- Armor: helm bonus rewritten (Light +1 torso, Heavy +1 all locations, up to class max); construction and
  material notes updated.
- Weapons: Flex Rule, Ring Rule and Material Suitability; Hinged, Madu and Javelin rewritten; Strips
  rewritten; Arrows is now a top-level section.
- States: Stunned rewritten, Invulnerable cannot act as an alternate base; Special Effects reworded.
- Classes overview: Credits and Levels rewritten (16 bonus credits/month, up to 3 credits without attendance);
  Color class entry added.
- Magic Items: restructured (Trinkets / Talismans / Artifacts, new per-player limits); Homestone and
  several items no longer say "Does not count as an Enchantment".
- Rules Revision Process: rewritten as a two-year Submission / Confirmation cycle.
- Appendix A (Warrior ladder wording) and Appendix B (Kingdom/Seat table now included).

## Class and ability changes (highlights)
Archer: 2 Suppression + 2 Phase Arrows. Monk: Banish (m), Innate 2/Life, Mystic Phase Bolt, Sanctuary
rules. Paladin: Protection from Evil. Scout: Evolution at 1st, Heal/Release extra at 5th, Heal Charge x5.
Warrior: Shake It Off 1/Life, Juggernaut grants Harden Armor. Wizard: Ward Self → Blessing Against Harm,
purchase limits on Icy Blast/Shatter. Healer: Blessing Against Harm / Blessed Aura 1/Life max 2,
Necromancer cost 2. Druid: Avatar of Nature cost 2. Plus wording changes in ~100 ability files
(see `git diff -- rules/magic-and-abilities`).

## Known source inconsistencies (kept faithfully)
- Scout table places Evolution at 1st and Pinning Arrow at 4th; their ability blocks still say `Sc 4` / `Sc 5`.
- Wizard table prints Fireball's type as "Magic-Ball".
