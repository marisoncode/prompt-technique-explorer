"""
A thin wrapper around the Gemini SDK.

Why wrap it at all? Because every script that needs to talk to the model
(your CLI chatbot, your RAG bot, your agent later) should reuse THIS,
not repeat the same client-setup code five times. If Google changes
the SDK again, you fix it in one place.
"""

import logging
from dataclasses import dataclass

from google import genai
from google.genai import errors as genai_errors

from config import Config

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class ModelResponse:
    """A predictable shape for a response, instead of passing the raw
    SDK object around everywhere. Makes the rest of your code easier
    to read and to test."""
    text: str
    input_tokens: int | None = None
    output_tokens: int | None = None


class GeminiClient:
    def __init__(self) -> None:
        Config.validate()
        self._client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self._model = Config.GEMINI_MODEL

    def generate(self, prompt: str, system_instruction: str | None = None) -> ModelResponse:
        """Send a single prompt to the model and return a clean response object.

        Args:
            prompt: the user's message / question.
            system_instruction: optional persona or behavior rule for the model.

        Raises:
            RuntimeError: if the API call fails, with a clear message
            instead of a raw traceback bubbling up to the caller.
        """
        try:
            config = {}
            if system_instruction:
                config["system_instruction"] = system_instruction

            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=config or None,
            )
        except genai_errors.ClientError as e:
            logger.error("Gemini API call failed: %s", e)
            raise RuntimeError(f"Model call failed: {e}") from e

        usage = getattr(response, "usage_metadata", None)

        return ModelResponse(
            text=response.text,
            input_tokens=getattr(usage, "prompt_token_count", None),
            output_tokens=getattr(usage, "candidates_token_count", None),
        )