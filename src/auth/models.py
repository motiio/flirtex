from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Sequence, String

from src.config.core import Settings, get_settings
from src.config.models import Base, TimeStampMixin


class User(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    __tablename__ = "user"
    id = Column(
        Integer,
        Sequence("user_seq", start=1, schema="core"),
        primary_key=True,
    )
    tg_id = Column(Integer, unique=True)
    tg_username = Column(String, unique=True)
    tg_first_name = Column(String)
    tg_last_name = Column(String)
    tg_is_premium = Column(Boolean)
    tg_language_code = Column(String)

    @property
    def access_token(self, settings: Settings = get_settings()):
        now = datetime.utcnow()
        exp = (now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS)).timestamp()
        data = {
            "exp": exp,
            "sub": str(self.id),
        }
        return jwt.encode(data, settings.JWT_SECRET, algorithm="HS256")


class DeviceSession(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    id = Column(
        Integer,
        Sequence("device_session_seq", start=1, schema="core"),
        primary_key=True,
    )
    user = Column(Integer, ForeignKey(User.id))
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    user_agent = Column(String, nullable=False)
