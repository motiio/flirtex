__all__ = [
    "IProfileRepository",
    "IInterestRepository",
    "IProfilePhotoS3Repository",
    "IProfilePhotoRepository",
]

from .profile import IProfileRepository
from .interest import IInterestRepository
from .photo import IProfilePhotoS3Repository, IProfilePhotoRepository
