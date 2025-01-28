import json
import logging
from pathlib import Path
from typing import List, Dict

SYNONYM_PATH = Path(__file__).resolve().parents[1] / "config" / "synonyms.json"


def find_provider_synonym(provider: str):

    with open(SYNONYM_PATH, "r") as j:
        synonyms = json.load(j)

    for canonical, provider_synonyms in synonyms.items():
        if provider in provider_synonyms:
            return canonical

    raise ValueError(f"Provider '{provider}' not found in synonyms list.")


def get_clean_providers(providers_raw: List[str]) -> Dict[str, str]:
    providers_clean = {}
    for provider_raw in providers_raw:
        try:
            selected_provider = find_provider_synonym(provider_raw)
            providers_clean[selected_provider] = provider_raw
        except ValueError:
            logging.getLogger(__name__).warning(
                f"Provider '{provider_raw}' not found in synonyms list. It will be ignored.")

    return providers_clean
