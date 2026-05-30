def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


def test_action_item_filters_bulk_complete_and_pagination(client):
    ids = []
    for text in ["one", "two", "three"]:
        created = client.post("/action-items/", json={"description": text})
        assert created.status_code == 201
        ids.append(created.json()["id"])

    bulk = client.post("/action-items/bulk-complete", json={"ids": ids[:2]})
    assert bulk.status_code == 200
    assert all(item["completed"] for item in bulk.json())

    filtered = client.get("/action-items/", params={"completed": True})
    assert filtered.status_code == 200
    assert len(filtered.json()) >= 2

    paged = client.get("/action-items/page", params={"page": 1, "page_size": 2, "sort": "description_asc"})
    assert paged.status_code == 200
    data = paged.json()
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) == 2
