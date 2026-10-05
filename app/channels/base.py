from abc import ABC, abstractmethod

from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import Channel

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification, user: User) -> None:
        pass
    
_channels: dict[Channel, NotificationChannel] = {}

def register(channel: Channel):
    def decorator(cls):
        _channels[channel] = cls()
        return cls
    return decorator

def get_channel(channel: Channel) -> NotificationChannel:
    return _channels[channel]