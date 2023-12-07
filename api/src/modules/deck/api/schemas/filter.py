from pydantic import field_validator, model_validator

from src.config.settings import settings
from src.core.schemas import BaseSchema
from src.modules.deck.application.utils import enums


class UpdateFilterRequestSchema(BaseSchema):
    age_from: int
    age_to: int
    max_distance: int
    looking_gender: enums.LookingGenderEnum

    @model_validator(mode="after")
    def check_fields(self) -> "UpdateFilterRequestSchema":
        if self.age_to < self.age_from:
            raise ValueError("Invalid age_from value. Must be > age_from")

        if self.age_from > self.age_to:
            raise ValueError("Invalid age_to value. Must be < age_from")

        self.age_to = (
            settings.MAX_PROFILE_AGE if self.age_to > settings.MAX_PROFILE_AGE else self.age_to
        )

        self.age_from = (
            settings.MIN_PROFILE_AGE if self.age_from < settings.MIN_PROFILE_AGE else self.age_from
        )
        return self

    @field_validator("max_distance")
    def check_max_distance(cls, v):
        if v < settings.MIN_FILTER_DISTANCE:
            raise ValueError("Max distance must by > 5")

        if v > settings.MAX_FILTER_DISTANCE:
            return settings.MAX_FILTER_DISTANCE
        return v
