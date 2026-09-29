---
title: "States, Special Effects and mechanics"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# States, Special Effects and mechanics

The rules semantics the platform uses to derive answers. Source: `rules/magic-states-effects/`.

## States

| State | Summary | Moves? | Speaks? | Casts? | Attacks? | Unaffected by most? |
| --- | --- | --- | --- | --- | --- | --- |
| Cursed | Immune to Spirit; persists after death, removed on respawn. | yes | yes | yes | yes | no |
| Fragile | Dies on the next wound. | yes | yes | yes | yes | no |
| Frozen | May not move, speak or take any action; unaffected by combat and abilities except those that work on States in general or on Frozen. | no | no | no | no | yes |
| Insubstantial | Cannot interact with players, items or objectives; may not move from the starting location unless the ability allows; unaffected by combat and abilities except those that work on States in general or on Insubstantial; may use Meta-Magic and Charge; may exit by incanting if they caused it. | unless the ability says otherwise | yes | may only target themselves with abilities that affect Insubstantial players; may use Meta-Magic and Charge | no | yes |
| Invulnerable | Unaffected by combat and abilities that do not specifically work on Invulnerable players; cannot interact; cannot be an alternate base or respawn. | yes | yes | only abilities that specifically allow it | no | yes |
| Stopped | May not move their feet; Forced Movement cast on them fails. | no | yes | yes | yes | no |
| Stunned | May not move, speak or take any action voluntarily; may still be forced to move to a specific destination (Shove, Banish). | voluntarily | no | no | no | no |
| Suppressed | Unable to cast abilities or use the Charge incantation; does not stop abilities already cast, Chants in progress or Enchantments activating. | yes | yes | no | yes | no |

General rules: A player can have any number of different States at once. States conferred by a class Trait are always on and cannot be removed by respawn, death or any other means. Gaining a State already held only extends it if the new duration is longer. Unless otherwise noted, States cannot apply to dead players and are removed when a player dies or avoids death through Troll Blood, Phoenix Tears or Song of Survival. When a State that prevented movement expires, the player declares 'No longer [State]' audibly to 20'.

## Derived capabilities

- **causes-death** — Causes death: an effect Causes death
- **can-be-lethal** — Can kill (directly or by making wounds lethal): Causes death, Wounds Kill or Siege, or makes another player Fragile
- **holds-in-place** — Holds a player in place: puts Frozen, Stopped or Stunned on another player, or forbids them to move from where they are
- **neutralizes** — Takes a player out of the fight: puts Frozen, Stunned, Insubstantial or Invulnerable on another player
- **silences** — Stops a player casting: puts a State that prevents casting (Frozen, Stunned, Suppressed) on another player
- **removes-from-play** — Removes a player from play for a time: puts Frozen, Insubstantial or Invulnerable on another player
- **makes-insubstantial** — Makes a player Insubstantial: puts Insubstantial on anyone, the user included
- **self-protection-state** — Makes the user Insubstantial or Invulnerable: puts Insubstantial or Invulnerable on the user or bearer
- **curses** — Curses another player: puts Cursed on another player (a Cursed drawback on the user shows under 'Applies State to own side')
- **wounds** — Wounds: inflicts a wound
- **heals** — Heals wounds: heals wounds
- **revives** — Returns the dead to life: returns a dead player to life
- **survives-death** — Survives death: prevents death
- **repairs** — Repairs equipment or armor: repairs equipment or armor
- **dispels** — Removes Enchantments from others: removes Enchantments from another player
- **cleanses** — Removes States or effects: removes or takes on States or Ongoing Effects
- **protects** — Protects: immunity, resistance, 'unaffected by', negating hits or Engulfing, blocking projectiles, Magic Armor, protecting armor, equipment or Enchantments, or preventing States
- **resists** — Makes Resistant: gives Resistance (to wounds, the next source, or a chosen School)
- **moves-others** — Moves other players: any movement effect on another player
- **moves-ally** — Moves an ally: a movement effect on another player that is good for them (Teleport, Summon Dead)
- **moves-self** — Moves the user or bearer: any movement effect on the user or bearer
- **restricts-others** — Restricts what others may do: limits the actions of another player
- **attacks-equipment** — Destroys or disables weapons or shields: destroys or disables equipment, or gives Weapon Destroying, Shield Destroying or Shield Crushing
- **defeats-armor** — Breaks, destroys or ignores armor: Armor Breaking or Armor Destroying, removes armor points, weapons that ignore (Magic) Armor, or the property 'ignores armor' / 'ignores Magic Armor'
- **more-uses** — More uses, charges or slots: instant Charge, restored uses, faster Charging, changed frequency, or extra Enchantment slots
- **changes-frequency** — Changes the frequency or Charge of abilities: changes the uses, frequency or Charge of a group of abilities, or speeds up Charging
- **extra-enchantments** — Extra Enchantments: an extra Enchantment slot, or exempt from the Enchantment limit
- **team-base** — Respawn point or Alternate Base: acts as a respawn point or Alternate Base
- **grants-abilities** — Grants other abilities: grants an ability, works 'as per' one, casts one from strips, or changes Look The Part to one (an extra use of an ability the class already has is recorded but gives nothing new)
- **castable-while-moving** — Can be used while moving: the property, Ambulant on a class listing, the Ambulant Meta-Magic, or a Specialty Arrow; through a grant when the granted ability is taken (Ambulant)
- **has-drawback** — Has a drawback for its user: something bad for the user's own side: a harmful effect on the user, bearer or their group, on the ally it is cast on, a limiting restriction (no other Protection Enchantments, other sources may not be used ...), or a drawback of an ability it works 'as per'

## Special Effects

- **Armor Breaking**: An armor location with 3 or fewer points drops to 0; otherwise a normal hit.
- **Armor Destroying**: The armor location drops to 0 points.
- **Phasing**: Hits and their Special Effects ignore ongoing abilities and Traits (not States).
- **Shield Crushing**: The shield is damaged; three cumulative damages destroy it.
- **Shield Destroying**: The shield is destroyed.
- **Siege**: A strike kills the player and destroys all their carried equipment.
- **Weapon Destroying**: The weapon is destroyed.
- **Wounds Kill**: A player wounded by it dies. Always Death School.

## Mechanics

- **ability-order**: Traits, then Immunities, then Resistances, then other Enchantments; other Enchantments trigger at the same time.
- **alternate-base**: Can be used as a base only for Forced Movement to base, not for exiting Sanctuary or Reload or repairing; works while the player is Dead, Frozen or Insubstantial.
- **archetype**: Class options marked (A), always active, not Enchantments, cannot be removed.
- **chant**: Audible, at most 5 seconds apart, heard to 50'; stopping ends the effect; may be spoken while moving; one Chant at a time.
- **charge**: Regain a use with the Charge Incantation repeated N times, with an empty hand and feet still.
- **empty-hand**: Not touching a shield (except incidental small shield), a weapon other than an unbroken Magic Staff, arrows, or game objectives.
- **enchantments**: Ongoing abilities worn by players; one Magical Enchantment at a time; only on willing players; Immunities do not prevent them; inactive while dead; removed on respawn unless Persistent.
- **engulfing**: Affects the target if it strikes a valid hit location, garb or carried equipment.
- **forced-movement**: Fails if cast on a Stopped player; Enchantment-triggered movement is still allowed; the player may drag a wounded leg.
- **immune**: Unaffected by abilities of a School; does not protect equipment unless noted; does not remove existing effects.
- **incantation**: The spoken part of an ability; see Casting Abilities for requirements.
- **magic-armor**: Only the highest source counts; repairable; covers all locations; fails on players wearing armor; not enhanced by Ancestral or Harden Armor unless inherent.
- **magic-balls**: Must be held at the end of the incantation; one active at a time; Engulfing affects on any valid hit; not stopped by Protection from Projectiles or Song of Deflection.
- **meta-magic**: Stated before the modified ability's incantation; expended when stated; cannot modify Magic Items or abilities granted by Enchantments.
- **ongoing-effects**: Effects with a duration (definite or indefinite); removed when the player dies unless noted.
- **range**: Self; Other (another player at Touch); Touch (self or other, by contact or within six inches); 20'; 50'. Touch needs the target willing, dead, Stunned, Frozen or immobile Insubstantial.
- **resistant**: Unaffected by the next effect of a type: wounds, a School, or a whole source.
- **school**: Command, Death, Flame, Neutral, Protection, Sorcery, Spirit, Subdual.
- **specialty-arrows**: Fired alone; incanted immediately before firing; not interrupted by moving the feet; count as a normal arrow hit plus their effect.
- **traits**: Always on, cannot be removed, persist through death and respawn, do not count towards Enchantment limits.
- **trigger**: Kill Trigger: within 30 seconds of a killing blow, outside 10' of living enemies, one per kill. Wound Trigger: immediately after wounding an enemy.
- **verbal**: Abilities that need only an incantation.
- **persistent**: An Enchantment that returns with the bearer after respawning.
- **respawn**: Returning to play at a base after death (battlegame rules).
- **refresh**: When per-Refresh abilities are restored (battlegame rules).
- **base**: A team's base (battlegame rules).
- **look-the-part**: A game-by-game bonus ability for visually impressive garb (rules/classes/_overview.md).
- **enchantment-limit**: The number of Enchantments a player may wear (one Magical Enchantment unless another ability allows more).
- **declaration**: Something said aloud that is not an incantation (not stopped by Suppressed, may be said while moving).
- **strips**: Enchantment strips worn to show an Enchantment and track its uses.
- **armor**: Worn armor and its points (rules/armor.md).
- **shield**: Shields (rules/weapon-types-shields-equipment.md).
- **weapon**: Weapons (rules/weapons.md).
- **game-objectives**: Items and objectives in a battlegame.
- **reeve**: The game official.
