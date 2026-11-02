import pytest

from app.core.enums import CategoryEnum
from app.exceptions import ContactNotFoundException
from app.repositories.contact_repository import ContactRepository
from app.repositories.group_repository import GroupRepository
from app.services.group_service import GroupService

def make_service(db_session, sample_contact=None):
    contact_repo = ContactRepository(db_session)
    contact = contact_repo.add_contact(sample_contact) if sample_contact else None
    service = GroupService(GroupRepository(db_session), contact_repo)
    return service, contact

def test_add_contact_to_group_returns_success(db_session, sample_contact):
    service, contact = make_service(db_session, sample_contact)
    group_result = service.create_group("Friends")
    group_id = group_result["data"]["group_id"]

    result = service.add_contact_to_group(group_id, contact.id)

    assert result["status"] is True
    assert result["data"]["group_name"] == "Friends"
    assert result["data"]["contact_fullname"] == contact.fullname

def test_add_contact_to_group_with_wrong_contact_id(db_session, sample_contact):
    service, contact = make_service(db_session, sample_contact)
    result = service.create_group("Friends")
    group_id = result["data"]["group_id"]

    with pytest.raises(ContactNotFoundException):
        service.add_contact_to_group(group_id, 1234)

def test_add_contact_to_group_with_wrong_group_id(db_session, sample_contact):
    service, contact = make_service(db_session, sample_contact)
    with pytest.raises(Exception):
        service.add_contact_to_group(9999, contact.id)

def test_create_group_with_existing_name(db_session, sample_contact):
    service, contact = make_service(db_session, sample_contact)
    service.create_group("Friends")
    result = service.create_group("Friends")

    assert result["status"] is False
    assert result["message"] == "Group name already exists."

def test_create_group_with_new_name(db_session, sample_contact):
    service, contact = make_service(db_session, sample_contact)
    result = service.create_group("Family")

    assert result["status"] is True
    assert result["message"] == "Group created successfully."
    assert result["data"]["group_name"] == "Family"


def test_view_all_groups_empty(db_session):
    service, _ = make_service(db_session)
    result = service.view_all_groups()

    assert result["status"] is False
    assert result["message"] == "No groups found."

def test_view_all_groups_with_data(db_session, sample_contact):
    service, contact = make_service(db_session, sample_contact)
    service.create_group("Friends")
    service.create_group("Family")

    result = service.view_all_groups()

    assert result["status"] is True
    assert len(result["data"]) == 2
    group_names = [group["group_name"] for group in result["data"]]
    assert "Friends" in group_names
    assert "Family" in group_names

def test_view_group_contacts_with_no_contacts(db_session, sample_contact):
    service, contact = make_service(db_session, sample_contact)
    group_result = service.create_group("Friends")
    group_id = group_result["data"]["group_id"]

    result = service.view_group_contacts(group_id)

    assert result["status"] is False
    assert result["message"] == "No contacts found for this group."

def test_get_group_by_name_existing(db_session, sample_contact):
    service, contact = make_service(db_session, sample_contact)
    service.create_group("Friends")

    result = service.get_group_by_name("Friends")

    assert result["status"] is True
    assert result["data"]["group_name"] == "Friends"

def test_get_group_by_name_non_existing(db_session, sample_contact):
    service, contact = make_service(db_session, sample_contact)

    result = service.get_group_by_name("NonExistingGroup")

    assert result["status"] is False
    assert result["message"] == "Group not found."