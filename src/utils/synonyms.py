from .providers.anthropic import SYNONYMS as ANTHROPIC_SYNONYMS
from .providers.openai import SYNONYMS as OPENAI_SYNONYMS


def find_provider_synonym(provider: str):

    synonyms = {
        "openai": OPENAI_SYNONYMS,
        "anthropic": ANTHROPIC_SYNONYMS,
    }

    for canonical, provider_synonyms in synonyms.items():
        if provider in provider_synonyms:
            return canonical

    raise ValueError(f"Provider '{provider}' not found in synonyms list.")
