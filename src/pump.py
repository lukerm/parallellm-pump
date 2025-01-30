import argparse
import asyncio
import logging
from datetime import datetime
from typing import Dict

from .config.prompt_config import PROMPT_FUNCTION_MAP
from .utils.synonyms import get_clean_providers


def format_pump_output(completions: Dict[str, str], providers_clean: Dict[str, str]) -> str:
    final_output = ""
    for provider, completion in completions.items():
        title = f'{providers_clean[provider]}'
        final_output += f"\n{title}\n"
        final_output += f"{'_' * len(title)}\n\n"
        final_output += f"{completion}\n"

    return final_output


async def parallellm_pump(prompt: str, providers_clean: Dict[str, str]) -> Dict[str, str]:
    """
    Run the parallel pump for the supplied prompt for each of the given providers.

    Note: this is the main asyncio entry point for getting the prompts asynchronously.

    :param prompt: str, the desired prompt to send to the language models
    :param providers_clean: dict, str:str, a map of canonical provider names to raw provider names
            Note: we only make use of the canonical provider names (stored as keys).
    :return: dict, str:str, a map of canonical provider names to their respective responses
        key: str, the canonical provider name
        value: str, the response from the language model
    """
    chats = [PROMPT_FUNCTION_MAP[provider](prompt) for provider in providers_clean.keys()]
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
    # TODO: Similar one that checks existence of API keys (prevent catastrophic failure)
    logger.info(f"Running the pump for the following providers: {', '.join(providers_clean)}")
    completions = asyncio.run(parallellm_pump(prompt=args.prompt, providers_clean=providers_clean))
    final_output = format_pump_output(completions=completions, providers_clean=providers_clean)

    t1 = datetime.now()
    logger.info(f"Total run time: {round((t1 - t0).total_seconds(), 2)}s")

    logger.info("Results\n" + final_output)
