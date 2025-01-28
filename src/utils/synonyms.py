import json
from pathlib import Path


SYNONYM_PATH = Path(__file__).resolve().parents[1] / "config" / "synonyms.json"


def find_provider_synonym(provider: str):

    with open(SYNONYM_PATH, "r") as j:
        synonyms = json.load(j)

    for canonical, provider_synonyms in synonyms.items():
        if provider in provider_synonyms:
            return canonical

    raise ValueError(f"Provider '{provider}' not found in synonyms list.")
