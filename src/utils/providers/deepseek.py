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

from .openai import prompt_openai


DEEPSEEK_MODEL_NAME = "deepseek-chat"


async def prompt_deepseek(prompt: str, model_type: str = None) -> str:
    """
    Prompt the DeepSeek API with a given prompt. Note that this is a wrapper around the OpenAI API, since it uses the
    same library.

    :param prompt: str, the prompt to send to the API
    :param model_type: str, sub-model identifier, e.g. "deepseek-chat" or "deepseek-reasoner"
    :return: str, the text response from the LLM
    """
    try:
        t0 = datetime.now()
        response_content: str = await prompt_openai(
            prompt,
            model_type=model_type if model_type else DEEPSEEK_MODEL_NAME,
            base_url="https://api.deepseek.com",
            api_key_name="deepseek",
            do_log=False,  # logging will happen in this outer function
        )
        t1 = datetime.now()
        logging.getLogger(__name__).info(f"DeepSeek response time: {round((t1 - t0).total_seconds(), 2)}s")
    except (openai.AuthenticationError, openai.APIError) as e:
        logging.getLogger(__name__).error(f"DeepSeek authentication error: {e}")
        return "Unable to connect to DeepSeek API. Please check your API key."

    return response_content
