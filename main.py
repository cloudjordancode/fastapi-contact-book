

from fastapi import FastAPI
from .routers import contacts

app = FastAPI(title="Contact Book API")

app.include_router(contacts.router)