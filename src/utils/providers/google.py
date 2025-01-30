import logging
from datetime import datetime

from google import genai
from google.genai.errors import APIError

from ..keys import get_key


GOOGLE_MODEL_NAME = "gemini-2.0-flash-exp"


async def prompt_google(prompt: str, model_type: str = None) -> str:
    """
    Prompt the Google API with a given prompt.

    :param prompt: str, the prompt to send to the API
    :param model_type: str, sub-model identifier, e.g. "gemini-2.0-flash-exp"
    :return: str, the text response from the LLM
    """
    api_key = get_key("google")
    client = genai.Client(api_key=api_key)

    try:
        t0 = datetime.now()
        response = await client.aio.models.generate_content(
            model=model_type if model_type else GOOGLE_MODEL_NAME,
            contents=prompt,
        )
        t1 = datetime.now()
        logging.getLogger(__name__).info(f"Google response time: {round((t1 - t0).total_seconds(), 2)}s")
    except APIError as e:
        logging.getLogger(__name__).error(f"Google authentication error: {e}")
        return "Unable to connect to Google API. Please check your API key."

    return response.candidates[0].content.parts[0].text
