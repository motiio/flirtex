from typing import Optional

from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.v1.models import Base, TimeStampMixin


class User(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    tg_id: Mapped[int] = mapped_column(Integer, unique=True)
    tg_username: Mapped[str] = mapped_column(String, unique=True)
    tg_first_name: Mapped[str]
    tg_last_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    tg_is_premium: Mapped[Optional[bool]] = mapped_column(default=False)
    tg_language_code: Mapped[Optional[str]] = mapped_column(nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="owner")  # type: ignore # noqa

    def __repr__(self) -> str:
        return f"User[{self.id=}, {self.tg_id=}, {self.tg_username=}]"


class RefreshToken(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    user: Mapped[UUID] = mapped_column(ForeignKey(User.id))
    value: Mapped[str]
    user_agent = Column(String, nullable=False)
