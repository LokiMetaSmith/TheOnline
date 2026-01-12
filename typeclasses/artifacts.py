from typeclasses.objects import Object
import random
from world import llm
from evennia.utils import logger
from evennia.commands.cmdset import CmdSet
from evennia.commands.default.muxcommand import MuxCommand as Command

class CmdTalkToShard(Command):
    """
    Talk to the shard.

    Usage:
      ask shard <message>
      talk shard <message>
    """
    key = "ask shard"
    aliases = ["talk shard", "shard"]

    def func(self):
        shard = self.obj
        msg = self.args.strip()
        if not msg:
            self.caller.msg("Say what to the shard?")
            return

        # Shift personality EVERY time
        shard._shift_personality()

        # Call LLM
        prompt = f"You are {shard.db.current_personality}. The holder says: '{msg}'. Reply in character, briefly."
        self.caller.msg(f"You say to the shard: {msg}")
        self.caller.msg(f"The shard flickers with new colors...")

        # Asynchronous LLM call
        d = llm.get_response(prompt) # Helper function from world.llm
        d.addCallback(self._handle_response)
        d.addErrback(self._handle_error)

    def _handle_response(self, response):
        self.caller.msg(f"The Shard whispers: {response}")

    def _handle_error(self, failure):
        logger.log_trace(failure)
        self.caller.msg("The shard screams in static.")

class ShardCmdSet(CmdSet):
    key = "ShardCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdTalkToShard())

class OrbOfAwakening(Object):
    """
    An artifact that grants the holder full autonomy and personality growth.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.key = "Orb of Awakening"
        self.desc = "A glowing orb that seems to hum with potential."

    def at_get(self, getter):
        super().at_get(getter)
        if hasattr(getter, "db") and getattr(getter.db, "llm_enabled", False):
            getter.msg("You feel a surge of consciousness expand within you!")
            getter.db.llm_autonomy_level = "high"
            getter.db.personality_growth = True
            if getter.db.auto_act_interval == 0:
                 getter.db.auto_act_interval = 60
                 if hasattr(getter, "start_ticker"):
                     getter.start_ticker()

    def at_drop(self, dropper):
        super().at_drop(dropper)
        if hasattr(dropper, "db") and getattr(dropper.db, "llm_enabled", False):
            dropper.msg("The expanded consciousness fades...")
            dropper.db.llm_autonomy_level = "low"
            dropper.db.personality_growth = False

class MemeticShard(Object):
    """
    A shard of pure memetic energy. It has a personality that shifts constantly.
    Players can interact with it by holding it and speaking.
    """

    PERSONALITIES = [
        "A grumpy ancient dwarf who hates heights.",
        "A hyperactive fairy obsessed with glitter.",
        "A melancholy poet who speaks in bad rhymes.",
        "A paranoid spy who thinks everyone is listening.",
        "A bored deity who treats mortals like ants.",
        "A confused time-traveler asking about the year.",
        "A hungry goblin who wants snacks.",
        "A wise old sage who has forgotten the point.",
        "A sarcastic robot from the future.",
        "A frightened child looking for their blanket."
    ]

    def at_object_creation(self):
        super().at_object_creation()
        self.key = "Memetic Shard"
        self.desc = "A jagged shard of crystal that pulses with shifting colors. It feels warm to the touch and seems to whisper in your mind."
        self.db.current_personality = "A void of static."
        # Add the command set
        self.cmdset.add_default(ShardCmdSet)

    def at_get(self, getter):
        super().at_get(getter)
        # Randomize personality on pickup
        self._shift_personality()
        getter.msg(f"The shard vibrates in your hand. You hear a voice: '{self._get_intro()}'")

    def _shift_personality(self):
        self.db.current_personality = random.choice(self.PERSONALITIES)

    def _get_intro(self):
        return "Oh? Who are you? Wait, who am I?"

    def return_appearance(self, looker, **kwargs):
        desc = super().return_appearance(looker, **kwargs)
        return f"{desc}\nIt feels like: {self.db.current_personality}"
