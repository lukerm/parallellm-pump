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


def test_find_provider_synonym_google():
    assert find_provider_synonym("google") == "google"
    assert find_provider_synonym("Google") == "google"
    assert find_provider_synonym("gemini") == "google"
    for typo in ["gogle", "googel", "gemnii"]:
        with pytest.raises(ValueError):
            find_provider_synonym(typo)