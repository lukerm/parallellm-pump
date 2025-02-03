#  Copyright (C) 2025 lukerm of www.zl-labs.tech
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import logging
from datetime import datetime

import openai

from ..keys import get_key

OPENAI_MODEL_NAME = "gpt-4o-mini"


async def prompt_openai(prompt: str, model_type: str = None, base_url: str = None, api_key_name: str = "openai", do_log: bool = True) -> str:
    """
    Prompt the OpenAI API with a given prompt.

    Note: if the base_url is specified, this will call a different provider's endpoint (e.g. Alibaba, DeepSeek).

    :param prompt: str, the prompt to send to the API
    :param model_type: str, sub-model identifier, e.g. "gpt-4o-mini"
    :param base_url: str, the base URL to use for the API (e.g. "https://api.deepseek.com")
            Note: this is for alternative providers that use the OpenAI python library
    :param api_key_name: str, the name of the API key to use (refers to the key in api-keys.json) (e.g. "openai")
    :param do_log: bool, whether to log output throughout this function's call
    :return: str, the text response from the LLM
    """
    api_key = get_key(api_key_name)
    client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)

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
        logging.getLogger(__name__).info(f"OpenAI response time: {round((t1 - t0).total_seconds(), 2)}s") if do_log else None
    except (openai.AuthenticationError, openai.APIError) as e:
        if api_key_name != "openai":
            raise  # Raising to other callers of this function
        logging.getLogger(__name__).error(f"OpenAI authentication error: {e}") if do_log else None
        return "Unable to connect to OpenAI API. Please check your API key."

    return response.choices[0].message.content
