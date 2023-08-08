from enum import Enum


class GenderEnum(Enum):
    male = 0
    female = 1


class LookingGenderEnum(Enum):
    nevemind = -1
    male = 0
    female = 1


class PhotoProcessStatusEnum(Enum):
    approved = 1
    processing = 0
    rejected = -1