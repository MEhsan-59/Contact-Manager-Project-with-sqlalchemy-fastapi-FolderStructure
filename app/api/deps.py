from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.favorite_repository import FavoriteRepository
from app.services.favorite_service import FavoriteService
from app.core.database import get_db
from app.repositories.contact_repository import ContactRepository
from app.services.contact_service import ContactService


def get_contact_service(db: Session = Depends(get_db)):
    repo = ContactRepository(db)
    return ContactService(repo)

def get_favorite_service(db: Session = Depends(get_db)):
    contact_repo = ContactRepository(db)
    favorite_repo = FavoriteRepository(db)
    return FavoriteService(contact_repo, favorite_repo)