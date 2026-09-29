#!/usr/bin/env python3
"""Controlled vocabulary for the Ability Metadata Platform (metadata/).

Every term has a plain-language label (what people search for), a definition, and for effects the parameters it takes and search
synonyms. Agents write records using only these ids; scripts/meta_check.py enforces it. See metadata/PLAN.md and
metadata/AUTHORING.md.
"""

STATES = ["cursed", "fragile", "frozen", "insubstantial", "invulnerable", "stopped", "stunned", "suppressed"]
SCHOOLS = ["Command", "Death", "Flame", "Neutral", "Protection", "Sorcery", "Spirit", "Subdual"]
SPECIAL_EFFECTS = ["armor-breaking", "armor-destroying", "phasing", "shield-crushing", "shield-destroying", "siege",
                   "weapon-destroying", "wounds-kill"]

# ----------------------------------------------------------------------------------------------------------- effects
# kind -> label, family, definition, params {name: allowed values | "int" | "text" | "ability" | "abilities" | "states" | "schools"},
#          synonyms (extra search words)
E = {}


def eff(kind, label, family, definition, params=None, synonyms=()):
    E[kind] = dict(label=label, family=family, definition=definition, params=params or {}, synonyms=list(synonyms))


# life and death
eff("death.cause", "Causes death", "life-death", "The subject dies.", {}, ["kill", "kills", "die", "dies", "death", "slay", "lethal", "execute"])
eff("death.prevent", "Prevents death", "life-death",
    "When the subject would die they do not; the text says what happens instead (often Frozen or Insubstantial for a time).",
    {"instead": ["frozen", "insubstantial", "heal-and-frozen"]}, ["survive", "cheat death", "saving throw", "second life"])
eff("life.revive", "Returns to life", "life-death", "A dead subject is returned to life.", {}, ["resurrect", "raise", "revive", "bring back"])
eff("life.set-death-location", "Moves where the player died", "life-death", "The place the player counts as having died changes.", {},
    ["corpse", "death location"])
eff("life.prevent-respawn", "Prevents respawning", "life-death", "The subject cannot respawn.", {}, ["no respawn"])
eff("team.respawn-point", "Acts as a respawn point", "team", "Friendly players (or a named player) may respawn at the subject.",
    {"for": ["friendly-players", "bearer-only"]}, ["spawn", "respawn at"])
eff("team.alternate-base", "Acts as an Alternate Base", "team", "The subject may be treated as an Alternate Base (see the mechanic).",
    {"for": ["friendly-players", "bearer-only"]}, ["base", "alternate base"])

# wounds
eff("wound.inflict", "Inflicts a wound", "wounds", "A hit location of the subject is wounded.",
    {"location": ["struck", "chosen-by-caster"]}, ["wound", "maim", "injure", "damage"])
eff("wound.heal", "Heals wounds", "wounds", "Wounds on the subject are healed.", {"amount": ["one", "all"]}, ["heal", "cure", "mend wound"])

# states
eff("state.apply", "Applies a State", "states", "The subject gains a State. Use the 'state' parameter; the label becomes e.g. 'Freezes'.",
    {"state": STATES}, [])
eff("state.remove", "Removes States or Ongoing Effects", "states", "States and/or Ongoing Effects are removed from the subject.",
    {"what": ["specific-state", "one-state-or-effect", "all-states-and-effects", "chosen-states-and-effects", "same-source-states-and-effects"], "state": STATES,
     "except": "states"}, ["cleanse", "release", "free", "cure"])
eff("state.prevent", "Prevents States", "states", "The subject cannot receive the listed States.", {"states": "states"}, ["immune to state"])
eff("state.transfer", "Takes on a State", "states", "A State is moved from the target to the caster.", {}, ["swap", "absorb"])

# movement and position
eff("move.push", "Pushes away", "movement", "The subject is moved a distance in a straight line away from the caster.", {"feet": "int"},
    ["knockback", "shove", "throw", "push"])
eff("move.to-base", "Sends to base", "movement", "The subject must go directly to their base.", {}, ["banish", "send home", "exile"])
eff("move.to-location", "Moves to a chosen location", "movement", "The subject moves directly to a fixed location chosen by the caster.", {},
    ["teleport", "relocate"])
eff("move.to-caster", "Brings to the caster", "movement", "The subject must go directly to the caster.", {}, ["summon", "pull"])
eff("move.keep-away", "Must keep away", "movement", "The subject must stay at least a distance away from someone.",
    {"feet": "int", "from": ["caster", "all-living-players", "combat"], "except": ["other-forced-movement"]}, ["fear", "repel", "keep distance", "flee"])
eff("move.free", "Moves freely", "movement", "The subject may move about (often while protected), within a limit if the text gives one.",
    {"feet": "int"}, ["reposition", "retrieve"])

# action restrictions (on anyone: a restriction on the bearer of a beneficial ability is a drawback)
eff("action.restrict", "Restricts actions", "control", "The subject may not do something, or may do it only to someone.",
    {"what": ["attack-caster", "cast-at-caster", "attack-anyone-but-caster", "cast-at-anyone-but-caster", "move-from-start",
              "wield-weapons", "wield-shields", "wear-armor", "interact-with-game", "impede-play", "approach-enemy-base",
              "fire-normal-arrows", "use-alternate-bases", "wield-great-weapons", "wield-javelins", "wield-heavy-thrown", "wield-long-weapons",
              "wield-bows", "wield-large-shields", "use-other-sources-of-ability", "wear-others-magical-enchantments", "exit-early"]}, ["taunt", "pacify", "restrict", "forbid"])

# equipment and armor
eff("equipment.destroy", "Destroys equipment", "equipment", "Equipment is destroyed.",
    {"what": ["weapon", "shield", "weapons-and-shields", "all-carried-equipment"]}, ["shatter", "break", "sunder"])
eff("equipment.disable", "Disables equipment", "equipment", "Equipment may not be wielded for a time.", {"what": ["weapon"]}, ["heat", "disarm"])
eff("equipment.repair", "Repairs equipment", "equipment", "Damaged or destroyed equipment is repaired.",
    {"what": ["one-item", "all-carried-equipment"]}, ["mend", "fix", "repair"])
eff("equipment.protect", "Protects equipment", "equipment", "Equipment cannot be destroyed or damaged, fully or except by some effects.",
    {"what": ["weapons", "shield", "weapons-or-shield", "weapons-and-shields"], "degree": ["except-object-destroying-abilities", "indestructible"]},
    ["harden", "unbreakable", "indestructible"])
eff("armor.destroy", "Destroys armor", "armor", "Armor points are removed.", {"scope": ["one-location", "all-locations"]}, ["strip armor"])
eff("armor.damage", "Damages armor", "armor", "Armor loses some points in a location.", {"points": "int"}, ["armor loss"])
eff("armor.repair", "Repairs armor", "armor", "Armor points are restored.",
    {"amount": ["one-point-one-location", "all-points-one-location", "one-point-each-location", "all-armor"]}, ["mend armor", "restore armor"])
eff("armor.magic", "Grants Magic Armor", "armor", "The subject gains points of Magic Armor.", {"points": "int"}, ["magic armor", "armor", "skin"])
eff("armor.protect", "Protects armor", "armor", "Worn armor is protected from something.", {"against": ["armor-breaking"]}, ["harden armor"])
eff("special-effect.grant", "Gives a Special Effect", "special-effects", "Weapons, a Magic Ball, an arrow or the next wound carry a Special Effect.",
    {"effect": SPECIAL_EFFECTS, "on": ["bearer-melee-weapons", "bearer-wielded-weapons", "this-magic-ball", "this-arrow", "next-wound", "this-weapon"]},
    [])
eff("armor.limit", "Changes the armor limit", "armor", "The class maximum armor changes.", {"points": "int", "change": ["increase", "set"]}, [])

# defense
eff("defense.immunity", "Grants Immunity", "defense", "The subject is Immune to a School (or one chosen from a list).",
    {"school": SCHOOLS + ["choice"], "options": "schools"}, ["immune", "immunity", "ward"])
eff("defense.resistance", "Grants Resistance", "defense", "The subject is Resistant: unaffected by the next matching effect.",
    {"to": ["wounds", "chosen-school", "next-source"], "options": "schools", "covers_equipment": ["yes", "no"]},
    ["resist", "resistant", "shield", "blessing", "absorb"])
eff("defense.unaffected", "Unaffected by", "defense", "The subject is unaffected by a class of things.",
    {"by": ["projectiles-except-magic-balls", "verbal-magical-beyond-touch", "magical-abilities", "verbal-abilities",
            "hostile-actions-within-20ft", "schools", "blink", "forced-movement-except-banish", "combat-and-abilities"],
     "schools": "schools"}, ["protection", "anti-magic", "untouchable", "deflect"])
eff("defense.negate-hit", "Ignores a hit", "defense", "The effects of a hit or event are ignored (the text says which and at what cost).",
    {"from": ["hits-on-worn-armor", "weapons-and-arrows", "lethal-event", "blocked-projectiles"], "except_effects": "special-effects"}, ["deflect", "absorb", "negate"])
eff("defense.negate-engulfing", "Ignores Engulfing effects", "defense", "Engulfing effects do not affect the subject.", {}, [])
eff("defense.block-projectiles", "Blocks projectiles by hand", "defense", "The subject may block projectiles with hands or weapons.", {}, ["catch", "deflect"])

# magic and enchantments
eff("enchantment.remove", "Removes Enchantments", "magic", "Enchantments on the subject are removed.",
    {"scope": ["all", "non-persistent", "non-persistent-others", "auto-insubstantial-only", "others-than-this", "chosen-to-meet-limit"]},
    ["dispel", "strip", "purge", "sever"])
eff("enchantment.spend-strip", "Uses up a strip", "magic", "A strip of this Enchantment is removed each time it activates or is used.",
    {"n": "int"}, ["charge", "strip"])
eff("enchantment.protect", "Protects Enchantments", "magic", "The subject's Enchantments cannot be removed by Dispel Magic or similar.", {}, ["anti-dispel"])
eff("enchantment.extra-slot", "Allows extra Enchantments", "magic", "The subject may wear more Enchantments.",
    {"count": "int", "only": ["any", "protection-school", "magical-from-this-caster"]}, ["slot", "enchantment limit"])
eff("enchantment.make-persistent", "Makes Enchantments Persistent", "magic", "Enchantments return after respawn.",
    {"which": ["all-worn", "the-extra-enchantment"]}, ["persistent"])

# abilities and resources
eff("ability.grant", "Grants an ability", "abilities", "The subject gains another named ability (or its effects, 'as per').",
    {"ability": "ability", "how": ["gains", "as-per", "extra-use"], "frequency": "text", "meta": "text"}, ["gain", "grant"])
eff("class.look-the-part", "Changes Look The Part", "abilities", "The class's Look The Part bonus becomes something else.",
    {"ability": "ability", "how": ["replaced-by", "extra-use-of"]}, ["look the part"])
eff("weapon.ignore-protections", "Weapons ignore protections", "special-effects",
    "The subject's weapons (and their Special Effects) ignore some protections.", {"against": ["magic-armor", "wound-resistances", "armor"]},
    ["pierce", "ignore armor"])
eff("ability.replace", "Replaces an ability", "abilities", "One named ability is replaced by another.", {"ability": "ability", "with": "ability", "note": "text"},
    ["replace", "upgrade"])
eff("ability.cast-via-strips", "Casts another ability by spending strips", "abilities",
    "The subject may cast a named ability by removing one of this Enchantment's strips.", {"ability": "ability"}, ["charges", "strips"])
eff("ability.charge", "Instantly Charges an ability", "abilities", "An ability is Charged instantly (no Charge Incantation).", {}, ["charge", "recharge"])
eff("ability.restore-uses", "Restores used abilities", "abilities", "Used per-life abilities are regained.",
    {"amount": ["one", "all"], "ability": "ability"}, ["refresh", "restore", "empower"])
eff("ability.charge-faster", "Speeds up Charging", "abilities", "Charge Incantation repetitions are reduced.", {"factor": "text"}, ["inspire"])
eff("ability.modify", "Changes another ability", "abilities", "A named ability (or group) works differently for the subject.",
    {"ability": "ability", "group": "text", "change": "text", "requirement": "text"}, [])
eff("ability.remove", "Removes an ability", "abilities", "The subject loses all instances of a named ability.", {"ability": "ability"}, ["lose"])
eff("ability.declare-instead", "Casts by declaration", "abilities",
    "The subject may use something by declaring it instead of incanting (not stopped by Suppressed, may move).", {"what": "text"}, [])
eff("ability.cast-while-insubstantial", "Casts while Insubstantial", "abilities", "Named abilities may be cast while Insubstantial.",
    {"abilities": "abilities", "on": ["self", "same-casting-targets"]}, [])
eff("meta.modify-next", "Modifies the next ability cast", "meta-magic", "Meta-Magic: changes how the next ability is cast.",
    {"mode": ["cast-while-moving", "extend-range-to-50ft", "single-incantation", "persistent-enchantment"]}, ["meta-magic"])
eff("economy.frequency", "Changes how often abilities can be used", "economy", "Uses, frequency or Charge of a group of abilities change.",
    {"scope": "text", "change": ["double-uses", "charge-x3", "charge-x5", "charge-x10", "unlimited", "other"]}, ["double", "frequency"])
eff("economy.cost", "Changes point costs", "economy", "Magic point costs change.", {"scope": "text", "change": ["double", "zero", "other"]}, ["cost"])
eff("economy.purchase-restrict", "Forbids purchases", "economy", "The class may not purchase some abilities or equipment.",
    {"scope": "text"}, ["forbid", "may not purchase"])
eff("equipment.permit", "Allows equipment", "equipment", "The subject may wield or wear equipment it otherwise could not.",
    {"per_instance": ["yes"], "what": ["short-weapon", "long-weapon", "great-weapon", "hinged-weapon", "javelins", "small-shield", "medium-shield", "bows",
              "any-number-of-specialty-arrows", "carry-extras"]}, ["wield", "equipment"])
eff("casting.modify", "Changes casting rules", "abilities", "A general casting rule changes for the subject (for example no empty hand needed).",
    {"change": "text"}, [])
eff("ability.range-change", "Changes ranges", "abilities", "Ranges of a group of abilities change.", {"group": "text", "to": "text"}, [])
eff("other", "Other effect", "other", "Anything the vocabulary cannot express. Always explain in 'note' and add an open question.", {"text": "text"}, [])

EFFECTS = E

# plain labels for state.apply by state
STATE_VERB = {"cursed": "Curses", "fragile": "Makes Fragile", "frozen": "Freezes", "insubstantial": "Makes Insubstantial",
              "invulnerable": "Makes Invulnerable", "stopped": "Stops", "stunned": "Stuns", "suppressed": "Suppresses"}

# ----------------------------------------------------------------------------------------------------------- other facets
SUBJECTS = {
    "caster": "the player using the ability",
    "bearer": "whoever wears the Enchantment or has the Trait/Archetype (may be the caster or another player)",
    "target": "a targeted living player other than (or possibly) the caster",
    "struck-player": "the player hit by the Magic Ball or Specialty Arrow",
    "dead-target": "a targeted dead player",
    "friendly-players": "friendly players (all, or within a distance given in the effect)",
    "group": "several players at once (e.g. the caster and up to five willing players)",
    "target-equipment": "a targeted item (weapon, shield) rather than the person",
    "bearer-equipment": "the bearer's own weapons, shield or armor",
    "hit-location": "a hit location (and its armor) on the target",
    "caster-of-enchantment": "the caster of an Enchantment worn by someone else (e.g. what Undead Minion gives its caster)",
}
POLARITY = {"benefit": "good for the subject", "harm": "bad for the subject (on the bearer of a helpful ability this is a drawback)",
            "neutral": "neither", "depends": "helpful on an ally, harmful on an enemy (the caster chooses the target)"}
DURATION = {
    "instant": "happens once and is over",
    "timed": "lasts a number of seconds (give 'seconds')",
    "while-worn": "lasts while the Enchantment is worn",
    "while-chanting": "lasts while the Chant continues",
    "until-used": "lasts until it triggers once (next wound, next source, next ability)",
    "until-arrival": "lasts until the subject reaches a destination",
    "until-removed": "lasts until removed or ended by a stated condition",
    "until-respawn": "lasts until the subject respawns",
    "rest-of-game": "lasts for the rest of the game",
    "permanent": "always on (Traits, Archetypes)",
}
TIMING = {
    "on-cast": "when the ability is cast",
    "while-active": "continuously while it is worn, chanted or in effect",
    "on-death": "when the subject would die",
    "on-kill": "after the caster kills an enemy (Kill Trigger)",
    "on-wound": "after the caster wounds an enemy (Wound Trigger)",
    "on-struck": "when a weapon, arrow or ball strikes the subject or their armor",
    "on-strip": "when the bearer spends one of the Enchantment's strips",
    "on-expiry": "when an earlier State from this ability ends",
    "on-removal": "when the Enchantment is removed",
    "on-arrival": "when the subject reaches the destination",
    "after-delay": "a number of seconds after casting (give 'seconds')",
    "on-choice": "when the bearer makes a stated choice",
}
CONDITIONS = {  # conditions that gate one effect (the ability can be cast, but this effect only happens if...)
    "target-wounded": "the target is wounded", "target-dead": "the target is dead", "target-willing": "the target is willing",
    "target-stopped": "the target is Stopped", "target-frozen": "the target is Frozen", "target-insubstantial": "the target is Insubstantial",
    "target-not-cursed": "the target is not Cursed", "target-not-wounded": "the target has no wounds",
    "target-not-moved-5ft": "the dead target has not moved more than 5' from where they died", "target-at-respawn": "the dead target is at their respawn",
    "still-enchanted": "the bearer still has the Enchantment", "armor-has-points": "the struck armor still has points",
    "caster-was-cause": "the caster caused (and voluntarily entered) the existing State",
    "caster-alive": "while the caster is alive", "touched-weapon": "the subject voluntarily carried or touched a weapon (other than blocking)",
    "bearer-wears-armor": "the bearer is wearing armor", "killed-with-thrown-weapon": "the kill was made with a thrown weapon",
    "cast-on-self": "the ability is cast on the caster", "cast-on-other": "the ability is cast on another player",
}
REQUIREMENTS = {  # must be true to cast the ability at all
    "target-willing": "target must be willing", "target-dead": "target must be dead", "target-wounded": "target must be wounded when the incantation begins",
    "target-dead-at-start": "target must be dead when the incantation begins", "target-stopped": "target must be Stopped",
    "target-frozen": "target must be Frozen", "target-insubstantial": "target must be Insubstantial", "target-not-cursed": "target must not be Cursed",
    "target-not-moved-5ft": "dead target must not have moved more than 5' (or be at respawn when stated)",
    "target-not-invulnerable": "does not affect Invulnerable targets", "target-not-already-wounded": "has no effect on already-wounded targets",
    "target-is-equipment": "the target is an item",
    "no-enemy-within-20ft": "no living enemy within 20' of the caster", "no-enemy-within-10ft": "no living enemy within 10' of the caster",
    "caster-not-cursed": "caster must not be Cursed", "caster-not-stopped": "caster must not be Stopped",
    "immediately-after-kill": "only immediately after the caster kills an enemy", "immediately-after-wound": "only immediately after the caster wounds an enemy", "after-dying": "only immediately after the caster dies",
    "only-verbals-20ft": "only on Verbals with a range of 20'", "only-touch-other-self-or-balls": "only on Touch/Other/Self abilities or Magic Balls",
    "not-on-charge-incantation": "may not be used on the Charge Incantation",
    "only-4th-level-or-lower": "only on a Verbal of 4th level or lower", "chosen-before-game": "must be chosen before the game and cannot be changed",
    "not-on-certain-abilities": "does not work on listed abilities (name them in references)", "needs-remaining-use": "a use must still remain",
    "only-magic-users": "only usable by Magic Users", "caster-alive": "the caster must be alive (may be cast even while otherwise unable)",
    "only-enchantments": "only works on Enchantments", "only-enchantments-balls-verbals": "only on Enchantments, Magic Balls or Verbals", "bearer-wears-armor": "only works on worn armor", "target-no-worn-armor": "fails on a target wearing armor", "chose-ability-at-level": "only if a listed ability was chosen at a given level",
}
RESTRICTIONS = {  # limits on using or combining the ability
    "no-other-protection-enchantments": "may not be worn with other Protection School Enchantments unless those are (ex)",
    "not-with-abilities": "may not be used or worn with named abilities (list them in references with relation 'excludes')",
    "not-with-itself-or-similar": "may not be used with itself or similar abilities",
    "one-active-per-caster": "a caster may only have one active at a time", "max-active-per-caster": "a caster may have at most N active (give n)",
    "once-per-life": "may be used or activate only once per life", "excludes-other-sources": "other sources of the same ability may not be used while it is worn",
    "caster-may-not-use-alternate-bases": "the caster may not use Alternate Bases", "bearer-not-alternate-base": "the bearer may not be treated as an Alternate Base",
    "may-not-impede-play": "the subject may not impede play", "stay-away-from-combat": "must stay at least 10' away from combat",
    "players-benefit-once": "a player benefits from only one instance at a time",
    "no-respawn-near-enemies": "cannot be used as a respawn point with living enemies or objectives within 20'",
    "not-exit-at-alternate-base": "may not be ended at an Alternate Base", "must-still-purchase": "the modified ability must still be purchased",
    "only-one-option": "only one of the listed options may be chosen", "not-on-self": "may not be cast on self",
    "limited-targets": "may only be cast on particular targets (explain in note)",
    "not-against-own-effects": "does not trigger against effects cast by the bearer", "no-exit-near-enemy": "may not be ended within N' of a living enemy (give n)",
    "no-exit-early": "the subject may not end it early", "magical-enchantments-only-from-caster": "the bearer may only wear (m) Enchantments from this caster",
}
TERMINATION = {  # what ends an ongoing effect early
    "exit-at-will": "the subject may end it at any time (states how)", "on-arrival": "ends on reaching the destination",
    "caster-attacks-or-casts-at-target": "ends if the caster attacks or casts at the target", "caster-dies": "ends if the caster dies",
    "either-dies": "ends if the caster or the target dies", "other-forced-movement": "ends if another Forced Movement effect affects the subject",
    "subject-gains-state": "ends if the subject becomes Frozen, Insubstantial, Invulnerable or Stunned (list them)",
    "insubstantial-ends": "ends if the Insubstantial State from it ends", "moves-from-start": "ends if the bearer moves from their starting location",
    "begins-incantation": "ends if the subject begins an incantation", "picks-up-magic-balls": "ends if the caster picks up more Magic Balls",
    "casts-new-magic": "ends if the caster begins casting new Magical abilities", "last-strip": "removed when the last strip is removed",
    "chant-stops": "ends if the Chant stops", "counting-stops": "ends if the caster stops counting aloud",
    "activates-once": "ends after it activates once", "caster-ends-for-all": "the caster ending it ends it for everyone",
    "attacked-by-caster": "ends if the target is attacked by the caster", "fails-to-count": "ends on failure to count",
    "exit-only-at-base": "may only be ended at base (in the circumstances given in a condition or note)",
}
PROPERTIES = {
    "forced-movement": "the text says it is a Forced Movement effect", "engulfing": "Engulfing", "chant": "requires a Chant",
    "kill-trigger": "Kill Trigger", "wound-trigger": "Wound Trigger", "castable-while-moving": "may be cast or used while moving",
    "works-while-suppressed": "usable while Suppressed or Stunned", "no-verbal-targeting": "does not require verbal targeting",
    "targets-equipment": "targets an item, not the person", "targets-player-affects-equipment": "targets the player but affects their equipment or armor",
    "persistent": "the Enchantment is Persistent (returns after respawn)", "active-while-dead": "remains active while the bearer is dead",
    "exempt-from-enchantment-limit": "does not count towards the Enchantment limit", "uses-strips": "tracked with enchantment strips",
    "count-aloud": "the caster must count aloud", "declaration-not-incantation": "uses a declaration that is not an incantation",
    "has-choice": "the subject chooses between options", "affects-caster-and-target": "can affect the caster and others",
    "bypass-armor": "ignores armor", "bypass-magic-armor": "ignores Magic Armor", "bypass-enchantments": "ignores Enchantments",
    "bypass-immunities": "works regardless of Immunities", "bypass-traits": "works regardless of Traits", "bypass-states": "works regardless of States",
    "bypass-resistances": "ignores Resistances", "bypass-cursed": "works on (or removes) Cursed", "cannot-be-removed": "cannot be removed",
    "caster-always-benefits": "the caster benefits regardless of their own Traits, States, Immunities, etc.",
    "not-expended-on-failure": "not expended if it fails", "reusable": "not used up when it triggers; keeps working until removed",
    "bypass-ongoing-effects": "works regardless of Ongoing Effects",
    "personal-protections-do-not-cover-equipment": "protections only stop it if they specifically extend to armor or equipment", "expended-even-if-ineffective": "expended even if it has no effect",
    "must-declare": "the subject must make a declaration (give the words in note)", "materials-required": "requires specific materials (strips, covers)",
}
REF_TARGETS = ["ability", "state", "special-effect", "mechanic"]
REF_RELATIONS = {
    "grants": "gives the subject the ability", "casts-via-strips": "lets the bearer cast it by spending strips", "as-per": "works as that ability does",
    "modifies": "changes how it works", "removes": "takes it away", "excludes": "cannot be combined with it", "works-with": "explicitly works together",
    "example": "named as an example", "protects-against": "protects against it", "countered-by": "is stopped or removed by it",
    "counters": "stops or removes it", "requires": "requires it", "mentions": "mentioned for another reason",
}
MECHANICS = ["ability-order", "alternate-base", "archetype", "base", "chant", "charge", "empty-hand", "enchantments", "engulfing",
             "forced-movement", "immune", "incantation", "magic-armor", "magic-balls", "meta-magic", "ongoing-effects", "range",
             "resistant", "respawn", "refresh", "school", "specialty-arrows", "traits", "trigger", "verbal", "persistent", "look-the-part",
             "enchantment-limit", "armor", "shield", "weapon", "game-objectives", "declaration", "strips", "reeve"]
ROLES = {
    "offense": "kills, wounds or damages enemies", "control": "limits what enemies can do or where they can be", "debuff": "weakens a target for later",
    "defense": "protects from harm", "healing": "heals wounds", "revival": "returns the dead to life", "mobility": "moves the user or allies",
    "anti-magic": "removes or blocks abilities and enchantments", "equipment": "affects weapons, shields or armor", "resource": "more uses, charges, slots",
    "team": "helps allies or the team as a whole", "utility": "anything else", "class-modifier": "changes class rules (archetypes, equipment traits)",
}
BENEFICIARY = {"self": "only ever helps the user", "ally": "used to help a friendly player (possibly the user)",
               "enemy": "used against an enemy (even if the point is to protect the user)", "any": "used on friend or foe (e.g. Release, Dispel Magic)",
               "team": "helps the team or several allies at once"}

# ------------------------------------------------------------------------------------------------------- capabilities
# Derived by scripts/meta_build.py (own_caps / derive). 'others' = target, struck player, dead target, group, hit location or target
# equipment; 'self' = caster, bearer or their equipment. Label is what people search for; rule is exactly how it is computed.
CAPABILITIES = {
    "causes-death": ("Causes death", "an effect Causes death"),
    "can-be-lethal": ("Can kill (directly or by making wounds lethal)", "Causes death, Wounds Kill or Siege, or makes another player Fragile"),
    "holds-in-place": ("Holds a player in place", "puts Frozen, Stopped or Stunned on another player, or forbids them to move from where they are"),
    "neutralizes": ("Takes a player out of the fight", "puts Frozen, Stunned, Insubstantial or Invulnerable on another player"),
    "silences": ("Stops a player casting", "puts a State that prevents casting (Frozen, Stunned, Suppressed) on another player"),
    "removes-from-play": ("Removes a player from play for a time", "puts Frozen, Insubstantial or Invulnerable on another player"),
    "makes-insubstantial": ("Makes a player Insubstantial", "puts Insubstantial on anyone, the user included"),
    "self-protection-state": ("Makes the user Insubstantial or Invulnerable", "puts Insubstantial or Invulnerable on the user or bearer"),
    "curses": ("Curses another player", "puts Cursed on another player (a Cursed drawback on the user shows under 'Applies State to own side')"),
    "wounds": ("Wounds", "inflicts a wound"),
    "heals": ("Heals wounds", "heals wounds"),
    "revives": ("Returns the dead to life", "returns a dead player to life"),
    "survives-death": ("Survives death", "prevents death"),
    "repairs": ("Repairs equipment or armor", "repairs equipment or armor"),
    "dispels": ("Removes Enchantments from others", "removes Enchantments from another player"),
    "cleanses": ("Removes States or effects", "removes or takes on States or Ongoing Effects"),
    "protects": ("Protects", "immunity, resistance, 'unaffected by', negating hits or Engulfing, blocking projectiles, Magic Armor, "
                 "protecting armor, equipment or Enchantments, or preventing States"),
    "resists": ("Makes Resistant", "gives Resistance (to wounds, the next source, or a chosen School)"),
    "moves-others": ("Moves other players", "any movement effect on another player"),
    "moves-ally": ("Moves an ally", "a movement effect on another player that is good for them (Teleport, Summon Dead)"),
    "moves-self": ("Moves the user or bearer", "any movement effect on the user or bearer"),
    "restricts-others": ("Restricts what others may do", "limits the actions of another player"),
    "attacks-equipment": ("Destroys or disables weapons or shields", "destroys or disables equipment, or gives Weapon Destroying, Shield Destroying or Shield Crushing"),
    "defeats-armor": ("Breaks, destroys or ignores armor", "Armor Breaking or Armor Destroying, removes armor points, weapons that ignore (Magic) Armor, "
                      "or the property 'ignores armor' / 'ignores Magic Armor'"),
    "more-uses": ("More uses, charges or slots", "instant Charge, restored uses, faster Charging, changed frequency, or extra Enchantment slots"),
    "changes-frequency": ("Changes the frequency or Charge of abilities", "changes the uses, frequency or Charge of a group of abilities, or speeds up Charging"),
    "extra-enchantments": ("Extra Enchantments", "an extra Enchantment slot, or exempt from the Enchantment limit"),
    "team-base": ("Respawn point or Alternate Base", "acts as a respawn point or Alternate Base"),
    "grants-abilities": ("Grants other abilities", "grants an ability, works 'as per' one, casts one from strips, or changes Look The Part to one "
                         "(an extra use of an ability the class already has is recorded but gives nothing new)"),
    "castable-while-moving": ("Can be used while moving", "the property, Ambulant on a class listing, the Ambulant Meta-Magic, or a Specialty Arrow; "
                              "through a grant when the granted ability is taken (Ambulant)"),
    "has-drawback": ("Has a drawback for its user", "something bad for the user's own side: a harmful effect on the user, bearer or their group, "
                     "on the ally it is cast on, a limiting restriction (no other Protection Enchantments, other sources may not be used ...), "
                     "or a drawback of an ability it works 'as per'"),
}
