from types import SimpleNamespace

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_returns_structured_items(monkeypatch):
    def fake_chat(*, model, messages, format, options):
        return SimpleNamespace(message=SimpleNamespace(content='{"items":["Draft agenda","Email team"]}'))

    monkeypatch.setattr("week2.app.services.extract._get_ollama_chat", lambda: fake_chat)
    items = extract_action_items_llm("- Draft agenda\n- Email team")
    assert items == ["Draft agenda", "Email team"]


def test_extract_action_items_llm_handles_empty_list(monkeypatch):
    def fake_chat(*, model, messages, format, options):
        return SimpleNamespace(message=SimpleNamespace(content='{"items":[]}'))

    monkeypatch.setattr("week2.app.services.extract._get_ollama_chat", lambda: fake_chat)
    items = extract_action_items_llm("")
    assert items == []
