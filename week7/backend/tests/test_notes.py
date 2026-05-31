def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_replace_and_delete_note(client):
    created = client.post("/notes/", json={"title": "Original", "content": "first"})
    assert created.status_code == 201, created.text
    note_id = created.json()["id"]

    replaced = client.put(f"/notes/{note_id}", json={"title": "Replacement", "content": "second"})
    assert replaced.status_code == 200, replaced.text
    assert replaced.json()["id"] == note_id
    assert replaced.json()["title"] == "Replacement"
    assert replaced.json()["content"] == "second"

    deleted = client.delete(f"/notes/{note_id}")
    assert deleted.status_code == 204

    missing = client.get(f"/notes/{note_id}")
    assert missing.status_code == 404


def test_note_validation_rejects_blank_and_oversized_fields(client):
    blank = client.post("/notes/", json={"title": "", "content": "content"})
    assert blank.status_code == 422

    oversized = client.patch("/notes/1", json={"title": "x" * 201})
    assert oversized.status_code == 422


def test_extract_note_returns_action_items_and_tags(client):
    created = client.post(
        "/notes/",
        json={"title": "Release prep", "content": "- [ ] Ship release #launch\n- ACTION: update docs #docs"},
    )
    assert created.status_code == 201, created.text
    note_id = created.json()["id"]

    extracted = client.post(f"/notes/{note_id}/extract")
    assert extracted.status_code == 200, extracted.text
    data = extracted.json()
    assert data["action_items"] == ["Ship release #launch", "ACTION: update docs #docs"]
    assert data["tags"] == ["launch", "docs"]


def test_extract_note_404_for_missing_note(client):
    response = client.post("/notes/999/extract")
    assert response.status_code == 404


def test_note_pagination_and_sorting_page(client):
    client.post("/notes/", json={"title": "Bravo", "content": "second"})
    client.post("/notes/", json={"title": "Alpha", "content": "first"})
    client.post("/notes/", json={"title": "Charlie", "content": "third"})

    page = client.get("/notes/search/page", params={"q": "", "page": 1, "page_size": 2, "sort": "title_asc"})
    assert page.status_code == 200, page.text
    data = page.json()
    assert data["total"] >= 3
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert [item["title"] for item in data["items"]] == ["Alpha", "Bravo"]


def test_tag_crud_and_note_relationships(client):
    note = client.post("/notes/", json={"title": "Tagged", "content": "content"})
    assert note.status_code == 201, note.text
    note_id = note.json()["id"]

    created_tag = client.post("/notes/tags/all", json={"name": "release"})
    assert created_tag.status_code == 201, created_tag.text
    tag_id = created_tag.json()["id"]
    assert created_tag.json()["name"] == "release"

    listed_tags = client.get("/notes/tags/all")
    assert listed_tags.status_code == 200
    assert listed_tags.json()[0]["name"] == "release"

    attached = client.post(f"/notes/{note_id}/tags", json={"tag_id": tag_id})
    assert attached.status_code == 200, attached.text
    assert attached.json()["tags"] == [{"id": tag_id, "name": "release"}]
    assert attached.json()["id"] == note_id

    detached = client.delete(f"/notes/{note_id}/tags/{tag_id}")
    assert detached.status_code == 200, detached.text
    assert detached.json()["tags"] == []

    deleted_tag = client.delete(f"/notes/tags/{tag_id}")
    assert deleted_tag.status_code == 204


def test_tag_endpoints_return_404_for_missing_entities(client):
    missing_attach = client.post("/notes/999/tags", json={"tag_id": 1})
    assert missing_attach.status_code == 404

    missing_delete = client.delete("/notes/tags/999")
    assert missing_delete.status_code == 404
