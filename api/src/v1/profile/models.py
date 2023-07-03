from __future__ import annotations

import enum
from datetime import date
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.v1.auth.models import User
from src.v1.models import Base, TimeStampMixin


class GenderEnum(enum.Enum):
    __table_args__ = {"schema": "core"}
    male = 1
    female = 0


class LookingGenderEnum(enum.Enum):
    __table_args__ = {"schema": "core"}
    male = 1
    female = 0
    unknown = -1


class ProfileInterests(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    profile_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    interest_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("core.interest.id", ondelete="CASCADE"),
    )


class Interest(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    name: Mapped[str] = mapped_column(String(32), unique=True)
    icon: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return f"Interest[{self.id=}, {self.name=}, {self.icon=}]"


class Profile(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("core.user.id"))
    owner: Mapped["User"] = relationship(back_populates="profile")
    name: Mapped[str] = mapped_column(String(32))
    bio: Mapped[str] = mapped_column(String(600), nullable=True)
    birthdate: Mapped[date] = mapped_column(Date)
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum, schema="core"))
    looking_gender: Mapped[LookingGenderEnum] = mapped_column(
        Enum(LookingGenderEnum, schema="core")
    )
    is_online: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    interests: Mapped[list[Interest]] = relationship(
        secondary="core.profile_interests",
    )
    photos: Mapped[list["ProfilePhoto"]] = relationship(back_populates="profile")

    def __repr__(self):
        return f"Profile[{self.id=}, {self.owner_id=}, {self.name=}, {self.birthdate=}, {self.gender=},]"


class ProfilePhoto(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    profile_id: Mapped[int] = mapped_column(ForeignKey(Profile.id, ondelete="CASCADE"))
    displaying_order: Mapped[int] = mapped_column(Integer)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    profile: Mapped["Profile"] = relationship(back_populates="photos")
    photo_url: Mapped[str] = mapped_column(String(100))
