from sqlalchemy import UUID, ForeignKey, Integer, Uuid
from sqlalchemy.dialects.postgresql import ENUM as Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import BaseModel, TimeStampMixin
from src.modules.deck.application.utils.enums import LookingGenderEnum


class LikeORM(BaseModel, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    source_profile: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    target_profile: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )


class SkipORM(BaseModel, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    source_profile: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    target_profile: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )


class MatchORM(BaseModel, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    profile_1: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    profile_2: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )


class SaveORM(BaseModel, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    profile_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    saved_profile_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )


class FilterORM(BaseModel, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    looking_gender: Mapped[LookingGenderEnum] = mapped_column(
        Enum(LookingGenderEnum, schema="core", create_type=False),
    )
    age_from: Mapped[int] = mapped_column(Integer)
    age_to: Mapped[int] = mapped_column(Integer)
    max_distance: Mapped[int] = mapped_column(Integer)
    profile_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
