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
