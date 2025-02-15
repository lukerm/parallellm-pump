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

import anthropic

from ..keys import get_key

ANTHROPIC_MODEL_NAME = "claude-3-5-sonnet-20241022"
ANTHROPIC_MAX_TOKENS = 4096


async def prompt_anthropic(prompt: str, model_type: str = None) -> str:
    """
    Prompt the Anthropic API with a given prompt.

    :param prompt: str, the prompt to send to the API
    :param model_type: str, sub-model identifier, e.g. "claude-3-5-sonnet-20241022"
    :return: str, the text response from the LLM
    """
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
