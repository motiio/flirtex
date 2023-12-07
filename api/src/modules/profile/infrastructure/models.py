from datetime import date
from typing import cast
from uuid import UUID

from geoalchemy2 import Geometry, WKBElement
from geoalchemy2.shape import to_shape
from sqlalchemy import Date, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.dialects.postgresql import ENUM as Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.modules.profile.domain.entities.types as types
from src.core.models import BaseModel, TimeStampMixin
from src.modules.profile.application.utils.enums import (
    GenderEnum,
    PhotoProcessStatusEnum,
)


class InterestORM(BaseModel, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    name: Mapped[str] = mapped_column(String(32), unique=True)
    icon: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return f"Interest[{self.id=}, {self.name=}, {self.icon=}]"


class ProfileInterestsORM(BaseModel, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    profile_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    interest_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("core.interest.id", ondelete="CASCADE"),
    )


class ProfileORM(BaseModel, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("core.user.id"))
    name: Mapped[str] = mapped_column(String(32))
    bio: Mapped[str] = mapped_column(String(600), nullable=True)
    birthdate: Mapped[date] = mapped_column(Date)
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum, schema="core"))
    interests: Mapped[list[InterestORM]] = relationship(
        secondary="core.profile_interests", lazy="selectin"
    )
    photos: Mapped[list["PhotoORM"]] = relationship(
        back_populates="profile", lazy="selectin", order_by="PhotoORM.displaying_order"
    )

    location: Mapped["WKBElement"] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326), nullable=True
    )

    @property
    def dict_location(
        self,
    ):
        if self.location is None:
            return None

        shply_geom = to_shape(self.location)
        coordinates = shply_geom.coords[0]
        return cast(types.Location, {"longitude": coordinates[0], "latitude": coordinates[1]})

    def __repr__(self):
        return f"Profile[{self.id=}, {self.owner_id=}, {self.name=}, {self.birthdate=}, {self.gender=}, Interests={','.join([interest.name for interest in self.interests])}]"


class PhotoORM(BaseModel, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    profile_id: Mapped[UUID] = mapped_column(ForeignKey("core.profile.id", ondelete="CASCADE"))
    displaying_order: Mapped[int] = mapped_column(Integer)
    status: Mapped[PhotoProcessStatusEnum] = mapped_column(
        Enum(PhotoProcessStatusEnum, schema="core"),
    )
    status_description: Mapped[str] = mapped_column(String(32), nullable=True)
    profile: Mapped["ProfileORM"] = relationship(back_populates="photos")  # type: ignore
    hash: Mapped[str] = mapped_column(String(32), nullable=False)
    url: Mapped[str] = mapped_column(String(512), unique=True, nullable=True)
    geo = (Geometry(geometry_type="POINT", srid=4326),)

    def __repr__(self) -> str:
        return f"Photo[{self.id=},{self.displaying_order=}, {self.status=}, {self.status_description=}, {self.photo_url=}]"
