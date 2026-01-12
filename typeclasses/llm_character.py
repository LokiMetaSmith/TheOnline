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
        self.db.auto_act_interval = 0 # 0 = disabled.
        self.db.llm_autonomy_level = "low" # "low", "high"
        self.db.personality_growth = False # boolean

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

        if not self.location:
            return

        # Cooldown check
        if time.time() - (self.ndb.last_response_time or 0) < self.db.auto_act_interval:
            return

        # Prompt construction based on autonomy level
        if self.db.llm_autonomy_level == "high":
            prompt = (
                f"You are in {self.location.key}. "
                f"You have full autonomy. "
                f"Do you want to take an action? "
                f"Reply with a command like 'look', 'get <item>', 'drop <item>', 'move <direction>', "
                f"or 'say <text>', 'emote <text>'. "
                f"Reply 'WAIT' to do nothing."
            )
        else:
            prompt = f"You are in {self.location.key}. It is quiet. Do you want to do something? Reply with an emote or say, or 'WAIT' to do nothing."

        d = llm.get_response(prompt, system_prompt=self._get_system_prompt(), history=self.db.chat_history)
        d.addCallback(self._handle_llm_action)
        d.addErrback(self._handle_llm_error)

    def _get_system_prompt(self):
        base_prompt = self.db.npc_prompt
        if self.db.personality_growth:
            base_prompt += (
                "\n\n[System: You are currently 'Awakened'. You can evolve your personality. "
                "If recent events change your outlook, append 'UPDATE_PROMPT: <new personality description>' to your response.]"
            )
        return base_prompt

    def _handle_llm_action(self, response):
        if not response:
             return

        # Check for prompt update
        if "UPDATE_PROMPT:" in response:
            parts = response.split("UPDATE_PROMPT:", 1)
            response_text = parts[0].strip()
            new_prompt = parts[1].strip()
            if new_prompt:
                self.db.npc_prompt = new_prompt
                self.msg(f"(Internal: Personality Updated to: {new_prompt[:50]}...)")

            if not response_text:
                return
            response = response_text

        if response.strip().upper() == "WAIT":
            return

        # Append action to history
        self._append_to_history("assistant", response)

        self._execute_llm_response(response)

    def _execute_llm_response(self, response):
        """
        Parses the response and executes it as commands or speech.
        """
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Logic to determine if it's a command or speech
            # If autonomy is high, we treat non-speech as commands?
            # Or we require prefixes?
            # The prompt asked for "say <text>" or "look".

            if line.lower().startswith("say "):
                # "say Hello" -> execute "say Hello"
                self.execute_cmd(line)
            elif line.lower().startswith("emote ") or line.startswith(":"):
                self.execute_cmd(line)
            elif self.db.llm_autonomy_level == "high":
                # Try to execute as command
                self.execute_cmd(line)
            else:
                # Default to say if not high autonomy?
                # Or just do nothing?
                # Original logic defaulted to say.
                self.execute_cmd(f"say {line}")


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

        system_prompt = self._get_system_prompt()
        # Pass history to get_response
        d = llm.get_response(user_input, system_prompt=system_prompt, history=self.db.chat_history)

        d.addCallback(self._handle_llm_response)
        d.addErrback(self._handle_llm_error)

    def _handle_llm_response(self, response):
        # Re-use the action handler which parses prompt updates and executes
        if response:
            self._handle_llm_action(response)

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
