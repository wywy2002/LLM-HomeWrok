def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_action_item_pagination_filter_and_bulk_complete(client):
    ids = []
    for description in ["one", "two", "three"]:
        created = client.post("/action-items/", json={"description": description})
        assert created.status_code == 201, created.text
        ids.append(created.json()["id"])

    bulk = client.post("/action-items/bulk-complete", json={"ids": ids[:2]})
    assert bulk.status_code == 200, bulk.text
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


def test_action_item_validation_and_missing_bulk_item(client):
    bad = client.post("/action-items/", json={"description": ""})
    assert bad.status_code == 422

    missing = client.post("/action-items/bulk-complete", json={"ids": [999]})
    assert missing.status_code == 404


