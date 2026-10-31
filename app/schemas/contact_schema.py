import re

from pydantic import BaseModel, ConfigDict, Field, field_validator
from core.enums import CategoryEnum

class AddContactSchema(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    fullname: str = Field(max_length=100)
    phone_number: str = Field(max_length=20)
    category: CategoryEnum
    favorite: bool = False

    @field_validator("phone_number", "fullname")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Any field can not be empty")
        return v.strip()

    @field_validator("phone_number")
    @classmethod
    def valid_phone(cls, v: str) -> str:
        cleaned = v.replace(" ", "").replace("-", "")
        if not re.fullmatch(r"\+?\d{1,15}", cleaned):
            raise ValueError("Phone number must have 7 to 15 digits (+ allowed at the start)")
        return v

class AddContactResponse(BaseModel):
    status: bool
    message: str
    data: dict | None = None

class ContactResponse(BaseModel):
    status: bool
    message: str
    data: dict | list[dict] = None