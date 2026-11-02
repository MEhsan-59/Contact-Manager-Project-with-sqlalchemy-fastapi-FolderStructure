def add_favorite(client, contact_id):
    return client.post(
        "/favorites/add_contact_to_favorite",
        params={"contact_id": contact_id},
    )


def test_add_contact_to_favorite_returns_success(client, sample_contact):
    contact_id = client.post(
        "/contacts/add_contact", json=sample_contact
    ).json()["data"]["id"]

    response = add_favorite(client, contact_id)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] is True
    assert body["message"] == "Contact added to favorites successfully."


def test_add_contact_to_favorite_marks_contact_as_favorite(client, sample_contact):
    contact_id = client.post(
        "/contacts/add_contact", json=sample_contact
    ).json()["data"]["id"]

    add_favorite(client, contact_id)

    response = client.get("/contacts/view_contact")
    contacts = response.json()["data"]
    assert contacts[0]["fullname"] == sample_contact["fullname"]
    assert contacts[0]["is_favorite"] is True


def test_add_contact_to_favorite_does_not_change_other_contacts(client, sample_contact):
    other_contact = {
        "fullname": "Other Contact",
        "phone_number": "555-0200",
        "category": "Work",
        "is_favorite": False,
    }
    contact_id = client.post(
        "/contacts/add_contact", json=sample_contact
    ).json()["data"]["id"]
    client.post("/contacts/add_contact", json=other_contact)

    add_favorite(client, contact_id)

    contacts = client.get("/contacts/view_contact").json()["data"]
    favorite_by_name = {c["fullname"]: c["is_favorite"] for c in contacts}
    assert favorite_by_name["Test Contact"] is True
    assert favorite_by_name["Other Contact"] is False


def test_add_unknown_contact_to_favorite_returns_not_found(client):
    response = add_favorite(client, 9999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Contact with ID '9999' not found."


def test_add_contact_to_favorite_twice_returns_bad_request(client, sample_contact):
    contact_id = client.post(
        "/contacts/add_contact", json=sample_contact
    ).json()["data"]["id"]
    add_favorite(client, contact_id)

    response = add_favorite(client, contact_id)

    assert response.status_code == 400
    assert response.json()["detail"] == "Contact is already a favorite."


def test_add_contact_to_favorite_requires_contact_id(client):
    response = client.post("/favorites/add_contact_to_favorite")

    assert response.status_code == 422


def test_view_favorite_contacts_returns_contact_data(client, sample_contact):
    contact_id = client.post(
        "/contacts/add_contact", json=sample_contact
    ).json()["data"]["id"]
    add_favorite(client, contact_id)

    response = client.get("/favorites/view_favorite_contacts")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] is True
    assert body["message"] == "Favorite contacts retrieved successfully."
    assert body["data"][0]["fullname"] == sample_contact["fullname"]
    assert body["data"][0]["is_favorite"] is True

def test_view_favorite_contacts_returns_not_found_when_no_favorites(client):
    response = client.get("/favorites/view_favorite_contacts")

    assert response.status_code == 404
    assert response.json()["detail"] == "No favorite contacts found."

def test_remove_contact_from_favorite_returns_success(client, sample_contact):
    contact_id = client.post(
        "/contacts/add_contact", json=sample_contact
    ).json()["data"]["id"]
    add_favorite(client, contact_id)

    response = client.delete(
        "/favorites/remove_contact_from_favorite",
        params={"contact_id": contact_id},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] is True
    assert body["message"] == "Contact removed from app.favorites successfully."

def test_remove_contact_from_favorite_marks_contact_as_not_favorite(client, sample_contact):
    contact_id = client.post(
        "/contacts/add_contact", json=sample_contact
    ).json()["data"]["id"]
    add_favorite(client, contact_id)

    client.delete(
        "/favorites/remove_contact_from_favorite",
        params={"contact_id": contact_id},
    )

    response = client.get("/contacts/view_contact")
    contacts = response.json()["data"]
    assert contacts[0]["fullname"] == sample_contact["fullname"]
    assert contacts[0]["is_favorite"] is False
