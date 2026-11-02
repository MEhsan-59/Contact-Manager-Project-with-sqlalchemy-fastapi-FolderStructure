def test_add_contact_returns_created_contact(client, sample_contact):
    response = client.post("/contacts/add_contact", json=sample_contact)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] is True
    assert body["data"]["fullname"] == sample_contact["fullname"]
    assert body["data"]["phone_number"] == sample_contact["phone_number"]
    assert body["data"]["category"] == sample_contact["category"]
    assert body["data"]["is_favorite"] is False
    assert isinstance(body["data"]["id"], int)


def test_view_contacts_returns_saved_contacts(client, sample_contact):
    client.post("/contacts/add_contact", json=sample_contact)

    response = client.get("/contacts/view_contact")

    assert response.status_code == 200
    assert response.json()["data"][0]["fullname"] == sample_contact["fullname"]


def test_search_contacts_by_name(client, sample_contact):
    client.post("/contacts/add_contact", json=sample_contact)

    response = client.get(
        "/contacts/view_contact_by_name_or_phone",
        params={"name": "Test"},
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["phone_number"] == sample_contact["phone_number"]


def test_search_contacts_by_phone(client, sample_contact):
    client.post("/contacts/add_contact", json=sample_contact)

    response = client.get(
        "/contacts/view_contact_by_name_or_phone",
        params={"phone_number": "555-0100"},
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["fullname"] == sample_contact["fullname"]


def test_search_without_criteria_returns_not_found(client):
    response = client.get("/contacts/view_contact_by_name_or_phone")

    assert response.status_code == 404
    assert response.json()["detail"] == "Please provide either name or phone number."

def test_add_contact_rejects_invalid_category(client, sample_contact):
    sample_contact["category"] = "Invalid"

    response = client.post("/contacts/add_contact", json=sample_contact)

    assert response.status_code == 422

def test_add_contact_rejects_blank_fullname(client, sample_contact):
    sample_contact["fullname"] = "   "

    response = client.post("/contacts/add_contact", json=sample_contact)

    assert response.status_code == 422


def test_delete_contact_removes_contact(client, sample_contact):
    contact_id = client.post(
        "/contacts/add_contact", json=sample_contact
    ).json()["data"]["id"]

    response = client.delete(
        "/contacts/delete_contact",
        params={"contact_id": contact_id},
    )

    assert response.status_code == 200
    assert response.json()["status"] is True
    assert client.get("/contacts/view_contact").json()["data"] == []


def test_delete_unknown_contact_returns_not_found(client):
    response = client.delete(
        "/contacts/delete_contact",
        params={"contact_id": 9999},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Contact not found."


def test_delete_contact_removes_group_memberships(client, sample_contact):
    create_response = client.post("/contacts/add_contact", json=sample_contact)
    contact_id = create_response.json()["data"]["id"]
    group_response = client.post(
        "/groups/create_group",
        params={"group_name": "Family"},
    )
    group_id = group_response.json()["data"]["group_id"]
    add_response = client.post(
        "/groups/add_contact_to_group",
        params={"group_id": group_id, "contact_id": contact_id},
    )
    assert add_response.status_code == 200

    delete_response = client.delete(
        "/contacts/delete_contact",
        params={"contact_id": contact_id},
    )

    assert delete_response.status_code == 200
    assert client.get(
        "/groups/view_group_contacts",
        params={"group_id": group_id},
    ).status_code == 404
    groups_response = client.get("/groups/view_all_groups")
    assert groups_response.status_code == 200
    assert groups_response.json()["data"][0]["group_name"] == "Family"


def test_update_contact_returns_updated_contact(client, sample_contact):
    create_response = client.post("/contacts/add_contact", json=sample_contact)
    contact_id = create_response.json()["data"]["id"]

    response = client.put(
        f"/contacts/update_contact/{contact_id}",
        json={"fullname": "Updated Contact"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "Contact updated successfully.",
        "data": {
            "id": contact_id,
            "fullname": "Updated Contact",
            "phone_number": sample_contact["phone_number"],
            "category": sample_contact["category"],
            "is_favorite": sample_contact["is_favorite"],
        },
    }


def test_update_unknown_contact_returns_not_found(client):
    response = client.put(
        "/contacts/update_contact/9999",
        json={"fullname": "Updated Contact"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Contact with ID '9999' not found."
