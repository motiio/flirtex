from abc import ABCMeta

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel, metaclass=ABCMeta):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
