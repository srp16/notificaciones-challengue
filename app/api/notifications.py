from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationRead

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("", status_code=201)
def create(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
    ) -> NotificationRead:
    row = Notification(**notification.model_dump())
    row.user_id = user.id
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.get("") 
def list_notifications(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
    ) -> list[NotificationRead]:
    rows = db.scalars(select(Notification).where(Notification.user_id == user.id)).all()
    return list(rows)
    
@router.put("/{notification_id}")
def update(
    notification_id: int,
    data: NotificationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
) -> NotificationRead:
    row = db.scalar(
        select(Notification).where(
            Notification.id == notification_id, 
            Notification.user_id == user.id
            )
        )
    if row is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    row.title = data.title
    row.content = data.content
    row.channel = data.channel
    db.commit()
    return row

    