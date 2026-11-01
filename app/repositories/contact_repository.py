from sqlalchemy.orm import Session
from app.models.contact import Contact
from  sqlalchemy import or_

class ContactRepository:
    def __init__(self, db : Session):
        self.db = db

    def add_contact(self, contact_data):
        new_contact = Contact(**contact_data)
        self.db.add(new_contact)
        self.db.commit()
        return new_contact

    def get_all_contacts(self):
        return self.db.query(Contact).all()

    def search_contacts(self, name: str | None = None, phone_number: str | None = None):
        conditions = []
        if name:
            conditions.append(Contact.fullname.ilike(f"%{name}%"))
        if phone_number:
            conditions.append(Contact.phone_number.ilike(f"%{phone_number}%"))
        if not conditions:
            return []
        return self.db.query(Contact).filter(or_(*conditions)).all()

    def get_contact_by_fullname(self, fullname: str):
        return self.db.query(Contact).filter(Contact.fullname == fullname).first()

    def get_contact_by_id(self, contact_id: int):
        return self.db.query(Contact).filter(Contact.id == contact_id).first()
    
    def delete_contact(self, contact: Contact):
        self.db.delete(contact)
        self.db.commit()