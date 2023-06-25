from __future__ import annotations

import enum

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    Sequence,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.models import User
from src.config.models import Base, TimeStampMixin
from src.s3.core import s3_session
from src.config.core import settings


class GenderEnum(enum.Enum):
    __table_args__ = {"schema": "core"}
    male = 1
    female = 0
    unknown = -1


class ProfileInterests(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    id = Column(
        Integer,
        Sequence("profile_interests_seq", start=1, schema="core"),
        primary_key=True,
    )
    profile_id = Column(Integer, ForeignKey("core.profile.id", ondelete="CASCADE"))
    interest_id = Column(Integer, ForeignKey("core.interest.id", ondelete="CASCADE"))


class Interest(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    id = Column(
        Integer,
        Sequence("interest_seq", start=1, schema="core"),
        primary_key=True,
    )
    name = Column(String(32), unique=True)
    description = Column(Text)


class Profile(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    id = Column(
        Integer,
        Sequence("profile_seq", start=1, schema="core"),
        primary_key=True,
    )
    # owner = Column(Integer, ForeignKey("core.user.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("core.user.id"))
    owner: Mapped["User"] = relationship(back_populates="profile")
    name = Column(String(32))
    birthdate = Column(Date)
    gender = Column(Enum(GenderEnum, schema="core"))
    looking_gender = Column(Enum(GenderEnum, schema="core"))
    is_active = Column(Boolean, nullable=False, default=False)
    interests: Mapped[list[Interest]] = relationship(secondary="core.profile_interests")
    photos: Mapped[set["ProfilePhoto"]] = relationship(back_populates="profile")

    def __repr__(self):
        return f"Profile[{self.id=}, {self.owner=}, {self.name=}, {self.birthdate=}, {self.gender=},]"


class ProfilePhoto(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    id = Column(
        Integer,
        Sequence("profile_photo_seq", start=1, schema="core"),
        primary_key=True,
    )
    profile_id: Mapped[int] = mapped_column(ForeignKey(Profile.id, ondelete="CASCADE"))
    displaying_order = Column(Integer)
    is_valid = Column(Boolean, default=False)
    profile: Mapped["Profile"] = relationship(back_populates="photos")

    @property
    async def photo_url(self) -> str:
        async with s3_session.resource(
            "s3",
            endpoint_url="https://storage.yandexcloud.net",
        ) as s3:
            presigned_url = await s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": settings.S3_PROFILES_BUCKET_NAME,
                    "Key": f"{self.profile_id}/photos/approved/{self.id}",
                },
                ExpiresIn=100,
            )
        return presigned_url
