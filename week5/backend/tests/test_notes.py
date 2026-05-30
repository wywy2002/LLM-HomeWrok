def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) >= 1


def test_search_pagination_and_note_crud(client):
    client.post("/notes/", json={"title": "Bravo", "content": "Second"})
    client.post("/notes/", json={"title": "Alpha", "content": "First"})

    paged = client.get("/notes/search/", params={"page": 1, "page_size": 1, "sort": "title_asc"})
    assert paged.status_code == 200
    data = paged.json()
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert data["total"] >= 2
    assert data["items"][0]["title"] == "Alpha"

    note = client.post("/notes/", json={"title": "Edit", "content": "Before"}).json()
    updated = client.put(f"/notes/{note['id']}", json={"title": "Edit", "content": "After"})
    assert updated.status_code == 200
    assert updated.json()["content"] == "After"

    deleted = client.delete(f"/notes/{note['id']}")
    assert deleted.status_code == 204
