import re
from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declarative_base, declared_attr, mapped_column


def resolve_table_name(name) -> str:
    """Resolves table names to their mapped names."""
    if name.endswith("ORM"):
        name = name[:-3]
    names = re.split("(?=[A-Z])", name)  # noqa
    table_name = "_".join([x.lower() for x in names if x])

    return table_name


class CustomBase:
    __repr_attrs__: list = []
    __repr_max_length__: int = 15
    __name__: str
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        sort_order=-10,
    )

    def dict(self):
        """Returns a dict representation of a model."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # type: ignore

    @declared_attr  # type: ignore
    def __tablename__(self) -> str:
        return resolve_table_name(self.__name__)

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__

        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError(
                    "{} has incorrect attribute '{}' in "
                    "__repr__attrs__".format(self.__class__, key)
                )
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, str)

            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + "..."

            if wrap_in_quote:
                value = "'{}'".format(value)
            values.append(value if single else "{}:{}".format(key, value))

        return " ".join(values)


BaseModel = declarative_base(cls=CustomBase)


class TimeStampMixin:
    """Timestamping mixin"""

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, sort_order=9998)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, sort_order=9999)

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)
