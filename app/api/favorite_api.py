from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_favorite_service
from app.services.favorite_service import FavoriteService
from app.services.contact_service import ContactService
from app.schemas.contact_schema import AddContactSchema, AddContactResponse, ContactResponse
router = APIRouter()

@router.post("/add_contact_to_favorite", response_model=AddContactResponse)
def add_contact_to_favorite(
    contact_id: int,
    service: FavoriteService = Depends(get_favorite_service),):
    return service.add_contact_to_favorite(contact_id)

@router.get("/view_favorite_contacts", response_model=ContactResponse)
def view_favorite_contacts(
    service: FavoriteService = Depends(get_favorite_service),):
    result = service.view_favorite_contacts()
    return result

@router.delete("/remove_contact_from_favorite", response_model=AddContactResponse)
def remove_contact_from_favorite(contact_id: int, service: FavoriteService = Depends(get_favorite_service)):
    return service.remove_contact_from_favorite(contact_id)

    