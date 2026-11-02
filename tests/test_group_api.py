def test_add_contact_to_group_returns_valid_response(client, sample_contact):
    contact_response = client.post("/contacts/add_contact", json=sample_contact)
    contact_id = contact_response.json()["data"]["id"]
    group_response = client.post(
        "/groups/create_group",
        params={"group_name": "Family"},
    )
    group_id = group_response.json()["data"]["group_id"]

    response = client.post(
        "/groups/add_contact_to_group",
        params={"group_id": group_id, "contact_id": contact_id},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "Contact added to group successfully.",
        "data": {
            "group_name": "Family",
            "contact_fullname": sample_contact["fullname"],
        },
    }


def test_view_all_groups_returns_valid_response(client):
    client.post("/groups/create_group", params={"group_name": "Family"})
    client.post("/groups/create_group", params={"group_name": "Friends"})

    response = client.get("/groups/view_all_groups")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] is True
    assert body["message"] == "Groups retrieved successfully."
    assert {
        (group["group_id"], group["group_name"])
        for group in body["data"]
    } == {(1, "Family"), (2, "Friends")}


def test_view_group_contacts_returns_serializable_contact_data(client, sample_contact):
    contact_response = client.post("/contacts/add_contact", json=sample_contact)
    contact_id = contact_response.json()["data"]["id"]
    group_response = client.post(
        "/groups/create_group",
        params={"group_name": "Family"},
    )
    group_id = group_response.json()["data"]["group_id"]
    client.post(
        "/groups/add_contact_to_group",
        params={"group_id": group_id, "contact_id": contact_id},
    )

    response = client.get(
        "/groups/view_group_contacts",
        params={"group_id": group_id},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "Contacts retrieved successfully.",
        "data": {
            sample_contact["fullname"]: {
                "id": contact_id,
                "fullname": sample_contact["fullname"],
                "phone_number": sample_contact["phone_number"],
                "category": sample_contact["category"],
                "is_favorite": sample_contact["is_favorite"],
            }
        },
    }

def test_view_group_contacts_with_invalid_group_id(client):
    response = client.get(
        "/groups/view_group_contacts",
        params={"group_id": 9999},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No contacts found for this group."
    }

def test_add_contact_to_group_with_invalid_group_id(client, sample_contact):
    contact_response = client.post("/contacts/add_contact", json=sample_contact)
    contact_id = contact_response.json()["data"]["id"]

    response = client.post(
        "/groups/add_contact_to_group",
        params={"group_id": 9999, "contact_id": contact_id},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Group ID not found."
    }