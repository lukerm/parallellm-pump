import logging
from datetime import datetime

import openai

from ..keys import get_key

OPENAI_MODEL_NAME = "gpt-4o-mini"


async def prompt_openai(prompt: str, model_type: str = None) -> str:
    """
    Prompt the OpenAI API with a given prompt.

    :param prompt: str, the prompt to send to the API
    :param model_type: str, sub-model identifier, e.g. "gpt-4o-mini"
    :return: str, the text response from the LLM
    """
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
