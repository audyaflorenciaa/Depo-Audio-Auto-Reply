"""
DA AUTOLIGHT AI — LLM Client Module

Wraps the Google Generative AI (Gemini) SDK.
Loads system_prompt.md + product_data.md at module import time,
then exposes an async function to generate structured JSON responses.
"""

import json
import logging
from pathlib import Path

import google.generativeai as genai

from app.config import settings

logger = logging.getLogger(__name__)

# ── Configure Gemini SDK ───────────────────────────────────────
genai.configure(api_key=settings.GEMINI_API_KEY)

# ── Load prompt files from disk ────────────────────────────────
_APP_DIR = Path(__file__).resolve().parent

_system_prompt_path = _APP_DIR / "prompts" / "system_prompt.md"
_product_data_path = _APP_DIR / "data" / "product_data.md"

_system_prompt_text = _system_prompt_path.read_text(encoding="utf-8")
_product_data_text = _product_data_path.read_text(encoding="utf-8")

# Concatenate system prompt + product data into one instruction
SYSTEM_INSTRUCTION = _system_prompt_text + "\n\n" + _product_data_text

logger.info(
    f"LLM system instruction loaded "
    f"({len(SYSTEM_INSTRUCTION):,} chars, "
    f"prompt={_system_prompt_path.name}, "
    f"data={_product_data_path.name})"
)

# ── Create the Gemini model ────────────────────────────────────
_model = genai.GenerativeModel(
    model_name=settings.GEMINI_MODEL,
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config=genai.types.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.1,
        max_output_tokens=2048,
    ),
)


# ── Custom exception ───────────────────────────────────────────
class LLMError(Exception):
    """Raised when the LLM call fails or returns invalid output."""

    pass


# ── Public API ─────────────────────────────────────────────────
async def generate_response(chat_history: list[dict]) -> dict:
    """
    Send conversation history to Gemini and return the parsed JSON dict.

    Args:
        chat_history: List of message dicts in Gemini format, e.g.
            [{"role": "user", "parts": ["Hello"]},
             {"role": "model", "parts": ["..."]}]

    Returns:
        Parsed JSON dict with keys: next_state, bot_message,
        extracted_entities, handoff, handoff_reason.

    Raises:
        LLMError: If the API call fails or the response is not valid JSON.
    """
    try:
        response = _model.generate_content(contents=chat_history)

        if not response or not response.text:
            raise LLMError("Gemini returned an empty response.")

        # Parse the JSON response
        result = json.loads(response.text)

        # Validate required keys
        required_keys = {
            "next_state",
            "bot_message",
            "extracted_entities",
            "handoff",
            "handoff_reason",
        }
        missing = required_keys - set(result.keys())
        if missing:
            raise LLMError(
                f"Gemini response missing required keys: {missing}. "
                f"Raw response: {response.text[:500]}"
            )

        logger.info(
            f"LLM response: next_state={result['next_state']}, "
            f"handoff={result['handoff']}"
        )
        return result

    except json.JSONDecodeError as e:
        raise LLMError(
            f"Gemini returned invalid JSON: {e}. "
            f"Raw text: {response.text[:500] if response else 'N/A'}"
        )

    except LLMError:
        raise  # Re-raise our own errors

    except Exception as e:
        raise LLMError(f"Gemini API call failed: {e}")
