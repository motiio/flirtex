from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.v1.base.models import Base, TimeStampMixin


class Like(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    source_profile: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    target_profile: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )


class Skip(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    source_profile: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    target_profile: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )


class Match(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    profile_1: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    profile_2: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )


class Save(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    profile_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
    saved_profile_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("core.profile.id", ondelete="CASCADE"),
    )
