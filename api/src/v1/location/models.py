from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.v1.base.models import Base, TimeStampMixin
from geoalchemy2 import Geography
from src.v1.profile.utils.geo.models import Point
from sqlalchemy import (
    ForeignKey,
    Uuid,
)


class ProfileLocation(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    profile_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("core.interest.id", ondelete="CASCADE")
    )
    profilt: Mapped["Profile"] = relationship(back_populates="Profile")
    point: Mapped[Point] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )
