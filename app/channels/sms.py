from datetime import datetime, timezone
import logging
from app.channels.base import NotificationChannel
from app.models.notification import Notification
from app.models.user import User
from app.channels.base import register
from app.schemas.notification import Channel

logger = logging.getLogger(__name__)
_SMS_LIMIT = 160

@register(Channel.sms)
class SmsChannel(NotificationChannel):    
    
    def send(self, notification: Notification, user: User) -> None:
        body = notification.content[:_SMS_LIMIT]
        number = f"+100000{user.id:04d}"
        sent_at =  datetime.now(timezone.utc)
        logger.info(
            "SMS enviado al %s el %s: %s",
            number,
            sent_at.isoformat(),
            body
        )
        