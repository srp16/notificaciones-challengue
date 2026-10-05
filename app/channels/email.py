import logging
import re
from app.channels.base import NotificationChannel
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import Channel
from app.channels.base import register

logger= logging.getLogger(__name__)
_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@register(Channel.email)
class EmailChannel(NotificationChannel):
    
    def send(self, notification: Notification, user: User) -> None:
        if not _EMAIL.match(user.email):
            raise ValueError("Destinatario de email invalido")
        
        template = f"Para: {user.email}\nAsunto: {notification.title}\n\n{notification.content}"
        logger.info("Email enviado  a %s: %s", user.email, template)