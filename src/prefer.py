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
import argparse
import asyncio
import logging
from datetime import datetime
from typing import Dict

from .pump import format_pump_output, parallellm_pump
from .utils.synonyms import get_clean_providers


async def parallellm_prefer(original_prompt: str, providers_clean: Dict[str, str]):
    """
    Run the parallel pump -> prefer pipeline for the supplied prompt for each of the given providers.
    This consists of two main steps:
      1. Send the original prompt to each of the language models
      2a. Make a new prompt containing original prompts and responses
      2b. Send the new prompt to each of the language models, asking them to rank the anonymous responses.

    :param prompt: str, the desired prompt to send to the language models
    :param providers_clean: dict, str:str, a map of canonical provider names to raw provider names
            Note: we only make use of the canonical provider names (stored as keys).
    :return: dict, str:str, a map of canonical provider names to their respective ranked responses
        key: str, the canonical provider name
        value: str, the response from the language model to the second, constructed prompt
    """

    original_responses = await parallellm_pump(prompt=original_prompt, providers_clean=providers_clean)
    logger.info(f"Results from original prompt:\n"
                f"{format_pump_output(completions=original_responses, providers_clean=providers_clean)}\n")

    # Construct the new randomized prompt
    new_prompt = f"""
    You are going to receive {len(original_responses)} responses from different large language models. The prompt will be 
    displayed first (labelled as the 'Prompt' section), followed by subsequent sections labelled as 'Response <n>'. 
    Section titles will be denoted with underscores. I want you to read through all the responses and select the one that 
    you think is the best, in terms of factuality and writing style. Please rank your answers from 1 to {len(original_responses)}, 
    where 1 is the best and {len(original_responses)} is the worst. Give a small bullet-point list briefly explaining the
    reasoning behind your choices. Please provide your answers (ranked list) before writing any other text, starting with
    the character '1'.
    
    Prompt
    ______
    {original_prompt}
    
    """

    for i, (provider, response) in enumerate(original_responses.items()):
        new_prompt += f"""
    Response {i + 1}
    __________
    {response}
        
        """

    logger.info(f"New prompt:\n{new_prompt}")

    preference_completions = await parallellm_pump(prompt=new_prompt, providers_clean=providers_clean)
    return preference_completions


if __name__ == "__main__":
    t0 = datetime.now()
    parser = argparse.ArgumentParser(
        description="""Pump a prompt to multiple language models in parallel, followed by a 'preference' step, where we
        ask each of the models to rate each of the responses, ranking them from best to worst. The --providers should be
        a list of well-known text-based LLM API providers, such as openai, deepseek, etc. 

        Due to its parallel implementation, the output will only take as long as the sum of the two slowest providers
        to respond in each step (pump, then prefer)."""
    )
    parser.add_argument(
        "--prompt", "-p", required=True, help="The prompt to send to the language models")
    parser.add_argument(
        "--providers", "-pp", nargs="+", required=True,
        help="The list of language model providers to send the prompt to")
    args = parser.parse_args()

    # Set up logging
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(level='INFO')

    providers_clean = get_clean_providers(providers_raw=args.providers)
    logger.info(f"Running the pump for the following providers: {', '.join(providers_clean)}")
    preference_completions = asyncio.run(parallellm_prefer(original_prompt=args.prompt, providers_clean=providers_clean))
    final_output = format_pump_output(preference_completions, providers_clean=providers_clean)
    # Make it easier to read which response belongs to which provider
    for i, provider_raw in enumerate(providers_clean.values()):
        final_output = final_output.replace(f"Response {i + 1}", f"Response {i + 1} ({provider_raw})")

    t1 = datetime.now()
    logger.info(f"Total run time: {round((t1 - t0).total_seconds(), 2)}s")

    logger.info("Final preference results:\n" + final_output)
