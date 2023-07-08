from sqlalchemy import (
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.v1.base.models import Base, TimeStampMixin


class Interest(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    name: Mapped[str] = mapped_column(String(32), unique=True)
    icon: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return f"Interest[{self.id=}, {self.name=}, {self.icon=}]"
