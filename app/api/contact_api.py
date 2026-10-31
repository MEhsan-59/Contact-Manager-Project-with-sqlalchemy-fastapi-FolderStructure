from fastapi import APIRouter, Depends, HTTPException
from api.deps import get_contact_service
from services.contact_service import ContactService
from schemas.contact_schema import AddContactSchema, AddContactResponse, ContactResponse
router = APIRouter()

@router.post("/add_contact", response_model=AddContactResponse)
def add_contact(
    contact_data: AddContactSchema,
    service: ContactService = Depends(get_contact_service),):
    return service.add_contact(contact_data.model_dump())

@router.get("/view_contact", response_model=ContactResponse)
def view_contact(service: ContactService = Depends(get_contact_service)):
    result = service.view_all_contact()

    if not result["status"]:
        raise HTTPException(status_code=404, detail=result["message"])    
    return result

@router.get("/view_contact_by_name_or_phone", response_model=ContactResponse)
def view_contact_by_name_or_phone(name: str | None = None, phone_number: str | None = None, service: ContactService = Depends(get_contact_service)):
    result = service.view_contact_by_name_or_phone(name, phone_number)
    print(result)
    if not result["status"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.delete("/delete_contact", response_model=ContactResponse)
def delete_contact(fullname: str, service: ContactService = Depends(get_contact_service)):
    return service.delete_contact(fullname)