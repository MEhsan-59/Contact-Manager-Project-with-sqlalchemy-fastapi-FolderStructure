from fastapi import Depends
from sqlalchemy.orm import Session
from app.repositories.favorite_repository import FavoriteRepository
from app.services.favorite_service import FavoriteService
from app.core.database import get_db
from app.repositories.contact_repository import ContactRepository
from app.services.contact_service import ContactService
from app.services.group_service import GroupService
from app.repositories.group_repository import GroupRepository

def get_contact_repository(db: Session = Depends(get_db)) -> ContactRepository:
    return ContactRepository(db)

def get_contact_service(repo: ContactRepository = Depends(get_contact_repository)) -> ContactService:
    return ContactService(repo)

def get_favorite_repository(db: Session = Depends(get_db)) -> FavoriteRepository:
    return FavoriteRepository(db)

def get_favorite_service(favorite_repo: FavoriteRepository = Depends(get_favorite_repository), contact_repo: ContactRepository = Depends(get_contact_repository)) -> FavoriteService:
    return FavoriteService(contact_repo, favorite_repo)


def get_group_repository(db: Session = Depends(get_db)) -> GroupRepository:
    return GroupRepository(db)

def get_group_service(group_repo: GroupRepository = Depends(get_group_repository), contact_repo: ContactRepository = Depends(get_contact_repository)) -> GroupService:
    return GroupService(group_repo, contact_repo)
