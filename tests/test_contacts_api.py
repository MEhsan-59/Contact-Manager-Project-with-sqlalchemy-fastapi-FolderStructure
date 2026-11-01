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
    client.post("/contacts/add_contact", json=sample_contact)

    response = client.delete(
        "/contacts/delete_contact",
        params={"fullname": sample_contact["fullname"]},
    )

    assert response.status_code == 200
    assert response.json()["status"] is True
    assert client.get("/contacts/view_contact").json()["data"] == []


def test_delete_unknown_contact_returns_not_found(client):
    response = client.delete(
        "/contacts/delete_contact",
        params={"fullname": "Missing Contact"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Contact not found."
