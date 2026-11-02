from app.exceptions import AppException, ContactNotFoundException, DuplicateException

class GroupService:
    def __init__(self, group_repository, contact_repository):
        self.group_repository = group_repository
        self.contact_repository = contact_repository

    def create_group(self, group_name):
        if self.group_repository.get_group_by_name(group_name):
            return {"status": False, "message": "Group name already exists."}
        group = self.group_repository.create_group(
            {"group_name": group_name}
        )
        return {
            "status": True,
            "message": "Group created successfully.",
            "data": {
                "group_id": group.group_id,
                "group_name": group.group_name
            },
        }

    def get_group_by_name(self, group_name):
        group = self.group_repository.get_group_by_name(group_name)
        if not group:
            return {"status": False, "message": "Group not found."}
        return {
            "status": True,
            "message": "Group retrieved successfully.",
            "data": {
                "id": group.group_id,
                "group_name": group.group_name,
            },
        }

    def add_contact_to_group(self, group_id, contact_id):
        contact = self.contact_repository.get_contact_by_id(contact_id)
        if not contact:
            raise ContactNotFoundException("Contact Id not found.")
        group = self.group_repository.get_group_by_id(group_id)
        if not group:
            raise ContactNotFoundException("Group ID not found.")
        result = self.group_repository.add_contact_to_group(group.group_id, contact.id)
        if not result:
            raise AppException("Failed to add contact to group.")
        return {
            "status": True,
            "message": "Contact added to group successfully.",
            "data": {
                "group_name": group.group_name,
                "contact_fullname": contact.fullname,
            },
        }

    def view_all_groups(self):
        groups = self.group_repository.view_all_groups()
        if not groups:
            return {"status": False, "message": "No groups found."}
        
        group_list = [
            {
                "group_id": group.group_id,
                "group_name": group.group_name,
            }
            for group in groups
        ]
        return {"status": True, "message": "Groups retrieved successfully.", "data": group_list}

    def view_group_contacts(self, group_id):
        group_contacts = self.group_repository.get_group_contact_by_group_id(group_id)
        if not group_contacts:
            return {"status": False, "message": "No contacts found for this group."}
        data = {}
        for group_contact in group_contacts:
            contact = self.contact_repository.get_contact_by_id(group_contact.contact_id)
            if not contact:
                raise ContactNotFoundException("Contact not found.")
            data[contact.fullname] = {
                "id": contact.id,
                "fullname": contact.fullname,
                "phone_number": contact.phone_number,
                "category": contact.category,
                "is_favorite": contact.is_favorite,
            }

        return {"status": True, "message": "Contacts retrieved successfully.", "data": data}