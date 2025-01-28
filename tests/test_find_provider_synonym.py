import pytest


def test_find_provider_synonym_openai():
    from src.utils.synonyms import find_provider_synonym

    assert find_provider_synonym("openai") == "openai"
    assert find_provider_synonym("open_ai") == "openai"
    assert find_provider_synonym("OpenAI") == "openai"
    with pytest.raises(ValueError):
        find_provider_synonym("openaii")
