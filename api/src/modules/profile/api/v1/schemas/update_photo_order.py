from uuid import UUID

from pydantic import field_validator

from src.core.schemas import BaseSchema
from src.modules.profile.application.dtos.photo import PhotoOrderDTO
from src.modules.profile.domain.exceptions import InvalidOrderList


class UpdatePhotoOrderRequest(BaseSchema):
    new_order: list[PhotoOrderDTO]

    @field_validator("new_order")
    def check_order(cls, v):
        if not v:
            raise InvalidOrderList

        orders = sorted([order.displaying_order for order in v])
        first = orders[0]
        last = orders[-1]
        n = len(orders)

        expected_sum = (n * (first + last)) // 2
        actual_sum = sum(orders)

        if not expected_sum == actual_sum:
            raise InvalidOrderList
        return v
