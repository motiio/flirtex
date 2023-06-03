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
from sqlalchemy.orm import relationship

from src.config.models import Base, TimeStampMixin


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
    profile_id = Column(Integer, ForeignKey("core.profile.id"))
    interest_id = Column(Integer, ForeignKey("core.interest.id"))


class Interest(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}

    id = Column(
        Integer,
        Sequence("interest_seq", start=1, schema="core"),
        primary_key=True,
    )
    name = Column(String(32), unique=True)
    description = Column(Text)
    profiles = relationship(
        "Profile", secondary="core.profile_interests", back_populates="interests"
    )


class Profile(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    id = Column(
        Integer,
        Sequence("profile_seq", start=1, schema="core"),
        primary_key=True,
    )
    owner = Column(Integer, ForeignKey("core.user.id"))
    name = Column(String(32))
    birthdate = Column(Date)
    # city = Column(Integer, ForeignKey("core.city.id"), comment="Profile settlement")
    gender = Column(Enum(GenderEnum, schema="core"))
    looking_gender = Column(Enum(GenderEnum, schema="core"))
    is_active = Column(Boolean, nullable=False)
    interests = relationship(
        "Interest",
        secondary="core.profile_interests",
        back_populates="profiles",
    )

    def __repr__(self):
        return f"Profile[{self.id=}, {self.owner=}, {self.name=}, {self.birthdate=}, {self.gender}]"


class ProfilePhoto(Base, TimeStampMixin):
    __table_args__ = {"schema": "core"}
    id = Column(
        Integer,
        Sequence("profile_photo_seq", start=1, schema="core"),
        primary_key=True,
    )
    profile = Column(Integer, ForeignKey(Profile.id))
    s3_path = Column(String(128))
    display_order = Column(Integer)
    is_valid = Column(Boolean)
