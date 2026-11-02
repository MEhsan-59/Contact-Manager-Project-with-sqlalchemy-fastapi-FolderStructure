from sqlalchemy.orm import Session
from app.exceptions import DuplicateException
from app.models.group_model import Group
from app.models.group_contact_model import GroupContact
from sqlalchemy.exc import IntegrityError

class GroupRepository:
    def __init__(self, db):
        self.db = db

    def create_group(self, group_data):
        new_group = Group(**group_data)
        self.db.add(new_group)
        self.db.commit()
        self.db.refresh(new_group)
        return new_group

    def get_group_by_name(self, group_name):
        return self.db.query(Group).filter(Group.group_name == group_name).first()

    def get_group_by_id(self, group_id):
        return self.db.query(Group).filter(Group.group_id == group_id).first()
    
    def add_contact_to_group(self, group_id, contact_id):
        try:
            group_contact = GroupContact(group_id=group_id, contact_id=contact_id)
            self.db.add(group_contact)
            self.db.commit()
            return group_contact
        except IntegrityError:
            self.db.rollback()
            raise DuplicateException()

    def view_all_groups(self):
        return self.db.query(Group).all()

    def get_group_contact_by_group_id(self, group_id):
        return self.db.query(GroupContact).filter(GroupContact.group_id == group_id).all()

    