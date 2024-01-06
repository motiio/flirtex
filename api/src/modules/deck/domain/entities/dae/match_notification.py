from dataclasses import dataclass
from typing import Literal

from src.core.types import BaseNotification


@dataclass
class MatchNotification(
    BaseNotification[Literal["match"]],
):
    pass
