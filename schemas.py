

from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ContactCategory(str, Enum):
    """Only allow these specific values."""
    personal = "personal"
    work = "work"
    family = "family"


class ContactCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: str
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    category: ContactCategory

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if "@" not in value: 
            raise ValueError("Email must contain @")
        return value

class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email: Optional[str] = None
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    category: Optional[ContactCategory] = None 

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if value is not None and "@" not in value:
            raise ValueError("Email must contain @")
        return value


class ContactResponse(ContactCreate):
    id: int 
    created_at: str




