import openai
from django.conf import settings
from evennia.utils import logger
from evennia.utils.utils import run_async

class LLMClient:
    def __init__(self):
        self.api_key = getattr(settings, "OPENAI_API_KEY", None)
        self.model = getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")
        self.client = None
        if self.api_key:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.log_trace(e)
                self.client = None
        else:
            logger.log_warn("OPENAI_API_KEY not found in settings.")

    def get_response_sync(self, messages, system_prompt):
        """
        Synchronous call to OpenAI.
        """
        if not self.client:
            return None

        # Prepend system prompt to messages
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.log_trace(e)
            return None

# Singleton instance
_client = None

def get_response(prompt, system_prompt="You are a helpful assistant in a MUD game.", history=None):
    """
    Returns a Deferred that fires with the response.
    If 'history' is provided, it is a list of dicts. 'prompt' is appended to it for the call (but not modified in place).
    If 'history' is None, just uses prompt.
    """
    global _client
    if not _client:
        _client = LLMClient()

    messages = []
    if history:
        messages.extend(history)

    # If the prompt is not already in history (which it shouldn't be for the API call construction typically,
    # but the calling code might have added it), we need to handle that.
    # calling code `respond_to` added it to `db.chat_history`.
    # So if `history` contains the latest prompt, we just use `history`.
    # But wait, `respond_to` appends `user_input` to history BEFORE calling `get_response`.
    # And `get_response` receives `prompt` (which is `user_input`) AND `history` (which includes it).
    # So we should just use `history` if provided.

    # However, `at_tick` calls `get_response(prompt, history=chat_history)`.
    # The `prompt` ("Quiet...") is NOT in chat_history.
    # So we need to handle both cases.

    # Logic:
    # If `history` is supplied, use it.
    # Check if `prompt` is the last message in `history`. If not, append it.

    msgs_to_send = list(messages) if messages else []

    if prompt:
        # Check if prompt is already effectively the last message content
        if not msgs_to_send or msgs_to_send[-1]["content"] != prompt:
             msgs_to_send.append({"role": "user", "content": prompt})

    return run_async(_client.get_response_sync, msgs_to_send, system_prompt)
