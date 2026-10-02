import os
from types import SimpleNamespace

import pytest

from app.integrations.gemini import GeminiClient


class FakeModels:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.calls = 0

    def generate_content(self, **kwargs):
        self.calls += 1
        outcome = next(self.outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return SimpleNamespace(text=outcome)


class FakeClient:
    def __init__(self, outcomes):
        self.models = FakeModels(outcomes)


def test_generate_retries_transient_failure(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test")
    monkeypatch.setenv("GEMINI_MAX_RETRIES", "3")
    monkeypatch.setenv("GEMINI_RETRY_BASE_DELAY", "0")
    fake = FakeClient([SimpleNamespace(status_code=503), "ok"])
    monkeypatch.setattr("app.integrations.gemini.genai.Client", lambda api_key: fake)

    client = GeminiClient()
    assert client.generate("test") == "ok"
    assert fake.models.calls == 2


def test_generate_stops_after_retry_limit(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test")
    monkeypatch.setenv("GEMINI_MAX_RETRIES", "2")
    monkeypatch.setenv("GEMINI_RETRY_BASE_DELAY", "0")
    fake = FakeClient([SimpleNamespace(status_code=503)] * 3)
    monkeypatch.setattr("app.integrations.gemini.genai.Client", lambda api_key: fake)

    client = GeminiClient()
    with pytest.raises(RuntimeError, match="after 3 attempt\(s\)"):
        client.generate("test")
    assert fake.models.calls == 3


def test_generate_does_not_retry_non_transient_error(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test")
    monkeypatch.setenv("GEMINI_MAX_RETRIES", "3")
    monkeypatch.setenv("GEMINI_RETRY_BASE_DELAY", "0")
    fake = FakeClient([SimpleNamespace(status_code=400)])
    monkeypatch.setattr("app.integrations.gemini.genai.Client", lambda api_key: fake)

    client = GeminiClient()
    with pytest.raises(RuntimeError, match="after 1 attempt\(s\)"):
        client.generate("test")
    assert fake.models.calls == 1
