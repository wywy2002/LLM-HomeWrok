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


def test_note_pagination_sorting_and_tags(client):
    client.post("/notes/", json={"title": "Bravo", "content": "hello #ops"})
    client.post("/notes/", json={"title": "Alpha", "content": "world #docs"})

    page = client.get("/notes/search/page", params={"q": "", "page": 1, "page_size": 1, "sort": "title_asc"})
    assert page.status_code == 200, page.text
    data = page.json()
    assert data["total"] >= 2
    assert data["page"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Alpha"

    note_id = client.post("/notes/", json={"title": "Tagged", "content": "- [ ] Add tag #release"}).json()["id"]
    extracted = client.post(f"/notes/{note_id}/extract", params={"apply": True})
    assert extracted.status_code == 200, extracted.text
    assert extracted.json()["tags"] == ["release"]

    tags = client.get("/notes/tags/all")
    assert tags.status_code == 200
    tag_id = tags.json()[0]["id"]

    attached = client.post(f"/notes/{note_id}/tags", json={"tag_id": tag_id})
    assert attached.status_code == 200
    assert len(attached.json()["tags"]) >= 1


def test_note_validation_and_delete(client):
    bad = client.post("/notes/", json={"title": "", "content": "x"})
    assert bad.status_code == 422

    note = client.post("/notes/", json={"title": "Delete me", "content": "content"}).json()
    deleted = client.delete(f"/notes/{note['id']}")
    assert deleted.status_code == 204

    missing = client.get(f"/notes/{note['id']}")
    assert missing.status_code == 404


