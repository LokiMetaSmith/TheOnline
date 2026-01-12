"""
Prototypes

A prototype is a simple way to create individualized instances of a
given typeclass. It is dictionary with specific key names.

For example, you might have a Sword typeclass that implements everything a
Sword would need to do. The only difference between different individual Swords
would be their key, description and some Attributes. The Prototype system
allows to create a range of such Swords with only minor variations. Prototypes
can also inherit and combine together to form entire hierarchies (such as
giving all Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a hierarchy of
typeclasses instead.

A prototype can either be a dictionary placed into a global variable in a
python module (a 'module-prototype') or stored in the database as a dict on a
special Script (a db-prototype). The former can be created just by adding dicts
to modules Evennia looks at for prototypes, the latter is easiest created
in-game via the `olc` command/menu.

Prototypes are read and used to create new objects with the `spawn` command
or directly via `evennia.spawn` or the full path `evennia.prototypes.spawner.spawn`.

A prototype dictionary have the following keywords:

Possible keywords are:
- `prototype_key` - the name of the prototype. This is required for db-prototypes,
  for module-prototypes, the global variable name of the dict is used instead
- `prototype_parent` - string pointing to parent prototype if any. Prototype inherits
  in a similar way as classes, with children overriding values in their partents.
- `key` - string, the main object identifier.
- `typeclass` - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
- `location` - this should be a valid object or #dbref.
- `home` - valid object or #dbref.
- `destination` - only valid for exits (object or #dbref).
- `permissions` - string or list of permission strings.
- `locks` - a lock-string to use for the spawned object.
- `aliases` - string or list of strings.
- `attrs` - Attributes, expressed as a list of tuples on the form `(attrname, value)`,
  `(attrname, value, category)`, or `(attrname, value, category, locks)`. If using one
   of the shorter forms, defaults are used for the rest.
- `tags` - Tags, as a list of tuples `(tag,)`, `(tag, category)` or `(tag, category, data)`.
-  Any other keywords are interpreted as Attributes with no category or lock.
   These will internally be added to `attrs` (eqivalent to `(attrname, value)`.

See the `spawn` command and `evennia.prototypes.spawner.spawn` for more info.

"""

## example of module-based prototypes using
## the variable name as `prototype_key` and
## simple Attributes

# from random import randint
#
# GOBLIN = {
# "key": "goblin grunt",
# "health": lambda: randint(20,30),
# "resists": ["cold", "poison"],
# "attacks": ["fists"],
# "weaknesses": ["fire", "light"],
# "tags": = [("greenskin", "monster"), ("humanoid", "monster")]
# }
#
# GOBLIN_WIZARD = {
# "prototype_parent": "GOBLIN",
# "key": "goblin wizard",
# "spells": ["fire ball", "lighting bolt"]
# }
#
# GOBLIN_ARCHER = {
# "prototype_parent": "GOBLIN",
# "key": "goblin archer",
# "attacks": ["short bow"]
# }
#
# This is an example of a prototype without a prototype
# (nor key) of its own, so it should normally only be
# used as a mix-in, as in the example of the goblin
# archwizard below.
# ARCHWIZARD_MIXIN = {
# "attacks": ["archwizard staff"],
# "spells": ["greater fire ball", "greater lighting"]
# }
#
# GOBLIN_ARCHWIZARD = {
# "key": "goblin archwizard",
# "prototype_parent" : ("GOBLIN_WIZARD", "ARCHWIZARD_MIXIN")
# }

# --- Custom LLM NPCs ---

LLM_NPC = {
    "typeclass": "typeclasses.llm_character.LLMCharacter",
    "llm_enabled": True,
    "llm_cooldown": 5,
    "memory_size": 20,
    "auto_act_interval": 60  # Default to acting every minute if in room
}

BARNABY = {
    "prototype_parent": "LLM_NPC",
    "key": "Barnaby",
    "desc": "A round, jovial man with a constant smudge of flour on his nose. He wipes a glass with a rag, eyes darting around the inn.",
    "npc_prompt": (
        "You are Barnaby, the innkeeper of The Rusty Tankard in Oakhaven. "
        "You are friendly, gossipy, and love to tell stories about the village. "
        "You know everyone's business but are harmless. "
        "You speak in a warm, rustic tone."
    ),
    "auto_act_interval": 45
}

KAELEN = {
    "prototype_parent": "LLM_NPC",
    "key": "Kaelen",
    "desc": "A muscular man with soot-stained skin and a gruff demeanor. He hammers away at a piece of glowing iron.",
    "npc_prompt": (
        "You are Kaelen, the blacksmith of Oakhaven. "
        "You are grumpy, focused on your work, and have little patience for idle chatter. "
        "You respect quality craftsmanship and strength. "
        "You are looking for 'Star Metal' to forge a masterpiece."
    )
}

ELARA = {
    "prototype_parent": "LLM_NPC",
    "key": "Elara",
    "desc": "A woman in flowing robes, her eyes obscured by a hood. She stands perfectly still, yet the air around her seems to shimmer.",
    "npc_prompt": (
        "You are Elara, a mystic living in the Whispering Woods. "
        "You are mysterious, speak in riddles, and sense things others cannot. "
        "You are 'Awakened' and have high autonomy. "
        "You warn travelers of the darkness rising in the old Watchtower."
    ),
    "llm_autonomy_level": "high",
    "personality_growth": True,
    "auto_act_interval": 30
}
