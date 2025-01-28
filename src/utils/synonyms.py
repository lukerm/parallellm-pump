from .providers.openai import SYNONYMS as OPENAI_SYNONYMS


def find_provider_synonym(provider: str):

    synonyms = {
        "openai": OPENAI_SYNONYMS,
    }

    for provider, provider_synonyms in synonyms.items():
        if provider in provider_synonyms:
            return provider

    raise ValueError(f"Provider '{provider}' not found in synonyms list.")
