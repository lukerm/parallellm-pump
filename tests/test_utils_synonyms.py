import pytest

from src.utils.synonyms import find_provider_synonym

def test_find_provider_synonym_openai():
    assert find_provider_synonym("openai") == "openai"
    assert find_provider_synonym("open_ai") == "openai"
    assert find_provider_synonym("OpenAI") == "openai"
    for typo in ["openaii", "apanai", "ClosedAI"]:
        with pytest.raises(ValueError):
            find_provider_synonym(typo)


def test_find_provider_synonym_anthropic():
    assert find_provider_synonym("anthropic") == "anthropic"
    assert find_provider_synonym("Anthropic") == "anthropic"
    assert find_provider_synonym("claude") == "anthropic"
    for typo in ["antropic", "clade", "aanthropiic"]:
        with pytest.raises(ValueError):
            find_provider_synonym(typo)