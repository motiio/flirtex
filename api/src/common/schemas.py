from src.config.schemas import ORJSONSchema


class CityReadSchema(ORJSONSchema):
    id: int
    name: str

    class Config:
        orm_mode = True


class InterestOutResponse(ORJSONSchema):
    id: int
    name: str

    class Config:
        orm_mode = True
