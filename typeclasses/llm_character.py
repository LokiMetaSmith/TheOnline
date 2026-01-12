from typeclasses.characters import Character
from world import llm
from evennia.utils import logger
from evennia import TICKER_HANDLER
import time

class LLMCharacter(Character):
    """
    A Character that uses an LLM to generate responses to messages and act autonomously.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.npc_prompt = "You are a generic NPC in a fantasy world. You are helpful and polite."
        self.db.llm_enabled = True
        self.db.llm_cooldown = 5 # seconds
        self.db.chat_history = [] # List of {role, content}
        self.db.memory_size = 10
        self.db.auto_act_interval = 0 # 0 = disabled. Set to e.g. 60 for 1 minute loop.

        # Initialize ticker if enabled
        if self.db.auto_act_interval > 0:
            self.start_ticker()

    def start_ticker(self):
        if self.db.auto_act_interval > 0:
             TICKER_HANDLER.add(self.db.auto_act_interval, self.at_tick, idstring=f"llm_tick_{self.id}")

    def stop_ticker(self):
        TICKER_HANDLER.remove(idstring=f"llm_tick_{self.id}")

    def at_tick(self):
        """
        Called by the ticker.
        """
        if not self.db.llm_enabled:
            return

        # Only act if players are in the room?
        # Finding players in location
        if not self.location:
            return

        # Check if anyone is around (optional, saves credits)
        # We can implement a check here. For now, let's assume always run if enabled.
        # Construct prompt for ambient action

        # Check cooldown (so we don't act if we just spoke)
        if time.time() - (self.ndb.last_response_time or 0) < self.db.auto_act_interval:
            return

        prompt = f"You are in {self.location.key}. It is quiet. Do you want to do something? Reply with an emote or say, or 'WAIT' to do nothing."
        # We don't necessarily add this to history to avoid cluttering chat log with "Quiet" prompts,
        # but the *action* should be added.

        d = llm.get_response(prompt, system_prompt=self.db.npc_prompt, history=self.db.chat_history)
        d.addCallback(self._handle_llm_action)
        d.addErrback(self._handle_llm_error)

    def _handle_llm_action(self, response):
        if not response or response.strip().upper() == "WAIT":
            return

        # Append action to history
        self._append_to_history("assistant", response)

        # Execute
        # If response starts with "say " or "emote ", use it.
        # Otherwise default to say? Or assume raw text is speech?
        # LLMs might output "smiles." -> emote?
        # Let's try to interpret.
        cmd = response.strip()
        if cmd.lower().startswith("say ") or cmd.lower().startswith("emote ") or cmd.lower().startswith(":"):
            self.execute_cmd(cmd)
        else:
            self.execute_cmd(f"say {cmd}")


    def msg(self, text=None, from_obj=None, session=None, **kwargs):
        """
        Overloading msg to catch messages sent to the character.
        """
        super().msg(text, from_obj=from_obj, session=session, **kwargs)

        if not self.db.llm_enabled or not from_obj or from_obj == self:
            return

        # Prevent bot-to-bot loops
        if hasattr(from_obj, 'db') and from_obj.db.llm_enabled:
             return

        # Cooldown check
        last_response = self.ndb.last_response_time or 0
        if time.time() - last_response < (self.db.llm_cooldown or 5):
            return

        msg_text = text
        if isinstance(text, tuple):
            msg_text = text[0]

        if hasattr(from_obj, 'location') and from_obj.location == self.location:
             self.respond_to(msg_text, from_obj)

    def respond_to(self, text, speaker):
        if not text:
            return

        self.ndb.last_response_time = time.time()

        # Update History
        user_input = f"{speaker.key} says: {text}"
        self._append_to_history("user", user_input)

        system_prompt = self.db.npc_prompt
        # Pass history to get_response
        d = llm.get_response(user_input, system_prompt=system_prompt, history=self.db.chat_history)

        d.addCallback(self._handle_llm_response)
        d.addErrback(self._handle_llm_error)

    def _handle_llm_response(self, response):
        if response:
            self._append_to_history("assistant", response)
            self.execute_cmd(f"say {response}")

    def _handle_llm_error(self, failure):
        logger.log_trace(failure)

    def _append_to_history(self, role, content):
        if not self.db.chat_history:
            self.db.chat_history = []

        self.db.chat_history.append({"role": role, "content": content})

        # Trim
        limit = self.db.memory_size or 10
        if len(self.db.chat_history) > limit:
            self.db.chat_history = self.db.chat_history[-limit:]
