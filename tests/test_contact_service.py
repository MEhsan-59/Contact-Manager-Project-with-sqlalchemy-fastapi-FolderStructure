import pytest

from app.core.enums import CategoryEnum
from app.exceptions import ContactNotFoundException
from app.repositories.contact_repository import ContactRepository
from app.services.contact_service import ContactService  


def test_add_contact_returns_saved_contact(db_session, sample_contact):
    service = ContactService(ContactRepository(db_session))

    result = service.add_contact(sample_contact)

    assert result["status"] is True
    assert result["data"]["fullname"] == sample_contact["fullname"]
    assert result["data"]["category"] == CategoryEnum.FAMILY.value


def test_search_requires_name_or_phone(db_session):
    service = ContactService(ContactRepository(db_session))

    result = service.view_contact_by_name_or_phone()

    assert result == {
        "status": False,
        "message": "Please provide either name or phone number.",
    }


def test_delete_unknown_contact_raises_not_found(db_session):
    service = ContactService(ContactRepository(db_session))

    with pytest.raises(ContactNotFoundException):
        service.delete_contact("Missing Contact")