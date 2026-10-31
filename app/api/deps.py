from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.contact_repository import ContactRepository
from services.contact_service import ContactService


def get_contact_service(db: Session = Depends(get_db)):
    repo = ContactRepository(db)
    return ContactService(repo)