from types import SimpleNamespace

from open_acp.tools.base_tool import ToolStatus
from open_acp.tools.generation.claude_generate import ClaudeGenerate
from open_acp.utils import claude as claude_module


def _settings(**overrides):
    values = {
        "anthropic_api_key": "",
        "openai_api_key": "",
        "model_provider": "auto",
        "openai_model_strong": "gpt-5",
        "openai_model_cheap": "gpt-5-mini",
        "openai_base_url": "https://api.openai.com/v1",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_active_provider_prefers_explicit_openai(monkeypatch):
    monkeypatch.setattr(claude_module, "get_settings", lambda: _settings(
        anthropic_api_key="ant-key",
        openai_api_key="openai-key",
        model_provider="openai",
    ))
    monkeypatch.setattr(
        claude_module.anthropic,
        "Anthropic",
        lambda api_key: SimpleNamespace(messages=SimpleNamespace(create=lambda **kwargs: None)),
    )

    client = claude_module.ClaudeClient()

    assert client.active_provider() == "openai"


def test_generate_falls_back_to_openai_and_pins_provider(monkeypatch):
    monkeypatch.setattr(claude_module, "get_settings", lambda: _settings(
        anthropic_api_key="ant-key",
        openai_api_key="openai-key",
        model_provider="auto",
    ))
    monkeypatch.setattr(
        claude_module.anthropic,
        "Anthropic",
        lambda api_key: SimpleNamespace(messages=SimpleNamespace(create=lambda **kwargs: None)),
    )

    client = claude_module.ClaudeClient()
    counts = {"anthropic": 0, "openai": 0}

    def fake_anthropic(**kwargs):
        counts["anthropic"] += 1
        raise RuntimeError("Your credit balance is too low to access the Anthropic API")

    def fake_openai(**kwargs):
        counts["openai"] += 1
        return "fallback response"

    monkeypatch.setattr(client, "_generate_anthropic", fake_anthropic)
    monkeypatch.setattr(client, "_generate_openai", fake_openai)

    assert client.generate("hello") == "fallback response"
    assert client.generate("hello again") == "fallback response"
    assert client.active_provider() == "openai"
    assert counts == {"anthropic": 1, "openai": 2}


def test_openai_payload_omits_temperature_for_gpt5(monkeypatch):
    monkeypatch.setattr(claude_module, "get_settings", lambda: _settings(
        openai_api_key="openai-key",
        model_provider="openai",
        openai_model_strong="gpt-5",
    ))

    captured = {}

    class FakeResponse:
        status_code = 200
        is_error = False
        text = ""

        @staticmethod
        def json():
            return {"output_text": "hello from openai"}

    class FakeClient:
        def __init__(self, timeout):
            self.timeout = timeout

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def post(self, url, headers=None, json=None):
            captured["url"] = url
            captured["headers"] = headers
            captured["json"] = json
            return FakeResponse()

    monkeypatch.setattr(claude_module.httpx, "Client", FakeClient)

    client = claude_module.ClaudeClient()
    text = client.generate("hello", system="system prompt", temperature=0.2)

    assert text == "hello from openai"
    assert captured["url"] == "https://api.openai.com/v1/responses"
    assert captured["json"]["model"] == "gpt-5"
    assert captured["json"]["instructions"] == "system prompt"
    assert "temperature" not in captured["json"]


def test_extract_openai_text_supports_nested_output():
    data = {
        "output": [
            {
                "type": "message",
                "content": [
                    {"type": "output_text", "text": "Part one"},
                    {"type": "text", "text": "Part two"},
                ],
            }
        ]
    }

    assert claude_module.ClaudeClient._extract_openai_text(data) == "Part one\nPart two"


def test_claude_generate_status_uses_settings(monkeypatch):
    monkeypatch.setattr(
        "open_acp.tools.generation.claude_generate.get_settings",
        lambda: _settings(openai_api_key="openai-key"),
    )

    tool = ClaudeGenerate()

    assert tool.get_status() == ToolStatus.AVAILABLE
