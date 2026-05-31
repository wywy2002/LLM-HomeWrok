from backend.app.services.extract import extract_action_items, extract_tags


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_action_items_and_tags_from_checkboxes():
    text = """
    - [ ] Ship release #launch
    - [ ] Update docs #docs
    - [ ] Ship release #launch
    """.strip()
    items = extract_action_items(text)
    tags = extract_tags(text)
    assert items == ["Ship release #launch", "Update docs #docs"]
    assert tags == ["launch", "docs"]
