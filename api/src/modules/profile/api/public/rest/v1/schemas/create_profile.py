from datetime import date
from uuid import UUID

from pydantic import Field, field_validator
from pydantic.fields import computed_field

import src.modules.profile.api.shared as shared
from core.schemas import BaseSchema
from src.modules.deck.application.dtos.filter import FilterOutDTO
from src.modules.deck.application.utils import enums as deck_enums
from src.modules.profile.application.dtos.profile import ProfileOutDTO
from src.modules.profile.application.utils import enums as profile_enums
from src.modules.profile.domain.entities import Profile


class CreateProfileRequestSchema(BaseSchema):
    name: str = Field(max_length=32)
    birthdate: date
    gender: profile_enums.GenderEnum
    bio: str | None = Field("", max_length=600)
    interests: list[UUID] | None = None
    location: shared.DistortedPointSchema | None = None

    @field_validator("birthdate")
    def check_legal_age(cls, v):
        years_from_born = Profile._calculate_age(birthdate=v)
        if years_from_born < 18:
            raise ValueError("Your age must be 18+")
        elif years_from_born > 100:
            raise ValueError("You're too old, sorry")
        return v

    @field_validator("interests")
    def check_interests_len(cls, v):
        if v is None:
            return v

        if 0 < len(v) < 8:
            return v

        raise ValueError("Invaled number of interests. Must be [1, 7]")

    @computed_field
    @property
    def looking_gender(self) -> deck_enums.LookingGenderEnum:
        return (
            deck_enums.LookingGenderEnum.female
            if self.gender == 0
            else deck_enums.LookingGenderEnum.male
        )


class ProfileResponseSchema(BaseSchema):
    profile: ProfileOutDTO
    filter: FilterOutDTO
