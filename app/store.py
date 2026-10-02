from app.schemas.notification import NotificationCreate, NotificationRead

notifications: list[NotificationRead] = []

def add_notification(data: NotificationCreate) -> NotificationRead:
    item = NotificationRead(id=len(notifications) + 1, **data.model_dump())
    notifications.append(item)
    return item

def list_notifications() -> list[NotificationRead]:
    return notifications