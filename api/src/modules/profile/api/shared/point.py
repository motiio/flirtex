from pydantic import field_validator

import src.modules.profile.application.utils as utils
from src.core.schemas import BaseSchema
from src.modules.profile.domain.exceptions import InvalidLatitude, InvalidLongitude


class DistortedPointSchema(BaseSchema):
    longitude: float
    latitude: float

    @field_validator("longitude")
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise InvalidLongitude

        distorted_longitude = round(utils.geo.add_random_offset(v), 3)
        return distorted_longitude

    @field_validator("latitude")
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise InvalidLatitude

        distorted_latitude = round(utils.geo.add_random_offset(v), 3)
        return distorted_latitude
