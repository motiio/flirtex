
from pydantic import BaseModel

from src.modules.deck.application.dtos import LikeMessageDTO, MatchMessageDTO


class BaseMessage(BaseModel):
    recipient: str


class LikeMessage(BaseMessage):
    msg_type: str = 'like'
    detail: LikeMessageDTO


class MatchMessage(BaseMessage):
    msg_type: str = 'match'
    detail: MatchMessageDTO
