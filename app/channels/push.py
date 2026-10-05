import logging
import re
from app.channels.base import NotificationChannel
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import Channel
from app.channels.base import register

logger= logging.getLogger(__name__)
_TOKEN = re.compile(r"^[A-Za-z0-9_-]{16,}$")

@register(Channel.push)
class PushChannel(NotificationChannel):
    
    def send(self, notification: Notification, user: User) -> None:
        token = f"device-{user.id:04d}-token"
        if not _TOKEN.match(token):
            raise ValueError("Token de dispositivo invalido")
        
        payload = {
            "to": token,
            "title": notification.title,
            "body": notification.content
        }
        logger.info("Push enviado. estado = sent payload=%s", payload)