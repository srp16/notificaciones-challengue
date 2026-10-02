from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationRead
from app.store import add_notification, list_notifications

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("", status_code=201)
def create(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
    ) -> NotificationRead:
    row = Notification(**notification.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.get("") 
def list(
    db: Session = Depends(get_db)
    ) -> list[NotificationRead]:
    rows = db.scalars(select(Notification)).all()
    return list(rows)
    