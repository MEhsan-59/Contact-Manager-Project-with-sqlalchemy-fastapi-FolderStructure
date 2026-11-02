import pytest

from app.exceptions import AppException, DuplicateException, ContactNotFoundException
from app.repositories.contact_repository import ContactRepository
from app.repositories.favorite_repository import FavoriteRepository
from app.services.favorite_service import FavoriteService


def make_service(db_session):
    contact_repo = ContactRepository(db_session)
    service = FavoriteService(contact_repo, FavoriteRepository(db_session))
    return service, contact_repo


def test_add_contact_to_favorite_marks_contact_as_favorite(db_session, sample_contact):
    service, contact_repo = make_service(db_session)
    contact = contact_repo.add_contact(sample_contact)

    result = service.add_contact_to_favorite(contact.id)

    assert result["status"] is True
    assert result["message"] == "Contact added to favorites successfully."
    saved = contact_repo.get_contact_by_id(contact.id)
    assert saved.is_favorite is True


def test_add_contact_to_favorite_rejects_unknown_contact(db_session):
    service, _ = make_service(db_session)

    with pytest.raises(ContactNotFoundException):
        service.add_contact_to_favorite(9999)


def test_add_contact_to_favorite_rejects_already_favorite(db_session, sample_contact):
    service, contact_repo = make_service(db_session)
    contact = contact_repo.add_contact(sample_contact)
    service.add_contact_to_favorite(contact.id)

    with pytest.raises(DuplicateException, match="already a favorite"):
        service.add_contact_to_favorite(contact.id)

def test_view_favorite_contacts_returns_favorites(db_session, sample_contact):
    service, contact_repo = make_service(db_session)
    contact = contact_repo.add_contact(sample_contact)
    service.add_contact_to_favorite(contact.id)

    result = service.view_favorite_contacts()

    assert result["status"] is True
    assert result["message"] == "Favorite contacts retrieved successfully."
    assert len(result["data"]) == 1
    assert result["data"][0]["fullname"] == sample_contact["fullname"]

def test_view_favorite_contacts_raises_exception_when_no_favorites(db_session):
    service, _ = make_service(db_session)

    with pytest.raises(ContactNotFoundException, match="No favorite contacts found"):
        service.view_favorite_contacts()

def test_add_contact_to_favorite_and_view_favorites(db_session, sample_contact):
    service, contact_repo = make_service(db_session)
    contact = contact_repo.add_contact(sample_contact)

    add_result = service.add_contact_to_favorite(contact.id)
    assert add_result["status"] is True

    view_result = service.view_favorite_contacts()
    assert view_result["status"] is True
    assert len(view_result["data"]) == 1
    assert view_result["data"][0]["fullname"] == sample_contact["fullname"]

def test_remove_contact_from_favorite_marks_contact_as_not_favorite(db_session, sample_contact):
    service, contact_repo = make_service(db_session)
    contact = contact_repo.add_contact(sample_contact)
    service.add_contact_to_favorite(contact.id)

    remove_result = service.remove_contact_from_favorite(contact.id)
    assert remove_result["status"] is True
    assert remove_result["message"] == "Contact removed from app.favorites successfully."

    saved = contact_repo.get_contact_by_id(contact.id)
    assert saved.is_favorite is False 

def test_remove_contact_from_favorite_rejects_unknown_contact(db_session):
    service, _ = make_service(db_session)

    with pytest.raises(ContactNotFoundException):
        service.remove_contact_from_favorite(9999)

def test_remove_contact_from_favorite_rejects_not_favorite(db_session, sample_contact):
    service, contact_repo = make_service(db_session)
    contact = contact_repo.add_contact(sample_contact)

    with pytest.raises(ContactNotFoundException, match="not a favorite"):
        service.remove_contact_from_favorite(contact.id)

def test_add_and_remove_contact_from_favorite(db_session, sample_contact):
    service, contact_repo = make_service(db_session)
    contact = contact_repo.add_contact(sample_contact)

    add_result = service.add_contact_to_favorite(contact.id)
    assert add_result["status"] is True

    remove_result = service.remove_contact_from_favorite(contact.id)
    assert remove_result["status"] is True

    saved = contact_repo.get_contact_by_id(contact.id)
    assert saved.is_favorite is False