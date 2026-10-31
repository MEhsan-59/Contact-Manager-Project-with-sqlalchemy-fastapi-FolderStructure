from exceptions import ContactNotFoundException

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
            "favorite": saved_contact.favorite,
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
                "favorite": contact.favorite,
            }
            for contact in contacts
        ]
        return {"status": True, "message": "Contacts retrieved successfully", "data": data}

    def view_contact_by_name_or_phone(self, name: str | None = None, phone_number: str | None = None):
        if not name and not phone_number:
            return {"status": False, "message": "Please provide either name or phone number."}

        contacts = self.contact_repo.search_contacts(name, phone_number)
        print(phone_number, type(phone_number))
        filtered_contacts = [
            {
                "id": contact.id,
                "fullname": contact.fullname,
                "phone_number": contact.phone_number,
                "category": contact.category, 
                "favorite": contact.favorite,
            }
            for contact in contacts
        ]
        print(filtered_contacts)

        if not filtered_contacts:
            return {"status": False, "message": "No contacts found with the provided criteria."}

        return {"status": True, "message": "Contacts retrieved successfully", "data": filtered_contacts}

    def delete_contact(self, fullname: str):
        contact = self.contact_repo.get_contact_by_fullname(fullname)
        if not contact:
            raise ContactNotFoundException()

        self.contact_repo.delete_contact(contact)
        return {"status": True, "message": "Contact deleted successfully."}