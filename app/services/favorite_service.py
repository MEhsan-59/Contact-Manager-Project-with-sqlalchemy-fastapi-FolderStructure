from app.repositories import contact_repository
from app.services.contact_service import ContactService
from app.repositories.favorite_repository import FavoriteRepository
from app.exceptions import ContactError, ContactNotFoundException

class FavoriteService:
    def __init__(self, contact_repo: contact_repository.ContactRepository, favorite_repo: FavoriteRepository):
        self.contact_repo = contact_repo
        self.favorite_repo = favorite_repo

    def add_contact_to_favorite(self, contact_id: int):
        contact = self.contact_repo.get_contact_by_id(contact_id)
        if not contact:
            raise ContactNotFoundException(f"Contact with contact_id '{contact_id}' not found.")
        if contact.is_favorite:
            raise ContactError("Contact is already a favorite.")

        self.favorite_repo.add_contact_to_favorite(contact)
        return {"status": True, "message": "Contact added to favorites successfully."}

    def remove_contact_from_favorite(self, contact_id: int):
        contact = self.contact_repo.get_contact_by_id(contact_id)
        if not contact:
            raise ContactNotFoundException(f"Contact with contact_id '{contact_id}' not found.")
        if not contact.is_favorite:
            raise ContactError("Contact is not a favorite.")

        self.favorite_repo.remove_contact_from_favorite(contact)
        return {"status": True, "message": "Contact removed from app.favorites successfully."}

    def view_favorite_contacts(self):
        contacts = self.favorite_repo.view_favorite_contacts()
        if not contacts:
            raise ContactNotFoundException("No favorite contacts found.")

        data = [
            {
                "id": contact.id,
                "fullname": contact.fullname,
                "phone_number": contact.phone_number,
                "category": contact.category,
                "is_favorite": contact.is_favorite,
            }
            for contact in contacts
        ]
        return {
            "status": True,
            "message": "Favorite contacts retrieved successfully.",
            "data": data,
        }