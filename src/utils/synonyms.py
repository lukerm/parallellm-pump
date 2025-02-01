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
import json
import logging
from pathlib import Path
from typing import List, Dict

SYNONYM_PATH = Path(__file__).resolve().parents[1] / "config" / "synonyms.json"


def find_provider_synonym(provider: str) -> str:
    """
    Find the canonical provider name from a synonym.
    :param provider: str, the provider name or likely synonym
    :return: str, the canonical provider name linked to the given synonym (provider arg)

    Raises ValueError if the provider is not found in any of the synonyms lists.
    """
    with open(SYNONYM_PATH, "r") as j:
        synonyms = json.load(j)

    for canonical, provider_synonyms in synonyms.items():
        if provider in provider_synonyms:
            return canonical

    raise ValueError(f"Provider '{provider}' not found in synonyms list.")


def get_clean_providers(providers_raw: List[str]) -> Dict[str, str]:
    """
    Creates a map of canonical provider names to raw provider names (given synonyms)
    Note: if a given synonym has no match, it is omitted from the output.
    Note: it is useful to keep a record of the raw names so that we can display them back in the final output.

    :param providers_raw: list, of str, the raw provider names given by the user
    :return: dict, str:str, a map of canonical provider names to raw provider names

    Side effects: logs a warning if a raw provider is not found in the synonyms list, removed from output.
    """
    providers_clean = {}
    for provider_raw in providers_raw:
        try:
            selected_provider = find_provider_synonym(provider_raw)
            providers_clean[selected_provider] = provider_raw
        except ValueError:
            logging.getLogger(__name__).warning(
                f"Provider '{provider_raw}' not found in synonyms list. It will be ignored.")

    return providers_clean
