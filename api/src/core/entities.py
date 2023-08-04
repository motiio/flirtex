from dataclasses import asdict, dataclass
from uuid import UUID


@dataclass
class BaseEntity:
    id: UUID

    def model_dump(self, exclude: set[str] | None = None):
        if exclude is None:
            exclude = set()

        return {key: value for key, value in asdict(self).items() if key not in exclude}
