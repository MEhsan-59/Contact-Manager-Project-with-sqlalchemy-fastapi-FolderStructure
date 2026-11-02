from sqlalchemy.orm import Session
from app.models.contact_model import Contact


class FavoriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_contact_to_favorite(self, contact):
        contact.is_favorite = True
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def view_favorite_contacts(self):
        return self.db.query(Contact).filter(Contact.is_favorite == True).all()

    def remove_contact_from_favorite(self, contact):
        contact.is_favorite = False
        self.db.commit()
        self.db.refresh(contact)
        return contact