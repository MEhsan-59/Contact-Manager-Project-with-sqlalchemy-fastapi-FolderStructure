from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_favorite_service, get_group_service
from app.exceptions import ContactNotFoundException
from app.schemas.contact_schema import AddContactSchema, AddContactResponse, ContactResponse
from app.services.group_service import GroupService
router = APIRouter()

@router.post("/create_group", response_model=AddContactResponse)
def create_group(group_name: str, service: GroupService = Depends(get_group_service)):
    result = service.create_group(group_name)
    return result

@router.post("/add_contact_to_group", response_model=ContactResponse)
def add_contact_to_group(group_id: int, contact_id: int, service: GroupService = Depends(get_group_service)):
    try:
        return service.add_contact_to_group(group_id, contact_id)
    except ContactNotFoundException as exc:
        if exc.message == "Group ID not found.":
            raise HTTPException(status_code=400, detail=exc.message) from exc
        raise
    

@router.get("/view_all_groups", response_model=ContactResponse)
def view_all_groups(service: GroupService = Depends(get_group_service)):
    result = service.view_all_groups()
    if not result["status"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.get("/view_group_contacts", response_model=ContactResponse)
def get_group_contacts(group_id: int, service: GroupService = Depends(get_group_service)):
    result = service.view_group_contacts(group_id)
    if not result["status"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result