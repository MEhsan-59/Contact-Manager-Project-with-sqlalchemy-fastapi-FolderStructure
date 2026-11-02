from app.exceptions import AppException, ContactNotFoundException, DuplicateException

class ContactService:
    def __init__(self, contact_repository):
        self.contact_repo = contact_repository

    def add_contact(self, contact_data):
        saved_contact = self.contact_repo.add_contact(contact_data)

        data = {
            "id": saved_contact.id,
            "fullname": saved_contact.fullname,
            "phone_number": saved_contact.phone_number,
            "category": saved_contact.category,
            "is_favorite": saved_contact.is_favorite,
        }
        return {"status": True, "message": "Contact added successfully", "data": data}

    def view_all_contact(self):
        contacts = self.contact_repo.get_all_contacts()
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
        return {"status": True, "message": "Contacts retrieved successfully", "data": data}

    def view_contact_by_name_or_phone(self, name: str | None = None, phone_number: str | None = None):
        if not name and not phone_number:
            return {"status": False, "message": "Please provide either name or phone number."}

        contacts = self.contact_repo.search_contacts(name, phone_number)
        filtered_contacts = [
            {
                "id": contact.id,
                "fullname": contact.fullname,
                "phone_number": contact.phone_number,
                "category": contact.category, 
                "is_favorite": contact.is_favorite,
            }
            for contact in contacts
        ]
        if not filtered_contacts:
            return {"status": False, "message": "No contacts found with the provided criteria."}

        return {"status": True, "message": "Contacts retrieved successfully", "data": filtered_contacts}

    def delete_contact(self, contact_id: int):
        contact = self.contact_repo.get_contact_by_id(contact_id)
        if not contact:
            raise ContactNotFoundException()
        self.contact_repo.delete_contact(contact)
        return {"status": True, "message": "Contact deleted successfully."}

    def update_contact(self, contact_id: int, contact_data: dict):
        contact = self.contact_repo.get_contact_by_id(contact_id)
        if not contact:
            raise ContactNotFoundException(f"Contact with ID '{contact_id}' not found.")
        new_name = contact_data.get("fullname")
        if new_name and new_name != contact.fullname:
            existing = self.contact_repo.get_contact_by_fullname(new_name)
            if existing and existing.id != contact.id:
                raise DuplicateException(message=f"Contact with name '{new_name}' already exists.")
        updated = self.contact_repo.update_contact(contact, contact_data)
        return {
            "status": True,
            "message": "Contact updated successfully.",
            "data": {
                "id": updated.id,
                "fullname": updated.fullname,
                "phone_number": updated.phone_number,
                "category": updated.category,
                "is_favorite": updated.is_favorite,
            },
        }