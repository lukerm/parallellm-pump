import logging
from datetime import datetime

import openai

from src.utils.keys import get_key

SYNONYMS = ["openai", "open_ai", "OpenAI", "Open AI", "OPENAI", "OPEN_AI"]
OPENAI_MODEL_NAME = "gpt-4o-mini"


async def prompt_openai(prompt: str, model_type: str = None):
    api_key = get_key("openai")
    client = openai.AsyncOpenAI(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    try:
        t0 = datetime.now()
        response = await client.chat.completions.create(
            model=model_type if model_type else OPENAI_MODEL_NAME,
            messages=messages,
        )
        t1 = datetime.now()
        logging.getLogger(__name__).info(f"OpenAI response time: {round((t1 - t0).total_seconds(), 2)}s")
    except (openai.AuthenticationError, openai.APIError) as e:
        logging.getLogger(__name__).error(f"OpenAI authentication error: {e}")
        return "Unable to connect to OpenAI API. Please check your API key."

    return response.choices[0].message.content
