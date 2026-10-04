from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.schemas.notification import Channel


class Notification(Base):
    __tablename__ = "notifications"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(String)
    channel: Mapped[Channel] = mapped_column(Enum(Channel, native_enum=False, length=20))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))