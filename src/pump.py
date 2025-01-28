import argparse
import asyncio
import logging
from datetime import datetime
from typing import List

from .utils.providers.anthropic import prompt_anthropic
from .utils.providers.openai import prompt_openai
from .utils.synonyms import find_provider_synonym

FUNCTION_MAP = {
    "openai": prompt_openai,
    "anthropic": prompt_anthropic,
}


def get_clean_providers(providers_raw: List[str]):
    providers_clean = []
    for provider in providers_raw:
        try:
            selected_provider = find_provider_synonym(provider)
            providers_clean.append(selected_provider)
        except ValueError:
            logging.getLogger(__name__).warning(
                f"Provider '{provider}' not found in synonyms list. It will be ignored.")

    return providers_clean


async def parallellm_pump(prompt: str, providers_clean: List[str]):
    chats = [FUNCTION_MAP[provider](prompt) for provider in providers_clean]
    completions = await asyncio.gather(*chats)
    return {provider: completions[i] for i, provider in enumerate(providers_clean)}


if __name__ == "__main__":
    t0 = datetime.now()
    parser = argparse.ArgumentParser(
        description="""Pump a prompt to multiple language models in parallel. The --providers should be a list of 
        well-known text-based LLM API providers, such as openai, deepseek, etc. 
        
        Due to its parallel implementation, the output will only take as long as the slowest provider to respond."""
    )
    parser.add_argument(
        "--prompt", "-p", required=True, help="The prompt to send to the language models")
    parser.add_argument(
        "--providers", "-pp", nargs="+", required=True, help="The list of language model providers to send the prompt to")
    args = parser.parse_args()

    # Set up logging
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(level='INFO')

    providers_clean = get_clean_providers(providers_raw=args.providers)
    logger.info(f"Running the pump for the following providers: {', '.join(providers_clean)}")
    completions = asyncio.run(parallellm_pump(prompt=args.prompt, providers_clean=providers_clean))

    final_output = ""
    for provider, completion in completions.items():
        final_output += f"\n{provider}\n"
        final_output += f"{'_'*len(provider)}\n\n"
        final_output += f"{completion}\n"

    t1 = datetime.now()
    logger.info(f"Total run time: {round((t1 - t0).total_seconds(), 2)}s")

    logger.info("Results\n" + final_output)
