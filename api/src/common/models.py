from sqlalchemy import Column, ForeignKey, Integer, Sequence, String

from api.src.config.models import Base, TimeStampMixin


class Region(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    id = Column(
        Integer,
        Sequence("region_seq", start=1),
        primary_key=True,
    )
    name = Column(String(32))
    type = Column(String(8))
    country_code = Column(String(8))


class City(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    id = Column(
        Integer,
        Sequence("city_seq", start=1),
        primary_key=True,
    )
    level_name = Column(String(32))
    region = Column(Integer, ForeignKey(Region.id), nullable=True)
    name = Column(String(32))
    type = Column(String(16))

    # latitude_dd = Column(String)
    # longitude_dd = Column(String)

    def __repr__(self):
        return f"City[{self.id=}, {self.name = }"
