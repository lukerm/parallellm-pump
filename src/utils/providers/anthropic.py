import logging
from datetime import datetime

import anthropic

from src.utils.keys import get_key

SYNONYMS = ["anthropic", "Anthropic", "claude", "Claude", "claude_sonnet", "Claude Sonnet", "ClaudeSonnet"]
ANTHROPIC_MODEL_NAME = "claude-3-5-sonnet-20241022"
ANTHROPIC_MAX_TOKENS = 4096


async def prompt_anthropic(prompt: str, model_type: str = None):
    api_key = get_key("anthropic")
    client = anthropic.AsyncAnthropic(api_key=api_key)

    messages = [
        {"role": "user", "content": prompt}
    ]

    try:
        t0 = datetime.now()
        response = await client.messages.create(
            model=model_type if model_type else ANTHROPIC_MODEL_NAME,
            max_tokens=ANTHROPIC_MAX_TOKENS,
            messages=messages,
        )
        t1 = datetime.now()
        logging.getLogger(__name__).info(f"Anthropic response time: {round((t1 - t0).total_seconds(), 2)}s")
    except (anthropic.AuthenticationError, anthropic.BadRequestError, anthropic.APIError) as e:
        logging.getLogger(__name__).error(f"Anthropic authentication error: {e}")
        return "Unable to connect to Anthropic API. Please check your API key."

    return response.content[0].text
