import app.channels
import logging

from fastapi import FastAPI
from app.api.notifications import router as notifications_router
from app.api.user import router as users_router

logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.include_router(notifications_router)
app.include_router(users_router)

@app.get("/health")
def health():
    return  {"status": "ok"}