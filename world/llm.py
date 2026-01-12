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

    def get_response_sync(self, prompt, system_prompt):
        """
        Synchronous call to OpenAI. Should be run in a thread.
        """
        if not self.client:
            return None

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.log_trace(e)
            return None

# Singleton instance
_client = None

def get_response(prompt, system_prompt="You are a helpful assistant in a MUD game."):
    """
    Returns a Deferred that fires with the response.
    """
    global _client
    if not _client:
        _client = LLMClient()

    # We use run_async to offload the blocking call to a thread.
    return run_async(_client.get_response_sync, prompt, system_prompt)
