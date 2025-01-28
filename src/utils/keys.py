"""
Keys should follow the structure below and be stored in a JSON file under config/secret/<FILENAME>

{
    "openai": {
        "api-key": "<KEY>"
    },
    "deepseek": {
        "api-key": "<KEY>"
    },
    ...
}

Note: it's possible to add your own metadata under each provider entry, but this data is currently not used.
"""

import json
from pathlib import Path


def get_key(provider: str, secret_dir: Path = None, filename: str = "api-keys.json") -> str:
    """
    Get the key for a given provider from a JSON file

    :param provider: str, the LLM provider, e.g. "openai"
    :param secret_dir: Path, the directory containing the file with API keys
    :param filename: str, the name of the JSON file containing the API keys
    :return: str, the API key for the given provider
    """
    if secret_dir is None:
        secret_dir = Path(__file__).resolve().parents[2] / "config" / "secret"

    full_filepath = Path(secret_dir) / filename
    with open(full_filepath, "r") as j:
        keys_dict = json.load(j)

        try:
            provider_details = keys_dict[provider]
        except KeyError as e:
            raise KeyError(f"Key for provider '{provider}' not found in {full_filepath}. Available providers: {keys_dict.keys()}")

        try:
            return provider_details["api-key"]
        except KeyError as e:
            raise KeyError(f"The api-key entry for provider '{provider}' not found under its entry in {full_filepath}.")
