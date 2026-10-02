from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class Channel(str, Enum):
    email = "email"
    sms = "sms"
    push = "push"

class NotificationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    channel: Channel
    
class NotificationRead(NotificationCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int