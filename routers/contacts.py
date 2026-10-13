

from fastapi import APIRouter, HTTPException
from typing import Optional
from ..schemas import ContactCreate, ContactUpdate, ContactResponse, ContactCategory
from datetime import datetime

router = APIRouter(prefix="/contacts", tags=["contacts"])

contacts_db: list[dict] = []
next_id = 1

@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):
    """Create a new contact with automatic validation"""
    global next_id
    new_contact = {
        "id": next_id,
        **contact.model_dump(),
        "created_at": datetime.now().isoformat()
    }

    contacts_db.append(new_contact)
    next_id += 1
    return new_contact 

@router.get("/", response_model=list[ContactResponse])
def list_contacts(category: Optional[ContactCategory] = None):
    """List contacts"""
    if category:
        return [
            contact for contact in contacts_db
            if contact["category"] == category 
        ] 
    return contacts_db 


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    for contact in contacts_db: 
        if contact["id"] == contact_id:
            return contact
        
    raise HTTPException(
        status_code=404, 
        detail="Contact not found"
    )


@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, updates: ContactUpdate):
    """Update a contact - only provided fields are changed."""
    for contact in contacts_db:
        if contact["id"] == contact_id:
            update_data = updates.model_dump(exclude_unset=True)
            contact.update(update_data)
            return contact 
    raise HTTPException(
        status_code=404, 
        detail="Contact not found."
    )
                 



