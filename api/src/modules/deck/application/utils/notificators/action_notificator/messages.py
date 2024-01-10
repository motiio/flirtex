from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from src.modules.deck.application.dtos import LikeMessageDTO, MatchMessageDTO, SkipMessageDTO


class BaseActionMessage(BaseModel):
    recipient: UUID
    message_type: Literal["like", "match", "skip"]


class LikeMessage(BaseActionMessage):
    detail: LikeMessageDTO


class MatchMessage(BaseActionMessage):
    detail: MatchMessageDTO


class SkipMessage(BaseActionMessage):
    detail: SkipMessageDTO
