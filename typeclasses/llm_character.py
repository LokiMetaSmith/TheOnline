from typeclasses.characters import Character
from world import llm
from evennia.utils import logger
import time

class LLMCharacter(Character):
    """
    A Character that uses an LLM to generate responses to messages.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.npc_prompt = "You are a generic NPC in a fantasy world. You are helpful and polite."
        self.db.llm_enabled = True
        self.db.llm_cooldown = 5 # seconds

    def msg(self, text=None, from_obj=None, session=None, **kwargs):
        """
        Overloading msg to catch messages sent to the character.
        """
        super().msg(text, from_obj=from_obj, session=session, **kwargs)

        # If not enabled or no sender, ignore
        if not self.db.llm_enabled or not from_obj:
            return

        # Ignore messages from self
        if from_obj == self:
            return

        # Prevent bot-to-bot loops
        # If the sender is also an LLMCharacter (or has llm_enabled), ignore.
        if hasattr(from_obj, 'db') and from_obj.db.llm_enabled:
             return

        # Cooldown check
        last_response = self.ndb.last_response_time or 0
        if time.time() - last_response < (self.db.llm_cooldown or 5):
            return

        # Basic filtering: Try to detect if this is spoken text.
        msg_text = text
        if isinstance(text, tuple):
            msg_text = text[0]

        # Only respond if the message seems to be addressed to us or spoken in room.
        if hasattr(from_obj, 'location') and from_obj.location == self.location:
             self.respond_to(msg_text, from_obj)

    def respond_to(self, text, speaker):
        """
        Generates a response using the LLM and speaks it.
        """
        if not text:
            return

        # Update cooldown immediately to prevent double triggers while processing
        self.ndb.last_response_time = time.time()

        system_prompt = self.db.npc_prompt
        # Context building
        # We pass the text directly. We assume the LLM can infer context from the system prompt or we can add minimal context.
        # "speaker.key says: text" is standard mud log format.
        prompt = f"{speaker.key} says: {text}\nResponse:"

        # Call the async function
        d = llm.get_response(prompt, system_prompt=system_prompt)

        # Add callback to handle the result
        d.addCallback(self._handle_llm_response)
        d.addErrback(self._handle_llm_error)

    def _handle_llm_response(self, response):
        if response:
            self.execute_cmd(f"say {response}")

    def _handle_llm_error(self, failure):
        logger.log_trace(failure)
