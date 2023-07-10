from pydantic_core.core_schema import nullable_schema
from src.v1.base.models import Base, TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Enum
from uuid import UUID
import enum


class ProcessStatusEnum(enum.Enum):
    __table_args__ = {"schema": "core"}
    approved = 1
    processing = 0
    rejected = -1


class Photo(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("core.profile.id", ondelete="CASCADE")
    )
    displaying_order: Mapped[int] = mapped_column(Integer)
    status: Mapped[ProcessStatusEnum] = mapped_column(
        Enum(ProcessStatusEnum, schema="core"),
    )
    status_description: Mapped[str] = mapped_column(String(32), nullable=True)
    profile: Mapped["Profile"] = relationship(back_populates="photos")  # type: ignore
    hash: Mapped[str] = mapped_column(String(32), nullable=False)
    short_url: Mapped[str] = mapped_column(String(64), unique=True, nullable=True)
    presigned_url: Mapped[str] = mapped_column(String(512), unique=True, nullable=True)

    def __repr__(self) -> str:
        return f"Photo[{self.id=},{self.displaying_order=}, {self.status=}, {self.status_description=}, {self.photo_url=}]"
