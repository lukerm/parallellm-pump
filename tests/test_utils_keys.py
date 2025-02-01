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
from unittest.mock import mock_open

import pytest

from src.utils.keys import get_key


def mock_open_fn(*args, **kwargs):
    key_data = {
        "openai": {"api-key": "test_key_abcdef"},
        "anthropic": {"api-key": "test_key_0123456789"},
    }
    return mock_open(read_data=json.dumps(key_data))()


def test_get_key(monkeypatch):
    monkeypatch.setattr("builtins.open", mock_open_fn)

    assert get_key(provider="openai") == "test_key_abcdef"
    assert get_key(provider="anthropic") == "test_key_0123456789"
    with pytest.raises(KeyError):
        get_key(provider="deepseek")
