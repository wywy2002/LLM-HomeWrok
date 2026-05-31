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


def test_get_and_delete_action_item(client):
    created = client.post("/action-items/", json={"description": "Clean up"})
    assert created.status_code == 201, created.text
    item_id = created.json()["id"]

    fetched = client.get(f"/action-items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json()["description"] == "Clean up"

    deleted = client.delete(f"/action-items/{item_id}")
    assert deleted.status_code == 204

    missing = client.get(f"/action-items/{item_id}")
    assert missing.status_code == 404


def test_action_item_validation_rejects_blank_and_oversized_description(client):
    blank = client.post("/action-items/", json={"description": ""})
    assert blank.status_code == 422

    oversized = client.patch("/action-items/1", json={"description": "x" * 1001})
    assert oversized.status_code == 422


def test_action_item_pagination_sorting_and_filter_page(client):
    created = []
    for description in ["bravo", "alpha", "charlie"]:
        response = client.post("/action-items/", json={"description": description})
        assert response.status_code == 201, response.text
        created.append(response.json()["id"])

    completed = client.patch(f"/action-items/{created[1]}", json={"completed": True})
    assert completed.status_code == 200, completed.text

    page = client.get(
        "/action-items/page",
        params={"completed": True, "page": 1, "page_size": 1, "sort": "description_asc"},
    )
    assert page.status_code == 200, page.text
    data = page.json()
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert len(data["items"]) == 1
    assert [item["description"] for item in data["items"]] == ["alpha"]
